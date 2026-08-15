#!/usr/bin/env python3
"""Build the realtor edition: the agent's details on the kit, plus a short
leave-behind sized for printing at volume.

Two documents come out of here, each with a fillable twin:

  the kit           all 27 pages, branded. The substantial thing, and the one an
                    agent is most likely to email rather than print.
  the leave-behind  four pages for handing over at closing. An agent doing
                    twenty deals prints eighty pages instead of five hundred and
                    forty, which is the difference between a gift and a chore.

The leave-behind closes by pointing at the free feeds, on purpose. A printed
sheet is filed away by March. A subscribed calendar puts the agent's gift back
on the client's phone every month for years, and that is the part that earns
the referral.

WHAT COSTS WORK PER ORDER, AND WHAT DOES NOT

Run this with no arguments and every detail comes out as a ruled blank that
build_fillable.py turns into a form field. The agent types their name once,
saves, and prints forever. That path is instant download and costs nothing per
sale.

A logo cannot work that way. AcroForm has no image field any ordinary reader
will populate, so a logo has to be baked in here, which means running this for
that one order. That is the whole of the manual work: pass --logo and re-run.

Run:  python build_agent_edition.py
      python build_agent_edition.py --agent "Dana Whitfield" \
             --brokerage "Bayou Oak Realty Group" --phone "(228) 555-0147" \
             --license "MS-B-22841" --logo bayou-oak.png

Out:  product/gulf-coast-agent-edition.pdf            + -fillable.pdf
      product/gulf-coast-agent-leave-behind.pdf       + -fillable.pdf

All four land in product/, which .gitignore keeps out of this public repo.
"""

import argparse
import os
import subprocess
import sys

import build_fillable as bf
import build_printables as bp

KIT = "gulf-coast-agent-edition"
LEAVE_BEHIND = "gulf-coast-agent-leave-behind"

# The reason the leave-behind is worth more to an agent than the paper it is
# printed on. Deliberately the last thing on the cover.
FEEDS_NOTE = (
    '      <p class="cover-feeds"><strong>The full twelve months are free on '
    'your phone.</strong> Three subscribe-able calendars, one per level, that '
    'drop into Google, Apple or Outlook and repeat every year. No purchase and '
    'no sign-up: gulfcoasthomemaintenance.com</p>\n'
)


def leave_behind_html():
    """The four pages an agent actually hands over.

    The Watch List and the year diagram are the two pages people keep, and the
    first-month list is the one a brand new owner uses in week one.
    """
    pages = [
        bp.cover_page(extra=FEEDS_NOTE),
        bp.year_page(),
        bp.first_month_page(),
        bp.watch_list_page(),
    ]
    return bp.DOCUMENT.format(css=bp.CSS + bp.brand_css(), body="\n".join(pages),
                              version=bp.VERSION,
                              disclaimer=bp.DISCLAIMER), len(pages)


def render(html, basename, chrome):
    html_path = os.path.join(bp.OUT_DIR, basename + ".html")
    with open(html_path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(html)

    pdf_path = os.path.abspath(os.path.join(bp.OUT_DIR, basename + ".pdf"))
    subprocess.run([
        chrome, "--headless", "--disable-gpu", "--no-sandbox",
        "--print-to-pdf-no-header",
        "--print-to-pdf=" + pdf_path,
        "file:///" + os.path.abspath(html_path).replace("\\", "/"),
    ], check=True, capture_output=True, timeout=180)
    return pdf_path


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Build the realtor edition of the kit and its leave-behind.")
    parser.add_argument("--agent", default="", help="the agent's name")
    parser.add_argument("--brokerage", default="", help="brokerage name")
    parser.add_argument("--phone", default="")
    parser.add_argument("--license", default="", help="real estate license number")
    parser.add_argument("--logo", default="",
                        help="PNG, JPG or SVG on a transparent or white "
                             "background. Supplying one makes this a per-order "
                             "build.")
    args = parser.parse_args(argv)

    bp.BRAND.update({
        "enabled": True,
        "agent": args.agent,
        "brokerage": args.brokerage,
        "phone": args.phone,
        "license": args.license,
        "logo": args.logo,
    })

    chrome = bp.find_chrome()
    if not chrome:
        print("No Chrome or Edge found.")
        return 1
    os.makedirs(bp.OUT_DIR, exist_ok=True)

    typed = [v for v in (args.agent, args.brokerage, args.phone, args.license) if v]
    if args.logo:
        print("per-order build: logo baked in, {0} detail(s) printed".format(len(typed)))
    elif typed:
        print("partly filled: {0} detail(s) printed, the rest left fillable".format(
            len(typed)))
    else:
        print("self-serve build: every detail is a form field the buyer fills in")

    for basename, builder in ((KIT, bp.build_html),
                              (LEAVE_BEHIND, leave_behind_html)):
        html, count = builder()
        pdf_path = render(html, basename, chrome)
        print("\n{0}.pdf  {1} pages, {2:,} bytes".format(
            basename, count, os.path.getsize(pdf_path)))

        fillable = os.path.join(bp.OUT_DIR, basename + "-fillable.pdf")
        bf.stamp(chrome, html, pdf_path, fillable)
        print("{0}-fillable.pdf  {1:,} bytes".format(
            basename, os.path.getsize(fillable)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
