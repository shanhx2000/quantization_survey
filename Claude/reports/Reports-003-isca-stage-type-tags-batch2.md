# Reports-003 — Stage × Type tags for ISCA papers, batch 2 (2026-10-02) — closed

**Input:** the remaining 16 ISCA papers from 2022 on (FATE, LightNobel and Phi from 2025, and the
thirteen 2026 papers), at upstream `main` 8922a85. **Method:** as
[Reports-002](Reports-002-isca-stage-type-tags.md) — each published note's Tags, §1 and §2 against
the stage pages and `papers.md`'s derived cells. The extracted text was opened once, for SingularBit,
to confirm its tensor core is a bit-serial LUT design (it is, p. 8). **Nothing is applied yet**;
decide in [`reports-003-tmp.md`](reports-003-tmp.md).

**Conventions carried over from batch 1:**
- **`S2T4` excludes** `S2T1`, `S2T2`, `S2T3` and `S1`. Stage-3 tags are unaffected.
- **`S1` is bare**, with its stage1.md element tag(s) appended after all other tags.
- **A substrate suffix** goes on a Stage-3 tag when the substrate is what puts it there: `S3T2(PIM)` (RAELLA), `S3T3f(SNN)` here.
- **Lean lists**: in batch 1 you cut weak secondaries every time, so weak matches are named in the comment rather than proposed.

Tag legend: [Reports-002 § The tag](Reports-002-isca-stage-type-tags.md#the-tag-in-one-paragraph).

## Proposals

| Paper | Year | Now (`papers.md` Stage · Type) | Proposed, most-matched first | Comment |
|---|---|---|---|---|
| [FATE](../../survey/papers/FATE/paper-note.md) ([pdf](../../survey/papers/FATE/10.1145_3695053.3731031.pdf)) | 2025 | `S2` · T2 | `S2T2` | Every hypervector dimension gets its own type — INT8 on DSPs, INT4/ternary/binary as FPGA logic, `INT0` pruned — mixed inside one vector and realigned by a fixed shift into one adder tree: different widths in one array, placed on different resources. Not `S2T1` (no scale is stored; "the type is the scale"). Not `S3`: the FPGA LUTs evaluate shifted low-bit products, not a trained function. |
| [LightNobel](../../survey/papers/LightNobel/paper-note.md) ([pdf](../../survey/papers/LightNobel/2505.05893.pdf)) | 2025 | `S2` · T4 · T1 · T2 | `S2T4` | INT4/INT8 inliers with per-token runtime scales and INT16 outliers by runtime top-k with adaptive k. The outlier path is the mechanism; per-token scale and the INT4/INT8/INT16 widths are part of it, so by the `S2T4` rule nothing else is carried. |
| [Phi](../../survey/papers/Phi/paper-note.md) ([pdf](../../survey/papers/Phi/2505.10909.pdf)) | 2025 | — · — | `S3T1a` · `S3T3f(SNN)` | **S3T1a**: k-means binary patterns whose products with the weights are precomputed offline, so a pattern index at runtime is a memory read — the table holds products. **S3T3f(SNN)**: stage3.md reserves T3f for spiking; the suffix follows RAELLA's `(PIM)`. **Caveat:** snn.md leaves the Stage axis open for spiking; tagging Phi answers that question for it. Reject to keep it untagged. |
| [FlexQ-NDP](../../survey/papers/NDPLowBitFP/paper-note.md) ([pdf](../../survey/papers/NDPLowBitFP/506501b383.pdf)) | 2026 | — · — | `S2T1` | The paper is about the cost of group-wise scaling on NDP — 75% of it DRAM row changes — fixed by a scale-value interleaved layout and dequantization hiding. *Who shares a scale, and where the scales live*, is the whole subject. The multi-precision PU (an FP32 multiplier split into 12- and 6-bit parts) would be a weak `S2T2`; left out. pim.md already gives `S2`. Add `(PIM)` if you want the substrate marked as on RAELLA. |
| [EVA](../../survey/papers/EVA/paper-note.md) ([pdf](../../survey/papers/EVA/506501b351.pdf)) | 2026 | `S3` · — | `S3T3a` | Dot products against the codebook itself (`O = XB`, all 256 input-centroid products), then structured lookups — the multiply happens against the table, never decoded into a GEMM. stage3.md §T3a lists it. The INT8 PE composed four times into FP16 is a substrate detail, not a contribution; left out. |
| [LoKA](../../survey/papers/LoKA/paper-note.md) ([pdf](../../survey/papers/LoKA/506501b368.pdf)) | 2026 | `S2` · T2 | `S2T2` · `S2T1` | **S2T2**: which layers are safe in FP8 and which stay TF32/BF16 is decided per layer by learned-distribution error — mixed precision across the model. **S2T1**: Dispatch picks tensorwise / rowwise / blockwise scaling per operator and per direction, and BlockNorm fixes a 256-element block. Production GPU software, no new hardware. |
| [MXFFP](../../survey/papers/MXFFP/paper-note.md) ([pdf](../../survey/papers/MXFFP/506501c505.pdf)) | 2026 | `S1→S2` · T3 · T1 · T2 | `S2T3` · `S2T1` · `S1` · `FLEXFP` | **S2T3**: one bit per block or sub-block selects E1M2 or E2M1, so two encodings coexist under one MX scale. **S2T1**: the paper's own framing is decoupling *format* granularity (sub-block) from *scale* granularity (block), which lets the block grow to 256. **S1** · `FLEXFP`: the element's e/m split is a runtime-selected variable (stage1.md `FLEXFP`). No `S2T2` — every element is the same width. |
| [OASIS](../../survey/papers/OASIS/paper-note.md) ([pdf](../../survey/papers/OASIS/506501a307.pdf)) | 2026 | `S3` · — | `S2T4` · `S3T3a` | **S3T3a**: both operands to learned 4-bit codebooks, so the table is their Cartesian product — GEMM becomes count indices and take a weighted sum of 256 static entries; stage3.md §T3a. **S2T4**: the top and bottom 0.5% of activations go to an FP16 compensation branch, detected by twin tournament trees — "Outlier-Aware" is in the title. **Order follows your Mokey ruling** (`S2T4` before `S3T3a`); swap if OASIS should lead with the table. |
| [Omni-LUT](../../survey/papers/Omni-LUT/paper-note.md) ([pdf](../../survey/papers/Omni-LUT/506501a322.pdf)) | 2026 | `S2→S3` · T5 · T1 · T2 | `S2T5` · `S3T1a` · `S2T1` | **S2T5**: weights and KV as ±1 bit-planes (BCQ), cost linear in bit-planes. **S3T1a**: Q or the attention scores build a table of partial sums that the bit-planes index — the same pair as LUT Tensor Core. **S2T1** kept, unlike LUT Tensor Core: folding per-channel K and per-token V scales *into* table generation is a stated contribution — the paper's claim is outliers handled by granularity, not isolation. No `S2T2` for the AS-Bit extra bit-planes; weak. |
| [P3-LLM](../../survey/papers/P3-LLM/paper-note.md) ([pdf](../../survey/papers/P3-LLM/506501a604.pdf)) | 2026 | — · — | `S2T3` · `S1` · `S2T1` · `MINIFP` | **S2T3**: a different format per operand — BitMoD FP4 weights, FP8-E4M3 activations, INT4-Asym KV, FP8-S0E4M4 scores — with PIM units built for exactly those. **S1** · `MINIFP`: the unsigned FP8-S0E4M4 score format is derived in the paper and is "the point" of `W4A8KV4P8`. **S2T1**: per-group-128 weights, per-token activations, per-head KV, and a score format with no scale at all. Key smoothing is a scale migration, not an outlier path, so no `S2T4`. pim.md gives `S2`; add `(PIM)` if wanted. |
| [SingularBit](../../survey/papers/SingularBit/paper-note.md) ([pdf](../../survey/papers/SingularBit/506501b001.pdf)) | 2026 | `S2` · T2 | `S2T2` · `S2T5` · `S3T1a` | **S2T2**: precision allocated by rank — 4/3/2/1-bit regions inside one matmul — is the contribution. **S2T5** · **S3T1a**: verified in the paper (p. 8): the SingularBit Tensor Core does "bit-serial mixed-precision matrix multiplication using lookup", with FP16 partial sums over four input channels selected by weight bits, built on LUT Tensor Core. The implementation, ranked after the allocation. |
| [UniCore](../../survey/papers/UniCore/paper-note.md) ([pdf](../../survey/papers/UniCore/506501c520.pdf)) | 2026 | `S1→S2` · T3 · T2 | `S2T2` · `S1` · `FLEXFP` · `MITCH` | **S2T2**: a composable FPMA built from uniform adder slices, so fusing to higher precision scales linearly — the Bit Fusion problem (stage2.md's T2 *fuse one PE*) solved for floats, evaluated W4A4 to W16A16. **S1** · `FLEXFP` `MITCH`: DynFP adapts the e/m allocation (`FLEXFP`), and the multiply is Mitchell's log approximation (`MITCH`). Not `S2T3`, although stage2.md lists it there: it is FP throughout — the note says pure integer formats have no logarithm to read off. |
| [XtraMAC](../../survey/papers/XtraMAC/paper-note.md) ([pdf](../../survey/papers/XtraMAC/506501c536.pdf)) | 2026 | `S1→S2` · — | `S2T3` · `S2T2` | **S2T3**: every format, INT×FP included, decomposed into one shared integer mantissa product, with an integer given a logical exponent of zero — different encodings in one MAC. **S2T2**: per-datatype multi-lane packing into the DSP keeps II = 1 at every width. **No `S1`**: it contributes no format ("executes existing formats"), so the derived `S1→S2` path is not supported. |
| [AQuant](../../survey/papers/AQuant/paper-note.md) ([pdf](../../survey/papers/AQuant/506501b417.pdf)) | 2026 | `S1→S2` · T4 · T1 · T2 | `S2T1` · `S2T2` | **S2T1**: tokens are grouped around a base (the middle of every 18) and only the delta is quantized — who shares a reference is the design. **S2T2**: per-token top-25% of each delta to INT4, the rest INT2, against INT8 bases. **No `S2T4`**: the derived T4 comes from one sentence on out-of-range tokens, whose fallback is unreported; the outlier is subtracted into the base, not given a path. **No `S1`**: plain INT; the H.265 reuse is a scalar quantizer. |
| [ENEC](../../survey/papers/ENEC/paper-note.md) ([pdf](../../survey/papers/ENEC/506501b319.pdf)) | 2026 | `S2` · T5 · T2 | `S3T2` | Lossless: only the exponent field is coded — frequency-rank remap plus a two-level fixed-length pack — and the vector units expand every weight to full BF16 before the Cube unit multiplies. A stored form that cannot be read by place value, decoded for an ordinary GEMM: stage3.md §T2, the compression chapter (the TunstallDec precedent: lossless and still T2). **This changes its Stage** (`S2` → path `S3→S2`); reject to keep it Stage 2. The derived `T5` is a keyword match on bit-packing, not bit splitting of a multiply. |
| [ELSA](../../survey/papers/ELSA/paper-note.md) ([pdf](../../survey/papers/ELSA/506501c550.pdf)) | 2026 | — · — | `S3T3f(SNN)` | A 4-bit quantized ANN run as an exactly equivalent spiking network: activations become ternary unary trains over T ≤ 32 steps and every MAC an add into a 12-bit membrane — no analytic GEMM in steady state. T3f is stage3.md's reserved spiking slot. The time-step count as a per-input precision knob would be a weak `S2T2`; left out. **Same caveat as Phi** on the open SNN question. |

## Decisions — 2026-10-02

From `reports-003-tmp.md`. Applied to the published note and our `paper-note.md` as a `Stage type`
row under the Stage row plus a `## Stage-type tags` section with the reason and date, as in batch 1.

| Paper | Proposed | Owner's decision | Final tags |
|---|---|---|---|
| [FATE](../../survey/papers/FATE/paper-note.md) ([pdf](../../survey/papers/FATE/10.1145_3695053.3731031.pdf)) | `S2T2` | approve | `S2T2` |
| [LightNobel](../../survey/papers/LightNobel/paper-note.md) ([pdf](../../survey/papers/LightNobel/2505.05893.pdf)) | `S2T4` | approve | `S2T4` |
| [Phi](../../survey/papers/Phi/paper-note.md) ([pdf](../../survey/papers/Phi/2505.10909.pdf)) | `S3T1a` · `S3T3f(SNN)` | approve; Stage `—` → `S3` | `S3T1a` · `S3T3f(SNN)` |
| [FlexQ-NDP](../../survey/papers/NDPLowBitFP/paper-note.md) ([pdf](../../survey/papers/NDPLowBitFP/506501b383.pdf)) | `S2T1` | reject → `S2T2`; `(PIM)` per Q1; Stage `—` → `S2` | `S2T2` · `(PIM)` |
| [EVA](../../survey/papers/EVA/paper-note.md) ([pdf](../../survey/papers/EVA/506501b351.pdf)) | `S3T3a` | approve | `S3T3a` |
| [MXFFP](../../survey/papers/MXFFP/paper-note.md) ([pdf](../../survey/papers/MXFFP/506501c505.pdf)) | `S2T3` · `S2T1` · `S1` · `FLEXFP` | reject → `S2T1` · `S2T2` | `S2T1` · `S2T2` |
| [OASIS](../../survey/papers/OASIS/paper-note.md) ([pdf](../../survey/papers/OASIS/506501a307.pdf)) | `S2T4` · `S3T3a` | approve | `S2T4` · `S3T3a` |
| [Omni-LUT](../../survey/papers/Omni-LUT/paper-note.md) ([pdf](../../survey/papers/Omni-LUT/506501a322.pdf)) | `S2T5` · `S3T1a` · `S2T1` | reject → `S3T1a` · `S2T5` | `S3T1a` · `S2T5` |
| [XtraMAC](../../survey/papers/XtraMAC/paper-note.md) ([pdf](../../survey/papers/XtraMAC/506501c536.pdf)) | `S2T3` · `S2T2` | reject → `S1` | `S1` |
| [AQuant](../../survey/papers/AQuant/paper-note.md) ([pdf](../../survey/papers/AQuant/506501b417.pdf)) | `S2T1` · `S2T2` | reject → `S2T5` · `S2T2` · `S2T1` | `S2T5` · `S2T2` · `S2T1` |
| [ELSA](../../survey/papers/ELSA/paper-note.md) ([pdf](../../survey/papers/ELSA/506501c550.pdf)) | `S3T3f(SNN)` | "more proper to be removed from quantization" → `legacy/`, listed in snn.md *Screened out* | — (removed from the corpus) |

**Answers to the questions.** (1) PIM papers carry **one `(PIM)` tag after the others**, not a
suffix on each tag — applied to FlexQ-NDP. RAELLA (batch 1) still reads `S3T2(PIM)`; say if it
should become `S2T5` · `S3T2` · `(PIM)`. (2) **Yes** to the implied Stage changes — applied for
FlexQ-NDP, P3-LLM (`—` → `S2`) and Phi (`—` → `S3`); ENEC waits on its own row.

**Carried through on the shared side** (ISCA Pass 13): ELSA excluded in `survey/gen/legacy.py` and
moved to `legacy/ISCA/`; `papers.md` row, name list and counts; `snn.md`; a path `OVERRIDE` for
FlexQ-NDP and P3-LLM (`S2`, not the PIM-substrate `S3→S2`); a stage-2 `PRIMARY` for FlexQ-NDP
(`MixedPrec`, matching `S2T2`); Phi listed in stage3.md §T3f; FlexQ-NDP in stage2.md §T2 and
P3-LLM in §T4 (the classifier's primary, pending its tag). `5-check.py`: 189 problems against 192
on upstream `main` 8922a85; the one check whose text moved — snn.md's corpus count against
`plat_snn` — was already off by one upstream.

**Second round, same day** (from `reports-003-tmp.md`):

| Paper | Proposed | Owner's decision | Final tags |
|---|---|---|---|
| LoKA | `S2T2` · `S2T1` | "reject, just S2T2?" — read as `S2T2` | `S2T2` |
| P3-LLM | `S2T3` · `S1` · `S2T1` · `MINIFP` | approve, remove `S1`, add `(PIM)` | `S2T3` · `S2T1` · `(PIM)` |
| SingularBit | `S2T2` · `S2T5` · `S3T1a` | approve | `S2T2` · `S2T5` · `S3T1a` |
| UniCore | `S2T2` · `S1` · `FLEXFP` · `MITCH` | approve, `S1` to the comment | `S2T2` (DynFP and Mitchell named in the justification) |

`PRIMARY` entries for P3-LLM (`MixedType`) and UniCore (`MixedPrec`) keep the derived Type in
line; P3-LLM moved from stage2.md §T4 to §T3 and UniCore from §T3 to §T2. `5-check.py`: 189.

**ENEC, decided last:** `S2T2` · `S2T1`, with `S2T5` named in the justification only. The first
proposal, `S3T2`, was withdrawn: the re-encoded exponent `y = (2ⁿ − x + b) mod 2ⁿ` is **analytic** —
recoverable by formula with the per-tensor pivot `b`, like a zero-point — and the frequency table
that would have made it non-analytic is the paper's *basic* design, which the optimized design
replaces (§V-C). Losslessness does not rest on a narrow range: Eq. 1 sets `n` from the tensor's
measured min and max exponent, so every occurring exponent is covered, and a group holding a large
code is stored at `n` bits with its high bits in a side buffer. ENEC's Stage stays `S2`; a `PRIMARY`
entry files it `MixedPrec` and its stage2.md row moved from §T5 to §T2. `5-check.py`: 189.

**Batch 2 is closed.** All 25 ISCA rows from 2022 on carry Stage-type tags.

**Not touched, and worth a look:** ELSA is still named in `writings/taxonomy.md` (§3.1, §4.2, §7)
and in `latex/figures/taxonomy.tex` (§3.1, §4.2 and the workloads leaf).

## Decisions these tags would also make

Three proposals settle something outside the Stage-type row, so approving them is a ruling, not
just a tag:

| Paper | Implied change | Where |
|---|---|---|
| ENEC | Stage `S2` → path `S3→S2` | venue index, `papers.md`, stage2.md → stage3.md §T2 |
| Phi, ELSA | spiking records placed on the Stage axis | `snn.md`'s open question 1; stage3.md §T3f stops being empty |
| FlexQ-NDP, P3-LLM | Stage `—` → `S2` (already pim.md's value) | venue index, `papers.md` — the open item from ISCA Pass 12 |

None of those is applied by the Stage-type row alone; say if you want them carried through.

## Not done

No note, venue index or `papers.md` was edited. Placement once decided: as in batch 1 — a
`Stage type` row under the Stage row of the Tags table, plus a `## Stage-type tags` section with the
justification and the date, in both the published note and our `paper-note.md`.
