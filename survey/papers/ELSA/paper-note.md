# ELSA: An ELastic SNN Inference Architecture for Efficient Neuromorphic Computing

**Venue / Year:** ISCA 2026, pp. 2550-2566 · **Link:** https://doi.org/10.1109/ISCA66397.2026.00178 · **Reader:** Haoxuan · **Date:** 2026-09-14

## Tags

| | |
|---|---|
| **Level** | `ARCH+SYS` |
| **Q-oriented** | `NON-Q-ORIENTED` |
| **Data type** | `TERNARY` `INT4` `MIXED` |
| **Generation** | `—` |
| **Optimization** | SNN · elastic inference · spine/token-wise pipeline · bundled AER · early termination · input-adaptive time-steps · mini-batch Gustavson-product · membrane-stationary dataflow · addition-only · near-SRAM · ANN-to-SNN conversion (SpikeZIP-TF) · NoC mapping + multi-path routing |

## 1. One-line summary

Runs a **4-bit-weight quantized ANN as an exactly equivalent spiking network** — the
activation re-coded from a binary-weighted integer into a **temporal unary train of ternary
{−1,0,+1} events over T ≤ 32 time-steps**, so every MAC becomes a 4-bit add into a **12-bit
membrane potential that lives in SRAM, one word per neuron** — and then spends the entire
architecture on making that code cheap: a **spine/token-wise pipeline** forwarding one output
row the instant it exists (first response **O(L)** not **O(L×N)**), a **bundled AER** flit
amortising one 12-bit row address over 17 spikes (425 → 256 bits), and a **mini-batch
Gustavson product** keeping the wide membrane row stationary so it is read and written once —
buying **3.4× throughput and 13.6× energy efficiency over ANT** at 28 nm and equal ImageNet
accuracy, at **22× ANT's area** with **half the die being membrane SRAM**, and turning the
time-step count itself into a **per-input precision knob** (avg T = 6.2 of 32; 21.9% latency
for <0.2% accuracy).

## 2. Data type

**The network is a QANN.** ST-BIF neuron ≡ quantized ReLU; SNN converted from a 4-bit-weight QANN via SpikeZIP-TF; QANN and SNN accuracies **identical to the decimal** on ResNet18/34/50 and ViT-S. The 2.57-point ImageNet drop is the *quantization*, not the spiking.

**Formats.** Weights **INT4**. Spikes **ternary {−1,0,+1}** — on the wire a 12-bit position + **1-bit sign**, 2 b inside the fire component. Membrane **12-bit**. Spike tracer **4-bit** (derived from Tab. III memory ratio 307.2 : 102.4 = 3; not stated).

**The activation's real format is temporal unary.** 1 bit per time-step × up to **T = 32**. `T` is the bitwidth analogue: NoC traffic ≈ **linear in T** (Fig. 6 — SNN crosses Eyeriss at ~2 steps, hits 3.4-7× by T = 8).

**Granularity.** **None.** No scales, no groups, no exponents, no metadata of any kind. `V_thr` is the only per-layer constant, and Fig. 9 draws it as `2^N`.

**Accumulator = the escape hatch.** The membrane: **12-bit, in SRAM, one word per neuron, all resident.** **52.44%** of a neural core's area, **4.2%** of its power. The dataflow exists to keep that ratio.

**Effective bitwidth.** A "1-bit" activation costs **16 bits of persistent per-neuron state** (12 membrane + 4 tracer) and up to 32 events. 72 MB on-chip; DRAM touched only for the input.

**Outliers.** **None** — the word does not appear. Range is handled by saturation (`S_max`/`S_min` clamp in the fire rule), not by an outlier path.

**Second escape hatch.** `ssoftmax` + `slayernorm` in integer-only units inherited from SwiftTron, **width never stated**, 6.72% of chip area.

**Retraining.** Neither PTQ nor QAT — **exact conversion from an already-quantized checkpoint**. The quantization is entirely upstream and uncharacterised; the **activation bitwidth is never given**. ViT-S is the exception, trained by the authors.

## 3. Optimization

**Spine/token-wise pipeline.** A *spine* is `Z^{1×1×C}` (one spatial position, all channels); a *token* is `Z^{1×D}`. Prior time-step-by-time-step accelerators advance a layer only once all `N` spines/tokens finish; ELSA forwards each on production, dropping first-response latency from `O(L×N)` to `O(L)` (Spikformer: L = 74, N = 197). For CNNs an output scheduler emits spines **right-to-left / bottom-to-top** so the next layer's first spine becomes computable as early as possible, deferring padding-dependent spines to the end. Transformers stall once, at `ssoftmax`, which needs all Q and K tokens. Worth **5.61-36.05×** over no pipeline, **2.2-2.8×** over a layer-wise one.

**Bundled AER.** Conventional AER pays a full header per spike: 17 spikes × 25 b = 425 b. BAER sends one 256-b flit — 6-b destination, 2-b type, **one** 12-b spine/token ID, then 17 × (12-b position + 1-b sign), + 15-b ECC. ≈15 b per spike; **19.1% less traffic than TrueNorth, 36.7% less than MorphIC**. Short tails zero-padded.

**Mini-batch Gustavson-product.** Gustavson is membrane-stationary — each output row read and written once — which is the right choice because the membrane is 12 b against 4 b weights and 1 b spikes. It needs row-aligned input, which asynchronous spikes destroy. ELSA does **not** synchronise; BAER's row-bundling already *is* the alignment, so one flit = one mini-batch = one membrane read, `N` parallel weight-row accumulations, one write-back. **The protocol and the dataflow are one decision seen from two ends.** Buys 2.7× over inner-product, 1.9× over outer-product; buffer-energy share falls 76.2% (IP, weights) / 70.3% (OP, membrane) → 43.1% combined.

**Elastic inference is a per-input precision knob.** Confidence-based early termination — max class probability, or YOLO objectness — truncates the unary code at run time. **Avg T = 6.2 of an allowed 32.** 21.9% mean latency for <0.2% accuracy; 30.6% for ≈3.4%. Note what the hardware does and does not do: **the SNN supplies the monotone precision ladder for free; the pipeline only lets you cash it in sooner.** Nothing in ELSA decides `T`.

**Datapath and mapping.** PE = 128 ST-BIF neurons, each on a 16-input adder tree, 1024 adds/cycle; three SRAMs (weight, membrane, spike tracer); negative spikes handled by two's-complementing the weight row. ALU is **add, compare, shift** — no multiplier anywhere. Column-wise tiling across PEs so spikes broadcast and partitions do not overlap. Offline three-stage mapping: greedy traffic-sorted partition, Hilbert-curve placement + force-potential refinement, multi-path routing with GA-tuned transmission probabilities (peak link BW 17.9 → 11.9 GB/s on ResNet50).

**What it costs.** 6×6 cores, **100.23 mm² at 28 nm, 72 MB SRAM** — 22× ANT's area and **6.4× worse GOPS/mm²**. Membrane SRAM is 52% of it. eDRAM trades 43% of the area for 7× worse TOPS/W.

## 4. Results

| | |
|---|---|
| Baseline | **QANN:** ANT, Eyeriss/v2, S-CONV, AIOQAB, Sanger, ViTALiTy, AEC-CIM, LLH-CIM; Jetson Orin / A100 / TPUv4 / Groq. **SNN, elastic:** TrueNorth, Darwin3, MorphIC, PAICORE. **SNN, non-elastic:** Phi, SpinalFlow, SASAP, Prosperity, C-DNN |
| Models / datasets | VGG16 (CIFAR10/100, CIFAR10-DVS), ResNet18/34/50/101 + ViT-S (ImageNet), YOLOv2-ResNet34 (COCO2017, VOC2007). All 4-bit weights, T ≤ 32, converted by SpikeZIP-TF |
| Accuracy delta | **Zero, SNN vs QANN** (ResNet50 75.60% = 75.60%; same on three others). ANN → QANN costs 2.57 pts. Early termination: **−0.2% for 21.9% latency**, or **≈−3.4% for 30.6%** (ResNet50 loses 4.46 pts at that point) |
| Speedup | vs ANT **3.4×**; vs PAICORE **2.9×**; vs C-DNN 4.9×; vs ViTALiTy 2.8× @ 500 MHz. Pipeline alone 5.61-36.05× over no-pipeline, 2.2-2.8× over layer-wise. FCR: earliest **2.76×**, geomean 1.83× |
| Energy / area | **25.55 TOPS/W** (ResNet50) — 13.6× ANT, 22.1× PAICORE, 8.2× Groq, 144.4× Jetson Orin. ViT-S collapses to 5.10 (9× the SOP count). **100.23 mm², 41.26 GOPS/mm² — 6.4× worse than ANT.** NoC 20.5% traffic / 24.3% energy under TrueNorth. 0.030-0.038 pJ/SOP, flat from ResNet18 to ResNet101 |
| Technology node | 28 nm, 200-500 MHz, 0.9 V (measured at 200 MHz) |
| Evidence level | **Post-synthesis** (DC + VCS + PrimeTime PX), memory compiler for SRAM, DRAMSim3/HBM3.0, DSENT for NoC, and a **cycle-level simulator parameterised from synthesis** for end-to-end. **No silicon** — but TrueNorth, PAICORE, Darwin3, MorphIC, C-DNN, AEC-CIM and LLH-CIM are fabricated chips. Baselines that reported nothing were **estimated from peak** |
| **Is the comparison fair?** | **Not iso-area** (100.23 mm² vs ANT's 4.527; 6.4× worse GOPS/mm²); **not iso-model** (ELSA's ResNet50 is pruned — Tab. IV footnote, dropped in Tab. V); **not iso-evidence** (ELSA post-synthesis vs fabricated PAICORE/TrueNorth/C-DNN; absent baselines estimated from peak). Iso-node, iso-frequency, ~iso-accuracy. **Not to quote bare:** 3.4×/13.6×, 2.9×/22.1×, 144.4× (28 nm vs 8 nm) |

## 5. Comment

No quantization. For SNN.

## 6. Claude notes

*Suggestions from the reading agent. **Strip this section before copying into
`QuantArchSurvey/venues/ISCA/notes/`.***

- **Disposition, human 2026-09-14: `ELSA` and `Phi` will both be removed from the survey later.** So the loose ends below need no resolution and this note is not going to be published. Recorded for completeness only, in case that decision is revisited: (i) the **data-type cell still reads `TERNARY` `INT4` `MIXED`** rather than `—`, unlike Cambricon-SR's, because those widths are sourced in the paper's own text and `Phi` is the precedent for a `non-Q` entry keeping sourced format tags — if SNNs are cut, the cell is moot either way; (ii) **Generation was set to `—`** as a consequence of the `non-Q` ruling, following the `Phi` precedent, not because the paper resists `G2`; (iii) the `ARCH` → `ARCH+SYS` dispute below is left open and unresolved.

- **Read depth.** Full close read of §I-§IX and the artifact appendix. Figs. 6, 9, 18-22, 24-26 and Tabs. IV, V, IX are bitmaps and were read by rendering pp. 3-5, 9-12 to PNG. **Not rendered, prose only: Figs. 15, 16, 17, 23, 27, 28** — so §VII-C's 27.4× / 1.65× geomean attributions are taken on trust. **Biggest gap: SpikeZIP-TF was not read**, so the condition making ST-BIF ≡ quantized ReLU, and with it the **activation bitwidth**, is nowhere in this paper; my A4 is derived from Tab. III's memory ratio, not stated. Also unresolved: whether Tab. V's ELSA ResNet50 is the pruned model (numbers identical to Tab. IV's `ResNet50*`, footnote absent), and whether §VII-D's extra 16 MB eDRAM is added to ELSA or to the baselines. All itemised in `ANALYSIS.md`.
- **Two seed-tag disputes, both flagged not settled.** `ARCH` → **`ARCH+SYS`**: §VI is a titled section with two algorithms doing offline partition / placement / routing, named in the abstract — your own RaPiD `SYS` rule. Counter: no ISA, no user compiler, and the placement/routing algorithms are borrowed. `non-Q` → `Q-ORIENTED`: **SETTLED 2026-09-14 — the human ruled `non-Q`; the seed stands and the draft argument below did not carry.** It ran: swap the spike code for INT8 and the adder-tree PE, ST-BIF circuit, membrane buffer, spike tracer, BAER, the *mini-batch* half of Gustavson and elastic inference all die; only generic Gustavson survives, which the paper itself credits to ANN work. Counter: ELSA proposes no format and you ruled Phi `non-Q`. My distinction — Phi changes no precision at all; ELSA's whole efficiency argument *is* the 12 : 4 : 1 asymmetry.
- **SUPERSEDED 2026-09-14 — the human kept ELSA with Phi. Recorded because the distinction may still be worth a sentence in the survey.** Your `Phi` §5 line is the load-bearing one here. You wrote: *"May not count as a quantization paper, unless one views SNN as a special case of 1-bit quantization."* ELSA answers that conditional from inside the paper — it names four widths, says its net is *equivalent to a QANN*, and uses INT4 weights. **I would separate the two rather than keep them as "the two SNN papers".** Phi is sparsity-plus-codebook that happens to run on spikes; ELSA is legible in format terms end to end. `survey/README.md`'s "outside the taxonomy, different axis, low-precision story is spikes not quantized tensors" is right for Phi and wrong for ELSA.
- **The most valuable finding, and it is not in the abstract: the membrane is the escape hatch and it is half the chip.** 12-bit, SRAM, one word per neuron, **52.44% of core area but only 4.2% of power** — and that gap *is* the design: Gustavson-product is chosen to hold the access rate down because the area cannot be reduced. Pair the two Tab. III rows in the survey; it is the cleanest "the accumulator is the design" exhibit in the corpus, and the only one where the paper breaks the accumulator out by name.
- **Numbers I would exclude or footnote.** (i) **3.4×/13.6× vs ANT** and **2.9×/22.1× vs PAICORE** — table-row ratios at 22× the area on a **pruned** ResNet50 (Tab. IV footnote, dropped in Tab. V), ELSA post-synthesis vs a fabricated PAICORE. (ii) **"§VII-K4: 2.2×/2.3×/2.8×/2.5× over the no-pipeline baseline"** — Fig. 26 makes those ratios **over layer-wise**; over no-pipeline they are 5.61-36.05×, and the 2.8× is ResNet50-*pruned*. The next sentence then quotes 36.1× and 5.6×, which *are* no-pipeline — two baselines in two sentences. (iii) **"30.6% latency at <3.3% accuracy"** — 30.6% is a mean and the losses are 3.47/2.95/**4.46**/2.83, mean 3.43: not a bound. (iv) **"82% earlier first correct response"** (§I) is a property of SNNs from Fig. 1b, not an ELSA result. (v) **82.49 mW** is a nominal spec; the TOPS/W come from ≈0.31 mJ/frame.
- **The metric is an *equivalent* OPS, exactly like RingCNN's.** Tab. V footnote: `TOPS/W = #OP of network / Latency per frame`. Reproduces from Fig. 22 + Tab. II. So GOP/s is the **dense ANN's** op count over ELSA's frame time — on a pruned network it credits work that is not done. Same trap you caught on RingCNN's "equivalent 41 TOPS", without the word.
- **§5 material, if you want it.** `G2` on paradigm: it builds an architecture whose purpose is executing a particular low-precision arithmetic and designs no numeric type — the G2 test, second clause, passed cleanly. The interesting part is that a **2026 ISCA paper carries none of the three G3 threads** — no outliers, no weight-only bandwidth argument, no codebook, no LLM. **Generation is now `—`, following the Phi precedent — applied 2026-09-14 as the consequence of the `non-Q` ruling.** On placement (**not adopted** — ELSA stays outside with Phi): the case for filing it inside as a boundary case on the *activation-format* axis rested on one claim — *an SNN is a 4-bit QANN with the activation re-coded from binary-weighted to temporal unary; that buys MAC → ADD and 8-bit wires → 1-bit events, and costs a 12-bit membrane per neuron and a T-linear traffic bill.*
- **Cross-paper.** On **static-vs-dynamic** ELSA takes a position nobody else holds: runtime **per-input** precision (avg T = 6.2 of 32) against OLAccel design-time and DRQ runtime-per-region — with the caveat that the hardware doesn't choose T, the SNN's monotone convergence does. On **structural reformulation** (your RingCNN/SmartExchange/SingularBit axis) ELSA is the **temporal** member: RingCNN restructures the algebra, ELSA restructures *where the bits live*. And the nearest conventional neighbour is **bit-serial**, not another SNN — spikes are a unary temporally-serial code where bit-serial is binary-weighted temporally-serial, `O(2^b)` steps against `O(b)`, in exchange for addition-only arithmetic and event skipping. That comparison is mine; it is nowhere in the paper.
- **Two cross-entry data points worth harvesting.** ELSA's Tab. IV reports **`Phi` at 0.662 mm², 242.8 GOPS, 0.286 TOPS/W, 366.8 GOPS/mm², CF10@91.1** against ELSA's VGG16 column of 1982.9 / 20.89 / **19.78** / CF10@92.3 — i.e. ELSA claims ~73× the energy efficiency while Phi holds ~18.5× the area efficiency. **Second-hand**, ELSA's rendering of Phi, not checked against Phi's paper. And Tab. V is the corpus's **only same-node, near-same-accuracy QANN-vs-SNN measurement**: the SNN wins ~14× on energy per frame and loses ~6× on area efficiency. ANT itself has no directory in `survey/papers/`; it may be worth one.
- **`survey/TAGS.md` and `survey/README.md` changes, reported not applied.** ELSA's `Tags:` line is now `analytical-dtype` `mixed-precision` `accelerator` (was `accelerator` alone) — TAGS.md's counts and reverse index at §(2), §(5) and the matrix row for ELSA need the same edit. In `survey/README.md`: ELSA's status row 28 goes `brief ready` → `analysis ready`; and the "Papers the taxonomy has no box for" paragraph pairing ELSA with Phi should be split — I'd move ELSA out of the **unplaced** data-type row and, if you accept the framing, open a **temporal / unary activation code** position rather than force it into 1.1/1.2/1.3.
