# Transitive Array: An Efficient GEMM Accelerator with Result Reuse

**Venue / Year:** ISCA 2025 · **Link:** https://arxiv.org/abs/2504.16339 (DOI 10.1145/3695053.3731043) · **Reader:** Haoxuan · **Date:** 2026-09-03

## Tags

| | |
|---|---|
| **Level** | `ARCH` |
| **Q-oriented** | `Q-ORIENTED` |
| **Data type** | `LUT` `INT4` `INT8` `MIXED` |
| **Generation** | `G3` (weight-only + codebook threads) |
| **Stage type** | `S2T5` · `S3T1a` |
| **Optimization** | LUT-GEMM · result reuse · bit-slice · Hasse-graph scheduling · multiplication-free · group-wise scaling (g=128) |

## Stage-type tags

**`S2T5` · `S3T1a`** (the **Stage type** row in Tags) — most-matched first. Bit-sliced weights with prefix partial-sum reuse over a Hasse graph (`S2T5`), pushed until the GEMM is a lookup into a table of products (`S3T1a`).

*Tag form `S{stage}T{type}`, vocabulary from `survey/stage2.md` and `survey/stage3.md`. Added 2026-10-02 (ISCA Stage-type batch 1).*

## 1. One-line summary

Bit-slices an INT4/INT8 weight matrix into 8-bit binary rows and treats each row as an
**index into a 256-entry table of partial sums over the activation group** — the table being
built lazily by one addition per new entry, in Hamming order over a Hasse graph — so that
GEMM becomes table lookup plus at most one add, giving a **multiplication-free** accelerator
that removes up to 87.5 % of the additions in binary GEMM at no accuracy cost beyond the
inherited quantization.

## 2. Data type

**Formats.** `W4A8` and `W8A8`, plain integer both sides. Bit-slice processing on weights. The design can be extended to arbitrary activation precisions if the lut/adder bit-width modified.  

Partial sums stored in table for later lookup. This table is constructed lazily. 

**Granularity.** Elementwise, since it's int8. Scaling factor should be no finer than vector-wise to ensure bit-slice working with T=8bit. 

**Escape hatch.** Attention stays FP16 in the accuracy table (§5.4). 

**Retraining.** PTQ-only (QServe / MQBench, no QAT). 

## 3. Optimization

GEMM -> Sparse LUT construction + Lookups.

Sparse construction reduces computation, and fixed path (hamming) avoids a very complex scheduler. 

Tile size exploration to decide what's a number of vector length (log2(Tiling Row Size)) gives the lowest table density (namely more sparsity) while the cost is also low. 

## 4. Results

| | |
|---|---|
| Baseline | BitFusion, ANT (MICRO'22), OliVe (ISCA'23), Tender (ISCA'24), "BitVert" (= BBS, arXiv:2409.05227)  |
| Models / datasets | LLaMA-1 (7/13/30/65B), LLaMA-2 (7/13B), LLaMA-3 (8B) on Wikitext (PPL); ResNet-18 on ImageNet |
| Accuracy delta | W4A8: +0.14 PPL vs FP16 on LLaMA-1-7B; **+0.45 on LLaMA-3-8B** (6.59 vs 6.14). W8A8: +0.07 / +0.25 |
| Speedup | FC, iso-accuracy (TA-W4A8 vs 8-bit baselines): **4.91× ANT, 7.46× OliVe, 3.97× BitVert**. Iso-precision (TA-W8A8): 2.47× / 3.75× / 1.99×. Attention: 1.54× over ANT. ResNet-18: 4.26× BitFusion, 2.21× ANT |
| Energy / area | Energy efficiency 1.65× / 2.31× / 1.65×. Core **0.443 mm²** vs 0.473–0.491 mm²; 480 KB buffer vs 512/608 KB |
| Technology node | 28 nm, 500 MHz, ARM standard cells |
| Evidence level | **post-synthesis** (Synopsys DC) area/power, Cacti 7.0 buffers, **cycle-level simulator** for performance. No silicon |

**Is the comparison fair?** Fair. Iso-node and iso-area yes; iso-algorithm no.


## 5. Comment

.
## 6. Claude notes

*Suggestions from the reading agent. **Strip this section before copying into
`QuantArchSurvey/venues/ISCA/notes/`.***

- **§5 is empty.** The two items I'd put there: the **eager/lazy** contrast with
  `LUTTensorCore` (it precomputes the whole table; this builds only the entries that occur),
  and **why G3** — codebook + weight-only threads both, though the paper never uses the word
  "lookup" or "codebook" in 15 pages.
- **§4 — two frames worth naming.** Every LLaMA number is **one Transformer block at prefill
  2048**; decode is never evaluated. And only TransArray and ANT got group-wise quantization,
  so 7.46× over OliVe is architecture *plus* algorithm.
- **Best citation for**: that a lookup table need not be built up front — it can be
  constructed by the GEMM itself, one addition per entry, in popcount order.
