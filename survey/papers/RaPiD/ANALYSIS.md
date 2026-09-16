# RaPiD — paper notes

**RaPiD: AI Accelerator for Ultra-Low Precision Training and Inference**
Swagath Venkataramani, Vijayalakshmi Srinivasan, Wei Wang, Sanchari Sen, Jintao Zhang, Ankur
Agrawal, … Sunil Shukla, Leland Chang, Kailash Gopalakrishnan — **59 authors**, IBM Research
(Yorktown, Zurich, Tokyo) plus IBM Boeblingen / Austin / Hopewell Junction / Poughkeepsie /
Hursley. Transcribed from page 1, 2026-09-09.
**ISCA 2021**, pp. 153-166 ｜ DOI: **10.1109/ISCA52012.2021.00021**
Publication info verified 2026-09-02: venue, year **and DOI** all read out of the archived
PDF's own text (IEEE proceedings banner; the DOI was grepped for, not assumed); page range
from the ACM DL / IEEE Xplore record.
Archived here: the **published IEEE version** (the page-1 IEEE proceedings banner is present in the extracted text), 14 pages.

Status: **note ready** ｜ Last updated: 2026-09-09
Tags: `analytical-dtype` `mixed-precision` `multi-bitwidth-hw` `training` `accelerator`
How far it was read: **full close read of §I-§VII.** §II (formats and baseline), §III (core
architecture — MPE, FPU/FXU split, sub-SIMD, dataflows), §IV (chip and system) and §V (results,
including the Fig. 17 cycle breakdown and the system-scaling study) read line by line; §VI read
for its positioning claims. Figures are bitmaps in the extraction, so **every number below comes
from the paper's prose**, and the figure-only per-benchmark bars are deliberately not transcribed.
Read after [`BitFusion`](../BitFusion/ANALYSIS.md), whose problem this paper solves the opposite
way (two pipelines, not one fused datapath).
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> Publisher record: https://ieeexplore.ieee.org/document/9499865/
> **There is no arXiv version** (arXiv API title search, 2026-09-02). The PDF was downloaded by a
> human and filed through [`survey/uploads/`](../../uploads/) — the sanctioned route when the
> arXiv-only rule leaves a paper unreachable; see
> [`Notes-002`](../../../Claude/notes/Notes-002-paper-source-access.md).
> The PDF is **not committed** (15.1 MB) and **cannot be re-downloaded by script** —
> both publishers 403. Re-extract with `python3 extract.py` → `extracted/` (committed).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, ISCA 2021 row.

---

## Brief

### 1. Motivation

AI accelerators must keep scaling across generations, and the error-resilience of AI
workloads makes **precision scaling** the most direct lever. The paper is IBM's realisation
of a precision-scaling roadmap in silicon.

### 2. Overview

A fabricated **4-core chip in 7 nm EUV, 36 mm²**, supporting a spectrum of precisions in one
datapath: 16- and 8-bit floating point (including hybrid FP8) and 4- and 2-bit fixed point.
Evaluated with a performance model **calibrated to within 1% of chip measurements**, then
projected to a 768 TFLOP 4-chip, 32-core-per-chip system.

### 3. Pros and cons

**Pros**

- Real fabricated silicon with measured peaks — **3.5 TFLOPS/W in HFP8, 16.5 TOPS/W in
INT4** — which makes it one of the few hard reference points in the corpus.
- Covers **both training and inference** in one architecture (FP8 training, INT4 inference),
which almost nothing else here does.
- The 1%-calibrated performance model is exactly the methodological standard the survey
should hold simulation-based papers to.

**Cons**

- INT2 is supported in hardware but not evaluated, because the models still lose ~2%
accuracy — an honest admission that the bottom of the precision range was not usable.
- Speedups at low precision are limited by the fraction of operations that must stay FP16;
the end-to-end gains (1.2–1.8×) are much smaller than the peak-TOPS ratios suggest.
- The formats supported are adopted from prior algorithmic work, so the contribution is the
chip, not the data type.

### 4. Where it applies

The industrial anchor for **multi-bitwidth hardware** and the only serious **training**
hardware entry. Its gap between peak and end-to-end numbers is a caution worth quoting
whenever the survey cites peak TOPS/W.

---

## Corrections to the brief

The brief was accurate. Four things it did not have, all of which matter:

1. **The training result is a 32× extrapolation beyond the fabricated chip.** The silicon is
   **4 cores**. The training system modelled is **4 chips × 32 cores = 128 cores** (§V-A)
   **verified**. The model is calibrated to within 1% of measurement — but that calibration is on
   a 4-core part. Inference uses the real 4-core configuration; **training does not**.
2. **INT4 inference here requires QAT, not PTQ.** The formats come from PACT [42] and SaWB [46],
   and PACT's clipping value is *learnt* — §II-C: "the clipping value is not statically fixed, but
   rather **learnt**" **verified**.
3. **"FP16" is not IEEE FP16.** §IV lists the five formats as **FP16 (1,6,9)**, FP8(1,4,3) with
   programmable bias, FP8(1,5,2), INT4, INT2 **verified**. (1,6,9) is IBM's DLFloat16, not IEEE's
   (1,5,10) — one extra exponent bit, one fewer mantissa bit. Stated exactly once, in passing.
4. **The paper states its own headline system size three ways** — "768 TFLOPs" (abstract),
   "760 TOPs" (§IV-A), "768 TOPs" (§VII) — and mixes TOPs with TFLOPs for an HFP8 system.

---

## Conclusions

**This is the corpus's only fabricated silicon, and that alone changes what it is for.** Every
other entry read so far is a cycle model, an RTL synthesis, or a PnR estimate. RaPiD is a 36 mm²
7 nm EUV part with measured power. It should be the **calibration point** the survey holds
simulation-based claims against, and it earns that role less through its headline numbers than
through what it measures about the *gap* between headline and reality.

**The most valuable number in the paper is Figure 17, and it is not in the abstract.** For INT4
inference, averaged across benchmarks, the compute cycles break down as: **Conv/GEMM 50%**,
Conv/GEMM overhead from array-dimension mismatch **14%**, **quantization 17%**, auxiliary
operations **19%** **verified**. Two readings follow, and both are things no other entry in this
corpus supplies. First, **only half the cycles are the matrix math the whole design exists to
accelerate.** Second, **quantization itself costs 17% of all compute cycles** — a measured price
for an operation that most papers in this corpus either omit or wave away as negligible.

**The peak-versus-sustained gap is measured, not argued.** Peak **16.5 TOPS/W** in INT4; sustained
**3-13.5, average 7** — a **2.4× gap at the mean and 5.5× at the worst case**. Peak 768 TFLOPS for
the training system; sustained **102-588, average 203** — a **3.8× gap**. Notably HFP8 inference is
much closer to its peak (3.5 → 3.16 average, 1.1×) than INT4 is, because INT4's Amdahl fraction is
larger: the ops that must stay FP16 — first and last layers, activation functions, normalization,
pooling — are a bigger share of what remains once you have made the multiplies 4× cheaper. **INT4
delivers 4× the peak ops and 2.8× the average end-to-end speedup, as little as 1.4×.**

**It answers BitFusion's question the opposite way, and reports the cost.** BitFusion fuses **one**
datapath across all precisions. RaPiD builds **two** — an FPU for FP16/HFP8 and an FXU for
INT4/INT2 — and says why: separating them "solves the architectural complexity of handling
multiple precisions while providing circuit implementation opportunities to aggressively improve
power efficiency." The price and the payoff are both stated: the separate INT pipeline costs
**~16% area**, but its power is **0.3× the FP16 pipeline's**, and that headroom is what paid for
**doubling** the INT4/INT2 engines. This is the corpus's only direct evidence on fuse-versus-split
from a team that built the thing.

**It contributes no data type.** HFP8 is from [44, 45]; PACT and SaWB are from [42, 46]. Like
`BitFusion`, RaPiD is a hardware-mechanism paper — the contribution is that these formats were
made to run at scale in silicon, not that they were invented.

**And it uses sparsity for power rather than for skipping**, which nothing else here does. Average
sparsity is 50-80%; RaPiD does not skip those operations, it uses the power they free to clock
higher under a fixed budget, worth **1.1-1.7× (average 1.3×)**. Every zero-skipping design in this
corpus (ZeNA, Cnvlutin, SCNN, `OLAccel`, `DRQ`) spends control logic to *avoid* the work; RaPiD
spends nothing and converts the slack into frequency.

---

## Method

**Five formats, two pipelines.** §IV **verified**:

| Format | Fields | Used for | Pipeline |
|---|---|---|---|
| **FP16** | **(1,6,9)** — IBM DLFloat, *not* IEEE (1,5,10) | baseline training/inference; all auxiliary ops | FPU |
| **FP8(1,4,3)** | programmable exponent bias | activations and weights, forward pass | FPU |
| **FP8(1,5,2)** | higher dynamic range | errors/gradients, backward pass | FPU |
| **INT4** | 2's complement | inference | FXU |
| **INT2** | 2's complement | inference — **supported, never evaluated** | FXU |

**HFP8 training** (§II-B, from [44, 45]) **verified**. Forward pass: **both** operands FP8(1,4,3).
Backward and gradient: **one** operand FP8(1,4,3), the other FP8(1,5,2). The exponent bias is
**configurable per layer**, which is how layers with different dynamic ranges share one exponent
width.

**On-the-fly widening to a 9-bit internal format** (§III-A2) **verified** — the detail worth
knowing. Supporting two different FP8 layouts as multiplier inputs would cost real area, so the
FPU converts **both** (1,4,3) and (1,5,2) to a custom **(1,5,3)** — a **9-bit** format — on the
horizontal bus from L0 or the FIFO from L1. **Storage is 8-bit; compute is 9-bit.** The escape
hatch is inside the datapath.

**sub-SIMD partition** (§III-A2). The FPU's 8-way SIMD is partitioned finely so that one HFP8
FMMA performs **2 multiplies and 2 adds**, giving **2× the peak TOPS of FP16 at the same power and
the same 128-bit interface width**. Logic depth stays comparable to FP16 "due to the 4-bit
multipliers" — a 3-bit mantissa plus the implicit leading 1.

**Double-pumped INT engines** (§III-A3) **verified**. The separate FXU costs **~16% area**, but
its power is **0.3×** the FP16 pipeline's, so the INT engines were doubled: each FXU holds
**8 INT4 (or 16 INT2)** MACs. The SIMD MAC datapath was widened to **256 bits** with two registers
readable per MAC instruction, which also amortises accumulation energy as multiplier cost falls.

**Operand reuse** (§III-A3). Weight-stationary variant: the 8 INT4 operands of B (32 bits) arriving
on the West link are reused across the 8-way sub-SIMD **and** propagated across MPE columns — **64
multiply-adds per operand fetch**.

**Accumulation.** The MPE array always emits **16-bit** results (FP16 or INT16) so auxiliary
operations can run at higher precision; the FP16 and HFP8 paths merge at the adder. HFP8 training
additionally uses **chunk-based accumulation** [51] — hierarchical partial-sum accumulation
performed in the SFUs — to preserve fidelity of long sums. SFUs run FP16/FP32.

**Precision granularity: per program.** §III-A2: "within a program, the precision of the operands
remains fixed, and is set in registers to allow the hardware to determine **data-gating width**."
So it is per-layer/per-kernel in practice, chosen by the compiler, and the registers drive power
gating as well as datapath configuration.

**Chip and system** (§IV). 4 cores on bidirectional CW/CCW rings; ring and cores in **separate
asynchronous clock domains** with independent PLLs; a chip management unit that closes the rings
locally or opens them to build many-chip systems; and a power-management block doing **workload-
aware throttling by clock-edge skipping** to spend the full power budget.

**Quantization algorithms: none of them are this paper's.** HFP8 [44, 45]; PACT [42] (learned
activation clipping) and SaWB [46] (statistics-aware weight binning) for INT4. **PACT is learnt,
so INT4 deployment here is QAT.**

---

## Key numbers, with their frame

**Two evidence levels, and they must not be pooled.** (a) **Silicon measurement** — the 36 mm²
7 nm EUV 4-core part, peak efficiency at nominal voltage, and per-primitive power measured on
chip. (b) **A performance model calibrated to within 1% of those measurements**, then used for
everything end-to-end. Inference is modelled at the **real 4-core** size; **training is modelled at
128 cores, 32× the fabricated part**.

| Setting | Model | Metric | Baseline | Result | Source |
|---|---|---|---|---|---|
| **Silicon, nominal voltage** | — | **peak efficiency, HFP8** | — | **3.5 TFLOPS/W** | §IV, §VII **measured** |
| **Silicon, nominal voltage** | — | **peak efficiency, INT4** | — | **16.5 TOPS/W** | §IV, §VII **measured** |
| Silicon | — | die area / node / clock | — | **36 mm², 7 nm EUV, 1.5 GHz** | §IV **measured** |
| INT4 inference, **batch 1**, 4-core, 96 TOPS, DDR 200 GB/s | 10 benchmarks | **sustained TOPS/W** | peak 16.5 | **3 - 13.5, average 7 → a 2.4× gap at the mean, 5.5× at worst** | §V-B **calibrated model** |
| FP8(1,4,3) inference, batch 1 | " | sustained TOPS/W | peak 3.5 | **1.4 - 4.68, average 3.16** — much closer to peak than INT4 | §V-B **calibrated model** |
| INT4 vs FP16 on the same chip | " | **end-to-end speedup** | FP16 on RaPiD | **1.4× - 4.2×, average 2.8×** — against **4×** the peak ops | §V-B **calibrated model** |
| FP8 vs FP16 on the same chip | " | end-to-end speedup | FP16 on RaPiD | **1.2× - 1.9×, average 1.55×** | §V-B **calibrated model** |
| INT4 / FP8 vs FP16 | " | efficiency improvement | FP16 on RaPiD | **3.6× / 1.6×** | §V-B **calibrated model** |
| **Cycle breakdown, INT4 inference** | average over benchmarks | share of compute cycles | — | **Conv/GEMM 50% · array-mismatch overhead 14% · quantization 17% · auxiliary 19%** | §V, Fig. 17 **calibrated model — the most useful number here** |
| HFP8 training, **mini-batch 512**, 4 chips × 32 cores | 10 benchmarks | **sustained throughput** | system peak **768 TFLOPS** | **102 - 588, average 203 TFLOPS → a 3.8× gap** | §V-C **model, 32× extrapolated** |
| HFP8 vs FP16 training | " | speedup | FP16 | **1.1× - 2×, average 1.4×** — *lower* than inference | §V-C **model, 32× extrapolated** |
| **Sparsity-aware throttling** | " | speedup from frequency selection | no throttling | **1.1× - 1.7×, average 1.3×**, at 50-80% average sparsity | §V-E **calibrated model** |
| INT pipeline cost | — | area overhead of a separate FXU | — | **~16%** | §III-A3 **verified** |
| INT pipeline payoff | — | INT4 pipeline power | FP16 pipeline | **0.3×** — which is what paid for doubling the engines | §III-A3 **verified** |
| Operand reuse | — | multiply-adds per operand fetch | — | **64** | §III-A3 **verified** |
| System scaling, INT4, batch 1 | VGG16, ResNet50, Yolov3, SSD300 | scaling 1 → 32 cores | — | **continues to scale**; MobileNetV1 and memory-bound cases **saturate** (external bandwidth held fixed) | §V-F **model** |
| INT2 | — | anything | — | **never evaluated.** ~2% accuracy loss is cited from [46]; §VII lists it as future work | §II-C, §VII **verified** |

**Benchmarks** (§IV-B) — **11**, not 10: VGG16, ResNet50, InceptionV3, InceptionV4, MobileNetV1
(ImageNet); SSD300, YoloV3, YoloV3-Tiny (COCO); BERT at sequence length 384; a 2-layer LSTM (PTB);
a **4-layer** bidirectional LSTM (SWB300). **Memory**: inference DDR 200 GB/s; training HBM
400 GB/s with a 128 GB/s chip-to-chip interconnect. §IV-B also claims the FP16 baseline is
"quite competitive compared to other accelerator designs, when normalized for technology and
power/area", citing MLPerf [54] — **an assertion, with no table**. **Note:** the paper says BERT is "trained on WMT14 En-De", which is a
translation corpus — likely a transcription slip for a Transformer entry, but it is what the text
says.

---

## Cost and requirements

| | |
|---|---|
| **Two pipelines, not one** | Separate FPU (FP16/HFP8) and FXU (INT4/INT2) per MPE, 8 units each. **~16% area** for the FXU, repaid by 0.3× power and doubled engines |
| **Internal widening** | Both FP8 layouts converted on the fly to a **9-bit (1,5,3)** internal format. Storage 8-bit, compute 9-bit |
| **Accumulator** | MPE array always emits **16-bit** (FP16 or INT16); SFUs at FP16/FP32; HFP8 training additionally needs **chunk-based hierarchical accumulation** in the SFUs |
| **Escape hatch — and it is measured** | First and last layers, activation functions, normalization and pooling stay **FP16**. §V-B names this as the limit on speedup, and Fig. 17 prices it: **auxiliary ops are 19% of INT4 cycles** |
| **Quantization overhead** | **17% of INT4 compute cycles.** Measured, not assumed |
| **Array-shape sensitivity** | **14% of cycles** lost where workload dimensions do not match the MPE array — worst on Inception3/4, Tiny-YOLOv3 and LSTMs |
| **Retraining** | **QAT for INT4** (PACT's clipping value is learnt). HFP8 training is training by definition. No PTQ path |
| **Granularity** | Per program, fixed in registers for the duration; registers also drive data gating |
| **Bandwidth** | 200 GB/s DDR for the inference chip; HBM plus a high-bandwidth inter-chip interconnect for training. INT4 scaling saturates at fixed external bandwidth |
| **Software** | A full in-house compiler and stack, not an afterthought — §IV-B treats it as a first-class requirement |

---

## Limitations and open questions

**Admitted, and unusually plainly for an industrial paper.**

- **INT2 is in the silicon and was never evaluated**, because models still lose ~2%. Listed as
  future work in §VII. The bottom of the precision range was built and left unused.
- **Speedups are limited by the FP16 fraction**, stated in §V-B and quantified in Fig. 17.
- **Training gains are smaller than inference gains** (1.4× vs 2.8×), and §V-C gives both reasons:
  off-chip gradient reduction and weight broadcast, and having to retain forward activations for
  the weight-gradient computation.
- **Mobile networks benefit least** — MobileNetV1 and Tiny-YOLOv3 carry the most auxiliary ops
  and saturate early in the core-scaling study.
- The formats are credited to prior work throughout; the paper does not claim them.

**Unadmitted, and material.**

- **The training system was never built.** 4 cores fabricated, 128 cores modelled. The "calibrated
  to within 1%" claim is real but is a *4-core* calibration; nothing validates the ring, the
  inter-chip interconnect, or gradient reduction at 32× the size. Every training number in this
  paper should be labelled *model*, and the abstract does not label it.
- **The abstract quotes peak efficiency and sustained throughput side by side** without noting
  that they differ by 2.4× (inference) and 3.8× (training). A reader who takes "16.5 TOPS/W" from
  the abstract takes a number the paper's own §V-B contradicts by more than 2×.
- **No accuracy results of any kind.** Accuracy for HFP8, INT4 and INT2 is entirely by citation to
  [42, 44, 45, 46]. There is no table, no dataset result, no confirmation that the *fabricated*
  datapath — including the (1,5,3) internal widening — reproduces the algorithms' published
  accuracy. For a paper about numerical formats this is a real gap.
- **The system size is stated three ways** (768 TFLOPs / 760 TOPs / 768 TOPs), with TOPs and
  TFLOPs used interchangeably for an HFP8 system.
- **"FP16 (1,6,9)" appears once, in a figure-adjacent sentence.** A reader comparing RaPiD's FP16
  baseline against another paper's IEEE FP16 is not comparing the same format, and nothing
  flags it.
- **Sparsity-aware throttling is evaluated as a speedup, never as an accuracy trade.** "50-80%
  sparsity with negligible loss in accuracy" is asserted with no data and no citation.

---

## Relation to other entries

**RaPiD's job in the survey is to be the reality check.** It is the only entry so far whose
numbers were measured on a die, and the one place where the survey can say what fraction of a
quantized accelerator's cycles actually go to the quantized matrix math: **50%**. Any claim
elsewhere in the corpus that quantization overhead is negligible now has a measured counterexample
at **17% of compute cycles**.

**It is the split-datapath answer to [`BitFusion`](../BitFusion/ANALYSIS.md)'s fused one.** Set the
two side by side and the survey has a real design-space argument rather than a chronology:

| | `BitFusion` (ISCA'18) | **`RaPiD` (ISCA'21)** |
|---|---|---|
| Datapath | **one**, fused from 2-bit BitBricks | **two**, FPU + FXU |
| Range | INT 1/2/4/8/16, both operands independent | FP16, HFP8, INT4, INT2 |
| Cost of flexibility | shift-add tree = **67% of the Fusion Unit** | separate INT pipeline = **~16% area** |
| Payoff claimed | 3.5× area / 3.2× power vs bit-serial | INT4 pipeline at **0.3×** FP16 power → engines doubled |
| Evidence | 45 nm synthesis + cycle model | **7 nm silicon** |
| Granularity | per layer, via Fusion-ISA | per program, via registers |

Neither can be called the winner from these papers alone — but RaPiD is the one that shipped, and
its argument (separate pipelines let you optimise each at circuit level) is the one the industry
followed.

**On the generation axis it is `G2` and late.** 2021, and still the `G2` paradigm: match the
datapath to the bitwidth, no tail format, no outlier concept, no codebook. It is the clearest
demonstration in the corpus that **generation is a paradigm and not a year** — RaPiD (2021) is
`G2` while `OLAccel` (2018) is `G3`. That pairing is worth a sentence wherever the survey
introduces the generation axis.

**It is the corpus's only training entry**, and the only one that has to care about gradients,
which is why HFP8's two-format asymmetry (1,4,3) forward / (1,5,2) backward exists at all. That
asymmetry — *different formats for different tensor roles within one computation* — is
structurally the same move `Oaken` makes for K vs V and `MicroScopiQ` makes for inliers vs
outliers, arrived at from a completely different direction.

**Node.** 7 nm EUV, measured — alongside `MicroScopiQ` and `Omni-LUT` at 7 nm (both synthesised
or PnR, not fabricated). The corpus now spans 7 nm to 65 nm, and RaPiD is the **only** entry whose
node figure is a manufactured one. Any TOPS/W table needs a column for that too, not just for node.

**Outside-corpus references it makes load-bearing:** HFP8 [44, 45], **PACT** [42] and **SaWB** [46].
PACT in particular is the reason RaPiD's INT4 is QAT, and it is not in the corpus.

---

## For the note

**§1 one-line summary.** A fabricated 4-core 36 mm² 7 nm EUV chip carrying **two separate
pipelines per PE** — an FPU for DLFloat FP16 (1,6,9) and Hybrid-FP8, an FXU for INT4/INT2 — where
the FP8 pair (1,4,3) forward / (1,5,2) backward is widened on the fly to a 9-bit (1,5,3) internal
format and the INT pipeline's 0.3× power buys twice the engines for ~16% area, measuring **3.5
TFLOPS/W HFP8 and 16.5 TOPS/W INT4 at peak** — and then, with a model calibrated to within 1% of
that silicon, showing the sustained numbers are **2.4× to 3.8× lower**, because only **50% of INT4
inference cycles are the matrix math and 17% are quantization itself**.

**Proposed tags. One change from the seed row: Level, on the human's ruling.**

| Axis | Value | Evidence |
|---|---|---|
| **Level** | `ARCH+SYS` | **Raised from `ARCH` by the human, 2026-09-09: the software stack counts as `SYS`.** §IV-B **verified**: "compile-time and execution-time extensions [53] that are **pluggable into existing frameworks**"; Fig. 12 is "End-to-End Software Stack for Inference and Training". The data types themselves are all cited to prior work (HFP8 [44,45], PACT [42], SaWB [46]), so the contribution is silicon **plus** the compiler and system around it. **`venues/ISCA/README.md` says `ARCH` — report the change, do not edit** |
| **Q-oriented** | `Q-ORIENTED` | Swap everything for one INT8 datapath and the sub-SIMD partition, the (1,5,3) on-the-fly conversion, the programmable exponent bias, the split FPU/FXU and the double-pumped INT engines all lose their purpose. Seed agrees |
| **Data type** | `FP16` `FP8` `INT4` `INT2` `MIXED` | Five formats **verified** in §IV. Worth noting in the note that "FP16" here is **(1,6,9)**, not IEEE. Seed agrees |
| **Generation** | `G2` | 2021 but squarely the multi-precision-datapath paradigm — no tail format, no outliers, no codebook. The corpus's best illustration that generation ≠ year, since `OLAccel` (2018) is `G3`. Seed agrees |
| **Optimization** | `multi-precision datapath` `hybrid FP8` `training` `7 nm silicon` + `split FP/INT pipelines` `sub-SIMD partition` `on-the-fly format conversion` `chunk-based accumulation` `sparsity-aware power throttling` | Seed has the first four; the five I would add are the mechanisms |

**§4 fairness verdict.** The baseline is RaPiD's own FP16 mode, so precision comparisons are
genuinely iso-everything — the cleanest internal control in the corpus. **Two evidence levels that
must not be pooled:** peak efficiency is measured silicon; every end-to-end number is a model, and
the training numbers are modelled at **128 cores against a 4-core part**. **Numbers not to quote
bare:** "16.5 TOPS/W" — sustained is 3-13.5, average 7; "768 TFLOPS" — sustained is 102-588,
average 203. **Quote instead:** the Fig. 17 breakdown, and the 2.8×-average end-to-end speedup
against 4× the peak ops.

**Proposed venue-list row:**

```
| [ ] | [RaPiD: AI Accelerator for Ultra-Low Precision Training and Inference](https://doi.org/10.1109/ISCA52012.2021.00021) | *close read* | ARCH+SYS | Q | `FP16` `FP8` `INT4` `INT2` `MIXED` | G2 | `multi-precision datapath` `hybrid FP8` `split FP/INT pipelines` `sub-SIMD partition` `sparsity-aware power throttling` `training` `7 nm silicon` | Fabricated 4-core chip; **measured silicon**, model calibrated to within 1%. **The corpus's reality check**: only 50% of INT4 inference cycles are Conv/GEMM and **17% are quantization itself**; sustained efficiency is 2.4× below peak |
```

## Note from the source list

> **Keywords:** a 4-core AI accelerator chip supporting a spectrum of precisions, namely, 16 and 8-bit floating-point and 4 and 2-bit fixed-point. Also Support Hybrid-FP8.


## Abstract (verbatim, from the archived PDF)

> The growing prevalence and computational demands of Artificial Intelligence (AI) workloads
> has led to widespread use of hardware accelerators in their execution. Scaling the
> performance of AI accelerators across generations is pivotal to their success in
> commercial deployments. The intrinsic error-resilient nature of AI workloads present a
> unique opportunity for performance/energy improvement through precision scaling. Motivated
> by the recent algorithmic advances in precision scaling for inference and training, we
> designed R A P I D1 , a 4-core AI accelerator chip supporting a spectrum of precisions,
> namely, 16 and 8-bit floating-point and 4 and 2-bit fixed-point. The 36mm2 R A P I D chip
> fabricated in 7nm EUV technology delivers a peak 3.5 TFLOPS/W in HFP8 mode and 16.5 TOPS/W
> in INT4 mode at nominal voltage. Using a performance model calibrated to within 1% of the
> measurement results, we evaluated DNN inference using 4-bit fixed-point representation for
> a 4-core 1 R A P I D chip system and DNN training using 8-bit floating point
> representation for a 768 TFLOPs AI system comprising 4 32-core R A P I D chips. Our
> results show INT4 inference for batch size of 1 achieves 3 - 13.5 (average 7) TOPS/W and
> FP8 training for a mini-batch of 512 achieves a sustained 102 - 588 (average 203) TFLOPS
> across a wide range of applications.
