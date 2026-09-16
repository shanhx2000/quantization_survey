# WRITING-STYLE — language rules for everything in this repo

Added **2026-09-16** at the human's request. Applies to **every Claude agent and human**
working here, and to all three sibling repos (`moe_placement/`, `quantization_survey/`,
`MobiQuant/`) — the rules are identical, each repo keeps its own copy so the file is
self-contained.

---

## The four rules

### 1. Code comments are always English

Every comment, docstring, inline note, assertion message, log line, `print` string,
CLI `--help` text and error message. No exceptions, including in throwaway
`playground/` scripts — throwaway code is exactly what someone else ends up reading.

### 2. Technical terms are always English

Never translate a technical term, and never invent a local-language equivalent for one.
Keep verbatim: commands, paths, flags, tool output, model and dataset names, paper
terminology, and the vocabulary of the field — *expert placement*, *all-to-all*,
*bit-slice*, *group size*, *zero-point*, *perplexity*, *router*, *prefix*, and so on.

### 3. Define a term where it is used, not only where it was introduced

**If a file uses an abbreviation or a project-specific term that is not defined in that
same file, restate the definition there** — one clause is enough — or link to the file
that defines it.

Why: files are read in isolation. A new agent opens one `ANALYSIS.md`, a reviewer opens
one report, a future you greps one source file. A term defined three files away is a term
nobody has. This costs one line to write and saves a lookup every time the file is read.

Examples of the habit:

- `ESP (expert sharding parallelism)` on first use in the file, not just in `Q6`.
- `FTD (fault-tolerant domain, a contiguous block of dies holding every expert)` —
  restate it in each file that reasons about FTDs.
- `PPL (perplexity, lower is better)` when a table reports it.
- `LWC (learnable weight clipping)` in every file that touches the calibration code.

### 4. Prose is English by default

Write documents, notes, reports, analyses, commit messages and PR text in English.
**Avoid Chinese unless the human explicitly asks for it** for a given piece of work.

---

## Scope, and what this does *not* mean

- **Applies to everything newly written or edited** from 2026-09-16 on.
- **Does not mean retro-translating the existing corpus.** Large parts of
  `moe_placement/` and `MobiQuant/` were written in Chinese under the earlier
  convention. Leave them alone unless asked.
- **When editing an existing Chinese file**, write the new text in English rather than
  matching the surrounding language. If that leaves a file badly mixed, say so and offer
  to convert the whole file — do not convert it unprompted, and do not silently keep
  writing Chinese to stay consistent with the old text.
- **Quoting is not writing.** A verbatim quote from a Chinese source stays in its
  original language, as any quote would.

## Where the earlier rule lived

This supersedes the older conventions that said the opposite:

- `moe_placement/Claude/instructions/AGENT-GUIDE.md` §4 used to end with
  *"正文用中文"* (write prose in Chinese). That clause is gone.
- `quantization_survey/Claude/instructions/AGENT-GUIDE.md` used to note that the sibling
  `moe_placement/` repo writes prose in Chinese. That cross-reference is stale; all three
  repos now share one rule.
