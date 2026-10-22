# 01 — MAC-GEMM vs LUT-GEMM cost per quantization frame

Generated 2026-10-22 by `make_tables.py` from [`../results/`](../results/) (the cmp00 sweep
snapshot; see [`../README.md`](../README.md)). Edit the script, not this file.

**Tables, one file per batch size: [bs = 1](tables-bs1.md) · [bs = 2](tables-bs2.md) · [bs = 4](tables-bs4.md) · [bs = 8](tables-bs8.md).** Each file has one table per frame
(wq ∈ {int1, ter, int2, int3, int4, int6, int8} × wa ∈ {int8, fp16}), one row per method and one column per
v. **Cell: area (µm²) / power (mW)** at 500 MHz, for hardware that consumes one v-element
slice of a dot product for every batch row each cycle. Power × 2 = energy per cycle in pJ.
`#` = no data yet. `*` = upper bound: an SRAM table CACTI cannot model (under 64 bytes, or N = 8, 16), costed as the smallest modelled table of the same width and ports; or register-file power from a 5 ns clock-transition run whose 0.1 ns rerun is not done yet. `—` = not costed: ternary register-file tables above v = 6. `#` and `*` apply to area and power separately.

## Missing data

| Data | Missing | Configurations | Why |
|---|---|---|---|
| Reg LUT, 1 read port | area + power | W = 20: N = 8, 16, 64, 128<br>W = 22: N = 32, 64, 128, 256, 512, 1024<br>W = 32: N = 8, 16, 32, 64, 128, 256, 512, 1024<br>W = 40: N = 8, 16, 64, 128<br>W = 44: N = 32, 64, 128, 256, 512, 1024<br>W = 64: N = 8, 16, 32, 64, 128, 256, 512, 1024<br>W = 80: N = 8, 16, 64, 128<br>W = 88: N = 32, 64, 128, 256, 512, 1024<br>W = 128: N = 8, 16, 32, 64, 128, 256, 512, 1024 | no run in this snapshot; queue state in [`mac_lut_status.md`](../results/todo/mac_lut_status.md) |
| Reg LUT, wq read ports | area + power | W = 16: N = 128, 256, R = 8<br>W = 20: N = 8, 16, R = 2/3/4/6/8<br>W = 22: N = 32, 64, 128, 256, R = 2/3/4/6/8<br>W = 32: N = 8, 16, 32, 64, 128, 256, R = 2/3/4/6/8<br>W = 40: N = 8, 16, R = 2/3/4/6/8<br>W = 44: N = 32, 64, 128, 256, R = 2/3/4/6/8<br>W = 64: N = 8, 16, 32, 64, 128, 256, R = 2/3/4/6/8<br>W = 80: N = 8, 16, R = 2/3/4/6/8<br>W = 88: N = 32, 64, 128, 256, R = 2/3/4/6/8<br>W = 128: N = 8, 16, 32, 64, 128, 256, R = 2/3/4/6/8 | no run in this snapshot; queue state in [`mac_lut_status.md`](../results/todo/mac_lut_status.md) |

The data is being collected on cmp00; the snapshot of its plan and status is in
[`../results/todo/`](../results/todo/).

## Methods and cost model

* **wq**: weight format: int1, ter, int2, int3, int4, int6, int8. int-b = b-bit integer; **ter** = ternary
  {−1, 0, +1}. **wa**: activation format (int8 or fp16). **v**: vector length, the number of
  activations combined per step. **bs**: batch size (1, 2, 4, 8).
* **MAC-GEMM**: bs·v multipliers and bs·v adders (a batch of bs needs bs times the resources).
  * *fp16*: v × fp16 mul + v × fp16 add.
  * *opt*: v × (int-wq × wa) mul + v × fp16 add. int × fp16 multipliers output fp16. The
    int → fp16 conversion that wa = int8 needs is not counted (note 5).
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
    port per read (plus one write port). With one read (int1, ter) the two are the same.
  * **Entry width** per batch row: 16 bits for wa = fp16; 8 + ⌈log2 v⌉ bits for wa = int8,
    which holds the exact sum of v int8 activations
    (10 bits at v = 4, 11 bits at v = 6, 11 bits at v = 7, 11 bits at v = 8). Times bs: one entry
    holds the partial sums of all bs batch rows, so a batch makes entries bs times wider, keeps
    the number of tables and reads, and multiplies the fp16 adds by bs.
  * *reg*: flip-flop register file (synthesized) at the exact entry width. Ternary
    register-file tables are costed only up to v = 6 (`—` above).
  * *SRAM*: CACTI, which sizes entries in whole bytes, so widths round up
    (10 → 16, 11 → 16, 20 → 24, 22 → 24, 44 → 48 bits).

| LUT entries | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|
| int-b, pre-ignore | 16 | 64 | 128 | 256 |
| int-b, pre-ignore+symm | 8 | 32 | 64 | 128 |
| ter, pre-ignore | 128 | 1,024 | 4,096 | 8,192 |
| ter, pre-ignore+symm | 64 | 512 | 2,048 | 4,096 |

* **Area** = Σ count × unit area. Adders, multipliers: logic-only area of `u_core` from
  pe_sweep. Register file: the whole `u_buf` (flops, address decode, read muxes, clock gating).
  SRAM: CACTI area.
* **Power** = Σ count × unit power, every unit busy every cycle. **LUT power is read-only**:
  register files, Genus vectorless power with writes held at 0; SRAM, CACTI leakage +
  R × 500 MHz × E_read.
* **Not counted:** table precompute, the sign flip, the 2^b weighting between bit-planes, and
  any int → fp conversion.

## Unit costs used

Only primitives with at least one number; the rest are in *Missing data*.

| Primitive | Area (µm²) | Power (mW) | Source |
|---|---|---|---|
| `add_fp16` | 515.1 | 1.530 | `add_fp16`, logic only |
| `add_int16` | 32.8 | 0.053 | `add_int16`, logic only |
| `mul_fp16` | 383.7 | 1.064 | `mul_fp16`, logic only |
| `mul_int2xfp16` | 37.9 | 0.100 | `mul_int2xfp16`, logic only |
| `mul_int2xint8` | 33.5 | 0.093 | `mul_int2xint8`, logic only |
| `mul_int3xfp16` | 172.9 | 0.522 | `mul_int3xfp16`, logic only |
| `mul_int3xint8` | 47.2 | 0.108 | `mul_int3xint8`, logic only |
| `mul_int4xfp16` | 224.9 | 0.746 | `mul_int4xfp16`, logic only |
| `mul_int4xint8` | 64.1 | 0.118 | `mul_int4xint8`, logic only |
| `mul_int6xfp16` | 336.0 | 0.932 | `mul_int6xfp16`, logic only |
| `mul_int6xint8` | 104.2 | 0.184 | `mul_int6xint8`, logic only |
| `mul_int8` | 142.3 | 0.244 | `mul_int8`, logic only |
| `mul_int8xfp16` | 423.5 | 1.155 | `mul_int8xfp16`, logic only |
| `reg_lut_n8_w10_r1` | 233.9 | 0.245* | `buffer_n8_w10`, 5.0 ns clock transition |
| `reg_lut_n16_w10_r1` | 447.0 | 0.315* | `buffer_n16_w10`, 5.0 ns clock transition |
| `reg_lut_n64_w10_r1` | 1,724.8 | 0.677* | `buffer_n64_w10`, 5.0 ns clock transition |
| `reg_lut_n128_w10_r1` | 3,394.3 | 1.076* | `buffer_n128_w10`, 5.0 ns clock transition |
| `reg_lut_n8_w10_r2` | 296.5 | 0.448* | `buffer1w2r_n8_w10`, 5.0 ns clock transition |
| `reg_lut_n16_w10_r2` | 551.1 | 0.542* | `buffer1w2r_n16_w10`, 5.0 ns clock transition |
| `reg_lut_n8_w10_r3` | 358.3 | 0.654* | `buffer1w3r_n8_w10`, 5.0 ns clock transition |
| `reg_lut_n16_w10_r3` | 653.3 | 0.772* | `buffer1w3r_n16_w10`, 5.0 ns clock transition |
| `reg_lut_n8_w10_r4` | 419.6 | 0.382 | `buffer1w4r_n8_w10`, 0.1 ns clock transition |
| `reg_lut_n16_w10_r4` | 755.2 | 0.541 | `buffer1w4r_n16_w10`, 0.1 ns clock transition |
| `reg_lut_n8_w10_r6` | 543.1 | 0.554 | `buffer1w6r_n8_w10`, 0.1 ns clock transition |
| `reg_lut_n16_w10_r6` | 960.4 | 0.772 | `buffer1w6r_n16_w10`, 0.1 ns clock transition |
| `reg_lut_n8_w10_r8` | 666.5 | 0.726 | `buffer1w8r_n8_w10`, 0.1 ns clock transition |
| `reg_lut_n16_w10_r8` | 1,156.0 | 0.993 | `buffer1w8r_n16_w10`, 0.1 ns clock transition |
| `reg_lut_n32_w11_r1` | 957.9 | 0.502* | `buffer_n32_w11`, 5.0 ns clock transition |
| `reg_lut_n64_w11_r1` | 1,875.6 | 0.730* | `buffer_n64_w11`, 5.0 ns clock transition |
| `reg_lut_n128_w11_r1` | 3,694.2 | 1.164* | `buffer_n128_w11`, 5.0 ns clock transition |
| `reg_lut_n256_w11_r1` | 7,387.9 | 2.818* | `buffer_n256_w11`, 5.0 ns clock transition |
| `reg_lut_n512_w11_r1` | 14,782.1 | 5.430* | `buffer_n512_w11`, 5.0 ns clock transition |
| `reg_lut_n1024_w11_r1` | 29,508.9 | 10.453* | `buffer_n1024_w11`, 5.0 ns clock transition |
| `reg_lut_n32_w11_r2` | 1,163.0 | 0.786* | `buffer1w2r_n32_w11`, 5.0 ns clock transition |
| `reg_lut_n64_w11_r2` | 2,248.3 | 1.047* | `buffer1w2r_n64_w11`, 5.0 ns clock transition |
| `reg_lut_n128_w11_r2` | 4,397.1 | 1.528* | `buffer1w2r_n128_w11`, 5.0 ns clock transition |
| `reg_lut_n256_w11_r2` | 8,791.6 | 3.247* | `buffer1w2r_n256_w11`, 5.0 ns clock transition |
| `reg_lut_n32_w11_r3` | 1,365.1 | 1.066* | `buffer1w3r_n32_w11`, 5.0 ns clock transition |
| `reg_lut_n64_w11_r3` | 2,622.8 | 1.369* | `buffer1w3r_n64_w11`, 5.0 ns clock transition |
| `reg_lut_n128_w11_r3` | 5,103.5 | 1.899* | `buffer1w3r_n128_w11`, 5.0 ns clock transition |
| `reg_lut_n256_w11_r3` | 10,158.9 | 3.369 | `buffer1w3r_n256_w11`, 0.1 ns clock transition |
| `reg_lut_n32_w11_r4` | 1,553.2 | 0.847 | `buffer1w4r_n32_w11`, 0.1 ns clock transition |
| `reg_lut_n64_w11_r4` | 2,970.3 | 1.214 | `buffer1w4r_n64_w11`, 0.1 ns clock transition |
| `reg_lut_n128_w11_r4` | 5,796.4 | 1.826 | `buffer1w4r_n128_w11`, 0.1 ns clock transition |
| `reg_lut_n256_w11_r4` | 11,548.2 | 3.696 | `buffer1w4r_n256_w11`, 0.1 ns clock transition |
| `reg_lut_n32_w11_r6` | 1,951.9 | 1.162 | `buffer1w6r_n32_w11`, 0.1 ns clock transition |
| `reg_lut_n64_w11_r6` | 3,701.5 | 1.613 | `buffer1w6r_n64_w11`, 0.1 ns clock transition |
| `reg_lut_n128_w11_r6` | 7,201.0 | 2.342 | `buffer1w6r_n128_w11`, 0.1 ns clock transition |
| `reg_lut_n256_w11_r6` | 14,331.9 | 4.350 | `buffer1w6r_n256_w11`, 0.1 ns clock transition |
| `reg_lut_n32_w11_r8` | 2,340.8 | 1.458 | `buffer1w8r_n32_w11`, 0.1 ns clock transition |
| `reg_lut_n64_w11_r8` | 4,436.5 | 2.017 | `buffer1w8r_n64_w11`, 0.1 ns clock transition |
| `reg_lut_n128_w11_r8` | 8,603.7 | 2.860 | `buffer1w8r_n128_w11`, 0.1 ns clock transition |
| `reg_lut_n256_w11_r8` | 17,125.2 | 5.017 | `buffer1w8r_n256_w11`, 0.1 ns clock transition |
| `reg_lut_n8_w16_r1` | 357.2 | 0.382* | `buffer_n8`, 5.0 ns clock transition |
| `reg_lut_n16_w16_r1` | 682.5 | 0.474* | `buffer_n16`, 5.0 ns clock transition |
| `reg_lut_n32_w16_r1` | 1,339.8 | 0.681* | `buffer_n32`, 5.0 ns clock transition |
| `reg_lut_n64_w16_r1` | 2,630.9 | 0.979* | `buffer_n64`, 5.0 ns clock transition |
| `reg_lut_n128_w16_r1` | 5,193.5 | 1.550* | `buffer_n128`, 5.0 ns clock transition |
| `reg_lut_n256_w16_r1` | 10,386.1 | 3.860* | `buffer_n256`, 5.0 ns clock transition |
| `reg_lut_n512_w16_r1` | 20,758.1 | 7.374* | `buffer_n512`, 5.0 ns clock transition |
| `reg_lut_n1024_w16_r1` | 41,461.2 | 14.247* | `buffer_n1024`, 5.0 ns clock transition |
| `reg_lut_n8_w16_r2` | 452.3 | 0.719* | `buffer1w2r_n8`, 5.0 ns clock transition |
| `reg_lut_n16_w16_r2` | 841.9 | 0.830* | `buffer1w2r_n16`, 5.0 ns clock transition |
| `reg_lut_n32_w16_r2` | 1,627.8 | 1.082* | `buffer1w2r_n32`, 5.0 ns clock transition |
| `reg_lut_n64_w16_r2` | 3,153.8 | 1.414* | `buffer1w2r_n64`, 5.0 ns clock transition |
| `reg_lut_n128_w16_r2` | 6,186.3 | 2.022* | `buffer1w2r_n128`, 5.0 ns clock transition |
| `reg_lut_n256_w16_r2` | 12,359.2 | 4.418* | `buffer1w2r_n256`, 5.0 ns clock transition |
| `reg_lut_n8_w16_r3` | 546.1 | 0.482 | `buffer1w3r_n8`, 0.1 ns clock transition |
| `reg_lut_n16_w16_r3` | 1,000.2 | 0.636 | `buffer1w3r_n16`, 0.1 ns clock transition |
| `reg_lut_n32_w16_r3` | 1,895.3 | 0.925 | `buffer1w3r_n32`, 0.1 ns clock transition |
| `reg_lut_n64_w16_r3` | 3,655.8 | 1.339 | `buffer1w3r_n64`, 0.1 ns clock transition |
| `reg_lut_n128_w16_r3` | 7,173.4 | 2.064 | `buffer1w3r_n128`, 0.1 ns clock transition |
| `reg_lut_n256_w16_r3` | 14,306.5 | 4.544 | `buffer1w3r_n256`, 0.1 ns clock transition |
| `reg_lut_n8_w16_r4` | 640.3 | 0.625 | `buffer1w4r_n8`, 0.1 ns clock transition |
| `reg_lut_n16_w16_r4` | 1,157.7 | 0.809 | `buffer1w4r_n16`, 0.1 ns clock transition |
| `reg_lut_n32_w16_r4` | 2,173.9 | 1.134 | `buffer1w4r_n32`, 0.1 ns clock transition |
| `reg_lut_n64_w16_r4` | 4,171.4 | 1.611 | `buffer1w4r_n64`, 0.1 ns clock transition |
| `reg_lut_n128_w16_r4` | 8,165.7 | 2.403 | `buffer1w4r_n128`, 0.1 ns clock transition |
| `reg_lut_n256_w16_r4` | 16,276.8 | 4.956 | `buffer1w4r_n256`, 0.1 ns clock transition |
| `reg_lut_n8_w16_r6` | 828.8 | 0.911 | `buffer1w6r_n8`, 0.1 ns clock transition |
| `reg_lut_n16_w16_r6` | 1,472.7 | 1.154 | `buffer1w6r_n16`, 0.1 ns clock transition |
| `reg_lut_n32_w16_r6` | 2,730.9 | 1.547 | `buffer1w6r_n32`, 0.1 ns clock transition |
| `reg_lut_n64_w16_r6` | 5,204.2 | 2.138 | `buffer1w6r_n64`, 0.1 ns clock transition |
| `reg_lut_n128_w16_r6` | 10,150.3 | 3.080 | `buffer1w6r_n128`, 0.1 ns clock transition |
| `reg_lut_n256_w16_r6` | 20,209.3 | 5.790 | `buffer1w6r_n256`, 0.1 ns clock transition |
| `reg_lut_n8_w16_r8` | 1,017.3 | 1.198 | `buffer1w8r_n8`, 0.1 ns clock transition |
| `reg_lut_n16_w16_r8` | 1,787.7 | 1.500 | `buffer1w8r_n16`, 0.1 ns clock transition |
| `reg_lut_n32_w16_r8` | 3,287.7 | 1.965 | `buffer1w8r_n32`, 0.1 ns clock transition |
| `reg_lut_n64_w16_r8` | 6,237.5 | 2.673 | `buffer1w8r_n64`, 0.1 ns clock transition |
| `sram_lut_n8_w16_r1` | 139.7* | 0.110* | CACTI, 2 B/entry; N = 32 stands in |
| `sram_lut_n16_w16_r1` | 139.7* | 0.110* | CACTI, 2 B/entry; N = 32 stands in |
| `sram_lut_n32_w16_r1` | 139.7 | 0.110 | CACTI, 2 B/entry |
| `sram_lut_n64_w16_r1` | 242.3 | 0.172 | CACTI, 2 B/entry |
| `sram_lut_n128_w16_r1` | 451.8 | 0.293 | CACTI, 2 B/entry |
| `sram_lut_n256_w16_r1` | 790.1 | 0.469 | CACTI, 2 B/entry |
| `sram_lut_n512_w16_r1` | 1,566.8 | 0.811 | CACTI, 2 B/entry |
| `sram_lut_n1024_w16_r1` | 2,779.9 | 1.429 | CACTI, 2 B/entry |
| `sram_lut_n2048_w16_r1` | 5,595.4 | 3.142 | CACTI, 2 B/entry |
| `sram_lut_n4096_w16_r1` | 14,105.0 | 5.258 | CACTI, 2 B/entry |
| `sram_lut_n8192_w16_r1` | 23,844.0 | 9.436 | CACTI, 2 B/entry |
| `sram_lut_n8_w16_r2` | 499.2* | 0.229* | CACTI, 2 B/entry; N = 32 stands in |
| `sram_lut_n16_w16_r2` | 499.2* | 0.229* | CACTI, 2 B/entry; N = 32 stands in |
| `sram_lut_n32_w16_r2` | 499.2 | 0.229 | CACTI, 2 B/entry |
| `sram_lut_n64_w16_r2` | 896.3 | 0.311 | CACTI, 2 B/entry |
| `sram_lut_n128_w16_r2` | 1,536.3 | 0.512 | CACTI, 2 B/entry |
| `sram_lut_n256_w16_r2` | 2,828.5 | 0.848 | CACTI, 2 B/entry |
| `sram_lut_n8_w16_r3` | 757.8* | 0.336* | CACTI, 2 B/entry; N = 32 stands in |
| `sram_lut_n16_w16_r3` | 757.8* | 0.336* | CACTI, 2 B/entry; N = 32 stands in |
| `sram_lut_n32_w16_r3` | 757.8 | 0.336 | CACTI, 2 B/entry |
| `sram_lut_n64_w16_r3` | 1,373.4 | 0.438 | CACTI, 2 B/entry |
| `sram_lut_n128_w16_r3` | 2,336.9 | 0.726 | CACTI, 2 B/entry |
| `sram_lut_n256_w16_r3` | 4,289.8 | 1.168 | CACTI, 2 B/entry |
| `sram_lut_n8_w16_r4` | 1,067.9* | 0.455* | CACTI, 2 B/entry; N = 32 stands in |
| `sram_lut_n16_w16_r4` | 1,067.9* | 0.455* | CACTI, 2 B/entry; N = 32 stands in |
| `sram_lut_n32_w16_r4` | 1,067.9 | 0.455 | CACTI, 2 B/entry |
| `sram_lut_n64_w16_r4` | 1,954.2 | 0.579 | CACTI, 2 B/entry |
| `sram_lut_n128_w16_r4` | 3,312.0 | 0.965 | CACTI, 2 B/entry |
| `sram_lut_n256_w16_r4` | 6,050.8 | 1.529 | CACTI, 2 B/entry |
| `sram_lut_n8_w16_r6` | 1,856.0* | 0.734* | CACTI, 2 B/entry; N = 32 stands in |
| `sram_lut_n16_w16_r6` | 1,856.0* | 0.734* | CACTI, 2 B/entry; N = 32 stands in |
| `sram_lut_n32_w16_r6` | 1,856.0 | 0.734 | CACTI, 2 B/entry |
| `sram_lut_n64_w16_r6` | 3,390.9 | 0.910 | CACTI, 2 B/entry |
| `sram_lut_n128_w16_r6` | 5,716.6 | 1.528 | CACTI, 2 B/entry |
| `sram_lut_n256_w16_r6` | 11,642.9 | 2.925 | CACTI, 2 B/entry |
| `sram_lut_n8_w16_r8` | 2,845.6* | 1.058* | CACTI, 2 B/entry; N = 32 stands in |
| `sram_lut_n16_w16_r8` | 2,845.6* | 1.058* | CACTI, 2 B/entry; N = 32 stands in |
| `sram_lut_n32_w16_r8` | 2,845.6 | 1.058 | CACTI, 2 B/entry |
| `sram_lut_n64_w16_r8` | 5,171.5 | 1.296 | CACTI, 2 B/entry |
| `sram_lut_n128_w16_r8` | 9,090.4 | 2.371 | CACTI, 2 B/entry |
| `sram_lut_n256_w16_r8` | 17,695.0 | 4.190 | CACTI, 2 B/entry |
| `sram_lut_n8_w24_r1` | 211.4* | 0.161* | CACTI, 3 B/entry; N = 32 stands in |
| `sram_lut_n16_w24_r1` | 211.4* | 0.161* | CACTI, 3 B/entry; N = 32 stands in |
| `sram_lut_n32_w24_r1` | 211.4 | 0.161 | CACTI, 3 B/entry |
| `sram_lut_n64_w24_r1` | 348.9 | 0.243 | CACTI, 3 B/entry |
| `sram_lut_n128_w24_r1` | 632.1 | 0.404 | CACTI, 3 B/entry |
| `sram_lut_n256_w24_r1` | 1,116.3 | 0.654 | CACTI, 3 B/entry |
| `sram_lut_n512_w24_r1` | 2,158.3 | 1.137 | CACTI, 3 B/entry |
| `sram_lut_n1024_w24_r1` | 4,378.9 | 2.466 | CACTI, 3 B/entry |
| `sram_lut_n2048_w24_r1` | 8,303.4 | 4.531 | CACTI, 3 B/entry |
| `sram_lut_n4096_w24_r1` | 19,022.2 | 7.428 | CACTI, 3 B/entry |
| `sram_lut_n8192_w24_r1` | 36,172.6 | 16.173 | CACTI, 3 B/entry |
| `sram_lut_n8_w24_r2` | 756.4* | 0.340* | CACTI, 3 B/entry; N = 32 stands in |
| `sram_lut_n16_w24_r2` | 756.4* | 0.340* | CACTI, 3 B/entry; N = 32 stands in |
| `sram_lut_n32_w24_r2` | 756.4 | 0.340 | CACTI, 3 B/entry |
| `sram_lut_n64_w24_r2` | 1,282.9 | 0.456 | CACTI, 3 B/entry |
| `sram_lut_n128_w24_r2` | 2,360.5 | 0.736 | CACTI, 3 B/entry |
| `sram_lut_n256_w24_r2` | 3,981.5 | 1.207 | CACTI, 3 B/entry |
| `sram_lut_n8_w24_r3` | 1,158.9* | 0.506* | CACTI, 3 B/entry; N = 32 stands in |
| `sram_lut_n16_w24_r3` | 1,158.9* | 0.506* | CACTI, 3 B/entry; N = 32 stands in |
| `sram_lut_n32_w24_r3` | 1,158.9 | 0.506 | CACTI, 3 B/entry |
| `sram_lut_n64_w24_r3` | 1,970.7 | 0.654 | CACTI, 3 B/entry |
| `sram_lut_n128_w24_r3` | 3,606.9 | 1.023 | CACTI, 3 B/entry |
| `sram_lut_n256_w24_r3` | 6,054.6 | 1.684 | CACTI, 3 B/entry |
| `sram_lut_n8_w24_r4` | 1,642.4* | 0.693* | CACTI, 3 B/entry; N = 32 stands in |
| `sram_lut_n16_w24_r4` | 1,642.4* | 0.693* | CACTI, 3 B/entry; N = 32 stands in |
| `sram_lut_n32_w24_r4` | 1,642.4 | 0.693 | CACTI, 3 B/entry |
| `sram_lut_n64_w24_r4` | 2,805.3 | 0.875 | CACTI, 3 B/entry |
| `sram_lut_n128_w24_r4` | 5,391.5 | 1.589 | CACTI, 3 B/entry |
| `sram_lut_n256_w24_r4` | 9,130.5 | 2.469 | CACTI, 3 B/entry |
| `sram_lut_n8_w24_r6` | 2,867.8* | 1.132* | CACTI, 3 B/entry; N = 32 stands in |
| `sram_lut_n16_w24_r6` | 2,867.8* | 1.132* | CACTI, 3 B/entry; N = 32 stands in |
| `sram_lut_n32_w24_r6` | 2,867.8 | 1.132 | CACTI, 3 B/entry |
| `sram_lut_n64_w24_r6` | 4,881.7 | 1.397 | CACTI, 3 B/entry |
| `sram_lut_n128_w24_r6` | 9,153.5 | 2.517 | CACTI, 3 B/entry |
| `sram_lut_n256_w24_r6` | 15,419.5 | 3.814 | CACTI, 3 B/entry |
| `sram_lut_n8_w24_r8` | 4,414.5* | 1.663* | CACTI, 3 B/entry; N = 32 stands in |
| `sram_lut_n16_w24_r8` | 4,414.5* | 1.663* | CACTI, 3 B/entry; N = 32 stands in |
| `sram_lut_n32_w24_r8` | 4,414.5 | 1.663 | CACTI, 3 B/entry |
| `sram_lut_n64_w24_r8` | 7,476.8 | 2.025 | CACTI, 3 B/entry |
| `sram_lut_n128_w24_r8` | 13,790.3 | 3.631 | CACTI, 3 B/entry |
| `sram_lut_n256_w24_r8` | 23,221.6 | 5.426 | CACTI, 3 B/entry |
| `sram_lut_n8_w32_r1` | 284.9* | 0.203* | CACTI, 4 B/entry; N = 32 stands in |
| `sram_lut_n16_w32_r1` | 284.9* | 0.203* | CACTI, 4 B/entry; N = 32 stands in |
| `sram_lut_n32_w32_r1` | 284.9 | 0.203 | CACTI, 4 B/entry |
| `sram_lut_n64_w32_r1` | 458.5 | 0.302 | CACTI, 4 B/entry |
| `sram_lut_n128_w32_r1` | 809.3 | 0.493 | CACTI, 4 B/entry |
| `sram_lut_n256_w32_r1` | 1,587.6 | 0.836 | CACTI, 4 B/entry |
| `sram_lut_n512_w32_r1` | 2,809.8 | 1.462 | CACTI, 4 B/entry |
| `sram_lut_n1024_w32_r1` | 5,662.9 | 3.188 | CACTI, 4 B/entry |
| `sram_lut_n2048_w32_r1` | 11,071.0 | 5.913 | CACTI, 4 B/entry |
| `sram_lut_n4096_w32_r1` | 24,503.6 | 9.607 | CACTI, 4 B/entry |
| `sram_lut_n8192_w32_r1` | 53,134.7 | 19.763 | CACTI, 4 B/entry |
| `sram_lut_n8_w32_r2` | 1,025.6* | 0.438* | CACTI, 4 B/entry; N = 32 stands in |
| `sram_lut_n16_w32_r2` | 1,025.6* | 0.438* | CACTI, 4 B/entry; N = 32 stands in |
| `sram_lut_n32_w32_r2` | 1,025.6 | 0.438 | CACTI, 4 B/entry |
| `sram_lut_n64_w32_r2` | 1,660.3 | 0.582 | CACTI, 4 B/entry |
| `sram_lut_n128_w32_r2` | 2,959.7 | 0.917 | CACTI, 4 B/entry |
| `sram_lut_n256_w32_r2` | 5,738.7 | 1.803 | CACTI, 4 B/entry |
| `sram_lut_n8_w32_r3` | 1,564.3* | 0.662* | CACTI, 4 B/entry; N = 32 stands in |
| `sram_lut_n16_w32_r3` | 1,564.3* | 0.662* | CACTI, 4 B/entry; N = 32 stands in |
| `sram_lut_n32_w32_r3` | 1,564.3 | 0.662 | CACTI, 4 B/entry |
| `sram_lut_n64_w32_r3` | 2,545.8 | 0.846 | CACTI, 4 B/entry |
| `sram_lut_n128_w32_r3` | 4,511.3 | 1.288 | CACTI, 4 B/entry |
| `sram_lut_n256_w32_r3` | 8,668.4 | 2.488 | CACTI, 4 B/entry |
| `sram_lut_n8_w32_r4` | 2,222.6* | 0.916* | CACTI, 4 B/entry; N = 32 stands in |
| `sram_lut_n16_w32_r4` | 2,222.6* | 0.916* | CACTI, 4 B/entry; N = 32 stands in |
| `sram_lut_n32_w32_r4` | 2,222.6 | 0.916 | CACTI, 4 B/entry |
| `sram_lut_n64_w32_r4` | 3,622.2 | 1.145 | CACTI, 4 B/entry |
| `sram_lut_n128_w32_r4` | 6,380.7 | 1.709 | CACTI, 4 B/entry |
| `sram_lut_n256_w32_r4` | 12,171.7 | 3.263 | CACTI, 4 B/entry |
| `sram_lut_n8_w32_r6` | 3,889.4* | 1.520* | CACTI, 4 B/entry; N = 32 stands in |
| `sram_lut_n16_w32_r6` | 3,889.4* | 1.520* | CACTI, 4 B/entry; N = 32 stands in |
| `sram_lut_n32_w32_r6` | 3,889.4 | 1.520 | CACTI, 4 B/entry |
| `sram_lut_n64_w32_r6` | 6,307.9 | 1.855 | CACTI, 4 B/entry |
| `sram_lut_n128_w32_r6` | 11,064.7 | 2.709 | CACTI, 4 B/entry |
| `sram_lut_n256_w32_r6` | 20,870.9 | 5.103 | CACTI, 4 B/entry |
| `sram_lut_n8_w32_r8` | 6,663.1* | 2.369* | CACTI, 4 B/entry; N = 32 stands in |
| `sram_lut_n16_w32_r8` | 6,663.1* | 2.369* | CACTI, 4 B/entry; N = 32 stands in |
| `sram_lut_n32_w32_r8` | 6,663.1 | 2.369 | CACTI, 4 B/entry |
| `sram_lut_n64_w32_r8` | 10,080.4 | 2.885 | CACTI, 4 B/entry |
| `sram_lut_n128_w32_r8` | 16,995.8 | 4.201 | CACTI, 4 B/entry |
| `sram_lut_n256_w32_r8` | 31,812.1 | 7.334 | CACTI, 4 B/entry |
| `sram_lut_n8_w40_r1` | 367.5* | 0.256* | CACTI, 5 B/entry; N = 32 stands in |
| `sram_lut_n16_w40_r1` | 367.5* | 0.256* | CACTI, 5 B/entry; N = 32 stands in |
| `sram_lut_n64_w40_r1` | 579.1 | 0.374 | CACTI, 5 B/entry |
| `sram_lut_n128_w40_r1` | 1,000.9 | 0.605 | CACTI, 5 B/entry |
| `sram_lut_n8_w40_r2` | 1,357.4* | 0.560* | CACTI, 5 B/entry; N = 32 stands in |
| `sram_lut_n16_w40_r2` | 1,357.4* | 0.560* | CACTI, 5 B/entry; N = 32 stands in |
| `sram_lut_n8_w40_r3` | 2,073.1* | 0.858* | CACTI, 5 B/entry; N = 32 stands in |
| `sram_lut_n16_w40_r3` | 2,073.1* | 0.858* | CACTI, 5 B/entry; N = 32 stands in |
| `sram_lut_n8_w40_r4` | 2,958.7* | 1.200* | CACTI, 5 B/entry; N = 32 stands in |
| `sram_lut_n16_w40_r4` | 2,958.7* | 1.200* | CACTI, 5 B/entry; N = 32 stands in |
| `sram_lut_n8_w40_r6` | 5,914.1* | 2.128* | CACTI, 5 B/entry; N = 32 stands in |
| `sram_lut_n16_w40_r6` | 5,914.1* | 2.128* | CACTI, 5 B/entry; N = 32 stands in |
| `sram_lut_n8_w40_r8` | 8,994.8* | 3.156* | CACTI, 5 B/entry; N = 32 stands in |
| `sram_lut_n16_w40_r8` | 8,994.8* | 3.156* | CACTI, 5 B/entry; N = 32 stands in |
| `sram_lut_n32_w48_r1` | 441.4 | 0.302 | CACTI, 6 B/entry |
| `sram_lut_n64_w48_r1` | 683.3 | 0.436 | CACTI, 6 B/entry |
| `sram_lut_n128_w48_r1` | 1,161.9 | 0.698 | CACTI, 6 B/entry |
| `sram_lut_n256_w48_r1` | 2,206.3 | 1.181 | CACTI, 6 B/entry |
| `sram_lut_n512_w48_r1` | 4,466.3 | 2.530 | CACTI, 6 B/entry |
| `sram_lut_n1024_w48_r1` | 8,466.9 | 4.625 | CACTI, 6 B/entry |
| `sram_lut_n2048_w48_r1` | 18,119.1 | 8.940 | CACTI, 6 B/entry |
| `sram_lut_n4096_w48_r1` | 36,750.1 | 15.983 | CACTI, 6 B/entry |
| `sram_lut_n8192_w48_r1` | 77,238.5 | 30.566 | CACTI, 6 B/entry |
| `sram_lut_n32_w48_r2` | 1,667.0 | 0.674 | CACTI, 6 B/entry |
| `sram_lut_n64_w48_r2` | 2,519.6 | 0.880 | CACTI, 6 B/entry |
| `sram_lut_n128_w48_r2` | 4,274.9 | 1.339 | CACTI, 6 B/entry |
| `sram_lut_n256_w48_r2` | 8,484.3 | 2.656 | CACTI, 6 B/entry |
| `sram_lut_n32_w48_r3` | 2,557.0 | 1.042 | CACTI, 6 B/entry |
| `sram_lut_n64_w48_r3` | 3,889.4 | 1.308 | CACTI, 6 B/entry |
| `sram_lut_n128_w48_r3` | 6,543.5 | 1.913 | CACTI, 6 B/entry |
| `sram_lut_n256_w48_r3` | 12,887.1 | 3.733 | CACTI, 6 B/entry |
| `sram_lut_n32_w48_r4` | 4,251.1 | 1.549 | CACTI, 6 B/entry |
| `sram_lut_n64_w48_r4` | 6,184.2 | 1.936 | CACTI, 6 B/entry |
| `sram_lut_n128_w48_r4` | 9,923.2 | 2.817 | CACTI, 6 B/entry |
| `sram_lut_n256_w48_r4` | 18,175.0 | 4.972 | CACTI, 6 B/entry |
| `sram_lut_n32_w48_r6` | 7,352.7 | 2.607 | CACTI, 6 B/entry |
| `sram_lut_n64_w48_r6` | 10,601.5 | 3.162 | CACTI, 6 B/entry |
| `sram_lut_n128_w48_r6` | 16,867.4 | 4.459 | CACTI, 6 B/entry |
| `sram_lut_n256_w48_r6` | 31,367.2 | 7.960 | CACTI, 6 B/entry |
| `sram_lut_n32_w48_r8` | 11,234.9 | 3.905 | CACTI, 6 B/entry |
| `sram_lut_n64_w48_r8` | 16,088.8 | 4.660 | CACTI, 6 B/entry |
| `sram_lut_n128_w48_r8` | 25,520.0 | 6.456 | CACTI, 6 B/entry |
| `sram_lut_n256_w48_r8` | 48,026.9 | 11.631 | CACTI, 6 B/entry |
| `sram_lut_n8_w64_r1` | 629.0* | 0.406* | CACTI, 8 B/entry; N = 32 stands in |
| `sram_lut_n16_w64_r1` | 629.0* | 0.406* | CACTI, 8 B/entry; N = 32 stands in |
| `sram_lut_n32_w64_r1` | 629.0 | 0.406 | CACTI, 8 B/entry |
| `sram_lut_n64_w64_r1` | 944.5 | 0.574 | CACTI, 8 B/entry |
| `sram_lut_n128_w64_r1` | 1,562.3 | 0.906 | CACTI, 8 B/entry |
| `sram_lut_n256_w64_r1` | 2,894.8 | 1.529 | CACTI, 8 B/entry |
| `sram_lut_n512_w64_r1` | 5,822.0 | 3.288 | CACTI, 8 B/entry |
| `sram_lut_n1024_w64_r1` | 11,378.5 | 6.082 | CACTI, 8 B/entry |
| `sram_lut_n2048_w64_r1` | 21,246.9 | 11.437 | CACTI, 8 B/entry |
| `sram_lut_n4096_w64_r1` | 48,695.8 | 20.444 | CACTI, 8 B/entry |
| `sram_lut_n8192_w64_r1` | 102,186.5 | 38.876 | CACTI, 8 B/entry |
| `sram_lut_n8_w64_r2` | 2,803.9* | 1.005* | CACTI, 8 B/entry; N = 32 stands in |
| `sram_lut_n16_w64_r2` | 2,803.9* | 1.005* | CACTI, 8 B/entry; N = 32 stands in |
| `sram_lut_n32_w64_r2` | 2,803.9 | 1.005 | CACTI, 8 B/entry |
| `sram_lut_n64_w64_r2` | 3,979.7 | 1.325 | CACTI, 8 B/entry |
| `sram_lut_n128_w64_r2` | 6,307.5 | 2.013 | CACTI, 8 B/entry |
| `sram_lut_n256_w64_r2` | 10,889.8 | 3.256 | CACTI, 8 B/entry |
| `sram_lut_n8_w64_r3` | 4,370.9* | 1.565* | CACTI, 8 B/entry; N = 32 stands in |
| `sram_lut_n16_w64_r3` | 4,370.9* | 1.565* | CACTI, 8 B/entry; N = 32 stands in |
| `sram_lut_n32_w64_r3` | 4,370.9 | 1.565 | CACTI, 8 B/entry |
| `sram_lut_n64_w64_r3` | 6,140.6 | 1.972 | CACTI, 8 B/entry |
| `sram_lut_n128_w64_r3` | 9,615.6 | 2.859 | CACTI, 8 B/entry |
| `sram_lut_n256_w64_r3` | 16,480.6 | 4.443 | CACTI, 8 B/entry |
| `sram_lut_n8_w64_r4` | 6,272.1* | 2.219* | CACTI, 8 B/entry; N = 32 stands in |
| `sram_lut_n16_w64_r4` | 6,272.1* | 2.219* | CACTI, 8 B/entry; N = 32 stands in |
| `sram_lut_n32_w64_r4` | 6,272.1 | 2.219 | CACTI, 8 B/entry |
| `sram_lut_n64_w64_r4` | 8,757.0 | 2.722 | CACTI, 8 B/entry |
| `sram_lut_n128_w64_r4` | 13,589.7 | 3.834 | CACTI, 8 B/entry |
| `sram_lut_n256_w64_r4` | 23,174.9 | 5.801 | CACTI, 8 B/entry |
| `sram_lut_n8_w64_r6` | 11,065.3* | 3.822* | CACTI, 8 B/entry; N = 32 stands in |
| `sram_lut_n16_w64_r6` | 11,065.3* | 3.822* | CACTI, 8 B/entry; N = 32 stands in |
| `sram_lut_n32_w64_r6` | 11,065.3 | 3.822 | CACTI, 8 B/entry |
| `sram_lut_n64_w64_r6` | 15,295.6 | 4.549 | CACTI, 8 B/entry |
| `sram_lut_n128_w64_r6` | 23,505.7 | 6.189 | CACTI, 8 B/entry |
| `sram_lut_n256_w64_r6` | 39,841.7 | 9.046 | CACTI, 8 B/entry |
| `sram_lut_n8_w64_r8` | 17,154.3* | 5.819* | CACTI, 8 B/entry; N = 32 stands in |
| `sram_lut_n16_w64_r8` | 17,154.3* | 5.819* | CACTI, 8 B/entry; N = 32 stands in |
| `sram_lut_n32_w64_r8` | 17,154.3 | 5.819 | CACTI, 8 B/entry |
| `sram_lut_n64_w64_r8` | 23,548.4 | 6.812 | CACTI, 8 B/entry |
| `sram_lut_n128_w64_r8` | 36,029.5 | 9.083 | CACTI, 8 B/entry |
| `sram_lut_n256_w64_r8` | 61,141.2 | 13.000 | CACTI, 8 B/entry |
| `sram_lut_n8_w80_r1` | 826.6* | 0.513* | CACTI, 10 B/entry; N = 32 stands in |
| `sram_lut_n16_w80_r1` | 826.6* | 0.513* | CACTI, 10 B/entry; N = 32 stands in |
| `sram_lut_n64_w80_r1` | 1,210.0 | 0.716 | CACTI, 10 B/entry |
| `sram_lut_n128_w80_r1` | 1,956.0 | 1.117 | CACTI, 10 B/entry |
| `sram_lut_n8_w80_r2` | 3,737.1* | 1.310* | CACTI, 10 B/entry; N = 32 stands in |
| `sram_lut_n16_w80_r2` | 3,737.1* | 1.310* | CACTI, 10 B/entry; N = 32 stands in |
| `sram_lut_n8_w80_r3` | 5,869.3* | 2.077* | CACTI, 10 B/entry; N = 32 stands in |
| `sram_lut_n16_w80_r3` | 5,869.3* | 2.077* | CACTI, 10 B/entry; N = 32 stands in |
| `sram_lut_n8_w80_r4` | 8,466.2* | 2.984* | CACTI, 10 B/entry; N = 32 stands in |
| `sram_lut_n16_w80_r4` | 8,466.2* | 2.984* | CACTI, 10 B/entry; N = 32 stands in |
| `sram_lut_n8_w80_r6` | 15,036.5* | 5.233* | CACTI, 10 B/entry; N = 32 stands in |
| `sram_lut_n16_w80_r6` | 15,036.5* | 5.233* | CACTI, 10 B/entry; N = 32 stands in |
| `sram_lut_n8_w80_r8` | 23,413.5* | 8.066* | CACTI, 10 B/entry; N = 32 stands in |
| `sram_lut_n16_w80_r8` | 23,413.5* | 8.066* | CACTI, 10 B/entry; N = 32 stands in |
| `sram_lut_n32_w88_r1` | 954.9 | 0.579 | CACTI, 11 B/entry |
| `sram_lut_n64_w88_r1` | 1,381.5 | 0.801 | CACTI, 11 B/entry |
| `sram_lut_n128_w88_r1` | 2,213.3 | 1.240 | CACTI, 11 B/entry |
| `sram_lut_n256_w88_r1` | 3,978.1 | 2.078 | CACTI, 11 B/entry |
| `sram_lut_n512_w88_r1` | 8,160.5 | 4.443 | CACTI, 11 B/entry |
| `sram_lut_n1024_w88_r1` | 15,088.1 | 8.244 | CACTI, 11 B/entry |
| `sram_lut_n2048_w88_r1` | 29,440.8 | 15.503 | CACTI, 11 B/entry |
| `sram_lut_n4096_w88_r1` | 67,166.3 | 27.298 | CACTI, 11 B/entry |
| `sram_lut_n8192_w88_r1` | 140,774.0 | 51.539 | CACTI, 11 B/entry |
| `sram_lut_n32_w88_r2` | 4,314.2 | 1.498 | CACTI, 11 B/entry |
| `sram_lut_n64_w88_r2` | 5,859.5 | 1.926 | CACTI, 11 B/entry |
| `sram_lut_n128_w88_r2` | 8,920.6 | 2.831 | CACTI, 11 B/entry |
| `sram_lut_n256_w88_r2` | 14,964.2 | 4.510 | CACTI, 11 B/entry |
| `sram_lut_n32_w88_r3` | 6,789.2 | 2.393 | CACTI, 11 B/entry |
| `sram_lut_n64_w88_r3` | 9,112.0 | 2.941 | CACTI, 11 B/entry |
| `sram_lut_n128_w88_r3` | 13,684.3 | 4.111 | CACTI, 11 B/entry |
| `sram_lut_n256_w88_r3` | 22,734.4 | 6.260 | CACTI, 11 B/entry |
| `sram_lut_n32_w88_r4` | 9,807.0 | 3.456 | CACTI, 11 B/entry |
| `sram_lut_n64_w88_r4` | 13,065.1 | 4.137 | CACTI, 11 B/entry |
| `sram_lut_n128_w88_r4` | 19,430.9 | 5.605 | CACTI, 11 B/entry |
| `sram_lut_n256_w88_r4` | 32,068.2 | 8.284 | CACTI, 11 B/entry |
| `sram_lut_n32_w88_r6` | 17,450.0 | 6.105 | CACTI, 11 B/entry |
| `sram_lut_n64_w88_r6` | 23,003.0 | 7.097 | CACTI, 11 B/entry |
| `sram_lut_n128_w88_r6` | 33,833.1 | 9.264 | CACTI, 11 B/entry |
| `sram_lut_n256_w88_r6` | 55,383.1 | 13.177 | CACTI, 11 B/entry |
| `sram_lut_n32_w88_r8` | 27,205.7 | 9.454 | CACTI, 11 B/entry |
| `sram_lut_n64_w88_r8` | 35,617.5 | 10.813 | CACTI, 11 B/entry |
| `sram_lut_n128_w88_r8` | 52,092.3 | 13.817 | CACTI, 11 B/entry |
| `sram_lut_n256_w88_r8` | 84,868.2 | 19.200 | CACTI, 11 B/entry |
| `sram_lut_n8_w128_r1` | 1,716.8* | 0.971* | CACTI, 16 B/entry; N = 32 stands in |
| `sram_lut_n16_w128_r1` | 1,716.8* | 0.971* | CACTI, 16 B/entry; N = 32 stands in |
| `sram_lut_n32_w128_r1` | 1,716.8 | 0.971 | CACTI, 16 B/entry |
| `sram_lut_n64_w128_r1` | 2,367.1 | 1.340 | CACTI, 16 B/entry |
| `sram_lut_n128_w128_r1` | 3,644.4 | 2.073 | CACTI, 16 B/entry |
| `sram_lut_n256_w128_r1` | 6,194.9 | 3.498 | CACTI, 16 B/entry |
| `sram_lut_n512_w128_r1` | 12,085.9 | 6.446 | CACTI, 16 B/entry |
| `sram_lut_n1024_w128_r1` | 21,954.3 | 11.801 | CACTI, 16 B/entry |
| `sram_lut_n2048_w128_r1` | 42,439.6 | 21.775 | CACTI, 16 B/entry |
| `sram_lut_n4096_w128_r1` | 100,938.7 | 40.884 | CACTI, 16 B/entry |
| `sram_lut_n8192_w128_r1` | 209,484.4 | 73.136 | CACTI, 16 B/entry |
| `sram_lut_n8_w128_r2` | 7,722.2* | 2.472* | CACTI, 16 B/entry; N = 32 stands in |
| `sram_lut_n16_w128_r2` | 7,722.2* | 2.472* | CACTI, 16 B/entry; N = 32 stands in |
| `sram_lut_n32_w128_r2` | 7,722.2 | 2.472 | CACTI, 16 B/entry |
| `sram_lut_n64_w128_r2` | 9,945.6 | 3.069 | CACTI, 16 B/entry |
| `sram_lut_n128_w128_r2` | 14,352.6 | 4.311 | CACTI, 16 B/entry |
| `sram_lut_n256_w128_r2` | 23,077.7 | 6.662 | CACTI, 16 B/entry |
| `sram_lut_n8_w128_r3` | 12,331.4* | 4.068* | CACTI, 16 B/entry; N = 32 stands in |
| `sram_lut_n16_w128_r3` | 12,331.4* | 4.068* | CACTI, 16 B/entry; N = 32 stands in |
| `sram_lut_n32_w128_r3` | 12,331.4 | 4.068 | CACTI, 16 B/entry |
| `sram_lut_n64_w128_r3` | 15,682.5 | 4.835 | CACTI, 16 B/entry |
| `sram_lut_n128_w128_r3` | 22,294.6 | 6.443 | CACTI, 16 B/entry |
| `sram_lut_n256_w128_r3` | 35,407.3 | 9.469 | CACTI, 16 B/entry |
| `sram_lut_n8_w128_r4` | 17,033.2* | 5.998* | CACTI, 16 B/entry; N = 32 stands in |
| `sram_lut_n16_w128_r4` | 17,033.2* | 5.998* | CACTI, 16 B/entry; N = 32 stands in |
| `sram_lut_n32_w128_r4` | 17,033.2 | 5.998 | CACTI, 16 B/entry |
| `sram_lut_n64_w128_r4` | 21,494.2 | 6.956 | CACTI, 16 B/entry |
| `sram_lut_n128_w128_r4` | 30,244.5 | 8.978 | CACTI, 16 B/entry |
| `sram_lut_n256_w128_r4` | 47,629.8 | 12.763 | CACTI, 16 B/entry |
| `sram_lut_n8_w128_r6` | 30,604.4* | 10.874* | CACTI, 16 B/entry; N = 32 stands in |
| `sram_lut_n16_w128_r6` | 30,604.4* | 10.874* | CACTI, 16 B/entry; N = 32 stands in |
| `sram_lut_n32_w128_r6` | 30,604.4 | 10.874 | CACTI, 16 B/entry |
| `sram_lut_n64_w128_r6` | 38,218.9 | 12.277 | CACTI, 16 B/entry |
| `sram_lut_n128_w128_r6` | 53,132.2 | 15.266 | CACTI, 16 B/entry |
| `sram_lut_n256_w128_r6` | 82,808.7 | 20.824 | CACTI, 16 B/entry |
| `sram_lut_n8_w128_r8` | 47,948.3* | 17.111* | CACTI, 16 B/entry; N = 32 stands in |
| `sram_lut_n16_w128_r8` | 47,948.3* | 17.111* | CACTI, 16 B/entry; N = 32 stands in |
| `sram_lut_n32_w128_r8` | 47,948.3 | 17.111 | CACTI, 16 B/entry |
| `sram_lut_n64_w128_r8` | 59,491.7 | 19.029 | CACTI, 16 B/entry |
| `sram_lut_n128_w128_r8` | 82,166.3 | 23.149 | CACTI, 16 B/entry |
| `sram_lut_n256_w128_r8` | 127,278.8 | 30.767 | CACTI, 16 B/entry |

## Notes

1. **Register-file power** comes from the 0.1 ns clock-transition run, the flow's setting
   since 2026-10-22. Where only the earlier 5 ns run exists, the power is marked `*`: 5 ns
   inflates flip-flop power, and the 16-bit tables run at 0.05 ns draw 0.49–0.83× their
   5 ns power. Area moves by under 1%, so it is not marked. A 0.1 ns rerun of those tables is
   queued on cmp00.
2. **CACTI cannot model N = 8 or 16 at any width** ("no valid data array organizations
   found"), nor tables under 64 bytes. Those cells use the smallest modelled table (`*`).
3. **Multi-port vs copies.** In CACTI, one table with R read ports has 1.70–3.56×
   the area of R single-port copies (all 180 cases) and 0.82–2.20×
   the read-only power. For register files, one table with R read ports has
   0.29–0.63× the area of R copies (58 cases so far): the flip-flops are shared
   and only the read muxes are replicated.
4. **wa = int8 entries are exact** (8 + ⌈log2 v⌉ bits), so no partial sum overflows. The adds
   stay fp16, as specified.
5. **The converter MAC opt leaves out is small.** A standalone `CW_fp_i2flt` → fp16 is
   70–120 µm² of logic for the int-wq × int8 products (10 to 16 bits), and an
   exact RTL converter 53–73 µm² where no rounding is needed (≤ 12 bits).
   See [02](../02-int-to-fp-converter-cost/README.md).
6. **`mul_int2xfp16` is only 38 µm²**: every int2
   value converts to fp16 with an all-zero mantissa, so Genus removes the significand
   multiplier and only sign and exponent logic remain. From int3 up there is a real multiplier.
7. **Ternary tables are large**: 128, 1,024, 4,096, 8,192 entries
   at v = 4, 6, 7, 8 (half with symm). Register files are costed only up to
   v = 6 (1,024 entries); SRAM at every v.
8. **fp16 units close timing at ~0 ps slack** at 2 ns (`mul_fp16` 0 ps,
   `add_fp16` 1 ps), so their area includes upsizing. At a 4 ns clock,
   `add_fp16` is 344 µm² and `mul_fp16`
   346 µm²; the tables use the 2 ns numbers.
