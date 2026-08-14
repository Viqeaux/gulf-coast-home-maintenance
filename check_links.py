#!/usr/bin/env python3
"""
Check every curated guide link in build_calendars.GUIDES still works.

Videos get deleted, set to private, or taken down by their uploader, and none of
that announces itself. The link keeps returning a perfectly healthy page that
says "Video unavailable". So YouTube links are checked through the oEmbed
endpoint, which returns an error for anything that can no longer be watched.
Everything else is checked by HTTP status.

Run:  python check_links.py
Exit: 0 if everything resolves, 1 if anything needs attention.

Worth running after editing GUIDES, and every month or two otherwise.
"""

import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

from build_calendars import GUIDES, TASKS

TIMEOUT = 20
UA = "Mozilla/5.0 (compatible; GulfCoastLinkCheck/1.0)"

YOUTUBE_HOSTS = ("youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be")


def youtube_id(url):
    """Return the video id if this is a YouTube link, else None."""
    parts = urllib.parse.urlparse(url)
    if parts.netloc not in YOUTUBE_HOSTS:
        return None
    if parts.netloc == "youtu.be":
        return parts.path.lstrip("/") or None
    if parts.path == "/watch":
        return urllib.parse.parse_qs(parts.query).get("v", [None])[0]
    match = re.match(r"^/(?:shorts|embed|v)/([\w-]+)", parts.path)
    return match.group(1) if match else None


def fetch(url, method="GET"):
    request = urllib.request.Request(url, method=method, headers={"User-Agent": UA})
    return urllib.request.urlopen(request, timeout=TIMEOUT)


def check(url):
    """Return (ok, note) for one URL."""
    video = youtube_id(url)
    if video:
        # oEmbed 404s for deleted, private and region-blocked videos, where the
        # watch page itself would still return a cheerful 200.
        probe = ("https://www.youtube.com/oembed?format=json&url="
                 + urllib.parse.quote("https://www.youtube.com/watch?v=" + video,
                                      safe=""))
        try:
            with fetch(probe) as response:
                data = json.loads(response.read().decode("utf-8"))
            return True, "ok, " + data.get("title", "")[:60]
        except urllib.error.HTTPError as error:
            if error.code in (401, 403, 404):
                return False, "UNAVAILABLE (deleted, private, or blocked)"
            return False, "HTTP {0}".format(error.code)
        except Exception as error:                      # network, DNS, timeout
            return False, type(error).__name__

    try:
        with fetch(url, method="HEAD") as response:
            return True, "ok, HTTP {0}".format(response.status)
    except urllib.error.HTTPError as error:
        if error.code in (403, 405):                    # some hosts refuse HEAD
            try:
                with fetch(url) as response:
                    return True, "ok, HTTP {0}".format(response.status)
            except Exception as inner:
                return False, "{0} on retry".format(type(inner).__name__)
        return False, "HTTP {0}".format(error.code)
    except Exception as error:
        return False, type(error).__name__


def main():
    titles = {t[3]: t[4] for t in TASKS}
    problems = []
    checked = 0

    if not GUIDES:
        print("No guides curated yet, so there is nothing to check.")
        print("Add entries to GUIDES in build_calendars.py.")
        return 0

    for slug in sorted(GUIDES):
        if slug not in titles:
            problems.append((slug, "", "slug is not a task in TASKS"))
            print("{0}\n  ! slug does not match any task".format(slug))
            continue

        print("{0}  ({1})".format(titles[slug], slug))
        for label, url, source in GUIDES[slug]:
            ok, note = check(url)
            checked += 1
            print("  {0} {1}\n      {2}".format("OK  " if ok else "DEAD", label, note))
            if not ok:
                problems.append((slug, url, note))
        print()

    print("-" * 66)
    print("{0} links checked across {1} tasks".format(checked, len(GUIDES)))
    if problems:
        print("\n{0} need attention:".format(len(problems)))
        for slug, url, note in problems:
            print("  {0}\n    {1}\n    {2}".format(slug, url, note))
        return 1
    print("All good.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
