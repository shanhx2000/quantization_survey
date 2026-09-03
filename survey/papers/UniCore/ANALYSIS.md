# UniCore — paper notes

**UniCore: A Bit-Width Scalable GEMM Unit for Unified LLM Inference**
Yonghao Chen, Jiaxiang Zou, Xingyu Chen, Chenxi Xu, Jingyu Guo, Xinyu Chen
**ISCA 2026** (2026 ACM/IEEE 53rd Annual International Symposium on Computer Architecture),
pp. 2520–2535 ｜ DOI: **10.1109/ISCA66397.2026.00176**
Publication info verified 2026-09-02 from the **official ISCA 2026 proceedings package**
(title, authors, pages, DOI and abstract all read from its `assets/data/data.js`).
Archived here: **the published proceedings PDF** (`506501c520.pdf`, 16 pages) — not a preprint.

Status: **brief ready** ｜ Last updated: 2026-09-02
Tags: `multi-bitwidth-hw` `new-data-type` `analytical-dtype` `mixed-precision` `accelerator`
How far it was read: **abstract, introduction, section map, headline result sentences and
conclusion.** The method and evaluation sections were **not** read line by line, and no numbers
have been transcribed into the table below with their full frame — so this stays `brief ready`.
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> The PDF is **not committed** (6.1 MB). It came from the proceedings package a human
> supplied, now archived at [`archieve/ISCA 2026.zip`](../../../archieve/), entry `pdfs/5065-3nexm57sBmVa6MJtFTiSrb/506501c520/506501c520.pdf`.
> **There is no public URL for it** — this is not an arXiv paper. Re-extract with
> `python3 extract.py` → `extracted/` (committed, greppable).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, 2026 row.

---

## Brief

### 1. Motivation

Different LLMs need different precisions — Llama-1/2 and OPT survive W4A4 while Llama-3
needs W8A8 — and a single model may want a low-precision 'draft' mode and a high-precision
'quality' mode. Fixed-format accelerators cannot span this. **Bit-composable** designs can,
but suffer a **quadratic collapse**: multiplier resources scale as O(n²) in area and delay,
so throughput falls as ~1/n² and high precision becomes unaffordable.

### 2. Overview

Change the primitive. **S-FPMA** is a composable floating-point multiply–add built from
**uniform adder slices**, so fusing to higher precision scales **linearly** rather than
quadratically. Numerical fidelity is restored by a lightweight format-conversion and **dual-
path compensation** pipeline correcting FPMA's structured approximation error. Complemented
by **DynFP**, a distribution-adaptive low-bit FP format.

### 3. Pros and cons

**Pros**

- Diagnoses the exact failure mode of the whole bit-composable lineage
([`BitFusion`](../BitFusion/ANALYSIS.md) onwards) and fixes it at the primitive level —
the strongest 'why previous designs plateaued' argument in the corpus.
- Delivers where composable designs are weakest: 1.24×–3.95× area efficiency at
W4A4/W4A8/W8A8 and **up to 5.26× at W16A16**, plus 24% smaller GEMM area than Tender even
with 16-bit support.
- Highest accuracy in nearly all configurations, and open-sourced.

**Cons**

- FPMA is an **approximate** primitive; correctness depends on the compensation pipeline, so
the design's fidelity is engineered rather than exact — a property to verify carefully
before citing it as lossless.
- Two contributions in one paper (S-FPMA and DynFP); how much of the accuracy result comes
from the format versus the compensation is not separable from the headline numbers.
- Compared mainly against composable-multiplier accelerators; against fixed-format designs
at their own single precision the flexibility premium is not shown.

### 4. Where it applies

The 2026 state of the art for **multi-bitwidth hardware (tag 9)** and the direct answer to
BitFusion. Read those two together — they bracket eight years of the same idea.

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

> Large Language Models (LLMs) have achieved remarkable success across a broad range of
> applications but impose extreme computational and memory demands due to their reliance on
> massive General Matrix–Matrix Multiplication (GEMM) operations. Quantization has emerged
> as a key approach to improve efficiency by reducing data precision; however, modern LLMs
> exhibit diverse sensitivities to quantization, requiring multiple precision settings.
> Existing hardware accelerators fail to efficiently support this diversity: fixed-function
> accelerators are limited to a few discrete formats, while bit-composable architectures
> suffer from quadratic resource scaling, leading to severe performance degradation at
> higher precision. We propose UniCore, a unified GEMM architecture that achieves both bit-
> width scalability and accuracy preservation through a hardware–software co-design. UniCore
> introduces Scalable FPMA (S-FPMA), the first composable FPMA primitive that fuses into
> different precisions using uniform adder slices, maintaining linear hardware scaling. To
> ensure numerical fidelity, UniCore integrates a lightweight format-conversion and dual-
> path compensation pipeline that corrects FPMA's structured approximation error.
> Complementing the architecture, DynFP, a distribution-adaptive low-bit floating-point
> format, improves representational accuracy for diverse LLM weight and activation
> distributions. UniCore delivers 1.24x-3.95x higher area efficiency for W4A4/W4A8/W8A8 and
> up to 5.26x at W16A16 compared to prior composable-multiplier accelerators, while
> achieving the highest accuracy in nearly all configurations. UniCore is open-sourced at:
> https://github.com/CLab-HKUST-GZ/isca53-unicore
