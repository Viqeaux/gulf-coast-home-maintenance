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

## [1.9.0], 2026-08-15

Came out of a security and branding review of the whole site. Nothing here
changes what a subscriber sees: all three feeds are byte-identical to 1.8.0 and
`SEQUENCE` stays at 1.

### Added

- **The brand has a face.** `build_brand.py` now writes `docs/favicon.svg`,
  `docs/icon-180.png` and `docs/icon-512.png` from the house glyph it was
  already drawing for the shop icon, and both pages reference them. Every
  browser tab, bookmark and home screen shortcut was a blank document icon
  before this. The favicon runs the glyph at 0.74 rather than the shop icon's
  0.62: at 16 px the shop version's margin reads as a dark square with something
  indistinct in it.
- **Somewhere to go from the guides page.** It carried 4,642 words across all
  thirty-six tasks and exactly one link, the back arrow, while every calendar
  event deep links into it. Twelve times a year a subscriber landed on the most
  useful page on the site and found no next step. It now ends with the free
  calendars, one quiet line about the kit, and the signup, in that order.
- **A privacy page**, at `docs/privacy.html`. The site collects email addresses
  and hands them to a third party and had no privacy notice at all. It also says
  plainly that nothing here watches visitors, which is true and is worth saying.
- **A branded 404**, at `docs/404.html`, with absolute paths throughout: Pages
  serves it for a missing address at any depth, so relative links would resolve
  against the wrong directory for exactly the people who are already lost.
- **`robots.txt` and `sitemap.xml`**, and a canonical tag on every page. The
  canonicals matter most: the old `viqeaux.github.io` address still resolves,
  and without them it can compete with the real domain for the same content.
- **Structured data.** `Product` for both editions, `FAQPage` on the home page,
  and a `HowTo` for each of the thirty-six tasks on the guides page, generated
  from `STEPS` so it cannot drift from the page it describes. No invented
  ratings or reviews: those go in when Etsy has real ones.
- **The origin on the site.** "I built this for my own house first" now sits
  above the footer, in the same words as the Etsy About section. The site was
  asking $12.99 and $39 from an anonymous voice while the strongest thing in the
  project sat on another website.
- **Three points arguing for the agent edition.** The kit's card had a diagram, a
  sample month and a lifespan chart standing behind it; the $39 product had a
  paragraph. The objections are always the same three, so there are three
  answers: what you actually hand over, how much work it is, and whether you are
  allowed to.
- **A honeypot on the signup**, on both pages. Disabled before submit, so
  MailerLite never receives a field it has no definition for.

### Changed

- **A Content Security Policy on both pages**, plus a referrer policy. GitHub
  Pages cannot set response headers, so it travels in the document. The page
  loads no third-party code today and the point of the policy is to keep that
  true: a pasted widget or an analytics snippet now fails loudly instead of
  quietly reading the signup. `frame-ancestors` is ignored in a meta tag, so
  clickjacking protection is not available on this host at all, which is
  acceptable on a page with no authenticated actions and is written down rather
  than assumed.
- **The subscribe buttons are built as nodes**, not as an HTML string. Every
  address in them comes from `location.href`. It was not reachable on Pages,
  which 404s any path that is not a real file, but the point of the rewrite is
  that it no longer depends on the host to be true.
- **The Android note is a disclosure**, not an open card. How often Google
  Calendar actually intercepts the link is still unmeasured, so this was a
  paragraph of troubleshooting sitting on the buttons for every Android visitor,
  most of whom never needed it. Collapsed it costs one line and is still there
  at the moment someone taps a button and nothing happens.
- **`<main>` and a skip link** on the home page. The guides page already had a
  main landmark; the home page had no way past the header for anyone using a
  keyboard or a screen reader. `main` opens at the hero, because a skip link
  that lands past the `h1` has skipped the content.
- **Titles and descriptions target the search phrasing.** Nobody searches "Gulf
  Coast home maintenance"; they search "Florida home maintenance checklist", and
  every page that currently ranks for this subject is a Florida or state-named
  one. Both pages now name the states. The guides page was titled "How-to
  guides", which targeted nothing, on the page carrying all thirty-six jobs.
  Titles are 54 and 60 characters and descriptions 147 and 142, so nothing
  important falls past where Google truncates. The pages still say Gulf Coast
  throughout: this is how they get found, not what they are called.
- The home page description no longer opens on salt air. One task of thirty-six
  is about salt, while fourteen are heat and humidity and five are hurricane
  season, so leading on salt described a coastal strip rather than the Gulf
  South. Less accurate, and a smaller audience.

### Fixed

- **"What to have to hand" is British.** It was live on the guides page and in
  both Etsy descriptions, while the home page already said "on hand", so the
  site contradicted itself. For a product whose whole claim is knowing this
  coast, that is exactly the tell that undercuts it. Both listings need the
  corrected description pasted in by hand.
- `kit_sections.py` read "Check the skirting and any flood vents are intact",
  which wants a "that" in American usage. This one is inside the kit, so the
  PDFs need rebuilding and re-uploading.

Minor rather than patch: new pages, new capability on the guides page, and a new
section on the home page. No task content changed.

---

## [1.8.0], 2026-08-15

### Added

- **Pinterest, as a channel rather than an afterthought.** `build_pins.py`
  renders six pins at 1000 x 1500 from the real kit pages, the same discipline
  the Etsy photos follow, and [product/pinterest.md](product/pinterest.md)
  carries the boards, the setup order and the copy for every pin. The market
  data has said since the beginning that volume is the binding constraint and
  that discovery cannot come from Etsy search, and this is the first thing built
  against that. Each pin targets one search intent, because a person looking up
  hurricane prep and an agent looking for a closing gift will never type the
  other's words.
- **Open Graph tags on the landing page.** The site had none, so every share of
  it resolved to a grey card and Pinterest had to guess at an image. Absolute
  URLs, since scrapers resolve them against their own host.
- **The Pinterest domain claim.** A `p:domain_verify` tag in the head. Without
  it, pins pointing at the site carry no shop attribution, including the ones
  other people reshare.

### Changed

- The README's file map had drifted: `build_agent_edition.py`,
  `build_agent_listing.py` and `build_brand.py` all shipped without being listed
  in it.

Minor rather than patch: a new capability, and a channel that did not exist
before. No task content changed, so `SEQUENCE` stays at 1 and all three feeds
are byte-identical to 1.7.0.

---

## [1.7.0], 2026-08-15

### Added

- **The realtor edition, and a section on the site that sells it.** A second
  paid product at $39: the full 27 page kit branded with an agent's name,
  brokerage, phone and license number on every page, plus a four page
  leave-behind for the closing table. `realtor closing gift` draws 9,400
  searches a month against 31.3k listings, a ratio of 1:3.3, where nothing else
  in the market data beats 1:21. Minor rather than patch: the site gained a
  section and a second buy path.
- The section sits directly under the kit rather than at the end. The agent who
  needs it is most likely reading the kit card and running into a license
  written for one household, so that card now points at it.
- **`build_agent_edition.py`**, producing four files, each document in a print
  and a fillable version. Run with no arguments, every detail comes out as a
  ruled blank that `build_fillable.py` turns into a form field, so an agent
  types their details once and saves, with no work per order. Pass `--logo` and
  it is baked in at build time, which is the only part that costs anything per
  sale. AcroForm has no image field an ordinary reader will populate, so a logo
  cannot be self-serve however much one would like it to be.
- **Why a four page leave-behind exists at all.** Handing a client 27 pages
  twenty times is 540 sheets, and nobody does that twice. The license was never
  the thing worth paying for, because it cannot be enforced on a PDF. What the
  $12.99 kit genuinely cannot do is fit the job.
- **A `BRAND` block in `build_printables.py`**, disabled by default. With it off
  the kit builds byte-identical to `HEAD`, verified by an A/B against a clean
  checkout.
- **`build_agent_listing.py`** and an `--agent` mode on `build_video.py`, for
  nine listing photos and a 14 second video. Two photos exist only for this
  listing: a footer close-up at twice actual size, the only way to prove the
  branding runs past the cover, and a blank cover beside a filled one, which
  answers the assumption that this is made to order and will be waited on.

### Fixed

- **The buy slot hid every price on the page, not only its own.** With one
  product that was invisible. With two, an empty `AGENT_URL` would have blanked
  the kit's price and download promise as well. Now scoped to the card that owns
  the slot.

### Changed

- The kit's listing copy no longer says an agent edition is coming, in both the
  license paragraph and the client-gifting question. It is here.

## [1.6.0], 2026-08-14

### Added

- **A signup for future releases, at the end of the free calendars.** The site
  has had no way to hear about anything since the kit listed. The MailerLite
  form was still in the markup but inside `#buy-slot`, and the script wipes that
  slot to write the buy button in whenever `SHOP_URL` is set, so the form only
  ever rendered in the one state the site will not be in again. Minor rather
  than patch: this is a capability the live site did not have.
- It is no longer a waitlist for the kit. The heading is "Hear about the next
  one" and the note promises only when there is something new, which is not
  often. The old copy promised one email at launch, the wrong promise for a list
  that outlives the launch.

### Changed

- The ask sits after the three free calendars rather than inside the buy card,
  which is the goodwill moment: someone who has just been handed three free
  things, not someone deciding whether to spend $12.99.
- The block is styled to not read as a fourth tier card. No colored left bar, an
  uncolored heading, no shadow. It keeps the `--paper` ground on purpose: the
  field is defined by its `--rule` border, and on `--paper-2` that border and
  the fill both land within 1.2 of the block behind them, which leaves the input
  invisible until it takes focus.
- `#buy-slot` is empty in the markup now, and the no-listing branch writes "Not
  listed yet" into it rather than falling back to a waitlist that no longer
  exists there.

### Note for the shop owner

- The MailerLite group is still named "Complete edition waitlist" and now
  collects general signups. Renaming it is a change in the MailerLite account,
  not in this repo. The form endpoint is a form ID and does not move when the
  group is renamed, so no code change follows.

## [1.5.4], 2026-08-14

### Changed

- **The free calendars now say so three times over.** The $12.99 kit sits
  directly above them, and a reader scanning down carries that price with them
  and assumes the feeds are priced too. "Free" was in the section only twice
  before, as a small section label and as one word mid-sentence in the deck,
  and both are easy to miss at scanning speed. There is now a solid pill in the
  heading, a deck that opens on it and names the wrong idea outright ("not a
  sample of the kit above and not a trial"), and a badge on each of the three
  tier cards beside the tier name. Six mentions, up from two. The deck also
  swaps "no signup" alone for "no signup, no card", since the card is the thing
  a suspicious reader actually wants ruled out.
- The pill and the badges take their color from `--accent` against `--paper`,
  the pair the topbar link already uses, so they invert with the palette
  instead of needing a dark-scheme variant. 7.4:1 on the light ground and 6.8:1
  on the dark one.

## [1.5.3], 2026-08-14

### Fixed

- **The price and the reassurance line sat left of center on desktop.** Not the
  button, which was centered correctly all along. `.buy p` caps those paragraphs
  at 30rem and centers them with auto side margins, and the shorthand
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
  have on hand, the order to do it in, and the mistake that costs money. Free on
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
  license. The twelve months come from the same `TASKS` list as the `.ics`
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
- Tier colors declared for clients that honor them. Google assigns its own
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

- The Apple `webcal://` handoff and the Android link-interception behavior are
  reasoned about but have never been observed on real hardware.
- The Etsy link is not set. `SHOP_URL` in `docs/index.html` is empty, so the
  purchase slot reads "Coming soon".
