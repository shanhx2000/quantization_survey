# Cambricon-SR — paper notes

**Cambricon-SR: An Accelerator for Neural Scene Representation with Sparse Encoding Table**
Tianbo Liu, Xinkai Song, Zhifei Yue, Rui Wen, Xing Hu, Zhuoran Song, Yuanbo Wen, Yifan Hao,
Wei Li, Zidong Du, Rui Zhang, Jiaming Guo, Di Huang, Shaohui Peng, Guangzhong Sun, Qi Guo,
Tianshi Chen (USTC · SKLP, ICT, CAS · SJTU · UCAS · ISCAS · Cambricon Technologies)
**ISCA 2025**, pp. 1254-1268 ｜ DOI: **10.1145/3695053.3731018**
Publication info verified 2026-09-09: venue, year, page range and DOI all read out of the
archived PDF's own text (ACM copyright block and page footers on p1/p15).
Archived here: the **published ACM version** (CC-BY), 15 pages.

Status: **note ready** ｜ Last updated: 2026-09-14 ｜ **Human-checked 2026-09-14** — confirmed `NON-Q-ORIENTED`, no quantization.
Tags: `accelerator`
How far it was read: **full close read of §1-§7** (pp. 1254-1267). Read line by line: §1
(motivation, Fig. 1), §2.1-§2.2 (the NSR pipeline, the hash-grid equation, the three prior
accelerators), §3.1-§3.3 (Algorithm 1, the sparsity-size trade-off, the GPU implementation
and the A100 structured-sparsity negative result), §4.1-§4.5 (dataflow, architecture, Sparse
Update Unit, Sparse Index Unit including all four rejected designs, MLP dynamic shared
buffer), §5.1-§5.2.5 (methodology, Tables 1-2, all figures' prose, ablation), §6-§7.
**Skimmed, and itemised honestly:** (a) the **reference list** (pp. 1267-1268) was read only
by grep, not entry by entry — the grep for `quantiz|compress|precision|bit-width|low-bit`
over both reference pages returns **zero**, which is the load-bearing fact; (b) **Figures
3, 4, 6, 11, 12, 14, 15, 16, 17, 18, 19 are raster images** in the text extraction and were
**not** rendered to PNG — every number quoted from them below is the one the *prose* states,
and no per-scene bar value has been read off a plot; (c) Figure 13's per-iteration counts
(678 vs 2027) and PSNR/SSIM come from the figure's own text labels, which did extract.
Table 1 and Table 2 extracted as text and were read in full. **Not resolved:** the paper
never states a numeric format or an operand width anywhere (see `## Method`, "The datapath
question"), so the 4 B/entry figure below is a **derivation from three of the paper's own
byte counts**, not a quotation, and the split of those 4 bytes into `F` elements is an
inference from Instant-NGP's defaults, not from this paper.

> Publisher record: https://dl.acm.org/doi/10.1145/3695053.3731018
> **There is no arXiv version** (arXiv API title search, 2026-09-02). The PDF was downloaded by
> a human and filed through [`survey/uploads/`](../../uploads/); see
> [`Notes-002`](../../../Claude/notes/Notes-002-paper-source-access.md).
> The PDF is **not committed** (4.7 MB). It is CC-BY licensed, so the publisher page is
> readable in a browser. Re-extract with `python3 extract.py` → `extracted/` (committed).
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, ISCA 2025 row.

---

## ⚠ Confirmed on a full read: this paper contains no quantization

The `brief ready` note carried this claim off a partial term sweep. **A negative claim needs
the same evidence as a positive one** (the `XtraMAC` precedent), so it was re-tested on the
full text with a much wider vocabulary and against a specific alternative hypothesis — that
a "sparse encoding table" in a neural-scene-representation workload might be a
**hash-table / feature-grid codebook** and therefore belong next to `Mokey`, `EVA` and
`OASIS` in the §1.3 lookup-table box. **It is not.** The claim stands, and now rests on
evidence rather than on not-having-noticed.

### The sweep, and what it returned

Counted over `extracted/10.1145_3695053.3731018.txt` (the `-layout` full text) and
cross-checked on `.raw.txt`; both give the same counts.

| Term | Hits | Term | Hits | Term | Hits |
|---|---|---|---|---|---|
| `quantiz*` | **0** | `precision` | **0** | `bitwidth` / `bit-width` / `bit width` | **0** |
| `INT8` / `int8` / `INT4` | **0** | `FP32` / `FP16` / `FP8` | **0** | `BF16` / `bf16` | **0**† |
| `fixed-point` / `fixed point` | **0** | `floating` | **0** | `integer` | **0** |
| `low-bit` / `low bit` | **0** | `mantissa` / `exponent` | **0** | `8-bit` / `16-bit` / `32-bit` | **0** |
| `compress*` | **0** | `codebook` / `code book` | **0** | `dictionary` | **0** |
| `centroid` | **0** | `cluster` / `k-means` | **0** | `vector quantiz*` | **0** |
| `LUT` (word-boundary) | **0**‡ | `numeric` / `data type` / `number format` | **0** | `half precision` / `mixed precision` | **0** |
| `word length` | **0** | `arithmetic` | **0** | `multiplier` / `adder` / `datapath` | **0** |

† The one substring hit is inside the hex-address table in Fig. 10(b) — `008016 009F16
00BF16 00DF16 00FF16`, i.e. addresses with a subscript-16 radix marker. Not a format.
‡ All 8 substring hits are inside `resoLUTion`, `soLUTe` and the word `Lookup`. Zero as a word.

**What the paper is actually full of:** `encoding table` 50, `sparse` 110, `sparsity` 59,
`hash` 29, `Instant-NGP` 16, `bitmap` 20, `index` 20, `prune` 17, `table` 156, `PSNR` 32,
`SSIM` 15. The word `bit` appears 4 times and `bits` twice, **all six in addressing
contexts** — "the upper 4 bits of the address", "based on the high bits of the addresses",
"the bitmap that stores the sparsity of each entry in a bit", "3.9 pJ/bit". None is a
datapath width.

**The reference list is clean too.** Grepping pp. 1267-1268 for
`quantiz|compress|precision|bit-width|low-bit` returns **zero**: the bibliography does not
cite a single quantization or compression paper. That is a stronger signal than the body
sweep, because it shows the authors do not situate themselves in this literature at all.

### The codebook hypothesis, tested and rejected

The title's "encoding table" is **Instant-NGP's multiresolution hash grid**, defined in the
paper's own Eq. 1 (§2.1, p. 1256): `h_i = H(x_i, y_i, z_i) = (π₁x_i ⊕ π₂y_i ⊕ π₃z_i) mod T`
with `π₁=1, π₂=2654435761, π₃=805459861`, and *"each hash table consists of T entries, and
each entry stores an F-dimensional feature vector … the total number of trainable parameters
in the hash encoding tables is L × T × F"*. **verified** (§2.1).

Tested against the corpus's **codebook-objective axis** — Ecco builds a codebook to *store*
through, [`EVA`](../EVA/ANALYSIS.md) to *compute* through, [`Phi`](../Phi/ANALYSIS.md) to
*skip* through, and [`Mokey`](../Mokey/ANALYSIS.md)/[`OASIS`](../OASIS/ANALYSIS.md) sit on
the same axis. **None of the three objectives applies, because the precondition of the axis
is absent.** A codebook exists to represent *some other value* more cheaply; recovering that
value is `codebook[index]`. Here:

1. **The index is a function of a 3D position, not of a value.** There is no encode step —
   no nearest-centroid search, no assignment, no quantization error. **verified** (Eq. 1).
2. **There is no original tensor being approximated.** The table entries *are* the model's
   trainable parameters (`L × T × F` of them). Nothing is reconstructed; the lookup returns
   the parameter itself. **verified** (§2.1).
3. **Nothing about the design depends on what a table entry looks like numerically.** The
   SIU matches *addresses* against a 1-bit-per-entry bitmap; the CAM translates a dense-table
   address to a sparse-table address; the SUU moves whole entries. All three are agnostic to
   the entry's content. **verified** (§4.3-§4.4).

**The strongest counter-argument, stated and then dismissed.** Instant-NGP's hash grid *is*
a lossy compression of a dense feature grid — collisions make many vertices share one entry,
which is structurally weight sharing. But (i) that is the *workload's* property, inherited
wholesale, not this paper's contribution; (ii) the paper never analyses collisions, never
measures a reconstruction error, and never frames the table as compression; (iii) a survey
that admitted it on those grounds would have to admit every embedding-table paper ever
written. **inferred / not verified** as a judgment; the three facts it rests on are verified.

**Verdict: `NON-Q-ORIENTED`, data type `—`, generation `—`.** Apply the taxonomy's own test
— swap the format for plain INT8 and see what is left — and *everything* is left: ST-NSR's
magnitude pruning, the Sparse Update Unit, the CAM address translation, the Sparse Index
Unit and the dynamic shared buffer are all format-blind. The seed tags `VQ` / `G3` in
`QuantArchSurvey/venues/ISCA/README.md` were inferred from the title before anyone held the
text; they are a false friend. Same treatment as [`SpZip`](../SpZip/ANALYSIS.md).

---

## What the close read changed in the brief

**The headline finding survived and got stronger; four things in the brief needed fixing.**
(1) The "no quantization" claim is **confirmed** on a sweep about four times wider than the
one behind it, and now additionally on the bibliography — but the earlier note's counts were
slightly off (`hash` is 29 not 24, `Instant-NGP` 16 not 15) and its list omitted the
alternative hypothesis that mattered, the codebook one, which is now tested explicitly above.
(2) **"4× more MLP units in the same area" is wrong** — the MLP *module* ends up **smaller**
than Cambricon-R's, but the **whole chip is +43.0% area** (§5.2.3), and that increase comes
from the CAM, the SUU and the SIU, not from the MLP units. (3) The brief called the
GPU-and-accelerator pairing "the honest pairing" and did not know the **node**: Cambricon-SR
is synthesized at **TSMC 45 nm and then analytically scaled to 7 nm** to meet baselines that
are on 7 nm (§5.1.1) — the comparison is **not iso-node**, it is node-projected, and that is
the single largest fairness hazard in the paper. (4) The brief's "negligible accuracy loss"
scepticism was right but under-specified: "negligible" is defined as **PSNR degradation
≤ 0.5 dB**, and the sparsity rate is **tuned per scene** (eight different forward rates, eight
different backward rates) with no held-out set (§3.2). New material the brief did not have:
a **derivable 4 B per table entry**, and an interesting **negative result about A100 2:4
structured sparsity** (§3.3).

---

## Brief

### 1. Motivation

Neural scene representation reconstructs a 3D scene from dozens of 2D photos. It is too slow
on GPUs (≥5 s per scene on an A100), and the prior accelerator, Cambricon-R, bought its
>60 scenes/second by giving up modelling quality — it completes only **250 training
iterations** per scene, which on the large-scale Kitchen dataset is a PSNR of **18.16**.
**verified** (§1, p. 1255).

### 2. Overview

An algorithm–hardware co-design in four parts. **ST-NSR** makes the encoding table >80%
sparse in the forward stage and its gradients >90% sparse in the backward stage, at ≤0.5 dB
PSNR. A **Sparse Update Unit** cuts off-chip traffic in the update stage by 83.5% (6.06×). A
**Sparse Index Unit** solves the awkward part — the structure bitmap is irregular to index —
by inverting the access: read the bitmap *sequentially* and match incoming addresses against
the read pointer, instead of randomly addressing the bitmap. A **dynamic shared buffer** cuts
per-MLP-unit buffer 85.3%, which buys 4× more MLP units while the MLP module's *total* buffer
shrinks 41%.

### 3. Pros and cons

**Pros**

- The sparse index unit is the real engineering, and the paper shows its work: three
  intermediate designs are costed and rejected (naive 2048×2048 crossbar — EDA cannot route
  it; pure sequential access — 418 mm² of buffers; parallel matching without grouping —
  123 mm², 52.37% of the chip) before the 20.17 mm² answer. That is unusually honest design
  exposition.
- Speedups are reported against both a GPU (A100) *and* the state-of-the-art accelerator
  (Cambricon-R, 4.12× speedup / 2.98× energy), which is the honest pairing — the 1259× over
  A100 alone would be a domain-specific-accelerator-vs-GPU number. Cambricon-R is
  **re-implemented in the authors' own simulator** rather than quoted (§5.1.3).
- Overheads are stated next to their gains (SIU: 7.54× encoding throughput for 8.59% area and
  16.77% of energy — and the paper volunteers that 70.7% of the bitmap data it reads is
  unused).

**Cons**

- **Out of scope for this survey.** No numeric format work of any kind; see the sweep above.
- **Not iso-node.** 45 nm synthesis scaled analytically to 7 nm against 7 nm baselines.
- Training-stage accelerator for one workload; nothing here transfers to inference or to LLMs.
- Evaluated on 8 scenes with **per-scene tuned sparsity rates** and no held-out set, and
  "negligible accuracy loss" means ≤0.5 dB PSNR — the claim the whole result rests on.
- The quality win in Table 1 is **iso-time, not iso-iteration**: the paper concedes ST-NSR
  *loses* PSNR at equal iteration count and wins only by running more iterations.

### 4. Where it applies

**Background only, and a defensible candidate for removal from the corpus.** Its use to the
survey is as an example of the same *structural* move the compression cluster makes —
[`SpZip`](../SpZip/ANALYSIS.md),
[`CommutativeDataReordering`](../CommutativeDataReordering/ANALYSIS.md) — where the
contribution is making an irregular access pattern cheap, with the value representation left
alone. Cite it, if at all, to delimit what the survey is not about. See
`## Relation to other entries` for the keep-or-cut recommendation.

---

## Method

**The workload.** NeRF-family NSR *training*, one training task per frame. Pipeline (§2.1):
sample pixels → rays → points; **encode** each point by hashing its 8 enclosing voxel corners
into `L` per-level hash tables and interpolating the retrieved `F`-dim features; concatenate
into an `F×L` vector; run two small MLPs (density, colour); volume-render; loss; backprop;
update. Three algorithms evaluated: Instant-NGP and Zip-NeRF (hash grid), K-Planes
(multi-planes). **verified** (§2.1, §5.1.2).

**ST-NSR (§3.1, Algorithm 1) — dynamic magnitude pruning of the encoding table, with
restoration.** Three modifications to the training loop, all marked in red in Algorithm 1:

- *Forward*: encode against the pruned sparse table `T_sparse` instead of the dense table
  `T_dense`. **verified** (Alg. 1 line 4).
- *Backward*: a **Backward-Sparsification** step prunes a whole encoded-feature gradient
  vector `df` if **all** its dimensions are below the threshold `θ`. **verified** (Alg. 1
  line 8, §3.1).
- *Update*: gradients accumulate into the **dense** table `T_dense`; then `θ` is set by
  **top-k on the updated dense table** for a pre-determined sparsity rate, and
  `T_sparse` is regenerated by thresholding. **verified** (Alg. 1 lines 13-16).

The dense table must be kept precisely so that pruned entries **can come back** — "pruned
parameters still have a chance to be restored rather than being permanently discarded due to
temporary inactivity", with Fig. 9's worked example of an entry climbing 0.1 → 6.
**verified** (§3.1, p. 1258). This is dynamic sparse training with regrowth in all but name;
the paper does not cite that literature.

**Sparsity-size trade-off (§3.2).** Bigger dense table → higher achievable sparsity at fixed
quality, but a bigger sparse table too. At a fixed ≤0.5 dB PSNR budget they sweep 8→256 MB
and pick **DT = 128 MB**, giving **ST ≤ 26 MB** and **table gradients ≤ 14 MB**, i.e. a
**40 MB on-chip buffer**. **verified** (§3.2, p. 1258).

**The datapath question — what numeric formats does this thing actually use?**
The paper **never says.** No format, no bitwidth, no operand width, anywhere (sweep above).
The MLP module is *"512 MLP units, each consisting of two 32 × 32 MAC (Multiply Accumulate)
arrays"* — **array dimensions, not operand widths** (§4.2, p. 1260). **verified** that the
paper is silent; this is the honest answer and the note records it as silence.

One quantity *is* derivable, from three of the paper's own numbers:

| Fact | Source |
|---|---|
| bitmap of **one level** = **256 KB**, at **1 bit per entry** | §3.3, p. 1259 (*"shared memory on A100 (164 KB per block) cannot accommodate the complete bitmap of one level (256 KB)"*) and §4.4.1 (*"the bitmap that stores the sparsity of each entry in a bit"*) — **verified** |
| ⇒ **T = 2²¹ = 2,097,152 entries per level** | 256 × 1024 × 8 — arithmetic |
| **L = 16 levels** | §4.2, p. 1260 (*"composed of 16 STAs, corresponding to 16 levels of encoding tables"*) — **verified** |
| **DT = 128 MB** total | §3.2, p. 1258 — **verified** |
| ⇒ **8 MB per level ÷ 2²¹ entries = exactly 4 bytes per table entry** | arithmetic — **derived, not stated** |

Cross-checks, both consistent: ST ≤ 26 MB ≈ 128 × 0.20 = 25.6 MB at ~80% sparsity;
gradients ≤ 14 MB ≈ 128 × 0.11 = 14.08 MB at ≥89% gradient sparsity — so **gradients are
stored at the same 4 B/entry**. **derived.**

Splitting those 4 bytes into `F` elements requires `F`, which the paper gives only
symbolically. Instant-NGP's published default is `F = 2` with the hash-grid parameters stored
as `__half`, which would make the element **FP16** and the entry `2 × 16 b`. That is
**inferred / not verified** — it comes from Instant-NGP, not from this paper, and `F = 4`
(8-bit) or `F = 1` (32-bit) are arithmetically just as consistent. **Record the 4 B/entry;
do not record a format.**

**Sparse Update Unit (§4.3) — out-of-order storage with in-place replacement.** The problem:
the on-chip sparse table is stored *compactly*, so inserting and deleting entries naively
means shifting everything after the hole. The observation: after the first 20 iterations,
**≤ 0.8% of entries change sparsity state per iteration**, and because `θ` is set from a
fixed sparsity *rate*, the number entering and the number leaving are **roughly equal**. So
changed entries are classified into four transitions (sparse→sparse skip; dense→dense write
in place; sparse→dense into Queue A; dense→sparse into Queue B) and each cycle one address is
popped from each queue: B's freed slot is where A's new entry is written, and the CAM is
updated to match. Residual imbalance is ~0.03%, absorbed by redundant CAM/SRAM capacity.
**verified** (§4.3, p. 1261).

**CAM (§4.2) — dense-address → sparse-address translation.** Because the ST is packed, every
access needs a translation from the DT address the hash produced to the ST address where the
entry actually lives. A content-addressable memory per STA node does it. Blocked to keep
match energy down: **16 CAM blocks × 160 entries per node**, block selected by the **upper 4
address bits**, ~2,500 entries+gradients per node. **Total CAM = 15 MB, 33.56 mm², 14.29% of
chip area** — the single most expensive consequence of compacting the table. **verified**
(§4.2, p. 1260).

**Sparse Index Unit (§4.4) — the contribution, and it is an access-pattern inversion.**
Requirement: STA sustains 256 requests/cycle and ~86% of requests are invalid, so the filter
must chew ~1800 requests/cycle; target set at **2048**. Four designs, three rejected with
their costs:

| Design | Why it fails | Cost |
|---|---|---|
| 2048 bitmap banks + 2048×2048 crossbar | **EDA cannot complete P&R**; hash-random addresses also unbalance banks | **83% throughput loss** even if built |
| Pure sequential access (1 SAU) | Traversing the whole bitmap is slow, so requests pile up | buffer for **1,059,584** requests, **418 mm²** |
| Many SAUs, all-to-all comparison | comparator count explodes | comparison network **123 mm² = 52.37% of chip** |
| **+ nearest grouping** (adopted) | route each request only to the SAU whose sequential pointer will reach it first → `mn×m` network becomes `m` independent `n×1` networks | comparison network **6.40 mm² = 2.73% of chip** |

Final configuration, chosen by an area sweep (Fig. 11): **32 SIU blocks × 16 SAUs**, 192
requests per group buffer, **SIU total 20.17 mm²**. Each SAU reads **4 bytes of bitmap per
cycle** into register A with its address in register B; matching requests read their bit and
are either enqueued or dropped. **verified** (§4.4, pp. 1261-1263).

*The idea in one line: don't randomly address the bitmap — stream it and let the requests
wait for their address to go past.*

**Dynamic shared buffer (§4.5).** Cambricon-R sizes each MLP unit's local buffer for the
worst-case ray, so average utilisation is **20.29%**. Two fixes: (i) **32 MLP units share one
buffer**, split into blocks of 32 points each with flag-register allocation — 64-way sharing
was rejected because the crossbar area blows up (Fig. 12a); (ii) **dynamic buffer management**
within a ray, reusing a dead tensor's space for a later one (the 5th layer's input activation
dies once its gradients are computed) — **−49.42% per block** on its own. Together:
**−85.31% average buffer per MLP unit**, utilisation to **69.49%**, allowing **512 MLP units**
(4×) with the module's total buffer **down 41%**. **verified** (§4.5, pp. 1263-1264).

**GPU-side result worth keeping (§3.3).** ST-NSR was also implemented in CUDA on an A100 and
gets only **1.55× on the encoding stage / 1.19× overall**, against a ≥5× theoretical memory
reduction — the gap is **bank conflicts** on the shared-memory bitmap. And a clean negative
result: **A100 2:4 structured sparsity is useless here**, twice over — the Tensor Cores'
2:4 support accelerates MACs and ST-NSR's sparsity is in *memory access*, not matrix
multiply; and forcing 2:4 structure onto the encoding table gives **no speedup and −1.5 dB
PSNR**, because table accesses are irregular single-entry lookups. **verified** (§3.3,
p. 1259).

## Key numbers, with their frame

Evidence level is stated per row and must not be pooled: `sim` = the authors' cycle-accurate
simulator (+ Ramulator for DRAM); `synth` = Synopsys DC at **TSMC 45 nm, 750 MHz, then
analytically scaled to 7 nm**; `HW` = measured on an A100; `analytical` = a closed-form
model (off-chip energy at 3.9 pJ/bit).

| Setting | Model | Metric | Baseline | Result | Source |
|---|---|---|---|---|---|
| **Headline speedup**, geomean over 8 scenes × 3 algorithms, measured at the iteration count reaching PSNR 25 | Instant-NGP / Zip-NeRF / K-Planes | training time per iteration | **A100 GPU** | **1259×** — *DSA-vs-GPU; do not quote alone* | §5.2.2, Fig. 14 — `sim` vs `HW` **verified** |
| same | same | training time | **Cambricon-R** (re-implemented by the authors in their simulator) | **4.12×** — the number that matters | §5.2.2, Fig. 14 — `sim` vs `sim` **verified** |
| **Headline energy**, same frame | same | energy per training iteration | A100 / Cambricon-R | **1139× / 2.98×** | §5.2.3, Fig. 15 — `sim`+`analytical` **verified** |
| Area cost of that 4.12× | — | total chip area | Cambricon-R | **+43.0%** (234.86 mm² total) | §5.2.3, Table 2 — `synth` **verified** |
| **Forward sparsity**, per-scene tuned | 8 scenes | encoding-table sparsity at ≤0.5 dB PSNR | dense NSR | **86 / 88 / 96 / 94 / 82 / 80 / 84 / 82 %** (abstract rounds to ">80%") | §3.2, Fig. 4a — `sim`/algorithmic **verified** |
| **Backward sparsity**, per-scene tuned | 8 scenes | gradient sparsity at ≤0.5 dB PSNR | dense NSR | **80 / 85 / 95 / 85 / 85 / 90 / 95 / 85 %** (abstract ">90%") | §3.2, Fig. 4b **verified** |
| Table gradient sparsity used by the SUU | — | gradient sparsity | — | **≥ 89%** ⇒ ≤11% of DT touched | §4.3 **verified** |
| **Memory sizing** | — | DT / ST / gradients / on-chip | — | **128 MB / ≤26 MB / ≤14 MB / 40 MB SRAM** | §3.2, §4.2 **verified** |
| **Entry size** | — | bytes per encoding-table entry | — | **4 B** (256 KB bitmap ⇒ T=2²¹; 128 MB / 16 levels / 2²¹) | **derived**, §3.3 + §4.2 + §3.2 |
| SUU gain | — | off-chip accesses in the table-update stage | naive full-DT update | **6.06× fewer = −83.5%**; update-stage time **−5.28×**; update share of total → **32.85%** | §4.3, §5.2.3 — `sim` **verified** |
| Where the update cost was | — | share of ST-NSR processing time before SUU | — | off-chip DT access **72.1%** total, of which DT update **13.0%** and ST update **59.1%** | §4.3 **verified** |
| SIU gain | — | encoding-stage throughput | no SIU (unfiltered requests) | **7.54×**, for **8.59%** of chip area | abstract, §4.4, §5.2.5 — `sim`+`synth` **verified** |
| SIU vs the design it replaces | — | throughput | naive 2048×2048 crossbar | **5.88×** | §4.4 — `sim` **verified** |
| SIU area, alternatives costed | — | comparison-network area | — | naive sequential **418 mm²** → ungrouped parallel **123 mm² (52.37%)** → **nearest grouping 6.40 mm² (2.73%)**; whole SIU **20.17 mm²** | §4.4 — `synth` **verified** |
| SIU energy, volunteered by the authors | — | share of chip energy | — | **16.77%** of energy at 8.59% of area; **70.7%** of bitmap data read is unused, = **52.8%** of SIU energy; net waste **8.85%** | §5.2.3, Fig. 16 **verified** |
| CAM cost | — | area | — | **15 MB CAM = 33.56 mm² = 14.29%** of chip | §4.2 — `synth` **verified** |
| Dynamic shared buffer | — | buffer per MLP unit | Cambricon-R's private buffers | **−85.31%**, utilisation **20.29% → 69.49%**; 4× units at **−41%** total MLP buffer; naive 4× would need **+144 MB** | §4.5, §5.2.5 **verified** |
| **Ablation** (Fig. 18/19) | — | incremental speedup | Cambricon-SR-plain | SUU **1.24×** → shared buffer **1.36×** (MLP stage 3.92×) → SIU **3.07×** | §5.2.5 — `sim` **verified** |
| **Quality at iso-time**, 0.1 s/scene = 10 scenes/s | Instant-NGP | PSNR, Kitchen / Counter / Bonsai | Cambricon-R | **24.5 → 26.4 / 22.9 → 24.8 / 26.0 → 28.6** | §5.2.1, Table 1 — `sim` **verified** |
| same | Zip-NeRF | PSNR, Kitchen | Cambricon-R | **16.2 → 20.9** (largest gap in Table 1) | Table 1 **verified** |
| Where the quality gain comes from | Instant-NGP | iterations in the same wall-clock | Cambricon-R | **678 → 2027 iterations**, PSNR 23.15 → 25.85, SSIM 0.735 → 0.802 | Fig. 13 **verified** |
| Iso-iteration quality | — | PSNR | dense NSR | ST-NSR is **worse** — *"ST-NSR introduces a slight PSNR loss under the same number of iterations"* | §5.2.1 **verified**; magnitude not quantified |
| Threshold approximation | — | PSNR impact of computing `θ` from **half** the DT | full-DT threshold | **< 0.1** | §4.1 **verified** |
| **GPU-side ST-NSR** | Instant-NGP | speedup on A100 from ST-NSR alone | dense NSR on A100 | **1.55× encoding / 1.19× overall** vs ≥5× theoretical — bank conflicts | §3.3, Fig. 6 — `HW` **verified** |
| A100 structured sparsity | Instant-NGP | 2:4 sparsity applied to the encoding table | dense | **no speedup, −1.5 dB PSNR** | §3.3 **verified** |
| Encoding-stage share on GPU | Instant-NGP | share of runtime | — | **46%** | §3.3 **verified** |
| Cambricon-R's quality ceiling | Instant-NGP | PSNR after its 250 iterations, Kitchen | — | **18.16** | §1 **verified** |
| Iterations to PSNR 25 | Instant-NGP | iteration count | — | **~200** (Fox, small) to **~4,300** (Kitchen, large) | §5.2.2 **verified** |
| GPU equivalent time | — | A100 time to match Cambricon-SR's 0.1 s/scene quality | — | **~2 minutes per scene** | §5.2.1 **verified** |
| **Area/power breakdown** | — | mm² / W at 7 nm-scaled | — | total **234.86 mm² / 356.57 W**; encoding-w/o-SIU **116.41 / 189.00**, MLP **89.79 / 97.48**, SIU **20.17 / 53.81**, sampling **2.64 / 5.62**, update **1.10 / 2.08**, global buffer **3.55 / 4.48** | Table 2 — `synth` **verified** |
| Energy breakdown | — | share | — | encoding **50.06%**, MLP **20.49%**, SIU **16.77%**, **off-chip only 7.68%**, sampling 2.67%, update 2.33% | Fig. 16 **verified** |
| Node & clock | — | — | — | **TSMC 45 nm, 750 MHz**, area/power **scaled to 7 nm** by the method of [44] because the baselines are 7 nm | §5.1.1 **verified** |
| Off-chip model | — | — | — | **HBM2, 1,555 GB/s**, Ramulator; energy **3.9 pJ/bit** | §5.1.1 **verified** |

### Citation hazards

1. **1259× / 1139× (vs A100) must never be quoted bare.** They are accelerator-vs-GPU on a
   memory-irregular training workload, and they pool a **simulated 7 nm-projected** design
   against a **measured 7 nm GPU**. The 4.12× / 2.98× against Cambricon-R is the citable pair.
2. **">80% sparsity with negligible accuracy loss" hides per-scene tuning.** Eight forward
   rates and eight backward rates, each chosen so that scene's PSNR drop stays ≤0.5 dB, on
   the same eight scenes the paper evaluates. No held-out scene. The honest phrasing is
   "80-96% forward sparsity, tuned per scene, at ≤0.5 dB".
3. **The area number and the speedup number come from different tools.** 234.86 mm² is
   45 nm synthesis analytically projected to 7 nm; 4.12× is a cycle-accurate simulator. They
   are not one experiment.
4. **7.54× is a stage throughput, not a system speedup.** The system-level contribution of
   the SIU is the ablation's **3.07×**.
5. **Table 1 is iso-time, not iso-iteration**, and the paper says outright that ST-NSR loses
   PSNR at iso-iteration without saying by how much. The quality claim is entirely
   "more iterations in the same second".

## Cost and requirements

- **Chip.** 234.86 mm², 356.57 W at a 7 nm-projected node — a datacentre-class training chip,
  roughly A100-scale in area and above it in power. Cambricon-R plus **43.0%**.
- **On-chip SRAM.** 40 MB of Sparse Table Array holding ST + gradients, in 16 STAs on a mesh
  NoC. Plus **15 MB of CAM** — this is the price of packing the sparse table, and it costs
  **14.29% of chip area** for pure address translation.
- **Off-chip.** HBM2 at 1,555 GB/s, holding the **128 MB dense table**, which is read every
  iteration for the top-k threshold and the ST regeneration. Cambricon-SR therefore has
  **more** off-chip traffic than Cambricon-R, which kept the whole (dense) table on-chip —
  the paper says so (§5.2.4).
- **Algorithmic requirement.** ST-NSR is a change to the **training loop**, not a
  post-processing step: the dense table must be maintained and gradient-accumulated for
  *every* entry so pruned entries can be restored. There is no PTQ/QAT analogue here — the
  method exists only during training, and the sparsity pattern is re-decided every iteration.
- **Tuning requirement.** A per-scene sparsity rate for the forward stage and another for the
  backward stage, plus a dense-table size chosen by design-space exploration (128 MB). None
  of these is learned; all are set by sweeping against PSNR.
- **What it does *not* require:** no calibration set, no retraining of a released checkpoint
  (there is no checkpoint — the whole workload is per-scene training from scratch), and no
  change to the numeric format of anything.

## Limitations and open questions

**Admitted by the authors**

- Off-chip access to the dense table remains, every iteration, and is strictly worse than
  Cambricon-R on that axis (§5.2.4).
- The SIU wastes **70.7%** of the bitmap it reads, which is **52.8% of the SIU's energy**;
  they argue the 8.85% net energy waste is worth the 3.07× (§5.2.3).
- ST-NSR loses PSNR at equal iteration count (§5.2.1).
- The gains shrink on Zip-NeRF and K-Planes, because their encoding workload dominates and
  the MLP/update optimizations have less to bite on (§5.2.5).

**Not admitted**

- **Per-scene sparsity tuning on the evaluation set.** Sixteen hyperparameters chosen against
  the reported metric, no held-out scene, no sensitivity analysis for a wrong rate.
- **Node projection.** 45 nm → 7 nm by an analytical method, compared against real 7 nm
  hardware, with no discussion of how much of the 4.12× survives the projection's error bars.
- **The CAM is a large and unexamined tax.** 14.29% of the chip to translate addresses — a
  cost created entirely by the decision to pack the sparse table. No alternative (e.g. a
  hashed sparse layout that avoids translation) is costed.
- **Scaling in the sparsity rate is never explored.** Everything is reported at the tuned
  rate; there is no curve of speedup or area efficiency against sparsity, so a reader cannot
  tell how the SIU's design point moves if a workload is only 50% sparse.
- **`F` is never given numerically**, so the paper cannot be reproduced at the byte level
  without recovering it from Instant-NGP.

**Open questions for the survey**

- Does anything here transfer to inference, or to any workload other than NeRF training? The
  paper makes no such claim, and the SUU's premise (≤0.8% of entries change per iteration) is
  a *training-dynamics* observation with no inference analogue.
- Is the "restore pruned entries from an off-chip dense shadow copy" pattern a general
  dynamic-sparse-training primitive? It is the most transferable idea in the paper and the
  paper does not pitch it as one.

## Relation to other entries

**Where it belongs: with the compression/irregular-access cluster, not with any data-type
box.**

- [`SpZip`](../SpZip/ANALYSIS.md) — the direct precedent in this corpus and the model for how
  to treat it. Both make an irregular access pattern cheap while leaving the value
  representation untouched; `SpZip` is already tagged `NON-Q-ORIENTED` with data type `—` and
  generation `—`, and Cambricon-SR should get exactly that. The taxonomy's own worked-example
  table names `SpZip` as the paper with "no quantization at all, only sparse-format
  compression"; Cambricon-SR is the second instance.
- [`CommutativeDataReordering`](../CommutativeDataReordering/ANALYSIS.md) — same family: the
  contribution is where data goes, not what a number is.
- [`Mokey`](../Mokey/ANALYSIS.md), [`EVA`](../EVA/ANALYSIS.md),
  [`OASIS`](../OASIS/ANALYSIS.md) — **tested against these and rejected**, see the sweep
  section. The codebook-objective axis (store through / compute through / skip through) needs
  an original value being represented by an index; a hash grid's index comes from a
  *position* and its entries are the parameters themselves. Recording the rejection is worth
  more than the tag would have been: it is the corpus's clearest example of a **false-friend
  "table"**, and the survey can use it to say what a codebook is by saying what it is not.
- [`AQB8`](../AQB8/ANALYSIS.md) — the useful contrast, and the two are the same venue and
  year. Both are graphics-adjacent ISCA'25 accelerators whose titles promise a
  representation change. AQB8 delivers one (INT8 boxes, a custom FP14 ray) and is
  `Q-ORIENTED`; Cambricon-SR's "encoding table" is the *workload*, and it is not. Reading
  them as a pair is the cheapest way to make the `Q-ORIENTED` test concrete.
- **Sparsity, not quantization, is the axis it lives on.** If the survey ever wants a
  one-paragraph aside on "the other compression thread in architecture", the trio
  SpZip / CommutativeDataReordering / Cambricon-SR is that paragraph.

**Keep or cut? — recommendation: KEEP, as a single background citation, and mark it
excluded from the taxonomy.** Reasons: (i) removing it loses the audit trail — the row and
the ⚠ are *evidence that the corpus was checked*, and a future reader who finds
"Cambricon-SR, ISCA'25, Sparse Encoding Table" in the ISCA'25 proceedings will re-ask exactly
the question this note answers; (ii) it is a working example the survey can cite in one
sentence when it defines what a codebook is, alongside SpZip; (iii) the ISCA venue list is a
*complete* enumeration of a source CSV, so silently dropping a row breaks the "40 rows, all
accounted for" property that the venue README depends on. What it must **not** get is a body
paragraph, a data-type tag, or a generation.

## For the note

### §1 one-line summary

> **No quantization anywhere** — the "encoding table" is Instant-NGP's multiresolution hash
> grid, the entries are the model's own trainable parameters retrieved by a hash of a 3D
> position, and no numeric format or bitwidth is named in the paper (`quantiz*`, `precision`,
> `bitwidth`, `INT8`, `FP16`, `FP32`, `codebook`: **zero hits each**, bibliography included);
> what is built is **dynamic magnitude pruning of that table during NeRF training** (80-96%
> forward, 80-95% gradient, per-scene tuned at ≤0.5 dB PSNR) plus the three pieces of hardware
> that make the sparsity pay — a **Sparse Index Unit that streams the bitmap sequentially and
> lets requests wait for their address to go past** instead of randomly addressing it (7.54×
> encoding throughput for 8.59% area), a **Sparse Update Unit** doing in-place slot
> replacement (−83.5% update traffic) and a **dynamic shared MLP buffer** (−85.3% per unit,
> 4× more units) — buying **4.12× over Cambricon-R at +43% area** on a 45 nm design
> analytically projected to 7 nm.

### Proposed values on their four axes

| Axis | Proposed | Evidence (one line) |
|---|---|---|
| **Level** | **`ALGO+ARCH`** — *seed says `ARCH`; I dispute it* | §3 contributes ST-NSR, *"the first NSR training algorithm with sparse encoding tables"* (their claim, §1/§7), with its own Algorithm 1, its own threshold/top-k rule and its own **GPU-only** evaluation (§3.3: 1.55× / 1.19× on an A100, no Cambricon-SR involved) — an algorithmic result that stands without the hardware. §4-§5 are the accelerator. **`SYS` checked and rejected:** "software stack" 0 hits, "compiler" only Synopsys Design Compiler, no ISA, no runtime, no framework plug-in — the CUDA kernel of §3.3 is an experiment, not a shipped stack. |
| **Q-oriented** | **`NON-Q-ORIENTED`** — seed agrees | Apply the test: swap the format for plain INT8 and ST-NSR's pruning, the SUU's four-way transition classification, the CAM translation, the SIU's sequential-stream-and-match and the dynamic shared buffer **all survive untouched**. Nothing in the design reads, writes, or reasons about the width of a value. |
| **Data type** | **`—`** (leave empty) — *seed says `VQ`; I dispute it* | `codebook`, `centroid`, `dictionary`, `k-means`, `vector quantiz*`: **zero hits each**. The hash-grid index is computed from a 3D coordinate (Eq. 1), not from a value; the entries are the trainable parameters themselves, so nothing is being represented by an index. The only derivable numeric fact in the whole paper is **4 bytes per table entry** (256 KB bitmap ⇒ T=2²¹; 128 MB ÷ 16 levels ÷ 2²¹), and even that is a derivation, not a claim — it belongs in `ANALYSIS.md`, not in a tag. |
| **Generation** | **`—`** (leave empty) — *seed says `G3`; I dispute it* | Generation is a quantization-paradigm axis; a paper with no quantization has no position on it. This follows the corpus's established convention for `non-Q` rows (`ELSA`, `ENEC`, `SpZip` all carry `—` `—`). **Note for the human:** the "do not correct a pre-2023 `G3` seed" rule does not apply — that rule protects deliberate early-codebook/outlier taggings (OLAccel, GOBO, Mokey); this is a 2025 seed inferred from a title. |
| **Optimization** (free text) | `sparsity` `dynamic magnitude pruning` `hash encoding table` `NSR training` `sparse index unit` `sequential bitmap streaming` `sparse update unit` `CAM address translation` `dynamic shared buffer` | The seed's four keywords all hold and are kept; the four added ones name the actual mechanisms, which the seed does not. |

### Proposed venue-list row

```
| [ ] | [Cambricon-SR: An Accelerator for Neural Scene Representation with Sparse Encoding Table](https://doi.org/10.1145/3695053.3731018) | *close read* | ALGO+ARCH | non-Q | — | — | `sparsity` `dynamic magnitude pruning` `hash encoding table` `sparse index unit` `sequential bitmap streaming` `sparse update unit` `CAM address translation` `dynamic shared buffer` `NSR training` | ⚠ **Confirmed on a full read: no quantization at all** — zero hits for quantiz*/precision/bitwidth/INT8/FP16/FP32/codebook/centroid/dictionary, **bibliography included**. The "encoding table" is Instant-NGP's hash grid: the index comes from a 3D position and the entries *are* the trainable parameters, so the seed `VQ`/`G3` is a false friend. Contribution is **dynamic magnitude pruning of that table during training** + a Sparse Index Unit that **streams the bitmap sequentially and makes requests wait for their address** instead of randomly addressing it. Belongs with `SpZip` |
```

*(Changes from the seed at line 47: `ARCH` → `ALGO+ARCH`; `non-Q` unchanged; data type and
generation stay `—` and the reasons are now sourced rather than assumed; the Verified column
goes `*agent brief*` → `*close read*`; the Optimization keywords gain the four mechanisms;
the Note is rewritten to record the **tested-and-rejected** codebook hypothesis rather than
only the absence.)*

*(A second seed correction, at line 180 of the same file: the "Seed-tag corrections" table
entry for Cambricon-SR should have its term list widened — it currently cites 7 terms and
"24 hits for hash, 15 for Instant-NGP"; the correct counts are **29** and **16**, and the
sweep is now ~30 terms plus the bibliography. Reported, not applied.)*

### §4 fairness verdict

**Honest in its choice of baseline, and unfair in its node.**

- **Baseline choice ✓, and better than most.** Both an A100 and the SOTA accelerator are
  reported, and Cambricon-R is **re-implemented in the authors' own cycle-accurate simulator
  "according to its paper"** rather than quoted (§5.1.3) — so the 4.12× is simulator-vs-
  simulator, which is the right kind of comparison even though it means the baseline is the
  authors' model of Cambricon-R.
- **Not iso-node ✗ — the biggest hazard.** Cambricon-SR is RTL, synthesized with Synopsys DC
  at **TSMC 45 nm / 750 MHz**, then **area and power are analytically scaled to 7 nm**
  because "the baseline hardwares operate on a 7 nm node" (§5.1.1). Every area, power and
  energy number is therefore a projection, compared against a real 7 nm GPU. The paper cites
  precedent for the method; that does not make it a measurement.
- **Not iso-area ✗.** 4.12× comes with **+43.0%** chip area over Cambricon-R (§5.2.3). Stated
  plainly by the authors, to their credit, but the headline does not carry it.
- **Not iso-algorithm ✗.** Cambricon-SR runs ST-NSR; Cambricon-R runs dense NSR. The
  architecture and the algorithm change together, and the ablation isolates the *hardware*
  pieces against `Cambricon-SR-plain` (which already runs ST-NSR) — so no experiment isolates
  ST-NSR's contribution on the accelerator. The closest thing is the GPU study (§3.3): ST-NSR
  alone buys **1.19×**.
- **Not iso-iteration ✗, and that is the whole quality claim.** Table 1 compares PSNR/SSIM at
  **equal wall-clock (0.1 s/scene)**, where Cambricon-SR completes ~3× the iterations
  (Fig. 13: 678 → 2027). The paper concedes ST-NSR is *worse* at equal iterations and never
  quantifies by how much.
- **Evidence levels pooled ✗.** Speedup from the authors' simulator + Ramulator; area/power
  from 45 nm synthesis projected to 7 nm; off-chip energy from an analytical 3.9 pJ/bit
  model; the A100 numbers from real hardware. Four kinds of fact in one bar chart.
- **Sparsity is tuned per scene on the evaluation scenes ✗.** Sixteen rates, no held-out set.
- **Numbers not to quote bare.** (i) **1259× / 1139×** — accelerator vs GPU, simulation vs
  measurement, node-projected; quote **4.12× / 2.98×** instead. (ii) **">80% sparsity with
  negligible accuracy loss"** — it is 80-96%, per-scene tuned, and "negligible" is defined as
  ≤0.5 dB PSNR. (iii) **7.54×** — an encoding-stage throughput; the system contribution of
  the SIU is the ablation's **3.07×**. (iv) **4.12×** itself should always be quoted with
  **+43% area**.

## Note from the source list

> _(no keywords recorded in the source CSV)_

## Abstract (verbatim, from the archived PDF)

> Neural Scene Representation (NSR) is a promising technique for representing real scenes. By
> learning from dozens of 2D photos captured from different viewpoints, NSR computes the 3D
> representation of real scenes. However, the performance of NSR processing running on GPU is
> insufficient for applications. Cambricon-R achieves high performance of more than 60 scenes
> per second, but at the cost of modeling quality. In this paper, we propose Cambricon-SR, an
> algorithm-hardware co-designed accelerator to improve NSR performance and quality. First, we
> propose a novel NSR algorithm with sparse encoding table, it achieves more than 80% of
> sparsity for the encoding table with negligible accuracy loss. Second, to efficiently
> eliminate the invalid memory access requests to the pruned entries, we propose the sparse
> index unit based on sequential SRAM access to address the challenge of irregular memory
> access to the sparse structure bitmap. It achieves a throughput increase of 7.54× for the
> encoding stage with an additional area overhead of 8.59%. Third, we propose the dynamic
> shared buffer for the MLP units to reduce the buffer usage by 85.3% so that we can increase
> the number of the MLP units. We conduct experimental evaluations on 8 typical scenes. The
> results demonstrate that, compared with A100 GPU and Cambricon-R, Cambricon-SR achieves
> 1259× and 4.12× speedup, and reduces the energy consumption by 1139× and 2.98× for each
> training iteration of NSR, respectively.
