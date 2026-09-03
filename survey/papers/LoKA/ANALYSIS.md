# LoKA — paper notes

**LoKA: Low-Precision Kernel Applications for Recommendation Models At Scale**
Liang Luo, Yinbin Ma, Quanyu Zhu, Vasiliy Kuznetsov, Yuxin Chen, Jian Jiao, Jiecao Yu, Buyun
Zhang, Tongyi Tang, Xiaohan Wei, Yanli Zhao, Zeliang Chen, Yuchen Hao, Venkatesh
Ranganathan, Sandeep Parab, Yantao Yao, Maxim Naumov, Chunzhi Yang, Shen Li, Ellie Wen,
Wenlin Chen, Chunqiang Tang
**ISCA 2026** (2026 ACM/IEEE 53rd Annual International Symposium on Computer Architecture),
pp. 1368–1382 ｜ DOI: **10.1109/ISCA66397.2026.00103**
Publication info verified 2026-09-02 from the **official ISCA 2026 proceedings package**
(title, authors, pages, DOI and abstract all read from its `assets/data/data.js`).
Archived here: **the published proceedings PDF** (`506501b368.pdf`, 15 pages) — not a preprint.

Status: **brief ready** ｜ Last updated: 2026-09-02
Tags: `analytical-dtype` `gpu-kernels` `training` `mixed-precision`
How far it was read: **abstract, introduction, section map, headline result sentences and
conclusion.** The method and evaluation sections were **not** read line by line, and no numbers
have been transcribed into the table below with their full frame — so this stays `brief ready`.
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> The PDF is **not committed** (1.0 MB). It came from the proceedings package a human
> supplied, now archived at [`archieve/ISCA 2026.zip`](../../../archieve/), entry `pdfs/5065-3nexm57sBmVa6MJtFTiSrb/506501b368/506501b368.pdf`.
> **There is no public URL for it** — this is not an arXiv paper. Re-extract with
> `python3 extract.py` → `extracted/` (committed, greppable).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, 2026 row.

---

## Brief

### 1. Motivation

Each GPU generation delivers far more FLOPs at lower precision — B200 FP8 is 29× and FP4 58×
an A100's TF32 — and FP8 has been made to work for LLMs. But **large recommendation models**
have not adopted it, and naively applying FP8 gives **1.3× slowdown and up to 2.5% relative
log-loss degradation** in production, where 0.02% is already significant.

### 2. Overview

A framework, not an architecture. Three parts: **LoKA Probe**, statistically grounded online
benchmarking that learns activation/weight statistics and quantifies per-layer error to
locate where FP8 is safe and where it is fast; **LoKA Mods**, reusable model adaptations
that widen the safe region; and **LoKA Dispatch**, a runtime that picks the fastest FP8
kernel meeting the accuracy requirement.

### 3. Pros and cons

**Pros**

- Deployed at production scale — recommendation models serving billions of users across
H100, B200, GB200, MI300X and MI350X — which no other entry in the corpus can claim.
- The diagnosis is sharp about *why* LRMs differ from LLMs: tight quality constraints,
architectural heterogeneity, and low arithmetic intensity (many small GEMMs followed by
normalization) where quantization overhead can exceed the benefit.
- 20% higher training throughput and 40% faster inference **with no quality loss**, and it
correctly argues these problems cannot be fixed by better kernels alone.

**Cons**

- No hardware contribution — it is systems and model co-design on stock GPUs, so it sits at
the edge of an architecture survey.
- Production results come with production opacity: model architectures and the exact quality
metric are only partly disclosable.
- FP8-specific; whether the Probe/Mods/Dispatch structure carries to FP4 or to non-
recommendation workloads is asserted rather than shown.

### 4. Where it applies

The corpus's main **GPU-kernel + training** entry and its only look at recommendation
models. Valuable to the survey as evidence that **where a format is safe** is a per-layer
empirical question, not a model-level one.

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

> Recent GPU generations deliver significantly higher FLOPs using lower-precision
> arithmetic, such as FP8. While successfully applied to large language models (LLMs), its
> adoption in large recommendation models (LRMs) has been limited. This is because LRMs are
> numerically sensitive, dominated by small matrix multiplications (GEMMs) followed by
> normalization, and trained in communication-intensive environments. Applying FP8 directly
> to LRMs often degrades model quality and prolongs training time. These challenges are
> inherent to LRM workloads and cannot be resolved merely by introducing better FP8 kernels.
> Instead, a system-model co-design approach is needed to successfully integrate FP8. We
> present LoKA (Low-precision Kernel Applications), a framework that makes FP8 practical for
> LRMs through three principles: profile under realistic distributions to know where low
> precision is safe, co-design model components with hardware to expand where it is safe,
> and orchestrate across kernel libraries to maximize the gains. Concretely, LoKA Probe is a
> statistically grounded, online benchmarking method that learns activation and weight
> statistics, and quantifies per-layer errors. This process pinpoints safe and unsafe, fast
> and slow sites for FP8 adoption. LoKA Mods is a set of reusable model adaptations that
> improve both numerical stability and execution efficiency with FP8. LoKA Dispatch is a
> runtime that leverages the statistical insights from LoKA Probe to select the fastest FP8
> kernel that satisfies the accuracy requirements. Deployed on production LRMs that serve
> billions of users with advertising recommendations at a major social media company, LoKA
> delivers up to 20% higher training throughput and 40% faster inference on heterogeneous
> GPUs (H100, B200, GB200, MI300X and MI350X) in production environment, with no quality
> loss, turning FP8 from a model-quality risk into a reliable performance lever for LRMs at
> scale.
