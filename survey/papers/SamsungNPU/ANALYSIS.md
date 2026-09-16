# SamsungNPU — paper notes

**Sparsity-Aware and Re-Configurable NPU Architecture for Samsung Flagship Mobile SoC**
Jun-Woo Jang, Sehwan Lee, Dongyoung Kim, Hyunsun Park, Ali Shafiee Ardestani, Yeongjae Choi,
Channoh Kim, … Joseph Hassoun, SukHwan Lim, Changkyu Choi — **23 authors**, Samsung Advanced
Institute of Technology (Suwon), Samsung Semiconductor (San Jose) and Samsung Electronics
(Hwaseong). Marked **"Industrial Product"** on page 1. Transcribed 2026-09-10.
**ISCA 2021** ｜ DOI: **10.1109/ISCA52012.2021.00011**
Publication info verified 2026-09-02: venue, year **and DOI** all read out of the archived
PDF's own text (IEEE proceedings banner; the DOI was grepped for, not assumed); page range
from the IEEE Xplore link in the source CSV.
Archived here: the **published IEEE version** (the page-1 IEEE proceedings banner is present in the extracted text), 14 pages.

Status: **note ready** ｜ Last updated: 2026-09-10
Tags: `analytical-dtype` `mixed-precision` `multi-bitwidth-hw` `accelerator`
How far it was read: **full close read of §I-§VIII**, with §V-D (mixed-precision) and §VII
(evaluation) read line by line and the rest at survey-relevance depth — this is `non-Q`, so the
quantization content and the evidence levels are worked out in full while the sparsity and
dataflow contributions are taken as reported. Figures are bitmaps in the extraction.

> Publisher record: https://ieeexplore.ieee.org/document/9499876
> **There is no arXiv version** (arXiv API title search, 2026-09-02). The PDF was downloaded by a
> human and filed through [`survey/uploads/`](../../uploads/) — the sanctioned route when the
> arXiv-only rule leaves a paper unreachable; see
> [`Notes-002`](../../../Claude/notes/Notes-002-paper-source-access.md).
> The PDF is **not committed** (2.7 MB) and **cannot be re-downloaded by script** —
> both publishers 403. Re-extract with `python3 extract.py` → `extracted/` (committed).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, ISCA 2021 row.

---

## Brief

### 1. Motivation

A commercial mobile NPU must run a *comprehensive range* of networks under a fixed power and
area budget — two goals that pull against each other. Academic accelerators optimize one
workload; a flagship SoC cannot.

### 2. Overview

An **industrial product paper** on the NPU in a Samsung flagship SoC (5 nm): an adder-tree
inner-product engine that skips zeros in the input feature map, a **re-configurable MAC
array**, dynamic internal memory-port assignment for bandwidth, and an architecture
supporting **mixed-precision (INT8/INT16)** arithmetic. Includes a lessons-learned section.

### 3. Pros and cons

**Pros**

- Silicon measurements, not simulation: **290.7 FPS and 13.6 TOPS/W** on 8-bit Inception-v3
with one core; 1.79× over the dense baseline from the combined optimizations.
- The lessons-learned section is unusually candid and is the most citable part — e.g. that
*limiting* reconfigurability costs little performance but saves significant area.
- Zero-skipping is analysed at two granularities (intra- and inter-lane) with the trade-offs
quantified rather than asserted.

**Cons**

- Mixed-precision support is one feature among several; the paper is about the whole NPU, so
the quantization content is thin relative to its neighbours here.
- As a product paper, design choices are reported rather than ablated against alternatives
that were not built.
- INT8/INT16 is a narrow precision range by 2026 standards — no sub-8-bit story.

### 4. Where it applies

Industrial calibration for the **multi-bitwidth hardware** box: what reconfigurability a
shipping mobile NPU actually pays for, versus what research designs propose. Pair with
[`TPUv4i`](../TPUv4i/ANALYSIS.md) and [`RaPiD`](../RaPiD/ANALYSIS.md).

---

## Conclusions

**`non-Q` is correct, and the close read confirms the revision log.** Apply the test — swap the
format for plain INT8 — and everything survives: IFM zero-skipping, the reconfigurable MAC array,
dynamic memory-port assignment, the adder-tree inner-product engine. INT8 **is** the format the
NPU is optimised for; INT16 is one section (§V-D) implemented as a time-multiplexing trick over the
INT8 datapath. There is no numeric format contribution here.

**But its one quantization section is more interesting than its size suggests, because it settles a
question `BitFusion` opened.** Samsung's INT16 support decomposes each 2-byte operand into two
1-byte halves and runs **four subcomputations (LL, LH, HL, HH)** on the INT8 datapath, accumulating
into a growing partial sum — **"without the addition of a multiplier or accumulators"**, using only
muxing in the data fetcher and vector unit. That is exactly the **temporal** design that BitFusion's
Fig. 10 measures losing **3.5× area and 3.2× power** to spatial fusion. Samsung, shipping a
flagship SoC three years later, chose temporal anyway.

**The area breakdown explains why, and it is the most useful thing in the paper for this survey.**
In a real mobile NPU core, **arithmetic circuits are 23.4% of an NPUE** while the **weight buffer
alone is 57.1% of the tensor unit**, and the whole **sparsity unit is 2.4%**. BitFusion's
spatial-versus-temporal comparison is measured over the multiplier, shifter and accumulator — a
component that, in a product, is under a quarter of the area. So the marginal cost of *adding
multipliers* for a capability used by a minority of workloads is a worse trade than the throughput
loss of doing it in four cycles. **BitFusion won the microbenchmark and lost the product**, and the
reason is that a product optimises the area of the capability it *doesn't* mostly use.

**Its evidence is split, and the split matters.** **13.6 TOPS/W, 290.7 FPS (Inception-v3) and
131.13 FPS (ResNet-50) are silicon measurements** on Samsung 5 nm. The **1.79×** speedup from the
combined optimisations is **simulation** — "extensive simulations verified". The abstract presents
them together. Only the first set belongs in a measured-silicon column.

**Its place in the survey is as a product reality-check, not as a quantization entry.** Alongside
`RaPiD`, it is one of only two fabricated designs in the corpus, and the two make different
industrial arguments about the same problem.

---

## Method

**The NPU** (§V-B) **verified**. Three cores; each core holds two engines (**NPUEs**) of **1k MACs**
each sharing an on-chip scratchpad; an adder-tree inner-product engine; a controller orchestrating
scratchpad ↔ external memory transfer.

**Precision support** (§IV-C, §V-D) **verified**:

- **INT8 is the design target** — "8-bit integer arithmetic is sufficient for most mobile
  applications, [so] we optimize the proposed NPU for 8-bit integer arithmetic."
- **INT16 by time-multiplexing**: a 2-byte operand splits into `F_H, F_L` and `W_H, W_L`; four
  subcomputations `LL, LH, HL, HH` run on the INT8 datapath; each result accumulates into the
  most-significant 3 or 4 bytes of the running partial sum (`S[3:0]`, then `S[4:1]`, …).
  **Four iterations for INT16×INT16**, and crucially **no additional multiplier or accumulator** —
  only muxing in the data fetcher and vector unit.
- **Channel-wise quantization is supported without tensor reshaping** (§V-B), because the 1-D output
  feature map tensor is already divided along the channel dimension; a dedicated quantization unit
  sits beside the activation unit.
- Accuracy framing is inherited, not measured: INT8 costs "1~2%" on well-known image classification
  models, cited to [24].

**The rest of the design** (reported, not audited here): IFM zero-skipping analysed at **intra- and
inter-lane** granularity; a **reconfigurable MAC array** with a tile/subtile scheme; **dynamic
internal memory-port assignment** for bandwidth.

---

## Key numbers, with their frame

**Two evidence levels in one paper — do not pool.** (a) **Silicon measurement** on a fabricated
Samsung **5 nm** die. (b) **Simulation** for the optimisation breakdown.

| Setting | Model | Metric | Baseline | Result | Source |
|---|---|---|---|---|---|
| **Silicon** | Inception-v3, INT8, **single core** | throughput | — | **290.7 FPS** | §VII **measured** |
| **Silicon** | ResNet-50 | throughput | — | **131.13 FPS** | §VIII **measured** |
| **Silicon** | — | **peak energy efficiency** | — | **13.6 TOPS/W** | §VII, §VIII **measured** |
| **Simulation** | — | speedup from combined optimisations | dense baseline | **1.79×** | §VIII **simulated — not silicon** |
| **Area breakdown, one NPUE** | — | share of area | — | **tensor unit 68.5%** · vector unit **17.0%** · data fetcher **3.4%** · **sparsity unit 2.4%** | Table IV **verified** |
| " — inside the tensor unit | — | share | — | **weight buffer 57.1%**, **arithmetic circuits 23.4%** | §VII **verified** |
| Configuration | — | cores / engines / MACs | — | **3 cores × 2 NPUEs × 1k MACs** | §V-B **verified** |
| INT16 cost | — | iterations, extra hardware | INT8 | **4 iterations, zero extra multipliers or accumulators** | §V-D **verified** |
| Node | — | — | — | **Samsung 5 nm**, fabricated | §VII **verified** |

**The area breakdown is the number to carry.** Arithmetic is **23.4%** of an engine and the weight
buffer is **57.1%** of the tensor unit — so in a shipping mobile NPU, buffers dominate and
multipliers do not.

---

## Cost and requirements

| | |
|---|---|
| **INT16** | **4× the cycles** of INT8, but **no extra multipliers or accumulators** — pure muxing. The deliberate product trade |
| **Reconfigurability** | The tile/subtile scheme "demands **double** the number of processing blocks in the vector unit"; the vector unit is **17.0%** of an NPUE |
| **Zero-skipping** | The sparsity unit costs **2.4%** of an NPUE — cheap |
| **Precision range** | **INT8/INT16 only.** No sub-8-bit path at all |
| **Accuracy** | Inherited by citation ("1~2%"), not measured in this paper |
| **Retraining** | Not discussed — the NPU consumes whatever the toolchain produces |
| **Escape hatch** | INT16 for accuracy-critical applications; channel-wise scales |

---

## Limitations and open questions

**Admitted.** The lessons-learned discussion is candid — notably that *limiting* reconfigurability
costs little performance while saving significant area, which is the paper's most citable
observation. Reconfigurability's vector-unit cost is stated explicitly.

**Unadmitted, and material.** (i) **Silicon and simulation numbers appear side by side** in the
abstract and conclusion without distinguishing them; only the FPS and TOPS/W figures are measured.
(ii) **As a product paper, alternatives are reported rather than ablated** — there is no
spatial-fusion comparison to justify the temporal INT16 choice, even though a well-known ISCA'18
result argues against it. (iii) **No accuracy measurements**, only a citation. (iv) **13.6 TOPS/W
is a peak**, and the per-network FPS figures are the sustained results; the paper does not present
a sustained TOPS/W.

---

## Relation to other entries

**It completes a three-paper argument about multi-precision datapaths, and it is the one that
shipped.**

| Paper | Approach | Cost of flexibility | Evidence |
|---|---|---|---|
| `BitFusion` (ISCA'18) | **one fused datapath, spatial** | shift-add tree = 67% of the Fusion Unit | 45 nm synthesis |
| `RaPiD` (ISCA'21) | **two separate pipelines** | ~16% area for the INT pipeline | **7 nm silicon** |
| **`SamsungNPU` (ISCA'21)** | **one datapath, temporal** | **zero extra multipliers — muxes only** | **5 nm silicon** |

BitFusion measures temporal designs losing **3.5× area / 3.2× power** to spatial fusion — and both
shipping products declined to fuse spatially. SamsungNPU's own area table says why: **arithmetic is
23.4% of an engine.** Optimising the multiplier is optimising a quarter of the area, and paying for
it with *more* multipliers is the wrong direction when the capability is a minority case. This is
the corpus's clearest instance of a microbenchmark result not surviving contact with a product, and
it deserves a paragraph.

**With `RaPiD` it is one of only two fabricated designs here.** The two disagree productively:
RaPiD builds a **second pipeline** for low precision because low precision is its *main* case
(training at FP8, inference at INT4); SamsungNPU **time-multiplexes** high precision onto the low
one because high precision is its *exception* case. Same problem, opposite majority assumption,
opposite answer. That framing is more useful to the survey than either paper alone.

**It also supplies the corpus's only product-grade area census.** Weight buffer 57.1% of the tensor
unit, arithmetic 23.4%, sparsity 2.4%, reconfigurability doubling vector-unit blocks. Every
simulation-based entry in this corpus reports area for the datapath it designed; this one reports
what a whole shipping engine looks like — useful for sanity-checking any "X% area overhead" claim.

**Node.** Samsung **5 nm, fabricated** — the finest measured node in the corpus, against `RaPiD`'s
7 nm measured and `MicroScopiQ`/`Omni-LUT`'s 7 nm synthesised.

---

## For the note

**§1 one-line summary.** A shipping Samsung flagship-SoC NPU (5 nm, 3 cores × 2 engines × 1k MACs)
whose quantization content is one section: **INT8 is the design target, and INT16 is supported by
time-multiplexing four INT8 subcomputations (LL/LH/HL/HH) over the same datapath with no extra
multiplier or accumulator** — the temporal design `BitFusion` measured losing 3.5× area to spatial
fusion, chosen anyway because in a real NPU **arithmetic is only 23.4% of an engine** while the
weight buffer is 57.1% of the tensor unit; measured at **13.6 TOPS/W and 290.7 FPS** on INT8
Inception-v3.

**Proposed tags — human-verified 2026-09-10. The seed row and the revision log's `Q` → `non-Q` change both stand.**

| Axis | Value | Evidence |
|---|---|---|
| **Level** | `ARCH` | An industrial product paper about a datapath. **Checked against the `SYS` rule**: a toolchain is implied but never described — no compiler or ISA section — so `SYS` does **not** apply |
| **Q-oriented** | **`non-Q`** — the log's change is right | Swap the format for plain INT8 and IFM zero-skipping, the reconfigurable MAC array, dynamic port assignment and the adder-tree engine all survive untouched. INT8 *is* the format; INT16 is a muxing trick in one section |
| **Data type** | `INT8` `INT16` `MIXED` | Both exact and both stated. No sub-8-bit path anywhere |
| **Generation** | `G2` | Match the datapath to the bitwidth, no tail format, no codebook, no outliers — the `BitFusion` family, three years later and in silicon |
| **Optimization** | `mobile NPU` `IFM zero-skipping` `reconfigurable MAC array` `dynamic port assignment` + **`time-multiplexed INT16`** `adder-tree inner product` `5 nm silicon` `industrial product` | The time-multiplexing is the only quantization mechanism, and it is the citable one |

**§4 fairness verdict.** Silicon, which almost nothing else here is — but **two evidence levels sit
side by side in the abstract**: **13.6 TOPS/W, 290.7 FPS and 131.13 FPS are measured**, while the
**1.79× optimisation speedup is simulation**. Only the first belongs in a measured column. As a
product paper, choices are **reported rather than ablated** — notably the temporal INT16 design,
with no comparison against the spatial alternative a well-known ISCA'18 result recommends. Accuracy
is a **citation ("1~2%"), not a measurement**, and 13.6 TOPS/W is a **peak** with no sustained
counterpart.

**Proposed venue-list row:**

```
| [ ] | [Sparsity-Aware and Re-Configurable NPU Architecture for Samsung Flagship Mobile SoC](https://doi.org/10.1109/ISCA52012.2021.00011) | *close read* | ARCH | non-Q | `INT8` `INT16` `MIXED` | G2 | `mobile NPU` `IFM zero-skipping` `reconfigurable MAC array` `time-multiplexed INT16` `dynamic port assignment` `5 nm silicon` `industrial product` | Industrial product. INT16 by **time-multiplexing four INT8 subcomputations with no extra multiplier** — the temporal design BitFusion measured losing 3.5×, chosen anyway because **arithmetic is 23.4% of a real NPU engine** |
```

## Note from the source list

> **Keywords:** Has a section discussing supports for Mixed-precision (int8 & int16)


## Abstract (verbatim, from the archived PDF)

> Of late, deep neural networks have become ubiquitous in mobile applications. As mobile
> devices generally require immediate response while maintaining user privacy, the demand
> for on-device machine learning technology is on the increase. Nevertheless, mobile devices
> suffer from restricted hardware resources, whereas deep neural networks involve
> considerable computation and communication. Therefore, the implementation of a neural-
> network specialized hardware accelerator, generally called neural processing unit (NPU),
> has started to gain attention for the mobile application processor (AP). However, NPUs for
> commercial mobile AP face two challenges that are difficult to realize simultaneously:
> execution of a wide range of applications and efficient performance. In this paper, we
> propose a flexible but efficient NPU architecture for a Samsung flagship mobile system-on-
> chip (SoC). To implement an efficient NPU, we design an energy-efficient innerproduct
> engine that utilizes the input feature map sparsity. We propose a re-configurable MAC
> array to enhance the flexibility of the proposed NPU, dynamic internal memory port
> assignment to maximize on-chip memory bandwidth utilization, and efficient architecture to
> support mixed-precision arithmetic. We implement the proposed NPU using the Samsung 5nm
> library. Our silicon measurement experiments demonstrate that the proposed NPU achieves
> 290.7 FPS and 13.6 TOPS/W, when executing an 8-bit quantized Inception-v3 model [1] with a
> single NPU core. In addition, we analyze the proposed zero-skipping architecture in
> detail. Finally, we present the findings and lessons learned when implementing the
> commercial mobile NPU and interesting avenues for future work.
