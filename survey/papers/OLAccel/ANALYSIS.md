# OLAccel — paper notes

**Energy-Efficient Neural Network Accelerator Based on Outlier-Aware Low-Precision Computation**
Eunhyeok Park, Dongyoung Kim, Sungjoo Yoo
**ISCA 2018**, pp. 688-698 ｜ DOI: **10.1109/ISCA.2018.00063**
Publication info verified 2026-09-02: venue, year **and DOI** all read out of the archived
PDF's own text (IEEE proceedings banner; the DOI was grepped for, not assumed); page range
from the ACM DL record.
Archived here: the **published IEEE version** (the page-1 IEEE proceedings banner is present in the extracted text), 11 pages.

Status: **note ready** ｜ Last updated: 2026-09-09
Tags: `analytical-dtype` `combined-dtype` `mixed-precision` `dtype-granularity` `accelerator`
How far it was read: **full close read of all seven sections** (pp. 688-698). §II (motivation),
§III-A-E (architecture), §IV (methodology) and §V (results) were read line by line, including
every figure caption and both footnotes; §VI (related work) and §VII (conclusion) were read in
full but are thin. Every number in the table below was transcribed from the paper's own text with
its frame. Cross-checked against the four entries in this corpus that use OLAccel as a baseline
([`OliVe`](../OliVe/ANALYSIS.md), [`MicroScopiQ`](../MicroScopiQ/ANALYSIS.md),
[`Tender`](../Tender/ANALYSIS.md), [`DRQ`](../DRQ/ANALYSIS.md)).
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> Publisher record: https://dl.acm.org/doi/10.1109/ISCA.2018.00063
> **There is no arXiv version** (arXiv API title search, 2026-09-02). The PDF was downloaded by a
> human and filed through [`survey/uploads/`](../../uploads/) — the sanctioned route when the
> arXiv-only rule leaves a paper unreachable; see
> [`Notes-002`](../../../Claude/notes/Notes-002-paper-source-access.md).
> The PDF is **not committed** (0.9 MB) and **cannot be re-downloaded by script** —
> both publishers 403. Re-extract with `python3 extract.py` → `extracted/` (committed).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, ISCA 2018 row.

---

## Brief

### 1. Motivation

Very deep networks (ResNet-101, DenseNet-121) resist 4-bit quantization because a small
number of large-magnitude values — **outliers** — blow up the quantization range. The
observation that carries the whole outlier line of work: keeping just ~3% of values at high
precision restores accuracy at <1% loss while the other 97% goes to 4 bits.

### 2. Overview

An accelerator built on 4-bit MAC units that handles the sparse high-precision outliers
separately: outlier *weights* get an extra MAC per SIMD lane (so the common case of one
outlier per lane costs no extra cycle), outlier *activations* go to dedicated high-precision
MACs, and both paths update partial sums in a pipeline to avoid coherence problems.

### 3. Pros and cons

**Pros**

- The origin point of outlier-aware quantization architecture — every later entry in that
thread ([`OliVe`](../OliVe/ANALYSIS.md), [`MicroScopiQ`](../MicroScopiQ/ANALYSIS.md),
[`OASIS`](../OASIS/ANALYSIS.md)) is answering it.
- Energy wins are substantial and honestly attributed: 43.5–62.2% versus a 16-bit zero-aware
accelerator, **mostly from DRAM and on-chip memory**, not from the MACs.
- Splitting weight and activation outlier handling into two different mechanisms is a
genuinely thoughtful piece of design, not a uniform bolt-on.

**Cons**

- Outliers are stored sparsely, so the design needs a coordinate list and irregular access —
exactly the cost [`OliVe`](../OliVe/ANALYSIS.md) later attacks as unaligned and hardware-
unfriendly.
- Evaluated on CNNs of its era; whether the 3% outlier budget holds for transformers is not
addressed here, and later LLM work suggests the outlier structure differs.
- [`DRQ`](../DRQ/ANALYSIS.md) reports OLAccel losing up to ~5% accuracy on compact models
such as MobileNet-v2 — a weakness not visible in this paper's own benchmark set.

### 4. Where it applies

The anchor of the **§2.2b outlier-compression** box, and the historical baseline for both
accuracy and hardware-overhead comparisons in outlier-aware work.

---

## Corrections to the brief

The close read overturns four things the abstract-level brief asserted:

1. **Outlier weights are 8-bit, not 16-bit.** §II says outliers "maintain their original high
   precision, e.g., 16 bits", and the brief repeated it. The **as-built** hardware stores outlier
   *weights* at **8 bits** (Table I text, p. 693: "OLAccel has 16 (8)-bit outlier activations …
   and **8-bit outlier weights**") **verified**. Only outlier *activations* are 16-bit — and only
   in the 16-bit comparison; the 8-bit comparison uses 8-bit outlier activations. This is the same
   shape of gap as [`Oaken`](../Oaken/ANALYSIS.md)'s 5-bit "high-precision" outliers.
2. **One extra MAC per SIMD *group*, not per lane.** The brief (and the seed-tag keyword
   `extra MAC per lane`) says an extra MAC per lane. §III-A: "The normal PE group contains
   **17 (16 normal and one outlier)** 4-bit MAC units" **verified**. The overhead is 1/16, not 1/1
   — a 16× difference in the cost of the paper's headline mechanism.
3. **DRQ's accuracy criticism stands as the brief had it** — this entry originally "corrected"
   it and the correction was wrong. DRQ §VI-A reports OLAccel losing **5.4% on MobileNet-v2** and
   **5.1% on Inception-v3**, against DRQ's 0.9% and 0.7% **verified**; separately it reports a
   5.1-point margin on ResNet-50 / ILSVRC-2012. Averages across its six networks: OLAccel **1.6%
   (CIFAR-10) / 4.3% (ILSVRC-2012)** vs DRQ 0.3% / 0.8%. The frame that *does* need stating:
   these are **DRQ's own reproduction** of OLAccel (DRQ §V-A: "For ResNet-18, ResNet-50, VGG16,
   Inception-v3 and MobileNet-v2 that are not available in their paper, **we reproduce their
   experiments**"); **DRQ retrains and OLAccel does not**; and DRQ never states whether its
   "accuracy" is top-1 or top-5, while OLAccel's <1% is top-5. Two of DRQ's six networks are ones
   OLAccel never evaluated.
4. **The accuracy study and the hardware are not the same configuration.** Figure 2's outlier-ratio
   sweep is explicitly "**for 16-bit outliers**" **verified**; the accelerator built in §III uses
   8-bit outlier weights. No accuracy number is reported for the configuration that was
   synthesised. **Inferred / not verified**: the gap is probably small, since 8 bits over a
   3%-tail is generous, but the paper does not close it.

---

## Conclusions

**The origin point of the outlier thread, and it already contains the whole argument.** The claim
that carries the next seven years of work is one sentence in §II: keep ~3% of values at high
precision and 4-bit quantization stops failing on deep networks — no retraining. Everything
`OliVe`, `MicroScopiQ`, `Oaken` and `OASIS` do is a dispute about *what currency you pay* for
that 3%, not about whether the 3% is worth keeping.

**Its lasting architectural idea is the asymmetry, not the outliers.** OLAccel handles outlier
weights and outlier activations by two completely different mechanisms, for a reason it never
states in one place but which the design makes obvious: **weight outlier positions are known
offline and can be packed into the format; activation outlier positions are only known at
runtime and must be discovered.** So weights get an in-place encoding inside the normal
datapath (usually free), and activations get a separate wider datapath fed by a coordinate list
(never free). Later papers mostly abandon the activation half — `GOBO` is weight-only,
`MicroScopiQ` is weight-only, `Oaken` is KV-only — which makes OLAccel the corpus's only entry
that pays for dynamic activation outlier detection in hardware.

**The energy result is real but is mostly a MAC-density result.** At iso-area, 4-bit MACs buy
768 units against Eyeriss's 165 and ZeNA's 168. The paper says so plainly (§V: "This is mainly
due to a large number of MAC units … which is enabled by reduced precision"). The honest reading
is that OLAccel demonstrates *the value of 4 bits*, and shows that outlier handling costs little
enough (+20.6% energy, +10.6% cycles over a 0%-outlier design) not to eat the gain. That second
number is the actual contribution and it is the one nobody cites.

**Unusually disciplined for 2018, and unusually honest about where the discipline stops.** It is
iso-area at one node with one memory model, and it volunteers three things against itself: that
the shared memory sizing "is advantageous for OLAccel"; that its baseline ZeNA skips both zero
weights *and* activations while OLAccel skips only activations; and that the first-layer escape
hatch costs **half of ResNet-18's total cycles**. Papers from 2023-25 in this corpus do not
volunteer as much.

---

## Method

**The format.** Two classes per tensor, split by magnitude at a per-layer threshold.

- **Normal weights** 4-bit, **normal activations** 4-bit.
- **Outlier weights** 8-bit — sign + 7 magnitude bits, **split across two fields** (below).
- **Outlier activations** 16-bit (8-bit in the 8-bit comparison), stored sparsely with
  coordinates.
- **Partial sums 24-bit** throughout (§III-B: "a partial sum requires higher precision (24 bits)";
  §III-E: "16 24-bit data items") **verified**.

**Weight chunk — an 80-bit record covering 16 weights** (§III-B, Fig. 5) **verified**:

| Field | Width | Purpose |
|---|---|---|
| 16 × 4-bit weights | 64 b | the dense low-precision stream |
| `OLptr` | 8 b | index of a second chunk, used only when ≥2 outliers |
| `OLidx` | 4 b | which of the 16 lanes holds the outlier |
| `OLMSB` | 4 b | the outlier weight's most-significant nibble |

The trick: with **one** outlier in the chunk, its low nibble (3 magnitude bits + sign) sits **in
the slot the normal weight would have occupied**, and only its high nibble needs new storage.
So a single outlier costs *no additional weight storage at all*. All three fields are zero when
there is no outlier, so the record is fixed-width. **Derived, verified arithmetic:**
80 b / 16 weights = **5.0 bits per weight**, paid unconditionally — a **25% metadata tax on the
nominal 4 bits, whether or not any outlier is present.** The paper never states this figure.

**Outlier weight execution** (§III-D, Fig. 7). A non-zero activation `a0` is broadcast to all 17
MACs. The 17th (outlier) MAC computes `a0 × OLMSB`; its result is broadcast back and the normal
MAC at lane `OLidx` adds it to its own partial sum. **All 17 MACs complete in one clock cycle** —
the common case of one outlier weight per 16 is *free*. **Inferred / not verified:** the `OLMSB`
product must be left-shifted by 4 before the add; the paper's text and Fig. 7 do not mention the
shift, but the split-nibble encoding requires it.

**Outlier weight, degraded case** (§III-D, Fig. 8). With ≥2 outliers in a chunk, `OLptr` points at
a second chunk carrying the extra MSBs, and the operation takes **two clock cycles**; the outlier
MAC is idle and the lanes holding normal weights idle in cycle 2. This is why the SIMD width is
16: **Fig. 17** shows P(multiple outliers) ≈ 20% at a 5% outlier ratio for 16 lanes but **> 50%
for 32 or 64 lanes** **verified**. (Derivation checks out: `1 − 0.95¹⁶ − 16·0.05·0.95¹⁵` = 0.189.)

**Outlier activation execution** (§III-E, Fig. 9). A wholly separate **outlier PE group** of 17
**mixed-precision (16b × 4b) MACs**. Its input is an **outlier activation FIFO** in the swarm
buffer, each entry being a 16-bit value plus **three coordinates** `OLw.idx`, `OLh.idx`,
`OLc.idx` — a coordinate list, exactly the encoding `OliVe` later attacks as unaligned. Coordinate
field widths are **not given**.

**Coherence** (§III-E, Fig. 10). Normal and outlier accumulation units both write partial sums,
so the cluster output is a **tri-buffer**: 2 buffers for the normal accumulator, 1 for the outlier
accumulator, rotating. The outlier accumulator only touches a buffer after the normal accumulator
has left it — a pipeline, not a lock. This is the paper's answer to the problem `MicroScopiQ`
later solves with a NoC and `OASIS` with a second datapath.

**Threshold calibration** (§II) **verified**. Runtime histogramming is too expensive, so the
threshold per layer is fixed at design time from **100 randomly sampled images**; at runtime each
activation is a single compare against it. Weights are thresholded offline. **No retraining** —
§II: "without additional retraining or fine-tuning"; footnote 1: "we apply retraining-free
quantization in this paper". Pure PTQ.

**Zero skipping** (§III-C). Zero *activations* only (not zero weights). PE groups that drain their
chunk early are handed a new one, so lanes stay busy.

---

## Key numbers, with their frame

All hardware numbers are **cycle-accurate model + Design Compiler post-synthesis power (65 nm LP
typical, 250 MHz, 1.0 V) + CACTI for SRAM + Micron DRAM power model** (§IV). **No silicon, no
FPGA.** Never pool with a measured number. All comparisons are **iso-area** and **iso-on-chip-
memory**, and the CNNs are **pruned** (AlexNet/VGG-16 from Han et al.; ResNet-18 pruned by the
authors) so that ZeNA's zero-skipping is exercised.

| Setting | Model | Metric | Baseline | Result | Source |
|---|---|---|---|---|---|
| 4-bit W/A, 3.5% outliers @16b, no retraining | AlexNet | top-5 accuracy | FP32 | **−0.8%** | §V, Fig. 14 **verified** |
| 4-bit W/A, ~1–3.5% outliers | AlexNet 3.5%, VGG-16 1%, ResNet-18 3%, ResNet-101 3%, DenseNet-121 3% | top-1/top-5 | FP32 | "<1% loss" of top-5 | §II, Fig. 3 **verified** |
| 4-bit linear quant, **0% outliers**, no fine-tuning | AlexNet | top-5 accuracy | FP32 | **−76.57%** (collapse) | §II **verified** |
| **Cost of the outlier path**, OLAccel16 | AlexNet | energy / cycles, 3.5% vs 0% outliers | OLAccel itself @0% | **+20.6% energy, +10.6% cycles** | §V, Fig. 14 **verified** |
| Energy, 16-bit comparison | AlexNet | total energy | **ZeNA16** | **−43.5%** | §V, Fig. 11 **verified** |
| Energy, 8-bit comparison | AlexNet | total energy | **ZeNA8** | **−27.0%** | §V, Fig. 11 **verified** |
| Energy, 16 / 8-bit | VGG-16 | total energy | ZeNA16 / ZeNA8 | **−56.7% / −36.3%** | §V, Fig. 12 **verified** |
| Energy, 16 / 8-bit | ResNet-18 | total energy | ZeNA16 / ZeNA8 | **−62.2% / −49.5%** | §V, Fig. 13 **verified** |
| Cycles | AlexNet | execution cycles | Eyeriss16 / Eyeriss8 | **−71.8% / −73.2%** | §V **verified** |
| Cycles | AlexNet | execution cycles | ZeNA16 / ZeNA8 | **−31.5% / −35.1%** | §V **verified** |
| Cycles | VGG-16 | execution cycles | ZeNA16 / ZeNA8 | **−45.3% / −28.3%** | §V **verified** |
| Cycles | ResNet-18 | execution cycles | Eyeriss16 / Eyeriss8 | **−80.1% / −81.1%** | §V **verified** |
| Cycles | ResNet-18 | execution cycles | ZeNA16 / ZeNA8 | **−25.3% / −29.0%** | §V **verified** |
| Area, 16-bit comparison | — | mm², 65 nm | Eyeriss 1.53 / ZeNA 1.66 | **OLAccel 1.67** | Table I **verified** |
| Area, 8-bit comparison | — | mm², 65 nm | Eyeriss 0.96 / ZeNA 1.01 | **OLAccel 0.93** | Table I **verified** |
| MAC count at that area | — | # PEs | Eyeriss 165 / ZeNA 168 | **OLAccel 768 (16b cmp) / 576 (8b cmp)** | Table I **verified** |
| **First-layer escape hatch** | ResNet-18 | share of total cycles, OLAccel16 | — | **~50% of all cycles in conv1** | §V **verified** |
| Zero-skip control cost | AlexNet | cycle overhead | — | **up to ~20%** | §V, Fig. 18 **verified** |
| **Weight metadata tax** | any | bits/weight in the dense stream | nominal 4 b | **5.0 b (+25%), unconditional** | derived from §III-B 80-b chunk **verified arithmetic, not stated in paper** |
| Design-space justification | — | P(≥2 outliers per group) @5% ratio | 32 or 64 lanes: **>50%** | **16 lanes: ~20%** | Fig. 17 **verified** |
| Motivation for non-plain-SIMD | — | P(outlier in a 16-way SIMD step) @1% ratio | — | **27.5% = 1 − 0.99³²** | §III-A **verified** (32 = 16 weights + 16 activations) |

**Numbers that are NOT in this paper** but circulate attributed to it — see *Limitations*:
the 71% PE-array area overhead (`OliVe`), any transformer/LLM result, any per-component area
breakdown, any accuracy figure for the 8-bit-outlier-weight configuration.

---

## Cost and requirements

| | |
|---|---|
| **Unconditional storage tax** | **+1 bit per weight** (80-b chunk / 16 weights), paid even in chunks with no outlier |
| **Per-outlier-activation tax** | 16-bit value **+ three coordinates** (widths unstated) in a FIFO — a coordinate list, unaligned |
| **Extra compute** | 1 extra 4-bit MAC per 16-lane group (**+6.25% MACs**), plus an entire **outlier PE group of 17 mixed-precision 16b×4b MACs**. **The number of outlier PE groups is never stated** — see below |
| **Extra buffering** | cluster output **tri-buffer** (3 banks of 24 b × 16) instead of a single output buffer, purely to keep the two accumulators coherent |
| **Accumulator** | **24-bit**, and Table I's area figures are whole-accelerator, so the psum path **is** included |
| **Calibration** | 100 sample images, once, at design time. No retraining, no fine-tuning, no gradient |
| **Runtime detection** | one compare per activation against a static per-layer threshold |
| **Escape hatch** | first conv layer takes **16- or 8-bit raw input activations** in every network; ResNet-18 and ResNet-101 additionally need **8-bit weights** in conv1. Cost is not small: **half of ResNet-18's OLAccel16 cycles** |
| **Control complexity** | `Tender` §VI-A calls this out directly: "OLAccel has complex control logic and outlier PEs to support mixed precision" |
| **Not exploited** | zero *weights* — ZeNA skips both, OLAccel only skips zero activations, and the paper concedes this costs it against ZeNA |

---

## Limitations and open questions

**The paper's own admitted limits.**

- The first convolutional layer is a genuine hole, and the paper measures it rather than hiding
  it: half of ResNet-18's cycles. Footnote 6 offers fine-tuning as the fix, which would forfeit
  the retraining-free property that is the whole selling point.
- Zero-skip control burns up to ~20% of cycles and §V ends with "In future work, we will work to
  reduce these overhead cycles."
- Single-batch scalability saturates at 16 NPUs from low utilisation (Fig. 15).
- §V notes that a large shared on-chip memory "is advantageous for OLAccel" and amplifies its
  energy win. That is a self-criticism most papers in this corpus do not make.

**Unadmitted, and material.**

- **The MAC count in Table I is not the MAC count.** "768 = 8 × 6 × 16" counts *normal* MACs only.
  The 17th MAC per group (+48) and the outlier PE groups (17 mixed-precision MACs each) are extra,
  and **the number of outlier PE groups is never given anywhere in the paper** **verified by
  exhaustive grep**. `DRQ` §V-B had to guess: it models OLAccel as `3 × 8 × 6 × 17` INT4 MACs plus
  `3 × 17` INT16 MACs — i.e. it assumed **one** outlier PE group per accelerator instance. The
  iso-area claim rests on a configuration the paper does not fully specify.
- **No accuracy number exists for what was built** (see *Corrections* §4).
- **No area or power breakdown by component.** Table I gives whole-accelerator area only. This
  matters because the corpus cites a breakdown to this paper that is not in it (below).
- **Outlier *activation* handling is evaluated only in aggregate.** There is no ablation isolating
  the outlier PE group from the outlier MAC, so the reader cannot tell which half of the
  asymmetric design earns its area.
- **Batch-normalised networks are claimed to behave better and no data is shown** — §V: "Although
  not shown in the paper, the neural networks adopting batch normalization layers, e.g.,
  ResNet-101, tend to provide better distributions."
- **ResNet-101 and DenseNet-121 appear in the accuracy study (Fig. 3) and never in the hardware
  study.** Every cycle and energy number is AlexNet, VGG-16 or ResNet-18. The paper's motivating
  claim is about "very deep networks such as ResNet-101"; the architecture is never run on one.

**Citation hazards this paper creates for the survey.**

1. **`OliVe` §2.2's "71% area overhead" is not traceable to OLAccel.** OliVe writes: "the extra
   outlier controllers of GOBO and OLAccel count up to 55% and 71% overhead to the total area of
   the processing element (PE) array [61, 85]", citing OLAccel. **OLAccel reports no such
   figure** — grep of every occurrence of "area" and "overhead" in the full text finds only
   whole-accelerator mm² and the ~20% zero-skip *cycle* overhead. The 71% is either OliVe's
   synthesis of its own OLAccel re-implementation or a mis-citation. **Do not repeat it as
   OLAccel's number.**
2. **Every OLAccel-on-a-transformer number in this corpus is somebody else's re-implementation.**
   `OliVe` §5: "We **extend** OLAccel to the Transformer-based models with element-wise
   mixed-precision weight and activation quantization." `Tender` and `MicroScopiQ` likewise build
   their own. OLAccel's published evaluation is AlexNet / VGG-16 / ResNet-18, ImageNet, 65 nm,
   2018. The published OLAccel and the baseline called "OLAccel" in ISCA'23-'25 share a name and
   little else.
3. **`DRQ`'s "static quantization on the weight values" is half wrong.** DRQ §VI-A: "OLAccel only
   statically analyzes the numerical distribution of **the weights** and quantizes the weights
   accordingly." OLAccel's *threshold* is static (design-time, 100 images), but its *activation*
   outlier detection is a runtime compare feeding a dedicated outlier PE group — half the design.
   DRQ's point about static-vs-dynamic thresholds is fair; its description of OLAccel as
   weight-only is not.
4. **`MicroScopiQ` §5 lumps OLAccel into "8-bit and 32-bit PEs".** OLAccel has no 32-bit PE; its
   outlier MACs are 16b × 4b and its accumulators 24-bit. The sentence bundles OLAccel with
   AdaptivFloat, which is where the 32 bits come from.
5. **"3% of values" is not one number.** It is 3.5% for AlexNet, **1% for VGG-16**, 3% for the
   rest (Fig. 3), and for activations it is 3% *of non-zero* activations, so the effective ratio
   after ReLU is lower still (§II). Quoting a flat "3%" loses a 3.5× spread.

---

## Relation to other entries

**This is the root of the outlier thread, and its `G3` tag is correct on the merits, not just by
fiat.** The taxonomy's `G3` marks a paradigm — separate the tail, spend on it, quantize the body
hard. OLAccel states that paradigm completely in 2018, five years before the LLM papers that
inherit it.

**It defines the outlier-currency axis' first position.** Adding it to the axis built over the
last five papers:

| Paper | What is paid for keeping an outlier | Who chooses the outlier |
|---|---|---|
| **OLAccel** (ISCA'18) | **+1 bit/weight unconditionally** (chunk metadata) + a **COO record per outlier activation** + a second datapath | magnitude vs a per-layer threshold calibrated on 100 images |
| `GOBO` (MICRO'20) | coordinate list, DRAM-level only | magnitude, weights only |
| `OliVe` (ISCA'23) | **a destroyed neighbour** — zero metadata | adjacency: whoever sits next to the outlier |
| `Oaken` (ISCA'25) | extra bits (5 vs 4) + COO metadata | threshold, 4% outer + 6% inner |
| `MicroScopiQ` (ISCA'25) | **a destroyed weight** + 24 b permutation metadata per μB | Hessian importance, `argmin wₚ²/[H⁻¹]ₚₚ` |
| `OASIS` (ISCA'26) | high precision on a **second datapath** | — |

Read down the "who chooses" column and the thread's actual progress is visible: OLAccel chooses by
magnitude against a calibrated threshold, and by 2025 `MicroScopiQ` chooses by second-order
importance. Read down "what is paid" and the progress is the opposite — from unconditional
metadata to **zero** metadata (`OliVe`) and back to metadata again (`MicroScopiQ`). The field
has not converged on the currency.

**It also seeds a second axis nobody in the corpus names: static vs dynamic outlier
identification.** OLAccel = per-layer threshold fixed at design time, compared at runtime.
`DRQ` (ISCA'20) exists specifically to attack this, substituting a runtime per-region predictor,
and claims 5.1% on ResNet-50 for it. `Tender` sidesteps identification entirely by
decomposing channels. This is worth a line in the survey because the 2023-25 LLM papers
almost all revert to OLAccel's static side.

**Direct baseline usage in this corpus:** `OliVe` (3.8× over it), `Tender` (1.84× speedup, 1.53×
energy efficiency over it), `MicroScopiQ` (1.5× energy on average over a baseline group including
it), `DRQ` (21% performance, 33% energy, 5.1% accuracy over it). **All four use their own
re-implementation.** Any table putting these side by side is comparing four different OLAccels.

**Node hazard, extended.** OLAccel is **65 nm**; `OliVe` is 22 nm; `Tender` and `Oaken` 28 nm;
`MicroScopiQ` and `Omni-LUT` 7 nm. `MicroScopiQ` scales everything to 7 nm with DeepScale; the
others do not scale at all. A corpus-wide TOPS/W or mm² table needs a node column **and** a
"scaled or not" column, and OLAccel now sets the far end of that range at 65 nm.

**Two references outside the ISCA corpus that OLAccel makes load-bearing:** `ZeNA` (Design & Test
2018 — the actual baseline behind every "43.5%" citation, not Eyeriss) and reference [11],
Park/Yoo/Vajda's *Value-aware quantization* (arXiv 2018), which is where the outlier-aware
quantization **method** actually comes from. OLAccel is the architecture paper for someone else's
algorithm; that matters for the `ARCH` vs `ALGO+ARCH` call.

---

## For the note

**§1 one-line summary.** OLAccel splits every weight and activation tensor by magnitude at a
calibrated per-layer threshold into a 4-bit dense body and a ~1–3.5% high-precision tail
(8-bit weights, 16-bit activations), and pays for the tail asymmetrically — outlier weights are
folded into the normal datapath by a 17th MAC per 16-lane group and cost nothing in the common
case, while outlier activations get their own coordinate list and their own 16b×4b PE group —
which at iso-area in 65 nm buys 768 4-bit MACs against a 16-bit baseline's 168 and cuts energy
43.5–62.2% versus ZeNA, retraining-free.

**Proposed tags.**

| Axis | Value | Evidence |
|---|---|---|
| **Level** | `ARCH` | The quantization *method* is cited to [11] (Park/Yoo/Vajda, arXiv 2018); this paper contributes the accelerator, the chunk format and the calibration procedure. Verilog + DC + CACTI, no algorithm ablation. Seed agrees |
| **Q-oriented** | `Q-ORIENTED` | Apply the test: swap the format for plain INT8 and the 17th MAC, `OLMSB`/`OLptr`/`OLidx`, the outlier PE group and the tri-buffer all have no reason to exist. Seed agrees |
| **Data type** | `INT4` `INT8` `INT16` `MIXED` | 4-bit normal W/A **verified**; 8-bit outlier weights **verified** (Table I); 16-bit outlier activations **verified**; 24-bit psum. Seed has `INT4` `MIXED` — I would **add** `INT8` and `INT16` |
| **Generation** | `G3` | Deliberate and correct: outlier separation as a paradigm, stated in full in 2018. Do not touch |
| **Optimization** | `outlier-aware` `sparse high-precision path` `extra MAC per SIMD group` `coordinate-list outliers` `static threshold calibration` `zero-activation skip` `24-bit psum tri-buffer` `iso-area` | |

**§4 fairness verdict.** Iso-area, iso-node (65 nm), iso-on-chip-memory, iso-DRAM-model — and
explicitly **not** iso-MAC (768 vs 168) or iso-accuracy (baselines assumed lossless at 8/16 bits,
OLAccel takes 0.8%). Two elisions the paper concedes: the shared memory sizing favours OLAccel,
and ZeNA skips zero weights while OLAccel does not. One it does not: the accuracy study uses
16-bit outliers, the hardware uses 8-bit outlier weights. **Number not to quote bare:** "43.5%
energy" — it is vs ZeNA16 on a *pruned* AlexNet at 4.6× the MAC count, from a cycle model plus
CACTI, not silicon.

**Proposed venue-list row:**

```
| [ ] | [Energy-Efficient Neural Network Accelerator Based on Outlier-Aware Low-Precision Computation](https://doi.org/10.1109/ISCA.2018.00063) | *close read* | ARCH | Q | `INT4` `INT8` `INT16` `MIXED` | G3 | `outlier-aware` `sparse high-precision path` `extra MAC per SIMD group` `coordinate-list outliers` `static threshold calibration` | "OLAccel". ~1-3.5% of values kept at 8/16-bit restores 4-bit accuracy with no retraining. Weight and activation outliers handled by two different mechanisms. **Pre-LLM root of the outlier thread — the `G3` here is deliberate** |
```

## Note from the source list

> **Keywords:** Dense and low-precision computations for a majority of data while efficiently handling a small number of sparse and high-precision outliers.


## Abstract (verbatim, from the archived PDF)

> Owing to the presence of large values, which we call outliers, conventional methods of
> quantization fail to achieve significantly low precision, e.g., four bits, for very deep
> neural networks, such as ResNet-101. In this study, we propose a hardware accelerator,
> called the outlier-aware accelerator (OLAccel). It performs dense and low-precision
> computations for a majority of data (weights and activations) while efficiently handling a
> small number of sparse and highprecision outliers (e.g., amounting to 3% of total data).
> The OLAccel is based on 4-bit multiply-accumulate (MAC) units and handles outlier weights
> and activations in a different manner. For outlier weights, it equips SIMD lanes of MAC
> units with an additional MAC unit, which helps avoid cycle overhead for the majority of
> outlier occurrences, i.e., a single occurrence in the SIMD lanes. The OLAccel performs
> computations using outlier activation on dedicated, high-precision MAC units. In order to
> avoid coherence problem due to updates from lowand high-precision computation units, both
> units update partial sums in a pipelined manner. Our experiments show that the OLAccel can
> reduce by 43.5% (27.0%), 56.7% (36.3%), and 62.2% (49.5%) energy consumption for AlexNet,
> VGG-16, and ResNet-18, respectively, compared with a 16-bit (8-bit) state-of-the-art zero-
> aware accelerator. The energy gain mostly comes from the memory components, the DRAM, and
> on-chip memory due to reduced precision.
