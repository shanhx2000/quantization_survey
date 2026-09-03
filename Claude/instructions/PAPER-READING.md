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

## 1. What you are producing — exactly one file

**`survey/papers/<Name>/ANALYSIS.md`.** That is your whole deliverable. Update the file
that is already there.

Its purpose is **to help the human read the paper faster** — not to replace their reading.
They then write `survey/papers/<Name>/paper-note.md` themselves and copy it into the shared
repo. See [`AGENT-GUIDE.md`](AGENT-GUIDE.md) §0b for the three steps and who owns each.

**Do not create `paper-note.md`.** Do not create a file shaped like
`QuantArchSurvey/templates/paper-note.md`. That is the human's authored note, and drafting
it takes their step away from them. Read their template to know *what they will need from
you* — then put those things in `ANALYSIS.md`.

Inside `ANALYSIS.md`, add a **"For the note"** section carrying the material their template
asks for that our format does not already hold:

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

## 7. Before you finish

```bash
bash Claude/scripts/check_survey.sh          # declared status vs. what is on disk
cd QuantArchSurvey && git status --short     # MUST be empty
```

Also confirm you did **not** create `paper-note.md` — that file is the human's.

Then report to the human: the §1 sentence, your four proposed tags with one line of
justification each, anything you left blank and why, and any disagreement with the seed tags
in `venues/ISCA/README.md`.
