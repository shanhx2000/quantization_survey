# BitFusion — paper notes

**Bit Fusion: Bit-Level Dynamically Composable Architecture for Accelerating Deep Neural Networks**
Hardik Sharma, Jongse Park, Naveen Suda, Liangzhen Lai, Benson Chau, Joon Kyung Kim, Vikas
Chandra, Hadi Esmaeilzadeh
**ISCA 2018** ｜ DOI: **not recorded** — the ACM/IEEE record is not reachable by script (403); look it up when citing
Venue evidence (**updated 2026-09-09 — now verified**): line 1 of the archived arXiv PDF's own
text reads, verbatim, *"Appears in the Proceedings of the 45th International Symposium on
Computer Architecture (ISCA), 2018"*. This was the last entry `survey/README.md` listed as
having an unverified venue; that note can now be dropped entirely.
Archived here: **arXiv:1712.01507v2** (2018-05-30), 12 pages — **the preprint, not the
published ISCA 2018 version**; the two were **not compared**.

Status: **note ready** ｜ Last updated: 2026-09-09
Tags: `analytical-dtype` `mixed-precision` `multi-bitwidth-hw` `accelerator`
How far it was read: **full close read of §I-§VII.** §II (architecture), §III (microarchitecture,
including the recursion in Eqs. 1-3 and the spatial-vs-temporal comparison in Fig. 10), §V
(evaluation, including Tables II-III and every per-benchmark comparison) read line by line;
§IV (Fusion-ISA) read for its cost and granularity implications rather than its encoding;
§VI-VII in full. Figures 11-15 are bitmaps in the extraction, so per-benchmark numbers below come
from the prose and from the numeric fragments recoverable in the layout extraction — **each is
marked where its source is a recovered table fragment rather than a sentence**. Read after
[`DRQ`](../DRQ/ANALYSIS.md), which borrows this paper's PE and MAC-area model.
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> Original: https://arxiv.org/abs/1712.01507
> The PDF is **not committed** (1.6 MB). Re-download: `curl -sSL -o 1712.01507.pdf https://arxiv.org/pdf/1712.01507`
> Extract text: `python3 extract.py` → `extracted/` (committed, greppable)
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, ISCA 2018 row.

---

## Brief

### 1. Motivation

Different DNNs — and different layers of the same DNN — tolerate different bitwidths, but a
fixed-bitwidth accelerator must be built for the worst case or lose accuracy. The paper's
framing datum: >99% of DNN operations are multiply-adds, and multiplier cost scales with the
*product* of operand bitwidths, so matching the datapath to each layer's width cuts bit-
level work almost quadratically.

### 2. Overview

An array of bit-level processing elements ("BitBricks") that **dynamically fuse and
decompose at runtime** to form multipliers of the width each layer needs, exposed through a
dedicated ISA (Fusion-ISA) so software drives the composition. Evaluated in Verilog at 45 nm
plus cycle-accurate simulation over eight CNN/RNN benchmarks.

### 3. Pros and cons

**Pros**

- The canonical bit-composable design: one substrate spans 1–8 bit operands with **no
accuracy loss**, since it matches whatever width the model already needs.
- Gains are large against fixed-width and bit-serial baselines alike — 3.9×/5.1×
speedup/energy over Eyeriss, 2.6×/3.9× over Stripes at iso-area and frequency.
- The ISA makes the flexibility programmable rather than a fixed mode switch, which is what
later composable designs inherit.

**Cons**

- Composability is bought with wiring and control overhead; the quadratic-resource problem
that this style of design hits at *high* precision is only named as a limitation by later
work (see [`UniCore`](../UniCore/ANALYSIS.md)), not confronted here.
- Per-layer bitwidths are assumed given — the quantization algorithm that produces them is
out of scope, so the accuracy claim rests on prior work's models.
- The GPU comparison scales 45 nm results to 16 nm analytically rather than measuring; treat
the Titan Xp parity claim as a projection.

### 4. Where it applies

The reference point for any **multi-bitwidth datapath** argument, and the baseline most
later mixed-precision accelerators compare against. Read it first in the architecture axis
of the taxonomy (§2.1 tensor-wise, with per-layer width selection).

---

## Corrections to the brief

The brief's framing was right. Three things it did not have:

1. **Venue is now verified** from the PDF's own first line (see header). `survey/README.md`'s
   "unverified venues" note can be retired.
2. **BitFusion contributes no quantization algorithm, and says so.** §V-A: "We did **not**
   engineer these quantized DNNs and merely took them from the existing deep learning literature
   [32, 34-36]" **verified**. Bitwidths come from DoReFa-Net, TTQ, WRPN and [35]. Every "no
   accuracy loss" claim in the paper is **inherited**, not demonstrated. This settles the Level
   tag at `ARCH` and makes the paper a pure hardware-mechanism entry.
3. **The two ImageNet benchmarks run a 4× larger workload than the baseline's.** AlexNet and
   ResNet-18 use WRPN's **2×-wide** models — double the channels — to hold accuracy at 4 bits,
   while Eyeriss runs the original models. §V-B states it outright: "We use the original AlexNet
   and ResNet-18 models on Eyeriss, which effectively requires **4× less multiply-add
   operations**" **verified**. This is the single most important frame on the headline number.

---

## Conclusions

**The contribution is spatial fusion, and Fig. 10 is where the paper actually proves something.**
Bit-serial precision flexibility already existed (Stripes, Tartan, Loom, UNPU). BitFusion's claim
is that you should compose 2-bit multipliers **spatially in one cycle** rather than **temporally
over many**, and it measures the difference against an equivalent temporal design at 45 nm:
**3.5× area, 3.2× power**. The mechanism behind that is specific and worth the survey's attention:
**16× of the saving is in the register/accumulator** (1454 → 91 µm²), because spatial fusion feeds
a shift-add tree into **one shared accumulator** while the temporal design needs an accumulator
sized for the largest supported bitwidth per unit. §III-C: in a temporal 16-bit design "the
shifter and the accumulator use up around **90%** of the area" — and Fig. 10 confirms it,
(2989+1454)/4905 = **90.6%**.

**The mathematical core is one line and it recurs.** A multiply between power-of-2-bitwidth
operands decomposes into 2-bit multiplies recombined by shift-add (Eqs. 1-3), applied recursively
16→8→4→2. Each level of recursion costs shift-add logic, and **that logic is the price of bit-level
flexibility**. Because the decomposition is per-operand, the two operands need not share a width —
`W2A8`, `W4A4`, `W8A2` all cost the same four BitBricks, which is the property bit-serial designs
flexible on only one operand cannot match.

**But BitFusion is a *mechanism* paper wearing a *quantization* paper's clothes.** It quantizes
nothing, chooses no bitwidths, and handles no outliers. It takes a per-layer bitwidth assignment
someone else produced and builds a datapath that can execute it without waste. Read against the
rest of this corpus, that is its identity: **the multi-precision-hardware root**, not a
quantization-format contribution.

**The headline numbers need their range, not their geomean.** "3.9× over Eyeriss" spans **1.9×
(AlexNet, ResNet-18) to 13× (Cifar-10)**, and the split is not random — it is exactly the split
between ImageNet and everything else. Six of eight benchmarks are MNIST/CIFAR-10/SVHN/Penn
TreeBank scale, where 1-bit and 2-bit operands work and BitFusion's 16-way fusion parallelism is
fully exposed. On the two ImageNet models, 4-bit accuracy in 2018 required doubling the network
width, and the architecture's win drops to 1.9× against a 4× smaller workload.

**"Almost matches a 250 W Titan Xp" is a geomean artifact.** Per benchmark, against Titan Xp with
INT8: AlexNet **3.2 vs 23** and ResNet-18 **5 vs 31** — BitFusion is **6-7× slower** on both
ImageNet models — while LSTM (38 vs 6.7) and RNN (39 vs 7.2) are **5-6× faster**. Geomean 16 vs 19.
The claim that survives per-benchmark scrutiny is not performance parity; it is **5.93 mm² and
895 mW against 471 mm² and 250 W** — 79× the area efficiency and 280× the power. That is a real
and large result, and the paper would have been better served by leading with it.

---

## Method

**What is flexible.** Operand bitwidth, **per layer**, for both operands independently, over
{2, 4, 8, 16} bits (plus binary/ternary as the 1-2 bit case). Set by the ISA, not by data.

**BitBrick** (§III-A, Fig. 5) — the atom. A **2-bit signed multiplier**: two 2-bit operands `x2b`,
`y2b` plus sign bits `sx`, `sy`, built from half- and full-adders, producing `p0..p6`. Operands may
be signed or unsigned. It is the smallest unit and everything else is composed from it.

**The recursion** (§III-A, Eqs. 1-3) **verified**. For `2n`-bit operands:

```
A₂ₙ = 2ⁿ·(A₂ₙ)hi + 2⁰·(A₂ₙ)lo
A₂ₙ × B₂ₙ = 2²ⁿ·(A)hi(B)hi + 2ⁿ·(A)hi(B)lo + 2ⁿ·(A)lo(B)hi + 2⁰·(A)lo(B)lo
A₂ₙ × Bₙ   = 2ⁿ·(A₂ₙ)hi·Bₙ + 2⁰·(A₂ₙ)lo·Bₙ        (unequal widths)
```

Applied 16→8→4→2. **Only the shift amounts differ between configurations** — a 4b×4b multiply and
two 4b×2b multiplies use the same four BitBricks and differ only in how the partial products are
shifted before summation. At 2b×2b all shifts are zero and each BitBrick does one independent
multiply.

**Fusion Unit** (§II-A, §III-C) — 16 BitBricks in a 2-D group, fusing **in powers of 2** to yield
**1, 2, 4, 8 or 16 Fused-PEs**:

| Fused-PEs | Configuration | Parallelism |
|---|---|---|
| 16 | binary (0,+1) / ternary (−1,0,+1) | 16× |
| 4 | W2×A8, W4×A4, W8×A2 | 4× |
| 1 | W8×A8 | 1× |

Higher widths (16-bit) fuse across Fusion Units by the same recursion.

**Spatial vs temporal** (§III-C, Figs. 8-10) — the paper's actual experiment. Both designs do
(1) 2-bit multiply, (2) shift, (3) accumulate. The **temporal** design (a deliberately favourable
model of bit-serial — it uses 2-bit, not 1-bit, units) takes **4 cycles** for a 4b×4b multiply, and
its shifter and accumulator must be sized for the **maximum** supported width (16 bits) in every
unit. The **spatial** design combines four BitBricks' products in **one cycle** through a shift-add
tree — three shift units and a four-input adder per level — into **one shared accumulator**.

**Systolic organisation** (§II-B, Fig. 3). A 2-D systolic array of Fusion Units: IBUFs at the row
borders feed inputs across, partial sums accumulate down columns, OBUFs at the bottom, with a
pooling and an activation unit per column. Each Fusion Unit carries only a **WBUF** — the systolic
dataflow removes the need for local input/output/psum buffers inside the unit, which is where the
area for extra BitBricks comes from. Input and weight buffers are augmented with a row register
plus multiplexers so one fetch can be fed out at whatever bitwidth the current fusion demands.

**Accumulator: 32-bit.** §III: "we support **32-bit** bitwidth for the partial and final results
to avoid any inaccuracies" **verified**. Full width, no truncation — the widest accumulator in the
corpus so far (`OLAccel` 24 b, `DRQ` 16 b).

**Fusion-ISA** (§IV). Block-structured with iterative semantics, so the cost of choosing a fusion
configuration is **amortised across a whole layer** rather than paid per operation. Instructions:
`setup`, `loop` (with `num-iterations`), `compute`, `gen-addr` (with `stride` and `loop-id`);
addresses generated as `base + Σᵢ loop_iterator[i]·stride[i]`. **This is why the granularity is
per-layer** — the ISA has no way to express a finer switch, and that is a deliberate trade against
control overhead.

**Quantization.** None. Models and bitwidths are taken unmodified from DoReFa-Net [32], TTQ [34],
[35] and WRPN [36].

---

## Key numbers, with their frame

Evidence level: **Verilog + synthesis in 45 nm** for the datapath, **cycle-accurate simulation**
(verified against the Verilog for cycle counts) for performance, **CACTI-P** for on-chip buffer
energy, and **analytical node scaling** (0.86× voltage, 0.42× capacitance) for the 16 nm GPU
comparison. Eyeriss numbers come from its authors' open-source simulator scaled to 45 nm; Stripes
numbers from its authors' simulator with 65 nm power scaled to 45 nm. **No silicon.** Do not pool
the synthesised 45 nm figures with the analytically scaled 16 nm ones.

| Setting | Model | Metric | Baseline | Result | Source |
|---|---|---|---|---|---|
| **Fusion Unit vs temporal design**, 45 nm | — | **total area** | temporal 4905 µm² | **1394 µm² — 3.5×** | Fig. 10 **verified** |
| " | — | **total power** | temporal 1712 nW | **538 nW — 3.2×** | Fig. 10 **verified** |
| " — where the saving is | — | register/accumulator area | 1454 µm² | **91 µm² — 16.0×** | Fig. 10 **verified** |
| " | — | shift-add area / BitBrick area | 2989 / 463 µm² | 934 (3.2×) / 369 (1.3×) | Fig. 10 **verified** |
| Temporal design's problem | — | share of area in shifter+accumulator | — | **~90%** (derived: 90.6%) | §III-C **verified** |
| Iso-area, iso-frequency, iso-SRAM, 45 nm | 8 CNN/RNN benchmarks | **speedup geomean** | **Eyeriss** (16-bit) | **3.9×** | §V-B **verified** |
| " | " | **energy reduction geomean** | Eyeriss | **5.1×** | §V-B **verified** |
| " — **the range matters more** | Cifar-10 (best) → AlexNet, ResNet-18 (worst) | speedup | Eyeriss | **13× → 1.9×** | §V-B **verified** |
| " — per benchmark | VGG-7 / SVHN / LeNet-5 / LSTM / RNN | speedup / energy | Eyeriss | **7.7/9.9 · 5.1/4.3 · 2.7/4.3 · 2.4/4.8 · 2.7/5.1** | Fig. 13, recovered table fragment — **treat as approximate** |
| **Workload asymmetry** | AlexNet, ResNet-18 | multiply-adds run | Eyeriss runs original models | **BitFusion runs 2×-wide (WRPN) models = 4× more MACs** | §V-A, §V-B **verified** |
| Iso-area (1.1 mm² compute), iso-memory, 45 nm | 8 benchmarks | **speedup / energy geomean** | **Stripes** (bit-serial) | **2.6× / 3.9×** | §V-B **verified** |
| " — per benchmark | AlexNet / Cifar-10 / LSTM / LeNet-5 / ResNet-18 / RNN / SVHN | speedup, energy | Stripes | **1.8/2.7 · 4/6 · 2.1/3.1 · 5.2/7.8 · 2.6/4.4 · 2/3 · 1.8/2.7** | recovered table fragment — **treat as approximate** |
| Scaled to 16 nm, 500 MHz (not raised) | 8 benchmarks | **speedup geomean** | **Jetson TX2 FP32** | **16×** | §I, §V-B **verified** |
| " | " | speedup geomean | **Titan Xp INT8 = 19×** over TX2 | **BitFusion 16× — i.e. 0.84×, not parity** | recovered table + §V-B **verified as "almost matches"** |
| " — **per benchmark, vs Titan Xp INT8** | AlexNet / ResNet-18 | speedup over TX2-FP32 | Titan Xp INT8 **23 / 31** | **BitFusion 3.2 / 5 — 7.2× and 6.2× SLOWER** | recovered table fragment |
| " — the other end | LSTM / RNN / VGG-7 | speedup over TX2-FP32 | Titan Xp INT8 6.7 / 7.2 / 30 | **BitFusion 38 / 39 / 48** | recovered table fragment |
| **The claim that survives** | — | chip area / power at 16 nm | **Titan Xp: 471 mm², 250 W TDP** | **BitFusion: 5.93 mm², 895 mW** | §V-B, Table III **verified** |
| 45 nm configuration | — | compute area / chip area / SRAM / clock | Eyeriss 168 PEs, Stripes 4096 SIPs/tile | **1.1 mm² / 5.87 mm² / 512 KB / 500 MHz** | §V-A **verified** |
| 16 nm configuration | — | Fusion Units / SRAM | — | **4096 FUs / 896 KB** | §V-B **verified** |
| Motivating datum | AlexNet | multiply-add share of all ops | — | **99.86%** (2678 of 2682 Mops) | §I **verified** |
| " | 8 benchmarks | share of multiply-adds needing ≤4 bits | — | **97.3% average** | §I **verified** |
| Batch sensitivity | AlexNet / ResNet-18 vs LSTM / RNN | speedup, batch 1 → 256 | — | **1.42× / 1.04× vs 21.1× / 21.4×** | recovered table fragment — **CNNs barely benefit from batching, RNNs enormously** |

---

## Cost and requirements

| | |
|---|---|
| **Shift-add logic** | The explicit price of flexibility. Each recursion level (16→8→4→2) adds a shift-add tree stage. Still **934 µm² of the Fusion Unit's 1394 µm² — 67% of the unit's area is not multipliers** |
| **Accumulator** | **32-bit**, full width, deliberately not truncated. One **shared** per Fusion Unit — the shared accumulator is where the 16× advantage over temporal designs comes from |
| **Buffer feed logic** | Row register + multiplexer chain on IBUF and WBUF so a single fetch can be dispensed at any bitwidth |
| **ISA** | A new one (Fusion-ISA) plus a compiler. Block-structured with iterative semantics precisely to **amortise** fusion-configuration cost over a layer. **High adoption barrier** — this is not a drop-in datapath change |
| **Granularity** | **Per layer.** Nothing finer is expressible in the ISA, and this is a deliberate trade against control overhead (§II-B: "essential to minimize the overhead of control") |
| **Quantization** | **Supplied by someone else.** No calibration, no retraining, no bitwidth search of its own. It inherits whatever the source paper achieved — including WRPN's 2×-wide models |
| **Outliers** | **None.** No mechanism, no discussion. Uniform bitwidth within a layer |
| **Escape hatch** | The 32-bit psum path, and the fact that any layer needing 16 bits simply gets 16 bits at 1/16 the parallelism |
| **Model-shape dependence** | Benefit ∝ how low the bitwidths go. On ImageNet-scale models where 2018-era 4-bit needed 2× width, most of the theoretical gain is spent buying accuracy back |

---

## Limitations and open questions

**Admitted, and creditably so.**

- The 2×-wide-model asymmetry on AlexNet/ResNet-18 is stated plainly in §V-B, including the "4×
  less multiply-add operations" for the Eyeriss baseline. Many papers would have buried it.
- The temporal baseline is deliberately made *stronger* than real bit-serial ("even the temporal
  design uses 2-bit multipliers, a configuration that provides a better area, delay, and power as
  opposed to a fully bit-serial design").
- 16 nm scaling is called "conservative" and the frequency is deliberately **not** raised from
  500 MHz.

**Unadmitted, and material.**

- **"Almost matches Titan Xp" is only true at the geomean.** Per benchmark it is 6-7× slower on
  both ImageNet CNNs and 5-6× faster on two tiny RNNs. A geomean over a benchmark set that mixes
  ImageNet with Penn TreeBank is not a summary of anything.
- **The benchmark set does the work.** Six of eight are MNIST/CIFAR-10/SVHN/Penn TreeBank. The
  average "97.3% of multiply-adds need ≤4 bits" is over that set, and Cifar-10's 13× comes from
  "most of its operations can be computed with the smallest bitwidth (1-bit input, 1-bit weight)".
  Neither number transfers to modern models.
- **No area breakdown for the ISA, control, or the buffer multiplexer chain.** Fig. 10 covers the
  Fusion Unit only. The 1.1 mm² compute budget is matched to Eyeriss, but what fraction is control
  is never shown — a real gap for a paper whose §II-B argument is that control overhead must be
  minimised.
- **Per-layer is the finest granularity, and the paper treats that as settled.** Every later
  entry in this corpus argues the opposite (per-channel, per-group, per-region, per-token). No
  sensitivity study asks what a finer switch would buy or cost here.
- **The Stripes characterisation is internally inconsistent.** §V-A says Stripes "operates on
  16-bit **inputs** and variable-bitwidth **weights**"; §VI says it provides "precision flexibility
  for **inputs**". One of these is backwards. What matters for the comparison holds either way:
  Stripes varies **one** operand, BitFusion varies **both**, and the work saved scales with the
  *product*.
- **Nothing about memory formats.** The paper claims reduced memory traffic from storing values at
  their native bitwidth, but there is no packing format, no alignment discussion, and no metadata
  accounting — the problem that consumes half of `OliVe` and `MicroScopiQ`.

---

## Relation to other entries

**This is the multi-precision-hardware root of the corpus, and it is `G2` for the right reason.**
The `G2` paradigm is *make the datapath match the bitwidth*; `G3`'s is *give the tail its own
format*. BitFusion is the purest statement of the former: a datapath with no opinion whatsoever
about what the numbers mean.

**Direct descendants.**

- **[`DRQ`](../DRQ/ANALYSIS.md) (ISCA'20) is its closest architectural descendant here.** DRQ's
  multi-precision PE is credited to BitFusion by name; DRQ's MAC-area model (INT4 100.5 / INT8
  377.5 / INT16 1423 µm² at 45 nm) prices BitFusion's PE; and BitFusion is the baseline **DRQ's
  abstract silently drops** — the +83% performance / −49% energy figures appear only in DRQ §VI-A.
  Note the reversal: BitFusion fuses **spatially in one cycle**, DRQ's PE goes back to
  **time-multiplexing over four cycles**, which is precisely the temporal design Fig. 10 shows
  losing 3.5×/3.2×. DRQ never addresses this.
- **[`Tender`](../Tender/ANALYSIS.md), [`MicroScopiQ`](../MicroScopiQ/ANALYSIS.md) and
  [`Oaken`](../Oaken/ANALYSIS.md)** all assume multi-precision PEs as a solved substrate. This is
  the paper that solved it.
- **`Stripes` (MICRO'16)** is the road not taken, and BitFusion is the corpus's best citation for
  **why spatial beat bit-serial**: 3.5× area and 3.2× power, 16× of it in the accumulator.

**Its place on the granularity axis is the coarse anchor.** BitFusion per-layer (2018) → `OLAccel`
per-layer threshold with per-value escape (2018) → `DRQ` per-region (2020) → `Tender` per-channel
band (2024) → `Oaken`/`MicroScopiQ` per-group (2025). The survey's granularity story starts here,
and BitFusion is the entry that shows the *hardware* cost of going finer: the ISA exists to
amortise reconfiguration, so finer switching is not free in this design family.

**`TAXONOMY.md` uses this paper as its worked example**, and the close read supports that choice —
it is unusually clean on all four axes (`ARCH`, `Q-ORIENTED`, a genuinely multi-valued data-type
cell, unambiguous `G2`).

**Node.** 45 nm synthesised, plus an analytically scaled 16 nm point. The corpus now spans
7 nm (`MicroScopiQ`, `Omni-LUT`) → 65 nm (`OLAccel`), with `DRQ` and BitFusion at 45 nm — and
BitFusion is the only entry so far carrying **two** nodes, which is a trap for any aggregate table.

**Outside-corpus references it makes load-bearing:** `Eyeriss` (ISCA'16), `Stripes` (MICRO'16),
and the four quantization papers it inherits models from — **DoReFa-Net**, **TTQ**, **WRPN**
[36] and [35]. WRPN matters most: the "2× wide" models are the reason the ImageNet speedups are
1.9×, and WRPN is not in the corpus.

---

## For the note

**§1 one-line summary.** Decomposes every multiply into **2-bit BitBrick products recombined by a
shift-add tree in a single cycle**, so a 16-BitBrick Fusion Unit fuses in powers of two into 1, 4
or 16 Fused-PEs matching whatever per-layer bitwidth (2/4/8/16, **independently per operand**) the
model needs — buying **3.5× area and 3.2× power over an equivalent bit-serial/temporal design**
(16× of it in the shared accumulator alone) and 3.9× speedup / 5.1× energy over Eyeriss at
iso-area, while contributing **no quantization algorithm of its own**.

**Proposed tags — the seed row is right on all four; I would only extend the data-type cell.**

| Axis | Value | Evidence |
|---|---|---|
| **Level** | `ARCH` | §V-A: "We did not engineer these quantized DNNs and merely took them from the existing deep learning literature." Verilog, synthesis, an ISA, a compiler — and zero algorithm. Seed agrees |
| **Q-oriented** | `Q-ORIENTED` | Swap in a fixed INT8 datapath and the BitBrick, the shift-add tree, the fusion control, the buffer multiplexer chain and the entire Fusion-ISA lose their reason to exist. Seed agrees |
| **Data type** | `INT8` `INT4` `INT2` `INT1` `MIXED` (+ `INT16`) | 2/4/8/**16**-bit supported by recursion (§III-A), binary and ternary at 16× parallelism, **operands independently sized**, 32-bit psum. Seed has the first five — I would **add `INT16`**, which the recursion explicitly reaches |
| **Generation** | `G2` | Match the datapath to the bitwidth; no tail format, no outlier concept, no codebook. Seed agrees |
| **Optimization** | `bit-flexible MAC` `BitBrick` `spatial fusion` `shift-add tree` `shared accumulator` `Fusion-ISA` `per-layer bitwidth` `systolic` `mixed operand widths` | Seed has the first, second, sixth and seventh; **`spatial fusion` and `shared accumulator` are the mechanism and deserve to be there** |

**§4 fairness verdict.** Iso-area (1.1 mm² compute), iso-SRAM, iso-frequency (500 MHz), baselines
re-simulated by their authors' own tools and scaled to 45 nm — good discipline. **Not iso-workload**:
AlexNet and ResNet-18 run 2×-wide WRPN models, **4× more MACs** than Eyeriss's originals, which the
paper states. **Numbers not to quote bare:** "3.9× over Eyeriss" (range is 1.9×-13×, and the low
end is both ImageNet models); "almost matches Titan Xp" (geomean 16 vs 19, but 6-7× slower on
AlexNet and ResNet-18 per-benchmark). **Quote instead:** 5.93 mm² / 895 mW vs 471 mm² / 250 W, and
the 3.5×/3.2× over the temporal design — the one number in the paper measured against a control
the authors built themselves.

**Proposed venue-list row:**

```
| [ ] | [Bit Fusion: Bit-Level Dynamically Composable Architecture for Accelerating Deep Neural Network](https://arxiv.org/abs/1712.01507) | *close read* | ARCH | Q | `INT16` `INT8` `INT4` `INT2` `INT1` `MIXED` | G2 | `bit-flexible MAC` `BitBrick` `spatial fusion` `shift-add tree` `shared accumulator` `Fusion-ISA` `per-layer bitwidth` | Bit-level PEs that fuse and decompose at runtime, **spatially in one cycle** — 3.5× area / 3.2× power over an equivalent bit-serial design, 16× of it in the shared accumulator. A [TAXONOMY](../../TAXONOMY.md) worked example. **Venue verified from the arXiv PDF's own first line** |
```

## Note from the source list

> **Keywords:** a bit-flexible accelerator


## Abstract (verbatim, arXiv:1712.01507v2)

> Fully realizing the potential of acceleration for Deep Neural Networks (DNNs) requires
> understanding and leveraging algorithmic properties. This paper builds upon the
> algorithmic insight that bitwidth of operations in DNNs can be reduced without
> compromising their classification accuracy. However, to prevent accuracy loss, the
> bitwidth varies significantly across DNNs and it may even be adjusted for each layer.
> Thus, a fixed-bitwidth accelerator would either offer limited benefits to accommodate the
> worst-case bitwidth requirements, or lead to a degradation in final accuracy. To alleviate
> these deficiencies, this work introduces dynamic bit-level fusion/decomposition as a new
> dimension in the design of DNN accelerators. We explore this dimension by designing Bit
> Fusion, a bit-flexible accelerator, that constitutes an array of bit-level processing
> elements that dynamically fuse to match the bitwidth of individual DNN layers. This
> flexibility in the architecture enables minimizing the computation and the communication
> at the finest granularity possible with no loss in accuracy. We evaluate the benefits of
> BitFusion using eight real-world feed-forward and recurrent DNNs. The proposed
> microarchitecture is implemented in Verilog and synthesized in 45 nm technology. Using the
> synthesis results and cycle accurate simulation, we compare the benefits of Bit Fusion to
> two state-of-the-art DNN accelerators, Eyeriss and Stripes. In the same area, frequency,
> and process technology, BitFusion offers 3.9x speedup and 5.1x energy savings over
> Eyeriss. Compared to Stripes, BitFusion provides 2.6x speedup and 3.9x energy reduction at
> 45 nm node when BitFusion area and frequency are set to those of Stripes. Scaling to GPU
> technology node of 16 nm, BitFusion almost matches the performance of a 250-Watt Titan Xp,
> which uses 8-bit vector instructions, while BitFusion merely consumes 895 milliwatts of
> power.
