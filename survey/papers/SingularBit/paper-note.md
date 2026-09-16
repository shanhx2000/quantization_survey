# SingularBit: Exploiting Synergy of SVD and Low-Bit Quantization for Weight and KV Compression in LLM Inference

**Venue / Year:** ISCA 2026 · **Link:** https://doi.org/10.1109/ISCA66397.2026.00079 · **Reader:** Haoxuan · **Date:** 2026-09-14

## Tags

| | |
|---|---|
| **Level** | `ALGO+ARCH` |
| **Q-oriented** | `Q-ORIENTED` |
| **Data type** | `SVD` `INT2` `INT1` `MIXED` |
| **Generation** | `G3` |
| **Optimization** | SVD · rank-aware mixed precision · analytical precision allocation · token-and-rank importance · offline decomposition · shared compression engine · dual memory wall · weight + KV |

## 1. One-line summary

Allocates precision along the **spectral axis** rather than any tensor axis — decompose weights and
KV by SVD, then give more bits to components with large singular values and **1–2 bits to the tail**
— addressing both halves of the **Dual Memory Wall** (decode starts weight-bound and becomes
KV-bound at an unpredictable crossover) with one principle, keeping SVD **entirely offline** so the
runtime path is only projection plus token- and rank-aware quantization, on a tensor core supporting
**rank-wise mixed precision** and a shared compression engine whose chip-level overhead stays
**under 4%**: **4.00× on a GPU from the algorithm alone**, 5.3× speedup and 4.8× energy on the
accelerator.

## 2. Data type

**Precision allocated by rank — a new axis.** Everyone else allocates along tensor geometry (per-tensor, channel, token, group, region, head). This allocates along the **spectrum**, justified by a data property: **singular values decay rapidly in both weight matrices and attention distributions**.

### Weights — `SingularBit-W`, entirely offline

**Decomposition: offline, once.** SVD is "applied **once offline** to the weight tensors, and **no decomposition is performed during inference**."

**Allocation: rank-aware mixed precision**, guided by **singular value magnitude**. Rank space split into K regions with boundaries `{r_k}` and bitwidths `{b_k}`; **most parameters reach 1–2 bits**. Evaluated at 2/3/4-bit average.

**The allocation is analytical, not searched.** `B_avg = (1/R)·Σ b_k·(r_k − r_{k−1})`, with one decay parameter `0 < p < 1`. Its "analytical nature **eliminates the need for empirical simulations**."

**Executed by** the **SingularBit Tensor Core**, which must support **rank-wise mixed precision** — different bitwidths across rank regions of one matmul.

### KV cache — `SingularBit-KV`, online

**Two importance axes at once: token importance × rank significance.** The only entry in the corpus using two simultaneously.

**Runtime path is projection + quantize only.** KV generation computes `K' = xU_WK`, `V' = xU_WV` — projections into the already-decomposed basis — and then "**token- and rank-aware mixed-precision quantization and packing**". **No decomposition at runtime.**

**Executed by** the **SingularBit Compression Engine**, shared across **≥ 8 tensor cores**, running **in parallel with post-attention computation** and finishing before the next attention layer — **off the critical path**.

### Both paths

**Outliers.** No outlier class — the high-rank regions *are* the protected components. Contrast ASVD, which pre-transforms to mitigate activation outliers.

**Accumulator.** Not reported.

**Escape hatch.** The leading rank regions, and whatever precision the `U` projections are carried at — **the basis storage is never netted out of the reported ratios**.

**Retraining.** **None.** PTQ; decomposition and allocation are offline preprocessing.

## 3. Optimization

**The Dual Memory Wall framing earns the design.** A decode session starts **weight-bound**
(O(L·D²·b_W) per token) and becomes **KV-bound** (O(N·L·D·b_KV)) as the sequence grows — and **the
crossover is unpredictable per request**. That's a real argument against one-sided compression: a
weight-only or KV-only design is correct for only part of any given request. Applying one principle
to both is the response, which is why `SingularBit-WKV` is the configuration that matters.

**The expensive part of SVD is removed rather than paid.** SVD-based compression normally trades
decomposition cost against compression; here the decomposition is hoisted entirely offline and the
runtime path reduces to a projection into an already-decomposed basis plus quantization. That single
decision is what makes an SVD scheme deployable at decode time.

**It quantizes *within* the decomposition rather than truncating it.** ASVD pre-transforms for
activation outliers, SVD-LLM whitens for truncation-awareness, SliceGPT removes rows and columns.
SingularBit keeps the tail and **spends fewer bits on it** — SVD supplies an *importance ordering*,
and quantization rather than truncation exploits it. That is the "synergy" of the title.

**The overhead accounting is unusually careful.** The compressor is **21.5 mW (23.3%) and 1.23 mm²
(27.9%) of the compression engine** — but **one engine is shared across ≥ 8 tensor cores**, so
**chip-level overhead is under 4%** in area and power, and compression "proceeds in parallel with the
post-attention computation and finishes before the next attention layer begins", so it is **off the
critical path**. Most entries assert their overhead is negligible; this one decomposes it and shows
the sharing ratio that makes it so.

## 4. Results

| | |
|---|---|
| Baseline | **NVIDIA A100 80 GB (2 TB/s)**, with **all baseline accelerators normalized to match it in peak throughput and memory bandwidth**. KV baselines: KIVI, GEAR, KVQuant, PALU, ReCalKV, ZipCache |
| Models / datasets | DeepSeek-R1-Distill-Qwen-1.5B and -LLaMA-8B; CoQA, TruthfulQA, GSM8K, LongBench |
| Accuracy delta | **At 2-bit KV: SingularBit-KV loses 2.0% (CoQA) / 0.5% (TruthfulQA) while KVQuant, PALU and ZipCache fall to 0–30% accuracy.** Weight methods evaluated at 2/3/4-bit |
| Speedup | **Algorithm alone on a GPU: 4.00×** at 3-bit average weight precision + 78.18% KV compression. Accelerator `SingularBit-WKV`: **5.27×**; headline **up to 5.3×** decode-heavy, **up to 9× throughput** on standard workloads |
| Energy / area | **4.64×** energy (WKV); **up to 4.8×** decode-heavy; **79% system energy reduction** on standard workloads. Compressor 21.5 mW / 1.23 mm² of the engine; **< 4% chip-level**, off the critical path |
| Technology node | **28 nm CMOS**, synthesised |
| Evidence level | **RTL synthesis** for the accelerator + **measured A100 execution** for the algorithmic results. No silicon |
| **Is the comparison fair?** | **Iso-resource** — SingularBit and every baseline accelerator normalised to the A100's peak throughput and bandwidth. Overhead decomposed rather than asserted. But the **`U` basis storage is never netted out** of the compression ratios; the headline **mixes regimes** (5.3×/4.8× decode-heavy vs 9×/79% standard); the accuracy claim sits at **2-bit KV where competitors collapse**; **no sensitivity study on `p` or `K`** |

## 5. Comment

## 6. Claude notes

> **Suggestions from the reading agent. Strip this section before copying into
> `QuantArchSurvey/venues/ISCA/notes/`.**

- **§5 material, if you want it — this is the reason the granularity figure needs a second
  dimension.** The axis so far runs along tensor geometry: BitFusion per-layer → DRQ per-region →
  Tender per-channel → Oaken/MicroScopiQ per-group → P3-LLM per-head → LightNobel per-token.
  **SingularBit allocates along rank**, which isn't a point on that line — it's a different line.
- **With SmartExchange it makes the corpus's decomposition-based pair, and they differ
  instructively.** SmartExchange factors `W = B·Ce` with a **learned** basis and sparse
  power-of-two coefficients; SingularBit uses **SVD**, an **analytic** basis, and quantizes within
  it rather than truncating. Learned-vs-analytic basis is the distinction — and both then owe the
  same answer: what do the factors cost to store?
- **It's the only entry using two importance axes at once** (token importance × rank significance
  for KV). On the outlier-selection lineage — OLAccel by magnitude, DRQ by spatial predictor,
  MicroScopiQ by Hessian, LightNobel by runtime top-k — SingularBit selects by **singular value
  magnitude**, a *basis-level* rather than *per-element* importance.
- **Best case in the corpus for analytical rather than searched hyperparameters.** DRQ retrains in
  a trial-and-error halving loop, Ecco sweeps S and H, LightNobel leaves `k` unspecified.
  SingularBit gives a closed form for average precision and says so explicitly. Worth citing
  wherever the survey discusses the deployment cost of quantization hyperparameters — though note
  the irony that `p` and `K` themselves get no sensitivity study.
- **KV compression is still unsettled, and this is the evidence.** Four ISCA entries, four unrelated
  mechanisms for the same tensor: Oaken splits by magnitude into outer/inner outliers, P3-LLM
  smooths per-channel then quantizes per-head, Ecco compresses entropically, SingularBit decomposes
  and allocates by rank. Worth one sentence.
- **The gap I'd want closed before citing a compression ratio:** the **`U` basis storage isn't netted
  out**. An SVD scheme's effective bitwidth has to include its factors, and "78.18% KV compression"
  reads as if it does not.
- **`SVD` in the data-type cell sits oddly** in a bitwidth-preferring column — it names the *basis*,
  not a numeric format. The bitwidths (`INT1` `INT2` `MIXED`) are the format; I'd keep `SVD` but
  footnote it, same issue as `ADAPTIVE` elsewhere. **Note the contrast with SmartExchange**, whose
  seed row also carried `SVD` — there it was simply wrong (the word never appears in that paper) and
  I've removed it. Here the SVD is real, which is exactly why the two rows shouldn't have looked
  alike.
- Checked against your `SYS` rule: no compiler or ISA contribution, so `ALGO+ARCH` as seeded.
