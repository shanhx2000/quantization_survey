# PE sweep: logic-only area and power of add, mul, MAC and counters

Generated 2026-10-15 by `scripts/make_report.py` from `pe_summary.csv`.

## Summary

* Integer adders are cheap: int8 add is 15.5 µm². FP addition is far costlier: fp8 add is 170.6 µm² (11× int8 add, 2.1× fp8 mul), fp16 add 515.1 µm².
* Integer multipliers grow roughly with the square of the width: int4 / int8 / int16 mul = 28.2 / 142.3 / 548.4 µm². fp mul is smaller than the int mul of the same width (fp16 383.7 µm², fp8 81.3 µm²) because only the mantissas are multiplied.
* In MACs the accumulator format dominates: with int8 inputs, the logic is 178.7 µm² into int16, 1,763.2 µm² into fp16 and 2,966.0 µm² into fp32 (including the int→fp conversion).
* Counters, 8-bit: +1 logic 7.4 µm², ±1 logic 19.4 µm², against 15.5 µm² for an int8 adder. The 8 counter flip-flops add another 19.2 µm².

## Setup

* **Flow:** the micro26rcf Genus flow (`scripts/run_syn.sh` → `syn/synth/run*.csh` →
  `syn_RISC*.scr`), copied into this folder. Genus 21.1, TSMC 28nm HPC+ 9-track
  (RVT/HVT/LVT, TT 0.9 V 25 °C), 500 MHz (2 ns clock), `set_max_area 0`.
* **Measured module:** every design is a wrapper top that registers every input and
  output (as in `src/v2_inter_pe/v2_systolic_inter_pe_top.v`) around the measured module
  `u_core`. All numbers are for `u_core` unless a column says *wrapper*.
* **Logic only:** combinational cells in `u_core`. Flip-flops (MAC accumulators, counter
  registers) and clock-gating cells are listed separately. Areas come from
  `report gates -instance_hier u_core`, power from `report_power -inst u_core -by_category`.
* **Power:** Genus vectorless estimate. Data inputs are random (P(1)=0.5, 0.5
  toggles/bit/cycle). Counters are enabled every cycle; the ±1 counter changes direction
  about every 50 cycles. Static = leakage, dynamic = internal + switching.
* **Formats:** int = two's complement. fp8 = E4M3 with IEEE-style encoding (exponent
  all-ones = Inf/NaN, max 240). FP units are Genus ChipWare with `ieee_compliance=0`
  (denormals read as zero) and round-to-nearest-even.
* **Units:** int add keeps W bits (wraps); int mul gives the full 2W-bit product; fp
  results are rounded to the operand format. MAC: `acc <= acc + convert(mul_x(a, b))`,
  with the accumulator in format y.

## Add and multiply (logic only)

### Add

| Type | Logic area (µm²) | Static (mW) | Dynamic (mW) | Total (mW) | Slack (ps) |
|---|---|---|---|---|---|
| int4 | 6.9 | 0.0001 | 0.010 | 0.010 | 1557 |
| int8 | 15.5 | 0.0001 | 0.024 | 0.024 | 1264 |
| fp8 | 170.6 | 0.0076 | 0.505 | 0.513 | 3 |
| int16 | 32.8 | 0.0004 | 0.053 | 0.053 | 715 |
| fp16 | 515.1 | 0.026 | 1.504 | 1.530 | 1 |
| fp32 | 1,411.3 | 0.083 | 3.594 | 3.676 | 0 |

### Multiply

| Type | Logic area (µm²) | Static (mW) | Dynamic (mW) | Total (mW) | Slack (ps) |
|---|---|---|---|---|---|
| int4 | 28.2 | 0.0004 | 0.048 | 0.049 | 1275 |
| int8 | 142.3 | 0.0025 | 0.242 | 0.244 | 730 |
| fp8 | 81.3 | 0.0020 | 0.221 | 0.223 | 395 |
| int16 | 548.4 | 0.015 | 1.570 | 1.585 | 1 |
| fp16 | 383.7 | 0.0099 | 1.054 | 1.064 | 0 |
| fp32 | 2,064.4 | 0.093 | 4.886 | 4.979 | 0 |

## MAC: mul{x}add{y} (logic only)

Logic area µm² / logic power mW:

| mul \ add | int16 | fp16 | fp32 |
|---|---|---|---|
| int4 | 61 / 0.11 | 880 / 2.15 | 1,947 / 4.60 |
| int8 | 179 / 0.33 | 1,763 / 3.81 | 2,966 / 6.41 |
| fp8 | 336 / 0.81 | 729 / 1.98 | 1,871 / 4.51 |
| int16 | 305 / 0.76 | 3,355 / 5.91 | 6,263 / 12.39 |
| fp16 | 1,275 / 2.72 | 1,803 / 4.19 | 3,253 / 7.27 |
| fp32 | 3,760 / 8.31 | 6,874 / 13.71 | 8,300 / 16.38 |

Detail, including the accumulator flip-flops:

| MAC | Logic area (µm²) | Logic static / dynamic (mW) | Accumulator flops: area (µm²) / power (mW) | Slack (ps) | Product → accumulator conversion |
|---|---|---|---|---|---|
| `mac_mulint4_addint16` | 61.5 | 0.0016 / 0.113 | 36.3 / 0.308 | 446 | sign-extend 8b->16b |
| `mac_mulint4_addfp16` | 880.5 | 0.051 / 2.099 | 36.3 / 0.384 | 0 | int8->fp16 (CW_fp_i2flt) |
| `mac_mulint4_addfp32` | 1,947.0 | 0.113 / 4.483 | 92.1 / 2.449 | 0 | int8->fp32 (CW_fp_i2flt) |
| `mac_mulint8_addint16` | 178.7 | 0.0050 / 0.324 | 36.3 / 0.308 | 110 | none |
| `mac_mulint8_addfp16` | 1,763.2 | 0.119 / 3.693 | 37.3 / 0.353 | 0 | int16->fp16 (CW_fp_i2flt) |
| `mac_mulint8_addfp32` | 2,966.0 | 0.193 / 6.214 | 103.8 / 2.434 | 0 | int16->fp32 (CW_fp_i2flt) |
| `mac_mulfp8_addint16` | 335.5 | 0.019 / 0.794 | 36.3 / 0.334 | 1 | fp8->fp16 (fp_up), fp8->int16 (CW_fp_flt2i) |
| `mac_mulfp8_addfp16` | 729.3 | 0.040 / 1.940 | 36.3 / 0.355 | 0 | fp8->fp16 (fp_up, exact) |
| `mac_mulfp8_addfp32` | 1,871.4 | 0.114 / 4.401 | 93.2 / 2.472 | 0 | fp8->fp32 (fp_up, exact) |
| `mac_mulint16_addint16` | 305.3 | 0.0068 / 0.752 | 36.3 / 0.310 | 42 | keep low 16 of 32 product bits (wraps) |
| `mac_mulint16_addfp16` | 3,354.6 | 0.250 / 5.662 | 51.4 / 0.848 | 0 | int32->fp16 (CW_fp_i2flt) |
| `mac_mulint16_addfp32` | 6,263.3 | 0.451 / 11.940 | 103.8 / 2.442 | 0 | int32->fp32 (CW_fp_i2flt) |
| `mac_mulfp16_addint16` | 1,275.1 | 0.079 / 2.641 | 36.3 / 0.337 | 0 | fp16->int16 (CW_fp_flt2i) |
| `mac_mulfp16_addfp16` | 1,803.2 | 0.114 / 4.078 | 36.3 / 0.392 | 0 | none |
| `mac_mulfp16_addfp32` | 3,253.1 | 0.209 / 7.059 | 103.8 / 2.457 | 0 | fp16->fp32 (fp_up, exact) |
| `mac_mulfp32_addint16` | 3,760.5 | 0.244 / 8.070 | 36.3 / 0.335 | 0 | fp32->int16 (CW_fp_flt2i) |
| `mac_mulfp32_addfp16` | 6,874.2 | 0.506 / 13.199 | 51.4 / 1.196 | 0 | fp32->fp16 (fp_down, RNE) |
| `mac_mulfp32_addfp32` | 8,300.2 | 0.598 / 15.778 | 103.8 / 2.440 | 0 | none |

## Counters (logic only)

Wrap-around counters with enable; the ±1 counter also has a direction input.

| Bits (max count) | +1 logic area (µm²) | +1 logic power (mW) | ±1 logic area (µm²) | ±1 logic power (mW) | +1 flops: area (µm²) / power (mW) | ±1 flops: area (µm²) / power (mW) |
|---|---|---|---|---|---|---|
| 4 (15) | 2.9 | 0.0018 | 7.7 | 0.0048 | 9.3 / 0.047 | 9.6 / 0.066 |
| 6 (63) | 5.2 | 0.0030 | 13.0 | 0.0062 | 13.9 / 0.072 | 14.6 / 0.109 |
| 8 (255) | 7.4 | 0.0038 | 19.4 | 0.0081 | 18.4 / 0.097 | 19.2 / 0.125 |
| 10 (1023) | 9.7 | 0.0043 | 25.1 | 0.0094 | 22.9 / 0.121 | 24.4 / 0.184 |

## Notes

1. **fp8 adder:** Genus 21.1 has no `CW_fp8_add` (documented, but elaboration
   black-boxes it), and `CW_fp_add` needs at least 5 exponent and 5 mantissa bits. fp8
   addition therefore uses an RTL adder (`fp_add_ftz` in `src/pe/pe_lib.v`) with the same
   rounding and denormal rules. Built at fp16 as a calibration point, it needs
   507.3 µm² / 1.366 mW, against
   515.1 µm² / 1.530 mW for ChipWare's fp16 adder.
2. **Single-cycle MACs are timing-limited.** Multiply, conversion and add must fit in
   one 2 ns cycle. MACs with an fp operand or accumulator end at ~0 ps slack, so Genus
   upsized cells, and their logic area is well above the sum of a separate multiplier and
   adder: `mac_mulfp16_addfp16` 1,803 µm² vs 899 µm² for `mul_fp16` + `add_fp16` (2.01×, slack 0 ps); `mac_mulfp8_addfp32` 1,871 µm² vs 1,493 µm² for `mul_fp8` + `add_fp32` (1.25×, slack 0 ps). An integer MAC with slack to spare stays close to its parts:
   `mac_mulint8_addint16` 179 µm² vs 175 µm² for `mul_int8` + `add_int16` (1.02×, slack 110 ps). A pipeline register between multiply and add would separate the logic cost
   from this timing effect.
3. **Unusual pairs, included to complete the grid:** `mac_mulint16_addint16` keeps only
   the low 16 bits of the 32-bit product. The fp → int16 MACs round every product to an
   integer before accumulating.
4. **Clock transition in the flow constraints:** `my.constraints.tcl` sets
   `set_clock_transition 5` (5 ns on a 2 ns clock). This inflates flip-flop internal
   power; on `buffer_n4` a 0.05 ns transition cut flip-flop power about 4× and left logic
   power unchanged. The logic-only numbers above are therefore essentially unaffected,
   but treat the flip-flop and wrapper power columns as upper bounds.
5. **Timing:** every design meets 500 MHz. 22 of 39 designs end at
   ≤5 ps slack (see the Slack columns), so their area includes upsizing to meet timing.
6. **Checks:** 39/39 designs pass their RTL tests (Python golden data →
   VCS with the ChipWare simulation models → bit-accurate check). 4- and 8-bit add/mul
   are tested on every input pair, other add/mul on 5000 random vectors, MACs over 4000
   cycles with random resets, counters over 6000 cycles. Synthesis runs with unresolved
   references or errors: none.

## All designs

Areas in µm², power in mW. *Wrapper* = the whole design including the IO registers.

| Design | Logic area | Flop area | Clock-gate area | u_core area | Logic power | Flop power | Clock-gate power | u_core power | Wrapper total area / power | Slack (ps) | RTL test |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `add_int4` | 6.9 | 0 | 0 | 6.9 | 0.010 | 0 | 0 | 0.010 | 34.1 / 0.163 | 1557 | PASS |
| `add_int8` | 15.5 | 0 | 0 | 15.5 | 0.024 | 0 | 0 | 0.024 | 69.9 / 0.332 | 1264 | PASS |
| `add_fp8` | 170.6 | 0 | 0 | 170.6 | 0.513 | 0 | 0 | 0.513 | 225.0 / 0.836 | 3 | PASS |
| `add_int16` | 32.8 | 0 | 0 | 32.8 | 0.053 | 0 | 0 | 0.053 | 141.6 / 0.672 | 715 | PASS |
| `add_fp16` | 515.1 | 0 | 0 | 515.1 | 1.530 | 0 | 0 | 1.530 | 624.0 / 2.181 | 1 | PASS |
| `add_fp32` | 1,411.3 | 0 | 0 | 1,411.3 | 3.676 | 0 | 0 | 3.676 | 1,629.1 / 4.954 | 0 | PASS |
| `mul_int4` | 28.2 | 0 | 0 | 28.2 | 0.049 | 0 | 0 | 0.049 | 64.5 / 0.234 | 1275 | PASS |
| `mul_int8` | 142.3 | 0 | 0 | 142.3 | 0.244 | 0 | 0 | 0.244 | 214.8 / 0.638 | 730 | PASS |
| `mul_fp8` | 81.3 | 0 | 0 | 81.3 | 0.223 | 0 | 0 | 0.223 | 135.7 / 0.539 | 395 | PASS |
| `mul_int16` | 548.4 | 0 | 0 | 548.4 | 1.585 | 0 | 0 | 1.585 | 693.9 / 2.898 | 1 | PASS |
| `mul_fp16` | 383.7 | 0 | 0 | 383.7 | 1.064 | 0 | 0 | 1.064 | 492.5 / 2.141 | 0 | PASS |
| `mul_fp32` | 2,064.4 | 0 | 0 | 2,064.4 | 4.979 | 0 | 0 | 4.979 | 2,292.7 / 7.581 | 0 | PASS |
| `add_fp16_rtl` | 507.3 | 0 | 0 | 507.3 | 1.366 | 0 | 0 | 1.366 | 616.1 / 2.005 | 0 | PASS |
| `mac_mulint4_addint16` | 61.5 | 36.3 | 0 | 97.8 | 0.114 | 0.308 | 0 | 0.422 | 152.2 / 0.667 | 446 | PASS |
| `mac_mulint4_addfp16` | 880.5 | 36.3 | 0 | 916.8 | 2.150 | 0.384 | 0 | 2.534 | 971.2 / 2.784 | 0 | PASS |
| `mac_mulint4_addfp32` | 1,947.0 | 92.1 | 0 | 2,039.1 | 4.596 | 2.449 | 0 | 7.045 | 2,129.8 / 7.617 | 0 | PASS |
| `mac_mulint8_addint16` | 178.7 | 36.3 | 0 | 215.0 | 0.329 | 0.308 | 0 | 0.637 | 287.5 / 1.034 | 110 | PASS |
| `mac_mulint8_addfp16` | 1,763.2 | 37.3 | 0 | 1,800.5 | 3.813 | 0.353 | 0 | 4.165 | 1,873.1 / 4.962 | 0 | PASS |
| `mac_mulint8_addfp32` | 2,966.0 | 103.8 | 0 | 3,069.9 | 6.406 | 2.434 | 0 | 8.840 | 3,178.7 / 9.752 | 0 | PASS |
| `mac_mulfp8_addint16` | 335.5 | 36.3 | 0 | 371.8 | 0.813 | 0.334 | 0 | 1.147 | 444.4 / 1.528 | 1 | PASS |
| `mac_mulfp8_addfp16` | 729.3 | 36.3 | 0 | 765.6 | 1.980 | 0.355 | 0 | 2.334 | 838.2 / 3.086 | 0 | PASS |
| `mac_mulfp8_addfp32` | 1,871.4 | 93.2 | 0 | 1,964.6 | 4.515 | 2.472 | 0 | 6.987 | 2,073.5 / 7.848 | 0 | PASS |
| `mac_mulint16_addint16` | 305.3 | 36.3 | 0 | 341.6 | 0.759 | 0.310 | 0 | 1.069 | 450.4 / 1.960 | 42 | PASS |
| `mac_mulint16_addfp16` | 3,354.6 | 51.4 | 0 | 3,406.0 | 5.912 | 0.848 | 0 | 6.760 | 3,515.8 / 8.186 | 0 | PASS |
| `mac_mulint16_addfp32` | 6,263.3 | 103.8 | 0 | 6,367.2 | 12.392 | 2.442 | 0 | 14.833 | 6,512.3 / 16.425 | 0 | PASS |
| `mac_mulfp16_addint16` | 1,275.1 | 36.3 | 0 | 1,311.4 | 2.720 | 0.337 | 0 | 3.057 | 1,420.3 / 4.141 | 0 | PASS |
| `mac_mulfp16_addfp16` | 1,803.2 | 36.3 | 0 | 1,839.5 | 4.192 | 0.392 | 0 | 4.584 | 1,948.3 / 5.886 | 0 | PASS |
| `mac_mulfp16_addfp32` | 3,253.1 | 103.8 | 0 | 3,356.9 | 7.268 | 2.457 | 0 | 9.725 | 3,504.7 / 11.278 | 0 | PASS |
| `mac_mulfp32_addint16` | 3,760.5 | 36.3 | 0 | 3,796.8 | 8.313 | 0.335 | 0 | 8.649 | 3,989.3 / 11.046 | 0 | PASS |
| `mac_mulfp32_addfp16` | 6,874.2 | 51.4 | 0 | 6,925.6 | 13.705 | 1.196 | 0 | 14.901 | 7,109.7 / 17.274 | 0 | PASS |
| `mac_mulfp32_addfp32` | 8,300.2 | 103.8 | 0 | 8,404.1 | 16.376 | 2.440 | 0 | 18.816 | 8,623.3 / 21.302 | 0 | PASS |
| `cnt_up_w4` | 2.9 | 9.3 | 1.9 | 14.1 | 0.0018 | 0.047 | 0.0035 | 0.053 | 25.5 / 0.080 | 1148 | PASS |
| `cnt_up_w6` | 5.2 | 13.9 | 1.9 | 20.9 | 0.0030 | 0.072 | 0.0038 | 0.079 | 36.8 / 0.115 | 1101 | PASS |
| `cnt_up_w8` | 7.4 | 18.4 | 1.9 | 27.7 | 0.0038 | 0.097 | 0.0041 | 0.105 | 48.1 / 0.147 | 1011 | PASS |
| `cnt_up_w10` | 9.7 | 22.9 | 1.9 | 34.5 | 0.0043 | 0.121 | 0.0045 | 0.129 | 59.5 / 0.179 | 998 | PASS |
| `cnt_updn_w4` | 7.7 | 9.6 | 1.9 | 19.2 | 0.0048 | 0.066 | 0.0035 | 0.075 | 32.8 / 0.114 | 1177 | PASS |
| `cnt_updn_w6` | 13.0 | 14.6 | 1.9 | 29.5 | 0.0062 | 0.109 | 0.0038 | 0.119 | 47.6 / 0.165 | 1177 | PASS |
| `cnt_updn_w8` | 19.4 | 19.2 | 1.9 | 40.4 | 0.0081 | 0.125 | 0.0041 | 0.137 | 63.1 / 0.211 | 881 | PASS |
| `cnt_updn_w10` | 25.1 | 24.4 | 1.9 | 51.4 | 0.0094 | 0.184 | 0.0045 | 0.198 | 78.6 / 0.279 | 990 | PASS |

## Reproduce (from `playground/pe_sweep`)

```bash
python scripts/gen_rtl.py       # RTL (src/pe/pe_gen.v), testbenches, designs.txt/.json
scripts/run_test.sh             # RTL tests
scripts/run_syn.sh              # synthesis, one design after another (run inside tmux)
python scripts/collect.py       # -> pe_summary.csv
python scripts/make_report.py   # -> REPORT.md
```
