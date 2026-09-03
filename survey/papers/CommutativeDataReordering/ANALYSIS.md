# CommutativeDataReordering — paper notes

**Commutative Data Reordering: A New Technique to Reduce Data Movement Energy on Sparse Inference Workloads**
Ben Feinberg, Benjamin C. Heyman, Darya Mikhailenko, Ryan Wong, An C. Ho, Engin Ipek
**ISCA 2020** ｜ DOI: **10.1109/ISCA45697.2020.00091**
Publication info verified 2026-09-02: venue, year **and DOI** all read out of the archived
PDF's own text (IEEE proceedings banner; the DOI was grepped for, not assumed); page range
from the IEEE Xplore record.
Archived here: the **published IEEE version** (the page-1 IEEE proceedings banner is present in the extracted text), 13 pages.

Status: **brief ready** ｜ Last updated: 2026-09-02
Tags: `lossless-compression` `gpu-kernels` `accelerator`
How far it was read: **abstract, introduction, section map, headline result sentences and
conclusion.** The method and evaluation sections were **not** read line by line, and no numbers
have been transcribed into the table below with their full frame — so this stays `brief ready`.
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> Publisher record: https://ieeexplore.ieee.org/document/9138978/
> **There is no arXiv version** (arXiv API title search, 2026-09-02). The PDF was downloaded by a
> human and filed through [`survey/uploads/`](../../uploads/) — the sanctioned route when the
> arXiv-only rule leaves a paper unreachable; see
> [`Notes-002`](../../../Claude/notes/Notes-002-paper-source-access.md).
> The PDF is **not committed** (0.9 MB) and **cannot be re-downloaded by script** —
> both publishers 403. Re-extract with `python3 extract.py` → `extracted/` (committed).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, ISCA 2020 row.

---

## Brief

### 1. Motivation

On interconnects where transmitting a 1 costs more than a 0, data movement energy is reduced
by encoding to minimize 1s. Prior encodings (DBI, Base+XOR) ignore application semantics.
The observation: in a dot product, **the order in which weights are fetched does not affect
the result**, so the order is free to optimize.

### 2. Overview

Commutative Data Reordering picks a low-energy fetch order for sparse weight matrices by
modelling ordering as a **Travelling Salesman / Capacitated Vehicle Routing** problem and
reusing the mature approximation literature. Crucially it hides the chosen order in the
indirection that sparse formats already carry, so **no extra metadata** is needed.

### 3. Pros and cons

**Pros**

- A clean, genuinely novel degree of freedom — exploiting algebraic commutativity for an
energy win is the kind of insight that is obvious only afterwards.
- Near-free in hardware: **<0.01% area** on a mobile-class GPU, no system-software changes,
and no runtime performance penalty at the stride sizes it restricts itself to.
- Honest about the size of the win: 53.1% DRAM **IO** energy reduction over DBI, but only
~5.7% average *total* DRAM energy — the paper reports both.

**Cons**

- The benefit is entirely conditional on an asymmetric-energy interconnect; on a
conventional bus it buys nothing.
- Depends on sparsity for the metadata-free trick, so it does not apply to dense quantized
tensors.
- Solution quality barely improves with better solvers (1.8% best case over greedy), which
suggests the achievable headroom is nearly exhausted at low effort.

### 4. Where it applies

Peripheral to quantization but a good exhibit for the survey's **data-movement** thread: it
changes neither the values nor their encoding width, only their order. Group with
[`SpZip`](../SpZip/ANALYSIS.md) and
[`IBMCompressionAccelerator`](../IBMCompressionAccelerator/ANALYSIS.md).

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

> **Keywords:** minimize 1s in transmission; use XOR to encode positions of non-zero values


## Abstract (verbatim, from the archived PDF)

> Data movement is a significant and growing consumer of energy in modern systems, from
> specialized low-power accelerators to GPUs with power budgets in the hundreds of Watts.
> Given the importance of the problem, prior work has proposed designing interconnects on
> which the energy cost of transmitting a 0 is significantly lower than that of transmitting
> a 1. With such an interconnect, data movement energy is reduced by encoding the
> transmitted data such that the number of 1s is minimized. Although promising, these data
> encoding proposals do not take full advantage of application level semantics. As an
> example of a neglected optimization opportunity, consider the case of a dot product
> computation as part of a neural network inference task. The order in which the neural
> network weights are fetched and processed does not affect correctness, and can be
> optimized to further reduce data movement energy. This paper presents commutative data
> reordering (CDR), a hardware-software approach that leverages the commutative property in
> linear algebra to strategically select the order in which weight matrix coefficients are
> fetched from memory. To find a low-energy transmission order, weight ordering is modeled
> as an instance of one of two well-studied problems, the Traveling Salesman Problem and the
> Capacitated Vehicle Routing Problem. This reduction makes it possible to leverage the vast
> body of work on efficient approximation methods to find a good transmission order. CDR
> exploits the indirection inherent to sparse matrix formats such that no additional
> metadata is required to specify the selected order. The hardware modifications required to
> support CDR are minimal, and incur an area penalty of less than 0.01% when implemented on
> top of a mobile-class GPU. When applied to 7 neural network inference tasks running on a
> GPU-based system, CDR respectively reduces average DRAM IO energy by 53.1% and 22.2% over
> the data bus invert encoding scheme used by LPDDR4, and the recently proposed Base+XOR
> encoding. These savings are attained with no changes to the mobile system software and no
> runtime performance penalty.
