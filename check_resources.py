#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Watch the agencies behind the resource pages, and say when one of them moves.

The resource pages promise a date. "Checked against the department's page on
21 August 2026" is a claim that somebody read that page that day, and it decays
the moment the department edits theirs. Nothing announced that before this
script: a grant round closing, an award ceiling moving from $10,000 to $12,000,
or a program going to a waitlist all look identical to a link checker, because
the URL keeps returning a cheerful 200.

So this does three separate jobs, and the third is the one that matters:

1. **Staleness.** Every entry in build_chrome.RESOURCE_CHECKED carries a date.
   Anything older than STALE_DAYS is reported, because a program page with no
   re-check behind it is exactly how a site ends up promising a credit that no
   longer exists.
2. **Reachability.** Every outbound source link on every generated resource
   page, checked by HTTP the way check_links.py checks the guide videos. A dead
   citation is worse than no citation.
3. **Drift.** A fingerprint of each source page's visible text, stored in
   SOURCES_FILE and compared on the next run. When the fingerprint moves, the
   script reports *what* moved: the dollar figures, the years, and the
   program-status words, which is nearly always where the answer is.

Job 3 is deliberately not a raw HTML diff. Government sites rewrite markup,
rotate nonces and stamp build dates on every response, so hashing the source
reports a change every single run and gets ignored inside a week. Hashing the
visible text with the volatile bits stripped is quiet enough to be believed.

**A drift report is a prompt to go and read the page, never a fact by itself.**
This script cannot tell you a grant changed. It tells you the page changed, and
which numbers are on it now. A human then reads the source, edits the page, and
moves the date in RESOURCE_CHECKED. That order matters and is the whole point:
the site's promise is that a person checked, not that a script did.

Run:  python check_resources.py
      python check_resources.py --update     accept current state as the baseline
      python check_resources.py --stale-only skip the network, just report dates

Exit: 0 if nothing needs attention, 1 if something does.

No third-party dependencies, on purpose: this has to keep working on a fresh
clone with nothing installed but Python.
"""

import argparse
import datetime
import hashlib
import html
import json
import os
import re
import sys
import urllib.error
import urllib.request

from build_chrome import RESOURCE_CHECKED

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
SOURCES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "resource_sources.json")

# Committed on purpose. The baseline is the record of what these agencies said
# when we last looked, so a git diff on this file is the history of who changed
# what. A gitignored cache would lose that on every clone.

STALE_DAYS = 90
TIMEOUT = 25
UA = ("Mozilla/5.0 (compatible; GulfCoastResourceCheck/1.0; "
      "+https://gulfcoasthomemaintenance.com)")

# Hosts that refuse automated clients at the firewall. ldi.la.gov returns 403
# to any non-browser request, and a browser User-Agent does not change that, so
# it is a challenge this script cannot pass by being more polite. It is not
# going to be passed by being less polite either: spoofing harder to get around
# a state agency's bot protection is not something this project does. They are
# reported separately from failures, because a source that always reports DEAD
# trains everybody to ignore the output, which costs more than the check is
# worth. At re-check time these get opened by hand.
MANUAL_HOSTS = ("ldi.la.gov",)

# Hosts that are ours, or are type and not content. Never checked.
SKIP_HOSTS = ("gulfcoasthomemaintenance.com", "fonts.googleapis.com",
              "fonts.gstatic.com", "etsy.com", "www.etsy.com")

# The words that mean a program's door just opened or shut. Case-insensitive.
# Keep this list short and specific: every vague word added here costs a false
# alarm on some agency's boilerplate, and a checker nobody believes is worse
# than no checker.
STATUS_WORDS = (
    "applications are closed", "applications are open", "now accepting",
    "no longer accepting", "not currently accepting", "currently closed",
    "currently open", "waitlist", "wait list", "lottery", "suspended",
    "paused", "reopens", "reopening", "closed for", "opens on",
    "funding is exhausted", "funds are exhausted", "no longer available",
    "program has ended", "deadline",
)

MONTHS = ("january", "february", "march", "april", "may", "june", "july",
          "august", "september", "october", "november", "december")


# --------------------------------------------------------------- text extraction

def visible_text(markup):
    """Strip a page to the words a reader would see, normalized flat.

    Deliberately crude, and that is the right trade. A parser that understood
    every agency's markup would still be guessing at which div is the content,
    and the fingerprint only has to be stable, not beautiful.
    """
    text = re.sub(r"(?is)<(script|style|noscript|svg|head)\b.*?</\1>", " ", markup)
    text = re.sub(r"(?s)<!--.*?-->", " ", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    text = html.unescape(text)
    # Volatile by nature: cache-busting query strings and clock stamps that
    # change on every request and would otherwise report drift forever.
    text = re.sub(r"\b\d{1,2}:\d{2}(:\d{2})?\s*(am|pm)?\b", " ", text, flags=re.I)
    text = re.sub(r"\bsessionid\b\S*", " ", text, flags=re.I)
    return re.sub(r"\s+", " ", text).strip()


def signals(text):
    """Pull the few things worth reporting when a page moves.

    Dollars and years cover award ceilings, income caps and program dates.
    The status words cover the single most consequential change an agency can
    make without touching either: closing the door.
    """
    low = text.lower()
    dollars = sorted(set(re.findall(r"\$\s?[\d,]+(?:\.\d{2})?", text)),
                     key=lambda s: (-len(s), s))
    years = sorted(set(re.findall(r"\b(?:19|20)\d{2}\b", text)))
    status = sorted({w for w in STATUS_WORDS if w in low})
    dates = sorted({m.group(0).strip().lower()
                    for m in re.finditer(
                        r"\b(?:%s)\s+\d{1,2},?\s+(?:19|20)\d{2}\b" % "|".join(MONTHS),
                        text, flags=re.I)})
    return {
        "dollars": dollars[:25],
        "years": years[:25],
        "status": status,
        "dates": dates[:15],
    }


def fingerprint(text):
    return hashlib.sha256(text.encode("utf-8", "replace")).hexdigest()[:16]


# --------------------------------------------------------------- the pages

def resource_slugs():
    """Every resource page that actually exists on disk, in slug order."""
    root = os.path.join(DOCS, "resources")
    if not os.path.isdir(root):
        return []
    return sorted(name for name in os.listdir(root)
                  if os.path.isfile(os.path.join(root, name, "index.html")))


def cited_urls(slug):
    """The outbound sources one resource page sends a reader to."""
    path = os.path.join(DOCS, "resources", slug, "index.html")
    with open(path, encoding="utf-8") as handle:
        markup = handle.read()
    found = []
    for url in re.findall(r'href="(https?://[^"]+)"', markup):
        if any(host in url for host in SKIP_HOSTS):
            continue
        url = url.rstrip("/") or url
        if url not in found:
            found.append(url)
    return found


def parse_checked(value):
    """'21 August 2026' -> date. Returns None rather than raising."""
    for fmt in ("%d %B %Y", "%B %d, %Y", "%B %d %Y"):
        try:
            return datetime.datetime.strptime(value.strip(), fmt).date()
        except ValueError:
            continue
    return None


# --------------------------------------------------------------- network

def fetch(url):
    """Return (ok, text_or_note). Never raises."""
    request = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.9",
    })
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            raw = response.read(3_000_000)
            charset = response.headers.get_content_charset() or "utf-8"
            return True, raw.decode(charset, "replace")
    except urllib.error.HTTPError as error:
        return False, "HTTP %d" % error.code
    except Exception as error:                  # DNS, TLS, timeout, refusal
        return False, type(error).__name__


# --------------------------------------------------------------- reporting

def describe_change(before, now):
    """Human-readable list of what moved between two signal sets."""
    lines = []
    for key, label in (("status", "status wording"), ("dollars", "dollar figures"),
                       ("dates", "dates"), ("years", "years")):
        was, is_ = set(before.get(key, [])), set(now.get(key, []))
        gone, new = sorted(was - is_), sorted(is_ - was)
        if not gone and not new:
            continue
        parts = []
        if new:
            parts.append("added " + ", ".join(new[:6]))
        if gone:
            parts.append("removed " + ", ".join(gone[:6]))
        lines.append("      %s: %s" % (label, "; ".join(parts)))
    return lines


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument("--update", action="store_true",
                        help="write current state as the new baseline")
    parser.add_argument("--stale-only", action="store_true",
                        help="report checked dates only, touch no network")
    parser.add_argument("--stale-days", type=int, default=STALE_DAYS)
    args = parser.parse_args()

    today = datetime.date.today()
    problems = []

    # ---- 1. staleness ------------------------------------------------------
    print("Checked dates")
    print("-" * 70)
    for slug in sorted(RESOURCE_CHECKED):
        _, when = RESOURCE_CHECKED[slug]
        date = parse_checked(when)
        if date is None:
            print("  ?    %-32s unparseable date %r" % (slug, when))
            problems.append((slug, "checked date does not parse: %r" % when))
            continue
        age = (today - date).days
        flag = "STALE" if age > args.stale_days else "ok   "
        print("  %s %-32s %s (%d days)" % (flag, slug, when, age))
        if age > args.stale_days:
            problems.append((slug, "checked %d days ago, over the %d day limit"
                             % (age, args.stale_days)))

    missing = set(resource_slugs()) - set(RESOURCE_CHECKED)
    for slug in sorted(missing):
        print("  MISS %-32s page exists with no RESOURCE_CHECKED entry" % slug)
        problems.append((slug, "no RESOURCE_CHECKED entry"))

    if args.stale_only:
        return report(problems)

    # ---- 2 and 3. reachability and drift ----------------------------------
    baseline = {}
    if os.path.exists(SOURCES_FILE):
        with open(SOURCES_FILE, encoding="utf-8") as handle:
            baseline = json.load(handle).get("sources", {})

    current = {}
    seen = {}
    manual = []
    print("\nSources")
    print("-" * 70)
    for slug in resource_slugs():
        urls = cited_urls(slug)
        if not urls:
            continue
        print("\n%s" % slug)
        for url in urls:
            if url in seen:
                print("  ---- %s\n       (already checked above)" % url)
                continue
            if any(host in url for host in MANUAL_HOSTS):
                print("  BYHAND %s\n       blocks automated checks, open it yourself" % url)
                manual.append((slug, url))
                seen[url] = None
                continue

            ok, payload = fetch(url)
            if not ok:
                print("  DEAD %s\n       %s" % (url, payload))
                problems.append((slug, "%s unreachable: %s" % (url, payload)))
                seen[url] = None
                # Keep the old baseline rather than erasing it on a blip.
                if url in baseline:
                    current[url] = baseline[url]
                continue

            text = visible_text(payload)
            entry = {"hash": fingerprint(text), "chars": len(text),
                     "signals": signals(text), "last_seen": today.isoformat()}
            seen[url] = entry
            current[url] = entry

            was = baseline.get(url)
            if was is None:
                print("  NEW  %s\n       baseline recorded, %d chars" % (url, len(text)))
            elif was.get("hash") == entry["hash"]:
                print("  same %s" % url)
            else:
                # Confirm before reporting. citizensfla.com served two different
                # bodies inside one run of this script, which is a load balancer
                # or a rotating banner rather than news about the wind pool. One
                # re-fetch costs a second and removes the whole class of false
                # alarm that would otherwise train everybody to ignore this.
                again_ok, again = fetch(url)
                if again_ok and fingerprint(visible_text(again)) == was.get("hash"):
                    print("  same %s\n       (differed once, matched on re-fetch,"
                          " treated as transient)" % url)
                    current[url] = was
                    seen[url] = was
                    continue

                delta = len(text) - was.get("chars", 0)
                detail = describe_change(was.get("signals", {}), entry["signals"])
                kind = "figures or status moved" if detail else "prose only"
                print("  MOVED %s\n       text changed (%+d chars, %s)"
                      % (url, delta, kind))
                for line in detail:
                    print(line)
                if not detail:
                    # Worth saying out loud: an eligibility rule can change
                    # completely without a dollar sign in it. "three consecutive
                    # policy years" becoming "two" is prose. Prose-only is a
                    # lower alarm, never a dismissal.
                    print("      no dollar figure, date or status word changed;"
                          " read it for wording")
                problems.append((slug, "%s changed since last check (%s)"
                                 % (url, kind)))

    if manual:
        print("\nBy hand")
        print("-" * 70)
        print("These block automated checks, so they are the ones to open in a")
        print("browser whenever their page is being re-checked:")
        for slug, url in manual:
            print("  %-32s %s" % (slug, url))

    if args.update or not baseline:
        merged = dict(baseline)
        merged.update(current)
        with open(SOURCES_FILE, "w", encoding="utf-8") as handle:
            json.dump({"updated": today.isoformat(), "sources": merged},
                      handle, indent=2, sort_keys=True)
            handle.write("\n")
        print("\nBaseline written to %s" % os.path.basename(SOURCES_FILE))

    return report(problems)


def report(problems):
    print("\n" + "=" * 70)
    if not problems:
        print("Nothing needs attention.")
        return 0
    print("%d thing(s) need attention:\n" % len(problems))
    for slug, note in problems:
        print("  %-32s %s" % (slug, note))
    print("\nA MOVED source is a prompt to go and read that page, not a finding.")
    print("Read it, correct the page if it is wrong, move the date in")
    print("RESOURCE_CHECKED, rebuild, then run with --update to accept the new")
    print("baseline.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
