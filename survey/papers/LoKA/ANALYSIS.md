# LoKA — paper notes

**LoKA: Low-Precision Kernel Applications for Recommendation Models At Scale**
Liang Luo, Yinbin Ma, Quanyu Zhu, Vasiliy Kuznetsov, Yuxin Chen, Jian Jiao, Jiecao Yu, Buyun
Zhang, Tongyi Tang, Xiaohan Wei, Yanli Zhao, Zeliang Chen, Yuchen Hao, Venkatesh
Ranganathan, Sandeep Parab, Yantao Yao, Maxim Naumov, Chunzhi Yang, Shen Li, Ellie Wen,
Wenlin Chen, Chunqiang Tang — **all 22 at Meta AI, Menlo Park** (verified from the p.1
affiliation block and the `@meta.com` address list)
**ISCA 2026** (2026 ACM/IEEE 53rd Annual International Symposium on Computer Architecture),
pp. 1368–1382 ｜ DOI: **10.1109/ISCA66397.2026.00103**
Publication info verified 2026-09-02 from the **official ISCA 2026 proceedings package**
(title, authors, pages, DOI and abstract all read from its `assets/data/data.js`).
Archived here: **the published proceedings PDF** (`506501b368.pdf`, 15 pages) — not a preprint.

Status: **note ready** ｜ Last updated: 2026-09-14 ｜ **Human-checked 2026-09-14** — tags confirmed; §2 Formats corrected to name all four formats.
Tags: `analytical-dtype` `gpu-kernels` `training` `mixed-precision`
How far it was read: **full close read of §I–§VII and both discussion subsections** (§I
introduction, §II-A–D characterisation, §III-A Probe including the estimator derivations,
§III-B Mods, §III-C Dispatch, §IV-A–D evaluation, §V production deployments, §VI-A–C related
work / limitations / future work, §VII conclusion). References were skimmed only for the
handful cited in-text as load-bearing ([22] LLM.int8() for the outlier premise, [45] AWQ for
error-based probing, [73] quantized collectives, [77] RMSNorm, [71] GroupNorm).
**Not fully resolved, and flagged everywhere they matter:** (i) **every figure in this paper
is a vector chart** — Figs. 3, 4, 8, 9, 10, 12, 13 were read by pulling the bar/axis labels
out of the extracted layout text, so those values are transcriptions, not the paper's prose,
and Fig. 11's latency breakdown carries **no numeric labels at all** in the extracted text
(only the prose "approximately 2×"); (ii) the Probe's estimator algebra (batched Welford,
Kronecker-factored matrix-normal EMA, Cholesky solves, §III-A1) was read for structure and
**not re-derived**; (iii) **MERE's units are never defined** and the Dispatch threshold cannot
be reconciled with any measured MERE in the paper (see Citation hazards); (iv) the mapping of
Fig. 10 / Fig. 12 bars to specific GPU platforms and counts is inferred from bar order, not
labelled per bar.

> The PDF is **not committed** (1.0 MB). It came from the proceedings package a human
> supplied, now archived at [`archieve/ISCA 2026.zip`](../../../archieve/), entry `pdfs/5065-3nexm57sBmVa6MJtFTiSrb/506501b368/506501b368.pdf`.
> **There is no public URL for it** — this is not an arXiv paper. Re-extract with
> `python3 extract.py` → `extracted/` (committed, greppable).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, 2026 row.

---

## Brief

> **What the close read changed** (2026-09-14): the brief's headline "20% higher training
> throughput and 40% faster inference" is a **benchmark** figure, and the paper's own
> production section reports **5–20% training and 10–17% inference** (§V) — the 40% is never
> claimed of production. The brief's con that "the exact quality metric is only partly
> disclosable" is **wrong**: the metric is disclosed as **relative log loss (RLL)** with a
> stated production significance threshold of **0.02%**; what is withheld is the absolute
> loss and the model internals. Two facts the brief did not have, both load-bearing: **the
> sparse embedding tables — i.e. essentially all of the 257 B–1.34 T parameters — are never
> quantized**, and **the quality claim and the speedup claim use different baselines**
> (unmodified model for quality, LoKA-Mods-rewritten model for speed). Everything else in
> the brief survived.

### 1. Motivation

Each GPU generation delivers far more FLOPs at lower precision — B200 FP8 is 29× and FP4 58×
an A100's TF32 (**Table I**, p.1) — and FP8 has been made to work for LLMs. But **large
recommendation models** have not adopted it, and naively applying FP8 gives **1.3× slowdown
and up to 2.5% relative log loss degradation** in production, where **0.02% is already
significant** (§I p.1, Fig. 3 p.3). Three named causes: tight quality constraints,
architectural heterogeneity (wide ensembles + deep hierarchical stacking + specialised
interaction modules, each with its own numerical sensitivity), and **low arithmetic intensity
despite LLM-scale FLOPs** — many small GEMMs immediately followed by normalization, where the
quantization overhead can exceed the benefit.

### 2. Overview

A framework, not an architecture. Three parts: **LoKA Probe**, statistically grounded online
benchmarking that learns activation/weight statistics and quantifies per-layer error to
locate where FP8 is safe and where it is fast; **LoKA Mods**, reusable model adaptations
that widen the safe region; and **LoKA Dispatch**, a runtime that picks the fastest FP8
kernel meeting the accuracy requirement. All of it ships as a PyTorch integration on top of
TorchRec / FSDP that routes to three third-party kernel libraries (TorchAO, DeepGEMM,
FBGEMM); **no hardware is designed, proposed or modified.**

### 3. Pros and cons

**Pros**

- Deployed at production scale — recommendation models serving billions of users across
H100, B200, GB200, MI300X and MI350X — which no other entry in the corpus can claim.
- The diagnosis is sharp about *why* LRMs differ from LLMs: tight quality constraints,
architectural heterogeneity, and low arithmetic intensity (many small GEMMs followed by
normalization) where quantization overhead can exceed the benefit.
- 20% higher training throughput and 40% faster inference **with no quality loss** *in the
§IV benchmarks* (production: 5–20% / 10–17%), and it correctly argues these problems cannot
be fixed by better kernels alone.
- **Table III is a datum nothing else in the corpus supplies**: an actual fleet census of the
top 500 Ads ranking models — 95% TF32 training, **0% FP8 training**, 99% FP16 inference,
**1% FP8 inference (PTQ)**.
- The Probe found and fixed a **real bug in FBGEMM's production benchmark** that random-input
testing could not see (Table V) — an unusually concrete demonstration of the paper's premise.

**Cons**

- No hardware contribution — it is systems and model co-design on stock GPUs, so it sits at
the edge of an architecture survey.
- Production results come with production opacity: model architectures and absolute losses
are not disclosed, the fleet census has no stated methodology, and no code is released.
- FP8-specific; whether the Probe/Mods/Dispatch structure carries to FP4 or to non-
recommendation workloads is asserted rather than shown (§VI-C makes FP4 future work).
- **The Probe's premise and its model contradict each other.** §II-C motivates the whole
paper with heavy-tailed, "highly systematic outlier activations" [22]; §III-A then models
activations as **multivariate Gaussians** and openly concedes it "is not to perfectly
reproduce the long-tail statistics". The tool is second-order; the stated failure mode is not.
- **No production quality experiment.** §V reports throughput only. "No quality loss" in
production rests on the §IV training-trajectory RLL curves; **no A/B test and no business
metric appears anywhere in the paper.**

### 4. Where it applies

The corpus's main **GPU-kernel + training** entry, its only look at recommendation
models, and its **only production-deployment entry for a software stack**. Valuable to the
survey as evidence that **where a format is safe is a per-layer empirical question, not a
model-level one** — and as the only place the survey can say what fraction of a real fleet
actually runs low precision.

---

## Conclusions

**Read in full.** The numbers below carry their frames and evidence levels. The four
Citation hazards must travel with any number quoted from this paper.

---

## Method

**The claim structure.** Three principles → three components. Principle 1: profile under
realistic distributions to know where low precision is safe → **LoKA Probe**. Principle 2:
co-design model components with hardware to *expand* where it is safe → **LoKA Mods**.
Principle 3: orchestrate across kernel libraries to maximise the gains → **LoKA Dispatch**
(§III, p.4). **verified** (§I p.2, §III p.4).

**What is quantized, and what is not.** FP8 is applied to the **linear layers (GEMMs) of the
dense architecture and the dense–sparse interaction modules**. The **sparse embedding tables
are not touched** — "LoKA does not modify the sparse embedding pipeline or inter-GPU
communication pattern" (§IV-C p.10) — and since the embedding tables "contain most model
parameters" (§II-A p.3), essentially none of the 257 B / 566 B / 1343 B parameters in Table IV
is in FP8. FP8 covers the **FLOPs** (24–40 GFLOPs/sample), not the parameters. **verified**
(§II-A p.3, §IV-A Table IV p.9, §IV-C p.10).

**LoKA Probe — online distribution learning.** Rather than storing tensors, the Probe keeps
compact second-order summaries and re-samples from them offline. Activations: exploits
**independence of the batch dimension** (legitimate here because LRMs avoid cross-batch
operators such as BatchNorm, to prevent label leakage through a user's future behaviour —
footnote 2, p.5), which collapses storage from `O(M²N²)` to `O(N²)`; maintained with a
**batched Welford** covariance update accumulated in **FP32**. Weights: cannot assume
dimension independence, so `W ~ MN(M, U, V)` with `vec(W) ~ N(vec(M), V ⊗ U)` — a
**matrix-normal** with row covariance `U ∈ R^{M×M}` and column covariance `V ∈ R^{N×N}`,
`O(M² + N²)` instead of `O(M²N²)`, maintained by a Kronecker-factor flip-flop update with EMA
momentum `m ∈ [0.9, 0.99]`, regularised Cholesky solves instead of explicit inverses, and a
trace renormalisation `s = trace(U)/M` to kill the `(U,V) → (cU, V/c)` scale drift.
**Sampling**: `T' = 1_B µᵀ + Z L_Σᵀ` for activations, `W' = M + L_U Z L_Vᵀ` for weights.
**verified** (§III-A1 pp.5–6; the algebra was read for structure and not re-derived).

**LoKA Probe — offline error quantification.** For each linear layer, sample from the learned
distribution, run the low-precision kernel and a TF32 reference, and compute **MERE** (Mean
Element-wise Relative Error) `Σ_m Σ_n |out_{m,n} − ref_{m,n}| / |ref_{m,n}|`, plus a measured
speedup. Layers with high MERE or low speedup are flagged and excluded. Probe activates
**every 100 training iterations**, saves asynchronously **every 10,000**, costing **≤1%
throughput**. **verified** (§III-A p.4, §III-A1 p.6, §III-A2 p.6).

**LoKA Mods — three model changes, all of them architecture edits.** **verified** (§III-B pp.6–8).
1. **No Bias.** A significant fraction of bias L2 norms never converge (Fig. 6 shows
   diverging / oscillating / vanishing / cycling / drifting / converging modes); diverging
   biases cascade, cause out-of-bounds errors, and when clamped and quantized make small
   values vanish. All biases removed **except in the final prediction layers**. Secondary
   benefit: under FSDP per-parameter padding, bias tensors smaller than the world size incur
   communication overhead.
2. **BlockNorm.** The goal is to fuse normalization into the **GEMM epilogue** while output
   tiles are still in registers/L1/L2. Standard normalization runs along the feature
   dimension, which misaligns with the GEMM output layout: when `N` is large a row does not
   fit in one thread block, so RMS statistics need **cross-block synchronization**, and the
   mitigations (smaller batch tiles) cost SM wave quantization and L2 hit rate. LoKA therefore
   **"deliberately relaxes full mathematical equivalence"** and normalizes over **fixed
   256-element blocks** along the feature dimension:
   `RMSNorm((Wx + b).view(−1, BlockN)).view(B, N)`. RMSNorm rather than LayerNorm because it
   skips mean subtraction and therefore the catastrophic cancellation. The paper argues this
   is exactly an unparameterized **Grouped RMSNorm**, that global RMSNorm "couples all
   channels to a single statistic, meaning one outlier suppresses all features", and that the
   block structure **"aligns closely with emerging Microscaling (MX) hardware standards"**.
   Block size must be **identical in training and inference**.
3. **Hard Swish.** `x · ReLU6(x+3)/6` replaces Swish `x·σ(x)` / SwishNorm `x·σ(Norm(x))`; the
   exponential amplifies large elements and diminishes small ones, "dramatically increasing
   quantization loss". Piecewise-linear, fuses into the same kernel as BlockNorm.

**LoKA Dispatch — constrained per-operator selection.** Candidate (library, recipe) pairs are
filtered by `MERE < 0.2` (typical) **and** `speedup > 1.05×` (typical), both from the Probe;
from the survivors, the highest measured throughput wins. Implemented as a **custom autograd
function acting as a universal adapter**, plus an **initialization-time transformation pass**
that swaps target `Linear` layers for LoKA-aware wrappers with identical PyTorch semantics.
**Forward and backward are dispatched independently.** It is **not** per-iteration dynamic:
for inference the selection is entirely static, and in training the dynamism is only a
safeguard against large distribution shifts, because switching precision mid-training pays a
recompilation tax. **verified** (§III-C pp.8–9).

**The shipped stack.** PyTorch + TorchRec [37] + hybrid parallelism [50] + balanced sharding
[75] + FSDP [81]; three kernel backends (TorchAO, DeepGEMM, FBGEMM); `torch.compile`
integration; **quantized collective communication [73] in BF16 for all models regardless of
compute datatype**. **verified** (§IV-A p.9).

## Key numbers, with their frame

Evidence levels used below: **P-deploy** = measured on a live production service;
**P-scale** = measured on production models, production data and production clusters but as
an experiment; **µbench** = kernel/GEMM microbenchmark; **fleet-survey** = an internal census
with no stated methodology.

| Setting | Model | Metric | Baseline | Result | Source |
|---|---|---|---|---|---|
| **The motivating failure.** TorchAO, tensorwise FP8, applied to *all* linear layers with in/out features ≥ 128; 64× H100. **P-scale** | Wukong | throughput + relative log loss (RLL) | BF16, **520 K examples/s** | FP8 **395 K/s = 1.32× slowdown**; RLL **up to +2.5%**, against a stated production significance threshold of **0.02%** | Fig. 3 + §II-B p.3; threshold §I p.1 — **verified** |
| **Kernel throughput.** 27 production GEMM shapes, `(2048,256)@(256,768)` → `(2048,123200)@(123200,1024)`, H100, forward only. **µbench** | production LRM shapes | effective TFLOPS/s | BF16 | FP8 end-to-end speedup **limited to 1.6× on average**; max effective TFLOPS/s **under 20% of hardware capacity**; **quantization overhead > 30% of end-to-end GEMM latency**; with memory-allocation (layout) overhead **FP8 can be slower than BF16** | §II-C p.4, four bullets — **verified** (prose). Fig. 4 bars read off as compute-only 404 / 409 / 611 / 663 and effective 255 / 285 / 422 / 438 TFLOPS/s for BF16 / TorchAO / DeepGEMM / FBGEMM — **inferred / not verified** |
| **Distribution sensitivity of kernel error.** 4 important linear layers, 50 input–weight pairs each, fast accumulation on, forward only. **µbench** | production LRM | geometric-mean MERE vs **TF32** | standard-normal inputs | learned-LRM inputs raise MERE **by up to 15%**: TorchAO RW 0.47→0.53, DeepGEMM BW 0.49→0.56, FBGEMM RW 0.48→0.52, PyTorch BF16 0.03→0.04 | Table II p.3 — **verified** |
| **Fleet adoption census.** Top 500 Ads ranking LRMs at "a large social-media company". **fleet-survey** | — | share of models by datatype | — | **Training: TF32 95%, BF16/TF32 5%, FP8 0%. Inference: FP16 99%, FP8 1% (PTQ).** | Table III p.4 — **verified** (as a reported census; methodology not given) |
| **Lossless FP8 training, full trajectory.** Tens of billions of examples, thousands of features, production configs. **P-scale** | Wukong, InterFormer, ELFM | RLL vs the **original, unmodified** high-precision model | unmodified baseline | Quality-neutral **for the whole trajectory**, not only at the end. Wukong plotted on a −0.1 → +0.3 pp axis, InterFormer and ELFM on −0.03 → +0.02 pp axes. **No single summary delta is printed.** | Fig. 9 p.9 + §IV-B p.9 — claim **verified**; the axis bounds are read off the figure, **inferred / not verified** |
| **Mods ablation on quality.** Same setup. **P-scale** | Wukong | RLL | FP8 baseline | No Bias reduces early instability, BlockNorm improves conditioning, Hard Swish reduces activation error; **none alone achieves full stability**, only the combination is loss-neutral | Fig. 9 top + §IV-B p.9 — **verified** (qualitative; per-curve values not printed) |
| **End-to-end training speedup.** 5 platforms. **Baseline is the model already rewritten with LoKA Mods**, i.e. this is the FP8-only increment. **P-scale** | Wukong / InterFormer / ELFM | training throughput | Mods-rewritten model in high precision | Prose: **"up to 1.19×"**. Fig. 10 bars: Wukong **1.13, 1.19, 1.15, 1.22, 1.26**; InterFormer 1.08, 1.13, 1.08; ELFM 1.02, 1.09, 1.07, 1.14 | §IV-C p.9 prose **verified**; bar values **inferred / not verified** (read off Fig. 10, bar→platform mapping not labelled) |
| **End-to-end (in-trainer) inference speedup.** Same baseline. **P-scale** | Wukong / InterFormer / ELFM | inference throughput | Mods-rewritten model in high precision | Prose: **"up to 1.4×"**. Fig. 10 bars: Wukong 1.24, **1.39, 1.41**, 1.31; InterFormer 1.21, 1.28, 1.36, 1.28; ELFM 1.14, 1.21, 1.32, 1.23 | §IV-C p.9 — prose **verified**; bars **inferred / not verified** |
| **Where the speedup comes from.** Iteration 706, averaged across all ranks. **P-scale** | Wukong, 16× B200 | iteration latency breakdown | without LoKA | Majority of the gain is **reduced GEMM latency, ≈2×**. Sparse embedding and inter-GPU communication **unchanged** (residual difference attributed to run-to-run variability) | §IV-C p.10 + Fig. 11 — prose **verified**; **Fig. 11 carries no extractable numbers** |
| **Scalability.** 16–256 GPUs on five platforms. **P-scale** | Wukong | training throughput | as above | **≈10% at 256 GPUs**; gain shrinks with cluster size as synchronization and embedding communication grow. Fig. 12 bars span **1.08–1.24×** (H100 1.13/1.12/1.12/1.08; B200 1.19/1.16/1.15/1.11/1.09; GB200 1.24/1.20/1.20/1.12; MI300X 1.15/1.15/1.13/1.12/1.10; MI350X 1.22/1.24/1.20/1.18/1.13) | §IV-C p.10 prose **verified**; bars **inferred / not verified** |
| **LoKA Mods latency contribution, on their own.** 9 GEMM shapes from (256,256) to (256,7680), batch 1024, `torch.compile` on. **µbench** | representative GEMM shapes | linear + activation + normalization latency | unmodified layers | **Combined > 2× latency reduction**; **No Bias is the largest single contributor**, BlockNorm next (fusion), Hard Swish smallest | §IV-D2 p.10 + Fig. 13 — **verified** (prose). Per-bar values are stacked and not reliably separable from the extracted text; **the precision at which Fig. 13 is measured is not stated** |
| **LoKA Dispatch vs uniform recipes.** Compute-only mode, communication removed. **µbench / P-scale hybrid** | Wukong | speedup | TorchAO TW **1.05**, TorchAO RW **1.01**, TorchAO RW-GW-HP **1.08**, DeepGEMM BW **0.85**, FBGEMM RW **0.98** | **LoKA Dispatch (mixed) 1.12×** — better than the best uniform recipe, and **two of the five uniform recipes are net slowdowns** | Table VI p.11 — **verified** |
| **LoKA Probe's detection power.** All 27 linear layers of the subject model, FBGEMM production benchmark before/after a real bug fix. **µbench** | production LRM | MERE | random normal inputs: **0.42 faulty / 0.42 fixed** (indistinguishable) | Probe-generated inputs: **17.04 faulty / 0.37 fixed — a 47× separation**. The bug was reported and fixed with FBGEMM's developers | Table V p.10 + §IV-D1 p.10 — **verified** |
| **Production deployment.** Flagship Ads recommendation services, billions of users, "various launches". **P-deploy** | production LRMs | end-to-end throughput | pre-launch production | **5–20% training throughput; 10–17% inference speedup** | §V p.11 — **verified**. This, not the abstract's 20%/40%, is the deployed number |
| **Probe overhead.** Continuous, during production training. **P-scale** | all | throughput overhead | no Probe | **≤ 1%** (active every 100 iterations, async save every 10,000) | §III-A1 p.6 — **verified** |
| **Hardware envelope.** Vendor peak, for context. | — | dense peak TFLOPS TF32 / BF16 / FP8-INT8 | — | A100 156 / 312 / 624; H100 NVL 418 / 840 / 1671; B200 HGX 1100 / 2250 / 4500 | Table I p.1 — **verified** (vendor datasheets [57]–[59], second-hand) |
| **Model scale.** | Wukong / InterFormer / ELFM | GFLOPs per sample; parameters; batch & GPU count | — | 24 / 28 / 40 GFLOPs; **257 B / 566 B / 1343 B parameters**; batches 2 K–20 K over 16–256 GPUs | Table IV p.9 — **verified**. **Almost all of those parameters are embedding tables and none of them is quantized** |

### Data type, per tensor class

| Tensor class | Format | Granularity | Evidence |
|---|---|---|---|
| **Sparse embedding tables** (≈ all parameters) | **not quantized** — untouched by LoKA | — | §IV-C p.10 **verified** ("does not modify the sparse embedding pipeline"). Their actual precision is never stated; Table III implies TF32 fleet-wide. |
| **Dense / interaction linear-layer weights** | **FP8**, sub-format (E4M3 / E5M2) **never stated** | tensorwise **or** rowwise **or** blockwise — **selected per operator by Dispatch**; no group size given for either rowwise or blockwise | §III-C p.8, §IV-D3 p.10–11 — **verified** that the choice is per-operator; **the group size is nowhere in the paper** |
| **Activations into those layers** | **FP8**, same caveat | same, per operator | as above |
| **Gradients** | **recipe-dependent** — the `RW GW HP` recipe keeps the **input gradient in high precision** and uses tensorwise scaling for the weight gradient; Dispatch decides forward and backward **independently** | per operator, per direction | §III-C p.8 and §IV-D3 p.11 — **verified** |
| **Collectives** (embedding AlltoAll, FSDP all-gather) | **BF16 quantized communication, always**, "regardless of compute datatype" | — | §IV-A p.9 — **verified** |
| **Normalization** | BlockNorm over **256-element blocks** (512 also tested), fused into the GEMM epilogue | block = 256 elements along the feature dimension, **identical in train and inference** | §III-B2 pp.7–8, Fig. 8 p.8 — **verified** |
| **Probe statistics** | **FP32** | — | §III-A1 p.5 — **verified** |
| **Accumulator** | **never reported.** "Fast accumulation" was enabled for the §II-C microbenchmarks; nothing is said about the production configuration | — | §II-C p.3 — **verified** that fast accumulation was used there; the width is **not in the paper** |

- **Outlier mechanism: none in the format.** The word "outlier" appears three times, all
  incidental (grep of the raw text). There is no outlier path, no split precision, no
  high-precision tail. The nearest thing is **BlockNorm as outlier containment** — "Global
  RMSNorm couples all channels to a single statistic, meaning one outlier suppresses all
  features. BlockNorm decouples feature subspaces, preventing catastrophic cancellation"
  (§III-B2 p.7) — **verified**.
- **Escape hatches, in full:** embedding tables and their pipeline; all collectives at BF16;
  bias retained in the final prediction layers; any layer whose Probe MERE ≥ 0.2 or whose
  speedup ≤ 1.05× stays high precision; Probe statistics in FP32; every non-linear op outside
  the fused epilogue. **verified** (§III-B1 p.6, §III-C p.8, §IV-A p.9).
- **Retraining: neither PTQ nor QAT.** The paper's own taxonomy (§II-B p.3) names four
  settings — QAT, PTQ, PQT, and **DLP (Direct Low Precision)** — and states "DLP is the focus
  of LoKA". Because the Mods change the architecture, **the model has to be trained from
  scratch**, and the BlockNorm block size must match between training and inference. A stock
  checkpoint cannot be used. **verified** (§II-B p.3, §III-B2 p.8).

### Citation hazards

1. **The abstract's two headline numbers are benchmark numbers, and the paper's own
   production numbers are smaller.** Abstract: "up to 20% higher training throughput and 40%
   faster inference". §V: **"5-20% end-to-end training throughput and 10-17% speedup in
   production inference"**. The 40% corresponds to Fig. 10's **in-trainer** inference bar
   (1.41×) on a benchmark. **Never quote 40% as a production number.** **verified** (abstract
   p.1 vs §V p.11).
2. **Three different values for the training speedup.** Abstract "up to 20%"; §IV-C prose
   **"up to 1.19×"**; Fig. 10's tallest training bar is **1.26×**; §V's production range tops
   out at 20%. The prose and its own figure disagree. **verified** (§IV-C p.9 text vs the
   Fig. 10 bar labels).
3. **The quality claim and the speedup claim have different baselines.** Fig. 9's quality
   curves are "compared to original, unmodified baselines" (§IV-B p.9); Fig. 10's speedups are
   "over strong baselines (i.e., models that have been rewritten with LoKA Mods)" (§IV-C p.9).
   So **1.19–1.26× is the FP8-only increment on top of the Mods**, and the Mods' own >2×
   GEMM-region latency win (Fig. 13) is inside the baseline. The paper **never reports the
   composed speedup of LoKA-over-an-unmodified-model**, and it is unclear whether Fig. 11's
   "without LoKA" includes the Mods. **verified** for the two baseline statements;
   **inferred / not verified** for what Fig. 11's baseline is.
4. **MERE has no stated units, and the Dispatch threshold contradicts every measured MERE in
   the paper.** Dispatch admits candidates only at `MERE < 0.2` (§III-C p.8), yet Table II's
   FP8 geomeans are **0.47–0.56** and Table V's fixed-code figure is **0.37**. Either MERE is
   reported in different units in different tables, or the threshold excludes essentially
   everything measured. **Do not build an argument on the 0.2 threshold.** **verified** that
   both numbers are printed; the reconciliation is **unresolved**.
5. **The FP8 sub-format is never named.** No "E4M3", no "E5M2", no "float8_e4m3fn" anywhere in
   the text (grepped). Do not attribute a specific FP8 variant, or a forward/backward format
   asymmetry, to this paper. **verified** by grep of `506501b368.raw.txt`.
6. **Table VI's 1.12× is compute-only** — communication deliberately removed, Wukong only.
   It is not comparable to the 1.02–1.26× end-to-end figures. **verified** (§IV-D3 p.10).
7. **"To our knowledge, no prior work has achieved successful FP8 training for large
   recommendation models at scale"** (§I p.1) is a claim about industry practice and cannot be
   checked from outside. Table III's fleet census is likewise an internal survey with no
   stated methodology. **verified** as quotations; unverifiable as facts.
8. **Table I's peak FLOPs are vendor datasheet numbers** [57]–[59], not measurements — and
   §II-C's "under 20% of hardware capacity" does not reconcile with the Fig. 4 bar values
   against Table I's 1,671 TFLOPS H100 NVL FP8 peak (438/1671 ≈ 26%). Minor, but the two
   should not be combined. **inferred / not verified**.

## Cost and requirements

**Hardware: none.** Stock H100, B200, GB200 NVL72, MI300X and MI350X. No datapath, no ISA, no
silicon. **verified** (§IV-A p.9, §VI-A p.12).

**Software, and this is the actual cost.** A custom autograd function acting as a universal
adapter across three kernel libraries; a model-initialization transformation pass that
replaces target `Linear` layers with LoKA-aware wrappers preserving PyTorch semantics;
per-direction dispatch state; integration with `torch.compile`, TorchRec, FSDP, hybrid
parallelism and balanced embedding sharding. **§VI-B concedes that introducing a new
low-precision kernel "may require manual intervention" to integrate with `torch.compile`.**
**verified** (§III-C pp.8–9, §VI-B p.12).

**Model changes — the hard requirement.** Bias removed everywhere but the final prediction
layers; LayerNorm → BlockNorm(256) with the block size frozen across train and inference;
Swish/SwishNorm → Hard Swish. These are architecture edits, so **the model is retrained from
scratch** and existing checkpoints do not transfer. **verified** (§III-B pp.6–8).

**Profiling cost.** ≤1% throughput; `O(N²)` per activation tensor and `O(M²+N²)` per weight
matrix of FP32 state; active every 100 iterations, checkpointed asynchronously every 10,000.
**verified** (§III-A1 pp.5–6).

**Applicability constraint.** "The framework requires models to use standard building blocks,
as novel architectures may need additional kernel development." **verified** (§VI-B p.12).

## Limitations and open questions

**Admitted by the authors (§VI-B, p.12):**
- Probe benchmarks cannot capture **compute–communication overlap**; SM carveout [54] only
  mitigates it.
- Models must use standard building blocks; novel architectures need new kernels.
- Dispatch may need manual work to integrate new kernels with `torch.compile`.
- **The sharpest one: error-based probing "lacks a mechanism to reason about error propagation
  throughout the network, making it more conservative than needed"** — large per-operator
  errors may cancel end-to-end, but Dispatch will disable low precision for all of them. This
  admits that the Probe→Dispatch chain optimises a proxy (per-layer MERE) that is not known to
  track the objective (final quality), and §VI-C floats AutoML as the fix.
- FP8 only; FP4 is future work.

**Not admitted, and worth pressing:**
- **The Gaussian/matrix-normal surrogate versus the heavy-tail motivation.** §II-C's premise
  is "highly systematic outlier activations" [22] and distributions that are "heavy-tailed,
  correlated, or non-stationary" (§I p.2). §III-A1 then models them as multivariate Gaussians
  and states plainly that the objective "is not to perfectly reproduce the long-tail
  statistics of activations but to approximate their second-order structure". A second-order
  surrogate cannot generate the tail events that break FP8 — yet the whole paper's claim is
  that random tensors miss them. The Probe's win in Table V (47×) is real but is evidence
  about *mean/covariance structure*, not about tails.
- **No production quality result.** §V is throughput-only. The evidence for "no quality loss"
  in production is the §IV training-trajectory RLL curves; there is **no A/B test, no business
  metric (revenue, CTR, engagement) and no post-launch quality measurement anywhere**.
- **No absolute quality numbers at all** — every quality figure is a *relative* log loss delta
  against an undisclosed baseline, on undisclosed model architectures, with no released code.
- **No comparison to any competing framework.** The only baselines are uniform single-library
  recipes and unmodified high precision. Nothing from the LLM FP8 literature ([19], [35]) is
  run on LRMs, so "LLM techniques do not transfer" is argued from first principles plus one
  TorchAO run.
- **The Mods are not separated into "helps FP8" and "helps anyway".** No Bias is the *largest*
  latency contributor in Fig. 13 and would speed up a BF16 model too. Fig. 9 does separate the
  quality contributions, but the latency story mixes generic efficiency with FP8 enablement.
- **BlockNorm is not the same function as RMSNorm.** The paper says so — it "deliberately
  relaxes full mathematical equivalence" — and defends it as an unparameterized Grouped
  RMSNorm with *more* representational capacity. That is a plausible argument, not a measured
  one; the only evidence is one Wukong curve at block 256 vs 512 (Fig. 8).
- **Sub-format, accumulator width, master-weight and optimizer-state precision are all
  unstated**, so the actual effective bitwidth of "FP8 training" here cannot be computed.

## Relation to other entries

**It changes the corpus's evidence hierarchy by adding a level above it.** The measured-silicon
entries are [`RaPiD`](../RaPiD/ANALYSIS.md) (7 nm fabricated), [`SamsungNPU`](../SamsungNPU/ANALYSIS.md)
(5 nm fabricated) and [`TPUv4i`](../TPUv4i/ANALYSIS.md) (deployed Google silicon). LoKA is the
first entry whose headline number comes from **a change shipped into a live revenue service and
measured there** — `P-deploy` in the table above. It is also the corpus's **least reproducible**
entry: no code, no architectures, no absolute losses. The survey should say both in the same
sentence, because the trade is exactly the one industrial papers make.

**The TPUv4i pairing is the most valuable cross-reference in this file.** TPUv4i's Lesson ⑥ is
that **"a DSA may offer quantization, but it must not require it"**, and its evidence is that
only *one* of Google's production DNNs was quantized at all (2020, pre-LLM). LoKA's Table III
is the same measurement five years later, at a different company, on a different workload:
**0% of the top-500 Ads LRMs train in FP8; 1% serve in FP8, by PTQ.** Set side by side they
give the survey a claim it cannot get from any accelerator paper — that **hardware low-precision
capability has run far ahead of workload adoption, and stayed there for five years** — and LoKA
is the paper that itemises what closing the gap costs: a profiler, three architecture edits, a
dispatch runtime and a retrain.

**With RaPiD it establishes that quantization overhead is first-order, on two different
substrates.** RaPiD measured that only 50% of cycles go to quantized matrix math (17% at INT4)
on its own die. LoKA measures **>30% of end-to-end GEMM latency spent on quantization overhead**
on a GPU, that end-to-end FP8 speedup is capped at **1.6×** against a 2.0× FP8:BF16 peak-FLOPs ratio on H100 (Table I: 1,671 vs 840 TFLOPS), and
that with layout/allocation overhead **FP8 can be net slower than BF16**. Same finding from a
datapath and from a kernel; together they are the corpus's strongest evidence that "the format
is cheaper" and "the workload is faster" are different claims.

**On the Level axis it is the cleanest test of the human's 2026-09-09 `SYS` ruling.** LoKA
designs no hardware whatsoever, and its contribution is precisely the thing that *drives*
hardware: a profiler, a runtime, framework plug-ins and a kernel-dispatch layer. Within the
ISCA corpus only three rows have no `ARCH` at all — LoKA, [`ENEC`](../ENEC/ANALYSIS.md) and
[`Gist`](../Gist/ANALYSIS.md) — and **LoKA is the only `Q-ORIENTED` one of the three.** In our
own `TAGS.md` matrix, LoKA and Gist are the only two papers without the `accelerator` tag.

**On the granularity axis it makes a move nothing else makes.** The corpus's ladder runs
per-layer → per-region → per-channel → per-group → per-head → per-token → per-rank, and every
rung is a *design-time* decision. LoKA does not occupy a rung: it **selects one per operator at
runtime**, from {tensorwise, rowwise, blockwise} × {TorchAO, DeepGEMM, FBGEMM}, forward and
backward independently, and shows that the best uniform choice loses to the mixed one
(1.08× → 1.12×) while two uniform choices are *slowdowns*. The nearest neighbour is
[`NDPLowBitFP`](../NDPLowBitFP/ANALYSIS.md), which also treats granularity cost as a
compiler/scheduling problem rather than a format problem.

**BlockNorm inverts the usual co-design direction, and pairs with the MX line.** Everywhere
else in the corpus the *format* is reshaped to fit the model's statistics. Here the **model** is
reshaped to fit the hardware's block structure — normalization is redefined over 256-element
blocks because that is what fits in a GEMM thread block, and the paper says outright that this
"aligns closely with emerging Microscaling (MX) hardware standards, which utilize block-shared
scaling". Read against [`MXFFP`](../MXFFP/ANALYSIS.md), which designs the block format, LoKA is
the same idea approached from the model side.

**On the outlier-currency axis it adds a currency: normalization scope.** LoKA has no outlier
mechanism, but BlockNorm buys outlier *containment* — an outlier can only suppress the 256
features that share its statistic instead of the whole layer — and pays for it in **mathematical
non-equivalence with the original model**, which is why the model must be retrained. Every other
entry pays in bits, a destroyed neighbour, a second datapath, compressibility or a runtime
budget; this one pays in the model's own definition.

**On the retraining axis it is a fourth category.** Not PTQ, not QAT, not
alternating-structure-preserving retraining — the paper's own **DLP**: native low precision
throughout, with the architecture edited to make it survivable and the whole model trained from
scratch. Same practical consequence as [`SmartExchange`](../SmartExchange/ANALYSIS.md) and
[`Phi`](../Phi/ANALYSIS.md) — **a stock checkpoint cannot be consumed** — reached from the
opposite direction.

**Workload.** The corpus's only recommendation-model entry, and its only entry where the
memory story (embedding tables) and the quantization story (dense GEMMs) are **disjoint**. Every
LLM entry here quantizes the thing that dominates memory; LoKA quantizes the thing that dominates
FLOPs and leaves 100% of the parameters alone. That is worth one sentence wherever the survey
claims quantization is a bandwidth argument.

---

## For the note

**§1 one-line summary.** Meta's production answer to "why has nobody shipped FP8 for
recommendation models": leave the sparse embedding tables — essentially all 257 B–1.34 T
parameters — untouched and put only the dense/interaction GEMMs into **FP8** (sub-format never
named), then make that survivable by **learning each layer's real input distribution online and
replaying it offline to measure per-layer error against TF32** (random-tensor benchmarks
under-report it by up to 15%, and hid a real FBGEMM bug that Probe-generated inputs exposed at
47×), by **editing the model** — biases removed except in the prediction head, LayerNorm →
RMSNorm over fixed 256-element blocks that fit a GEMM thread block and fuse into its epilogue,
Swish → Hard Swish — and by **dispatching tensorwise/rowwise/blockwise recipes across three
kernel libraries per operator and per direction**; the hardware is stock H100/B200/GB200/
MI300X/MI350X and what it gets is **5–20% training and 10–17% inference throughput in
production**, quality-neutral on relative log loss where 0.02% is significant.

**Proposed tags.**

| Axis | Proposed | Evidence, one line |
|---|---|---|
| **Level** | `ALGO+SYS` (agrees with the seed) | No hardware exists in this paper; the deliverable is a PyTorch autograd adapter + init-time layer-rewriting pass + kernel-dispatch runtime over TorchAO/DeepGEMM/FBGEMM (§III-C pp.8–9), and `ALGO` is earned by LoKA Probe's per-layer sensitivity analysis and the Mods' model redesign (§III-A, §III-B). |
| **Q-oriented** | `Q-ORIENTED` (agrees with the seed) | Every component is conditioned on the format: the Probe's output is MERE of an FP8 kernel against TF32, the Mods are motivated by FP8 range and stability (§III-B), and Dispatch chooses among FP8 recipes. Remove quantization and there is no paper. |
| **Data type** | `FP8` `BF16` `TF32` `MIXED` (seed plus `TF32`) | FP8 is the compute format throughout; BF16 is the collectives format "regardless of compute datatype" (§IV-A p.9) and the Fig. 3 baseline; **TF32 is the escape-hatch and reference precision** — the MERE reference (§II-C p.3) and 95% of the training fleet (Table III p.4); `MIXED` because Dispatch mixes precisions per operator *and per direction*. |
| **Generation** | `G2` (agrees with the seed) — **but see the disagreement note** | Placed by the outline's **§4.6 mixed-precision search (per-layer sensitivity)** and **§4.7 shrinking granularity**, which is exactly Probe + Dispatch, and by the BlockNorm/MX co-design of block granularity with the datapath. It fails TAXONOMY's literal G2 test — LoKA designs neither a numeric type nor an architecture — so a `G1` reading is defensible. |

**Proposed row for `venues/ISCA/README.md`** (report only — do not apply):

```
| [x] | [LoKA: Low-precision Kernel Applications for Recommendation Models At Scale](https://doi.org/10.1109/ISCA66397.2026.00103) | [**human ✓**](notes/loka.md) | ALGO+SYS | Q | `FP8` `BF16` `TF32` `MIXED` | G2 | `production deployment` `FP8 training` `recommendation models` `distribution-aware profiling` `per-layer sensitivity` `per-operator kernel dispatch` `model-hardware co-design` `BlockNorm` `bias removal` `Hard Swish` `GPU` `PyTorch` | Dense/interaction GEMMs to FP8; **embedding tables — nearly all the parameters — untouched**. Probe learns the real input distribution because random-tensor benchmarks under-report error; Mods rewrite the model so FP8 is safe; Dispatch picks library+recipe per operator and per direction. **Production: 5–20% training, 10–17% inference** — not the abstract's 20%/40% |
```

**§4 fairness verdict (for the note's last table row).**

> **Iso-hardware, iso-data, iso-model-scale** (same production models, data and clusters);
> **not iso-baseline** — quality is measured against the unmodified model, speed against the
> Mods-rewritten one; **not iso-checkpoint** (DLP retrain, no stock weights). No hardware, so
> iso-area/node do not apply. **Do not quote 40% inference or 20% training as production**:
> §V says **10–17% / 5–20%**. Prose says 1.19×, Fig. 10 shows 1.26×.

---

## Abstract (verbatim, ISCA 2026 proceedings)

> Recent GPU generations deliver significantly higher FLOPs using lower-precision
> arithmetic, such as FP8. While successfully applied to large language models (LLMs), its
> adoption in large recommendation models (LRMs) has been limited. This is because LRMs are
> numerically sensitive, dominated by small matrix multiplications (GEMMs) followed by
> normalization, and trained in communication-intensive environments. Applying FP8 directly
> to LRMs often degrades model quality and prolongs training time. These challenges are
> inherent to LRM workloads and cannot be resolved merely by introducing better FP8 kernels.
> Instead, a system-model co-design approach is needed to successfully integrate FP8. We
> present LoKA (Low-precision Kernel Applications), a framework that makes FP8 practical for
> LRMs through three principles: profile under realistic distributions to know where low
> precision is safe, co-design model components with hardware to expand where it is safe, and
> orchestrate across kernel libraries to maximize the gains. Concretely, LoKA Probe is a
> statistically grounded, online benchmarking method that learns activation and weight
> statistics, and quantifies per-layer errors. This process pinpoints safe and unsafe, fast
> and slow sites for FP8 adoption. LoKA Mods is a set of reusable model adaptations that
> improve both numerical stability and execution efficiency with FP8. LoKA Dispatch is a
> runtime that leverages the statistical insights from LoKA Probe to select the fastest FP8
> kernel that satisfies the accuracy requirements. Deployed on production LRMs that serve
> billions of users with advertising recommendations at a major social media company, LoKA
> delivers up to 20% higher training throughput and 40% faster inference on heterogeneous
> GPUs (H100, B200, GB200, MI300X and MI350X) in production environment, with no quality
> loss, turning FP8 from a model-quality risk into a reliable performance lever for LRMs at
> scale.
