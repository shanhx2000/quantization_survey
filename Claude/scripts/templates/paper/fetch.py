#!/usr/bin/env python3
"""
Snapshot a web page and convert it to plain text. Standard library only.

  python3 fetch.py             # re-derive text from the local snapshot; fetch only if there is none
  python3 fetch.py --refetch   # force a network fetch, **overwrites the local snapshot**
  python3 fetch.py --offline   # local snapshot only, never touch the network

Source page: __URL__

Outputs:
  <stem>.html               **the raw HTML snapshot, committed to git** -- pages get
                            redesigned and taken down, and this snapshot is the only
                            way back to the original. Older versions live in git
                            history: confirm the previous one is committed before
                            running --refetch.
  extracted/<stem>.txt      body text with script/style/nav stripped, for grep
  extracted/<stem>.meta.txt snapshot time (mtime of the html), source, byte counts, <title>

Cite web content by the snapshot time in extracted/<stem>.meta.txt.
Never write "the site currently says".
"""
import datetime
import html
import os
import re
import sys
import urllib.request
from html.parser import HTMLParser

URL = "__URL__"
STEM = "__STEM__"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

SKIP = {"script", "style", "noscript", "svg", "head"}
BLOCK = {"p", "div", "section", "article", "br", "li", "tr", "table",
         "h1", "h2", "h3", "h4", "h5", "h6", "ul", "ol", "header", "footer"}


class Text(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out, self.depth, self.title, self.in_title = [], 0, "", False

    def handle_starttag(self, tag, attrs):
        if tag in SKIP:
            self.depth += 1
        if tag == "title":
            self.in_title = True
        if tag in BLOCK:
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in SKIP and self.depth:
            self.depth -= 1
        if tag == "title":
            self.in_title = False
        if tag in BLOCK:
            self.out.append("\n")

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.depth == 0 and data.strip():
            self.out.append(re.sub(r"[ \t\r]+", " ", data))


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    raw = os.path.join(here, f"{STEM}.html")
    outdir = os.path.join(here, "extracted")
    os.makedirs(outdir, exist_ok=True)

    have = os.path.exists(raw)
    if "--offline" in sys.argv and not have:
        sys.exit(f"no local snapshot at {raw}; drop the --offline flag to fetch it.")
    fetch = "--refetch" in sys.argv or (not have and "--offline" not in sys.argv)

    if fetch:
        if have:
            print(f"!! overwriting the existing snapshot {os.path.basename(raw)} -- "
                  f"the old one only survives in git history; confirm it is committed.")
        req = urllib.request.Request(URL, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as r:
            body, how = r.read().decode("utf-8", "replace"), f"HTTP {r.status}"
        open(raw, "w", encoding="utf-8").write(body)
    else:
        body, how = open(raw, encoding="utf-8").read(), "local snapshot (no network)"

    snap = datetime.datetime.fromtimestamp(os.path.getmtime(raw))
    p = Text()
    p.feed(body)
    text = re.sub(r"\n{3,}", "\n\n", "".join(p.out)).strip() + "\n"
    txt = os.path.join(outdir, f"{STEM}.txt")
    open(txt, "w", encoding="utf-8").write(text)
    open(os.path.join(outdir, f"{STEM}.meta.txt"), "w", encoding="utf-8").write(
        f"url:       {URL}\n"
        f"snapshot:  {snap:%Y-%m-%d %H:%M:%S}  (mtime of {STEM}.html)\n"
        f"source:    {how}\n"
        f"html:      {len(body)} bytes ({STEM}.html, committed to git)\n"
        f"text:      {len(text)} bytes\n"
        f"title:     {html.unescape(' '.join(p.title.split()))}\n")

    print(f"url      : {URL}")
    print(f"source   : {how}")
    print(f"snapshot : {raw} ({len(body)/1024:.0f} KB, {snap:%Y-%m-%d})")
    print(f"text     : {txt} ({len(text)/1024:.0f} KB)")


if __name__ == "__main__":
    main()
