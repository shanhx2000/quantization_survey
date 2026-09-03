# MXFFP — paper notes

**MXFFP: Microscaling Flexible Floating Point Format for Large-Scale AI Model Acceleration**
Sungwoo Kim, Sungbin Kim, Dongho Ha, Hyunwuk Lee, Junsung Kim, Seunghyun Lee, Mingu Jung,
Murali Annavaram, Won Woo Ro
**ISCA 2026** (2026 ACM/IEEE 53rd Annual International Symposium on Computer Architecture),
pp. 2505–2519 ｜ DOI: **10.1109/ISCA66397.2026.00175**
Publication info verified 2026-09-02 from the **official ISCA 2026 proceedings package**
(title, authors, pages, DOI and abstract all read from its `assets/data/data.js`).
Archived here: **the published proceedings PDF** (`506501c505.pdf`, 15 pages) — not a preprint.

Status: **brief ready** ｜ Last updated: 2026-09-02
Tags: `new-data-type` `analytical-dtype` `dtype-granularity` `accelerator`
How far it was read: **abstract, introduction, section map, headline result sentences and
conclusion.** The method and evaluation sections were **not** read line by line, and no numbers
have been transcribed into the table below with their full frame — so this stays `brief ready`.
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> The PDF is **not committed** (1.7 MB). It came from the proceedings package a human
> supplied, now archived at [`archieve/ISCA 2026.zip`](../../../archieve/), entry `pdfs/5065-3nexm57sBmVa6MJtFTiSrb/506501c505/506501c505.pdf`.
> **There is no public URL for it** — this is not an arXiv paper. Re-extract with
> `python3 extract.py` → `extracted/` (committed, greppable).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, 2026 row.

---

## Brief

### 1. Motivation

Microscaling floating point (MXFP) groups values into blocks sharing a common exponent,
which shrinks memory and suits hardware. But the trend — **fewer bits, larger blocks** —
creates growing **inter-block** and **intra-block** value diversity: a fixed
exponent/mantissa split must trade range against precision across blocks, and packing more
values per block amplifies variation within one.

### 2. Overview

Stop using one fixed configuration. **MXFFP** assigns exponent and mantissa bits **flexibly,
at both block and sub-block level**, to match each block's (or element's) actual value
distribution. Contributes conversion mechanisms from FP16/BF16 with minimal runtime overhead
and a Tensor-Core-based architecture that interprets the format using **a single
configuration bit per block**.

### 3. Pros and cons

**Pros**

- The one-configuration-bit encoding is what makes the idea cheap enough to be real —
flexibility usually costs metadata, and here it costs almost nothing.
- Attacks both diversity axes (inter- and intra-block) rather than just one, which is why it
can keep larger block sizes usable.
- 2–5× perplexity reduction in 4-bit settings across multiple LLMs **at hardware performance
comparable to MXFP** — an accuracy gain that is close to free.

**Cons**

- Choosing the per-block configuration is a fitting problem; the paper's MSE comparisons
show it works but the selection cost and its input-dependence deserve scrutiny on a close
read.
- Benefit is largest exactly where MXFP is weakest (4-bit, large blocks); at more generous
settings the margin should shrink.
- Still within the exponent/mantissa family — a flexible reallocation of fields rather than
a departure from the analytical form.

### 4. Where it applies

The purest **§1.2 new-analytical-data-type** entry in the corpus, and directly relevant to
the microscaling/NVFP4 direction the industry is moving in. Read with
[`MicroScopiQ`](../MicroScopiQ/ANALYSIS.md), which combines microscaling with outlier
handling instead of with field flexibility.

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

> The rise of AI/ML applications has reignited interest in floating-point formats beyond the
> IEEE 754 standard, leading to innovations such as Microscaling Floating-Point (MXFP). MXFP
> groups values into blocks that share a common exponent, allowing them to be represented as
> scaled FP values. This enables a reduced memory footprint and efficient hardware
> execution. However, due to the trend of shrinking bit-widths and increasing block sizes,
> MXFP faces growing inter-block and intra-block value diversity. The limited number of
> exponent and mantissa bits forces a tradeoff between range and precision across blocks,
> while packing more values into a block amplifies the variation within each block. As a
> result, fewer bits with larger blocks often lead to precision loss and degraded model
> accuracy. In this paper, we observe that these limitations can be addressed by flexibly
> assigning exponent and mantissa bits to match the value distribution of each block or
> element within a block, rather than relying on a single fixed MXFP configuration. Based on
> this observation, we propose MXFFP, a flexible numeric format that leverages diverse
> exponent-mantissa configurations at both the block and sub-block levels. This diversity
> allows MXFFP to better preserve the original value distribution, leading to higher
> inference accuracy for ML models even with larger block sizes. To support this format, we
> introduce efficient conversion mechanisms that transform FP16/BF16 values into MXFFP with
> a minimal runtime overhead and design a Tensor Core based hardware architecture that
> interprets and executes MXFFP using only a single configuration bit per block. Our
> evaluation shows that MXFFP significantly improves numerical accuracy, reducing perplexity
> by 2–5× in 4-bit settings across multiple LLMs, while maintaining hardware performance
> comparable to MXFP.
