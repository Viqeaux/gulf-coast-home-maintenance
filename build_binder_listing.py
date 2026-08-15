#!/usr/bin/env python3
"""
Render Etsy listing images from the real storm binder pages.

Same rule as build_listing_images.py, and the same machinery: every image is a
render of a page genuinely in the PDF, because Etsy requires listing photos to
represent the actual item and printable buyers scroll specifically to see the
pages.

What is different is which pages sell it. The kit's photos lead with pages you
read. This one leads with pages you fill in, and three of the eight are mostly
blank lines on purpose. That is the product: a buyer has to understand within
two images that this is a thing they write in, not a thing they read.

Run:  python build_binder_listing.py
Out:  product/listing-binder/*.png   (gitignored, rebuilt in seconds)
"""

import os
import shutil
import sys

from build_listing_images import (HERO_H, HERO_SCALE, HERO_W, PAGE_H,
                                  PAGE_SCALE, PAGE_W, find_chrome, shot,
                                  split_pages)
from build_printables import OUT_DIR
from build_storm_binder import build_html

LISTING_DIR = os.path.join(OUT_DIR, "listing-binder")

# Matched on a distinctive substring of the heading rather than the whole
# thing, since the headings carry entities that would not survive an exact
# comparison. Order is the order a buyer should meet them.
# Nine plus the hero is ten, which is Etsy's maximum.
#
# The two inventory images are deliberately a pair and deliberately in this
# order. A blank ruled sheet on its own undersells: a shopper scrolling past it
# sees an empty page rather than the product. The intro page goes first because
# it carries a worked example line, a real make, model, serial and price, which
# says what the standard is. The Kitchen sheet follows and says how much room
# there is to meet it.
WANTED = [
    ("01-cover", "cover"),
    ("02-policies", "Policies and coverage"),
    ("03-inventory-how", "The home inventory"),
    ("04-inventory-kitchen", "Kitchen"),
    ("05-countdown", "The countdown"),
    ("06-shutdown", "Shutdown sequence"),
    ("07-claim-log", "Claim call log"),
    ("08-vetting", "Vetting a contractor"),
    ("09-supplies", "Water and supplies"),
]

HERO = """<!doctype html><html><head><meta charset="utf-8"><style>
  {css}
  html, body {{ margin:0; padding:0; background:#f4efe4; }}
  .frame {{
    width:{w}px; height:{h}px; display:flex; align-items:center;
    justify-content:center; gap:46px; background:#f4efe4;
    font-family: Georgia, serif;
  }}
  /* Bigger and further apart than the kit's stack. The binder cover is mostly
     white space by design, so at the kit's 0.74 it reads as a blank sheet at
     thumbnail size, and the back page has to clear the front by enough to
     show that the thing behind it is a form. */
  .stack {{ position:relative; width:800px; height:940px; flex:none; }}
  .stack .page {{
    position:absolute; background:#fff; transform-origin:top left;
    box-shadow:0 16px 44px rgba(23,33,31,.20);
  }}
  .stack .back {{ left:132px; top:0; z-index:1; transform:scale(0.82) rotate(5deg); }}
  .stack .front {{ left:0; top:66px; z-index:2; transform:scale(0.82); }}
  .say {{ width:600px; }}
  .say h1 {{
    font:400 62px/1.06 Georgia, serif; color:#17211f; margin:0 0 18px;
    letter-spacing:-.02em;
  }}
  .say .rule {{ width:120px; height:5px; background:#9c3722; margin:0 0 22px; }}
  .say p {{ font:400 25px/1.45 Georgia, serif; color:#3d4a48; margin:0 0 26px; }}
  .badge {{
    display:inline-block; font:700 19px/1 "Segoe UI", sans-serif;
    letter-spacing:.18em; text-transform:uppercase; color:#fff;
    background:#9c3722; padding:15px 22px; border-radius:3px;
  }}
</style></head><body>
<div class="frame">
  <div class="stack">{back}{front}</div>
  <div class="say">
    <h1>Hurricane prep,<br>including the<br>part afterward</h1>
    <div class="rule"></div>
    <p>Your policy numbers, a room by room inventory, the countdown, and the
       claim logs that decide how much you actually get paid.</p>
    <span class="badge">33 pages &middot; fillable &middot; undated</span>
  </div>
</div></body></html>
"""


def main():
    chrome = find_chrome()
    if not chrome:
        print("No Chrome or Edge found.")
        return 1

    if os.path.isdir(LISTING_DIR):
        shutil.rmtree(LISTING_DIR)
    os.makedirs(LISTING_DIR)

    html, _ = build_html()
    css, pages = split_pages(html)

    def find_page(needle):
        if needle == "cover":
            return next((p for h, p in pages if h == "cover"), None)
        return next((p for h, p in pages if needle.lower() in h.lower()), None)

    tmp = os.path.join(LISTING_DIR, "_tmp.html")
    made = 0

    for name, heading in WANTED:
        match = find_page(heading)
        if match is None:
            print("  ! no page titled {0!r}, skipped".format(heading))
            continue
        with open(tmp, "w", encoding="utf-8") as handle:
            handle.write(
                "<!doctype html><html><head><meta charset='utf-8'><style>{0}\n"
                "html,body{{margin:0;padding:0;background:#fff}}\n"
                ".page{{box-shadow:none;margin:0;page-break-after:auto}}</style>"
                "</head><body>{1}</body></html>"
                .format(css, match))
        out = os.path.join(LISTING_DIR, name + ".png")
        shot(chrome, tmp, out, PAGE_W, PAGE_H, PAGE_SCALE)
        print("  {0}  {1:,} bytes".format(out, os.path.getsize(out)))
        made += 1

    # The 4:3 thumbnail. The countdown sits behind the cover: at four inches
    # wide the only thing legible on any page is structure, and the countdown
    # is the one page carrying red rules, bold headings and a column of
    # checkboxes. A ruled form page just reads as blank paper that far out.
    front = find_page("cover") or ""
    back = find_page("The countdown") or ""
    with open(tmp, "w", encoding="utf-8") as handle:
        handle.write(HERO.format(
            css=css, w=HERO_W, h=HERO_H,
            back=back.replace('class="page', 'class="back page', 1),
            front=front.replace('class="page', 'class="front page', 1)))
    out = os.path.join(LISTING_DIR, "00-hero.png")
    shot(chrome, tmp, out, HERO_W, HERO_H, HERO_SCALE)
    print("  {0}  {1:,} bytes  (4:3 thumbnail)".format(out, os.path.getsize(out)))
    made += 1

    os.remove(tmp)
    print("\n{0} images in {1}".format(made, LISTING_DIR))
    return 0


if __name__ == "__main__":
    sys.exit(main())
