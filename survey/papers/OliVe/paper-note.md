# OliVe: Accelerating Large Language Models via Hardware-friendly Outlier-Victim Pair Quantization

**Venue / Year:** ISCA 2023 · **Link:** https://arxiv.org/abs/2304.07493 · **Reader:** Haoxuan · **Date:** 2026-09-09

## Tags

| | |
|---|---|
| **Level** | `ALGO+ARCH` |
| **Q-oriented** | `Q-ORIENTED` |
| **Data type** | `ADAPTIVE` `INT4` `INT8` `FP4` `MIXED` |
| **Generation** | `G3` (outlier thread) |
| **Stage type** | `S2T4` |
| **Optimization** | outlier-aware · outlier-victim pair · abfloat · adaptive-bias float · memory-aligned encoding · local decoding · tensor-core integration · systolic · pruning |

## Stage-type tags

**`S2T4`** (the **Stage type** row in Tags) — most-matched first. The outlier-victim pair gives each outlier its own encoding in its victim's slot. Its abfloat element and the int4/flint4/int8 modes are part of that one mechanism, so no further tags are carried.

*Tag form `S{stage}T{type}`, vocabulary from `survey/stage2.md` and `survey/stage3.md`. Added 2026-10-02 (ISCA Stage-type batch 1).*

## 1. One-line summary

Steals one codepoint from a 4-bit integer type to mark "my neighbour is an outlier", prunes
that neighbour to zero to free its 4 bits, and stores the outlier there as an **adaptive-bias
4-bit float whose exponent bias places its range complementary to the normal type's** — so
outliers need **no index, no sparse list, no second datapath and no extra bits**, at a flat
byte-aligned 4-bit format that drops into a tensor core or systolic array for ~2% of core area.

## 2. Data type

**Formats.** `W4A4` / `W8A8`. Normal values `int4`, `flint4` (ANT's) or `int8`, each with one codepoint stolen as the outlier identifier (`1000₂` = −8 in int4; = −0 in flint4, so **flint4 loses nothing**). Outliers: 4-bit **abfloat E2M1** — fixed-point float, decode is shifts only.
**Granularity.** **Pairwise** — the unit is two adjacent values. No group size, no scale sharing; threshold is per-tensor by MSE minimisation. Finest outlier granularity in the corpus.
**Outliers.** Local substitution: victim holds the identifier, outlier holds the value, direction implicit in *which half* — **no index bit**. Adaptive exponent bias moves abfloat's range complementary to the normal type's (int4 + `bias=2` → `{12…96}`) instead of overlapping it.
**Accumulator.** Not reported. Decoder emits int4 + exponent into the host datapath's existing shift-and-add; GPU path uses the tensor core's INT32 accumulate.
**Escape hatch — the victims, a different currency.** Effective bitwidth is **exactly 4**, byte-aligned, **zero metadata**. What's spent is *information*: every outlier zeroes a neighbour, and in a two-outlier pair **one outlier is destroyed**. **PTQ**, no retraining.

## 3. Optimization

Prior outlier architectures (GOBO, OLAccel, BiScaled, DRQ) separate outliers **globally** —
coordinate list, block-sparse indices, or bitmap. That means unaligned access, encode/decode
logic, an orchestration controller, and incompatibility with existing memory subsystems. GOBO
can only compress weights in DRAM and still computes FP16.

**The observation.** Of the three adjacent-pair types, **two-outlier pairs "almost never show
up"**. And pruning a normal value costs almost nothing: clipping 0.1% of outliers is
disastrous, pruning 0.1% of normals costs **<0.1% accuracy**. So the neighbour is expendable.

**OVP encoding.** Steal one codepoint as the outlier identifier; write it into the victim's
slot. An OV pair is exactly **8 bits, byte-aligned**, decoded entirely locally. Two-outlier
pairs keep the larger and prune the other.

**abfloat.** The bias is the real idea — without it E2M1's range *overlaps* int4's (both
contain 3, 4, 6), so codepoints are wasted re-covering ground. `bias=2` moves E2M1 to
`{12…96}`, complementary to int4; `bias=3` gives `{24…192}` for flint4. Every codepoint buys
range the normal type doesn't already have. E2M1 chosen by measuring rounding error of the
largest outliers across E0M3/E1M2/E2M1/E3M0.

**Threshold search.** MSE minimisation, with the real tension stated: a lower threshold means
more OV pairs and lower MSE but **more two-outlier pairs, where an outlier is destroyed**. The
knob is really "how often may the scheme destroy an outlier".

**Integration.** A lightweight OVP decoder per FEDP in a Turing tensor core, or at the PE in a
systolic array. No datapath redesign either way — 13.53 µm² (4-bit) at 22 nm, **2.2% of
systolic core area**, **0.25% of a 2080 Ti die**.

## 4. Results

| | |
|---|---|
| Baseline | Quantization: GOBO, Outlier Suppression, Q8BERT, ANT. Accelerators: OLAccel, AdaptivFloat, GOBO, ANT, int8 tensor cores |
| Models / datasets | BERT-base/large, BART-base on 8 GLUE tasks + SQuAD v1.1/v2.0; GPT2-XL, BLOOM-7B1, OPT-6.7B on Wikitext103 + C4. **Nothing above 7B; no LLaMA** |
| Accuracy delta | **The headline: plain int8 breaks on OPT-6.7B** — C4 PPL **74.30** vs FP32 **10.63**; 8-bit OliVe **10.73**. 4-bit OliVe on GPT2-XL 19.11/18.08 vs FP32 17.48/16.30 (int4 = 1E+4, 4-bit ANT = 27.79). BERT-like <1% loss |
| Speedup | GPU: **4.5× GOBO, 2.7× int8, 2.4× ANT.** Systolic: **4.8× AdaFloat, 3.8× OLAccel, 3.7× ANT** |
| Energy / area | GPU energy 4.0× / 2.3× / 2.0×; accelerator 3.7× / 2.1× / 3.3×. Decoder 13.53 µm² (4b) / 18.00 µm² (8b) @22 nm → **2.2% / 1.5% of core**, 0.25% of a 754 mm² GPU die |
| Technology node | TSMC 22 nm (decoder RTL); GPU claims scaled to 12 nm |
| Evidence level | **synthesis** (Synopsys DC + CACTI) + **GPGPU-Sim 4.0 / AccelSim** as RTX 2080 Ti + **DnnWeaver cycle-level simulator** for the accelerator. Three kinds; don't pool. No silicon |
| **Is the comparison fair?** | Iso-area ✓ on the accelerator side — *"we implement all accelerators with a similar area size"*, baselines scaled to 22 nm via DeepScaleTool, overhead reported precisely. |

## 5. Comment


## 6. Claude notes

*Suggestions from the reading agent. **Strip this section before copying into
`QuantArchSurvey/venues/ISCA/notes/`.***

**Human verified: no.**

- **Three currencies for outlier handling — a better axis than "outlier-aware yes/no".**
  OliVe pays with a **destroyed neighbour** (flat 4 bits, zero metadata); `Oaken` pays with
  **extra bits + metadata** (5-bit + 8-bit COO → 4.8 effective); `OASIS` pays with **high
  precision** (1% at FP16 on a second datapath). `OLAccel` and `MicroScopiQ` still to place.
  This is the cleanest organizing idea the outlier thread has given us.
- **A genuine contradiction to record, not resolve.** OliVe's whole claim is *low* hardware
  overhead (2.2% of core area); `TransitiveArray` attacks it for *"larger overhead from their
  complex PEs"*. Both are defensible — the decoder is tiny, but the PE must carry an exponent
  path that pure-integer designs don't. Worth stating as a disagreement.
- **The scale gap matters for its anchor status.** The taxonomy makes OliVe *the* G3 outlier
  anchor, but it evaluates nothing above **7B and no LLaMA** — while opening on OPT-175B.
  Every later corpus entry that runs it on LLaMA finds it weaker than this paper implies. Not a
  reason to move the anchor, but the survey should say the anchor's evidence base is pre-LLaMA.
- **Untested assumption worth flagging.** "Two-outlier pairs almost never show up" is asserted
  from BERT / GPT2-XL / OPT-6.7B. If outliers cluster — and the channel-structured-outlier
  literature since suggests they do — the failure mode is *silent destruction of real
  outliers*. No sensitivity study on the two-outlier rate.
- **§5 material, if you want it.** Placement: G3 outlier anchor, §2.2 fine-grained. Best
  citation for: the >6B int8 breakdown (74.30 vs 10.63 on OPT-6.7B), which is sharper than any
  speedup here. Contrast with `Tender`: both keep memory aligned and avoid sparse encoding, but
  Tender changes only grouping and a shift while OliVe changes the encoding — and Tender's own
  numbers beat it at both precisions, so the restraint pays.
- **ANT (MICRO'22) is load-bearing again** — `flint4` comes from it. Fifth corpus entry
  depending on a non-ISCA paper.
