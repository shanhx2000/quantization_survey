# TPUv4i — paper notes

**Ten Lessons From Three Generations Shaped Google's TPUv4i : Industrial Product**
Norman P. Jouppi, Doe Hyun Yoon, Matthew Ashcraft, Mark Gottscho, Thomas B. Jablin,
George Kurian, James Laudon, Sheng Li, Peter Ma, Xiaoyu Ma, Thomas Norrie, Nishant Patil,
Sushma Prasad, Cliff Young, Zongwei Zhou, David Patterson (Google LLC)
**ISCA 2021**, pp. 1-14 ｜ DOI: **10.1109/ISCA52012.2021.00010**
Publication info verified 2026-09-09: venue, year and DOI all read out of the archived PDF's
own text (IEEE proceedings banner on page 1).
Archived here: the **published IEEE version**, 14 pages.

Status: **note ready** ｜ Last updated: 2026-09-14 ｜ **Human-checked 2026-09-14** — tags confirmed.
Tags: `analytical-dtype` `mixed-precision` `accelerator`
(Tag change proposed, **not applied** — see "Reported, not applied" at the end.)
How far it was read: **full close read of the whole paper** — abstract, §1 (Introduction to
TPUs and the contribution bullets), all ten lessons in §2, §3 (how the lessons shaped the
design, including the "Arithmetic improvements" paragraph line by line), §4 (performance),
§5 (CMEM in depth), §6 (related work / five commercial inference DSAs), §7.A–§7.H (discussion,
including §7.H on quantization-aware training), §8 (conclusion), and **Tables 1–7 with their
captions and footnotes**, read from the `-layout` extraction. Term sweeps run over
`raw.txt` for `outlier`, `per-tensor`, `zero-point`, `requant`, `dequant`, `calibrat`,
`bitwidth`/`bit-width`, `INT4`, `fixed point`, `granular`, `accumulat`, `precision`, `scale`.
**Skimmed / not resolved, itemised:**
1. **Figures 2, 3, 4, 7–14 are bitmaps** in the extraction. Only captions survive, so every
   figure-derived number below comes from the paper's **prose**, and no per-benchmark bar is
   transcribed.
2. **How Table 2's 7 nm arithmetic column was produced is never stated** — no tool, no
   library, no corner, no voltage. Only the conclusion's phrase "current models of SRAM and
   DRAM" hints at the method, and it hints only at the memory rows. **Verify before citing as
   anything but a model.**
3. **The text's "DRAM access improved 6.3X" (§2 ①) cannot be reconciled with Table 2's own
   DRAM rows.** Unresolved — see Citation hazards (b).
4. **How the Figure 13 CMEM-size sweep (0–128 MB) was performed** is not stated; compiler
   flags are named for the CMEM-on/off experiment (Figure 11) but not for the sweep.
5. The TCO methodology (§7.D) and the multi-tenancy / SLO material (lessons ⑦ ⑩) were read
   but are outside the survey's scope and are not analysed here beyond one line each.

> Publisher record: https://ieeexplore.ieee.org/document/9499913/
> **There is no arXiv version** (arXiv API title search, 2026-09-02). The PDF was downloaded by
> a human over the Duke subscription and filed through [`survey/uploads/`](../../uploads/); the
> IEEE download stamp is in the extracted text. See
> [`Notes-002`](../../../Claude/notes/Notes-002-paper-source-access.md).
> The PDF is **not committed** (3.8 MB) and **cannot be re-downloaded by script** — both
> publishers 403. Re-extract with `python3 extract.py` → `extracted/` (committed).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, ISCA 2021 row.

---

## What the close read changed in the brief

**One factual correction, one decisive addition, one absence made explicit.**

1. **Correction — "Its systolic MXU has 64K 8-bit MACs" is TPUv1, not TPUv4i.** That sentence
   ("The systolic array MXU has 64K 8-bit integer Multiply Accumulate (MAC) units", p. 1) is in
   the paragraph describing **TPUv1**, whose MXU is a single 256×256 array. TPUv4i has **four
   128×128 MXUs in one core** (Table 1) — the same 65,536 MACs by arithmetic coincidence, but
   the contribution bullets call them "four systolic **floating point** matrix units for TPUv4i
   in 2020 versus one systolic **integer** matrix unit for TPUv1 in 2015" (p. 2). The brief
   attributed TPUv1's integer array to TPUv4i. **verified** (p. 1, p. 2, Table 1).
2. **Addition, and it settles the `Q-oriented` question — int8 buys no throughput.** Table 1
   gives TPUv4i's peak as **"138 (bf16/8b int)"**: one number for both formats. The NVIDIA T4
   in the same table is "65 (ieee fp16)/130 (8b int)" — a 2× int8 datapath. So on TPUv4i int8
   is a *format the compiler accepts*, not a *faster path*; its only stated benefit anywhere in
   the paper is memory footprint. The brief had the right conclusion for a weaker reason.
   **verified** (Table 1, p. 2).
3. **Absence, now evidenced rather than assumed.** The paper contains **no quantization
   mechanism at all**: zero occurrences of `outlier`, `per-tensor`, `zero-point`,
   `requantization`, `dequantization`, `calibration`, `bit-width`/`bitwidth`, `INT4`, or
   `fixed point`; `accumulat*` occurs three times and all three describe TPUv1's Accumulators
   SRAM. There is no scale, no granularity and no accuracy experiment of Google's own.
   **verified** (term sweep over `extracted/*.raw.txt`).

Everything else in the brief holds and was confirmed: lesson ⑥'s content, the 1%-quality
anecdote, "offer quantization but do not require it", only RNN0 quantized, the MLPerf
post-training-quantization figures, and §7.H on QAT.

**Also missing from the brief and much the most citable thing in the paper: Table 2** — a 7 nm
update of Horowitz's energy-per-operation table. The brief did not mention it. It is why the
source CSV's comment reads *"Provide 'Energy per Operation'; FP32 to 8-bit"*.

---

## Brief

### 1. Motivation

Not a quantization paper: a **retrospective product paper**. Three TPU generations in
production taught Google ten lessons, and TPUv4i (deployed since March 2020, 7 nm) is what
those lessons produced. Quantization is **lesson ⑥ of ten**, and the lesson is a warning.

### 2. Overview

**⑥ "Some inference apps need floating point arithmetic."** TPUv1 *required* quantization
because it had only integer arithmetic, and that proved a problem in the datacenter.
Developers said up front that a 1% quality drop was acceptable and changed their minds once
the hardware arrived — the paper's explanation is that 1% on a 40% error rate is small but 1%
on a 12% error rate is not. Recovering the quality took months of extra integer work per
application.

The conclusion drawn is the survey-relevant one: **a DSA may offer quantization, but it must
not require it.** So TPUv4i keeps bfloat16 and IEEE fp32 from TPUv3 despite being an inference
chip, and adds int8 only so that applications already quantized for TPUv1 port easily —
**at the same 138 T peak as bf16, so int8 buys memory footprint and not throughput.** Its
TensorCore has four 128×128 systolic floating-point MXUs. §7.H adds that quantization-aware
training would avoid the separate post-training step, but that motivating developers to use it
is the open problem.

Of the production DNNs in the paper's own table, **only one (RNN0) was quantized at all**, and
the benefit was halving the memory footprint rather than throughput. From MLPerf, 3D-Unet and
DLRM post-training quantize to 8 bits at <0.1% accuracy loss and BERT at <1%.

Separately, **Table 2 updates Horowitz's 45 nm energy-per-operation table to 7 nm**, giving
per-operation picojoules for INT8 / INT32 / BF16 / IEEE FP16 / IEEE FP32 add and multiply
alongside SRAM and DRAM access energies. That table, not the quantization lesson, is the
paper's most reusable artefact for this survey.

### 3. Pros and cons

**Pros**

- Measured, deployed silicon at scale — the strongest evidence level in the corpus, and the
  only entry reporting what fraction of a **real production workload** is actually quantized.
- The deployment argument is one this survey cannot get from academic accelerator papers:
  quality regressions are discovered late, by application teams, after the hardware exists.
- Frames PTQ as a *schedule and organizational* risk, not only an accuracy number.
- Gives the counter-case to every design in this corpus that assumes low precision is free to
  adopt.
- **Table 2 is a cross-format energy reference at 7 nm** that almost nothing else in the corpus
  has: per-operation energy for five numeric formats plus SRAM and DRAM in the same units.

**Cons**

- Contributes no numeric format and no quantization mechanism; the arithmetic decision is to
  keep the wide formats.
- The workload evidence is Google's 2020 production mix, pre-LLM. Its "only one model is
  quantized" datum should not be projected onto today's inference.
- Being a lessons paper, the quantization material is a few paragraphs and cannot be
  cross-examined; no ablation, no per-application breakdown, **no accuracy experiment of
  Google's own** — the two accuracy claims are second-hand (MLPerf submissions) and the one
  visual (Figure 4) is borrowed from reference [40].
- **Table 2's derivation is not disclosed**, which limits how firmly it can be cited.

### 4. Where it applies

**The industrial reality check, plus one table.** Best citation in the corpus for (a) *offer
quantization, do not require it* as a design principle, (b) the observation that accuracy
targets are renegotiated after silicon exists, (c) evidence on how much production inference is
quantized in practice, and (d) **energy per operation across formats at 7 nm**. Belongs in the
survey's background, in the PTQ/QAT-as-architectural-constraint section, and in whatever
section motivates low precision by arithmetic energy — where it is simultaneously the best
source for the numbers and the best source for the caveat that memory dominates them. Read
alongside [`SamsungNPU`](../SamsungNPU/ANALYSIS.md) and [`RaPiD`](../RaPiD/ANALYSIS.md), the
other two shipping-silicon entries — the three disagree about how much precision flexibility is
worth paying for.

---

## Conclusions

**Read in full.** The claims below carry `**verified**` (with the table, section or page) or
`**inferred / not verified**`. Numbers derived by me from the paper's own figures are marked
`**derived**` and are not the paper's claims.

---

## Method

**What the paper is.** An ISCA **Industry Track** retrospective: ten lessons from five years of
running TPUv1/v2/v3 in Google datacenters, then §3 showing how each lesson shaped TPUv4i, then
a measured evaluation of TPUv4i against TPUv3 and the NVIDIA T4. It is a *product* paper —
there is no proposed technique, no ablation of a mechanism, and no design-space exploration.
**verified** (§1, §2 preamble, p. 2 contribution bullets).

**The chip.** 7 nm, <400 mm², 16 B transistors, 1.05 GHz, **one** TensorCore (TPUv3 has two),
144 MB on-chip / 8 GB HBM at 614 GB/s, 175 W chip TDP / 275 W system TDP, 55 W idle, deployed
since Q1 2020. TensorCore = 4 × 128×128 MXU + a 128-lane 32-bit vector unit + cross-lane unit +
sequencer; uncore = OCI, ICI router, HBM controller, host interface, chip manager.
**verified** (Table 1, Figures 5–6, §3).

**The arithmetic decision — the only place the paper touches numeric format.** §3
"Arithmetic improvements", quoted in full because it is short and load-bearing:

> "Another big decision is the arithmetic unit. The danger of requiring quantization ⑥ and the
> importance of backwards ML compatibility ④ meant retaining bfloat16 and fp32 from TPUv3
> despite aiming at inference. As we also wanted applications quantized for TPUv1 to port
> easily to TPUv4i, TPUv4i also supports int8."

That is the entire specification of int8 support in the paper. **verified** (§3, p. 8).

**The adder-tree redesign** (also §3, and the only microarchitectural change to the multiply
path): instead of a chain of 128 two-input floating-point adders accumulating one product at a
time, TPUv4i sums groups of **four** products and then chains **32** two-input adders — cutting
the systolic array's critical path to **¼**. Having committed to a four-input sum, they built a
**custom four-input floating-point adder that removes the rounding and normalization logic for
the intermediate results**; the result is not bit-identical to the two-input chain but is
*more* accurate, and the difference is small enough not to move ML results. **verified** (§3,
p. 8).

**How it was evaluated.**
- **Production apps (Figure 8, Figures 11–13, Table 7):** eight DNNs that are ~100% of Google's
  February 2020 inference workload, **measured on the deployed chips**. **verified** (§4, §5,
  Table 3).
- **MLPerf Inference 0.5–0.7 (Figures 9, 10, 13, 14):** run **in Google datacenters**, using
  NVIDIA's own latest MLPerf code for the T4. The caption states the results are **unofficial
  and unverified by MLPerf**. **verified** (Figure 9 caption, §4, §7.B).
- **The CMEM ablation (Figure 11)** is a real hardware experiment, not a simulation: compiler
  flags disabled CMEM, and running on **TPUv4** with one core disabled doubled the HBM
  bandwidth available to one core. **verified** (§5).
- **Table 2's energy figures are modelled, not measured.** The 45 nm column is Horowitz's
  ISSCC 2014 table [16]; the 7 nm column is Google's update. §8: "This paper also updated
  Horowitz's influential energy operation table [16] to a modern technology **with current
  models** of SRAM and DRAM." No method is given for the *arithmetic* rows at all.
  **verified as to the wording; the derivation is inferred / not verified.**

**Definition of "operation" in Table 2.** Caption: *"Energy per Operation: 45 nm [16] vs 7 nm.
Memory is pJ per 64-bit access."* So arithmetic rows are **one add or one multiply of the named
format**, and memory rows are **one 64-bit access**. A multiply–accumulate is therefore the sum
of two rows and must be assembled by the reader. **verified** (Table 2 caption, p. 3).

---

## Key numbers, with their frame

Evidence levels are **not** pooled: rows marked *silicon* are measurements on deployed chips,
rows marked *model* are Table 2, rows marked *second-hand* are quoted from third parties.

| Setting | Model | Metric | Baseline | Result | Source |
|---|---|---|---|---|---|
| **Energy/op, multiply, 7 nm** *(model)* | — | pJ per multiply | 45 nm (Horowitz [16]) | **INT8 0.070** · BF16 0.210 · IEEE FP16 0.340 · IEEE FP32 1.310 · INT32 1.480. 45 nm was INT8 0.200 · FP16 1.100 · FP32 3.700 · INT32 3.100; **BF16 has no 45 nm entry** | Table 2, p. 3 **verified** |
| **Energy/op, add, 7 nm** *(model)* | — | pJ per add | 45 nm (Horowitz [16]) | **INT8 0.007** · INT32 0.030 · BF16 0.110 · IEEE FP16 0.160 · IEEE FP32 0.380. 45 nm was INT8 0.030 · INT32 0.100 · FP16 0.400 · FP32 0.900 | Table 2, p. 3 **verified** |
| **Memory energy, 7 nm** *(model)* | — | pJ per **64-bit** access | 45 nm | SRAM **8 KB 7.5** (was 10) · **32 KB 8.5** (was 20) · **1 MB 14.0** (was 100, single-bank at 45 nm, excluded from the geomean). DRAM: **DDR3/4 1300 → 1300 (1.0×)** · **HBM2 250–450** · **GDDR6 350–480**, all **I/O energy only** | Table 2 + footnotes 1–2, p. 3 **verified** |
| **Whole-table technology gain** *(model)* | — | geomean 45 nm → 7 nm | — | **2.6×**, uneven: SRAM only 1.3–2.4×, wire energy <2× [15], logic much faster | Table 2 + §2 ①, p. 3 **verified** |
| **Format ratios at 7 nm** *(derived from Table 2)* | — | multiply energy ratio | INT8 multiply | BF16 **3.0×** · FP16 4.9× · FP32 **18.7×** · INT32 21.1× | **derived**, my arithmetic on Table 2 |
| **Realistic MAC at 7 nm** *(derived from Table 2)* | — | pJ per multiply-accumulate | — | INT8 mul + INT32 add = **0.100 pJ**; BF16 mul + FP32 add = **0.590 pJ** → **5.9×**. (Naive same-format MACs: INT8 0.077, BF16 0.320, FP32 1.690.) The paper never assembles a MAC; accumulator width is **not stated** | **derived**; accumulator width **inferred / not verified** |
| **Arithmetic vs memory** *(derived from Table 2)* | — | INT8 multiplies per one 64-bit access | — | one **8 KB SRAM** read ≈ **107** INT8 multiplies; one **1 MB SRAM** read ≈ 200; one **HBM2** access ≈ **3,570–6,430**; one **DDR3/4** access ≈ 18,600 | **derived** |
| **The paper's own gloss** | — | — | — | "SRAM is 20x more energy efficient than DRAM (Table 2)" (§3) and "reduced-precision FLOPS can be relatively **free** in comparison to memory references" (§7 closing) | §3, §7 **verified** |
| **Peak throughput** *(silicon spec)* | — | TFLOPS or TOPS / chip | TPUv3 123 (bf16); T4 65 (fp16) / 130 (8b int) | TPUv4i **138 (bf16/8b int)** — **one figure for both formats: int8 has no peak advantage**. TPUv1 was 92 (8b int) | Table 1, p. 2 **verified** |
| **Peak arithmetic check** | — | 2 × 65,536 MAC × 1.05 GHz | — | **137.6 T** — consistent with 4 × 128×128 MACs in one core at 1.05 GHz | **derived** from Table 1 |
| **Production quantization census** *(silicon / workload)* | MLP0/1, CNN0/1, RNN0/1, BERT0/1 (~100% of Google inference, Feb 2020) | fraction quantized | — | **1 of 8** (RNN0). "the primary benefit was **halving the memory footprint**" — not throughput | §2 ⑥ + Table 3, p. 5 **verified** |
| **PTQ accuracy** *(second-hand, MLPerf submissions)* | 3D-Unet, DLRM | accuracy loss, INT8 PTQ | FP32 | **<0.1%** | §2 ⑥, p. 5 **verified as quoted; second-hand** |
| **PTQ accuracy** *(second-hand)* | BERT | accuracy loss, INT8 PTQ | FP32 | **<1%** | §2 ⑥, p. 5 **verified as quoted; second-hand** |
| **PTQ failure case** *(second-hand, NVIDIA)* | NMT (MLPerf Inference 0.5) | usable at int8? | — | **No** — "The T4 used int8 on ResNet and SSD but used fp16 on NMT, since **NVIDIA couldn't get int8 to work for this DNN** ⑥" | §4, p. 9 **verified** |
| **The 1%-quality anecdote** *(organizational)* | TPUv1 era | quality budget | — | Developers pre-agreed 1% loss, then refused it on delivery; "**months of extra development** to restore the quality score using integers". Explanation offered: 1% on a 40% error is small, on a 12% error is large | §2 ⑥, p. 5 **verified** |
| **Production performance** *(silicon)* | 8 production DNNs | perf, relative to TPUv2 | TPUv2 = 1 | TPUv1 **0.7×**; TPUv3 and TPUv4i both **~1.9×** | §4 + Figure 8, p. 9 **verified** |
| **Production perf/TDP** *(silicon)* | 8 production DNNs | perf / system TDP | TPUv3 | **2.3×** = 1.1× FLOPS (123→138 T) · 4.5× SRAM (32→144 MB) · 0.7× DRAM BW (900→614 GB/s) · 0.4× TDP (450→175 W) + 2× MXU/core. Attribution: **CMEM ~1.5× · 7 nm ~1.3× · everything else ~1.2×** | §4, p. 9 **verified** |
| **vs NVIDIA T4** *(silicon, MLPerf, unverified)* | ResNet50, SSD, NMT | perf; perf/system TDP | T4 = 1 | **1.3–1.6× perf**, **0.9–1.0× perf/TDP** (NMT 1.3× perf/TDP). Perf/**average** power: NMT 1.6–2.0×, ResNet50 1.0×, SSD 0.5–0.6×, **geomean 1.0×**. **TPUs ran everything in bf16; the T4 ran int8 on ResNet/SSD and fp16 on NMT** | §4 + Figure 9 caption, p. 9 **verified** |
| **T4 thermal/ECC caveat** *(silicon)* | MLPerf 0.5/0.7, 10 min, ECC on | perf drop | T4's own MLPerf score | **−19% to −26%**; TPUv4i unchanged (+~5 °C over 10 min) | §7.B + Figure 14, p. 11–12 **verified** |
| **Four-input FP adder** *(design, unattributed method)* | — | area / power / latency | a series of **128 two-input** adders | **−40% area, −25% power** for the adder tree; **−12% MXU peak power**; systolic-array critical path cut to **¼**. Not bit-identical; *more* accurate | §3, p. 8 **verified** |
| **Die budget** *(silicon)* | — | % of die | — | **MXUs 11%** (TPUv1 24%, TPUv2 8%, TPUv3 11%); **CMEM 28%** | Table 7 §7.A + Figure 6 caption **verified** |
| **Utilization** *(silicon)* | 8 production DNNs, average | % of peak FLOPS/s; % of roofline | TPUv1 20%/20%, TPUv2 51%/66%, TPUv3 38%/63% | TPUv4i **33% of peak FLOPS, 99% of roofline**. Without CMEM: **22% / 67%** | Table 7, §7.A, p. 11 **verified** |
| **CMEM benefit** *(silicon)* | MLPerf 0.5–0.7 | speedup, CMEM on vs off | CMEM off | offline **1.1×**, server **1.3×** | §5 + Figure 10, p. 9–10 **verified** |
| **CMEM benefit** *(silicon)* | 8 production DNNs | speedup, CMEM on vs off | CMEM off | 5 of 8 apps **1.1–1.4×**; 3 apps **1.7–2.2×** (BERT1 1.71, BERT0 1.85, RNN1 2.22), driven by embedding-table Gather ops running ~13–15× faster from CMEM | §5, p. 10 **verified** |
| **CMEM sizing** *(silicon, method unstated)* | apps / MLPerf server | % of 128 MB performance | 128 MB = 100% | apps **69% at 0 MB**, 82% at 16 MB, 90% at 72 MB, 98% at 112 MB; MLPerf 76% / 87% / 97% / 100% | §5 + Figure 13, p. 10 **verified as quoted; method inferred / not verified** |
| **Commercial inference DSAs** *(second-hand, MLPerf)* | ResNet50 / SSD server | perf / **chip** TDP | T4 = 1.00 | Goya 0.46 (200 W) · Nervana NNP-I 0.69 (100 W) · Zebra 0.25 (225 W) · **HanGuang 800 2.17** (280 W, 192 MB SRAM, **no DRAM**). **TDP here is per chip, not per system** | Table 6 + caption, §6, p. 11 **verified** |
| **TCO ↔ TDP** *(silicon / business)* | 5 DNN DSAs | correlation of TCO with system TDP | — | **R = 0.99** (R² = 0.98); R = 0.88 over 15 CPUs/GPUs/TPUs | §2 ③, §7.D, Figure 3 **verified** |
| **Workload growth** *(silicon / workload)* | CNN1, MLP1, CNN0, MLP0 | annual increase, memory / FLOPS | — | 0.97/1.46 · 1.26/1.26 · 1.63/1.63 · 2.16/2.16 → "**~1.5× annually**" | Table 4, §2 ⑧, p. 5 **verified** |
| **Compiler gain** *(second-hand, MLPerf Training)* | MLPerf Training 0.5 → 0.7, 20 months | per-chip speedup from the compiler alone | same hardware | **CUDA 1.8× (GPU), XLA 2.2× (TPU)**; C compilers 1–2%/year | §2 ②, Figure 2, p. 3 **verified** |

### Citation hazards

**(a) Table 2's 7 nm column is a model with no disclosed method.** No tool, library, corner,
voltage or temperature is named; §8 says only "current models of SRAM and DRAM", which does not
cover the arithmetic rows at all. Cite it as *Google's 7 nm update of Horowitz's table*, never
as a measurement, and never alongside a synthesised or measured number as if they were the same
kind of fact. **This is the single most important hazard in the paper**, because Table 2 is the
part most likely to be quoted.

**(b) "DRAM access improved 6.3X" does not follow from Table 2.** §2 ① asserts it, but the
table's own DRAM rows give DDR3/4 **1300 → 1300 = 1.0×**, and DDR3/4 → HBM2 gives only
**2.9–5.2×**. No combination of the printed values yields 6.3. Do not quote "6.3×"; quote the
rows.

**(c) "SRAM is 20x more energy efficient than DRAM" depends on which SRAM row.** §3's claim
matches **1 MB SRAM (14 pJ) vs HBM2 (250–450 pJ)** = 18–32×. Using the 8 KB row instead gives
33–60×. State the pair.

**(d) 138 T is a peak, and it is the *same* peak for bf16 and int8.** It must never be quoted
as an int8 throughput number in a way that implies int8 is faster on this chip. Measured
utilization of that peak on production apps is **33%** (Table 7).

**(e) The 1.3–1.6× over the T4 is not iso-anything.** TPUs ran **bf16**; the T4 ran **int8**
(ResNet, SSD) and **fp16** (NMT). Different node (7 vs 12 nm), different era (2020 vs 2018),
and the MLPerf runs are explicitly **unverified**. The honest headline is the perf/TDP figure:
**0.9–1.0×**, i.e. parity. The paper says so itself: "Backwards ML compatibility makes TPUv4i
good for Google even if its int8 perf/TDP isn't much larger than T4."

**(f) Table 6 changes the TDP denominator.** Every other perf/TDP number in the paper uses
**system** TDP; Table 6 uses **chip** TDP because system TDP was unavailable (stated in the
caption). Do not compare Table 6's 2.17× for HanGuang against Figure 9's system-TDP numbers.

**(g) The "only one production DNN is quantized" datum is Feb 2020 and pre-LLM.** Eight models,
Google's mix, weighted by TPUv1/v2/v3 system TCO. It is evidence about 2020 datacenter
inference, not about inference in general and certainly not about LLM serving.

**(h) Both accuracy numbers are second-hand and neither is Google's measurement.** <0.1% for
3D-Unet/DLRM and <1% for BERT are attributed to **MLPerf** submissions; the paper reports no
accuracy experiment of its own. Likewise **Figure 4**, the visual demonstration of int8
segmentation damage, is captioned "Quantization error for segmentation **[40]**" — borrowed
from Shih et al., ACM TOG 2019, a paper about wide-angle portrait correction, not about
quantization.

**(i) The 40% / 25% adder savings are the adder tree's, not the MXU's.** They are "relative to
a series of 128 two-input adders". The chip-level consequence the paper gives is **−12% MXU
peak power**. Quote the 12% when talking about the chip.

**(j) The "64K 8-bit MAC" figure belongs to TPUv1.** See "What the close read changed". Any
survey sentence attaching 64K *8-bit* MACs to TPUv4i is wrong.

**(k) BF16 has no 45 nm entry in Table 2**, so the table's 45/7 ratio column and its 2.6×
geomean say nothing about bf16, and the 1 MB SRAM row is excluded from the geomean by footnote.

---

## Cost and requirements

**What the arithmetic decision costs.** Keeping bf16 and fp32 in a chip whose only job is
inference is the paper's *expenditure*, not its saving, and the paper never prices it: there is
no area or power figure for "what an int8-only TPUv4i would have cost". What can be said:

- The MXUs — four 128×128 floating-point systolic arrays — occupy **11% of the die**
  (Table 7). CMEM occupies **28%** (Figure 6). Google spent 2.5× more die on SRAM than on
  arithmetic. **verified**.
- The adder-tree redesign was needed *because* the accumulation is floating point: the ¼
  critical-path win and the −12% MXU peak power come from restructuring an FP adder chain, a
  problem an integer array would not have had. **verified** (§3); the counterfactual is
  **inferred / not verified**.
- **int8 costs almost nothing and delivers almost nothing.** Same peak as bf16 (Table 1); the
  only benefit named anywhere is RNN0's halved memory footprint (§2 ⑥). The paper does not say
  whether int8 reuses the bf16 multiplier, and the term sweep finds no int8 datapath
  description. **inferred / not verified.**

**What the design requires of software.**

- **A compiler, treated as a first-class deliverable.** XLA is credited with a **2.2×** gain on
  the same hardware over 20 months (Figure 2); TPUv4i deliberately chose **compiler
  compatibility over binary compatibility** and widened the VLIW bundle by **25%** to address
  four MXUs and CMEM; XLA's HLO/LLO split is what makes that safe. §7.F: XLA allocates weights
  in HBM and *prefetches* them into CMEM so that multi-tenant context switches stay cheap.
  **verified** (§3, §7.F, §7.G).
- **Backwards ML compatibility as a hard constraint on numerics.** "Any new inference TPU would
  at least need to offer the same numerics to get the same results and the same exception
  behavior: bfloat16 and IEEE fp32 would be required." Because FP addition is not associative,
  bit-identical results also require the *same compiler* making the same ordering choices —
  which is why a new numeric format is not a free choice for Google. **verified** (§2 ④).
- **PTQ is the assumed workflow, and §7.H names its replacement.** QAT "uses integers during
  training, allowing the switch to serving without a separate quantization step. Basically, the
  developer gets backwards ML compatibility while using integer data types." The stated
  obstacle is not technical: "The challenge is **motivating the use of** quantization aware
  training." **verified** (§7.H).

**What it costs to deploy.** 175 W chip / 275 W system TDP, air-cooled by design (lesson ⑤,
against TPUv3's 450 W liquid-cooled), 8 GB HBM sized for multi-tenancy (>80% of the production
workload needs it), and 128 MB of CMEM chosen as "the knee of the curve". **verified** (§3,
Table 1, Table 3).

---

## Limitations and open questions

**Admitted by the authors.**

- Getting developers to adopt **QAT** is unsolved, and the paper frames it as a motivation
  problem rather than a technical one (§7.H). **verified**.
- CMEM may be oversized: "Reducing CMEM 10%–20% might have little impact on current DNNs, but
  given our perf/TCO orientation ③ and the growth of DNNs ⑧, we won't know for sure for a few
  years." (§5) **verified**.
- int8 perf/TDP against the T4 "isn't much larger" (§4) — an unusual concession. **verified**.
- TCO is confidential, so TDP is used as its proxy (§2 ③). **verified**.

**Not admitted, and material for this survey.**

- **The paper never prices the road not taken.** It argues that requiring quantization was a
  mistake, but gives no number for what keeping bf16 + fp32 cost in area, power or peak
  throughput. The strongest version of lesson ⑥ would be "we paid X and it was worth it";
  what is offered is "we paid something and we would do it again."
- **No accuracy experiment of Google's own.** The whole quantization lesson rests on one
  anecdote (the 1% renegotiation), one borrowed figure ([40]), one workload census, and three
  second-hand MLPerf numbers. That is thin evidence for a claim the survey will lean on, and
  the thinness should be stated when leaning on it.
- **Table 2's method is undisclosed**, and the paper offers the table as a contribution
  ("including an update of Horowitz's operation energy table [16] from 45 nm to 7 nm", p. 2)
  without the reproducibility that framing would demand.
- **The int8 datapath is a black box.** Whether int8 reuses the bf16 multiplier array, what the
  accumulator width is, whether there is any scale or zero-point support in hardware, and how a
  TPUv1-era quantized model is actually mapped — none of it is described. For a survey on
  quantization in architecture, this is the most frustrating gap in the paper.
- **The lesson generalises further than the evidence.** "Some inference apps need floating
  point" is supported by NMT and a segmentation example; "a DSA may offer quantization but must
  not require it" is a much stronger claim about all DSAs.
- **Pre-LLM.** BERT is 28% of the 2020 workload and there is no generative decoding anywhere.
  The weight-only / memory-bound argument that dominates 2023+ quantization is absent, even
  though Table 2 and the CMEM result are exactly the evidence that argument needs.

---

## Relation to other entries

**Evidence level — the axis on which this paper wins.** Three entries in the corpus rest on
fabricated silicon, and they are not equivalent:

| Entry | What is silicon-measured | What is not |
|---|---|---|
| **TPUv4i** (ISCA'21) | Everything performance-related: production apps, MLPerf, the CMEM ablation (real hardware, compiler flags + a core disabled), utilization, thermals. Deployed at datacenter scale since March 2020 | **Table 2's energy is modelled**; both accuracy numbers are second-hand; MLPerf runs are unverified |
| [`SamsungNPU`](../SamsungNPU/ANALYSIS.md) (ISCA'21) | 290.7 FPS and 13.6 TOPS/W on 8-bit Inception-v3, 5 nm, shipping mobile SoC | Its **1.79× is simulation** — the headline speedup and the silicon number are different kinds of fact |
| [`RaPiD`](../RaPiD/ANALYSIS.md) (ISCA'21) | A fabricated 4-core 7 nm chip, 36 mm², measured peaks (3.5 TFLOPS/W HFP8, 16.5 TOPS/W INT4) | Everything at system scale is a **performance model calibrated to within 1% of the chip**, then projected to 4 chips / 32 cores |

TPUv4i is the only one measured **in production, on a real workload mix, at scale**, and the
only one that reports what fraction of that workload is quantized. That is its unique
contribution to this survey and it is not a technical one.

**The three ISCA'21 silicon entries make three incompatible bets on precision flexibility.**
This is the sharpest cross-paper observation available here:

- **RaPiD** bets that *precision scaling is the lever* — one datapath spanning FP16/FP8/INT4/INT2,
  split FPU/FXU pipelines, and a roadmap built on getting narrower.
- **SamsungNPU** bets on *modest, reconfigurable* flexibility — INT8/INT16 in a re-configurable
  MAC array, with the lessons section observing that *limiting* reconfigurability costs little
  performance and saves significant area.
- **TPUv4i** bets *against precision flexibility entirely* — it keeps the widest formats,
  gives int8 no performance advantage, and spends the silicon on 128 MB of SRAM instead.

Same venue, same year, three shipping-silicon teams, three different answers. The deciding
variable is not technology but **who bears the cost of a quality regression**: IBM's and
Samsung's customers choose a precision; Google's application teams discover one.

**Multi-precision datapath axis** ([`BitFusion`](../BitFusion/ANALYSIS.md) spatial → RaPiD split
pipelines → SamsungNPU temporal → EVA temporal → XtraMAC DSP bit-space → UniCore adder slices).
**TPUv4i is the axis's null point**: a chip that supports three widths and composes nothing,
because it charges the same for all of them. The organising claim of that axis — *the deciding
variable is what the substrate charges for* — is exactly what Table 2 lets you price, and
TPUv4i's answer is that at 7 nm the substrate charges so little for arithmetic of any width
that composability is not worth the muxes. BitFusion's framing datum (multiplier cost scales
with the *product* of operand bitwidths) can be checked against Table 2 for the first time in
this corpus: INT32 multiply / INT8 multiply = **1.48 / 0.07 = 21×** against a predicted
(32/8)² = 16×, and FP32 / BF16 = **1.31 / 0.21 = 6.2×**. **derived.**

**Compression vs cheaper arithmetic — the proposed missing axis.** TPUv4i is the best evidence
in the corpus for splitting it. Table 2 says an INT8 multiply is **0.07 pJ** and one 64-bit
read from an **8 KB** SRAM is **7.5 pJ** — a factor of **107** — and HBM2 is **250–450 pJ**.
Google's own conclusion: "reduced-precision FLOPS can be relatively free in comparison to memory
references." The chip is built accordingly: 28% of the die is CMEM, 11% is MXUs, and the
perf/TDP win over TPUv3 is attributed **~1.5× to CMEM and only ~1.3× to the node**. Read next to
[`Ecco`](../Ecco/ANALYSIS.md), which decompresses to FP16 between L1 and L2 and so buys bandwidth
rather than arithmetic, this is the industrial confirmation that **the bandwidth branch of the
axis is where the energy is**. It is also the strongest available argument for why weight-only
G3 quantization took the shape it did.

**Retraining axis (PTQ / QAT / structure-preserving retraining).** TPUv4i contributes the
*deployment* view that no algorithm paper in the corpus can: PTQ's real cost is not the accuracy
delta but **months of application-team schedule discovered after tape-out**, and §7.H's argument
for QAT is organizational, not numerical. When the survey says "hardware that cannot consume a
stock checkpoint cannot be deployed", this is the citation.

**Generation.** `G1` by paradigm in 2021, and the corpus's clearest illustration that generation
is not a date: bf16 + fp32 + per-nothing int8, exactly the TPUv2-era format set that
[`TAXONOMY.md`](../../../QuantArchSurvey/TAXONOMY.md) files under G1 silicon. Its contemporaries
in the same venue and year (RaPiD, SamsungNPU, and the G2/G3 academic entries) are one or two
paradigms ahead of it, deliberately.

---

## For the note

### §1 one-line summary

> An inference chip whose data-type decision is to **keep** bf16 and IEEE fp32 from a training
> chip and add int8 only as a porting path — at **the same 138 T peak as bf16**, so int8 buys
> memory footprint and not throughput — because lesson ⑥ of ten is that TPUv1 *required*
> quantization and that was a mistake (developers pre-agreed a 1% quality budget, refused it
> once the silicon existed, and spent months restoring quality in integers), evidenced by a
> production census in which **1 of Google's 8 production DNNs is quantized**, and accompanied
> by the paper's most reusable artefact: **Table 2, Horowitz's energy-per-operation table
> updated to 7 nm** — INT8 multiply **0.07 pJ**, bf16 **0.21**, fp32 **1.31**, INT8 add
> **0.007**, fp32 add **0.38** — whose real lesson is that all of them are dwarfed by **7.5 pJ**
> for one 64-bit 8 KB-SRAM read and **250–450 pJ** for HBM2, which is why the chip spends
> **28% of its die on SRAM and 11% on MXUs**.

### Proposed values on their four axes

| Axis | Proposed | Evidence (one line) |
|---|---|---|
| **Level** | **`ARCH+SYS`** — *seed says `ARCH`; I dispute it, with a caveat* | Two of the ten lessons and two of the ten contribution bullets are software: lesson ② is entirely about compilers (XLA gives **2.2×** on fixed hardware, Figure 2), and the bullet "**Explain why TPUv4i architects chose compiler compatibility over binary compatibility for its VLIW ISA**" is an ISA contribution — the VLIW bundle was widened **25%** precisely because binary compatibility was abandoned (§3). §7.F (XLA's HBM→CMEM prefetch policy for multi-tenancy) and §7.G (LLO vs PTX) are software-stack sections. That is the AGENT-GUIDE tell for `SYS`. **Caveat, stated honestly:** XLA is not *built* by this paper, it is inherited and reasoned about — so `ARCH` alone is defensible if the human wants `SYS` to mean "shipped a new stack". Flagging, not resolving. |
| **Q-oriented** | **`NON-Q-ORIENTED`** — seed agrees, and the close read makes it much stronger | Apply the test: swap int8 for anything, or delete it entirely, and **nothing in the paper changes** — the ten lessons, TCO, multi-tenancy, air cooling, CMEM, compiler compatibility, P99 latency and the 4-input adder all survive untouched. Better than that, the paper's quantization content is an *argument against* quantization being required, and Table 1 shows int8 runs at the **same peak as bf16**, so there is no quantization-serving hardware to remove. `NON-Q-ORIENTED` by the widest margin in the corpus. |
| **Data type** | **`INT8` `BF16` `FP32` `MIXED`** — seed agrees; `MIXED` is the weak one | `BF16` and `FP32`: "retaining bfloat16 and fp32 from TPUv3", §3 **verified**. `INT8`: "TPUv4i also supports int8", §3 + Table 1 **verified**. `MIXED`: three formats coexist on the chip, but **the paper never describes mixing precisions inside a network** — no W8A8, no per-layer widths, no scheme at all. Keep it as "the chip supports several", but do not read it as a mixed-precision *quantization scheme*. Not `INT32`/`FP16` despite both appearing in Table 2 — those are rows of an energy comparison, not TPUv4i datapath formats. |
| **Generation** | **`G1`** — seed agrees, and it is a finding, not a default | Judged by paradigm: bf16 + fp32 + plain int8 with **no scale, no granularity, no outlier handling, no format design** is exactly the format set `TAXONOMY.md` lists as G1 silicon ("TPUv2 BF16"). The G2 test — *does it design a numeric type, or build an architecture whose purpose is to execute quantized arithmetic?* — fails twice: no type is designed, and the MXU gives int8 no advantage. A 2021 chip that is G1 by paradigm, in the same venue and year as a G2 (`RaPiD`) and a G2 (`SamsungNPU`). |
| **Optimization** (free text) | `commercial silicon` `deployed at scale (2020)` `7 nm` `systolic bf16 MXU` `offer quantization, do not require it` `energy per operation (Horowitz updated to 7 nm)` `backwards ML compatibility` `perf/TCO` `compiler compatibility over binary compatibility` `128 MB CMEM` `four-input FP adder` `multi-tenancy` | The seed's four keywords all hold. Three additions matter for this survey: the **energy-per-operation table** (the reason the source CSV flagged the paper), **CMEM** (where the perf/TDP win actually comes from), and **backwards ML compatibility** (the constraint that forbids a new numeric format). |

### Proposed venue-list row

```
| [ ] | [Ten Lessons From Three Generations Shaped Google's TPUv4i](https://doi.org/10.1109/ISCA52012.2021.00010) | *close read* | ARCH+SYS | non-Q | `INT8` `BF16` `FP32` `MIXED` | G1 | `commercial silicon` `deployed 2020` `7 nm` `systolic bf16 MXU` `offer quantization, do not require it` `energy per operation (Horowitz updated to 7 nm)` `backwards ML compatibility` `perf/TCO` `compiler compatibility` `128 MB CMEM` | Lesson ⑥ of ten is a warning: TPUv1 *required* int8 and that hurt in production, so TPUv4i keeps bf16/fp32 and adds int8 **at the same 138 T peak** — memory footprint, not throughput. 1 of 8 production DNNs quantized. **Table 2 (p. 3) is the reason to cite it:** energy/op at 7 nm — INT8 mul 0.07 pJ, bf16 0.21, fp32 1.31 — against 7.5 pJ for one 64-bit 8 KB-SRAM read |
```

*(Changes from the seed at line 79: `ARCH` → `ARCH+SYS` (disputed, see above); `*agent brief*`
→ `*close read*`; data type and generation unchanged; Optimization gains the energy table,
backwards ML compatibility, perf/TCO, compiler compatibility and CMEM; the Note column now
carries the two things a reader of this survey actually needs — that int8 has no throughput
advantage, and that Table 2 exists.)*

### §4 fairness verdict

**Deployed silicon, measured in production** — the corpus's strongest evidence level, but
**not iso-format** (TPUs bf16, T4 int8/fp16), **not iso-node** (7 vs 12 nm) or iso-era, and
MLPerf unverified. Table 2's energy is **modelled, method undisclosed**. **Not to quote bare:**
1.3–1.6× over T4 (perf/TDP is 0.9–1.0×); 138 T (peak, identical for bf16 and int8).

---

## Note from the source list

> **Keywords:** Provide "Energy per Operation"; FP32 to 8-bit

**Answered.** The energy-per-operation table is **Table 2, page 3**, titled *"Energy per
Operation: 45 nm [16] vs 7 nm. Memory is pJ per 64-bit access."* The 45 nm column is
Horowitz's ISSCC 2014 table; the 7 nm column is Google's own **model** (method undisclosed).
"FP32 to 8-bit" at 7 nm: multiply **1.310 → 0.070 pJ (18.7×)**, add **0.380 → 0.007 pJ
(54.3×)**. The frame that must travel with those numbers: they are **per single operation**,
**modelled not measured**, and **memory is on the same table** at 7.5–14 pJ per 64-bit SRAM
access and 250–1300 pJ per DRAM access, which is the comparison the paper itself draws.

## Abstract (verbatim, from the archived PDF)

> Google deployed several TPU generations since 2015, teaching us lessons that changed our
> views: semiconductor technology advances unequally; compiler compatibility trumps binary
> compatibility, especially for VLIW domain-specific architectures (DSA); target total cost of
> ownership vs initial cost; support multi-tenancy; deep neural networks (DNN) grow 1.5X
> annually; DNN advances evolve workloads; some inference tasks require floating point;
> inference DSAs need air-cooling; apps limit latency, not batch size; and backwards ML
> compatibility helps deploy DNNs quickly. These lessons molded TPUv4i, an inference DSA
> deployed since 2020.

---

## Appendix — Table 2 as printed (page 3)

Recovered from the `-layout` extraction; `--` is a blank cell in the original.

| Op | Format | 45 nm (pJ) | 7 nm (pJ) | 45/7 |
|---|---|---|---|---|
| **+** | Int 8 | 0.030 | **0.007** | 4.3 |
| **+** | Int 32 | 0.100 | 0.030 | 3.3 |
| **+** | BFloat 16 | -- | **0.110** | -- |
| **+** | IEEE FP 16 | 0.400 | 0.160 | 2.5 |
| **+** | IEEE FP 32 | 0.900 | **0.380** | 2.4 |
| **✕** | Int 8 | 0.200 | **0.070** | 2.9 |
| **✕** | Int 32 | 3.100 | 1.480 | 2.1 |
| **✕** | BFloat 16 | -- | **0.210** | -- |
| **✕** | IEEE FP 16 | 1.100 | 0.340 | 3.2 |
| **✕** | IEEE FP 32 | 3.700 | **1.310** | 2.8 |
| SRAM | 8 KB | 10.000 | **7.500** | 1.3 |
| SRAM | 32 KB | 20.000 | 8.500 | 2.4 |
| SRAM | 1 MB¹ | 100.000 | 14.000 | 7.1 |
| — | **GeoMean¹** | -- | -- | **2.6** |
| DRAM | DDR3/4² | 1300 | 1300 | 1.0 |
| DRAM | HBM2² | -- | 250–450 | -- |
| DRAM | GDDR6² | -- | 350–480 | -- |

¹ Horowitz's 1 MB SRAM figure is a single-bank SRAM; most designs would use multiple banks,
which explains the 7.1× reduction. **It is omitted from the geomean.**
² 1300 pJ for DDR3/4 is **I/O only** [43]; HBM2 and GDDR6 also list **only I/O energy**
[26, 32, 42].
Memory rows are **pJ per 64-bit access**; arithmetic rows are pJ per single operation.

---

## Reported, not applied

Changes I am **not** making, per the standing rule that `survey/README.md`, `survey/TAGS.md`,
`survey/papers-tags.csv` and everything under `QuantArchSurvey/` are the human's.

1. **`survey/TAGS.md` — drop `mixed-precision` (5) from TPUv4i.** TAGS.md defines (5) as the
   *quantization scheme* mixing precisions (W4A8, per-layer widths, INT4 inliers + FP16
   outliers). TPUv4i has **no quantization scheme**; it has three supported formats and no
   description of using more than one at a time. That would take (5) from 23 papers to 22 and
   changes the reverse index at line 70 and the matrix row at line 170. `analytical-dtype` (2)
   and `accelerator` (8) both stay. `multi-bitwidth-hw` (9) was checked and does **not** apply:
   nothing is reconfigurable, and int8 and bf16 run at the same rate.
2. **`QuantArchSurvey/venues/ISCA/README.md` line 79** — the row above, and the `Verified`
   column from *agent brief* to *close read*. The seed's **`non-Q`, `G1`, and the four data
   types are all confirmed**; the only substantive dispute is `ARCH` → `ARCH+SYS`.
3. **`survey/README.md`** — TPUv4i's status goes from `brief ready` to `analysis ready`.
