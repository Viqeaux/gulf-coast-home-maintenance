#!/usr/bin/env python3
"""
Build the printable PDF edition — the free download the shop leads with.

Run:  python build_pdf.py
Out:  product/Gulf-Coast-Home-Maintenance-Calendar.pdf   (20 pages, US Letter)
      product/listing/*.png                              (Etsy listing images)

Two sources feed it, and the split is deliberate:

  build_calendars.py   the twelve months of tasks, shared with the .ics feeds so
                       the print edition and the digital one cannot drift apart
  product_content.py   the pages the feeds do not carry — the Watch List
                       lifespans, how to date what you own, the first-month
                       checklist, the licence

The finished PDF is gitignored, but only because it is a build artifact. There
is nothing in it to protect — it is given away — and it is not served from
docs/, so committing it would put a binary in the repo that nothing reads.

Design notes worth keeping:

  * Interiors are white. It is a print-at-home file, and a full-bleed tinted
    page costs the reader a cartridge to save us nothing. Colour is spent on the
    cover, the rules, and the tier bars.
  * Serif is Times, one of the fourteen fonts every PDF reader already has, so
    nothing is embedded that could render differently on someone else's
    printer. The sans is Bitstream Vera, which ships with reportlab under a
    licence that allows embedding.
"""

import os
import sys

import reportlab
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as pdfcanvas

from build_calendars import (DISCLAIMER, MONTH_NAMES, SITE_URL, TASKS,
                             TIER_ORDER, VERSION)

try:
    import product_content as content
except ImportError:
    sys.exit(
        "product_content.py is missing. It holds the Watch List, the dating\n"
        "page, the first-month checklist, and the licence — without it this\n"
        "build would produce a calendar missing the pages that make it worth\n"
        "downloading, which is worse than producing nothing."
    )

OUT_DIR = "product"
PDF_NAME = "Gulf-Coast-Home-Maintenance-Calendar.pdf"

TITLE = "The Gulf Coast Home Maintenance Calendar"
SUBTITLE = "Perpetual edition · undated"

# --- Palette ---------------------------------------------------------------
# The site's tokens from docs/theme.css, minus the ones that only mean anything
# on a screen. Kept as hex strings matching that file so the two can be compared
# by eye when either changes.

INK = HexColor("#15201f")
MUTED = HexColor("#5b6a68")
RULE = HexColor("#d9cfba")
RULE_SOFT = HexColor("#ebe4d6")
PAPER_2 = HexColor("#f4efe4")
DEEP = HexColor("#0e2429")
ON_DEEP = HexColor("#e8e2d4")
ON_DEEP_MUTE = HexColor("#93a5a6")
ACCENT = HexColor("#0f5e6b")
SAND = HexColor("#c08b2e")

TIER_COLOR = {
    "must": HexColor("#a33520"),
    "should": HexColor("#14606e"),
    "above": HexColor("#5b6f34"),
}
TIER_WORD = {"must": "Must do", "should": "Should do", "above": "Going above"}

TIER_BLURB = [
    ("must", "Must do",
     "Safety, or skipping it costs you thousands. If you do nothing else, "
     "do these twelve things."),
    ("should", "Should do",
     "Protects your home’s value and makes what you own last longer."),
    ("above", "Going above",
     "For the homeowner who wants to stay ahead of everything."),
]

# --- Page geometry ---------------------------------------------------------

W, H = letter                 # 612 x 792 pt
MARGIN = 54                   # 0.75in — inside every home printer's dead zone
CW = W - 2 * MARGIN           # content width, 504pt
TOP = H - MARGIN
FOOT = 40                     # baseline of the running foot

# --- Fonts -----------------------------------------------------------------

SERIF = "Times-Roman"
SERIF_B = "Times-Bold"
SERIF_I = "Times-Italic"
SANS = "Vera"
SANS_B = "Vera-Bold"


def register_fonts():
    """Embed the sans. The serif is base-14 and needs no embedding."""
    fonts = os.path.join(os.path.dirname(reportlab.__file__), "fonts")
    pdfmetrics.registerFont(TTFont(SANS, os.path.join(fonts, "Vera.ttf")))
    pdfmetrics.registerFont(TTFont(SANS_B, os.path.join(fonts, "VeraBd.ttf")))


# --- Text primitives -------------------------------------------------------
#
# Everything is drawn on a bare canvas rather than through platypus flowables.
# Every page here is a fixed composition that has to fit exactly once, which is
# the case flowables are worst at and hand placement is best at.


def wrap(text, font, size, width):
    """Greedy line break. Returns a list of lines that fit inside width."""
    lines = []
    for hard in text.split("\n"):
        words = hard.split()
        if not words:
            lines.append("")
            continue
        line = words[0]
        for word in words[1:]:
            trial = line + " " + word
            if pdfmetrics.stringWidth(trial, font, size) <= width:
                line = trial
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


def block_height(text, font, size, leading, width):
    """How tall wrap() will make this, without drawing it."""
    return len(wrap(text, font, size, width)) * leading


def para(c, text, x, top, width, font=SERIF, size=10.5, leading=14.5,
         color=INK):
    """Draw wrapped text from `top` downward. Returns the new top."""
    c.setFont(font, size)
    c.setFillColor(color)
    y = top - size * 0.86
    for line in wrap(text, font, size, width):
        c.drawString(x, y, line)
        y -= leading
    return y + leading - size * 0.86


def tracked(c, text, x, y, font=SANS_B, size=7.5, color=MUTED, space=1.6,
            center=None):
    """Letterspaced small caps — the field-guide label used across the site."""
    text = text.upper()
    if center is not None:
        width = pdfmetrics.stringWidth(text, font, size) + space * (len(text) - 1)
        x = center - width / 2.0
    # Letterspacing is a text-object setting, not a canvas one, so this goes
    # through beginText rather than drawString. It is also part of the PDF text
    # state, which survives the end of the text object — leave it set and every
    # later drawString on the page comes out spaced and overflowing its column.
    # Hence the reset before the object closes.
    obj = c.beginText(x, y)
    obj.setFont(font, size)
    obj.setFillColor(color)
    obj.setCharSpace(space)
    obj.textOut(text)
    obj.setCharSpace(0)
    c.drawText(obj)


def rule(c, x, y, width, color=RULE, thickness=0.6):
    c.setStrokeColor(color)
    c.setLineWidth(thickness)
    c.line(x, y, x + width, y)


def checkbox(c, x, y, size=9, color=None):
    c.setStrokeColor(color or RULE)
    c.setLineWidth(0.8)
    c.rect(x, y, size, size, stroke=1, fill=0)


def footer(c, page):
    """Running foot. Skipped on the cover, which has its own."""
    tracked(c, TITLE, MARGIN, FOOT, size=6.5, color=MUTED, space=1.2)
    c.setFont(SANS, 7.5)
    c.setFillColor(MUTED)
    c.drawRightString(W - MARGIN, FOOT, str(page))
    rule(c, MARGIN, FOOT + 12, CW, RULE_SOFT, 0.5)


def page_head(c, kicker, heading, deck=None):
    """Standard interior page header. Returns the top of the content area."""
    tracked(c, kicker, MARGIN, TOP - 6, size=7.5, color=ACCENT, space=2.0)
    c.setFont(SERIF_B, 26)
    c.setFillColor(INK)
    c.drawString(MARGIN, TOP - 38, heading)
    top = TOP - 52
    if deck:
        top = para(c, deck, MARGIN, top - 8, CW * 0.86, SERIF, 11, 15.5, MUTED)
    rule(c, MARGIN, top - 14, CW, RULE, 1.2)
    return top - 32


# --- Pages -----------------------------------------------------------------


def cover(c):
    """The one page that gets to spend ink."""
    c.setFillColor(DEEP)
    c.rect(0, 0, W, H, stroke=0, fill=1)

    # Hairline frame, inset from the trim — the field-guide plate look.
    c.setStrokeColor(HexColor("#2c4448"))
    c.setLineWidth(0.7)
    c.rect(30, 30, W - 60, H - 60, stroke=1, fill=0)

    tracked(c, "Texas to Florida · Undated · Never expires", 0, H - 118,
            size=8, color=SAND, space=2.4, center=W / 2.0)

    c.setFillColor(white)
    c.setFont(SERIF_B, 44)
    for i, line in enumerate(["The Gulf Coast", "Home Maintenance", "Calendar"]):
        c.drawCentredString(W / 2.0, H - 190 - i * 52, line)

    rule(c, W / 2.0 - 40, H - 372, 80, SAND, 1.4)

    c.setFont(SERIF_I, 13)
    c.setFillColor(ON_DEEP)
    deck = ("Twelve months of what to do, in the order the coast asks for it.")
    c.drawCentredString(W / 2.0, H - 402, deck)

    # The three tiers as a row of chips — the structure of the whole book, said
    # once on the cover so nobody has to be told it twice inside.
    chip_w, chip_h, gap = 138, 30, 12
    total = chip_w * 3 + gap * 2
    x = (W - total) / 2.0
    for key, word, _ in TIER_BLURB:
        c.setFillColor(TIER_COLOR[key])
        c.rect(x, H - 470, chip_w, chip_h, stroke=0, fill=1)
        tracked(c, word, 0, H - 470 + 11, size=8, color=white, space=2.0,
                center=x + chip_w / 2.0)
        x += chip_w + gap

    c.setFont(SERIF, 11)
    c.setFillColor(ON_DEEP_MUTE)
    for i, line in enumerate([
            "Built for salt air, humidity, termites, and a hurricane season",
            "that runs half the year. Print it once and hang it anywhere.",
    ]):
        c.drawCentredString(W / 2.0, H - 520 - i * 17, line)

    rule(c, MARGIN + 60, 132, CW - 120, HexColor("#2c4448"), 0.7)
    tracked(c, "gulfcoasthomemaintenance.com", 0, 108, size=8,
            color=ON_DEEP_MUTE, space=2.0, center=W / 2.0)
    tracked(c, "Includes three free calendars for your phone", 0, 88, size=7.5,
            color=SAND, space=1.8, center=W / 2.0)


def how_it_works(c):
    top = page_head(
        c, "Start here", "How this works",
        "Three levels of care, twelve months each. Every month page holds one "
        "task from each level — what to do, and why it matters here and not "
        "somewhere else.")

    for key, word, blurb in TIER_BLURB:
        c.setFillColor(TIER_COLOR[key])
        c.rect(MARGIN, top - 46, 3.5, 46, stroke=0, fill=1)
        tracked(c, word, MARGIN + 14, top - 11, size=9,
                color=TIER_COLOR[key], space=2.0)
        para(c, blurb, MARGIN + 14, top - 20, CW - 30, SERIF, 11, 15, INK)
        top -= 64

    c.setFillColor(PAPER_2)
    c.rect(MARGIN, top - 54, CW, 50, stroke=0, fill=1)
    c.setFont(SERIF_I, 12)
    c.setFillColor(INK)
    c.drawCentredString(W / 2.0, top - 26,
                        "Start with Must Do. Add the others when you are ready.")
    c.setFont(SERIF_I, 12)
    c.drawCentredString(W / 2.0, top - 43,
                        "Nobody does all of this the first year.")
    top -= 84

    rule(c, MARGIN, top, CW, RULE_SOFT, 0.6)
    top -= 24

    col = (CW - 30) / 2.0
    left_top = top
    tracked(c, "Using the month pages", MARGIN, left_top, size=8, color=ACCENT,
            space=2.0)
    para(c, "There is no year on this calendar and no weekday grid, which is "
            "what lets it hang on the same nail forever. Each task has a box "
            "and a line: tick it, write the date, and next year you can see "
            "when you last did it.",
         MARGIN, left_top - 12, col, SERIF, 10, 14, MUTED)

    x2 = MARGIN + col + 30
    tracked(c, "Printing it", x2, left_top, size=8, color=ACCENT, space=2.0)
    para(c, "Sized for US Letter, with margins inside what every home printer "
            "can reach. Print single-sided at 100% — do not let the dialog "
            "scale it to fit. Black and white loses only the tier colours, "
            "and the tiers are labelled anyway.",
         x2, left_top - 12, col, SERIF, 10, 14, MUTED)


# The four seasons the house has to survive, as (label, start month, end month,
# colour). Hurricane season is June 1 to November 30 — 183 days, which is the
# number the whole calendar is shaped around.
SEASONS = [
    ("Hurricane season", 6, 11, HexColor("#a33520")),
    ("Heat & humidity", 5, 9, SAND),
    ("Termite swarm", 3, 5, HexColor("#5b6f34")),
    ("Freeze risk", 12, 2, HexColor("#14606e")),   # wraps the year
]


def the_year(c):
    top = page_head(
        c, "The shape of it", "The Gulf Coast year",
        "Four overlapping seasons that do not line up with the ones on a "
        "normal calendar. This is what the twelve months are built around.")

    label_w = 96
    grid_x = MARGIN + label_w
    grid_w = CW - label_w
    col = grid_w / 12.0
    band_h = 26
    gap = 12
    grid_top = top - 20
    grid_bottom = grid_top - (len(SEASONS) * (band_h + gap))

    # month grid
    c.setStrokeColor(RULE_SOFT)
    c.setLineWidth(0.5)
    for i in range(13):
        x = grid_x + i * col
        c.line(x, grid_top, x, grid_bottom - 6)
    for i, name in enumerate(MONTH_NAMES):
        tracked(c, name[:3], 0, grid_top + 8, size=6.5, color=MUTED, space=0.8,
                center=grid_x + (i + 0.5) * col)

    y = grid_top - band_h
    for label, start, end, color in SEASONS:
        tracked(c, label, 0, y + band_h / 2.0 - 3, size=7, color=INK,
                space=1.2, center=MARGIN + label_w / 2.0 - 8)
        spans = ([(start, 12), (1, end)] if end < start else [(start, end)])
        for a, b in spans:
            x = grid_x + (a - 1) * col
            c.setFillColor(color)
            c.rect(x, y, (b - a + 1) * col, band_h, stroke=0, fill=1)
        y -= band_h + gap

    # The May 1 deadline, which is the single most useful line on the page.
    may_x = grid_x + 4 * col
    c.setStrokeColor(INK)
    c.setLineWidth(1.1)
    c.setDash(3, 2)
    c.line(may_x, grid_top + 2, may_x, grid_bottom - 14)
    c.setDash()
    tracked(c, "Insure before May 1", may_x + 6, grid_bottom - 26, size=7.5,
            color=INK, space=1.6)

    top = grid_bottom - 52
    rule(c, MARGIN, top, CW, RULE, 1.0)
    top -= 26

    col_w = (CW - 30) / 2.0
    for i, (heading, body) in enumerate([
        ("Why May, not June",
         "A flood policy generally takes 30 days to take effect. Buy it on "
         "June 1 and you are uninsured for the opening weeks of the season. "
         "That is why hurricane prep sits in May on this calendar and why it "
         "is the one task with a date on it."),
        ("Why the numbers are shorter here",
         "Salt air, humidity, and UV wear a coastal house faster than the "
         "national averages assume. An A/C that runs nine months a year is "
         "doing double the work it was rated against. Everything in this "
         "calendar is adjusted for that."),
    ]):
        x = MARGIN + i * (col_w + 30)
        tracked(c, heading, x, top, size=8, color=ACCENT, space=2.0)
        para(c, body, x, top - 12, col_w, SERIF, 10, 14, MUTED)


def first_month(c):
    top = page_head(c, "Before month one", "Your first month",
                    content.FIRST_MONTH_NOTE)

    for item in content.FIRST_MONTH:
        checkbox(c, MARGIN, top - 12, 11, RULE)
        para(c, item, MARGIN + 24, top, CW - 24, SERIF, 12, 16, INK)
        rule(c, MARGIN + 24, top - 20, CW - 24, RULE_SOFT, 0.5)
        top -= 38

    top -= 10
    note = ("Filter sizes, shutoff locations, and anything else you had to go "
            "looking for. Write it here once and you never look again.")
    lines = 4
    height = (24 + block_height(note, SERIF, 10, 14, CW - 40)
              + 16 + (lines - 1) * 18 + 14)
    c.setFillColor(PAPER_2)
    c.rect(MARGIN, top - height, CW, height, stroke=0, fill=1)
    tracked(c, "What I had to go find", MARGIN + 20, top - 22, size=8,
            color=ACCENT, space=2.0)
    inner = para(c, note, MARGIN + 20, top - 30, CW - 40, SERIF, 10, 14, MUTED)
    for i in range(lines):
        rule(c, MARGIN + 20, inner - 16 - i * 18, CW - 40, RULE, 0.5)


def month_page(c, month):
    """One of the twelve. Three tasks, one per tier, with room to sign off."""
    name = MONTH_NAMES[month - 1]
    note = content.MONTH_NOTES.get(month)

    tracked(c, "Gulf Coast Home Maintenance", MARGIN, TOP - 6, size=7,
            color=MUTED, space=2.0)
    c.setFont(SERIF_B, 52)
    c.setFillColor(INK)
    c.drawString(MARGIN - 3, TOP - 62, name)

    tracked(c, "{0} of 12".format(month), 0, TOP - 20, size=8, color=SAND,
            space=2.0, center=W - MARGIN - 24)

    top = TOP - 76
    if note:
        c.setFillColor(TIER_COLOR["must"])
        c.rect(MARGIN, top - 20, 3, 18, stroke=0, fill=1)
        c.setFont(SERIF_I, 12)
        c.setFillColor(TIER_COLOR["must"])
        c.drawString(MARGIN + 12, top - 15, note)
        top -= 30
    rule(c, MARGIN, top - 6, CW, RULE, 1.4)
    top -= 30

    tasks = sorted([t for t in TASKS if t[0] == month],
                   key=lambda t: TIER_ORDER[t[2]])

    for _month, _day, tier, _slug, title, body in tasks:
        parts = [p.strip() for p in body.split("\n\n") if p.strip()]
        instruction = parts[0]
        why = parts[1] if len(parts) > 1 else ""
        if why.startswith("Why:"):
            # The feed reads "Why: caulk is the cheapest..." as one sentence. In
            # print the label is dropped, so the sentence has to stand up on its
            # own capital.
            why = why[4:].strip()
            why = why[:1].upper() + why[1:]

        pad = 14
        tag_h = 20        # the MUST DO / SHOULD DO line above the title
        row_h = 14        # the sign-off row along the bottom
        text_w = CW - 2 * pad - 6

        content_h = block_height(title, SANS_B, 12.5, 16, text_w)
        content_h += 4 + block_height(instruction, SERIF, 11, 15, text_w)
        if why:
            content_h += 8 + block_height(why, SERIF_I, 10, 13.5, text_w)
        height = pad + tag_h + content_h + 12 + row_h + 10

        y = top - height
        c.setStrokeColor(RULE)
        c.setLineWidth(0.7)
        c.rect(MARGIN, y, CW, height, stroke=1, fill=0)
        c.setFillColor(TIER_COLOR[tier])
        c.rect(MARGIN, y, 3.5, height, stroke=0, fill=1)

        text_x = MARGIN + pad + 6
        inner = top - pad - tag_h
        tracked(c, TIER_WORD[tier], text_x, top - pad - 8, size=7.5,
                color=TIER_COLOR[tier], space=2.0)
        inner = para(c, title, text_x, inner, text_w, SANS_B, 12.5, 16, INK)
        inner = para(c, instruction, text_x, inner - 4, text_w, SERIF, 11, 15,
                     INK)
        if why:
            inner = para(c, why, text_x, inner - 8, text_w, SERIF_I, 10, 13.5,
                         MUTED)

        # Sign-off row: the thing that makes an undated calendar worth keeping.
        # A tick alone says you did it once; the date is what tells you next
        # year whether "once" was recent.
        row_y = y + 10
        right = MARGIN + CW - pad - 6
        checkbox(c, text_x, row_y, 10, TIER_COLOR[tier])
        tracked(c, "Done", text_x + 16, row_y + 2.5, size=7, color=MUTED,
                space=1.2)
        tracked(c, "Date", text_x + 62, row_y + 2.5, size=7, color=MUTED,
                space=1.2)
        rule(c, text_x + 92, row_y, 110, RULE, 0.6)
        tracked(c, "Notes", text_x + 216, row_y + 2.5, size=7, color=MUTED,
                space=1.2)
        rule(c, text_x + 250, row_y, right - (text_x + 250), RULE, 0.6)

        top = y - 14


def watch_list(c):
    top = page_head(
        c, "The page that pays for itself", "The Big Ticket Watch List",
        "Everything expensive in a house is on a clock. Fill in the year and "
        "you will see the bill coming years before it arrives.")

    # Letterspaced headers are wide. These four have to clear each other at
    # 6.5pt with 1pt of tracking, which is what sets the column stops.
    cols = [0, 200, 292, 404]      # item, installed, life, start watching
    widths = [192, 80, 104, 100]
    headers = ["Item", "Year installed", "Gulf Coast life", "Start watching"]

    for i, head in enumerate(headers):
        tracked(c, head, MARGIN + cols[i], top, size=6.5, color=MUTED,
                space=1.0)
    top -= 8
    rule(c, MARGIN, top, CW, INK, 0.8)

    row_h = 25.5
    for i, (item, life) in enumerate(content.WATCH_LIST):
        y = top - (i + 1) * row_h
        if i % 2 == 0:
            c.setFillColor(HexColor("#faf7ef"))
            c.rect(MARGIN, y, CW, row_h, stroke=0, fill=1)
        base = y + 8.5
        c.setFont(SERIF, 10.5)
        c.setFillColor(INK)
        c.drawString(MARGIN + cols[0], base, item)
        c.setFont(SANS, 8.5)
        c.setFillColor(MUTED)
        c.drawString(MARGIN + cols[2], base, life)
        rule(c, MARGIN + cols[1], y + 6, widths[1] - 12, RULE, 0.6)
        rule(c, MARGIN + cols[3], y + 6, widths[3], RULE, 0.6)
        rule(c, MARGIN, y, CW, RULE_SOFT, 0.4)

    top = top - len(content.WATCH_LIST) * row_h - 26

    c.setFillColor(PAPER_2)
    height = 30 + block_height(content.WATCH_LIST_NOTE, SERIF, 10, 14,
                               CW - 40)
    c.rect(MARGIN, top - height, CW, height, stroke=0, fill=1)
    c.setFillColor(SAND)
    c.rect(MARGIN, top - height, 3, height, stroke=0, fill=1)
    tracked(c, content.WATCH_LIST_NOTE_TITLE, MARGIN + 20, top - 20, size=8,
            color=ACCENT, space=1.8)
    para(c, content.WATCH_LIST_NOTE, MARGIN + 20, top - 28, CW - 40, SERIF,
         10, 14, INK)


def find_out(c):
    top = page_head(c, "Facing the Watch List", "How to find out",
                    content.FIND_OUT_INTRO)

    for subject, how in content.FIND_OUT:
        c.setFillColor(ACCENT)
        c.circle(MARGIN + 3, top - 6, 2.5, stroke=0, fill=1)
        c.setFont(SANS_B, 11)
        c.setFillColor(INK)
        c.drawString(MARGIN + 14, top - 10, subject)
        after = para(c, how, MARGIN + 14, top - 24, CW - 20, SERIF, 10.5, 14.5,
                     MUTED)
        top = after - 20
        rule(c, MARGIN, top + 8, CW, RULE_SOFT, 0.5)

    top -= 14
    height = 34 + block_height(content.FIND_OUT_CLOSE, SERIF, 11, 15, CW - 40)
    c.setFillColor(DEEP)
    c.rect(MARGIN, top - height, CW, height, stroke=0, fill=1)
    tracked(c, content.FIND_OUT_CLOSE_TITLE, MARGIN + 20, top - 22, size=8,
            color=SAND, space=2.0)
    para(c, content.FIND_OUT_CLOSE, MARGIN + 20, top - 30, CW - 40, SERIF, 11,
         15, ON_DEEP)


def draw_qr(c, url, x, y, size):
    """Vector QR, drawn module by module, so it stays sharp at any print size."""
    try:
        import segno
    except ImportError:
        return False
    matrix = list(segno.make(url, error="m").matrix)
    n = len(matrix)
    quiet = 4
    module = size / float(n + quiet * 2)
    c.setFillColor(white)
    c.rect(x, y, size, size, stroke=0, fill=1)
    c.setFillColor(INK)
    for row_i, row in enumerate(matrix):
        for col_i, dark in enumerate(row):
            if dark:
                c.rect(x + (col_i + quiet) * module,
                       y + size - (row_i + quiet + 1) * module,
                       module, module, stroke=0, fill=1)
    return True


def digital(c):
    top = page_head(
        c, "Included with your calendar", "Three calendars for your phone",
        "The same twelve months, as subscribe-able calendars. They repeat "
        "every year with no end date, so once you add them you are done.")

    qr_size = 132
    qr_x = W - MARGIN - qr_size
    drawn = draw_qr(c, SITE_URL, qr_x, top - qr_size, qr_size)
    if drawn:
        tracked(c, "Scan me", 0, top - qr_size - 14, size=7, color=MUTED,
                space=1.6, center=qr_x + qr_size / 2.0)

    text_w = CW - qr_size - 40
    inner = top
    for key, word, _ in TIER_BLURB:
        c.setFillColor(TIER_COLOR[key])
        c.rect(MARGIN, inner - 15, 3, 15, stroke=0, fill=1)
        c.setFont(SANS_B, 10)
        c.setFillColor(INK)
        c.drawString(MARGIN + 12, inner - 12, word)
        c.setFont(SANS, 8.5)
        c.setFillColor(MUTED)
        c.drawString(MARGIN + 12 + 96, inner - 12, "12 events a year")
        inner -= 26

    inner -= 10
    tracked(c, "Where to get them", MARGIN, inner, size=8, color=ACCENT,
            space=2.0)
    inner = para(c, SITE_URL.rstrip("/").replace("https://", ""),
                 MARGIN, inner - 14, text_w, SERIF_B, 15, 19, INK)

    top = min(inner, top - qr_size) - 34
    rule(c, MARGIN, top + 14, CW, RULE, 1.0)

    steps = [
        ("On a computer, once",
         "Open that page, pick a level, and press Add to Google Calendar or "
         "Subscribe. It syncs to every phone on the account afterwards."),
        ("Subscribe, don’t import",
         "Import is a one-time copy that never updates and duplicates itself "
         "if you do it twice. Subscribing means corrections and added how-to "
         "videos reach you on their own."),
        ("Give it a day",
         "Google refreshes subscribed calendars slowly, sometimes up to a "
         "day. Nothing in here is urgent to the hour."),
    ]
    col_w = (CW - 40) / 3.0
    for i, (heading, body) in enumerate(steps):
        x = MARGIN + i * (col_w + 20)
        tracked(c, "0{0}".format(i + 1), x, top, size=8, color=SAND, space=1.6)
        c.setFont(SANS_B, 9.5)
        c.setFillColor(INK)
        c.drawString(x, top - 16, heading)
        para(c, body, x, top - 24, col_w, SERIF, 9.5, 13, MUTED)

    top -= 130
    c.setFillColor(PAPER_2)
    c.rect(MARGIN, top - 62, CW, 62, stroke=0, fill=1)
    tracked(c, "There is also a how-to page", MARGIN + 20, top - 20, size=8,
            color=ACCENT, space=2.0)
    para(c, "Every task on this calendar has a section on the site with a "
            "picked video from someone who explains it well. It is filled in "
            "over time, and it is free.",
         MARGIN + 20, top - 28, CW - 40, SERIF, 10, 14, INK)


def closing(c):
    top = page_head(c, "The fine print", content.LICENCE_TITLE)

    for heading, body in content.LICENCE:
        c.setFont(SANS_B, 10.5)
        c.setFillColor(INK)
        c.drawString(MARGIN, top - 10, heading)
        top = para(c, body, MARGIN, top - 24, CW - 40, SERIF, 10.5, 14.5,
                   MUTED) - 22

    rule(c, MARGIN, top, CW, RULE_SOFT, 0.6)
    top -= 30

    c.setFont(SERIF_I, 11)
    c.setFillColor(MUTED)
    for line in wrap(DISCLAIMER, SERIF_I, 11, CW - 60):
        c.drawCentredString(W / 2.0, top, line)
        top -= 15

    top -= 40
    c.setFillColor(DEEP)
    c.rect(MARGIN, top - 108, CW, 108, stroke=0, fill=1)
    c.setFont(SERIF_B, 17)
    c.setFillColor(white)
    c.drawCentredString(W / 2.0, top - 40, "Thank you.")
    c.setFont(SERIF, 10.5)
    c.setFillColor(ON_DEEP_MUTE)
    c.drawCentredString(
        W / 2.0, top - 62,
        "If something in here is wrong, or a video has gone dead, tell me.")
    c.drawCentredString(
        W / 2.0, top - 78, "It gets fixed for everyone who has it.")
    tracked(c, "gulfcoasthomemaintenance.com", 0, top - 96, size=7.5,
            color=SAND, space=2.0, center=W / 2.0)

    tracked(c, "Perpetual edition · v{0}".format(VERSION), 0, FOOT + 30,
            size=7, color=MUTED, space=1.6, center=W / 2.0)


# --- Assembly --------------------------------------------------------------


def build(path):
    c = pdfcanvas.Canvas(path, pagesize=letter)
    c.setPageCompression(1)
    c.setTitle(TITLE)
    c.setSubject("A home maintenance calendar built for the Gulf Coast — "
                 "undated, twelve months, three levels of care.")
    c.setAuthor("Gulf Coast Home Maintenance")
    c.setCreator("build_pdf.py")
    c.setKeywords("home maintenance, Gulf Coast, hurricane season, printable, "
                  "undated calendar, homeowner checklist")

    pages = [("Cover", cover, None), ("How this works", how_it_works, 1),
             ("The Gulf Coast year", the_year, 2),
             ("Your first month", first_month, 3)]
    for month in range(1, 13):
        pages.append((MONTH_NAMES[month - 1],
                      lambda cv, m=month: month_page(cv, m), None))
    pages.extend([
        ("The Big Ticket Watch List", watch_list, None),
        ("How to find out", find_out, None),
        ("Calendars for your phone", digital, None),
        (content.LICENCE_TITLE, closing, None),
    ])

    months_key = None
    for i, (title, draw, _) in enumerate(pages):
        number = i + 1
        key = "p{0}".format(number)
        c.bookmarkPage(key)
        if title == "January":
            # The group heading and January land on the same page, but they
            # cannot share a destination key: reportlab stores outline entries
            # against the key, so the second title would overwrite the first
            # and the group would come out named "January" too.
            months_key = "months"
            c.bookmarkPage(months_key)
            c.addOutlineEntry("The twelve months", months_key, level=0,
                              closed=True)
            c.addOutlineEntry(title, key, level=1)
        elif months_key and title in MONTH_NAMES:
            c.addOutlineEntry(title, key, level=1)
        else:
            c.addOutlineEntry(title, key, level=0)

        draw(c)
        if number > 1:
            footer(c, number)
        c.showPage()

    c.save()
    return len(pages)


def listing_hero(path):
    """
    The first listing image, which is the one that has to work at thumbnail
    size in a search grid.

    Etsy crops the grid thumbnail to 4:3, so a portrait page uploaded as the
    first image gets its title sliced off. This is a 4:3 composition instead,
    with four real pages drawn into it at scale — the same code that draws the
    book, so the preview cannot show something the file does not contain.
    """
    hw, hh = 800, 600
    c = pdfcanvas.Canvas(path, pagesize=(hw, hh))
    c.setPageCompression(1)

    c.setFillColor(PAPER_2)
    c.rect(0, 0, hw, hh, stroke=0, fill=1)

    band_h = 158
    c.setFillColor(DEEP)
    c.rect(0, hh - band_h, hw, band_h, stroke=0, fill=1)

    tracked(c, "Instant download · US Letter PDF", 0, hh - 40, size=9,
            color=SAND, space=2.6, center=hw / 2.0)
    c.setFillColor(white)
    c.setFont(SERIF_B, 34)
    c.drawCentredString(hw / 2.0, hh - 82, "The Gulf Coast")
    c.drawCentredString(hw / 2.0, hh - 118, "Home Maintenance Calendar")
    tracked(c, "20 pages · undated · never expires", 0, hh - 142, size=8.5,
            color=ON_DEEP_MUTE, space=2.2, center=hw / 2.0)

    thumbs = [cover, lambda cv: month_page(cv, 5), watch_list, find_out]
    scale = 0.29
    tw, th = W * scale, H * scale
    gap = 12
    total = tw * len(thumbs) + gap * (len(thumbs) - 1)
    x = (hw - total) / 2.0
    # Centred in the space between the title band and the closing line, rather
    # than hung off the band — otherwise the whole composition floats upward
    # and leaves a dead third at the bottom.
    y = 70 + ((hh - band_h - 70) - th) / 2.0

    for draw in thumbs:
        # A flat offset stands in for a drop shadow: reportlab has no blur, and
        # a hard grey edge at this size reads as depth anyway.
        c.setFillColor(HexColor("#ded5c2"))
        c.rect(x + 3, y - 3, tw, th, stroke=0, fill=1)
        c.setFillColor(white)
        c.rect(x, y, tw, th, stroke=0, fill=1)

        c.saveState()
        c.translate(x, y)
        c.scale(scale, scale)
        draw(c)
        c.restoreState()

        c.setStrokeColor(RULE)
        c.setLineWidth(0.6)
        c.rect(x, y, tw, th, stroke=1, fill=0)
        x += tw + gap

    c.setFont(SERIF_I, 15)
    c.setFillColor(INK)
    c.drawCentredString(hw / 2.0, 52,
                        "Built for salt air, humidity, termites, and a "
                        "hurricane season that runs half the year.")
    tracked(c, "Three free phone calendars included", 0, 28, size=8.5,
            color=ACCENT, space=2.2, center=hw / 2.0)

    c.save()


def listing_images(pdf_path, out_dir):
    """Raster a few pages for the Etsy listing. Optional — skipped if absent."""
    try:
        import pypdfium2 as pdfium
    except ImportError:
        print("  (pypdfium2 not installed — skipping listing images)")
        return []

    # Page numbers are 1-based in the file and 0-based here: the cover is 1,
    # January is 5, May is 9.
    wanted = [(0, "01-cover"), (4, "02-january"), (16, "03-watch-list"),
              (17, "04-how-to-find-out"), (18, "05-phone-calendars"),
              (8, "06-may"), (2, "07-the-year"), (3, "08-first-month")]
    os.makedirs(out_dir, exist_ok=True)
    written = []

    hero_pdf = os.path.join(out_dir, "00-hero.pdf")
    listing_hero(hero_pdf)
    hero_png = os.path.join(out_dir, "00-hero.png")
    pdfium.PdfDocument(hero_pdf)[0].render(scale=2000 / 800.0).to_pil().save(
        hero_png)
    written.append(hero_png)

    doc = pdfium.PdfDocument(pdf_path)
    for index, name in wanted:
        # 2000px on the long edge. Etsy wants at least 2000 on the shortest
        # side and upscales anything smaller, which looks soft.
        image = doc[index].render(scale=2000 / 792.0).to_pil()
        path = os.path.join(out_dir, name + ".png")
        image.save(path)
        written.append(path)
    return written


def main():
    register_fonts()
    os.makedirs(OUT_DIR, exist_ok=True)
    pdf_path = os.path.join(OUT_DIR, PDF_NAME)

    count = build(pdf_path)
    print("{0}  {1} pages  {2:,} bytes".format(
        pdf_path, count, os.path.getsize(pdf_path)))

    for path in listing_images(pdf_path, os.path.join(OUT_DIR, "listing")):
        print("  {0:<44} {1:,} bytes".format(path, os.path.getsize(path)))


if __name__ == "__main__":
    main()
