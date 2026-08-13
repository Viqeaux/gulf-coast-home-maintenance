# Changelog

Versions use [semantic versioning](https://semver.org): `MAJOR.MINOR.PATCH`.

What each part means **for this project specifically**:

- **MAJOR** — something existing subscribers would notice as a break. Changing a
  task's `slug`, renaming or removing a feed file, or moving the site to a new
  address. These orphan calendars people already added, so they should be rare.
- **MINOR** — new content or new capability. A new task, how-to video links,
  a new page section, a new way to subscribe.
- **PATCH** — fixes and wording. Corrections, design tweaks, copy edits.

Newest first.

---

## [1.0.0] — 2026-08-13

First public release. Live at
<https://viqeaux.github.io/gulf-coast-home-maintenance/>.

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
