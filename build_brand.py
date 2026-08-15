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
Out:  product/brand/shop-icon.png        1000 square, for the shop icon
      product/brand/shop-banner.png      3360 x 840, the big banner
      product/brand/pinterest-cover.png        1600 x 900, flat profile cover
      product/brand/pinterest-cover-photo.png  1600 x 900, over the hero photo
      product/brand/icon-sizes.png       proof it survives being small
"""

import os
import shutil
import subprocess
import sys

from build_printables import CHROME_CANDIDATES

OUT_DIR = os.path.join("product", "brand")

# The site's own icons, unlike everything else here, are served rather than
# uploaded, so they land in docs/ and are committed. OUT_DIR gets wiped on every
# run, which is exactly why they cannot live in it.
SITE_DIR = "docs"

# The served hero, reached from inside OUT_DIR where the markup is written. It
# is already 1600 x 900, which is exactly the cover's aspect, so nothing is
# cropped away by using it.
PHOTO = "../../docs/img/hero-1600.jpg"

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

# The favicon carries no width or height, so it scales to whatever slot the
# browser puts it in. The glyph runs larger than the shop icon's 0.62: a tab
# favicon is 16 px, and at that size the shop icon's generous margin reads as a
# dark square with something indistinct inside it.
#
# Deliberately not theme-aware. A favicon that inverts is a favicon people stop
# recognizing, and the deep ground is the brand's own anyway.
# The {dims} slot is empty for the served file, so it scales to whatever slot
# the browser gives it. It is filled in when Chrome rasterizes the PNGs: an SVG
# opened as a top-level document with no intrinsic size is laid out at the
# default replaced-element size, which rendered a white page with a sliver of
# the icon down one edge.
FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"{dims}>
  <rect width="100" height="100" fill="{deep}"/>
  <g transform="translate(50 52) scale(0.74) translate(-50 -50)">
    <path d="{house}" fill="{sand}"/>
  </g>
</svg>
"""

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

# The Pinterest profile cover. 16:9, uploaded at 1600 x 900 for retina. Older
# guides say 1200 x 600, which is out of date: Pinterest displays 16:9 now and
# crops a 2:1 image top and bottom.
#
# It does not repeat the shop name, the way the Etsy banner does. Pinterest
# already prints the profile name in large type right beside this, so a second
# copy of it would spend the whole image saying what is said above it anyway.
# The cover's job is the thing the name cannot carry: where this is for, and
# what it is about.
#
# Everything sits centered and well inside the edges. Pinterest narrows the
# crop on phones, and a composition that runs to the corners loses its ends.
COVER = """<!doctype html><html><head><meta charset="utf-8"><style>
  html, body {{ margin:0; padding:0; }}
  .cover {{
    width:{w}px; height:{h}px; background:{deep};
    display:flex; flex-direction:column; align-items:center;
    justify-content:center; text-align:center;
  }}
  .mark {{ width:132px; height:132px; margin:0 0 40px; }}
  .head {{
    font-family:Georgia, serif; font-size:96px; line-height:1.04;
    letter-spacing:-.02em; color:#fff; margin:0 0 30px; font-weight:normal;
  }}
  .rule {{ width:132px; height:6px; background:{sand}; margin:0 0 32px; }}
  .tag {{
    font-family:"Segoe UI", system-ui, sans-serif; font-size:27px;
    letter-spacing:.15em; text-transform:uppercase; color:{muted}; margin:0;
  }}
</style></head><body>
  <div class="cover">
    <svg class="mark" viewBox="0 0 100 100">
      <g transform="translate(50 52) scale(0.9) translate(-50 -50)">
        <path d="{house}" fill="{sand}"/>
      </g>
    </svg>
    <p class="head">Built for the Gulf&nbsp;Coast</p>
    <div class="rule"></div>
    <p class="tag">Texas to Florida &middot; Heat, humidity, termites, hurricane season</p>
  </div>
</body></html>"""

# The same cover over the site's hero photograph, which is already exactly 16:9.
# Pinterest is a visual surface and a flat card is the weaker play there, so
# this is the one to reach for first. The scrim is the site's own, so a visitor
# who arrives here from a pin recognizes the same place.
#
# No house mark on this one. There is already a house in the photograph, and a
# second one floating above it in gold reads as clutter rather than as a logo.
COVER_PHOTO = """<!doctype html><html><head><meta charset="utf-8"><style>
  html, body {{ margin:0; padding:0; background:{deep}; }}
  .cover {{
    position:relative; width:{w}px; height:{h}px; overflow:hidden;
    background:{deep};
  }}
  .cover img {{
    position:absolute; inset:0; width:100%; height:100%;
    object-fit:cover; object-position:62% 42%;
  }}
  .scrim {{
    position:absolute; inset:0;
    background:
      linear-gradient(to bottom,
        rgba(14,36,41,.55) 0%, rgba(14,36,41,.30) 30%,
        rgba(14,36,41,.86) 78%, rgba(14,36,41,.97) 100%);
  }}
  .say {{
    position:absolute; inset:0; display:flex; flex-direction:column;
    align-items:center; justify-content:center; text-align:center;
  }}
  .head {{
    font-family:Georgia, serif; font-size:96px; line-height:1.04;
    letter-spacing:-.02em; color:#fff; margin:0 0 28px; font-weight:normal;
    text-shadow:0 2px 22px rgba(14,36,41,.75);
  }}
  .rule {{ width:132px; height:6px; background:{sand}; margin:0 0 30px; }}
  .tag {{
    font-family:"Segoe UI", system-ui, sans-serif; font-size:27px;
    letter-spacing:.15em; text-transform:uppercase; color:#cfd8d4; margin:0;
    text-shadow:0 2px 16px rgba(14,36,41,.85);
  }}
</style></head><body>
  <div class="cover">
    <img src="{photo}" alt="">
    <div class="scrim"></div>
    <div class="say">
      <p class="head">Built for the Gulf&nbsp;Coast</p>
      <div class="rule"></div>
      <p class="tag">Texas to Florida &middot; Heat, humidity, termites, hurricane season</p>
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


def build_site_icons(chrome):
    """Write the icons the site itself serves, into docs/.

    Three files rather than one, because the three consumers want different
    things. Modern browsers take the SVG and scale it. iOS ignores SVG entirely
    and wants a 180 px PNG for a home screen shortcut. Android's install prompt
    and most link unfurlers want 512.

    No .ico. It exists for browsers nobody on this site is running, and the
    bare /favicon.ico request 404s harmlessly when a link element is present.
    """
    os.makedirs(SITE_DIR, exist_ok=True)

    svg_path = os.path.join(SITE_DIR, "favicon.svg")
    with open(svg_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(FAVICON.format(dims="", deep=DEEP, sand=SAND, house=HOUSE))
    print("  {0:<34} {1:>9,} bytes  scalable, every modern browser".format(
        svg_path, os.path.getsize(svg_path)))

    for size, label in ((180, "apple touch icon"), (512, "Android and unfurlers")):
        src = os.path.join(SITE_DIR, "_icon.svg")
        with open(src, "w", encoding="utf-8") as handle:
            handle.write(FAVICON.format(
                dims=' width="{0}" height="{0}"'.format(size),
                deep=DEEP, sand=SAND, house=HOUSE))
        out = os.path.join(SITE_DIR, "icon-{0}.png".format(size))
        shot(chrome, src, out, size, size)
        os.remove(src)
        print("  {0:<34} {1:>9,} bytes  {2}".format(
            out, os.path.getsize(out), label))


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
        ("pinterest-cover", COVER.format(w=1600, h=900, deep=DEEP, sand=SAND,
                                         muted=MUTED, house=HOUSE),
         1600, 900, "Pinterest profile cover, 16:9"),
        ("pinterest-cover-photo",
         COVER_PHOTO.format(w=1600, h=900, deep=DEEP, sand=SAND, house=HOUSE,
                            photo=PHOTO),
         1600, 900, "Pinterest profile cover over the hero photo"),
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

    # These are site assets, not shop uploads, so they are committed and served.
    build_site_icons(chrome)
    return 0


if __name__ == "__main__":
    sys.exit(main())
