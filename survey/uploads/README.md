# uploads/ — drop box for hand-downloaded PDFs

**An inbox for the human.** Papers the scripts cannot fetch (ACM DL / IEEE Xplore and
other subscription publishers) get downloaded by a person and **dropped straight into
this directory** — no need to rename them or work out which paper directory they
belong to. The agent claims them and files them.

## How to use it

1. Check the **"Needs a human download"** section of [`../README.md`](../README.md) —
   it lists what is currently missing, with DOIs and direct links.
2. Open the link over the Duke subscription (campus network / VPN) and download the PDF.
3. Drop the file in here. (Keeping ACM's default `<doi-suffix>.pdf` name is easiest,
   but anything works.)
4. Tell the agent "it's in there". The agent will:
   - claim it to the right `../papers/<PaperShortName>/` using the PDF's embedded
     `Title` metadata;
   - run `python3 extract.py` to produce `extracted/`;
   - upgrade that paper's `ANALYSIS.md` from the `pdf missing` placeholder to a real
     `brief ready` entry;
   - update the status table in [`../README.md`](../README.md) and **leave this
     directory empty again**.

## Conventions

- **This directory should normally be empty** (just this README). Anything in it means
  there is a delivery waiting to be filed.
- PDFs do not go into git (the repo `.gitignore` covers this directory too).
- Nothing lives here long-term — once filed, the original is moved out. Small originals are
  deleted (the extracted text is in git); **bulk packages move to
  [`../../archieve/`](../../archieve/)** rather than being deleted, when they are the only
  copy of a paper's full text.
