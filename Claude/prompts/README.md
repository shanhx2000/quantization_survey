# prompts/ — copy-paste prompts for launching agents

Each file is one prompt, written to be **pasted whole** into a fresh agent. They carry
their own constraints, so an agent that reads nothing else still cannot break the rules.

Fill the `<ANGLE BRACKETS>` before sending. Everything else is deliberate.

| Prompt | Use it when | Scale |
|---|---|---|
| [`01-read-one-paper.md`](01-read-one-paper.md) | **The main one.** One paper, close read → updated `ANALYSIS.md` with a `For the note` section | 1 paper, 1 agent |
| [`02-read-thread.md`](02-read-thread.md) | A cluster that only makes sense together (the outlier thread, the LUT line) — cross-comparison is the point | 3–6 papers, 1 agent |
| [`03-audit-numbers.md`](03-audit-numbers.md) | After papers are read: check the results tables and fairness lines against the PDFs | 5–10 papers, 1 agent |
| [`04-tag-mapping.md`](04-tag-mapping.md) | Once, to build our-tags → their-axes mapping and draft all 40 ISCA rows | whole corpus |
| [`05-fill-gaps.md`](05-fill-gaps.md) | To find and file what the corpus is missing (TransArray, Posit/APoT/ANT/GOBO/BiScale/NF4) | 1–8 papers |

## Rules every prompt repeats, because they are the ones that matter

1. **`QuantArchSurvey/` is read-only.** Six other people own venues in it.
2. **The agent never writes `paper-note.md`.** Step 1 (reading assistance, `ANALYSIS.md`)
   is the agent's; step 2 (writing the note) and step 3 (copying it into the shared repo)
   are the human's. See [AGENT-GUIDE §0b](../instructions/AGENT-GUIDE.md).
3. **PDFs from arXiv only.** The full text is already extracted and committed — you
   should not need to download anything.
4. **Mark verified vs. inferred**, and never move a number without its frame.

## Practical notes

- **One paper per agent** is the right default. The template's §2 and §4 need the whole
  paper in context, and a shared agent across ten papers reads all of them shallowly.
  Use [`02-read-thread.md`](02-read-thread.md) only when the *comparison* is the deliverable.
- Launch several single-paper agents **in parallel** — they touch disjoint directories, so
  they do not conflict. The one shared file is `survey/README.md`; tell them not to edit it
  (the prompts already do) and update it yourself afterwards.
- Point every agent at [`../instructions/PAPER-READING.md`](../instructions/PAPER-READING.md)
  rather than re-explaining the method; keep the prompts about *which* paper and *what for*.
