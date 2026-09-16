# Commutative Data Reordering: A New Technique to Reduce Data Movement Energy on Sparse Inference Workloads

**Venue / Year:** ISCA 2020, pp. 1076-1088 · **Link:** https://doi.org/10.1109/ISCA45697.2020.00091 · **Reader:** Haoxuan · **Date:** 2026-09-14

## Tags

| | |
|---|---|
| **Level** | `SYS+ARCH` |
| **Q-oriented** | `NON-Q-ORIENTED` |
| **Data type** | `—` |
| **Generation** | `—` |
| **Optimization** | data-movement energy · bit-flip minimization · Hamming-distance minimization · **commutative operand reordering** · TSP/CVRP ordering · Base+XOR · DBI-aware cost · strided reordering · offline weight-layout transform |

## 1. One-line summary

**No quantization contribution** — the subject is **bit-level switching activity on the DRAM bus**, not numeric format: where a 1 costs energy and a 0 is free, the fetch **order** of weights in a dot product is algebraically free, so each matrix row is reduced to a **TSP / Capacitated Vehicle Routing** problem over Hamming distances (auxiliary node also elects the low-weight Base+XOR base; vehicle capacity = one cache block), solved **offline with greedy descent in OR-Tools**, with the permutation hidden in the `<column, value>` indirection CSR already carries so **no metadata is added** — buying **−22.2% DRAM IO energy over Base+XOR = −5.3% total DRAM energy**, with **no hardware beyond the prior-work codec** and ≤2.1% runtime cost.

## 2. Data type

**None proposed.** `quantiz*` 3 (all about Deep Compression as a *baseline network's* property) · `bitwidth` 0 · `INT8`/`FP16`/`FP32` 0 · `mantissa` 0 · `two's complement` 0 · `sign-magnitude` 0 · `per-tensor`/`per-channel`/`scale factor`/`calibrat*`/`accumulator` 0 each · `accuracy` 1, in someone else's pruning background.

**Not format-silent, though.** Every result is reported at **8-bit fixed point and 16-bit float** — "(a) Fixed Point / (b) Floating Point" panels throughout — and the paper concludes they agree. That is the swap-for-INT8 test, run by the authors. IEEE-754 half vs **bfloat16**: similar relative benefit, but bfloat16 carries **9.4% more 1s** under Base+XOR.

**Granularity, outliers, escape hatch: n/a** — no value changes. The 8-bit conversion is eight words with no scale, no clipping, no calibration, and is never validated. **Neither PTQ nor QAT**: an offline pass over the trained checkpoint, ~0.31 s/row, <3 CPU-hours worst case. **Workload is DNN, not scientific sparse** — 7 pruned nets (AlexNet ×3 via Deep Compression / SkimCaffe / iterative, MobileNet, ResNet, VD-LSTM ×2); `SpMV` 0 hits.

## 3. Optimization

**The reduction.** Each non-zero is a node; edges are the **DBI-aware Hamming distance** between full `<column, value>` tuples. An auxiliary node with asymmetric edges (cost *in* = that node's Hamming weight, cost *out* = 0) turns the cycle into a path and simultaneously elects the cheapest tuple as the Base+XOR base. Per-block base retransmission makes it a **CVRP** — vehicle = cache block, capacity = tuples per block, plus a **fill vehicle** taking `RowLength mod C` and a **remainder vehicle** measured from the previous row's last tuple. Rows are independent under CSR contiguity, so it parallelises.

**Strided reordering, the performance valve.** Unrestricted permutation scatters the *input-vector* stream and breaks GPU coalescing (≈1.97× L1 accesses, ≈1.21× misses), so reordering is confined to a per-network stride, characterised cheaply on warp multiples from the solver's first solution. A zero-loss stride exists for every network. Solver ablation: 24 h/matrix of GLS, simulated annealing and tabu beat greedy by **1.8% best layer, 0.5% average, <0.1%** for the other two — headroom looks close to exhausted.

**Hardware: none of its own.** Needs a Base+XOR-class codec at the memory controller (prior work) and an asymmetric-energy interconnect; DBI on in every experiment, **incompatible with data scrambling**, and cannot touch the row-pointer array or the vectors — no indirection to hide a permutation in. **The one real quantization link:** Deep Compression's codebook cuts unique coefficients, i.e. **bit entropy**, so long strides pack runs of identical values — **13.1%** gain shortest-stride-to-unrestricted, **11.4%** with those matrices removed.

## 4. Results

| | |
|---|---|
| Baseline | **Base+XOR** (Lee et al., the real prior art) and **DBI alone** (LPDDR4 standard). DBI enabled in every configuration |
| Models / datasets | 7 pruned nets on a mobile-class GPU (Tegra-X2-like, 256-core Pascal, 8 GB LPDDR4); CSR-vector SpMV from SHOC; direct sparse convolution |
| Accuracy delta | **None reported** — no accuracy, no bit-exactness check. Correctness argued from commutativity, though reordering an FP16 sum needs *associativity* (`associat*`: 6 hits, all "JEDEC … Association") |
| Speedup | None claimed. Cost **≤2.1%** worst case, **<1.1%** elsewhere; a zero-loss stride exists per network; some conv layers speed up (prefetch effect) |
| Energy / area | **DRAM IO −22.2%** avg / **−30.6%** max vs Base+XOR; **−53.1% vs DBI** (framing disputed). **Total DRAM −5.3%** vs Base+XOR, **−12.7%** vs DBI. Area: **no CDR hardware**; the Base+XOR codec is 2232 µm², **<0.01%** of SOC (0.02% at a 128B line) |
| Technology node | 16 nm — **for the quoted codec area only**; everything else is simulation |
| Evidence level | **Three kinds, none measured:** GPGPU-Sim cycle-accurate simulation (performance); **Micron LPDDR4 power calculator**, an analytical vendor model (all energy); third-party 16 nm synthesis **quoted** (area) |
| **Is the comparison fair?** | Iso-hardware, iso-workload, iso-baseline (Base+XOR, the real prior art) — unusually clean, and both IO and total energy are given. **Not iso-numerics** (FP16 reordering changes rounding; no accuracy check). **Not to quote:** 53.1% ("average" in the abstract, "up to" in the body); <0.01% area (prior work's codec). Quote **22.2% IO = 5.3% total DRAM** |

## 5. Comment

No quantization.

## 6. Claude notes

*Suggestions from the reading agent. **Strip this section before copying into
`QuantArchSurvey/venues/ISCA/notes/`.***

- **Read depth, and the negative claim tested rather than assumed.** Full close read of §I-§IX; Figs. 8-15 **rendered to PNG** (subset-encoded fonts extract as control characters), so series names come from the images and the two L1 values are eyeballed, marked as such in `ANALYSIS.md`; references by grep only. ~35 terms swept over the **ligature-normalised** text including the bibliography — a naive grep is unsafe here, `ﬁ`/`ﬂ` ligatures make `scientific`/`efficient`/`coefficient` return 0. Verdict: **no quantization contribution, but not format-silent** — unlike `Cambricon-SR` this paper names INT8, FP16 and bfloat16 and runs every experiment at two of them. Same tag, opposite kind of absence.
- **Before you accept `Data type: —`:** the taxonomy's own worked example tags `Sanger` `NON-Q-ORIENTED` **with** `INT8`. By that precedent the sourced cell is `INT8` `FP16` `BF16` (not `MIXED` — alternative settings, never coexisting). Written `—` per your ruling; flagging, not resolving.
- **Seed dispute `ARCH` → `SYS+ARCH`, possibly not worth churning.** §VI: *"no hardware overhead is required beyond an encoder and decoder for the underlying data similarity based encoding scheme"* — the contribution is an offline OR-Tools pass. `ARCH` stays defensible via the memory-controller codec; your call on an out-of-scope row.
- **Two internal inconsistencies.** **53.1%** is "average" in the abstract, "up to" in §VIII-A, with no third statement; §VIII-A gives **5.3%** then **5.7%** for the same quantity two sentences apart (the conclusion says 5.3%). Both filed as citation hazards.
- **Disposition: keep as a background citation; do not drop the row, do not give it a paragraph.** It is the **extreme point** of the compression/data-movement cluster — every other entry changes what is stored, this one changes only the order, same bits, same count, energy still falls. It is also the corpus's cleanest demonstration of what `NON-Q-ORIENTED` means, because the authors ran the swap-for-INT8 test themselves. And its Deep Compression finding is one genuine quantization sentence: **a codebook lowers bit entropy, so it lowers switching activity on the wire too** — compression and transmission encoding compose, which none of `GOBO`/`Mokey`/`Ecco`/`Phi` says. Suggests a third value on the compression axis: **encode-for-activity**, beside encode-for-capacity and cheaper-arithmetic.
- **The gap the authors do not see.** Reordering a >2-term FP accumulation needs associativity, not commutativity. Half the results are FP16, with no accuracy or bit-exactness check anywhere; the 8-bit results are exact, the FP ones are not.
