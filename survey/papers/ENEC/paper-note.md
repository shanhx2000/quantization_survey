# ENEC: A Lossless AI Model Compression Method Enabling Fast Inference on Ascend NPUs

**Venue / Year:** ISCA 2026, pp. 1319-1335 · **Link:** https://doi.org/10.1109/ISCA66397.2026.00100 · code: https://github.com/jinwuyang/ENEC_ISCA_AE · **Reader:** Haoxuan · **Date:** 2026-09-14

## Tags

| | |
|---|---|
| **Level** | `ALGO+SYS` |
| **Q-oriented** | `Q-ORIENTED` |
| **Data type** | `BF16` `FP16` `FP32` |
| **Generation** | `G3` |
| **Optimization** | lossless compression · exponent-only coding · fixed-length block coding · frequency-rank affine remap · two-level bit-width packing · hierarchical halving bit-packing · dependency-decoupled scan · branch-free SIMD · Ascend NPU · weight-only · CPU-NPU offload |

## 1. One-line summary

Changes nothing about the number — weights stay **BF16 / FP16 / FP32**, bit-identical — and
compresses only the **exponent field** (2.58 bits of entropy against 7.97 for sign+mantissa),
replacing the entropy coder that Ascend's branch-free SIMD cannot run with a **frequency-rank
affine remap** `y = (2ⁿ − x + b) mod 2ⁿ` plus a **two-level fixed-length group pack** (L = 16:
3 bits if the group's max fits, else 6, one mask bit per group) and a transpose-based prefix scan
that dodges Ascend's 32-byte intra-segment dependency: **BF16 16 → 11.85 bits, CR 1.35×**, at
**372 GB/s compress / 214 GB/s decompress measured on a shipping Ascend 910B2**, worth **up to
6.3× TTFT** against an uncompressed CPU-offload baseline (1.8× against the other NPU compressor)
— and **no arithmetic changes anywhere**, because the vector units expand every weight to full
width before the Cube unit sees it.

## 2. Data type

**Formats.** `W16 lossless` — BF16 in, BF16 out, bit-identical on 10/10 models. Also FP16 and FP32. Activations and KV cache untouched. **No quantization anywhere; no value is changed.**

**Effective width.** BF16 `1 + 7 + 3.85 = 11.85 bits/element` → **CR 1.35×**. FP16 1.12×, FP32 1.15×.

**What is actually coded.** The exponent field only. Sign and mantissa written verbatim — 7.97 bits of entropy, incompressible; exponent 2.58 bits.

**Granularity.** Groups of **L = 16** exponents, 1 mask bit per group; block of **16,384 elements** (32,768 would exceed the 192 KB Unified Buffer). `(b, n, m, L)` searched per tensor; BF16 and FP32 all land on `(≈121-125, 6, 3, 16)`, FP16 on `(7, 4, 3, 16)` / `(11, 5, 3, 16)`.

**Two-level pack, not variable-length.** ≤ `m = 3` bits if the group's max fits, else `n = 6` for the whole group. From `B_exp = 1/L + n + (m−n)p(m)^L = 3.8465`: **~74% of groups at 3 bits, ~26% at 6**.

**Outliers. None as a value mechanism.** A group whose max exceeds `m` is not an outlier path, just the 6-bit branch, with its high `n−m` bits diverted to a side buffer and OR-ed back on decode. Cost is a mask bit, not precision.

**Escape hatch — the mantissa.** 8 of 16 BF16 bits are never compressed. That caps *any* exponent-only method at `8 + 2.58 = 10.58` bits, i.e. **CR 1.51×** — which is exactly what ZipNN achieves and why every BF16 row of Table II tops out there.

**Accumulator.** Not applicable — there is no arithmetic. The Cube unit multiplies full-width BF16.

**Retraining. Neither PTQ nor QAT.** Bit-identical reconstruction, no calibration set, no accuracy experiment of any kind.

**Explicitly not INT8/FP8.** The paper declines both: lower precision "risks accuracy", quantization is "a separate lossy compression step" offering "limited additional compressibility beyond the quantization itself", the AIV API lacks the bit-manipulation instructions, and FP8 is "entirely unsupported by the hardware". Integer formats are future work.

## 3. Optimization

**Why entropy coding dies on Ascend — the premise.** The authors port ANS and get ~0.3-1 GB/s. The diagnosis is six numbered architectural mismatches: SIMD with no conditional branch, no scatter, variable-length memory handling slower than fixed-length, compression is vector work so the Cube units sit idle, no cheap inter-thread sync (each AI core is one heavyweight thread), and no cheap comparisons/reductions. Every entropy coder and every LZ variant needs at least one of these. **So the contribution is the replacement of variable-length coding with a fixed-length code that loses a little ratio and gains three orders of magnitude of throughput** — the abstract's own words are "block-based fixed-length encoding".

**Frequency-rank affine remap.** The basic design gathers into a frequency table: 35% of compression time, 45% of decompression time. Observation 5 says exponent value versus frequency rank is a straight line (`Y = −1.00X + 123.00`), so the table is replaced by `y = (2ⁿ − x + b) mod 2ⁿ` — vector subtract, negate, mask. Two's complement does the negative-value handling, so no branch; the map is injective, so it stays lossless. It *approximates* the true frequency order, and that is where the ratio goes.

**Two-level bit-width pack + hierarchical halving bit-packing.** Group-uniform width turns a reduction-max (40% of compression time) into a bitwise OR. Algorithm 2 then folds lane pairs (`data[i] |= data[i+len] << width`), doubling effective width each round, splitting off aligned bytes whenever the width crosses 8 and recursing on the overflow — the byte normalisation that makes the stream 32-byte alignable. V1 also cuts per-group metadata from 4 bits to 1.

**IDD-Scan.** AscendC forbids arithmetic between elements inside one 32-byte segment, and a row of 16 halves is exactly 32 bytes, so `row[i] += row[i−1]` is illegal. Transpose so intra-row dependencies become inter-row, scan columns in `log₂M` steps, transpose back, run a second hierarchical scan on a copy in `log₂N` steps, take its last column, shift to exclusive, broadcast, add. Decoupled look-back expressed entirely in transposes and broadcasts, because those are the only primitives available. Worth ~2× on decompression on its own.

**Offline parameter search, and it transfers.** Histogram the exponents, exhaustively scan `b` minimising `Σp(x)·y`, then jointly search `(m, L)` minimising `B_exp`. Run per tensor, but largely avoidable: DeepSeek-V3's parameters transfer at **0% ratio loss** to Falcon-7B, Qwen3-8B and Qwen3-32B, **5%** to Llama-3.1-8B.

**What runs where — the fact that places the paper.** Compression and decompression are AscendC kernels on the **AIV vector units**; the model runs on the **AIC Cube unit**. Decompression is layer-wise and overlapped with the previous layer's forward pass. **The compute datapath never sees a compressed value, and no value is ever changed** — so this buys PCIe and HBM traffic, and nothing else, ever. One step further out than Ecco, which at least decompresses inside the cache hierarchy and does change the stored values.

**Hardware cost: none.** No RTL, no synthesis, no area, no power figure in the paper. Runtime cost is a 32 KB lane buffer plus a 32 KB overflow buffer per thread, 48 AIV threads, and a 192 KB UB ceiling on block size. §VII-B asks future accelerators for variable-length decode near the vector registers, per-lane bit extraction, parallel prefix-sum units, and datapaths that "decouple exponent and mantissa processing" — a wish list, not a design.

## 4. Results

| | |
|---|---|
| Baseline | **ZipNN** (CPU), **nvCOMP** Zstd/Deflate/GDeflate/ANS/Bitcomp and **DietGPU** ANS/Float (A800 GPU), **HANS** (Huawei's closed-source Ascend compressor); end-to-end vs uncompressed inference with partial CPU offloading |
| Models / datasets | 10 models: 5 BF16 (Falcon-7B, Qwen3-8B, DeepSeek-7B, Qwen3-32B, Llama-3.1-8B), 2 FP16 (Mistral-7B, SVD-img2vid), 3 FP32 (OLMo-1B, BERT-base, Wav2Vec2). End-to-end on Qwen3-32B and Falcon-40B |
| Accuracy delta | **Zero, verified** — bit-identical reconstruction on all 10 models. No accuracy experiment exists or is needed |
| Compression ratio | **BF16 1.35-1.37, FP16 1.09-1.12, FP32 1.15.** Beats HANS (1.33-1.35) and nvCOMP's general modes; **loses to ZipNN (1.50-1.51 BF16) and DietGPU::Float (1.47-1.48) on every model**; ties nvCOMP-Bitcomp on FP32 |
| Throughput | Compress **263-523 GB/s**, decompress **188-336 GB/s**. BF16 avg 372 GB/s = 1.39× Bitcomp, 1.36× HANS; FP32 3.08× Bitcomp, 2.47× HANS. Decompress up to 4.22× Bitcomp, 2.11× HANS, but **−6% vs Diet-Float on BF16**. Same-model (Qwen3-32B): ENEC-NPU 360.6/213.8 — **ENEC's own A800 port reaches 419.2/421.0** |
| End-to-end | Qwen3-32B **4.1× TTFT / 3.9× TPOT** vs baseline, **1.7× / 1.6× vs HANS**; Falcon-40B **6.3× / 4.9×** vs baseline, **1.8× / 1.7× vs HANS** |
| Energy / area | **None reported** — software only, no hardware built |
| Technology node | N/A. Ascend 910B2 (24 AIC / 48 AIV), CANN 8.2.RC1.alpha002, Kunpeng-920 host; baselines on NVIDIA A800 + Xeon 8358P, CUDA 12.6 |
| Evidence level | **Silicon measurement throughout** — `msprof` kernel time on a shipping 910B2 and a shipping A800, device-side only, PCIe excluded; end-to-end inside HuggingFace Transformers; public BSD-3 artifact. **No synthesis, RTL, simulator or analytical model anywhere in the paper** |
| **Is the comparison fair?** | Fair where it counts: **iso-era, iso-model, iso-metric**, all silicon measurement, losslessness verified 10/10. **Not iso-thread** (987×/1266× vs an apparently single-core ZipNN) and **not iso-ratio** — ENEC loses to ZipNN and DietGPU::Float on every model. Do not quote **1.12× vs nvCOMP** (max over a grid, weakest variant) or **3.43× vs DietGPU** (unsourced); 6.3× is vs CPU offload, 1.8× vs HANS |

## 5. Comment

`Q-ORIENTED`. The whole design is conditioned on the float format: it compresses the **exponent
field** specifically, and the coder exists because that field's entropy (2.58 b) is so much lower
than sign+mantissa's (7.97 b).

## 6. Claude notes

*Suggestions from the reading agent. **Strip this section before copying into
`QuantArchSurvey/venues/ISCA/notes/`.***

- **Read depth.** Full close read of §I-§IX and the Artifact Appendix. Flagged in `ANALYSIS.md`: **Fig. 9 and Fig. 10 are bitmaps** whose bar values `pdftotext` recovers unordered with no label mapping, so **no throughput number here comes from a figure** — all from prose, Table VII or the artifact appendix; Fig. 13's ablation values are order-assigned and approximate; Algorithm 2 was read but not hand-traced; and **the abstract's 3.43× cannot be sourced to any sentence or table** — verify before citing.
- **One seed tag is factually wrong, with the evidence.** `entropy coding` → **`fixed-length block coding`** + `frequency-rank affine remap`. Grepped: `entropy` appears 11 times and **never describes ENEC's own code** — it is background, or a statement that Ascend cannot run it ("particularly unsuitable for entropy coding"; "renders traditional entropy coding ... impractical"). The abstract says "block-based **fixed-length** encoding scheme". Same failure mode as `SmartExchange`/`SVD`: a plausible term carried from the seed and never grepped.
- **Second seed dispute: Data type `—` → `BF16` `FP16` `FP32`.** With `—` a reader cannot tell that ENEC's input is an **un-quantized** checkpoint, which is the one fact that places it against every other row. Table III partitions the corpus by exactly these three formats and Table IV gives different `(b, n)` per format because the exponent width differs.
- **Generation `G3` is now on firmer ground than when I drafted it.** I had hedged it against the `SpZip` precedent (`—` on both Generation and Data type) — but **that precedent covers *non-Q* compression papers, and the 2026-09-14 ruling makes ENEC `Q-ORIENTED`**, so it no longer applies. `G3` stands on paradigm: LLM-scale weight transfer, weight-only, format merging with compression.
- **The boundary question — my draft recommendation was overridden, and the interesting part survives.** I had argued ENEC is *not* a quantization paper (no value changed, no format proposed, the Cube datapath never sees the compressed form, §III argues *against* applying the method to quantized tensors); **the human ruled `Q-ORIENTED` on 2026-09-14, on the ground that the design is conditioned on the float format — it compresses the exponent field specifically.** So ENEC sits *inside* on the Q axis while still changing no value: a compression paper that is quantization-oriented without being lossy. But **do not give the seven no-box papers one shared box**: `Ecco` has a real quantizer (k-means codebook) and belongs *inside*; `SpZip` and `CommutativeDataReordering` are not about numeric formats at all; `Gist` and `JPEG-ACT` are training-activation work; `ENEC` and `IBMCompressionAccelerator` are the lossless pair. Three exclusions, not one.
- **What I would actually cite it for — the lossless floor.** `CR 1.35× on BF16 = 11.85 effective bits`, measured on production silicon, bit-identical. That bounds every quantization claim in the corpus: **it is what refusing to lose anything buys you**, and a W4 method's remaining 3× is entirely the price of being lossy. No other entry supplies this number. The derivation is worth one line: `1/16 + 6 − 3·p(3)^16 = 3.85` exponent bits + 8 raw bits.
- **Second citation, and it is the more interesting one.** Observation 1 — BF16 sign+mantissa **7.97 bits** of entropy, exponent **2.58** — is the *same distributional fact* that motivates shared-exponent formats (`MXFFP`, BFP, `UniCore`'s DynFP), exponent codebooks (`Mokey`, GOBO, `Ecco`) and `AQuant`'s exponent-only L1 distance. **ENEC exploits it losslessly and outside the datapath; the format papers exploit it lossily and inside it.** That contrast opens a subsection on exponent structure cleanly, and ENEC gives it a measured number.
- **Place it as the pole of the compression-vs-arithmetic axis, past Ecco.** Ecco decompresses between L1 and L2 and *does* change the stored values. ENEC decompresses on a **different core type** from the one that computes, and changes nothing. If the axis is drawn with Ecco at one end, ENEC extends it — and that makes Ecco the midpoint rather than the pole.
- **Numbers I would exclude.** (i) **987× / 1266× / 767× vs ZipNN** — 48 NPU vector units against an apparently single-core CPU (§VII-A prices ENEC-CPU vs "ZipNN in a single-core configuration"; Table VII shows ZipNN at 0.4 GB/s). (ii) **1.12× vs nvCOMP** — the only pairing that yields it is Wav2Vec FP32 vs nvCOMP's *ANS*, its weakest mode; against Bitcomp it is 1.02× on BF16 and **1.00×** on FP32. (iii) **3.43× vs DietGPU** — unsourced. (iv) **"0.58× higher than Bitcomp"** (FP16) is printed as a win but states a 42% loss.
- **The awkward row is the authors' own, and I would keep it in the note.** ENEC-GPU-V1 on an A800 reaches **419.2 / 421.0 GB/s** at the same 1.35 ratio, beating ENEC-NPU's 360.6 / 213.8 on both. Credit for printing it — but it means "optimized for Ascend" is a claim about *feasibility*, not superiority, and the survey should say so if it uses the portability argument.
- **§5 material, if you want it.** The `G3` call rests on the problem, not the mechanism — the mechanism (HCLOG-style bit-packing over a frequency-ranked symbol) is 1980s compression. Its `G3`-ness is that it is the **first entry in the corpus that measures the lossless bound on a real accelerator**, which is a G3-era question (weight transfer as *the* bottleneck) answered with a G1-era code. Worth one sentence, because it is the reason the paper strains the taxonomy rather than fitting it.
- **The experiment the survey most wants is absent, and it is one line of work.** §III asserts that quantized tensors offer "limited additional compressibility beyond the quantization itself" and never measures it. **ENEC on an INT8 or FP8 checkpoint is the composition experiment**, and §IX lists it as future work. Until someone runs it, the survey cannot say whether lossless coding composes with quantization or is subsumed by it — and that, not ENEC's throughput, is the open question this entry contributes.
- **`survey/TAGS.md`, reported not applied.** Tags stay `lossless-compression` `accelerator`. But `(8) accelerator` is defined as "**custom hardware**: ASIC, NPU, or FPGA" and ENEC builds none — it *targets* a shipping NPU, which is what `(7) gpu-kernels` means for GPUs. Consider generalising (7) to cover vendor-kernel work on shipping accelerators, or leave ENEC on `(8)` as a platform tag and say so in the definition. Your call; I changed nothing.
