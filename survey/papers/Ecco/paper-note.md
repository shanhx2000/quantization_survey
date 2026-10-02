# Ecco: Improving Memory Bandwidth and Capacity for LLMs via Entropy-aware Cache Compression

**Venue / Year:** ISCA 2025 (Tokyo) · **Link:** https://arxiv.org/abs/2505.06901 (DOI 10.1145/3695053.3731024) · **Reader:** Haoxuan · **Date:** 2026-09-10

## Tags

| | |
|---|---|
| **Level** | `ARCH` |
| **Q-oriented** | `Q-ORIENTED` |
| **Data type** | `VQ` `FP8` `INT8` `MIXED` |
| **Generation** | `G3` |
| **Stage type** | `S3T2` · `S2T4` |
| **Optimization** | GPU L2 · k-means codebook · Huffman · entropy coding · parallel decoder · clip-and-pad outliers · fixed-block variable-rate · KV cache |

## Stage-type tags

**`S3T2` · `S2T4`** (the **Stage type** row in Tags) — most-matched first. k-means patterns and Huffman codes in memory, decoded between L1 and L2 so the SMs compute in FP16 (`S3T2`); under-budget blocks re-store their largest values as FP8 outliers (`S2T4`).

*Tag form `S{stage}T{type}`, vocabulary from `survey/stage2.md` and `survey/stage3.md`. Added 2026-10-02 (ISCA Stage-type batch 1).*

## 1. One-line summary

Compresses weights and KV cache **4×** into fixed **64-byte blocks** by quantizing each group of
128 against one of **64 shared k-means patterns** and Huffman-coding the resulting 16-index
alphabet — clipping when a group codes badly and, when it codes well, **spending the slack
re-storing that group's largest values as FP8 outliers** — and makes the serial decode affordable
with **64 parallel decoders speculating at every bit offset, resolved by a 6-stage tree in 28
cycles**, placed between L1 and L2 where NVIDIA already puts its own compressor: **< 1% of an A100
die for ~4× capacity and 2.9× average over TensorRT FP16**, with **no reduction in arithmetic
precision at all**.

## 2. Data type

**Two schemes under one name.** **4×** (weights, KV) = shared k-means patterns + Huffman. **2×** (activations) = **plain uniform INT8, scale + zero point**, bit-interleaved. "Entropy-aware" covers only the 4× path.
**Per group of 128:** abs-max is the scale and takes **index 15**; the pattern supplies **15 centroids** → **16 indices**, Huffman-coded. **No group-level zero point** (unlike AWQ).
**Per tensor:** **S = 64** k-means patterns, **H = 4** Huffman codebooks each (16 codes), one FP16→FP8 scale that is a **power of two**. Naming the codebook costs **2 bits/group**.
**Block size 64 B, derived:** > 32 B (one sector, min transaction), ≤ 128 B (one cache line), and 64 B is the default DRAM→L2 transaction. Ratios powers of two for alignment.
**Outliers = padding.** Under-budget blocks re-store the largest values from the second-largest down, **15 bits each (7 location + 8 FP8)**. The currency is the group's own compressibility.
**Clipping is real data loss.** Over-budget groups are truncated. Projection layers **clip < 0.04%, pad ~0.7%**; **K-cache pads 7.11%**, V-cache 2.19%. **KV clipping ratio is never reported.**
**KV differs:** Huffman + clip/pad move **online**; pattern choice can't afford MSE, so it compares **group min/max vs pattern min/max — G comparisons → 2**. Hardware uses **16 patterns, not 64**.
**Accumulator / compute precision.** **None low.** Decompression sits **between L1 and L2**, so SMs receive **FP16**. `W4A8KV4` is a *storage* format; arithmetic never runs low-precision.
**Escape hatch.** FP8 padded outliers; activations only 2×; and everything is FP16 by the time it is computed on.
**Retraining.** PTQ, but **calibration-dependent** — a small set from **Pile**, for weights *and* KV patterns.

## 3. Optimization

**Entropy coding made to fit a cache.** Huffman decoding is serial by construction, which is why
compressed caches use fixed-width schemes. Ecco refuses that: **64 decoders on overlapping
segments**, each holding **8 sub-decoders that speculatively decode the same 15-bit chunk starting
at every bit offset 0–7**, with a **6-stage tree** (2⁶ = 64) resolving which speculation was right
using each segment's end-of-parse pointer. Code lengths are bounded to **2–8 bits** to cap the
speculation; each decoder consumes 8 bits plus a 7-bit overlap and yields 1–4 values. Then **128
parallel mappers** turn indices into centroids, with an outlier mask choosing centroid or restored
FP8 value per position. **28-cycle** decompress, replicated **20×** to match L2's 5120 B/cycle.
Speculate-everywhere-then-reduce is the standard way to parallelise a serial parse; doing it at
cache throughput is the contribution.

**Padding as an outlier scheme.** A variable-length code doesn't fit a fixed block, so something
gives. Ecco clips overflow — and when a block comes in *under* budget, spends the slack restoring
that group's largest values at FP8. Easy-to-code groups buy back more of their tail. Against the
rest of the corpus — a destroyed neighbour (OliVe), a destroyed weight plus permutation metadata
(MicroScopiQ), extra bits plus COO (Oaken), a second datapath (OLAccel, OASIS) — **paying for
outliers out of compressibility is a genuinely new answer.**

**Why not AWQ or SqueezeLLM, arithmetically.** AWQ's group-128 FP16 scale *and* FP16 zero point is
**32 bits**; held inside the block at 4 bits/element that evicts **8 of 128 points = 6.25% of
weights**. SqueezeLLM needs a **dense kernel plus a sparse kernel** for its per-tensor outliers,
and outlier counts vary per block and can overflow it. Ecco's answer is one scale, no zero point,
shared patterns, and outliers that live inside the block by construction.

**Integration is the quiet win.** Decompressor L1↔L2, compressor L2↔HBM — **the same placement as
NVIDIA's Compute Data Compression**. Opt-in via `CUmemAllocationProp`; **two spare PTE/TLB bits**
carry "compressed" and "which ratio". **5.11 mm² of an 826 mm² A100 die, 7.36 W.** No kernel
changes, no ISA, no model changes.

**What it does not buy.** Arithmetic. The SMs see FP16, so the entire win is bandwidth and
capacity — which is exactly why the speedup is largest when the workload is memory-bound and
decays as batch size grows.

## 4. Results

| | |
|---|---|
| Baseline | TensorRT-LLM FP16, AWQ (W4A16), SmoothQuant (W8A8), **OliVe reconfigured by Ecco to W8A8**. QuaRot is in the accuracy table but **excluded from the speed comparison** (it loses to FP16 at batch ≤ 64) |
| Models / datasets | LLaMA 7/13/30/65B, LLaMA-2 7/13/70B, Mistral-7B. Wikitext-2 perplexity at seq 2048; simulation to 4K only |
| Accuracy delta | **W4A16: +0.10 PPL average vs FP16**, beating every baseline except on LLaMA-7B. **W4A8KV4: beats all baselines including QuaRot** on every LLaMA/LLaMA-2 from 7B to 70B |
| Speedup | Batch sweep (LLaMA-13B, seq 2048): **2.6×–3.2×, avg 2.9× vs TensorRT FP16**; up to **2.9× / 2.4× / 1.8×** vs AWQ / OliVe / SmoothQuant. Length sweep (BS 8): up to **2.1× / 2.3× / 1.9×** |
| Energy / area | **5.11 mm² on an 826 mm² A100 = < 1%**; **7.36 W** (quoted as "< 10% of A100 *idle* 82 W"; ≈1.8% of the 400 W TDP). Decompress **28 cycles**, compress **62**, replicated **20×** for L2's 5120 B/cycle. **~4× capacity** |
| Technology node | RTL at **28 nm** (ARM cells, Synopsys DC), area and power **scaled to 7 nm** to match A100 |
| Evidence level | **RTL + synthesis** (area/power) + **Accel-Sim / GPGPU-Sim 4.0** with NVBit traces, A100 config tuned and correlated against real hardware. No silicon |
| **Is the comparison fair?** | Same GPU model and simulator throughout, baselines in their own frameworks, QuaRot's exclusion disclosed with a figure. But the three headline ratios are **per-baseline maxima from whichever of two sweeps was kinder**; the **OliVe baseline is Ecco's own W8A8 reconfiguration**; power is compared to A100 **idle**, not TDP; and the **KV clipping ratio — the number that prices the risk — is never reported** |

## 5. Comment

## 6. Claude notes

> **Suggestions from the reading agent. Strip this section before copying into
> `QuantArchSurvey/venues/ISCA/notes/`.**

- **This settles the open `Q` row in the tag revision log, in favour of `Q-ORIENTED`.** The log
  flags Ecco's `non-Q` → `Q` as "worth a second opinion", reasoning that a parallel Huffman decoder
  would survive an INT8 swap. It wouldn't: the decoder's **alphabet is the quantization** — 16
  codes = 15 k-means centroids + 1 scale index, `ID_KP`/`ID_HF` name a centroid set, and the
  clip/pad path restores *quantization* outliers. Swap in INT8 and the pattern retriever, the
  16-code books, the centroid mappers and the padding scheme all lose their referent.
- **But the discomfort behind that tag is real, and I think it's a missing axis.** Every other
  hardware entry read so far makes **arithmetic** cheaper. Ecco makes **traffic** cheaper and hands
  the SM FP16. *Quantization-as-compression* vs *quantization-as-cheaper-arithmetic* explains three
  things at once: why Ecco's speedup decays with batch size, why P3-LLM rates it *high accuracy,
  high memory saving, **low** hardware efficiency* without contradiction, and why `Q`/`non-Q` felt
  uncomfortable. `Gist`, `SpZip`, `JPEG-ACT` and `IBMCompressionAccelerator` are probably on the
  same side of that line — might be worth reading as a group.
- **DOI recovered.** The arXiv PDF carries its own ACM block: **10.1145/3695053.3731024**. The
  entry previously said "not recorded".
- **P3-LLM's criticism of Ecco is correct and correctly scoped — and the pair makes a point neither
  makes alone.** P3-LLM says Ecco "requires complicated online decompression of quantized operand
  **back to FP16 for computation**... its idea cannot be applied to designing low-precision PCUs."
  Every clause checks out. But Ecco's decompressor is **< 1% of a GPU die**; put the same logic in
  DRAM with P3-LLM's own **10× density penalty** and it's ~51 mm² against P3-LLM's entire 8.4 mm²
  PCU budget. **Read generally, "Ecco is hardware-inefficient" is wrong; read about PIM, it's
  right.** *The same decoder is cheap in logic and impossible in DRAM* — that's the sharpest
  substrate-dependence instance so far and I'd give it a line in the survey.
- **§5 material, if you want it.** On the codebook thread, Ecco is the odd member: Mokey,
  TransitiveArray, LUT Tensor Core, Omni-LUT and OASIS build **tables to compute through**; Ecco
  builds a **codebook to store through** and never computes on the indices. "Codebook-based" as one
  survey category currently conflates the two.
- **Adoption-barrier anchor.** Two PTE bits, an allocator flag, < 1% die — the easy end, against
  LUT Tensor Core (replace the Tensor Core + new ISA + new compiler) at the hard end and Oaken
  (engines in a DMA path) in between. If that axis makes the survey, these three calibrate it.
- **Data-type cell:** I'd extend the seed's `VQ` `MIXED` to **`VQ` `FP8` `INT8` `MIXED`** — padded
  outliers are FP8 and the **2× activation path is plain uniform INT8 with a zero point**, not VQ
  at all. Also checked against your `SYS` rule: an allocator flag and two PTE bits are an
  *interface*, not a software stack, so `ARCH` alone stands.
- **Two gaps worth knowing if we cite the accuracy.** The **KV clipping ratio is never given** —
  and KV is the online, distribution-shifting case where clipping is the actual risk. And **which
  pattern selector produced Table 1 is unstated**: the algorithm searches S = 64 by MSE, the
  hardware compressor uses **16** patterns by min/max, and "minimal drop" is asserted without a
  number for the as-built path.
- **SqueezeLLM is load-bearing and outside the corpus** — Ecco's whole format is an argument
  against its dense-plus-sparse split. Add it to the list with ANT, GOBO, WRPN, PACT, BitMoD.
