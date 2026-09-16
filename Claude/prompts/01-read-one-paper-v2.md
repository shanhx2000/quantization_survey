# Prompt — read one paper (v2, consolidated 2026-09-14)

**Self-contained.** Supersedes `01-read-one-paper.md`, which it folds in along with every
standing correction the human issued through 2026-09-14 (17 papers read). Fill in `<PAPER>`
— a directory name under `survey/papers/` — and send the rest as-is. One agent per paper.
If the human names several papers, do each one fully and report them together.

---

You are preparing **reading assistance** for one paper, for a human writing a survey on
quantization in computer architecture. They will read the paper themselves and rewrite the
note you draft. Your job is to make that reading faster and better-aimed — not to replace it.

**Read these first, in order:**
1. `Claude/instructions/PAPER-READING.md` — your method, especially §6a (the register the
   note must be written in). Follow it; do not improvise.
2. `Claude/instructions/AGENT-GUIDE.md` §0b — the four-step workflow and who owns each step.
3. `QuantArchSurvey/TAXONOMY.md` — the four tag axes you will propose values for.
4. `QuantArchSurvey/templates/paper-note.md` — the shape your note must take.

**Your paper:** `survey/papers/<PAPER>/`

Full text is already extracted and committed under `extracted/`: read `<stem>.txt` (the
`-layout` version), grep `<stem>.raw.txt`, and use `<stem>.pages/pNN.txt` to say which page
something is on. **Download nothing.** `ANALYSIS.md` already holds a brief written from an
abstract-level read — treat it as a **hypothesis to confirm or overturn**, never as ground truth.

---

## Deliverables — two files, both under `survey/papers/<PAPER>/`

### 1. `ANALYSIS.md` — the working record

- **Fill the `Key numbers, with their frame` table** — this is the main thing missing.
- Fill `Method`, `Cost and requirements`, `Limitations and open questions`,
  `Relation to other entries`.
- **Correct the brief** where the close read contradicts it; the close read wins. Say in one
  line what changed rather than silently overwriting.
- Raise status to `analysis ready` and rewrite `How far it was read:` to name which sections
  you read closely versus skimmed. **If you skimmed something load-bearing, say so there and
  itemise what you did not resolve** — see "Read-depth honesty" below.
- Add a `## For the note` section: the §1 one-line summary; proposed values on the four axes
  with one line of evidence each; a proposed venue-list row as a fenced block; the §4
  fairness verdict.

### 2. `paper-note.md` — a terse draft for the human to rewrite

Write it **after** `ANALYSIS.md`, as a compression of it: nothing goes in the note that is not
in the analysis with its evidence. The human's notes run **well under half an agent's default
length**. Budgets:

| Section | Budget |
|---|---|
| Tags table, §1 sentence, §4 table | full care — these land unchanged |
| **§2 Data type** | **one labelled point per line, keyword-dense.** Put a **blank line between points** so they render on separate lines instead of wrapping together. No paragraphs |
| **§3 Optimization** | room to breathe — a short labelled paragraph per mechanism. This is "what was actually built". Do not let it sprawl; the human has asked for it to be simplified twice |
| **§4 Results** | the table only, no prose under it |
| **§5 Comment** | **LEAVE EMPTY** — heading and nothing else. Placement and generation are the human's judgments |

No `**verified**` markers and no page citations in the note — those stay in `ANALYSIS.md`.
A bold label plus one line is a complete entry; prefer a number or a derivation to a sentence
describing it.

**Keep the fairness verdict as the §4 table's last row** (`| **Is the comparison fair?** | … |`)
— it is the most valuable line in the note. **Verdicts, not discussion: ~50–60 words, hard
ceiling ~70.** Name what is iso, what is not, and the number that must not be quoted, and
nothing else. No "because" clauses, no section numbers, no mechanism. Prefer parentheses to
clauses (`**not iso-training** (DRQ QAT vs OLAccel PTQ)`) and semicolons to sentences. If a
verdict needs a "because", it is `ANALYSIS.md` material.

§2 must still carry, however briefly: **format per tensor class, granularity with the group
size, the outlier mechanism (or an explicit "none"), the escape hatch, and PTQ vs QAT.**
Terseness is not licence to drop a required field.

### 3. `## 6. Claude notes` — past the template's §5

Short bullets: what you would argue for that they may not want, cross-paper observations, a
number you think should be excluded, the §5 material you were told not to write. It **must**
open by saying **strip this section before copying into `QuantArchSurvey/venues/ISCA/notes/`.**

---

## On data type — "low precision" is not an answer

Give the **exact format and bitwidth per tensor class** in field notation (`W4A16`, `W8A8`,
`W4A4KV4`); **scale granularity with the group size**; the **outlier mechanism** or an explicit
"none"; the **escape hatch** — almost every paper keeps something high-precision (accumulators,
first/last layer, softmax, a few percent of values), and a "4-bit" method holding 3% at FP16
has a far higher effective bitwidth; and whether it needs **PTQ or QAT**.

---

## Verification discipline — the traps that actually bit

Every one of these is a real error made and caught during the first 17 papers. They are the
difference between a note that can be cited and one that cannot.

1. **Never carry a seed tag you have not found in the paper's own text.** `SmartExchange` was
   tagged `SVD`; the words "SVD" and "singular" appear **zero times** in it. The tag was
   carried from the seed row and then *rationalised* with a footnote. **Grep for the term. If
   it is not there, the tag is wrong** — and never write a footnote explaining why a tag you
   cannot source is still defensible.
2. **Check the direction and order of every equation against the paper's notation.**
   `SmartExchange` factorises `W = Ce · B` with `Ce` the *large sparse* matrix and `B` the
   *small basis* — recorded backwards as `B · Ce` and propagated into three files.
3. **Verify negative claims by grepping, not by not-having-noticed.** "No accuracy content"
   was written for `XtraMAC`, which in fact reports **bit-exact agreement with A100/H100 Tensor
   Cores**. An absence claim needs the same evidence as a presence claim.
4. **Read contribution bullets for which number belongs to which baseline.** `XtraMAC`'s
   1.2× latency / 1.9× energy are **against a GPU**, not against the FPGA baselines named in
   the same sentence.
5. **Before "correcting" the brief, verify against the source.** A correction was issued on
   `OLAccel` saying DRQ does not report a ~5% MobileNet-v2 loss; DRQ reports **5.4% on
   MobileNet-v2 and 5.1% on Inception-v3**. The brief was right and the correction had to be
   withdrawn. The close read wins only when it is actually a read.
6. **Interrogate every headline number before repeating it.** Ask: is it a **maximum across a
   grid** with no average (`SmartExchange`, `Ecco`, `NDPLowBitFP`)? Is it **iso-bitwidth**
   (`EVA`'s 11.17× is 2-bit against a 4-bit FIGLUT; iso-bitwidth it is ~5.6×)? Was the
   baseline **re-simulated or quoted** (`Phi` quotes Stellar)? Do several "independent"
   speedups collapse to **one geometric fact** (`EVA`'s 31–33× across three baselines is
   `v=32`)? Record what you find as a **citation hazard** in `ANALYSIS.md`.
7. **Every number needs its frame** — model, task, baseline, bitwidth, granularity — and its
   **evidence level**. Never pool evidence levels: silicon measurement / post-synthesis / PnR /
   RTL sim / cycle-level simulator / analytical model are not interchangeable. `SamsungNPU`
   measures 13.6 TOPS/W in silicon but its 1.79× is simulation. Prefer end-to-end to peak.
8. **Mark every claim** `**verified**` (with the section or table) or
   `**inferred / not verified**` in `ANALYSIS.md`. Never restate a hedged claim as firm.

### Read-depth honesty

If you did not fully understand the paper, **say so in `## 6. Claude notes` as the first
bullet and in the `How far it was read` line** — separate what you are confident in from an
itemised list of what you skimmed or could not resolve, and mark anything that should be
**verified before citing**. A flagged gap is useful; a confident note over a shallow read is
worse than no note. (`SmartExchange` carries the model of this.)

---

## Tag axes — how they are judged here

- **Level** — `ALGO` / `SYS` / `ARCH`, combinable. **A shipped software stack counts toward
  `SYS`**: a compiler, an ISA, framework plug-ins, a runtime. If the paper builds the thing
  that *drives* the hardware and treats it as a contribution rather than an implementation
  note, the Level is `ARCH+SYS`. An ISA section or a "software stack" figure is the tell.
  Do not reserve `SYS` for papers with no hardware.
- **Q-oriented** — the test is: **swap the format for plain INT8; what is left?** If the
  contribution survives intact it is `non-Q`. Judge the *mechanism*, not the contribution's
  category label — `NDPLowBitFP`'s interleaved layout and free-slot scheduling have nothing to
  optimise under per-tensor INT8, so it is `Q-ORIENTED` despite reading as generic NDP work.
- **Data type** — multi-valued; prefer bitwidths to vague family names. Every value must be
  sourced to a sentence giving element precision.
- **Generation** — `G1` / `G2` / `G3`, judged **by paradigm, never by year**. **Do not
  "correct" a pre-2023 `G3` seed tag**: `OLAccel` (ISCA'18), `GOBO` (MICRO'20) and `Mokey`
  (ISCA'22) are deliberately `G3` as early instances of the outlier and codebook threads.
- **Optimization** — free text.

---

## Place the paper on the cross-paper axes

This is where the survey's value is, and it belongs in `ANALYSIS.md`'s
`Relation to other entries` plus a bullet in §6. Read the neighbouring `ANALYSIS.md` files
before asserting a placement. The axes built so far:

- **Multi-precision datapath** — BitFusion (spatial) → RaPiD (split pipelines) → SamsungNPU
  (temporal) → EVA (temporal) → XtraMAC (spatial in DSP bit-space) → UniCore (adder slices).
  Organising claim: **the deciding variable is what the substrate charges for** — multipliers
  in an ASIC, muxes in a product, DSP bit capacity on an FPGA.
- **Outlier currency — what gets paid to keep an outlier**: extra bits (OLAccel, Oaken), a
  destroyed neighbour (OliVe, MicroScopiQ), a second datapath (OASIS), compressibility itself
  (Ecco), a runtime top-k budget (LightNobel), sign balance in a crossbar column (RAELLA).
- **Granularity** — per-layer (BitFusion, OLAccel) → per-region (DRQ) → per-channel (Tender)
  → per-group (Oaken, MicroScopiQ) → per-head (P3-LLM) → per-token (LightNobel) → **per-rank**
  (SingularBit — a different dimension entirely).
- **Static vs dynamic outlier identification** — OLAccel design-time, DRQ runtime, most
  successors revert to design-time.
- **Substrate** — logic die / DRAM near-memory (P3-LLM, NDPLowBitFP) / analog ReRAM PIM
  (RAELLA). Each makes a different resource scarce (multiplier area / row locality / ADC
  energy), and **that scarcity, not the data distribution, selects the format**.
- **Codebook objective** — Ecco builds one to *store* through, EVA to *compute* through, Phi
  to *skip* through. "Codebook-based" as one category conflates three objectives.
- **Compression vs cheaper arithmetic** — a proposed missing axis. Ecco decompresses to FP16
  between L1 and L2, so it buys bandwidth, not arithmetic.
- **Retraining** — PTQ / QAT / **alternating structure-preserving retraining** (SmartExchange,
  Phi's PAFT), where the structure is not differentiable through.

---

## Non-negotiable

- **Never write anything into `QuantArchSurvey/`** — not files, not git config, not a branch,
  not a commit, not a remote. It is a clone of a shared repo owned by six other people. Read
  it freely; write nothing. Before finishing run `cd QuantArchSurvey && git status --short`.
  It must show nothing of yours. (A modification to `README.md` is the human's own edit —
  leave it alone; do not revert it.)
- **The `## 6. Claude notes` section must never reach `QuantArchSurvey/`.**
- **Do not edit `survey/README.md`, `survey/TAGS.md` or `survey/papers-tags.csv`** — other
  agents may run in parallel and the human maintains those. **Report** what should change.
  Seed-tag corrections for `venues/ISCA/README.md` are reported, never applied.
- **PDFs from arXiv only**, if you need one at all. ACM/IEEE for metadata only.
- Run `bash Claude/scripts/check_survey.sh` before finishing.

---

## Report back

1. The **§1 one-line summary** — what data type, what optimization, what the hardware gets.
2. Your **four proposed tags**, each with one line of justification.
3. **What you left blank and why.** Leave a field empty rather than guessing.
4. **Any disagreement with the seed tags** in `venues/ISCA/README.md`, with evidence.
   Disagreement is useful output — flag it, do not resolve it silently.
5. Say plainly that the note is a **draft for the human to rewrite**.

**Priorities, from their README:** the deliverable for one paper is **the sentence in §1**.
§1, §2 (data type) and the fairness line in §4 are worth more than a fully but shallowly
filled template.
