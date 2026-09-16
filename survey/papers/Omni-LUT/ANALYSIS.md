# Omni-LUT — paper notes

**Omni-LUT: Energy-Efficient LUT-Based Accelerator with Hardware-Aware KV Cache Quantization**
Cheng-Han Tsai, Kuan-Chen Chou, Yu-Hsin Wang, Chieh-Dun Wen, Tsung Tai Yeh
**ISCA 2026** (2026 ACM/IEEE 53rd Annual International Symposium on Computer Architecture),
pp. 322–337 ｜ DOI: **10.1109/ISCA66397.2026.00037**
Publication info verified 2026-09-02 from the **official ISCA 2026 proceedings package**
(title, authors, pages, DOI and abstract all read from its `assets/data/data.js`).
Archived here: **the published proceedings PDF** (`506501a322.pdf`, 16 pages) — not a preprint.

Status: **note ready** ｜ Last updated: 2026-09-03
Tags: `lut-accelerator` `kv-cache` `non-analytical-dtype` `mixed-precision` `accelerator`
How far it was read: **close read of §I–§VIII** — introduction, §II background, §III (KV value
distribution, BC-UQ/BCQ, AS-Bit), §IV (architecture, BQU, scale-aware LGU, hybrid systolic
array), §V methodology, §VI.A–§VI.E (accuracy, kernel energy, system-level, overheads,
bit-width trade-off) and the conclusion. **Skimmed:** §VII related work, references. Figures
10–15 read for prose claims; per-bar values not transcribed.
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> The PDF is **not committed** (2.0 MB). It came from the proceedings package a human
> supplied, now archived at [`archieve/ISCA 2026.zip`](../../../archieve/), entry `pdfs/5065-3nexm57sBmVa6MJtFTiSrb/506501a322/506501a322.pdf`.
> **There is no public URL for it** — this is not an arXiv paper. Re-extract with
> `python3 extract.py` → `extracted/` (committed, greppable).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, 2026 row.

---

## Brief

### 1. Motivation

LUT-based GEMM accelerators only handle **activation–weight** GEMM in linear layers. But as
context grows, **activation–activation** GEMM in attention dominates: AW-GEMM scales as O(T)
while AA-GEMM scales as O(T²) in prefill, and in decode the KV cache must be read in full
for every token. A LUT accelerator that cannot do attention is solving the shrinking half of
the problem.

### 2. Overview

Extends LUT execution to **both** GEMM types. Doing so requires a LUT-consumable KV cache,
so the paper contributes a **BCQ-based KV quantization** design combining offline
calibration with lightweight online quantization, plus quantization compensation applied
*during LUT creation* to support the accuracy-preferred scaling direction (prior LUT designs
scale after lookup, which does not allow it). Hardware is a **phase-adaptive hybrid-
stationary LUT systolic array** serving prefill and decode differently.

### 3. Pros and cons

**Pros**

- Identifies a real structural gap — the O(T) vs O(T²) argument is the clearest
justification in the corpus for why attention, not the linear layers, is where long-
context effort belongs.
- The scaling-direction observation is a subtle, specific hardware insight: it explains
*why* prior LUT designs could not simply be pointed at attention.
- 1.25×–1.91× energy efficiency over the state-of-the-art LUT GEMM accelerator at equal peak
throughput, with competitive accuracy against dedicated KV quantization methods.

**Cons**

- Gains are reported at **equal peak-throughput** configuration — an iso-resource framing
that is fair but not the same as end-to-end serving throughput.
- KV quantization depends on offline calibration; the paper studies calibration-dataset
choice, which signals sensitivity worth checking before citing.
- Two mechanisms (BCQ KV quantization + phase-adaptive array) are entangled in the results;
their separate contributions are not obvious from the headline numbers.

### 4. Where it applies

Sits at the intersection of **LUT accelerators** and the **KV-cache** cluster, and is the
corpus's main argument that attention-side GEMM is the next target. Read after
[`LUTTensorCore`](../LUTTensorCore/ANALYSIS.md) and [`Oaken`](../Oaken/ANALYSIS.md).

---

## Conclusions

**Read in full 2026-09-03.** The brief survives intact — all three cons were correct — with
two additions.

**Added.** (a) **The node is TSMC 7 nm at 500 MHz**, not the 28 nm that most of this corpus
uses; comparisons against 28 nm entries are not like-for-like. (b) The brief did not record
that **activations stay FP16 throughout** — this is `W4A16KV3/KV4`, a weight-plus-KV design,
not a weight-and-activation one. That single fact separates it cleanly from
[`OASIS`](../OASIS/ANALYSIS.md) and decides how the two get grouped.

**Minor, for citation care:** the paper's own section numbering is disordered — §VI.B "GEMM
Kernel Performance Evaluation" is printed *before* §VI.A "Accuracy Evaluation", and §VIII
Conclusion appears before §VII Related Work (**verified**, extracted text).

---

## Method

**Verified** unless marked.

**The gap.** LUT-based GEMM accelerators execute **AW-GEMM** — high-precision activations
against low-bit weights — because the weight side is binary and can index a table. Attention's
**AA-GEMM** (`QK^T` and `Attn×V`) has *no* low-bit operand, so every prior LUT design falls
back to a floating-point systolic array for it. As context grows this is the wrong half to
accelerate: AW-GEMM scales O(T), AA-GEMM scales O(T²) in prefill, and decode must stream the
whole KV cache per token.

**The move: make the KV cache the binary operand.** Quantize K and V with **binary-coding
quantization (BCQ)** — decompose a vector into `±1` bit-planes times high-precision scaling
factors — and attention becomes structurally identical to AW-GEMM, so it can run on the same
LUT datapath. Three parts:

1. **Split strategy by tensor, driven by distribution** (§III-A). Keys show **stable
   per-channel outliers** → per-channel quantization, but per-channel statistics are global
   and cannot be estimated on the fly during autoregressive decode, so they are **calibrated
   offline**. Values are **highly token-dependent** with no stable channel structure →
   **online per-token BC-UQ**, cheap enough to run at inference time. Two mechanisms because
   the two tensors genuinely differ.
2. **AS-Bit — attention-aware bit allocation** (§III-C). A fixed bit width penalises every Key
   channel equally, but in `A = QK^T` the error `ΔK` is scaled by the corresponding Query
   magnitude. Sensitivity is therefore defined as per-channel quantization MSE weighted by
   **per-channel Query energy `E[Q²]_d`** — which is usable precisely because Fig. 3 shows Q
   *also* has stable per-channel structure. Sensitive channels get extra bit-planes.
3. **Scale-aware LUT generation (LGU)** — the subtle part (§IV-C). Prior LUT accelerators
   (FIGLUT) apply **a single scale after the lookup**, which can only express **column-wise**
   scaling. But the accuracy-optimal direction is **row-wise** for all three tensors: weights
   row-wise, Keys per-channel (= row-wise K in `QK^T`), Values per-token (= row-wise V in
   `Attn×V`). Post-lookup scaling cannot give four different scales to the four elements of a
   group, so it simply cannot express what accuracy wants. Omni-LUT therefore **scales inside
   the table generator**: each activation in the 4-element group is multiplied by its own
   scaling factor before the entries are enumerated, and **zero-point compensation is folded
   into the first bit-plane's entries**, removing a separate addition. *This is the enabler* —
   without it, AA-GEMM on a LUT costs accuracy.

**Which operand is which, in the two attention GEMMs** (**verified**, §IV-C and §VI.B —
*"Omni-LUT-KV3 processes three bit-planes for QK^T and for Attn × V"*):

| GEMM | Builds the LUT (FP16) | Indexes it (BCQ bit-planes) | Scale direction |
|---|---|---|---|
| `QK^T` | **Q** | **K** | row-wise K = per-channel, offline-calibrated |
| `Attn×V` | **Attn** (post-softmax) | **V** | row-wise V = per-token, online |

**Q is never quantized** — the configuration is `W4A16KV3/KV4` and Q is an activation. Compute
cost is linear in the number of bit-planes, which is why KV3 cuts AA-GEMM work by 25 % over
KV4.

**Where the quantization happens: on-chip, once per generated token** (§IV-B). The **BQU**
converts each newly generated K and V vector to BCQ bit-planes before it enters the cache, so
the cost amortizes over every later decode step that reads that token. Two asymmetric paths —
**Key**: scales offline-calibrated, bit-planes computed online; **Value**: scales *and*
bit-planes both online, via the TSE (pipelined min/max reduction tree → zero-point and step
size → power-of-two base scales {4, 2, 1, 0.5}) feeding the BEA's greedy residual algorithm,
one pass per bit-plane. Cost: **0.014 mm² (2.63 % area), 0.16 J (0.25 % energy)** — Table VII.
Note the paper states the **LGU** runs in parallel with the PE array but makes **no such claim
for the BQU**; whether BQU latency is hidden is `**inferred / not verified**`.

**Hardware** (§IV). A **32×4 LUT systolic array**, plus a **BQU** (token-scale estimator +
greedy-residual BCQ encoder) quantizing K and V on the fly, and the LGU. The array is
**phase-adaptive**: weight-stationary for GEMM-heavy prefill, and a GEMV-optimized
output-stationary mode (**OS-V**) for decode, which broadcasts one LGU's table vertically to
all rows (gating the others) and feeds each row from its own weight FIFO. The LGU builds a
**half-LUT** — 8 base entries for a 4-element group using 6 adders and 6 subtractors — with
the PE recovering complements by sign symmetry, and runs in parallel with the array, so table
generation adds no stall cycles.

## Key numbers, with their frame

**Frames.** Accuracy on WikiText-2 (train split for calibration, test for PPL) plus zero-shot
tasks. Hardware is **post-synthesis**: Synopsys DC at **500 MHz, TSMC 7 nm**, power via
PrimeTime PX, with a simulator **calibrated by gate-level simulation** (VCS) on kernels from
real inference tensors; SRAM macros in-process; DRAM via **DRAMPower, LPDDR5 at 51.2 GB/s**
across all baselines. FlashAttention with tile size 256, so attention matrices are never
materialised to DRAM. **No silicon.**

⚠️ **7 nm, not 28 nm.** Most of this corpus synthesizes at 28 nm; do not compare absolute
area or TOPS/W across that boundary.

| Setting | Model | Metric | Baseline | Result | Source |
|---|---|---|---|---|---|
| **Headline: equal peak throughput, long context** | OPT / LLaMA3 / Mixtral / Qwen3 | TOPS/W | **FIGLUT (W4A16KV16)** | **1.25×–1.91×** | §VI.B, p332 |
| Short/medium context (128, 1024 tokens) | same | Energy efficiency | FPE (FP16 baseline) | **+85–110 %** | §VI.B, p332 |
| Long context, decode-heavy (8192 output tokens) | OPT-6.7B | Energy reduction | FPE / Tender / FIGLUT | **59 % / 54 % / 46 %** | §VI.B |
| KV quantization accuracy | across models | Avg PPL increase | FP16 | **+0.17 at 4-bit, +0.75 at 3-bit** (BCQ) | §VI.A, p331 |
| **Effective KV bitwidth — the real efficiency claim** | — | bits | KIVI / KVQuant / Oaken: **4.8–5.0** avg | **4.25** effective Key bits (25 % high-bit fraction), **no extra bits on Value** | §VI.A, p331 |
| **BQU cost (on-chip KV quantization)** | OPT-6.7B, 8192 in / 512 out | area / energy | — | **0.014 mm² = 2.63 % of area; 0.16 J = 0.25 % of energy** | Table VII, p333 |
| Uniform vs BC-UQ, 4-bit KV | LLaMA3-8B / Qwen3-8B / 14B / 30B-A3B | WikiText-2 PPL | FP16 = 6.14 / 9.85 / 8.76 / 8.81 | Uniform-KV4 6.38 / **>500** / 10.49 / 14.12 → Omni **6.26 / 9.91 / 8.82 / 8.87** | Table IV |
| same, 3-bit KV | same | PPL | — | Uniform-KV3 7.90 / **>500** / 47.72 / 304.91 → Omni **6.79 / 10.04 / 9.06 / 9.14** | Table IV |
| Dataflow choice, prefill | OPT-6.7B, 4096 in / 512 out | Throughput | LUT OS | **LUT WS 1.3× better** | Fig. 10, p328 |
| Dataflow choice, decode | same | Throughput | LUT OS / LUT WS | **OS-V 1.49× / 1.68× better** | Fig. 10, p328 |
| Area efficiency | MHA / GQA / MoE models | TOPS/mm² | FPE | **2.8×–3.9×** (KV4) | §VI.C, p333 |
| Area | — | mm² @7 nm | **Tender 0.20** | **Omni-LUT 0.53** — 2.7× larger, comparable or better TOPS/mm² anyway | Table I, §VI.C |
| Compute-core breakdown | OPT-6.7B, 8192 in / 512 out | area / energy share | — | PE array **86.34 % / 90.09 %**; LGU 3.11 % / 5.36 %; **BQU 2.63 % / 0.25 %**; total 0.532 mm², 64.02 J | Table VII, p333 |
| KV bit-width sweep | LLaMA2-7B, 8192 in / 256 out | PPL vs TOPS/W | FP16 PPL = 5.47 | KV4 and KV3 small PPL rise; **KV2 → PPL 9.96, not deployable** | Fig. 15, p333 |
| Integer baseline at low bits | LLaMA2-7B | PPL | — | **Tender-INT4 → PPL 123.1** (catastrophic); Tender used at INT8 for this reason | §VI.E, p333 |

Left blank: per-bar values of Figs. 11–14, and the separate contribution of BCQ-KV vs the
phase-adaptive array — the brief's third con stands, they are **not** disentangled anywhere.

## Cost and requirements

- **Data type.** `W4A16KV4` and `W4A16KV3`. Weights 4-bit BCQ, **activations FP16**, KV cache
  3–4-bit BCQ. **Not** a weight-and-activation design — the activation side is untouched, and
  the paper says so explicitly: activation outliers make low-bit activations hard, so they
  stay high-precision.
- **Values are indices into ±1 bit-planes with high-precision scales** — binary-coding
  quantization, a non-uniform format. Taxonomy §1.3.
- **Granularity, per tensor, and it is the design.** Keys: **per-channel, offline-calibrated**,
  with AS-Bit giving sensitive channels extra bit-planes → effective **4.25 bits**. Values:
  **per-token, online**. Weights: row-wise. All three must be *row-wise* in the A×W
  formulation, which is exactly what the LGU exists to make possible.
- **Scaling-factor group size — no number is given; the paper states axes only.** From the BEA
  (§IV-C): a quantized vector takes a zero-point vector plus **q scaling factors, one per
  bit-plane**, and the two paths differ in what they are indexed by (**verified**: *"for the
  Key Path, the per-channel `zp_k,c` and `α_i,c` are fetched from offline-calibrated results;
  for the Value Path, the token-wise `zp_v` and `α_i` are provided by the TSE"*).

  | | Scale set | Shared across | Group on that axis | Group on the reduction axis |
  |---|---|---|---|---|
  | **K** (`QK^T`) | `zp_k,c` + q × `α_i,c` **per channel** | all tokens | **entire sequence T**, unbounded | channels → **1** |
  | **V** (`Attn×V`) | `zp_v` + q × `α_i = δ_v·{4,2,1,0.5}` **per token** | all channels | **d** (head dim) | tokens → **1** |

  **In both cases the scale is per-element along the reduction dimension and shared along the
  orthogonal one.** That is the structural reason scaling must move inside LUT generation: the
  4-element group needs four distinct scales and a single post-lookup scale cannot supply
  them — §IV-C's argument restated in group-size terms.

  **There is no sub-grouping on the shared axis**, unlike KIVI's group-of-G scheme. K scales
  are global over the whole sequence — which is precisely what makes on-the-fly estimation
  impossible and forces the offline calibration step. V scales cover the full token vector.
  `**inferred / not verified**`: that the absence of sub-grouping is a deliberate cost-saving
  rather than an omission; the paper does not discuss it.
- **Outliers — handled by choosing the granularity, not by isolating values.** The explicit
  claim is that Omni-LUT preserves accuracy *"without relying on high-precision outlier
  isolation"*, unlike KIVI, KVQuant and Oaken — and that this is why its effective bitwidth is
  4.25 rather than their 4.8–5.0. **This is the cleanest counter-example in the corpus to the
  inlier/outlier-split orthodoxy.**
- **Escape hatch.** Activations at FP16 is the big one. LUT entries are high-precision.
  Non-GEMM operators run on a VPU identical across all designs.
- **Retraining: PTQ**, but with a **mandatory offline calibration** step for Key channels
  (WikiText-2 train split), and BCQ's alternating optimization is *"a more intensive offline
  calibration step"* than BC-UQ. Calibration-dataset sensitivity is studied (Table V) — the
  brief's second con was right to flag it.
- **What the hardware pays.** BQU 2.63 % of area, LGU 3.11 %; together with control logic,
  **online quantization and control overhead is ~5 % of area and under 1 % of energy**. Cheap,
  and honestly reported.

## Limitations and open questions

**Authors admit:** KV2 is not deployable (PPL 9.96); Tender-INT4 collapses so the integer
baseline had to run at INT8; Amdahl's law pushes the non-GEMM fraction up as GEMM speeds up;
BCQ calibration is more expensive than BC-UQ.

**Not admitted:**

1. **The headline is an iso-peak-throughput comparison, at the single most favourable point.**
   1.25×–1.91× over FIGLUT is measured at **8192-token context** — where FIGLUT is forced onto
   its FP systolic backend for AA-GEMM. At 128 and 1024 tokens the two are much closer. The
   paper reports this honestly in prose but the abstract does not carry the qualifier.
2. **FIGLUT is run at KV16.** The comparison is `W4A16KV4` against `W4A16KV16`, so it folds in
   the memory-traffic gain of 4-bit KV — a quantization choice, not an architectural one. The
   architectural claim (LUT can execute AA-GEMM at all) and the algorithmic one (KV needs
   fewer bits) are measured together.
3. **7 nm, and the corpus is mostly 28 nm.** Absolute TOPS/W and mm² do not transfer.
4. **Two contributions entangled**, as the brief predicted: BCQ-KV quantization and the
   phase-adaptive array. Fig. 10 isolates the *dataflow* choice, and Table VII isolates
   *overheads*, but nothing isolates how much of 1.25–1.91× comes from which.
5. **Section numbering is disordered** (§VI.B before §VI.A; §VIII before §VII).
6. **Pre- or post-RoPE KV quantization is never stated — and it matters.** The only mention of
   RoPE in the paper is that it runs on the VPU as a non-GEMM operator (§V). But K is consumed
   **directly as bit-planes** by the LUT PEs and is never reconstructed in high precision, so
   there is no point at which RoPE could be applied afterwards, and RoPE's relative rotation
   depends on both query and key positions so it cannot be folded into Q alone. **The design
   therefore requires post-RoPE quantization** (`**inferred / not verified**`). That cuts
   against its own motivation: the stable per-channel Key outlier structure justifying
   per-channel offline calibration is a **pre-RoPE** property — RoPE mixes channel pairs and
   smears it, which is why KVQuant quantizes pre-RoPE. Fig. 3 shows the per-channel structure
   at LLaMA2-7B Layer-4 but **does not label the stage**. Either the hardware sees weaker
   structure than Fig. 3 implies, or Fig. 3 does not describe what the hardware sees.
   **Open question; do not cite Fig. 3's per-channel claim without resolving it.**

## Relation to other entries

- **The LUT thread, and the axis this paper adds.** With
  [`LUTTensorCore`](../LUTTensorCore/ANALYSIS.md) and [`OASIS`](../OASIS/ANALYSIS.md) the
  organizing question was *when is the table built* — eager per-tile, lazy per-tile, or offline
  and static. Omni-LUT is **eager per-tile like LUT Tensor Core** (*"a new LUT will be created
  when conducting the dot products of a new activation group"*), so it adds a **second axis:
  which operand is binarized.** Every prior LUT design binarizes weights, which is why none of
  them can touch attention. Omni-LUT binarizes the **KV cache**, and attention becomes
  LUT-shaped. **Framing for §5.6: a LUT accelerator's reach is set by which tensor you are
  willing to make binary.** (`**inferred / not verified**` as a framing.)
- **Direct contrast with `OASIS`.** Both 2026, both LUT, both attack the same shortfall from
  opposite sides. OASIS quantizes **both GEMM operands** (`W4A4`) to make the table *static*;
  Omni-LUT leaves **activations at FP16** and quantizes the **KV cache** to make *attention*
  reachable. OASIS's table is data-independent; Omni-LUT's is rebuilt per activation group.
  They should be a paired paragraph, not two entries in a list.
- **KV-cache cluster:** [`Oaken`](../Oaken/ANALYSIS.md) is both a cited baseline and a corpus
  entry — and Omni-LUT's central accuracy claim is *against* it and KIVI/KVQuant: **4.25
  effective bits without outlier isolation vs their 4.8–5.0 with it.** A direct, checkable
  cross-entry disagreement. Also [`Ecco`](../Ecco/ANALYSIS.md),
  [`P3-LLM`](../P3-LLM/ANALYSIS.md), [`SingularBit`](../SingularBit/ANALYSIS.md).
- **[`Tender`](../Tender/ANALYSIS.md)** is a baseline here, run at INT8 because its INT4 point
  gives PPL 123.1 — a corpus entry being used as evidence against itself at low bitwidth.
- **Non-corpus baselines:** FIGLUT, KIVI, KVQuant, QServe, NVFP4, Atom. Fourth consecutive
  paper leaning on non-ISCA work.

## For the note

### §1 one-line summary

> Quantizes the **KV cache** to 3–4-bit binary-coding bit-planes — per-channel offline for
> Keys with extra bit-planes on Query-energy-weighted sensitive channels, per-token online for
> Values — so that attention's activation×activation GEMM becomes structurally identical to
> activation×weight GEMM and can run on the same LUT datapath, with scaling folded **into**
> table generation so the accuracy-optimal row-wise direction survives, giving 1.25×–1.91×
> energy efficiency over a LUT accelerator that must fall back to floating point for attention.

### Proposed values on their four axes

| Axis | Proposed | Evidence (one line) |
|---|---|---|
| **Level** | **`ALGO+ARCH`** | The KV quantization scheme (BCQ/BC-UQ split, AS-Bit) is a contribution in its own right, and the LGU/BQU/phase-adaptive array is the architecture that makes it executable. |
| **Q-oriented** | `Q-ORIENTED` | Swap in plain INT8 and there are no bit-planes, no table, no LGU — and no reason for the design to exist. |
| **Data type** | **`LUT` + `VQ` + `INT4` + `INT3` + `FP16` + `MIXED`** | BCQ = binary bit-planes with high-precision scales (non-uniform, index-coded); `W4A16KV3/KV4` — note **A16**, activations are not quantized. |
| **Generation** | **`G3`** | Codebook/lookup thread plus the KV-cache thread, which is G3-specific. Not the outlier thread — it is explicitly an argument *against* outlier isolation. |
| **Optimization** (free text) | `LUT-GEMM` `KV cache` `BCQ` `binary-coding` `AA-GEMM` `attention` `scale-aware-LUT` `sensitivity-based-bit-allocation` `hybrid-stationary` `systolic` `phase-adaptive` | — |

### Proposed venue-list row

```
| [x] | Omni-LUT: Energy-Efficient LUT-based Accelerator with Hardware-Aware KV Cache Quantization | ALGO+ARCH | Q | `LUT` `VQ` `INT4` `INT3` `FP16` `MIXED` | G3 | `LUTGEMM` `KV cache` `BCQ` `AA-GEMM` `hybrid-stationary` | Binarizes the KV cache so attention's AA-GEMM runs on the LUT datapath; scaling folded into LUT generation to keep row-wise direction; 4.25 effective KV bits without outlier isolation |
```

### §4 fairness verdict

**Iso-throughput and iso-node yes; iso-precision no; and the headline is quoted from its best
operating point.**

- **Iso-node ✓** — all engines synthesized at TSMC 7 nm, 500 MHz, same DRAM model (LPDDR5,
  51.2 GB/s), same VPU for non-GEMM work, same FlashAttention tiling. Careful methodology.
- **Iso-peak-throughput ✓ and stated** — the 1.25×–1.91× is explicitly "configurations with
  equivalent peak throughput". That is a fair framing, and *not* the same as end-to-end
  serving throughput.
- **Iso-precision ✗** — FIGLUT runs `W4A16**KV16**`, Omni-LUT `W4A16**KV4**`. The comparison
  folds a 4× KV memory-traffic reduction into what reads as an architecture result.
- **Best-case operating point** — the headline is the **8192-token** number, where FIGLUT is
  forced onto its FP backend. At 128/1024 tokens the margin is much smaller, and the paper
  says so in prose but not in the abstract.
- **Iso-accuracy ✓ against the KV-quantization baselines, and this is the strongest part.**
  +0.17 PPL at 4-bit while using **4.25 effective bits against KIVI/KVQuant/Oaken's 4.8–5.0** —
  fewer bits *and* no outlier-isolation hardware.
- **Cross-node caution** — 7 nm here vs 28 nm for most of the corpus.

## Abstract (verbatim, ISCA 2026 proceedings)

> Large language model (LLM) inference incurs substantial computation and energy
> consumption. Lookup-table (LUT)-based general matrix multiplication (GEMM) accelerators
> reduce this burden by replacing costly multiplications with table lookups. However,
> existing designs only support activation-weight GEMM (AW-GEMM) in LLM linear layers, while
> LUT execution for activation-activation GEMM (AA-GEMM) in attention has not been realized.
> As AA-GEMM is a major contributor to the computation and energy costs of LLM inference in
> long-context scenarios, supporting both GEMM types-not just AW-GEMM-is crucial. To solve
> this problem, we propose Omni-LUT, a hardware-software co-designed LUT-based GEMM
> accelerator that supports both AW-GEMM in linear layers and AA-GEMM in attention with
> efficient LUT execution. Omni-LUT uses a hardware-aware Key-Value (KV) cache quantization
> design that combines offline calibration with lightweight online quantization, preserving
> model accuracy while enabling compatibility with LUT accelerators. It also supports a more
> accurate quantization direction by leveraging quantization compensation during LUT
> creation. Omni-LUT further comprises a phase-adaptive hybrid-stationary LUT-based systolic
> array to improve the efficiency of both the prefill and decode phases in LLMs. Across
> diverse long context workloads, Omni-LUT achieves 1.25x-1.91x higher energy efficiency
> than the state-of-the-art (SOTA) LUT-based GEMM accelerator under an equal peak-throughput
> hardware setup, while maintaining competitive model accuracy compared with SOTA KV
> quantization methods.
