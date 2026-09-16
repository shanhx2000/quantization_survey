# FATE — paper notes

**FATE: Boosting the Performance of Hyper-Dimensional Computing Intelligence with Flexible Numerical DAta TypE**
Haomin Li, Fangxin Liu, Yichi Chen, Zongwu Wang, Shiyuan Huang, Ning Yang, Dongxu Lyu, Li Jiang
(Shanghai Jiao Tong University · Shanghai Qi Zhi Institute · Tianjin University)
**ISCA 2025**, pp. 1269-1282 ｜ DOI: **10.1145/3695053.3731031**
Publication info verified 2026-09-09: venue, year, page range and DOI all read out of the
archived PDF's own text (ACM copyright block and page footers on p1/p14).
Archived here: the **published ACM version**, 14 pages.

Status: **note ready** ｜ Last updated: 2026-09-14 ｜ **Human-checked 2026-09-14** — tags confirmed; §5 supplied by the human.
Tags: `analytical-dtype` `mixed-precision` `dtype-granularity` `multi-bitwidth-hw` `accelerator`
How far it was read: **full close read of the twelve body pages, 1269-1280** — abstract, §1
introduction, §2 background/motivation (Table 1, Table 2, Figure 3's utilisation percentages),
§3 the whole FATE framework (§3.1-§3.6: dimensional analysis, the fuzzing-distance equation,
mixed bit-width alignment, the permutation/redundant-storage problem, online inference, the
adjustment loop), §4 the FPGA implementation (§4.1-§4.4: architecture, encoding, associative
search with the shift amounts, pipeline), §5 evaluation (§5.1-§5.9) and §6-§7 related work and
conclusion, all read line by line.
**What could not be read, and it is load-bearing: every figure is a bitmap in the extraction.**
Figures 9-17 carry the per-dataset accuracy, latency, energy, resource-utilisation and speedup
bars, and Figure 9(a)/16(a)/17(a) carry the **bit-width ratio definitions of FATE-3, FATE-4,
FATE-5, FATE-CV-1..5 and FATE-G1..4**. Only FATE-1 (binary, 50% pruned) and FATE-2
(INT8:INT4:Ternary:Binary = 4:3:2:1) are defined in prose. Every number below therefore comes
from prose or from Tables 1-6; anything that exists only as a bar is recorded as unresolved.

> Publisher record: https://dl.acm.org/doi/10.1145/3695053.3731031
> **There is no arXiv version** (arXiv API title search, 2026-09-02). The PDF was downloaded by
> a human and filed through [`survey/uploads/`](../../uploads/); see
> [`Notes-002`](../../../Claude/notes/Notes-002-paper-source-access.md).
> The PDF is **not committed** (2.6 MB) and **cannot be re-downloaded by script** — both
> publishers 403. Re-extract with `python3 extract.py` → `extracted/` (committed).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, ISCA 2025 row.

---

## Brief

*(Written from an abstract-level read on 2026-09-09. **Four corrections from the close read are
listed under "What the close read changed" below**; the text is left as written so the diff is
visible.)*

### 1. Motivation

Hyper-dimensional computing encodes data into very long vectors, and cosine similarity over
them needs multiplications the edge cannot afford. Binary HDC removes the multipliers but
costs accuracy. Everyone quantizes **every dimension the same way** — and that is the waste,
because the dimensions are not equally important, and because an FPGA has two kinds of
resource (DSPs and LUTs) that suit two different precisions.

### 2. Overview

Assign **a different numeric data type per dimension**, chosen by a new **dimensional
fuzzing-distance** importance measure. Important dimensions stay INT8 and run on **DSPs**;
unimportant ones drop to INT4, ternary or binary and run as **logic on FPGA LUTs**, where
multiplication becomes a logic calculation; the least important are given `INT0`, meaning
pruned outright. A workload-aware mixed scheme picks the ratio, so the compression target and
the FPGA's resource mix are solved together rather than in sequence. Prototyped on a Kintex-7.

### 3. Pros and cons

**Pros**

- The per-dimension assignment is a genuine **granularity** contribution, and the importance
  measure is the part that makes it more than a heuristic.
- Rare and valuable framing: the precision ladder is chosen to **match heterogeneous hardware
  resources**, not only to match the data. Low precision goes where LUTs are idle. Most
  mixed-precision work assumes one homogeneous datapath.
- Sparsity is folded into the same ladder rather than bolted on — `INT0` makes pruning the
  bottom rung of the precision scale instead of a separate mechanism.
- Honest headline: up to 50% speedup and 53.79% energy saving are stated against *the same
  design using DSPs for all dimensions*, which is the right baseline.

**Cons**

- Accuracy is preserved "under 0.5%" loss, but the ratios are found by design-space
  exploration per workload; the paper's own future work is to automate that search, which
  concedes it is currently manual.
- FPGA-specific by construction. The DSP/LUT split has no ASIC analogue, so the numbers do not
  transfer to the rest of this corpus.
- HDC is a niche workload; the importance measure's generality beyond it is untested.

### 4. Where it applies

A **fine-grained mixed-precision** entry (§2.2), and the corpus's clearest case of precision
chosen by *hardware resource* rather than by value distribution — pair with
[`XtraMAC`](../XtraMAC/ANALYSIS.md) as the other FPGA entry, and with
[`DRQ`](../DRQ/ANALYSIS.md) and [`LightNobel`](../LightNobel/ANALYSIS.md) on granularity.

**Watch the word "LUT" here.** FATE's LUTs are **FPGA lookup-table logic resources**, not the
lookup-table-GEMM/codebook idea of [`LUTTensorCore`](../LUTTensorCore/ANALYSIS.md),
[`OASIS`](../OASIS/ANALYSIS.md), [`Omni-LUT`](../Omni-LUT/ANALYSIS.md) and
[`Mokey`](../Mokey/ANALYSIS.md). Do not tag it into that thread.

### What the close read changed

1. **"A workload-aware mixed scheme picks the ratio" is wrong — the *user* picks the ratio.**
   §3.1: the second input to FATE is a "compression requirement … mainly about the rate of each
   kind of bit-width that the users wish to use." The "workload-aware mixed scaling strategy" of
   the abstract is, in the body, (a) that user-supplied ratio plus (b) the segment-balanced
   dimension reordering of §3.4 that makes *any* ratio schedulable. **There is no search**, and
   §7's future work says so explicitly.
2. **"Honest headline" is too generous.** 53.79% energy and 47.14% latency are **maxima**; the
   average energy reduction is **17.84%** and appears in the same sentence. The abstract's
   "up to 50% speedup" is a rounded restatement of a **47.14% latency reduction** (≈1.89×), not
   a 1.5× speedup — the word "speedup" is used to mean "latency reduction".
3. **"Prototyped on a Kintex-7" needs a qualifier.** All numbers come from **Vivado utilisation
   and power-estimation reports** at 200 MHz (§5.1); the paper never reports a board measurement.
4. **The importance measure is weaker than "more than a heuristic" implies.** Its own ablation
   (§5.5, Fig. 14(b)) concedes it is **"slightly worse than the range-based method on ISOLET"**
   when the INT8 share is high. It always beats random; it does not always beat range.

The LUT warning, the `INT0` reading and the per-dimension granularity claim all **survive**
verification — see below.

---

## Conclusions

**The word "LUT" is an FPGA resource here and nowhere near LUT-GEMM. Verified by exhaustive
grep, not by not-having-noticed.** Every occurrence of `LUT`/`LUTs` in the full text is either a
Xilinx resource count (Figure 3's `LUT(INT8)`/`LUT(Binary)` legend, Table 5's `LUT` rows), the
phrase "FPGA Look-Up Table (LUT) resources", or a block name in Figure 7 (`LUT based Multiplier`,
`LUT based Multiplexer`) meaning *combinational logic built out of LUT primitives*. The strings
`codebook`, `lookup table`, `table lookup` and `look-up table` (other than the resource
expansion) appear **zero times**; `VQ`/`vector quantization` appears only in reference [6]'s
title. **verified**

**`INT0` is the paper's own notation, and it is the interesting move.** §3.3, p1273: *"In HDC, we
unify these two operations into one operation, which is to reduce the data bit-width. For
example, reducing from FP32 to INT8, Ternary, Binary, or even INT0, where INT0 indicates that the
dimension is pruned."* Pruning is not a second mechanism bolted onto quantization; it is the
bottom rung of one precision ladder, and it falls out of a single sorted list. **verified**

**The granularity is per-dimension, and "dimension" means a *column* of the associative
memory — the reduction axis, shared across all classes.** §3.2 recasts the associative search as
`argmax_i (C · S)` where `C` is the `K × D` class-hypervector matrix; a "dimension" is one column
index `i`, i.e. one element position shared by **all K class hypervectors** and by the query.
That choice is what makes the hardware simple: the precision of a lane is a property of the lane,
not of the row being computed, so every class is processed by the same mixed multiplier array in
the same cycle and the shift amounts are hardwired per lane. **verified** (§3.2 Eq. 2, §4.3)

**The importance measure is a median-deviation statistic, not a gradient or a Hessian.** §3.2,
Eq. 3: for column `i` with elements `{c_1i … c_Ki}` and median `median_i`,
`f_i = Σ_j |c_ji − median_i|`. The motivating idea is the *fuzzed dimension*: a column whose
entries are all equal cannot influence `argmax`, so importance is the minimum edit distance
needed to fuzz the column to a single value. It requires **only the trained class hypervectors**
— no calibration data, no labels, no gradients. **verified**

**The scale is the shift, and there is no scale metadata at all.** §4.3: *"the INT4 results are
shifted 4 bits to the left, the ternary results are shifted 6 bits to the left, and the binary
results are shifted 7 bits to the left"*, with a worked example (`54 × 3 = 162`, `162 << 4 =
2,592`). So each low-precision format holds the **top bits of the 8-bit class value** and the
left shift restores the INT8 alignment before the adder tree; the "scale" of a dimension is a
power of two implied by its data type. **No per-dimension, per-group or per-tensor scale factor
is ever stored or transmitted.** **verified** (§4.3, p1275-1276)

**The effective bitwidth is derivable and reproduces the paper's own headline exactly.** FATE-2
is INT8:INT4:Ternary:Binary = 4:3:2:1, and ternary must be stored in 2 bits for the shift by 6 to
be consistent. Then `0.4·8 + 0.3·4 + 0.2·2 + 0.1·1 = 4.9` bits per element, and
`1 − 4.9/8 = 38.75%` — **exactly** the "average storage reduction of 38.75%" reported in §5.2.
The derivation confirms both that ternary occupies 2 bits and that **nothing else is stored**.
**inferred, but an exact match to the reported figure**

**The motivating measurement is a resource-imbalance measurement, and it is the mirror image of
`XtraMAC`'s.** Figure 3, p1272: on a Kintex-7, INT8 HDC occupies **87% / 90% / 83% of DSPs** on
speech / activity / disease while using only **38% / 41% / 17% of LUTs**; binary HDC uses **0%
DSPs** and **31% / 27% / 11% of LUTs**. The DSP is exhausted, the LUT fabric is idle, and the
throughput ceiling is a DSP count. **verified**

**One admitted-then-buried inconsistency.** §5.3's framing sentence reads *"By employing
LUT-based multipliers for all configurations to overcome DSP limitations, FATE-2 achieves a
maximum energy consumption reduction of 53.79%…"* — which does not obviously square with the
architecture's DSP-for-INT8 story, nor with Table 5, where FATE-2 uses **260 DSPs** on ISOLET.
The energy comparison's exact configuration is therefore ambiguous. **flagged, unresolved**

---

## Method

**Inputs (§3.1)** **verified**. Two: a trained HDC model (IM, CIM, AM) and a *compression
requirement* — the percentage of dimensions the user wants at each bit-width. Three modules:
dimensional analysis, mixed bit-width alignment, compression.

**Dimensional analysis (§3.2)** **verified**. Cosine similarity is reduced to a dot product
(`1/|S|` is common to all classes; `1/|C_i|` drops if class hypervectors are normalised — a
stated precondition), giving `argmax_i (C·S)` over a `K × D` matrix. Column importance is the
**fuzzing-distance** `f_i = Σ_j |c_ji − median_i|` (Eq. 3).

**Mixed bit-width alignment (§3.3)** **verified**. Sort columns by `f_i` descending; cut the
sorted list at the user's percentages; head gets INT8, tail gets ternary/binary, the last slice
gets `INT0` = deleted. Worked example in the paper: 50% INT8 / 30% INT4 / 20% pruned.

**Fine-grained compression + segment reordering (§3.4)** **verified**. Because the hypervector is
processed in `D/d` segments (`D = 1000`, `d = 100` in the running example), a naive contiguous
layout would give one segment "80 INT8 and 20 INT4" and another "10 INT8 and 90 INT4" — an
unbalanced workload needing dynamic scheduling. FATE **interleaves the dimensions so every
segment carries the same mix** (50/50 in the example), which removes scheduling entirely and
makes the per-lane precision assignment static. IM and CIM are reordered and pruned to match.

**Permutation is removed, at a storage price (§3.4, Fig. 5)** **verified**. HDC's `ρ` (rotational
shift) encodes position, but after offline dimension deletion `ρ(prune(s)) ≠ prune(ρ(s))`, so
permuting a pruned base hypervector produces bit errors. FATE's answer is **redundant storage**:
precompute and store the pruned version of every permutation that will be needed — for N-gram
with `N = 4`, all of `s, ρ(s), ρ²(s), ρ³(s)` per character. Argued acceptable because `N` is
small and base hypervectors are binary.

**Adjustment mechanism (§3.6)** **verified** — and this is the retraining requirement. Compress;
keep the uncompressed copy; run inference on the **training set** with the compressed model;
for each misclassified sample apply HDC's standard update (subtract the sample hypervector from
the wrong class, add it to the right one) **to the uncompressed copy**; recompress; repeat for
several rounds. So FATE is **not PTQ**: it needs the training set and a compress-evaluate-update
loop. It is also not gradient QAT — HDC retraining is a perceptron-style prototype update.

**Architecture (§4.1-§4.4)** **verified**. Two blocks. *Encoding*: base-hypervector memory →
XOR accumulation array → segment buffer producing query segments `Q_i` of `d ≈ 100` dimensions.
*Associative search*: compressed class-hypervector RAM → **hybrid bit-width multiplier array**
(INT8 lanes on **DSPs**; INT4 and ternary lanes as **LUT-built multipliers**; binary lanes as a
**logic gate deciding whether the query value passes through or is zeroed**) → **per-lane left
shift** (`<<4` INT4, `<<6` ternary, `<<7` binary) → **`log(d)`-level adder tree**. The shift is
implemented free, "by concatenating the multiplication result with zero bits". Multiplier lanes
are register-balanced to a uniform **3-stage** pipeline so all bit-widths retire together;
`II = 1` per segment is implied but never stated as such.

**Composability with FACH (§5.6)** **verified, and it is a composition experiment, not a
baseline comparison.** FACH clusters AM values and pre-accumulates query elements sharing a
cluster, removing multiplications. FATE-FACH applies FACH *on top of* a 500-dimension INT8 FATE
model. Table 4 is the only place FACH appears numerically — **§5.1 lists FACH as a baseline but
no head-to-head FATE-vs-FACH comparison exists.**

---

## Key numbers, with their frame

**Evidence level, stated once and not to be pooled with anything else in this corpus:**
**Verilog on a Xilinx Kintex-7 at 200 MHz, synthesised in Vivado; latency from the Vivado
timing/latency report and energy from the Vivado power-estimation report (§5.1); resource counts
from the Vivado utilisation report (§2.3 footnote 1, Table 5).** This is a **synthesis-report
estimate**, not a board measurement and not silicon. The software side (accuracy) is a Python
model on an Intel Xeon Silver 4208. All baselines — CompHD, SparseHD, QuantHD, INT8 HDC,
binary HDC — are **re-implemented by the authors on the same FPGA**, not quoted (§5.1).
All main-body models use **D = 1000 dimensions**.

| Setting | Model / dataset | Metric | Baseline | Result | Source |
|---|---|---|---|---|---|
| **The motivation** | Speech / Activity / Disease, D=1000, Kintex-7 | DSP utilisation, INT8 HDC | — | **87% / 90% / 83%** | Fig. 3, p1272 **verified** |
| " | same | LUT utilisation, INT8 HDC | — | **38% / 41% / 17%** | Fig. 3 **verified** |
| " | same | DSP / LUT utilisation, binary HDC | — | **0% / 31%, 27%, 11%** | Fig. 3 **verified** |
| " | D=1000, INT8 | associative-search cost vs encoding cost | — | **3.05× higher** (average) | §1, p1270 **verified** |
| " | Speech, INT8 vs binary | associative-search energy / latency | INT8 | **6.345 → 0.705 µJ**, **87 → 9.67 µs**, accuracy **90.57 → 78.45%** | Table 1 **verified** |
| **Storage** | FATE-2, avg over ISOLET/HAR/CARDIO | AM size reduction | INT8 HDC, D=1000 | **38.75%** (average), accuracy loss **< 0.5%** | §1 p1271, §5.2 p1277 **verified** |
| " | FATE-2 | effective bits per AM element | 8 | **4.9** (`0.4·8+0.3·4+0.2·2+0.1·1`) | derived; reproduces 38.75% exactly **inferred** |
| **Latency** | FATE-2 (INT8:INT4:Tern:Bin = 4:3:2:1) | associative-search latency reduction | INT8 HDC (DSP-only), same FPGA | **47.14% — a MAXIMUM, dataset not named in prose**; < 0.5% accuracy loss | §5.2 p1277 **verified** |
| " | — | abstract's phrasing of the same result | — | **"up to 50% speedup"** — a rounding of the 47.14% latency reduction, *not* a 1.5× factor | Abstract vs §5.2 **inferred** |
| **Energy** | FATE-2 | energy reduction | INT8 HDC | **53.79% MAXIMUM; 17.84% AVERAGE** | §5.3 p1277 **verified** |
| " | FATE-4 | energy | INT8 HDC | **78% of INT8** (average) | §5.3 **verified** |
| " | FATE-1 | energy | **binary** HDC (not INT8) | **50% average saving**, by pruning half the dimensions | §5.3 **verified** |
| " | FATE-* | multiplier share of associative-memory power | original HDC | **~10 percentage points lower** on average | §5.3, Fig. 12 **verified** |
| **vs sparsity baselines** | FATE-1, binary, half dims pruned, **iso-AM-size** | accuracy loss vs binary HDC @ D=1000 | CompHD / SparseHD | **FATE < 3.5%** vs **CompHD 23.59%**, **SparseHD 15.93%** | §5.2 p1277 **verified** |
| " | binary HDC, 80% sparsity | accuracy advantage | CompHD / SparseHD | **+32% / +20%** (best case) | §5.4 p1278 **verified** |
| " | INT8 HDC, 50% sparsity | accuracy advantage | CompHD / SparseHD | **+5% / +3%** (average) | §5.4 **verified** |
| " | 30% sparsity | accuracy advantage | best of the two | **binary >10%, INT8 >4%** | §5.4 **verified** |
| " | ISOLET | iso-accuracy point | CompHD | **FATE @ 90% sparsity ≈ CompHD @ 20% sparsity** | §5.4 **verified** |
| **vs quantization baseline** | ternary/binary mixes | accuracy | QuantHD (binary or ternary only) | QuantHD loses **up to 12%** worst case; FATE matches ternary accuracy on HAR **with 20% of dimensions binary** | §5.2, §5.5 **verified** |
| **Importance-measure ablation** | FATE-Q1..Q6 | accuracy vs alternative metrics | random / range-based | **+5% over range-based** (best case, HAR); **"slightly worse than range-based on ISOLET"** when the INT8 share is high; always ≥ random | §5.5 p1278 **verified** |
| **Composability** | FATE @ 500 dims INT8 + FACH | accuracy / multiplications per inference | FATE alone (13000 / 6000 / 5000 mults) | k=256: **−50%+ mults, near-lossless**; k=64: **−~90% mults, −1.2% acc**; k=32: **−~95% mults, −2.7% acc** | Table 4, §5.6 **verified** |
| **Resources** | ISOLET | LUT / FF / DSP | — | FATE-1 **29,759 / 50,591 / 0**; FATE-2 **45,234 / 45,163 / 260**; FATE-3 **55,520 / 71,253 / 520**; FATE-4 **55,158 / 61,203 / 468**; FATE-5 **48,697 / 39,694 / 546** | Table 5 **verified** |
| " | HAR | LUT / FF / DSP | — | FATE-1 **18,716 / 29,398 / 0**; FATE-2 **27,339 / 26,857 / 120**; FATE-3 **36,261 / 40,926 / 240**; FATE-4 **35,324 / 34,830 / 144**; FATE-5 **32,552 / 26,591 / 252** | Table 5 **verified** |
| **Vision** | MNIST, FATE-CV-5 (= binary + 50% pruned) | speedup | INT8 HDC | **up to 20×, no accuracy loss** | §5.8 p1279 **verified** — see hazard 3 |
| " | Fashion-MNIST, FATE-CV-4 (INT4+ternary+binary) | AM size / compression | INT8 HDC | **34.18 KB, 2.8×, lossless**; ternary-only is 24.41 KB but **−~3% accuracy** | §5.8 **verified** |
| **Graph** | Cora / CiteSeer / NELL, FATE-G4 | speedup / compression | INT8 HDC | **up to 10× / 3×, no accuracy loss** | §5.9 p1279 **verified**; FATE-G4's ratio is figure-only |
| " | Cora / CiteSeer / NELL, FP32 | accuracy | GCN / GIN | HDC **82.6 / 72.0 / 68.2** vs GCN **81.5 / 71.1 / 66.0** | Table 6 **verified** — a property of the HDC model, not of FATE |
| **Substrate context** | all baselines | FPGA vs GPU | AMD **Radeon R390** (2015), OpenCL | FPGA ≈ **8× energy efficiency, 2× speed** — mentioned once, then the FPGA versions are used as the baselines | §5.1 footnote 2 **verified** |

### Citation hazards

1. **53.79% is a maximum whose average is 17.84%, and both are in the same sentence.** Quoting
   the abstract's "53.79% energy saving" without "average 17.84%" misrepresents the paper.
   Same shape as `SmartExchange` / `Ecco` / `NDPLowBitFP`.
2. **"Up to 50% speedup" (abstract) is not a speedup factor.** It is a rounding of §5.2's
   **47.14% latency reduction** for FATE-2, i.e. ≈1.89×. The paper uses "speedup" to mean
   "latency reduction". Do not print "1.5×".
3. **The 20× (MNIST) and 10× (graph) headline speedups are not evidence for mixed precision.**
   FATE-CV-5 is explicitly *"prunes 50% of the dimensions in the binary HDC implementation"* — a
   **binary** model at half dimensionality. The 20× over INT8 HDC is therefore a
   binary-versus-INT8-datapath fact plus 2× fewer dimensions; FATE's contribution there is that
   it costs **no accuracy**, not that it is fast. Cite it for the accuracy claim, not the speed.
4. **CompHD and SparseHD have no independent hardware numbers.** §5.2: *"CompHD and SparseHD are
   not listed separately because they share the same hardware implementation as FATE-1."* The
   comparison against them is **accuracy-only, at iso-memory and iso-hardware** — which is
   defensible, but it means there is no latency or energy win over them to quote.
5. **FACH is named as a baseline and never compared against.** §5.1 lists it among the
   state-of-the-art comparisons; the only FACH numbers in the paper (Table 4) are for
   FATE-**with**-FACH.
6. **§5.3's opening clause contradicts the architecture.** *"By employing LUT-based multipliers
   for all configurations to overcome DSP limitations"* sits over an energy result whose FATE-2
   configuration uses 260 DSPs in Table 5. Which multiplier implementation the energy numbers
   assume is not resolvable from the text.
7. **"Improvements of up to 35.68%" (§5.2) has no unit.** The sentence — *"FATE-1 and FATE-2
   surpass other designs (CompHD and SparseHD) with improvements of up to 35.68%"* — sits between
   an accuracy discussion and a storage discussion. Do not quote it.
8. **The 47.14%, the <0.5% and the 38.75% are not all the same frame.** 38.75% is an average
   across three datasets; 47.14% is a maximum; "<0.5% accuracy loss" is stated for FATE-2 without
   saying whether it is the average or the worst case. The per-dataset values are figure-only.

---

## Cost and requirements

| | |
|---|---|
| **Retraining** | **Not PTQ.** §3.6's adjustment mechanism runs the compressed model over the **training set**, finds misclassifications and applies HDC's prototype update to a retained uncompressed copy, for several rounds. It needs training data and labels. It is not gradient QAT either — HDC retraining is a perceptron-style add/subtract on class hypervectors, so "iterative compress-and-update retraining" is the honest label |
| **Ratio search** | **Manual.** The bit-width percentages are a **user input** (§3.1) explored by design-space exploration; §7 names an automated binary-search loop as *future work* |
| **Offline reordering** | Dimensions are permuted globally so that every segment carries an identical bit-width mix (§3.4). IM, CIM and AM must all be reordered consistently, and the ordering is baked in at deployment |
| **Permutation storage** | HDC's `ρ` operator is **abandoned** and replaced by **redundant storage** of every needed permutation of every base hypervector (N copies for N-gram order N). Argued small because base hypervectors are binary; **never quantified** |
| **Addressing** | Mixed bit-width storage "introduces some addressing overhead", asserted to be smaller than the multiplication saved (§4.3). **Not measured** |
| **Scale metadata** | **None.** The data type *is* the scale; realignment is a hardwired per-lane left shift (`<<4`/`<<6`/`<<7`) |
| **Accumulator** | **Not stated anywhere.** Products are shifted into a common 8-bit-aligned frame and summed by a `log(d)`-level adder tree; neither the product width nor the accumulator width is given, and whether the reported LUT/FF counts include it can only be assumed from Table 5 being a whole-design utilisation report |
| **Datapath cost** | Three multiplier implementations coexist (DSP for INT8, LUT-built for INT4/ternary, a pass/zero gate for binary), plus per-lane shifters and register balancing to a uniform 3-stage pipeline |
| **Substrate** | **FPGA-only economics.** The entire argument is that DSPs are exhausted at 83-90% while LUTs sit at 17-41%; on an ASIC, where multiplier width is a free design variable, there is no idle second resource to migrate work onto |
| **Precondition** | Class hypervectors must be **normalised** for the cosine-to-dot-product reduction to hold (§3.2) |

---

## Limitations and open questions

**Admitted.** (i) The compression ratio is chosen by the user and explored by hand; automating it
is future work (§7). (ii) The importance measure is *"slightly worse than the range-based
method on ISOLET"* when the high-bit-width share is large (§5.5). (iii) Mixed bit-width storage
adds addressing overhead (§4.3). (iv) FATE-3's *"less smooth bit-width change"* costs an average
3% accuracy against INT4 HDC (§5.2) — i.e. the ratio choice is fragile in a way the paper shows
but does not characterise.

**Unadmitted, and material.**

1. **The value-level quantizer is never specified.** The paper gives bit-widths and shift
   amounts and nothing else: `round`, `clip`, `threshold`, `saturate`, `truncate` and
   `two's complement` return **zero hits** in the full text (grepped). How an INT8 class value
   becomes an INT4, ternary or binary value — rounding rule, clipping range, whether ternary is
   `{−1,0,1}` with a threshold or a top-2-bits truncation — is left to the reader. This is the
   single biggest gap for anyone trying to reproduce the accuracy numbers.
2. **No outlier mechanism, and no discussion of why one is not needed.** `outlier` appears only
   in a reference title. Class hypervectors are bundled sums, so their distributions may well be
   benign — but the paper does not say so, and every dimension's dynamic range is silently
   assumed to fit the same power-of-two frame.
3. **Two evidence levels, presented as one.** Accuracy comes from a Python model; latency,
   energy and area come from Vivado reports. Neither is a measurement of a running board.
4. **Only one FPGA part, one frequency, one dimensionality.** Kintex-7, 200 MHz, D = 1000. The
   whole argument turns on a specific DSP:LUT ratio; how the design behaves on a DSP-rich part
   (or a Versal with AI Engines) is not examined, and the claim "embedded FPGA devices have a
   limited number of DSPs, typically not exceeding 1,000" (§4.3) is asserted, not surveyed.
5. **The importance measure ignores the query.** `f_i` is computed from the class hypervectors
   alone (Eq. 3). A dimension where classes differ but the encoder rarely produces a large query
   value contributes little in practice, and the measure cannot see that. No sensitivity to the
   data distribution is reported.
6. **The per-dimension assignment is static for the model's lifetime.** No runtime adaptation,
   no per-input reconfiguration — which is a reasonable design choice, but it makes FATE
   design-time in the same sense as `OLAccel`, not runtime like `DRQ` or `LightNobel`.
7. **Generality beyond HDC is claimed structurally and never tested.** §6.1 argues DNN
   compression does not transfer to HDC; the converse — whether fuzzing-distance means anything
   for a weight matrix — is not attempted.

**Unresolved by this read (figure-only).** The bit-width ratios defining FATE-3, FATE-4, FATE-5,
FATE-CV-1..5 and FATE-G1..4; every per-dataset accuracy, latency and energy value; the
utilisation percentages in Figure 15; which dataset gives the 47.14% maximum. Anyone citing a
per-configuration number must read the figures in the PDF.

---

## Relation to other entries

**It is the corpus's second FPGA entry, and together with `XtraMAC` it makes the substrate
argument twice, from opposite ends.** The multi-precision-datapath thread's organising claim is
that *the deciding variable is what the substrate charges for*. Both FPGA papers open with a
utilisation measurement, and they diagnose **two different failures of the same resource**:

| | `XtraMAC` (ISCA'26) | **`FATE` (ISCA'25)** |
|---|---|---|
| Diagnosis | The DSP's **bit-space** is empty — **8.9%** effective utilisation for a BF16-based MAC under operand upcasting | The DSP **count** is exhausted — **83-90%** of DSPs used by INT8 HDC while LUTs sit at **17-41%** |
| Scarce thing | bits inside one DSP | DSP slices on the die |
| Fix | **pack more lanes into the DSP** at bit-precise offsets | **move low-precision lanes off the DSP** into LUT fabric |
| Composition | spatial, in DSP bit-space | **spatial, across two heterogeneous fabrics** |
| What chooses the precision | the checkpoint (formats mix in one forward pass) | **the resource mix** — precision is assigned to fill idle LUTs |
| Alignment cost | per-lane leading-zero normalisation | per-lane hardwired left shift (`<<4`/`<<6`/`<<7`), free |
| Accumulation | INT and FP paths deliberately **separate** | one adder tree, because everything is integer in a common frame |

Placed on the multi-precision-datapath axis, FATE is a **new node, not a variant of an existing
one**: BitFusion composes spatially inside one homogeneous fabric, SamsungNPU and EVA compose
temporally, XtraMAC composes spatially inside one DSP, UniCore removes the multiplier — and
**FATE composes spatially across two *different* fabrics**, which no other entry does. Its
precision assignment is not driven by accuracy sensitivity alone but by *which fabric is free*,
and that is the cleanest instance in the corpus of the survey's own organising claim.

**On granularity it adds a genuinely new position: per-reduction-index.** The axis so far runs
per-layer (`BitFusion`, `OLAccel`) → per-region (`DRQ`) → per-channel (`Tender`) → per-group
(`Oaken`, `MicroScopiQ`) → per-head (`P3-LLM`) → per-token (`LightNobel`) → per-rank
(`SingularBit`). FATE assigns precision **per column of the weight matrix — i.e. along the
contraction axis, shared by every output row**. That direction is chosen for a hardware reason:
a lane's precision becomes a property of the lane, so the shift amounts are hardwired and no
per-row reconfiguration is ever needed. Anyone reading the granularity axis should note that the
*direction* of the grouping, not just its size, is a design variable, and FATE is the entry that
makes that visible.

**Its shift-alignment trick is `Tender`'s, arrived at independently.** Tender constrains
consecutive channel-band scales to be **exactly 2× apart** so that accumulating across bands is a
1-bit shift instead of a floating-point requantization. FATE's data types sit at fixed
power-of-two scales (`2⁰`, `2⁴`, `2⁶`, `2⁷`) so that accumulating across *precisions* is a
hardwired shift into one adder tree. Same structural move — **make the ratio between scales a
power of two so requantization disappears into the wiring** — applied to a different axis. Worth
a sentence in the survey wherever scale alignment is discussed.

**Pruning-as-`INT0` belongs with the outlier-currency and sparsity threads by contrast.** Where
`MicroScopiQ` *pays* for an outlier by pruning a neighbour in the same micro-block and `OliVe`
destroys a victim, FATE has no outliers at all: pruning is simply the zero-bit end of one
monotone precision ladder over a single sorted list. It is the corpus's cleanest statement that
**pruning and quantization can be one mechanism rather than two composed ones** — the same claim
`SparseHD` and `CompHD` make separately and lose 15.93% / 23.59% accuracy doing.

**Do not put it in the LUT/codebook thread.** `LUTTensorCore`, `OASIS`, `Omni-LUT`, `Mokey`,
`TransitiveArray` and `EVA` resolve *computation* by table lookup. FATE's LUTs are Xilinx logic
primitives. The word is a false friend and the seed row already flags it; this read confirms it
by exhaustive grep.

**Static, design-time precision assignment** puts it with `OLAccel` and `BitFusion` on the
static-vs-dynamic axis, against `DRQ`'s runtime region prediction and `LightNobel`'s runtime
top-k.

---

## For the note

**§1 one-line summary.**

> Gives **every hypervector dimension its own numeric type** — INT8, INT4, ternary, binary or
> `INT0` (the paper's notation for *pruned*) — ranked by a **fuzzing-distance** measure
> (`f_i = Σ_j |c_ji − median_i|`, computed from the trained class hypervectors alone) and cut to
> a user-given ratio, so the low-precision dimensions **leave the FPGA's saturated DSPs** (INT8
> HDC occupies 83-90% of DSPs while only 17-41% of LUTs) and run as LUT logic instead, with a
> hardwired per-type left shift (`<<4`/`<<6`/`<<7`) putting every product back in one 8-bit frame
> for a single adder tree — **4.9 effective bits, 38.75% smaller associative memory at <0.5%
> accuracy loss, up to 47.14% lower associative-search latency and up to 53.79% (average 17.84%)
> less energy** on a Kintex-7.

**Proposed tags — all four seeds confirmed; I would extend only the Optimization cell.**

| Axis | Value | Evidence |
|---|---|---|
| **Level** | **`ALGO+ARCH`** — seed agrees | The fuzzing-distance measure, the alignment rule and the compress-and-update loop are the algorithm (§3, a Python framework); the heterogeneous DSP/LUT multiplier array, shift alignment and adder tree are the architecture (§4, Verilog on Kintex-7). **Checked against the `SYS` rule**: the Python "FATE Framework" is a model-compression tool, not a compiler, ISA or runtime that drives the hardware — no ISA section, no software-stack figure — so `SYS` does **not** apply |
| **Q-oriented** | **`Q-ORIENTED`** — seed agrees | Swap the whole thing to plain INT8 and the mixed multiplier array, the per-lane shift alignment, the segment-balanced reordering and the bit-width alignment module all have nothing to do. *Caveat worth knowing:* the importance measure alone would survive as a pure pruning criterion (that is FATE-1), so a sliver of the contribution is sparsity work — but the paper's headline mechanism is the type assignment |
| **Data type** | **`INT8` `INT4` `TERNARY` `BINARY` `MIXED`** — seed agrees, all five grepped | INT8/INT4 named throughout §3.3, §4.3, Table 5; "Ternary"/"Binary" are column headings in Figure 9 and the shift list in §4.3; `MIXED` is the whole point. **`FP32` is a judgment call I would decline** — it appears only as the *source* format in §3.3's ladder sentence and as the GNN accuracy column in Table 6; no FP32 datapath exists and every hardware baseline is INT8 HDC. **`LUT` must not be added** — FATE's LUTs are Xilinx logic primitives, `codebook`/`lookup table` have zero hits |
| **Generation** | **`G2`** — seed agrees | Judged by paradigm: an architecture built to execute quantized arithmetic across bit-widths, the `BitFusion` family. No LLM, no outlier format, no codebook, no weight-only bandwidth argument — none of the three G3 threads is present. 2025 publication date is irrelevant |
| **Optimization** | `FPGA` `per-dimension mixed precision` `DSP/LUT resource split` `importance measure` `pruning as INT0` `HDC` + **`fuzzing-distance`** **`power-of-two shift alignment`** **`segment-balanced dimension reordering`** | The seed's six are all sourced. The three additions are the paper's own mechanisms and are what make it citable: `fuzzing-distance` is the measure's own name (§3.2), the shift alignment is why one adder tree suffices (§4.3), and the reordering is why no dynamic scheduling is needed (§3.4) |

**§4 fairness verdict (≈60 words).**

> Iso-substrate and iso-baseline: every baseline re-implemented on the same Kintex-7 at 200 MHz,
> and CompHD/SparseHD share FATE-1's hardware, so those are accuracy-only at iso-memory. Not
> measured — Vivado utilisation and power-estimate reports, accuracy from a Python model. Do not
> quote **53.79%** (maximum; average 17.84%), the abstract's **"50% speedup"** (a 47.14% latency
> reduction), or the **20×** (binary at half dimensionality).

**Proposed venue-list row** (line 49; the seed's ASIC→FPGA correction at line 181 is confirmed):

```
| [ ] | [FATE: Boosting the Performance of Hyper-Dimensional Computing Intelligence with Flexible Numerical DAta TypE](https://doi.org/10.1145/3695053.3731031) | *close read* | ALGO+ARCH | Q | `INT8` `INT4` `TERNARY` `BINARY` `MIXED` | G2 | `FPGA` `per-dimension mixed precision` `DSP/LUT resource split` `fuzzing-distance importance measure` `pruning as INT0` `power-of-two shift alignment` `segment-balanced reordering` `HDC` | A different type per **dimension**: INT8 on DSPs, INT4/ternary/binary as logic on idle LUTs, `INT0` = pruned — precision chosen by **which fabric is free** (INT8 HDC saturates 83-90% of DSPs at 17-41% LUTs), not by the value distribution. 4.9 effective bits. Its "LUT" is an FPGA resource, **not** LUT-GEMM |
```

## Note from the source list

> _(no keywords recorded in the source CSV)_

## Abstract (verbatim, from the archived PDF)

> Hyper-Dimensional Computing (HDC) is a promising brain-inspired learning framework designed
> for efficient, hardware-friendly computation. By utilizing highly parallel operations, HDC
> encodes raw data into a hyper-dimensional space, facilitating efficient training and
> inference processes. However, the high precision required for representing high-dimensional
> vectors presents challenges for implementing HDC on resource-constrained edge devices,
> mainly due to the significant computational cost of performing multiplication for cosine
> similarity calculations. On the other hand, binary HDC offers lower costs but sacrifices
> accuracy. This paper addresses these challenges by focusing on data quantization, a
> hardware-efficient compression technique that incorporates sparsity to effectively balance
> cost and accuracy on embedded FPGA. Unlike existing methods that employ the same
> quantization scheme for all dimensions, we propose a novel solution that applies different
> numerical data types to different dimensions of data representations. This approach is
> motivated by two factors: (1) the varying importance among dimensions and (2) the potential
> for better utilization of heterogeneous FPGA hardware resources. To achieve this, we propose
> FATE, an algorithm/architecture co-designed solution that utilizes low-precision data types
> for less important dimensions, enabling the replacement of multiplication operations with
> logic calculations. This approach leverages FPGA Look-Up Table (LUT) resources for efficient
> implementation. The key insight of FATE is that dimensions with high importance require
> high-precision data types, while the low-importance dimensions do not, allowing them to be
> sacrificed for low hardware overheads. Furthermore, to maximize resource utilization, we
> design a workload-aware mixed quantization scheme that offers flexible compression based on
> these differences in dimensional importance. The proposed quantization framework is
> seamlessly integrated into the existing FPGA implementations, leveraging the heterogeneous
> resources available (LUTs and DSPs) for low-precision and high-precision dimensions,
> respectively. We evaluate FATE across multiple application domains. With optimized data type
> ratios on the Kintex-7 FPGA device, our design results in up to 50% speedup and 53.79% energy
> saving, while maintaining accuracy compared to solely exploiting DSPs for all dimension
> computations.
