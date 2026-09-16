# JPEG-ACT — paper notes

**JPEG-ACT: Accelerating Deep Learning via Transform-Based Lossy Compression**
R. David Evans, Lufei Liu, Tor M. Aamodt
**ISCA 2020**, pp. 860-873 ｜ DOI: **10.1109/ISCA45697.2020.00075**
Publication info verified 2026-09-02: **the archived PDF carries no DOI and no IEEE banner**
(grepped, not assumed; re-grepped 2026-09-14 — `DOI`, `10.1109` and `ISCA45697` all return **zero
hits** in the full text) — venue and title come from its own page 1; **DOI and page range come
from the IEEE Xplore record surfaced via search**, and are second-hand.
Archived here: an **author-hosted copy, not the IEEE version** — no IEEE proceedings banner on page 1, and the filename is the author's.
The two versions were **not compared**. 14 pages.
**Page citations below are PDF pages of this author copy** (`extracted/…​.pages/pNN.txt`), *not*
IEEE printed pages, because the printed page numbers are not in the file.

Status: **note ready** ｜ Last updated: 2026-09-14 ｜ **Human-checked 2026-09-14** — tags confirmed, including the reclassification to `Q-ORIENTED` — SFPR is a mandatory per-channel INT8 quantizer worth half the compression, so the source CSV's "compresses spatio info instead of values" is refuted and the paper comes off the "no box" list.
Tags: `training` `gpu-kernels` `accelerator`
How far it was read: **full close read of all 14 PDF pages.** Line by line: §I, §II-A/B (all five
prior-work subsections and the JPEG walkthrough), §III-A through §III-G (system placement, SFPR,
alignment buffer, DCT, DIV/RLE, SH/ZVC, collector/splitter), §IV (the DQT optimization, Eqns 6-12),
§V (methodology), §VI-A through §VI-F (all six evaluation subsections), §VII, §VIII, and Tables
I-V. **Skimmed:** the 72-entry reference list, checked only for the baselines (vDNN [19], cDMA
[21], GIST [13]), the tool citations (GPGPU-Sim [45]-[47], FreePDK45 [62], LLM DCT [52], OpenCores
RLE [53]/[54]) and the BFP/DPR ancestry ([32], [38], [49]).
**Read from figure text only, and therefore weak:** Figs. 2, 6, 10, 16, 17, 18, 19, 20, 21 are
rasterised plots — axis labels and legends survive extraction, **bar and line values do not**.
Every number below comes from prose or from Tables I-V, never from a figure.
**Not resolved** (itemised under `Limitations and open questions`): the total number of training
epochs (never stated anywhere); the internal precision of the DCT datapath; whether Table I's
compression ratios include the 3.0-6.4% padding overhead; and where the abstract's headline
**2.4×** comes from, since no sentence or table in the body produces it.
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> Publisher record: https://ieeexplore.ieee.org/document/9138963/
> **There is no arXiv version** (arXiv API title search, 2026-09-02). The PDF was downloaded by a
> human and filed through [`survey/uploads/`](../../uploads/) — the sanctioned route when the
> arXiv-only rule leaves a paper unreachable; see
> [`Notes-002`](../../../Claude/notes/Notes-002-paper-source-access.md).
> The PDF is **not committed** (1.8 MB) and **cannot be re-downloaded by script** —
> both publishers 403. Re-extract with `python3 extract.py` → `extracted/` (committed).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, ISCA 2020 row.

---

## Brief

**What the close read changed** (one line, per the reading protocol): the brief said the paper is
"orthogonal to the data-type axis of the taxonomy" on the strength of the source list's *"compresses
spatio info instead of values"* — **that is wrong, and it is the most important correction here**:
JPEG-ACT's first stage, **SFPR, is a value-domain per-channel INT8 quantizer with a tuned clipping
factor, it is mandatory on every compressed tensor, and it alone delivers 4× of the headline 8.5×**
(§VI-E, PDF p. 13: *"The minimum compression rate is 4× due to the mandatory use of SFPR"*).
Two further brief-level claims fail on the close read: the design **does not reuse any existing GPU
codec or texture hardware** (`texture`, `codec`, `video`, `reuse`, `repurpos` — **zero hits** in the
full text; the CDU is new RTL), and the "2.4× / 1.6×" abstract framing does not match the body's
2.61× / 1.59×. Everything else in the brief stands.

### 1. Motivation

Training large CNNs requires stashing activations that exceed GPU memory (ResNet50/ImageNet
needs >40 GB against a 12 GB Titan V), so they are offloaded to CPU memory — and the PCIe
transfer, not the compute, becomes the cost. Prior activation compression relied on sparsity,
which deep ResNets do not have: with batch norm, **up to 60% of activation storage is dense**
(§VI-B, PDF p. 11), and the sparse methods of GIST and cDMA cap at 4× dense.

### 2. Overview

A **lossy** activation offload accelerator that exploits *spatial correlation* in CNN activations
rather than sparsity. Four stages in sequence: **(1) SFPR** — per-channel max-scaled FP32→INT8
cast with a global clip factor `S = 1.125`; **(2) 8×8 2D DCT**; **(3) SH** — per-frequency
power-of-two quantization by a 64-entry table learned offline against a rate-distortion objective;
**(4) ZVC** — zero-value mask coding. Stages 1 and 3 are both quantizers; stage 2 is the transform
that makes stage 3 pay. The units sit **at the DMA engine**, not in the cache hierarchy and not in
the SMs.

### 3. Pros and cons

**Pros**

- The right insight for the right workload — CNN activations retain image-like spatial
correlation 40 conv layers deep (Fig. 6), so a codec's transform is a natural fit, and it works
where sparsity-based schemes have nothing to exploit.
- **2.61× over vDNN, 1.59× over GIST at 8.5× compression and −0.38% average accuracy**, in
1.48 mm² / 1.36 W — **verified** (§VI-D, Tables I and V). Under 1% of a Titan V's area and power
*as the paper accounts for it*.
- Explicitly engineers for convergence rather than just reporting final accuracy: the DQT
optimization objective is derived from the *gradient* error (Eqns 6-9), and the two-stage optL5H
schedule exists because the first five epochs are the fragile ones.
- **Honest about its failures.** Table I prints three non-converged runs with an asterisk,
including a **28.9% vs 71.7%** collapse on ResNet50/ImageNet, and §VI-B diagnoses them (diverging
batch-norm mean) rather than hiding them.

**Cons**

- The spatial-correlation premise is CNN-specific; transformer activations have no analogous 2D
structure, so this does not carry to LLM training.
- **One DQT, tuned on one model** (ResNet50/CIFAR10 at epoch 5, 240 sample activations), is
applied to all seven model/dataset pairs — and the aggressive variant of it destroys
ResNet50/ImageNet. The transfer is asserted by the results table, not established.
- Speedup and accuracy come from **different experiments at different batch sizes**: accuracy
from full Chainer training runs, speedup from a GPGPU-Sim microbenchmark of **three CNR blocks**
per network at batch 16, compression ratios from an offline pass at batch 8.
- The source list flags it as compressing *"spatio info instead of values"* — **the close read
rejects this**: it does both, and the value-domain half is the mandatory half.

### 4. Where it applies

The lossy counterpart to [`Gist`](../Gist/ANALYSIS.md) in the **training + compression** cluster,
and the corpus's clearest case that *where the quantized value is consumed* (a backward-pass
operand, not an inference operand) is a distinct axis. Also the **algorithm** half of the
codec-borrowing pair whose **silicon** half is [`AQuant`](../AQuant/ANALYSIS.md), ISCA'26.

---

## Method

**Where it sits.** DMA-side, not cache-side (§III-A, Fig. 7, PDF p. 4). The baseline is a Titan-V-
class GPU with HBM and PCIe DMA to CPU DRAM. Compression/Decompression Units (CDUs) are added
between the GPU crossbar and the DMA engine, with a **collector** (forward) and **splitter**
(backward) multiplexing four CDUs onto one PCIe stream by round-robin, one 8×8 block per cycle.
**verified** (§III-A, §III-G). Cache-side placement — what cDMA does — is rejected for two named
reasons: 48 memory partitions on Volta would need 48 replicated CDUs, and a JPEG block spans up to
eight cache lines, which on a GPU are interleaved across partitions, so a cache-side DCT would need
inter-partition communication. **verified** (§III-A, PDF p. 4).

**Stage 1 — SFPR (Scaled Fix-point Precision Reduction): this is a value-domain quantizer.**
`s_c = S / max_{n,h,w}|x_{nchw}|` and `y_{nchw} = clip([2^{m−1} s_c x_{nchw}], −2^{m−1}, 2^{m−1}−1)`
with `m = 8` — per-channel symmetric max scaling into signed INT8, round-to-nearest, saturating
(not truncating) cast. **verified** (§III-B Eqns 4-5, PDF p. 5; §III-B "Casting of out-of-range
values saturates"). `S` is a single global clip hyper-parameter, **`S = 1.125`, one value across
all networks and layers**, chosen by minimising recovered-activation L2 error jointly for SFPR,
JPEG-BASE and JPEG-ACT (Fig. 10). Sensitivity is low: mean error rises by `5.0 × 10⁻⁵` across
`S ∈ [0.5, 1.25]`. **verified** (§III-B, PDF p. 5).
The stated reason SFPR beats GIST's DPR is **integer-range utilisation**: on the ResNets, the
minimum per-channel activation range is 0.16, which uses **15% of the 256 available DPR codes
against 66% for SFPR**. **verified** (§VI-B, PDF p. 11). That is a per-channel-scaling argument,
made in exactly the terms the quantization literature makes it.
Hardware: eight SPE lanes, a 2-stage FP multiplier and a float→int cast each, 32 B in / 8 B out per
crossbar sector; the backward path is int→float then `× 1/s_c`. **verified** (§III-B, Fig. 11).
The `s_c` computation itself is **not measured** — the paper says it can be taken from the batch-
norm statistics already computed, or sampled, and declines to model it. **verified as an omission**
(§III-B, PDF p. 6: *"We do not measure scaling factor calculation"*).

**Stage 2 — 8×8 2D DCT.** Eight 8-point Loeffler (LLM) 1D DCT units, 11 multiplies + 29 adds each
→ 88 multipliers; two passes with a transpose between, four cycles per pass. The iDCT is the same
structure inverted plus a normalising shift stage. **verified** (§III-D, Fig. 13, PDF p. 7).
An **alignment buffer** (256 B = four JPEG blocks = eight 128 B cache lines compressed to 8 bits
per activation) converts the linear NCHW address space into 8×8 (H×W) blocks; its size is *derived
from the 8-bit format*. Activations are zero-padded in W to a multiple of 8 and, after reshaping
`R^{N×C×H×W} → R^{NCH×W}`, in NCH. Only ResNet18/ImageNet and ResNet50/ImageNet need padding:
**6.4% (H,W) and 3.0% (NCH,W) storage overhead on ResNet50**. **verified** (§III-C, PDF pp. 6-7).

**Stage 3 — the second quantizer, and the paper's real numeric contribution.** JPEG-BASE keeps
the standard **DIV** stage: divide each of the 64 DCT coefficients by its entry in the 64-entry
Discrete Quantization Table and round to 8 bits. JPEG-ACT replaces DIV with **SH**: 64 parallel
right-shifts (left-shifts on decode) driven by a **log-DQT of 64 three-bit entries**, i.e. **DQT
values are restricted to powers of two and each frequency has 8 available quantization modes**.
**verified** (§III-F, Fig. 14, PDF p. 7). This cuts the quantizer's area by **88%** (Table IV:
12 507 → 1 593 µm², = 87.3%, arithmetic mine). The effective width of a DCT coefficient is
therefore `8 − s` bits with `s ∈ [0, 7]`, **per frequency** — a per-frequency bitwidth ladder
inside one 8×8 block. **inferred / not verified**: the paper never writes it this way, but it
follows from "8 bits after quantization" plus a 3-bit shift.

**How the DQT is chosen — offline, by SGD, against a rate-distortion objective.** Not fixed, not
the JPEG standard tables. §IV derives the objective from the *gradient* error:
`∇w* − ∇w = ∇y ∘ (x* − x)`, so to first order `‖∇w − ∇w*‖ ∝ ‖x − x*‖`, giving
`O = (1−α)λ₁H + αλ₂L₂` with `H` the Shannon entropy of the quantized coefficient matrix `q`
(the rate), `L₂` the mean recovered-activation error (the distortion), `λ₁ = 10`, `λ₂ = 10000`.
Minimised **with respect to the 64 DQT entries** by SGD (`lr = 2.0`, momentum 0) with **forward
finite-difference gradients** (difference of 5), over **240 example activations** from a frozen
ResNet50/CIFAR10 at epoch 5. **verified** (§IV, Eqns 6-12, PDF pp. 8-9).
`α` selects the operating point: **optL `α = 0.025`** (low compression, low error) and
**optH `α = 0.005`** (high compression, high error). **verified** (§IV, PDF p. 9).
**One DQT is used for all convolution layers**, and the DQT tuned on ResNet50/CIFAR10 is used for
every model and dataset in Table I. **verified** (§IV: *"with respect to the DQT for all
convolution layers"*).
**Escape hatch inside the DQT:** *"The first of the 64 DQT parameters, representing the activation
mean, is fixed to 8 to prevent instability in the batch normalization parameters."* — the DC
coefficient is excluded from the optimization. **verified** (§IV, PDF p. 9).

**optL5H — a schedule, not a table.** Piece-wise: optL for the first five epochs, optH thereafter.
Motivated by Fig. 17 (activation error is highest in the earliest epochs, from weight decay, and
flat after epoch 5) and by the literature on the critical early period. It converts optH's
catastrophic runs into optL-level accuracy at near-optH compression. **verified** (§IV, §VI-B).

**Stage 4 — coding.** JPEG-BASE uses standard **RLE + Huffman** (OpenCores IP). JPEG-ACT uses
**ZVC** (zero-value mask, from cDMA) instead, because CNN activation spectra are flat where image
spectra are not: images put their zeros at high frequency in runs, activations scatter them across
mid and high frequencies, and the optimized DQTs' flatter profile randomises them further.
ZVC over RLE is worth **1.12×** compression and **5.85× less area** (Table IV: 125 890 → 21 519
µm², arithmetic mine). **verified** (§III-F, §VI-C, PDF p. 12).

**What is applied to what** (Table II, PDF p. 10) — this table is the whole data-type story:

| Tensor class | cDMA+ | GIST | JPEG-ACT |
|---|---|---|---|
| conv or sum (dense) | none | DPR (8-bit) | **SFPR + DCT + SH + ZVC** (only if `NCH ≥ 8` and `W ≥ 8`; otherwise SFPR alone) |
| ReLU → other layer | ZVC | BRC (1-bit sign mask) | **BRC (1-bit)** |
| ReLU → conv | ZVC | DPR + CSR | **SFPR (8-bit)** |
| pool or dropout | ZVC | DPR + CSR | **SFPR + ZVC** |

**verified** (Table II). Note that **three of the four rows never see the DCT at all** — they are
plain 8-bit or 1-bit value-domain compression. JPEG is additionally skipped on the final four
convolutions and all fully-connected layers (activations too small). **verified** (§V, PDF p. 9).

**What the compute datapath sees: FP32, always.** SFPR converts back to FP32 before the crossbar
on the decompression path (§III-B ⑦). No arithmetic anywhere in the GPU is changed; weights,
gradients and the forward pass are untouched FP32. The lossy value `x*` re-enters computation only
as the **backward-pass operand** in `∇w* = ∇y ∘ x*`. **verified** (§III-B, §IV Eqns 6-9).

---

## Key numbers, with their frame

Evidence levels are **not** interchangeable and are named in every row. Three separate setups:
**(A)** Chainer functional simulation, full training runs, lossless stage skipped, compression
ratios computed offline at **batch 8**; **(B)** GPGPU-Sim cycle-level, Titan V config, PCIe 3.0 at
**12.8 GB/s effective**, **three CNR blocks** (first / middle / last) per network at **batch 16**;
**(C)** Synopsys DC post-synthesis at **45 nm FreePDK45, analytically scaled to 15 nm** with 50%
wire overhead added. **verified** (§V, PDF pp. 9-10).

| Setting | Model | Metric | Baseline | Result | Source |
|---|---|---|---|---|---|
| **Headline compression + accuracy** | 7 model/dataset pairs, average | compression ratio; Δ Top-1 / PSNR | FP32 uncompressed | **8.5×, −0.38%** (optL5H) | Table I. **verified**. Setup A |
| Low-compression variant | same | same | same | **6.7×, +0.07%** (optL) | Table I. **verified** |
| Aggressive variant | same | same | same | **8.6×, −9.58%** (optH) — **two runs diverge** | Table I. **verified**. Do not quote 8.6× |
| Prior art, lossless | same | same | same | **1.3×, 0%** (cDMA+) | Table I. **verified** |
| Prior art, lossy | same | same | same | **4.5×, −1.07%** (GIST 8-bit) | Table I. **verified** |
| Value-domain quantizer alone | same | same | same | **4.0×, −0.12%** (SFPR 8-bit) | Table I. **verified**. 4× is exactly 32/8 |
| Stock JPEG tables | same | same | same | **5.8×, −0.87%** (jpeg80, WRN diverges); **6.6×, −2.27%** (jpeg60) | Table I. **verified** |
| **Worst single run** | ResNet50 / ImageNet | Top-1 | 71.7% (uncompressed) | **28.9%** with optH — did not converge | Table I. **verified**. optL5H recovers to 71.6% |
| Second divergence | WRN / CIFAR10 | Top-1 | 95.4% | **91.8%** with optH; **92.6%** with jpeg80 | Table I. **verified** |
| Super-resolution | VDSR / Div2K | PSNR | 35.6 dB | **35.4 dB** (optL5H, 9.1×) | Table I. **verified** |
| **End-to-end speedup** | 7 networks, average | training performance | **vDNN** (uncompressed offload) | **2.61×** | §VI-D p. 12. **verified**. Setup B |
| vs prior activation compression | same | same | **GIST** | **1.59×** | §VI-D p. 12. **verified** |
| vs stock JPEG | same | same | JPEG-BASE (jpeg80) | **1.12×** performance, **2.3×** lower error change | §VI-D p. 12. **verified** |
| SFPR alone | same | same | GIST | **1.35×** — *despite lower compression*, because CSR is slower than SFPR | §VI-D p. 12. **verified** |
| **Abstract's headline** | — | training performance | *"prior offload accelerators"* | **2.4×** | Abstract only. **Not reproducible from any body sentence or table** — see hazards |
| Conv+sum compression, back-end ablation | ResNet50 / CIFAR10 | compression ratio | — | jpeg80: DIV+RLE **5.29** → SH+ZVC **5.77**; optL5H: **7.72 → 7.96**; optL: **3.52 → 5.08** | Table III. **verified**. The "1.4×" claim is optL only |
| **Area, whole design** | 4 CDUs + buffers, **crossbar excluded** | mm² | cDMA+ 0.35; SFPR 0.31; JPEG-BASE 2.16 | **JPEG-ACT 1.48 mm²** | Table V. **verified**. Setup C |
| **Power, whole design** | same | W | cDMA+ 0.26; SFPR 0.35; JPEG-BASE 1.82 | **JPEG-ACT 1.36 W** | Table V. **verified** |
| Fraction of a GPU | — | area / power | NVIDIA Titan V | **"<1% of the power and area"** | §VI-F p. 13. **verified as stated**; = 0.18% area, 0.54% power on an 815 mm² / 250 W part (**arithmetic mine, inferred**) |
| **Cost the table excludes** | — | mm² / mW | — | **Crossbar (+3 ports): 2 253 427 µm² = 2.25 mm², 1 668 mW** — *larger than the accelerator it feeds* | Table IV. **verified**; Table V says "Crossbar excluded". Including it, power is **1.21% of a 250 W Titan V** (**arithmetic mine, inferred**) |
| Where the area goes | one CDU | µm² | — | DCT+iDCT **229 118** (77% of a CDU); SFPR 44 924; ZVC+ZVD 21 519; SH 1 593 | Table IV. **verified**; percentage mine |
| Quantizer area saving | — | µm² | DIV 12 507 | **SH 1 593** = **−87.3%** (paper says 88%) | Table IV, §III-F. **verified** |
| Coder area saving | — | µm² | RLE+RLD 125 890 | **ZVC+ZVD 21 519** = **5.85×** | Table IV. **verified**; ratio mine |
| **Effective offload bandwidth** | — | GB/s | PCIe 3.0 at 12.8 GB/s | cDMA+ 15.6; SFPR 48.0; JPEG-BASE 69.6; **JPEG-ACT 108.8** | Table V. **verified as printed**, but this is **compression ratio × PCIe BW** (12.8 × 8.5 = 108.8), i.e. **analytical**, not simulated |
| CDU scaling | ResNet50 / CIFAR10 | runtime | 1 CDU | No gain past 1 CDU at 2× and 4× (PCIe-bound); at 12×, **1.08×** from 2→4 CDUs and **<0.5%** from 4→8 (memory partitions bind) | §VI-E p. 12. **verified** |
| Cache-side SFPR variant | same | runtime | 4-CDU DMA-side | **+1%**, for 48 replicated SFPR units | §VI-E p. 13. **verified**. The paper's own argument against cache-side placement |
| Padding overhead | ResNet50 / ImageNet | storage | — | **6.4%** (H,W) / **3.0%** (NCH,W) | §III-C p. 7. **verified** |
| Dense fraction | batch-norm networks | activation storage | — | **up to 60% dense** | §VI-B p. 11. **verified**. This is why sparsity methods stall |
| ZVC baseline rates | — | compression ratio | — | ReLU **2.1×**, dropout **3.9×** | §VI-B p. 10. **verified** |

### Citation hazards

1. **The abstract's 2.4× cannot be sourced.** Abstract: *"2.4× higher training performance compared
   to prior offload accelerators, and 1.6× compared to prior activation compression methods."*
   Contribution bullet 3: *"2.6× over uncompressed offload, and 1.6× over GIST."* Body §VI-D:
   **2.61× vs vDNN** and **1.59× over GIST**. So 2.6×/1.6× are vs **vDNN** and **GIST**; the
   abstract's **2.4×** is against something else — presumably cDMA+, the only other "prior offload
   accelerator" — and **that comparison appears in no sentence and no table**. Fig. 18's x-axis is
   "Performance (relative to vDNN)" but its values are not extractable. **Quote 2.61× vs vDNN and
   1.59× vs GIST; do not quote 2.4× without naming its baseline as unstated.**
2. **"1.98× over GIST" (contribution bullet 2) does not reconcile with Table I.** Table I's average
   row gives JPEG-ACT optL5H **8.5×** and GIST **4.5×**; 8.5/4.5 = **1.89×**, not 1.98×. Likely a
   per-model mean of ratios rather than a ratio of means, but the paper does not say. **Quote 8.5×
   and 4.5× and let the reader divide.**
3. **§VI-F swaps area and power.** *"reduce overall area and power by 1.3× and 1.5×,
   respectively"* — Table V gives area 2.16 → 1.48 = **1.46×** and power 1.82 → 1.36 = **1.34×**.
   §III-F states the same fact the other way round and is correct: *"decrease hardware area by
   1.5×"*. **The area saving is ~1.5×, the power saving ~1.3×; §VI-F has them reversed.**
4. **"increase compression by up to 1.4×" is an `up to`.** Table III: SH+ZVC over DIV+RLE is
   **1.44× on optL**, **1.03× on optH**, **1.09% on jpeg80**. Averaged over the DQTs actually
   deployed it is far below 1.4×.
5. **Table V's "Offload (GB/s)" row is analytical, not simulated** — it is the compression ratio
   times the 12.8 GB/s PCIe rate. Do not pool it with the GPGPU-Sim speedups.
6. **"<1% of the power and area of a modern GPU" excludes the crossbar ports the design adds.**
   Table IV prices "Crossbar (+3 ports)" at **2.25 mm² / 1.668 W** — bigger than the 1.48 mm² /
   1.36 W accelerator — and Table V is explicitly captioned *"Crossbar excluded"*. On a 250 W Titan
   V the two together are **1.21% of power** (arithmetic mine). The area claim survives; the power
   claim does not, on the paper's own numbers.
7. **Accuracy is the *best* validation score over training, not the final converged score.**
   §VI-B: *"we train all networks under compression and report the best validation score."* For a
   method whose whole risk is late-training divergence, best-over-training is the wrong statistic,
   and it is the one reported.
8. **The ImageNet baselines are 4.2% below the published numbers**, by the authors' own statement
   (cheaper augmentation, 1-crop instead of 10-crop). Self-consistent, but do not compare Table I's
   71.7% ResNet50 against the literature.
9. **Speedup and accuracy are different experiments.** 2.61× comes from three CNR blocks at batch
   16 in GPGPU-Sim; −0.38% comes from full training runs in Chainer; the 8.5× comes from an offline
   pass at batch 8. No single experiment produces the abstract's pair of claims.
10. **The DOI and page range in the header are second-hand** — the archived PDF is an author copy
    with no IEEE banner and no DOI string anywhere in it (re-grepped 2026-09-14). Cite the venue
    and year from the paper; treat `10.1109/ISCA45697.2020.00075` and `pp. 860-873` as taken from
    the Xplore record, not from the document.

---

## Cost and requirements

**Silicon.** 1.48 mm² / 1.36 W at 15 nm (analytically scaled from a 45 nm FreePDK45 synthesis,
+50% wire overhead), for four CDUs plus buffers, collector and splitter. **Plus three extra GPU
crossbar ports at 2.25 mm² / 1.67 W, which Table V excludes.** The DCT+iDCT is 77% of a CDU.
**verified** (Tables IV-V).

**Interconnect.** The design is a multi-link, multi-CDU attachment to the GPU crossbar precisely
so it is not link-limited; the paper says its residual overhead is *"congestion on the GPU
interconnect from the increase in DMA traffic"* (§VI-D). At 12× compression the bottleneck moves
to the memory partitions (§VI-E). So the cost is not just the CDU area — it is crossbar bandwidth
and three ports.

**Framework.** Padding and reshaping are done in software (`R^{N×C×H×W} → R^{NCH×W}`, W padded to
a multiple of 8), and the paper stresses that reshaping *"requires no data movement as only the
indices are changed, and padding in this manner requires no framework modifications"* (§III-C).
The per-channel scales `s_c` must come from somewhere — batch-norm statistics or sampling — and
**their cost is explicitly not modelled**.

**Training-time cost, and it is real.** `optL5H` requires switching the DQT at epoch 5, i.e. a
**modification to the training schedule** — which sits awkwardly against §VII's claim that, unlike
reduced-precision training, JPEG-ACT needs no *"modification of the CNN framework, network
architecture, and training schedule."* The DQT itself must be produced by an offline SGD +
finite-difference search over 240 activations from a partially-trained donor network.

**Retraining category: neither PTQ nor QAT.** There is no pretrained checkpoint to quantize and no
quantized deployment target. Networks are trained **from scratch with the lossy stash in the
loop**, and the model that comes out is an ordinary FP32 model. This is a third setting the
survey's PTQ/QAT vocabulary does not name: call it **lossy-in-the-loop training**, where the
quantization error lands on the gradient and the accuracy question is *convergence*, not
*post-hoc degradation*.

**Accumulator / internal precision: not reported.** The paper gives no internal width for the DCT
datapath. Figs. 13-14 imply 8-bit coefficients (64 B per 64-coefficient block) and the iDCT has a
"normalizing shift stage", but an 8-bit-input 2D DCT has ~3 bits of gain, so either the transform
is scaled internally or headroom is being spent. **inferred / not verified — flag before citing
any bitwidth for the transform domain.**

---

## Limitations and open questions

**The authors' own.**

- Non-convergence is diagnosed but not solved: *"We suspect that activation compression is
  affecting the activation mean, causing divergence of the mean-dependent batch normalization
  parameters... More investigation into the training dynamics of CNNs under error is required to
  fully understand this issue."* (§VI-B). The two mitigations — fixing the DC DQT entry, and the
  optL5H anneal — are empirical.
- Very large networks (GPipe) are excluded for memory reasons (§V).
- Compressed activations are **not** kept in HBM, only shipped over PCIe, because a single
  activation can be 1 GB (§III-A). So this buys interconnect, not GPU memory capacity — GIST buys
  the opposite.
- VDSR is 1.4-2.3× worse than the other networks and the cause is a hypothesis about cuDNN kernel
  selection, not a measurement (§VI-D).

**Not admitted, and load-bearing.**

- **One DQT for everything.** Tuned on ResNet50/CIFAR10 at epoch 5, applied to ImageNet and to a
  super-resolution network. The generalisation is never tested as a variable; the closest thing to
  a test is optH's collapse on ResNet50/ImageNet, which is evidence *against*.
- **"Best validation score"** rather than final accuracy, for a method whose failure mode is
  late divergence.
- **Three CNR blocks, not networks**, for every performance number.
- **The crossbar ports are excluded** from the "<1% of a GPU" claim.
- **No transformer, no LLM, no non-CNN workload.** The paper is explicit that the premise is
  spatial correlation in conv activations; the survey should not extrapolate.

**What I could not resolve.**

1. **The total number of training epochs is never stated** — anywhere. `epoch` appears 14 times,
   all referring to the epoch-5 snapshot or to Fig. 17's 0-20 range. So "final converged accuracy"
   cannot be distinguished from "best score in however long they ran". **Verify before citing any
   convergence claim.**
2. **Where the abstract's 2.4× comes from.** See hazard 1.
3. **Whether Table I's compression ratios are net of the 3.0-6.4% padding overhead.** The two
   numbers are reported in different sections and never combined.
4. **Internal DCT precision and overflow handling.** See `Cost and requirements`.
5. **Whether the DQT optimization was ever rerun per network.** §IV describes one run on one donor;
   Table I applies the result to seven pairs; no sentence says either way.

---

## Relation to other entries

**1. `AQuant` (ISCA'26) and `JPEG-ACT` (ISCA'20) are *not* the same idea six years apart — and the
difference is exactly the interesting part.** Both start from "a video codec already knows how to
throw away perceptually irrelevant detail, and a neural tensor tolerates the same treatment". They
diverge on what they take:

| | `JPEG-ACT` (ISCA'20) | `AQuant` (ISCA'26) |
|---|---|---|
| What is borrowed | the **algorithm**: JPEG's DCT → quantization-table → coding pipeline | the **silicon**: the SoC's H.265 encoder motion-estimation PEs, comparator trees and residual quantizer |
| Hardware added | **all of it** — new RTL for SFPR, DCT/iDCT, SH, ZVC, collector/splitter. `texture`, `codec`, `video`, `reuse`, `repurpos` = **zero hits** in the text | claimed **almost none** — the CODEC is already there and idle |
| Where the codec idea lands | data movement (PCIe offload) | compute (delta GEMM operands) |
| Codec concept used | the **transform + quantization table** (intra-frame coding) | **motion estimation** (inter-frame prediction: value = reference + delta) |
| Workload | CNN training | VLM inference |

So: **JPEG-ACT borrows intra-frame coding as an algorithm and builds the hardware; AQuant borrows
inter-frame coding as hardware and does not build it.** They are complementary halves of the same
observation, not a repeat. `AQuant/ANALYSIS.md` already states this ("borrows a *codec algorithm*
where AQuant borrows *codec silicon*") and the close read confirms it from JPEG-ACT's side. The
pairing is worth a paragraph in the survey — and the sharpest line in it is that the 2020 paper,
which had no codec silicon to reuse, still found the transform worth **229 118 µm² of new DCT
logic**, which is the strongest available evidence that AQuant's "the hardware is free" argument is
about *area*, not about *value*.

**2. Compression vs cheaper arithmetic: JPEG-ACT is at the far compression end, and it splits the
axis in two.** The axis as `Ecco` opened it asks *"does the compute datapath ever see the
compressed form?"*. For JPEG-ACT the answer is an unqualified **no** — SFPR reconstructs FP32
before the crossbar, and no multiplier anywhere in the GPU changes. But that single question is
not enough, because JPEG-ACT is **lossy** and the lossy values re-enter arithmetic as the
backward-pass operand `x*` in `∇w* = ∇y ∘ x*`. Two dimensions, not one:

| Paper | Datapath sees compressed form? | Any value changed? | Where the reconstruction happens |
|---|---|---|---|
| `ENEC` | no | **no** (bit-identical) | a different core type (AIV vector units) |
| `JPEG-ACT` | no | **yes, and it perturbs the gradient** | the DMA engine, on the PCIe path |
| `Ecco` | no | yes (k-means centroids) | between L1 and L2 |
| `Gist` | no | yes for DPR, no for the 1-bit ReLU encoding | in framework kernels on the SMs |
| every other ARCH entry | **yes** | yes | n/a — the format *is* the operand |

So JPEG-ACT is the entry that shows "compression vs arithmetic" is really two questions, and it
occupies the one cell nothing else does: **furthest from the datapath, and yet the only one of the
far group whose error reaches a gradient**.

**3. Granularity.** SFPR is **per-channel** (one scale per `c`, max over `n,h,w`), which puts it
between DRQ's per-region and Tender's per-channel on the existing ladder — with the twist that the
per-channel argument is made in *utilisation* terms (15% vs 66% of the 256 INT8 codes on ResNets)
rather than in outlier terms. The DQT is **per-frequency**, 64 groups inside an 8×8 block, and that
is a granularity the corpus has no other instance of: **groups defined by a basis function, not by
a tensor index.**

**4. Outlier currency: none, and the paper pays in a different coin.** There is no outlier path.
Large activations are simply **clipped** (`S = 1.125` clips slightly past the channel max), and the
error budget is spent by *frequency* rather than by *value*. The one value it protects is the DC
coefficient — the block mean — and it protects it because batch norm reads the mean. **"Protect the
statistic the next layer consumes"** is a distinct currency worth naming alongside re-anchoring
(`AQB8`) and compressibility (`Ecco`).

**5. `Gist` (ISCA'18) is the direct predecessor and the direct baseline.** JPEG-ACT reimplements it
(no public source) and beats it 1.59× in performance and ~1.9× in compression at less than half the
accuracy loss. It also **adopts one of Gist's encodings unchanged** — BRC, the 1-bit ReLU sign mask
— for the ReLU→other rows of Table II. The two together are the corpus's only **training-time**
activation entries, and the pair makes the cleanest statement of the training/inference split:
in inference the quantized value is an operand of one forward pass, in training it is an operand of
a gradient that is applied thousands of times.
**And they split on the Q axis, which sharpens both.** The parallel `Gist` read lands on
`NON-Q-ORIENTED` — Binarize, SSDC, the in-place rewrites, the Schedule Builder and the allocator
all survive an INT8 swap, and DPR is one encoding among several. JPEG-ACT does not survive it:
SFPR *is* the swap, and everything downstream of it (the DQT, its optimizer, the SH unit, optL5H,
ZVC's advantage over RLE) loses its referent. **Same tensor, same year-adjacent problem, opposite
Q verdicts** — a useful pair for the survey, because it shows the axis is about the mechanism and
not about the topic.

**6. The box question — recommendation.** The `survey/README.md` "Papers the taxonomy has no box
for" list should **not** keep JPEG-ACT. It contains a value-domain quantizer (`SFPR`: FP32 → INT8,
per-channel, symmetric, clipped, saturating) that runs on **every** tensor it touches and delivers
**4× of the 8.5×**, plus a second quantizer with a **learned** step-size table in the transform
domain. On the ENEC precedent — where the human ruled `Q-ORIENTED` on the weaker ground that the
design is *conditioned on* the float format — JPEG-ACT is inside by a wide margin: it does not
merely read the format, it replaces it. What it needs is not exclusion but a **sub-box**:
**training-time activation quantization**, with `Gist`, where the object being quantized is a
backward-pass operand and the accuracy criterion is convergence. That leaves the no-box list as
`SpZip` + `CommutativeDataReordering` (no numeric formats at all) and, if the human wants a
lossless corner, `IBMCompressionAccelerator`.

---

## For the note

### §1 one-line summary

> Two quantizers in series on the **training activation stash**: **SFPR** casts FP32 → **INT8
> per-channel** (`s_c = 1.125 / max_{n,h,w}|x|`, symmetric, saturating) and is mandatory on every
> tensor — worth **4×** on its own — after which an **8×8 DCT** and a **64-entry power-of-two
> quantization table learned offline by SGD** against a rate-distortion objective
> `O = (1−α)λ₁H + αλ₂L₂` (the DC entry frozen at 8 so batch norm survives) take it to **8.5× at
> −0.38% average accuracy**, with **ZVC** replacing Huffman because activation spectra are flat;
> the hardware is **new RTL at the DMA engine**, **1.48 mm² / 1.36 W** and 77% DCT, buying
> **2.61× over vDNN and 1.59× over GIST** purely as PCIe bandwidth — the compute datapath never
> sees anything but FP32, but the lossy value does reach the gradient.

### Proposed values on their four axes

| Axis | Proposed | Evidence (one line) |
|---|---|---|
| **Level** | **`ALGO+ARCH`** — **seed says `ARCH`; I disagree** | Three algorithmic contributions no hardware executes: SFPR's scale-normalisation rule and the `S = 1.125` search (§III-B, Fig. 10), the DQT rate-distortion optimizer (SGD + forward finite differences over Eqns 10-12, §IV), and the optL5H two-stage training schedule (§IV). Contribution bullets 1 and 2 of §I are both algorithms. **Checked `SYS` and it does not apply** — the Chainer/CUDA implementation is evaluation infrastructure, and §VIII's claim is that *no* framework changes are needed |
| **Q-oriented** | **`Q-ORIENTED`** — **seed says `non-Q`; I disagree** | Apply the test: swap the format for plain INT8 and SFPR *is* the swap (per-channel INT8), so the DQT, the DQT optimizer, the SH unit, the optL5H schedule and ZVC's advantage over RLE all lose their referent, and 8.5× collapses to the 4.0× of Table I's SFPR column. The **SH unit exists only to quantize** (a 3-bit-per-frequency power-of-two step table, 88% smaller than the multiplier it replaces) and the alignment buffer is sized *"to cover eight cache lines compressed to eight bits per activation"* — the format sizes the hardware |
| **Data type** | **`INT8` `FP32` `MIXED`** — **seed has `—`; I disagree** | `INT8`: §III-B Eqn 5 with `m = 8`, and Table I's "SFPR 8-bit" at exactly 4× from FP32. `FP32`: every operand the SMs see, both passes (§III-B ⑦). `MIXED`: three precisions coexist in one network by Table II — 8-bit SFPR, **1-bit BRC** on ReLU→other, and DCT coefficients at an effective `8 − s` bits that differs per frequency |
| **Generation** | **`G2`** — seed has `—` | By paradigm, not year. **Not `G1`**: the hardware is not passive and the format is not given — the 64 quantization step sizes are *learned* against a rate/distortion objective. **Not `G3`**: none of the three threads is present (no outliers, no weight-only bandwidth argument, no codebook, no LLM; grep: zero hits for `outlier`, `codebook`, `transformer`). It designs a numeric representation **and** builds the architecture that produces and consumes it — the G2 test, passed twice. Same call as `AQB8`, for the same reason |
| **Optimization** (free text) | `lossy activation compression` · `training offload` · `DCT transform coding` · `per-channel INT8 scale normalization (SFPR)` · `learned quantization table` · `power-of-two shift quantization` · `rate-distortion objective` · `zero-value coding` · `piecewise DQT schedule` · `DMA-side CDU` | Seed has three; the four that change how the paper reads are **`per-channel INT8 scale normalization`**, **`learned quantization table`**, **`power-of-two shift quantization`** and **`rate-distortion objective`** |

### Seed-tag disagreements

1. **`Q-oriented: non-Q` → `Q-ORIENTED`.** The seed follows the source CSV's *"compresses spatial
   info instead of values"*. The paper's own §VI-E sentence refutes it: *"The minimum compression
   rate is 4× due to the mandatory use of SFPR."* SFPR is a value-domain quantizer (Eqns 4-5,
   `m = 8`), it runs on every compressed tensor including the three of four Table II rows that
   never reach the DCT, and it is half the compression. There is then a **second** quantizer in the
   transform domain whose step sizes are learned. `quantiz*` appears **34 times**. This is the tag
   I most want the human to look at.
2. **`Level: ARCH` → `ALGO+ARCH`.** Same ground the revision log already used for twelve rows
   ("contributes a quantization scheme *and* the hardware to run it"). See the table above.
3. **`Data type: —` → `INT8` `FP32` `MIXED`.** With `—` a reader cannot tell that the paper's first
   stage is per-channel INT8, which is precisely the fact that decides tag 1.
4. **`Generation: —` → `G2`.** Consequential on tag 1: the ENEC precedent for leaving Generation
   blank covers *non-Q* compression papers.
5. **Optimization: keep all three seeds** (`lossy activation compression`, `DCT`, `training
   offload`) — all three are correct and grep-confirmed. **Add** the quantization terms; they are
   what is missing rather than what is wrong.
6. **The summary cell needs rewriting.** *"JPEG adapted to activations. Sheet comment: compresses
   spatial info instead of values"* — the second half should be marked as refuted, since the venue
   list is where the next reader will meet it.
7. **Consider `POW2` and reject it, deliberately.** SH restricts DQT entries to powers of two
   (§III-F), but those are **quantization step sizes, i.e. scales**, not a value encoding — the
   same distinction the human drew on `Tender` and that `AQB8` cites. Not tagged. Recorded here so
   nobody re-litigates it.

### Proposed venue-list row

```
| [ ] | [JPEG-ACT: Accelerating Deep Learning via Transform-Based Lossy Compression](https://doi.org/10.1109/ISCA45697.2020.00075) | *close read* | ALGO+ARCH | Q | `INT8` `FP32` `MIXED` | G2 | `lossy activation compression` `training offload` `DCT transform coding` `per-channel INT8 scale normalization` `learned quantization table` `power-of-two shift quantization` `rate-distortion objective` `zero-value coding` `DMA-side CDU` | **It does quantize values — the sheet comment is wrong.** SFPR (FP32→INT8, per-channel, clipped) is mandatory and worth 4× of the 8.5×; the DCT then feeds a *second* quantizer whose 64 power-of-two step sizes are learned against `(1−α)λ₁H + αλ₂L₂`. New RTL at the DMA, 1.48 mm²; the datapath still only ever sees FP32 |
```

### §4 fairness verdict (note version, ≈62 words)

> Iso-baseline and iso-workload (GIST and cDMA both re-implemented, same simulator, same seven
> pairs); **not iso-experiment** — accuracy is full Chainer training, speedup is three CNR blocks
> in GPGPU-Sim, area is 45 nm synthesis scaled to 15 nm. Accuracy is **best-over-training**, not
> final. **Do not quote:** 2.4× (abstract; no body source), 8.6× optH (two runs diverge), "<1%
> power" (excludes 1.67 W of crossbar ports).

### §4 fairness — the long form (stays here, not in the note)

**What is genuinely iso.** The baselines are the right ones and they were *re-implemented*, not
quoted: GIST has no public source, so the authors rebuilt DPR, BRC, the in-place optimizations and
Sparse-Storage-Dense-Compute for both functional and performance simulation, and cDMA was rebuilt
as `cDMA+`, a DMA-side variant, *so that its CDU placement matches JPEG-ACT's rather than
handicapping it*. Same simulator, same GPU model, same PCIe rate, same seven model/dataset pairs,
same 45 nm library for every area figure in Table V. That is careful work and it should be said.

**What is not iso — three different experiments carrying one claim.** The accuracy delta comes from
full training runs in Chainer with the lossless stage skipped and compression ratios computed
offline at batch 8. The speedup comes from GPGPU-Sim on **three CNR blocks** — first, middle and
last — of each network at batch 16, because full networks were computationally infeasible. The area
and power come from a 45 nm synthesis **analytically scaled to 15 nm** with 50% wire overhead added
by hand. No single experiment supports "8.5× at −0.38% for 2.61×", and the three should never be
pooled into one sentence.

**Not iso-accuracy against the literature.** ImageNet baselines are −4.2% versus the original
ResNet papers, stated openly (cheaper augmentation, 1-crop not 10-crop). Internally consistent,
externally not comparable.

**Not final accuracy.** "Best validation score" is the reported statistic. For a method whose
characteristic failure is a *sudden decrease in accuracy during training* — the paper's own
description of its non-convergence signature — the maximum over the trajectory systematically
flatters it. And the trajectory length is never given.

**The self-comparison that is fair, and matters most.** Table III is a clean 4 × 5 ablation
(DIV/SH × RLE/ZVC against five DQTs) on one model, and Table I prints the divergences with an
asterisk instead of dropping them. The paper does not hide its bad runs, which is more than most.

**The area claim, audited.** 1.48 mm² / 1.36 W is 0.18% / 0.54% of an 815 mm² / 250 W Titan V, so
"<1%" holds as printed. But Table V is captioned "Crossbar excluded" while Table IV prices the
three extra crossbar ports the multi-CDU design requires at **2.25 mm² / 1.668 W**. Add them and
the power is **1.21%** of a 250 W part. The area claim survives; the power claim does not.

---

## Note from the source list

> **Keywords:** a lossy activation offload accelerator for training CNNs; adapts JPEG algorithm for activation compression
>
> **Comment:** Compress Spatio Info instead of values

**Verdict on the comment: half wrong, and the wrong half is the one that placed the paper.**
JPEG-ACT quantizes values *first* (SFPR: FP32 → per-channel INT8, mandatory, 4×) and spatial
frequencies *second* (DCT + a learned power-of-two step table, taking 4× → 8.5×). "Instead of" is
false; "as well as" is true.

## Abstract (verbatim, from the archived PDF)

> A reduction in the time it takes to train machine learning models can be translated into
> improvements in accuracy. An important factor that increases training time in deep neural
> networks (DNNs) is the need to store large amounts of temporary data during the back-
> propagation algorithm. To enable training very large models this temporary data can be
> offloaded from limited size GPU memory to CPU memory but this data movement incurs large
> performance overheads. We observe that in one important class of DNNs, convolutional
> neural networks (CNNs), there is spatial correlation in these temporary values. We propose
> JPEG for ACTivations (JPEGACT), a lossy activation offload accelerator for training CNNs
> that works by discarding redundant spatial information. JPEGACT adapts the well-known JPEG
> algorithm from 2D image compression to activation compression. We show how to optimize the
> JPEG algorithm so as to ensure convergence and maintain accuracy during training. JPEG-ACT
> achieves 2.4× higher training performance compared to prior offload accelerators, and 1.6×
> compared to prior activation compression methods. An efficient hardware implementation
> allows JPEG-ACT to consume less than 1% of the power and area of a modern GPU.
