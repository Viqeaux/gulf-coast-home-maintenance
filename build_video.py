#!/usr/bin/env python3
"""
Build the Etsy listing video from the real kit pages.

Etsy plays listing videos silently and caps them at 15 seconds, so nothing can
be narrated and nothing can be lingered over. Every shot has to make one point
in about two seconds, which is why each carries a short caption rather than
letting the page speak for itself.

Square, because Etsy shows the video inside the image carousel and a square
survives every crop it might get.

Run:  python build_video.py            the kit cut
      python build_video.py --agent    the realtor cut
Out:  product/listing/video.mp4            (gitignored, rebuilt in seconds)
      product/listing-realtor/video.mp4

The two cuts share every frame, crossfade and encoding decision and differ only
in which images they pull and what the captions say. The realtor cut argues a
different case: its buyer is not the person who reads the thing.
"""

import argparse
import os
import shutil
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

LISTING_DIR = os.path.join("product", "listing")
FRAME_DIR = os.path.join(LISTING_DIR, "_frames")
OUT = os.path.join(LISTING_DIR, "video.mp4")

SIZE = 1080
FPS = 30
SHOT_FRAMES = 60          # two seconds a shot
FADE_FRAMES = 9           # the crossfade between them

PAPER = (244, 239, 228)
INK = (23, 33, 31)
MUTED = (91, 106, 104)
ACCENT = (15, 94, 107)
SAND = (168, 118, 31)

FONT_DIR = r"C:\Windows\Fonts"
SERIF = os.path.join(FONT_DIR, "georgiab.ttf")
SANS = os.path.join(FONT_DIR, "segoeuib.ttf")

# Each shot is one page and one point. Order is the argument the listing makes:
# who it is for, what is in it, what makes it worth money, what it costs you.
KIT_SHOTS = [
    ("01-cover.png", "Built for the Gulf Coast", "Texas to Florida"),
    ("03-may.png", "Twelve months, three levels", "Step by step, not a bare list"),
    ("02-watch-list.png", "Everything is on a clock", "Lifespans adjusted for this coast"),
    ("05-how-to-find-out.png", "Don't know how old it is?", "Five minutes to find out"),
    ("06-septic.png", "Septic, pool, generator", "Seven sections for what you have"),
    ("04-the-year.png", "Why May, not June", "A flood policy takes 30 days"),
]

KIT_END_LINES = [
    ("27 pages", SERIF, 96, INK),
    ("Undated, so it never expires", SERIF, 44, MUTED),
    ("INSTANT DOWNLOAD", SANS, 30, ACCENT),
]

# The realtor cut argues something different: the buyer is not the reader. It
# has to establish the branding first, because that is the whole reason an agent
# is paying three times the price, and close on the license.
# Portrait sources only. page_frame fixes the height and derives the width, so a
# 4:3 composition comes back shrunk to fit a square frame, and the caption it
# already carries ends up unreadable above the caption this adds.
AGENT_SHOTS = [
    ("01-cover.png", "Your name on the cover", "Branded in about a minute"),
    ("07-full-kit.png", "And on all 27 pages", "Look along the footer"),
    ("04-watch-list.png", "The page they keep", "Seventeen things already on a clock"),
    ("05-the-year.png", "Built for this coast", "Why May, not June"),
    ("06-first-month.png", "Four pages to hand over", "Not thirty, twenty times"),
    ("08-license.png", "Print for every client", "A client gifting license"),
]

AGENT_END_LINES = [
    ("27 pages, branded", SERIF, 80, INK),
    ("Plus a four page leave-behind", SERIF, 42, MUTED),
    ("INSTANT DOWNLOAD", SANS, 30, ACCENT),
]

SHOTS = KIT_SHOTS
END_LINES = KIT_END_LINES


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def centered(draw, y, text, fnt, fill, tracking=0):
    if tracking:
        width = sum(draw.textlength(ch, font=fnt) + tracking for ch in text) - tracking
        x = (SIZE - width) / 2
        for ch in text:
            draw.text((x, y), ch, font=fnt, fill=fill)
            x += draw.textlength(ch, font=fnt) + tracking
    else:
        width = draw.textlength(text, font=fnt)
        draw.text(((SIZE - width) / 2, y), text, font=fnt, fill=fill)


def page_frame(page_img, caption, sub, progress):
    """One frame. A slow push in keeps a still page from looking like a slide."""
    frame = Image.new("RGB", (SIZE, SIZE), PAPER)

    # Ken Burns: 1.00 to 1.05 across the shot.
    box_h = int(700 * (1.0 + 0.05 * progress))
    box_w = int(box_h * page_img.width / page_img.height)
    scaled = page_img.resize((box_w, box_h), Image.LANCZOS)

    x = (SIZE - box_w) // 2
    y = 46 - int(14 * progress)

    shadow = Image.new("RGB", (box_w + 16, box_h + 16), (214, 206, 190))
    frame.paste(shadow, (x - 8, y - 4))
    frame.paste(scaled, (x, y))

    draw = ImageDraw.Draw(frame)
    draw.rectangle([(0, 812), (SIZE, SIZE)], fill=PAPER)
    draw.line([(SIZE // 2 - 40, 836), (SIZE // 2 + 40, 836)], fill=SAND, width=4)
    centered(draw, 872, caption, font(SERIF, 52), INK)
    centered(draw, 946, sub, font(SANS, 30), MUTED)
    return frame


def end_frame():
    frame = Image.new("RGB", (SIZE, SIZE), PAPER)
    draw = ImageDraw.Draw(frame)
    y = 300
    for text, path, size, color in END_LINES:
        tracking = 6 if path == SANS and text.isupper() else 0
        centered(draw, y, text, font(path, size), color, tracking)
        y += size + 58
        if text == END_LINES[0][0]:
            draw.line([(SIZE // 2 - 60, y - 26), (SIZE // 2 + 60, y - 26)],
                      fill=SAND, width=5)
    centered(draw, 760, "GULF COAST HOME MAINTENANCE",
             font(SANS, 24), MUTED, tracking=5)
    return frame


def blend(a, b, t):
    return Image.blend(a, b, t)


def main(argv=None):
    global LISTING_DIR, FRAME_DIR, OUT, SHOTS, END_LINES

    parser = argparse.ArgumentParser(
        description="Build the Etsy listing video from the real pages.")
    parser.add_argument("--agent", action="store_true",
                        help="the realtor edition cut, from "
                             "product/listing-realtor/")
    args = parser.parse_args(argv)

    source = "build_listing_images.py"
    if args.agent:
        LISTING_DIR = os.path.join("product", "listing-realtor")
        FRAME_DIR = os.path.join(LISTING_DIR, "_frames")
        OUT = os.path.join(LISTING_DIR, "video.mp4")
        SHOTS = AGENT_SHOTS
        END_LINES = AGENT_END_LINES
        source = "build_agent_listing.py"

    missing = [s[0] for s in SHOTS
               if not os.path.exists(os.path.join(LISTING_DIR, s[0]))]
    if missing:
        print("Run {0} first, missing: {1}".format(source, ", ".join(missing)))
        return 1

    if os.path.isdir(FRAME_DIR):
        shutil.rmtree(FRAME_DIR)
    os.makedirs(FRAME_DIR)

    shots = []
    for name, caption, sub in SHOTS:
        page = Image.open(os.path.join(LISTING_DIR, name)).convert("RGB")
        shots.append([page_frame(page, caption, sub, i / (SHOT_FRAMES - 1))
                      for i in range(SHOT_FRAMES)])
    shots.append([end_frame()] * SHOT_FRAMES)

    index = 0
    for shot_no, frames in enumerate(shots):
        tail = FADE_FRAMES if shot_no < len(shots) - 1 else 0
        for i, frame in enumerate(frames[:len(frames) - tail]):
            frame.save(os.path.join(FRAME_DIR, "f{0:04d}.png".format(index)))
            index += 1
        if tail:
            nxt = shots[shot_no + 1]
            for i in range(tail):
                t = (i + 1) / (tail + 1)
                blend(frames[-tail + i], nxt[i], t).save(
                    os.path.join(FRAME_DIR, "f{0:04d}.png".format(index)))
                index += 1

    seconds = index / FPS
    print("{0} frames, {1:.1f} seconds".format(index, seconds))
    if seconds > 15:
        print("  ! longer than Etsy's 15 second cap")

    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-framerate", str(FPS),
        "-i", os.path.join(FRAME_DIR, "f%04d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-crf", "20", "-movflags", "+faststart",
        OUT,
    ], check=True, timeout=300)

    shutil.rmtree(FRAME_DIR)
    print("{0}  {1:,} bytes".format(OUT, os.path.getsize(OUT)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
