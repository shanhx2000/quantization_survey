#!/usr/bin/env python3
"""
Extract searchable plain text and metadata from a paper PDF into extracted/.
Depends only on the system poppler-utils (pdftotext / pdfinfo) -- no Python packages.

  python3 extract.py [pdf_path ...]    # default: every *.pdf in this directory

PDFs are not committed (see the repo .gitignore). Re-download with:
  curl -sSL -o 2304.07493.pdf https://arxiv.org/pdf/2304.07493

Outputs:
  extracted/<stem>.txt          pdftotext -layout: keeps columns and table alignment, for humans
  extracted/<stem>.raw.txt      pdftotext default stream: for grep / full-text search
  extracted/<stem>.info.txt     pdfinfo metadata (page count, size, producer)
  extracted/<stem>.pages/       one txt per page, to pin down "which page said it"
"""
import glob
import os
import subprocess
import sys

DOWNLOAD = "curl -sSL -o 2304.07493.pdf https://arxiv.org/pdf/2304.07493"


def run(cmd, out_path=None):
    if out_path:
        with open(out_path, "w", encoding="utf-8") as f:
            subprocess.run(cmd, check=True, stdout=f)
    else:
        return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def extract_one(pdf, outdir):
    stem = os.path.splitext(os.path.basename(pdf))[0]
    pagedir = os.path.join(outdir, f"{stem}.pages")
    os.makedirs(pagedir, exist_ok=True)

    run(["pdfinfo", pdf], os.path.join(outdir, f"{stem}.info.txt"))
    run(["pdftotext", "-layout", pdf, os.path.join(outdir, f"{stem}.txt")])
    run(["pdftotext", pdf, os.path.join(outdir, f"{stem}.raw.txt")])

    n_pages = 0
    for line in open(os.path.join(outdir, f"{stem}.info.txt"), encoding="utf-8"):
        if line.startswith("Pages:"):
            n_pages = int(line.split()[1])
    for p in range(1, n_pages + 1):
        run(["pdftotext", "-layout", "-f", str(p), "-l", str(p), pdf,
             os.path.join(pagedir, f"p{p:02d}.txt")])

    print(f"pdf     : {pdf} ({os.path.getsize(pdf)/1e6:.1f} MB, {n_pages} pages)")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    pdfs = [os.path.abspath(a) for a in sys.argv[1:]] or sorted(
        glob.glob(os.path.join(here, "*.pdf")))
    if not pdfs:
        sys.exit(f"no *.pdf in {here}. "
                 f"PDFs are not committed (see .gitignore); re-download: {DOWNLOAD}")

    outdir = os.path.join(here, "extracted")
    for pdf in pdfs:
        extract_one(pdf, outdir)

    print(f"outputs : {outdir}/")
    for f in sorted(os.listdir(outdir)):
        path = os.path.join(outdir, f)
        size = (sum(os.path.getsize(os.path.join(path, x)) for x in os.listdir(path))
                if os.path.isdir(path) else os.path.getsize(path))
        print(f"  {f:<28} {size/1024:8.1f} KB")


if __name__ == "__main__":
    main()
