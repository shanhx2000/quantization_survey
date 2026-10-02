# Omni-LUT: Energy-Efficient LUT-based Accelerator with Hardware-Aware KV Cache Quantization

**Venue / Year:** ISCA 2026 · **Link:** no public URL (proceedings only; DOI 10.1109/ISCA66397.2026.00037) · **Reader:** Haoxuan · **Date:** 2026-09-03

## Tags

| | |
|---|---|
| **Level** | `ALGO+ARCH` |
| **Q-oriented** | `Q-ORIENTED` |
| **Data type** | `LUT` `INT4` `INT3` `FP16` `MIXED` |
| **Generation** | `G3` (codebook + KV-cache threads) |
| **Stage type** | `S3T1a` · `S2T5` |
| **Optimization** | LUT-GEMM · KV cache · BCQ · AA-GEMM · scale-aware LUT · sensitivity-based bit allocation · hybrid stationary · phase-adaptive systolic |

## Stage-type tags

**`S3T1a` · `S2T5`** (the **Stage type** row in Tags) — most-matched first. Q, or the post-softmax scores, build a table of partial sums that the KV bit-planes index, so attention runs on the same LUT datapath as A×W (`S3T1a`); weights and KV are stored as ±1 bit-planes (BCQ), with cost linear in bit-planes (`S2T5`).

*Tag form `S{stage}T{type}`, vocabulary from `survey/stage2.md` and `survey/stage3.md`. Added 2026-10-02 (ISCA Stage-type batch 2).*

## 1. One-line summary

Quantizes the **KV cache** to 3–4-bit binary-coding bit-planes — per-channel offline for Keys
with extra bit-planes on Query-energy-weighted sensitive channels, per-token online for Values
— so attention's activation×activation GEMM becomes structurally identical to
activation×weight GEMM and runs on the same LUT datapath. Scaling is folded **into** table
generation so the accuracy-optimal row-wise direction survives. 1.25×–1.91× energy efficiency
over a LUT accelerator that must fall back to floating point for attention.

## 2. Data type

**Formats.** `W4A16KV4` and `W4A16KV3`. Weights 4-bit BCQ, KV 3–4-bit BCQ, **activations
FP16**. 
BCQ = decompose into ±1 bit-planes × high-precision scales. Non-uniform, index-coded.  

**The two attention GEMMs.** `QK^T`: Q builds the LUT, K indexes it. `Attn×V`: post-softmax
scores build the LUT, V indexes it. Cost is linear in bit-planes.

**Quantization is done on-chip, once per generated token** (BQU), so it amortizes over the
whole remaining decode. Key path: scales offline, bit-planes online. Value path: both online.
Costs 2.63% area, 0.25% energy.


**Granularity — per vector/channel/token.** Keys per-channel, offline-calibrated
(per-channel stats are global, can't be estimated during autoregressive decode). Values
per-token, online (token-dependent, no stable channel structure). Weights row-wise. All three
must be row-wise in A×W, which is exactly what the LGU exists to permit.

**Scaling factor group size.** No number given — the paper states axes, not sizes. Per
quantized vector the BEA takes a zero-point plus q scaling factors, one per bit-plane.

- **K:** `zp_k,c` + q × `α_i,c` **per channel**, offline-calibrated, shared across **all T
  tokens**. 
- **V:** `zp_v` + q × `α_i = δ_v·{4,2,1,0.5}` **per token**, from TSE min/max, shared across
  **all d channels**. 
Both are per-element along the reduction dimension, shared along the orthogonal one. That is
why scaling must live inside LUT generation: a 4-element group needs 4 distinct scales and one
post-lookup scale cannot supply them.

**No sub-grouping on the shared axis** — unlike KIVI's group-of-G. K scales are global over the
sequence, which is what forces offline calibration; V scales cover the full token vector.
AS-Bit then varies q per channel (K only): 25% of channels at high bits → 4.25 effective.

**Outliers — handled by granularity, not isolation.** No high-precision outlier path at all.
That's the claim: 4.25 effective Key bits vs KIVI/KVQuant/Oaken's 4.8–5.0 average, *because*
they spend bits on outlier isolation and this doesn't. Cleanest counter-example in the corpus
to the inlier/outlier-split orthodoxy.




## 3. Optimization

AW-GEMM scales O(T), AA-GEMM O(T²) in prefill; decode streams the whole KV cache per token →
LUT accelerators are accelerating the shrinking half.

Binarize KV → attention is LUT-shaped. Keys and Values need different schemes because their
distributions differ: Keys have stable per-channel outliers, Values don't.

AS-Bit: in `A = QK^T` the Key error is scaled by Query magnitude, so sensitivity = per-channel
MSE weighted by per-channel Query energy `E[Q²]`. Works because Q also has stable per-channel
structure. Sensitive channels get extra bit-planes → 4.25 effective bits.

Scale-aware LGU — the subtle enabler. FIGLUT scales *after* lookup, which only expresses
column-wise scaling; one post-lookup scale can't give four different scales to a 4-element
group. Accuracy wants row-wise for weights, Keys and Values alike. So scale *inside* table
generation: multiply each activation by its own factor before enumerating entries, and fold
zero-point compensation into the first bit-plane. Without this, AA-GEMM on a LUT costs
accuracy.

Phase-adaptive 32×4 array: WS for prefill (1.3× over OS), OS-V for decode (1.49×/1.68× over
OS/WS) — OS-V broadcasts one table vertically and gates the other LGUs. Half-LUT, 6 adders +
6 subtractors, runs in parallel with the array so table generation adds no stalls.

Overhead is small and honestly reported: BQU + LGU + control = ~5% of area, <1% of energy.

## 4. Results

| | |
|---|---|
| Baseline | FIGLUT (LUT, W4A16KV16), FPE (FP16 systolic, W4A16KV16), Tender (INT8 W8A8KV8); quantization baselines KIVI, KVQuant, Oaken, QServe, NVFP4, Atom, Tender |
| Models / datasets | OPT-1.3/6.7/13B, LLaMA2-7/13B, Mistral-7B, Mixtral-8x7B, LLaMA3-8B, Qwen3-8/14/30B-A3B (MHA, GQA, MoE); WikiText-2 PPL + zero-shot |
| Accuracy delta | **+0.17 avg PPL at KV4, +0.75 at KV3.** Effective Key bits **4.25** vs KIVI/KVQuant/Oaken 4.8–5.0. KV2 → PPL 9.96, not deployable |
| Speedup | Energy efficiency **1.25×–1.91× over FIGLUT** at equal peak throughput, long context. +85–110% over FPE at short/medium context. At 8192 output tokens: 59% / 54% / 46% energy reduction vs FPE / Tender / FIGLUT |
| Energy / area | Area efficiency 2.8×–3.9× TOPS/mm² over FPE. Area 0.53 mm² vs Tender 0.20 mm². PE array is 86% of area, 90% of energy |
| Technology node | **TSMC 7 nm**, 500 MHz — most of this corpus is 28 nm, do not compare absolutes |
| Evidence level | **post-synthesis** (DC + PrimeTime PX) with a simulator calibrated by **gate-level simulation** (VCS) on real inference tensors; DRAMPower LPDDR5 51.2 GB/s; FlashAttention tile 256. No silicon |

**Is the comparison fair?** Iso-node and iso-peak-throughput yes; iso-precision no; headline
quoted from its best operating point.

Methodology is careful — same node, same DRAM model, same VPU, same attention tiling across
all engines, and "equal peak throughput" is stated rather than implied.

But FIGLUT runs **KV16** against Omni-LUT's KV4, so a 4× KV traffic reduction is folded into
what reads as an architecture result. And 1.25×–1.91× is the **8192-token** number, where
FIGLUT is forced onto its FP backend; at 128/1024 tokens the margin is much smaller. The paper
says so in prose, the abstract does not.

Iso-accuracy against the KV baselines is the strongest part: fewer effective bits *and* no
outlier-isolation hardware.

## 5. Comment

**Pre- or post-RoPE is never stated.** Must be post-RoPE — K is consumed as bit-planes and
never reconstructed, and RoPE's rotation is relative so it can't fold into Q. But per-channel
Key outlier structure is a pre-RoPE property, which is what per-channel calibration rests on.



**§5.6, and it adds a second axis.** With LUT Tensor Core and OASIS the question was *when the
table is built* — eager per-tile, lazy per-tile, offline static. Omni-LUT is eager per-tile
like LUT Tensor Core, so it adds: **which operand you binarize.** Everyone binarizes weights,
which is why no prior LUT design can touch attention. Binarize the KV cache and attention
becomes LUT-shaped. A LUT accelerator's reach is set by which tensor you'll make binary.

**Pair with OASIS.** Both 2026, both LUT, opposite sides of the same shortfall. OASIS
quantizes both GEMM operands (W4A4) to make the table *static*; Omni-LUT leaves activations at
FP16 and quantizes KV to make *attention* reachable. Should be one paragraph, not two entries.

**Best citation for.** The O(T) vs O(T²) argument — why attention, not linear layers, is where
long-context effort belongs. And for the claim that outlier isolation is avoidable: 4.25
effective bits beats methods spending 4.8–5.0 with dedicated outlier paths.

**Why G3.** Codebook/lookup thread plus the KV-cache thread. Explicitly *against* the outlier
thread.

**Admitted limits.** KV2 not deployable; Tender-INT4 collapses (PPL 123.1) so the integer
baseline runs at INT8; Amdahl pushes the non-GEMM fraction up; BCQ calibration is expensive.

**Unadmitted.** The two contributions — BCQ-KV quantization and the phase-adaptive array — are
never disentangled. Fig. 10 isolates the dataflow choice and Table VII the overheads, but
nothing says how much of 1.25–1.91× comes from which.

## 6. Claude notes

*Suggestions from the reading agent. **Strip this section before copying into
`QuantArchSurvey/venues/ISCA/notes/`.***

- **Node mismatch is a corpus-wide hazard, not just this entry.** Omni-LUT is **7 nm**; OASIS,
  LUT Tensor Core and TransitiveArray are all **28 nm**. Any cross-paper TOPS/W or mm² table
  in the survey needs a node column, or it will be wrong.
- **Cross-entry disagreement worth chasing.** Omni-LUT's accuracy claim is directly against
  `Oaken`, which is also in our corpus: 4.25 effective KV bits without outlier isolation vs
  Oaken's 4.8–5.0 with it. Both are checkable. This is the sharpest head-to-head the KV
  cluster has.
- **`Tender` is used here as evidence against itself** — run at INT8 because its INT4 point
  gives PPL 123.1. Worth noting in Tender's own entry when you get to it.
- **§5.6 now has two axes**, not one: *when the table is built* (eager / lazy / offline) and
  *which operand is binary* (weights / KV / both). Four papers populate the grid; the
  weights+offline cell is empty, which may itself be a finding.
- **Open question — pre/post-RoPE.** Fig. 3's per-channel Key structure is the evidence for
  per-channel offline calibration, but the figure never labels the RoPE stage and the hardware
  appears to require post-RoPE quantization. Worth resolving before citing that figure; KVQuant
  quantizes pre-RoPE for exactly this reason.
- Minor: the paper's section numbering is disordered (§VI.B printed before §VI.A, §VIII before
  §VII). Cite section titles rather than numbers.
