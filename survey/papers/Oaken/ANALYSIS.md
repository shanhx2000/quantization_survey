# Oaken — paper notes

**Oaken: Fast and Efficient LLM Serving with Online-Offline Hybrid KV Cache Quantization**
Minsu Kim, Seongmin Hong, RyeoWook Ko, Soongyu Choi, Hunjong Lee, Junsoo Kim, Joo-Young Kim,
Jongse Park
**ISCA 2025** ｜ DOI: **not recorded** — the ACM/IEEE record is not reachable by script (403); look it up when citing
Venue evidence (2026-09-02): arXiv `comments` field, verbatim: *"16 pages, 14 figures, and 4 tables"*
Archived here: **arXiv:2503.18599v2** (2025-05-14), 16 pages — **the preprint, not the
published ISCA 2025 version**; the two were **not compared**.

Status: **brief ready** ｜ Last updated: 2026-09-02
Tags: `kv-cache` `combined-dtype` `mixed-precision` `dtype-granularity` `analytical-dtype` `accelerator`
How far it was read: **abstract, introduction, section map, headline result sentences and
conclusion.** The method and evaluation sections were **not** read line by line, and no numbers
have been transcribed into the table below with their full frame — so this stays `brief ready`.
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

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

**Not read in full.** The brief above is the current state of knowledge; nothing below it
has been filled in, and no number from this paper may be cited without reading the
evaluation section first.

---

## Method

<!-- what is quantized (weights / activations / KV cache), PTQ vs QAT vs co-designed
     hardware, granularity and group size, numeric format, and what hardware it assumes -->

## Key numbers, with their frame

<!-- a number without its frame does not go into the survey: model, task, baseline,
     bit-width, granularity, and which hardware the speedup was measured or simulated on -->

| Setting | Model | Metric | Baseline | Result | Source |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## Cost and requirements

<!-- silicon area / energy numbers, the simulator or synthesis flow used, whether the
     speedup needs the proposed hardware or runs on stock GEMM -->

## Limitations and open questions

## Relation to other entries

## Note from the source list

> _(no keywords recorded in the source CSV)_


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
