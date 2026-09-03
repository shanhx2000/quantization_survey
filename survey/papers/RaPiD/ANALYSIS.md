# RaPiD — paper notes

**RaPiD: AI Accelerator for Ultra-Low Precision Training and Inference**
Authors: **not transcribed** — a large industrial author list; read it off page 1 of the PDF before citing.
**ISCA 2021**, pp. 153-166 ｜ DOI: **10.1109/ISCA52012.2021.00021**
Publication info verified 2026-09-02: venue, year **and DOI** all read out of the archived
PDF's own text (IEEE proceedings banner; the DOI was grepped for, not assumed); page range
from the ACM DL / IEEE Xplore record.
Archived here: the **published IEEE version** (the page-1 IEEE proceedings banner is present in the extracted text), 14 pages.

Status: **brief ready** ｜ Last updated: 2026-09-02
Tags: `analytical-dtype` `mixed-precision` `multi-bitwidth-hw` `training` `accelerator`
How far it was read: **abstract, introduction, section map, headline result sentences and
conclusion.** The method and evaluation sections were **not** read line by line, and no numbers
have been transcribed into the table below with their full frame — so this stays `brief ready`.
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> Publisher record: https://ieeexplore.ieee.org/document/9499865/
> **There is no arXiv version** (arXiv API title search, 2026-09-02). The PDF was downloaded by a
> human and filed through [`survey/uploads/`](../../uploads/) — the sanctioned route when the
> arXiv-only rule leaves a paper unreachable; see
> [`Notes-002`](../../../Claude/notes/Notes-002-paper-source-access.md).
> The PDF is **not committed** (15.1 MB) and **cannot be re-downloaded by script** —
> both publishers 403. Re-extract with `python3 extract.py` → `extracted/` (committed).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, ISCA 2021 row.

---

## Brief

### 1. Motivation

AI accelerators must keep scaling across generations, and the error-resilience of AI
workloads makes **precision scaling** the most direct lever. The paper is IBM's realisation
of a precision-scaling roadmap in silicon.

### 2. Overview

A fabricated **4-core chip in 7 nm EUV, 36 mm²**, supporting a spectrum of precisions in one
datapath: 16- and 8-bit floating point (including hybrid FP8) and 4- and 2-bit fixed point.
Evaluated with a performance model **calibrated to within 1% of chip measurements**, then
projected to a 768 TFLOP 4-chip, 32-core-per-chip system.

### 3. Pros and cons

**Pros**

- Real fabricated silicon with measured peaks — **3.5 TFLOPS/W in HFP8, 16.5 TOPS/W in
INT4** — which makes it one of the few hard reference points in the corpus.
- Covers **both training and inference** in one architecture (FP8 training, INT4 inference),
which almost nothing else here does.
- The 1%-calibrated performance model is exactly the methodological standard the survey
should hold simulation-based papers to.

**Cons**

- INT2 is supported in hardware but not evaluated, because the models still lose ~2%
accuracy — an honest admission that the bottom of the precision range was not usable.
- Speedups at low precision are limited by the fraction of operations that must stay FP16;
the end-to-end gains (1.2–1.8×) are much smaller than the peak-TOPS ratios suggest.
- The formats supported are adopted from prior algorithmic work, so the contribution is the
chip, not the data type.

### 4. Where it applies

The industrial anchor for **multi-bitwidth hardware** and the only serious **training**
hardware entry. Its gap between peak and end-to-end numbers is a caution worth quoting
whenever the survey cites peak TOPS/W.

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

> **Keywords:** a 4-core AI accelerator chip supporting a spectrum of precisions, namely, 16 and 8-bit floating-point and 4 and 2-bit fixed-point. Also Support Hybrid-FP8.


## Abstract (verbatim, from the archived PDF)

> The growing prevalence and computational demands of Artificial Intelligence (AI) workloads
> has led to widespread use of hardware accelerators in their execution. Scaling the
> performance of AI accelerators across generations is pivotal to their success in
> commercial deployments. The intrinsic error-resilient nature of AI workloads present a
> unique opportunity for performance/energy improvement through precision scaling. Motivated
> by the recent algorithmic advances in precision scaling for inference and training, we
> designed R A P I D1 , a 4-core AI accelerator chip supporting a spectrum of precisions,
> namely, 16 and 8-bit floating-point and 4 and 2-bit fixed-point. The 36mm2 R A P I D chip
> fabricated in 7nm EUV technology delivers a peak 3.5 TFLOPS/W in HFP8 mode and 16.5 TOPS/W
> in INT4 mode at nominal voltage. Using a performance model calibrated to within 1% of the
> measurement results, we evaluated DNN inference using 4-bit fixed-point representation for
> a 4-core 1 R A P I D chip system and DNN training using 8-bit floating point
> representation for a 768 TFLOPs AI system comprising 4 32-core R A P I D chips. Our
> results show INT4 inference for batch size of 1 achieves 3 - 13.5 (average 7) TOPS/W and
> FP8 training for a mini-batch of 512 achieves a sustained 102 - 588 (average 203) TFLOPS
> across a wide range of applications.
