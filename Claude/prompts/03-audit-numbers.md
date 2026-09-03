# Prompt — audit the numbers and the fairness lines

> Run this **after** papers have been read. It is a verification pass, not a reading pass:
> it checks what earlier agents wrote against what the papers say.

Fill in `<PAPERS>`.

---

You are auditing recorded results for a survey on quantization architecture. Earlier agents
read these papers and filled in their `Key numbers, with their frame` tables and their
notes. **Your job is to try to break those records**, not to extend them.

**Read first:** `Claude/instructions/PAPER-READING.md` §3–4 (what a frame and a fairness
line must contain) and `Claude/instructions/AGENT-GUIDE.md` §0b.

**Papers to audit:** `<PAPERS>` (directories under `survey/papers/`)

For each, check `ANALYSIS.md` against the extracted full text. If the human has already
written a `paper-note.md` in that directory, **read it but never edit it** — it is their
authored note; report defects you find in it instead.

**For every recorded number, verify:**

1. **It exists in the paper**, at the section or table cited. Quote the sentence. A number
   that cannot be located gets struck, not softened.
2. **Its frame is complete and correct** — model, task/dataset, baseline, bitwidth,
   granularity. A wrong baseline is worse than a missing number.
3. **Its evidence level is stated and right** — silicon measurement / post-synthesis / RTL
   sim / simulator / analytical model. Papers routinely present projections in the same
   table as measurements.
4. **Peak versus end-to-end.** Prefer end-to-end. Where only peak is recorded and the paper
   also reports end-to-end, that is a defect: fix it and note it.
5. **The escape hatch is accounted for.** If the paper keeps a fraction of values, the first
   and last layer, accumulators or softmax at high precision, the effective bitwidth is
   higher than the headline. Compute it where the paper gives enough to do so.

**Then answer, per paper:** is the headline comparison **iso-area, iso-accuracy, iso-node,
iso-era** — or none of these? Rewrite the "is the comparison fair?" line where it is thin.

**Produce:** `Claude/reports/Reports-NNN-<slug>.md` (check `ls Claude/reports` for the next
number) containing:

- **Conclusions first**: how many recorded numbers survived, how many were corrected, how
  many struck.
- A defect table: paper · what was recorded · what the paper says · severity.
- The survey-outline §9.5 datum: **how many of the audited papers use a same-node,
  same-accuracy baseline.** The outline predicts an uncomfortable answer — report the real
  one either way.
- Corrections applied in-place to each `ANALYSIS.md`, listed here. Defects found in a
  human-written `paper-note.md` are **reported, never edited**.

**Non-negotiable:**

- **Never write anything into `QuantArchSurvey/`.** Verify with `git status --short`.
- Do not edit `survey/README.md` or `survey/TAGS.md`.
- **Report defects you cannot fix.** If a paper's own numbers are internally inconsistent,
  that is a finding — record it, do not paper over it.
- Do not add new numbers that were not previously recorded unless they replace a defective
  one. This is an audit, and scope creep dilutes it.
