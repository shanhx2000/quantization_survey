# Prompt — read a thread of related papers

> Use this **only** when the cross-comparison is the deliverable. For individual notes,
> launch [`01-read-one-paper.md`](01-read-one-paper.md) once per paper instead — an agent
> spread across many papers reads all of them shallowly.

Fill in `<THREAD NAME>` and `<PAPERS>`.

---

You are reading a **thread of related papers** for a survey on quantization architecture.
The point is not five separate notes — it is **what the thread argues with itself about**.

**Read first:** `Claude/instructions/PAPER-READING.md`, `Claude/instructions/AGENT-GUIDE.md`
§0b, and `QuantArchSurvey/TAXONOMY.md`.

**Thread:** `<THREAD NAME>`
**Papers:** `<PAPERS>` (directories under `survey/papers/`)

Full text for each is already extracted and committed under `extracted/`. **Download
nothing.** Each directory's `ANALYSIS.md` holds a brief from an abstract-level read —
hypotheses, not ground truth.

**Produce:**

1. An updated `ANALYSIS.md` in each paper's directory, including its `## For the note`
   section. Depth per paper may be lighter than a solo read, **but the one-line summary, the
   data-type detail and the fairness verdict must be solid**. **Do not create
   `paper-note.md` in any of them** — that file is the human's own writing.
2. `Claude/reports/Reports-NNN-<thread-slug>.md` — the real deliverable. Check
   `ls Claude/reports` for the next free number; numbers are never reused.

**The report must answer, with evidence:**

- **What each paper claims the previous one got wrong.** These threads are arguments. Quote
  the criticism and name where it appears. Example already in our notes: MicroScopiQ argues
  "adjacent outliers matter" against OliVe's locality assumption; Tender reports beating
  OliVe on perplexity. Find every such pair in your thread.
- **Which claims are actually comparable.** Different baselines, nodes, models, accuracy
  targets and evidence levels usually mean two headline numbers cannot be put in one table.
  **Say so explicitly** rather than tabulating them anyway. If a comparison *is* fair,
  build the table.
- **What the thread has converged on**, and what is still contested.
- **The mechanism-cost comparison** the survey outline §5.2 asks for: silicon cost per point
  of accuracy for each approach in the thread, or a clear statement of why the published
  numbers do not support that comparison.
- **A recommended reading order** with one line on what each paper adds.

**Non-negotiable:**

- **Never write anything into `QuantArchSurvey/`.** Shared repo, six other owners. Verify
  with `cd QuantArchSurvey && git status --short` — must be empty.
- **Do not edit `survey/README.md` or `survey/TAGS.md`.** Report; the human edits.
- Mark `**verified**` / `**inferred / not verified**` on every claim; keep every number's
  frame; distinguish evidence levels (silicon / post-synthesis / RTL / simulator /
  analytical) and never pool them.
- Conclusions first: the report opens with its findings, details after.

**Report back:** the thread's central disagreement in two sentences, which comparisons you
judged unfair and why, and the reading order.
