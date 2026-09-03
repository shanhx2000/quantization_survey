# ELSA — paper notes

**ELSA: An Elastic SNN Inference Architecture for Efficient Neuromorphic Computing**
Kang You, Chen Nie, Jun Yan Lee, Ziling Wei, Zou Cheng, Zekai Xu, Feng Yu, Honglan Jiang,
Zhezhi He
**ISCA 2026** (2026 ACM/IEEE 53rd Annual International Symposium on Computer Architecture),
pp. 2550–2566 ｜ DOI: **10.1109/ISCA66397.2026.00178**
Publication info verified 2026-09-02 from the **official ISCA 2026 proceedings package**
(title, authors, pages, DOI and abstract all read from its `assets/data/data.js`).
Archived here: **the published proceedings PDF** (`506501c550.pdf`, 17 pages) — not a preprint.

Status: **brief ready** ｜ Last updated: 2026-09-02
Tags: `accelerator`
How far it was read: **abstract, introduction, section map, headline result sentences and
conclusion.** The method and evaluation sections were **not** read line by line, and no numbers
have been transcribed into the table below with their full frame — so this stays `brief ready`.
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> The PDF is **not committed** (3.2 MB). It came from the proceedings package a human
> supplied, now archived at [`archieve/ISCA 2026.zip`](../../../archieve/), entry `pdfs/5065-3nexm57sBmVa6MJtFTiSrb/506501c550/506501c550.pdf`.
> **There is no public URL for it** — this is not an arXiv paper. Re-extract with
> `python3 extract.py` → `extracted/` (committed, greppable).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, 2026 row.

---

## Brief

### 1. Motivation

SNNs have a property nobody exploits: **elastic inference** — outputs emerge progressively,
so salient inputs can be answered long before full evaluation, with the first correct
response arriving up to **82% earlier** than the stable-state output. That matters for real-
time tasks like autonomous driving. But existing SNN accelerators forfeit it: layer-by-layer
designs emit nothing until all layers finish, and time-step-by-time-step designs use coarse
layer-wise pipelines that synchronize every spine/token in a layer.

### 2. Overview

A near-SRAM dataflow architecture realising true elastic inference through a **fine-grained
spine/token-wise pipeline** that forwards each spine or token the moment it is produced,
forming a continuous stream. Supported by a **bundled address-event-representation
protocol** to cut NoC traffic and a mini-batch spiking Gustavson-product dataflow to reduce
memory access and exploit sparsity.

### 3. Pros and cons

**Pros**

- Identifies and then delivers a latency metric the field had been leaving on the table —
first-correct-response latency, not just throughput.
- Beats both neighbours: for 4-bit ResNet-50, 3.4×/13.6× speedup and energy efficiency over
the SOTA **quantized-ANN** accelerator (ANT), and 2.9×/22.1× over the SOTA SNN
accelerator.
- Attributes gains to their sources — 27.4× geomean energy saving from the dataflow, 1.65×
geomean speedup from the fine-grained pipeline — rather than reporting one lump number.

**Cons**

- **No quantization contribution.** The source list's own note is about its address-event
protocol lowering communication traffic; it is in this corpus as an SNN architecture, not
a data-type or precision paper.
- The elastic-inference benefit presumes an application that can act on an early,
provisional answer — a real constraint the paper illustrates but does not bound.
- Comparing SNNs against quantized ANNs requires accepting an accuracy-parity claim across
two model families, which is a heavier assumption than a same-family comparison.

### 4. Where it applies

Outside the taxonomy, alongside [`Phi`](../Phi/ANALYSIS.md), as the corpus's two **spiking-
neural-network** entries. Its ANT comparison is the one place the survey can see quantized-
ANN and SNN hardware measured on the same benchmark.

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

> Spiking neural networks (SNNs) exploit event-driven and addition-only computation to
> substantially improve efficiency for intelligent computation. A key temporal property of
> SNNs, elastic inference, allows outputs to emerge progressively, enabling responses to
> salient inputs much earlier than full evaluation. However, existing SNN-specific
> accelerators cannot capitalize on this property. Layer-by-layer designs emit outputs only
> after all layers are complete, while time-step-by-time-step designs rely on coarse-
> grained, layer-wise pipelines that require synchronizing all spines/tokens within a layer.
> This barrier prevents results from being forwarded immediately, delaying the earliest
> possible response and forfeiting the benefits of elastic inference. To address these
> challenges, we propose ELSA, a near-SRAM dataflow architecture that realizes true elastic
> inference through a fine-grained spine/token-wise pipeline and hardware optimizations
> tailored to SNNs. ELSA forwards each spine/token immediately upon production, forming a
> continuous streaming pipeline that substantially reduces the latency to the first
> response. To enhance this lightweight execution, ELSA introduces a bundled address event
> representation protocol to lower communication traffic of network-on-chip (NoC), and
> leverages mini-batch spiking Gustavson-product to cut memory access and exploit inherent
> sparsity. Combined with mapping and scheduling optimizations, ELSA achieves efficient,
> event-driven computation without compromising accuracy. Experiments show that SNNs can
> outperform quantized artificial neural networks (QANNs) while maintaining on-par accuracy.
> For a 4-bit ResNet-50, ELSA achieves 3.4× speedup and 13.6× higher energy efficiency over
> the SOTA QANN accelerator (ANT), and 2.9× speedup and 22.1× energy efficiency gains over
> the SOTA SNN accelerator (PAICORE).
