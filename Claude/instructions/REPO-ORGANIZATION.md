# REPO-ORGANIZATION — where an agent puts things in this repo

Added **2026-10-02** at the human's request. For every Claude agent working in
`quantization_survey/`. Read it with [`AGENT-GUIDE.md`](AGENT-GUIDE.md), which owns the rules
about *what* the work is; this file owns *where its output goes and what it is called*.
Version control is [`G06-VERSION-CONTROL.md`](G06-VERSION-CONTROL.md); prose rules are
[`WRITING-STYLE.md`](WRITING-STYLE.md).

## Conclusions first

1. **Everything an agent writes about the work goes under `Claude/`** — rules, prompts, notes,
   reports, to-do lists, scripts. The only agent output outside it is per-paper reading material
   in `survey/papers/<Name>/` and, with the human's permission for that change, edits in
   `QuantArchSurvey/`.
2. **Pick the folder by what the file is for**, using the table in §2. A to-do list is not a
   note, a note is not a report, and a decision table is part of the report it belongs to.
3. **Numbered files are never renumbered and numbers are never reused.** A file that moves keeps
   a line saying where it came from, and its old number is retired.
4. **Every new file is linked from somewhere a person already reads** — the README's tables, the
   report it belongs to, or AGENT-GUIDE. An unlinked file is a file nobody finds.

## 1. The `Claude/` folder

```
Claude/
├── instructions/   # rules for agents — this file, AGENT-GUIDE, ENVIRONMENT, PAPER-READING,
│                   #   WRITING-STYLE, LATEX, G06-VERSION-CONTROL. UPPERCASE names, no number
├── prompts/        # copy-paste prompts for launching task-specific agents: NN-<slug>.md
├── notes/          # Notes-NNN-<slug>.md — reusable knowledge
├── reports/        # Reports-NNN-<slug>.md — one task's result
│                   #   + reports-NNN-tmp.md — the human's decision table for that report
├── todo/           # TODO-NNN-<slug>.md — open items left for later, with checkboxes
└── scripts/        # reusable scripts + templates/. One-off commands do NOT go here
```

## 2. Which folder

| Folder | Holds | Test | Lifetime |
|---|---|---|---|
| `instructions/` | A rule: *from now on we do X* | Did a human decide this is how the work is done? | Permanent; edited when the rule changes |
| `prompts/` | A prompt someone pastes into a fresh agent | Is it meant to be read by an agent that has read nothing else? | Permanent; superseded versions kept and marked |
| `notes/` | Reusable knowledge — a tool's real limits, a trap, a root cause | Will the next person waste time if this is not written down? | Permanent; appended over time |
| `reports/` | One task's input, method, result, conclusion, leftovers | What did this task deliver, and how far was it verified? | Permanent; closed when the task is |
| `todo/` | Open items: decisions waiting on the human, items for other owners, known-unsafe tools | Is this something that still has to be **done**? | Temporary; delete the file when every box is ticked |
| `scripts/` | Code that will be run again | Will someone run this a second time? | Permanent |

**The common mistakes, all made here at least once:**

- **A to-do list in `notes/`.** `Notes-003` was one, and moved to `todo/TODO-001` on 2026-10-02.
  A note records what is true; a to-do records what is not done yet. They age differently.
- **Leftovers buried in a report.** A report's *Not done* section says what the task did not do.
  Anything that someone still has to act on **also** goes in a `todo/` file, linked from the
  report, so it is found without rereading old reports.
- **A decision table as its own report.** It belongs to the report that proposed the decisions —
  see §4.

## 3. Naming

| Kind | Pattern | Example |
|---|---|---|
| Note | `Notes-NNN-<kebab-slug>.md` | `Notes-002-paper-source-access.md` |
| Report | `Reports-NNN-<kebab-slug>.md` | `Reports-003-isca-stage-type-tags-batch2.md` |
| Decision table | `reports-NNN-tmp.md`, lowercase, same `NNN` as its report | `reports-003-tmp.md` |
| To-do | `TODO-NNN-<kebab-slug>.md` | `TODO-001-isca-followups.md` |
| Prompt | `NN-<slug>.md`, `-v2` for a revision | `01-read-one-paper-v2.md` |
| Instruction | `UPPERCASE.md`; `G0N-` prefix for a file shared across all `~/moe_ws/` repos | `LATEX.md`, `G06-VERSION-CONTROL.md` |

- **`NNN` is zero-padded, monotonic within its kind, and never reused.** Before allocating, run
  `ls Claude/notes Claude/reports Claude/todo` **and** check `git log` for numbers committed since
  you last looked — two agents picking the same number is the known failure (G06 §7).
- **A moved or renamed file** starts with an italic line saying where it was created and that the
  old number is retired. Update every link to it in the same commit (`git grep` the old name).
- **Slugs are English, kebab-case, and say what the file is about**, not when it was written.

## 4. Reports and decision tables

The workflow that has worked for tag proposals, and the shape to reuse:

1. **The report** proposes, row by row, with a justification and the evidence for each row.
2. **The decision table** (`reports-NNN-tmp.md`) repeats only what the human needs to decide:
   the item, its old value, the proposal, and `☐ approve ☐ reject` plus free-text columns. Links
   go to the paper note and the PDF so each row can be checked without searching.
3. **The human writes in the table.** The agent reads it, applies only rows marked approve or
   given an explicit replacement, and **leaves undecided rows where they are**.
4. **The report gains a *Decisions* section** — proposed, decided, final, status — and decided
   rows are removed from the table. When none are left, both files are marked *closed*.
5. **Rules the human states while deciding** ("a paper with `S2T4` carries no `S2T1`") are written
   into the report's Decisions section the first time and applied to every later batch.

Decision tables are committed: they are the record of what the human decided, and the report
cites them.

## 5. Top-level layout, as it actually is

AGENT-GUIDE §1 describes the agreed layout and asks for a human before a new top-level directory
is added. **As of 2026-10-02 the tree has more than that**, added by the owner and not yet
reflected in AGENT-GUIDE:

| Path | In git | What it is |
|---|---|---|
| `Claude/`, `survey/` | yes | The agreed layout — see AGENT-GUIDE §1 |
| `writings/` | yes | Survey prose drafts, e.g. `taxonomy.md` (the ISCA fill of the taxonomy figure) |
| `figures/`, `scripts/`, `tables/` | **no** (untracked) | The owner's figure data, plotting scripts and generated figures |
| `quantization_survey_paper_pdf/` | **no**, and **not in `.gitignore`** | ~85 MB of paper PDFs. Never `git add` it |
| `archieve/` | no (ignored) | Cold storage for bulk sources |
| `QuantArchSurvey/` | no (ignored; its own repo) | The shared team repo — AGENT-GUIDE §0b |
| `latex/` | no (ignored; its own repo) | The manuscript — a clone of the Overleaf project, see [LATEX.md](LATEX.md). Moved here from `QuantArchSurvey/latex/` on 2026-10-15 |

**Do not tidy these on your own initiative.** Moving, renaming or committing the owner's untracked
directories is the owner's call; say what you see and ask.

## 6. Finishing a piece of work

Before reporting a task done:

- [ ] Output is in the folder §2 says, named as §3 says.
- [ ] Every new file is linked from the README, its report, or AGENT-GUIDE.
- [ ] Anything left for later is in a `todo/` file, not only in a report's *Not done*.
- [ ] Changes in `QuantArchSurvey/` were made with the human's permission for that change, and
      its `survey/gen/5-check.py` was run before and after (AGENT-GUIDE §0b).
- [ ] Commit per G06: name the paths, never `git add -A`, and say how far it was verified.
