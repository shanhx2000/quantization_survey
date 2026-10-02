# LUT Tensor Core: A Software-Hardware Co-Design for LUT-Based Low-Bit LLM Inference

**Venue / Year:** ISCA 2025 · **Link:** https://arxiv.org/abs/2408.06003 · **Reader:** Haoxuan · **Date:** 2026-09-03

## Tags

| | |
|---|---|
| **Level** | `ALGO+SYS+ARCH` |
| **Q-oriented** | `Q-ORIENTED` |
| **Data type** | `LUT` `INT1` `INT2` `INT4` `INT8` `FP16` `FP8` `MIXED` |
| **Generation** | `G3` (weight-only + codebook threads) |
| **Stage type** | `S2T5` · `S3T1a` |
| **Optimization** | LUT-GEMM · mpGEMM · bit-serial · table quantization · weight reinterpretation · operator fusion · elongated tiling · LMMA |

## Stage-type tags

**`S2T5` · `S3T1a`** (the **Stage type** row in Tags) — most-matched first. Bit-serial low-bit weights against a K=4 activation table (`S2T5`), where the table holds precomputed, INT8-quantized products (`S3T1a`).

*Tag form `S{stage}T{type}`, vocabulary from `survey/stage2.md` and `survey/stage3.md`. Added 2026-10-02 (ISCA Stage-type batch 1).*

## 1. One-line summary

LUT-based mpGEMM for W-IntX model. Four optimizations, each measured: precompute fused into
the preceding op (overhead 16.5%/24.4% → 2.6%/2.5%); weight reinterpretation {0,1}→{−1,1}
halves the table (1.32× compute intensity over UNPU); negation circuit elimination (→1.35×);
DFG transform + kernel fusion (→1.44×). Plus elongated `M2 N64 K4` tiling. ISA (LMMA) and
compiler supports. Net **4×–6×** power and area over a MAC Tensor Core at 1-bit weights.

## 2. Data type

**Formats.** `W_INT1/2/4` × `A_FP16/FP8/INT16/INT8`. Weight-only. Activations stay ≥8-bit.

**Table quantization.** Precomputed table *entries* quantized to INT8 at runtime — the
products, not the activations. Activations stay FP16 and are quantized only in the sense that
the dot products formed from them are. Finer than operand-side quantization and only reachable
after the product exists.

**Granularity.** Weight vector K=4. The weight scaling factor granularity impacts the table reusability — s_w factors out of the K-group in Eq. 3, so it must be constant across those 4 weights or the shared table is wrong. Never stated by the paper. Activation vector K=4, table quantized as a unit.

**Escape hatch.** Activations never below 8 bits. The headline 61.55 TFLOPs/mm² is measured
"No Psum" — accumulator cost excluded. Attention and KV cache out of scope.

**Retraining.** Hardware is quantizer-agnostic, but every evaluated model is QAT or
from-scratch (BitDistiller, BitNet b1.58). Not reachable from a stock checkpoint; the paper
concedes PTQ is near-lossless only at 4-bit.

## 3. Optimization

Precompute redundancy: one table recomputed 3072× across units → split into an independent
operator, broadcast once. Fuse with the preceding element-wise op to hide the memory traffic.

Table storage: `{0,1}→{−1,1}` remap makes `LUT[W] = −LUT[~W]`, so half the entries are
redundant. Done offline on static weights, which also deletes the per-unit negation circuit.
Halves storage, MUX width and broadcast together.

Tiling: table size = `M × 2^(K−1) × LUT_BIT`, so K must stay small while N sets how many MUXes
reuse each entry → elongated `M2 N64 K4`, against A100's `M8 N4 K16` at the same 512 array.

Integration is the cost: replaces the Tensor Core, adds an LMMA instruction. 

## 4. Results

| | |
|---|---|
| Baseline | MAC- and ADD-based Tensor Cores (authors' Verilog); UNPU (re-implemented, no public code); LUT-GEMM software; A100 / H100 Tensor Cores |
| Models / datasets | LLAMA2-7B/13B/70B, OPT-175B, BLOOM-176B, BitNet b1.58 3B; WikiText2 PPL, MMLU, zero-shot |
| Accuracy delta | Table quantization is ~free: `W_INT2 A_FP16` 7.68 PPL → `A_LUT_INT8` 7.69. The INT2 quantization itself costs 5.47 → 7.68 vs FP16 |
| Speedup | **4×–6× power and area** vs MAC TC at 1-bit weights (post-synthesis). 1.42× GEMV / 72.2× GEMM vs LUT-GEMM. 1.44× vs UNPU. End-to-end up to 8.2× at 38.3% of MAC TC area |
| Energy / area | DP4 `W_INT1 A_FP16`: 61.55 TFLOPs/mm² vs MAC `W_FP16A_FP16` 3.39. Smallest area×power in 11 of 12 precision pairs |
| Technology node | TSMC 28 nm, 1 GHz, Synopsys DC medium effort |
| Evidence level | **post-synthesis** (PPA) / **cycle-level simulator** Accel-Sim (kernel) / **authors' analytical tile simulator** (end-to-end + all of Table 1). Do not pool |

**Is the comparison fair?** The post-synthesis comparison is fair — same authors, same
Verilog flow, same node, same array size, 12 precision pairs. Cite 4×–6×.

## 5. Comment

**Admitted limits.** Inference only; no long-context attention or KV cache; `W_FP` is a sketch;
Blackwell's native mpGEMM may erode the premise.


## 6. Claude notes

*Suggestions from the reading agent. **Strip this section before copying into
`QuantArchSurvey/venues/ISCA/notes/`.***

- **§4 — consider excluding Table 1 explicitly.** Its 5.51× / 20.9× / 11.2× / 2.02× come from
  A100/H100 baselines the authors normalized from 7nm/4nm down to 28nm, and the rows change
  models (LLAMA-3B vs BitNet b1.58 3B). These are the numbers a survey reader is most likely
  to lift.
- **§5 — the eager/lazy pairing is the highest-value item here.** This paper precomputes all
  2^(K−1) entries and spends its whole software contribution making that cheap;
  `TransitiveArray` materialises only entries that occur, one add each. Same problem, opposite
  ends, no mutual citation. Strongest pairing in the corpus for survey §5.6.
- **Cross-paper.** Both LUT papers need the weight scale constant across the K-group, and
  **neither states its scale granularity.** That silence is itself a survey finding.
- **§5 — best citation for**: why weight-only quantization creates a *hardware* problem
  (mpGEMM has no native support, so dequantization eats the gain). Cleanest statement of it in
  the corpus.
