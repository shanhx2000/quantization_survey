# 01 — MAC-GEMM vs LUT-GEMM cost per quantization frame

Generated 2026-10-22 by `make_tables.py` from [`../results/`](../results/) (the cmp00 sweep
snapshot; see [`../README.md`](../README.md)). Edit the script, not this file.

**Tables, one file per batch size: [bs = 1](tables-bs1.md) · [bs = 2](tables-bs2.md) · [bs = 4](tables-bs4.md) · [bs = 8](tables-bs8.md).** Each file has one table per frame
(wq ∈ {int1, ter, int2, int3, int4, int6, int8} × wa ∈ {int8, fp16}), one row per method and one
column per v. **Cell: area (µm²) / power (mW)** at 500 MHz, for hardware that consumes one
v-element slice of a dot product for every batch row each cycle. Power × 2 = energy per cycle in
pJ. **`#` = no data yet**, for area and power separately.

## Missing data

| Data | Missing | Configurations | Why |
|---|---|---|---|
| Mixed-type multiplier | area + power | `mul_int2xfp16`, `mul_int2xint8`, `mul_int3xfp16`, `mul_int3xint8`, `mul_int4xfp16`, `mul_int4xint8`, `mul_int6xfp16`, `mul_int6xint8`, `mul_int8xfp16` | pe_sweep has only same-type multipliers (`mul_int4` is int4 × int4) |
| Reg LUT, 1 read port | power | W = 16: N = 8, 16, 32, 64, 128, 256 | no read-only power run (measured at 80% read / 20% write) |
| Reg LUT, 1 read port | area + power | W = 8: N = 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192<br>W = 16: N = 512, 1024, 2048, 4096, 8192<br>W = 32: N = 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192<br>W = 64: N = 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192<br>W = 128: N = 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192 | only W = 16, N ≤ 256 tables were run |
| Reg LUT, wq read ports | area + power | W = 8: N = 8, 16, 32, 64, 128, 256, R = 2/3/4/6/8<br>W = 16: N = 8, 16, 32, 64, 128, 256, R = 2/3/4/6/8<br>W = 32: N = 8, 16, 32, 64, 128, 256, R = 2/3/4/6/8<br>W = 64: N = 8, 16, 32, 64, 128, 256, R = 2/3/4/6/8<br>W = 128: N = 8, 16, 32, 64, 128, 256, R = 2/3/4/6/8 | no multi-read-port table was run |
| SRAM LUT, 1 read port | area + power | W = 8: N = 8, 16, 32<br>W = 16: N = 8, 16<br>W = 32: N = 8 | below the CACTI floor of 64 bytes |
| SRAM LUT, 1 read port | area + power | W = 8: N = 64, 128, 256, 512, 1024, 2048, 4096, 8192<br>W = 16: N = 512, 1024, 2048, 4096, 8192<br>W = 32: N = 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192<br>W = 64: N = 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192<br>W = 128: N = 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192 | only W = 16, N ≤ 256 tables were run |
| SRAM LUT, wq read ports | area + power | W = 8: N = 8, 16, 32, R = 2/3/4/6/8<br>W = 16: N = 8, 16, R = 2/3/4/6/8<br>W = 32: N = 8, R = 2/3/4/6/8 | below the CACTI floor of 64 bytes |
| SRAM LUT, wq read ports | area + power | W = 8: N = 64, 128, 256, R = 2/3/4/6/8<br>W = 16: N = 32, 64, 128, 256, R = 2/3/4/6/8<br>W = 32: N = 16, 32, 64, 128, 256, R = 2/3/4/6/8<br>W = 64: N = 8, 16, 32, 64, 128, 256, R = 2/3/4/6/8<br>W = 128: N = 8, 16, 32, 64, 128, 256, R = 2/3/4/6/8 | no multi-read-port table was run |

What to run to fill these: `cmp00:~/isca26hw/micro26rcf/playground/todo/mac_lut_data_to_collect.md`.

## Methods and cost model

* **wq**: weight format: int1, ter, int2, int3, int4, int6, int8. int-b = b-bit integer; **ter** = ternary
  {−1, 0, +1}. **wa**: activation format (int8 or fp16). **v**: vector length, the number of
  activations combined per step. **bs**: batch size (1, 2, 4, 8).
* **MAC-GEMM**: bs·v multipliers and bs·v adders (a batch of bs needs bs times the resources).
  * *fp16*: v × fp16 mul + v × fp16 add.
  * *opt*: v × (int-wq × wa) mul + v × fp16 add. The int → fp16 conversion that wa = int8
    needs is not counted; see
    [02-int-to-fp-converter-cost](../02-int-to-fp-converter-cost/README.md) for its size.
  * *int8*: v × int8 mul + v × int16 add.
  * **wq = int1 and ter: no multiplier in any MAC row**, only the adds. The weight just
    selects, negates or zeroes the activation, and that is not counted. So for these two,
    *fp16* and *opt* are the same row.
* **LUT-GEMM** (lookup table): the table holds the partial sums of v activations for every
  weight pattern. **Reads per slice:** int-b weights read once per bit-plane (b reads, b fp16
  adds; one for int1); ternary weights index one table with all v trits (1 read, 1 add).
  * *pre-ignore*: the cost of building the table is ignored. *pre-ignore+symm*: half the
    table is stored and the other half is a sign flip of it; the flip is ignored.
  * **Entries**: int-b: 2^v, or 2^v / 2 with symm. ter: the smallest 2^k ≥ 3^v, or ≥ ⌊3^v / 2⌋
    with symm.
  * *dup*: one table copy per read, one read port each. *multi-port*: one table with one read
    port per read. With one read (int1, ter) the two are the same.
  * *reg*: flip-flop register file (synthesized). *SRAM*: CACTI.
  * **Entry width**: 8 bits for wa = int8, 16 bits for wa = fp16, times bs: one entry holds the
    partial sums of all bs batch rows, so a batch makes entries bs times wider, keeps the
    number of tables and reads, and multiplies the fp16 adds by bs.

| LUT entries | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|
| int-b, pre-ignore | 16 | 64 | 128 | 256 |
| int-b, pre-ignore+symm | 8 | 32 | 64 | 128 |
| ter, pre-ignore | 128 | 1,024 | 4,096 | 8,192 |
| ter, pre-ignore+symm | 64 | 512 | 2,048 | 4,096 |

* **Area** = Σ count × unit area. Adders and multipliers: logic-only area of `u_core` from
  pe_sweep. Reg LUT: the whole `u_buf` (flops, address decode, read mux, clock gating).
  SRAM LUT: CACTI area.
* **Power** = Σ count × unit power, every unit busy every cycle. **LUT power is read-only**:
  for SRAM, leakage + 500 MHz × E_read per read port; for reg, not measured yet (`#`).
* **Not counted:** table precompute, the sign flip, the 2^b weighting between bit-planes, and
  any int → fp conversion.

## Unit costs used

Only primitives with at least one number; the rest are in *Missing data*.

| Primitive | Area (µm²) | Power (mW) | Source |
|---|---|---|---|
| `add_fp16` | 515.1 | 1.530 | `add_fp16`, logic only |
| `add_int16` | 32.8 | 0.053 | `add_int16`, logic only |
| `mul_fp16` | 383.7 | 1.064 | `mul_fp16`, logic only |
| `mul_int8` | 142.3 | 0.244 | `mul_int8`, logic only |
| `reg_lut_n8_w16_r1` | 357.2 | # | `buffer_n8` (synthesized u_buf) |
| `reg_lut_n16_w16_r1` | 682.5 | # | `buffer_n16` (synthesized u_buf) |
| `reg_lut_n32_w16_r1` | 1,339.8 | # | `buffer_n32` (synthesized u_buf) |
| `reg_lut_n64_w16_r1` | 2,630.9 | # | `buffer_n64` (synthesized u_buf) |
| `reg_lut_n128_w16_r1` | 5,193.5 | # | `buffer_n128` (synthesized u_buf) |
| `reg_lut_n256_w16_r1` | 10,386.1 | # | `buffer_n256` (synthesized u_buf) |
| `sram_lut_n32_w16_r1` | 139.7 | 0.110 | CACTI 1RW, N = 32: leakage + 500 MHz × E_read |
| `sram_lut_n64_w16_r1` | 242.3 | 0.172 | CACTI 1RW, N = 64: leakage + 500 MHz × E_read |
| `sram_lut_n128_w16_r1` | 451.8 | 0.293 | CACTI 1RW, N = 128: leakage + 500 MHz × E_read |
| `sram_lut_n256_w16_r1` | 790.1 | 0.469 | CACTI 1RW, N = 256: leakage + 500 MHz × E_read |

## Notes

1. **Reg LUT power is `#` everywhere.** The buffer sweep measured 80% reads / 20% writes; a
   LUT is read-only during the GEMM. When a read-only run is added, check the clock
   transition too: the flow's 5 ns setting inflates flip-flop power (on `buffer_n4`, 0.05 ns
   cut `u_buf` power from 0.375 to 0.153 mW; buffer REPORT note 2).
2. **SRAM read-only power** is a few percent under the 80/20 number the earlier version used
   (N = 32: 0.110 vs 0.114 mW; N = 256: 0.469 vs 0.482 mW), because CACTI's write energy is
   higher than its read energy.
3. **8-bit entries for wa = int8.** An exact partial sum of v int8 activations needs
   8 + ⌈log2 v⌉ bits (11 at v = 8), so 8-bit entries assume the partial sums are requantized.
   The adds stay fp16, as specified.
4. **MAC opt with wa = int8 excludes the converter**, as specified. It is not what made the
   pe_sweep MAC large: inside `mac_mulint8_addfp16` the converter's cells are 272 µm² of
   1,763 µm², and most of the rest is upsizing to close timing in one cycle
   ([02](../02-int-to-fp-converter-cost/README.md)).
5. **Ternary tables are large**: 128, 1,024, 4,096, 8,192 entries
   at v = 4, 6, 7, 8 (half with symm), so most ternary LUT cells need tables
   beyond the 256-entry sweep.
6. **fp16 units close timing at ~0 ps slack** (`mul_fp16` 0 ps,
   `add_fp16` 1 ps), so their area includes upsizing.
