# RAELLA — paper notes

**RAELLA: Reforming the Arithmetic for Efficient, Low-Resolution, and Low-Loss Analog PIM: No Retraining Required!**
Tanner Andrulis, Joel S. Emer, Vivienne Sze
**ISCA 2023** ｜ DOI: **not recorded** — the ACM/IEEE record is not reachable by script (403); look it up when citing
Venue evidence (2026-09-02): arXiv `comments` field, verbatim: *"16 pages; 15 figures; Accepted at ISCA 2023 (the International Symposium on Computer Architecture)"*
Archived here: **arXiv:2304.07935v1** (2023-04-17), 16 pages — **the preprint, not the
published ISCA 2023 version**; the two were **not compared**.

Status: **brief ready** ｜ Last updated: 2026-09-02
Tags: `pim-ndp` `combined-dtype` `dtype-granularity` `multi-bitwidth-hw` `accelerator`
How far it was read: **abstract, introduction, section map, headline result sentences and
conclusion.** The method and evaluation sections were **not** read line by line, and no numbers
have been transcribed into the table below with their full frame — so this stays `brief ready`.
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> Original: https://arxiv.org/abs/2304.07935
> The PDF is **not committed** (2.6 MB). Re-download: `curl -sSL -o 2304.07935.pdf https://arxiv.org/pdf/2304.07935`
> Extract text: `python3 extract.py` → `extracted/` (committed, greppable)
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, ISCA 2023 row.

---

## Brief

### 1. Motivation

Analog processing-in-memory should be efficient — ReRAM crossbars compute densely in place —
but **ADCs dominate the energy**, so much that some PIM accelerators do not beat digital
ones. Existing fixes either lower ADC resolution (losing fidelity) or prune/retrain the DNN,
and **retraining may be impossible** when training data is private or the training recipe is
model-specific.

### 2. Overview

Adapt the *arithmetic* to the architecture so that analog values are small and thus cheap to
digitize: **encode weights to produce near-zero analog values** (Center+Offset),
**adaptively slice weights** per layer, and **dynamically slice inputs** with speculation
and recovery. Low-resolution analog values then permit low-resolution ADCs and fewer
converts, with no retraining.

### 3. Pros and cons

**Pros**

- "No retraining required" is the load-bearing claim and the paper argues for it as a
deployability property, not a convenience — a well-made point about who can actually use a
technique.
- Up to 4.9× energy efficiency and 3.3× throughput over other low-accuracy-loss PIM
accelerators, and it matches retraining-based designs *without* retraining.
- The Center+Offset encoding is a nice instance of representing a value as two components
chosen to suit the physics — a combined data type driven by hardware, not statistics.

**Cons**

- Entirely within the ReRAM analog-PIM setting, which carries device non-idealities, write
costs and maturity questions the paper mitigates but cannot remove.
- Speculation-and-recovery for input slicing implies a variable-cost path; worst-case
behaviour is less visible than the average results shown.
- Evaluated on CNN-era models; nothing here about transformers or LLM-scale weights.

### 4. Where it applies

The **analog PIM** entry in the corpus, and a useful counterexample: it shows the constraint
driving the data-type design can be a *circuit* constraint (ADC resolution) rather than a
statistical one. Read with [`P3-LLM`](../P3-LLM/ANALYSIS.md) and
[`NDPLowBitFP`](../NDPLowBitFP/ANALYSIS.md) for the digital PIM/NDP contrast.

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

> **Keywords:** encoding weights to produce near-zero analog values; Center+Offset


## Abstract (verbatim, arXiv:2304.07935v1)

> Processing-In-Memory (PIM) accelerators have the potential to efficiently run Deep Neural
> Network (DNN) inference by reducing costly data movement and by using resistive RAM
> (ReRAM) for efficient analog compute. Unfortunately, overall PIM accelerator efficiency is
> limited by energy-intensive analog-to-digital converters (ADCs). Furthermore, existing
> accelerators that reduce ADC cost do so by changing DNN weights or by using low-resolution
> ADCs that reduce output fidelity. These strategies harm DNN accuracy and/or require costly
> DNN retraining to compensate. To address these issues, we propose the RAELLA architecture.
> RAELLA adapts the architecture to each DNN; it lowers the resolution of computed analog
> values by encoding weights to produce near-zero analog values, adaptively slicing weights
> for each DNN layer, and dynamically slicing inputs through speculation and recovery. Low-
> resolution analog values allow RAELLA to both use efficient low-resolution ADCs and
> maintain accuracy without retraining, all while computing with fewer ADC converts.
> Compared to other low-accuracy-loss PIM accelerators, RAELLA increases energy efficiency
> by up to 4.9$\times$ and throughput by up to 3.3$\times$. Compared to PIM accelerators
> that cause accuracy loss and retrain DNNs to recover, RAELLA achieves similar efficiency
> and throughput without expensive DNN retraining.
