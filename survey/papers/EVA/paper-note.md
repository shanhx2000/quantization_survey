# EVA: Accelerating LLM Decoding via an Efficient Vector Quantization Architecture

**Venue / Year:** ISCA 2026 · **Link:** https://doi.org/10.1109/ISCA66397.2026.00102 · code https://github.com/dbw6/Eva.git · **Reader:** Haoxuan · **Date:** 2026-09-10

## Tags

| | |
|---|---|
| **Level** | `ARCH` |
| **Q-oriented** | `Q-ORIENTED` |
| **Data type** | `VQ` `LUT` `FP16` `INT8` |
| **Generation** | `G3` |
| **Optimization** | weight-only · VQ · GEMV→GEMM · output codebook · conflict-free lookup · additive VQ (AQLM) · codebook-stationary · decode-specialised, prefill-compatible |

## 1. One-line summary

Turns LLM decoding from GEMV into GEMM by **computing the dot products between the reshaped input
and the weight codebook itself** — `O = XB`, all `2ⁿ = 256` possible input–centroid products at
once — then assembling the output by structured lookups into that intermediate table, so the array
GEMV left ~1/32 idle runs full and codebook bank conflicts **cannot arise by construction**:
**31.6× over a systolic array and 11.17× over FIGLUT at 2-bit** (≈5.6× at matched bitwidth), adding
no arithmetic error beyond the vector quantization it inherits.

## 2. Data type

**True vector quantization — the only one in the corpus.** Groups **d = 8** consecutive weights along K into one vector, replaced by an index into **2ⁿ = 256** k-means centroids. Everything else here (Mokey, Ecco, OASIS, TransitiveArray) clusters *scalars*.
**Additive VQ (AQLM).** One codebook gives n/d = 1 bit/element — too low. **C codebooks** stack for `q = C·n/d`: **C = 2/3/4 → 2/3/4-bit**.
**Compute scales with C.** 4-bit costs **1.99×** the work of 2-bit. Bitwidth is a direct throughput knob, not just an accuracy knob.
**Everything else FP16.** Activations, codebook entries, the output codebook — and **all attention layers stay FP16**, for EVA and every baseline alike.
**But the PE underneath is INT8.** §IV-B: the base GEMM unit is an **INT8-based PE**, and FP16 is reconstructed by **decomposing into four INT8 multiplications** — so a conventional 32×32 INT8 array becomes a unit executing both. EVA also **runs INT8 prefill** on the same array. The same temporal-composition trick as BitFusion, SamsungNPU and RaPiD.
**Outliers.** None. VQ's centroids absorb the distribution; no separate outlier path.
**Granularity.** Codebook shared per tensor; vectors of 8 along K. Input tiled **v = 32** × d.
**Accumulator.** Not reported as a width; the epilogue unit is FP16 multiply/add with alignment and diagonal accumulation.
**Escape hatch.** Attention in FP16, and prefill runs as a conventional GEMM on a reconfigured array.
**Retraining.** **PTQ.** Codebooks are AQLM's — EVA contributes no quantization algorithm and explicitly "preserves arithmetic precision after vector quantization", i.e. the hardware adds no error of its own.

## 3. Optimization

**The reframing, as algebra.** Decoding is `y = xW`. Under VQ, W's columns are built from
`d`-dimensional centroids in a codebook `B ∈ R^{d×2ⁿ}`. Reshape `x` into `X ∈ R^{(K/d)×d}` and the
observation is that **however large N is, each input sub-vector can only ever meet 2ⁿ distinct
weight vectors.** So compute all of them: `O = XB`, the **output codebook**, then assemble `y` by
looking up `O` with the weight indices. With d = 8, n = 8 that is a GEMM over **256** instead of a
GEMV over **N > 4096**.

**The table construction *is* the computation — and that inverts the LUT cost model.** LUT Tensor
Core, TransitiveArray and OASIS all treat table building as overhead to amortise, minimise or hoist
offline; that is exactly what the eager/lazy/offline axis measures. EVA builds its table per token,
and building it is a dense GEMM that **fills the array**. The lookup afterwards is the cheap part.
This is the sentence EVA is the best citation for.

**Three consequences, all stated.** (i) Memory access becomes regular and coalesced, so the bank
conflicts that force FIGLUT to broadcast and LUT-DLA to replicate **cannot occur**. (ii) Lookup
bandwidth drops by a factor of **d**, since each lookup returns a value already aggregating 8
weights. (iii) Work drops from N columns to 2ⁿ.

**What prior LUT designs pay, by the paper's own accounting.** FIGLUT broadcasts 8×16-bit to a
32-lane PE column — **16 × 32 × (8 × 16) bits** of bandwidth; LUT-DLA replicates into
**256 × (16×16 bit)** registers. Both "limit the effective codebook size to at most **16 entries**"
— against EVA's 256. Making the codebook big enough for real VQ is what the recasting buys.

**The gain is the utilisation, and the tiling gives it away.** Speedups of 31.56× / 32.53× /
33.50× against a systolic array, ANT and FIGNA — with input tile width **v = 32**. EVA isn't making
arithmetic cheaper; it's filling an array GEMV left 1/32 idle. That's a real win for the decode
regime and it's also why the advantage vanishes past batch 32, which the paper reports.

## 4. Results

| | |
|---|---|
| Baseline | Systolic Array (QSERVE INT8), ANT (8-bit), FIGNA (A16W4, AWQ), **FIGLUT (A16W4, BCQ + ShiftAddLLM)** — all re-implemented in Verilog and synthesised in the same flow |
| Models / datasets | LLaMA 1/2/3, **Mixtral-8x7B, Qwen3-30B-A3B**. Synthetic fixed-length decode + Dolly, Arxiv Summarization, GSM8K. **First Transformer block only** |
| Accuracy delta | **4-bit near-lossless** (Mixtral AQLM-4×8: ARC-C 58.87 vs FP16 59.81). **2-bit is not**: AQLM-2×8 drops to **50.43, −9.4 points**; GPTQ at 2-bit collapses to 27.30 |
| Speedup | **EVA-A16W2: 31.56× / 32.53× / 33.50× / 11.17×** over SA / ANT / FIGNA / FIGLUT. EVA-A16W2 is **1.99× / 1.49×** faster than its own W4 / W3 modes → **iso-bitwidth ≈5.6× over FIGLUT** |
| Energy / area | **7.17×** energy efficiency over FIGLUT end-to-end (**≈3.6×** iso-bitwidth). Peak table: **1.414 mm², 3.117 W, 498.49 GOPs** vs FIGLUT's 1.582 / 4.037 / 44.49 — but on-chip energy efficiency is only **1.52×** over FIGLUT, so the win is **DRAM traffic**, not the datapath |
| Technology node | **TSMC 28 nm, 500 MHz**, Cadence Genus; CACTI 7.0 for SRAM; DRAMsim3 for DRAM. 528 KB buffer, 64 GB/s |
| Evidence level | **RTL + synthesis** for all five designs + a **simulator built on ANT's validated open-source simulator**. No silicon. End-to-end extrapolated from **one Transformer block** |
| **Is the comparison fair?** | Strongest iso-node discipline in the corpus — every baseline re-implemented and synthesised at the same node, flow, clock, buffer and DRAM bandwidth. But the headline **11.17× / 7.17× are EVA at 2-bit against FIGLUT at 4-bit**, and 2-bit costs **9.4 points of ARC-C on Mixtral**; matched-bitwidth is ≈5.6× / ≈3.6×, derivable but never stated. End-to-end comes from **one Transformer block** |

## 5. Comment

## 6. Claude notes

> **Suggestions from the reading agent. Strip this section before copying into
> `QuantArchSurvey/venues/ISCA/notes/`.**

- **You are an author on this paper** (4th of 11), so I've left §5 entirely alone and written
  everything below from the text as published, with no inside knowledge. How a survey handles its
  own authors' work is your call — including whether the fairness row above is the right tone.
- **The number I'd carry into the survey is not the abstract's.** Both headlines are **EVA-A16W2**,
  and EVA-A16W2 is 1.99× faster than EVA-A16W4 simply because it uses fewer codebooks — while
  Table VII shows 2-bit AQLM losing **9.4 ARC-C points on Mixtral** where 4-bit is near-lossless.
  FIGLUT is evaluated at W4. **Matched-bitwidth is ≈5.6× speedup / ≈3.6× energy**, derivable from
  the paper's own rows. Still a strong result, and defensible under scrutiny in a way 11.17× isn't.
- **§5 material, if you want it.** EVA doesn't join the §5.6 table-construction axis (eager
  per-tile / lazy per-tile / offline-static) — it **inverts** it. Everywhere else, building the
  table is overhead to amortise; here `O = XB` **is** the GEMM, and the lookup is the leftover.
  I'd add it as a fourth position, *construction-as-computation*, and note it's the only one where
  table building isn't a cost.
- **EVA and Ecco are the cleanest possible fork inside "codebook-based", and both are ISCA'25/'26.**
  Ecco builds a codebook to **store** through and never computes on indices; EVA builds one to
  **compute** through and never reconstructs weights. Same non-analytical data type, opposite use.
  The survey shouldn't put them in one bucket.
- **It's the corpus's only true *vector* quantization entry** — Mokey, TransitiveArray, Ecco and
  OASIS all cluster scalars. The d = 8 vector is exactly what makes the 2ⁿ-bounded output codebook
  possible, so this isn't incidental. §II-B is also the clearest statement anywhere in the corpus
  of the analytic / non-analytic distinction that `survey/TAGS.md` encodes — worth citing for the
  definition itself.
- **The 31–33× over three different baselines is one geometric fact, not three results** — `v = 32`
  is the input tile width. I'd say so explicitly in the survey; it makes the claim *more* credible,
  not less, because it identifies the mechanism.
- **Two accountings of the same energy claim differ by 4.7×.** Table VIII's on-chip efficiency over
  FIGLUT is **1.52×**; the reported end-to-end figure is **7.17×**. Both are legitimate — the gap
  *is* the finding, since it localises the win in DRAM traffic rather than the datapath.
- **Tags:** seed row stands, plus **`FP16` `INT8`** in the data-type cell (**human-verified
  2026-09-10**) and **`output codebook`** in the keywords — the object the whole design turns on.
  The `INT8` is not incidental: §IV-B's base PE **is** an INT8 array and FP16 is built from **four
  INT8 multiplications**, which also makes EVA a fourth instance of the
  BitFusion / RaPiD / SamsungNPU composing-high-precision-from-INT8 story. Checked against your `SYS` rule: the prefill/decode
  reconfiguration is architectural, no compiler or ISA, so `ARCH` alone.
- **FIGLUT, FIGNA and LUT-DLA are load-bearing and outside the corpus.** FIGLUT is what both
  headline numbers are measured against. Running list is now ANT (six entries), GOBO (four), WRPN,
  PACT, BitMoD, SqueezeLLM, FIGLUT.
