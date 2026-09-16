# Tender — paper notes

**Tender: Accelerating Large Language Models via Tensor Decomposition and Runtime Requantization**
Jungi Lee, Wonbeom Lee, Jaewoong Sim
**ISCA 2024** ｜ DOI: **not recorded** — the ACM/IEEE record is not reachable by script (403); look it up when citing
Venue evidence (2026-09-02): arXiv `comments` field, verbatim: *"To appear at the 51st International Symposium on Computer Architecture (ISCA 2024)"*
Archived here: **arXiv:2406.12930v1** (2024-06-16), 15 pages — **the preprint, not the
published ISCA 2024 version**; the two were **not compared**.

Status: **note ready** ｜ Last updated: 2026-09-09
Tags: `analytical-dtype` `dtype-granularity` `mixed-precision` `accelerator`
How far it was read: **close read of §I–§VII** — introduction, §II background and motivation,
§III algorithmic implementation (decomposition, the power-of-2 rule and its three
justifications, runtime requantization, walking example), §IV hardware architecture, §V
evaluation (methodology, Table II perplexity, area/power, speedup, energy) and §VI analysis.
**Skimmed:** §VII related work, references. Figures read for prose claims; per-bar values of
Figs. 10–11 not transcribed.


> Original: https://arxiv.org/abs/2406.12930
> The PDF is **not committed** (3.3 MB). Re-download: `curl -sSL -o 2406.12930.pdf https://arxiv.org/pdf/2406.12930`
> Extract text: `python3 extract.py` → `extracted/` (committed, greppable)
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, ISCA 2024 row.

---

## Brief

### 1. Motivation

Past ~6.7B parameters, a few activation feature dimensions carry extreme-magnitude outliers
that widen the quantization range and force higher bitwidths. Software-only fixes are too
slow or too lossy at 4 bits; existing co-designs need **mixed-precision compute units or
custom datatypes commodity hardware does not support**.

### 2. Overview

Split the activation tensor into subtensors along the **channel** dimension so each groups
elements of similar range, and quantize each with its own scale. The trick that makes it
cheap: choose the scale factors to be **powers of two apart**, so accumulating partial sums
across subtensors needs only a shift — **no explicit requantization** — which is a minimal
extension to commodity tensor hardware.

### 3. Pros and cons

**Pros**

- The least intrusive design in the outlier thread: it deliberately avoids custom datatypes
and mixed-precision units, so it can ride existing integer pipelines. That restraint is
the contribution.
- The power-of-two-apart constraint is the elegant step — it converts an expensive
dequantize/requantize into a shift, turning a scheme that would be impractical into one
that is nearly free.
- Reports higher accuracy *and* higher performance than the state of the art it compares
against, including [`OliVe`](../OliVe/ANALYSIS.md) and SmoothQuant on perplexity.

**Cons**

- Channel-grouping requires knowing which channels hold outliers, i.e. a
calibration/profiling step whose stability across inputs is assumed rather than stress-
tested here.
- Constraining scales to powers of two is a real loss of representational freedom; the paper
argues the trade is favourable but the gap to unconstrained per-group scales is not
isolated.
- Later work ([`Omni-LUT`](../Omni-LUT/ANALYSIS.md), [`P3-LLM`](../P3-LLM/ANALYSIS.md)) uses
Tender as a baseline it beats, so its position is not final.

### 4. Where it applies

A key **§2.2 fine-grained / channel-wise** entry, and the corpus's best example of
*designing the algorithm around what existing hardware can already do*. Contrast directly
with [`OliVe`](../OliVe/ANALYSIS.md), which instead changes the encoding.

---

## Conclusions

<!-- Nothing here yet: the paper has not been read. Replace this with numbered,
     evidence-marked claims on the close read, then move the status to `analysis ready`. -->

**Read in full 2026-09-09.** The brief holds. Two things it could not have known, both about
how *other* papers use this one.

**1. The "Tender is bad at INT4" claim is Tender's own number, not a hostile reproduction.**
Table II reports Tender INT4 on Llama-2-7B WikiText-2 at **36.47** against an FP16 base of
**5.47** (**verified**). [`TransitiveArray`](../TransitiveArray/ANALYSIS.md)'s Table 3 lists
"TD-4" at 23.85 (LLaMA-7B) and 36.47 (Llama-2-7B) — **identical to Tender's own table**. So
that paper quoted correctly, and Tender's own authors report the failure.

**2. Three papers report three different "Tender at 4-bit" numbers, and all three are
legitimate.** This is a citation hazard worth a survey footnote:

| Source | Llama-2-7B PPL | Configuration |
|---|---|---|
| **Tender**, Table II | **36.47** | INT4 weights **and** activations, incl. attention AA-GEMM |
| [`Oaken`](../Oaken/ANALYSIS.md), Table 2 | **6.42** | **KV-cache-only** 4-bit; W and A left FP16 |
| [`Omni-LUT`](../Omni-LUT/ANALYSIS.md), Fig. 15 | **123.1** | "global precision point", **W/K/V/A all INT4** |

Same method, same model, same metric, three numbers spanning 19×. **Never quote "Tender at
4-bit" without naming which tensors were quantized.**

---

## Method

**Verified** unless marked.

**The premise.** Activation outliers live in a few *channels*. Isolating them needs per-channel
scales, but that multiplies the number of matmul/dequant/add operations by the channel count
(**4096× for OPT-6.7B**, §III-D). Every prior fix either accepted that cost or introduced a
custom datatype. Tender's position: **change nothing about the number format; change only how
channels are grouped and how partial sums are rescaled.**

**1. Bias subtraction** (§III-B). Per channel, subtract `(max+min)/2` — a zero-point in effect —
so `|max| = |min|` and the symmetric range is fully used.

**2. Power-of-2 channel decomposition** (§III-B). Take each channel's absolute max (`CMax`) and
the tensor max (`TMax`). Assign channel *i* to group *g* where
`TMax/α^g < CMax_i ≤ TMax/α^(g−1)`, with **α = 2**. Group *g*'s scale is
`TMax / (α^(g−1)·(2^(b−1)−1))`. This is **classification against fixed thresholds, not
clustering** — chosen because clustering "is not likely applicable at runtime without complex
hardware".

> **Why the thresholds are geometric rather than uniform** — the paper's own argument, and the
> best part of it: quantization error of a group ∝ **absolute maximum × number of channels**.
> Outlier channels are few, so a *coarse* threshold there costs little; inlier channels are
> many, so they need *fine* thresholds. A geometric split gives exactly that gradient for free.

**3. Runtime (implicit) requantization** (§III-B). Because consecutive group scales differ by
exactly 2×, accumulating across groups needs **a 1-bit shift, not a floating-point rescale**.
Process the largest-scale group first, shift the accumulator 1 bit before the next group, and
dequantize once at the end with the smallest scale. Mathematically equivalent to
`Y = Σ (s_i·s_w)·P_i`, but with the reduction axis intact — so the systolic array stays full
rather than being split into `G` small matmuls.

**4. Hardware** (§IV). An INT4-only output-stationary systolic array (**64×64 PEs**, 64 FPUs in
the VPU, 32-bit accumulators) plus **a shifter next to the accumulator**. That shifter is the
whole architectural extension. No mixed-precision PEs, no datatype decoder — the contrast with
ANT and OliVe, both of which shift by an exponent sum and need decode logic.

**Calibration** (§III-B, §V-A): channel groups, biases and scale factors are all **precomputed
offline** from **128 samples of the Pile validation set**. Nothing is derived at runtime.

## Key numbers, with their frame

**Frames.** Perplexity on WikiText-2 and PTB at sequence length 2048, PyTorch/HuggingFace, OPT
and LLaMA/Llama-2 families; BERT-Large on GLUE additionally. Hardware from a **cycle-level
simulator** (Ramulator for DRAM timing) parameterised by **RTL synthesis at 28 nm** (Synopsys
DC), SRAM from a memory compiler, HBM2 with the FG-DRAM energy model. **Batch size 1,
input:output = 2048:1** — prefill-dominated. **No silicon.**

| Setting | Model | Metric | Baseline | Result | Source |
|---|---|---|---|---|---|
| **INT8 W+A — where it works** | OPT-6.7B / 13B / 66B | WikiText-2 PPL | FP16 10.86 / 10.13 / 9.34 | **10.93 / 10.17 / 9.43** (**+0.07 / +0.04 / +0.09**) | Table II |
| INT8 W+A | Llama-2-7B / 13B / 70B | WikiText-2 PPL | FP16 5.47 / 4.88 / 3.32 | 5.77 / 5.09 / 3.48 (+0.30 / +0.21 / +0.16) | Table II |
| INT8, vs baselines | Llama-2-7B | WikiText-2 PPL | SmoothQuant 48.54 · ANT 8.79 · OliVe 8.16 | **Tender 5.77** | Table II |
| **INT4 W+A — where it fails, by its own report** | Llama-2-7B / 13B | WikiText-2 PPL | FP16 5.47 / 4.88 | **36.47 / 55.08** | Table II |
| INT4, vs baselines (the "10988×" claim in context) | Llama-2-7B | WikiText-2 PPL | SmoothQuant 3E+5 · ANT 189.72 · OliVe 44.24 | **Tender 36.47 — best of a failing set** | Table II |
| INT4 W+A | OPT-6.7B / 13B / 66B | WikiText-2 PPL | FP16 10.86 / 10.13 / 9.34 | 13.56 / 16.43 / 12.38 | Table II |
| Speedup, **iso-area** | OPT + Llama-2 | × over baseline | ANT / OLAccel / OliVe | **2.63× / 1.84× / 1.48×** | §V, Fig. 10 · simulator |
| Energy efficiency, iso-area | same | × | ANT / OLAccel / OliVe | **1.84× / 1.53× / 1.24×** | §V, Fig. 11 |
| Area / power | — | mm² / W @28 nm, 1 GHz | — | **3.98 mm², 1.60 W peak**; 64×64 PEs + 64 FPUs | Table V, §V |
| Calibration | — | samples | — | **128 from Pile validation**, offline | §V-A |

Left blank: per-bar values of Figs. 10–11; the GLUE/BERT-Large results (read but not
transcribed — they are a generality check, not a headline).

⚠️ **Curiosity, not transcribed as a finding:** on **PTB**, Llama-2 FP16 perplexities (20.83 at
7B, 28.93 at 13B) are *worse* than several quantized rows (Tender INT8: 18.95, 21.13). The
FP16 PTB baselines for Llama-2 look anomalous. Use WikiText-2 columns when citing.

## Cost and requirements

- **Data type — plain INT, and that is the point.** `W8A8` and `W4A4`, standard **symmetric
  linear** quantization on both sides, applied to activation×weight *and* activation×activation
  matmuls (so attention `X_Q × X_K^T` is quantized too). Weights are quantized to INT8 offline.
  **No custom datatype, no mixed precision, no outlier encoding.**
- **Granularity — threshold-binned channel groups, and the group size is *not* fixed.** Channels
  are binned by `CMax` into `G` geometric bands; **band membership is data-dependent**, so
  "group size" varies per group and per tensor by construction. The outlier bands hold few
  channels, the inlier bands many — that asymmetry is the design, not an artefact.
- **Outlier mechanism: isolation by grouping, no separate path.** Outliers get their own
  scale, not their own datatype, precision or hardware lane. The cheapest outlier mechanism in
  the corpus.
- **Accumulator: 32-bit, and it is load-bearing.** Each PE holds an internal 32-bit `Acc`
  register (§IV-A, Table V). The rescale is a **1-bit left shift of that register** at each band
  transition, so every additional channel band consumes one bit of headroom upward — the band
  count `G` is bounded by accumulator width. The paper **asserts** sufficiency rather than
  deriving the bound: *"our intuition is that the systolic array accumulator has a sufficiently
  large bit width, and we can safely requantize"* (§III), and separately that rescaling proceeds
  *"without clipping values due to limited bit width"*. `**inferred / not verified**`: that `G`
  is headroom-limited follows from the mechanism but is never stated or quantified. For
  fairness the **baselines were also extended to 32-bit accumulators** *"due to the large
  reduction length of matrix multiplications in LLMs"* (§V-A) — a good methodological detail.
- **Rescale cost: a 1-cycle bubble** per decomposed matrix, with the rescale signal
  synchronised to the input wavefront and passed along each PE row; the Execution Controller
  holds channel counts, split indices and rescale factors as metadata (§IV-A).
- **Output-stationary was chosen partly for the accumulator.** Because `Acc` is wired to both
  multiplier and shifter, it can be **split into 8 × 4-bit parts** to support an arbitrary
  integer rescale factor (e.g. α = 3) at **8 cycles per rescale** (§IV-A). So α = 2 is the free
  case and the design degrades gracefully rather than breaking if the power-of-two constraint is
  relaxed — an answer to the brief's "power-of-two costs representational freedom" concern that
  the paper never connects to it.
- **Escape hatch.** The per-channel **bias must be added back** (`bias × weights` added to the
  output) for correctness — extra state and an extra add. Final dequantization in FP16, and a
  64-FPU VPU for non-matmul work.
- **Retraining: PTQ**, with offline calibration on **128 Pile samples**. No QAT. This is the
  paper's strongest practical claim — it needs a calibration pass and nothing else.
- **What the hardware pays: one shifter.** That is the entire extension over a commodity
  integer systolic array, which is why it is denser than ANT's and OliVe's decoder-bearing
  arrays and wins on speed at iso-area despite doing nothing clever numerically.

## Limitations and open questions

**Authors admit:** the generation (decode) stage under-utilises the array, and they defer to
batching work; LLaMA-65B is omitted from Table II because *every* scheme's perplexity is
unacceptable; ANT and OliVe need higher precision on most layers, which is why they lose.

**Not admitted:**

1. **INT4 does not work, and the framing obscures it.** "Tender outperforms any other
   outlier-aware PTQ technique (up to 10988× lower perplexity)" is true and nearly
   meaningless — the comparison set is at 3E+5 and 189.72 while Tender is at 36.47 against an
   FP16 base of 5.47. **Best of a failing set.** The honest reading of Table II is that
   INT4 W+A PTQ was unsolved in 2024 by *all* outlier-aware methods, which is exactly the
   opening that non-uniform formats ([`OASIS`](../OASIS/ANALYSIS.md),
   [`Omni-LUT`](../Omni-LUT/ANALYSIS.md)) later exploited. **That is the survey-relevant fact.**
2. **All hardware results are batch size 1 with a 2048:1 input:output ratio** — essentially
   prefill. Tender's own §V-A concedes decode under-utilisation. Its speedups are therefore not
   comparable to the batched-serving regime [`Oaken`](../Oaken/ANALYSIS.md) targets.
3. **The power-of-2 constraint's cost is never isolated.** No ablation against unconstrained
   per-group scales, so the accuracy given up for the shift is unmeasured — the brief flagged
   this and the close read confirms it.
4. **Calibration stability is assumed.** 128 Pile samples fix the channel groups, biases and
   scales for all inputs; no sensitivity study. [`OASIS`](../OASIS/ANALYSIS.md) and
   [`Oaken`](../Oaken/ANALYSIS.md) both study calibration-dataset sensitivity; Tender does not.
5. **Baselines are 2018–2023 accelerators** (OLAccel, ANT, OliVe) and no software INT4 GPU
   baseline is run for the hardware comparison.

## Relation to other entries

- **The restraint pole of the outlier thread.** [`OliVe`](../OliVe/ANALYSIS.md) changes the
  *encoding* (outlier-victim pairs); [`OLAccel`](../OLAccel/ANALYSIS.md) adds *mixed-precision
  lanes*; [`MicroScopiQ`](../MicroScopiQ/ANALYSIS.md) changes the *block format*; Tender changes
  **neither the format nor the datapath** — only the grouping and a shift. Best corpus example
  of designing the algorithm around what commodity hardware already does. Pairs with
  [`Oaken`](../Oaken/ANALYSIS.md) at the low-adoption-barrier end.
- **It is a baseline in four corpus entries** — TransitiveArray, Oaken, Omni-LUT, and cited by
  P3-LLM — and **loses in all of them**. Combined with its own Table II, the corpus position is:
  *Tender's INT8 is competitive; its INT4 is not, and later non-uniform methods use exactly that
  gap as their motivation.*
- **Citation hazard**: see Conclusions — three papers, three "Tender at 4-bit" numbers (36.47 /
  6.42 / 123.1), all under different tensor sets.
- **Seed-tag disagreement — `POW2`.** `venues/ISCA/README.md` tags Tender `INT` `POW2`. But
  **no value in Tender is a power of two**; values are plain symmetric INT4/INT8. What is
  power-of-two is the **ratio between group scale factors**. `TAXONOMY.md` defines `POW2` under
  "Logarithmic / power-of-two / logarithmic number system" — a *number format*. Tagging Tender
  `POW2` therefore signals a log-domain format it does not have. **Suggest `INT8`+`INT4`+`MIXED`
  with the power-of-two-scale idea carried in the free-text Optimization field instead.**

## For the note

### §1 one-line summary

> Bins activation channels into geometric bands by their absolute maximum so outlier channels
> get their own scale, and constrains consecutive band scales to be **exactly 2× apart** so
> accumulating partial sums across bands is a **1-bit shift instead of a floating-point
> requantization** — giving outlier isolation on a plain symmetric-INT systolic array whose
> only extension over commodity hardware is one shifter.

### Proposed values on their four axes

| Axis | Proposed | Evidence (one line) |
|---|---|---|
| **Level** | **`ALGO+ARCH`** | The decomposition rule and bias/scale scheme are the algorithm; the shifter-augmented INT4 systolic array is the architecture, and the paper is explicit that the algorithm's "full potential is realized" only with it. |
| **Q-oriented** | `Q-ORIENTED` | The channel decomposition exists solely to make low-bit quantization survive outliers; remove quantization and nothing remains. |
| **Data type** | **`INT8` + `INT4` + `MIXED`** — **not `POW2`** | Plain symmetric linear integers on both operands (§III-A). Power-of-two applies to the *ratio between group scales*, not to any value's encoding — see the seed-tag disagreement above. |
| **Generation** | **`G3`** | LLM activation-outlier thread (thread 1), the defining G3 problem, on OPT/LLaMA at 6.7B–70B. No new numeric format, so G3 by problem rather than by format design. |
| **Optimization** (free text) | `outlier-aware` `channel-decomposition` `power-of-two-scale-ratio` `implicit-requantization` `runtime-requantization` `shift-based-rescale` `systolic` `commodity-friendly` | — |

### Proposed venue-list row

```
| [x] | [Tender: Accelerating Large Language Models via Tensor Decomposition and Runtime Requantization](https://arxiv.org/abs/2406.12930) | ALGO+ARCH | Q | `INT8` `INT4` `MIXED` | G3 | `outlier-aware` `channel-decomposition` `power-of-two-scale-ratio` `implicit-requantization` | Channels binned into geometric bands by absolute max; consecutive band scales exactly 2× apart so cross-band accumulation is a 1-bit shift. Only extension over commodity INT hardware is one shifter |
```

### §4 fairness verdict

**Iso-area, and unusually explicit about it — the weak point is the INT4 framing, not the
setup.**

- **Iso-area ✓, stated and constructed** — "For an iso-area comparison, we synthesize the MAC
  units and accumulators of each accelerator and configure the number of PEs accordingly", with
  the same memory bandwidth and on-chip buffer, and 32-bit accumulators forced on every
  baseline. That is a real iso-area comparison, not a claimed one.
- **Iso-node ✓** — everything at 28 nm, 1 GHz.
- **Iso-accuracy ✗ at INT4, and this is the problem.** The 2.63× / 1.84× / 1.48× speedups are
  measured at INT4, where **Tender's own perplexity is 36.47 against an FP16 base of 5.47**.
  The speedup is real; the operating point is not deployable. Quote the speedups only with the
  accuracy attached.
- **"Up to 10988× lower perplexity" is a ratio between two failing numbers** and should not be
  cited.
- **Regime ✗ for comparison with later work** — batch 1, 2048:1 in:out, prefill-dominated.
  Decode under-utilisation is admitted. Not comparable to Oaken's batch-256 serving results.
- **Evidence level** — post-synthesis area/power, cycle-level simulator for performance. Not
  pooled in the paper, correctly.

## Abstract (verbatim, arXiv:2406.12930v1)

> Large language models (LLMs) demonstrate outstanding performance in various tasks in
> machine learning and have thus become one of the most important workloads in today's
> computing landscape. However, deploying LLM inference poses challenges due to the high
> compute and memory requirements stemming from the enormous model size and the difficulty
> of running it in the integer pipelines. In this paper, we present Tender, an algorithm-
> hardware co-design solution that enables efficient deployment of LLM inference at low
> precision. Based on our analysis of outlier values in LLMs, we propose a decomposed
> quantization technique in which the scale factors of decomposed matrices are powers of two
> apart. The proposed scheme allows us to avoid explicit requantization (i.e.,
> dequantization/quantization) when accumulating the partial sums from the decomposed
> matrices, with a minimal extension to the commodity tensor compute hardware. Our
> evaluation shows that Tender achieves higher accuracy and inference performance compared
> to the state-of-the-art methods while also being significantly less intrusive to the
> existing accelerators.
