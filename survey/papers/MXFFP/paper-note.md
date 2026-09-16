# MXFFP: Microscaling Flexible Floating Point Format for Large-Scale AI Model Acceleration

**Venue / Year:** ISCA 2026, pp. 2505-2519 · **Link:** https://doi.org/10.1109/ISCA66397.2026.00175 · **Reader:** Haoxuan · **Date:** 2026-09-14

## Tags

| | |
|---|---|
| **Level** | `ARCH` |
| **Q-oriented** | `Q-ORIENTED` |
| **Data type** | `MX` `FP4` `FP8` `ADAPTIVE` `MIXED` |
| **Generation** | `G2` |
| **Optimization** | microscaling · flexible exponent/mantissa split · sub-block configuration · 1-bit config selector · bit mapper · quadratic-weighted counting rule · decoupled scale/format granularity · tensor core · PTQ · calibration-free |

## 1. One-line summary

Keeps OCP MX exactly as it is — same element width, same 8-bit E8M0 shared exponent — and adds
**one configuration bit** that switches the element between **two exponent/mantissa presets**
(`E1M2` or `E2M1` at 4 bits), chosen **offline by MSE for weights** and at runtime for
activations by a **quadratically-weighted counting rule** over relative exponents, with both
encodings collapsed back into a single internal **E2M2** by a mux array so the arithmetic core
needs only **one extra mantissa bit** — buying **2-5× lower perplexity than MXFP4** (10.23 vs
30.98 on Llama3-8B, against BF16's 5.50) for **+22.26% threadgroup area** and **0.03
bits/element**, and, because the sub-block sets *format* granularity while the block still sets
*scale* granularity, letting the block grow to 256 for **4× less metadata**.

## 2. Data type

**Formats.** `W4A4` — "all tensors involved in MMA operations" are converted. Also 6- and 8-bit (`W6A6` / `W8A8`).

**Element encoding.** 1 sign + **E1M*x* or E2M*x***, selected per block or sub-block. At 4 bits: **E1M2 / E2M1**. At 8 bits: **E1M6 / E2M5** — *not* OCP's E5M2/E4M3.

**Scale.** 8-bit **E8M0** shared exponent, one per block of 32-256. Unchanged from OCP MX.

**Two granularities, set independently.** Scale granularity = **block** (32/64/128/256); format granularity = **sub-block** (4/8/16/32). This decoupling is the paper's own framing of its contribution.

**Config metadata.** **1 bit** per block or sub-block, packed 8-to-a-byte into a "configuration set" for byte addressability. Block set: 9 B / 256 elements. Large block: **2 B / 256 elements**.

**Effective bitwidth.** 4.25 (MXFP4) → **4.28** at block 32 → **4.50** at sub-block 4 (best accuracy) → **4.06** at block 256 / sub-block 32 (the 4×-metadata setting).

**Outliers.** **None.** No outlier path, no second precision, no victim, no sparse list, no permutation metadata — the word appears only in background and the bibliography. The shared exponent is the whole answer, inherited.

**Escape hatch.** Accumulators **FP16/BF16** (named once, never costed); **non-GEMM ops stay on the BF16 path** — the stated reason end-to-end is 2.08× against GEMM's 2.7×; the internal compute format is **E2M2 (5 bits)**, wider than either stored encoding.

**Retraining.** **PTQ and calibration-free** — weights converted offline by trying both presets, activations by a hardware counting rule. `QAT` 0 hits, `retrain` 0, `calibrat` 0.

## 3. Optimization

**The config bit.** MXFFP = MXFP + 1 bit per block (or sub-block) selecting between exactly **two** presets. The four-way space (E0M3/E1M2/E2M1/E3M0) that §III-B motivates with is **not implemented**; §VII-D defends two at **97.2%** coverage of lowest-MSE selections, and offers E0/E2 or E2/E3 as alternative pairs.

**Weights: exhaustive, offline.** Known in advance, so each block is quantized under both presets and the lower-MSE one wins. With two presets the "search" is two evaluations. No calibration set anywhere.

**Activations: a counting rule in silicon.** Take each element's exponent, subtract the block max to get relative exponent `E_i^r ≤ 0`, then `Config = E1Mx if count(E_i^r = 0)² > count(E_i^r ∈ {−2,−3})`. The square is deliberate — `E_i^r = 0` elements carry the largest magnitudes and dominate fidelity. Table I is the justification: at 0, E1M2 gives `2¹×1.xx` against E2M1's `2²×1.x`; at −2/−3 E2M1 wins; at −1 and −4 they tie.

**Shared exponent follows the config, not the other way round.** `E_b^shared = E_b^MAX − E_element^MAX`, with `E_element^MAX` = 1 for E1M*x*, 2 for E2M*x*. When sub-blocks inside a large block disagree, **one** exponent is stored computed as if all were E2M*x*, and E1M*x* sub-blocks subtract one on use. That is the entire cost of letting sub-blocks disagree.

**Bit mapper — the datapath trick.** A compact mux array reinterprets each 4-bit word by its config bit into a single internal **E2M2**: E1M2 routes its exponent bit low and both mantissa bits through (`S 0 E MM`); E2M1 forwards both exponent bits and appends a zero (`S E E M 0`). The FP4 core then needs **one additional mantissa bit** in the significand path plus a widened normalizer; exponent biasing and range handling are unchanged. **Unify by widening, not by composing.**

**Cost.** Per threadgroup: 16 bit mappers, +1 mantissa bit in 4 dot-product paths, 1 converter extended with Subtractor + Counter + Config Selector, 2 B + 2 B of registers → **+22.26% area / +21.4% power**, or ~12% power with per-configuration gating.

## 4. Results

| | |
|---|---|
| Baseline | MXFP (OCP-compliant conversion) at matched bit-width; BF16. Against prior work: M-ANT, BitMoD (**W4A8**), MicroScopiQ, MX+ |
| Models / datasets | 7 LLMs (Llama3-8B, OPT-6.7B, Qwen2.5-14B, Vicuna-13B, Mistral-7B, Deepseek-7B-chat…) on WikiText-2 + ARC-e/ARC-c/Lambada; ViT-base/large |
| Accuracy delta | 4-bit PPL **10.23 vs MXFP4's 30.98** on Llama3-8B (BF16 5.50) — **still 1.86× worse than BF16**. 8-bit: 5.50 vs 5.55, i.e. near-parity. Zero-shot +16-29% over MXFP4 but **5-12% below BF16**. Sub-block 4 vs prior work: **6.75 on Llama3-8B — loses to BitMoD's 6.54**; best on Mistral and Deepseek |
| Speedup | **2.7× GEMM and 2.08× end-to-end vs BF16 — these are MXFP's numbers; MXFFP's claim is that it does not lose them** ("no measurable latency overhead"). Prefill only; **decode is never evaluated** |
| Energy / area | Energy 0.35× of BF16 (again MXFP's). Area **+22.26%** / power **+21.4%** per threadgroup; 0.038% of a 750 mm² die |
| Technology node | FreePDK **45 nm** (Design Compiler) for area/power; Accel-Sim configured from an RTX 5090 + AccelWattch for performance/energy |
| Evidence level | **Three, not to be pooled:** PyTorch PTQ for accuracy; **simulator** (Accel-Sim + CUTLASS traces + AccelWattch) for speed/energy; **post-synthesis 45 nm** of "a representative 4-bit datapath", not a Tensor Core. No silicon |
| **Is the comparison fair?** | Iso-format-family and iso-block-size vs MXFP; PTQ both sides. **Not iso-node** (FreePDK 45 nm scaled onto a 750 mm² 4 nm-class die); Fig. 22 **not iso-setting** (BitMoD W4A8 vs everyone else's W4A4; MicroScopiQ shown off its W4A16 headline). **Not to quote:** 2-5× PPL (ratio of two broken numbers); 2.7× / 2.08× / 0.35× are **MXFP's**, not MXFFP's |

## 5. Comment

## 6. Claude notes

*Suggestions from the reading agent. **Strip this section before copying into
`QuantArchSurvey/venues/ISCA/notes/`.***

- **Read depth.** Full close read of §I-§IX. **One unresolved internal discrepancy, flagged and not papered over:** §VII-A states that at sub-block 4 the average perplexity degradation is **0.98**, while Fig. 22 at the same setting and same three models gives **1.25 / 0.02 / 0.12**, mean **0.46**. One of the two measures something else. **Verify before citing either.** Also: Fig. 22's bar values are not printed in prose — I recovered them by x-coordinate and checked the assignment against the paper's own stated 0.36 MicroScopiQ delta, which recomputes to 0.367. Repeat that check if you re-derive them.
- **`ADAPTIVE` is right here — and note it is the opposite call to the one I made on AQuant today.** TAXONOMY defines `ADAPTIVE` as the *numeric type itself* being a data-dependent design variable. MXFFP genuinely changes the **type** per block (E1M2 vs E2M1); AQuant only changes **which fixed type** each element gets, which is what `MIXED` says. Worth keeping the pair as the worked example of where that line falls. The venue README's line-122 amendment should stand.
- **On `MIXED` (human ruling 2026-09-14, applied).** Tagged `MIXED`. Worth keeping in mind when reading the multi-precision-datapath thread: every MXFFP element is the same *width*, and what coexists is two **encodings** of that width, not two precisions — so it is a different sense of "mixed" from BitFusion/RaPiD/UniCore.
- **The best cross-paper output: this paper adds an axis the survey does not have.** The granularity spine measures **one** granularity — the scale's: per-layer (BitFusion, OLAccel) → per-region (DRQ) → per-channel (Tender) → per-group (Oaken, MicroScopiQ) → per-head (P3-LLM) → per-token (LightNobel) → per-rank (SingularBit). **MXFFP sets scale granularity and format granularity independently**, and says so itself in §VIII. That is the cleanest available statement of the idea and I would give it a paragraph.
- **A load-bearing negative result for the outlier section.** The "outlier currency" list should gain a **null row**: MXFFP pays *nothing*, has no outlier concept at all, and still reaches 6.75 PPL on Llama3-8B W4A4 where MicroScopiQ reaches 6.80. Whatever a shared exponent plus a movable field boundary is doing, at this granularity it does most of what an outlier mechanism does. That is worth saying out loud.
- **It sharpens the multi-precision-datapath thread by *not* being in it.** BitFusion (spatial) → RaPiD (split pipelines) → SamsungNPU/EVA (temporal) → XtraMAC (DSP bit-space) → UniCore (adder slices) all answer *how do I span several bit-widths*. MXFFP has **one** bit-width and two encodings, and answers a different question by collapsing both into E2M2 before arithmetic. **"Unify by widening, not by composing"** is a fifth strategy.
- **MicroScopiQ pairing.** Same base format, opposite theory of what MXFP gets wrong: MicroScopiQ says *the block contains values that do not belong*; MXFFP says *the block's field split is in the wrong place*. EBW 2.36 vs 4.28. If you write one paragraph on microscaling, that contrast is it.
- **Two numbers I would exclude.** (i) **"2-5× perplexity reduction"** — a ratio between two bad numbers (MXFP4 is at 30.98-88.81); quote absolute perplexities or the sub-block-4 result. OPT-6.7B is 5.44×, outside the stated band. (ii) **The 0.038%-of-die figure**, which crosses nodes; +22.26% / +21.4% at threadgroup level are the defensible ones. Also note §V-C calls the dot-product extension "negligible" and §VI-D measures it at **+26.4%** — use the number.
- **Never quote the accuracy claim and the 4×-metadata claim in one sentence.** They are at different operating points (block 32 vs block 256), and **at block 32 MXFFP costs *more* metadata than MXFP** (9 B vs 8 B per 256 elements).
- **§5 material, if you want it.** `G2` in 2026, and confidently: it designs a numeric type and none of the three G3 threads is present. The ViT results (§VII-C) support reading it as a format paper rather than an LLM paper, which is the argument for G2 over G3. Also worth one line: the motivation's oracle is a **four-way exhaustive MSE search** reaching 8.5/9.0 PPL at block 64/256, while the shipped two-way heuristic reaches 13.5/24.3 — Fig. 8's numbers are not MXFFP's.
