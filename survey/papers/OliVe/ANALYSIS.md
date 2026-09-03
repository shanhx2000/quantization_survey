# OliVe — paper notes

**OliVe: Accelerating Large Language Models via Hardware-friendly Outlier-Victim Pair Quantization**
Cong Guo, Jiaming Tang, Weiming Hu, Jingwen Leng, Chen Zhang, Fan Yang, Yunxin Liu, Minyi
Guo, Yuhao Zhu
**ISCA 2023** ｜ DOI: **not recorded** — the ACM/IEEE record is not reachable by script (403); look it up when citing
Venue evidence (2026-09-02): arXiv `comments` field, verbatim: *"ISCA 2023"*
Archived here: **arXiv:2304.07493v1** (2023-04-15), 15 pages — **the preprint, not the
published ISCA 2023 version**; the two were **not compared**.

Status: **brief ready** ｜ Last updated: 2026-09-02
Tags: `new-data-type` `combined-dtype` `analytical-dtype` `mixed-precision` `accelerator`
How far it was read: **abstract, introduction, section map, headline result sentences and
conclusion.** The method and evaluation sections were **not** read line by line, and no numbers
have been transcribed into the table below with their full frame — so this stays `brief ready`.
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> Original: https://arxiv.org/abs/2304.07493
> The PDF is **not committed** (1.4 MB). Re-download: `curl -sSL -o 2304.07493.pdf https://arxiv.org/pdf/2304.07493`
> Extract text: `python3 extract.py` → `extracted/` (committed, greppable)
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, ISCA 2023 row.

---

## Brief

### 1. Motivation

LLM size grows 240× every two years, outpacing hardware. Outliers block low-bit
quantization, and the existing fix — sparsity encoding with a **global coordinate list** —
needs global coordination, complex encode/decode logic and an orchestration controller. That
overhead is why outlier-aware accelerators underdeliver.

### 2. Overview

The key insight is asymmetric: **outliers matter, and the normal values adjacent to them do
not**. So sacrifice the neighbour — the "victim" — and use its bits to store the outlier in
place. This **outlier-victim pair (OVP)** encoding is memory-aligned and purely local, which
means it drops into a systolic array or tensor core without a global sparsity structure.

### 3. Pros and cons

**Pros**

- Turns a global, irregular problem into a local, aligned one — the single cleanest idea in
the outlier thread, and the reason it is so widely cited.
- 4.5× speedup and 4.0× energy reduction over GOBO **with better model accuracy**, i.e. it
wins on both axes rather than trading them.
- Being memory-aligned is what makes it embeddable in existing hardware (the paper shows GPU
and systolic-array integration), which is a deployability argument the sparsity-based
predecessors cannot make.

**Cons**

- Pruning the victim is a real accuracy cost that is *assumed* tolerable because victims are
'unimportant'; that assumption is validated empirically, not derived.
- It works because outliers are locally sparse — where two outliers are adjacent, the scheme
has to degrade. [`MicroScopiQ`](../MicroScopiQ/ANALYSIS.md) attacks exactly this, arguing
'adjacent outliers matter' and that OliVe assumes an outlier locality that does not hold
for all foundation models.
- [`Tender`](../Tender/ANALYSIS.md) reports OliVe behind it on perplexity at comparable
settings, and [`MicroScopiQ`](../MicroScopiQ/ANALYSIS.md) claims ≥8% accuracy advantage at
lower precision — so its accuracy standing is contested by later work.

### 4. Where it applies

The hinge of the **outlier / combined-data-type** thread and a required read: it is both the
state of the art that 2025–26 papers cite and the target they attack. Its argument that
*hardware-friendliness is part of the algorithm* is a survey-level theme.

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

> **Keywords:** Outlier-Victim Pair


## Abstract (verbatim, arXiv:2304.07493v1)

> Transformer-based large language models (LLMs) have achieved great success with the
> growing model size. LLMs' size grows by $240\times$ every two years, which outpaces the
> hardware progress and makes model inference increasingly costly. Model quantization is a
> promising approach to mitigate the widening gap between LLM size and hardware capacity.
> However, the existence of outliers, values with significant magnitudes, in LLMs makes
> existing quantization methods less effective. Prior outlier-aware quantization schemes
> adopt sparsity encoding techniques to separate outliers from normal values where the
> process requires global coordination (e.g., a global sparsity coordination list). This
> incurs complex encoding/decoding hardware logics and an extra orchestration controller for
> the computation between outlier and normal values. As such, it is not hardware-efficient
> and hence only achieves sub-optimal quantization benefits. We propose OliVe, an
> algorithm/architecture co-designed solution that adopts an outlier-victim pair (OVP)
> quantization and handles outlier values locally with low hardware overheads and high
> performance gains. The key insight of OliVe is that outliers are important while the
> normal values next to them are not. Thus those normal values (called victims) can be
> sacrificed to accommodate outliers. This enables a memory-aligned OVP encoding scheme,
> which can be efficiently integrated to the existing hardware accelerators like systolic
> array and tensor core. As a result, OliVe-based accelerator surpasses the existing
> outlier-aware accelerator, GOBO, by 4.5$\times$ speedup and 4.0$\times$ energy reduction,
> respectively, with a superior model accuracy.
