# RAELLA: Reforming the Arithmetic for Efficient, Low-Resolution, and Low-Loss Analog PIM: No Retraining Required!

**Venue / Year:** ISCA 2023 · **Link:** https://arxiv.org/abs/2304.07935 · **Reader:** Haoxuan · **Date:** 2026-09-14

## Tags

| | |
|---|---|
| **Level** | `ALGO+ARCH` |
| **Q-oriented** | `Q-ORIENTED` |
| **Data type** | `INT` `ADAPTIVE` `MIXED` |
| **Generation** | `G2` |
| **Stage type** | `S2T5` · `S3T2` |
| **Optimization** | analog PIM · ReRAM crossbar · Center+Offset encoding · adaptive weight slicing · dynamic input slicing · speculation and recovery · ADC-resolution reduction · no retraining |

## Stage-type tags

**`S2T5` · `S3T2`** (the **Stage type** row in Tags) — most-matched first. Adaptive weight slicing and dynamic input slicing split the multiply along the bit dimension (`S2T5`) on an analog ReRAM crossbar whose ADC is the return to ordinary numbers (`S3T2`). No `(PIM)` tag: the substrate is already in the Platform column (`PIM`); owner's ruling 2026-10-03, when the record's Stage was also set to `—`.

*Tag form `S{stage}T{type}`, vocabulary from `survey/stage2.md` and `survey/stage3.md`. Added 2026-10-02 (ISCA Stage-type batch 1); `(PIM)` split out into its own tag the same day and removed on 2026-10-03.*

## 1. One-line summary

Redesigns the *arithmetic* of analog ReRAM PIM so the analog quantity the ADC must digitize is
**small by construction** — **Center+Offset** shifts weights to equalise positive and negative slice
magnitudes within each crossbar column so accumulated results **self-cancel toward zero**,
**Adaptive Weight Slicing** tunes bits-per-weight-slice per layer, and **Dynamic Input Slicing**
tunes bits-per-input-slice at runtime with speculation and recovery — cutting column-sum resolution
from **17 b to 7 b** and ADC saturation from **98% to 0.1%**, buying low-resolution ADCs and fewer
converts for **up to 4.9× energy efficiency and 3.3× throughput**, **with no retraining**.

## 2. Data type

**The ADC is the budget, so the format is chosen to fit the ADC — not the data.** Inverts the usual direction: everywhere else a format fits the distribution and hardware executes it.
**Center+Offset.** Shift weights so that within each crossbar column the **average magnitude of positive and negative weight slices is equal**. Analog accumulation then **self-cancels toward near-zero sums**, convertible at low resolution — so you can accumulate *more* values in analog, not fewer.
**Adaptive Weight Slicing.** Bits per weight slice chosen **per layer**, offline. More bits/slice → larger column sums → higher ADC resolution needed. Result: column sums **≤ 7 b, 82.1% of the time**.
**Dynamic Input Slicing.** Bits per input slice chosen **at runtime**, with **speculation and recovery** — fewer bits lowers sums but costs cycles and converts.
**Base precision.** 8-bit DNNs, sliced. `ADAPTIVE` here names a real format property (slice width), not a selection policy.
**Outliers.** No outlier class. Range is handled by **cancellation**, which is a position nothing else in the corpus occupies.
**Accumulator.** The analog column itself; the "resolution" that matters is the **ADC's**, driven from 17 b down to 7 b.
**Escape hatch.** The ADC and the digital periphery that undoes the Center+Offset shift.
**Retraining.** **None — that's the title claim and the organising constraint.** No calibration dataset either.

## 3. Optimization

**The prior-work taxonomy is worth borrowing.** Analog PIM designs fail in one of two ways:
**Weight-Count-Limited** (limit how many weights accumulate so the ADC can resolve the sum — costs
throughput) or **Sum-Fidelity-Limited** (use a cheap low-resolution ADC on a high-resolution analog
value — costs fidelity). "To reduce this accuracy loss, **both** … retrain DNNs."

**Center+Offset breaks the trade rather than picking a side.** Prior designs must choose between
accumulating many values and reading the sum precisely. RAELLA makes the **sum** small instead of
limiting the **accumulation**: equalise positive and negative slice magnitudes per column, and the
analog result cancels toward zero. A physics argument, not a statistical one.

**The mechanism number tells the story better than the headline.** Figure 3, ResNet18/ImageNet:
column-sum resolution **17 b → 7 b**, ADC saturation **98% → 0.1%**. A 98% saturation rate means the
baseline's ADC was clipping nearly every conversion. Those two numbers explain the entire design.

**All three mechanisms are one idea at three points** — every one exists to shrink the column sum.
Only Dynamic Input Slicing can cost cycles, and it hedges that with speculation.

**"No retraining" is argued as deployability, and the argument is good.** §2: retraining "has a very
high computational cost, can require cumbersome hyperparameter tuning…, and **may be impossible if
the training data is private**." Across the corpus the PTQ/QAT distinction is usually a table entry;
here it's the thesis.

## 4. Results

| | |
|---|---|
| Baseline | **ISAAC** and **FORMS** modelled in the same flow; **TIMELY** quoted from its own paper (cross-node) |
| Models / datasets | 8-bit CNNs, ResNet18-class, on ImageNet. **Pre-LLM, no transformer workload** |
| Accuracy delta | **Low loss without retraining**; matches retraining-based designs. Center+Offset's accuracy contribution shown separately |
| Speedup | **up to 3.3× throughput** over other low-accuracy-loss PIM |
| Energy / area | **up to 4.9× energy efficiency**. At **600 mm²**, RAELLA fits **743 tiles** where ISAAC and FORMS fit **1024** — a 27% tile deficit its per-tile efficiency must overcome |
| Technology node | **32 nm** via Accelergy/Timeloop; rescaled to **65 nm** for the TIMELY comparison |
| Evidence level | **Analytical architecture modelling (Accelergy/Timeloop).** No silicon, no SPICE — so analog device non-idealities are invisible |
| **Is the comparison fair?** | Iso-area at 600 mm², with ISAAC and FORMS modelled in the **same flow at 32 nm**, and RAELLA discloses its **743-vs-1024 tile deficit**. But TIMELY is **quoted from its own paper** across a node boundary; everything is **analytical, not SPICE or silicon**, so analog device non-idealities are invisible; 17b→7b / 98%→0.1% is **ResNet18 only**; the **speculation-miss rate** is never quoted |

## 5. Comment

## 6. Claude notes

> **Suggestions from the reading agent. Strip this section before copying into
> `QuantArchSurvey/venues/ISCA/notes/`.**

- **§5 material, if you want it — this opens a third substrate and completes a claim I think the
  survey should make explicitly.** We now have **logic-die** accelerators (most entries),
  **DRAM/near-memory** (P3-LLM, NDPLowBitFP), and **analog PIM in ReRAM** (RAELLA). Each substrate
  makes a *different* resource scarce — multiplier area, DRAM row locality, **ADC energy and
  resolution** — and in all three the scarcity, not the data distribution, is what selects the
  numeric format. RAELLA is the third and most extreme instance: here the arithmetic is redesigned
  around the **conversion between domains**, not the arithmetic itself.
- **Center+Offset is a genuinely new position on the outlier-currency axis.** Everything else pays
  for range with bits, metadata, a destroyed neighbour, or a second datapath. RAELLA pays with
  **sign balance within a crossbar column** — free at read time, bought by an offline weight shift.
  The quantity being measured is arranged to cancel.
- **The number to carry is 17b → 7b and 98% → 0.1%, not 4.9×.** The saturation figure in particular
  says the baseline ADC was clipping almost every conversion — it explains the design in a way the
  efficiency ratio doesn't.
- **This is the corpus's best statement of PTQ as a *deployability* property.** Compare DRQ (needs
  QAT and says so only in §III-D) and P3-LLM / LightNobel (calibration-free, but argued as an
  *accuracy* property — overfitting — rather than an *access* property: private training data,
  unavailable recipes). If the survey has a paragraph on why PTQ matters, this is the citation.
- **The log's `G1` → `G2` revision is correct on the merits** — the close read finds exactly what
  the log claimed: the arithmetic is redesigned for the ADC constraint. That's a representation
  change driven by hardware (`G2`), not per-tensor scaling (`G1`), and there's no outlier format or
  codebook (`G3`).
- **`ADAPTIVE` is doing real work here**, as in UniCore's DynFP — it names slice *width*, a format
  property, not a selection policy. That's now two entries where `ADAPTIVE` is legitimate and
  several where I've recommended moving it to Optimization. Might be worth a consistency pass.
- **Node needs its own treatment.** 32 nm modelled (65 nm for TIMELY) is the coarsest in the corpus
  alongside OLAccel — and it's the only entry whose "node" also implies an **analog device
  technology**. It can't share a column with digital entries under any scaling.
- **The scope limit is real:** 8-bit CNNs on ImageNet, pre-LLM. Analog PIM's constraints don't
  obviously transfer to transformer decode, so I'd cite it for the *principle* (substrate selects
  format) rather than for any number.
