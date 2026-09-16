# EVA — paper notes

**EVA: Accelerating LLM Decoding via an Efficient Vector Quantization Architecture**
Bowen Duan, Cong Guo, Chiyue Wei, Haoxuan Shan, Yuzhe Fu, Xinhua Chen, Yifan Xu, Ziyue
Zhang, Changchun Zhou, Hai Li, Yiran Chen
**ISCA 2026** (2026 ACM/IEEE 53rd Annual International Symposium on Computer Architecture),
pp. 1351–1367 ｜ DOI: **10.1109/ISCA66397.2026.00102**
Publication info verified 2026-09-02 from the **official ISCA 2026 proceedings package**
(title, authors, pages, DOI and abstract all read from its `assets/data/data.js`).
Archived here: **the published proceedings PDF** (`506501b351.pdf`, 17 pages) — not a preprint.

Status: **note ready** ｜ Last updated: 2026-09-10
Tags: `non-analytical-dtype` `lut-accelerator` `accelerator`
How far it was read: **full close read of §I-§VIII.** §II (VQ background, the analytic /
non-analytic distinction, prior LUT designs), §III (overview and the GEMV→GEMM recasting), §IV
(tiling and the VQ-GEMM unit), §V (epilogue and pipeline) and §VI (evaluation, Tables V-VIII) read
line by line. Figures are bitmaps in the extraction, so every number below comes from prose or a
recoverable table. Read after [`Ecco`](../Ecco/ANALYSIS.md).

> **Note for the human: you are an author on this paper** (4th of 11). Everything below is read
> from the text as written, with no inside knowledge, and §5 of the note is left for you — a
> survey's treatment of its own authors' work is your call, not mine.

> The PDF is **not committed** (2.3 MB). It came from the proceedings package a human
> supplied, now archived at [`archieve/ISCA 2026.zip`](../../../archieve/), entry `pdfs/5065-3nexm57sBmVa6MJtFTiSrb/506501b351/506501b351.pdf`.
> **There is no public URL for it** — this is not an arXiv paper. Re-extract with
> `python3 extract.py` → `extracted/` (committed, greppable).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, 2026 row.

---

## Brief

### 1. Motivation

LLM **decoding** is a sequence of small GEMV-like operations: memory-bound, and it
underutilizes accelerators built for GEMM. Weight-only **vector quantization** compresses
weights to ~2-bit levels via a shared codebook, but leaves two inefficiencies — GEMV still
underutilizes the array, and codebook lookups cause frequent **memory bank conflicts**.

### 2. Overview

Invert the dataflow. Instead of reconstructing weights from indices and doing GEMV,
**compute dot products directly between the input vector and the weight codebook** — which
turns decoding from GEMV into **GEMM** — then perform structured lookups from an
intermediate output buffer, which eliminates bank conflicts by construction. Co-designed
architecture that still runs conventional prefill.

### 3. Pros and cons

**Pros**

- The reframing is the whole idea and it is a good one: computing against the codebook
rather than the reconstructed weights changes the operation's *shape*, fixing utilization
and conflicts at once.
- Preserves arithmetic precision exactly after vector quantization — the architecture adds
no error of its own.
- 11.17× speedup and 7.17× energy efficiency over the state-of-the-art lookup-based
architecture; open-sourced.

**Cons**

- Benefit is proportional to codebook reuse, so it depends on VQ configuration (vector
length, codebook size); the paper tabulates many AQLM/GPTVQ configurations, which signals
the result is configuration-sensitive.
- Targets **decoding only** — prefill runs conventionally, so end-to-end gains depend on the
decode/prefill mix of the workload.
- Inherits vector quantization's own accuracy characteristics; the paper's contribution is
executing VQ well, not making VQ more accurate.

### 4. Where it applies

The clearest **non-analytical data type (§1.3)** entry — vector quantization with a genuine
codebook — and simultaneously a **LUT-accelerator** design. Its GEMV→GEMM reframing is worth
a sentence in the survey's own analysis.

---

## Conclusions

**The reframing is exact and worth stating as mathematics.** Decoding computes `y = xW` with
`x ∈ R^{1×K}`. Under VQ, `W`'s columns are built from `d`-dimensional centroids drawn from a
codebook `B ∈ R^{d×2ⁿ}`. Reshape `x` into `X ∈ R^{(K/d)×d}` and the key observation is that
**however large `N` is, each input sub-vector can only ever meet `2ⁿ` distinct weight vectors.**
So compute all of them at once:

```
O = X B        O ∈ R^{(K/d)×2ⁿ}      the "output codebook"
```

and then assemble `y` by **looking up** `O` with the weight indices. With `d = 8`, `n = 8`,
`2ⁿ = 256` while `N` in an LLM exceeds 4096 — so the GEMV over `N` columns becomes a **GEMM over
256**, and the lookups that follow read a small, on-chip, regularly-addressed table.

**Its structural claim is the inverse of every other LUT design in the corpus: here the table
construction *is* the computation.** `LUT Tensor Core`, `TransitiveArray` and `OASIS` all treat
table construction as overhead to be amortised, minimised, or hoisted offline — that is exactly
what the §5.6 eager/lazy/offline axis measures. EVA builds its table **per token**, and building it
is a dense GEMM that fills the array; the lookup afterwards is the cheap part. That inverts the LUT
cost model rather than optimising within it, and it is the sentence this paper is the best citation
for.

**Three consequences follow, and the paper states them cleanly.** Converting to GEMM (i) makes all
memory accesses regular and coalesced, so the bank conflicts that motivate FIGLUT's broadcast and
LUT-DLA's replication **cannot occur by construction**; (ii) reduces lookup bandwidth by a factor
of `d`, because each lookup now returns a value that already aggregates `d` weights; and (iii)
replaces `N` columns of work with `2ⁿ`.

**The throughput result is almost exactly the underutilisation it removes, and that is the honest
reading.** Speedups are **31.56× / 32.53× / 33.50×** over a systolic array, ANT and FIGNA — and the
input tile width is **v = 32**. EVA is not making arithmetic cheaper; it is filling an array that
GEMV left ~1/32 idle. That is a real and large win for the decode regime, and it is also why the
advantage disappears at batch > 32, which the paper reports.

**But the headline numbers are quoted at the configuration with the accuracy loss.** Both
"11.17× speedup" and "7.17× energy efficiency" are for **EVA-A16W2**, the 2-bit setting — and
EVA-A16W2 is **1.99× faster and 1.99× more energy-efficient than EVA-A16W4**, because fewer
codebooks mean proportionally less work. Meanwhile Table VII shows 2-bit AQLM losing **9.4 points
of ARC-C on Mixtral-8x7B** (50.43 vs FP16's 59.81) while 4-bit AQLM is near-lossless (58.87).
**The FIGLUT baseline is evaluated at W4.** So the iso-bitwidth comparison — EVA-A16W4 against
FIGLUT-A16W4 — is roughly **5.6× speedup and 3.6× energy efficiency**, still a strong result, and
the number the survey should carry.

---

## Method

**Vector quantization** (§II-A, §III-A) **verified**. Group `d` consecutive weights along `K` into
a `d`-dimensional vector; replace each with an index into a shared codebook of `2ⁿ` centroids
learned by k-means. `K×N` weights become `V×N` indices with `V = K/d`.

**Configuration** (§III-A) **verified**: `d = 8`, `n = 8` → **256 centroids**. That is `n/d = 1`
bit per element per codebook, "too low to preserve model accuracy", so EVA adopts **AQLM's additive
VQ** with `C` codebooks for hierarchical refinement: effective precision `q = C·n/d`.
**`C = 2, 3, 4` → 2-bit, 3-bit, 4-bit.**

**The recasting** (§III-B) **verified** — see *Conclusions* for the algebra. Stated advantages:
regularised memory access, `d`× lower lookup bandwidth, and `2ⁿ` work instead of `N`.

**Tiling** (§IV-A) **verified**. Input reshaped and tiled `v × d` with **`v = 32`**; the weight
index matrix streamed `v` rows at a time (`v×N` elements); **the weight codebook and the output
stay stationary on-chip** to maximise reuse. Only input and WI are streamed from DRAM.

**What prior LUT designs pay, and why EVA does not** (§II-C) **verified** — the paper's own
accounting:

- **FIGLUT** broadcasts 8 × 16-bit to a full PE column of 32 lanes → **16 × 32 × (8 × 16) bits** of
  bandwidth;
- **LUT-DLA** replicates the codebook into **256 × (16 × 16 bit)** registers;
- both strategies "significantly constrain scalability and limit the effective codebook size to at
  most **16 entries**" — against EVA's 256.

**Pipeline** (§V). An epilogue unit performs the structured lookups from the intermediate output
buffer, with FP16 multiply/add, alignment and a diagonal accumulation path; the array is
**reconfigurable so prefill runs as a regular GEMM**.

**Escape hatch** (§VI-B) **verified**: "**All methods maintain Attention layers in FP16 precision**"
— EVA and every baseline. VQ is applied to projection and FFN weights only.

**Retraining.** PTQ — EVA inherits AQLM's codebooks and contributes no quantization algorithm of
its own. The paper is explicit that it "preserves arithmetic precision after vector quantization",
i.e. the architecture adds no error.

**Open source**: `https://github.com/dbw6/Eva.git` **verified**.

---

## Key numbers, with their frame

Evidence level: **Verilog RTL + Cadence Genus, TSMC 28 nm, 500 MHz** for all designs including
baselines; **CACTI 7.0** for SRAM (28 nm); **DRAMsim3** for DRAM power; performance from **a
simulator built on ANT's validated open-source simulator**, with all baselines re-implemented
inside it. **528 KB buffer, 64 GB/s DRAM.** No silicon. **"To simplify our experiments, we run the
first Transformer block of each model"** — every end-to-end figure is extrapolated from one block.

| Setting | Model | Metric | Baseline | Result | Source |
|---|---|---|---|---|---|
| **EVA-A16W2 (2-bit)** | LLaMA-2-7B | **speedup** | SA / ANT / FIGNA / **FIGLUT** | **31.56× / 32.53× / 33.50× / 11.17×** | §VI **verified** |
| **EVA-A16W2** | " | **energy efficiency** | SA / ANT / FIGNA / **FIGLUT** | **12.48× / 15.96× / 14.96× / 7.17×** | §VI **verified** |
| **Cost of accuracy** | " | EVA-A16W2 vs its own higher-bit modes | EVA-A16W4 / EVA-A16W3 | **1.99× / 1.49× faster; 1.99× / 1.50× more efficient** | §VI **verified** |
| ⇒ **iso-bitwidth estimate** | " | EVA-A16W4 vs FIGLUT-A16W4 | FIGLUT at W4 | **≈5.6× speedup, ≈3.6× energy** — derived, **not stated in the paper** | derived from the two rows above |
| Peak hardware, 28 nm 500 MHz | — | throughput | SA 15.75 / ANT 15.28 / FIGNA 14.84 / FIGLUT 44.49 GOPs | **498.49 GOPs (31.64× over SA)** | Table VIII **verified** |
| " | — | area | SA 1.256 / ANT 1.472 / FIGNA 1.211 / FIGLUT 1.582 mm² | **1.414 mm²** | Table VIII **verified** |
| " | — | on-chip power | SA 1.647 / ANT 2.741 / FIGNA 2.602 / FIGLUT 4.037 W | **3.117 W** | Table VIII **verified** |
| " | — | area efficiency | SA 12.54 / FIGLUT 28.12 GOPs/mm² | **352.54 (28.10×)** | Table VIII **verified** |
| " | — | energy efficiency | SA 9.56 / FIGLUT 11.02 GOPs/W | **159.94 (16.72×)** — **on-chip only, excludes DRAM** | Table VIII **verified** |
| **Accuracy, 4-bit** | Mixtral-8x7B | ARC-C / ARC-E / PIQA / BoolQ / Winogrande | FP16 **59.81 / 83.54 / 83.73 / 85.26 / 76.56** | **AQLM-4×8: 58.87 / 83.38 / 83.51 / 85.02 / 76.01** — near-lossless | Table VII **verified** |
| **Accuracy, 2-bit** | Mixtral-8x7B | ARC-C | FP16 59.81 | **AQLM-2×8: 50.43 — a 9.4-point drop.** GPTQ at 2-bit collapses to **27.30** | Table VII **verified** |
| Batch crossover | LLaMA-2-7B | latency and energy | EVA-A8W8 | **beyond batch 32, EVA-A16W2 is worse than EVA-A8W8** | §VI **verified** |
| Energy composition | all architectures | — | — | **DRAM access dominates total energy** | §VI **verified** |
| Prior LUT codebook limit | — | effective codebook entries | FIGLUT, LUT-DLA | **≤16** vs EVA's **256** | §II-C **verified** |

**Both headline numbers are for the 2-bit configuration, against a 4-bit FIGLUT.** Table VIII's
on-chip energy-efficiency ratio over FIGLUT is **16.72/11.02 = 1.52× at equal peak**, while the
end-to-end figure is 7.17× — the difference is where the win actually is: **DRAM traffic**, not the
datapath.

---

## Cost and requirements

| | |
|---|---|
| **On-chip codebook** | The weight codebook and output stay **resident**; `C` codebooks of 256 × 8 FP16 centroids each |
| **Output codebook buffer** | `O ∈ R^{(K/d)×2ⁿ}` must be held and then randomly read by the epilogue unit — this is the structure that replaces bank conflicts with regular access |
| **Compute scales with `C`** | 4-bit costs **1.99×** the work of 2-bit. The bitwidth knob is a direct throughput knob |
| **Reconfiguration** | The array must switch between VQ-GEMM (decode) and regular GEMM (prefill) |
| **Escape hatch** | **Attention layers stay FP16** — for EVA and every baseline |
| **Regime** | Decode only, and **batch ≤ 32**; past that EVA-A16W2 loses to plain A8W8 |
| **Retraining** | PTQ; codebooks from AQLM. **No quantization algorithm of its own** |
| **Accuracy is inherited** | Including AQLM's 2-bit behaviour, which is not near-lossless |

---

## Limitations and open questions

**Admitted.**

- Decode-only; prefill runs conventionally, so end-to-end gain depends on the workload mix.
- The batch-32 crossover is measured and reported rather than hidden.
- DRAM dominates energy for every architecture, EVA included.
- "We run the first Transformer block of each model" — stated plainly.

**Unadmitted, and material.**

- **The headline compares a 2-bit EVA against a 4-bit FIGLUT**, and 2-bit AQLM costs 9.4 points of
  ARC-C on Mixtral. The iso-bitwidth number (~5.6×) is derivable from the paper's own text but is
  never stated.
- **The throughput gain is the array utilisation, and `v = 32` gives it away.** Speedups of
  31.56-33.50× against three different non-LUT baselines are not three independent results; they
  are one geometric fact. Worth saying so — it makes the claim *more* credible, not less.
- **Table VIII's energy-efficiency ratio (1.52× over FIGLUT) and the reported 7.17× differ by
  4.7×**, because one is on-chip peak and the other is end-to-end with DRAM. Both are legitimate;
  quoting either without the frame is not.
- **No area or latency accounting for the epilogue unit's random reads into `O`.** The claim is
  that structured lookup eliminates bank conflicts by construction; the buffer's ports, banking and
  the epilogue's occupancy are not costed separately in Table VIII.
- **One Transformer block extrapolated to end-to-end** understates layer-boundary and
  non-projection costs, which is exactly where the FP16 attention escape hatch lives.

---

## Relation to other entries

**It inverts the §5.6 table-construction axis rather than joining it.** The axis so far —
**eager per-tile** (`LUT Tensor Core`), **lazy per-tile** (`TransitiveArray`), **offline-static**
(`OASIS`), with a second dimension for *which operand is binarised* (`Omni-LUT`) — measures how
cheaply a table can be built and reused. EVA's answer is that **you should make the table
construction be the GEMM**: `O = XB` is dense, regular, and fills the array that GEMV was starving.
Add it as a fourth position — **construction-as-computation** — and note it is the only one where
building the table is not overhead.

**On the codebook thread it is the `Mokey` line's LLM-era hardware terminus.** `Mokey` (ISCA'22)
is the pre-LLM root; `Ecco` builds a codebook to **store** through and never computes on indices;
EVA builds a codebook to **compute** through and never reconstructs weights. Those two ISCA
entries are the cleanest possible statement of the fork inside "codebook-based", and the survey
should not put them in one bucket.

**It is the corpus's only true vector-quantization entry.** Everything else — `Mokey`,
`TransitiveArray`, `Ecco`, `OASIS` — clusters **scalars**. EVA clusters `d = 8`-dimensional
**vectors**, which is what makes the `2ⁿ`-bounded output codebook possible at all. Its §II-B
analytic / non-analytic framing is also the clearest statement in the corpus of the distinction
`survey/TAGS.md` encodes as `analytical-dtype` / `non-analytical-dtype`, and is worth citing for
the definition itself.

**`FIGLUT`, `FIGNA`, `LUT-DLA` and `GOBO` are load-bearing and outside the ISCA corpus.** FIGLUT is
the baseline both headline numbers are measured against. Add them to the running list with ANT
(six entries), GOBO (now four), WRPN, PACT, BitMoD and SqueezeLLM.

**Node.** 28 nm synthesised, alongside `Tender` and `Oaken` (28 nm) and `P3-LLM`'s 28 nm RTL. All
baselines were re-implemented and synthesised at the same node in the same flow, which is the
strongest form of the iso-node discipline seen so far.

---

## For the note

**§1 one-line summary.** Turns LLM decoding from GEMV into GEMM by **computing the dot products
between the reshaped input and the weight codebook itself** — `O = XB`, all `2ⁿ = 256` possible
input-centroid products at once — and then assembling the output by structured lookups into that
intermediate table, so the array that GEMV left ~1/32 idle runs full and codebook bank conflicts
cannot arise by construction: **31.6× over a systolic array, 11.17× over FIGLUT at 2-bit** (≈5.6×
at matched bitwidth), with no arithmetic error added beyond the vector quantization it inherits.

**Proposed tags — the seed row stands, with one addition.**

| Axis | Value | Evidence |
|---|---|---|
| **Level** | `ARCH` | Codebooks are AQLM's; the contribution is the dataflow, the array and the epilogue unit. Verilog + Genus + a simulator. **Checked against the `SYS` rule** — the reconfiguration is architectural, there is no compiler or ISA, so `SYS` does not apply. Seed agrees |
| **Q-oriented** | `Q-ORIENTED` | Swap in plain INT8 and there is no codebook, no output codebook, no structured lookup, and no GEMV→GEMM recasting — the entire design premise is the vector-quantized format. Seed agrees |
| **Data type** | `VQ` `LUT` `FP16` `INT8` (**human-verified 2026-09-10**) | `d = 8`, `n = 8`, 256 centroids, `C = 2/3/4` codebooks → **2/3/4-bit** effective. `FP16` for activations, codebook entries, the output codebook and **all attention layers**; **`INT8`** because §IV-B's base PE **is** an INT8 array — FP16 is reconstructed from **four INT8 multiplications**, and INT8 prefill runs on the same array |
| **Generation** | `G3` | Codebook thread, weight-only, LLM decode. Seed agrees |
| **Optimization** | `weight-only` `VQ` `GEMV→GEMM` `conflict-free lookup` + **`output codebook`** `additive VQ (AQLM)` `codebook-stationary` `decode-specialised, prefill-compatible` | Seed has four; "output codebook" is the object the whole design turns on |

**§4 fairness verdict.** Every baseline re-implemented in Verilog and synthesised at the **same
node, same flow, same clock, same buffer and same DRAM bandwidth** — the strongest iso-node
discipline in the corpus. Against that: the headline **11.17× / 7.17× are EVA at 2-bit versus
FIGLUT at 4-bit**, and 2-bit AQLM costs **9.4 points of ARC-C on Mixtral**; matched-bitwidth is
≈5.6× / ≈3.6×, derivable from the paper but never stated. Everything end-to-end is extrapolated
from **one Transformer block**, and the 31-33× speedups over the three non-LUT baselines are one
geometric fact (`v = 32`), not three results.

**Proposed venue-list row:**

```
| [ ] | [EVA: Accelerating LLM Decoding via an Efficient Vector Quantization Architecture](https://doi.org/10.1109/ISCA66397.2026.00102) | *close read* | ARCH | Q | `VQ` `LUT` `FP16` `INT8` | G3 | `weight-only` `VQ` `GEMV→GEMM` `output codebook` `conflict-free lookup` `additive VQ` | Dot products against the codebook rather than reconstructed weights — **the table construction *is* the GEMM**, which fills an array GEMV left 1/32 idle and makes bank conflicts structurally impossible |
```

## Abstract (verbatim, ISCA 2026 proceedings)

> Large Language Models (LLMs) have achieved impressive performance across diverse domains
> but remain inefficient during the autoregressive decoding phase. Unlike the prefill stage,
> which employs compute-bound GEMM operations, decoding executes a sequence of small GEMV-
> like computations that are memory-bound and underutilize modern accelerators. Weight-only
> vector quantization (VQ) has emerged as an effective compression technique that clusters
> model weights into a shared codebook and replaces the original weight matrix with low-
> precision indices, enabling 2-bit-level weight compression. While this approach
> substantially reduces model size and memory bandwidth, it still suffers from two critical
> inefficiencies: the low utilization of GEMV computation and frequent memory conflicts
> during codebook lookups. This paper presents EVA, an efficient vector-quantization-based
> architecture that addresses both computational and memory bottlenecks in LLM decoding. EVA
> builds on a simple yet effective insight that combines input-codebook computation with
> conflict-free memory access. Instead of reconstructing quantized weights from indices, EVA
> directly performs dot products between input vectors and the weight codebook, transforming
> LLM decoding from GEMV to GEMM computation. It then performs structured lookups from an
> intermediate output buffer, eliminating memory bank conflicts. We further design a
> hardware-software co-optimized architecture specialized for LLM decoding while remaining
> compatible with conventional prefill execution. Evaluations show that EVA achieves up to
> 11.17x speedup and 7.17x higher energy efficiency compared with the SOTA lookup-based
> architecture, while preserving arithmetic precision after vector quantization. Our code is
> available at https://github.com/dbw6/Eva.git.
