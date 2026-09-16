# Prompt — read one paper and prepare reading assistance

**This is the main prompt.** Papers are done one at a time; launch one agent per paper.

> Fill in `<PAPER>` (a directory name under `survey/papers/`) and send the rest as-is.

---

You are preparing **reading assistance** for one paper, for a human writing a survey on
quantization architecture. They will read the paper themselves and rewrite the note you draft.
Your job is to make that reading faster and better-aimed — not to replace it.

**Read these first, in order:**
1. `Claude/instructions/PAPER-READING.md` — your method. Follow it; do not improvise.
2. `Claude/instructions/AGENT-GUIDE.md` §0b — the four-step workflow and who owns each step.
3. `QuantArchSurvey/TAXONOMY.md` — the four tag axes you will propose values for.
4. `QuantArchSurvey/templates/paper-note.md` — the shape your note draft must take. Copy the
   structure into `survey/papers/<PAPER>/paper-note.md`; **never write inside that directory.**

**Your paper:** `survey/papers/<PAPER>/`

Full text is already extracted and committed there under `extracted/`: read
`<stem>.txt` (the `-layout` version) and grep `<stem>.raw.txt`; use `<stem>.pages/pNN.txt`
to say which page something is on. **Download nothing.** `ANALYSIS.md` already holds a
brief written from an abstract-level read — treat it as a hypothesis to confirm or
overturn, not as ground truth.

**Your deliverables are two files, both under `survey/papers/<PAPER>/`.**

**First, `ANALYSIS.md`.** Update it:

- **Fill the `Key numbers, with their frame` table** — this is the main thing missing.
- **Fill `Method`, `Cost and requirements`, `Limitations and open questions`,
  `Relation to other entries`.**
- **Correct the brief** where the close read contradicts it; the close read wins. Say in one
  line what changed rather than silently overwriting.
- **Raise the status** to `analysis ready` and rewrite `How far it was read:` to name which
  sections you read closely versus skimmed.
- **Add a `## For the note` section** with: the one-line summary in their §1 sense (what
  data type, what optimization, what the hardware gets out of it); proposed values on their
  four axes with one line of evidence each; a proposed venue-list row as a fenced block;
  and their §4 fairness verdict.

**Second, `survey/papers/<PAPER>/paper-note.md`** — a **draft** of the human's note in
`QuantArchSurvey/templates/paper-note.md` form, which they will rewrite. Write it *after*
`ANALYSIS.md` and as a compression of it: nothing goes in the note that is not in the
analysis with its evidence. **Read `PAPER-READING.md` §6a for the register** — the human's
notes run well under half the length of an agent's default. Keep the tags table, the §1
sentence and the §4 results table at full care; write **§2 through §5 as terse fragments** —
*"just a few key words / key conclusions"* — with no `**verified**` markers and no page
citations. **Budgets: §2 = one labelled point per line, keyword-dense, no paragraphs; §3 = room to breathe (a labelled paragraph per mechanism
— it is "what was actually built"); §4 = the table only; §5 = LEAVE EMPTY, heading and nothing
else, because the placement and generation judgments there are the human's.** Offer your §5
material in `## 6. Claude notes` instead.
A bold label plus a single line is a complete entry; prefer a number or a derivation over a
sentence describing it. Keep the §4 fairness verdict as the table's **last row**
(`| **Is the comparison fair?** | … |`) — it is the most valuable line in the note and must
not be lost to the "table only" rule — but keep it to **verdicts, not discussion**: what is iso,
what is not, the number not to quote, and nothing else. **~50-60 words, ceiling ~70.** No "because"
clauses, no section numbers, no mechanism — the reasoning stays in `ANALYSIS.md`. §2 must still carry format-per-tensor-class,
granularity with group size, outlier mechanism, the escape hatch, and PTQ vs QAT.

Then **add a `## 6. Claude notes` section** past the template's §5 — short bullets carrying
your suggestions: what you would argue for that they may not want, cross-paper observations,
a number you think should be excluded, a section you would fill. It must open by saying
**strip this section before copying into `QuantArchSurvey/venues/ISCA/notes/`** — §6 is
scaffolding for the human's rewrite and never reaches the team repo.

**The note goes in `survey/papers/<PAPER>/`, never in `QuantArchSurvey/`.** Copying it into
`venues/ISCA/notes/` is the human's step, not yours. Say in your report that the note is a
draft for them to rewrite.

**Priorities.** Their repo's README is explicit that this is not a form-filling exercise:

> The deliverable for one paper is **the sentence in §1** — what data type, what
> optimization, and what the hardware gets out of it. §1, §2 (data type) and the "is the
> comparison fair?" line in §4 are worth more than a fully but shallowly filled template.

So: get the one-line summary right first, then the data-type detail, then fairness. Leave a
field empty rather than guessing, and say what you left and why.

**On data type, "low precision" is not an answer.** Give: exact format and bitwidth **per
tensor class** in field notation (`W4A16`, `W8A8`, `W4A4KV4`); scale granularity **with the
group size**; the outlier mechanism or an explicit "none"; the **escape hatch** — almost
every paper keeps something at high precision (accumulators, first/last layer, softmax, a
few percent of values), and a "4-bit" method holding 3% at FP16 has a far higher effective
bitwidth; and whether it needs PTQ or QAT.

**Non-negotiable:**

- **Never write anything into `QuantArchSurvey/`** — not files, not git config, not a
  commit. It is a shared repo owned by six other people. Read it freely. Before finishing,
  run `cd QuantArchSurvey && git status --short`; it must be empty.
- **Do not edit `survey/README.md`, `survey/TAGS.md` or `survey/papers-tags.csv`** — other
  agents may be running in parallel and the human maintains those. Report what should change.
- **Mark every claim** `**verified**` (with section/table) or `**inferred / not verified**`.
- **Every number needs its frame**: model, task, baseline, bitwidth, granularity, and its
  evidence level — silicon measurement / post-synthesis / RTL sim / simulator / analytical
  model. Never pool evidence levels. Prefer end-to-end numbers over peak.
- **Do not "correct" a pre-2023 `G3` seed tag.** Their taxonomy deliberately tags OLAccel
  (ISCA'18), GOBO (MICRO'20) and Mokey (ISCA'22) as `G3` — early instances of the outlier
  and codebook threads. Generation is judged by paradigm, never by year.
- **PDFs from arXiv only**, if you somehow need one at all.

**Report back:** the one-line summary; your four proposed tags each with one line of
justification; what you left blank and why; and any disagreement with the seed tags in
`QuantArchSurvey/venues/ISCA/README.md`, with evidence. Disagreement is useful output —
flag it, do not resolve it silently.
