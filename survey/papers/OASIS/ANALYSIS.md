# OASIS — paper notes

**OASIS: Outlier-Aware LUT-Based GEMM with Dual-Side Quantization for LLM Inference Acceleration**
Xueying Wu, Baijun Zhou, Zhihui Gao, Yuzhe Fu, Qilin Zheng, Yintao He, Hai Li
**ISCA 2026** (2026 ACM/IEEE 53rd Annual International Symposium on Computer Architecture),
pp. 307–321 ｜ DOI: **10.1109/ISCA66397.2026.00036**
Publication info verified 2026-09-02 from the **official ISCA 2026 proceedings package**
(title, authors, pages, DOI and abstract all read from its `assets/data/data.js`).
Archived here: **the published proceedings PDF** (`506501a307.pdf`, 15 pages) — not a preprint.

Status: **note ready** ｜ Last updated: 2026-09-03
Tags: `lut-accelerator` `non-analytical-dtype` `combined-dtype` `mixed-precision`
`dtype-granularity` `accelerator`
(**Proposed addition**: `dtype-granularity` — per-output-channel weight scales and per-token
activation scales over a *globally shared* codebook is a granularity design, not an inherited
default. `survey/TAGS.md` not edited.)
How far it was read: **close read of §I–§VII** — introduction, §II (LLM quantization, LUT-GEMM
schemes, outlier handling), §III (quantization scheme, WAQ LUT-GEMM, look-ahead + error
compensation), §IV (architecture, Table II), §V.A–§V.D (all of evaluation incl. Tables III–IV
and all seven ablations) and the conclusion. **Skimmed:** §VI related work, references.
Figures 11–18 were read for their prose claims; per-bar values not transcribed.
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> The PDF is **not committed** (1.2 MB). It came from the proceedings package a human
> supplied, now archived at [`archieve/ISCA 2026.zip`](../../../archieve/), entry `pdfs/5065-3nexm57sBmVa6MJtFTiSrb/506501a307/506501a307.pdf`.
> **There is no public URL for it** — this is not an arXiv paper. Re-extract with
> `python3 extract.py` → `extracted/` (committed, greppable).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, 2026 row.

---

## Brief

### 1. Motivation

LLM quantization is caught between three bad options: weight-only quantization pays a
**dequantization cost that can be 20–90% of GEMM runtime**; integer weight-and-activation
quantization is cheap but loses quality; and non-uniform weight-and-activation quantization
fits LLM distributions best but **cannot run on conventional low-precision units at all**.

### 2. Overview

A LUT-based architecture that executes GEMM between **non-uniformly quantized weights AND
activations** — dual-side — with no dequantization. The enabling mechanism is **precomputed
Cartesian-Product LUTs**, giving a 64× smaller table and 1024× more parallelism than prior
LUT GEMM. Accuracy under aggressive activation quantization is protected by keeping the top
0.5% and bottom 0.5% of activations in FP16 on a parallel error-compensation path, fed by
**Orizuru**, a top-k detection engine.

### 3. Pros and cons

**Pros**

- Dual-side non-uniform quantization is the part nobody had made work in hardware; the
Cartesian-product table is what makes it tractable rather than a combinatorial blow-up.
- Two parallel branches — LUT GEMM for inliers, FP16 compensation for outliers — is a clean
separation that keeps the common path uniform.
- 1.94% average accuracy drop from FP16, **6.34% better than Atom**, with 3.00× speedup and
1.44× energy efficiency over the FIGLUT accelerator.

**Cons**

- Top-k outlier detection is an online cost on every activation tensor; Orizuru is optimized
(its min-tree initialization saves 50% of comparisons) but it is still dedicated hardware
that must keep up with the datapath.
- Accuracy degrades noticeably at the aggressive end — 2.05% at W4A4 but **5.90% at W4A3** —
so the usable operating range is narrower than the headline suggests.
- Compared against LUT and INT-WAQ baselines; no direct comparison against the microscaling
line ([`MicroScopiQ`](../MicroScopiQ/ANALYSIS.md)) that attacks the same accuracy problem
differently.

### 4. Where it applies

The 2026 head of the **LUT + non-analytical data type** thread, and the first to push non-
uniform quantization to *both* GEMM operands. Read directly after
[`LUTTensorCore`](../LUTTensorCore/ANALYSIS.md).

---

## Conclusions

**Read in full 2026-09-03.** The brief survives, with one number corrected and one
mechanism sharpened.

**Corrected — the brief's headline accuracy numbers are the paper's own error, inherited.**
The brief says *"1.94% average accuracy drop … 6.34% better than Atom"*. Those are the
**LLaMA-2-7B numbers alone**, not averages. The paper states the figure three different ways
and only one is derivable:

| Where | Avg. drop vs FP16 (W4A4) | Better than Atom |
|---|---|---|
| Abstract | 1.98 % | 5.18 % |
| §I Introduction | 1.94 % | 6.34 % |
| **§V-B (correct)** | **2.05 %** | **6.44 %** |

Table IV gives three models: LLaMA-2-7B 70.49→68.55 (−1.94), LLaMA-3-8B 75.09→72.06 (−3.03),
Mistral-7B 74.99→73.80 (−1.19); mean **2.05 %** (**verified**, arithmetic checks). The gaps to
Atom are 6.34 / 10.16 / 2.83, mean **6.44 %**. So the abstract and the introduction both
misreport their own result, and the introduction has substituted one model for the average.
**Cite §V-B's 2.05 % / 6.44 %, never the abstract's.**

**Sharpened.** The brief calls the Cartesian-product table "64× smaller". That is the
analytical figure for one configuration; the *measured* comparison (Fig. 16) is **62.1× vs
FIGLUT and LUT Tensor Core, 994.2× vs LUT-GEMM**, and the deeper point is that the table is
**constant in size regardless of reduction length** — which is what actually distinguishes it.

---

## Method

**Verified** unless marked. Pages are `extracted/506501a307.pages/pNN.txt`.

**The trilemma it attacks** (§I, Fig. 1). Weight-only quantization must dequantize to FP16
before the GEMM, and that step is **20–90 % of GEMM runtime**. Integer weight-and-activation
quantization (INT-WAQ) runs natively but loses accuracy. Non-uniform WAQ — learned codebooks —
fits LLM distributions best but is *index-coded*, so existing units must dequantize it too,
losing the advantage again.

**The central move: quantizing both sides makes the table static.** Prior LUT-GEMM (FIGLUT,
LUT Tensor Core, LUT-GEMM) stores **inner products** of a group of μ activations against
weight patterns. Because activations stream, that table must be regenerated on the fly, its
size is `2^μ`, and μ must stay small (μ = 4), which forces partial-sum reductions across
`K/μ` groups. OASIS instead stores the **Cartesian product of the two codebooks** — every
(weight centroid × activation centroid) pair. Both codebooks are learned offline, so:

- the LUT is **precomputed before inference** and loaded on-chip — no runtime generation;
- its size is `2^(nW+nA)` = **256 entries at W4A4**, and **independent of reduction length**;
- reduction becomes a **weighted sum over occurrence counts** of unique concatenated indices,
  cutting FP16 additions from `K` to `2^(nW+nA)` — 4096 → 256 for LLaMA-7B's `q_proj`.

Analytically, for `M=1, K=N=4096, nW=nA=4`: **64× smaller LUT, 1024× larger group size, 16×
fewer reduction FLOPs** (§II-B, §III-B). Measured over `q_proj` across LLaMA sizes (Fig. 16):
**62.1× / 994.2× smaller** than FIGLUT-LUT-Tensor-Core / LUT-GEMM, and **497.1× / 248.6×**
fewer reduction FLOPs.

**Quantization scheme** (§III-A, §V-A). K-Means learned codebooks both sides. **Weights:**
4-bit, the *entire matrix shares one set of centroids*, each **output channel** has its own
scaling factor, **no outlier protection on weights at all**. **Activations:** 3- or 4-bit,
**per-token**, centroids learned offline from **16 C4 calibration samples** using
weighted K-Means with Fisher-information weights; indices computed online.

> ⚠️ **Internal inconsistency worth noting.** §III-A says *"each token has its own set of
> quantization centroids and scaling factors"*, but §V-A says centroids are *"trained offline
> … and the indices are computed online"*. Only the latter can be true — per-token online
> centroids would make the Cartesian LUT non-static and destroy the paper's premise. Read
> §V-A as operative: **globally shared centroids, per-token scale**.

**Outliers** (§II-C, §III-C). Activation outliers only. Top **0.5 %** largest and bottom
**0.5 %** smallest values kept in **FP16** — 1 % total. Detection is **dynamic**, justified by
Fig. 3: offline-vs-online outlier thresholds have RMSE 0.32–0.38 (low similarity), while
Fig. 5 shows offline-vs-online *centroids* have RMSE 0.01 — so centroids can be learned
offline but thresholds cannot. **The look-ahead trick**: instead of scanning, splitting, then
computing, both branches run concurrently — the main branch quantizes *everything* including
outliers and ignores their error; the outlier branch computes that error and compensates.
Mathematically identical, but detection leaves the critical path. **Orizuru** is the top-k
engine: twin max/min tournament trees with **shared leaf nodes**.

**Hardware** (§IV, Table II). 16 PE Lines; each has **4096 Concat Units** (the whole PE is a
4-bit + 4-bit → 8-bit concatenation into a register), 32 16-in Index Counters, 1 dequant unit,
a 32-in FP16 MAC tree for reduction, and **8 FP16 MAC units for the outlier branch**. Chip
total **15.31 mm², 9.66 W** at TSMC 28 nm. The main GEMM datapath contains **no multiplier** —
concatenate, count, look up, weighted-sum.

## Key numbers, with their frame

**Frames.** Accuracy on an **A100-80GB**, HuggingFace Transformers, sequence length 2048.
Hardware from a **cycle-accurate simulator modified from DnnWeaver**, with core-logic area and
power from **TSMC 28 nm synthesis**, SRAM from **Cacti**, HBM from **DRAMSim3** (§V-A). **No
silicon.** Unless stated, hardware results are **single-batch decoding**, output length 2048.

| Setting | Model | Metric | Baseline | Result | Source |
|---|---|---|---|---|---|
| **W4A4 accuracy (the correct figure)** | LLaMA-2-7B, LLaMA-3-8B, Mistral-7B (3 models) | Zero-shot avg drop vs FP16 | FP16 | **2.05 %**; **6.44 %** better than Atom, **6.92 %** better than QuaRot | §V-B, p315 · Table IV |
| **W4A3 accuracy** | same 3 models | Zero-shot avg drop | FP16 | **5.90 %**; 8.79 % better than Atom, 30.44 % better than QuaRot | §V-B, p315 |
| PPL, W4A4 | LLaMA-2-7B | WikiText-2 | FP16 = 5.47 · Atom = 6.12 · QuaRot = 6.19 | **5.90** (Δ +0.43, 34 % less than Atom's) | Table III, p315 |
| PPL, W4A4 | LLaMA-3-8B (quantization-sensitive) | WikiText-2 | FP16 = 6.14 · Atom = 8.10 | **7.11** (Δ +0.97; 49 % less than Atom's) | Table III, p315 |
| PPL, W4A3 | LLaMA-2-7B | WikiText-2 | FP16 = 5.47 · Atom = 11.40 | **7.49** (Δ **+2.02**) | Table III, p315 |
| Dynamic vs static outlier thresholds | LLaMA-2-7B | PPL gain of dynamic | OASIS-S (offline thresholds) | **−0.05 at W4A4, −0.27 at W4A3** | §V-B, p315 |
| Throughput, single-batch decode | LLaMA family | Speedup | A100 / QuaRot-on-A100 / **FIGLUT (W4A16)** | OASIS-A4 **5.41× / 3.12× / 3.00×**; A3 5.67× / 3.27× / 3.15× | §V-C, p316 · simulator |
| Energy efficiency, same | same | × improvement | A100 / QuaRot / FIGLUT | OASIS-A4 **198.1× / 108.8× / 1.44×**; A3 206.5× / 113.6× / 1.51× | §V-C, p316 |
| Low-batch decode (BS 1/2/4) | LLaMA-2-7B/13B | Speedup / energy | avg over baseline accelerators | 3.41× / 3.73× and 26.43× / 28.20× | §V-D.1, p316 |
| Prefill/decode length sweep | LLaMA-2-7B/70B | Speedup | FIGLUT | **2.80× / 2.93×**; larger gain on 70B (more input channels) | §V-D.2, p317 |
| Look-ahead benefit | LLaMA-2-7B, 1 % outliers | Throughput | OASIS-C (detection on critical path) | **+16 % (A4), +18 % (A3)** | §V-D.4, p317 |
| LUT size, measured | `q_proj`, LLaMA 7B–70B | × smaller | FIGLUT / LUT Tensor Core; LUT-GEMM | **62.1×; 994.2×** — and **constant in K** | Fig. 16, p317 |
| Reduction FLOPs, measured | same | × fewer | same | **497.1×; 248.6×** | Fig. 16, p317 |
| Outlier sensitivity | LLaMA-2-7B, Mistral-7B | PPL / throughput | — | 0.5 %→1 % negligible throughput cost; **1 %→10 % the outlier branch becomes the bottleneck** | §V-D.4, Fig. 15, p317 |
| Calibration cost | LLaMA-3-8B | PPL / quantization time | 4 samples | 16 C4 samples: PPL 7.39 → **7.11**; time **42.47 → 100.52 min** at 32 | §V-D.6, Fig. 17, p318 |
| Area / power | — | mm² / W @28 nm | — | **15.31 mm² / 9.66 W** total; PE Lines 9.08 mm² (59 %), Orizuru 0.739 mm², memory controller 1.47 mm² | Table II, p313 |
| On-chip traffic / energy split | 1-4096-4096 GEMM, 1 % outliers | % | — | Weight Index Buffer **76.0 %** of traffic, LUT only **19.2 %**; energy: reduction 33.1 %, branch merging 22.1 % | §V-D.7, Fig. 18, p318 |

Left blank: **no area or power figure is given for any baseline accelerator**, so no iso-area
statement is possible (see below). Per-bar values of Figs. 11–15 not transcribed.

## Cost and requirements

- **Data type.** `W4A4` and `W4A3` — **dual-side non-uniform**, K-Means learned codebooks
  both sides. Values are *indices*, not encodings: taxonomy §1.3, and unusually the
  *activations* are index-coded too, which almost nothing else in the corpus does.
- **Granularity.** Weights: one codebook for the whole matrix, **scale per output channel**.
  Activations: **scale per token**, codebook global and offline-learned. This is the fact that
  makes the Cartesian LUT static — a finer weight or activation *codebook* granularity would
  break it. Compare the group size 128 that Atom uses, which the paper flags with a dagger in
  its own tables.
- **Outlier mechanism.** Top 0.5 % + bottom 0.5 % of **activations** in FP16, detected
  dynamically by Orizuru, compensated on a concurrent branch. **Weights get no outlier
  protection whatsoever** (§V-A) — unusual, and worth a survey sentence.
- **Escape hatch.** That 1 % of activations at FP16 → effective activation bitwidth
  ≈ 4×0.99 + 16×0.01 ≈ **4.12 bits**, plus the FP16 compensation datapath (8 MAC units per PE
  Line) and the FP16 MAC tree used for reduction. The reduction itself is FP16, so "no
  multiplier" applies to the GEMM, not to the chip.
- **Retraining: PTQ.** Post-training K-Means on stock weights; activation centroids from
  **16 C4 samples**. No QAT. But calibration is not free — 42 minutes for 16 samples on
  LLaMA-3-8B, rising to 100 minutes at 32.
- **What the hardware pays.** A dedicated top-k engine (Orizuru, 0.739 mm², 273 units), index
  counters (0.271 mm² per PE Line — **the largest single logic item inside a line**, 3× the
  Concat Units' 0.0868 mm²), a clustering unit to map activations to centroids every layer,
  and a second FP16 branch that must be sized to match the main branch at the design's 1 %
  outlier point.

## Limitations and open questions

**Authors admit:** the outlier branch becomes the bottleneck above 1 % outliers (§V-D.4);
W4A3 costs 5.90 % accuracy; calibration time grows steeply past 16 samples.

**Not admitted:**

1. **The headline hardware comparison is not iso-precision.** FIGLUT is evaluated at
   **W4A16** — weight-only, activations untouched — while OASIS is W4A4/W4A3 (§V-C, p316).
   The **3.00× speedup and 1.44× energy** therefore fold in the gain from quantizing
   activations 4× narrower, which is an algorithmic choice FIGLUT never made and which costs
   OASIS 2.05 % accuracy that FIGLUT does not pay. This is the number most likely to be
   misquoted and it should always carry "W4A4 vs W4A16".
2. **No baseline area or power is reported.** Table II gives OASIS's 15.31 mm² / 9.66 W and
   nothing for FIGLUT, so there is **no iso-area comparison anywhere in the paper**.
3. **The 198× / 108.8× energy figures compare a 28 nm ASIC to an A100 GPU.** Different node,
   different platform class, different memory system. They are reported without qualification.
4. **Abstract, introduction and §V-B disagree** on the headline accuracy (see Conclusions).
   Two of the three are wrong.
5. **Zero-shot averages cover 3 models; the PPL table covers 11.** The "average accuracy drop"
   is over LLaMA-2-7B, LLaMA-3-8B and Mistral-7B only.
6. **§III-A and §V-A contradict each other** on whether activation centroids are per-token or
   global (see Method). The paper's whole premise needs them global.
7. **Weight index traffic is 76 % of on-chip memory traffic** (§V-D.7). The design removes
   dequantization and shrinks the LUT, but the dominant cost is simply streaming weight
   indices — so the LUT-size victory over FIGLUT addresses 19.2 % of the traffic.

## Relation to other entries

- **The third pole of the LUT thread, and the reason to read all three together.**
  [`LUTTensorCore`](../LUTTensorCore/ANALYSIS.md) builds an **eager per-tile** table
  (precompute all `2^(K−1)` entries for each activation tile, and spend the whole software
  contribution making that precompute cheap).
  [`TransitiveArray`](../TransitiveArray/ANALYSIS.md) builds a **lazy per-tile** table (only
  the entries that occur, one add each). OASIS builds **no table at runtime at all** — the
  Cartesian product of two codebooks is a compile-time constant.
  **The survey claim this supports: quantizing both operands is what converts a runtime table
  into a static one.** That is the cleanest organizing idea §5.6 has, and it is
  `**inferred / not verified**` as a framing — the papers do not state it, though OASIS names
  offline computability as opportunity (1) of three.
- **Direct baseline it beats:** FIGLUT and, by citation, `LUTTensorCore` — Fig. 16 measures
  both, treating them as one design point (both halve the table via MSB-negation).
- **Outlier thread:** shares the inlier/outlier split with [`OliVe`](../OliVe/ANALYSIS.md),
  [`OLAccel`](../OLAccel/ANALYSIS.md) and [`MicroScopiQ`](../MicroScopiQ/ANALYSIS.md), but is
  the only one that takes detection **off the critical path** rather than making it cheaper.
  The brief's con stands: **no comparison against the microscaling line.**
- **Codebook thread:** [`Mokey`](../Mokey/ANALYSIS.md) (indices into fixed-point centroids)
  and [`EVA`](../EVA/ANALYSIS.md). OASIS extends it to *both* operands, which none of them do.
- **Non-corpus baselines carrying the paper:** Atom, QuaRot, SmoothQuant, FIGLUT — all
  outside ISCA. Third consecutive paper with this pattern.

## For the note

### §1 one-line summary

> Quantizes **both** weights and activations to 4-bit learned K-Means codebooks, which makes
> the lookup table the **Cartesian product of the two codebooks** — 256 static entries,
> computed offline and independent of reduction length — so GEMM becomes concatenate indices,
> count occurrences, and take a weighted sum of table entries, with the top and bottom 0.5 %
> of activations compensated in FP16 on a concurrent branch so outlier detection never touches
> the critical path.

### Proposed values on their four axes

| Axis | Proposed | Evidence (one line) |
|---|---|---|
| **Level** | **`ALGO+ARCH`** | The quantization scheme is a contribution (weighted K-Means with Fisher weights, dual-side codebooks, the 0.5 %/0.5 % split) and so is the accelerator; neither works without the other. |
| **Q-oriented** | `Q-ORIENTED` | Swap in plain INT8 and there is no codebook, no Cartesian product, no Concat Unit — the entire datapath is an artefact of index-coded operands. |
| **Data type** | **`VQ` + `LUT` + `INT4` + `INT3` + `FP16` + `MIXED`** | K-Means learned codebooks on both operands (`VQ`), compute resolved by table (`LUT`), W4A4/W4A3 with 1 % of activations escaping to FP16 (`MIXED`). |
| **Generation** | **`G3`** | Codebook thread taken further than anyone else in the corpus — to *both* GEMM operands — plus the outlier thread. Not weight-only; it is explicitly the argument *against* weight-only. |
| **Optimization** (free text) | `LUT-GEMM` `Cartesian-product-LUT` `dual-side-quantization` `NU-WAQ` `learned-codebook` `outlier-aware` `look-ahead-compensation` `top-k-engine` `tournament-tree` | — |

### Proposed venue-list row

```
| [x] | OASIS: Outlier-Aware LUT-Based GEMM with Dual-Side Quantization for LLM Inference Acceleration | ALGO+ARCH | Q | `VQ` `LUT` `INT4` `INT3` `MIXED` | G3 | `LUTGEMM` `dual-side` `outlier-aware` `top-k` | Cartesian-product LUT over two learned codebooks — static, 256 entries, independent of reduction length; 0.5%+0.5% activation outliers compensated on a concurrent branch |
```

### §4 fairness verdict

**Iso-node yes, iso-precision no, iso-area unknowable.**

- **Iso-node ✓ for the ASIC comparison** — OASIS and FIGLUT both TSMC 28 nm, same simulator
  methodology.
- **Iso-precision ✗, and this is the headline's weak point.** FIGLUT runs **W4A16**; OASIS
  runs **W4A4/W4A3**. The 3.00× speedup and 1.44× energy include the benefit of quantizing
  activations 4× narrower — a gain OASIS pays 2.05 % accuracy for and FIGLUT pays nothing for.
  Quote it only as "W4A4 vs W4A16".
- **Iso-area unknown** — no baseline area or power is reported anywhere.
- **Iso-platform ✗ for the GPU numbers.** 198.1× / 108.8× energy over A100 and QuaRot compares
  a 28 nm ASIC against a GPU. Not an architecture comparison.
- **Iso-accuracy ✓ against the algorithm baselines, and carefully done.** Atom's group-size-128
  advantage is disclosed with a dagger in both tables, and OASIS still wins.
- **Self-consistency ✗.** The abstract (1.98 %/5.18 %) and introduction (1.94 %/6.34 %) both
  misstate the paper's own average. **§V-B's 2.05 % / 6.44 % is the only derivable version.**

## Abstract (verbatim, ISCA 2026 proceedings)

> Large language models (LLMs) have demonstrated impressive capabilities across a wide range
> of applications, but demand substantial memory and compute resources during inference.
> Existing quantization methods expose a trade-off between efficiency and accuracy: weight-
> only quantization (WOQ) incurs costly dequantization overheads, while integer weight-and-
> activation quantization (INT-WAQ) reduces precision and degrades model quality. Non-
> uniform weight-and-activation quantization (NU-WAQ) better captures the distributions of
> LLM weights and activations, yet remains incompatible with conventional low-precision
> compute units. This paper presents OASIS, a lookup table (LUT)-based architecture that
> enables efficient general matrix multiplication (GEMM) between non-uniformly quantized
> weights and activations without requiring dequantization. OASIS employs precomputed
> Cartesian product LUTs, achieving a 64× reduction in LUT size and enabling 1024× higher
> computational parallelism compared to existing LUT-based GEMM methods. To preserve
> accuracy under aggressive activation quantization, OASIS introduces an outlier-aware
> quantization scheme with concurrent LUT-based GEMM and error compensation for outliers.
> Furthermore, we design Orizuru, an efficient top-k detection engine for real-time
> activation outlier identification. According to extensive evaluations, OASIS incurs an
> average accuracy drop of only 1.98% compared to the FP16 baseline, which is 5.18% lower
> than Atom. On the hardware side, OASIS achieves an average 3.00× speedup and a 1.44×
> improvement in energy efficiency compared to the FIGLUT accelerator.
