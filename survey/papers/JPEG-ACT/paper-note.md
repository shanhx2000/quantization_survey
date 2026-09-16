# JPEG-ACT: Accelerating Deep Learning via Transform-Based Lossy Compression

**Venue / Year:** ISCA 2020, pp. 860-873 · **Link:** https://doi.org/10.1109/ISCA45697.2020.00075 (DOI second-hand — the archived copy is an author PDF with no IEEE banner) · **Reader:** Haoxuan · **Date:** 2026-09-14

## Tags

| | |
|---|---|
| **Level** | `ALGO+ARCH` |
| **Q-oriented** | `Q-ORIENTED` |
| **Data type** | `INT8` `FP32` `MIXED` |
| **Generation** | `G2` |
| **Optimization** | lossy activation compression · training offload · DCT transform coding · per-channel INT8 scale normalization (SFPR) · learned quantization table · power-of-two shift quantization · rate-distortion objective · zero-value coding · piecewise DQT schedule · DMA-side CDU |

## 1. One-line summary

Two quantizers in series on the **training activation stash**: **SFPR** casts FP32 → **INT8
per-channel** (`s_c = 1.125 / max_{n,h,w}|x|`, symmetric, saturating) and is mandatory on every
tensor — worth **4×** on its own — after which an **8×8 DCT** and a **64-entry power-of-two
quantization table learned offline by SGD** against `O = (1−α)λ₁H + αλ₂L₂` (DC entry frozen at 8
so batch norm survives) take it to **8.5× at −0.38% average accuracy**, with **ZVC** replacing
Huffman because activation spectra are flat where image spectra are not; the hardware is **new RTL
at the DMA engine**, **1.48 mm² / 1.36 W** and 77% DCT, buying **2.61× over vDNN and 1.59× over
GIST** purely as PCIe bandwidth — the compute datapath never sees anything but FP32, but the lossy
value does reach the gradient.

## 2. Data type

**It does quantize values.** The sheet's "compresses spatial info instead of values" is wrong: `4×` of the `8.5×` is plain value-domain INT8, and three of Table II's four tensor rows never reach the DCT.

**Formats, per tensor class.** conv/sum → SFPR **INT8** + DCT + power-of-two SH + ZVC. ReLU→conv → **INT8** SFPR only. ReLU→other → **1-bit** BRC sign mask (borrowed from Gist). pool/dropout → **INT8** + ZVC. Weights, gradients, forward pass: **FP32**, untouched.

**Quantizer 1 — value domain.** `y = clip([2⁷·s_c·x], −128, 127)`, `s_c = S/max_{n,h,w}|x_{nchw}|`, `S = 1.125` global. **Per-channel**, group = all `N·H·W` of one channel. Saturating, not truncating. `S` is one number for every network and layer.

**Quantizer 2 — transform domain.** 64 step sizes, one per DCT frequency, **restricted to powers of two** (3-bit log-DQT, 8 modes per frequency) → effective width `8 − s` bits, per frequency. Learned offline: SGD + forward finite differences on `O = (1−α)λ₁H + αλ₂L₂`, 240 activations from a frozen ResNet50/CIFAR10 at epoch 5. `α = 0.025` optL, `0.005` optH. **One table for all conv layers of all seven model/dataset pairs.**

**Outliers. None.** No outlier path, no second datapath. Large values are simply clipped (`S = 1.125`); the error budget is spent by *frequency*, not by *value*.

**Escape hatches, four.** DC coefficient's step fixed at 8, outside the optimizer, because batch norm reads the mean. Last four convs + all FC: no DCT. Any tensor with `NCH < 8` or `W < 8`: SFPR only. And everything the SMs compute on is FP32 — reconstruction happens before the crossbar.

**Accumulator / internal DCT width: not reported.** 64 B per 64-coefficient block implies 8-bit coefficients, but an 8-bit-input 2D DCT has ~3 bits of gain and the paper never says where they go.

**Neither PTQ nor QAT — a third setting.** No checkpoint to quantize, no quantized deployment. Train from scratch with the lossy stash in the loop; out comes an ordinary FP32 model. The error lands on the **gradient** (`∇w* = ∇y ∘ x*`), so the criterion is convergence, not post-hoc degradation.

**Why per-channel, in the paper's own terms.** Minimum per-channel range on the ResNets is 0.16 → GIST's DPR uses **15% of 256 codes**, SFPR **66%**. Utilisation, not outliers.

## 3. Optimization

**The pipeline, and where it sits.** Four CDUs between the GPU crossbar and the PCIe DMA engine — *not* cache-side, for two named reasons: Volta has 48 memory partitions (48 replicated units), and an 8×8 block spans eight cache lines that are interleaved across partitions, so a cache-side DCT would need inter-partition traffic. A round-robin collector (forward) and splitter (backward) multiplex the four variable-length streams onto one PCIe stream, one block per cycle. Compressing into HBM instead is rejected outright: a single activation can be 1 GB. **So this buys interconnect, not capacity — the opposite trade from Gist.**

**SFPR.** Eight SPE lanes: FP multiply by `s_c`, saturating cast to INT8, 32 B in / 8 B out per crossbar sector; inverted on the backward path. Its real job is **scale normalisation** — without it, compression ratio swings wildly across channels and networks, and channels with range < 1.0 quantize to all zeros. `s_c` is meant to come free from batch-norm statistics; **the paper does not model its cost.**

**DCT and the alignment buffer.** Eight Loeffler 8-point 1D DCT units (11 mults, 29 adds each = 88 multipliers), two passes with a transpose, four cycles each. A 256 B alignment buffer converts linear NCHW addresses into 8×8 blocks — and it is sized *by the format*: eight 128 B cache lines compressed to 8 bits per activation. Tensors are zero-padded in W to a multiple of 8 and, after reshaping `R^{N×C×H×W} → R^{NCH×W}`, in NCH; only the two ImageNet ResNets need it, at 6.4% / 3.0% storage. The DCT+iDCT is **229 118 µm², 77% of a CDU** — the design's whole cost is the transform.

**SH replaces DIV; ZVC replaces RLE+Huffman.** Both swaps are hardware-motivated and both are enabled by a property of activations rather than images. SH: powers of two turn the quantizer into 64 parallel shifts, **12 507 → 1 593 µm² (−88%)**, at the price of 8 modes per frequency — acceptable because no single frequency matters much. ZVC: activation spectra scatter zeros across mid *and* high frequencies where images bunch them in high-frequency runs, and the optimized DQTs' flat profile randomises them further, so a mask beats run-lengths — **1.12× more compression and 125 890 → 21 519 µm² (5.85× smaller)**. Together: ~1.5× area, ~1.3× power, and up to 1.44× compression (on optL; 1.03× on optH).

**optL5H — the convergence fix is a schedule.** optH alone diverges on WRN/CIFAR10 and collapses ResNet50/ImageNet to **28.9%**, diagnosed as the compressed activation *mean* dragging the batch-norm parameters. Two mitigations: freeze the DC step size, and run optL for the first five epochs then switch to optH. That recovers 71.6% at 5.9×. It is also, quietly, a modification to the training schedule — which §VII claims the method does not need.

**Cost.** 1.48 mm² / 1.36 W at 15 nm, four CDUs plus buffers, collector and splitter. **Plus three extra crossbar ports at 2.25 mm² / 1.668 W, which the table excludes.** Past 4 CDUs the memory partitions bind; a cache-side SFPR variant costs 48 replicated units and buys 1%.

## 4. Results

| | |
|---|---|
| Baseline | **vDNN** (uncompressed offload), **cDMA+** (cDMA's ZVC moved DMA-side so placement matches), **GIST** — both re-implemented, no public source. FP32 uncompressed for compression ratios |
| Models / datasets | VGG-16, ResNet18/50/101, WRN on CIFAR10 + ImageNet; VDSR on Div2K. 7 model/dataset pairs |
| Accuracy delta | **−0.38% average at 8.5×** (optL5H); optL **+0.07% at 6.7×**; GIST −1.07% at 4.5×; SFPR alone −0.12% at 4.0×. optH **−9.58%** with two non-converged runs (WRN 91.8%, **ResNet50/ImageNet 28.9% vs 71.7%**). VDSR 35.6 → 35.4 dB PSNR. Reported statistic is **best validation score over training**, not final |
| Compression | **8.5×** average (optL5H) vs 5.8× stock jpeg80, 4.5× GIST, 1.3× cDMA+. Effective offload 108.8 GB/s = 8.5 × 12.8 GB/s PCIe (analytical) |
| Speedup | **2.61× vs vDNN**, **1.59× vs GIST**, 1.12× vs JPEG-BASE(jpeg80). Abstract's 2.4× has no body source |
| Energy / area | **1.48 mm² / 1.36 W**, "<1% of a Titan V". DCT+iDCT = 77% of a CDU. Crossbar +3 ports (2.25 mm² / 1.668 W) excluded |
| Technology node | 45 nm FreePDK45, Synopsys DC, **analytically scaled to 15 nm** + 50% wire overhead |
| Evidence level | **Three setups, never pooled:** Chainer functional simulation, full training runs (accuracy), ratios computed offline at batch 8; GPGPU-Sim cycle-level on **three CNR blocks** per network at batch 16 (speedup); post-synthesis, scaled node (area/power). No silicon |
| **Is the comparison fair?** | Iso-baseline and iso-workload (GIST and cDMA both re-implemented, same simulator, same seven pairs); **not iso-experiment** — accuracy is full Chainer training, speedup is three CNR blocks in GPGPU-Sim, area is 45 nm scaled to 15 nm. Accuracy is **best-over-training**, not final. **Do not quote:** 2.4× (abstract; no body source), 8.6× optH (two runs diverge), "<1% power" (excludes 1.67 W of crossbar ports) |

## 5. Comment

## 6. Claude notes

*Suggestions from the reading agent. **Strip this section before copying into
`QuantArchSurvey/venues/ISCA/notes/`.***

- **Read depth.** Full close read of all 14 PDF pages, §I-§VIII and Tables I-V. Figures 2/6/10/16-21 are rasterised — **no number here comes from a figure**. Four things unresolved, all in `ANALYSIS.md`: **the total number of training epochs is never stated anywhere** (so "converged" cannot be checked); the internal precision of the DCT datapath; whether Table I's ratios are net of the 3-6.4% padding; and where the abstract's 2.4× comes from.
- **The seed tag I most want you to look at: `non-Q` → `Q-ORIENTED`.** The seed carries the sheet's "compresses spatial info instead of values". §VI-E refutes it in the paper's own words: *"The minimum compression rate is 4× due to the mandatory use of SFPR."* SFPR is Eqns 4-5, `m = 8`, per-channel symmetric INT8 with a clip factor — a textbook value-domain quantizer — and it runs on every tensor, including the three of four Table II rows that never see the DCT. `quantiz*` appears 34 times. On the ENEC precedent (you ruled `Q-ORIENTED` on the weaker ground that the design is merely *conditioned on* the float format) this is inside by a wide margin.
- **Also disputed: `ARCH` → `ALGO+ARCH`, `—` → `INT8` `FP32` `MIXED`, `—` → `G2`.** Level: SFPR's scale-normalisation rule, the DQT rate-distortion optimizer and the optL5H schedule are algorithms no hardware executes, and two of the paper's four contribution bullets are algorithmic. Checked `SYS` — does not apply. Generation is consequential on the Q call.
- **`POW2` considered and rejected, deliberately.** SH restricts DQT entries to powers of two, but those are quantization *step sizes* — scales, not a value encoding. Same distinction you drew on Tender and that AQB8 cites. Recorded so nobody re-litigates it.
- **AQuant and JPEG-ACT are *not* the same idea six years apart, and the difference is the paper.** JPEG-ACT borrows the **codec algorithm** (intra-frame: DCT + quantization table) and builds every gate itself — `texture`, `codec`, `video`, `reuse`, `repurpos` all **zero hits**. AQuant borrows the **codec silicon** (inter-frame: motion estimation as reference+delta) and builds almost none. Complementary halves, not a repeat. The sharpest line for the survey: the 2020 paper, with no codec to reuse, still thought the transform worth **229 118 µm² of new DCT logic** — which is the best available evidence that AQuant's "the hardware is free" is an argument about *area*, not about *value*.
- **The box question — my recommendation is to take it off the no-box list.** It has a real value-domain quantizer delivering half the compression, plus a *learned* step-size table in the transform domain. What it needs is a **sub-box with Gist: training-time activation quantization**, where the quantized tensor is a **backward-pass operand** and the accuracy criterion is convergence rather than one forward pass. That leaves the no-box list as `SpZip` + `CommutativeDataReordering`, and optionally `IBMCompressionAccelerator` as the lossless corner.
- **It splits the compression-vs-arithmetic axis into two questions.** "Does the datapath see the compressed form?" is not enough. ENEC: no / no value changed. **JPEG-ACT: no / yes, and the changed value perturbs the gradient.** Ecco: no / yes. Everyone else: yes / yes. JPEG-ACT occupies the cell nothing else does — furthest from the datapath, and the only one of that group whose error reaches a gradient.
- **A new entry for the outlier-currency table, and it costs nothing.** No outlier path at all; large values are clipped. What it *does* protect is the **DC coefficient — the block mean — because batch norm reads it**. "Protect the statistic the next layer consumes" is a distinct currency, alongside re-anchoring (AQB8) and compressibility (Ecco).
- **Granularity: a kind the corpus has no other instance of.** SFPR is per-channel; the DQT is **per-frequency**, 64 groups inside an 8×8 block — groups defined by a **basis function**, not by a tensor index.
- **Numbers I would exclude.** (i) **2.4×** — the abstract's headline, unreproducible from any sentence or table; body says 2.61× vs vDNN, 1.59× vs GIST. (ii) **1.98× over GIST** — Table I's averages give 8.5/4.5 = **1.89×**. (iii) **8.6× (optH)** — two divergent runs. (iv) **"<1% power"** — Table V is captioned "Crossbar excluded" while Table IV prices the three added ports at 1.668 W; together that is **1.21%** of a 250 W Titan V. (v) §VI-F's *"area and power by 1.3× and 1.5×"* is **reversed** — Table V gives area 1.46×, power 1.34×, and §III-F states it correctly.
- **§5 material, if you want it.** `G2`, and it is useful *because* it is 2020: none of the three G3 threads is present (grep: `outlier` 0, `codebook` 0, `transformer` 0), yet it both designs a numeric representation — 64 learned power-of-two step sizes against a rate/distortion objective — and builds the architecture that produces and consumes it. Same call and same reasoning as AQB8. Best-citation claim: **the corpus's only entry where the quantization error is applied to a gradient thousands of times rather than to one forward pass**, and the only one that reports what that costs (three non-converged runs, printed, not hidden).
- **`survey/TAGS.md`, reported not applied.** Tags stay `training` `gpu-kernels` `accelerator`. But `gpu-kernels` fits badly: the CUDA/Chainer code is *evaluation infrastructure*, not the contribution — the contribution is RTL. Consider dropping `gpu-kernels` and adding a lossy-compression tag, since `lossless-compression` currently has no lossy counterpart and Gist would want the same one. Your call; I changed nothing.
