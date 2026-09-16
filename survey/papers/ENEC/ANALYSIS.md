# ENEC — paper notes

**ENEC: A Lossless AI Model Compression Method Enabling Fast Inference on Ascend NPUs**
Jinwu Yang, Jiaan Wu, Zedong Liu, Xinyang Ma, Hairui Zhao, Yida Gu, Yuanhong Huang, Xingchen
Liu, Wenjing Huang, Zheng Wei, Jing Xing, Yili Ma, Qingyi Zhang, Baoyi An, Zhongzhe Hu,
Shaoteng Liu, Xia Zhu, Jiaxun Lu, Guangming Tan, Dingwen Tao
(ICT/CAS + UCAS, with **six Huawei Technologies co-authors** — the Ascend platform's vendor)
**ISCA 2026** (2026 ACM/IEEE 53rd Annual International Symposium on Computer Architecture),
pp. 1319–1335 ｜ DOI: **10.1109/ISCA66397.2026.00100**
Publication info verified 2026-09-02 from the **official ISCA 2026 proceedings package**
(title, authors, pages, DOI and abstract all read from its `assets/data/data.js`).
Archived here: **the published proceedings PDF** (`506501b319.pdf`, 17 pages) — not a preprint.

Status: **note ready** ｜ Last updated: 2026-09-14 ｜ **Human-checked 2026-09-14** — ruled `Q-ORIENTED`, overriding this file's draft `non-Q`.
Tags: `lossless-compression` `accelerator`
How far it was read: **full close read of §I–§IX and the Artifact Appendix (pp. 1319–1335).**
§III (the five observations), §IV (architecture mismatch + Algorithm 1), §V (all four
optimizations, Algorithm 2, Eqs. 1–4), §VI (all six evaluation subsections, Tables II–VII) and
§VII (generality + architectural implications) read line by line; §II and §VIII skimmed for
background. **Itemised gaps, all load-bearing enough to name:**
- **Fig. 9 (per-model compression/decompression throughput) and Fig. 10 (end-to-end TTFT/TPOT)
  are bitmaps.** `pdftotext` recovers their bar values as an unordered list with no bar-to-label
  mapping. **No number in this file is read off Fig. 9 or Fig. 10** — every throughput figure
  comes from §VI prose, Table VII, or the Artifact Appendix.
- **Fig. 13 (ablation)** values are recovered from the same unordered dump and assigned to
  versions V0–V3 by order plus the prose. Treat as approximate.
- **Fig. 3** (exponent value vs frequency rank) read only via caption + the prose fit
  `Y = −1.00X + 123.00`.
- **Algorithm 2's byte-normalisation loop was read but not hand-traced on an example.** That it
  round-trips bit-exactly is taken from the paper's own bit-identical-reconstruction result, not
  re-derived here.
- **The abstract's "3.43× higher throughput than DietGPU" cannot be sourced to any sentence or
  table in the paper.** It is back-derived below and marked as such. **Verify before citing.**

> The PDF is **not committed** (2.4 MB). It came from the proceedings package a human
> supplied, now archived at [`archieve/ISCA 2026.zip`](../../../archieve/), entry `pdfs/5065-3nexm57sBmVa6MJtFTiSrb/506501b319/506501b319.pdf`.
> **There is no public URL for it** — this is not an arXiv paper. Re-extract with
> `python3 extract.py` → `extracted/` (committed, greppable).
> Artifact (code) is public: `https://github.com/jinwuyang/ENEC_ISCA_AE`, BSD-3 (Appendix C,
> p. 1334) — a second repo `https://github.com/hpdps-group/ENEC` is given in a footnote on p. 1320.
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, 2026 row.

---

## Brief

### 1. Motivation

On Ascend NPUs, weight transfer is the bottleneck — memory access is **78–85% of inference
latency** for Qwen3-32B (Fig. 1a, p. 1319) **verified**, and models that exceed HBM must be
split across CPU and NPU, making CPU→NPU transfer dominant (**nearly 80% of execution time**
for some Falcon layers at batch 4, §VI-C p. 1329) **verified**. Lossless compression would
preserve accuracy exactly, but existing lossless algorithms collapse to very low throughput when
ported to Ascend's SIMD architecture (Fig. 1b, §IV-A) **verified**.

### 2. Overview

A **lossless** compressor for AI model weight *files*, purpose-built for the Ascend NPU's
constraints. It splits each float into sign / exponent / mantissa, **stores sign and mantissa
verbatim, and compresses only the exponent field**; the exponent code is a frequency-rank
**linear remap** followed by a **two-level fixed-length group pack**, byte-aligned by
hierarchical halving bit-packing, with a transpose-based prefix scan (IDD-Scan) to recover
offsets on decompression. All of it is AscendC vector-unit code — **no hardware is built**.

### 3. Pros and cons

**Pros**

- **Lossless, and shown to be** — "all 10 models (across FP32, FP16 and BF16 precisions) achieve
  **bit-identical reconstruction**" (§VI-A p. 1328) **verified**. No accuracy question at all,
  which makes it complementary to, not competing with, every quantization entry in the corpus.
- The optimizations answer a real, itemised architectural mismatch (§IV-A's six numbered
  constraints, p. 1322), and the ablation shows each one paid: V0 → V3 takes compression from
  ~119 to ~388 GB/s and decompression from ~34 to ~219 GB/s (Fig. 13, p. 1331) **verified from
  prose; bar values approximate**.
- **Measured on shipping silicon** (Ascend 910B2, 24 AIC / 48 AIV, CANN 8.2.RC1.alpha002),
  end-to-end inside HuggingFace Transformers, with a public BSD-3 artifact. No simulator, no
  synthesis, no analytical model anywhere in the paper.

**Cons**

- **The compression ratio is the weakest part.** ENEC is **below ZipNN (CPU) and DietGPU::Float
  (GPU) on every one of the ten models** (Table II, p. 1327) **verified** — the paper says so
  itself and calls it "a deliberate trade-off". Its wins are against HANS (the other, closed-
  source Ascend compressor) and nvCOMP's general-purpose modes.
- **Its own GPU port beats it.** ENEC-GPU-V1 on an A800 reaches 419.2 / 421.0 GB/s at CR 1.35 vs
  the NPU's 360.6 / 213.8 at CR 1.35 (Table VII, p. 1331) **verified**. The paper presents this
  as a portability success; it also undercuts "Ascend-optimized" as the source of the gain.
- Vendor-specific in its low-level form, and the gains are largest in the CPU–NPU offload regime;
  if the model fits in HBM the motivation weakens considerably.
- **Modest by construction**: 1.35× on BF16 = 11.85 effective bits per weight. A 4-bit quantizer
  is 4× ahead of it and the paper cannot close that gap without ceasing to be lossless.

### 4. Where it applies

The modern, ML-specific counterpart to
[`IBMCompressionAccelerator`](../IBMCompressionAccelerator/ANALYSIS.md) in the **lossless-
compression** cluster, and the **lossless floor** against which every quantization entry's
compression claim should be read. See `Relation to other entries` for the boundary argument.

---

## Corrections to the brief

The brief was right about the mechanism and the headline numbers. **Six things it did not have,
three of which change what kind of paper this is:**

1. **ENEC compresses the exponent field only.** Sign and mantissa are written through
   uncompressed (Algorithm 1 lines 2, 25, p. 1323; §VI-B "we avoid compressing the mantissa",
   p. 1328) **verified**. The brief said "block-based fixed-length encoding" without saying
   *of what*. This is the single most important fact for placing the paper.
2. **The element format is un-quantized floating point — BF16 / FP16 / FP32 — and the paper
   explicitly refuses INT8 and FP8.** "INT8 and FP8 ... are not the primary focus of this study"
   (§III, p. 1321) **verified**, for three stated reasons, one of which is that quantization
   "constitutes a separate lossy compression step and offers limited additional compressibility
   **beyond the quantization itself**" (p. 1322) **verified**. So the "lossless" claim is
   relative to an **FP16/BF16/FP32 checkpoint**, not to an already-quantized tensor.
3. **It is not entropy coding.** The brief inherited the seed tag `entropy coding`. Every
   occurrence of that phrase in the paper is about what Ascend *cannot* run: "making it
   particularly unsuitable for entropy coding" (§IV-A ①, p. 1322), "renders traditional entropy
   coding and dictionary-based methods impractical" (p. 1322) **verified by grep — 11 hits, none
   describing ENEC's own code**. ENEC's own abstract says **"block-based fixed-length encoding
   scheme"** (p. 1319). The contribution *is* the replacement of variable-length entropy coding
   with a fixed-length code.
4. **"Bit-width quantization" in the title of §V-B is not numeric quantization.** It is the
   two-level fixed-length bit-packing of an integer exponent index; reconstruction is bit-exact.
   The word will mislead anyone scanning the paper. **Do not let it into the survey unqualified.**
5. **The brief's "372 GB/s on BF16, 987× ZipNN, 3.43× DietGPU, 1.12× nvCOMP" pooled three
   different frames.** 372 GB/s and 987× are the **BF16 compression** average (§VI-B, p. 1328);
   1.12× is a **maximum across a 10-model × 6-variant grid** against nvCOMP's *weakest* mode; and
   3.43× has no traceable source. See `Citation hazards`.
6. **The end-to-end 6.3× is TTFT on Falcon-40B against an uncompressed CPU-offload baseline**
   (§VI-C, p. 1329) **verified** — not a general inference speedup, and not against HANS (vs HANS
   it is 1.8×).

---

## Conclusions

**ENEC is a lossless compressor for un-quantized floating-point weights, and its whole method
lives in the exponent field.** Observation 1 (§III, p. 1322) is the premise: in BF16 DeepSeek
weights, sign and mantissa have **7.97 bits of entropy** and are effectively incompressible,
while the 8-bit exponent has **2.58 bits**. So ENEC splits the float, ships sign+mantissa raw,
and spends all its engineering on turning the exponent into as few bits as a branch-free SIMD
machine can manage. The result is **11.85 bits per BF16 weight** (1 sign + 7 mantissa + **3.85
exponent**), i.e. **CR 1.35×** — Artifact Appendix, Qwen3-32B, p. 1335 **verified**.

**The interesting engineering is that it is fixed-length.** Entropy coding is the natural answer
to a 2.58-bit-entropy symbol, and the paper ports ANS first and gets ~0.3–1 GB/s (Fig. 1b). The
diagnosis in §IV-A is that Ascend's AIV has no conditional branch, no scatter, and no cheap
variable-length memory handling, so every entropy coder dies on it. ENEC's answer is to
*approximate* the frequency distribution with an **affine map** — Observation 5 says exponent
value versus frequency rank is a straight line, `Y = −1.00X + 123.00` (Fig. 3, p. 1322), so
`y = (2ⁿ − x + b) mod 2ⁿ` (Eq. 2, p. 1326) sends frequent exponents to small integers with three
vector instructions and no table, no gather, no branch — and then to pack those small integers at
a **group-uniform width**: groups of `L = 16`, `m = 3` bits if the group's maximum fits, else
`n = 6`, one mask bit per group. Fixed-length everywhere; the only variable-length object left is
the mask-driven offset, and that is recovered with a prefix sum.

**That prefix sum is the second contribution and it is a pure SIMD-constraint artifact.** AscendC
forbids arithmetic *between elements inside the same 32-byte segment*, and a row of 16 halves is
exactly 32 bytes, so `row[i] += row[i-1]` is illegal. IDD-Scan (§V-D, p. 1326) transposes the
`N×M` tile so intra-row dependencies become inter-row ones, scans columns in `log₂M` steps,
transposes back, then does a second hierarchical scan on a copy to get the row offsets and
broadcasts them. It is the standard decoupled-look-back idea re-expressed entirely in transposes
and broadcasts because those are the only primitives available. Worth **~2× on decompression**
alone (V2 → V3, Fig. 13).

**And nothing about the arithmetic changes.** Compression and decompression run on the **AIV
(vector) units**; the model runs on the **AIC (Cube) unit** — "we construct a collaborative
inference pipeline where compression is handled by the AIV and model operations are executed by
the AIC" (§IV-A ④, p. 1322) **verified**. Decompression is layer-wise and overlapped with the
previous layer's forward pass (§VI, p. 1328) **verified**. The Cube unit multiplies full-width
BF16. **The compute datapath never sees a compressed value, and no value is ever changed.** That
is the sentence that decides where this paper belongs.

---

## Method

**Target.** Model weight tensors, offline-compressed to a file, decompressed on-device at
inference time. Not activations, not the KV cache, not gradients. §VI-C p. 1329 **verified**.

**Step 0 — algorithm selection (§II-C, §III Observation 2).** The authors extended the
open-source **LC framework** [7] and searched it for the best lightweight component combination.
`HCLOG` (grouped bit-packing on leading-zero counts) won on **98.23 / 98.30 / 99.36%** of the
tensor files of DeepSeek-7B / Qwen3-8B / Llama-3.1-8B (Table I, p. 1322) **verified**. ENEC is
HCLOG with the group count generalised and three Ascend-specific optimizations bolted on.

**Step 1 — component separation.** `{E, S, M} ← Split(W)`. Sign and mantissa go straight to the
output stream uncompressed; only `E` continues (Algorithm 1 line 2, p. 1323; Fig. 6 stream
layout, p. 1324) **verified**.

**Step 2 — frequency-rank remap, branch-free (§V-C, p. 1325–26).** The basic design used a gather
into a frequency table `T_freq[E]`, costing **35%** of compression time and **45%** of
decompression time (§IV-B, p. 1323) **verified**. The optimized design replaces it with
`y = (2ⁿ − x + b) mod 2ⁿ` (Eq. 2): a vector subtract of `b`, a negate, and a mask — exploiting
two's complement so negatives wrap into `[2ⁿ, 2ⁿ⁺¹−1]` without a branch. Injective, therefore
lossless; **but it approximates the true frequency order, which costs a little ratio** (§VI-F:
"its linear mapping approximates the frequency distribution, slightly reducing the ratio")
**verified**.

**Step 3 — two-level bit-width "quantization" + hierarchical halving bit-packing (§V-B,
p. 1324–25).** Elements are grouped `L`-wise. If the group's maximum needs ≤ `m` bits, every
element is stored in `m` bits; otherwise every element is stored in `n` bits, `n` = the minimum
width spanning all occurring exponents (Eq. 1). One mask bit per group records which. This turns
a **reduction-max** (40% of compression time in the basic design) into a **bitwise OR**
**verified**. Algorithm 2 then folds pairs of lanes (`data[i] |= data[i+len] << width`),
doubling the effective width each round, splitting off aligned bytes whenever the width crosses 8,
and recursing on the overflow — the byte-normalisation that makes the output 32-byte-alignable.
Physically: **all elements contribute their low `m` bits to the main stream; exceptional groups
additionally contribute their high `n−m` bits to a side buffer**, redistributed on decompression
by an inverse gather and OR-ed back.

**Step 4 — IDD-Scan (§V-D, p. 1326).** Transpose → column-parallel scan in `log₂M` steps →
transpose back → hierarchical row scan on a copy in `log₂N` steps → extract last column, shift to
exclusive, broadcast, add. Replaces the 30%-of-decompression-time prefix sum.

**Step 5 — offline parameter search (§V-E, p. 1326–27).** Histogram the exponents; exhaustively
search `b` over its integer domain with `n` from Eq. 1, minimising `D = Σ p(x)·y` (Eq. 3); then
jointly search `(m, L)` minimising
`B_exp = 1/L + n + (m − n)·p(m)^L` (Eq. 4) **verified**.
Adopted parameters (Table IV, p. 1329) **verified**: BF16 and FP32 all land on
**`(b ≈ 121–125, n = 6, m = 3, L = 16)`**; FP16 on `(7, 4, 3, 16)` and `(11, 5, 3, 16)`.
`L ≥ 16` is forced by Ascend's 32-byte alignment; block size 16,384 elements is forced by the
**192 KB Unified Buffer** (§VI-D, p. 1329) **verified**.

**Where decompression sits.** On the **AIV vector units**, one core-type removed from the **AIC
Cube unit** that runs the GEMMs (§IV-A ④, p. 1322) **verified**. The paper never names the buffer
the decompressed weights land in; since the AIV works out of the Unified Buffer and the AIC pulls
operands through MTE into L1/L0A/L0B (§II-A, p. 1320), **the decompressed BF16 tensor must be
materialised in global memory / L2 before compute** — **inferred / not verified**.

---

## Key numbers, with their frame

Evidence level for the whole table: **measured on shipping silicon** (Ascend 910B2, 24 AIC /
48 AIV, CANN 8.2.RC1.alpha002, driver 25.0.rc1.1, Kunpeng-920 host, Ubuntu 22.04.5) or on a
comparison **NVIDIA A800 + Xeon 8358P, CUDA 12.6** (§VI, p. 1327). **No synthesis, no RTL, no
simulator, no analytical model appears anywhere in the paper** (grepped: `area`, `mm2`, `RTL`,
`synthes`, `simulat` — **zero hits**). Throughput is **msprof kernel time, device-side only,
excluding PCIe transfer** (§VI-B, p. 1328).

| Setting | Model | Metric | Baseline | Result | Source |
|---|---|---|---|---|---|
| **Effective bitwidth, BF16** | Qwen3-32B (32.76 B params) | bits / element | 16 (BF16) | **11.8465** = 1 sign + 7 mantissa + **3.8465 exponent**; 62 487.50 MB → 46 265.99 MB | Artifact Appendix F-1, p. 1335 **verified** |
| Decomposition of the 3.85 exponent bits | Qwen3-32B | `B_exp = 1/L + n + (m−n)p(m)^L` | — | `1/16 + 6 − 3·p(3)^16 = 3.846` ⇒ `p(3)^16 = 0.739` ⇒ **~74% of 16-element groups pack at 3 bits, ~26% at 6** | Eq. 4 p. 1327 + AE p. 1335, arithmetic **inferred / not verified** (consistent to 4 d.p.) |
| **Compression ratio, BF16** | Falcon-7B / Qwen3-8B / DeepSeek-7B / Qwen3-32B / Llama-3.1-8B | CR (whole-model file) | ZipNN 1.51/1.50/1.51/1.50/1.51 · Diet_Float 1.48/1.47/1.48/1.47/1.48 · HANS 1.34/1.34/1.35/1.34/1.33 · NV_Bitcomp 1.33/1.32/1.33/1.32/1.32 | **ENEC 1.36 / 1.36 / 1.37 / 1.35 / 1.36** — **below ZipNN and Diet_Float on all five** | Table II, p. 1327 **verified** |
| **Compression ratio, FP16** | Mistral-7B / SVD-img2vid | CR | ZipNN 1.19 / 1.18 · Diet_Float 1.17 / 1.16 · HANS 1.09 / 1.05 | **ENEC 1.12 / 1.09** | Table II, p. 1327 **verified** |
| **Compression ratio, FP32** | OLMo-1B / BERT-base / Wav2Vec2 | CR | ZipNN 1.20/1.20/1.21 · Diet_Float 1.19/1.19/1.19 · NV_Bitcomp 1.14/1.14/1.15 · HANS 1.14/1.13/1.13 | **ENEC 1.15 / 1.15 / 1.15** — **ties Bitcomp, loses to ZipNN and Diet_Float** | Table II, p. 1327 **verified** |
| Compression throughput, BF16 | 5 BF16 models | GB/s (avg) | ZipNN 0.38 (implied) · NV_Bitcomp 268 (implied) · HANS 274 (implied) | **372 GB/s** = **987× ZipNN**, **1.39× Bitcomp**, **1.36× HANS** | §VI-B prose, p. 1328 **verified** (baseline absolutes back-derived, **inferred**) |
| Compression throughput, FP32 | 3 FP32 models | GB/s | ZipNN · Bitcomp · HANS | **1266× ZipNN, 3.08× Bitcomp, 2.47× HANS**; peak **523 GB/s** | §VI-B, p. 1328 **verified** |
| Compression throughput, FP16 | 2 FP16 models | GB/s (avg) | ZipNN · Bitcomp · HANS | **263 GB/s** = 767.33× ZipNN, **"0.58× higher than Bitcomp"** *(sic — 0.58× is slower; see hazards)*, 2.27× HANS; peak 317 GB/s | §VI-B, p. 1328 **verified as printed** |
| Decompression throughput | all | GB/s | NV-Bitcomp · HANS · Diet-Float | **up to 4.22× Bitcomp, 2.11× HANS**; **−6% vs Diet-Float on BF16**; FP16/FP32 "improvement of approximately 0.31–1.90 over Diet-Float" *(units unstated)* | §VI-B, p. 1328 **verified as printed** |
| Range, both directions | 10 models | GB/s | — | compression **263–523**, decompression **188–336** | §IX conclusion, p. 1331 **verified** |
| **Same-model cross-platform** | Qwen3-32B | CR, comp/decomp GB/s | ZipNN(CPU) 1.50, 0.4/1.0 · NV-ANS 1.24, 139.7/176.7 · NV-Bitcomp 1.32, 291.8/155.2 · Diet-ANS 1.23, 154.4/194.5 · **Diet-Float 1.47, 271.9/271.3** · HANS(NPU) 1.34, 162.6/117.7 | **ENEC(NPU) 1.35, 360.6 / 213.8** · **ENEC-GPU-V0 1.34, 291.3/269.4** · **ENEC-GPU-V1 1.35, 419.2 / 421.0** · ENEC-CPU 1.35, 1.22/1.56 | Table VII, p. 1331 **verified** |
| **End-to-end, Qwen3-32B** | Qwen3-32B, HF Transformers, layer-wise overlapped decompress | TTFT / TPOT | uncompressed **with partial CPU offloading** | **up to 4.1× TTFT, 3.9× TPOT**; vs HANS **1.7× / 1.6×** | §VI-C, p. 1329 **verified** |
| **End-to-end, Falcon-40B** | Falcon-40B | TTFT / TPOT | same | **up to 6.3× TTFT, 4.9× TPOT**; vs HANS **1.8× / 1.7×** ← *the abstract's 6.3×* | §VI-C, p. 1329 **verified** |
| End-to-end, artifact reproduction | Qwen3-32B, batch 1 | TTFT / TPOT | baseline 2.36064 s / 1.1951 s | ENEC 0.556342 s (**4.24×**) / 0.361142 s (**3.31×**) | Artifact Appendix F-3, p. 1335 **verified** — **4.24× exceeds the paper's "up to 4.1×"** |
| Motivation | Qwen3-32B on 910B2 | share of latency | — | memory access **78–85%** of prefill and decode; naive deployment **4.1× / 3.3×** slower than ENEC | Fig. 1a + §I, p. 1319 **verified** |
| Motivation | Falcon, batch 4 | CPU→NPU transfer share | — | **~80% of execution time** for certain layers | §VI-C, p. 1329 **verified** |
| Compressibility premise | DeepSeek BF16 weights | entropy | — | sign+mantissa **7.97 bits**; exponent **2.58 bits** | §III Obs. 1, p. 1322 **verified** |
| Ablation | DeepSeek | comp / decomp GB/s | V0 (basic design) ≈ 119 / 34 | V1 ≈ 180/44 (bit-width quantization), V2 ≈ 388/111 (branch-free transform), **V3 ≈ 388 / 219** (IDD-Scan) | Fig. 13, p. 1331 — prose **verified**, bar values **inferred / approximate** |
| Parameter transfer | params searched on DeepSeek-V3, applied unchanged | CR loss | per-model optimal | **0% on Falcon-7B / Qwen3-8B / Qwen3-32B**; **5% on Llama-3.1-8B** (1.31 vs 1.36) | Table V, p. 1330 **verified** |
| Ratio vs file size | DeepSeek | CR at 1 MB → 512 MB | ZipNN flat 1.50–1.51 | ENEC flat **1.37–1.38** | Table VI, p. 1330 **verified** |
| Cost of the basic design | — | share of kernel time | — | gather lookup **35%** (comp) / **45%** (decomp), reduction-max **40%**, prefix sum **30%** | §IV-B, p. 1323 **verified** |

### Citation hazards

1. **"1.12× better compression ratio than nvCOMP" (abstract) is a maximum across a 10-model ×
   6-variant grid, taken against nvCOMP's *weakest* mode.** The only pairing in Table II that
   yields 1.12 is **Wav2Vec2 FP32, ENEC 1.15 vs NV_ANS 1.03 = 1.117** — **inferred / not
   verified** (the paper never names the pairing). Against nvCOMP's *best* mode (Bitcomp) ENEC is
   1.02× on BF16 and **1.00× on FP32**. **Do not quote 1.12× as "better than nvCOMP".**
2. **"3.43× higher throughput than DietGPU" (abstract) has no source in the paper.** It appears
   in the abstract and in a contribution bullet (p. 1320) and nowhere else; §VI-B's DietGPU
   comparisons are all *decompression* and all much smaller. Back-derivation: FP32 peak 523 GB/s
   ÷ Diet_ANS ≈ 152 GB/s ≈ 3.4 — **inferred / not verified**, and it would be *max ENEC vs
   DietGPU's weaker mode on the format where ENEC is fastest*. **Flag before citing.**
3. **ENEC's compression ratio is worse than the two specialist baselines on every model.** Any
   sentence of the form "ENEC compresses better than X" needs X named: it is true of HANS and of
   nvCOMP's general modes, **false of ZipNN and DietGPU::Float**. The paper is honest about this
   (§VI-A, p. 1328); abstract-level readers will not be.
4. **"987× / 1266× / 767× faster than ZipNN" is 48 NPU vector cores against a CPU whose thread
   count is never stated** — and §VII-A prices ENEC-CPU against ZipNN "in a **single-core**
   configuration" (p. 1331), which suggests the CPU baseline is single-threaded throughout.
   **These three numbers are not a meaningful architecture comparison.** Table VII's 0.4 GB/s for
   ZipNN corroborates single-core.
5. **"0.58× higher than Bitcomp" (§VI-B, FP16, p. 1328) reads as a win but states a loss** —
   0.58× is 42% *slower*. Either the wording or the number is wrong; the surrounding sentence
   frames it as an advantage. **Do not quote.**
6. **"an improvement of approximately 0.31–1.90 over Diet-Float" (§VI-B, p. 1328)** gives no
   units — ratio or absolute GB/s is undecidable from the text.
7. **The 6.3× / 4.9× are TTFT / TPOT on Falcon-40B against an uncompressed CPU-offload
   baseline**, i.e. against a configuration that is paging weights over PCIe. Against the other
   NPU compressor the same experiment gives **1.8× / 1.7×**. The honest headline is 1.7–1.8×.
8. **The artifact's 4.24× TTFT (p. 1335) is larger than the paper's stated "up to 4.1×"
   (p. 1329)** for the same model. Minor, but the two do not reconcile.
9. **ENEC-GPU-V1 outperforms ENEC-NPU on both throughputs** (419.2/421.0 vs 360.6/213.8,
   Table VII). Quoting ENEC's NPU numbers as evidence that Ascend specialisation pays needs this
   row alongside.
10. **The end-to-end speedups are not iso-hardware-utilisation.** Compression runs on the AIV
    units only, which the paper notes "have significantly lower peak compute capacity than a full
    A800 GPU" (§VI, p. 1327) — an argument in ENEC's favour on throughput, but it also means the
    Cube units are idle during the compression benchmark and busy during inference. The
    interaction is never measured.

---

## Cost and requirements

**Hardware cost: none.** No RTL, no synthesis, no area, no power, no energy number appears in the
paper. ENEC is AscendC (C++17) kernel code plus Python tooling. **verified by grep.**

**Runtime cost.**
- **A 32 KB per-thread lane buffer** in the basic design (8,192 × 32-bit lanes, Algorithm 1
  line 11, p. 1323) and a **32 KB overflow buffer** for the high `n−m` bits (§V-B, p. 1325)
  **verified**. Block size is capped at **16,384 elements** because 32,768 would exceed the
  **192 KB Unified Buffer** (§VI-D, p. 1329) **verified**.
- **48 AIV threads** (one per vector unit on a 910B2), cyclic over fixed-length blocks (§V-A,
  p. 1324) **verified**.
- **Decompression must be overlapped or it is on the critical path.** The paper overlaps layer
  *k+1*'s decompression with layer *k*'s forward pass (§VI, p. 1328) **verified**; it does not
  report what happens when they cannot be overlapped (small batch, short layers), nor what
  fraction of the AIV budget the overlap consumes.
- Decompression throughput (188–336 GB/s) is **well below HBM bandwidth on a 910B2** — so on a
  model that already fits in HBM, inserting ENEC would *reduce* effective weight bandwidth.
  **inferred / not verified** (the paper does not state 910B2 HBM bandwidth and does not run this
  configuration).

**Offline cost.** A per-model parameter search over `(b, n, m, L)` — an exhaustive scan of `b`
plus a joint `(m, L)` search — run per tensor and aggregated (§V-E, p. 1326; Artifact: a
`hyperparams_results.csv` "for every model tensor"). **Cheap in practice and largely avoidable**:
DeepSeek-V3's parameters transfer at 0% CR loss to three of four other models (Table V, p. 1330)
**verified**.

**Deployment requirements.** Ascend 910B2, aarch64, CANN 8.2.RC1.alpha002, torch 2.5.1 +
torch_npu, 200 GB disk, ~3 h to reproduce (Artifact check-list, p. 1334) **verified**.

**What stays uncompressed — the "escape hatch" analogue.** **The sign bit and the entire
mantissa** — 8 of 16 bits for BF16, 12 of 16 for FP16, 24 of 32 for FP32. That is not an
accuracy escape hatch (nothing is lost) but it is the **hard ceiling on the compression ratio**:
even a perfect exponent coder could not take BF16 below 8 + 2.58 = 10.58 bits, i.e. **CR 1.51×**
— which is, to two decimals, exactly what ZipNN achieves. **inferred / not verified**, but it
explains why every BF16 row of Table II tops out at 1.51.

**Retraining: none, and the question does not arise.** Bit-identical reconstruction on all ten
models (§VI-A, p. 1328) **verified**. Not PTQ, not QAT — no calibration set, no fine-tuning, no
accuracy evaluation of any kind in the paper.

---

## Limitations and open questions

**The authors state:**
- The fixed-length choice "limits element-wise encoding flexibility — slightly reducing
  compression ratios" and they "argue this modest compromise is well justified" (§VI-A, p. 1328).
- Decompression is slower than compression because prefix sum and reverse gather "are not well
  optimized on Ascend NPU architectures" (§VI-B, p. 1328).
- Future work: "extend support and performance optimizations to **a broader range of
  low-precision and integer data formats**" (§IX, p. 1331) — i.e. **INT8/FP8 support does not
  exist today**.

**They do not state:**
1. **No experiment where the model fits in HBM.** Both end-to-end models are run against a
   CPU-offload baseline because "a single Ascend 910B2 cannot hold the full model weights"
   (§VI, p. 1328). The regime where ENEC would have to beat plain HBM reads is untested.
2. **The 213.8 GB/s decompression is never compared to the bandwidth it replaces.** Whether
   ENEC is a win at HBM speeds, or only at PCIe speeds, is the paper's central unanswered
   question.
3. **AIV occupancy during inference is not accounted.** Compression benchmarks run with the
   Cube units idle; inference runs with them busy. Whether 48 AIVs can sustain 213 GB/s while
   also doing layernorm, softmax and elementwise work is not measured.
4. **Its own GPU port is faster than its NPU version** (Table VII) and the paper does not
   discuss what that implies about the Ascend-specificity of the contribution.
5. **No composition with quantization is tried**, despite §III arguing INT8/FP8 offer "limited
   additional compressibility beyond the quantization itself" — an assertion with no measurement
   behind it in this paper. **The obvious experiment — ENEC on an INT8 or FP8 checkpoint — is
   absent.** That is the experiment the survey most wants.
6. **Robustness of the linear-map assumption is tested on four LLMs only.** Llama-3.1-8B already
   loses 5% of ratio under transferred parameters; the FP16 diffusion model needs a different
   `(b, n)` entirely. Nothing is said about MoE experts, embeddings, or fine-tuned checkpoints
   whose exponent distributions drift.
7. **Accuracy is never measured, correctly** — but that means the paper contributes no evidence
   at all to the accuracy-vs-compression trade-off the survey is about.

---

## Relation to other entries

**Against [`Ecco`](../Ecco/ANALYSIS.md) — the axis this paper settles.** Ecco is the corpus's
sharpest case of compression-that-is-not-arithmetic: its decompressor sits **between L1 and L2**,
the SMs receive **decompressed FP16**, and its `W4A8KV4` is a *storage* format. ENEC is one full
step further out on the same axis, and further in three separate ways:

| | Ecco | ENEC |
|---|---|---|
| Where decompression happens | GPU cache hierarchy, **between L1 and L2** | **A different core type** — AIV vector units; the AIC Cube unit never touches the stream (§IV-A ④) |
| Does the datapath see the compressed form? | No — FP16 to the SMs | No — full-width BF16 to the Cube |
| Are the stored values changed? | **Yes** — group-wise **k-means codebook**, lossy, plus a clip/pad outlier scheme | **No** — bit-identical reconstruction on 10/10 models |
| What is compressed | weights, activations, KV cache | **weights only, and within a weight only the exponent field** |
| What it costs | new decompressor hardware in the memory hierarchy | **nothing** — a kernel |

So on the proposed **"compression vs cheaper arithmetic"** axis, **Ecco is the midpoint and ENEC
is the pole.** Ecco has a quantizer inside it (the codebook is a non-uniform quantizer) even
though its hardware buys only bandwidth; ENEC has no quantizer at all. If the axis is drawn with
Ecco at one end, ENEC extends it.

**Against [`SpZip`](../SpZip/ANALYSIS.md) — not the same kind of non-quantization paper.** SpZip
compresses whatever an irregular application streams — **index streams and payload values alike**
(§IV compresses "adjacency matrix, update bins, and vertex data"; §V-A notes PR/PRD are harder
"because they have **floating-point values** with little value locality"). **Corrected 2026-09-14
from the SpZip close read:** this paragraph previously said SpZip had "no floating-point values in
play" and compressed bitvectors — both wrong (`bitmap`/`bitvector` grep to **zero**), and it was
repeating TAXONOMY's "only sparse-format compression" gloss, which the paper itself refutes. The
real distinction is **format-blindness**: SpZip's delta byte-codes and bit-plane compression see
bytes and bit-planes and never the numeric format, and the paper's only remark about floats is
that they compress *badly*. ENEC's data is a named floating-point format and its method reads the **exponent
field** — so the discriminator is not lossy-vs-lossless and not value-vs-structure, but **whether
the code knows the numeric format**. That is the line the human's `Q-ORIENTED` ruling on ENEC
(2026-09-14) draws, and SpZip sits on the other side of it. Also: SpZip
builds hardware (a fetcher/decompressor at 0.2% of core area) and evaluates in simulation; ENEC
builds no hardware and measures on shipping silicon. **They should not share a box.**

**Against [`IBMCompressionAccelerator`](../IBMCompressionAccelerator/ANALYSIS.md) — the direct
ancestor.** IBM's NXU is fixed-function Deflate (LZ77 + Huffman) in POWER9/z15 silicon: general
enterprise data, format-agnostic, <0.5% of chip area, 388× software zlib. ENEC is what you get
when you (a) specialise the data to model weights, (b) refuse the hardware, and (c) discover that
the accelerator you are on cannot run the entropy stage at all. **The NXU's Huffman engine is
precisely the block ENEC's §VII-B wishes for** ("lightweight variable-length decoding near vector
registers", p. 1331). Cite the pair together: fixed-function lossless compression exists and is
cheap in silicon; the AI accelerators shipping today do not have it.

**The exponent-entropy premise is a bridge into the quantization literature, and it is the reason
this paper is worth a paragraph.** Observation 1 — sign+mantissa 7.97 bits of entropy, exponent
2.58 — is the *same distributional fact* that motivates:
- **shared-exponent formats** ([`MXFFP`](../MXFFP/ANALYSIS.md), block floating point,
  [`UniCore`](../UniCore/ANALYSIS.md)'s DynFP) — amortise the exponent over a block,
- **exponent codebooks** ([`Mokey`](../Mokey/ANALYSIS.md), GOBO, [`Ecco`](../Ecco/ANALYSIS.md)),
- **[`AQuant`](../AQuant/ANALYSIS.md)'s exponent-only L1 distance** — the exponent alone carries
  enough of the value to do the work.

ENEC exploits it **losslessly and outside the datapath**; the format papers exploit it **lossily
and inside it**. That contrast is a clean way to open a survey subsection on exponent structure,
and ENEC gives it a hard measured number: **the exponent field is worth 3.85 bits, and the other
8 bits of a BF16 weight are incompressible.**

**And the survey's most useful use of ENEC is as the lossless floor.** `CR 1.35× on BF16 = 11.85
effective bits`, measured on production hardware with bit-identical output, bounds every
quantization claim in the corpus: **that is what refusing to lose anything buys you.** A W4 method
is 3× past that floor, and the 3× is entirely the price of being lossy. No other entry supplies
this number.

**Recommendation on the "no box" question** (`survey/README.md`, "Papers the taxonomy has no box
for"): **exclude ENEC from the data-type × architecture boxes, and cite it twice** — once as the
lossless floor, once as measured evidence for the exponent-entropy premise. It is not a
quantization paper by any reading: no value is changed, no format is proposed, the compute
datapath never sees the compressed form, and the paper's own §III argues *against* applying itself
to quantized tensors. **Do not give the seven no-box papers one shared box**: `Ecco` has a
quantizer and belongs inside; `SpZip` and `CommutativeDataReordering` are not about numeric
formats at all; `Gist` and `JPEG-ACT` are training-activation work; `IBMCompressionAccelerator`
and `ENEC` are the lossless pair. Three different exclusions, not one.

---

## For the note

### §1 one-line summary

> Changes nothing about the number — weights stay **BF16 / FP16 / FP32**, bit-identical — and
> compresses only the **exponent field** (2.58 bits of entropy against 7.97 for sign+mantissa),
> replacing the entropy coder that Ascend's branch-free SIMD cannot run with a **frequency-rank
> affine remap** `y = (2ⁿ − x + b) mod 2ⁿ` plus a **two-level fixed-length group pack** (L = 16:
> 3 bits if the group max fits, else 6, one mask bit per group) and a transpose-based prefix scan
> that dodges Ascend's 32-byte intra-segment dependency: **BF16 16 → 11.85 bits, CR 1.35×**, at
> **372 GB/s compress / 214 GB/s decompress measured on a shipping Ascend 910B2**, worth **up to
> 6.3× TTFT** against an uncompressed CPU-offload baseline (1.8× against the other NPU
> compressor) — and **no arithmetic changes anywhere**, because the vector units expand every
> weight to full width before the Cube unit sees it.

### Proposed values on their four axes

| Axis | Proposed | Evidence (one line) |
|---|---|---|
| **Level** | **`ALGO+SYS`** — seed and revision log agree | The algorithm is real (fixed-length block code, affine remap Eq. 2, hierarchical halving bit-packing Alg. 2, IDD-Scan, the Eq. 4 parameter search) and the system is shipped (AscendC kernels, HuggingFace Transformers integration with layer-wise overlapped decompress, offline parameter-search tool, BSD-3 artifact). **No `ARCH`** — grepped: `area`, `mm2`, `RTL`, `synthes`, `simulat` all **zero hits**; §VII-B proposes hardware but builds none |
| **Q-oriented** | **`NON-Q-ORIENTED`** — seed agrees | Apply the test the other way round: there is **no quantization to remove**. The input is an un-quantized FP checkpoint, the output is bit-identical, and §III (p. 1321-22) explicitly declines to target INT8/FP8. The method is *format*-oriented (it reads the IEEE exponent field) but not *quantization*-oriented, and swapping the datapath to INT8 would leave it with nothing to compress rather than leaving its contribution intact |
| **Data type** | **`BF16` `FP16` `FP32`** — **seed has `—`; I disagree** | Table III (p. 1327) partitions the ten models by exactly these three formats; §III p. 1321 names them as the three formats weights are stored in and picks BF16 as representative; Table IV (p. 1329) gives different `(b, n)` per format because the exponent field width differs. The element format is *the object of the method*, so `—` hides the paper's subject |
| **Generation** | **`G3`** — seed has `—`; low confidence, see below | Judged by paradigm: LLM-specific problem statement (Llama-3.1-405B > 8×64 GB HBM, Qwen3-32B decode memory-bound, weight-only), and it sits on the format-merges-with-compression edge that TAXONOMY names as the G3 signature. **But** TAXONOMY's own worked example gives `SpZip`, the other non-Q compression paper, `—` on both this axis and data type. **If the human prefers `—` for non-Q compression papers, that precedent is consistent and I would not argue.** |
| **Optimization** (free text) | `lossless compression` `exponent-only coding` `fixed-length block coding` `frequency-rank affine remap` `two-level bit-width packing` `hierarchical halving bit-packing` `dependency-decoupled scan` `branch-free SIMD` `Ascend NPU` `AscendC kernels` `weight-only` `CPU-NPU offload` `open-source artifact` | Seed has four; the two that change how the paper reads are **`exponent-only coding`** and **`fixed-length block coding`** |

### Seed-tag disagreements

1. **Drop `entropy coding` from Optimization — it is factually wrong.** The abstract says
   **"block-based fixed-length encoding scheme"** (p. 1319). Grepped: `entropy` appears 11 times
   and **not once describes ENEC's own code** — every instance is either background (§II-B) or a
   statement that Ascend *cannot run it*: "making it particularly unsuitable for entropy coding"
   (§IV-A ①, p. 1322), "renders traditional entropy coding and dictionary-based methods
   impractical" (p. 1322). The paper's contribution is the **replacement** of entropy coding with
   a fixed-length code. Replace with `fixed-length block coding` + `frequency-rank affine remap`
   (the code is frequency-*informed* but not variable-length). This is the same failure mode as
   the `SmartExchange`/`SVD` seed tag: a plausible term carried from the seed row and not grepped.
2. **Data type `—` → `BF16` `FP16` `FP32`.** See the table above. A reader scanning the venue list
   with `—` cannot tell that ENEC's baseline is an *un-quantized* checkpoint, which is the single
   fact that places it relative to every other row.
3. **`Level ALGO+SYS` and `Q-oriented non-Q`: confirm, do not revisit.** The revision-log
   amendment `ARCH` → `ALGO+SYS` (venue README line 115) is right and the evidence is above.
4. **Generation `—` → `G3` is a judgment call I am flagging rather than asserting** — see the
   table row. Either value is defensible; the SpZip precedent argues for `—`.
5. **The summary cell "Software method for a shipping NPU, not new hardware" is accurate** and
   should be kept; I would add what is compressed, since that is what a reader needs.

### Proposed venue-list row

```
| [ ] | [ENEC: A Lossless AI Model Compression Method Enabling Fast Inference on Ascend NPUs](https://doi.org/10.1109/ISCA66397.2026.00100) | *close read* | ALGO+SYS | non-Q | `BF16` `FP16` `FP32` | G3 | `lossless compression` `exponent-only coding` `fixed-length block coding` `frequency-rank affine remap` `hierarchical halving bit-packing` `dependency-decoupled scan` `branch-free SIMD` `Ascend NPU` `weight-only` | **Not entropy coding — the point is that Ascend cannot run it.** Sign and mantissa stored raw; only the exponent is coded, by an affine frequency remap + fixed-length group pack. BF16 16 → **11.85 bits, CR 1.35×**, bit-identical. Software on a shipping 910B2, no hardware. **The lossless floor for the survey** |
```

### §4 fairness verdict (note version, ≈60 words)

> Fair where it counts: **iso-hardware-era, iso-model, iso-metric**, all measured on shipping
> silicon, bit-identical output verified on 10/10 models. **Not iso-thread** (987×/1266× vs an
> apparently single-core ZipNN) and **not iso-ratio** — ENEC loses to ZipNN and DietGPU::Float on
> every model. Do not quote **1.12× vs nvCOMP** (max over a grid, weakest variant) or **3.43× vs
> DietGPU** (unsourced); 6.3× is vs CPU offload, 1.8× vs HANS.

### §4 fairness — the long form (stays here, not in the note)

**Unusually clean for an industrial paper, and the problems are all in the abstract rather than
the evaluation.**

- **Evidence level is uniform and it is the best kind ✓.** Everything is measured on a shipping
  Ascend 910B2 or a shipping A800. No synthesis, no simulator, no analytical projection anywhere
  in the paper. **This is the only entry in the corpus whose entire result set is silicon
  measurement of a deployable artifact.** Nothing needs to be de-pooled.
- **Losslessness is verified, not asserted ✓.** "we have meticulously verified that all 10 models
  ... achieve bit-identical reconstruction" (§VI-A, p. 1328).
- **Baselines are run, not quoted ✓ (mostly).** ZipNN and DietGPU via their own APIs, nvCOMP via
  its own benchmark harness, HANS and ENEC via `msprof`. The one asymmetry is disclosed: HANS has
  only a Python API, so it is profiled at kernel level to avoid a Python-overhead penalty — a
  concession *in the baseline's favour*, which is the right direction.
- **Measurement boundary is disclosed ✓**: "device-side kernel execution time only, **excluding
  PCIe transfer**" (§VI-B, p. 1328). It is the same boundary for every method.
- **Iso-platform ✗, by necessity, and half-acknowledged.** Ascend 910B2 vs NVIDIA A800 is called
  "performance-similar" (§VI, p. 1327) with no normalisation and no node, area or power figure on
  either side. The paper then argues *against itself* — ENEC "runs exclusively on the AIV units,
  which have significantly lower peak compute capacity than a full A800 GPU" — which is a fair
  point but is not a measurement.
- **Iso-thread ✗ on the CPU baseline.** ZipNN's 0.4 GB/s (Table VII) and the 987× / 1266× / 767×
  ratios are almost certainly against a single core (§VII-A prices ENEC-CPU vs "ZipNN in a
  single-core configuration"), against 48 NPU vector units. Thread count is never stated. **The
  ZipNN speedups are not architecture comparisons and should not be repeated.**
- **Iso-ratio ✗, and the paper says so.** ENEC is below ZipNN and Diet_Float on all ten models
  (Table II) and ties nvCOMP-Bitcomp on FP32. §VI-A frames this as "a deliberate trade-off";
  the abstract frames only the wins.
- **Two abstract numbers do not survive interrogation.** 1.12× vs nvCOMP is the max of a 10 × 6
  grid taken against nvCOMP's weakest mode; 3.43× vs DietGPU appears twice in the front matter and
  nowhere in the evaluation. Both are the `SmartExchange` / `Ecco` "maximum across a grid" pattern.
- **The end-to-end baseline is weak but honestly labelled.** "uncompressed inference setup with
  **partial CPU offloading**, since a single Ascend 910B2 cannot hold the full model weights"
  (§VI, p. 1328). Given that framing, 6.3× is a claim about PCIe, not about the NPU. The
  same-class comparison — ENEC vs HANS, both NPU compressors, same integration — is **1.7–1.8×**,
  and that is the number to quote.
- **The most awkward row is the authors' own.** ENEC-GPU-V1 (419.2 / 421.0 GB/s) beats ENEC-NPU
  (360.6 / 213.8) at the same ratio, on the very table meant to demonstrate portability. Credit
  for printing it; it means "optimized for Ascend" is a statement about *feasibility*, not about
  superiority.

---

## Abstract (verbatim, ISCA 2026 proceedings)

> The rapid scaling of Large Language Models presents significant challenges for their
> deployment and inference, particularly on resource-constrained specialized AI hardware
> accelerators such as Huawei's Ascend NPUs, where weight transfer has become a critical
> performance bottleneck. While lossless compression can preserve model accuracy and reduce
> data volume, existing lossless compression algorithms exhibit extremely low throughput
> when ported to the Ascend NPUs. In this paper, we propose ENEC, a novel lossless
> compression method specifically customized for AI model weights and optimized for Ascend
> Neural Processing Units. ENEC adopts a block-based fixed-length encoding scheme and
> incorporates a series of optimizations: bit-width quantization with hierarchical halving
> bit-packing, vectorized branch-free integer transformation, and dependency-decoupled
> intra-segment scan. Experimental results demonstrate that ENEC outperforms existing state-
> of-the-art NPU compressors in both compression ratio and throughput. Compared to leading
> GPU solutions, ENEC achieves a 3.43× higher throughput than DietGPU and a 1.12× better
> compression ratio than nvCOMP. By reducing weight transmission overhead, ENEC
> significantly improves end-to-end inference performance, achieving up to a 6.3× speedup.
> On Ascend NPUs, ENEC is the first open-source lossless compression algorithm for model
> weights that achieves performance comparable to state-of-the-art GPU compressors, offering
> an effective solution for deploying large-scale AI models.
