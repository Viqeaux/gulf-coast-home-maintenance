# Changelog

Versions use [semantic versioning](https://semver.org): `MAJOR.MINOR.PATCH`.

What each part means **for this project specifically**:

- **MAJOR** — something existing subscribers would notice as a break. Changing a
  task's `slug`, renaming or removing a feed file, or moving the site to a new
  address. These orphan calendars people already added, so they should be rare.
- **MINOR** — new content or new capability. A new task, how-to video links,
  a new page section, a new way to subscribe.
- **PATCH** — fixes and wording. Corrections, design tweaks, copy edits.

**When to cut one.** Don't wait to be asked, and don't tag every commit. Cut a
version when a coherent piece of work lands and the site is verified working:

- a visitor-facing feature is finished (a page, a form, a new way to subscribe)
- calendar content changes — that one also needs a `SEQUENCE` bump
- infrastructure moves, like the domain switch
- a batch of fixes has accumulated

Not for a half-finished feature, and not for a commit that only touches build
scripts or notes. If a change is worth someone reloading the site for, it is
worth a version.

Newest first.

---

## [1.1.0] — 2026-08-13

Guides, a waitlist, and the move to a real domain.

### Added

- **How-to guides page** at `/guides/`, with a stable anchor for every one of
  the 36 tasks. Calendar events will link here rather than straight to YouTube,
  so a dead video is fixed in one place and the visitor lands on this site
  instead of being handed to Google. Curated links live in `GUIDES` in
  `build_calendars.py`; tasks without one get no link at all, so it can be
  filled in gradually.
- **`check_links.py`**, which finds curated videos that have gone dead. It asks
  YouTube's oEmbed endpoint rather than checking HTTP status, because a deleted
  or private video still serves a healthy page that happens to say "Video
  unavailable" — the failure a status check sails straight past.
- **Waitlist for the complete edition**, posting to MailerLite from a native
  form with no third-party code on the page. It sits in the buy slot, so
  setting `SHOP_URL` later replaces it with the buy button.

### Changed

- **Moved to <https://gulfcoasthomemaintenance.com>** with HTTPS enforced. The
  `viqeaux.github.io` address redirects, so existing subscriptions and anything
  already written down keep working untouched.
- The palette moved to `docs/theme.css`, shared by both pages, so the two
  cannot drift apart.

### Notes

- The three `.ics` files are byte-identical to 1.0.0. `GUIDES` is still empty,
  so no event carries a guide link yet, and no `SEQUENCE` bump was needed. The
  first curated video is the change that will require one.
- Still unverified on real hardware: the Apple `webcal://` handoff and Android
  link interception.

## [1.0.0] — 2026-08-13

First public release, at `viqeaux.github.io/gulf-coast-home-maintenance`.

### Calendar feeds

- Three subscribe-able `.ics` feeds — Must Do, Should Do, Going Above — with
  twelve all-day events each, recurring yearly with no end date so they match
  the undated print edition.
- Anchored to the 1st of each month, with two deliberate exceptions: **May 1**,
  which leaves room for the 30-day flood insurance waiting period before the
  June 1 season opens, and **November 30**, the season close.
- Every event carries the task, the reason it matters, and the disclaimer.
- Calendar names lead with the tier, because sidebars truncate and the tier is
  the only thing distinguishing the three feeds.
- Tier colours declared for clients that honour them. Google assigns its own
  per subscriber and ignores the file, which is why the name has to carry it.

### Landing page

- Field-guide design: a diagram of the Gulf Coast year showing the hurricane,
  heat, termite and freeze seasons against the May 1 insurance deadline; the
  Big Ticket Watch List as a lifespan chart; a live oak hero.
- Sections alternate between the paper and deep grounds.
- Four ways to subscribe per tier, covering Google and Android, Apple and
  Outlook desktop, direct download, and paste-a-URL clients.
- Detects when it is not on a public HTTPS origin and explains why subscribing
  cannot work there, instead of rendering a button that silently does nothing.
- Android visitors get the route that does not depend on the OS handing the
  link to a browser rather than to the Google Calendar app.

### Build

- All task content lives in one editable list in `build_calendars.py`, which
  handles RFC 5545 escaping and 75-octet folding.
- `optimize_images.py` resizes the photographic master into the served JPEGs.
- `.gitattributes` pins the `.ics` files against line-ending conversion, which
  would otherwise publish a malformed feed from a Windows checkout.

### Known and unverified

- The Apple `webcal://` handoff and the Android link-interception behaviour are
  reasoned about but have never been observed on real hardware.
- The Etsy link is not set. `SHOP_URL` in `docs/index.html` is empty, so the
  purchase slot reads "Coming soon".
