# Ten Lessons From Three Generations Shaped Google's TPUv4i (Industrial Product)

**Venue / Year:** ISCA 2021, pp. 1-14 · **Link:** https://doi.org/10.1109/ISCA52012.2021.00010 · **Reader:** Haoxuan · **Date:** 2026-09-14

## Tags

| | |
|---|---|
| **Level** | `ARCH+SYS` |
| **Q-oriented** | `NON-Q-ORIENTED` |
| **Data type** | `INT8` `BF16` `FP32` `MIXED` |
| **Generation** | `G1` |
| **Optimization** | commercial silicon, deployed 2020 · 7 nm · systolic bf16 MXU · **offer quantization, do not require it** · energy per operation (Horowitz updated to 7 nm) · backwards ML compatibility · perf/TCO · compiler compatibility over binary compatibility · 128 MB CMEM · four-input FP adder · multi-tenancy |

## 1. One-line summary

An inference chip whose data-type decision is to **keep** bf16 and IEEE fp32 from a training
chip and add int8 only as a porting path — at **the same 138 T peak as bf16**, so int8 buys
memory footprint and not throughput — because lesson ⑥ of ten is that TPUv1 *required*
quantization and that was a mistake (developers pre-agreed a 1% quality budget, refused it once
the silicon existed, then spent months restoring quality in integers), evidenced by a
production census in which **1 of Google's 8 production DNNs is quantized**, and accompanied by
the paper's most reusable artefact: **Table 2, Horowitz's energy-per-operation table updated to
7 nm** — INT8 multiply **0.07 pJ**, bf16 **0.21**, fp32 **1.31** — whose real lesson is that
all of them are dwarfed by **7.5 pJ** for one 64-bit 8 KB-SRAM read and **250-450 pJ** for
HBM2, which is why the chip spends **28% of its die on SRAM and 11% on MXUs**.

## 2. Data type

**Formats.** bf16 + IEEE fp32 retained from TPUv3; int8 added. No `W_A_` notation is possible — the paper specifies no quantization scheme at all.

**int8 has no throughput advantage.** Peak 138 T for bf16 **and** int8 (one cell in Table 1). NVIDIA T4 in the same table: 65 fp16 / 130 int8, a real 2× path. int8's only stated benefit anywhere: halved memory footprint.

**MXU.** 4 × 128×128 = 64K MACs in one core, called "four systolic **floating point** matrix units". TPUv1's "64K 8-bit integer MACs" is a different chip — do not transplant it.

**Accumulator.** Not stated. Summation is floating point: custom **4-input FP adder** with intermediate rounding/normalisation removed (not bit-identical, but *more* accurate), then 32 two-input adders. Vector unit is 128-lane 32-bit.

**Granularity.** None. Zero occurrences of per-tensor, zero-point, requantization, calibration, bit-width, scale-as-quantization.

**Outliers.** None — the word does not appear.

**Escape hatch.** The whole chip is the escape hatch: fp32 and bf16 are always there, and **every** MLPerf run in the paper used bf16.

**Retraining.** PTQ assumed, and lesson ⑥ is its indictment. §7.H offers QAT as the fix and names the obstacle as *motivating developers to use it* — organizational, not technical.

**Energy per operation, 7 nm (Table 2 — the citable thing).** mul: INT8 0.070 · BF16 0.210 · FP16 0.340 · FP32 1.310 · INT32 1.480 pJ. add: INT8 0.007 · INT32 0.030 · BF16 0.110 · FP16 0.160 · FP32 0.380 pJ. Per 64-bit access: 8 KB SRAM 7.5 · 32 KB 8.5 · 1 MB 14 · HBM2 250-450 · DDR3/4 1300 (I/O only). 45 nm column is Horowitz [16]; 7 nm column is **modelled, method undisclosed**; bf16 has no 45 nm entry.

**The ratio that matters.** 1 INT8 multiply ≈ 1/107 of one 8 KB-SRAM read ≈ 1/3600 of an HBM2 access. INT8 MAC 0.10 pJ vs bf16-mul/fp32-add 0.59 pJ = 5.9×. Google's own gloss: "reduced-precision FLOPS can be relatively free in comparison to memory references."

**Production census.** 1 of 8 (RNN0), for half the memory footprint, not for speed. Feb 2020, pre-LLM.

## 3. Optimization

**`NON-Q-ORIENTED`, and unusually so — the contribution is a design methodology, and quantization appears in it as a cautionary tale.** Ten lessons from TPUv1/v2/v3 in production, then a chip built from them, then measurements. Delete int8 from the paper and nothing else moves: TCO-vs-CapEx, multi-tenancy, air cooling, P99 latency, DNN growth at 1.5×/yr, compiler compatibility and CMEM are all untouched. Lesson ⑥ is not "we quantized well", it is "**a DSA may offer quantization, but it must not require it**" — TPUv1 required it, application teams renegotiated the quality budget after tape-out, and recovery cost months per app. §7.H is the sequel: QAT would remove the separate post-training step, and the open problem is getting anyone to use it.

**The arithmetic decision is to spend, not to save.** "The danger of requiring quantization ⑥ and the importance of backwards ML compatibility ④ meant retaining bfloat16 and fp32 from TPUv3 despite aiming at inference." Backwards ML compatibility is what forbids a new format: bit-identical results need the same numerics *and* the same compiler ordering, because FP addition is not associative. int8 is added purely so TPUv1-era quantized apps port. The paper never prices the road not taken — no area or power figure for an int8-only TPUv4i.

**The one microarchitectural change to the multiply path is an adder tree, and it exists because the accumulation is floating point.** Instead of 128 two-input FP adders chained down the systolic array, sum groups of **four** then chain **32** — critical path to **¼**. Then a custom 4-input FP adder that drops intermediate rounding and normalisation: **−40% area, −25% power** vs the 128-adder chain, **−12% MXU peak power**, which matters because the MXUs are the most power-dense blocks and set the TDP for air cooling.

**Where the perf/TDP actually comes from: 128 MB of SRAM, not narrower numbers.** CMEM is **28% of the die**; the four MXUs are **11%**. The 2.3× perf/TDP over TPUv3 decomposes as **CMEM ~1.5× · 7 nm ~1.3× · everything else ~1.2×**. HBM roofline utilization goes 63% → **99%** (22%/67% with CMEM off). Three apps gain 1.7-2.2×, driven by embedding-table Gather ops running 13-15× faster out of CMEM. This is Google answering the inference-energy question with bandwidth rather than bitwidth — and Table 2 is the arithmetic that justifies it.

**The `SYS` half.** XLA is credited with **2.2×** on fixed hardware over 20 months (CUDA 1.8× for comparison; C compilers 1-2%/yr). TPUv4i deliberately chose **compiler compatibility over binary compatibility** and widened the VLIW bundle **25%** to address four MXUs and CMEM. §7.F: XLA keeps weights in HBM and prefetches into CMEM so multi-tenant context switches stay under ~100 µs. Also a 4D (triple-strided) tensor DMA and a new on-chip interconnect split four ways because wires do not scale.

## 4. Results

| | |
|---|---|
| Baseline | TPUv3 and TPUv2 on production apps; **NVIDIA T4** on MLPerf Inference 0.5-0.7, run in Google datacenters (unofficial, unverified). Table 2's 45 nm column is Horowitz, ISSCC'14 |
| Models / datasets | 8 production DNNs (MLP0/1, CNN0/1, RNN0/1, BERT0/1) = ~100% of Google's Feb-2020 inference; MLPerf ResNet50 / SSD / NMT |
| Accuracy delta | **No experiment of Google's own.** Second-hand from MLPerf: 3D-Unet and DLRM PTQ to int8 at **<0.1%** vs FP32, BERT **<1%**. Counter-cases: **NVIDIA could not make int8 work on NMT** and ran fp16; the int8 segmentation-damage figure is borrowed from ref. [40] |
| Speedup | Production apps: TPUv3 and TPUv4i both **~1.9× TPUv2** (TPUv1 0.7×). MLPerf: **1.3-1.6× T4**. CMEM on vs off: MLPerf 1.1× offline / 1.3× server; apps 1.1-1.4× (5 of 8) and 1.7-2.2× (3 of 8) |
| Energy / area | **perf/TDP 2.3× TPUv3** (CMEM ~1.5× · 7 nm ~1.3× · rest ~1.2×) but only **0.9-1.0× T4**; perf/avg-power vs T4 geomean **1.0×**. Peak **138 T, the same for bf16 and int8**; 33% of peak FLOPS achieved, **99% of roofline**. 175 W chip / 275 W system TDP, <400 mm², 16 B transistors. **MXUs 11% of die, CMEM 28%**. 4-input FP adder −40% area / −25% power (tree), −12% MXU peak power. Energy/op at 7 nm: INT8 mul 0.070 / bf16 0.210 / fp32 1.310 pJ; adds 0.007 / 0.110 / 0.380; 8 KB SRAM 7.5 pJ, HBM2 250-450 pJ per 64-bit |
| Technology node | **7 nm**, 1.05 GHz, deployed since March 2020 (TPUv3 16 nm; T4 12 nm) |
| Evidence level | **Deployed silicon, measured in production** for everything performance-related — the strongest in the corpus; the CMEM ablation is real hardware (compiler flags + a disabled core). **Table 2's energy is modelled, method undisclosed.** MLPerf runs unverified; both accuracy numbers second-hand |
| **Is the comparison fair?** | **Deployed silicon, measured in production** — the corpus's strongest evidence level, but **not iso-format** (TPUs bf16, T4 int8/fp16), **not iso-node** (7 vs 12 nm) or iso-era, and MLPerf unverified. Table 2's energy is **modelled, method undisclosed**. **Not to quote bare:** 1.3-1.6× over T4 (perf/TDP is 0.9-1.0×); 138 T (peak, identical for bf16 and int8) |

## 5. Comment

## 6. Claude notes

*Suggestions from the reading agent. **Strip this section before copying into
`QuantArchSurvey/venues/ISCA/notes/`.***

- **Read depth.** Full close read of the whole paper including Tables 1-7 and all captions; term sweeps run for outlier / per-tensor / zero-point / requant / calibrat / bitwidth / INT4 / fixed-point / accumulat (all zero or irrelevant). **All figures are bitmaps**, so every figure-derived number comes from the prose. Three things I could not resolve, all in `ANALYSIS.md`: (i) **how Table 2's 7 nm arithmetic column was produced** — no tool, library or corner is named anywhere; (ii) §2 ①'s "**DRAM access improved 6.3X**" cannot be reconciled with Table 2's own DRAM rows (DDR3/4 is 1300 → 1300 = 1.0×; DDR→HBM2 is 2.9-5.2×) — do not quote the 6.3×; (iii) how the Figure 13 CMEM-size sweep was performed.
- **One correction to the earlier brief.** "Its systolic MXU has 64K 8-bit MACs" was **TPUv1**, not TPUv4i — the same MAC count by coincidence, but the contribution bullets say "four systolic **floating point** matrix units for TPUv4i in 2020 versus one systolic **integer** matrix unit for TPUv1 in 2015."
- **Seed-tag dispute, one only: `ARCH` → `ARCH+SYS`, and I am flagging it rather than asserting it.** For: lesson ② is entirely compilers, the ISA/compiler-compatibility choice is a listed contribution, the VLIW bundle grew 25% because of it, and §7.F/§7.G are software-stack sections — that is the AGENT-GUIDE tell. Against: XLA is inherited and reasoned about, not built here. `non-Q`, `G1` and the four data types are all **confirmed** against the text.
- **The number I would exclude: 138 T as an int8 figure.** Table 1 prints "138 (bf16/8b int)" as one cell. Any sentence implying TPUv4i is faster in int8 is wrong, and measured utilization of that peak is 33%. The related trap is 1.3-1.6× over T4 — that is **bf16 against int8**, and the perf/TDP is parity (0.9-1.0×), which the authors concede in their own words.
- **Best-citation claim, and it is two claims.** (1) *Offer quantization, do not require it* — the deployment argument no academic paper in the corpus can supply, with the mechanism named: quality budgets are renegotiated **after** tape-out, by application teams, and the cost is schedule not accuracy. (2) **Table 2** — the only cross-format per-operation energy reference at 7 nm we have. Cite them separately; they support opposite halves of an argument.
- **§5 material, if you want it.** `G1`, and it is a finding rather than a default: bf16 + fp32 + scale-less int8 is exactly the TPUv2-era format set that TAXONOMY files under G1 silicon, and the G2 test fails twice (no type designed; the MXU gives int8 no advantage). Worth one sentence that this sits in the *same venue and year* as RaPiD and SamsungNPU, which are a paradigm ahead — generation is not a date.
- **Cross-paper: the three ISCA'21 silicon entries make three incompatible bets on precision flexibility.** RaPiD bets precision scaling *is* the lever (FP16/FP8/INT4/INT2 in one datapath); SamsungNPU bets on modest reconfigurability (INT8/INT16, and its own lessons section says *limiting* reconfigurability is nearly free); TPUv4i bets **against it entirely** and spends the silicon on 128 MB of SRAM. Same venue, same year, three shipping teams. My reading of the deciding variable: **who bears the cost of a quality regression** — IBM's and Samsung's customers pick a precision, Google's application teams discover one.
- **Evidence-level comparison worth a bullet, since SamsungNPU is the other silicon entry.** SamsungNPU measures 13.6 TOPS/W in silicon but its 1.79× is **simulation**; RaPiD measures chip peaks but scales by a **calibrated model**. TPUv4i is the only one measured **in production on a real workload mix**, and the only one that reports what fraction of that workload is quantized. Its *modelled* part is the one thing everyone will want to quote — Table 2.
- **On the "compression vs cheaper arithmetic" axis you proposed:** this is the industrial evidence for it. 0.07 pJ per INT8 multiply against 7.5 pJ for one 64-bit 8 KB-SRAM read (107×) and 250-450 pJ for HBM2, and a chip that puts 28% of its die into SRAM and 11% into arithmetic. Google's own sentence — "reduced-precision FLOPS can be relatively free in comparison to memory references" — is the best one-line statement of that axis in the corpus, and it is also the strongest available explanation for why G3 went weight-only.
- **BitFusion's premise, checkable for the first time.** Multiplier cost ∝ product of operand bitwidths predicts 16× between INT32 and INT8; Table 2 gives **21×** (1.48 / 0.07), and FP32/BF16 gives **6.2×**. Mine, derived, not the paper's.
- **`survey/TAGS.md` change, reported not applied:** drop **`mixed-precision`** from TPUv4i. TAGS.md defines it as the *quantization scheme* mixing precisions; TPUv4i has no scheme, only three supported formats and no description of using two at once. 23 papers → 22; touches the reverse index at line 70 and the matrix row at line 170. `multi-bitwidth-hw` was checked and does not apply — nothing reconfigures, and int8 and bf16 run at the same rate. Keep `analytical-dtype` and `accelerator`.
