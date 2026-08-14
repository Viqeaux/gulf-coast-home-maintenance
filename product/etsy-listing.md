# Etsy listing, the free printable calendar

Everything to paste into a new listing on **etsy.com/shop/GulfCoastHomeCare**.
Nothing here is generated; edit it freely. What is generated is what it points
at, run `python build_pdf.py` and the file and images appear in `product/`.

This is the free download, and it is the first thing in the shop. Its job is to
be found, to be worth having, and to make the paid kit an easy second purchase
later. Etsy field limits are noted where they bite.

---

## Listing type

**Digital · instant download.** Answer *yes* to "Is this a digital file?" during
setup. There is no shipping profile and no physical variant.

## Files to upload

| File | Notes |
|---|---|
| `product/Gulf-Coast-Home-Maintenance-Calendar.pdf` | ~85 KB, well under Etsy's 20 MB per-file cap |

One file, not a zip. A zip makes someone on a phone do work before they can see
what they downloaded.

## Photos, in this order

Etsy crops the search-grid thumbnail to 4:3, which slices the title off a
portrait page. `00-hero.png` is composed at 4:3 for exactly that reason and has
to stay first.

1. `00-hero.png`, the 4:3 cover composition
2. `01-cover.png`
3. `03-watch-list.png`, the page people keep; put it early
4. `02-january.png`. Shows what a month actually looks like
5. `06-may.png`. The hurricane month, the reason the thing exists
6. `04-how-to-find-out.png`
7. `07-the-year.png`, the seasons diagram
8. `08-first-month.png`
9. `05-phone-calendars.png`. The free calendars, last, as a bonus

## Title

*140 characters max. This is 133.*

```
Gulf Coast Home Maintenance Calendar, Printable Undated PDF, Hurricane Season Checklist, New Homeowner Gift, Coastal Home Care
```

## Description

Etsy shows roughly the first 160 characters in search results, so the first two
lines carry the whole pitch.

```
Generic home maintenance advice assumes a climate you don't live in. This one is built for the Gulf Coast. Salt air, humidity, termites, and a hurricane season that runs half the year.

Twelve months of what to do and when, in the order the coast actually asks for it. Undated, so it never expires and never goes on sale in January. Print it once and hang it on the same nail forever.

WHAT YOU GET
• A 20-page PDF, sized for US Letter (8.5 x 11)
• Twelve month pages, three tasks each, at three levels of care
• The Big Ticket Watch List. 17 things in your house that are on a clock, with lifespans adjusted for the coast, and room to fill in the year yours went in
• How To Find Out. How to date a water heater, an A/C unit, a roof, or an appliance in about five minutes each
• Your First Month. Ten one-time jobs every new homeowner should do before anything goes wrong
• The Gulf Coast Year. A one-page diagram of hurricane, heat, termite and freeze season, and why May, not June, is the real insurance deadline
• Three subscribe-able calendars for your phone, so the reminders find you

THREE LEVELS, SO IT IS NOT OVERWHELMING
MUST DO. Safety, or skipping it costs you thousands. If you do nothing else, do these twelve things.
SHOULD DO. Protects your home's value and makes what you own last longer.
GOING ABOVE. For the homeowner who wants to stay ahead of everything.
Start with Must Do. Nobody does all of this the first year.

WHY IT IS DIFFERENT DOWN HERE
A flood policy generally takes 30 days to take effect, which is why hurricane prep sits in May and not June. Termites swarm every spring and the damage is almost never covered by homeowners insurance. An A/C that runs nine months a year is doing double the work it was rated against. The lifespans in this calendar are shorter than the national numbers you will find online, because salt air, humidity and UV make them shorter.

WHO IT IS FOR
First-time buyers, anyone who just moved to the coast, and anyone who has owned a coastal house long enough to be tired of finding out the hard way. Texas to Florida. It also makes a genuinely useful closing gift, agents, print a stack.

INSTANT DOWNLOAD
Your file is available the moment checkout completes, nothing is mailed. Print at home on plain letter paper, or take the file to any print shop. Print it black and white if you like; the levels are labelled as well as coloured.

If anything is wrong with your download, message me and I will fix it, and the fix reaches everyone, not just you.

Follow the shop. A full Gulf Coast home care kit is in the works, and this calendar is the spine of it.

General maintenance guidance, not a substitute for a licensed inspector, contractor, or your insurance policy terms.
```

## Tags

*13 tags, 20 characters each, max.*

```
home maintenance
printable calendar
gulf coast
hurricane prep
new homeowner gift
undated calendar
house checklist
home care planner
coastal living
first time home buy
home binder
seasonal checklist
realtor closing gift
```

## Category and attributes

- **Category:** Paper & Party Supplies → Paper → Calendars & Planners
- **Type:** Digital download
- **Holiday / occasion:** Housewarming
- **Renewal:** Automatic

## Price

**Set it as low as Etsy will let you.** Etsy has no $0 price, the floor is
**$0.20**, and each listing costs $0.20 to publish and $0.20 again every four
months when it renews. So the calendar is free in every sense that matters and
costs pennies a year to keep up. If Etsy ever offers a true $0 digital listing,
take it.

Why a free listing is the right first move rather than a wasted one:

- **It is how the shop gets found.** Etsy ranks on engagement, views,
  favourites, orders. A free download collects all three far faster than a
  paid one, and that ranking is what the kit inherits when it lists.
- **Reviews.** A shop with no reviews converts badly. Free downloads review
  well and often, and those reviews sit on the shop, not just the listing.
- **It qualifies the audience.** Everyone who downloads it owns a house on the
  Gulf Coast and cares enough to plan. That is precisely who the kit is for.

The one thing to keep an eye on: a free listing that ships a file pointing at
your own site is fine while the site sells nothing, but Etsy's fee-avoidance
policy forbids using a listing to route buyers somewhere else to *purchase*.
Once the kit is for sale on the site as well as on Etsy, revisit the FAQ line
that names the domain.

## Frequently asked questions

**Will this work outside the Gulf Coast?**
Some of it. The structure works anywhere, but the timing, the lifespans, and
half the tasks are specific to salt air, humidity, and hurricane season. If you
are inland or north, most of the value is in the Watch List.

**Is it dated?**
No, deliberately. There is no year and no weekday grid, so the same printout
works every year. Each task has a box and a line for the date you did it.

**Do I need special paper or a colour printer?**
No. Plain US Letter paper, and black and white loses only the level colours,
which are labelled anyway.

**What are the phone calendars?**
Three subscribe-able calendars, one per level, that put the same twelve
months into Google, Apple, or Outlook, repeating every year. The last page of
the PDF shows you where to get them. They are free as well.

**Can I give this to my clients?**
Yes, and please do. Print a stack for closings. The only ask is that you send
people the link rather than the file, so they get the current version.

---

## After it is published

1. Copy the **listing** URL, `https://www.etsy.com/listing/<id>/<slug>`, not
   the shop URL. People should land on the download, not on a shop front they
   have to search.
2. Paste it into `SHOP_URL` at the bottom of `docs/index.html`. That replaces
   the waitlist with a download button, which is the whole point of the
   waitlist having existed.
3. Email the waitlist. They asked to be told once, and this is the once, and
   the email is now good news rather than an invoice.
4. Rebuild, commit, and cut a version. A live download path is visitor-facing.
5. Point the waitlist form at the kit instead, so it keeps collecting against
   the thing that will actually be for sale.
