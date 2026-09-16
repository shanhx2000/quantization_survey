# Oaken — paper notes

**Oaken: Fast and Efficient LLM Serving with Online-Offline Hybrid KV Cache Quantization**
Minsu Kim, Seongmin Hong, RyeoWook Ko, Soongyu Choi, Hunjong Lee, Junsoo Kim, Joo-Young Kim,
Jongse Park
**ISCA 2025** ｜ DOI: **not recorded** — the ACM/IEEE record is not reachable by script (403); look it up when citing
Venue evidence (2026-09-02): arXiv `comments` field, verbatim: *"16 pages, 14 figures, and 4 tables"*
Archived here: **arXiv:2503.18599v2** (2025-05-14), 16 pages — **the preprint, not the
published ISCA 2025 version**; the two were **not compared**.

Status: **note ready** ｜ Last updated: 2026-09-09
Tags: `kv-cache` `combined-dtype` `mixed-precision` `dtype-granularity` `analytical-dtype` `accelerator`
How far it was read: **close read of §1–§7** — abstract, introduction, §2 background, §4
(algorithm overview, threshold-based online-offline hybrid quantization, group-shift
quantization, fused dense-and-sparse encoding), §5 accelerator architecture, §6.1–§6.2 (all of
methodology and results incl. Tables 1–4) and §7 related work. Figures 11–14 read for prose
claims; per-bar values not transcribed.


> Original: https://arxiv.org/abs/2503.18599
> The PDF is **not committed** (4.3 MB). Re-download: `curl -sSL -o 2503.18599.pdf https://arxiv.org/pdf/2503.18599`
> Extract text: `python3 extract.py` → `extracted/` (committed, greppable)
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, ISCA 2025 row.

---

## Brief

### 1. Motivation

LLM serving batches requests for throughput, but attention is un-batchable and memory-
bandwidth-bound, and the **KV cache** grows with context until capacity, not compute, is the
limit. KV quantization normally keeps most values at INT4 and outliers at FP16 — but
**online outlier detection is so expensive it cancels the benefit**.

### 2. Overview

An **online–offline hybrid**: outlier *thresholds* are determined offline from calibration,
and only the cheap step — applying those thresholds to pick the quantization scale — happens
online. Adds group-shift quantization plus custom quantization/dequantization engines and
memory-management units that can be attached to any LLM accelerator; demonstrated on the
LPU.

### 3. Pros and cons

**Pros**

- Puts the expensive half of outlier handling offline and keeps only the cheap half online —
a well-targeted answer to the specific reason prior KV quantization did not pay off.
- 1.58× throughput over an A100 at batch 256 with only **0.54% average accuracy loss**
against state-of-the-art KV quantization.
- Packaged as engines that integrate with an existing accelerator rather than a whole new
chip, which makes the result more portable than most.

**Cons**

- Offline thresholds are calibration-dependent: [`P3-LLM`](../P3-LLM/ANALYSIS.md) argues
Oaken's offline calibration is inefficient and forces ~10% of values to stay high-
precision, and reports 1.04% better accuracy at 4-bit KV.
- The arXiv record does not state the venue, so its ISCA 2025 placement here rests on the
source list alone (see the master table's venue note).
- Evaluated in a serving configuration tuned to its own accelerator; sensitivity to batch
size and context length beyond the reported points is not fully mapped.

### 4. Where it applies

The entry point to the **KV-cache** cluster — the biggest single theme in the 2025–26 half
of the corpus. Read before [`Omni-LUT`](../Omni-LUT/ANALYSIS.md),
[`SingularBit`](../SingularBit/ANALYSIS.md) and [`P3-LLM`](../P3-LLM/ANALYSIS.md), all of
which position against it.

---

## Conclusions

<!-- Nothing here yet: the paper has not been read. Replace this with numbered,
     evidence-marked claims on the close read, then move the status to `analysis ready`. -->

**Read in full 2026-09-09.** Three changes, one of them a resolution.

**1. Venue is RESOLVED — the brief's second con is now closed.** The archived PDF carries its
own ACM copyright block: *"ISCA '25, Tokyo, Japan … ACM ISBN 979-8-4007-1261-6/2025/06 …
https://doi.org/10.1145/3695053.3731019"* (**verified**). ISCA 2025 no longer rests on the
source list alone. **`survey/README.md`'s venue note should drop Oaken from the "two entries
with unverified venues" list, leaving only `BitFusion`.** (Not edited — the human maintains it.)

**2. Two headline numbers were mis-attributed in the brief.** It says *"1.58× throughput over
an A100 … with only 0.54% average accuracy loss"*. Per §6.2: the speedup over the **A100 FP16
baseline (vLLM) is 1.79×**; the **1.58× is over QServe** (also running on an A100). And the
accuracy loss **against FP16 is 0.87%**; the 0.54% is the *gap to KVQuant*. The paper's own
abstract makes the same conflation — it reports "1.58× over NVIDIA A100 GPU", which is the
QServe number.

**3. `P3-LLM`'s criticism is substantively right — this entry's earlier "half right" verdict was
too generous and is withdrawn** (revised 2026-09-10, after the close read of
[`P3-LLM`](../P3-LLM/ANALYSIS.md) §VI-B). Its claim is about **effective bitwidth**, and every part
of it checks out: Oaken forces **10 % of values out of the dense path** (outer 4 % + inner 6 %,
§6.1 — **verified**), and that lands Oaken at **4.8 effective bits**, confirmed by **Oaken's own
Table 2** (4.82 / 4.82 / 4.89). P3-LLM's per-head INT4-Asym sits at **4.16** — 4 + (16-bit scale +
4-bit zero-point)/128, a derivation that checks — and still beats Oaken by **1.04 % accuracy** and
on perplexity. *Oaken pays 0.64 more effective bits and loses anyway* is a fair statement.
The **only** imprecision is the phrase "in high precision": Oaken's outliers are **5 bits**, one
wider than its 4-bit inliers, and the real cost is the **sparse COO metadata** (6 index + 1 group +
1 sign bit). That is loose wording, not a wrong claim, and it does not touch the argument.

---

## Method

**Verified** unless marked.

**The problem it names.** Standard KV quantization keeps most values at INT4 and outliers at
FP16. Finding the outliers needs a **topK**, i.e. a sort, **online, per token** — and that cost
"negat[es] the advantages of quantization" (Abstract). Oaken's thesis is that the expensive
half of outlier handling can be moved offline.

**1. Threshold-based online–offline hybrid quantization** (§4.3). Split each per-token KV
vector into **three groups by magnitude**: **outer** (large-magnitude outliers), **middle**
(inliers), **inner** (small-magnitude outliers). The inner group exists so small outliers do
not *vanish* under a scale set by the bulk — a symmetric concern to the usual one. Four
thresholds define the boundaries; **the thresholds are profiled offline**, and only the cheap
step — comparing values against them to pick a scale — runs online. Profiling collects topK
boundaries over ~100 inferences and takes **~10 minutes even for Llama2-70B**, once per model
before serving. Ratios are fixed **globally at outer 4 % / middle 90 % / inner 6 %** for every
model and dataset, justified by §4.1's claim that KV distribution is insensitive to the input.

**2. Group-shift quantization** (§4.4). A group of large-magnitude values quantized uniformly
wastes most of its range. So **subtract the group's offline threshold before quantizing**,
narrowing the span and letting a low bitwidth cover it. Applied to the outer and middle groups.
**Middle → 4-bit, inner and outer → 5-bit.**

**3. Fused dense-and-sparse encoding** (§4.5) — the part that makes the bitwidth work. Inliers
go in a dense matrix; outliers go in **COO** sparse format, with their dense-matrix slots
zeroed. Those zeroed 4-bit slots are then **reused to hold 4 of the outlier's 5 bits**, leaving
the sparse entry to carry 6 index + 1 group + 1 sign = **exactly 8 bits, memory-aligned**. This
cuts an outlier entry from 23 bits to 8 and lets the MMU page dense and sparse matrices
uniformly.

> **Effective bitwidth, derived:** 4 bits per element (dense) + 10 % × 8 bits (sparse) = **4.8**
> — matching the 4.82 reported in Table 2 (`**inferred / not verified**`: the derivation is
> mine; the paper states the result, not the arithmetic).

**4. Hardware** (§5). Not a new chip: **quantization/dequantization engines plus memory
management units integrated into the DMA path** of an existing accelerator (LPU), which is why
the paper claims it "can be integrated with any LLM accelerator". Quant/dequant latency is
**hidden by overlapping and streaming**.

## Key numbers, with their frame

**Frames.** Accuracy on Wikitext2 (PPL) plus PIQA / Winogrande / Hellaswag (zero-shot), eight
LLMs. Hardware is a **simulator extending the LPU simulator**, with RTL in SystemVerilog
verified in VCS and synthesized by Synopsys DC at **1 GHz, TSMC 28 nm**. GPU baselines are
**A100-80GB** (two GPUs with pipeline parallelism for OPT-30B / Mixtral-8x7B / Llama2-70B).
Two Oaken configs: **LPDDR** (256 GB, 1.1 TB/s) and **HBM** (80 GB, 2.0 TB/s). All
quantization baselines run **KV-cache-only 4-bit**, with QServe's and Tender's weight/activation
quantization **disabled for fairness**. **No silicon.**

| Setting | Model | Metric | Baseline | Result | Source |
|---|---|---|---|---|---|
| **Throughput, batch 256** | 6 LLMs, 1K:1K in:out | Avg speedup | **vLLM (A100 FP16)** / **QServe** | Oaken-LPDDR **1.79× / 1.58×** | §6.2 |
| **Accuracy** | 8 LLMs, 4 datasets | Avg accuracy loss | **FP16** | **0.87 %** | §6.2 |
| same | same | Gap to KV-quant baselines | KVQuant / KIVI / QServe | **−0.54 % / −0.32 % / +1.38 %** | §6.2 |
| **Effective bitwidth (the number that settles the Omni-LUT dispute)** | Llama2-7B / 13B / 70B | bits | — | **Oaken 4.82 / 4.82 / 4.89** · KVQuant 4.82 / 4.81 / 5.01 · KIVI 4.99 · Tender 4.07 / 4.07 / 4.10 · Atom 4.25 / 4.25 / 4.63 · QServe 4.25 | **Table 2** |
| PPL | Llama2-7B / 13B / 70B | Wikitext2 | FP16 5.47 / 4.88 / 3.32 | Oaken **5.53 / 4.93 / 3.34**; KVQuant 5.49 / 4.94 / 3.33; KIVI 5.50 / 4.90 / 3.33; Atom 5.62 / 4.98 / 3.37; QServe 5.67 / 5.12 / 3.36; **Tender 6.42 / 5.74 / 4.25** | Table 2 |
| Attention latency | Llama2-7B | Reduction | LPU (same accelerator, no KV quant) | **55.0 % shorter** | §6.2 |
| Quant/dequant cost at batch 64 | Llama2-7B | % of end-to-end latency | — | **1.29 % / 3.23 %**, and both hidden by overlap | §6.2 |
| **Where it loses** | Llama2-13B, batch 16 | Throughput | vLLM, QServe | **Below 8K sequence length, QServe and vLLM beat Oaken** | §6.2, Fig. 13 |
| Long-sequence reach | Llama2-13B | Max sequence | QServe / Oaken-HBM cap at 16K | **Oaken-LPDDR reaches 32K** | §6.2 |
| Area | — | mm² @28 nm | Total compute core **3.971** | Quant engine **0.074 (1.86 %)**, dequant **0.252 (6.35 %)** → **8.21 % overhead** | Table 4 |
| Power | — | W | A100 TDP **400 W** | **222.7 W** (−44.3 %) | §6.2 |
| Group-count ablation | Llama2-7B | PPL / effective bits | 3 groups (4/90/6) = 5.526 @ 4.8 bits | 2 groups 5.804 @ 4.8; 4–5 groups marginally better PPL but **5.6 bits** | Table 3 |
| Offline profiling cost | Llama2-70B | time | — | **~100 inferences, ~10 min**, once per model | §6.1 |

Left blank: per-bar values of Figs. 11–14; the OPT/Mistral/Mixtral effective bitwidths (Table 2
reports them for Llama2 only).

## Cost and requirements

- **Data type.** KV cache only — **`W16A16KV~4.8`**. Weights and activations are **untouched**;
  the paper explicitly disables QServe's and Tender's W/A quantization to keep the comparison
  KV-only. **Oaken's own datapath is FP16** — Table 1 reports "Peak FP16 TFLOPS" (270 for both
  Oaken configs, against the A100's 312) (**verified**).
- **Leaving weights at FP16 is an argued position, not an omission** (§4.1). Fig. 5(a): weight
  memory is **constant in batch size** while the KV cache grows until it dominates device
  memory. Fig. 5(b): 4-bit *weight* quantization gives *"minimal performance improvement"*
  against 4-bit *KV* quantization, *"showing its ineffectiveness in addressing the memory wall
  for batched LLM inference"* (**verified**). This is a **substantive disagreement with the
  weight-quantization line** — [`LUTTensorCore`](../LUTTensorCore/ANALYSIS.md) (`W4A16`),
  [`TransitiveArray`](../TransitiveArray/ANALYSIS.md) (`W4A8`),
  [`OASIS`](../OASIS/ANALYSIS.md) (`W4A4`) — all of which treat weight quantization as the
  lever, with OASIS opening on the 20–90 % dequantization overhead as the cost worth removing.
  The positions are reconcilable by regime (LUT papers: compute-bound prefill and single-batch
  edge decode; Oaken: batch-256 serving) but **no paper states the boundary**. Survey material. Middle group **INT4**, inner and outer groups **INT5**, plus 8 bits of COO metadata
  per outlier.
- **Granularity.** **Per-token vector**, split into three magnitude groups. Scale per group per
  token; **thresholds are global per model**, profiled offline and shared across all tokens,
  layers and datasets. No sub-grouping inside the middle group — that is the contrast with
  KIVI's fine-grained grouping, which is why KIVI sits at 4.99 bits.
- **Outlier mechanism — present, and two-sided.** Both large *and* small magnitude outliers are
  isolated (outer + inner). 10 % of values total. Crucially they are **not kept at FP16** — they
  are 5-bit. What they cost is the sparse-format metadata.
- **Escape hatch.** The 10 % sparse path and its 8 bits/entry of index+group+sign. Weights and
  activations at FP16 throughout. Attention arithmetic itself is not quantized.
- **Retraining: PTQ**, but with a **mandatory per-model offline profiling pass** — ~100
  inferences, ~10 min. Cheap, but it is a deployment step, and the thresholds are model-specific
  even though the group *ratios* are global.
- **What the hardware pays.** 8.21 % of compute-core area (1.86 % quant + 6.35 % dequant).
  Dequantization is 3.4× the area of quantization — it runs on every KV read, quantization only
  on generation.

## Limitations and open questions

**Authors admit:** below 8K sequence length **QServe and vLLM outperform Oaken** (Fig. 13);
Oaken-HBM cannot hold sequences past 16K; on Mixtral-8x7B with GQA and short generations,
quantization baselines including Oaken show "little to no performance gain"; the Conversation
trace's short outputs blunt the advantage. This is unusually candid about the operating range.

**Not admitted:**

1. **The abstract's 1.58× is over QServe, not over the FP16 A100.** It reads "1.58× throughput
   improvement over NVIDIA A100 GPU"; §6.2 shows 1.79× over vLLM and 1.58× over QServe. QServe
   does run on an A100, so it is not false — but it names the smaller of the two numbers against
   the more impressive-sounding baseline.
2. **"0.54 % accuracy loss" is the gap to KVQuant, not to FP16.** Loss against FP16 is 0.87 %.
   The abstract's phrasing ("compared to state-of-the-art KV cache quantization techniques") is
   technically accurate and reliably misread.
3. **Oaken is beaten on accuracy by both KVQuant and KIVI** (by 0.54 % and 0.32 %) at
   essentially the same or slightly higher bitwidth. The defence is that their advantage is
   "offset by the prohibitively high overhead of online sorting" — an argument about *systems
   cost*, not accuracy, and it is not quantified in the same table.
4. **The three-group ratio is fixed globally at 4/90/6 for all eight models**, justified by a
   claim that KV distribution is input-insensitive. Table 3 sweeps group *count* on Llama2-7B
   only; per-model ratio sensitivity across the other seven is not shown.
5. **Tender is used as a baseline and performs badly** (PPL 6.42 vs 5.47 on Llama2-7B, and 4.25
   vs 3.32 on 70B) at 4.07 effective bits. As with `Omni-LUT`, a corpus entry appears here as
   the weak point of the comparison set.
6. **The accelerator is a simulator extension of another paper's simulator** (LPU), with RTL
   synthesized only for the added engines. The 8.21 % overhead figure is post-synthesis; the
   throughput numbers are not.

## Relation to other entries

- **The KV-cache cluster's anchor, and now a settled dispute.**
  [`Omni-LUT`](../Omni-LUT/ANALYSIS.md) claims KIVI, KVQuant and Oaken *"yield a higher average
  KV cache bit width of 4.8–5.0 bits"* because they rely on sparsity-based outlier handling.
  **Oaken's own Table 2 confirms this exactly**: Oaken 4.82–4.89, KVQuant 4.81–5.01, KIVI 4.99.
  Omni-LUT's characterisation is **accurate**, and its 4.25-bit claim puts it at the *Atom /
  QServe* bitwidth point (4.25 in the same table) while claiming Oaken-class accuracy. **That is
  the real comparison to make in the survey**, and neither paper makes it: Omni-LUT vs
  Atom/QServe at iso-bitwidth. `**inferred / not verified**` — the two papers' accuracy
  evaluations use different model sets and are not directly commensurable.
- **[`P3-LLM`](../P3-LLM/ANALYSIS.md)'s criticism**: the "~10 % of values" figure is exact
  (4 % + 6 %), but "high-precision" is wrong — they are 5-bit. Fix the framing before citing.
- **[`Tender`](../Tender/ANALYSIS.md)** is a baseline here and the weakest one, exactly as in
  Omni-LUT. Two independent papers now use it as the floor; worth recording in Tender's entry.
- **Against the LUT thread**: Oaken is the *non*-LUT answer to the same KV pressure —
  dense-and-sparse encoding plus offline thresholds, rather than making KV the binary operand
  of a lookup ([`Omni-LUT`](../Omni-LUT/ANALYSIS.md)). Good paired contrast for §5.6/§5.7.
- **Integration story**: unlike almost everything else in the corpus, Oaken is *engines bolted
  into an existing accelerator's DMA path*, not a new datapath. Closest in spirit to
  [`Ecco`](../Ecco/ANALYSIS.md). This is the corpus's best example of the **low-adoption-barrier**
  end of the spectrum, against [`LUTTensorCore`](../LUTTensorCore/ANALYSIS.md) at the high end.

## For the note

### §1 one-line summary

> Splits each per-token KV vector into three magnitude groups — inliers at INT4, large *and*
> small outliers at INT5 — using **thresholds profiled offline** so the only online work is a
> comparison rather than a topK sort, then reuses the zeroed dense slots left behind by the
> outliers to hold 4 of their 5 bits so each sparse entry lands on exactly 8 aligned bits,
> giving ~4.8 effective bits and 1.79× throughput over an FP16 A100 as engines bolted into an
> existing accelerator's DMA path.

### Proposed values on their four axes

| Axis | Proposed | Evidence (one line) |
|---|---|---|
| **Level** | **`ALGO+ARCH`** | The three-group threshold scheme, group-shift and fused encoding are the algorithm; the quant/dequant engines and MMU are the architecture. |
| **Q-oriented** | `Q-ORIENTED` | The engines exist only to produce and consume this format; remove quantization and nothing is left. |
| **Data type** | **`INT4` + `INT5` + `MIXED`** | Middle group INT4, inner/outer INT5 (§4.4), plus COO metadata. Uniform quantization within each group — **not** `VQ` or `LUT`. |
| **Generation** | **`G3`** | KV-cache thread, which is G3-specific, plus the outlier thread. No new numeric format — this is G3 by *problem*, not by format design. |
| **Optimization** (free text) | `KV cache` `outlier-aware` `offline-threshold-profiling` `group-shift` `dense-and-sparse` `COO` `three-group` `DMA-integrated` `LPDDR` | — |

### Proposed venue-list row

```
| [x] | [Oaken: Fast and Efficient LLM Serving with Online-Offline Hybrid KV Cache Quantization](https://arxiv.org/abs/2503.18599) | ALGO+ARCH | Q | `INT4` `INT5` `MIXED` | G3 | `KV cache` `outlier-aware` `group-shift` `dense-and-sparse` | Three magnitude groups with offline-profiled thresholds so online work is a compare not a topK; zeroed dense slots reused to hold outlier bits → 8-bit aligned sparse entries, ~4.8 effective bits |
```

### §4 fairness verdict

**Unusually fair on setup, and unusually candid about where it loses; the abstract is the
weakest part.**

- **Iso-task ✓** — all quantization baselines run **KV-cache-only 4-bit**, and QServe's and
  Tender's weight/activation quantization is **deliberately disabled** so the comparison isolates
  KV. That is a real fairness effort and rare in this corpus.
- **Iso-capability ✓** — GPU baselines get two A100s with pipeline parallelism for the large
  models "to keep computation capability and memory bandwidth consistent"; Tender is aligned to
  A100 memory and compute.
- **Iso-node ✗ / not claimed** — Oaken is 28 nm post-synthesis against A100 silicon at 7 nm. The
  paper does not make a per-area claim, only a **power** one (222.7 W vs 400 W TDP), which is
  the safer framing but still crosses nodes.
- **Evidence levels must not be pooled**: the 8.21 % area figure is **post-synthesis**; every
  throughput number is a **simulator** extending another paper's simulator.
- **Operating range is disclosed** — Oaken *loses* to vLLM and QServe below 8K sequence length,
  and gains little on GQA models with short generations. Stated plainly in §6.2. Any survey
  claim must carry "long sequence, large batch".
- **The abstract overstates twice**: 1.58× is over QServe not the FP16 A100 (1.79× is the FP16
  number), and 0.54 % is the gap to KVQuant not the loss vs FP16 (0.87 %). **Cite §6.2, not the
  abstract.**

## Abstract (verbatim, arXiv:2503.18599v2)

> Modern Large Language Model serving system batches multiple requests to achieve high
> throughput, while batching attention operations is challenging, rendering memory bandwidth
> a critical bottleneck. The community relies on high-end GPUs with multiple high-bandwidth
> memory channels. Unfortunately, HBM's high bandwidth often comes at the expense of limited
> memory capacity, which reduces core utilization and increases costs. Recent advancements
> enabling longer contexts for LLMs have substantially increased the key-value cache size,
> further intensifying the pressures on memory capacity. The literature has explored KV
> cache quantization techniques, which commonly use low bitwidth for most values,
> selectively using higher bitwidth for outlier values. While this approach helps achieve
> high accuracy and low bitwidth simultaneously, it comes with the limitation that cost for
> online outlier detection is excessively high, negating the advantages. We propose Oaken,
> an acceleration solution that achieves high accuracy and high performance simultaneously
> through co-designing algorithm and hardware. To effectively find a sweet spot in the
> accuracy-performance trade-off space of KV cache quantization, Oaken employs an online-
> offline hybrid approach, setting outlier thresholds offline, which are then used to
> determine the quantization scale online. To translate the proposed algorithmic technique
> into tangible performance gains, Oaken also comes with custom quantization engines and
> memory management units that can be integrated with any LLM accelerators. We built an
> Oaken accelerator on top of an LLM accelerator, LPU, and conducted a comprehensive
> evaluation. Our experiments show that for a batch size of 256, Oaken achieves up to 1.58x
> throughput improvement over NVIDIA A100 GPU, incurring a minimal accuracy loss of only
> 0.54\% on average, compared to state-of-the-art KV cache quantization techniques.
