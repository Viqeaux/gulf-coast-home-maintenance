# Site audit — gulfcoasthomemaintenance.com

Audited 22 August 2026 against the live site and the working tree at `main`
(`5bc3858`). The brief said 14 pages at v1.32.2; the deployed site is
**v1.33.0** and carries **16 HTML pages** (plus the Search Console
verification file). All 16 were audited. `privacy.html` and `404.html` were
judged against their intended austerity and are not criticised for it.

**Screenshots could not be captured.** The Browser pane in this session never
composited frames, so `computer{action:"screenshot"}` timed out on every
attempt. Every Pass 3 finding below is therefore measured from the live DOM
instead of eyeballed — computed colours, contrast ratios, element geometry,
scroll positions, and viewport overflow at 390 × 844 and 1440 × 900. Where a
finding would normally cite a screenshot it cites the measurement and the
command that produced it. Nothing in Pass 3 is asserted from the source alone.

Two files are **generated**, so fixes to them belong in the Python, not the
HTML:

| Deployed file | Generator |
|---|---|
| `docs/calculator/index.html`, `docs/calc-widget.js` | `build_calculator.py` |
| `docs/guides/index.html`, `docs/month-tasks.js`, the `.ics` feeds | `build_calendars.py` |

---

## Status

**Eight findings were fixed and shipped in v1.33.1 on 2026-08-22**, the batch
that needed no design decisions. Each is marked `FIXED 1.33.1` in place below,
and the fix was verified against a local server rather than only written:

`C1` scroll-behavior · `C4` FAQ schema · `H10` product images ·
`M1` scroll-padding · `M4` aria-current · `M8` shim routing ·
`M9` floir.gov · `M11` unclosed div

Everything else stands. The ranked order for what comes next is in
`HANDOFF.md` under "The full-site audit, 2026-08-22"; the short version is
contrast tokens first, then one footer and one mobile menu built as page
assembly in Python rather than sixteen hand edits.

**Chad's calls, 2026-08-22.** *Loans:* nothing dealing with loans anywhere on
the site, which resolves the scope question flagged under H11 — the site was
already clean, so nothing had to be removed. *FAQ:* delete the markup now,
write a real FAQ section later and bring the markup back alongside it.

---

## Critical

### C1. Every on-load `#fragment` link into a `site.css` page silently fails to scroll  ·  FIXED 1.33.1

**Where:** [site.css:15](docs/site.css:15) — `html { scroll-behavior: smooth; }`

`scroll-behavior: smooth` on the root makes Chrome animate the browser's
initial fragment scroll. On these five pages that animation never completes,
and the reader is left at the top of the document with the hash still in the
address bar.

Measured on clean loads in a fresh tab, 2.5–3.2 s settle time:

| URL | root `scroll-behavior` | final `scrollY` | target's distance down the page | result |
|---|---|---|---|---|
| `/shop/#edition` | smooth | **0** (stable over 3.2 s) | 1,283 px | **fails** |
| `/shop/#binder` | smooth | **0** | 2,766 px | **fails** |
| `/#who` | smooth | **0** | 4,723 px | **fails** |
| `/calendars/#calendars` | smooth | **0** | 372 px | **fails** |
| `/calculator/#adjust` | auto | 566 | — | works |
| `/guides/#oct-flush-water-heater` | auto | correct | — | works |

The two pages that work are the two that do not load `site.css`. Same
harness, same navigation, same lazy-loaded images — the only variable is the
property. Clicking an in-page anchor after load still works (the animation
completes in ~1–2 s); it is specifically the navigation-time fragment that
dies.

**Why it matters.** This breaks, in order of cost:

- **The Pinterest shim's entire reason for existing.** [index.html:83-89](docs/index.html:83) redirects `/#edition`, `/#binder`, `/#agents` and `/#calendars` to their new homes. Its own comment says a pin "that lands on a page with no matching anchor just dumps the reader at the top with no idea what they were promised." That is exactly what happens today: the shim redirects correctly to `shop/#binder`, and then the destination refuses to scroll.
- **The purchase path.** The three "View details" buttons on the homepage ([index.html:621, 631, 641](docs/index.html:621)), the three on the shop page itself ([shop/index.html:193, 205, 217](docs/shop/index.html:193)), the "The storm season binder" row on all seven resource pages, and the shop column in every full footer all target `/shop/#edition|#binder|#agents`. A reader clicking "The agent edition" lands 5,000 px above the agent edition, on a 9.6-screen page, with no indication anything went wrong.
- **"Who made this"**, the trust link in every full footer, never reaches the bio.

**Fix:** delete `scroll-behavior: smooth` from [site.css:15](docs/site.css:15).
Nothing on the site depends on animated scrolling, and the
`prefers-reduced-motion` override at [site.css:25](docs/site.css:25) already
concedes the point. If the animation is wanted for in-page clicks, scope it to
`@media (prefers-reduced-motion: no-preference)` on a container rather than the
root, and verify each of the six URLs above lands on its target after reload.
Do this before anything else in this document: it is one deleted line and it is
currently costing conversions on live traffic.

---

### C2. There is no navigation on a phone

**Where:** [nav.css:55](docs/nav.css:55) — `@media (max-width: 52rem) { .nav-links { display: none; } }`

Below 832 px the six top-level links and both dropdown menus are removed and
nothing replaces them. There is no menu button, no drawer, no `<details>`
fallback.

Measured at 390 × 844 on `/resources/louisiana-fortify-homes/`, every link
visible in the top bar:

```
["Gulf Coast Home Maintenance", "Get the free calendar"]
```

That is the whole bar: a wordmark and one gold button. The comment at
[nav.css:45-47](docs/nav.css:45) says the links "drop out, leaving the one gold
button, because a bar with nothing actionable on a phone would be a dead
strip." The button is actionable. The problem is that it is the *only* thing
actionable, and it points at the calendar regardless of what the reader came
for.

**Why it matters.** The brief's own premise is that most visitors arrive from
a search engine onto a deep resource page. Those visitors are overwhelmingly on
phones. A Louisiana homeowner who lands on the Fortify Homes page and wants to
know whether the same money exists in Mississippi — because they are moving, or
because their sister asked — has no route to it except the browser back button.
The site's coverage is invisible to the majority of its audience.

**Fix:** add a disclosure menu below 52 rem. The lowest-cost version that needs
no JavaScript is a `<details class="nav-mobile">` in the bar whose `<summary>`
is a hamburger and whose body is the same link list the desktop bar carries,
shown only under `@media (max-width: 52rem)` while `.nav-links` stays hidden.
Give the summary a ≥ 44 px hit area and a `:focus-visible` ring. The markup is
already duplicated verbatim into all 16 pages, so this is one block added to
each — or better, fixed as part of C3 below.

---

### C3. The seven deep resource pages — the primary landing pages — are the only pages with no real footer

**Where:** [resources/louisiana-fortify-homes/index.html:276-289](docs/resources/louisiana-fortify-homes/index.html:276) and the equivalent block in all six siblings.

The site has two footer tiers:

| Tier | Pages | Footer |
|---|---|---|
| Full `foot-grid` | `/`, `/calendars/`, `/shop/`, `/storm/`, `/resources/` | 21 links in four columns |
| Minimal | 7 resource detail pages | 4 links: Etsy, Resources, home, Privacy |
| Minimal | `/guides/`, `/calculator/` | 3–4 links, none to Resources or Storm |

Combine that with C2 and the total site map available to a cold search visitor
on the Louisiana page at 390 px is **nine links**, measured:

- top bar: wordmark → home, "Get the free calendar" → `/calendars/`
- body: "← Resources", `ldi.la.gov`, wind-mitigation ×2, `/shop/#binder`, `/calculator/`
- footer: Etsy, `/resources/`, home, `/privacy.html`

**Named dead ends.** From any resource detail page there is no route to
`/storm/`, `/guides/`, `/shop/` (except the broken `#binder` anchor), or the
other four state grant pages. From `/guides/` and `/calculator/` there is no
route to `/resources/` or `/storm/` at all. From `/calendars/` there is no
route to `/resources/`, `/storm/` or `/calculator/`.

**Why it matters.** These seven pages are where the search traffic lands and
where the site's credibility is earned. They are also where it terminates. A
reader who has just decided this site is trustworthy is given nowhere to spend
that trust.

**Fix:** the `foot-grid` block is already byte-identical across five pages.
Move it into a shared include — or, since these are static files, into a small
`footer.css` plus a copy-paste block — and put it on all 16 pages with the path
prefix adjusted. Keep the resource pages' "spotted something wrong?" line above
it. That one change also solves half of C2, because the footer then carries the
full map on every page even before a mobile menu exists.

---

### C4. The homepage ships FAQ structured data for six questions that appear nowhere on the page  ·  FIXED 1.33.1

**Where:** [index.html:110-186](docs/index.html:110) — the `FAQPage` node in the `@graph`.

Verified against the rendered page:

```
questionsInSchema: 6
"Are the phone calendars really free?"     onPage: false
"Is the kit dated?"                        onPage: false
"Will this work outside the Gulf Coast?"   onPage: false
"Do I need a color printer for the kit?"   onPage: false
"Why is hurricane prep in May rather..."   onPage: false
"Can I give the kit to my clients?"        onPage: false
first answer text present on page:         false
the string "FAQ" anywhere on the page:     false
```

Google's structured data policy requires FAQ content to be "visible to the user
on the source page." Markup that describes content the page does not contain is
the definition of the spammy-structured-markup manual action.

**Why it matters twice.** First, the risk: a manual action would drop the
homepage from search, and the whole site's traffic model assumes search.
Second, the irony: the comment immediately above the block
([index.html:106-109](docs/index.html:106)) explains that `aggregateRating` was
deliberately omitted because inventing one is "the fastest way to lose the one
thing this brand is actually selling, which is being straight with people." The
FAQ block is the same offence in a different field.

The content is also stale. It describes "the three seasonal tiers" (there are
four calendars since the Monthly Rounds shipped) and four of the six questions
are about the printable kit, dating from before the site widened to grants.

**Fix:** two options, and the second is better.
1. Delete lines 122-185 (the `FAQPage` node), leaving the `WebSite` node.
2. Render a real FAQ section on the homepage and rewrite the questions for what
   the site is now — "Which Gulf states pay for a new roof?", "Is the calendar
   really free?", "Do you run any of these grant programs?", "When was this last
   checked?" — then keep the markup in sync with it. This is genuinely useful
   content for the audience and it would give the homepage something it
   currently lacks: plain answers to the questions people type into a search box.

---

### C5. `/storm/` promises four phases of storm content and delivers 274 words and a buy button

**Where:** [storm/index.html](docs/storm/index.html), whole page. Measured `main` word count: **274**.

The `<title>` and description ([storm/index.html:12-13](docs/storm/index.html:12))
promise "before the storm, during, after, and the insurance claim that decides
what gets paid." The page delivers four cards of one sentence each
([storm/index.html:112-137](docs/storm/index.html:112)), then immediately:

- `<h2>Get the complete system in the Storm Season Binder</h2>` ([:144](docs/storm/index.html:144))
- a `$16.99` price block and a direct **"Get the binder on Etsy"** button ([:157-158](docs/storm/index.html:157))
- "See what's inside on the shop page" ([:164](docs/storm/index.html:164))

Of the five links in `main`, two go to the paid binder and the first one is the
Etsy buy button. Three Etsy links are visible on the page.

**Why it matters.** This is the answer to the brief's question about storefront
versus reference, and it is the clearest case on the site. "Storm prep" is one
of the four doors on the homepage and one of six items in the desktop nav. A
homeowner who clicks it during a named-storm week gets four teasers and a
checkout. The page does not tell them one useful thing they could act on today:
not the wind-versus-flood deductible distinction, not what to photograph, not
the claim deadline, not the evacuation-zone lookup. The content exists — the
binder has 33 pages of it, and the flood-insurance resource page proves the
house style can give the substance away and still sell.

**Fix:** give the page the same treatment the resource pages get. Each of the
four cards becomes a real section with the actionable minimum: for *Before*, the
wind and flood deductible arithmetic (a `$400,000` house at 2 % owes `$8,000` —
the site already says this once, buried at
[resources/strengthen-mississippi-homes/index.html:294-298](docs/resources/strengthen-mississippi-homes/index.html:294));
for *After*, photograph before you clean up and log the cause of each item
because wind and flood are different policies; for *Claims*, the notice
deadlines and what a claim log needs. Link out to the state emergency-management
evacuation-zone lookups the way the resource pages link to FEMA. Then keep the
binder offer, once, at the bottom — where it reads as "there is a printed
version of this" rather than "the content is behind this button."

---

## High

### H1. Two palette tokens fail WCAG AA in the light theme, across every page

**Where:** [theme.css:36-37](docs/theme.css:36) — `--accent: #327d82` and `--sand: #a97822`.

Measured ratios:

| Pair | Ratio | Verdict | What it colours |
|---|---|---|---|
| `--accent` on `--bg` `#f5f2e9` | **4.27** | fail (needs 4.5) | every in-body link on a paper section, `.sec-no`, `.hm-more` |
| `--accent` on `--paper-2` `#ede7d8` | **3.88** | fail | links inside `.checked` / tinted boxes |
| `--sand` on `--deep` `#17322c` | **3.53** | fail | hero eyebrow, both `.hero-alt` links, `← Resources`, **every link in every resource-page footer** |
| `--sand` on `--bg` | **3.48** | fail | `.next .label` |
| `--sand` on `--paper` | **3.76** | fail | same |
| `--accent` on `--paper` | 4.62 | marginal pass | |
| `--muted`, `--must`, `--above`, `--on-deep-mute` | 4.84–10.82 | pass | |

The dark palette has no failures at all — measured on the same pages with
`prefers-color-scheme: dark`, zero elements below 4.5. The dark tokens were
lifted; the light ones never were.

Concrete instances measured on `/resources/louisiana-fortify-homes/` at 390 px:

- `← Resources`, the page's primary escape hatch — **3.53** at 11 px / 600
- `ldi.la.gov/fortifyhomes`, the outbound link the whole page exists to deliver — **4.27** at 17 px
- `its own page on this shelf` — **4.27**
- `Related tools` label — **3.76**
- all four footer links — **3.53** at 13.9 px

On the homepage, `Find the roof grant in your state →` and `See what's already
on borrowed time →` ([index.html:173, 176](docs/index.html:173)) are both
**3.53** at 15.2 px / 600. Those two lines are the hero's only routes into the
grants shelf and the calculator.

**Why it matters.** The audience skews toward older homeowners — Florida's
grant priority groups start at "low income, 60 and over," which the site itself
quotes. Under-contrast links at 11–15 px in bright coastal daylight are links
that do not get followed.

**Fix:** darken the light-theme values in [theme.css](docs/theme.css) and add a
separate token for sand-as-text, since sand also has to keep working as a
*surface* (the gold CTA button, where it is the background and passes easily).
Measured candidates:

```css
:root {
  --accent:     #2a6b70;   /* 5.46 on --bg, 5.90 on --paper */
  --sand:       #a97822;   /* unchanged: still the button ground */
  --sand-text:  #8a6112;   /* 4.94 on --bg, 5.34 on --paper */
  --sand-on-deep: #c99230; /* 5.00 on --deep */
}
```

Then point the text uses at the new tokens: `.hero .label`, `.hero-alt a`,
`.season-link`, `header a.back`, `.next .label`, `footer a` on the resource
pages, `.band .deck a`, `.mark .label`. Leave `.topbar a.cta--free`'s background
alone. Re-measure after: the dark block needs no change.

---

### H2. `/calendars/` delivers nothing at all without JavaScript, and says nothing about it

**Where:** [calendars/index.html:126, 136, 140, 144, 154](docs/calendars/index.html:126) — five empty `<div class="actions" data-file="…">` elements, filled by [calendar-buttons.js:141-168](docs/calendar-buttons.js:141).

With scripts off, the free calendar page renders four tier cards and a picker
with **zero buttons and zero links to any `.ics` file**. There is no
`<noscript>`. The `.ics` files are static and reachable — `/gulf-coast-must-do.ics`
returns `200` — so the page is withholding files it does not need to.

The calculator page, by contrast, handles this properly with a `<noscript>`
block ([calculator/index.html:330-339](docs/calculator/index.html:330)) that
explains why and points somewhere useful.

**Why it matters.** The free calendar is the site's stated primary offer and the
target of the one CTA that survives on mobile. Anyone with scripting blocked —
a corporate network, a privacy extension, a slow connection where the script
times out — sees a page describing four calendars and offering none of them,
with no explanation.

**Fix:** put a real `<a href="/gulf-coast-must-do.ics" download>Download .ics</a>`
inside each `.actions` div in the markup, and have `renderActions()` replace it
rather than fill an empty box (it already calls `box.textContent = ''` first, so
this costs nothing). Add a `<noscript>` explaining that Subscribe needs
JavaScript but Download does not.

---

### H3. Four pages have no `<h1>`

**Where:**

| Page | First heading |
|---|---|
| [calendars/index.html:91](docs/calendars/index.html:91) | `<h2>One at a time <span class="free-tag">Free</span></h2>` |
| [shop/index.html:166](docs/shop/index.html:166) | `<h2>Shop</h2>` |
| [storm/index.html:90](docs/storm/index.html:90) | `<h2>Storm season</h2>` |
| [resources/index.html:90](docs/resources/index.html:90) | `<h2>Grants and programs</h2>` |

Confirmed on the live pages — `document.querySelector('h1')` returns `null` on
all four.

**Why it matters.** `/resources/` is the hub for the site's highest-value
content and the destination of the homepage's "Find the roof grant in your
state" link; it has no document title in the heading sense. A screen-reader user
landing there and pressing `1` to jump to the main heading finds nothing.
Search engines lose the strongest on-page signal for a page targeting
"Gulf Coast roof grant."

**Fix:** promote the existing `<h2>` on each page to `<h1>` and demote the
section `<h2>`s below it by one level. On `/resources/` this also fixes H4.
`site.css` already styles `h1` with a `clamp()` that will read correctly in
these positions; check `/calendars/`, where the `.free-tag` span sits inside the
heading.

---

### H4. `/resources/` uses `<h3>` for both the categories and the items inside them

**Where:** [resources/index.html:98](docs/resources/index.html:98) (`<h3 class="res-cat">Roof grant programs, by state</h3>`) and [:105, 113, 122, 130, 138](docs/resources/index.html:105) (`<h3>` inside each `.res-row`), then [:147](docs/resources/index.html:147) (`<h3 class="res-cat">Insurance rules and discounts</h3>`) and [:153, 161](docs/resources/index.html:153).

Rendered heading outline, measured:

```
H2: Grants and programs
H3: Roof grant programs, by state
H3: Mississippi's $10,000 FORTIFIED roof grant
H3: Alabama's $10,000 FORTIFIED roof grant
…
H3: Insurance rules and discounts
H3: The flood insurance 30-day rule
H3: Wind mitigation insurance discounts
```

Nothing in the structure says the second line is a category and the third is a
member of it.

**Why it matters.** This is the page whose whole job is "the topic coverage is
legible without already knowing what's there." Visually the `.res-cat` styling
does the work; structurally it does not, so a screen-reader user browsing by
heading gets a flat list of nine equal siblings and cannot tell that Texas
belongs under "roof grant programs" while flood insurance does not.

**Fix:** with H3 applied, make the two categories `<h2>` and the seven rows
`<h3>`. Add `.res-cat { }` styling under the new selector so the visual weight
is unchanged.

---

### H5. Program facts and dollar figures on the homepage carry no last-checked date

**Where:** [index.html:175-212](docs/index.html:175) — the four grant cards and the Texas line.

The cards assert, undated:

- "Up to $10,000" ×4
- "Wind Pool policyholders in three coastal counties" (Mississippi)
- "awarded by lottery in eligible parishes" (Louisiana)
- "A free wind inspection first, then a matching grant" (Florida)
- "In Texas there is no statewide roof grant"

Every one of those is a fact that changes between legislative sessions and
funding rounds. The detail pages date each of them correctly
(`Checked August 21–22, 2026`), and `/resources/` dates every row
([resources/index.html:70, 79, 87, 95, 103, 118, 126](docs/resources/index.html:70)).
The homepage — the page that sets whether a reader believes the rest — does not.

`/storm/` and `/guides/` carry no date anywhere either, and both make
time-sensitive claims (`/guides/` states the 30-day flood rule at
[guides/index.html:381](docs/guides/index.html:381); `/storm/` states a price
and links a live Etsy listing).

The site's own trust panel promises the opposite:
[index.html:696-699](docs/index.html:696) — *"Dates matter. Time-sensitive
resources show when they were last verified against the source."*

**Why it matters.** Someone who reads "Mississippi: three coastal counties" in
2027 and drives to a county office has been misled by a page that had no way to
warn them. The dates on the detail pages are the product; leaving them off the
front door means the promise is kept only where nobody sees it first.

**Fix:** put a single dated line under the grant row — *"Programs checked
against their own agencies' pages, most recently 22 August 2026. Each page below
carries its own date."* — and make it a build-time value rather than a typed
one so it cannot rot. Add the same line to `/storm/` and `/guides/`. Longer
term, the resource pages need a staleness rule: after N months the `.checked`
stamp should read *"last checked 14 months ago — verify against the agency"*
rather than a bare date that looks equally authoritative at any age. That can be
done with `<time datetime>` plus four lines of JS, or in the build.

---

### H6. Nothing on the site captures the reader at the one moment they want to be told something

**Where:** the MailerLite form exists on exactly three pages —
[index.html:739-762](docs/index.html:739), [guides/index.html:579-604](docs/guides/index.html:579),
[calculator/index.html:505-530](docs/calculator/index.html:505). It is absent
from all seven resource pages, `/resources/`, `/storm/`, `/shop/` and
`/calendars/`.

Meanwhile the resource pages say, in their own words:

- Louisiana: *"lottery registration is closed and additional grant rounds will be announced at a later date… it carries a signup for program announcements: the single most useful click on this subject"* ([:184-187](docs/resources/louisiana-fortify-homes/index.html:184))
- Alabama: *"Registering interest on their site before a round opens is how you avoid learning about a deadline after it has started"* ([:229-231](docs/resources/strengthen-alabama-homes/index.html:229))
- Mississippi: *"If you do not fit today's phase, that is a reason to watch the page, not a final answer"* ([:238-241](docs/resources/strengthen-mississippi-homes/index.html:238))

**Why it matters.** The site correctly refuses to be the authority and sends
people to the agency. But it is uniquely well placed to be the *watcher* — one
person tracking five agencies is a real service, and it is the reason someone
would come back rather than bookmark five `.gov` pages. Right now a reader
arrives at the exact moment of "nothing I can do today," and the page's answer
is a $16.99 binder.

**Fix:** add the signup to every resource page with copy matched to the moment —
*"Rounds open and close without much notice. Leave your email and I'll tell you
when a Gulf Coast program changes status. That is all the list is for."* This is
also a reason to consolidate the handler (M6): three copies is already two too
many, ten would be untenable.

---

### H7. The internal link graph points at the shop and nowhere else

Measured by stripping the top bar and footer from each page and looking only at
links in the body — i.e. what a mobile visitor can actually reach:

| Page | Reaches |
|---|---|
| `/` | calendars, shop, resources, MS, AL, LA, FL, TX |
| `/calendars/` | calendars, guides, shop |
| `/guides/` | guides, calculator, **shop**, privacy |
| `/calculator/` | guides, calculator, **shop**, privacy |
| `/storm/` | storm, **shop**, flood, wind |
| `/shop/` | **shop**, Etsy |
| `/resources/` | **shop**, all 7 resource pages, Etsy |
| `/resources/flood-insurance-30-day-rule/` | **shop**, MS |
| `/resources/louisiana-fortify-homes/` | calculator, **shop**, wind |
| `/resources/my-safe-florida-home/` | calculator, **shop**, wind |
| `/resources/strengthen-alabama-homes/` | calculator, **shop**, MS, wind |
| `/resources/strengthen-mississippi-homes/` | calculator, **shop** |
| `/resources/texas-windstorm-coverage/` | calculator, **shop**, MS, AL, LA, FL, wind |
| `/resources/wind-mitigation-discounts/` | calculator, **shop**, MS, AL, LA, FL, TX |

**`/shop/` is the only destination linked from all 14 content pages.** Nothing
except the homepage's door grid links to `/storm/`. Nothing outside `/calendars/`
and `/` links to `/calendars/` in body copy.

The specific gaps worth fixing, in order of value to a reader:

1. **`/calculator/` → `/resources/`.** The calculator's whole output is "your roof is on borrowed time." Four Gulf states will pay up to $10,000 toward replacing it, and the page never says so. Its "next" section ([calculator/index.html:479-495](docs/calculator/index.html:479)) instead pitches an unreleased spreadsheet and the printable kit. This is the single highest-value missing link on the site.
2. **`/resources/flood-insurance-30-day-rule/` → `/storm/`.** Its own "Worth knowing while you are here" section ([:239-245](docs/resources/flood-insurance-30-day-rule/index.html:239)) is entirely about post-storm damage documentation, and links to the paid binder rather than the free storm page.
3. **`/resources/flood-insurance-30-day-rule/` → `/resources/`.** Its third "related tool" is *"Mississippi's $10,000 roof grant · the other insurance-adjacent program worth knowing on this coast"* ([:256-258](docs/resources/flood-insurance-30-day-rule/index.html:256)). This is the most universally relevant page on the site — every Gulf homeowner in every state — and it hands a Floridian a Mississippi program. It should point at the shelf, or at the state pages as a set.
4. **`/resources/strengthen-mississippi-homes/` → `/resources/wind-mitigation-discounts/`.** Mississippi is the most linked-*to* resource page and the least linked-*from*: it reaches only the shop and the calculator. Every other state page links to wind-mitigation; this one does not, despite its own closing section being about wind deductibles.
5. **The five state pages → each other.** Only Texas and wind-mitigation cross-link the set. A "the other four Gulf states" strip at the foot of each state page costs four links and answers the second question every reader of one of these pages has.
6. **`/guides/` → everything.** See H8.
7. **`/resources/*` → `/calendars/`.** The topbar CTA does this on desktop; on mobile it is the one thing that survives, so it is covered — but the body never makes the argument, and the calendar's May task *is* the flood-insurance deadline.

**Fix:** these are `<a>` tags, not architecture. The `.next` "Related tools" box
already exists on every resource page and is the natural home for most of them.
Rename it — it currently says "Related tools" over a list that is mostly
articles — and make the composition rule explicit: two free things from this
site, then at most one paid one, and the paid one last.

---

### H8. `/guides/` is 16 phone screens long, has no way to jump to a month, and contains exactly one link

Measured at 390 × 844: document height **13,737 px = 16.3 screens**. January's
first task sits at 711 px; December's last sits at **12,405 px**. There is no
table of contents, no month strip, no back-to-top.

`document.querySelectorAll('main a')` returns **one** link, and it points at
`/shop/`.

**Why it matters.** Two audiences hit this page. Subscribers arrive from a
calendar reminder on a deep anchor (`#oct-flush-water-heater`) — that works, and
is a nice piece of design. Search visitors arrive at the top and are asked to
thumb through 15 screens to find November. Meanwhile 1,763 words about
termites, hurricane prep, insurance verification, roof inspection and water
heater life contain not one link to the pages this site has written on exactly
those subjects.

The page also opens with a shop pitch: the first `<h2>` in the document is
*"Looking for how to actually do one?"* ([guides/index.html:935](docs/guides/index.html:935),
generated at [build_calendars.py:934](build_calendars.py:934)), above January.

**Fix**, all in `build_calendars.py`:

- A month jump strip under the `<h1>` — twelve links to `#jan-…`-style month anchors. Give each `<section class="month">` an `id`. Sticky on desktop if it is cheap; a plain wrapped row is enough.
- Contextual links from the task copy, generated from a small table in `TASKS`: `may-insurance-hurricane-prep` → `/resources/flood-insurance-30-day-rule/`; `sep-roof-inspection` and `may-secure-exterior` → `/resources/`; `dec-watch-list` → `/calculator/`; `feb-termite-inspection` → whatever termite page gets written (H10).
- Move the `.kit-pointer` box below January, or turn it into a one-line note. The first heading on a free reference page should not be an upsell.

---

### H9. The seven resource pages have no `og:image` and no `twitter:card`

**Where:** heads of all seven, e.g. [resources/louisiana-fortify-homes/index.html:13-19](docs/resources/louisiana-fortify-homes/index.html:13) — `og:title`, `og:description`, `og:type`, `og:url`, `og:site_name` are present; `og:image`, `og:image:width/height/alt` and `twitter:card` are not. Every other page on the site has all of them.

**Why it matters.** These are the pages that get shared. "Louisiana will pay
$10,000 toward your roof" is a Facebook-group link, and Gulf Coast neighbourhood
and storm groups on Facebook are a real distribution channel. Without an image,
Facebook and Messenger render a bare grey card, which converts far worse and
looks less legitimate than the same link from a local news site.

**Fix:** add the four lines the other pages carry. Better: give this set its own
image rather than reusing the live-oak hero — a plain card with the state name
and "$10,000 FORTIFIED roof grant" would out-perform a photograph, and
`build_site_images.py` already generates card images for the products.

---

### H10. Product structured data uses the hero photograph as the product image  ·  FIXED 1.33.1

**Where:** [shop/index.html:60, 79, 98](docs/shop/index.html:60) — all three `Product` nodes carry
`"image": "https://gulfcoasthomemaintenance.com/img/hero-1600.jpg"`.

That is the live oak and Spanish moss photograph. The actual cover images exist
and are used in the visible markup four lines away:
`img/cover-kit.jpg`, `img/cover-binder.jpg`, `img/cover-agent.jpg` (560 × 725,
verified loading).

**Why it matters.** Where Google renders a product image from this markup —
shopping surfaces, some rich results — it shows a tree instead of the thing for
sale, and the mismatch between structured data and page content is itself a
quality signal.

**Fix:** point each node at its own cover.

---

### H11. Obvious Gulf Coast homeowner questions with no page at all

The shelf answers "who will pay for my roof" thoroughly. These are the questions
a Gulf Coast homeowner asks next, ranked by how often they are searched against
how badly they are answered elsewhere:

1. **How a hurricane / wind deductible actually works.** A percentage of dwelling limit, not a flat dollar figure; separate from the all-peril deductible; and it is why a $400,000 house owes $8,000 before anything pays. The site states this once, in a closing aside on the Mississippi page. It deserves its own page and it is the highest-intent unanswered question on this coast.
2. **What to do when your insurer non-renews or leaves the state.** The defining Gulf Coast homeowner experience of the last several years, and the search results are dominated by lead-generation sites. This page would be the strongest possible demonstration of the site's "no lead selling" promise.
3. **Roof age and insurability.** Carriers refusing to write or renew on roofs past 15–20 years, what an inspection looks for, and how this connects to both the calculator and the grant programs. It is the bridge between the two halves of the site and neither half mentions it.
4. **Filing a hurricane claim: deadlines, adjusters, and the appraisal clause.** Currently 100 % inside the paid binder.
5. **Elevation certificates and Risk Rating 2.0.** Why flood premiums changed and what an elevation certificate is worth. Sits directly beside the existing flood page.
6. **State wind pools as a set.** Texas gets TWIA; MWUA and Citizens are named in passing on other pages with no explanation. One page mapping the five states' insurers-of-last-resort would complete the state grid the shelf already implies.
7. **Homestead exemption.** Both the Louisiana and Florida grant pages make it an eligibility requirement and neither explains what it is or how to get one — for a reader who does not have it, the grant page is a dead end with no next step.
8. **Vetting a contractor after a storm.** Licence lookup by state, the roofing-scam patterns that follow a landfall, and why "sign here and we'll handle your insurance" is the sentence to walk away from.
9. **Termite bonds.** The calendar has an annual termite inspection task; the bond/contract question that follows it is distinctly Gulf and nowhere on the site.
10. **Shutters versus impact windows,** and how each is treated in mitigation credits — the natural follow-on from the wind-mitigation page.

*Scope, resolved 2026-08-22.* The brief listed "loans" among the subjects the
site should cover, which disagreed with the project's recorded position. Chad
settled it the same day: **nothing dealing with loans, anywhere on the site.**
The list above already stands without any — no SBA disaster loans, no mortgage
products — so nothing in it changes. The site itself was checked and was
already clean. Two things a future grep will find and should leave alone: the
word `mortgage` twice on the flood insurance page, which is FEMA's own rule
text for when the 30-day wait is waived, and a "Loan number" blank on a storm
binder record page, which is a printed product rather than site content.

---

## Medium

### M1. Fragment targets land under the sticky bar  ·  FIXED 1.33.1

**Where:** no `scroll-padding-top` anywhere; the top bar is `position: sticky` at [nav.css:21](docs/nav.css:21).

Measured, once C1 is worked around:

| URL | bar bottom | target top | obscured |
|---|---|---|---|
| `/guides/#oct-flush-water-heater` | 56 px | 24 px | **31 px** — the "Should" tier tag |
| `/calculator/#adjust` | 57 px | 0 px | **56 px** — the section heading |

**Why it matters.** The guides anchors are hit twelve times a year by every
subscriber, from a calendar reminder. The thing hidden is the tier tag, which is
the label answering "is this one I actually have to do?"

**Fix:** `html { scroll-padding-top: 4.5rem; }` in [site.css](docs/site.css),
and in the `<style>` blocks of `/guides/`, `/calculator/` and the resource pages
(via `build_calendars.py`, `build_calculator.py`, and the shared resource
stylesheet from M5).

---

### M2. Six meta descriptions and two titles will be truncated in search results

| Page | Title | Description |
|---|---|---|
| `/resources/texas-windstorm-coverage/` | **81 ch** | 193 ch |
| `/resources/strengthen-mississippi-homes/` | **72 ch** | 210 ch |
| `/resources/my-safe-florida-home/` | 63 | **254 ch** |
| `/resources/wind-mitigation-discounts/` | 53 | **240 ch** |
| `/resources/louisiana-fortify-homes/` | 67 | **234 ch** |
| `/resources/flood-insurance-30-day-rule/` | 67 | **222 ch** |
| `/resources/strengthen-alabama-homes/` | 64 | **220 ch** |

Google renders roughly 60 characters of title and 155–160 of description. Every
resource description is 40–100 characters over, so the sentence that ends
*"Verified against the Louisiana Department of Insurance"* — the credibility
line, deliberately placed last — is the part that gets cut.

**Fix:** trim each description to ≤ 155 characters and move the verification
claim to the front, since that is the differentiator against the content farms
these pages compete with. Shorten the Texas title to something like *"Texas
Windstorm Coverage: WPI-8, TWIA, and the Roof Grant That Doesn't Exist"* (69) or
shorter.

---

### M3. Four titles do not match what a Gulf Coast homeowner types into a search box

| Page | Current | Problem |
|---|---|---|
| `/calculator/` | `What in Your House Is on Borrowed Time` | No brand, no location, no searched term. Nobody types this. |
| `/guides/` | `What Is on the Calendar, Gulf Coast Home Maintenance` | "What is on the calendar" is internal vocabulary. |
| `/calendars/` | `The Calendars, Gulf Coast Home Maintenance` | Doesn't say free, doesn't say what it is. |
| `/storm/` | `Storm Season, Gulf Coast Home Maintenance` | Generic against a very competitive query set. |

The seven resource page titles and `/resources/` are, by contrast, well judged
— they lead with the state, the dollar figure and the programme name, which is
exactly what gets typed.

**Fix**, matching real query shapes:

- `/calculator/` → `How Long Do a Roof, A/C and Water Heater Last on the Gulf Coast?` (in `build_calculator.py:200`)
- `/guides/` → `Gulf Coast Home Maintenance Checklist, Month by Month` (in `build_calendars.py:664`)
- `/calendars/` → `Free Gulf Coast Home Maintenance Calendar for Google, Apple and Outlook`
- `/storm/` → `Hurricane Prep for Gulf Coast Homeowners: Before, During, After, and the Claim` — but only once C5 makes the page true.

---

### M4. `aria-current="page"` on a link that goes to a different page, on seven pages  ·  FIXED 1.33.1

**Where:** [resources/louisiana-fortify-homes/index.html:136](docs/resources/louisiana-fortify-homes/index.html:136) and the same line in all six siblings —
`<a href="../" aria-current="page">Resources</a>`.

The link targets `/resources/`. The current page is the Louisiana page. A screen
reader announces "Resources, current page" while the user is somewhere else.

`/calculator/`, `/calendars/`, `/shop/`, `/storm/`, `/resources/` and `/guides/`
all use it correctly (self-referencing links).

**Fix:** on the seven detail pages use `aria-current="true"` — the correct value
for "this is the ancestor of the current page within a set" — or drop the
attribute and mark the current page in the dropdown instead, which would also be
more useful.

---

### M5. Seven copies of a 71-line stylesheet, two of which have already drifted

**Where:** the `<style>` block in each resource page,
e.g. [resources/louisiana-fortify-homes/index.html:33-104](docs/resources/louisiana-fortify-homes/index.html:33).

MD5 of the block, per page:

```
99c213a2   flood-insurance-30-day-rule      71 lines
99c213a2   louisiana-fortify-homes          71 lines
99c213a2   my-safe-florida-home             71 lines
99c213a2   strengthen-alabama-homes         71 lines
99c213a2   texas-windstorm-coverage         71 lines
a5e615b0   strengthen-mississippi-homes     74 lines   ← drifted
0a18d6de   wind-mitigation-discounts        75 lines   ← drifted
```

The drift, diffed:

- `strengthen-mississippi-homes` has an extra `.next p { margin: 0 0 .6rem; font-size: .95rem; }`
- `wind-mitigation-discounts` has an extra `h3 { font: 700 1.02rem/1.3 var(--font-serif); … }`

That second one is the consequence made concrete: `wind-mitigation-discounts` is
the only resource page that uses `<h3>`, so it is the only one carrying an `h3`
rule. The next resource page that adds a subheading gets browser-default Times
bold and nobody finds out until they look.

This is precisely the failure mode `site.css`, `theme.css`, `nav.css` and
`analytics.js` all exist to prevent — their file headers say so in four separate
places, including [nav.css:6-10](docs/nav.css:6): *"the drift trap this project
has already paid for three times."* This is the fourth.

**Fix:** extract to `docs/resources.css`, loaded after `nav.css` on the seven
pages. Fold in the two drifted rules so nothing regresses. It also removes ~500
lines of duplicated bytes from the pages that get the most search traffic.

---

### M6. Three copies of the mailing-list submit handler

**Where:**

- [calendar-buttons.js:31-57](docs/calendar-buttons.js:31) — the shared one, deliberately bound before the `#calendars` guard
- [guides/index.html:626-646](docs/guides/index.html:626) — generated at [build_calendars.py:1030](build_calendars.py:1030)
- [calculator/index.html:740-760](docs/calculator/index.html:740) — generated at [build_calculator.py:825](build_calculator.py:825)

All three implement the same honeypot / hidden-iframe / 2500 ms fallback
contract. The calculator's comment even says *"Same signup contract as the other
two pages."* The shared file is already written to be safe on a page with no
feed section — it returns early after binding the form.

**Fix:** load `../calendar-buttons.js` on `/guides/` and `/calculator/` and
delete both inline copies from the generators. Net: two fewer places for the
honeypot logic to diverge, and one fewer inline `<script>` for the CSP to have
to allow.

---

### M7. Roughly 350 lines of dead CSS, and a comment that misdescribes it

**Where:** [site.css](docs/site.css). Class selectors defined in `site.css` that
appear in no HTML file and in no JS file:

| Block | Lines |
|---|---|
| `.hero--split`, `.hero-copy`, `.hero-photo` (a whole alternate hero) | [1058-1123](docs/site.css:1058) |
| `.res-card`, `.checked-chip` (superseded by `.res-row`) | [992-1025](docs/site.css:992) |
| `.mini-calc`, `.mini-calc-row`, `.mini-calc-note` | [945-963, 1022](docs/site.css:945) |
| `.month-card` and children | [529-542, 1021](docs/site.css:529) |
| `.benefits` | [1218-1236](docs/site.css:1218) |
| `.get-grid`, `.pgrid--sm` | [1348-1363](docs/site.css:1348) |
| `.todo-cols` | [1183-1185](docs/site.css:1183) |
| `.followup`, `.followup-blurb` | [714-724, 1023](docs/site.css:714) |
| `.pcard-more` | [454-459, 479](docs/site.css:454) |
| `.k`, `.k--must/should/above` | [550](docs/site.css:550) |
| `.level--must/should/above/rounds` | [1166+](docs/site.css:1166) |
| `.buy-blurb`, `.stats`, `.now-head` | [607, 206, 941](docs/site.css:607) |
| `.cta--alert`, `.cta--kit` | [109](docs/site.css:109) (referenced in a comment) |

Separately, the comment at [site.css:106-110](docs/site.css:106) states that the
`.cta--alert` and `.cta--kit` rules "went with the move rather than into it: no
markup had used them since the 1.25.0 nav redesign." They did not go anywhere —
they are still in `site.css`, and still unused. A comment that describes a
cleanup that did not happen is worse than no comment.

`.android-note`, `.preview-warning`, `.btn--copied`, `.mini-sys`, `.chip` and
their children are **live** — injected by `calendar-buttons.js` and
`calc-widget.js`. Do not remove those.

**Why it matters.** `site.css` is 68 KB / 1,388 lines and 17 KB over the wire on
every one of the five pages that load it. More than that: an unused
`.hero--split` block that styles an alternate hero layout is a trap for whoever
next edits the hero, because grepping `hero` returns two complete
implementations.

**Fix:** delete the blocks above and correct the comment at line 106 to say what
is actually true.

---

### M8. Twelve internal links route through a compatibility shim built for Pinterest  ·  FIXED 1.33.1

**Where:** the `#calendars` entry in [index.html:83-89](docs/index.html:83), and
these twelve links:

```
calculator/index.html:495       calendars/index.html:237
guides/index.html:564, 615      resources/index.html:195
resources/flood-insurance-30-day-rule/index.html:253
resources/strengthen-mississippi-homes/index.html:307
shop/index.html:171, 223, 512   storm/index.html:174, 195
```

The shim exists to catch published Pinterest pins that cannot be edited in
bulk. Internal links have no such excuse: they cost a load of the homepage, a
`location.replace`, and a second load of `/calendars/`; they break entirely
with scripting off; and they inflate homepage pageviews in the analytics the
privacy page promises are only counting visits.

**Fix:** point all twelve at `/calendars/` directly. Keep the shim for the pins.

---

### M9. `floir.com` has moved to `floir.gov`  ·  FIXED 1.33.1

**Where:** [resources/wind-mitigation-discounts/index.html:249](docs/resources/wind-mitigation-discounts/index.html:249) —
`<a href="https://floir.com">Florida Office of Insurance Regulation</a>`.

Verified: `https://floir.com` → `301` → `https://floir.gov/`.

All fifteen other outbound links resolve `200`
(`ldi.la.gov/fortifyhomes`, `mysafeflhome.com`, `strengthenalabamahomes.com`,
`aldoi.gov`, `mid.ms.gov/…/smh/`, `msplans.com`, `fortifiedhome.org`,
`fortifiedhome.org/incentives/`, `tdi.texas.gov/wind/index.html`, `twia.org`,
`floodsmart.gov` ×2, `msc.fema.gov/portal/home`, `magnoliatribune.com`).
`aldoi.gov` and `msplans.com` are linked with a `www.` prefix that redirects;
harmless, but worth normalising.

**Why it matters.** On a page whose credibility rests on "we link you to the
institution in charge," linking the old `.com` when the agency has moved to
`.gov` is the one link a sceptical reader would notice.

**Fix:** `https://floir.gov`, and drop the redundant `www.` on the two others.

---

### M10. Bare agency homepages where a deep link exists

**Where:** [resources/wind-mitigation-discounts/index.html:216, 227, 238, 249, 261](docs/resources/wind-mitigation-discounts/index.html:216) —
links to `mid.ms.gov`, `ldi.la.gov`, `aldoi.gov`, `floir.com` and
`tdi.texas.gov/wind/`.

The page's own copy says LDI *"publishes its own discount guide, featured on its
homepage"* — that is a page, and the reader is left to find it.

**Why it matters.** The page's promise is *"a map to who runs that, state by
state."* A state agency homepage is not a map, it is a directory the reader now
has to search. Every other resource page deep-links correctly, which is why this
one stands out.

**Fix:** link the specific discount / mitigation page on each agency site and
date it in the `.checked` line like everything else. Where a state genuinely has
no such page, say so — "LDI has no standing discount page; the guide is
promoted from their homepage during season" is more useful than a bare domain.

---

### M11. Unclosed `<div>` on `/calendars/`  ·  FIXED 1.33.1

**Where:** [calendars/index.html:133](docs/calendars/index.html:133) —
`<div style="margin-top:2rem">` opens and never closes. Counted: 32 `<div>`,
31 `</div>`. Every other page balances.

The parser repairs it (verified: all four `.tier` elements still resolve inside
`#calendars`), so nothing is visibly wrong today. But the `</div>` at
[:158](docs/calendars/index.html:158) that was written for `.wrap` now closes
the anonymous div instead, and `.wrap` is closed implicitly at `</section>`.
Any future edit inside that section will behave unpredictably.

**Fix:** close the div before `</section>`, and drop the inline `style` into a
class while you are there.

---

### M12. Three horizontally scrolling regions cannot be scrolled by keyboard

**Where:** the three `.prow` containers on [shop/index.html:293, 396, 477](docs/shop/index.html:293).

Measured at 390 px: `scrollWidth` 781, `clientWidth` 347, `overflow-x: auto`,
`tabindex: null`, no `role`.

WCAG 2.1.1 requires scrollable regions to be operable from a keyboard. A
keyboard-only user can reach the images' `alt` text via a screen reader but
cannot bring images two and three into view.

The homepage's `.scroll` diagram wrapper ([index.html:361](docs/index.html:361))
has the same shape but carries an `<svg role="img" aria-label="…">` with a full
prose description, so the content is at least reachable another way.

**Fix:** `tabindex="0"` plus an accessible name (`role="group"
aria-label="Pages from the kit"`) on each `.prow` and on `.scroll`, and a
`:focus-visible` outline so the focus is visible when it lands there.

---

### M13. No focus styles anywhere in the top bar

**Where:** [nav.css](docs/nav.css) defines `:hover` for `.nav-links a`,
`.nav-menu a`, `a.mark` and `.topbar a.cta--free`, and `:focus-within` for the
dropdown, but **no `:focus-visible` rule at all**.

Every other interactive surface on the site defines one explicitly —
`site.css:229, 366, 666, 685, 752, 791, 960, 1322`, `calculator/index.html:80,
88, 162, 244`, `guides/index.html:169, 190`, `404.html:54`.

The keyboard path through the dropdowns does work — focusing the trigger
satisfies `:focus-within`, which displays the menu, and the next Tab enters it.
That part is correct and the comment at [nav.css:71-73](docs/nav.css:71)
describes it accurately.

**Fix:** add `.topbar a:focus-visible { outline: 2px solid var(--sand);
outline-offset: 2px; }` (using the lifted sand from H1). Consider
`aria-expanded` on the dropdown triggers, though with a CSS-only menu that
cannot be kept truthful — a small script or a `<details>` would be needed to do
it properly.

---

### M14. The only way to contact this site is an Etsy storefront

**Where:** every "get in touch" route on the site:

- resource page footers: *"Spotted something above that no longer matches the department's page? Message the [Etsy shop](https://www.etsy.com/shop/GulfCoastHomeCare) and it gets fixed"* — [resources/louisiana-fortify-homes/index.html:278-282](docs/resources/louisiana-fortify-homes/index.html:278)
- `/resources/`: *"If there is a program or a rule you want mapped out, say so through the Etsy shop"* — [resources/index.html:170-175](docs/resources/index.html:170)
- every full footer: "Message the shop" → Etsy
- **`/privacy.html`:** *"Questions about any of this go to the Etsy shop, where messages reach me"* — [privacy.html:228-230](docs/privacy.html:228)

There is also no About page. The author is "Chad" in one paragraph on the
homepage ([index.html:662-677](docs/index.html:662)), which is not reachable from
`/guides/`, `/calculator/` or any resource page, and the `#who` anchor that
would reach it is broken by C1.

**Why it matters.** This is the largest single drag on the "reference or
storefront" question, and it is structural rather than cosmetic. A reader
checking whether to trust a page about $10,000 of public money finds that the
only way to reach its author is through a marketplace listing — which requires
an Etsy account, and which routes a correction about a state agency through a
retail channel. For search purposes it is also a straightforward E-E-A-T
weakness on exactly the kind of content Google treats as sensitive: money,
insurance, government programmes.

**Fix:** three things, none large.
1. A real contact address — even `hello@gulfcoasthomemaintenance.com` forwarded to a mailbox — used everywhere Etsy is currently offered as the contact route. In `privacy.html` this is close to a requirement: a privacy policy needs a controller contact that is not a third-party storefront.
2. An `/about/` page: who wrote this, why, what the sourcing rule is (the pointer-form discipline in `HANDOFF.md` is genuinely unusual and worth stating publicly), how corrections are handled, and how the site makes money. Link it from the nav and every footer.
3. `Organization` structured data on the homepage with `contactPoint`, alongside the existing `WebSite` node, and `author`/`publisher` on the resource pages pointing at it rather than at a bare organisation name.

---

### M15. Footer link sets differ from page to page for no reason

- `/calendars/` ([:237-240](docs/calendars/index.html:237)) omits "Storm season" from the Free column, which every other full footer includes.
- `/calendars/` puts the disclaimer above the `foot-grid`; every other page puts it below.
- `/calculator/` ([:538-542](docs/calculator/index.html:538)) has three links: Home, guides, Privacy.
- `/guides/` ([:613-617](docs/guides/index.html:613)) has four: Home, `#calendars`, calculator, Privacy.
- Neither reaches `/resources/`, `/storm/` or `/shop/`.

**Fix:** one footer, everywhere. See C3.

---

### M16. No breadcrumbs, and no structured data on four pages

`BreadcrumbList` appears nowhere. `/storm/`, `/calendars/`, `/resources/` and
`/privacy.html` carry no structured data at all.

**Why it matters.** The resource pages are three levels deep and are the primary
landing pages. Breadcrumb markup is what turns
`gulfcoasthomemaintenance.com › resources › louisiana-fortify-homes` into
`Gulf Coast Home Maintenance › Grants and programs › Louisiana` in the search
result — which is both more clickable and, for a reader deciding whether this is
a real site, more legible.

**Fix:** add a `BreadcrumbList` to the seven resource pages and to `/resources/`,
and a `WebPage` node to `/storm/` and `/calendars/` matching the one `/guides/`
already has at [guides/index.html:648](docs/guides/index.html:648).

---

### M17. `docs/img/hero.png` is a 2.9 MB file that is not deployed and not referenced

**Where:** `docs/img/hero.png`, 2,892,840 bytes.

Verified: no HTML, CSS or JS file references it, and
`https://gulfcoasthomemaintenance.com/img/hero.png` returns **404** — so it is
not even being published. It is 79 % of the `docs/img/` directory by size and it
is in the repository's history permanently.

**Fix:** delete it, or move it out of `docs/` into a source-assets directory if
`optimize_images.py` needs the original. Note the deployed pages are lean —
total transfer for the homepage measured at **195 KB**, of which the hero
accounts for 166 KB — so this is repo hygiene rather than a page-weight problem.

---

### M18. `/privacy.html` footer link is mislabelled

**Where:** [privacy.html:230](docs/privacy.html:230) —
`Back to <a href="./">the calendars</a>.`

`./` from `/privacy.html` is the site root, not `/calendars/`. The link is
either mislabelled or pointing at the wrong place; it predates the 1.29.0 move
of the picker to its own page.

**Fix:** either `Back to <a href="./">Gulf Coast Home Maintenance</a>` or
`<a href="calendars/">the calendars</a>`, whichever was meant.

---

## Nitpick

- **N1.** Every page uses the same `og:image` (the live-oak hero). A shared link to the shop, the calculator and the grant shelf all preview identically. Product covers and per-topic cards exist or are cheap to generate.
- **N2.** [resources/strengthen-mississippi-homes/index.html:280](docs/resources/strengthen-mississippi-homes/index.html:280) cites SB 2409 through a news outlet (`magnoliatribune.com`). Every other institutional fact on the shelf is sourced to the institution; the bill text on the legislature's site would match the house rule.
- **N3.** The `.next` boxes are labelled "Related tools" but mostly contain articles. "Read next" or "Related" would be accurate, and the box would then not have to carry a price tag to justify its name.
- **N4.** `.nav-drop > a::after` ([nav.css:75-78](docs/nav.css:75)) draws a ▾ implying an openable menu. Between 832 px and touch-tablet width, tapping the trigger navigates instead of opening it. The top link goes somewhere real so nothing is lost, but the affordance is not honest.
- **N5.** Below 480 px the wordmark loses its label ([nav.css:108-110](docs/nav.css:108)) and the home link becomes an **18 × 18 px** target — measured. WCAG 2.2 SC 2.5.8 asks for 24 × 24. Padding the anchor to 44 px costs nothing since the bar has the room. (The footer link lists were checked and *pass* via spacing: 25 px tall on a 33 px pitch.)
- **N6.** [guides/index.html:254 and 257](docs/guides/index.html:254) both carry `aria-current="page"` for the same destination — once in the Tools dropdown, once on "Guide". Harmless, but announced twice.
- **N7.** `sitemap.xml` sets `changefreq` and `priority` on all 15 URLs. Google has ignored both for years. `lastmod` — which it does use — is correct and per-page here, which is the part that matters.
- **N8.** [404.html](docs/404.html) has no `<main>` landmark; content sits in `.middle > .card`. Given the page's intended austerity this is a one-attribute fix, not a redesign.
- **N9.** Nine `!important` declarations in `site.css` ([619, 631, 633, 691, 695, 963, 1386, 1387](docs/site.css:619)) fight specificity that could be resolved by ordering. Two of them (`.mini-calc-note`) are on dead rules and go away with M7.
- **N10.** Hardcoded hex values that should be tokens: `#7fa6ad` ([site.css:479](docs/site.css:479)), `#7a5719` ([:647](docs/site.css:647)), `#7a5c22` and `#3d4f52` ([:196-197](docs/site.css:196)), `#d8d3c7` and `#ded8cb` ([:155, 177](docs/site.css:155)). Most are dark-mode variants of an existing token and would be a `color-mix()` or a new `--*` entry in `theme.css`.
- **N11.** The hero `<img>` ([index.html:135-137](docs/index.html:135)) has no `width`/`height` attributes, unlike every other image on the site. No layout shift results — `.hero-media` is `position: absolute; inset: 0` — but it is the one exception to an otherwise consistent rule.
- **N12.** `body { overflow-x: hidden }` ([site.css:22](docs/site.css:22)) suppresses horizontal overflow rather than preventing it. No overflow was found at 390 px on any page (the SVG diagram and the `.prow` strips are inside proper `overflow-x: auto` wrappers), so it is currently doing nothing except hiding future bugs.
- **N13.** The `og:image:alt` string is duplicated verbatim in nine files. Same drift class as M5, one line each.
