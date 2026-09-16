# AQB8 — paper notes

**AQB8: Energy-Efficient Ray Tracing Accelerator through Multi-Level Quantization**
Yen-Chieh Huang, Chen-Pin Yang, Tsung Tai Yeh (National Yang Ming Chiao Tung University)
**ISCA 2025**, pp. 374-387 ｜ DOI: **10.1145/3695053.3731104**
Publication info verified 2026-09-09: venue, year, page range **and DOI** all read out of the
archived PDF's own text (ACM reference-format block and page footers on p1/p14).
Archived here: the **published ACM version**, 14 pages.

Status: **note ready** ｜ Last updated: 2026-09-14 ｜ **Human-checked 2026-09-14** — tags confirmed; §5 supplied by the human.
Tags: `analytical-dtype` `new-data-type` `combined-dtype` `mixed-precision` `dtype-granularity` `accelerator`
How far it was read: **full close read of §1-§9** (pp. 374-387). Read line by line: §1
(motivation, Fig. 1), §2.3 (traffic breakdown), §3 (multi-level quantization), §4.1-§4.7
(box quantization, the SAH-derived cost function, the clustering DP, ray quantization, the
quantized ray-box derivation, memory layout, Algorithm 1), §5 (architecture), §6
(methodology, both evaluation setups), §7.1-§7.5 (every result), §8-§9. **Table 1, Table 3
and Figures 11-16 are raster images in the text extraction and were read by rendering the
PDF pages to PNG** (`pdftoppm`) — Table 1 and Table 3 are transcribed in full below;
Figures 12/13/14/16 were read for the MEAN bar and the shape of the per-scene spread, and
**per-scene bar values were not transcribed** (the prose gives every range and mean quoted
here). Not resolved, itemised in `## 6. Claude notes` of `paper-note.md`: (a) whether the
Vulkan-Sim performance runs use the same extrapolated unit counts as the Fig. 15 area
comparison; (b) whether Fig. 14's "ray-box intersection test" count includes the anchor-BB
tests (Table 3 suggests it does not); (c) whether ray quantization is conservative — the
paper proves the *box* side is and never discusses the *ray* side. Every number in the
table below carries its frame and an evidence marker.

> Publisher record: https://dl.acm.org/doi/10.1145/3695053.3731104
> **There is no arXiv version** (arXiv API title search, 2026-09-02). The PDF was downloaded by
> a human and filed through [`survey/uploads/`](../../uploads/) — the sanctioned route when the
> arXiv-only rule leaves a paper unreachable; see
> [`Notes-002`](../../../Claude/notes/Notes-002-paper-source-access.md).
> The PDF is **not committed** (5.6 MB) and **cannot be re-downloaded by script** — both
> publishers 403. Re-extract with `python3 extract.py` → `extracted/` (committed).
> Authors publish code at https://github.com/nycu-caslab/AQB8 (this is the link the source CSV
> carried; it is a repo, not the paper). **The code was not consulted** — this is a
> paper-only read, so the status is `analysis ready`, not `thorough ready`.
>
> **Why this paper is in the survey**: from the source list
> `Quantization Architecture Survey - ISCA.csv`, ISCA 2025 row.

---

## What the close read changed in the brief

**Five changes; the substance of the brief survived.** (1) The false-positive cost was
understated — 3-6% is the **ray-box** figure alone; **ray-triangle tests rise 6-31%**, and
Table 3's operation counts imply total ray-box *work* rises ~19% once the anchor tests are
counted. (2) The abstract's **"49% energy reduction" is the per-scene maximum**; §7.2 gives
the mean as **42%**. (3) The 1.82× is the **2-ary** configuration against an *uncompressed*
FP32 baseline; the 6-wide configuration gives **1.43×**, and against the INT8-compressed
baseline the gains are **1.39× / 1.20×**. (4) **There is no image-quality metric anywhere in
the paper** — no PSNR, no SSIM, no rendered comparison (full-text grep, zero hits);
correctness is argued *structurally*, from conservative outward rounding of the box, and the
ray side of the rounding is never discussed. (5) The FP14 field order is the paper's own
"1 sign bit, 8 mantissa bits, and 5 exponent bits" — same widths the brief recorded, listed
in a different order; **the seed row's `custom FP14` and `power-of-two ray scale` are both in
the paper's own text and both stand.**

---

## Brief

### 1. Motivation

Ray tracing walks a bounding-volume-hierarchy tree whose bounding boxes are conventionally
FP32. That costs twice: memory traffic for the large boxes, and FP32 arithmetic units for the
ray-box intersection tests. Prior work compressed the boxes to 8 bits — but **decompressed
them back to FP32 to do the intersection test**, so it bought bandwidth and left the compute
and energy cost untouched. Bounding boxes are **69% of L1D bytes and 74% of DRAM bytes**
(§2.3, Fig. 5) **verified**, and naively dropping the whole traversal to FP16 inflates ray-box
tests up to **2.7×** and ray-triangle tests up to **19.6×** (§1, Fig. 1) **verified** — so the
problem is not "can boxes be made smaller" but "can the *test* be done in low precision
without the box growing".

### 2. Overview

**Multi-level quantization.** BVH nodes are grouped into clusters. Each cluster keeps one
**anchor bounding box in FP32** as its reference frame, and every other box in the cluster is
stored as **six INT8 coordinates in the anchor's local [0, 255] frame**, with a single
**isotropic** per-cluster scale `S_x = max(l_x, l_y, l_z)/255` taken from the anchor's own
extent. The ray is quantized too: the inverse-direction component `w = 1/d` uses a fixed
power-of-two scale `S_w = 2⁻⁷` and a **custom 14-bit float (1 sign / 8 mantissa / 5 exponent)**,
and the origin term `b = -o/d` becomes **INT32**, re-quantized whenever traversal crosses into
a new cluster. The intersection test then runs **directly on the integers** — no conversion
back to FP32 during traversal. The paper's own framing of the inversion: *"we take a reverse
approach: we transform the ray to fit the quantized BBs"* (§4.4) **verified**.

### 3. Pros and cons

**Pros**

- Attacks the part prior compression work conceded: the *arithmetic*, not just the storage.
  Anchoring to a high-precision reference is what keeps the INT8 error from inflating the
  traversal step count.
- The whole numeric design is legible and self-consistent — per-cluster scale derived from the
  anchor extent, power-of-two ray scale so that rescaling is a shift, a custom float sized to
  the actual distribution of the inverse ray direction (`f(w) = 1/2w²` for `|w| ≥ 1`, §4.4.2).
- Reports area **down** 27% alongside the energy and traffic wins, which is the honest way to
  present a format change: the cheaper unit is why the energy fell. The area comparison is
  built at **matched throughput** — extra TRV/TRIG units are added to AQB8 to pay for its
  extra traversal steps *before* the comparison is taken (§6.3.2, Fig. 15).
- The escape hatch is genuinely cheap: **~0.5 amortised bits per box coordinate** for the FP32
  anchors (derived from Table 1 + §4.6).
- Code is public.

**Cons**

- Quantization error inflates the box, causing false positives: **+3-6% ray-box tests, +6-31%
  ray-triangle tests, +20% TRV operations**. The speedup is net of a real algorithmic loss,
  and it is larger than the brief previously recorded.
- The FP32 anchors, the FP14 ray format, the INT32 origin term and the **entirely unmodified
  FP32 ray-triangle unit** are all escape hatches — the "8-bit" headline describes the box
  payload, not the datapath. After quantization the untouched TRIG unit becomes **~55% of
  compute energy** (derived from Table 3), i.e. the paper's own success moves the bottleneck
  into the part it did not touch.
- **No image-quality metric of any kind.** The correctness argument is structural and applies
  only to the box; the ray-side rounding is never analysed.
- Baseline is a *model* of a GPU RT accelerator (Vulkan-Sim's RT unit, [56]) at TSMC 40 nm, not
  silicon and not a commercial GPU; the 1.82× is simulated, 2-ary, and against an uncompressed
  baseline.
- The two evaluation setups use **different cache hierarchies** (energy: 32 KB L1 / 1 MB L2;
  Vulkan-Sim: 64 KB L1 per SM / 3 MB L2), so the traffic and energy numbers must not be pooled.
- Cluster construction is an offline build-time step; only its **complexity** is given
  (`O(n(log n)²)` vs `O(n log n)`), never a measured build time.

### 4. Where it applies

The corpus's only **ray tracing** entry, and unexpectedly one of its cleanest examples of a
**combined / residual data type** — a value stored as high-precision reference plus low-bit
offset. That is structurally the same move as [`AQuant`](../AQuant/ANALYSIS.md) (reference
token + INT delta), [`SmartExchange`](../SmartExchange/ANALYSIS.md) (basis × coefficients) and
[`SingularBit`](../SingularBit/ANALYSIS.md) (rank components at different precision), reached
from a completely different workload. Also a **granularity** entry: the cluster is the group,
and the group's scale comes from its own geometry.

---

## Conclusions

**The paper's thesis is an inversion, not a format.** Every prior BVH compression scheme it
cites brings the *box* to the ray's coordinate system (decompress to FP32); AQB8 brings the
*ray* to the box's coordinate system, and the whole design — the isotropic per-cluster scale,
the FP14 inverse direction, the INT32 origin term, the power-of-two `S_w` — exists to make
that direction of conversion cheap and to make it happen once per cluster rather than once per
box. The number that makes the case is not 1.82×: it is that the paper's own INT8-compressed
baseline (`Compress-2`) **increases** compute energy while cutting memory traffic, and lands at
1.31×, while AQB8 cuts both and lands at 1.82×. That contrast is the paper's real contribution
to the survey.

---

## Method

**The quantized BVH tree (§4).**

1. **Build a standard BVH first**, with any existing builder — the scheme is explicitly
   agnostic to it (§4.3.1) **verified**. Evaluated on a 2-ary tree from `madmann91/bvh` [4] and
   a 6-wide tree from Embree [75].
2. **Partition the tree into clusters.** Each cluster gets one **anchor BB** kept in FP32
   (six 32-bit values, 24 B) which defines a local `[0,255]³` coordinate system; every other
   node in the cluster stores its two child boxes as **six INT8 each** in that frame (§4.2)
   **verified**. The quantized box is *the smallest box in the [0,255] lattice that fully
   encloses the FP32 box* — the bounds are rounded **outwards**, so the quantized box is a
   superset (§4.2) **verified**.
3. **Choose the cluster boundaries by dynamic programming over a modified SAH cost.** The
   Surface Area Heuristic cost `C(N) = (1/S(N))[Σ_Ni T(Ni)S(Ni) + c_i Σ_Nl S(Nl)|Nl|]` with
   `T(Ni) = c_t + c_s` if the node's policy is `SWITCH` and `c_t` if `STAY` (§4.3.2)
   **verified**. Brute force is `O(2ⁿ)`; the optimal-substructure property gives a bottom-up
   DP running in `O(n(log n)²)` (§4.3.3) **verified**. Empirical parameters
   `[c_t, c_i, c_s] = [0.5, 1, 1]` for 2-ary and `[0.5, 1, 0.6]` for 6-wide (§4.3.2/§4.3.4)
   **verified**. Lowering `c_s` makes clusters smaller and more numerous.
4. **Quantize the ray into the cluster's frame (§4.4).** `q_w = w / S_w` with `S_w = 2⁻⁷`
   fixed, held in a **custom FP14 (1 sign, 8 mantissa, 5 exponent)**; `q_b = b / (S_w S_x)`
   held in **INT32**. `S_w S_x` is stored per cluster as one FP32 word. Only `q_b` depends on
   the cluster, so only `q_b` is recomputed on a cluster switch **verified**. FP14 is chosen
   because `w = 1/d` has density `f(w) = 1/(2w²)` for `|w| ≥ 1`, so a float's finer resolution
   near zero matches the distribution (§4.4.2) **verified**.
5. **The quantized ray-box test (§4.5).** Substituting `t = S_w S_x q_t`, `w = S_w q_w`,
   `x = S_x q_x`, `b = S_w S_x q_b` into `t = wx + b` cancels `S_w S_x` on both sides and
   leaves `q_t = i_w · 2^{r_w} · m_w · q_x + q_b`. Executed as: **INT8 multiply** `m_w × q_x`
   → **left shift** by `r_w` → **2's complement** if the sign bit `i_w` is set → **INT32 add**
   of `q_b` (§4.5) **verified**. Fig. 11(d) confirms the QBOX unit is exactly six of these
   feeding an INT32 MIN / INT32 MAX / INT32 CMP, against Fig. 11(c)'s six FP32 MUL + FP32 ADD
   feeding FP32 MIN / MAX / CMP **verified**.
6. **Memory layout (§4.6).** Standard node = 56 B (24 + 24 + 4 + 4). Quantized node = **16 B**
   (6 + 6 + 2 + 2), with each 2-byte child field split into Field A (1 b, internal vs leaf),
   Field B (3 b) and Field C (12 b) encoding one of `SWITCH` / `STAY` / `LEAF` plus a
   cluster-relative offset. Cluster record = **36 B** (24 B anchor + 4 B `S_w S_x` + 4 B node
   base index + 4 B triangle base index) **verified**.
7. **Traversal (Algorithm 1).** `SWITCH` → one FP32 ray-box test against the anchor, which
   also produces the new `qRay`; `STAY` → quantized tests only; `LEAF` → unmodified FP32
   ray-triangle tests. The ray is also re-quantized when popping a stack entry from a
   different cluster **verified**.

**Why the per-cluster scale is isotropic** (a single `S_x` for x, y and z rather than three):
the slab method compares `t` values *across* axes (`t_max > t_min` over all three), so the
three axes must share one scale for the INT32 comparison to be meaningful. The paper does not
say this. **inferred / not verified.**

**The accelerator (§5).** Baseline = TRV units + FP32 BOX units + FP32 TRIG units + an 8 KB L0
cache, modelled on the Vulkan-Sim RT unit [56] because commercial RT-core internals are not
public **verified**. AQB8 = **modified TRV** (cluster-switch logic and the three node
policies), **modified BOX** (also computes the quantized ray, used only on anchors), **new
QBOX** (integer-only), same TRIG. The design change is a **ratio change**, not a
reconfigurable datapath: 51 FP32 BOX → 9 FP32 BOX + 53 QBOX **verified**.

**Evaluation (§6).** Two separate setups, and they are not interchangeable:

| | Energy (Fig. 13, Table 3) | Everything else (Figs. 12, 14, 16) |
|---|---|---|
| Workload | rays pre-collected from pbrt-v4, **1 sample/pixel**, replayed | rays generated at runtime, **256×256** |
| Model | cycle-accurate sim of the synthesized units + CACTI caches + DRAM at a **fixed 6.5 pJ/bit** | **Vulkan-Sim** full-GPU timing model, 30 SMs |
| Memory | **32 KB L1 / 1 MB L2**, *unlimited bandwidth and zero latency* by construction | **64 KB L1 per SM / 3 MB L2**, real timing |
| Synthesis | Catapult HLS + Design Compiler, **TSMC 40 nm**, PrimePower on gate-level sim | — |

All **verified** from §6.2-§6.4 and Table 2.

## Key numbers, with their frame

Three configurations throughout: **Baseline** (all BBs FP32), **Compress** (all BBs INT8 per
Ylitie et al. [77], decompressed to FP32 to test), **AQB8**. Suffix `-2` = 2-ary BVH, `-6` =
6-wide BVH. All three share the same tree topology (§6.1) **verified**.

| Setting | Scene / config | Metric | Baseline | Result | Source & evidence level |
|---|---|---|---|---|---|
| Motivation | 7 scenes | test-count inflation from naive FP16 traversal | FP32 traversal | ray-box up to **2.7×**, ray-triangle up to **19.6×** | §1, Fig. 1; counters in the RT program. **verified** |
| Motivation | 7 scenes | BB share of memory traffic | — | **69%** of L1D bytes, **74%** of DRAM bytes | §2.3, Fig. 5; Vulkan-Sim. **verified** |
| Memory traffic | 7 scenes, Vulkan-Sim 256×256 | L1D cache requests | Baseline | −**65-82%**, **74% mean** | §7.1.1. Cycle-level simulator. **verified** |
| Memory traffic | same | L2 cache requests | Baseline | −**48-68%**, **60% mean** | §7.1.1. **verified** |
| Memory traffic | same | DRAM accesses (bytes) | Baseline | −**61-76%**, **70% mean** — this is the abstract's 70%, and it *is* the mean | §7.1.2. **verified** |
| Memory traffic | same | which config the "AQB8" in §7.1 means | — | **§7.1 says "AQB8" without the -2/-6 suffix while Fig. 12 plots both.** Unresolved | §7.1. **inferred / not verified** |
| BVH footprint | 7 scenes | tree size in bytes | Baseline | AQB8 ≈ **30%** of baseline (Compress ≈ **41%**) | Table 1. **verified** |
| BVH footprint | KIT | node record | 56 B | **16 B** + 36 B per cluster | §4.6, Fig. 10. **verified** |
| BVH footprint | KIT | reconstruction check | — | 0.695 M internal nodes × 16 B + 0.021 M clusters × 36 B = **11.9 MB** = Table 1 exactly | derived from Table 1 + §4.6. **verified arithmetic** |
| Granularity | 7 scenes | clusters ÷ nodes | — | **0.9-3.3%** → **~30-110 nodes per cluster**, i.e. a new anchor every ~5-7 binary levels | Table 1. **verified** (ratio derived) |
| Effective bitwidth | KIT | bits per BB coordinate | 32 (FP32) | **8 + ~0.5 amortised anchor ≈ 8.5** | derived: 24 B anchor ÷ (0.695/0.021 nodes × 12 coords). **inferred** |
| Energy | 7 scenes, replay, 1 spp | total energy (compute + SRAM + cache + DRAM) | Baseline-2 | −**29-49%**, **42% mean**. **The abstract's "49%" is the per-scene maximum** | §7.2 vs abstract. Gate-level power + CACTI + 6.5 pJ/bit DRAM. **verified** |
| Energy | MEAN bar | total energy | **Compress-2** | ≈ **−38%** (0.58 vs 0.93 normalized) | Fig. 13, read off the rendered figure. **inferred / not verified** |
| Energy | MEAN bar | Compress-2's own compute energy | Baseline-2 | **increases** — "actually increase it across all tested scenes" | §7.2. **verified** |
| Energy | replay | compute energy, ops × nJ/op | Baseline-2 5.95 mJ | Compress-2 **6.50 mJ (+9%)**, AQB8-2 **3.67 mJ (−38%)** | derived from Table 3. **inferred / not verified** |
| Energy | replay | share of compute energy in the untouched FP32 TRIG unit | 30% | **55%** in AQB8-2 | derived from Table 3. **inferred / not verified** |
| Area | AQB8-2 vs Baseline-2, TSMC 40 nm | total RT-accelerator area, unit counts extrapolated to matched throughput | Baseline-2 | −**27%** (≈6.82 → ≈5.00; Fig. 15's axis is µm² with a max near 7e6, so ≈**6.8 → 5.0 mm²**) | §7.4, Fig. 15. Post-synthesis. **verified**; the mm² reading **inferred** |
| Area | one unit, 40 nm | QBOX vs FP32 BOX | 82.13 | **16.08** → **5.1× smaller** | Table 3, §7.4. Post-synthesis. **verified** |
| Area | one unit | AQB8's modified BOX (also computes qRay) | 82.13 | **97.05** (+18%) | Table 3. **verified** |
| Area | one unit | AQB8's modified TRV | 7.88 | **9.80** (+24%) | Table 3. **verified** |
| Energy/op | one unit | QBOX vs FP32 BOX | 1.38e-1 nJ | **2.43e-2 nJ** → **5.7× lower** | Table 3. **verified** (ratio derived) |
| Energy/op | one unit | AQB8's TRV is *cheaper per op* than baseline's despite being larger | 6.0e-3 nJ | **5.5e-3 nJ** | Table 3. **verified**; the reason is not given |
| Unit counts | Fig. 15 | matched-throughput sizing | 64 TRV / 51 BOX / 11 TRIG | AQB8-2: **78 TRV / 53 QBOX / 9 BOX / 13 TRIG** | Fig. 15 + §7.4. **verified** |
| Accuracy cost | Vulkan-Sim | ray-box intersection tests | Baseline-2 | **+3-6%** | §7.3, Fig. 14. **verified** |
| Accuracy cost | Vulkan-Sim | ray-triangle intersection tests | Baseline-2 | **+6-31%** (but only ~0.12-0.25× the ray-box count in absolute terms — Fig. 14 normalizes *both* panels to the baseline ray-box count) | §7.3, Fig. 14. **verified** |
| Accuracy cost | replay | TRV operations (cluster switching) | 35.9 M | **43.1 M (+20%)** | Table 3. **verified** |
| Accuracy cost | replay | total ray-box work incl. anchor tests | 28.8 M | 30.0 M QBOX + 4.3 M anchor BOX = **34.3 M (+19%)**; the QBOX part alone is +4.2%, matching §7.3's 3-6% — **so Fig. 14's count appears to exclude the anchor tests** | derived from Table 3. **inferred / not verified** (Table 3 and Fig. 14 are also different workloads) |
| Performance | 7 scenes, Vulkan-Sim | geomean speedup, 2-ary | Baseline-2 | **1.82×** (Compress-2: **1.31×**) | §7.5. Cycle-level simulator. **verified** |
| Performance | same | geomean speedup, 6-wide | Baseline-6 | **1.43×** (Compress-6: **1.19×**) | §7.5. **verified** |
| Performance | same | speedup over the actual prior art | Compress | **1.39×** (2-ary), **1.20×** (6-wide) | 1.82/1.31 and 1.43/1.19. **inferred / not verified** |
| Image quality | — | PSNR / SSIM / any rendered-image comparison | — | **none — the paper reports no image-quality metric at all** | full-text grep: `PSNR` 0, `SSIM` 0, `image quality` 0, `identical` 0, `false negative` 0. **verified (negative claim, grepped)** |
| Correctness | §4.2 | argument, not measurement | — | the quantized box's bounds are moved **outwards** so it fully encloses the FP32 box → false positives only, no missed hits. Stated for the **box**; the **ray** side (FP14 / INT32 rounding) is never discussed | §3, §4.2. **verified that the claim is made and that it covers only the box** |
| Build cost | — | clustering DP | `O(n log n)` standard build | `O(n(log n)²)`, "does not introduce significant overhead" — **no measured build time** | §4.3.3. Analytical only. **verified (that only a complexity claim is given)** |

## Cost and requirements

**What the hardware pays.**

- **A second, larger box unit.** The FP32 BOX unit is retained (9 of them) purely for anchor
  tests, and made **18% larger** because it now also computes `qRay` on a cluster switch. The
  TRV unit grows **24%** for the SWITCH/STAY/LEAF policy logic and the re-quantization check
  on stack pops. **verified** (Table 3).
- **More units, on purpose.** Because AQB8 does more traversal steps, the area comparison adds
  units to restore throughput: **+14 TRV, +2 TRIG** over the baseline. This is disclosed and
  is good practice, but the extra count is set by **linear extrapolation from Baseline-2's
  operation counts**, not measured (§6.3.2) **verified**.
- **A variable shifter in every lane.** The QBOX replaces an FP32 multiply-add with INT8
  multiply → shift-left by a 5-bit exponent → conditional 2's complement → INT32 add. The
  shifter is the price of using a float for `q_w`; it is what buys the 5.1×. **verified**
  (Fig. 11(d), §4.5).
- **Per-cluster metadata.** 36 B per cluster — 24 B FP32 anchor + 4 B `S_w S_x` + two 4 B base
  indices. At 0.9-3.3% cluster density this is 6-8% of the compressed tree. **verified**
  (Table 1, §4.6).
- **INT32 everywhere downstream.** `q_b` is INT32 and so is the accumulated `q_t`; MIN/MAX/CMP
  are INT32. There is no narrower accumulator. **verified** (Fig. 11(d), §4.5).

**What it requires of the software.**

- **The BVH must be rebuilt.** A stock BVH cannot be consumed: the clustering DP must run over
  it and the tree must be re-emitted in the 16 B/36 B layout. This is the ray-tracing analogue
  of "needs a calibration pass, not a retraining loop" — offline, data-independent, and it does
  not touch the geometry.
- **Three tuning constants** `[c_t, c_i, c_s]`, set empirically and *differently* for 2-ary and
  6-wide (`[0.5,1,1]` vs `[0.5,1,0.6]`). No sensitivity study is reported for them.
  **verified** (§4.3.2, §4.3.4) — and the absence of the sensitivity study is **verified** by
  reading §7 in full.
- **No change to the graphics API.** Vulkan RT calls are used unmodified; there is no ISA
  extension, no compiler, no runtime. **verified** (§2.2 describes the existing API path and
  §5 changes only the hardware) — this is why the Level tag is `ALGO+ARCH` and **not** `+SYS`.

## Limitations and open questions

1. **No image-quality evidence.** The conservative-enclosure argument makes the *box* side
   sound: a superset box can only add tests, never remove a hit. But the **ray** is also
   quantized, and `q_w` (FP14) and `q_b` (INT32) rounding perturb the ray itself. A perturbed
   ray can miss a box it should hit. The paper never states a rounding mode for the ray, never
   argues the perturbation is conservative, and never renders a comparison image. **This is the
   one gap that would have to be closed before citing AQB8 as loss-free.**
2. **The bottleneck moves into the untouched unit.** Ray-triangle intersection stays FP32 and
   goes from ~30% to ~55% of compute energy. The paper's technique does not extend to triangle
   vertices as written (they have no cluster frame), so the next 2× is not available by doing
   more of the same.
3. **The 6-wide result is the honest one and it is much smaller.** Commercial RT hardware uses
   wide BVHs; the paper's own 6-wide configuration gives 1.43× over uncompressed and 1.20× over
   compressed. The abstract quotes 1.82×, the 2-ary number.
4. **The `Compress` baseline is the authors' own adaptation.** Ylitie et al. [77] is a
   *compressed wide* BVH scheme; a 2-ary `Compress-2` is not what that paper proposes.
   Its per-node local frames are also finer-grained than AQB8's per-cluster frames, which is
   presumably why `Compress-2` has *fewer* extra ray-triangle tests than AQB8-2 in Fig. 14 —
   AQB8 trades some box tightness for a coarser, cheaper reference frame. The paper does not
   discuss this trade. **inferred / not verified.**
5. **Two evaluation setups with different cache hierarchies**, and the abstract's four headline
   numbers come from three of them. See the fairness verdict.
6. **The clustering DP's constants are unswept**, and `c_s` directly controls the anchor
   density — i.e. the effective bitwidth. A sensitivity curve over `c_s` is the obvious missing
   experiment and would have been the paper's granularity ablation.
7. **Build time is asserted, not measured** — `O(n(log n)²)` against a standard `O(n log n)`.
   For animated scenes, which rebuild per frame, that exponent matters and is not evaluated;
   all seven scenes are static.
8. **No sensitivity to bitwidth.** The paper fixes INT8 and never asks what INT6 or INT10 would
   cost, even though the `[0,255]` lattice is the one free parameter in the whole format.

## Relation to other entries

- **Combined / residual data type** — [`AQuant`](../AQuant/ANALYSIS.md),
  [`SmartExchange`](../SmartExchange/ANALYSIS.md), [`SingularBit`](../SingularBit/ANALYSIS.md),
  [`OLAccel`](../OLAccel/ANALYSIS.md). AQB8 differs from all of them in **what the
  high-precision part is**: in OLAccel/OliVe/Oaken/MicroScopiQ the FP32/wide part is a *large
  value*; in AQuant it is a *reference value*; in SingularBit it is a *high-energy component*.
  In AQB8 it is a **coordinate frame** — the anchor is not a value the offsets are added to so
  much as the origin and unit of the space the offsets live in. That is a genuinely different
  kind of residual and worth a sentence in the survey: **the reference can be a frame, not a
  value.**
- **Granularity axis** (per-layer → per-region → per-channel → per-group → per-head → per-token
  → per-rank). AQB8 adds **per-cluster**, but the interesting part is not the level, it is
  **who chooses the boundary**. Fixed size: [`Oaken`](../Oaken/ANALYSIS.md),
  [`MicroScopiQ`](../MicroScopiQ/ANALYSIS.md). Data-derived at runtime:
  [`DRQ`](../DRQ/ANALYSIS.md), [`LightNobel`](../LightNobel/ANALYSIS.md). Data-derived offline:
  [`Tender`](../Tender/ANALYSIS.md)'s geometric channel bands,
  [`OLAccel`](../OLAccel/ANALYSIS.md)'s calibrated threshold. **AQB8 is the only entry where the
  group boundaries are the output of a cost-model optimisation** — a dynamic program over a
  modified SAH that explicitly prices a scale change (`c_s`) against the error it avoids. That
  is a fourth answer on this axis and I would propose it as a sub-axis:
  *fixed / runtime-predicted / calibrated / **cost-model-optimised***.
- **Compression vs cheaper arithmetic** — the proposed missing axis, with
  [`Ecco`](../Ecco/ANALYSIS.md) at the compression end (decompresses to FP16 between L1 and L2,
  so it buys bandwidth, not arithmetic). **AQB8 is the axis's other endpoint and, better, it
  measures the axis.** Its `Compress` baseline *is* Ecco's position instantiated in ray
  tracing: memory traffic down, compute energy **up**, 1.31× overall. AQB8 keeps the traffic
  win and adds the arithmetic win, reaching 1.82×. If the survey wants one experiment to
  justify separating the two ends of that axis, this is it.
- **Multi-precision datapath** (BitFusion spatial → RaPiD split pipelines → SamsungNPU/EVA
  temporal → XtraMAC DSP bit-space → UniCore adder slices; the organising claim being that the
  deciding variable is what the substrate charges for). AQB8 gives a **fifth answer that is not
  a multi-precision unit at all**: two *fixed* datapaths, FP32 BOX and INT8 QBOX, with the
  design freedom in their **ratio** (51:0 → 9:53). It can do this because the precision is
  determined by the *node type*, which is known statically from the tree, not by a
  layer-configuration decision at runtime. Where [`BitFusion`](../BitFusion/ANALYSIS.md) pays
  3.5× area over a temporal design to be reconfigurable, AQB8 pays nothing for flexibility
  because it needs none. **The substrate here charges for FP32 multiply-add in a 6-lane
  slab-test unit, and the answer to that charge is "build the cheap unit and use it 92% of the
  time".**
- **Outlier currency** (extra bits / a destroyed neighbour / a second datapath / compressibility
  / a runtime top-k / crossbar sign balance). AQB8 pays in a currency not yet on the list: **a
  redundant test at the frame boundary.** Every cluster switch costs one full FP32 ray-box test
  against the anchor (4.3 M of them, ~13% of the box-test budget) plus a ray re-quantization —
  work the baseline never does. The bits are almost free (~0.5/coordinate); the frame changes
  are not.
- **Static vs dynamic identification** — firmly **design/build-time**, like OLAccel's calibrated
  threshold and unlike DRQ's runtime mask. Consistent with the corpus's pattern that
  successors revert to design-time.
- **Retraining axis** — not applicable in the NN sense, and the honest translation is
  **"requires a preprocessing pass over the artefact, not a retraining loop"**: the BVH must be
  rebuilt by AQB8's clustering pass, but no geometry, no shader and no scene data changes. In
  deployment terms that is closer to PTQ-with-calibration than to QAT.
- **Correctness model** — worth flagging as a cross-domain observation: ray tracing has a
  *structural* correctness argument (conservative enclosure ⇒ superset of candidate hits) that
  has no analogue in NN quantization, where every error is a distributional argument. AQB8 uses
  it for the box and then does not extend it to the ray, which is where a graphics reviewer
  would press.

---

## For the note

### §1 one-line summary

> Groups every ~30-110 BVH nodes into a cluster with one **FP32 anchor box as a local
> coordinate frame** and stores the rest as **six INT8 offsets** under a single isotropic
> per-cluster scale `S_x = max(l_x,l_y,l_z)/255` — then inverts what every prior BVH
> compression scheme does by **quantizing the ray into the box's frame instead of
> decompressing the box into the ray's** (inverse direction as a custom **FP14** 1s/8m/5e,
> origin term as INT32, ray scale fixed at `2⁻⁷` so the rescale is a shift), turning the
> ray-box test into INT8 multiply → variable left shift → 2's complement → INT32 add, which
> buys a **5.1× smaller box unit**, **−27% RT-accelerator area**, **−70% DRAM traffic** and
> **1.82× geomean** on a 2-ary Vulkan-Sim GPU model — at the cost of +3-6% ray-box and
> +6-31% ray-triangle tests, with **no image-quality metric reported anywhere in the paper**.

### Proposed values on their four axes

| Axis | Proposed | Evidence (one line) |
|---|---|---|
| **Level** | **`ALGO+ARCH`** — *seed says `ARCH`; I dispute it* | §8 in the paper's own words: *"our work differentiates itself by **co-designing** a BVH structure and a corresponding RT accelerator"*; §4.3 contributes a modified-SAH cost function and an `O(n(log n)²)` dynamic program that no hardware executes. Checked for `SYS` explicitly: no ISA, no compiler, no runtime, Vulkan unmodified — `SYS` does **not** apply. |
| **Q-oriented** | `Q-ORIENTED` — seed agrees | Swap the format for plain per-scene INT8 and you get Fig. 1's disaster; the clustering DP, the SWITCH/STAY policy, the FP14 ray format, the QBOX unit and the 16 B node layout all lose their referent. |
| **Data type** | **`INT8` `FP14` `INT32` `FP32` `MIXED`** — *seed has `INT8` `FP32` `MIXED`; I would add two* | `INT8`: six per box, §4.2 **verified**. `FP32`: six per anchor, §4.2 **verified**. `FP14`: *"a custom 14-bit floating-point (FP14) format with 1 sign bit, 8 mantissa bits, and 5 exponent bits"*, §4.4.1 **verified** — a **new token**, drop it if the human would rather keep the vocabulary closed. `INT32`: `q_b` and the accumulated `q_t`, §4.4.1/§4.5 **verified** — this is the one to drop first if the cell is too long. **Explicitly not `POW2`**: `S_w = 2⁻⁷` is a fixed *scale factor*, not a value encoding — the same distinction the reader already drew on [`Tender`](../Tender/ANALYSIS.md). **Explicitly not `BFP`**: each `w` component carries its own 5-bit exponent; nothing is shared across a block. |
| **Generation** | `G2` — seed agrees, and confidently | The G2 test is *"does the paper design a numeric type, or build an architecture whose purpose is to execute quantized arithmetic?"* — AQB8 does both. None of the three G3 threads is present: no outliers, no weight-only bandwidth argument, no codebook, and no LLM. A 2025 paper that is squarely G2 by paradigm. |
| **Optimization** (free text) | `ray tracing` `BVH` `anchor + INT8 offset` `per-cluster scale` `quantize the ray, not the box` `hierarchical local frames` `SAH-derived clustering DP` `custom FP14` `power-of-two ray scale` `conservative outward rounding` `INT8 ray-box test` | The seed's six keywords all hold; `quantize the ray, not the box` is the paper's actual thesis and is missing from the seed. |

**On "multi-level" — the levels, enumerated.** The title's "multi-level" does **not** mean
multiple bitwidths. §3: *"Anchor BBs are used throughout the BVH tree across multiple levels
(Figure 7). Larger anchors represent coarse scene structures, while progressively smaller
anchors handle finer-scale features."* The levels are **BVH tree depths at which a new anchor
frame is opened** — Fig. 7 illustrates three (coarse cluster, finer cluster, very fine
cluster), but the number is not fixed: it is whatever the clustering DP chooses, empirically a
new frame every ~5-7 binary levels (0.9-3.3% of nodes are anchors, Table 1). So: **a
scene-dependent hierarchy of nested local coordinate frames, each with its own scale, chosen by
a cost model — not a fixed number of precision levels.** **verified.**

### Proposed venue-list row

```
| [ ] | [AQB8: Energy-Efficient Ray Tracing Accelerator through Multi-Level Quantization](https://doi.org/10.1145/3695053.3731104) | *close read* | ALGO+ARCH | Q | `INT8` `FP14` `INT32` `FP32` `MIXED` | G2 | `ray tracing` `BVH` `anchor + INT8 offset` `per-cluster scale` `quantize the ray, not the box` `SAH-derived clustering DP` `custom FP14` `power-of-two ray scale` | Clusters of ~30-110 BVH nodes share one FP32 **anchor box as a local frame**; the rest are six INT8 offsets. **Inverts prior BB compression: the ray is quantized into the box's frame, not the box decompressed into the ray's** — so the slab test is INT8 mul + shift + INT32 add. 5.1× smaller box unit. **No image-quality metric is reported anywhere** |
```

*(Changes from the seed at line 46: `ARCH` → `ALGO+ARCH`; data type gains `FP14` and `INT32`;
`G2` and `Q` unchanged; the Note column is rewritten around the ray-vs-box inversion, which the
seed's note does not name.)*

### §4 fairness verdict

**Fair in the places that are usually gamed, and loose in one place that is not usually
checked.**

- **Iso-node ✓** — all three designs synthesized at TSMC 40 nm with the same flow (Catapult HLS
  + Design Compiler + PrimePower).
- **Iso-topology ✓, and stated as a design goal** — §6.1: *"All configurations share the same
  tree topology for their respective branching factors to isolate the impact of multi-level
  quantization without introducing additional factors that could obscure or inflate its
  benefits."* Both 2-ary and 6-wide are reported, which is more than most.
- **Iso-throughput ✓, but modelled** — §6.3.2 adds TRV/BOX/TRIG units to Compress and AQB8 to
  pay for their extra traversal steps *before* comparing area. The count is set by **linear
  extrapolation from Baseline-2's operation counts**, not by measurement. Credit for doing it;
  note that it is a model.
- **Iso-accuracy — undefined, and that is the real gap.** There is no accuracy metric to be iso
  on. The conservative-enclosure argument covers the box; the ray's own quantization is never
  analysed and no image is ever compared.
- **Not iso-experiment.** The abstract's four numbers come from **three different setups**:
  70% DRAM and 1.82× from Vulkan-Sim (64 KB L1 / 3 MB L2, 256×256, runtime rays); 49% energy
  from a replay model (32 KB L1 / 1 MB L2, 1 spp, *unlimited bandwidth and zero latency* by
  construction); 27% area from post-synthesis. They must not be quoted as one result.
- **Baseline era/reality ✗ in framing.** "over modern GPU RT accelerators" is a **model** of an
  RT unit (Vulkan-Sim [56]) at 40 nm, chosen because commercial RT-core internals are not
  public — the paper says so. Nothing here is silicon.
- **Numbers not to quote bare.** (i) **"49% energy"** — that is the per-scene **maximum**; the
  mean is **42%**. (ii) **"1.82×"** — 2-ary, against an *uncompressed* FP32 baseline; the
  6-wide figure is **1.43×**, and against the paper's own INT8-compressed baseline the gains
  are **1.39×** and **1.20×**. (iii) **"82.13 mm²"** for the BOX unit — Table 3's area column is
  labelled `mm²` but Fig. 15's axis is µm² and the totals only reconcile at **×10³ µm²**; the
  whole baseline RT accelerator is ≈6.8 mm², not 6815 mm². **Quote instead:** the QBOX/BOX
  ratio (5.1× area, 5.7× energy per op) and the fact that `Compress-2` **increases** compute
  energy — both are internal comparisons the authors built themselves.

## Note from the source list

> _(no keywords recorded in the source CSV)_
>
> **Comment:** CSV link is a GitHub repo, not a paper

## Abstract (verbatim, from the archived PDF)

> Ray tracing (RT) is a rendering technique that produces high-fidelity images by simulating
> how light physically interacts with objects in a scene. This realism comes at a high
> computational and memory cost, largely driven by the need to find numerous ray-object
> intersections. To accelerate this process, scenes are typically structured using bounding
> volume hierarchy (BVH) trees, where objects are grouped within bounding boxes to minimize
> the number of required intersection tests. Specialized hardware, known as RT accelerators,
> accelerates BVH processing to boost computational speed, yet memory traffic persists as a
> major bottleneck, largely due to the bandwidth consumed by standard 32-bit floating-point
> (FP32) bounding boxes. Consequently, previous work has aimed to reduce memory traffic by
> compressing these boxes into low-bit (e.g., 8-bit) representations. However, existing
> compression techniques typically require decompressing bounding boxes back to FP32 for
> intersection tests, thus failing to eliminate the computational burden and energy cost
> associated with complex FP32 arithmetic during BVH traversal. This work introduces AQB8, an
> RT accelerator designed to operate on a quantized BVH tree constructed using a novel
> multi-level quantization technique. This approach enables RT to operate directly on low-bit
> integers using simpler, area-efficient hardware units, thereby drastically reducing the need
> for FP32 arithmetic during BVH traversal while mitigating overheads associated with reduced
> precision. As a result, across various scenes, AQB8 achieves a 70% reduction in DRAM
> accesses, a 49% reduction in energy consumption, a 27% hardware area reduction, and a 1.82x
> performance speedup over modern GPU RT accelerators. Our code is publicly available at
> https://github.com/nycu-caslab/AQB8.

## Appendix — tables recovered from the PDF's raster images

Both tables are images in the text extraction; transcribed by rendering pages 10 and 11.

**Table 1 (p. 383) — statistics of evaluated scenes.**

| | KIT | BA | BMW | CLA | HOU | STR | TEA |
|---|---|---|---|---|---|---|---|
| # of rays | 0.92M | 1.05M | 1.40M | 0.92M | 0.92M | 0.92M | 0.92M |
| # of triangles | 1.44M | 0.59M | 0.79M | 0.10M | 1.82M | 0.26M | 0.13M |
| # of nodes | 1.39M | 0.55M | 0.78M | 0.09M | 1.79M | 0.23M | 0.11M |
| # of clusters | 0.021M | 0.005M | 0.012M | 0.003M | 0.032M | 0.003M | 0.001M |
| Baseline-2 BVH size | 39.0MB | 15.4MB | 22.0MB | 2.6MB | 50.1MB | 6.4MB | 3.1MB |
| Compress-2 BVH size | 16.0MB | 6.3MB | 9.0MB | 1.1MB | 20.6MB | 2.6MB | 1.3MB |
| AQB-2 BVH size | 11.9MB | 4.6MB | 6.7MB | 0.8MB | 15.5MB | 1.9MB | 0.9MB |

*(BVH sizes include BBs, child indices and other metadata. "# of nodes" counts internal **and**
leaf nodes; only internal nodes carry a record, which is why 0.695 M × 56 B = 39.0 MB for KIT.)*

**Table 3 (p. 384) — per-unit area, energy per operation, and average operation counts.**
Area column is labelled `mm²` in the paper; Fig. 15's axis is µm² and the totals only
reconcile at **×10³ µm²**.

| | | TRV | QBOX | BOX | TRIG |
|---|---|---|---|---|---|
| Hardware area | Baseline-2 | 7.88 | — | 82.13 | 192.92 |
| | Compress-2 | 8.12 | — | 90.58 | 192.92 |
| | AQB8-2 | 9.80 | 16.08 | 97.05 | 192.92 |
| Energy per operation (nJ) | Baseline-2 | 6.0e-3 | — | 1.38e-1 | 2.90e-1 |
| | Compress-2 | 8.4e-3 | — | 1.51e-1 | 2.90e-1 |
| | AQB8-2 | 5.5e-3 | 2.43e-2 | 1.56e-1 | 2.90e-1 |
| Average operation counts | Baseline-2 | 35.9M | — | 28.8M | 6.07M |
| | Compress-2 | 36.3M | — | 29.2M | 6.17M |
| | AQB8-2 | 43.1M | 30.0M | 4.3M | 7.0M |

**Figure 15 (p. 385) — unit counts and total area (µm²).**
Baseline-2: 64 TRV, 51 BOX, 11 TRIG (≈6.8e6 µm²). Compress-2: 65, 52, 11 (**+8%**).
AQB8-2: 78 TRV, 53 QBOX, 9 BOX, 13 TRIG (**−27%**). The `OTHER` segment is a thin sliver in
all three.
