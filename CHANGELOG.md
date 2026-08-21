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

## [1.20.0], 2026-08-21

**`SEQUENCE` goes to 2.** Every subscriber's existing events move, which is the
first time that has happened since the feeds launched. Read the note at the
bottom before touching task dates again.

### Changed

- **Task dates spread across the month.** Must Do on the 1st, Should Do on the
  10th, Going Above on the 20th. Everything used to sit on the 1st, so thirteen
  days a year carried anything at all and a subscriber opening a week view on
  any of the other three hundred and fifty-two saw an empty calendar with no way
  to tell that from a broken feed. Chad reached exactly that conclusion about
  his own product on 2026-08-21. Spread, something lands in three weeks of four.
- November 30 stays put. It is the close of hurricane season and the date is the
  whole point. May's Must Do sits on the 1st with the rest, which still clears
  the 30-day flood policy window ahead of June 1.
- **The guide link is labelled "Details:" rather than "How to:".** Parked in
  1.10.0 for the next `SEQUENCE` bump, because the page stopped carrying steps
  when they moved into the kit and a label promising them was overselling what
  it leads to. This is that bump, so it travels here rather than earning its own.

### Added

- **A fourth feed, Monthly Rounds**, at `gulf-coast-monthly-rounds.ics`. Seven
  rounds a month, one per area: HVAC and air, plumbing, safety, appliances, the
  exterior walk, interior upkeep, and the generator and storm kit. Every item
  travels in the event description.
- **Deliberately a fourth feed rather than a fourth tier.** The three tiers are
  levels of effort on one seasonal list. This is a different kind of thing, the
  short routine that repeats regardless of season, and subscribing to it is a
  separate decision: seven events a month is welcome to somebody who wants a
  routine and noise to somebody who came for twelve seasonal reminders.
- **Seven events a month, not twenty-four.** The list ran to twenty-four jobs,
  which as separate reminders is 288 events a year against the seasonal
  calendar's 36. That is the volume at which people mute a calendar rather than
  read it. Grouped by area it is 84, it lands in most weeks, and nothing is lost
  because each event carries its whole list.
- Rounds fall on the 3rd, 6th, 8th, 13th, 16th, 23rd and 26th, which interleaves
  them with the seasonal tasks rather than stacking on them, and keeps every
  round inside a February.

### Notes

- **Overlaps with the seasonal calendars are deliberate.** Detectors, GFCIs, the
  condensate line, gutters, the roof and the generator appear in both. The
  monthly version is the quick pass and the seasonal one is the thorough
  version, and the wording differs to say so: the monthly safety round is press
  and hold the test button, while January is fresh batteries and replacing any
  detector over ten years old.
- **UIDs are unchanged**, verified against 1.19.1. With the same UID and a
  raised `SEQUENCE`, a client moves the event it already holds instead of adding
  a second copy, which is the whole reason this is safe to do at all.
- The printed kit is untouched. `build_printables.py` filters `TASKS` by month
  and never reads the day, so spreading the dates changed nothing about the 27
  pages, and the rounds live in their own constant rather than in `TASKS`.
- All four feeds verified: CRLF throughout with no bare LF, no line over the
  75 octet limit, `SEQUENCE:2` everywhere, seven `FREQ=MONTHLY` events in the
  new feed and none of them carrying a guide link, since the contents page has
  no anchors for them.

## [1.19.1], 2026-08-21

### Fixed

- **The setup instructions told a lie about phones, and it cost the owner an
  evening.** The Google panel said adding the feed from a browser makes it
  "appear on every device on that account". It does not. Google keeps a
  per-device sync list for the mobile app, and a newly subscribed calendar
  starts switched off, so it lands on desktop and never reaches the phone. Chad
  followed his own instructions on 2026-08-21 and concluded the feed was broken.
  It was not: the feed returns 200 as `text/calendar`, parses clean, CRLF
  throughout, twelve events, and the certificate is good until November.
- The panel now says adding it puts the calendar on the account rather than on
  the phone, makes switching it on in the app a real step rather than an aside,
  and names the case nothing in the app can fix: when the calendar is missing
  from the app's own Settings list, the only control is
  `calendar.google.com/calendar/syncselect`, which the app does not link to.

### Noted, not changed

- **Thirteen days a year carry an event.** Every task sits on the 1st, plus
  November 30, so a subscriber opening a week view on any of the other three
  hundred and fifty-two days sees an empty calendar and cannot tell that from a
  broken one. That is the same false conclusion the owner reached, and it is the
  free product's real weakness rather than a display detail. Spreading each
  month's three tasks through the month would fix it, and it rewrites dates
  subscribers already hold, so it needs a `SEQUENCE` bump and belongs in its own
  release. Recorded in [HANDOFF.md](HANDOFF.md).

Feeds are byte-identical to 1.19.0 and `SEQUENCE` stays at 1.

## [1.19.0], 2026-08-21

Google Analytics, and the reversal of the zero-tracking position.

### Added

- **Google Analytics 4 on the three pages that matter**: the home page, the
  calendar contents page and the free calculator. Property `G-KB3D46WDYK`.
  Chad's call, 2026-08-21, made deliberately rather than drifted into. The shop
  has been running on nothing but Etsy's own stats since it opened, which meant
  there was no way to tell whether anybody was arriving at the site at all,
  which is the one number the whole business currently turns on.
- **`docs/analytics.js`**, which exists so the Measurement ID lives in exactly
  one place. Three pages load it. A constant pasted into three files is a
  constant that drifts, and this project has already paid for that lesson once
  with the four version markers. An empty `GA_ID` disables the whole thing:
  nothing is requested and no cookie is set.

### Changed

- **The Content Security Policy names Google and nothing else.**
  `googletagmanager.com` in `script-src` is now the only third party permitted
  to run code, and the `google-analytics` hosts in `connect-src` and `img-src`
  are the only destinations a measurement may be sent to. The property that
  made the old policy worth having is intact: a tracker that arrives by paste
  rather than by decision still fails loudly instead of silently working.
- **`docs/privacy.html` says what is now true**, in the lede, the opening line,
  the meta description and the date. The page had promised that if anything
  ever watched visitors it would say so before that went live, so the wording
  and the tag ship in the same release rather than the wording following after.
- The zero-tracking rule in [HANDOFF.md](HANDOFF.md) is replaced by the
  decision that superseded it, so a future session does not read the old rule
  and quietly argue the position back.

### Deliberately not done

- **`404.html` and `privacy.html` are not measured.** Both run no script on
  purpose, `404.html` at `script-src 'none'`, and neither sees enough traffic to
  justify widening its policy.
- **The calculator sends the visit, never the answer.** The page tells visitors
  that nothing they type leaves their machine, and that remains true: no build
  year, system name or computed figure is attached to an event, however useful
  it would look in a report. The constraint is written into the header of
  `build_calculator.py` so it is hit before it is broken.
- **No custom events yet.** Enhanced measurement covers outbound clicks, which
  is the Etsy click. Feed subscribes and signup submits are worth instrumenting
  once data is confirmed arriving, on the principle that you verify a pipe
  before sending structured data down it.

### Notes

- The three `.ics` files are byte-identical to 1.18.0, so no subscriber sees
  anything and `SEQUENCE` stays at 1.
- Verified in a browser before release: with the ID empty, no `gtag`, no
  `dataLayer`, no cookie and no request; with an ID set, the tag loads, the
  `_ga` cookies appear and there are zero CSP violations. Both subdirectory
  pages resolve `../analytics.js` correctly, the two unmeasured pages load no
  analytics at all, and the calculator still computes.

## [1.18.0], 2026-08-16

### Added

- **The storm season workbook**, built but not listed. The companion to the
  storm binder and the fifth product: ten tabs of the things paper cannot do.
  Wind and flood deductibles resolved to dollars against your savings, a 500 row
  home inventory subtotaled by room and against the contents limit, the supply
  calculator with a live "still need" column, a damage log subtotaled by which
  policy pays, a claim call log, and four contractors scored against ten checks
  and eight red flags. Built by `build_workbook.py` from `workbook_data.py` and
  verified by `qa_workbook.py`, which compiles the workbook and reads the
  answers back rather than checking them by eye. Fifteen cases, all passing.
- **`Receipts & Loss of Use`, which is a gap in the binder rather than a
  duplicate of it.** The binder's claim steps tell the buyer to keep every
  receipt and correctly say loss of use is a separate limit, and there is
  nowhere in the binder to log either. This tab keeps mitigation spending in its
  own subtotal and says on the page why: mitigation is reimbursable under the
  duty to prevent further damage and is not drawn from the loss of use limit.
  Buyers conflate the two constantly. Worth adding to a v2 of the PDF as well.
- The rooms and the supply rules are imported from `binder_pages.py` and
  `check_against_binder()` fails the build if they drift, so the two products
  cannot end up calling the same room different things.

### Fixed

- **Two corrupted strings in `binder_pages.py`**, and therefore in the live
  $16.99 binder PDF. `insurer's` and `board's` had been mangled into control
  characters by an apostrophe pass at some point before 1.11.0, on the damage
  log page and the contractor vetting page. Reworded rather than re-apostrophed,
  because the file carries no apostrophes anywhere else in 682 lines of prose.
  **The binder PDFs need rebuilding and re-uploading to the listing.**

### Notes

- Nothing about the workbook is on the site or on Etsy. Deliberate: the shop's
  constraint is traffic rather than products, and this is a fifth thing to sell
  to the same room. It earns its place by making the binder worth more rather
  than by competing with it.
- Two things in the build spec were changed on purpose. `Unknown — described
  below` lost its em dash, because those dropdown values are also `SUMIF`
  criteria and a punctuation fix later would silently break a subtotal. And the
  spec's count of un-entered sub-limits,
  `COUNTIF(range,"Limit not entered")+COUNTIF(range,"LIMIT NOT ENTERED*")`,
  double-counts: `COUNTIF` is case-insensitive, so the wildcard matches the
  exact string too. It counts entered limits and subtracts instead.
- The feeds are byte-identical to 1.17.0 and `SEQUENCE` stays at 1. No task
  content changed, so subscribers have nothing to pick up.

---

## [1.17.0], 2026-08-16

### Added

- **The free calculator**, at `/calculator/`. Type the year the house was built
  and it answers whether four of the most expensive things you own are already
  past due. It is the only page on the site that gives something before it asks
  for anything, which is what makes it the one worth linking or pinning, and the
  shop's constraint is traffic rather than conversion. The arithmetic runs in
  the visitor's browser, so nothing typed into it leaves their machine and the
  page adds no origin to the policy.
- Placed as a line in the hero under the two buttons rather than as a third
  button, because three buttons turn a clear choice into a menu. Also in both
  footers, the guides page tailpiece, and `sitemap.xml`.
- **The reserve planner**, built but not listed. One spreadsheet, nine tabs, 49
  systems, a 30 year forecast and a funding dashboard. Its `Quick Check` tab is
  the paid version of the calculator: the same estimate from the same build
  year, across twelve systems, with the region factor applied. Built by
  `build_planner.py` from `planner_data.py` and verified by `qa_planner.py`,
  which compiles the workbook and reads the answers back rather than checking
  them by eye. Eleven cases, all passing.

### Changed

- Four became the number of systems on the free page. It was briefly twelve,
  which was too much to be a teaser and too little to be a product.

### Notes

- `What Breaks Next` existed for a few hours as a standalone `.html` download
  and is now the workbook's `Quick Check` tab. A raw `.html` attachment cannot
  be relied on to open on a phone, and no static format fixes that: PDFs and
  images cannot compute, and a zipped `.html` is worse rather than better. The
  only thing that reliably calculates on a phone is a spreadsheet.
- The feeds are byte-identical to 1.16.0. `SEQUENCE` stays at 1: no task
  content changed, so subscribers have nothing to pick up.

---

## [1.16.0], 2026-08-15

### Added

- **Page previews in all three product sections.** Three per product, with
  captions, above each buy card. Until now nobody browsing the site had seen a
  page of anything they were being asked to pay for, which is a lot of trust to
  ask of someone buying a printable.
- `build_site_images.py`, renamed from `build_site_covers.py` because it now
  makes the nine previews as well as the three covers. Committed outputs, for
  the same reason the covers already were: the sources live under gitignored
  `product/` and a fresh clone could not rebuild them.

### How this stays inside the 1.10.0 decision

`README.md` puts the step-by-step, the Watch List, How To Find Out and Your
First Month on the paid side, and the listing builders render exactly those
pages. The previews get around that by **cropping rather than shrinking**, and
the crop is the whole protection: what falls below the cut is not in the image
file, at any zoom.

- **Shrinking was tried first and abandoned.** At 420px wide the body text of a
  month page is still perfectly legible. Picking a smaller number until it stops
  being legible is guesswork dressed up as a rule, and it fails the moment
  someone upscales it or a better model reads it.
- **On the month pages the crop lands on a line that already exists.** The task,
  its one-line instruction and the "why" sit above it, and all three are free
  and already public inside the `.ics` feeds. The numbered steps start below it.
  Nothing paid is in the file.
- The Watch List preview shows three of seventeen rows. The home page already
  charts eight of them, deliberately, so this is inside an existing teaser
  rather than a new disclosure.
- The binder previews are its blank forms, an inventory sheet and a claim log,
  where the structure is the useful part and there is no prose to give away.
- Each preview was opened and read back before shipping, rather than trusting
  the arithmetic.

### Fixed

- **Two links had never been styled and rendered browser-default blue**, the
  agent cross-sell inside the kit's buy card and the privacy link under the
  signup. Both sit on paper and now take `--accent`, 7.29 against the card.
  Pre-existing, unrelated to the previews, found while checking this work.
- Preview captions bottom-align across each strip. The three crops are not the
  same shape, because the pages are not, and forcing a common aspect ratio would
  crop sideways into the page margins.

## [1.15.2], 2026-08-15

### Changed

- **The hero's free CTA is no longer gold.** 1.15.1 made gold the checkout
  color across all six Etsy buttons, which left the loudest button on the page
  wearing "this costs money" to offer something free. It takes a light fill,
  `--on-deep` with `--deep` text, measuring 12.48 on the light scheme and 13.38
  on the dark one against both its own label and the hero ground behind it.
- Teal was the obvious alternative, since that is what the FREE badges use lower
  down, and it does not work here: `--accent` against `--deep` is about 1.4:1,
  so a teal fill sinks into the hero's own ground. Written down because it looks
  like the right answer until it is measured.

The two colors now each mean one thing: gold goes to a checkout, light is the
free action. The outlined secondary button is untouched.

## [1.15.1], 2026-08-15

### Changed

- **Every button that ends at an Etsy checkout is gold.** All six of them, the
  three in the shop grid and the three on the product cards, so "this one costs
  money" is a color the reader learns once. New `.btn--buy`, reusing the exact
  pair the hero's primary button already used rather than introducing a yellow:
  `--sand` with `--deep` text, because white on sand lands near 3:1 and fails.
  Measures 5.35 on the light scheme and 8.06 on the dark one.
- The big buy buttons carry a 2px shadow that was mixed from `--accent`. It now
  mixes from `--sand`, or a teal lip sat under a gold button. The no-`color-mix`
  fallback moved with it.
- **The agent edition reads $39.00 rather than $39**, on the shop card and on
  its buy card, so all three prices carry cents. The structured data already
  said 39.00 and is unchanged.

## [1.15.0], 2026-08-15

### Added

- **A shop grid under the hero.** Three product cards with a cover image, a
  price, a Buy on Etsy button and a link down to the section that makes the
  case. Until now the only way to learn the shop had three products was to
  scroll through three long sections, and a reader who left early never knew
  two of them existed.
- `build_site_covers.py`, which makes `docs/img/cover-*.jpg` from the cover
  render each listing builder already produces. Those covers are committed,
  unusually for build output, because their sources live under gitignored
  `product/` and a fresh clone would otherwise have a grid with no images.

### Why a grid and not a carousel

Asked for as a carousel, built as a grid deliberately. A carousel shows one
product and puts the other two behind an interaction most people never make,
which is the opposite of the problem being solved here. An auto-rotating one is
also a WCAG 2.2.2 failure. The shops this is modelled on, Etsy included, are
grids. The grid needs no JavaScript, stacks to one column on a phone, and shows
all three products in a single screen.

### Why only cover images

The covers are title pages: the product name, its one-line promise, and nothing
a buyer is paying for. The listing builders also render the Watch List, How To
Find Out and Your First Month, and those are on the paid side of the line in
`README.md` settled in 1.10.0. None of them may come to the site without
reversing that decision on purpose.

### Fixed while building it

- **`.band p` was repainting the card prices.** It is a class plus an element,
  so it outranks a lone class, and the prices came out in the band's muted tone
  instead of the brand red. The card rules are scoped through `.pcard` now.
- **The free-calendars link in the grid rendered as browser-default blue.**
  Nothing had ever styled a bare link on the deep ground before. It takes
  `--sand`, which every other link on a band already uses.

### Kept

The three product sections stay where they are. The grid is an index, not a
replacement: the arguments those sections carry, the $8,000 deductible, the 540
sheets, the Watch List chart, are the case Etsy's own listings cannot make, and
a card cannot hold them. The grid is unnumbered because the 01 to 09 sequence is
an argument that builds and a shelf of products is not a step in it. On the band,
so the page still alternates strictly and the grid reads as continuous with the
hero above it.

## [1.14.0], 2026-08-15

Came out of an external design critique. Roughly half of it described a site
three versions old, and two of its recommendations would have broken documented
decisions, so what follows is the part that survived checking. What was declined
and why is recorded in [HANDOFF.md](HANDOFF.md) so it is not re-litigated.

### Fixed

- **Buying anything required JavaScript, and now does not.** The three buy
  buttons were built by a script from `SHOP_URL`, `BINDER_URL` and `AGENT_URL`
  and appended into empty slots, so a visitor with scripting blocked, or one of
  the small number whose script request simply fails, saw a price with nothing
  to click. The anchors now ship in the markup. The critique reported this as
  "no visible purchase button", which was wrong about the live page and right
  about the underlying build.
- `wireBuy` and the three URL constants are gone with it. Unlisting a product is
  now one instruction rather than two mechanisms: delete its anchor, its
  `.buy-price` line and its `Product` block in the structured data, which is
  what the structured-data comment already told you to do.

### Added

- **A third link in the sticky bar, "The kit, $12.99".** The bar is the only
  navigation that follows the reader, and it carried the free feeds and the
  seasonal binder but no path to the flagship. The price is in the label because
  "The kit" alone does not tell a first-time reader whether clicking it costs
  anything. It hides below 46rem, measured as the width where three buttons and
  the wordmark stop sharing a line.

### Changed

- **The per-app setup steps fold into `<details>`.** Three quarters of that
  section was instructions for an app the reader has not chosen yet, sitting
  between the products and the About section that closes the page. Visible text
  drops from 1,834 characters to 973. Native `<details>`, not a scripted
  accordion, so it still opens with JavaScript blocked and find-in-page still
  reaches inside it.
- The Android interception note goes inside the Google panel. It apologized for
  a failure before anyone had clicked anything; folded, it reaches the person
  who has that problem and nobody else.
- **The agent card's blurb stops repeating the three cards above it.** It restated
  540 sheets, the typing and the license close enough to verbatim that the two
  read as a stutter. It now says what is in the box, which nothing else on the
  page did: four PDFs, print and fillable of both documents, and that the
  branding persists once saved.

### Checked and found already correct

Recorded because the critique reported each as a defect and a future reader will
otherwise re-check them.

- The season diagram already carries `role="img"` and a descriptive
  `aria-label`, so a screen reader reads the summary rather than "JANFEBMAR".
- The signup honeypot is already `aria-hidden` on the wrapper and `tabindex="-1"`
  on the input.
- The hero image already has an empty `alt` inside an `aria-hidden` container.
- The stat strip has a 5px gap between number and label at every breakpoint, so
  nothing collides.
- The kit is 27 pages in the builder, in the built PDF, on the site and in the
  Etsy listing copy. All four agree.
- Bar and body contrast pass AA throughout. The kit link measures 6.46 on the
  paper ground, identical to the link beside it.

## [1.13.0], 2026-08-15

### Added

- **A hurricane season countdown in the hero**, above the buttons, linking to
  the binder. It states whichever of three facts is next rather than printing
  all of them: how long until the season starts, until the September 10 peak,
  or until it ends on November 30. Today it reads "Peak of hurricane season is
  in 26 days."
- **Days, not a ticking clock.** Seconds counting down to a six month season is
  theatre, and days is both the unit a reader can act on and the unit the whole
  product is organized around. It states a fact and links to the thing that
  answers it rather than manufacturing alarm, for the same reason the structured
  data carries no invented rating.
- Hidden in the markup until the script has a real number. A countdown showing a
  blank or a stale figure is worse than no countdown, and anyone without
  scripting still gets the season dates from the stat strip directly below it.

### Notes on the implementation

- **Compared as local calendar days, never as raw timestamps.** Subtracting two
  `Date` objects and dividing by 86400000 is off by an hour across a daylight
  saving change, which is enough to round a day the wrong way, and it would show
  a reader in Galveston at 11pm a different number from one in Pensacola ten
  minutes later. Both ends normalize to UTC midnight of their local date.
- **Verified against all 365 days of a year**, by extracting the shipped
  function and running it against stubbed dates rather than checking today and
  assuming. All seven branches read correctly, including the two nobody would
  see for months: November 30 says "Today is the last day of hurricane season",
  and December rolls to the following June rather than reporting a negative.
  Singular and plural are right at the boundaries, so May 31 reads "1 day".

## [1.12.1], 2026-08-15

### Changed

- The sticky bar's binder button reads "Hurricane checklist" rather than
  "Hurricane prep". Chad's wording, and it matches the term the listing title
  leads on. Sentence case to match "Free calendars" sitting next to it. It grows
  from 120 to 145 px, still one line and still clear of the wordmark at 375 px.

## [1.12.0], 2026-08-15

### Added

- **A second button in the sticky bar, for the binder.** Filled in the brand's
  red rather than outlined in the teal the rest of the furniture uses, so it
  reads as the one urgent thing on the page. It scrolls to the binder section
  rather than leaving the site, which puts the reader at the card with the price
  and the button on it. The binder is the only product with a deadline, and the
  sticky bar is the only element that follows the reader down the page.
- A slow pulse on it, a ring fading outward every 2.4 seconds. **Deliberately a
  pulse and not a blink.** A hard on and off at a noticeable rate is a WCAG
  2.2.2 problem, it never hides the label this way, and blinking is the one
  animation pattern people reliably read as an advert, which is the opposite of
  what this brand sells on. The existing `prefers-reduced-motion` block stops it,
  verified by applying the same declaration and confirming the animation count
  drops to zero. The solid red carries the emphasis on its own when it does.

### Changed

- **The small-screen rule no longer hides both buttons.** `.topbar a.cta` was
  set to `display: none` under 30rem, written when there was one button and
  dropping it was free. The seasonal button now stays: a phone in August is
  exactly the case it exists for.
- To make room, the wordmark gives up its text below 30rem and keeps the house
  glyph. The name is already in the tab title and the hero, and the button is
  worth more than its second reading. Measured at 375px: the button is 120 by 32
  and sits inside the bar with no horizontal overflow.

## [1.11.1], 2026-08-15

### Changed

- **The agent section moves onto the band, restoring the page's alternation.**
  Adding the binder in 1.11.0 put three paper sections in a row, since the
  binder, the agents and the free calendars all sat on the paper ground. The
  page alternates strictly again: paper, deep, paper, deep, paper, deep, paper,
  deep, paper. It uses the same `--band-bg` as every other band, not a variant,
  so there is still exactly one dark ground on the site.
- Every hairline between sections is gone as a result, and correctly so. That
  rule only fires between two sections sharing a ground, and no two paper
  sections are adjacent any more, which is what its own comment asks for.

### Fixed

- **The points grid was unreadable on a band, which nothing had exposed until
  now.** `.point .pn`, the large number on each card, takes `--accent`, and on
  the light scheme that is a dark teal sitting near 2:1 against the deep ground.
  The grid had only ever appeared on paper sections before the agent section
  moved, so this was latent rather than new. It now takes `--sand` on a band,
  the token already designated for deep grounds and already used there by
  `.sec-no`. Measures 5.35 on the light scheme.

## [1.11.0], 2026-08-15

### Added

- **The storm season binder is on the site**, as section 05 with its own buy
  card at $16.99. Chad published the Etsy listing the same day, which answered
  the open question from 1.10.0 about whether the site should link to a third
  product. It earns a version by the rule in this file: the binder now has a
  live buy path, which is what was being waited for, rather than merely
  compiling.
- A third `Product` block in the structured data, with the binder's price and
  listing URL. The comment above that graph now names all three URL constants,
  since the rule about deleting a block when its URL is emptied applies to each.
- `BINDER_URL` and a third `wireBuy` call. No new machinery: `wireBuy` was made
  per-card in 1.10.0 and takes a third slot without changes.

### Changed

- **The binder sits above the agent edition, not below it.** It sells to the
  same person as the kit, a homeowner, and it is the only product on the page
  with a deadline: search for every term it lives on collapses in winter and
  peaks around September 10. An agent arriving at the kit's license wall has a
  direct link out of that card, so adjacency was doing less work for that
  section than it appeared. A homeowner had no such link and would have had to
  scroll past a realtor-only pitch. Worth revisiting out of season, when the
  binder is the one product nobody is shopping for.
- Sections after it renumber: agents 05 to 06, free 06 to 07, how-to 07 to 08,
  who 08 to 09.
- Plain section rather than a band, so the kit keeps the deep ground and stays
  the loudest paid thing on the page.
- The card's copy was cut to the length the other two cards use. First draft ran
  44 to 47 words per point against the agent card's 33 to 35, and 69 words of
  blurb against 52 and 57. Now 35 to 38 and 54.

## [1.10.0], 2026-08-15

**The step-by-step detail is kit only now.** Chad's call, and it corrects a
split that had been the wrong way round since the guides page shipped.

### Changed

- **`docs/guides/` no longer prints `STEPS`.** The tools to have on hand, the
  numbered steps and the caution were free to anyone with the URL, which is the
  material the $12.99 kit is sold on. All of it comes off the site. The page
  drops from 101 KB to 40 KB, and all 186 steps, 8 tool lists and 11 cautions
  were checked against every published file afterwards to confirm none of them
  survive anywhere, feeds included.
- **The page is now the schedule rather than the method.** It keeps the task,
  the one-line instruction and the "why", which the `.ics` feeds publish to
  every subscriber anyway, so withholding them here would have hidden nothing
  and left thirty-six live calendar events pointing at empty anchors. Retitled
  from "How to do each of these" to "What is on the calendar", because a title
  promising how-to would be advertising something the page no longer carries.
- **The structured data is an `ItemList`, not thirty-six `HowTo` blocks.** A
  `HowTo` carries its steps in the markup, so leaving that in would have
  republished the whole thing in a tidier form than the page ever had.
  Structured data is published content, not metadata about it.
- The page now opens with a pointer to the kit for anyone who came looking for
  the method, once at the top rather than under all thirty-six tasks, where it
  would read as thirty-six adverts.
- The home page's "Not sure how to do one?" block promised step-by-step detail
  that is no longer there. It now points at the kit for the method and at the
  contents page for the schedule.

### Kept deliberately

- **All thirty-six anchors.** Every guide link inside all three feeds was
  checked against the rebuilt page: 36 of 36 still resolve. Nobody's calendar
  breaks.
- **`has_guide()` unchanged**, though it now reads oddly. It gates the link
  inside every event's `DESCRIPTION`, so narrowing it to check `GUIDES` alone
  would strip that link from all thirty-six events and force a `SEQUENCE` bump
  for no gain. There is a comment on the function saying so.
- **Curated video links**, when there are any. Those are other people's work,
  linked and not republished, so they were never the kit's to withhold.

Feeds are byte-identical to 1.9.0 and `SEQUENCE` stays at 1.

**Known wrinkle, deliberately not fixed here.** Each event's description still
labels the link "How to:", which is no longer quite what it leads to. Correcting
it changes all three feeds, so it is worth bundling with the first curated video,
which needs a `SEQUENCE` bump anyway.

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
