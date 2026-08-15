#!/usr/bin/env python3
"""
Web images for docs/index.html: the shop grid covers and the page previews
inside each product section.

Run:  python build_site_images.py
Out:  docs/img/cover-*.jpg     the three shop grid covers
      docs/img/preview-*.jpg   three page previews per product

Reads renders the listing builders already produce. Run the matching builder
first if a source is missing; this says which one.

--------------------------------------------------------------------------
The rule these images have to live inside
--------------------------------------------------------------------------

`README.md` "What the site may publish" puts the step-by-step detail, the Big
Ticket Watch List, How To Find Out and Your First Month on the paid side.
Settled by Chad in 1.10.0. The listing builders render exactly those pages,
because on Etsy a buyer sees the photos before paying, which is Etsy's bargain
and not this site's.

**The crop is the protection, not the resolution.** Shrinking a page until the
words go soft was tried first and does not hold: at 420px the body text of a
month page is still legible, and picking a smaller number until it stops being
legible is guesswork dressed as a rule. Every preview here instead keeps only
the top slice of its page, and what falls below the cut is not in the file at
all.

On the month pages the slice is chosen so the boundary matches the one README
already draws. The task, its one-line instruction and the "why" are above it,
and all three are free and already public inside the .ics feeds. The numbered
steps begin below it and never reach the image.

**Raising a keep_top fraction is a content decision, not a quality tweak.** If a
preview looks thin, change which page it shows.

Covers are different and stay at COVER_WIDTH. A cover is a title page: the
product name, its one-line promise, and nothing anybody paid for.
"""

import os
import sys

from PIL import Image

COVER_WIDTH = 560
PREVIEW_WIDTH = 520
QUALITY = 88

# (source, output)
COVERS = [
    ("product/listing/01-cover.png", "docs/img/cover-kit.jpg"),
    ("product/listing-binder/01-cover.png", "docs/img/cover-binder.jpg"),
    ("product/listing-realtor/01-cover.png", "docs/img/cover-agent.jpg"),
]

# Three per product. Each entry carries the fraction of the page to keep from
# the top, because the crop is the protection and it has to be set per page
# rather than globally.
#
# On the month pages the boundary is not arbitrary: the task, its one-line
# instruction and the "why" sit above it, and README lists all three as free and
# already public inside the .ics feeds. The numbered steps start below it and
# are the thing the kit is sold on. The crop lands on the line that already
# exists rather than inventing a new one.
PREVIEWS = [
    ("product/listing/03-may.png", "docs/img/preview-kit-1.jpg", 0.30),
    ("product/listing/02-watch-list.png", "docs/img/preview-kit-2.jpg", 0.30),
    ("product/listing/08-levels.png", "docs/img/preview-kit-3.jpg", 0.30),

    ("product/listing-binder/04-inventory-kitchen.png", "docs/img/preview-binder-1.jpg", 0.42),
    ("product/listing-binder/07-claim-log.png", "docs/img/preview-binder-2.jpg", 0.42),
    ("product/listing-binder/09-supplies.png", "docs/img/preview-binder-3.jpg", 0.34),

    ("product/listing-realtor/02-footer.png", "docs/img/preview-agent-1.jpg", 1.0),
    ("product/listing-realtor/03-self-serve.png", "docs/img/preview-agent-2.jpg", 1.0),
    ("product/listing-realtor/07-full-kit.png", "docs/img/preview-agent-3.jpg", 0.30),
]

BUILDERS = {
    "product/listing/": "build_listing_images.py",
    "product/listing-binder/": "build_binder_listing.py",
    "product/listing-realtor/": "build_agent_listing.py",
}


def builder_for(src):
    for prefix, script in BUILDERS.items():
        if src.startswith(prefix):
            return script
    return "the matching listing builder"


def emit(src, out, width, keep_top=1.0):
    im = Image.open(src)
    if im.mode != "RGB":
        # The renders carry alpha. Flatten onto white rather than letting JPEG
        # conversion decide, which turns transparent pixels black.
        bg = Image.new("RGB", im.size, "white")
        bg.paste(im, mask=im.split()[-1] if im.mode in ("RGBA", "LA") else None)
        im = bg
    if keep_top < 1.0:
        im = im.crop((0, 0, im.width, int(im.height * keep_top)))
    height = round(im.height * width / im.width)
    im = im.resize((width, height), Image.LANCZOS)
    im.save(out, "JPEG", quality=QUALITY, optimize=True, progressive=True)
    return width, height, os.path.getsize(out)


def main():
    jobs = [(s, o, COVER_WIDTH, 1.0) for s, o in COVERS] + \
           [(s, o, PREVIEW_WIDTH, k) for s, o, k in PREVIEWS]

    missing = [(s, builder_for(s)) for s, _, _, _ in jobs if not os.path.exists(s)]
    if missing:
        for src, maker in missing:
            print("missing: %s\n  run: python %s" % (src, maker), file=sys.stderr)
        return 1

    os.makedirs("docs/img", exist_ok=True)
    total = 0
    for src, out, width, keep in jobs:
        w, h, size = emit(src, out, width, keep)
        total += size
        print("%-32s %4d x %4d  %3d KB" % (out.replace("docs/img/", ""), w, h, size // 1024))
    print("%d files, %d KB total" % (len(jobs), total // 1024))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
