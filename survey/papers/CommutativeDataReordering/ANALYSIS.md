# CommutativeDataReordering — paper notes

**Commutative Data Reordering: A New Technique to Reduce Data Movement Energy on Sparse Inference Workloads**
Ben Feinberg (Sandia National Laboratories), Benjamin C. Heyman, Darya Mikhailenko, Ryan Wong,
An C. Ho, Engin Ipek (University of Rochester)
**ISCA 2020**, pp. 1076-1088 ｜ DOI: **10.1109/ISCA45697.2020.00091**
Publication info verified 2026-09-02: venue, year **and DOI** all read out of the archived
PDF's own text (IEEE proceedings banner; the DOI was grepped for, not assumed); page range
confirmed 2026-09-14 from the PDF's own page footers (p01 = 1076, p13 = 1088).
Archived here: the **published IEEE version** (the page-1 IEEE proceedings banner is present in the extracted text), 13 pages.

Status: **note ready** ｜ Last updated: 2026-09-14 ｜ **Human scope ruling 2026-09-14: "no quantization" — out of scope for the survey body.**
Tags: `lossless-compression` `gpu-kernels` `accelerator`
How far it was read: **full close read of §I-§IX** (pp. 1076-1086). Read line by line: §I;
§II-A1/A2 (terminated vs unterminated interconnects, transition signalling, DBI/BIC, LWC/MiLC,
FV/BD/Base+XOR, Childers' CLR); §II-B/B1 (pruning background, COO and CSR); §III (the key idea
and Fig. 3's worked 4-vector example); §IV-A-D (TSP formulation and the auxiliary node, CVRP
formulation with fill and remainder vehicles, OR-Tools and the metaheuristic comparison, other
formats); §V/§V-A (strided reordering, stride-size selection); §VI/§VI-A (hardware support, DBI
and data scrambling); §VII-A/B (Tables I and II, the simulator and the energy model); §VIII-A-E
(all five evaluation subsections); §IX.
**Figures 8-15 were rendered to PNG and read** (`pdftoppm -r 200`, pp. 1084-1086) — their fonts
are subset-encoded and extract as control characters, so the series names, axis labels and
metrics below come from the rendered images, not from the text layer. Bar *values* read off
those plots are approximations and are marked as such; every number in the table below that is
not so marked is quoted from the prose.
**Skimmed, and itemised honestly:** (a) the **reference list** (pp. 1087-1088) was read by grep,
not entry by entry; (b) Figs. 1, 2, 4-7 (the interconnect, CSR/COO, TSP and CVRP schematics) were
read from the text layer and the prose, not rendered.
**Not resolved:** (i) whether **53.1%** is an average or a maximum — the abstract says "average",
§VIII-A says "up to", and the paper gives no third statement (see Citation hazards); (ii) whether
the **5.3%** and **5.7%** total-DRAM-energy figures in adjacent sentences of §VIII-A have different
frames or one is a typo; (iii) how the Micron LPDDR4 power calculator converts a count of 1s into
IO energy — no equation, no pJ/bit and no wire capacitance is given anywhere.

> Publisher record: https://ieeexplore.ieee.org/document/9138978/
> **There is no arXiv version** (arXiv API title search, 2026-09-02). The PDF was downloaded by a
> human and filed through [`survey/uploads/`](../../uploads/) — the sanctioned route when the
> arXiv-only rule leaves a paper unreachable; see
> [`Notes-002`](../../../Claude/notes/Notes-002-paper-source-access.md).
> The PDF is **not committed** (0.9 MB) and **cannot be re-downloaded by script** —
> both publishers 403. Re-extract with `python3 extract.py` → `extracted/` (committed).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, ISCA 2020 row.

---

## ⚠ Confirmed on a full read: no quantization contribution — but the paper is **not** format-silent

Human ruling 2026-09-14: **"no quantization"**, out of scope. The close read supports the ruling,
and the evidence is worth recording precisely, because the shape of the absence here is different
from [`Cambricon-SR`](../Cambricon-SR/ANALYSIS.md)'s (which never names a format at all).

### The sweep

Over the ligature-normalised full text including the bibliography (`ﬁ`→`fi` etc. — the raw
extraction uses ligatures, so a naive grep for `scientific`/`efficient`/`coefficient` returns 0
and must not be trusted):

| Term | Hits | Where |
|---|---|---|
| `quantiz*` | **3** | all three about **Deep Compression** [22] as a *baseline network's* property, never about CDR: §VIII-A p.1084, §VIII-E1 p.1085, ref [22] p.1087 |
| `precision` | **5** | "double precision FMA" (§I motivation); "half-precision floating point" ×3 (§VII-B, §VIII-A, §VIII-E3); "IEEE-754 half precision" (§VIII-E3) |
| `floating point` | 14 | figure captions and §VII-B / §VIII-E3 |
| `fixed point` | 4 | Fig. 8/9/10 sub-captions "(a) Fixed Point" + §VIII-A |
| `bfloat` | 5 | §VIII-E3 only (p.1086) |
| `exponent` | **1** | "eight exponent bits instead of five", describing bfloat16 (§VIII-E3) |
| `eight-bit` | 2 | §VII-B "eight-bit integer representations"; §VIII-A "eight-bit fixed point" |
| `16-bit` | 2 | §VII-B "16-bit floating point"; §VIII-E3 "16-bit floating point format" |
| `mantissa` · `bitwidth` · `bit-width` · `INT8` · `INT4` · `FP32` · `FP16` | **0 each** | — |
| `two's complement` · `sign-magnitude` · `sign bit` · `denormal` | **0 each** | — |
| `per-tensor` · `per-channel` · `scale factor` · `calibrat*` · `accumulator` | **0 each** | — |
| `codebook` · `centroid` · `k-means` · `dictionary` · `vector quantiz*` | **0 each** | — |
| `low-bit` · `reduced precision` · `binary` · `ternary` | **0 each** | — |
| `accuracy` | **1** | §II-B, about the *pruning* literature. **No accuracy experiment exists in this paper.** |
| `Hamming` | 10 | §III-§IV and §VI-A1 — the actual objective function |
| `transition` | 5 | §II-A1 transition signalling + ref [10] |
| `switching` | 2 | both "simultaneous switching noise" (§VI-A1, §VI-A2) — signal integrity, not activity factor |
| `toggle` | 1 | ref [28] title, "toggle-aware compression" |
| `sparse` · `sparsity` | 41 · 5 | the real subject |
| `neural network` | 27 | the real workload |
| `SpMV` · `scientific` (as a workload) | 0 · 1 | see "The workload set" below |

**verified** — counts taken on the normalised raw text, 2026-09-14.

### What the format content actually is

Three places, and all three treat the numeric encoding as a **sensitivity parameter of the input**,
never as a design variable:

1. **Every headline experiment is run twice, at two precisions.** §VII-B: *"For each network, the
   weight matrices are extracted as 32-bit floating point values and converted to both 16-bit
   floating point and eight-bit integer representations."* Figs. 8, 9 and 10 each have an **(a)
   Fixed Point** and a **(b) Floating Point** panel. §VIII-B's conclusion: *"these results are
   consistent between both fixed and floating point reordering patterns, suggesting broad
   applicability"*. **verified** (§VII-B p.1083, Figs. 8-10 pp. 1084-1085, §VIII-B p.1085).
   *This is the `Q-oriented` test run as an experiment by the authors themselves, and it comes back
   `NON-Q-ORIENTED`: swap FP16 for 8-bit integer and every conclusion holds.*
2. **§VIII-E3 "Sensitivity to Floating Point Format"** compares IEEE-754 half precision against
   **bfloat16** and reports *"CDR has similar impact on both"*, adding that CDR *"may be more
   beneficial on systems using bfloat16, since bfloat16 values have **9.4% more 1s** when encoded
   using Base+XOR"*. **verified** (§VIII-E3 p.1086, Fig. 15). The metric in Fig. 15 is *Normalized
   1s in the Matrix Representation*, each format normalised to its own un-reordered cost.
3. **Codebook quantization makes CDR work better, and the paper measures it.** §VIII-A: Deep
   Compression AlexNet *"stands out"* because Deep Compression *"not only prunes the matrix but also
   quantizes the coefficients into a smaller number of floating point values"*; §VIII-E1 gives the
   mechanism — it *"reduce[s] the number of unique coefficients in a weight matrix, thereby reducing
   the **bit entropy**"*, letting long strides *"pack runs of identical coefficients together"*. The
   number: average improvement from the smallest stride to unrestricted reordering is **13.1%**
   overall and **11.4% excluding the Deep Compression matrices**. **verified** (§VIII-A p.1084,
   §VIII-E1 p.1085).

**What is absent.** No bit-field analysis of any kind — sign/exponent/mantissa positions are never
examined, two's complement vs sign-magnitude is never mentioned, and the words `mantissa`,
`two's complement` and `sign bit` do not appear. The 8-bit conversion in §VII-B is stated in eight
words and never specified (no scale, no granularity, no clipping, no calibration) and never
validated (no accuracy number anywhere in the paper). The words are treated as opaque bit patterns
by the optimiser; the format only sets *how many 1s there are to remove*.

**The one place the bitwidth structurally enters the method** — and the paper does not remark on it:
in the CVRP formulation the vehicle capacity `C` is *"the number of tuples in each cache block …
if a system has 32B cache blocks and each operand is 2B, C for this system is 16"* (§IV-B, p.1081).
Halving the element width doubles `C`, i.e. doubles the optimisation horizon between base
retransmissions. **verified** for the sentence; the consequence is **inferred / not verified**.

### The workload set — it *is* a DNN paper

Despite the Sandia affiliation and the sparse-linear-algebra machinery, **every evaluated workload
is a pruned neural network.** Table II (p.1083): `an_dc` AlexNet + Deep Compression, `an_skim`
AlexNet + SkimCaffe, `an_ip` AlexNet + Iterative Pruning, `mn_agp` MobileNet + Automated Gradual
Pruning, `rn_agp` ResNet + AGP, `vd_agp` and `vd_bd` VD-LSTM+REAL + AGP / Baidu RNN pruning — seven
networks, three CNN families and one RNN. The kernel is CSR-vector sparse MVM from SHOC, and
convolutions are run as direct sparse convolution (Park et al.). `SpMV` as a term: 0 hits;
`scientific`: 1 hit, and it is the phrase *"formats originally designed for scientific computing"*
in §II-B1, i.e. provenance of the format, not a workload. **verified** (§VII-A/B pp. 1083, Table II).

---

## What the close read changed in the brief

The abstract-level brief was **substantially right** and is kept. Four corrections, all in the
direction of tightening a frame rather than reversing a claim:

1. The brief reported "53.1% DRAM IO energy reduction over DBI" as a headline; **§VIII-A calls it
   "up to" while the abstract calls it "average"**, and the paper never resolves the conflict. It is
   now filed as the paper's principal citation hazard.
2. The brief's "~5.7% average *total* DRAM energy" is one of **two** numbers the paper gives in
   adjacent sentences (5.3% and 5.7%); the conclusion uses **5.3%**, so that is the one to quote.
3. "**<0.01% area** on a mobile-class GPU" is the abstract's framing; §VI and §I say CDR itself needs
   **no hardware at all** beyond the prior-work Base+XOR codec, and the 0.01% is that codec's area,
   **quoted from Lee et al. at 16 nm**, not synthesised here.
4. The brief said CDR "does not apply to dense quantized tensors". Correct as to the metadata-free
   trick, but the reason is narrower than "sparsity": it is that a **dense array carries no
   indirection in which to hide a permutation**. CDR also cannot reorder the CSR row-pointer array
   or the input/output vectors (§VI, p.1082).

Not changed: the mechanism, the TSP/CVRP reduction, the metadata-free property, the <0.01%-order
area, the "no runtime performance penalty" claim, and the observation that better solvers barely
help.

---

## Brief

### 1. Motivation

On interconnects where transmitting a 1 costs more than a 0 — terminated buses, or unterminated
buses under transition signalling (§II-A1) — data movement energy is reduced by encoding to
minimise the number of 1s. Prior encodings (DBI/BIC, LWC/MiLC, Frequent Value, Bitwise Difference,
Base+XOR) treat the payload as *"a mere stream of bits, ignoring the semantics of the application"*
(§I). The observation: in a dot product, **the order in which weights are fetched does not affect
the result**, so the order is a free variable no prior encoder has used.

### 2. Overview

Commutative Data Reordering picks a low-energy fetch order for sparse weight matrices **offline, at
training time**, by modelling the ordering as a **Travelling Salesman** problem (one base per matrix)
or a **Capacitated Vehicle Routing** problem (one base per cache block), with edge weights equal to
the DBI-aware Hamming distance between consecutive `<column, value>` tuples, and solving it with
Google OR-Tools. It hides the chosen order in the indirection sparse formats already carry, so **no
extra metadata** is needed, and it restricts reordering to a **stride** so the input-vector access
stream is not scattered enough to cost performance.

### 3. Pros and cons

**Pros**

- A clean, genuinely novel degree of freedom — exploiting algebraic commutativity for an
energy win is the kind of insight that is obvious only afterwards, and the reduction to TSP/CVRP
lets them inherit fifty years of solver work in one page.
- Near-free: **no hardware beyond the prior-work Base+XOR codec** (§VI), no system-software change,
and a stride size can be found per network at which there is no runtime penalty at all.
- Unusually honest reporting: the IO-energy number and the *total* DRAM-energy number are both given,
and the paper explicitly benchmarks its 5.3% against what prior encoding papers reported (2.9%, 8%,
4%, 9%) rather than presenting it as a breakthrough.
- Runs its own robustness checks: two precisions, five stride sizes, six base-retransmission
frequencies, three metaheuristics against greedy, and a bfloat16 study.

**Cons**

- The benefit is entirely conditional on an **asymmetric-energy interconnect**; on a conventional
symmetric bus it buys nothing, and the paper does not quantify what fraction of deployed mobile
systems qualify.
- The win is small in system terms: **5.3% of DRAM energy**, on a subsystem that is 20-40% of system
power — so roughly **1-2% of system energy**, a figure the paper never computes.
- Solution quality barely improves with better solvers (1.8% best case, 0.5% average for GLS over
greedy), which suggests the achievable headroom is nearly exhausted at low effort.
- **Correctness is asserted from commutativity, but reordering a sum of more than two terms needs
associativity, which floating-point addition does not have.** `associat*` appears 6 times in the
paper, all inside "JEDEC Solid State Technology Association"; `rounding` 0 hits. Half of the results
are FP16, and there is no accuracy or bit-exactness check anywhere. See Limitations.

### 4. Where it applies

**Out of scope for the survey body** (human ruling, 2026-09-14). Keep as a **background citation** in
the data-movement thread: it changes neither the values nor their encoding width, only their order.
Group with [`SpZip`](../SpZip/ANALYSIS.md),
[`IBMCompressionAccelerator`](../IBMCompressionAccelerator/ANALYSIS.md) and
[`Cambricon-SR`](../Cambricon-SR/ANALYSIS.md).

---

## Method

**The reduction.** Each non-zero of a matrix row becomes a node in a complete graph; the edge
between two nodes is weighted by the **Hamming distance between the two full tuples** (value plus
column ID — *"all three values in the tuple must be reordered together"*, §III, p.1079). A tour is a
transmission order. Because a transmission order has a start and an end but a TSP tour is a cycle,
an **auxiliary node ∅** is added with **asymmetric** edges: the cost *into* any node is that node's
**Hamming weight** (it will be sent unencoded as the Base+XOR base), the cost back *to* ∅ is zero
(§IV-A, Fig. 5, p.1080). So the same optimisation that minimises inter-tuple distance also picks a
low-weight tuple to be the base.

**Why CVRP and not TSP.** One base per matrix would force every thread to replay the matrix from the
start to decode. Bases are therefore retransmitted per cache block, which turns the row into a
**Capacitated Vehicle Routing** problem: each vehicle is a cache block with capacity `C` = tuples per
block, each node has demand 1 (§IV-B, p.1081). Two patches make the analogy exact when a row does not
divide evenly into blocks: a single **fill vehicle** with reduced capacity `RowLength mod C` absorbs
the remainder so no other vehicle is underfilled, and a **remainder vehicle** in the next row departs
from a second auxiliary node (`%`) whose distances are measured from the *last tuple of the previous
row*, so the block that straddles a row boundary is still optimised. The row-pointer array is
untouched because the count per row does not change. Rows are optimised independently — CSR requires
row contiguity, which conveniently makes the problem embarrassingly parallel.

**Strided reordering — the performance safety valve.** Unrestricted reordering scatters the *input
vector* access stream, hurting GPU coalescing and L1 hit time (the value, column and row-pointer
arrays are all read sequentially regardless, so only the input vector suffers). CDR therefore
partitions each row into **strides** and reorders only within a stride (§V-A, p.1082). Stride size is
a tunable; characterisation only needs the solver's *first* solution, and only strides that are
integer multiples of the warp size need be tried. Fig. 14 shows the cost being bought off: at
unrestricted reordering, L1 array accesses go to ≈**1.97×** and L1 misses to ≈**1.21×** on `an_dc_fc7`
(read off the rendered plot).

**Solver.** Google OR-Tools, greedy descent. Guided local search, simulated annealing and tabu search
were each given a 24-hour budget per matrix over 16 weight matrices and were **rejected**: max 1.8%
better than greedy on one layer, 0.5% average for GLS, <0.1% for the other two (§IV-C, p.1081).

**Hardware.** *"When CDR is applied to a GPU-based system, no hardware overhead is required beyond an
encoder and decoder for the underlying data similarity based encoding scheme"* (§VI, p.1082) — i.e.
the Base+XOR codec of Lee et al., which sits at the memory controller and needs no DIMM change. CDR
cannot reorder the row-pointer array or the input/output vectors, and because some traffic is
therefore un-reordered, Base+XOR's special-case handling of all-zero words has to be kept even though
CDR makes that case rare. **DBI is enabled in every experiment**, and the Hamming weights/distances
in the optimisation are DBI-aware (§VI-A1, p.1083). CDR is **incompatible with data scrambling**
(§VI-A2) — as are all the encoding schemes it builds on.

## Key numbers, with their frame

All energy numbers: 7 pruned networks on a mobile-class GPU model, LPDDR4, geomean over networks,
**GPGPU-Sim cycle-accurate simulation driving the Micron LPDDR4 power calculator** — an analytical
DRAM energy model, not a measurement and not a circuit simulation.

| Setting | Model | Metric | Baseline | Result | Source |
|---|---|---|---|---|---|
| Perf-neutral strides | 7 nets, geomean | DRAM **IO** energy | Base+XOR [32] | **−22.2%** (average) | §VIII-A p.1084; also abstract, §I, §IX — the paper's most consistently framed number **verified** |
| Best single net | — | DRAM **IO** energy | Base+XOR | **−30.6%** (maximum) | §I p.1076 **verified** |
| Perf-neutral strides | 7 nets | DRAM **IO** energy | DBI alone | **53.1%** — ⚠ "**up to**" in §VIII-A, "**average**" in the abstract | §VIII-A p.1084 vs abstract p.1076 **verified as a conflict** |
| Perf-neutral strides | 7 nets, geomean | **Total** DRAM energy | DBI alone | **−12.7%** (average) | §VIII-A p.1084 **verified** |
| All evaluated strides | 7 nets | **Total** DRAM energy | DBI alone | **up to −13%** | §VIII-A p.1084 **verified** |
| Perf-neutral strides | 7 nets, geomean | **Total** DRAM energy | Base+XOR | **−5.3%** average (§VIII-A and §IX) — ⚠ §VIII-A also says "**5.7%** … and up to **8.8%** … over existing schemes" one sentence later | §VIII-A p.1084, §IX p.1086 **verified as a conflict** |
| Perf-neutral strides | 7 nets | Execution time | no CDR | **≤2.1%** loss worst case, **<1.1%** for all others; a zero-loss stride exists for every network; some conv layers speed up (prefetch effect) | §VIII-B p.1084-85, Fig. 10 **verified** |
| — | — | Area | mobile SOC | Base+XOR codec **2232 µm² at 16 nm, quoted from Lee et al. [32]**; 4 codecs **<0.01%** of SOC; scaled to a 128B line (est. 8×) **0.02%**. CDR itself: **no hardware** | §VI p.1082, §VIII-C p.1085 **verified** |
| Offline, worst case | `vd_bd_encoder`, stride 512 | Reordering time | — | **<3 h** (≈172 min, Fig. 11) on one 2.4 GHz Xeon E5-2630; 33,278 rows ⇒ **0.31 s/row**, trivially parallel | §VIII-D p.1085 **verified** |
| Solver ablation | 16 weight matrices, 24 h each | 1s in the matrix | greedy descent | GLS **+1.8%** best single layer, **+0.5%** average; SA and tabu **<0.1%** ⇒ greedy used throughout | §IV-C p.1081 **verified** |
| Stride sweep | 16 matrices | 1s in the matrix | smallest stride | **−13.1%** at unrestricted reordering; **−11.4%** excluding the Deep Compression matrices | §VIII-E1 p.1085, Fig. 12 **verified** |
| Base retransmission | 16 matrices | 1s in the matrix | single base, no CDR | CDR keeps a **32%** improvement over Base+XOR alone even at the most frequent retransmission | §VIII-E2 p.1086, Fig. 13 **verified** |
| Format sensitivity | 16 matrices | 1s in the matrix | per-format un-reordered | CDR's *relative* benefit is **similar on IEEE-754 FP16 and bfloat16**; bfloat16 carries **9.4% more 1s** under Base+XOR, so its *absolute* saving is larger | §VIII-E3 p.1086, Fig. 15 **verified** |
| Locality cost | `an_dc_fc7` | L1 accesses / misses | stride 32 | ≈**1.97×** accesses, ≈**1.21×** misses at unrestricted reordering | Fig. 14 p.1086, **read off the rendered plot — approximate** |
| Accuracy | — | any accuracy metric | — | **None. The paper reports no accuracy, no PSNR, no bit-exactness check.** `accuracy` = 1 hit, in the pruning background | grep, whole text **verified** |

**Evidence level, stated exactly:** cycle-accurate **simulation** (GPGPU-Sim, modified for LPDDR4) for
performance and access traces; an **analytical vendor power model** (Micron LPDDR4 power calculator)
for DRAM energy; a **quoted third-party 16 nm synthesis result** for area. No RTL and no synthesis by
these authors, no silicon, no circuit-level interconnect simulation. The asymmetric-energy premise
itself (1 costs, 0 free) is an assumption imported from §II-A1, not something measured here.

### Citation hazards

1. **53.1% — do not quote it bare.** The abstract calls it an *average* reduction in DRAM IO energy
   over DBI; §VIII-A, the only other place it appears in the paper, calls it *"up to"*. Quote
   **22.2% over Base+XOR** instead, which is framed as an average in all four places it appears
   (abstract, §I, §VIII-A, §IX), and pair it with the max, **30.6%**.
2. **5.3% vs 5.7%.** §VIII-A gives *"5.3% compared to Base+XOR alone"* and then, two sentences later,
   *"the 5.7% reduction in average DRAM energy — and up to an 8.8% reduction — over existing schemes"*.
   The conclusion uses **5.3%**. Quote 5.3%.
3. **IO energy is not DRAM energy.** 22.2% of IO energy is 5.3% of DRAM energy. Any quotation of the
   53.1%/22.2% pair without the 5.3% overstates the result by roughly 4×. The paper does the right
   thing and gives both — a citer must not drop the second.
4. **The area figure is not this paper's.** 2232 µm² at 16 nm is Lee et al.'s Base+XOR codec, quoted
   for a direct comparison; CDR adds no hardware of its own (§I, §VI). Do not report "<0.01% area
   for CDR" as a synthesis result.
5. **Everything is conditional on an asymmetric-energy interconnect.** On a symmetric bus the
   objective function is meaningless and the saving is zero. This is stated in §II-A1 and then
   assumed silently thereafter.
6. **The 12.7% and 53.1% are against DBI alone**, i.e. against a system with no data-similarity
   encoder at all. The honest incremental contribution of *this paper*, over the state of the art it
   builds on, is the Base+XOR-relative pair: **22.2% IO / 5.3% total**.

## Cost and requirements

- **Hardware:** none of its own. Requires a **Base+XOR-class data-similarity codec at the memory
  controller** (prior work, 2232 µm² @16 nm per controller) and an **asymmetric-energy
  interconnect** (terminated, or unterminated with transition signalling). Compatible with, and
  evaluated with, **DBI**; **incompatible with data scrambling**.
- **Software:** an **offline weight-layout pass** in the deployment toolchain — Google OR-Tools
  greedy descent over a CVRP per row per stride. Worst observed 3 CPU-hours per matrix at stride
  512, ~0.31 s/row, embarrassingly parallel across rows. Run **once, at training time**; never on
  the device. *"No changes to the mobile system software"* (abstract).
- **Data format requirement:** a sparse format carrying per-element indirection — CSR, CSC, CSR5,
  CSR-Adaptive, ELLPACK/JDS/SELLPACK — with **no ordering requirement on values within a row**
  (§IV-D, p.1081). A dense tensor has nowhere to hide the permutation and is therefore excluded.
- **Numeric requirement:** none stated. Evaluated at 8-bit integer, IEEE-754 FP16 and bfloat16, with
  the same conclusions.
- **Per-network tuning:** the stride size must be characterised per network to hit the zero-
  performance-loss operating point. Cheap (first solver solution suffices, warp-multiple strides
  only), but it is a per-model calibration step and the reported energy numbers all assume it.

## Limitations and open questions

1. **Floating-point associativity is never addressed, and half the results are FP.** The correctness
   argument (§III, p.1079) is *"addition has the commutative property, (a + b = b + a)"*. Commutativity
   is enough to swap two summands; reordering an `n`-term accumulation requires **associativity**,
   which IEEE floating-point addition does not have. `associat*`: 6 hits, all in
   "JEDEC Solid State Technology Association"; `rounding`, `round-off`, `bit-exact`, `determinis*`,
   `reproduc*`: **0 hits each**. The 8-bit fixed-point results are exact (integer addition is
   associative, absent overflow — and no accumulator width is stated); the FP16 and bfloat16 results
   are **not bit-identical to the unreordered network**, and the paper offers no bound, no experiment
   and no acknowledgement. *The grep counts are* **verified**; *the consequence is my analysis —*
   **inferred / not verified**.
2. **The headroom looks nearly exhausted.** 24 hours of GLS/SA/tabu buys ≤1.8% over greedy descent
   on the best layer and 0.5% on average. Either the landscape is flat or the formulation is close to
   its ceiling; the paper reads this as good news (greedy suffices) and does not ask the other question.
3. **The system-level win is never computed.** 5.3% of DRAM energy, with DRAM at 20-40% of system
   power (§VIII-A's own citation), is ~1-2% of system energy. The abstract leads with 53.1%.
4. **No sparsity, size or bit-statistics characterisation of the 16 matrices** is given, and §VIII-E1
   reports that *"neither sparsity nor matrix size appear to have a predictable influence"* on how
   much reordering helps — so there is no way to predict CDR's benefit for a new model. The authors
   flag this themselves and propose **reordering-aware pruning** as future work; nobody in this corpus
   appears to have taken it up.
5. **The energy model is unexamined.** No pJ/bit, no wire capacitance, no activity factor, no
   statement of how the Micron calculator turns a 1s-count into joules. For a paper whose entire
   thesis is a bit-level energy argument, the energy model is the least documented part of it.
6. **Only DRAM traffic is optimised.** §I motivates with on-chip SRAM weight-fetch energy [23], but
   nothing on-chip is evaluated; the L1/L2 interconnects are only ever a performance cost here, never
   an energy target.
7. **CDR cannot touch the row-pointer array or the input/output vectors** — no indirection to hide a
   permutation in (§VI, p.1082). For very sparse matrices, where the metadata share of traffic rises,
   the covered fraction falls; not quantified.

## Relation to other entries

- **The "compression and data movement" cluster the taxonomy has no box for**
  ([`survey/README.md`](../../README.md)) — [`Gist`](../Gist/), [`JPEG-ACT`](../JPEG-ACT/),
  [`SpZip`](../SpZip/), this paper, [`IBMCompressionAccelerator`](../IBMCompressionAccelerator/),
  [`ENEC`](../ENEC/), [`Ecco`](../Ecco/), plus [`Cambricon-SR`](../Cambricon-SR/ANALYSIS.md) since
  2026-09-14. **CDR is the extreme point of that cluster and defines one end of it:** every other
  entry changes *what is stored*; CDR changes only *the order in which it is sent*. The bits are
  identical, the count of bits is identical, and the energy still falls. If the survey wants one
  sentence to establish that "data movement optimisation" and "quantization" are different subjects,
  this is the paper that makes it unarguable.
- **A missing axis this paper names: encode-for-capacity vs encode-for-activity.** Ecco, Gist,
  JPEG-ACT, SpZip and IBMCompressionAccelerator all compress to move *fewer bits*. CDR moves exactly
  the same number of bits and changes only *how many of them are 1s*. The proposed
  "compression vs cheaper arithmetic" axis in [`PAPER-READING.md`](../../../Claude/instructions/PAPER-READING.md)
  needs a **third** value for this: bus switching activity is a currency neither of the other two
  captures.
- **[`Cambricon-SR`](../Cambricon-SR/ANALYSIS.md), read the same day, is the instructive contrast.**
  Both are `NON-Q-ORIENTED`. Cambricon-SR mentions no numeric format at all (zero hits); CDR names
  three (INT8 fixed point, IEEE-754 FP16, bfloat16), runs every experiment at two of them, and
  publishes a format-sensitivity figure. **Same tag, opposite kind of absence** — and CDR is the
  better of the two for showing what `NON-Q-ORIENTED` actually means, because the authors ran the
  swap-for-INT8 test themselves and reported that nothing changed.
- **[`SpZip`](../SpZip/ANALYSIS.md)** is the taxonomy's own worked example of the no-quantization
  case (`— / —`). CDR pairs with it; SpZip accelerates traversal+decompression of a compressed
  format, CDR permutes an uncompressed one.
- **The one genuine bridge to the quantization literature** is the Deep Compression observation
  (§VIII-A, §VIII-E1): **codebook quantization reduces bit entropy, which makes bit-level transmission
  encodings work better** — 13.1% vs 11.4%. Read alongside [`GOBO`](../GOBO/), [`Mokey`](../Mokey/),
  [`Ecco`](../Ecco/) and [`Phi`](../Phi/), it says something none of them says: a codebook's value is
  not only fewer stored bits but **lower switching activity on the wire**, and the two compose.
  If this paper earns one sentence in the survey, that is the sentence.
- **[`OLAccel`](../OLAccel/) (ISCA'18) is the near neighbour in venue and era** and the contrast is
  clean: OLAccel changes the *values*' precision and pays in outlier machinery; CDR changes nothing
  about the values and pays in offline solver time.

---

## For the note

### §1 one-line summary

> **No quantization contribution** — the paper's subject is **bit-level switching activity on the
> DRAM bus**, not numeric format: on an interconnect where a 1 costs energy and a 0 is free, it
> exploits the fact that the **order** of weight fetches in a dot product is algebraically free, and
> picks a low-Hamming-distance order by reducing the row to a **TSP / Capacitated Vehicle Routing**
> problem (Hamming-distance edges, an auxiliary node that also selects the low-weight Base+XOR base,
> vehicle capacity = one cache block) solved offline with **greedy descent in Google OR-Tools**,
> hiding the permutation inside the `<column, value>` indirection CSR already carries so **no metadata
> is added**, and restricting it to a per-network **stride** so GPU coalescing survives — buying
> **−22.2% DRAM IO energy over Base+XOR (= −5.3% total DRAM energy)** with **no hardware beyond the
> prior-work codec** and **≤2.1% runtime cost**; the **numeric encoding is studied only as an input
> sensitivity** (all results reported at both **8-bit fixed point and FP16**, with the same
> conclusions, plus a **bfloat16** study showing 9.4% more 1s than FP16), never designed or changed.

### Proposed values on their four axes

| Axis | Proposed | Evidence (one line) |
|---|---|---|
| **Level** | **`SYS+ARCH`** — *seed says `ARCH`; reported, not resolved* | The contribution is an **offline toolchain pass** (§IV: TSP/CVRP formulation, OR-Tools, metaheuristic ablation, stride selection — the longest technical section by far) that rewrites the weight layout before deployment and runs on **existing** hardware; §VI states plainly that *"no hardware overhead is required beyond an encoder and decoder for the underlying data similarity based encoding scheme"*, and §I that there is *"no area overhead beyond the previously proposed Base+XOR encoder"*. Under the human's 2026-09-09 RaPiD ruling ("a shipped software stack counts toward `SYS`"), the software half is the contribution and `ARCH` alone under-reports it. **For an out-of-scope row this may not be worth churning** — `ARCH` is defensible via the memory-controller codec and the interconnect precondition. Human's call. |
| **Q-oriented** | **`NON-Q-ORIENTED`** — seed agrees | The test *"swap the format for plain INT8 — what is left?"* **is an experiment in the paper**: §VII-B converts every weight matrix to *both* 16-bit float *and* eight-bit integer, Figs. 8/9/10 report both, and §VIII-B concludes *"these results are consistent between both fixed and floating point reordering patterns"*. The TSP/CVRP reduction, the auxiliary-node base selection, the strided reordering and the CSR-metadata trick all survive the swap untouched. |
| **Data type** | **`—`** — seed agrees, **with a caveat the human should see** | Per the 2026-09-14 ruling ("no quantization"), and matching `SpZip` / `Cambricon-SR`. **But this paper is not format-silent**: it names `INT8` (as "eight-bit integer"/"eight-bit fixed point"), `FP16` (as "16-bit floating point"/"IEEE-754 half precision") and `BF16` (as "bfloat16"), and reports results per format. If the human prefers the taxonomy's own `Sanger` precedent (`NON-Q-ORIENTED` **with** `INT8`), the sourced cell would be `INT8` `FP16` `BF16` — **not** `MIXED`, since the formats are alternative settings, never coexisting. Flagged, not resolved. |
| **Generation** | **`—`** — seed agrees | Generation is a quantization-paradigm axis and CDR takes no position on it: it designs no numeric type (`G2` test fails), builds no architecture for executing quantized arithmetic (`G2` test fails again — it builds no architecture at all), and never asks how few bits accuracy tolerates (`G1`'s question, and `accuracy` has 1 hit in the whole paper, in someone else's background). Matches `SpZip`, `ELSA`, `ENEC`, `Cambricon-SR`. |
| **Optimization** (free text) | `data-movement energy` `bit-flip minimization` `Hamming-distance minimization` `commutative operand reordering` `TSP/CVRP ordering` `Base+XOR` `DBI-aware cost` `strided reordering` `offline weight-layout transform` | The seed's three keywords all hold and are kept. The additions name the actual objective (Hamming distance, DBI-aware), the actual freedom being exploited (commutativity), the encoder it rides on, the performance valve, and the fact that the whole thing is an offline pass. |

### Proposed venue-list row

```
| [ ] | [Commutative Data Reordering: A New Technique to Reduce Data Movement Energy on Sparse Inference Workloads](https://doi.org/10.1109/ISCA45697.2020.00091) | *close read* | SYS+ARCH | non-Q | — | — | `data-movement energy` `bit-flip minimization` `Hamming-distance minimization` `commutative operand reordering` `TSP/CVRP ordering` `Base+XOR` `DBI-aware cost` `strided reordering` `offline weight-layout transform` | ⚠ **No quantization contribution** — the subject is bus switching activity, not format. Fetch order in a dot product is algebraically free, so pick a low-Hamming-distance order (TSP/CVRP, OR-Tools, offline) and hide it in the CSR `<column,value>` indirection: no metadata, no hardware beyond the prior Base+XOR codec. **−22.2% DRAM IO energy over Base+XOR = −5.3% total DRAM energy**; 53.1%-over-DBI is "average" in the abstract and "up to" in §VIII-A — do not quote it. Not format-silent, though: every result is reported at both **8-bit fixed point and FP16** (same conclusions — the swap-for-INT8 test, run by the authors), and §VIII-E3 finds **bfloat16 carries 9.4% more 1s than FP16** under Base+XOR. One real quantization link: Deep Compression's codebook lowers **bit entropy**, so CDR helps *more* (13.1% vs 11.4%). Belongs with `SpZip` |
```

*(Changes from the seed at line 88: `ARCH` → `SYS+ARCH` (**reported, human's call — see the Level
row above**); `non-Q`, `—`, `—` all unchanged and now sourced rather than assumed; the Verified
column goes `*agent brief*` → `*close read*`; the Optimization keywords gain six mechanisms; the
Note is rewritten to carry the numbers with their frames, the 53.1% hazard, and the two
format-adjacent findings.)*

### §4 fairness verdict

**Fair, and unusually so — the honesty is in the reporting, and the one lapse is in the abstract.**

- **Iso-hardware ✓ and iso-workload ✓.** Every configuration — DBI, Base+XOR, CDR at five strides —
  runs the same networks on the same GPGPU-Sim model with the same LPDDR4 parameters. DBI is enabled
  in all of them. The only variable is the order of the tuples, which is exactly the claim.
- **Baseline choice ✓.** The real prior art (Lee et al.'s Base+XOR, 2018-era, same problem) is the
  primary baseline and the paper leads with the number *against it*, not against the weaker DBI-only
  system. It even lists what competing papers reported (2.9%, 8%, 4%, 9%) so the reader can size 5.3%.
- **Both framings of the win are given ✓.** IO energy **and** total DRAM energy, in the same paragraph
  and again in the conclusion. Most papers in this corpus give only the flattering one.
- **Evidence levels not pooled ✗/✓ — mixed but disclosed.** Performance from a cycle-accurate
  simulator, DRAM energy from an analytical vendor power model, area **quoted from a third party's
  16 nm synthesis**. Three kinds of fact, none of them measurement; the paper says where each comes
  from but presents them in one narrative.
- **Not iso-anything on area, because there is nothing to compare ✓.** CDR adds no hardware; the
  0.01%/0.02% is the pre-existing codec's cost, correctly attributed in §VI and §I — but the
  **abstract's** *"the hardware modifications required to support CDR … incur an area penalty of less
  than 0.01%"* reads as CDR's own cost, and it is not.
- **Not iso-numerics ✗, unacknowledged.** Reordering an FP16 accumulation changes the rounding;
  the paper argues correctness from commutativity alone and reports no accuracy or bit-exactness
  check. Half the results are floating point.
- **Numbers not to quote bare.** (i) **53.1%** — "average" in the abstract, "up to" in §VIII-A, and
  it is measured against DBI-only, not against the state of the art; quote **22.2% / 30.6% max** over
  Base+XOR. (ii) **5.7%** — §VIII-A's own second figure for the same quantity it just called 5.3%;
  the conclusion says 5.3%. (iii) **<0.01% area** — prior work's codec, quoted at 16 nm, not
  synthesised here. (iv) Never quote the IO-energy number without the **5.3% total DRAM energy**
  beside it.

## Note from the source list

> **Keywords:** minimize 1s in transmission; use XOR to encode positions of non-zero values

*(Close read, 2026-09-14: the first keyword is exactly right. The second is wrong — the XOR is
**Base+XOR encoding of consecutive transmitted words** (prior work, Lee et al.), not an encoding of
non-zero positions. Positions are carried by CSR's ordinary column-index array, unmodified; CDR's
whole trick is that it needs no new positional encoding at all.)*


## Abstract (verbatim, from the archived PDF)

> Data movement is a significant and growing consumer of energy in modern systems, from
> specialized low-power accelerators to GPUs with power budgets in the hundreds of Watts.
> Given the importance of the problem, prior work has proposed designing interconnects on
> which the energy cost of transmitting a 0 is significantly lower than that of transmitting
> a 1. With such an interconnect, data movement energy is reduced by encoding the
> transmitted data such that the number of 1s is minimized. Although promising, these data
> encoding proposals do not take full advantage of application level semantics. As an
> example of a neglected optimization opportunity, consider the case of a dot product
> computation as part of a neural network inference task. The order in which the neural
> network weights are fetched and processed does not affect correctness, and can be
> optimized to further reduce data movement energy. This paper presents commutative data
> reordering (CDR), a hardware-software approach that leverages the commutative property in
> linear algebra to strategically select the order in which weight matrix coefficients are
> fetched from memory. To find a low-energy transmission order, weight ordering is modeled
> as an instance of one of two well-studied problems, the Traveling Salesman Problem and the
> Capacitated Vehicle Routing Problem. This reduction makes it possible to leverage the vast
> body of work on efficient approximation methods to find a good transmission order. CDR
> exploits the indirection inherent to sparse matrix formats such that no additional
> metadata is required to specify the selected order. The hardware modifications required to
> support CDR are minimal, and incur an area penalty of less than 0.01% when implemented on
> top of a mobile-class GPU. When applied to 7 neural network inference tasks running on a
> GPU-based system, CDR respectively reduces average DRAM IO energy by 53.1% and 22.2% over
> the data bus invert encoding scheme used by LPDDR4, and the recently proposed Base+XOR
> encoding. These savings are attained with no changes to the mobile system software and no
> runtime performance penalty.
