# Gulf Coast Home Maintenance

Two products from one set of content:

- **The calendar** is free. Three subscribe-able `.ics` feeds, plus the landing
  page and how-to guides that hand them out. Lives on
  <https://gulfcoasthomemaintenance.com>.
- **The kit** is paid. Every printable page, 27 of them, sold on Etsy at $12.99.
  Built locally and never committed, because this repo is public.

Built to the spec in `gulf-coast-maintenance-calendar-content.md`, which is kept
out of this repo on purpose, see [.gitignore](.gitignore) for why.

```
build_calendars.py        the 36 tasks, video links, and the feed generator
task_steps.py             step by step detail for each task
kit_sections.py           the "if you have one" pages, kit only
build_printables.py       renders the kit to HTML then PDF, via headless Chrome
build_listing_images.py   renders Etsy photos from the real kit pages
check_links.py            finds curated videos that have gone dead
optimize_images.py        resizes the hero photo for the web

product/                  the paid kit. Gitignored except the listing copy
  gulf-coast-home-maintenance-kit.pdf    27 pages, US Letter
  gulf-coast-home-maintenance-kit.html   what the PDF is rendered from
  listing/                               Etsy photos, 00-hero.png first
  etsy-listing.md                        title, tags and copy to paste in

docs/                     published by GitHub Pages, exactly as-is
  gulf-coast-must-do.ics       12 events
  gulf-coast-should-do.ics     12 events
  gulf-coast-going-above.ics   12 events
  index.html                   the landing page the QR code points to
  guides/index.html            generated, one anchor per task
  theme.css                    the palette, shared by both pages
  img/hero-1600.jpg            hero, desktop
  img/hero-900.jpg             hero, mobile
  img/hero.png                 the master, local only, not published
  CNAME                        the custom domain
  .nojekyll                    stops Pages running the site through Jekyll
```

`docs/guides/index.html` and everything in `product/` are generated. Edit the
Python, not the output. `docs/index.html` is hand-written.

Rebuild the feeds and the guides page, after editing tasks or steps:

```bash
python build_calendars.py
```

Rebuild the kit and its Etsy photos, after editing anything it contains:

```bash
python build_printables.py && python build_listing_images.py
```

Rebuild the web hero, after replacing `docs/img/hero.png`:

```bash
python optimize_images.py
```

## What the events look like

- One all-day event per task, no alert attached.
- `RRULE:FREQ=YEARLY` with no `UNTIL`. Repeats forever, matching the undated print edition.
- Anchored to the 1st of each month, with two deliberate exceptions: **May 1**
  (hurricane prep, leaving room for the 30-day flood insurance window before June 1)
  and **November 30** (season close / post-season inspection).
- Description holds the task, the reason it matters, and the disclaimer. The
  how-to video link goes here later. Add it to the body text in `TASKS`.
- Marked `TRANSP:TRANSPARENT`, so they don't make you look busy to anyone who
  checks your availability.

The first occurrence is anchored to 2026 (`ANCHOR_YEAR`). That only sets where the
series starts, not when it ends. Subscribers see this year and every year after.

## Publishing

The landing page builds its own subscribe links from whatever URL it's served
from, so there is nothing to find-and-replace. Upload the contents of `docs/`
to any static host, keeping the same layout, and it works.

Two requirements from Google:

1. **HTTPS, publicly reachable.** Google's servers fetch the file themselves. It can't be behind a login, a private repo, or localhost.
2. **Served as `text/calendar`.** GitHub Pages, Netlify, and Cloudflare Pages all
   do this for `.ics` automatically. Some hosts serve it as `text/plain`, which
   Google rejects.

Then point the back-cover QR code at the landing page URL, not at an `.ics` file
directly. The page is what lets someone pick a tier and gives them instructions.

### GitHub Pages

The build writes to `docs/` because Pages can only serve from the repo root or
from `/docs`. That means no workflow and no config: in the repo's
**Settings → Pages**, set source to **Deploy from a branch**, branch `main`,
folder `/docs`. The empty `.nojekyll` file stops Pages from running the site
through Jekyll on the way out.

After any content change: re-run the build, commit, push. Pages redeploys in
about a minute; Google then picks it up on its own slower schedule.

### Why subscribing does nothing until it's hosted

Google doesn't read the calendar file from your browser, it stores the URL and
its own servers go fetch it. So a file opened from your hard drive, or served
from `localhost`, is invisible to Google. Pressing **Add to Google Calendar**
in that state just opens Google Calendar and adds nothing, with no error.

The landing page checks for this: off a public HTTPS origin it hides the two
subscribe buttons, leaves **Download .ics**, and explains why. If you ever see
that banner on the real site, the host is the problem, most likely it's serving
over `http://` or the domain isn't public yet.

## What has been checked on real devices

Everything up to the point where the operating system takes over is verified
automatically. The feeds parse, the links are well formed, the files serve as
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
a URL, but whether it does depends on a per-device setting, so it will hit some
visitors and not others. If it turns out to be rare, that card is noise and
should go.

## Adding a calendar in Google Calendar

The mobile app can't subscribe to a URL. It has to be done once from a browser,
then it syncs to every device on that account.

The landing page's **Add to Google Calendar** button handles this. To do it by
hand: Google Calendar → **Other calendars** → **+** → **From URL** → paste the
`https://` address of the `.ics` file → **Add calendar**.

Two things worth telling buyers up front, because both generate support email:

- **Google refreshes subscribed calendars slowly**, up to a day, occasionally
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
has a quoting mistake, so it's worth a look at the output, 12 events per file,
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

**Videos disappear silently**. Deleted, set to private, or region-blocked, and
the URL keeps returning a healthy page that says "Video unavailable". That is
why `check_links.py` checks YouTube through its oEmbed endpoint rather than by
HTTP status. Run it after editing `GUIDES`, and every month or two regardless.

## The kit

`build_printables.py` builds the paid product: a 27-page US Letter PDF, laid out
in HTML and CSS and rendered by headless Chrome. No extra Python packages, and
nothing to install beyond a browser you already have.

The pages are: cover, how it works, the Gulf Coast year, your first month, the
twelve months with step by step detail, the Big Ticket Watch List, how to date
what you own, and seven "if you have one" sections.

Three sources feed it:

- **`build_calendars.py`** holds the twelve months of tasks, shared with the
  `.ics` feeds. Editing a task changes the kit and the calendar together, so the
  two cannot drift apart and say different things.
- **`task_steps.py`** holds the step by step detail, shared with the free guides
  page.
- **`kit_sections.py`** holds the conditional sections, which are kit only.

**Everything in `product/` is gitignored, and that matters here.** This repo is
public and the kit is the paid product, so committing the PDF would publish it
as a free download. The HTML it renders from is excluded for the same reason.

Three constraints drive the design, in order:

1. **It has to survive a home printer.** Consumer printers cannot reach the
   paper edge, so nothing bleeds. Everything sits inside a 0.6in margin.
2. **Ink is the buyer's money.** Large dark fills streak, print slowly and empty
   a cartridge, so the pages work through type, white space and hairlines. That
   also happens to look more expensive than decoration would.
3. **It has to read in grayscale.** Tier is carried by label, weight and
   position as well as color, so a black and white print loses nothing.

A page whose content overflows its sheet is silently truncated in the PDF and
invisible in the HTML. The month pages are close to full, so check after editing
content: open the built HTML and compare each `.sheet` scroll height against the
page box. `TWO_PAGE_MONTHS` in the builder exists because May measured over.

## Listing images

`build_listing_images.py` renders the Etsy photos from the real kit pages, so a
preview cannot show something the file does not contain.

Each page image is 2040 x 2640. That comes from sizing the Chrome window to the
sheet exactly, 816 x 1056 CSS pixels, and raising the device scale factor.
Setting a larger window instead renders the page at actual size in the corner of
a bigger canvas and pads the rest with white.

`00-hero.png` is composed at 4:3 rather than being a page render, because Etsy
crops the search-grid thumbnail to 4:3 and would otherwise slice the title off
the cover.

## Selling it

The Etsy shop is **GulfCoastHomeCare**, `etsy.com/shop/GulfCoastHomeCare`. The
name is shorter than the domain because Etsy caps shop names at 20 characters
with no spaces; "Gulf Coast" was the half worth keeping intact.

**The calendar is free and the kit is the product.** The three feeds are given
away from the site and are not sold anywhere. The kit lists on Etsy at $12.99.
The reasoning for that price, along with the title, description, all thirteen
tags, and the photo order, lives in
[product/etsy-listing.md](product/etsy-listing.md).

When there is a published listing, paste its URL into `SHOP_URL` at the bottom
of `docs/index.html`. That swaps the waitlist for a buy button, which is the
right trade: once the kit is purchasable the waitlist has done its job.

Use the **listing** URL rather than the shop URL, so buyers land on the product
instead of a shop front they have to search. And don't link the shop at all
until something is listed: an empty shop reads as abandoned.

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
  task content. A version bump alone does not do it, and a `SEQUENCE` bump is
  not needed for a design-only release.

To see what a released version contained: `git show v1.0.0 --stat`.

---

*General maintenance guidance, not a substitute for a licensed inspector,
contractor, or your insurance policy terms.*
