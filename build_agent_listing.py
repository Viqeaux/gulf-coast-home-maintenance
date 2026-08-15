#!/usr/bin/env python3
"""
Render the Etsy listing images for the realtor edition, from the real pages.

The kit's listing has to prove what is inside. This one has to prove two things
the kit never had to: that the branding really does run on every page, and that
putting it there takes the buyer about a minute. So two of these are
compositions rather than page shots, a footer close-up and a blank-versus-filled
pair.

The sample brand is deliberately the words "Your Name" and "Your Brokerage"
rather than an invented agent at an invented firm. It documents itself in the
photo, and it cannot be mistaken for a real brokerage. The logo is generated
here as an SVG, so no binary placeholder enters the repo.

Run:  python build_agent_listing.py
Out:  product/listing-realtor/*.png   (gitignored, rebuilt in seconds)
"""

import os
import shutil
import sys

import build_agent_edition as agent
import build_printables as bp
from build_listing_images import (HERO_H, HERO_SCALE, HERO_W, PAGE_H,
                                  PAGE_SCALE, PAGE_W, find_chrome, shot,
                                  split_pages)

LISTING_DIR = os.path.join(bp.OUT_DIR, "listing-realtor")

SAMPLE = {
    "enabled": True,
    "agent": "Your Name",
    "brokerage": "Your Brokerage",
    "phone": "Your Phone",
    "license": "Your License #",
}

BLANK = dict(SAMPLE, agent="", brokerage="", phone="", license="", logo="")

SAMPLE_LOGO = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 80">
  <rect x="2" y="2" width="76" height="76" rx="8" fill="none"
        stroke="#17211f" stroke-width="5"/>
  <path d="M18 44 L40 24 L62 44 L62 62 L18 62 Z" fill="none" stroke="#17211f"
        stroke-width="5" stroke-linejoin="round"/>
  <text x="94" y="40" font-family="Georgia, serif" font-size="26"
        fill="#17211f">Your Logo</text>
  <text x="95" y="63" font-family="Segoe UI, sans-serif" font-size="13"
        letter-spacing="3" fill="#5b6a68">HERE</text>
</svg>
"""

# Page shots, matched on a distinctive substring of the heading.
WANTED = [
    ("04-watch-list", "Big Ticket Watch List"),
    ("05-the-year", "Gulf Coast year"),
    ("06-first-month", "Your first month"),
]

FRAME_HEAD = """<!doctype html><html><head><meta charset="utf-8"><style>
  {css}
  html, body {{ margin:0; padding:0; background:#f4efe4; }}
  .frame {{
    width:{w}px; height:{h}px; box-sizing:border-box; background:#f4efe4;
    font-family: Georgia, serif; display:flex; flex-direction:column;
    align-items:center; justify-content:center; gap:38px; padding:56px;
  }}
  .page {{ background:#fff; box-shadow:0 16px 44px rgba(23,33,31,.20); }}
  .cap {{ text-align:center; }}
  .cap h1 {{
    font:400 {h1}px/1.1 Georgia, serif; color:#17211f; margin:0 0 14px;
    letter-spacing:-.02em;
  }}
  .cap p {{ font:400 {p}px/1.4 Georgia, serif; color:#3d4a48; margin:0; }}
  .badge {{
    display:inline-block; font:700 19px/1 "Segoe UI", sans-serif;
    letter-spacing:.18em; text-transform:uppercase; color:#fff;
    background:#0f5e6b; padding:15px 22px; border-radius:3px;
  }}
</style></head><body>
"""

HERO = FRAME_HEAD + """
<div class="frame" style="flex-direction:row; gap:46px;">
  <div style="position:relative; width:660px; height:900px; flex:none;">
    <div style="position:absolute; left:96px; top:0; z-index:1;
                transform:scale(0.70) rotate(4deg); transform-origin:top left;">
      {back}
    </div>
    <div style="position:absolute; left:0; top:56px; z-index:2;
                transform:scale(0.70); transform-origin:top left;">
      {front}
    </div>
  </div>
  <div style="width:640px;">
    <h1 style="font:400 62px/1.06 Georgia, serif; color:#17211f; margin:0 0 18px;
               letter-spacing:-.02em;">Your name on<br>every page</h1>
    <div style="width:120px; height:5px; background:#a8761f; margin:0 0 22px;"></div>
    <p style="font:400 25px/1.45 Georgia, serif; color:#3d4a48; margin:0 0 26px;">
      27 pages built for the Gulf Coast, branded with your details, and licensed
      to print for every client you close.</p>
    <span class="badge">Type it once &middot; print forever</span>
  </div>
</div></body></html>
"""

# The footer strip, genuinely doubled. Shows the bottom of a real interior page,
# which is the only way to prove the mark is not just on the cover.
#
# transform-origin is bottom left so the page's own bottom edge stays pinned to
# the bottom of the crop. A page is 816 CSS px wide, so at scale 2 the strip is
# 1632 wide and shows twice whatever height the crop is set to.
FOOTER_SHOT = FRAME_HEAD + """
<div class="frame">
  <div class="cap">
    <h1>It runs on all 27 pages</h1>
    <p>Not just the cover. Every page carries your logo and your name.</p>
  </div>
  <div style="width:{strip_w}px; height:{strip_h}px; overflow:hidden;
              position:relative; background:#fff; text-align:left;
              box-shadow:0 16px 44px rgba(23,33,31,.20);">
    <div style="position:absolute; left:0; bottom:0; width:816px;
                transform:scale(2); transform-origin:bottom left;">{page}</div>
  </div>
  <div class="cap"><p style="font-size:22px; color:#5b6a68;">
    Shown at twice actual size</p></div>
</div></body></html>
"""

# The cover before and after. text-align has to be reset on the sheet wrapper:
# the captions below need centering, and without the reset the page inherits it
# and every left-aligned line on the real cover comes out centered.
# The cover before and after. Both captions name who is acting, because the
# objection this image exists to kill is "this is made to order and I will be
# waiting on the seller". A caption about elapsed time reads as the seller's
# turnaround, which argues the opposite of the point.
#
# text-align also has to be reset on each sheet wrapper: the captions need
# centering, and without the reset the page inherits it and every left-aligned
# line on the real cover comes out centered.
PAIR = FRAME_HEAD + """
<div class="frame" style="gap:34px; padding:44px 40px;">
  <div class="cap">
    <h1>You fill it in yourself</h1>
    <p>No proofs, no waiting, and nothing to reorder for the next client.</p>
  </div>
  <div style="display:flex; flex-direction:row; gap:56px; align-items:center;">
    <div style="text-align:center;">
      <div style="width:640px; height:828px; overflow:hidden; margin:0 auto 24px;
                  box-shadow:0 16px 44px rgba(23,33,31,.20); background:#fff;">
        <div style="transform:scale(0.784); transform-origin:top left;
                    width:816px; text-align:left;">{blank}</div>
      </div>
      <p style="font:700 23px/1 'Segoe UI',sans-serif; letter-spacing:.16em;
                text-transform:uppercase; color:#5b6a68; margin:0;">
        What you download</p>
    </div>
    <div style="font:400 70px/1 Georgia,serif; color:#a8761f;
                margin-bottom:46px;">&rarr;</div>
    <div style="text-align:center;">
      <div style="width:640px; height:828px; overflow:hidden; margin:0 auto 24px;
                  box-shadow:0 16px 44px rgba(23,33,31,.20); background:#fff;">
        <div style="transform:scale(0.784); transform-origin:top left;
                    width:816px; text-align:left;">{filled}</div>
      </div>
      <p style="font:700 23px/1 'Segoe UI',sans-serif; letter-spacing:.16em;
                text-transform:uppercase; color:#0f5e6b; margin:0;">
        Fully customized</p>
    </div>
  </div>
</div></body></html>
"""

# Set at page size rather than 4:3, for two reasons. It sits beside eight
# portrait pages in the carousel, and build_video.py fixes frame height and
# derives width, so a wide card would overflow a square video frame.
LICENSE_CARD = """<!doctype html><html><head><meta charset="utf-8"><style>
  html, body {{ margin:0; padding:0; background:#fff; }}
  .sheetcard {{
    width:816px; height:1056px; box-sizing:border-box; padding:96px 84px;
    display:flex; flex-direction:column; justify-content:center;
    text-align:center; font-family:Georgia, serif; background:#fff;
  }}
  .sheetcard .kick {{
    font:700 13px/1 "Segoe UI",sans-serif; letter-spacing:.2em;
    text-transform:uppercase; color:#a8761f; margin:0 0 30px;
  }}
  .sheetcard h1 {{ font:400 52px/1.12 Georgia,serif; color:#17211f; margin:0;
                   letter-spacing:-.02em; }}
  .sheetcard .rule {{ width:110px; height:4px; background:#a8761f; margin:34px auto; }}
  .sheetcard p {{ font:400 23px/1.55 Georgia,serif; color:#3d4a48; margin:0; }}
  .sheetcard .small {{ font-size:19px; color:#5b6a68; margin-top:34px; }}
</style></head><body>
<div class="sheetcard">
  <p class="kick">How you may use it</p>
  <h1>Print it for every<br>client you close</h1>
  <div class="rule"></div>
  <p>A client gifting license. As many copies as you like, for as many clients
     as you close, for as long as you are licensed.</p>
  <p class="small">Not a per-client fee. Not a subscription. Not a reorder.</p>
</div></body></html>
"""


def build_pages(brand):
    """Return (css, {heading: page_html}) for the leave-behind and the kit."""
    bp.BRAND.update(brand)
    lb_html, _ = agent.leave_behind_html()
    kit_html, _ = bp.build_html()

    css, lb_pages = split_pages(lb_html)
    _, kit_pages = split_pages(kit_html)
    return css, lb_pages, kit_pages


def pick(pages, needle):
    if needle == "cover":
        return next((p for h, p in pages if h == "cover"), None)
    return next((p for h, p in pages if needle.lower() in h.lower()), None)


# The compositions place real pages at fractional scale, where Chrome's subpixel
# antialiasing puts colored fringes on small type. Grayscale antialiasing costs
# a little crispness and looks clean at any size.
CRISP = ("--disable-lcd-text",)


def write_shot(chrome, tmp, html, out, w, h, scale, extra=None):
    with open(tmp, "w", encoding="utf-8") as handle:
        handle.write(html)
    shot(chrome, tmp, out, w, h, scale, extra)
    print("  {0}  {1:,} bytes".format(out, os.path.getsize(out)))


def main():
    chrome = find_chrome()
    if not chrome:
        print("No Chrome or Edge found.")
        return 1

    if os.path.isdir(LISTING_DIR):
        shutil.rmtree(LISTING_DIR)
    os.makedirs(LISTING_DIR)

    logo_path = os.path.join(LISTING_DIR, "_sample-logo.svg")
    with open(logo_path, "w", encoding="utf-8") as handle:
        handle.write(SAMPLE_LOGO)

    css, lb, kit = build_pages(dict(SAMPLE, logo=logo_path))
    _, lb_blank, _ = build_pages(BLANK)

    tmp = os.path.join(LISTING_DIR, "_tmp.html")
    plain = ("html,body{margin:0;padding:0;background:#fff}"
             ".page{box-shadow:none;margin:0;page-break-after:auto}")

    def page_doc(page_html):
        return ("<!doctype html><html><head><meta charset='utf-8'><style>{0}\n{1}"
                "</style></head><body>{2}</body></html>"
                .format(css, plain, page_html))

    cover = pick(lb, "cover")
    blank_cover = pick(lb_blank, "cover")
    may = pick(kit, "May")

    # 00, the 4:3 thumbnail. Everything else is portrait.
    write_shot(chrome, tmp, HERO.format(
        css=css, w=HERO_W, h=HERO_H, h1=62, p=25,
        front=cover, back=may),
        os.path.join(LISTING_DIR, "00-hero.png"), HERO_W, HERO_H, HERO_SCALE,
        CRISP)

    # 01, the branded cover on its own.
    write_shot(chrome, tmp, page_doc(cover),
               os.path.join(LISTING_DIR, "01-cover.png"),
               PAGE_W, PAGE_H, PAGE_SCALE)

    # 02, the proof it is not only the cover.
    write_shot(chrome, tmp, FOOTER_SHOT.format(
        css=css, w=HERO_W, h=HERO_H, h1=56, p=26,
        strip_w=1632, strip_h=240, page=may),
        os.path.join(LISTING_DIR, "02-footer.png"), HERO_W, HERO_H, HERO_SCALE,
        CRISP)

    # 03, the proof it is self-serve.
    write_shot(chrome, tmp, PAIR.format(
        css=css, w=HERO_W, h=HERO_H, h1=56, p=26,
        blank=blank_cover, filled=cover),
        os.path.join(LISTING_DIR, "03-self-serve.png"), HERO_W, HERO_H,
        HERO_SCALE, CRISP)

    # 04 to 06, the pages that carry the leave-behind.
    for name, heading in WANTED:
        match = pick(lb, heading)
        if match is None:
            print("  ! no page titled {0!r}, skipped".format(heading))
            continue
        write_shot(chrome, tmp, page_doc(match),
                   os.path.join(LISTING_DIR, name + ".png"),
                   PAGE_W, PAGE_H, PAGE_SCALE)

    # 07, a month page, so the 27 do not have to be taken on trust.
    write_shot(chrome, tmp, page_doc(may),
               os.path.join(LISTING_DIR, "07-full-kit.png"),
               PAGE_W, PAGE_H, PAGE_SCALE)

    # 08, the license, stated plainly.
    write_shot(chrome, tmp, LICENSE_CARD.format(),
               os.path.join(LISTING_DIR, "08-license.png"),
               PAGE_W, PAGE_H, PAGE_SCALE)

    os.remove(tmp)
    print("\nimages in {0}".format(LISTING_DIR))
    return 0


if __name__ == "__main__":
    sys.exit(main())
