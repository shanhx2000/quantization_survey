# XtraMAC — paper notes

**XtraMAC: An Efficient MAC Architecture for Mixed-Precision LLM Inference on FPGA**
Feng Yu, Hongshi Tan, Yao Chen, Weng-Fai Wong, Bingsheng He
**ISCA 2026** (2026 ACM/IEEE 53rd Annual International Symposium on Computer Architecture),
pp. 2536–2549 ｜ DOI: **10.1109/ISCA66397.2026.00177**
Publication info verified 2026-09-02 from the **official ISCA 2026 proceedings package**
(title, authors, pages, DOI and abstract all read from its `assets/data/data.js`).
Archived here: **the published proceedings PDF** (`506501c536.pdf`, 14 pages) — not a preprint.

Status: **brief ready** ｜ Last updated: 2026-09-02
Tags: `multi-bitwidth-hw` `mixed-precision` `analytical-dtype` `accelerator`
How far it was read: **abstract, introduction, section map, headline result sentences and
conclusion.** The method and evaluation sections were **not** read line by line, and no numbers
have been transcribed into the table below with their full frame — so this stays `brief ready`.
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> The PDF is **not committed** (1.2 MB). It came from the proceedings package a human
> supplied, now archived at [`archieve/ISCA 2026.zip`](../../../archieve/), entry `pdfs/5065-3nexm57sBmVa6MJtFTiSrb/506501c536/506501c536.pdf`.
> **There is no public URL for it** — this is not an arXiv paper. Re-extract with
> `python3 extract.py` → `extracted/` (committed, greppable).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, 2026 row.

---

## Brief

### 1. Motivation

Real quantized checkpoints mix datatypes *within one forward pass*: Qwen3-8B-AWQ runs **over
68% of decode-stage MACs as INT4×BF16** in projection layers while attention stays
BF16×BF16, and GPT-oss uses MXFP4 in MoE blocks with BF16 elsewhere. So hardware must handle
both **mixed-precision operands** and **runtime datatype switching**. FPGA MAC designs fail
at this — fixed-datatype designs, inefficient sharing, and consequently under-utilized DSPs.

### 2. Overview

A single datatype-adaptive MAC microarchitecture that decomposes **every** supported format
— integer, floating point, mixed — into a **shared integer mantissa product** plus
lightweight sign and exponent handling. That shared core enables dynamic operand packing and
DSP sharing, at **constant latency and initiation interval of one across all datatypes**.
Evaluated on an AMD Xilinx U55c.

### 3. Pros and cons

**Pros**

- The problem statement is empirical rather than assumed — Figure 1's measured MAC-mix
across real quantized checkpoints is the kind of evidence this survey should prize.
- Decomposing to a shared mantissa product is the right unification: it makes format
diversity nearly free instead of multiplying the datapath, saving ~50% of adder LUT/FF
against instantiating separate MAC units.
- Concrete FPGA numbers: 1.4–2.0× compute density, 27–51% lower per-operation LUT/FF/DSP,
1.9× energy efficiency, 1.2× speedup, constant DSP cost across configurations; open-
sourced.

**Cons**

- FPGA-specific in its economics — the win is largely about DSP packing and LUT sharing, so
it does not translate directly into an ASIC area argument.
- Improves the MAC unit; end-to-end LLM speedup is a modest 1.2×, which bounds how much a
better MAC can buy at system level.
- Supports the datatypes that today's checkpoints use, so its longevity depends on that mix
staying recognizable.

### 4. Where it applies

The **FPGA** entry in the multi-bitwidth cluster, and the corpus's best evidence that
*runtime datatype switching* — not just multi-precision — is what deployed quantization
actually demands.

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

> The widespread adoption of mixed-precision quantization in large language models (LLMs)
> has created demand for hardware that can efficiently perform multiply–accumulate (MAC)
> operations across mixed datatypes and switch datatypes at runtime. Existing FPGA-based MAC
> solutions fall short due to limitations in fixed-datatype design, inefficient spatial or
> temporal resource sharing, and poor support for mixed-precision execution. These
> limitations collectively lead to under-utilization of DSP resources, limiting achievable
> parallelism and throughput. In this work, we present XtraMAC, a novel MAC architecture
> that unifies integer, floating-point, and mixed-precision operations within a single,
> datatype-adaptive microarchitecture. XtraMAC decomposes all supported MAC formats into a
> shared integer mantissa product with lightweight sign and exponent handling, enabling
> dynamic operand packing and efficient DSP resource sharing with constant latency and
> initiation interval of one across all datatypes. Evaluated on an AMD Xilinx U55c FPGA,
> XtraMAC achieves 1.4–2.0× higher compute density, reduces per-operation LUT, FF, and DSP
> consumption by 27–51%, and delivers up to 1.9× greater energy efficiency and 1.2× speedup
> on representative mixed-precision LLM workloads. The implemen- tation of XtraMAC is open-
> sourced at https://github.com/Xtra- Computing/XtraMAC.
