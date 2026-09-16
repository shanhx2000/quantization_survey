# OASIS: Outlier-Aware LUT-Based GEMM with Dual-Side Quantization for LLM Inference Acceleration

**Venue / Year:** ISCA 2026 · **Link:** no public URL (proceedings only; DOI 10.1109/ISCA66397.2026.00036) · **Reader:** Haoxuan · **Date:** 2026-09-03

## Tags

| | |
|---|---|
| **Level** | `ALGO+ARCH` |
| **Q-oriented** | `Q-ORIENTED` |
| **Data type** | `VQ` `LUT` `INT4` `INT3` `FP16` `MIXED` |
| **Generation** | `G3` (codebook + outlier threads) |
| **Optimization** | LUT-GEMM · Cartesian-product LUT · dual-side quantization · NU-WAQ · learned codebook · outlier-aware · look-ahead compensation · top-k engine |

## 1. One-line summary

Quantizes **both** operands to 4-bit learned K-Means codebooks, which makes the table the
**Cartesian product of the two codebooks** — 256 static entries, computed offline, independent
of reduction length. GEMM becomes: concatenate indices → count occurrences → weighted sum of
table entries. Top and bottom 0.5% of activations compensated in FP16 on a concurrent branch,
so outlier detection never touches the critical path.

## 2. Data type

**Formats.** `W4A4` and `W4A3`. Non-uniform both sides — K-Means learned codebooks, values are
indices. Activations index-coded too, which almost nothing else does.

Dual-side is what makes the table static. WOQ LUT stores inner products of μ activations →
regenerated per tile, size 2^μ, forces μ=4 and partial-sum reductions across K/μ groups. Both
sides quantized → store the codebook Cartesian product instead: 2^(nW+nA) = 256 entries at
W4A4, precomputed, **constant in K**. Reduction drops from K FP16 adds to 256.

**Granularity.** Weights: one codebook for the whole matrix, scale per output channel.
Activations: scale per token, codebook global and offline-learned from 16 C4 samples. Codebook
granularity must stay global or the Cartesian LUT stops being static — that constraint is the
design, not a default.

**Outliers.** Top 0.5% + bottom 0.5% of activations in FP16, detected dynamically by Orizuru
(twin max/min tournament trees, shared leaves). Weights get **no outlier protection at all**.
Dynamic detection is required: offline-vs-online thresholds RMSE 0.32–0.38, but centroids RMSE
0.01 — so centroids can be learned offline and thresholds cannot.

**Escape hatch.** 1% of activations at FP16 → effective ~4.12 bits. Reduction tree is FP16;
"no multiplier" applies to the GEMM, not the chip. 8 FP16 MAC units per PE line for the
compensation branch.

**Retraining.** PTQ. Post-training K-Means on stock weights; activation centroids from 16 C4
samples. Not free — 42 min for 16 samples on LLaMA-3-8B, 100 min at 32.

## 3. Optimization

WOQ dequantization is 20–90% of GEMM runtime → kill it by quantizing both sides. But NU-WAQ is
index-coded, so existing units dequantize anyway → build hardware that consumes indices
directly.

Cartesian-product LUT: 64× smaller / 1024× group size / 16× fewer reduction FLOPs (analytical,
W4A4, K=N=4096). Measured on q_proj: 62.1× smaller than FIGLUT and LUT Tensor Core, 994.2×
than LUT-GEMM; reduction FLOPs 497.1× / 248.6× fewer. The real win is size **constant in K** —
WOQ tables grow with input channels, this one does not.

Look-ahead: don't scan-then-split. Main branch quantizes everything including outliers and
ignores their error; outlier branch computes that error and compensates. Same result,
detection off the critical path. Worth 16–18% throughput over doing it conventionally.

PE is a Concat Unit — takes two 4-bit indices, concatenates to 8 bits. 4096 per line, 16 lines.
15.31 mm², 9.66 W at 28nm.

Sized for 1% outliers: both branches take comparable time there. Past 1% the outlier branch
becomes the bottleneck.

## 4. Results

| | |
|---|---|
| Baseline | A100-80GB (FP16), QuaRot W4A4 kernel on A100, FIGLUT ASIC **at W4A16**; algorithm baselines RTN, SmoothQuant, QuaRot, Atom (group size 128) |
| Models / datasets | OPT-6.7/13/30B, LLaMA-7/13/30B, LLaMA-2-7/13/70B, LLaMA-3-8B, Mistral-7B; WikiText-2 PPL + 6 zero-shot tasks |
| Accuracy delta | **W4A4: 2.05% avg zero-shot drop vs FP16, 6.44% better than Atom. W4A3: 5.90%.** LLaMA-2-7B PPL 5.47 → 5.90; LLaMA-3-8B 6.14 → 7.11 |
| Speedup | OASIS-A4: 5.41× A100, 3.12× QuaRot, **3.00× FIGLUT**. Low-batch 3.41×. Prefill/decode sweep 2.80× over FIGLUT |
| Energy / area | 198.1× A100, 108.8× QuaRot, **1.44× FIGLUT**. 15.31 mm² / 9.66 W @28nm. No baseline area reported |
| Technology node | TSMC 28 nm |
| Evidence level | **synthesis** (core logic area/power) + **cycle-accurate simulator** modified from DnnWeaver + Cacti (SRAM) + DRAMSim3 (HBM). No silicon |

**Is the comparison fair?** Iso-node yes, iso-precision **no**, iso-area unknowable.

FIGLUT runs **W4A16**; OASIS runs W4A4/A3. The 3.00× and 1.44× fold in the gain from
quantizing activations 4× narrower — which OASIS pays 2.05% accuracy for and FIGLUT pays
nothing for. Always quote as "W4A4 vs W4A16". No baseline area or power is given anywhere, so
there is no iso-area claim. The 198× energy over A100 compares a 28nm ASIC to a GPU.

Iso-accuracy against the algorithm baselines is done carefully — Atom's group-128 advantage is
disclosed with a dagger and OASIS still wins.

## 5. Comment

**§5.6, third pole of the LUT thread.** LUT Tensor Core builds an eager per-tile table;
TransitiveArray a lazy per-tile table; OASIS builds **no runtime table at all**. Reading the
three together gives §5.6 its organizing claim: **quantizing both operands is what turns a
runtime table into a compile-time constant.**

**Best citation for.** That dual-side non-uniform quantization is executable in hardware
without dequantization — and for the 20–90% dequantization-overhead figure that motivates the
whole LUT line.

**Why G3.** Codebook thread pushed further than anything else in the corpus (to both operands)
plus the outlier thread. Explicitly *against* weight-only, so not that thread.

**Admitted limits.** Outlier branch becomes the bottleneck above 1%; W4A3 costs 5.90%;
calibration time grows steeply past 16 samples.

**Unadmitted.** Weight index traffic is 76% of on-chip traffic while the LUT is 19.2% — the
LUT-size victory addresses the smaller share. Zero-shot averages cover 3 models, the PPL table
11. Weights get no outlier protection.

## 6. Claude notes

*Suggestions from the reading agent. **Strip this section before copying into
`QuantArchSurvey/venues/ISCA/notes/`.***

**Human verified. Yet further careful proofreading is still suggested.**

- **The paper misreports its own headline three ways.** Abstract 1.98%/5.18%, intro
  1.94%/6.34%, §V-B 2.05%/6.44%. Only §V-B is derivable from Table IV — the intro's figures
  are the **LLaMA-2-7B row alone**, substituted for the average. Our `ANALYSIS.md` brief had
  inherited the intro's numbers; corrected there. Worth flagging if you ever cite this paper.
- **§III-A and §V-A contradict each other** on whether activation centroids are per-token or
  global. Only global works — per-token online centroids would make the Cartesian LUT
  non-static and collapse the premise. §V-A is operative.
- **Eager / lazy / offline** is now a three-paper structure with `LUTTensorCore` and
  `TransitiveArray`. If §5.6 wants one sentence, this is it.
- **Cross-paper.** All three LUT papers constrain scale granularity so the table stays shared —
  and OASIS is the only one that says so. The other two leave it unstated.
