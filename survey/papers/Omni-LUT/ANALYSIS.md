# Omni-LUT — paper notes

**Omni-LUT: Energy-Efficient LUT-Based Accelerator with Hardware-Aware KV Cache Quantization**
Cheng-Han Tsai, Kuan-Chen Chou, Yu-Hsin Wang, Chieh-Dun Wen, Tsung Tai Yeh
**ISCA 2026** (2026 ACM/IEEE 53rd Annual International Symposium on Computer Architecture),
pp. 322–337 ｜ DOI: **10.1109/ISCA66397.2026.00037**
Publication info verified 2026-09-02 from the **official ISCA 2026 proceedings package**
(title, authors, pages, DOI and abstract all read from its `assets/data/data.js`).
Archived here: **the published proceedings PDF** (`506501a322.pdf`, 16 pages) — not a preprint.

Status: **brief ready** ｜ Last updated: 2026-09-02
Tags: `lut-accelerator` `kv-cache` `non-analytical-dtype` `mixed-precision` `accelerator`
How far it was read: **abstract, introduction, section map, headline result sentences and
conclusion.** The method and evaluation sections were **not** read line by line, and no numbers
have been transcribed into the table below with their full frame — so this stays `brief ready`.
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> The PDF is **not committed** (2.0 MB). It came from the proceedings package a human
> supplied, now archived at [`archieve/ISCA 2026.zip`](../../../archieve/), entry `pdfs/5065-3nexm57sBmVa6MJtFTiSrb/506501a322/506501a322.pdf`.
> **There is no public URL for it** — this is not an arXiv paper. Re-extract with
> `python3 extract.py` → `extracted/` (committed, greppable).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, 2026 row.

---

## Brief

### 1. Motivation

LUT-based GEMM accelerators only handle **activation–weight** GEMM in linear layers. But as
context grows, **activation–activation** GEMM in attention dominates: AW-GEMM scales as O(T)
while AA-GEMM scales as O(T²) in prefill, and in decode the KV cache must be read in full
for every token. A LUT accelerator that cannot do attention is solving the shrinking half of
the problem.

### 2. Overview

Extends LUT execution to **both** GEMM types. Doing so requires a LUT-consumable KV cache,
so the paper contributes a **BCQ-based KV quantization** design combining offline
calibration with lightweight online quantization, plus quantization compensation applied
*during LUT creation* to support the accuracy-preferred scaling direction (prior LUT designs
scale after lookup, which does not allow it). Hardware is a **phase-adaptive hybrid-
stationary LUT systolic array** serving prefill and decode differently.

### 3. Pros and cons

**Pros**

- Identifies a real structural gap — the O(T) vs O(T²) argument is the clearest
justification in the corpus for why attention, not the linear layers, is where long-
context effort belongs.
- The scaling-direction observation is a subtle, specific hardware insight: it explains
*why* prior LUT designs could not simply be pointed at attention.
- 1.25×–1.91× energy efficiency over the state-of-the-art LUT GEMM accelerator at equal peak
throughput, with competitive accuracy against dedicated KV quantization methods.

**Cons**

- Gains are reported at **equal peak-throughput** configuration — an iso-resource framing
that is fair but not the same as end-to-end serving throughput.
- KV quantization depends on offline calibration; the paper studies calibration-dataset
choice, which signals sensitivity worth checking before citing.
- Two mechanisms (BCQ KV quantization + phase-adaptive array) are entangled in the results;
their separate contributions are not obvious from the headline numbers.

### 4. Where it applies

Sits at the intersection of **LUT accelerators** and the **KV-cache** cluster, and is the
corpus's main argument that attention-side GEMM is the next target. Read after
[`LUTTensorCore`](../LUTTensorCore/ANALYSIS.md) and [`Oaken`](../Oaken/ANALYSIS.md).

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

> Large language model (LLM) inference incurs substantial computation and energy
> consumption. Lookup-table (LUT)-based general matrix multiplication (GEMM) accelerators
> reduce this burden by replacing costly multiplications with table lookups. However,
> existing designs only support activation-weight GEMM (AW-GEMM) in LLM linear layers, while
> LUT execution for activation-activation GEMM (AA-GEMM) in attention has not been realized.
> As AA-GEMM is a major contributor to the computation and energy costs of LLM inference in
> long-context scenarios, supporting both GEMM types-not just AW-GEMM-is crucial. To solve
> this problem, we propose Omni-LUT, a hardware-software co-designed LUT-based GEMM
> accelerator that supports both AW-GEMM in linear layers and AA-GEMM in attention with
> efficient LUT execution. Omni-LUT uses a hardware-aware Key-Value (KV) cache quantization
> design that combines offline calibration with lightweight online quantization, preserving
> model accuracy while enabling compatibility with LUT accelerators. It also supports a more
> accurate quantization direction by leveraging quantization compensation during LUT
> creation. Omni-LUT further comprises a phase-adaptive hybrid-stationary LUT-based systolic
> array to improve the efficiency of both the prefill and decode phases in LLMs. Across
> diverse long context workloads, Omni-LUT achieves 1.25x-1.91x higher energy efficiency
> than the state-of-the-art (SOTA) LUT-based GEMM accelerator under an equal peak-throughput
> hardware setup, while maintaining competitive model accuracy compared with SOTA KV
> quantization methods.
