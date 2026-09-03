# ENEC — paper notes

**ENEC: A Lossless AI Model Compression Method Enabling Fast Inference on Ascend NPUs**
Jinwu Yang, Jiaan Wu, Zedong Liu, Xinyang Ma, Hairui Zhao, Yida Gu, Yuanhong Huang, Xingchen
Liu, Wenjing Huang, Zheng Wei, Jing Xing, Yili Ma, Qingyi Zhang, Baoyi An, Zhongzhe Hu,
Shaoteng Liu, Xia Zhu, Jiaxun Lu, Guangming Tan, Dingwen Tao
**ISCA 2026** (2026 ACM/IEEE 53rd Annual International Symposium on Computer Architecture),
pp. 1319–1335 ｜ DOI: **10.1109/ISCA66397.2026.00100**
Publication info verified 2026-09-02 from the **official ISCA 2026 proceedings package**
(title, authors, pages, DOI and abstract all read from its `assets/data/data.js`).
Archived here: **the published proceedings PDF** (`506501b319.pdf`, 17 pages) — not a preprint.

Status: **brief ready** ｜ Last updated: 2026-09-02
Tags: `lossless-compression` `accelerator`
How far it was read: **abstract, introduction, section map, headline result sentences and
conclusion.** The method and evaluation sections were **not** read line by line, and no numbers
have been transcribed into the table below with their full frame — so this stays `brief ready`.
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> The PDF is **not committed** (2.4 MB). It came from the proceedings package a human
> supplied, now archived at [`archieve/ISCA 2026.zip`](../../../archieve/), entry `pdfs/5065-3nexm57sBmVa6MJtFTiSrb/506501b319/506501b319.pdf`.
> **There is no public URL for it** — this is not an arXiv paper. Re-extract with
> `python3 extract.py` → `extracted/` (committed, greppable).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, 2026 row.

---

## Brief

### 1. Motivation

On Ascend NPUs, weight transfer is the bottleneck — memory access is **78–85% of inference
latency** for Qwen3-32B, and models that exceed HBM must be split across CPU and NPU, making
CPU→NPU transfer dominant (nearly 80% of execution time for some Falcon layers at batch 4).
Lossless compression would preserve accuracy exactly, but existing lossless algorithms
collapse to very low throughput when ported to Ascend's SIMD architecture.

### 2. Overview

A **lossless** compression method purpose-built for AI model weights and for the Ascend
NPU's constraints: block-based fixed-length encoding, plus bit-width quantization with
hierarchical halving bit-packing, vectorized branch-free integer transformation, and a
dependency-decoupled intra-segment scan (the classic serial-dependency problem in entropy
coding).

### 3. Pros and cons

**Pros**

- **Lossless** — no accuracy question at all, which makes it complementary to, not competing
with, every quantization entry in the corpus.
- The optimizations are specific to a real architectural mismatch, and the throughput result
shows it mattered: 372 GB/s on BF16, 987× ZipNN (best CPU) and 3.43× DietGPU, with 1.12×
better compression ratio than nvCOMP.
- End-to-end gains on real models — up to 6.3× TTFT and 4.9× TPOT reduction on Falcon40B —
and it is open-source, the first such for Ascend.

**Cons**

- Vendor-specific: the optimizations are shaped by Ascend's SIMD design, so the throughput
results do not transfer to other accelerators.
- Lossless compression ratios on weights are inherently modest compared with quantization;
the win is bandwidth, not capacity of the kind 4-bit quantization delivers.
- The gains are largest in the CPU–NPU offload regime; if the model fits in HBM the
motivation weakens considerably.

### 4. Where it applies

The modern, ML-specific counterpart to
[`IBMCompressionAccelerator`](../IBMCompressionAccelerator/ANALYSIS.md) in the **lossless-
compression** cluster, and a useful reminder for the survey that not every memory-wall
answer is a quantization answer.

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

> The rapid scaling of Large Language Models presents significant challenges for their
> deployment and inference, particularly on resource-constrained specialized AI hardware
> accelerators such as Huawei's Ascend NPUs, where weight transfer has become a critical
> performance bottleneck. While lossless compression can preserve model accuracy and reduce
> data volume, existing lossless compression algorithms exhibit extremely low throughput
> when ported to the Ascend NPUs. In this paper, we propose ENEC, a novel lossless
> compression method specifically customized for AI model weights and optimized for Ascend
> Neural Processing Units. ENEC adopts a block-based fixed-length encoding scheme and
> incorporates a series of optimizations: bit-width quantization with hierarchical halving
> bit-packing, vectorized branch-free integer transformation, and dependency-decoupled
> intra-segment scan. Experimental results demonstrate that ENEC outperforms existing state-
> of-the-art NPU compressors in both compression ratio and throughput. Compared to leading
> GPU solutions, ENEC achieves a 3.43× higher throughput than DietGPU and a 1.12× better
> compression ratio than nvCOMP. By reducing weight transmission overhead, ENEC
> significantly improves end-to-end inference performance, achieving up to a 6.3× speedup.
> On Ascend NPUs, ENEC is the first open-source lossless compression algorithm for model
> weights that achieves performance comparable to state-of-the-art GPU compressors, offering
> an effective solution for deploying large-scale AI models.
