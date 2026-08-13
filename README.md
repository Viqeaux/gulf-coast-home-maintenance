# Gulf Coast Home Maintenance — Digital Companion

Three subscribe-able calendar feeds and the landing page that hands them out.

Built to the spec in `gulf-coast-maintenance-calendar-content.md`, which is kept
out of this repo on purpose — see [.gitignore](.gitignore) for why.

```
build_calendars.py   all task content + the ICS generator (edit this)
optimize_images.py   resizes the hero photo for the web
docs/                published by GitHub Pages, exactly as-is
  gulf-coast-must-do.ics       12 events
  gulf-coast-should-do.ics     12 events
  gulf-coast-going-above.ics   12 events
  index.html                   the landing page the QR code points to
  img/hero-1600.jpg            hero, desktop
  img/hero-900.jpg             hero, mobile
  img/hero.png                 the master — local only, not published
  .nojekyll                    stops Pages running the site through Jekyll
```

Regenerate after editing task content:

```bash
python build_calendars.py
```

Regenerate after replacing `docs/img/hero.png`:

```bash
python optimize_images.py
```

## What the events look like

- One all-day event per task, no alert attached.
- `RRULE:FREQ=YEARLY` with no `UNTIL` — repeats forever, matching the undated print edition.
- Anchored to the 1st of each month, with two deliberate exceptions: **May 1**
  (hurricane prep, leaving room for the 30-day flood insurance window before June 1)
  and **November 30** (season close / post-season inspection).
- Description holds the task, the reason it matters, and the disclaimer. The
  how-to video link goes here later — add it to the body text in `TASKS`.
- Marked `TRANSP:TRANSPARENT`, so they don't make you look busy to anyone who
  checks your availability.

The first occurrence is anchored to 2026 (`ANCHOR_YEAR`). That only sets where the
series starts, not when it ends — subscribers see this year and every year after.

## Publishing

The landing page builds its own subscribe links from whatever URL it's served
from, so there is nothing to find-and-replace. Upload the contents of `docs/`
to any static host, keeping the same layout, and it works.

Two requirements from Google:

1. **HTTPS, publicly reachable.** Google's servers fetch the file themselves —
   it can't be behind a login, a private repo, or localhost.
2. **Served as `text/calendar`.** GitHub Pages, Netlify, and Cloudflare Pages all
   do this for `.ics` automatically. Some hosts serve it as `text/plain`, which
   Google rejects.

Then point the back-cover QR code at the landing page URL, not at an `.ics` file
directly — the page is what lets someone pick a tier and gives them instructions.

### GitHub Pages

The build writes to `docs/` because Pages can only serve from the repo root or
from `/docs`. That means no workflow and no config: in the repo's
**Settings → Pages**, set source to **Deploy from a branch**, branch `main`,
folder `/docs`. The empty `.nojekyll` file stops Pages from running the site
through Jekyll on the way out.

After any content change: re-run the build, commit, push. Pages redeploys in
about a minute; Google then picks it up on its own slower schedule.

### Why subscribing does nothing until it's hosted

Google doesn't read the calendar file from your browser — it stores the URL and
its own servers go fetch it. So a file opened from your hard drive, or served
from `localhost`, is invisible to Google. Pressing **Add to Google Calendar**
in that state just opens Google Calendar and adds nothing, with no error.

The landing page checks for this: off a public HTTPS origin it hides the two
subscribe buttons, leaves **Download .ics**, and explains why. If you ever see
that banner on the real site, the host is the problem — most likely it's serving
over `http://` or the domain isn't public yet.

## Adding a calendar in Google Calendar

The mobile app can't subscribe to a URL. It has to be done once from a browser,
then it syncs to every device on that account.

The landing page's **Add to Google Calendar** button handles this. To do it by
hand: Google Calendar → **Other calendars** → **+** → **From URL** → paste the
`https://` address of the `.ics` file → **Add calendar**.

Two things worth telling buyers up front, because both generate support email:

- **Google refreshes subscribed calendars slowly** — up to a day, occasionally
  longer. Nothing in this calendar is time-critical to the hour.
- **Subscribing is not importing.** Import is a one-time copy that never updates
  and duplicates itself if you do it twice. Subscribing is what lets you improve
  the content later and have existing owners get the fix.

## Editing the content later

All twelve months for all three tiers live in the `TASKS` list in
`build_calendars.py`, as `(month, day, tier, slug, title, body)`.

When you publish a change to a feed people already subscribe to:

- **Bump `SEQUENCE`** at the top of the script. Calendar clients use it to tell a
  real update from a re-fetch of the same data.
- **Don't change a `slug`.** It becomes the event's `UID`. Changing it reads as
  "old event deleted, unrelated new event created" to every existing subscriber.
  Rewriting a title or body under the same slug is a clean update.

## Verifying a change

`python build_calendars.py` will happily produce a malformed file if the content
has a quoting mistake, so it's worth a look at the output — 12 events per file,
each with a `DTSTART`, an `RRULE`, and a description that reads correctly after
the line wrapping. The generator handles RFC 5545 escaping and 75-octet folding;
what it can't check is whether the words are right.

---

*General maintenance guidance, not a substitute for a licensed inspector,
contractor, or your insurance policy terms.*
