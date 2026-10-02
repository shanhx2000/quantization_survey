# LightNobel: Improving Sequence Length Limitation in Protein Structure Prediction Model via Adaptive Activation Quantization

**Venue / Year:** ISCA 2025 · **Link:** https://arxiv.org/abs/2505.05893 · **Reader:** Haoxuan · **Date:** 2026-09-10

## Tags

| | |
|---|---|
| **Level** | `ARCH` |
| **Q-oriented** | `Q-ORIENTED` |
| **Data type** | `INT4` `INT8` `INT16` `MIXED` |
| **Generation** | `G2` |
| **Stage type** | `S2T4` |
| **Optimization** | token-wise adaptive quantization · runtime top-k outliers · dynamic per-token scaling · calibration-free · multi-precision MPU · activation-only · granularity chosen for dataflow |

## Stage-type tags

**`S2T4`** (the **Stage type** row in Tags) — most-matched first. INT4/INT8 inliers with per-token runtime scales and INT16 outliers picked by runtime top-k with adaptive k. The per-token scale and the three widths belong to that outlier path, so nothing else is carried.

*Tag form `S{stage}T{type}`, vocabulary from `survey/stage2.md` and `survey/stage3.md`. Added 2026-10-02 (ISCA Stage-type batch 2).*

## 1. One-line summary

Quantizes **only the activations** of a protein-structure model — INT4/INT8 inliers with
**per-token scale factors computed at runtime** and INT16 outliers picked by **runtime top-k with
adaptive k** — choosing token granularity because attention-based models *compute* token-wise, so
channel-wise scaling would force per-value dequantization inside every token and break the
parallelism; executed on a reconfigurable multi-precision MAC-tree unit, cutting **peak memory up
to 120.05×** and so turning protein sequences that previously did not fit into ones that run, at
**8.44×/8.41×** over A100/H100 with TM-score essentially unchanged.

## 2. Data type

**Weights are not quantized at all.** 16-bit fixed point throughout — "to maximize model accuracy". The corpus's only **activation-only** design.
**Activation inliers: INT4 or INT8**, chosen dynamically. **Outliers: INT16.** Applied to **Pair Representation** activations, the identified bottleneck.
**Granularity: per token**, one scale each, **computed at runtime**. No calibration set, no fine-tuning.
**Why token-wise — the reason is dataflow, not statistics.** Linear layers and LayerNorm compute token-wise, so channel-wise scaling "necessitates the dequantization of individual values within a token before every operation." That PPM also concentrates large values in specific tokens is the *second* reason.
**Outliers: runtime top-k, adaptive k.** Thresholds can't be precomputed — token counts vary with the input protein and PPM outliers move unpredictably (biasing, merging with Sequence Representation). `O(n log n)` is affordable **only because PPM's hidden dimension is 128**.
**Symmetric, not asymmetric** — justified by measurement: symmetric *without* outlier handling costs **+27.35% RMSE**; with outliers removed the inlier distribution is uniform, so symmetry suffices.
**Accumulator.** Not reported. RMPU is a MAC-tree; VVPU handles quantize/dequantize/top-k.
**Escape hatch.** 16-bit weights everywhere, plus INT16 outliers with a **variable count per token**.
**Retraining.** **None, and no calibration dataset either** — the strongest form of PTQ in the corpus alongside P3-LLM.

## 3. Optimization

**The granularity argument is architectural, and that makes it the best-reasoned in the corpus.**
Everyone else picks a granularity to reduce quantization error. LightNobel picks token-wise because
the *hardware* is token-parallel: a channel-wise scale factor cuts across the unit of parallel work,
forcing you to dequantize individual values inside a token before every operation. Token-wise
scaling keeps the scale constant across exactly the granularity the datapath executes. That is a
different and, for accelerator design, more consequential claim than "finer is more accurate."

**Dynamic outlier selection, and an honest account of why it's affordable.** Because token counts
vary per protein and PPM's outliers shift with input, nothing can be precomputed the way
channel-wise schemes precompute thresholds. So top-k runs at inference, with adaptive k and
dedicated hardware. The paper doesn't pretend this generalises: `O(n log n)` per group would be
prohibitive in a general attention model, and it works here **only because the hidden dimension is
128**. This is the clearest case in the corpus of a technique that is affordable *only* in its
domain — worth citing as exactly that.

**It's a capacity paper, and the headline is a capability claim.** Pair Representation carries an
extra dimension, so activation memory explodes with sequence length and long proteins simply cannot
be run. **120.05× peak memory reduction** converts impossible sequence lengths into feasible ones.
That is a different kind of result from a speedup and should be presented as one.

**Hardware.** A reconfigurable multi-precision **RMPU** (MAC tree) handling INT4/INT8 inliers
against 16-bit weights, plus **4 VVPUs per RMPU** (the design-space saturation point) doing
quantization, dequantization and top-k.

## 4. Results

| | |
|---|---|
| Baseline | **NVIDIA A100 and H100 only** — no accelerator exists for this workload. Algorithmic comparison against MEFold and other quantization schemes |
| Models / datasets | AlphaFold2, ESMFold class (PPM). CAMEO, CASP14, CASP15 — including T1169, 3,364 residues |
| Accuracy delta | **TM-score 0.539–0.540 vs no-quant 0.540** — negligible. A competing scheme drops to **0.493**. **TM-score is not comparable with any other accuracy number in the corpus** |
| Speedup | **8.44× / 8.41×** over A100 / H100 |
| Energy / area | **37.29× / 43.35×** power efficiency over A100 / H100. **Peak memory up to 120.05×**; footprint on T1169: no-quant FP16 **113.49 GB**, MEFold INT4 94.60 GB |
| Technology node | **28 nm, 1 GHz** (SystemVerilog + Synopsys DC 2019.3); scratchpads via 28 nm memory compiler + CACTI 7.0 **downscaled from 32 nm**; Ramulator with **80 GB / 5 HBM2E stacks matched to the GPUs** |
| Evidence level | **Cycle-accurate Python simulator cross-validated against RTL simulation** + synthesis. No silicon |
| **Is the comparison fair?** | HBM capacity and stack count matched to the GPUs, RTL synthesised, simulator cross-validated against it. But the **only baselines are A100/H100** (no peer design exists) and they are **not node-matched** — 28 nm vs 7/4 nm, with no scaling applied. The headline **120.05×** appears to include the token-wise-MHA saving that §8.1 explicitly **excludes** from its own fair-comparison table, and is never itemised |

## 5. Comment

Only INT support is mentioned.

## 6. Claude notes

> **Suggestions from the reading agent. Strip this section before copying into
> `QuantArchSurvey/venues/ISCA/notes/`.**

- **The revision log's `non-Q` → `Q` change is correct.** Apply the test: swap AAQ for plain INT8
  and the multi-precision reconfigurability, the top-k hardware, the per-token dynamic scaling and
  the INT16 outlier path all lose their purpose. That's the second of the log's flagged rows
  settled (Ecco was the first).
- **One data-type refinement.** The seed says `ADAPTIVE` `INT` `MIXED`. The taxonomy prefers
  bitwidths and all three are known exactly: **`INT4` `INT8` `INT16` `MIXED`**. "Adaptive" describes
  the *selection policy*, not the format — I'd move it to Optimization.
- **§5 material, if you want it.** This is the best-reasoned granularity argument in the corpus and
  the reason is worth stating: **it picks token-wise because attention *computes* token-wise**, not
  because tokens quantize better. Channel-wise scaling cuts across the unit of parallel work.
  Everyone else (Tender per-channel, Oaken/MicroScopiQ per-group, DRQ per-region) argues from
  accuracy; this argues from dataflow, which for accelerator design is the stronger claim.
- **It's also the strongest `dynamic` entry since DRQ**, and it explains why dynamic selection
  hasn't generalised. Both the scales *and* the outlier set are chosen at runtime with no
  calibration at all — affordable **only because PPM's hidden dimension is 128**. DRQ argued for
  runtime selection in 2020 and lost the field to design-time methods; P3-LLM recovered part of it
  with per-request smoothing; LightNobel goes furthest, on a domain exemption.
- **Corpus's only activation-only design.** GOBO and MicroScopiQ are weight-only, Oaken is KV-only,
  most others do both. Here the weights stay 16-bit because in PPM the *activations* are what won't
  fit — the format follows from the capacity framing.
- **Outlier currency, seventh position:** INT16 outliers chosen by runtime top-k with **adaptive
  count** — the only entry where the *number* of outliers isn't fixed in advance.
- **Two things to watch when citing.** The **120.05×** and §8.1's fair-comparison footprint table
  are different accountings — §8.1 excludes the token-wise-MHA saving "for a fair comparison", the
  headline apparently doesn't, and it's never itemised. And **TM-score is incommensurable** with
  perplexity/accuracy elsewhere; 0.540 → 0.539 reads as negligible but comes with no variance.
- **A gap in the mechanism:** `k` is "set adaptively based on the activation characteristics" and
  the policy is never specified. For a runtime scheme that's the load-bearing hyperparameter.
- **`G2` in 2025 is worth one defending sentence**, same as RaPiD: uniform symmetric INT with an
  outlier escape and no new number format is a G2 paradigm regardless of date.
