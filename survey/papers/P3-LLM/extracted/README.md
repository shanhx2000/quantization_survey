# extracted/

Output of `extract.py` (or `fetch.py`). **Committed to git**, so the full text is
greppable without downloading the PDF.

| File | Purpose |
|---|---|
| `<stem>.txt` | `pdftotext -layout`: keeps columns and table alignment, for reading |
| `<stem>.raw.txt` | streamed output — **for grep / search** (columns flattened, paragraphs continuous) |
| `<stem>.info.txt` | `pdfinfo` metadata |
| `<stem>.pages/pNN.txt` | one file per page, to pin down "which page said it" |
| `<stem>.meta.txt` | web pages only: snapshot time, source URL, byte counts, title |

**Check quotations against the `-layout` version.** The raw version flattens two-column
layouts and occasionally splices figure captions into the body text.
