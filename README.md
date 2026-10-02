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
[LATEX.md](Claude/instructions/LATEX.md) (the Overleaf manuscript), [PAPER-READING.md](Claude/instructions/PAPER-READING.md), the brief for a single-paper
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
python3 Claude/scripts/sync_notes.py --dry-run        # publish notes to QuantArchSurvey (preview)
```

## Notes

| Note | What it saves you |
|---|---|
| [Notes-001](Claude/notes/Notes-001-webpub-proceedings-package.md) | Reading a conference proceedings package: the publisher's own metadata is in `assets/data/data.js`, MessagePack-packed — decode it instead of opening PDFs to identify them |
| [Notes-002](Claude/notes/Notes-002-paper-source-access.md) | What is fetchable from this host: arXiv yes, ACM DL and IEEE Xplore 403 even on landing pages — plus the arXiv-only provenance rule and what it cost |
| [Notes-003](Claude/notes/Notes-003-todo-isca-followups.md) | **TODO list** — open ISCA follow-ups from the 2026-10-01/02 tag work: two Stage cells for the owner, upstream items to raise with other owners, and this repo's unsafe `sync_notes.py` |

**No conda environment is needed.** The extraction scripts use only the Python
standard library plus the system `poppler-utils` (`pdftotext` / `pdfinfo`), so
`/usr/bin/python3` is enough.

## Current status

**40 papers filed**, all with full text, from the source list
[`survey/Quantization Architecture Survey - ISCA.csv`](survey/Quantization%20Architecture%20Survey%20-%20ISCA.csv).
Every one has both an `ANALYSIS.md` and a `paper-note.md`, and **all 40 are `note ready` and
published**. `venues/ISCA` stands at **35 rows** (2026-10-01) — every tag from a full read:
six out-of-scope papers were removed on 2026-09-14 (see below), the two SNN papers of Group B
were restored on 2026-10-01, and upstream moved `RingCNN` to `legacy/` on 2026-09-23 (its Pass 9).
Everything stays filed here, so this repo holds 40 readings and the venue holds 35.
Master table: [`survey/README.md`](survey/README.md).

**Scope** is the taxonomy in that file: data type (**traditional / new data type / lookup
table**) × architecture (**tensor-wise / fine-grained**, outlier compression as a sub-case),
as realised in accelerator hardware. Not LLM-only.

### Scope review — 6 papers removed (2026-09-14)

Every paper has been read, and six of the 40 do not belong in a survey organised by
**data type × granularity**. They were **removed from
[`QuantArchSurvey/venues/ISCA/`](QuantArchSurvey/venues/ISCA/README.md) on 2026-09-14** — rows
and notes both — taking that venue from 40 to 34.

**They are still filed here**, with their readings intact: the work stands, the papers just are
not quantization papers. `Claude/scripts/sync_notes.py` lists them as `EXCLUDED`, so a later
sync cannot silently republish them.

**Group A — no quantization at all (4).** Each was settled by a full-text term sweep,
bibliography included, not by reading the abstract:

| Paper | What it actually is | Evidence |
|---|---|---|
| [`Cambricon-SR`](survey/papers/Cambricon-SR/) (ISCA'25) | Magnitude **pruning** of Instant-NGP's multiresolution hash grid during NeRF training, plus hardware to turn that sparsity into fewer memory requests | `quantiz*` `precision` `bitwidth` `INT8` `FP16` `FP32` `codebook` `centroid` — **zero hits each** |
| [`SpZip`](survey/papers/SpZip/) (ISCA'21) | Lossless delta + bit-plane coding for sparse-traversal data structures, with a dataflow configuration language | `quantiz*` `precision` `bitwidth` `INT8` `FP16`/`FP32` `mantissa`/`exponent` `codebook` `accuracy` — **zero hits each** |
| [`IBMCompressionAccelerator`](survey/papers/IBMCompressionAccelerator/) (ISCA'20) | IBM's shipping NXU: a fixed-function **Deflate (LZ77 + Huffman)** engine in POWER9 / z15 | `neural` `DNN` `learning` `inference` `training` `quantiz*` `precision` `bitwidth` `mantissa` `exponent` `tensor` `GPU` — **zero hits each** |
| [`CommutativeDataReordering`](survey/papers/CommutativeDataReordering/) (ISCA'20) | Bit-level **switching activity on the DRAM bus**: the fetch order of a dot product is algebraically free, so it is permuted as a TSP/CVRP problem | No numeric format is proposed or changed; the values are identical |

The readers' own verdicts: *"Too general compression, and focuses on circuit design. Not for
LLM. Beyond our interested range."* (IBM) and *"General compression for sparse data. Not for
LLM. Likely beyond our interested range."* (SpZip).

**Group B — a different axis (2).** [`ELSA`](survey/papers/ELSA/) (ISCA'26) and
[`Phi`](survey/papers/Phi/) (ISCA'25) are **spiking-neural-network** architectures, ruled out by
the human on 2026-09-14. Their low-precision story is *spikes*, not quantized tensors, so the
data-type axis has nothing to say about them. `ELSA`'s `ANALYSIS.md` carries the ruling in its
status line. Do not re-litigate their tags. **Restored by the human on 2026-10-01** (ISCA
Pass 11): both rows and notes are back in `venues/ISCA/`, tagged `non-Q` with Stage `—`, and
they are no longer `EXCLUDED` in `sync_notes.py`. **ELSA was removed again on 2026-10-02** (ISCA
Pass 13, now in upstream `legacy/` and `EXCLUDED` here once more); **Phi stays**, staged `S3`.

**The two groups are decided by different tests**, which is worth stating rather than hiding:
Group A fails *"does the paper change what a number is?"*; Group B fails *"is this our axis?"*
Both are defensible, but they are not the same question.

### Borderline — kept, and why

Five looked removable and are not. Recorded here so the question is not reopened every pass:

| Paper | Why it stays |
|---|---|
| [`JPEG-ACT`](survey/papers/JPEG-ACT/) (ISCA'20) | It *is* quantization, despite the compression framing: **two quantizers in series**, and the FP32 → per-channel INT8 cast is mandatory on every tensor and worth 4× on its own |
| [`ENEC`](survey/papers/ENEC/) (ISCA'26) | Lossless and bit-identical, but the whole design is **conditioned on the float format** — it compresses the *exponent field specifically*, because its entropy is 2.58 bits against sign+mantissa's 7.97 |
| [`TPUv4i`](survey/papers/TPUv4i/) (ISCA'21) | `NON-Q-ORIENTED`, but the best citation in the corpus for *offer quantization, do not require it*, and the only evidence of how much production inference is actually quantized |
| [`SamsungNPU`](survey/papers/SamsungNPU/) (ISCA'21) | `NON-Q-ORIENTED`, but **measured 5 nm silicon** with a real INT8/INT16 mechanism — industrial calibration the academic entries cannot supply |

[`Gist`](survey/papers/Gist/) (ISCA'18) was the fifth of these and the closest to the line.
**Ruled `Q-ORIENTED` on 2026-09-14**, so it is no longer borderline: it designs two custom
narrow floats — FP10 (1s5e4m) and FP8 (1s4e3m) — for the forward→backward stash, and that is
enough under the `ENEC` precedent, which counts a design **conditioned on the float format**.
The reading had drafted it `non-Q` and recorded a dissent — most of Gist survives swapping the
format for INT8, and the lossless half alone is 1.4× of the 1.8×; **only delayed precision
reduction dies** — and the ruling resolves that dissent in DPR's favour. The dissent is kept in
[`Gist/ANALYSIS.md`](survey/papers/Gist/ANALYSIS.md) because it is why the call was close.

**The operative rule, now settled by two rulings** (`ENEC` and `Gist`): a paper is
`Q-ORIENTED` if its design is **conditioned on the numeric format** — not only if the
arithmetic units see the narrow value.

**ISCA is now 34 rows**, split **32 `Q-ORIENTED` / 2 `NON-Q-ORIENTED`** (the two being
`TPUv4i` and `SamsungNPU`). The taxonomy loses its compression/data-movement cluster entirely,
which is a **finding, not a loss** — it says the source list's "less related" rows were
correctly flagged as such in the original sheet.

**PDF provenance rule:** PDFs from **arXiv only**; ACM DL and IEEE Xplore may be used for
metadata; no other source. Both publishers 403 scripts even on landing pages, so anything
without an arXiv version waits on a human download through
[`survey/uploads/`](survey/uploads/).

**The eventual deliverable** is the **ISCA** part of the shared
[`QuantArchSurvey/`](QuantArchSurvey/) repo — 40 rows in `venues/ISCA/README.md` plus one
note per paper, in *their* template and *their* four-axis taxonomy. **All 40 rows are now
covered** by our 40 filed papers.

Papers are done **one at a time**:

1. **agent** → `survey/papers/<Name>/ANALYSIS.md`: full read, key numbers with frames,
   fairness verdict.
2. **agent** → `survey/papers/<Name>/paper-note.md`: a *draft* note, in their template,
   compressed from the analysis. §5 is left empty — that section is the human's judgment.
3. **human** adopts it: edits, signs the `Reader:` line, and raises the status to
   `note ready`. **Only the human sets `note ready`; the agent never sets it on their behalf.**
4. `python3 Claude/scripts/sync_notes.py` publishes exactly the `note ready` entries into
   `QuantArchSurvey/venues/ISCA/notes/`, verbatim minus the agent's §6.

Two scripts write into `QuantArchSurvey/`, and nothing else does:

- `Claude/scripts/sync_notes.py` -> `venues/ISCA/notes/*.md`
- `Claude/scripts/build_index.py` -> `guidelines/INDEXING.md` (the whole-repo paper
  index, rebuilt from the seven venue READMEs; the `abbr` column is hand-editable
  there and is read back, so a teammate's correction survives regeneration)

Everything else there is edited by hand, with the human's permission for the specific change.

Next: [`Claude/prompts/01-read-one-paper.md`](Claude/prompts/01-read-one-paper.md).
Nothing here may be cited outward yet.
