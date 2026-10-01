#!/usr/bin/env python3
"""The top bar and the footer, defined once for the whole site.

Why this exists
---------------
Until 1.34.0 the bar and the footer were pasted into sixteen HTML files. That
is the drift trap this project has already paid for four times, and the file
headers of site.css, theme.css, nav.css and analytics.js each say so in their
own words. The audit found the fourth instance: seven resource pages sharing a
71 line stylesheet that had already diverged in two of them, and two tiers of
footer where the pages carrying the search traffic had the smaller one.

So the chrome moves here, and the pages get it written in by build_chrome.py.
The two already-generated pages, /guides/ and /calculator/, import these same
functions rather than carrying their own copy.

What is deliberately NOT here
-----------------------------
Page content. This file owns the bar, the footer, and nothing between them.
A page's own words stay in its own file, hand-written and readable, because
that is the part a person edits.

The rule for adding a page
--------------------------
A new page gets an entry in NAV or FOOTER here, a row on /resources/ if it is
a resource, a sitemap entry, and a PAGES entry in build_chrome.py, all in the
same commit. Then run build_chrome.py and every page has it.
"""

# --------------------------------------------------------------------------
# The one list of what this site contains.
#
# Paths are written from the site root without a leading slash. Every builder
# below prefixes them with the right number of ../ for the page being built,
# or with a leading / for 404.html, which has to work from any address.
# --------------------------------------------------------------------------

RESOURCES = [
    ("resources/strengthen-mississippi-homes/", "Mississippi roof grant"),
    ("resources/strengthen-alabama-homes/",     "Alabama roof grant"),
    ("resources/louisiana-fortify-homes/",      "Louisiana roof grant"),
    ("resources/my-safe-florida-home/",         "Florida inspections and grants"),
    ("resources/texas-windstorm-coverage/",     "Texas windstorm coverage"),
    ("resources/flood-insurance-30-day-rule/",  "Flood insurance 30-day rule"),
    ("resources/wind-mitigation-discounts/",    "Wind mitigation discounts"),
    ("resources/hurricane-deductibles/",        "Hurricane deductibles"),
    ("resources/gulf-wind-pools/",              "Wind pools by state"),
    ("resources/roof-age-and-insurance/",       "Roof age and insurance"),
    ("resources/storm-contractors/",            "Checking a contractor"),
]

TOOLS = [
    ("calculator/", "Borrowed Time Calculator"),
    ("guides/",     "What's on the calendar"),
]

# The desktop bar. A dropdown's own link still goes somewhere real, so the menu
# is a shortcut rather than a gate.
NAV = [
    ("calendars/",  "Calendar",   None),
    ("resources/",  "Resources",  [("resources/", "All resources")] + RESOURCES),
    ("storm/",      "Storm prep", None),
    ("calculator/", "Tools",      TOOLS),
    ("guides/",     "Guide",      None),
    ("shop/",       "Shop",       None),
]

ETSY = "https://www.etsy.com/shop/GulfCoastHomeCare"

# A real address for corrections and questions, and the one thing on this site
# that cannot be written for Chad. Same contract as GA_ID in analytics.js:
# empty means the feature is simply off. While it is empty every "get in touch"
# route on the site says Etsy, which works but routes a correction about a state
# agency through a retail storefront. Put a mailbox that somebody actually reads
# between these quotes and every page starts offering it instead.
CONTACT_EMAIL = ""


def contact_html(prefix="", absolute=False):
    """The one sentence that says how to reach a person."""
    if CONTACT_EMAIL:
        return ('Email <a href="mailto:%s">%s</a>, which reaches a person.'
                % (CONTACT_EMAIL, CONTACT_EMAIL))
    return ('Messages reach us through the '
            '<a href="%s" target="_blank" rel="noopener">Etsy shop</a>, '
            'which is where the printables are sold and where the message '
            'box is.' % ETSY)

FOOTER_COLUMNS = [
    ("Free", [
        ("calendars/",  "The free calendars"),
        ("guides/",     "What's on the calendar"),
        ("calculator/", "Borrowed Time Calculator"),
        ("storm/",      "Storm season"),
    ]),
    ("The shop", [
        ("shop/#edition", "The maintenance kit"),
        ("shop/#binder",  "The storm season binder"),
        ("shop/#agents",  "The agent edition"),
        (ETSY,            "The shop on Etsy"),
    ]),
    ("Grants and programs", [("resources/", "All resources")] + RESOURCES),
    ("About", [
        ("about/",       "About this site"),
        ("#who",         "Who made this"),
        (ETSY,           "Message the shop"),
        ("privacy.html", "Privacy"),
    ]),
]

DISCLAIMER = ("General maintenance guidance, not a substitute for a licensed "
              "inspector, contractor, or your insurance policy terms.")

# The thermal report builder, which is not part of this site: it lives on its
# own subdomain, is served from the office PC through a tunnel, and is behind a
# password. It sits with the version marker rather than in the footer columns
# for the same reason the version does, that both are furniture for whoever
# runs the site rather than anything offered to a reader. The label says it is
# private so that meeting a password box reads as intended rather than broken.
PRIVATE_TOOL = ("https://thermal.gulfcoasthomemaintenance.com/", "Thermal report tool")

HOUSE_SVG = (
    '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" '
    'stroke="currentColor" stroke-width="1.7" stroke-linecap="round" '
    'stroke-linejoin="round" aria-hidden="true">'
    '<path d="M3 11.5 12 4l9 7.5"/><path d="M5.5 10v9.5h13V10"/>'
    '<path d="M10 19.5V14h4v5.5"/></svg>'
)

BURGER_SVG = (
    '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" '
    'stroke="currentColor" stroke-width="2" stroke-linecap="round" '
    'aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'
)


def _href(path, prefix, absolute):
    """Resolve a root-relative path for the page being built."""
    if path.startswith(("http://", "https://", "mailto:")):
        return path
    if path.startswith("#"):                      # a home page anchor
        return ("/" if absolute else prefix or "./") + path
    if absolute:
        return "/" + path
    return (prefix + path) if prefix else (path or "./")


def _current(path, current):
    """aria-current for a nav entry.

    "page" only on the link that really is this page. "true" on an ancestor,
    which is the correct value for "this is the section you are in" and is what
    the Resources trigger on a state page needs: it points at the shelf, and
    the shelf is not the page you are reading.
    """
    if current is None:
        return ""
    if path.rstrip("/") == current.rstrip("/"):
        return ' aria-current="page"'
    if current.startswith(path) and path not in ("", "./"):
        return ' aria-current="true"'
    return ""


def topbar(prefix="", current=None, absolute=False):
    """The sticky bar. Same markup on every page, paths resolved per depth."""
    h = lambda p: _href(p, prefix, absolute)

    # Only one link may say aria-current="page", and two of them can point at
    # the same place: /guides/ is both "Guide" in the bar and "What's on the
    # calendar" in the Tools menu, so a screen reader announced the current page
    # twice. The first one wins; the second is left plain. "true", which marks
    # an ancestor rather than the page itself, is not limited this way, because
    # a section really can contain the page you are on.
    said = {"page": False}

    def c(path):
        value = _current(path, current)
        if value.endswith('"page"'):
            if said["page"]:
                return ""
            said["page"] = True
        return value

    # On the home page the wordmark is a span: a link to the page you are on is
    # a link that does nothing.
    home = h("")
    if current in ("", "./", None) and not absolute and prefix == "":
        mark = '    <span class="mark">\n      %s\n      <span class="label">Gulf Coast Home Maintenance</span>\n    </span>' % HOUSE_SVG
    else:
        mark = '    <a class="mark" href="%s">\n      %s\n      <span class="label">Gulf Coast Home Maintenance</span>\n    </a>' % (home, HOUSE_SVG)

    items = []
    for path, label, menu in NAV:
        if menu is None:
            items.append('      <a href="%s"%s>%s</a>' % (h(path), c(path), label))
        else:
            rows = "\n".join(
                '          <a href="%s"%s>%s</a>' % (h(p), c(p), t) for p, t in menu)
            items.append(
                '      <span class="nav-drop">\n'
                '        <a href="%s"%s>%s</a>\n'
                '        <span class="nav-menu"><span class="menu-card">\n%s\n'
                '        </span></span>\n'
                '      </span>' % (h(path), c(path), label, rows))
    desktop = "\n".join(items)

    # The phone menu. A <details> rather than a script: it is keyboard operable
    # and screen-reader announced for free, it works with scripting off, and
    # there is no state for anything to get out of step with. Below 52rem the
    # desktop links are display:none and this is the only way through the site,
    # which is why it carries every destination rather than a shortlist.
    groups = [("Pages", [(p, l) for p, l, _ in NAV]),
              ("Grants and programs", RESOURCES),
              ("Free tools", TOOLS),
              ("About", [("about/", "About this site"),
                         ("privacy.html", "Privacy")])]
    panel = []
    for title, links in groups:
        panel.append('          <p class="nm-group">%s</p>' % title)
        for p, t in links:
            panel.append('          <a href="%s"%s>%s</a>' % (h(p), c(p), t))
    panel = "\n".join(panel)

    return (
        '<div class="topbar">\n'
        '  <div class="inner">\n'
        '%s\n'
        '    <nav class="nav-links" aria-label="Site">\n%s\n    </nav>\n'
        '    <span class="topbar-ctas">\n'
        '      <a class="cta cta--free" href="%s">Get the free calendar</a>\n'
        '      <details class="nav-mobile">\n'
        '        <summary>%s Menu</summary>\n'
        '        <nav class="nm-panel" aria-label="All pages">\n%s\n        </nav>\n'
        '      </details>\n'
        '    </span>\n'
        '  </div>\n'
        '</div>' % (mark, desktop, h("calendars/"), BURGER_SVG, panel))


def footer(prefix="", version="", prelude="", absolute=False):
    """The full footer, on every content page.

    `prelude` is the one slot: page-specific content that belongs above the
    grid. The resource pages put their corrections line and checked date there;
    the home page puts the mailing list there. Everything below it is the same
    on every page, which is the whole point of this file.
    """
    h = lambda p: _href(p, prefix, absolute)

    cols = []
    for title, links in FOOTER_COLUMNS:
        rows = "\n".join(
            '          <li><a href="%s"%s>%s</a></li>'
            % (h(p), ' target="_blank" rel="noopener"' if p.startswith("http") else "", t)
            for p, t in links)
        cols.append('      <div>\n        <h3>%s</h3>\n        <ul>\n%s\n        </ul>\n      </div>'
                    % (title, rows))
    grid = "\n".join(cols)

    pre = ("\n" + prelude.rstrip() + "\n") if prelude.strip() else ""
    # New tab, like every other off-site link in this footer: it is a separate
    # application on its own subdomain, not another page of the site.
    #
    # nofollow, which the footer column links do not carry, because that
    # subdomain answers 401 to everything including its own robots.txt. Without
    # this, Googlebot follows the link from all twenty pages and bounces off a
    # password every time. It could never index it either way, since a crawler
    # that is refused at the door never reads the noindex header behind it, but
    # there is no reason to send a crawler somewhere it cannot go.
    tool = ('\n    <p class="private-tool"><a href="%s" target="_blank"'
            ' rel="noopener nofollow">%s</a>'
            ' &middot; private, password required</p>' % PRIVATE_TOOL)
    ver = ('\n    <!-- Bump on release, alongside the CHANGELOG entry and the git tag.\n'
           '         Shown so a tester can say which version they were looking at. -->\n'
           '    <p class="version">v%s</p>' % version) if version else ""

    return (
        '<footer>\n'
        '  <div class="foot-wrap">%s\n'
        '    <span class="mark" style="margin-bottom:1.25rem">\n'
        '      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" '
        'style="color:var(--sand-lift)">\n'
        '        <path d="M3 11.5 12 4l9 7.5"/><path d="M5.5 10v9.5h13V10"/>'
        '<path d="M10 19.5V14h4v5.5"/>\n'
        '      </svg>\n'
        '      <span class="label">Gulf Coast Home Maintenance</span>\n'
        '    </span>\n\n'
        '    <div class="foot-grid">\n%s\n    </div>\n\n'
        '    <p class="disclaimer">%s</p>%s%s\n'
        '  </div>\n'
        '</footer>' % (pre, grid, DISCLAIMER, tool, ver))
