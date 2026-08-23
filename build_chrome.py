#!/usr/bin/env python3
"""Write the shared bar and footer into every hand-written page.

Run this after changing site_chrome.py, or after adding a page. It rewrites
two regions in each file and touches nothing else: the <div class="topbar">
block and the <footer> block. Everything between them is the page's own words
and is never read or moved.

/guides/ and /calculator/ are not listed here. They are generated already, by
build_calendars.py and build_calculator.py, and those two import site_chrome
directly. Running all three is what a full site build is.

    python build_chrome.py && python build_calendars.py && python build_calculator.py
"""

import io
import os
import sys

import site_chrome
from build_calendars import VERSION

DOCS = "docs"

# The one slot in the footer: content that belongs to a page rather than to the
# site. Kept here rather than in the pages, because the footer around it is
# rewritten on every run and anything left inside would be lost.
#
# The resource pages each name the institution they were checked against and
# the date they were checked, which is the promise those pages are built on.
# Move the date when you re-check the facts, not when you edit the wording.
RESOURCE_CHECKED = {
    "flood-insurance-30-day-rule":  ("FEMA's pages",          "22 August 2026"),
    "louisiana-fortify-homes":      ("the department's page", "22 August 2026"),
    "my-safe-florida-home":         ("the program's pages",   "22 August 2026"),
    "strengthen-alabama-homes":     ("the program's pages",   "22 August 2026"),
    "strengthen-mississippi-homes": ("the department's page", "21 August 2026"),
    "texas-windstorm-coverage":     ("the sources",           "22 August 2026"),
    "wind-mitigation-discounts":    ("the sources",           "22 August 2026"),
}

SIGNUP = """    <div class="foot-signup">
      <div>
        <p class="fs-title">Hear about the next one</p>
        <p class="fs-sub">I'm still building tools like this. Leave your email
        and I'll tell you when there's something new. That is all the list is
        for.</p>
      </div>
      <div>
        <form class="signup" method="post" target="ml-sink"
              action="https://assets.mailerlite.com/jsonp/2575029/forms/195731645629727806/subscribe">
          <div class="signup-row">
            <label class="sr-only" for="signup-email">Your email address</label>
            <input id="signup-email" type="email" name="fields[email]" required
                   autocomplete="email" placeholder="you@example.com">
            <button class="btn btn--buy" type="submit">Keep me posted</button>
          </div>
          <div class="sr-only" aria-hidden="true">
            <label for="signup-website">Leave this field empty</label>
            <input id="signup-website" type="text" name="website"
                   tabindex="-1" autocomplete="off">
          </div>
          <p class="signup-note">
            Only when there's something new, which is not often. Leave any time.
            <a href="privacy.html" style="color:var(--sand-lift)">What happens to your email.</a>
          </p>
          <input type="hidden" name="ml-submit" value="1">
          <input type="hidden" name="anticsrf" value="true">
        </form>
        <p class="signup-done" hidden>
          <strong>Nearly there, check your email.</strong>
          You'll have a confirmation link waiting; the list won't have you until you click it.
        </p>
        <iframe name="ml-sink" title="Signup handler" hidden></iframe>
      </div>
    </div>"""


# The privacy page says, in its own body, that "the date below changes" if
# anything about tracking changes. That makes the date part of the promise
# rather than decoration, so it survives here rather than in the page. The old
# version of this line said "Back to the calendars" and linked to the site
# root, which is not the calendars; the audit caught it as M18.
PRIVACY = ('''    <p class="foot-correction">
      Questions about any of this go to the
      <a href="https://www.etsy.com/shop/GulfCoastHomeCare" target="_blank" rel="noopener">Etsy shop</a>,
      where messages reach me.
    </p>
    <p class="updated">Last updated 22 August 2026</p>''')


def resource_prelude(slug, prefix):
    agency, date = RESOURCE_CHECKED[slug]
    return ('    <p class="foot-correction">\n'
            '      Spotted something above that no longer matches %s?\n'
            '      Message the\n'
            '      <a href="%s" target="_blank" rel="noopener">Etsy shop</a>\n'
            '      and it gets fixed.\n'
            '    </p>\n'
            '    <p class="updated">Links checked %s</p>'
            % (agency, site_chrome.ETSY, date))


# path, prefix, current, prelude, absolute, footer?
def pages():
    out = [
        ("index.html",           "",     "",            SIGNUP, False, True),
        ("privacy.html",         "",     "privacy.html", PRIVACY, False, True),
        # 404 is served from any address, so its links have to be root
        # absolute. It keeps its own austere card instead of a footer: a page
        # that exists to get you unstuck already carries three ways out, and
        # the bar above now carries the rest.
        ("404.html",             "",     None,          "",     True,  False),
        ("calendars/index.html", "../",  "calendars/",  "",     False, True),
        ("shop/index.html",      "../",  "shop/",       "",     False, True),
        ("storm/index.html",     "../",  "storm/",      "",     False, True),
        ("resources/index.html", "../",  "resources/",  "",     False, True),
        ("about/index.html",     "../",  "about/",      "",     False, True),
    ]
    for slug in sorted(RESOURCE_CHECKED):
        path = "resources/%s/index.html" % slug
        cur = "resources/%s/" % slug
        out.append((path, "../../", cur, resource_prelude(slug, "../../"), False, True))
    return out


def newest_checked():
    """The most recent date in RESOURCE_CHECKED, written as it is on the pages.

    The home page's grant row asserts dollar figures and eligibility with no
    date of its own. Rather than a second date to keep in step, it reports the
    newest of the ones the detail pages already carry, so re-checking a program
    and moving its date here is what updates the front door too.
    """
    months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"]

    def key(text):
        day, month, year = text.split()
        return (int(year), months.index(month), int(day))

    return max((d for _, d in RESOURCE_CHECKED.values()), key=key)


def replace_span(text, span_id, inner):
    """Rewrite the contents of one <span id="...">, leaving the tag alone."""
    open_tag = '<span id="%s">' % span_id
    i = text.find(open_tag)
    if i < 0:
        return text
    j = text.index("</span>", i)
    return text[:i + len(open_tag)] + inner + text[j:]


def replace_block(text, open_tag, path):
    """Swap the region from open_tag to its matching close.

    Counts nesting rather than regex-matching, because the footer contains
    divs and the topbar contains several.
    """
    tag = open_tag.split()[0].lstrip("<").rstrip(">")
    start = text.find(open_tag)
    if start < 0:
        return None
    depth, i = 0, start
    op, cl = "<" + tag, "</" + tag + ">"
    while i < len(text):
        if text.startswith(op, i):
            depth += 1
            i += len(op)
        elif text.startswith(cl, i):
            depth -= 1
            i += len(cl)
            if depth == 0:
                return start, i
        else:
            i += 1
    raise SystemExit("unbalanced <%s> in %s" % (tag, path))


def main():
    changed = 0
    for rel, prefix, current, prelude, absolute, wants_footer in pages():
        path = os.path.join(DOCS, rel)
        original = io.open(path, encoding="utf-8").read()
        text = original

        span = replace_block(text, '<div class="topbar">', rel)
        if span is None:
            raise SystemExit("no topbar in %s" % rel)
        bar = site_chrome.topbar(prefix=prefix, current=current, absolute=absolute)
        text = text[:span[0]] + bar + text[span[1]:]

        if wants_footer:
            span = replace_block(text, "<footer>", rel)
            if span is None:
                raise SystemExit("no footer in %s" % rel)
            foot = site_chrome.footer(prefix=prefix, version=VERSION,
                                      prelude=prelude, absolute=absolute)
            text = text[:span[0]] + foot + text[span[1]:]

        if rel == "index.html":
            text = replace_span(text, "grants-checked",
                                "Most recently checked %s." % newest_checked())

        if text != original:
            io.open(path, "w", encoding="utf-8", newline="\n").write(text)
            changed += 1
            print("  %s" % rel)

    print("%d of %d pages rewritten" % (changed, len(pages())))
    print("Now run build_calendars.py and build_calculator.py for the other two.")


if __name__ == "__main__":
    main()
