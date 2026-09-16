# MicroScopiQ: Accelerating Foundational Models through Outlier-Aware Microscaling Quantization

**Venue / Year:** ISCA 2025 · **Link:** https://arxiv.org/abs/2411.05282 (DOI 10.1145/3695053.3730989) · **Reader:** Haoxuan · **Date:** 2026-09-09

## Tags

| | |
|---|---|
| **Level** | `ALGO+ARCH` |
| **Q-oriented** | `Q-ORIENTED` |
| **Data type** | `MX` `FP4` `INT2` `INT4` `MIXED` |
| **Generation** | `G3` (outlier thread) |
| **Optimization** | outlier-aware · microscaling · pruning · Hessian · N:M structured sparsity · aligned memory · NoC (ReCoN) · systolic · multi-precision PE |

## 1. One-line summary

Keeps outliers at **2× the inlier bitwidth in MX-FP** while inliers stay **MX-INT**, and pays
for the extra outlier bits by **pruning the least important weights in the same micro-block —
chosen by Hessian, not by adjacency** — so every element still occupies a fixed bit budget with
aligned memory and homogeneous INT PEs, reaching **2.36 effective bits**, with a NoC (ReCoN)
reassembling the scattered outlier halves for 3% area.

## 2. Data type

**`bb`** = per-element bit budget = "operational bit-width of each PE". Every slot is `bb` bits.
**Formats.** Inliers MX-INT @ `bb` (2/4). Outliers MX-FP @ **2·`bb`**, split into two `bb`-sized halves; a pruned slot holds one half.
Uniform `bb` per layer **is** the alignment mechanism. `bb`=2 → EBW 2.36; `bb`=4 → EBW 4.15.
Ablated (Table 7): outliers need more bits than inliers, and **FP beats INT for outliers** (dynamic range).
**Granularity.** Macro-block shares the inlier scale; **micro-block B_μ = 8** is the unit of outlier accounting, pruning, permutation. MXScale 8b, inlier scale 7+1b.
**Outliers.** 3σ rule. Higher precision *and* different format, paid by pruning the `n` least-important inliers per μB (Hessian `argmin wₚ²/[H⁻¹]ₚₚ`) → `(B_μ−n):B_μ` pattern. Cap `n ≤ B_μ/2`.
**Accumulator.** Not reported. Multi-precision INT PEs; PE→ReCoN column bus explicitly off the critical path.
**Escape hatch.** Pruned weights + 24-bit permutation list per outlier-bearing μB.
**Retraining.** PTQ. 256 PILE samples, 30 min–9 h on one H100.

## 3. Optimization

The mutual exclusivity (Table 1): Group A (GOBO, OLAccel) keeps outliers high-precision → high
accuracy but **unaligned memory, complex PEs, EBW 18.17 bits**. Group B (OliVe) quantizes
outliers at inlier precision → aligned, EBW 2 bits, but **low accuracy**. MicroScopiQ claims all
three.

**Why OliVe fails, measured.** OliVe prunes the *neighbour*, so two adjacent outliers means a
real outlier dies. Adjacent-outlier rate: **<0.04% in BERT/OPT** (OliVe's models) vs **>0.5%
average, >2% peak in LLaMA3/LlaVa**. Two orders of magnitude. Prune by *importance* instead.

**Three steps.** (1) Split into macro/micro-blocks, separate by 3σ, inliers → MX-INT, outliers →
MX-FP at 2×. (2) Reorganise each outlier into two halves that **mimic the inlier layout** —
duplicate the sign onto each mantissa bit, `{s·m₁, s·m₀}` — so the LSB half fits a slot the PE
already knows how to read. (3) Prune the `n` least-important inliers by Hessian and write the
Lower halves there; a per-μB permutation list records where each went.

**Why alignment follows.** Every element occupies exactly `bb` bits, one datatype per layer →
homogeneous PE array, regular access. Table 1 identifies alignment as the real discriminator,
and this is how Group-A accuracy becomes reachable at Group-B cost.

**ReCoN.** A NoC that reassembles split outliers and routes partial sums, so the PE array never
knows an outlier was scattered. Amortised: **3% area at 128×128** with one unit, 11% with eight.
Power: PE array 56%, on-chip memory 37%, **ReCoN 5.9%** (7.7% on outlier-heavy VILA-7B).

## 4. Results

| | |
|---|---|
| Baseline | Algorithms: OmniQuant, AWQ, GPTQ, Atom, SDQ. Co-designs: OliVe, GOBO. Accelerators: OliVe, ANT, GOBO, OLAccel, AdaptivFloat, MTIA, Eyeriss-v2. GPU: TensorRT-LLM FP16, Atom W4A4 |
| Models / datasets | OPT, LLaMA2, LLaMA3, Phi-3, Mixtral; VLMs OpenFlamingo, VILA, LlaVa; CNN (ResNet50, VGG16) and SSM (VMamba, Vim). WikiText2 PPL + 6 LLM benchmarks + 5 VL benchmarks |
| Accuracy delta | **W4A16 <1% drop** (near-lossless). **W2A16 LLaMA2-70B**: ARC-c/HellaSwag/MMLU/WinoGrande **53.30/81.60/63.70/77.80** vs FP16 60.50/84.30/68.90/80.60 — **15–24 points above OliVe** (38.60/55.30/39.80/60.70). AWQ and **OliVe ≥1e4 PPL** at W2A16 |
| Speedup | v1 (W4A4) **1.50×**, v2 (WxA4) **2.47×** avg over baselines at iso-accuracy; **2–3× over OliVe**. GPU: 1.2× / 1.7× over A100 W4A4 |
| Energy / area | **1.5× lower energy** (v2). EBW **2.36 bits** vs GOBO/OLAccel 15.6–18.17, OliVe 2. ReCoN 3% area at 128×128; OliVe's area is *higher* than the 1-ReCoN variant |
| Technology node | **TSMC 7 nm**, 1 GHz, DC + Innovus PnR; all baselines scaled to 7 nm via DeepScale |
| Evidence level | **PnR** (DC + Innovus) area/power + **cycle-accurate simulator** (DnnWeaver + BitFusion) + **GPGPU-Sim/AccelSim** for the GPU story. Three kinds; don't pool. No silicon |
| **Is the comparison fair?** | Best baseline discipline in the corpus. Iso-node (7 nm, DeepScale), iso-clock, same memory hierarchy; **iso-accuracy constructed** — all models within ±2% of best, two variants reported. **Elision**: Table 1 marks "aligned memory" equal for OliVe and MicroScopiQ, but OliVe carries zero metadata vs 24 b/μB here. Baselines analytically scaled, not measured. Calibration budgets differ (OmniQuant 5–6×) |

## 5. Comment


## 6. Claude notes

*Suggestions from the reading agent. **Strip this section before copying into
`QuantArchSurvey/venues/ISCA/notes/`.***

**Human verified: no.**

- **This is the corpus's sharpest cross-entry refutation, and it confirms a flag we raised.**
  On OliVe's close read I noted its "two-outlier pairs almost never show up" was asserted from
  BERT/GPT2-XL/OPT-6.7B with no sensitivity study, and that clustered outliers would mean
  *silent destruction of real outliers*. MicroScopiQ measures exactly that: **<0.04% adjacent
  outliers in OliVe's models vs >0.5% average and >2% peak in LLaMA3/LlaVa**. Combined with
  OliVe evaluating nothing above 7B, the survey can now say precisely why the G3 outlier
  anchor's mechanism doesn't carry forward.
- **The outlier-currency axis now has four entries and a second dimension** — not just *what an
  outlier costs* but *how the sacrifice is chosen*:

  | Paper | Currency | Chosen by |
  |---|---|---|
  | OliVe | destroyed weight | **adjacency** — the neighbour, whatever it is |
  | MicroScopiQ | destroyed weight + permutation metadata | **importance** — Hessian, anywhere in the μB |
  | Oaken | extra bits + COO metadata | magnitude thresholds, offline |
  | OASIS | high precision (FP16 second path) | top-k, online |

  The trend reads cleanly: local-and-free → global-and-informed.
- **Closes the gap OASIS's brief flagged** — that OASIS never compares against the microscaling
  line. These two are direct competitors (both 2025–26, both outlier-aware, both non-INT outlier
  formats) and **neither cites the other**. Worth a paired paragraph.
- **§5 material, if you want it.** Placement: head of the outlier/combined-dtype thread and a
  core `MX` entry. Best citation for: **memory alignment is the property that decides whether
  outlier handling is practical** (Table 1 is the cleanest statement of that trade anywhere),
  and for the adjacent-outlier measurement. `G3` by problem and by model set.
- **GOBO is load-bearing again** (Group-A reference here, baseline in OliVe, named in the
  taxonomy) and is **not in the corpus** — MICRO'20. Along with ANT, the strongest case yet for
  extending past ISCA.
