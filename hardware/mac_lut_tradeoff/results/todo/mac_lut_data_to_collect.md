# Data to collect for the MAC vs LUT GEMM cost tables

Written 2026-10-22 and updated the same day with the owner's decisions. Every item fills `#`
cells in the cost tables at
`~/moe_ws/quantization_survey/hardware/mac_lut_tradeoff/01-gemm-cost-per-frame/` (on the
quantization_survey host). Its README.md has the cost model and, under *Missing data*, the
exact (N, W, R) list still missing; this file says how to get them. The tables are built from
a 2026-10-21 copy of `playground/pe_sweep` and `playground/buffer_sweep`.

## Owner decisions (2026-10-22)

* Batch sizes bs ∈ {1, 2, 4, 8}.
* int × fp16 multipliers output **fp16**.
* SRAM tables under CACTI's 64-byte floor: **no new run**. They take the numbers of the
  smallest table at or above 64 bytes with the same width, marked `*` as an upper bound.
* Ternary register-file tables: **only v ≤ 6** (at most 1,024 entries). SRAM at every v.
* wa = int8 LUT entries: **8 + ⌈log2 v⌉ bits** per batch row, enough for the exact sum of v
  int8 activations: 10 bits at v = 4, 11 bits at v = 6, 7, 8.

## What the tables need

* Frames: wq ∈ {int1, ter (ternary), int2, int3, int4, int6, int8} × wa ∈ {int8, fp16};
  vector length v ∈ {4, 6, 7, 8}; bs ∈ {1, 2, 4, 8}.
* MAC-GEMM: fp16 mul, fp16 add, int8 mul, int16 add (all exist), and **int-wq × wa
  multipliers** for wq = int2 … int8 (missing except int8 × int8). int1 and ter need no
  multiplier.
* LUT entries N: int-b weights, 2^v or 2^v / 2 → N = 8 … 256. Ternary weights, the smallest
  2^k ≥ 3^v (or ≥ ⌊3^v / 2⌋) → N = 64 … 8192, register file only up to 1,024.
* Entry width W = bs × 16 bits (wa = fp16) or bs × (8 + ⌈log2 v⌉) bits (wa = int8):
  * register file, exact width: **W ∈ {10, 11, 16, 20, 22, 32, 40, 44, 64, 80, 88, 128}**;
  * CACTI, rounded up to whole bytes: **{2, 3, 4, 5, 6, 8, 10, 11, 16} bytes per entry**.
* Two organizations: b copies with one read port each, or one table with **R = b ∈
  {2, 3, 4, 6, 8} read ports** (int1 and ter read once).
* **LUT power must be read-only**: the table is written once (precompute, ignored) and then
  only read. Every buffer_sweep number so far is at 80% read / 20% write.

Today only W = 16 with one read port exists: register file N = 4 … 256 (its area is used;
its power is not, being 80/20), CACTI N = 32 … 256.

## Priority 1 — fills the bs = 1 tables

1. **Read-only power of the existing 16-bit register files** (`buffer_n<N>`, 1RW).
   In `syn/synth/script/activity.tcl`, hold `we` at 0 (`we {0.0 0.0}`; `cs` is already 1, so
   every cycle is a read) and rerun N = 8 … 256. Area does not change.
   While at it, run them once more with a realistic clock transition (e.g.
   `set_clock_transition 0.05` instead of 5 ns in `my.constraints.tcl`): a buffer is mostly
   flip-flops, and on `buffer_n4` that setting alone cut `u_buf` power 0.375 → 0.153 mW.
   Report both, so the tables can say which one they use.
2. **10- and 11-bit register files, 1RW, read-only power** (wa = int8, bs = 1):
   W = 10: N = 8, 16, 64, 128; W = 11: N = 32, 64, 128, 256, 512, 1024 (10 designs).
   `scripts/gen_rtl.py` hard-codes `.WIDTH(16)`; make the width a parameter and name the
   designs `buffer_n<N>_w<W>`.
3. **Ternary 16-bit register files**, N = 512 and 1024 (wa = fp16, v = 6). By the
   41 µm²-per-entry slope of `buffer_n256`, 1,024 entries is about 42,000 µm².
4. **CACTI, 2-byte entries, N = 512 … 8192**, one read port (the ternary tables at bs = 1, for
   both wa: 10- and 11-bit entries round up to 2 bytes). Keep the read energy:
   read-only power = leakage + gate leakage + 500 MHz × E_read. Nothing else is needed from
   CACTI for bs = 1, because the existing 16-bit sweep already covers N = 32 … 256.
5. **Mixed multipliers in pe_sweep**, named exactly like this so `make_tables.py` picks them
   up:
   * `mul_int2xint8`, `mul_int3xint8`, `mul_int4xint8`, `mul_int6xint8`: signed int-wq ×
     signed int8, full (wq + 8)-bit product, like `mul_int8`.
   * `mul_int2xfp16`, `mul_int3xfp16`, `mul_int4xfp16`, `mul_int6xfp16`, `mul_int8xfp16`:
     **fp16 output** (decided), round-to-nearest-even, `ieee_compliance=0` like the other fp
     units. Quickest build: int → fp16 (`CW_fp_i2flt`, exact for these widths) followed by
     `CW_fp_mult`; this is an upper bound. A direct 11-bit-significand × wq-bit-int multiplier
     with one normalize/round would be tighter.

## Priority 2 — multi-port tables and wider entries (bs > 1)

6. **Multi-read-port register file**: one write port + R read ports, R ∈ {2, 3, 4, 6, 8}, new
   RTL (e.g. `buffer_1wNr`), read-only power with all R ports reading every cycle. Only int-b
   weights read more than once, so N ≤ 256. Start with the bs = 1 widths: W = 10: N = 8, 16;
   W = 11: N = 32 … 256; W = 16: N = 8 … 256 → 12 tables × 5 port counts = 60 designs.
   Then the wider widths of item 7.
7. **Wider register files, 1RW**: W ∈ {20, 22, 32, 40, 44, 64, 80, 88, 128}, the N listed per
   W in the README's *Missing data* table (54 designs; ternary sizes stop at 1,024). After a
   few widths, check whether area is linear in W; if it is, whether to run the rest is the
   owner's call.
8. **CACTI, wider and multi-port**: entries of {3, 4, 5, 6, 8, 10, 11, 16} bytes × N = 8 … 8192
   with one read port, and every entry size × N = 8 … 256 with `exclusive read port` = R ∈
   {2, 3, 4, 6, 8} plus one write port. CACTI is cheap, so run the whole grid; sanity-check
   that R ports cost less than R single-port copies. Tables under 64 bytes are skipped (they
   use the decision above).

## Priority 3 — separate the effects

9. **Standalone int → fp16 converter**: registered `CW_fp_i2flt`, isize ∈ {10, 11, 12, 14, 16}
   (the int-wq × int8 products for wq = 2, 3, 4, 6, 8) → fp16, named `cvt_int<isize>_fp16`.
   Inside `mac_mulint8_addfp16` the converter cells are only 272 µm² of 1,763 µm²; the rest of
   the gap to `mul_int8` + `add_fp16` is upsizing to close timing in one cycle (analysis in
   `mac_lut_tradeoff/02-int-to-fp-converter-cost/`). For isize ≤ 12 the conversion is exact,
   so an RTL leading-zero-count + shift without rounding is also worth one run.
10. **Pipelined MAC**: `mac_mulint8_addfp16` with a register after the converter, to measure
    how much of the 4.1× multiplier growth inside the MAC goes away.
11. *Optional:* `add_fp16` and `mul_fp16` at a relaxed clock (e.g. 4 ns). They close at
    0–1 ps slack, so their 2 ns area includes upsizing, and every MAC and LUT row uses them.
12. *Optional:* the LUT precompute cost, which the tables ignore by spec ("pre-ignore"): a
    builder that fills the table from v activations.

## Handing the results back

Add `W` (bits) and `R` columns and a read-only power column (`syn_ro_total_mW`,
`cacti_ro_total_mW`) to `compare_summary.csv`, or write a new CSV with those columns. Copy it
into `quantization_survey/hardware/mac_lut_tradeoff/results/`. `make_tables.py` currently
assumes W = 16 and R = 1 for every buffer row, so it needs a small update to read them.
