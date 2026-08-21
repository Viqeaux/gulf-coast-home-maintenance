"""Builds the free calculator, the teaser for the reserve planner.

    python build_calculator.py

Writes `docs/calculator/index.html`. Four systems, one input, an answer. The
arithmetic runs in the visitor's browser, which is why nothing typed into it
leaves their machine and why the page adds no origin to the site's policy.

**It is the only page on the site that gives before it asks.** Everything else
wants a subscribe, a signup or a sale. That is what makes it the one worth
linking and pinning, and the shop's constraint is traffic rather than
conversion.

**Four, and no more.** It went twelve, then four. Twelve was the worst of both:
too much to be a teaser and too little to be a product. Four is the roof, the
a/c, the water heater and the furnace, all checkable in fifteen seconds, and
enough that somebody who gets a red row wants the rest.

**What it withholds is legible rather than arbitrary.** No region picker, no
print, and forty-five systems it does not carry. A visitor can see the shape of
what they are not getting, which is what a teaser is for.

**The paid half of this used to be a second HTML file** and is now the
`Quick Check` tab of the planner workbook. Chad's call, 2026-08-16: a raw
`.html` attachment could not be relied on to open on a phone, and a tool that
will not open is worth nothing. Nothing was lost in the move except a delivery
problem. The `installYear` logic here is the same model the workbook runs, so
somebody who tries this and then buys never finds the two disagreeing about the
same roof; `FREE_FOUR` is checked to be a subset of `planner_data.COMMON`, which
is the twelve the Quick Check tab is built from.

**No dollar amounts.** Lifespans are the verified half and costs are not, and a
wrong figure on a public page has nobody to email about it. It is also the
commercial line: this answers what and when, the workbook answers what it costs.
"""

import json
import os

from build_calendars import VERSION
from planner_data import COMMON, SYSTEMS

FREE_OUT = os.path.join("docs", "calculator", "index.html")

# The planner's listing. Paste it in and the buy slot becomes a buy button;
# until then it holds the signup. Same trade as SHOP_URL at the bottom of
# docs/index.html before the kit was purchasable.
BUNDLE_URL = ""

DOMAIN = "gulfcoasthomemaintenance.com"

DISCLAIMER = ("General maintenance guidance, not a substitute for a licensed "
              "inspector, contractor, or your insurance policy terms.")

# Shortened for the page. The workbook's names have to disambiguate 49 rows in a
# dropdown; these four only have to be readable on a phone.
SHORTER = {
    "Roof - asphalt shingle, architectural": "Roof, architectural shingle",
    "HVAC condenser - outdoor unit": "A/C condenser, the outdoor unit",
    "HVAC air handler / furnace": "Air handler or furnace",
    "Water heater - tank": "Water heater, tank",
}


def escape(text):
    return (text.replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;").replace('"', "&quot;"))


# The arithmetic, shared verbatim by the download and the free page.
#
# Both are inserted into a .format() template, so this string carries plain
# single braces and gets substituted rather than formatted. The point of
# sharing it is that a visitor who tries the free page and then buys must never
# find the two disagreeing about the same roof. Two copies of four functions
# would drift on the first fix.
ENGINE_JS = """
  // The same three estimates the planner runs, and the same order of
  // preference: a year you actually know always wins.
  function installYear(mode, life, buildYear, known) {
    if (mode === 'known') {
      return (known && known > 1849 && known <= NOW + 1) ? known : null;
    }
    if (mode === 'mid') { return Math.max(buildYear, NOW - Math.round(life / 2)); }
    if (mode === 'original') { return buildYear; }
    // On schedule: step forward from the build year in whole lifespans and stop
    // at the last one that has already happened. A house younger than a single
    // cycle lands back on its build year, which is right.
    return buildYear + Math.floor(Math.max(NOW - buildYear, 0) / life) * life;
  }

  function status(remaining) {
    if (remaining <= 0) { return ['overdue', 'Overdue']; }
    if (remaining <= 2) { return ['soon', 'Due soon']; }
    if (remaining <= 5) { return ['watch', 'Watch']; }
    return ['ok', 'OK'];
  }

  function whenText(remaining, dueYear) {
    if (remaining === 0) { return 'due this year'; }
    if (remaining < 0) {
      var over = -remaining;
      return 'due in ' + dueYear + ', ' + over + (over === 1 ? ' year' : ' years') + ' ago';
    }
    return 'due around ' + dueYear + ', ' + remaining +
           (remaining === 1 ? ' year' : ' years') + ' away';
  }

  function escapeHtml(text) {
    return String(text).replace(/[&<>"]/g, function (ch) {
      return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[ch];
    });
  }
""".rstrip()


# The free page's four. Deliberately the four biggest and most recognizable,
# and deliberately nowhere near a useful list: it exists to be worth linking and
# pinning, and to be obviously less than the file it points at. Any of these can
# be checked in about fifteen seconds, which is the whole idea.
#
# It must stay a strict subset of COMMON, so a system can never appear free with
# one lifespan and paid with another. `free_rows()` enforces that.
FREE_FOUR = [
    "Roof - asphalt shingle, architectural",
    "HVAC condenser - outdoor unit",
    "Water heater - tank",
    "HVAC air handler / furnace",
]


def free_rows():
    table = dict((row[0], row) for row in SYSTEMS)
    stray = [name for name in FREE_FOUR if name not in COMMON]
    if stray:
        raise SystemExit("FREE_FOUR must be a subset of COMMON, these are not: "
                         + ", ".join(stray))
    out = []
    for name in FREE_FOUR:
        if name not in table:
            raise SystemExit("FREE_FOUR names a row that is not in planner_data: " + name)
        out.append({"name": SHORTER.get(name, name), "life": table[name][2]})
    return out


def free_items_html(items):
    out = []
    for index, row in enumerate(items):
        out.append(
            '        <li class="item">\n'
            '          <div class="item-head">\n'
            '            <span class="item-name">{name}</span>\n'
            '            <span class="item-life">{life} yrs typical</span>\n'
            '          </div>\n'
            '          <div class="item-controls">\n'
            '            <label class="sr-only" for="mode-{i}">What you know about the '
            '{name}</label>\n'
            '            <select id="mode-{i}" class="mode" data-index="{i}">\n'
            '              <option value="schedule" selected>Replaced on schedule</option>\n'
            '              <option value="original">Never replaced</option>\n'
            '              <option value="mid">Roughly half way through</option>\n'
            '              <option value="known">I know the year</option>\n'
            '              <option value="skip">Not in my house</option>\n'
            '            </select>\n'
            '            <label class="sr-only" for="year-{i}">Year the {name} went in</label>\n'
            '            <input id="year-{i}" class="year" data-index="{i}" type="number"\n'
            '                   inputmode="numeric" placeholder="Year" min="1850" max="2100" '
            'hidden>\n'
            '          </div>\n'
            '        </li>'.format(i=index, name=escape(row["name"]), life=row["life"]))
    return "\n".join(out)


FREE_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>What in Your House Is on Borrowed Time</title>
<meta name="description" content="Free. Enter the year your house was built and see whether the roof, the a/c, the water heater or the furnace are already past their expected life on the Gulf Coast.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://{domain}/calculator/">

<meta property="og:title" content="What in your house is on borrowed time">
<meta property="og:description" content="Enter one number and find out whether four of the most expensive things in your house are already past due. Free, no signup, timed for the Gulf Coast.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://{domain}/calculator/">
<meta property="og:site_name" content="Gulf Coast Home Maintenance">
<meta property="og:image" content="https://{domain}/img/hero-1600.jpg">
<meta property="og:image:width" content="1600">
<meta property="og:image:height" content="900">
<meta property="og:image:alt" content="A live oak hung with Spanish moss over the roof of a Gulf Coast house at sunset.">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0e2429">

<!-- Pages cannot set headers, so the policy travels in the document. See the
     longer note in docs/index.html for why 'unsafe-inline' is here, why
     frame-ancestors is not, and why Google is the only third party named.

     This page tells the visitor, in the body text below, that nothing they type
     leaves their machine. That is still true and it has to stay true: analytics
     here counts the visit, not the answer. Sending a build year, a system name
     or a computed figure to Google as an event parameter would make the page
     lie, however useful the data looked. The arithmetic stays local. -->
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline' https://www.googletagmanager.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: https://*.google-analytics.com https://*.googletagmanager.com; font-src 'self'; connect-src 'self' https://*.google-analytics.com https://*.analytics.google.com https://*.googletagmanager.com; form-action https://assets.mailerlite.com; frame-src 'self'; base-uri 'none'; object-src 'none'">
<meta name="referrer" content="strict-origin-when-cross-origin">

<!-- One Measurement ID for the whole site, in docs/analytics.js. -->
<script src="../analytics.js"></script>

<link rel="icon" href="../favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="../icon-180.png">
<link rel="stylesheet" href="../theme.css">
<style>
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; background: var(--bg); color: var(--ink);
    font: 17px/1.65 ui-serif, Georgia, "Iowan Old Style", "Times New Roman", serif;
    -webkit-font-smoothing: antialiased;
  }}
  .wrap {{ max-width: 46rem; margin: 0 auto; padding: 0 1.35rem; }}
  a {{ color: var(--accent); }}
  .sr-only {{
    position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px;
    overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; border: 0;
  }}

  header {{ background: var(--deep); color: var(--on-deep); padding: 3rem 0 2.5rem; }}
  header a.back {{
    font: 600 11px/1 ui-sans-serif, system-ui, sans-serif;
    letter-spacing: .14em; text-transform: uppercase;
    color: var(--sand); text-decoration: none;
  }}
  header a.back:hover {{ text-decoration: underline; }}
  header h1 {{
    font-size: clamp(1.9rem, 5vw, 2.6rem); line-height: 1.1;
    margin: 1rem 0 .9rem; letter-spacing: -.02em; color: #fff;
  }}
  header p {{ color: var(--on-deep-mute); margin: 0; max-width: 34rem; }}

  main {{ padding: 2.5rem 0 0; }}
  h2 {{
    font: 700 clamp(1.3rem, 3.5vw, 1.7rem)/1.2 ui-serif, Georgia, serif;
    margin: 0 0 .6rem; letter-spacing: -.015em;
  }}
  .lede {{ color: var(--muted); font-size: .96rem; margin: 0 0 1.5rem; max-width: 34rem; }}

  .card {{
    background: var(--paper); border: 1px solid var(--rule); border-radius: 3px;
    box-shadow: var(--shadow); padding: 1.5rem 1.5rem 1.6rem; margin: 0 0 2rem;
  }}

  .built {{ display: flex; align-items: flex-end; gap: .9rem; flex-wrap: wrap; }}
  .built label {{
    font: 600 .95rem/1.4 ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
    display: block; margin-bottom: .35rem;
  }}
  /* --muted rather than --rule for the boundary: a --rule hairline on --paper is
     under 3:1 and the control vanishes until it takes focus. WCAG 1.4.11. */
  input, select {{
    font: 400 15px/1.2 ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
    padding: .7rem .8rem; border-radius: 2px;
    border: 1px solid var(--muted); background: var(--bg); color: var(--ink);
    max-width: 100%;
  }}
  input:focus-visible, select:focus-visible {{
    outline: 2px solid var(--accent); outline-offset: 1px; border-color: var(--accent);
  }}
  .built input {{ width: 8rem; }}
  .built .hint {{
    font: 400 .86rem/1.5 ui-sans-serif, system-ui, sans-serif;
    color: var(--muted); margin: 0; flex: 1 1 14rem; min-width: 0;
  }}

  .items {{ list-style: none; margin: 0; padding: 0; }}
  .item {{ border-top: 1px solid var(--rule-soft); padding: .85rem 0; }}
  .item:first-child {{ border-top: 0; padding-top: 0; }}
  .item-head {{ display: flex; justify-content: space-between; gap: .75rem; align-items: baseline; }}
  .item-name {{
    font: 600 .98rem/1.4 ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
  }}
  .item-life {{
    font: 400 12px/1.4 ui-sans-serif, system-ui, sans-serif;
    color: var(--muted); white-space: nowrap;
  }}
  .item-controls {{ display: flex; gap: .5rem; margin-top: .5rem; flex-wrap: wrap; }}
  .item-controls select {{ flex: 1 1 15rem; min-width: 0; }}
  .item-controls .year {{ width: 7rem; }}

  .results {{ margin: 0 0 2rem; }}
  .verdict {{
    font: 700 clamp(1.15rem, 3vw, 1.4rem)/1.35 ui-serif, Georgia, serif; margin: 0 0 1rem;
  }}
  .verdict .big {{ color: var(--must); }}
  .nudge {{
    font: 400 .93rem/1.6 ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
    color: var(--muted); margin: -.4rem 0 1.1rem; max-width: 33rem;
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
    font: 600 .98rem/1.4 ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
  }}
  .row .when {{ font: 400 .9rem/1.4 ui-sans-serif, system-ui, sans-serif; color: var(--muted); }}
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

  .next {{
    background: var(--paper-2); border-top: 1px solid var(--rule);
    margin-top: 1rem; padding: 3rem 0;
  }}
  .next h2 {{ margin-bottom: .7rem; }}
  .next p {{ color: var(--muted); font-size: .96rem; max-width: 33rem; margin: 0 0 1.2rem; }}
  .btn {{
    display: inline-block;
    font: 600 14px/1 ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
    text-decoration: none; padding: .85rem 1.3rem; border-radius: 2px;
    background: var(--accent); border: 1px solid var(--accent); color: var(--paper);
    cursor: pointer; -webkit-appearance: none; appearance: none;
    transition: filter .15s ease;
  }}
  .btn:hover {{ filter: brightness(1.09); text-decoration: none; }}
  .btn:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 2px; }}
  .btn--quiet {{ background: transparent; color: var(--accent); }}
  .actions {{ display: flex; gap: .6rem; flex-wrap: wrap; margin: 0 0 1.4rem; }}

  .signup {{ margin: 0; }}
  .signup-row {{ display: flex; gap: .5rem; flex-wrap: wrap; max-width: 27rem; }}
  .signup-row input {{ flex: 1 1 12rem; min-width: 0; }}
  .signup-note {{
    font: 400 12.5px/1.5 ui-sans-serif, system-ui, sans-serif;
    color: var(--muted); margin: .75rem 0 0; max-width: 32rem;
  }}
  .signup-done {{
    font: 400 .95rem/1.6 ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
    color: var(--muted); margin: 0;
  }}
  .signup-done strong {{ display: block; color: var(--accent); margin-bottom: .2rem; }}
  .tail-signup {{ margin-top: 2.25rem; padding-top: 1.9rem; border-top: 1px solid var(--rule); }}
  .tail-signup h3 {{
    font: 700 1.05rem/1.3 ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif;
    margin: 0 0 .4rem;
  }}
  @media (max-width: 26rem) {{
    .signup-row input, .signup-row .btn {{ flex: 1 1 100%; }}
  }}

  .fine {{
    font: 400 .87rem/1.6 ui-sans-serif, system-ui, sans-serif;
    color: var(--muted); max-width: 34rem;
  }}

  footer {{
    background: var(--deep); color: var(--on-deep-mute);
    padding: 2.5rem 0 3rem; font-size: .87rem;
  }}
  footer p {{ margin: 0 0 .8rem; max-width: 34rem; }}
  footer .disclaimer {{ font-style: italic; }}
  footer .foot-links {{
    display: flex; flex-wrap: wrap; gap: 1.25rem; margin-bottom: 1.1rem;
    font: 400 .87rem/1 ui-sans-serif, system-ui, sans-serif;
  }}
  footer .foot-links a {{ color: var(--sand); text-decoration: none; }}
  footer .foot-links a:hover {{ text-decoration: underline; }}
  footer .version {{
    font: 600 11px/1 ui-sans-serif, system-ui, sans-serif;
    letter-spacing: .12em; opacity: .55; margin: 0;
  }}
</style>
</head>
<body>

<header>
  <div class="wrap">
    <a class="back" href="../">&#8592; Gulf Coast Home Maintenance</a>
    <h1>What in your house is on borrowed time</h1>
    <p>
      Four of the most expensive things you own, and whether they are already
      past due. Type the year it was built. That is the only thing you have to
      know.
    </p>
  </div>
</header>

<main class="wrap">

  <noscript>
    <div class="card">
      <h2>This one needs JavaScript</h2>
      <p class="fine">
        The arithmetic runs in your browser, which is also why nothing you type
        here is sent anywhere. With scripts off there is nothing to run it. The
        <a href="../guides/">calendar contents</a> page works without it.
      </p>
    </div>
  </noscript>

  <div class="card">
    <div class="built">
      <div>
        <label for="built">What year was it built?</label>
        <input id="built" type="number" inputmode="numeric" placeholder="1998"
               min="1850" max="2100">
      </div>
      <p class="hint">
        On your county appraisal record if you do not have it to hand. Nothing
        you type leaves your browser.
      </p>
    </div>
  </div>

  <section class="results" id="results" aria-live="polite">
    <p class="empty">Put a build year in above and the answer appears here.</p>
  </section>

  <div class="card">
    <h2>Correct anything you actually know</h2>
    <p class="lede">
      All four start at <strong>replaced on schedule</strong>, which assumes
      whoever owned the house before you kept up with it. That is the most
      generous of the three guesses, on purpose. What it means is that the
      answer above is the best case, and the real one is rarely better than the
      best case.
    </p>
    <ul class="items">
{items}
    </ul>
  </div>

  <p class="fine">
    Lifespans are Gulf South figures. Heat, humidity and hard UV age a house
    faster than the national averages assume, and these are the same numbers
    printed in the kit. They are guidelines rather than guarantees: a
    well-maintained roof outlives a neglected one, and a bad one fails early.
  </p>

</main>

<section class="next">
  <div class="wrap">
    <h2>This is four of forty-nine</h2>
    <p>
      The full version is a spreadsheet. Its Quick Check tab is this, with all
      forty-nine systems and your own region instead of ours, and it answers
      from the same one number. The rest of the workbook is the part this page
      does not attempt: what each one costs, what it will cost in the year it
      actually breaks, and what to put aside every month so the money is there.
    </p>
    <p class="actions">
{buy}
      <a class="btn btn--quiet" href="../#edition">See the printable kit</a>
    </p>
    <p class="fine">
      There are also three free calendars of the small jobs that keep this list
      from getting shorter faster than it has to.
      <a href="../#calendars">Those are here.</a>
    </p>

    <div class="tail-signup" id="keep-posted">
      <h3>Hear about the next one</h3>
      <p>
        The spreadsheet above is not on sale yet. Leave your email and I'll
        tell you when it is, and when there's anything else new. That is all
        the list is for.
      </p>
      <form class="signup" method="post" target="ml-sink"
            action="https://assets.mailerlite.com/jsonp/2575029/forms/195731645629727806/subscribe">
        <div class="signup-row">
          <label class="sr-only" for="signup-email">Your email address</label>
          <input id="signup-email" type="email" name="fields[email]" required
                 autocomplete="email" placeholder="you@example.com">
          <button class="btn" type="submit">Keep me posted</button>
        </div>
        <!-- Honeypot, same as the home page. Off screen rather than hidden,
             disabled before submit so MailerLite never sees it. -->
        <div class="sr-only" aria-hidden="true">
          <label for="signup-website">Leave this field empty</label>
          <input id="signup-website" type="text" name="website" tabindex="-1" autocomplete="off">
        </div>
        <p class="signup-note">
          Only when there's something new, which is not often. Leave any time.
          <a href="../privacy.html">What happens to your email.</a>
        </p>
        <input type="hidden" name="ml-submit" value="1">
        <input type="hidden" name="anticsrf" value="true">
      </form>
      <p class="signup-done" hidden>
        <strong>Nearly there, check your email.</strong>
        You'll have a confirmation link waiting; the list won't have you until you click it.
      </p>
      <iframe name="ml-sink" title="Signup handler" hidden></iframe>
    </div>
  </div>
</section>

<footer>
  <div class="wrap">
    <p class="disclaimer">{disclaimer}</p>
    <p class="foot-links">
      <a href="../">Home</a>
      <a href="../guides/">What is on the calendar</a>
      <a href="../privacy.html">Privacy</a>
    </p>
    <p class="version">v{version}</p>
  </div>
</footer>

<script>
(function () {{
  'use strict';

  // The four, and their lifespans, written out of planner_data.py at build
  // time. The download runs this same arithmetic on the same numbers, so
  // somebody who tries this and then buys never finds the two disagreeing.
  var SYSTEMS = {systems};
  var NOW = new Date().getFullYear();

  var built = document.getElementById('built');
  var results = document.getElementById('results');
  var modes = Array.prototype.slice.call(document.querySelectorAll('.mode'));
  var years = Array.prototype.slice.call(document.querySelectorAll('.year'));
{engine}

  function render() {{
    var buildYear = parseInt(built.value, 10);
    if (!buildYear || buildYear < 1850 || buildYear > NOW + 1) {{
      results.innerHTML =
        '<p class="empty">Put a build year in above and the answer appears here.</p>';
      return;
    }}

    var found = [];
    var untouched = true;
    for (var i = 0; i < SYSTEMS.length; i++) {{
      var mode = modes[i].value;
      if (mode !== 'schedule') {{ untouched = false; }}
      if (mode === 'skip') {{ continue; }}
      var installed = installYear(mode, SYSTEMS[i].life, buildYear,
                                  parseInt(years[i].value, 10));
      if (installed === null) {{ continue; }}
      found.push({{
        name: SYSTEMS[i].name,
        due: installed + SYSTEMS[i].life,
        remaining: installed + SYSTEMS[i].life - NOW,
        estimated: mode !== 'known'
      }});
    }}

    if (!found.length) {{
      results.innerHTML = '<p class="empty">Nothing is switched on. Turn one back on ' +
        'below, or put a year in for anything set to <em>I know the year</em>.</p>';
      return;
    }}

    found.sort(function (a, b) {{ return a.remaining - b.remaining; }});
    var pressing = found.filter(function (r) {{ return r.remaining <= 2; }}).length;
    var overdue = found.filter(function (r) {{ return r.remaining <= 0; }}).length;

    var verdict;
    if (pressing === 0) {{
      verdict = '<p class="verdict">None of the four is past due. The next one up is ' +
        'the ' + escapeHtml(found[0].name.toLowerCase()) + '.</p>';
    }} else {{
      verdict = '<p class="verdict"><span class="big">' + pressing + '</span> of ' +
        found.length + (pressing === 1 ? ' is ' : ' are ') +
        'overdue or due within two years.</p>';
    }}

    // "Replaced on schedule" cannot produce an overdue item: by definition it
    // dates everything to its most recent cycle. So on an uncorrected list the
    // absence of red means the assumption held, not that the house is fine.
    if (!overdue && untouched) {{
      verdict += '<p class="nudge">That is assuming all four were replaced on schedule. ' +
        'If you know the roof or the water heater has never been touched since the house ' +
        'was built, set those to <strong>never replaced</strong> below.</p>';
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
  modes.forEach(function (select, index) {{
    select.addEventListener('change', function () {{
      years[index].hidden = select.value !== 'known';
      if (select.value === 'known' && !years[index].value) {{ years[index].focus(); }}
      render();
    }});
  }});
  years.forEach(function (input) {{ input.addEventListener('input', render); }});

  // Same signup contract as the other two pages: post to MailerLite through a
  // hidden frame so the visitor never leaves, and swap the form for the
  // check-your-email line once the frame reports back.
  var signup = document.querySelector('.signup');
  if (signup) {{
    signup.addEventListener('submit', function (event) {{
      var hp = signup.querySelector('input[name="website"]');
      var done = document.querySelector('.signup-done');
      if (hp && hp.value) {{
        event.preventDefault();
        signup.hidden = true;
        done.hidden = false;
        return;
      }}
      if (hp) {{ hp.disabled = true; }}
      var sink = document.querySelector('iframe[name="ml-sink"]');
      var swap = function () {{ signup.hidden = true; done.hidden = false; }};
      sink.addEventListener('load', swap, {{ once: true }});
      setTimeout(swap, 2500);
    }});
  }}
}})();
</script>

</body>
</html>
"""


def build_free():
    """The thin free page, four systems, pointing at the paid file."""
    items = free_rows()

    # Until the bundle has a listing there is nothing to send anyone to, so the
    # buy slot holds the list instead. Same trade as SHOP_URL at the bottom of
    # docs/index.html before the kit was purchasable.
    if BUNDLE_URL:
        buy = ('      <a class="btn" href="{0}" rel="noopener">Get the full version'
               '</a>'.format(escape(BUNDLE_URL)))
    else:
        buy = ('      <a class="btn" href="#keep-posted">Tell me when it is out</a>')

    html = FREE_TEMPLATE.format(
        domain=DOMAIN,
        items=free_items_html(items),
        systems=json.dumps([{"name": r["name"], "life": r["life"]} for r in items],
                           ensure_ascii=False).replace("</", "<\\/"),
        engine=ENGINE_JS,
        buy=buy,
        disclaimer=escape(DISCLAIMER),
        version=VERSION,
    )

    folder = os.path.dirname(FREE_OUT)
    if not os.path.isdir(folder):
        os.makedirs(folder)
    with open(FREE_OUT, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(html)

    print("{0}  {1} systems, the teaser".format(FREE_OUT, len(items)))
    if not BUNDLE_URL:
        print("  BUNDLE_URL is empty, so the buy slot holds the signup instead")
    return FREE_OUT


if __name__ == "__main__":
    build_free()
