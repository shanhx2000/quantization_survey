# PAPER-READING — brief for a single-paper deep-read agent

You have been launched to read **one paper** (occasionally a small thread of related ones)
and produce a note that the human can hand to a shared team repo. Read this file and
[`AGENT-GUIDE.md`](AGENT-GUIDE.md) §0b before touching anything.

---

## 0. Three hard rules

1. **Never write into `QuantArchSurvey/`.** It is a clone of a shared repo owned by six
   other people. Read it; write nothing — not files, not git config, not commits.
   Your output goes in **our** tree. Full rule: [`AGENT-GUIDE.md`](AGENT-GUIDE.md) §0b.
2. **Never download a PDF from anywhere but arXiv.** You almost certainly do not need to:
   the full text is already extracted and committed under
   `survey/papers/<Name>/extracted/`. See [`Notes-002`](../notes/Notes-002-paper-source-access.md).
3. **Mark every claim.** `**verified**` with the section or table it came from, or
   `**inferred / not verified**`. Never restate a hedged claim as a firm one, and never
   promote a number without its frame (§3).

## 1. What you are producing — two files

**Changed 2026-09-03 by the human.** Agents previously produced `ANALYSIS.md` only and were
forbidden from drafting the note. That rule is lifted: **draft the note too.** The human then
edits it into their own writing and hands it on — in practice they cut it by roughly half.

1. **`survey/papers/<Name>/ANALYSIS.md`** — the working record. Update the file that is
   already there. Full evidence apparatus lives here: `**verified**` markers, page numbers,
   number frames, disagreements.
2. **`survey/papers/<Name>/paper-note.md`** — a **draft** in
   `QuantArchSurvey/templates/paper-note.md` form, for the human to rewrite. See §6a for the
   register it must be written in.

**Still forbidden: writing anything into `QuantArchSurvey/`.** The draft note goes in
`survey/papers/<Name>/`, never in `QuantArchSurvey/venues/ISCA/notes/`. Copying it across is
the human's step and needs their explicit permission for that specific file (§0 rule 1,
[`AGENT-GUIDE.md`](AGENT-GUIDE.md) §0b).

Inside `ANALYSIS.md`, keep the **"For the note"** section carrying the material their template
asks for that our format does not already hold. It is the bridge between the two files — write
it first, then compress it into `paper-note.md`:

- **proposed values on their four axes**, each with one line of evidence
- a **proposed venue-list row** for `venues/ISCA/README.md`, as a fenced block they can
  copy — never edit that file yourself
- the **§1 one-line summary** in their sense: what data type, what optimization, what the
  hardware gets out of it
- their **§4 fairness verdict**: is the headline comparison iso-area / iso-accuracy /
  iso-node / iso-era, or none of those

## 2. The order to work in

**Their repo's README states the priority, and it is not "fill every field":**

> The deliverable for one paper is **the sentence in §1** — what data type, what
> optimization, and what the hardware gets out of it. Everything else exists to make that
> sentence defensible. §1, §2 (data type) and the "is the comparison fair?" line in §4 are
> worth more than a fully but shallowly filled template.

So:

1. **Read the paper.** `extracted/<stem>.txt` is the `-layout` version for reading;
   `<stem>.raw.txt` is for grep; `<stem>.pages/pNN.txt` pins down which page said it.
   Quote from the `-layout` version — the raw one flattens columns and splices captions.
2. **Write §1 first, in one sentence.** If you cannot, you have not finished reading.
3. **Then §2 (data type)** — the densest and most important section. Then §4's fairness
   line. Then §3, then §5. Then the tags. Then the venue row.
4. **Leave a field empty rather than guessing**, and say in §5 what you left and why.
5. **Write `ANALYSIS.md` first, `paper-note.md` second.** The note is a compression of the
   analysis, not a parallel effort. If a claim is not in `ANALYSIS.md` with its evidence, it
   does not belong in the note.

## 3. §2 — data type: what "be specific" means here

"Low precision" is not an answer. Every one of these, or an explicit statement that the
paper does not say:

- **Exact format and bitwidth, per tensor class** — weights, activations, KV cache
  separately. Use the field's notation: `W4A16`, `W8A8`, `W4A4KV4`.
- **Scale granularity** — per-tensor / per-channel / per-token / per-group, **with the
  group size**. This is the single most under-reported number in the literature.
- **Outlier mechanism**, or an explicit "does not handle outliers".
- **The escape hatch.** Almost every paper keeps *something* in high precision —
  accumulators, the first and last layer, softmax, a fraction of values. **Find it.** A
  paper claiming 4 bits while holding 3% of values at FP16 has an effective bitwidth well
  above 4, and that is the comparison that matters.
- **Accumulator bitwidth, always, as its own line.** It has been load-bearing in most papers
  read so far: Tender's 32-bit `Acc` is left-shifted once per channel band, so it bounds the
  band count; TransitiveArray splits a 12-bit PPE / 24-bit APE for 4-bit activations; LUT
  Tensor Core's headline density is measured **"No Psum"**, i.e. with accumulator cost
  excluded. Record the width, and whether the reported area/energy includes it.
- **Retraining requirement** — PTQ off an off-the-shelf checkpoint, or QAT? This is an
  *architectural* constraint, not an accuracy footnote: hardware that cannot consume a
  stock checkpoint cannot be deployed.

## 4. §4 — results, and the fairness line

Fill the table, then answer **"is the comparison fair?"** in prose. Check, at minimum:

- **Iso-what?** Same area? Same node? Same accuracy target? Accelerator papers most often
  overclaim by comparing a new design against a baseline at a different point.
- **Baseline era and node.** A 2026 design beating a 2016 accelerator scaled analytically
  to 7 nm is not a measurement.
- **Evidence level** — silicon measurement / post-synthesis / RTL sim / simulator /
  analytical model. Record which. A simulator number and a fabricated-chip number are not
  the same kind of fact and must not be pooled.
- **Peak versus end-to-end.** [`RaPiD`](../../survey/papers/RaPiD/ANALYSIS.md) is the
  cautionary case: peak TOPS/W ratios across precisions are far larger than its 1.2–1.8×
  end-to-end gains, because some operations stay FP16. Always prefer the end-to-end number.

## 5. The four tag axes

Definitions are in `QuantArchSurvey/TAXONOMY.md` — **read it once before your first paper.**
The traps:

- **`Q-oriented` decides whether the paper is worth reading closely, and it is a test, not
  a vibe**: *swap its numeric format for plain INT8 — what is left?* Nothing →
  `Q-ORIENTED`. The contribution survives untouched (sparsity, dataflow, scheduling,
  pruning) → `NON-Q-ORIENTED`. `NON-Q-ORIENTED` is not an insult; it means the paper
  becomes a background citation instead of a body paragraph.
- **Generation is judged by paradigm, not by year.** A 2025 paper doing plain per-tensor
  INT8 is `G1`, and saying so is a finding. The converse matters more: their taxonomy
  **deliberately** tags several pre-2023 papers `G3` — OLAccel (ISCA'18), GOBO (MICRO'20),
  Mokey (ISCA'22) — as early instances of the outlier and codebook threads. **Do not
  "correct" those.** If a paper genuinely bridges, write `G2→G3` and justify it in §5.
- **A shipped software stack counts toward `SYS`** (their ruling, 2026-09-09, on RaPiD).
  A compiler, an ISA, framework plug-ins, a runtime — if the paper builds the thing that
  *drives* the hardware and treats it as a contribution rather than an implementation note,
  the Level is `ARCH+SYS`, not `ARCH`. Do not reserve `SYS` for papers with no hardware.
  Check for this explicitly: an ISA section or a "software stack" figure is the tell.
- **Data type is multi-valued and wants the bitwidth**: `INT4` beats `INT`. Tag `MIXED`
  *alongside* the underlying formats. If the paper says microscaling, tag `MX`, not `BFP`.
- The venue list's existing tags are **seeds**, not answers. Their workflow says to
  **replace** them with what you found. When you disagree with a seed, say so in §5 with
  the evidence — that disagreement is useful output, not a problem.

## 6. Updating `ANALYSIS.md`

The file already holds a **brief** (motivation / overview / pros and cons / where it
applies) written from an abstract-level read. On a close read:

- **Fill the `Key numbers, with their frame` table.** This is the main thing missing.
- **Correct the brief where the close read contradicts it** — the close read wins. Say what
  changed, in one line, rather than silently overwriting.
- **Raise the status** to `analysis ready` and rewrite the `How far it was read:` line to
  name the sections you actually read closely versus skimmed. Do not claim
  `thorough ready` unless you cross-checked against released code or data.
- Add cross-links to related entries under `Relation to other entries`.
- Add the **"For the note"** section described in §1.

## 6a. `paper-note.md` — the register to write it in

The human's own notes are **far terser than an agent's default**. Measured on
`TransitiveArray` (2026-09-03): the agent draft ran 128 lines for §2–§5; the human's rewrite
was 56. Write the draft closer to their length, not to yours.

**Keep at full care** — these landed unchanged and are what the note is for:

- the **tags table**
- the **§1 one-line summary**
- the **§4 results table**

**Compress hard** — §2 through §5. **Budgets, set by the human 2026-09-09 after two rounds of
"shorter":**

| Section | Budget |
|---|---|
| §2 Data type | **one point per line, keyword-dense.** No line wraps into a paragraph; if a point needs two sentences it is two points or it belongs in `ANALYSIS.md` |
| §3 Optimization | **room to breathe** — a short labelled paragraph per mechanism, plus what the hardware costs. This is "what was actually built"; detail earns its place here and nowhere else in the note |
| §4 Results | **the table only** — no prose under it |
| §5 Comment | **LEAVE EMPTY.** Heading and nothing else |

Outside §3, one line means one line: a bold label and a sentence or two, wrapped. If it does
not fit, the material belongs in `ANALYSIS.md`, not in a longer note.

**§5 is the human's, and you leave it blank** (their instruction, 2026-09-09). It carries survey
placement, the claim the paper is the best citation for, and the generation justification —
the judgments that are the point of them writing the note themselves. Write the heading, leave
it empty, and put what you *would* have said in `## 6. Claude notes` under a "§5 material, if
you want it" bullet, where they can take it or ignore it.

**The §4 fairness verdict is not dropped — it becomes the table's last row.** Their README calls
that line worth more than a fully filled template, so keep it as a
`| **Is the comparison fair?** | … |` row: iso-what, the one number not to quote, and the
disclosed operating range. That satisfies "just a table" without losing the most valuable
sentence in the note.

**Keep that row short — verdicts, not discussion** (their instruction, 2026-09-09, restated
2026-09-09 after DRQ). **Target ~50-60 words; hard ceiling ~70.** Name what is iso, what is not,
and the number that must not be quoted — nothing else. Do not explain *why* each holds, do not
name the section a concession appears in, do not give the mechanism behind an elision: all of that
lives in `ANALYSIS.md`'s fairness section, and the note is a pointer to it. Prefer parentheses to
clauses (`**not iso-training** (DRQ QAT vs OLAccel PTQ)`) and a semicolon list to sentences. If a
verdict needs a "because", it is `ANALYSIS.md` material.

- **Fragments and arrows are the register**, not paragraphs. *"GEMM -> Sparse LUT
  construction + Lookups."* No topic sentences. Bold lead-ins only for the template's own
  field names (Formats, Granularity, Escape hatch, Retraining).
- **A bold label plus one line is a complete entry.** *"**Outliers.** Isolated but not
  high-precision — 5-bit, one above inliers. Cost is metadata, not precision."* That is the
  target density: the claim and its consequence, nothing else.
- **Numbers instead of description.** *"4 + 10%×8 = 4.8"* beats a sentence explaining the
  encoding. Put the derivation in `ANALYSIS.md`; put the result in the note.
- **Cut the evidence apparatus entirely.** No `**verified**` markers, no page or section
  citations except where a fact is meaningless without one, no commentary about how the paper
  frames itself. All of that stays in `ANALYSIS.md`.
- **State the verdict, drop the case.** A multi-paragraph fairness analysis becomes *"Fair.
  Iso-node and iso-area yes; iso-algorithm no."* Keep the exceptions that change a decision;
  cut the reasoning that led to them.
- **Generalize to what the design constrains**, not what the paper happened to report. "Can
  be extended to arbitrary activation precisions if the LUT/adder bit-width is modified"
  beats reciting the two widths the paper synthesized.

§2 must still carry, however briefly, the five things §3 above demands — format per tensor
class, granularity **with group size**, outlier mechanism, the **escape hatch**, and PTQ vs
QAT. Terseness is not licence to drop a required field.

**Add a `## 6. Claude notes` section** — the template stops at §5; this one is ours. Put your
suggestions there rather than pushing them into the human's §1–§5: things you would argue for
but they may not want, cross-paper observations, a number you think should be excluded, an
empty section you would fill. **Keep it short** — bullets, a few lines each, not a second
essay. Open it with:

```
*Suggestions from the reading agent. **Strip this section before copying into
`QuantArchSurvey/venues/ISCA/notes/`.***
```

**§6 never goes into `QuantArchSurvey/`.** It is scaffolding for the human's rewrite, not part
of the note they hand to the team repo. Say so in the section itself, every time.

## 7. Before you finish

```bash
bash Claude/scripts/check_survey.sh          # declared status vs. what is on disk
cd QuantArchSurvey && git status --short     # MUST be empty
```

Confirm `paper-note.md` exists in `survey/papers/<Name>/` and **nowhere inside
`QuantArchSurvey/`**.

Then report to the human: the §1 sentence, your four proposed tags with one line of
justification each, anything you left blank and why, and any disagreement with the seed tags
in `venues/ISCA/README.md`. Say plainly that the note is a **draft for them to rewrite**.
