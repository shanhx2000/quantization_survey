# Tender: Accelerating Large Language Models via Tensor Decomposition and Runtime Requantization

**Venue / Year:** ISCA 2024 · **Link:** https://arxiv.org/abs/2406.12930 · **Reader:** Haoxuan · **Date:** 2026-09-09

## Tags

| | |
|---|---|
| **Level** | `ALGO+ARCH` |
| **Q-oriented** | `Q-ORIENTED` |
| **Data type** | `INT8` `INT4` |
| **Generation** | `G3` (LLM activation-outlier thread) |
| **Optimization** | outlier-aware · channel decomposition · power-of-two scale ratio · implicit requantization · shift-based rescale · systolic · commodity-friendly |

## 1. One-line summary

Bins activation channels into geometric bands by absolute max so outlier channels get their own
scale, and constrains consecutive band scales to be **exactly 2× apart** so accumulating across
bands is a **1-bit shift instead of a floating-point requantization** — outlier isolation on a
plain symmetric-INT systolic array whose only extension over commodity hardware is one shifter.

## 2. Data type

**Formats.** `W8A8` and `W4A4`, plain **symmetric linear INT** both sides, applied to AW *and* AA matmuls (attention `X_Q·X_K^T` included). No custom datatype, no mixed precision, no outlier encoding — that restraint is the contribution.
**Granularity.** Channels binned by `CMax` into `G` geometric bands (`TMax/2^g < CMax_i ≤ TMax/2^(g-1)`), one scale per band — i.e. **block (group-wise) quantization**, where the blocks are clusters of channels grouped by magnitude rather than contiguous runs, and each cluster carries its own scale. **Group size is not fixed** — band membership is data-dependent; outlier bands hold few channels, inlier bands many.
**Outliers.** Isolated by grouping only — own scale, not own datatype/precision/lane. Cheapest outlier mechanism in the corpus.
**Accumulator.** **32-bit** per PE (internal `Acc` register). Each band transition **left-shifts** it 1 bit, so headroom is consumed upward and band count `G` is bounded by it — the paper asserts the width is "sufficiently large" rather than deriving a bound. Baselines forced to 32-bit too, "due to the large reduction length" in LLMs.
**Escape hatch.** Per-channel bias must be added back (`bias × W` into the output); FP16 final dequant; 64-FPU VPU; 1-cycle bubble per band transition. **PTQ**, calibrated offline on 128 Pile samples.

## 3. Optimization

Premise: outliers live in channels, so isolating them wants per-channel scales — but that
multiplies matmul/dequant/add count by the channel count (**4096× for OPT-6.7B**). Every prior
fix paid that or introduced a custom datatype. Tender changes neither the format nor the
datapath, only the grouping and the rescale.

**Bias subtraction.** Per channel subtract `(max+min)/2` so `|max| = |min|` and the symmetric
range is fully used.

**Power-of-2 decomposition.** Bin channel *i* into band *g* where
`TMax/2^g < CMax_i ≤ TMax/2^(g−1)`. Classification against fixed thresholds, not clustering —
clustering "is not likely applicable at runtime without complex hardware". *Why geometric:*
quantization error ∝ absolute max × channel count. Outlier channels are few, so a coarse
threshold there is cheap; inlier channels are many, so they need fine thresholds. A geometric
split gives exactly that gradient for free.

**Implicit requantization.** Consecutive band scales differ by exactly 2× → accumulating across
bands is a **1-bit shift**, no FP rescale. Process largest-scale band first, shift the
accumulator between bands, dequantize once at the end. Mathematically equal to
`Y = Σ(s_i·s_w)·P_i` but with the reduction axis intact, so the array stays full instead of
splitting into `G` small matmuls.

**Hardware.** INT4-only output-stationary systolic array (64×64 PEs, 64 FPUs, 32-bit
accumulators) **plus one shifter next to the accumulator**. That shifter is the entire
extension. ANT and OliVe by contrast shift by an exponent sum and need decode logic — which is
why Tender's array is denser and wins at iso-area while doing nothing clever numerically.

## 4. Results

| | |
|---|---|
| Baseline | SmoothQuant (software); ANT, OliVe, OLAccel (accelerators). Iso-area: MAC units of each synthesized and PE counts matched |
| Models / datasets | OPT-6.7/13/66B, LLaMA-7/13B, Llama-2-7/13/70B; WikiText-2 + PTB perplexity, seq 2048. BERT-Large/GLUE as generality check |
| Accuracy delta | **INT8 works**: OPT-6.7/13/66B **+0.07 / +0.04 / +0.09** PPL vs FP16; Llama-2-7B 5.47 → 5.77. Beats SmoothQuant 48.54, ANT 8.79, OliVe 8.16 on Llama-2-7B. **INT4 fails**: Llama-2-7B **36.47** vs FP16 5.47 (baselines worse — SmoothQuant 3E+5, ANT 189.72, OliVe 44.24) |
| Speedup | **2.63× ANT, 1.84× OLAccel, 1.48× OliVe** at iso-area — but measured at INT4 |
| Energy / area | Energy efficiency 1.84× / 1.53× / 1.24×. **3.98 mm², 1.60 W peak**, 64×64 PEs + 64 FPUs |
| Technology node | 28 nm, 1 GHz |
| Evidence level | **post-synthesis** (RTL, Synopsys DC) + **cycle-level simulator** (Ramulator DRAM timing), HBM2 with FG-DRAM energy model. No silicon |
| **Is the comparison fair?** | Iso-area **constructed, not just claimed** — MAC units of every baseline synthesized, PE counts matched, same bandwidth and buffer, 32-bit accumulators forced on all. Iso-node ✓ (28 nm). **But iso-accuracy ✗**: the speedups are measured at INT4, where Tender's own PPL is 36.47 vs FP16 5.47. Quote speedups only with the accuracy attached. "Up to 10988× lower perplexity" is a ratio between two failing numbers. Regime: **batch 1, 2048:1 in:out — prefill**; decode under-utilisation admitted |

## 5. Comment


## 6. Claude notes

*Suggestions from the reading agent. **Strip this section before copying into
`QuantArchSurvey/venues/ISCA/notes/`.***

**Human verified: no.**

- **Seed-tag disagreement — drop `POW2`.** `venues/ISCA/README.md` tags Tender `INT` `POW2`,
  but **no value in Tender is a power of two** — values are plain symmetric INT4/INT8. What is
  power-of-two is the *ratio between band scale factors*. `TAXONOMY.md` defines `POW2` as a
  logarithmic / power-of-two **number format**, so the tag signals a log-domain encoding Tender
  does not have. Suggest `INT8`+`INT4`+`MIXED`, with the power-of-two-scale idea in the
  free-text Optimization field.
- **Citation hazard — three papers report three "Tender at 4-bit" numbers, all legitimate.**
  Tender's own Table II: **36.47** (Llama-2-7B, INT4 W+A). Oaken: **6.42** (KV-cache-only 4-bit,
  W/A left FP16). Omni-LUT: **123.1** (W/K/V/A all INT4). Spans 19×. Never quote it without
  naming which tensors were quantized. Also worth knowing: TransitiveArray's "TD-4" figures
  match Tender's own table exactly, so that paper quoted correctly.
- **The real survey fact is stronger than "Tender is weak at INT4".** Table II shows *every*
  outlier-aware PTQ method of 2024 failing at INT4 W+A on Llama-2 — SmoothQuant 3E+5, ANT
  189.72, OliVe 44.24, Tender 36.47, against FP16 5.47. **INT4 weight-and-activation PTQ was
  unsolved with uniform formats**, and that is precisely the opening OASIS and Omni-LUT
  exploited with non-uniform ones. Good §5.x transition.
- **§5 material, if you want it.** Placement: the *restraint pole* of the outlier thread —
  OliVe changes the encoding, OLAccel adds mixed-precision lanes, MicroScopiQ changes the block
  format; Tender changes neither format nor datapath. Best citation for: designing the algorithm
  around what commodity hardware already does, and for the error model `Qerr ∝ absmax × channel
  count` that justifies geometric binning. `G3` by problem, not format.
- **Data caution.** On **PTB**, Llama-2 FP16 baselines (20.83 at 7B, 28.93 at 13B) are *worse*
  than several quantized rows. Those FP16 PTB numbers look anomalous — cite the WikiText-2
  columns.
