# JPEG-ACT — paper notes

**JPEG-ACT: Accelerating Deep Learning via Transform-Based Lossy Compression**
R. David Evans, Lufei Liu, Tor M. Aamodt
**ISCA 2020**, pp. 860-873 ｜ DOI: **10.1109/ISCA45697.2020.00075**
Publication info verified 2026-09-02: **the archived PDF carries no DOI and no IEEE banner**
(grepped, not assumed) — venue and title come from its own page 1; **DOI and page range come
from the IEEE Xplore record surfaced via search**, and are second-hand.
Archived here: an **author-hosted copy, not the IEEE version** — no IEEE proceedings banner on page 1, and the filename is the author's.
The two versions were **not compared**. 14 pages.

Status: **brief ready** ｜ Last updated: 2026-09-02
Tags: `training` `gpu-kernels` `accelerator`
How far it was read: **abstract, introduction, section map, headline result sentences and
conclusion.** The method and evaluation sections were **not** read line by line, and no numbers
have been transcribed into the table below with their full frame — so this stays `brief ready`.
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> Publisher record: https://ieeexplore.ieee.org/document/9138963/
> **There is no arXiv version** (arXiv API title search, 2026-09-02). The PDF was downloaded by a
> human and filed through [`survey/uploads/`](../../uploads/) — the sanctioned route when the
> arXiv-only rule leaves a paper unreachable; see
> [`Notes-002`](../../../Claude/notes/Notes-002-paper-source-access.md).
> The PDF is **not committed** (1.8 MB) and **cannot be re-downloaded by script** —
> both publishers 403. Re-extract with `python3 extract.py` → `extracted/` (committed).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, ISCA 2020 row.

---

## Brief

### 1. Motivation

Training large CNNs requires stashing activations that exceed GPU memory (ResNet50/ImageNet
needs >40 GB), so they are offloaded to CPU memory — and the transfer, not the compute,
becomes the cost. Prior activation compression relied on sparsity, which deep ResNets do not
have.

### 2. Overview

A **lossy** activation offload accelerator that exploits *spatial correlation* in CNN
activations rather than sparsity: it adapts the JPEG image-compression pipeline (DCT-style
transform, quantization, entropy coding) to activation tensors, with modifications to keep
training convergent and accurate.

### 3. Pros and cons

**Pros**

- The right insight for the right workload — CNN activations look like images, so an image
codec is a natural fit, and it works where sparsity-based schemes have nothing to exploit.
- 2.4× training performance over prior offload accelerators and 1.6× over prior activation
compression, at **<1% of the power and area of a modern GPU**.
- Explicitly engineers for convergence rather than just reporting final accuracy — the right
standard for a lossy method applied during training.

**Cons**

- The spatial-correlation premise is CNN-specific; transformer activations have no analogous
2D structure, so this does not carry to LLM training.
- Lossy compression inside the training loop is a convergence risk that has to be re-
established per model family; the paper shows it for its own set, not in general.
- The source list flags it as compressing **"spatio info instead of values"** — it is
orthogonal to the data-type axis of the taxonomy.

### 4. Where it applies

The lossy counterpart to [`Gist`](../Gist/ANALYSIS.md) in the **training + compression**
cluster, and a good illustration that *what* is redundant depends on the workload's
structure, not just its numeric range.

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

> **Keywords:** a lossy activation offload accelerator for training CNNs; adapts JPEG algorithm for activation compression
>
> **Comment:** Compress Spatio Info instead of values

## Abstract (verbatim, from the archived PDF)

> A reduction in the time it takes to train machine learning models can be translated into
> improvements in accuracy. An important factor that increases training time in deep neural
> networks (DNNs) is the need to store large amounts of temporary data during the back-
> propagation algorithm. To enable training very large models this temporary data can be
> offloaded from limited size GPU memory to CPU memory but this data movement incurs large
> performance overheads. We observe that in one important class of DNNs, convolutional
> neural networks (CNNs), there is spatial correlation in these temporary values. We propose
> JPEG for ACTivations (JPEGACT), a lossy activation offload accelerator for training CNNs
> that works by discarding redundant spatial information. JPEGACT adapts the well-known JPEG
> algorithm from 2D image compression to activation compression. We show how to optimize the
> JPEG algorithm so as to ensure convergence and maintain accuracy during training. JPEG-ACT
> achieves 2.4× higher training performance compared to prior offload accelerators, and 1.6×
> compared to prior activation compression methods. An efficient hardware implementation
> allows JPEG-ACT to consume less than 1% of the power and area of a modern GPU.
