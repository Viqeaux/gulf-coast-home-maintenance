#!/usr/bin/env python3
"""
Build the print edition as HTML, then hand it to headless Chrome for the PDF.

Design constraints, in priority order:

1. It has to survive a home printer. No full-bleed anything: consumer printers
   cannot reach the paper edge, so a background that runs off the page comes out
   with a white frame around it. Everything sits inside a 0.6in safe margin.
2. Ink is the buyer's money. Large dark fills streak, print slowly, and empty a
   cartridge. So the page earns its keep through type, white space and hairlines
   rather than through decoration, which also happens to look more expensive.
3. It has to read in grayscale. Plenty of people print black and white, so
   color is never the only thing distinguishing one tier from another; weight
   and position carry it too.

This builds the KIT, which is the paid product: every printable page. The free
product is the three calendar feeds, which build_calendars.py makes.

Run:  python build_printables.py
Out:  product/gulf-coast-home-maintenance-kit.html   (source, edit the generator)
      product/gulf-coast-home-maintenance-kit.pdf    (the deliverable, sold on Etsy)
"""

import os
import subprocess
import sys

from build_calendars import TASKS, VERSION
from kit_sections import SECTIONS
from task_steps import STEPS

# The repo is public and this is the paid product, so the build lands in
# product/, which .gitignore keeps out of git. Committing it would put the kit
# on GitHub as a free download.
OUT_DIR = "product"
BASENAME = "gulf-coast-home-maintenance-kit"

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]

TIER_ORDER = {"must": 0, "should": 1, "above": 2}
TIER_LABEL = {"must": "Must do", "should": "Should do", "above": "Going above"}

# Months that carry a standing note across the top of the page.
MONTH_BANNERS = {
    5:  ("Hurricane prep month", "Season opens June 1"),
    8:  ("Peak hurricane season", "Storms are most likely now"),
    11: ("Season closes November 30", "Walk the property before you relax"),
}

WATCH_LIST = [
    ("Roof, asphalt shingle", "12–15 years"),
    ("Roof, metal", "30–40 years"),
    ("Water heater, tank", "8–10 years"),
    ("Water heater anode rod", "4–5 years"),
    ("A/C condenser (outdoor)", "10–12 years"),
    ("Furnace / air handler", "15–18 years"),
    ("Ductwork", "15–20 years"),
    ("Exterior paint", "5–7 years"),
    ("Exterior caulk & sealants", "2–4 years"),
    ("Windows", "15–25 years"),
    ("Garage door opener", "10–12 years"),
    ("Dishwasher", "9 years"),
    ("Refrigerator", "10–13 years"),
    ("Washer / dryer", "10–13 years"),
    ("Septic tank, pump out", "every 3–5 years"),
    ("Fence, wood", "10–15 years"),
    ("Deck, wood", "10–20 years"),
]

FIRST_MONTH = [
    "Find and tag the main water shutoff",
    "Find and tag the gas shutoff",
    "Label every breaker in the panel",
    "Locate the septic tank lid or the sewer cleanout",
    "Find the A/C condensate drain line and its cleanout",
    "Write down every air filter size and tape the list inside the closet door",
    "Photograph every room and the full exterior, before anything happens",
    "Register warranties on anything new",
    "Collect appliance manuals in one folder",
    "Open a maintenance fund and start setting money aside monthly",
]

HOW_TO_FIND_OUT = [
    ("Water heater",
     "The manufacture date is encoded in the serial number on the label. Search "
     "the brand name plus &ldquo;serial number date&rdquo; and you will find the decoder."),
    ("A/C and furnace",
     "Check the data plate on the outdoor unit and inside the air handler closet. "
     "Most list the manufacture date outright."),
    ("Roof",
     "Try the old real estate listing photos, the seller&rsquo;s disclosure statement, "
     "or your county permit records. A re-roof usually pulls a permit."),
    ("Appliances",
     "Model and serial are on a sticker inside the door, on the back, or under the lid."),
    ("Anything original to the house",
     "Use the year the house was built. It is rarely wrong."),
]

DISCLAIMER = ("General maintenance guidance, not a substitute for a licensed "
              "inspector, contractor, or your insurance policy terms.")


def esc(text):
    return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# --- page helpers ----------------------------------------------------------

def page(inner, foot="", classes=""):
    cls = ("page " + classes).strip()
    return (
        '<section class="{0}">\n'
        '  <div class="sheet">\n{1}\n  </div>\n'
        '  <footer class="page-foot"><span>Gulf Coast Home Maintenance</span>'
        '<span>{2}</span></footer>\n'
        '</section>'.format(cls, inner, foot)
    )


def cover_page():
    return page(
        '    <div class="cover">\n'
        '      <p class="kicker">The</p>\n'
        '      <h1 class="cover-title">Gulf&nbsp;Coast<br>Home Maintenance<br>Calendar</h1>\n'
        '      <div class="cover-rule"></div>\n'
        '      <p class="cover-sub">Twelve months, three tiers, and the list of everything '
        'in your house that is already on a clock.</p>\n'
        '      <p class="cover-note">Undated. It never expires, so start any month you like.</p>\n'
        '    </div>',
        foot="")


def tiers_page():
    rows = ""
    for key, blurb in (
        ("must", "Safety, or skipping it costs you thousands. If you do nothing "
                 "else, do these twelve things."),
        ("should", "Protects your home&rsquo;s value and makes what you own last longer."),
        ("above", "For the homeowner who wants to stay ahead of everything."),
    ):
        rows += (
            '      <div class="tier-row tier--{0}">\n'
            '        <p class="tier-name">{1}</p>\n'
            '        <p class="tier-blurb">{2}</p>\n'
            '      </div>\n'.format(key, TIER_LABEL[key], blurb))

    return page(
        '    <p class="eyebrow">How to use this</p>\n'
        '    <h2>Start with one column</h2>\n'
        '    <p class="lede">Each month gives you three tasks at three levels of effort. '
        'They are meant to be taken in order, not all at once.</p>\n'
        '{0}'
        '    <p class="pull">Nobody does all of this the first year. Working down the '
        '<em>Must do</em> line for twelve months puts you ahead of most homeowners on '
        'this coast.</p>\n'.format(rows),
        foot="How to use this")


def first_month_page():
    items = ""
    for job in FIRST_MONTH:
        items += ('      <li><span class="box" data-fill="check"></span>{0}</li>\n'.format(esc(job)))
    return page(
        '    <p class="eyebrow">Before the months begin</p>\n'
        '    <h2>Your first month</h2>\n'
        '    <p class="lede">One-time jobs. They never repeat, which is exactly why '
        'they get forgotten. Do these once and the rest of the year is easier.</p>\n'
        '    <ul class="checklist">\n{0}    </ul>\n'.format(items),
        foot="Your first month")


# Months whose three tasks carry too much detail for one sheet. Measured, not
# guessed: the build harness reports any page whose content exceeds the sheet,
# and these are the ones that did. Add to this set if a month grows.
TWO_PAGE_MONTHS = {5}


def year_page():
    """The seasons diagram. Same information as the one on the site, redrawn for
    paper: solid bands on white rather than tinted bands on a dark ground."""
    months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
              "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    # 12 columns across the plot area, which starts after the row labels.
    x0, width = 150.0, 750.0
    col = width / 12.0

    grid = "".join(
        '          <line x1="{0:.1f}" y1="34" x2="{0:.1f}" y2="250"/>\n'.format(
            x0 + i * col) for i in range(13))
    labels = "".join(
        '          <text x="{0:.1f}" y="24">{1}</text>\n'.format(
            x0 + (i + 0.5) * col, name) for i, name in enumerate(months))

    def band(start_month, months_long, y, fill):
        return ('          <rect x="{0:.1f}" y="{1}" width="{2:.1f}" height="30" '
                'rx="2" fill="{3}"/>\n'.format(
                    x0 + (start_month - 1) * col, y, months_long * col, fill))

    bands = (
        band(6, 6, 46, "#9c3722") +     # hurricane, June 1 to Nov 30
        band(5, 5, 92, "#a8761f") +     # heat and humidity, May to September
        band(3, 3, 138, "#56682f") +    # termite swarm, March to May
        band(1, 2, 184, "#14606e") +    # freeze, January and February
        band(12, 1, 184, "#14606e")     # and December
    )

    # May 1 is where the insurance deadline actually falls.
    marker_x = x0 + 4 * col
    return page(
        '    <p class="eyebrow">Why the months are ordered this way</p>\n'
        '    <h2>The Gulf Coast year</h2>\n'
        '    <p class="lede">Four overlapping seasons your house has to survive, and '
        'they do not line up with the ones on an ordinary calendar.</p>\n'
        '    <div class="figure">\n'
        '      <svg viewBox="0 0 920 300" width="100%">\n'
        '        <g class="diag-grid">\n{0}        </g>\n'
        '        <g class="diag-month" text-anchor="middle">\n{1}        </g>\n'
        '        <g class="diag-row" text-anchor="end">\n'
        '          <text x="138" y="66">HURRICANE</text>\n'
        '          <text x="138" y="112">HEAT &amp; HUMIDITY</text>\n'
        '          <text x="138" y="158">TERMITE SWARM</text>\n'
        '          <text x="138" y="204">FREEZE RISK</text>\n'
        '        </g>\n{2}'
        '        <line class="diag-marker" x1="{3:.1f}" y1="34" x2="{3:.1f}" y2="258"/>\n'
        '        <text class="diag-note" x="{3:.1f}" y="276" text-anchor="middle">'
        'INSURE BEFORE MAY 1</text>\n'
        '      </svg>\n'
        '    </div>\n'
        '    <p class="pull">A flood policy generally takes 30 days to take effect. '
        'That is the whole reason hurricane prep sits in May and not in June: by the '
        'time the season opens, buying cover is already too late to help you.</p>\n'.format(
            grid, labels, bands, marker_x),
        foot="The year")


def month_pages(index):
    """Return the sheets for one month, usually one, sometimes two."""
    name = MONTHS[index - 1]
    tasks = sorted([t for t in TASKS if t[0] == index],
                   key=lambda t: TIER_ORDER[t[2]])

    if index in TWO_PAGE_MONTHS:
        return [_month_sheet(name, index, tasks[:2], part=1),
                _month_sheet(name, index, tasks[2:], part=2)]
    return [_month_sheet(name, index, tasks)]


def _month_sheet(name, index, tasks, part=0):
    banner = ""
    if index in MONTH_BANNERS and part != 2:
        head, sub = MONTH_BANNERS[index]
        banner = ('    <p class="banner"><strong>{0}</strong><span>{1}</span></p>\n'
                  .format(head, sub))

    heading = ('    <h2 class="month-name">{0}{1}</h2>\n'.format(
        name, '<span class="cont">continued</span>' if part == 2 else ''))

    blocks = ""
    for _, _, tier, slug, title, body in tasks:
        parts = [p.strip() for p in body.split("\n\n") if p.strip()]
        instruction = parts[0] if parts else ""
        why = parts[1] if len(parts) > 1 else ""
        detail = STEPS.get(slug) or {}

        extras = ""
        if detail.get("need"):
            extras += ('        <p class="need"><span>You need</span>{0}</p>\n'
                       .format(esc(" &middot; ".join(detail["need"]))
                               .replace("&amp;middot;", "&middot;")))
        if detail.get("pro"):
            extras += ('        <p class="pro">A job for a professional, '
                       'here is what to ask for.</p>\n')
        if detail.get("steps"):
            extras += '        <ol class="steps">\n'
            for step in detail["steps"]:
                extras += '          <li>{0}</li>\n'.format(esc(step))
            extras += '        </ol>\n'
        if detail.get("watch"):
            extras += ('        <p class="watch"><span>Watch out</span>{0}</p>\n'
                       .format(esc(detail["watch"])))

        blocks += (
            '      <div class="task tier--{0}">\n'
            '        <p class="tier-tag">{1}<span class="box box--task" data-fill="check"></span></p>\n'
            '        <h3>{2}</h3>\n'
            '        <p class="do">{3}</p>\n'
            '{4}{5}'
            '      </div>\n'.format(
                tier, TIER_LABEL[tier], esc(title), esc(instruction),
                ('        <p class="why">{0}</p>\n'.format(esc(why)) if why else ""),
                extras))

    # A short sheet gets ruled space rather than an awkward gap at the bottom.
    notes = ""
    if part == 2 or len(tasks) < 3:
        notes = ('    <div class="notes">\n'
                 '      <p class="notes-label">Notes</p>\n'
                 + ('      <div class="rule-line" data-fill="text"></div>\n' * 5) +
                 '    </div>\n')

    return page(
        '{0}{1}    <div class="tasks">\n{2}    </div>\n{3}'.format(
            heading, banner, blocks, notes),
        foot=name)


def watch_list_page():
    # data-fill marks the blanks. build_fillable.py measures them in the browser
    # and stamps real form fields at those positions, so the same layout serves
    # the print file and the fillable one.
    rows = ""
    for item, life in WATCH_LIST:
        rows += (
            '        <tr>\n'
            '          <td class="item">{0}</td>\n'
            '          <td class="fill" data-fill="text"></td>\n'
            '          <td class="life">{1}</td>\n'
            '          <td class="fill" data-fill="text"></td>\n'
            '        </tr>\n'.format(esc(item), esc(life)))

    return page(
        '    <p class="eyebrow">The back page</p>\n'
        '    <h2>The Big Ticket Watch List</h2>\n'
        '    <p class="lede">Everything expensive in your house is already on a clock. '
        'Fill in the year each one went in, add the lifespan, and you will know what to '
        'start saving for, instead of finding out the hard way.</p>\n'
        '    <table class="watch-list">\n'
        '      <thead><tr>\n'
        '        <th>Item</th><th>Year installed</th>\n'
        '        <th>Typical Gulf&nbsp;Coast life</th><th>Start watching in</th>\n'
        '      </tr></thead>\n'
        '      <tbody>\n{0}      </tbody>\n'
        '    </table>\n'
        '    <p class="footnote"><strong>Why these run shorter than the numbers online.</strong> '
        'Salt air, high humidity and hard UV wear coastal homes faster than national averages '
        'assume. These are adjusted for the Gulf Coast. They are guidelines rather than '
        'guarantees, and a well-maintained roof outlives a neglected one.</p>\n'.format(rows),
        foot="The Watch List")


def how_to_find_out_page():
    blocks = ""
    for label, text in HOW_TO_FIND_OUT:
        blocks += ('      <div class="find">\n'
                   '        <p class="find-label">{0}</p>\n'
                   '        <p class="find-text">{1}</p>\n'
                   '      </div>\n'.format(label, text))

    return page(
        '    <p class="eyebrow">Facing the Watch List</p>\n'
        '    <h2>Don&rsquo;t know when it was installed?</h2>\n'
        '    <p class="lede">Most of these take five minutes to find. You do not need '
        'the previous owner, and you do not need a contractor.</p>\n'
        '    <div class="finds">\n{0}    </div>\n'
        '    <p class="pull">Still cannot tell? Write <em>unknown</em> and put this year '
        'in the last column. Have it looked at once, note the condition, and you have a '
        'baseline from here on. Unknown is a starting point, not a dead end.</p>\n'.format(blocks),
        foot="How to find out")


# --- design ----------------------------------------------------------------

CSS = """
  @page { size: Letter; margin: 0; }

  :root {
    --ink:    #17211f;
    --body:   #3d4a48;
    --muted:  #6b7876;
    --hair:   #cfc6b4;   /* hairlines: warm, so they read as printed not digital */
    --accent: #0f5e6b;
    --sand:   #a8761f;
    --must:   #9c3722;
    --should: #14606e;
    --above:  #56682f;
  }

  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; background: #fff; }
  body {
    font: 10.5pt/1.5 Georgia, "Iowan Old Style", serif;
    color: var(--body);
    -webkit-print-color-adjust: exact; print-color-adjust: exact;
  }

  /* A sheet is exactly Letter. Nothing bleeds: consumer printers cannot reach
     the paper edge, so a full-bleed design returns with a white frame round it. */
  .page {
    width: 8.5in; height: 11in; padding: 0.62in 0.68in 0.5in;
    position: relative; page-break-after: always; overflow: hidden;
    display: flex; flex-direction: column;
  }
  .page:last-child { page-break-after: auto; }
  .sheet { flex: 1 1 auto; }
  .page-foot {
    flex: 0 0 auto; display: flex; justify-content: space-between;
    border-top: 0.5pt solid var(--hair); padding-top: 6pt;
    font: 6.5pt/1 "Segoe UI", system-ui, sans-serif;
    letter-spacing: .14em; text-transform: uppercase; color: var(--muted);
  }

  /* --- shared type ----------------------------------------------------- */
  .eyebrow {
    font: 700 7pt/1 "Segoe UI", system-ui, sans-serif;
    letter-spacing: .2em; text-transform: uppercase; color: var(--accent);
    margin: 0 0 10pt;
  }
  h2 {
    font: 400 26pt/1.08 Georgia, serif; color: var(--ink);
    margin: 0 0 10pt; letter-spacing: -.01em;
  }
  .lede {
    font-size: 10.5pt; color: var(--body); margin: 0 0 20pt;
    max-width: 6.1in;
  }
  .pull {
    margin: 22pt 0 0; padding: 12pt 0 0; border-top: 1.5pt solid var(--ink);
    font-size: 10pt; color: var(--ink); max-width: 6.1in;
  }
  .pull em { font-style: italic; }

  /* --- cover ----------------------------------------------------------- */
  .cover { height: 100%; display: flex; flex-direction: column; justify-content: center; }
  .kicker {
    font: 700 8pt/1 "Segoe UI", system-ui, sans-serif;
    letter-spacing: .34em; text-transform: uppercase; color: var(--sand);
    margin: 0 0 14pt;
  }
  .cover-title {
    font: 400 46pt/1.03 Georgia, serif; color: var(--ink);
    margin: 0; letter-spacing: -.022em;
  }
  .cover-rule { width: 1.5in; height: 2.5pt; background: var(--sand); margin: 26pt 0; }
  .cover-sub {
    font-size: 13pt; line-height: 1.45; color: var(--body);
    max-width: 4.6in; margin: 0 0 16pt;
  }
  .cover-note {
    font: 700 8pt/1.4 "Segoe UI", system-ui, sans-serif;
    letter-spacing: .12em; text-transform: uppercase; color: var(--muted); margin: 0;
  }

  /* --- tiers page ------------------------------------------------------ */
  .tier-row { border-left: 3pt solid var(--tone); padding: 2pt 0 2pt 14pt; margin-bottom: 18pt; }
  .tier--must   { --tone: var(--must); }
  .tier--should { --tone: var(--should); }
  .tier--above  { --tone: var(--above); }
  .tier-name {
    font: 700 11pt/1 "Segoe UI", system-ui, sans-serif;
    color: var(--tone); margin: 0 0 5pt; letter-spacing: .01em;
  }
  .tier-blurb { margin: 0; font-size: 10.5pt; max-width: 5.6in; }

  /* --- checklist ------------------------------------------------------- */
  .checklist { list-style: none; margin: 0; padding: 0; }
  .checklist li {
    display: flex; align-items: flex-start; gap: 11pt;
    padding: 11pt 0; border-bottom: 0.5pt solid var(--hair);
    font-size: 11pt; color: var(--ink);
  }
  /* An outlined box costs a few drops of ink. A filled one costs a cartridge. */
  .box {
    flex: none; width: 12pt; height: 12pt; margin-top: 1pt;
    border: 1pt solid var(--muted); border-radius: 1.5pt;
  }

  /* --- month page ------------------------------------------------------ */
  .month-name {
    font: 400 40pt/1 Georgia, serif; color: var(--ink);
    margin: 0 0 4pt; letter-spacing: -.02em;
  }
  .month-name .cont {
    font: 400 9pt/1 "Segoe UI", system-ui, sans-serif;
    letter-spacing: .18em; text-transform: uppercase; color: var(--muted);
    margin-left: 12pt; vertical-align: middle;
  }
  .banner {
    display: flex; align-items: baseline; gap: 10pt;
    border-top: 1.5pt solid var(--must); border-bottom: 0.5pt solid var(--hair);
    padding: 7pt 0; margin: 10pt 0 0;
  }
  .banner strong {
    font: 700 8pt/1 "Segoe UI", system-ui, sans-serif;
    letter-spacing: .16em; text-transform: uppercase; color: var(--must);
  }
  .banner span { font-size: 9.5pt; color: var(--muted); font-style: italic; }

  .tasks { margin-top: 14pt; }
  .task { padding: 0 0 8pt 12pt; margin-bottom: 10pt; border-left: 3pt solid var(--tone); }
  .task:last-child { margin-bottom: 0; padding-bottom: 0; }
  .tier-tag {
    font: 700 7pt/1 "Segoe UI", system-ui, sans-serif;
    letter-spacing: .2em; text-transform: uppercase; color: var(--tone);
    margin: 0 0 5pt; display: flex; justify-content: space-between; align-items: center;
  }
  .task h3 {
    font: 700 12pt/1.25 "Segoe UI", system-ui, sans-serif;
    color: var(--ink); margin: 0 0 4pt;
  }
  .box--task { margin-top: 0; }
  .task .do { margin: 0 0 4pt; font-size: 10pt; color: var(--body); }
  .task .why { margin: 0 0 5pt; font-size: 9pt; color: var(--muted); font-style: italic; }

  /* Numbered steps are the substance of the page. They stay tight so a month
     still fits one sheet. Three tasks with six steps each is a lot of lines. */
  .steps { margin: 0 0 5pt; padding-left: 13pt; }
  .steps li {
    font-size: 9.5pt; line-height: 1.36; color: var(--ink);
    margin-bottom: 1.5pt; padding-left: 2pt;
  }
  .steps li::marker { color: var(--tone); font-weight: bold; font-size: 8.5pt; }

  .need, .watch {
    font-size: 8.5pt; line-height: 1.4; margin: 0 0 6pt; color: var(--muted);
  }
  .need span, .watch span {
    font: 700 6.5pt/1 "Segoe UI", system-ui, sans-serif;
    letter-spacing: .14em; text-transform: uppercase;
    display: inline-block; margin-right: 6pt; color: var(--ink);
  }
  .watch { border-left: 1.5pt solid var(--must); padding-left: 8pt; }
  /* Inline label on a task, but a full-width section note reads better with the
     label on its own line above the text. */
  .watch--block span { display: block; margin-bottom: 4pt; }
  .watch span { color: var(--must); }
  .pro {
    font: italic 8.5pt/1.4 Georgia, serif; color: var(--accent); margin: 0 0 6pt;
  }

  /* --- watch list ------------------------------------------------------ */
  table.watch-list { width: 100%; border-collapse: collapse; margin-bottom: 16pt; }
  table.watch-list th {
    font: 700 6.5pt/1.3 "Segoe UI", system-ui, sans-serif;
    letter-spacing: .13em; text-transform: uppercase; color: var(--muted);
    text-align: left; padding: 0 6pt 6pt 0; border-bottom: 1.25pt solid var(--ink);
  }
  table.watch-list td {
    padding: 0; height: 21pt; border-bottom: 0.5pt solid var(--hair);
    font-size: 9.5pt; vertical-align: middle;
  }
  table.watch-list .item { color: var(--ink); padding-right: 8pt; width: 2.5in; }
  table.watch-list .life { color: var(--accent); font-weight: bold; width: 1.35in; padding: 0 8pt; }
  /* The blank columns are the point of the page, give them room to write. */
  table.watch-list .fill { width: 1.2in; }
  .footnote {
    font-size: 8.5pt; line-height: 1.45; color: var(--muted);
    border-top: 0.5pt solid var(--hair); padding-top: 9pt; margin: 0;
  }
  .footnote strong { color: var(--ink); }

  /* --- year diagram ----------------------------------------------------- */
  .figure { margin: 24pt 0 0; }
  .diag-grid line { stroke: #ded6c6; stroke-width: 0.75; }
  .diag-month {
    font: 700 9pt "Segoe UI", system-ui, sans-serif;
    letter-spacing: .08em; fill: var(--muted);
  }
  .diag-row {
    font: 700 9pt "Segoe UI", system-ui, sans-serif;
    letter-spacing: .08em; fill: var(--ink);
  }
  .diag-marker { stroke: var(--must); stroke-width: 1.5; stroke-dasharray: 4 3; }
  .diag-note {
    font: 700 8.5pt "Segoe UI", system-ui, sans-serif;
    letter-spacing: .1em; fill: var(--must);
  }

  /* --- conditional sections -------------------------------------------- */
  .checklist--tight li { padding: 8pt 0; font-size: 10.5pt; }
  .sub-label {
    font: 700 7pt/1 "Segoe UI", system-ui, sans-serif;
    letter-spacing: .2em; text-transform: uppercase; color: var(--accent);
    margin: 20pt 0 10pt; padding-bottom: 5pt; border-bottom: 1pt solid var(--ink);
  }
  .when-row {
    display: flex; gap: 14pt; padding: 8pt 0;
    border-bottom: 0.5pt solid var(--hair);
  }
  .when-label {
    flex: 0 0 1.5in; margin: 0;
    font: 700 8.5pt/1.35 "Segoe UI", system-ui, sans-serif; color: var(--ink);
  }
  .when-text { margin: 0; font-size: 9.5pt; line-height: 1.42; }
  ul.plain { list-style: none; margin: 0; padding: 0; }
  ul.plain li {
    position: relative; padding: 5pt 0 5pt 14pt; font-size: 9.5pt; line-height: 1.42;
  }
  /* A rule rather than a bullet glyph: it reads as a field guide and prints
     identically on any printer, whatever it does with dingbats. */
  ul.plain li::before {
    content: ""; position: absolute; left: 0; top: 11pt;
    width: 7pt; height: 0.75pt; background: var(--muted);
  }
  .watch--block {
    margin-top: 20pt; padding: 10pt 0 0 10pt;
    border-left: 1.5pt solid var(--must); border-top: 0.5pt solid var(--hair);
    font-size: 9pt;
  }

  /* --- how to find out ------------------------------------------------- */
  .find { padding: 11pt 0; border-bottom: 0.5pt solid var(--hair); }
  .find:first-child { padding-top: 0; }
  .find-label {
    font: 700 9.5pt/1 "Segoe UI", system-ui, sans-serif;
    color: var(--ink); margin: 0 0 4pt;
  }
  .find-text { margin: 0; font-size: 10pt; max-width: 6.1in; }
"""

DOCUMENT = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>The Gulf Coast Home Maintenance Calendar, print edition v{version}</title>
<style>{css}</style>
</head>
<body>
{body}
</body>
</html>
"""


def conditional_intro_page():
    items = ""
    for section in SECTIONS:
        items += ('      <li><span class="box" data-fill="check"></span>{0}</li>\n'
                  .format(esc(section["title"].replace("If you ", "")
                                              .replace("If your ", "your ")
                                              .capitalize())))
    return page(
        '    <p class="eyebrow">The rest of the house</p>\n'
        '    <h2>If you have one of these</h2>\n'
        '    <p class="lede">The twelve months cover what every house on this coast '
        'needs. These pages cover what yours might have on top of that. Tick what '
        'applies to you and skip the rest.</p>\n'
        '    <ul class="checklist checklist--tight">\n{0}    </ul>\n'
        '    <p class="pull">None of this is on the month pages on purpose. A '
        'checklist that lists jobs you cannot do, for equipment you do not own, is '
        'a checklist people stop reading.</p>\n'.format(items),
        foot="If you have one")


def conditional_page(section):
    when = ""
    for label, text in section["when"]:
        when += ('        <div class="when-row">\n'
                 '          <p class="when-label">{0}</p>\n'
                 '          <p class="when-text">{1}</p>\n'
                 '        </div>\n'.format(esc(label), esc(text)))

    always = ""
    for item in section.get("always", []):
        always += '          <li>{0}</li>\n'.format(esc(item))

    watch = ""
    if section.get("watch"):
        watch = ('      <p class="watch watch--block"><span>Watch out</span>{0}</p>\n'
                 .format(esc(section["watch"])))

    return page(
        '    <p class="eyebrow">Only if it applies</p>\n'
        '    <h2>{0}</h2>\n'
        '    <p class="lede">{1}</p>\n'
        '      <p class="sub-label">When</p>\n'
        '{2}'
        '      <p class="sub-label">Year round</p>\n'
        '        <ul class="plain">\n{3}        </ul>\n'
        '{4}'.format(esc(section["title"]), esc(section["lead"]), when, always, watch),
        foot=section["title"].replace("If you have ", "").replace("If you are ", "")
                             .replace("If your ", "").replace("a ", "").capitalize())


# --- assembly --------------------------------------------------------------

def build_html():
    pages = [cover_page(), tiers_page(), year_page(), first_month_page()]
    for index in range(1, 13):
        pages.extend(month_pages(index))
    pages += [watch_list_page(), how_to_find_out_page()]
    pages.append(conditional_intro_page())
    for section in SECTIONS:
        pages.append(conditional_page(section))
    return DOCUMENT.format(css=CSS, body="\n".join(pages),
                           version=VERSION, disclaimer=DISCLAIMER), len(pages)


def find_chrome():
    for path in CHROME_CANDIDATES:
        if os.path.exists(path):
            return path
    return None


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    html_path = os.path.join(OUT_DIR, BASENAME + ".html")
    html, count = build_html()
    with open(html_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(html)
    print("{0}  {1} pages".format(html_path, count))

    chrome = find_chrome()
    if not chrome:
        print("No Chrome or Edge found. Open the HTML and print to PDF by hand.")
        return 1

    pdf_path = os.path.abspath(os.path.join(OUT_DIR, BASENAME + ".pdf"))
    subprocess.run([
        chrome, "--headless", "--disable-gpu", "--no-sandbox",
        "--print-to-pdf-no-header",
        "--print-to-pdf=" + pdf_path,
        "file:///" + os.path.abspath(html_path).replace("\\", "/"),
    ], check=True, capture_output=True, timeout=180)
    print("{0}  {1:,} bytes".format(pdf_path, os.path.getsize(pdf_path)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
