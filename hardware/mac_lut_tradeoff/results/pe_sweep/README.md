# PE sweep: add / mul / MAC / counter area and power (TSMC 28nm HPC+, 500 MHz)

Synthesis follows `micro26rcf/scripts/run_syn.sh` (same Genus script, libraries,
constraints, 2 ns clock), copied here so nothing outside `playground/` is touched.

## Commands (run from this folder)

```bash
python scripts/gen_rtl.py      # src/pe/pe_gen.v, tb/, designs.txt, designs.json
scripts/run_test.sh [design ...]  # RTL tests: golden generate -> VCS -> golden check
scripts/run_syn.sh  [design ...]  # Genus, one design after another (use tmux)
python scripts/collect.py      # -> pe_summary.csv
python scripts/make_report.py  # -> REPORT.md
```

With no arguments both scripts run every design in `designs.txt`.

## Designs

Each design is a wrapper top that registers every input and output (as in
`src/v2_inter_pe/v2_systolic_inter_pe_top.v`) around the measured module `u_core`.
Results are for `u_core`, split into logic (combinational cells), flip-flops and
clock-gating cells. See `REPORT.md`.

| design | core |
|---|---|
| `add_<t>`, `mul_<t>` | t in int4, int8, fp8, int16, fp16, fp32. int add: W-bit wrap; int mul: full 2W-bit product; fp results rounded to t |
| `mac_mul<x>_add<y>` | `acc <= acc + conv_y(mul_x(a, b))`, y in int16, fp16, fp32 (conversion per design in `designs.txt`) |
| `add_fp16_rtl` | the RTL fp adder used for fp8, built at fp16 to compare with `CW_fp_add` |
| `cnt_up_w<W>`, `cnt_updn_w<W>` | +1 / +-1 counter with enable (and direction), W in 4, 6, 8, 10, wraps |
| `mul_int<q>xint8` | q in 2, 3, 4, 6: signed int-q x int8, full (q+8)-bit product |
| `mul_int<q>xfp16` | q in 2, 3, 4, 6, 8: int-q -> fp16 (`CW_fp_i2flt`, exact) then `CW_fp_mult`, fp16 result |
| `cvt_int<k>_fp16` | k in 10, 11, 12, 14, 16: `CW_fp_i2flt` to fp16 (RNE); `_rtl` (k <= 12): exact leading-one + shift |
| `mac_mulint8_addfp16_pipe` | `mac_mulint8_addfp16` with a register between the converted product and the adder |

Run variants (environment of `scripts/run_syn.sh`, appended to the run folder name):
`SYN_PERIOD=<ns>`, `SYN_ACT=<activity profile>`, `SYN_CLK_TRAN=<ns>`. `collect.py` reports the
default variant under the design name and others as `<design>@<variant>` rows.

* FP blocks are Genus ChipWare (`CW_fp_add`, `CW_fp_mult`, `CW_fp_i2flt`, `CW_fp_flt2i`) with
  `ieee_compliance=0` (denormals read as zero, no NaN handling) and round-to-nearest-even.
* fp8 is E4M3 with IEEE-style encoding (exp all-ones = Inf/NaN, max 240). Genus 21.1 has
  no `CW_fp8_add` (its documentation lists one, but elaboration black-boxes it), and
  `CW_fp_add` needs exp/mantissa >= 5 bits, so fp8 addition uses `fp_add_ftz` in
  `src/pe/pe_lib.v`. That adder follows the same rules and is tested exhaustively.
* Converters: `fp_up` (exact widening) and `fp_down` (RNE narrowing) are in `pe_lib.v`.
  fp8 -> int16 goes through fp16 because `CW_fp_flt2i` needs exp/mantissa >= 5 bits.
* Power is Genus vectorless power with `syn/synth/script/activity.tcl`. Data inputs are
  random (P=0.5, 0.5 toggles/cycle). Counters count on 100% of cycles (`en`=1), and the
  up/down counter changes direction about every 50 cycles.

## Tests

`golden/gen_golden.py` writes per-cycle stimulus and checks the VCS output with a
cycle model built on bit-accurate FP references (`golden/fpmodel.py`, exact rational
arithmetic). Coverage: 4- and 8-bit add/mul use every input pair; wider add/mul use 5000
random vectors; MACs run 4000 cycles with random resets; counters run 6000 cycles.
The ChipWare simulation models come from Genus (`share/synth/lib/chipware/sim`).
`-error=noNMCM` lets VCS accept a negative replication count in the `CW_fp_i2flt` model
(in a branch that isn't taken).

## Notes on the flow

* Do not run two syntheses from the same `syn/synth` at once. `run_pe.csh` rewrites
  `config_temp.tcl` there, and a second run can change it before the first Genus reads it.
* `run_syn.sh` feeds Genus `/dev/null` as input. The Genus script does not end with
  `exit`, so in a terminal (e.g. tmux) it would stop at the `legacy_genus:/>` prompt.
* `hdl_error_on_blackbox` is false in the flow, so a missing module is not an error.
  `collect.py` flags any run with unresolved references or errors in `syn_flags`.
