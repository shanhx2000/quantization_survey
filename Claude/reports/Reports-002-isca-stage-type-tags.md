# Reports-002 — Stage × Type tags for ISCA papers, batch 1 (2026-10-02) — closed

**Input:** the stage vocabularies in `QuantArchSurvey/survey/` (`stages.md`, `stage1.md`, `stage2.md`,
`stage3.md`, `stage0.md`, `papers.md`) at upstream `main` 8922a85, and ten ISCA papers from 2022 on
— the oldest ten of the 26: Mokey, OliVe, RAELLA, Tender, Transitive Array, LUT Tensor Core,
MicroScopiQ, Oaken, AQB8, Ecco. **Method:** read each published note's Tags, §1 and §2, compared
with the classifier's current `papers.md` Stage and Type cells and with each stage page's tables.
No PDF was opened — every call below was settled by the note and the stage pages, so none needed the
extracted text. **Nothing is applied yet**; decide in [`reports-002-tmp.md`](reports-002-tmp.md).

## The tag, in one paragraph

`S{stage}T{type}` names **which stage's vocabulary** a mechanism belongs to and **which type within
it**. Each stage numbers its own types from 1, so the `S` is what disambiguates — a bare `T2` means
*mixed precision* in stage2.md and *back into arithmetic* in stage3.md.

| Tag | Means | Defined in |
|---|---|---|
| `S1` | one designed scalar element. Stage 1 has no type vocabulary, so the tag is bare `S1`; when a stage1.md §3 element tag matches well (`ABFLOAT`, `MINIFP`, `PO2`…) it is **appended after all the other tags** | stage1.md §3 |
| `S2T1` | quantization granularity — who shares a scale | stage2.md |
| `S2T2` | mixed precision — different widths in one array | stage2.md |
| `S2T3` | mixed formats — different encodings in one array | stage2.md |
| `S2T4` | outlier handling — the outlier gets its own path | stage2.md |
| `S2T5` | bit splitting — decompose the multiply along the bit dimension | stage2.md |
| `S3T1a` / `S3T1b` | into the table: the table holds products / a trained function | stage3.md §T1 |
| `S3T2` | back into arithmetic: a non-analytic form decoded for an ordinary GEMM | stage3.md §T2 |
| `S3T3a`…`f` | off GEMM entirely (a = codebook arithmetic) | stage3.md §T3 |

**Several tags per paper, most-matched first.** The first tag is the contribution; the rest are
mechanisms the design also uses. This differs from `papers.md`'s Type cell in two ways: it can name
types from different stages for one paper (an `S2→S3` path gets both), and its order is a reading,
not the classifier's fixed T4 → T5 → T3 → T1 → T2 priority.

## Proposals

| Paper | Year | Now (`papers.md` Stage · Type) | Proposed, most-matched first | Comment |
|---|---|---|---|---|
| [Mokey](../../survey/papers/Mokey/paper-note.md) ([pdf](../../survey/papers/Mokey/2203.12758.pdf)) | 2022 | `S3` · — | `S3T3a` · `S2T4` | **S3T3a** (codebook arithmetic): centroids forced onto `a^int+b`, so a multiply is a 3-bit index *addition* against the table and the dot product is a histogram of exponent sums; nothing is decoded into a GEMM, so not `S3T2`. Already in stage3.md §T3a. **S2T4**: separate outlier dictionary + pointer list, with outlier products sent to a real MAC; stage2.md counts Mokey in the T4 thread outside `S2`. Granularity is per-tensor, so no `S2T1`. |
| [OliVe](../../survey/papers/OliVe/paper-note.md) ([pdf](../../survey/papers/OliVe/2304.07493.pdf)) | 2023 | `S1→S2` · T4 · T2 · T3 | `S2T4` · `S2T3` · `S1` · `S2T2` · `ABFLOAT` | **S2T4**: the outlier-victim pair is the contribution and stage2.md's T4 anchor. **S2T3**: normal int4/flint4 values and abfloat outliers coexist in one tensor and one decoder — two encodings. **S1**: abfloat is a designed scalar (stage1.md names it `ABFLOAT`), which is the `S1` half of the path. **S2T2** last and weakest: 4-bit and 8-bit are separate configurations; kept because the owner ruled the format multi-mode (Pass 12). |
| [RAELLA](../../survey/papers/RAELLA/paper-note.md) ([pdf](../../survey/papers/RAELLA/2304.07935.pdf)) | 2023 | — · — | `S3T2` · `S2T5` | **S3T2** (back into arithmetic): an analog ReRAM crossbar whose contribution is making the column sum small enough for a low-resolution ADC — stage3.md §T2 point 4 names RAELLA and says a crossbar with an ADC is `T2` because the converter *is* the return. pim.md already gives path `S3→S2`. **S2T5**: adaptive weight slicing and dynamic input slicing decompose the multiply along the bit dimension across cells and cycles. **Note:** choosing these also settles the open Stage cell (`—` → path `S3→S2`, venue `S2`). |
| [Tender](../../survey/papers/Tender/paper-note.md) ([pdf](../../survey/papers/Tender/2406.12930.pdf)) | 2024 | `S2` · T4 | `S2T1` · `S2T4` | **S2T1 first**: channels clustered by magnitude into bands, one scale per band, with power-of-two scale ratios so cross-band accumulation is a shift — *who shares a scale* is the whole design (your Pass 12 note: block quantization). **S2T4 second**: the bands exist to isolate outlier channels, but the outlier gets its own *scale*, not its own path, precision or format. The classifier put T4 first only because it ranks T4 above T1. |
| [Transitive Array](../../survey/papers/TransitiveArray/paper-note.md) ([pdf](../../survey/papers/TransitiveArray/2504.16339.pdf)) | 2025 | `S2→S3` · T5 · T1 · T2 | `S2T5` · `S3T1a` | **S2T5**: bit-slices INT4/INT8 weights into binary rows and reuses prefix partial sums over a Hasse graph — stage2.md's T5 anchor; venue Stage is `S2` (Pass 7). **S3T1a** (table holds products): the 256-entry partial-sum table makes the GEMM a lookup plus one add; stage3.md §T1a lists it. Not `S2T1`: g=128 group scaling is inherited from QServe, not designed. |
| [LUT Tensor Core](../../survey/papers/LUTTensorCore/paper-note.md) ([pdf](../../survey/papers/LUTTensorCore/2408.06003.pdf)) | 2025 | `S2→S3` · T5 · T2 | `S2T5` · `S3T1a` · `S2T2` | **S2T5**: bit-serial weights against a K=4 activation table. **S3T1a**: the table holds precomputed products (with INT8 table quantization); stage3.md §T1a lists it. **S2T2**: mpGEMM is literally a mixed-width GEMM (`W_INT1/2/4` × `A_FP16/FP8/INT8`) in one tensor-core datapath — weaker, because the widths are per operand class, not chosen per layer. |
| [MicroScopiQ](../../survey/papers/MicroScopiQ/paper-note.md) ([pdf](../../survey/papers/MicroScopiQ/2411.05282.pdf)) | 2025 | `S2` · T4 · T1 · T2 | `S2T4` · `S2T3` · `S2T1` · `S2T2` | **S2T4**: outliers at 2× inlier bits, paid for by Hessian-chosen pruning in the same micro-block. **S2T3** (missing from the derived cell): inliers MX-INT, outliers MX-FP — the ablation shows FP beats INT for outliers, so the *format* split is part of the claim. **S2T1**: MX macro-/micro-block scales (B_μ = 8). **S2T2**: the 2× outlier width; it is how T4 is paid for, not a separate mechanism, so last. |
| [Oaken](../../survey/papers/Oaken/paper-note.md) ([pdf](../../survey/papers/Oaken/2503.18599.pdf)) | 2025 | `S2` · T4 · T2 | `S2T4` · `S2T2` | **S2T4**: three magnitude groups per KV token — inliers INT4, large *and* small outliers INT5 in a dense-and-sparse COO path, thresholds profiled offline. **S2T2**: INT4 and INT5 coexist in one tensor. Not `S2T1`: the per-token split is a magnitude classification, not a shared-scale design. |
| [AQB8](../../survey/papers/AQB8/paper-note.md) ([pdf](../../survey/papers/AQB8/10.1145_3695053.3731104.pdf)) | 2025 | `S1→S2` · T1 · T2 | `S2T1` · `S1` · `S2T3` · `S2T2` · `MINIFP` | **S2T1**: one FP32 anchor and one isotropic scale per cluster of ~30–110 BVH nodes, cluster boundaries chosen by a SAH-derived DP — the granularity *is* the design. **S1**: a custom FP14 (1s/8m/5e) for the inverse ray direction, chosen for the distribution of 1/d — the stage1.md element tag `MINIFP`, appended last. **S2T3**: FP32 anchors, INT8 offsets, an FP14 ray and an INT32 origin term meet in one test datapath. **S2T2** weakest: the widths follow from the formats. Off-workload (ray tracing), worth saying in the comment. |
| [Ecco](../../survey/papers/Ecco/paper-note.md) ([pdf](../../survey/papers/Ecco/2505.06901.pdf)) | 2025 | `S3→S2` · — | `S3T2` · `S2T4` | **S3T2** (back into arithmetic): k-means patterns + Huffman in memory, decoded by parallel decoders between L1 and L2 so the SMs compute in FP16 — "remove the decode path and nothing is left"; stage3.md §T2 lists it. **S2T4**: under-budget blocks re-store their largest values as FP8 outliers (pad); stage2.md counts Ecco in the T4 thread outside `S2`. Not `S2T1`: the per-group abs-max scale is ordinary. |

## Decisions — 2026-10-02

Decided by the owner in `reports-002-tmp.md`. **Rule set the same day: a paper tagged `S2T4` carries
no `S2T1`, `S2T2`, `S2T3` or `S1`** — outlier handling already composes those three (stage2.md §T4),
and with `S1` gone its appended element tag goes too (OliVe's `ABFLOAT`). Stage-3 tags are unaffected
(Ecco keeps `S3T2`). Each applied row is written as a `## Stage-type tags` section right after the
note's Tags table; the old Tags table is unchanged.

| Paper | Proposed | Owner's decision | Final tags | Status |
|---|---|---|---|---|
| [Mokey](../../survey/papers/Mokey/paper-note.md) ([pdf](../../survey/papers/Mokey/2203.12758.pdf)) | `S3T3a` · `S2T4` | ☐ approve, put S2T4 before S3T3a. ☐  | `S2T4` · `S3T3a` | applied to the published note and `paper-note.md` |
| [OliVe](../../survey/papers/OliVe/paper-note.md) ([pdf](../../survey/papers/OliVe/2304.07493.pdf)) | `S2T4` · `S2T3` · `S1` · `S2T2` · `ABFLOAT` | ☐ approve, remove S2T3, S2T2, S1. ☐ reject | `S2T4` | applied to the published note and `paper-note.md` |
| [RAELLA](../../survey/papers/RAELLA/paper-note.md) ([pdf](../../survey/papers/RAELLA/2304.07935.pdf)) | `S3T2` · `S2T5` | ☐ approve, PutS2T5 and "S3T2(PIM)". ☐ reject | `S2T5` · `S3T2` · `(PIM)` — `(PIM)` split out 2026-10-02 | applied to the published note and `paper-note.md` |
| [Tender](../../survey/papers/Tender/paper-note.md) ([pdf](../../survey/papers/Tender/2406.12930.pdf)) | `S2T1` · `S2T4` | ☐ approve, remove S2T1 ☐ reject | `S2T4` | applied to the published note and `paper-note.md` |
| [Transitive Array](../../survey/papers/TransitiveArray/paper-note.md) ([pdf](../../survey/papers/TransitiveArray/2504.16339.pdf)) | `S2T5` · `S3T1a` | ☐ approve ☐  | `S2T5` · `S3T1a` | applied to the published note and `paper-note.md` |
| [LUT Tensor Core](../../survey/papers/LUTTensorCore/paper-note.md) ([pdf](../../survey/papers/LUTTensorCore/2408.06003.pdf)) | `S2T5` · `S3T1a` · `S2T2` | ☐ approve, , remove S2T2 ☐  | `S2T5` · `S3T1a` | applied to the published note and `paper-note.md` |
| [Oaken](../../survey/papers/Oaken/paper-note.md) ([pdf](../../survey/papers/Oaken/2503.18599.pdf)) | `S2T4` · `S2T2` | ☐ approve, remove S2T2 ☐  | `S2T4` | applied to the published note and `paper-note.md` |
| [Ecco](../../survey/papers/Ecco/paper-note.md) ([pdf](../../survey/papers/Ecco/2505.06901.pdf)) | `S3T2` · `S2T4` | ☐ approve ☐  | `S3T2` · `S2T4` | applied to the published note and `paper-note.md` |

| [MicroScopiQ](../../survey/papers/MicroScopiQ/paper-note.md) | `S2T4` · `S2T3` · `S2T1` · `S2T2` | approve, `S2T4` | `S2T4` | applied |
| [AQB8](../../survey/papers/AQB8/paper-note.md) | `S2T1` · `S1` · `S2T3` · `S2T2` · `MINIFP` | approve, just `S2T3` · `S2T2` | `S2T3` · `S2T2` | applied |

**Placement, decided the same day:** a **`Stage type` row in the Tags table**, directly under the
`Stage` row (under `Generation` in our working notes, which still carry it), **plus** the
`## Stage-type tags` section after the table, which now holds only the justification and the date.
All ten notes, published and working copies, carry both. **Batch 1 is closed.**

## What changes against the derived cells

- **Order changed:** Tender (T1 before T4). **Added:** MicroScopiQ `S2T3`, AQB8 `S2T3`, RAELLA
  (from nothing), and the `S3` types for the six `S3`-touching papers, which the Stage-2-only Type
  column leaves blank. **Agreed with the derived cell:** Oaken, Transitive Array, LUT Tensor Core and
  OliVe, apart from the added `S1`/`S3` tags.
- **One decision this forces:** RAELLA's tags imply its open Stage (`—` → `S3→S2`, venue `S2`).

## Questions

1. ~~**`S1` has no types.**~~ **Decided 2026-10-02:** bare `S1`, with the stage1.md element tag
   appended after all other tags when it matches well.
2. **Where the tags go in a note.** Planned, once you decide: a new section right after the Tags
   table, leaving the old Tags table untouched —

   ```markdown
   ## Stage-type tags

   `S2T4` · `S2T3` · `S1` · `S2T2` · `ABFLOAT` — most-matched first. <one-line justification>
   ```

   in both the published note and our `paper-note.md`. Say if you would rather have a row in the
   Tags table instead.

## Not done

The other 16 ISCA papers from 2022 on (the 2025–2026 rest). No venue index, `papers.md` or note was
edited.
