# Etsy listing: the realtor edition

Everything to paste into a second listing on **etsy.com/shop/GulfCoastHomeCare**.

Nothing here is generated, so edit it freely. What it points at *is* generated:
run `python build_agent_edition.py` and all four files appear in `product/`.

**This is the second paid product at $39.** The first is the personal kit at
$12.99 ([etsy-listing.md](etsy-listing.md)), and the free product is the three
calendar feeds on gulfcoasthomemaintenance.com. Etsy field limits are noted
where they bite.

Why this exists: `realtor closing gift` draws 9,400 searches a month against
31.3k listings, a ratio of 1:3.3. Every other term in the market data is
somewhere between 1:21 and 1:711. It is the best opening the shop has.

---

## What makes it worth 3x the kit, and what does not

Worth reading before editing any of the copy below, because two earlier
theories were wrong and the listing is written against the third.

**Not the license.** It cannot be enforced on a PDF, and the median solo agent
will never once wonder whether printing twenty copies is allowed. A license
alone is a listing that invites the buyer to go and purchase the $12.99 one.

**Not the branding on its own.** A name typed on a cover is the only visible
difference between two listings sitting side by side, and one line of text
cannot carry a $26 gap.

**It is that the $12.99 kit does not fit the job.** It is 27 pages. An agent
closing twenty deals prints 540 sheets and collates them twenty times. Copying
the file does not solve that, which is why the four page leave-behind is the
actual product here: 80 sheets across twenty clients. The branding and the
license are what make it *theirs*, but the short edition is what makes it
usable.

## Listing type

**Digital, instant download.** Answer *yes* to "Is this a digital file?" during
setup. There is no shipping profile and no physical variant.

**No custom options and no variations.** The listing form stays empty of
anything that collects buyer input. Branding is arranged by message after the
sale, which keeps the download genuinely instant. See "Why no custom options"
below.

## Files to upload

Four, in this order. Etsy allows five, and all four are under the 20 MB cap.

| File | |
|---|---|
| `product/gulf-coast-agent-edition-fillable.pdf` | ~1.2 MB, all 27 pages, type your details and save |
| `product/gulf-coast-agent-edition.pdf` | ~399 KB, all 27 pages, the print version |
| `product/gulf-coast-agent-leave-behind-fillable.pdf` | ~200 KB, 4 pages, fillable |
| `product/gulf-coast-agent-leave-behind.pdf` | ~106 KB, 4 pages, print |

The full 27 page kit goes first. Etsy lists files in upload order and most
buyers open the first one, and the first thing someone who just paid $39 should
meet is the substantial document, not the short one. The leave-behind follows as
what it is: the version built for handing over twenty times.

Build them with no arguments, so every detail arrives as an empty form field:

```bash
python build_agent_edition.py
```

## Title

*140 characters max, 14 words or fewer, no repeated words. This is 97 and 13.*

```
Realtor Closing Gift: Branded Gulf Coast Home Maintenance Calendar for Clients, Undated Printable
```

Search results truncate around 60 characters, so what most people see is
`Realtor Closing Gift: Branded Gulf Coast Home Maintenance Cal...`. The exact
search term lands first, and "Branded" is the word that separates this from the
personal listing before anyone has to read further.

## Description

Etsy shows only the first few lines before "expand", so the opening two
paragraphs carry the whole pitch and have to stand alone.

```
The trouble with most closing gifts is that they get used once. A candle burns down, a bottle gets opened, and the card goes in a drawer. Six months later there is nothing in that house with your name on it.

This one goes on the fridge. It is a home maintenance calendar built specifically for Gulf Coast houses, Texas to Florida, branded with your name and brokerage on every single page, and licensed for you to print for every client you close.

WHAT YOU GET

Four files. Two documents, each in a print version and a type-and-save version.

1. THE FULL KIT, 27 pages, branded throughout. Twelve months of tasks, three a month at three levels of effort, each with step by step instructions, what to have to hand, and where people go wrong. The Big Ticket Watch List, seventeen things in a house that are already on a clock, with lifespans adjusted for salt air, humidity and UV. How To Find Out, for dating a water heater or a roof in five minutes. Your First Month. The Gulf Coast Year. And seven extra sections for whatever the house happens to have: septic, well water, pool, generator, raised or pier foundations, storm shutters, and waterfront.

2. THE LEAVE-BEHIND, four pages, drawn from the same kit. Because handing over 27 pages twenty times is 540 sheets, and nobody does that twice. This is the version you print in a stack and give out at the table: the Gulf Coast Year diagram, Your First Month, and the Big Ticket Watch List, behind your own cover. Four sheets a client. Give this one out, and email the full 27 to anyone who wants the rest.

YOUR NAME ON EVERY PAGE

Open the fillable version, type your name, brokerage, phone and license number once, and save. It is on the cover and in the footer of every page from then on. No account, no subscription, no design software, and nothing to order.

Would you rather I set it up for you, or want your brokerage logo on there as well? Message me after you buy with your details and your logo file, and I will build your copies and send them back, usually within a day. There is no extra charge and no personalization fee. Your download still arrives the moment you check out, so you have a usable file in hand either way and you are never waiting on me to get started.

ABOUT LOGO FILES

If you send a logo, a few things matter. Send a PNG or SVG on a transparent or white background, at least 1000 pixels wide, or a vector file if your brokerage has one. A logo sitting on a dark block will print a solid band of ink on every page, which is the one thing this kit is built to avoid.

Your logo is placed exactly as you send it. I do not redraw it, retouch it, sharpen it, or scale it up. A small, blurry, or very detailed file will print looking small, blurry, or cluttered, and that is not something I can fix from the file itself. If you are not sure yours will hold up, ask your brokerage for the print or vector version. That is usually the one you want.

HOW YOU MAY USE IT

This is a client gifting license. Print as many copies as you like, for as many clients as you close, for as long as you are licensed. Hand them out at closing, at open houses, at client appreciation events, or mail them.

Please do not resell the files, share them as files, or list them anywhere. If another agent wants a copy, send them this listing.

WHY GULF COAST, AND WHY THAT HELPS YOU

A flood policy generally takes 30 days to take effect, which is why hurricane prep sits in May and not June. Termites swarm every spring and the damage is almost never covered by homeowners insurance. An A/C running nine months a year is doing roughly double the work it was rated for. Exterior caulk fails in 2 to 4 years on this coast while a roof lasts 12 to 15.

Every lifespan in here runs shorter than the national numbers, on purpose. A generic checklist tells your client nothing they could not have found in ten seconds. This one tells them something true about the house they just bought, which is the difference between a gift and a leaflet.

THE PART THAT KEEPS WORKING

The same twelve months exist as three free subscribe-able calendars that drop into Google, Apple or Outlook and repeat every year. The leave-behind points your client at them.

That is the piece worth paying attention to. A printed sheet gets filed away by March. A subscribed calendar puts a reminder on your client's phone every month, for as long as they own the house, and it got there because of you.

THE DETAILS

US Letter, 8.5 x 11 inches, portrait. Interior pages are white on purpose, so printing a stack does not cost you a cartridge, and every level is labeled as well as colored, so black and white loses nothing. Undated, so it never expires and there is no reprint next January.

Both open in any PDF reader, with no special software or fonts to install.

One honest note on the fillable versions: typing and saving works in Adobe Reader and most desktop PDF apps. Some phone apps will let you type but cannot save what you typed, so set yours up on a computer.

Instant download the moment checkout completes. Nothing is mailed.

If anything is wrong with your download, message me and I will fix it, and the fix reaches everyone rather than just you.

General maintenance guidance, not a substitute for a licensed inspector, contractor, or your insurance policy terms. You are responsible for meeting your own state and brokerage advertising rules.
```

## The logo service

**This is the only part with work per order, and it is deliberately kept off
the critical path.**

Text branding is self-serve: `build_fillable.py` stamps AcroForm fields over
the blank lines, so the buyer types their details once and saves. A logo cannot
work that way, because AcroForm has no image field an ordinary reader will
populate. A logo has to be baked in at build time.

So the logo is offered as a **free service after purchase**, not as a delivery
requirement. The buyer downloads a usable file in thirty seconds, and only the
ones who actually want a logo create any work.

**Etsy Messages is the whole channel.** No custom option field, no upload box,
nothing on the listing form that collects anything. Etsy cannot attach a
customized file to an instant download, so any field promising branding at
checkout would be writing a cheque the delivery cannot cash. Keeping the form
empty means the download is exactly what it says, and the branding is a service
offered inside the description rather than a step in the purchase.

When the details arrive:

```bash
python build_agent_edition.py --agent "Dana Whitfield" \
  --brokerage "Bayou Oak Realty Group" --phone "(228) 555-0147" \
  --license "MS-B-22841" --logo bayou-oak.png
```

Then send the four files back through Etsy Messages. Call it four minutes.

Ask for **PNG or SVG on a transparent or white background**. A logo sitting on
a dark block prints an ink slab on all 27 pages, which is the one thing this kit
is built not to do. Wide brokerage lockups are normal and fine: the footer mark
is capped at 13pt tall and the cover mark at 32pt, and both are set to
`contain`, so nothing distorts.

Check it in grayscale before sending. Plenty of agents print black and white,
and a mid-tone color logo can go to mud.

## Tags

*13 tags, 20 characters each, max.*

```
realtor closing gift
closing gift
agent closing gift
buyer closing gift
real estate agent
realtor marketing
client gift
new homeowner gift
gulf coast
home maintenance
hurricane prep
housewarming gift
branded printable
```

Four variants of the closing gift term, because that is the 9,400 search
opportunity and Etsy matches phrasing rather than meaning. Two aim at the agent
rather than the gift (`real estate agent`, `realtor marketing`), which is how
an agent shopping for their own supplies finds it. The rest describe what it is.

Deliberately absent: `closing gift for clients`. 215 searches a month and
flagged very low conversion, and `client gift` plus the title covers it.

## Materials

*13 max, 45 characters each.*

```
Printable PDF
Fillable PDF with form fields
US Letter 8.5 x 11 inches
Instant digital download
Undated, never expires
27 page kit
4 page client leave-behind
Client gifting license
Realtor closing gift
Gulf Coast regional content
Works in any PDF reader
Free logo setup included
No physical item is shipped
```

Materials carry far less search weight than tags, so nothing here is a term
worth winning. They are doing two other jobs: repeating the facts a skimmer
needs (fillable, Letter, undated, instant) where Etsy surfaces them as a tidy
list, and stating the two things that pre-empt a bad review, that no object is
posted and that the logo setup costs nothing extra.

## Item options

**About this listing**

- **Who made it:** I did
- **What is it:** A finished product
- **When did you make it:** 2020 to 2026

Not *Made to order*, even though the logo service exists. Made to order changes
what Etsy promises the buyer about delivery, and the download really is finished
and instant. The logo is a service performed after the sale, not the item.

**Settings**

- **Category:** Paper & Party Supplies, Paper, Calendars & Planners
- **Type:** Digital download
- **Holiday / occasion:** Housewarming
- **Renewal:** Automatic
- **Quantity:** Digital listings do not take one, Etsy sells them unlimited
- **Custom options:** none. See below.
- **Variations:** unavailable. Etsy blocks them on digital items outright.
- **SKU:** `GCHM-AGENT-01` if you want one. Etsy does not require it, and a
  second product is the point at which they start being worth keeping.

No shipping profile, no production partners, no returns policy field. Etsy does
not offer returns on digital items.

## Why no custom options

Etsy offers up to five input fields on a digital listing, of three kinds: a text
box, a list of options, and a file upload. Leave all of them off.

The pull is obvious, especially the file upload: the logo could ride in attached
to the order instead of arriving by message. It is not worth what it costs.

**A field in front of every buyer changes who asks.** The fillable PDF exists so
nobody has to wait on anyone. Put a branding box at checkout and buyers who would
happily have typed their own details in decide they would rather you did, and
that is per-order work that grows with every sale.

**A list of options adds a way to fail.** Somebody picks "yes please, brand it"
and leaves the details blank, and now the order is stuck waiting on a message
anyway, except this time the buyer thinks the job is already underway.

**The description already carries the offer.** An agent reading far enough to
care about branding reaches it. One channel, Etsy Messages, handles the logo,
the details and anything that needs redoing, and that is one place to look rather
than three fields plus an inbox.

What this leaves is a plain instant download that is genuinely instant, with a
free service offered inside it. Nothing on the listing form promises the buyer
anything that depends on you being awake.

**Variations are not a fallback here.** Etsy blocks them on digital items
outright, and the listing form says so where they would otherwise appear.

## Price

**$39.**

Etsy takes roughly $0.20 to list, 6.5% of the sale, and about 3% plus $0.25 to
process payment, so $39 nets about $34.85. One agent sale is worth roughly
three kit sales.

Why not $19.99: the buyer is a business, spending out of a marketing budget
against a commission, and pricing a professional tool like a consumer printable
reads as a reason to doubt it. Why not $59: nothing here is per-order work, so
there is no cost to recover, and $59 invites a comparison with the $12.99
listing that the buyer wins.

A $6,000 year needs about 172 sales at $39. At $12.99 it needs 531.

Worth considering: list at $49 and open with a launch sale to $39. Etsy shows a
strikethrough and a discount badge, which helps conversion, and ending the sale
later leaves you at your real price without having to justify a rise.

## Photos

Etsy crops the search-grid thumbnail to **4:3**, which slices the title off a
portrait page. Compose the first image at 4:3 rather than screenshotting a page.

Put **YOUR NAME ON EVERY PAGE** on that first image, over a cover showing a
filled-in Compliments Of block. Shoppers scan images before they read titles,
and "branded" is the thing this listing has to prove fastest.

Build them, then upload in numbered order:

```bash
python build_agent_listing.py
```

| | | |
|---|---|---|
| `00-hero.png` | 4:3 | The branded cover, "Your name on every page" |
| `01-cover.png` | page | That cover on its own |
| `02-footer.png` | 4:3 | The footer at twice actual size, on a real month page |
| `03-self-serve.png` | 4:3 | Blank cover next to filled cover, "fully customized" |
| `04-watch-list.png` | page | The Big Ticket Watch List |
| `05-the-year.png` | page | The Gulf Coast Year diagram |
| `06-first-month.png` | page | Your First Month |
| `07-full-kit.png` | page | A month page, so the 27 are not taken on trust |
| `08-license.png` | page | The client gifting license, stated plainly |

Two of these exist only for this listing and are worth understanding.

**`02-footer`** is the one that answers the buyer's real doubt. "Branded" usually
means a name on a cover, and an agent has seen that before. Showing the footer
enlarged, on an interior page, is the only way to prove it runs throughout.

**`03-self-serve`** kills the objection that costs the sale: that this is a
made-to-order item they will wait on. Blank download on the left, filled cover
on the right.

The sample brand deliberately reads "Your Name" and "Your Brokerage" rather than
an invented agent at an invented firm. It documents itself, and it cannot
collide with a real brokerage. The placeholder logo is generated as an SVG
inside `build_agent_listing.py`, so no binary asset enters the repo.

## Featured video

`product/listing-realtor/video.mp4`, built by:

```bash
python build_video.py --agent
```

Fourteen seconds, silent, square, inside Etsy's 15 second cap. It shares every
frame and encoding decision with the kit's video and differs only in what it
argues, because the buyer here is not the person who reads the thing. It opens
on the name landing on the cover, establishes that the branding runs on all 27
pages, and closes on the license.

Run `build_agent_listing.py` first. The video is assembled from those images.

## Frequently asked questions

**Do I have to order a new file every time I get a new client?**
No. Type your details in once, save the file, and print it as often as you like
for as long as you are licensed. There is nothing to reorder and no per-client
fee.

**Can I put my brokerage logo on it?**
Yes, and it is included. Message me your logo after you buy, PNG or SVG on a
transparent or white background and at least 1000 pixels wide, and I will build
your copies and send them back, usually within a day. Your logo is placed
exactly as you send it, so send the best version your brokerage has.

**Do I have to set it up myself?**
No, that is your choice. Message me your details and I will do it at no extra
charge. Or open the fillable version and type them in yourself in about a
minute. Either way your download arrives the moment you check out, so you are
never waiting on me to have something usable.

**Is my brokerage name on it? My compliance officer will ask.**
There is a dedicated brokerage line and a license number line on the cover, and
your name runs in the footer of every page. Advertising rules vary by state and
by brokerage, so check the result against yours before you print a stack.

**How many clients can I print for?**
As many as you close. That is what separates this from the $12.99 personal
listing, which is licensed for one household.

**Will this work outside the Gulf Coast?**
Some of it. The structure works anywhere, but the timing, the lifespans and
about half the tasks are specific to long humid summers, termite pressure and
hurricane season. Texas to Florida is where it is exactly right. Further north,
the Watch List is where the value is.

**Is it dated?**
No, deliberately. There is no year and no weekday grid, so the same printout
works every year and you are not reprinting every January.

**Do I need a color printer?**
No. Plain US Letter paper, and black and white loses only the level colors,
which are labeled anyway. Interior pages are white so a stack does not empty a
cartridge.

**What are the free calendars it mentions?**
Three subscribe-able calendars, one per level, that put the same twelve months
into Google, Apple or Outlook and repeat every year, free at
gulfcoasthomemaintenance.com. The leave-behind points your client at them,
which is how the gift keeps working after the paper gets filed.

---

## After it is published

1. Copy the **listing** URL, `https://www.etsy.com/listing/<id>/<slug>`.
2. Update [etsy-listing.md](etsy-listing.md) in two places, and the live kit
   listing to match. Both currently say an agent edition is *coming* and to
   message about it, which stops being true the moment this goes live:
   - the `HOW YOU MAY USE IT` paragraph in the description
   - the **Can I give this to my clients?** FAQ answer
3. Answer anyone who already messaged about the agent edition. The kit listing
   has been inviting that since it went up, so check the inbox before promoting
   anything.
4. Rebuild, commit, and cut a version.
