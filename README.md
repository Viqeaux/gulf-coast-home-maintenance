# Gulf Coast Home Maintenance

The printable calendar that gets sold, three subscribe-able calendar feeds, and
the landing page that hands the feeds out.

Built to the spec in `gulf-coast-maintenance-calendar-content.md`, which is kept
out of this repo on purpose — see [.gitignore](.gitignore) for why.

```
build_calendars.py   task content, curated video links, and the feed generator
build_pdf.py         the printable edition — the product
product_content.py   the paid-only pages — local only, not published
check_links.py       finds curated videos that have gone dead
optimize_images.py   resizes the hero photo for the web
product/             built by build_pdf.py — local only, except the listing copy
  Gulf-Coast-Home-Maintenance-Calendar.pdf   20 pages, US Letter
  listing/                                   Etsy photos, 00-hero.png first
  etsy-listing.md                            the copy to paste into Etsy
docs/                published by GitHub Pages, exactly as-is
  gulf-coast-must-do.ics       12 events
  gulf-coast-should-do.ics     12 events
  gulf-coast-going-above.ics   12 events
  index.html                   the landing page the QR code points to
  guides/index.html            generated — one anchor per task
  theme.css                    the palette, shared by both pages
  img/hero-1600.jpg            hero, desktop
  img/hero-900.jpg             hero, mobile
  img/hero.png                 the master — local only, not published
  .nojekyll                    stops Pages running the site through Jekyll
```

`docs/guides/index.html` is generated — edit `build_calendars.py`, not the HTML.
`docs/index.html` is hand-written.

Regenerate after editing task content:

```bash
python build_calendars.py
```

Regenerate after replacing `docs/img/hero.png`:

```bash
python optimize_images.py
```

Rebuild the product and its listing images:

```bash
python build_pdf.py
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

## What has been checked on real devices

Everything up to the point where the operating system takes over is verified
automatically — the feeds parse, the links are well formed, the files serve as
`text/calendar`. The last hop is the part no amount of local testing can prove,
because it depends on what the device decides to do with the link.

| Path | Status |
|---|---|
| Desktop browser → Google Calendar | Confirmed working |
| iPhone → **Subscribe (Apple / Outlook)** | Confirmed working, 2026-08-13 |
| Android → **Add to Google Calendar** | **Not yet tested** |

The Android case is the one that matters, because it decides whether the
Android-only card on the landing page earns its place. Android can hand a
`calendar.google.com` link to the Google Calendar app, which cannot subscribe to
a URL — but whether it does depends on a per-device setting, so it will hit some
visitors and not others. If it turns out to be rare, that card is noise and
should go.

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

## Adding a how-to video

Videos are other people's, linked rather than republished. They live in the
`GUIDES` table in `build_calendars.py`, keyed by task slug:

```python
GUIDES = {
    "oct-flush-water-heater": [
        ("Flushing a tank water heater", "https://www.youtube.com/watch?v=...",
         "This Old House"),
    ],
}
```

Then `python build_calendars.py` and `python check_links.py`.

A task with no entry gets no link in its calendar event, so the list can be
filled in a few at a time without anyone following a link to an empty section.

**Calendar events link to our guides page, never straight to YouTube.** Two
reasons, both of which matter more than they look:

- A dead video gets fixed in one place. A URL baked into the feed only reaches
  subscribers on their next refresh, which can take a day.
- Someone following that link was just reminded to do this exact job. That is
  the most motivated visitor the site will ever get, and they should land on it
  rather than be handed to YouTube.

**Videos disappear silently** — deleted, set to private, or region-blocked — and
the URL keeps returning a healthy page that says "Video unavailable". That is
why `check_links.py` checks YouTube through its oEmbed endpoint rather than by
HTTP status. Run it after editing `GUIDES`, and every month or two regardless.

## The printable edition

`build_pdf.py` builds the free download: a 20-page US Letter PDF, plus the
images for the Etsy listing. It needs three packages that the rest of the
project does not — `reportlab`, `segno` for the QR code, and `pypdfium2` to
turn pages into listing photos:

```bash
python -m pip install "reportlab<4.1" segno pypdfium2
```

The `<4.1` pin is not cosmetic. Newer reportlab calls `md5(usedforsecurity=…)`,
which needs Python 3.9, and the `python` on this machine is 3.8. If you move to
a newer interpreter, drop the pin.

The pages are: cover, how it works, the Gulf Coast year, your first month, the
twelve months, the Big Ticket Watch List, how to date what you own, the free
phone calendars, and the licence.

Two sources feed it, and the split is the whole design:

- **`build_calendars.py`** holds the twelve months of tasks, shared with the
  `.ics` feeds. Editing a task changes the print edition and the digital one
  together, so the two cannot drift apart and say different things.
- **`product_content.py`** holds the pages the feeds do not carry — the Watch
  List lifespans, the dating page, the first-month checklist, the licence.

The PDF and the listing images are gitignored, but only as build artifacts.
Nothing in them is held back — the calendar is a free download — and they are
not served from `docs/` either, so committing them would put binaries in the
repo that nothing reads.

Interior pages are white on purpose. It is a print-at-home file, and a
full-bleed tinted page costs the reader a cartridge to save us nothing. The
serif is Times, one of the fourteen fonts every PDF reader already has, so
nothing that could substitute badly on someone else's printer is embedded; the
sans is Bitstream Vera, which ships inside reportlab under a licence that
allows it.

## Selling it

The Etsy shop is **GulfCoastHomeCare** — `etsy.com/shop/GulfCoastHomeCare`. The
name is shorter than the domain because Etsy caps shop names at 20 characters
with no spaces; "Gulf Coast" was the half worth keeping intact.

**The calendar is the free download, not the product.** It goes up at the
lowest price Etsy allows — there is no $0 there, the floor is $0.20 — because a
free listing is how a new shop gets found. Views, favourites and reviews
accumulate far faster on something free, and that standing is what the paid kit
inherits when it lists later. The kit is the thing that will be for sale.

The listing copy — title, description, all thirteen tags, the price reasoning,
and the photo order — lives in
[product/etsy-listing.md](product/etsy-listing.md). The first photo is composed
at 4:3 rather than being a page render, because Etsy crops the search-grid
thumbnail to 4:3 and would otherwise slice the title off the cover.

When there is a published listing, paste its URL into `SHOP_URL` at the bottom
of `docs/index.html`. That swaps the waitlist for a download button, which is
the right trade — once the thing is downloadable the waitlist has done its job,
and it can start collecting against the kit instead.

Use the **listing** URL rather than the shop URL, so people land on the
download instead of a shop front they have to search. And don't link the shop
at all until something is listed: an empty shop reads as abandoned.

One thing to watch later: Etsy's fee-avoidance policy forbids using a listing
to route buyers somewhere else to purchase. Naming the domain is harmless while
the site sells nothing. When the kit is for sale on both, revisit the FAQ line
in the listing copy that mentions it.

## Cutting a version

Versions are tracked in [CHANGELOG.md](CHANGELOG.md), which explains what counts
as major, minor, and patch here. To release:

1. Rebuild if task content changed: `python build_calendars.py`
2. Add the entry at the top of `CHANGELOG.md`
3. Update the version in the footer of `docs/index.html`
4. Commit, then tag and push:

```bash
git tag -a v1.0.1 -m "Short description" && git push origin main --follow-tags
```

Two things that are easy to conflate:

- **The version number is for you.** It tracks the project and appears in the
  page footer so a tester can tell you which build they were looking at.
- **`SEQUENCE` is for subscribers.** It lives in `build_calendars.py` and is what
  tells a calendar client an event actually changed. Bump it whenever you edit
  task content — a version bump alone does not do it, and a `SEQUENCE` bump is
  not needed for a design-only release.

To see what a released version contained: `git show v1.0.0 --stat`.

---

*General maintenance guidance, not a substitute for a licensed inspector,
contractor, or your insurance policy terms.*
