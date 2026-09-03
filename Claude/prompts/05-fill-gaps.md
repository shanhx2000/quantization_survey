# Prompt — find and file what the corpus is missing

> Acquisition, not reading. Ends with papers filed at `brief ready`, or an honest
> statement of what could not be obtained.

---

You are filling known gaps in the corpus for a survey on quantization architecture.

**Read first:**
- `Claude/instructions/AGENT-GUIDE.md` §2–3 — recording rules and the **arXiv-only** PDF rule
- `Claude/notes/Notes-002-paper-source-access.md` — what is and is not reachable from this
  host. Measured, not guessed: ACM DL and IEEE Xplore return **403 to scripts even on
  landing pages**
- `survey/README.md` — the scope taxonomy and the master table
- `QuantArchSurvey/TAXONOMY.md` — what the survey's spine needs these papers *for*

**The gaps, in priority order:**

1. ✅ **Done — TransArray is filed.** The human identified it (2026-09-03) as *"Transitive
   Array: An Efficient GEMM Accelerator with Result Reuse"*, and it is now
   `survey/papers/TransitiveArray/` at `brief ready`. All 40 rows of their ISCA list are
   covered. Do not re-file it.
2. **The papers the scope taxonomy names but the corpus does not contain** — an ISCA-only
   sweep cannot supply them, and their absence leaves the taxonomy's §1.2 and §1.3 branches
   nearly empty:
   `Posit` · `APoT` · `ANT / Flint` (MICRO'22) · `GOBO` (MICRO'20) · `BiScale` ·
   `NormalFloat / NF4` · k-means codebook quantization.
   Most are MICRO / ICLR / NeurIPS, i.e. **outside ISCA**. Their taxonomy already treats
   ANT and GOBO as load-bearing (`G2` adaptive-type anchor and `G3` early-codebook anchor).
3. **Anything else the master table's "Known gaps" section lists** as missing.

**Method:**

```bash
bash Claude/scripts/new_paper.sh <ShortName> <arxiv-id>   # scaffold, then download + extract
```

- **PDFs come from arXiv only.** Metadata may additionally come from ACM DL / IEEE Xplore
  records — including what their records expose through web search, since the pages
  themselves 403. **No other source**: not author homepages, not university mirrors, not
  ResearchGate / Semantic Scholar / OpenAlex / Crossref, **even when one of them serves a
  legitimate free copy**. One auditable provenance chain per paper.
- Check for an arXiv version by exact-title search against the arXiv API before concluding
  there is none. Sleep ~3 s between calls.
- **No arXiv version ⇒ the paper stays `pdf missing`.** Add it to the "Needs a human
  download" table in `survey/README.md` with title, venue, DOI, record link and why we want
  it. Do **not** substitute a copy from elsewhere. Note explicitly if it is ACM Open — free
  in a browser, blocked only to scripts, so it needs a human but **not** a subscription.
- Each filed paper gets a real `ANALYSIS.md`: verified publication info (venue + year
  minimum; DOI and pages when the ACM/IEEE record gives them, marked second-hand if so),
  the **verbatim** abstract, why it is in the survey, and status `brief ready`.
- **A paper from outside ISCA is a scope question.** File it, and flag in your report that
  the corpus is no longer ISCA-only — that is the human's call to ratify, not yours.

**Produce:** the new paper directories, plus a report of what you filed, what you could not
get and exactly why, and which taxonomy branch each new paper populates.

**Non-negotiable:**

- **Never write anything into `QuantArchSurvey/`.** Verify with `git status --short`.
- **Do not edit `survey/README.md`** beyond the "Needs a human download" table and the
  master table rows for papers you actually filed — other agents may be running.
- **Never bypass a paywall.** If a publisher blocks you, that is the answer; record it and
  queue the paper for a human.
- Do not pad the corpus. A paper that does not populate a named gap does not get filed.
