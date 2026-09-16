# P3-LLM: An Integrated NPU-PIM Accelerator for Edge LLM Inference Using Hybrid Numerical Formats

**Venue / Year:** ISCA 2026 · **Link:** https://doi.org/10.1109/ISCA66397.2026.00055 · code https://github.com/yc2367/P3-LLM · **Reader:** Haoxuan · **Date:** 2026-09-10

## Tags

| | |
|---|---|
| **Level** | `ALGO+ARCH` |
| **Q-oriented** | `Q-ORIENTED` |
| **Data type** | `FP4` `INT4` `FP8` `MIXED` |
| **Generation** | `G3` |
| **Optimization** | PIM · NDP · operand-dependent formats · dynamic input-aware smoothing · calibration-free · operator fusion · temporal weight reuse · pre/post-RoPE offload · KV cache |

## 1. One-line summary

Gives **each LLM operand its own numerical format** — BitMoD FP4 weights, FP8-E4M3 activations,
per-head INT4-Asym KV cache smoothed **per request with no calibration set**, and an unsigned
**FP8-S0E4M4 for attention scores derived from the fact that softmax outputs lie in [0,1]**, so
they need no sign bit, no positive exponents and **no scale at all** — then builds DRAM-side PIM
units for exactly those formats, quadrupling multipliers per PCU and spending the resulting timing
slack on **temporal weight reuse at `tCCD_S`**: **4.9× over HBM-PIM for +1.1 pp of HBM area**.

## 2. Data type

**`W4A8KV4P8` — and the `P8` is the point.** Attention scores are a first-class quantized operand with their own format. QuaRot and QoQ keep query *and* scores in FP16.
**Weights.** BitMoD **FP4**: reuses FP4's redundant −0 slot for one of {±5, ±8}, searched **per group of 128**. Base values {±0, ±0.5, ±1, ±1.5, ±2, ±3, ±4, ±6}.
**Activations.** **FP8-E4M3**, direct cast, **per-token**. Chosen over INT8-SmoothQuant by ablation.
**KV-cache.** **INT4-Asym, per-head** (`D_h` = 128), 16-bit scale + **4-bit zero-point** → **4.16 effective bits** = 4 + 20/128.
**Attention scores.** **FP8-S0E4M4** (unsigned, E4, M4, bias −15), *derived*: post-softmax ⇒ non-negative ⇒ no sign bit; ⇒ ≤1 ⇒ only negative exponents ⇒ FP16's [−14,15] collapses to 14 values ⇒ E4 suffices; both saved bits go to mantissa. **No scaling factor at all** — round FP16, keep the top 4 mantissa bits.
**Outliers.** Key cache only — value cache has **no** outlier pattern. Fixed by **dynamic per-channel smoothing computed from the prefill context**, not from a calibration set.
**Pre- vs post-RoPE is a per-model decision with an architectural cost.** Llama-3.1-8B keeps structured channel outliers post-RoPE (smoothing works); Llama-2-7B's go unstructured, forcing pre-RoPE.
**Accumulator.** **Not reported.** §V-A raises the problem (64 multipliers would each need a 32-bit accumulator in plain SIMD) and never gives the width or the structure. The one gap.
**Escape hatch — unusually small.** RoPE, Softmax, element-wise stay FP16 on the NPU. **No FP16 KV window** (unlike KIVI, MANT) because per-head granularity lets each new token quantize immediately. But **`Q·Kᵀ` falls back to the NPU whenever pre-RoPE keys are used.**
**Retraining.** **PTQ *and* calibration-free** — the strongest form of PTQ in the corpus. Neither retraining nor a calibration set.

## 3. Optimization

**A format derived from what its operand mathematically is.** The attention-score format is the
best worked example in the corpus. Softmax outputs are non-negative and ≤ 1, so the sign bit is
dead and every positive exponent is dead; FP16's exponent range [−14, 15] collapses to [−14, −1],
14 distinct values, which 4 bits cover. Both saved bits buy mantissa — M4 where FP8-E4M3 has M3.
The payoff isn't only accuracy (Table II: beats INT8 *and* FP8-E4M3): because the format already
spans exactly [0,1], **attention scores carry no scale**. Every other quantized operand in this
corpus needs one.

**Quantization buys frequency; frequency buys reuse.** A low-precision PCU isn't just smaller — it
closes timing at **2× HBM-PIM's frequency**, so PIM commands issue at `tCCD_S` instead of `tCCD_L`.
One 256-bit weight read out of a DRAM row then serves **two different inputs**, doubling throughput
wherever inputs share weights (batch > 1, or a GQA group), and halving duplicated row activations.
Spatial reuse would have cost multipliers; temporal reuse costs only the slack quantization already
created. Same instinct as RaPiD spending sparsity on clock frequency rather than skip logic.

**The PCU itself.** Built on HBM-PIM: 8 PCUs per channel, each shared by 2 banks. Baseline has
**16 FP16 multipliers**; P3-LLM has **64 at 4 bits**, sized to HBM's 256-bit column access
granularity — 4× throughput for the same access.

**Pre/post-RoPE decides whether attention can run on PIM at all.** Quantize keys **pre-RoPE** and
the cache carries no positional information, so RoPE must be applied online each decode step; RoPE
runs on the NPU in high precision, so **`Q·Kᵀ` stays on the NPU** and the offload is forfeited.
Quantize **post-RoPE** and `Q·Kᵀ` runs on the PCU. The model forces the choice — and the cost is
measured: Llama-2-7B is the one model that does **not** gain from longer context.

**Operator fusion, because dequantization is NPU work.** Scales are folded into operands that are
being quantized anyway: `S_SF` (the key's smoothing factors) into the **query** before its FP8 cast;
`S_V` into the **attention scores** before theirs. Fusing `S_V` can push a score past 1 and out of
FP8-S0E4M4's range, so a **second-level scale** divides `S_V` by `S_Vmax`, reapplied after `P·V`.
Scales are positive by construction, so the fused scores stay unsigned.

**Smoothing, priced.** Per-request, per-channel, from the prefill context: **< 1% memory, < 5 ms
across all layers** (Llama-3.1-8B, 32K, A6000) = **< 2% of a 250 ms TTFT budget**, and **zero** at
decode.

## 4. Results

| | |
|---|---|
| Baseline | Algorithms: **Oaken** (compared KV-only — the right restriction), QuaRot, QoQ, SmoothQuant, AWQ. Accelerators: NPU+FP16, **HBM-PIM**, **Ecco**, **Pimba** (enhanced by P3-LLM with W8A8 it does not have). Same NPU and DRAM config throughout |
| Models / datasets | Llama-1, Llama-2-7B/13B, Llama-3.1-8B, Llama-3.2-3B, Mistral-7B-v0.3. Wikitext-2 + C4 perplexity; MMLU, ARC-Challenge, GSM8K. 4K context (2K for perplexity, to match baselines) |
| Accuracy delta | vs **Oaken** at KV4: **+1.04% accuracy**, better perplexity, **at 4.16 effective bits vs Oaken's 4.8**. vs QuaRot / QoQ: **39% / 22% lower perplexity loss** and **+2.57% / +3.05% accuracy** — while *also* quantizing query and attention scores, which they keep FP16. **< 0.1 PPL** from FP16 |
| Speedup | **4.9× / 2.0× / 3.4×** over HBM-PIM / Ecco / Pimba. **3.9× / 3.0×** over SmoothQuant / AWQ on the same NPU |
| Energy / area | **HBM area overhead 16.4% → 17.5% for 4.9×.** Per PE at 1 GHz vs an FP16 MAC: **4 MACs/cycle at 1.08× area and 0.26× energy/MAC** → 3.7× MACs per area, 3.85× less energy per MAC |
| Technology node | RTL at **TSMC 28 nm** → scaled to **20 nm** (DeepScaleTool) → **scaled again ×10 for DRAM transistor density**. NPU 1 GHz, PCU 500 MHz (HBM2 `tCCD_S`) |
| Evidence level | **RTL + Synopsys DC** (area/power) + **cycle-level simulator** (4 NPU cores, 16 pseudo HBM channels; NPU 128×128 systolic + 16 MB CACTI scratchpad; PIM per **Newton**). No silicon. Area passes through **two** analytical scalings |
| **Is the comparison fair?** | Iso-NPU, iso-DRAM, comparable area; baselines from official repos; Oaken compared KV-only, the right restriction. But area is **scaled analytically twice** and nothing is fabricated; **Pimba is "enhanced" with W8A8 it does not have** before the 3.4× is measured on top; and `W4A8KV4P8` is a **per-model configuration** — query quantization is Llama-3/Mistral only, Llama-2-7B forfeits the `Q·Kᵀ` offload — which every average folds together |

## 5. Comment

## 6. Claude notes

> **Suggestions from the reading agent. Strip this section before copying into
> `QuantArchSurvey/venues/ISCA/notes/`.**

- **Tags human-verified 2026-09-10.** The data-type change from the seed's `INT` `FP` `MIXED` to
  **`FP4` `INT4` `FP8` `MIXED`** is accepted; `ALGO+ARCH`, `Q`, `G3` stand.
  **`venues/ISCA/README.md` still carries the old data-type cell** — I did not edit it. I also checked it against your new `SYS` rule: there's no compiler, ISA or framework
  stack here, and operator fusion is dataflow mapping, so **`SYS` does not apply**.
- **This closes the P3-LLM ↔ Oaken disagreement, and my earlier "half right" was too kind to
  Oaken.** P3-LLM's claim is that Oaken sits at **4.8 effective bits** because ~10% of values stay
  high — the 10% is exact (4% outer + 6% inner), the 4.8 is **Oaken's own Table 2**, and P3-LLM's
  4.16 derives cleanly as 4 + (16+4)/128. So *Oaken pays 0.64 more effective bits and still loses
  by 1.04%* is **right**. Only the phrase "in high precision" is loose — Oaken's outliers are 5-bit,
  one above its inliers, and the real cost is COO metadata. I've updated Oaken's entry.
- **This answers the pre/post-RoPE question you asked during the Oaken read — and the answer is
  architectural, not just algorithmic.** Pre-RoPE keys carry no positional information, so RoPE
  must run online on the NPU in high precision, so `Q·Kᵀ` cannot go to PIM. Post-RoPE keys can.
  Which one is available is decided by the *model*: Llama-3.1-8B keeps structured channel outliers
  after RoPE (smoothing works), Llama-2-7B doesn't (smoothing fails, pre-RoPE forced). And it's
  measured — Llama-2-7B is the only model that doesn't gain from longer context. **Best citation in
  the corpus for "an algorithmic detail about RoPE determines whether attention is offloadable."**
- **§5 material, if you want it.** This opens the **PIM/NDP axis** — every other entry places
  quantized compute in a logic die. The 10× DRAM density penalty inverts the usual pressure: the
  format is chosen for what can be *built* in DRAM, not for what fits the tensor. That's why this
  isn't interchangeable with Oaken despite the overlapping KV story.
- **"Low precision frees a resource — spend it on a different axis" now has two instances**, and I
  think it's worth naming. RaPiD converts sparsity into clock frequency instead of skipped work;
  P3-LLM converts a shorter critical path into `tCCD_S` command timing and thence into temporal
  weight reuse, instead of into more multipliers. Both refuse the obvious spatial answer.
- **Fig. 8 is the corpus's only *measurement* of calibration-set overfitting.** Oaken matches
  P3-LLM's key-cache error on Wikitext-2 — **Oaken's own calibration set** — and degrades on C4;
  QoQ (calibrated on Pile) is worst on both. This claim gets asserted constantly in the literature
  and almost never measured.
- **Granularity as an escape-hatch eliminator, not an error reducer.** Per-head KV granularity lets
  a new token be quantized the instant it's produced, which removes the FP16 residual window KIVI
  and MANT carry. That's a different argument for fine granularity than any other entry makes.
- **A gap worth noting if we cite the area claim.** §V-A raises the accumulator problem — 64
  multipliers would each need a 32-bit accumulator in plain SIMD — and then never gives the width,
  the reduction structure, or its area. For a paper whose thesis is area efficiency under DRAM
  constraints, that's the single number most worth having.
- **BitMoD is load-bearing and outside the corpus** — it *is* P3-LLM's weight format. Add it to the
  running list with ANT (six entries), GOBO (three), WRPN and PACT.
