# Energy-Efficient Neural Network Accelerator Based on Outlier-Aware Low-Precision Computation (OLAccel)

**Venue / Year:** ISCA 2018 · **Link:** https://doi.org/10.1109/ISCA.2018.00063 (no arXiv) · **Reader:** Haoxuan · **Date:** 2026-09-09

## Tags

| | |
|---|---|
| **Level** | `ARCH` |
| **Q-oriented** | `Q-ORIENTED` |
| **Data type** | `INT4` `INT8` `INT16` `MIXED` |
| **Generation** | `G3` (outlier thread — **pre-LLM root, deliberate**) |
| **Optimization** | outlier-aware · sparse high-precision path · extra MAC per SIMD group · coordinate-list outliers · static threshold calibration · zero-activation skip · 24-bit psum tri-buffer · iso-area |

## 1. One-line summary

Splits every tensor by magnitude at a calibrated per-layer threshold into a **4-bit dense body**
and a **1–3.5% high-precision tail** (8-bit weights, 16-bit activations), and pays for the tail
**asymmetrically** — outlier weights fold into the normal datapath via a 17th MAC per 16-lane
group and cost nothing in the common case, outlier activations get their own coordinate list and
their own 16b×4b PE group — which at iso-area in 65 nm buys **768 4-bit MACs against a 16-bit
baseline's 168** and cuts energy **43.5–62.2%** vs ZeNA, **retraining-free**.

## 2. Data type

**Normal.** W4A4, plain symmetric INT. Split by magnitude, not by position.
**Outliers.** Weights **INT8** (sign + 7 mag). Activations **INT16** (INT8 in the 8-bit comparison). *Not* 16-bit weights — the abstract's "e.g. 16 bits" is the algorithm, Table I is the hardware.
**Granularity.** **Per-layer** threshold, one scalar per layer. No per-channel, no per-group, no per-token. Weight side offline; activation side a runtime compare.
**Outlier ratio.** AlexNet 3.5% · VGG-16 **1%** · ResNet-18/101 3% · DenseNet-121 3%. Activation ratio is **of non-zero** activations, so post-ReLU it is lower. Never one flat "3%".
**Outlier storage — weights.** In-place. 80-bit chunk / 16 weights = 64b data + `OLptr` 8b + `OLidx` 4b + `OLMSB` 4b. One outlier's low nibble reuses its own slot; only the high nibble is new. → **5.0 b/weight, +25%, paid whether or not an outlier is present** (derived, not stated).
**Outlier storage — activations.** COO: 16-bit value + 3 coordinates (w, h, c). Widths unstated. This is the unaligned encoding OliVe later attacks.
**Accumulator.** **24-bit** psums throughout, in a 3-bank cluster tri-buffer. Included in the reported area.
**Escape hatch.** conv1 keeps **16-/8-bit raw input activations** in every network; ResNet-18/101 also need **8-bit weights** there. Costs **~half of ResNet-18's total cycles**.
**Retraining.** **PTQ, none.** Calibration = 100 sample images at design time → per-layer threshold. Footnote 1 admits fine-tuning would fix conv1 — which would forfeit the selling point.
**Not exploited.** Zero *weights*. Only zero activations are skipped; baseline ZeNA skips both.

## 3. Optimization

**The asymmetry is the idea, not the outliers.** Weight outlier positions are known offline and
can be packed into the format; activation outlier positions are only known at runtime and must be
discovered. So the two get different machinery, and nothing in the paper is symmetric after that.
Most later work drops the activation half entirely (GOBO, MicroScopiQ weight-only; Oaken KV-only),
which leaves OLAccel as the corpus's only entry paying for **dynamic** outlier detection in
hardware.

**Outlier weights — a 17th MAC per group of 16.** Not per lane; the seed keyword `extra MAC per
lane` overstates the cost 16×. The activation is broadcast to all 17; MAC₁₇ computes
`a × OLMSB`, broadcasts the result back, and the normal MAC at `OLidx` (which is already holding
the outlier's low nibble) adds it to its own psum. **One clock cycle for all 17** — a single
outlier weight per 16 is free. Cost: +6.25% MACs, +25% weight storage, one 4-bit shift. Degraded
case (≥2 outliers in a chunk): `OLptr` chains to a second chunk, **two cycles**, outlier MAC idle,
normal lanes idle in cycle 2. This is why the SIMD width is 16 — Fig. 17 shows P(≥2 outliers)
≈20% at 16 lanes and >50% at 32 or 64, for a 5% outlier ratio.

**Outlier activations — a separate wider datapath.** A dedicated **outlier PE group** of 17
mixed-precision **16b × 4b** MACs, fed from an outlier-activation FIFO in the swarm buffer.
Detection is one compare against the static per-layer threshold. Cost: a whole second PE group
plus the COO records. **The paper never says how many outlier PE groups there are** — DRQ had to
assume one when it modelled this.

**Coherence — a tri-buffer, not a lock.** Two accumulation units write partial sums, so the
cluster output has 3 banks: 2 for the normal accumulator, 1 for the outlier accumulator,
rotating. The outlier accumulator only reaches a bank after the normal one has left it, so the
two run in parallel in a pipeline. This is OLAccel's answer to the problem MicroScopiQ later
solves with a NoC and OASIS with a second datapath.

**What the hardware actually buys.** At iso-area, 4-bit MACs are small enough to fit 768 where a
16-bit baseline fits 168. The energy win is mostly that. The paper's real contribution is the
*other* number: the outlier machinery costs only **+20.6% energy and +10.6% cycles** over the
same design with 0% outliers — cheap enough not to eat the 4-bit gain. Nobody cites it.

## 4. Results

| | |
|---|---|
| Baseline | **ZeNA** (Design & Test'18, skips zero W *and* A) at 16b and 8b — the real baseline behind every headline number. Eyeriss16/8 as the weaker reference |
| Models / datasets | AlexNet, VGG-16, ResNet-18 on ImageNet, all **pruned** (Han et al.; ResNet-18 by the authors). ResNet-101 and DenseNet-121 appear in the accuracy study only — **never run on the hardware** |
| Accuracy delta | AlexNet 4-bit @3.5% outliers: **−0.8% top-5** vs FP32. "<1% top-5" across the five networks. 4-bit linear with 0% outliers: **−76.57%**, total collapse |
| Speedup | Cycles vs ZeNA16/8 — AlexNet **−31.5%/−35.1%**, VGG-16 **−45.3%/−28.3%**, ResNet-18 **−25.3%/−29.0%**. vs Eyeriss16: AlexNet −71.8%, ResNet-18 −80.1% |
| Energy / area | vs ZeNA16 (ZeNA8): AlexNet **−43.5% (−27.0%)**, VGG-16 **−56.7% (−36.3%)**, ResNet-18 **−62.2% (−49.5%)**. Area 1.67 mm² (16b cmp) / 0.93 mm² (8b cmp). Outlier path itself: **+20.6% energy, +10.6% cycles** over 0% outliers |
| Technology node | **65 nm LP**, 250 MHz, 1.0 V — the far end of the corpus's node range (OliVe 22 nm, Tender/Oaken 28 nm, MicroScopiQ 7 nm) |
| Evidence level | **Cycle-accurate model + Design Compiler post-synthesis power + CACTI (SRAM) + Micron DRAM model.** No silicon, no FPGA, no PnR |
| **Is the comparison fair?** | Iso-area, iso-node, iso-memory — disciplined for 2018. **Not iso-MAC** (768 vs 168), **not iso-accuracy** (baselines assumed lossless; OLAccel takes 0.8%). Conceded: memory sizing favours OLAccel; ZeNA skips zero weights and it does not. Not conceded: accuracy study at 16-bit outliers, hardware at 8-bit. Don't quote "43.5%" bare — vs ZeNA16, pruned AlexNet, 4.6× the MACs, cycle model |

## 5. Comment

## 6. Claude notes

> **Suggestions from the reading agent. Strip this section before copying into
> `QuantArchSurvey/venues/ISCA/notes/`.**

- **§5 material, if you want it.** The `G3` here earns itself rather than being granted: the
  paradigm — separate the tail, spend on it, quantize the body hard — is stated *completely* in
  2018, five years before the LLM papers that inherit it. This is the best citation in the corpus
  for "outlier-aware quantization is not an LLM-era invention."
- **Outlier-currency axis, now five entries.** OLAccel = **+1 b/weight unconditionally + a COO
  record per outlier activation + a second datapath**, chosen by magnitude vs a calibrated
  threshold. Reading down "who chooses the outlier" (magnitude'18 → adjacency'23 → Hessian'25)
  shows real progress; reading down "what is paid" (metadata → **zero** metadata in OliVe →
  metadata again in MicroScopiQ) shows the field has **not** converged. That contrast may be worth
  a paragraph.
- **A second axis this paper seeds and nobody names: static vs dynamic outlier identification.**
  OLAccel fixes the threshold at design time; DRQ (ISCA'20) exists specifically to attack that;
  Tender sidesteps identification entirely. Worth noting that the 2023-25 LLM papers mostly
  revert to OLAccel's static side.
- **Three citation hazards, all documented in `ANALYSIS.md`.**
  (1) **OliVe §2.2's "71% PE-array area overhead" is not in OLAccel** — the paper reports no area
  breakdown at all, only whole-accelerator mm². Do not repeat it as OLAccel's number.
  (2) **Every OLAccel-on-a-transformer number in this corpus is a re-implementation** — OliVe
  says so outright ("We *extend* OLAccel to the Transformer-based models"), and Tender,
  MicroScopiQ and DRQ each build their own. The published OLAccel and the baseline called
  "OLAccel" in ISCA'23-'25 share a name and little else. Any table putting those four side by
  side compares four different OLAccels.
  (3) **DRQ's ~5% accuracy criticism is real** (5.4% MobileNet-v2, 5.1% Inception-v3, 4.3% avg
  on ILSVRC-2012) — but it is DRQ's own reproduction, **DRQ retrains where OLAccel does not**,
  and DRQ never says top-1 or top-5. That last asymmetry, not the number, is the thing to cite.
- **Seed-tag suggestions (I did not edit the file).** In `venues/ISCA/README.md`: add `INT8` and
  `INT16` to the data-type cell — outlier weights are 8b and outlier activations 16b, both
  verified in Table I, and the current `INT4` `MIXED` hides the actual tail format. Change the
  keyword `extra MAC per lane` → `extra MAC per SIMD group`: it is one extra MAC per **16** lanes,
  a 16× difference in the cost of the paper's headline mechanism. `ARCH`, `Q`, `G3` all stand.
- **`ARCH` vs `ALGO+ARCH` was a real call.** The quantization *method* is cited to ref [11]
  (Park/Yoo/Vajda, *Value-aware quantization*, arXiv 2018) — this is the architecture paper for
  someone else's algorithm. I kept `ARCH`, matching the seed, but the calibration procedure and
  the split-nibble format are algorithmic contributions if you want to argue it.
- **A number I would exclude from any cross-paper table:** all of OLAccel's energy figures,
  unless the table carries a node column. 65 nm against MicroScopiQ's 7 nm is a ~9× process gap
  and only MicroScopiQ scales its baselines.
- **`survey/TAGS.md` should gain** `outlier-aware` for OLAccel if that tag exists locally, and
  OLAccel should be added wherever `mixed-precision` is enumerated.
