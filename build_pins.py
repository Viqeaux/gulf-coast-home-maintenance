#!/usr/bin/env python3
"""
Render Pinterest pins from the real kit pages.

Pinterest is the discovery channel. Etsy is only the checkout, and the market
data says volume is the binding constraint, so pins have to do the work of
finding people that search never will.

Two things drive that. Pins are seen at thumbnail size first, so the headline
has to be readable when the whole image is an inch tall, which is why the type
block is a third of the pin and the page render sits under it rather than
beside it. And a pin is saved for later far more often than it is clicked, so
every pin carries the domain at the foot: the save has to still point somewhere
weeks later when the pin has been reshared past its own link.

Same approach as build_listing_images.py: every pin shows a page that is
genuinely in the kit, not an illustration of one.

Run:  python build_pins.py
Out:  product/pins/*.png   (gitignored, rebuilt in seconds)
"""

import os
import shutil
import sys

from build_printables import build_html, OUT_DIR
from build_storm_binder import build_html as build_binder_html
from build_listing_images import find_chrome, shot, split_pages

# Which document a pin's page is cut from. The kit and the binder are separate
# products with separate listings, and a pin has to be able to come from either.
DOCS = {
    "kit": build_html,
    "binder": build_binder_html,
}

PINS_DIR = os.path.join(OUT_DIR, "pins")

# Pinterest wants 2:3. Anything taller gets truncated in the feed, anything
# squarer surrenders height a competing pin will take. Designed at 1000x1500
# CSS pixels and rendered at 2x, the same trick the listing images use: the
# scale factor enlarges the rendering rather than the paper.
PIN_W, PIN_H = 1000, 1500
PIN_SCALE = 2

# Each pin is one search intent, not one product. A person looking up hurricane
# prep in June and a realtor looking for a closing gift are different people who
# will never type the other's words, and a single pin cannot be found by both.
#
# `page` is matched on a distinctive substring of the heading, the same way the
# listing images match, since headings carry HTML entities that would not
# survive an exact comparison.
#
# `zoom`, `lift` and `crop` exist because the kit's pages are not equally full.
# A month page runs to the bottom margin and sits happily at the defaults, but
# the cover and the year chart carry deliberate white space that reads as a
# printing fault once it is dropped into a pin. So the sheet is cut at `crop`,
# where its content actually ends, and the pin's own sand ground fills the rest
# rather than an acre of white. `lift` shifts the sheet up inside that cut, for
# a page whose content starts low, and `zoom` sizes the result. Both are in
# unscaled page pixels; a Letter sheet is 1056 tall.
PINS = [
    {
        "name": "01-free-calendar",
        "page": "Gulf Coast year",
        "eyebrow": "Texas to Florida",
        "head": "The home maintenance calendar built for the Gulf&nbsp;Coast",
        "sub": "Heat, humidity, termites, hurricane season. Free, and it "
               "subscribes straight to your phone.",
        "zoom": 1.15,
        "lift": 40,
        "crop": 520,
    },
    {
        "name": "02-hurricane-season",
        "page": "June",
        "eyebrow": "Before the season starts",
        "head": "What to do to your house before hurricane&nbsp;season",
        "sub": "June through November, month by month, for a house on the "
               "Gulf Coast.",
    },
    {
        "name": "03-summer-heat",
        "page": "August",
        "eyebrow": "July and August",
        "head": "Gulf Coast summer is harder on a house than winter&nbsp;is",
        "sub": "Fourteen of the thirty-six tasks exist because of heat and "
               "humidity. Here is when to do them.",
    },
    {
        "name": "04-first-month",
        "page": "Your first month",
        "eyebrow": "Just bought a house",
        "head": "The first month in a new house, in the order it should&nbsp;happen",
        "sub": "Find the shutoffs, learn the breaker box, start the list. One "
               "page, no guessing.",
        "zoom": 0.95,
        "crop": 950,
    },
    {
        "name": "05-watch-list",
        "page": "Big Ticket Watch List",
        "eyebrow": "The Big Ticket Watch List",
        "head": "How long does a water heater actually&nbsp;last?",
        "sub": "Roof, HVAC, water heater, and the rest. Write down the year it "
               "went in and stop being surprised.",
    },
    {
        "name": "06-realtor",
        "page": "cover",
        "eyebrow": "For real estate agents",
        "head": "A closing gift your clients actually keep",
        "sub": "Twenty-seven pages branded with your name, brokerage and "
               "license, plus a leave-behind for the table.",
        "zoom": 1.12,
        "lift": 330,
        "crop": 470,
    },

    # --- the storm season binder ------------------------------------------
    # The binder is the only product with a clock on it. Peak Atlantic season
    # is around September 10 and the search terms are close to dead in winter,
    # so 07 is the seasonal pin and 08 is the hedge: home inventory and
    # insurance claims are searched all year by people who have just bought a
    # house or just been told by their agent to make a list.
    {
        "name": "07-storm-countdown",
        "doc": "binder",
        "page": "The countdown",
        "eyebrow": "When a storm is named",
        "head": "It is not what you buy. It is when you buy&nbsp;it.",
        "sub": "Almost nobody fails because they did not know to get water. They "
               "fail because they got it on the wrong day. The countdown starts "
               "five to seven days out.",
        "zoom": 1.05,
        "crop": 810,
    },
    {
        "name": "08-home-inventory",
        "doc": "binder",
        "page": "The home inventory",
        "eyebrow": "The largest number in your policy",
        "head": "Could you list everything you own, from&nbsp;memory?",
        "sub": "Contents coverage runs 50 to 70 percent of what the house is "
               "insured for. To collect it you have to say what you owned, and "
               "the adjuster will not help you remember.",
        "zoom": 1.05,
        "crop": 800,
    },
]

# The pin ground is the site's own paper and deep tokens. A visitor who saves a
# pin and later lands on the site should recognize it as the same thing, and the
# palette is the only part of the site a 1000 pixel image can carry.
PIN = """<!doctype html><html><head><meta charset="utf-8"><style>
  {css}
  html, body {{ margin:0; padding:0; background:#f4efe4; }}
  .pin {{
    width:{w}px; height:{h}px; display:flex; flex-direction:column;
    background:#f4efe4; overflow:hidden;
  }}
  .top {{
    background:#0e2429; color:#e8e2d4; padding:52px 62px 46px; flex:none;
  }}
  .eyebrow {{
    font:700 21px/1 "Segoe UI", sans-serif; letter-spacing:.20em;
    text-transform:uppercase; color:#c08b2e; margin:0 0 22px;
  }}
  .top h1 {{
    font:400 62px/1.09 Georgia, serif; color:#fffdf7; margin:0 0 20px;
    letter-spacing:-.02em;
  }}
  .top p {{
    font:400 27px/1.42 Georgia, serif; color:#93a5a6; margin:0;
  }}
  /* The page is clipped rather than shrunk to fit. A whole sheet scaled into
     the remaining height renders its body type below legibility, and the point
     of showing a real page is that a buyer can read it. */
  .show {{
    flex:1; display:flex; justify-content:center; align-items:center;
    overflow:hidden; padding:38px 0;
  }}
  .lens {{
    flex:none; overflow:hidden; transform-origin:top center; background:#fff;
    box-shadow:0 18px 46px rgba(23,33,31,.24);
  }}
  .lens .page {{ margin:0; background:#fff; page-break-after:auto; }}
  .foot {{
    flex:none; background:#0e2429; color:#e8e2d4; text-align:center;
    padding:26px 20px; font:700 27px/1 "Segoe UI", sans-serif;
    letter-spacing:.06em;
  }}
</style></head><body>
<div class="pin">
  <div class="top">
    <div class="eyebrow">{eyebrow}</div>
    <h1>{head}</h1>
    <p>{sub}</p>
  </div>
  <div class="show">
    <div class="lens" style="height:{crop}px; transform:scale({zoom})">
      <div style="transform:translateY(-{lift}px)">{page}</div>
    </div>
  </div>
  <div class="foot">gulfcoasthomemaintenance.com</div>
</div></body></html>
"""


def main():
    chrome = find_chrome()
    if not chrome:
        print("No Chrome or Edge found.")
        return 1

    if os.path.isdir(PINS_DIR):
        shutil.rmtree(PINS_DIR)
    os.makedirs(PINS_DIR)

    # Each document is rendered once and reused. Both are slow to build and a
    # pin only ever needs one page out of either.
    built = {}

    def document(key):
        if key not in built:
            html, _ = DOCS[key]()
            built[key] = split_pages(html)
        return built[key]

    def find_page(pages, needle):
        """First page whose heading contains this text. Exact for the cover,
        which has no heading of its own."""
        if needle == "cover":
            return next((p for h, p in pages if h == "cover"), None)
        return next((p for h, p in pages if needle.lower() in h.lower()), None)

    tmp = os.path.join(PINS_DIR, "_tmp.html")
    made = 0

    for spec in PINS:
        css, pages = document(spec.get("doc", "kit"))
        match = find_page(pages, spec["page"])
        if match is None:
            print("  ! no page titled {0!r}, skipped".format(spec["page"]))
            continue
        with open(tmp, "w", encoding="utf-8") as handle:
            handle.write(PIN.format(
                css=css, w=PIN_W, h=PIN_H, page=match,
                zoom=spec.get("zoom", 0.80), lift=spec.get("lift", 0),
                crop=spec.get("crop", 1056),
                eyebrow=spec["eyebrow"], head=spec["head"], sub=spec["sub"]))
        out = os.path.join(PINS_DIR, spec["name"] + ".png")
        # Fractional scale plus subpixel antialiasing leaves colored fringes on
        # the page type, the same problem the realtor compositions hit.
        shot(chrome, tmp, out, PIN_W, PIN_H, PIN_SCALE,
             extra=["--disable-lcd-text"])
        print("  {0}  {1:,} bytes".format(out, os.path.getsize(out)))
        made += 1

    os.remove(tmp)
    print("\n{0} pins in {1}".format(made, PINS_DIR))
    return 0


if __name__ == "__main__":
    sys.exit(main())
