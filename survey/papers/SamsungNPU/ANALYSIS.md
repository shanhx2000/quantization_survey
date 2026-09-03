# SamsungNPU — paper notes

**Sparsity-Aware and Re-Configurable NPU Architecture for Samsung Flagship Mobile SoC**
Authors: **not transcribed** — a large industrial author list; read it off page 1 of the PDF before citing.
**ISCA 2021** ｜ DOI: **10.1109/ISCA52012.2021.00011**
Publication info verified 2026-09-02: venue, year **and DOI** all read out of the archived
PDF's own text (IEEE proceedings banner; the DOI was grepped for, not assumed); page range
from the IEEE Xplore link in the source CSV.
Archived here: the **published IEEE version** (the page-1 IEEE proceedings banner is present in the extracted text), 14 pages.

Status: **brief ready** ｜ Last updated: 2026-09-02
Tags: `analytical-dtype` `mixed-precision` `multi-bitwidth-hw` `accelerator`
How far it was read: **abstract, introduction, section map, headline result sentences and
conclusion.** The method and evaluation sections were **not** read line by line, and no numbers
have been transcribed into the table below with their full frame — so this stays `brief ready`.
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> Publisher record: https://ieeexplore.ieee.org/document/9499876
> **There is no arXiv version** (arXiv API title search, 2026-09-02). The PDF was downloaded by a
> human and filed through [`survey/uploads/`](../../uploads/) — the sanctioned route when the
> arXiv-only rule leaves a paper unreachable; see
> [`Notes-002`](../../../Claude/notes/Notes-002-paper-source-access.md).
> The PDF is **not committed** (2.7 MB) and **cannot be re-downloaded by script** —
> both publishers 403. Re-extract with `python3 extract.py` → `extracted/` (committed).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, ISCA 2021 row.

---

## Brief

### 1. Motivation

A commercial mobile NPU must run a *comprehensive range* of networks under a fixed power and
area budget — two goals that pull against each other. Academic accelerators optimize one
workload; a flagship SoC cannot.

### 2. Overview

An **industrial product paper** on the NPU in a Samsung flagship SoC (5 nm): an adder-tree
inner-product engine that skips zeros in the input feature map, a **re-configurable MAC
array**, dynamic internal memory-port assignment for bandwidth, and an architecture
supporting **mixed-precision (INT8/INT16)** arithmetic. Includes a lessons-learned section.

### 3. Pros and cons

**Pros**

- Silicon measurements, not simulation: **290.7 FPS and 13.6 TOPS/W** on 8-bit Inception-v3
with one core; 1.79× over the dense baseline from the combined optimizations.
- The lessons-learned section is unusually candid and is the most citable part — e.g. that
*limiting* reconfigurability costs little performance but saves significant area.
- Zero-skipping is analysed at two granularities (intra- and inter-lane) with the trade-offs
quantified rather than asserted.

**Cons**

- Mixed-precision support is one feature among several; the paper is about the whole NPU, so
the quantization content is thin relative to its neighbours here.
- As a product paper, design choices are reported rather than ablated against alternatives
that were not built.
- INT8/INT16 is a narrow precision range by 2026 standards — no sub-8-bit story.

### 4. Where it applies

Industrial calibration for the **multi-bitwidth hardware** box: what reconfigurability a
shipping mobile NPU actually pays for, versus what research designs propose. Pair with
[`TPUv4i`](../TPUv4i/ANALYSIS.md) and [`RaPiD`](../RaPiD/ANALYSIS.md).

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

## Note from the source list

> **Keywords:** Has a section discussing supports for Mixed-precision (int8 & int16)


## Abstract (verbatim, from the archived PDF)

> Of late, deep neural networks have become ubiquitous in mobile applications. As mobile
> devices generally require immediate response while maintaining user privacy, the demand
> for on-device machine learning technology is on the increase. Nevertheless, mobile devices
> suffer from restricted hardware resources, whereas deep neural networks involve
> considerable computation and communication. Therefore, the implementation of a neural-
> network specialized hardware accelerator, generally called neural processing unit (NPU),
> has started to gain attention for the mobile application processor (AP). However, NPUs for
> commercial mobile AP face two challenges that are difficult to realize simultaneously:
> execution of a wide range of applications and efficient performance. In this paper, we
> propose a flexible but efficient NPU architecture for a Samsung flagship mobile system-on-
> chip (SoC). To implement an efficient NPU, we design an energy-efficient innerproduct
> engine that utilizes the input feature map sparsity. We propose a re-configurable MAC
> array to enhance the flexibility of the proposed NPU, dynamic internal memory port
> assignment to maximize on-chip memory bandwidth utilization, and efficient architecture to
> support mixed-precision arithmetic. We implement the proposed NPU using the Samsung 5nm
> library. Our silicon measurement experiments demonstrate that the proposed NPU achieves
> 290.7 FPS and 13.6 TOPS/W, when executing an 8-bit quantized Inception-v3 model [1] with a
> single NPU core. In addition, we analyze the proposed zero-skipping architecture in
> detail. Finally, we present the findings and lessons learned when implementing the
> commercial mobile NPU and interesting avenues for future work.
