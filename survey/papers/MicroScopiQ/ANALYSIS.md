# MicroScopiQ — paper notes

**MicroScopiQ: Accelerating Foundational Models through Outlier-Aware Microscaling Quantization**
Akshat Ramachandran, Souvik Kundu, Tushar Krishna
**ISCA 2025** ｜ DOI: **not recorded** — the ACM/IEEE record is not reachable by script (403); look it up when citing
Venue evidence (2026-09-02): arXiv `comments` field, verbatim: *"ISCA 2025"*
Archived here: **arXiv:2411.05282v4** (2025-04-29), 17 pages — **the preprint, not the
published ISCA 2025 version**; the two were **not compared**.

Status: **brief ready** ｜ Last updated: 2026-09-02
Tags: `analytical-dtype` `dtype-granularity` `combined-dtype` `mixed-precision` `accelerator`
How far it was read: **abstract, introduction, section map, headline result sentences and
conclusion.** The method and evaluation sections were **not** read line by line, and no numbers
have been transcribed into the table below with their full frame — so this stays `brief ready`.
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> Original: https://arxiv.org/abs/2411.05282
> The PDF is **not committed** (9.3 MB). Re-download: `curl -sSL -o 2411.05282.pdf https://arxiv.org/pdf/2411.05282`
> Extract text: `python3 extract.py` → `extracted/` (committed, greppable)
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, ISCA 2025 row.

---

## Brief

### 1. Motivation

Outlier-aware co-designs are stuck in a mutual exclusivity: keep outliers at high precision
and you get accuracy but **unaligned memory and complex PEs**; quantize outliers like
everything else and you get hardware efficiency but lose accuracy. The paper's table makes
the trade explicit — prior Group A reaches 18.17 effective bits, Group B drops to 2 bits
with low accuracy.

### 2. Overview

Use **pruning to pay for outliers**: keep outliers at higher precision, and prune a fraction
of the least important weights so the freed bits absorb the extra outlier bits — which keeps
memory **aligned** at a low effective bitwidth (2.36 bits). Hardware is a systolic array of
multi-precision INT PEs plus a network-on-chip, **ReCoN**, that hides the complexity of
routing high-precision outliers. Explicitly assumes **no locality** of outlier weights.

### 3. Pros and cons

**Pros**

- The alignment argument is the strongest part: it gets Group-A accuracy at Group-B-like
effective bitwidth and simple PEs, which is precisely the exclusivity it set out to break.
- Dropping the outlier-locality assumption is a direct and well-aimed critique of
[`OliVe`](../OliVe/ANALYSIS.md); it makes the method applicable across foundation models
rather than models with convenient outlier structure.
- Broad and strong evaluation: up to 3× faster inference and 2× lower energy, ≥8% accuracy
over OliVe at lower precision, and <1% drop at W4A16 with usable W2A16 results. Code is
released.

**Cons**

- Trades pruning error for outlier fidelity — the accuracy budget is spent, not created, and
how that trade behaves at extreme sparsity is not fully mapped.
- The ReCoN NoC is an added structure whose cost is amortized over the array; on a smaller
design that overhead could dominate.
- Comparisons are against methods with different calibration budgets (it notes OmniQuant
needs 5–6× its runtime), so accuracy-per-effort comparisons need care.

### 4. Where it applies

The current head of the **outlier / combined-data-type** thread and the strongest single
argument that **memory alignment** is the property that decides whether outlier handling is
practical. Also a core **microscaling (§1.2 + granularity)** entry.

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


## Abstract (verbatim, arXiv:2411.05282v4)

> Quantization of foundational models (FMs) is significantly more challenging than
> traditional DNNs due to the emergence of large magnitude values called outliers. Existing
> outlier-aware algorithm-architecture co-design techniques either use mixed-precision,
> retaining outliers at high precision but compromise hardware efficiency, or quantize
> inliers and outliers at the same precision, improving hardware efficiency at the cost of
> accuracy. To address this mutual exclusivity, we propose MicroScopiQ, a novel co-design
> technique that leverages pruning to complement outlier-aware quantization. MicroScopiQ
> retains outliers at higher precision while pruning a certain fraction of least important
> weights to distribute the additional outlier bits; ensuring high accuracy, aligned memory
> and hardware efficiency. We design a high-throughput, low overhead accelerator
> architecture composed of multi-precision INT processing elements and a network-on-chip
> called ReCoN that efficiently abstracts the complexity of supporting high-precision
> outliers. Additionally, unlike prior techniques, MicroScopiQ does not assume any locality
> of outlier weights, enabling applicability to a broad range of FMs. Extensive experiments
> across diverse quantization settings demonstrate that MicroScopiQ achieves state-of-the-
> art quantization accuracy, while delivering up to 3x faster inference and 2x lower energy
> consumption compared to existing alternatives. Code is available at:
> https://github.com/georgia-tech-synergy-lab/MicroScopiQ-LLM-Quantization
