# EVA — paper notes

**EVA: Accelerating LLM Decoding via an Efficient Vector Quantization Architecture**
Bowen Duan, Cong Guo, Chiyue Wei, Haoxuan Shan, Yuzhe Fu, Xinhua Chen, Yifan Xu, Ziyue
Zhang, Changchun Zhou, Hai Li, Yiran Chen
**ISCA 2026** (2026 ACM/IEEE 53rd Annual International Symposium on Computer Architecture),
pp. 1351–1367 ｜ DOI: **10.1109/ISCA66397.2026.00102**
Publication info verified 2026-09-02 from the **official ISCA 2026 proceedings package**
(title, authors, pages, DOI and abstract all read from its `assets/data/data.js`).
Archived here: **the published proceedings PDF** (`506501b351.pdf`, 17 pages) — not a preprint.

Status: **brief ready** ｜ Last updated: 2026-09-02
Tags: `non-analytical-dtype` `lut-accelerator` `accelerator`
How far it was read: **abstract, introduction, section map, headline result sentences and
conclusion.** The method and evaluation sections were **not** read line by line, and no numbers
have been transcribed into the table below with their full frame — so this stays `brief ready`.
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> The PDF is **not committed** (2.3 MB). It came from the proceedings package a human
> supplied, now archived at [`archieve/ISCA 2026.zip`](../../../archieve/), entry `pdfs/5065-3nexm57sBmVa6MJtFTiSrb/506501b351/506501b351.pdf`.
> **There is no public URL for it** — this is not an arXiv paper. Re-extract with
> `python3 extract.py` → `extracted/` (committed, greppable).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, 2026 row.

---

## Brief

### 1. Motivation

LLM **decoding** is a sequence of small GEMV-like operations: memory-bound, and it
underutilizes accelerators built for GEMM. Weight-only **vector quantization** compresses
weights to ~2-bit levels via a shared codebook, but leaves two inefficiencies — GEMV still
underutilizes the array, and codebook lookups cause frequent **memory bank conflicts**.

### 2. Overview

Invert the dataflow. Instead of reconstructing weights from indices and doing GEMV,
**compute dot products directly between the input vector and the weight codebook** — which
turns decoding from GEMV into **GEMM** — then perform structured lookups from an
intermediate output buffer, which eliminates bank conflicts by construction. Co-designed
architecture that still runs conventional prefill.

### 3. Pros and cons

**Pros**

- The reframing is the whole idea and it is a good one: computing against the codebook
rather than the reconstructed weights changes the operation's *shape*, fixing utilization
and conflicts at once.
- Preserves arithmetic precision exactly after vector quantization — the architecture adds
no error of its own.
- 11.17× speedup and 7.17× energy efficiency over the state-of-the-art lookup-based
architecture; open-sourced.

**Cons**

- Benefit is proportional to codebook reuse, so it depends on VQ configuration (vector
length, codebook size); the paper tabulates many AQLM/GPTVQ configurations, which signals
the result is configuration-sensitive.
- Targets **decoding only** — prefill runs conventionally, so end-to-end gains depend on the
decode/prefill mix of the workload.
- Inherits vector quantization's own accuracy characteristics; the paper's contribution is
executing VQ well, not making VQ more accurate.

### 4. Where it applies

The clearest **non-analytical data type (§1.3)** entry — vector quantization with a genuine
codebook — and simultaneously a **LUT-accelerator** design. Its GEMV→GEMM reframing is worth
a sentence in the survey's own analysis.

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

> Large Language Models (LLMs) have achieved impressive performance across diverse domains
> but remain inefficient during the autoregressive decoding phase. Unlike the prefill stage,
> which employs compute-bound GEMM operations, decoding executes a sequence of small GEMV-
> like computations that are memory-bound and underutilize modern accelerators. Weight-only
> vector quantization (VQ) has emerged as an effective compression technique that clusters
> model weights into a shared codebook and replaces the original weight matrix with low-
> precision indices, enabling 2-bit-level weight compression. While this approach
> substantially reduces model size and memory bandwidth, it still suffers from two critical
> inefficiencies: the low utilization of GEMV computation and frequent memory conflicts
> during codebook lookups. This paper presents EVA, an efficient vector-quantization-based
> architecture that addresses both computational and memory bottlenecks in LLM decoding. EVA
> builds on a simple yet effective insight that combines input-codebook computation with
> conflict-free memory access. Instead of reconstructing quantized weights from indices, EVA
> directly performs dot products between input vectors and the weight codebook, transforming
> LLM decoding from GEMV to GEMM computation. It then performs structured lookups from an
> intermediate output buffer, eliminating memory bank conflicts. We further design a
> hardware-software co-optimized architecture specialized for LLM decoding while remaining
> compatible with conventional prefill execution. Evaluations show that EVA achieves up to
> 11.17x speedup and 7.17x higher energy efficiency compared with the SOTA lookup-based
> architecture, while preserving arithmetic precision after vector quantization. Our code is
> available at https://github.com/dbw6/Eva.git.
