# LUTTensorCore — paper notes

**LUT Tensor Core: A Software-Hardware Co-Design for LUT-Based Low-Bit LLM Inference**
Zhiwen Mo, Lei Wang, Jianyu Wei, Zhichen Zeng, Shijie Cao, Lingxiao Ma, Naifeng Jing, Ting
Cao, Jilong Xue, Fan Yang, Mao Yang
**ISCA 2025** ｜ DOI: **not recorded** — the ACM/IEEE record is not reachable by script (403); look it up when citing
Venue evidence (2026-09-02): arXiv `comments` field, verbatim: *"Conference Version (ISCA'25). Fixed a typo"*
Archived here: **arXiv:2408.06003v3** (2025-07-28), 14 pages — **the preprint, not the
published ISCA 2025 version**; the two were **not compared**.

Status: **note ready** ｜ Last updated: 2026-09-03
Tags: `lut-accelerator` `non-analytical-dtype` `multi-bitwidth-hw` `mixed-precision`
`analytical-dtype` `gpu-kernels` `accelerator`
(**Proposed additions**: `non-analytical-dtype` — compute is resolved by table, not by
decoding a formula; `gpu-kernels` — this is a Tensor Core replacement inside a GPU with an
LMMA instruction-set extension and a TVM/Welder/Roller compiler stack, not a standalone ASIC.
`survey/TAGS.md` not edited.)
How far it was read: **close read of §1–§5** — abstract, introduction, §2 (mpGEMM background,
LUT-based mpGEMM, gaps), §3 (all of software table optimization, hardware microarchitecture,
instructions and compilation), §4.1–§4.6 (all of evaluation, incl. Tables 1–5) and §5
Discussion and Limitations. **Skimmed:** §6 related work and references. Figures 12–18 were
read for their prose claims; **per-bar values were not transcribed** — see "left blank" below.
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> Original: https://arxiv.org/abs/2408.06003
> The PDF is **not committed** (1.8 MB). Re-download: `curl -sSL -o 2408.06003.pdf https://arxiv.org/pdf/2408.06003`
> Extract text: `python3 extract.py` → `extracted/` (committed, greppable)
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, ISCA 2025 row.

---

## Brief

### 1. Motivation

Low-bit weight quantization turns the core LLM operation into **mixed-precision GEMM
(mpGEMM)** — low-bit weights times higher-precision activations — which off-the-shelf
hardware does not support natively. Everyone therefore dequantizes first, and that becomes
the bottleneck at large batch sizes. LUT-based mpGEMM is the obvious alternative, but the
paper finds a **naive LUT implementation does not deliver the promised gains**.

### 2. Overview

A full software–hardware co-design: software-side optimizations to cut table-precompute
overhead and reinterpret weights to shrink table storage; a LUT-based Tensor Core with an
**elongated tiling shape** to maximize table reuse and a **bit-serial** design to cover
diverse precision combinations; plus a new instruction set and compiler support.

### 3. Pros and cons

**Pros**

- Starts by showing why the obvious version fails, then fixes each cause — a much stronger
structure than proposing LUTs as self-evidently good.
- The bit-serial datapath makes one design cover many W/A precision pairs (WINT1–4 against
FP16/FP8), which is what mpGEMM diversity actually demands.
- 1.44× compute density and energy efficiency over the previous best LUT-based accelerator,
plus a large margin over software LUT implementations.

**Cons**

- Table precompute and storage are reduced, not eliminated; the design's advantage still
depends on reuse, so it is tiling- and shape-sensitive.
- Being a Tensor Core replacement, the benefit assumes you can change the GPU's core — the
highest-barrier form of adoption in this corpus.
- [`OASIS`](../OASIS/ANALYSIS.md) and [`Omni-LUT`](../Omni-LUT/ANALYSIS.md) both identify
remaining limits (LUT size, parallelism, and no support for activation–activation GEMM),
so this is a waypoint rather than an endpoint.

### 4. Where it applies

The central **§1.3 / LUT-accelerator** reference for LLM inference, and the baseline the
2026 LUT papers measure against. Its mpGEMM framing is the cleanest statement in the corpus
of why weight-only quantization creates a hardware problem.

---

## Conclusions

**Read in full 2026-09-03.** The brief survives, with three corrections and one addition.

**Corrected.** (a) The brief calls the 1.44× "over the previous best LUT-based accelerator" —
true, but that baseline is **UNPU (ISSCC'18), re-implemented by these authors because no code
is public**, and the comparison is a single `W_INT2 A_INT8` Tensor Core configuration
(**verified**, Table 2, p11). It is an ablation, not a broad win. (b) The brief's headline
framing understates the paper: the **4×–6× PPA gain over a MAC Tensor Core** is the larger
result, and the 1.44× is only the increment over prior LUT hardware. (c) "Tiling- and
shape-sensitive" is right but backwards in emphasis — the tiling shape is a *designed*
contribution (`M2 N64 K4`), not a fragility.

**Added — the thing the brief missed entirely.** §3.1.3 introduces **table quantization**:
the precomputed table entries are themselves quantized to INT8, per table of 8 entries over a
group of 4 activations (**verified**, p05, p11). This is a genuinely new quantization axis for
the survey — **quantizing the precomputed products rather than the operands** — and it is
what lets one datapath absorb FP16/FP8/INT16/INT8 activations. It belongs in the taxonomy
discussion, not in a footnote.

---

## Method

**Verified** unless marked. Pages are `extracted/2408.06003.pages/pNN.txt`.

**The problem.** Weight-only quantization makes the core op **mpGEMM** — low-bit weights ×
high-precision activations — which GPUs and TPUs do not support natively, so everyone
dequantizes first and forfeits the low-precision gain (§2.2, p03). LUT-based mpGEMM removes
both the dequantization and the multiplication: precompute the dot products of an activation
tile against every possible weight pattern, then look up. The paper's premise is that **the
naive version of this loses to dequantization anyway** — LUT-GEMM software is beaten by
CUTLASS on an A100 and degrades by orders of magnitude at large batch (Fig. 4, p03), and
conventional LUT *hardware* has no area advantage over MAC beyond 2-bit weights (Fig. 13,
p08). Four named gaps: table precompute/storage, bit-width flexibility, tiling shape,
instruction and compilation (§2.3, p03–p04).

**Four fixes, three of them in software.**

1. **DFG transformation + operator fusion** (§3.1.1, p04–p05). Conventional designs put a
   precompute unit next to every LUT unit, recomputing the same table — for a
   `[4096,12288]×[12288,12288]` OPT-175B GEMM with array `N=4`, **3072 times over**.
   LUT Tensor Core splits precompute into an independent operator computed once and
   broadcast, then fuses it with the preceding element-wise operator to hide the memory
   traffic. Overhead falls from 16.47 %/24.41 % to **2.62 %/2.52 %** (Table 4, p11).
2. **Weight reinterpretation for table symmetry** (§3.1.2, p05). Remap the stored bits
   `{0,1} → {−1,1}` by `q' = 2q − (2^K − 1)`, `s' = s/2`, `z' = 2z + 1 − 2^K` — mathematically
   identical, but now `LUT[W] = −LUT[~W]`, so **half the table is redundant**: `2^K → 2^(K−1)`
   entries. The remap is done **offline on static weights**, which also deletes the per-unit
   negation circuit. This halves table storage, MUX width *and* the broadcast to N PEs.
3. **Table quantization** (§3.1.3, p05). Quantize the *table entries* to INT8 — one scale per
   table of 8 entries over a group of **4 activation elements**. Finer-grained and more
   dynamic than quantizing activations directly, and it is what makes one datapath cover
   FP16/FP8/INT16/INT8 activations.
4. **Hardware** (§3.2, p06–p07). A **bit-serial** LUT unit maps a `W_BIT` weight to `W_BIT`
   cycles over the same 1-bit table, so INT1–INT4 share one datapath. Tiling is **elongated**:
   table size is `M × 2^(K−1) × LUT_BIT`, so `K` must stay small while `N` sets how many MUXes
   reuse each entry — DSE picks **K = 4** (§4.2.1, p07) and **`M2 N64 K4`** (§4.2.2, p08),
   against the A100 INT8 Tensor Core's `M8 N4 K16` at the same 512-element array size.
5. **Integration** (§3.3, p06). An **LMMA** instruction
   (`lmma.{M}{N}{K}.{A}{W}{Accum}{O}`) extending MMA, plus a compiler stack on TVM, Welder
   and Roller.

## Key numbers, with their frame

**Frames differ per row and must not be pooled.** PPA is **post-synthesis** (Verilog +
Synopsys DC, **TSMC 28 nm**, medium effort, 1 GHz target, §4.1.1 p07). Kernel numbers are
**Accel-Sim**, a cycle-level GPU simulator (§4.1.2, p07). End-to-end numbers are a
**custom analytical tile-based simulator** the authors wrote because Accel-Sim would take
579 days and emit 79 TB of trace (§4.4, p09) — validated to **5.21 % MAPE on a single layer**
(§4.4.1, p09). **No silicon.**

| Setting | Model / shape | Metric | Baseline | Result | Source |
|---|---|---|---|---|---|
| DP4 unit, `W_INT1 A_FP16`, no psum | — | Compute density | MAC `W_FP16 A_FP16` = 3.39 TFLOPs/mm² | **61.55 TFLOPs/mm²** | Fig. 12, p08 · post-synthesis 28 nm |
| Tensor Core, 1-bit weights | — | Power **and** area | MAC-based Tensor Core | **4×–6× reduction** | Fig. 14, p08 · post-synthesis |
| Tensor Core DSE, 12 configs (A ∈ FP16/INT16/FP8/INT8 × W ∈ INT1/2/4) | — | Area × power | MAC- and ADD-based | LUT smallest in **11 of 12**; loses only at `W_INT8 A_INT4` | Fig. 14, p08 · post-synthesis |
| mpGEMM kernel, `W_INT1 A_FP16` | LLAMA2-13B, M=2048 N=27648 K=5120 | Perf per area | A100 MAC Tensor Core | slightly higher perf at **14.3 % of the area** | §4.3, p09 · Accel-Sim |
| vs SOTA LUT **software** | LLAMA2-70B shapes | Speedup | LUT-GEMM | **1.42× GEMV, 72.2× GEMM** | Fig. 18, p10 · Accel-Sim |
| vs SOTA LUT **hardware**, `W_INT2 A_INT8`, M×N×K=512 | — | Compute intensity / power eff. | **UNPU, re-implemented by the authors** (no public code) | **1.44× / 1.442×** (ablation: reinterpretation 1.317×, +negation elim. 1.351×, +DFG/fusion 1.440×) | Table 2, p11 · post-synthesis |
| End-to-end, up to 8× array | OPT-175B, BLOOM-176B, LLAMA2-70B | Speedup | `W_FP16 A_FP16` Tensor Core | **up to 8.2×**, at **38.3 %** of its area | §4.4.2, p09 · analytical simulator |
| End-to-end headline (Table 1) | **A100 FP16 TC running LLAMA-3B** vs **A100-LUT-8X running BitNet b1.58 3B** `W_INT2 A_INT8` | Latency | 106.71 ms (BS1 SEQ2048) / 41.15 ms (BS1024 SEQ1) | 38.02 ms / **7.47 ms → 5.51×** | Table 1, p10 · analytical simulator |
| same | same | Compute density / energy eff. / area | 2.96 TFLOPs/mm² · 2.98 TFLOPs/W · 0.975 mm²/SM | 61.95 TOPs/mm² (**20.9×**) · 33.65 TOPs/W (**11.2×**) · 0.373 mm² (**38.3 %**) | Table 1, p10 |
| same, vs H100 | BitNet b1.58 3B | Area efficiency | H100 FP8 TC, 12.59 TFLOPs/mm² | 25.40 TFLOPs/mm² (**2.02×**) | Table 1, p10 |
| Precompute overhead | OPT-175B / BLOOM-176B / LLAMA2-70B, 1 layer | % of runtime | separate precompute: 16.47 % / 24.41 % | fused: **2.62 % / 2.52 %** | Table 4, p11 · analytical |
| Table quantization cost | LLAMA2-7B `W_INT2` (BitDistiller **QAT**) | WikiText2 PPL | `A_FP16` = 7.68 | `A_LUT_INT8` = **7.69** (FP16 model = 5.47) | Table 5, p11 |
| Accuracy of the low-bit models themselves | LLAMA2-7B | Zero-shot avg | FP16 = 62.7 % | `W_INT2` = 56.4 %, +table quant = 56.5 % | Table 5, p11 |

Left blank: per-bar values of Figs. 12–18 (the extracted layout does not bind bars to
series), and the PPA of individual `W×A` pairs beyond the two the prose names.

## Cost and requirements

- **Data type.** `W_INT1` / `INT2` / `INT4` (up to INT4; the DP4 study shows the design still
  wins to **6-bit** weights) × `A_FP16` / `A_FP8` / `A_INT16` / `A_INT8`. Weight-only —
  activations stay ≥8-bit throughout, which the paper justifies by activation outliers
  (§2.1, p02–p03).
- **The value is an index, not a number.** A weight bit-pattern selects a precomputed dot
  product. That is what puts this in taxonomy §1.3 rather than §1.2 — nothing decodes a
  weight into a magnitude.
- **Granularity.** The activation vector length is **K = 4**; a table covers those 4
  activations and is quantized as a unit (8 entries after symmetrization). Weight scale
  granularity is **inherited from whatever quantizer produced the weights** and is not
  specified by the paper — see "left blank" below.
- **Outliers.** Not handled, by construction: outliers are the stated *reason* activations
  are not pushed below 8 bits (§2.1, p03).
- **Escape hatches.** Activations never go below 8 bits. Accumulation and partial sums stay
  wide (Fig. 12 is explicitly measured "No Psum", so the reported density **excludes**
  accumulator cost). **Attention and the KV cache are out of scope entirely** — §5 lists
  long-context attention and KV-cache quantization as future work (p11–p12). Training is out
  of scope: the backward pass "still demand[s] more high precision computation" (§5, p11).
- **Retraining — read carefully.** LUT Tensor Core is *itself* quantization-agnostic, but
  **every low-bit model it is evaluated on comes from QAT or from scratch**: BitNet b1.58
  (trained from scratch) and BitDistiller (a QAT framework) supply the INT2 weights (§4.6.2,
  p11). §2.1 concedes PTQ is near-lossless only at 4-bit and that 2-bit needs QAT (p02–p03).
  So the headline configurations are **not reachable from a stock checkpoint**.
- **Adoption barrier — the highest in this corpus.** It replaces the GPU Tensor Core, adds an
  instruction (LMMA), and needs a modified compiler stack. Code released at
  `github.com/microsoft/T-MAC/tree/LUTTensorCore_ISCA25`; **not checked against the paper**,
  so this stays `analysis ready` and not `thorough ready`.

## Limitations and open questions

**Authors admit** (§5, p11–p12): inference only, no training; no long-context attention or
KV-cache support; only `W_INT A_FP` and `W_INT A_INT` — `W_FP` is a sketch (mantissa+sign as
index, exponent to a shifter); and Blackwell's native mpGEMM support may erode the premise.

**Not admitted:**

1. **Table 1's baselines are analytically scaled, not measured.** The footnote reads: *"Due
   to the lack of public data on A100/H100 Tensor Cores and their 7/4 nm processes, † indicates
   that the data are normalized to 28 nm at 1.41 GHz and optimized to the best of our ability"*
   (p10). So **5.51×, 20.9×, 11.2× and 2.02× compare a synthesized 28 nm design against an
   analytical model of a 7 nm and a 4 nm chip.** This is precisely the failure mode
   [`PAPER-READING`](../../../Claude/instructions/PAPER-READING.md) §4 warns about. The
   post-synthesis 4×–6× against their own MAC baseline is the defensible number; Table 1 is
   not.
2. **Table 1 also changes the model between rows.** The A100 FP16 row runs **LLAMA-3B**
   (49.7 % avg acc); every LUT row runs **BitNet b1.58 3B** (49.4 %). The latency ratio is
   therefore across two different models that merely have similar accuracy — defensible as an
   iso-accuracy argument, indefensible as an iso-workload one, and the paper does not
   distinguish them.
3. **The end-to-end simulator is the authors' own analytical model**, validated on *one
   layer* at 5.21 % MAPE (§4.4.1, p09) and then used for whole-model claims up to 8.2×. The
   validation was against `W_FP16 A_FP16` and `W_INT8 A_INT8` — **not** against any LUT
   configuration, which is the thing being predicted.
4. **The 1.44× over UNPU is one configuration against a re-implementation.** UNPU is ISSCC'18
   silicon at 65 nm; here it is re-synthesized at 28 nm by its competitor, with DSE applied by
   its competitor, at `W_INT2 A_INT8` only (Table 2, p11).
5. **"4×–6×" is the 1-bit-weight corner.** Fig. 13 shows conventional LUT loses to MAC beyond
   2-bit weights, and LUT Tensor Core's own advantage runs out at **6-bit** (p08). At INT4 —
   the bit-width most PTQ work actually ships — the margin is much smaller than the headline.
6. **Weight scale granularity is never stated.** For a survey whose §2 asks for group size,
   this is a real hole: the design takes low-bit weights as given and never says at what
   granularity they were scaled.

## Relation to other entries

- **The §1.3 LUT anchor, and the one the 2026 papers measure against.**
  [`OASIS`](../OASIS/ANALYSIS.md) and [`Omni-LUT`](../Omni-LUT/ANALYSIS.md) both position
  against it; [`EVA`](../EVA/ANALYSIS.md) takes the codebook route instead.
- **Eager vs lazy table construction** — the distinction that came out of the
  [`TransitiveArray`](../TransitiveArray/ANALYSIS.md) read. LUT Tensor Core is the **eager**
  pole: it precomputes all `2^(K−1)` entries for every activation tile, and its whole software
  contribution is making that precompute cheap (fusion, symmetry, table quantization).
  TransitiveArray is the **lazy** pole: it materialises only the entries that occur, one add
  each. The two papers never cite each other and solve the same problem from opposite ends —
  **this is the strongest pairing in the corpus for survey §5.6.**
- **Weight-only + mpGEMM framing**: the cleanest statement in the corpus of *why* weight-only
  quantization creates a hardware problem. Cite it for that even where the design is not the
  point. Contrast [`Tender`](../Tender/ANALYSIS.md) and [`Oaken`](../Oaken/ANALYSIS.md),
  which quantize both sides.
- **Bit-serial lineage**: shares the `W_BIT`-cycles trick with
  [`BitFusion`](../BitFusion/ANALYSIS.md) and the bit-slice line, but uses it to *reuse one
  table* rather than to compose multipliers.
- **Non-corpus baselines that carry the paper**: UNPU (ISSCC'18), ANT (MICRO'22), Mokey
  (ISCA'22 — in corpus), FIGNA, LUT-GEMM, T-MAC, BitNet, BitDistiller. Same pattern as
  TransitiveArray: **the comparison set is mostly outside ISCA.**

## For the note

### §1 one-line summary

> Makes LUT-based mpGEMM actually pay by moving the table's cost into software — fusing
> precompute into the previous operator, halving the table by reinterpreting weight bits
> `{0,1}→{−1,1}` for symmetry, and quantizing the table entries themselves to INT8 — leaving
> a bit-serial LUT Tensor Core with an elongated `M2 N64 K4` tile that runs `W_INT1–4` against
> FP16/FP8/INT8 activations at **4×–6× the power and area efficiency** of a MAC Tensor Core.

### Proposed values on their four axes

| Axis | Proposed | Evidence (one line) |
|---|---|---|
| **Level** | **`ALGO+SYS+ARCH`** (if only two are allowed, `SYS+ARCH`) | Genuinely all three: table quantization is an algorithm (§3.1.3), the DFG transform + fusion + TVM/Welder/Roller stack is systems (§3.1.1, §3.3), the bit-serial LUT Tensor Core is architecture (§3.2). The paper's own title says "software-hardware co-design". |
| **Q-oriented** | `Q-ORIENTED` | Swap the format for plain INT8 and the entire design disappears — there is no table, no mpGEMM problem, and no reason for the elongated tile. |
| **Data type** | **`LUT` + `INT1` `INT2` `INT4` + `FP16` `FP8` `INT8` + `MIXED`** | Weights INT1–4 become table indices; activations FP16/FP8/INT16/INT8; the table itself is quantized to INT8 (§3.1.3, p05). |
| **Generation** | **`G3`** | Weight-only thread (activations stay wide *because of outliers*, §2.1) and codebook thread (compute becomes lookup) together — the same two threads as TransitiveArray, but here the paper says so itself. |
| **Optimization** (free text) | `LUT-GEMM` `mpGEMM` `weight-only` `bit-serial` `table-quantization` `weight-reinterpretation` `operator-fusion` `elongated-tiling` `LMMA` `GPU-tensor-core` | — |

### Proposed venue-list row

Replaces the LUT Tensor Core row under **2025**. For the human to apply.

```
| [x] | [LUT Tensor Core: A Software-Hardware Co-Design for LUT-Based Low-Bit LLM Inference](https://arxiv.org/abs/2408.06003) | ALGO+SYS+ARCH | Q | `LUT` `INT1` `INT2` `INT4` `FP16` `FP8` `MIXED` | G3 | `LUTGEMM` `mpGEMM` `bit-serial` `table-quantization` `weight-only` | Eager LUT-mpGEMM: precompute fused into the prior operator, table halved by {0,1}→{−1,1} symmetry, entries quantized to INT8; elongated M2N64K4 Tensor Core, 4–6× PPA over MAC |
```

### §4 fairness verdict

**Two comparisons, and only one of them is fair.**

- **The post-synthesis comparison is fair and is the number to cite.** MAC-, ADD- and
  LUT-based designs all written in Verilog by the same authors, synthesized in the same
  **TSMC 28 nm** flow at the same 1 GHz target with the same DC effort level, swept over the
  same `M×N×K = 512` array size and 12 precision pairs (§4.1.1 p07, §4.2.2 p08). Iso-node,
  iso-area-budget, iso-effort. **4×–6× at 1-bit weights** stands.
- **Table 1 is not a fair comparison and should not be quoted.** The A100 and H100 Tensor
  Core baselines are **analytically normalized from 7 nm and 4 nm down to 28 nm at 1.41 GHz**
  by the authors (footnote, p10), *and* the rows run different models (LLAMA-3B vs BitNet
  b1.58 3B). So 5.51× / 20.9× / 11.2× / 2.02× are model-vs-model across a scaled baseline —
  neither iso-node in any measured sense nor iso-workload.
- **Iso-accuracy: argued, not held.** The LUT rows are only comparable to the FP16 row
  because BitNet b1.58 3B (49.4 %) happens to score near LLAMA-3B (49.7 %). And the INT2
  weights come from **QAT** (BitDistiller) or from-scratch training (BitNet), not PTQ.
- **Peak vs end-to-end.** 61.55 TFLOPs/mm² is a **DP4 microbenchmark measured without partial
  sums** — a peak-of-a-peak. Prefer the 4×–6× Tensor-Core-level PPA, or the end-to-end
  8.2×, remembering the latter comes from the authors' own analytical simulator validated only
  on non-LUT configurations.
- **Evidence levels must not be pooled**: post-synthesis (PPA) / cycle-level simulator
  (kernel) / analytical model (end-to-end and all of Table 1). Three different kinds of fact.

## Note from the source list

> _(no keywords recorded in the source CSV)_


## Abstract (verbatim, arXiv:2408.06003v3)

> Large Language Model (LLM) inference becomes resource-intensive, prompting a shift toward
> low-bit model weights to reduce the memory footprint and improve efficiency. Such low-bit
> LLMs necessitate the mixed-precision matrix multiplication (mpGEMM), an important yet
> underexplored operation involving the multiplication of lower-precision weights with
> higher-precision activations. Off-the-shelf hardware does not support this operation
> natively, leading to indirect, thus inefficient, dequantization-based implementations. In
> this paper, we study the lookup table (LUT)-based approach for mpGEMM and find that a
> conventional LUT implementation fails to achieve the promised gains. To unlock the full
> potential of LUT-based mpGEMM, we propose LUT Tensor Core, a software-hardware co-design
> for low-bit LLM inference. LUT Tensor Core differentiates itself from conventional LUT
> designs through: 1) software-based optimizations to minimize table precompute overhead and
> weight reinterpretation to reduce table storage; 2) a LUT-based Tensor Core hardware
> design with an elongated tiling shape to maximize table reuse and a bit-serial design to
> support diverse precision combinations in mpGEMM; 3) a new instruction set and compilation
> optimizations for LUT-based mpGEMM. LUT Tensor Core significantly outperforms existing
> pure software LUT implementations and achieves a 1.44$\times$ improvement in compute
> density and energy efficiency compared to previous state-of-the-art LUT-based
> accelerators.
