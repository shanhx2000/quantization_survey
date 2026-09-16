# AQuant: Repurposing CODEC for VLM Acceleration via Adaptive Quantization

**Venue / Year:** ISCA 2026, pp. 1417-1431 · **Link:** https://doi.org/10.1109/ISCA66397.2026.00106 · **Reader:** Haoxuan · **Date:** 2026-09-14

## Tags

| | |
|---|---|
| **Level** | `ALGO+ARCH` |
| **Q-oriented** | `Q-ORIENTED` |
| **Data type** | `INT2` `INT4` `INT8` `INT16` `MIXED` |
| **Generation** | `G3` |
| **Optimization** | CODEC reuse · base-delta quantization · visual-token similarity · exponent-only L1 distance · per-row top-k mixed precision · workload-balanced dual MAC arrays · activation-only · KV cache · VLM |

## 1. One-line summary

Rewrites each visual token as **base + delta** — the base picked by positional stride from the
tokens themselves — and quantizes only the deltas, **per-token top-25% to INT4 and the rest to
INT2** against INT8 bases and **INT16 weights**, finding each token's base with an
**exponent-only L1 distance** (`sign ‖ 2^exp`, a 10-bit integer) so the whole
similarity-detect-and-quantize path lands on the H.265 encoder's *existing* motion-estimation
subtract-and-abs trees and residual quantizer sitting idle in the SoC: **−0.7% accuracy over 3
VLMs / 14 datasets, 2.1× over a measured Jetson AGX Xavier** (6.9× over the same GPU shrunk to
AQuant's compute budget), the CODEC reuse itself worth **1.4×**.

## 2. Data type

**Formats.** **`W16 A2/A4 + A8 bases`** — activations only. Weights are **never quantized** (INT2×INT16 and INT4×INT16 MACs); the paper calls itself orthogonal to weight quantization.

**Effective activation bitwidth.** `0.25×4 + 0.75×2 + 0.074×8 ≈ 3.1 bits` — but against **16-bit weights**, so the product is not a low-bit GEMM in this corpus's usual sense.

**Granularity.** **Never stated.** The quantizer is the CODEC's affine `Clamp((Res/Factor) + Offset) >> b` with an FP scaling-factor input; no per-tensor / per-token / per-group is given anywhere. The only per-something is the *precision assignment*, which is per-row (per-token top-`p`).

**Precision assignment.** Top **`p` = 25%** of each delta vector by magnitude → INT4, remaining 75% → INT2, recorded as a bitmask. Per-*row* is a **load-balancing** choice, not an accuracy one — it keeps the two MAC arrays in lockstep.

**Base tokens.** `M` bases chosen **positionally, not by content**: the middle token of every `F = 18` consecutive tokens. No clustering, no k-means, no importance measure. **7.4%** of tokens stay INT8.

**Accumulator.** Not reported for the MAC arrays. Known only: the reused ME tree accumulates 64 INT8 in 16 bits; the reconstruction buffers hold INT16.

**Outliers.** One sentence: tokens with exponents outside [0, 8] bypass similarity detection and go to "higher precision". **The fallback precision, its frequency and its cost are all unreported.**

**Escape hatches.** INT16 weights; 7.4% INT8 bases; **all non-linear ops in FP** — GELU/Softmax/LayerNorm consume activations reconstructed and dequantized after every linear layer, priced at 5.1% of latency.

**Retraining.** **PTQ, none required** — evaluated in PyTorch on stock checkpoints, no fine-tuning.

## 3. Optimization

**Base + delta.** `T ≈ B + δ` with `B` a base token from the sequence itself. The argument is that the ViT encoder is near-homomorphic from pixels to tokens, so spatially/temporally similar pixels give similar tokens and `δ` has a much narrower distribution than `T` — narrow enough for 2-4 bits. The outlier is **subtracted away rather than encoded**, which is what distinguishes this from every outlier scheme in the corpus.

**Exponent-only similarity — the real trick.** Instead of an FP32 L1 distance, AQuant compares `sign(T)·2^Ē` using only the IEEE-754 exponent field. Each operand becomes `sign ‖ (1 << exponent)`, a **10-bit integer**, and the distance becomes an integer subtract-and-abs reduction — precisely what the H.265 motion-estimation PE already does on INT8 pixels. This is what makes the CODEC reuse possible at all; without it the similarity search needs FP32 hardware costing 1.269 mm² / 422.7 mW.

**What is actually reused.** The *arithmetic skeleton* only: the 64-wide subtract-and-abs trees, the comparator reduction trees, and one multiplier-adder-shifter-clamper chain. Modified or new: the subtractor front-end (exponent extract, shift, sign concat, INT10 in), reconfigurable 4×4 PE partitioning, a reconfigurable comparator tree, the similar-token table, a mantissa clamp 23→16, an fp-to-int unit, a QuickSelect top-k unit, and bitmask generation. **Entirely new:** both MAC arrays, the accumulation engine, the reconstruction engine, all on-chip buffers.

**Reconstruction.** `W_q T = W_q B + W_q δ`. `W_q B` is computed once per base at INT8 and then *selected*, not recomputed, for every token sharing it; a dedicated engine (16 KB base / 8 KB delta / 16 KB recovery, INT16) walks the similar-token table and adds the two.

**Decode.** The only mechanism helping the memory-bound phase: after KV projection the KV cache is **re-quantized rather than written back reconstructed**, stored compressed off-chip, and reconstructed on demand — trading compute for bandwidth.

## 4. Results

| | |
|---|---|
| Baseline | Jetson AGX Xavier (measured, and analytically rescaled); hypothetical mixed-precision GPU; VisPruner; **OliVe, LLM.265, CMC — all re-implemented by the authors as cycle-accurate simulators, not quoted** |
| Models / datasets | LLaVA, VideoLLaVA, Qwen2.5-VL-72B across 14 datasets; `p` = 25%, `F` = 18 |
| Accuracy delta | **−0.7%** average. Pruning the bottom 75% instead of keeping INT2 costs **−23%** — the low-magnitude deltas carry real signal. Fast motion −0.83%, low-similarity bucket −0.92% |
| Speedup | **2.1× measured Xavier**; 6.9× rescaled GPU; 2.2× idealised mixed-precision GPU; 2.5× OliVe, 4.6× LLM.265, 2.8× CMC, 2.8× VisPruner. Composed: 8.3× with VisPruner. **GPU-AQuant is 0.843× — the algorithm without the hardware is *slower*** |
| Energy / area | **1.858 mm²**, **510.5 mW** (sums computed from Table III; the paper prints no total). Energy efficiency 2.2× vs measured Xavier, 7.2× vs rescaled. Decomposition: algorithm 3.3× → exponent detection 1.6× → CODEC reuse 1.4× |
| Technology node | 28 nm, 500 MHz; LPDDR4x 32 GB / 136.5 GB/s matched to Xavier |
| Evidence level | **Five kinds in one bar chart:** measured PyTorch-on-Xavier → analytically rescaled GPU → author-reproduced cycle-accurate simulators → AQuant's own cycle-level simulator + Ramulator + CACTI → post-synthesis 28 nm + modified OpenASIC CODEC IP |
| **Is the comparison fair?** | **Not iso-node** (28 nm synthesis vs a shipping edge GPU, never normalised); baselines re-simulated rather than quoted, but no area match stated for CMC/LLM.265/OliVe. **Do not quote 6.9× as a Xavier speedup** — that is an analytically shrunk GPU; measured Xavier is **2.1×**, an idealised mixed-precision GPU 2.2×. The area argument charges nothing for the CODEC edits the paper itself lists |

## 5. Comment

## 6. Claude notes

*Suggestions from the reading agent. **Strip this section before copying into
`QuantArchSurvey/venues/ISCA/notes/`.***

- **Read depth.** Full close read of §I-§V. Three things unresolved and flagged in `ANALYSIS.md`: (i) the **definition of "exponent"** in Fig. 19's range claim — whether it is the raw IEEE-754 field or a bias-adjusted value is never stated, which matters because the whole outlier rule keys off [0, 8]; (ii) the **7.4% base-token fraction is not reproducible** — `F = ⌊N/M⌋` gives 1/18 = 5.6%; (iii) "both account for 5.1%" is ambiguous between *each* and *together*.
- **Both revision-log amendments are correct — confirm, don't revisit.** `non-Q` → **`Q`**: apply the test — under plain per-tensor INT8, delta generation buys nothing (deltas still cost 8 bits), the top-`p` bitmask has nothing to assign, the dual-array balance has no purpose, the reused CODEC quantizer has nothing to quantize. `G2` → **`G3`**: the problem is VLM-specific and value = reference + delta is literally a video-*compression* representation — the format-merging-with-compression signature G3 names.
- **I would drop `ADAPTIVE`.** TAXONOMY defines it as the *numeric type itself* being a learned or data-dependent variable (ANT/MERSIT/Anda). AQuant's types are plain INT2/INT4/INT8 fixed at synthesis; what is data-dependent is **which one each element gets** — which is what `MIXED` already says. The word comes from the title, not the encoding. **Precedent: you made the same call on LightNobel.** Contrast OliVe, which earns it via a genuinely adaptive exponent bias.
- **I would add `INT8` and `INT16`.** The seed's `INT4` `INT2` describes the deltas only and hides both escape hatches — a reader scanning the venue list concludes this is a W4A4-class design. It is **weight-unquantized**.
- **Best-citation claim, and the cross-paper point.** On the **outlier currency** axis this is a genuinely new entry: every other paper *pays* to keep an outlier (extra bits, a destroyed neighbour, a second datapath, compressibility). AQuant pays nothing because it **subtracts the outlier away** — the delta is small precisely where the token is extreme. That only works when the data has exploitable redundancy between rows, which is why it is a VLM paper and not an LLM one. Worth naming as **"reference-and-residual"** alongside re-anchoring (AQB8).
- **Credit where due, and it is unusual.** The self-audit is the most thorough in the corpus: CODEC-busy-with-real-video (6.9× → 6.8×), the algorithm on an unmodified GPU (**slower**), INT2-vs-pruning, fast/slow-motion splits, an L1-bucketed accuracy sweep, and a quant/dequant overhead breakdown. It also **discloses that its own GPU-Mixed-precision baseline is optimistic**. That makes **2.2× the most defensible number in the paper** and the one I would quote.
- **The one unaudited premise: the 36% → 1.4× CODEC saving.** It is measured against *a hypothetical AQuant with no CODEC* that spends 0.26 of its 0.714 mm² MAC budget on similarity + quantization logic. The paper never reports the **incremental** area of the modifications it lists — only the 0.26 mm² post-modification total — so the counterfactual charges nothing for the augmented subtractor, the reconfigurable partitioning, the top-k unit or the fp-to-int unit.
- **Second-hand number to avoid:** the claim that LLM.265 costs 97.8 / 63.5 pJ/bit, "higher than simply loading from LPDDR4X". That is a re-implementation's number about someone else's design, and it drives the 14.0× energy figure.
- **§5 material, if you want it.** The abstract/body mismatch on LLM.265 (4.5× vs 4.6×) is trivial in size but means the abstract and Fig. 14 disagree — cite the body. And Table I's motivating "43% of on-chip area" counts **only two blocks**, against a 64×64 INT8 array that is **not** the array AQuant builds (it builds 5×32×32).
