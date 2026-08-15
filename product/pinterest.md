# Pinterest

Etsy is the checkout. Pinterest is how anyone finds out the thing exists.

The market data says why. The maintenance search terms are dead (`home
maintenance checklist printable` draws 47 searches a month) and the big gift
terms are unwinnable for a new shop. Volume is the binding constraint, so
discovery has to come from somewhere that is not Etsy search. Pinterest is the
one channel where a printable, a checklist and a seasonal home task are all
native content rather than an ad wearing a costume.

Pins are built by `python build_pins.py`, six of them, into `product/pins/`.
Every pin shows a page that is genuinely in the kit.

---

## Setup, in order

Steps 1 through 3 have to be done in a browser, on the Pinterest site. There is
no way around that and no API shortcut worth the trouble.

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

Settings, then **Claimed accounts**, then **Claim** next to Websites. Choose the
**Add HTML tag** option. Pinterest gives back one line that looks like this:

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

Five, in this order. A board is a search target of its own, so the name matters
more than it looks like it should. Give each one the description below, because
Pinterest indexes board descriptions.

| Board | Description |
|---|---|
| **Gulf Coast Home Maintenance** | Seasonal home maintenance for the Gulf Coast, Texas to Florida. What to do and when, in a climate that runs on its own schedule. |
| **Hurricane Season Prep** | Getting a house ready before June, and through to November. Shutters, drainage, insurance timing, and the jobs that have to happen early. |
| **Home Maintenance by Month** | A month by month home maintenance schedule. Twelve months of tasks, sorted by what actually has to happen and what can wait. |
| **New Homeowner Checklists** | First year in a new house. Shutoffs, breaker boxes, appliance lifespans, and the maintenance nobody hands you at closing. |
| **Realtor Closing Gifts** | Closing gift ideas for real estate agents. Branded, useful, and the kind a client keeps rather than regifts. |

### 4. Upload the six pins

`python build_pins.py`, then upload each from `product/pins/`. Copy is below,
one block per file. Fill in **Title**, **Description**, **Alt text**,
**Destination link**, **Board**.

Space them out. Six pins uploaded in one sitting is a worse start than one pin
a day for six days, because Pinterest reads a burst from a brand new account as
a spam signal. One a day, then repin the good ones to a second relevant board a
week later.

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

Titles run to 100 characters and descriptions to 800, but the description is
cut off around 50 characters in the feed, so the first sentence carries it. The
rest is there to be indexed.

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
