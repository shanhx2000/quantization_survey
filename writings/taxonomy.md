# Taxonomy of Quantization Hardware for LLMs — ISCA fill

Transcription of [`QuantArchSurvey/latex/figures/taxonomy.tex`](../QuantArchSurvey/latex/figures/taxonomy.tex)
(Fig. 1), with the ISCA branch of the corpus filled in.

The tree text is reproduced **exactly** as it stands in the `forest` source — same
wording, same order, same section pointers. LaTeX markup is rendered
(`$\rightarrow$` → `→`, `\textit{}` → *italic*, `\\` → line break); no phrase is
added, dropped or reordered.

## How to read this file

| Element | Meaning |
|---|---|
| `## Branch` / `### Sub` | a level-1 / level-2 node of the figure |
| > blockquote | the level-3 leaf text, **verbatim from `taxonomy.tex`** |
| **⊕ Entered from ISCA** | papers *added by this pass* — everything in these blocks is new, none of it is in the `.tex` |
| *[add papers]* | the leaf's `\fillhere` marker is still standing — nothing in the ISCA set belongs here |

Papers already named in the `.tex` prose (OLAccel, OliVe, GOBO, Mokey, ANT,
FIGLUT, Transitive Array, EVA, Cambricon-S, RapidNN, ANNA) stay in the
blockquote where the source put them; where the ISCA set confirms one, the entry
block says **(already in the figure)** rather than repeating it as new.

## Source of the fill

`quantization_survey/survey/papers/` — 40 analysed ISCA papers. **35 are entered
here** — every row of `venues/ISCA/README.md` as of 2026-10-01. Five are not, and the reason
is recorded rather than left implicit:

| Excluded | Why |
|---|---|
| Cambricon-SR | no quantization anywhere; the "encoding table" is Instant-NGP's hash grid |
| CommutativeDataReordering | subject is bit-level switching activity on the DRAM bus, not numeric format |
| IBMCompressionAccelerator | a shipping Deflate engine; no quantization and no AI |
| SpZip | no value is ever changed; a fetcher/compressor beside each core |
| RingCNN | imposes algebraic sparsity; uses fixed point, designs none |

**ELSA and Phi were in this table until 2026-10-01**, as spiking work out of scope. The owner
restored both to the venue (ISCA Pass 11), so they are entered below. Neither changes what a
number is in the usual sense — ELSA re-codes a quantized integer in time, Phi decomposes a
binary matrix exactly — so they enter through the encoding and lookup leaves, not the format ones. **ELSA was removed from the corpus again on 2026-10-02 (ISCA Pass 13)** and carries Stage type
`—`: it may not fit this survey's topic, since its quantization is inherited. Its entries below are
**kept on purpose**, each marked *(may not fit)*, so the spiking question stays visible in the figure.
A paper appears in **every** leaf its mechanism touches. The tree is not a
partition, and forcing one paper into one leaf is what made the earlier
`Optimization` column unusable.

---

# Quantization Hardware for Large Language Models

## Stage 1 — Numerics
*one value, one PE* (§3)

### Fundamentals and formulas (§3.1)

> Affine/integer x̂ = (q−z)·s; floating point (−1)^S 2^(E−bias) 1.M; analytic non-uniform grids (logarithmic/power-of-two, posit);
> error metrics (MSE, QSNR, kurtosis) and MSE-optimal clipping; PTQ vs. QAT as a deployment constraint; fixed- vs. variable-length encodings.

**⊕ Entered from ISCA**

| Paper | Year | What it contributes to this leaf |
|---|---|---|
| **TPUv4i** | 2021 | *PTQ as a deployment constraint*, stated as a lesson rather than a result: lesson ⑥ of ten is that TPUv1 **required** quantization and that was a mistake — developers pre-agreed a 1% quality budget and then refused it. The clearest industrial evidence that the constraint, not the error metric, decides. |
| **LoKA** | 2026 | *Error metrics* operationalised: LoKA Probe learns activation/weight statistics and quantifies per-layer error to locate where FP8 is numerically safe and where it is merely fast. |
| **ENEC** | 2026 | *Fixed- vs. variable-length encodings*, decided by the substrate: replaces the entropy coder Ascend's branch-free SIMD cannot run with a frequency-rank affine remap `y = (2ⁿ − x + b) mod 2ⁿ` plus a two-level **fixed-length** group pack. |
| **ELSA** *(may not fit)* | 2026 | *Fixed- vs. variable-length encodings* taken to the limit: a 4-bit-weight quantized ANN run as an **exactly equivalent** spiking network, the activation re-coded from a binary-weighted integer into a **temporal unary train** of ternary {−1,0,+1} events over up to T = 32 time-steps. The conversion is exact, so the 2.57-point ImageNet drop is the quantization, not the spiking. |

### Shipped scalar formats 2017--2025 (§3.2)

> FP32; TF32 1-8-10; FP16 1-5-10; BF16 1-8-7; INT16; FP8 E4M3 / E5M2; INT8; FP6 E3M2 / E2M3; FP4 E2M1; INT4.
> Silicon: V100, T4, A100, H100, Blackwell, TPU v4/v5p/v6e/v7, Trainium1/2, Inferentia, MI300X, Gaudi 3, MTIA v1/v2, Maia 100, Groq LPU.

**⊕ Entered from ISCA** — the parts of that silicon list ISCA documents from the inside

| Paper | Year | What it contributes to this leaf |
|---|---|---|
| **TPUv4i** | 2021 | The TPU v4 entry, first-hand. Keeps bf16 and IEEE fp32 from the training chip and adds int8 **only as a porting path** — at the same 138 T peak as bf16, so int8 buys memory footprint, not throughput. |
| **RaPiD** | 2021 | A fabricated 4-core chip, 7 nm EUV, 36 mm², spanning FP16, FP8 (including hybrid FP8), INT4 and INT2 in one datapath. |
| **SamsungNPU** | 2021 | The NPU in a 5 nm Samsung flagship SoC: INT8/INT16 in a re-configurable MAC array, with a lessons-learned section. |
| **LoKA** | 2026 | FP8 as it is actually deployed — Meta-scale recommendation kernels on commodity GPUs, dispatched per layer against an accuracy requirement. |

### Designed scalar types in the literature (§3.3)

> Posit and LNS variants; hybrid FP/INT encodings; self-describing formats with a data-dependent exponent/mantissa boundary (ANT's Flint).

**⊕ Entered from ISCA**

| Paper | Year | What it contributes to this leaf |
|---|---|---|
| **OliVe** | 2023 | *abfloat* — an adaptive-bias 4-bit float whose exponent bias places its range complementary to the normal type's. A designed type that only makes sense in a pair. |
| **MXFFP** | 2026 | A *self-describing* element in the ANT/Flint sense, but with the boundary made discrete: one configuration bit switches the element between `E1M2` and `E2M1` at 4 bits. |
| **UniCore** | 2026 | **DynFP**, a distribution-adaptive low-bit FP format, paired with S-FPMA so the format and its multiplier are designed together. |
| **FATE** | 2025 | A per-dimension type ladder — INT8, INT4, ternary, binary, and `INT0` meaning pruned outright — so "which type" and "whether at all" become the same decision. |
| **AQB8** | 2025 | A composite record rather than a scalar: one FP32 anchor box as a local coordinate frame, the rest as six INT8 offsets under a single isotropic per-cluster scale. |

---

## Stage 2 — Architecture
*a block, an array, a datapath* (§4)

### Granularity: the block floating point line (§4.1)

> Per-tensor → per-channel → per-token → per-group; block floating point (BFP); OCP microscaling (MXINT8/MXFP8/MXFP6/MXFP4, block 32, E8M0);
> NVFP4 two-level scaling (E4M3 per 16 + FP32 per tensor); scale application, block/tile alignment, cross-block accumulation.

**⊕ Entered from ISCA**

| Paper | Year | What it contributes to this leaf |
|---|---|---|
| **Tender** | 2024 | The *cross-block accumulation* clause, solved: consecutive band scales are constrained to be **exactly 2× apart**, so accumulating partial sums across bands is a 1-bit shift instead of a floating-point requantization. |
| **MXFFP** | 2026 | Keeps OCP MX exactly as it is — same element width, same 8-bit E8M0 shared exponent — and varies only what sits inside the block. |
| **MicroScopiQ** | 2025 | *Block/tile alignment* as the binding constraint: every element keeps a fixed bit budget so memory stays aligned and the PEs stay homogeneous, at 2.36 effective bits. |
| **Oaken** | 2025 | Per-token granularity on the KV cache, with the group boundaries profiled **offline** so the online cost is a comparison rather than a topK sort. |
| **AQuant** | 2026 | Per-token again, but the group is defined by content: base + delta, the base picked by positional stride from the tokens themselves. |
| **NDPLowBitFP** | 2026 | *Scale application* as a memory-layout problem: a scale-value interleaved layout to cut row changes, plus dequantization hiding by instruction reordering. |
| **AQB8** | 2025 | One isotropic scale per cluster of ~30–110 BVH nodes, `S_x = max(l_x,l_y,l_z)/255` — block floating point in a workload nobody files under LLMs. |
| **DRQ** | 2020 | The pre-LLM granularity root: regions (e.g. 4×16) inside a feature map, sized by design-space exploration, not channels or tokens. |
| **P3-LLM** | 2026 | Granularity chosen per operand rather than per tensor, so each LLM operand carries its own format. |

### Mixed precision — *different widths* (§4.2)

> BitFusion and the composable/bit-flexible MAC family; bit-serial and bit-parallel-slice arrays; per-layer bitwidth search (sensitivity, RL, ILP);
> weight-only asymmetry (W4A16, W4A8) as a bandwidth argument.

**⊕ Entered from ISCA**

| Paper | Year | What it contributes to this leaf |
|---|---|---|
| **BitFusion** | 2018 | *(already in the figure)* The named ancestor: BitBricks that dynamically fuse and decompose at runtime to form the multiplier width each layer needs, driven by software through Fusion-ISA. |
| **XtraMAC** | 2026 | The family's current endpoint: every supported format decomposed into a **shared integer mantissa product** plus sign/exponent handling, at constant latency and II = 1 across all datatypes. |
| **UniCore** | 2026 | Changes the primitive so composition scales **linearly** rather than quadratically — S-FPMA built from uniform adder slices, with dual-path compensation for the structured approximation error. |
| **RaPiD** | 2021 | One datapath carrying FP16, FP8, INT4 and INT2, in fabricated silicon. |
| **SamsungNPU** | 2021 | A re-configurable MAC array with INT8/INT16, in a shipped mobile SoC. |
| **DRQ** | 2020 | A *variable-speed* mixed-precision convolution array, sized so INT8 and INT4 regions both keep it busy — the scheduling half of mixed precision, which the format papers omit. |
| **LightNobel** | 2025 | A multi-precision reconfigurable matrix processing unit driven by token-wise adaptive activation quantization. |
| **SingularBit** | 2026 | *Per-layer bitwidth search* replaced by a structural rule: allocate precision **by rank**, since singular values decay fast, and push most weight parameters to 1–2 bits. |
| **LoKA** | 2026 | The search done statistically and online — probe, adapt, dispatch the fastest FP8 kernel that still meets the accuracy requirement. |
| **AQuant** | 2026 | Per-token top-25% to INT4 and the rest to INT2 against INT8 bases, with INT16 weights. |
| **FATE** | 2025 | Width chosen per dimension by a fuzzing-distance importance measure, with the ratio set workload-aware. |
| **ELSA** *(may not fit)* | 2026 | Precision chosen **per input, at runtime**: confidence-based early termination truncates the unary code — average T = 6.2 of an allowed 32, 21.9% mean latency saved for <0.2% accuracy. The spiking code supplies a monotone precision ladder for free; nothing in the hardware decides T. |
| **P3-LLM** | 2026 | A flexible mixed-precision scheme over hybrid numerical formats, one per LLM operand. |
| **TPUv4i** | 2021 | The negative result this leaf needs: int8 at the same peak as bf16 means the mixed-precision argument is about footprint, not throughput, unless the array is widened for it. |

### Mixed type — *different formats* (§4.3)

> ANT (inter-tensor format selection, intra-tensor adaptive boundary, type fusion with edge decoders); successors MERSIT, Anda.

**⊕ Entered from ISCA**

| Paper | Year | What it contributes to this leaf |
|---|---|---|
| **OliVe** | 2023 | Int and abfloat inside the same tensor, bound as **outlier–victim pairs** — intra-tensor mixed type with no index and no second datapath. |
| **MicroScopiQ** | 2025 | MX-INT inliers and MX-FP outliers in one micro-block; two formats, one aligned bit budget. |
| **MXFFP** | 2026 | The *intra-tensor adaptive boundary* made cheap: one bit per element, chosen offline by MSE for weights and at runtime for activations by a quadratically-weighted counting rule over relative exponents. |
| **XtraMAC** | 2026 | *Type fusion* without edge decoders: integer, floating point and mixed all reduce to the same integer mantissa product. |
| **UniCore** | 2026 | Unified FP/INT execution on one composable primitive, with format conversion folded into the pipeline. |
| **AQB8** | 2025 | FP32 anchor and INT8 offsets in one record — two formats whose roles differ by position, not by value. |
| **P3-LLM** | 2026 | *Inter-tensor format selection* in the ANT sense, with PIM compute units co-designed for exactly the formats chosen. |

### Outlier handling (§4.4)

> Separate high-precision path: OLAccel. Codebook-plus-wide-outliers: GOBO. In-format preservation: outlier-aware microscaling.
> Paired encoding: OliVe (outlier--victim pairs). Discrete in-block scale factors. Decomposition: low-rank + sparse, SVD splits.
> Shared cost: the edge decoder that normalizes mixed formats. Streaming variant: KV-cache quantization.

**⊕ Entered from ISCA** — this leaf names five mechanisms; ISCA supplies a paper for every one

| Paper | Year | Mechanism in this leaf |
|---|---|---|
| **OLAccel** | 2018 | *(already in the figure)* **Separate high-precision path.** 4-bit MAC units, with outlier weights given an extra MAC per SIMD lane — so the common case of one outlier per lane costs no extra cycle — and outlier activations sent to dedicated high-precision MACs. |
| **MicroScopiQ** | 2025 | *(already in the figure, unnamed)* **In-format preservation** — this is the "outlier-aware microscaling" the leaf refers to. Outliers at 2× the inlier bitwidth in MX-FP, paid for by pruning the least important weights **in the same micro-block, chosen by Hessian rather than by adjacency**. |
| **OliVe** | 2023 | *(already in the figure)* **Paired encoding.** Steals one codepoint from a 4-bit integer to mark "my neighbour is an outlier", prunes that neighbour, and stores the outlier in the freed 4 bits. |
| **Tender** | 2024 | **Discrete in-block scale factors.** Activation channels binned into geometric bands by absolute maximum, so outlier channels get their own scale on a plain symmetric-INT systolic array. |
| **SingularBit** | 2026 | **Decomposition: SVD splits.** Precision allocated by rank in both weight matrices and attention distributions — the leaf's low-rank clause, done for KV as well as W. |
| **Oaken** | 2025 | **Streaming variant: KV-cache quantization.** Three magnitude groups per token — inliers INT4, large *and* small outliers INT5 — with the outliers' spare bits packed into the zeroed dense slots they leave behind, landing every sparse entry on 8 aligned bits. |
| **Omni-LUT** | 2026 | KV-cache again, by sensitivity: extra bit-planes on Query-energy-weighted sensitive channels, per-channel offline for Keys and per-token online for Values. |
| **OASIS** | 2026 | The top and bottom 0.5% handled outside the codebook, which is what makes a dual-side 4-bit K-Means table survivable. |
| **AQuant** | 2026 | Base + delta: the outlier magnitude is absorbed into the base, so only the residual is quantized. |
| **Ecco** | 2025 | Non-uniform k-means patterns plus Huffman coding — the codebook-plus-wide-outliers shape of GOBO, moved into the GPU L2 cache. |
| **DRQ** | 2020 | The pre-LLM ancestor of the whole leaf: sensitive **regions** promoted to INT8 at runtime, everything else INT4. |

### Bit splitting (§4.5)

> Decomposing the multiply along the bit dimension at fixed width: FIGLUT (table of activation partial sums), Transitive Array (partial-product deduplication);
> the bit-serial/bit-slice ancestry and the batch-size crossover.

**⊕ Entered from ISCA**

| Paper | Year | What it contributes to this leaf |
|---|---|---|
| **TransitiveArray** | 2025 | *(already in the figure)* **Partial-product deduplication.** Bit-slices an ordinary INT4/INT8 group-wise checkpoint into binary matrices, observes that one binary row's partial sum is a **prefix** of another's, orders rows by Hamming weight over a Hasse graph, and computes each row with a single addition onto a reused prefix — multiplication-free. |
| **BitFusion** | 2018 | The *bit-serial/bit-slice ancestry* the leaf points back to: decomposition along the bit dimension as a composition mechanism, seven years before the LLM framing. |
| **LUTTensorCore** | 2025 | Bit-serial on the LUT side: `W_INT1–4` against an elongated `M2 N64 K4` tile, with the table halved by reinterpreting weight bits `{0,1}→{−1,1}` for symmetry. |
| **Omni-LUT** | 2026 | Binary-coding bit-planes applied to the **KV cache**, so attention's activation×activation GEMM becomes structurally identical to activation×weight GEMM and runs on the same datapath. |

---

## Stage 3 — Paradigm
*the mapping itself* (§5)

### The analytic ceiling (§5.1)

> Bounded design space (bit-field split, block size, one or two scales) against an unbounded distribution; MSE-vs-bitwidth flattening near 4 bits.

**⊕ Entered from ISCA**

| Paper | Year | What it contributes to this leaf |
|---|---|---|
| **Mokey** | 2022 | The argument for leaving the analytic grid: an out-of-the-box FP transformer needs a **dictionary of representative centroids**, not a narrower uniform type, and no fine-tuning is available to rescue one. |
| **MicroScopiQ** | 2025 | The ceiling measured rather than asserted — 2.36 effective bits, and the accounting that gets there. |
| **MXFFP** | 2026 | The bounded design space enumerated exactly: two presets, one bit, and an argument about which of the two the data wants. |

### Vector quantization (§5.2)

> W → codebook C + index matrix Q, value = C[i]; K-means grouping, product quantization, residual quantization, AQLM;
> honest bit accounting (index bits + amortized codebook bits + codebook precision).

**⊕ Entered from ISCA**

| Paper | Year | What it contributes to this leaf |
|---|---|---|
| **Mokey** | 2022 | *(already in the figure, §5.6)* Every value a 4-bit index into a dictionary of 16-bit fixed-point centroids, **with no fine-tuning** — and the centroids chosen to also fit an exponential curve, so most MACs become narrow 3-bit additions. |
| **EVA** | 2026 | *(already in the figure, §5.4)* VQ built for decoding: the codebook is the thing you compute against, not the thing you decode from. |
| **OASIS** | 2026 | **Dual-side** VQ — both weights *and* activations to 4-bit learned K-Means codebooks, which makes the table the **Cartesian product of the two**: 256 static entries, computed offline, independent of reduction length. |
| **Omni-LUT** | 2026 | Hardware-aware codebook construction, with the scaling folded **into** the table rather than applied after it. |
| **Ecco** | 2025 | Group-wise non-uniform quantization against **pre-defined shared** k-means patterns — codebook cost amortized to zero by not learning one per tensor — then Huffman coded, with a parallel decoder to make it L2-rate. |

### Lattice and higher-dimensional (§5.3)

> QTIP, QuIP#, E8-lattice and sphere-packing codebooks decodable without an explicit table; the sub-2-bit frontier.

*[add papers]* — **no ISCA paper in the analysed set belongs here.** The sub-2-bit
lattice line is an algorithms-venue thread; the nearest ISCA work is
**SingularBit** (1–2 bit weights), but it gets there by rank allocation, not by a
lattice, and is entered under §4.2 and §4.4 instead. This leaf's `\fillhere`
should stay standing until another venue's owner fills it.

### Lookup-First vs. Multiply-First (§5.4)

> LUF: resolve indices through the codebook, materialize weights, feed a conventional MXU --- memory-bound and array-idle at M=1.
> MUF: transform activations against the codebook first, then gather and accumulate --- restores density at M=1.
> Implementations and baselines: EVA, Marlin, Machete, EXL3, CodeGEMM, AQLM kernels; report the batch-size crossover.

**⊕ Entered from ISCA**

| Paper | Year | Side of the split |
|---|---|---|
| **EVA** | 2026 | *(already in the figure)* **MUF, and the paper that names the inversion.** "Instead of reconstructing weights from indices and doing GEMV, compute dot products directly between the input vector and the weight codebook" — which turns decoding from GEMV into **GEMM** — then structured lookups from an intermediate output buffer, bank-conflict-free by construction. |
| **OASIS** | 2026 | **MUF taken to both sides.** GEMM becomes concatenate indices, count occurrences, take a weighted sum of table entries — so the table is independent of reduction length and the crossover moves again. |
| **LUTTensorCore** | 2025 | **LUF made to pay** by moving the table's cost into software: precompute fused into the previous operator, table halved by symmetry, table entries themselves quantized to INT8. |
| **Omni-LUT** | 2026 | Applies the split to attention rather than to the weight GEMM, which is where the M=1 argument is strongest. |

### LUT as a hardware primitive (§5.5)

> LUT-GEMM and the FIGLUT line vs. lookup as the definition of the format; NVIDIA Rubin 3-bit LUT (8-entry FP8 codebook per 512-weight tile, inline in the MMA);
> table placement, port pressure and contention, serial lookup-to-multiply dependence.

**⊕ Entered from ISCA**

| Paper | Year | What it contributes to this leaf |
|---|---|---|
| **LUTTensorCore** | 2025 | The table treated as a cost to be budgeted, not a free resource: fused precompute, halved table, INT8 entries, and a tile shape (`M2 N64 K4`) chosen to match. |
| **EVA** | 2026 | *Table placement, port pressure and contention*, answered structurally: lookups are issued from an intermediate output buffer so **bank conflicts are eliminated by construction** rather than scheduled around. |
| **OASIS** | 2026 | A 256-entry static table, computed offline and independent of reduction length — the strongest available answer to the *serial lookup-to-multiply dependence*. |
| **Omni-LUT** | 2026 | A LUT accelerator whose codebook is chosen hardware-aware, with scaling folded into the table so no post-lookup multiply is needed. |
| **FATE** | 2025 | The other sense of LUT, and worth keeping distinct: **physical FPGA LUTs** as the multiplier for low-bit dimensions. The table is logic, not a numeric codebook — the distinction §5.5 draws in its first clause. |
| **Phi** | 2025 | A third sense, also worth keeping distinct: the table holds **offline-precomputed pattern-weight products** for k-means binary patterns, so a pattern index at runtime is a memory read rather than arithmetic. The decomposition is **exact** — the table stores products, not quantized values — and the cost is the leaf's *port pressure* clause in numbers: only **27.73%** of the precomputed products are used per tile, and DRAM energy is conceded not to fall. |

### Pre-LLM roots and current limits (§5.6--5.7)

> Roots: Cambricon-S, OLAccel, GOBO, Mokey, RapidNN, ANNA. Limits: FP16 codebooks make it compression not a compute format; decode-phase only; prefill unserved.

**⊕ Entered from ISCA**

| Paper | Year | Root or limit |
|---|---|---|
| **OLAccel** | 2018 | *(already in the figure)* Root. |
| **Mokey** | 2022 | *(already in the figure)* Root — and a direct instance of the first limit: the centroids are **16-bit fixed point**, so without the exponential-curve trick it would be compression, not a compute format. |
| **SmartExchange** | 2020 | Root, and one the figure does not list: `W = B · Ce`, a large sparse coefficient matrix times a small basis whose non-zero entries are all **powers of two** — sparsification, decomposition and quantization unified in one representation. |
| **BitFusion** | 2018 | Root for the bit-flexible line rather than the codebook line. |
| **DRQ** | 2020 | Root for outlier handling by region. |
| **EVA** | 2026 | **The "decode-phase only / prefill unserved" limit, confirmed by its own design:** the architecture accelerates decoding and *still runs conventional prefill*. |
| **OASIS** | 2026 | The first ISCA attempt at the limit rather than around it — dual-side quantization is what makes the prefill GEMM tractable, and it is the direct answer to "prefill unserved". |

---

## Hardware substrates
*same format, different cost* (§6)

### Fixed low-bitwidth datapaths (§6.1)

> Systolic arrays and fixed-width MAC arrays.

**⊕ Entered from ISCA**

| Paper | Year | Note |
|---|---|---|
| **Tender** | 2024 | Its whole point: outlier isolation on a **plain symmetric-INT systolic array**, with no datapath change — the scale constraint does the work. |
| **OLAccel** | 2018 | A fixed 4-bit MAC array, with the exceptions bolted on beside it. |
| **TPUv4i** | 2021 | The shipped fixed-width MXU, and the accounting for what int8 does and does not buy on one. |
| **AQB8** | 2025 | Fixed INT8 offsets against an FP32 anchor, in a ray-tracing datapath. |

### Variable bitwidth (§6.2)

> Bit-flexible, bit-serial and bit-slice substrates.

**⊕ Entered from ISCA**

| Paper | Year | Note |
|---|---|---|
| **BitFusion** | 2018 | Bit-flexible; the substrate the rest answer to. |
| **XtraMAC** | 2026 | Bit-flexible at constant latency and II = 1 across every datatype. |
| **UniCore** | 2026 | Bit-width scalable by uniform adder slices — linear, not quadratic, composition cost. |
| **RaPiD** | 2021 | Four precisions in one fabricated datapath. |
| **SamsungNPU** | 2021 | Re-configurable MAC array, INT8/INT16, shipped. |
| **DRQ** | 2020 | Variable-**speed** rather than variable-width: two precisions, one array, balanced occupancy. |
| **LightNobel** | 2025 | Multi-precision reconfigurable MPU plus a versatile vector unit. |
| **TransitiveArray** | 2025 | Bit-slice, with the slices deduplicated against each other. |
| **LUTTensorCore** | 2025 | Bit-serial, with the partial sums tabled instead of accumulated. |

### LUT engines and codebook buffers (§6.3)

> Lookup units, table storage, codebook buffers adjacent to the PE array.

**⊕ Entered from ISCA**

| Paper | Year | Note |
|---|---|---|
| **LUTTensorCore** | 2025 | The lookup unit as a tensor-core-class primitive, with the table budgeted in software. |
| **EVA** | 2026 | Codebook buffer placed so that structured lookups cannot conflict. |
| **OASIS** | 2026 | A 256-entry static table — small enough to sit adjacent to the array and stay there. |
| **Omni-LUT** | 2026 | Table storage sized by a hardware-aware codebook rather than by the algorithm's preference. |
| **Mokey** | 2022 | The early instance: a centroid dictionary beside the datapath, usable as a pure memory-compression front-end for another accelerator. |
| **Ecco** | 2025 | The table in the **cache** rather than beside the PE array, with a parallel Huffman decoder to make that placement viable. |
| **Phi** | 2025 | A pattern-weight-product buffer, 128 patterns per K tile, fed by a prefetcher that reads the next layer's pattern indices ahead — the table storage, not the arithmetic, is what this design has to size. |

### CIM / PIM / NDP (§6.4)

> Bitwidth forced by ADC resolution rather than chosen, so most of Stage 1's design space does not exist here.

**⊕ Entered from ISCA**

| Paper | Year | Note |
|---|---|---|
| **RAELLA** | 2023 | The leaf's claim, inverted into a method: adapt the **arithmetic** so analog values are near zero and therefore cheap to digitize — Center+Offset encoding, adaptive weight slicing per layer, dynamic input slicing with speculation and recovery. Low-resolution ADCs then suffice, with no retraining. |
| **P3-LLM** | 2026 | An integrated NPU-PIM edge accelerator, with PIM compute units co-designed for the chosen formats under an iso-area DRAM constraint. |
| **NDPLowBitFP** | 2026 | NDP brought into the low-bit FP era: FlexQ-NDP compiler, scale-value interleaved layout, dequantization hiding, pruned compilation-space search. |

### FPGA and commodity GPU (§6.5)

> Different constraints; do not pool these numbers with ASIC results.

**⊕ Entered from ISCA** — and the leaf's warning applies to all six

| Paper | Year | Substrate |
|---|---|---|
| **FATE** | 2025 | FPGA. Important dimensions on DSPs, unimportant ones as **logic on LUTs**, where the multiply stops being arithmetic. |
| **XtraMAC** | 2026 | FPGA — evaluated on an AMD Xilinx U55c. |
| **Ecco** | 2025 | Commodity GPU, at the L2 cache. |
| **LoKA** | 2026 | Commodity GPU, as a PyTorch integration in production. |
| **JPEG-ACT** | 2020 | GPU training, with a hardware assist. |
| **Gist** | 2018 | GPU training, in software only. |

### Measured silicon (§6.6)

> JSSC / ISSCC parts and commercial accelerators --- the only place energy numbers are directly comparable.

**⊕ Entered from ISCA** — ISCA's industry track is the other place, and these are its entries

| Paper | Year | What is measured |
|---|---|---|
| **RaPiD** | 2021 | A fabricated 7 nm EUV chip, 36 mm²; the performance model is calibrated to within **1% of chip measurements** before being projected to a 4-chip system. |
| **TPUv4i** | 2021 | A shipped Google product, reported with ten lessons across three generations. |
| **SamsungNPU** | 2021 | A shipped 5 nm flagship-SoC NPU, with a lessons-learned section. |
| **ENEC** | 2026 | Ascend NPUs, with six Huawei co-authors — the vendor's own constraint (branch-free SIMD) is what shapes the method. |
| **LoKA** | 2026 | Meta production recommendation serving; the numbers are fleet numbers, not simulator numbers. |

---

## Workloads and lifecycle (§7--8)

### Workloads (§7)

> CNN (settled --- compress); Transformer / ViT; **LLM inference (the focus)**; KV cache; diffusion and video;
> others: GNN, NeRF, recommendation, SNN, point cloud, vector search.

**⊕ Entered from ISCA**

| Workload | Papers |
|---|---|
| CNN | **BitFusion** (2018), **OLAccel** (2018), **DRQ** (2020), **SmartExchange** (2020) |
| Transformer / ViT | **Mokey** (2022), **AQuant** (2026, VLM) |
| **LLM inference (the focus)** | **OliVe** (2023), **Tender** (2024), **MicroScopiQ** (2025), **LUTTensorCore** (2025), **TransitiveArray** (2025), **EVA** (2026), **OASIS** (2026), **Omni-LUT** (2026), **UniCore** (2026), **XtraMAC** (2026), **SingularBit** (2026), **P3-LLM** (2026), **NDPLowBitFP** (2026), **MXFFP** (2026), **ENEC** (2026) |
| KV cache | **Ecco** (2025), **Oaken** (2025), **Omni-LUT** (2026), **SingularBit** (2026), **P3-LLM** (2026) |
| diffusion and video | *[add papers]* — none in the ISCA set |
| others | **AQB8** (2025, ray tracing / BVH), **FATE** (2025, hyperdimensional computing), **LightNobel** (2025, protein structure prediction), **LoKA** (2026, recommendation) |
| SNN (named in `others`) | **Phi** (2025), **ELSA** (2026, *may not fit* — out of the corpus since 2026-10-02) — both ISCA, both restored 2026-10-01. See [`QuantArchSurvey/survey/snn.md`](../QuantArchSurvey/survey/snn.md) for the open question of whether the Stage axis applies to them |

The "others" row is the one to watch: four of the last two years' ISCA
quantization papers target a workload the taxonomy's `others` list does not
name. Ray tracing, HDC and protein structure prediction are each a first.

### Lifecycle (§8)

> PTQ; QAT; low-precision training; PEFT --- framed as deployment constraints rather than accuracy results.

**⊕ Entered from ISCA**

| Stage | Papers |
|---|---|
| PTQ | **Mokey** (2022, explicitly no fine-tuning), **RAELLA** (2023, no retraining), **OliVe** (2023), **Tender** (2024), **MicroScopiQ** (2025), **Oaken** (2025, thresholds profiled offline), **MXFFP** (2026, offline MSE for weights) |
| QAT | **OASIS** (2026, learned K-Means codebooks), **FATE** (2025, importance measure trained in) |
| low-precision training | **Gist** (2018), **JPEG-ACT** (2020), **RaPiD** (2021), **LoKA** (2026) |
| PEFT | *[add papers]* — none in the ISCA set |

---

## Cross-cutting analysis and open problems (§9--10)

### Comparative analysis (§9)

> Area/energy at a fixed accuracy target across the three stages; scale-factor and codebook accounting normalized across papers;
> outlier mechanisms per point of accuracy recovered; flexibility-vs-throughput reversal in the LLM era; evaluation-methodology audit.

**⊕ Entered from ISCA**

| Paper | Year | What it supplies to the analysis |
|---|---|---|
| **TPUv4i** | 2021 | The *flexibility-vs-throughput reversal*, stated from the vendor side before the LLM era made it general: int8 at the same peak as bf16 means flexibility was bought and throughput was not. |
| **MicroScopiQ** | 2025 | *Codebook and scale-factor accounting normalized* — 2.36 **effective** bits, counted rather than quoted. |
| **LoKA** | 2026 | An *evaluation-methodology* contribution in its own right: statistically grounded online benchmarking instead of a static accuracy table. |
| **RaPiD** | 2021 | The calibration discipline the audit should ask for — a model held to within 1% of measured silicon before any projection. |
| **Oaken** | 2025 | *Outlier mechanism per point of accuracy recovered*, made explicit by moving the cost offline and pricing what remains. |

### Open problems (§10)

> Where the table lives and who pays for contention; codebooks vs. sparsity; dual-side VQ and on-the-fly quantization for prefill;
> computing directly on an index matrix; KV-cache VQ; training below 8 bits; format proliferation against ISA stability; standardizing learned formats.

**⊕ Entered from ISCA** — the ISCA set touches six of the eight

| Open problem | Papers that touch it |
|---|---|
| Where the table lives; who pays for contention | **LUTTensorCore** (2025, table cost moved into software), **EVA** (2026, conflicts removed by construction), **Ecco** (2025, table in the L2) |
| Codebooks vs. sparsity | **MicroScopiQ** (2025, prunes to pay for outlier bits), **SingularBit** (2026, rank instead of either), **SmartExchange** (2020, the pre-LLM version of the trade), **Phi** (2025, k-means patterns used to *manufacture* sparsity — the Level-2 residual is 96.80% sparse against ~83% native) |
| Dual-side VQ and on-the-fly quantization for prefill | **OASIS** (2026) — the only ISCA paper that attempts it; **EVA** (2026) states the gap by leaving prefill conventional |
| Computing directly on an index matrix | **OASIS** (2026, concatenate-count-weighted-sum), **TransitiveArray** (2025, prefix reuse over bit-planes) |
| KV-cache VQ | **Omni-LUT** (2026), **Ecco** (2025), **Oaken** (2025) |
| Training below 8 bits | **RaPiD** (2021, INT4/INT2 in a training datapath), **LoKA** (2026, FP8 in production) |
| Format proliferation against ISA stability | **UniCore** (2026), **XtraMAC** (2026), **MXFFP** (2026) — all three argue that one primitive should absorb the proliferation |
| Standardizing learned formats | *[add papers]* — none in the ISCA set. The closest is **MXFFP** (2026), which standardizes *within* OCP MX rather than proposing a new standard. |

---

## What the ISCA fill says about the figure

Three observations worth carrying back into `taxonomy.tex`:

1. **§5.3 (lattice) has no ISCA paper at all,** and §7's `diffusion and video`,
   §8's `PEFT` and §10's `standardizing learned formats` are likewise empty. Four
   leaves that the ISCA corpus cannot fill — which is information about the venue,
   not a gap in the reading.

2. **The `others` workload row is carrying too much.** AQB8 (ray tracing), FATE
   (HDC) and LightNobel (protein structure) are three distinct non-LLM workloads
   from a single year, each with a real quantization contribution. The row names
   none of them.

3. **§4.2 and §6.2 draw the same papers.** BitFusion, XtraMAC, UniCore, RaPiD,
   SamsungNPU, DRQ and LightNobel appear in both, because "mixed precision" as a
   design choice and "variable bitwidth" as a substrate are the same nine
   papers seen twice. Worth deciding whether the figure wants that duplication or
   a cross-reference.

4. **The two spiking papers enter through encoding and lookup, never through format.**
   ELSA lands in §3.1 and §4.2 (a temporal code whose length is the precision), Phi in
   §5.5 and §6.3 (a table of precomputed products). Neither touches §3.2–§3.3 or §4.1. That
   is the pattern `survey/snn.md`'s first question predicts if the spike is a *re-coding* of
   an ordinary number rather than a number of its own.
