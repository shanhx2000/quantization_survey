# FATE: Boosting the Performance of Hyper-Dimensional Computing Intelligence with Flexible Numerical DAta TypE

**Venue / Year:** ISCA 2025, pp. 1269-1282 · **Link:** https://doi.org/10.1145/3695053.3731031 · **Reader:** Haoxuan · **Date:** 2026-09-14

## Tags

| | |
|---|---|
| **Level** | `ALGO+ARCH` |
| **Q-oriented** | `Q-ORIENTED` |
| **Data type** | `INT8` `INT4` `TERNARY` `BINARY` `MIXED` |
| **Generation** | `G2` |
| **Optimization** | FPGA · per-dimension mixed precision · DSP/LUT resource split · fuzzing-distance importance measure · pruning as INT0 · power-of-two shift alignment · segment-balanced reordering · HDC |

## 1. One-line summary

Gives **every hypervector dimension its own numeric type** — INT8, INT4, ternary, binary, or
`INT0` (the paper's own notation for *pruned*) — ranked by a **fuzzing-distance** measure computed
from the trained class hypervectors alone and cut to a user-given ratio, so the low-precision
dimensions **leave the FPGA's saturated DSPs** (INT8 HDC occupies 83-90% of DSPs while only 17-41%
of LUTs) and run as LUT logic instead, with a hardwired per-type left shift putting every product
back into one 8-bit frame for a single adder tree — **4.9 effective bits, 38.75% smaller
associative memory at <0.5% accuracy loss, up to 47.14% lower associative-search latency, up to
53.79% (average 17.84%) less energy** on a Kintex-7.

## 2. Data type

**Tensor classes are HDC's, not a DNN's.** Three: **class hypervectors** (the `K × D` associative
memory — the only thing FATE quantizes), **item memory / continuous item memory** (base
hypervectors, binary by construction in HDC), **query hypervector** (the encoded sample).

**Formats — class hypervectors only.** INT8 · INT4 · ternary (stored 2b) · binary (1b) · `INT0` = deleted. One type per dimension, mixed within the same vector.

**Escape hatch — the query hypervector is never quantized.** It is the integer output of XOR-accumulate over binary base hypervectors and enters the multiplier at full width. Only one operand is low-precision.

**Effective bits.** FATE-2 = INT8:INT4:Ternary:Binary 4:3:2:1 → `0.4·8 + 0.3·4 + 0.2·2 + 0.1·1 = 4.9` bits → `1 − 4.9/8 = 38.75%`, exactly the reported AM reduction.

**Granularity — per dimension, i.e. per *column* of the AM, shared by all K classes.** Group size 1, but assigned by rank cut over one sorted list, so each type owns a contiguous slice of the ranking.

**Scale — none stored. The type is the scale.** Low-precision values hold the top bits of the INT8 value; realignment is a fixed left shift, `<<4` INT4, `<<6` ternary, `<<7` binary, done free by zero-concatenation into the adder tree.

**Importance measure.** `f_i = Σ_j |c_ji − median_i|` over the column's K class entries — the minimum edit distance needed to make the column uniform ("fuzzed") and therefore irrelevant to `argmax`. Needs no calibration set, no labels, no gradients.

**Outliers — none.** No outlier mechanism and no argument that one is unnecessary; every dimension is assumed to fit the same power-of-two frame.

**Value-level quantizer — the paper never specifies it.** No rounding rule, clipping range or ternary threshold anywhere in the text.

**Accumulator — not stated.** Products are shifted into a common frame and summed by a `log(d)`-level adder tree; neither product nor accumulator width is given.

**Retraining — not PTQ.** §3.6 compresses, runs the compressed model over the **training set**, and applies HDC's prototype update (subtract from the wrong class, add to the right one) to a retained uncompressed copy, for several rounds. Needs training data; not gradient QAT either.

**Ratio — a user input, not a search.** Automating it is future work.

## 3. Optimization

**The motivation is a resource-imbalance measurement.** On a Kintex-7, INT8 HDC occupies **83-90%
of DSPs** while using only **17-41% of LUTs**; binary HDC uses **0% of DSPs** and 11-31% of LUTs.
Throughput is capped by DSP count with half the fabric idle. Associative search is also **3.05×**
the cost of encoding at D=1000/INT8, so it is the only block worth attacking.

**One ladder for pruning and quantization.** Sort dimensions by fuzzing-distance descending, cut
the sorted list at the user's percentages: head → INT8, middle → INT4/ternary/binary, tail →
`INT0`, deleted. Pruning is the zero-bit rung of the precision scale, not a second mechanism
composed with it — which is why FATE-1 (binary, 50% pruned) loses **<3.5%** where CompHD and
SparseHD lose **23.59%** and **15.93%** at the same AM size.

**Heterogeneous multiplier array.** INT8 lanes on **DSPs**; INT4 and ternary lanes as **LUT-built
multipliers**; binary lanes as a logic gate deciding whether the query value passes or is zeroed.
All lanes register-balanced to a uniform 3-stage pipeline so every bit-width retires together.
Precision is chosen by **which fabric is free**, not by the value distribution.

**Power-of-two shift alignment.** Each type sits at a fixed power-of-two scale, so accumulating
across *precisions* is a hardwired left shift into one shared adder tree — no requantization, no
per-lane scale, no metadata. (Structurally Tender's trick, applied across bit-widths instead of
channel bands.)

**Segment-balanced dimension reordering.** The hypervector is processed in `D/d` segments
(D=1000, d≈100). Contiguous layout would give one segment 80 INT8 / 20 INT4 and another 10 / 90,
needing dynamic scheduling. FATE interleaves dimensions so every segment carries an identical mix,
making the lane precision static and deleting the scheduler. IM and CIM are reordered to match.

**What it costs.** Permutation (`ρ`) is abandoned — after offline dimension deletion it produces
bit errors — and replaced by **redundant storage** of every needed permutation of every base
hypervector (N copies for N-gram order N), argued small and never quantified. Mixed-width storage
adds addressing overhead, asserted smaller than the multiplication saved, never measured.

**Composes with codebook methods.** Stacking FACH (value clustering) onto a 500-dim INT8 FATE
model cuts multiplications by ~90% for 1.2% accuracy at k=64.

## 4. Results

| | |
|---|---|
| Baseline | INT8 HDC and binary HDC, plus CompHD, SparseHD, QuantHD — **all re-implemented by the authors on the same Kintex-7**. CompHD/SparseHD share FATE-1's hardware, so they differ only in accuracy. FACH is listed as a baseline but only ever composed with FATE, never compared |
| Models / datasets | HDC at D=1000 on ISOLET (speech), UCIHAR (activity), CARDIO (disease); plus MNIST / Fashion-MNIST; plus Cora / CiteSeer / NELL node classification |
| Accuracy delta | FATE-2: **<0.5%** vs INT8 HDC. FATE-1: **<3.5%** vs binary HDC at iso-AM-size, against CompHD **23.59%** and SparseHD **15.93%**. QuantHD loses up to **12%**. Importance measure: **+5%** over range-based at best, **slightly worse than range-based on ISOLET** when the INT8 share is high |
| Speedup | **47.14% associative-search latency reduction** (FATE-2, maximum) vs INT8 HDC. **20×** on MNIST and **10×** on graph tasks — but those configurations are binary at half dimensionality |
| Energy / area | **53.79% energy reduction, maximum; 17.84% average.** FATE-4 sits at 78% of INT8. **38.75%** average AM reduction. Resources (ISOLET): FATE-1 29,759 LUT / 50,591 FF / **0 DSP**; FATE-2 45,234 / 45,163 / 260 |
| Technology node | **Xilinx Kintex-7 embedded FPGA, 200 MHz**, Verilog. The corpus's second FPGA entry — LUT/FF/DSP counts are not comparable with mm² at any node |
| Evidence level | **Vivado synthesis reports** — utilisation report for area, power-estimation report for energy, timing for latency. Not a board measurement, not silicon. Accuracy from a separate Python model |
| **Is the comparison fair?** | Iso-substrate and iso-baseline (all baselines re-implemented on the same Kintex-7 at 200 MHz; CompHD/SparseHD share FATE-1's hardware, so those are accuracy-only at iso-memory). Not measured — Vivado utilisation and power estimates. Do not quote **53.79%** (maximum; average 17.84%), the abstract's **"50% speedup"** (a 47.14% latency reduction), or the **20×** (binary at half dimensionality) |

## 5. Comment

**Not an LLM paper.** Hyper-dimensional computing on an FPGA; nothing here transfers to LLM
inference directly.

## 6. Claude notes

*Suggestions from the reading agent. **Strip this section before copying into
`QuantArchSurvey/venues/ISCA/notes/`.***

- **Read-depth flag, first because it matters.** All twelve body pages were read line by line, but
  **every figure is a bitmap in the extraction**. Figures 9-17 hold the per-dataset accuracy /
  latency / energy bars and, worse, the **bit-width ratios defining FATE-3, FATE-4, FATE-5,
  FATE-CV-1..5 and FATE-G1..4**. Only FATE-1 (binary, 50% pruned) and FATE-2 (4:3:2:1) are defined
  in prose. **Verify any per-configuration number against the PDF before citing it**, including
  which dataset gives the 47.14% maximum.
- **The best cross-paper output is the FPGA pair, and it is worth a paragraph.** Both FPGA entries
  open with a DSP utilisation measurement and diagnose opposite failures. `XtraMAC`: the DSP's
  **bit-space** is empty (8.9% for BF16 under upcasting) → **pack more lanes in**. `FATE`: the DSP
  **count** is exhausted (83-90%) while LUTs idle at 17-41% → **move lanes off the DSP entirely**.
  Same substrate, same scarcity claim, opposite fix. That is the strongest available evidence for
  the thread's organising claim that the deciding variable is what the substrate charges for.
- **On the multi-precision-datapath axis FATE is a new node, not a variant.** BitFusion composes
  spatially in one fabric; SamsungNPU and EVA temporally; XtraMAC spatially inside one DSP;
  UniCore removes the multiplier. FATE composes **spatially across two *different* fabrics** —
  nothing else in the corpus does, and it is the only entry where the precision is chosen by which
  fabric is free rather than by the data.
- **On granularity it adds a direction, not just a size: per-reduction-index.** Precision is
  assigned per *column* of the K×D matrix — along the contraction axis, shared by every output
  row — precisely so a lane's precision is a property of the lane and the shift amounts can be
  hardwired. Worth saying in the granularity section that the *direction* of the grouping is a
  design variable, which the axis currently does not capture.
- **Its shift alignment is Tender's move on a different axis.** Tender makes consecutive band
  scales exactly 2× apart so cross-band accumulation is a 1-bit shift; FATE puts its data types at
  2⁰/2⁴/2⁶/2⁷ so cross-*precision* accumulation is a hardwired shift. Same idea: make the ratio
  between scales a power of two and requantization disappears into the wiring.
- **Numbers I would exclude.** (i) The abstract's **"up to 50% speedup"** — it is a rounding of a
  47.14% *latency reduction* (≈1.89×), and printing "1.5×" would be wrong. (ii) **20×** on MNIST
  and **10×** on graphs — FATE-CV-5 is explicitly binary at 50% sparsity, so the speedup is a
  binary-vs-INT8 fact; the citable part is that it costs **no** accuracy. (iii) **"improvements of
  up to 35.68%"** (§5.2) has no stated unit.
- **One inconsistency I could not resolve.** §5.3 opens *"By employing LUT-based multipliers for
  all configurations to overcome DSP limitations…"* over an energy result whose FATE-2 uses 260
  DSPs in Table 5. Which multiplier the energy numbers assume is not recoverable from the text.
- **Seed tags: all four confirmed, and the line-181 ASIC→FPGA amendment is correct.** `INT0` is
  verified as the paper's own notation (§3.3: *"or even INT0, where INT0 indicates that the
  dimension is pruned"*). The LUT trap is confirmed by exhaustive grep — every `LUT` is a Xilinx
  resource; `codebook`, `lookup table` and `table lookup` have **zero** hits. I would **add**
  `fuzzing-distance`, `power-of-two shift alignment` and `segment-balanced reordering` to the
  Optimization cell, and **decline** `FP32` (it appears only as the source format in one ladder
  sentence and as a GNN accuracy column; no FP32 datapath exists).
- **Checked against your `SYS` rule.** The Python "FATE Framework" is a model-compression tool, not
  a compiler, ISA or runtime driving the hardware — no ISA section, no software-stack figure. So
  `ALGO+ARCH`, not `+SYS`.
- **§5 material, if you want it.** Best citation for: *precision assigned by which hardware
  resource is idle rather than by the value distribution*, and for *pruning as the zero-bit rung of
  one precision ladder instead of a second mechanism*. Generation `G2` on paradigm — an
  architecture built to execute quantized arithmetic across bit-widths, the BitFusion family; none
  of the three G3 threads (outliers, weight-only bandwidth, codebooks) is present, and the 2025
  date is irrelevant. The `Q-ORIENTED` caveat, if you want it in §5: the importance measure alone
  would survive as a pure pruning criterion, which is what FATE-1 is.
- **Biggest reproducibility gap, unadmitted.** The value-level quantizer is never specified —
  `round`, `clip`, `threshold`, `saturate`, `truncate` all return zero hits. How an INT8 class
  value becomes INT4 or ternary is left to the reader.
