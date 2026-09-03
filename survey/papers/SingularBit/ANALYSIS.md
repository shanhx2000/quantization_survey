# SingularBit — paper notes

**SingularBit: Exploiting Synergy of Singular Value Decomposition and Low-Bit Quantization for Weight and KV Compression in LLM Inference**
Seongyon Hong, Hyundeok Kong, Jungwan Lee, Sangjin Kim, Hoi-Jun Yoo
**ISCA 2026** (2026 ACM/IEEE 53rd Annual International Symposium on Computer Architecture),
pp. 1001–1015 ｜ DOI: **10.1109/ISCA66397.2026.00079**
Publication info verified 2026-09-02 from the **official ISCA 2026 proceedings package**
(title, authors, pages, DOI and abstract all read from its `assets/data/data.js`).
Archived here: **the published proceedings PDF** (`506501b001.pdf`, 15 pages) — not a preprint.

Status: **brief ready** ｜ Last updated: 2026-09-02
Tags: `combined-dtype` `mixed-precision` `kv-cache` `dtype-granularity` `accelerator`
How far it was read: **abstract, introduction, section map, headline result sentences and
conclusion.** The method and evaluation sections were **not** read line by line, and no numbers
have been transcribed into the table below with their full frame — so this stays `brief ready`.
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> The PDF is **not committed** (3.3 MB). It came from the proceedings package a human
> supplied, now archived at [`archieve/ISCA 2026.zip`](../../../archieve/), entry `pdfs/5065-3nexm57sBmVa6MJtFTiSrb/506501b001/506501b001.pdf`.
> **There is no public URL for it** — this is not an arXiv paper. Re-extract with
> `python3 extract.py` → `extracted/` (committed, greppable).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, 2026 row.

---

## Brief

### 1. Motivation

Inference-time scaling — long contexts, long generations, multi-step reasoning — creates a
**Dual Memory Wall**: a decode session starts weight-bound (O(L·D²·b_W) per token) and
becomes KV-bound as the sequence grows (O(N·L·D·b_KV)), and **the crossover point is
unpredictable per request**. Prior work treats weight compression and KV compression in
isolation.

### 2. Overview

The first accelerator to exploit the synergy between **SVD and low-bit quantization** for
both. The insight is that singular values decay fast in both weight matrices and attention
distributions, so precision can be allocated **by rank**: SingularBit-W compresses most
weight parameters to **1–2 bits** under rank-aware mixed precision, executed by a tensor
core supporting rank-wise mixed precision; SingularBit-KV extends the same principle online,
allocating precision by both token importance and rank significance. 28 nm CMOS.

### 3. Pros and cons

**Pros**

- Addressing both walls in one mechanism is the right response to an unpredictable crossover
— a single-sided solution is only ever right for part of a request.
- Rank as the precision-allocation axis is a genuinely different granularity from the
channel/block/token options elsewhere in the corpus.
- Holds up where competitors collapse: at 2-bit, KVQuant/PALU/ZipCache fall to 0–30%
accuracy while SingularBit-KV loses 2.0% on CoQA and 0.5% on TruthfulQA. Algorithmic gains
are real even on a GPU (4.00× speedup at 3-bit average weight precision).

**Cons**

- SVD is a preprocessing cost for weights and a structural constraint online; the paper
reports end-to-end gains but the decomposition overhead is not the easiest thing to audit
from the abstract-level reading.
- 1–2 bit weights are an aggressive claim resting on rank-aware allocation — the accuracy
story depends on the singular-value decay assumption holding for the models tested.
- 28 nm synthesis is a conservative node; comparisons against GPU baselines at far newer
nodes need care.

### 4. Where it applies

The **combined data type** taken to its most general form — a value as a sum of rank
components at different precisions. The natural modern successor to
[`SmartExchange`](../SmartExchange/ANALYSIS.md)'s factorization idea, and a KV-cache entry.

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

> Large language models (LLMs) have become indispensable across diverse domains, while
> inference-time scaling has further enhanced their ability to tackle complex real-world
> tasks through long-context processing and extended generation. However, autoregressive
> decoding with extended sequences intensifies the memory bandwidth bottleneck through
> repeated weight access and growing key-value (KV) caches, a challenge we term the Dual
> Memory Wall. Although quantization and low-rank approximation have been explored
> independently for weight and KV compression, existing approaches remain insufficient for
> the demands of modern LLM inference. We present SingularBit, the first accelerator to
> exploit the synergy between singular value decomposition (SVD) and low-bit quantization
> for both offline weight and online KV cache compression. Our key insight is that singular
> values decay rapidly in both weight matrices and attention distributions, enabling
> aggressive compression of less critical components while preserving model accuracy through
> rank-aware mixed-precision allocation. SingularBit comprises two algorithm-hardware co-
> designs. First, SingularBit-W applies rank-aware mixed-precision quantization to weights,
> compressing most parameters to 1-2 bits guided by singular value magnitude, executed
> efficiently by the SingularBit Tensor Core supporting rank-wise mixed-precision
> computation. Second, SingularBit-KV extends this principle to online KV cache compression,
> dynamically allocating precision based on both token importance and rank significance,
> accelerated by the SingularBit Compression Engine. Synthesized in 28nm CMOS, SingularBit
> achieves state-of-the-art algorithmic efficiency across standard language modeling,
> commonsense reasoning, and long-context benchmarks.
