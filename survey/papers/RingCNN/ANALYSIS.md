# RingCNN — paper notes

**RingCNN: Exploiting Algebraically-Sparse Ring Tensors for Energy-Efficient CNN-Based Computational Imaging**
Chao-Tsung Huang (single author, Dept. of Electrical Engineering, National Tsing Hua University, Taiwan)
**ISCA 2021** ｜ DOI: **not recorded** — the ACM/IEEE record is not reachable by script (403); look it up when citing
Venue evidence (2026-09-02): arXiv `comments` field, verbatim: *"To Appear in 2021 ACM/IEEE 48th Annual International Symposium on Computer Architecture (ISCA)"*; the archived PDF's own page-1 header repeats it.
Archived here: **arXiv:2104.09056v1** (2021-04-19), 14 pages — **the preprint, not the
published ISCA 2021 version**; the two were **not compared**.
**Author's project page (with video):** https://www.ee.nthu.edu.tw/chaotsung/RingCNN/index.html
— Chao-Tsung Huang's own page at NTHU, supplied by the human 2026-09-14. **Link only: nothing
was downloaded from it**, and it is not a PDF source under the arXiv-only rule. Its contents
were **not** read, so nothing in this file rests on it.

Status: **note ready** ｜ Last updated: 2026-09-14
Tags: `new-data-type` `analytical-dtype` `dtype-granularity` `accelerator`
— **`new-data-type` stands.** It was disputed in this file's first draft; the human's `Q-ORIENTED`
ruling of 2026-09-14 (real → complex → ring: the *value* becomes a ring element) reinstates it, and
no change to `survey/TAGS.md` is needed.
How far it was read: **full close read of §I–§VIII and Appendix C.** §III (ring algebra: Eqs. 2–10,
conditions C1–C3, Tables I and II) and §IV–§V (modelling, dynamic fixed-point quantization,
eRingCNN, the on-the-fly directional-ReLU pipeline) read line by line; §VI read line by line
against Tables IV–VIII. **All eight tables and every figure in this paper are bitmaps —
`pdftotext` recovers only their captions** — so Tables I–VIII were read by rendering the PDF pages
at 250 dpi, and every table number below comes from that rendering, not from `extracted/`.
Numbers taken off a **plot** rather than a table are marked *(read off Fig. N)* and are approximate.
**Skimmed, and load-bearing to nothing quoted here:** Appendix A (minimality proof for
diagonalizable `G`), Appendix B (associativity from commutativity), and the CP-ARLS `grank` search
procedure — I take the paper's claim that the n=4 exhaustion yields exactly two non-isomorphic
grank-4 permutations **on trust**, and did not re-derive it. **Not resolved:** the exact
sub-column split of Table II's transform matrices for `C`, `R_H4-I` and `H` (the composite
`(H_k / 0 1 …)` blocks); I did not need them, because the paper's chosen ring uses identity
transforms. **Verified before citing:** the ring product, the operand order and which factor is
structurally constrained — see *Method*, first block, which is written to settle that question.
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> Original: https://arxiv.org/abs/2104.09056
> The PDF is **not committed** (3.1 MB). Re-download: `curl -sSL -o 2104.09056.pdf https://arxiv.org/pdf/2104.09056`
> Extract text: `python3 extract.py` → `extracted/` (committed, greppable)
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, ISCA 2021 row.

---

## What the close read changed in the brief

Six corrections; the brief was substantially right on motivation and overview, and wrong on
placement. Each is a one-liner here and is worked out in full below.

1. **Taxonomy placement — the brief's biggest error.** It filed the paper under **§1.2 "new data
   type"** on the grounds that it is "a representation change at the algebra level rather than the
   bit-field level". That reasoning is right and the conclusion does not follow: §1.2 is for papers
   *whose point is the numeric format*. RingCNN's numeric format is **plain dynamic 8-bit fixed
   point**, cited to the ARM Q-format guide [1] and to the author's own eCNN [21]. The paper
   belongs in **§1.1** (uses a traditional type; the novelty is elsewhere) with a real claim on
   **§2.2** (fine-grained granularity — *n* feature Q-formats per layer). See *Is this a
   quantization paper at all?*.
2. **"50% and 75% sparsity" is a degrees-of-freedom count, not zeros in data.** Each `n×n` block of
   real weights is replaced by one ring element carrying `n` real numbers: DoF `n² → n`. For the
   ring the paper actually implements this is *literally* an `n`-group group convolution.
3. **"Equivalent 41 TOPS" is not delivered arithmetic.** It is the real-valued model's operation
   count. Delivered is **20.48 TOPS (n=2)** and **10.24 TOPS (n=4)** — derived below.
4. **"2.00×/3.84× energy efficiency" is the convolution *engines*, not the accelerator.** Whole-chip
   is **1.85× (n=2)** and **3.12× (n=4)**. The abstract does say "our ring convolution engines", so
   this is a reading hazard rather than a paper error.
5. **"No path to quantizing an existing network post hoc" — confirmed and sharpened.** It is worse
   than the brief says: there is no path to *converting* an existing trained network either. The
   structure is imposed on the architecture and the model is trained from scratch (§IV-A/B).
6. **"PSNR-on-imaging does not tell you how the idea would behave on classification" — partly
   wrong.** **Appendix C** reports ResNet-56 on CIFAR-100 against LeGR structured pruning. The
   result is weaker than the imaging one and is a genuine limitation, but the paper is not silent.

---

## Brief

### 1. Motivation

CNNs for **computational imaging** (denoising, super-resolution) are unlike recognition
CNNs: few weights, huge images, high precision needed, and they "defy conventional sparsity
techniques" when rendering dense details. FFDNet at 4K30 demands ~106 TOPS **(verified, §I, p1)**.
Natural sparsity fails on regularity — SparTen spends only 11.7% of power and 5.6% of area on MACs
**(verified, §II, p2)** — and low-rank sparsity fails on quality: depthwise convolution alone costs
1.2 dB PSNR on SR networks **(verified, §I, p2, cited to eCNN [21])**.

### 2. Overview

Rather than finding sparsity in the data, **impose it algebraically**. Build CNNs over a
*ring algebra* on n-tuples, which defines multiplication, addition and non-linearity such
that the real-valued weight count drops n-fold **by construction**. The paper unifies several
ring variants into one framework, prices each in **fixed-point** terms, and finds that the cheapest
is the one with **identity transforms** — component-wise product, i.e. group convolution — whose
lost information mixing is restored by a **directional ReLU** `H·ReLU(H·y)` placed in the
non-linearity instead of in the multiplication. It implements the eRingCNN accelerator at 40 nm for
n=2 and n=4 (50% and 75% sparsity).

### 3. Pros and cons

**Pros**

- **Structural, not statistical, sparsity** — regular by construction, so it avoids the
irregularity overheads that make unstructured pruning expensive in hardware (the paper
cites SparTen at only 0.43 TOPS/W as the cautionary case).
- **The internal control is the cleanest in the corpus.** The baseline is the same author's eCNN
[21], re-implemented at the same node, same dataflow, same dynamic 8-bit quantization, same
throughput target — and the real-valued baseline models are *retrained with higher learning rates*
so they beat their own published numbers **(verified, §VI-A, p8)**.
- Layout-level results at two design points: equivalent 41 TOPS at 3.76 W (n=2) and 2.22 W
(n=4); **engine-level** 2.00×/3.84× energy and 2.08×/3.77× area over the real-valued counterpart,
at +0.01 dB (n=2) / −0.11 dB (n=4) average PSNR.
- Targets a workload the rest of the corpus ignores, with a quality metric (PSNR)
appropriate to it.

**Cons**

- A new algebra means models must be **built and trained in it** — no path to quantizing, or even
converting, an existing network post hoc.
- **The ring buys weights and arithmetic and nothing else.** Feature SRAM (1570 KB) and DRAM
bandwidth (1.93 GB/s) are identical to eCNN, and the block-buffer bank is 6.24 mm² in *both*
configurations — which is why the whole-chip gain (2.36× area at n=4) falls far short of the
engine gain (3.77×).
- The n=4 quality drop is small but real, and the one recognition data point (Appendix C) is
noticeably weaker: LeGR structured pruning **beats** the ring at 2× and 4× computation efficiency
and only loses at 8×.
- Ring algebra is conceptually heavy relative to its adoption; **no other paper in this corpus
cites RingCNN, ring algebra or eCNN** (verified by grep over all 40 `extracted/*.raw.txt`,
2026-09-14).

### 4. Where it applies

**§1.1 + §2.2, not §1.2** — see the correction list above. The most unusual *structural* proposal
in the corpus, but the number itself is an ordinary 8-bit fixed-point value. Read with
[`SmartExchange`](../SmartExchange/ANALYSIS.md) and [`SingularBit`](../SingularBit/ANALYSIS.md) as
the corpus's three structural-decomposition entries — RingCNN is the one whose structure is chosen
*before* seeing any weights.

---

## Conclusions

**1. The contribution is above the number, and the number never changes.** Weights and features are
8-bit dynamic fixed point in both the baseline and the proposal (`Quantization Precision: Dynamic
8-bit`, **verified, Table V, p11**; and `Quantization: Dynamic 8-bit` for eRingCNN against
`Dynamic 8-bit` for eCNN, **verified, Table VII, p12**). Apply the survey's own test — swap the
format for plain INT8 — and the ring algebra, the n× weight reduction, the n× MAC reduction, the
RCONV engines and the near-maximum efficiency all survive untouched. What does *not* survive is a
0.1–0.2 dB tail: the component-wise Q-formats and the full-precision non-linearity. **The
quantization content is a supporting mechanism, not the contribution.**

**2. But fixed-point cost is what selects the design, and that is the paper's sharpest idea.** Under
a *multiplication count*, `R_I` and `R_H` tie: both reach the maximum `n×` (Table I, "Real Mult."
column: 2.0× for both `R_H2` and `R_I2`, 4.0× for both `R_H4` and `R_I4`). Under **8-bit
fixed-point complexity**, approximated as the product of the multiplier's two input bitwidths
`w_x × w_g` **(verified, §III-D, p6, and Fig. 3, p6)**, they separate: the Hadamard transforms
widen both operands, so `R_H4` and `R_O4` fall to **2.6×** while `R_I4` keeps **4.0×** — "1.6×
worse than `R_I4`" **(verified, §III-D, p6; Table I rightmost column, p5)**. The whole design
follows from that column. **A transform-based fast algorithm is free in floating point and
expensive in fixed point, and this paper is the corpus's cleanest statement of why.**

**3. The chosen ring's linear operator is exactly group convolution — the paper says so.** "a ring
`R_I` equivalent to group convolution which applies component-wise products for a diagonal
full-rank `G`, and its invertible `T` is simply the identity matrix `I`" **(verified, §III-B, p4)**;
Table II labels the `R_I2` and `R_I4` rows "Group convolution" **(verified, p6)**. So the artifact
is *group convolution with n groups plus a Hadamard-sandwiched ReLU*. The ring machinery is the
derivation that identifies it and prices its alternatives, not a runtime object. Saying this
plainly costs the paper nothing and makes it far easier to place.

**4. The quantization mechanism that *is* new is a granularity.** After the directional ReLU "the
different ring components have different dynamic ranges, and using one single Q-format for them
causes large saturation errors. Therefore, for the directional ReLU we propose to use
**component-wise Q-formats** for feature maps… there are `n` different feature Q-formats in one
layer, and each component of `n`-tuple features follows its corresponding Q-format" **(verified,
§IV-C, p7)**. Since real channel `c` is component `c mod n` of ring channel `⌊c/n⌋`, this is `n`
scales per layer, each shared by `C/n` **strided, non-contiguous** real channels — a granularity
axis nothing else in the corpus uses.

**5. Where the requantization happens is a hardware decision, and the paper gets it right.** A
conventional MAC-based accelerator would implement the two Hadamard transforms of `f_H` on the same
fixed-point MACs, which means requantizing the 24-bit accumulator output to 8 bits before each
transform — "up to 0.2 dB of PSNR drop for denoising and SR tasks" **(verified, §V, p8)**. eRingCNN
instead builds a dedicated **on-the-fly** butterfly pipeline that keeps full precision end to end,
up to **33-bit internal**, of which 5 bits are the left-shifts that align components under their
different Q-formats **(verified, §V and Fig. 8, p8)**. Cost: 3.4% of the RCONV-3×3 engine area at
n=2, 8.9% at n=4 **(verified, §VI-C, p11)**.

**6. Two headline numbers need their frame attached before they are quoted.** "Equivalent 41 TOPS"
is the *real-valued model's* operation count, not ops executed; and the 2.00×/3.84× gains are
engine-level. Both are worked out under *Key numbers*.

---

## Method

### The algebra — operand order, product form, and which factor is constrained

Written out deliberately, because this is the trap on this paper.

- **Ring multiplication is `z = g · x`** (Eq. 2, §III-A, p3), with **`g` the filter weights and `x`
  the feature map**: "we will use `g` for filter weights and `x` for feature maps in the following"
  **(verified, §III-A, p4)**.
- **Its bilinear form is** `z_i = Σ_j Σ_k M_ikj g_k x_j` (Eq. 3, p3), where `M` is a 3-D indexing
  tensor with entries in `{1, 0, −1}`.
- **Its isomorphic matrix form is `z = G x`** (Eq. 4, p4) with `G_ij = Σ_k M_ikj g_k`. **`G` is built
  from the weights and multiplies the features from the left.** Not `x G`, not `G` built from `x`.
- **The structurally constrained factor is `G`, i.e. the weights.** `G` is `n×n` but has only `n`
  degrees of freedom: "using `n`-tuple rings instead will only need `n` real-valued weights to
  represent the matrix `G`, i.e. DoF of `G` is reduced from `n²` to `n`" **(verified, §III-D, p5)**.
  **Features are untouched:** an `n`-tuple holds `n` real activations, so the feature volume is
  identical to the real-valued network.
- **The fast algorithm is `z = T_z ( (T_g g) ∘ (T_x x) )`** — transform *both* operands, multiply
  component-wise on `m`-tuples, then reconstruct (Eqs. 6–8, §III-B, p4). `T_g`, `T_x` are `m×n`;
  `T_z` is `n×m`; `∘` is the component-wise product. The multiplication count drops from `n²` to
  `m`, and `m ≥ grank(M)`; when `G` is diagonalizable over ℝ as `G = T⁻¹ D T`, the minimum is
  `m = rank(G)` with `g̃ = diag(D)` (Theorem A.1).
- **For the chosen ring `R_I`, `T_g = T_x = T_z = I`**, `G = diag(g_0, …, g_{n−1})`, and the product
  reduces to **`z_i = g_i x_i`** — an honest-to-goodness component-wise product, `m = n`, 8-bit ×
  8-bit multipliers with no operand widening **(verified, Table II rows `R_I2` / `R_I4`, p6)**.
- **Directional ReLU is `f_dir(y) ≜ U f_cw(V y)`** — **`V` inside, `U` outside** (§III-E, p6). The
  proposed instance is **`f_H(y) ≜ H f_cw(H y)`** (Eq. 10, p6) with `H` the `n×n` Hadamard matrix
  and `f_cw` the component-wise ReLU (Eq. 5, p4). *"performing non-linearity in the directions of
  the row vectors of `V`… and then turning the axes to the column vectors of `U`."*
- **The proposed ring is written `(R_I, f_H)`** — the pair of a *multiplication* (`R_I`) and a
  *non-linearity* (`f_H`). It is **not** `R_H`: "`(R_I, f_H)` multiplies input features by weights
  `g` **directly** while `R_H` does that **after applying the filter transform**", and "`(R_I, f_H)`
  applies Hadamard transform **only when non-linearity is required**, but `R_H` always does"
  **(verified, ablation study §VI-A, p9)**.
- **Consequence for the datapath.** Weights never pass through a transform; both multiplier operands
  stay 8-bit; the Hadamards act only on the **accumulated** output (24-bit at n=4) inside the
  non-linearity block.

### What is quantized

| | |
|---|---|
| **Weights** | 8-bit dynamic fixed point, **one Q-format per layer** |
| **Features** | 8-bit dynamic fixed point, **`n` Q-formats per layer, one per ring component** (n = 2 or 4) |
| **Biases** | separate bias memory (12 KB); precision not stated |
| **Accumulator** | **24-bit at n=4** entering the non-linearity **(verified, §V, p8)** |
| **Non-linearity datapath** | **full precision, up to 33-bit internal**; 5 of those bits are component-alignment left-shifts **(verified, §V and Fig. 8, p8)** |
| **Outliers** | **none.** The word "outlier" does not appear in the paper (grepped). The only distributional problem named is *saturation* after `f_H`, and it is solved with granularity |
| **Escape hatch** | the `f_H` block itself — no requantization between the two Hadamards. Requantizing there (24→8 bit at n=4) costs **up to 0.2 dB** |
| **Retraining** | **neither PTQ nor QAT on a stock checkpoint.** The ring model is a *different architecture*, converted structurally from a real-valued backbone (Fig. 5(a)→(b)) and **trained from scratch**; the float model is then quantized to 8 bits and **fine-tuned** — Table III's dedicated **"Fine-tune for Quantization"** rows, applied identically to Real and Ring **(verified, Table III, p9; §VI-A, p9)** |

The Q-format scheme itself is **inherited, not proposed**: "it has been shown effective to apply
dynamic quantization with separate per-layer Q-formats [1] for real-valued feature maps and
parameters [21]" — [1] is the ARM Q-format guide, [21] is the author's own eCNN **(verified,
§IV-C, p7)**. Only the *component-wise* refinement is new.

### What hardware it assumes

eCNN [21] (MICRO'19) as the backbone: block-based inference with recompute at block boundaries,
highly-parallel dense convolution engines, dynamic 8-bit. eRingCNN replaces the real-valued
convolution engine with an RCONV engine and the ReLU block with the on-the-fly directional-ReLU
block; everything else is eCNN. Per cycle it computes `(32/n)`-channel `n`-tuple outputs from
`(32/n)`-channel `n`-tuple inputs over a 4×2 spatial tile **(verified, §V, p7)**.

---

## Key numbers, with their frame

Everything below is **40 nm TSMC, 250 MHz**. Evidence levels present, and **not to be pooled**:
**post-layout** (Synopsys IC Compiler + PrimeTime PX on post-layout parasitics with RTL activity
waveforms) for Tables V–VII and Fig. 14; **post-synthesis** (Design Compiler) for Fig. 12 and
Table VIII; **training/inference simulation** for all PSNR; **analytical node projection** for
Diffy's 40 nm column. **There is no silicon anywhere in this paper.**

| Setting | Model | Metric | Baseline | Result | Source |
|---|---|---|---|---|---|
| Layout, n=2 | ERNet@UHD30 | area / power / MACs / SRAM | — | **33.73 mm² · 3.76 W · 40,960 MACs · 2,550 KB** | Table V, p11 **verified** |
| Layout, n=4 | ERNet@UHD30 | area / power / MACs / SRAM | — | **23.36 mm² · 2.22 W · 20,480 MACs · 2,070 KB** | Table V, p11 **verified**. *Table VI's breakdown totals 2.20 W — a 0.02 W inconsistency* |
| Throughput | — | "equivalent" TOPS | — | **41.0 for both**, i.e. the real-valued model's op count. **Delivered arithmetic is 20.48 TOPS (n=2) and 10.24 TOPS (n=4)** | Tables V + VIII; **derived**: 40,960 × 2 × 250 MHz = 20.48 TOPS, × 2 = 40.96 ≈ 41; 20,480 × 2 × 250 MHz = 10.24, × 4 = 40.96 |
| RCONV engines, layout | ERNet@UHD30 | area / energy efficiency | eCNN's real-valued engines | **n=2: 2.08× area, 2.00× energy. n=4: 3.77× area, 3.84× energy** | Fig. 14 + §VI-C, p11 **verified** |
| **Whole accelerator**, layout | ERNet@UHD30 | area / energy efficiency | eCNN | **n=2: 1.64× area, 1.85× energy. n=4: 2.36× area, 3.12× energy** | §VI-C, p11 **verified** — *this, not the row above, is the end-to-end number* |
| Conv-engine synthesis | SR4ERNet-B17R3N1, 8-bit | area efficiency vs PSNR, one 3×3 layer, 32→32 real channels | real-valued engine at 1× | `(R_I2,f_H2)` ≈2.0× at 28.46 dB (real: 28.44); `(R_I4,f_H4)` ≈3.8× at 28.35 dB | Fig. 12, p10 *(read off Fig. 12)* |
| Ring choice, synthesis | same | area efficiency and PSNR against the named alternatives | `R_H4-I` (CirCNN-alike), `R_H4` (HadaNet-alike) | `(R_I4,f_H4)` is **1.8×** and **1.5×** their area efficiency with **≈0.1 dB** more PSNR | §VI-A, p10 **verified** (prose) |
| 8-bit quantization loss | six ERNet targets (Dn/SR×2/SR×4 at HD30 and UHD30) | avg PSNR drop, float → dynamic 8-bit | the same models in float | **−0.11 dB (n=2), −0.12 dB (n=4)**; "similar to the case of using real numbers" | Fig. 13 top + §VI-B, p10 **verified** |
| Algebra loss | same six, **quantized** | avg PSNR difference | eCNN (real-valued) | **+0.01 dB (n=2), −0.11 dB (n=4)** — this is the abstract's "0.11 dB drop" | Fig. 13 bottom + §VI-B, p10 **verified** |
| Denoise, HD30, **float** | DnERNet-PU B19R3N15 (22-layer), CBSD68 σ=25 | PSNR | eCNN 31.36 / FFDNet | n=2 **31.36** (+0.15 vs FFDNet); n=4 **31.27** (+0.06) | Table IV, p10 **verified** |
| Denoise, UHD30, **float** | DnERNet-PU B8R2N5 (11-layer) | PSNR | eCNN 31.19 / FFDNet | n=2 **31.17** (**−0.04** vs FFDNet); n=4 **31.00** (**−0.21**) — the one place the method loses to the software state of the art | Table IV, p10 **verified** |
| SR×4, HD30, **float** | SR4ERNet-B34R4N0 (39-layer), Set5/Set14/BSD100 | PSNR | eCNN 29.47 / SRResNet | n=2 **29.51** (+0.14 vs SRResNet); n=4 **29.47** (+0.10) | Table IV, p10 **verified** |
| SR×4, UHD30, **float** | SR4ERNet-B17R3N1 (22-layer) | PSNR | eCNN 29.40 / SRResNet | n=2 **29.40** (+0.03); n=4 **29.33** (−0.04) | Table IV, p10 **verified** |
| vs unstructured pruning | SR4ERNet-B17R3N1 / -B34R4N0 | PSNR at 2× / 4× / 8× compression | magnitude pruning + 200 fine-tune epochs | Ring wins at all three; at 2× the ring (≈28.52) **beats the uncompressed 1× real model** (≈28.50) | Fig. 11, p9 *(read off)*; §VI-A **verified** for the direction |
| vs Diffy | FFDNet-level inference @ Full-HD 20 fps | power | Diffy **65 nm reported 13.58 W**, **40 nm projected 6.79 W** (2.35× gate density, 0.5× power) | n=2 **2.51 W (2.71×)**, n=4 **1.48 W (4.59×)** | Table VII, p12 **verified**. *Baseline is a projection, and areas are 12.43 mm² (Diffy) vs 33.73 / 23.36* |
| vs sparsity SOTA | — | **equivalent** TOPS/W, **synthesis** | SparTen 2.7 (45 nm, 3.1× @VGG16 CONV) · TIE 1.9 CONV / **72.9 FC** (28 nm) · CirCNN 10.0 (45 nm, 66× @AlexNet) | n=2 **19.1**, n=4 **28.4** — at only **2× / 4×** compression | Table VIII, p12 **verified**. *Power here is 2.14 / 1.45 W, not Table V's 3.76 / 2.22 W* |
| Directional-ReLU cost | — | share of RCONV-3×3 engine area | — | **3.4% (n=2), 8.9% (n=4)**; inference datapath grows 3.85 → 4.38 mm² | §VI-C, p11 **verified** |
| Requantization avoided | denoising + SR | PSNR saved by the full-precision `f_H` pipeline | quantizing 24→8 bit before each Hadamard | **up to 0.2 dB** | §V, p8 **verified** |
| Weight memory | — | weight SRAM | eCNN 1288 KB | **972 KB (n=2), 492 KB (n=4)** — *not* 640/320, because eCNN's parameter compression was dropped and the memory grown 1.5× | §V p7 + Table VII p12 **verified** |
| Feature memory / bandwidth | — | feature SRAM / DRAM BW | eCNN 1570 KB / 1.93 GB/s | **1570 KB / 1.93 GB/s — unchanged** | Table VII p12 + §VI-C p11 **verified** |
| **Recognition** (Appendix C) | ResNet-56, CIFAR-100 | top-1 vs computation efficiency | LeGR structured pruning; original ≈72.5% | Ring ≈69.5% @2×, ≈67% @4×, ≈64% @8×. **LeGR is better at 2× and 4×**; the ring only wins at 8× | Fig. C-1, p14 *(read off)* |

### Citation hazards

1. **"Equivalent 41 TOPS" is a workload-referred number, not ops executed.** Both configurations
   report 41.0 because both serve the same real-valued model: `MACs × 2 × f × n`. Delivered
   arithmetic is **20.48 TOPS (n=2)** and **10.24 TOPS (n=4)** — the n=4 part does *half* the
   arithmetic of the n=2 part. The paper is consistent (it applies "equivalent" throughput to
   SparTen, TIE and CirCNN too, and the word is in the abstract), but stripped of "equivalent" the
   number becomes a 4× overstatement for n=4.
2. **The abstract's efficiency gains are engine-level; the accelerator's are much smaller.** 2.00×/
   2.08× (n=2) and 3.84×/3.77× (n=4) are the RCONV engines. End-to-end: **1.85×/1.64×** and
   **3.12×/2.36×**. The gap is the block-buffer bank — 6.24 mm² in *both* designs, 18.5% of n=2's
   area and **26.7%** of n=4's — plus an inference datapath that *grows* with n. Quote the
   whole-accelerator pair.
3. **Two power numbers for the same chip, unreconciled.** Table V (layout): 3.76 / 2.22 W. Table VIII
   (labelled "synthesis results"): **2.14 / 1.45 W**, and the 19.1 / 28.4 TOPS/W are computed from
   those. The difference is presumably pre- vs post-layout, but the paper never says. **19.1 / 28.4
   TOPS/W must not be quoted alongside 3.76 / 2.22 W.** At layout power the equivalent efficiency is
   10.9 / 18.4 TOPS/W, and the *delivered* efficiency is 5.4 / 4.6 TOPS/W.
4. **Table VIII is not iso-anything.** Different nodes (45/28/45 vs 40 nm), different applications
   (recognition vs computational imaging), different bitwidths (8/16/16 vs dynamic 8), different
   compression ratios (3.1×/7.4×/66× vs 2×/4×). And **TIE reports 72.9 TOPS/W** — higher than
   eRingCNN's 28.4 — on FC layers; the paper says so in prose but the table's bolding does not.
5. **The Diffy comparison rests on an analytical node projection** (65 → 40 nm at 2.35× gate density
   and 0.5× power, from a TSMC web page, footnote 1, p11) and is **not iso-area**: projected Diffy is
   **12.43 mm²** against eRingCNN's 33.73 / 23.36 mm², at 4× the clock.
6. **Two frames inside one abstract sentence.** "3.84× and 3.77× with only 0.11 dB drop of PSNR": the
   efficiencies are engine-vs-engine, the 0.11 dB is whole-model-vs-eCNN averaged over six
   application targets. They are not measured on the same object.
7. **Table IV is float, Fig. 13 is fixed point.** The PSNR-gain-over-FFDNet/SRResNet numbers people
   will want to quote (+0.15, +0.14 …) are **floating-point models**; the deployed 8-bit models are
   ~0.11 dB below them.
8. **This is arXiv v1, not the published ISCA 2021 paper.** Not compared.

---

## Cost and requirements

**Flow.** Verilog RTL, bit- and cycle-accurate functional verification; Synopsys Design Compiler
with a TSMC 40 nm library; ARM memory compilers for SRAM macros; Synopsys IC Compiler for P&R and
layout of five pipelined macro circuits; PrimeTime PX for time-based power on post-layout
parasitics driven by RTL activity waveforms **(verified, §VI-C, p10)**. **No fabricated silicon.**

**Area and power breakdown (Table VI, p11, post-layout).**

| Block | n=2 area | n=2 power | n=4 area | n=4 power |
|---|---|---|---|---|
| RCONV-3×3 | 17.50 mm² (51.86%) | 3.02 W (80.32%) | 9.61 (41.13%) | 1.56 W (70.23%) |
| RCONV-1×1 | 1.88 (5.56%) | 0.23 (6.19%) | 1.05 (4.50%) | 0.14 (6.33%) |
| Inference datapath | 3.85 (11.43%) | 0.23 (6.08%) | **4.38 (18.74%)** | 0.27 (12.19%) |
| Main controller | 0.73 (2.15%) | 0.00 (0.10%) | 0.32 (1.36%) | 0.00 (0.12%) |
| Weight/bias memory | 3.54 (10.50%) | 0.05 (1.25%) | 1.77 (7.57%) | 0.02 (0.84%) |
| Block buffer bank | **6.24 (18.49%)** | 0.23 (6.07%) | **6.24 (26.71%)** | 0.23 (10.28%) |
| **Total** | **33.73** | **3.76** | **23.36** | **2.20** |

**What the design pays for the ring.** (i) The **on-the-fly directional-ReLU block** — butterfly
Hadamard adder networks plus per-component left-shifters, full precision to 33 bits — at 3.4% of
the RCONV-3×3 engine at n=2 and 8.9% at n=4, and it appears again in the inference datapath for the
non-linearity after skip and residual connections. (ii) The **inference datapath grows with n**
(3.85 → 4.38 mm²) because a larger n means more adders and wider bitwidths — the one cost in this
paper that moves the *wrong* way with more sparsity. (iii) The **block buffer bank does not shrink
at all**, being feature-side.

**What it does not need.** No variable-bitwidth multiplier, no operand alignment across precisions,
no outlier path, no codebook, no metadata, no index storage, no load balancing — the whole
irregular-sparsity apparatus is absent by construction, which is the point.

**Does it need the proposed hardware?** Partly. The linear half maps onto stock hardware as an
`n`-group group convolution and would get the MAC saving anywhere. **The non-linearity does not**:
`H·ReLU(H·y)` on a MAC-based accelerator means requantizing to 8 bits twice and losing up to 0.2 dB,
and the ±1 weights waste the multipliers. The dedicated block is the part that must be built.

**Does it need retraining?** Yes, all the way down. The model is a different architecture; there is
no conversion path from a trained real-valued checkpoint.

---

## Limitations and open questions

- **Hardware exists only for n=2 and n=4.** n=8 appears in the model study (Fig. 11, 8×
  compression) with no accelerator; the inference-datapath growth with n suggests the returns are
  already bending at n=4.
- **Feature-side costs are untouched.** Same feature SRAM, same DRAM bandwidth, same block buffers
  as eCNN. Any workload where activations dominate gets nothing from this idea.
- **The recognition evidence is thin and unfavourable at the useful end.** One model
  (ResNet-56 / CIFAR-100), and LeGR beats it at 2× and 4× computation efficiency (Fig. C-1). The
  paper defers accelerator work for recognition to future work.
- **The proposed linear operator is group convolution**, which the paper itself criticises in §III-E
  ("`R_I` will have the worst model capacity… the same as the discussion on group convolution
  [52]"). The claim is therefore not "grouped convolution is good" but "grouped convolution plus
  the right non-linearity is good, and it is the cheapest thing to build in fixed point". A reader
  who takes the paper as vindicating group convolution generally will over-read it.
- **The `f_H` design is asserted, not ablated against alternatives at fixed area.** `(R_I4, f_O4)`
  is reported inferior in Fig. 9 but no cost-matched sweep of `U`/`V` choices is given.
- **The quality argument depends on training both algebras well.** The paper raises learning rates
  "as high as possible before training procedures become unstable" per algebra and uses a *different*
  denoising schedule for Real (1e-3) and Ring (5e-4) in the polishment setting (Table III). This is
  disclosed and is the right thing to do, but it means the comparison is tuned-vs-tuned by the same
  author, not held fixed.
- **No independent baseline is run in-house.** FFDNet, SRResNet, VDSR, CBM3D, SparTen, TIE, CirCNN
  and Diffy are all quoted or projected.
- **Table V vs Table VI (2.22 vs 2.20 W) and Table V vs Table VIII (3.76/2.22 vs 2.14/1.45 W) are
  not reconciled.**
- **Open:** whether the component-wise Q-format idea generalises off the ring. Any mechanism that
  mixes channels with a fixed ±1 transform (Hadamard rotation for outlier suppression, for example)
  produces the same "different dynamic ranges after mixing" problem, and `n` scales per layer is a
  cheap answer to it. Nothing in the corpus has tried that.
- **Open:** what the published ISCA 2021 version says. Not compared.

---

## Relation to other entries

**The corpus's three structural-decomposition entries, and the axis that separates them.**
[`SmartExchange`](../SmartExchange/ANALYSIS.md) (ISCA'20) forces `W = Ce·B`, a *large sparse*
coefficient matrix with power-of-two non-zeros times a *small basis*, fitted to the trained weights
by alternating structure-preserving retraining. [`SingularBit`](../SingularBit/ANALYSIS.md)
(ISCA'26) takes an SVD and allocates precision **by rank**, again reading the structure out of the
weights. **RingCNN reads nothing out of the weights.** The structure is a fixed algebraic
constraint chosen before training, and the `n×n` block's degrees of freedom are `n` because the
algebra says so. So the axis is **where the structure comes from**: *fitted to the data*
(SmartExchange, SingularBit) versus *imposed by construction* (RingCNN). RingCNN is the cheapest of
the three at inference — no basis to store, no rank metadata, no encoding overhead, exactly `n`
numbers per block — and the most expensive at training time, because there is no path from an
existing checkpoint at all.

**Retraining axis — RingCNN is a rung past the existing end.** The axis so far runs PTQ / QAT /
*alternating structure-preserving retraining* (SmartExchange, Phi's PAFT). RingCNN adds
**structure-by-construction**: the constraint is not something you retrain a model into, it is a
property of the architecture you instantiate. That is a strictly harder deployment constraint than
SmartExchange's, and worth naming as such.

**Granularity axis — a new value: per-ring-component.** The axis runs per-layer (BitFusion,
OLAccel) → per-region (DRQ) → per-channel (Tender) → per-group (Oaken, MicroScopiQ) → per-head
(P3-LLM) → per-token (LightNobel) → per-rank (SingularBit). RingCNN's `n` feature Q-formats per
layer are **per-position-within-an-algebraic-tuple**: `n` scales, each shared by `C/n` real channels
that are **strided, not contiguous**. Every other group-wise scheme in the corpus groups contiguous
neighbours because that is what a memory layout gives you cheaply; here the grouping is dictated by
the algebra and is free because the datapath already carries the tuple as a unit.

**Multi-precision datapath axis — RingCNN is deliberately *not* on it**, and that is informative.
BitFusion (spatial) → RaPiD (split pipelines) → SamsungNPU (temporal) → EVA → XtraMAC → UniCore all
answer "how do I make one multiplier serve several widths". RingCNN keeps **one 8×8-bit multiplier
forever** and asks the adjacent question: *given a fixed multiplier width, which algebraic
reformulation of the convolution is cheapest?* Its answer — the one whose transforms do not widen
the operands — extends the organising claim ("the deciding variable is what the substrate charges
for") with a case where the substrate charges for **operand width growth in a fast algorithm**.
Table I's rightmost column, which prices each ring as `w_x × w_g` rather than by multiplication
count, is the corpus's clearest single statement that a Winograd/Hadamard/Fourier-style fast
algorithm is free in floating point and taxed in fixed point.

**Compression-vs-cheaper-arithmetic (the proposed missing axis) — a clean data point.** Ecco sits at
the "buys bandwidth, not arithmetic" end. **RingCNN sits at the opposite end**: it buys arithmetic
and weight storage and buys *literally zero* bandwidth — DRAM traffic 1.93 GB/s and feature SRAM
1570 KB are identical to eCNN, by the paper's own table. Its whole-chip gain (2.36× area at n=4)
against its engine gain (3.77×) is exactly the price of being on that end of the axis.

**Outlier axis — nothing to pay, but the same underlying problem.** RingCNN has no outliers and no
outlier currency. It nonetheless hits the distribution problem the outlier papers hit, from the
other side: a **fixed ±1 mixing transform makes the components' dynamic ranges diverge**, and the
answer is a finer scale rather than a second datapath (OASIS), extra bits (OLAccel, Oaken) or a
sacrificed neighbour (OliVe, MicroScopiQ). Worth a sentence in the outlier section as the cheap
degenerate case.

**Same venue, same year, opposite instincts.** [`SamsungNPU`](../SamsungNPU/ANALYSIS.md) and
[`RaPiD`](../RaPiD/ANALYSIS.md) are the other two ISCA 2021 entries. All three take 8-bit integer
arithmetic as the design target; RaPiD and SamsungNPU spend their innovation *inside* the number
(more formats, more widths, more datapath), RingCNN spends all of it *above* the number and touches
the format only where the algebra forces it. Set against `SamsungNPU`'s area census (arithmetic is
23.4% of a real NPU engine), RingCNN's own breakdown is the counterexample: in a *computational
imaging* accelerator the convolution engines are **51.9% of area and 80.3% of power** at n=2, which
is why attacking the multiplier count pays here and did not pay for Samsung.

**[`BitFusion`](../BitFusion/ANALYSIS.md) is the `G2` archetype and RingCNN is the odd member.**
BitFusion contributes no quantization algorithm and all datapath; RingCNN contributes no numeric
format and all representation. They share a generation by paradigm — *design the representation and
the architecture together* — while sitting on opposite sides of what "representation" means.

---

## Is this a quantization paper at all? — the test, applied

**The question.** The seed comment in `venues/ISCA/README.md` says RingCNN is "a representation
change at the algebra level, not the bit field". That is right about the primary contribution, and
the survey's test settles what follows from it.

**Swap the format for plain INT8. What is left?** Almost everything:

| Mechanism | Survives plain per-tensor INT8? |
|---|---|
| Ring algebra, DoF `n² → n`, n× weight and MAC reduction | **Yes, untouched** |
| The `R_I` choice, and the `w_x × w_g` argument that makes it | **Yes** — the argument is about *fixed-point operand width*, and INT8 is fixed point |
| RCONV engines, near-maximum `≅ n` efficiency | **Yes** |
| Directional ReLU `H f_cw(H y)` as a *function* | **Yes** |
| Component-wise Q-formats | **No** — this is the paper's one genuine format-granularity mechanism |
| Full-precision on-the-fly `f_H` (no 24→8 requantization) | **No** — worth up to 0.2 dB |

**Verdict: `Q-ORIENTED` — settled by the human 2026-09-14, confirming the seed.** The reasoning is
a **data-type** one, not a swap-test one: *real number → complex number → ring element*. A value
stops being a scalar and becomes an `n`-tuple in a ring — a generalisation of the step from real to
complex — so what changes is *what one number is*, which is the data type itself. On that reading
RingCNN belongs in the format chapters, not in the background.

**Superseded draft verdict, kept for the record:** this file originally recorded `NON-Q-ORIENTED`
on the swap-for-INT8 test — the ring algebra, the `n×` MAC reduction, the `R_I` selection argument
and the RCONV engines all survive it, and only a 0.1–0.2 dB tail dies. The ruling is that **the
algebra is the type here**, which the swap test does not detect: swapping the *bit field* for INT8
leaves the ring intact precisely because the ring lives one level above the bit field. Recorded
because it is a limit of the swap test worth knowing, not because the verdict is still open.

**The honest counter-case, for the human to weigh.** Two things pull the other way, and neither is
frivolous. (i) The *decision* that produces the design is a fixed-point-cost argument: under a
multiplication count `R_H` and `R_I` tie, and only the `w_x × w_g` column separates them, so
"quantization" (in the sense of finite operand width) genuinely selects the architecture. (ii)
Without component-wise Q-formats the proposed ring's quality advantage over plain group convolution
partly evaporates, so the quantization mechanism is load-bearing for the *claim*, if not for the
*speedup*. If the human weighs "what decided the design" above "what survives the swap", `Q` is
defensible — and that is the reading the human adopted, on the stronger data-type ground above.

**Taxonomy box: §1.1, with a real claim on §2.2 — not §1.2.** §1.2 is reserved for papers "whose
point **is** the new type… beyond a normal fixed-length exponent and mantissa". RingCNN's number is
a plain 8-bit fixed-point value with a per-layer binary point, cited to an ARM debugger guide. What
changed is the *object above* the number — a weight block, not a weight. §1.1 says a paper belongs
there "when it merely *uses* such a type rather than proposing a new one", which is exactly this.
The component-wise Q-format then earns it a place in **§2.2 fine-grained granularity**, alongside
BiScale/OLAccel/GOBO/BFP, as the corpus's only *strided* sub-tensor grouping. Filing it in §1.2
would put an unchanged 8-bit fixed-point value next to Posit and ANT.

---

## For the note

**§1 one-line summary.** Leaves the number alone — **8-bit dynamic fixed point throughout** — and
changes what a weight *is*: each `n×n` block of real weights becomes one `n`-tuple **ring** element,
dropping the block from `n²` to `n` degrees of freedom, and because a fixed-point multiplier costs
`w_x × w_g` the ring that wins is the one whose transforms are the **identity** (`R_I` — literally
an `n`-group group convolution, 8×8-bit multipliers, no operand widening), with the lost channel
mixing pushed out of the multiplication and into a **directional ReLU** `H·ReLU(H·y)` evaluated
on-the-fly in full precision on the 24-bit accumulator output under **`n` Q-formats per layer, one
per ring component**; 40 nm layout at n=2/4 gives the convolution engines **2.00×/3.84× energy and
2.08×/3.77× area** over the same author's real-valued eCNN — **1.85×/3.12× for the whole chip** — at
**+0.01 / −0.11 dB** average PSNR.

**Proposed tags — two changes from the seed row, both on the format axes.**

| Axis | Value | Evidence |
|---|---|---|
| **Level** | `ALGO+ARCH` | ALGO: the RingCNN framework, the `grank` search over sign/permutation matrices, the directional ReLU, the training and quantization recipe (Table III). ARCH: eRingCNN, RCONV engines, the on-the-fly `f_H` pipeline, 40 nm layout. **Checked against the `SYS` rule**: no compiler, no ISA, no software-stack figure — the 8 KB "Program" ROM is inherited eCNN plumbing, not a contribution. Seed agrees |
| **Q-oriented** | **`Q-ORIENTED`** — *seed confirmed; human ruling 2026-09-14* | Real → complex → **ring element**: the value itself changes kind, so the data type is the contribution. Supersedes this file's draft `non-Q`, which came from the swap-for-INT8 test — that test misses the ring because the ring sits above the bit field |
| **Data type** | **`FIXED` `INT8`** — *drops the seed's `ADAPTIVE`, adds `INT8`* | "Dynamic 8-bit" (Tables V, VII, VIII); 8-bit features and weights (§III-D, §VI-A); 24-bit accumulator, 33-bit non-linearity datapath. **The word "adaptive" appears zero times in the paper** (grepped). A per-layer moving binary point is dynamic fixed point, not an `ADAPTIVE` type in TAXONOMY's ANT/Flint sense — the *type* never changes, only the scale |
| **Generation** | `G2` | Representation-and-architecture co-design with no LLM, no outlier concept, no codebook and no weight-only asymmetry. Seed agrees. **Caveat worth one line in §5:** on the *numeric* axis alone this is `G1` — an inherited 2001 ARM Q-format applied to a network. Its `G2`-ness comes from designing a representation jointly with the datapath, where "representation" means the algebra rather than the number |
| **Optimization** | `algebraic sparsity` `ring algebra` `group convolution` `directional ReLU` `component-wise Q-format` `dynamic fixed-point` `on-the-fly non-linearity` `computational imaging` `40 nm layout` | Seed has the first, second, fourth and fifth. **`group convolution` should be there** — it is what `R_I` is, in the paper's own words — and `on-the-fly non-linearity` is the actual hardware contribution |

**§4 fairness verdict.** *(the note's table last row)*

> **Iso-node, iso-format, iso-dataflow, iso-throughput** — the baseline is the author's own eCNN at
> 40 nm, dynamic 8-bit, UHD30, with the real-valued models retrained *up*. Post-layout, **no
> silicon**. **Not to quote bare:** 41 TOPS and 19.1/28.4 TOPS/W (both *equivalent*, and the latter
> on a lower unexplained power); 2.00×/3.84× (engines only — whole chip 1.85×/3.12×). Diffy
> comparison node-projected, **not iso-area**.

**Proposed venue-list row** — for `QuantArchSurvey/venues/ISCA/README.md` line 77. **Reported, not
applied.** One cell changes: `FIXED ADAPTIVE` → `FIXED INT8`. **`Q` is confirmed, not changed.**

```
| [ ] | [RingCNN: Exploiting Algebraically-Sparse Ring Tensors for Energy-Efficient CNN-Based Computational Imaging](https://arxiv.org/abs/2104.09056) | *close read* | ALGO+ARCH | Q | `FIXED` `INT8` | G2 | `algebraic sparsity` `ring algebra` `group convolution` `directional ReLU` `component-wise Q-format` `dynamic fixed-point` `on-the-fly non-linearity` `computational imaging` | **Not a bit-field change — a change of what a number is**: real → complex → ring element. The bit field stays dynamic 8-bit fixed point while the `n×n` weight block loses `n²−n` degrees of freedom. The one real quantization idea is a **granularity** — `n` feature Q-formats per layer, one per ring component. 41 TOPS is *equivalent*, not delivered; 2.00×/3.84× is engines only |
```

**Proposed changes to `survey/TAGS.md`** — **reported, not applied** (other agents are reading in
parallel and the human owns that file):

- **Drop `new-data-type`** from RingCNN. TAGS.md defines it as "the numeric format itself is the
  contribution… Taxonomy §1.2". RingCNN's numeric format is inherited dynamic 8-bit fixed point.
  That would take tag (1) from 7 papers to 6 and change the reverse index at line 46 and the matrix
  row at line 164.
- **Keep** `analytical-dtype` (a fixed-point value is formula-decoded), `dtype-granularity` (the
  component-wise Q-format is precisely a new granularity), and `accelerator`.
- **Consider adding** a tag for structural/algebraic reformulation, which would group RingCNN with
  `SmartExchange` and `SingularBit`; none of the 14 covers it, and `combined-dtype` does not fit
  (a RingCNN value has one component, not several).

## Note from the source list

> **Keywords:** dynamic quantization with component-wise Q-formats

Confirmed verbatim in the paper: "a novel directional ReLU block, including **dynamic quantization
with component-wise Q-formats**, is devised to replace their real-valued counterparts" **(verified,
§V, p8)**. The keyword names the paper's quantization content exactly — and, read carefully, also
concedes how small it is relative to the ring.

## Abstract (verbatim, arXiv:2104.09056v1)

> In the era of artificial intelligence, convolutional neural networks (CNNs) are emerging
> as a powerful technique for computational imaging. They have shown superior quality for
> reconstructing fine textures from badly-distorted images and have potential to bring next-
> generation cameras and displays to our daily life. However, CNNs demand intensive
> computing power for generating high-resolution videos and defy conventional sparsity
> techniques when rendering dense details. Therefore, finding new possibilities in regular
> sparsity is crucial to enable large-scale deployment of CNN-based computational imaging.
> In this paper, we consider a fundamental but yet well-explored approach -- algebraic
> sparsity -- for energy-efficient CNN acceleration. We propose to build CNN models based on
> ring algebra that defines multiplication, addition, and non-linearity for n-tuples
> properly. Then the essential sparsity will immediately follow, e.g. n-times reduction for
> the number of real-valued weights. We define and unify several variants of ring algebras
> into a modeling framework, RingCNN, and make comparisons in terms of image quality and
> hardware complexity. On top of that, we further devise a novel ring algebra which
> minimizes complexity with component-wise product and achieves the best quality using
> directional ReLU. Finally, we implement an accelerator, eRingCNN, in two settings, n=2 and
> 4 (50% and 75% sparsity), with 40 nm technology to support advanced denoising and super-
> resolution at up to 4K UHD 30 fps. Layout results show that they can deliver equivalent 41
> TOPS using 3.76 W and 2.22 W, respectively. Compared to the real-valued counterpart, our
> ring convolution engines for n=2 achieve 2.00x energy efficiency and 2.08x area efficiency
> with similar or even better image quality. With n=4, the efficiency gains of energy and
> area are further increased to 3.84x and 3.77x with 0.11 dB drop of PSNR.
