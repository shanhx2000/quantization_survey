# Notes-001 — reading a WebPub conference proceedings package

**Conclusion first: don't open the PDFs to find out what they are.** A proceedings
package like `ISCA 2026.zip` carries the **publisher's own record** — exact title,
author list, abstract, DOI, page range, and each paper's PDF path — in
`assets/data/data.js`. Decode that and you get authoritative metadata for the whole
volume in one shot. `Claude/scripts/webpub_proceedings.py` does it.

Verified 2026-09-02 against the ISCA 2026 package a human supplied; it now lives in
`archieve/ISCA 2026.zip` (see [`archieve/README.md`](../../archieve/README.md)).

---

## What the package is

The offline web app that IEEE/ACM ship for a conference volume (ISCA, and by the look
of the layout, MICRO / HPCA / ASPLOS too). Structure:

```
ISCA 2026/
├── index.html, main-*.js, styles-*.css   # an Angular app; ignore it
├── assets/data/data.js                   # <-- the record. 817 KB
├── assets/data/search.js                 # a prebuilt search index; not needed
└── pdfs/<volume-id>/<fno>/<fno>.pdf      # 189 files, 320 MB extracted
```

**`fno`** is the IEEE article number (`506501b351`), and it is the *only* thing naming
the PDF on disk. There is no title in the filename and no manifest next to the files —
the join between "paper" and "file" exists **only** inside `data.js`.

## The format, and why it needs 40 lines of code

`data.js` is one line:

```js
window.WEBPUB_CORE_DATA_B64 = '<base64 of a MessagePack blob>';
```

base64 → **MessagePack**, not JSON. There is no `msgpack` module in this host's
`/usr/bin/python3` and this project deliberately has no conda env
(see `Claude/instructions/ENVIRONMENT.md`), so the decoder is written out longhand in
`Claude/scripts/webpub_proceedings.py`. It is ~40 lines and handles the whole spec;
that was cheaper than taking a dependency.

Decoded shape:

```
{ conferences, primaryConferencePid, sections, volumes,
  entries: { ids: [...], entities: { <eid>: {...} } } }
```

One `entities` value per item:

```json
{"eid": "...", "title": "EVA: Accelerating LLM Decoding via ...",
 "authorString": "Bowen Duan, Cong Guo, ...", "abstract": "...",
 "doi": "10.1109/ISCA66397.2026.00102",
 "pages": {"start": 1351, "end": 1367, "count": 17},
 "files": {"pdfPath": "pdfs/5065-.../506501b351/506501b351.pdf"},
 "class": "FM" | ..., "fno": "506501b351"}
```

**Two kinds of junk to filter**, both learned the hard way:
- `class == "FM"` — front matter (title pages, ToC, committee lists).
- **Session/track rows.** They look like papers but have `pages` 0–0 and a `doi` that
  decodes to raw bytes (`b'\x00'`). Filtering on **`files.pdfPath` being present** drops
  both cleanly: the ISCA 2026 volume goes from 226 entities → 210 → **173 real papers**.

## Using the script

```bash
python3 Claude/scripts/webpub_proceedings.py <dir-or-zip> --list          # pages, doi, title
python3 Claude/scripts/webpub_proceedings.py <dir-or-zip> --json out.json # everything
python3 Claude/scripts/webpub_proceedings.py <dir-or-zip> --grab "EVA: Accelerating" --out DIR
```

It accepts the `.zip` directly (extracts to a temp dir, cleans up) or an
already-extracted directory. **Pass the extracted directory when grabbing more than one
paper** — otherwise it re-extracts 320 MB per invocation.

`--grab` reports how it matched: `substring 1.000` is a clean hit;
`substring, N candidates` or a `fuzzy` score means **check it**, and the script says so.
A short query like `--grab "Quantization"` matches five ISCA 2026 papers and silently
takes the shortest title — the warning is the only thing standing between that and a
misfiled paper.

## Matching a reading list against the volume

Normalise both sides (strip accents, lowercase, collapse everything non-alphanumeric to
single spaces) and use `difflib.SequenceMatcher`. All 13 titles from the survey CSV
matched their ISCA 2026 entries at **ratio 1.000** — the CSV's titles were exact, with
only casing differences (`LUT-based` vs `LUT-Based`) and one `ﬁ` ligature
(`Efﬁcient` in `ELSA`) that NFKD normalisation handles.

**Always confirm the grabbed PDF against the title on its own page 1:**

```bash
pdftotext -layout -f 1 -l 1 506501b351.pdf - | head -5
```

The record-to-file join is a path string in `data.js` and nothing else validates it.
All 13 were confirmed this way before filing.

## What this is worth

The metadata out of the package is **better than anything reachable over the network**
for these papers: it is the publisher's record, it includes the abstract, and it needs
no access to `ieeexplore.ieee.org` (which 403s scripts — see
[`Notes-002`](Notes-002-paper-source-access.md)). For a volume a human has already
downloaded, **prefer the package over any lookup.**
