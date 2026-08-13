#!/usr/bin/env python3
"""
Turn the source photograph in docs/img/ into web-sized JPEGs.

The source PNG is ~3 MB, which is a bad thing to put at the top of a page
someone opens on a phone over cell data. This writes two widths so the browser
can pick one, and keeps the original untouched as the master.

Run:  python optimize_images.py
"""

import os
from PIL import Image

IMG_DIR = os.path.join("docs", "img")
SOURCE = "hero.png"          # master, not served
WIDTHS = [(1600, "hero-1600.jpg"), (900, "hero-900.jpg")]
QUALITY = 78


def main():
    src_path = os.path.join(IMG_DIR, SOURCE)
    src = Image.open(src_path)
    if src.mode != "RGB":
        src = src.convert("RGB")

    print("source: {0}  {1}x{2}  {3:,} bytes".format(
        SOURCE, src.width, src.height, os.path.getsize(src_path)))

    for width, name in WIDTHS:
        height = round(src.height * width / src.width)
        out = src.resize((width, height), Image.LANCZOS)
        out_path = os.path.join(IMG_DIR, name)
        # optimize + progressive: smaller file, and it paints in passes rather
        # than top-to-bottom on a slow connection.
        out.save(out_path, "JPEG", quality=QUALITY, optimize=True, progressive=True)
        print("  {0:<16} {1}x{2}  {3:,} bytes".format(
            name, width, height, os.path.getsize(out_path)))


if __name__ == "__main__":
    main()
