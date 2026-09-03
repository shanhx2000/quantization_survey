# NDPLowBitFP — paper notes

**Bringing Near Data Processing into the Low-Bit Floating-Point Era**
Tongxin Xie, Mingyu Gao, Zehao Wang, Zhihao Jia, Yuechen Xi, Bing Li, Mo Guang, Jiale Yan,
Kaiwen Long, Xingcheng Zhang, Huazhong Yang, Yuan Xie, Zhenhua Zhu, Yu Wang
**ISCA 2026** (2026 ACM/IEEE 53rd Annual International Symposium on Computer Architecture),
pp. 1383–1399 ｜ DOI: **10.1109/ISCA66397.2026.00104**
Publication info verified 2026-09-02 from the **official ISCA 2026 proceedings package**
(title, authors, pages, DOI and abstract all read from its `assets/data/data.js`).
Archived here: **the published proceedings PDF** (`506501b383.pdf`, 17 pages) — not a preprint.

Status: **brief ready** ｜ Last updated: 2026-09-02
Tags: `pim-ndp` `analytical-dtype` `dtype-granularity` `mixed-precision` `accelerator`
How far it was read: **abstract, introduction, section map, headline result sentences and
conclusion.** The method and evaluation sections were **not** read line by line, and no numbers
have been transcribed into the table below with their full frame — so this stays `brief ready`.
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> The PDF is **not committed** (1.5 MB). It came from the proceedings package a human
> supplied, now archived at [`archieve/ISCA 2026.zip`](../../../archieve/), entry `pdfs/5065-3nexm57sBmVa6MJtFTiSrb/506501b383/506501b383.pdf`.
> **There is no public URL for it** — this is not an arXiv paper. Re-extract with
> `python3 extract.py` → `extracted/` (committed, greppable).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, 2026 row.

---

## Brief

### 1. Motivation

Near-data processing answers the memory wall, and group-wise low-bit floating point answers
accuracy — FP4 gives 3–4× speedup and ~4× memory reduction on GPUs at comparable accuracy,
because exponent+mantissa gives finer resolution over a wider range than integers, and per-
group scales handle outliers. But **existing NDP compilers cannot support it**: different
quantization configurations prefer different compilation strategies; fine-grained grouping
makes execution alternate between value and scale accesses, **raising DRAM row-buffer
misses**; and frequent dequantization adds latency.

### 2. Overview

**FlexQ-NDP**, an NDP compiler for general low-bit FP, with an open-source simulation
framework for the cost model, a **scale-value interleaved layout** to cut row changes, a
**dequantization-hiding** technique based on instruction reordering, and a pruned
compilation-space search.

### 3. Pros and cons

**Pros**

- Targets the least glamorous and most real obstacle — the compiler — and each of the three
fixes maps to a specific measured cause.
- The scale-value interleaving insight is precise and non-obvious: fine-grained grouping's
cost is not arithmetic but DRAM row locality.
- Up to 3.29× speedup over existing compilation strategies across quantization
configurations, ~1.31× average energy reduction, with the simulation framework released.

**Cons**

- Simulation-based throughout, on a modelled NDP architecture — no silicon and no real DRAM-
PIM measurement.
- The compilation-space search is pruned 4–5×, which helps but still leaves a search whose
cost is a deployment consideration.
- Contributes no new data type: it makes existing group-wise low-bit FP practical on NDP, so
its place in §1.2 is as an enabler rather than an originator.

### 4. Where it applies

The **compiler/toolchain** perspective on quantization in the PIM/NDP cluster, and a good
corrective for a survey that would otherwise treat format support as purely a datapath
question. Read with [`P3-LLM`](../P3-LLM/ANALYSIS.md).

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

> Near data processing (NDP) based on DRAM has emerged to be a promising solution to the
> "memory wall" problem of machine learning models. From the algorithmic perspective, group-
> wise low-bit floating-point (FP) quantization has become an important trend for both
> efficient training and inference. Integrating low-bit FP quantization into NDP also
> notably shrinks the memory footprint of large models, alleviating the memory-capacity
> constraints of NDP architectures. However, existing NDP compilers struggle to support
> efficient low-bit FP computation on NDP. First, different quantization configurations
> exhibit different preferences for NDP compilation strategies. Second, the fine-grained
> grouping leads to frequent switching between quantized value access and group scale access
> during computation, increasing the DRAM row-buffer miss rate. Third, fine-grained grouping
> triggers frequent high-precision dequantization operations, causing significant latency
> overhead. To address these challenges, this paper proposes FlexQ-NDP, an NDP compiler
> tailored for general low-bit FP computation. Firstly, we develop an open-source simulation
> framework to model the low-bit FP computation overhead on NDP. Secondly, we design a
> scale-value interleaved FP layout, effectively reducing DRAM row-changing overhead.
> Thirdly, we propose a dequantization-hiding technique based on instruction reordering to
> reduce the DRAM idle time induced by frequent dequantization operations. Finally, we
> develop a lightweight compilation-space pruning and search strategy to enable efficient
> low-bit FP computation on NDP. Extensive experiments show that FlexQ-NDP achieves up to
> 3.29× speedup over existing compilation strategies on various low-bit FP quantization
> configurations.
