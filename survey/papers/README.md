# papers/ — one directory per paper

Each directory is named after the paper's **short name with spaces removed**
(`GPTQ`, `SmoothQuant`, `AWQ`, `LLM-FP4`) — not the arXiv id, which goes on the files
inside so that a diff stays readable.

Fixed contents:

| Path | What | In git |
|---|---|---|
| `extract.py` | PDF → text, via poppler-utils. Its docstring carries that paper's re-download command | yes |
| `fetch.py` | web pages instead: snapshots the HTML and converts it to text. Offline by default | yes |
| `<stem>.pdf` | the paper itself | **no** (`.gitignore`) |
| `<stem>.html` | a web resource's raw snapshot — the only way back to the original | **yes** |
| `extracted/` | the extracted text, greppable without downloading the PDF | yes |
| `ANALYSIS.md` | the actual reading notes; header carries venue, DOI, status and how far it was read | yes |
| `paper-note.md` | **the human's own note**, in the team repo's template. Written after the close read, and the only file published to `QuantArchSurvey/venues/ISCA/notes/` — see [`../README.md`](../README.md#publishing-notes-to-the-team-repo) | yes |

Create one with:

```bash
bash Claude/scripts/new_paper.sh <PaperShortName> <arxiv-id-or-pdf-url>
bash Claude/scripts/new_paper.sh <PaperShortName> --web <page-url>
```

Never hand-copy an existing directory — the download command and the URL are baked
into the templates, and a stale copy is how the wrong download command ends up in the
wrong `ANALYSIS.md`.

Every directory here must have a row in [`../README.md`](../README.md);
`bash Claude/scripts/check_survey.sh` reports any that does not.
