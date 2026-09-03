# OLAccel — paper notes

**Energy-Efficient Neural Network Accelerator Based on Outlier-Aware Low-Precision Computation**
Eunhyeok Park, Dongyoung Kim, Sungjoo Yoo
**ISCA 2018**, pp. 688-698 ｜ DOI: **10.1109/ISCA.2018.00063**
Publication info verified 2026-09-02: venue, year **and DOI** all read out of the archived
PDF's own text (IEEE proceedings banner; the DOI was grepped for, not assumed); page range
from the ACM DL record.
Archived here: the **published IEEE version** (the page-1 IEEE proceedings banner is present in the extracted text), 11 pages.

Status: **brief ready** ｜ Last updated: 2026-09-02
Tags: `analytical-dtype` `combined-dtype` `mixed-precision` `dtype-granularity` `accelerator`
How far it was read: **abstract, introduction, section map, headline result sentences and
conclusion.** The method and evaluation sections were **not** read line by line, and no numbers
have been transcribed into the table below with their full frame — so this stays `brief ready`.
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> Publisher record: https://dl.acm.org/doi/10.1109/ISCA.2018.00063
> **There is no arXiv version** (arXiv API title search, 2026-09-02). The PDF was downloaded by a
> human and filed through [`survey/uploads/`](../../uploads/) — the sanctioned route when the
> arXiv-only rule leaves a paper unreachable; see
> [`Notes-002`](../../../Claude/notes/Notes-002-paper-source-access.md).
> The PDF is **not committed** (0.9 MB) and **cannot be re-downloaded by script** —
> both publishers 403. Re-extract with `python3 extract.py` → `extracted/` (committed).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, ISCA 2018 row.

---

## Brief

### 1. Motivation

Very deep networks (ResNet-101, DenseNet-121) resist 4-bit quantization because a small
number of large-magnitude values — **outliers** — blow up the quantization range. The
observation that carries the whole outlier line of work: keeping just ~3% of values at high
precision restores accuracy at <1% loss while the other 97% goes to 4 bits.

### 2. Overview

An accelerator built on 4-bit MAC units that handles the sparse high-precision outliers
separately: outlier *weights* get an extra MAC per SIMD lane (so the common case of one
outlier per lane costs no extra cycle), outlier *activations* go to dedicated high-precision
MACs, and both paths update partial sums in a pipeline to avoid coherence problems.

### 3. Pros and cons

**Pros**

- The origin point of outlier-aware quantization architecture — every later entry in that
thread ([`OliVe`](../OliVe/ANALYSIS.md), [`MicroScopiQ`](../MicroScopiQ/ANALYSIS.md),
[`OASIS`](../OASIS/ANALYSIS.md)) is answering it.
- Energy wins are substantial and honestly attributed: 43.5–62.2% versus a 16-bit zero-aware
accelerator, **mostly from DRAM and on-chip memory**, not from the MACs.
- Splitting weight and activation outlier handling into two different mechanisms is a
genuinely thoughtful piece of design, not a uniform bolt-on.

**Cons**

- Outliers are stored sparsely, so the design needs a coordinate list and irregular access —
exactly the cost [`OliVe`](../OliVe/ANALYSIS.md) later attacks as unaligned and hardware-
unfriendly.
- Evaluated on CNNs of its era; whether the 3% outlier budget holds for transformers is not
addressed here, and later LLM work suggests the outlier structure differs.
- [`DRQ`](../DRQ/ANALYSIS.md) reports OLAccel losing up to ~5% accuracy on compact models
such as MobileNet-v2 — a weakness not visible in this paper's own benchmark set.

### 4. Where it applies

The anchor of the **§2.2b outlier-compression** box, and the historical baseline for both
accuracy and hardware-overhead comparisons in outlier-aware work.

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

> **Keywords:** Dense and low-precision computations for a majority of data while efficiently handling a small number of sparse and high-precision outliers.


## Abstract (verbatim, from the archived PDF)

> Owing to the presence of large values, which we call outliers, conventional methods of
> quantization fail to achieve significantly low precision, e.g., four bits, for very deep
> neural networks, such as ResNet-101. In this study, we propose a hardware accelerator,
> called the outlier-aware accelerator (OLAccel). It performs dense and low-precision
> computations for a majority of data (weights and activations) while efficiently handling a
> small number of sparse and highprecision outliers (e.g., amounting to 3% of total data).
> The OLAccel is based on 4-bit multiply-accumulate (MAC) units and handles outlier weights
> and activations in a different manner. For outlier weights, it equips SIMD lanes of MAC
> units with an additional MAC unit, which helps avoid cycle overhead for the majority of
> outlier occurrences, i.e., a single occurrence in the SIMD lanes. The OLAccel performs
> computations using outlier activation on dedicated, high-precision MAC units. In order to
> avoid coherence problem due to updates from lowand high-precision computation units, both
> units update partial sums in a pipelined manner. Our experiments show that the OLAccel can
> reduce by 43.5% (27.0%), 56.7% (36.3%), and 62.2% (49.5%) energy consumption for AlexNet,
> VGG-16, and ResNet-18, respectively, compared with a 16-bit (8-bit) state-of-the-art zero-
> aware accelerator. The energy gain mostly comes from the memory components, the DRAM, and
> on-chip memory due to reduced precision.
