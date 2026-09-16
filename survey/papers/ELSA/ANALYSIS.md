# ELSA — paper notes

**ELSA: An ELastic SNN Inference Architecture for Efficient Neuromorphic Computing**
Kang You, Chen Nie, Lee Jun Yan, Ziling Wei, Cheng Zou, Zekai Xu, Yu Feng, Honglan Jiang,
Zhezhi He (Shanghai Jiao Tong University; Shanghai AI Laboratory)
**ISCA 2026** (2026 ACM/IEEE 53rd Annual International Symposium on Computer Architecture),
pp. 2550–2566 ｜ DOI: **10.1109/ISCA66397.2026.00178**
Publication info verified 2026-09-02 from the **official ISCA 2026 proceedings package**
(title, authors, pages, DOI and abstract all read from its `assets/data/data.js`). The author
list in that metadata gives "Jun Yan Lee" and "Feng Yu"; the PDF's own byline reads
**"Lee Jun Yan"** and **"Yu Feng"** — the PDF is used above.
Archived here: **the published proceedings PDF** (`506501c550.pdf`, 17 pages) — not a preprint.

Status: **note ready** ｜ Last updated: 2026-09-14 ｜ **TO BE REMOVED FROM THE SURVEY** — the human ruled 2026-09-14 that the two SNN entries, `ELSA` and `Phi`, will both be dropped later; nothing here needs further resolution. ｜ **Human-checked 2026-09-14** — ruled `NON-Q-ORIENTED` (no quantization; an SNN paper), overriding this file's draft `Q-ORIENTED`. Generation set to `—`, following the Phi precedent.
Tags: `analytical-dtype` `mixed-precision` `accelerator`
How far it was read: **full close read of §I–§IX plus the artifact appendix (pp. 2550–2563).**
Read line by line: §I, §II-A (IF and ST-BIF dynamics, Eqs. 1–3), §II-B (MM-sc / MM-ss,
Tab. I), §III-A/B/C (all three motivations), §IV-A (PE microarchitecture, Figs. 8–10, the
per-spike three-step flow, tiling), §IV-B (router, BAER, Figs. 11–12), §V (spine- and
token-wise pipelines, Algorithm 1), §VI (partition / Hilbert mapping / multi-path routing,
Algorithm 2), §VII-A–§VII-K (every experiment), §VIII, §IX, Appendix A–F. **Figures 6, 9,
18–22, 24–26 and Tables IV, V, IX are raster images in the text extraction and were read by
rendering pp. 3, 4, 5, 9, 10, 11, 12 to PNG at 200–400 dpi** (`pdftoppm`); values read that
way are marked *(read off Fig. N)*.

**Skimmed, and not resolved — itemised because it is load-bearing:**

1. **Figs. 16 and 17** (per-benchmark energy / latency / AEDP versus SNN and QANN
   accelerators, normalised to Eyeriss) were **not rendered**; only the prose summary is used.
   The two "geomean" attributions in §VII-C — 27.4× energy from the dataflow, 1.65× speedup
   from the pipeline — come from Fig. 16 and are **not independently checked**.
2. **Fig. 15** (per-benchmark energy breakdown, W1–W7) is used only via the percentages the
   text extractor recovered; **not rendered**.
3. **Figs. 23, 27, 28** read from prose only; per-point values not transcribed.
4. **SpikeZIP-TF [4] was not read.** The condition under which the ST-BIF neuron is
   "mathematically equivalent to quantized ReLU" lives there, not here — so the **activation
   bitwidth of the source QANN is never stated in this paper** and is inferred below from
   Table III's memory sizing. This is the largest single gap; see
   `Limitations and open questions`.
5. Two ambiguities left open: whether the extra **16 MB eDRAM (4.76 mm²)** in §VII-D is added
   to ELSA or to the QANN baselines, and whether Table V's ELSA `ResNet50` column is the same
   **pruned** model Table IV marks with `*` (the numbers are byte-identical, so almost
   certainly yes, but Table V carries no such footnote).

> The PDF is **not committed** (3.2 MB). It came from the proceedings package a human
> supplied, now archived at [`archieve/ISCA 2026.zip`](../../../archieve/), entry `pdfs/5065-3nexm57sBmVa6MJtFTiSrb/506501c550/506501c550.pdf`.
> **There is no public URL for it** — this is not an arXiv paper. Re-extract with
> `python3 extract.py` → `extracted/` (committed, greppable).
> Authors release code and a simulator at https://github.com/Intelligent-Computing-Research-Group/ELSA
> and https://zenodo.org/records/19449728 (Appendix C/D). **Neither was consulted** — this is a
> paper-only read, so the status is `analysis ready`, not `thorough ready`.
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, 2026 row.

---

## What the close read changed in the brief

**One substantive reversal and three corrections.** (1) The brief's headline con — *"No
quantization contribution"* — is **half wrong, and the half that is wrong is the important
half**. ELSA proposes no numeric *format*, which is true; but it states an explicit bitwidth
for four separate tensor classes (**weights 4-bit, spikes 1-bit + 1-bit sign, membrane
12-bit, spike tracer 4-bit inferred**), its efficiency argument is entirely *about* those
widths, and its network is an **exactly equivalent re-encoding of a 4-bit-weight QANN** with
byte-identical accuracy (Tab. VII). The right statement is "contributes no format, but is
fully legible in format terms" — not "no quantization content". (2) The abstract's **3.4× /
13.6× over ANT** are **Table V ratios of GOP/s and TOPS/W at 22× ANT's area**, and ELSA's
ResNet50 is marked *"after prune"* in Tab. IV — a footnote that **disappears in Tab. V**,
where the ANT comparison is actually made. (3) The **82% earlier first correct response** in
§I is a property of SNNs generally (Fig. 1b), **not an ELSA result**; ELSA's own elastic
numbers are 2.76× earliest-FCR and 1.83× geomean at the sweet point on COCO2017. (4) The
brief's "near-SRAM dataflow" is better said as **everything resident on chip** — 72 MB of
SRAM, DRAM touched only for the network's input.

---

## Brief

### 1. Motivation

SNNs have a property nobody exploits: **elastic inference** — outputs emerge progressively,
so salient inputs can be answered long before full evaluation, with the first correct
response arriving up to **82% earlier** than the stable-state output. That matters for real-
time tasks like autonomous driving. But existing SNN accelerators forfeit it: layer-by-layer
designs emit nothing until all layers finish, and time-step-by-time-step designs use coarse
layer-wise pipelines that synchronize every spine/token in a layer.

### 2. Overview

A near-SRAM dataflow architecture realising true elastic inference through a **fine-grained
spine/token-wise pipeline** that forwards each spine or token the moment it is produced,
forming a continuous stream. Supported by a **bundled address-event-representation
protocol** to cut NoC traffic and a mini-batch spiking Gustavson-product dataflow to reduce
memory access and exploit sparsity.

### 3. Pros and cons

**Pros**

- Identifies and then delivers a latency metric the field had been leaving on the table —
first-correct-response latency, not just throughput.
- Beats both neighbours: for 4-bit ResNet-50, 3.4×/13.6× speedup and energy efficiency over
the SOTA **quantized-ANN** accelerator (ANT), and 2.9×/22.1× over the SOTA SNN
accelerator.
- Attributes gains to their sources — 27.4× geomean energy saving from the dataflow, 1.65×
geomean speedup from the fine-grained pipeline — rather than reporting one lump number.

**Cons**

- **No quantization contribution.** The source list's own note is about its address-event
protocol lowering communication traffic; it is in this corpus as an SNN architecture, not
a data-type or precision paper. *(Corrected above — see `What the close read changed`.)*
- The elastic-inference benefit presumes an application that can act on an early,
provisional answer — a real constraint the paper illustrates but does not bound.
- Comparing SNNs against quantized ANNs requires accepting an accuracy-parity claim across
two model families, which is a heavier assumption than a same-family comparison.
*(The paper's answer is stronger than the brief assumed: the conversion is exact and the
accuracies are byte-identical, Tab. VII — but the QANN itself is never characterised.)*

### 4. Where it applies

Outside the taxonomy, alongside [`Phi`](../Phi/ANALYSIS.md), as the corpus's two **spiking-
neural-network** entries. Its ANT comparison is the one place the survey can see quantized-
ANN and SNN hardware measured on the same benchmark. *(This placement is challenged in
`Relation to other entries` — the close read argues ELSA and Phi do **not** belong in one
box, and that ELSA is inside the survey's reach.)*

---

## Conclusions

**An SNN in this paper is a quantized ANN with the activation re-coded from binary-weighted
into temporal unary, and ELSA says so out loud.** §II-A2 **verified**: *"The ST-BIF neuron can
be mathematically equivalent to quantized ReLU under specific conditions [4]"* (p. 2551).
§VII-F **verified**: *"Since the SNN, comprised of ST-BIF neurons, is equivalent to QANN
(Sec. II-A2), the accuracies of QANNs and SNNs in ELSA are identical"* (p. 2559) — and
Tab. VII bears it out to the decimal on four models. §VII-A2 **verified**: *"all SNNs in
Tab. II use 4-bit quantized weights"* (p. 2556). So the network ELSA runs is a
**4-bit-weight quantized network whose activations have been unrolled from a binary-weighted
integer into a train of ternary events over up to 32 time-steps**. That is a change of
*format*, not of *model*, and it is what makes ELSA legible to this survey at all.

**The escape hatch is the membrane potential, and it costs half the die.** §III-C
**verified**: *"membranes have a much larger bitwidth (12-bit) than weights (4-bit) or spikes
(1-bit)"* (p. 2553). Tab. III **verified**: membrane memory is **4 × 307.2 KB per neural core
= 1.460 mm², 52.44% of a neural core's area** — and PEs are 93.03% of the chip, so **roughly
half of ELSA's 100.23 mm² is 12-bit membrane SRAM**. The paper concedes the consequence
twice: elastic SNN accelerators *"generally show lower area efficiency than non-elastic
accelerators … as all weights and membrane states are stored on-chip"* (§VII-C), and C-DNN's
near-parity in TOPS/W is because it *"avoids SRAM storage for membrane states"* (§VII-C).
**Every 1-bit activation on the wire is paid for with 16 bits of persistent per-neuron state
(12-bit membrane + 4-bit tracer).** That is the effective-bitwidth accounting the survey
should record, and the paper never assembles it.

**The dataflow choice exists to make the escape hatch cheap in energy while leaving it
expensive in area.** Gustavson-product is chosen precisely because the membrane is the wide
operand: it is membrane-stationary, so each membrane row is read and written **once**
(§III-C). The result is that membrane SRAM is **52.44% of area but only 4.2% of power**
(Tab. III), while the weight buffer is 17.49% of area and **31.2%** of power. Read the two
rows together and the thesis is visible: *the wide tensor is made stationary, the narrow
tensor is made to move.* Fig. 23 is the ablation — inner-product spends 76.2% of energy in
the weight buffer, outer-product 70.3% in the membrane buffer, Gustavson 43.1% combined:
**2.7× over inner-product, 1.9× over outer-product**.

**Time-steps are the precision knob, and ELSA turns it per input.** Elastic inference is
implemented as **confidence-based early termination** (§VII-A5): max class probability for
classification, YOLO objectness for detection, terminate once the score crosses a threshold.
Tab. VII quantifies it — **21.9% mean latency reduction for <0.2% accuracy loss**, and a
second operating point at **30.6% for ≈3.4%** (the paper writes "<3.3%"; see hazards).
Fig. 21 marks **Avg T = 6.2** for ResNet50 at confidence 0.55 against Tab. II's allowed
maximum of 32. So the length of the unary activation code is chosen **at run time, per
input**, by a confidence controller. In this corpus that is a **new position on the
static-versus-dynamic axis**: OLAccel design-time, DRQ runtime per-region, ELSA runtime
**per-input**. But be precise about what the hardware contributes: **the SNN supplies the
monotone precision ladder for free; ELSA's pipeline only lets you cash it in sooner.** No
hardware in ELSA decides T.

**BAER is an admission of what the temporal code costs on the wire.** A 1-bit spike needs a
25-bit AER packet under TrueNorth's protocol; BAER amortises the row address over 17 spikes,
425 bits → **256 bits**, ≈15 bits per spike (Fig. 12). Fig. 6 is the honest framing and it is
in the paper's own motivation: on ResNet-18/34 and ViT-Small, TrueNorth's NoC traffic
**crosses Eyeriss's at about two time-steps and reaches 3.4× / 3.5× / ~7× by T = 8**, growing
essentially linearly in T. BAER removes 19.1% of that versus TrueNorth (§VII-K3). So the
protocol narrows the gap; it does not close it. **An SNN's communication bill is T-linear,
and that is the price of the format.** The paper states the problem and never states the
residual.

---

## Method

**The neuron (§II-A2, Fig. 9) — verified.** ST-BIF, three steps per incoming spike:
integrate `V̂ₜ = Vₜ₋₁ + Σᵢ xᵢ,ₜ·wᵢ` (Eq. 1); fire `yₜ = Θ(V̂ₜ, V_thr, Sₜ) ∈ {−1, 0, +1}` with
`+1` iff `V̂ₜ ≥ V_thr ∧ Sₜ < S_max` and `−1` iff `V̂ₜ < 0 ∧ Sₜ > S_min` (Eq. 2); update by
**soft reset** `Vₜ = V̂ₜ − yₜ·V_thr` and `Sₜ = Sₜ₋₁ + Θ(...)` (Eq. 3). The **spike tracer `S`
is the running count of net emitted spikes** — i.e. it holds the quantized activation value
as it converges. Fig. 9's schematic labels the reset constant **`2^N`** and the update mux
inputs `{−2^N, +2^N, 0}` *(read off Fig. 9)*, so `V_thr` appears **constrained to a power of
two** in hardware; the prose only ever writes `V_thr`. Consistent with Tab. IV/V listing
ELSA's ALU as **"8-b Add, Cmp, Shift"** — the only multiplier-shaped thing on the chip is a
shift.

**The PE (§IV-A, Fig. 8b) — verified.** 128 ST-BIF neuron circuits, each fed by a **16-input
adder tree**; **1024 additions/cycle per PE**. Three SRAMs per PE: an *N*-way weight buffer,
a membrane buffer, a spike-tracer buffer. A spike arrives as `(x, yᵢ, qᵢ)` — row address,
column ID, polarity; the weight buffer reads row `yᵢ`, the adder tree accumulates it into
membrane row `x`, negating via **two's complement** when `qᵢ = 1`. Tiling is **column-wise**
across PEs (Fig. 10d) rather than block-wise, so spikes broadcast and the weight/membrane
partitions do not overlap.

**Mini-batch spiking Gustavson-product (§III-C, §IV-A2) — verified.** Gustavson (row-wise
product, cited to Gamma [22]) minimises membrane access because each output row is read and
written once. It normally needs row-aligned input, which asynchronous spikes destroy. ELSA
does **not** add synchronisation (that would break the pipeline); instead BAER's row-bundling
*supplies* the alignment — every BAER flit carries spikes sharing one row address `x`, so one
flit is one mini-batch: one membrane read, *N* parallel weight-row accumulations, one
write-back. **The protocol and the dataflow are one design decision seen from two ends.**

**Spine/token-wise pipeline (§III-A, §V) — verified.** Fig. 4 defines a **spine** as
`Z^{1×1×C}` (one spatial position across all channels) in a CNN and a **token** as `Z^{1×D}`
in a transformer. Prior TBT accelerators advance a layer only after all *N* spines/tokens
finish; ELSA forwards each on production, cutting first-response latency from **O(L×N) to
O(L)** — for Spikformer with L = 74, N = 197 that is the dominant term. For CNNs the output
scheduler (Alg. 1) emits spines **right-to-left / bottom-to-top** so the next layer's first
spine becomes computable as early as possible; spines depending on padding are deferred to
the end. For transformers, dependence is within a token, except that **ssoftmax stalls the
pipeline** waiting for all query and key tokens.

**Bundled AER (§IV-B3, Fig. 12) — verified.** Traditional AER: 17 spikes × 25 bits (12-bit
spine/token ID + 12-bit position + 1-bit sign) = 425 bits. BAER: one 256-bit flit — 6-bit
router destination (hop counts *m*,*n*), 2-bit type (begin/body/end), **one** 12-bit
spine/token ID, then 17 × (12-bit position + 1-bit sign), plus a 15-bit ECC field. Short
tails are zero-padded.

**Router (§IV-B, Fig. 11) — verified.** Five contention-free data paths; one SNN layer per
router. Carries an **SSoftmax Unit** and an **SLayerNorm Unit** (integer-only softmax and
layernorm inherited from SwiftTron [24], each with its own ST-BIF circuits and state
memories — together **6.72% of ELSA's area**) and an **im2col unit** doing convolution
broadcast at the router. MM-ss (spiking attention) is realised as two MM-sc by treating
spike tracers as continuous operands, following SpikeZIP-TF.

**Mapping (§VI) — verified.** Three offline stages. **Partition**: Alg. 2, greedy — sort
inter-layer traffic `cᵢⱼ` descending, fuse layer pairs while memory and neuron-count budgets
hold; layer-wise partition preferred so intra-layer broadcast and reduction stay inside a
core. **Mapping**: Hilbert-curve placement from [26], refined by greedy force-potential
minimisation. **Routing**: two alternative paths beyond the shortest, with transmission
probabilities tuned by a **genetic algorithm** to flatten link load.

**Chip (Tab. III) — verified.** 6×6 mesh of neural cores; each core = 4 PEs + 1 router. Per
core: weight memory 4×102.4 KB, membrane memory 4×307.2 KB, spike-tracer memory 4×102.4 KB →
**72 MB total on-chip**. 100.23 mm², 82.49 mW nominal, 28 nm, 200–500 MHz. PEs 93.03% of
area / 91.8% of power; routers 6.97% / 8.2%.

---

## Key numbers, with their frame

**Evidence level.** RTL in Synopsys Design Compiler, **commercial 28 nm**, post-synthesis;
VCS post-synthesis simulation for toggle rates; **PrimeTime PX** for energy; a commercial
memory compiler for SRAM; **DRAMSim3 + HBM3.0** for off-chip; **DSENT** for NoC; and a
**cycle-level simulator parameterised from the synthesis results** for end-to-end numbers.
**No silicon.** §VII-A4 **verified**: baseline metrics *"reported in the original papers"* are
used directly, and where absent are *"estimate[d] … using the reported peak throughput and
peak energy efficiency"* — so several baselines are **peak-derived**, and TrueNorth, PAICORE,
Darwin3, MorphIC, C-DNN, AEC-CIM and LLH-CIM are **fabricated chips** measured against ELSA's
post-synthesis model. **Do not pool these.**

**How the throughput metric is defined.** Tab. V footnote ** **verified**: *"1 MAC = 2 OP,
#time-step Sop = 2 OP, TOPS/W = #OP of network / Latency per frame"*. Cross-checking against
Fig. 22 (ResNet50 on ELSA: 2.0 ms, 0.31 mJ) and Tab. II (ResNet50 #Ops = 8.18 G) reproduces
4135 GOP/s and 26.4 TOPS/W. So **GOP/s and TOPS/W are the *dense ANN's* operation count
divided by ELSA's per-frame latency / energy** — an *equivalent*-OPS metric, not a count of
work ELSA performs. **Inferred / not verified** (arithmetic reproduction, not a stated
derivation).

| Setting | Model | Metric | Baseline | Result | Source |
|---|---|---|---|---|---|
| **Headline vs QANN** | ResNet50, ImageNet, 4-bit weights | throughput / energy efficiency | **ANT** (MICRO'22), 28 nm, 200 MHz, 4.527 mm², IN@75.08 | **3.4× / 13.6×** (4135.42 vs 1210.06 GOP/s; 25.55 vs 1.880 TOPS/W) | Abstract, Tab. V **verified** — ratios of table rows, at **22.1× ANT's area** |
| **Headline vs SNN** | ResNet50, ImageNet | throughput / energy efficiency | **PAICORE** (JSSC'25), 28 nm, 537.98 mm², *4-bit synaptic weight* | **2.9× / 22.1×** (4135.4 vs 1421.6 GOP/s; 25.55 vs 1.156 TOPS/W) | Abstract, Tab. IV **verified**. PAICORE is **fabricated silicon** |
| **The pruning footnote** | ResNet50 | — | — | Tab. IV's ELSA column reads **`ResNet50*`**, footnote **`*: after prune`**. Tab. V repeats the identical 4135.42 / 25.55 / IN@75.6 **with no such footnote** | Tab. IV + V, p. 2558 **verified** *(read off rendered page)* |
| **Area efficiency** | ResNet50 | GOPS/mm² | ANT 264.78 · S-CONV 275.81 · Prosperity 737.4 | **ELSA 41.26 — 6.4× worse than ANT** | Tab. IV, V **verified**. Conceded in §VII-C |
| **Where the die goes** | — | area share | — | **membrane memory 52.44%** of a neural core; weight memory 17.49%; spike-tracer memory 17.49%; adder tree 5.02%; router 6.97% | Tab. III **verified** |
| **Where the power goes** | — | power share | — | **adder tree 52.0%**, weight memory 31.2%, **membrane memory 4.2%** | Tab. III **verified** |
| **Bitwidths** | — | per tensor class | — | membrane **12-bit**, weights **4-bit**, spikes **1-bit** (+1-bit sign) | §III-C, p. 2553 **verified** |
| **Spike-tracer width** | — | bits | — | **4-bit** — derived from Tab. III: membrane 307.2 KB ÷ tracer 102.4 KB = 3 at equal entry counts, and the membrane is 12-bit. Implies the equivalent QANN activation has ≤16 levels, i.e. **A4** | **inferred / not verified** |
| **Accuracy chain** | ResNet50, ImageNet | top-1 | ANN 78.17% | QANN **75.60%** (−2.57) = SNN **75.60%** (−0.00) | Tab. VII **verified**. Same pattern on ResNet18/34 and ViT-S |
| **Elastic inference, safe point** | 4 models, ImageNet | latency reduction @ accuracy cost | SNN at full T | **21.9% mean @ <0.2%** | Tab. VII, §VII-F **verified** |
| **Elastic inference, aggressive** | 4 models | " | " | **30.6% mean @ ≈3.4% mean** (per model 3.47 / 2.95 / **4.46** / 2.83 points) — the paper writes *"<3.3%"* | Tab. VII **verified**; the *"<3.3%"* bound is **contradicted by its own table** |
| **Time-steps actually run** | ResNet50, conf. 0.55 | average T | Tab. II allowed max **T = 32** | **Avg T = 6.2** | Fig. 21 *(read off p. 2560)*. Definition not given in prose — **inferred / not verified** |
| **First-correct-response** | YOLOv2 / COCO2017, conf. 0.2 | latency | full inference **3.30 ms** | geomean FCR **1.80 ms** (1.83×); **earliest 1.19 ms (2.76×)**; match rate 94.9% | §VII-F, Fig. 18 **verified** |
| **Pipeline vs no-pipeline** | RN18 / RN34 / RN50 / RN50-prune / ViT-S | speedup | no pipeline | **5.61× / 8.60× / 9.03× / 10.63× / 36.05×** | Fig. 26 *(read off p. 2561)* |
| **Pipeline vs layer-wise** | same | speedup | layer-wise pipeline | **2.2× / 2.3× / 2.2× / 2.8× / 2.5×** — §VII-K4's prose calls these *"over the no-pipeline baseline"*, which Fig. 26 contradicts | §VII-K4 vs Fig. 26 — **the prose is wrong**, see hazards |
| **Pipeline, iso-accuracy** | ResNet50 / ViT-S | latency to converged accuracy | layer-wise / no-pipeline | RN50 **1.95 / 4.2 / 14.9 ms**; ViT-S **3.9 / 6.7 / 97.6 ms** | Fig. 20 *(read off p. 2560)*. §VII-I's "2.4× / 2.0×" do **not** reproduce from these (2.15× / 1.72×) |
| **Technique ablation** | ResNet50 energy / latency | — | Eyeriss 10.68 mJ / 203.2 ms | baseline 1.17 / 72.5 → +Gustavson 0.38 / 14.7 → +pipeline 0.33 / 2.2 → +BAER **0.31 mJ / 2.0 ms** | Fig. 22 *(read off p. 2560)*, §VII-K1 **verified** |
| **Technique ablation** | ViT-S energy / latency | — | Eyeriss 8.3 mJ / 210.5 ms | 4.1 / 115.7 → 2.5 / 100.5 → 2.0 / 6.6 → **1.8 mJ / 3.9 ms** | Fig. 22 *(read off p. 2560)* |
| **Dataflow ablation** | RN34 / RN50 / ViT-S | energy | inner-product / outer-product | Gustavson **2.7× / 1.9×** better. Buffer-energy share: IP 76.2% weight, OP 70.3% membrane, GP 43.1% combined | §VII-K2, Fig. 23 **verified** |
| **NoC traffic** | RN18 / RN34 / RN50 / ViT-S | MB | TrueNorth 12.9 / 26.7 / 72.3 / 701.6 | ELSA **11.2 / 21.0 / 52.6 / 560.3** — **20.5% traffic, 24.3% energy** mean reduction | Tab. VIII, §VII-H **verified**. Iso-NoC: same 6×6 mesh, bandwidth, flit buffer |
| **What the temporal code costs on the wire** | RN18 / RN34 / ViT-S | SNN NoC traffic ÷ Eyeriss | Eyeriss (INT8 ANN) = 1 | **3.4× / 3.5× / ~7× at T = 8**, ≈linear in T; text says *"up to 8×"* | Fig. 6 *(read off p. 2552)* **verified**. Extrapolation to the T these benchmarks run is **inferred / not verified** |
| **BAER alone** | 64-bit flit | traffic reduction | TrueNorth / MorphIC | **19.1% / 36.7%** | §VII-K3, Fig. 25 **verified** |
| **Spike sparsity** | RN18 / RN34 / ViT-S | activation sparsity | — | **92.75% / 94.00% / 80.52%** (statistics from SpikeZIP-TF) | Fig. 6 **verified**. §I's "98%" is cited to [6], **not measured here** |
| **Work actually done** | ResNet50 / ViT-S | #Sop vs #Op | — | RN50 **10.04 G Sop / 8.18 G Op** (1.23×); ViT-S **90.74 G Sop / 8.50 G Op (10.7×)** — why ViT-S collapses to 5.10 TOPS/W | Tab. II, §VII-D **verified** |
| **Memory technology** | RN18/34/50/ViT-S | TOPS/W, allocated area | SRAM | eDRAM **5.97 / 5.32 / 3.64 / 2.61** TOPS/W (vs 29.96 / 27.12 / 25.55 / 5.10) at **9.78 / 17.12 / 29.34 / 48.70 mm²** (vs 16.69 / 29.73 / 51.83 / 79.53) | Tab. IX **verified** |
| **Scaling** | RN18 → RN101 | pJ/SOP, GSOPS/mm², FCR speedup | — | **0.030–0.038 pJ/SOP**, 80.6–98.9 GOPS/mm², **1.84–1.94×** | §VII-K7, Tab. X **verified** |
| **Communication share** | RN18 → RN101 | energy | — | compute **93.5% → 89.3%**; communication **2.99% → 8.05%**; pipeline-support logic **<4%, flat** | Tab. X **verified** |
| **vs large chips** | ResNet50, IN@75.6 | TOPS/W | Jetson Orin 0.177 (8 nm) / A100 1.560 (7 nm) / TPUv4 1.432 (7 nm) / Groq 3.125 (14 nm) | ELSA **25.55** — 144.4× Orin, 8.2× Groq. **Not iso-node**, and §VII-E says so | Tab. VI **verified** |
| **Second-hand: `Phi` in this corpus** | VGG16 / CIFAR10 | — | — | ELSA reports [`Phi`](../Phi/ANALYSIS.md) at 28 nm, 0.662 mm², **242.8 GOPS, 0.286 TOPS/W, 366.8 GOPS/mm², CF10@91.1**; ELSA's own VGG16 column is 1982.9 / 20.89 / **19.78** / CF10@92.3 | Tab. IV **verified as ELSA's rendering** — **second-hand**, not checked against Phi's paper. Phi is **18.5× better in GOPS/mm²** |
| Node | — | — | — | **28 nm**, 200–500 MHz, 0.9 V | §VII-A1, Tab. V **verified** |

---

## Cost and requirements

| | |
|---|---|
| **Formats, per tensor class** | Weights **INT4** (§VII-A2). Spikes **ternary {−1,0,+1}**, carried as a position plus a **1-bit sign**, 2 bits inside the fire component *(read off Fig. 9)*. Membrane **12-bit** fixed. Spike tracer **4-bit** (**inferred** from Tab. III). Accumulation into the membrane is the only arithmetic on the chip |
| **Granularity** | **None, in the scaling sense** — no scale factors, no groups, no per-channel or per-tensor scales anywhere in the paper. `V_thr` is the only per-layer constant, and Fig. 9 draws it as `2^N`. Worth stating positively: **the format carries no metadata at all**, which is why BAER's overhead is addresses rather than exponents |
| **Accumulator** | **The membrane, 12-bit — and it is not a register, it is SRAM.** One 12-bit word per neuron per layer, all resident: 4 × 307.2 KB per core, **52.44% of core area**. The corpus's most expensive accumulator by a wide margin. Gustavson-product exists to hold its *access rate* down (4.2% of power); its *area* cannot be reduced, only traded to eDRAM (Tab. IX: −43% area, −7× TOPS/W) |
| **Outliers** | **None.** The word does not appear in the paper. No outlier path, no second datapath, no metadata. Dynamic range is handled by the 12-bit membrane and by the `S_max`/`S_min` clamp in Eq. 2 — i.e. by **saturation** |
| **The escape hatch** | Three. (i) **12-bit membrane + 4-bit tracer = 16 bits of persistent state per neuron** — the real cost of a "1-bit" activation. (ii) **ssoftmax and slayernorm** in integer-only units inherited from SwiftTron [24], width unstated, **6.72% of chip area**. (iii) **T itself** — the activation is 1 bit *per time-step*, and there are up to 32 of them |
| **Retraining** | **Neither PTQ nor QAT — conversion.** SNNs are *converted* from CNN/transformer checkpoints "following SpikeZIP-TF [4]" (§VII-A2); §VII-E calls it a *"lossless conversion algorithm"* and Tab. VII shows byte-identical QANN and SNN accuracy. **But the quantization step is entirely upstream and uncharacterised** — how the 4-bit QANN was obtained, and at what activation width, is never said. ViT-S is the exception: Tab. V footnote, *"ViT-S on ELSA is trained by ourselves"* |
| **Time-steps** | Tab. II: allowed maximum **T = 32** on every benchmark; reported latencies are taken "after the accuracy converges". At run time, early termination cuts this to **Avg T = 6.2** on ResNet50 at confidence 0.55 |
| **Everything on-chip** | **72 MB SRAM**; weights and all neuron state resident. §VII-B: *"the off-chip DRAM access is negligible, as only the inputs of SNN are loaded from DRAM."* This is why the chip is 100.23 mm² and why its area efficiency loses to every non-elastic design in Tab. IV |
| **Software** | A three-stage offline **mapping toolchain** (§VI): greedy partition (Alg. 2), Hilbert-curve placement [26] + force-potential refinement, multi-path routing with GA-tuned probabilities. Plus the per-layer **Output Scheduler** control algorithm (Alg. 1). Released as `ELSA_Algorithm` (PyTorch) and `ELSA_Simulator` (Appendix C/D). **No ISA** |
| **Applicability** | Needs a task whose answer can be acted on while still provisional, and a **confidence signal** — max class probability or detector objectness. Autonomous driving is illustrated; when a provisional answer is safe is never bounded |

---

## Limitations and open questions

**Admitted.**
- Elastic SNN accelerators have **lower area efficiency** than non-elastic ones because all
  weights and membrane states sit on chip (§VII-C).
- **Darwin3 beats ELSA on precision flexibility** — 1/2/4/8/16-bit versus ELSA's fixed
  arrangement (§VII-C, **verified**). The paper's own statement that its format is rigid.
- The gain over **C-DNN is marginal** (24.53 → 25.55 TOPS/W) because C-DNN, being LBL, does
  not store membranes at all (§VII-C).
- **ViT-S is the bad case**: 9.0× more SOPs than the ANN op count, so both GOPS and TOPS/W
  fall, and ELSA's AEDP is **worse than ViTALiTy's** (§VII-D).
- The pipeline **stalls at ssoftmax** waiting for all query and key tokens (§V-B).
- Above an injection rate of 0.04 (10× practical) the NoC congests (§VII-J).

**Unadmitted.**
1. **The pruning footnote is dropped where it matters.** `ResNet50*` / *"after prune"* appears
   in Tab. IV; Tab. V, which carries the ANT comparison and the abstract's 3.4× / 13.6×,
   repeats the identical numbers without it.
2. **The throughput metric is an *equivalent* OPS** — the dense ANN's operation count over
   ELSA's frame latency. On a pruned network it credits work that is not done. Same
   construction as `RingCNN`'s "equivalent 41 TOPS", without the word "equivalent".
3. **The activation bitwidth of the source QANN is never stated.** "4-bit ResNet-50" in the
   abstract refers, in the body, only to **weights**. The equivalent activation precision is
   set by `S_max − S_min` and by T, and neither is given.
4. **The residual NoC gap versus a QANN is never closed.** Fig. 6 opens with SNN traffic at
   3.4–7× Eyeriss's at T = 8; BAER removes ~19%; Tab. VIII then compares only against other
   SNNs. **Inferred / not verified**: at the T these benchmarks actually run, ELSA's NoC still
   moves roughly an order of magnitude more bytes than an INT8 ANN accelerator would.
5. **Elastic inference is claimed at spine/token granularity and demonstrated at network
   granularity.** §VII-I: *"Each token and spine can exit independently once confidence is
   high."* No per-token confidence mechanism is described anywhere; §VII-A5's early
   termination is a single whole-output confidence test. **Not resolved.**
6. **No area or energy is attributed to the confidence controller** — the softmax, the
   comparison, the threshold. It does not appear in Tab. III.
7. **Fig. 9's `2^N` threshold is never discussed.** If `V_thr` really is constrained to a
   power of two, that is a quantization constraint on the converted model and belongs in the
   text. **Not resolved.**

**Citation hazards** (all **verified** unless marked):

- **"3.4× / 13.6× over ANT"** — a ratio of two table rows at **22.1× the area**, on a
  possibly-pruned ResNet50, ELSA post-synthesis against ANT's published numbers.
- **"2.9× / 22.1× over PAICORE"** — same possibly-pruned model; PAICORE is a **fabricated
  chip**.
- **"§VII-K4: speedups of 2.2×, 2.3×, 2.8× and 2.5× over the no-pipeline baseline"** — Fig. 26
  makes these ratios **over the layer-wise pipeline**; over no-pipeline the values are
  5.61× / 8.60× / 9.03× / 10.63× / 36.05×. The **2.8× is ResNet50-*pruned***; plain ResNet50
  gives 2.16×. The very next sentence quotes 36.1× and 5.6×, which *are* the no-pipeline
  ratios — so the paragraph uses two baselines in two consecutive sentences.
- **"30.6% latency reduction with mild accuracy degradation (<3.3%)"** — 30.6% is the **mean**
  of 31.0 / 39.1 / 19.3 / 33.1, and the accuracy losses are 3.47 / 2.95 / **4.46** / 2.83
  points, mean 3.43. **`<3.3%` is neither a bound nor the mean.**
- **"§VII-I: 2.0× earlier on ViT-S and 2.4× on ResNet50"** — Fig. 20's marked latencies give
  **1.72× and 2.15×** against layer-wise. The derivation is not shown. **Not resolved.**
- **"up to 82% earlier first correct response"** (§I) — a **property of SNNs** from Fig. 1b,
  not an ELSA measurement. ELSA's own figures are 2.76× earliest / 1.83× geomean.
- **"144.4× over Jetson Orin", "8.2× over Groq"** — 28 nm against 8 nm and 14 nm; conceded in
  §VII-E, but the numbers travel without the concession.
- **"82.49 mW"** (Tab. III) — a nominal spec. The TOPS/W figures derive from per-frame energy
  (≈0.31 mJ on ResNet50, Fig. 22), not from this; 4135 GOP/s ÷ 82.49 mW would give
  ~50 TOPS/W, twice the reported value.
- **"98% activation sparsity"** (§I) — cited to [6]. The sparsities ELSA actually uses are
  **80.52–94.00%**, from SpikeZIP-TF.
- **Baselines that did not report a metric were "estimated using the reported peak throughput
  and peak energy efficiency"** (§VII-A4). Which baselines those are is never listed.

---

## Relation to other entries

**ELSA and [`Phi`](../Phi/ANALYSIS.md) should not share a box, and the reason is precise.**
Phi's analysis concluded it *"contains no quantization to strip — activations are 1-bit going
in and 1-bit coming out, and L1 + L2 is exact"*, and the human's note on it says it *"may not
count as a quantization paper, unless one views SNN as a special case of 1-bit
quantization."* ELSA answers that conditional in the affirmative **from inside the paper**:
it names four tensor classes at four widths, states that its network is *equivalent to a
QANN*, uses **INT4** weights, and rests its whole efficiency argument on 1-bit-times-4-bit
addition against an 8-bit MAC. Phi is a **sparsity/codebook** paper that happens to run on
spikes; ELSA is a **dataflow and interconnect** paper whose every decision is dictated by a
precision asymmetry it states explicitly (12 : 4 : 1). Grouping them as "the two SNN papers"
files them by subject matter — the one axis this survey does not use.

**Where ELSA belongs on the axes already built:**

- **Substrate → scarcity → format.** The axis says *"each substrate makes a different resource
  scarce, and that scarcity, not the data distribution, selects the format"*: multiplier area
  in an ASIC, DRAM row locality in NDP ([`NDPLowBitFP`](../NDPLowBitFP/ANALYSIS.md)), ADC
  energy in ReRAM ([`RAELLA`](../RAELLA/ANALYSIS.md)). ELSA adds a clean fourth: **on-chip
  SRAM for per-neuron state is the scarce resource** (52% of the die), and that is what
  selects membrane-stationary Gustavson-product over inner- or outer-product. Fig. 23 is the
  axis in one figure.
- **Accumulator cost.** `Tender`'s 32-bit `Acc` bounds its band count; `TransitiveArray`
  splits a 12-bit PPE / 24-bit APE; `LUTTensorCore`'s headline density is measured
  **"No Psum"**. ELSA is the extreme: the accumulator is **12 bits × every neuron × resident
  in SRAM**, it is **more than half the chip**, and unlike the others it is *reported* —
  Tab. III breaks it out by name. The corpus's best citation for "the accumulator is the
  design".
- **Static versus dynamic precision.** OLAccel design-time, DRQ runtime **per-region**, most
  successors back to design-time. ELSA is runtime **per-input**: T chosen by a confidence
  controller, mean 6.2 of an allowed 32. No other entry has a per-input knob. The caveat that
  belongs with it: the *hardware* does not choose T; the SNN's monotone convergence supplies
  the ladder and ELSA only shortens the rungs.
- **Retraining.** The axis currently reads PTQ / QAT / *alternating structure-preserving
  retraining* (`SmartExchange`, `Phi`'s PAFT). ELSA occupies a fourth position: **exact
  conversion from an already-quantized checkpoint**, with the quantization pushed upstream
  into a cited algorithm and never characterised. Architecturally this is the strongest
  constraint of the four — ELSA can consume neither a stock FP checkpoint nor a stock INT8
  one; it needs a QANN of a particular shape.
- **Structural reformulation** (proposed on `RingCNN`, with `SmartExchange` and
  `SingularBit`). RingCNN leaves the number alone and changes the *algebra*; ELSA leaves the
  value alone and changes **where the bits live** — from parallel bit positions to serial time
  steps. Both are "the number is unchanged; the representation is restructured". If that axis
  is created, ELSA is its **temporal** member, and it makes the axis two-dimensional
  (algebraic / temporal) rather than a list.
- **Bit-serial.** The nearest *conventional* neighbour is not another SNN. A spike train over
  T time-steps is a **unary, temporally-serial** activation code; bit-serial designs use a
  **binary-weighted, temporally-serial** one. Same axis, different code, and the trade is
  legible: unary buys addition-only arithmetic and event-driven skipping at the cost of
  `O(2^b)` rather than `O(b)` steps. `BitFusion`'s spatial composition and
  `SamsungNPU`/`EVA`'s temporal composition are the other corners. **This framing is mine;
  it is nowhere in ELSA.**
- **The ANT datapoint.** ANT (MICRO'22) is `ALGO+ARCH` / `Q-ORIENTED` / `ADAPTIVE` / `G2` in
  `TAXONOMY.md`'s own worked-examples table but has **no directory in this corpus**. ELSA's
  Tab. V is the survey's only same-node, near-same-accuracy measurement of an SNN accelerator
  against a quantized-ANN accelerator, and the honest reading is: **the SNN wins on energy per
  frame by ~14× and loses on area efficiency by ~6×.**

---

## For the note

### §1 one-line summary

Runs a **4-bit-weight quantized ANN as an exactly equivalent spiking network** — the
activation re-coded from a binary-weighted integer into a **temporal unary train of ternary
{−1,0,+1} events over up to 32 time-steps**, so every MAC becomes a 4-bit add into a
**12-bit membrane potential that lives in SRAM, one word per neuron** — and then spends the
entire architecture on making that code cheap: a **spine/token-wise pipeline** forwarding one
output row the instant it exists (first response **O(L)** instead of **O(L×N)**), a **bundled
AER** flit amortising one 12-bit row address over 17 spikes (425 → 256 bits), and a
**mini-batch Gustavson product** keeping the wide membrane row stationary so it is read and
written once — buying **3.4× throughput and 13.6× energy efficiency over ANT** at 28 nm and
equal ImageNet accuracy, at **22× ANT's area** with **half the die being membrane SRAM**, and
turning the time-step count itself into a **per-input precision knob** (avg T = 6.2 of 32;
21.9% latency for <0.2% accuracy).

### Proposed values on their four axes

| Axis | Value | Evidence |
|---|---|---|
| **Level** | **`ARCH+SYS`** — *disagrees with the seed's `ARCH`* | §VI "SNN Mapping Optimization" is a titled section with **two algorithms** (greedy partition Alg. 2; Hilbert placement + force-potential refinement; multi-path routing with GA-tuned probabilities) plus Alg. 1's output scheduler, and the abstract names it: *"Combined with mapping and scheduling optimizations."* That is an offline compile/place/route pass that drives the hardware and is presented as a contribution — the human's own `SYS` test (RaPiD ruling, 2026-09-09). **Counter, so it can be flipped in one line:** no ISA, no user-facing compiler, and the placement and routing algorithms are largely borrowed ([26], Valiant's). My least confident call |
| **Q-oriented** | **`Q-ORIENTED`** — *disagrees with the seed's `non-Q`* | Apply the test literally. Swap the spike code for plain INT8 and: the adder-tree PE becomes a MAC array; the ST-BIF circuit, membrane buffer and spike tracer vanish; **BAER vanishes** (no events to bundle, and no address worth amortising when the value is 8 bits and dense); the *mini-batch* half of Gustavson vanishes (it exists only to restore row-alignment for asynchronous spikes); and **elastic inference vanishes**, taking the title with it. Only generic Gustavson survives — which the paper itself attributes to ANN work [22], [63]. **Counter, stated plainly:** ELSA proposes no format and inherits every width, and the human already ruled `Phi` non-Q. The distinction I would draw: Phi changes no precision at all, whereas ELSA's whole efficiency argument *is* the 12 : 4 : 1 asymmetry. Flag; do not settle silently |
| **Data type** | **`TERNARY` `INT4` `MIXED`** — *the seed is `—`* | `TERNARY`: §II-A2 **verified**, *"ST-BIF emits ternary spikes ({-1,0,1})"*. `INT4`: §VII-A2 **verified**, *"all SNNs in Tab. II use 4-bit quantized weights"*. `MIXED`: four coexisting widths in one datapath — 12-bit membrane, 4-bit weight, ternary spike, 4-bit tracer (§III-C **verified** for the first three). **Not `BINARY`** — the {0,1} train belongs to the IF neuron, which ELSA describes as background and does not use. **Not `POW2`** despite Fig. 9's `2^N`: that is a reset constant, not a value encoding (the distinction drawn on Tender and AQB8) |
| **Generation** | **`G2`** — *the seed is `—`* | By the taxonomy's own G2 test — *"does the paper design a numeric type, **or** build an architecture whose purpose is to execute quantized arithmetic? Either one → G2"* — ELSA does the second unambiguously and the first not at all. And **none of the three G3 threads appears in a 2026 ISCA paper**: no outliers, no weight-only bandwidth argument, no codebook, no LLM. That is itself worth reporting. **Alternative, following the `Phi` precedent:** leave it `—`, on the grounds that Generation classifies *quantization* paradigms and this one is neuromorphic. I prefer `G2` because the test is passed cleanly and a value beats a dash, but I would not argue if it goes to `—` |
| **Optimization** | `SNN` · `elastic inference` · `spine/token-wise pipeline` · `bundled AER` · **`early termination`** · **`input-adaptive time-steps`** · **`mini-batch Gustavson-product`** · **`membrane-stationary dataflow`** · **`addition-only`** · **`near-SRAM`** · **`ANN-to-SNN conversion (SpikeZIP-TF)`** · **`NoC mapping + multi-path routing`** | **All four seed keywords grep clean in the paper's own text** and stand unchanged. The additions name the mechanisms the seed's four do not — in particular the dataflow, which carries the larger of the paper's two attributed gains (27.4× geomean energy versus 1.65× from the pipeline) |

### Proposed venue-list row

```
| [ ] | [ELSA: An ELastic SNN Inference Architecture for Efficient Neuromorphic Computing](https://doi.org/10.1109/ISCA66397.2026.00178) | *close read* | ARCH+SYS | Q | `TERNARY` `INT4` `MIXED` | G2 | `SNN` `elastic inference` `spine/token-wise pipeline` `bundled AER` `early termination` `input-adaptive time-steps` `mini-batch Gustavson-product` `membrane-stationary dataflow` `ANN-to-SNN conversion` | A 4-bit QANN with the activation re-coded from binary-weighted into **temporal unary over T ≤ 32 steps**: MAC → 4-bit add, but the "1-bit" activation is paid for with a **12-bit membrane in SRAM that is 52% of the die**. Time-steps are a **per-input precision knob** (avg T = 6.2 of 32) |
```

### §4 fairness verdict

**Not iso-area** (100.23 mm² vs ANT's 4.527; 6.4× worse GOPS/mm²); **not iso-model** (ELSA's
ResNet50 is pruned — Tab. IV footnote, dropped in Tab. V); **not iso-evidence** (ELSA
post-synthesis vs fabricated PAICORE/TrueNorth/C-DNN; absent baselines estimated from peak).
Iso-node, iso-frequency, ~iso-accuracy. **Not to quote bare:** 3.4×/13.6×, 2.9×/22.1×, 144.4×
(28 nm vs 8 nm).

---

## Note from the source list

> Bundled address-event-representation protocol to lower communication traffic.

---

## Abstract (verbatim, ISCA 2026 proceedings)

> Spiking neural networks (SNNs) exploit event-driven and addition-only computation to
> substantially improve efficiency for intelligent computation. A key temporal property of
> SNNs, elastic inference, allows outputs to emerge progressively, enabling responses to
> salient inputs much earlier than full evaluation. However, existing SNN-specific
> accelerators cannot capitalize on this property. Layer-by-layer designs emit outputs only
> after all layers are complete, while time-step-by-time-step designs rely on coarse-
> grained, layer-wise pipelines that require synchronizing all spines/tokens within a layer.
> This barrier prevents results from being forwarded immediately, delaying the earliest
> possible response and forfeiting the benefits of elastic inference. To address these
> challenges, we propose ELSA, a near-SRAM dataflow architecture that realizes true elastic
> inference through a fine-grained spine/token-wise pipeline and hardware optimizations
> tailored to SNNs. ELSA forwards each spine/token immediately upon production, forming a
> continuous streaming pipeline that substantially reduces the latency to the first
> response. To enhance this lightweight execution, ELSA introduces a bundled address event
> representation protocol to lower communication traffic of network-on-chip (NoC), and
> leverages mini-batch spiking Gustavson-product to cut memory access and exploit inherent
> sparsity. Combined with mapping and scheduling optimizations, ELSA achieves efficient,
> event-driven computation without compromising accuracy. Experiments show that SNNs can
> outperform quantized artificial neural networks (QANNs) while maintaining on-par accuracy.
> For a 4-bit ResNet-50, ELSA achieves 3.4× speedup and 13.6× higher energy efficiency over
> the SOTA QANN accelerator (ANT), and 2.9× speedup and 22.1× energy efficiency gains over
> the SOTA SNN accelerator (PAICORE).
