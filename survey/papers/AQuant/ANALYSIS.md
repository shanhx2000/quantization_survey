# AQuant — paper notes

**AQuant: Repurposing CODEC for VLM Acceleration via Adaptive Quantization**
Zhuoran Song, Chunyu Qi, Jian Weng, Xiaoyao Liang, Haibing Guan
**ISCA 2026** (2026 ACM/IEEE 53rd Annual International Symposium on Computer Architecture),
pp. 1417–1431 ｜ DOI: **10.1109/ISCA66397.2026.00106**
Publication info verified 2026-09-02 from the **official ISCA 2026 proceedings package**
(title, authors, pages, DOI and abstract all read from its `assets/data/data.js`).
Archived here: **the published proceedings PDF** (`506501b417.pdf`, 15 pages) — not a preprint.

Status: **note ready** ｜ Last updated: 2026-09-14
Tags: `combined-dtype` `mixed-precision` `dtype-granularity` `accelerator`
How far it was read: **close read of the whole body — §I–§VII, all fifteen pages of
`extracted/506501b417.pages/`.** Read line by line: §I, §II-A/B/C (H.265 background and the CMC /
LLM.265 comparison), §III-A/B/C/D (the algorithm), §IV-A/B/C (the microarchitecture), §V-A/B/C/D
(all of the evaluation, including the design-exploration subsection), §VI, §VII, Tables I–III.
**Skimmed:** the reference list (52 entries, checked only for the OpenASIC / Scale-Sim / Ramulator /
CACTI tool citations and the CMC / LLM.265 / OliVe / VisPruner baselines).
**Read from figure text only, and therefore weak:** every bar chart (Figs. 12–23) is a rasterised
plot whose axis labels survive extraction but whose *bar values do not*. Every per-benchmark number
below therefore comes from the prose, not from the figure. **Not resolved** (itemised in
`Limitations and open questions`): the definition of "exponent" that makes the claimed [0, 8] range
consistent with Fig. 3; where the INT8 base-token GEMM executes, given that the NPU contains only
INT2 and INT4 MAC arrays; the incremental area of the CODEC modifications as distinct from the
CODEC's pre-existing area; the scale granularity of the delta quantizer; and the arithmetic behind
"7.4% INT8 bases" and "2.16× compute reduction".
The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> The PDF is **not committed** (3.3 MB). It came from the proceedings package a human
> supplied, now archived at [`archieve/ISCA 2026.zip`](../../../archieve/), entry `pdfs/5065-3nexm57sBmVa6MJtFTiSrb/506501b417/506501b417.pdf`.
> **There is no public URL for it** — this is not an arXiv paper. Re-extract with
> `python3 extract.py` → `extracted/` (committed, greppable).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, 2026 row.

---

## Brief

**What the close read changed** (one line, per the reading protocol): the brief was right about the
mechanism but wrong about the accounting — the abstract's "6.9× over Xavier AGX GPU" is against a
GPU *analytically shrunk* to AQuant's compute budget (the measured Xavier is **2.1×**), and the
"almost nothing" cost of reusing the CODEC is an area argument that charges **zero** for the new PE,
reconfigurable PE array, reconfigurable comparator tree, fp-to-int unit and top-k/QuickSelect unit
the paper itself says it added. Everything else in the brief stands.

### 1. Motivation

Vision-language model cost scales with image resolution and frame count, which blocks real-
time use. Two things prior quantization accelerators miss: **visual tokens are highly
similar to each other** (unlike LLM tokens), and the floating-point units used to convert
FP→INT are themselves expensive — quantization only applies to linear layers, yet precision-
critical non-linear ops (GELU, Softmax, LayerNorm) keep forcing casts back and forth.

### 2. Overview

Exploit the similarity by quantizing **deltas** between similar visual tokens rather than
the tokens themselves — a narrower distribution, so INT4/INT2 delta GEMM suffices. To avoid
paying for floating-point similarity detection, use **exponent-based** similarity detection.
Then the structural move: **repurpose the video CODEC already present in the SoC** to
perform similarity detection and adaptive quantization, paired with a mixed-precision NPU.

### 3. Pros and cons

**Pros**

- Reusing an idle on-chip CODEC is the kind of systems insight that costs almost nothing and
is easy to overlook — the hardware is already there in real SoCs. *(Close read: the insight is
real; the "costs almost nothing" is the paper's own accounting and is not audited — see
`Cost and requirements`.)*
- Delta quantization is well matched to the data: visual-token similarity is a property of
the modality, and the narrower delta distribution is what makes INT2 viable. **verified** (Fig. 3,
p. 1418: 46% of visual-token values in [-0.3, 0.3] against 74% of delta values).
- Exponent-based detection removes exactly the FP overhead identified in the motivation;
4.5×/2.8×/6.9× speedups over LLM.265, CMC and an Xavier AGX GPU at negligible accuracy
loss. *(Close read: the body says **4.6×** for LLM.265, not 4.5×, and the 6.9× GPU number is not
the measured Xavier — see `Key numbers`.)*
- The one honest-scarcity number in the paper: **quantization + dequantization = 5.1% of
inference latency, KV-cache dequantization 2.3%**, and both are pipelined against the MAC arrays
so they are hidden. **verified** (§V-D, p. 1428). The paper does not hide its reconstruction cost.

**Cons**

- The whole premise depends on **visual** token similarity — it does not transfer to LLM
decoding, and the paper says so.
- Assumes a CODEC is present and available; on hardware without one, or where it is busy
with actual video, the argument weakens. *(The paper does measure this: AQuant-Decoding, §V-C,
p. 1426 — video decode is 8.3% of end-to-end time and the speedup falls 6.9× → 6.8×.)*
- Delta computation introduces a dependency between tokens, so the reported stalls and
synchronization in the pipeline are intrinsic rather than incidental.
- **New from the close read:** the area argument that carries the CODEC contribution (1.4× of the
7.4× total, §V-C Fig. 17) double-counts. The same 0.26 mm² is described as "these modifications
occupy 0.26 mm²" (p. 1427) *and* as the pre-existing CODEC whose area is free (p. 1427). Both
cannot be true.

### 4. Where it applies

The **VLM** entry, and the corpus's most creative instance of a **combined/residual data
type** (value = reference + delta). Compare with [`SingularBit`](../SingularBit/ANALYSIS.md)
and [`SmartExchange`](../SmartExchange/ANALYSIS.md), which decompose in different bases for
the same reason, and with [`JPEG-ACT`](../JPEG-ACT/ANALYSIS.md), which borrows a *codec
algorithm* where AQuant borrows *codec silicon*.

---

## Method

**The identity.** Every visual token is written `T ≈ B + δ`, where `B` is one of `M` **base
tokens** drawn from the token sequence itself and `δ = T − B` is the residual. Because the ViT
encoder is (the paper argues) a homomorphism from pixels to tokens, spatially/temporally similar
pixels give similar tokens, so `δ` has a much narrower distribution than `T` and survives 2–4 bits.
**verified** (§II-A p. 1418, §III-A p. 1420).

**Step 1 — base-token selection.** `M` candidates are chosen *positionally, not by content*: for
every `F` consecutive tokens (`F = ⌊N/M⌋`), the **middle** token is taken. `F = 18` is the chosen
operating point. **verified** (§III-A p. 1420; §V-D p. 1428). This is a striking simplification —
no clustering, no k-means, no importance measure; the "codebook" is a fixed positional stride.

**Step 2 — exponent-only similarity detection (the paper's real trick).** Rather than an FP32 L1
distance `D_{i,j} = Σ_k |T^i_k − T^j_k|`, AQuant computes

> `D̄_{i,j} = Σ_k | sign(T^i_k)·2^{Ē^i_k} − sign(T^j_k)·2^{Ē^j_k} |`

where `Ē` is the IEEE-754 exponent field. Each operand becomes `sign ‖ (1 << exponent)`, a **10-bit
integer** (9 bits for `2^exp ∈ [1, 256]` plus sign), and the distance is an integer
subtract-and-abs reduction — exactly the operation the H.265 motion-estimation PE already performs
on INT8 pixels. **verified** (§III-A p. 1421, §IV-A p. 1422). The `argmin` over the `M` candidates
gives each token its base; the `(T^i, T^j)` pairs are written into a **similar token table**.

**Step 3 — adaptive (per-row top-p) precision assignment.** Within each delta vector `δ^i`, the
**top `p` = 25% of elements by magnitude go to INT4** and the remaining 75% to **INT2**; the split
is recorded as a bitmask and materialises as **two mutually complementary sparse matrices**.
Base tokens themselves are kept at **INT8**. **verified** (§III-B p. 1421, §V-B p. 1424).
The choice of a *per-row* (per-token) ratio is not an accuracy decision — it is a **load-balancing**
decision: it guarantees every MAC line of the high-precision array and every MAC line of the
low-precision array retire the same number of elements, so the two arrays run in lockstep and
neither stalls (§IV-B p. 1423, Fig. 11).

**Step 4 — result reconstruction.** `W_q T = W_q B + W_q δ`. `W_q B` is computed **once** for the
`M` base tokens at INT8 and then *selected*, not recomputed, for every token that shares that base;
`W_q δ` runs on the two low-precision arrays. A dedicated reconstruction engine (three SRAMs: base
16 KB, delta 8 KB, recovery 16 KB; INT16 entries) walks the similar-token table and adds the two.
**verified** (§III-C p. 1422, §IV-C p. 1424).

**Step 5 — decoding.** After the KV projection the KV-cache is **re-quantized rather than written
back reconstructed**, stored compressed off-chip, and reconstructed on demand. This is the only
mechanism by which AQuant helps the memory-bound decode phase; the paper describes it as trading
compute for bandwidth. **verified** (§III-D p. 1422).

**What is reused versus what is added — the whole area argument turns on this.**

| CODEC block | Reused as-is | Modified / added |
|---|---|---|
| ME 8×8 PE array | the 64-wide **subtract-and-abs reduction tree** per PE | the **subtractor front-end is replaced** ("Augmented Subtractor"): exponent extract, `<<`, sign concat, **INT10** instead of INT8 in / INT16 accumulate |
| ME PE array partitioning | the 8×8 mesh itself | made **reconfigurable at 4×4 block granularity**, `⌈M/16⌉` blocks merged per logical group — new control logic |
| ME comparator reduction tree | the tree structure | made **reconfigurable**: 4-stage basic unit + composable 2-stage tree |
| ME output | motion-vector generation engine | new **similar token table** |
| Quantization unit (Fig. 5b) | the **multiplier, adder, shifter and clamper** of the affine datapath | mantissa **clamped 23 → 16 bits**; **XOR** gate for the sign; **fp-to-int unit** (2×2:1 mux + 7:1 mux + 32:1 mux + AND + 16 registers); **top-k unit** (QuickSelect: 3 FIFOs, 4 comparator groups, OR, XOR, 2:1 mux); bitmask generation |
| — | — | **entirely new**: the NPU's two MAC arrays, the result accumulation engine, the result reconstruction engine, the bitmask buffer, the on-chip buffers |

**verified** (§IV-A pp. 1422–1423, §V-C p. 1427). The reused part is the *arithmetic skeleton*
(subtract-abs trees, comparator trees, one multiplier-adder-shifter-clamper chain). Everything that
touches floating point, everything that selects, and the entire compute engine are new. The paper
**never reports the incremental area of the additions** — only the 0.26 mm² total of the
post-modification ME + quantization modules.

## Key numbers, with their frame

Unless stated otherwise: LLaVA / VideoLLaVA / Qwen2.5-VL-72B across fourteen datasets;
`p` = 25%, `F` = 18; deltas INT4/INT2, bases INT8, **weights INT16**; AQuant synthesised at
**28 nm, 500 MHz**; performance from a **custom cycle-level simulator** (validated against
Scale-Sim) + **Ramulator** DRAM + **CACTI** buffers + modified **OpenASIC** H.265 encoder IP for
the CODEC; LPDDR4x 32 GB / 136.5 GB/s, matched to Jetson AGX Xavier.

| Setting | Model | Metric | Baseline | Result | Source |
|---|---|---|---|---|---|
| **Headline speedup, abstract** | 3 VLMs, 14 datasets | end-to-end speedup | LLM.265 / CMC / "Xavier AGX GPU" | **4.5× / 2.8× / 6.9×** | Abstract, p. 1417. **verified**. *The body says 4.6× for LLM.265 and the 6.9× is against `GPU-Full`, not the measured Xavier* |
| **Speedup vs GPU family** | same | end-to-end speedup, simulator | `GPU-Full` (Xavier analytically rescaled to AQuant's compute-unit count) / `GPU-Full-unscale` (**measured** PyTorch on Jetson AGX Xavier) / `GPU-Mixed-precision` (hypothetical, *optimistic analytical upper bound*) | **6.9× / 2.1× / 2.2×** | §V-C p. 1425, Fig. 14. **verified**. **The only measured-hardware comparison in the paper is the 2.1×** |
| **Speedup vs accelerators** | same | end-to-end speedup, simulator | GPU-VisPruner / OliVe / LLM.265 / CMC — all three accelerators **re-implemented by the authors** as cycle-accurate simulators, not quoted | **2.8× / 2.5× / 4.6× / 2.8×** | §V-C p. 1425, Fig. 14. **verified** |
| **Composed with token pruning** | same | speedup | GPU-Full | **8.3×** (AQuant + VisPruner) | §V-C p. 1425. **verified** |
| **Composed with CMC** | same | speedup | CMC | **+3.4×** over CMC | §V-C p. 1425. **verified** |
| **CODEC busy with real video** | VideoLLaVA, Qwen2.5-VL | speedup with decode latency added in | GPU-Full | **6.8×** (vs 6.9×); video decode = **8.3%** of end-to-end time | §V-C p. 1426. **verified**. Does not apply to LLaVA (still images) |
| **Algorithm on a GPU** | same | speedup | GPU-Full | **0.843×** — GPU-AQuant is **15.7% slower** than the unmodified GPU | §V-C p. 1426. **verified**. INT2 must be padded to INT4 and INT4×INT16 decomposes into four INT4×INT4 kernels |
| **Accuracy** | 3 VLMs × 14 datasets | avg accuracy drop | FP baseline model | **−0.7%** | §V-B p. 1425, Fig. 13. **verified** (prose; per-dataset bars not extractable) |
| **Ablation — is INT2 needed?** | same | avg accuracy drop | FP baseline | **−23%** if the bottom 75% of deltas are *pruned* instead of kept at INT2 | §V-B p. 1425. **verified**. Strong evidence the low-magnitude deltas carry real signal |
| **Robustness — fast motion** | VideoLLaVA, fast-motion subset | accuracy loss at fixed `F` = 18 | FP baseline | **−0.83%** | §V-D p. 1429, Fig. 22. **verified** |
| **Robustness — low similarity** | bucketed by inter-frame L1 distance | accuracy loss in the [350, 400) bucket | FP baseline | **−0.92%** | §V-D p. 1429, Fig. 23. **verified** |
| **Threshold sensitivity** | VideoLLaVA-MSVD | accuracy drop at `p` = 20% | FP baseline | **−2.1%**, called "unacceptable"; `p` = 25% chosen | §V-B p. 1424, Fig. 12. **verified** |
| **Theoretical compute saving** | — | analytical, activation bitwidth only | **full INT8 model** | **3.2×** = 8 / (4×0.25 + 2×0.75) | §V-C p. 1425. **verified as arithmetic**; ignores the 7.4% INT8 bases, the INT16 weights, and reconstruction |
| **Compute reduction vs pruning** | — | analytical | VisPruner (prunes 61.1% of tokens, rest in **FP16**) | **2.16×** | §V-C p. 1425. **verified as stated**; **inferred / not verified** as arithmetic — I get ≈2.0× from the stated 38.9% FP16 residue vs (75% INT2 + 25% INT4 + 7.4% INT8) |
| **Area, whole design** | — | post-synthesis, 28 nm | — | **1.858 mm²** total: NPU low-prec MAC 0.476 + high-prec MAC 0.238 + reconstruction 0.183 + on-chip buffer 0.675; enhanced CODEC ME 0.138 + quant 0.122 + buffer 0.026 | Table III p. 1427. **verified** (sum computed by me; the paper prints no total) |
| **Power, whole design** | — | post-synthesis, 28 nm | — | **510.5 mW** (164.8 + 82.4 + 9.3 + 197.4 + 23.4 + 21.3 + 11.9) | Table III p. 1427. **verified** (sum computed by me) |
| **Claimed CODEC area saving** | — | analytical | a hypothetical AQuant with no CODEC, spending 0.26 of its 0.714 mm² MAC budget on similarity + quantization logic | **36%** (0.26 / 0.714), worth **1.4×** performance | §V-C p. 1427, Fig. 17. **verified as stated**; the *premise* is disputed — see `Cost and requirements` |
| **Contribution decomposition** | — | speedup, cumulative | AQuant-plain (INT8 VLM, no optimization) | algorithm **3.3×** → + exponent detection **1.6×** → + CODEC reuse **1.4×** ⇒ **≈7.4× compounded** | §V-C p. 1427, Fig. 17. **verified** (3.3 × 1.6 × 1.4 = 7.39, product computed by me) |
| **Motivating cost of naive FP** | — | post-synthesis area/power | a 64×64-INT8 systolic array (1.672 mm², 560.4 mW) | FP32 similarity-detect + quantize = **1.269 mm², 422.7 mW** = **43%** of the two blocks combined | Table I p. 1420, text p. 1421. **verified**. NB "43% of the on-chip area" counts **only those two blocks**, and the 64×64 array is **not** the array AQuant actually builds (it builds 5×32×32) |
| **Energy efficiency** | 3 VLMs, 14 datasets | improvement | GPU-Full / GPU-Full-unscale / GPU-Mixed-prec / GPU-AQuant / GPU-VisPruner / LLM.265 / CMC / OliVe | **7.2× / 2.2× / 2.3× / 8.6× / 2.9× / 14.0× / 2.5× / 2.1×** | §V-C p. 1427, Fig. 18. **verified** |
| **Why LLM.265's energy is so bad** | — | reported by AQuant about LLM.265 | LPDDR4X load energy | LLM.265 costs **97.8 / 63.5 pJ/bit** compress/decompress — *higher than simply loading from LPDDR4X* | §V-C p. 1427. **verified as AQuant's claim**; not independently checked. **Citation hazard** — this is a re-implementation's number about someone else's design |
| **Quant/dequant overhead** | all benchmarks | fraction of inference latency | — | quantization **5.1%**, dequantization **5.1%**, KV-cache dequant during decode **2.3%** — all pipeline-hidden | §V-D p. 1428, Fig. 20(a). **verified as stated**; the sentence "both account for 5.1%" is ambiguous between *each* and *together* |
| **Cycle breakdown** | — | fraction of MAC-array time | high/low-precision MAC arrays | ME 47.8%, quantization module 24.3%, reconstruction engine 7.8% — all hidden by pipelining | §V-C p. 1426, Fig. 15. **verified** |
| **Where the time is** | all benchmarks | latency share | — | visual tokens = **95.8%** of total latency; AQuant cuts that portion by **85.7%** | §V-D p. 1428, Fig. 20(b). **verified** |
| **Exponent range** | LLaVA + Qwen2.5-VL, slow/fast motion | cumulative exponent distribution | — | **>99.7%** in [0, 7], **1.2%** in [7, 8] (the two overlap — sloppy) | §V-D p. 1428, Fig. 19. **verified as stated**; the *definition* of "exponent" is **not resolved** — see below |
| **Base-token fraction** | — | share of tokens kept at INT8 | — | **7.4%** at `F` = 18 | §V-D p. 1428. **verified as stated**; **not reproducible** — `F = ⌊N/M⌋` gives 1/18 = 5.6% |

## Cost and requirements

**Data type, in field notation.** Activations only. Per linear layer:
`A8` for the ~7.4% of tokens acting as bases, `A4` for the top 25% of each delta vector, `A2` for
the remaining 75%. **Weights are `W16`** — the NPU is built from `INT2×INT16` and `INT4×INT16`
MACs (Table III p. 1427; §V-C p. 1426 says "the matrix multiplications in AQuant involve
INT4×INT16 multiplications"). **AQuant does not quantize weights at all** and says so: it is
"orthogonal to the existing static weight quantization" (§III p. 1420, citing OliVe). So the honest
label is **W16 A2/A4 + A8 bases**, and the effective activation bitwidth is
`0.25×4 + 0.75×2 + 0.074×8 ≈ 3.1 bits` — but against **16-bit weights**, so the *product* is not a
low-bit GEMM in the sense most of this corpus means. **verified**.

**Scale granularity: never stated.** The quantizer is the CODEC's affine
`Clamp((Res/Factor) + Offset) >> b` with an FP `Scaling Factor` input (Figs. 5b, 10b). The paper
gives no granularity for `Factor` — not per-tensor, not per-token, not per-group. The only
per-something in the algorithm is the **precision assignment**, which is per-row (per-token
top-`p`). Recording this as a gap rather than guessing. **not stated in the paper**.

**Accumulator.** Not reported as a datapath width. What is reported: the reused ME reduction tree
accumulates 64 INT8 pixels in **16 bits** (§II-B p. 1419); the reconstruction engine's three buffers
store **INT16** outputs (§IV-C p. 1424). The MAC arrays' partial-sum width is never given, and the
area in Table III therefore cannot be checked against an accumulator assumption. **not stated**.

**Outlier mechanism: exponent-range fallback, at token granularity.** "Tokens with exponents
outside this range [0, 8] are treated as outliers, bypass similarity detection, and are directly
processed using higher precision" (§V-D p. 1428). **verified**. Three things are missing: the
precision they fall back to, the measured frequency of the fallback, and its performance cost. This
is the paper's only outlier path and it is one sentence long.

**Escape hatches** (the things that stay wide):
1. **Weights, INT16** — never quantized.
2. **Base tokens, INT8** — 7.4% of tokens.
3. **All non-linear ops in FP** — GELU/Softmax/LayerNorm consume FP activations reconstructed and
   dequantized by the CODEC after every linear layer (Fig. 1b p. 1417; §V-D p. 1428 prices this at
   5.1% of latency).
4. **Reconstruction in INT16** — every token's output is `base_result + delta_result` in INT16.
5. **Out-of-range-exponent tokens** — bypass the whole path.

**Retraining: PTQ, but not calibration-free.** "The AQuant algorithm does not require retraining"
— and then, in the same paragraph, "the required calibration data for threshold selection is **10%
of the training dataset**" (§V-B p. 1424). **verified.** 10% of a VLM's training set is an enormous
calibration budget by this corpus's standards (Tender: 128 Pile samples; P3-LLM: calibration-free).
It is used to pick `p` and `F`, which are then **fixed across all fourteen datasets** and, per
§V-D p. 1429, tuned on a single benchmark (VideoLLaVA-MSVD) and reused — so in practice the
calibration is two scalars, and the "10%" claim reads as over-stated rather than as a real
deployment obstacle. Worth flagging both ways.

**The area argument, audited.** Total 1.858 mm² @ 28 nm, of which the CODEC-derived part is
0.286 mm² (15.4%) and the NPU + buffers + reconstruction is 1.572 mm² (84.6%). The paper's
1.4× CODEC contribution rests on this chain (§V-C p. 1427):

> MACs = 0.476 + 0.238 = 0.714 mm². Repurposed CODEC = 0.138 + 0.122 = 0.26 mm². Without the
> CODEC you would carve 0.26 out of 0.714, leaving 0.454 mm² for MACs. Therefore reusing the
> CODEC "achieves a 36% area saving", which buys 1.4× performance.

The step that does not hold is that **0.26 mm² is the area of the *enhanced* ME and quantization
modules, not of the stock H.265 blocks**. The paper says so itself two sentences earlier: "we
enhance the functionality of the existing ME module by designing a new PE, a reconfigurable PE
array, a reconfigurable comparator tree, and associated control logic. Additionally, we extend the
capabilities of the quantization module. **These modifications occupy 0.26 mm² of area.**" The same
0.26 mm² is used once as *the cost of the additions* and once as *the free pre-existing hardware*.
Since they modelled the CODEC with a real open-source H.265 encoder IP (OpenASIC), the stock-vs-
enhanced delta was available to them and is not reported. **This is the single most important
unverified claim in the paper**, because the CODEC-reuse contribution is exactly the 1.4× that the
title is about. **verified that the paper says both things; the resolution is not in the paper.**

**Platform requirements.** An SoC with an H.265-class encoder whose ME PE array and residual
quantizer can be re-wired (not merely re-driven); the CODEC idle during inference, or a willingness
to lose 8.3% of end-to-end time; a mixed-precision NPU with separate INT2 and INT4 arrays sized at
the fixed 4:1 ratio that `p` = 25% implies (Table III: 4×(32×32) INT2 vs 1×(32×32) INT4). **Changing
`p` at runtime is not possible** — the MAC array ratio is hardwired to it.

## Limitations and open questions

Ordered by how much they would change a citation.

1. **The exponent range [0, 8] cannot be reconciled with the paper's own Fig. 3.** §IV-A (p. 1422)
   argues that `2^exponent ∈ [1, 256]`, so 9 bits + sign = INT10 suffices. That requires
   `exponent ≥ 0`, i.e. `|value| ≥ 1`. But Fig. 3(a) (p. 1418) reports that **46% of visual-token
   values lie in [-0.3, 0.3]**, whose exponents are ≤ −2. Under a plain IEEE-754 reading the two
   statements contradict each other; some unstated normalisation, clamp or offset must be in play
   (clamping negative exponents to 0 would work, and would collapse all sub-unit magnitudes to the
   same approximate magnitude — which is arguably fine for an L1 *ranking* but is never said).
   **Not resolved. Verify before citing the INT10 width or the [0, 8] range.**
2. **Where does the INT8 base GEMM run?** §III-B says the `M` base tokens are "multiplied by the
   weight matrix `W_q` for high-precision GEMM", but Table III's NPU contains only INT2×INT16 and
   INT4×INT16 arrays. No INT8 datapath is described, budgeted or timed. **Not resolved.**
3. **The incremental CODEC area is never reported** (see above). Consequence: the 1.4× and the
   "36% area saving" should be treated as upper bounds.
4. **The 7.4% INT8 base fraction does not follow from `F = 18`.** `F = ⌊N/M⌋` gives `M/N = 1/18 =
   5.6%`. Neither the PE-array rounding (`⌈M/16⌉` blocks) nor any stated averaging closes the gap.
   **Not resolved.** Affects the effective-bitwidth arithmetic.
5. **Scale granularity is never stated** — see `Cost and requirements`. For a paper whose whole
   claim is dynamic runtime quantization, this is the missing number.
6. **`p` is baked into the silicon.** The 4:1 MAC-array ratio is chosen for `p` = 25%. A model or
   input that wants `p` = 35% (Fig. 12 shows some benchmarks improving up to 40%) runs the
   high-precision array as the bottleneck. The paper presents the workload balance as a feature and
   never discusses the rigidity it implies.
7. **Extension to FFN and attention is asserted, not shown.** "The same procedure can be extended to
   other linear layers by applying to the right matrix" (§III-A p. 1420). But *visual-token
   similarity* is a property of the ViT output; the FFN's inputs are post-attention hidden states,
   and no evidence is offered that similarity survives depth. Every distribution and similarity plot
   in the paper (Figs. 2, 3, 19, 23) is of **input** visual tokens.
8. **Decode-stage KV-cache handling is under-specified.** The KV-cache is re-quantized after the KV
   projection and reconstructed on demand, but no KV bitwidth is given, and the tokens *generated*
   during decoding are language tokens, whose lack of similarity is the paper's own motivating
   observation (Fig. 2). What happens to their KV entries is not said.
9. **The outlier fallback is one sentence** — no precision, no measured rate, no cost.
10. **Baselines get no stated area budget.** The GPU comparisons are constructed with care and
    disclosed; CMC, LLM.265 and OliVe are re-implemented but the paper never says they were sized to
    AQuant's 1.858 mm², nor at what node. Contrast Tender and MicroScopiQ, which state their iso-area
    and iso-node construction explicitly.
11. **Fig. 13's baseline is the FP model; Fig. 12's "3.2×" baseline is the INT8 model.** Two
    different baselines in adjacent subsections. Not an error, but a trap for anyone quoting
    "0.7% loss for 3.2× saving" as one sentence.

## Relation to other entries

**A new axis this paper opens: *borrowed silicon*.** The corpus already has the "compression vs
cheaper arithmetic" axis ([`Ecco`](../Ecco/ANALYSIS.md) buys bandwidth, not arithmetic). AQuant adds
a second question — **whose transistors?**

- [`JPEG-ACT`](../JPEG-ACT/ANALYSIS.md) (ISCA'20) borrows the **JPEG algorithm** (DCT-style
  transform coding) and builds new hardware for it in the GPU memory path.
- **AQuant borrows the H.265 encoder's actual silicon** — ME subtract-and-abs trees, comparator
  trees, and the residual quantizer's multiplier/adder/shifter/clamper.
- Between them sit CMC and LLM.265, AQuant's own baselines, which use the CODEC as a black box
  (CMC for integer-domain similarity detection to *prune* tokens; LLM.265 to compress weights and
  KV-cache through the standard coding pipeline). AQuant's differentiator, stated at §II-C p. 1420,
  is that it goes *inside* the CODEC to make an integer-native datapath consume floating point.

**Outlier currency.** The corpus's ledger — extra bits (OLAccel, Oaken), a destroyed neighbour
([`OliVe`](../OliVe/ANALYSIS.md), [`MicroScopiQ`](../MicroScopiQ/ANALYSIS.md)), a second datapath
(OASIS), compressibility itself ([`Ecco`](../Ecco/ANALYSIS.md)), a runtime top-k budget
([`LightNobel`](../LightNobel/ANALYSIS.md)), sign balance in a crossbar column (RAELLA). **AQuant
pays with a reference vector**: the outlier is not encoded at all, it is *subtracted away*. If a
token is unlike its neighbours the mechanism does not isolate it, it simply produces a large delta
that lands in the INT4 quarter. The exponent-range fallback is a second, much weaker path. This is
the only entry in the corpus where the outlier is handled by **changing the origin** rather than
changing the encoding.

**Granularity.** The corpus's ladder is per-layer (BitFusion, OLAccel) → per-region
([`DRQ`](../DRQ/ANALYSIS.md)) → per-channel ([`Tender`](../Tender/ANALYSIS.md)) → per-group (Oaken,
MicroScopiQ) → per-head (P3-LLM) → per-token ([`LightNobel`](../LightNobel/ANALYSIS.md)) →
per-rank ([`SingularBit`](../SingularBit/ANALYSIS.md)). **AQuant is per-element-within-a-token**:
the top-`p` mask is computed inside each delta vector, so the precision decision is finer than
per-token. But note the reason — LightNobel chose per-token because attention *computes* token-wise;
AQuant chose per-element-within-token because that is what makes the two MAC arrays balance. **In
both cases the granularity is selected by the dataflow, not by the data.** That is a survey
sentence.

**Static vs dynamic.** OLAccel identifies outliers at design time, DRQ at runtime, and the axis
notes that most successors reverted to design-time. AQuant is emphatically **runtime**: base
selection, distance computation, top-`p` masking and scaling all happen per inference on live
activations, which is why it needs dedicated detection hardware at all. It sits with DRQ and
LightNobel on the dynamic side — and like DRQ, it discovers that runtime decisions must be
*load-balanced* or the array stalls. DRQ time-multiplexes four INT4 cycles into an INT8 MAC and
stalls the column; AQuant pre-commits to a fixed `p:q` ratio so no stall can occur. **AQuant is
DRQ's answer to DRQ's problem**, one hardware generation later.

**Base + delta as a decomposition.** [`SmartExchange`](../SmartExchange/ANALYSIS.md) factorises
`W = Ce·B` with a small learned basis; [`SingularBit`](../SingularBit/ANALYSIS.md) decomposes by
SVD and allocates bits per rank; AQuant decomposes `T ≈ B + δ` with the basis drawn **from the data
itself, by positional stride**. All three are "value = reference + correction", and the axis that
separates them is **where the reference comes from and when**: learned offline (SmartExchange),
computed offline by SVD (SingularBit), selected online from the activations themselves (AQuant).
AQuant is the only one whose reference is *free* — it is a token that must be computed anyway.

**Substrate.** The corpus's substrate axis — logic die / DRAM near-memory (P3-LLM, NDPLowBitFP) /
analog ReRAM PIM (RAELLA) — says the scarce resource selects the format. AQuant extends it: the
scarce resource here is **an integer-only datapath you do not own the design of**, and that is what
selects `sign ‖ 2^exp` as the similarity metric. The format is chosen to fit borrowed silicon, not
to fit the data.

---

## For the note

### §1 one-line summary

> Rewrites each visual token as **base + delta** — the base picked by positional stride from the
> tokens themselves — and quantizes only the deltas, **per-token top-25% to INT4 and the rest to
> INT2** against INT8 bases and **INT16 weights**, finding each token's base with an
> **exponent-only L1 distance** (`sign ‖ 2^exp`, a 10-bit integer) so that the entire
> similarity-detect-and-quantize path lands on the H.265 encoder's *existing* motion-estimation
> subtract-and-abs trees and residual quantizer sitting idle in the SoC: **−0.7% accuracy over 3
> VLMs / 14 datasets, 2.1× over a measured Jetson AGX Xavier** (6.9× over the same GPU shrunk to
> AQuant's compute budget), with the CODEC reuse itself worth **1.4×** on an area argument that
> charges nothing for the modifications the paper lists.

### Proposed values on their four axes

| Axis | Proposed | Evidence (one line) |
|---|---|---|
| **Level** | **`ALGO+ARCH`** — seed agrees | Base-delta + exponent-similarity + top-`p` assignment is a real algorithm (implemented in Python on PyTorch, §V-B p. 1424, and evaluated for accuracy independently of hardware); the enhanced CODEC + dual MAC arrays + reconstruction engine is the architecture. **No `SYS`** — grepped: no ISA, no compiler, no runtime, no software-stack figure; the PyTorch integration is an experimental harness, not a shipped stack |
| **Q-oriented** | **`Q-ORIENTED`** — the revision log's `non-Q` → `Q` is **correct** | Apply the test: with plain per-tensor INT8, delta generation buys nothing (deltas would still cost 8 bits), the top-`p` bitmask has nothing to assign, the two-array workload balance has no purpose, and the reused CODEC quantizer has nothing to quantize. Only the base-token *reuse* of `W_q B` would survive, and that is a caching trick, not the paper |
| **Data type** | **`INT2` `INT4` `INT8` `INT16` `MIXED`** — **drop `ADAPTIVE`** | INT2/INT4 deltas and INT8 bases stated verbatim (§V-B p. 1424); INT16 weights from Table III's `INT2×INT16` / `INT4×INT16` MACs (p. 1427) and §V-C p. 1426 — **the weight width is load-bearing and the seed omits it**. On `ADAPTIVE` see the disagreement below |
| **Generation** | **`G3`** — the revision log's `G2` → `G3` is **correct** | Judged by paradigm: the problem is VLM-specific (visual-token similarity, prefill/decode asymmetry, KV-cache traffic), and value = reference + delta is literally a video-*compression* representation, i.e. the format-merging-with-compression signature the taxonomy names for G3. The mixed-precision MAC array alone would read G2; dominant signal wins |
| **Optimization** (free text) | `CODEC reuse` `base-delta quantization` `visual-token similarity` `exponent-only L1 distance` `dynamic activation quantization` `per-row top-k mixed precision` `workload-balanced dual MAC arrays` `activation-only` `KV cache` `VLM` | Seed has three; `workload-balanced` and `activation-only` are the two that change how the paper reads |

### Seed-tag disagreements

1. **Drop `ADAPTIVE`.** `TAXONOMY.md` defines `ADAPTIVE` as *"the numeric type itself is a learned
   or data-dependent design variable (the ANT / MERSIT / Anda line)"*. AQuant's numeric types are
   plain INT2, INT4 and INT8, fixed at synthesis; what is data-dependent is **which of them each
   element gets**, which is exactly what `MIXED` already says. The word "adaptive" comes from the
   paper's title, not from its encoding. **Precedent: the same call was made on
   [`LightNobel`](../LightNobel/ANALYSIS.md)** ("Adaptive describes the selection policy, which
   belongs in Optimization"). Contrast [`OliVe`](../OliVe/ANALYSIS.md), which earns `ADAPTIVE`
   because its abfloat has a *genuinely adaptive exponent bias*.
2. **Add `INT8` and `INT16` to the data type.** The seed's `INT4` `INT2` describes the deltas only
   and hides both escape hatches. A reader scanning the venue list would conclude AQuant is a
   W4A4-class design; it is `W16 A2/A4`, weight-unquantized.
3. **Confirm, do not revisit, `Q` and `G3`** (venue README line 131). Both amendments are right and
   the evidence is above.

### Proposed venue-list row

```
| [ ] | [AQuant: Repurposing CODEC for VLM Acceleration via Adaptive Quantization](https://doi.org/10.1109/ISCA66397.2026.00106) | *close read* | ALGO+ARCH | Q | `INT2` `INT4` `INT8` `INT16` `MIXED` | G3 | `CODEC reuse` `base-delta quantization` `visual-token similarity` `exponent-only L1 distance` `per-row top-k mixed precision` `workload-balanced dual MAC arrays` `activation-only` | Visual tokens rewritten as base + delta and only the delta quantized — **the outlier is subtracted away, not encoded**. Similarity measured on exponents alone (`sign ‖ 2^exp`, INT10) so it runs on the H.265 encoder's existing motion-estimation trees. Weights stay INT16 |
```

### §4 fairness verdict (note version, ≈55 words)

> **Not iso-node** (28 nm synthesis vs a shipping edge GPU, never normalised); baselines
> re-simulated rather than quoted, but no area match stated for CMC/LLM.265/OliVe. **Do not quote
> 6.9× as a Xavier speedup** — that is an analytically shrunk GPU; measured Xavier is **2.1×**, an
> idealised mixed-precision GPU 2.2×. The area argument charges nothing for the CODEC edits the
> paper itself lists.

### §4 fairness — the long form (stays here, not in the note)

**Constructed with more care than most, and unusually candid about its own weak spots — the
problems are in the framing of two numbers, not in the setup.**

- **Baselines re-simulated, not quoted ✓.** "For CMC, LLM.265, and Olive, we reproduce their
  algorithms and try our best to build cycle-accurate simulators" (§V-C p. 1425). That is the right
  discipline and avoids the `Phi`-quotes-`Stellar` hazard. It also means every accelerator number is
  AQuant's reproduction of someone else's design.
- **Iso-memory ✓, explicitly.** LPDDR4x 32 GB / 136.5 GB/s, "the same configuration as the NVIDIA
  Jetson AGX Xavier" (§V-C p. 1425).
- **Iso-node ✗, and never mentioned.** AQuant is synthesised at 28 nm; the Jetson AGX Xavier is a
  commercial part on a much finer node (12 nm — *external fact, not in the paper*). No DeepScale-style
  normalisation is applied in either direction. Compare MicroScopiQ, which puts every design at 7 nm
  via DeepScale and says so.
- **Iso-area ~, GPU side only, and by core count not area.** The paper says `GPU-Full` is "scaled in
  the number of compute cores to match the area budget of AQuant" but then says the scaling is "the
  ratio between the number of GPU cores and the compute units in AQuant" (§V-C p. 1425). Those are
  different quantities and the resulting factor (≈3.3×, back-derived from 6.9 / 2.1) is not stated.
  **The scaling factor is not reproducible from the paper.** For CMC, LLM.265 and OliVe no area
  budget is stated at all.
- **The headline GPU number is the shrunken GPU.** The abstract's "6.9× over ... Xavier AGX GPU"
  (p. 1417) is `GPU-Full`. The measured device is `GPU-Full-unscale`, at **2.1×**. Both are in
  Fig. 14 and Table II labels them honestly (`Measurement: PyTorch on Xavier` vs `Scaled GPU`) —
  the elision is in the abstract, not the evaluation. **The number that must not be quoted as a
  GPU speedup is 6.9×.**
- **`GPU-Mixed-precision` is disclosed as optimistic.** "a hypothetical GPU"; "an optimistic
  analytical upper bound by proportionally scaling throughput"; "assumes ideal mixed-precision
  execution on the GPU without overheads from precision switching or additional control complexity"
  (§V-C p. 1425). Disclosing that the *baseline* is optimistic is better practice than this corpus's
  average, and it makes 2.2× the most defensible number in the paper.
- **Abstract/body mismatch: 4.5× vs 4.6× for LLM.265.** Trivial in size, but it means the abstract
  and Fig. 14 disagree; cite the body.
- **Evidence levels must not be pooled.** Measured (PyTorch on Xavier) → analytically rescaled
  (GPU-Full, GPU-Mixed-precision, GPU-VisPruner) → author-reproduced cycle-accurate simulation
  (CMC, LLM.265, OliVe) → AQuant's own custom cycle-level simulator + Ramulator → post-synthesis
  28 nm area/power (Design Compiler) + CACTI buffers + modified OpenASIC for the CODEC. Five
  distinct kinds of fact appear in one bar chart (Fig. 14).
- **Accuracy is measured on real models and real datasets ✓** — 3 VLMs × 14 datasets in PyTorch,
  no retraining. That half of the evaluation is solid.
- **The self-audit the paper does run, and deserves credit for:** AQuant-Decoding (CODEC busy with
  real video), GPU-AQuant (the algorithm without the hardware is *slower*), AQuant-Pruning (INT2 is
  necessary, not decorative), fast/slow-motion splits, an L1-distance-bucketed accuracy sweep, and
  a quantization/dequantization overhead breakdown. Few papers in this corpus test their own
  premise this hard.
- **The one number whose premise is unaudited: 36% area saving → 1.4×.** See
  `Cost and requirements`.

## Abstract (verbatim, ISCA 2026 proceedings)

> Vision-Language Models (VLMs) have reached the forefront of accuracy in various vision
> understanding tasks. Despite their remarkable success, the computing costs of VLMs scale
> significantly with the high image resolutions or the increasing number of video frames
> that need to be processed, posing substantial challenges for deployment to real-time
> applications. Although specialized quantization accelerators have been developed, they may
> not be the optimal solutions due to their neglect of the inherent data similarity within
> VLMs. Additionally, the use of floating-point units for floating-point to integer
> conversion introduces non-negligible hardware overhead. This paper introduces Adaptive
> Quantization (AQuant), an algorithm-hardware co-design framework that repurposes the CODEC
> to accelerate VLM inference in an end-to-end and unified manner. AQuant leverages the
> inherent similarities in visual tokens, exploiting them for differential value (delta)
> generation, which is well-suited for dynamic quantization due to its narrower
> distribution. To eliminate the expensive floating-point similarity detection, AQuant
> integrates an exponent-based similarity detection operation. On the hardware side, we
> enhance the video CODEC's capabilities to efficiently implement exponent-similarity
> detection and adaptive quantization. The framework also incorporates a Neural Processing
> Unit (NPU) with mixed-precision support, which collaborates closely with the CODEC to
> translate algorithmic savings into real speedup. Experimental results show that AQuant
> achieves speedups of 4.5x, 2.8x, and 6.9x over state-of-the-art accelerators, such as
> LLM.265, CMC, and Xavier AGX GPU, with negligible accuracy loss.
