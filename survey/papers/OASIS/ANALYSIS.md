# OASIS — paper notes

**OASIS: Outlier-Aware LUT-Based GEMM with Dual-Side Quantization for LLM Inference Acceleration**
Xueying Wu, Baijun Zhou, Zhihui Gao, Yuzhe Fu, Qilin Zheng, Yintao He, Hai Li
**ISCA 2026** (2026 ACM/IEEE 53rd Annual International Symposium on Computer Architecture),
pp. 307–321 ｜ DOI: **10.1109/ISCA66397.2026.00036**
Publication info verified 2026-09-02 from the **official ISCA 2026 proceedings package**
(title, authors, pages, DOI and abstract all read from its `assets/data/data.js`).
Archived here: **the published proceedings PDF** (`506501a307.pdf`, 15 pages) — not a preprint.

Status: **brief ready** ｜ Last updated: 2026-09-02
Tags: `lut-accelerator` `non-analytical-dtype` `combined-dtype` `mixed-precision` `accelerator`
How far it was read: **abstract, introduction, section map, headline result sentences and
conclusion.** The method and evaluation sections were **not** read line by line, and no numbers
have been transcribed into the table below with their full frame — so this stays `brief ready`.
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> The PDF is **not committed** (1.2 MB). It came from the proceedings package a human
> supplied, now archived at [`archieve/ISCA 2026.zip`](../../../archieve/), entry `pdfs/5065-3nexm57sBmVa6MJtFTiSrb/506501a307/506501a307.pdf`.
> **There is no public URL for it** — this is not an arXiv paper. Re-extract with
> `python3 extract.py` → `extracted/` (committed, greppable).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, 2026 row.

---

## Brief

### 1. Motivation

LLM quantization is caught between three bad options: weight-only quantization pays a
**dequantization cost that can be 20–90% of GEMM runtime**; integer weight-and-activation
quantization is cheap but loses quality; and non-uniform weight-and-activation quantization
fits LLM distributions best but **cannot run on conventional low-precision units at all**.

### 2. Overview

A LUT-based architecture that executes GEMM between **non-uniformly quantized weights AND
activations** — dual-side — with no dequantization. The enabling mechanism is **precomputed
Cartesian-Product LUTs**, giving a 64× smaller table and 1024× more parallelism than prior
LUT GEMM. Accuracy under aggressive activation quantization is protected by keeping the top
0.5% and bottom 0.5% of activations in FP16 on a parallel error-compensation path, fed by
**Orizuru**, a top-k detection engine.

### 3. Pros and cons

**Pros**

- Dual-side non-uniform quantization is the part nobody had made work in hardware; the
Cartesian-product table is what makes it tractable rather than a combinatorial blow-up.
- Two parallel branches — LUT GEMM for inliers, FP16 compensation for outliers — is a clean
separation that keeps the common path uniform.
- 1.94% average accuracy drop from FP16, **6.34% better than Atom**, with 3.00× speedup and
1.44× energy efficiency over the FIGLUT accelerator.

**Cons**

- Top-k outlier detection is an online cost on every activation tensor; Orizuru is optimized
(its min-tree initialization saves 50% of comparisons) but it is still dedicated hardware
that must keep up with the datapath.
- Accuracy degrades noticeably at the aggressive end — 2.05% at W4A4 but **5.90% at W4A3** —
so the usable operating range is narrower than the headline suggests.
- Compared against LUT and INT-WAQ baselines; no direct comparison against the microscaling
line ([`MicroScopiQ`](../MicroScopiQ/ANALYSIS.md)) that attacks the same accuracy problem
differently.

### 4. Where it applies

The 2026 head of the **LUT + non-analytical data type** thread, and the first to push non-
uniform quantization to *both* GEMM operands. Read directly after
[`LUTTensorCore`](../LUTTensorCore/ANALYSIS.md).

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

## Abstract (verbatim, ISCA 2026 proceedings)

> Large language models (LLMs) have demonstrated impressive capabilities across a wide range
> of applications, but demand substantial memory and compute resources during inference.
> Existing quantization methods expose a trade-off between efficiency and accuracy: weight-
> only quantization (WOQ) incurs costly dequantization overheads, while integer weight-and-
> activation quantization (INT-WAQ) reduces precision and degrades model quality. Non-
> uniform weight-and-activation quantization (NU-WAQ) better captures the distributions of
> LLM weights and activations, yet remains incompatible with conventional low-precision
> compute units. This paper presents OASIS, a lookup table (LUT)-based architecture that
> enables efficient general matrix multiplication (GEMM) between non-uniformly quantized
> weights and activations without requiring dequantization. OASIS employs precomputed
> Cartesian product LUTs, achieving a 64× reduction in LUT size and enabling 1024× higher
> computational parallelism compared to existing LUT-based GEMM methods. To preserve
> accuracy under aggressive activation quantization, OASIS introduces an outlier-aware
> quantization scheme with concurrent LUT-based GEMM and error compensation for outliers.
> Furthermore, we design Orizuru, an efficient top-k detection engine for real-time
> activation outlier identification. According to extensive evaluations, OASIS incurs an
> average accuracy drop of only 1.98% compared to the FP16 baseline, which is 5.18% lower
> than Atom. On the hardware side, OASIS achieves an average 3.00× speedup and a 1.44×
> improvement in energy efficiency compared to the FIGLUT accelerator.
