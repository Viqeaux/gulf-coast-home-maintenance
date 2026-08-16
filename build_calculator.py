"""Builds "What Breaks Next", the offline house timeline tool.

    python build_calculator.py

Writes `product/gulf-coast-what-breaks-next.html`. One file, and one file is the
whole delivery: the buyer downloads it, double-clicks it, and it runs in
whatever browser they already have. No install, no account, no server, and no
internet.

**It is a paid download and not a page on the site.** Chad's call, 2026-08-16.
An earlier draft of this was a free traffic play living at `/calculator/`, cut
down to twelve systems so it would not give the planner away. As a product it
has no reason to hold anything back, so it carries all 49.

**Everything is inlined, including the palette.** `docs/theme.css` is read at
build time rather than copied, so the tool looks like the shop without being a
second hand-synced copy of the colors. A relative `<link>` would be a broken
file the moment it left the folder it was built in, which for a download is
always.

**It sends nothing anywhere, and the policy in the file enforces that** rather
than merely claiming it: `default-src 'none'` with no `connect-src` means a
script in here cannot reach the network even if one tried. That is worth having
for its own sake and it is also the honest version of the promise on the page,
which is that what you type about your house stays on your machine.

**No dollar amounts, and that is the line between this and the planner.** This
answers what and when, in five minutes, from one number. The planner answers
what it costs, what it will cost in the year it breaks, what to set aside every
month, and it is the thing you keep and update. A browser file cannot reliably
save anything from one open to the next, so it should not pretend to be a
record. Adding costs here would make the spreadsheet redundant rather than make
this better.
"""

import json
import os

from build_calendars import VERSION
from planner_data import REGIONS, SYSTEMS

OUT = os.path.join("product", "gulf-coast-what-breaks-next.html")
THEME = os.path.join("docs", "theme.css")

PRODUCT = "What Breaks Next"
DOMAIN = "gulfcoasthomemaintenance.com"

DISCLAIMER = ("General maintenance guidance, not a substitute for a licensed "
              "inspector, contractor, or your insurance policy terms.")

# Deliberately narrow, and deliberately not a full license. The kit's terms live
# in product/etsy-listing.md and there is an open question there about gifting
# that is Chad's to answer. Nothing here should quietly settle it.
LICENSE = "For your own household. Not for resale or redistribution."

# The ones almost every house has. These start switched on, so a build year
# alone produces a real answer; the other 37 start at "not in my house" and are
# added by anyone who has them. Defaulting all 49 on would open with a wall of
# rows about septic fields and well pumps for a buyer with neither.
COMMON = [
    "Roof - asphalt shingle, architectural",
    "HVAC condenser - outdoor unit",
    "HVAC air handler / furnace",
    "Ductwork",
    "Water heater - tank",
    "Water heater anode rod",
    "Windows - whole house",
    "Exterior paint",
    "Exterior caulk & sealants",
    "Main electrical panel",
    "Refrigerator",
    "Dishwasher",
]

# Shortened where the planner's name is longer than the line it sits on here.
# The planner's dropdown has to disambiguate 49 rows; this page shows them
# grouped, so the group does half the work.
SHORTER = {
    "HVAC condenser - outdoor unit": "A/C condenser, the outdoor unit",
    "HVAC air handler / furnace": "Air handler or furnace",
    "Windows - whole house": "Windows, whole house",
    "Exterior caulk & sealants": "Exterior caulk and sealants",
    "Water heater - tank": "Water heater, tank",
    "Water heater - tankless": "Water heater, tankless",
    "Roof - asphalt shingle, 3-tab": "Roof, 3-tab shingle",
    "Roof - asphalt shingle, architectural": "Roof, architectural shingle",
    "Roof - metal": "Roof, metal",
    "Roof - tile, concrete or clay": "Roof, tile",
    "Siding - vinyl": "Siding, vinyl",
    "Siding - fiber cement": "Siding, fiber cement",
    "Flooring - carpet": "Carpet",
    "Flooring - luxury vinyl plank": "Vinyl plank flooring",
    "Flooring - hardwood refinish": "Hardwood, refinish",
    "Supply lines - braided": "Braided supply lines",
    "Microwave - over-range": "Microwave, over-range",
    "Deck - wood": "Deck, wood",
    "Fence - wood": "Fence, wood",
    "Driveway - concrete": "Driveway, concrete",
    "Smoke & CO detectors": "Smoke and CO detectors",
}

# The order groups appear in, roughly most expensive first. Anything in SYSTEMS
# with a category not named here fails the build rather than being dropped.
GROUPS = ["Roof & Structure", "HVAC", "Plumbing", "Electrical", "Appliances",
          "Interior", "Outdoor"]


def rows():
    """Every system, with the name this tool shows and whether it starts on."""
    out = []
    unknown = sorted(set(row[1] for row in SYSTEMS) - set(GROUPS))
    if unknown:
        raise SystemExit(
            "planner_data has categories this tool does not group: " + ", ".join(unknown))
    for group in GROUPS:
        for system, category, life, life_range, _c, _cr, _t, exposure, _s in SYSTEMS:
            if category != group:
                continue
            out.append({
                "name": SHORTER.get(system, system),
                "life": life,
                "range": life_range,
                "group": group,
                "exposure": exposure == "Yes",
                "common": system in COMMON,
            })
    missing = set(COMMON) - set(row[0] for row in SYSTEMS)
    if missing:
        raise SystemExit("COMMON names rows that are not in planner_data: "
                         + ", ".join(sorted(missing)))
    return out


def escape(text):
    return (text.replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;").replace('"', "&quot;"))


def groups_html(items):
    out, index, seen = [], 0, None
    for row in items:
        if row["group"] != seen:
            if seen is not None:
                out.append("      </ul>\n    </section>")
            seen = row["group"]
            out.append(
                '    <section class="group">\n'
                '      <h3>{0}</h3>\n'
                '      <ul class="items">'.format(escape(seen)))
        out.append(
            '        <li class="item{extra}">\n'
            '          <div class="item-head">\n'
            '            <span class="item-name">{name}</span>\n'
            '            <span class="item-life">{life} yrs</span>\n'
            '          </div>\n'
            '          <div class="item-controls">\n'
            '            <label class="sr-only" for="mode-{i}">What you know about the '
            '{name}</label>\n'
            '            <select id="mode-{i}" class="mode" data-index="{i}">\n'
            '              <option value="schedule"{on}>Replaced on schedule</option>\n'
            '              <option value="original">Never replaced</option>\n'
            '              <option value="mid">Roughly half way through</option>\n'
            '              <option value="known">I know the year</option>\n'
            '              <option value="skip"{off}>Not in my house</option>\n'
            '            </select>\n'
            '            <label class="sr-only" for="year-{i}">Year the {name} went in</label>\n'
            '            <input id="year-{i}" class="year" data-index="{i}" type="number"\n'
            '                   inputmode="numeric" placeholder="Year" min="1850" max="2100" '
            'hidden>\n'
            '          </div>\n'
            '        </li>'.format(
                i=index, name=escape(row["name"]), life=row["life"],
                extra="" if row["common"] else " item--extra",
                on=" selected" if row["common"] else "",
                off="" if row["common"] else " selected"))
        index += 1
    out.append("      </ul>\n    </section>")
    return "\n".join(out)


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{product}</title>

<!-- This file talks to nothing. 'none' by default with no connect-src means a
     script in here cannot reach the network even if one were added, which is
     the enforceable version of the promise on the page: what you type about
     your house stays on your machine. -->
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; base-uri 'none'; form-action 'none'">
<meta name="robots" content="noindex, nofollow">

<style>
{theme}

  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; background: var(--bg); color: var(--ink);
    font: 17px/1.65 ui-serif, Georgia, "Iowan Old Style", "Times New Roman", serif;
    -webkit-font-smoothing: antialiased;
  }}
  .wrap {{ max-width: 48rem; margin: 0 auto; padding: 0 1.35rem; }}
  .sr-only {{
    position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px;
    overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; border: 0;
  }}

  header {{ background: var(--deep); color: var(--on-deep); padding: 2.75rem 0 2.25rem; }}
  header .eyebrow {{
    font: 600 11px/1 ui-sans-serif, system-ui, sans-serif;
    letter-spacing: .14em; text-transform: uppercase; color: var(--sand); margin: 0;
  }}
  header h1 {{
    font-size: clamp(1.9rem, 5vw, 2.5rem); line-height: 1.1;
    margin: .9rem 0 .8rem; letter-spacing: -.02em; color: #fff;
  }}
  header p {{ color: var(--on-deep-mute); margin: 0; max-width: 34rem; }}

  main {{ padding: 2.25rem 0 0; }}
  h2 {{
    font: 700 clamp(1.25rem, 3.5vw, 1.6rem)/1.2 ui-serif, Georgia, serif;
    margin: 0 0 .55rem; letter-spacing: -.015em;
  }}
  .lede {{ color: var(--muted); font-size: .95rem; margin: 0 0 1.4rem; max-width: 34rem; }}

  .card {{
    background: var(--paper); border: 1px solid var(--rule); border-radius: 3px;
    box-shadow: var(--shadow); padding: 1.4rem 1.5rem 1.5rem; margin: 0 0 1.75rem;
  }}

  .setup {{ display: flex; gap: 1.25rem; flex-wrap: wrap; }}
  .field label {{
    font: 600 .93rem/1.4 ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
    display: block; margin-bottom: .35rem;
  }}
  /* --muted rather than --rule for the boundary: a --rule hairline on --paper is
     under 3:1 and the control vanishes until it takes focus. WCAG 1.4.11. */
  input, select, button {{
    font: 400 15px/1.2 ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
    padding: .7rem .8rem; border-radius: 2px;
    border: 1px solid var(--muted); background: var(--bg); color: var(--ink);
    max-width: 100%;
  }}
  input:focus-visible, select:focus-visible, button:focus-visible {{
    outline: 2px solid var(--accent); outline-offset: 1px; border-color: var(--accent);
  }}
  .field input {{ width: 8rem; }}
  .field select {{ width: 12rem; }}
  .field .why {{
    font: 400 .82rem/1.5 ui-sans-serif, system-ui, sans-serif;
    color: var(--muted); margin: .35rem 0 0; max-width: 15rem;
  }}

  .group {{ border-top: 1px solid var(--rule); padding-top: 1.15rem; margin-top: 1.35rem; }}
  .group:first-of-type {{ border-top: 0; padding-top: 0; margin-top: 0; }}
  .group h3 {{
    font: 700 .82rem/1 ui-sans-serif, system-ui, sans-serif;
    letter-spacing: .13em; text-transform: uppercase; color: var(--accent);
    margin: 0 0 .85rem;
  }}
  .items {{ list-style: none; margin: 0; padding: 0; }}
  .item {{ border-top: 1px solid var(--rule-soft); padding: .8rem 0; }}
  .item:first-child {{ border-top: 0; padding-top: 0; }}
  .item--extra {{ display: none; }}
  body.show-extras .item--extra {{ display: block; }}
  .item-head {{ display: flex; justify-content: space-between; gap: .75rem; align-items: baseline; }}
  .item-name {{
    font: 600 .97rem/1.4 ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
  }}
  .item-life {{
    font: 400 12px/1.4 ui-sans-serif, system-ui, sans-serif;
    color: var(--muted); white-space: nowrap;
  }}
  .item-controls {{ display: flex; gap: .5rem; margin-top: .5rem; flex-wrap: wrap; }}
  .item-controls select {{ flex: 1 1 15rem; min-width: 0; }}
  .item-controls .year {{ width: 7rem; }}

  .btn {{
    font: 600 14px/1 ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
    padding: .8rem 1.2rem; border-radius: 2px; cursor: pointer;
    background: var(--accent); border: 1px solid var(--accent); color: var(--paper);
    -webkit-appearance: none; appearance: none; transition: filter .15s ease;
  }}
  .btn:hover {{ filter: brightness(1.09); }}
  .btn--quiet {{ background: transparent; color: var(--accent); }}
  .toolbar {{ display: flex; gap: .6rem; flex-wrap: wrap; margin: 1.4rem 0 0; }}

  .results {{ margin: 0 0 1.75rem; }}
  .verdict {{
    font: 700 clamp(1.15rem, 3vw, 1.4rem)/1.35 ui-serif, Georgia, serif; margin: 0 0 1rem;
  }}
  .verdict .big {{ color: var(--must); }}
  .nudge {{
    font: 400 .92rem/1.6 ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
    color: var(--muted); margin: -.4rem 0 1.1rem; max-width: 34rem;
    border-left: 3px solid var(--sand); padding-left: .85rem;
  }}
  .rows {{ list-style: none; margin: 0; padding: 0; }}
  .row {{
    display: flex; align-items: baseline; gap: .75rem; flex-wrap: wrap;
    border-top: 1px solid var(--rule-soft); padding: .7rem 0;
  }}
  .row:first-child {{ border-top: 0; }}
  .row .what {{
    flex: 1 1 12rem;
    font: 600 .97rem/1.4 ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
  }}
  .row .when {{ font: 400 .89rem/1.4 ui-sans-serif, system-ui, sans-serif; color: var(--muted); }}
  .tag {{
    font: 700 10px/1 ui-sans-serif, system-ui, sans-serif;
    letter-spacing: .12em; text-transform: uppercase;
    border: 1px solid currentColor; border-radius: 2px; padding: .32rem .45rem;
    white-space: nowrap;
  }}
  .tag--overdue {{ color: var(--must); }}
  .tag--soon {{ color: var(--sand); }}
  .tag--watch {{ color: var(--should); }}
  .tag--ok {{ color: var(--above); }}
  .estimated {{
    font: 400 11px/1 ui-sans-serif, system-ui, sans-serif;
    color: var(--muted); letter-spacing: .06em; text-transform: uppercase;
  }}
  .empty {{ color: var(--muted); font-size: .95rem; margin: 0; }}

  .fine {{
    font: 400 .86rem/1.6 ui-sans-serif, system-ui, sans-serif;
    color: var(--muted); max-width: 35rem;
  }}

  footer {{
    background: var(--deep); color: var(--on-deep-mute);
    margin-top: 2.5rem; padding: 2.25rem 0 2.75rem; font-size: .86rem;
  }}
  footer p {{ margin: 0 0 .7rem; max-width: 35rem; }}
  footer .disclaimer {{ font-style: italic; }}
  footer .mark {{
    font: 600 11px/1 ui-sans-serif, system-ui, sans-serif;
    letter-spacing: .12em; text-transform: uppercase; color: var(--sand); margin: 0 0 .9rem;
  }}
  footer .version {{
    font: 600 11px/1 ui-sans-serif, system-ui, sans-serif;
    letter-spacing: .12em; opacity: .55; margin: 0;
  }}

  /* Printing is the only way anything leaves this file, so it is worth doing
     properly: the answer, on paper, with nothing else on it. */
  @media print {{
    body {{ background: #fff; color: #000; font-size: 11pt; }}
    header {{ background: none; color: #000; padding: 0 0 .6rem; border-bottom: 1px solid #000; }}
    header h1 {{ color: #000; font-size: 18pt; margin: .2rem 0; }}
    header p, .setup, .card, .toolbar, footer .mark, .noprint {{ display: none !important; }}
    .results {{ margin: 1rem 0 0; }}
    .tag {{ border-color: #000; color: #000; }}
    .row {{ border-color: #bbb; }}
    footer {{ background: none; color: #000; margin-top: 1.5rem; padding: .6rem 0 0;
              border-top: 1px solid #000; }}
    .print-only {{ display: block !important; }}
  }}
  .print-only {{ display: none; }}
</style>
</head>
<body>

<header>
  <div class="wrap">
    <p class="eyebrow">Gulf Coast Home Maintenance</p>
    <h1>{product}</h1>
    <p>
      Type the year your house was built. That is the only thing you have to
      know. Everything else starts on the kindest assumption available and you
      correct it line by line.
    </p>
  </div>
</header>

<main class="wrap">

  <noscript>
    <div class="card">
      <h2>This needs JavaScript switched on</h2>
      <p class="fine">
        The arithmetic runs inside this file, which is why nothing you type
        goes anywhere. With scripts off there is nothing to run it. If you
        opened this from a download folder and it looks empty, try dragging it
        onto a browser window instead.
      </p>
    </div>
  </noscript>

  <div class="card">
    <div class="setup">
      <div class="field">
        <label for="built">Year built</label>
        <input id="built" type="number" inputmode="numeric" placeholder="1998"
               min="1850" max="2100">
        <p class="why">On your county appraisal record if you do not have it.</p>
      </div>
      <div class="field">
        <label for="region">Where you are</label>
        <select id="region">
{regions}
        </select>
        <p class="why">Adjusts the weather-driven lifespans. Heat, humidity and UV
        age a roof. They do nothing to a dishwasher.</p>
      </div>
    </div>
  </div>

  <section class="results" id="results" aria-live="polite">
    <p class="empty">Put a year built in above and your list appears here.</p>
  </section>

  <div class="card noprint">
    <h2>Correct anything you actually know</h2>
    <p class="lede">
      Every line starts at <strong>replaced on schedule</strong>, which assumes
      whoever owned it before you kept up with it. That is the most generous of
      the three guesses, on purpose: the list above is the best case, and the
      real one is rarely better than the best case. Switch anything you know has
      never been touched to <strong>never replaced</strong> and watch what
      happens.
    </p>
    <div class="toolbar">
      <button class="btn btn--quiet" id="toggle-extras" type="button" aria-expanded="false">
        Show the other {extras} systems
      </button>
      <button class="btn" id="print" type="button">Print my list</button>
    </div>
    <div style="margin-top:1.5rem">
{groups}
    </div>
  </div>

  <p class="fine noprint">
    Lifespans are Gulf South figures adjusted for where you said you are. They
    run shorter than national averages because heat, humidity and hard UV age a
    house faster, and they are the same numbers printed in the Gulf Coast Home
    Maintenance Kit. They are guidelines rather than guarantees: a
    well-maintained roof outlives a neglected one, and a bad one fails early.
  </p>

</main>

<footer>
  <div class="wrap">
    <p class="mark">{domain}</p>
    <p class="print-only"><strong>{product}</strong>, {domain}</p>
    <p class="disclaimer">{disclaimer}</p>
    <p class="fine noprint">
      This file works offline and sends nothing anywhere. Everything you type
      about your house stays on this machine, which also means it is not saved:
      close the tab and it is gone. Print your list, or keep it in the reserve
      planner spreadsheet, which is built to be kept and updated.
    </p>
    <p>{license}</p>
    <p class="version">v{version}</p>
  </div>
</footer>

<script>
(function () {{
  'use strict';

  var SYSTEMS = {systems};
  var REGIONS = {regions_js};
  var NOW = new Date().getFullYear();

  var built = document.getElementById('built');
  var region = document.getElementById('region');
  var results = document.getElementById('results');
  var modes = Array.prototype.slice.call(document.querySelectorAll('.mode'));
  var years = Array.prototype.slice.call(document.querySelectorAll('.year'));

  function lifeOf(system) {{
    var factor = REGIONS[region.value] || 1;
    return system.exposure ? Math.round(system.life * factor) : system.life;
  }}

  // The same three estimates the planner runs, and the same order of
  // preference: a year you actually know always wins.
  function installYear(mode, life, buildYear, known) {{
    if (mode === 'known') {{
      return (known && known > 1849 && known <= NOW + 1) ? known : null;
    }}
    if (mode === 'mid') {{ return Math.max(buildYear, NOW - Math.round(life / 2)); }}
    if (mode === 'original') {{ return buildYear; }}
    // On schedule: step forward from the build year in whole lifespans and stop
    // at the last one that has already happened. A house younger than a single
    // cycle lands back on its build year, which is right.
    return buildYear + Math.floor(Math.max(NOW - buildYear, 0) / life) * life;
  }}

  function status(remaining) {{
    if (remaining <= 0) {{ return ['overdue', 'Overdue']; }}
    if (remaining <= 2) {{ return ['soon', 'Due soon']; }}
    if (remaining <= 5) {{ return ['watch', 'Watch']; }}
    return ['ok', 'OK'];
  }}

  function whenText(remaining, dueYear) {{
    if (remaining === 0) {{ return 'due this year'; }}
    if (remaining < 0) {{
      var over = -remaining;
      return 'due in ' + dueYear + ', ' + over + (over === 1 ? ' year' : ' years') + ' ago';
    }}
    return 'due around ' + dueYear + ', ' + remaining +
           (remaining === 1 ? ' year' : ' years') + ' away';
  }}

  function escapeHtml(text) {{
    return String(text).replace(/[&<>"]/g, function (ch) {{
      return {{'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}}[ch];
    }});
  }}

  function render() {{
    var buildYear = parseInt(built.value, 10);
    if (!buildYear || buildYear < 1850 || buildYear > NOW + 1) {{
      results.innerHTML =
        '<p class="empty">Put a year built in above and your list appears here.</p>';
      return;
    }}

    var found = [];
    var untouched = true;
    for (var i = 0; i < SYSTEMS.length; i++) {{
      var mode = modes[i].value;
      var expected = SYSTEMS[i].common ? 'schedule' : 'skip';
      if (mode !== expected) {{ untouched = false; }}
      if (mode === 'skip') {{ continue; }}
      var life = lifeOf(SYSTEMS[i]);
      var installed = installYear(mode, life, buildYear, parseInt(years[i].value, 10));
      if (installed === null) {{ continue; }}
      found.push({{
        name: SYSTEMS[i].name,
        due: installed + life,
        remaining: installed + life - NOW,
        estimated: mode !== 'known'
      }});
    }}

    if (!found.length) {{
      results.innerHTML = '<p class="empty">Nothing is switched on. Turn a line back on ' +
        'below, or put a year in for anything set to <em>I know the year</em>.</p>';
      return;
    }}

    found.sort(function (a, b) {{ return a.remaining - b.remaining; }});
    var pressing = found.filter(function (r) {{ return r.remaining <= 2; }}).length;
    var overdue = found.filter(function (r) {{ return r.remaining <= 0; }}).length;

    var verdict;
    if (pressing === 0) {{
      verdict = '<p class="verdict">Nothing on your list is past due. The next one up is ' +
        'the ' + escapeHtml(found[0].name.toLowerCase()) + '.</p>';
    }} else {{
      verdict = '<p class="verdict"><span class="big">' + pressing + '</span> of ' +
        found.length + ' are overdue or due within two years.</p>';
    }}

    // "Replaced on schedule" cannot produce an overdue item: by definition it
    // dates everything to its most recent cycle. So on an uncorrected list the
    // absence of red means the assumption held, not that the house is fine, and
    // saying so is the difference between a tool and a toy.
    if (!overdue && untouched) {{
      verdict += '<p class="nudge noprint">That is with every line assumed to have been ' +
        'replaced on schedule. If you know the roof or the water heater has never been ' +
        'touched since the house was built, set those to <strong>never replaced</strong> ' +
        'below.</p>';
    }}

    results.innerHTML = verdict + '<ul class="rows">' + found.map(function (item) {{
      var state = status(item.remaining);
      return '<li class="row">' +
        '<span class="tag tag--' + state[0] + '">' + state[1] + '</span>' +
        '<span class="what">' + escapeHtml(item.name) + '</span>' +
        '<span class="when">' + whenText(item.remaining, item.due) +
        (item.estimated ? ' <span class="estimated">estimated</span>' : '') +
        '</span></li>';
    }}).join('') + '</ul>';
  }}

  built.addEventListener('input', render);
  region.addEventListener('change', render);
  modes.forEach(function (select, index) {{
    select.addEventListener('change', function () {{
      years[index].hidden = select.value !== 'known';
      if (select.value === 'known' && !years[index].value) {{ years[index].focus(); }}
      render();
    }});
  }});
  years.forEach(function (input) {{ input.addEventListener('input', render); }});

  var toggle = document.getElementById('toggle-extras');
  toggle.addEventListener('click', function () {{
    var open = document.body.classList.toggle('show-extras');
    toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    toggle.textContent = open ? 'Hide the other {extras} systems'
                              : 'Show the other {extras} systems';
  }});

  document.getElementById('print').addEventListener('click', function () {{ window.print(); }});
}})();
</script>

</body>
</html>
"""


def build():
    items = rows()
    with open(THEME, encoding="utf-8") as handle:
        theme = handle.read()

    options = "\n".join(
        '          <option value="{0}"{1}>{0}</option>'.format(
            escape(name), " selected" if name == REGIONS[0][0] else "")
        for name, _cost, _life, _why in REGIONS)

    payload = json.dumps(
        [{"name": row["name"], "life": row["life"], "exposure": row["exposure"],
          "common": row["common"]} for row in items],
        ensure_ascii=False).replace("</", "<\\/")
    factors = json.dumps(
        dict((name, life) for name, _cost, life, _why in REGIONS),
        ensure_ascii=False).replace("</", "<\\/")

    html = TEMPLATE.format(
        product=escape(PRODUCT),
        domain=DOMAIN,
        theme=theme,
        regions=options,
        regions_js=factors,
        groups=groups_html(items),
        systems=payload,
        extras=sum(1 for row in items if not row["common"]),
        disclaimer=escape(DISCLAIMER),
        license=escape(LICENSE),
        version=VERSION,
    )

    folder = os.path.dirname(OUT)
    if not os.path.isdir(folder):
        os.makedirs(folder)
    with open(OUT, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(html)

    size = os.path.getsize(OUT)
    print("{0}  {1} systems in {2} groups, {3} on by default, {4} KB, one file"
          .format(OUT, len(items), len(GROUPS),
                  sum(1 for row in items if row["common"]), size // 1024))
    return OUT


if __name__ == "__main__":
    build()
