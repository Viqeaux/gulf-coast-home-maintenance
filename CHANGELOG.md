# Changelog

Versions use [semantic versioning](https://semver.org): `MAJOR.MINOR.PATCH`.

What each part means **for this project specifically**:

- **MAJOR:** something existing subscribers would notice as a break. Changing a
  task's `slug`, renaming or removing a feed file, or moving the site to a new
  address. These orphan calendars people already added, so they should be rare.
- **MINOR:** new content or new capability. A new task, how-to video links,
  a new page section, a new way to subscribe.
- **PATCH:** fixes and wording. Corrections, design tweaks, copy edits.

**When to cut one.** Don't wait to be asked, and don't tag every commit. Cut a
version when a coherent piece of work lands and the site is verified working:

- a visitor-facing feature is finished (a page, a form, a new way to subscribe)
- calendar content changes, which also needs a `SEQUENCE` bump
- infrastructure moves, like the domain switch
- a batch of fixes has accumulated

Not for a half-finished feature, and not for a commit that only touches build
scripts or notes. If a change is worth someone reloading the site for, it is
worth a version.

Newest first.

---

## [1.5.3], 2026-08-14

### Fixed

- **The price and the reassurance line sat left of centre on desktop.** Not the
  button, which was centred correctly all along. `.buy p` caps those paragraphs
  at 30rem and centres them with auto side margins, and the shorthand
  `margin: 0 0 1.35rem` added in 1.5.2 zeroed those margins, dropping both
  against the left edge of a wider card. Auto restored on the sides.
- **The button ignored its `min-width`.** An anchor is inline, and min-width
  does not apply to inline elements, so it rendered at 219px rather than the
  272px intended. Now `inline-block`.

### Changed

- The price is the brand's brick red rather than ink, so it reads as a price at
  a glance instead of as more type. It is the palette's existing red, not a
  discount red, and it lifts to the paler variant on the dark scheme.

## [1.5.2], 2026-08-14

The buy card reads as something for sale.

### Changed

- **The price moved to sit with the button.** It had been a small uppercase
  label above the heading, which is exactly how the section eyebrows are
  styled, so it read as a category label rather than a price, and it sat five
  lines from the thing you click. It is now 2.6rem serif immediately above the
  button, with "one time, no subscription" under it.
- **The button carries weight**, wide enough to hold its own against the price
  and with a solid drop edge, so it reads as a control rather than a link.
- **A reassurance line under the button**: instant download, two PDFs, prints
  on letter paper. That is the "what happens if I click" question answered
  where it gets asked.
- A rule separates the description from the price, so the card has a pitch half
  and a purchase half rather than one undifferentiated column.

### Notes

- The waitlist path still works: with `SHOP_URL` empty the price and the
  download promise hide themselves, since advertising a price above a form for
  something nobody can buy would be worse than the old layout.

## [1.5.1], 2026-08-14

Audit pass. Stale claims found and corrected, some of them live.

### Fixed

- **The site said the kit was eighteen pages.** It is twenty-seven, and the
  wrong number sat directly above the buy button. The blurb now also mentions
  the seven conditional sections and the fillable file, neither of which the
  site had caught up with.
- **The listing copy claimed the last page of the PDF points to the free
  calendars.** No such page exists; it died with the removed reportlab builder.
  Both places now point at gulfcoasthomemaintenance.com instead. The same copy
  suggested featuring a phone-calendars photo that was never rendered.
- **The kit footers printed wrong page numbers**, "Page 15" on a sheet that is
  eighteenth of twenty-seven. Footers now carry section names, which cannot go
  stale the way numbers already had, twice.
- The site still described the guides as pairing each task with a video, and
  promised how-to videos on the way. The guides are step-by-step text, and no
  videos exist yet. The guides page footer likewise discussed dead video links
  with zero videos on the page; that line now appears only once one does.
- "See the full edition" button, two product renames behind the buy section it
  scrolls to.

### Removed

- A stray fill-test PDF from `product/`, an unused import, an unused parameter.

### Notes

- The three feeds are byte-identical before and after, verified by hash.
  Subscribers see nothing.
- The corrected kit PDFs need re-uploading to the Etsy listing, and two lines
  of the live description need the same edit as the copy here.

## [1.5.0], 2026-08-14

The kit is on sale, and the site points at it.

### Changed

- **`SHOP_URL` is set**, so the buy slot now shows a button to the Etsy listing
  instead of the waitlist. The waitlist did its job: it collected interest while
  there was nothing to sell, and it steps aside the moment there is.
- **The price on the site is $12.99**, corrected from $7.99. It was written
  before the search data settled the question, and was still sitting in three
  places: the price line, the button label, and a comment.
- The price is now stated once, in the markup. The button no longer repeats it,
  so changing it later means editing one line rather than hunting for the rest.

### Notes

- The button uses the listing URL rather than the shop URL, so buyers land on
  the product rather than a shop front they have to search.
- Still unverified: Android link interception, which needs a real phone.

## [1.4.0], 2026-08-14

A fillable copy of the kit, so a buyer can type into it or print it blank.

### Added

- **`build_fillable.py`**, which produces a second file with 97 real form
  fields: the 34 Watch List blanks, every task checkbox, the first-month
  checklist, the conditional contents page, and the notes lines. Shipped
  alongside the print version rather than replacing it, so anyone printing at
  home still gets clean pages.

  Chrome's print-to-PDF emits no form fields, so they cannot come from the HTML.
  The generator marks each blank, headless Chrome reports where it actually
  landed, and reportlab stamps invisible fields there for pypdf to merge on.
  Measuring rather than calculating means the fields follow the layout when the
  design changes.

### Changed

- The listing now ships two files and says so. The description previously
  stated the file was not fillable, which is no longer true, and `fillable pdf`
  replaces `coastal homeowner` in the tags.

### Notes

- Verified by round trip rather than by eye: values written into fields, saved,
  reopened and read back. Confirmed on real hardware too.
- Desktop readers save form data reliably; some phone apps allow typing but not
  saving. The listing copy says so plainly rather than letting a buyer find out.

## [1.3.0], 2026-08-14

The kit becomes the paid product, and every task gains step by step detail.

### Added

- **Step by step detail for all 36 tasks** in `task_steps.py`, with what to
  have to hand, the order to do it in, and the mistake that costs money. Free on
  the guides page, and printed in the kit. Where a task is genuinely a
  hire-someone job it says so, and the steps become what to ask for.
- **Seven "if you have one" sections** in `kit_sections.py`, kit only: septic,
  well water, pool, generator, raised or pier foundations, storm shutters, and
  waterfront. Written for this coast rather than in general, so the septic page
  leads with the high water table and the pool page says not to drain it before
  a storm.
- **`build_printables.py`**, which lays the kit out in HTML and CSS and renders
  it through headless Chrome. Replaces a parallel reportlab builder from another
  session, which was solving the same problem with a different product strategy.
- **`build_listing_images.py`**, which renders the Etsy photos from the real kit
  pages so a preview cannot show something the file does not contain.
- **The Gulf Coast Year** is now a page in the kit. It was described in the
  listing copy while existing only on the website, which would have been
  misrepresenting the product.

### Changed

- **The calendar is free, the kit is paid.** The three feeds are given away and
  are not sold anywhere; the printable kit lists on Etsy at $12.99. A previous
  session had built the printable as the free download, so the buy slot, the
  section labels, the README and the listing copy all move with it.
- **Every em dash is gone**, 162 of them, from everything generated. Not a find
  and replace: a comma would have left splices wherever a dash joined two
  clauses, so short asides took commas, independent clauses took full stops, and
  definitions took colons.
- **British spellings and vocabulary corrected to American**, 31 in all. The
  product claims local expertise, and a reader in Gulfport being told to go
  under the house with a torch and clear the autumn leaves undercuts that.
- `SEQUENCE` goes to 1. Every event description now carries a link to its guide,
  so this is the first release that changes what subscribers see.

### Fixed

- The Watch List table and the "watch out" callout shared a CSS class name, so
  the table inherited a red left border it was never meant to have.
- A stray space before a period in the Watch List footnote, left by the em dash
  pass where a dash spanned two Python string literals.
- Listing images rendered at actual size in the corner of an oversized canvas.
  The Chrome window has to match the sheet exactly and resolution has to come
  from the device scale factor.

### Notes

- The kit and its HTML are gitignored. This repo is public, and committing the
  PDF would publish the paid product as a free download.
- `SHOP_URL` is still empty. The listing has to exist before the button can
  point anywhere.

## [1.2.0], 2026-08-13

The printable edition. The free download the shop will lead with.

### Added

- **`build_pdf.py`**, which builds the 20-page US Letter PDF: cover, how it
  works, the Gulf Coast year, your first month, the twelve months, the Big
  Ticket Watch List, how to date what you own, the phone calendars, and the
  licence. The twelve months come from the same `TASKS` list as the `.ics`
  feeds, so the print edition and the digital one cannot drift apart and say
  different things. The rest comes from `product_content.py`. The built PDF and
  its images are gitignored as build artifacts, a second to regenerate, and
  not served from `docs/`, so committing them would put binaries in the repo
  that nothing reads.
- **Listing images**, rendered from the real pages so a preview cannot show
  something the file does not contain. The first one is composed at 4:3, since
  Etsy crops the search thumbnail to 4:3 and would slice the title off a
  portrait page.
- **`product/etsy-listing.md`**. The listing copy, tags, the reasoning for
  listing it free, and what to do after it goes live.
- Each month task now carries a tick box and a line for the date it was done.
  That is what makes an undated calendar worth keeping rather than reprinting.

### Changed

- The buy slot on the landing page becomes **"Download it free on Etsy"** when
  `SHOP_URL` is set, rather than a buy button. The calendar is the free front
  door; the kit is what will be for sale.

### Fixed

- The seasons diagram on the landing page drew hurricane season running
  through **December**. Six columns, not seven. It now agrees with its own
  caption and with the 183-day figure above it.

### Notes

- The three `.ics` files are byte-identical to 1.1.0, so no `SEQUENCE` bump.
- `SHOP_URL` is still empty. The listing has to exist before the button can
  point anywhere, and an empty shop reads as abandoned.

## [1.1.0], 2026-08-13

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
  unavailable". The failure a status check sails straight past.
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

## [1.0.0], 2026-08-13

First public release, at `viqeaux.github.io/gulf-coast-home-maintenance`.

### Calendar feeds

- Three subscribe-able `.ics` feeds. Must Do, Should Do, Going Above, with
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
