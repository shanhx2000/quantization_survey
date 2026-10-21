# Buffer sweep: N × 16-bit buffer, 1RW and 1R1W

Generated 2026-10-15 by `scripts/make_report.py` from `compare_summary.csv`.

A buffer of N 16-bit elements (N = 4 … 256) with 1-cycle read/write, modelled two ways:
a flip-flop register file synthesized with the micro26rcf Genus flow, and a CACTI SRAM.

## Summary

* The flip-flop buffer costs about 41 µm² per 16-bit entry (u_buf, N = 256), about 75% of it flip-flops. 1R1W costs the same area as 1RW.
* Against the CACTI SRAM (N = 32 … 256), the flip-flop buffer takes 9.6–13.1× the area and 5.2–8.2× the power of a 1RW SRAM, and 4.6–6.3× the area and 4.7–6.7× the power of a 1R1W SRAM. Its power is an upper bound because of the clock-transition setting (note 2).
* In CACTI, a second port (1R1W) roughly doubles the area (1.98–2.13×); total power rises by 1.09–1.26×.

## Setup

* **Node and clock:** 28nm, 500 MHz, for both models.
* **Workload:** one 16-bit access per cycle, 80% reads and 20% writes.
* **Synthesized:** RTL in `src/buffer/` (`buffer_1rw`, `buffer_1r1w`). Each sits as `u_buf`
  inside a wrapper top that registers every input and output (as in
  `src/v2_inter_pe/v2_systolic_inter_pe_top.v`), and the numbers are for `u_buf` only:
  storage flops, read register, address decode, read mux and clock-gating cells. Flow,
  library and constraints are the same as `micro26rcf/scripts/run_syn.sh` (Genus 21.1, TSMC
  28nm HPC+ 9-track, TT 0.9 V 25 °C). Power is the Genus vectorless estimate with
  `syn/synth/script/activity.tcl`: 1RW `cs`=1 and `we` high 20% of cycles; 1R1W `re` 80%
  and `we` 20%, set independently, so about 16% of cycles both read and write. Addresses
  and data are random. Static = leakage, dynamic = internal + switching.
* **CACTI:** copied from `crisscross/EVA/memory`, built locally, and run with the EVA
  `sram_config.json` at 28nm (itrs-hp cells, 360 K, ECC on). 1RW = one read/write port;
  1R1W = one exclusive read port + one exclusive write port. Dynamic power =
  500 MHz × (0.8 E_read + 0.2 E_write); the range runs from all reads to all writes.
  Static = leakage + gate leakage.

## Synthesized buffer (`u_buf`)

### 1RW

| N | Area (µm²) | Flops / logic / clock-gate area (µm²) | Static (mW) | Dynamic (mW) | Total (mW) | Flops / logic / clock-gate power (mW) | Slack (ps) |
|---|---|---|---|---|---|---|---|
| 4 | 198 | 157 / 32 / 9 | 0.0020 | 0.373 | 0.375 | 0.302 / 0.063 / 0.010 | 1010 |
| 8 | 357 | 278 / 62 / 17 | 0.0039 | 0.409 | 0.413 | 0.305 / 0.093 / 0.015 | 951 |
| 16 | 683 | 520 / 130 / 32 | 0.0049 | 0.502 | 0.507 | 0.343 / 0.139 / 0.024 | 849 |
| 32 | 1,340 | 1,004 / 273 / 62 | 0.0088 | 0.708 | 0.717 | 0.473 / 0.201 / 0.043 | 812 |
| 64 | 2,631 | 1,972 / 536 / 123 | 0.020 | 0.999 | 1.020 | 0.648 / 0.292 / 0.080 | 780 |
| 128 | 5,193 | 3,907 / 1,043 / 244 | 0.044 | 1.561 | 1.605 | 1.055 / 0.397 / 0.153 | 816 |
| 256 | 10,386 | 7,778 / 2,123 / 486 | 0.072 | 3.867 | 3.939 | 1.883 / 1.756 / 0.300 | 789 |

### 1R1W

| N | Area (µm²) | Flops / logic / clock-gate area (µm²) | Static (mW) | Dynamic (mW) | Total (mW) | Flops / logic / clock-gate power (mW) | Slack (ps) |
|---|---|---|---|---|---|---|---|
| 4 | 198 | 157 / 31 / 9 | 0.0020 | 0.375 | 0.377 | 0.307 / 0.060 / 0.010 | 1030 |
| 8 | 358 | 278 / 63 / 17 | 0.0036 | 0.414 | 0.418 | 0.306 / 0.097 / 0.015 | 990 |
| 16 | 685 | 520 / 132 / 32 | 0.0050 | 0.499 | 0.504 | 0.343 / 0.137 / 0.024 | 972 |
| 32 | 1,344 | 1,004 / 278 / 62 | 0.0095 | 0.714 | 0.724 | 0.473 / 0.208 / 0.043 | 845 |
| 64 | 2,629 | 1,972 / 534 / 123 | 0.019 | 0.997 | 1.016 | 0.648 / 0.288 / 0.080 | 774 |
| 128 | 5,192 | 3,907 / 1,042 / 244 | 0.044 | 1.559 | 1.604 | 1.055 / 0.396 / 0.153 | 855 |
| 256 | 10,384 | 7,778 / 2,120 / 486 | 0.072 | 3.861 | 3.933 | 1.883 / 1.749 / 0.300 | 656 |

## CACTI SRAM

CACTI does not model arrays under 64 bytes, so there are no numbers for N < 32.

| N | 1RW area (µm²) | 1RW static / dynamic (mW) | 1RW dynamic range (mW) | 1RW total (mW) | 1R1W area (µm²) | 1R1W static / dynamic (mW) | 1R1W dynamic range (mW) | 1R1W total (mW) |
|---|---|---|---|---|---|---|---|---|
| 32 | 140 | 0.052 / 0.062 | 0.0577-0.0768 | 0.114 | 289 | 0.070 / 0.072 | 0.0672-0.0932 | 0.143 |
| 64 | 242 | 0.108 / 0.073 | 0.0644-0.1062 | 0.181 | 517 | 0.129 / 0.083 | 0.0723-0.1269 | 0.212 |
| 128 | 452 | 0.202 / 0.108 | 0.0906-0.1780 | 0.310 | 895 | 0.214 / 0.124 | 0.1155-0.1561 | 0.338 |
| 256 | 790 | 0.332 / 0.150 | 0.1368-0.2026 | 0.482 | 1,655 | 0.406 / 0.178 | 0.1607-0.2455 | 0.584 |

## Synthesized ÷ CACTI

| N | 1RW area ratio | 1RW power ratio | 1R1W area ratio | 1R1W power ratio |
|---|---|---|---|---|
| 32 | 9.6× | 6.3× | 4.6× | 5.1× |
| 64 | 10.9× | 5.6× | 5.1× | 4.8× |
| 128 | 11.5× | 5.2× | 5.8× | 4.7× |
| 256 | 13.1× | 8.2× | 6.3× | 6.7× |

## Notes

1. **Port count:** with flip-flops, 1R1W costs the same area as 1RW
   (0.997–1.003×), because the storage flops
   dominate and both need one write decoder and one read mux. In CACTI, 1R1W costs
   1.98–2.13× the 1RW area.
2. **Clock transition in the flow constraints:** `my.constraints.tcl` sets
   `set_clock_transition 5` (5 ns on a 2 ns clock). Flip-flop internal power depends on
   clock slew, and this buffer is mostly flip-flops. In a one-off run of `buffer_n4` with
   0.05 ns, `u_buf` power fell from 0.375 to 0.153 mW: flip-flop internal power dropped
   about 4× and logic power did not change. The synthesized power above is therefore an
   upper bound: about 2.5× too high at N = 4, the only size measured. Area is unaffected.
3. **Wrapper effect:** without the wrapper, inputs came straight from ports, which Genus
   treats as ideal drivers (0 ps transition). Registered inputs give real transitions, so
   `u_buf` power is higher than in earlier unwrapped runs. `u_buf` area is unchanged.
4. **Logic power at N = 256:** 1RW logic power goes from 0.397 to 1.756 mW (4.4×) while logic area grows 2.0×; 1R1W logic power goes from 0.396 to 1.749 mW (4.4×) while logic area grows 2.0×. The same step appeared in every run (with or
   without the wrapper, default or 80/20 activity). It
   comes from how Genus builds the 256-entry read path, not from the measurement setup,
   so treat that point with care.
5. **Static power differs a lot between the models.** The CACTI config uses high-performance
   cells at 360 K with ECC; Genus uses typical-corner standard cells at 25 °C.
6. **Checks:** 14/14 designs pass their RTL tests (Python golden memory
   model → VCS → check; every entry written first, then random reads/writes, including
   same-address read+write on 1R1W). Synthesis runs with unresolved references or errors:
   none.

## Reproduce (from `playground/buffer_sweep`)

```bash
python cacti_exp/run_buffer_sweep.py   # CACTI -> cacti_exp/buffer_cacti_summary.csv
python scripts/gen_rtl.py              # wrapper tops, testbenches, designs.json
scripts/run_test.sh                    # RTL tests
scripts/run_syn.sh                     # synthesis, one design after another (run inside tmux)
python scripts/collect.py              # -> compare_summary.csv
python scripts/make_report.py          # -> REPORT.md
```
