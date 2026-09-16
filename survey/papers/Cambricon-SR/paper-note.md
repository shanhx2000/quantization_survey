# Cambricon-SR: An Accelerator for Neural Scene Representation with Sparse Encoding Table

**Venue / Year:** ISCA 2025, pp. 1254-1268 · **Link:** https://doi.org/10.1145/3695053.3731018 · **Reader:** Haoxuan · **Date:** 2026-09-14

## Tags

| | |
|---|---|
| **Level** | `ALGO+ARCH` |
| **Q-oriented** | `NON-Q-ORIENTED` |
| **Data type** | `—` |
| **Generation** | `—` |
| **Optimization** | sparsity · dynamic magnitude pruning · hash encoding table · sparse index unit · **sequential bitmap streaming** · sparse update unit · CAM address translation · dynamic shared buffer · NSR training |

## 1. One-line summary

**No quantization anywhere** — the "encoding table" of the title is Instant-NGP's
multiresolution hash grid, whose index comes from a 3D position and whose entries *are* the
model's trainable parameters, and no numeric format or bitwidth is named in the paper
(`quantiz*`, `precision`, `bitwidth`, `INT8`, `FP16`, `FP32`, `codebook`, `centroid`:
**zero hits each**, bibliography included); what is built is **dynamic magnitude pruning of
that table during NeRF training** (80-96% forward, 80-95% gradient, per-scene tuned at
≤0.5 dB PSNR) plus the three pieces of hardware that convert the sparsity into fewer memory
requests — a **Sparse Index Unit that streams the bitmap sequentially and makes requests wait
for their address to go past** instead of randomly addressing it (7.54× encoding throughput
for 8.59% area), a **Sparse Update Unit** doing in-place slot replacement (−83.5% update
traffic), and a **dynamic shared MLP buffer** (−85.3% per unit → 4× units) — buying **4.12×
over Cambricon-R at +43% area**, on a 45 nm design analytically projected to 7 nm.

## 2. Data type

**There is none.** `quantiz*` 0 · `precision` 0 · `bitwidth`/`bit-width` 0 · `INT8`/`INT4` 0 · `FP32`/`FP16`/`FP8`/`BF16` 0 · `fixed-point` 0 · `mantissa`/`exponent` 0 · `numeric`/`data type`/`word length` 0. `bit`/`bits` appear 6 times, all addressing (`upper 4 bits of the address`, `1 bit per entry`, `3.9 pJ/bit`). Bibliography: 0 quantization or compression citations.

**Formats per tensor class.** Not stated — not for table entries, not for table gradients, not for MLP weights or activations. The MLP is "512 units, each two 32 × 32 MAC arrays": array dimensions, not operand widths.

**The one derivable number: 4 bytes per encoding-table entry.** 256 KB bitmap at 1 bit/entry → T = 2²¹; 128 MB dense table ÷ 16 levels ÷ 2²¹ = 4 B. Cross-checks: ST ≤ 26 MB ≈ 128×0.20; gradients ≤ 14 MB ≈ 128×0.11. Splitting 4 B into `F` elements needs `F`, which the paper never gives numerically (Instant-NGP's default `F=2` would make it FP16 — external, not this paper's).

**Granularity.** Of *pruning*, not of scaling: one flag per table entry, i.e. per `F`-dim feature vector. Group size = 1 entry = 4 B.

**Outliers.** No concept. Magnitude is used the other way round — small entries are pruned.

**Escape hatch.** A **128 MB off-chip dense shadow table**, kept at full size and gradient-accumulated for *every* entry so pruned entries can be restored (Fig. 9: an entry climbing 0.1 → 6). The sparsity is in the on-chip copy only.

**PTQ vs QAT.** Neither applies — there is no checkpoint. NSR trains from scratch per scene; ST-NSR is a change to the training loop, and the sparsity pattern is re-decided every iteration by top-k on the dense table.

**Codebook test, run and failed.** Tested against the store-through / compute-through / skip-through axis (Ecco / EVA / Phi): all three need an original value that an index represents more cheaply. Here the index is `h = (π₁x ⊕ π₂y ⊕ π₃z) mod T` on a coordinate, and the entries are the parameters — no encode step, no reconstruction, no error. `VQ` is a false friend.

**Swap-for-INT8 test.** Everything survives: the pruning rule, the four-way transition classifier, the CAM, the SIU, the shared buffer. Nothing in the design reads the width of a value.

## 3. Optimization

**ST-NSR — dynamic magnitude pruning with regrowth (the algorithm).** Three edits to the training loop: encode against the pruned sparse table (ST); prune a backward feature-gradient vector when *all* its dimensions fall below θ; accumulate gradients into an off-chip **dense** table (DT), then set θ by top-k on the updated DT for a pre-set sparsity rate and regenerate ST. The DT exists solely so pruned entries can come back — this is dynamic sparse training with regrowth, uncited as such. Sizing by sweep at a ≤0.5 dB budget: DT 128 MB → ST ≤ 26 MB + gradients ≤ 14 MB → 40 MB on-chip. GPU-only version: **1.55× encoding / 1.19× overall** on an A100 against a ≥5× theoretical memory saving — the gap is shared-memory bank conflicts, and that gap is the whole argument for the chip.

**Sparse Index Unit — an access-pattern inversion, and the real contribution.** STA sustains 256 req/cycle and ~86% of requests hit pruned entries, so the filter needs ~1800; target 2048. *Don't address the bitmap — stream it.* Each Sequential Access Unit reads 4 B/cycle with its address in a register; requests sit in a buffer and are matched against the pointer as it goes past. Three costed rejections make the case: 2048-bank + 2048×2048 crossbar (**EDA cannot route it**; hash-random addresses also unbalance banks, 83% throughput loss); one SAU (buffer for **1,059,584** requests, **418 mm²**); many SAUs all-to-all (comparison network **123 mm² = 52.37% of chip**). Fix is **nearest grouping** — route each request only to the SAU whose pointer will reach it soonest, turning one `mn×m` network into `m` independent `n×1` networks: **6.40 mm², 2.73%**. Final 32 blocks × 16 SAUs, 192 req/buffer, **20.17 mm²**. **7.54× encoding throughput for 8.59% area**, 5.88× over the crossbar, **3.07× system** in the ablation. Authors volunteer the tax: 70.7% of bitmap reads are unused = 52.8% of SIU energy; SIU is **16.77% of chip energy at 8.59% of area**.

**Sparse Update Unit — out-of-order storage, in-place replacement.** Off-chip DT access was **72.1%** of runtime (13.0% DT update + 59.1% ST regeneration). Two observations: after iteration 20, **≤0.8%** of entries change sparsity state per iteration, and because θ comes from a fixed *rate*, insertions ≈ deletions. So changed entries are classified four ways (sparse→sparse skip; dense→dense write in place; sparse→dense into Queue A; dense→sparse into Queue B) and each cycle B's freed slot receives A's new entry, CAM updated to match. Residual imbalance ~0.03%, absorbed by redundant capacity. **6.06× fewer update-stage accesses (−83.5%), 5.28× faster, 1.24× system.**

**The cost of packing the table: 15 MB of CAM, 33.56 mm², 14.29% of the chip.** Compact ST storage means every hash-produced dense address needs translating to a sparse address. Blocked for match energy — 16 blocks × 160 entries per node, block selected by the upper 4 address bits, ~2,500 entries/node. Pure address translation, and the single largest unexamined tax in the design; no translation-free layout is costed.

**Dynamic shared MLP buffer.** Cambricon-R sizes each MLP unit's buffer for the worst-case ray → **20.29%** utilisation. (i) 32 units share one buffer in 32-point blocks with flag-register allocation (64-way rejected: crossbar area). (ii) Within a ray, a dead tensor's space is reused by a later one — layer 5's input activation dies once its gradients exist — **−49.42%** alone. Together **−85.31%** per unit, utilisation **69.49%**, so **512 MLP units** (4×) fit with the module's *total* buffer **down 41%**; the naive 4× would have needed **+144 MB**. **3.92× MLP stage, 1.36× system.**

**Negative result worth keeping.** A100 2:4 structured sparsity is useless twice over: Tensor-Core 2:4 accelerates MACs while ST-NSR's sparsity is in memory access, and forcing 2:4 onto the encoding table gives **no speedup and −1.5 dB PSNR** (table accesses are irregular single-entry lookups).

## 4. Results

| | |
|---|---|
| Baseline | **A100 GPU** (measured, official Instant-NGP CUDA) and **Cambricon-R** (ISCA'22-lineage NSR training accelerator, **re-implemented by the authors in their own simulator**, not quoted). Ablation vs `Cambricon-SR-plain`, which already runs ST-NSR |
| Models / datasets | Instant-NGP, Zip-NeRF, K-Planes × 8 scenes (Fox, Ficus, Hotdog, Mic from NeRF-Synthetic/Instant-NGP; Bonsai, Room, Counter, Kitchen from Mip-NeRF-360). Runtime/energy taken at the iteration count reaching **PSNR 25** |
| Accuracy delta | **PSNR/SSIM, not accuracy.** Sparsity budget is **≤0.5 dB** PSNR at **per-scene tuned** rates (forward 80-96%, backward 80-95%, 16 hyperparameters, no held-out scene). Iso-time (0.1 s/scene) Cambricon-SR **wins**: Instant-NGP Kitchen 24.5→26.4, Counter 22.9→24.8; Zip-NeRF Kitchen 16.2→20.9. **Iso-iteration it loses** — conceded, never quantified. The win is iterations: 678 → 2027 in the same second. Half-DT threshold approximation: <0.1 dB |
| Speedup | Geomean **1259× vs A100** / **4.12× vs Cambricon-R**. Ablation: SUU 1.24× → shared buffer 1.36× → SIU 3.07×. Stage-level: encoding 7.54×, update 5.28×, MLP 3.92×. ST-NSR on GPU alone: 1.19× |
| Energy / area | Energy **1139× / 2.98×**. **234.86 mm², 356.57 W** — Cambricon-R **+43.0%**. Breakdown: encoding-w/o-SIU 116.41 mm², MLP 89.79, **SIU 20.17 (8.59%)**, **CAM 33.56 (14.29%)**. Energy: encoding 50.06%, MLP 20.49%, SIU 16.77%, off-chip only 7.68% |
| Technology node | **TSMC 45 nm, 750 MHz** (Verilog RTL + Synopsys DC), **area and power analytically scaled to 7 nm** to meet the 7 nm baselines. HBM2 1,555 GB/s; off-chip energy 3.9 pJ/bit |
| Evidence level | **Four kinds pooled:** authors' cycle-accurate simulator + Ramulator (speedup); 45 nm synthesis projected to 7 nm (area/power); analytical 3.9 pJ/bit (off-chip energy); real A100 (GPU baseline). No silicon |
| **Is the comparison fair?** | **Not iso-node** (45 nm synthesis projected to 7 nm, vs 7 nm baselines); **not iso-area** (+43%); **not iso-iteration** (Table 1 is iso-wall-clock); simulator, synthesis, analytical DRAM and measured GPU pooled. Baseline choice good — Cambricon-R re-implemented, not quoted. **Not to quote bare:** 1259×/1139× (DSA vs GPU); 7.54× (stage, not system — 3.07×); ">80%, negligible loss" (80-96%, per-scene tuned, ≤0.5 dB) |

## 5. Comment

No quantization.

## 6. Claude notes

*Suggestions from the reading agent. **Strip this section before copying into
`QuantArchSurvey/venues/ISCA/notes/`.***

- **Read depth.** Full close read of §1-§7 (pp. 1254-1267). Two honest gaps: (i) **Figures 3, 4, 6, 11, 12, 14-19 are raster images** and were *not* rendered to PNG — every number above is the one the prose states, and no per-scene bar was read off a plot; the per-scene sparsity rates and Table 1/2 did extract as text and were read in full. (ii) The **reference list was read by grep, not entry by entry** — the load-bearing fact there is that `quantiz|compress|precision|bit-width|low-bit` over both reference pages returns **zero**. Nothing load-bearing is unresolved *except* that the paper genuinely never states a format, which is the finding rather than a gap.
- **The negative claim was re-tested, not rubber-stamped.** ~30 terms over the full text plus the bibliography, against a specific alternative hypothesis (hash-table/feature-grid = codebook in all but name). Counts in `ANALYSIS.md`. **The prior brief's counts were slightly wrong** — `hash` is 29 not 24, `Instant-NGP` 16 not 15 — worth fixing at `venues/ISCA/README.md` line 180 when you touch it.
- **Three seed-tag disputes**, all reported not applied. `ARCH` → **`ALGO+ARCH`**: §3 is an algorithm with its own Algorithm 1, its own top-k/threshold rule and its own GPU-only result (1.55×/1.19×, no Cambricon-SR involved) — it stands without the hardware, and they claim it as "the first NSR training algorithm with sparse encoding tables". `SYS` checked and rejected: "software stack" 0, "compiler" only Synopsys DC, no ISA, no runtime. `VQ` → **`—`** and `G3` → **`—`**: evidence above; note the "don't correct a pre-2023 `G3` seed" rule protects deliberate early-codebook taggings (OLAccel/GOBO/Mokey) and does not cover a 2025 seed inferred from a title.
- **Keep it in the corpus, as one background citation — do not cut the row.** Three reasons: the row and its ⚠ *are* the audit trail (a future reader who sees "Sparse Encoding Table" in the ISCA'25 proceedings will re-ask exactly this question); it is the corpus's cleanest **false-friend "table"**, so the survey can define what a codebook *is* by naming what it is not, in one sentence alongside `SpZip`; and the ISCA list is a complete enumeration of the source CSV, so dropping a row breaks the "40 rows, all accounted for" property. What it must not get is a body paragraph, a data-type tag, or a generation.
- **§5 material, if you want it.** Placement: **not in any data-type box** — it goes with `SpZip` and `CommutativeDataReordering` as "the other compression thread in architecture", where the contribution is making an irregular access pattern cheap and the value representation is untouched. The taxonomy's worked-example table already names `SpZip` as the no-quantization case; Cambricon-SR is the second instance and the pair is the paragraph. Generation: `—` deliberately, because generation is a quantization-paradigm axis and a paper with no quantization has no position on it — matching `SpZip`, `ELSA`, `ENEC`.
- **Read it as a pair with [`AQB8`](../AQB8/ANALYSIS.md).** Same venue, same year, both graphics-adjacent, both with titles promising a representation change. AQB8 delivers one (INT8 boxes, custom FP14 ray) and is `Q-ORIENTED`; Cambricon-SR's "encoding table" is the *workload*. Cheapest way to make the `Q-ORIENTED` test concrete for a reader.
- **The number I would exclude: 1259× and 1139×.** Accelerator-vs-GPU on a memory-irregular training workload, and they pool a **simulated, node-projected** design against a **measured** GPU. Quote 4.12× / 2.98× — and always with **+43% area**, which the headline omits.
- **The most transferable idea, and the paper doesn't pitch it.** *"Don't randomly address the bitmap — stream it sequentially and make the requests wait for their address to go past."* That is a general answer to "how do you filter N irregular requests per cycle against a sparsity metadata structure", and the three costed rejections (418 mm² / 123 mm² / EDA-cannot-route) make it citable for the *design-space* argument even in a quantization survey — outlier-metadata filtering has the same shape. If the survey ever wants one non-quantization sentence from this paper, that is it.
- **The 14.29%-of-chip CAM deserves a raised eyebrow.** The entire cost exists because the sparse table is stored *compactly*; no translation-free layout is costed anywhere. It is the paper's own biggest overhead and its least examined decision.
