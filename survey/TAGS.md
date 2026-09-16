# TAGS — the tag vocabulary and the tagged corpus

Every filed paper carries a `Tags:` line in its `ANALYSIS.md` header. This file is the
dictionary and the reverse index.

Last updated: **2026-09-09** ｜ 14 tags over 40 papers.

> `TransitiveArray` (filed 2026-09-03) is tagged `analytical-dtype` `multi-bitwidth-hw`
> `accelerator`. It is **deliberately not** tagged `lut-accelerator` or
> `non-analytical-dtype`, against the team repo's seed tags — reasoning in
> [`papers/TransitiveArray/ANALYSIS.md`](papers/TransitiveArray/ANALYSIS.md).

⚠️ **These tags were assigned from a brief-level reading** (abstract, introduction, section
map, headline results, conclusion) — not a full read. They are a working index, not a
finding. **As of 2026-09-09 every paper has full text** — the last four
(`TPUv4i`, `AQB8`, `Cambricon-SR`, `FATE`) were hand-downloaded and re-tagged from the papers
themselves, so no tag in this file is title-only any more.

---

## How the tags relate

Tags 1–4 answer *what kind of thing a value is*; 5–6 answer *at what precision and
granularity*; 7–10 answer *what hardware runs it*; 11–14 are cross-cutting.

The two distinctions that were settled explicitly with the human, because they are easy to
get wrong:

- **(1) vs (2)** — orthogonal, not exclusive. `(2) analytical-dtype` means *formula-defined*
  (exponent/mantissa fields, or any closed-form decode). `(1) new-data-type` means *novel*.
  A newly proposed analytical format such as MXFFP's flexible exponent/mantissa split gets
  **both**; a paper that merely runs INT8 gets `(2)` alone.
- **(5) vs (9)** — scheme versus datapath. `(5) mixed-precision` is the **quantization
  scheme** mixing precisions (W4A8, per-layer widths, INT4 inliers + FP16 outliers).
  `(9) multi-bitwidth-hw` is the **hardware** being reconfigurable across widths (bit-serial,
  bit-slice, composable, runtime datatype switching). **A fixed W4A8 unit is (5), not (9).**

---

## The tags

### (1) `new-data-type` — 7 papers

**The numeric format itself is the contribution.** The paper proposes a representation, not merely a use of one. Taxonomy §1.2.

[`AQB8`](papers/AQB8/ANALYSIS.md) · [`Mokey`](papers/Mokey/ANALYSIS.md) · [`MXFFP`](papers/MXFFP/ANALYSIS.md) · [`OliVe`](papers/OliVe/ANALYSIS.md) · [`RingCNN`](papers/RingCNN/ANALYSIS.md) · [`SmartExchange`](papers/SmartExchange/ANALYSIS.md) · [`UniCore`](papers/UniCore/ANALYSIS.md)

### (2) `analytical-dtype` — 23 papers

**Formula-defined format** — a value is decoded from fixed fields by an expression: INT4/8, FP8/FP4, MX, DynFP, power-of-two. Orthogonal to (1): a *new* analytical format gets both; a paper that merely uses INT8 gets only this.

[`AQB8`](papers/AQB8/ANALYSIS.md) · [`BitFusion`](papers/BitFusion/ANALYSIS.md) · [`DRQ`](papers/DRQ/ANALYSIS.md) · [`FATE`](papers/FATE/ANALYSIS.md) · [`LightNobel`](papers/LightNobel/ANALYSIS.md) · [`LoKA`](papers/LoKA/ANALYSIS.md) · [`LUTTensorCore`](papers/LUTTensorCore/ANALYSIS.md) · [`MicroScopiQ`](papers/MicroScopiQ/ANALYSIS.md) · [`MXFFP`](papers/MXFFP/ANALYSIS.md) · [`NDPLowBitFP`](papers/NDPLowBitFP/ANALYSIS.md) · [`Oaken`](papers/Oaken/ANALYSIS.md) · [`OLAccel`](papers/OLAccel/ANALYSIS.md) · [`OliVe`](papers/OliVe/ANALYSIS.md) · [`P3-LLM`](papers/P3-LLM/ANALYSIS.md) · [`RaPiD`](papers/RaPiD/ANALYSIS.md) · [`RingCNN`](papers/RingCNN/ANALYSIS.md) · [`SamsungNPU`](papers/SamsungNPU/ANALYSIS.md) · [`SmartExchange`](papers/SmartExchange/ANALYSIS.md) · [`Tender`](papers/Tender/ANALYSIS.md) · [`TPUv4i`](papers/TPUv4i/ANALYSIS.md) · [`TransitiveArray`](papers/TransitiveArray/ANALYSIS.md) · [`UniCore`](papers/UniCore/ANALYSIS.md) · [`XtraMAC`](papers/XtraMAC/ANALYSIS.md)

### (3) `non-analytical-dtype` — 6 papers

**Mapping, not encoding** — the value is a table entry: vector quantization, k-means centroids, learned codebooks, dictionaries. Taxonomy §1.3.

[`Ecco`](papers/Ecco/ANALYSIS.md) · [`EVA`](papers/EVA/ANALYSIS.md) · [`Mokey`](papers/Mokey/ANALYSIS.md) · [`OASIS`](papers/OASIS/ANALYSIS.md) · [`Omni-LUT`](papers/Omni-LUT/ANALYSIS.md) · [`Phi`](papers/Phi/ANALYSIS.md)

### (4) `combined-dtype` — 11 papers

**A value represented by more than one component**: dense inliers + sparse outliers, base + residual/delta, basis × coefficient, rank components at different precisions.

[`AQB8`](papers/AQB8/ANALYSIS.md) · [`AQuant`](papers/AQuant/ANALYSIS.md) · [`MicroScopiQ`](papers/MicroScopiQ/ANALYSIS.md) · [`Mokey`](papers/Mokey/ANALYSIS.md) · [`Oaken`](papers/Oaken/ANALYSIS.md) · [`OASIS`](papers/OASIS/ANALYSIS.md) · [`OLAccel`](papers/OLAccel/ANALYSIS.md) · [`OliVe`](papers/OliVe/ANALYSIS.md) · [`RAELLA`](papers/RAELLA/ANALYSIS.md) · [`SingularBit`](papers/SingularBit/ANALYSIS.md) · [`SmartExchange`](papers/SmartExchange/ANALYSIS.md)

### (5) `mixed-precision` — 23 papers

**The quantization scheme mixes precisions** across tensors, layers, channels or value classes — W4A8, per-layer bitwidths, INT4 inliers with FP16 outliers. Distinct from (9): this is the *scheme*.

[`AQB8`](papers/AQB8/ANALYSIS.md) · [`AQuant`](papers/AQuant/ANALYSIS.md) · [`BitFusion`](papers/BitFusion/ANALYSIS.md) · [`DRQ`](papers/DRQ/ANALYSIS.md) · [`FATE`](papers/FATE/ANALYSIS.md) · [`LightNobel`](papers/LightNobel/ANALYSIS.md) · [`LoKA`](papers/LoKA/ANALYSIS.md) · [`LUTTensorCore`](papers/LUTTensorCore/ANALYSIS.md) · [`MicroScopiQ`](papers/MicroScopiQ/ANALYSIS.md) · [`NDPLowBitFP`](papers/NDPLowBitFP/ANALYSIS.md) · [`Oaken`](papers/Oaken/ANALYSIS.md) · [`OASIS`](papers/OASIS/ANALYSIS.md) · [`OLAccel`](papers/OLAccel/ANALYSIS.md) · [`OliVe`](papers/OliVe/ANALYSIS.md) · [`Omni-LUT`](papers/Omni-LUT/ANALYSIS.md) · [`P3-LLM`](papers/P3-LLM/ANALYSIS.md) · [`RaPiD`](papers/RaPiD/ANALYSIS.md) · [`SamsungNPU`](papers/SamsungNPU/ANALYSIS.md) · [`SingularBit`](papers/SingularBit/ANALYSIS.md) · [`Tender`](papers/Tender/ANALYSIS.md) · [`TPUv4i`](papers/TPUv4i/ANALYSIS.md) · [`UniCore`](papers/UniCore/ANALYSIS.md) · [`XtraMAC`](papers/XtraMAC/ANALYSIS.md)

### (6) `dtype-granularity` — 16 papers

**A new granularity for the format or its scale**: block, sub-block, microscaling, channel, region, rank, token, element.

[`AQB8`](papers/AQB8/ANALYSIS.md) · [`AQuant`](papers/AQuant/ANALYSIS.md) · [`DRQ`](papers/DRQ/ANALYSIS.md) · [`Ecco`](papers/Ecco/ANALYSIS.md) · [`FATE`](papers/FATE/ANALYSIS.md) · [`LightNobel`](papers/LightNobel/ANALYSIS.md) · [`MicroScopiQ`](papers/MicroScopiQ/ANALYSIS.md) · [`MXFFP`](papers/MXFFP/ANALYSIS.md) · [`NDPLowBitFP`](papers/NDPLowBitFP/ANALYSIS.md) · [`Oaken`](papers/Oaken/ANALYSIS.md) · [`OLAccel`](papers/OLAccel/ANALYSIS.md) · [`P3-LLM`](papers/P3-LLM/ANALYSIS.md) · [`RAELLA`](papers/RAELLA/ANALYSIS.md) · [`RingCNN`](papers/RingCNN/ANALYSIS.md) · [`SingularBit`](papers/SingularBit/ANALYSIS.md) · [`Tender`](papers/Tender/ANALYSIS.md)

### (7) `gpu-kernels` — 5 papers

**Targets GPUs or GPU kernels** rather than custom silicon — including hardware proposals that modify a GPU.

[`CommutativeDataReordering`](papers/CommutativeDataReordering/ANALYSIS.md) · [`Ecco`](papers/Ecco/ANALYSIS.md) · [`Gist`](papers/Gist/ANALYSIS.md) · [`JPEG-ACT`](papers/JPEG-ACT/ANALYSIS.md) · [`LoKA`](papers/LoKA/ANALYSIS.md)

### (8) `accelerator` — 38 papers

**Custom hardware**: ASIC, NPU, or FPGA. The default platform of this corpus.

[`AQB8`](papers/AQB8/ANALYSIS.md) · [`AQuant`](papers/AQuant/ANALYSIS.md) · [`BitFusion`](papers/BitFusion/ANALYSIS.md) · [`Cambricon-SR`](papers/Cambricon-SR/ANALYSIS.md) · [`CommutativeDataReordering`](papers/CommutativeDataReordering/ANALYSIS.md) · [`DRQ`](papers/DRQ/ANALYSIS.md) · [`Ecco`](papers/Ecco/ANALYSIS.md) · [`ELSA`](papers/ELSA/ANALYSIS.md) · [`ENEC`](papers/ENEC/ANALYSIS.md) · [`EVA`](papers/EVA/ANALYSIS.md) · [`FATE`](papers/FATE/ANALYSIS.md) · [`IBMCompressionAccelerator`](papers/IBMCompressionAccelerator/ANALYSIS.md) · [`JPEG-ACT`](papers/JPEG-ACT/ANALYSIS.md) · [`LightNobel`](papers/LightNobel/ANALYSIS.md) · [`LUTTensorCore`](papers/LUTTensorCore/ANALYSIS.md) · [`MicroScopiQ`](papers/MicroScopiQ/ANALYSIS.md) · [`Mokey`](papers/Mokey/ANALYSIS.md) · [`MXFFP`](papers/MXFFP/ANALYSIS.md) · [`NDPLowBitFP`](papers/NDPLowBitFP/ANALYSIS.md) · [`Oaken`](papers/Oaken/ANALYSIS.md) · [`OASIS`](papers/OASIS/ANALYSIS.md) · [`OLAccel`](papers/OLAccel/ANALYSIS.md) · [`OliVe`](papers/OliVe/ANALYSIS.md) · [`Omni-LUT`](papers/Omni-LUT/ANALYSIS.md) · [`P3-LLM`](papers/P3-LLM/ANALYSIS.md) · [`Phi`](papers/Phi/ANALYSIS.md) · [`RAELLA`](papers/RAELLA/ANALYSIS.md) · [`RaPiD`](papers/RaPiD/ANALYSIS.md) · [`RingCNN`](papers/RingCNN/ANALYSIS.md) · [`SamsungNPU`](papers/SamsungNPU/ANALYSIS.md) · [`SingularBit`](papers/SingularBit/ANALYSIS.md) · [`SmartExchange`](papers/SmartExchange/ANALYSIS.md) · [`SpZip`](papers/SpZip/ANALYSIS.md) · [`Tender`](papers/Tender/ANALYSIS.md) · [`TPUv4i`](papers/TPUv4i/ANALYSIS.md) · [`TransitiveArray`](papers/TransitiveArray/ANALYSIS.md) · [`UniCore`](papers/UniCore/ANALYSIS.md) · [`XtraMAC`](papers/XtraMAC/ANALYSIS.md)

### (9) `multi-bitwidth-hw` — 11 papers

**The datapath is reconfigurable across bitwidths** — bit-serial, bit-slice, composable MACs, runtime datatype switching. Per the agreed rule, a *fixed* W4A8 unit does **not** qualify; W2/3/4-style width scalability does.

[`BitFusion`](papers/BitFusion/ANALYSIS.md) · [`DRQ`](papers/DRQ/ANALYSIS.md) · [`FATE`](papers/FATE/ANALYSIS.md) · [`LightNobel`](papers/LightNobel/ANALYSIS.md) · [`LUTTensorCore`](papers/LUTTensorCore/ANALYSIS.md) · [`RAELLA`](papers/RAELLA/ANALYSIS.md) · [`RaPiD`](papers/RaPiD/ANALYSIS.md) · [`SamsungNPU`](papers/SamsungNPU/ANALYSIS.md) · [`TransitiveArray`](papers/TransitiveArray/ANALYSIS.md) · [`UniCore`](papers/UniCore/ANALYSIS.md) · [`XtraMAC`](papers/XtraMAC/ANALYSIS.md)

### (10) `lut-accelerator` — 5 papers

**Compute is table lookup**, not arithmetic.

[`EVA`](papers/EVA/ANALYSIS.md) · [`LUTTensorCore`](papers/LUTTensorCore/ANALYSIS.md) · [`Mokey`](papers/Mokey/ANALYSIS.md) · [`OASIS`](papers/OASIS/ANALYSIS.md) · [`Omni-LUT`](papers/Omni-LUT/ANALYSIS.md)

### (11) `kv-cache` — 5 papers

**The KV cache is the quantization target**, rather than weights or activations. _(added 2026-09-02)_

[`Ecco`](papers/Ecco/ANALYSIS.md) · [`Oaken`](papers/Oaken/ANALYSIS.md) · [`Omni-LUT`](papers/Omni-LUT/ANALYSIS.md) · [`P3-LLM`](papers/P3-LLM/ANALYSIS.md) · [`SingularBit`](papers/SingularBit/ANALYSIS.md)

### (12) `pim-ndp` — 3 papers

**Compute in or near memory** — DRAM-PIM, NDP, analog ReRAM PIM. _(added 2026-09-02)_

[`NDPLowBitFP`](papers/NDPLowBitFP/ANALYSIS.md) · [`P3-LLM`](papers/P3-LLM/ANALYSIS.md) · [`RAELLA`](papers/RAELLA/ANALYSIS.md)

### (13) `training` — 4 papers

**Quantization or compression during training**, not inference. _(added 2026-09-02)_

[`Gist`](papers/Gist/ANALYSIS.md) · [`JPEG-ACT`](papers/JPEG-ACT/ANALYSIS.md) · [`LoKA`](papers/LoKA/ANALYSIS.md) · [`RaPiD`](papers/RaPiD/ANALYSIS.md)

### (14) `lossless-compression` — 5 papers

**No value loss at all.** Gives the compression-not-quantization papers a handle. _(added 2026-09-02)_

[`CommutativeDataReordering`](papers/CommutativeDataReordering/ANALYSIS.md) · [`ENEC`](papers/ENEC/ANALYSIS.md) · [`Gist`](papers/Gist/ANALYSIS.md) · [`IBMCompressionAccelerator`](papers/IBMCompressionAccelerator/ANALYSIS.md) · [`SpZip`](papers/SpZip/ANALYSIS.md)

---

## Matrix

Columns are the tag numbers above.

| Paper | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| [`AQB8`](papers/AQB8/ANALYSIS.md) | ● | ● |  | ● | ● | ● |  | ● |  |  |  |  |  |  |
| [`AQuant`](papers/AQuant/ANALYSIS.md) |  |  |  | ● | ● | ● |  | ● |  |  |  |  |  |  |
| [`BitFusion`](papers/BitFusion/ANALYSIS.md) |  | ● |  |  | ● |  |  | ● | ● |  |  |  |  |  |
| [`Cambricon-SR`](papers/Cambricon-SR/ANALYSIS.md) |  |  |  |  |  |  |  | ● |  |  |  |  |  |  |
| [`CommutativeDataReordering`](papers/CommutativeDataReordering/ANALYSIS.md) |  |  |  |  |  |  | ● | ● |  |  |  |  |  | ● |
| [`DRQ`](papers/DRQ/ANALYSIS.md) |  | ● |  |  | ● | ● |  | ● | ● |  |  |  |  |  |
| [`Ecco`](papers/Ecco/ANALYSIS.md) |  |  | ● |  |  | ● | ● | ● |  |  | ● |  |  |  |
| [`ELSA`](papers/ELSA/ANALYSIS.md) |  |  |  |  |  |  |  | ● |  |  |  |  |  |  |
| [`ENEC`](papers/ENEC/ANALYSIS.md) |  |  |  |  |  |  |  | ● |  |  |  |  |  | ● |
| [`EVA`](papers/EVA/ANALYSIS.md) |  |  | ● |  |  |  |  | ● |  | ● |  |  |  |  |
| [`FATE`](papers/FATE/ANALYSIS.md) |  | ● |  |  | ● | ● |  | ● | ● |  |  |  |  |  |
| [`Gist`](papers/Gist/ANALYSIS.md) |  |  |  |  |  |  | ● |  |  |  |  |  | ● | ● |
| [`IBMCompressionAccelerator`](papers/IBMCompressionAccelerator/ANALYSIS.md) |  |  |  |  |  |  |  | ● |  |  |  |  |  | ● |
| [`JPEG-ACT`](papers/JPEG-ACT/ANALYSIS.md) |  |  |  |  |  |  | ● | ● |  |  |  |  | ● |  |
| [`LightNobel`](papers/LightNobel/ANALYSIS.md) |  | ● |  |  | ● | ● |  | ● | ● |  |  |  |  |  |
| [`LoKA`](papers/LoKA/ANALYSIS.md) |  | ● |  |  | ● |  | ● |  |  |  |  |  | ● |  |
| [`LUTTensorCore`](papers/LUTTensorCore/ANALYSIS.md) |  | ● |  |  | ● |  |  | ● | ● | ● |  |  |  |  |
| [`MicroScopiQ`](papers/MicroScopiQ/ANALYSIS.md) |  | ● |  | ● | ● | ● |  | ● |  |  |  |  |  |  |
| [`Mokey`](papers/Mokey/ANALYSIS.md) | ● |  | ● | ● |  |  |  | ● |  | ● |  |  |  |  |
| [`MXFFP`](papers/MXFFP/ANALYSIS.md) | ● | ● |  |  |  | ● |  | ● |  |  |  |  |  |  |
| [`NDPLowBitFP`](papers/NDPLowBitFP/ANALYSIS.md) |  | ● |  |  | ● | ● |  | ● |  |  |  | ● |  |  |
| [`Oaken`](papers/Oaken/ANALYSIS.md) |  | ● |  | ● | ● | ● |  | ● |  |  | ● |  |  |  |
| [`OASIS`](papers/OASIS/ANALYSIS.md) |  |  | ● | ● | ● |  |  | ● |  | ● |  |  |  |  |
| [`OLAccel`](papers/OLAccel/ANALYSIS.md) |  | ● |  | ● | ● | ● |  | ● |  |  |  |  |  |  |
| [`OliVe`](papers/OliVe/ANALYSIS.md) | ● | ● |  | ● | ● |  |  | ● |  |  |  |  |  |  |
| [`Omni-LUT`](papers/Omni-LUT/ANALYSIS.md) |  |  | ● |  | ● |  |  | ● |  | ● | ● |  |  |  |
| [`P3-LLM`](papers/P3-LLM/ANALYSIS.md) |  | ● |  |  | ● | ● |  | ● |  |  | ● | ● |  |  |
| [`Phi`](papers/Phi/ANALYSIS.md) |  |  | ● |  |  |  |  | ● |  |  |  |  |  |  |
| [`RAELLA`](papers/RAELLA/ANALYSIS.md) |  |  |  | ● |  | ● |  | ● | ● |  |  | ● |  |  |
| [`RaPiD`](papers/RaPiD/ANALYSIS.md) |  | ● |  |  | ● |  |  | ● | ● |  |  |  | ● |  |
| [`RingCNN`](papers/RingCNN/ANALYSIS.md) | ● | ● |  |  |  | ● |  | ● |  |  |  |  |  |  |
| [`SamsungNPU`](papers/SamsungNPU/ANALYSIS.md) |  | ● |  |  | ● |  |  | ● | ● |  |  |  |  |  |
| [`SingularBit`](papers/SingularBit/ANALYSIS.md) |  |  |  | ● | ● | ● |  | ● |  |  | ● |  |  |  |
| [`SmartExchange`](papers/SmartExchange/ANALYSIS.md) | ● | ● |  | ● |  |  |  | ● |  |  |  |  |  |  |
| [`SpZip`](papers/SpZip/ANALYSIS.md) |  |  |  |  |  |  |  | ● |  |  |  |  |  | ● |
| [`Tender`](papers/Tender/ANALYSIS.md) |  | ● |  |  | ● | ● |  | ● |  |  |  |  |  |  |
| [`TPUv4i`](papers/TPUv4i/ANALYSIS.md) |  | ● |  |  | ● |  |  | ● |  |  |  |  |  |  |
| [`UniCore`](papers/UniCore/ANALYSIS.md) | ● | ● |  |  | ● |  |  | ● | ● |  |  |  |  |  |
| [`XtraMAC`](papers/XtraMAC/ANALYSIS.md) |  | ● |  |  | ● |  |  | ● | ● |  |  |  |  |  |

---

## What the tag distribution says

- **`analytical-dtype` dominates and `non-analytical-dtype` is the minority** — the corpus is
  mostly exponent/mantissa and integer work, with the lookup-table line ([`Mokey`](papers/Mokey/ANALYSIS.md)
  2022 → [`LUTTensorCore`](papers/LUTTensorCore/ANALYSIS.md) 2025 →
  [`OASIS`](papers/OASIS/ANALYSIS.md)/[`Omni-LUT`](papers/Omni-LUT/ANALYSIS.md)/[`EVA`](papers/EVA/ANALYSIS.md)
  2026) growing late and fast. That trend is a survey finding in itself.
- **`combined-dtype` is the most persistent thread**, running unbroken from
  [`OLAccel`](papers/OLAccel/ANALYSIS.md) (2018) to [`OASIS`](papers/OASIS/ANALYSIS.md) (2026),
  and it is where papers most often contradict each other — see the cons in
  [`OliVe`](papers/OliVe/ANALYSIS.md) and [`MicroScopiQ`](papers/MicroScopiQ/ANALYSIS.md).
- **`kv-cache` appears only from 2025** and is already five papers — the fastest-growing
  target in the corpus.
- **`new-data-type` is thin** (7 papers, 2 of them pre-2022). The taxonomy's §1.2
  and §1.3 branches name Posit, APoT, ANT/Flint, GOBO, BiScale and NormalFloat —
  **none of which is in this ISCA-only corpus.** See the scope note in
  [`README.md`](README.md#scope).
- **`training` is nearly absent** (4 papers, 3 of them pre-2022 CNN work plus
  [`LoKA`](papers/LoKA/ANALYSIS.md)). If the survey means to cover low-precision training,
  the corpus does not currently support it.
