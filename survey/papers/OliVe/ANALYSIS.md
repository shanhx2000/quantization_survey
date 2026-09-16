# OliVe — paper notes

**OliVe: Accelerating Large Language Models via Hardware-friendly Outlier-Victim Pair Quantization**
Cong Guo, Jiaming Tang, Weiming Hu, Jingwen Leng, Chen Zhang, Fan Yang, Yunxin Liu, Minyi
Guo, Yuhao Zhu
**ISCA 2023** ｜ DOI: **not recorded** — the ACM/IEEE record is not reachable by script (403); look it up when citing
Venue evidence (2026-09-02): arXiv `comments` field, verbatim: *"ISCA 2023"*
Archived here: **arXiv:2304.07493v1** (2023-04-15), 15 pages — **the preprint, not the
published ISCA 2023 version**; the two were **not compared**.

Status: **note ready** ｜ Last updated: 2026-09-09
Tags: `new-data-type` `combined-dtype` `analytical-dtype` `mixed-precision` `accelerator`
How far it was read: **close read of §1–§6** — abstract, introduction, §2 motivation and prior
outlier architectures, §3 (OVP encoding algorithm, normal-value data types, abfloat, threshold
framework), §4 (GPU tensor-core and systolic-array integration), §5 (all of evaluation incl.
Tables 3–11) and §6. **Skimmed:** related work, references. Figures read for prose claims;
per-bar values of Figs. 9–10 not transcribed.


> Original: https://arxiv.org/abs/2304.07493
> The PDF is **not committed** (1.4 MB). Re-download: `curl -sSL -o 2304.07493.pdf https://arxiv.org/pdf/2304.07493`
> Extract text: `python3 extract.py` → `extracted/` (committed, greppable)
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, ISCA 2023 row.

---

## Brief

### 1. Motivation

LLM size grows 240× every two years, outpacing hardware. Outliers block low-bit
quantization, and the existing fix — sparsity encoding with a **global coordinate list** —
needs global coordination, complex encode/decode logic and an orchestration controller. That
overhead is why outlier-aware accelerators underdeliver.

### 2. Overview

The key insight is asymmetric: **outliers matter, and the normal values adjacent to them do
not**. So sacrifice the neighbour — the "victim" — and use its bits to store the outlier in
place. This **outlier-victim pair (OVP)** encoding is memory-aligned and purely local, which
means it drops into a systolic array or tensor core without a global sparsity structure.

### 3. Pros and cons

**Pros**

- Turns a global, irregular problem into a local, aligned one — the single cleanest idea in
the outlier thread, and the reason it is so widely cited.
- 4.5× speedup and 4.0× energy reduction over GOBO **with better model accuracy**, i.e. it
wins on both axes rather than trading them.
- Being memory-aligned is what makes it embeddable in existing hardware (the paper shows GPU
and systolic-array integration), which is a deployability argument the sparsity-based
predecessors cannot make.

**Cons**

- Pruning the victim is a real accuracy cost that is *assumed* tolerable because victims are
'unimportant'; that assumption is validated empirically, not derived.
- It works because outliers are locally sparse — where two outliers are adjacent, the scheme
has to degrade. [`MicroScopiQ`](../MicroScopiQ/ANALYSIS.md) attacks exactly this, arguing
'adjacent outliers matter' and that OliVe assumes an outlier locality that does not hold
for all foundation models.
- [`Tender`](../Tender/ANALYSIS.md) reports OliVe behind it on perplexity at comparable
settings, and [`MicroScopiQ`](../MicroScopiQ/ANALYSIS.md) claims ≥8% accuracy advantage at
lower precision — so its accuracy standing is contested by later work.

### 4. Where it applies

The hinge of the **outlier / combined-data-type** thread and a required read: it is both the
state of the art that 2025–26 papers cite and the target they attack. Its argument that
*hardware-friendliness is part of the algorithm* is a survey-level theme.

---

## Conclusions

<!-- Nothing here yet: the paper has not been read. Replace this with numbered,
     evidence-marked claims on the close read, then move the status to `analysis ready`. -->

**Read in full 2026-09-09.** The brief holds. Three additions, one of which changes how the
survey should place this paper.

**1. OliVe pays for outliers in a currency no other corpus entry uses.** Everything stays at a
**flat 4 bits (or 8), perfectly memory-aligned, with zero metadata** — the outlier's cost is
paid by **destroying its neighbour**, not by extra bits, a sparse index, or a high-precision
path. That gives the corpus three distinct outlier currencies, which is a cleaner organizing
axis than "outlier-aware yes/no":

| Paper | What an outlier costs |
|---|---|
| [`Oaken`](../Oaken/ANALYSIS.md) | **extra bits + metadata** — 5-bit value + 8-bit COO entry → 4.8 effective bits |
| [`OASIS`](../OASIS/ANALYSIS.md) | **high precision** — 1 % of activations kept at FP16 on a second datapath |
| **OliVe** | **a destroyed neighbour** — the adjacent normal value is pruned to zero; bitwidth stays exactly 4 |

**2. The evaluation stops at 7B and contains no LLaMA.** Largest models are GPT2-XL,
BLOOM-7B1 and OPT-6.7B; the rest are BERT-base/large and BART-base (**verified**, §5.1). For a
paper the taxonomy uses as *the* G3 outlier anchor, that is a narrow base — and it explains why
[`TransitiveArray`](../TransitiveArray/ANALYSIS.md) and [`Tender`](../Tender/ANALYSIS.md), both
evaluating OliVe on LLaMA, find it much weaker than this paper reports.

**3. The paper's own strongest result is one the brief did not mention**: plain **INT8 breaks
on OPT-6.7B** — C4 perplexity **74.30 against FP32's 10.63** — while 8-bit OliVe lands at
**10.73** (Table 9, **verified**). That is the sharpest demonstration in the corpus of the
"6B threshold" phenomenon, and a better citation than any of its speedups.

---

## Method

**Verified** unless marked.

**The complaint.** Prior outlier architectures (GOBO, OLAccel, BiScaled-DNN, DRQ) separate
outliers **globally** — a coordinate list, block-sparse indices, or a bitmap. That means
unaligned memory access, decode/encode logic, and an orchestration controller, and it is
"incompatible with the memory sub-systems of existing accelerators". GOBO in particular can
only compress weights in DRAM and still computes in FP16.

**The observation.** Take two adjacent values. Three cases: normal-normal, one-outlier, and
two-outlier. **Two-outlier pairs "almost never show up" in well-trained LLMs.** And for a
one-outlier pair, *pruning the normal neighbour to zero costs almost nothing* — clipping 0.1 %
of outliers is disastrous, but pruning 0.1 % of normal values costs **< 0.1 % accuracy**. So
the neighbour is expendable. It becomes the **victim**.

**1. OVP encoding** (§3.1). Steal one codepoint from the normal-value type to act as an
**outlier identifier**: `1000₂` is `−8` in signed int4, so int4's range narrows to `[−7, 7]`
and `1000₂` marks "my partner is an outlier". A victim is written as that identifier; the
outlier goes in the other half. Left-outlier (O-V) and right-outlier (V-O) are distinguished
**implicitly by position — no index bit**. An OV pair is therefore exactly **8 bits, byte
aligned**, and decoding is entirely local. Two-outlier pairs keep the larger and **prune the
other outlier**.

**2. Normal-value types** (§3.2). `int4`, `flint4` (from ANT), or `int8`. For `flint4` the
identifier `1000₂` is `−0`, unused in the original design — so **no representable value is
sacrificed at all**. For int8, `10000000₂` becomes the identifier and range narrows to
`[−127, 127]`.

**3. abfloat — adaptive biased float** (§3.3), the outlier type. A 4-bit float in fixed-point
form, `sign × (1≪mb + mantissa) ≪ (exponent + bias)`, so decoding is **shifts only**. `E2M1`
is chosen by measuring rounding error of the largest outliers across E0M3/E1M2/E2M1/E3M0. The
**bias is the trick**: without it, abfloat's range *overlaps* the normal type's (int4 and E2M1
share 3, 4, 6). Setting `bias = 2` moves E2M1's range to `{12 … 96}`, **complementary to int4**
rather than redundant with it; `bias = 3` gives `{24 … 192}` for flint4. Every codepoint
therefore buys range the normal type does not already cover.

**4. Threshold selection** (§3.4). The outlier threshold is chosen by **MSE minimisation**, the
standard PTQ approach. The tension is explicit: a lower threshold means more OV pairs and lower
MSE, but also **more two-outlier pairs, where an outlier is destroyed** — so the search is
really controlling the two-outlier rate.

**5. Integration** (§4). Two targets. **GPU tensor core**: a lightweight OVP decoder per FEDP
on a Turing 2080 Ti (68 SM × 8 TC × 2 octets × 8 FEDPs). **Systolic array**: decoder at the PE.
No datapath redesign in either — the decoder emits an int4 and an exponent into an existing
shift-and-add path.

## Key numbers, with their frame

**Frames.** PyTorch; BERT-base/large and BART-base on **8 GLUE datasets** plus SQuAD v1.1/v2.0;
GPT2-XL, BLOOM-7B1, OPT-6.7B on **Wikitext103 and C4**. Decoder in Verilog RTL, **Synopsys DC at
TSMC 22 nm**, CACTI for memories. GPU results from **GPGPU-Sim 4.0 / AccelSim** configured as an
RTX 2080 Ti, energy from AccelWattch/GPUWattch/CACTI, GEMM via CUTLASS. Accelerator results
from a **DnnWeaver-based cycle-level simulator**. Batch 2 for GPT-like, 16 for BERT-like.
**No silicon. Nothing above 7B, and no LLaMA.**

| Setting | Model | Metric | Baseline | Result | Source |
|---|---|---|---|---|---|
| **The headline finding — INT8 breaking at 6.7B** | OPT-6.7B | C4 perplexity | FP32 **10.63**; plain int8 **74.30** | **8-bit OliVe 10.73** | Table 9 |
| same | OPT-6.7B | Wikitext103 PPL | FP32 22.14; int8 **37.45** | **8-bit OliVe 22.34** | Table 9 |
| 8-bit | GPT2-XL / BLOOM-7B1 | Wiki PPL | FP32 17.48 / 13.05 | **17.49 / 13.13** — essentially exact | Table 9 |
| 4-bit PTQ | GPT2-XL | Wiki / C4 PPL | FP32 17.48 / 16.30; int4 **1E+4 / 9E+3**; 4-bit ANT 27.79 / 27.35 | **19.11 / 18.08** | Table 9 |
| 4-bit PTQ | BERT-base | GLUE (CoLA / SST-2) | FP32 59.60 / 93.35 | **59.30 / …** — "< 1 % loss" claimed across BERT-like | Table 6, §5.2 |
| Speedup, **GPU** | 5 models, geomean | × | GOBO / int8 / ANT | **4.5× / 2.7× / 2.4×** | §5.3, Fig. 9a · GPGPU-Sim |
| Energy, GPU | same | × reduction | GOBO / int8 / ANT | **4.0× / 2.3× / 2.0×** | §5.3, Fig. 9b |
| Speedup, **systolic accelerator** | same | × | AdaFloat / OLAccel / ANT | **4.8× / 3.8× / 3.7×** | §5.4, Fig. 10a · DnnWeaver sim |
| Energy, accelerator | same | × reduction | AdaFloat / OLAccel / ANT | **3.7× / 2.1× / 3.3×** | §5.4, Fig. 10b |
| Decoder area | — | µm² @22 nm | — | 4-bit **13.53**, 8-bit **18.00** | Table 10 |
| Area overhead, systolic | — | % of core | — | **2.2 % (4-bit), 1.5 % (8-bit)** | §5.4, Table 11 |
| Area overhead, GPU | RTX 2080 Ti, 754 mm² die | % of die | — | **0.250 % / 0.166 %** (139,264 4-bit + 69,632 8-bit decoders, scaled to 12 nm) | §5.3, Table 10 |

Left blank: per-bar values of Figs. 9–10; the full GLUE and SQuAD tables (read, not transcribed
— they support a "< 1 % loss" claim rather than being individually citable).

## Cost and requirements

- **Data type.** `W4A4` and `W8A8`. **Normal values**: `int4`, `flint4` (ANT's adaptive type)
  or `int8`, each with one codepoint stolen as the outlier identifier. **Outliers**: 4-bit
  **abfloat E2M1** with an adaptive exponent bias placing its range *complementary* to the
  normal type's. Both weights and activations quantized — unlike GOBO, which is weight-only.
- **Granularity: pairwise, and that is unusual.** The unit is **two adjacent values**, not a
  tensor, channel, token or group. There is no group size to report; the threshold is
  per-tensor via MSE minimisation. **The corpus's finest outlier granularity** and the only one
  with no scale-sharing structure at all.
- **Outlier mechanism: local substitution.** No coordinate list, no bitmap, no sparse matrix,
  no second datapath, **no index bit** — direction is implicit in which half holds the
  identifier.
- **Escape hatch — the victims, and it is genuinely different.** Effective bitwidth is
  **exactly 4** (or 8), byte-aligned, **zero metadata overhead**. What is spent instead is
  **information**: every outlier zeroes its neighbour, and in a two-outlier pair **one outlier
  is destroyed outright**. The threshold search in §3.4 is, read plainly, a knob for how often
  the scheme is allowed to destroy an outlier.
- **Retraining: PTQ**, no retraining, explicitly argued for on the grounds that QAT on LLMs is
  "resource-consuming".
- **What the hardware pays.** A decoder — 13.53 µm² (4-bit) / 18.00 µm² at 22 nm; **2.2 % /
  1.5 % of systolic core area**, **0.25 % of a 2080 Ti die**. The cheapest outlier hardware in
  the corpus by a wide margin, which is the paper's actual claim to fame.

## Limitations and open questions

**Authors admit:** two-outlier pairs force pruning a real outlier, and the threshold search
must keep their rate low; ANT ends up at int8 on 80 % of layers under PTQ, so its comparison is
partly a comparison against a degraded configuration.

**Not admitted:**

1. **Nothing above 7B, and no LLaMA.** The paper opens on OPT-175B not fitting an H100 and
   evaluates nothing larger than BLOOM-7B1. Every later corpus entry that runs OliVe on LLaMA
   reports worse results than this paper's framing suggests.
2. **The victim mechanism assumes outliers are isolated, and that assumption is load-bearing
   and untested at scale.** "Two-outlier pairs almost never show up" is asserted from
   BERT/GPT2-XL/OPT-6.7B tensors. If outliers cluster in larger models — and the literature
   since suggests channel-structured outliers do — the failure mode is silent destruction of
   real outliers. **No sensitivity study on the two-outlier rate is reported.**
3. **Pairing is position-dependent, so the scheme is sensitive to tensor layout.** An outlier
   whose neighbour is also needed cannot be encoded; nothing addresses reordering or what
   happens under different memory layouts.
4. **The 4.5× over GOBO is partly an artefact of GOBO's scope.** GOBO is **weight-only and
   computes in FP16**; OliVe quantizes both operands to 4 bits. The comparison is fair as
   "these are the two designs", but it is not an outlier-mechanism comparison — most of the gap
   is weight-only versus W4A4.
5. **Evidence levels differ across the two integration stories** — GPU numbers from GPGPU-Sim,
   accelerator numbers from a DnnWeaver-based simulator, area from 22 nm synthesis scaled to
   12 nm for the GPU claim. Not pooled in the paper, but easy to pool when citing.

## Relation to other entries

- **The G3 outlier anchor, and `TAXONOMY.md`'s own worked example** (`ALGO+ARCH`,
  `Q-ORIENTED`, `ADAPTIVE`+`INT4`, `G3`). The close read supports that placement.
- **Three currencies for outlier handling** — see Conclusions. OliVe (destroyed neighbour) /
  [`Oaken`](../Oaken/ANALYSIS.md) (extra bits + metadata) / [`OASIS`](../OASIS/ANALYSIS.md)
  (high precision). [`OLAccel`](../OLAccel/ANALYSIS.md) and
  [`MicroScopiQ`](../MicroScopiQ/ANALYSIS.md) still to place on that axis.
- **It is a baseline in three corpus entries and loses in all three**:
  [`TransitiveArray`](../TransitiveArray/ANALYSIS.md) (7.46× speedup over it, and argues its
  "mixed-precision advantage disappears on LLMs" because of "larger overhead from their complex
  PEs"), [`Tender`](../Tender/ANALYSIS.md) (beats it at both INT8 and INT4 perplexity),
  and by citation in later LUT work. **Note the direct contradiction**: OliVe's whole claim is
  *low* hardware overhead (2.2 % of core area), and TransitiveArray attacks it for *complex
  PEs*. Both are defensible — OliVe's decoder is tiny, but its PE must handle an exponent path
  the pure-integer designs do not. Worth stating as a genuine disagreement rather than picking
  a side.
- **Depends on [`ANT`](../../../QuantArchSurvey/TAXONOMY.md) (MICRO'22) for `flint4`** — a
  non-corpus paper that is load-bearing here, as in TransitiveArray and Tender. Fifth entry
  leaning on ANT.
- **Contrast with [`Tender`](../Tender/ANALYSIS.md)**: both keep memory aligned and avoid
  sparse encoding, but Tender changes *only grouping and a shift* while OliVe changes *the
  encoding*. Tender's own results beat OliVe's at both precisions — the restraint pays.

## For the note

### §1 one-line summary

> Steals one codepoint from a 4-bit integer type to mark "my neighbour is an outlier", prunes
> that neighbour to zero to free its 4 bits, and stores the outlier there as an **adaptive-bias
> 4-bit float whose exponent bias places its range complementary to the normal type's** — so
> outliers are handled with **no index, no sparse list, no second datapath and no extra bits**,
> at a flat byte-aligned 4-bit format that drops into a GPU tensor core or systolic array for
> ~2 % of core area.

### Proposed values on their four axes

| Axis | Proposed | Evidence (one line) |
|---|---|---|
| **Level** | **`ALGO+ARCH`** | OVP encoding, abfloat and the MSE threshold search are the algorithm; the decoder and its tensor-core / systolic-array integration are the architecture. Matches the taxonomy's worked example. |
| **Q-oriented** | `Q-ORIENTED` | The entire design is an encoding plus its decoder; swap in plain INT8 and nothing remains. |
| **Data type** | **`ADAPTIVE` + `INT4` + `INT8` + `FP4` + `MIXED`** | Normal values int4/flint4/int8; outliers a 4-bit E2M1 float with adaptive exponent bias (`ADAPTIVE`, and `FP4` is literally what abfloat is). The taxonomy's worked example says `ADAPTIVE`+`INT4`; adding `FP4` makes the outlier type explicit. |
| **Generation** | **`G3`** | Outlier thread, thread 1 of G3, and the architecture-side anchor the taxonomy names. Motivated directly by the >6B outlier threshold. |
| **Optimization** (free text) | `outlier-victim pair` `outlier-aware` `abfloat` `adaptive-bias-float` `memory-aligned-encoding` `local-decoding` `tensor-core-integration` `systolic` `pruning` | — |

### Proposed venue-list row

```
| [x] | [OliVe: Accelerating Large Language Models via Hardware-friendly Outlier-Victim Pair Quantization](https://arxiv.org/abs/2304.07493) | ALGO+ARCH | Q | `ADAPTIVE` `INT4` `FP4` `MIXED` | G3 | `outlier-victim pair` `abfloat` `memory-aligned-encoding` `local-decoding` | Prunes an outlier's neighbour to free 4 bits for it, marked by a stolen codepoint — no index, no sparse list, flat byte-aligned 4-bit. Outliers cost a destroyed neighbour, not extra bits |
```

### §4 fairness verdict

**Iso-area on the accelerator side and honest about overhead; the baselines are the weak
point, and the evaluation never reaches the models the paper is about.**

- **Iso-area ✓ (accelerator)** — *"we implement all accelerators with a similar area size"*,
  with other designs scaled to 22 nm via DeepScaleTool. Area overhead is reported precisely
  (2.2 % / 1.5 % of core) rather than waved at.
- **Iso-accuracy ~** — the accelerator comparison states all designs reach "close to original
  accuracy", but ANT gets there only by falling back to int8 on **80 % of layers**, so part of
  the speedup measures ANT's fallback rather than OliVe's encoding.
- **The GOBO comparison is not an outlier-mechanism comparison.** GOBO is **weight-only,
  computing in FP16**; OliVe is W4A4. Most of the 4.5× is that difference, not the encoding.
- **Model scale ✗ — the real limitation.** The paper argues from OPT-175B and evaluates nothing
  above **7B**, with **no LLaMA**. Its G3 anchor status rests on models a generation smaller
  than the ones later corpus entries use to beat it.
- **Evidence levels** — GPU numbers from GPGPU-Sim/AccelSim, accelerator numbers from a
  DnnWeaver-based simulator, area from 22 nm synthesis (scaled to 12 nm for the GPU die claim).
  Three different kinds of fact; do not pool.
- **Best number to cite is not a speedup**: plain int8 gives **74.30** C4 perplexity on
  OPT-6.7B against FP32's **10.63**, and 8-bit OliVe gives **10.73**. That is the cleanest
  demonstration of the 6B outlier threshold in the corpus.

## Abstract (verbatim, arXiv:2304.07493v1)

> Transformer-based large language models (LLMs) have achieved great success with the
> growing model size. LLMs' size grows by $240\times$ every two years, which outpaces the
> hardware progress and makes model inference increasingly costly. Model quantization is a
> promising approach to mitigate the widening gap between LLM size and hardware capacity.
> However, the existence of outliers, values with significant magnitudes, in LLMs makes
> existing quantization methods less effective. Prior outlier-aware quantization schemes
> adopt sparsity encoding techniques to separate outliers from normal values where the
> process requires global coordination (e.g., a global sparsity coordination list). This
> incurs complex encoding/decoding hardware logics and an extra orchestration controller for
> the computation between outlier and normal values. As such, it is not hardware-efficient
> and hence only achieves sub-optimal quantization benefits. We propose OliVe, an
> algorithm/architecture co-designed solution that adopts an outlier-victim pair (OVP)
> quantization and handles outlier values locally with low hardware overheads and high
> performance gains. The key insight of OliVe is that outliers are important while the
> normal values next to them are not. Thus those normal values (called victims) can be
> sacrificed to accommodate outliers. This enables a memory-aligned OVP encoding scheme,
> which can be efficiently integrated to the existing hardware accelerators like systolic
> array and tensor core. As a result, OliVe-based accelerator surpasses the existing
> outlier-aware accelerator, GOBO, by 4.5$\times$ speedup and 4.0$\times$ energy reduction,
> respectively, with a superior model accuracy.
