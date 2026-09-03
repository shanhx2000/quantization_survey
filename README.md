# quantization_survey

Drafting a **survey paper on quantization**.

**Read [`Claude/instructions/AGENT-GUIDE.md`](Claude/instructions/AGENT-GUIDE.md) and
[`Claude/instructions/ENVIRONMENT.md`](Claude/instructions/ENVIRONMENT.md) first** —
humans and agents alike. Directory conventions, how to record a paper, the status
ladder, and the shared-server rules all live there.

**Everything in this repo is written in English.** (The sibling `moe_placement/`
project writes prose in Chinese; that convention does not cross this boundary.)

## Stages

1. **Read** (in progress): one directory per paper → [`survey/papers/`](survey/papers/)
2. **Structure**: settle the taxonomy and the section outline → [`survey/README.md`](survey/README.md)
3. **Write**: produce the manuscript → *no directory yet; agree one with the human first*

## Layout

The top level has **three directories**. Discuss before adding a fourth.

| Path | Contents |
|---|---|
| `Claude/` | Rules for agents, notes, reports, reusable scripts and templates |
| `survey/` | The reading work: [`papers/`](survey/papers/) (one directory per paper), [`README.md`](survey/README.md) (the index), [`uploads/`](survey/uploads/) (drop box for hand-downloaded PDFs, kept empty) |
| `archieve/` | [Backup](archieve/README.md) of bulk sources already filed — proceedings packages and the like. Not in git |
| `QuantArchSurvey/` | Clone of the **shared team repo** (`shanhx2000/QuantArchSurvey`). **Read-only — the agent never modifies it**; see [AGENT-GUIDE §0b](Claude/instructions/AGENT-GUIDE.md). Not in git |

Inside `Claude/`: `instructions/` (rules — including
[PAPER-READING.md](Claude/instructions/PAPER-READING.md), the brief for a single-paper
deep-read agent), [`prompts/`](Claude/prompts/) (copy-paste prompts for launching agents),
`notes/` (`Notes-NNN-<slug>.md`, reusable knowledge), `reports/`
(`Reports-NNN-<slug>.md`, one task's conclusions), `scripts/` (reusable scripts +
`templates/`).

## Quick start

```bash
bash Claude/scripts/check_host.sh                     # read-only: tools, disk, network, survey status
bash Claude/scripts/check_survey.sh                   # declared status vs. what is on disk
bash Claude/scripts/new_paper.sh GPTQ 2210.17323      # scaffold one paper directory
python3 Claude/scripts/webpub_proceedings.py <zip> --list   # read a proceedings package
```

## Notes

| Note | What it saves you |
|---|---|
| [Notes-001](Claude/notes/Notes-001-webpub-proceedings-package.md) | Reading a conference proceedings package: the publisher's own metadata is in `assets/data/data.js`, MessagePack-packed — decode it instead of opening PDFs to identify them |
| [Notes-002](Claude/notes/Notes-002-paper-source-access.md) | What is fetchable from this host: arXiv yes, ACM DL and IEEE Xplore 403 even on landing pages — plus the arXiv-only provenance rule and what it cost |

**No conda environment is needed.** The extraction scripts use only the Python
standard library plus the system `poppler-utils` (`pdftotext` / `pdfinfo`), so
`/usr/bin/python3` is enough.

## Current status

**39 papers filed** from the source list
[`survey/Quantization Architecture Survey - ISCA.csv`](survey/Quantization%20Architecture%20Survey%20-%20ISCA.csv):
**35 at `brief ready`** (full text extracted, verbatim abstract, nothing read past it) and
**4 at `pdf missing`**. Master table: [`survey/README.md`](survey/README.md).

**Scope** is the taxonomy in that file: data type (**traditional / new data type / lookup
table**) × architecture (**tensor-wise / fine-grained**, outlier compression as a sub-case),
as realised in accelerator hardware. Not LLM-only.

**PDF provenance rule:** PDFs from **arXiv only**; ACM DL and IEEE Xplore may be used for
metadata; no other source. Both publishers 403 scripts even on landing pages, so anything
without an arXiv version waits on a human download through
[`survey/uploads/`](survey/uploads/).

**The eventual deliverable** is the **ISCA** part of the shared
[`QuantArchSurvey/`](QuantArchSurvey/) repo — 40 rows in `venues/ISCA/README.md` plus one
note per paper, in *their* template and *their* four-axis taxonomy. **All 40 rows are now
covered** by our 40 filed papers.

Papers are done **one at a time**, in three steps:

1. **agent** → `survey/papers/<Name>/ANALYSIS.md`: brief, tags, key numbers with frames,
   fairness verdict. Reading assistance.
2. **human** → `survey/papers/<Name>/paper-note.md`: their own note, in their template.
3. **human** → renames and copies it into `QuantArchSurvey/venues/ISCA/notes/`.

**The agent does step 1 only** — it never writes `paper-note.md` and never touches
`QuantArchSurvey/`.

Next: launch step 1 with [`Claude/prompts/01-read-one-paper.md`](Claude/prompts/01-read-one-paper.md).
Nothing here may be cited outward yet.
