# Bit Fusion: Bit-Level Dynamically Composable Architecture for Accelerating Deep Neural Networks

**Venue / Year:** ISCA 2018 · **Link:** https://arxiv.org/abs/1712.01507 · **Reader:** Haoxuan · **Date:** 2026-09-09

## Tags

| | |
|---|---|
| **Level** | `ARCH` |
| **Q-oriented** | `Q-ORIENTED` |
| **Data type** | `INT16` `INT8` `INT4` `INT2` `INT1` `TERNARY` `MIXED` |
| **Generation** | `G2` |
| **Optimization** | bit-flexible MAC · BitBrick · spatial fusion · shift-add tree · shared accumulator · Fusion-ISA · per-layer bitwidth · mixed operand widths · systolic |

## 1. One-line summary

Decomposes every multiply into **2-bit BitBrick products recombined by a shift-add tree in a
single cycle**, so a 16-BitBrick Fusion Unit fuses in powers of two into 1, 4 or 16 Fused-PEs
matching whatever per-layer bitwidth (2/4/8/16, **independently per operand**) the model needs —
buying **3.5× area and 3.2× power over an equivalent bit-serial/temporal design** (16× of it in
the shared accumulator alone) and 3.9× speedup / 5.1× energy over Eyeriss at iso-area, while
contributing **no quantization algorithm of its own**.

## 2. Data type

**Bitwidths, not formats.** Plain signed/unsigned INT at 2/4/8/**16** bits, plus binary (0,+1) and ternary (−1,0,+1). No new number representation anywhere.
**Both operands sized independently.** W2A8, W4A4, W8A2 all cost the same four BitBricks — only the shift amounts differ. This is what bit-serial designs flexible on one operand cannot do.
**Granularity: per layer.** Set by the ISA, not by data. Nothing finer is expressible — a deliberate trade against control overhead.
**Outliers.** **None.** No mechanism, no discussion, uniform bitwidth within a layer.
**Accumulator.** **32-bit**, full width, explicitly untruncated "to avoid any inaccuracies". Widest in the corpus (OLAccel 24 b, DRQ 16 b). One **shared** accumulator per Fusion Unit — this is where the win over bit-serial comes from.
**Escape hatch.** Any layer needing 16 bits simply gets 16 bits, at 1/16 the parallelism. Plus the 32-bit psum path.
**Retraining.** **N/A — it quantizes nothing.** §V-A: "We did not engineer these quantized DNNs and merely took them from the existing deep learning literature." Bitwidths come from DoReFa-Net, TTQ, WRPN, [35]. Every "no accuracy loss" claim is inherited.
**Hidden cost of that inheritance.** AlexNet and ResNet-18 use WRPN's **2×-wide** models to hold 4-bit accuracy — **4× more multiply-adds** than the originals Eyeriss runs.

## 3. Optimization

**One mathematical line, applied recursively.** A multiply between power-of-2-bitwidth operands
decomposes into 2-bit multiplies recombined by shift-add: `A₂ₙ×B₂ₙ = 2²ⁿ(A)hi(B)hi + 2ⁿ(A)hi(B)lo
+ 2ⁿ(A)lo(B)hi + (A)lo(B)lo`, applied 16→8→4→2, with a separate form for unequal widths. **Each
recursion level costs a shift-add stage, and that logic is the entire price of bit-level
flexibility** — 934 of the Fusion Unit's 1394 µm², i.e. **67% of the unit is not multipliers**.

**Spatial fusion is the contribution, and Fig. 10 is where it is proved.** Bit-serial precision
flexibility already existed (Stripes, Tartan, Loom, UNPU). BitFusion's claim is that you should
compose 2-bit multipliers **spatially in one cycle** rather than **temporally over four**, and it
builds the control: an equivalent temporal design at 45 nm, deliberately made *stronger* than real
bit-serial by giving it 2-bit rather than 1-bit units. Result: **3.5× area, 3.2× power**. The
mechanism is specific — **16× of the saving is the register/accumulator** (1454 → 91 µm²), because
spatial fusion feeds a shift-add tree into **one shared accumulator** while the temporal design
needs a per-unit accumulator sized for the largest supported width. In a temporal 16-bit design
"the shifter and the accumulator use up around 90% of the area" — Fig. 10 confirms it at 90.6%.

**The systolic array pays for the extra BitBricks.** IBUFs feed rows from the borders, psums
accumulate down columns, pooling and activation sit per column. Each Fusion Unit carries **only a
WBUF** — no local input, output or psum buffers — and that reclaimed area is what buys more
BitBricks in the same budget. Buffers get a row register plus a multiplexer chain so one fetch can
be dispensed at any bitwidth.

**Fusion-ISA exists to make reconfiguration free.** Block-structured with iterative semantics, so
the cost of choosing a fusion configuration is amortised over a whole layer:
`setup` / `loop` / `compute` / `gen-addr`, addresses as `base + Σ loop_iterator[i]·stride[i]`.
This is why granularity is per-layer — and why the adoption barrier is high: a new ISA and a
compiler, not a drop-in datapath change.

**What it deliberately is not.** A mechanism paper wearing a quantization paper's clothes. It
chooses no bitwidths, handles no outliers, defines no memory format, and accounts for no metadata.
It takes a per-layer assignment someone else produced and executes it without waste.

## 4. Results

| | |
|---|---|
| Baseline | **Eyeriss** (16-bit, 168 PEs) and **Stripes** (bit-serial, 4096 SIPs/tile) — both re-simulated with their own authors' tools and scaled to 45 nm. Plus **Titan Xp** and **Jetson TX2** GPUs. Internal control: an equivalent **temporal** design the authors built |
| Models / datasets | 8 benchmarks: AlexNet, ResNet-18 (ImageNet); Cifar-10, VGG-7 (CIFAR-10); SVHN, LeNet-5 (OCR); LSTM, RNN (Penn TreeBank). **Six of eight are MNIST/CIFAR/SVHN/PTB scale** |
| Accuracy delta | **None claimed by this paper** — models and bitwidths taken unmodified from DoReFa-Net, TTQ, WRPN, [35], each reported lossless vs FP32 by its source |
| Speedup | **vs Eyeriss 3.9× geomean — but the range is 1.9× (AlexNet, ResNet-18) to 13× (Cifar-10)**. vs Stripes **2.6×**. vs TX2-FP32 **16×** at 16 nm |
| Energy / area | vs Eyeriss **5.1×**, vs Stripes **3.9×**. **Fusion Unit vs temporal: 3.5× area (4905→1394 µm²), 3.2× power (1712→538 nW), 16.0× on the accumulator alone (1454→91 µm²)**. 45 nm: 1.1 mm² compute / 5.87 mm² chip / 512 KB / 500 MHz. 16 nm: **5.93 mm², 895 mW** vs Titan Xp's **471 mm², 250 W** |
| Technology node | **45 nm synthesised**, plus an **analytically scaled 16 nm** point (0.86× V, 0.42× C, frequency deliberately not raised). Two nodes in one paper — a trap for aggregate tables |
| Evidence level | **Verilog + synthesis** (datapath) + **cycle-accurate simulation** verified against the RTL + **CACTI-P** (buffers) + **analytical node scaling** (16 nm). No silicon. Don't pool the 45 nm and 16 nm figures |
| **Is the comparison fair?** | Iso-area, iso-SRAM, iso-frequency; baselines re-simulated with their authors' own tools. **Not iso-workload** — AlexNet/ResNet-18 run 2×-wide WRPN models, **4× more MACs** than Eyeriss's. Don't quote "3.9× over Eyeriss" (range 1.9×–13×) or "almost matches Titan Xp" (geomean 16 vs 19; **6–7× slower** on both ImageNet models). Quote 895 mW vs 250 W, and 3.5×/3.2× over the temporal control |

## 5. Comment

## 6. Claude notes

> **Suggestions from the reading agent. Strip this section before copying into
> `QuantArchSurvey/venues/ISCA/notes/`.**

- **Venue is now verified.** Line 1 of the archived arXiv PDF reads *"Appears in the Proceedings of
  the 45th International Symposium on Computer Architecture (ISCA), 2018."* This was the **last**
  entry `survey/README.md` listed as having an unverified venue — that note can be retired
  entirely (Oaken was cleared earlier).
- **Seed-tag suggestions (I did not edit the file).** Add **`INT16`** to the data-type cell — the
  recursion in §III-A explicitly reaches 16-bit operands and the current cell stops at INT8. Add
  **`spatial fusion`** and **`shared accumulator`** to the optimization keywords: they are the
  actual mechanism, and "bit-flexible MAC" alone does not distinguish this from Stripes. `ARCH`,
  `Q`, `G2` all stand.
- **§5 material, if you want it.** `G2` is unusually clean here and worth one sentence: the G2
  paradigm is *make the datapath match the bitwidth*, G3's is *give the tail its own format*.
  BitFusion is the purest statement of the former — a datapath with **no opinion at all** about
  what the numbers mean. Contrast OLAccel, published the same year and `G3`.
- **This is the best citation in the corpus for "why spatial beat bit-serial."** 3.5× area, 3.2×
  power, and the decomposition says exactly where: **16× in the accumulator**, because spatial
  fusion shares one where temporal needs one per unit sized for the maximum width. That is a
  reusable architectural argument, not just a result.
- **A reversal worth a line when DRQ and BitFusion appear together.** DRQ credits its PE to
  BitFusion — but DRQ's PE goes back to **time-multiplexing over four cycles**, which is precisely
  the temporal design Fig. 10 shows losing 3.5×/3.2×. DRQ never addresses this, and its abstract
  also silently drops BitFusion as a baseline (the +83%/−49% figures appear only in DRQ §VI-A).
- **The granularity axis starts here.** BitFusion per-layer (2018) → DRQ per-region (2020) →
  Tender per-channel band (2024) → Oaken/MicroScopiQ per-group (2025). BitFusion is also the entry
  that shows the *hardware* reason coarse was chosen: the ISA exists to amortise reconfiguration,
  so finer switching is not free in this design family.
- **Numbers I would exclude from any cross-paper table.** The 16 nm figures — they are
  analytically scaled from a 45 nm synthesis, not resynthesised, and BitFusion is the only entry
  so far carrying two nodes. Also the 3.9×/5.1× Eyeriss geomeans unless the workload asymmetry
  travels with them.
- **WRPN is load-bearing and outside the corpus.** The 2×-wide models are the whole reason the
  ImageNet speedups are 1.9× rather than ~7.6×. Alongside ANT (six entries) and GOBO (three), it
  belongs on the list of non-ISCA references the survey cannot avoid citing.
