# XtraMAC — paper notes

**XtraMAC: An Efficient MAC Architecture for Mixed-Precision LLM Inference on FPGA**
Feng Yu, Hongshi Tan, Yao Chen, Weng-Fai Wong, Bingsheng He
**ISCA 2026** (2026 ACM/IEEE 53rd Annual International Symposium on Computer Architecture),
pp. 2536–2549 ｜ DOI: **10.1109/ISCA66397.2026.00177**
Publication info verified 2026-09-02 from the **official ISCA 2026 proceedings package**
(title, authors, pages, DOI and abstract all read from its `assets/data/data.js`).
Archived here: **the published proceedings PDF** (`506501c536.pdf`, 14 pages) — not a preprint.

Status: **note ready** ｜ Last updated: 2026-09-14
Tags: `multi-bitwidth-hw` `mixed-precision` `analytical-dtype` `accelerator`
How far it was read: **full close read of §I-§VIII.** §II (motivation and the DSP-utilisation
measurements), §III (the processing-pattern formulation — the unified multiplication decomposition,
the adder analysis, and DSP lane packing), §IV (architecture and pipeline) and §V-VI (evaluation
and the LLM case study) read line by line. Figures are bitmaps in the extraction, so numbers come
from prose. Read as the fifth entry in the multi-precision-datapath thread
(`BitFusion` → `RaPiD` → `SamsungNPU` → `EVA` → here).

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

**The unification is stated as algebra and it is genuinely general.** Every supported format reduces
to the same three pieces:

```
x · y = (s_x ⊕ s_y) · 2^(e_x + e_y − bias) · (m_x · m_y)
```

— a sign XOR, an exponent add, and **an integer mantissa product**. The move that makes it cover
mixed INT×FP is small and neat: an integer has no exponent field, so it is assigned a **logical
unbiased exponent of zero** (a biased exponent equal to the output format's bias — 127 for
BF16/FP32, 15 for FP16) and its magnitude is treated as the mantissa. After that, INT×INT, FP×FP
and INT×FP are the same operation. Normalisation is a leading-zero count applied per lane:
`m_norm = (m_x m_y) ≪ Δ`, `e = e_x + e_y − bias − Δ`.

**Its most valuable finding is negative, and no other entry in this corpus states it: multiplication
unifies across formats, accumulation does not.** §III-B works out why, and the reason is structural
rather than an implementation detail. Integer addition needs a **wide accumulator** (32 bits for
INT4/INT8) but **no shifting** — carry chains are cheap. Floating-point addition needs **narrow
mantissas** (10 bits FP16, 7 bits BF16) but pays for **alignment and normalisation shifters**, which
"dominate the LUT footprint of FPGA floating-point adders". A unified INT–FP adder would drag
integer additions through shifters that must be **sized for the wider integer width**, so XtraMAC
**keeps separate adder paths on purpose**. Every other multi-precision entry in this corpus argues
about the multiplier; this is the one that separates the two questions and shows they have opposite
answers.

**It reframes the DSP as a bit-space rather than a lane.** §II-C's diagnosis: existing FPGA designs
either **upcast** low-precision operands to the widest format (leaving most DSP bit capacity idle —
**8.9% effective utilisation for BF16-based MAC**) or **serialise** a wide operation over a narrow
core (e.g. decomposing a BF16 MAC into **four sequential INT8 operations** — which is exactly what
`SamsungNPU`, `EVA` and `RaPiD` do). Both "treat the DSP multiplier as an **opaque, single-lane
primitive**, rather than as a bit-space that can be systematically partitioned and shared across
datatypes." XtraMAC packs multiple lanes into the DSP48E2's `L_A = 27` and `L_B = 18` input widths
at bit-precise offsets, with the polynomial structure of the packed product preserving **lane
isolation**.

**So it lands on BitFusion's side of the spatial-versus-temporal argument, at a different
granularity.** `BitFusion` composes 2-bit BitBricks spatially in one cycle; `SamsungNPU` and `EVA`
decompose temporally into four INT8 passes; XtraMAC partitions a fixed DSP's **bit-space**
spatially and holds **latency and initiation interval constant at one across all datatypes**. The
thread now has both answers argued three times each, and the deciding variable each time is what
the substrate charges for — multipliers in an ASIC, muxes in a product, DSP bit capacity on an FPGA.

**Its motivation is empirical, which is rarer than it should be.** Figure 1 measures the MAC mix in
real quantized checkpoints: **Qwen3-8B-AWQ runs over 68% of decode-stage MACs as INT4×BF16** while
attention stays BF16×BF16, and GPT-oss uses MXFP4 in MoE blocks with BF16 elsewhere. The premise —
that formats mix **within one forward pass** — is measured, not assumed.

---

## Method

**Unified multiplication** (§III-A) **verified**. As above. The three pieces are: sign XOR, exponent
addition, and an integer mantissa product computed on the DSP. Integers enter with a logical
unbiased exponent of zero and sign-extracted magnitude.

**Separate accumulation** (§III-B) **verified** — a deliberate non-unification:

| | Integer add | Floating-point add |
|---|---|---|
| Width | **wide** (`w_int` = 32 for INT4/INT8) | **narrow** mantissa (`w_fp` = 10 FP16, 7 BF16) |
| Shifters | **none** — carry chain | **alignment + normalisation**, which dominate LUT cost |

A unified adder sizes the shifters for `w_int`, wasting area on operations that need no shifting.
So the adder paths stay separate.

**DSP lane packing** (§III-C) **verified**. A DSP slice computes one wide integer multiplication
over input bit vectors `A_DSP`, `B_DSP`. XtraMAC assigns each datatype a **per-lane stride `S`** and
packs lanes at bit-precise offsets, so `Parallelism ≤ min(L_A/S, L_B/S)` with **`L_A = 27`,
`L_B = 18`** for the DSP48E2. Different datatypes get different strides and therefore different
parallelism from the same slice. Lane isolation is preserved by the polynomial structure of the
packed product.

**Pipeline** (§IV). Four logical stages, each a bounded combinational block followed by a register
boundary. **Stage 4** concatenates the `P` lane results into a packed output word (four FP8 lanes or
two BF16 lanes forming 32 bits) with **no additional normalisation or conversion**, emitting one
multi-lane MAC result per cycle. **Constant latency and II = 1 across every datatype.**

**Numeric conventions** (§V-A) **verified**: FP uses **round-to-nearest-even** with **subnormals
flushed to zero**; INT uses **two's complement with saturation on overflow** and **truncation during
accumulation**.

**Open source**: `https://github.com/Xtra-Computing/XtraMAC` — the release **includes the Verilog implementations**, so the RTL is checkable **verified**.

---

## Key numbers, with their frame

Evidence level: **actual FPGA implementation** — Vivado/Vitis 2022.2 on an **AMD Xilinx Alveo
U55c**, identical tool settings across all designs. Resource and density numbers are measured from
place-and-route. **The end-to-end LLM latency figures are analytical** — §VI "extend[s] an
analytical simulation framework to estimate end-to-end LLM inference latency". Do not pool the two.

| Setting | Metric | Baseline | Result | Source |
|---|---|---|---|---|
| **The diagnosis** | DSP effective utilisation, BF16-based MAC under upcasting | — | **8.9%** | §II **verified** |
| Compute density | ops per resource | AMD Xilinx **Floating-Point Operator**, **TATAA** | **1.4-2.0×** | §V **measured** |
| Resource per operation | LUT / FF / DSP | same | **−30.0% / −47.9% / −50.0%** (abstract rounds to "27-51%") | §I, §V **measured** |
| Latency | GEMV | **GPU baseline — NVIDIA H100 PCIe + CUTLASS** | **1.2× lower** | §I, §V **measured** |
| Energy efficiency | — | **GPU baseline (H100)**, power via nvidia-smi vs xbutil on the U55c | **1.9×** | §I, §V **measured** |
| Throughput behaviour | latency and initiation interval | — | **constant, II = 1, across all datatypes** | §IV-F **verified** |
| DSP cost | across datatype configurations | — | **constant** | §I **verified** |
| Adder sharing saving | adder LUT/FF vs instantiating separate MAC units | separate MACs | **~50%** | §I **verified** |
| **Motivating measurement** | share of decode-stage MACs that are INT4×BF16 | — | **>68% on Qwen3-8B-AWQ**, with attention at BF16×BF16 | Fig. 1 **verified** |
| " | format mix | — | **GPT-oss: MXFP4 in MoE blocks, BF16 elsewhere** | Fig. 1 **verified** |
| DSP geometry | input widths | DSP48E2 | **L_A = 27, L_B = 18** | §III-C **verified** |
| **Numerical correctness** | — | bit-exactness | NVIDIA **A100/H100 Tensor Cores** and the AMD Floating-Point Operator | **bit-exact across all supported datatypes** | §III **verified** |
| Accuracy context | deployed checkpoints | model accuracy | — | **2-3% loss** (Qwen-3-8B-AWQ edge reasoning), **99-100%** (Llama-3.1-8B-W8A8), **99.52% recovery** — properties of the quantization schemes, not of XtraMAC | Table I **verified** |

**XtraMAC contributes no *model* accuracy of its own** — it executes formats other people chose, and
Table I's figures belong to those schemes. But it **does** make and verify the correctness claim a
MAC unit owes: **bit-exact results matching NVIDIA A100/H100 Tensor Cores and the AMD Floating-Point
Operator across all supported datatypes**, with FTZ/DAZ/qNaN semantics adopted deliberately to match
those Tensor Cores. An earlier draft of this entry said "no accuracy content"; that was wrong.

---

## Cost and requirements

| | |
|---|---|
| **Separate adders** | The unification deliberately stops at the multiplier. INT and FP accumulate on **different paths** — a real area cost, argued to be cheaper than the alternative |
| **Per-datatype strides** | Each format needs its own lane stride and packing offsets; parallelism varies by datatype from the same DSP |
| **Normalisation per lane** | Leading-zero count and exponent reconstruction **per lane**, not per operation |
| **Control** | Runtime datatype switching is fine-grained — the paper's point is that it should be an allocation problem inside the DSP bit-space, not a datapath-level mode switch |
| **Substrate** | **FPGA-specific economics.** The win is DSP bit-packing and LUT sharing; on an ASIC where multiplier width is a free design variable, the argument changes |
| **Data type** | **Contributes none.** Executes INT4, INT8, BF16, FP8, FP4 and MX formats that others define |
| **Retraining** | N/A |

---

## Limitations and open questions

**Admitted.** FPGA-specific; the adder is deliberately not unified, with the reasoning given; the
end-to-end LLM numbers come from an analytical framework rather than measurement.

**Unadmitted, and material.** (i) **Two evidence levels sit together** — MAC-level resource and
density figures are place-and-route measurements, the end-to-end LLM latency is analytical, and
the abstract presents them in one sentence. (ii) **The 8.9% DSP utilisation figure characterises
the upcasting baseline**, not a fundamental limit — a temporal design would score differently, and
the paper does not report the equivalent figure for the serialising strategy it also criticises.
(iii) **No *model* accuracy content** — correct for a MAC paper, and it does verify bit-exactness
against A100/H100 Tensor Cores — but it means the entry cannot be cited for any quantization
accuracy result. (iv) **The parallelism bound is stated for DSP48E2 specifically** (`L_A = 27`,
`L_B = 18`); how the formulation transfers to other DSP geometries or to Versal AI Engines is not
examined.

---

## Relation to other entries

**It is the fifth entry in the multi-precision-datapath thread, and the thread is now the corpus's
most developed cross-paper structure.**

| Paper | Composition | Granularity of sharing | Cost of flexibility | Substrate |
|---|---|---|---|---|
| `BitFusion` (ISCA'18) | **spatial** | 2-bit BitBricks | shift-add tree = 67% of the unit | ASIC, 45 nm |
| `RaPiD` (ISCA'21) | **split pipelines** | whole FPU vs FXU | ~16% area for the INT pipeline | ASIC, 7 nm silicon |
| `SamsungNPU` (ISCA'21) | **temporal** | byte (4 INT8 passes) | **zero extra multipliers** — muxes only | ASIC, 5 nm silicon |
| `EVA` (ISCA'26) | **temporal** | 4 INT8 → FP16 | reuses an INT8 array | ASIC, 28 nm |
| **`XtraMAC` (ISCA'26)** | **spatial, in DSP bit-space** | bit-precise lane offsets | **separate adders**; II = 1 | **FPGA** |

The deciding variable each time is what the substrate charges for: multipliers in an ASIC, muxes in
a shipping product, DSP bit capacity on an FPGA. That is a cleaner organising claim than "spatial
beats temporal", and XtraMAC is what makes it visible — it is the only entry whose substrate makes
the multiplier a **fixed, indivisible resource you must fill**.

**Its multiplication-unifies-but-accumulation-does-not result is the corpus's only clean statement
of that split**, and it bears on entries that never raise it. `OLAccel` carries 24-bit psums,
`DRQ` 16-bit, `BitFusion` 32-bit, `RaPiD` emits 16-bit from the array with chunk-based
hierarchical accumulation in the SFUs, `P3-LLM` raises the accumulator problem in §V-A and drops
it. XtraMAC explains why accumulator design keeps resisting the unification that multipliers accept:
**integer addition wants width without shifting, FP addition wants shifting without width.**

**With `UniCore` it forms an FPGA/ASIC pair on the same question** — UniCore's claim is that
composable FP MACs can be built to fuse **linearly rather than quadratically**, which is the
scaling law BitFusion's shift-add tree pays. Read them together.

**Empirically it supplies something the survey needs: evidence that format mixing is real.** The
Qwen3-8B-AWQ measurement (**>68% of decode MACs as INT4×BF16** with attention at BF16×BF16) is the
best justification in the corpus for why mixed-precision hardware matters at all, and it is a
measurement of shipping checkpoints rather than a design assumption.

**Node/substrate.** The corpus's **first FPGA entry**. Any aggregate efficiency table must keep it
separate — LUT/FF/DSP counts are not comparable with mm² at any process node.

---

## For the note

**§1 one-line summary.** Shows that **every** MAC format — INT×INT, FP×FP and mixed INT×FP — reduces
to the same sign XOR, exponent add and **integer mantissa product** (integers entering with a
logical unbiased exponent of zero), then exploits that by treating an FPGA DSP slice as a
**bit-space to be partitioned rather than a single lane**, packing per-datatype lanes at bit-precise
offsets into the DSP48E2's 27- and 18-bit inputs with polynomial lane isolation — while deliberately
**keeping INT and FP accumulation on separate paths**, because integer addition wants width without
shifting and FP addition wants shifting without width — for **1.4-2.0× compute density, 30/48/50%
less LUT/FF/DSP, and constant latency with II = 1 across all datatypes** on an Alveo U55c.

**Proposed tags — the seed row stands.**

| Axis | Value | Evidence |
|---|---|---|
| **Level** | `ARCH` | A MAC microarchitecture and its pipeline. **Checked against the `SYS` rule**: the tile-based GEMV integration in §VI is a case study, not a compiler or ISA contribution, so no `SYS`. Seed agrees |
| **Q-oriented** | `Q-ORIENTED` | The whole design exists to execute **several numeric formats in one datapath**. Fix a single format and the lane-stride machinery, per-lane normalisation, exponent reconstruction and datatype-switch control have nothing to do |
| **Data type** | `INT4` `BF16` `MX` `FP4` `MIXED` + **`INT8`** `FP8` | Seed has five. §III-C and §IV name **INT8×INT8** and **FP8×FP8** explicitly as packed configurations, and Stage 4 packs "four FP8 lanes or two BF16 lanes" |
| **Generation** | `G3` | Seed agrees. Mixed formats *within one forward pass* driven by real LLM checkpoints (AWQ, MXFP4 MoE) is a G3-era premise, even though the mechanism is `G2`-family datapath composition |
| **Optimization** | `mixed-precision MAC` `DSP bit-space packing` `unified mantissa product` `separate INT/FP accumulation` `runtime datatype switching` `constant II` `FPGA` | |

**§4 fairness verdict.** Each platform is measured natively — post-place-and-route timing and
**xbutil** on the Alveo U55c, **CUTLASS** kernels and **nvidia-smi** on an H100 — with rounding and
overflow conventions stated, and numerics verified **bit-exact against A100/H100 Tensor Cores and the
AMD Floating-Point Operator**, which is the correctness claim a MAC unit owes. Note the headline
**splits its baselines**: density and LUT/FF/DSP are against **FPGA** baselines, while the 1.2×
latency and 1.9× energy efficiency are against the **GPU** baseline. End-to-end LLM latency is
**analytical**, not measured. The **8.9%** DSP utilisation characterises the *upcasting* baseline
only, with no equivalent figure for the serialising strategy also criticised.

**Proposed venue-list row:**

```
| [ ] | [XtraMAC: An Efficient MAC Architecture for Mixed-Precision LLM Inference on FPGA](https://doi.org/10.1109/ISCA66397.2026.00177) | *close read* | ARCH | Q | `INT8` `INT4` `FP8` `FP4` `BF16` `MX` `MIXED` | G3 | `mixed-precision MAC` `DSP bit-space packing` `unified mantissa product` `separate INT/FP accumulation` `runtime datatype switching` `constant II` `FPGA` | Every format decomposed into one shared integer mantissa product — **but accumulation deliberately stays split, because integer addition wants width without shifting and FP addition wants shifting without width**. Treats the DSP as a bit-space, not a lane |
```

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
