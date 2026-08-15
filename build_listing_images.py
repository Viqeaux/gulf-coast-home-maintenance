#!/usr/bin/env python3
"""
Render Etsy listing images from the real kit pages.

Etsy requires listing photos to represent the actual item, and printable buyers
scroll specifically to see the pages. So every image here is a render of a page
that is genuinely in the PDF, not an illustration of one.

The first image is composed at 4:3 on purpose. Etsy crops the search-grid
thumbnail to 4:3, which would slice the top off a portrait page.

Run:  python build_listing_images.py
Out:  product/listing/*.png   (gitignored, rebuilt in seconds)
"""

import os
import shutil
import subprocess
import sys

from build_printables import CHROME_CANDIDATES, OUT_DIR, build_html

LISTING_DIR = os.path.join(OUT_DIR, "listing")

# A Letter sheet is 816 x 1056 CSS pixels. The window has to match that exactly
# or Chrome renders the page at actual size in the corner of a larger canvas and
# pads the rest with white. Resolution comes from the device scale factor
# instead, which enlarges the rendering rather than the paper.
PAGE_W, PAGE_H = 816, 1056
PAGE_SCALE = 2.5                     # produces 2040 x 2640
HERO_W, HERO_H = 2000, 1500          # 4:3, already sized in CSS pixels
HERO_SCALE = 1

# Which sheets to show, and in what order a buyer should meet them. Matched on a
# distinctive substring of the heading rather than the whole thing, since the
# headings carry HTML entities that would not survive an exact comparison.
WANTED = [
    ("01-cover", "cover"),
    ("02-watch-list", "Big Ticket Watch List"),
    ("03-may", "May"),
    ("04-the-year", "Gulf Coast year"),
    ("05-how-to-find-out", "know when it was installed"),
    ("06-septic", "septic system"),
    ("07-first-month", "Your first month"),
    ("08-levels", "Start with one column"),
]

HERO = """<!doctype html><html><head><meta charset="utf-8"><style>
  {css}
  html, body {{ margin:0; padding:0; background:#f4efe4; }}
  .frame {{
    width:{w}px; height:{h}px; display:flex; align-items:center;
    justify-content:center; gap:46px; background:#f4efe4;
    font-family: Georgia, serif;
  }}
  /* The sheets need their own white ground. .page inherits the body background
     otherwise, and two transparent pages stacked print through each other. */
  .stack {{ position:relative; width:720px; height:900px; flex:none; }}
  .stack .page {{
    position:absolute; background:#fff; transform-origin:top left;
    box-shadow:0 16px 44px rgba(23,33,31,.20);
  }}
  .stack .back {{
    left:88px; top:0; z-index:1;
    transform:scale(0.74) rotate(4deg);
  }}
  .stack .front {{
    left:0; top:52px; z-index:2;
    transform:scale(0.74);
  }}
  .say {{ width:640px; }}
  .say h1 {{
    font:400 62px/1.06 Georgia, serif; color:#17211f; margin:0 0 18px;
    letter-spacing:-.02em;
  }}
  .say .rule {{ width:120px; height:5px; background:#a8761f; margin:0 0 22px; }}
  .say p {{ font:400 25px/1.45 Georgia, serif; color:#3d4a48; margin:0 0 26px; }}
  .badge {{
    display:inline-block; font:700 19px/1 "Segoe UI", sans-serif;
    letter-spacing:.18em; text-transform:uppercase; color:#fff;
    background:#0f5e6b; padding:15px 22px; border-radius:3px;
  }}
</style></head><body>
<div class="frame">
  <div class="stack">{back}{front}</div>
  <div class="say">
    <h1>27 pages,<br>built for this coast</h1>
    <div class="rule"></div>
    <p>Twelve months, the Big Ticket Watch List, and seven sections for whatever
       your house happens to have.</p>
    <span class="badge">Undated &middot; never expires</span>
  </div>
</div></body></html>
"""


def find_chrome():
    for path in CHROME_CANDIDATES:
        if os.path.exists(path):
            return path
    return None


def shot(chrome, html_path, out_path, width, height, scale, extra=None):
    """`extra` takes additional Chrome flags. The realtor compositions set
    --disable-lcd-text: they place small type at fractional scale, where
    subpixel antialiasing leaves colored fringes on the letters."""
    subprocess.run([
        chrome, "--headless", "--disable-gpu", "--no-sandbox",
        "--hide-scrollbars",
        "--force-device-scale-factor={0}".format(scale),
        "--default-background-color=ffffff",
        "--window-size={0},{1}".format(width, height),
    ] + list(extra or []) + [
        "--screenshot=" + os.path.abspath(out_path),
        "file:///" + os.path.abspath(html_path).replace("\\", "/"),
    ], check=True, capture_output=True, timeout=120)


def split_pages(html):
    """Return (css, [(heading, page_html), ...]) from the built document."""
    css = html.split("<style>", 1)[1].split("</style>", 1)[0]
    body = html.split("<body>", 1)[1].rsplit("</body>", 1)[0]

    pages = []
    for chunk in body.split('<section class="page')[1:]:
        page_html = '<section class="page' + chunk.rsplit("</section>", 1)[0] + "</section>"
        if "<h2" in page_html:
            heading = page_html.split("<h2", 1)[1].split(">", 1)[1].split("</h2>")[0]
            heading = heading.replace('<span class="cont">continued</span>', "")
        elif "cover-title" in page_html:
            heading = "cover"
        else:
            heading = ""
        pages.append((heading.strip(), page_html))
    return css, pages


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
        """First page whose heading contains this text. Exact for the cover,
        which has no heading of its own."""
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

    # The 4:3 thumbnail, built from the two pages that sell it fastest.
    front = find_page("cover") or ""
    back = find_page("Big Ticket Watch List") or ""
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
