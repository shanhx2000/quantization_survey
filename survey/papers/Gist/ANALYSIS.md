# Gist — paper notes

**Gist: Efficient Data Encoding for Deep Neural Network Training**
Animesh Jain, Amar Phanishayee, Jason Mars, Lingjia Tang, Gennady Pekhimenko
**ISCA 2018**, pp. 776-789 ｜ DOI: **10.1109/ISCA.2018.00070**
Publication info verified 2026-09-02: **the archived PDF carries no DOI and no IEEE banner**
(grepped, not assumed) — venue and title come from its own page 1; **DOI and page range come
from the ACM DL record surfaced via search**, and are second-hand.
Archived here: an **author-hosted copy, not the IEEE version** — no IEEE proceedings banner on page 1, and the filename is the author's.
The two versions were **not compared**. 14 pages; PDF creation timestamp 2018-05-04, i.e. camera-ready-or-earlier.
**Cite the DOI and the page range with care — neither appears in the file we hold.**

Status: **note ready** ｜ Last updated: 2026-09-14 ｜ **Human ruling 2026-09-14:** `Q-ORIENTED`, resolving the partial dissent below in favour of DPR — consistent with the `ENEC` ruling that a design *conditioned on the float format* is Q-oriented. ｜ **Human-checked 2026-09-14** — tags confirmed, including the seed dispute `Data type: —` → `FP32` `FP16` `FP10` `FP8` `MIXED` (the paper specifies E4M3 in 2018) and `Generation: —` → `G2`.
Tags: `training` `gpu-kernels` `lossless-compression`
How far it was read: **close read of §I-§VII in the `-layout` extraction, plus every figure
caption and the reference list.** Line by line: §II (memory breakdown), §III (the three
opportunities), §IV-A (all three encodings, in full), §IV-B (Schedule Builder), §IV-C (CNTK
allocator and the Figure 7 worked example), §V-A through §V-H (every subsection), §VI, §VII.
**What could not be resolved, and is flagged in place below:**
(i) **Figures 8-17 are vector plots whose bar labels `pdftotext` recovers as an unordered
set** — Fig. 10's totals (`1.04×…1.65×`, 20 values) and Fig. 11's (`16×, 16.8×, 16×, 16×,
14.6×`) cannot be attached to a specific CNN, so **only values the prose names explicitly are
attributed here**; the rest are given as ranges.
(ii) **Figure 12 is a scatter plot.** The accuracy curves are dots; the only readable facts
are the caption's per-network minimum precision and the axis ranges (90 epochs; 50 for
Inception). **No accuracy number for any Gist configuration exists anywhere in the text.**
(iii) The Binarize `≈16×` category ratio does **not** reconstruct from the paper's own
`32× ReLU output / 8× pool output` plus `pool = N/4 or N/9` — my arithmetic gives 20-25×. Use
the measured Fig. 11 range (14.6-16.8×); the discrepancy is unexplained and I did not resolve it.

> Publisher record: https://doi.org/10.1109/ISCA.2018.00070
> **There is no arXiv version** (arXiv API title search, 2026-09-02). The PDF was downloaded by a
> human and filed through [`survey/uploads/`](../../uploads/) — the sanctioned route when the
> arXiv-only rule leaves a paper unreachable; see
> [`Notes-002`](../../../Claude/notes/Notes-002-paper-source-access.md).
> The PDF is **not committed** (0.4 MB) and **cannot be re-downloaded by script** —
> both publishers 403. Re-extract with `python3 extract.py` → `extracted/` (committed).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, ISCA 2018 row.

---

## Brief

### 1. Motivation

In DNN *training* — unlike inference — the memory bottleneck is not weights but **feature
maps** stashed in the forward pass for reuse in the backward pass. Prior compression work
targeted weights and therefore barely helps training.

### 2. Overview

A layer-aware encoding framework inside CNTK. The key structural observation is that a
feature map has two uses separated by a long temporal gap: keep it full-fidelity for the
immediate forward use, store an **encoded** form across the gap, decode for the backward
pass. Two encoding classes: lossless (e.g. exploiting that a ReLU→Pool feature map needs
only **1 bit instead of 32** given how backprop uses it) and lossy (delayed precision
reduction).

### 3. Pros and cons

**Pros**

- The insight is exact, not statistical: the 1-bit ReLU-Pool encoding is *lossless* because
of what backpropagation actually reads — a rare case of compression with no accuracy
question at all.
- Pure software on a stock GPU stack: 2× footprint reduction (1.8× average across 5 CNNs)
for ~4% performance overhead, with no hardware changes.
- Separating lossless from lossy encodings lets the accuracy risk be confined to the part
that carries it.

**Cons**

- CNN-specific: the encodings are derived from convolution/ReLU/pool semantics and do not
transfer to transformer training as-is.
- 1.8× average is modest next to what quantization achieves elsewhere; the paper's larger
4.1× figure depends on further software and hardware changes it does not implement.
- The source list marks this **"Less related"** — it is memory-footprint compression, not
quantization, and sits outside the scope taxonomy.

### 4. Where it applies

Background for the **training** and **compression-not-quantization** clusters. Its real
value to the survey is the lossless/lossy split and the observation that training and
inference have different bottlenecks.

---

## Corrections to the brief

**What the close read changed.** The brief was broadly right; four things are sharper or different.

1. **Binarize is not "1 bit instead of 32" on its own.** It is 1 bit for the ReLU output
   **plus a newly invented 4-bit-per-element MaxPool argmax map** (`YtoXmap`), without which
   pool's backward pass would still need the values. The brief quotes the abstract, not the
   mechanism. **verified** (§IV-A, p. 5).
2. **Three encodings plus a fourth optimization, not two classes.** Binarize (lossless), SSDC
   (lossless), DPR (lossy), and *inplace computation* — which targets a different tensor class
   (immediately-consumed data, not stashed) and is credited to prior work [4]. **verified**
   (Table I, p. 4; §III-C, p. 5).
3. **"2× footprint reduction" is a maximum.** The result is **1.8× average, up to 2×
   (AlexNet)**. **verified** (abstract; §V-B, p. 8).
4. **"Pure software on a stock GPU stack" understates the dependency.** The reduction is
   realised *by the CNTK static memory allocator's lifetime-sharing groups*, not by the
   encoding ratio: a 16× encoding yields **1.26×** total footprint on AlexNet, and encoding
   **increases** immediately-consumed memory. **verified** (§IV-B/§IV-C, Fig. 7, p. 7-8;
   §V-C1, p. 9).

The cons stand. The "outside the scope taxonomy" line needs the qualification in
`Relation to other entries`: **one of the three encodings is a quantization mechanism.**

---

## Conclusions

**Read in full.** Two findings dominate this entry's value to the survey.

- **The compute datapath never sees a narrowed value as an arithmetic operand.** Every
  multiply-accumulate in Gist runs FP32 through unmodified cuDNN. **verified**: "The
  computation still happens in FP32 format while the data is stored with lower precision for
  most of its lifetime… we convert back to FP32 because cuDNN is closed-source library"
  (§IV-A, p. 6); "for DPR encodings, we decode the data back into FP32 format, because cuDNN
  library requires data to be in the FP32 format" (§V-H, p. 12).
  **The one exception, and it needs stating precisely:** for **Binarize**, Figure 6's decode
  column reads **"Work on encoded data"**, and "Pool and ReLU backward pass have been updated
  to perform computation on the encoded data structures itself" (§IV-A, p. 5). But that
  computation is `dx = (y>0) ? dy : 0` — a **predicate** — plus a scatter through the argmax
  map. Control, not operands. **verified** (Fig. 4b/4c, p. 4; Fig. 6, p. 5).
- **DPR is a quantization mechanism inside a paper that disclaims quantization.** It defines
  three narrow float formats (one of them **E4M3**) and applies them to a real tensor class
  with rounding, clamping and dropped denormals. The paper's own framing puts distance
  between itself and the word: "we investigate precision reduction as it is amenable to GPU
  architecture compared to prior offline approaches like quantization and Huffman encoding
  [18]" (§III-B, p. 4). **verified.**

---

## Method

### The structural claim (§III, p. 3-4)

A stashed feature map has exactly **two** uses, far apart: once in the forward pass, once in
the backward pass, and in the baseline it is held FP32 for the whole interval. Gist splits
that lifetime into **three**: FP32 live only for the immediate forward use → **encoded** for
the temporal gap → FP32 (decoded) live only for the immediate backward use. **verified**
(Fig. 2, p. 3; §IV-B, p. 7).

The motivating breakdown (§II-A1, Fig. 1, p. 3): stashed feature maps + immediately-consumed
data are **83% of footprint for VGG16 and 97% for Inception**; weights are a small fraction.
Within stashed feature maps (Fig. 3, p. 4), VGG16 is **40% ReLU-Pool + 49% ReLU-Conv = 89%
ReLU output**. **verified.**

### The three encodings, separated by kind

| # | Encoding | Layer pair | Lossless / lossy | What is actually stored | Compression |
|---|---|---|---|---|---|
| 1 | **Binarize** | **ReLU → Pool** | **Lossless** | (a) ReLU output as a **1-bit sign predicate**; (b) a new **`YtoXmap`** argmax index, **4 bits** per *pool-output* element (4 bits suffices because the largest window in the suite is 3×3) | **32×** on the ReLU output, **8×** on the pool output; **≈16×** on the category (measured **14.6-16.8×**) |
| 2 | **SSDC** (Sparse Storage, Dense Compute) | **ReLU → Conv**, and **Pool → Conv** where the preceding ReLU is sparse | **Lossless** | **CSR** over the 2-D-collapsed tensor: non-zero values + column indices. **Narrow Value Optimization** reshapes to ≤256 columns so an index is **1 byte, not 4** | Data-dependent, **up to 7×** (Overfeat). Break-even sparsity **50% → 20%** after the index change |
| 3 | **DPR** (Delayed Precision Reduction) | **any layer** — the "Other" stashed feature maps, and *composed on top of SSDC's non-zero value array* | **LOSSY** | **FP16** = IEEE half (1s/5e/10m); **FP10** = 1s/**5e/4m**; **FP8** = 1s/**4e/3m**. Packed **2 / 3 / 4** values per 4 bytes; round-to-nearest; clamped at format max/min; **denormals ignored** | **2× / 3× / 4×** on the stashed feature maps |
| — | *Inplace computation* | ReLU (read-once, write-once) | Lossless, no encoding | Conv's output buffer is reused by ReLU | **up to 1.4×** on immediately-consumed data (AlexNet) |

All **verified** (§IV-A, p. 5-6; Fig. 6, p. 5; Fig. 11, p. 9; Fig. 13, p. 10).

**The lossy/lossless boundary is drawn on a principle worth quoting.** DPR is applied to
SSDC's *value* array but **not** to its index array and **not** to Binarize's masks — "we do
not touch the meta array in CSR format and Binarize encoded data structures as these affect
**control**, and thus are not suitable for lossy encoding" (§IV-A, p. 6). **verified.**

### Why *delaying* the reduction is the contribution

Prior practice reduces precision **immediately after a layer produces a value**, so the
rounding error is injected into the next layer and propagates through the forward pass. Gist
keeps the forward copy FP32 and narrows **only the copy stashed for the backward pass**, so
**no error ever enters the forward pass**. That is why uniform All-FP16 diverges while
Gist-FP8 does not. **verified** (§III-B, p. 4; §IV-A, p. 6; §V-D1, p. 10).

### The software stack (this is what makes the Level tag `SYS`)

- **Schedule Builder** — a pass over CNTK's execution graph: identify which edges admit which
  encoding, insert encode/decode nodes, emit a new graph. **verified** (Fig. 5, p. 5; §IV-B).
- **Static liveness analysis** of the three sub-lifetimes, handed to the **CNTK static memory
  allocator**, which groups non-overlapping lifetimes onto one buffer. **verified** (§IV-B/C, p. 7).
- **CUDA kernels** for every encode/decode; **cuSPARSE** for CSR; a **rewritten MaxPool
  backward**. cuDNN and the conv kernels are untouched. **verified** (§IV-A, p. 5-6; §V-A, p. 8).
- Figure 7 is the mechanism in miniature: a 5× encoding on one 10 MB tensor moves total
  footprint **18 MB → 12 MB**, because stashed drops 10 → 2 while immediately-consumed
  **rises** 8 → 10. **verified** (p. 8).

---

## Key numbers, with their frame

Two baselines are in play and **must not be mixed**. **CNTK baseline**: original static
allocation, footprint counted over stashed feature maps + immediately-consumed data **only**
— weights, weight gradients and cuDNN workspace are excluded. **Investigation baseline**: the
same, but memory sharing is disabled for stashed feature maps, to isolate one encoding.
MFR = baseline footprint ÷ encoded footprint. **verified** (§V-A, p. 8).

| Setting | Model | Metric | Baseline | Result | Source |
|---|---|---|---|---|---|
| Lossless only (Binarize+SSDC+inplace) | 5 CNNs | MFR | CNTK | **1.4× avg**; >1.5× AlexNet and VGG16 | §V-B, Fig. 8, p. 8 |
| **Lossless + DPR (headline)** | 5 CNNs | MFR | CNTK | **1.8× avg, 2.0× max (AlexNet)** | Abstract; §V-B, Fig. 8, p. 8 |
| Perf overhead, lossless | 5 CNNs | minibatch time | CNTK, memory-optimal cuDNN | **3% avg** | §V-B, p. 8 |
| **Perf overhead, lossless+lossy** | 5 CNNs | minibatch time | same | **4% avg, 7% max (VGG16)** | §V-B, p. 8-9 |
| Perf overhead, DPR alone | 5 CNNs | minibatch time | same | **1% avg** | §V-D3, p. 10 |
| Perf, Binarize alone | 5 CNNs | minibatch time | same | **small speedup** — ReLU backward is bandwidth-bound; no number given | §V-C2, p. 9 |
| Perf, SSDC alone | 5 CNNs | minibatch time | same | up to **4%** overhead | §V-C2, p. 9 |
| Binarize on its category | 5 CNNs | category MFR | **investigation** | **14.6-16.8×** (Fig. 11 label set; prose says "close to 16×") | Fig. 11, p. 9 |
| SSDC on its category | 5 CNNs | category MFR | **investigation** | **up to 7× (Overfeat)**; varies widely across CNNs | Fig. 11, p. 9 |
| Inplace | AlexNet | category MFR | **investigation** | **up to 1.4×** | Fig. 11, p. 9 |
| Lossless stack, cumulative | AlexNet | total MFR | **investigation** | S **1.06×** → B **1.26×** → S+B **1.35×** → S+B+I **1.56×** | §V-C1 prose + Fig. 10, p. 9 |
| DPR, stashed feature maps only | 5 CNNs | stashed-FM ratio | **investigation** | **FP16 2×, FP10 3×, FP8 4×** | Fig. 13, p. 10 |
| DPR, total | AlexNet | total MFR | **investigation** | **FP16 1.18×, FP8 1.48×** | §V-D2, p. 10 |
| Minimum DPR width, no training-accuracy loss | AlexNet, Overfeat | bits | FP32 | **FP8** (1s/4e/3m) | Fig. 12 caption, p. 10 |
| " | Inception | bits | FP32 | **FP10** (1s/5e/4m); **at FP8 "the network stops training"** | Fig. 12 caption + §V-D1, p. 10 |
| " | VGG16 | bits | FP32 | **FP16**; does not train below | Fig. 12 caption + §V-D1, p. 10 |
| Uniform All-FP16 (every data structure; compute still FP32) | 4 CNNs | training accuracy | FP32 | **"severe accuracy losses"** — **no number given anywhere** | §V-D1, Fig. 12, p. 10 |
| vs prior work | 5 CNNs | slowdown | CNTK | naive swap **30% avg**; **vDNN 15% avg / 27% max (Inception)**; **Gist 4% avg / 7% max** | §V-F, p. 11 |
| Largest minibatch that fits in 12 GB | Resnet-509 / 851 / 1202 | minibatch | CNTK | **32→64 / 16→32 / 8→16** | Fig. 16, p. 11 |
| Training speedup from the bigger minibatch | Resnet-1202 | throughput | CNTK at its largest fitting minibatch | **22%** | §V-G, p. 11 |
| Simulated dynamic allocation, alone | 5 CNNs | MFR | CNTK | **1.2× avg**, >1.5× Overfeat | §V-H, p. 12 |
| Dynamic + Gist lossless | 5 CNNs | MFR | CNTK | **1.7×** | §V-H, p. 12 |
| Dynamic + full Gist | 5 CNNs | MFR | CNTK | **2.6×** | §V-H, p. 12 |
| **Dynamic + full Gist + "optimized software"** | 5 CNNs | MFR | CNTK | **2.9× avg, 4.1× max (AlexNet)** — **a projection, see hazard 2** | §V-H, Fig. 17, p. 12 |
| Footprint composition | VGG16 / Inception | share of total | — | stashed + immediately-consumed = **83% / 97%** | §II-A1, Fig. 1, p. 3 |
| ReLU share of stashed FMs | VGG16 | share | — | **40% ReLU-Pool + 49% ReLU-Conv = 89%** | §III-A, Fig. 3, p. 4 |
| ReLU output sparsity | VGG16 | sparsity | — | **>80% across all ReLU outputs** | §III-A, p. 4 |
| Sparse *compute* break-even on GPU | — | sparsity | — | **>97.5%** before sparse GEMM wins — the reason SSDC keeps compute dense | §IV-A, p. 5 |
| CSR index width | — | min useful sparsity | cuSPARSE default 4-byte index | **50% → 20%** with 1-byte indices (≤256 columns) | §IV-A, p. 6 |
| SSDC stability over training | VGG16, 11 layers, 15 epochs | MFR over time | — | "much larger than 1" except the first **~200 minibatches** of epoch 1 (an epoch is 20K minibatches) | §V-E, Fig. 14, p. 11 |

**Evidence level: real-system measurement**, uniformly, with two exceptions.
Hardware: **Nvidia Maxwell GTX Titan X, 12 GB GDDR5**, cuDNN v6.0, CUDA 8.0, CNTK, ImageNet;
timing is a minibatch averaged over 5 minutes of training. **verified** (§V-A, p. 8).
The exceptions are both in §V-H: **dynamic allocation is simulated** ("we modify the liveness
analysis module from CNTK and **simulate** dynamic memory management") and the "optimized
software" row is **analytical** (the decoded FP32 buffer is deleted from the liveness model;
no cuDNN change exists). **verified** (§V-H, p. 12).
**There is no RTL, no synthesis, no area and no energy number in the paper** — greps: `area`
0 hits, `RTL` 0 hits, `simulat` 1 hit (the above), `energy` 3 hits, all qualitative arguments
against PCIe swapping. **verified.**

### Citation hazards

1. **`2×` is a maximum; the result is `1.8×` average.** Both are in the abstract; 2× is the
   one that gets quoted. **verified.**
2. **`4.1×` is not Gist.** It is Gist + a **simulated** dynamic allocator + a **hypothetical**
   cuDNN that consumes encoded data directly — neither implemented — and it is the AlexNet
   maximum of a **2.9× average**. The paper is honest about this; a citation that drops the
   qualification is not. **verified** (§V-H, p. 12).
3. **Category ratios and end-to-end ratios have different baselines.** 16× / 7× / 1.4× are
   against the **investigation** baseline (sharing disabled for stashed FMs); 1.4× and 1.8×
   are against the **CNTK** baseline. Never put them in one sentence. **verified** (§V-A, p. 8).
4. **MFR covers a subset of GPU memory.** Weights, weight gradients and cuDNN workspace are
   excluded from numerator and denominator. "2× memory footprint reduction" is 2× on 83-97%
   of the footprint for VGG16/Inception, less for the smaller nets. Declared, and justified as
   in line with vDNN. **verified** (§V-A, p. 8).
5. **"No effect on training accuracy" is training-curve overlap, per network, with the
   bitwidth tuned per network.** There is **no validation or test accuracy anywhere** —
   greps: `validation` 0, `top-1` 0, `top-5` 0, `test` 0, `converge` 0. The evidence is a
   scatter plot of *training* accuracy over 90 epochs (50 for Inception) overlapping the FP32
   curve. **The paper never states a final accuracy figure for any configuration.** **verified.**
   **And it is contradicted second-hand**: [`JPEG-ACT`](../JPEG-ACT/ANALYSIS.md)'s Table I
   prices its re-implementation of "GIST 8-bit" at **−1.07% Top-1** for 4.5×. Second-hand,
   another paper's re-implementation — but it is the only accuracy number about Gist that
   exists, and it is not zero.
6. **"As small as 8 bits" is AlexNet and Overfeat only.** Inception needs FP10 and **fails to
   train at FP8**; VGG16 needs FP16. The paper says so: "the minimum acceptable precision is
   network dependent". **verified** (§V-D1, p. 10).
7. **The 22% Resnet-1202 number is a minibatch-size effect, not a compute speedup** — 8 → 16
   images per batch raises GPU utilisation. Resnet does not appear in the 5-CNN MFR figures.
   **verified** (§V-G, p. 11).
8. **The vDNN comparison is the authors' own reimplementation in CNTK**, not the MICRO'16
   artifact. **verified** (§V-F, p. 11).
9. **The 4% overhead is measured against the *memory-optimal* cuDNN configuration**, which
   §II describes as a performance/workspace tradeoff. So the overhead is relative to an
   already slower baseline. **verified** that memory-optimal is the baseline and that it is a
   tradeoff (§II-A1, p. 3; §V-A, p. 8); **inferred / not verified** by how much — the paper
   gives no performance-optimal datapoint.
10. **DOI and page range are second-hand** (see header). The archived file carries neither.

---

## Cost and requirements

- **Hardware cost: none.** No accelerator, no RTL, no area, no power. A stock Maxwell GPU.
- **Software cost: a framework fork.** Encode/decode CUDA kernels, a modified ReLU backward, a
  **rewritten MaxPool backward** (it must now build and consume `YtoXmap` instead of the
  stashed input/output feature maps), a graph-rewriting pass, a liveness analyser and changes
  to CNTK's static memory allocator. Not a library you link — a framework you patch.
- **Memory cost paid back.** Encoding **adds** live bytes: the FP32 forward copy, the encoded
  copy, and later the decoded FP32 copy. The net win exists only because the allocator can
  share the short-lived FP32 buffers; Fig. 10 shows immediately-consumed footprint **rising**
  in every configuration. **verified** (§IV-B, §V-C1).
- **Runtime cost:** 3% (lossless) / 4% (lossless+lossy) average, 7% worst case (VGG16).
- **Calibration / retraining: neither, and it is not PTQ either.** No calibration set, no QAT;
  the network trains from scratch as before, with narrowed *stashed* values, and the converged
  model that comes out is a plain FP32 model. The encoding exists only during training. **verified.**
- **A tuning requirement the paper understates:** the DPR bitwidth is found empirically per
  network by training to convergence at each candidate width. For a new network that is
  several full training runs.
- **Applicability requirement:** a ReLU + MaxPool + Conv topology with high ReLU sparsity. The
  argmax map assumes windows ≤ 3×3 (4 bits); SSDC needs ≥20% sparsity to pay.

---

## Limitations and open questions

**The authors state:**
- The minimum DPR precision is network-dependent and must be found empirically (§V-D1).
- DPR must decode to FP32 because cuDNN is closed source; pulling the decode inside cuDNN, or
  tiling it, would remove the decoded buffer and raise MFR (§IV-A, §V-H).
- Static allocation is the framework's choice; dynamic allocation would help further and would
  want hardware support (§V-H).
- SSDC's ratio is data-dependent and near 1 for the first ~200 minibatches (§V-E).
- Recompute [4] is orthogonal and composable (§II-B).

**They do not state:**
- **No validation or test accuracy is ever reported** — only training-accuracy curves. For a
  method whose entire safety argument is "the converged model is unchanged", the experiment
  that would establish it (final top-1/top-5 against an FP32 run) is absent. **This is the
  biggest gap in the paper**, and the thing to say when citing its accuracy claim.
- **No number for the All-FP16 "severe accuracy loss"** it is contrasted against.
- `YtoXmap` changes MaxPool's backward *algorithm*, not just its storage; ties and numerical
  edge cases in argmax selection are never discussed.
- **Average pooling is never mentioned.** Binarize's premise is MaxPool's argmax; the encoding
  does not obviously extend to it.
- **No transformer, no RNN, no non-vision workload** — six CNNs, all ImageNet classification.
- No multi-GPU or distributed result, despite the PCIe-contention argument against vDNN.
- No energy number, despite arguing that vDNN's PCIe traffic costs energy.
- The interaction between DPR's rounding and *sparsity* is not examined: DPR is applied to
  SSDC's value array, so small values may round to zero and change the CSR structure.
- **No scale factor of any kind.** DPR reduces the float fields directly, so a channel whose
  activations span 0.16 uses a sliver of the representable range. The paper never asks whether
  a per-tensor or per-channel scale would buy bits; `JPEG-ACT` later shows it buys a lot.
- **No released code** — `JPEG-ACT` had to re-implement the whole system to compare.

**Open question worth recording for the survey.** Gist's accuracy claim is that a *lossy*
encoding applied to a tensor read only by the backward pass does not change the converged
model. The evidence is curve overlap on four CNNs. Nobody in this corpus has tested that claim
at transformer scale, and it is the precondition for every "compress the activation stash"
method. [`JPEG-ACT`](../JPEG-ACT/ANALYSIS.md), two years later, takes convergence seriously
enough to name it in its abstract — the right standard, and the one Gist does not meet.

---

## Relation to other entries

### The boundary question: where Gist sits on *compression vs cheaper arithmetic*

**Direct answer: the compute datapath never sees an encoded value as an arithmetic operand.**
All GEMM/conv runs FP32 through unmodified cuDNN; DPR decodes to FP32 before every use and
says so twice (§IV-A, §V-H). The one place encoded data is consumed directly is Binarize's
ReLU/MaxPool backward, where the 1-bit form is a **predicate** and the 4-bit form is an
**index** — control, not operands. Gist is unambiguously on the compression side.
**verified.**

But it is not at the same point as the other two, and the axis needs a **third term**:

| | `Ecco` | `ENEC` | **`Gist`** |
|---|---|---|---|
| What the compression buys | **L2/HBM bandwidth** + capacity | **PCIe/HBM transfer bandwidth** | **GPU DRAM capacity** — peak allocated bytes |
| Where the decode happens | between **L1 and L2** | on a **different core type** (AIV, not AIC) | in a **CUDA kernel**, one graph node before the consumer |
| Does the datapath see the encoded form? | No (FP16 to the SMs) | No (BF16 to the Cube) | **No for arithmetic; yes as a predicate** (Binarize) |
| Are values changed? | **Yes** (k-means codebook, lossy) | **No** (bit-identical) | **Both** — Binarize/SSDC lossless, **DPR lossy** |
| Tensor class | weights, activations, KV cache | weights, exponent field only | **stashed activations, training-time, with a lifetime** |
| Metric | ratio → speedup | ratio → TTFT | **peak footprint → a bigger minibatch** |

**The third term is the point.** Ecco and ENEC both buy bandwidth, and a compression ratio maps
onto their metric almost directly. Gist buys **capacity**, and a compression ratio does **not**
map onto peak footprint: a 16× encoding produces a 1.26× total reduction, because the payoff is
mediated by an allocator's lifetime-sharing groups and because the encoded copy coexists with an
FP32 copy at both ends. **Gist is the corpus's evidence that compression ratio ≠ memory saving
once an allocator is in the loop** — a caveat that reaches every weight-compression claim
reported as a ratio.

### `Q-oriented`: the test, applied honestly

Swap the format for plain INT8. What survives?
- **Binarize survives intact.** The 1-bit form comes from `dx = (y>0) ? dy : 0` — a fact about
  backprop, not about the format. Under INT8 it is 8× rather than 32×; the argmax map is unchanged.
- **SSDC survives intact.** CSR + Narrow Value Optimization + dense compute is a sparsity
  argument with no numeric content at all.
- **Inplace, the Schedule Builder, the liveness analysis and the allocator work survive intact.**
- **DPR does not survive.** It *is* the format: three narrow floats, rounding, clamping, dropped
  denormals, sub-word packing.

Most of the paper survives, and the lossless half alone delivers 1.4× of the 1.8×. Drafted
here as `NON-Q-ORIENTED`; **the human ruled `Q-ORIENTED` on 2026-09-14**, resolving the dissent
below in favour of DPR. The reasoning is kept because it is why the call was close. The human's 2026-09-14 ruling on [`ENEC`](../ENEC/ANALYSIS.md) — `Q-ORIENTED` because
"the design is conditioned on the float format" — cuts the other way for DPR specifically,
which is conditioned on the format down to the exponent/mantissa split. **Taken alone, DPR
would be `Q-ORIENTED`.** Recorded, not resolved.

### The quantization fact worth extracting regardless of the box

**Gist's FP8 is 1 sign / 4 exponent / 3 mantissa — E4M3 — in 2018**, and at that width AlexNet
and Overfeat match FP32 training accuracy. FP10 is 1s/5e/4m. Both are custom formats designed
for this paper and packed 4-per-word and 3-per-word. That predates H100's FP8 by five years and
predates every FP8 entry in this corpus. **verified** (§IV-A, p. 6). Whatever box Gist ends up
in, that sentence belongs in the survey's FP8 lineage.

### Against `JPEG-ACT` (ISCA'20) — the direct successor, and Gist's only third-party audit

[`JPEG-ACT`](../JPEG-ACT/ANALYSIS.md) (close read completed 2026-09-14, in parallel with this
one) targets the same tensor class and inverts every choice: **new RTL at the DMA engine** vs
software in the framework; **offload to CPU memory over PCIe** vs keep it in GPU memory;
**spatial correlation + a per-channel INT8 quantizer** vs sparsity + raw float truncation;
**lossy by design with an explicit convergence objective** vs Gist's lossless-first split. It
**adopts Binarize unchanged** (it calls the 1-bit ReLU sign mask **BRC**) and replaces DPR and
SSDC with SFPR.

**Three second-hand facts about Gist come from it, and they are the most useful things any
other entry says about this paper.** All are *JPEG-ACT's* measurements of its own
re-implementation of Gist, **not Gist's numbers** — mark them second-hand wherever they are used:

1. **Gist costs accuracy.** JPEG-ACT's Table I prices "GIST 8-bit" at **4.5× compression,
   −1.07% Top-1**, against JPEG-ACT's 8.5× / −0.38%. Gist's own paper reports **no accuracy
   number at all** and claims no effect. **The only quantitative accuracy statement about Gist
   in this corpus comes from a competitor, and it is not zero.** Treat Gist's "no effect on
   training accuracy" as unaudited by the authors and contradicted second-hand.
2. **Why DPR is weak, in quantization terms.** JPEG-ACT §VI-B: on the ResNets the minimum
   per-channel activation range is 0.16, so DPR uses **15% of the 256 available codes against
   SFPR's 66%**. That is exactly the diagnosis this survey would make — **DPR has no scale and
   no group, so it cannot follow the per-channel dynamic range**. It is a format substitution,
   not a quantizer with a calibration constant, and the cost is measurable.
3. **Gist has no public source.** JPEG-ACT had to rebuild DPR, BRC, SSDC and the inplace
   optimizations to compare against it.

Their agent's independent conclusion matches this one on the axis: *"Compressed activations are
not kept in HBM, only shipped over PCIe… So this buys interconnect, not GPU memory capacity —
GIST buys the opposite."*

### Against `SpZip` / `CommutativeDataReordering`

Not the same kind of paper: those compress structure, with no numeric format in play. Gist
defines three named float formats. Following the argument [`ENEC`](../ENEC/ANALYSIS.md) makes
against sharing a box with `SpZip`, Gist should **not** inherit `SpZip`'s `—` on Data type.

### Where it sits on the corpus's existing axes

- **Retraining** — a fourth value beyond PTQ / QAT / alternating structure-preserving
  retraining: **training-time-only encoding**, where the narrow form exists during training
  and the shipped model is FP32. No other entry occupies this.
- **Granularity** — the degenerate case, and it is a finding rather than an omission: **no
  scale, no group, no calibration constant anywhere.** DPR narrows the exponent/mantissa fields
  of an FP32 value in place. `JPEG-ACT` measured what that costs — 15% code-space utilisation
  against 66% for a per-channel scale (second-hand). Gist is the corpus's zero point on the
  granularity ladder.
- **Compression vs cheaper arithmetic** — the **capacity** pole, distinct from Ecco's and
  ENEC's bandwidth. Order it: *arithmetic (everything else) → cache bandwidth (Ecco) →
  interconnect bandwidth (ENEC) → allocator capacity (Gist, and probably JPEG-ACT)*.
- **A new axis Gist opens: where in the dataflow the narrow form lives.** Gist's answer —
  "only in the interval where nothing reads it" — is the cleanest instance in the corpus;
  Ecco's "between L1 and L2" and ENEC's "on the vector core, never the Cube" are two more
  points on it. It is a *placement* axis, orthogonal to format, and Gist is its earliest member.

### The box question — explicit recommendation

**Do not give the seven no-box papers one box.** For Gist specifically:

1. **Keep the row.** Drafted `NON-Q-ORIENTED` on the taxonomy test, since the lossless half is
   most of the paper — **overruled to `Q-ORIENTED` by the human, 2026-09-14**, on the `ENEC`
   precedent.
2. **But move it out of "no box" and into a sub-box shared with `JPEG-ACT`:
   *training-time activation quantization*** — the object is a **backward-pass operand**, the
   accuracy criterion is **convergence** rather than a PPL/Top-1 delta on a fixed checkpoint,
   and the resource bought is **capacity or interconnect**, never arithmetic. Two entries with
   a direct lineage (JPEG-ACT reuses Binarize, re-implements DPR/SSDC and beats them 1.59×) is
   enough to be a paragraph, not a footnote. *(JPEG-ACT's agent proposed the same sub-box
   independently, on stronger grounds: its SFPR is an unambiguous per-channel INT8 quantizer,
   so JPEG-ACT should be tagged `Q-ORIENTED` and Gist should not — the sub-box holds one of
   each, which is the honest shape.)*
3. **Cite DPR by name in the survey's *placement* discussion, not its *format* discussion.**
   The transferable idea is "narrow the value only over the interval in which nothing reads
   it", and Gist is its earliest and cleanest instance.
4. **Cite the FP8 = 1s4e3m fact in the FP8 lineage** regardless of the box.
5. **Cite the compression-ratio-≠-footprint-reduction fact** wherever the survey reports a
   memory saving as a ratio.
6. That leaves the no-box list as `SpZip` + `CommutativeDataReordering` (no numeric format at
   all) and, if a lossless corner is wanted, `IBMCompressionAccelerator` with `ENEC`. `Ecco`
   has a real quantizer and belongs inside.

---

## For the note

### §1 one-line summary

> Training, not inference: the tensor is the **stashed feature map** that must survive from the
> forward pass to the backward pass, and Gist narrows it **only for that interval** — a **1-bit
> sign predicate** for ReLU→Pool (lossless, 32× on the ReLU output, plus a new 4-bit MaxPool
> argmax map so pool's backward pass no longer needs the values at all), **CSR storage with
> dense FP32 compute** for ReLU/Pool→Conv (lossless, up to 7×, break-even sparsity dropped
> 50%→20% by 1-byte column indices), and **Delayed Precision Reduction** to custom **FP16 /
> FP10 (1s5e4m) / FP8 (1s4e3m)** applied *after* the forward use, so no rounding error ever
> enters the forward pass — which is why 8 bits trains where uniform All-FP16 diverges.
> Everything decodes to FP32 before any multiply, so what it buys is **GPU DRAM capacity**, not
> arithmetic and not bandwidth: **1.8× geomean peak footprint (2× max) at 4% overhead**, pure
> software on a stock Titan X + CNTK, worth a doubled minibatch and **22% on Resnet-1202**.

### Proposed values on their four axes

| Axis | Proposed | Evidence (one line) |
|---|---|---|
| **Level** | **`ALGO+SYS`** — the seed row's revision-log correction is right; confirm it | The algorithms are real (three encodings derived from layer backward-pass semantics) and the system is real (graph-rewriting Schedule Builder, static liveness analysis, modified CNTK static allocator, CUDA encode/decode kernels, rewritten MaxPool backward). **No `ARCH`**: greps `area` 0, `RTL` 0, synthesis 0; §V-H *asks* for hardware dynamic allocation but builds none |
| **Q-oriented** | **`Q-ORIENTED`** — human ruling 2026-09-14, overriding this file's draft `non-Q` | Swap the format for INT8: Binarize (a fact about `dx=(y>0)?dy:0`), SSDC (sparsity), inplace, the Schedule Builder and the allocator work all survive untouched, and lossless alone is 1.4× of the 1.8×. **Only DPR dies** — and DPR alone would be `Q-ORIENTED` under the ENEC ruling |
| **Data type** | **`FP32` `FP16` `FP10` `FP8` `MIXED`** — **seed has `—`; I disagree** | §IV-A p. 6 gives element precision for all three: FP16 = IEEE half; **FP10 = 1s/5e/4m**; **FP8 = 1s/4e/3m** (E4M3, in 2018); packed 2/3/4 per 4 bytes, round-to-nearest, clamped, denormals dropped. `MIXED` because FP32 forward and narrow stash coexist by construction. **`FP10` is a new token** (the `FP14` precedent from AQB8) — drop it first if the vocabulary should stay closed. **Explicitly not `BINARY`**: the 1-bit field is a sign *predicate*, not a value encoding. **Explicitly not `VQ`/`LUT`**: no codebook anywhere |
| **Generation** | **`G2`** — seed has `—`; medium confidence | TAXONOMY §4's G2 test is "does the paper **design a numeric type**, or build an architecture to execute quantized arithmetic? **Either one → G2**". Gist designs two (FP10, FP8) and inherits one; it builds no architecture, so it is G2 on the first clause only. Not G1 (the formats are designed, not inherited); not G3 (no LLM, no outlier thread, no codebook, no weight-only bandwidth argument). **The alternative is `—`**, following TAXONOMY's own `SpZip` worked example for non-Q compression papers — defensible, but `SpZip` has no numeric format at all and Gist has three |
| **Optimization** (free text) | `training` `stashed feature maps` `feature-map encoding` `ReLU 1-bit mask` `MaxPool argmax map` `sparse storage dense compute` `CSR` `delayed precision reduction` `custom FP8/FP10` `liveness analysis` `static memory allocator` `inplace computation` `CNTK` | All four seed tags **verified present in the paper's own words**; these add the mechanisms that change how it reads — `MaxPool argmax map`, `sparse storage dense compute`, `liveness analysis` |

### Seed-tag disagreements

1. **Data type `—` → `FP32` `FP16` `FP10` `FP8` `MIXED`.** The only substantive disagreement.
   With `—`, a reader scanning the venue list cannot tell that this paper defines an E4M3 FP8
   in 2018 — the one fact in it a quantization survey needs. The `SpZip` `—` precedent does not
   reach a paper that specifies three exponent/mantissa splits.
2. **Generation `—` → `G2`.** Reported, lower stakes; the counter-argument is in the row above.
3. **Level `ALGO+SYS`: confirm, do not revisit.** (Q-oriented was drafted `non-Q` here and
   **ruled `Q-ORIENTED`** on 2026-09-14.) The revision-log
   correction (`ARCH` → `ALGO+SYS`, venue README line 114) is right; evidence above.
4. **No disagreement on the four Optimization seeds.** `training`, `feature-map encoding`,
   `ReLU 1-bit`, `delayed precision reduction` are all the paper's own terms. Grepped.
5. **The Comment column understates it.** "Encode across the forward/backward temporal gap. A
   CNTK framework, not hardware. Sheet: Less related" is true but hides the lossless/lossy
   split, which is the reason to keep the row at all.

### §4 fairness verdict (note version, ≈57 words)

> Fair: iso-GPU, iso-framework, iso-model, real measurement (Titan X, CNTK, ImageNet).
> **Not iso-accuracy** — training-curve overlap only, no validation number, DPR width tuned per
> network. Footprint baseline excludes weights/gradients/workspace; category ratios use a
> different baseline from the end-to-end ones. **Do not quote** 4.1× (projection) or 2× bare
> (max; geomean 1.8×).

### Proposed venue-list row

```
| [ ] | [Gist: Efficient Data Encoding for Deep Neural Network Training](https://doi.org/10.1109/ISCA.2018.00070) | *close read* | ALGO+SYS | Q | `FP32` `FP16` `FP10` `FP8` `MIXED` | G2 | `training` `stashed feature maps` `ReLU 1-bit mask` `MaxPool argmax map` `sparse storage dense compute` `CSR` `delayed precision reduction` `liveness analysis` `static memory allocator` | Encodes the feature map only across the forward/backward gap. Two lossless encodings (1-bit ReLU predicate + 4-bit MaxPool argmax map; CSR) and one lossy (**delayed** precision reduction to a custom **1s4e3m FP8** — E4M3, in 2018). All decoded to FP32 before any multiply: buys **capacity**, not arithmetic. Software in CNTK, no hardware. 1.8× geomean footprint, 4% overhead |
```

## Note from the source list

> **Keywords:** store an encoded representation of feature maps for this temporal gap and decode this data for use in the backward pass
>
> **Comment:** Less related

## Abstract (verbatim, from the archived PDF)

> Modern deep neural networks (DNNs) training typically relies on GPUs to train complex
> hundred-layer deep networks. A significant problem facing both researchers and industry
> practitioners is that, as the networks get deeper, the available GPU main memory becomes a
> primary bottleneck, limiting the size of networks it can train. In this paper, we
> investigate widely used DNNs and find that the major contributors to memory footprint are
> intermediate layer outputs (feature maps). We then introduce a framework for DNN-layer-
> specific optimizations (e.g., convolution, ReLU, pool) that significantly reduce this
> source of main memory pressure on GPUs. We find that a feature map typically has two uses
> that are spread far apart temporally. Our key approach is to store an encoded
> representation of feature maps for this temporal gap and decode this data for use in the
> backward pass; the full-fidelity feature maps are used in the forward pass and
> relinquished immediately. Based on this approach, we present Gist, our system that employs
> two classes of layer-specific encoding schemes – lossless and lossy – to exploit existing
> value redundancy in DNN training to significantly reduce the memory consumption of
> targeted feature maps. For example, one insight is by taking advantage of the
> computational nature of back propagation from pool to ReLU layer, we can store the
> intermediate feature map using just 1 bit instead of 32 bits per value. We deploy these
> mechanisms in a state-of-the-art DNN framework (CNTK) and observe that Gist reduces the
> memory footprint to upto 2× across 5 state-of-the-art image classification DNNs, with an
> average of 1.8× with only 4% performance overhead. We also show that further software
> (e.g., CuDNN) and hardware (e.g., dynamic allocation) optimizations can result in even
> larger footprint reduction (upto 4.1×).
