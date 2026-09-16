# UniCore — paper notes

**UniCore: A Bit-Width Scalable GEMM Unit for Unified LLM Inference**
Yonghao Chen, Jiaxiang Zou, Xingyu Chen, Chenxi Xu, Jingyu Guo, Xinyu Chen
**ISCA 2026** (2026 ACM/IEEE 53rd Annual International Symposium on Computer Architecture),
pp. 2520–2535 ｜ DOI: **10.1109/ISCA66397.2026.00176**
Publication info verified 2026-09-02 from the **official ISCA 2026 proceedings package**
(title, authors, pages, DOI and abstract all read from its `assets/data/data.js`).
Archived here: **the published proceedings PDF** (`506501c520.pdf`, 16 pages) — not a preprint.

Status: **note ready** ｜ Last updated: 2026-09-14
Tags: `multi-bitwidth-hw` `new-data-type` `analytical-dtype` `mixed-precision` `accelerator`
How far it was read: **close read of the abstract, §I-§III (motivation and the FPMA formulation),
the contribution list, §VIII (evaluation setup and results) and the conclusion**; the compensation
pipeline and DynFP were read for mechanism and cost rather than circuit detail. The PDF extraction
mangles the "FPMA" ligature and drops section headers, so text was located by pattern search —
numbers below come from prose I could read directly. Read as the partner to
[`XtraMAC`](../XtraMAC/ANALYSIS.md).

> The PDF is **not committed** (6.1 MB). It came from the proceedings package a human
> supplied, now archived at [`archieve/ISCA 2026.zip`](../../../archieve/), entry `pdfs/5065-3nexm57sBmVa6MJtFTiSrb/506501c520/506501c520.pdf`.
> **There is no public URL for it** — this is not an arXiv paper. Re-extract with
> `python3 extract.py` → `extracted/` (committed, greppable).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, 2026 row.

---

## Brief

### 1. Motivation

Different LLMs need different precisions — Llama-1/2 and OPT survive W4A4 while Llama-3
needs W8A8 — and a single model may want a low-precision 'draft' mode and a high-precision
'quality' mode. Fixed-format accelerators cannot span this. **Bit-composable** designs can,
but suffer a **quadratic collapse**: multiplier resources scale as O(n²) in area and delay,
so throughput falls as ~1/n² and high precision becomes unaffordable.

### 2. Overview

Change the primitive. **S-FPMA** is a composable floating-point multiply–add built from
**uniform adder slices**, so fusing to higher precision scales **linearly** rather than
quadratically. Numerical fidelity is restored by a lightweight format-conversion and **dual-
path compensation** pipeline correcting FPMA's structured approximation error. Complemented
by **DynFP**, a distribution-adaptive low-bit FP format.

### 3. Pros and cons

**Pros**

- Diagnoses the exact failure mode of the whole bit-composable lineage
([`BitFusion`](../BitFusion/ANALYSIS.md) onwards) and fixes it at the primitive level —
the strongest 'why previous designs plateaued' argument in the corpus.
- Delivers where composable designs are weakest: 1.24×–3.95× area efficiency at
W4A4/W4A8/W8A8 and **up to 5.26× at W16A16**, plus 24% smaller GEMM area than Tender even
with 16-bit support.
- Highest accuracy in nearly all configurations, and open-sourced.

**Cons**

- FPMA is an **approximate** primitive; correctness depends on the compensation pipeline, so
the design's fidelity is engineered rather than exact — a property to verify carefully
before citing it as lossless.
- Two contributions in one paper (S-FPMA and DynFP); how much of the accuracy result comes
from the format versus the compensation is not separable from the headline numbers.
- Compared mainly against composable-multiplier accelerators; against fixed-format designs
at their own single precision the flexibility premium is not shown.

### 4. Where it applies

The 2026 state of the art for **multi-bitwidth hardware (tag 9)** and the direct answer to
BitFusion. Read those two together — they bracket eight years of the same idea.

---

## Conclusions

**It names the failure mode of the entire bit-composable lineage, and the diagnosis is correct
against `BitFusion`'s own numbers.** §II-C, verbatim: "BitFusion [39] is a pioneering example…
However, despite their flexibility, these architectures are **fundamentally limited by the quadratic
O(n²) cost of multipliers**. Because partial-product generation and accumulation grow with n², the
achievable throughput of fused PEs decreases proportionally to **1/n²** as precision increases. This
**'dynamic tax'** allows good efficiency at 4-bit, but causes **severe throughput collapse** when
switched to 8-bit or 16-bit modes." Figure 3(a) makes it concrete — **16 MACs/cycle at 4-bit,
4 at 8-bit, 1 at 16-bit** — which is *exactly* BitFusion's own fusion table (16 / 4 / 1 Fused-PEs).
The critique uses the criticised paper's numbers, which is the strongest form it could take.

**The fix is to stop multiplying.** FPMA — floating-point multiplication approximation — rests on
**Mitchell's logarithmic approximation** (1962): `log₂(1 + M_x) ≈ M_x`. So a float's
**concatenated exponent–mantissa field is already, approximately, its logarithm**:
`log₂|x| ≈ E_x + M_x − B`. Multiplication therefore becomes **integer addition of those fields**:

```
R = X + Y      with  X = E_x + M_x,  Y = E_y + M_y,  R = E_r + M_r
```

Adders scale **linearly** in width where multipliers scale quadratically, so composing to higher
precision costs `O(n)` rather than `O(n²)`. Figure 3(b): **O(1/n) scaling**. That is the entire
architectural argument, and it is a clean one — the primitive is changed, not the fusion logic.

**The bill comes as structured error, and the paper pays it explicitly.** Mitchell's approximation
is systematically biased, so UniCore adds "**subnormal removal, mantissa reconstruction, and
dual-path fine- and coarse-grained compensation**". That pipeline is the real cost of the linear
scaling, and whether it stays lightweight as precision rises is the question the survey should ask
of it.

**Where it wins is exactly where composable designs were weakest, which is the right proof.**
**1.24×-3.95×** area efficiency at W4A4/W4A8/W8A8, rising to **up to 5.26× at W16A16**. The gain
*grows with precision* — the signature of having removed a quadratic term rather than tuned a
constant. A design that beat the baselines uniformly would be less convincing.

**It completes the multi-precision thread by changing the axis.** `BitFusion`, `RaPiD`,
`SamsungNPU`, `EVA` and `XtraMAC` all argue about **how to compose** a multiplier — spatially,
temporally, in split pipelines, in DSP bit-space. UniCore argues you should **not compose a
multiplier at all**. It is the only entry in the thread that attacks the primitive rather than the
composition strategy.

---

## Method

**FPMA** (§III-A) **verified**. From the IEEE normalised form and Mitchell's approximation
`log₂(1 + M_x) ≈ M_x`, approximate `log₂|x| ≈ E_x + M_x − B`; then `r = x·y` in the log domain is
`R = X + Y` over the concatenated exponent–mantissa fields. The paper's own summary: FPMA
"**eliminat[es] multipliers**: it replaces floating-point multiplication with **integer addition over
the concatenated exponent–mantissa field**. This makes precision scaling **slice-composable**."

**S-FPMA** — the contribution: the first composable FPMA primitive, fusing to different precisions
using **uniform adder slices**, so hardware scaling stays **linear**.

**Compensation pipeline** — three named stages: **subnormal removal**, **mantissa reconstruction**,
and **dual-path fine- and coarse-grained compensation**, correcting FPMA's structured approximation
error.

**DynFP** — a configurable low-bit floating-point format that **adapts exponent–mantissa
allocation** and **eliminates redundant encodings**, targeted at "the diverse weight and **K/V**
distributions in LLMs". This is the paper's one data-type contribution.

**Motivation for bit-width flexibility** (§I) **verified**: Llama-1/2 and OPT hold accuracy at
**W4A4**; Llama-3 needs **W8A8**; and one model may want a low-precision **"draft" mode** and a
high-precision **"quality" mode** — so no single format is universally applicable.

---

## Key numbers, with their frame

Evidence level: **SpinalHDL RTL synthesised with Synopsys Design Compiler, TSMC 28 nm, 1 GHz**,
applied **consistently across all accelerator comparisons** — the baselines are re-synthesised in
the same flow, not quoted. System-level behaviour from an extended simulator. **No silicon.**

| Setting | Metric | Baseline | Result | Source |
|---|---|---|---|---|
| **The diagnosis** | throughput scaling of composable-multiplier PEs | — | **O(1/n²)** — **16 / 4 / 1 MACs per cycle at 4 / 8 / 16-bit** | §II-C, Fig. 3(a) **verified** |
| **The fix** | throughput scaling of S-FPMA PEs | — | **O(1/n)** | Fig. 3(b) **verified** |
| Area efficiency | W4A4 / W4A8 / W8A8 | **OliVe, Tender, M-ANT** (composable-multiplier) | **1.24×-3.95×** | abstract, §VIII **verified** |
| **Area efficiency** | **W16A16** | same | **up to 5.26×** — the gain **grows with precision** | abstract, §VIII **verified** |
| Compute density, C-PE | normalised, across precisions | Tender (=1.00 at W4A4) | UniCore **1.52×** at W4A4, rising to **8.16×**-class at W16A16 | Fig. 15, recovered fragment — **treat as approximate** |
| Fixed-precision comparison | compute density | **Synopsys DesignWare IP**; **Tender with composability removed** | UniCore **highest across all fixed-precision points** | §VIII **verified** |
| Accuracy | perplexity and task accuracy | five accelerators (OliVe, Tender, M-ANT, BitMoD, AxCore) | **highest accuracy in nearly all configurations; lowest perplexity in most** | abstract, §VIII **verified** |
| Area | GEMM area vs a 16-bit-capable baseline | Tender | **24% smaller GEMM area even with 16-bit support** | brief/§VIII **verified** |
| Implementation | node / clock / language | — | **TSMC 28 nm, 1 GHz, SpinalHDL** | §VIII-A **verified** |
| Open source | — | — | `github.com/CLab-HKUST-GZ/isca53-unicore` | abstract **verified** |

**Two of the five baselines are in this corpus** — `OliVe` and `Tender` — and both are re-synthesised
in UniCore's own 28 nm flow rather than quoted, which is the same node those papers used.

---

## Cost and requirements

| | |
|---|---|
| **Approximation error** | **Structural, not incidental.** Mitchell's approximation is systematically biased; correctness depends entirely on the compensation pipeline |
| **Compensation pipeline** | Subnormal removal + mantissa reconstruction + **dual-path** (fine and coarse) compensation. Called "lightweight"; its share of area is the number to check |
| **Format dependency** | FPMA needs an **exponent–mantissa** encoding to exploit. Pure integer formats have no logarithm to read off — which is why this is an **FP** design, unlike the INT-centric rest of the thread |
| **DynFP** | A new format, so it needs tooling support; "quantized online during inference and require a lightweight [conversion]" |
| **Accumulation** | Not analysed here — contrast `XtraMAC`, which shows accumulation is exactly where unification fails |
| **Retraining** | PTQ; DynFP is applied online |

---

## Limitations and open questions

**Admitted.** FPMA introduces structured approximation error, and the compensation pipeline exists
to correct it — stated rather than hidden.

**Unadmitted, and material.** (i) **The compensation pipeline's area is not isolated** in anything
I could read. Since it is the price of the linear scaling, "lightweight" needs a number — and if it
grows with precision, the O(n) claim needs qualification. (ii) **Accuracy comparisons mix two
different things**: UniCore's accuracy advantage comes partly from **DynFP** (a better format) and
partly from the compensated FPMA datapath, and the two are not separated in the headline claim.
(iii) **FPMA is not new** — Mitchell 1962, and refs [17], [26] — so the contribution is
*composability* of FPMA, which the abstract states precisely but the framing can blur.
(iv) **No analysis of error accumulation over long dot products**, which is where a systematically
biased multiplier would be expected to hurt most.

---

## Relation to other entries

**It closes the multi-precision-datapath thread by changing the question.**

| Paper | What it composes | Scaling | Substrate |
|---|---|---|---|
| `BitFusion` (ISCA'18) | 2-bit multipliers, **spatially** | **O(1/n²)** — 16/4/1 | ASIC 45 nm |
| `RaPiD` (ISCA'21) | nothing — **two separate pipelines** | n/a | ASIC 7 nm silicon |
| `SamsungNPU` (ISCA'21) | INT8 multipliers, **temporally** | 4 cycles for INT16 | ASIC 5 nm silicon |
| `EVA` (ISCA'26) | INT8 multipliers, **temporally** | 4 INT8 → FP16 | ASIC 28 nm |
| `XtraMAC` (ISCA'26) | DSP **bit-space**, spatially | fills a fixed multiplier | FPGA |
| **`UniCore` (ISCA'26)** | **adder slices — no multiplier at all** | **O(1/n)** | ASIC 28 nm |

Five papers argue about *how to compose a multiplier*; UniCore argues you should not have one. That
makes it the natural last word in the thread, and the pairing with `BitFusion` — first and last,
with UniCore quoting BitFusion's own 16/4/1 table as the problem — is the cleanest narrative arc
available to the survey.

**With `XtraMAC` it makes a matched pair on one question, from opposite substrates.** XtraMAC keeps
the multiplier and **fills** it (because on an FPGA the DSP is a fixed resource you cannot redesign);
UniCore **removes** it (because on an ASIC you can). Both published at ISCA 2026, both about
multi-format GEMM, opposite conclusions — and the substrate explains the difference exactly.

**It also links the thread back to the `POW2`/logarithmic family.** Mitchell's approximation is the
same observation that underlies logarithmic number systems, and `TAXONOMY.md` defines `POW2` as a
logarithmic number *format*. UniCore does not change the storage format — it exploits the fact that
**IEEE floating point is already approximately logarithmic in its stored bits**. That distinction is
worth making where the survey discusses log-domain arithmetic.

**Node.** TSMC 28 nm, alongside `Tender`, `Oaken`, `EVA` and `P3-LLM`'s RTL — and it re-synthesises
`OliVe` and `Tender` in that same flow, which is the right discipline.

---

## For the note

**§1 one-line summary.** Observes that a float's **concatenated exponent–mantissa field is already
approximately its logarithm** (Mitchell: `log₂(1+M) ≈ M`), so floating-point multiplication can be
done as **integer addition** — and builds the first **composable** version of that primitive from
**uniform adder slices**, so fusing to higher precision scales **linearly instead of quadratically**,
escaping the 16/4/1-MACs-per-cycle collapse that `BitFusion`-style composable multipliers suffer;
a subnormal-removal, mantissa-reconstruction and **dual-path compensation** pipeline repairs the
structured approximation error, and **DynFP** adapts exponent–mantissa allocation to LLM weight and
K/V distributions: **1.24×-3.95× area efficiency at W4A4/W4A8/W8A8 and up to 5.26× at W16A16**.

**Proposed tags — the seed row stands.**

| Axis | Value | Evidence |
|---|---|---|
| **Level** | `ARCH` | **Seed says `ARCH`** and the close read agrees on the hardware side — but note DynFP is a *format* contribution, so `ALGO+ARCH` is arguable. I would keep `ARCH`: DynFP is applied online with a lightweight conversion, not a training or calibration method. **Checked against the `SYS` rule** — no compiler or ISA, so no `SYS` |
| **Q-oriented** | `Q-ORIENTED` | The entire primitive exists to span multiple quantization formats. Fix one format and S-FPMA's slice composability, the compensation pipeline and DynFP all have nothing to do |
| **Data type** | `FP8` `FP4` `ADAPTIVE` `MIXED` | Correct. **`ADAPTIVE` is DynFP**, which genuinely adapts exponent–mantissa allocation and eliminates redundant encodings — the one place in this corpus where `ADAPTIVE` names a real format property rather than a selection policy |
| **Generation** | `G2` | Datapath-matched-to-bitwidth paradigm, no outlier format, no codebook — and the FPMA primitive is 1962. Paradigm, not year |
| **Optimization** | `composable FPMA` `Mitchell logarithmic approximation` `uniform adder slices` `linear scaling` `dual-path compensation` `DynFP` `bit-width scalable GEMM` | |

**§4 fairness verdict.** All five baselines — including in-corpus `OliVe` and `Tender` — are
**re-synthesised in UniCore's own SpinalHDL → Synopsys DC → TSMC 28 nm, 1 GHz flow**, not quoted:
strong iso-node discipline, at the same node those papers used. Against that: the **compensation
pipeline's area is never isolated**, and it is the price of the O(n) claim; and the accuracy
advantage **mixes DynFP (a better format) with the compensated datapath** without separating them.
Gains growing with precision (1.24× → 5.26×) is the right signature for a removed quadratic term.

**Proposed venue-list row:**

```
| [ ] | [UniCore: A Bit-Width Scalable GEMM Unit for Unified LLM Inference](https://doi.org/10.1109/ISCA66397.2026.00176) | *close read* | ARCH | Q | `FP8` `FP4` `ADAPTIVE` `MIXED` | G2 | `composable FPMA` `Mitchell logarithmic approximation` `uniform adder slices` `linear scaling` `dual-path compensation` `DynFP` | Composable FPMA from uniform adder slices — fuses **linearly, not quadratically**. Diagnoses BitFusion's lineage with BitFusion's own numbers (16/4/1 MACs per cycle at 4/8/16-bit) and answers by **removing the multiplier**: a float's exponent–mantissa field is already its logarithm |
```

## Abstract (verbatim, ISCA 2026 proceedings)

> Large Language Models (LLMs) have achieved remarkable success across a broad range of
> applications but impose extreme computational and memory demands due to their reliance on
> massive General Matrix–Matrix Multiplication (GEMM) operations. Quantization has emerged
> as a key approach to improve efficiency by reducing data precision; however, modern LLMs
> exhibit diverse sensitivities to quantization, requiring multiple precision settings.
> Existing hardware accelerators fail to efficiently support this diversity: fixed-function
> accelerators are limited to a few discrete formats, while bit-composable architectures
> suffer from quadratic resource scaling, leading to severe performance degradation at
> higher precision. We propose UniCore, a unified GEMM architecture that achieves both bit-
> width scalability and accuracy preservation through a hardware–software co-design. UniCore
> introduces Scalable FPMA (S-FPMA), the first composable FPMA primitive that fuses into
> different precisions using uniform adder slices, maintaining linear hardware scaling. To
> ensure numerical fidelity, UniCore integrates a lightweight format-conversion and dual-
> path compensation pipeline that corrects FPMA's structured approximation error.
> Complementing the architecture, DynFP, a distribution-adaptive low-bit floating-point
> format, improves representational accuracy for diverse LLM weight and activation
> distributions. UniCore delivers 1.24x-3.95x higher area efficiency for W4A4/W4A8/W8A8 and
> up to 5.26x at W16A16 compared to prior composable-multiplier accelerators, while
> achieving the highest accuracy in nearly all configurations. UniCore is open-sourced at:
> https://github.com/CLab-HKUST-GZ/isca53-unicore
