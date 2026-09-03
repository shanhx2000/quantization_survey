# Tender — paper notes

**Tender: Accelerating Large Language Models via Tensor Decomposition and Runtime Requantization**
Jungi Lee, Wonbeom Lee, Jaewoong Sim
**ISCA 2024** ｜ DOI: **not recorded** — the ACM/IEEE record is not reachable by script (403); look it up when citing
Venue evidence (2026-09-02): arXiv `comments` field, verbatim: *"To appear at the 51st International Symposium on Computer Architecture (ISCA 2024)"*
Archived here: **arXiv:2406.12930v1** (2024-06-16), 15 pages — **the preprint, not the
published ISCA 2024 version**; the two were **not compared**.

Status: **brief ready** ｜ Last updated: 2026-09-02
Tags: `analytical-dtype` `dtype-granularity` `mixed-precision` `accelerator`
How far it was read: **abstract, introduction, section map, headline result sentences and
conclusion.** The method and evaluation sections were **not** read line by line, and no numbers
have been transcribed into the table below with their full frame — so this stays `brief ready`.
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> Original: https://arxiv.org/abs/2406.12930
> The PDF is **not committed** (3.3 MB). Re-download: `curl -sSL -o 2406.12930.pdf https://arxiv.org/pdf/2406.12930`
> Extract text: `python3 extract.py` → `extracted/` (committed, greppable)
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, ISCA 2024 row.

---

## Brief

### 1. Motivation

Past ~6.7B parameters, a few activation feature dimensions carry extreme-magnitude outliers
that widen the quantization range and force higher bitwidths. Software-only fixes are too
slow or too lossy at 4 bits; existing co-designs need **mixed-precision compute units or
custom datatypes commodity hardware does not support**.

### 2. Overview

Split the activation tensor into subtensors along the **channel** dimension so each groups
elements of similar range, and quantize each with its own scale. The trick that makes it
cheap: choose the scale factors to be **powers of two apart**, so accumulating partial sums
across subtensors needs only a shift — **no explicit requantization** — which is a minimal
extension to commodity tensor hardware.

### 3. Pros and cons

**Pros**

- The least intrusive design in the outlier thread: it deliberately avoids custom datatypes
and mixed-precision units, so it can ride existing integer pipelines. That restraint is
the contribution.
- The power-of-two-apart constraint is the elegant step — it converts an expensive
dequantize/requantize into a shift, turning a scheme that would be impractical into one
that is nearly free.
- Reports higher accuracy *and* higher performance than the state of the art it compares
against, including [`OliVe`](../OliVe/ANALYSIS.md) and SmoothQuant on perplexity.

**Cons**

- Channel-grouping requires knowing which channels hold outliers, i.e. a
calibration/profiling step whose stability across inputs is assumed rather than stress-
tested here.
- Constraining scales to powers of two is a real loss of representational freedom; the paper
argues the trade is favourable but the gap to unconstrained per-group scales is not
isolated.
- Later work ([`Omni-LUT`](../Omni-LUT/ANALYSIS.md), [`P3-LLM`](../P3-LLM/ANALYSIS.md)) uses
Tender as a baseline it beats, so its position is not final.

### 4. Where it applies

A key **§2.2 fine-grained / channel-wise** entry, and the corpus's best example of
*designing the algorithm around what existing hardware can already do*. Contrast directly
with [`OliVe`](../OliVe/ANALYSIS.md), which instead changes the encoding.

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

> **Keywords:** decomposed quantization technique in which the scale factors of decomposed matrices are powers of two apart.


## Abstract (verbatim, arXiv:2406.12930v1)

> Large language models (LLMs) demonstrate outstanding performance in various tasks in
> machine learning and have thus become one of the most important workloads in today's
> computing landscape. However, deploying LLM inference poses challenges due to the high
> compute and memory requirements stemming from the enormous model size and the difficulty
> of running it in the integer pipelines. In this paper, we present Tender, an algorithm-
> hardware co-design solution that enables efficient deployment of LLM inference at low
> precision. Based on our analysis of outlier values in LLMs, we propose a decomposed
> quantization technique in which the scale factors of decomposed matrices are powers of two
> apart. The proposed scheme allows us to avoid explicit requantization (i.e.,
> dequantization/quantization) when accumulating the partial sums from the decomposed
> matrices, with a minimal extension to the commodity tensor compute hardware. Our
> evaluation shows that Tender achieves higher accuracy and inference performance compared
> to the state-of-the-art methods while also being significantly less intrusive to the
> existing accelerators.
