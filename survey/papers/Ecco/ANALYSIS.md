# Ecco — paper notes

**Ecco: Improving Memory Bandwidth and Capacity for LLMs via Entropy-aware Cache Compression**
Feng Cheng, Cong Guo, Chiyue Wei, Junyao Zhang, Changchun Zhou, Edward Hanson, Jiaqi Zhang,
Xiaoxiao Liu, Hai "Helen" Li, Yiran Chen
**ISCA 2025** ｜ DOI: **not recorded** — the ACM/IEEE record is not reachable by script (403); look it up when citing
Venue evidence (2026-09-02): arXiv `comments` field, verbatim: *"ISCA 2025"*
Archived here: **arXiv:2505.06901v1** (2025-05-11), 15 pages — **the preprint, not the
published ISCA 2025 version**; the two were **not compared**.

Status: **brief ready** ｜ Last updated: 2026-09-02
Tags: `non-analytical-dtype` `gpu-kernels` `kv-cache` `dtype-granularity` `accelerator`
How far it was read: **abstract, introduction, section map, headline result sentences and
conclusion.** The method and evaluation sections were **not** read line by line, and no numbers
have been transcribed into the table below with their full frame — so this stays `brief ready`.
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> Original: https://arxiv.org/abs/2505.06901
> The PDF is **not committed** (1.4 MB). Re-download: `curl -sSL -o 2505.06901.pdf https://arxiv.org/pdf/2505.06901`
> Extract text: `python3 extract.py` → `extracted/` (committed, greppable)
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, ISCA 2025 row.

---

## Brief

### 1. Motivation

LLM deployment is memory-bound: the KV cache alone can be 72.7% (34.4 GB) of memory use.
Quantization helps but existing methods carry **high runtime overhead or accuracy loss**.
The unexploited angle is that cache data has exploitable *entropy* structure, not just range
structure.

### 2. Overview

Entropy-aware cache compression integrated at the **GPU L2 cache**: group-wise **non-
uniform** quantization against pre-defined shared **k-means** patterns, then **Huffman**
coding. Because textbook Huffman decoding is serial and slow, the paper contributes a
**parallel Huffman decoder** with a multi-stage pipeline that cuts latency by two orders of
magnitude to reach L2-comparable throughput.

### 3. Pros and cons

**Pros**

- The parallel Huffman decoder is the real engineering contribution — entropy coding is
usually dismissed as too serial for a cache, and this is a direct refutation.
- Sits at the L2 cache, so it compresses traffic to HBM transparently to the SMs, giving ~4×
capacity increase without changing the model or the kernels.
- Beats both software frameworks and a prior accelerator: 2.9×/1.9× over AWQ/SmoothQuant and
2.4× over the OliVe accelerator, at state-of-the-art accuracy.

**Cons**

- Shared **pre-defined** k-means patterns are fixed ahead of time; the paper reports low
clipping and padding ratios to argue they generalize, but distribution shift is an
unquantified risk.
- Requires modifying the GPU memory hierarchy — evaluated as a hardware proposal, not
something deployable on existing silicon.
- Entropy coding gives data-dependent compression ratios, so worst-case behaviour (and thus
provisioning) is harder to reason about than fixed-width quantization.

### 4. Where it applies

Bridges three clusters: **non-analytical data types** (k-means codebooks), **KV cache**, and
**GPU-integrated** compression. Note it is later used as a baseline by
[`P3-LLM`](../P3-LLM/ANALYSIS.md).

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


## Abstract (verbatim, arXiv:2505.06901v1)

> Large language models (LLMs) have demonstrated transformative capabilities across diverse
> artificial intelligence applications, yet their deployment is hindered by substantial
> memory and computational demands, especially in resource-constrained environments.
> Quantization techniques have emerged as a critical solution, reducing data precision to
> enhance memory and computational efficiency. However, existing methods often suffer from
> high runtime overheads and potential accuracy degradation. To address these challenges, we
> propose Ecco, an entropy-based cache compression technique tailored for LLMs. Ecco
> combines group-wise and non-uniform quantization with pre-defined shared k-means patterns
> and Huffman coding to exploit the inherent entropy characteristics of LLM cache data.
> Recognizing the inefficiencies of traditional Huffman coding in terms of parallelism and
> latency, we introduce a novel parallel Huffman-based decoding process with a multi-stage
> pipeline design, reducing latency by two orders of magnitude and achieving throughput
> comparable to GPU L2 caches. Comprehensive evaluations demonstrate that Ecco achieves an
> up to 2.9$\times$ and 1.9$\times$ speedup over the state-of-the-art AWQ and SmoothQuant
> framework, 2.4$\times$ over the Olive accelerator, all while increasing memory capacity by
> nearly 4$\times$ and maintaining state-of-the-art LLM accuracy. These results underscore
> the effectiveness of our entropy-based cache compression in enhancing LLM performance and
> efficiency, paving the way for more deployable large-scale AI models.
