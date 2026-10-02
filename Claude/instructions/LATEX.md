# LATEX — managing the survey manuscript

Added **2026-10-01** at the human's request. For every Claude agent (and human) that touches
the manuscript. Read [`AGENT-GUIDE.md`](AGENT-GUIDE.md) §0b and
[`G06-VERSION-CONTROL.md`](G06-VERSION-CONTROL.md) first.

## Conclusions first

1. **Overleaf is the single source of truth.** The manuscript lives in one Overleaf project;
   every local copy is a clone of it, and nothing else holds the text.
2. **The local clone is `QuantArchSurvey/latex/`.** It is its own git repo, not a submodule,
   and both outer repos ignore it — `QuantArchSurvey/.gitignore` has `/latex/`, and ours
   ignores the whole of `QuantArchSurvey/`. **Never commit manuscript files to either outer
   repo.**
3. **Pull and push are human steps.** Overleaf asks for a git token, and agent sessions here
   cannot answer the prompt. Verified 2026-10-01: `git fetch` fails with
   `could not read Password for 'https://git@git.overleaf.com': terminal prompts disabled`.
4. **There is no TeX on this host.** `pdflatex`, `lualatex` and `latexmk` are all absent
   (checked 2026-10-01), so nothing can be compiled here. Overleaf compiles.
5. **A push to Overleaf is live in every co-author's editor at once.** There is no review step
   and no branch to hide behind. Treat it as publishing.

## Source

```bash
cd ~/moe_ws/quantization_survey/QuantArchSurvey
git clone https://git@git.overleaf.com/6a98c3ae3305c3abab2c1b63 latex
```

- **Username** `git`. **Password: an Overleaf git token, not the account password** —
  *Overleaf → Account Settings → Git integration → Create token*. You need access to the
  project; ask Haoxuan if you do not have it.
- **Never write the token anywhere**: not into the remote URL, a credential file in the repo,
  a note, a report, a commit message or a shell history line someone else will read. Let git
  prompt for it.
- The remote is `origin`; the only branch is `main`. Overleaf's git bridge works with one
  branch, so do not create others and expect them to appear in Overleaf.

## Layout

| Path | What it is | Edit? |
|---|---|---|
| `main.tex` | preamble, title, authors, then one `\input` per section | rarely; front matter only with the human |
| `macros.tex` | **every** `\usepackage` and `\newcommand` | add packages here, never in a section |
| `sections/NN-*.tex` | one file per section, `00-abstract` … `12-appendix` | yes, the file you were asked about |
| `figures/taxonomy.tex` | Fig. 1, a `forest` tree; one level-1 branch per owner | your own leaves only (see below) |
| `figures/taxonomy-preview.tex` | standalone A3 wrapper that compiles only the taxonomy | set it as main document in Overleaf to iterate on the figure |
| `figures/timeline.tex` | TikZ timeline | yes, with the human |
| `refs.bib` | the manuscript's bibliography (see *Citations*) | yes, with review |
| `acmart.cls`, `ACM-Reference-Format.bst` | ACM template | **never** |

**Section file names still carry the retired Generation names** — `03-g1-…`, `04-g2-…`,
`05-g3-…`. The text has moved to Stages. Do not rename them on your own initiative: a rename
changes `main.tex` and breaks every co-author's open editor tab at the same moment.

## Workflow

Every change, in this order:

1. **Human pulls first:** `git -C QuantArchSurvey/latex pull`. Co-authors edit Overleaf
   directly, so a stale clone is the normal state, not the exception. Run `git status` in
   `latex/` and say what is already modified before you add to it.
2. **Agent edits only the files the human named**, in English, defining every abbreviation in
   the file that uses it ([`WRITING-STYLE.md`](WRITING-STYLE.md)). Leave other people's
   comments as they are, whatever their language.
3. **Agent checks what it can without TeX**, and says that is all it checked:
   brace and bracket balance with comments stripped (`%…` and `\{` `\}` removed first);
   every `\cite{key}` exists in `refs.bib`; every `\ref`/`\label` pair matches; no new
   package outside `macros.tex`.
4. **Human compiles in Overleaf** — the whole document, or `taxonomy-preview.tex` for the
   figure — and looks at the page. A figure scaled with `\resizebox{\textwidth}{!}` keeps its
   aspect ratio, so adding rows can push it past the page height without any error.
5. **Commit with a G06 message** (what, why, how far verified — *"not compiled"* is a valid
   and necessary line), naming the paths. The agent may commit locally; **the human pushes**.
6. **Never force-push**, never rebase anything already pushed. If the push is rejected,
   pull, resolve, push again.

## Citations — two stores, not yet reconciled

| | Keys | State on 2026-10-01 |
|---|---|---|
| `latex/refs.bib` | `firstauthor-shorttitle-year` (`park-olaccel-2018`) | 12 entries, written to make §1 compile; several marked `% VERIFY` |
| `QuantArchSurvey/bibtex/<CONF>.bib` | Google Scholar `authorYearFirstword`, per [`legacy/guidelines/BIBITEM.md`](../../QuantArchSurvey/legacy/guidelines/BIBITEM.md) | **every file is empty** |

**Do not `\cite` a key that is not in `refs.bib`** — it prints `[?]` and Overleaf only warns.
This is why the ISCA fill of `taxonomy.tex` uses plain paper names rather than `\cite`. Which
store becomes canonical, and which key scheme survives, is the human's decision; until it is
made, do not migrate keys between them.

## The taxonomy figure

`figures/taxonomy.tex`'s header sets the rules; the ones that bite:

- **Edit your own leaves.** Each level-1 branch has an owner. ISCA's papers are appended to a
  leaf as `\\ \textit{ISCA:} Name, Name, ...` before its `\fillhere`.
- **Keep `\fillhere`** while any venue still has papers to add to that leaf; it prints the grey
  *[add papers]* marker.
- **Never remove the braces** around node text — a bare comma inside a node is read as a
  `forest` option.
- The paper list for each leaf is derived from [`../../writings/taxonomy.md`](../../writings/taxonomy.md);
  change that file first, then the `.tex`.

## Current state

*(update this when it changes)*

- **2026-10-01:** local `main` is at `25d9f79`, which equals `origin/main` as last fetched — but
  the fetch could not authenticate, so Overleaf may be ahead. `figures/taxonomy.tex` is
  **modified locally and uncommitted**: 23 of 24 leaves carry the ISCA fill. Brace/bracket
  balance checked; **not compiled**. Next: human pulls, compiles `taxonomy-preview.tex`,
  checks the page height, commits, pushes.
