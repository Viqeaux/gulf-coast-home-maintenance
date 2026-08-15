#!/usr/bin/env python3
"""
Web-sized cover images for the shop grid on docs/index.html.

Run:  python build_site_covers.py
Out:  docs/img/cover-kit.jpg
      docs/img/cover-binder.jpg
      docs/img/cover-agent.jpg

Reads the cover render each listing builder already produces and writes a small
JPEG for the site. Run the matching listing builder first if a source is
missing; this says which one.

Why only the covers. `README.md` "What the site may publish" puts the Watch
List, How To Find Out and Your First Month on the paid side, settled in 1.10.0.
The listing builders render those pages too, and none of them may come here. A
cover is a title page: the product name, its one-line promise, and nothing a
buyer is paying for. Adding another image to this list means checking it against
that rule first, not just that it looks good.

The sources live under `product/`, which is gitignored, so these outputs are
committed rather than built on demand. That is the one place in this repo where
a build artifact belongs in git, because the alternative is a site whose images
vanish on a fresh clone.
"""

import os
import sys

from PIL import Image

# (source, output, human name of the builder that makes the source)
COVERS = [
    ("product/listing/01-cover.png",
     "docs/img/cover-kit.jpg", "build_listing_images.py"),
    ("product/listing-binder/01-cover.png",
     "docs/img/cover-binder.jpg", "build_binder_listing.py"),
    ("product/listing-realtor/01-cover.png",
     "docs/img/cover-agent.jpg", "build_agent_listing.py"),
]

# Cards render around 280 CSS px wide, so 560 covers a 2x display and nothing
# more. These are thumbnails: at card size the body text is not meant to be
# read, which is also what keeps them on the right side of the rule above.
WIDTH = 560
QUALITY = 86


def main():
    missing = [(src, maker) for src, _, maker in COVERS if not os.path.exists(src)]
    if missing:
        for src, maker in missing:
            print("missing: %s\n  run: python %s" % (src, maker), file=sys.stderr)
        return 1

    os.makedirs("docs/img", exist_ok=True)
    for src, out, _ in COVERS:
        im = Image.open(src)
        if im.mode != "RGB":
            # The renders carry alpha. Flatten onto white rather than letting
            # JPEG conversion decide, which turns transparent pixels black.
            bg = Image.new("RGB", im.size, "white")
            bg.paste(im, mask=im.split()[-1] if im.mode in ("RGBA", "LA") else None)
            im = bg
        height = round(im.height * WIDTH / im.width)
        im = im.resize((WIDTH, height), Image.LANCZOS)
        im.save(out, "JPEG", quality=QUALITY, optimize=True, progressive=True)
        print("%s  %d x %d  %s KB" % (out, WIDTH, height, f"{os.path.getsize(out) // 1024:,}"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
