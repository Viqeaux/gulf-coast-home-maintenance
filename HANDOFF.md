# Handoff

Everything a fresh session needs to pick this up. Read this first, then
[README.md](README.md) for how the build works and [CHANGELOG.md](CHANGELOG.md)
for why things are the way they are.

Current version **v1.5.3**. Everything below is live unless marked otherwise.

---

## The two products

| | What | Where | Price |
|---|---|---|---|
| **The calendar** | Three subscribe-able `.ics` feeds, one per tier, plus the site and how-to guides that hand them out | <https://gulfcoasthomemaintenance.com> | Free, and stays free |
| **The kit** | Every printable page, 27 of them, in two PDFs: print and fillable | Etsy only | $12.99 |

The words matter and were confused once already. **"Calendar" means the feeds.
"Kit" means the printables.** A previous session built the printable as a free
download, which is the opposite arrangement, and unwinding that touched the buy
slot, the section labels, the README and the listing copy.

**Owner:** Chad. Bought his first house at forty-five, built the list for
himself before it was a product. That origin is in the Etsy About section and is
the strongest thing in the listing. Do not embellish it.

## Live things

- **Site:** <https://gulfcoasthomemaintenance.com> (GitHub Pages, custom domain,
  HTTPS enforced). The old `viqeaux.github.io/gulf-coast-home-maintenance`
  redirects, so anything already pointing there still works.
- **Repo:** <https://github.com/Viqeaux/gulf-coast-home-maintenance>, **public**.
- **Etsy shop:** GulfCoastHomeCare
- **Etsy listing:** <https://www.etsy.com/listing/4555777332/new-homeowner-gift-undated-gulf-coast>
- **Email:** MailerLite, group still named "Complete edition waitlist", double
  opt-in on. That waitlist is retired, since the kit is now buyable and the site
  shows a buy button in its place. See the first outstanding item: it is being
  repurposed as a general "hear about new tools" signup.

## Build

```bash
python build_calendars.py       # feeds + guides page, into docs/
python build_printables.py      # the kit PDF, into product/
python build_fillable.py        # the fillable twin, needs the PDF above first
python build_listing_images.py  # nine Etsy photos from the real pages
python build_video.py           # the 14 second Etsy listing video
python build_brand.py           # shop icon and banner
python check_links.py           # finds curated videos that have died
python optimize_images.py       # after replacing docs/img/hero.png
```

Content lives in three files: `build_calendars.py` holds the 36 tasks and the
`GUIDES` video table, `task_steps.py` holds the step-by-step detail, and
`kit_sections.py` holds the seven kit-only conditional sections.

**`docs/index.html` is hand-written. Everything in `docs/guides/` and
`product/` is generated.** Edit the Python, not the output.

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

**Four version markers, and they must agree:** `VERSION` in
`build_calendars.py`, the footer of `docs/index.html`, an entry in
`CHANGELOG.md`, and an annotated git tag. Rebuild after changing `VERSION`, or
the guides page keeps reporting the old one.

**`SEQUENCE` is not the version.** It lives in `build_calendars.py` and is what
tells a calendar client an event actually changed. Bump it only when task
content changes. It is at **1** because every event gained a guide link. A
design or infrastructure release does not need it.

**Cut versions without being asked**, when a coherent piece of work lands and is
verified. Not every commit, and not a half-finished feature.

**Verify the feeds are byte-identical** after any change that should not affect
subscribers. Hash them against the previous tag. It has caught real mistakes.

## Gotchas that cost time

**GitHub Pages silently misses build triggers.** Twice now the commit landed but
no deployment was created. The tell: `raw.githubusercontent.com` shows the new
content while the site shows the old. Check
`api.github.com/repos/Viqeaux/gulf-coast-home-maintenance/deployments` for the
latest sha rather than waiting longer. Fix is an empty commit.

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
off-centre". And `min-width` does nothing on an inline element, which an anchor
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

## Outstanding

**The listing is done.** Files, title, description, tags, category, price,
photos, video, shop icon and banner are all live and current. The description
matches [product/etsy-listing.md](product/etsy-listing.md), including the
personal-use licence that deliberately withholds bulk client printing and
redirects agents to message about the coming edition.

**Site:**

1. **A "future releases" signup.** The waitlist is retired: it existed to
   collect interest while there was nothing to buy, and the buy button replaced
   it when the kit listed. Chad wants a general signup in its place, for people
   who want to hear about new tools. The pieces are mostly there. The MailerLite
   form still posts correctly and its markup is still in `docs/index.html`, but
   it only renders when `SHOP_URL` is empty, so it needs lifting out of the buy
   slot into its own place, probably near the free calendars where the
   already-interested reader is. The MailerLite group is still named "Complete
   edition waitlist" and should be renamed to match.

**Unverified:**

2. **Android link interception.** A friend was going to test and never reported
   back. Android can hand a `calendar.google.com` link to the Google Calendar
   app, which cannot subscribe. It depends on a per-device setting, so it hits
   some visitors and not others. The site shows an Android-only card with the
   fallback route. If interception turns out to be rare, that card is noise on
   every Android visit and should be cut down. Apple's `webcal://` handoff is
   confirmed working on real hardware.

**Next products, in order:**

3. **The realtor edition.** The best opportunity in the data: 9,400 searches
   against 31k listings, twenty times the ratio of anything else. Agents are
   local by definition, so the regional angle helps rather than limits, and they
   buy in bulk and repeatedly. The kit's licence already points agents here, so
   there may be messages waiting. **One decision is blocking the build:** manual
   personalisation via Etsy's personalisation field, which justifies $39 to $59
   but needs a rebuild per order, versus a blank "Compliments of ___" line that
   scales with no work per sale. Chad will decide, and has not yet.
4. **Curated how-to videos.** `GUIDES` in `build_calendars.py` is empty and the
   plumbing is done. Adding entries puts links on the guides page and into the
   calendar events. **Adding the first one requires a `SEQUENCE` bump**, since
   it changes what subscribers see. `check_links.py` finds dead ones.
5. **Regional editions.** Chad's own plan, explicitly later. The content is Gulf
   South regional rather than coastal-only, so a Texas or Florida edition is a
   retiming and a relabelling, not a rewrite.
