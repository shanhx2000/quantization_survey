# P3-LLM — paper notes

**P3-LLM: An Integrated NPU-PIM Accelerator for Edge LLM Inference Using Hybrid Numerical Formats**
Yuzong Chen, Chao Fang, Xilai Dai, Yuheng Wu, Thierry Tambe, Marian Verhelst, Mohamed
Abdelfattah
**ISCA 2026** (2026 ACM/IEEE 53rd Annual International Symposium on Computer Architecture),
pp. 604–619 ｜ DOI: **10.1109/ISCA66397.2026.00055**
Publication info verified 2026-09-02 from the **official ISCA 2026 proceedings package**
(title, authors, pages, DOI and abstract all read from its `assets/data/data.js`).
Archived here: **the published proceedings PDF** (`506501a604.pdf`, 16 pages) — not a preprint.

Status: **brief ready** ｜ Last updated: 2026-09-02
Tags: `pim-ndp` `mixed-precision` `analytical-dtype` `dtype-granularity` `kv-cache` `accelerator`
How far it was read: **abstract, introduction, section map, headline result sentences and
conclusion.** The method and evaluation sections were **not** read line by line, and no numbers
have been transcribed into the table below with their full frame — so this stays `brief ready`.
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> The PDF is **not committed** (1.6 MB). It came from the proceedings package a human
> supplied, now archived at [`archieve/ISCA 2026.zip`](../../../archieve/), entry `pdfs/5065-3nexm57sBmVa6MJtFTiSrb/506501a604/506501a604.pdf`.
> **There is no public URL for it** — this is not an arXiv paper. Re-extract with
> `python3 extract.py` → `extracted/` (committed, greppable).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, 2026 row.

---

## Brief

### 1. Motivation

Edge LLM inference suits an NPU (compute-bound prefill GEMM) plus DRAM-based PIM (memory-
bound decode GEMV) split. But PIM compute units built for FP16 are **area- and power-
prohibitive in DRAM**, where transistor density is ~10× worse than logic — which has
confined PIM's practical speedup to single-batch inference on older models. Grouped-query
attention raises arithmetic intensity above one, so that confinement now bites.

### 2. Overview

Three parts: a **flexible mixed-precision quantization scheme using hybrid numerical
formats**, choosing a different format per LLM operand; PIM compute units co-designed for
exactly those formats, so throughput rises under an iso-area DRAM constraint; and dataflow
optimization with **operator fusion** to minimize runtime dequantization overhead.

### 3. Pros and cons

**Pros**

- The format choice is driven by what can be built cheaply in DRAM — co-design in the strong
sense, where the numeric format is selected for the substrate rather than the other way
round.
- Wins on accuracy against both comparison classes: 1.04% better than
[`Oaken`](../Oaken/ANALYSIS.md) at 4-bit KV, and 39%/22% lower perplexity loss than
QuaRot/QoQ **while quantizing more aggressively** (8-bit queries and attention scores).
- 4.9×/2.0×/3.4× average speedups over HBM-PIM, [`Ecco`](../Ecco/ANALYSIS.md) and Pimba;
open-sourced.

**Cons**

- Scoped to **edge, low-batch** inference; the DRAM-area argument that motivates it is
weaker in datacenter settings with different cost structures.
- Area is scaled analytically for the DRAM process (the 10× density factor) rather than laid
out, so the iso-area claim rests on a model.
- 'Hybrid numerical formats' means several formats coexisting, which pushes complexity into
the compiler/dataflow — the operator-fusion work is necessary, not optional.

### 4. Where it applies

The corpus's strongest **PIM/NDP + mixed-precision** entry and a KV-cache participant. Read
with [`NDPLowBitFP`](../NDPLowBitFP/ANALYSIS.md) (the compiler-side view of the same
problem) and [`RAELLA`](../RAELLA/ANALYSIS.md) (the analog view).

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

> The substantial memory bandwidth and computational demands of large language models (LLMs)
> present critical challenges for efficient inference. To tackle this, the literature has
> explored heterogeneous systems that combine neural processing units (NPUs) with DRAM-based
> processing-in-memory (PIM) for LLM acceleration. However, the high-precision PIM compute
> units incur significant area and power overhead in DRAM technology, limiting the effective
> computation throughput. In this paper, we introduce P3-LLM, a novel NPU-PIM integrated
> accelerator for edge LLM inference. Our approach is threefold: First, we propose a
> flexible mixed-precision quantization scheme, which leverages hybrid numerical formats to
> quantize different LLM operands with high compression efficiency and minimal accuracy
> loss. Second, we architect an efficient PIM accelerator for P3-LLM, featuring enhanced
> compute units to support hybrid numerical formats. Our careful choice of numerical formats
> allows to co-design low-precision PIM compute units that significantly boost the
> computation throughput under iso-area constraints. Third, we optimize the low-precision
> dataflow of different LLM modules by applying operator fusion to minimize the overhead of
> runtime dequantization. Evaluations on diverse LLMs and tasks demonstrate that P3-LLM
> achieves higher accuracy than state-of-the-art KV-cache quantization and weight-activation
> quantization algorithms. Combining the proposed quantization scheme with low-precision PIM
> architecture co-design, P3-LLM yields an average of 4.9×, 2.0×, and 3.4× speedups over
> state-of-the-art LLM accelerators HBM-PIM, Ecco, and Pimba, respectively. Code is
> available at https://github.com/yc2367/P3-LLM.
