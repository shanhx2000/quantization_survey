# Ecco — paper notes

**Ecco: Improving Memory Bandwidth and Capacity for LLMs via Entropy-aware Cache Compression**
Feng Cheng, Cong Guo, Chiyue Wei, Junyao Zhang, Changchun Zhou, Edward Hanson, Jiaqi Zhang,
Xiaoxiao Liu, Hai "Helen" Li, Yiran Chen
**ISCA 2025**, Tokyo, June 21-25 ｜ DOI: **10.1145/3695053.3731024**
Venue evidence (**updated 2026-09-10 — DOI now verified**): the archived arXiv PDF carries its own
ACM reference block, verbatim: *"In Proceedings of the 52nd Annual International Symposium on
Computer Architecture (ISCA '25), June 21-25, 2025, Tokyo, Japan. ACM... ISBN 979-8-4007-1261-6...
https://doi.org/10.1145/3695053.3731024"*. The DOI was previously recorded as unavailable.
Archived here: **arXiv:2505.06901v1** (2025-05-11), 15 pages — **the preprint, not the
published ISCA 2025 version**; the two were **not compared**.

Status: **note ready** ｜ Last updated: 2026-09-10
Tags: `non-analytical-dtype` `gpu-kernels` `kv-cache` `dtype-granularity` `accelerator`
How far it was read: **full close read of §1-§6.** §3 (compression target, weight and KV schemes,
clip/pad, the S/H design-space exploration), §4 (decompressor, parallel Huffman decoder,
compressor) and §5 (accuracy, area/power, performance) read line by line; §2 skimmed for
background. Figures are bitmaps in the extraction, so every number below comes from prose or a
recoverable table. Read directly after [`P3-LLM`](../P3-LLM/ANALYSIS.md), which uses Ecco as a
baseline and criticises it — that criticism is checked from Ecco's side below.

> Original: https://arxiv.org/abs/2505.06901
> The PDF is **not committed** (1.4 MB). Re-download: `curl -sSL -o 2505.06901.pdf https://arxiv.org/pdf/2505.06901`
> Extract text: `python3 extract.py` → `extracted/` (committed, greppable)
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, ISCA 2025 row.

---

## Brief

### 1. Motivation

LLM deployment is memory-bound: the KV cache alone can be 72.7% (34.4 GB) of memory use.
Quantization helps but existing methods carry **high runtime overhead or accuracy loss**.
The unexploited angle is that cache data has exploitable *entropy* structure, not just range
structure.

### 2. Overview

Entropy-aware cache compression integrated at the **GPU L2 cache**: group-wise **non-
uniform** quantization against pre-defined shared **k-means** patterns, then **Huffman**
coding. Because textbook Huffman decoding is serial and slow, the paper contributes a
**parallel Huffman decoder** with a multi-stage pipeline that cuts latency by two orders of
magnitude to reach L2-comparable throughput.

### 3. Pros and cons

**Pros**

- The parallel Huffman decoder is the real engineering contribution — entropy coding is
usually dismissed as too serial for a cache, and this is a direct refutation.
- Sits at the L2 cache, so it compresses traffic to HBM transparently to the SMs, giving ~4×
capacity increase without changing the model or the kernels.
- Beats both software frameworks and a prior accelerator: 2.9×/1.9× over AWQ/SmoothQuant and
2.4× over the OliVe accelerator, at state-of-the-art accuracy.

**Cons**

- Shared **pre-defined** k-means patterns are fixed ahead of time; the paper reports low
clipping and padding ratios to argue they generalize, but distribution shift is an
unquantified risk.
- Requires modifying the GPU memory hierarchy — evaluated as a hardware proposal, not
something deployable on existing silicon.
- Entropy coding gives data-dependent compression ratios, so worst-case behaviour (and thus
provisioning) is harder to reason about than fixed-width quantization.

### 4. Where it applies

Bridges three clusters: **non-analytical data types** (k-means codebooks), **KV cache**, and
**GPU-integrated** compression. Note it is later used as a baseline by
[`P3-LLM`](../P3-LLM/ANALYSIS.md).

---

## Corrections to the brief

The brief was right about the mechanism. Four things it did not have, one of which changes what
kind of paper this is:

1. **Ecco buys memory, not arithmetic.** The decompressor sits **between L1 and L2**, so the SMs
   receive **decompressed FP16** — §4.1 **verified**, and confirmed independently by
   [`P3-LLM`](../P3-LLM/ANALYSIS.md): "Ecco requires complicated online decompression of quantized
   operand **back to FP16 for computation**." Its `W4A8KV4` is a **storage** format; no compute
   ever runs low-precision. Ecco's own speedup curve corroborates it — gains shrink at larger
   batch because "the impact of memory bandwidth limits" falls.
2. **The clip/pad step is an outlier mechanism, not bookkeeping.** Leftover space in a block is
   spent **re-storing the largest-magnitude values at FP8** (7-bit location + 8-bit value).
   Entropy slack buys outlier fidelity — a position on the outlier-currency axis nobody else takes.
3. **"Ecco" is two schemes.** 4× (weights, KV) = shared k-means patterns + Huffman. **2×
   (activations) = plain uniform INT8 with a scale and a zero point** plus bit-interleaving. The
   "entropy-aware" title covers only the 4× path.
4. **The hardware pattern selector is coarser than the algorithm.** The design-space exploration
   picks **S = 64** patterns; the 4× compressor "decreases the number of shared k-means patterns
   from 64 to 16" and selects by comparing **group min/max against pattern min/max — 2 comparisons
   instead of G** (§3, §4.3) **verified**.

---

## Conclusions

**The engineering claim is real: entropy coding can live in a cache.** Huffman decoding is serial
by construction, which is why compressed caches use fixed-width schemes. Ecco's decoder refuses
that: **64 decoders on overlapping segments**, each containing **8 sub-decoders that speculatively
decode the same 15-bit chunk starting at every bit offset 0-7**, with a **6-stage tree** (2⁶ = 64)
resolving which speculation was correct using each segment's end-of-parse pointer. Code lengths are
constrained to **2-8 bits** to bound the speculation. The result is a **28-cycle** pipelined
decompress, replicated 20× to match L2's **5120 B/cycle**. Speculate-everywhere-then-reduce is the
standard way to parallelise a serial parse; applying it at cache throughput is the contribution.

**Its quietly best idea is that padding is an outlier scheme.** A variable-length code does not fit
a fixed block, so something must give. Ecco clips overflow — and when a block comes in *under*
budget, it spends the slack **restoring the largest-magnitude values of the group at FP8**, 15 bits
each. So the currency for keeping outliers is **the group's own compressibility**: easy-to-code
groups buy back more of their tail. Measured, it works — projection layers clip **< 0.04%** and pad
**~0.7%**; the **K-cache pads 7.11%** and the V-cache 2.19%. Set against the rest of the corpus,
where outliers are paid for with a destroyed neighbour (`OliVe`), a destroyed weight plus
permutation metadata (`MicroScopiQ`), extra bits plus COO (`Oaken`) or a second datapath
(`OLAccel`, `OASIS`), this is a genuinely new answer.

**But it is a compression paper, and that distinction matters more than its tags currently show.**
Every other hardware entry read so far makes arithmetic cheaper. Ecco makes **traffic** cheaper and
hands the SM FP16. That is why its speedup is largest exactly where the workload is memory-bound
and decays as batch size grows, and why `P3-LLM` can simultaneously rate it **high accuracy, high
memory saving, low hardware efficiency** and be right on all three. The survey would be clearer
with an explicit distinction between *quantization-as-compression* and
*quantization-as-cheaper-arithmetic*; Ecco is the corpus's purest instance of the former.

**Its adoption story is the strongest in the corpus.** Decompressor between L1 and L2, compressor
between L2 and HBM — **the same placement as NVIDIA's own Compute Data Compression**; two spare
bits in existing PTEs; opt-in through `CUmemAllocationProp`. **5.11 mm² of an 826 mm² A100 die
(< 1%)** and **7.36 W**. Compare `LUT Tensor Core`, which replaces the Tensor Core and adds an ISA
and a compiler. If the survey keeps an adoption-barrier axis, Ecco anchors the easy end.

**What to hold it to.** The headline "2.9× / 1.9× / 2.4× over AWQ / SmoothQuant / OliVe" takes the
**maximum for each baseline from whichever of two sweeps flattered it** (§5.3), the OliVe baseline
is one **Ecco reconfigured to W8A8**, and QuaRot — the strongest accuracy baseline — is **excluded
from the speed comparison entirely** because it loses to FP16 at batch ≤ 64.

---

## Method

**Design constraints, stated up front** (§3.1) **verified** — unusually explicit, and they drive
everything:

1. all metadata (outliers, scales) must live **inside** the compressed block → no extra memory
   transactions at decompress time;
2. shared metadata at **tensor or channel** level;
3. decompression **on the fly**, whole block at once → no separate compute kernel.

**Block size = 64 B**, derived rather than chosen: > 32 B (one sector, the minimum transaction) or
decompression overhead and excess group metadata dominate; ≤ 128 B (one cache line) or load
flexibility drops and group-level features are obscured; and 64 B is the default DRAM→L2
transaction. **Ratios are powers of two** for alignment.

| Operand | Ratio | Bits/element | Group | Scheme |
|---|---|---|---|---|
| **Weights** | **4×** | 4 | **128** | shared k-means patterns + Huffman |
| **KV cache** | **4×** | 4 | **128** | same, but pattern choice made **online** |
| **Activations** | **2×** | 8 | **64** | **uniform INT8, scale + zero point**, bit-interleaved |

**Why not AWQ or SqueezeLLM** (§3.1) **verified**, and the arithmetic is the argument:

- **AWQ** — group 128 with an FP16 scale *and* FP16 zero point = **32 bits** of overhead. Held
  inside the block at 4 bits/element that evicts **8 of 128 data points = 6.25% of weights**.
- **SqueezeLLM** — per-channel groups and per-tensor outliers, because per-group centroids are too
  costly; needs a **dense kernel plus a sparse kernel**, and outliers carry location *and* value
  with a variable count that can overflow a block.

**Ecco's format** (§3.1) **verified**. Per group of 128: the **absolute maximum is the scale
factor** and is assigned **index 15**; the k-means pattern supplies **15 centroids** → **16 unique
indices** per group. Stored per tensor: **S = 64** shared k-means patterns and **H = 4** Huffman
codebooks per pattern (16 codes each), costing **log₂H = 2 bits per group** to name the codebook.
**No zero point at group level** (unlike AWQ); **far fewer patterns** than SqueezeLLM. The pattern
minimising group MSE is selected.

**Design-space exploration** (Fig. 5, LLaMA2-7B) **verified**: perplexity improves with S but with
diminishing returns past **64**; H matters little past **4**. S = 64, H = 4 beats the AWQ baseline.

**Clipped and padded Huffman** (§3.1) **verified** — how a variable-length code is made to fit a
fixed block:

- **over budget → clip** the excess;
- **under budget → pad**, inserting values from the **second-largest** absolute value downward (the
  largest is already the scale) until the block fills. Each padded value costs **15 bits: 7 bits of
  location + 8 bits of FP8 value**, using a **per-tensor FP16→FP8 scale that is a power of two**,
  so the inverse is an exponent adjustment.

**KV cache differs where it must** (§3.1) **verified**. Offline steps are shared with weights;
Huffman coding and clip/pad move **online**. Pattern selection cannot afford an MSE search over S
patterns per group at runtime, so Ecco exploits the fact that the patterns are **highly skewed**
(each group's k-means is scaled by an absmax that is excluded from the pattern) and compares only
**the group's min and max against each pattern's min and max** — **G comparisons → 2**. The paper
argues this is not merely cheaper but **more robust**: "more predictable compression ratios and
greater adaptability to changing pattern distributions during inference." Sharing the format with
weights gives **one decompressor for both**.

**Parallel Huffman decoder** (§4.2) **verified** — the headline hardware:

- tensor-wise metadata (patterns, codebooks, FP16→FP8 scale) preloaded **once** into the
  decompressor buffer;
- per-group scale, pattern id (`ID_KP`) and codebook id (`ID_HF`) drive a **pattern retriever**;
  the FP8 group scale is restored to FP16 by exponent adjustment;
- **64 decoders** on overlapping segments; **code length bounded to 2-8 bits**; each decoder
  consumes **8 bits plus a 7-bit overlap**, yielding **1-4 data points** and an **EOP** marking
  where the next segment begins;
- each decoder holds **8 sub-decoders** over the same 15-bit chunk at offsets **0-7**, emitting all
  eight candidate parses;
- a **6-stage tree** merges neighbouring decoders, each left result using its EOP to select the
  matching right result; the concatenator also emits an **outlier mask**;
- **128 parallel mappers** turn indices into centroids; padded outliers are scaled to FP16; the
  mask chooses centroid or outlier per position.

**Compressor** (§4.3) **verified**. The 4× compressor takes **256 B blocks** (128 FP16 values → 64 B).
A **bitonic sorter** extracts the scale, the **top 16 sorted values and indices** for padding, and
the group min/max. The pattern selector uses **16** patterns (not 64) scored by squared difference
of min/max. **Four encoders**, one per Huffman codebook, run in parallel and the shortest encoding
wins. **28-cycle decompress, 62-cycle compress** (compression is off the critical path, latency
traded for area).

**Integration** (§4.1) **verified**. Decompressor L1↔L2, compressor L2↔HBM — matching NVIDIA's
Compute Data Compression. Users declare compressibility and ratio in `CUmemAllocationProp`; **two
spare PTE/TLB bits** carry "compressed" and "which ratio", at no extra cost since NVIDIA PTEs have
unused bits.

**Calibration.** A small calibration set from **Pile** (§5.1) **verified**. Ecco is
calibration-dependent — the same dependence `P3-LLM` Fig. 8 measures QoQ suffering from, also
Pile-calibrated.

---

## Key numbers, with their frame

Evidence level: **Verilog RTL + Synopsys Design Compiler, ARM standard cells, 28 nm**, area and
power **scaled to 7 nm** to match A100; performance from **Accel-Sim + GPGPU-Sim 4.0** with
**NVBit 1.7.1** traces, CUDA 11.8, A100 configuration from the Accel-Sim tuner and correlated
against real hardware; accuracy in HuggingFace/PyTorch on A100s. **No silicon.**

| Setting | Model | Metric | Baseline | Result | Source |
|---|---|---|---|---|---|
| **Decompress latency** | — | pipelined cycles | — | **28** | §5.2 **verified** |
| **Compress latency** | — | cycles, off critical path | — | **62** | §5.2 **verified** |
| Throughput matching | — | replication to reach L2 peak **5120 B/cycle** | — | **20×** | §5.2 **verified** |
| **Area** | — | mm² added, scaled to 7 nm | A100 die **826 mm²** | **5.11 mm² — < 1%** | §5.2 **verified** |
| **Power** | — | W added | A100 **idle** 82 W @1410 MHz | **7.36 W — "< 10% of idle"** (≈1.8% of the 400 W TDP) | §5.2 **verified; the idle framing is theirs** |
| Accuracy, W4A16 | LLaMA 7/13/30B, LLaMA-2 7/13/70B, Mistral-7B | Wikitext-2 PPL, seq 2048 | FP16 | **+0.10 average**; beats every baseline except on LLaMA-7B | §5.1, Table 1 **verified** |
| Accuracy, W4A8KV4 | same | Wikitext-2 PPL | QuaRot and others | **beats all baselines on every LLaMA/LLaMA-2 from 7B to 70B** | §5.1 **verified** |
| **Clip / pad ratios** | LLaMA2-13B | share of values | — | projection layers **clip < 0.04%, pad ~0.7%**; **K-cache pad 7.11%**, V-cache **2.19%** | §5.1, Fig. 10 **verified — note the KV *clip* ratio is never given** |
| Speedup, batch sweep | LLaMA-13B, seq 2048, BS 1→64 | latency | **TensorRT FP16** | **2.6×-3.2×, average 2.9×** | §5.3 **verified — the only average in the paper** |
| " | " | latency | **AWQ / OliVe / SmoothQuant** | **up to 2.9× / 2.4× / 1.8×** | §5.3 **verified** |
| Speedup, length sweep | LLaMA-13B, BS 8, up to 4K | latency | FP16 | **2.8× → 3.1×, then falls** | §5.3 **verified** |
| " | " | latency | **AWQ / OliVe / SmoothQuant** | **up to 2.1× / 2.3× / 1.9×** | §5.3 **verified** |
| Capacity | — | memory capacity | FP16 | **nearly 4×** | abstract **verified** |
| Design space | LLaMA2-7B | patterns S / codebooks H | — | **S = 64, H = 4**; diminishing returns past both | Fig. 5 **verified** |
| Motivating datum | — | KV cache share of memory | — | **up to 72.7% (34.4 GB)** | §1 **verified** |

**The abstract's three headline ratios are each a maximum, taken from whichever sweep was kinder.**
AWQ 2.9× and OliVe 2.4× come from the **batch** sweep; SmoothQuant 1.9× comes from the **length**
sweep, where the batch sweep gave 1.8×. And the paper's only *average* — **2.9× versus TensorRT
FP16** — is numerically identical to the AWQ **maximum**, which makes the abstract read stronger
than §5.3 supports.

---

## Cost and requirements

| | |
|---|---|
| **Compute savings** | **None.** Data is decompressed to FP16 before reaching the SMs. The entire win is bandwidth and capacity |
| **Hardware** | Compressor + decompressor **replicated 20×**; 5.11 mm² and 7.36 W at 7 nm; 28/62-cycle latencies |
| **Metadata** | Per tensor: **64 k-means patterns** (FP16/FP8) + **4 Huffman codebooks per pattern** + one FP16→FP8 scale, preloaded into the decompressor. Per group: one scale + `ID_KP` + **2 bits** of `ID_HF` |
| **Calibration** | Required, from **Pile** — for weights *and* for the KV-cache patterns |
| **Data loss is structural** | Clipping **discards** data whenever a group codes badly. Measured at < 0.04% for projection layers; **not reported for KV cache**, which is the dynamic case |
| **Software/OS surface** | `CUmemAllocationProp` opt-in, two PTE/TLB bits, page-granular compression |
| **Compression ratio is data-dependent** | Fixed *block* size hides it, at the cost of clipping — so the ratio is guaranteed and the **fidelity** is what varies |
| **Escape hatch** | Padded outliers at FP8; activations only 2×; everything is FP16 by the time it is computed on |
| **Adoption barrier** | **Lowest in the corpus** — matches NVIDIA's existing compression placement, no kernel changes, no ISA, no model changes |

---

## Limitations and open questions

**Admitted.**

- Sequence lengths beyond 4K were not simulated ("due to slow simulation speeds") — honest, and it
  matters, because the KV-cache case strengthens with length.
- QuaRot is **excluded from the performance comparison** because it "consistently falls short of the
  FP16 baseline when the batch size is ≤ 64" — stated plainly, with a figure.
- The hardware KV pattern selector trades compression efficiency for predictability, and the paper
  says so.

**Unadmitted, and material.**

- **The KV-cache clipping ratio is never reported.** Fig. 10 gives clipping for projection layers
  (< 0.04%) and padding for K/V (7.11% / 2.19%), but not K/V clipping — and KV is the *online*,
  distribution-shifting, calibration-exposed case where clipping is the actual risk. This is the
  one number a reader most needs and it is absent.
- **Which pattern selector produced Table 1 is not stated.** The algorithm searches **S = 64** by
  MSE; the hardware compressor uses **16** patterns selected by min/max. "Minimal drop in
  perplexity" is asserted without a number for the as-built configuration.
- **The three headline speedups are per-baseline maxima drawn from two different sweeps**, and the
  only reported average happens to equal one of them.
- **The OliVe baseline is Ecco's own reconfiguration** — "we unified all layer weights to 8-bit and
  adopted W8A8 precision" — not OliVe's native 4-bit setting.
- **Power is compared to A100 *idle* (82 W), not TDP (400 W).** "Less than 10%" is the conservative
  framing, but any cross-paper table should use the same denominator.
- **No end-to-end accuracy for the full hardware path.** Accuracy comes from a software model of
  the scheme; the built decompressor's rounding, the FP8 outlier path and the 16-pattern selector
  are not shown to reproduce it.
- **Distribution shift is argued, not tested.** The patterns are fixed from a Pile calibration set.
  The min/max selector is claimed to adapt better than MSE, and the low clipping ratios are offered
  as evidence — but no experiment shifts the distribution deliberately.

---

## Relation to other entries

**It settles the flagged Q-tag disagreement, in favour of `Q-ORIENTED`.**
`venues/ISCA/README.md`'s revision log marks Ecco's `non-Q` → `Q` change as "arguable in the other
direction, and worth a second opinion... this row is the disagreement", on the grounds that a
parallel Huffman decoder would survive an INT8 swap. The close read says it would not. The decoder's
alphabet **is** the quantization: **16 indices per group = 15 k-means centroids + 1 scale**, the
Huffman codebooks contain exactly 16 codes, and `ID_KP`/`ID_HF` name a codebook *and a centroid
set*. Swap in plain INT8 and the pattern retriever, the 16-code books, the centroid mappers and the
clip/pad outlier path all lose their referent. **`Q-ORIENTED` is correct** — but the reason the tag
felt uncertain is real and worth naming: see below.

**It exposes a distinction the taxonomy does not currently make.** Every other hardware entry read
so far makes *arithmetic* cheaper. Ecco makes *traffic* cheaper and hands the SM FP16.
**Quantization-as-compression** versus **quantization-as-cheaper-arithmetic** is a genuine axis, and
it explains several things at once: why Ecco's speedup decays with batch size, why `P3-LLM` can rate
it *high accuracy, high memory saving, low hardware efficiency* without contradiction, and why the
`Q`/`non-Q` call felt uncomfortable. `Gist`, `SpZip`, `JPEG-ACT` and
`IBMCompressionAccelerator` are probably on the same side of that line and would be worth reading
as a group.

**`P3-LLM`'s criticism is correct and correctly scoped.** Verbatim: "Ecco requires complicated
online decompression of quantized operand **back to FP16 for computation**, leading to considerable
hardware overhead. Thus, although Ecco achieves **high accuracy**, its idea **cannot be applied to
designing low-precision PCUs**." Every clause checks out against Ecco's own §4.1, and P3-LLM's
Table I rates Ecco `W4A8KV4` / memory High / accuracy High / **hardware efficiency Low**.

**But the two papers are both right, because the substrate differs — and that is the interesting
part.** Ecco's decompressor is 5.11 mm² at 7 nm, **under 1% of an 826 mm² GPU die**. Put the same
logic in DRAM, where P3-LLM measures a **10× transistor-density penalty**, and it is roughly
**51 mm² equivalent** against P3-LLM's entire 8.4 mm² PCU budget — prohibitive, exactly as P3-LLM
says. **Read as a general claim, "Ecco is hardware-inefficient" is wrong; read as a claim about
PIM, it is right.** This is the sharpest instance so far of the substrate-dependence the P3-LLM read
opened, and it deserves a line in the survey: *the same decoder is cheap in logic and impossible in
DRAM.*

**New position on the outlier-currency axis — the currency is compressibility.**

| Paper | What is paid for keeping an outlier |
|---|---|
| `OLAccel` | +1 bit/weight always + COO per outlier activation + a second datapath |
| `OliVe` | a destroyed neighbour |
| `Oaken` | extra bits + COO metadata |
| `MicroScopiQ` | a destroyed weight + 24 b permutation metadata |
| `OASIS` | high precision on a second datapath |
| **`Ecco`** | **nothing — you get outliers only if the group compressed well enough to leave room** |

**On the codebook thread it is the LLM-era, hardware-decoded member.** `Mokey` (ISCA'22) is the
pre-LLM root; `TransitiveArray`, `LUT Tensor Core`, `Omni-LUT` and `OASIS` build *tables to compute
through*; **Ecco builds a codebook to store through** and never computes on the indices. Same
non-analytical data type, opposite use — worth stating explicitly, because "codebook-based" as a
single survey category currently conflates the two.

**Adoption-barrier anchor.** Ecco (two PTE bits, an allocator flag, < 1% die) at one end;
`LUT Tensor Core` (replace the Tensor Core, new ISA, new compiler) at the other; `Oaken` (engines
in a DMA path) in between. If that axis makes the survey, these three are its calibration points.

**Outside-corpus references it makes load-bearing:** **AWQ**, **SqueezeLLM** (its two named
foils), **SmoothQuant**, **QuaRot**, **Accel-Sim/GPGPU-Sim** and NVIDIA's **Compute Data
Compression**. SqueezeLLM matters most — Ecco's whole format is an argument against
SqueezeLLM's dense-plus-sparse split.

---

## For the note

**§1 one-line summary.** Compresses weights and KV cache **4×** into fixed **64-byte blocks** by
quantizing each group of 128 against one of **64 shared k-means patterns** and Huffman-coding the
resulting 16-index alphabet — clipping when a group codes badly and, when it codes well, **spending
the slack re-storing that group's largest values as FP8 outliers** — and makes the serial decode
affordable with **64 parallel decoders speculating at every bit offset and resolved by a 6-stage
tree, 28 cycles**, placed between L1 and L2 where NVIDIA already puts its own compressor: **< 1% of
an A100 die for ~4× capacity and 2.9× average over TensorRT FP16**, with **no reduction in
arithmetic precision at all**.

**Proposed tags — the seed row stands, and it resolves the flagged `Q` disagreement.**

| Axis | Value | Evidence |
|---|---|---|
| **Level** | `ARCH` | Verilog, synthesis, a cache-hierarchy change. The `CUmemAllocationProp` flag and two PTE bits are an *interface*, not a software stack — **checked against the `SYS` rule; there is no compiler or ISA here**, so `SYS` does not apply. Seed agrees |
| **Q-oriented** | **`Q-ORIENTED`** | **Settles the open row in the revision log.** The Huffman alphabet *is* the quantization — 16 codes = 15 centroids + 1 scale index. Swap for INT8 and the pattern retriever, the codebooks, the centroid mappers and the clip/pad outlier path all lose their referent |
| **Data type** | `VQ` `MIXED` + **`FP8`** `INT8` | k-means codebook for the 4× path; **padded outliers are FP8**; the **2× activation path is plain uniform INT8 with scale and zero point**. The seed's `VQ` `MIXED` misses that the 2× path is not VQ at all |
| **Generation** | `G3` | Codebook thread, LLM-era, KV-cache-centric. Seed agrees |
| **Optimization** | `GPU L2` `k-means codebook` `Huffman` `parallel decoder` `KV cache` + **`entropy coding`** `clip-and-pad outliers` `fixed-block variable-rate` `power-of-two ratios` | Seed has five; clip-and-pad is the mechanism worth naming |

**§4 fairness verdict.** Same GPU model, same simulator, baselines run in their own frameworks —
and QuaRot's exclusion from the speed comparison is disclosed with a figure. Against that: the
three headline ratios are **per-baseline maxima from two different sweeps**, the **OliVe baseline is
Ecco's own W8A8 reconfiguration**, power is compared to A100 **idle** rather than TDP, and the
**KV-cache clipping ratio — the number that would price the risk — is never reported**.

**Proposed venue-list row:**

```
| [ ] | [Ecco: Improving Memory Bandwidth and Capacity for LLMs via Entropy-Aware Cache Compression](https://arxiv.org/abs/2505.06901) | *close read* | ARCH | Q | `VQ` `FP8` `INT8` `MIXED` | G3 | `GPU L2` `k-means codebook` `Huffman` `entropy coding` `parallel decoder` `clip-and-pad outliers` `KV cache` | Group-wise non-uniform quantization then Huffman, at the GPU L2. **Outliers are paid for out of the group's own compressibility.** Decompresses to FP16, so it buys bandwidth and capacity, **not arithmetic** — < 1% of an A100 die |
```

## Note from the source list

> _(no keywords recorded in the source CSV)_


## Abstract (verbatim, arXiv:2505.06901v1)

> Large language models (LLMs) have demonstrated transformative capabilities across diverse
> artificial intelligence applications, yet their deployment is hindered by substantial
> memory and computational demands, especially in resource-constrained environments.
> Quantization techniques have emerged as a critical solution, reducing data precision to
> enhance memory and computational efficiency. However, existing methods often suffer from
> high runtime overheads and potential accuracy degradation. To address these challenges, we
> propose Ecco, an entropy-based cache compression technique tailored for LLMs. Ecco
> combines group-wise and non-uniform quantization with pre-defined shared k-means patterns
> and Huffman coding to exploit the inherent entropy characteristics of LLM cache data.
> Recognizing the inefficiencies of traditional Huffman coding in terms of parallelism and
> latency, we introduce a novel parallel Huffman-based decoding process with a multi-stage
> pipeline design, reducing latency by two orders of magnitude and achieving throughput
> comparable to GPU L2 caches. Comprehensive evaluations demonstrate that Ecco achieves an
> up to 2.9$\times$ and 1.9$\times$ speedup over the state-of-the-art AWQ and SmoothQuant
> framework, 2.4$\times$ over the Olive accelerator, all while increasing memory capacity by
> nearly 4$\times$ and maintaining state-of-the-art LLM accuracy. These results underscore
> the effectiveness of our entropy-based cache compression in enhancing LLM performance and
> efficiency, paving the way for more deployable large-scale AI models.
