# Oaken: Fast and Efficient LLM Serving with Online-Offline Hybrid KV Cache Quantization

**Venue / Year:** ISCA 2025 · **Link:** https://arxiv.org/abs/2503.18599 (DOI 10.1145/3695053.3731019) · **Reader:** Haoxuan · **Date:** 2026-09-09

## Tags

| | |
|---|---|
| **Level** | `ALGO+ARCH` |
| **Q-oriented** | `Q-ORIENTED` |
| **Data type** | `INT4` `INT5` `MIXED` |
| **Generation** | `G3` (KV-cache + outlier threads) |
| **Stage type** | `S2T4` |
| **Optimization** | KV cache · outlier-aware · offline threshold profiling · group-shift · dense-and-sparse · COO · DMA-integrated |

## Stage-type tags

**`S2T4`** (the **Stage type** row in Tags) — most-matched first. Large and small KV outliers leave the INT4 inliers for an INT5 dense-and-sparse path, with thresholds profiled offline.

*Tag form `S{stage}T{type}`, vocabulary from `survey/stage2.md` and `survey/stage3.md`. Added 2026-10-02 (ISCA Stage-type batch 1).*

## 1. One-line summary

Splits each per-token KV vector into three magnitude groups — inliers INT4, large *and* small
outliers INT5 — using **thresholds profiled offline**, so the only online work is a comparison
instead of a topK sort. Reuses the zeroed dense slots the outliers leave behind to hold 4 of
their 5 bits, landing each sparse entry on exactly 8 aligned bits. ~4.8 effective bits, 1.79×
throughput over an FP16 A100, as engines bolted into an existing accelerator's DMA path.

## 2. Data type

**Formats.** KV-only, `W16A16KV~4.8`. Middle group (inliers, 90%) INT4; inner 6% + outer 4% INT5 + 8b COO. Effective bits = 4 + 10%×8 = **4.8**.
**Granularity.** Per-token vector → 3 magnitude groups; thresholds global per model, offline-profiled. No sub-grouping inside the middle group (KIVI's is why it sits at 4.99).
**Outliers.** Isolated both sides (large *and* small) but **not high-precision** — 5-bit, one above inliers. Cost is metadata, not precision.
**Weights FP16 by argument** (§4.1: weight memory constant in batch, KV grows). PTQ + mandatory ~10 min per-model threshold profiling.

## 3. Optimization

Premise: online topK to find outliers costs more than quantization saves. Move the expensive
half offline.

**Threshold-based online–offline hybrid.** Four thresholds cut each per-token KV vector into
outer / middle / inner. Profiled offline (~100 inferences, ~10 min per model); online is a
compare, not a sort. Ratios fixed globally at 4 / 90 / 6 on the claim that KV distribution is
input-insensitive.

**Group-shift.** A large-magnitude group quantized uniformly wastes its range → subtract the
group's offline threshold first, narrowing the span so a low bitwidth covers it. Applied to
outer and middle.

**Fused dense-and-sparse encoding.** Outliers are zeroed out of the dense matrix → reuse those
dead 4-bit slots to carry 4 of the outlier's 5 bits. Sparse entry drops 23 → 8 bits and stays
memory-aligned, so the MMU pages dense and sparse uniformly. This is what lands the bitwidth at
4.8 rather than well above 5.

**Hardware.** Not a new chip — quant/dequant engines + MMU in an existing accelerator's DMA
path (demonstrated on LPU), so it is portable to other accelerators. 8.21% of core area; dequant
is 3.4× quant's area because it runs on every KV read, quant only on generation. Both latencies
hidden by overlap and streaming (1.29% / 3.23% of end-to-end at batch 64).

## 4. Results

| | |
|---|---|
| Baseline | vLLM (A100 FP16), QServe, KIVI, KVQuant on A100; Tender (ASIC); LPU (same accelerator, no KV quant). All quantization baselines **KV-only 4-bit**, QServe/Tender W+A quantization **disabled** |
| Models / datasets | Llama2-7/13/70B, OPT-6.7/13/30B, Mistral-7B, Mixtral-8x7B; Wikitext2 PPL + PIQA/Winogrande/Hellaswag; Azure Conversation + BurstGPT traces |
| Accuracy delta | **0.87% avg loss vs FP16.** −0.54% vs KVQuant, −0.32% vs KIVI, **+1.38% vs QServe.** Effective bits: Oaken **4.82/4.82/4.89** vs KVQuant 4.81–5.01, KIVI 4.99, Atom/QServe 4.25, Tender 4.07 |
| Speedup | Batch 256: **1.79× vLLM, 1.58× QServe.** Attention latency −55.0% vs LPU. Oaken-LPDDR reaches 32K seq; QServe and Oaken-HBM cap at 16K |
| Energy / area | **222.7 W** vs A100 400 W TDP (−44.3%). Quant 1.86% + dequant 6.35% = **8.21%** of 3.971 mm² core |
| Technology node | TSMC 28 nm, 1 GHz (Oaken engines); A100 baselines at 7 nm |
| Evidence level | **post-synthesis** (added engines only) + **simulator** extending the LPU simulator (all throughput). No silicon |
| **Is the comparison fair?** | Setup yes — baselines held to KV-only 4-bit, QServe/Tender W+A disabled, 2× A100 for large models. Node not iso (28 nm vs 7 nm), but only a *power* claim is made. **Cite §6.2, not the abstract**: "1.58× over A100" is the QServe number (FP16 is 1.79×); "0.54% loss" is the gap to KVQuant (vs FP16 = 0.87%). Range disclosed: **below 8K sequence, vLLM and QServe win** |

## 5. Comment


## 6. Claude notes

*Suggestions from the reading agent. **Strip this section before copying into
`QuantArchSurvey/venues/ISCA/notes/`.***

- **Venue is now resolved.** The archived PDF carries its own ACM block — "ISCA '25, Tokyo,
  Japan … DOI 10.1145/3695053.3731019". `survey/README.md`'s "two entries with unverified
  venues" note should drop Oaken, leaving only `BitFusion`. Not edited — yours to maintain.
- **The Omni-LUT dispute is settled in Omni-LUT's favour, factually.** Its claim that
  KIVI/KVQuant/Oaken sit at "4.8–5.0 bits" is confirmed by **Oaken's own Table 2** (4.82/4.82/
  4.89). But that reframes the question: Omni-LUT's 4.25 bits is the **Atom/QServe** point in
  the same table, and Oaken beats QServe by 1.38% accuracy. **The comparison the survey wants
  is Omni-LUT vs Atom/QServe at iso-bitwidth — and neither paper makes it.**
- **P3-LLM's criticism is substantively right** (revised after reading P3-LLM in full). Its
  "~10% of values" is exact (4%+6%), and that puts Oaken at **4.8 effective bits** — confirmed by
  **Oaken's own Table 2**. P3-LLM sits at 4.16 and still wins by 1.04% accuracy. Only the phrase
  "high-precision" is loose: Oaken's outliers are **5-bit**, one above the inliers, and the real
  cost is COO metadata. Don't cite the wording; the bitwidth argument stands.
- **`Tender` is now the weak baseline in two independent papers** (here: PPL 6.42 vs FP16 5.47
  on Llama2-7B; in Omni-LUT: INT4 gives PPL 123.1). Worth carrying into Tender's own entry.
- **§5 material, if you want it.** Placement: §5.7 KV-cache anchor — the non-LUT answer to the
  pressure Omni-LUT attacks. Best citation for: *online outlier detection*, not the arithmetic,
  is what kills KV quantization. `G3` by problem, not format — no new numeric type. Unadmitted
  limits: KVQuant and KIVI beat it on accuracy at comparable bits (the defence is their sorting
  cost, never quantified in the same table), and 4/90/6 is fixed across 8 models with
  sensitivity shown for Llama2-7B only.
- **Weight-vs-KV is a live disagreement, not a difference of emphasis.** Oaken argues in §4.1
  that weight quantization is the wrong lever for batched serving; LUT Tensor Core,
  TransitiveArray and OASIS are all built on it. Reconcilable by regime (prefill/edge vs
  batch-256 serving), but no paper draws that line. Worth a paragraph.
- **Adoption barrier may deserve to be a survey axis.** Oaken = engines in a DMA path;
  LUT Tensor Core = replace the Tensor Core + new ISA + new compiler. That spread predicts
  which of these ever ships, and nothing in our current tag set captures it.
