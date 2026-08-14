#!/usr/bin/env python3
"""
Build the Etsy shop icon and banner.

Two constraints shape this more than taste does.

The icon is shown small. Etsy renders it around 40 pixels in reviews and search,
and crops it to a circle in places. So the mark is one solid shape with a wide
margin, no thin strokes, and nothing near the corners. Anything with fine detail
turns to mush at that size, and anything near an edge gets sliced off.

And the shop is GulfCoastHomeCare, not a calendar shop. The mark deliberately
says house rather than calendar, so a second and third product do not date it.
It is the same house that sits in the site header, redrawn solid, so the shop
and the site read as the same thing.

Run:  python build_brand.py
Out:  product/brand/shop-icon.png     1000 square, for the shop icon
      product/brand/shop-banner.png   3360 x 840, the big banner
      product/brand/icon-sizes.png    proof it survives being small
"""

import os
import shutil
import subprocess
import sys

from build_printables import CHROME_CANDIDATES

OUT_DIR = os.path.join("product", "brand")

DEEP = "#0e2429"
SAND = "#d9a441"
PAPER = "#f4efe4"
MUTED = "#93a5a6"

# One path, drawn solid rather than stroked, so it holds together when small.
# Roof, walls, and a door knocked out of the wall by the even-odd fill rule.
HOUSE = (
    "M50 8 L94 44 L84 44 L84 92 L58 92 L58 62 L42 62 L42 92 L16 92 L16 44 L6 44 Z"
)

ICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="{size}" height="{size}">
  <rect width="100" height="100" fill="{deep}"/>
  <g transform="translate(50 52) scale(0.62) translate(-50 -50)">
    <path d="{house}" fill="{sand}"/>
  </g>
</svg>"""

BANNER = """<!doctype html><html><head><meta charset="utf-8"><style>
  @font-face {{ font-family: x; src: local("Georgia"); }}
  html, body {{ margin:0; padding:0; }}
  .banner {{
    width:{w}px; height:{h}px; background:{deep};
    display:flex; align-items:center; justify-content:center; gap:110px;
  }}
  .mark {{ width:360px; height:360px; flex:none; }}
  .words {{ color:{paper}; font-family:Georgia, serif; }}
  .name {{
    font-size:150px; line-height:1.02; margin:0 0 26px; letter-spacing:-.02em;
    color:#fff; font-weight:normal;
  }}
  .rule {{ width:150px; height:7px; background:{sand}; margin:0 0 30px; }}
  .tag {{
    font-family:"Segoe UI", system-ui, sans-serif; font-size:40px;
    letter-spacing:.13em; text-transform:uppercase; color:{muted}; margin:0;
  }}
</style></head><body>
  <div class="banner">
    <svg class="mark" viewBox="0 0 100 100">
      <g transform="translate(50 52) scale(0.9) translate(-50 -50)">
        <path d="{house}" fill="{sand}"/>
      </g>
    </svg>
    <div class="words">
      <p class="name">Gulf Coast<br>Home Care</p>
      <div class="rule"></div>
      <p class="tag">Tools for people who own a house down here</p>
    </div>
  </div>
</body></html>"""

SIZES = """<!doctype html><html><head><meta charset="utf-8"><style>
  html, body {{ margin:0; padding:0; background:{paper}; }}
  .row {{
    width:{w}px; height:{h}px; display:flex; align-items:center;
    justify-content:center; gap:64px; font-family:"Segoe UI", sans-serif;
  }}
  .one {{ text-align:center; color:#5b6a68; font-size:20px; }}
  .one img {{ display:block; margin:0 auto 18px; border-radius:6px; }}
  .circle img {{ border-radius:50%; }}
</style></head><body>
  <div class="row">
    <div class="one"><img src="shop-icon.png" width="200" height="200">200 px</div>
    <div class="one"><img src="shop-icon.png" width="96" height="96">96 px</div>
    <div class="one"><img src="shop-icon.png" width="40" height="40">40 px</div>
    <div class="one circle"><img src="shop-icon.png" width="120" height="120">circle crop</div>
  </div>
</body></html>"""


def find_chrome():
    for path in CHROME_CANDIDATES:
        if os.path.exists(path):
            return path
    return None


def shot(chrome, src, out, width, height):
    subprocess.run([
        chrome, "--headless", "--disable-gpu", "--no-sandbox", "--hide-scrollbars",
        "--force-device-scale-factor=1", "--default-background-color=00000000",
        "--window-size={0},{1}".format(width, height),
        "--screenshot=" + os.path.abspath(out),
        "file:///" + os.path.abspath(src).replace("\\", "/"),
    ], check=True, capture_output=True, timeout=120)


def main():
    chrome = find_chrome()
    if not chrome:
        print("No Chrome or Edge found.")
        return 1

    if os.path.isdir(OUT_DIR):
        shutil.rmtree(OUT_DIR)
    os.makedirs(OUT_DIR)

    jobs = [
        ("shop-icon", ICON.format(size=1000, deep=DEEP, sand=SAND, house=HOUSE),
         1000, 1000, "shop icon, 1000 square"),
        ("shop-banner", BANNER.format(w=3360, h=840, deep=DEEP, sand=SAND,
                                      paper=PAPER, muted=MUTED, house=HOUSE),
         3360, 840, "big banner"),
    ]

    for name, markup, w, h, label in jobs:
        ext = ".svg" if markup.lstrip().startswith("<svg") else ".html"
        src = os.path.join(OUT_DIR, "_" + name + ext)
        with open(src, "w", encoding="utf-8") as handle:
            handle.write(markup)
        out = os.path.join(OUT_DIR, name + ".png")
        shot(chrome, src, out, w, h)
        os.remove(src)
        print("  {0:<34} {1:>9,} bytes  {2}".format(
            out, os.path.getsize(out), label))

    # Proof it still reads once Etsy shrinks it.
    src = os.path.join(OUT_DIR, "_sizes.html")
    with open(src, "w", encoding="utf-8") as handle:
        handle.write(SIZES.format(w=900, h=300, paper=PAPER))
    out = os.path.join(OUT_DIR, "icon-sizes.png")
    shot(chrome, src, out, 900, 300)
    os.remove(src)
    print("  {0:<34} {1:>9,} bytes  legibility check".format(
        out, os.path.getsize(out)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
