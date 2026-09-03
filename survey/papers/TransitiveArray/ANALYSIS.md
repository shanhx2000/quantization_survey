# TransitiveArray — paper notes

**Transitive Array: An Efficient GEMM Accelerator with Result Reuse**
Cong Guo, Chiyue Wei, Jiaming Tang, Bowen Duan, Song Han, Hai Li, Yiran Chen
(Duke University; MIT)
**ISCA 2025** ｜ DOI: **10.1145/3695053.3731043** ｜ pages **not recorded**
Publication info verified 2026-09-03: **venue and DOI read out of the archived PDF's own
ACM Reference Format block** — *"ISCA '25, June 21–25, 2025, Tokyo, Japan … ACM, New York,
NY, USA, 15 pages. https://doi.org/10.1145/3695053.3731043"* (**verified**).
Archived here: **arXiv:2504.16339v1** (2025-04-23), 15 pages — **the preprint, not the
published ISCA version**; the two were **not compared**.

Status: **analysis ready** ｜ Last updated: 2026-09-03
Tags: `analytical-dtype` `non-analytical-dtype` `mixed-precision` `multi-bitwidth-hw`
`lut-accelerator` `accelerator`
(**Proposed additions**: `mixed-precision` — the scheme is INT8 activations with INT4 *or*
INT8 weights, Table 3 p10; `lut-accelerator` + `non-analytical-dtype` — per the human's
2026-09-03 ruling that the method is LUT-based, see the resolved flag below. `survey/TAGS.md`
not edited; the human maintains it.)
How far it was read: **close read of §1–§5 and §7** — abstract, introduction, §2 (background,
motivation, Hasse representation, parallelism), §3 (Scoreboard, both algorithms), §4 (tiling,
dispatch, network, PEs, scheduling), §5.1–§5.10 (all of evaluation, incl. Tables 1–3 and the
design-space figures) and the conclusion. **Skimmed:** §6 Related Works and the reference
list. Figures 9–13 were read for their prose claims; **per-bar values in Fig. 9–12 were not
transcribed** because the extracted text does not attach bar labels to series reliably — see
"what was left blank" below.

> Original: https://arxiv.org/abs/2504.16339
> The PDF is **not committed** (1.3 MB). Re-download: `curl -sSL -o 2504.16339.pdf https://arxiv.org/pdf/2504.16339`
> Extract text: `python3 extract.py` → `extracted/` (committed, greppable)
>
> **Why this paper is in the survey**: it is the **40th row of
> [`QuantArchSurvey/venues/ISCA/README.md`](../../../QuantArchSurvey/venues/ISCA/README.md)**
> — the one paper on that list that was missing from this corpus. Their list calls it
> **"TransArray"** with no link; the human identified it (2026-09-03) as this paper.
> **Alias: `TransArray` = `Transitive Array` = this directory.**

---

## Flag: RESOLVED by the human, 2026-09-03 — seed tags stand

`QuantArchSurvey` leans on this paper as a load-bearing anchor, and **the anchor may be
mis-set**. Three places say so:

| Where | What it says |
|---|---|
| `venues/ISCA/README.md` | Tags it `LUT`, `G3`, optimization `LUTGEMM`, note *"Lookup-based quantization; G3 codebook anchor on the timeline"* |
| `TAXONOMY.md` §G3 thread 3 | *"Codebook-based quantization. Values become indices into a table and compute becomes lookup — lookup-based quantization (TransArray, ISCA'25)"* |
| `survey/outline.md` §5.6 | *"Lookup-based compute: arithmetic replaced by table lookup (TransArray, ISCA'25)"* |

**But the paper does not appear to be a codebook or lookup-table method.** Its own framing,
verbatim from the abstract (**verified**): *"a novel sparsity paradigm, **transitive
sparsity**, which leverages the reuse of previously computed results"*, delivered by *"the
Transitive Array, a **multiplication-free** accelerator"*. Values are **not** turned into
indices into a table of representative values. What is reused is a **partial sum already
computed for another row** of a bit-sliced binary matrix — memoization over a DAG of
transitive relations, not a data-type codebook. §2.1 is *"Background: Quantization and
**Bit-slicing**"*, and the paper positions itself against **bit-slice** accelerators
(BitVert, and the Olive line), not against codebook ones.

So on their axes this looks like `INT`/`BINARY` + bit-slicing with a *sparsity* and
*result-reuse* optimization — **closer to their `G2` bit-slice lineage than to the `G3`
codebook thread** — even though it is a 2025 LLM-era paper.

**This is a question, not a verdict.** There is a defensible reading where reusing a stored
result *is* a lookup, and the human may have intended the anchor loosely. But if §5.6 of the
survey needs a genuine "arithmetic replaced by table lookup" anchor, the corpus already has
better candidates — [`LUTTensorCore`](../LUTTensorCore/ANALYSIS.md),
[`OASIS`](../OASIS/ANALYSIS.md), [`Omni-LUT`](../Omni-LUT/ANALYSIS.md) — and for the
*codebook* thread, [`Mokey`](../Mokey/ANALYSIS.md) and [`EVA`](../EVA/ANALYSIS.md).
**Resolve this on the close read before the taxonomy hardens around it.**

### Close-read verdict on the flag (2026-09-03)

**The flag is upheld, but with an important qualification that cuts the other way.**

*Upheld:* the paper **never uses the words "lookup", "look-up", "LUT", "codebook" or
"memoization" anywhere in its 15 pages** (**verified** — grep over `2504.16339.raw.txt`; the
only hits for "table" are Tables 1–3, the Scoreboard Information "simplified table", and the
spec line "Two 8-way 256-entry tables"). It cites no LUT-GEMM work. Values are never mapped
to indices into a dictionary of representative values. On the paper's own framing this is
**bit-slice + sparsity**, not `LUT` and not `VQ`.

*The qualification:* mechanically, the **prefix buffer is a partial-sum table indexed by
TransRow value**, and the steady-state datapath per TransRow is *read the prefix result, add
one input* (§4.3, p07). A LUT-GEMM engine precomputes all 2^T sums of T activations and
indexes by the weight bit-pattern; TransArray computes **only the 2^T entries that actually
occur**, incrementally, one add each, in Hamming order. So it is fairly described as a
**sparse, incrementally-built LUT-GEMM** — which makes the seed tag less wrong than it first
looked. **This reading is `**inferred / not verified**`; it is mine, not the paper's.**

### Human's ruling, 2026-09-03 — the seed tags stand, and the flag was wrong

**The human ruled the method LUT-based and the generation `G3` (weight-only + codebook
threads).** `venues/ISCA/README.md`, `TAXONOMY.md` §G3 thread 3 and `survey/outline.md` §5.6
therefore need **no change**, and this entry stays the §5.6 anchor.

The paper's own §5.2 carries the decisive evidence, which the flag above missed: **Full
Result Reuse (FR)** is defined as *"nodes that have been computed previously, allowing
subsequent TransRows to reuse the results without requiring prefix computations or PPE"*
(**verified**, §5.2, p09) — a pure table read with **zero** arithmetic — and FR is stated to
be **the majority of TransRows** at the design point. A TransRow's 8 bits are an index into
the 2^8 = 256 possible partial sums of an activation group; the 18 KB **prefix buffer is that
table**. That is TAXONOMY's G3 thread-3 definition met literally: *values become indices into
a table and compute becomes lookup*. **Weight-only** likewise holds: the bit-slicing,
TransRows and reuse structure are entirely weight-side (K/V treated as weights in attention)
while activations stay dense INT8.

What survives from the flag is only that **the paper resists the label** — it never writes
"lookup", "LUT" or "codebook" in 15 pages and cites no LUT-GEMM work (**verified** by grep).
That makes `G3`/`LUT` a claim *about* the paper rather than a restatement of it — and the
more useful claim, since the real distinction from LUT Tensor Core / OASIS is **lazy versus
eager codebook construction**, not lookup versus arithmetic. That is the survey paragraph.

**Consequently: our own tags should gain `lut-accelerator` and `non-analytical-dtype`.**
`survey/TAGS.md` is not edited here — the human maintains it.

---

## Brief

### 1. Motivation

Quantization has taken GEMM to 4 bits (AWQ) and towards 1 bit (BitNet 1.58), and
**bit-slicing** — decomposing a quantized matrix into binary 1-bit matrices — lets
accelerators exploit bit-level sparsity for computational reductions of **up to 50–60%**.
But bit sparsity has a floor: it can only skip the zero bits that happen to be there.
BitVert, for instance, guarantees *at least* 50% sparsity and stops there. The paper's
observation is that in binary GEMM, **different rows share partial sums**, so work already
done for one row can be reused for another instead of being redone.

### 2. Overview

Introduces **transitive sparsity**: represent the reuse relations among rows of a
bit-sliced binary matrix as a **directed acyclic graph**, then compute an execution order
that maximizes reuse. Because reuse creates execution *dependencies*, the hard part is
ordering and parallelism, addressed with **Hamming-order execution** and a **scoreboard**.
The resulting **Transitive Array** is a **multiplication-free** accelerator (adds only)
that balances work across parallel lanes; one unit supports a 32×8 tile at 8-bit weights or
64×8 at 4-bit, and it also supports on-the-fly quantization of attention layers.

### 3. Pros and cons

**Pros**

- Attacks a floor the bit-slice line had accepted: bit sparsity skips zeros, whereas result
  reuse eliminates **redundant work that is not zero at all** — a genuinely different axis
  of saving.
- **Multiplication-free** — the PE reduces to additions, which is where the area and energy
  win comes from, and the conclusion attributes the gains to exactly that plus the
  generality of the design.
- Strong margins against the right baselines: **≈7.46× and 3.97× speedup and 2.31× and
  1.65× energy reduction over Olive and BitVert**, at comparable accuracy on LLaMA models.
- Claims **broad support for existing quantization frameworks "without specialized
  requirements"**, which — if it holds — is a much lower adoption barrier than a new format.

**Cons**

- **Reuse creates dependencies**, which is the opposite of what a parallel array wants. The
  scoreboard and Hamming-order execution exist to manage that, and the scoreboard is not
  cheap — the area breakdown lists it at **92507 µm²** against a 548 µm² 8-bit PE, so
  roughly the area of ~170 PEs. Whether that trade holds at other array sizes needs the
  close read.
- The design leans on a distributional fact — *"only approximately 1.67% of TransRows in
  our design have distances greater than 1"* — so the sparsity available is data-dependent,
  not structural like BitVert's guaranteed 50%.
- Scaling the mechanism costs disproportionately: **"10-bit TranSparsity requires 4× the
  hardware overhead of 8-bit TranSparsity but offers comparable sparsity"** at a 256 tile
  row — the paper's own note that the idea does not extend upward for free.
- Accuracy is reported as "comparable" on LLaMA rather than as a quantization contribution;
  the paper is an execution-efficiency result on top of someone else's quantization.

### 4. Where it applies

Sits in the **bit-slice / multi-bitwidth datapath** lineage —
[`BitFusion`](../BitFusion/ANALYSIS.md) → [`RaPiD`](../RaPiD/ANALYSIS.md) →
[`UniCore`](../UniCore/ANALYSIS.md) → here — as the entry that changes *what work is done*
rather than *how wide the operands are*. It is also the corpus's clearest case of
**sparsity and quantization interacting**: bit-slicing is what makes transitive sparsity
visible at all. Given the flag above, it is **also the paper to settle before writing
survey §5.6**, because the survey currently cites it as that section's anchor.

---

## Conclusions

**Read in full 2026-09-03.** The brief above survives the close read essentially intact.
**What changed:** (a) the con about scoreboard area is now quantified and turns out to be
*understated in one direction and overstated in another* — the Scoreboard is 92 507 µm², but
so is the on-array NoC at 6 × 19 520 = 117 120 µm², so **47 % of the 0.443 mm² core is reuse
machinery rather than compute** (**verified**, Table 2, p09, arithmetic checks to 443 099 µm²);
(b) the brief's "one unit supports 32×8 at 8-bit or 64×8 at 4-bit" is correct but the design
ships **six** such units (**verified**, §5.3, p09); (c) the brief did not know that **every LLaMA
number comes from one Transformer block at prefill length 2048** (**verified**, §5.1, p08) —
this is the single most important frame in the paper and it was missing. Nothing in the brief
was overturned.

---

## Method

**Verified** unless marked. Page numbers are `extracted/2504.16339.pages/pNN.txt`.

1. **Bit-slice.** An `S`-bit quantized matrix of shape `(N×K)` is decomposed into `S` binary
   matrices and stacked into an `(S·N × K)` binary matrix (§2.1, p02–p03). Each binary row of
   width `T` is a **TransRow (TR)**, read as an unsigned `T`-bit integer. `T = 8` in the built
   design. Bit-slicing is exact given wide enough accumulators (§2.1, p02).
2. **Transitive sparsity.** If TR `a`'s 1-bits are a subset of TR `b`'s, `b` can start from
   `a`'s already-computed partial sum and add only the difference bits `a ⊕ b`. Reuse is
   **lossless** and **algorithm-agnostic** — it changes the order of integer additions, not
   the values (§1, p02).
3. **Hasse graph.** The subset relation over `T`-bit patterns is a partial order, drawn as a
   Hasse diagram; a node's level is its popcount. `distance` = level difference to its prefix
   (§2.3, p03). Nodes on the same level are independent → **parallelism is horizontal**, and
   the graph splits into `T` independent trees, one per Level-1 node (§2.4, p03–p04).
4. **Scoreboard.** Builds the execution order: PopCount (Hamming-order) sort via a bitonic
   sorter → record present TRs → **forward pass** assigns candidate prefixes → **backward
   pass** keeps exactly one shortest-distance prefix per node → round-robin lane assignment
   for load balance → emits **Scoreboard Information (SI)**, just `(TransRow, Prefix)` pairs
   (§3.1–§3.2, p04–p05). SI costs `2·T·2^T` bits = **512 B at T=8** (§3.2, p06).
   - **Static SI**: computed offline per tensor, shared by all tiles, no hardware Scoreboard —
     but suffers **\"SI Miss\"** when a tile lacks the prefix (§3.3, p06).
   - **Dynamic SI**: a per-sub-tile hardware Scoreboard, transparent to software, and the
     only path that supports attention (§3.4, p06). **All experiments use dynamic except
     §5.8.**
5. **Datapath.** Per TransRow: XOR with its prefix to get the difference bits → fetch inputs
   through an **8-way Beneš network** → **PPE** (one 12-bit adder) adds input to the prefix
   partial sum and writes the **prefix buffer** → **APE** (one 24-bit accumulator) produces
   the output; a crossbar + double buffer avoid prefix-buffer bank conflicts (§4.3–§4.5,
   p07–p08). **No multipliers anywhere.** Three-stage pipeline (Scoreboard / PPE / APE); the
   PPE array is the critical path (§4.6, p08).
6. **Escape valves in the mechanism** (not precision): TRs with **distance ≥ 4 are \"treated
   as outliers and dispatched at the end of other operations\"** (§5.2, p09); non-GEMM work
   (de-quantization, softmax) goes to a **VPU** (§4.5, p08).

## Key numbers, with their frame

**Common frame for every row below**: 28 nm, 500 MHz, all designs re-implemented by the
authors at the same node and frequency; area/power from **Synopsys DC post-synthesis** with
ARM standard cells, buffers from **Cacti 7.0**; performance from a **cycle-level simulator**
built on ANT's open-source simulator (§5.1, p08). **No silicon.** LLaMA results use **only
the first Transformer block, prefill sequence length 2048**, extrapolated on the argument
that all blocks are identical (§5.1, p08).

| Setting | Model | Metric | Baseline | Result | Source |
|---|---|---|---|---|---|
| FC layers, iso-precision (TA W8A8 vs 8-bit baselines) | LLaMA-1/2/3, geomean | Speedup | ANT / OliVe / BitVert | **2.47× / 3.75× / 1.99×**, "similar energy" | §5.5, p10–p11 · simulator |
| FC layers, iso-accuracy (TA **W4A8** vs 8-bit baselines) | LLaMA-1/2/3, geomean | Speedup | ANT / OliVe / BitVert | **4.91× / 7.46× / 3.97×** | §5.5, p11 · simulator |
| FC layers, iso-accuracy | same | Energy efficiency | ANT / OliVe / BitVert | **1.65× / 2.31× / 1.65×** | §5.5, p11 · simulator + synth. power |
| Attention layers, seq 2048, 8-bit group-wise both sides | LLaMA-1-7B, 2-?B, 3-8B | Speedup | ANT (8-bit) | **1.54×** (and 3.97× vs BitFusion-16b) | §5.7, p11 · simulator |
| ResNet-18 / ImageNet, TA W4 (first conv + last FC at 8-bit) | ResNet-18 | Speedup | BitFusion / ANT | **4.26× / 2.21×** | §5.10, p12 · simulator |
| Accuracy, W4A8 group-wise (QServe) | LLaMA-1-7B / 3-8B | Wikitext PPL | FP16 = 5.68 / 6.14 | **5.82 / 6.59** (Δ +0.14 / **+0.45**) | Table 3, p10 |
| Accuracy, W8A8 group-wise | LLaMA-1-7B / 3-8B | Wikitext PPL | FP16 = 5.68 / 6.14 | **5.75 / 6.39** (Δ +0.07 / +0.25) | Table 3, p10 |
| Compute-core area, 6 units | — | mm² @28 nm | BitFusion 0.491 · ANT 0.484 · OliVe 0.489 · BitVert 0.473 · Tender 0.474 | **0.443** (−6 % to −10 %) | Table 2, p09 · post-synthesis |
| Core-area composition | — | µm² | — | PPE 6·256·50.3 = 77 261 · APE 6·256·101.7 = 156 211 · **NoC 6·19 520 = 117 120** · **Scoreboard 92 507** (sums to 443 099) | Table 2, p09 · arithmetic checks |
| Buffer capacity | — | KB | baselines 512 / 608 | **480** (6 × 80 KB, incl. **18 KB prefix buffer per unit**) | Tables 1–2, p09 |
| Theoretical sparsity ceiling | — | ops removed | dense GEMM | **75 %** at T=4, **87.5 % (8×)** at T=8 | §4.3, p07 |
| Achieved density, random 1024×1024 binary, T=8, tile row 256 | — | density | — | **≈12.45 %** (≈8.0×) | Fig. 9(c), p09 · simulator, **random data** |
| TRs needing >1 add from their prefix | LLaMA (design point) | % | — | **≈1.67 %** | §4.6, p08 |
| Energy split | LLaMA-1-7B, first FC layer | % of total | — | **buffer 56.4 %**, "primarily … frequent accesses to the prefix buffer" | §5.6, p11 |
| Static vs dynamic Scoreboard | LLaMA-1-7B first FC | density | — | dynamic much better below tile row 512; **equal at 1024**; static saves **≈25 % area** | §5.8, p11 |

Not transcribed: per-bar values of Figs. 10–12 and the full Fig. 9 series — the extracted
layout does not bind bar labels to series reliably. Everything above is from prose, Tables
1–3, or a caption.

## Cost and requirements

- **Data type — the honest statement: TransArray proposes no data type.** Weights and
  activations are plain **INT**; the evaluated points are **W8A8** and **W4A8** (Table 3
  header, p10). No new format, no outlier class, no codebook.
- **Granularity: group-wise, group size 128** — the VPU applies an integer scale per
  `128/T`-element tile (§4.5, p08). This is the one genuinely quantization-side choice, and
  it is inherited, cited only to a survey ([56]), not to a method.
- **Outliers: none, by design.** The word "outlier" appears only for *distance ≥ 4
  TransRows* (§5.2, p09) and when describing OliVe. Numeric outliers are simply not this
  paper's problem — it defers them to whatever PTQ framework it runs on top of.
- **Escape hatch — three of them.** (i) **Attention is left at FP16 in the accuracy table**
  ("We maintain the Attention layer with FP16 precision", §5.4, p10) — TA *can* quantize
  attention (§5.7) but the reported PPL does not; (ii) accumulation is **12-bit in PPE,
  24-bit in APE** (§4.5, p08) — wide, because bit-sliced sums must not overflow for
  losslessness; (iii) ResNet-18's **first conv and last FC stay 8-bit** (§5.10, p12).
- **Retraining: PTQ only.** Runs **QServe** for LLaMA and **MQBench** for ResNet-18 (§5.4
  p10, §5.10 p12). No QAT anywhere. Its selling point is precisely that it takes a stock
  quantized checkpoint: *"broad support for state-of-the-art quantization frameworks without
  specialized requirements"* (§7, p12).
- **Mixed precision comes free**: bit-slicing handles any weight width; the 12-bit PPE and
  24-bit APE split into two 6-bit / two 12-bit units for 4-bit activations (§4.5, p08).
- **What the hardware pays**: 92 507 µm² Scoreboard + 117 120 µm² on-array NoC = **47 % of
  the compute core**, plus 18 KB of prefix buffer per unit and **56.4 % of energy in buffer
  traffic**. The paper concedes this: *"TransArray design enhances computational efficiency
  at the expense of increased buffer energy consumption"* (§5.6, p11).

## Limitations and open questions

**Authors admit:**
- Buffer energy dominates and prefix-buffer traffic is the cause (§5.6, p11).
- The idea does not scale up: *"10-bit TranSparsity requires 4× the hardware overhead of
  8-bit … but offers comparable sparsity"* at tile row 256 (§5.2, p08).
- Static SI misses badly at small tiles (§5.3/§5.8) — dynamic Scoreboard exists to fix a
  problem the approach creates.
- Speedup is data-dependent, not structural (§5.9, p12), unlike BitVert's guaranteed 50 %.

**Not admitted, and worth the survey's attention:**
1. **The evaluation is one Transformer block at prefill 2048** (§5.1, p08). Decode — the
   memory-bound regime that motivates weight-only quantization across this whole corpus — is
   **never evaluated**. A design whose energy is 56 % buffer traffic and whose win is fewer
   *arithmetic ops* is being measured in exactly the regime that flatters it.
2. **Only TransArray and ANT get group-wise quantization** (Table 3 caption, p10: "ANT with
   group quantization, and TransArray (TA) with group quantization"; §5.4 says ANT was
   modified "for a fair comparison"). OliVe, Tender, BitVert and BitFusion were **not**
   given it. The headline **7.46× over OliVe** therefore compares TA-at-W4-with-groups
   against OliVe-at-W8-without — an algorithmic advantage, not only an architectural one.
   The paper's defence is that generality *is* the contribution, which is fair; but the
   number should not be quoted as a pure architecture comparison.
3. **The BitVert accuracy row is almost entirely empty** — PPL exists for LLaMA-3-8B only
   (6.24), everything else "—" (Table 3, p10; §5.4 says results were taken from its paper).
   The iso-accuracy claim against BitVert rests on one model.
4. **TA-W4A8 is not uniformly iso-accurate.** On LLaMA-3-8B it scores **6.59** against ANT's
   6.27 and BitVert's 6.24 (Table 3, p10) — worse than both baselines it claims 4.91× and
   3.97× over. Only LLaMA-1/2 support the "similar accuracy" framing.
5. **Naming.** The baseline called *BitVert* throughout is cited as **BBS: Bi-directional
   Bit-level Sparsity** (Chen et al., arXiv:2409.05227), listed **twice** as refs [8] and
   [9]. Cite carefully.
6. **Iso-area is core-only.** Table 2 gives an area column for the computation core and a
   separate *capacity* column for buffers, with no buffer area (p09). TA's smaller 480 KB
   helps the claim, but the 18 KB/unit prefix buffer is state the baselines do not carry.

## Relation to other entries

- **Direct lineage — architecture for executing quantized arithmetic, no new format:**
  [`BitFusion`](../BitFusion/ANALYSIS.md) (ISCA'18) → [`RaPiD`](../RaPiD/ANALYSIS.md)
  (ISCA'21) → [`UniCore`](../UniCore/ANALYSIS.md) / [`XtraMAC`](../XtraMAC/ANALYSIS.md)
  (ISCA'26) → here. TransArray is the entry that changes *what work is done* rather than
  *how wide the operands are* — and the only one that removes the multiplier entirely.
- **Explicit baselines it beats:** [`OliVe`](../OliVe/ANALYSIS.md) (7.46×) and
  [`Tender`](../Tender/ANALYSIS.md) (reference only — its 4-bit PPL is called
  "unacceptable", §5.4 p10). Both are in this corpus, so **this is a cross-entry
  disagreement worth recording**: TransArray's §5.5 argues the mixed-precision advantage of
  ANT and OliVe *disappears* on LLMs and that they become "even slower than BitFusion
  because of the larger overhead from their complex PEs" (p10). That is a direct attack on
  OliVe's own claims.
- **Non-corpus baselines:** ANT (MICRO'22) and BBS/"BitVert" (2024) — **neither is in this
  ISCA-only corpus**, and both are load-bearing. Reinforces the README's "extend beyond
  ISCA" gap.
- **The LUT/codebook thread it is *not* part of:** [`LUTTensorCore`](../LUTTensorCore/ANALYSIS.md),
  [`OASIS`](../OASIS/ANALYSIS.md), [`Omni-LUT`](../Omni-LUT/ANALYSIS.md),
  [`Mokey`](../Mokey/ANALYSIS.md), [`EVA`](../EVA/ANALYSIS.md) — but see the close-read
  verdict above for the mechanistic kinship the survey may want to draw.
- **Sparsity × quantization:** the clearest case in the corpus that bit-slicing is what
  *makes* a sparsity opportunity visible. [`SpZip`](../SpZip/ANALYSIS.md) is the contrast —
  sparse-format compression with no quantization at all.

## For the note

### §1 one-line summary

> **TransArray takes an ordinary INT4/INT8 group-wise-quantized checkpoint, bit-slices it
> into binary matrices, and observes that one binary row's partial sum is a prefix of
> another's — so it orders rows by Hamming weight over a Hasse graph and computes each row
> with a single addition onto a reused prefix result, yielding a multiplication-free
> accelerator that removes up to 87.5 % of the additions in binary GEMM at no accuracy cost
> beyond the quantization it inherits.**

The data type is *not* the contribution — that is the point to make about this paper.

### Proposed values on their four axes

| Axis | Proposed | Evidence (one line) |
|---|---|---|
| **Level** | `ARCH` | Datapath, NoC, Scoreboard unit and PE design; the quantization algorithm is inherited wholesale from QServe / MQBench (§5.4 p10, §5.10 p12). Not `ALGO+ARCH`: no quantization algorithm is proposed. |
| **Q-oriented** | **`Q-ORIENTED`** | The taxonomy's literal test ("swap the format for plain INT8") mis-fires here because the paper *already is* plain INT — but the architecture cannot execute anything except bit-sliced quantized integers, so removing quantization deletes the paper. Same species as `BitFusion`, which their own list tags `Q-ORIENTED` with no novel format. |
| **Data type** | **`LUT` + `INT4` + `INT8` + `MIXED`** | An 8-bit TransRow indexes the 256 possible partial sums of an activation group; the 18 KB prefix buffer is the table, and §5.2's "Full Result Reuse" majority reads it with zero arithmetic (p09). Formats are plain integer: Int8 activations with Int4 or Int8 weights, group size 128 (Table 3 p10, §4.5 p08). |
| **Generation** | **`G3`** (human's ruling, 2026-09-03) | Two of the three G3 threads. **Codebook**: weight bit-patterns become indices into a table of partial sums and compute becomes lookup (§5.2 FR nodes, p09). **Weight-only**: the whole reuse structure is weight-side — K/V treated as weights in attention — while activations stay dense INT8. LLM framing throughout (LLaMA, attention, QServe, AWQ/BitNet). |
| **Optimization** (free text) | `LUT-GEMM` `result-reuse` `lazy-codebook-construction` `bit-slice` `multiplication-free` `Hasse-graph-scheduling` `scoreboard` `group-wise scaling` | — |

### Proposed venue-list row

Replaces the `TransArray` row under **2025** in `venues/ISCA/README.md`. **Do not let an
agent paste this** — it is for the human to apply.

```
| [x] | [Transitive Array: An Efficient GEMM Accelerator with Result Reuse](https://arxiv.org/abs/2504.16339) | ARCH | Q | `LUT` `INT4` `INT8` `MIXED` | G3 | `LUTGEMM` `result-reuse` `multiplication-free` | Lookup-based quantization built **lazily**: a TransRow indexes a 256-entry table of activation partial sums, one add per new entry |
```

### §4 fairness verdict

**Iso-node and iso-area: yes. Iso-accuracy: mostly, with one real exception. Iso-algorithm:
no — and that is where the headline number comes from.**

- **Iso-node ✓** — everything at 28 nm / 500 MHz, all baseline PEs re-implemented by the
  authors (§5.1, p08). Unusually clean for this corpus.
- **Iso-area ✓ (favouring the baselines)** — TA's core is 0.443 mm² against 0.473–0.491 mm²,
  with a *smaller* 480 KB buffer against 512/608 KB (Table 2, p09). Caveat: the area column
  covers the compute core only; buffer area is not tabulated.
- **Iso-accuracy ~** — TA-W4A8 matches or beats the 8-bit baselines on LLaMA-1 and LLaMA-2
  (Table 3, p10), so the headline is defensible there. **On LLaMA-3-8B it does not**: 6.59
  against ANT 6.27 and BitVert 6.24.
- **Iso-algorithm ✗ — the live issue.** Only TA and ANT were given group-wise quantization;
  OliVe, Tender, BitVert and BitFusion were not (Table 3 caption + §5.4, p10). The 7.46× over
  OliVe is *TA at W4 with groups and QServe* versus *OliVe at W8 without*. The paper is open
  that generality is the contribution — but the number is an architecture-plus-algorithm
  result and should be quoted as such.
- **Peak vs end-to-end ~** — the 87.5 % / 8× figure is a **theoretical ceiling on random
  data** (§4.3 p07, Fig. 9 p09); the end-to-end speedups (2.47×–7.46×) are the numbers to
  cite. Prefer them. But note "end-to-end" here means **one Transformer block at prefill
  2048**, never a full model and never decode.

## Note from the source list

> Not on the source CSV at all — this paper comes from
> `QuantArchSurvey/venues/ISCA/README.md`, where it is listed as **"TransArray"** with the
> note *"Lookup-based quantization; G3 codebook anchor on the timeline"*. See the flag above.

## Abstract (verbatim, arXiv:2504.16339v1)

> Deep Neural Networks (DNNs) and Large Language Models (LLMs) have revolutionized
> artificial intelligence, yet their deployment faces significant memory and computational
> challenges, especially in resource-constrained environments. Quantization techniques have
> mitigated some of these issues by reducing data precision, primarily focusing on General
> Matrix Multiplication (GEMM). This study introduces a novel sparsity paradigm, transitive
> sparsity, which leverages the reuse of previously computed results to substantially
> minimize computational overhead in GEMM operations. By representing transitive relations
> using a directed acyclic graph, we develop an efficient strategy for determining optimal
> execution orders, thereby overcoming inherent challenges related to execution
> dependencies and parallelism. Building on this foundation, we present the Transitive
> Array, a multiplication-free accelerator designed to exploit transitive sparsity in GEMM.
> Our architecture effectively balances computational workloads across multiple parallel
> lanes, ensuring high efficiency and optimal resource utilization. Comprehensive
> evaluations demonstrate that the Transitive Array achieves approximately 7.46× and 3.97×
> speedup and 2.31× and 1.65× energy reduction compared to state-of-the-art accelerators
> such as Olive and BitVert while maintaining comparable model accuracy on LLaMA models.
