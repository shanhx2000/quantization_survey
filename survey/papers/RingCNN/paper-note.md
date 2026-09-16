# RingCNN: Exploiting Algebraically-Sparse Ring Tensors for Energy-Efficient CNN-Based Computational Imaging

**Venue / Year:** ISCA 2021 · **Link:** https://arxiv.org/abs/2104.09056 · project page + video: https://www.ee.nthu.edu.tw/chaotsung/RingCNN/index.html · **Reader:** Haoxuan · **Date:** 2026-09-14

## Tags

| | |
|---|---|
| **Level** | `ALGO+ARCH` |
| **Q-oriented** | `Q-ORIENTED` |
| **Data type** | `FIXED` `INT8` |
| **Generation** | `G2` |
| **Optimization** | algebraic sparsity · ring algebra · group convolution · directional ReLU · component-wise Q-format · dynamic fixed-point · on-the-fly non-linearity · computational imaging |

## 1. One-line summary

Leaves the number alone — dynamic 8-bit fixed point throughout — and changes what a weight
*is*: each `n×n` block of real weights becomes one `n`-tuple **ring** element, dropping the
block from `n²` to `n` degrees of freedom, and since a fixed-point multiplier costs
`w_x × w_g` the winning ring is the one whose transforms are the **identity** (`R_I` —
literally an `n`-group group convolution, 8×8-bit multipliers, no operand widening), with
the lost channel mixing pushed out of the multiply and into a **directional ReLU**
`H·ReLU(H·y)` evaluated on-the-fly in full precision on the 24-bit accumulator under **`n`
Q-formats per layer, one per ring component** — 40 nm layout at n=2/4 buying **1.85×/3.12×
whole-chip energy** at **+0.01 / −0.11 dB** PSNR.

## 2. Data type

**Formats.** Dynamic 8-bit fixed point, weights and features alike. No new encoding — the Q-format scheme is inherited from ARM [1] and the author's own eCNN [21]; only the *component-wise* refinement is new.

**Granularity.** Weights: one Q-format per layer. Features: **`n` Q-formats per layer, one per ring component** (n = 2 or 4). That per-component split is the paper's only actual quantization contribution.

**Accumulator.** 24-bit at n=4 entering the non-linearity; the non-linearity datapath runs full precision to **33 bits**, 5 of them component-alignment left-shifts.

**Outliers.** **None** — the word does not appear in the paper. The only distributional problem named is saturation after `f_H`, and it is fixed with granularity, not with an outlier path.

**Escape hatch.** The `f_H` block: no requantization between the two Hadamards. Inserting one (24→8 bit at n=4) costs **up to 0.2 dB**.

**Retraining.** Neither PTQ nor QAT on a stock checkpoint — the ring model is a *different architecture*, converted structurally from a real-valued backbone and **trained from scratch**, then quantized to 8 bits and fine-tuned.

**DoF, not bitwidth.** Compression is `n×` on weights (`n²` → `n` per block) at unchanged element precision. Features are untouched: an `n`-tuple holds `n` real activations, so the feature volume equals the real-valued network's.

## 3. Optimization

**Ring tensors.** `z = g · x` with `g` the weights, `x` the features; matrix form `z = G x`, `G` built from the weights and multiplying features from the left. `G` is `n×n` with only `n` degrees of freedom — that is the "algebraic sparsity", and it is a **structural constraint on the weights**, not sparsity in the pruning sense. The general fast algorithm transforms both operands, `z = T_z((T_g g) ∘ (T_x x))`, cutting multiplications from `n²` to `m ≥ grank(M)`.

**Why `R_I` wins.** A fixed-point multiplier costs `w_x × w_g`, so any ring whose transforms widen an operand pays for its own multiplication saving. `R_I` sets `T_g = T_x = T_z = I`, `G = diag(g_0…g_{n−1})`, and the product collapses to `z_i = g_i x_i` — a component-wise product on plain 8×8-bit multipliers. Selected over `R_H4-I` (CirCNN-alike) and `R_H4` (HadaNet-alike) by **1.8×** and **1.5×** area efficiency at ≈0.1 dB more PSNR. `R_I` is exactly `n`-group group convolution.

**Directional ReLU buys the mixing back.** `f_dir(y) ≜ U f_cw(V y)`, instanced as `f_H(y) ≜ H f_cw(H y)` with `H` Hadamard. The proposed ring is the *pair* `(R_I, f_H)` — a multiplication and a non-linearity — not `R_H`: the Hadamards touch only the **accumulated** output, so weights never pass through a transform and both multiplier operands stay 8-bit. This is where the channel mixing that `R_I` gave up is recovered, at **3.4% / 8.9%** of RCONV engine area.

**eRingCNN.** eCNN (MICRO'19) with the real-valued convolution engine replaced by an RCONV engine and the ReLU block by the on-the-fly directional-ReLU pipeline; everything else inherited. `(32/n)`-channel `n`-tuple in/out per cycle over a 4×2 spatial tile. Weight SRAM 1288 → **972 / 492 KB** (not 640/320 — eCNN's parameter compression was dropped and the memory grown 1.5×); feature SRAM and DRAM bandwidth **unchanged** at 1570 KB / 1.93 GB/s.

## 4. Results

| | |
|---|---|
| Baseline | Author's own eCNN (MICRO'19), real-valued, same node/dataflow/throughput. Also Diffy (node-projected), SparTen, TIE, CirCNN, magnitude pruning, LeGR |
| Models / datasets | ERNet family — denoising (CBSD68 σ=25) and SR×2/×4 (Set5/Set14/BSD100) at HD30 and UHD30; ResNet-56 / CIFAR-100 in Appendix C |
| Accuracy delta | vs eCNN, quantized: **+0.01 dB (n=2), −0.11 dB (n=4)** avg PSNR. Float→8-bit costs a further −0.11 / −0.12 dB. Loses to software SOTA in one cell: UHD30 denoise n=4, **−0.21 dB** vs FFDNet |
| Speedup | Throughput is *equivalent* 41.0 TOPS for both n. **Delivered arithmetic 20.48 (n=2) / 10.24 (n=4) TOPS** |
| Energy / area | **Whole accelerator: 1.85× energy / 1.64× area (n=2), 3.12× / 2.36× (n=4)**. RCONV engines alone: 2.00×/2.08× and 3.84×/3.77×. 33.73 mm² · 3.76 W and 23.36 mm² · 2.22 W |
| Technology node | TSMC 40 nm, 250 MHz |
| Evidence level | **post-layout** (IC Compiler + PrimeTime PX) for area/power; **post-synthesis** for the ring-choice sweep and the TOPS/W table; simulation for all PSNR; **analytical node projection** for Diffy. No silicon |
| **Is the comparison fair?** | Iso-node, iso-format, iso-dataflow, iso-throughput (own eCNN at 40 nm, dynamic 8-bit, real-valued models retrained up). Post-layout, no silicon. **Not to quote bare:** 41 TOPS and 19.1/28.4 TOPS/W (both *equivalent*, the latter on a lower unexplained power); 2.00×/3.84× (engines only — whole chip 1.85×/3.12×). Diffy node-projected, not iso-area |

## 5. Comment

Accuracy is evaluated **only by PSNR**. No more common accuracy metric is reported for the
computational-imaging models. (The single exception is Appendix C's ResNet-56 / CIFAR-100 top-1,
which is a side experiment, not the main evaluation.)

## 6. Claude notes

*Suggestions from the reading agent. **Strip this section before copying into
`QuantArchSurvey/venues/ISCA/notes/`.***

- **Read depth.** Full close read of §I–§VIII and Appendix C. **All eight tables are bitmaps** — `pdftotext` recovers only captions, so Tables I–VIII were read by rendering pages at 250 dpi; numbers marked *(read off Fig. N)* in `ANALYSIS.md` are approximate. Taken on trust and not re-derived: the n=4 exhaustion yielding exactly two non-isomorphic grank-4 permutations (Appendix A/B, CP-ARLS `grank` search). Not resolved: the sub-column split of Table II's transform matrices for `C`, `R_H4-I`, `H` — not needed, the chosen ring uses identity transforms.
- **`Q-ORIENTED` settled by the human 2026-09-14, on the data-type reading**: real number → complex number → **ring element**. A value stops being a scalar and becomes an `n`-tuple in a ring, which is a change to *what one number is* — the data type itself — so the seed's `Q` stands. (My draft had argued `non-Q` from the swap-for-INT8 test, on the grounds that the ring algebra and the RCONV engines survive it. The ruling is that the algebra **is** the type here, which the swap test does not see.)
- **One seed-tag dispute remains: `FIXED` `ADAPTIVE` → `FIXED` `INT8`.** **"adaptive" appears zero times** (grepped); a per-layer moving binary point is dynamic fixed point, not `ADAPTIVE` in TAXONOMY's ANT/Flint sense — the *type* never changes, only the scale.
- **Where I would place it.** Not in the data-type boxes at all. It belongs with **SmartExchange** and **SingularBit** as structural/algebraic reformulation — and it is the cleanest of the three, because it is honest that the number is unchanged. Worth proposing a **"structural reformulation"** axis; `combined-dtype` does not fit (a RingCNN value has one component, not several).
- **§5 material, if you want it.** The `G2` call is on paradigm: representation-and-architecture co-design, no LLM, no outliers, no codebook. But on the *numeric* axis alone this is `G1` — a 2001 ARM Q-format applied to a network. Its `G2`-ness comes from co-designing a representation with the datapath where "representation" means the **algebra**, not the number. That is worth one sentence, because it is the paper's most interesting property and the reason it strains the taxonomy.
- **The number I would exclude: "equivalent 41 TOPS."** Both configs report 41.0 because both serve the same real-valued model (`MACs × 2 × f × n`). Stripped of "equivalent" it is a **4× overstatement at n=4**, which does *half* the arithmetic of n=2. The paper is internally consistent — it applies "equivalent" to SparTen/TIE/CirCNN too — but the word is load-bearing.
- **Three more hazards** (full list in `ANALYSIS.md`): two unreconciled power figures for the same chip (Table V layout 3.76/2.22 W vs Table VIII "synthesis" 2.14/1.45 W, and the TOPS/W come from the lower pair); Table VIII is not iso-anything (45/28/45 vs 40 nm, recognition vs imaging, 8/16/16 vs dynamic 8), and **TIE reports 72.9 TOPS/W on FC — higher than eRingCNN's 28.4** — stated in prose but not reflected in the table's bolding; Table IV is float while Fig. 13 is fixed point, so the headline gains over FFDNet/SRResNet are floating-point models.
- **`survey/TAGS.md`: `new-data-type` should now STAY** — my draft recommended dropping it, and the `Q-ORIENTED` ruling withdraws that. If the ring element is the new data type, RingCNN satisfies "the numeric format itself is the contribution" at the algebra level even though the *bit field* is inherited dynamic 8-bit. No edit needed to that file. Keep `analytical-dtype`, `dtype-granularity`, `accelerator` as they are.
- **Appendix C undercuts the generality claim** and is easy to miss: on ResNet-56/CIFAR-100, LeGR structured pruning **beats** the ring at 2× and 4×; the ring only wins at 8×. The method is a computational-imaging result first.
