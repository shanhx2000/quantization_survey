# AGENT-GUIDE — rules for working in `quantization_survey/`

For every Claude agent (and human) working in this repo. **Read this file,
`ENVIRONMENT.md` and [`WRITING-STYLE.md`](WRITING-STYLE.md) before doing anything.** The conventions are adapted from
`~/moe_ws/moe_placement/Claude/instructions/AGENT-GUIDE.md`, retuned for a project
whose only deliverable is **a written survey paper**.

**Language: everything in this folder is written in English** — files, commit
messages, `ANALYSIS.md` bodies, notes, reports. Code comments and technical terms are
English too, and **every abbreviation is defined in the file that uses it**. Full rules
in [`WRITING-STYLE.md`](WRITING-STYLE.md). (This used to be a local exception; as of
2026-09-16 the sibling `moe_placement/` and `MobiQuant/` repos follow the same rule.)

---

## 0. What this project is (scope)

Drafting a **survey paper on quantization**. Three stages; we are in stage 1.

| Stage | Content | Status |
|---|---|---|
| 1. Read | Collect and read the literature; one directory per paper under `survey/papers/` | **in progress** |
| 2. Structure | Decide the taxonomy, the section outline, and what claims the survey makes | not started |
| 3. Write | Produce the manuscript | not started |

**Topic boundary: quantization in computer architecture** — low-precision formats and the
compression around them **as realised in accelerator hardware**. The survey is organised by
a **taxonomy the human supplied**: data type (**1.1 traditional** / **1.2 new data type** /
**1.3 lookup table**) × architecture (**2.1 tensor-wise** / **2.2 fine-grained**, with
outlier compression as a sub-case). Not LLM-only. (An earlier draft of this file said
"algorithms-led LLM quantization"; the supplied corpus contradicted it.) The taxonomy in
full, and what it implies about venues, is the "Scope" section of
[`../../survey/README.md`](../../survey/README.md), which is the single place where
the boundary is recorded. When it changes, edit it *there*, not here.

## 0b. `QuantArchSurvey/` is READ-ONLY — hard rule

[`QuantArchSurvey/`](../../QuantArchSurvey/) is a **clone of a shared team repo**
(`git@github.com:shanhx2000/QuantArchSurvey.git`, forked from
`git@github.com:clevercool/QuantArchSurvey.git`). Six other people own venues in it.

**The agent never modifies it.** Not the files, not the git config, not a branch, not a
commit, not a remote. Read it freely; write nothing.

The only content that may ever go into it is **the human's own writing**, and only **with
their explicit permission for that specific change**. If work in this project should end up
there — and finishing the **ISCA** venue eventually should — the agent's job is to prepare
the material *here*, under `survey/`, and hand it to the human. Drafting a diff or a file
"ready to paste" is fine; putting it in that directory is not.

### What the deliverable is

The human owns the **ISCA** venue there: `venues/ISCA/README.md` (**40 rows, all unchecked**)
and one note per paper in `venues/ISCA/notes/`. Per that repo's README, finishing one paper
means: fill a copy of `templates/paper-note.md`, then flip `[ ]` → `[x]` in the venue list,
link the note, and **replace the seed tags with what you actually found**.

**Their schema is not ours.** Four axes, defined in `QuantArchSurvey/TAXONOMY.md`:

| Axis | Values |
|---|---|
| **Level** | `ALGO` / `SYS` / `ARCH`, combinable (`ALGO+ARCH`) |
| **Q-oriented** | `Q-ORIENTED` / `NON-Q-ORIENTED` — the test is *swap the format for plain INT8; what is left?* |
| **Data type** | multi-valued: `INT4` `FP8` `FP4` `BFP` `MX` `LOG` `POW2` `POSIT` `ADAPTIVE` `VQ` `LUT` `SVD` `MIXED` … |
| **Generation** | `G1` pre-2018 / `G2` 2018–2022 / `G3` 2022–now — **judged by paradigm, not by year** |

Plus free-text **Optimization**. Our 14 tags (`survey/TAGS.md`) do **not** map one-to-one
onto this; building the mapping is an open task.

### How work reaches it — the three steps, and who does which

The human set this out on 2026-09-03. **Papers are done one at a time.**

**Revised 2026-09-03.** The original arrangement had the agent stop at `ANALYSIS.md` and the
human author `paper-note.md` from scratch. After two papers the human changed it: **the agent
now drafts the note as well**, and the human rewrites it. Both files live under
`survey/papers/<Name>/`.

| Step | Who | Output |
|---|---|---|
| **1. Reading assistance** | **agent** | `survey/papers/<Name>/ANALYSIS.md` — brief summary, tags, key numbers with frames, fairness assessment, and a `For the note` section |
| **2. Note draft** | **agent** | `survey/papers/<Name>/paper-note.md` — a **draft** in `QuantArchSurvey/templates/paper-note.md` form, written terse (see [`PAPER-READING.md`](PAPER-READING.md) §6a), plus a `## 6. Claude notes` section of short suggestions |
| **3. The note** | **human** | rewrites that draft into their own writing — in practice cutting it by about half |
| **4. Hand-off** | **human** | renames and copies it into `QuantArchSurvey/venues/ISCA/notes/` |

**What has not changed: the agent still writes nothing into `QuantArchSurvey/`.** The draft
note goes in `survey/papers/<Name>/`; carrying it across into `venues/ISCA/notes/`, and
editing `venues/ISCA/README.md`, remain the human's steps. Propose the venue-list row inside
`ANALYSIS.md` as a fenced block for them to paste.

**The draft is a draft.** The survey's prose has to end up genuinely the human's, so an agent
report must say the note is theirs to rewrite, and must never present it as finished.

**`## 6. Claude notes` is ours and stops here.** The agent's suggestions go in that section
rather than inside the human's §1–§5. It is stripped at step 4 and never reaches
`QuantArchSurvey/`.

**There are no experiments in this project.** If we ever need to run or reproduce
a quantization method, that is a new stage and a new top-level directory — ask the
human first (see §1).

## 1. Directory layout

**The top level has four directories** (plus `.gitignore` / `README.md`).
Ask a human before adding a fifth.

```
quantization_survey/
├── Claude/
│   ├── instructions/       # rules for agents. Only edit when a human (or an agent,
│   │                       #   explicitly) decides "this is how we do it from now on"
│   │                       #   PAPER-READING.md is the brief for a single-paper agent
│   ├── prompts/            # copy-paste prompts for launching task-specific agents
│   ├── notes/              # Notes-NNN-<slug>.md — reusable knowledge, appended over time
│   ├── reports/            # Reports-NNN-<slug>.md — the result of one task
│   └── scripts/            # reusable scripts + templates/. One-off commands do NOT go here
├── survey/
│   ├── README.md           # the index: scope taxonomy, status table, gaps
│   ├── papers/             # one directory per paper/resource
│   │   └── <PaperShortName>/
│   │       ├── extract.py  # (PDF) or fetch.py (web page)
│   │       ├── extracted/  # extracted text — **goes into git**
│   │       └── ANALYSIS.md
│   └── uploads/            # drop box for PDFs a human downloaded by hand; kept EMPTY
├── archieve/               # backup of filed bulk sources (proceedings zips). NOT in git
└── QuantArchSurvey/        # clone of the SHARED team repo. **READ-ONLY** -- see 0b. NOT in git
```

`uploads/` is an inbox and `archieve/` is cold storage: material arrives in the first and,
once filed, is either deleted (small — the extracted text is in git) or moved to the second
(bulk, and the only copy of some paper's full text).

Naming rules:
- `Notes-NNN-<kebab-slug>.md` / `Reports-NNN-<kebab-slug>.md`, `NNN` zero-padded to
  three digits, globally monotonic, **numbers are never reused**.
  Run `ls Claude/notes Claude/reports` before creating one.
- `survey/papers/<PaperShortName>/` — the paper's short name with spaces removed
  (`GPTQ`, `SmoothQuant`, `AWQ`, `LLM-FP4`). Not the arXiv id: the id goes on the
  PDF and the extracted files, the directory name has to be readable in a diff.
- Scaffold a new paper directory with
  `bash Claude/scripts/new_paper.sh <PaperShortName> <arxiv-id-or-url>`
  rather than copy-pasting an existing one.

**Notes vs Reports — do not mix them:**

| | What goes in | Test |
|---|---|---|
| `notes/` | Reusable knowledge: a tool's real limits, a trap we hit, a version constraint, a root cause | "Will the next person waste time if this is not written down?" |
| `reports/` | One task: its input, method, result, conclusion, leftovers | "What did this task deliver, and how far was it verified?" |

## 2. How to read a paper (the actual work)

In this order — **get the facts before forming an opinion**:

1. **Publication info first, and it must be exact.** Every `ANALYSIS.md` header
   carries **venue + year**; add **DOI, pages, the date you checked, and the source**
   (Crossref / the official proceedings page / the PDF footer) when you can find them.
   **If there is no formal publication, write `preprint` and add "no publication
   record as of \<date\>"** — never leave it blank, never guess.
   A preprint and the published version **are two different documents**: what we
   archive is usually the arXiv version, and the header must say so.
2. **Get the full text into `extracted/` before writing any judgement.** A conclusion
   drawn from the abstract alone is a `brief ready` conclusion and must be labelled as such.
3. **Quote, don't paraphrase-upward.** When you cite a number or a claim, copy the
   original sentence and mark it **verified**. Anything you inferred is marked
   **inferred / not verified**. Never restate someone's hedged claim as a firm one.
4. **Record the frame of every headline number.** "4-bit, 2.1 PPL degradation" is
   meaningless without: which model, which dataset, which baseline, weight-only or
   W+A, per-channel or per-group, group size, and whether the baseline is FP16 or
   the same method at a different width. **A number without its frame does not go in
   the survey.**
5. **Second-hand facts are marked second-hand.** If paper A's table is your source
   for paper B's number, say so — B's own paper may report it differently, and
   surveys that launder these become wrong.

## 3. Paywalls and downloads (hard rules)

- **The agent does not bypass paywalls.** ACM DL / IEEE Xplore / Elsevier return 403
  to scripts. When that happens, **list the paper in the "Needs a human download"
  table in [`survey/README.md`](../../survey/README.md)** (title / venue / DOI / direct
  link / target directory / why we want it) and set its status to `pdf missing`.
  Verified 2026-09-02: both hosts 403 scripts **even on landing pages**, so neither the
  PDF nor the metadata can be fetched directly. A human downloads with the Duke
  subscription and drops it in [`survey/uploads/`](../../survey/uploads/); the agent then
  files it. Flow:
  [`survey/uploads/README.md`](../../survey/uploads/README.md).
- **PDFs come from arXiv only.** Metadata may additionally be looked up on the ACM DL
  and IEEE Xplore records. **No other source** — not author homepages, not university
  mirrors, not aggregators (ResearchGate / Semantic Scholar / OpenAlex / Crossref) —
  even when one of them serves a legitimate free copy. One auditable provenance chain
  per paper. A paper with no arXiv version stays at `pdf missing` and goes in the
  human-download table; **do not substitute a copy from elsewhere.**
- **PDFs do not go into git** (`survey/papers/**/*.pdf` is in `.gitignore`). The
  extracted text does. Every `ANALYSIS.md` opens with the command that re-downloads
  its PDF, or says why there is none.
- **Web pages keep an HTML snapshot in git.** Pages get redesigned and taken down.
  `fetch.py` is **offline by default** (re-derives text from the committed snapshot);
  updating a snapshot needs an explicit `--refetch`, and **you confirm the old
  snapshot is committed before overwriting it**. Cite web content by the **snapshot
  timestamp** in `extracted/*.meta.txt`, never as "the site currently says".
- Ask a human before downloading anything large (datasets, model weights). This
  project should never need to; if you think it does, say why first.

## 3b. Reading a paper in depth

A single-paper deep read has its own brief: **[`PAPER-READING.md`](PAPER-READING.md)**.
Read it instead of improvising. Ready-made prompts for launching such agents are in
[`../prompts/`](../prompts/).


> **Version control:** see [`G06-VERSION-CONTROL.md`](G06-VERSION-CONTROL.md).
> The one to remember: **never `git add -A` / `-u` / `.`** — name the paths you changed.
> Several agents work in these repos at once and a wildcard add commits their
> unfinished work under your message.

## 4. How to record

- **Conclusions first.** Every file opens with its conclusions; details follow.
- **Separate verified from inferred**, everywhere, with those words.
- Keep commands, paths, tool output, and the papers' own terminology verbatim.
- **Write down what you did not do**, and why. Do not quietly drop part of a task.
- Never upgrade a `brief ready` judgement into a survey claim without reading the
  full text first. §5 defines the ladder.

## 5. Status ladder

Use these six, **do not invent new ones**. The test is "what can someone else do
with this material?"

| Status | Meaning | Test |
|---|---|---|
| `pdf missing` | Metadata only (title/authors/venue/DOI); **no full text** | no `extracted/` in the directory |
| `pdf ready` | Full text downloaded and extracted, greppable, but **nobody has read it** | `extracted/` has content, `ANALYSIS.md` is metadata only |
| `brief ready` | Above + `ANALYSIS.md` has metadata, the verbatim abstract, a first-pass "why it is here", and the questions to resolve on a close read | conclusions rest on the abstract alone |
| `analysis ready` | **Full text read.** `ANALYSIS.md` states the method, the key numbers **with their frame**, and the limitations | can answer "under what assumptions does this hold?" |
| `note ready` | Above + **`paper-note.md` written** — the human's own note in the team repo's template, ready to publish | `paper-note.md` exists in the directory and its §1 and §4 are filled |
| `thorough ready` | Above + cross-checked against the released code / the reported data | can point out where the paper and the implementation disagree |

Every file at `analysis ready` or above carries a **"How far it was read"** line
naming which sections were read closely and which were skimmed — so the next agent
does not redo the work, and so nobody cites a section nobody read.

`note ready` is the rung that says a paper is **finished on this side**:
`python3 Claude/scripts/sync_notes.py` publishes exactly those entries into
`QuantArchSurvey/venues/ISCA/notes/`. Do not set it because a `paper-note.md` file
exists — set it when the note is one the human is willing to publish under their own
name. **Never raise it on their behalf; that is their call, not the agent's.**

## 6. Shared-server red lines (violating these affects other people)

`hl279-cmp-04` is **shared**, and the user `hs359` **has no sudo**. See
`ENVIRONMENT.md`. This project is text-only, so in practice: do not write large files
to `/home`, do not launch massively parallel jobs, do not touch system software.
Read-only inspection (`df`, `ls`, `nvidia-smi`) is unrestricted.

---

## Shared GPU queue (all repos)

**Before running anything on a GPU, read
[`~/moe_ws/Claude/QUEUED_TASKS.md`](../../../Claude/QUEUED_TASKS.md).** All four repos in
this workspace contend for the same 4 GPUs on `hl279-cmp-04`, and more than one agent is
usually active, so GPUs are handed out by lease rather than by looking at `nvidia-smi`
and hoping.

```bash
export MOE_AGENT=<name yourself>
L=~/moe_ws/Claude/scripts/gpu_lease.sh
bash $L status                       # who holds what, plus real VRAM
G=$(bash $L free 12 50) || G=""      # a GPU with >=12 GB free and <=50% util
bash $L claim $G 120 "$MOE_AGENT: <task>"
CUDA_VISIBLE_DEVICES=$G <command> &  # long jobs: background + logfile
bash $L attach $G $!                 # register the real PID
bash $L release $G                   # always, when done
```

**If no GPU is free, do not poll and wait — take a task from section 3 of that file.**
Those are all CPU-only and need no new weights. Add tasks there for your own repo so the
next blocked agent has something to pick up.

⚠️ The lease table is advisory: agents that skip the tool never appear in it, so
**trust the VRAM column first**.
