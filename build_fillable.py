#!/usr/bin/env python3
"""
Make a fillable copy of the kit, so a buyer can type into it or print it blank.

Chrome's print-to-PDF emits no form fields at all, so they cannot come from the
HTML. Instead:

  1. The generator marks the blanks with data-fill="text" or data-fill="check".
  2. This measures where those elements actually landed, by loading the page in
     headless Chrome and letting the browser report each rectangle. Measuring
     beats computing: the CSS decides the layout, and any attempt to work the
     positions out by hand goes stale the moment a margin changes.
  3. reportlab draws an invisible overlay of real AcroForm fields at those
     rectangles, and pypdf merges it onto the finished pages.

The print edition is untouched. This is a second file, so nobody printing at
home gets form widgets they did not ask for.

Run:  python build_fillable.py
Out:  product/gulf-coast-home-maintenance-kit-fillable.pdf
"""

import io
import json
import os
import re
import subprocess
import sys

from pypdf import PdfReader, PdfWriter
from reportlab.lib.colors import Color
from reportlab.pdfgen import canvas as pdfcanvas

from build_printables import BASENAME, CHROME_CANDIDATES, OUT_DIR, build_html

BASE_PDF = os.path.join(OUT_DIR, BASENAME + ".pdf")
OUT_PDF = os.path.join(OUT_DIR, BASENAME + "-fillable.pdf")

# CSS pixels are 96 to the inch, PDF points are 72, so one pixel is 0.75 points.
PX_TO_PT = 0.75
PAGE_W_PT, PAGE_H_PT = 612.0, 792.0      # US Letter

# Injected into a throwaway copy of the document. Chrome runs it on load, and
# --dump-dom then hands us the result.
MEASURE_JS = """
<script>
window.addEventListener('load', function () {
  var out = [];
  document.querySelectorAll('.page').forEach(function (page, pageIndex) {
    var pageBox = page.getBoundingClientRect();
    page.querySelectorAll('[data-fill]').forEach(function (el, i) {
      var r = el.getBoundingClientRect();
      out.push({
        page: pageIndex,
        kind: el.getAttribute('data-fill'),
        name: 'p' + pageIndex + '_f' + i,
        x: r.left - pageBox.left,
        y: r.top - pageBox.top,
        w: r.width,
        h: r.height
      });
    });
  });
  var sink = document.createElement('div');
  sink.id = 'measurements';
  sink.textContent = JSON.stringify(out);
  document.body.appendChild(sink);
});
</script>
"""


def find_chrome():
    for path in CHROME_CANDIDATES:
        if os.path.exists(path):
            return path
    return None


def measure(chrome, html):
    """Ask the browser where every marked blank ended up."""
    tmp = os.path.join(OUT_DIR, "_measure.html")
    with open(tmp, "w", encoding="utf-8") as handle:
        handle.write(html.replace("</body>", MEASURE_JS + "</body>"))

    result = subprocess.run([
        chrome, "--headless", "--disable-gpu", "--no-sandbox",
        "--virtual-time-budget=8000", "--dump-dom",
        "file:///" + os.path.abspath(tmp).replace("\\", "/"),
    ], check=True, capture_output=True, timeout=180)
    os.remove(tmp)

    dom = result.stdout.decode("utf-8", "replace")
    match = re.search(r'<div id="measurements">(.*?)</div>', dom, re.S)
    if not match:
        raise SystemExit("Could not read measurements back from the browser.")
    # The DOM arrives HTML-escaped.
    raw = (match.group(1).replace("&quot;", '"').replace("&amp;", "&")
                         .replace("&lt;", "<").replace("&gt;", ">"))
    return json.loads(raw)


def overlay(fields_by_page, page_count):
    """A PDF of nothing but invisible form fields, one page per kit page."""
    buffer = io.BytesIO()
    pdf = pdfcanvas.Canvas(buffer, pagesize=(PAGE_W_PT, PAGE_H_PT))
    transparent = Color(0, 0, 0, alpha=0)

    for index in range(page_count):
        for f in fields_by_page.get(index, []):
            x = f["x"] * PX_TO_PT
            w = f["w"] * PX_TO_PT
            h = f["h"] * PX_TO_PT
            # PDF measures up from the bottom of the page, CSS down from the top.
            y = PAGE_H_PT - (f["y"] * PX_TO_PT) - h

            if f["kind"] == "check":
                size = min(w, h)
                pdf.acroForm.checkbox(
                    name=f["name"], x=x, y=y, size=size,
                    borderWidth=0, borderColor=transparent,
                    fillColor=transparent, textColor=Color(0.09, 0.13, 0.12),
                    buttonStyle="check", forceBorder=False)
            else:
                # A hair of inset keeps the caret clear of the printed rule.
                pdf.acroForm.textfield(
                    name=f["name"], x=x + 1, y=y + 1.5,
                    width=max(w - 2, 8), height=max(h - 2, 9),
                    fontSize=9, textColor=Color(0.09, 0.13, 0.12),
                    borderWidth=0, borderColor=transparent,
                    fillColor=transparent, forceBorder=False)
        pdf.showPage()

    pdf.save()
    buffer.seek(0)
    return buffer


def stamp(chrome, html, base_pdf, out_pdf):
    """Measure the blanks in `html` and lay real form fields over `base_pdf`.

    Kept separate from main() because the realtor edition needs the same
    treatment on two documents, the branded kit and the short leave-behind.
    """
    fields = measure(chrome, html)

    by_page = {}
    for f in fields:
        by_page.setdefault(f["page"], []).append(f)

    texts = sum(1 for f in fields if f["kind"] == "text")
    checks = len(fields) - texts
    print("measured {0} fields across {1} pages: {2} text, {3} checkbox".format(
        len(fields), len(by_page), texts, checks))

    base = PdfReader(base_pdf)

    # Clone from the overlay, not the other way round. A form lives in the
    # document catalog as well as on the page: merging the overlay into the base
    # copies the widgets but leaves /AcroForm behind, and a PDF whose fields are
    # not listed there is one most readers decline to fill in. Starting from the
    # overlay keeps that structure and its references intact, and the page
    # content merges in underneath because widgets always draw above content.
    writer = PdfWriter(clone_from=overlay(by_page, len(base.pages)))
    for index, page in enumerate(writer.pages):
        page.merge_page(base.pages[index])

    # Without this, some readers show typed text only while a field has focus.
    writer.set_need_appearances_writer(True)
    with open(out_pdf, "wb") as handle:
        writer.write(handle)
    return out_pdf


def main():
    chrome = find_chrome()
    if not chrome:
        print("No Chrome or Edge found.")
        return 1
    if not os.path.exists(BASE_PDF):
        print("Run build_printables.py first, {0} is missing.".format(BASE_PDF))
        return 1

    html, _ = build_html()
    stamp(chrome, html, BASE_PDF, OUT_PDF)

    print("{0}  {1:,} bytes".format(OUT_PDF, os.path.getsize(OUT_PDF)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
