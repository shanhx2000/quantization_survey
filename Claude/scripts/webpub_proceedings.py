#!/usr/bin/env python3
"""
Read the metadata out of a WebPub-style conference proceedings package (the offline
web app that IEEE/ACM ship for ISCA, MICRO, HPCA and friends), and optionally pull
named papers' PDFs out of it.

  python3 webpub_proceedings.py <dir-or-zip> --list
  python3 webpub_proceedings.py <dir-or-zip> --json out.json
  python3 webpub_proceedings.py <dir-or-zip> --grab "OASIS: Outlier-Aware" --out ./here

Why this exists: the package's `assets/data/data.js` holds the *publisher's own*
record -- exact title, author list, abstract, DOI, page range, and the path of each
paper's PDF -- but it is MessagePack packed and base64'd, and the PDFs themselves are
filed under opaque IEEE article numbers (`pdfs/<vol>/506501b351/506501b351.pdf`). So
matching a reading list against the package by hand means opening PDFs one at a time.
This reads the record instead.

Stdlib only: the MessagePack decoder below is ~40 lines and beats adding a dependency.

Matching is substring-then-fuzzy on a normalised title, and --grab prints the ratio so
a weak match is visible rather than silent. Always confirm a grabbed PDF against the
title printed on its own page 1 (`pdftotext -f 1 -l 1 <pdf> -`) before filing it: the
record and the file are joined by a path in the package, and nothing else checks it.
"""
import argparse, base64, difflib, json, os, re, shutil, struct, sys, tempfile, unicodedata, zipfile


# --- minimal MessagePack decoder -------------------------------------------------
class _R:
    def __init__(self, b): self.b, self.i = b, 0
    def u(self, n):
        v = self.b[self.i:self.i + n]; self.i += n; return v
    def byte(self):
        v = self.b[self.i]; self.i += 1; return v


def _dec(r):
    c = r.byte()
    if c <= 0x7f: return c
    if c >= 0xe0: return c - 256
    if 0x80 <= c <= 0x8f: return {_dec(r): _dec(r) for _ in range(c & 0x0f)}
    if 0x90 <= c <= 0x9f: return [_dec(r) for _ in range(c & 0x0f)]
    if 0xa0 <= c <= 0xbf: return r.u(c & 0x1f).decode('utf-8', 'replace')
    if c == 0xc0: return None
    if c == 0xc2: return False
    if c == 0xc3: return True
    if c == 0xc4: return r.u(r.byte())
    if c == 0xc5: return r.u(struct.unpack('>H', r.u(2))[0])
    if c == 0xc6: return r.u(struct.unpack('>I', r.u(4))[0])
    if c == 0xca: return struct.unpack('>f', r.u(4))[0]
    if c == 0xcb: return struct.unpack('>d', r.u(8))[0]
    if c == 0xcc: return r.byte()
    if c == 0xcd: return struct.unpack('>H', r.u(2))[0]
    if c == 0xce: return struct.unpack('>I', r.u(4))[0]
    if c == 0xcf: return struct.unpack('>Q', r.u(8))[0]
    if c == 0xd0: return struct.unpack('>b', r.u(1))[0]
    if c == 0xd1: return struct.unpack('>h', r.u(2))[0]
    if c == 0xd2: return struct.unpack('>i', r.u(4))[0]
    if c == 0xd3: return struct.unpack('>q', r.u(8))[0]
    if c == 0xd9: return r.u(r.byte()).decode('utf-8', 'replace')
    if c == 0xda: return r.u(struct.unpack('>H', r.u(2))[0]).decode('utf-8', 'replace')
    if c == 0xdb: return r.u(struct.unpack('>I', r.u(4))[0]).decode('utf-8', 'replace')
    if c == 0xdc: return [_dec(r) for _ in range(struct.unpack('>H', r.u(2))[0])]
    if c == 0xdd: return [_dec(r) for _ in range(struct.unpack('>I', r.u(4))[0])]
    if c == 0xde: return {_dec(r): _dec(r) for _ in range(struct.unpack('>H', r.u(2))[0])}
    if c == 0xdf: return {_dec(r): _dec(r) for _ in range(struct.unpack('>I', r.u(4))[0])}
    if c in (0xd4, 0xd5, 0xd6, 0xd7, 0xd8):
        n = {0xd4: 1, 0xd5: 2, 0xd6: 4, 0xd7: 8, 0xd8: 16}[c]; r.byte(); return r.u(n)
    if c == 0xc7: n = r.byte(); r.byte(); return r.u(n)
    if c == 0xc8: n = struct.unpack('>H', r.u(2))[0]; r.byte(); return r.u(n)
    if c == 0xc9: n = struct.unpack('>I', r.u(4))[0]; r.byte(); return r.u(n)
    raise ValueError(f"unknown msgpack byte 0x{c:02x} at offset {r.i - 1}")


# --- package handling ------------------------------------------------------------
def norm(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', ' ', s.lower()).strip()


def find_root(path):
    """Return the directory holding assets/data/data.js (handles a single wrapper dir)."""
    for base, _dirs, files in os.walk(path):
        if os.path.basename(base) == 'data' and 'data.js' in files:
            return os.path.dirname(os.path.dirname(base))
    sys.exit(f"no assets/data/data.js under {path} -- is this a WebPub proceedings package?")


def load(root):
    src = open(os.path.join(root, 'assets', 'data', 'data.js'), encoding='utf-8').read()
    m = re.search(r"B64\s*=\s*'([^']+)'", src)
    if not m:
        sys.exit("assets/data/data.js has no base64 blob (format changed?)")
    d = _dec(_R(base64.b64decode(m.group(1))))
    # Drop front matter and the session/track rows: only entries with their own PDF are papers.
    return [e for e in d['entries']['entities'].values()
            if e.get('class') != 'FM' and (e.get('files') or {}).get('pdfPath')]


def brief(e):
    p = e.get('pages') or {}
    return {"title": e.get('title'), "authors": e.get('authorString'),
            "abstract": e.get('abstract'), "doi": e.get('doi'),
            "pages": f"{p.get('start')}-{p.get('end')}" if p else None,
            "fno": e.get('fno'), "pdf": (e.get('files') or {}).get('pdfPath')}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('package', help='the proceedings .zip, or an already-extracted directory')
    ap.add_argument('--list', action='store_true', help='print every paper: pages, doi, title')
    ap.add_argument('--json', metavar='FILE', help='dump all entries as JSON')
    ap.add_argument('--grab', action='append', default=[], metavar='TITLE',
                    help='copy the best-matching paper PDF out (repeatable)')
    ap.add_argument('--out', default='.', help='destination directory for --grab')
    a = ap.parse_args()

    tmp = None
    pkg = a.package
    if zipfile.is_zipfile(pkg):
        tmp = tempfile.mkdtemp(prefix='webpub-')
        with zipfile.ZipFile(pkg) as z:
            z.extractall(tmp)
        pkg = tmp
    try:
        root = find_root(pkg)
        entries = load(root)
        print(f"{len(entries)} papers in {os.path.basename(a.package)}", file=sys.stderr)

        if a.list:
            for e in sorted(entries, key=lambda x: (x.get('pages') or {}).get('start') or 0):
                p = e.get('pages') or {}
                print(f"{str(p.get('start')):>5}-{str(p.get('end')):<5} {e.get('doi','')}  {e.get('title','')}")
        if a.json:
            json.dump([brief(e) for e in entries], open(a.json, 'w'), indent=1)
            print(f"wrote {a.json}", file=sys.stderr)

        pool = [(norm(e.get('title')), e) for e in entries]
        for want in a.grab:
            nw = norm(want)
            subs = [p for p in pool if nw in p[0]]
            # A substring hit is strong even when the query is much shorter than the title,
            # so score it on the matching prefix rather than the whole title -- otherwise a
            # correct short query looks like a bad fuzzy match.
            if subs:
                n, e = min(subs, key=lambda p: len(p[0]))
                ratio, how = 1.0, f"substring{'' if len(subs) == 1 else f', {len(subs)} candidates'}"
            else:
                n, e = max(pool, key=lambda p: difflib.SequenceMatcher(None, nw, p[0]).ratio())
                ratio, how = difflib.SequenceMatcher(None, nw, n).ratio(), 'fuzzy'
            src = os.path.join(root, e['files']['pdfPath'])
            dst = os.path.join(a.out, os.path.basename(src))
            os.makedirs(a.out, exist_ok=True)
            shutil.copy(src, dst)
            flag = '' if (ratio > 0.9 and len(subs) < 2) else '   <-- CHECK THIS ONE'
            print(f"{how} {ratio:.3f}  {e['title']}\n  -> {dst}{flag}")
    finally:
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == '__main__':
    main()
