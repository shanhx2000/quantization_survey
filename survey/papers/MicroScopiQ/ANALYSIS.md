# MicroScopiQ — paper notes

**MicroScopiQ: Accelerating Foundational Models through Outlier-Aware Microscaling Quantization**
Akshat Ramachandran, Souvik Kundu, Tushar Krishna
**ISCA 2025** ｜ DOI: **not recorded** — the ACM/IEEE record is not reachable by script (403); look it up when citing
Venue evidence (2026-09-02): arXiv `comments` field, verbatim: *"ISCA 2025"*
Archived here: **arXiv:2411.05282v4** (2025-04-29), 17 pages — **the preprint, not the
published ISCA 2025 version**; the two were **not compared**.

Status: **note ready** ｜ Last updated: 2026-09-09
Tags: `analytical-dtype` `dtype-granularity` `combined-dtype` `mixed-precision` `accelerator`
How far it was read: **close read of §1–§8** — abstract, introduction, §2 background, §3
motivation (incl. the adjacent-outlier measurement and Table 1), §4 quantization methodology
and Algorithm 1, §5 accelerator and ReCoN, §6 EBW calculation, §7 all of experimental
evaluation (Tables 2–7, area/power/timing) and §8. **Skimmed:** related work, appendices.
Figures read for prose claims; per-bar values of Figs. 12–17 not transcribed.


> Original: https://arxiv.org/abs/2411.05282
> The PDF is **not committed** (9.3 MB). Re-download: `curl -sSL -o 2411.05282.pdf https://arxiv.org/pdf/2411.05282`
> Extract text: `python3 extract.py` → `extracted/` (committed, greppable)
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, ISCA 2025 row.

---

## Brief

### 1. Motivation

Outlier-aware co-designs are stuck in a mutual exclusivity: keep outliers at high precision
and you get accuracy but **unaligned memory and complex PEs**; quantize outliers like
everything else and you get hardware efficiency but lose accuracy. The paper's table makes
the trade explicit — prior Group A reaches 18.17 effective bits, Group B drops to 2 bits
with low accuracy.

### 2. Overview

Use **pruning to pay for outliers**: keep outliers at higher precision, and prune a fraction
of the least important weights so the freed bits absorb the extra outlier bits — which keeps
memory **aligned** at a low effective bitwidth (2.36 bits). Hardware is a systolic array of
multi-precision INT PEs plus a network-on-chip, **ReCoN**, that hides the complexity of
routing high-precision outliers. Explicitly assumes **no locality** of outlier weights.

### 3. Pros and cons

**Pros**

- The alignment argument is the strongest part: it gets Group-A accuracy at Group-B-like
effective bitwidth and simple PEs, which is precisely the exclusivity it set out to break.
- Dropping the outlier-locality assumption is a direct and well-aimed critique of
[`OliVe`](../OliVe/ANALYSIS.md); it makes the method applicable across foundation models
rather than models with convenient outlier structure.
- Broad and strong evaluation: up to 3× faster inference and 2× lower energy, ≥8% accuracy
over OliVe at lower precision, and <1% drop at W4A16 with usable W2A16 results. Code is
released.

**Cons**

- Trades pruning error for outlier fidelity — the accuracy budget is spent, not created, and
how that trade behaves at extreme sparsity is not fully mapped.
- The ReCoN NoC is an added structure whose cost is amortized over the array; on a smaller
design that overhead could dominate.
- Comparisons are against methods with different calibration budgets (it notes OmniQuant
needs 5–6× its runtime), so accuracy-per-effort comparisons need care.

### 4. Where it applies

The current head of the **outlier / combined-data-type** thread and the strongest single
argument that **memory alignment** is the property that decides whether outlier handling is
practical. Also a core **microscaling (§1.2 + granularity)** entry.

---

## Conclusions

<!-- Nothing here yet: the paper has not been read. Replace this with numbered,
     evidence-marked claims on the close read, then move the status to `analysis ready`. -->

**Read in full 2026-09-09.** The brief holds. The important addition is that this paper
**measures and refutes the assumption [`OliVe`](../OliVe/ANALYSIS.md) is built on**, and gives
the number.

**The adjacent-outlier measurement (§3.2, verified).** OliVe's OVP encoding requires that
outliers are almost never adjacent — it prunes the neighbour, so two adjacent outliers means
one real outlier is destroyed. MicroScopiQ measures the rate:

| Models | Adjacent outliers per layer |
|---|---|
| BERT, OPT — **the models OliVe evaluated** | **< 0.04 %** |
| LLaMA3, LlaVa and other modern FMs | **> 0.5 % average, peaks > 2 %** |

**Two orders of magnitude.** This confirms, with data, the flag raised on OliVe's close read:
its locality assumption was measured on a pre-LLaMA corpus and does not survive the move to
modern foundation models. It is the cleanest cross-entry refutation in this corpus so far,
and it is the reason OliVe collapses at W2A16 (≥ 1e4 PPL, §7.2) while MicroScopiQ does not.

**Consequence for the outlier-currency axis.** MicroScopiQ pays for outliers in *the same
currency as OliVe* — **destroyed weights** — but chooses the victims by **Hessian importance
anywhere in the micro-block** rather than by adjacency. The axis therefore has a second
dimension: not just *what an outlier costs*, but *how the thing being sacrificed is chosen*.

---

## Method

**Verified** unless marked.

**The mutual exclusivity it names** (Table 1). Group A (GOBO, OLAccel) keeps outliers at high
precision → high accuracy, but **unaligned memory, complex PEs, EBW 18.17 bits**. Group B
(OliVe) quantizes outliers at the same precision → aligned memory, EBW 2 bits, but **low
accuracy**. MicroScopiQ claims all three: high accuracy, **EBW 2.36 bits**, aligned memory,
*simple* PEs.

**The move: pay for outlier bits with pruned weights, chosen by importance.** Three steps
(Algorithm 1):

1. **Separate and quantize** (§4, step 1). Weights split into **macro-blocks (MaB)** and
   **micro-blocks (μB)**. Outliers identified by the **3σ rule**. Inliers → low-precision
   **MX-INT**; outliers → **MX-FP at 2× the inlier bitwidth**. Two deliberate format choices,
   both justified by ablation (Table 7): outliers need more bits than inliers, and **FP beats
   INT for outliers** because dynamic range matters more than resolution at the extremes.
2. **Reorganise the outlier into distributable halves** (§4, step 2). For MX-FP-4 with a
   shared 1-bit μX, an outlier is 1 sign + 2 mantissa. Duplicate the sign onto each mantissa
   bit → `{s·m₁, s·m₀}`, two 2-bit halves that **mimic the inlier MX-INT layout**. That is what
   lets the LSB half be stored in a slot the PE already knows how to read.
3. **Distribute the LSBs into pruned slots** (§4, step 3). For `n` outliers in a μB, find the
   `n` least important inliers by the **OBS/GPTQ Hessian criterion** `argmin wₚ²/[H⁻¹]ₚₚ`,
   prune them, and write the outliers' Lower halves there. The result is a
   **(B_μ−n):B_μ structured sparsity pattern**. A per-μB **permutation list** records where
   each half went; μBs with no outliers store none. Constraint: `n ≤ B_μ/2`.

**Why this keeps memory aligned.** Every element occupies exactly `bb` bits with one data type
per layer, so the PE array is homogeneous and the access pattern is regular — the property
Table 1 identifies as the real discriminator, and the reason Group A's accuracy was previously
unreachable at Group B's cost.

**ReCoN** (§5). A network-on-chip that reassembles outliers whose halves were scattered across
the μB, routing partial sums and performing swaps so the PE array itself never has to know an
outlier is split. Cost is amortised over the array: at **128×128 a single ReCoN is 3 % area
overhead**; even **8 ReCoN units cost 11 %**.

**EBW derivation** (§6, **verified arithmetic**): a μB with no outliers costs `bb` = **2 bits**;
a μB with outliers costs `(perm_bits + 2·B_μ + Os_bits)/B_μ` = `(24 + 16 + 8)/8` = **6 bits**.
Model average lands at **≈2.36 bits**. So the metadata is real but confined to blocks that
actually contain outliers.

## Key numbers, with their frame

**Frames.** PyTorch, quantized on a single **H100**, runtime **30 min – 9 h** for 3.8B–175B.
Calibration: **256 PILE samples** (64 ImageNet samples for CNN/SSM). Accelerator in Verilog
RTL, **Synopsys DC + Innovus PnR, TSMC 7 nm, 1 GHz**, CACTI for memories, cycle-accurate
simulator built on **DnnWeaver + BitFusion**. All baselines scaled to 7 nm with **DeepScale**,
same clock, same memory hierarchy and bandwidth. GPU results from **GPGPU-Sim/AccelSim** for
Ampere. **No silicon.**

⚠️ **7 nm** — same node as [`Omni-LUT`](../Omni-LUT/ANALYSIS.md), unlike the 22–28 nm entries.

| Setting | Model | Metric | Baseline | Result | Source |
|---|---|---|---|---|---|
| **The refutation of OliVe's premise** | BERT/OPT vs LLaMA3/LlaVa | adjacent outliers per layer | — | **< 0.04 %** vs **> 0.5 % avg, > 2 % peak** | §3.2, Fig. 2(a) |
| **W2A16 accuracy** | LLaMA2-70B | ARC-c / HellaSwag / MMLU / WinoGrande | FP16 **60.50 / 84.30 / 68.90 / 80.60** | **53.30 / 81.60 / 63.70 / 77.80** | Table 3 |
| same | LLaMA2-70B | same | **OliVe** 38.60 / 55.30 / 39.80 / 60.70 · OmniQuant 49.70 / 77.80 / 58.20 / 74.20 | MicroScopiQ ahead of OliVe by **15–24 points** | Table 3 |
| W2A16 perplexity | LLMs | WikiText2 PPL | AWQ and **OliVe ≥ 1e4 PPL** (omitted from table) | up to **2.04 PPL better** than the best surviving baseline | §7.2 |
| W4A16 | LLMs | accuracy drop | FP16 | **< 1 % on average** — near-lossless | §7.2 |
| Effective bitwidth | — | bits incl. metadata | GOBO/OLAccel **15.6–18.17**; OliVe 2 (`bb`) | **2.36** | Table 1, §6 |
| Speedup, iso-accuracy | across FMs | × over baselines | OliVe, ANT, GOBO, OLAccel, AdaptivFloat | **v1 (W4A4) 1.50×, v2 (WxA4) 2.47×** avg; **2–3× over OliVe** | §7.5, Table 5 |
| Energy, iso-accuracy | across FMs | × lower | same baselines | **1.5×** (v2) | §7.5 |
| ReCoN area overhead | 128×128 array | % | — | **3 % (1 ReCoN), 11 % (8 ReCoN)**; OliVe's area is *higher* than the 1-ReCoN variant | §7.7, Fig. 17 |
| Power breakdown | LLaMA2-7B | % | — | PE array 56.23 %, on-chip memory 36.80 %, **ReCoN 5.94 %** (VILA-7B, more outliers: ReCoN 7.65 %) | §7.5 |
| GPU integration | — | × over A100 W4A4 | A100 | v1 **1.2×**, v2 **1.7×** | §7.6, Fig. 13 |
| Format ablation | — | — | — | outliers at 2-bit ≪ outliers at 4-bit; **MX-FP outliers > MX-INT outliers** | Table 7 |

Left blank: per-bar values of Figs. 12–17; the VLM benchmark tables (read, not transcribed).

## Cost and requirements

- **`bb` — the paper's central quantity, defined once and then used everywhere.** Verbatim
  (§4 step 3): *"each of size `bb` (per element bit-budget), with `bb` representing the
  **operational bit-width of each PE**"* (**verified**). It is the fixed width of **every
  storage slot**, whatever occupies it:

  | Slot contents | Width |
  |---|---|
  | an inlier | `bb` (MX-INT) |
  | an outlier | `2·bb`, stored as **two `bb`-sized halves** (Upper, Lower) |
  | a pruned inlier's slot | `bb`, holding some outlier's Lower half |

  **That uniformity is the alignment mechanism.** One `bb` and one datatype per layer ⇒ regular
  memory access and a homogeneous PE array — the two properties Table 1 says Group A sacrifices.
  It is also why step 2's sign-duplication exists: an MX-FP-4 outlier is 1 sign + 2 mantissa, so
  duplicating the sign gives `{s·m₁, s·m₀}`, two 2-bit halves **shaped like an inlier**, fitting
  slots the PE already reads. The paper labels configurations by `bb` (footnote 5), so
  "W2A16" and "`bb` = 2" name the same setting.

  **`bb` is not EBW.** `bb` is raw storage; EBW adds the permutation-list metadata:
  **`bb` = 2 → EBW 2.36; `bb` = 4 → EBW 4.15** (§7.3, **verified**). Note the quiet claim
  alongside it — *"all other baselines employ software-managed metadata and have EBW = `bb`"* —
  i.e. their metadata is held outside the tensor, so their reported EBW understates the true
  cost while MicroScopiQ counts its 0.36. `**inferred / not verified**`: whether that is a fair
  characterisation of each baseline is not examined.
- **Data type.** **Inliers MX-INT at `bb` bits (2 or 4); outliers MX-FP at 2·`bb`.** Both
  microscaling — shared block scale plus per-element field. `W4A16`, `W2A16`, `W4A4`, and a
  mixed `WxA4`. **Tag `MX`, not `BFP`**, per the taxonomy rule.
- **Granularity — two levels, both stated.** **Macro-block** shares the inlier scale factor;
  **micro-block B_μ = 8** is the unit of outlier accounting, pruning and permutation. MXScale
  8 bits, inlier scale factor 7+1 bits shared across the MaB. This is one of the few entries
  in the corpus that reports its group size unambiguously.
- **Outlier mechanism — higher precision *and* a different format, paid for by pruning.**
  Outliers keep 2× bits in MX-FP; the extra bits live in slots freed by pruning the `n` least
  important inliers per μB, located by Hessian. **≤ B_μ/2 outliers per μB.**
- **Escape hatch.** Pruned weights (a `(B_μ−n):B_μ` structured sparsity pattern) **plus** a
  24-bit permutation list per outlier-bearing μB. Unlike OliVe there *is* metadata — but it is
  confined to blocks that contain outliers, which is why EBW is 2.36 rather than 6.
- **Accumulator.** Not reported. PEs are multi-precision INT; the critical path is local weight
  registers → multipliers, and the PE-to-ReCoN column bus is explicitly **off** the critical
  path.
- **Retraining: PTQ**, calibration on **256 PILE samples**, 30 min–9 h on one H100 — and the
  paper notes OmniQuant needs 5–6× that.
- **What the hardware pays.** ReCoN: **3 % of a 128×128 array**, 5.9–7.7 % of power. Simple
  homogeneous INT PEs otherwise — the explicit contrast with OliVe's exponent-integer decode
  path.

## Limitations and open questions

**Authors admit:** ReCoN overhead is only small at large array sizes (it is amortised, so a
small design pays more); EBW is data-dependent, varying with outlier percentage and μB size;
outliers at the *same* precision as inliers degrades sharply (Table 7), so the 2× rule is load-
bearing.

**Not admitted:**

1. **The accuracy budget is spent, not created** — the brief's first con, and the close read
   confirms nothing addresses it. Pruning error is traded for outlier fidelity; there is no
   study of where that trade inverts, and the `n ≤ B_μ/2` cap means a μB with many outliers
   silently cannot represent them all.
2. **The Hessian criterion needs calibration data and an `H⁻¹`** — this is GPTQ-class
   machinery, not a runtime rule. It is offline and one-time, but it makes MicroScopiQ
   dependent on calibration in a way OliVe's purely local rule is not. Calibration sensitivity
   is not studied.
3. **A permutation list is metadata, and the comparison with OliVe on "aligned memory" elides
   this.** Table 1 marks both as "Aligned", but OliVe carries **zero** metadata while
   MicroScopiQ carries 24 bits per outlier-bearing μB. Aligned is not the same as free.
4. **Baselines have different calibration budgets** (OmniQuant 5–6× the runtime) — the brief
   flagged this and it stands.
5. **7 nm against baselines scaled by DeepScale**, including OliVe (22 nm original) and GOBO/
   OLAccel (older still). Scaling tools are standard practice, but the comparison is
   analytical, not measured, for every baseline.

## Relation to other entries

- **It refutes [`OliVe`](../OliVe/ANALYSIS.md) with data, and this is the corpus's sharpest
  cross-entry result.** See Conclusions: < 0.04 % adjacent outliers in BERT/OPT vs > 0.5 % in
  LLaMA3/LlaVa. Combined with OliVe's own evaluation stopping at 7B with no LLaMA, the survey
  can now say precisely *why* the G3 outlier anchor's mechanism does not carry forward.
- **The outlier-currency axis, now with four entries and a second dimension:**

  | Paper | Currency | How the sacrifice is chosen |
  |---|---|---|
  | [`OliVe`](../OliVe/ANALYSIS.md) | destroyed weight | **adjacency** — the neighbour, whatever it is |
  | **MicroScopiQ** | destroyed weight **+ permutation metadata** | **importance** — Hessian, anywhere in the μB |
  | [`Oaken`](../Oaken/ANALYSIS.md) | extra bits + COO metadata | magnitude thresholds, offline-profiled |
  | [`OASIS`](../OASIS/ANALYSIS.md) | high precision (FP16 second path) | top-k, online |

  **The trend is legible**: from local-and-free (OliVe) to global-and-informed (MicroScopiQ).
- **Answers the gap flagged in [`OASIS`](../OASIS/ANALYSIS.md)'s brief** — that OASIS has no
  comparison against the microscaling line. The two are close competitors: both 2025–26, both
  outlier-aware, both non-INT outlier formats. Neither cites the other. **Worth a paired
  paragraph.**
- **`GOBO` and `OLAccel` are the Group-A reference points** — OLAccel is in the corpus,
  GOBO is not (MICRO'20) and is load-bearing here, in OliVe, and in the taxonomy's G3 examples.
- **`ANT` again** as an accelerator baseline — sixth entry depending on it.

## For the note

### §1 one-line summary

> Keeps outliers at **2× the inlier bitwidth in MX-FP** while inliers stay **MX-INT**, and pays
> for the extra outlier bits by **pruning the least important weights in the same micro-block —
> chosen by Hessian, not by adjacency** — so every element still occupies a fixed bit budget
> with aligned memory and homogeneous INT PEs, reaching **2.36 effective bits** with a
> network-on-chip (ReCoN) reassembling the scattered outlier halves for 3 % area.

### Proposed values on their four axes

| Axis | Proposed | Evidence (one line) |
|---|---|---|
| **Level** | **`ALGO+ARCH`** | Hessian-guided pruning + MX-INT/MX-FP assignment is the algorithm; the multi-precision INT PE array and ReCoN NoC are the architecture, and neither works alone. |
| **Q-oriented** | `Q-ORIENTED` | ReCoN exists solely to reassemble split outliers; remove quantization and the entire NoC and PE design lose their purpose. |
| **Data type** | **`MX` + `FP4` + `INT2` + `INT4` + `MIXED`** | MX-INT inliers and MX-FP outliers at 2× precision (§3.3); the paper says microscaling, so `MX` not `BFP` per taxonomy rule. |
| **Generation** | **`G3`** | Outlier thread, on LLaMA3 / Phi-3 / Mixtral / VLMs, and explicitly about *foundation-model* outlier structure rather than pre-LLM outliers. |
| **Optimization** (free text) | `outlier-aware` `microscaling` `MX` `pruning` `Hessian` `N:M-structured-sparsity` `aligned-memory` `NoC` `ReCoN` `systolic` `mixed-precision-PE` | — |

### Proposed venue-list row

```
| [x] | [MicroScopiQ: Accelerating Foundational Models through Outlier-Aware Microscaling Quantization](https://arxiv.org/abs/2411.05282) | ALGO+ARCH | Q | `MX` `FP4` `INT2` `INT4` `MIXED` | G3 | `outlier-aware` `microscaling` `pruning` `Hessian` `aligned-memory` `ReCoN` | Outliers kept at 2× bitwidth in MX-FP, paid for by pruning the least-important weights in the same micro-block by Hessian — aligned memory at 2.36 effective bits. Measures >0.5% adjacent outliers in modern FMs vs <0.04% in OliVe's models |
```

### §4 fairness verdict

**Carefully constructed, and the strongest baseline discipline in the corpus so far — with one
elision.**

- **Iso-node ✓, iso-clock ✓, iso-memory ✓** — all designs at **7 nm via DeepScale**, 1 GHz,
  "same memory hierarchy and bandwidth". Stated explicitly.
- **Iso-accuracy ✓ and constructed** — §7.5 builds the comparison so "all model accuracies are
  within ±2 % of the best quantized model", and reports two MicroScopiQ variants (v1 at
  `bb=4`, v2 mostly `bb=2`) rather than one flattering point. That is better practice than most
  of this corpus.
- **The elision: "aligned memory" is marked equal for OliVe and MicroScopiQ in Table 1**, but
  OliVe carries **zero** metadata and MicroScopiQ carries a 24-bit permutation list per
  outlier-bearing μB. Both are aligned; they are not equally cheap. The 2.36 vs 2 EBW gap is
  exactly this, and the table does show it — but the "Aligned memory" row invites the reader to
  treat them as equivalent.
- **Baselines are analytically scaled**, not measured — OliVe from 22 nm, GOBO/OLAccel older.
  Standard practice, worth naming.
- **Calibration budgets differ** — OmniQuant needs 5–6× MicroScopiQ's runtime, noted by the
  paper, so accuracy-per-effort comparisons need care.
- **Evidence levels**: PnR-level area/power (DC + Innovus), cycle-accurate simulator for
  performance, GPGPU-Sim for the GPU story. Three kinds; do not pool.

## Abstract (verbatim, arXiv:2411.05282v4)

> Quantization of foundational models (FMs) is significantly more challenging than
> traditional DNNs due to the emergence of large magnitude values called outliers. Existing
> outlier-aware algorithm-architecture co-design techniques either use mixed-precision,
> retaining outliers at high precision but compromise hardware efficiency, or quantize
> inliers and outliers at the same precision, improving hardware efficiency at the cost of
> accuracy. To address this mutual exclusivity, we propose MicroScopiQ, a novel co-design
> technique that leverages pruning to complement outlier-aware quantization. MicroScopiQ
> retains outliers at higher precision while pruning a certain fraction of least important
> weights to distribute the additional outlier bits; ensuring high accuracy, aligned memory
> and hardware efficiency. We design a high-throughput, low overhead accelerator
> architecture composed of multi-precision INT processing elements and a network-on-chip
> called ReCoN that efficiently abstracts the complexity of supporting high-precision
> outliers. Additionally, unlike prior techniques, MicroScopiQ does not assume any locality
> of outlier weights, enabling applicability to a broad range of FMs. Extensive experiments
> across diverse quantization settings demonstrate that MicroScopiQ achieves state-of-the-
> art quantization accuracy, while delivering up to 3x faster inference and 2x lower energy
> consumption compared to existing alternatives. Code is available at:
> https://github.com/georgia-tech-synergy-lab/MicroScopiQ-LLM-Quantization
