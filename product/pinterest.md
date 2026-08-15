# Pinterest

Etsy is the checkout. Pinterest is how anyone finds out the thing exists.

The market data says why. The maintenance search terms are dead (`home
maintenance checklist printable` draws 47 searches a month) and the big gift
terms are unwinnable for a new shop. Volume is the binding constraint, so
discovery has to come from somewhere that is not Etsy search. Pinterest is the
one channel where a printable, a checklist and a seasonal home task are all
native content rather than an ad wearing a costume.

Pins are built by `python build_pins.py`, eight of them, into `product/pins/`.
Every pin shows a page that is genuinely in the product it sells: six from the
kit, two from the storm season binder.

---

## Setup, in order

Every step here happens in a browser, on the Pinterest site. There is no way
around that and no API shortcut worth the trouble. What the repo supplies is
the images and the copy to paste.

### 1. Create a **business** account

<https://www.pinterest.com/business/create/>

Business, not personal, and not a personal account converted later if it can be
helped. Business is free and is the only kind that gets analytics, claimed
websites, and Rich Pins. Use the shop's identity, not a personal one:

- **Name:** Gulf Coast Home Maintenance
- **Website:** `https://gulfcoasthomemaintenance.com`
- **Description:** A home maintenance calendar built for the Gulf Coast. Heat,
  humidity, termites, and hurricane season, month by month, Texas to Florida.

Skip the ads onboarding. It will push hard for a campaign. There is no reason to
spend money before there is anything to measure.

### 2. Claim the domain

Settings, then **Link to Pinterest**, then **Claim** next to Websites. The help
articles and every guide written before about 2025 call that menu "Claimed
accounts", which is what it used to be. Same place, renamed.

Choose the **Add HTML tag** option. Pinterest gives back one line that looks
like this:

```html
<meta name="p:domain_verify" content="a1b2c3d4e5f6...">
```

**Paste that line into the chat and it goes into `docs/index.html` and gets
deployed.** Then come back and press Verify. Do not upload the HTML file option
instead: it works, but it puts a stray file in `docs/` that nothing else reads
and that no future session will understand.

Claiming matters for two reasons. Every pin that links to the domain then
carries the shop name and avatar, including pins other people reshare. And
claimed-domain traffic is the only traffic that shows up in analytics as coming
from the site rather than from nowhere.

Pages already carry the Open Graph tags Rich Pins need, added the same day this
file was written. After the claim goes through, run the site through
<https://developers.pinterest.com/tools/url-debugger/> once to confirm.

### 3. Make the boards

Six, in this order. A board is a search target of its own, so the name matters
more than it looks like it should. Give each one the description below, because
Pinterest indexes board descriptions.

**This table is the spec, not a record of the account.** Names have already
drifted once: what is called "Hurricane Season Prep" here is live as "Hurricane
Prep Checklist". Check the account rather than trusting this list.

| Board | Description |
|---|---|
| **Gulf Coast Home Maintenance** | Seasonal home maintenance for the Gulf Coast, Texas to Florida. What to do and when, in a climate that runs on its own schedule. |
| **Hurricane Season Prep** | Getting a house ready before June, and through to November. Shutters, drainage, insurance timing, and the jobs that have to happen early. |
| **Home Maintenance by Month** | A month by month home maintenance schedule. Twelve months of tasks, sorted by what actually has to happen and what can wait. |
| **New Homeowner Checklists** | First year in a new house. Shutoffs, breaker boxes, appliance lifespans, and the maintenance nobody hands you at closing. |
| **Realtor Closing Gifts** | Closing gift ideas for real estate agents. Branded, useful, and the kind a client keeps rather than regifts. |
| **Home Inventory and Insurance** | What to write down before you need it. Room by room home inventory, policy numbers and deductibles in dollars, and what an adjuster actually asks for. |

### 4. Upload the pins

`python build_pins.py`, then upload each from `product/pins/`. Copy is below,
one block per file. Fill in **Title**, **Description**, **Alt text**,
**Destination link**, **Board**.

Space them out. Six pins uploaded in one sitting is a worse start than one pin
a day for six days, because Pinterest reads a burst from a brand new account as
a spam signal. One a day, then repin the good ones to a second relevant board a
week later.

**The one exception is `07-storm-countdown`, which should go up first and
immediately.** It is the only pin with a deadline. Peak Atlantic season is
around September 10, the binder's whole listing strategy is built on being live
before the demand rather than during it, and a pin needs weeks to gather saves
before it can ride a spike. Every day it waits is a day off the front of that
run-up.

### 5. The profile cover

`python build_brand.py` makes two, beside the Etsy icon and banner:

| File | |
|---|---|
| `pinterest-cover-photo.png` | **Use this one.** The site's hero photograph under the site's own scrim, so a visitor arriving from a pin recognizes the same place |
| `pinterest-cover.png` | The flat version, deep ground and the house mark. Kept as the fallback if the photograph ever changes |

Both are 1600 x 900. The spec is 16:9 at a minimum of 800 x 450, and 1600 is
double that so it stays sharp on a retina screen. Anything quoting 1200 x 600
is out of date, Pinterest crops a 2:1 image top and bottom now.

Neither repeats the shop name. Pinterest already prints the profile name in
large type beside the cover, so a second copy of it would spend the whole image
saying what is said above it. Both keep their content centered and well inside
the edges, because Pinterest narrows the crop on phones.

---

## Product tags, and when to use one

Separate field from the destination link, and it does not replace it. A product
tag hangs an Etsy listing off the pin while the pin itself still lands on the
claimed domain, so the attribution and the email capture both survive and a
ready-to-buy viewer gets a direct route.

**Use one on the five product pins only:**

| Pin | Product tag |
|---|---|
| `04-first-month` | the kit listing |
| `05-watch-list` | the kit listing |
| `06-realtor` | the realtor listing |
| `07-storm-countdown` | the binder listing |
| `08-home-inventory` | the binder listing |

**Not on `01-free-calendar`, `02-hurricane-season` or `03-summer-heat`.** Those
three promise something free, and that promise is the entire reason they get
saved. Hanging a price tag off them argues against the headline.

Leave the **affiliate link or sponsored product** toggle off. It is for
disclosing compensation from someone else's product. This is your own listing,
so there is nothing to disclose, and switching it on puts a paid-promotion label
on a pin that is not one.

Nothing here conflicts with Etsy's fee-avoidance policy, which forbids using a
listing to route buyers away from Etsy. This routes the other direction.

---

## Why every pin links to the site and not to Etsy

Etsy is one click further on, and the site is the only page that can do all
three jobs: hand over the free calendars, capture an email, and sell both
products. A pin that lands on Etsy has nothing to offer a person who is not
buying today, which is nearly all of them.

It is also the only link Pinterest will attribute. `etsy.com` cannot be claimed
by this shop, so an Etsy pin is anonymous, while a pin to a claimed domain
carries the shop name wherever it travels.

---

## Pin copy

Titles run to 100 characters, of which Pinterest says the **first 40 are the
ones most likely to be shown**. Descriptions run to 500. All eight below are
inside both, and every title still reads at 40.

### Topic tags: pick from the list below, do not go hunting

Up to ten per pin, from a fixed vocabulary. Free text does not stick, and
neither does anything invented for this niche. **Home maintenance barely exists
in Pinterest's taxonomy.** Searching `home`, `hurricane`, `weather`, `summer`,
`cleaning` and `moving` across three pins produced the eleven tags below and
almost nothing else, so treat that as the ceiling rather than a starting point.

Pinterest says outright that viewers never see these, so they are an
algorithmic hint and nothing else. Take what fits from the table, add anything
new you happen to spot, and do not spend more than a few seconds per pin. One
relevant tag is a fine result. Padding with the wrong ones argues for the wrong
audience.

The real keyword work is the title, the description, the board name and the
board description. Those are the fields Pinterest's own guidance ranks, and
they are already written.

### Known to exist

A pool, not an assignment. Any of these can go on any pin it actually fits.

**Home and DIY:** Home Care, Home Organization Tips, Home Buying, Home
Improvement Projects, Home Hacks, DIY Gifts

**Real estate and gifting:** Real Estate Marketing, Real Estate Buying, Real
Estate Selling, Housewarming Gifts

The first group covers the four calendar and kit pins. The second is for
`06-realtor`, where Housewarming Gifts and DIY Gifts are the two worth having:
they reach past the real estate audience into browse categories this shop
cannot win on Etsy.

**Hashtags: no.** Pinterest's own guidance ranks the title, the description,
the board title and the board description, and hashtags appear nowhere in it.
The advice to stuff ten or fifteen of them comes almost entirely from sites
selling hashtag generators. Keywords belong in the description as sentences,
which is how the copy below is written.

### 01-free-calendar.png

- **Board:** Gulf Coast Home Maintenance
- **Link:** `https://gulfcoasthomemaintenance.com/`
- **Title:** The Gulf Coast Home Maintenance Calendar, free for your phone
- **Description:** Most home maintenance advice is written for a climate you do
  not live in. This one is built for the Gulf Coast: heat, humidity, termites,
  and hurricane season, from Texas to Florida. Twelve months of tasks in three
  tiers, so you can do the must-do list and leave the rest. The calendar is a
  free subscription that drops the tasks straight into the calendar app on your
  phone, and it updates itself.
- **Alt text:** A chart of the four Gulf Coast seasons, hurricane, heat and
  humidity, termite swarm, and freeze risk, laid out across twelve months.

### 02-hurricane-season.png

- **Board:** Hurricane Season Prep
- **Link:** `https://gulfcoasthomemaintenance.com/#calendars`
- **Title:** Hurricane season home prep, month by month
- **Description:** Hurricane season opens June 1 and the work that matters
  happens before it. A flood policy generally takes 30 days to take effect,
  which is why the prep sits in May on this calendar and not in June. Here is
  what to do to a Gulf Coast house each month of the season, from clearing the
  A/C condensate line to checking the attic ventilation. Free calendar
  subscription, Texas to Florida.
- **Alt text:** The June page of a home maintenance calendar, listing must-do,
  should-do, and going-above tasks with step by step instructions.

### 03-summer-heat.png

- **Board:** Home Maintenance by Month
- **Link:** `https://gulfcoasthomemaintenance.com/#calendars`
- **Title:** Summer home maintenance for a hot, humid climate
- **Description:** On the Gulf Coast the hard season is summer, not winter.
  Fourteen of the thirty-six tasks on this calendar exist because of heat and
  humidity: condensate lines, condenser coils, attic ventilation, exterior
  caulk, and the mildew that follows all of it. August is the month most of it
  comes due. Free monthly calendar you can subscribe to on your phone.
- **Alt text:** The August page of a Gulf Coast home maintenance calendar with
  tasks sorted into three tiers.

### 04-first-month.png

- **Board:** New Homeowner Checklists
- **Link:** `https://gulfcoasthomemaintenance.com/#edition`
- **Title:** First month in a new house: the checklist nobody hands you
- **Description:** Ten one-time jobs for a new house, in the order they should
  happen. Find and tag the main water shutoff and the gas shutoff, label every
  breaker in the panel, locate the septic lid or sewer cleanout, write down
  every air filter size, and photograph every room before anything happens to
  it. They never repeat, which is exactly why they get forgotten. Part of a
  27 page Gulf Coast home maintenance kit.
- **Alt text:** A printable first month checklist for a new house, ten items
  with checkboxes.

### 05-watch-list.png

- **Board:** New Homeowner Checklists
- **Link:** `https://gulfcoasthomemaintenance.com/#edition`
- **Title:** How long does a water heater last? The Big Ticket Watch List
- **Description:** Everything expensive in your house is already on a clock. A
  tank water heater runs 8 to 10 years, an A/C condenser 10 to 12, asphalt
  shingles 12 to 15, exterior caulk 2 to 4. These are adjusted down for the Gulf
  Coast, where salt air, humidity and hard UV wear a house faster than national
  averages assume. Write down the year each one went in, add the lifespan, and
  you know what to start saving for instead of finding out the hard way.
- **Alt text:** A printable table of home components with typical Gulf Coast
  lifespans and a column to write in the year installed.

### 06-realtor.png

- **Board:** Realtor Closing Gifts
- **Link:** `https://gulfcoasthomemaintenance.com/#agents`
- **Title:** A closing gift your clients actually keep
- **Description:** A 27 page Gulf Coast home maintenance kit branded with your
  name, brokerage, phone and license number on every page, plus a four page
  leave-behind for the closing table. Your clients keep it on the fridge and see
  your name every time they check what month it is. Print it as many times as
  you like for as many clients as you like. Undated, so it never expires.
- **Alt text:** The cover of the Gulf Coast Home Maintenance Calendar, a
  printable kit for real estate agents to brand and give to clients.

---

## After the first six

Do not add more pins until the first six have numbers on them. Two weeks is
enough to see which board and which promise people save, and that answer should
pick the next batch rather than a guess.

The cheapest expansion is one pin per month page. Twelve months, twelve pins,
each targeting "what to do to your house in March" and its eleven siblings.
`build_pins.py` already renders any page in the kit by heading, so a new pin is
a new entry in `PINS` and nothing else.

### 07-storm-countdown.png

- **Board:** Hurricane Season Prep
- **Link:** `https://gulfcoasthomemaintenance.com/#binder`
- **Product tag:** the binder listing
- **Title:** Hurricane prep checklist, in the order it happens
- **Description:** Almost nobody fails because they did not know to buy water.
  They fail because they bought it on the wrong day. Hurricane prep written as a
  sequence: what to do five to seven days out while it is still a disturbance,
  what changes at 72 hours, and what is already too late by 24. Refill
  prescriptions early, get cash in small bills, fill every vehicle before the
  queues. From a 33 page printable storm season binder for the Gulf Coast.
- **Alt text:** A printable hurricane countdown checklist, tasks grouped under
  five to seven days out and 72 hours, each with a checkbox.

### 08-home-inventory.png

- **Board:** Home Inventory and Insurance
- **Link:** `https://gulfcoasthomemaintenance.com/#binder`
- **Product tag:** the binder listing
- **Title:** Home inventory for insurance, before you need it
- **Description:** Contents coverage is usually 50 to 70 percent of what the
  house itself is insured for, a six figure number on most policies. To collect
  it you have to say what you owned, and the adjuster will not help you
  remember. People settle for a fraction of their limit because listing four
  hundred items from memory, three weeks after losing them, is impossible. Do
  one room at a time and start with the expensive things. Nine room by room
  sheets in a printable binder.
- **Alt text:** A printable home inventory page showing item, make and model,
  serial number, year and replacement cost, with a worked example.
