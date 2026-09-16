# DRQ: Dynamic Region-based Quantization for Deep Neural Network Acceleration

**Venue / Year:** ISCA 2020 · **Link:** https://doi.org/10.1109/ISCA45697.2020.00086 (no arXiv) · **Reader:** Haoxuan · **Date:** 2026-09-09

## Tags

| | |
|---|---|
| **Level** | `ALGO+ARCH` |
| **Q-oriented** | `Q-ORIENTED` |
| **Data type** | `INT4` `INT8` `MIXED` |
| **Generation** | `G2` |
| **Optimization** | region-wise granularity · dynamic/runtime precision selection · mean-filter sensitivity predictor · binary mask map · variable-speed systolic array · time-multiplexed multi-precision PE · predictor fused into pooling · QAT |

## 1. One-line summary

Predicts **at runtime, one layer ahead**, which *spatial regions* of an activation map are
accuracy-critical — mean-filter the pooled output, threshold it into a binary mask — and runs
**INT8 over those regions, INT4 everywhere else** on a variable-speed systolic array whose PEs
time-multiplex four INT4 cycles into an INT8 MAC and **stall their whole column** while doing it:
**+92% performance, −72% energy** over Eyeriss at iso-MAC-area, at the cost of a per-network
**retraining** and hyperparameter loop the abstract never mentions.

## 2. Data type

**Two precisions, no new format.** INT8 = high, INT4 = low. Both operands switch together — a sensitive region is W8A8, an insensitive one W4A4. **No W8A4.**
**Granularity: a spatial region of the input feature map.** Unique in the corpus — everyone else picks a tensor axis (channel, token, group) or a magnitude class. Region sizes per network: **2×4 · 2×4 · 4×16 · 4×8 · 4×8 · 2×4**, shrinking with depth, fixed **2×2** in the last conv layers.
**Chosen per image, at runtime.** Mean-filter each region, compare to a per-layer threshold → 1 bit per region **per input channel**. ResNet-18 threshold **0.025**.
**Weights: INT8 in DRAM, always.** Clipped to INT4 only inside the PE. **No weight compression anywhere in the hierarchy** — DRQ concedes this costs it more DRAM energy than OLAccel.
**Activations:** stored INT8 or INT4 by mask bit. The only real memory saving.
**Outliers.** No outlier format at all. Sensitivity is *geometric*, not magnitude-based — this is what makes it `G2` and not `G3`.
**Accumulator.** **16-bit** psum register per PE. Narrower than OLAccel's 24-bit, while claiming better accuracy.
**Escape hatch.** No layer exempt by rule, but ResNet-18's first block runs **12% of cycles in INT8** (highest of any block), and the permanent INT8 weight store is itself an escape hatch.
**Retraining.** **QAT, required** — mixed-precision forward, full-precision backward, repeated to convergence, **once per (network, threshold, region-size) trial**. Stated only in §III-D; absent from abstract, contributions, results and conclusion. Cost never reported.

## 3. Optimization

**The claim is about *when* you decide, not *what* you keep.** §II earns it in two steps: inject
noise into the top-20% / middle-60% / bottom-20% of activations and only the top segment moves
accuracy (the "TFF" curve collapses, "FFT" barely moves); then show those values **aggregate
spatially** rather than scattering. The first half is OLAccel's observation restated; the second
half is the novelty, and it is the one thing in this paper nobody else in the corpus proposes.

**The predictor is cheap and genuinely elegant.** Sensitivity prediction *is* a mean filter — a
dot product with an all-ones x×y kernel — and the current layer's pooling output *is* the next
layer's input, so the pooling adders already compute the mean-filter partial sums. The pipeline
stage becomes "activation-pooling-**prediction**". Pooling and prediction scan in different orders,
so partials are held in a temporal buffer sized `w/y + (w/n)(x/n−1)` — which is why **stripe-shaped
regions win** (large y, small x). Total: **~2 KB on ResNet-18**. For a runtime, per-image,
per-region decision that is close to free.

**The PE is BitFusion's, and DRQ says so.** Two 8-bit registers W and F, a 16-bit P. Default INT4,
one MAC/cycle. INT8 = **four cycles** of the same INT4 MAC over the nibble products with a `<<4`
between accumulations.

**The variable-speed array is where it actually costs.** A systolic column must stay synchronised
for the partial-sum shift, so **any PE receiving an INT8 value switches the whole column to INT8**,
and the INT4 PEs in that column **stall 3 cycles**; the stall signal then shifts right one column
per cycle. **The unit of cost is the column, not the value** — one sensitive value in a 4-PE column
costs the same as four. This is why the design-space sweep has a "stall ratio" axis at all, and
why the threshold is tuned against it.

**What the hardware buys — and the part that does not hold.** At iso-MAC-area DRQ fields 3168
INT4 MACs against its OLAccel model's 2499 (**+26.8%**) and reports a **21% speedup**, which §VI-A
attributes exactly that way: "thanks to the larger number of PEs under the same area budget."
There is **no DRQ-with-a-static-threshold ablation**, so the paper's actual architectural claim —
that dynamic beats static selection — is never isolated by any experiment.

## 4. Results

| | |
|---|---|
| Baseline | **Eyeriss** (INT16), **BitFusion**, **OLAccel** — all re-modelled by DRQ at its own node, which is the right call. OLAccel reproduced by DRQ for 5 of 6 networks (only AlexNet is quoted from the original) |
| Models / datasets | AlexNet, VGG16, ResNet-18, ResNet-50, Inception-v3, MobileNet-v2 on **CIFAR-10 and ILSVRC-2012**. **The paper never says top-1 or top-5** |
| Accuracy delta | Avg loss vs Eyeriss/BitFusion — **CIFAR-10: DRQ 0.3% · OLAccel 1.6%**; **ILSVRC-2012: DRQ 0.8% · OLAccel 4.3%**. Per-network: Inception-v3 **0.7% vs 5.1%**, MobileNet-v2 **0.9% vs 5.4%**, ResNet-50/ILSVRC 0.9% loss |
| Speedup | Avg **+92% vs Eyeriss · +83% vs BitFusion · +21% vs OLAccel**. ResNet-50: +93% / +73% / +20% |
| Energy / area | Avg **−72% / −49% / −33%**. Iso-area **0.32 mm² of MAC**, 45 nm: Eyeriss 224 INT16 · BitFusion 3168 INT4 · **OLAccel 2499 (2448 INT4 + 51 INT16)** · **DRQ 3168 INT4**. Predictor +2 KB |
| Technology node | **TSMC 45 nm**, 500 MHz, DDR3, 5 MB shared global buffer |
| Evidence level | **Cycle-accurate simulator** (masks + feature maps dumped from TensorFlow) + **CACTI 5.1** + an **analytical MAC-area table** (INT4 100.5 / INT8 377.5 / INT16 1423 µm²). **No Verilog, no synthesis, no PnR** — weaker than OLAccel's Design Compiler flow |
| **Is the comparison fair?** | Iso-MAC-area, iso-buffer, baselines re-modelled at 45 nm. **Not iso-training** (DRQ QAT vs OLAccel PTQ), **not iso-costed** (multi-precision PE priced as plain INT4; predictor/mask/im2col/stall network outside the budget; nothing synthesised), **not iso-MAC-count** (3168 vs 2499). Don't quote "3% accuracy" or "21% over OLAccel" — the latter ≈ the +26.8% MAC ratio |

## 5. Comment

## 6. Claude notes

> **Suggestions from the reading agent. Strip this section before copying into
> `QuantArchSurvey/venues/ISCA/notes/`.**

- **No disagreement with the seed row on any axis** — `ALGO+ARCH` `Q` `INT4` `INT8` `MIXED` `G2`
  all stand after the close read.
- **§5 material, if you want it.** The `G2` is worth one sentence of defence, because DRQ sits
  *between* two `G3` papers by date. The distinction that holds: `OLAccel` separates the tail into
  **its own format** (that is the G3 paradigm); DRQ separates a **region** and keeps both halves
  plain INT. A precision switch is not a number representation.
- **This is the paper's best citation, and it is not the headline.** §II-A's noise-injection
  experiment + §II-B's LeNet-5 visualisation are the corpus's only direct evidence that
  **activation sensitivity is spatially clustered**. Cite it for that, not for "fine-grained
  quantization."
- **The static-vs-dynamic axis is now worth naming in the survey.** OLAccel'18 design-time →
  **DRQ'20 runtime, per image** → and then *everything* after reverts to design-time (OliVe,
  Tender, MicroScopiQ, OASIS), with Oaken the only partial exception. DRQ's own numbers explain
  why: the runtime path costs a predictor, a mask buffer, a stall network **and** a retraining
  loop, and its measured win over the static competitor is indistinguishable from a MAC-count
  difference. That is a much better paragraph than "granularity got finer over time."
- **The retraining requirement is the single most important thing this read turned up.** It is in
  §III-D and nowhere else — not the abstract, not the contributions, not §VI, not the conclusion.
  Every accuracy comparison in the paper is **QAT against PTQ baselines**. If we cite DRQ's
  accuracy advantage over OLAccel anywhere, that sentence has to carry this.
- **DRQ's own model of OLAccel contradicts itself across three places** — Table I credits it with
  value-wise 4/8-bit granularity (correct); Table II budgets 2448 INT4 + 51 INT16 MACs (consistent
  with an outlier path); but §VI-A and §VII-A4 describe it as "16-bit MAC for the first layer,
  4-bit for the rest", which drops the outlier mechanism entirely. Since OLAccel's own paper shows
  4-bit-without-outliers collapsing 76.57% on AlexNet, the prose cannot be what was simulated —
  but the reader cannot tell what was. Worth one line if we ever put DRQ's OLAccel numbers in a
  table.
- **I corrected the OLAccel entry because of this read.** I had "corrected" our old brief's claim
  that DRQ reports OLAccel losing ~5% on MobileNet-v2. The brief was right — DRQ reports **5.4%**
  there and 5.1% on Inception-v3. `OLAccel/ANALYSIS.md` and its note now say so.
- **A number I would exclude from any cross-paper table:** DRQ's area figures. 0.32 mm² is a
  *MAC-only* budget from a lookup table, not a synthesised design, and it is not comparable to
  OLAccel's 1.67 mm² post-synthesis whole-accelerator figure even before the node difference.
- **DRQ pulls `BitFusion` into this thread** — its PE, its MAC budget, and the baseline the
  abstract silently drops (+83% perf / −49% energy appear only in §VI-A). Worth remembering when
  BitFusion's own entry comes up; it is BitFusion's most direct architectural descendant here.
