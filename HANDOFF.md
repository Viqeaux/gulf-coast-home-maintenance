# Handoff

Everything a fresh session needs to pick this up. Read this first, then
[README.md](README.md) for how the build works and [CHANGELOG.md](CHANGELOG.md)
for why things are the way they are.

Current version **v1.10.0**. Everything below is live unless marked otherwise.

---

## The three products

| | What | Where | Price |
|---|---|---|---|
| **The calendar** | Three subscribe-able `.ics` feeds, one per tier, plus the site and the calendar contents page that hand them out | <https://gulfcoasthomemaintenance.com> | Free, and stays free |
| **The kit** | Every printable page, 27 of them, in two PDFs: print and fillable | Etsy only | $12.99 |
| **The agent edition** | The same 27 pages branded for a realtor, plus a 4 page leave-behind. Four PDFs, print and fillable of each | Etsy only | $39 |

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
python build_pins.py            # six Pinterest pins, 1000x1500
python build_brand.py           # shop icon and banner
python check_links.py           # finds curated videos that have died
python optimize_images.py       # after replacing docs/img/hero.png
```

Content lives in three files: `build_calendars.py` holds the 36 tasks and the
`GUIDES` video table, which are the free half; `task_steps.py` holds the
step-by-step detail and `kit_sections.py` the seven conditional sections, both
of which are **kit only and must not reach the site**.

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

## Outstanding

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

**Pinterest is launched.** Done 2026-08-15: the account, the boards, the pins
uploaded, and the domain claim, whose `p:domain_verify` tag is live in the head
of `docs/index.html`. `build_pins.py` makes the six pins and
[product/pinterest.md](product/pinterest.md) holds the boards, the copy for
every pin, and the setup steps. Re-run the script and re-upload if a pin's
source page changes.

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

**2. The public repo still rebuilds both paid products.** `build_printables.py`
holds `WATCH_LIST` and `FIRST_MONTH`, `kit_sections.py` the seven conditional
sections, `task_steps.py` all thirty-six step-by-steps. A clone plus
`python build_printables.py` is the $12.99 kit; `build_agent_edition.py` is the
$39 one. `.gitignore` protects the built PDF, which was never the thing worth
protecting. `product_content.py` also sits in history at commit `8a9f1f1` with
the lifespans and the license in it.

Nobody is doing this today: zero stars, zero forks, and the site does not link
to the repo. It is also permanent and it grows with every bit of marketing that
works. **The recommended fix is to move the site to Cloudflare Pages**, which
is free, supports private repositories, and can set real response headers,
which GitHub Pages cannot. DNS is already on Cloudflare. See
"Hosting" in [README.md](README.md). GitHub Pro at about $4 a month and a
private repo is the smaller-change alternative. Doing nothing is defensible;
doing nothing without deciding is not.

**3. Both Etsy descriptions need one line re-pasted.** "What to have to hand" is
British and was corrected to "on hand" in
[product/etsy-listing.md](product/etsy-listing.md) and
[product/etsy-listing-realtor.md](product/etsy-listing-realtor.md). The files
are right; the live listings still say the old thing until the description is
pasted in again.

**4. The kit PDFs need rebuilding and re-uploading.** `kit_sections.py` had
"Check the skirting and any flood vents are intact", which wants a "that" in
American usage. Rebuild with `build_printables.py` then `build_fillable.py`,
and replace the files on the listing. Low urgency, worth folding into the next
time the kit changes for another reason.

**5. Decide how Pinterest gets measured, before it launches.** There is no
analytics of any kind, so there is no way to tell whether the pins did anything.
The zero-tracker profile is a real asset and the privacy page now says so out
loud, so anything added should be cookieless and consent-free, and should
instrument three events only: Etsy click, feed subscribe, signup submit. If the
answer is "add nothing", the fallback is Etsy's own traffic-source report plus
MailerLite signup counts. Either is fine. Deciding after the launch is not.

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

1. **The storm season binder, $16.99. In progress, started 2026-08-15.** A third
   paid product, not kit pages. It is bought in a different moment than the kit:
   the kit is a calm purchase, this one is bought with a cone on the TV.

   Contents as scoped: home inventory sheets by room, a policy and account
   numbers page, a what-to-photograph-before checklist, a water and supply
   calculator by household size, an evacuation and shutdown sequence, a
   post-storm damage log, a claim call log with adjuster names and dates, and a
   contractor vetting sheet.

   **The code is nearly free and the content is the whole job.**
   `build_printables.py` already renders HTML to PDF and `build_fillable.py`
   already stamps AcroForm fields, which the inventory and claim log pages need
   anyway. Writing the content at the depth of `task_steps.py` is the schedule
   risk, not the engineering. Keep it out of the public repo the same way the
   kit is: gitignored under `product/`.

   **It has a clock the other products do not.** Peak of Atlantic hurricane
   season is around September 10. That is why this outranks the reserve planner
   below, which was originally ranked first on the grounds that its data already
   existed. The planner sells the same in November; this does not.

2. **The reserve planner, $9.99.** The calculator idea, and the cheapest build
   left. `WATCH_LIST` in `build_printables.py` already holds 17 components with
   Gulf-Coast-shortened lifespans. The buyer enters an install year per item and
   gets years remaining, a projected replacement year, a sorted what-breaks-next
   list, and an annualized set-aside summed into one number. That last line is
   the pitch. Ship as `.xlsx` plus a Sheets copy link plus a one-page quick
   start, built by a `build_planner.py` reading the same constant.

   **Do not hardcode replacement dollar amounts.** They go stale and vary by
   market, and a wrong number in a sold product is a support problem. Offer a
   plainly-marked typical range, and let the buyer's own figure drive the math.

3. **A free calculator on the site.** Once the planner math exists, the same
   numbers render as a web page: enter four ages, see what is on borrowed time.
   The visitor gets a real answer and meets the buy button warm. Feeds the
   signup form already on `docs/index.html`.

4. **A bundle at $29.99.** Kit plus planner plus binder. Lifts order value with
   no new content. Worth doing once any two of the three exist.

5. **Curated how-to videos.** `GUIDES` in `build_calendars.py` is empty and the
   plumbing is done. Adding entries puts links on the guides page and into the
   calendar events. **Adding the first one requires a `SEQUENCE` bump**, since
   it changes what subscribers see. `check_links.py` finds dead ones.

6. **Regional editions.** Chad's own plan, explicitly later. The content is Gulf
   South regional rather than coastal-only, so a Texas or Florida edition is a
   retiming and a relabeling, not a rewrite.

Items 1 through 4 came out of a product brainstorm on 2026-08-14 and lived only
in that session's transcript until 2026-08-15, which is how the binder went
missing for a day of its own selling season. **Product ideas worth building go
in this list, not in a chat.**
