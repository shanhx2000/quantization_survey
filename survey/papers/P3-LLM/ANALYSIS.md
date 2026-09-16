# P3-LLM — paper notes

**P3-LLM: An Integrated NPU-PIM Accelerator for Edge LLM Inference Using Hybrid Numerical Formats**
Yuzong Chen, Chao Fang, Xilai Dai, Yuheng Wu, Thierry Tambe, Marian Verhelst, Mohamed
Abdelfattah
**ISCA 2026** (2026 ACM/IEEE 53rd Annual International Symposium on Computer Architecture),
pp. 604–619 ｜ DOI: **10.1109/ISCA66397.2026.00055**
Publication info verified 2026-09-02 from the **official ISCA 2026 proceedings package**
(title, authors, pages, DOI and abstract all read from its `assets/data/data.js`).
Archived here: **the published proceedings PDF** (`506501a604.pdf`, 16 pages) — not a preprint.

Status: **note ready** ｜ Last updated: 2026-09-10
Tags: `pim-ndp` `mixed-precision` `analytical-dtype` `dtype-granularity` `kv-cache` `accelerator`
How far it was read: **full close read of §I-§IX.** §III (motivation, including the KV-cache
distribution study in Fig. 5), §IV (quantization framework — smoothing, all four operand formats),
§V (architecture — PCU, offload mapping, operator fusion) and §VI (evaluation, Tables IV-VIII)
read line by line; §II skimmed for the GQA background; §VII-VIII read in full. Figures are bitmaps
in the extraction, so every number below comes from the prose or from a recoverable table.
Read after [`RaPiD`](../RaPiD/ANALYSIS.md), and specifically to settle this corpus's open
disagreement between P3-LLM and [`Oaken`](../Oaken/ANALYSIS.md) — see *Relation to other
entries*.
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> The PDF is **not committed** (1.6 MB). It came from the proceedings package a human
> supplied, now archived at [`archieve/ISCA 2026.zip`](../../../archieve/), entry `pdfs/5065-3nexm57sBmVa6MJtFTiSrb/506501a604/506501a604.pdf`.
> **There is no public URL for it** — this is not an arXiv paper. Re-extract with
> `python3 extract.py` → `extracted/` (committed, greppable).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, 2026 row.

---

## Brief

### 1. Motivation

Edge LLM inference suits an NPU (compute-bound prefill GEMM) plus DRAM-based PIM (memory-
bound decode GEMV) split. But PIM compute units built for FP16 are **area- and power-
prohibitive in DRAM**, where transistor density is ~10× worse than logic — which has
confined PIM's practical speedup to single-batch inference on older models. Grouped-query
attention raises arithmetic intensity above one, so that confinement now bites.

### 2. Overview

Three parts: a **flexible mixed-precision quantization scheme using hybrid numerical
formats**, choosing a different format per LLM operand; PIM compute units co-designed for
exactly those formats, so throughput rises under an iso-area DRAM constraint; and dataflow
optimization with **operator fusion** to minimize runtime dequantization overhead.

### 3. Pros and cons

**Pros**

- The format choice is driven by what can be built cheaply in DRAM — co-design in the strong
sense, where the numeric format is selected for the substrate rather than the other way
round.
- Wins on accuracy against both comparison classes: 1.04% better than
[`Oaken`](../Oaken/ANALYSIS.md) at 4-bit KV, and 39%/22% lower perplexity loss than
QuaRot/QoQ **while quantizing more aggressively** (8-bit queries and attention scores).
- 4.9×/2.0×/3.4× average speedups over HBM-PIM, [`Ecco`](../Ecco/ANALYSIS.md) and Pimba;
open-sourced.

**Cons**

- Scoped to **edge, low-batch** inference; the DRAM-area argument that motivates it is
weaker in datacenter settings with different cost structures.
- Area is scaled analytically for the DRAM process (the 10× density factor) rather than laid
out, so the iso-area claim rests on a model.
- 'Hybrid numerical formats' means several formats coexisting, which pushes complexity into
the compiler/dataflow — the operator-fusion work is necessary, not optional.

### 4. Where it applies

The corpus's strongest **PIM/NDP + mixed-precision** entry and a KV-cache participant. Read
with [`NDPLowBitFP`](../NDPLowBitFP/ANALYSIS.md) (the compiler-side view of the same
problem) and [`RAELLA`](../RAELLA/ANALYSIS.md) (the analog view).

---

## Corrections to the brief

The brief was accurate on all four points. What it did not have:

1. **The scheme is `W4A8KV4P8` — and the `P8` is the finding.** Attention scores are a
   **first-class quantized operand with their own dedicated format**, which no other entry in this
   corpus does. QuaRot and QoQ keep both query and attention-scores in FP16 **verified** (§VI-A).
2. **The pre/post-RoPE choice decides whether attention can run on PIM at all**, and the *model*
   forces the choice. This is the paper's sharpest algorithm→architecture consequence and it is
   buried in §V-B and one sentence of §VI-C.
3. **It settles the corpus's open P3-LLM-vs-Oaken disagreement**, and in Oaken's disfavour on the
   substance — see *Relation to other entries*.
4. **The iso-area claim is stronger than "analytically scaled" suggests.** It is +1.1 percentage
   points of total HBM area (16.4% → 17.5%) for **4.9×** — Table VII **verified**.

---

## Conclusions

**The idea is that a format should be derived from what its operand mathematically *is*, and
FP8-S0E4M4 is the best worked example of that in the corpus.** Attention scores come out of a
softmax, so: they are non-negative, therefore **no sign bit**; and they are ≤ 1, so of FP16's
exponent range [−14, 15] only the negative half is ever used — **14 distinct values, which 4
exponent bits cover**. The bit saved on the sign and the bit saved on the exponent both go to the
mantissa, giving **4 mantissa bits where FP8-E4M3 has 3**. The payoff is not just accuracy (Table
II: it beats both INT8 and FP8-E4M3): because the format already spans exactly [0, 1], **attention
scores need no scaling factor at all** — you round an FP16 value and keep its top 4 mantissa bits.
Every other quantized operand in this corpus carries a scale; this one does not, because the
format was designed to fit the operand's range rather than the other way round.

**Its second idea is that quantization buys frequency, and frequency buys reuse.** A low-precision
PCU is not just smaller — it closes timing at **2× HBM-PIM's frequency**, which lets P3-LLM issue
PIM commands at `tCCD_S` instead of `tCCD_L`. The same 256-bit weight slice read out of a DRAM row
then serves **two different inputs**, doubling throughput wherever inputs share weights (batch > 1,
or a GQA group). Spatial reuse would have cost multipliers and area; temporal reuse costs nothing
but the timing slack the quantization already created. This is structurally the same move
[`RaPiD`](../RaPiD/ANALYSIS.md) makes when it spends sparsity on clock frequency rather than on
skip logic — **convert a resource low precision frees into a different kind of throughput** — and
two independent instances make it worth naming in the survey.

**The pre/post-RoPE finding deserves to outlive this paper.** Quantize the key cache **pre-RoPE**
and it carries no positional information, so RoPE must be applied online each decoding step; RoPE
runs on the NPU in high precision, so **`Q·Kᵀ` must stay on the NPU** and the PIM offload is
forfeited. Quantize **post-RoPE** and `Q·Kᵀ` runs on the low-precision PCU. Which one you may use
is decided by the model: Fig. 5 shows Llama-3.1-8B keeps **structured per-channel** key outliers
after RoPE (so smoothing works, so post-RoPE is available), while Llama-2-7B's post-RoPE outliers
become **unstructured** (so per-channel smoothing cannot fix them, so pre-RoPE is forced). And the
cost is measured: **Llama-2-7B is the one model that does not gain from longer context**, precisely
because its `Q·Kᵀ` runs on the NPU. An algorithmic detail about rotary embeddings determines
whether attention is offloadable.

**Its smoothing is the honest answer to a criticism it makes of others.** Oaken and QoQ set outlier
thresholds and smoothing factors offline from a calibration set; P3-LLM computes smoothing factors
**from the prefill context of the actual request**, so there is nothing to overfit. Fig. 8 shows the
consequence cleanly: Oaken matches P3-LLM's key-cache error on **Wikitext-2 — its own calibration
set** — and degrades on C4, while QoQ (calibrated on Pile) is worst on both. The cost is small and
measured: **< 5 ms across all layers** at 32K context on an A6000, **< 2%** of a 250 ms
time-to-first-token budget, **< 1%** memory, and **zero** decoding-stage cost.

**What to be careful about.** The paper's headline `W4A8KV4P8` is not uniformly applied: query is
quantized to FP8-E4M3 **only for Llama-3 and Mistral**, and Llama-2-7B uses pre-RoPE keys and so
loses the attention offload. Two of the paper's own configuration choices vary per model, and the
averages fold them together.

---

## Method

**Four operands, four formats — this is the whole point.**

| Operand | Format | Granularity | Scale |
|---|---|---|---|
| **Weights** | **BitMoD FP4** [6] | per-group, **group size 128** | per-group + a searched special value |
| **Activations** | **FP8-E4M3**, direct cast | **per-token** | per-token |
| **KV-cache** | **INT4-Asym** | **per-head, `D_h` = 128** | 16-bit scale + **4-bit zero-point** |
| **Attention scores** | **FP8-S0E4M4** (unsigned, 4-bit exp, 4-bit mantissa, bias −15) | — | **none — no scaling factor at all** |

**BitMoD FP4 for weights** (§IV-C) **verified**. FP4's encoding wastes a slot on negative zero.
BitMoD reuses it: base values {±0, ±0.5, ±1, ±1.5, ±2, ±3, ±4, ±6} plus four candidates
{±5, ±8}, one of which replaces −0, **searched per weight group**. Cheaper than asymmetric integer
for the same error, at minimal hardware cost.

**FP8-S0E4M4 for attention scores** (§IV-B) **verified** — derived, not chosen:

- post-softmax ⇒ non-negative ⇒ **drop the sign bit**;
- post-softmax ⇒ ≤ 1 ⇒ only negative exponents occur ⇒ FP16's [−14, 15] collapses to **[−14, −1],
  14 values** ⇒ **4 exponent bits suffice**;
- the two saved bits go to the mantissa ⇒ **M4**, one more than FP8-E4M3.

Consequence: **no scaling factor**. Quantization is "round the least significant bits of every
FP16 attention-score and keep its highest 4 mantissa bits."

**KV-cache: INT4-Asym at per-head granularity** (§IV-A, §V-C) **verified**. `D_h` = 128 for every
model evaluated. Effective precision **4 + (16+4)/128 = 4.16 bits** — derivation checks out.
Per-head granularity has a structural payoff the paper states plainly: each newly generated token
can be quantized **immediately**, which **eliminates the FP16 buffer window** that KIVI and MANT
must keep. No residual high-precision window is an escape hatch this design does not have.

**Dynamic input-aware smoothing** (§IV-A) **verified**. Per-channel smoothing factors computed
**from the prefilling context**, no calibration dataset. Two differences from prior per-channel
smoothing, both stated: (i) no offline threshold or factor, so no overfitting; (ii) **both**
pre-RoPE and post-RoPE are analysed, where KIVI [28] is pre-only and QoQ [53] post-only.
Cost: < 1% memory; < 5 ms across all layers, Llama-3.1-8B, 32K context, A6000; < 2% of a 250 ms
TTFT SLO; **nothing at decode time**.

**Why the key cache needs it and the value cache does not** (§III, Fig. 5) **verified**:

| Tensor | Outlier structure |
|---|---|
| Value cache | **none** |
| Key cache, **pre-RoPE** | distinct **channel** outliers — smoothing works |
| Key cache, **post-RoPE**, Llama-3.1-8B | **still** distinct channel outliers — smoothing works |
| Key cache, **post-RoPE**, Llama-2-7B | "much less structured" — smoothing **cannot** fix it |

**PCU microarchitecture** (§V-A) **verified**. Built on **HBM-PIM** [49]: one PIM channel holds
8 PCUs, each shared by **2 banks** to amortise area. Baseline HBM-PIM PCU = **16 FP16
multipliers**; P3-LLM PCU = **64 multipliers**, sized to match HBM's **256-bit column access
granularity** at 4-bit operands — **4× the compute throughput**. The paper names the problem this
creates: at that multiplier count a plain SIMD organisation needs a 32-bit accumulator per
multiplier, and the register file dominates.

**Throughput-enhanced PCU — temporal reuse** (§V-D) **verified**. The low-precision PCU closes
timing at **2× the frequency** of HBM-PIM's FP32-accumulator design. HBM-PIM issues one PIM command
per **`tCCD_L`** (4 memory bus cycles); P3-LLM issues at **`tCCD_S`** (half of `tCCD_L` in every HBM
generation). One 256-bit weight read therefore serves **two inputs**, halving duplicated DRAM row
activations and their energy.

**Offload mapping** (§V-B) **verified**. NPU keeps RoPE, Softmax and all element-wise work in high
precision; GEMM/GEMV goes to PIM. **The one exception is `Q·Kᵀ`**, whose home depends on the
pre/post-RoPE decision above.

**Operator fusion to kill runtime dequantization** (§V-C) **verified**. Dequantization scaling is
high-precision NPU work, so it is folded into operands that are being quantized anyway:

- linear layers — dequant scaling applied **after** the matmul;
- `Q·Kᵀ` — the post-RoPE key's per-channel smoothing factors `S_SF` are **fused into the query**
  before its FP8 quantization;
- `P·V` — per-value-head scales `S_V` are **fused into the attention scores** before FP8
  quantization. This can push a score above 1, outside FP8-S0E4M4's range, so a **second-level
  scale** divides `S_V` by `S_Vmax` to return it to [0, 1]; `S_Vmax` is multiplied back into the
  `P·V` result. Scales are positive by construction, so the fused scores stay unsigned.

**Code is open-sourced**: `https://github.com/yc2367/P3-LLM` **verified** (§I footnote).

---

## Key numbers, with their frame

Evidence level: **RTL (SystemVerilog) + Synopsys Design Compiler at TSMC 28 nm**, scaled to
HBM-PIM's **20 nm** with **DeepScaleTool**, then **scaled again by the 10× DRAM transistor-density
penalty**; performance from a **cycle-level simulator** (4 NPU cores, 16 pseudo HBM channels; NPU
from [27] — 128×128 systolic array, 128-way VPU, 16 MB scratchpad modelled in CACTI; PIM subsystem
following **Newton** [23]). **NPU 1 GHz, PCU 500 MHz** (HBM2 `tCCD_S` = 2 DRAM clocks). **No
silicon.** Accuracy reproduced from baselines' official repositories. Context length **4K**
(2K for the perplexity table, to match baselines' published numbers).

| Setting | Model | Metric | Baseline | Result | Source |
|---|---|---|---|---|---|
| **Iso-area co-design payoff** | — | HBM area overhead → speedup | HBM-PIM **16.4%**, 1.0× | **17.5% → 4.9×** — +1.1 pp of HBM area | Table VII **verified** |
| PCU area split | — | compute / buffer, mm² | HBM-PIM 7.7 / 6.2 | **8.4 / 6.2** | Table VII **verified** |
| **Per-PE efficiency, 1 GHz** | — | MACs/cycle · area · energy/MAC, normalised to an FP16 MAC | HBM-PIM 1 MAC, 1023.1 µm² (1.00×), 0.69 pJ (1.00×) | **4 MACs, 1109.2 µm² (1.08×), 0.18 pJ (0.26×)** → **3.7× MACs per area, 3.85× less energy per MAC** | Table VIII **verified** |
| " — the other co-designs | — | same | MANT 2 MACs, 0.70×, 0.58× · BitMoD 2 MACs, 1.26×, 0.88× | — | Table VIII **verified** |
| Compute throughput | — | multipliers per PCU | HBM-PIM **16 FP16** | **64 @ 4-bit → 4×** | §V-A **verified** |
| " | — | PIM command rate | HBM-PIM `tCCD_L` | **`tCCD_S` = ½ → 2× temporal reuse** | §V-D **verified** |
| **End-to-end decoding speedup** | 5 models, 4K context | average | **HBM-PIM / Ecco / Pimba (enhanced)** | **4.9× / 2.0× / 3.4×** | §I, §VI **verified** |
| vs software quantization on the same NPU | BS 1-8, 4K | decoding throughput | **SmoothQuant / AWQ** | **3.9× / 3.0×** | §VI-C **verified** |
| Pimba's own headroom | — | speedup from adding W8A8 to Pimba | original Pimba (KV-only) | **2.1×** — then P3-LLM is 3.4× on top | §VI-C **verified** |
| **KV-cache accuracy** | Llama family, avg | reasoning-task accuracy, KV4 | **Oaken** | **+1.04%** | Table V **verified** |
| " | avg | perplexity | Oaken | **outperforms Oaken, < 0.1 PPL loss vs FP16** | §VI-B **verified** |
| **Effective KV precision** | — | bits | **Oaken 4.8** (≈10% outliers kept high) | **P3-LLM 4.16** = 4 + (16+4)/128 | §VI-B **verified, derivation checks** |
| Weight-activation accuracy | avg | perplexity **loss** | **QuaRot / QoQ** | **39% / 22% lower** — while also quantizing query and attention-scores, which they keep in FP16 | §VI-B **verified** |
| " | avg | reasoning accuracy | QuaRot / QoQ | **+2.57% / +3.05%**, "particularly pronounced on Llama-3.2-3B" | Table V **verified** |
| **Smoothing cost** | Llama-3.1-8B, 32K ctx, A6000 | wall time, all layers | — | **< 5 ms**, i.e. **< 2%** of a 250 ms TTFT SLO; **< 1%** memory; **0** at decode | §IV-A **verified** |
| Context-length sensitivity | 2K → 16K, batch 1 | speedup trend | — | **improves for every model except Llama-2-7B**, which uses pre-RoPE keys and so runs `Q·Kᵀ` on the NPU | §VI-C **verified** |
| Attention-score format | — | perplexity | INT8, FP8-E4M3 | **FP8-S0E4M4 beats both**, near-lossless | Table II **verified** |

**Configuration varies by model and the averages hide it:** query is quantized to FP8-E4M3
**only for Llama-3 and Mistral**; Llama-2-7B uses **pre-RoPE** key quantization and forfeits the
`Q·Kᵀ` offload. Attention-score quantization is the one thing applied to all models.

---

## Cost and requirements

| | |
|---|---|
| **Smoothing** | Per-channel factors recomputed **per request** from the prefill context. < 1% memory, < 5 ms/32K-context, **< 2% of TTFT**, nothing at decode. Cheap, but it is a prefill-stage dependency the decode path inherits |
| **Format zoo** | Four formats coexisting (FP4-BitMoD, FP8-E4M3, INT4-Asym, FP8-S0E4M4). The PCU must support all of them; the operator-fusion work in §V-C is **necessary, not optional** |
| **Scales** | Weights per-group-128 + a searched special value; activations per-token; KV per-head 16-bit scale **+ 4-bit zero-point**; **attention scores carry none** |
| **Second-level scaling** | Fusing `S_V` into attention scores can exceed FP8-S0E4M4's [0,1] range, so `S_V` is renormalised by `S_Vmax` and `S_Vmax` reapplied after `P·V` — an extra scalar per value head |
| **Accumulator** | Not reported as a width. §V-A names the problem — 64 multipliers would need a 32-bit accumulator each in plain SIMD — but the resolution is not stated numerically. **Gap** |
| **Escape hatch — smaller than most** | RoPE, Softmax and element-wise ops stay high-precision on the NPU. **No FP16 KV window** (unlike KIVI, MANT). But **`Q·Kᵀ` on the NPU whenever pre-RoPE keys are used** is a large, model-dependent one |
| **Retraining** | **PTQ, and calibration-free** — the strongest version of PTQ in the corpus, since it needs neither retraining nor a calibration set |
| **Deployment scope** | **Edge, low batch.** The DRAM-area argument that motivates the whole design is weaker where cost structures differ |
| **Substrate** | Requires HBM-PIM-class hardware. Adoption barrier is at the memory-vendor level, not the accelerator level |

---

## Limitations and open questions

**Admitted.**

- Scoped to edge, low-batch decoding; §VII says so.
- Area is **analytically** scaled twice — 28 nm → 20 nm via DeepScaleTool, then by the 10× DRAM
  density factor. The iso-area claim rests on a model, and the paper is explicit about the method.
- Llama-2-7B's lower context-length gain is reported and explained rather than smoothed over.

**Unadmitted, and material.**

- **The accumulator question is raised and dropped.** §V-A states that 64 multipliers in a SIMD
  organisation would each need a 32-bit accumulator, "leading to substantial register overhead" —
  and then the text moves to §V-B without giving the accumulator width, the reduction structure,
  or its area. For a paper whose central claim is area efficiency under DRAM constraints, this is
  the one number most worth having.
- **`W4A8KV4P8` is a per-model configuration, not a scheme.** Query quantization applies to
  Llama-3 and Mistral only; pre- vs post-RoPE differs per model. Every average in §VI mixes these.
- **The Ecco and Pimba baselines are modified by P3-LLM.** Pimba is "enhanced" with W8A8
  quantization it does not have (and credited 2.1× for it) before P3-LLM's 3.4× is measured on
  top. That is generous and clearly stated — but it means the 3.4× is against a design Pimba's
  authors did not publish.
- **No sensitivity study on `D_h` = 128.** Per-head granularity is load-bearing for both the 4.16
  effective bits and the no-FP16-window property, and every evaluated model happens to have
  `D_h` = 128. What happens at 64 or 256 is not asked.
- **Fig. 5 is a two-model observation carrying a large architectural conclusion.** That Llama-2-7B
  loses structured post-RoPE outliers and Llama-3.1-8B does not is shown for those two models, from
  "representative layers and heads". Whether this is a Llama-2-vs-Llama-3 property, a model-size
  property, or something narrower is not established — and the offloadability of attention depends
  on the answer.
- **No accuracy result for the full hardware configuration.** Accuracy is reported for the
  quantization scheme; the PCU's actual arithmetic (rounding, accumulation order, the
  second-level `S_Vmax` scaling) is not shown to reproduce it.

---

## Relation to other entries

**It settles this corpus's open disagreement with [`Oaken`](../Oaken/ANALYSIS.md), and my earlier
"half right" verdict should be upgraded.** P3-LLM §VI-B: Oaken "has a higher effective KV-cache
precision of **4.8 bits** due to its inefficient offline calibration, which keeps a large ratio
(**∼10%**) of outliers in high precision."

- The **10%** is exact — Oaken's own scheme is 4% outer + 6% inner.
- The **4.8 bits** is confirmed by **Oaken's own Table 2** (4.82 / 4.82 / 4.89).
- P3-LLM's **4.16** is derivable and correct: 4 + (16 + 4)/128.
- So the substantive claim — *Oaken pays 0.64 more effective bits and still loses by 1.04%
  accuracy* — **is right**.

The only imprecision is the phrase "in high precision": Oaken's outliers are **5-bit**, one bit
above its inliers, and the real cost is the COO metadata, not the precision. That is loose wording,
not a wrong claim, and it does not touch the argument. **Update the Oaken entry accordingly.**

**It also gives the survey a clean statement of the calibration-overfitting problem** — Fig. 8:
Oaken matches P3-LLM's key-cache quantization error **on Wikitext-2, which is Oaken's own
calibration set**, and degrades on C4; QoQ, calibrated on Pile, is worst on both. Calibration-set
overfitting is asserted often in this literature and rarely measured; this is the measurement.

**It opens the PIM/NDP axis, which nothing read so far occupies.** Everything else in the corpus
places quantized compute in a *logic* die — a systolic array, a PE array, a tensor core. P3-LLM's
premise is that the substrate has a **10× transistor-density penalty**, which inverts the usual
design pressure: the format is chosen for what can be built cheaply in DRAM rather than for what
best fits the tensor. That is co-design in the strong sense and it is the reason this entry is not
interchangeable with [`Oaken`](../Oaken/ANALYSIS.md) despite the overlapping KV-cache story.
Read next to [`NDPLowBitFP`](../NDPLowBitFP/ANALYSIS.md) and [`RAELLA`](../RAELLA/ANALYSIS.md).

**"Low precision frees a resource; spend it on a different axis" now has two instances.** RaPiD
converts sparsity into **clock frequency** under a power budget rather than into skipped work;
P3-LLM converts a shorter critical path into **`tCCD_S` command timing**, and thence into temporal
weight reuse, rather than into more multipliers. Both refuse the obvious spatial answer. That
pattern is worth naming in the survey.

**On the granularity axis it lands at per-head / per-token**, and it is the first entry to give a
*structural* reason rather than an accuracy reason: per-head granularity means a new token can be
quantized the instant it is produced, which **removes the FP16 residual window** that KIVI and MANT
carry. Granularity as an escape-hatch eliminator, not just as an error reducer.

**It is the first entry to treat attention scores as their own operand class.** `W4A8KV4P8`. Every
other KV-cache paper here (`Oaken`, `Omni-LUT`) quantizes K and V and leaves the softmax output
alone. Structurally this is the same instinct as `RaPiD`'s HFP8 — *different formats for different
tensor roles inside one computation* — reached from a third direction.

**Node and evidence.** 28 nm RTL → 20 nm → ×10 DRAM density, plus a cycle-level simulator. The
corpus now spans 7 nm to 65 nm; P3-LLM is the only entry whose area figure passes through **two**
analytical scalings, and the only one where the target process is DRAM rather than logic. Any
aggregate area table needs a column for that.

**Outside-corpus references it makes load-bearing:** **BitMoD** [6] (its entire weight format),
**HBM-PIM** [49] (its substrate and baseline), **Newton** [23] (its simulation methodology),
**Pimba** [44], **QuaRot** [2] and **QoQ** [53]. BitMoD in particular is doing as much work here as
ANT does in six other entries.

---

## For the note

**§1 one-line summary.** Gives **each LLM operand its own numerical format** — BitMoD FP4 weights,
FP8-E4M3 activations, per-head INT4-Asym KV cache smoothed **per request** with no calibration set,
and an **unsigned FP8-S0E4M4 for attention scores derived from the fact that softmax outputs lie in
[0, 1]** and therefore need no sign bit, no positive exponents and no scale at all — then builds
DRAM-side PIM compute units for exactly those formats, quadrupling multipliers per PCU and spending
the resulting timing slack on **temporal weight reuse at `tCCD_S`**, for **4.9× over HBM-PIM at
+1.1 percentage points of HBM area**.

**Proposed tags — one disagreement with the seed row, on Data type. Human-verified 2026-09-10.**

| Axis | Value | Evidence |
|---|---|---|
| **Level** | `ALGO+ARCH` | Genuine co-design: §IV is an algorithm, §V is hardware, and the format choice is explicitly driven by DRAM buildability. Seed agrees. **Checked against the new `SYS` rule** — there is no compiler, ISA or framework stack here; operator fusion is dataflow mapping, so `SYS` does **not** apply |
| **Q-oriented** | `Q-ORIENTED` | Swap everything for plain INT8 and the four-format PCU, the smoothing path, the fusion of `S_SF`/`S_V`, and the second-level `S_Vmax` scaling all lose their purpose. Seed agrees |
| **Data type** | **`FP4` `INT4` `FP8` `MIXED`** | **Seed says `INT` `FP` `MIXED`; changed, and confirmed by the human 2026-09-10.** The taxonomy prefers bitwidths, and all four are known exactly: BitMoD **FP4** weights, **INT4**-Asym KV, **FP8**-E4M3 activations, **FP8**-S0E4M4 attention scores |
| **Generation** | `G3` | Outlier-driven (dynamic per-channel key smoothing) and KV-cache-centric — squarely the G3 paradigm. Seed agrees |
| **Optimization** | `PIM` `NDP` `hybrid formats` `operator fusion` `KV cache` + **`operand-dependent formats`** `dynamic input-aware smoothing` `calibration-free` `temporal weight reuse` `pre/post-RoPE offload` | Seed has the first five; the rest are the mechanisms |

**§4 fairness verdict.** Iso-NPU, iso-DRAM, comparable total area; baselines reproduced from their
official repos; Oaken compared **KV-only**, which is the right restriction. Against that: area is
**analytically scaled twice** (28→20 nm, then ×10 for DRAM density) and nothing is fabricated;
**Pimba is "enhanced" by P3-LLM with W8A8 it does not have** before the 3.4× is measured on top; and
`W4A8KV4P8` is a **per-model configuration** — query quantization is Llama-3/Mistral only, and
Llama-2-7B forfeits the `Q·Kᵀ` offload — which every average folds together.

**Proposed venue-list row:**

```
| [ ] | [P3-LLM: An Integrated NPU-PIM Accelerator for Edge LLM Inference Using Hybrid Numerical Formats](https://doi.org/10.1109/ISCA66397.2026.00055) | *close read* | ALGO+ARCH | Q | `FP4` `INT4` `FP8` `MIXED` | G3 | `PIM` `NDP` `operand-dependent formats` `dynamic input-aware smoothing` `calibration-free` `operator fusion` `temporal weight reuse` `KV cache` | A format derived per operand — **FP8-S0E4M4 for attention scores drops the sign bit and all positive exponents because softmax outputs lie in [0,1], so they need no scale at all**. PIM units co-designed for exactly those formats: 4.9× over HBM-PIM for +1.1 pp of HBM area |
```

## Abstract (verbatim, ISCA 2026 proceedings)

> The substantial memory bandwidth and computational demands of large language models (LLMs)
> present critical challenges for efficient inference. To tackle this, the literature has
> explored heterogeneous systems that combine neural processing units (NPUs) with DRAM-based
> processing-in-memory (PIM) for LLM acceleration. However, the high-precision PIM compute
> units incur significant area and power overhead in DRAM technology, limiting the effective
> computation throughput. In this paper, we introduce P3-LLM, a novel NPU-PIM integrated
> accelerator for edge LLM inference. Our approach is threefold: First, we propose a
> flexible mixed-precision quantization scheme, which leverages hybrid numerical formats to
> quantize different LLM operands with high compression efficiency and minimal accuracy
> loss. Second, we architect an efficient PIM accelerator for P3-LLM, featuring enhanced
> compute units to support hybrid numerical formats. Our careful choice of numerical formats
> allows to co-design low-precision PIM compute units that significantly boost the
> computation throughput under iso-area constraints. Third, we optimize the low-precision
> dataflow of different LLM modules by applying operator fusion to minimize the overhead of
> runtime dequantization. Evaluations on diverse LLMs and tasks demonstrate that P3-LLM
> achieves higher accuracy than state-of-the-art KV-cache quantization and weight-activation
> quantization algorithms. Combining the proposed quantization scheme with low-precision PIM
> architecture co-design, P3-LLM yields an average of 4.9×, 2.0×, and 3.4× speedups over
> state-of-the-art LLM accelerators HBM-PIM, Ecco, and Pimba, respectively. Code is
> available at https://github.com/yc2367/P3-LLM.
