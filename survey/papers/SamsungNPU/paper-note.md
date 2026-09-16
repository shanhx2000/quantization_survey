# Sparsity-Aware and Re-configurable NPU Architecture for Samsung Flagship Mobile SoC

**Venue / Year:** ISCA 2021 (Industrial Product) · **Link:** https://doi.org/10.1109/ISCA52012.2021.00011 · **Reader:** Haoxuan · **Date:** 2026-09-10

## Tags

| | |
|---|---|
| **Level** | `ARCH` |
| **Q-oriented** | `NON-Q-ORIENTED` |
| **Data type** | `INT8` `INT16` `MIXED` |
| **Generation** | `G2` |
| **Optimization** | mobile NPU · IFM zero-skipping · reconfigurable MAC array · time-multiplexed INT16 · dynamic port assignment · adder-tree inner product · 5 nm silicon · industrial product |

## 1. One-line summary

A shipping Samsung flagship-SoC NPU (5 nm, 3 cores × 2 engines × 1k MACs) whose quantization
content is one section: **INT8 is the design target, and INT16 is supported by time-multiplexing
four INT8 subcomputations (LL/LH/HL/HH) over the same datapath with no extra multiplier or
accumulator** — the temporal design `BitFusion` measured losing 3.5× area to spatial fusion, chosen
anyway because in a real NPU **arithmetic is only 23.4% of an engine** while the weight buffer is
57.1% of the tensor unit; measured at **13.6 TOPS/W and 290.7 FPS** on INT8 Inception-v3.

## 2. Data type

**INT8 is the design target**, not a compromise — "8-bit integer arithmetic is sufficient for most mobile applications, [so] we optimize the proposed NPU for 8-bit integer arithmetic."
**INT16 by time-multiplexing.** A 2-byte operand splits into `F_H/F_L`, `W_H/W_L`; four subcomputations **LL, LH, HL, HH** run on the INT8 datapath, each accumulating into the top 3–4 bytes of the running partial sum. **4 iterations, and zero extra multipliers or accumulators** — only muxing in the data fetcher and vector unit.
**Channel-wise quantization without reshaping**, because the 1-D output feature map tensor is already split along the channel dimension; a quantization unit sits beside the activation unit.
**Outliers.** None. No sub-8-bit path anywhere either.
**Accumulator.** Partial sums grow across subcomputations (`S[3:0]` → `S[4:1]` → …); no fixed width stated.
**Escape hatch.** INT16 for accuracy-critical applications; channel-wise scales.
**Accuracy.** **Inherited by citation** — INT8 costs "1~2%" on well-known image classifiers, cited to [24]. Nothing measured in this paper.
**Retraining.** Not discussed — the NPU consumes whatever the toolchain produces.

## 3. Optimization

**The quantization content is thin, and honestly so** — this is a product paper about a whole NPU:
an adder-tree inner-product engine, IFM zero-skipping at intra- and inter-lane granularity, a
reconfigurable MAC array with a tile/subtile scheme, and dynamic internal memory-port assignment.
Mixed precision is §V-D, one section of eight.

**But that one section settles a question BitFusion opened.** Samsung's INT16 support is exactly the
**temporal** decomposition — four byte-granularity subcomputations recombined by accumulation —
that BitFusion's Fig. 10 measures losing **3.5× area and 3.2× power** to spatial fusion. Samsung,
shipping a flagship SoC three years later, chose temporal anyway.

**The area census explains why, and it's the most useful thing here.** In a real mobile NPU engine:
**tensor unit 68.5%** (weight buffer alone **57.1%** of it, arithmetic circuits **23.4%**), vector
unit **17.0%**, data fetcher 3.4%, **sparsity unit 2.4%**. BitFusion's spatial-vs-temporal
comparison is measured over the multiplier, shifter and accumulator — under a quarter of the area
in a product. So paying *more multipliers* to speed up a capability most workloads don't use is the
wrong trade; four cycles of muxing is right. **BitFusion won the microbenchmark and lost the
product**, and the area table is why.

**The reconfigurability cost is stated too**: the tile/subtile scheme "demands **double** the number
of processing blocks in the vector unit", which is 17.0% of an engine. And the lessons-learned
discussion concedes the inverse — that *limiting* reconfigurability costs little performance while
saving significant area.

## 4. Results

| | |
|---|---|
| Baseline | A dense (no-optimisation) version of the same NPU. No external accelerator comparison |
| Models / datasets | Inception-v3, ResNet-50, MobileNet-v2 — image classification, INT8 |
| Accuracy delta | **None measured.** INT8's "1~2%" is a citation to prior work |
| Speedup | **1.79× from the combined optimisations — simulation, not silicon** |
| Energy / area | **13.6 TOPS/W peak** and **290.7 FPS** (Inception-v3, single core), **131.13 FPS** (ResNet-50) — **measured on silicon**. Area per engine: tensor unit 68.5% (weight buffer 57.1%, arithmetic 23.4%), vector unit 17.0%, data fetcher 3.4%, sparsity 2.4% |
| Technology node | **Samsung 5 nm, fabricated** — the finest measured node in the corpus |
| Evidence level | **Two levels, do not pool.** FPS and TOPS/W are **silicon measurement**; the 1.79× optimisation breakdown is **simulation** |
| **Is the comparison fair?** | Silicon, which almost nothing else here is. But **two evidence levels sit side by side in the abstract** — 13.6 TOPS/W and both FPS figures are measured, the **1.79× is simulation**. As a product paper choices are **reported, not ablated**: nothing justifies the temporal INT16 design against the spatial alternative. Accuracy is a **citation, not a measurement**; 13.6 TOPS/W is a **peak** |

## 5. Comment

## 6. Claude notes

> **Suggestions from the reading agent. Strip this section before copying into
> `QuantArchSurvey/venues/ISCA/notes/`.**

- **Tags human-verified 2026-09-10.** The revision log's `Q` → `non-Q` change is confirmed — third
  and last of the flagged rows
  settled (Ecco → `Q`, LightNobel → `Q`, this one → `non-Q`). Swap the format for plain INT8 and
  zero-skipping, the reconfigurable MAC array, dynamic port assignment and the adder-tree engine
  all survive untouched. INT8 *is* the format; INT16 is a muxing trick in one section.
- **§5 material, if you want it — and I think this is the strongest cross-paper find of the batch.**
  Three papers now form one argument about multi-precision datapaths, and the two that shipped both
  declined BitFusion's answer:

  | Paper | Approach | Cost of flexibility | Evidence |
  |---|---|---|---|
  | BitFusion (ISCA'18) | one fused datapath, **spatial** | shift-add tree = 67% of the Fusion Unit | 45 nm synthesis |
  | RaPiD (ISCA'21) | **two separate pipelines** | ~16% area for the INT pipeline | 7 nm silicon |
  | SamsungNPU (ISCA'21) | one datapath, **temporal** | **zero extra multipliers — muxes only** | 5 nm silicon |

  BitFusion measures temporal losing **3.5× area / 3.2× power** — and this paper's own area table
  says why that didn't decide anything: **arithmetic is 23.4% of an engine**. Optimising the
  multiplier optimises a quarter of the area, and paying for it with *more* multipliers is wrong
  when the capability is the exception case. **A microbenchmark result not surviving contact with a
  product** is worth a paragraph.
- **It and RaPiD disagree productively, and the framing is more useful than either alone.** RaPiD
  builds a *second pipeline* for low precision because low precision is its **main** case (FP8
  training, INT4 inference). SamsungNPU *time-multiplexes* high precision onto the low one because
  high precision is its **exception** case. Same problem, opposite majority assumption, opposite
  answer.
- **The corpus's only product-grade area census.** Weight buffer 57.1% of the tensor unit,
  arithmetic 23.4%, sparsity 2.4%, reconfigurability doubling vector-unit blocks. Every
  simulation-based entry reports area for the datapath it designed; this reports what a whole
  shipping engine looks like. Useful for sanity-checking any "X% area overhead" claim elsewhere.
- **Careful with the abstract.** 13.6 TOPS/W / 290.7 FPS / 131.13 FPS are measured; the **1.79× is
  simulated**, and they're presented together. Only the first set goes in a measured column.
- **Author list transcribed** (23 authors, Samsung SAIT / Semiconductor / Electronics) — the entry
  previously said "not transcribed".
- Checked against your `SYS` rule: a toolchain is implied but never described, no compiler or ISA
  section, so `ARCH` alone stands.
