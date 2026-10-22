# Buffer sweep: N × 16-bit buffer, 1RW, 1R1W, 1RW1R and 1RW3R

Generated 2026-10-22 by `scripts/make_report.py` from `compare_summary.csv`.

A buffer of N 16-bit elements (N = 4 … 256) with 1-cycle read/write and four port
configurations, modelled two ways: a flip-flop register file synthesized with the
micro26rcf Genus flow, and a CACTI SRAM.

| Ports | Meaning |
|---|---|
| 1RW | one read/write port |
| 1R1W | one read port + one write port |
| 1RW1R | one read/write port + one read port |
| 1RW3R | one read/write port + three read ports |

## Summary

* The flip-flop buffer costs about 41 µm² per 16-bit entry (1RW, N = 256), 75% of it flip-flops. Ports are cheap there because the storage is shared: relative to 1RW, 1R1W is 1.00× the area, 1RW1R 1.19–1.33× and 1RW3R 1.57–2.00× (each extra read port adds a read mux and a read register).
* In CACTI every port widens the SRAM cell and adds wordlines and bitlines: relative to 1RW, 1R1W is 1.98–2.13× the area, 1RW1R 2.04–2.18× and 1RW3R 5.24–5.72× (N = 32 … 256).
* Against the CACTI SRAM (N = 32 … 256), the flip-flop buffer takes 9.6–13.1× the area and 5.2–8.2× the power for 1RW; 4.6–6.3× the area and 4.7–6.7× the power for 1R1W; 5.4–7.3× the area and 4.7–6.2× the power for 1RW1R; 2.8–3.8× the area and 3.7–4.8× the power for 1RW3R. The gap narrows from 1RW to 1RW1R to 1RW3R because an extra port costs an SRAM far more than a flip-flop buffer. The flip-flop power is an upper bound because of the clock-transition setting (note 2).

## Setup

* **Node and clock:** 28nm, 500 MHz, for both models.
* **Workload:** a read/write port reads on 80% and writes on 20% of cycles; a read-only
  port reads on 80% of cycles; a write-only port writes on 20% of cycles. 1RW and 1R1W
  therefore do one 16-bit access per cycle (80% reads, 20% writes). 1RW1R and 1RW3R add
  0.8 reads per cycle per read-only port, i.e. 1.6 and 3.2 reads per cycle in total.
* **Synthesized:** RTL in `src/buffer/` (`buffer_1rw`, `buffer_1r1w`, `buffer_1rw_nr` with
  NR = 1 or 3 read-only ports, each with its own read register). Each sits as `u_buf`
  inside a wrapper top that registers every input and output (as in
  `src/v2_inter_pe/v2_systolic_inter_pe_top.v`), and the numbers are for `u_buf` only:
  storage flops, read registers, address decode, read muxes and clock-gating cells. Flow,
  library and constraints are the same as `micro26rcf/scripts/run_syn.sh` (Genus 21.1, TSMC
  28nm HPC+ 9-track, TT 0.9 V 25 °C). Power is the Genus vectorless estimate with
  `syn/synth/script/activity.tcl`, which applies the workload above per port (`cs`=1 on
  the read/write port, `we` 20%, every `re` 80%, set independently; addresses and data
  random). Static = leakage, dynamic = internal + switching.
* **CACTI:** copied from `crisscross/EVA/memory`, built locally, and run with the EVA
  `sram_config.json` at 28nm (itrs-hp cells, 360 K, ECC on). Ports map to CACTI's
  `read-write port`, `exclusive read port` and `exclusive write port` counts. Dynamic
  power = 500 MHz × (0.8 E_read + 0.2 E_write + 0.8 E_read per read-only port beside a
  read/write port). The range lets the one read/write (or 1R1W) access be all reads or all
  writes, with any extra read ports kept at 80%. Static = leakage + gate leakage.

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

### 1RW1R

| N | Area (µm²) | Flops / logic / clock-gate area (µm²) | Static (mW) | Dynamic (mW) | Total (mW) | Flops / logic / clock-gate power (mW) | Slack (ps) |
|---|---|---|---|---|---|---|---|
| 4 | 264 | 194 / 60 / 11 | 0.0033 | 0.658 | 0.661 | 0.526 / 0.120 / 0.015 | 1010 |
| 8 | 451 | 314 / 118 / 19 | 0.0061 | 0.707 | 0.713 | 0.510 / 0.184 / 0.020 | 951 |
| 16 | 840 | 556 / 250 / 34 | 0.0063 | 0.825 | 0.831 | 0.540 / 0.262 / 0.029 | 849 |
| 32 | 1,624 | 1,040 / 519 / 64 | 0.011 | 1.065 | 1.076 | 0.656 / 0.372 / 0.047 | 800 |
| 64 | 3,157 | 2,008 / 1,025 / 125 | 0.029 | 1.406 | 1.435 | 0.821 / 0.530 / 0.084 | 793 |
| 128 | 6,189 | 3,943 / 2,000 / 246 | 0.052 | 1.999 | 2.051 | 1.214 / 0.680 / 0.158 | 816 |
| 256 | 12,356 | 7,814 / 4,055 / 488 | 0.092 | 4.373 | 4.466 | 2.036 / 2.124 / 0.305 | 789 |

### 1RW3R

| N | Area (µm²) | Flops / logic / clock-gate area (µm²) | Static (mW) | Dynamic (mW) | Total (mW) | Flops / logic / clock-gate power (mW) | Slack (ps) |
|---|---|---|---|---|---|---|---|
| 4 | 397 | 266 / 116 / 15 | 0.0048 | 1.224 | 1.229 | 0.974 / 0.231 / 0.024 | 1010 |
| 8 | 640 | 387 / 230 / 23 | 0.010 | 1.302 | 1.313 | 0.919 / 0.364 / 0.029 | 951 |
| 16 | 1,153 | 629 / 487 / 38 | 0.010 | 1.469 | 1.479 | 0.933 / 0.508 / 0.038 | 849 |
| 32 | 2,191 | 1,113 / 1,011 / 68 | 0.017 | 1.777 | 1.795 | 1.024 / 0.714 / 0.057 | 796 |
| 64 | 4,197 | 2,081 / 1,988 / 129 | 0.039 | 2.185 | 2.223 | 1.166 / 0.964 / 0.093 | 787 |
| 128 | 8,177 | 4,016 / 3,912 / 249 | 0.083 | 2.880 | 2.963 | 1.531 / 1.265 / 0.167 | 816 |
| 256 | 16,294 | 7,887 / 7,916 / 491 | 0.135 | 5.382 | 5.517 | 2.342 / 2.861 / 0.314 | 711 |

## CACTI SRAM

CACTI does not model arrays under 64 bytes, so there are no numbers for N < 32.

| Ports | N | Area (µm²) | Static (mW) | Dynamic (mW) | Dynamic range (mW) | Total (mW) | Read / write energy per access (pJ) |
|---|---|---|---|---|---|---|---|
| 1RW | 32 | 140 | 0.052 | 0.062 | 0.0577-0.0768 | 0.114 | 0.115 / 0.154 |
| 1RW | 64 | 242 | 0.108 | 0.073 | 0.0644-0.1062 | 0.181 | 0.129 / 0.212 |
| 1RW | 128 | 452 | 0.202 | 0.108 | 0.0906-0.1780 | 0.310 | 0.181 / 0.356 |
| 1RW | 256 | 790 | 0.332 | 0.150 | 0.1368-0.2026 | 0.482 | 0.274 / 0.405 |
| 1R1W | 32 | 289 | 0.070 | 0.072 | 0.0672-0.0932 | 0.143 | 0.134 / 0.186 |
| 1R1W | 64 | 517 | 0.129 | 0.083 | 0.0723-0.1269 | 0.212 | 0.145 / 0.254 |
| 1R1W | 128 | 895 | 0.214 | 0.124 | 0.1155-0.1561 | 0.338 | 0.231 / 0.312 |
| 1R1W | 256 | 1,655 | 0.406 | 0.178 | 0.1607-0.2455 | 0.584 | 0.321 / 0.491 |
| 1RW1R | 32 | 300 | 0.073 | 0.127 | 0.1215-0.1488 | 0.200 | 0.135 / 0.189 |
| 1RW1R | 64 | 529 | 0.131 | 0.142 | 0.1308-0.1866 | 0.273 | 0.145 / 0.257 |
| 1RW1R | 128 | 920 | 0.217 | 0.217 | 0.2090-0.2505 | 0.434 | 0.232 / 0.315 |
| 1RW1R | 256 | 1,681 | 0.409 | 0.308 | 0.2903-0.3761 | 0.716 | 0.323 / 0.494 |
| 1RW3R | 32 | 769 | 0.098 | 0.279 | 0.2717-0.3103 | 0.378 | 0.160 / 0.237 |
| 1RW3R | 64 | 1,386 | 0.177 | 0.314 | 0.2979-0.3770 | 0.491 | 0.175 / 0.333 |
| 1RW3R | 128 | 2,366 | 0.297 | 0.500 | 0.4883-0.5478 | 0.797 | 0.287 / 0.406 |
| 1RW3R | 256 | 4,320 | 0.554 | 0.723 | 0.6985-0.8204 | 1.277 | 0.411 / 0.655 |

## Cost of extra ports

Area / total power relative to 1RW at the same N.

| N | Flops 1R1W | Flops 1RW1R | Flops 1RW3R | CACTI 1R1W | CACTI 1RW1R | CACTI 1RW3R |
|---|---|---|---|---|---|---|
| 4 | 1.00× / 1.00× | 1.33× / 1.76× | 2.00× / 3.28× | — | — | — |
| 8 | 1.00× / 1.01× | 1.26× / 1.73× | 1.79× / 3.18× | — | — | — |
| 16 | 1.00× / 1.00× | 1.23× / 1.64× | 1.69× / 2.92× | — | — | — |
| 32 | 1.00× / 1.01× | 1.21× / 1.50× | 1.64× / 2.50× | 2.07× / 1.26× | 2.15× / 1.76× | 5.50× / 3.33× |
| 64 | 1.00× / 1.00× | 1.20× / 1.41× | 1.60× / 2.18× | 2.13× / 1.17× | 2.18× / 1.51× | 5.72× / 2.72× |
| 128 | 1.00× / 1.00× | 1.19× / 1.28× | 1.57× / 1.85× | 1.98× / 1.09× | 2.04× / 1.40× | 5.24× / 2.57× |
| 256 | 1.00× / 1.00× | 1.19× / 1.13× | 1.57× / 1.40× | 2.09× / 1.21× | 2.13× / 1.49× | 5.47× / 2.65× |

## Synthesized ÷ CACTI

| N | 1RW area | 1RW power | 1R1W area | 1R1W power | 1RW1R area | 1RW1R power | 1RW3R area | 1RW3R power |
|---|---|---|---|---|---|---|---|---|
| 32 | 9.6× | 6.3× | 4.6× | 5.1× | 5.4× | 5.4× | 2.8× | 4.8× |
| 64 | 10.9× | 5.6× | 5.1× | 4.8× | 6.0× | 5.3× | 3.0× | 4.5× |
| 128 | 11.5× | 5.2× | 5.8× | 4.7× | 6.7× | 4.7× | 3.5× | 3.7× |
| 256 | 13.1× | 8.2× | 6.3× | 6.7× | 7.3× | 6.2× | 3.8× | 4.3× |

## Notes

1. **Ports in flip-flop vs SRAM buffers:** in the flip-flop buffer the storage is shared,
   so a port costs only its own decode/mux logic and read register. 1R1W equals 1RW, and
   each extra read port adds a read mux. In an SRAM every port adds wordlines, bitlines
   and transistors to every cell, so area grows much faster with port count (see *Cost of
   extra ports*).
2. **Clock transition in the flow constraints:** `my.constraints.tcl` sets
   `set_clock_transition 5` (5 ns on a 2 ns clock). Flip-flop internal power depends on
   clock slew, and this buffer is mostly flip-flops. In a one-off run of `buffer_n4` with
   0.05 ns, `u_buf` power fell from 0.375 to 0.153 mW: flip-flop internal power dropped
   about 4× and logic power did not change. The synthesized power above is therefore an
   upper bound: about 2.5× too high for 1RW at N = 4, the only point measured. Area is
   unaffected.
3. **Wrapper effect:** without the wrapper, inputs came straight from ports, which Genus
   treats as ideal drivers (0 ps transition). Registered inputs give real transitions, so
   `u_buf` power is higher than in earlier unwrapped runs. `u_buf` area is unchanged.
4. **Logic power from N = 128 to N = 256:** 1RW 0.397 → 1.756 mW (4.4×, logic area 2.0×); 1R1W 0.396 → 1.749 mW (4.4×, logic area 2.0×); 1RW1R 0.680 → 2.124 mW (3.1×, logic area 2.0×); 1RW3R 1.265 → 2.861 mW (2.3×, logic area 2.0×). For 1RW the same step appeared in
   every run (with or without the wrapper, default or 80/20 activity). It comes from how
   Genus builds the 256-entry read path, not from the measurement setup, so treat the
   N = 256 logic power with care.
5. **The multi-read workload is busy:** 1RW1R and 1RW3R power assumes every read port
   reads on 80% of cycles. For a lighter workload, scale the read-port share of the CACTI
   dynamic power using the per-access energies in the CACTI table. The synthesized power
   would need a rerun with different `re` activity in `activity.tcl`.
6. **Static power differs a lot between the models.** The CACTI config uses high-performance
   cells at 360 K with ECC; Genus uses typical-corner standard cells at 25 °C.
7. **Checks:** 28/28 designs pass their RTL tests (Python golden memory
   model → VCS → check; every entry written first, then random reads/writes on all ports,
   including reads of an address being written in the same cycle). Synthesis runs with
   unresolved references or errors: none.

## Reproduce (from `playground/buffer_sweep`)

```bash
python cacti_exp/run_buffer_sweep.py   # CACTI -> cacti_exp/buffer_cacti_summary.csv
python scripts/gen_rtl.py              # wrapper tops, testbenches, designs.json
scripts/run_test.sh                    # RTL tests
scripts/run_syn.sh                     # synthesis, one design after another (run inside tmux)
python scripts/collect.py              # -> compare_summary.csv
python scripts/make_report.py          # -> REPORT.md
```
