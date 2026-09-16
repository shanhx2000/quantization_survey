# RaPiD: AI Accelerator for Ultra-Low Precision Training and Inference

**Venue / Year:** ISCA 2021 · **Link:** https://doi.org/10.1109/ISCA52012.2021.00021 (no arXiv) · **Reader:** Haoxuan · **Date:** 2026-09-09

## Tags

| | |
|---|---|
| **Level** | `ARCH+SYS` |
| **Q-oriented** | `Q-ORIENTED` |
| **Data type** | `FP16` `FP8` `INT4` `INT2` `MIXED` |
| **Generation** | `G2` |
| **Optimization** | multi-precision datapath · hybrid FP8 · split FP/INT pipelines · sub-SIMD partition · on-the-fly format conversion · chunk-based accumulation · sparsity-aware power throttling · training · 7 nm silicon |

## 1. One-line summary

A fabricated 4-core 36 mm² 7 nm EUV chip carrying **two separate pipelines per PE** — an FPU for
DLFloat FP16 (1,6,9) and Hybrid-FP8, an FXU for INT4/INT2 — where the FP8 pair (1,4,3) forward /
(1,5,2) backward is widened on the fly to a **9-bit (1,5,3)** internal format and the INT
pipeline's 0.3× power buys twice the engines for ~16% area, measuring **3.5 TFLOPS/W HFP8 and
16.5 TOPS/W INT4 at peak** — then showing, with a model calibrated to within 1% of that silicon,
that sustained numbers are **2.4×–3.8× lower**, because only **50% of INT4 inference cycles are
the matrix math and 17% are quantization itself**.

## 2. Data type

**Five formats, two pipelines.** FPU: **FP16 (1,6,9)** + FP8(1,4,3) + FP8(1,5,2). FXU: INT4, INT2. Not a fused datapath — two physical pipelines, chosen per program.
**"FP16" is not IEEE FP16.** (1,6,9) is IBM DLFloat — one more exponent bit, one fewer mantissa bit than (1,5,10). Stated once, in passing. Any cross-paper FP16 baseline comparison is not like-for-like.
**HFP8 splits by tensor role, not by magnitude.** Forward: both operands **(1,4,3)**. Backward/gradient: one **(1,4,3)**, one **(1,5,2)** — errors need the dynamic range. **Exponent bias programmable per layer.**
**Storage 8-bit, compute 9-bit.** Both FP8 layouts converted on the fly to a custom **(1,5,3)** on the bus from L0 / FIFO from L1, so the multiplier sees one format. The escape hatch is inside the datapath.
**INT4/INT2.** 2's complement, inference only. **INT2 is in the silicon and was never evaluated** (~2% loss); listed as future work.
**Granularity.** **Per program**, fixed in registers for the duration — the registers also drive data gating. No per-channel, per-group or per-token anything.
**Outliers.** None. No mechanism, no discussion.
**Accumulator.** MPE array always emits **16-bit** (FP16 or INT16) so auxiliary ops stay high-precision; SFUs at FP16/FP32; HFP8 training adds **chunk-based hierarchical accumulation** in the SFUs to protect long sums.
**Escape hatch — and it is measured.** First/last layers, activations, normalization, pooling stay FP16. Fig. 17 prices it: **auxiliary ops = 19% of INT4 cycles**.
**Retraining.** **QAT for INT4** — PACT's clipping value is *learnt*. HFP8 training is training. No PTQ path anywhere.
**None of the formats are this paper's.** HFP8 from [44,45]; PACT [42] + SaWB [46] for INT4.

## 3. Optimization

**Two pipelines instead of one, and the cost is reported.** BitFusion fuses one datapath across all
precisions; RaPiD builds an FPU and an FXU and says why — separating them "solves the architectural
complexity of handling multiple precisions while providing circuit implementation opportunities to
aggressively improve power efficiency." Price: **~16% area** for the extra INT pipeline. Payoff:
that pipeline runs at **0.3× the FP16 pipeline's power**, and the headroom paid for **doubling** the
engines — 8 INT4 (or 16 INT2) MACs per FXU, on a datapath widened to 256 bits reading two
registers per MAC instruction. This is the corpus's only fuse-versus-split evidence from a team
that built both halves.

**sub-SIMD partition is how FP8 gets 2× without more wires.** Finely partitioning the 8-way SIMD
lets one HFP8 FMMA do **2 multiplies and 2 adds**, giving 2× FP16's peak TOPS at the **same power
and the same 128-bit interface**. Logic depth stays comparable to FP16 because a 3-bit mantissa
plus implicit 1 is only a 4-bit multiplicand.

**Operand reuse.** Weight-stationary variant: 8 INT4 operands (32 bits) on the West link are reused
across the sub-SIMD *and* propagated across MPE columns — **64 multiply-adds per operand fetch**.

**Sparsity spent on power, not on skipping.** Average sparsity is 50–80%, and RaPiD skips none of
it. It uses the power those zeros free to clock higher under a fixed budget — clock-edge skipping
under workload-aware throttling — worth **1.1–1.7× (avg 1.3×)**. Every zero-skipping design in this
corpus (ZeNA, Cnvlutin, SCNN, OLAccel, DRQ) spends control logic to *avoid* the work; RaPiD spends
nothing and converts slack into frequency.

**A software stack, not just a chip — and this is the `SYS` half of the tag.** §IV-B treats the
stack as a first-class requirement rather than an afterthought: **compile-time and execution-time
extensions pluggable into existing DL frameworks**, so the accelerator gets its specific
optimizations without users leaving PyTorch/TensorFlow. Figure 12 is titled "End-to-End Software
Stack for **Inference and Training**" — one stack covering both. Nothing else in the corpus ships
the compiler with the silicon.

**What it actually contributes.** Not a data type — a demonstration that these formats survive
fabrication, a compiler and system to drive them, and, most usefully for us, **an honest
measurement of what is left over**: Conv/GEMM 50%, array-shape mismatch 14%, quantization 17%,
auxiliary 19%.

## 4. Results

| | |
|---|---|
| Baseline | **RaPiD's own FP16 mode** — the cleanest internal control in the corpus. No external accelerator comparison |
| Models / datasets | **11 benchmarks.** VGG16, ResNet50, InceptionV3/V4, MobileNetV1 (ImageNet); SSD300, YoloV3, YoloV3-Tiny (COCO); BERT (seq 384); 2-layer LSTM (PTB); 4-layer bidirectional LSTM (SWB300) |
| Accuracy delta | **None reported.** Accuracy is entirely by citation to [42,44,45,46]. No table, no dataset result, no confirmation the fabricated datapath reproduces it |
| Speedup | INT4 vs FP16 **1.4×–4.2×, avg 2.8×** — against **4×** the peak ops. FP8 vs FP16 **1.2×–1.9×, avg 1.55×**. HFP8 training **1.1×–2×, avg 1.4×** |
| Energy / area | **Peak (measured): 3.5 TFLOPS/W HFP8, 16.5 TOPS/W INT4.** Sustained INT4 **3–13.5, avg 7 TOPS/W**; FP8 **1.4–4.68, avg 3.16**. Training: system peak 768 TFLOPS, sustained **102–588, avg 203**. **36 mm²** |
| Technology node | **7 nm EUV, fabricated, 1.5 GHz** — the corpus's only manufactured part. Inference: DDR 200 GB/s. Training: HBM 400 GB/s, chip-to-chip 128 GB/s |
| Evidence level | **Two levels, never pool them.** Peak efficiency and per-primitive power = **silicon measurement**. Everything end-to-end = a model **calibrated to within 1%** of that silicon — and the **training system is modelled at 128 cores against a 4-core die** |
| **Is the comparison fair?** | Baseline is RaPiD's own FP16 mode — the cleanest internal control in the corpus. But peak is measured silicon and every end-to-end number is a model, and **training is modelled at 128 cores against a 4-core die**. Don't quote "16.5 TOPS/W" (sustained avg 7) or "768 TFLOPS" (sustained avg 203). Quote the Fig. 17 cycle breakdown, and 2.8× end-to-end against 4× peak ops |

## 5. Comment

Supports **both training and inference** in one architecture — HFP8 for training, INT4 for
inference — which nothing else in the corpus does.

## 6. Claude notes

> **Suggestions from the reading agent. Strip this section before copying into
> `QuantArchSurvey/venues/ISCA/notes/`.**

- **Level raised to `ARCH+SYS` by the human** — the in-house software stack counts as `SYS`.
  Supporting evidence from §IV-B: "compile-time and execution-time extensions [53] that are
  **pluggable into existing frameworks**", and Figure 12, "End-to-End Software Stack for Inference
  and Training". **`venues/ISCA/README.md` says `ARCH` and should be changed to `ARCH+SYS`** — I
  did not edit it.
- **The same argument may apply to `BitFusion`, and I have not acted on it.** BitFusion ships
  **Fusion-ISA plus a compiler**, and its §IV exists precisely to define that hardware-software
  interface. If the software stack makes RaPiD `ARCH+SYS`, BitFusion looks like the same case.
  Its seed row currently says `ARCH`. Your call — say the word and I'll update both notes.
- **Otherwise no disagreement with the seed row.** I'd extend the optimization keywords with
  `split FP/INT pipelines`, `sub-SIMD partition`, `on-the-fly format conversion`,
  `chunk-based accumulation`, `sparsity-aware power throttling` — those are the mechanisms, and
  `multi-precision datapath` alone doesn't separate this from BitFusion.
- **This paper's job in the survey is to be the reality check, and Fig. 17 is why.** For INT4
  inference, averaged: **Conv/GEMM 50% · array-mismatch overhead 14% · quantization 17% ·
  auxiliary 19%**. Only half the cycles are the math the design exists for, and **quantization
  itself costs 17%** — measured. Every "negligible overhead" claim elsewhere in the corpus now has
  a counterexample. If one number from this paper reaches the survey, make it this one.
- **The peak-vs-sustained gap is the second thing to take.** 16.5 → avg 7 TOPS/W (2.4×, and 5.5×
  at worst); 768 → avg 203 TFLOPS (3.8×). Note HFP8 is *much* closer to peak (3.5 → 3.16) than
  INT4, because INT4's Amdahl fraction is bigger — once multiplies are 4× cheaper, the FP16
  remainder dominates. That asymmetry is a real finding about where low-precision stops paying.
- **§5 material, if you want it.** RaPiD (2021, `G2`) against OLAccel (2018, `G3`) is the corpus's
  cleanest proof that **generation is a paradigm, not a year**. Worth one sentence wherever the
  generation axis is introduced.
- **Pair it with BitFusion as a design-space argument, not a chronology.** One fused datapath
  (shift-add tree = 67% of the Fusion Unit, 45 nm synthesis) vs two split pipelines (~16% area,
  0.3× power, 7 nm silicon). Neither paper settles it, but RaPiD is the one that shipped and the
  split-pipeline answer is the one industry followed.
- **HFP8's asymmetry is structurally familiar.** Different formats for different *tensor roles*
  within one computation — (1,4,3) forward, (1,5,2) backward — is the same move Oaken makes for
  K vs V and MicroScopiQ for inliers vs outliers, reached from a completely different direction
  (gradient dynamic range, not outliers). Might be worth a line.
- **Three things to be careful citing.** (1) "FP16" here is **(1,6,9)**, not IEEE — a cross-paper
  FP16 baseline comparison is not like-for-like, and the paper flags this exactly once. (2) The
  system size is stated three ways: 768 TFLOPs (abstract) / 760 TOPs (§IV-A) / 768 TOPs (§VII),
  with TOPs and TFLOPs mixed for an HFP8 system. (3) The paper says BERT was "trained on WMT14
  En-De" — a translation corpus; likely a slip for a Transformer entry.
- **A number I would exclude from cross-paper tables:** everything from the training system. It
  was never built — 4 cores fabricated, 128 modelled. The 1% calibration is real but is a 4-core
  calibration; nothing validates the interconnect or gradient reduction at 32× the size.
- **PACT is load-bearing and outside the corpus.** It's the reason RaPiD's INT4 is QAT rather than
  PTQ — worth adding to the running list alongside ANT, GOBO and WRPN.
