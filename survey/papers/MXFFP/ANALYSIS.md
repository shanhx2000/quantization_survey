# MXFFP — paper notes

**MXFFP: Microscaling Flexible Floating Point Format for Large-Scale AI Model Acceleration**
Sungwoo Kim, Sungbin Kim, Dongho Ha, Hyunwuk Lee, Junsung Kim, Seunghyun Lee, Mingu Jung,
Murali Annavaram, Won Woo Ro
**ISCA 2026** (2026 ACM/IEEE 53rd Annual International Symposium on Computer Architecture),
pp. 2505–2519 ｜ DOI: **10.1109/ISCA66397.2026.00175**
Publication info verified 2026-09-02 from the **official ISCA 2026 proceedings package**
(title, authors, pages, DOI and abstract all read from its `assets/data/data.js`).
Archived here: **the published proceedings PDF** (`506501c505.pdf`, 15 pages) — not a preprint.

Status: **note ready** ｜ Last updated: 2026-09-14
Tags: `new-data-type` `analytical-dtype` `dtype-granularity` `accelerator`
How far it was read: **close read of §I-§V and §VII (abstract, introduction, §II formats, §III
motivation, §IV the format and Algorithm 1, §V the Tensor Core, §VII discussion / prior-work
comparison / ViT / two-config robustness) and of §VI's prose numbers and evaluation
methodology.** Read for mechanism and cost, not circuit detail.

**What was skimmed or could not be resolved** (itemised, per the read-depth rule):
- **§V-B dataflow (Fig. 11, threadgroup/step mapping)** was read for what it costs — two 2 B
  registers per threadgroup — not for correctness of the mapping itself.
- **Every figure-only number had to be recovered from `pdftotext` bar labels**, since the
  proceedings PDF has no figure data. Fig. 22's six-bar groups were reconstructed by
  x-coordinate and then **cross-checked arithmetically** (see the numbers table) — that one is
  safe. **Fig. 13, 14, 15, 16, 17, 18, 19, 21, 24 bar values that the prose does not state are
  not transcribed here.**
- **One internal discrepancy I could not resolve**: §VII-A's "average perplexity degradation is
  only 0.98" at sub-block 4 does not reconcile with Fig. 22's own per-model numbers at the same
  setting (1.25 / 0.02 / 0.12, mean **0.46**). See "Citation hazards". **Verify before citing.**
- The paper's **memory-requirement model is never stated**, so its 47.8% / 29.1% / 9.38% / 0.5%
  memory claims could not be reproduced from bit counts (my derivation gives ~45% / ~28%).

The **cons** in the brief combine the paper's own stated limits with criticisms other entries in
this corpus make of it; where a criticism is another paper's, it is attributed inline.

> The PDF is **not committed** (1.7 MB). It came from the proceedings package a human
> supplied, now archived at [`archieve/ISCA 2026.zip`](../../../archieve/), entry `pdfs/5065-3nexm57sBmVa6MJtFTiSrb/506501c505/506501c505.pdf`.
> **There is no public URL for it** — this is not an arXiv paper. Re-extract with
> `python3 extract.py` → `extracted/` (committed, greppable).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, 2026 row.

---

## Brief

> **What the close read changed (2026-09-14).** The brief was right about the idea and wrong
> about its price: the flexibility is **binary, not free-form** (two presets, E1Mx / E2Mx, one
> bit — not the four-way E3M0/E2M1/E1M2/E0M3 choice the motivation studies), the headline
> **2-5×** is measured **without** sub-blocking at block 32 and still lands ~1.9× above BF16
> perplexity, and "hardware performance comparable to MXFP" is a **runtime** claim only — the
> threadgroup pays **+22.26% area and +21.4% power** (~12% power with per-configuration gating).
> Corrections are marked inline below.

### 1. Motivation

Microscaling floating point (MXFP) groups values into blocks sharing a common exponent,
which shrinks memory and suits hardware. But the trend — **fewer bits, larger blocks** —
creates growing **inter-block** and **intra-block** value diversity: a fixed
exponent/mantissa split must trade range against precision across blocks, and packing more
values per block amplifies variation within one.

### 2. Overview

Stop using one fixed configuration. **MXFFP** assigns exponent and mantissa bits **flexibly,
at both block and sub-block level**, to match each block's (or element's) actual value
distribution. Contributes conversion mechanisms from FP16/BF16 with minimal runtime overhead
and a Tensor-Core-based architecture that interprets the format using **a single
configuration bit per block**.

### 3. Pros and cons

**Pros**

- The one-configuration-bit encoding is what makes the idea cheap enough to be real —
flexibility usually costs metadata, and here it costs almost nothing **in memory**.
*(Close read: at the same block size it is not zero — a block set is **9 B / 256 elements**
against MXFP's 8 B, i.e. **+12.5% metadata**. The metadata *win* only appears at block 256 with
sub-blocks: 2 B / 256 elements, the "4×" of the conclusion.)*
- Attacks both diversity axes (inter- and intra-block) rather than just one, which is why it
can keep larger block sizes usable. *(Close read: confirmed, and sub-blocking is the half that
does the work — Fig. 21's best setting is block 32 with **sub-block 4**, not a large block.)*
- 2–5× perplexity reduction in 4-bit settings across multiple LLMs **at hardware performance
comparable to MXFP** — an accuracy gain that is close to free. *(Close read: free in **latency
and energy** — MXFFP's speedup curve is MXFP's, to within noise — but **not in area or power**:
+22.26% threadgroup area, +21.4% power, ~12% with gating. And a "2-5× perplexity reduction" off
a broken MXFP4 baseline still leaves Llama3-8B at **10.23 vs BF16's 5.50**.)*

**Cons**

- Choosing the per-block configuration is a fitting problem; the paper's MSE comparisons
show it works but the selection cost and its input-dependence deserve scrutiny on a close
read. *(Close read: **resolved, and it is cheap.** Weights are converted **offline** by trying
both presets and keeping the lower MSE — zero runtime cost. Activations use a hardware rule:
count elements at relative exponent 0 vs {−2,−3} and compare `count_E1² > count_E2`. That rule
is four blocks in the converter (Max / Subtractor / Counter / Config Selector) for **+4.3% area
and +9.6% power on the converter**. The real cost is not selection, it is the **+26.4% area on
the dot-product unit** to widen the significand to an internal E2M2.)*
- Benefit is largest exactly where MXFP is weakest (4-bit, large blocks); at more generous
settings the margin should shrink.
- Still within the exponent/mantissa family — a flexible reallocation of fields rather than
a departure from the analytical form. *(Close read: and the reallocation is **one bit wide**.
Only E1Mx and E2Mx are implemented; the paper defends this with a 97.2% coverage measurement.)*
- **Added by the close read:** **no outlier mechanism of any kind.** The word "outlier" appears
in this paper only in the §II background and the bibliography. MXFFP's answer to outliers is
whatever the MX shared exponent already gave you.
- **Added by the close read:** **only the prefill stage is evaluated.** Every latency and energy
number is prefill (seq 1024, batch 1-8). A format whose case is memory footprint is never
measured in the memory-bound phase.

### 4. Where it applies

The purest **§1.2 new-analytical-data-type** entry in the corpus, and directly relevant to
the microscaling/NVFP4 direction the industry is moving in. Read with
[`MicroScopiQ`](../MicroScopiQ/ANALYSIS.md), which combines microscaling with outlier
handling instead of with field flexibility — and which is a **direct baseline here** (Fig. 22).

---

## Conclusions

**The finding worth carrying out of this paper is not the format — it is the measurement in
Fig. 5.** Once a block has been normalised by an 8-bit shared exponent, its elements need
**one or two exponent bits**, at every bit-width tested. §VII-D quantifies it: E1M*x* and E2M*x*
account for **97.2%** of the lowest-MSE selections across all models and layers; everything else
takes 2.8% **verified** (§VII-D). That is a direct empirical rebuke of OCP MXFP8's own
E5M2/E4M3 choice — five or four exponent bits inside a block that already has a shared
exponent are mostly wasted. MXFFP8 is therefore **E1M6 / E2M5**, not a variant of E5M2
**verified** (§IV-A, which selects E1M*x*/E2M*x* "across all bit-widths (4, 6, and 8 bits)").
The survey should carry this as "the shared exponent already bought the dynamic range; spend
the element bits on mantissa."

**The second finding is structural, and the paper states it itself.** §VIII, verbatim: prior
microscaling work "still manage[s] scale assignment and representation selection within the
same structural unit. Consequently, they cannot independently tune scaling granularity and bit
configuration granularity... **MXFFP overcomes this limitation by decoupling the two
granularities**." **verified**. That is a new axis for the survey — *scale* granularity and
*format* granularity are separable, and MXFFP sets them independently (block 32-256 for the
shared exponent, sub-block 4-32 for the exponent/mantissa split).

**The flexibility is one bit wide, and the hardware trick is to collapse it, not to compose
it.** Both presets are mapped by a mux array into a single internal **E2M2** and executed on
one arithmetic core widened by exactly one mantissa bit **verified** (§V-C). Every other
multi-format datapath in the corpus composes (BitFusion, RaPiD, SamsungNPU, EVA, XtraMAC) or
removes the multiplier (UniCore). MXFFP does neither: it makes the two encodings **the same
encoding** before they reach arithmetic.

**What the design does not buy is speed.** MXFFP's speedup and energy curves are MXFP's, to
within reading error — that is the *claim*, not an omission. Every performance number in §VI-D
is an **MXFP4-vs-BF16** number that MXFFP inherits by not spoiling it. Anyone citing "2.7×" or
"2.08×" from this paper is citing 4-bit microscaling, not MXFFP.

---

## Method

**The format** (§IV-A) **verified**. MXFFP = MXFP plus a **1-bit configuration field** per block
(or per sub-block). Block of *N* elements, one **8-bit E8M0 shared exponent** (unchanged from
OCP MX), and the config bit selects between exactly **two** exponent/mantissa presets at the
element bit-width: **E1M2 or E2M1** at 4 bits, and the corresponding **E1M*x* / E2M*x*** at 6
and 8 bits. The four-way space (E0M3/E1M2/E2M1/E3M0) that §III-B motivates with is **not**
implemented; two presets are, and §VII-D defends the choice at 97.2% coverage. §VII-D also
notes MXFFP "can adopt an alternative pair of presets, such as E0/E2 or E2/E3" or widen the
selector to more than two configurations "at the cost of higher area/power and design
complexity" **verified**.

**Memory layout** (§IV-A, Fig. 10) **verified**. A 1-bit field is not byte-addressable, so eight
config bits are packed into a **1-byte configuration set**:
- **Block set** — 8 blocks × 32 elements: **9 B of metadata per 256 elements** (1 B config +
  8 B shared exponents).
- **Large block** — 1 block of 256 elements with **8 sub-blocks of 32**: **2 B per 256 elements**
  (1 B config + **one** shared exponent). All sub-blocks share the single shared exponent; only
  the E/M split varies within the block.

**Sub-blocking is the accuracy mechanism, and it is independent of block size** (§IV-A, §VII-A).
The sub-block is the unit of *configuration*, the block is the unit of *scale*. §VII-A varies
the sub-block down to **4 elements inside a block of 32**.

**Weight conversion — offline, exhaustive, calibration-free** (§IV-B) **verified**. "Since the
weights of ML mod[e]ls are known in advance, we perform static offline conversion... Each block
(or sub-block) is quantized under both E1M*x* and E2M*x* configurations, and the one that yields
a smaller quantization error (e.g., lower MSE) is selected as the oracle format... without
incurring any runtime overhead." Two presets means the "search" is two evaluations. **No
calibration set is used or mentioned anywhere in the paper** (grep: `calibrat` = 0 hits).

**Activation conversion — a counting rule, in hardware** (§IV-B, Algorithm 1) **verified**.
Per block: take each element's exponent `E_i`, find the block max `E_b^MAX`, form the **relative
exponent** `E_i^r = E_i − E_b^MAX` (always ≤ 0). Then, for MXFFP4:

```
count_E1 = |{ E_i^r = 0 }|              (E1M2 favours these)
count_E2 = |{ E_i^r ∈ {−2, −3} }|       (E2M1 favours these)
Config   = E1Mx  if  count_E1²  >  count_E2 ,  else  E2Mx
```

The square is deliberate — "Because `E_i^r = 0` elements carry larger magnitudes and dominate
numerical fidelity, we apply quadratic weighting." Table I is the justification: at `E_i^r = 0`
E1M2 represents `2¹×1.xx` against E2M1's `2²×1.x`, so E1M2 wins; at `E_i^r ∈ {−2,−3}` E2M1 wins;
at −1 and −4 they tie.

**The shared exponent depends on the configuration, so it is chosen after it** (§IV-B, §V-E)
**verified**. `E_b^shared = E_b^MAX − E_element^MAX`, with `E_element^MAX = 1` for E1M*x* and
`2` for E2M*x*. For a large block whose sub-blocks disagree, **one** shared exponent is stored,
computed as if every sub-block were E2M*x*; E1M*x* sub-blocks **subtract one** from it when it is
used. That is the whole cost of letting sub-blocks disagree.

**Bit mapper — the datapath trick** (§V-C, Fig. 12(b)) **verified**. A "compact multiplexer
array" reinterprets each 4-bit word by its config bit into a single internal **E2M2**: E1M2
routes its one exponent bit into the low exponent position and both mantissa bits through
(`S 0 E MM`); E2M1 forwards both exponent bits and appends a zero mantissa bit (`S E E M 0`).
The FP4 (E2M1) arithmetic core is then "minimally extended to support an internal E2M2 format.
Specifically, **one additional mantissa bit is added to the significand path**. The
corresponding normalization unit is widened... while exponent biasing and range handling remain
unchanged."

**Converter — the runtime rule in silicon** (§V-D, Fig. 12(c)) **verified**. Four blocks in
sequence: **Max** (`E_b^MAX` over 32 elements) → **Subtractor** (`E_i^r`) → **Counter** (counts
of each `E_i^r`) → **Config Selector** (`×`, `+`, `>` — i.e. the `count_E1² > count_E2` test) →
**Normalize & Round**. The paper notes Max and Normalize & Round "are already employed in the
baseline MXFP design", so only the Subtractor / Counter / Config Selector are new.

**Tensor Core integration** (§V-B) **verified**. A 16×16 output tile is split into eight 4×8
submatrices over four steps; each threadgroup holds a **2 B configuration register** (the whole
block set's config byte, loaded once and held across the four steps) and a **2 B shared-exponent
register** (reloaded each step). Accumulation is unchanged MX semantics: each element is scaled
by its block's shared exponent before accumulation.

**Accumulator** (§V-C) **verified**, and stated only in passing: "Accumulated results are stored
in **high-precision accumulators (e.g., FP16 or BF16)**, ensuring numerical stability across the
full dot-product sequence." No width analysis, no area attribution for the accumulator. The
converter's own output is drawn in Fig. 12(b)-(c) as a 16-bit `S E×8 M×7` word.

---

## Key numbers, with their frame

**Evidence levels — three, and they must not be pooled.**
1. **Numerical accuracy**: PyTorch-level quantization, **post-training**, WikiText-2 perplexity
   and three zero-shot tasks; MXFP converted "following the OCP-compliant conversion rule";
   "**all tensors involved in MMA operations** during LLM inference are converted to MX formats"
   (§VI-A) **verified** → this is **W4A4** at 4 bits, confirmed independently in §VII-B.
2. **Performance / energy**: **Accel-Sim** configured from an **NVIDIA RTX 5090**, GEMM kernels
   and instruction traces from **CUTLASS**, energy from **AccelWattch** with synthesis-derived
   power. Metadata traffic for shared exponents and config bits is explicitly modelled (§VI-A)
   **verified**. **Simulator, not silicon, not a real GPU.**
3. **Area / power**: RTL of "a representative 4-bit low-bit datapath" and its MXFFP extension,
   **Synopsys Design Compiler, FreePDK 45 nm** (§VI-A) **verified**. Not a Tensor Core; the
   authors say so.

**Unless a row says otherwise, MXFFP is at block size 32 with no sub-blocking** — the setting
of Fig. 13/14 and of the abstract's 2-5×.

| Setting | Model | Metric | Baseline | Result | Source |
|---|---|---|---|---|---|
| **4-bit, block 32, PTQ, W4A4** | Llama3-8B | WikiText-2 PPL | MXFP4 (E2M1) **30.98**; BF16 **5.50** | **10.23** (3.03× lower than MXFP4; **1.86× worse than BF16**) | §VI-B prose **verified**; BF16 5.50 from Fig. 22 |
| 4-bit, block 32 | OPT-6.7B | PPL | MXFP4 **88.81** | **16.32** (5.44×) | §VI-B **verified** |
| 4-bit, block 32 | Qwen2.5-14B | PPL | MXFP4 **15.90** | **6.93** (2.29×) | §VI-B **verified** |
| 4-bit, block 32 | Vicuna-13B | PPL | MXFP4 **38.13** | **13.31** (2.86×) | §VI-B **verified** |
| **The headline** | 7 LLMs | "reducing perplexity by **2-5×** in 4-bit settings" | MXFP4 | the four rows above are the whole basis; OPT is **5.44×**, i.e. above the stated range | abstract, §IX **verified** |
| 8-bit, block 32 | Llama3-8B | PPL | MXFP8 **E4M3 5.55** | **5.50** (−0.05) | §VI-B **verified** |
| 8-bit, block 32 | OPT-6.7B | PPL | MXFP8 **10.12** | **9.89** (−0.23) | §VI-B **verified** |
| 4-bit zero-shot | 7 LLMs, avg | ARC-e / ARC-c / Lambada drop vs BF16 | MXFP4 drops **18.9% / 24.9% / 28.6%** | MXFFP4 **+16-29%** over MXFP4; **still 5-12% below BF16** | §VI-B **verified** |
| 4-bit zero-shot | Qwen2.5-14B, Vicuna-13B | same | MXFP4 **5.4% / 3.5% / 10.7%** | MXFFP4 **3.5% / 3.3% / 7.0%** | §VI-B **verified** |
| **Block scalability**, 4-bit, sub-block 32 | Llama3-8B | PPL at block **32 / 64 / 128 / 256** | MXFP4 at block 32 = **30.98** | **10.2 / 13.5 / 16.81 / 24.3** | §VI-C **verified**. Note MXFFP **degrades 2.4× across the range**; the claim is only that 24.3 &lt; 30.98 |
| **Sub-block ablation**, 4-bit, block 32 | Llama3 / Mistral / Deepseek | avg PPL degradation vs BF16 at **sub-block 4** | MXFP4 degradations **25.48 / 24.05 / 17.89** | paper states **0.98** — but Fig. 22 gives **1.25 / 0.02 / 0.12**, mean **0.46**. **Unresolved; see hazards** | §VII-A **verified as a quote**, **not reproducible** |
| Memory, sub-block 4 | — | memory requirement | MXFP8 / MXFP6 | **47.8% / 29.1% lower** (my bit-count derivation gives ~45% / ~28%; the paper's memory model is not stated) | §VII-A **verified as a quote**; derivation **inferred / not verified** |
| **Vs prior work**, 4-bit, block 32, sub-block 4 | Llama3-8B | PPL | BF16 5.50 · M-ANT **6.92** · BitMoD **6.54** (W4A8) · **MicroScopiQ 6.80** · MX+ **8.09** | MXFFP **6.75** — **loses to BitMoD** | Fig. 22 **verified** (bar labels recovered by x-coordinate; see hazards) |
| Vs prior work | Mistral-7B | PPL | BF16 4.31 · M-ANT 5.09 · BitMoD 5.29 · MicroScopiQ 4.75 · MX+ 5.02 | MXFFP **4.33** — best | Fig. 22 **verified** |
| Vs prior work | Deepseek-7B-chat | PPL | BF16 6.79 · M-ANT 7.78 · BitMoD 7.81 · MicroScopiQ 7.54 · MX+ 8.15 | MXFFP **6.91** — best | Fig. 22 **verified** |
| Vs prior work, memory | 3 models | memory requirement | BitMoD (W4A8) / MicroScopiQ (W4A4) | **9.38% less** than BitMoD; **0.5% more** than MicroScopiQ for **0.36 lower avg PPL** | §VII-B **verified** — and the 0.36 recomputes exactly from the three bars (0.05+0.42+0.63)/3 = 0.367 |
| **GEMM speedup** | 1024×1024×1024 | vs **BF16** | MXFP | **up to 2.7×** at 4-bit; **1.8×** at 8/6-bit. **MXFFP ≈ MXFP** — "no measurable latency overhead" | §VI-D, Fig. 16 **verified**. This is an **MXFP number MXFFP does not spoil** |
| **End-to-end, prefill only** | 7 LLMs, 1024 input tokens | vs BF16 | MXFP | **1.55×** at 8/6-bit, **2.08×** at 4-bit (avg); **2.18×** at 4-bit for larger models | §VI-D, Fig. 17 **verified**. **Decode is never evaluated** |
| Batch sensitivity, prefill, seq 1024 | Llama3-8B, batch 1/2/4/8 | vs BF16 | — | 8/6-bit **1.47-1.60×**; 4-bit **1.86-2.18×** | §VI-D, Fig. 18 **verified** |
| **Energy** | 1024³ GEMM, 4-bit | vs BF16 | MXFP | **0.35×** of BF16; MXFFP "nearly identical" to MXFP across all sizes and precisions | §VI-D, Fig. 19 **verified** (AccelWattch) |
| **Area** | one threadgroup | vs a 4-bit baseline datapath | own RTL, FreePDK **45 nm** | dot-product **+26.4%**, converter **+4.3%**, bit mapper negligible → **+22.26%** for the threadgroup (4 dot-product units, 1 converter, 16 bit mappers) | §VI-D **verified** |
| Area, system-level | 192 Tensor Cores, 750 mm² die | share of die | — | **0.038%** | §VI-D **verified** — but 45 nm cells dropped into a 4 nm-class die budget; see hazards |
| **Power** | one threadgroup | same | same | dot-product **+24.4%**, converter **+9.6%** → **+21.4%**; **~12%** with per-configuration power gating (>86% of dot-product power is dynamic) | §VI-D **verified** |
| **Two-preset robustness** | all models and layers | share of lowest-MSE selections | — | **E1M*x* + E2M*x* = 97.2%**; all others **2.8%** | §VII-D, Fig. 25 **verified** |
| Metadata, motivating figure | Llama3-405B | MXFP metadata footprint, block 32 → 256 | — | **11.7 GB → 1.46 GB** | §III-D **verified**. This is **MXFP's** number, not MXFFP's |
| **Metadata claim** | — | "reducing metadata overhead by up to **4×**" | MXFP block 32 = **8 B / 256 elements** | MXFFP block 256 + sub-block 32 = **2 B / 256 elements** | §IX + Fig. 10 **verified**; the 8→2 reading is **inferred** but is the only one that gives 4× |
| **ViT (non-LLM)** | ViT-base / ViT-large | Top-1, 4-bit | MXFP4 **76.46% / 79.54%**; BF16 **81.24% / 82.66%** | **79.36% / 81.36%** | §VII-C **verified** (BF16 values from Fig. 24 labels) |

**Derived effective bit-widths** (mine, **inferred / not verified** — the paper never states one):

| Configuration | b/element | vs MXFP4 (4.25) |
|---|---|---|
| MXFP4, block 32 | 4 + 8/32 = **4.25** | — |
| MXFFP4, block 32, no sub-block | 4 + 8/32 + 1/32 = **4.28** | **+0.7%** |
| MXFFP4, block 32, **sub-block 4** (the best-accuracy setting) | 4 + 8/32 + 1/4 = **4.50** | **+5.9%** |
| MXFFP4, block 256, sub-block 32 (the 4×-metadata setting) | 4 + 8/256 + 8/256 = **4.06** | **−4.4%** |

---

## Cost and requirements

| | |
|---|---|
| **Formats** | **W4A4** at 4 bits — "all tensors involved in MMA operations... are converted to MX formats" (§VI-A), confirmed as W4A4 in §VII-B. Also evaluated at 6 and 8 bits (W6A6 / W8A8 by the same statement) |
| **Element encoding** | 1 sign + **E1M*x* or E2M*x***, chosen per block/sub-block. At 4 bits: **E1M2 / E2M1**. At 8 bits this is **E1M6 / E2M5**, *not* OCP's E5M2/E4M3 |
| **Scale** | **8-bit E8M0 shared exponent**, one per block (32-256 elements). Unchanged from OCP MX |
| **Config metadata** | **1 bit per block or per sub-block**, packed 8-to-a-byte into a "configuration set" for byte addressability |
| **Two granularities, set independently** | scale granularity = block (32/64/128/256); format granularity = sub-block (4/8/16/32). This decoupling is the paper's own framing of its contribution (§VIII) |
| **Outliers** | **None.** No outlier path, no second precision, no victim, no sparse list, no permutation metadata. The word "outlier" appears in this paper only in §II background and the bibliography (**verified by grep**, 8 hits, all background or references). MXFFP's answer to outliers is the MX shared exponent, inherited |
| **Escape hatch** | (i) **Accumulators FP16/BF16** (§V-C); (ii) **non-GEMM operations stay on the BF16 baseline path** — stated as the reason end-to-end speedup (2.08×) is below GEMM speedup (2.7×) (§VI-D); (iii) the internal compute format is **E2M2 (5 bits)**, wider than either stored 4-bit encoding |
| **Accumulator** | FP16 or BF16, named once and never analysed. **Not costed** — the 45 nm area/power model is of "a representative 4-bit low-bit datapath", and whether the accumulator is inside it is not stated. **Treat the +22.26% as excluding accumulator cost until checked** |
| **Retraining** | **PTQ, and calibration-free.** Weights converted offline by trying both presets; activations by a hardware counting rule. No calibration set, no fine-tuning, no QAT anywhere in the paper (**verified by grep**: `QAT` 0, `retrain` 0, `calibrat` 0) |
| **Hardware added** | Per threadgroup: 16 **bit mappers** (mux arrays), **+1 mantissa bit** in each of 4 dot-product significand paths with a widened normalizer, **1 converter** extended with Subtractor + Counter + Config Selector, and **2 B + 2 B** of registers. **+22.26% area / +21.4% power** on that threadgroup |
| **What it needs from the software side** | An offline weight-conversion pass. No compiler, no ISA extension, no kernel work is claimed — CUTLASS is used only to generate traces |

---

## Limitations and open questions

**Admitted.**
- Gains at 8 and 6 bits are small "since MXFP already approaches BF16 level accuracy, leaving
  limited room for further gains" (§VI-B) **verified**. The paper is a 4-bit paper.
- Only two presets are implemented; §VII-D admits more would cost "higher area/power and design
  complexity", and offers alternative preset pairs (E0/E2, E2/E3) as future flexibility.
- The 45 nm area model "likely overestimates the overhead of a full Tensor Core, as it excludes
  other hardware components (e.g., pipeline registers, operand buffers, and multi-precision
  units) that would enlarge the baseline area and power" (§VI-D) **verified**.
- "Since NVIDIA Tensor Core microarchitecture details are not publicly available, we model a
  representative 4-bit low-bit datapath" (§VI-D) **verified**.

**Unadmitted, and material.**
1. **The paper calls the dot-product extension "negligible" in §V-C and measures it at +26.4%
   area / +24.4% power in §VI-D.** Both sentences are in the paper; only the second is a number.
   The word "negligible" is only defensible at the **0.038%-of-die** level, which is a different
   claim.
2. **MXFFP4 at its headline setting is still ~1.9× BF16 perplexity.** 10.23 vs 5.50 on
   Llama3-8B. The usable operating point is **sub-block 4** (6.75), which the abstract does not
   mention and which costs **5.9% more bits than MXFP4**.
3. **The 2-5× accuracy claim and the 4× metadata claim are at different operating points** and
   cannot be combined. 2-5× is block 32 (where MXFFP costs 9 B/256 elements against MXFP's 8 B —
   **12.5% more** metadata); 4× is block 256 + sub-block 32, where Llama3-8B perplexity is
   **24.3**.
4. **Decode is never evaluated.** Every latency and energy number is **prefill**, seq 1024,
   batch 1-8 (**verified by grep**: `decode` appears once in the paper, in a reference title).
   A block-scaled 4-bit format's strongest argument is memory-bound decode, and that regime is
   absent.
5. **The comparison with prior work (Fig. 22) is accuracy and memory only.** M-ANT, BitMoD,
   MicroScopiQ and MX+ are all *accelerator* papers; MXFFP compares no area, no power, no
   latency against any of them — only against MXFP. How the four baselines' perplexities were
   obtained (re-run or quoted) is not stated.
6. **The gap to the paper's own oracle is not discussed.** §III-D's oracle-SB reaches **8.5 and
   9.0** at block 64 and 256; MXFFP delivers **13.5 and 24.3** at the same block sizes
   (sub-block 32). The motivation's ceiling and the design's floor are 1.6× and 2.7× apart, and
   §VI-C does not mention it.
7. **The counting rule's thresholds are hand-derived from Table I for MXFFP4 and asserted to
   generalise.** "[W]hile the exact thresholds differ for MXFFP6 and MXFFP8, the overall trend
   remains the same" (§IV-B) — the 6- and 8-bit thresholds are never given.
8. **Accumulator width is named and dropped**, as in most of this corpus.

**Open questions for the survey.**
- Is E1M6/E2M5 really better than E4M3 at 8 bits *for training or for long-context inference*,
  or only for the WikiText-2 perplexity of a normalised block? Fig. 5 measures per-block MSE,
  not tail behaviour.
- Does the config bit survive **MoE and attention** tensors, whose distributions differ from the
  projection weights Fig. 5 characterises? The paper measures Llama3-8B layer 9 query projection
  and ViT-base, nothing else.
- With no outlier mechanism at all, what happens at **W4A4 on models with strong activation
  outliers** (the OliVe/MicroScopiQ motivating case)? Llama3-8B at 10.23 may be that answer.

---

## Relation to other entries

**Microscaling is now a two-entry family in this corpus, and the two entries spend their bits in
opposite places.** [`MicroScopiQ`](../MicroScopiQ/ANALYSIS.md) (ISCA'25) keeps MX-INT inliers and
promotes outliers to MX-FP at 2× the bit-width, paying with a **pruned neighbour plus a 24-bit
permutation list per outlier-bearing micro-block** — EBW 2.36 at `bb`=2. MXFFP keeps every
element at the same width and spends **one bit per block** moving the exponent/mantissa boundary
— EBW 4.28. Same base format, opposite theory of what MXFP gets wrong: MicroScopiQ says *the
block contains values that do not belong*; MXFFP says *the block's field split is in the wrong
place*. They meet in Fig. 22, where MXFFP is 0.36 PPL better on average for 0.5% more memory —
though MXFFP evaluates MicroScopiQ at **W4A4**, whereas MicroScopiQ's own headline (&lt;1% drop)
is **W4A16**, so that row is not MicroScopiQ's best case.

**It adds an axis the survey does not yet have: scale granularity ≠ format granularity.** The
existing granularity spine — per-layer (BitFusion, OLAccel) → per-region (DRQ) → per-channel
(Tender) → per-group (Oaken, MicroScopiQ) → per-head (P3-LLM) → per-token (LightNobel) →
per-rank (SingularBit) — measures **one** granularity, the scale's. MXFFP sets two independently
and says so in §VIII. That is the cleanest statement of the idea available, and it is the
paper's own.

**It is the corpus's counter-example on the outlier axis.** The "outlier currency" list —
extra bits (OLAccel, Oaken), a destroyed neighbour (OliVe, MicroScopiQ), a second datapath
(OASIS), compressibility (Ecco), a top-k budget (LightNobel), sign balance (RAELLA) — should
gain a null row: **MXFFP pays nothing and has no outlier concept**, and reaches 6.75 PPL on
Llama3-8B W4A4 where MicroScopiQ reaches 6.80. Whatever the shared exponent plus a movable field
boundary is doing, it is doing most of what an outlier mechanism does at this granularity. That
is a load-bearing negative result for the survey's outlier section.

**It is *not* in the multi-precision-datapath thread, and the contrast sharpens that thread.**
BitFusion (spatial) → RaPiD (split pipelines) → SamsungNPU / EVA (temporal) → XtraMAC (DSP
bit-space) → UniCore (adder slices) all answer *how do I make one datapath span several
bit-widths*. MXFFP has **one** bit-width and two encodings, and answers a different question by
**collapsing both encodings into one internal E2M2 before arithmetic** — a mux array plus one
mantissa bit. "Unify by widening, not by composing" is a fifth strategy, and it is available
only because the formats differ in field split rather than in width. The substrate rule holds:
the GPU Tensor Core charges for *utilization of a single-format arithmetic core*, so the design
buys that back first.

**On `ADAPTIVE`, it is the strongest case in the corpus.** The corpus already distinguishes
`ADAPTIVE`-as-format-property ([`RAELLA`](../RAELLA/ANALYSIS.md)'s slice width,
[`UniCore`](../UniCore/ANALYSIS.md)'s DynFP, [`OliVe`](../OliVe/ANALYSIS.md)'s abfloat bias) from
`ADAPTIVE`-as-selection-policy ([`LightNobel`](../LightNobel/ANALYSIS.md), where the note argues
it belongs in Optimization). MXFFP is unambiguously the first kind: **the adaptation is a field
of the stored datum**, one bit, byte-packed and decoded by the bit mapper. Nothing about the
runtime is needed to know what a stored MXFFP block means.

**Node and evidence company.** FreePDK **45 nm** puts it with [`BitFusion`](../BitFusion/ANALYSIS.md)
(45 nm) and apart from the 28 nm cluster (Tender, Oaken, EVA, UniCore) and MicroScopiQ's 7 nm.
Its performance evidence is a **GPU simulator (Accel-Sim + AccelWattch)** — the same class as
[`OliVe`](../OliVe/ANALYSIS.md)'s GPGPU-Sim/AccelSim numbers, and weaker than
[`RaPiD`](../RaPiD/ANALYSIS.md)'s silicon or [`SamsungNPU`](../SamsungNPU/ANALYSIS.md)'s measured
13.6 TOPS/W.

**Baselines it names that the corpus does not hold.** M-ANT (HPCA'25), BitMoD (HPCA'25), MX+
(MICRO'25), and Avant-Garde (ISCA'25, whose author list overlaps this one) are all cited here;
only BitMoD and M-ANT appear anywhere else in the corpus, and only as other papers' baselines.
**MX+ and Avant-Garde are gaps** — MX+ is the direct microscaling competitor and MXFFP beats it
by the widest margin of the four.

---

## Citation hazards

1. **"2-5× perplexity reduction" is a ratio between two bad numbers.** The MXFP4 baseline is
   broken (30.98-88.81 perplexity); the MXFFP4 result is 10.23-16.32 against BF16's 5.50-10.86.
   Quote the *absolute* perplexities or the sub-block-4 result (avg degradation 0.46-0.98), not
   the ratio. OPT-6.7B is **5.44×**, outside the stated 2-5× band.
2. **The abstract's accuracy claim and the conclusion's "4× metadata" claim are at different
   operating points** (block 32 vs block 256). At block 32 MXFFP costs **more** metadata than
   MXFP (9 B vs 8 B per 256 elements). Never quote them in one sentence.
3. **Every speed and energy number in this paper is MXFP's.** "2.7× GEMM", "2.08× end-to-end",
   "0.35× energy" are 4-bit-microscaling-vs-BF16 numbers; MXFFP's contribution is that it does
   not lose them. Citing MXFFP for a speedup misattributes it.
4. **"Negligible" (§V-C) vs "+26.4%" (§VI-D)** describe the same dot-product extension. Use the
   number.
5. **The 0.038%-of-die figure crosses nodes.** A **FreePDK 45 nm** synthesis is scaled onto a
   **750 mm² / 192-Tensor-Core** die (RTX 5090 class, 4 nm-family). Not iso-node. The
   threadgroup-level **+22.26% / +21.4%** are the defensible numbers.
6. **Unresolved internal discrepancy.** §VII-A states "with a sub-block size of 4, the average
   perplexity degradation is only **0.98**". Fig. 22, same setting and same three models, gives
   degradations of **1.25 / 0.02 / 0.12** (mean **0.46**). One of the two is measuring something
   else. **Verify before citing either.**
7. **Fig. 22's bar values were recovered from the PDF, not printed in prose.** I assigned them by
   x-coordinate and then checked: the MicroScopiQ delta computes to (0.05+0.42+0.63)/3 = **0.367**
   against the paper's stated **0.36**, so the assignment is right. Anyone re-deriving them
   should repeat that check.
8. **Fig. 22 is not iso-setting across baselines.** BitMoD runs **W4A8**; M-ANT, MicroScopiQ,
   MX+ and MXFFP run **W4A4**. The paper says so, and uses it to explain BitMoD's win on
   Llama3-8B — but the memory comparison then rests on that same asymmetry.
9. **MicroScopiQ appears here at W4A4, not at its own headline W4A16.** Do not read Fig. 22 as
   MicroScopiQ's best result.
10. **The motivation's "oracle" is a four-way exhaustive MSE search; the product is a two-way
    heuristic.** Oracle-SB reaches 8.5/9.0 at block 64/256; MXFFP reaches 13.5/24.3. Fig. 8's
    numbers are not MXFFP's.

---

## For the note

### §1 one-line summary

> Keeps OCP MX exactly as it is — same element width, same 8-bit E8M0 shared exponent — and adds
> **one configuration bit** that switches the element between **two exponent/mantissa presets**
> (`E1M2` or `E2M1` at 4 bits), chosen **offline by MSE for weights** and at runtime for
> activations by a **quadratically-weighted counting rule** over relative exponents
> (`count(E_i^r=0)² > count(E_i^r∈{−2,−3})`), with the whole thing collapsed back into a single
> internal **E2M2** by a mux array so the arithmetic core needs only **one extra mantissa bit** —
> buying **2–5× lower perplexity than MXFP4** (10.23 vs 30.98 on Llama3-8B, against BF16's 5.50)
> for **+22.26% threadgroup area** and **0.03 bits/element**, and — because the sub-block sets the
> *format* granularity while the block still sets the *scale* granularity — letting the block grow
> to 256 for **4× less metadata**.

### Proposed values on their four axes

| Axis | Proposed | Evidence (one line) |
|---|---|---|
| **Level** | **`ARCH`** — seed agrees | Datapath only: bit mappers, one extra significand bit, a widened normalizer, the converter's Subtractor/Counter/Config-Selector, 2 B + 2 B of registers. **Checked `SYS` explicitly and it does not apply** — "no compiler, no ISA extension, no kernel work is claimed"; CUTLASS is used only to generate traces, and the offline weight-conversion pass is a script, not a shipped stack |
| **Q-oriented** | **`Q-ORIENTED`** — seed agrees | Swap the format for plain INT8 and *nothing* survives: the config bit has nothing to select, the counting rule has no exponents to count, the bit mapper has no encodings to unify, and the shared exponent is gone |
| **Data type** | **`MX` `FP4` `FP8` `ADAPTIVE` `MIXED`** — *seed has `MX` `FP4` `ADAPTIVE`; `FP8` added by me, `MIXED` added by the human 2026-09-14* | `MX`: OCP-compliant block + E8M0 shared exponent (§IV-A). `FP4`: E1M2/E2M1 (§IV-A). `FP8`: the 8-bit instance is **E1M6 / E2M5**, *not* OCP's E5M2/E4M3 — a distinct format worth its own tag. **`ADAPTIVE` is correct here** and the venue README's line-122 amendment should stand. On **`MIXED`**: I had argued against it — every element is the same width, and what coexists is two *encodings* of one width rather than two precisions. **The human ruled `MIXED` in on 2026-09-14 and it is applied above**; the observation is kept here because it is the distinction between MXFFP's sense of "mixed" and BitFusion/RaPiD/UniCore's |
| **Generation** | **`G2`** — seed agrees | The G2 test — *does the paper design a numeric type?* — is passed outright. **None of the three G3 threads is present**: no outlier concept (grepped: 8 hits, all background/bibliography), no weight-only asymmetry (it is W4A4), no codebook. Evaluated on LLMs, but the *problem* is a format problem, and §VII-C shows it on ViTs |
| **Optimization** (free text) | `microscaling` `flexible exponent/mantissa split` `sub-block configuration` `1-bit config selector` `bit mapper` `quadratic-weighted counting rule` `decoupled scale/format granularity` `tensor core` `PTQ` `calibration-free` | Seed has the first three plus `tensor core`; the counting rule and the granularity decoupling are the two the seed misses, and the second is the paper's own framing of its contribution (§VIII) |

### Proposed venue-list row

```
| [ ] | [MXFFP: Microscaling Flexible Floating Point Format for Large-Scale AI Model Acceleration](https://doi.org/10.1109/ISCA66397.2026.00175) | *close read* | ARCH | Q | `MX` `FP4` `FP8` `ADAPTIVE` `MIXED` | G2 | `microscaling` `flexible exponent/mantissa split` `sub-block configuration` `1-bit config selector` `bit mapper` `quadratic-weighted counting rule` `decoupled scale/format granularity` `tensor core` | One config bit per block/sub-block picks E1Mx or E2Mx; a mux array collapses both into an internal E2M2 so the core needs **one extra mantissa bit**. **Scale granularity (block) and format granularity (sub-block) are set independently** — the corpus's only entry that separates them. Has **no outlier mechanism at all** and still matches MicroScopiQ |
```

*(Changes from the seed at line 27: data type gains `FP8`; `ARCH`, `Q`, `G2` and `ADAPTIVE` all
confirmed. The Note column is rewritten around the granularity decoupling, which the seed's note
does not name.)*

### §4 fairness verdict (note version, 54 words)

> Iso-format-family and iso-block-size vs MXFP; PTQ both sides. **Not iso-node** (FreePDK 45 nm
> synthesis scaled onto a 750 mm² 4 nm-class die); Fig. 22 **not iso-setting** (BitMoD W4A8 vs
> everyone else's W4A4; MicroScopiQ shown off its W4A16 headline). **Not to quote:** 2–5× PPL
> (ratio of two broken numbers); 2.7× / 2.08× / 0.35× are **MXFP's**, not MXFFP's.

## Abstract (verbatim, ISCA 2026 proceedings)

> The rise of AI/ML applications has reignited interest in floating-point formats beyond the
> IEEE 754 standard, leading to innovations such as Microscaling Floating-Point (MXFP). MXFP
> groups values into blocks that share a common exponent, allowing them to be represented as
> scaled FP values. This enables a reduced memory footprint and efficient hardware
> execution. However, due to the trend of shrinking bit-widths and increasing block sizes,
> MXFP faces growing inter-block and intra-block value diversity. The limited number of
> exponent and mantissa bits forces a tradeoff between range and precision across blocks,
> while packing more values into a block amplifies the variation within each block. As a
> result, fewer bits with larger blocks often lead to precision loss and degraded model
> accuracy. In this paper, we observe that these limitations can be addressed by flexibly
> assigning exponent and mantissa bits to match the value distribution of each block or
> element within a block, rather than relying on a single fixed MXFP configuration. Based on
> this observation, we propose MXFFP, a flexible numeric format that leverages diverse
> exponent-mantissa configurations at both the block and sub-block levels. This diversity
> allows MXFFP to better preserve the original value distribution, leading to higher
> inference accuracy for ML models even with larger block sizes. To support this format, we
> introduce efficient conversion mechanisms that transform FP16/BF16 values into MXFFP with
> a minimal runtime overhead and design a Tensor Core based hardware architecture that
> interprets and executes MXFFP using only a single configuration bit per block. Our
> evaluation shows that MXFFP significantly improves numerical accuracy, reducing perplexity
> by 2–5× in 4-bit settings across multiple LLMs, while maintaining hardware performance
> comparable to MXFP.
