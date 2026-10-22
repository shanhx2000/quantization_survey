# 02 — How large is the int → fp16 converter after the multiplier?

Written 2026-10-22. Asked by the owner after [01](../01-gemm-cost-per-frame/README.md) noted
that *MAC opt* with wa = int8 needs an int → fp16 conversion of the product before the fp16
add, and quoted `mac_mulint8_addfp16` at 1,763 µm² of logic against 657 µm² for
`mul_int8` + `add_fp16`. The owner expected the converter to be small.

## Answer

**The converter is small; the gap is timing.** Inside `mac_mulint8_addfp16` the converter's
cells (`CW_fp_i2flt`, int16 → fp16) take **272 µm², 15% of the logic**. Most of the
1,106 µm² gap is the multiplier and adder growing to close timing: multiply, convert and add
sit in one 2 ns cycle with the accumulator fed back, the design ends at 0 ps slack, and Genus
upsized the int8 multiplier **4.1×** (142 → 588 µm²) and the fp16 adder **1.36×**
(515 → 702 µm²).

| Part of the 1,106 µm² gap | µm² | Share |
|---|---|---|
| Multiplier upsizing (588.4 − 142.3) | 446 | 40% |
| Converter cells | 272 | 25% |
| Glue: cells Genus renamed while restructuring across the block boundaries | 201 | 18% |
| fp16 adder upsizing (702.2 − 515.1) | 187 | 17% |

The glue cannot be assigned to a block. Even counting all of it as converter, the converter
is at most 473 µm² (27% of the logic).

Power tells the same story where it can be split: only `u_mul` stays a separate hierarchy in
the power report, and inside the MAC it draws 0.979 mW against 0.244 mW standalone (4.0×).
The converter and adder are flattened into `u_core`, so their power cannot be separated.

## Breakdown of every int → fp MAC, and two references

Logic area in µm², from `mac_area_breakdown.py` (below). *In MAC / standalone* compares the
block inside the MAC with the standalone pe_sweep design of the same type.

| MAC | Slack (ps) | Multiplier: in MAC / standalone | Converter | Adder: in MAC / standalone | Glue | Logic |
|---|---|---|---|---|---|---|
| `mac_mulint4_addfp16` | 0 | 98.8 / 28.2 (3.5×) | 137.6 (int8 → fp16) | 504.0 / 515.1 (0.98×) | 140.1 | 880.5 |
| `mac_mulint8_addfp16` | 0 | 588.4 / 142.3 (4.1×) | 271.5 (int16 → fp16) | 702.2 / 515.1 (1.36×) | 201.1 | 1,763.2 |
| `mac_mulint16_addfp16` | 0 | 2,014.7 / 548.4 (3.7×) | 311.3 (int32 → fp16) | 776.8 / 515.1 (1.51×) | 251.7 | 3,354.6 |
| `mac_mulint8_addfp32` | 0 | 681.8 / 142.3 (4.8×) | 332.9 (int16 → fp32) | 1,631.6 / 1,411.3 (1.16×) | 319.8 | 2,966.0 |
| `mac_mulint8_addint16` (no converter) | 110 | 145.9 / 142.3 (1.03×) | — | 32.8 / 32.8 (1.00×) | 0 | 178.7 |
| `mac_mulfp16_addfp16` (no converter) | 0 | 927.6 / 383.7 (2.4×) | — | 562.0 / 515.1 (1.09×) | 313.6 | 1,803.2 |

* The converter is 9–16% of the logic in every int → fp MAC.
* **Timing, not conversion, drives the inflation.** The integer MAC with 110 ps of slack keeps
  its parts at standalone size (1.03×). `mac_mulfp16_addfp16`, which has no converter at all,
  still ends at 0 ps and its multiplier still grows 2.4×.
* The critical path of `mac_mulint8_addfp16` runs `a_q` → multiplier (to 210 ps) → converter
  (to ~670 ps) → adder → `acc` (`rpt/mac_mulint8_addfp16.timing_100.rpt`, path 1).

## Width matters for MAC opt

In *MAC opt* the converter input is the int-wq × int8 product, not int16. Products of int3 or
int4 with int8 have magnitude at most 512 or 1,024, which fp16 holds exactly (11 significant
bits). So for wq ≤ 4 the converter needs no rounding, only sign handling, a leading-zero
count and a shift. For wq = 6 and 8 (magnitude up to 4,096 and 16,384), it must round.

## Not known yet

* **A standalone converter.** All numbers above come from inside a timing-bound MAC. A
  registered `CW_fp_i2flt` with isize = 11, 12, 14 and 16 (the int-wq × int8 products for
  wq = 3, 4, 6, 8) → fp16 would give a converter cost to add to 01's *MAC opt* row.
* **A pipelined MAC** (a register between multiplier/converter and adder) would show how much
  of the 4× multiplier growth goes away once timing is relaxed.

Both are in the data-collection list on cmp00:
`~/isca26hw/micro26rcf/playground/todo/mac_lut_data_to_collect.md`.

## Method

`mac_area_breakdown.py` reads the per-cell areas from each run's `rpt/<design>.gates.rpt`,
applies them to every instance in `gate/<design>.v`, and groups the instances in
`mac_core_*` by name: the `u_mul` hierarchy or `mul_*` cells, `u_cvt*`, `u_add*`, the
`acc_reg` flops, and everything else as glue. For every design above, the sum matches
`core_area_um2` in `pe_summary.csv` exactly, and the sum without flops matches
`logic_area_um2`. It needs the full sweep copy, which is not in git:

```bash
# from quantization_survey/hardware/
python3 mac_lut_tradeoff/02-int-to-fp-converter-cost/mac_area_breakdown.py pe_sweep \
    mac_mulint4_addfp16 mac_mulint8_addfp16 mac_mulint16_addfp16 mac_mulint8_addfp32 \
    mac_mulint8_addint16 mac_mulfp16_addfp16
```
