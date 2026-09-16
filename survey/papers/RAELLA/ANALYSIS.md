# RAELLA — paper notes

**RAELLA: Reforming the Arithmetic for Efficient, Low-Resolution, and Low-Loss Analog PIM: No Retraining Required!**
Tanner Andrulis, Joel S. Emer, Vivienne Sze
**ISCA 2023** ｜ DOI: **not recorded** — the ACM/IEEE record is not reachable by script (403); look it up when citing
Venue evidence (2026-09-02): arXiv `comments` field, verbatim: *"16 pages; 15 figures; Accepted at ISCA 2023 (the International Symposium on Computer Architecture)"*
Archived here: **arXiv:2304.07935v1** (2023-04-17), 16 pages — **the preprint, not the
published ISCA 2023 version**; the two were **not compared**.

Status: **note ready** ｜ Last updated: 2026-09-14
Tags: `pim-ndp` `combined-dtype` `dtype-granularity` `multi-bitwidth-hw` `accelerator`
How far it was read: **close read of the abstract, §1-§2 (motivation and the prior-PIM taxonomy),
§3 (all three mechanisms — Center+Offset, Adaptive Weight Slicing, Dynamic Input Slicing), and §6
(methodology and results)**; the tile/IMA dataflow was read for cost rather than circuit detail.
Numbers below come from prose. The corpus's **first analog / ReRAM PIM entry**.

> Original: https://arxiv.org/abs/2304.07935
> The PDF is **not committed** (2.6 MB). Re-download: `curl -sSL -o 2304.07935.pdf https://arxiv.org/pdf/2304.07935`
> Extract text: `python3 extract.py` → `extracted/` (committed, greppable)
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, ISCA 2023 row.

---

## Brief

### 1. Motivation

Analog processing-in-memory should be efficient — ReRAM crossbars compute densely in place —
but **ADCs dominate the energy**, so much that some PIM accelerators do not beat digital
ones. Existing fixes either lower ADC resolution (losing fidelity) or prune/retrain the DNN,
and **retraining may be impossible** when training data is private or the training recipe is
model-specific.

### 2. Overview

Adapt the *arithmetic* to the architecture so that analog values are small and thus cheap to
digitize: **encode weights to produce near-zero analog values** (Center+Offset),
**adaptively slice weights** per layer, and **dynamically slice inputs** with speculation
and recovery. Low-resolution analog values then permit low-resolution ADCs and fewer
converts, with no retraining.

### 3. Pros and cons

**Pros**

- "No retraining required" is the load-bearing claim and the paper argues for it as a
deployability property, not a convenience — a well-made point about who can actually use a
technique.
- Up to 4.9× energy efficiency and 3.3× throughput over other low-accuracy-loss PIM
accelerators, and it matches retraining-based designs *without* retraining.
- The Center+Offset encoding is a nice instance of representing a value as two components
chosen to suit the physics — a combined data type driven by hardware, not statistics.

**Cons**

- Entirely within the ReRAM analog-PIM setting, which carries device non-idealities, write
costs and maturity questions the paper mitigates but cannot remove.
- Speculation-and-recovery for input slicing implies a variable-cost path; worst-case
behaviour is less visible than the average results shown.
- Evaluated on CNN-era models; nothing here about transformers or LLM-scale weights.

### 4. Where it applies

The **analog PIM** entry in the corpus, and a useful counterexample: it shows the constraint
driving the data-type design can be a *circuit* constraint (ADC resolution) rather than a
statistical one. Read with [`P3-LLM`](../P3-LLM/ANALYSIS.md) and
[`NDPLowBitFP`](../NDPLowBitFP/ANALYSIS.md) for the digital PIM/NDP contrast.

---

## Conclusions

**The premise is that in analog PIM the ADC is the budget, so the arithmetic should be redesigned to
produce values the ADC can cheaply digitize.** That inverts the usual direction: everywhere else in
this corpus a format is chosen to fit the data distribution and the hardware is then built to
execute it. RAELLA chooses an encoding so that **the analog quantity being measured is small by
construction**, and the ADC requirement falls out. It is the purest instance of
hardware-constraint-driven data type in the corpus.

**Center+Offset is the idea, and it is a physics argument, not a statistics one.** RAELLA "**shifts
DNN weights to equalize the average magnitude of the positive and negative weight slices in each
crossbar column**", so that "as analog-domain calculations are accumulated, **positive and negative
results negate to produce near-zero sums**". The crossbar still accumulates many values in analog —
which is what makes PIM efficient — but the *result* stays near zero, so a low-resolution ADC
suffices. Prior designs faced a trade between how many weights you may accumulate and how precisely
you can read the sum; RAELLA breaks it by making the sum small rather than by limiting the
accumulation.

**The mechanism number is the one to carry: column-sum resolution 17b → 7b, ADC saturation 98% →
0.1%.** On ResNet18/ImageNet, Figure 3 shows the three strategies compounding to that. A 98%
saturation rate means the baseline's ADC was effectively clipping almost every conversion — the
before/after pair explains the whole design in two numbers, and is far more informative than the
4.9× headline.

**"No retraining required" is argued as a deployability property and the argument is good.** §2
states it plainly: retraining "has a very high computational cost, can require cumbersome
hyperparameter tuning to achieve high accuracy, and **may be impossible if the training data is
private**." Both prior PIM families — Weight-Count-Limited and Sum-Fidelity-Limited — retrain to
recover what their ADC constraints cost. RAELLA matches them without it. Across this corpus the
PTQ/QAT distinction is usually a line in a table; here it is the thesis.

**The three mechanisms are one idea applied at three points.** Every one of them exists to shrink
the column sum: **Center+Offset** cancels it, **Adaptive Weight Slicing** tunes bits-per-weight-slice
per layer, **Dynamic Input Slicing** tunes bits-per-input-slice at runtime with speculation and
recovery. The last is the only place RAELLA spends cycles to buy resolution, and it hedges that with
speculation.

---

## Method

**The problem taxonomy** (§2) **verified** — worth borrowing, because it cleanly partitions prior
analog PIM:

| Family | Constraint | Consequence |
|---|---|---|
| **Weight-Count-Limited** | limit how many weights accumulate in analog so the ADC can resolve the sum | throughput loss |
| **Sum-Fidelity-Limited** | use a lower-resolution ADC on a high-resolution analog value | fidelity loss and error |

"To reduce this accuracy loss, **both** … retrain DNNs."

**Center+Offset encoding** (§3.1) **verified**. Shift weights so that, within each crossbar column,
the **average magnitude of positive and negative weight slices is equalised**. Accumulation in the
analog domain then self-cancels toward **near-zero sums**, which a low-resolution ADC can convert
faithfully. This lets RAELLA **accumulate more values in analog** while keeping sums small — the two
things prior designs had to trade against each other.

**Adaptive Weight Slicing** (§3.2) **verified**. "More bits per weight slice increase the values
stored in weight slices, raising column sum values and resolutions." So bits-per-weight-slice is
chosen **per DNN layer**, offline. RAELLA "uses a simple preprocessing strategy and **reuses DNN
weights for many inferences to minimize preprocessing costs**". Result: **column sum resolution is
≤ 7b 82.1% of the time**.

**Dynamic Input Slicing** (§3.3) **verified**. Same problem on the input side. Fewer bits per input
slice lowers column sums but costs **more cycles and more ADC converts**, so the slicing is chosen
**at runtime**, with **speculation and recovery** to avoid paying the cost when it is not needed.

**Dataflow** (§4-5). Tiles consume input rows from the previous tile in the same top-to-bottom order,
so communication and reuse patterns are **fixed at program time** by pattern generators; **Timeloop**
finds reuse patterns below the tile level. Weights are **replicated** to raise throughput —
in-crossbar via a partial Toeplitz expansion, then across crossbars, IMAs and tiles, by a greedy
policy.

**Retraining: none.** That is the paper's title claim and its organising constraint.

---

## Key numbers, with their frame

Evidence level: **analytical architecture modelling with Accelergy/Timeloop at 32 nm**, with
8-bit DNNs, under a **600 mm² area budget**. Baselines `ISAAC` and `FORMS` are modelled **in the
same flow**; **`TIMELY`'s results are taken from its own paper**, with RAELLA rescaled to TIMELY's
**65 nm** node and TIMELY's analog components substituted. **No silicon, no SPICE-level results
reported here.**

| Setting | Model | Metric | Baseline | Result | Source |
|---|---|---|---|---|---|
| **The mechanism, measured** | ResNet18 / ImageNet | **column sum resolution** | baseline **17 b** | **7 b** | Fig. 3 **verified** |
| " | " | **ADC saturation rate** | baseline **98%** | **0.1%** | Fig. 3 **verified** |
| Adaptive Weight Slicing alone | " | share of column sums at ≤ 7 b | — | **82.1%** | §3.2.4 **verified** |
| Headline | — | **energy efficiency** | other **low-accuracy-loss** PIM accelerators | **up to 4.9×** | abstract **verified** |
| Headline | — | **throughput** | same | **up to 3.3×** | abstract **verified** |
| The deployability claim | — | efficiency and throughput | PIM accelerators **that retrain** | **similar — without retraining** | abstract **verified** |
| Area budget | — | tiles fitted at **600 mm²** | **ISAAC 1024, FORMS 1024** | **RAELLA 743** | §6.1 **verified** |
| Node | — | — | — | **32 nm** (Accelergy/Timeloop); **65 nm** for the TIMELY comparison | §6.1 **verified** |

**RAELLA fits 743 tiles where ISAAC and FORMS fit 1024** at the same area — a **27% tile deficit**
that its per-tile efficiency has to overcome. The paper states this openly, and it makes the
iso-area comparison meaningful rather than nominal.

---

## Cost and requirements

| | |
|---|---|
| **Per-layer preprocessing** | Adaptive Weight Slicing needs an offline pass per layer; amortised because "DNN weights [are reused] for many inferences" |
| **Runtime speculation** | Dynamic Input Slicing speculates and recovers — recovery cost is the exposure, and it is the only mechanism that can cost cycles |
| **Bigger tiles** | **743 vs 1024 tiles** at iso-area: the encoding and slicing machinery is not free |
| **Program-time fixed dataflow** | Communication patterns are fixed by pattern generators at program time — flexibility is traded for cost |
| **Weight replication** | Throughput relies on replicating weights (partial Toeplitz in-crossbar, then across crossbars/IMAs/tiles) — a capacity cost |
| **Retraining** | **None — this is the point.** No calibration dataset is mentioned either |
| **Escape hatch** | The ADC itself, and whatever digital periphery handles the Center+Offset correction |
| **Scope** | 8-bit CNNs (ResNet18-class) on ImageNet. **Pre-LLM**, and analog PIM's constraints do not obviously transfer to transformer decode |

---

## Limitations and open questions

**Admitted.** RAELLA fits fewer tiles than ISAAC/FORMS at equal area. Dynamic Input Slicing costs
cycles and converts when speculation misses. TIMELY is compared across a node boundary using
TIMELY's own reported numbers.

**Unadmitted, and material.** (i) **Everything is analytical** — Accelergy/Timeloop models, not
SPICE or silicon; for an *analog* design, device non-idealities (conductance drift, write variance,
IR drop) are the obvious risk and are not visible in the numbers I read. (ii) **The 17b→7b and
98%→0.1% figures are for one network** (ResNet18/ImageNet) and are the strongest claim in the paper;
their spread across models is not given in the text I read. (iii) **Speculation-miss rate is never
quoted** — Dynamic Input Slicing's cost depends on it entirely. (iv) **No LLM or transformer
workload**, which limits how far the survey can carry it.

---

## Relation to other entries

**It is the corpus's only analog/ReRAM entry, and it opens a third substrate.** The survey now has:
**logic-die** accelerators (most entries), **DRAM/near-memory** (`P3-LLM`, `NDPLowBitFP`), and
**analog PIM in ReRAM crossbars** (RAELLA). Each substrate imposes a different scarce resource —
multiplier area, DRAM row locality, and here **ADC energy and resolution** — and in all three cases
that scarcity, not the data distribution, is what selects the numeric format. That is a strong
organising claim and RAELLA is the third and most extreme instance.

**Center+Offset belongs on the outlier-currency axis, at an entirely new position.** Every other
entry pays for range with *bits, metadata, a destroyed neighbour, or a second datapath*. RAELLA pays
by **arranging for the quantity being measured to cancel**. The currency is **sign balance within a
crossbar column** — it costs nothing at read time and is bought by an offline weight shift.

**Its "no retraining" argument is the corpus's best statement of PTQ as a deployability property**
rather than a convenience, and should be cited for that. Compare `DRQ`, which requires QAT and never
says so outside §III-D, and `P3-LLM`/`LightNobel`, which are calibration-free but argue it as an
accuracy property (overfitting) rather than an access property (private training data).

**It also answers `RaPiD`'s and `SamsungNPU`'s question from the far end.** Those two show that in
a product the scarce resource is not the multiplier. RAELLA shows a substrate where the scarce
resource is not even the arithmetic — it is the **conversion between domains**. Any survey section
on "what does quantization actually buy" should have all three.

**The `G1` → `G2` revision is correct on the merits.** The log's reasoning — "the arithmetic is
redesigned for the ADC constraint — adaptive weight slicing, dynamic input slicing, Center+Offset
encoding" — is exactly what the close read finds. This is a *representation* change driven by
hardware, which is the `G2` paradigm; it is not plain per-tensor scaling (`G1`), and it has no
outlier format or codebook (`G3`).

**Node.** **32 nm** modelled (plus a 65 nm point for TIMELY) — the coarsest in the corpus alongside
`OLAccel`'s 65 nm, and the only one whose "node" also implies an analog device technology. It cannot
share a column with digital entries.

---

## For the note

**§1 one-line summary.** Redesigns the *arithmetic* of analog ReRAM PIM so that the analog quantity
the ADC must digitize is **small by construction** — **Center+Offset** shifts weights to equalise
positive and negative slice magnitudes within each crossbar column so accumulated results
**self-cancel toward zero**, **Adaptive Weight Slicing** tunes bits-per-weight-slice per layer, and
**Dynamic Input Slicing** tunes bits-per-input-slice at runtime with speculation and recovery —
cutting column-sum resolution from **17 b to 7 b** and ADC saturation from **98% to 0.1%**, which
buys low-resolution ADCs and fewer converts for **up to 4.9× energy efficiency and 3.3× throughput**
over low-loss PIM baselines, **with no retraining**.

**Proposed tags — the seed row stands, including the log's `G1` → `G2` revision.**

| Axis | Value | Evidence |
|---|---|---|
| **Level** | `ALGO+ARCH` | Center+Offset and the two slicing strategies are algorithmic (offline weight transformation, per-layer search, runtime policy); the crossbar/tile architecture executes them. Neither works alone. Seed agrees. **Checked against the `SYS` rule**: Timeloop is a mapping tool the authors *use*, not a compiler they contribute, so no `SYS` |
| **Q-oriented** | `Q-ORIENTED` | Slicing bits, encoding weights and shaping analog value distributions are all quantization decisions; the ADC-resolution saving exists only because of them |
| **Data type** | `INT` `ADAPTIVE` `MIXED` | 8-bit DNNs sliced into per-layer-adaptive weight slices and runtime-adaptive input slices. **`ADAPTIVE` here names a genuine format property** (slice width), like UniCore's DynFP and unlike the selection-policy uses elsewhere |
| **Generation** | `G2` | **The log's `G1` → `G2` revision is right**: the arithmetic is redesigned for a hardware constraint — a representation change, not per-tensor scaling. No outlier format, no codebook |
| **Optimization** | `analog PIM` `ReRAM crossbar` `Center+Offset encoding` `adaptive weight slicing` `dynamic input slicing` `speculation and recovery` `ADC-resolution reduction` `no retraining` | |

**§4 fairness verdict.** Iso-area at **600 mm²** with `ISAAC` and `FORMS` modelled in the **same
Accelergy/Timeloop flow at 32 nm** — and RAELLA discloses that it fits only **743 tiles to their
1024**, so its per-tile efficiency must overcome a 27% deficit. `TIMELY` is different: its numbers
are **quoted from its own paper**, with RAELLA rescaled to **65 nm** and TIMELY's analog components
substituted. Everything is **analytical modelling, not SPICE or silicon**, which for an analog design
leaves device non-idealities invisible. The **17b→7b / 98%→0.1%** figures are for **ResNet18 only**,
and the **speculation-miss rate** that prices Dynamic Input Slicing is never quoted.

**Proposed venue-list row:**

```
| [ ] | [RAELLA: Reforming the Arithmetic for Efficient, Low-Resolution, and Low-Loss Analog PIM: No Retraining Required!](https://arxiv.org/abs/2304.07935) | *close read* | ALGO+ARCH | Q | `INT` `ADAPTIVE` `MIXED` | G2 | `analog PIM` `ReRAM crossbar` `Center+Offset encoding` `adaptive weight slicing` `dynamic input slicing` `ADC-resolution reduction` `no retraining` | Encode weights so positive and negative slices **cancel within a crossbar column** — the analog sum is near zero by construction, so a cheap ADC suffices. **17b → 7b column sums, 98% → 0.1% ADC saturation**, no retraining |
```

## Note from the source list

> **Keywords:** encoding weights to produce near-zero analog values; Center+Offset


## Abstract (verbatim, arXiv:2304.07935v1)

> Processing-In-Memory (PIM) accelerators have the potential to efficiently run Deep Neural
> Network (DNN) inference by reducing costly data movement and by using resistive RAM
> (ReRAM) for efficient analog compute. Unfortunately, overall PIM accelerator efficiency is
> limited by energy-intensive analog-to-digital converters (ADCs). Furthermore, existing
> accelerators that reduce ADC cost do so by changing DNN weights or by using low-resolution
> ADCs that reduce output fidelity. These strategies harm DNN accuracy and/or require costly
> DNN retraining to compensate. To address these issues, we propose the RAELLA architecture.
> RAELLA adapts the architecture to each DNN; it lowers the resolution of computed analog
> values by encoding weights to produce near-zero analog values, adaptively slicing weights
> for each DNN layer, and dynamically slicing inputs through speculation and recovery. Low-
> resolution analog values allow RAELLA to both use efficient low-resolution ADCs and
> maintain accuracy without retraining, all while computing with fewer ADC converts.
> Compared to other low-accuracy-loss PIM accelerators, RAELLA increases energy efficiency
> by up to 4.9$\times$ and throughput by up to 3.3$\times$. Compared to PIM accelerators
> that cause accuracy loss and retrain DNNs to recover, RAELLA achieves similar efficiency
> and throughput without expensive DNN retraining.
