# AQB8: Energy-Efficient Ray Tracing Accelerator through Multi-Level Quantization

**Venue / Year:** ISCA 2025, pp. 374-387 · **Link:** https://doi.org/10.1145/3695053.3731104 · **Reader:** Haoxuan · **Date:** 2026-09-14

## Tags

| | |
|---|---|
| **Level** | `ALGO+ARCH` |
| **Q-oriented** | `Q-ORIENTED` |
| **Data type** | `INT8` `FP14` `INT32` `FP32` `MIXED` |
| **Generation** | `G2` |
| **Optimization** | ray tracing · BVH · anchor + INT8 offset · per-cluster scale · **quantize the ray, not the box** · hierarchical local frames · SAH-derived clustering DP · custom FP14 · power-of-two ray scale · conservative outward rounding |

## 1. One-line summary

Groups every ~30-110 BVH nodes into a cluster with one **FP32 anchor box as a local
coordinate frame** and stores the rest as **six INT8 offsets** under a single isotropic
per-cluster scale `S_x = max(l_x,l_y,l_z)/255` — then inverts what every prior BVH
compression scheme does by **quantizing the ray into the box's frame instead of decompressing
the box into the ray's** (inverse direction as a custom **FP14** 1s/8m/5e, origin term as
INT32, ray scale fixed at `2⁻⁷` so the rescale is a shift), turning the ray-box test into
INT8 multiply → variable left shift → 2's complement → INT32 add, which buys a **5.1× smaller
box unit**, **−27% RT-accelerator area**, **−70% DRAM traffic** and **1.82× geomean** — at
+3-6% ray-box and +6-31% ray-triangle tests, with **no image-quality metric anywhere**.

## 2. Data type

**Not a DNN.** Tensor classes here are BVH bounding boxes, the ray, and triangles — read the rows below in that frame.

**Bounding boxes.** Six **INT8** per box, in the anchor's `[0,255]³` frame. Anchor box itself: six **FP32** (24 B).

**Ray.** Inverse direction `q_w` in a custom **FP14** (1 sign, 8 mantissa, 5 exponent) — chosen because `w = 1/d` has density `1/(2w²)` for `|w| ≥ 1`, so float resolution near zero matches the distribution. Origin term `q_b` in **INT32**.

**Scales.** `S_w = 2⁻⁷` fixed and global → the rescale is a shift, not a multiply. `S_x` per cluster, **isotropic** (one scale for x/y/z, because the slab test compares `t` across axes). `S_w S_x` stored once per cluster as FP32.

**Granularity.** Per-cluster, cluster = **~30-110 nodes** (anchors are 0.9-3.3% of nodes) — a new local frame every ~5-7 binary levels. Boundaries chosen by DP over a modified SAH cost, `O(n(log n)²)`.

**"Multi-level" ≠ multiple bitwidths.** It means **nested local coordinate frames at multiple BVH depths**, count scene-dependent, not a precision ladder.

**Effective bitwidth.** 8 + ~0.5 amortised anchor ≈ **8.5** bits per BB coordinate.

**Outliers.** None — no outlier concept. The wide-dynamic-range problem is solved by re-anchoring the frame, not by an outlier path.

**Escape hatch.** Ray-**triangle** tests stay **FP32**, entirely untouched — and become **55%** of compute energy (from 30%). Anchor tests are FP32 too.

**Correctness, not accuracy.** Box bounds round **outwards** → quantized box encloses the FP32 box → false positives only, no missed hits. Stated for the box; **the ray side's FP14/INT32 rounding is never analysed**.

**Retraining.** N/A — no training anywhere. Works on any BVH from any builder.

## 3. Optimization

**Anchor + offset, hierarchically.** Build a standard BVH with any builder, then partition it into clusters. Each cluster keeps one FP32 anchor BB defining a `[0,255]³` frame; every other node stores its two child boxes as six INT8 each in that frame, rounded outwards. Cluster boundaries come from a dynamic program over a modified SAH cost with per-node `SWITCH`/`STAY` policies — brute force is `O(2ⁿ)`, optimal substructure gives `O(n(log n)²)`.

**The inversion — quantize the ray.** This is the thesis. Prior schemes (Ylitie et al.) decompress the box to FP32 to test it, which is why `Compress-2` *increases* compute energy (+9%). AQB8 instead pushes the ray into the box's frame: substituting `t = S_w S_x q_t`, `w = S_w q_w`, `x = S_x q_x`, `b = S_w S_x q_b` into `t = wx + b` **cancels `S_w S_x` on both sides**, leaving `q_t = i_w · 2^{r_w} · m_w · q_x + q_b`. Only `q_b` depends on the cluster, so only `q_b` is recomputed on a switch.

**QBOX.** Six lanes of INT8 multiply → left shift by `r_w` → 2's complement if signed → INT32 add, feeding INT32 MIN/MAX/CMP — against the FP32 unit's six FP32 MUL + ADD into FP32 MIN/MAX/CMP. **5.1× smaller, 5.7× lower energy per op.**

**A ratio change, not a reconfigurable datapath.** The accelerator keeps the same unit types and changes the mix: 51 FP32 BOX → **9 FP32 BOX + 53 QBOX**, with TRV modified for cluster-switch logic (+24% area) and BOX modified to also compute `qRay` (+18%). Node record 56 B → **16 B**, plus 36 B per cluster; whole tree ≈30% of baseline.

## 4. Results

| | |
|---|---|
| Baseline | **Baseline** (all BBs FP32) and **Compress** (all BBs INT8 per Ylitie et al., decompressed to FP32 to test) — the latter is the real prior art. 2-ary and 6-wide variants; all three share tree topology |
| Models / datasets | 7 scenes; 2-ary tree from `madmann91/bvh`, 6-wide from Embree. Vulkan-Sim GPU model, 30 SMs |
| Accuracy delta | **No image-quality metric is reported anywhere** (PSNR/SSIM grep: zero hits). Cost is extra work: **+3-6%** ray-box, **+6-31%** ray-triangle, +20% TRV ops |
| Speedup | Geomean **1.82×** (2-ary) / **1.43×** (6-wide) vs uncompressed. **vs Compress: 1.39× / 1.20×** |
| Energy / area | Energy −29-49%, **mean 42%**. Area **−27%** (≈6.8 → 5.0 mm²). QBOX vs FP32 BOX: **5.1× area, 5.7× energy/op**. Memory: L1D −74%, L2 −60%, **DRAM −70%** (all means) |
| Technology node | TSMC 40 nm (Catapult HLS + Design Compiler + PrimePower) |
| Evidence level | **Three setups, not interchangeable:** post-synthesis (area); replay model at 1 spp with *unlimited bandwidth and zero latency* (energy); Vulkan-Sim cycle-level (traffic, speedup). No silicon; the RT-unit baseline is itself a model |
| **Is the comparison fair?** | Iso-node (40 nm, same flow), iso-topology (stated design goal), iso-throughput (modelled — units extrapolated, not measured). **No iso-accuracy: no image-quality metric exists.** Not one experiment — 70%/1.82× Vulkan-Sim, 49% energy a zero-latency replay, 27% area synthesis. **Not to quote bare:** 49% (max; mean 42%), 1.82× (vs uncompressed; vs prior art 1.39×) |

## 5. Comment

**Could also be read as `NON-Q-ORIENTED`.** What the architecture actually requires is *a*
mixed-precision scheme — not specifically the anchor + INT8-offset combination this paper uses.
Swap in another mixed-precision representation of the same boxes and the traversal, the clustering
DP and the unit-mix argument all still stand.

**Not an LLM paper.** Ray tracing; nothing here transfers to LLM inference directly.

## 6. Claude notes

*Suggestions from the reading agent. **Strip this section before copying into
`QuantArchSurvey/venues/ISCA/notes/`.***

- **Read depth.** Full close read of §1-§8 including Algorithm 1 and all tables. Two things I could not resolve: (i) §7.1 says "AQB8" without the `-2`/`-6` suffix while Fig. 12 plots both, so the memory-traffic percentages cannot be pinned to a configuration; (ii) whether Fig. 14's ray-box count excludes anchor tests — Table 3 arithmetic suggests it does (+4.2% QBOX-only matches §7.3's 3-6%, but +19% including anchors), though the two are different workloads. Both marked in `ANALYSIS.md`.
- **Seed-tag dispute: `ARCH` → `ALGO+ARCH`.** The paper's own §8: *"our work differentiates itself by **co-designing** a BVH structure and a corresponding RT accelerator"*, and §4.3 contributes a modified-SAH cost function plus an `O(n(log n)²)` DP that **no hardware executes**. Checked `SYS` explicitly and it does not apply — no ISA, no compiler, no runtime, Vulkan unmodified.
- **Data type: I would add `FP14` and `INT32`.** `FP14` is a **new token** for the vocabulary — drop it if you would rather keep it closed, but the format is genuinely custom and named as such in §4.4.1. `INT32` is the one to drop first if the cell runs long. **Explicitly not `POW2`** (`S_w = 2⁻⁷` is a scale factor, not a value encoding — same distinction you drew on Tender) and **explicitly not `BFP`** (each `w` carries its own 5-bit exponent; nothing shared across a block).
- **The number I would exclude: "82.13 mm²"** for the FP32 BOX unit. Table 3's area column is labelled `mm²` but Fig. 15's axis is µm², and the totals only reconcile at **×10³ µm²** — the whole baseline RT accelerator is ≈6.8 mm², not 6815 mm². Quote the **ratios** (5.1× area, 5.7× energy/op) instead; they are unit-free and the authors built them.
- **Best-citation claim.** This is the corpus's clean example of **"quantize the consumer, not the producer."** Every outlier/compression paper we have read decompresses to compute; AQB8 pushes the *other* operand into the quantized frame so the scales cancel algebraically. That inversion, not the INT8 boxes, is the transferable idea — and `Compress-2`'s **+9% compute energy** is the authors' own evidence for why it matters.
- **§5 material, if you want it.** `G2`, confidently, and it is a useful data point *because* it is 2025: none of the three G3 threads is present (no outliers, no weight-only bandwidth argument, no codebook, no LLM), yet it both designs a numeric type and builds an architecture to execute it — the G2 test, passed twice. A reminder that generation tracks paradigm, and that non-LLM domains are still living in G2.
- **Cross-paper placement.** On the **granularity** axis it sits between per-region (DRQ) and per-group, but with a twist none of the others have: the group is chosen by a **cost-model DP over a tree**, not by a fixed size. On **outlier currency** it pays nothing — it re-anchors the frame instead, which is arguably the cheapest currency in the corpus and only works because the data is spatial. Worth naming as a distinct entry: **"re-anchoring"** as an alternative to paying for outliers.
- **Where the escape hatch bites.** FP32 ray-triangle goes from 30% to **55%** of compute energy. Amdahl is already the binding constraint on this design, and the paper does not say so.
