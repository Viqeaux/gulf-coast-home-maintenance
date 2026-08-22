# Handoff

Everything a fresh session needs to pick this up. Read this first, then
[README.md](README.md) for how the build works and [CHANGELOG.md](CHANGELOG.md)
for why things are the way they are.

Current version **v1.23.2**. Everything below is live unless marked otherwise.

---

## The products

| | What | Where | Price |
|---|---|---|---|
| **The calendar** | Three subscribe-able `.ics` feeds, one per tier, plus the site and the calendar contents page that hand them out | <https://gulfcoasthomemaintenance.com> | Free, and stays free |
| **The kit** | Every printable page, 27 of them, in two PDFs: print and fillable | Etsy only | $12.99 |
| **The agent edition** | The same 27 pages branded for a realtor, plus a 4 page leave-behind. Four PDFs, print and fillable of each | Etsy only | $39 |
| **The storm season binder** | 33 pages, mostly blanks: policies, room by room inventory, supply calculator, the countdown, shutdown, damage log, claim log, contractor vetting. Two PDFs, print and fillable | Etsy | $16.99 |
| **The reserve planner** | One spreadsheet, nine tabs. Quick Check, 49 systems, the IDK engine, a 30 year forecast and a funding dashboard. Built 2026-08-16, **not listed yet** | Etsy, plus a Sheets copy link | Not set. See below |
| **The storm season workbook** | One spreadsheet, ten tabs. The companion to the binder: deductibles in dollars, a 500 row inventory against the contents limit, the supply calculator, the damage log subtotaled by policy side, receipts and loss of use, the claim log, four contractors scored. Built 2026-08-16, **not listed yet** | Etsy, plus a Sheets copy link | Not set. See below |
| **The free calculator** | Four systems of the forty-nine, on the site. The teaser for the planner, and the only page that gives before it asks | <https://gulfcoasthomemaintenance.com/calculator/> | Free, and stays free |

**The binder is a different buying moment from the kit, and that is the point.**
The kit is a calm January purchase by somebody being responsible. The binder is
bought in August with a cone on the television. Chad's call, 2026-08-15: peak of
season is September 10, so the listing is the thing standing between this and
the revenue, not the build.

The words matter and were confused once already. **"Calendar" means the feeds.
"Kit" means the printables.** A previous session built the printable as a free
download, which is the opposite arrangement, and unwinding that touched the buy
slot, the section labels, the README and the listing copy.

**The step-by-step detail is kit only.** Settled by Chad on 2026-08-15 in
1.10.0. `docs/guides/` used to print all of `STEPS`, the tools, the numbered
steps and the caution, free to anyone, which gave away the thing the kit is
sold on. It now lists the thirty-six jobs and the month each falls in, which is
what the `.ics` feeds publish anyway, and points at the kit for the method.
Read "What the site may publish" in [README.md](README.md) before adding
anything to that page, including structured data.

**Owner:** Chad. Bought his first house at forty-five, built the list for
himself before it was a product. That origin is in the Etsy About section and is
the strongest thing in the listing. Do not embellish it.

## Live things

- **Site:** <https://gulfcoasthomemaintenance.com> (GitHub Pages, custom domain,
  HTTPS enforced). The old `viqeaux.github.io/gulf-coast-home-maintenance`
  redirects, so anything already pointing there still works.
- **Repo:** <https://github.com/Viqeaux/gulf-coast-home-maintenance>, **public**.
- **Etsy shop:** GulfCoastHomeCare
- **Etsy listing, the kit:** <https://www.etsy.com/listing/4555777332/new-homeowner-gift-undated-gulf-coast>
- **Etsy listing, the agent edition:** <https://www.etsy.com/listing/4556335504/realtor-closing-gift-branded-gulf-coast>
- **Etsy listing, the storm binder:** <https://www.etsy.com/listing/4556502794/hurricane-prep-binder-printable-home>
  Published by Chad 2026-08-15, and on the site the same day in 1.11.0 as
  section 05.
- **Email:** MailerLite, group **"General Signups"**, double opt-in on. It began
  as a waitlist for the kit and the buy button retired that job, so in 1.6.0 it
  became a general "hear about the next one" list living at the end of the free
  calendar section. The form endpoint is a form ID, so renaming the group did
  not move it and no code depends on the name.

## Build

```bash
python build_calendars.py       # feeds + calendar contents page, into docs/
python build_printables.py      # the kit PDF, into product/
python build_fillable.py        # the fillable twin, needs the PDF above first
python build_listing_images.py  # nine Etsy photos from the real pages
python build_video.py           # the 14 second Etsy listing video
python build_agent_edition.py   # the realtor edition, four PDFs. --logo bakes one in
python build_agent_listing.py   # nine photos for the realtor listing
python build_video.py --agent   # the realtor cut of the video
python build_pins.py            # eight Pinterest pins, 1000x1500
python build_site_images.py     # shop covers + nine page previews, into docs/img/
python build_brand.py           # shop icon and banner
python check_links.py           # finds curated videos that have died
python optimize_images.py       # after replacing docs/img/hero.png

python build_planner.py                   # the reserve planner, one .xlsx, into product/
python qa_planner.py                      # builds it, calculates it, runs the eleven cases
python qa_planner.py --checklist          # the five checks to do by hand in Sheets
python build_calculator.py                # the free calculator, into docs/calculator/

python build_storm_binder.py              # the binder, print PDF, into product/
python build_storm_binder.py --fillable   # both PDFs, 1,876 form fields
python build_storm_binder.py --fill-report  # lists pages with space going spare
python build_binder_listing.py            # ten Etsy photos for the binder
python build_video.py --binder            # the 14 second binder video

python build_workbook.py                  # the storm workbook, one .xlsx, into product/
python qa_workbook.py                     # builds it, calculates it, runs the fifteen cases
python qa_workbook.py --checklist         # the six checks to do by hand in Sheets
```

Content lives in six files: `build_calendars.py` holds the 36 tasks and the
`GUIDES` video table, which are the free half; `task_steps.py` holds the
step-by-step detail, `kit_sections.py` the seven conditional sections,
`binder_pages.py` all of the binder's writing, `planner_data.py` the planner's
49 systems with their lifespans and costs, and `workbook_data.py` the storm
workbook's lists and rule text, all five of which are **paid product only and
must not reach the site**.

**The planner needs `openpyxl`, the first dependency the project has had.**
`pip install openpyxl`. `qa_planner.py` also needs `formulas`, which is a test
dependency rather than a build one: nothing a buyer receives depends on it.

**The binder imports the kit's design system rather than copying it.**
`build_storm_binder.py` pulls `CSS`, `page()` and `esc()` out of
`build_printables.py`, and reuses `build_fillable.stamp()` for the fillable
twin. So the two products look like one shop, and a fix to the kit's type or
footer fixes the binder too. Only what the binder invents, the record blanks,
the log tables, the calculator, lives in its own `BINDER_CSS`.

**The binder build checks every page for overflow, and it is not optional.**
The kit learned the hard way that a page can run past its sheet invisibly and
come out truncated in the PDF. `--fill-report` also names pages using less than
85 percent of the sheet, which on a product made of blanks is writing space the
buyer paid for and did not get. Note that `.sheet` is `flex: 1`, so measuring
its own `scrollHeight` can never report short: the check measures how far the
content reaches instead.

**The site is six pages now, and three of them are hand-written.**

| Page | What it is for | Written how | Phone screens |
|---|---|---|---|
| `/` | Say what this is, prove it is Gulf specific, hand over one calendar | Hand-written `docs/index.html` | 9 |
| `/calendars/` | The four feeds one at a time, plus all the setup help | Hand-written `docs/calendars/index.html` | 4.5 |
| `/shop/` | Sell the three printables | Hand-written `docs/shop/index.html` | 13.4 |
| `/guides/` | The schedule, thirty-six jobs and their months | Generated by `build_calendars.py` | |
| `/calculator/` | The free teaser for the reserve planner | Generated by `build_calculator.py` | |
| `/resources/strengthen-mississippi-homes/` | First resource page: the roof grant, pointer form | Hand-written, prose layout like `privacy.html` | |

**Resource pages follow the pointer rule and carry a checked date.** See "The
direction" below before writing one. The sitemap is hand-maintained and a new
page goes in it in the same commit; `/shop/` and `/calendars/` were missing
from it from 1.22.0 until 1.24.0, which is the failure mode.

**Edit the Python for the generated two, not their output.** Everything in
`product/` is generated as well.

**The split happened in 1.22.0 and the reason is worth keeping.** On one page
the products sat between the argument and the free calendars, which put the
thing the site is named after at 77 percent scroll depth on a phone: screen
18.2 of 23.7, against the first buy button at 2.3. Split, the home page is 11.1
screens and the free calendars sit at 6.2.

**The home page carries the picker, not the four cards.** Chad's call,
2026-08-21: showing the individual feed cards and the picker together made the
reader choose between two ways of choosing. The picker answers the question
most people actually have, which is "just give me a calendar", so it is the
prominent one and the cards moved to `/calendars/` with the setup help.

**`docs/calendar-buttons.js` is shared by the home page and `/calendars/`.**
The feed buttons, the preview warning, the Android note, the clipboard handler
and the picker all live in it. Everything is guarded by an existence check, so
the file is safe on any page, and it returns immediately where there is no
`#calendars` section. Same reasoning as `site.css`: a thing two pages share
cannot live inside one of them.

**`docs/site.css` is shared by all three hand-written pages.** It was an 839 line
`<style>` block inside `index.html` until the shop needed the same look. Two
pages cannot each keep a copy, for the same reason `theme.css` and
`analytics.js` exist. Anything styling both pages belongs there.

**Live Pinterest pins point at `/#edition`, `/#agents` and `/#binder`**, which
were sections on the home page until 1.22.0. GitHub Pages cannot redirect, so a
small script at the top of `index.html` rewrites those three hashes to
`/shop/`. **Do not remove it.** Those pins are published, cannot be edited in
bulk, and Pinterest is one of the few traffic sources this shop has.
[product/pinterest.md](product/pinterest.md) still lists the old addresses; new
pins should use `/shop/#...` directly.

**`docs/img/cover-*.jpg` and `preview-*.jpg` are committed build outputs, and
that is deliberate.** `build_site_images.py` makes them from renders the listing
builders already produce, but those sources live under `product/`, which is
gitignored, so a fresh clone cannot rebuild them. Committing them is the only
way the site has images after a clone.

**The previews are crops, and the crop is the protection.** Each keeps only the
top slice of its page. On a month page the slice ends exactly where
[README.md](README.md) already draws the line: the task, the one-line
instruction and the "why" are above it and are free and already public in the
feeds, and the numbered steps start below it and never reach the image file at
all. Shrinking whole pages was tried first and does not work: at 420px wide the
body text of a month page is still legible.

**Adding an image, or raising a `keep_top` fraction, is a content decision.**
Read the header of `build_site_images.py` before either. If a preview looks
thin, change which page it shows rather than showing more of the same one.

**The hero's hurricane season countdown hardcodes three dates**, in the script
at the bottom of `docs/index.html`: June 1, September 10, November 30. The same
three appear in the hero stat strip and in `binder_pages.py`. If the season
framing ever changes they all move together. The line picks whichever of the
three is next rather than printing all of them, so every branch matters: it was
checked against all 365 days of a year, and the December branch rolls to the
following June.

## Rules that are not obvious

**The repo is public and the kit is the paid product.** Everything in
`product/` except `etsy-listing.md` is gitignored. Committing the PDF would
publish the thing being sold as a free download. Check `git status` before
committing anything under `product/`.

**No em dashes, anywhere.** Chad's explicit preference. 162 were removed once
already. Use commas for short asides, full stops for independent clauses, colons
for definitions. A blind swap to commas creates splices.

**American English.** Thirty-one Britishisms were fixed once: "stabiliser",
"vapour", "colour", "labelled", plus vocabulary a spellchecker misses, like
"torch" for flashlight, "tap" for faucet, "autumn" for fall. The product claims
local expertise, and this undercuts it. It is a recurring default, so watch for
it.

**Costs in the planner: defaults yes, quotes never.** The old note under next
products said not to hardcode replacement dollar amounts at all, because they go
stale, vary by market, and a wrong number in a sold product is a support
problem. That still holds, and the planner ships 49 of them anyway, which is a
deliberate change of position rather than an oversight. Chad's call,
2026-08-16. What makes it safe is the three things that note assumed would not
exist:

1. **An override column beside every default.** Put a real quote in column N and
   the entire workbook follows your number instead of ours. `START HERE` frames
   that as the expected path, not a fallback.
2. **A visible range next to every point figure**, on the reference tab and in
   the tab's own header text. A number with a range printed beside it does not
   read as a quote.
3. **A sourcing note per row**, one of `kit`, `consensus` or `estimate`. Anything
   marked `estimate` is ours and says so.

The rule that replaces it: **a default may ship if it carries a range, a source
note and an override.** A bare number may not. The same three apply to any
regional edition, and the region factors themselves are `estimate`.

**Lifespans are locked to the kit and the kit wins.** `check_against_kit()` in
`planner_data.py` maps 19 planner systems onto `WATCH_LIST` in
`build_printables.py` and fails the build if a default drifts outside the range
the kit prints. A buyer can own both products and hold them side by side, and
the kit is the one already published in a PDF, so the planner is the one that
moves.

**Four version markers, and they must agree:** `VERSION` in
`build_calendars.py`, the footer of `docs/index.html`, an entry in
`CHANGELOG.md`, and an annotated git tag. Rebuild after changing `VERSION`, or
the guides page keeps reporting the old one.

**`SEQUENCE` is not the version.** It lives in `build_calendars.py` and is what
tells a calendar client an event actually changed. Bump it only when task
content changes. It is at **2**: 1 was every event gaining a guide link, and 2
was 1.20.0 spreading the task dates across the month, relabelling that link, and
adding the Monthly Rounds feed. A design or infrastructure release does not need
it.

**Task dates are now the tier.** Must Do on the 1st, Should Do on the 10th,
Going Above on the 20th, and November 30 left alone because it is the close of
the season. Moving them again means another `SEQUENCE` bump and another round of
every subscriber's events shifting under them, so it is not a thing to tidy.

**There are fifteen feed addresses, not four.** The four singles are the ones
the cards hand out. The other eleven are every combination of two or more,
built by `all_combos()` and chosen by the picker in the calendar section, so
somebody who wants three of the four gets one calendar instead of three
sidebar entries. **`combo_file()` in `build_calendars.py` and the picker's
filename logic in `docs/index.html` must agree**, or the picker hands out a
404; each has a comment pointing at the other. All fifteen were exercised in a
browser at 1.21.0.

**Per-task customization needs a server and is not possible here.** Picking
individual tasks is 2^36 combinations, so it cannot be pre-built. It wants a
small Worker assembling feeds from query parameters, which is worth folding
into the Cloudflare Pages move recorded below rather than justifying alone.
House-specific tasks are a separate problem again: the conditional sections
live in `kit_sections.py` and are paid-only, so "customize for my house" is a
pricing decision before it is a technical one.

**There are four feeds, not three.** The fourth is Monthly Rounds, seven events
a month grouped by area, and it is deliberately not a fourth tier: the tiers are
levels of effort on the seasonal list, this is the routine that repeats whatever
the season. It lives in `MONTHLY_ROUNDS` rather than `TASKS`, which is what
keeps it out of the printed kit. Anything added to `TASKS` reaches the kit;
anything added to `MONTHLY_ROUNDS` does not.

**Cut versions without being asked**, when a coherent piece of work lands and is
verified. Not every commit, and not a half-finished feature.

**Verify the feeds are byte-identical** after any change that should not affect
subscribers. Hash them against the previous tag. It has caught real mistakes.

## Gotchas that cost time

**GitHub Pages silently misses build triggers.** Three times now the commit
landed but no deployment was created. The tell: `raw.githubusercontent.com`
shows the new content while the site shows the old. Check
`api.github.com/repos/Viqeaux/gulf-coast-home-maintenance/deployments` for the
latest sha rather than waiting longer. Fix is an empty commit.

**Check the deployment's state, not just its sha.** A queued deployment already
reports the new sha while still serving the old build, so a sha match alone says
nothing. Follow `statuses_url` and wait for `success`. On top of that the CDN
sends `Cache-Control: max-age=600`, so the site can lag a successful build by up
to ten minutes. In 1.7.0 that combination read exactly like a second failure and
sent a session chasing one that was not there.

**Never commit a `CNAME` before DNS resolves.** Doing that took the site down:
Pages starts redirecting immediately, and deleting the file does not undo it
because the domain lives in repo settings too. DNS first, `CNAME` last.

**`.gitattributes` pins `*.ics` to `-text`.** Windows autocrlf would rewrite
them to LF, and RFC 5545 requires CRLF. Without it a Windows checkout publishes
a malformed feed.

**Chrome's print-to-PDF emits no form fields.** That is why `build_fillable.py`
measures positions in the browser and stamps AcroForm fields on afterwards. When
merging, clone from the overlay and merge the page underneath, or `/AcroForm`
is left out of the catalog and readers refuse to fill the form.

**Listing images need the window sized to the sheet** (816x1056 CSS px) with
resolution coming from the device scale factor. A bigger window just renders the
page small in the corner of a white canvas.

**Kit pages can overflow their sheet silently.** Invisible in HTML, truncated in
the PDF. Measure `.sheet` scroll height against the page box after content
edits. `TWO_PAGE_MONTHS` exists because May measured over.

**CSS shorthand `margin` overwrites the sides.** Cost two rounds of "it looks
off-center". And `min-width` does nothing on an inline element, which an anchor
is by default.

## Market data, from Etsy Marketplace Insights

Searches per 30 days against competing listings. This is what set the price and
the positioning.

| Term | Searches | Listings | Ratio | Converts |
|---|---|---|---|---|
| **realtor closing gift** | **9,400** | 31.3k | **1:3.3** | Very low |
| **new homeowner gift** | **899** | 89k | 1:99 | **High** |
| housewarming gift | 63,100 | 1.4M | 1:22 | Low |
| new home gift | 31,700 | 671k | 1:21 | Typical |
| closing gift for clients | 215 | 12.9k | 1:60 | Very low |
| home maintenance | 159 | 70.6k | 1:444 | High |
| home maintenance checklist printable | 47 | 8.6k | 1:183 | Very low |
| first time home buyer gift | 35 | 24.9k | 1:711 | High |

**What it means.** The obvious maintenance terms are dead. The giant gift terms
are unwinnable for a new shop. **Volume is the binding constraint, not price**,
which is why $12.99 rather than $7.99: you cannot make up the difference on
units when the search term gets 47 a month. Etsy is the checkout; discovery has
to come from Pinterest, the free feeds, and the site.

Only ~1 task of 36 mentions salt. The real drivers are heat and humidity (~14
tasks), hurricane season (~5), termites (2), freeze (2). So the content is
**Gulf South regional, not coastal-only and not national**. Regional editions
for other climates are a later product line, not a rebrand.

## What to do next, as of 2026-08-21 evening

Ranked. The site is in good shape after 1.19.1 through 1.23.2 and **site work
has hit diminishing returns**: everything there improves conversion for people
who already arrive, and almost nobody does. Analytics went live this morning,
so the first real traffic numbers exist within a week.

**Peak of hurricane season is September 10.**

1. **Run the Insights tag check. The quota returns around 2026-08-22.** The
   marketing plan's own first priority is Etsy SEO, all thirteen tags on the
   binder are reasoned rather than measured, and the spend order is written
   below so no search is wasted. Ten minutes, and the window closes with the
   season.
2. **Price and list the reserve planner and the storm workbook.** Two finished
   products earning nothing, with no price set and, as of this date, **no
   listing copy written at all**: the kit, binder and agent edition each have an
   `etsy-listing-*.md` and these two have nothing. Writing both is the largest
   piece of work a session can do here without Chad.

   **An Etsy listing is itself a traffic source**, which is the counter to
   "traffic is the constraint, so do not build more." That reasoning is right
   about the site and wrong about Etsy: the site converts arrivals, a listing
   creates them. Two more listings are two more surfaces in Etsy's own search.
3. **Pinterest pins for the binder.** The plan calls Pinterest the best free
   channel for printables and pins stay discoverable for months. `build_pins.py`
   exists. New pins must link to `/shop/#binder` rather than the old home page
   anchors: see the redirect note above.
4. **The kit's cross-sell line**, parked twice now. Five minutes, no cost.

**Do not spend another session on the site's layout** without a reason from the
analytics. It went from 23.7 phone screens to 9 on the home page and 9.8 on the
shop in one evening, and the next change to make is not obvious from the inside.

## The direction, set by Chad on 2026-08-21

**Make the site the place people go for Gulf Coast home maintenance**, not only
a shop with three printables behind it. This is the same conclusion the
marketing plan reaches from the other end and the same one the 1.23.2 decision
reached about product pages: **content that earns traffic beats pages that
reorganize the traffic you already have.** Nobody is arriving, so the work worth
doing is the work that makes strangers arrive.

It does not displace the Insights tag check above. That is deadline-driven and
takes ten minutes. It does reframe everything after it.

### Refined by Chad later the same day: the site points, it does not claim

**The site never presents itself as the authority.** Chad's words: no claims,
no implying the site is the authority, just link to the resources and make them
easier to go through. The agreed shape, which Chad approved as a hybrid:

- **Facts that belong to institutions**, grant terms, deductible rules, flood
  zones, program status, are always attributed and linked, never restated in
  the site's own voice. A page says "their page says", names the source, and
  sends the reader there for the rules.
- **The spine of each page is something this shop legitimately owns**: a
  question-shaped walkthrough, or a small interactive tool in the calculator's
  mold. Curation is the supporting layer, not the product, because pure link
  lists do not rank and nobody pins them.
- **Every resource page carries a visible "checked on" date**, and editing a
  fact means re-checking it against the source and moving the date. This
  replaces the heavier verify-every-claim rule for pages that make no claims:
  what gets verified is that each destination actually says what the framing
  implies.
- The relevant product is the quiet next step at the end, one paragraph, with
  an explicit not-affiliated, not-endorsed disclaimer on the page.

**The first page under this rule shipped in 1.24.0:**
`docs/resources/strengthen-mississippi-homes/`, hand-written, measured by
analytics, linked from the three hand-written footers, the sitemap, and, as
of 1.24.1, a hero line on the home page in the calculator's slot, because a
footer link alone is a route for crawlers and Chad caught that within the
hour. One hero line per resource page holds up to two of them; a third means
building a resources index page and pointing one hero line at it. The
next two candidates in the same mold: a wind-deductible mini-tool (type your
dwelling limit and percentage, see the dollar figure; arithmetic, not advice)
and a find-your-flood-zone walkthrough around FEMA's map tool.

### The rule that comes first

**Nothing regulatory goes live until it has been checked against the primary
source, and the page carries the date it was checked.** Chad's own framing, and
it is the right one: being the site that is correct is worth more than the
traffic. Competing sites still promise a 30 percent federal credit that no
longer exists.

This matters more here than on most sites. A reader who believes they qualify
for a grant, and does not, has spent money on the strength of this page. Treat
eligibility rules, dollar figures and dates as claims to verify rather than
copy to paste, and put a "checked on" line on any page describing a program,
because a program with an expansion date will go stale.

### The lead opportunity: verified 2026-08-21 and the page is live

**Strengthen Mississippi Homes**, administered by the Mississippi Insurance
Department:
<https://www.mid.ms.gov/mississippi-insurance-department/preparedness/mitigation/smh/>

Checked against MID's own page on 2026-08-21, and Chad's research held up
almost entirely: up to $10,000 for FORTIFIED Roof upgrades, paid directly to
the contractor, currently limited to Wind Pool (MWUA) policyholders in
Hancock, Harrison and Jackson counties who have held coverage three
consecutive policy years, owner-occupied single-family primary residences
only, evaluator's fee not covered. MWUA is at <https://www.msplans.com>,
confirmed as the wind pool's site, and it carries its own June 2026 notice
about the program.

**The one specific that did not verify: "statewide expansion expected early
2027."** That date appears only in contractor blogs, not in any primary
source, so the live page does not print it. What is verifiable: Senate Bill
2409 passed unanimously in spring 2026 (Magnolia Tribune, 2026-04-02), the
statute is written statewide with awards by lottery, and MID says the program
"will open periodically throughout the year." Also floating around: a stale
2025 claim that funding was suspended; MID's current page supersedes it.

The page is live at `/resources/strengthen-mississippi-homes/`. When a new
phase opens, updating it and moving the checked date is cheap and is exactly
the second life the page was built for.

### Do not build a page on the federal energy credits

The 25C Energy Efficient Home Improvement Credit and 25D were terminated by the
One Big Beautiful Bill Act for property placed in service after 2025-12-31.
**Also unverified and worth checking**, but if it holds, a page promising 30
percent back is exactly the mistake this site should be the one not making.
There is an honest page in saying the credits ended and what replaced them, if
anything.

### The reference list Chad assembled

Storm and flood:

- Ready.gov hurricanes, <https://www.ready.gov/hurricanes>
- FEMA Flood Map Service Center, flood zone by address, <https://msc.fema.gov/portal/home>
- FloodSmart / NFIP, <https://www.floodsmart.gov>
- National Hurricane Center, <https://www.nhc.noaa.gov>
- NWS New Orleans and Baton Rouge, which covers the Mississippi coast, <https://www.weather.gov/lix>
- MEMA, <https://www.msema.org>, hurricanes page <https://www.msema.org/prepare/types-disasters/hurricanes>
- disasterassistance.gov, <https://www.disasterassistance.gov>

Home safety and systems:

- CPSC recalls, a natural annual "check your appliances" task, <https://www.cpsc.gov/Recalls> and <https://www.saferproducts.gov>
- EPA mold, <https://www.epa.gov/mold>
- EPA radon, <https://www.epa.gov/radon>
- EPA lead and the RRP rule, <https://www.epa.gov/lead>
- DOE Energy Saver, <https://www.energy.gov/energysaver/energy-saver>
- ENERGY STAR maintenance checklist, <https://www.energystar.gov/saveathome/heating-cooling/maintenance-checklist>
- HUD Healthy Homes, <https://www.hud.gov/hudprograms/healthy-homes>
- Mississippi State Department of Health, private well testing, <https://msdh.ms.gov>

**A page that is only this list is worth very little.** Link lists do not rank
and nobody links to them. The list is raw material for pages that answer a
question, not a page of its own.

### Federal works are public domain, with four caveats

United States federal government works are not under copyright, 17 U.S.C. 105,
so Ready.gov and FEMA checklist material can be **adapted into the binder and
the calendar** rather than merely linked. That is a real content supply and it
is the largest thing on this page.

1. **Agency logos and seals are protected separately** from the text. Do not use
   them.
2. **FORTIFIED is an IBHS trademark**, not a government one, so it does not get
   the same treatment.
3. **State and county material is not automatically public domain.** MEMA and
   county items have to be checked individually.
4. **Public domain does not permit implying endorsement.** Adapting Ready.gov
   text is fine; laying a page out so a buyer infers FEMA endorses a product for
   sale is a different problem from copyright, and it applies to the paid PDFs
   more than to the site.

### Open question Chad has not answered

He asked that the products be "compliant with all regulations". That could mean
building code accuracy, insurance claim guidance being defensible, FTC rules
about how the products are described, or accessibility. They need different
work, and the products already carry a disclaimer that they are not a substitute
for an inspector, contractor or policy terms. **Ask which one he means before
starting compliance work.**

### The recommended first move: done, 2026-08-21, in 1.24.0

The Strengthen Mississippi Homes page is built and live, in the pointer form
described above: researched, dated, honest about who does not qualify, binder
as the quiet next step, not-affiliated disclaimer at the bottom. If it ranks,
that is the template and it repeats. If it does not, a day is lost rather than
a strategy. The 25C and 25D status remains unverified because no page is being
built on it; verify before ever writing one.

## Permission prompts, and why the allowlist is small

`.claude/settings.json` holds twelve entries, all read-only: the browser tools
that read a page and GETs to this site and this repo's API. That is genuinely
all that is safely allowlistable, and it is worth writing down why so nobody
adds more.

The prompts come overwhelmingly from three places that **must not** be
blanket-allowed: `python` heredocs and `javascript_tool`, which are arbitrary
code execution, and `git add`/`commit`/`push`/`tag`, which mutate and one of
which publishes to a public repo. `grep`, `sed`, `head`, `tail`, `ls`, `wc` and
the read-only `git` subcommands never prompt at all, so entries for them do
nothing.

`.claude/settings.local.json` is gitignored, personal, and had grown to 140
entries, most of them exact one-off command strings carrying version numbers or
temp paths that can never match again. It is worth pruning and it is Chad's.

**The real lever is a permission mode, not an allowlist.** `acceptEdits` clears
the file-edit prompts, which are the largest single share, and everything here
is in git and recoverable. `bypassPermissions` clears everything including
`git push` to a public repo, which is the one worth thinking about. Neither is
set; Chad has not chosen.

## Outstanding

**The free calendar's real problem is that nobody can tell it is working.**
Found on 2026-08-21, when Chad concluded his own feed had broken. It had not.
Two separate causes, one fixed and one open.

**Fixed in 1.19.1.** The site claimed that adding the feed from a browser makes
it "appear on every device on that account". It does not. Google keeps a
per-device sync list for the mobile app, and a newly subscribed calendar starts
switched off, so it shows on desktop and never reaches the phone. Worse, if the
calendar is missing from the app's own Settings list, nothing inside the app can
fix it: the only control is `calendar.google.com/calendar/syncselect`, which the
app does not link to. Both facts are now in the Google panel on the site.

**Fixed the same day, in 1.20.0.** Every event used to sit on the 1st, so
thirteen days a year carried anything at all and a subscriber opening a week
view on any of the other three hundred and fifty-two saw an empty calendar with
no way to tell that from a broken feed. Dates are spread now: Must Do on the
1st, Should Do on the 10th, Going Above on the 20th, November 30 left alone.
`SEQUENCE` went to 2 and the "How to:" label was relabelled in the same bump,
which is what it had been waiting for. **Do not move task dates again without
another `SEQUENCE` bump.**


**The binder is launched and on the site.** Chad published the listing on
2026-08-15 and it went onto `docs/index.html` the same day, in 1.11.0, as
section 05 with its own `BINDER_URL` and a `Product` entry in the structured
data. Both PDFs render and verify: 33 pages, every page measured against its
sheet, 1,876 uniquely named AcroForm fields with `/AcroForm` in the catalog and
every widget on its page. Peak of season is September 10, so what is left is
worth doing in the next three weeks rather than eventually:

1. ~~Mail the MailerLite list.~~ **Dead for now: the list has no subscribers**,
   confirmed by Chad on 2026-08-15. Do not rank this again until it does. It is
   worth reading as a result rather than a detail: the signup has been live
   since 1.6.0 and Pinterest since 2026-08-15, and between them they have
   produced nobody. **The shop's constraint is traffic, not conversion or
   price.** Nothing on the site is broken; there is simply almost nobody
   arriving. Any future session weighing what to build should weigh it against
   that, because another product sells to the same empty room.
2. Add a cross-sell line to the kit's description, the way the kit already
   points at the realtor edition. **Chad is leaving this for later, as of
   2026-08-15.**
3. **Run the tag list through Etsy Marketplace Insights. Blocked until roughly
   2026-08-22:** Chad is out of Insights searches until then. Do not send a
   session at this before that date. Every keyword on the binder listing is
   reasoned rather than measured, because the market data table below covers
   gift and maintenance terms and not storm terms. Tags are editable on a live
   listing, so this stays worth doing when the searches come back, and there is
   still room before September 10.

   **Spend the searches in this order**, since the quota is the scarce thing
   rather than the time:

   1. The four near-synonyms: `hurricane prep`, `hurricane checklist`,
      `hurricane season`, `storm prep`. Four of thirteen slots on terms that
      overlap heavily is the biggest thing the data could correct, and freeing
      even one slot is a real gain.
   2. The evergreen four: `home inventory`, `insurance claim`, `important
      documents`, `disaster planning`. These are what earn between seasons, so
      a dud here costs all year rather than for six weeks.
   3. `printable binder` and `gulf coast`, the two most likely to be dead
      generic weight.

   **Do not spend one on `new homeowner gift`.** It is already in the table
   below at 899 searches against 89k listings and flagged high converting.

   **One trap when the searches return.** If Insights reports trailing 30 days,
   storm terms measured in late August sit near seasonal peak and will look
   far stronger than their annual average, while the evergreen terms are being
   measured at their normal level. Do not let that flatter the storm terms into
   displacing the evergreen ones. The 5 storm, 4 evergreen, 2 descriptive, 1
   gift split is a deliberate hedge: replace within a category.
4. **The site placement is worth revisiting out of season.** The binder sits
   above the agent edition because it sells to the same homeowner as the kit
   and because it has a deadline. In February it is the one product on the page
   nobody is shopping for, and the order that is right in August is not
   obviously right in January.

**The reserve planner is built and unlisted.** Chad asked for it on 2026-08-16
against a written spec, and it landed the same day: `build_planner.py`,
`planner_data.py` and `qa_planner.py`, one .xlsx of nine tabs, 49 systems, 100
register rows and a 30 year forecast. All eleven QA cases pass against a real
formula engine, plus a file-structure pass for the parts a formula engine
cannot see, re-confirmed green on 2026-08-21. Nothing about it is on the site or on Etsy. What is left, in order:

1. **Verify the numbers before listing, and treat this as the gate.** The
   lifespans are sound: 19 of the 49 are locked to the kit's Watch List by a
   build-time check, and the rest are consensus trade figures. **The costs and
   the seven region factors are ours and are marked `estimate` or `consensus`
   in column I, and none of them has been checked against a published source.**
   The spec Chad wrote says it plainly: a buyer who finds a wildly wrong number
   leaves a two-star review that kills the listing. Worth a pass against
   Remodeling Magazine's Cost vs Value report and the InterNACHI life
   expectancy chart, correcting `planner_data.py` and updating the source note
   per row as it goes. Do not reproduce either source's table wholesale, cite
   it per row.
2. **Decide the price.** The old note here said $9.99. What got built is
   considerably more than that sketch, and Chad's spec suggests $20 to $35
   standalone and $40 to $50 bundled with the kit. The binding constraint is
   still traffic rather than price, which argues for the top of the range
   rather than the bottom: at these volumes the extra ten dollars is the whole
   difference and there is nobody to lose.
3. **Import it into Google Sheets once and run `qa_planner.py --checklist`.**
   Five checks, and the fourth one, whether the chart survived, is the one that
   matters, because the forecast chart with the reserve line dipping negative
   is the listing screenshot.
4. **Then the listing**, and a `build_planner_listing.py` alongside the other
   three listing builders. There are no page renders to reuse here, so the
   photos have to come from screenshots of the real workbook.

**One thing to weigh before any of that.** The shop's constraint is traffic,
not products, and this is a fourth thing to sell to the same empty room. The
free web calculator under next products is the item that changes that, and the
planner's math is what it was waiting on.

**The storm season workbook is built and unlisted.** Chad asked for it on
2026-08-16 against a written spec and it landed the same day: `build_workbook.py`,
`workbook_data.py` and `qa_workbook.py`, one .xlsx of ten tabs. All fifteen QA
cases pass against a real formula engine, including the print setup and the
protection, which a formula engine cannot see and openpyxl reads back out of the
shipped file. Nothing about it is on the site or on Etsy.

**It is the companion to the binder, not a fifth standalone.** The positioning
line is the whole product and belongs in both listings: *the binder is what you
carry, the workbook is what you calculate.* Do not rebuild the countdown, the
shutdown sequence, coming home, the go bag, what to photograph or the calm-week
list in it. Those are narrative and sequential, they are better on paper, and
duplicating them makes the bundle look like one product sold twice.

What is left, in order:

1. **Decide the price.** The spec says $18 to $28 alone and $35 to $45 bundled
   with the binder. The same argument as the planner applies and points at the
   top of the range: the binding constraint is traffic rather than price, so at
   these volumes the extra ten dollars is the whole difference and there is
   nobody to lose.
2. **Import it into Google Sheets once and run `qa_workbook.py --checklist`.**
   Six checks. The one that matters is number 3, that B19 to B24 on
   `Coverage & Deductibles` are empty, yellow, and refuse a typed zero, because
   the entire safety argument for the product rests on a blank limit never
   reading as a limit you are inside of.
3. **The money screenshot is `Coverage & Deductibles`** with a $400,000 dwelling
   limit and a 2 percent wind deductible resolving to $8,000, with the gap in
   red below it. That one image is the pitch, and QA case 2 asserts the number.
4. **Then the listing**, and a `build_workbook_listing.py` alongside the other
   listing builders. There are no page renders to reuse, so the photos have to
   come from screenshots of the real workbook, the same problem the planner has.

**Two things in the spec were changed on purpose, and both were right.** Em
dashes came out of the dropdown values, because those strings are also `SUMIF`
criteria and a punctuation fix later would silently break a subtotal. And the
spec's count of un-entered sub-limits,
`COUNTIF(range,"Limit not entered")+COUNTIF(range,"LIMIT NOT ENTERED*")`,
double-counts every gray row: `COUNTIF` is case-insensitive, so the wildcard
matches the exact string as well. It counts entered limits and subtracts.

**The thing most likely to be broken by a future edit** is the blank-limit
handling. `='Coverage & Deductibles'!$B$19` on an empty cell returns 0, not
blank, and every policy figure that crosses a tab boundary is wrapped in
`IF(source="","",source)` to keep the emptiness. Take one of those wrappers off
and the workbook starts telling buyers they are within a sub-limit they have
never looked up, with no error anywhere. QA cases 6a and 6b exist for exactly
that and will catch it.

**What Breaks Next became the planner's Quick Check tab.** For a few hours on
2026-08-16 it was a standalone `.html` download, all 49 systems in one
self-contained file. Chad killed that the same day and he was right: a raw
`.html` attachment cannot be relied on to open on a phone, Etsy buyers are
heavily mobile, and a tool that will not open is worth nothing.

**No static file format fixes that**, which is worth writing down so nobody
re-opens it. PDFs and images cannot compute. PDF JavaScript only runs in
Acrobat. A zipped `.html` is worse on a phone rather than better. The only
thing that reliably calculates on a phone is a spreadsheet, and there already
was one.

So it is tab three of the workbook now: two cells on Setup, the twelve systems
almost every house has, and a headline count across the top. It answers before
the buyer spends thirty minutes on the register, which is a better product than
the download was. `product/gulf-coast-what-breaks-next.html` is deleted and was
never committed.

**The free calculator is on the site.** `docs/calculator/index.html`, four
systems, built by `build_calculator.py` from the same numbers. Placed the same
day: a line in the hero under the two buttons, both footers, the guides page
tailpiece, and `sitemap.xml`.

**It is a line rather than a third hero button on purpose.** Three buttons turn
a clear choice into a menu, and this is the offer most likely to be taken by
somebody not yet sure they want a calendar. Nothing else on the site answers a
question before asking for something, which is what makes it the only page here
worth linking or pinning, and the shop's constraint is traffic.

What is left on the pair:

1. **`BUNDLE_URL` in `build_calculator.py`** when the planner is listed. That
   turns the free page's buy slot from the signup anchor into a buy button.
2. **A pin for it, after the two week read on the first eight.** A calculator
   pins far better than a printable does. Resist adding it sooner: a burst from
   a young account reads as spam and destroys the signal being waited on.
3. ~~Nothing has been deployed.~~ **Live as of 2026-08-16.** Pushed with
   v1.18.0 and verified: the deployment reached `success` rather than sitting
   queued, `/calculator/` returns 200, the footer serves v1.18.0, and the
   homepage links the page. **This is the first thing the shop has ever put up
   that answers a question before asking for anything**, so it is also the first
   real test of whether the constraint is traffic. Nothing measures it yet, which
   is item 5 under "Waiting on Chad" and is now overdue rather than early.

**Deferred, and do not re-propose it.** Outbound links from the calculator to
county appraisal records, so a visitor who does not know their build year can go
and find it, plus serial number date decoders. Both are real improvements to the
one blocker the page has. Chad's call, 2026-08-16: after there are sales, not
before. He is right that it does not touch the constraint, which is that almost
nobody is arriving. Note the boundary if it ever comes back: "How to date what
you own" is a kit page and sits on the paid side of "What the site may publish",
so linking somebody else's decoder is adjacent enough to be Chad's decision.

Worth keeping straight either way: **linking out is free, pulling live data in
is not.** The calculator's policy is `connect-src 'self'` and the page tells the
visitor that nothing they type leaves their machine. Fetching from a third-party
origin would widen that policy and make the promise false. The zero-tracker
posture is an asset the privacy page claims out loud; do not spend it on
convenience.

**The video is built.** `python build_video.py --binder` makes a fourteen
second cut from the binder's own pages, into `product/listing-binder/`. It
opens on the wind deductible, which is the one fact most homeowners have never
looked up, and closes on the claim log, which is the only thing in the shop no
free hurricane checklist carries.

**Do not commit the binder before reading item 2 under "Waiting on Chad".**
`binder_pages.py` is the entire content of the highest-value product in the shop
and the repo is public. The build outputs are already covered by
`product/*.pdf` and `product/*.html` in `.gitignore`, so nothing leaks by
accident, but the source does not have that protection and neither does
`task_steps.py` today. This is the same open decision as before, with more
riding on it.

**Both listings are done.** Files, title, description, tags, materials,
category, price, photos and video are live and current for each, and they match
[product/etsy-listing.md](product/etsy-listing.md) and
[product/etsy-listing-realtor.md](product/etsy-listing-realtor.md). The kit's
personal-use license still withholds bulk client printing, which is what makes
the agent edition worth buying, and it now points at that listing rather than
promising a future one.

**The agent edition takes work per order, but only sometimes.** Text branding is
self-serve: the buyer types into AcroForm fields and saves. A logo cannot work
that way, so a logo means running `build_agent_edition.py --logo` for that order
and sending the four files back through Etsy Messages. Four minutes. The listing
has **no custom option fields on purpose**, so nothing at checkout promises the
buyer anything that depends on you being awake. Read the "Why no custom options"
section before adding any.

**The site was reviewed end to end in 1.9.0** for security and branding. Most
of what came out of it is fixed and shipped. What is left needs Chad's hands or
Chad's decision, and is listed under "Waiting on Chad" below. Nothing on the
site is known to be broken.

**Pinterest is launched.** Live as of 2026-08-15: the account, the boards, all
eight pins, and the domain claim, whose `p:domain_verify` tag is in the head of
`docs/index.html`. The two binder pins went up the same day with product tags
connecting them to the Etsy listing. `build_pins.py` makes the pins and
[product/pinterest.md](product/pinterest.md) holds the boards, the covers, the
copy for every pin, and the setup steps. Re-run the script and re-upload if a
pin's source page changes.

The profile cover, the About text and the Website field were all done by Chad
the same day. One thing is left, and it is not urgent:

**`08-home-inventory` is on the Hurricane Prep Checklist board, and it was
built to be the thing that is not seasonal.** Home inventory and insurance
claims are searched in every month, and that pin is what keeps the binder
earning from November to May, the same way half the listing's Etsy tags are
deliberately not about hurricanes. A board name is a ranking signal, so on a
hurricane board Pinterest reads that pin as hurricane content and it goes quiet
with the season.

The fix is a minute of work and does not involve moving anything: make the
**Home Inventory and Insurance** board, description in
[product/pinterest.md](product/pinterest.md), and save the existing pin to it
as well. A pin can sit on several boards, and the second one gives it the
year-round context without costing it the storm-season one.

**Board names on the account do not all match the table in
`product/pinterest.md`.** "Hurricane Prep Checklist" is the live name of what
that table calls "Hurricane Season Prep". The table is the spec, not a record
of what exists, so check the account before assuming a name.

**No pin has been measured yet.** Nothing was built against Pinterest data
because there is none. Give the first pins two weeks, then let saves and clicks
pick the next batch rather than a guess. Resist adding pins in the meantime: a
burst from a young account reads as spam and it also destroys the signal being
waited on.

## From the design critique, 2026-08-15

An external critique was run against the site. What it got right shipped in
1.14.0. It was working from a page three versions old, so several findings were
already fixed, and the list below is what was **deliberately not done**. Do not
re-open these without reading the reason.

**1. Page previews of the kit. Chad's decision, and it is a real tradeoff.**
The critique's strongest point: a printable with no images of itself asks for
blind trust at the moment of payment. The problem is that
[README.md](README.md) "What the site may publish" puts the Watch List, How To
Find Out and Your First Month explicitly on the paid side, settled by Chad in
1.10.0, and `build_listing_images.py` renders exactly those pages. Publishing
them on the site would undo that decision by the back door.

Three ways forward, in the order I would try them:

- `01-cover.png` gives nothing away and can go up today.
- Cropped or angled shots that show density and typography without being
  readable, which is standard for printable listings.
- Full page renders, which is genuinely reversing the 1.10.0 decision. It may
  be the right call, since these images are already public on the Etsy listing,
  but it is a reversal and should be made as one rather than drifted into.

**2. Renaming the "Going Above" tier.** The critique is right that it breaks the
verb pattern the other two share. It is not a copy tweak: the tier name is in
`TIERS` in `build_calendars.py` and therefore in the `X-WR-CALNAME` of a feed
people have already subscribed to. Renaming it changes what every existing
subscriber sees in their sidebar, forces a `SEQUENCE` bump, and has to be done
across the kit, the agent edition and the binder at the same time or the
products disagree. Worth doing one day, as its own release, never folded into
something else.

**3. Removing the footer version.** It is one of the four version markers, and
the comment above it says why it is visible: so a tester can say which version
they were looking at. The critique called it developer-facing, which it is, on
purpose.

**4. Moving the agent section below the free calendars.** Would put two paper
sections next to each other again and undo the alternation fixed in 1.11.1. The
current order also already answers the underlying worry, since the binder sits
between the kit and the agent pitch.

**5. A dedicated `/agents` landing page.** Genuinely a good idea and the agent
edition is the highest margin product. It is a new page rather than a fix, and
it wants ad spend pointed at it to be worth anything, so it belongs on the
product list rather than in a critique response.

**6. Moving the signup below the About section.** Left where it is. Both spots
are defensible and there is no data to choose between them, and with zero
subscribers the binding constraint is traffic rather than placement.

## Waiting on Chad, from the 1.9.0 review

In priority order. Item 2 is the one that still matters.

**1. The domain email records. Done 2026-08-15.** Verified live against both
Cloudflare and Google public resolvers:

| Type | Name | Value |
|---|---|---|
| MX | `@` | null MX, priority `0`, meaning this domain receives no mail |
| TXT | `@` | `v=spf1 -all` |
| TXT | `_dmarc` | `v=DMARC1; p=reject; sp=reject; adkim=s; aspf=s;` |

Stricter than the version originally recommended. There is deliberately no
`rua=` reporting address, so enforcement works but no aggregate reports arrive.
If mail ever gets sent *from* the domain, loosen SPF then.

**2. The public repo still rebuilds every paid product, and each new one raises
the stakes.** `build_printables.py` holds `WATCH_LIST` and `FIRST_MONTH`,
`kit_sections.py` the seven conditional sections, `task_steps.py` all thirty-six
step-by-steps, `binder_pages.py` the whole binder, `planner_data.py` all 49
systems with their lifespans and costs, and now `workbook_data.py` the storm
workbook's lists and rule text. A clone plus `python build_printables.py` is the
$12.99 kit; `build_agent_edition.py` is the $39 one; `build_storm_binder.py` is
the $16.99 one; `build_planner.py` is the planner; `build_workbook.py` is the
storm workbook. `.gitignore` protects the built PDFs and the built .xlsx files,
which was never the thing worth protecting. `product_content.py` also sits in
history at commit `8a9f1f1` with the lifespans and the license in it.

**Decided, and it is settled: the repo stays public.** Chad's call, 2026-08-16,
made with the position fully described. Everything through v1.18.0 was pushed
the same day, including the planner, the free calculator and the storm workbook.
Git history is permanent, so this is not a decision that gets unmade by going
private later: the source of all five products is now in a public history.

**Do not re-open this.** A future session that notices the exposure and proposes
Cloudflare Pages or a private repo is re-running an argument that has already
been had and lost on purpose. What changes the answer is evidence, not
reasoning: forks, stars, a scraped listing, or somebody selling the kit back.
Until one of those exists, the position stands. The Cloudflare Pages notes under
"Hosting" in [README.md](README.md) stay useful for the response headers Pages
cannot set, which is a separate reason and still worth doing one day.

Worth naming what was accepted, so nobody has to reconstruct it: a clone plus
one command rebuilds the $12.99 kit, the $39 realtor edition, the $16.99 binder,
the reserve planner and the storm workbook. `build_workbook.py` is the sharpest
case, because a spreadsheet's value is its formulas rather than its prose and
the file carries the whole model. The counterweight is that the shop's
constraint is traffic: zero stars, zero forks, nobody arriving, and the site
does not link to the repo.

**The trigger to revisit is traffic. Chad's call, 2026-08-21.** If the site
starts getting real visitors, the move is off GitHub Pages to hosting that
supports a private repository, which means Cloudflare Pages. See "Hosting" in
[README.md](README.md), and note that Pages can also set real response headers,
which GitHub cannot, so the move is worth something on its own terms.

That is a better trigger than the one it replaces. The old wording waited for
forks, stars, a scraped listing or somebody reselling the kit, all of which are
evidence that the damage has already happened. Traffic is the leading indicator:
nobody goes looking for the repository behind a site nobody has heard of, so
exposure and audience arrive together.

**Also public, and it is a different category: `Marketing Plan.md`**, committed
2026-08-21. Product source is one thing; that file is competitive strategy. It
names competitors and their prices, the pricing rationale, the channel plan, the
seasonal timing, and the realtor association to approach. Chad was told before
choosing to leave it, and left it on the same reasoning: nobody is arriving yet.
It moves with everything else when the traffic trigger fires.

**3. Both Etsy descriptions need one line re-pasted.** "What to have to hand" is
British and was corrected to "on hand" in
[product/etsy-listing.md](product/etsy-listing.md) and
[product/etsy-listing-realtor.md](product/etsy-listing-realtor.md). The files
are right; the live listings still say the old thing until the description is
pasted in again.

**4. The kit PDFs need rebuilding and re-uploading.** Two wording fixes are
waiting in `kit_sections.py`, both corrected in the source and neither one live
on the listing yet. It had "Check the skirting and any flood vents are intact",
which wants a "that" in American usage. It also had "hot-dip galvanised" in the
on-the-water section, a Britishism found on 2026-08-15 while writing the binder
and fixed the same day. Rebuild with `build_printables.py` then
`build_fillable.py`, and replace the files on the listing. Low urgency
individually, but that is now two, so fold them into the next kit upload rather
than letting a third accumulate.

**4b. The binder PDFs need rebuilding and re-uploading, and this one is not
cosmetic. Chad has seen this and is doing it later, as of 2026-08-16, so raise
it once and do not nag.** It is the only known defect in a product people are
currently paying for, so it should lead the next handful of Etsy admin rather
than waiting for a reason of its own. Two strings in `binder_pages.py` were corrupted into control
characters by an apostrophe pass at some point before the binder shipped, and
they are in the live $16.99 PDF on the listing: the damage log page read "use
the insure[garbage] words" and the contractor vetting page "the state licensing
boar[garbage] website". Both are fixed in the source as of 1.18.0 and reworded
rather than re-apostrophed, because the file carries no apostrophes anywhere
else in 682 lines. Rebuild with `python build_storm_binder.py --fillable` and
replace both files on the listing. Found while wiring the workbook to the
binder's own text, which is the argument for importing rather than retyping.

**5. How the site gets measured. Decided 2026-08-21, and it is Google
Analytics.** Property `G-KB3D46WDYK`, on the home page, the calendar contents
page and the free calculator, shipped in 1.19.0.

**The old rule here said any analytics must be cookieless and consent-free,
because the zero-tracker profile was an asset worth protecting. That rule is
gone, and it was Chad's call to spend it.** He is right about the trade: the
asset was only ever worth something to visitors who noticed it, and the shop
could not tell whether it had any visitors at all. A future session that
proposes replacing this with Plausible, Fathom or a cookieless setup on privacy
grounds is re-running an argument that has already been had. What changes the
answer is a complaint, a legal requirement, or the data turning out to be
useless, not a preference.

Two boundaries that came with the decision and are not preferences:

- **The calculator sends the visit, never the answer.** The page tells visitors
  nothing they type leaves their machine. No build year, system name or
  computed figure may be attached to an event. The note is in the head of
  `build_calculator.py`.
- **The CSP names Google and nothing else.** A second tool means adding its
  origins deliberately. That is the feature: a tracker pasted in without a
  decision does not run.

`docs/privacy.html` describes what is collected and is part of the same
release as any change to what is collected, because the page promises it says
so before anything watches visitors.

Still worth doing, in order: confirm data is arriving, then instrument the two
events enhanced measurement does not already cover. Outbound clicks are
automatic, so the Etsy click is handled; feed subscribe and signup submit are
not. Etsy's own traffic-source report and MailerLite's signup count remain the
cross-check, and are the only source for anything that happens off the site.

**6. Small repository hygiene.** Issues and the Wiki are enabled on a public
repo that is not an open source project, so anyone can publish text under the
brand's GitHub presence. The description reads "Home maintenance Calendar" and
the homepage field is empty. All three are settings-page work, and all three
stop mattering if the repo goes private.

**7. The gifting line in the kit's FAQ is still an open decision.**
[product/etsy-listing.md](product/etsy-listing.md) answers "Can I give this to
my clients?" with "A printed copy as a closing or housewarming gift, gladly."
That is written permission for a single copy of exactly what the $39 edition
sells. It may well be the right call, since it keeps a warm pre-sale question
warm and the upsell follows immediately. It was flagged rather than changed:
published permissions are hard to take back, and this one is Chad's call. Do
not improvise a stance on gifting in a customer reply either. Answer the
question actually asked, and if someone asks outright, ask Chad.

**Unverified:**

1. **Android link interception.** A friend was going to test and never reported
   back. Android can hand a `calendar.google.com` link to the Google Calendar
   app, which cannot subscribe. It depends on a per-device setting, so it hits
   some visitors and not others. The site shows an Android-only card with the
   fallback route. If interception turns out to be rare, that card is noise on
   every Android visit and should be cut down. Apple's `webcal://` handoff is
   confirmed working on real hardware.

**Next products, in order:**

**The storm season binder is built.** It came off this list on 2026-08-15 and
now has its own entry under Outstanding above, where the remaining work is the
Etsy listing rather than the product.

**The reserve planner is built.** It came off this list on 2026-08-16 and has
its own entry under Outstanding above. It landed considerably larger than the
$9.99 sketch here, which is why the price is an open question rather than a
settled one.

**The free calculator is built.** It came off this list on 2026-08-16 and has
its own entry under Outstanding above. What is left on it is placement, not
build.

1. **A bundle.** Lifts order value with no new content, and everything it needs
   now exists. There are two of them and they are not the same offer.
   **Binder plus workbook is the one to do first**: the spec names it *The Gulf
   Coast Storm Season System*, the two products were designed against each other,
   and it has a September 10 deadline. Kit plus planner is the calm January
   pairing and can wait for the new year.

2. **Curated how-to videos.** `GUIDES` in `build_calendars.py` is empty and the
   plumbing is done. Adding entries puts links on the guides page and into the
   calendar events. **Adding the first one requires a `SEQUENCE` bump**, since
   it changes what subscribers see. `check_links.py` finds dead ones.

3. **Regional editions.** Chad's own plan, explicitly later. The content is Gulf
   South regional rather than coastal-only, so a Texas or Florida edition is a
   retiming and a relabeling, not a rewrite. **The planner is already built for
   this**: `REGIONS` in `planner_data.py` carries a cost factor and a lifespan
   factor for seven regions, and the workbook applies them itself, so the
   planner half of a regional edition is a dropdown rather than a build.

The planner, the free calculator and the bundle came out of a product
brainstorm on 2026-08-14 and lived only
in that session's transcript until 2026-08-15, which is how the binder went
missing for a day of its own selling season. **Product ideas worth building go
in this list, not in a chat.**
