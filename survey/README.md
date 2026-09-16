# survey/ — the reading index

The reading list and **current progress** for the quantization survey.
One paper per directory under [`papers/`](papers/), each containing a fixed set:
`extract.py` + `extracted/` (the extracted text, **committed to git**) + `ANALYSIS.md`.

Last updated: **2026-09-14** ｜ Papers filed: **40** — **all 40 `note ready`**

Source list: [`Quantization Architecture Survey - ISCA.csv`](Quantization%20Architecture%20Survey%20-%20ISCA.csv)
(kept verbatim as received; every directory below traces back to one of its rows).
Tag vocabulary and the tagged corpus: [`TAGS.md`](TAGS.md).

> **Every paper with full text now carries a brief** in its `ANALYSIS.md`: motivation,
> overview, pros and cons, and where it applies — plus tags. Those briefs rest on a
> **brief-level read** (abstract, introduction, section map, headline results, conclusion),
> **not** a full read: method and evaluation sections were not read line by line, so every
> entry stays `brief ready` and no number may be cited without going back to the paper.

---

## Scope

**The survey is organised by the taxonomy below** (given by the human, 2026-09-02).
A paper is in scope if it lands in one of these boxes. This replaces the earlier
inferred scope table — and in particular replaces the first draft's "algorithms-led LLM
quantization" framing, which the supplied corpus contradicted.

Field: **computer architecture** — quantization, low-precision numeric formats, and the
compression that rides along with them, **as realised in hardware**. Not LLM-only: the
corpus runs from CNN accelerators (2018) through LLM/KV-cache work (2023–2026), and also
covers SNNs, ray tracing, hyper-dimensional computing, protein structure and recommenders.

> Figures referenced in the source taxonomy (`image.png` markers for the variable
> exponent/mantissa layout, Posit, APoT, ANT/Flint, and the BitFusion diagram) were **not
> supplied** and are not reproduced here.

---

### 1. Data type

**1.1 Traditional data type** — *"it's just quantized"*
Only an **exponent and a mantissa**: Int4, Int8, FP16, FP8, FP4, and anything with a
**variable-length** exponent/mantissa split. The basic quantization method, and what most
papers use. **A paper goes here when it merely *uses* such a type rather than proposing a
new one** — i.e. the novelty is elsewhere (the datapath, the dataflow, the memory system),
not in the number format.

**1.2 New data type** — *the format is the contribution*
Papers whose point **is** the new type: **Posit**, **APoT**, **ANT / Flint**, and anything
else that goes **beyond a normal fixed-length exponent and mantissa**.

**1.3 Lookup table** — *the final form of a data type: **mapping***
Not formulatable, so it needs a **lookup table**: **NormalFloat**, **GOBO**, **K-means**
codebooks, and every other learned or clustered codebook. A value's meaning is an entry,
not an encoding.

> The 1.1 / 1.2 / 1.3 split is a ladder of how a bit pattern becomes a number:
> **a formula with fixed fields** → **a different formula** → **no formula, a table**.

### 2. Quantization architecture

**Mixed precision — and mixed data type — is the most popular design.** The axis that
matters is **granularity**, because granularity is what costs hardware.

**2.1 Tensor-wise** — hardware-friendly
One precision per tensor / layer / operator. **BitFusion** is the archetype; a **GPU is
itself a mixed-precision unit** (Int1, Int4, Int8). **All mixed-precision designs go here**
unless they are finer than a tensor.

**2.2 Fine-grained** — channel, block, element-wise; needs more hardware modification
**BiScale**, **OLAccel**, **GOBO**, **block floating point**.
- **Element-wise** granularity **needs an extra bit** per element (BiScale).
- **Outlier compression** is the sub-case that **only** targets sparse outliers.

---

### Consequence: the corpus does not cover its own taxonomy

The taxonomy names papers that are **not on the ISCA source list and not filed here** —
**Posit**, **APoT**, **ANT / Flint**, **GOBO**, **BiScale**, **NormalFloat**, K-means
codebooks. Several are MICRO / ICLR / NeurIPS work, not ISCA.

So **§1.2 and §1.3 are currently near-empty**, and §1.3 has no filed paper at all: an
ISCA-only sweep cannot populate a taxonomy whose new-data-type and lookup-table branches
live largely at other venues. **Extending beyond ISCA is now a requirement of the
taxonomy, not an open question** — but which venues, and how far back, is still the
human's call.

---

## Where the PDFs come from

**PDFs are taken from arXiv only.** Metadata may additionally come from the ACM DL and
IEEE Xplore records. **No other source** — not author homepages, not university mirrors,
not aggregators — so that every entry has one auditable provenance chain.

Details of what is and is not reachable from this host, and the full list of what was
deleted under this rule, are in
[`Claude/notes/Notes-002`](../Claude/notes/Notes-002-paper-source-access.md).

That rule is why 13 entries started at `pdf missing`: they have **no arXiv version**
(checked by arXiv API title search on 2026-09-02), and both `dl.acm.org` and
`ieeexplore.ieee.org` return **403 to scripts even on landing pages** — verified today, not
assumed. **All 13 have since been downloaded by a human** and filed through
[`uploads/`](uploads/) — the last four on **2026-09-09**. Nothing is queued.

Of the first nine, seven are the **published IEEE version** and carry their own DOI in the PDF
text (grepped, which confirms the DOI independently of any third party). **Two —
[`JPEG-ACT`](papers/JPEG-ACT/) and [`Gist`](papers/Gist/) — are author-hosted copies** with
no IEEE banner and no DOI in the file; their DOI and page range are second-hand, and the
published version was not compared. Each header says which it is.

The **ISCA 2026** entries are the exception in the other direction: their PDFs are the
**published proceedings PDFs**, taken from the `ISCA 2026.zip` package a human put in
[`uploads/`](uploads/). Their filenames are the IEEE article numbers (e.g. `506501b351.pdf`),
and their metadata — title, authors, pages, DOI, abstract — was read from the package's own
`assets/data/data.js`, which is the publisher's record. How to read such a package (and the
script that does it) is in
[`Claude/notes/Notes-001`](../Claude/notes/Notes-001-webpub-proceedings-package.md).

---

## Needs a human download

✅ **Nothing queued — the last four cleared 2026-09-09.**

Every paper on the source list now has its full text. Should another paper need a
hand-download, the flow is in [`uploads/README.md`](uploads/README.md): download over the
Duke subscription, drop the file in [`uploads/`](uploads/), and tell the agent.

| Cleared | Papers |
|---|---|
| 2026-09-02 | `OLAccel` · `Gist` · `IBMCompressionAccelerator` · `JPEG-ACT` · `DRQ` · `CommutativeDataReordering` · `SamsungNPU` · `RaPiD` · `SpZip` |
| **2026-09-09** | [`TPUv4i`](papers/TPUv4i/) (IEEE) · [`AQB8`](papers/AQB8/) · [`Cambricon-SR`](papers/Cambricon-SR/) · [`FATE`](papers/FATE/) (three ACM) |

---

## Status ladder

Use these six, **do not invent new ones**. (Same ladder as
[`AGENT-GUIDE.md`](../Claude/instructions/AGENT-GUIDE.md) §5.)

| Status | Meaning | Test |
|---|---|---|
| `pdf missing` | Metadata only; **no full text** | no `extracted/` in the directory |
| `pdf ready` | Full text extracted and greppable, but **nobody has read it** | `extracted/` has content, `ANALYSIS.md` is metadata only |
| `brief ready` | Above + metadata, verbatim abstract, why it is here, and the questions for a close read | conclusions rest on the abstract alone |
| `analysis ready` | **Full text read**; method, key numbers **with their frame**, limitations | can answer "under what assumptions does this hold?" |
| `note ready` | Above + **`paper-note.md` written** — the human's own note, ready to publish to the team repo | `paper-note.md` exists in the directory and §1 and §4 are filled |
| `thorough ready` | Above + cross-checked against released code / reported data | can point out where paper and implementation disagree |

`note ready` is the rung that matters for the team repo: it is the one that says a paper is
**done on this side**. `python3 Claude/scripts/sync_notes.py` publishes exactly the
`note ready` entries — see [Publishing notes to the team
repo](#publishing-notes-to-the-team-repo).

It is a rung rather than a separate flag because in practice the order is fixed: the note is a
compression of a finished `ANALYSIS.md`, so `note ready` always implies `analysis ready`. The
one case it cannot express is a paper cross-checked against code but not yet written up —
if that happens, `thorough ready` wins and the note is tracked by the file's presence.

**Where the corpus stands (2026-09-14):** all 40 at `note ready`; **34 published**
to the team repo, the other six withdrawn as out of scope (`Cambricon-SR`, `SpZip`,
`IBMCompressionAccelerator`, `CommutativeDataReordering`, `ELSA`, `Phi`) — they stay filed
here but are `EXCLUDED` in `sync_notes.py`. None at `thorough ready` — no entry has been cross-checked against released code.
No `Key numbers` table has been filled for a `brief ready` entry, and no entry has reached
`thorough ready`.

---

## Master table

**Full text** says where the archived PDF came from, and they are not equivalent:
an `arXiv:NNNN.NNNNNvN` entry is **the preprint, not the published ISCA version**;
`IEEE PDF (human)` is the published version, downloaded by a person and carrying its own DOI;
`**author copy** (human)` is neither — no IEEE banner, no DOI in the file.
**No entry has had its preprint/author copy compared against the published version.**

| # | Directory | Venue | Year | Status | Full text | Source-list comment |
|---|---|---|---|---|---|---|
| 1 | [`BitFusion/`](papers/BitFusion/) | ISCA | 2018 | **note ready** | arXiv:1712.01507v2 |  |
| 2 | [`Gist/`](papers/Gist/) | ISCA | 2018 | **brief ready** | **author copy** (human) | Less related |
| 3 | [`OLAccel/`](papers/OLAccel/) | ISCA | 2018 | **note ready** | IEEE PDF (human) |  |
| 4 | [`CommutativeDataReordering/`](papers/CommutativeDataReordering/) | ISCA | 2020 | **brief ready** | IEEE PDF (human) |  |
| 5 | [`DRQ/`](papers/DRQ/) | ISCA | 2020 | **note ready** | IEEE PDF (human) |  |
| 6 | [`IBMCompressionAccelerator/`](papers/IBMCompressionAccelerator/) | ISCA | 2020 | **brief ready** | IEEE PDF (human) | Less related |
| 7 | [`JPEG-ACT/`](papers/JPEG-ACT/) | ISCA | 2020 | **brief ready** | **author copy** (human) | Compress Spatio Info instead of values |
| 8 | [`SmartExchange/`](papers/SmartExchange/) | ISCA | 2020 | **brief ready** | arXiv:2005.03403v2 |  |
| 9 | [`RaPiD/`](papers/RaPiD/) | ISCA | 2021 | **note ready** | IEEE PDF (human) |  |
| 10 | [`RingCNN/`](papers/RingCNN/) | ISCA | 2021 | **brief ready** | arXiv:2104.09056v1 |  |
| 11 | [`SamsungNPU/`](papers/SamsungNPU/) | ISCA | 2021 | **note ready** | IEEE PDF (human) |  |
| 12 | [`SpZip/`](papers/SpZip/) | ISCA | 2021 | **brief ready** | IEEE PDF (human) |  |
| 13 | [`TPUv4i/`](papers/TPUv4i/) | ISCA | 2021 | **brief ready** | IEEE PDF (human) | Provide "Energy per Operation"; FP32 to 8-bit |
| 14 | [`Mokey/`](papers/Mokey/) | ISCA | 2022 | **note ready** | arXiv:2203.12758v1 |  |
| 15 | [`OliVe/`](papers/OliVe/) | ISCA | 2023 | **note ready** | arXiv:2304.07493v1 |  |
| 16 | [`RAELLA/`](papers/RAELLA/) | ISCA | 2023 | **brief ready** | arXiv:2304.07935v1 |  |
| 17 | [`Tender/`](papers/Tender/) | ISCA | 2024 | **note ready** | arXiv:2406.12930v1 |  |
| 18 | [`AQB8/`](papers/AQB8/) | ISCA | 2025 | **brief ready** | ACM PDF (human) | CSV link is a GitHub repo, not a paper |
| 19 | [`Cambricon-SR/`](papers/Cambricon-SR/) | ISCA | 2025 | **brief ready** | ACM PDF (human) | ⚠ full text has **no quantization at all** |
| 20 | [`Ecco/`](papers/Ecco/) | ISCA | 2025 | **note ready** | arXiv:2505.06901v1 |  |
| 21 | [`FATE/`](papers/FATE/) | ISCA | 2025 | **brief ready** | ACM PDF (human) | FPGA; its "LUT" is an FPGA resource, not LUT-GEMM |
| 22 | [`LightNobel/`](papers/LightNobel/) | ISCA | 2025 | **note ready** | arXiv:2505.05893v1 |  |
| 23 | [`LUTTensorCore/`](papers/LUTTensorCore/) | ISCA | 2025 | **note ready** | arXiv:2408.06003v3 |  |
| 24 | [`MicroScopiQ/`](papers/MicroScopiQ/) | ISCA | 2025 | **note ready** | arXiv:2411.05282v4 |  |
| 25 | [`Oaken/`](papers/Oaken/) | ISCA | 2025 | **note ready** | arXiv:2503.18599v2 |  |
| 26 | [`Phi/`](papers/Phi/) | ISCA | 2025 | **note ready** | arXiv:2505.10909v1 |  |
| 26b | [`TransitiveArray/`](papers/TransitiveArray/) | ISCA | 2025 | **note ready** | arXiv:2504.16339v1 | ⭐ from the team repo's ISCA list, not the source CSV |
| 27 | [`AQuant/`](papers/AQuant/) | ISCA | 2026 | **brief ready** | proceedings PDF |  |
| 28 | [`ELSA/`](papers/ELSA/) | ISCA | 2026 | **brief ready** | proceedings PDF |  |
| 29 | [`ENEC/`](papers/ENEC/) | ISCA | 2026 | **brief ready** | proceedings PDF |  |
| 30 | [`EVA/`](papers/EVA/) | ISCA | 2026 | **note ready** | proceedings PDF |  |
| 31 | [`LoKA/`](papers/LoKA/) | ISCA | 2026 | **brief ready** | proceedings PDF |  |
| 32 | [`MXFFP/`](papers/MXFFP/) | ISCA | 2026 | **brief ready** | proceedings PDF |  |
| 33 | [`NDPLowBitFP/`](papers/NDPLowBitFP/) | ISCA | 2026 | **note ready** | proceedings PDF |  |
| 34 | [`OASIS/`](papers/OASIS/) | ISCA | 2026 | **note ready** | proceedings PDF |  |
| 35 | [`Omni-LUT/`](papers/Omni-LUT/) | ISCA | 2026 | **note ready** | proceedings PDF |  |
| 36 | [`P3-LLM/`](papers/P3-LLM/) | ISCA | 2026 | **note ready** | proceedings PDF |  |
| 37 | [`SingularBit/`](papers/SingularBit/) | ISCA | 2026 | **brief ready** | proceedings PDF |  |
| 38 | [`UniCore/`](papers/UniCore/) | ISCA | 2026 | **brief ready** | proceedings PDF |  |
| 39 | [`XtraMAC/`](papers/XtraMAC/) | ISCA | 2026 | **brief ready** | proceedings PDF |  |

**Venue evidence.** For arXiv-sourced entries the venue is taken from the arXiv `comments`
field where it names ISCA (quoted verbatim in each `ANALYSIS.md`). Two entries —
[`BitFusion/`](papers/BitFusion/) and [`Oaken/`](papers/Oaken/) — have **no venue statement on
arXiv**; their ISCA year comes only from the source CSV's grouping and is **not
independently verified**.

---

## Provisional placement in the taxonomy

⚠️ **Assigned from titles and abstracts only** — with the exception of cells corrected
against a full text, which are marked. Every unmarked cell is a guess to be confirmed or
overturned on the close read.

**Corrected 2026-09-09 from the newly filed full texts:** `AQB8` moved 1.1 → 1.2 (it designs
a custom FP14 and an anchor-plus-INT8-offset representation); `FATE` moved 1.2 → 1.1 (it
assigns *existing* types per dimension rather than designing one); both gained a 2.2 cell;
`Cambricon-SR` confirmed to contain no quantization. It is here to make the corpus
navigable in the [scope taxonomy](#scope)'s own terms, **not** as a proposed section
structure, and **not** as evidence for anything.

### 1. Data type

| Box | Filed papers (provisional) |
|---|---|
| **1.1 Traditional** — uses Int/FP, novelty is elsewhere | [`BitFusion`](papers/BitFusion/) · [`OLAccel`](papers/OLAccel/) · [`DRQ`](papers/DRQ/) · [`SamsungNPU`](papers/SamsungNPU/) · [`RaPiD`](papers/RaPiD/) · [`TPUv4i`](papers/TPUv4i/) · [`Tender`](papers/Tender/) · [`XtraMAC`](papers/XtraMAC/) · [`UniCore`](papers/UniCore/) · [`LoKA`](papers/LoKA/) · [`LightNobel`](papers/LightNobel/) · [`FATE`](papers/FATE/) · [`AQuant`](papers/AQuant/) |
| **1.2 New data type** — the format *is* the contribution | [`MXFFP`](papers/MXFFP/) · [`MicroScopiQ`](papers/MicroScopiQ/) · [`AQB8`](papers/AQB8/) · [`P3-LLM`](papers/P3-LLM/) · [`NDPLowBitFP`](papers/NDPLowBitFP/) · [`OliVe`](papers/OliVe/) · [`RingCNN`](papers/RingCNN/) · [`RAELLA`](papers/RAELLA/) |
| **1.3 Lookup table** — mapping, not encoding | [`LUTTensorCore`](papers/LUTTensorCore/) · [`OASIS`](papers/OASIS/) · [`Omni-LUT`](papers/Omni-LUT/) · [`EVA`](papers/EVA/) · [`Mokey`](papers/Mokey/) |
| **unplaced** — no clear data-type claim | [`SmartExchange`](papers/SmartExchange/) · [`SingularBit`](papers/SingularBit/) · [`Phi`](papers/Phi/) · [`ELSA`](papers/ELSA/) · [`Cambricon-SR`](papers/Cambricon-SR/) **(read: no quantization at all)** |

### 2. Quantization architecture

| Box | Filed papers (provisional) |
|---|---|
| **2.1 Tensor-wise** — one precision per tensor/layer/op | [`BitFusion`](papers/BitFusion/) · [`SamsungNPU`](papers/SamsungNPU/) · [`RaPiD`](papers/RaPiD/) · [`UniCore`](papers/UniCore/) · [`XtraMAC`](papers/XtraMAC/) · [`LoKA`](papers/LoKA/) · [`TPUv4i`](papers/TPUv4i/) |
| **2.2 Fine-grained** — channel / block / element-wise | [`DRQ`](papers/DRQ/) (region) · [`MXFFP`](papers/MXFFP/) · [`MicroScopiQ`](papers/MicroScopiQ/) (block/microscaling) · [`Tender`](papers/Tender/) · [`AQuant`](papers/AQuant/) · [`LightNobel`](papers/LightNobel/) · [`SingularBit`](papers/SingularBit/) · [`FATE`](papers/FATE/) (per-dimension) · [`AQB8`](papers/AQB8/) (per-cluster) |
| **2.2b Outlier compression** — sparse outliers only | [`OLAccel`](papers/OLAccel/) · [`OliVe`](papers/OliVe/) · [`MicroScopiQ`](papers/MicroScopiQ/) · [`OASIS`](papers/OASIS/) |

### Papers the taxonomy has no box for

**Seven filed papers are about compression and data movement, not quantization**, and the
taxonomy as given does not reach them:

[`Gist`](papers/Gist/) · [`JPEG-ACT`](papers/JPEG-ACT/) · [`SpZip`](papers/SpZip/) ·
[`CommutativeDataReordering`](papers/CommutativeDataReordering/) ·
[`IBMCompressionAccelerator`](papers/IBMCompressionAccelerator/) · [`ENEC`](papers/ENEC/) ·
[`Ecco`](papers/Ecco/)

The source CSV already marks two of them "Less related", and one "Compress Spatio Info
instead of values". **They need either a box of their own or an explicit exclusion** — an
open question for the human, not something to settle by quietly dropping them.

Two more sit outside on a different axis: [`Phi`](papers/Phi/) and [`ELSA`](papers/ELSA/)
are **spiking-neural-network** architectures, where the low-precision story is spikes rather
than quantized tensors.

---

## Adding a paper

```bash
# from the repo root
bash Claude/scripts/new_paper.sh <PaperShortName> <arxiv-id>
```

Then download and extract as the script prints, fill in every `__PLACEHOLDER__` in
`ANALYSIS.md`, verify the publication info (AGENT-GUIDE §2.1), and add a row to the
[master table](#master-table).

## Re-fetching the sources

```bash
cd survey/papers
# arXiv PDFs: not committed; each ANALYSIS.md opens with its own download command. Re-extract:
for d in */; do (cd "$d" && ls *.pdf >/dev/null 2>&1 && python3 extract.py); done
```

**The ISCA 2026 PDFs cannot be re-downloaded** — they exist only in the proceedings package
in [`uploads/`](uploads/). Do not delete that archive without a replacement.

## Checking the state of this directory

```bash
bash Claude/scripts/check_survey.sh   # declared status vs. what is actually on disk
```

## Publishing notes to the team repo

`papers/<Name>/paper-note.md` is **the human's own writing** and is the only thing that ever
goes into the shared [`QuantArchSurvey`](../QuantArchSurvey/) repo. Publish with:

```bash
python3 Claude/scripts/sync_notes.py --dry-run   # preview
python3 Claude/scripts/sync_notes.py             # write
```

It publishes **only entries at `note ready`** — a drafted `paper-note.md` sitting at
`analysis ready` is held back and reported, because the status is the human's statement that
the note goes out under their name. It copies each note verbatim to
`QuantArchSurvey/venues/ISCA/notes/<short-name>.md`, minus two publish-time removals:

1. **`## 6. Claude notes`** and everything after it — the reading agent's suggestions, which
   say so in their own first line.
2. Inside **`## 5. Comment`**, blocks labelled `**Unadmitted.**` or `**Pair with …**`
   (instruction of 2026-09-03). That material belongs in `ANALYSIS.md`.

The script is idempotent, reports every change, and warns about a file in `notes/` with no
source here. It writes nowhere else in that repo. **Everything else in `QuantArchSurvey/` is
edited by hand and only with the owner's permission** — the script exists precisely so that
publishing cannot quietly become "the agent wrote in the shared repo".

| Published | Awaiting a `paper-note.md` |
|---|---|
| **34** published · 6 excluded as out of scope | 0 |

---

## Known gaps

- **Nothing has been read.** All 35 entries with full text are `brief ready`: abstract only.
  The survey has no claims yet.
- **The taxonomy's §1.2 and §1.3 branches are under-populated, and that is structural.**
  The scheme names **Posit, APoT, ANT/Flint, GOBO, BiScale, NormalFloat** and K-means
  codebooks — **none is on the ISCA source list**, and several are MICRO / ICLR / NeurIPS
  work. An ISCA-only sweep cannot fill this taxonomy. **Extending to other venues is now
  required by the scope**; which ones, and how far back, is the human's call.
- **Seven filed papers have no box** (compression / data movement) and two more are SNN
  work — see [the end of the taxonomy placement section](#papers-the-taxonomy-has-no-box-for).
- ~~**4 papers still have no full text**~~ — **closed 2026-09-09**: `TPUv4i`, `AQB8`,
  `Cambricon-SR` and `FATE` were hand-downloaded and filed. All 40 entries are now
  `brief ready`.
- **Version fidelity is unchecked across the board.** 13 entries are arXiv preprints (several
  say "to appear", so camera-ready-or-earlier), and 2 are author-hosted copies with no DOI in
  the file. **No entry has been compared against its published version.**
- **Two entries have unverified venues** (`BitFusion`, `Oaken`) — see the note under the
  master table.
- **ISCA 2019 is absent by design, not by oversight.** The human checked the ISCA 2019
  program and found nothing fitting the topic (recorded 2026-09-02). The CSV keeps the year
  heading with no rows for exactly this reason — **do not "fix" it by adding papers.**
- **The corpus is ISCA-only, 2018–2026.** MICRO / HPCA / ASPLOS / DAC are not represented.
- ✅ **`TransitiveArray` filed 2026-09-03** — the 40th row of the team repo's ISCA list,
  identified by the human as *"Transitive Array: An Efficient GEMM Accelerator with Result
  Reuse"* (ISCA'25, `10.1145/3695053.3731043`, arXiv:2504.16339). Their list calls it
  **"TransArray"**. ⚠️ **Its seed tags there (`LUT`, `G3`, "codebook anchor") look
  misplaced** — the paper is a multiplication-free **bit-slice + result-reuse** design, not
  a codebook method. See the flag at the top of
  [`papers/TransitiveArray/ANALYSIS.md`](papers/TransitiveArray/ANALYSIS.md); it affects
  `TAXONOMY.md` §G3 thread 3 and survey outline §5.6.
- **`uploads/` is empty and should stay that way.** The ISCA 2026 proceedings package moved
  to [`archieve/`](../archieve/) — it is the only copy of those 13 PDFs, so it is kept rather
  than deleted.
