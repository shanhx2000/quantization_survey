# Notes-002 — what is actually reachable when fetching papers

**Conclusion first:** from this host, **arXiv works and the two publishers do not**.
`dl.acm.org` and `ieeexplore.ieee.org` return **403 to scripts even on landing pages** —
not just on PDFs — so neither the full text nor the metadata can be fetched from them
directly. Combined with this project's arXiv-only provenance rule, that is why 13 of the
39 filed papers sit at `pdf missing`.

All of it measured 2026-09-02. Re-check before assuming any of it still holds.

---

## The provenance rule (project policy, not a technical limit)

**PDFs come from arXiv only. Metadata may additionally come from the ACM DL and IEEE
Xplore records. No other source** — not author homepages, not university mirrors, not
ResearchGate / Semantic Scholar / OpenAlex / Crossref — **even when one of them serves a
legitimate free copy**.

The reason is one auditable provenance chain per paper: an author-hosted PDF may differ
from the published version, and aggregator metadata is unverified, so mixing them makes
the survey's citations impossible to audit.

**This rule has teeth.** Six papers were downloaded from author and institution pages
before the rule was set — `Gist` (microsoft.com), `JPEG-ACT` (ubc.ca), `TPUv4i`
(gwern.net), `RaPiD` (epfl.ch), `SpZip` (csail.mit.edu), `CommutativeDataReordering`
(bfeinberg.com) — **all six were deleted** and their papers moved to the human-download
queue. If a paper has no arXiv version, it stays `pdf missing`. Do not substitute.

## What each source does

| Source | Result | Detail |
|---|---|---|
| **arXiv PDF** (`arxiv.org/pdf/<id>`) | ✅ works | 13/13 downloaded with plain `curl -sSL`; no UA spoofing needed |
| **arXiv API** (`export.arxiv.org/api/query`) | ✅ works | title, authors, abstract, version, dates, and the **`comments` field** |
| **dl.acm.org** landing page | ❌ **403** | verified on `10.1145/3695053.3731018` |
| **dl.acm.org** PDF, *including ACM Open* | ❌ **403** | tried with a browser UA on three papers marked open access — all 403 |
| **ieeexplore.ieee.org** landing page | ❌ **empty** | returns a body with no content to a fetcher |
| Google/web search | ✅ useful | search *results* surface the ACM/IEEE records' DOI, pages, authors — the allowed way to get publisher metadata |

**ACM Open is a trap.** `AQB8`, `Cambricon-SR` and `FATE` are genuinely open access —
free to anyone with a browser — and still 403 every scripted request. They need a human,
but **not a subscription**. Say so in the download queue, or someone wastes time hunting
for institutional access they don't need.

## Getting the venue right without the publisher page

The arXiv API's **`comments` field is the best available venue evidence** and is worth
quoting verbatim in `ANALYSIS.md`. Of 13 arXiv-sourced papers, 11 state the venue there:

- explicit: `"ISCA 2023"`, `"ISCA 2025"`
- forward-looking: `"To appear at the 51st International Symposium on Computer Architecture"`,
  `"Accepted by 47th International Symposium on Computer Architecture"`
- versioned: `"Conference Version (ISCA'25). Fixed a typo"`

**Two say nothing**: `BitFusion` (arXiv 2017, predates the ISCA'18 acceptance) and
`Oaken` (comment is only `"16 pages, 14 figures, and 4 tables"`). Their venue rests on
the source CSV's year grouping alone and is flagged **not independently verified** in
both `ANALYSIS.md` files and under the master table. Don't quietly promote those.

⚠️ A "to appear" comment also means the archived PDF is a **camera-ready-or-earlier
draft**. Preprint vs. published version is **uncompared for every arXiv entry here**.

## Checking whether an arXiv version exists at all

```bash
curl -s 'http://export.arxiv.org/api/query?search_query=ti:"<exact title>"&max_results=3'
```

Returns a feed whose only `<title>` is the query echo when there is no hit. All 13
queued papers were checked this way — **none has an arXiv version**, which is the whole
reason they are queued. Sleep ~3 s between calls; the API is not rate-limit friendly.

**The 13 with no arXiv version** cluster in the old years: ISCA 2018 (2 of 3), 2020
(4 of 5), 2021 (4 of 5), 2025 (3 of 9). Everything from ISCA 2022–2024 on the list is on
arXiv. Expect a similar split if the survey extends backwards to MICRO/HPCA of the same
era; **budget for human downloads when adding pre-2022 work.**

## Aggregator APIs — why they are not used

`api.openalex.org`, `api.crossref.org` and `api.semanticscholar.org` all answer, and
Crossref in particular returns clean DOIs and page ranges. **They are out of bounds under
the provenance rule above.** Recorded here only so the next agent doesn't rediscover them
and assume they are fair game. (OpenAlex also 429s aggressively — three calls in a row
was enough.)
