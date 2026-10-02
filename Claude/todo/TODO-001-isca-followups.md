# TODO-001 — open ISCA follow-ups (2026-10-02)

*Created as `Claude/notes/Notes-003-todo-isca-followups.md` and moved here on 2026-10-02; the
number Notes-003 is retired.*

**A to-do list, not a finding.** Everything below was left open on purpose during the ISCA tag
audit ([Reports-001](../reports/Reports-001-isca-tag-audit.md)) and the two Stage-type batches
([Reports-002](../reports/Reports-002-isca-stage-type-tags.md),
[Reports-003](../reports/Reports-003-isca-stage-type-tags-batch2.md)). Tick an item when it is done
and say where; delete the file when every box is ticked.

Abbreviations: PIM (processing-in-memory), NDP (near-data processing), SNN (spiking neural network).

## Needs the owner's decision

- [ ] **RAELLA venue Stage.** Venue row `—`, published note `S2`. The Stage-type tags
      `S2T5` · `S3T2` · `(PIM)` imply venue `S2` with path `S3→S2` (pim.md already gives that
      path). Set it, or keep `—` for the PIM owner.
- [ ] **XtraMAC venue Stage.** Venue row `—` (the 2026-09-22 FPGA owner reset), note `S2`; the
      Stage-type tag is `S1` and the path classifier's `OVERRIDE` already says `S1→S2`. Pick `S1`,
      `S2`, or leave `—` for the FPGA owner.

## Shared repo (`QuantArchSurvey/`) — other owners' items, raise with them

- [ ] **Nine DAC 2016–2018 records have no short name** in `survey/gen/names.py` (added in upstream
      commit 8922a85). Without names `survey/gen/5-check.py` crashes; locally it is run with a
      placeholder written only into the gitignored `survey/gen/named.json`. DAC owner.
- [ ] **One of those nine is spiking** — *Towards Accurate and High-Speed Spiking Neuromorphic
      Systems…* (DAC'18) — and is missing from `survey/snn.md`'s *In the corpus* table. That is the
      one remaining `5-check` failure this work touches (`snn.md` says 4, `plat_snn` is 5).
- [ ] **Tell the other owners that `papers.md` gained a `Stage type` column** (between Platform and
      Audit A) on 2026-10-02. Anyone adding a row by hand must add the extra cell; `5-check.py`
      now expects 10 cells and fails if a cell disagrees with its note's `Stage type` row.
- [ ] `venues/ASPLOS/README.md:145` still says *383 records*. ASPLOS owner.
- [ ] `5-check.py` reported 189 problems at the last run (192 on upstream `main` before this work);
      the rest are stale prose counts in shared pages, not ISCA rows.

## This repo

- [ ] **`Claude/scripts/sync_notes.py` is unsafe to run.** Our `paper-note.md` files still carry the
      retired `Generation` row where the published notes have `Stage`, so a sync would revert every
      published note's Stage line. Port the Stage rows back first. RingCNN is no longer `EXCLUDED`
      and would be republished although upstream moved it to `legacy/` — add it.
- [ ] **`latex/figures/taxonomy.tex` is edited locally and not pushed to Overleaf.** 23 of 24 leaves
      carry the ISCA fill. Pull, compile `figures/taxonomy-preview.tex`, check page height, commit,
      push (see [LATEX.md](../instructions/LATEX.md)). ELSA is still named in it — kept on purpose,
      as in `writings/taxonomy.md`, where it is marked *(may not fit)*.
- [ ] **`quantization_survey_paper_pdf/` (~85 MB of PDFs) is not covered by `.gitignore`.** Add a
      rule before anyone runs a broad `git add`.
- [ ] **Untracked owner work still not committed:** `figures/`, `scripts/`, `tables/`,
      `Claude/scripts/build_index.py`, `Claude/reports/reports-001-tmp.md`.
- [ ] **Stage-type tags for other venues.** Only ISCA rows from 2022 on are tagged. ISCA 2018–2021
      (already two-reviewer audited) and the other venues are untouched.
