# NDPLowBitFP — paper notes

**Bringing Near Data Processing into the Low-Bit Floating-Point Era**
Tongxin Xie, Mingyu Gao, Zehao Wang, Zhihao Jia, Yuechen Xi, Bing Li, Mo Guang, Jiale Yan,
Kaiwen Long, Xingcheng Zhang, Huazhong Yang, Yuan Xie, Zhenhua Zhu, Yu Wang
**ISCA 2026** (2026 ACM/IEEE 53rd Annual International Symposium on Computer Architecture),
pp. 1383–1399 ｜ DOI: **10.1109/ISCA66397.2026.00104**
Publication info verified 2026-09-02 from the **official ISCA 2026 proceedings package**
(title, authors, pages, DOI and abstract all read from its `assets/data/data.js`).
Archived here: **the published proceedings PDF** (`506501b383.pdf`, 17 pages) — not a preprint.

Status: **note ready** ｜ Last updated: 2026-09-10
Tags: `pim-ndp` `analytical-dtype` `dtype-granularity` `mixed-precision` `accelerator`
How far it was read: **full close read of §I-§XII.** §III (NDP architecture and the multi-precision
PU), §IV (motivation experiment), §VI (scale-value interleaved layout), §VII (dequantization
hiding), §VIII (compilation-space exploration) and §IX-X (methodology and results) read line by
line. Figures are bitmaps in the extraction, so numbers come from prose. Read after
[`P3-LLM`](../P3-LLM/ANALYSIS.md), the corpus's other near-memory entry.

> The PDF is **not committed** (1.5 MB). It came from the proceedings package a human
> supplied, now archived at [`archieve/ISCA 2026.zip`](../../../archieve/), entry `pdfs/5065-3nexm57sBmVa6MJtFTiSrb/506501b383/506501b383.pdf`.
> **There is no public URL for it** — this is not an arXiv paper. Re-extract with
> `python3 extract.py` → `extracted/` (committed, greppable).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, 2026 row.

---

## Brief

### 1. Motivation

Near-data processing answers the memory wall, and group-wise low-bit floating point answers
accuracy — FP4 gives 3–4× speedup and ~4× memory reduction on GPUs at comparable accuracy,
because exponent+mantissa gives finer resolution over a wider range than integers, and per-
group scales handle outliers. But **existing NDP compilers cannot support it**: different
quantization configurations prefer different compilation strategies; fine-grained grouping
makes execution alternate between value and scale accesses, **raising DRAM row-buffer
misses**; and frequent dequantization adds latency.

### 2. Overview

**FlexQ-NDP**, an NDP compiler for general low-bit FP, with an open-source simulation
framework for the cost model, a **scale-value interleaved layout** to cut row changes, a
**dequantization-hiding** technique based on instruction reordering, and a pruned
compilation-space search.

### 3. Pros and cons

**Pros**

- Targets the least glamorous and most real obstacle — the compiler — and each of the three
fixes maps to a specific measured cause.
- The scale-value interleaving insight is precise and non-obvious: fine-grained grouping's
cost is not arithmetic but DRAM row locality.
- Up to 3.29× speedup over existing compilation strategies across quantization
configurations, ~1.31× average energy reduction, with the simulation framework released.

**Cons**

- Simulation-based throughout, on a modelled NDP architecture — no silicon and no real DRAM-
PIM measurement.
- The compilation-space search is pruned 4–5×, which helps but still leaves a search whose
cost is a deployment consideration.
- Contributes no new data type: it makes existing group-wise low-bit FP practical on NDP, so
its place in §1.2 is as an enabler rather than an originator.

### 4. Where it applies

The **compiler/toolchain** perspective on quantization in the PIM/NDP cluster, and a good
corrective for a survey that would otherwise treat format support as purely a datapath
question. Read with [`P3-LLM`](../P3-LLM/ANALYSIS.md).

---

## Conclusions

**Its best contribution is a diagnosis, and it is exact.** Fine-grained group-wise scaling is
assumed to cost extra *scale traffic*. §VI-A measures it: **75% of the scale-related latency
overhead is DRAM row-changing, and only 25% is the scale access itself** **verified**. Values and
scales live in separate regions, so fine grouping forces the PU to alternate between two DRAM rows,
and the NDP buffer is too small to hold both. That reframing — the cost of fine granularity is
**row locality, not bandwidth** — is the single most reusable sentence in the paper, and it applies
to every group-wise scheme in the corpus, not just to NDP.

**The layout fix follows directly from the diagnosis.** Interleave scales into the value stream in
**itBlocks** whose ratio and stride are derived from the quantization config and the GEMM loop
order, so the alternating access pattern lands inside one row instead of across two. The ratio is
`Prec(Value)·G_M·G_K / Prec(Scale)`; the stride bottoms out at **one DRAM column** for the scale
region, to avoid mixing so finely that the layout itself becomes irregular; and the constraint that
**a QGroup's values must share an itBlock** (or its scale gets duplicated) is what keeps it correct.
Layout alone is worth **~2×**.

**Dequantization hiding is a genuinely elegant observation about DRAM timing.** The authors noticed
that at QGroup size 128 dequantization costs **zero** extra latency, and worked out why: those
instructions fall between two DRAM row accesses, where the PU is idle for
**tRP + tRCD = 48 cycles** while one row precharges and the next activates. A dequantization costs
**8 cycles (2·tCCD_L)** and touches no DRAM, so it fits entirely inside that window — a **free
slot**. At smaller group sizes only **~10%** of dequantizations land in one naturally, so
FlexQ-NDP reorders instructions to put them there. This is scheduling into a memory-timing bubble,
and it is the kind of result only a compiler paper finds.

**It contributes no data type, and does not pretend to.** FlexQ-NDP makes *existing* group-wise
low-bit FP practical on NDP. Its place in the survey is as an **enabler** — the entry that explains
why fine-grained scaling is expensive on near-memory substrates and what to do about it.

**Read the headline carefully.** "Up to 3.29×" is a **maximum** over quantization configs and
workloads. The paper's own averages are more modest and are stated plainly elsewhere: **1.31×**
energy on average, **1.49×** on CNN CONV layers, **1.38×** persisting as SRAM grows, and
**1.66×** average latency reduction from the mixed-precision PU. The survey should carry an
average, not the maximum.

---

## Method

**The NDP substrate** (§III, §IX-A) **verified**. A multi-precision dot-product PU: FP multipliers
into an FP adder tree. FP32 mantissa multiplication normally needs a 24-bit multiplier; it is
decomposed into **four 12-bit**, each further into **four 6-bit**, to expose parallelism at low
precision — with the paper noting that only a small fraction of multipliers are actually used at
FP4/FP8, so the FP32 design point is a deliberate area trade. Synthesised with **Synopsys DC at
14 nm**, aligned to the **1y-nm DRAM process of GDDR6-AiM**; **PU clock 0.4 GHz**, set so one MAC
completes within a bank access interval (`tCCD_L × tCK`) under GDDR6 timing.

**Scale-value interleaved layout** (§VI) **verified**:

- **Diagnosis**: values and scales stored in separate regions; fine grouping alternates accesses
  between them; the small NDP buffer cannot hold both, so refills force a row change and a change
  back. **75% of the overhead is the row change.**
- **Step 1 — interleaving ratio**: `Size(ValueRegion)/Size(ScaleRegion) = Prec(Value)·G_M·G_K /
  Prec(Scale)`, where `G_M`/`G_K` are the group sizes along M/K. **Values in one QGroup must land
  in the same itBlock**, else that scale must be duplicated.
- **Step 2 — interleaving stride**: the itBlock size, adjustable to the buffer refill frequency.
  The scale region's minimum granularity is **one DRAM column**, to avoid over-fine mixing; the
  column count `ColS` is bounded by the scale buffer and is a compilation-space variable.

**Dequantization hiding** (§VII) **verified**:

- **Free slots** are instruction positions where the PU is idle for a DRAM row change:
  **tRP + tRCD = 48 cycles** (DRAMSim3 timing) versus a dequantization's **8 cycles (2·tCCD_L)**,
  which needs no DRAM access.
- At QGroup 128, dequantization is **free** because all such instructions already sit in free
  slots. At small group sizes only **~10%** do.
- Dequantization latency scales with **the number of partial results it processes**, bounded by the
  partial-result buffer allocation — so the buffer split is part of the schedule.
- FlexQ-NDP reorders instructions to place dequantizations into free slots.

**Compilation-space exploration** (§VIII). A pruned search (**4-5×** reduction per the brief) over
loop schedules, buffer allocations and layout parameters, driven by a cost model.

**Mixed-precision PU extension** (§X). With mixed-precision PUs, **dequantization can be applied to
the result rather than to the weight**, which re-enables the instruction-reordering technique for
**weight-only** configurations where it was otherwise blocked — worth **1.66× average** latency
reduction.

**Open source**: the simulation framework is released.

---

## Key numbers, with their frame

Evidence level: **cycle-level NDP simulation** with **DRAMSim3** timing, plus **Synopsys DC at
14 nm** for PU area/power. **No silicon and no real DRAM-PIM measurement.** All comparisons are
against **existing NDP compilation strategies** on the same modelled architecture.

| Setting | Model | Metric | Baseline | Result | Source |
|---|---|---|---|---|---|
| **Headline** | LLM MVM, several QConfigs | speedup | existing NDP compilation | **up to 3.29× — a maximum, not an average** | §I, §X **verified** |
| **The diagnosis** | — | share of scale-related latency overhead | — | **75% DRAM row-changing, 25% scale access** | §VI-A **verified — the paper's most reusable number** |
| Layout alone | — | speedup contribution | — | **~2×** | §X **verified** |
| Dequant at QGroup 128 | — | added latency | — | **zero** — all instructions fall in free slots | §VII-A **verified** |
| Free-slot budget | — | PU idle window vs dequant cost | — | **48 cycles (tRP+tRCD) vs 8 cycles (2·tCCD_L)** | §VII-A **verified** |
| Natural free-slot hit rate | small QGroups | share of dequant instructions | — | **~10%** — the rest must be scheduled | §VII-A **verified** |
| Energy | all workloads | reduction | baseline | **~1.31× average, 1.78× peak** | §X **verified** |
| CNN | CONV layers (im2col) | speedup | baseline | **1.49× average** | §X-B **verified** |
| Buffer pressure | — | required buffer capacity | baseline | **~3× less** | §X **verified** |
| Large-SRAM regime | LLaMA-7B MVM2 | speedup as SRAM grows | baseline | **stabilises at 1.38×** | §X **verified** |
| Mixed-precision PU | weight-only configs | latency reduction | baseline | **1.66× average** — re-enables reordering for W-only | §X **verified** |
| Implementation | — | node / clock | — | **14 nm, 0.4 GHz**, matched to GDDR6-AiM's 1y-nm DRAM | §IX-A **verified** |

**Trends the paper states** (§X): finer quantization groups favour **weight-activation** configs;
larger batch sizes favour **weight-only** configs. So the 3.29× maximum belongs to a specific
corner of a two-dimensional space.

---

## Cost and requirements

| | |
|---|---|
| **Compilation search** | Pruned 4-5×, but still a search. A per-(model, QConfig, buffer-size) compile-time cost |
| **Layout is QConfig-specific** | itBlock ratio and stride derive from `G_M`, `G_K`, precisions and the loop order — **change the quantization config and the data must be re-laid-out in DRAM** |
| **QGroup-itBlock constraint** | A QGroup's values must share an itBlock, or its scale is duplicated — a correctness constraint on the layout, not just a performance one |
| **Partial-result buffer** | Dequantization latency scales with the partial results it covers, so buffer partitioning is coupled to the schedule |
| **Substrate** | GDDR6-AiM-class NDP. Adoption is at the memory-vendor level |
| **Data type** | **None contributed.** Consumes existing group-wise FP4/FP8 |
| **Retraining** | N/A — a compiler, not a quantization method |

---

## Limitations and open questions

**Admitted.** Simulation-only, on a modelled NDP architecture. The compilation space needs pruning.
FP32 throughput is a deliberate area trade-off, and benefits shrink when computation dominates.

**Unadmitted, and material.** (i) **The abstract leads with a maximum.** 3.29× is the best cell of
a QConfig × workload grid whose averages the paper reports as 1.31×-1.66× elsewhere. (ii) **The
layout is quantization-config-specific**, so switching QConfig at deployment means re-writing DRAM
layout — never costed. (iii) **No accuracy content at all**, which is correct for a compiler paper
but means the entry cannot be cited for any quantization result. (iv) The 75%/25% split — the
paper's most valuable number — is reported once, without saying which workload or QConfig produced
it.

---

## Relation to other entries

**With `P3-LLM` it makes the near-memory case two-sided, and the two are complementary rather than
competing.** P3-LLM asks *what format can be built cheaply in DRAM* (a **hardware** answer: choose
formats for the substrate); NDPLowBitFP asks *how to schedule an existing format against DRAM
timing* (a **compiler** answer: choose layouts and instruction order for the substrate). Together
they say that near-memory quantization is constrained at both ends, and neither constraint appears
anywhere in the logic-die entries.

**Its 75%/25% diagnosis generalises beyond NDP and should be flagged as such.** Every group-wise
scheme in this corpus — `Oaken`'s groups, `MicroScopiQ`'s micro-blocks, `Ecco`'s 128-element
groups, `P3-LLM`'s per-head scales — separates values from scales somewhere in the hierarchy. This
is the only entry that measures what that separation costs, and it finds the cost is **row
locality**, not bandwidth. Worth a sentence wherever the survey discusses group size.

**The `SYS+ARCH` precedent is relevant to the RaPiD ruling.** The revision log already raised this
entry from `ARCH` to `SYS+ARCH` because "the contribution is **FlexQ-NDP, a compiler**". That is
the same reasoning applied to `RaPiD` on 2026-09-09, and it makes the two consistent — and
strengthens the case for re-examining `BitFusion` (Fusion-ISA + compiler), still `ARCH`.

**On the dequantization-cost question it is the only entry with a number.** `P3-LLM` fuses scales
into operands to avoid runtime dequantization but never prices what it avoided; `RaPiD` measures
quantization at **17% of INT4 compute cycles**; NDPLowBitFP shows dequantization can be **free**
when it fits a row-change bubble and costly when it does not. Those two measurements are the
corpus's only quantitative accounts of dequantization overhead, from opposite substrates.

**Node.** 14 nm logic aligned to a 1y-nm DRAM process — a third node convention in the corpus,
alongside logic-die nodes (7-65 nm) and P3-LLM's 28 nm→20 nm→×10-density chain. Any aggregate area
or efficiency table needs to treat DRAM-process entries separately.

---

## For the note

**§1 one-line summary.** Shows that the real cost of fine-grained group-wise scaling on near-data
processing is **DRAM row locality rather than scale bandwidth — 75% of the overhead is row-changing,
only 25% is reading the scales** — and fixes it in the compiler: a **scale-value interleaved layout**
whose block ratio and stride are derived from the quantization config and loop order so the
alternating accesses stay inside one row (~2× alone), plus **dequantization hiding** that reorders
dequantizations into the **48-cycle PU idle window** while DRAM precharges one row and activates the
next (where an 8-cycle dequantization is free), reaching **up to 3.29×** over existing NDP
compilation with ~**1.31×** average energy reduction and ~**3×** less buffer capacity.

**Proposed tags — the seed row stands; `SYS+ARCH` and the data-type revision confirmed.**

| Axis | Value | Evidence |
|---|---|---|
| **Level** | `SYS+ARCH` | The contribution is a **compiler** — layout, instruction reordering, pruned compilation-space search — running on a multi-precision PU the paper also designs. Log already revised this from `ARCH`; the close read confirms it, and it is the same reasoning that gives `RaPiD` its `SYS` |
| **Q-oriented** | `Q-ORIENTED` | **Reverted 2026-09-14**; the 2026-09-10 `non-Q` call is withdrawn. Every technique exists because values carry **separate per-group scales**: under per-tensor INT8 the interleaved layout has no alternating access to fix and free-slot scheduling has almost nothing to schedule. The `non-Q` reading (no data type contributed, generic compiler machinery, no accuracy content) describes the *contribution category* rather than the mechanisms |
| **Data type** | `FP4` `FP8` `MIXED` | Correct as revised. **Contributes none of them** — it consumes existing group-wise low-bit FP |
| **Generation** | `G2` | Group-wise scaled FP, no outlier format, no codebook. Paradigm, not year |
| **Optimization** | `NDP` `group-wise scaling` `compiler` `dequant hiding` + **`scale-value interleaved layout`** `DRAM row locality` `free-slot scheduling` `compilation-space search` | Seed has four; the layout is the mechanism and "row locality" is the finding |

**§4 fairness verdict.** Baselines are existing NDP compilation strategies on the **same modelled
architecture**, so the comparison isolates the compiler cleanly — the right control for this claim.
But everything is **simulation on a modelled NDP with no silicon or real DRAM-PIM measurement**, and
the headline **3.29× is a maximum** over a QConfig × workload grid whose averages the paper itself
reports as **1.31× (energy), 1.49× (CNN), 1.38× (large SRAM), 1.66× (mixed-precision PU)**. Quote an
average. There is **no accuracy content**, so this entry cannot be cited for any quantization result.

**Proposed venue-list row:**

```
| [ ] | [Bringing Near Data Processing into the Low-Bit Floating-Point Era](https://doi.org/10.1109/ISCA66397.2026.00104) | *close read* | SYS+ARCH | Q | `FP4` `FP8` `MIXED` | G2 | `NDP` `group-wise scaling` `compiler` `scale-value interleaved layout` `dequant hiding` `free-slot scheduling` | FlexQ-NDP. **The cost of fine-grained scaling is DRAM row locality, not scale bandwidth — 75/25** — so interleave scales into the value stream and reorder dequantizations into the 48-cycle row-change bubble |
```

## Abstract (verbatim, ISCA 2026 proceedings)

> Near data processing (NDP) based on DRAM has emerged to be a promising solution to the
> "memory wall" problem of machine learning models. From the algorithmic perspective, group-
> wise low-bit floating-point (FP) quantization has become an important trend for both
> efficient training and inference. Integrating low-bit FP quantization into NDP also
> notably shrinks the memory footprint of large models, alleviating the memory-capacity
> constraints of NDP architectures. However, existing NDP compilers struggle to support
> efficient low-bit FP computation on NDP. First, different quantization configurations
> exhibit different preferences for NDP compilation strategies. Second, the fine-grained
> grouping leads to frequent switching between quantized value access and group scale access
> during computation, increasing the DRAM row-buffer miss rate. Third, fine-grained grouping
> triggers frequent high-precision dequantization operations, causing significant latency
> overhead. To address these challenges, this paper proposes FlexQ-NDP, an NDP compiler
> tailored for general low-bit FP computation. Firstly, we develop an open-source simulation
> framework to model the low-bit FP computation overhead on NDP. Secondly, we design a
> scale-value interleaved FP layout, effectively reducing DRAM row-changing overhead.
> Thirdly, we propose a dequantization-hiding technique based on instruction reordering to
> reduce the DRAM idle time induced by frequent dequantization operations. Finally, we
> develop a lightweight compilation-space pruning and search strategy to enable efficient
> low-bit FP computation on NDP. Extensive experiments show that FlexQ-NDP achieves up to
> 3.29× speedup over existing compilation strategies on various low-bit FP quantization
> configurations.
