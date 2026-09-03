# archieve/ — backup of source packages and processed files

**Cold storage.** Bulk inputs that have already been filed into `survey/papers/`, kept
only so the filing can be redone or audited. Nothing here is read during normal work,
and **nothing here is in git** — the directory is a local backup, not a record.

| File | What it is | What was taken from it |
|---|---|---|
| `ISCA 2026.zip` (289 MB) | The official ISCA 2026 proceedings package (IEEE WebPub offline app: 173 papers, metadata in `assets/data/data.js`) | The 13 ISCA 2026 papers on the survey list — their PDFs, and their titles/authors/abstracts/DOIs/page ranges |

## Why `ISCA 2026.zip` is kept

**It is the only copy of those 13 PDFs.** They are published proceedings papers with no
arXiv version and no public URL, so if this archive goes, the full text is gone and those
13 entries drop back to `pdf missing`. The extracted text under
`survey/papers/*/extracted/` is in git and survives independently, but the PDFs do not.

Read it without unpacking by hand:

```bash
python3 Claude/scripts/webpub_proceedings.py "archieve/ISCA 2026.zip" --list
```

See [`Claude/notes/Notes-001`](../Claude/notes/Notes-001-webpub-proceedings-package.md).

## What belongs here

Source packages and large intermediate files that have been fully processed: proceedings
archives, bulk downloads, one-off conversion output worth keeping. **Not** a drop box for
new material — that is [`survey/uploads/`](../survey/uploads/), which the agent empties
after filing. Something lands here only once it has been filed.
