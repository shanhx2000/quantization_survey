# AQuant — paper notes

**AQuant: Repurposing CODEC for VLM Acceleration via Adaptive Quantization**
Zhuoran Song, Chunyu Qi, Jian Weng, Xiaoyao Liang, Haibing Guan
**ISCA 2026** (2026 ACM/IEEE 53rd Annual International Symposium on Computer Architecture),
pp. 1417–1431 ｜ DOI: **10.1109/ISCA66397.2026.00106**
Publication info verified 2026-09-02 from the **official ISCA 2026 proceedings package**
(title, authors, pages, DOI and abstract all read from its `assets/data/data.js`).
Archived here: **the published proceedings PDF** (`506501b417.pdf`, 15 pages) — not a preprint.

Status: **brief ready** ｜ Last updated: 2026-09-02
Tags: `combined-dtype` `mixed-precision` `dtype-granularity` `accelerator`
How far it was read: **abstract, introduction, section map, headline result sentences and
conclusion.** The method and evaluation sections were **not** read line by line, and no numbers
have been transcribed into the table below with their full frame — so this stays `brief ready`.
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> The PDF is **not committed** (3.3 MB). It came from the proceedings package a human
> supplied, now archived at [`archieve/ISCA 2026.zip`](../../../archieve/), entry `pdfs/5065-3nexm57sBmVa6MJtFTiSrb/506501b417/506501b417.pdf`.
> **There is no public URL for it** — this is not an arXiv paper. Re-extract with
> `python3 extract.py` → `extracted/` (committed, greppable).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, 2026 row.

---

## Brief

### 1. Motivation

Vision-language model cost scales with image resolution and frame count, which blocks real-
time use. Two things prior quantization accelerators miss: **visual tokens are highly
similar to each other** (unlike LLM tokens), and the floating-point units used to convert
FP→INT are themselves expensive — quantization only applies to linear layers, yet precision-
critical non-linear ops (GELU, Softmax, LayerNorm) keep forcing casts back and forth.

### 2. Overview

Exploit the similarity by quantizing **deltas** between similar visual tokens rather than
the tokens themselves — a narrower distribution, so INT4/INT2 delta GEMM suffices. To avoid
paying for floating-point similarity detection, use **exponent-based** similarity detection.
Then the structural move: **repurpose the video CODEC already present in the SoC** to
perform similarity detection and adaptive quantization, paired with a mixed-precision NPU.

### 3. Pros and cons

**Pros**

- Reusing an idle on-chip CODEC is the kind of systems insight that costs almost nothing and
is easy to overlook — the hardware is already there in real SoCs.
- Delta quantization is well matched to the data: visual-token similarity is a property of
the modality, and the narrower delta distribution is what makes INT2 viable.
- Exponent-based detection removes exactly the FP overhead identified in the motivation;
4.5×/2.8×/6.9× speedups over LLM.265, CMC and an Xavier AGX GPU at negligible accuracy
loss.

**Cons**

- The whole premise depends on **visual** token similarity — it does not transfer to LLM
decoding, and the paper says so.
- Assumes a CODEC is present and available; on hardware without one, or where it is busy
with actual video, the argument weakens.
- Delta computation introduces a dependency between tokens, so the reported stalls and
synchronization in the pipeline are intrinsic rather than incidental.

### 4. Where it applies

The **VLM** entry, and the corpus's most creative instance of a **combined/residual data
type** (value = reference + delta). Compare with [`SingularBit`](../SingularBit/ANALYSIS.md)
and [`SmartExchange`](../SmartExchange/ANALYSIS.md), which decompose in different bases for
the same reason.

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

> Vision-Language Models (VLMs) have reached the forefront of accuracy in various vision
> understanding tasks. Despite their remarkable success, the computing costs of VLMs scale
> significantly with the high image resolutions or the increasing number of video frames
> that need to be processed, posing substantial challenges for deployment to real-time
> applications. Although specialized quantization accelerators have been developed, they may
> not be the optimal solutions due to their neglect of the inherent data similarity within
> VLMs. Additionally, the use of floating-point units for floating-point to integer
> conversion introduces non-negligible hardware overhead. This paper introduces Adaptive
> Quantization (AQuant), an algorithm-hardware co-design framework that repurposes the CODEC
> to accelerate VLM inference in an end-to-end and unified manner. AQuant leverages the
> inherent similarities in visual tokens, exploiting them for differential value (delta)
> generation, which is well-suited for dynamic quantization due to its narrower
> distribution. To eliminate the expensive floating-point similarity detection, AQuant
> integrates an exponent-based similarity detection operation. On the hardware side, we
> enhance the video CODEC's capabilities to efficiently implement exponent-similarity
> detection and adaptive quantization. The framework also incorporates a Neural Processing
> Unit (NPU) with mixed-precision support, which collaborates closely with the CODEC to
> translate algorithmic savings into real speedup. Experimental results show that AQuant
> achieves speedups of 4.5x, 2.8x, and 6.9x over state-of-the-art accelerators, such as
> LLM.265, CMC, and Xavier AGX GPU, with negligible accuracy loss.
