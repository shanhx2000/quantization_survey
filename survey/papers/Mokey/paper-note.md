# Mokey: Enabling Narrow Fixed-Point Inference for Out-of-the-Box Floating-Point Transformer Models

**Venue / Year:** ISCA 2022 · **Link:** https://arxiv.org/abs/2203.12758 (DOI 10.1145/3470496.3527438) · **Reader:** Haoxuan · **Date:** 2026-09-09

## Tags

| | |
|---|---|
| **Level** | `ALGO+ARCH` |
| **Q-oriented** | `Q-ORIENTED` |
| **Data type** | `VQ` `LUT` `FIXED` `INT4` |
| **Generation** | `G3` (codebook thread — **pre-LLM root, deliberate**) |
| **Optimization** | codebook · golden dictionary · exponential centroid fit · histogram-of-exponents · index-domain accumulation · outlier dictionary + pointer list · PTQ · memory-compression plug-in |

## 1. One-line summary

Forces every centroid onto the curve `a^int + b` (`a=1.179`, `b=−0.977`, `int∈[0,7]`) so that
`a^i·a^j = a^(i+j)` turns a multiply into a **3-bit index addition** — collapsing 256 possible
products into **15 possible exponent sums**, so a dot product becomes *counting how often each
sum occurs* plus one weighted reduction at the end, giving `W4A4` post-training at **0.22 error**
on BERT-Base MNLI with a fixed-point-only datapath.

## 2. Data type

**Formats.** `W4A4` — weights, embeddings, activations all 4b. 4b = 1 sign + 3b index.
Centroids 16b fixed-point. No floating point anywhere.

**Codebook — non-uniform but *constrained*.** Centroids must lie on `a^int + b`. That
constraint, not the codebook, is the paper. Fitted once, weighted `2^7`→`2^0` from the dense
bins outward.

**Dictionary source.** One model-independent **Golden Dictionary**: agglomerative clustering
(not k-means — no initialisation sensitivity) over 50k synthetic `N(0,1)` samples, offline,
reused across all models. Per tensor = `GD × s + m`, non-iterative.

**Granularity — per tensor.** One `(mean, std)` pair, two dictionaries (G 8×16b, OT 16×16b).
**No group, channel, block or token split.** Coarsest granularity in the corpus.

**Outliers.** Separate OT dictionary; values stay 4b indices; membership held in an explicit
**pointer list**, not in extra bits. Widening one dictionary instead would need `int`≤45 → 7b.
W 1.2–1.6%, A 1.7–4.5%; <4% of BERT multiplications.

**Escape hatch.** Outlier products expand to 16b centroids → **real MAC** in a shared OPP, one
at a time, 8 GPEs per OPP. Activations materialise as 16b fixed-point before requantization.
Final reduction is 15 multiplies.

**Retraining.** PTQ, **no fine-tuning**. Profiling = 1 batch × 8 samples; repeat runs
near-identical because exponential bins widen with the index.

## 3. Optimization

**The collapse.** `Σ A·W` expands to four terms. The dominant one carries exponent
`int_A + int_W ∈ [0,14]` — 15 values. So the PE holds 15 counters, increments one per operand
pair, and reduces once at the end against the 15 precomputed centroid products. The other three
terms: a sum over activations (computed for free while the previous layer's output is being
quantized), a sum over weights (compile-time constant), and `N·b²`. The multiplier is gone from
the inner loop entirely; what is left is an adder and a counter.

**Why 15 and not 256.** Without the exponential constraint, 16×16 centroids give 256 distinct
products and would need 256 counters per PE — the paper says outright that this is impractical
against an FP16 MAC. The curve is what makes the histogram small enough to be hardware.

**Outlier path.** Serial cascaded leading-one detector across the 8 GPEs picks the first PE
holding an outlier and routes its indices to the shared Outlier/Post-Processing unit, which
looks up the 16b centroids and does an ordinary MAC. Affordable only because outliers are
rare; the same unit doubles as the post-processing engine for the four final summations.

**Requantizer.** Output activations arrive as 16b fixed-point and are compared against all 32
sorted centroids (G and OT together); a leading-one detector and two muxes pick the two
neighbours, a subtract-and-compare picks the nearer, and the result is encoded as an index.

**Plug-in mode.** The compression half works alone: keep an FP16 accelerator, use Mokey only to
pack values to 4b indices going into and out of memory, expand on the way back. Buys 4× off-chip
traffic without touching the datapath.

## 4. Results

| | |
|---|---|
| Baseline | 2048-unit FP16 Tensor Core accelerator; **GOBO** (MICRO'20) re-implemented in the same flow; buffer capacity swept 256 KB – 4 MB |
| Models / datasets | BERT-Base/Large, RoBERTa-Large, DeBERTa-XL (750M); MNLI, STS-B, SQuAD v1 |
| Accuracy delta | `W4A4` PTQ: **0.22** BERT-Base MNLI, **0.57** DeBERTa-XL, worst case **0.98** RoBERTa-Large SQuAD. Weight-only sometimes *beats* FP (−0.36) |
| Speedup | Accelerator **11× → 4.1×** over FP16 TC (small → 4 MB buffers). Plug-in only: **3.9× → 4.3×** |
| Energy / area | **78× → 13×** energy efficiency over FP16 TC; **9× → 2×** over GOBO. 512 KB, iso-area: 29M cycles / 0.09 J vs TC 167M / 0.36 J and GOBO 52M / 0.17 J. PE 39% smaller at equal MAC/cycle |
| Compression | **7.9×** total footprint, at lower error than Q8BERT (0.69/4.0×), I-BERT (0.32/4.0×), GOBO (0.68/4.1×). Only row that is both fixed-point **and** post-training |
| Technology node | **TSMC 65 nm**, 1 GHz |
| Evidence level | **post-layout** (DC + Innovus, CACTI memories) + **custom cycle-accurate simulator**. No silicon, no artifact |
| **Is the comparison fair?** | **Fair, and conservatively set up.** Iso-compute-area and iso-buffer-capacity, both stated; Mokey's smaller total chip area is deliberately *not* spent. Authors volunteer that an FP32 baseline would have flattered them. Do not quote **78×** bare — it is the 256 KB point; the range is 13–78×. **65 nm: no absolute number here compares with the 28/7 nm entries.** |

## 5. Comment

## 6. Claude notes

*Suggestions from the reading agent. **Strip this section before copying into
`QuantArchSurvey/venues/ISCA/notes/`.***

- **§5 material, if you want it.** *Placement:* §5.5/§5.6, and it is the **root** of the
  lookup thread — "count index occurrences, then reduce once against a small table" is Mokey
  2022 and it is also OASIS 2026. *Best citation for:* that a codebook's value is not the
  centroids but the **algebraic structure you can impose on them** — Mokey buys 15 bins instead
  of 256 by giving up centroid freedom. *Why G3:* codebook thread, four years before the LLM
  pressure that made it mainstream; TAXONOMY assigns this deliberately, do not soften it.
- **The pairing worth writing down.** Mokey and [`OASIS`](../OASIS/ANALYSIS.md) solve the same
  problem — make the product table small enough to be hardware — and pay opposite prices.
  Mokey **constrains the centroids** (free table, lossy fit); OASIS **learns both codebooks**
  (perfect fit, 256-entry table, but constant in `K`). **OASIS does not cite Mokey.** That is
  a survey-level observation, not a criticism of either.
- **The unablated question.** How much accuracy does forcing centroids onto `a^int+b` actually
  cost versus free agglomerative-clustering centroids? The paper never separates it, and it is
  the paper's central trade. If §5.5 wants one open question, this is it.
- **Per-tensor scaling is the reason this did not scale.** Every 2023+ entry moved to
  per-channel / per-token / per-group. Mokey has one `(m,s)` per tensor and never meets a model
  where that breaks — encoder-only, ≤750M, ≤512 tokens, no decode, no KV cache. Worth one
  sentence in the survey as *why the pre-LLM roots stayed roots*.
- **Outlier shape is inherited from [`OLAccel`](../OLAccel/ANALYSIS.md)**, 2018: dense
  low-precision majority + sparse high-precision path + an explicit list of which is which.
  Two threads, same structural answer, four years apart — that is the §5.10 paragraph.
- **GOBO (MICRO'20) is the missing entry.** It is Mokey's direct predecessor and its main
  baseline, and it is not in this ISCA-only corpus. §5.5 will feel the hole.
