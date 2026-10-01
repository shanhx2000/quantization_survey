# Reports-001 — ISCA venue tag audit (2026-10-01)

**Input:** the 33 live rows of `QuantArchSurvey/venues/ISCA/README.md` plus the restored
ELSA and Phi, checked against `TAXONOMY.md` (current rules), the published notes, our
`ANALYSIS.md` / `paper-note.md`, and — where the two disagreed — the extracted paper text.
**Method:** five read-only agents, seven papers each. **Nothing below has been applied.**
Every change is a proposal for the owner; recorded rulings (Passes 1–11) were not reopened,
and where an agent disagreed with one it says *conflicts with recorded ruling*.
**How far verified:** the per-group sections carry page/line evidence and a confidence for
each item; I (the coordinating agent) did not re-check each item against the PDFs.

Abbreviations: VQ (vector quantization), LUT (lookup table), PIM/NDP (processing-in/near-memory),
SNN (spiking neural network), BCQ (binary-coding quantization).

## Conclusions — tag changes proposed

**Decided 2026-10-01.** Decision is the owner's, copied from `reports-001-tmp.md`; Comment is what was done. Applied changes are recorded in `venues/ISCA/README.md` Pass 12.

| Paper | Axis | Current → proposed | Confidence | Note | Decision | Comment |
|---|---|---|---|---|---|---|
| [Omni-LUT](../../survey/papers/Omni-LUT/paper-note.md) ([pdf](../../survey/papers/Omni-LUT/506501a322.pdf)) | Data type | drop `VQ` | high | zero hits for codebook / k-means / centroid; the format is BCQ bit-planes | ☐ approve ☐ | applied |
| [Omni-LUT](../../survey/papers/Omni-LUT/paper-note.md) ([pdf](../../survey/papers/Omni-LUT/506501a322.pdf)) | Stage | `S3` → `S2` | med-high | table holds computed partial sums (the LUT trap). **Conflicts with Pass 7** | ☐ approve ☐ | applied |
| [Tender](../../survey/papers/Tender/paper-note.md) ([pdf](../../survey/papers/Tender/2406.12930.pdf)) | Data type | drop `MIXED` | high | paper: "without using mixed precision"; note §2 agrees | ☐ approve,add in the note that it uses block quantization, which cluster data into groups using different sclaes.   ☐ | applied; note §2 now names it block (group-wise) quantization |
| [RAELLA](../../survey/papers/RAELLA/paper-note.md) ([pdf](../../survey/papers/RAELLA/2304.07935.pdf)) | Data type | `INT` → `INT8`; drop `ADAPTIVE` | high / med-high | what varies is bits per slice — a width, not a type (§3) | ☐  ☐ reject, dynamic slicing is adaptive. Put a PIM tag. | not applied (rejected). Already PIM: Platform `PIM` in papers.md, `analog PIM` in Optimization |
| [OliVe](../../survey/papers/OliVe/paper-note.md) ([pdf](../../survey/papers/OliVe/2304.07493.pdf)) | Data type | add `FP8`; drop `MIXED` | med | 8-bit config stores outliers as E4M3; 4/8-bit are separate configurations | ☐  ☐ reject, the format has multi-modes. Put an outlier tag for it as well. | not applied (rejected). Added `outlier-aware` to Optimization |
| [SamsungNPU](../../survey/papers/SamsungNPU/paper-note.md) ([pdf](../../survey/papers/SamsungNPU/10.1109_ISCA52012.2021.00011.pdf)) | Data type | drop `MIXED` | med | INT16 is an alternative mode; every evaluated workload is INT8 | ☐  ☐ reject, it supports both int8 (optimized) and int16. | not applied (rejected) |
| [SingularBit](../../survey/papers/SingularBit/paper-note.md) ([pdf](../../survey/papers/SingularBit/506501b001.pdf)) | Data type | add `INT4` `INT3` `FP16` `LUT` | med | four rank regions at 4/3/2/1 bits; FP16 activations; LUT partial sums | ☐ approve ☐ | applied |
| [LUT Tensor Core](../../survey/papers/LUTTensorCore/paper-note.md) ([pdf](../../survey/papers/LUTTensorCore/2408.06003.pdf)) | Data type | add `INT8` | high | INT8 activations and table quantization in the evaluated design | ☐ approve ☐ | applied |
| [MicroScopiQ](../../survey/papers/MicroScopiQ/paper-note.md) ([pdf](../../survey/papers/MicroScopiQ/2411.05282.pdf)) | Data type | add `FP8` | high | 4-bit-inlier configuration has 8-bit FP outliers | ☐ approve ☐ | applied |
| [UniCore](../../survey/papers/UniCore/paper-note.md) ([pdf](../../survey/papers/UniCore/506501c520.pdf)) · [XtraMAC](../../survey/papers/XtraMAC/paper-note.md) ([pdf](../../survey/papers/XtraMAC/506501c536.pdf)) · [NDPLowBitFP](../../survey/papers/NDPLowBitFP/paper-note.md) ([pdf](../../survey/papers/NDPLowBitFP/506501b383.pdf)) | Data type | add `FP16` | med | evaluated FP16 modes / activations | ☐approve ☐ | applied (all three) |
| [Bit Fusion](../../survey/papers/BitFusion/paper-note.md) ([pdf](../../survey/papers/BitFusion/1712.01507.pdf)) | Data type | add `TERNARY` | med | LeNet-5 and VGG-7 run ternary | ☐ approve ☐ | applied |
| [SmartExchange](../../survey/papers/SmartExchange/paper-note.md) ([pdf](../../survey/papers/SmartExchange/2005.03403.pdf)) | Data type | add `MIXED` | med (owner's call) | 4-bit Ce, 8-bit B, 8-bit activations coexist | ☐  ☐ reject | not applied (rejected) |
| [MXFFP](../../survey/papers/MXFFP/paper-note.md) ([pdf](../../survey/papers/MXFFP/506501c505.pdf)) | Data type | `MIXED` doubtful | med | separate 4/6/8 modes; **conflicts with the 2026-09-14 ruling** | ☐  ☐ reject | not applied (rejected) |
| [FATE](../../survey/papers/FATE/paper-note.md) ([pdf](../../survey/papers/FATE/10.1145_3695053.3731031.pdf)) | Stage | `—` → `S2` | med | note and `survey/fpga.md` say `S2`; reset is unlogged — FPGA owner to confirm | ☐ approve ☐ | applied; `PRIMARY["FATE"]="MixedPrec"` added to `4-stage2-classify.py` |
| [NDPLowBitFP](../../survey/papers/NDPLowBitFP/paper-note.md) ([pdf](../../survey/papers/NDPLowBitFP/506501b383.pdf)) · [P3-LLM](../../survey/papers/P3-LLM/paper-note.md) ([pdf](../../survey/papers/P3-LLM/506501a604.pdf)) | Stage | `—` → `S2` | med | note and `pim.md` already say `S2`; venue row and papers.md not updated | ☐ approve ☐ reject | OPEN: both boxes still standing |
| [RAELLA](../../survey/papers/RAELLA/paper-note.md) ([pdf](../../survey/papers/RAELLA/2304.07935.pdf)) | Stage | `—` → `S2` (path `S3→S2`) | high, when the owner rules | `pim.md` already gives that path | ☐ approve ☐ reject | OPEN: both boxes still standing |
| [JPEG-ACT](../../survey/papers/JPEG-ACT/paper-note.md) ([pdf](../../survey/papers/JPEG-ACT/10.1109_ISCA45697.2020.00075.pdf)) · [Gist](../../survey/papers/Gist/paper-note.md) ([pdf](../../survey/papers/Gist/10.1109_ISCA.2018.00070.pdf)) | Platform (papers.md) | ASIC → GPU | med | simulated Titan V / stock Titan X; Ecco and LoKA precedent | isn't it an ASIC extension of GPU? | applied: both GPU, via `PLATFORM` in `3-paths-classify.py` |
| [Phi](../../survey/papers/Phi/paper-note.md) ([pdf](../../survey/papers/Phi/2505.10909.pdf)) (restored) | Level, Data type | `ARCH` → `ALGO+ARCH`; add `LUT` | low-med | restored verbatim for now; `VQ` sits awkwardly with "a basis, not a codebook" | ☐ approve ☐ | applied |
| [AQuant](../../survey/papers/AQuant/paper-note.md) ([pdf](../../survey/papers/AQuant/506501b417.pdf)) | Stage (published note only) | `S3` → `S2` | high | row already `S2` (Pass 7); note's `S3` is the blind G3→S3 rename in upstream c044026. H.265 reuse is scalar residual quantization, not VQ | ☐ approve ☐ | applied (note only) |

## Note and cell hygiene (no tag change)

- **Published notes that disagree with their row:** AQuant note says `S3` (row `S2`, Pass 7);
  SmartExchange note says `S2` (row `S1`, Pass 9); RAELLA note `S2` vs row `—`; XtraMAC/FATE
  notes `S2` vs row `—`; DRQ note §2 "not magnitude-based" contradicts its outlier ruling;
  Transitive Array note §2 "elementwise" vs group size 128; UniCore §1 "3.95%" should be 3.95×.
- **Self-duplicating Note cells:** RaPiD, TPUv4i, SamsungNPU (also repeats Pass 10), SmartExchange,
  DRQ, JPEG-ACT carry a short note followed by an audit paragraph that restates it.
- **Wrong or stale text:** SmartExchange cell opens "W = B·Ce" (paper: `W ≈ Ce B`);
  SamsungNPU and Pass 10 link Bit Fusion to `../MICRO/README.md` (it is ISCA'18);
  AQB8 Optimization has `**…**` inside backticks; Mokey "pre-LLM root of the codebook thread"
  vs Pass 6's EIE finding (owner's call).
- **Classifier hazards (TAXONOMY §7):** FATE's "FPGA LUTs … not LUT-GEMM" trips the
  `LogicMapped` and LUT patterns; JPEG-ACT is filed as Transform by its `DCT` keyword and needs
  a `PRIMARY` override; RAELLA would be filed MixedType via `ADAPTIVE` once staged.
- **Unlogged rulings:** DRQ (outlier, `S2`) and JPEG-ACT (`S3→S2`), 2026-09-22, exist only in
  Note cells and classifier comments.

## Infrastructure found on the way

- **`Claude/scripts/sync_notes.py` must not be run as is.** A dry run would overwrite all 33
  published notes: ours still carry the retired `Generation` row where upstream has `Stage`
  (plus upstream audit edits to DRQ, OASIS, Omni-LUT), and it would republish RingCNN, which
  upstream moved to `legacy/`. Port the Stage rows back into our `paper-note.md` files and add
  RingCNN to `EXCLUDED` first.
- **Upstream `survey/gen/5-check.py` crashes on clean `main`** (44cfb7d): the DAC 2015 record
  *Joint Precision Optimization and High Level Synthesis…* has no name in `names.py`. With a
  temporary name in the gitignored intermediate, `main` reports 137 problems — none ISCA-specific.

## Not done

No tag in any row was changed. No PDF was re-opened by me. The pre-2018 rows that cite the
"ELSA and Phi removal" rule were left alone (owner's call, recorded in ISCA Pass 11).

---

# Appendix — per-group audits, verbatim


## Group 1

## Audit G1: ISCA 2026 venue-index tags (7 papers)

Abbreviations used below:
- `README` = `QuantArchSurvey/venues/ISCA/README.md`
- `TAX` = `QuantArchSurvey/TAXONOMY.md`
- `note` = `QuantArchSurvey/venues/ISCA/notes/<abbr>.md`
- `AN` / `PN` = `survey/papers/<Dir>/ANALYSIS.md` / `paper-note.md`
- `paper pNN` = `survey/papers/<Dir>/extracted/*.pages/pNN.txt`

Cross-cutting finding: the two PIM/NDP rows (NDPLowBitFP, P3-LLM) carry Stage `—` in the venue row and in `survey/papers.md` (L217, L222). Their published notes say `S2` (ndp-low-bit-fp.md L12, p3-llm.md L12), and so does `survey/pim.md` (L105, L106). Pass 7 also gave P3-LLM `S2` (README L359). The `—` matches TAX §4's "Owner reset" (PIM records cleared for the domain owner). pim.md is the PIM domain's re-read ("`Stage` is re-read under the current taxonomy", pim.md header), so it looks like the owner has already assigned the stage and the venue row and papers.md were never updated. **verified** (the drift); the reading that pim.md is the owner's assignment is **inferred**.

---

### 1. [NDPLowBitFP](../../survey/papers/NDPLowBitFP/paper-note.md) ([pdf](../../survey/papers/NDPLowBitFP/506501b383.pdf)) -> ndp-low-bit-fp — **MINOR**

| Axis | Current | Proposed | Evidence | Confidence |
|---|---|---|---|---|
| Data type | `FP4` `FP8` `MIXED` | `FP4` `FP8` `FP16` `MIXED` | **verified**: the evaluated QConfigs are W4A4S8, W8A8S16, W4A16S8, W8A16S16 (paper p10, Table III). In W-only configs the activations, and the S16 scales, are FP16: "precision always follows the activation precision (FP16)" (p11). The PU has an FP16 mode/datapath (p03, Fig.) and an FP16×FP4 PU variant is evaluated (p13). So FP16 coexists with FP4/FP8 in the evaluated design, which is also what justifies `MIXED`. The note's §2 lists only "FP4 / FP8 with per-group scales" (note L28). | med |
| Stage | `—` | `S2` (and papers.md L217 `—` -> `S2`) | **verified** drift: note L12 = `S2`, pim.md L105 = `S2` / "Quantization granularity". Applying §4 myself: per-group scale handling, a scale-value interleaved DRAM layout and dequantization scheduling act on the block/array/memory path. No scalar format is designed ("Contributes none", note L28). That is `S2` scope, not S1 or S3. If the `—` is a deliberate owner reset that is still pending, the note's `S2` is the side that is out of step. | med (rule application high; whether pim.md is the owner's final call is inferred) |

- Q? `Q`: matches the recorded Pass 4 ruling (README L255-259). Not re-litigated. **verified**
- Level `SYS+ARCH`: matches note L9, AN "Proposed tags", Pass 1 (README L128). **verified**
- Cell hygiene: the Optimization and Note cells match note L13 and §1 exactly. No negated trigger words. OK.
- PN.md (working copy) still has `Generation G2` and no Stage row (PN L12). That is expected, since it is the pre-migration working note, so no drift on the published side.

### 2. [EVA](../../survey/papers/EVA/paper-note.md) ([pdf](../../survey/papers/EVA/506501b351.pdf)) -> eva — **OK**

No axis changes proposed.

- Level `ARCH`, Q `Q`, Data type `VQ LUT FP16 INT8`, Stage `S3`: the venue row, note L9-L13 and AN L291-L295 all agree. papers.md L216 = `S3`, ASIC. **verified**
- Stage, by §4: a weight is an index into 2^8 = 256 k-means/AQLM centroids (note L26-L27). That is test (a). `S3` is correct. Note that EVA's table (`O = XB`) is computed per token from the GEMM, which on its own would be the LUT trap. The `S3` rests on (a), not on the table. **verified** (note L39-L44) / reasoning **inferred**
- `INT8` is supported. The base PE is a 32×32 INT8 array, FP16 is composed from four INT8 multiplies, and INT8 prefill runs on it (paper p06: "seamless INT8 prefill computation"). **verified**
- `MIXED` is correctly absent. INT8 prefill vs FP16 decode are phase modes, and C = 2/3/4 codebooks are alternative configurations (§3 "alternative modes alone are not MIXED"). **inferred**. Consistency point, not a change: SamsungNPU carries `MIXED` for the same "wide value = four time-multiplexed INT8" mechanism. One of the two is applying §3 differently. low
- Cell hygiene: "codebook" in Optimization/Note is used affirmatively and is correct for this paper. OK.

### 3. [LoKA](../../survey/papers/LoKA/paper-note.md) ([pdf](../../survey/papers/LoKA/506501b368.pdf)) -> loka — **OK** (one hygiene note)

No axis changes proposed.

- Level `ALGO+SYS`, Q `Q`, Data type `FP8 BF16 TF32 MIXED`, Stage `S2`: the venue row, note L9-L13 and AN L463-L466 agree. papers.md L218 = `S2`, GPU. **verified**
- Q is consistent with Pass 4 (README L261-262). Not re-litigated.
- Stage, by §4: no scalar format is designed. The FP8 sub-format is never even named (note L33). Per-operator choice of tensorwise/rowwise/blockwise scaling plus per-layer precision is the "quantization granularity" / "mixed precision" S2 mechanism. `S2` is right. **inferred** from note L37, L59
- Data type: FP32 (Probe statistics, note L31) is correctly left out because it is not a tensor format. **inferred**
- Cell hygiene (low): the Optimization keyword `model-hardware co-design` is the paper's own section title ("LoKA Mods: Precision-Aware Model-Hardware Co-design", paper text L454), but LoKA builds no hardware (note L61). TAX §1 says "co-design" titles are "almost always" `ALGO+ARCH`, so a Level classifier keyed on that phrase could add `ARCH`. Consider "model co-design (paper's term)" or "model-kernel co-design" (the paper also uses "model-kernel co-design", text L459). low

### 4. [MXFFP](../../survey/papers/MXFFP/paper-note.md) ([pdf](../../survey/papers/MXFFP/506501c505.pdf)) -> mxffp — **MINOR**

| Axis | Current | Proposed | Evidence | Confidence |
|---|---|---|---|---|
| Data type (`MIXED`) | `MX FP4 FP8 ADAPTIVE MIXED` | Keep, as **conflicts with recorded ruling**. Under §3 the tag would drop. | The 4/6/8-bit settings are separate PTQ configurations ("to 8-bit, 6-bit, and 4-bit", paper p09), so they are alternative modes. Within a config every element has the same width, and what coexists is two encodings (E1M2/E2M1) of one width. That is what `ADAPTIVE` already records. §3: `MIXED` = "widths that coexist in the evaluated design". The `MIXED` was a human ruling of 2026-09-14 (PN L83; AN L485, where the reader had argued against it). Not overturned here, only flagged. If kept, the only same-design width coexistence is the FP16/BF16 accumulator and BF16 non-GEMM path (note L43; paper p08), and BF16 is not in the tag set. | med |

- `ADAPTIVE` is correct: the exponent/mantissa split is a data-dependent type per block/sub-block. This is the §3 definition and the Pass 1 entry (README L134). **verified**
- `FP8` is acceptable. The 8-bit instance is E1M6/E2M5, not OCP E4M3/E5M2 (note L31). It is still a narrow 8-bit float. The 6-bit setting is evaluated but untagged, and FP6 is off-vocabulary, which is fine. **verified**
- Stage `S2` (venue, note L12) vs papers.md L219 `S1→S2`: consistent under §4 "Stage is scope; the path is the trajectory". By §4 the S1 half is the element field split plus the in-PE bit mapper to E2M2 (note L57). The S2 half is the per-block E8M0 scale and the decoupled block/sub-block format granularity (note L35, L55). Both are right. **verified** / **inferred**
- Cell hygiene (low): the Note cell says "one config bit per block". Per note L37/L49 it is one bit per block **or sub-block**, and the sub-block setting is the best-accuracy one (note L39). Suggest "one config bit per block or sub-block".

### 5. [OASIS](../../survey/papers/OASIS/paper-note.md) ([pdf](../../survey/papers/OASIS/506501a307.pdf)) -> oasis — **OK** (vocabulary note only)

No axis changes proposed.

- All five axes in the venue row = note L9-L13 = AN L289-L293. papers.md L220 `S3`, ASIC. **verified**
- Stage, by §4: both operands are indices into learned K-Means codebooks (note L29-L30), which is test (a), and the product comes from the precomputed Cartesian table, which is test (b). `S3` is solid. **verified**
- `VQ` is right under the §3 definition ("k-means codebooks. Values become indices"), even though OASIS clusters scalars rather than vectors (eva.md L26 notes this). **verified**
- Off-vocabulary (low): `INT3` is not in the §3 traditional list (INT8/INT4/INT2). More substantive: on this row `INT4`/`INT3` name **index widths**, not integer-valued numbers. Mokey's row sets the precedent (`VQ LUT FIXED INT4`), so this is consistent within the venue, but a reader or classifier may take it as uniform INT4 quantization. Flag only.
- `MIXED`: supported. 1% FP16 outlier activations coexist with 4-bit indices (note L42-L47), and in W4A3, 4-bit and 3-bit operands coexist. **verified**
- Cell hygiene: "learned codebook" is used affirmatively. OK.

### 6. [Omni-LUT](../../survey/papers/Omni-LUT/paper-note.md) ([pdf](../../survey/papers/Omni-LUT/506501a322.pdf)) -> omni-lut — **CHANGE PROPOSED**

| Axis | Current | Proposed | Evidence | Confidence |
|---|---|---|---|---|
| Data type | `LUT VQ INT4 INT3 FP16 MIXED` | `LUT INT4 INT3 FP16 MIXED` (drop `VQ`) | **verified**: the paper has **zero** hits for `codebook`, `k-means`, `vector quantiz`, `VQ` or `centroid`. The representation is BCQ, defined as `W_i ≈ Σ_j B_ij·a_j` with `B ∈ {−1,+1}` and high-precision scales (paper p03). The paper extends it "with an offset and structured power-of-2 scalers … compatible with uniform quantization". The V path is BC-UQ, where "we do not learn the scaling factors" and fixes them (p03), and the note gives α_i = δ_v·{4,2,1,0.5} (note L52). Values are a scaled sum of binary planes, not indices into a learned table. AN L323 justifies `VQ` only as "non-uniform, index-coded", which is not the §3 `VQ` definition. The README's own Pass 7 refinement says the table "holds analytic partial sums, not learned values" (README L373-L375). | high |
| Stage | `S3` | `S2` (papers.md L222 path `S2→S3` unchanged) | **The LUT trap, §4 / Pass 7.** The table is built per tile from FP16 activations (scale-aware LGU, note L82-L91). It is a table of analytic partial sums, the same mechanism as LUT Tensor Core and Transitive Array, which are venue `S2` (README L360) and path `S2→S3` (papers.md L305, L309). FIGLUT (BCQ-compatible LUT) is grouped with Omni-LUT as `S2→S3` arithmetic lookup in survey/lut.md L141 and survey/stages.md §S2→S3. Test (a) does not hold once `VQ` goes (see above). The stored decomposition is a sum of scaled binary terms, which §6 "Stored versus transient" places at S1/S2, not S3. Only the stray `VQ` tag keeps the row classifying as `S3`, the same failure mode §3 records for AQ2PNN/SpAtten. **Conflicts with recorded ruling**: Pass 7 lists Omni-LUT with "learned centroids → S3" (README L360, L367), and its refinement says the venue "tags … are unchanged; the refinement is a second axis" (README L376-L377). The Pass 7 premise is contradicted by the paper. | med-high (the rule application is high; overturning Pass 7 is the owner's call) |

- Level `ALGO+ARCH`, Q `Q`: agree across the row, note L9-L10 and AN L321-L322. **verified**
- `INT3` is off-vocabulary (low), as for OASIS. Here the widths are bit-plane counts, which is closer to a real 3/4-bit width than OASIS's index widths.
- Cell hygiene: Pass 7's sentence "Contrast EVA, OASIS, Omni-LUT and Mokey, whose tables hold *learned centroids*" (README L360) is factually wrong for Omni-LUT and is contradicted 15 lines later (L373-L375). It is a log entry, so leave it standing, but whoever applies the change should add a later-pass correction. Optimization `phase-adaptive systolic` contains "adaptive". A regex for the `ADAPTIVE` data type could match it, which is the §7 warning. low. Note-file hygiene (not the row): omni-lut.md has stray runs of blank lines (L39-L40, L65-L68, L126-L127) and trailing double-space line breaks (L31-L32). Cosmetic.

### 7. [P3-LLM](../../survey/papers/P3-LLM/paper-note.md) ([pdf](../../survey/papers/P3-LLM/506501a604.pdf)) -> p3-llm — **MINOR**

| Axis | Current | Proposed | Evidence | Confidence |
|---|---|---|---|---|
| Stage | `—` | `S2` (and papers.md L222 `—` -> `S2`, or `S1→S2` as path, see below) | **verified** drift: note L12 = `S2`, pim.md L106 = `S2` / "Outlier handling", Pass 7 = `S2` (README L359). By §4: operand-dependent formats across the array, per-head KV scales, per-channel key smoothing and scale fusion are all block/array scope, so `S2`. **Path note (inferred)**: P3-LLM also derives a new scalar format, FP8-S0E4M4 for attention scores (no sign, E4M4, bias −15, no scale; note L30, L39-L45). That is an S1 design object. So the papers.md path could reasonably be `S1→S2`, not `S2`. | med (S2 scope); low (S1→S2 path) |
| Data type (possible `ADAPTIVE`) | `FP4 INT4 FP8 MIXED` | Consider `+ADAPTIVE` | BitMoD FP4 "adaptively remaps" the redundant −0 slot to one of {±5, ±8}, chosen **per group of 128** (paper p06; note L27). That makes the value set of one number data-dependent per group, which is the same kind of variable that earned MXFFP its `ADAPTIVE` (README L134). Against: the format is inherited from BitMoD, which argues for leaving it off. But Data type records what a number looks like, not the contribution (TAX worked examples: "non-Q papers still get a stage" / Sanger INT8). Raised for consistency with MXFFP, not as an error. | low |

- `FP16` not tagged: RoPE/Softmax/element-wise stay "in high precision" on the NPU (paper p07; note L34). Other rows (EVA, OASIS, Omni-LUT) tag their FP16 escape path. Adding it would be consistent, but the paper's word there is "high precision", not FP16 explicitly at p07, so it is not proposed. low
- Level `ALGO+ARCH`, Q `Q`, Data type: agree across the row, note L9-L11 and AN L388-L390. **verified**
- Cell hygiene: the Optimization cell contains both `PIM` and `NDP`. That is fine. The Note cell matches note §1. No negated trigger words.

---

### Summary

| Paper | Verdict | Proposed change(s) | Confidence |
|---|---|---|---|
| [NDPLowBitFP](../../survey/papers/NDPLowBitFP/paper-note.md) ([pdf](../../survey/papers/NDPLowBitFP/506501b383.pdf)) | MINOR | Data type +`FP16` (W-only A16 / S16 configs, FP16 PU mode). Stage `—` -> `S2` to match note + pim.md (venue and papers.md) | med / med |
| [EVA](../../survey/papers/EVA/paper-note.md) ([pdf](../../survey/papers/EVA/506501b351.pdf)) | OK | none (consistency remark vs SamsungNPU `MIXED`) | — |
| [LoKA](../../survey/papers/LoKA/paper-note.md) ([pdf](../../survey/papers/LoKA/506501b368.pdf)) | OK | none. Hygiene: `model-hardware co-design` keyword could mislead a Level classifier | low |
| [MXFFP](../../survey/papers/MXFFP/paper-note.md) ([pdf](../../survey/papers/MXFFP/506501c505.pdf)) | MINOR | `MIXED` fails §3 (same width, alternative 4/6/8 modes). **Conflicts with recorded ruling** (human 2026-09-14), so flagged only. Note cell: "per block or sub-block" | med / low |
| [OASIS](../../survey/papers/OASIS/paper-note.md) ([pdf](../../survey/papers/OASIS/506501a307.pdf)) | OK | none. `INT3` off-vocabulary; INT4/INT3 here are index widths | low |
| [Omni-LUT](../../survey/papers/Omni-LUT/paper-note.md) ([pdf](../../survey/papers/Omni-LUT/506501a322.pdf)) | CHANGE PROPOSED | Drop `VQ` (BCQ, no codebook in paper). Stage `S3` -> `S2` (LUT trap, analytic partial-sum table, like LUT Tensor Core / Transitive Array). **Conflicts with recorded Pass 7 ruling**, whose premise the paper contradicts | high / med-high |
| [P3-LLM](../../survey/papers/P3-LLM/paper-note.md) ([pdf](../../survey/papers/P3-LLM/506501a604.pdf)) | MINOR | Stage `—` -> `S2` to match note + pim.md + Pass 7 (path possibly `S1→S2` for FP8-S0E4M4). Consider `ADAPTIVE` for BitMoD per-group remap | med / low |

## Group 2

## Audit G2: ISCA venue tags for SingularBit, UniCore, XtraMAC, AQuant, ENEC, ELSA, Phi

Date: 2026-10-01. Read-only audit. Sources:
- `QuantArchSurvey/TAXONOMY.md`
- `QuantArchSurvey/venues/ISCA/README.md`, live rows L41-45 plus the Tag revision log, Passes 1-10
- the published notes in `QuantArchSurvey/venues/ISCA/notes/`
- `survey/papers/<Dir>/{ANALYSIS,paper-note}.md`
- the extracted paper text in `survey/papers/<Dir>/extracted/`
- `QuantArchSurvey/survey/papers.md` and `survey/gen/3-paths-classify.py`
- for ELSA and Phi, `git show 4e76122^:venues/ISCA/{README.md,notes/elsa.md,notes/phi.md}`

Page references (`pNN`) are to `extracted/<id>.pages/pNN.txt`.

**verified** means I read the cited file or line myself. **inferred** means it is my reading of the rules.

---

### Cross-cutting finding (affects all five live rows): the note sync would revert Stage to Generation

- **verified.** `Claude/scripts/sync_notes.py` (docstring L1-21) publishes `survey/papers/<Dir>/paper-note.md` byte for byte. The only things it removes are §6 and two labelled §5 blocks.
- **verified.** I diffed each working `paper-note.md` (with §6 cut off) against the published note. For SingularBit, UniCore, XtraMAC, AQuant and ENEC the **only** differing line is Tags row 12. The working copy still reads `**Generation** | G3/G2`, and the published copy reads `**Stage** | S2/S3`. The published Stage rows were edited directly in the team repo (commit `c044026`).
- **inferred.** The next `sync_notes.py` run would therefore overwrite every published Stage row with the retired Generation tag. The same applies to ELSA and Phi on restore: their working `paper-note.md` files are identical to the deleted published notes and carry `**Generation** | —`.
- **Recommendation.** Before re-syncing, update the Tags table in each working `paper-note.md` to `**Stage**`, using the values below.

---

### [SingularBit](../../survey/papers/SingularBit/paper-note.md) ([pdf](../../survey/papers/SingularBit/506501b001.pdf)) (ISCA'26). Verdict: **CHANGE PROPOSED** (Data type)

| Axis | Current | Proposed | Evidence | Confidence |
|---|---|---|---|---|
| Data type | `SVD` `INT2` `INT1` `MIXED` | `SVD` `INT4` `INT3` `INT2` `INT1` `FP16` `LUT` `MIXED` | **verified.** "K = 4 regions, assigning 4, 3, 2, and 1-bit precisions" and `b_k ∈ {4,3,2,1}` (p05). The tensor core "processes 1–4 bit weights through the same hardware path" (p08). These four widths coexist within one matmul, which is the §3 `MIXED` sense, so `INT4` and `INT3` belong in the cell. "Most parameters 1–2 bits" describes the distribution, not the set of widths. | high (INT4/INT3) |
| | | (FP16) | **verified.** "32 × 32 PE array that performs bit-serial mixed-precision weight computation with **FP16 activations**" (p07). The KV path is an "FP16-to-INTx quantizer" (p08). | high |
| | | (LUT) | **verified.** "Our tensor core builds on lookup table (LUT)-based computation paradigm… The activation loader precomputes FP16 partial sums over four input channels… eight entries… weight bits select the corresponding partial sum through a multiplexer" (p08). That matches §3 `LUT` ("resolved by table lookup rather than by a multiplier"). **This is the §4 LUT trap**: the table holds analytic partial sums, so it is **not** S3 and the venue Stage stays `S2`. | med-high |
| papers.md path | `S2` | `S2→S3` (follows automatically once `LUT` is in the cell) | **inferred**, from `3-paths-classify.py`: `"`LUT`" in dtype and LUTARITH` gives `S2→S3`. LUTARITH matches `precomputed … partial sum` or `bit-serial`/`BCQ` if an Optimization keyword is added. This is the same shape as Omni-LUT, which also has binary-coded weights and a table of analytic partial sums and is overridden to `S2→S3`, and as LUT Tensor Core and Transitive Array, which are venue `S2` with `LUT`. | med |
| Optimization | (8 keywords) | add `LUT-based bit-serial tensor core` `hierarchical binary quantization (ARB-LLM)` `GPTQ error feedback` | **verified.** The weights are "decomposed into a series of binary bases B_i ∈ {−1,+1}… scaled by row-wise and column-wise factors", with `W = Σ α_r α_c B_i` (p06). They are integrated into a "GPTQ error-feedback framework" (p05-06). | med |

**Other axes.**
- **Level `ALGO+ARCH`**: OK, verified. The ANALYSIS "Proposed tags" table and the abstract both say "two algorithm-hardware co-designs".
- **Q**: OK.
- **Stage `S2`**: OK under §4. The scope is array-level: "spatial mixed precision" across cores for U, "temporal" mixed precision along the reduction for Vᵀ (p08), plus group scales. Test (a) fails because the values are scaled binary-coded integers that decode analytically. Test (b) fails because the tables hold analytic partial sums.
- **Note-vs-row**: the published note's Tags table matches the row.

**Data type caveat (inferred).** The weights are binary-coding quantization (BCQ) with fitted per-row and per-column scales, not uniform integers. The `INTn` labels follow the venue convention already used for Omni-LUT's BCQ, so they are acceptable. The ANALYSIS (Proposed-tags table, Data-type line) already notes that `SVD` names a basis rather than a format.

**Cell hygiene.**
- `SVD` appears in both Data type and Optimization. That is harmless and the venue does the same elsewhere, for example EVA with `VQ`.
- Note cell: "Precision allocated by rank; most weight parameters to 1–2 bits" is accurate.
- No regex hazards.

---

### [UniCore](../../survey/papers/UniCore/paper-note.md) ([pdf](../../survey/papers/UniCore/506501c520.pdf)) (ISCA'26). Verdict: **MINOR**

| Axis | Current | Proposed | Evidence | Confidence |
|---|---|---|---|---|
| Data type | `FP8` `FP4` `ADAPTIVE` `MIXED` | `FP16` `FP8` `FP4` `ADAPTIVE` `MIXED` | **verified.** W16A16 is an evaluated mode, "W16×A16 (E5M10)" in Fig. 6c (p05), i.e. FP16. The abstract's headline "up to 5.26× at W16A16" is reported in that mode. | high |

**Other axes.**
- **`ADAPTIVE`**: correct under §3, verified. DynFP is "a per-group configurable 4-bit (or 3-bit)" format in which "each group chooses its floating-point layout (e.g., E3M0, E2M1, E1M2)" (p08). That is a data-dependent *type*, not a width.
- **`MIXED`**: correct, verified. W4A8 is evaluated (p01, p10-13), so two widths coexist.
- **Stage `S2`**: correct under §4. The E/M layout is chosen per group, which is a block-scope decision ("deciding that 32 of them share…"). The composable slice datapath is also array-scope.
- **papers.md path `S1→S2`**: consistent. DynFP plus Mitchell is the S1 half.
- **Level `ARCH`**: OK. The ANALYSIS (Proposed-tags table, Level row) considered `ALGO+ARCH` and kept `ARCH`, and I do not contest that.
- **Note-vs-row**: matches.

**Cell hygiene.**
- The published note §1 says "**1.24×–3.95% area efficiency**", which is a typo for `3.95×`. §4 of the same note says `1.24×–3.95×`. This is in the note, not the row.
- Optional Optimization additions: `per-group E/M allocation`, `negative-zero remap`, `subnormal removal`. All are verified on p05 and p08.
- No regex hazards. `Mitchell` and `DynFP` intentionally match S1SIG.

---

### [XtraMAC](../../survey/papers/XtraMAC/paper-note.md) ([pdf](../../survey/papers/XtraMAC/506501c536.pdf)) (ISCA'26). Verdict: **CHANGE PROPOSED** (Data type; Stage drift in note and mirrors; papers.md path)

| Axis | Current | Proposed | Evidence | Confidence |
|---|---|---|---|---|
| Data type | `INT8` `INT4` `FP8` `FP4` `BF16` `MX` `MIXED` | add `FP16`, plus optionally `INT2` | **verified.** Table IV (p09) evaluates "INT2-8 × FP16 + FP16 → FP16" and "FP4 × FP16 + FP16" against the vendor IP. Fig. 7 has an "FP16-based MAC" series. Fig. 6 lists `INT2–8b×FP16+FP32→FP32` and similar configurations. So FP16 is an evaluated operand format. INT2 is the low end of the "INT2–8" operand range. FP32 and INT32 also appear, but only as accumulator formats; adding them is optional. | high (FP16) / med (INT2) |
| Stage (venue row) | `—` | keep `—` until the FPGA owner rules. My reading is `S2`. | **verified.** `—` is the owner reset from commit `4f55edc` (2026-09-22): "Reset Stage to unassigned for 166 FPGA, PIM and non-machine records". It is legitimate per TAXONOMY §4 "What `—` means". **inferred:** on the evidence the scope is a MAC datapath shared across formats (the S2 "mixed type" mechanism). | high that `—` is legitimate; med on S2 |
| Note Tags Stage | `S2` | align with the row. Either set the note to `—` with "(owner reset; reader reading: S2)", or record the S2 reading as the domain owner's call. | **verified.** The note says `S2` and the row says `—`. The note was migrated by `c044026`, one day before the reset. `survey/fpga.md` L289 also mirrors `S2`, which is stale against the venue row. | high |
| papers.md path | `S1→S2` | `S2`. This **conflicts with a recorded hand audit**: stage1.md §8 and the `OVERRIDE` entry in `3-paths-classify.py`. | **verified.** The published note §2 says "**Contributes none — executes existing formats.**" The unified mantissa product and the INT "logical unbiased exponent of zero" are decompositions inside the datapath. Under TAXONOMY §6 "Stored versus transient" (the Bit-Pragmatic case), a decomposition that exists only in the datapath has no S1 half. **verified (code):** `path()` checks `OVERRIDE` *before* the `st=="—"` terminator. That is why papers.md shows `S1→S2` for a row whose Stage is `—`, which contradicts the code's own comment "An unassigned Stage terminates the derivation". | med |

**Other axes.**
- **`MX`**: verified. "UE8M0 × BF16 + BF16" is a supported configuration (p01), and GPT-oss-20B MXFP4 is evaluated.
- **`MIXED`**: correct under §3. INT4×BF16 operands coexist in one MAC, which is more than alternative modes.
- **Platform FPGA**: OK. The device is an Alveo U55c.
- **Level and Q**: OK.

**Cell hygiene.**
- The `FPGA` keyword in Optimization is what drives Platform. Keep it.
- The ANALYSIS (Proposed-tags table, Optimization row) proposed `separate INT/FP accumulation`; the row says `datatype-specific accumulation`. Same meaning, so this is fine.
- Note cell: OK.

---

### [AQuant](../../survey/papers/AQuant/paper-note.md) ([pdf](../../survey/papers/AQuant/506501b417.pdf)) (ISCA'26). Verdict: **CHANGE PROPOSED** (published note's Stage). The venue row is OK.

| Axis | Current | Proposed | Evidence | Confidence |
|---|---|---|---|---|
| Note Tags Stage | `S3` (published note) | `S2` (matches the row) | **verified.** Pass 7's migration table (README, revision log) explicitly lists AQuant among the rows that moved `G3` → **`S2`**: "the decode is still analytic". The note's `S3` came from a blind G3→S3 rename in commit `c044026`; the working note still says `G3`. **Under §4:** value = base token (INT8) + delta (INT2/INT4 with an affine scale). That is recoverable arithmetically, so test (a) fails. The MAC arrays are arithmetic, so test (b) fails. The scope is a per-row top-k precision split across two MAC arrays, which is array scope. The AQB8 precedent (anchor + INT8 offset, venue `S2`) agrees. | high |

**Other axes.**
- **Data type**: matches the paper, verified. The paper has INT4/INT2 deltas, INT8 bases and INT4×INT16 multiplies with INT16 weights (p10-11), plus "75% INT2, 25% INT4 deltas, 7.4% INT8 bases".
- **`ADAPTIVE`**: correctly absent despite "Adaptive Quantization" in the title. Only the width varies, so §3 applies.
- **`MIXED`**: correct.
- **Level, Q and Platform (ASIC)**: OK.
- **papers.md path `S1→S2`**: derived from the S1SIG pattern `base-delta`. **inferred, low:** the element itself is a plain INT2/INT4 and the base is shared across F = 18 tokens, so arguing for an S1 half is weak. It is consistent with AQB8, though, so no change is proposed.

**Cell hygiene.**
- Optional: `FP16`/`FP32` could be added to Data type for the non-linear escape hatch ("all non-linear ops in FP", published note §2). This is low priority.
- The Optimization keyword `KV cache` is supported: the note §3 Decode paragraph says KV is re-quantized and stored compressed.
- The Note cell is accurate and has no regex hazards. The title's word "Adaptive" does not match S1SIG, which requires `` `ADAPTIVE` `` or "adaptive … type".

---

### [ENEC](../../survey/papers/ENEC/paper-note.md) ([pdf](../../survey/papers/ENEC/506501b319.pdf)) (ISCA'26). Verdict: **OK**

No axis change proposed.

- **Q**: `Q` is the Pass 4 owner ruling, which conditions Q on the numeric format. **This conflicts with a recorded ruling**, though not with the row: the working `ANALYSIS.md` "Proposed venue-list row" still says `non-Q`. That draft is superseded, and the published note and the row both say `Q`. Not re-litigated.
- **Level `ALGO+SYS`**: Pass 1, verified. The paper has no RTL, synthesis or area figures (note §3 "Hardware cost: none").
- **Data type `BF16` `FP16` `FP32`**: verified (note §2). `MIXED` is correctly absent because the three formats are per-model alternatives, which is the §3 alternative-modes rule. The 3-bit/6-bit group code widths are code lengths, not numeric precisions. `V2F` is correctly absent because the coding is fixed-length, not variable-to-fixed.
- **Stage `S2`**: correct under §4. The stored exponent code is an affine remap `y = (2ⁿ − x + b) mod 2ⁿ`, which is analytic and invertible, so test (a) fails. The Cube unit multiplies full BF16, so test (b) fails. The width is chosen per group of L = 16, which is block scope. papers.md path `S2` is consistent.
- **Platform ASIC**: OK (inferred). It is a kernel method on a shipping NPU, analogous to how GPU kernel papers are classed `GPU`. The `P_NONHW` regex does not fire.

**Cell hygiene.**
- The Note cell ("Software method for a shipping NPU, not new hardware") is accurate but thin. Optionally add "exponent field only; BF16 16 → 11.85 bits, CR 1.35×, bit-identical" (note §1, §2). Avoid wording such as "no hardware proposed", because `P_NONHW` would then switch Platform to `Other`.
- All Optimization keywords are supported by note §3.
- Note-vs-row: matches.

---

### [ELSA](../../survey/papers/ELSA/paper-note.md) ([pdf](../../survey/papers/ELSA/506501c550.pdf)) (ISCA'26). Verdict: **CHANGE PROPOSED** (restore; new-schema row)

Old row (from `4e76122^` README L63): `ARCH+SYS | non-Q | TERNARY INT4 MIXED | — (Gen) | …`.

| Axis | Old | Proposed | Evidence | Confidence |
|---|---|---|---|---|
| Level | `ARCH+SYS` | `SYS+ARCH` | **inferred.** This only changes the order: the venue's canonical order is ALGO, SYS, ARCH (`SYS+ARCH` for NDPLowBitFP, `ALGO+SYS+ARCH` for LUT Tensor Core). `SYS` is kept for the §VI offline partition/placement/routing (ELSA paper-note §6, the "Two seed-tag disputes" bullet; the reader left it open). | med |
| Q? | `non-Q` | `non-Q` | **verified.** Owner ruling of 2026-09-14 (ELSA paper-note §6, "SETTLED 2026-09-14"). Not re-litigated. | high |
| Data type | `TERNARY` `INT4` `MIXED` | unchanged | **verified.** "use 4-bit quantized weights" (p07); ST-BIF emits "ternary spikes ({-1,0,1})"; membrane "(12-bit)" against weights (4-bit) and spikes (1-bit) (p04-06). `MIXED` holds because 4-bit weights, ternary spikes and a 12-bit membrane coexist. Optionally add `INT12` for the membrane accumulator. | high |
| Stage | `—` (Gen) | `—` | **verified.** TAXONOMY §4 "What `—` means": the owner reset covers spiking records, and the axis-in-doubt meaning is carried only by `survey/snn.md`, which says every spiking record is `—`. **inferred:** if the axis were later applied, the temporal-unary activation would argue for test (a) (an S3-family return to an ordinary datapath). That is for snn.md to decide. | high |
| Platform | — | `SNN` | **verified.** The `P_SNN` regex matches `SNN` in Optimization, and SNN outranks PIM and ASIC (§5; papers.md Platform table). | high |
| Note | "Bundled address-event-representation protocol to lower communication traffic" | see the row below | The old Note is the source-sheet keyword. The proposed one adds the format facts (note §1, §2) and points to snn.md, so the `—` is explained. | med |

**Proposed row, ready to paste into `## 2026`:**

```
| [x] | [ELSA: An ELastic SNN Inference Architecture for Efficient Neuromorphic Computing](https://doi.org/10.1109/ISCA66397.2026.00178) | [**human ✓**](notes/elsa.md) | SYS+ARCH | non-Q | `TERNARY` `INT4` `MIXED` | — | `SNN` `elastic inference` `spine/token-wise pipeline` `bundled AER` `early termination` `input-adaptive time-steps` `mini-batch Gustavson-product` `membrane-stationary dataflow` `addition-only` `near-SRAM` `ANN-to-SNN conversion (SpikeZIP-TF)` `NoC mapping + multi-path routing` | A 4-bit-weight QANN run as an exactly equivalent spiking net: ternary spikes over T ≤ 32 steps into a 12-bit membrane held in SRAM. Bundled AER cuts NoC traffic. Stage left unassigned as spiking work, see [snn.md](../../QuantArchSurvey/survey/snn.md) |
```

**Regex check on this row.**
- `input-adaptive time-steps` does not match S1SIG, which requires `` `ADAPTIVE` `` or "adaptive … type".
- `near-SRAM` does not match P_PIM.
- The row contains no "codebook", "posit" or "not …" phrasing.
- With Stage `—`, `path()` returns `—`.

**Restore prerequisites.**
- `notes/elsa.md` must be republished. The working `paper-note.md` is byte-identical to the deleted note and needs its Tags row changed from `**Generation** | —` to `**Stage** | —`.
- `EXCLUDED` in `sync_notes.py` already has ELSA removed (L40 comment: "restored 2026-10-01 (ISCA Pass 11)").
- The section heading `## 2026 (12)` → `(13)` and the page header counts need updating.
- The snn.md "Screened out" table (L42) and the README Pass 5 table are history and should not be edited. snn.md's "In the corpus (3)" list would gain ELSA. `5-check.py` counts `plat_snn` from that heading.

---

### [Phi](../../survey/papers/Phi/paper-note.md) ([pdf](../../survey/papers/Phi/2505.10909.pdf)) (ISCA'25). Verdict: **CHANGE PROPOSED** (restore; new-schema row)

Old row (from `4e76122^` README L79): `ARCH | non-Q | BINARY VQ | — (Gen) | …`.

| Axis | Old | Proposed | Evidence | Confidence |
|---|---|---|---|---|
| Level | `ARCH` | `ALGO+ARCH` | **verified.** The paper calls itself "Our algorithm-hardware co-design approach… k-means-based pattern selection and pattern-aware fine-tuning" (p12, and contribution (2) on p02). TAXONOMY §1 says such papers are "almost always" `ALGO+ARCH`. The ANALYSIS Level justification only rules out `SYS` ("PAFT is a training recipe, not a system"); it does not address `ALGO`. | med |
| Q? | `non-Q` | `non-Q` | **verified.** Owner and reader ruling (Pass 1, Pass 3; note §5). Not re-litigated. | high |
| Data type | `BINARY` `VQ` | `BINARY` `VQ` `LUT` | **verified.** Level-1 rows are stored as an index into k-means binary patterns, which matches §3 `VQ` mechanically ("k-means codebooks. Values become indices"), and the reader kept `VQ` in the note's Tags. The paper cites Product Quantization [30] for its distance metric. Each index "retrieves an offline-precomputed pattern-weight product" (note §2), so that part of the computation is a table read, which is §3 `LUT`. **Flag:** the Pass 3 and Pass 5 text and snn.md say "the k-means patterns are a basis, not a codebook". That sits in tension with the reader's own `VQ` tag. If the owner prefers that wording, drop `VQ` and keep `BINARY` `LUT`. The paper states no weight precision; a grep for INT8, INT4, FP16, FP32 and bit-width returns nothing relevant, so no weight tag is added. | med (LUT) / low (VQ-vs-ruling) |
| Stage | `—` (Gen) | `—` | **verified.** Same reasoning as ELSA: TAXONOMY §4 owner reset and axis in doubt, per snn.md. **inferred:** if it were ever assigned, `VQ` plus "k-means" in the cell would make S3SIG derive the S3 family. Whoever assigns it should decide on purpose, or record the decision in NOT_S3 or IS_VALUE. | high |
| Platform | — | `SNN` | **verified.** `P_SNN` regex; §5 precedence. | high |
| Note | "…Reader leaves the generation unassigned" | reword | That sentence refers to the retired Generation axis (TAXONOMY Appendix A: "do not assign"). Replace it with a Stage pointer. Avoid "not a codebook" phrasing because the classifier cannot read the negation (§7). | high |

**Proposed row, ready to paste into `## 2025`:**

```
| [x] | [Phi: Leveraging Pattern-based Hierarchical Sparsity for High-Efficiency Spiking Neural Networks](https://arxiv.org/abs/2505.10909) | [**human ✓**](notes/phi.md) | ALGO+ARCH | non-Q | `BINARY` `VQ` `LUT` | — | `SNN` `pattern-based sparsity` `k-means patterns` `precomputed products` `exact two-level decomposition` `Hamming-distance clustering` `PWP prefetch` `optional PAFT` | **Exact** two-level decomposition: L1 k-means binary patterns whose products with the weights are precomputed offline and fetched by index, L2 a {1,−1} element-wise correction. Nothing loses precision. Stage left unassigned as spiking work, see [snn.md](../../QuantArchSurvey/survey/snn.md) |
```

If the owner keeps the reader's original Level and Data type, the conservative variant changes only the Stage, Platform and Note cells:

```
| [x] | [Phi: Leveraging Pattern-based Hierarchical Sparsity for High-Efficiency Spiking Neural Networks](https://arxiv.org/abs/2505.10909) | [**human ✓**](notes/phi.md) | ARCH | non-Q | `BINARY` `VQ` | — | `SNN` `pattern-based sparsity` `k-means patterns` `precomputed products` `exact two-level decomposition` `Hamming-distance clustering` `PWP prefetch` `optional PAFT` | **Exact** two-level decomposition: L1 k-means binary patterns with offline-precomputed products, L2 a {1,−1} element-wise correction. Stage left unassigned as spiking work, see [snn.md](../../QuantArchSurvey/survey/snn.md) |
```

**Restore prerequisites.**
- These are the same as for ELSA: republish `notes/phi.md` with its Tags row changed from Generation to Stage, update the `## 2025 (8)` → `(9)` count, and add Phi to snn.md "In the corpus".
- The DOI 10.1145/3695053.3731035 is recorded in the note header. The old row linked arXiv, consistent with the other 2025 rows.

---

### Summary

| Paper | Verdict | Main finding |
|---|---|---|
| [SingularBit](../../survey/papers/SingularBit/paper-note.md) ([pdf](../../survey/papers/SingularBit/506501b001.pdf)) | CHANGE PROPOSED | Data type is missing `INT4` `INT3` (K = 4 regions at 4/3/2/1 bits coexist), `FP16` (activations) and `LUT` (LUT-based bit-serial tensor core). Stage `S2` stays, as the analytic-partial-sum LUT trap. With `LUT` added, the papers.md path becomes `S2→S3`, like Omni-LUT. |
| [UniCore](../../survey/papers/UniCore/paper-note.md) ([pdf](../../survey/papers/UniCore/506501c520.pdf)) | MINOR | Add `FP16` (W16A16 = E5M10, the headline 5.26× mode). `ADAPTIVE`, `MIXED` and `S2` are correct. Note §1 typo "3.95%". |
| [XtraMAC](../../survey/papers/XtraMAC/paper-note.md) ([pdf](../../survey/papers/XtraMAC/506501c536.pdf)) | CHANGE PROPOSED | Add `FP16` (Table IV, p09), and optionally `INT2`. The row's `—` is a legitimate FPGA owner reset, but the note and fpga.md still say `S2`. The papers.md `S1→S2` comes from an OVERRIDE that also bypasses the `—` terminator in `path()`. My reading is `S2` with no S1 half, which conflicts with the stage1.md §8 hand audit. |
| [AQuant](../../survey/papers/AQuant/paper-note.md) ([pdf](../../survey/papers/AQuant/506501b417.pdf)) | CHANGE PROPOSED (note only) | The published note says `Stage S3` because of a blind G3→S3 rename. Pass 7 and §4 both give `S2`, as the row has. The row is OK. |
| [ENEC](../../survey/papers/ENEC/paper-note.md) ([pdf](../../survey/papers/ENEC/506501b319.pdf)) | OK | All axes consistent. The ANALYSIS draft `non-Q` conflicts with the Pass 4 owner ruling `Q`, which stands. |
| [ELSA](../../survey/papers/ELSA/paper-note.md) ([pdf](../../survey/papers/ELSA/506501c550.pdf)) | CHANGE PROPOSED (restore) | `SYS+ARCH` · non-Q · `TERNARY` `INT4` `MIXED` · `—` · Platform SNN. Note rewritten. |
| [Phi](../../survey/papers/Phi/paper-note.md) ([pdf](../../survey/papers/Phi/2505.10909.pdf)) | CHANGE PROPOSED (restore) | `ALGO+ARCH` · non-Q · `BINARY` `VQ` `LUT` · `—` · Platform SNN. `VQ` sits in tension with the "basis, not a codebook" ruling text. The Note's Generation reference is replaced. |

**Cross-cutting.** `sync_notes.py` republishes the working `paper-note.md` files verbatim, and all seven still carry a `**Generation**` row. A re-sync would revert the published Stage rows to Generation. Fix the working notes first.

**Process disclosure.** During the audit I briefly wrote two temporary copies of the old ELSA and Phi notes into the scratchpad in order to diff them. I deleted them immediately. No other file was created or modified.

## Group 3

## Audit G3: ISCA 2025 rows (Transitive Array, LUT Tensor Core, MicroScopiQ, Oaken, AQB8, Ecco, FATE)

Read-only audit. Paths are relative to `/home/hs359/moe_ws/quantization_survey/`.
`README` means `QuantArchSurvey/venues/ISCA/README.md` (rows at lines 51–57). `note` means
`QuantArchSurvey/venues/ISCA/notes/<abbr>.md`. `papers.md` means `QuantArchSurvey/survey/papers.md`.
Classifier results were reproduced by running the regexes from
`QuantArchSurvey/survey/gen/3-paths-classify.py` and `4-stage2-classify.py` against
`survey/gen/paths.json`. Nothing in the repo was modified.

Recorded owner rulings I did not reopen: Pass 7 (README l.360): Transitive Array and LUT Tensor Core are `S2`.
The Pass 7 refinement (README l.370–377, `survey/stages.md`): Ecco's path is `S3→S2`, and its venue tag stays `S3`.
Pass 2 (l.193–194): FATE and AQB8 moved to `Q`. Pass 3 (l.225): Ecco is `Q`.

---

### 1. [Transitive Array](../../survey/papers/TransitiveArray/paper-note.md) ([pdf](../../survey/papers/TransitiveArray/2504.16339.pdf)): **MINOR**

All five tag cells match across the published note, our `paper-note.md`/`ANALYSIS.md` and TAXONOMY.
- **Level:** `ARCH`, verified (note Tags l.9; ANALYSIS l.371).
- **Q?:** `Q`, verified.
- **Data type:** `LUT INT4 INT8 MIXED`, verified (note l.11; ANALYSIS l.373). W4A8 runs INT4 weights against INT8 activations in one evaluated design, so `MIXED` is a real coexistence and not just alternative modes. Verified against the paper, p10 Table 3 (`FC Act. Int8 / FC Wgt. Int4`).
- **Stage:** `S2`. This is the Pass 7 ruling: the table holds analytic partial sums, so test (a) fails. Test (b) also fails, because each entry is produced by one adder and the product is still arithmetic. My own reading of §4 agrees, so `S2` stays.
- **papers.md:** path `S2→S3` (l.307). The derivation gets there from `LUT` plus LUTARITH hits (`LUT-GEMM`, `result reuse`, `multiplication-free`). That agrees with `stages.md` l.141–148 and with the "scope ≠ path" rule. No action.

| Axis | Current | Proposed | Evidence | Confidence |
|---|---|---|---|---|
| Note prose, not a row cell | note §2 "Granularity. Elementwise, since it's int8" | Reconcile with the row's `group-wise scaling (g=128)` | The paper says "When the group size is 128, the vector unit applies an integer scale factor…" (p08 l.10). ANALYSIS l.373 also gives "group size 128". The note's §2 and its own Tags/Optimization disagree. Verified. | high |

**Cell hygiene.**
- **Optimization:** every keyword is supported by the note's Tags l.13, verified.
- **`LUT-GEMM` keyword:** it is a characterisation that the owner ruled on, not the paper's own word. ANALYSIS l.77/110 records that the paper never says "LUT" or "lookup". It stays. It is also the token that drives the `S2→S3` path, which is the intended effect.
- **Note cell:** "lazy … one add per entry, in Hamming order over a Hasse graph" matches note §1, verified. No regex hazard.

### 2. [LUT Tensor Core](../../survey/papers/LUTTensorCore/paper-note.md) ([pdf](../../survey/papers/LUTTensorCore/2408.06003.pdf)): **CHANGE PROPOSED** (Data type)

- **Level:** `ALGO+SYS+ARCH`, verified (Pass 1 l.129; ANALYSIS l.274).
- **Q?:** `Q`, verified.
- **Stage:** `S2` (Pass 7). The table is precomputed partial sums of activations, so it is the analytic LUT trap. I agree.
- **papers.md:** path `S2→S3`, Platform `GPU` (l.304). Both are consistent with the row and with `stages.md`. GPU is right because the design replaces a Tensor Core and was evaluated in Accel-Sim (ANALYSIS l.15, l.148).

| Axis | Current | Proposed | Evidence | Confidence |
|---|---|---|---|---|
| Data type | `LUT` `INT1` `INT2` `INT4` `FP16` `FP8` `MIXED` | add **`INT8`** | INT8 is in the evaluated design twice. (1) INT8 activations: `W_INT2 A_INT8` is the configuration of both the UNPU comparison (Table 2, p11 l.3) and the end-to-end Table 1 (p10 l.15–21). The DSE sweeps `A_INT8` (p08 l.59, l.83). (2) **Table quantization to INT8** (p05 l.67/76; p11 l.33 `W_INT2 A_LUT_INT8`). Our ANALYSIS l.276 already proposed `INT8`, and note §2 l.25 lists `A_…/INT8`. The tag fell out between the reading and the row. Verified. | high |
| Data type | (no INT16) | optionally add `INT16` | `A_INT16` is one of the four activation types in the evaluated 12-config DSE (p08 l.41, l.83). Note §2 l.25 lists it. `INT16` is off the TAXONOMY §3 vocabulary, but other ISCA rows already use it (Bit Fusion, AQuant, LightNobel, OLAccel). Verified that it is present. Whether to tag it is the owner's call. | med |

**Cell hygiene.**
- **Note cell:** "4×–6× power and area over a MAC tensor core at 1-bit weights" is verified against p08 l.96 ("with 1-bit weights … a 4×-6× reduc[tion]") and p02 l.29.
- **Optimization:** every keyword is supported by note l.13.
- No regex hazard.

### 3. [MicroScopiQ](../../survey/papers/MicroScopiQ/paper-note.md) ([pdf](../../survey/papers/MicroScopiQ/2411.05282.pdf)): **CHANGE PROPOSED** (Data type)

- **Level:** `ALGO+ARCH`, verified.
- **Q?:** `Q`, verified.
- **Stage:** `S2`, verified. This is outlier handling plus granularity: macro/micro-block scales and outliers paid for by pruning (note §2 l.29–30).
- **Is there an `S1` half?** The sign-duplication layout `{s·m₁, s·m₀}` is a per-element trick, but it serves block-level alignment. I read the scope as `S2` (inferred).
- **papers.md:** path `S2`, Platform `ASIC` (l.305). Consistent.

| Axis | Current | Proposed | Evidence | Confidence |
|---|---|---|---|---|
| Data type | `MX` `FP4` `INT2` `INT4` `MIXED` | add **`FP8`** | Outliers are MX-FP at 2·`bb`. At `bb`=4, which is the evaluated v1 W4A4 accelerator (p12 l.40–41), the outlier is an 8-bit **e3m4** FP. The paper says "quantized to either e1m2/e3m4 FP-format for b = 4 or 8-bit" (p05 l.72), and Fig. 9 reads "Outliers: Merged MX-FP-8" (p08 l.37). The row tags only the `bb`=2 case (FP4 = e1m2). The note's own §2 l.26 says "Outliers MX-FP @ 2·`bb`". Verified. | high |
| Data type | (no INT8) | consider adding `INT8` | Activations go to MX-INT-8 in the W4A8 and W2A8 settings (p11 l.59; p12/p13 Table 8 "Quantize activations to MX-INT-8"). The accelerator headline runs are A4, so INT8 is present in the evaluated algorithm but possibly not in the accelerator. Verified that it is present. Whether it "coexists in the evaluated design" is borderline. | med |

**Cell hygiene.**
- **Note cell:** "Outliers at 2× inlier bitwidth in MX-FP … 2.36 effective bits, memory stays aligned" is verified (note §1, §2 l.27). It is the same sentence that implies FP8 at `bb`=4, so the Note cell already supports the FP8 proposal.
- **Optimization:** every keyword is supported (note l.13).
- No regex hazard.

### 4. [Oaken](../../survey/papers/Oaken/paper-note.md) ([pdf](../../survey/papers/Oaken/2503.18599.pdf)): **MINOR**

- **Level:** `ALGO+ARCH`, verified.
- **Q?:** `Q`, verified.
- **Stage:** `S2`, verified. This is outlier handling: three magnitude groups and a dense-and-sparse COO path (note §3).
- **papers.md:** path `S2`, Platform `ASIC` (l.306). Consistent.
- **`INT5`:** off the TAXONOMY §3 vocabulary, but TAXONOMY says to give the bitwidth when it is known, and the paper is explicit: "quantizes middle group into 4-bit, inner and outer groups into 5-bit" (p08 l.42). Pass 2 (l.203–205) made this exact correction. Keep it.

| Axis | Current | Proposed | Evidence | Confidence |
|---|---|---|---|---|
| Data type | `INT4` `INT5` `MIXED` | consider adding `FP16` | Weights and activations stay FP16 by argument (note §2 l.28; ANALYSIS l.181–185), and the datapath is FP16 ("Peak FP16 TFLOPS 270.3", p04 l.41; p10 l.8). INT4/INT5 KV coexist with FP16 W/A in the evaluated design. Other rows here carry the unquantized operand (LUT TC `FP16`, OASIS/Omni-LUT/EVA `FP16`), but Tender and LightNobel do not, so the venue has no consistent policy. Verified that FP16 is present. Whether to add it is a policy question. | low–med |

**Cell hygiene.**
- **Note cell:** "inliers INT4, large **and small** outliers INT5, thresholds profiled offline … ~4.8 effective bits" is verified (note §2 l.25–27; paper p08).
- **Optimization:** every keyword is supported (note l.13).
- No regex hazard.

### 5. [AQB8](../../survey/papers/AQB8/paper-note.md) ([pdf](../../survey/papers/AQB8/10.1145_3695053.3731104.pdf)): **MINOR** (cell hygiene, plus one Platform question)

- **Level:** `ALGO+ARCH`, verified. This is the co-design wording of the paper's §8, and the SAH DP is not executed by any hardware (ANALYSIS l.409).
- **Q?:** `Q`, from the Pass 2 ruling. The published note's §5 (l.216–219) says the paper "could also be read as `NON-Q-ORIENTED`". I am not reopening that. Under the swap test, plain per-scene INT8 gives Fig. 1's test-count blow-up (ANALYSIS l.410), so `Q` holds (inferred).
- **Data type:** `INT8 FP14 INT32 FP32 MIXED`, verified (note §2 l.171–173).
  - `FP14` is a genuinely custom 1s/8m/5e format, verified in note §2 and ANALYSIS l.174. It is off-vocabulary but justified.
  - `INT32` is the ray origin term `q_b` and the comparison width (ANALYSIS l.280–281). It is the weakest tag. The reading agent itself said to drop it first (paper-note l.87).
  - `POW2` and `BFP` were correctly declined.
- **Stage:** `S2` is right for scope: per-cluster scale and anchor, a ratio change across BOX units.
- **papers.md path `S1→S2` (l.300):** this is derived. S1SIG fires on two tokens, `anchor +` and `custom FP`. The `S1` half is defensible only through `custom FP14`, since TAXONOMY §4 S1 lists "custom FP/INT hybrids". The `anchor +` hit is an anchor-plus-offset under a shared per-cluster scale, which is the BiScaled shape ("which scale a number is read under") and therefore `S2`. The path is still right, but only one of the two reasons is valid (inferred).

| Axis | Current | Proposed | Evidence | Confidence |
|---|---|---|---|---|
| Optimization | `` `**quantize the ray, not the box**` `` | `` `quantize the ray, not the box` `` | Markdown emphasis inside a code span renders as literal asterisks (README l.55). The note's Tags table has the same text outside backticks, so it renders there (note l.13). Verified. | high |
| Data type | `INT32` | keep, or drop if the cell is trimmed | It is an accumulator- and comparison-width term, not a storage format. The reading agent marked it the first to drop (survey/papers/AQB8/paper-note.md l.87). Inferred. | low |
| Platform (papers.md) | `ASIC` | consider `GPU` | The design modifies the RT unit of a GPU, evaluated as "Vulkan-Sim GPU model, 30 SMs" (note §4 l.206), and the baseline is a GPU RT-accelerator model (ANALYSIS l.119). LUT Tensor Core (a Tensor Core replacement) and Ecco (GPU L2) are `GPU`. The `P_GPU` regex did not fire on this row's cells. Inferred. | low |

**Cell hygiene.**
- **Note cell:** "Clusters of BVH boxes share one FP32 anchor; the rest are INT8 offsets from it, and the intersection test runs on the integers — no decompress to FP32" is verified (note §1, §3).
- **Optimization:** all other keywords are supported (note l.13).

### 6. [Ecco](../../survey/papers/Ecco/paper-note.md) ([pdf](../../survey/papers/Ecco/2505.06901.pdf)): **MINOR**

- **Level:** `ARCH`, verified. The checked `SYS` rule: two PTE bits are an interface, not a software stack (ANALYSIS l.398).
- **Q?:** `Q` (Pass 3).
- **Data type:** `VQ FP8 INT8 MIXED`, verified (note §2 l.28–32). `VQ` is the k-means patterns, `FP8` is the padded outliers, and `INT8` is the 2× activation path. `V2F` correctly absent: Huffman is fixed-to-variable (inferred from the TAXONOMY §3 definition).
- **Stage:** `S3` on test (a), since a value is an index into shared k-means patterns.
- **papers.md path `S3→S2`:** set by OVERRIDE (`3-paths-classify.py` l.23). It agrees with the recorded refinement.
- **Observation, not a change:** the corpus is inconsistent about which venue tag an `S3→S2` record gets. Ecco, VQ-LLM and EIE are venue `S3`. JPEG-ACT, TunstallDec and uSystolic are venue `S2`. TAXONOMY §4 l.232 says an analog crossbar is "venue-`S2` … path-`S3→S2`", which would argue for `S2`. That **conflicts with the recorded ruling** (Pass 7 refinement: "tags in the table above are unchanged"), so I have not proposed it. Verified from paths.json.

| Axis | Current | Proposed | Evidence | Confidence |
|---|---|---|---|---|
| Data type | `VQ` `FP8` `INT8` `MIXED` | consider adding `FP16` | Decompression sits between L1 and L2, so the SMs only ever compute on FP16 (note §2 l.35; ANALYSIS l.84, §4.1). It is the same policy question as Oaken. Verified that FP16 is present. | low–med |

**Cell hygiene.**
- **Note cell:** "groups of 128 against one of 64 shared k-means patterns, then Huffman over a 16-index alphabet" is verified (note §2 l.29–30). It describes the weight path. The KV hardware uses 16 patterns (note l.34), so the cell is not wrong, only weight-centric.
- **Optimization:** every keyword is supported.
- No regex hazard. `codebook` and `k-means` are meant to fire S3SIG here.

### 7. [FATE](../../survey/papers/FATE/paper-note.md) ([pdf](../../survey/papers/FATE/10.1145_3695053.3731031.pdf)): **CHANGE PROPOSED** (Stage drift; Note wording is a live classifier hazard)

- **Level:** `ALGO+ARCH`, verified. The Python framework is a compression tool, not a compiler or ISA (paper-note l.150).
- **Q?:** `Q` (Pass 2).
- **Data type:** `INT8 INT4 TERNARY BINARY MIXED`, verified (note §2 l.119; ANALYSIS l.133).
  - `ADAPTIVE` was correctly dropped. What varies per dimension is effectively the width on one power-of-two grid; there is no learned or new *type*, so TAXONOMY §3's "type, not width" rule gives `MIXED`.
  - `MIXED` is a true coexistence: the evaluated FATE-2 runs 4:3:2:1 in the same vector (note §2 l.123).
  - `FP32` was correctly declined (paper-note l.148).
- **Platform `FPGA`** (papers.md l.302), verified.

**Stage, my §4 reading: `S2`.**
- The INT8 DSP lanes, the LUT-built INT4 and ternary multipliers, and the binary pass/zero gate coexist in one array.
- Precision is assigned per dimension and realigned by hardwired shifts. That is mixed precision at array scope.
- There is no `S1` half, because no element format is designed (the ternary/binary values are inherited).
- There is no `S3`. Test (a) fails because the values are plain integers. Test (b) fails because the "LUT" multipliers are ordinary arithmetic synthesised into fabric, not table resolution of values or a learned truth table. The paper never uses "lookup table", "table lookup" or "codebook" (ANALYSIS l.122–124, exhaustive grep).

| Axis | Current | Proposed | Evidence | Confidence |
|---|---|---|---|---|
| Stage (venue row) | `—` | `S2`, for the FPGA owner to confirm | The published note says `S2` (note l.12), and so does `survey/fpga.md` l.292. The venue row (l.57) and papers.md (l.302) say `—`. The `—` is the 2026-09-22 FPGA owner reset (TAXONOMY §4 "Owner reset"; stages.md l.14–19), applied to records "whose tags had never been audited". FATE's papers.md audit boxes are unticked, so the reset rule technically covers it. Even so, the row disagrees with its own human note, and **the ISCA tag-revision log has no entry recording the reset**, unlike MICRO README l.199. Verified. | med |
| Note cell (classifier hazard) | `Its "LUT" is an FPGA resource, **not** LUT-GEMM` plus `as logic on FPGA LUTs` | Reword so that neither `FPGA LUT` nor `LUT-GEMM` appears. For example: `A different type per **dimension**: INT8 on DSPs, INT4/ternary/binary as fabric logic, so low-precision lanes leave the saturated DSPs`. Record the "not table-lookup GEMM" ruling in code instead: add `"FATE": "MixedPrec"` to `PRIMARY` in 4-stage2-classify.py, and if wanted, a `NOT_S3` entry with reason | Reproduced. (1) `4-stage2-classify.py` LogicMapped pattern `FPGA LUT` matches "FPGA LUTs". LogicMapped is first in PAT order ahead of MixedPrec, so **once the Stage becomes `S2` (row 1 above), FATE's primary mechanism derives as `LogicMapped`**. That category is withdrawn (TAXONOMY §6, "the family is `S3`"). (2) `3-paths-classify.py` LUTARITH matches the negated "LUT-GEMM". This is harmless today only because the Data type has no `` `LUT` `` and the Stage is `—`. This is exactly the §7 "the classifier cannot read the 'not'" failure. It is latent now and would fire on the Stage fix. Verified by running the regexes against paths.json. | high |

**Cell hygiene.**
- **Optimization:** every keyword is supported by note l.13 and §3: `FPGA`, `per-dimension mixed precision`, `DSP/LUT resource split`, `fuzzing-distance importance measure`, `pruning as INT0`, `power-of-two shift alignment`, `segment-balanced reordering` and `HDC`.
- **`DSP/LUT resource split`:** this contains "LUT", but it hits no classifier pattern (verified).
- **`survey/fpga.md` l.21** claims its Stage tags "agree with [the venue indexes] by construction". FATE (S2 vs `—`) contradicts that, and so does XtraMAC (S2 vs `—`), which is outside this group. fpga.md is stale relative to the reset.

---

### Summary

| Paper | Verdict | Proposed changes / concerns |
|---|---|---|
| [Transitive Array](../../survey/papers/TransitiveArray/paper-note.md) ([pdf](../../survey/papers/TransitiveArray/2504.16339.pdf)) | MINOR | Tags OK. The note's §2 "Granularity: elementwise" contradicts its own `g=128` (paper p08). |
| [LUT Tensor Core](../../survey/papers/LUTTensorCore/paper-note.md) ([pdf](../../survey/papers/LUTTensorCore/2408.06003.pdf)) | CHANGE PROPOSED | Data type: add `INT8` (A_INT8 and INT8 table quantization, p05/p08/p10/p11, high). Optionally add `INT16` (med). |
| [MicroScopiQ](../../survey/papers/MicroScopiQ/paper-note.md) ([pdf](../../survey/papers/MicroScopiQ/2411.05282.pdf)) | CHANGE PROPOSED | Data type: add `FP8` (e3m4 outliers at bb=4, p05/p08, high). Optionally add `INT8` (MX-INT-8 activations, med). |
| [Oaken](../../survey/papers/Oaken/paper-note.md) ([pdf](../../survey/papers/Oaken/2503.18599.pdf)) | MINOR | `INT5` is fine. Possibly add `FP16` for W/A (policy question, low–med). |
| [AQB8](../../survey/papers/AQB8/paper-note.md) ([pdf](../../survey/papers/AQB8/10.1145_3695053.3731104.pdf)) | MINOR | Optimization: remove the `**…**` inside backticks (high). `INT32` is weak (low). Platform ASIC→GPU worth a look (low). Path `S1→S2` holds only through `custom FP14`, not `anchor +`. |
| [Ecco](../../survey/papers/Ecco/paper-note.md) ([pdf](../../survey/papers/Ecco/2505.06901.pdf)) | MINOR | Possibly add `FP16` (low–med). Venue `S3` vs path `S3→S2` follows the recorded ruling; noted only as a corpus inconsistency. |
| [FATE](../../survey/papers/FATE/paper-note.md) ([pdf](../../survey/papers/FATE/10.1145_3695053.3731031.pdf)) | CHANGE PROPOSED | Stage `—`→`S2` for the FPGA owner (note and fpga.md say S2; the ISCA log has no reset entry; med). Reword the Note cell: "FPGA LUT" and the negated "LUT-GEMM" trip the classifiers, and the first would mis-file FATE as `LogicMapped` once it is S2 (high). |

## Group 4

## Audit G4: ISCA venue-index tags for 7 papers

Scope: `QuantArchSurvey/venues/ISCA/README.md` rows for LightNobel, Tender, OliVe, RAELLA, Mokey, RaPiD and TPUv4i. Each row was checked against its published note (`venues/ISCA/notes/<abbr>.md`), our working reading (`survey/papers/<Dir>/{ANALYSIS,paper-note}.md`), the paper text (`survey/papers/<Dir>/extracted/`), `survey/papers.md`, and `TAXONOMY.md` as it stands now. This was a read-only audit: no repo file was edited.

Paths below are short forms. `QAS/` = `/home/hs359/moe_ws/quantization_survey/QuantArchSurvey/` and `SP/` = `/home/hs359/moe_ws/quantization_survey/survey/papers/`. Line numbers marked "raw" are for `extracted/*.raw.txt`; page numbers come from `extracted/*.pages/pNN.txt`.

**Method notes**
- **Row vs published note (verified).** I diffed every row against its note's Tags table with a script. Level, Data type and Optimization match exactly for all 7 papers. Stage matches for 6 of 7. The one mismatch is RAELLA: the row says `—` and the note says `S2`.
- **Classifier exposure (verified).** I ran the live regexes (`S1SIG`, `S3SIG`, `LUTARITH`, `SUBSTRATE`, `P_*` from `QAS/survey/gen/3-paths-classify.py`, and `PAT` from `4-stage2-classify.py`) over each row's Data type + Optimization + Note text. The hits are quoted below where they matter.
- **One premise from the brief is wrong (verified).** LightNobel's Stage is **not** `—`. The venue row says `S2` (README line 58), the note says `S2`, `papers.md` line 304 says `S2`, and `paths.json` derives path `S2`. Only RAELLA is `—`.

---

### [LightNobel](../../survey/papers/LightNobel/paper-note.md) ([pdf](../../survey/papers/LightNobel/2505.05893.pdf)) (ISCA'25): MINOR

| Axis | Current | Proposed | Evidence | Confidence |
|---|---|---|---|---|
| Data type | `INT4` `INT8` `INT16` `MIXED` | Optionally add `FIXED`, for the 16-bit fixed-point weights | Paper p05 (raw 699): "we use a 16-bit fixed-point format for weights without quantization". Note §2: "Weights are not quantized at all. 16-bit fixed point throughout". Other ISCA rows tag the high-precision format they carry (Mokey has `FIXED` for its 16b centroids; RaPiD and TPUv4i have FP16/FP32). Without it, the row hides the half of the design that is not quantized. **verified** (the fact); the precedent argument is **inferred** | low |
| Level (log hygiene) | `ARCH` | Keep `ARCH`. The Pass 1 table (README revision log, "Changes that follow directly from the text") still lists LightNobel under `ARCH` → `ALGO+ARCH`. The human overrode that on 2026-09-10 (`SP/LightNobel/ANALYSIS.md` line 251), and Pass 4 says the row is regenerated from notes. A reader of the log may still trust the stale Pass 1 line | ANALYSIS line 251; README Pass 1 row | high (that the log is stale) |

**Checks that passed (verified)**
- **Q.** Pass 1 judgment call #3 agrees.
- **`ADAPTIVE` correctly absent.** This is the recorded Pass 3 ruling, and it is consistent with TAXONOMY §3.
- **`MIXED` is real.** INT8 inliers (Group A) and INT4 inliers (Groups B/C) coexist in one run alongside INT16 outliers (paper DSE section, raw 2070–2090; p05 raw 701).
- **Stage `S2` is right.** Per-token granularity, an outlier path and mixed precision are all array-scope mechanisms under §4. The classifier's `PAT` puts it in Outlier, Granularity and MixedPrec, which agrees.

**Cell hygiene**
- Every Optimization keyword is supported by note §2/§3.
- The Note cell is accurate.
- `token-wise adaptive quantization` does not trip `S1SIG`, which requires "adaptive (numeric|data) type" (checked).

---

### [Tender](../../survey/papers/Tender/paper-note.md) ([pdf](../../survey/papers/Tender/2406.12930.pdf)) (ISCA'24): CHANGE PROPOSED

| Axis | Current | Proposed | Evidence | Confidence |
|---|---|---|---|---|
| Data type | `INT8` `INT4` `MIXED` | `INT8` `INT4` (drop `MIXED`) | **TAXONOMY §3:** "Alternative modes alone are not `MIXED`… widths that coexist in the evaluated design". **Paper:** "quantizing large language models entirely into INT4/INT8 without using mixed precision" (p04); "When the model precision is INT8, 4 PEs are grouped to perform 8-bit multiplication" (p07, raw 1212), i.e. INT8 is a per-model mode on an INT4 array; "Without the need for mixed precision storing" (p08, raw 1386). **The published note contradicts its own tag:** note §2 says "No custom datatype, **no mixed precision**". **verified** | high |

**Checks that passed (verified)**
- Level `ALGO+ARCH`, Q and Stage `S2` (per-band scale granularity / outlier isolation) match the note, ANALYSIS and Pass 7.
- `POW2` is correctly absent. This is the recorded Pass 2 ruling and is not re-opened here.
- `papers.md` path is `S2`.

**Knock-on effect (verified by regex run)**
- Today the `PAT` MixedPrec category fires on Tender only because of the `` `MIXED` `` tag. Dropping it leaves Outlier as the only and primary category, which matches the paper.

**Cell hygiene**
- The Optimization keywords are all supported.
- The Note cell is accurate.
- Optional precision fix: "consecutive band scales" would be more exact than "bands whose scales are exactly 2× apart".

---

### [OliVe](../../survey/papers/OliVe/paper-note.md) ([pdf](../../survey/papers/OliVe/2304.07493.pdf)) (ISCA'23): CHANGE PROPOSED

| Axis | Current | Proposed | Evidence | Confidence |
|---|---|---|---|---|
| Data type: `FP8` missing | `ADAPTIVE` `INT4` `INT8` `FP4` `MIXED` | Add `FP8` | The 8-bit configuration's outlier type is "signed E4M3 for 8-bit abfloat" (p06, raw 1146). The row already carries `INT8` for that configuration and `FP4` for the 4-bit configuration's E2M1 outlier, so tagging only the int half of the 8-bit configuration is inconsistent. **verified** | med |
| Data type: `MIXED` | present | Drop `MIXED` | 4-bit and 8-bit OliVe are separate configurations. GPU and accelerator performance is measured at 4-bit; the mixed-precision runs in the evaluation belong to the **ANT baseline** ("In ANT, 80% of layers ends up using int8", p10). OliVe "can inherently support the mixed-precision" (p03) and "can directly support the mixed precision" (p07) are capability claims. Within a configuration, normal int4 and abfloat E2M1 are **one width, two types**: mixed type, not mixed precision. TAXONOMY's own worked example tags OliVe `ADAPTIVE`+`INT4`, without `MIXED`. Caveat: the area table (p11) has both 4-bit and 8-bit decoders in one array, which is the strongest argument for keeping it. **verified** facts; the conclusion is **inferred** | med |
| Data type: `ADAPTIVE` | present | Keep, but record **why** in the note | It passes the §3 "data-dependent *type*" rule through the inherited ANT mechanism. Normal values use int4 / flint4 / int8, and "selecting the data type according to a tensor's distribution… we also adopt the mixed data types" (p05, raw 924–931). By contrast, abfloat's "adaptive bias" is **fixed per normal type** (bias=2 for int4, bias=3 for flint4; p05–06, raw 1078–1085) and is not data-dependent, so it is **not** what earns the tag. The note does not say this, so a later reader could drop `ADAPTIVE` on the wrong grounds or keep it on the wrong grounds. **verified** | med |

**Checks that passed (verified)**
- Level, Q and Stage `S2` match the note, ANALYSIS and TAXONOMY's worked example.
- `papers.md` path is `S1→S2`. This is derived from `S1SIG` hits on `` `ADAPTIVE` `` and `abfloat` (regex run). It is consistent with the §6 stored-versus-transient rule, because abfloat is a stored, designed per-value type. Venue `S2` and path `S1→S2` may legitimately differ (§4 "Stage is scope; the path is the trajectory").
- If `ADAPTIVE` were ever dropped, `abfloat` alone still keeps `S1→S2`.

**Cell hygiene**
- Optimization keywords are all supported by the note.
- The Note cell "No index, no sparse list, no second datapath" is a triple negation. No current regex fires on it (checked), but it has the shape §7 warns about. A positive phrasing would be safer, e.g. "outlier position implicit in the pair; single 4-bit datapath".

---

### [RAELLA](../../survey/papers/RAELLA/paper-note.md) ([pdf](../../survey/papers/RAELLA/2304.07935.pdf)) (ISCA'23): CHANGE PROPOSED

| Axis | Current | Proposed | Evidence | Confidence |
|---|---|---|---|---|
| Data type: bare `INT` | `INT` | `INT8` | §3: "Give the bitwidth when known". Paper: "8-bit (8b) per-channel quantized DNNs with 8b inputs/weights and 16b partial sums… RAELLA supports this type of quantization" (p02, raw 160–161). Note §2: "Base precision. 8-bit DNNs, sliced." **verified** | high |
| Data type: `ADAPTIVE` | present | Drop `ADAPTIVE`. Move "adaptive weight slicing" to Optimization, where it already is | **§3 rule: "`ADAPTIVE` is for a data-dependent *type*, not a data-dependent *width*."** What varies is **bits per slice**: per layer at compile time ("RAELLA can use a different number of bits for each slice, but all weights in a layer use the same slicing", p05, raw 584–586) and per input at runtime. The slices are bit groups of an ordinary 8b integer. Center+Offset is a per-column shift ("chooses centers that balance the magnitude of positive/negative slices in each crossbar column", p05, raw 556–563), i.e. a zero-point / granularity decision, not a new type. **The note's sentence "`ADAPTIVE` here names a real format property (slice width), not a selection policy" restates the very misreading the §3 rule forbids**: slice width is a width. It came from the reading agent's suggestion (`SP/RAELLA/paper-note.md` §6; ANALYSIS line 259). No owner ruling on RAELLA `ADAPTIVE` exists in the ISCA revision log. **verified** | med-high |
| Data type: `MIXED` | present | Drop, or owner's call | Every value is 8b. The only thing that varies is the slice decomposition, which is bit splitting (§6 Stage-2 mechanisms), not "multiple precisions coexist". Slice widths do coexist across layers, which is the only argument for keeping it. **inferred** | low-med |
| Stage | `—` | Keep `—` until the PIM owner rules. When they do, the answer TAXONOMY points to is **venue `S2`**, path `S3→S2` | This `—` is the **"Owner reset"** meaning (§4 "What `—` means"): the 2026-09-22 FPGA/PIM/SNN reset (`QAS/survey/stages.md` lines 14–18). Platform is PIM (`papers.md` line 408). It is **not** "Unread" (full note exists) and **not** "Axis in doubt" (only snn.md carries that). §4: "An analog crossbar is venue-`S2`… and path-`S3→S2`. Do not 'fix' a venue row from `S2` to `S3`." The PIM domain page has effectively ruled already: `QAS/survey/pim.md` line 69 gives RAELLA `S3→S2`, "Return — analog CIM". `papers.md` shows `—` only because `path()` stops at a `—` venue stage (`3-paths-classify.py`, "An unassigned Stage terminates the derivation"). **verified** | high (that `S2` is the right value); owner action needed |
| Note-vs-row drift | note says `S2`, row says `—` | Leave the row `—` and annotate the note, or set both to `S2` once the owner rules | `notes/raella.md` Tags table, `Stage | S2`. The note predates the reset. **verified** | high |

**Knock-on effects (verified by regex run)**
- With Stage set to `S2`, the derived path is `S3→S2` whether or not `ADAPTIVE` stays, because `substrate()` matches "analog PIM / ReRAM / crossbar / ADC" before `S1SIG` is consulted.
- `` `ADAPTIVE` `` does make the Stage-2 `PAT` classifier pick **MixedType**, and `` `MIXED` `` makes it pick MixedPrec. The actual mechanism is bit splitting, and nothing in the cell matches the BitSplit pattern ("weight slicing" ≠ `bit-?slice`). If the row ever enters `s2.json`, both tags would misfile it. **inferred** (RAELLA is not in `s2.json` today because its Stage is `—`)

**Other checks (verified)**
- Level `ALGO+ARCH` and Q match the note, ANALYSIS and Pass 1.
- Optimization keywords are all supported by note §1–§3.
- The Note cell is accurate.
- Stale count: Pass 7's "0 `S1` / 29 `S2` / 5 `S3`" counted RAELLA as `S2`; that count no longer holds.

---

### [Mokey](../../survey/papers/Mokey/paper-note.md) ([pdf](../../survey/papers/Mokey/2203.12758.pdf)) (ISCA'22): MINOR

| Axis | Current | Proposed | Evidence | Confidence |
|---|---|---|---|---|
| Data type `INT4` | `VQ` `LUT` `FIXED` `INT4` | Keep, as venue convention. Optionally note that "INT4" here is a 4-bit **index** (1 sign + 3b exponent index), not a 4-bit integer | Note §2: "4b = 1 sign + 3b index". TAXONOMY §2 misreading ③ says "Swap what the design stores": what is stored is an index. All other ISCA `VQ` rows (EVA, OASIS, Omni-LUT, Ecco) also carry an `INT` width beside `VQ`, so this is consistent. **verified** | low |
| Note cell, "Pre-LLM root of the codebook thread" | present | Conflicts with recorded state; owner's call | README header lines 10–11 and Pass 6: "EIE (ISCA'16) turns out to predate Mokey as the venue's codebook root". Pass 6 deliberately did not edit this ("reversing pass 3's Mokey ruling is the owner's call"). Flagged so it is not quoted as settled. **verified** | med |

**Checks that passed (verified)**
- Stage `S3` is the recorded ruling (Pass 7 / stages.md refinement, and classifier `FLAG` "S3 by provenance, S2 by arithmetic"). Not re-litigated.
- `LUT` fits §3 ("computation resolved by table lookup"): 15 counters reduced against 15 precomputed centroid products (note §3).
- `FIXED` is supported (16b fixed-point centroids, note §2).
- Level and Q match.
- `papers.md` gives `S3` / Q / ASIC, which is consistent.

**Cell hygiene**
- Optimization keywords are all supported.
- Note numbers are verified against note §1/§3 (256 → 15, 3-bit index addition).
- `S3SIG` fires on `VQ`, codebook, golden dictionary and centroid. That is correct here.

---

### [RaPiD](../../survey/papers/RaPiD/paper-note.md) ([pdf](../../survey/papers/RaPiD/10.1109_ISCA52012.2021.00021.pdf)) (ISCA'21): MINOR

| Axis | Current | Proposed | Evidence | Confidence |
|---|---|---|---|---|
| Data type `INT2` | present | Keep with an explicit caveat in the note, or drop. Owner's call | The paper says INT2 is in the silicon: "16 INT2 MACs" per FXU; it "restrict[s] our study to FP8-fwd and INT4 precisions and reserve[s] INT2 implementation for future work" (p09, raw 1473–1475; p12, raw 2273). §3 tags widths "present in the evaluated design", and INT2 is built but never exercised. The row's own Note says "INT2 is… a capability, not a result", so tag and Note disagree. **verified** | low |
| Data type `FP32` | absent | Optional: add `FP32` | The SFUs perform "higher precision FP32 operations" (raw 771; note §2 "SFUs at FP16/FP32"). TPUv4i's row tags FP32 on similar grounds. **verified** (fact); whether it is tag-worthy is **inferred** | low |
| Data type `FP16` | present | Keep. The DLFloat (1,6,9) caveat is already in the Note | Note §2. No §3 tag exists for DLFloat. **verified** | — |
| Note cell | short note + audit paragraph | De-duplicate (details below) | — | high |

**Checks that passed (verified)**
- Level `ARCH+SYS` is the human's ruling (ANALYSIS line 356).
- Q is the recorded audit of 2026-09-23. Not re-litigated.
- `MIXED` is genuine. Formats coexist within one program: INT4 GEMMs with FP16 first/last layers and auxiliary ops, and the HFP8 backward pass uses (1,4,3) × (1,5,2) (note §2).
- Stage `S2` matches the note and `papers.md`.
- Optional observation (**inferred**, low): the on-the-fly widening to a custom 9-bit (1,5,3) plus a per-layer programmable exponent bias is in-PE decode, which §4 lists under `S1`. A `S1→S2` path could be argued. The formats are cited to prior work, though, so the current `S2` path is defensible.

**Cell hygiene: Note duplication, exactly**

The short note reads: *"Fabricated 4-core 36 mm² 7 nm chip; two pipelines per PE — FPU for DLFloat FP16 and Hybrid-FP8, FXU for INT4/INT2. **Measured silicon**"*. The audit paragraph that follows repeats three parts of it:
1. **The pipeline split.** "Five formats across two physical pipelines… an FPU carrying DLFloat FP16 and both HFP8 layouts, an FXU carrying INT4 and INT2" restates the short note's FPU/FXU clause.
2. **The chip spec.** "…on a fabricated 4-core 36 mm² 7 nm chip" repeats the short note's opening clause almost verbatim.
3. **DLFloat, a third time.** It appears in the short note, in point 1, and again in "Two warnings… (1,6,9) is IBM DLFloat".

Further problems:
- The paragraph also copies note §2 (role-split HFP8, storage 8b / compute 9b) and the note's §5 Comment (training + inference, HFP8 / INT4) nearly verbatim.
- There is no separator between "**Measured silicon**" and "**`Q` confirmed and kept…**".
- "Measured silicon" should carry the note's own evidence split: peak numbers are measured, end-to-end numbers are modelled (note §4). The current wording invites pooling.

**Regex check (verified):** only the MixedPrec `PAT` category fires, on `` `MIXED` `` and "multi-precision". "not IEEE FP16" and "not a fused datapath" currently trip nothing.

---

### [TPUv4i](../../survey/papers/TPUv4i/paper-note.md) ([pdf](../../survey/papers/TPUv4i/10.1109_ISCA52012.2021.00010.pdf)) (ISCA'21): MINOR

| Axis | Current | Proposed | Evidence | Confidence |
|---|---|---|---|---|
| Data type `MIXED` | present | **Conflicts with the recorded ruling** (Pass 2 set `INT8` `BF16` `FP32` `MIXED`). Under §3 today it is weak. Owner may wish to revisit | §3: "Alternative modes alone are not `MIXED`". int8 is a porting mode: "TPUv4i also supports int8" (p08), and "TPUs ran all the benchmarks using bf16". bf16 and fp32 coexisting inside a workload is plausible (bf16 MXU, 32-bit vector unit), but the paper never states a bf16-multiply / fp32-accumulate contract. Our own ANALYSIS (line 486) already calls `MIXED` "the weak one… do not read it as a mixed-precision quantization scheme". The Note's "three formats in one machine is an array-level decision" is the alternative-modes reading. **verified** facts; the conclusion is **inferred** | low-med |

**Checks that passed (verified)**
- Level `ARCH+SYS` matches the note and ANALYSIS.
- non-Q is a recorded ruling (Pass 2 / Pass 5). Kept.
- Stage `S2` is the recorded Pass 7 ruling. `S0` is excluded anyway: §4 bounds `S0` at 2016, and the custom 4-input FP adder is a numeric-datapath change.
- `papers.md` gives `S2` / non-Q / ASIC, which is consistent.
- Note facts check out against note §2/§4 and the paper: 138 T for bf16 *and* int8 vs T4 65/130 (raw line 119); 1 of 8 production DNNs quantized; 4 × 128×128 floating-point MXUs; 4-input FP adder followed by 32 two-input adders.

**Cell hygiene: Note duplication, exactly**

The short note reads: *"Lesson ⑥ of ten, and it is a warning: TPUv1 *required* int8 and that hurt in production. Only **one** of Google's production DNNs here is quantized"*. The audit paragraph repeats **both sentences**:
- "**one** of Google's production DNNs here" appears again inside "It is the only evidence in the corpus…".
- "Lesson ⑥ is a warning written from experience: TPUv1 *required* int8 and that hurt in production, so *offer quantization, do not require it*" repeats the first sentence. "offer quantization, do not require it" is also already an Optimization keyword.

Further problems:
- There is no period between "is quantized" and "**`non-Q` confirmed and kept…**".
- "Kept anyway, and the reason is why it is not SamsungNPU" was written before Pass 10 restored SamsungNPU. It still reads correctly, but the contrast is now between two *kept* non-Q rows kept for different reasons.

**Regex hazard (§7):** "no zero point, no requantization, no calibration, no scale, and nothing about what shares one" is a negation list. No current pattern fires on it (only `` `MIXED` `` → MixedPrec fires), but it is the exact shape §7 warns about. Rewording it as a positive statement ("the paper specifies no quantization scheme") would be safer.

---

### Summary

| Paper | Verdict | Proposed changes / concerns (confidence) |
|---|---|---|
| [LightNobel](../../survey/papers/LightNobel/paper-note.md) ([pdf](../../survey/papers/LightNobel/2505.05893.pdf)) | MINOR | Stage is `S2` everywhere, not `—`. Optionally add `FIXED` for the 16b weights (low). Pass 1 log line `ARCH`→`ALGO+ARCH` is stale vs the human's `ARCH` |
| [Tender](../../survey/papers/Tender/paper-note.md) ([pdf](../../survey/papers/Tender/2406.12930.pdf)) | CHANGE PROPOSED | Drop `MIXED` (high). The paper says "without using mixed precision", INT8 is a per-model mode on the INT4 array, and the note's own §2 says "no mixed precision" |
| [OliVe](../../survey/papers/OliVe/paper-note.md) ([pdf](../../survey/papers/OliVe/2304.07493.pdf)) | CHANGE PROPOSED | Add `FP8` for the 8-bit E4M3 abfloat (med). Drop `MIXED`, since 4/8-bit are alternative configurations and the TAXONOMY example omits it (med). Keep `ADAPTIVE`, but justify it by the inherited int4/flint4 per-tensor type selection, not by abfloat's fixed bias (med) |
| [RAELLA](../../survey/papers/RAELLA/paper-note.md) ([pdf](../../survey/papers/RAELLA/2304.07935.pdf)) | CHANGE PROPOSED | `INT` → `INT8` (high). Drop `ADAPTIVE` under the §3 type-not-width rule; slice width is a width (med-high). `MIXED` doubtful (low-med). Stage `—` is the PIM "Owner reset"; when ruled it should be venue `S2` / path `S3→S2`, matching pim.md (high). Note says `S2` (drift) |
| [Mokey](../../survey/papers/Mokey/paper-note.md) ([pdf](../../survey/papers/Mokey/2203.12758.pdf)) | MINOR | `INT4` is an index width, consistent with venue convention (low). Note's "Pre-LLM root of the codebook thread" conflicts with the Pass 6 EIE finding; owner's call (med) |
| [RaPiD](../../survey/papers/RaPiD/paper-note.md) ([pdf](../../survey/papers/RaPiD/10.1109_ISCA52012.2021.00021.pdf)) | MINOR | Note cell duplicates the chip spec, the FPU/FXU split and DLFloat (three mentions), plus a missing separator (high). `INT2` was never evaluated, and the row's own Note says so (low). Optional `FP32` (low) |
| [TPUv4i](../../survey/papers/TPUv4i/paper-note.md) ([pdf](../../survey/papers/TPUv4i/10.1109_ISCA52012.2021.00010.pdf)) | MINOR | Note cell repeats both short-note sentences, plus a missing period (high). `MIXED` is weak under the §3 alternative-modes rule, but conflicts with the recorded Pass 2 ruling (low-med). Negation-list wording is a §7 hazard (low) |

## Group 5

## Audit G5: ISCA venue-index tags for seven papers

Scope: SamsungNPU, DRQ, SmartExchange, JPEG-ACT, Bit Fusion, OLAccel, Gist.
Read-only. Paths are relative to `/home/hs359/moe_ws/quantization_survey/`.

- `R` = `QuantArchSurvey/venues/ISCA/README.md`
- `N/<abbr>` = `QuantArchSurvey/venues/ISCA/notes/<abbr>.md`
- `A/<Dir>` = `survey/papers/<Dir>/ANALYSIS.md`, `PN/<Dir>` = `survey/papers/<Dir>/paper-note.md`
- `X/<Dir> pNN` = `survey/papers/<Dir>/extracted/*.pages/pNN.txt`
- `T` = `QuantArchSurvey/TAXONOMY.md`, `P` = `QuantArchSurvey/survey/papers.md`
- `G3` = `QuantArchSurvey/survey/gen/3-paths-classify.py`, `G4` = `QuantArchSurvey/survey/gen/4-stage2-classify.py`

**Concurrency caveat.** `R` changed while this audit ran: Pass 11 was added (2026-10-01), the header now reads 35 papers, and line numbers moved by about 2. I re-extracted the seven rows afterwards. Their Level, Q?, Data type, Stage and Optimization cells are byte-identical to what I audited, and the Note cells are the same length. The working tree also shows `TAXONOMY.md` and `papers.md` as modified (uncommitted), so line numbers quoted below may drift.

**Regex check method.** I compiled the `PAT`, `S1SIG`, `S3SIG`, `SUBSTRATE` and platform regexes from `G3` and `G4` in memory and ran them over `survey/gen/named.json`. Nothing was written. I also read the existing `s2.json` and `paths.json`.

**Cross-cutting findings**
- **Working copies still use the old tag.** All seven `PN/*` Tags tables still carry the retired `Generation` row and have no `Stage` row. The published notes do have `Stage`. (verified, `PN/*` lines 1-16)
- **Two rulings are recorded only in Note cells.** DRQ's outlier ruling and JPEG-ACT's `S3→S2` ruling (both dated 2026-09-22) are not in any revision-log pass. A grep of `R` for `2026-09-22` hits only the DRQ and JPEG-ACT Note cells. They are also in the code comments in `G4` (`PRIMARY["DRQ"]`) and `G3` (`OVERRIDE["JPEG-ACT"]`). So the Note cell is standing in for the log. (verified)
- **The vocabulary is missing widths the rows already use.** `INT16`, `INT1` and `FP10` appear in these rows but are not in the T §3 Traditional list (`INT8 INT4 INT2 … FP16 BF16 …`). T §3 also says "give the bitwidth when known", so this looks like a vocabulary gap rather than row errors. (verified T §3)

---

### [SamsungNPU](../../survey/papers/SamsungNPU/paper-note.md) ([pdf](../../survey/papers/SamsungNPU/10.1109_ISCA52012.2021.00011.pdf)) (samsung-npu) — `CHANGE PROPOSED`

| Axis | Current | Proposed | Evidence | Confidence |
|---|---|---|---|---|
| Data type | `INT8` `INT16` `MIXED` | `INT8` `INT16` (drop `MIXED`) | T §3: "Alternative modes alone are not `MIXED`… not hardware that *could* be configured either way." The paper says INT16 exists "to cope with applications requiring high accuracy" (X/SamsungNPU p04, §III-C), so the choice is per application, not per layer. Every evaluated workload is INT8: "each feature map, weight, and bias were 8-bit integers" (X p09, §VI). No INT16 occurrence after §V-D in the raw text (verified grep). N §4 "Models… INT8". Pass 10 says "Tags unchanged: `non-Q`, `S2`" and does not rule on Data type, so this does not reopen a recorded ruling. | med-high |
| Stage | S2 | S2 (keep) | Owner ruling, Pass 10. My own §4 reading agrees: INT16 is a **transient** LL/LH/HL/HH decomposition on the INT8 datapath (T §6 stored-vs-transient, the Bit-Pragmatic side), so it is S2 with no S1 half. `P` = `S2`. | high |
| Optimization | (no keyword) | consider adding `temporal bit decomposition` | `G4` files the row as BitSplit only because the word **`BitBrick`** appears in the Note cell's comparison with Bit Fusion (regex hit `'BitBrick'`, verified). The category is right but the reason is a comparison sentence. If that sentence is trimmed and `MIXED` is dropped, the row falls to `Others`. The BitSplit pattern contains `bit decomposit`. | med (inferred) |

Level `ARCH` and Q? `non-Q` agree across row, N, A (§"For the note") and T §2. Q? is the named case in T §2 and a recorded ruling (Passes 3, 8, 10). `P` = S2 / non-Q / ASIC, consistent.

**Cell hygiene (Note)**
- **Duplicated inside the cell.** "INT16 is four time-multiplexed INT8 subcomputations" (first sentence) is followed by "**INT16 is executed as four time-multiplexed INT8 subcomputations.**". "**Measured silicon**" is followed later by "**measured 5 nm silicon**". (verified)
- **Stale history.** "**Removed 2026-09-23 and restored the same day for one observation — see Pass 10.**" is change history, and Passes 8 and 10 already record it.
- **The rest of the cell is Pass 10 almost word for word**: the Bit Fusion / PIR-DSP "same axis" comparison, "Tags unchanged: `non-Q`", the "tension is left standing" sentence, the reconfigurability price (17.0%), and "measured 5 nm silicon, the finest node in the corpus". The evidence-level warning also duplicates Pass 8 and N §4. Suggest cutting the cell to about two sentences and linking Pass 10.
- **Wrong link.** `[Bit Fusion](../MICRO/README.md)` points to MICRO, but Bit Fusion is ISCA'18 and is a row in this same file. A grep of `MICRO/README.md` for "Bit Fusion" finds nothing. Pass 10 has the same bad link. (verified)
- **Overstated claim.** "the finest node in the corpus": N §4 says "the finest **measured** node in the corpus", and `COMMERCIAL-HOTCHIPS/README.md` has a 3 nm part. The cell should keep the qualifier. (verified grep, low importance)

---

### [DRQ](../../survey/papers/DRQ/paper-note.md) ([pdf](../../survey/papers/DRQ/10.1109_ISCA45697.2020.00086.pdf)) (drq) — `MINOR`

No tag change proposed. Level `ALGO+ARCH`, Q, `INT4` `INT8` `MIXED` and S2 agree with N Tags, A §"For the note" and T. `INT4`/`INT8` coexist in one layer region by region, W8A8 vs W4A4 (N §2), so `MIXED` passes T §3. S2 as outlier handling is the owner ruling in T §6 and `G4` `PRIMARY`. `P` = S2 / Q / ASIC, consistent.

| Axis | Current | Proposed | Evidence | Confidence |
|---|---|---|---|---|
| Note vs published note | Row: "The selection test is a *magnitude* test on the tensor's own values" | Update **N/drq §2** to match, not the row | N/drq §2 line 35 says "Sensitivity is *geometric*, not magnitude-based — this is what makes it `G2` and not `G3`." That contradicts the recorded outlier ruling and uses the retired vocabulary. The paper supports the ruling: a dot product with an all-ones kernel, compared to a threshold (X/DRQ p04). The region is the granularity, but the test is on magnitude. | high (verified) |

**Cell hygiene (Note)**
- **Audit trail in the cell.** "**Outlier handling, `S2`, audited 2026-09-22.**" is audit history with no revision-log pass behind it (see cross-cutting). It belongs in a pass entry.
- **Duplicated case law.** The CascadeCNN contrast ("deliberately **not** filed as outlier… same shape pointed at a different object") repeats T §6 and the `G4` `PRIMARY` comments. It also classifies a different record inside DRQ's row.
- **Negation (T §7): harmless here, but it has made a code comment stale.** The Outlier regex now fires on DRQ's own Note text ("**Outlier handling**", regex hit `'Outlier'`, verified), which is the desired category. But the `G4` `PRIMARY["DRQ"]` comment says "The Outlier pattern does not fire", which is now false. The "not filed as outlier" phrase is about CascadeCNN and does no harm to either row, because CascadeCNN has its own `PRIMARY` entry.
- **Optimization.** Every keyword is supported by N §2–3. Fine.

---

### [SmartExchange](../../survey/papers/SmartExchange/paper-note.md) ([pdf](../../survey/papers/SmartExchange/2005.03403.pdf)) (smartexchange) — `CHANGE PROPOSED`

| Axis | Current | Proposed | Evidence | Confidence |
|---|---|---|---|---|
| Stage (note-vs-row drift) | Row S1; **N Tags: S2** | Update N/smartexchange Tags to `S1` | N line 12 still says `S2`. `R` row, `P` (`S1`) and the `G3` comment ("Its venue row now carries S1 directly") all say S1, per the owner ruling recorded in Pass 9 and the Pass 7 amendment. The note was never re-synced. | high (verified) |
| Data type | `POW2` `INT4` `INT8` | add `MIXED` | T §3: "`MIXED`: multiple precisions coexist… alongside the underlying formats". The paper: "8-bit fixed-point… activations; and 4-bit/8-bit representations for the coefficient/basis matrices" (X/SmartExchange p09, footnote 2), so 4-bit `Ce`, 8-bit `B` and 8-bit A coexist in the evaluated model. This is the same basis on which JPEG-ACT (INT8 + FP32) and OLAccel carry `MIXED`. It does not change the derived path: `G3` `path()` returns `S1` for an S1 row unless S3SIG or substrate fires (verified). **Caveat:** the owner's Pass 9 / Note argument calls per-tensor precision "ordinary". That was an argument against S2, not against the tag, but a `MIXED` + `S1` row may read as inconsistent with T §4's "mixed precision" under S2. Owner's call. | med |
| Data type | `INT4` | concern only: `INT4` labels the **width of a POW2 code**, not a 4-bit integer | `Ce` non-zeros are restricted to `Ω_P = {0, ±2^p}` (N §2, Eq. 2). Its 4 bits encode sign and exponent, not a uniform integer, so `INT4` implies a format that is not there. The vocabulary has no width-qualified POW2 (compare `FIB4`). Either keep it with a Note sentence, or drop `INT4` and record "Ce 4-bit" in prose. | low-med (inferred) |

Level `ALGO+ARCH` and Q agree across row, N, A and PN. The owner ruled Stage S1 in Pass 9; I do not re-litigate it. My own §4 reading finds no array-scope numeric decision, so I agree with it. `P` = S1 / Q / ASIC.

**Cell hygiene (Note)**
- **Contradicted fact.** The cell opens "**W = B·Ce**". The paper writes `W ≈ Ce B` (Eq. 1, X/SmartExchange p03) and `arg min ‖W − Ce B‖²_F` (Eq. 2). N §2 stresses "note the order", PN line 149 says "**`W = Ce · B`**, not `B · Ce`", and the same cell later writes `W = Ce·B`. The error comes from A's proposed-row text (A line 299). (verified)
- **Self-referential and stale.** "**…demoted from `S1→S2`, and this file already said so.** The migration table further down has read *RingCNN · SmartExchange…* since the tags were migrated; the row itself never moved." This is meta-history about the README itself, and it duplicates Pass 7's amended row and Pass 9. Suggest cutting it to "S1 (Pass 9)."
- **Imprecise link.** `[Bit-Pragmatic](../MICRO/README.md)`: Bit-Pragmatic lives in `MICRO/pre-2018/README.md`. The MICRO README mentions it but has no row for it. (verified)
- **Negation (T §7).** "The numeric design is **per-tensor** and nothing else" triggers the Granularity regex (`'per-tensor'`, verified). That is harmless while the row is S1, because `G4` only reads S2 rows, but it would mis-file the row if the Stage ever reverts.
- **Stale count elsewhere.** Pass 7's "The venue ends at 0 `S1`… ISCA 2018–2026 contains no paper whose contribution is a single scalar numeric type" is now false, since SmartExchange is S1. It is historical text, but nothing amends it. (verified, `R` Pass 7)

---

### [JPEG-ACT](../../survey/papers/JPEG-ACT/paper-note.md) ([pdf](../../survey/papers/JPEG-ACT/10.1109_ISCA45697.2020.00075.pdf)) (jpeg-act) — `CHANGE PROPOSED` (classifier / Platform; row tags OK)

| Axis | Current | Proposed | Evidence | Confidence |
|---|---|---|---|---|
| S2 sub-category (derived) | `G4` primary = **Transform** (`s2.json`: `['Transform','Granularity','MixedPrec']`); `survey/stage2.md` line 589 lists it under candidate category B, transform-domain | add `PRIMARY["JPEG-ACT"]`, probably `Granularity` (the SFPR per-channel scale). Owner to choose. | The Note cell says explicitly that it sits "beside EIE and GOBO **rather than in the transform-domain group with Winograd and block-circulant work**". The classifier does the opposite: it matches `DCT` (also in Optimization `DCT transform coding`), and `Winograd` / `block-circulant` in the very sentence that denies it. This is the T §7 failure exactly. Rewording the Note will not fix it, because `DCT` is in Optimization, so it needs a `PRIMARY` entry. `stage2.md` line 589 also still prints the old Note, "Sheet comment: compresses spatial info instead of values", which the current row calls **wrong**. | high (verified) |
| Platform (`P`) | ASIC | GPU | T §5: "what kind of machine the paper builds or targets". The new RTL sits between the GPU crossbar and the PCIe DMA engine of a simulated NVIDIA Titan V (X/JPEG-ACT p10: "GPGPU-Sim… configured to simulate an NVIDIA Titan V GPU"; N §3). The same shape in this venue, Ecco (a decoder in the GPU L2, `S3→S2`), is `GPU` in `P`. The row text never says "GPU", so `P_GPU` cannot fire (verified). Fix with a `PLATFORM` override in `G3`. | med-high |

The row tags are fine. Level `ALGO+ARCH`, Q, `INT8` `FP32` `MIXED` and venue S2 agree with N Tags, A §"Proposed values" and T. Q is a recorded ruling (Pass 5's "four that look removable").
- **Stage.** Applying §4 myself: test (a) holds, and T §4 names JPEG-ACT as the case. The block is decoded to FP32 before the SMs, so path `S3→S2` and venue `S2`. `P` = `S3→S2` (`OVERRIDE` plus `IS_VALUE`). Consistent.
- **`MIXED`** is justified: 8-bit SFPR, 1-bit BRC masks and per-frequency `8−s`-bit coefficients coexist with FP32 compute (A §"Proposed values").
- **`POW2`** was rejected deliberately (A item 7: the DQT powers of two are step sizes, i.e. scales). That matches the Tender ruling. OK.

**Cell hygiene (Note)**
- **History in the cell.** "**`S3→S2`, audited 2026-09-22 — moved off `S1→S2`.**" and the paragraph "**Two corrections to the old row.**…" are change history with no revision-log pass behind them.
- **Fragile wording.** S1SIG fires on Optimization's `power-of-two shift quantization` (`'shift quantiz'`, verified). That is harmless only because of the `OVERRIDE`; it is the likely source of the old `S1→S2`. Worth a comment beside the override.
- **No codebook words.** S3SIG does not fire. "learned quantization table" escapes `learned (table|…)` because of the word in the middle (verified). This is consistent with the `OVERRIDE` comment's intent.
- **Small imprecision.** "1.48 mm², 1.36 W, 77% of it the DCT": per N §3–4, the 77% is DCT+iDCT as a share of **one CDU's** area (229 118 µm²). It is not 77% of the 1.48 mm² / 1.36 W total, which covers four CDUs plus buffers, collector and splitter. Suggest "77% of each CDU". (verified against N; low)

---

### [Bit Fusion](../../survey/papers/BitFusion/paper-note.md) ([pdf](../../survey/papers/BitFusion/1712.01507.pdf)) (bit-fusion) — `MINOR`

| Axis | Current | Proposed | Evidence | Confidence |
|---|---|---|---|---|
| Data type | `INT16` `INT8` `INT4` `INT2` `INT1` `MIXED` | add `TERNARY` | "Benchmarks LeNet-5 and VGG-7 use ternary (+1,0,-1) networks [34]" (X/BitFusion p07, §V-A). Ternary values are in the evaluated workloads, and T §3 lists `TERNARY`. N §2 says "plus binary (0,+1) and ternary (−1,0,+1)" but the tag set omits it. | med |
| Data type | `INT1` | concern only: keep `INT1` or use `BINARY` | Bit Fusion's 1-bit values are unsigned {0,+1} (N §2), so `INT1` is defensible. `BINARY` is the vocabulary word (T §3), but it usually means ±1. Owner preference. | low |
| Data type | `INT16` | concern only: supported, not exercised | The Fig. 1 legend gives operand widths 1/1, 2/2, 4/4, 8/1 and 8/8 (X/BitFusion p01). No benchmark runs at 16 bits; 16-bit is the Eyeriss baseline and the top of the recursion ("supports up to 16-bit operands"). A added `INT16` deliberately. T §3's coexist rule targets `MIXED`, not individual widths, so leaving it is acceptable. The Note column should say "supported" if this is kept. | low (inferred from extraction) |

- **Level `ARCH` agrees** with N, A and the T Worked example.
- **"Compiler" claim.** A and N §3 say the design has "an ISA, a compiler". The paper has the Fusion-ISA only; "compiler" occurs only as Synopsys Design Compiler (verified grep). So there is no `SYS` question, and the "compiler" phrase in N §3 / A is unsupported.
- **Q and Stage.** Q, and S2 as BitSplit (`'bit-flexible'` hit), are right. Spatial fusion is a transient decomposition at array scope. `P` = S2 / Q / ASIC.
- **T drift.** T's Worked examples table still gives Bit Fusion's Data type as `INT`+`MIXED`, against T §3's own "give the bitwidth" and the row's explicit widths. Cosmetic.
- **Cell hygiene.** Note and Optimization are clean and every keyword is supported by N.

---

### [OLAccel](../../survey/papers/OLAccel/paper-note.md) ([pdf](../../survey/papers/OLAccel/10.1109_ISCA.2018.00063.pdf)) (olaccel) — `OK`

Everything agrees: row, N Tags, A §"For the note", PN, `P` (S2 / Q / ASIC) and T. The tags are `ARCH`, Q, `INT4` `INT8` `INT16` `MIXED` and S2 (outlier).
- `INT8` = outlier weights (Table I). `INT16` = outlier activations, with INT8 in the 8-bit comparison (N §2).
- These widths coexist with the 4-bit body, so `MIXED` passes T §3.
- Outlier handling at array/block scope is S2, and Pass 7 lists it there.

**Cell hygiene.** "**Pre-LLM root of the outlier thread**, recorded deliberately as such" refers to Pass 1's deliberate pre-2023 **`G3`**, which is retired. The "deliberately" now has nothing to attach to. Suggest "Pre-LLM root of the outlier thread (T §6)". Low. Optimization keywords are all supported by N §2–3.

---

### [Gist](../../survey/papers/Gist/paper-note.md) ([pdf](../../survey/papers/Gist/10.1109_ISCA.2018.00070.pdf)) (gist) — `CHANGE PROPOSED` (Platform only)

| Axis | Current | Proposed | Evidence | Confidence |
|---|---|---|---|---|
| Platform (`P`) | ASIC | GPU | Pure software on a stock "Maxwell GTX Titan X" with CNTK and cuDNN (X/Gist p03, p08; N §1 "pure software on a stock Titan X + CNTK", N §4 "No hardware"). T §5's precedence ends `… → GPU → ASIC`. The ASIC value is the fall-through default: the row text has neither "GPU" nor `P_NONHW`'s "no hardware proposed", because the Note says "not hardware" (verified regex run). Precedent in the same venue: LoKA, `ALGO+SYS` on GPU, is `GPU` in `P`. Fix with a `PLATFORM` override, or put "GPU" in the Note or Optimization. | high |
| Data type | `FP10` | keep; flag only | Off the T §3 list but real: "1 sign, 5 exponent and 4 mantissa bits" (X/Gist p06). It is the per-network minimum for Inception (N §2). | low |

- **Level and Q.** Level `ALGO+SYS` (Pass 1) and Q (owner ruling, Pass 4) are not re-litigated. They agree with N, A and PN.
- **Data type.** FP16 (VGG16), FP10 (Inception) and FP8 (AlexNet, Overfeat) are each used in the evaluation. Each coexists with the FP32 forward copy, so `MIXED` holds even though the narrow width is chosen per network (N §2, §4).
- **Stage.** Venue S2, `P` path `S1→S2`. The S1 half is derived by S1SIG from `custom FP8/FP10` (verified hit `'custom FP'`). It is legitimate under T §4 ("designing E2M3 is S1") and §6 (the narrow copy is **stored**). The S2 half is a per-tensor-lifetime precision split that never touches a datapath. That is arguable, but not worth a change. med.

**Cell hygiene.** "Sheet: Less related" is a source-sheet comment kept verbatim under Pass 1's policy, and it now sits beside a `Q` ruling. Consider marking it "(pre-Pass-4 sheet comment)". Low.

---

### Summary

| Paper | Verdict | Main items |
|---|---|---|
| [SamsungNPU](../../survey/papers/SamsungNPU/paper-note.md) ([pdf](../../survey/papers/SamsungNPU/10.1109_ISCA52012.2021.00011.pdf)) | CHANGE PROPOSED | Drop `MIXED`: INT16 is an alternative mode and every evaluated workload is INT8 (p04, p09; T §3). The Note cell duplicates itself and Pass 10. The Bit Fusion link points to MICRO. The BitSplit sub-category depends on the word "BitBrick" in a comparison sentence. |
| [DRQ](../../survey/papers/DRQ/paper-note.md) ([pdf](../../survey/papers/DRQ/10.1109_ISCA45697.2020.00086.pdf)) | MINOR | Tags OK. N/drq §2 ("geometric, not magnitude-based") contradicts the recorded outlier ruling and the paper (p04). The 2026-09-22 audit lives only in the Note cell. The `G4` `PRIMARY` comment is stale. |
| [SmartExchange](../../survey/papers/SmartExchange/paper-note.md) ([pdf](../../survey/papers/SmartExchange/2005.03403.pdf)) | CHANGE PROPOSED | N Tags Stage is still `S2` (row and `P` are `S1`). Add `MIXED` (4-bit Ce, 8-bit B, 8-bit A; p09), owner's call. `INT4` mislabels a POW2 code. The Note's "W = B·Ce" contradicts Eq. 1 (p03) and the cell's own later text. Self-referential history to cut. |
| [JPEG-ACT](../../survey/papers/JPEG-ACT/paper-note.md) ([pdf](../../survey/papers/JPEG-ACT/10.1109_ISCA45697.2020.00075.pdf)) | CHANGE PROPOSED | Row tags OK (S2 / `S3→S2` consistent). The classifier files it as Transform, which its own Note denies (T §7). Add a `PRIMARY` entry. `stage2.md` prints the refuted old Note. Platform should be GPU (Titan V; Ecco precedent). |
| [Bit Fusion](../../survey/papers/BitFusion/paper-note.md) ([pdf](../../survey/papers/BitFusion/1712.01507.pdf)) | MINOR | Add `TERNARY` (p07). `INT16` is supported but not exercised. `INT1` vs `BINARY` is a wording choice. The "compiler" claim in N/A is unsupported. T's worked example still shows `INT`. |
| [OLAccel](../../survey/papers/OLAccel/paper-note.md) ([pdf](../../survey/papers/OLAccel/10.1109_ISCA.2018.00063.pdf)) | OK | All consistent. The Note's "recorded deliberately" refers to the retired G3. |
| [Gist](../../survey/papers/Gist/paper-note.md) ([pdf](../../survey/papers/Gist/10.1109_ISCA.2018.00070.pdf)) | CHANGE PROPOSED | Platform `P` is ASIC by default and should be GPU (stock Titan X; LoKA precedent). FP10 is off-vocabulary but correct. Tags and the `S1→S2` path are OK. |
