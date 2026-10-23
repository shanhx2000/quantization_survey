# 01 — MAC-GEMM vs LUT-GEMM cost per quantization frame

Generated 2026-10-23 by `make_tables.py` from [`../results/`](../results/) (the cmp00 sweep
snapshot; see [`../README.md`](../README.md)). Edit the script, not this file.

**Tables, one file per batch size: [bs = 1](tables-bs1.md) · [bs = 2](tables-bs2.md) · [bs = 4](tables-bs4.md) · [bs = 8](tables-bs8.md).** Each file has one table per frame
(wq ∈ {int1, ter, int2, int3, int4, int6, int8} × wa ∈ {int8, fp16}), one row per method and one column per
v. **Cell: area (µm²) / power (mW)** at 500 MHz, for hardware that consumes one v-element
slice of a dot product for every batch row each cycle. Power × 2 = energy per cycle in pJ.
`#` = no data yet. `*` = upper bound: an SRAM table CACTI cannot model (under 64 bytes, or N = 8, 16), costed as the smallest modelled table of the same width and ports. `—` = not costed: ternary register-file tables above v = 6. `#` and `*` apply to area and power separately.

## Missing data

| Data | Missing | Configurations | Why |
|---|---|---|---|
| Reg LUT, 1 read port | area + power | W = 40: N = 8, 16, 64, 128<br>W = 44: N = 32, 64, 128, 256, 512, 1024<br>W = 80: N = 8, 16, 64, 128<br>W = 88: N = 32, 64, 128, 256, 512, 1024<br>W = 128: N = 8, 16, 32, 64, 128, 256, 512, 1024 | not synthesized: W = 40, 44, 80, 88, 128 wait for an owner decision, predict with the gate-count model or synthesize ([`mac_lut_status.md`](../results/todo/mac_lut_status.md)) |
| Reg LUT, wq read ports | area + power | W = 20: N = 8, 16, R = 2/3/4/6/8<br>W = 22: N = 32, 64, 128, 256, R = 2/3/4/6/8<br>W = 32: N = 8, 16, 32, 64, 128, 256, R = 2/3/4/6/8<br>W = 40: N = 8, 16, R = 2/3/4/6/8<br>W = 44: N = 32, 64, 128, 256, R = 2/3/4/6/8<br>W = 64: N = 8, 16, 32, 64, 128, 256, R = 2/3/4/6/8<br>W = 80: N = 8, 16, R = 2/3/4/6/8<br>W = 88: N = 32, 64, 128, 256, R = 2/3/4/6/8<br>W = 128: N = 8, 16, 32, 64, 128, 256, R = 2/3/4/6/8 | not synthesized: W = 40, 44, 80, 88, 128 wait for an owner decision, predict with the gate-count model or synthesize ([`mac_lut_status.md`](../results/todo/mac_lut_status.md)) |

The data is being collected on cmp00; the snapshot of its plan and status is in
[`../results/todo/`](../results/todo/).

## Methods and cost model

* **wq**: weight format: int1, ter, int2, int3, int4, int6, int8. int-b = b-bit integer; **ter** = ternary
  {−1, 0, +1}. **wa**: activation format (int8 or fp16). **v**: vector length, the number of
  activations combined per step. **bs**: batch size (1, 2, 4, 8).
* **MAC-GEMM**: bs·v multipliers and bs·v adders (a batch of bs needs bs times the resources).
  * *fp16*: v × fp16 mul + v × fp16 add.
  * *opt*: v × (int-wq × wa) mul + v × fp16 add. int × fp16 multipliers output fp16. The
    int → fp16 conversion that wa = int8 needs is not counted (note 6).
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
* **Power** = Σ count × unit power, every unit busy every cycle. **LUT power is read-only**,
  the read-only corner of `buffer_costs_v2.csv`: every read port reads every cycle, the write
  port is idle with its data and address held. Register files: a power-only Genus
  re-analysis of the 0.1 ns netlist, measured instance only. SRAM: CACTI at
  300 K, leakage + R × 500 MHz × E_read.
* **Not counted:** table precompute, the sign flip, the 2^b weighting between bit-planes, and
  any int → fp conversion.

## Unit costs used

Only primitives with at least one number; the rest are in *Missing data*.

| Primitive | Area (µm²) | Power (mW) | Source |
|---|---|---|---|
| `add_fp16` | 515.1 | 1.530 | `add_fp16`, logic only |
| `add_int16` | 32.8 | 0.053 | `add_int16`, logic only |
| `mul_fp16` | 383.7 | 1.064 | `mul_fp16`, logic only |
| `mul_int2xfp16` | 40.7 | 0.116 | `mul_int2xfp16`, logic only |
| `mul_int2xint8` | 33.5 | 0.093 | `mul_int2xint8`, logic only |
| `mul_int3xfp16` | 189.4 | 0.582 | `mul_int3xfp16`, logic only |
| `mul_int3xint8` | 47.5 | 0.109 | `mul_int3xint8`, logic only |
| `mul_int4xfp16` | 223.4 | 0.659 | `mul_int4xfp16`, logic only |
| `mul_int4xint8` | 64.3 | 0.119 | `mul_int4xint8`, logic only |
| `mul_int6xfp16` | 315.8 | 0.963 | `mul_int6xfp16`, logic only |
| `mul_int6xint8` | 106.3 | 0.202 | `mul_int6xint8`, logic only |
| `mul_int8` | 142.3 | 0.244 | `mul_int8`, logic only |
| `mul_int8xfp16` | 401.6 | 1.105 | `mul_int8xfp16`, logic only |
| `reg_lut_n8_w10_r1` | 234.0 | 0.103 | `buffer_n8_w10`, 0.1 ns clock transition |
| `reg_lut_n16_w10_r1` | 446.5 | 0.144 | `buffer_n16_w10`, 0.1 ns clock transition |
| `reg_lut_n64_w10_r1` | 1,713.2 | 0.302 | `buffer_n64_w10`, 0.1 ns clock transition |
| `reg_lut_n128_w10_r1` | 3,390.7 | 0.459 | `buffer_n128_w10`, 0.1 ns clock transition |
| `reg_lut_n8_w10_r2` | 296.1 | 0.182 | `buffer1w2r_n8_w10`, 0.1 ns clock transition |
| `reg_lut_n16_w10_r2` | 551.5 | 0.250 | `buffer1w2r_n16_w10`, 0.1 ns clock transition |
| `reg_lut_n8_w10_r3` | 357.8 | 0.268 | `buffer1w3r_n8_w10`, 0.1 ns clock transition |
| `reg_lut_n16_w10_r3` | 652.7 | 0.363 | `buffer1w3r_n16_w10`, 0.1 ns clock transition |
| `reg_lut_n8_w10_r4` | 419.6 | 0.354 | `buffer1w4r_n8_w10`, 0.1 ns clock transition |
| `reg_lut_n16_w10_r4` | 755.2 | 0.478 | `buffer1w4r_n16_w10`, 0.1 ns clock transition |
| `reg_lut_n8_w10_r6` | 543.1 | 0.526 | `buffer1w6r_n8_w10`, 0.1 ns clock transition |
| `reg_lut_n16_w10_r6` | 960.4 | 0.708 | `buffer1w6r_n16_w10`, 0.1 ns clock transition |
| `reg_lut_n8_w10_r8` | 666.5 | 0.699 | `buffer1w8r_n8_w10`, 0.1 ns clock transition |
| `reg_lut_n16_w10_r8` | 1,156.0 | 0.936 | `buffer1w8r_n16_w10`, 0.1 ns clock transition |
| `reg_lut_n32_w11_r1` | 950.7 | 0.212 | `buffer_n32_w11`, 0.1 ns clock transition |
| `reg_lut_n64_w11_r1` | 1,865.9 | 0.324 | `buffer_n64_w11`, 0.1 ns clock transition |
| `reg_lut_n128_w11_r1` | 3,690.4 | 0.479 | `buffer_n128_w11`, 0.1 ns clock transition |
| `reg_lut_n256_w11_r1` | 7,380.4 | 0.730 | `buffer_n256_w11`, 0.1 ns clock transition |
| `reg_lut_n512_w11_r1` | 14,754.1 | 1.356 | `buffer_n512_w11`, 0.1 ns clock transition |
| `reg_lut_n1024_w11_r1` | 29,530.6 | 2.450 | `buffer_n1024_w11`, 0.1 ns clock transition |
| `reg_lut_n32_w11_r2` | 1,154.9 | 0.352 | `buffer1w2r_n32_w11`, 0.1 ns clock transition |
| `reg_lut_n64_w11_r2` | 2,233.6 | 0.483 | `buffer1w2r_n64_w11`, 0.1 ns clock transition |
| `reg_lut_n128_w11_r2` | 4,392.5 | 0.680 | `buffer1w2r_n128_w11`, 0.1 ns clock transition |
| `reg_lut_n256_w11_r2` | 8,770.1 | 0.985 | `buffer1w2r_n256_w11`, 0.1 ns clock transition |
| `reg_lut_n32_w11_r3` | 1,353.7 | 0.508 | `buffer1w3r_n32_w11`, 0.1 ns clock transition |
| `reg_lut_n64_w11_r3` | 2,600.5 | 0.682 | `buffer1w3r_n64_w11`, 0.1 ns clock transition |
| `reg_lut_n128_w11_r3` | 5,094.2 | 0.937 | `buffer1w3r_n128_w11`, 0.1 ns clock transition |
| `reg_lut_n256_w11_r3` | 10,158.9 | 1.310 | `buffer1w3r_n256_w11`, 0.1 ns clock transition |
| `reg_lut_n32_w11_r4` | 1,553.2 | 0.665 | `buffer1w4r_n32_w11`, 0.1 ns clock transition |
| `reg_lut_n64_w11_r4` | 2,970.3 | 0.885 | `buffer1w4r_n64_w11`, 0.1 ns clock transition |
| `reg_lut_n128_w11_r4` | 5,796.4 | 1.194 | `buffer1w4r_n128_w11`, 0.1 ns clock transition |
| `reg_lut_n256_w11_r4` | 11,548.2 | 1.636 | `buffer1w4r_n256_w11`, 0.1 ns clock transition |
| `reg_lut_n32_w11_r6` | 1,951.9 | 0.979 | `buffer1w6r_n32_w11`, 0.1 ns clock transition |
| `reg_lut_n64_w11_r6` | 3,701.5 | 1.284 | `buffer1w6r_n64_w11`, 0.1 ns clock transition |
| `reg_lut_n128_w11_r6` | 7,201.0 | 1.710 | `buffer1w6r_n128_w11`, 0.1 ns clock transition |
| `reg_lut_n256_w11_r6` | 14,331.9 | 2.290 | `buffer1w6r_n256_w11`, 0.1 ns clock transition |
| `reg_lut_n32_w11_r8` | 2,340.8 | 1.281 | `buffer1w8r_n32_w11`, 0.1 ns clock transition |
| `reg_lut_n64_w11_r8` | 4,436.5 | 1.688 | `buffer1w8r_n64_w11`, 0.1 ns clock transition |
| `reg_lut_n128_w11_r8` | 8,603.7 | 2.227 | `buffer1w8r_n128_w11`, 0.1 ns clock transition |
| `reg_lut_n256_w11_r8` | 17,125.2 | 2.956 | `buffer1w8r_n256_w11`, 0.1 ns clock transition |
| `reg_lut_n8_w16_r1` | 357.2 | 0.152 | `buffer_n8`, 0.1 ns clock transition |
| `reg_lut_n16_w16_r1` | 681.7 | 0.201 | `buffer_n16`, 0.1 ns clock transition |
| `reg_lut_n32_w16_r1` | 1,333.1 | 0.268 | `buffer_n32`, 0.1 ns clock transition |
| `reg_lut_n64_w16_r1` | 2,622.2 | 0.398 | `buffer_n64`, 0.1 ns clock transition |
| `reg_lut_n128_w16_r1` | 5,191.6 | 0.559 | `buffer_n128`, 0.1 ns clock transition |
| `reg_lut_n256_w16_r1` | 10,378.6 | 0.824 | `buffer_n256`, 0.1 ns clock transition |
| `reg_lut_n512_w16_r1` | 20,731.9 | 1.444 | `buffer_n512`, 0.1 ns clock transition |
| `reg_lut_n1024_w16_r1` | 41,475.8 | 2.542 | `buffer_n1024`, 0.1 ns clock transition |
| `reg_lut_n8_w16_r2` | 451.8 | 0.297 | `buffer1w2r_n8`, 0.1 ns clock transition |
| `reg_lut_n16_w16_r2` | 842.8 | 0.367 | `buffer1w2r_n16`, 0.1 ns clock transition |
| `reg_lut_n32_w16_r2` | 1,616.7 | 0.460 | `buffer1w2r_n32`, 0.1 ns clock transition |
| `reg_lut_n64_w16_r2` | 3,138.8 | 0.618 | `buffer1w2r_n64`, 0.1 ns clock transition |
| `reg_lut_n128_w16_r2` | 6,182.2 | 0.837 | `buffer1w2r_n128`, 0.1 ns clock transition |
| `reg_lut_n256_w16_r2` | 12,341.4 | 1.175 | `buffer1w2r_n256`, 0.1 ns clock transition |
| `reg_lut_n8_w16_r3` | 546.1 | 0.440 | `buffer1w3r_n8`, 0.1 ns clock transition |
| `reg_lut_n16_w16_r3` | 1,000.2 | 0.539 | `buffer1w3r_n16`, 0.1 ns clock transition |
| `reg_lut_n32_w16_r3` | 1,895.3 | 0.671 | `buffer1w3r_n32`, 0.1 ns clock transition |
| `reg_lut_n64_w16_r3` | 3,655.8 | 0.883 | `buffer1w3r_n64`, 0.1 ns clock transition |
| `reg_lut_n128_w16_r3` | 7,173.4 | 1.177 | `buffer1w3r_n128`, 0.1 ns clock transition |
| `reg_lut_n256_w16_r3` | 14,306.5 | 1.595 | `buffer1w3r_n256`, 0.1 ns clock transition |
| `reg_lut_n8_w16_r4` | 640.3 | 0.583 | `buffer1w4r_n8`, 0.1 ns clock transition |
| `reg_lut_n16_w16_r4` | 1,157.7 | 0.712 | `buffer1w4r_n16`, 0.1 ns clock transition |
| `reg_lut_n32_w16_r4` | 2,173.9 | 0.881 | `buffer1w4r_n32`, 0.1 ns clock transition |
| `reg_lut_n64_w16_r4` | 4,171.4 | 1.155 | `buffer1w4r_n64`, 0.1 ns clock transition |
| `reg_lut_n128_w16_r4` | 8,165.7 | 1.516 | `buffer1w4r_n128`, 0.1 ns clock transition |
| `reg_lut_n256_w16_r4` | 16,276.8 | 2.007 | `buffer1w4r_n256`, 0.1 ns clock transition |
| `reg_lut_n8_w16_r6` | 828.8 | 0.869 | `buffer1w6r_n8`, 0.1 ns clock transition |
| `reg_lut_n16_w16_r6` | 1,472.7 | 1.057 | `buffer1w6r_n16`, 0.1 ns clock transition |
| `reg_lut_n32_w16_r6` | 2,730.9 | 1.294 | `buffer1w6r_n32`, 0.1 ns clock transition |
| `reg_lut_n64_w16_r6` | 5,204.2 | 1.682 | `buffer1w6r_n64`, 0.1 ns clock transition |
| `reg_lut_n128_w16_r6` | 10,150.3 | 2.192 | `buffer1w6r_n128`, 0.1 ns clock transition |
| `reg_lut_n256_w16_r6` | 20,209.3 | 2.841 | `buffer1w6r_n256`, 0.1 ns clock transition |
| `reg_lut_n8_w16_r8` | 1,017.3 | 1.156 | `buffer1w8r_n8`, 0.1 ns clock transition |
| `reg_lut_n16_w16_r8` | 1,787.7 | 1.403 | `buffer1w8r_n16`, 0.1 ns clock transition |
| `reg_lut_n32_w16_r8` | 3,287.7 | 1.711 | `buffer1w8r_n32`, 0.1 ns clock transition |
| `reg_lut_n64_w16_r8` | 6,237.5 | 2.217 | `buffer1w8r_n64`, 0.1 ns clock transition |
| `reg_lut_n128_w16_r8` | 12,133.8 | 2.875 | `buffer1w8r_n128`, 0.1 ns clock transition |
| `reg_lut_n256_w16_r8` | 24,138.6 | 3.676 | `buffer1w8r_n256`, 0.1 ns clock transition |
| `reg_lut_n8_w20_r1` | 456.8 | 0.195 | `buffer_n8_w20`, 0.1 ns clock transition |
| `reg_lut_n16_w20_r1` | 870.8 | 0.262 | `buffer_n16_w20`, 0.1 ns clock transition |
| `reg_lut_n64_w20_r1` | 3,345.4 | 0.527 | `buffer_n64_w20`, 0.1 ns clock transition |
| `reg_lut_n128_w20_r1` | 6,631.9 | 0.777 | `buffer_n128_w20`, 0.1 ns clock transition |
| `reg_lut_n32_w22_r1` | 1,860.3 | 0.383 | `buffer_n32_w22`, 0.1 ns clock transition |
| `reg_lut_n64_w22_r1` | 3,645.8 | 0.554 | `buffer_n64_w22`, 0.1 ns clock transition |
| `reg_lut_n128_w22_r1` | 7,229.8 | 0.810 | `buffer_n128_w22`, 0.1 ns clock transition |
| `reg_lut_n256_w22_r1` | 14,461.8 | 1.226 | `buffer_n256_w22`, 0.1 ns clock transition |
| `reg_lut_n512_w22_r1` | 28,898.0 | 2.185 | `buffer_n512_w22`, 0.1 ns clock transition |
| `reg_lut_n1024_w22_r1` | 57,660.9 | 3.909 | `buffer_n1024_w22`, 0.1 ns clock transition |
| `reg_lut_n8_w32_r1` | 703.5 | 0.301 | `buffer_n8_w32`, 0.1 ns clock transition |
| `reg_lut_n16_w32_r1` | 1,343.4 | 0.379 | `buffer_n16_w32`, 0.1 ns clock transition |
| `reg_lut_n32_w32_r1` | 2,627.6 | 0.498 | `buffer_n32_w32`, 0.1 ns clock transition |
| `reg_lut_n64_w32_r1` | 5,154.7 | 0.704 | `buffer_n64_w32`, 0.1 ns clock transition |
| `reg_lut_n128_w32_r1` | 10,222.5 | 0.986 | `buffer_n128_w32`, 0.1 ns clock transition |
| `reg_lut_n256_w32_r1` | 20,465.0 | 1.424 | `buffer_n256_w32`, 0.1 ns clock transition |
| `reg_lut_n512_w32_r1` | 40,861.4 | 2.408 | `buffer_n512_w32`, 0.1 ns clock transition |
| `reg_lut_n1024_w32_r1` | 82,011.9 | 4.359 | `buffer_n1024_w32`, 0.1 ns clock transition |
| `reg_lut_n8_w64_r1` | 1,395.2 | 0.605 | `buffer_n8_w64`, 0.1 ns clock transition |
| `reg_lut_n16_w64_r1` | 2,665.9 | 0.734 | `buffer_n16_w64`, 0.1 ns clock transition |
| `reg_lut_n32_w64_r1` | 5,219.6 | 0.952 | `buffer_n32_w64`, 0.1 ns clock transition |
| `reg_lut_n64_w64_r1` | 10,227.8 | 1.326 | `buffer_n64_w64`, 0.1 ns clock transition |
| `reg_lut_n128_w64_r1` | 20,321.2 | 1.810 | `buffer_n128_w64`, 0.1 ns clock transition |
| `reg_lut_n256_w64_r1` | 40,841.1 | 2.610 | `buffer_n256_w64`, 0.1 ns clock transition |
| `reg_lut_n512_w64_r1` | 81,735.4 | 4.385 | `buffer_n512_w64`, 0.1 ns clock transition |
| `reg_lut_n1024_w64_r1` | 164,116.4 | 7.549 | `buffer_n1024_w64`, 0.1 ns clock transition |
| `sram_lut_n8_w16_r1` | 139.7* | 0.075* | CACTI 300 K, 2 B/entry; N = 32 stands in |
| `sram_lut_n16_w16_r1` | 139.7* | 0.075* | CACTI 300 K, 2 B/entry; N = 32 stands in |
| `sram_lut_n32_w16_r1` | 139.7 | 0.075 | CACTI 300 K, 2 B/entry |
| `sram_lut_n64_w16_r1` | 242.3 | 0.102 | CACTI 300 K, 2 B/entry |
| `sram_lut_n128_w16_r1` | 451.8 | 0.161 | CACTI 300 K, 2 B/entry |
| `sram_lut_n256_w16_r1` | 790.1 | 0.248 | CACTI 300 K, 2 B/entry |
| `sram_lut_n512_w16_r1` | 1,566.8 | 0.380 | CACTI 300 K, 2 B/entry |
| `sram_lut_n1024_w16_r1` | 2,779.9 | 0.664 | CACTI 300 K, 2 B/entry |
| `sram_lut_n2048_w16_r1` | 5,595.4 | 1.374 | CACTI 300 K, 2 B/entry |
| `sram_lut_n4096_w16_r1` | 14,105.0 | 1.966 | CACTI 300 K, 2 B/entry |
| `sram_lut_n8192_w16_r1` | 23,844.0 | 3.494 | CACTI 300 K, 2 B/entry |
| `sram_lut_n8_w16_r2` | 499.2* | 0.175* | CACTI 300 K, 2 B/entry; N = 32 stands in |
| `sram_lut_n16_w16_r2` | 499.2* | 0.175* | CACTI 300 K, 2 B/entry; N = 32 stands in |
| `sram_lut_n32_w16_r2` | 499.2 | 0.175 | CACTI 300 K, 2 B/entry |
| `sram_lut_n64_w16_r2` | 896.3 | 0.212 | CACTI 300 K, 2 B/entry |
| `sram_lut_n128_w16_r2` | 1,536.3 | 0.343 | CACTI 300 K, 2 B/entry |
| `sram_lut_n256_w16_r2` | 2,828.5 | 0.528 | CACTI 300 K, 2 B/entry |
| `sram_lut_n8_w16_r3` | 757.8* | 0.273* | CACTI 300 K, 2 B/entry; N = 32 stands in |
| `sram_lut_n16_w16_r3` | 757.8* | 0.273* | CACTI 300 K, 2 B/entry; N = 32 stands in |
| `sram_lut_n32_w16_r3` | 757.8 | 0.273 | CACTI 300 K, 2 B/entry |
| `sram_lut_n64_w16_r3` | 1,373.4 | 0.323 | CACTI 300 K, 2 B/entry |
| `sram_lut_n128_w16_r3` | 2,336.9 | 0.530 | CACTI 300 K, 2 B/entry |
| `sram_lut_n256_w16_r3` | 4,289.8 | 0.801 | CACTI 300 K, 2 B/entry |
| `sram_lut_n8_w16_r4` | 1,067.9* | 0.384* | CACTI 300 K, 2 B/entry; N = 32 stands in |
| `sram_lut_n16_w16_r4` | 1,067.9* | 0.384* | CACTI 300 K, 2 B/entry; N = 32 stands in |
| `sram_lut_n32_w16_r4` | 1,067.9 | 0.384 | CACTI 300 K, 2 B/entry |
| `sram_lut_n64_w16_r4` | 1,954.2 | 0.450 | CACTI 300 K, 2 B/entry |
| `sram_lut_n128_w16_r4` | 3,312.0 | 0.743 | CACTI 300 K, 2 B/entry |
| `sram_lut_n256_w16_r4` | 6,050.8 | 1.115 | CACTI 300 K, 2 B/entry |
| `sram_lut_n8_w16_r6` | 1,856.0* | 0.645* | CACTI 300 K, 2 B/entry; N = 32 stands in |
| `sram_lut_n16_w16_r6` | 1,856.0* | 0.645* | CACTI 300 K, 2 B/entry; N = 32 stands in |
| `sram_lut_n32_w16_r6` | 1,856.0 | 0.645 | CACTI 300 K, 2 B/entry |
| `sram_lut_n64_w16_r6` | 3,390.9 | 0.751 | CACTI 300 K, 2 B/entry |
| `sram_lut_n128_w16_r6` | 5,716.6 | 1.252 | CACTI 300 K, 2 B/entry |
| `sram_lut_n256_w16_r6` | 11,642.9 | 2.317 | CACTI 300 K, 2 B/entry |
| `sram_lut_n8_w16_r8` | 2,845.6* | 0.951* | CACTI 300 K, 2 B/entry; N = 32 stands in |
| `sram_lut_n16_w16_r8` | 2,845.6* | 0.951* | CACTI 300 K, 2 B/entry; N = 32 stands in |
| `sram_lut_n32_w16_r8` | 2,845.6 | 0.951 | CACTI 300 K, 2 B/entry |
| `sram_lut_n64_w16_r8` | 5,171.5 | 1.108 | CACTI 300 K, 2 B/entry |
| `sram_lut_n128_w16_r8` | 9,090.4 | 1.967 | CACTI 300 K, 2 B/entry |
| `sram_lut_n256_w16_r8` | 17,695.0 | 3.467 | CACTI 300 K, 2 B/entry |
| `sram_lut_n8_w24_r1` | 211.4* | 0.111* | CACTI 300 K, 3 B/entry; N = 32 stands in |
| `sram_lut_n16_w24_r1` | 211.4* | 0.111* | CACTI 300 K, 3 B/entry; N = 32 stands in |
| `sram_lut_n32_w24_r1` | 211.4 | 0.111 | CACTI 300 K, 3 B/entry |
| `sram_lut_n64_w24_r1` | 348.9 | 0.146 | CACTI 300 K, 3 B/entry |
| `sram_lut_n128_w24_r1` | 632.1 | 0.222 | CACTI 300 K, 3 B/entry |
| `sram_lut_n256_w24_r1` | 1,116.3 | 0.347 | CACTI 300 K, 3 B/entry |
| `sram_lut_n512_w24_r1` | 2,158.3 | 0.538 | CACTI 300 K, 3 B/entry |
| `sram_lut_n1024_w24_r1` | 4,378.9 | 1.094 | CACTI 300 K, 3 B/entry |
| `sram_lut_n2048_w24_r1` | 8,303.4 | 2.004 | CACTI 300 K, 3 B/entry |
| `sram_lut_n4096_w24_r1` | 19,022.2 | 2.799 | CACTI 300 K, 3 B/entry |
| `sram_lut_n8192_w24_r1` | 36,172.6 | 6.063 | CACTI 300 K, 3 B/entry |
| `sram_lut_n8_w24_r2` | 756.4* | 0.262* | CACTI 300 K, 3 B/entry; N = 32 stands in |
| `sram_lut_n16_w24_r2` | 756.4* | 0.262* | CACTI 300 K, 3 B/entry; N = 32 stands in |
| `sram_lut_n32_w24_r2` | 756.4 | 0.262 | CACTI 300 K, 3 B/entry |
| `sram_lut_n64_w24_r2` | 1,282.9 | 0.316 | CACTI 300 K, 3 B/entry |
| `sram_lut_n128_w24_r2` | 2,360.5 | 0.474 | CACTI 300 K, 3 B/entry |
| `sram_lut_n256_w24_r2` | 3,981.5 | 0.756 | CACTI 300 K, 3 B/entry |
| `sram_lut_n8_w24_r3` | 1,158.9* | 0.415* | CACTI 300 K, 3 B/entry; N = 32 stands in |
| `sram_lut_n16_w24_r3` | 1,158.9* | 0.415* | CACTI 300 K, 3 B/entry; N = 32 stands in |
| `sram_lut_n32_w24_r3` | 1,158.9 | 0.415 | CACTI 300 K, 3 B/entry |
| `sram_lut_n64_w24_r3` | 1,970.7 | 0.491 | CACTI 300 K, 3 B/entry |
| `sram_lut_n128_w24_r3` | 3,606.9 | 0.722 | CACTI 300 K, 3 B/entry |
| `sram_lut_n256_w24_r3` | 6,054.6 | 1.162 | CACTI 300 K, 3 B/entry |
| `sram_lut_n8_w24_r4` | 1,642.4* | 0.589* | CACTI 300 K, 3 B/entry; N = 32 stands in |
| `sram_lut_n16_w24_r4` | 1,642.4* | 0.589* | CACTI 300 K, 3 B/entry; N = 32 stands in |
| `sram_lut_n32_w24_r4` | 1,642.4 | 0.589 | CACTI 300 K, 3 B/entry |
| `sram_lut_n64_w24_r4` | 2,805.3 | 0.690 | CACTI 300 K, 3 B/entry |
| `sram_lut_n128_w24_r4` | 5,391.5 | 1.199 | CACTI 300 K, 3 B/entry |
| `sram_lut_n256_w24_r4` | 9,130.5 | 1.729 | CACTI 300 K, 3 B/entry |
| `sram_lut_n8_w24_r6` | 2,867.8* | 1.000* | CACTI 300 K, 3 B/entry; N = 32 stands in |
| `sram_lut_n16_w24_r6` | 2,867.8* | 1.000* | CACTI 300 K, 3 B/entry; N = 32 stands in |
| `sram_lut_n32_w24_r6` | 2,867.8 | 1.000 | CACTI 300 K, 3 B/entry |
| `sram_lut_n64_w24_r6` | 4,881.7 | 1.164 | CACTI 300 K, 3 B/entry |
| `sram_lut_n128_w24_r6` | 9,153.5 | 2.033 | CACTI 300 K, 3 B/entry |
| `sram_lut_n256_w24_r6` | 15,419.5 | 2.903 | CACTI 300 K, 3 B/entry |
| `sram_lut_n8_w24_r8` | 4,414.5* | 1.501* | CACTI 300 K, 3 B/entry; N = 32 stands in |
| `sram_lut_n16_w24_r8` | 4,414.5* | 1.501* | CACTI 300 K, 3 B/entry; N = 32 stands in |
| `sram_lut_n32_w24_r8` | 4,414.5 | 1.501 | CACTI 300 K, 3 B/entry |
| `sram_lut_n64_w24_r8` | 7,476.8 | 1.746 | CACTI 300 K, 3 B/entry |
| `sram_lut_n128_w24_r8` | 13,790.3 | 3.053 | CACTI 300 K, 3 B/entry |
| `sram_lut_n256_w24_r8` | 23,221.6 | 4.346 | CACTI 300 K, 3 B/entry |
| `sram_lut_n8_w32_r1` | 284.9* | 0.142* | CACTI 300 K, 4 B/entry; N = 32 stands in |
| `sram_lut_n16_w32_r1` | 284.9* | 0.142* | CACTI 300 K, 4 B/entry; N = 32 stands in |
| `sram_lut_n32_w32_r1` | 284.9 | 0.142 | CACTI 300 K, 4 B/entry |
| `sram_lut_n64_w32_r1` | 458.5 | 0.184 | CACTI 300 K, 4 B/entry |
| `sram_lut_n128_w32_r1` | 809.3 | 0.272 | CACTI 300 K, 4 B/entry |
| `sram_lut_n256_w32_r1` | 1,587.6 | 0.404 | CACTI 300 K, 4 B/entry |
| `sram_lut_n512_w32_r1` | 2,809.8 | 0.696 | CACTI 300 K, 4 B/entry |
| `sram_lut_n1024_w32_r1` | 5,662.9 | 1.427 | CACTI 300 K, 4 B/entry |
| `sram_lut_n2048_w32_r1` | 11,071.0 | 2.644 | CACTI 300 K, 4 B/entry |
| `sram_lut_n4096_w32_r1` | 24,503.6 | 3.660 | CACTI 300 K, 4 B/entry |
| `sram_lut_n8192_w32_r1` | 53,134.7 | 7.648 | CACTI 300 K, 4 B/entry |
| `sram_lut_n8_w32_r2` | 1,025.6* | 0.343* | CACTI 300 K, 4 B/entry; N = 32 stands in |
| `sram_lut_n16_w32_r2` | 1,025.6* | 0.343* | CACTI 300 K, 4 B/entry; N = 32 stands in |
| `sram_lut_n32_w32_r2` | 1,025.6 | 0.343 | CACTI 300 K, 4 B/entry |
| `sram_lut_n64_w32_r2` | 1,660.3 | 0.410 | CACTI 300 K, 4 B/entry |
| `sram_lut_n128_w32_r2` | 2,959.7 | 0.595 | CACTI 300 K, 4 B/entry |
| `sram_lut_n256_w32_r2` | 5,738.7 | 1.077 | CACTI 300 K, 4 B/entry |
| `sram_lut_n8_w32_r3` | 1,564.3* | 0.549* | CACTI 300 K, 4 B/entry; N = 32 stands in |
| `sram_lut_n16_w32_r3` | 1,564.3* | 0.549* | CACTI 300 K, 4 B/entry; N = 32 stands in |
| `sram_lut_n32_w32_r3` | 1,564.3 | 0.549 | CACTI 300 K, 4 B/entry |
| `sram_lut_n64_w32_r3` | 2,545.8 | 0.645 | CACTI 300 K, 4 B/entry |
| `sram_lut_n128_w32_r3` | 4,511.3 | 0.916 | CACTI 300 K, 4 B/entry |
| `sram_lut_n256_w32_r3` | 8,668.4 | 1.648 | CACTI 300 K, 4 B/entry |
| `sram_lut_n8_w32_r4` | 2,222.6* | 0.785* | CACTI 300 K, 4 B/entry; N = 32 stands in |
| `sram_lut_n16_w32_r4` | 2,222.6* | 0.785* | CACTI 300 K, 4 B/entry; N = 32 stands in |
| `sram_lut_n32_w32_r4` | 2,222.6 | 0.785 | CACTI 300 K, 4 B/entry |
| `sram_lut_n64_w32_r4` | 3,622.2 | 0.914 | CACTI 300 K, 4 B/entry |
| `sram_lut_n128_w32_r4` | 6,380.7 | 1.286 | CACTI 300 K, 4 B/entry |
| `sram_lut_n256_w32_r4` | 12,171.7 | 2.309 | CACTI 300 K, 4 B/entry |
| `sram_lut_n8_w32_r6` | 3,889.4* | 1.352* | CACTI 300 K, 4 B/entry; N = 32 stands in |
| `sram_lut_n16_w32_r6` | 3,889.4* | 1.352* | CACTI 300 K, 4 B/entry; N = 32 stands in |
| `sram_lut_n32_w32_r6` | 3,889.4 | 1.352 | CACTI 300 K, 4 B/entry |
| `sram_lut_n64_w32_r6` | 6,307.9 | 1.563 | CACTI 300 K, 4 B/entry |
| `sram_lut_n128_w32_r6` | 11,064.7 | 2.184 | CACTI 300 K, 4 B/entry |
| `sram_lut_n256_w32_r6` | 20,870.9 | 3.922 | CACTI 300 K, 4 B/entry |
| `sram_lut_n8_w32_r8` | 6,663.1* | 2.123* | CACTI 300 K, 4 B/entry; N = 32 stands in |
| `sram_lut_n16_w32_r8` | 6,663.1* | 2.123* | CACTI 300 K, 4 B/entry; N = 32 stands in |
| `sram_lut_n32_w32_r8` | 6,663.1 | 2.123 | CACTI 300 K, 4 B/entry |
| `sram_lut_n64_w32_r8` | 10,080.4 | 2.456 | CACTI 300 K, 4 B/entry |
| `sram_lut_n128_w32_r8` | 16,995.8 | 3.422 | CACTI 300 K, 4 B/entry |
| `sram_lut_n256_w32_r8` | 31,812.1 | 5.923 | CACTI 300 K, 4 B/entry |
| `sram_lut_n8_w40_r1` | 367.5* | 0.181* | CACTI 300 K, 5 B/entry; N = 32 stands in |
| `sram_lut_n16_w40_r1` | 367.5* | 0.181* | CACTI 300 K, 5 B/entry; N = 32 stands in |
| `sram_lut_n64_w40_r1` | 579.1 | 0.231 | CACTI 300 K, 5 B/entry |
| `sram_lut_n128_w40_r1` | 1,000.9 | 0.336 | CACTI 300 K, 5 B/entry |
| `sram_lut_n8_w40_r2` | 1,357.4* | 0.443* | CACTI 300 K, 5 B/entry; N = 32 stands in |
| `sram_lut_n16_w40_r2` | 1,357.4* | 0.443* | CACTI 300 K, 5 B/entry; N = 32 stands in |
| `sram_lut_n8_w40_r3` | 2,073.1* | 0.718* | CACTI 300 K, 5 B/entry; N = 32 stands in |
| `sram_lut_n16_w40_r3` | 2,073.1* | 0.718* | CACTI 300 K, 5 B/entry; N = 32 stands in |
| `sram_lut_n8_w40_r4` | 2,958.7* | 1.038* | CACTI 300 K, 5 B/entry; N = 32 stands in |
| `sram_lut_n16_w40_r4` | 2,958.7* | 1.038* | CACTI 300 K, 5 B/entry; N = 32 stands in |
| `sram_lut_n8_w40_r6` | 5,914.1* | 1.878* | CACTI 300 K, 5 B/entry; N = 32 stands in |
| `sram_lut_n16_w40_r6` | 5,914.1* | 1.878* | CACTI 300 K, 5 B/entry; N = 32 stands in |
| `sram_lut_n8_w40_r8` | 8,994.8* | 2.848* | CACTI 300 K, 5 B/entry; N = 32 stands in |
| `sram_lut_n16_w40_r8` | 8,994.8* | 2.848* | CACTI 300 K, 5 B/entry; N = 32 stands in |
| `sram_lut_n32_w48_r1` | 441.4 | 0.216 | CACTI 300 K, 6 B/entry |
| `sram_lut_n64_w48_r1` | 683.3 | 0.272 | CACTI 300 K, 6 B/entry |
| `sram_lut_n128_w48_r1` | 1,161.9 | 0.390 | CACTI 300 K, 6 B/entry |
| `sram_lut_n256_w48_r1` | 2,206.3 | 0.580 | CACTI 300 K, 6 B/entry |
| `sram_lut_n512_w48_r1` | 4,466.3 | 1.155 | CACTI 300 K, 6 B/entry |
| `sram_lut_n1024_w48_r1` | 8,466.9 | 2.108 | CACTI 300 K, 6 B/entry |
| `sram_lut_n2048_w48_r1` | 18,119.1 | 3.543 | CACTI 300 K, 6 B/entry |
| `sram_lut_n4096_w48_r1` | 36,750.1 | 6.541 | CACTI 300 K, 6 B/entry |
| `sram_lut_n8192_w48_r1` | 77,238.5 | 11.684 | CACTI 300 K, 6 B/entry |
| `sram_lut_n32_w48_r2` | 1,667.0 | 0.539 | CACTI 300 K, 6 B/entry |
| `sram_lut_n64_w48_r2` | 2,519.6 | 0.637 | CACTI 300 K, 6 B/entry |
| `sram_lut_n128_w48_r2` | 4,274.9 | 0.882 | CACTI 300 K, 6 B/entry |
| `sram_lut_n256_w48_r2` | 8,484.3 | 1.625 | CACTI 300 K, 6 B/entry |
| `sram_lut_n32_w48_r3` | 2,557.0 | 0.881 | CACTI 300 K, 6 B/entry |
| `sram_lut_n64_w48_r3` | 3,889.4 | 1.021 | CACTI 300 K, 6 B/entry |
| `sram_lut_n128_w48_r3` | 6,543.5 | 1.382 | CACTI 300 K, 6 B/entry |
| `sram_lut_n256_w48_r3` | 12,887.1 | 2.534 | CACTI 300 K, 6 B/entry |
| `sram_lut_n32_w48_r4` | 4,251.1 | 1.324 | CACTI 300 K, 6 B/entry |
| `sram_lut_n64_w48_r4` | 6,184.2 | 1.532 | CACTI 300 K, 6 B/entry |
| `sram_lut_n128_w48_r4` | 9,923.2 | 2.062 | CACTI 300 K, 6 B/entry |
| `sram_lut_n256_w48_r4` | 18,175.0 | 3.603 | CACTI 300 K, 6 B/entry |
| `sram_lut_n32_w48_r6` | 7,352.7 | 2.315 | CACTI 300 K, 6 B/entry |
| `sram_lut_n64_w48_r6` | 10,601.5 | 2.651 | CACTI 300 K, 6 B/entry |
| `sram_lut_n128_w48_r6` | 16,867.4 | 3.521 | CACTI 300 K, 6 B/entry |
| `sram_lut_n256_w48_r6` | 31,367.2 | 6.247 | CACTI 300 K, 6 B/entry |
| `sram_lut_n32_w48_r8` | 11,234.9 | 3.543 | CACTI 300 K, 6 B/entry |
| `sram_lut_n64_w48_r8` | 16,088.8 | 4.039 | CACTI 300 K, 6 B/entry |
| `sram_lut_n128_w48_r8` | 25,520.0 | 5.332 | CACTI 300 K, 6 B/entry |
| `sram_lut_n256_w48_r8` | 48,026.9 | 9.565 | CACTI 300 K, 6 B/entry |
| `sram_lut_n8_w64_r1` | 629.0* | 0.296* | CACTI 300 K, 8 B/entry; N = 32 stands in |
| `sram_lut_n16_w64_r1` | 629.0* | 0.296* | CACTI 300 K, 8 B/entry; N = 32 stands in |
| `sram_lut_n32_w64_r1` | 629.0 | 0.296 | CACTI 300 K, 8 B/entry |
| `sram_lut_n64_w64_r1` | 944.5 | 0.366 | CACTI 300 K, 8 B/entry |
| `sram_lut_n128_w64_r1` | 1,562.3 | 0.513 | CACTI 300 K, 8 B/entry |
| `sram_lut_n256_w64_r1` | 2,894.8 | 0.761 | CACTI 300 K, 8 B/entry |
| `sram_lut_n512_w64_r1` | 5,822.0 | 1.526 | CACTI 300 K, 8 B/entry |
| `sram_lut_n1024_w64_r1` | 11,378.5 | 2.821 | CACTI 300 K, 8 B/entry |
| `sram_lut_n2048_w64_r1` | 21,246.9 | 4.978 | CACTI 300 K, 8 B/entry |
| `sram_lut_n4096_w64_r1` | 48,695.8 | 8.519 | CACTI 300 K, 8 B/entry |
| `sram_lut_n8192_w64_r1` | 102,186.5 | 15.026 | CACTI 300 K, 8 B/entry |
| `sram_lut_n8_w64_r2` | 2,803.9* | 0.795* | CACTI 300 K, 8 B/entry; N = 32 stands in |
| `sram_lut_n16_w64_r2` | 2,803.9* | 0.795* | CACTI 300 K, 8 B/entry; N = 32 stands in |
| `sram_lut_n32_w64_r2` | 2,803.9 | 0.795 | CACTI 300 K, 8 B/entry |
| `sram_lut_n64_w64_r2` | 3,979.7 | 0.940 | CACTI 300 K, 8 B/entry |
| `sram_lut_n128_w64_r2` | 6,307.5 | 1.279 | CACTI 300 K, 8 B/entry |
| `sram_lut_n256_w64_r2` | 10,889.8 | 1.833 | CACTI 300 K, 8 B/entry |
| `sram_lut_n8_w64_r3` | 4,370.9* | 1.313* | CACTI 300 K, 8 B/entry; N = 32 stands in |
| `sram_lut_n16_w64_r3` | 4,370.9* | 1.313* | CACTI 300 K, 8 B/entry; N = 32 stands in |
| `sram_lut_n32_w64_r3` | 4,370.9 | 1.313 | CACTI 300 K, 8 B/entry |
| `sram_lut_n64_w64_r3` | 6,140.6 | 1.517 | CACTI 300 K, 8 B/entry |
| `sram_lut_n128_w64_r3` | 9,615.6 | 2.005 | CACTI 300 K, 8 B/entry |
| `sram_lut_n256_w64_r3` | 16,480.6 | 2.794 | CACTI 300 K, 8 B/entry |
| `sram_lut_n8_w64_r4` | 6,272.1* | 1.923* | CACTI 300 K, 8 B/entry; N = 32 stands in |
| `sram_lut_n16_w64_r4` | 6,272.1* | 1.923* | CACTI 300 K, 8 B/entry; N = 32 stands in |
| `sram_lut_n32_w64_r4` | 6,272.1 | 1.923 | CACTI 300 K, 8 B/entry |
| `sram_lut_n64_w64_r4` | 8,757.0 | 2.196 | CACTI 300 K, 8 B/entry |
| `sram_lut_n128_w64_r4` | 13,589.7 | 2.858 | CACTI 300 K, 8 B/entry |
| `sram_lut_n256_w64_r4` | 23,174.9 | 3.925 | CACTI 300 K, 8 B/entry |
| `sram_lut_n8_w64_r6` | 11,065.3* | 3.431* | CACTI 300 K, 8 B/entry; N = 32 stands in |
| `sram_lut_n16_w64_r6` | 11,065.3* | 3.431* | CACTI 300 K, 8 B/entry; N = 32 stands in |
| `sram_lut_n32_w64_r6` | 11,065.3 | 3.431 | CACTI 300 K, 8 B/entry |
| `sram_lut_n64_w64_r6` | 15,295.6 | 3.875 | CACTI 300 K, 8 B/entry |
| `sram_lut_n128_w64_r6` | 23,505.7 | 4.964 | CACTI 300 K, 8 B/entry |
| `sram_lut_n256_w64_r6` | 39,841.7 | 6.715 | CACTI 300 K, 8 B/entry |
| `sram_lut_n8_w64_r8` | 17,154.3* | 5.323* | CACTI 300 K, 8 B/entry; N = 32 stands in |
| `sram_lut_n16_w64_r8` | 17,154.3* | 5.323* | CACTI 300 K, 8 B/entry; N = 32 stands in |
| `sram_lut_n32_w64_r8` | 17,154.3 | 5.323 | CACTI 300 K, 8 B/entry |
| `sram_lut_n64_w64_r8` | 23,548.4 | 5.983 | CACTI 300 K, 8 B/entry |
| `sram_lut_n128_w64_r8` | 36,029.5 | 7.601 | CACTI 300 K, 8 B/entry |
| `sram_lut_n256_w64_r8` | 61,141.2 | 10.208 | CACTI 300 K, 8 B/entry |
| `sram_lut_n8_w80_r1` | 826.6* | 0.380* | CACTI 300 K, 10 B/entry; N = 32 stands in |
| `sram_lut_n16_w80_r1` | 826.6* | 0.380* | CACTI 300 K, 10 B/entry; N = 32 stands in |
| `sram_lut_n64_w80_r1` | 1,210.0 | 0.465 | CACTI 300 K, 10 B/entry |
| `sram_lut_n128_w80_r1` | 1,956.0 | 0.640 | CACTI 300 K, 10 B/entry |
| `sram_lut_n8_w80_r2` | 3,737.1* | 1.055* | CACTI 300 K, 10 B/entry; N = 32 stands in |
| `sram_lut_n16_w80_r2` | 3,737.1* | 1.055* | CACTI 300 K, 10 B/entry; N = 32 stands in |
| `sram_lut_n8_w80_r3` | 5,869.3* | 1.768* | CACTI 300 K, 10 B/entry; N = 32 stands in |
| `sram_lut_n16_w80_r3` | 5,869.3* | 1.768* | CACTI 300 K, 10 B/entry; N = 32 stands in |
| `sram_lut_n8_w80_r4` | 8,466.2* | 2.617* | CACTI 300 K, 10 B/entry; N = 32 stands in |
| `sram_lut_n16_w80_r4` | 8,466.2* | 2.617* | CACTI 300 K, 10 B/entry; N = 32 stands in |
| `sram_lut_n8_w80_r6` | 15,036.5* | 4.741* | CACTI 300 K, 10 B/entry; N = 32 stands in |
| `sram_lut_n16_w80_r6` | 15,036.5* | 4.741* | CACTI 300 K, 10 B/entry; N = 32 stands in |
| `sram_lut_n8_w80_r8` | 23,413.5* | 7.433* | CACTI 300 K, 10 B/entry; N = 32 stands in |
| `sram_lut_n16_w80_r8` | 23,413.5* | 7.433* | CACTI 300 K, 10 B/entry; N = 32 stands in |
| `sram_lut_n32_w88_r1` | 954.9 | 0.432 | CACTI 300 K, 11 B/entry |
| `sram_lut_n64_w88_r1` | 1,381.5 | 0.525 | CACTI 300 K, 11 B/entry |
| `sram_lut_n128_w88_r1` | 2,213.3 | 0.716 | CACTI 300 K, 11 B/entry |
| `sram_lut_n256_w88_r1` | 3,978.1 | 1.053 | CACTI 300 K, 11 B/entry |
| `sram_lut_n512_w88_r1` | 8,160.5 | 2.109 | CACTI 300 K, 11 B/entry |
| `sram_lut_n1024_w88_r1` | 15,088.1 | 3.638 | CACTI 300 K, 11 B/entry |
| `sram_lut_n2048_w88_r1` | 29,440.8 | 6.852 | CACTI 300 K, 11 B/entry |
| `sram_lut_n4096_w88_r1` | 67,166.3 | 11.643 | CACTI 300 K, 11 B/entry |
| `sram_lut_n8192_w88_r1` | 140,774.0 | 20.229 | CACTI 300 K, 11 B/entry |
| `sram_lut_n32_w88_r2` | 4,314.2 | 1.216 | CACTI 300 K, 11 B/entry |
| `sram_lut_n64_w88_r2` | 5,859.5 | 1.412 | CACTI 300 K, 11 B/entry |
| `sram_lut_n128_w88_r2` | 8,920.6 | 1.853 | CACTI 300 K, 11 B/entry |
| `sram_lut_n256_w88_r2` | 14,964.2 | 2.612 | CACTI 300 K, 11 B/entry |
| `sram_lut_n32_w88_r3` | 6,789.2 | 2.049 | CACTI 300 K, 11 B/entry |
| `sram_lut_n64_w88_r3` | 9,112.0 | 2.327 | CACTI 300 K, 11 B/entry |
| `sram_lut_n128_w88_r3` | 13,684.3 | 2.963 | CACTI 300 K, 11 B/entry |
| `sram_lut_n256_w88_r3` | 22,734.4 | 4.050 | CACTI 300 K, 11 B/entry |
| `sram_lut_n32_w88_r4` | 9,807.0 | 3.045 | CACTI 300 K, 11 B/entry |
| `sram_lut_n64_w88_r4` | 13,065.1 | 3.420 | CACTI 300 K, 11 B/entry |
| `sram_lut_n128_w88_r4` | 19,430.9 | 4.285 | CACTI 300 K, 11 B/entry |
| `sram_lut_n256_w88_r4` | 32,068.2 | 5.758 | CACTI 300 K, 11 B/entry |
| `sram_lut_n32_w88_r6` | 17,450.0 | 5.548 | CACTI 300 K, 11 B/entry |
| `sram_lut_n64_w88_r6` | 23,003.0 | 6.162 | CACTI 300 K, 11 B/entry |
| `sram_lut_n128_w88_r6` | 33,833.1 | 7.587 | CACTI 300 K, 11 B/entry |
| `sram_lut_n256_w88_r6` | 55,383.1 | 10.013 | CACTI 300 K, 11 B/entry |
| `sram_lut_n32_w88_r8` | 27,205.7 | 8.731 | CACTI 300 K, 11 B/entry |
| `sram_lut_n64_w88_r8` | 35,617.5 | 9.643 | CACTI 300 K, 11 B/entry |
| `sram_lut_n128_w88_r8` | 52,092.3 | 11.767 | CACTI 300 K, 11 B/entry |
| `sram_lut_n256_w88_r8` | 84,868.2 | 15.384 | CACTI 300 K, 11 B/entry |
| `sram_lut_n8_w128_r1` | 1,716.8* | 0.724* | CACTI 300 K, 16 B/entry; N = 32 stands in |
| `sram_lut_n16_w128_r1` | 1,716.8* | 0.724* | CACTI 300 K, 16 B/entry; N = 32 stands in |
| `sram_lut_n32_w128_r1` | 1,716.8 | 0.724 | CACTI 300 K, 16 B/entry |
| `sram_lut_n64_w128_r1` | 2,367.1 | 0.872 | CACTI 300 K, 16 B/entry |
| `sram_lut_n128_w128_r1` | 3,644.4 | 1.173 | CACTI 300 K, 16 B/entry |
| `sram_lut_n256_w128_r1` | 6,194.9 | 1.730 | CACTI 300 K, 16 B/entry |
| `sram_lut_n512_w128_r1` | 12,085.9 | 3.173 | CACTI 300 K, 16 B/entry |
| `sram_lut_n1024_w128_r1` | 21,954.3 | 5.331 | CACTI 300 K, 16 B/entry |
| `sram_lut_n2048_w128_r1` | 42,439.6 | 9.931 | CACTI 300 K, 16 B/entry |
| `sram_lut_n4096_w128_r1` | 100,938.7 | 17.196 | CACTI 300 K, 16 B/entry |
| `sram_lut_n8192_w128_r1` | 209,484.4 | 29.324 | CACTI 300 K, 16 B/entry |
| `sram_lut_n8_w128_r2` | 7,722.2* | 2.073* | CACTI 300 K, 16 B/entry; N = 32 stands in |
| `sram_lut_n16_w128_r2` | 7,722.2* | 2.073* | CACTI 300 K, 16 B/entry; N = 32 stands in |
| `sram_lut_n32_w128_r2` | 7,722.2 | 2.073 | CACTI 300 K, 16 B/entry |
| `sram_lut_n64_w128_r2` | 9,945.6 | 2.349 | CACTI 300 K, 16 B/entry |
| `sram_lut_n128_w128_r2` | 14,352.6 | 2.949 | CACTI 300 K, 16 B/entry |
| `sram_lut_n256_w128_r2` | 23,077.7 | 4.026 | CACTI 300 K, 16 B/entry |
| `sram_lut_n8_w128_r3` | 12,331.4* | 3.570* | CACTI 300 K, 16 B/entry; N = 32 stands in |
| `sram_lut_n16_w128_r3` | 12,331.4* | 3.570* | CACTI 300 K, 16 B/entry; N = 32 stands in |
| `sram_lut_n32_w128_r3` | 12,331.4 | 3.570 | CACTI 300 K, 16 B/entry |
| `sram_lut_n64_w128_r3` | 15,682.5 | 3.964 | CACTI 300 K, 16 B/entry |
| `sram_lut_n128_w128_r3` | 22,294.6 | 4.832 | CACTI 300 K, 16 B/entry |
| `sram_lut_n256_w128_r3` | 35,407.3 | 6.381 | CACTI 300 K, 16 B/entry |
| `sram_lut_n8_w128_r4` | 17,033.2* | 5.392* | CACTI 300 K, 16 B/entry; N = 32 stands in |
| `sram_lut_n16_w128_r4` | 17,033.2* | 5.392* | CACTI 300 K, 16 B/entry; N = 32 stands in |
| `sram_lut_n32_w128_r4` | 17,033.2 | 5.392 | CACTI 300 K, 16 B/entry |
| `sram_lut_n64_w128_r4` | 21,494.2 | 5.926 | CACTI 300 K, 16 B/entry |
| `sram_lut_n128_w128_r4` | 30,244.5 | 7.108 | CACTI 300 K, 16 B/entry |
| `sram_lut_n256_w128_r4` | 47,629.8 | 9.215 | CACTI 300 K, 16 B/entry |
| `sram_lut_n8_w128_r6` | 30,604.4* | 10.023* | CACTI 300 K, 16 B/entry; N = 32 stands in |
| `sram_lut_n16_w128_r6` | 30,604.4* | 10.023* | CACTI 300 K, 16 B/entry; N = 32 stands in |
| `sram_lut_n32_w128_r6` | 30,604.4 | 10.023 | CACTI 300 K, 16 B/entry |
| `sram_lut_n64_w128_r6` | 38,218.9 | 10.900 | CACTI 300 K, 16 B/entry |
| `sram_lut_n128_w128_r6` | 53,132.2 | 12.853 | CACTI 300 K, 16 B/entry |
| `sram_lut_n256_w128_r6` | 82,808.7 | 16.335 | CACTI 300 K, 16 B/entry |
| `sram_lut_n8_w128_r8` | 47,948.3* | 15.983* | CACTI 300 K, 16 B/entry; N = 32 stands in |
| `sram_lut_n16_w128_r8` | 47,948.3* | 15.983* | CACTI 300 K, 16 B/entry; N = 32 stands in |
| `sram_lut_n32_w128_r8` | 47,948.3 | 15.983 | CACTI 300 K, 16 B/entry |
| `sram_lut_n64_w128_r8` | 59,491.7 | 17.286 | CACTI 300 K, 16 B/entry |
| `sram_lut_n128_w128_r8` | 82,166.3 | 20.193 | CACTI 300 K, 16 B/entry |
| `sram_lut_n256_w128_r8` | 127,278.8 | 25.374 | CACTI 300 K, 16 B/entry |

## Notes

1. **LUT numbers are the revised (2026-10-23) results.** The earlier read-only register-file
   runs left the idle write port's data toggling every cycle and overstated read-only power
   2–4×; they are no longer used. CACTI moved from 360 K to 300 K (the owner's
   choice, matched to the synthesis library's 25 °C): same area and access energy, 0.31–0.35×
   the leakage. Still open on cmp00: whether power includes the input nets that fan out into
   the table (for the read-only corner only the address nets, ≤ ~10% at the smallest N).
2. **The baselines are at a different clock transition from the rest.** `add_fp16`,
   `mul_fp16`, `mul_int8` and `add_int16` are 5.0 ns runs; the register files
   and the pe designs added on 2026-10-22 are 0.1 ns. Logic area moves by up to
   ±10% between the two for designs at ~0 ps slack. The pe_sweep rebuild at 0.1 ns with the
   owner's revised MAC precision and names (`pe_sweep_v2`) was running at this sync.
3. **CACTI cannot model N = 8 or 16 at any width** ("no valid data array organizations
   found"), nor tables under 64 bytes. Those cells use the smallest modelled table (`*`).
4. **Multi-port vs copies.** In CACTI, one table with R read ports has 1.70–3.56×
   the area of R single-port copies (180 cases) and 1.04–2.76× the
   read-only power. For register files it is the other way round: 0.29–0.63× the area and
   0.51–0.98× the read-only power of R copies (60 cases), because the
   flip-flops are shared and only the read muxes are replicated.
5. **wa = int8 entries are exact** (8 + ⌈log2 v⌉ bits), so no partial sum overflows. The adds
   stay fp16, as specified.
6. **The converter MAC opt leaves out is small.** A standalone `CW_fp_i2flt` → fp16 is
   70–116 µm² of logic for the int-wq × int8 products (10 to 16 bits), and an
   exact RTL converter 53–74 µm² where no rounding is needed (≤ 12 bits).
   See [02](../02-int-to-fp-converter-cost/README.md).
7. **`mul_int2xfp16` is only 41 µm²**: every int2
   value converts to fp16 with an all-zero mantissa, so Genus removes the significand
   multiplier and only sign and exponent logic remain. From int3 up there is a real multiplier.
8. **Ternary tables are large**: 128, 1,024, 4,096, 8,192 entries
   at v = 4, 6, 7, 8 (half with symm). Register files are costed only up to
   v = 6 (1,024 entries); SRAM at every v.
9. **fp16 units close timing at ~0 ps slack** at 2 ns (`mul_fp16` 0 ps,
   `add_fp16` 1 ps), so their area includes upsizing. At a 4 ns clock,
   `add_fp16` is 344 µm² and `mul_fp16`
   346 µm²; the tables use the 2 ns numbers.
