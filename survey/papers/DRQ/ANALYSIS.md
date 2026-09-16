# DRQ — paper notes

**DRQ: Dynamic Region-Based Quantization for Deep Neural Network Acceleration**
Zhuoran Song, Bangqi Fu, Feiyang Wu, Zhaoming Jiang, Li Jiang, Naifeng Jing, Xiaoyao Liang
**ISCA 2020**, pp. 1010-1021 ｜ DOI: **10.1109/ISCA45697.2020.00086**
Publication info verified 2026-09-02: venue, year **and DOI** all read out of the archived
PDF's own text (IEEE proceedings banner; the DOI was grepped for, not assumed); page range
from the ACM DL record.
Archived here: the **published IEEE version** (the page-1 IEEE proceedings banner is present in the extracted text), 12 pages.

Status: **note ready** ｜ Last updated: 2026-09-09
Tags: `analytical-dtype` `mixed-precision` `dtype-granularity` `multi-bitwidth-hw` `accelerator`
How far it was read: **full close read of all eight sections** (pp. 1010-1021). §II (sensitivity
study), §III (algorithm), §IV-A-E (architecture), §V (methodology) and §VI (results) were read
line by line, including Tables I-III and every figure caption; §VII (related work) and §VIII
(conclusion) read in full. Figures 11-16 are bitmaps in the extraction, so **all figure numbers
below come from the paper's own prose**, not from reading the plots. Read immediately after
[`OLAccel`](../OLAccel/ANALYSIS.md), which this paper exists to attack.
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> Publisher record: https://dl.acm.org/doi/10.1109/ISCA45697.2020.00086
> **There is no arXiv version** (arXiv API title search, 2026-09-02). The PDF was downloaded by a
> human and filed through [`survey/uploads/`](../../uploads/) — the sanctioned route when the
> arXiv-only rule leaves a paper unreachable; see
> [`Notes-002`](../../../Claude/notes/Notes-002-paper-source-access.md).
> The PDF is **not committed** (0.4 MB) and **cannot be re-downloaded by script** —
> both publishers 403. Re-extract with `python3 extract.py` → `extracted/` (committed).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, ISCA 2020 row.

---

## Brief

### 1. Motivation

Quantization applied at network or layer level is too coarse to exploit; applied to weights
only, it ignores that the *input feature map* varies in how much precision it needs. The
paper's finding is that accuracy-critical ("sensitive") values are not scattered — they
**cluster into contiguous regions**.

### 2. Overview

A dynamic, region-based scheme: an algorithm identifies sensitive regions in each input
feature map at runtime and assigns higher precision (INT8) there and lower (INT4) elsewhere,
executed by a **variable-speed mixed-precision convolution array** sized so both precisions
keep the array busy. Threshold and region size are tuned by design-space exploration (e.g.
4×16 regions, threshold 0.025).

### 3. Pros and cons

**Pros**

- Introduces a granularity nobody had used — **spatial regions of the activation map** — and
shows it is the right one, since sensitivity is spatially clustered.
- Beats its two natural competitors on both axes at similar area: 92%/72% performance/energy
over Eyeriss, and 21%/33% over [`OLAccel`](../OLAccel/ANALYSIS.md) **with 3% better
accuracy**.
- Metadata cost is honestly reported and genuinely small (~2 KB for ResNet-18).

**Cons**

- Region detection runs online, so its cost and the pipeline stalls it causes are intrinsic;
the paper reports a stall ratio and tunes around it rather than eliminating it.
- CNN-shaped throughout — the array prioritizes 3×3 kernels, and "regions of a feature map"
has no direct analogue in transformer activations.
- Threshold and region size are hyperparameters swept per network; no automatic selection is
offered.

### 4. Where it applies

The best example in the corpus of **granularity as the contribution** (§2.2 fine-grained).
Pair with [`Tender`](../Tender/ANALYSIS.md) and [`LightNobel`](../LightNobel/ANALYSIS.md),
which pick channel- and token-wise granularity for the same reason.

---

## Corrections to the brief

The brief was substantially right about *what* DRQ does. Three things it missed, all of which
change how the paper should be cited:

1. **DRQ requires retraining. The brief implied otherwise by silence.** §III-D: "we need to
   **retrain** the predefined NN model and **fine-tune the weights** so that they can be aware of
   the sensitivity information in the feature maps … we retrain the model for guaranteed accuracy,
   during which we will apply the mix-precision convolution in the forward propagation, but
   full-precision backward propagation" **verified**. This is QAT with a straight-through-style
   backward pass, and it is **inside the tuning loop** — threshold and region size are found by
   repeatedly retraining. Its headline comparison is therefore **QAT against
   [`OLAccel`](../OLAccel/ANALYSIS.md)'s explicitly retraining-free PTQ**, and neither the abstract
   nor §VI says so.
2. **The stall is column-wide, not value-wide.** The brief called region detection the intrinsic
   cost. The larger cost is in §IV-C2: when any PE in a column receives a sensitive (INT8) value,
   **every other PE in that column stalls three cycles** so the systolic array stays synchronised,
   and the stall signal shifts to the next column. One sensitive value costs 4× on a whole column.
   This is why the design-space sweep has a "stall ratio" axis at all.
3. **Weights are never stored below INT8.** §III-C: "we **always** store the kernel weights in
   INT8 format in the DRAM", clipped to INT4 only inside the PE **verified**. So DRQ gets no weight
   traffic reduction, and §VI-A concedes it therefore burns **more DRAM energy than OLAccel**.
   Only the activation side is genuinely compressed.

---

## Conclusions

**The contribution is a granularity nobody else in the corpus proposes: a spatial region of the
activation map.** Every other entry quantizes along a tensor axis — per-tensor, per-channel
(`Tender`), per-token (`LightNobel`), per-group (`Oaken`, `MicroScopiQ`) — or along magnitude
(`OLAccel`, `OliVe`). DRQ quantizes along **image geometry**, and §II earns the right to: it
shows first that the largest 20% of activations dominate accuracy under injected noise (Fig. 2's
"TFF" curve collapses while "FFT" barely moves), then that those values **aggregate spatially**
rather than scattering (Fig. 3, LeNet-5 on MNIST). The second half is the actual novelty; the
first half is OLAccel's observation restated.

**Its real claim is about *when* you decide, not *what* you keep.** OLAccel fixes a per-layer
threshold at design time from 100 images. DRQ computes a mask **per image, at runtime**, fused
into the pooling unit, one layer ahead. That is the axis this paper opens, and it is the one
the survey should cite it for — not "fine-grained quantization", which several other entries do
better.

**The mechanism is cheap and genuinely elegant.** Sensitivity prediction is a mean filter — a
dot product with an all-ones x×y kernel — thresholded into a binary mask. Because the current
layer's pooling output *is* the next layer's input, the predictor reuses the pooling adders and
costs ~2 KB of extra buffering on ResNet-18. For a runtime, per-image, per-region decision that
is close to free.

**But the evaluation does not support the headline.** Three things stack in the same direction:
DRQ retrains and its baselines do not; DRQ's PE is charged the area of a plain INT4 MAC while
its multi-precision capability is free in the model; and DRQ gets 3168 MACs against its OLAccel
model's 2499, then reports a **21% speedup** — which is within rounding distance of the 26.8%
MAC-count ratio. The paper says so itself: "DRQ can achieve 20% performance improvement **thanks
to the larger number of PEs under the same area budget**." The honest reading is that the
performance result is a MAC-density result and the accuracy result is a retraining result.

**The accuracy gap against OLAccel is the number to be most careful with.** DRQ's reproduction of
OLAccel loses **4.3% on average on ILSVRC-2012**; OLAccel's own paper reports **<1% top-5** on the
three CNNs it evaluated. DRQ never mentions the discrepancy, never states whether its "accuracy"
is top-1 or top-5, and two of its six networks (Inception-v3, MobileNet-v2) are ones OLAccel never
tried. All of that can be true and DRQ can still be right that OLAccel degrades on compact
models — but the 4.3% is not comparable to OLAccel's <1%.

---

## Method

**The format.** Two precisions, INT8 and INT4, chosen per **spatial region of the input feature
map**, per image, at runtime.

- **Weights**: stored **INT8 in DRAM, always**. Clipped to INT4 inside the PE when the kernel
  sits over an insensitive region. No weight compression at any level of the hierarchy.
- **Activations**: stored **INT8 or INT4 depending on the region's mask bit** — this is the only
  place DRQ actually saves memory.
- **Partial sums: 16-bit** (§IV-C1: "A 16-bit register P store the partial result") **verified**.
  Compare `OLAccel`'s 24-bit — DRQ is 8 bits narrower on the accumulator while claiming better
  accuracy.
- Both operands switch together: a sensitive region gets INT8 weights **and** INT8 activations
  (§III-C, Fig. 5, Case 1); an insensitive region gets INT4 both (Case 2). There is no W8A4.

**Sensitivity prediction** (§III-B, §IV-E) **verified**. Quantize the feature map FP32→INT8;
partition into x×y regions; **dot-product each region with an all-ones kernel — i.e. a mean
filter**; compare against a per-layer threshold (a step activation); emit a binary mask of
dimension `h·w/(x·y)`, **per input channel**. A `1` marks a sensitive region.

The implementation trick is that the predictor is **fused into the pooling unit**: the current
layer's pooled output is the next layer's input, so for a x×y prediction window containing n×n
pooling windows, the pooling partial sums are *already* the mean-filter partial sums. §IV-E
extends the usual "activation-pooling" pipeline stage to "**activation-pooling-prediction**".
Pooling and prediction scan in different orders (Fig. 10), so partial results are held in a
temporal buffer: `w/y` partial predictions + `(w/n)·(x/n − 1)` pooling results, where `w` is the
feature-map width. **This is why stripe-shaped regions win** — large `y`, small `x` minimises
that buffer. **2 KB on ResNet-18 at 4×16** **verified**.

**Multi-precision PE** (§IV-C1, Fig. 8). Two 8-bit registers `W` and `F`, a **16-bit** `P`. Default
mode is INT4, one MAC per cycle. INT8 mode is **four cycles of the same INT4 MAC**, time-
multiplexed over the nibble products (`W_H·F_H`, `W_L·F_H`, `W_H·F_L`, `W_L·F_L`) with a `<<4`
between accumulations. DRQ credits this PE to `BitFusion` [29] rather than claiming it.
**Inferred / not verified:** the shift pattern in Fig. 8 is a Horner-style `P = (P<<4) + product`;
the paper describes cycles t and t+1 only and does not write the recurrence out.

**Variable-speed systolic array** (§IV-C2-3, Fig. 7b) — the part that costs. A column of PEs must
stay synchronised for the systolic partial-sum shift, so:

- Any PE in a column receiving an INT8 value **switches the whole column to INT8 mode**.
- INT8 PEs take 4 cycles; the INT4 PEs **in that same column stall for 3**.
- The stall signal shifts right one column per cycle, so the wave propagates across the array.

So the unit of cost is the **column**, not the value: one sensitive value in a 4-PE column costs
the same as four. §VI-B1's "stall ratio" axis exists to tune this down, and the threshold is
chosen by balancing 4-bit percentage against stall ratio against accuracy.

**Data path.** Global buffer → `im2col`/pack engine → line buffer (**densely packed**: insensitive
values in 4-bit registers, sensitive in 8-bit, with the mask deciding) → variable-speed array →
accumulation unit → output buffer (double-buffered) → activation/pooling/**prediction** → mask
buffer + global buffer. Weight-stationary by preference, because "the storage overhead of weights
is larger than input values". 3×3 kernels are prioritised; 5×5 and 7×7 are split into sub-kernels
and recombined in the accumulation unit.

**Tuning loop** (§III-D). Start from a large threshold and region size → **retrain** with
mixed-precision forward and full-precision backward → evaluate → if accuracy misses, **halve the
region size or the threshold** and repeat. Per network. Region size also **shrinks with depth**,
fixed at 2×2 for the last few conv layers, and the threshold becomes "5× smaller in the last few
layers".

---

## Key numbers, with their frame

Evidence level: **cycle-accurate simulator** (feature maps and binary masks dumped from
TensorFlow, replayed) + **CACTI 5.1** for buffers + an **analytical MAC-area table** (INT4 100.5,
INT8 377.5, INT16 1423 µm², TSMC 45 nm). **No Verilog, no synthesis, no PnR** — weaker than
`OLAccel`'s Design Compiler flow, which matters because DRQ's own control logic, predictor and
im2col engine are never synthesised. 500 MHz, DDR3, **iso-area at 0.32 mm² of MAC** with a shared
5 MB global buffer. Accuracy is from TensorFlow. **The paper never states top-1 or top-5.**

| Setting | Model | Metric | Baseline | Result | Source |
|---|---|---|---|---|---|
| Headline, averaged over 6 networks | AlexNet, VGG16, ResNet-18/50, Inception-v3, MobileNet-v2 | performance | **Eyeriss** (INT16) | **+92%** | §VI-A **verified** |
| " | " | performance | **BitFusion** | **+83%** | §VI-A **verified** (abstract omits this) |
| " | " | performance | **OLAccel** | **+21%** | §VI-A **verified** |
| " | " | energy | Eyeriss / BitFusion / OLAccel | **−72% / −49% / −33%** | §VI-A **verified** |
| " | " | accuracy improvement | OLAccel | **+3.3%** | §VI-A **verified — but not reconstructible, see below** |
| Accuracy loss, average | 6 networks, **CIFAR-10** | acc. loss vs Eyeriss/BitFusion | — | **DRQ 0.3% · OLAccel 1.6%** | §VI-A, Fig. 13 **verified** |
| Accuracy loss, average | 6 networks, **ILSVRC-2012** | acc. loss vs Eyeriss/BitFusion | — | **DRQ 0.8% · OLAccel 4.3%** | §VI-A, Fig. 13 **verified** |
| Per-network accuracy | **Inception-v3** | acc. loss, ~90% of ops 4-bit | — | **DRQ 0.7% · OLAccel 5.1%** | §VI-A **verified** |
| Per-network accuracy | **MobileNet-v2** | acc. loss, 85% of ops 4-bit | — | **DRQ 0.9% · OLAccel 5.4%** | §VI-A **verified** |
| Per-network | **ResNet-50 / ILSVRC-2012** | acc. loss / margin | Eyeriss, BitFusion / OLAccel | **0.9% loss / +5.1% over OLAccel** | §VI-A **verified** |
| Per-network perf | **ResNet-50** | performance | Eyeriss / BitFusion / OLAccel | **+93% / +73% / +20%** | §VI-A **verified** |
| Per-network energy | **ResNet-50** | energy | Eyeriss / BitFusion / OLAccel | **−72% / −43% / −32%** | §VI-A **verified** |
| Iso-area configs | — | # MACs at 0.32 mm², 45 nm | Eyeriss 224 INT16 · BitFusion 3168 INT4 · **OLAccel 2499 (2448 INT4 + 51 INT16)** | **DRQ 3168 INT4** | Table II **verified** |
| **MAC-count ratio vs OLAccel** | — | INT4 MACs | 2448 | **3168 = +29.4%** (2499 total → **+26.8%**) | derived from Table II — **compare with the 21% speedup** |
| Predictor storage | ResNet-18 @ 4×16 regions | extra on-chip buffer | — | **~2 KB** ("negligible") | §IV-E **verified** |
| Chosen hyperparameters | ResNet-18 | threshold / region | swept 0.001-1 | **0.025 / 4×16** | §VI-B1-2 **verified** |
| Per-network hyperparameters | AlexNet, VGG16, ResNet-18, ResNet-50, Inception-v3, MobileNet | region size / avg integer threshold | — | **2×4/18, 2×4/17, 4×16/21, 4×8/19, 4×8/23, 2×4/25** | Table III **verified** |
| Cycle breakdown | ResNet-18 | INT8 share of cycles, first block (C1) | other blocks lower | **12%** | §VI-C **verified** |
| Weight-reload stall | ResNet-18, last block (B4) | share of cycles | negligible elsewhere | **~4%** | §VI-C **verified** |

**"+3.3% accuracy improvement" is not derivable from the paper's own averages.** Fig. 13 gives
1.6−0.3 = **1.3 points on CIFAR-10** and 4.3−0.8 = **3.5 points on ILSVRC-2012**; the mean of
those is 2.4, not 3.3. The abstract rounds it further, to "3%". **Quote 1.3% / 3.5% per dataset,
never the 3%.**

---

## Cost and requirements

| | |
|---|---|
| **Retraining** | **Required — QAT.** Mixed-precision forward, full-precision backward, repeated until convergence, **once per (network, threshold, region size) trial**. Epochs, time and dataset are **never reported** |
| **Hyperparameter search** | Threshold **and** region size, per network, by trial-and-error halving (§III-D); region size additionally shrinks with depth (fixed 2×2 in late layers), threshold "5× smaller in the last few layers" |
| **Predictor** | Mean filter fused into the pooling unit; ~2 KB temporal buffer on ResNet-18 @4×16. Genuinely cheap. **Not synthesised** |
| **Mask storage** | 1 bit per region **per input channel**, in a dedicated mask buffer, written a layer ahead |
| **Stalls** | **3 cycles for every INT4 PE sharing a column with an INT8 PE.** Cost granularity is the column, not the value |
| **Accumulator** | **16-bit** psum register per PE — narrower than OLAccel's 24-bit |
| **PE overhead** | Multi-precision MAC (credited to BitFusion). **The area model charges it as a plain INT4 MAC at 100.5 µm²** — the shift/control/16-bit-P overhead is not costed |
| **Weight memory** | **No saving at all** — INT8 in DRAM always. DRQ concedes it uses **more DRAM energy than OLAccel** for this reason |
| **Escape hatch** | No layer is exempt by rule, but ResNet-18's first block runs **12% of its cycles in INT8**, the highest of any block. Weights never go below INT8 in memory, which is itself a permanent escape hatch |
| **Shape assumptions** | Prioritises 3×3 kernels; assumes a pooling stage exists to fuse the predictor into (§IV-E gives a fallback when it does not, keeping the adders live) |

---

## Limitations and open questions

**Admitted.**

- Stalls are intrinsic and are tuned around, not removed (§VI-B1's stall-ratio axis).
- Threshold and region size are per-network hyperparameters with no automatic selection.
- **More DRAM energy than OLAccel**, because weights stay INT8 (§VI-A) — a rare concession.
- Region size must be rescaled by depth by hand.

**Unadmitted, and material.**

- **The retraining requirement is never surfaced outside §III-D.** It is absent from the abstract,
  the contributions list, §VI and the conclusion. Every accuracy comparison in the paper is QAT
  against PTQ baselines, and no reader of the abstract would know.
- **The area model is asymmetric.** OLAccel is charged 1423 µm² for each of its 51 INT16 MACs;
  DRQ's multi-precision PE is charged 100.5 µm², the price of a plain INT4 MAC. `BitFusion`, whose
  PE design DRQ borrows, is charged the same. The predictor, mask buffer, im2col engine, packing
  logic and stall-control network are **outside the 0.32 mm² budget entirely** — nothing was
  synthesised.
- **The 21% speedup over OLAccel is ≈ the MAC-count ratio** (3168 vs 2499, +26.8%), and §VI-A
  attributes it exactly that way: "thanks to the larger number of PEs under the same area budget."
  DRQ's actual architectural claim — that dynamic region selection beats static thresholds — is
  **not isolated by any experiment**. There is no DRQ-with-a-static-threshold ablation.
- **DRQ's own model of OLAccel contradicts itself across three places.** Table I credits OLAccel
  with value-wise granularity at 4/8 bit (correct). Table II budgets it 2448 INT4 + 51 INT16
  MACs (consistent with an outlier path). But §VI-A and §VII-A4 describe it as "**16-bit MAC for
  the first layer, 4-bit MAC for the rest**" — which drops the outlier mechanism entirely. Given
  that OLAccel's own paper shows 4-bit-with-no-outliers collapsing by 76.57% top-5 on AlexNet, the
  prose description cannot be what was simulated; but the reader cannot tell what *was*.
- **4.3% average loss for OLAccel on ILSVRC-2012 vs OLAccel's own <1% top-5** is a 4× gap that
  DRQ never mentions. Possible legitimate explanations — top-1 vs top-5, two networks OLAccel
  never tried, no per-network outlier-ratio tuning — are all unstated.
- **No metric is named anywhere.** "Accuracy" appears ~30 times; "top-1" and "top-5" appear zero
  times **verified by grep**.
- **CIFAR-10 accuracy is load-bearing but weak evidence.** Half the accuracy claims are CIFAR-10,
  where the OLAccel gap is 1.3 points, not 3.5.
- **CNN-shaped throughout.** "Regions of a feature map" has no analogue in transformer activations
  — there is no spatial adjacency in a token×channel matrix in the sense §II relies on. The
  channel-wise and token-wise entries in this corpus are the transformer-era answer to the same
  question.

---

## Relation to other entries

**DRQ is the corpus's one sustained argument for *dynamic* outlier/sensitivity identification,
and it lost.** This is the axis worth naming in the survey, seeded in
[`OLAccel`](../OLAccel/ANALYSIS.md)'s analysis and confirmed here:

| Paper | When is the high-precision set chosen | Basis |
|---|---|---|
| `OLAccel` (ISCA'18) | **design time** — per-layer threshold from 100 images | magnitude |
| **`DRQ` (ISCA'20)** | **runtime, per image, one layer ahead** | mean-filtered spatial region |
| `OliVe` (ISCA'23) | design time | magnitude, adjacency-paired |
| `Tender` (ISCA'24) | design time (channel bands) | channel range |
| `Oaken` (ISCA'25) | **hybrid** — offline thresholds, online group selection | magnitude |
| `MicroScopiQ` (ISCA'25) | design time | Hessian importance |
| `OASIS` (ISCA'26) | design time | — |

Everything after 2020 reverts to design-time selection, with `Oaken` the only partial exception.
**The survey should say why**: DRQ's own numbers show the runtime path costs a per-image
predictor, a mask buffer, a stall network *and* a retraining loop, and its measured win over the
static-threshold competitor is indistinguishable from a MAC-count difference. That is a cleaner
story than "fine-grained quantization is good."

**On the granularity axis it is genuinely unique — and that is its best citation.** Group it with
`Tender` (per-channel bands) and `LightNobel` (per-token) as "granularity is the contribution",
but note that DRQ's axis is **spatial**, not tensorial, and that this is exactly why it did not
survive the transformer transition. It is the best citation in the corpus for *"activation
sensitivity is spatially clustered, and here is the noise-injection experiment that shows it"*
(§II-A Fig. 2, §II-B Fig. 3).

**Direct lineage.** DRQ → `OLAccel` is an attack (see above). `OliVe` §2.2 cites DRQ as the
bitmap-encoding member of its unaligned-outlier table: "DRQ's bitmap is **aligned**, but data is
stored by mixed and thus unaligned 4- & 8-bit values" — a fair reading of §IV-B's dense packing.
`Tender` §II groups DRQ with OLAccel and GOBO as mixed-precision designs "requiring complex
hardware and unaligned memory access". Both criticisms land on the *packing*, not on the
prediction, which suggests the field never really engaged with DRQ's actual idea.

**It also imports `BitFusion` into the outlier thread.** DRQ's PE is BitFusion's, its MAC budget
is BitFusion's, and BitFusion is the baseline the abstract silently drops (the +83% performance /
−49% energy figures appear only in §VI-A). When `BitFusion`'s own entry is read, note that DRQ is
its most direct architectural descendant in this corpus.

**Node hazard.** DRQ is **TSMC 45 nm** analytically modelled, `OLAccel` **65 nm** post-synthesis.
The two are compared *inside DRQ* at 45 nm — DRQ re-models OLAccel at its own node rather than
quoting OLAccel's numbers, which is the right call and worth crediting. The corpus range is now
7 nm (`MicroScopiQ`, `Omni-LUT`) → 65 nm (`OLAccel`).

**Outside-corpus references DRQ makes load-bearing:** `Eyeriss` (ISCA'16) and `BitFusion`
(ISCA'18, in-corpus) as baselines, and ref [27] — Park et al.'s weighted-entropy quantization,
the same group as OLAccel — which §VII-B3 correctly identifies as the intra-layer ancestor of
both.

---

## For the note

**§1 one-line summary.** DRQ predicts, at runtime and one layer ahead, which **spatial regions**
of an activation map are accuracy-critical — by mean-filtering the pooled output and thresholding
it into a binary mask — and runs INT8 over those regions and INT4 everywhere else on a
variable-speed systolic array whose PEs time-multiplex four INT4 cycles into an INT8 MAC and stall
their whole column while doing it, buying +92% performance and −72% energy over Eyeriss at iso-MAC-
area, at the cost of a per-network retraining and hyperparameter loop that the abstract does not
mention.

**Proposed tags — no disagreement with the seed row on any of the four axes.**

| Axis | Value | Evidence |
|---|---|---|
| **Level** | `ALGO+ARCH` | Genuine co-design: §II-III are an algorithm (sensitivity study, mean-filter predictor, retraining loop), §IV is an accelerator, and neither works alone. Seed agrees (revised to `ALGO+ARCH` in the 2026-09-03 log) |
| **Q-oriented** | `Q-ORIENTED` | Swap the format for plain INT8 and the mask buffer, the variable-speed stall network, the multi-precision PE and the predictor all lose their purpose |
| **Data type** | `INT4` `INT8` `MIXED` | INT8/INT4 both operands, switched per region **verified** §III-C; 16-bit psum |
| **Generation** | `G2` | Seed agrees. Correct on paradigm, not just year: the mechanism is a **precision switch**, not a new number representation, and there is no outlier *format*. Contrast `OLAccel` two years earlier, which is `G3` because separating the tail into its own format **is** the G3 paradigm. DRQ separates a *region*, and keeps both halves plain INT |
| **Optimization** | region-wise granularity · dynamic/runtime precision selection · mean-filter sensitivity predictor · binary mask map · variable-speed systolic array · time-multiplexed multi-precision PE · predictor fused into pooling · QAT | |

**§4 fairness verdict.** Iso-MAC-area (0.32 mm², 45 nm) and iso-buffer (5 MB) — and DRQ re-models
every baseline at its own node instead of quoting theirs, which is the right call. Against that:
**not iso-training** (DRQ retrains, OLAccel is retraining-free, and this is never stated outside
§III-D); **not iso-costed** (DRQ's multi-precision PE is priced as a plain INT4 MAC while
OLAccel's INT16 MACs are priced in full, and DRQ's predictor, mask buffer, im2col engine and
stall network are outside the area budget entirely — nothing was synthesised); and **not
iso-MAC-count** (3168 vs OLAccel's 2499, +26.8%, against a reported 21% speedup that §VI-A itself
attributes to the PE count). **Numbers not to quote:** "3% accuracy improvement over OLAccel" —
it is 1.3 points on CIFAR-10 and 3.5 on ILSVRC-2012 and the 3.3% average is not reconstructible;
and "21% over OLAccel", which is within rounding distance of the MAC-count ratio.

**Proposed venue-list row:**

```
| [ ] | [DRQ: Dynamic Region-Based Quantization for Deep Neural Network Acceleration](https://doi.org/10.1109/ISCA45697.2020.00086) | *close read* | ALGO+ARCH | Q | `INT4` `INT8` `MIXED` | G2 | `region-wise granularity` `dynamic precision selection` `mean-filter predictor` `binary mask map` `variable-speed systolic array` `QAT` | Sensitivity is **spatially clustered** in the feature map, so pick precision per region, per image, at runtime. The corpus's only sustained argument for *dynamic* selection — and everything after 2020 reverts to static |
```

## Note from the source list

> **Keywords:** a dynamic region-based quantization, change the precision of model based on the sensitive regions in the feature map


## Abstract (verbatim, from the archived PDF)

> Quantization is an effective technique for Deep Neural Network (DNN) inference
> acceleration. However, conventional quantization techniques are either applied at network
> or layer level that may fail to exploit fine-grained quantization for further speedup, or
> only applied on kernel weights without paying attention to the feature map dynamics that
> may lead to lower NN accuracy. In this paper, we propose a dynamic region-based
> quantization, namely DRQ, which can change the precision of a DNN model dynamically based
> on the sensitive regions in the feature map to achieve greater acceleration while
> reserving better NN accuracy. We propose an algorithm to identify the sensitive regions
> and an architecture that utilizes a variable-speed mixedprecision convolution array to
> enable the algorithm with better performance and energy efficiency. Our experiments on a
> wide variety of networks show that compared to a coarse-grained quantization accelerator
> like “Eyeriss”, DRQ can achieve 92% performance gain and 72% energy reduction with less
> then 1% accuracy loss. Compared to the state-of-the-art mixed-precision quantization
> accelerator “OLAccel”, DRQ can also achieve 21% performance gain and 33% energy reduction
> with 3% prediction accuracy improvement which is quite impressive for inference.
