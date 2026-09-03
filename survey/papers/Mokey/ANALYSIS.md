# Mokey — paper notes

**Mokey: Enabling Narrow Fixed-Point Inference for Out-of-the-Box Floating-Point Transformer Models**
Ali Hadi Zadeh, Mostafa Mahmoud, Ameer Abdelhadi, Andreas Moshovos
**ISCA 2022** ｜ DOI: **not recorded** — the ACM/IEEE record is not reachable by script (403); look it up when citing
Venue evidence (2026-09-02): arXiv `comments` field, verbatim: *"Accepted at the 49th IEEE/ACM International Symposium on Computer Architecture (ISCA '22)"*
Archived here: **arXiv:2203.12758v1** (2022-03-23), 14 pages — **the preprint, not the
published ISCA 2022 version**; the two were **not compared**.

Status: **brief ready** ｜ Last updated: 2026-09-02
Tags: `non-analytical-dtype` `new-data-type` `lut-accelerator` `combined-dtype` `accelerator`
How far it was read: **abstract, introduction, section map, headline result sentences and
conclusion.** The method and evaluation sections were **not** read line by line, and no numbers
have been transcribed into the table below with their full frame — so this stays `brief ready`.
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> Original: https://arxiv.org/abs/2203.12758
> The PDF is **not committed** (1.4 MB). Re-download: `curl -sSL -o 2203.12758.pdf https://arxiv.org/pdf/2203.12758`
> Extract text: `python3 extract.py` → `extracted/` (committed, greppable)
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, ISCA 2022 row.

---

## Brief

### 1. Motivation

Transformer models are large and getting larger, and for long sequences **activations
dominate the footprint** (past 512 tokens in BERT-Large). Quantization helps, but most
methods need fine-tuning — and the training resources or datasets are often simply
unavailable to whoever is deploying the model.

### 2. Overview

Quantize every value to a **4-bit index into a dictionary of representative 16-bit fixed-
point centroids**, with **no fine-tuning**. The trick that makes it a hardware paper:
centroids are chosen to also fit an exponential curve, so most of the original multiply-
accumulates can be replaced by **narrow 3-bit fixed-point additions**. Can also serve purely
as a memory-compression front-end for another accelerator.

### 3. Pros and cons

**Pros**

- No fine-tuning required — the paper is explicit that this is an accessibility argument,
not just a convenience, and it is within 1% of the FP baseline.
- The exponential-curve constraint on centroids is the elegant part: it turns a lookup-based
scheme into an **arithmetic** simplification rather than just a storage one.
- Order-of-magnitude energy-efficiency improvement over a Tensor Cores baseline with 4–15×
performance depending on model and buffer size; optionally deployable as a compression
assist, which lowers the adoption barrier.

**Cons**

- Dictionary-based (non-analytical) representation means codebook storage, lookup traffic
and a calibration step — costs that scale with how many dictionaries you keep.
- Outliers still need separate handling (~2.5% of values in the worst case), so the clean
"everything is a 4-bit index" story has an exception.
- Evaluated on BERT-class encoder models; generative LLM decoding, where the memory-
boundedness is different, is not covered.

### 4. Where it applies

The earliest **§1.3 lookup-table** entry in the corpus and the direct ancestor of the
2025–26 LUT thread ([`LUTTensorCore`](../LUTTensorCore/ANALYSIS.md),
[`OASIS`](../OASIS/ANALYSIS.md), [`EVA`](../EVA/ANALYSIS.md)). Read it first in that group.

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

> **Keywords:** quantizing all values to 4-bit indexes into dictionaries of representative 16-bit fixed-point centroids; Golden Dictionary generation


## Abstract (verbatim, arXiv:2203.12758v1)

> Increasingly larger and better Transformer models keep advancing state-of-the-art accuracy
> and capability for Natural Language Processing applications. These models demand more
> computational power, storage, and energy. Mokey reduces the footprint of state-of-the-art
> 32-bit or 16-bit floating-point transformer models by quantizing all values to 4-bit
> indexes into dictionaries of representative 16-bit fixed-point centroids. Mokey does not
> need fine-tuning, an essential feature as often the training resources or datasets are not
> available to many. Exploiting the range of values that naturally occur in transformer
> models, Mokey selects centroid values to also fit an exponential curve. This unique
> feature enables Mokey to replace the bulk of the original multiply-accumulate operations
> with narrow 3b fixed-point additions resulting in an area- and energy-efficient hardware
> accelerator design. Over a set of state-of-the-art transformer models, the Mokey
> accelerator delivers an order of magnitude improvements in energy efficiency over a Tensor
> Cores-based accelerator while improving performance by at least $4\times$ and as much as
> $15\times$ depending on the model and on-chip buffering capacity. Optionally, Mokey can be
> used as a memory compression assist for any other accelerator, transparently stashing wide
> floating-point or fixed-point activations or weights into narrow 4-bit indexes. Mokey
> proves superior to prior state-of-the-art quantization methods for Transformers.
