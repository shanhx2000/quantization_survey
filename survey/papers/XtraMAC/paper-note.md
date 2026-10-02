# XtraMAC: An Efficient MAC Architecture for Mixed-Precision LLM Inference on FPGA

**Venue / Year:** ISCA 2026 · **Link:** https://doi.org/10.1109/ISCA66397.2026.00177 · code https://github.com/Xtra-Computing/XtraMAC (includes the **Verilog implementations**) · **Reader:** Haoxuan · **Date:** 2026-09-14

## Tags

| | |
|---|---|
| **Level** | `ARCH` |
| **Q-oriented** | `Q-ORIENTED` |
| **Data type** | `INT8` `INT4` `FP16` `FP8` `FP4` `BF16` `MX` `MIXED` |
| **Generation** | `G3` |
| **Stage type** | `S1` |
| **Optimization** | mixed-precision MAC · DSP bit-space packing · unified mantissa product · datatype-specific accumulation · runtime datatype switching · constant II · FPGA |

## Stage-type tags

**`S1`** (the **Stage type** row in Tags) — most-matched first. A MAC-level design: every supported format, INT×FP included, is reduced to sign, exponent and one shared integer mantissa product inside the multiplier, with datatype-specific accumulation — the decision is made for one value in one PE.

*Tag form `S{stage}T{type}`, vocabulary from `survey/stage2.md` and `survey/stage3.md`. Added 2026-10-02 (ISCA Stage-type batch 2).*

## 1. One-line summary

Decomposes **all supported MAC formats into a shared integer mantissa product with lightweight sign
and exponent handling**, then applies a **DSP-centric design principle that exploits dynamic bit
mapping and multi-lane packing to maximize multiplier utilization**, with a **fixed four-stage
pipeline sustaining a constant latency and initiation interval of one across all supported
datatypes** — improving compute density **1.4–2.0×** and reducing LUT/FF/DSP usage by
**30.0%/47.9%/50.0%** against state-of-the-art FPGA baselines, and achieving **1.2× lower GEMV
latency and 1.9× higher energy efficiency against a GPU baseline**.

## 2. Data type

**Contributes none — executes existing formats.** INT4, INT8, FP4, FP8, BF16, MX, and mixed INT×FP.

**Unified multiplication.** `x · y = (s_x ⊕ s_y) · 2^(e_x + e_y − bias) · (m_x · m_y)`. The DSP "computes only the mantissa product `m_x m_y`, while sign and exponent are processed separately."

**Normalization.** The product mantissa is normalized by a leading-zero count: `m_norm = (m_x m_y) ≪ Δ`, `e = e_x + e_y − bias − Δ`.

**How integers join.** For mixed INT×FP the integer operand "is interpreted as a two's complement value and decomposed into sign and magnitude". "Since an integer carries no exponent encoding, we assign it a **logical unbiased exponent of zero**, which corresponds to a biased exponent value equal to the bias of the floating-point output format (e.g., 127 for FP32 and BF16, or 15 for FP16)."

**Multi-lane packing.** Per-datatype stride `S`, bounded by the DSP48E2 input widths `L_A = 27`, `L_B = 18`. "The polynomial structure of packed multiplication preserves strict lane isolation, while per-lane normalization and exponent reconstruction restore correct floating point."

**Datatype-specific accumulation, by design.** Integer addition "requires a wide bit width `w_int` (for example, 32 bits for INT4/INT8) but avoids expensive shifting by relying on efficient carry-chain logic"; floating-point addition "operates on narrower mantissas `w_fp` … but incurs substantial cost due to alignment and normalization shifters". A unified INT–FP adder "would force integer additions to traverse the same alignment and normalization shifters … making it significantly less resource-efficient than maintaining **separate adder paths**."

**Numerical conventions match GPU Tensor Cores.** FTZ and DAZ throughout; subnormal inputs treated as zero on ingestion, outputs below the minimum flushed to zero; NaN propagates as canonical qNaN. RN-even for FP; two's complement with saturation on overflow and truncation during accumulation for INT.

**Correctness.** "XtraMAC produces **bit-exact results matching NVIDIA A100/H100 Tensor Cores and the official AMD Floating-Point Operator across all supported datatypes**."

**Retraining.** N/A — model accuracy belongs to the quantization schemes XtraMAC executes.

## 3. Optimization

**The DSP is a bit-space, not a lane.** Existing FPGA MACs fail in one of two ways: **operand
upcasting**, "which promotes low-precision operands to match a fixed high-precision MAC unit,
resulting in significant waste of the DSP bit space" — dropping utilization to **8.9%** for
BF16-based MAC — or **spatial replication / temporal sharing**, which instantiates or serialises
datatype-specific datapaths. Both "use the DSP multiplier as an **opaque, single-lane primitive**,
rather than as a bit-space that can be systematically partitioned and shared across datatypes."

**The fix.** "By reducing all numerical formats to products and packing these lanes into the DSP
inputs at bit-precise offsets, XtraMAC enables a single DSP multiplier to be shared across integer,
floating-point, and mixed-precision MACs." A fixed four-stage pipeline holds **latency and
initiation interval constant at one** across every datatype.

**Multiplication unifies; accumulation deliberately does not** — integer addition wants width
without shifting, FP addition wants shifting without width, so separate adder paths are kept.

**The motivation is measured.** Table I surveys deployed checkpoints with their download counts:
Qwen-3-8B-AWQ runs **>68% of decode-stage MACs as INT4×BF16** while attention stays BF16×BF16, and
GPT-oss uses MXFP4 in MoE blocks with BF16 elsewhere — formats mix **within one forward pass**.

## 4. Results

| | |
|---|---|
| Baseline | **FPGA**: AMD Xilinx Floating-Point Operator, TATAA — identical Vivado/Vitis 2022.2 settings. **GPU**: NVIDIA **H100 PCIe** with CUTLASS official GEMV kernels |
| Models / datasets | Qwen-3-8B-AWQ, Llama-3.1-8B (W8A8 and FP8), Qwen-3-8B-FP8, GPT-oss-20B; mixed-precision GEMV kernels |
| Accuracy delta | **Numerical correctness verified: bit-exact against NVIDIA A100/H100 Tensor Cores and the AMD Floating-Point Operator across all supported datatypes.** Model accuracy belongs to the quantization schemes — Table I records 2–3% loss for Qwen-3-8B-AWQ edge reasoning, 99–100% for Llama-3.1-8B-W8A8, 99.52% recovery for another |
| Speedup | **1.4–2.0× compute density** vs FPGA baselines; **1.2× lower GEMV latency vs the GPU baseline**; constant latency and II = 1 across all datatypes; constant DSP cost across configurations |
| Energy / area | **−30.0% LUT, −47.9% FF, −50.0% DSP** per operation vs FPGA baselines; **1.9× higher energy efficiency vs the GPU baseline**; ~50% adder LUT/FF saved vs instantiating separate MAC units |
| Technology node | **AMD Xilinx Alveo U55c** — the corpus's first FPGA entry. DSP48E2, `L_A = 27`, `L_B = 18` |
| Evidence level | **Post-place-and-route implementation** (Vivado/Vitis 2022.2); FPGA power via **xbutil under steady-state streaming**, GPU power via **nvidia-smi**. End-to-end LLM latency from an **extended analytical simulation framework** |
| **Is the comparison fair?** | Each platform measured natively — post-PnR timing and xbutil on the U55c, CUTLASS and nvidia-smi on an H100 — and numerics are **bit-exact against A100/H100 Tensor Cores**, the right correctness claim for a MAC unit. Note the headline splits baselines: **density and resources vs FPGA, latency and energy vs GPU**. End-to-end LLM latency is **analytical**, not measured |

## 5. Comment

## 6. Claude notes

> **Suggestions from the reading agent. Strip this section before copying into
> `QuantArchSurvey/venues/ISCA/notes/`.**

- **Two corrections to my earlier draft, both material.** (1) I wrote "no accuracy content" — wrong.
  The paper states **bit-exact equivalence to NVIDIA A100/H100 Tensor Cores and the AMD
  Floating-Point Operator across all supported datatypes**, which is precisely the correctness claim
  a MAC unit owes; it also adopts FTZ/DAZ/qNaN semantics deliberately to match those Tensor Cores.
  (2) I attributed **1.2× latency and 1.9× energy** to the FPGA baselines — they are **against the
  GPU baseline** (H100 + CUTLASS). The FPGA baselines give the density and resource numbers.
- **Repo link corrected** to `https://github.com/Xtra-Computing/XtraMAC`, and the release **includes
  the Verilog implementations**, not just scripts — so the RTL is checkable.
- **§5 material, if you want it — the multi-precision thread is now six papers, and this one makes
  the organising claim visible.**

  | Paper | Composition | Cost of flexibility | Substrate |
  |---|---|---|---|
  | BitFusion'18 | spatial, 2-bit bricks | shift-add tree = 67% of the unit | ASIC 45 nm |
  | RaPiD'21 | split pipelines | ~16% area for the INT pipeline | ASIC 7 nm silicon |
  | SamsungNPU'21 / EVA'26 | temporal, 4 INT8 passes | zero extra multipliers | ASIC 5/28 nm |
  | **XtraMAC'26** | **spatial, in DSP bit-space** | **separate adders**; II = 1 | **FPGA** |
  | UniCore'26 | adder slices — no multiplier | O(1/n) | ASIC 28 nm |

  The deciding variable is never "spatial vs temporal" — it's **what the substrate charges for**.
  XtraMAC is the one whose multiplier is a **fixed, indivisible resource you must fill**, which is
  why it keeps the multiplier where UniCore removes it.
- **The best single finding: multiplication unifies across formats, accumulation does not.** This
  explains something visible corpus-wide but never explained in it — OLAccel carries 24-bit psums,
  DRQ 16-bit, BitFusion 32-bit, RaPiD emits 16-bit with hierarchical chunk accumulation, and
  **P3-LLM raises the accumulator problem and drops it**. I'd cite XtraMAC wherever the survey
  discusses accumulators.
- **Table I is the survey's best evidence that format mixing is real** — deployed checkpoints with
  download counts, and **>68% of Qwen-3-8B-AWQ's decode MACs are INT4×BF16** with attention at
  BF16×BF16. A measurement of what people actually run, not a design assumption.
- **Data type:** I'd add **`INT8`** and **`FP8`** to the seed's five — §III-C and §IV name INT8×INT8
  and FP8×FP8 as packed configurations, and Stage 4 packs "four FP8 lanes or two BF16 lanes".
- **First FPGA entry in the corpus.** Any aggregate efficiency table must keep it separate — LUT/FF/
  DSP counts aren't comparable with mm² at any node.
- Checked against your `SYS` rule: §VI's tile-based GEMV integration is a case study, not a compiler
  or ISA contribution, so `ARCH` alone.
