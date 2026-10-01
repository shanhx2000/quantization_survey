# UniCore: A Bit-Width Scalable GEMM Unit for Unified LLM Inference

**Venue / Year:** ISCA 2026 · **Link:** https://doi.org/10.1109/ISCA66397.2026.00176 · code https://github.com/CLab-HKUST-GZ/isca53-unicore · **Reader:** Haoxuan · **Date:** 2026-09-14

## Tags

| | |
|---|---|
| **Level** | `ARCH` |
| **Q-oriented** | `Q-ORIENTED` |
| **Data type** | `FP16` `FP8` `FP4` `ADAPTIVE` `MIXED` |
| **Generation** | `G2` |
| **Optimization** | composable FPMA · Mitchell logarithmic approximation · uniform adder slices · linear scaling · dual-path compensation · DynFP · bit-width scalable GEMM |

## 1. One-line summary

Observes that a float's **concatenated exponent–mantissa field is already approximately its
logarithm** (Mitchell: `log₂(1+M) ≈ M`), so floating-point multiplication can be done as **integer
addition** — and builds the first **composable** version of that primitive from **uniform adder
slices**, so fusing to higher precision scales **linearly instead of quadratically**, escaping the
16/4/1-MACs-per-cycle collapse that BitFusion-style composable multipliers suffer; a
subnormal-removal, mantissa-reconstruction and **dual-path compensation** pipeline repairs the
structured approximation error: **1.24×–3.95% area efficiency at W4A4/W4A8/W8A8 and up to 5.26× at
W16A16**.

## 2. Data type

**FPMA — the primitive, not a storage format.** From Mitchell's approximation `log₂(1+M_x) ≈ M_x`: `log₂|x| ≈ E_x + M_x − B`, so `r = x·y` becomes **`R = X + Y`** over the concatenated exponent–mantissa fields. **Integer addition replaces FP multiplication.**
**Storage format is unchanged.** UniCore doesn't store logarithms — it exploits the fact that **IEEE floating point is already approximately logarithmic in its stored bits**. Worth distinguishing from `POW2` / logarithmic number *formats*.
**DynFP** — the one format contribution: configurable low-bit FP that **adapts exponent–mantissa allocation** and **eliminates redundant encodings**, targeted at LLM weight and **K/V** distributions. Applied online with a lightweight conversion.
**Precision range.** W4A4, W4A8, W8A8, W16A16 — the only entry in the thread evaluated at 16-bit, which is where its advantage is largest.
**Approximation error is structural.** Mitchell's approximation is systematically biased, so correctness depends on the compensation pipeline: **subnormal removal → mantissa reconstruction → dual-path fine- and coarse-grained compensation**.
**Requires an exponent–mantissa encoding.** Pure integer formats have no logarithm to read off — this is why UniCore is an **FP** design where the rest of the thread is INT-centric.
**Accumulation.** Not analysed — contrast XtraMAC, which shows accumulation is exactly where format unification fails.
**Retraining.** PTQ; DynFP applied online.

## 3. Optimization

**The diagnosis, in the criticised paper's own numbers.** §II-C: BitFusion-style bit-composable
architectures are "**fundamentally limited by the quadratic O(n²) cost of multipliers**. Because
partial-product generation and accumulation grow with n², the achievable throughput of fused PEs
decreases proportionally to **1/n²**… This **'dynamic tax'** allows good efficiency at 4-bit, but
causes **severe throughput collapse** when switched to 8-bit or 16-bit modes." Figure 3(a) makes it
concrete: **16 MACs/cycle at 4-bit, 4 at 8-bit, 1 at 16-bit** — which is *exactly* BitFusion's own
fusion table (16 / 4 / 1 Fused-PEs). Using the criticised design's own numbers is the strongest
form the critique could take.

**The fix is to stop multiplying.** Adders scale linearly in width where multipliers scale
quadratically, so if multiplication *is* addition, composition costs `O(n)` not `O(n²)`. Figure
3(b): **O(1/n)**. The primitive is changed; the fusion logic is not. That's the whole architectural
argument and it's unusually clean.

**The bill is paid explicitly.** Mitchell's approximation is biased, so the compensation pipeline is
not optional — it's the price of linear scaling, and whether it stays lightweight as precision rises
is the question to ask.

**The win grows with precision, which is the right proof.** 1.24×–3.95× at W4A4/W4A8/W8A8, rising
to **5.26× at W16A16**. A removed quadratic term should show exactly this signature; a design that
beat the baselines uniformly would be less convincing.

## 4. Results

| | |
|---|---|
| Baseline | Composable-multiplier: **OliVe, Tender, M-ANT** (two in this corpus). Fixed-width mixed-precision: **BitMoD, AxCore**. Fixed-precision control: **Synopsys DesignWare IP** and **Tender with composability removed**. All **re-synthesised in UniCore's own flow** |
| Models / datasets | Llama-2-7B/70B, Llama-3-8B, Mistral-7B, Qwen3-8B/14B across W4A4 → W16A16 |
| Accuracy delta | **Highest accuracy in nearly all configurations; lowest perplexity in most.** But this mixes DynFP (a better format) with the compensated datapath — the two aren't separated |
| Speedup | Throughput scaling **O(1/n)** vs composable multipliers' **O(1/n²)** — 16/4/1 MACs per cycle at 4/8/16-bit for the baseline |
| Energy / area | **1.24×–3.95× area efficiency** at W4A4/W4A8/W8A8; **up to 5.26× at W16A16**. **24% smaller GEMM area than Tender even with 16-bit support** |
| Technology node | **TSMC 28 nm, 1 GHz**, SpinalHDL → Synopsys Design Compiler, applied **consistently across all accelerator comparisons** |
| Evidence level | **RTL synthesis** for area/power + an extended simulator for system-level behaviour. No silicon |
| **Is the comparison fair?** | All five baselines — including in-corpus OliVe and Tender — are **re-synthesised in UniCore's own 28 nm flow**, not quoted: strong iso-node discipline, at the node those papers used. But the **compensation pipeline's area is never isolated**, and it is the price of the O(n) claim; and the accuracy advantage **mixes DynFP with the compensated datapath** without separating them |

## 5. Comment

## 6. Claude notes

> **Suggestions from the reading agent. Strip this section before copying into
> `QuantArchSurvey/venues/ISCA/notes/`.**

- **§5 material, if you want it — this is the natural last word in the multi-precision thread, and
  the BitFusion↔UniCore pairing is the cleanest narrative arc the survey has.**

  | Paper | What it composes | Scaling |
  |---|---|---|
  | BitFusion'18 | 2-bit multipliers, spatially | **O(1/n²)** — 16/4/1 |
  | RaPiD'21 | nothing — two separate pipelines | n/a |
  | SamsungNPU'21 / EVA'26 | INT8 multipliers, temporally | 4 cycles for the wide case |
  | XtraMAC'26 | DSP bit-space, spatially | fills a fixed multiplier |
  | **UniCore'26** | **adder slices — no multiplier at all** | **O(1/n)** |

  Five papers argue about *how to compose a multiplier*. UniCore argues you shouldn't have one — and
  quotes BitFusion's own 16/4/1 table as the problem. First and last of the thread, eight years
  apart.
- **UniCore and XtraMAC are a matched pair from opposite substrates**, both ISCA'26, both on
  multi-format GEMM, opposite conclusions. XtraMAC **keeps** the multiplier and fills it (on an FPGA
  the DSP is fixed and you can't redesign it); UniCore **removes** it (on an ASIC you can). The
  substrate explains the disagreement exactly — which is the organising claim I'd draw from the
  whole thread.
- **A distinction worth making where the survey discusses log-domain arithmetic.** `TAXONOMY.md`
  defines `POW2` as a logarithmic number *format*. UniCore changes **no storage format** — it
  exploits the fact that IEEE floating point is *already* approximately logarithmic in its stored
  bits. Same mathematics, different taxonomic place. (Same issue I flagged on Tender's `POW2` tag.)
- **`ADAPTIVE` is doing real work here, unusually.** In most entries `ADAPTIVE` names a *selection
  policy* (and I've recommended moving it to Optimization — e.g. LightNobel). DynFP genuinely adapts
  **exponent–mantissa allocation** and eliminates redundant encodings, so `ADAPTIVE` names a format
  property. Worth keeping, and worth noting the inconsistency across rows.
- **Level is arguable and I kept `ARCH`.** DynFP is a format contribution, which would support
  `ALGO+ARCH`. I kept `ARCH` because DynFP is applied **online with a lightweight conversion** — no
  training, no calibration procedure. Flagging it since you've been tightening Level calls.
- **Two things to watch when citing.** The **compensation pipeline's area is never isolated**, and
  it is what the O(n) claim costs — if it grows with precision, the scaling claim needs qualifying.
  And the accuracy headline **bundles DynFP with the datapath**; an ablation separating them isn't
  offered.
- **FPMA itself is not new** — Mitchell 1962, plus refs [17],[26]. The contribution is its
  *composability*. The abstract states this precisely; secondary framing could blur it.
- **It re-synthesises OliVe and Tender**, two entries we've already read, in its own 28 nm flow.
  Useful if we ever want a cross-checked area number for either.
