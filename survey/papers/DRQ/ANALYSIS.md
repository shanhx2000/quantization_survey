# DRQ — paper notes

**DRQ: Dynamic Region-Based Quantization for Deep Neural Network Acceleration**
Zhuoran Song, Bangqi Fu, Feiyang Wu, Zhaoming Jiang, Li Jiang, Naifeng Jing, Xiaoyao Liang
**ISCA 2020**, pp. 1010-1021 ｜ DOI: **10.1109/ISCA45697.2020.00086**
Publication info verified 2026-09-02: venue, year **and DOI** all read out of the archived
PDF's own text (IEEE proceedings banner; the DOI was grepped for, not assumed); page range
from the ACM DL record.
Archived here: the **published IEEE version** (the page-1 IEEE proceedings banner is present in the extracted text), 12 pages.

Status: **brief ready** ｜ Last updated: 2026-09-02
Tags: `analytical-dtype` `mixed-precision` `dtype-granularity` `multi-bitwidth-hw` `accelerator`
How far it was read: **abstract, introduction, section map, headline result sentences and
conclusion.** The method and evaluation sections were **not** read line by line, and no numbers
have been transcribed into the table below with their full frame — so this stays `brief ready`.
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> Publisher record: https://dl.acm.org/doi/10.1109/ISCA45697.2020.00086
> **There is no arXiv version** (arXiv API title search, 2026-09-02). The PDF was downloaded by a
> human and filed through [`survey/uploads/`](../../uploads/) — the sanctioned route when the
> arXiv-only rule leaves a paper unreachable; see
> [`Notes-002`](../../../Claude/notes/Notes-002-paper-source-access.md).
> The PDF is **not committed** (0.4 MB) and **cannot be re-downloaded by script** —
> both publishers 403. Re-extract with `python3 extract.py` → `extracted/` (committed).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, ISCA 2020 row.

---

## Brief

### 1. Motivation

Quantization applied at network or layer level is too coarse to exploit; applied to weights
only, it ignores that the *input feature map* varies in how much precision it needs. The
paper's finding is that accuracy-critical ("sensitive") values are not scattered — they
**cluster into contiguous regions**.

### 2. Overview

A dynamic, region-based scheme: an algorithm identifies sensitive regions in each input
feature map at runtime and assigns higher precision (INT8) there and lower (INT4) elsewhere,
executed by a **variable-speed mixed-precision convolution array** sized so both precisions
keep the array busy. Threshold and region size are tuned by design-space exploration (e.g.
4×16 regions, threshold 0.025).

### 3. Pros and cons

**Pros**

- Introduces a granularity nobody had used — **spatial regions of the activation map** — and
shows it is the right one, since sensitivity is spatially clustered.
- Beats its two natural competitors on both axes at similar area: 92%/72% performance/energy
over Eyeriss, and 21%/33% over [`OLAccel`](../OLAccel/ANALYSIS.md) **with 3% better
accuracy**.
- Metadata cost is honestly reported and genuinely small (~2 KB for ResNet-18).

**Cons**

- Region detection runs online, so its cost and the pipeline stalls it causes are intrinsic;
the paper reports a stall ratio and tunes around it rather than eliminating it.
- CNN-shaped throughout — the array prioritizes 3×3 kernels, and "regions of a feature map"
has no direct analogue in transformer activations.
- Threshold and region size are hyperparameters swept per network; no automatic selection is
offered.

### 4. Where it applies

The best example in the corpus of **granularity as the contribution** (§2.2 fine-grained).
Pair with [`Tender`](../Tender/ANALYSIS.md) and [`LightNobel`](../LightNobel/ANALYSIS.md),
which pick channel- and token-wise granularity for the same reason.

---

## Conclusions

**Not read in full.** The brief above is the current state of knowledge; nothing below it
has been filled in, and no number from this paper may be cited without reading the
evaluation section first.

---

## Method

## Key numbers, with their frame

| Setting | Model | Metric | Baseline | Result | Source |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

## Cost and requirements

## Limitations and open questions

## Relation to other entries

## Note from the source list

> **Keywords:** a dynamic region-based quantization, change the precision of model based on the sensitive regions in the feature map


## Abstract (verbatim, from the archived PDF)

> Quantization is an effective technique for Deep Neural Network (DNN) inference
> acceleration. However, conventional quantization techniques are either applied at network
> or layer level that may fail to exploit fine-grained quantization for further speedup, or
> only applied on kernel weights without paying attention to the feature map dynamics that
> may lead to lower NN accuracy. In this paper, we propose a dynamic region-based
> quantization, namely DRQ, which can change the precision of a DNN model dynamically based
> on the sensitive regions in the feature map to achieve greater acceleration while
> reserving better NN accuracy. We propose an algorithm to identify the sensitive regions
> and an architecture that utilizes a variable-speed mixedprecision convolution array to
> enable the algorithm with better performance and energy efficiency. Our experiments on a
> wide variety of networks show that compared to a coarse-grained quantization accelerator
> like “Eyeriss”, DRQ can achieve 92% performance gain and 72% energy reduction with less
> then 1% accuracy loss. Compared to the state-of-the-art mixed-precision quantization
> accelerator “OLAccel”, DRQ can also achieve 21% performance gain and 33% energy reduction
> with 3% prediction accuracy improvement which is quite impressive for inference.
