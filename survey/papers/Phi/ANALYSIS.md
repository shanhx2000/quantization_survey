# Phi — paper notes

**Phi: Leveraging Pattern-based Hierarchical Sparsity for High-Efficiency Spiking Neural Networks**
Chiyue Wei, Bowen Duan, Cong Guo, Jingyang Zhang, Qingyue Song, Hai "Helen" Li, Yiran Chen
**ISCA 2025** ｜ DOI: **10.1145/3695053.3731035**
Venue evidence (2026-09-02): arXiv `comments` field, verbatim: *"ISCA 2025"*
Archived here: **arXiv:2505.10909v1** (2025-05-16), 14 pages — **the preprint, not the
published ISCA 2025 version**; the two were **not compared**.

Status: **brief ready** ｜ Last updated: 2026-09-02
Tags: `non-analytical-dtype` `accelerator`
How far it was read: **abstract, introduction, section map, headline result sentences and
conclusion.** The method and evaluation sections were **not** read line by line, and no numbers
have been transcribed into the table below with their full frame — so this stays `brief ready`.
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> Original: https://arxiv.org/abs/2505.10909
> The PDF is **not committed** (1.3 MB). Re-download: `curl -sSL -o 2505.10909.pdf https://arxiv.org/pdf/2505.10909`
> Extract text: `python3 extract.py` → `extracted/` (committed, greppable)
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, ISCA 2025 row.

---

## Brief

### 1. Motivation

Spiking neural networks are efficient because activations are binary and mostly zero, and
existing SNN accelerators exploit that by skipping zeros. But bit-level sparsity is not the
whole story: the paper observes that **spike activations fall into recurring patterns**,
which zero-skipping alone leaves on the table.

### 2. Overview

A two-level sparsity hierarchy. **Level 1** replaces each activation vector with a **pre-
defined pattern** chosen by k-means, so its product with the weights can be **precomputed
offline** — removing most runtime computation. **Level 2** is an element-wise-sparse
correction matrix that fixes the mismatch, kept highly sparse by pattern-aware fine-tuning.
A dedicated architecture generates and consumes both levels on the fly.

### 3. Pros and cons

**Pros**

- Reframes sparsity as *pattern redundancy* rather than zero-counting, and the numbers back
it: Level-2 element sparsity reaches 96.80% against 83% original bit sparsity.
- The offline-precomputation trick is a genuine structural win — it moves work out of the
inference loop entirely, not merely skips it.
- 3.45× speedup and 4.93× energy efficiency over state-of-the-art SNN accelerators, with
much larger margins against older SNN ASICs.

**Cons**

- Needs **pattern-aware fine-tuning** to keep Level 2 sparse, so it is not a drop-in for an
existing trained SNN.
- The paper concedes DRAM energy is *not* significantly reduced — precomputed pattern-weight
products add memory traffic, and only ~27.73% of them are used per tile.
- SNN-only, and its 'codebook of activation patterns' is a data representation for spikes,
not a numeric format — it sits at the edge of this survey's taxonomy.

### 4. Where it applies

Outside the data-type axis proper, but a legitimate **non-analytical / codebook** exhibit:
k-means patterns standing in for activation vectors is vector quantization by another name.
Pair with [`ELSA`](../ELSA/ANALYSIS.md) as the corpus's two SNN entries.

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


## Abstract (verbatim, arXiv:2505.10909v1)

> Spiking Neural Networks (SNNs) are gaining attention for their energy efficiency and
> biological plausibility, utilizing 0-1 activation sparsity through spike-driven
> computation. While existing SNN accelerators exploit this sparsity to skip zero
> computations, they often overlook the unique distribution patterns inherent in binary
> activations. In this work, we observe that particular patterns exist in spike activations,
> which we can utilize to reduce the substantial computation of SNN models. Based on these
> findings, we propose a novel \textbf{pattern-based hierarchical sparsity} framework,
> termed \textbf{\textit{Phi}}, to optimize computation. \textit{Phi} introduces a two-level
> sparsity hierarchy: Level 1 exhibits vector-wise sparsity by representing activations with
> pre-defined patterns, allowing for offline pre-computation with weights and significantly
> reducing most runtime computation. Level 2 features element-wise sparsity by complementing
> the Level 1 matrix, using a highly sparse matrix to further reduce computation while
> maintaining accuracy. We present an algorithm-hardware co-design approach.
> Algorithmically, we employ a k-means-based pattern selection method to identify
> representative patterns and introduce a pattern-aware fine-tuning technique to enhance
> Level 2 sparsity. Architecturally, we design \textbf{\textit{Phi}}, a dedicated hardware
> architecture that efficiently processes the two levels of \textit{Phi} sparsity on the
> fly. Extensive experiments demonstrate that \textit{Phi} achieves a $3.45\times$ speedup
> and a $4.93\times$ improvement in energy efficiency compared to state-of-the-art SNN
> accelerators, showcasing the effectiveness of our framework in optimizing SNN computation.
