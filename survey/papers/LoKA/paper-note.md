# LoKA: Low-precision Kernel Applications for Recommendation Models At Scale

**Venue / Year:** ISCA 2026, pp. 1368-1382 · **Link:** https://doi.org/10.1109/ISCA66397.2026.00103 · **Reader:** Haoxuan · **Date:** 2026-09-14

## Tags

| | |
|---|---|
| **Level** | `ALGO+SYS` |
| **Q-oriented** | `Q-ORIENTED` |
| **Data type** | `FP8` `BF16` `TF32` `MIXED` |
| **Generation** | `G2` |
| **Stage type** | `S2T2` |
| **Optimization** | production deployment · FP8 training · recommendation models · distribution-aware profiling · per-layer sensitivity · per-operator kernel dispatch · model-hardware co-design · BlockNorm · bias removal · Hard Swish · GPU · PyTorch |

## Stage-type tags

**`S2T2`** (the **Stage type** row in Tags) — most-matched first. Which layers run in FP8 and which stay in TF32/BF16 is decided per layer from the error measured on each layer's learned input distribution — mixed precision across one model, in production on stock GPUs. The per-operator choice of tensorwise/rowwise/blockwise scaling is recorded in the note but not tagged.

*Tag form `S{stage}T{type}`, vocabulary from `survey/stage2.md` and `survey/stage3.md`. Added 2026-10-02 (ISCA Stage-type batch 2).*

## 1. One-line summary

Meta's production answer to why nobody had shipped FP8 for recommendation models: leave the
**sparse embedding tables — essentially all 257 B to 1.34 T parameters — unquantized** and put
only the dense/interaction **GEMMs into FP8**, then make that survivable by **learning each
layer's real input distribution online and replaying it offline** to measure per-layer error
against TF32 (random-tensor benchmarks under-report it by 15%, and hid an FBGEMM bug that
Probe inputs exposed at **47×**), by **editing the model** — no biases outside the prediction
head, RMSNorm over fixed **256-element blocks** that fit a GEMM thread block and fuse into its
epilogue, Swish → Hard Swish — and by **dispatching tensorwise/rowwise/blockwise recipes across
three kernel libraries per operator and per direction**; hardware is stock H100/B200/GB200/
MI300X/MI350X, and what it buys is **5-20% training and 10-17% inference throughput in
production**, quality-neutral on relative log loss where **0.02% is significant**.

## 2. Data type

**Formats — four, per tensor class.** **FP8** `W8A8` for selected dense/interaction linear layers (weights and activations both). **BF16** for all collectives, always. **FP32** for Probe statistics. **TF32** as the MERE reference precision and the fleet's actual training format (95%, Table III). Gradients recipe-dependent — the best uniform recipe keeps the **input gradient high-precision**.

**The FP8 sub-format is never named** — no E4M3, no E5M2, anywhere in the paper.

**Embedding tables are not quantized.** Nearly all parameters, the whole memory story of an LRM, untouched — LoKA quantizes the FLOPs, not the parameters. Their precision is never stated.

**Granularity.** No fixed choice: **tensorwise / rowwise / blockwise, selected per operator** by Dispatch, forward and backward independently. **No group size is given** for rowwise or blockwise.

**Only stated block size: BlockNorm's 256** (512 also tested). A *normalization* block, not a scale block — but the paper aligns it explicitly with MX block-shared scaling.

**Gradients.** Recipe-dependent. The best uniform recipe keeps the **input gradient in high precision** with tensorwise scaling on the weight gradient.

**Accumulator.** **Not reported.** "Fast accumulation" enabled in the microbenchmarks; nothing said about production. Master weights and optimizer state also unstated.

**Outliers.** No outlier path. BlockNorm is outlier *containment* — global RMSNorm lets one outlier suppress every feature; a 256-block confines it to 256.

**Escape hatches.** Embedding tables and their AlltoAll · **all collectives BF16 regardless of compute datatype** · bias kept in the prediction head · any layer with MERE ≥ 0.2 or speedup ≤ 1.05× stays high precision · Probe statistics in FP32.

**Retraining.** Neither PTQ nor QAT — the paper's own fourth category, **DLP (Direct Low Precision)**: native FP8 end to end. The Mods change the architecture, so **the model is trained from scratch** and block size must match train/inference. **No stock checkpoint can be used.**

## 3. Optimization

**The diagnosis.** LRMs are not LLMs: tight quality constraints (0.02% relative log loss is significant), architectural heterogeneity, and **low arithmetic intensity at LLM-scale FLOPs** — many small GEMMs immediately followed by normalization. Applied naively, FP8 gives Wukong a **1.32× slowdown and +2.5% RLL**. On 27 production GEMM shapes, end-to-end FP8 caps at **1.6× over BF16** against a 2.0× FP8:BF16 peak ratio, **quantization overhead is >30% of GEMM latency**, and with layout/allocation overhead FP8 can be **slower** than BF16. Table III makes the consequence concrete: of the top 500 Ads ranking models, **0% train in FP8 and 1% serve in FP8**.

**LoKA Probe — learn the distribution, don't store the tensor.** Activations exploit batch-dimension independence (LRMs avoid cross-batch operators to prevent label leakage), collapsing state from `O(M²N²)` to `O(N²)` under a batched Welford covariance accumulated in FP32. Weights get a matrix-normal `W ~ MN(M, U, V)`, `O(M²+N²)`, maintained by a Kronecker-factor EMA with Cholesky solves and a trace renormalization against scale drift. Offline, sample from the learned parameters, run the FP8 kernel against a TF32 reference, and score each layer by **MERE** and measured speedup. Cost: **≤1% throughput**, active every 100 iterations. The premise is measured, not asserted — realistic inputs raise MERE by 15% over normal ones, and a broken FBGEMM kernel that random inputs could not distinguish (0.42 vs 0.42) separated by **47×** under Probe inputs.

**LoKA Mods — change the model, not the kernel.** *No Bias*: a large fraction of bias norms never converge, and diverging biases cascade into out-of-bounds errors and, once clamped, annihilate small values; biases removed everywhere but the prediction head. *BlockNorm*: normalization is fused into the GEMM epilogue, but a full output row does not fit one thread block when N is large, and cross-block synchronization eats the fusion win — so LoKA **deliberately relaxes mathematical equivalence** and RMS-normalizes over fixed 256-element blocks, i.e. an unparameterized Grouped RMSNorm, arguing it also decouples feature subspaces so one outlier no longer suppresses all. *Hard Swish*: `x·ReLU6(x+3)/6` removes the exponential that amplifies large values and crushes small ones, and fuses into the same kernel. **None of the three alone achieves stability; only the combination is loss-neutral.**

**LoKA Dispatch — granularity as a runtime decision.** Filter candidate (library, recipe) pairs by `MERE < 0.2` and `speedup > 1.05×`, then take the highest measured throughput; forward and backward decided separately. Shipped as a custom autograd function acting as a universal adapter over TorchAO/DeepGEMM/FBGEMM, plus an init-time pass swapping `Linear` for LoKA-aware wrappers with identical semantics. Not dynamic per iteration — static for inference, and in training only a safeguard against distribution shift, because switching precision mid-run costs a recompile. The payoff is small but the counterfactual is sharp: **1.12× vs 1.08× for the best uniform recipe, and two of five uniform recipes are net slowdowns (0.85×, 0.98×)**.

**What the hardware gets, and what it costs.** No hardware: stock H100/B200/GB200 NVL72/MI300X/MI350X, PyTorch, TorchRec, FSDP. The cost is a retrain, a framework integration, and an admitted gap — error-based probing **has no model of error propagation**, so per-operator errors that would cancel end-to-end still disable low precision for the whole layer.

## 4. Results

| | |
|---|---|
| Baseline | Quality: the **original, unmodified** high-precision model. Speed: the **LoKA-Mods-rewritten** model in high precision. Dispatch: five uniform single-library recipes. Motivating failure: TorchAO tensorwise FP8 |
| Models / datasets | Wukong (257 B params), InterFormer (566 B), ELFM (1343 B; DHEN + SUM + DLRM + DCN + FMB); tens of billions of real examples, thousands of features, 16-256 GPUs across H100 / B200 / GB200 NVL72 / MI300X / MI350X |
| Accuracy delta | **Quality-neutral on relative log loss over the full training trajectory**, all three families; 0.02% RLL is the stated production significance threshold. Naive FP8 for comparison: **+2.5% RLL**. No absolute loss, no A/B test, no business metric anywhere |
| Speedup | **Production: 5-20% training, 10-17% inference.** Benchmarks: training prose "up to 1.19×" (Fig. 10 bars reach **1.26×**), in-trainer inference "up to 1.4×" (bars reach 1.41×), ~10% at 256 GPUs. GEMM latency ≈2×; Mods alone >2× on GEMM-region latency; Dispatch 1.12× compute-only |
| Energy / area | **None reported** — no hardware is built. Probe overhead ≤1% throughput |
| Technology node | N/A. Stock commercial GPUs, five platforms; GB200 and MI350X were unavailable during development and needed no changes |
| Evidence level | **Four levels, and the corpus's first of the top one:** production deployment on a live Ads service (§V, throughput only) → production-scale experiments on real models/data/clusters → GEMM microbenchmarks → vendor peak-FLOPs datasheets. Every figure is a chart; Fig. 11 carries no numbers |
| **Is the comparison fair?** | **Iso-hardware, iso-data, iso-model-scale**; **not iso-baseline** (quality vs unmodified model, speed vs Mods-rewritten model); **not iso-checkpoint** (DLP retrain). No hardware, so iso-area/node N/A. **Do not quote 40%/20% as production** — deployed is **10-17% inference, 5-20% training**; prose says 1.19× training where its own figure shows 1.26× |

## 5. Comment

## 6. Claude notes

*Suggestions from the reading agent. **Strip this section before copying into
`QuantArchSurvey/venues/ISCA/notes/`.***

- **Read depth.** Full close read of §I-§VII. Four things flagged in `ANALYSIS.md` and not resolved: (i) **every figure is a vector chart** — Figs. 3, 4, 8, 9, 10, 12, 13 were read by pulling bar labels out of the extracted layout text, and **Fig. 11 has no extractable numbers at all**; (ii) the Probe's estimator algebra was read for structure, **not re-derived**; (iii) **MERE's units are never defined**, and the `MERE < 0.2` dispatch threshold is *below every measured MERE in the paper* (Table II 0.47-0.56, Table V 0.37) — do not build an argument on that threshold; (iv) bar→platform mapping in Figs. 10/12 is inferred from bar order.
- **All three no-hardware rows are now `Q-ORIENTED`.** Only three ISCA rows lack `ARCH` — LoKA, ENEC and Gist, all `ALGO+SYS` — and after the 2026-09-14 rulings on ENEC and Gist the other two are `Q-ORIENTED` too, so LoKA is no longer the lone case it was when this was written. It is the cleanest test of your 2026-09-09 ruling that a shipped software stack counts toward `SYS`, and I would keep `ALGO+SYS`: `SYS` for the autograd adapter / layer-rewriting pass / dispatch runtime, `ALGO` for the per-layer sensitivity method and the model redesign. In our own `TAGS.md` matrix LoKA and Gist are the only two papers without `accelerator`.
- **On the `Q` test, the literal swap is degenerate here and worth naming.** "Swap FP8 for INT8" leaves LoKA-for-INT8, because the framework's *subject* is the format. The test that discriminates is TAXONOMY's other sentence — remove quantization and the paper collapses. It does, entirely. `Q-ORIENTED`.
- **I would add `TF32` to the seed's data types.** It is the MERE reference, the escape-hatch precision, and 95% of the training fleet. Without it a reader sees `FP8` `BF16` and concludes the fleet is BF16, which Table III contradicts.
- **The `G2` call is the weakest thing in this row, and you already said so.** By TAXONOMY's literal test LoKA is `G1`: it designs neither a numeric type nor an architecture, and "the format is given, and the algorithm adapts to it" is LoKA Mods in one sentence. It is `G2` only by the outline's §4.6 (per-layer sensitivity / mixed-precision search) and §4.7 (granularity), plus BlockNorm-vs-MX as genuine format/model co-design. There is even a `G3` pull — the outline puts FP8 under §5.4 — which the paper defeats by being explicitly non-LLM. I would keep `G2` and say in §5 that it is a §4.6 placement, not a §4.1 one.
- **The one thing I would argue for in §5, if you want it: the TPUv4i pairing.** TPUv4i's Lesson ⑥ is "a DSA may offer quantization, but it must not require it", evidenced by *one* quantized production DNN at Google in 2020. LoKA's Table III is the same measurement five years later at Meta: **0% of the top-500 Ads LRMs train in FP8, 1% serve in FP8**. Together they support a claim no accelerator paper in the corpus can: **hardware low-precision capability has run five years ahead of workload adoption**, and LoKA itemises the bill for closing it — a profiler, three architecture edits, a dispatch runtime, and a retrain.
- **Second cross-paper point: it adds an evidence level above silicon.** RaPiD (7 nm fabricated), SamsungNPU (5 nm fabricated) and TPUv4i are measured hardware; LoKA is the first entry whose headline number comes from a change **shipped into a live revenue service and measured there**. It is also the least reproducible entry here — no code, no architectures, no absolute losses. Both belong in the same sentence.
- **Third: it inverts the co-design direction.** Everywhere else the format is reshaped to fit the model's statistics; here the **model** is reshaped to fit the hardware's block structure, and the paper says outright that BlockNorm "aligns closely with emerging Microscaling (MX) hardware standards". Pairs with MXFFP from the opposite side. On the outlier-currency axis it adds a currency — **normalization scope**, paid in mathematical non-equivalence with the original model.
- **Numbers I would exclude.** (1) **The abstract's 40%** — it is the in-trainer inference *benchmark*; production is 10-17%. (2) **20% training as a production figure** — production is 5-20%. (3) **Table VI's 1.12×** — compute-only, communication removed. (4) Any composed "LoKA vs unmodified model" speedup: the paper never reports one, because the Mods are inside the speedup baseline and outside the quality baseline.
- **The sharpest unadmitted problem, if you want a critical sentence.** §II-C motivates the entire paper with heavy-tailed, "highly systematic outlier activations" (citing LLM.int8()); §III-A then models activations as **multivariate Gaussians** and concedes it does "not perfectly reproduce the long-tail statistics". A second-order surrogate cannot generate the tail events that break FP8. The 47× FBGEMM result is real, but it is evidence about mean/covariance structure, not tails.
- **Credit where due.** §VI-B admits the thing that most undercuts the design: error-based probing **has no model of error propagation**, so Dispatch is "more conservative than needed" and will disable low precision for layers whose errors would have cancelled. Very few papers in this corpus name the flaw in their own optimization objective.
- **`survey/README.md` change, reported not applied:** line 210 status `brief ready` → `analysis ready`; line 254 currently files LoKA under **2.1 Tensor-wise**, which is wrong — its granularity is *selected per operator* from {tensorwise, rowwise, blockwise}, so it belongs under 2.2 or in both with a note. `survey/TAGS.md` needs no change: `analytical-dtype` `gpu-kernels` `training` `mixed-precision` all hold, and the absence of `accelerator` is correct.
