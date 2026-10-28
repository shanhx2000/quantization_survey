# 02 — How large is the int → fp16 converter after the multiplier?

Written 2026-10-22; **rewritten 2026-10-28 on the rebuilt pe sweep** (`pe_sweep_v2`: every
design at the flow's 0.1 ns clock transition, names `op_{a}x{b}_{out}`). Asked by the owner
after [01](../01-gemm-cost-per-frame/README.md) noted that *MAC opt* with wa = int8 needs an
int → fp16 conversion of the product before the fp16 add, and that the single-cycle
int8 × int8 → fp16 MAC was far larger than a multiplier plus an adder. The owner expected the
converter to be small. The first version used the older 5 ns runs; its numbers are at the
end, and they support the same answer.

## Answer

**The converter is small; the gap is timing.** In `mac_int8xint8_fp16` (int8 × int8 → int16
→ fp16, accumulated in fp16) the converter's cells (`CW_fp_i2flt`, int16 → fp16) take
**230 µm², 15% of the 1,508 µm² of logic**. Multiply, convert and add sit in one 2 ns cycle
with the accumulator fed back, and the design ends at 0 ps slack. To meet that, Genus
upsized the int8 multiplier **3.7×** (144 → 532 µm²) and the fp16 adder 1.11× (526 →
583 µm²).

| Part of the 839 µm² gap to `mul_int8xint8_int16` + `add_fp16xfp16_fp16` (670 µm²) | µm² | Share |
|---|---|---|
| Multiplier upsizing (531.6 − 143.9) | 388 | 46% |
| Converter cells | 230 | 27% |
| Glue: cells Genus renamed while restructuring across the block boundaries | 165 | 20% |
| fp16 adder upsizing (582.5 − 525.8) | 57 | 7% |

The glue cannot be assigned to a block. Even counting all of it as converter, the converter
is at most 394 µm² (26% of the logic).

Power tells the same story where it can be split: only `u_mul` stays a separate hierarchy in
the power report, and inside the MAC it draws 0.880 mW against 0.261 mW standalone (3.4×).
The converter and adder are flattened into `u_core`, so their power cannot be separated.

## Breakdown of the int → fp MACs, and two references

Logic area in µm², from `mac_area_breakdown.py` (below), all at 0.1 ns. *In MAC / standalone*
compares the block inside the MAC with the standalone `pe_sweep_v2` unit of the same type.

| MAC | Slack (ps) | Multiplier: in MAC / standalone | Converter | Adder: in MAC / standalone | Glue | Logic |
|---|---|---|---|---|---|---|
| `mac_int4xint4_fp16` | 0 | 90.3 / 28.2 (3.2×) | 131.2 (int8 → fp16) | 456.5 / 525.8 (0.87×) | 118.8 | 796.8 |
| `mac_int8xint8_fp16` | 0 | 531.6 / 143.9 (3.7×) | 229.6 (int16 → fp16) | 582.5 / 525.8 (1.11×) | 164.7 | 1,508.3 |
| `mac_int8xint8_fp32` | 0 | 717.3 / 143.9 (5.0×) | 338.7 (int16 → fp32) | 1,634.6 / 1,489.1 (1.10×) | 309.0 | 2,999.6 |
| `mac_int16xint16_fp32` | 0 | 2,522.0 / 537.3 (4.7×) | 741.4 (int32 → fp32) | 2,250.4 / 1,489.1 (1.51×) | 482.5 | 5,996.2 |
| `mac_int8xint8_int16` (no converter) | 344 | 145.7 / 143.9 (1.01×) | — | 32.8 / 32.8 (1.00×) | 0 | 178.4 |
| `mac_fp16xfp16_fp16` (no converter) | 0 | 872.5 / 397.8 (2.2×) | — | 513.4 / 525.8 (0.98×) | 293.1 | 1,679.1 |

* The converter is 11–17% of the logic in every int → fp MAC.
* **Timing, not conversion, drives the inflation.** The integer MAC with 344 ps of slack keeps
  its parts at standalone size (1.01×). `mac_fp16xfp16_fp16`, which has no converter at all,
  still ends at 0 ps and its multiplier still grows 2.2×.
* The critical path of `mac_int8xint8_fp16` runs `a_q` → multiplier (to ~344 ps) →
  converter (to ~725 ps) → adder → `acc_reg` (`rpt/mac_int8xint8_fp16.timing_100.rpt`,
  path 1, 0 ps slack).
* The int16 × int16 → fp16 MAC of the first version is gone: the owner dropped MACs whose
  accumulator is narrower than the operands (assumption revision 9 on cmp00).
  int16 × int16 → fp32 takes its place.

## Width matters for MAC opt

In *MAC opt* the converter input is the int-q_W × int8 product, not int16. Products of int3 or
int4 with int8 have magnitude at most 512 or 1,024, which fp16 holds exactly (11 significant
bits). So for q_W ≤ 4 the converter needs no rounding, only sign handling, a leading-zero
count and a shift. For q_W = 6 and 8 (magnitude up to 4,096 and 16,384), it must round.

## Standalone converter and pipelined MAC

**Standalone converter**, registered like every pe sweep design, int → fp16, 0.1 ns:

| Input (product of) | `CW_fp_i2flt`: logic µm² / mW / slack | Exact RTL, no rounding: logic µm² / mW |
|---|---|---|
| int10 (int2 × int8) | 69.7 / 0.198 / 20 ps | 52.9 / 0.134 |
| int11 (int3 × int8) | 73.7 / 0.210 / 4 ps | 63.6 / 0.160 |
| int12 (int4 × int8) | 80.5 / 0.235 / 1 ps | 73.6 / 0.184 |
| int14 (int6 × int8) | 101.1 / 0.276 / 0 ps | — (needs rounding) |
| int16 (int8 × int8) | 116.2 / 0.309 / 5 ps | — (needs rounding) |

So the int16 → fp16 converter is **116 µm² on its own**, against 230 µm² of converter cells
inside the single-cycle MAC.

**Pipelined MAC** (`mac_int8xint8_fp16_pipe`: a 16-bit register between converter and adder):

| Block | Single-cycle MAC | Pipelined MAC | Standalone |
|---|---|---|---|
| Multiplier | 531.6 | 253.0 | 143.9 (`mul_int8xint8_int16`) |
| Converter | 229.6 | 109.0 | 116.2 (`cvt_int16_fp16`) |
| fp16 adder | 582.5 | 485.5 | 525.8 (`add_fp16xfp16_fp16`) |
| Glue | 164.7 | 101.1 | — |
| **Logic** | **1,508.3** | **948.5** | |
| Flops (accumulator; + pipeline register) | 36.3 | 72.6 | |

The pipeline register takes 37% off the logic. The converter and the adder come back to
their standalone size; the multiplier is still 1.8× its standalone size. The design still ends
at 0 ps slack, now on the fp16 add + accumulator loop.

## First version (5 ns clock transition, 2026-10-22)

Same method on the old `pe_summary.csv` runs, kept for the record: converter 272 of
1,763 µm² logic in `mac_mulint8_addfp16` (15%); multiplier upsized 4.1×, adder 1.36×; the
int → fp MACs' converter share 9–16%; standalone `cvt_int16_fp16` 120 µm²; pipelining took
41% off. The 0.1 ns rebuild moved designs at 0 ps slack by up to −14% (this MAC: 1,763 →
1,508 µm²) without changing any conclusion.

## Method

`mac_area_breakdown.py` reads the per-cell areas from each run's `rpt/<design>.gates.rpt`,
applies them to every instance in `gate/<design>.v`, and groups the instances in
`mac_core_*` by name: the `u_mul` hierarchy or `mul_*` cells, `u_cvt*`, `u_add*`, the
`acc_reg` flops, and everything else as glue. For every design above, the sum matches
`core_area_um2` in the summary CSV exactly, and the sum without flops matches
`logic_area_um2`. It reads `pe_summary_v2.csv` when the folder has one, else
`pe_summary.csv`, and needs the full sweep copy, which is not in git:

```bash
# from quantization_survey/hardware/
python3 mac_lut_tradeoff/02-int-to-fp-converter-cost/mac_area_breakdown.py pe_sweep_v2 \
    mac_int4xint4_fp16 mac_int8xint8_fp16 mac_int8xint8_fp32 mac_int16xint16_fp32 \
    mac_int8xint8_int16 mac_fp16xfp16_fp16 mac_int8xint8_fp16_pipe
# the first version: same script on pe_sweep, with the old names
```
