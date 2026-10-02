# Bringing Near Data Processing into the Low-Bit Floating-Point Era (FlexQ-NDP)

**Venue / Year:** ISCA 2026 · **Link:** https://doi.org/10.1109/ISCA66397.2026.00104 · **Reader:** Haoxuan · **Date:** 2026-09-10

## Tags

| | |
|---|---|
| **Level** | `SYS+ARCH` |
| **Q-oriented** | `Q-ORIENTED` |
| **Data type** | `FP4` `FP8` `FP16` `MIXED` |
| **Generation** | `G2` |
| **Stage type** | `S2T2` · `(PIM)` |
| **Optimization** | NDP · group-wise scaling · compiler · scale-value interleaved layout · DRAM row locality · dequant hiding · free-slot scheduling · compilation-space search |

## Stage-type tags

**`S2T2` · `(PIM)`** (the **Stage type** row in Tags) — most-matched first. The NDP processing unit decomposes an FP32 mantissa multiplier into four 12-bit and sixteen 6-bit parts so FP4 and FP8 run in parallel on one unit, and both weight-activation and weight-only low-bit configurations are evaluated — different widths in one datapath. `(PIM)`: near-data processing in DRAM is the substrate.

*Tag form `S{stage}T{type}`, vocabulary from `survey/stage2.md` and `survey/stage3.md`. Added 2026-10-02 (ISCA Stage-type batch 2).*

## 1. One-line summary

Shows that the real cost of fine-grained group-wise scaling on near-data processing is **DRAM row
locality rather than scale bandwidth — 75% of the overhead is row-changing, only 25% is reading the
scales** — and fixes it in the compiler: a **scale-value interleaved layout** whose block ratio and
stride derive from the quantization config and loop order so alternating accesses stay inside one
row (~2× alone), plus **dequantization hiding** that reorders dequantizations into the **48-cycle
PU idle window** while DRAM precharges one row and activates the next (where an 8-cycle
dequantization is free) — **up to 3.29×** over existing NDP compilation, ~1.31× average energy, ~3×
less buffer.

## 2. Data type

**Contributes none.** FlexQ-NDP consumes *existing* group-wise low-bit FP — **FP4 / FP8 with per-group scales** — and makes it practical on NDP. Its place is as an enabler, not an originator.
**Group-wise scaling is the whole premise.** Group sizes `G_M` × `G_K` along M/K; the interleaving ratio is `Prec(Value)·G_M·G_K / Prec(Scale)`.
**Both W-A and W-only configs evaluated.** Trend: finer groups favour **weight-activation**; larger batches favour **weight-only**.
**Multi-precision PU.** FP32's 24-bit mantissa multiplier decomposed into **four 12-bit**, each into **four 6-bit**, to expose FP4/FP8 parallelism — with the paper conceding only a small fraction is used at low precision, so FP32 is a deliberate area trade.
**Outliers.** None — per-group scales are the only range mechanism.
**Accumulator.** FP adder tree after the multiplier array; width not reported.
**Escape hatch.** Dequantization to high precision, which is exactly what the paper works to hide rather than eliminate.
**Retraining.** N/A — a compiler, not a quantization method. **No accuracy content anywhere in the paper.**

## 3. Optimization

**The diagnosis is the contribution, and it generalises.** Fine-grained scaling is assumed to cost
scale *traffic*. §VI-A measures it: **75% of the scale-related latency overhead is DRAM
row-changing, only 25% is the scale access**. Values and scales sit in separate regions, so fine
grouping makes the PU alternate between two DRAM rows, and the small NDP buffer can't hold both —
every refill costs a row change and a change back. The cost of fine granularity is **row locality,
not bandwidth**. That sentence applies to every group-wise scheme in the corpus.

**The layout fix follows from it.** Interleave scales into the value stream in **itBlocks** whose
ratio and stride come from the quantization config and GEMM loop order, so the alternation lands
inside one row. The scale region bottoms out at **one DRAM column** (finer mixing makes the layout
itself irregular), and a correctness constraint holds it together: **a QGroup's values must share an
itBlock**, or its scale must be duplicated. Layout alone is worth **~2×**.

**Dequantization hiding is scheduling into a DRAM timing bubble.** The authors noticed that at
QGroup 128, dequantization costs **zero** extra latency — and worked out why: those instructions
sit between two DRAM row accesses, where the PU idles for **tRP + tRCD = 48 cycles** while one row
precharges and the next activates. A dequantization costs **8 cycles (2·tCCD_L)** and touches no
DRAM, so it fits entirely inside — a **free slot**. At small group sizes only **~10%** land in one
naturally, so the compiler reorders instructions to put them there. Dequantization latency also
scales with the partial results it covers, so buffer partitioning is coupled to the schedule.

**Mixed-precision PU extension.** With mixed-precision PUs, dequantization can be applied to the
*result* rather than the weight, which re-enables instruction reordering for **weight-only** configs
where it was otherwise blocked — **1.66× average**.

## 4. Results

| | |
|---|---|
| Baseline | **Existing NDP compilation strategies on the same modelled architecture** — the right control for a compiler claim |
| Models / datasets | LLaMA-class LLM MVM operators across quantization configs and batch sizes; CNN CONV layers via im2col |
| Accuracy delta | **None — the paper reports no accuracy at all.** Correct for a compiler paper, but it means this entry can't be cited for any quantization result |
| Speedup | **up to 3.29× (a maximum, not an average).** Averages the paper reports elsewhere: **1.49×** CNN CONV, **1.38×** in the large-SRAM regime, **1.66×** from the mixed-precision PU. Layout alone ~**2×** |
| Energy / area | **~1.31× average energy reduction, 1.78× peak**. **~3× less required buffer capacity** — significant for resource-constrained NDP |
| Technology node | **14 nm** (Synopsys DC), aligned to the **1y-nm DRAM process of GDDR6-AiM**; **PU at 0.4 GHz**, set so one MAC fits a bank access interval under GDDR6 timing |
| Evidence level | **Cycle-level NDP simulation with DRAMSim3 timing** + synthesis for PU area/power. **No silicon, no real DRAM-PIM measurement.** Simulation framework open-sourced |
| **Is the comparison fair?** | Baselines are existing NDP compilation strategies on the **same modelled architecture**, which isolates the compiler cleanly. But everything is **simulation on a modelled NDP**, and the headline **3.29× is a maximum** over a QConfig × workload grid whose averages the paper itself reports as 1.31×–1.66×. Quote an average. **No accuracy content**, so it cannot be cited for a quantization result |

## 5. Comment

## 6. Claude notes

> **Suggestions from the reading agent. Strip this section before copying into
> `QuantArchSurvey/venues/ISCA/notes/`.**

- **`Q-ORIENTED` (reverted 2026-09-14 — the earlier `non-Q` call is withdrawn).** This matches my
  original reading: the two headline techniques do not survive the INT8 swap. Under per-tensor INT8
  there is one scale, so no alternating scale/value access and nothing for the **interleaved layout**
  to fix; and dequantization happens once rather than per group, so **free-slot scheduling** has
  almost nothing to schedule. What would survive is only the compilation-space search and the
  multi-precision PU. The `non-Q` reading (no data type contributed, generic compiler machinery, no
  accuracy content) is defensible but describes the *contribution category*, not the mechanisms —
  and the mechanisms are quantization-specific throughout.
- **The 75/25 diagnosis is the thing to take from this paper, and it generalises well beyond NDP.**
  Every group-wise scheme in the corpus — Oaken's groups, MicroScopiQ's micro-blocks, Ecco's
  128-element groups, P3-LLM's per-head scales — separates values from scales somewhere in the
  hierarchy. This is the **only** entry that measures what that separation costs, and the answer is
  **row locality, not bandwidth**. I'd put it wherever the survey discusses group size.
- **Quote an average, not 3.29×.** It's the best cell of a QConfig × workload grid. The paper's own
  averages are 1.31× (energy), 1.49× (CNN), 1.38× (large SRAM), 1.66× (mixed-precision PU).
- **§5 material, if you want it.** With P3-LLM this makes the near-memory case two-sided and the two
  are complementary, not competing: P3-LLM asks *what format can be built cheaply in DRAM* (a
  hardware answer); FlexQ-NDP asks *how to schedule an existing format against DRAM timing* (a
  compiler answer). Near-memory quantization is constrained at both ends, and neither constraint
  shows up in any logic-die entry.
- **It's one of only two entries anywhere in the corpus that prices dequantization.** RaPiD measures
  it at **17% of INT4 compute cycles**; this one shows it can be **free** when it fits a row-change
  bubble and costly when it doesn't. Opposite substrates, and between them the corpus's only
  quantitative account of dequantization overhead. P3-LLM fuses scales to avoid it but never prices
  what it avoided.
- **The `SYS+ARCH` here is the same reasoning you applied to RaPiD**, and the revision log got there
  first ("the contribution is FlexQ-NDP, a compiler"). That makes the two consistent — and
  strengthens the case for revisiting **BitFusion**, which ships Fusion-ISA plus a compiler and is
  still `ARCH`. Still your call; I haven't touched it.
- **A cost the paper never sizes:** the layout is **quantization-config-specific** — itBlock ratio
  and stride derive from `G_M`, `G_K`, precisions and loop order — so changing QConfig at deployment
  means re-writing the DRAM layout. Never costed.
- **Node convention #3.** 14 nm logic aligned to a 1y-nm DRAM process, alongside logic-die nodes
  (7–65 nm) and P3-LLM's 28→20 nm→×10-density chain. Any aggregate area or efficiency table needs to
  keep DRAM-process entries separate.
- **A small gap:** the 75/25 split — the paper's most valuable number — is reported once, without
  saying which workload or QConfig produced it.
