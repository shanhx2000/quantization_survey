# 01 — MAC-GEMM vs LUT-GEMM cost per quantization frame

Generated 2026-10-22 by `make_tables.py` from [`../results/`](../results/) (the
cmp00 sweep snapshot; see [`../README.md`](../README.md)). Edit the script, not this file.

**Cell format: area (µm²) / power (mW)** at 500 MHz, for hardware that consumes one
v-element slice of a dot product every cycle. Power × 2 = energy per cycle in pJ.

## Missing data

`#` in a cell means at least one primitive has no number in the snapshot:

| Primitive | Needed by | Frames | v | Why it is missing |
|---|---|---|---|---|
| `mul_int3xint8` | MAC opt | wq=3 wa=int8 | all | pe_sweep has only same-type multipliers (`mul_int4` is int4 × int4) |
| `mul_int4xint8` | MAC opt | wq=4 wa=int8 | all | pe_sweep has only same-type multipliers (`mul_int4` is int4 × int4) |
| `mul_int6xint8` | MAC opt | wq=6 wa=int8 | all | pe_sweep has only same-type multipliers (`mul_int4` is int4 × int4) |
| `mul_int3xfp16` | MAC opt | wq=3 wa=fp16 | all | pe_sweep has only same-type multipliers (`mul_int4` is int4 × int4) |
| `mul_int4xfp16` | MAC opt | wq=4 wa=fp16 | all | pe_sweep has only same-type multipliers (`mul_int4` is int4 × int4) |
| `mul_int6xfp16` | MAC opt | wq=6 wa=fp16 | all | pe_sweep has only same-type multipliers (`mul_int4` is int4 × int4) |
| `mul_int8xfp16` | MAC opt | wq=8 wa=fp16 | all | pe_sweep has only same-type multipliers (`mul_int4` is int4 × int4) |
| `sram_lut_n8` | LUT SRAM, pre-ignore+symm | every frame | 4 | CACTI does not model arrays under 64 bytes (N < 32 at 16 bits) |
| `sram_lut_n16` | LUT SRAM, pre-ignore | every frame | 4 | CACTI does not model arrays under 64 bytes (N < 32 at 16 bits) |

The script looks for the multipliers under the names in the first column, so a pe_sweep
design with that name fills the cells on the next run.

## Methods and cost model

* **wq**: weight bits (int: 3, 4, 6, 8). **wa**: activation format (int8 or fp16).
  **v**: vector length, the number of activations combined per step.
* **MAC-GEMM**: v multipliers and v adders.
  * *fp16*: v × fp16 mul + v × fp16 add. Same in every frame.
  * *opt*: v × (int-wq × wa) mul + v × fp16 add.
  * *int8*: v × int8 mul + v × int16 add. Same in every frame.
* **LUT-GEMM** (lookup table): the table holds the partial sums of v activations for every
  v-bit weight pattern; each of the wq weight bit-planes reads one entry, and wq fp16 adders
  combine them. Entries are 16 bits (fp16), matching the 16-bit buffer sweep.
  * *pre-ignore*: 2^v entries; the cost of building the table is ignored.
  * *pre-ignore+symm*: 2^v / 2 entries; the other half is a sign flip of the stored half,
    and the flip is ignored.
  * *reg*: the table is a flip-flop register file (`buffer_n<N>`, synthesized).
    *SRAM*: the table is a CACTI 1RW SRAM.

| v | 4 | 6 | 7 | 8 |
|---|---|---|---|---|
| LUT entries, pre-ignore (2^v) | 16 | 64 | 128 | 256 |
| LUT entries, pre-ignore+symm (2^v / 2) | 8 | 32 | 64 | 128 |

* **Area** = Σ count × unit area. Adders and multipliers: logic-only area of `u_core` from
  pe_sweep. Reg LUT: the whole `u_buf` (flops, address decode, read mux, clock gating).
  SRAM LUT: CACTI area.
* **Power** = Σ count × unit power, every unit doing one operation per cycle.
* **Not counted:** table precompute, the sign flip, the 2^b weighting between bit-planes, and
  any int → fp conversion.

## Tables

### wq = int3, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int3×int8 mul + v × fp16 add | # | # | # | # |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg, pre-ignore | 3 × LUT[2^v] read + 3 × fp16 add | 3,593 / 6.11 | 9,438 / 7.65 | 17,126 / 9.41 | 32,703 / 16.41 |
| LUT reg, pre-ignore+symm | 3 × LUT[2^v/2] read + 3 × fp16 add | 2,617 / 5.83 | 5,565 / 6.74 | 9,438 / 7.65 | 17,126 / 9.41 |
| LUT SRAM, pre-ignore | 3 × LUT[2^v] read + 3 × fp16 add | # | 2,272 / 5.13 | 2,901 / 5.52 | 3,916 / 6.03 |
| LUT SRAM, pre-ignore+symm | 3 × LUT[2^v/2] read + 3 × fp16 add | # | 1,964 / 4.93 | 2,272 / 5.13 | 2,901 / 5.52 |

### wq = int4, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int4×int8 mul + v × fp16 add | # | # | # | # |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg, pre-ignore | 4 × LUT[2^v] read + 4 × fp16 add | 4,791 / 8.15 | 12,584 / 10.20 | 22,834 / 12.54 | 43,605 / 21.88 |
| LUT reg, pre-ignore+symm | 4 × LUT[2^v/2] read + 4 × fp16 add | 3,489 / 7.77 | 7,419 / 8.99 | 12,584 / 10.20 | 22,834 / 12.54 |
| LUT SRAM, pre-ignore | 4 × LUT[2^v] read + 4 × fp16 add | # | 3,030 / 6.84 | 3,868 / 7.36 | 5,221 / 8.05 |
| LUT SRAM, pre-ignore+symm | 4 × LUT[2^v/2] read + 4 × fp16 add | # | 2,619 / 6.57 | 3,030 / 6.84 | 3,868 / 7.36 |

### wq = int6, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int6×int8 mul + v × fp16 add | # | # | # | # |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg, pre-ignore | 6 × LUT[2^v] read + 6 × fp16 add | 7,186 / 12.22 | 18,876 / 15.30 | 34,251 / 18.81 | 65,407 / 32.81 |
| LUT reg, pre-ignore+symm | 6 × LUT[2^v/2] read + 6 × fp16 add | 5,234 / 11.66 | 11,129 / 13.48 | 18,876 / 15.30 | 34,251 / 18.81 |
| LUT SRAM, pre-ignore | 6 × LUT[2^v] read + 6 × fp16 add | # | 4,544 / 10.26 | 5,801 / 11.04 | 7,831 / 12.07 |
| LUT SRAM, pre-ignore+symm | 6 × LUT[2^v/2] read + 6 × fp16 add | # | 3,929 / 9.86 | 4,544 / 10.26 | 5,801 / 11.04 |

### wq = int8, wa = int8

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int8×int8 mul + v × fp16 add | 2,629 / 7.10 | 3,944 / 10.65 | 4,601 / 12.42 | 5,259 / 14.19 |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg, pre-ignore | 8 × LUT[2^v] read + 8 × fp16 add | 9,581 / 16.29 | 25,168 / 20.40 | 45,668 / 25.08 | 87,209 / 43.75 |
| LUT reg, pre-ignore+symm | 8 × LUT[2^v/2] read + 8 × fp16 add | 6,978 / 15.54 | 14,839 / 17.97 | 25,168 / 20.40 | 45,668 / 25.08 |
| LUT SRAM, pre-ignore | 8 × LUT[2^v] read + 8 × fp16 add | # | 6,059 / 13.68 | 7,735 / 14.72 | 10,442 / 16.09 |
| LUT SRAM, pre-ignore+symm | 8 × LUT[2^v/2] read + 8 × fp16 add | # | 5,239 / 13.15 | 6,059 / 13.68 | 7,735 / 14.72 |

### wq = int3, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int3×fp16 mul + v × fp16 add | # | # | # | # |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg, pre-ignore | 3 × LUT[2^v] read + 3 × fp16 add | 3,593 / 6.11 | 9,438 / 7.65 | 17,126 / 9.41 | 32,703 / 16.41 |
| LUT reg, pre-ignore+symm | 3 × LUT[2^v/2] read + 3 × fp16 add | 2,617 / 5.83 | 5,565 / 6.74 | 9,438 / 7.65 | 17,126 / 9.41 |
| LUT SRAM, pre-ignore | 3 × LUT[2^v] read + 3 × fp16 add | # | 2,272 / 5.13 | 2,901 / 5.52 | 3,916 / 6.03 |
| LUT SRAM, pre-ignore+symm | 3 × LUT[2^v/2] read + 3 × fp16 add | # | 1,964 / 4.93 | 2,272 / 5.13 | 2,901 / 5.52 |

### wq = int4, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int4×fp16 mul + v × fp16 add | # | # | # | # |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg, pre-ignore | 4 × LUT[2^v] read + 4 × fp16 add | 4,791 / 8.15 | 12,584 / 10.20 | 22,834 / 12.54 | 43,605 / 21.88 |
| LUT reg, pre-ignore+symm | 4 × LUT[2^v/2] read + 4 × fp16 add | 3,489 / 7.77 | 7,419 / 8.99 | 12,584 / 10.20 | 22,834 / 12.54 |
| LUT SRAM, pre-ignore | 4 × LUT[2^v] read + 4 × fp16 add | # | 3,030 / 6.84 | 3,868 / 7.36 | 5,221 / 8.05 |
| LUT SRAM, pre-ignore+symm | 4 × LUT[2^v/2] read + 4 × fp16 add | # | 2,619 / 6.57 | 3,030 / 6.84 | 3,868 / 7.36 |

### wq = int6, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int6×fp16 mul + v × fp16 add | # | # | # | # |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg, pre-ignore | 6 × LUT[2^v] read + 6 × fp16 add | 7,186 / 12.22 | 18,876 / 15.30 | 34,251 / 18.81 | 65,407 / 32.81 |
| LUT reg, pre-ignore+symm | 6 × LUT[2^v/2] read + 6 × fp16 add | 5,234 / 11.66 | 11,129 / 13.48 | 18,876 / 15.30 | 34,251 / 18.81 |
| LUT SRAM, pre-ignore | 6 × LUT[2^v] read + 6 × fp16 add | # | 4,544 / 10.26 | 5,801 / 11.04 | 7,831 / 12.07 |
| LUT SRAM, pre-ignore+symm | 6 × LUT[2^v/2] read + 6 × fp16 add | # | 3,929 / 9.86 | 4,544 / 10.26 | 5,801 / 11.04 |

### wq = int8, wa = fp16

| Method | Counts | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|---|
| MAC fp16 | v × fp16 mul + v × fp16 add | 3,595 / 10.38 | 5,393 / 15.56 | 6,291 / 18.16 | 7,190 / 20.75 |
| MAC opt | v × int8×fp16 mul + v × fp16 add | # | # | # | # |
| MAC int8 | v × int8 mul + v × int16 add | 700 / 1.19 | 1,050 / 1.79 | 1,225 / 2.08 | 1,400 / 2.38 |
| LUT reg, pre-ignore | 8 × LUT[2^v] read + 8 × fp16 add | 9,581 / 16.29 | 25,168 / 20.40 | 45,668 / 25.08 | 87,209 / 43.75 |
| LUT reg, pre-ignore+symm | 8 × LUT[2^v/2] read + 8 × fp16 add | 6,978 / 15.54 | 14,839 / 17.97 | 25,168 / 20.40 | 45,668 / 25.08 |
| LUT SRAM, pre-ignore | 8 × LUT[2^v] read + 8 × fp16 add | # | 6,059 / 13.68 | 7,735 / 14.72 | 10,442 / 16.09 |
| LUT SRAM, pre-ignore+symm | 8 × LUT[2^v/2] read + 8 × fp16 add | # | 5,239 / 13.15 | 6,059 / 13.68 | 7,735 / 14.72 |

## Unit costs used

| Primitive | Area (µm²) | Power (mW) | Source | Slack (ps) |
|---|---|---|---|---|
| `mul_fp16` | 383.7 | 1.064 | `mul_fp16` | 0 |
| `add_fp16` | 515.1 | 1.530 | `add_fp16` | 1 |
| `mul_int8` | 142.3 | 0.244 | `mul_int8` | 730 |
| `add_int16` | 32.8 | 0.053 | `add_int16` | 715 |
| `mul_int3xint8` | # | # | `mul_int3xint8` |  |
| `mul_int4xint8` | # | # | `mul_int4xint8` |  |
| `mul_int6xint8` | # | # | `mul_int6xint8` |  |
| `mul_int3xfp16` | # | # | `mul_int3xfp16` |  |
| `mul_int4xfp16` | # | # | `mul_int4xfp16` |  |
| `mul_int6xfp16` | # | # | `mul_int6xfp16` |  |
| `mul_int8xfp16` | # | # | `mul_int8xfp16` |  |
| `reg_lut_n8` | 357.2 | 0.413 | `buffer_n8` (synthesized, 1RW) | 951 |
| `reg_lut_n16` | 682.5 | 0.507 | `buffer_n16` (synthesized, 1RW) | 849 |
| `reg_lut_n32` | 1,339.8 | 0.717 | `buffer_n32` (synthesized, 1RW) | 812 |
| `reg_lut_n64` | 2,630.9 | 1.020 | `buffer_n64` (synthesized, 1RW) | 780 |
| `reg_lut_n128` | 5,193.5 | 1.605 | `buffer_n128` (synthesized, 1RW) | 816 |
| `reg_lut_n256` | 10,386.1 | 3.939 | `buffer_n256` (synthesized, 1RW) | 789 |
| `sram_lut_n8` | # | # | CACTI 1RW, N = 8 |  |
| `sram_lut_n16` | # | # | CACTI 1RW, N = 16 |  |
| `sram_lut_n32` | 139.7 | 0.114 | CACTI 1RW, N = 32 |  |
| `sram_lut_n64` | 242.3 | 0.181 | CACTI 1RW, N = 64 |  |
| `sram_lut_n128` | 451.8 | 0.310 | CACTI 1RW, N = 128 |  |
| `sram_lut_n256` | 790.1 | 0.482 | CACTI 1RW, N = 256 |  |

## Notes

1. **LUT area counts wq separate tables.** The spec counts wq LUT reads, and each read is
   costed as one whole table. All wq bit-planes of a weight index the *same* activation
   table, so one table with wq read ports, or one table shared across output channels,
   would need less storage. The sweep has no multi-read-port buffer, so that case is not
   costed. The LUT rows are an upper bound on area and on flop power.
2. **Reg LUT power is an upper bound.** It was measured with 80% reads / 20% writes; a LUT
   is read-only during the GEMM, and read-only power was not measured. The flow's 5 ns
   clock transition also inflates flip-flop power: on `buffer_n4`, 0.05 ns cut `u_buf` power
   from 0.375 to 0.153 mW (buffer REPORT note 2).
3. **SRAM LUT power** uses the same 80/20 mix. Read-only (static + 500 MHz × E_read) is a
   little lower: N = 32: 0.110 vs 0.114 mW; N = 64: 0.172 vs 0.181 mW; N = 128: 0.293 vs 0.310 mW; N = 256: 0.469 vs 0.482 mW.
4. **Reg LUT at N = 256** (v = 8, pre-ignore) carries the logic-power step that the
   buffer report flags in its note 4. Treat that column with care.
5. **The LUT rows do not depend on wa** because the spec uses 16-bit entries and fp16 adds in
   both frames. With wa = int8, the entries could be integer partial sums (8 + ⌈log2 v⌉ bits)
   added in int16. That variant is not in the spec and is not costed.
6. **MAC opt with wa = int8** adds an integer product in fp16, which needs an int → fp16
   conversion that the spec does not count. In pe_sweep it is not free:
   `mac_mulint8_addfp16` has 1,763 µm² of logic against 657 µm² for
   `mul_int8` + `add_fp16`, although part of that gap is upsizing to close timing in one
   cycle (pe REPORT note 2).
7. **fp16 units close timing at ~0 ps slack** (`mul_fp16` 0 ps,
   `add_fp16` 1 ps), so their area includes upsizing.
