# Status: MAC vs LUT data collection

Tracks `mac_lut_data_to_collect.md`. Started 2026-10-22. The missing (N, W, R) list was
rebuilt from that file's rules, because the cost-table repo is not on this machine. The
rules reproduce its explicit lists: item 2 (10 designs), item 3 (N = 512, 1024) and
item 7 (54 designs).

## Assumption revisions (2026-10-23)

The owner reviewed the modeling assumptions behind the results (details and the
with/without-activity comparison: `activity_assumptions.md`). Several had been my (Claude's)
choices and had never been confirmed.

**Old results are kept unchanged**; another agent uses them as examples for now:
* `buffer_sweep/compare_summary.csv`, `buffer_sweep/lut_buffer_costs.csv`,
  `pe_sweep/pe_summary.csv`, both `REPORT.md` files, and every existing run folder;
* don't rerun their collectors (`collect.py`, `collect_lut.py`, `pe_sweep/scripts/collect.py`):
  they take the newest run of each variant, so later runs could change rows.

Revised results go to new files.

| # | Assumption | Before (old results) | Revised |
|---|---|---|---|
| 1 | Register-file workload | One activity profile per run: 80/20 (`we` P = 0.2, independent each cycle) or read-only (`ro`) | **Three corners per design**: read-only (`roq`), write-only (`wo`), idle. Interpolate P(r, w) = P_idle + r·(P_ro − P_idle) + w·(P_wo − P_idle) (owner) |
| 2 | Data / address activity | Random, 0.5 toggles/cycle (my choice) | Same, **confirmed** by the owner |
| 3 | Write data in read-only use | Toggled every cycle (`ro`; a bug, see below) | Held (`roq`) |
| 4 | MAC product | FP product rounded to the input format before accumulation; `int16 × int16 → int16` kept the low 16 product bits | **Product kept at full precision** (owner). MACs whose integer accumulator can't hold the exact product are **dropped**: `int16 × int16 → int16`, fp → int16 |
| 5 | Design names | `mul_int8`, `mac_mulint8_addfp16`, … | `op_{a}x{b}_{out}`, e.g. `mul_int8xint8_int16`, `mac_int8xint8_fp16` (owner). A `legacy_name` column keeps the old names, which `make_tables.py` reads |
| 6 | fp8 format | IEEE-style E4M3 (max 240, subnormals flushed) | Unchanged, **confirmed** |

Still open: the CACTI configuration (EVA's 360 K / ECC on, or 25 °C / ECC off); the structure
of int × int → fp MACs; FP-accumulator combos whose product range can overflow the
accumulator; whether to delete the 4 ns rows (kept so far).

### Revised register-file power (in progress)

* **Corners** (`buffer_sweep/syn/synth/script/activity.tcl`):
  * `roq`: every read port reads every cycle; write data and address held.
  * `wo`: the write port writes every cycle (random address and data); read ports idle.
  * `idle`: no access; addresses and data held.
* **Assumption from the corners:** the read-only corner has all read ports active together,
  so for multi-port files the model gives every read port the same read rate r.
* **Power-only re-analysis** (`script/repower.tcl`): reads an existing netlist, applies each
  corner and reports with the flow's commands. Activity doesn't change the netlist; area and
  slack were identical in every with/without pair. On 4 netlists (N = 16, 128, 256) it
  reproduces the synthesis-session `u_buf` power to 4 decimals (top level within 0.2%), so
  nothing is re-synthesized.
* **Interpolation check:** against a direct 80/20 run (write data changing only on writes),
  the interpolation is 3.4–3.8% low on `buffer_n16`, `buffer_n128` and `buffer1r1w_n128`.
  The gap is the cost of switching between reads and writes.

  | Design | P_idle | P_ro | P_wo | Interpolated 80/20 | Direct 80/20 | Old `rw` |
  |---|---|---|---|---|---|---|
  | `buffer_n16` | 0.021 | 0.201 | 0.301 | 0.221 | 0.229 | 0.286 |
  | `buffer_n128` | 0.170 | 0.559 | 1.177 | 0.682 | 0.709 | 1.169 |
  | `buffer1r1w_n128` | 0.170 | 0.487 | 0.894 | 0.568 | 0.591 | 1.167 |

  Power in mW for `u_buf`. The old `rw` numbers are 25–100% higher than the direct run,
  because their write data changed every cycle.
* **Queue `rf_corners`** (`rf_corners.sh`, log `logs/rf_corners.log`, started 10-23 12:09):
  1. synthesize at 0.1 ns the 21 designs of the 80/20 sweep that only had 5 ns netlists;
  2. re-analyze all 126 register files with a 0.1 ns netlist under the three corners.

  Reports go under `<run>/rpt/power_corners/<corner>/`. The remaining item 7 widths have no
  netlist (not synthesized).
* **Result file:** `buffer_sweep/rf_corner_costs.csv` (`python buffer_sweep/scripts/collect_corners.py`).
  It has area, corner powers (total, static, flip-flop / logic / clock-gate), `E_read_pJ_per_port`,
  `E_write_pJ` and `P_r0.8_w0.2_mW`.
* **Bug fixed in `activity.tcl`:** `array set ACT_OVERRIDE` never cleared earlier entries, so
  profiles leaked into each other when one Genus session sourced the file several times. Only
  the first re-analysis attempt was affected (since rerun). Synthesis runs source the file once
  per Genus process and are unaffected.

## Queues (finished)

One sequential Genus queue (no two runs at once), in three chained tmux sessions, all done:

| Session | Script | Contents | Finished |
|---|---|---|---|
| `lut_a` | `lut_queue_a.sh` | item 1: `buffer_n8 … buffer_n256` read-only, at 5 ns and at 0.05 ns clock transition; items 2–3: 10/11-bit register files and 16-bit N = 512, 1024 (read-only) | 10-22 15:46 |
| `lut_b` | `lut_queue_b.sh` | items 5, 9, 10 (pe_sweep), item 11 (`add_fp16`, `mul_fp16` at 4 ns), item 6 (60 1W\<R\>R register files, `lut_multiport.list`), item 7 first widths W = 20, 22, 32, 64 (26 designs, `lut_wide_first.list`) | 10-22 23:49 |
| `lut_c` | `lut_queue_c.sh` | 0.1 ns reruns of everything that only had a 5 ns run (35 register files, 18 pe designs) | 10-23 03:50 |

Logs: `logs/lut_queue_{a,b,c}.log`. Every new design passed its RTL test (VCS against a
Python golden model) before it was queued. Result: 104 register-file designs, all with a
0.1 ns run, no errors or black boxes, all PASS, min slack 501 ps.

**Read-only workload:** activity profile `ro` (`we` held at 0, every `re` and `cs` at 1). The
variant is appended to the run folder name (`…_Periodclk2_ro`, `…_ro_ct0.05`, `…_Periodclk4`),
so the earlier 80/20 runs and `compare_summary.csv` are untouched.

**Clock transition changed to 0.1 ns (2026-10-22, 16:40).** The owner set
`set_clock_transition 0.1 [get_clocks clk]` in the flow (logged in
`micro26rcf/syn/synth/CHANGELOG.md`; it was 5 ns). The playground copies default to 0.1 ns
too, and their run folders now end in `_ct0.1`. Everything queued after 16:40 runs at 0.1 ns;
item 6 switched after its first 17 designs. Session `lut_c` (`lut_queue_c.sh`, after
`lut_b`) reruns at 0.1 ns every LUT design that only has a 5 ns run: items 1–3, those 17
item-6 designs, and the 18 pe designs of items 5, 9 and 10. The collectors take the 0.1 ns
run when one exists (`primary` / `clk_transition_ns` columns), so the tables can use one
setting throughout. The 5 ns and 0.05 ns rows stay in `lut_buffer_costs.csv` for
comparison.

## Done

* **Item 4 and item 8 (CACTI), whole grid:** `buffer_sweep/cacti_exp/lut_cacti_grid.csv`.
  Entry sizes 2–16 bytes, N = 8–8192 single-port; R = 2, 3, 4, 6, 8 read ports + 1 write port
  for N ≤ 256. Read-only power = leakage + gate leakage + R × 500 MHz × E_read.
* **CACTI fails at N = 8 and N = 16 for every entry size**, not only under 64 bytes ("no
  valid data array organizations found"). The rule for tables under 64 bytes (take the
  smallest modelled table of the same width, marked `*`) therefore has to cover N = 8, 16
  too; in practice the substitute is N = 32.
* **Sanity check "R ports cost less than R copies" fails in CACTI:** an R-read-port table is
  1.70–3.56× the area of R single-port tables in all 180 cases. Read-only power is
  0.82–2.20× (a little lower for small R, because leakage is shared). In CACTI's model a
  multi-port cell grows much faster than linearly with port count, so for a read-only LUT,
  copies are cheaper in area.

## Priority 1 and the pe items (finished 2026-10-22 16:10)

All runs pass their RTL tests, with no unresolved references or errors; every design meets
500 MHz.

* **Items 1–3 (register files, read-only):** 24 rows in `lut_buffer_costs.csv`. The
  16-bit N = 1024 file is 41,460 µm² (the todo estimated about 42,000). A 0.05 ns clock
  transition gives 0.49–0.83× the 5 ns power; area moves by under 1% (timing-driven sizing).
* **Item 5:** `mul_int2xfp16` is only 38 µm². Every int2 value converts to fp16 with an
  all-zero mantissa, so Genus removes the significand multiplier; only sign and exponent logic
  remain. From int3 up there is a real multiplier (173–424 µm²). Int × int8: 34–104 µm².
* **Item 9:** `CW_fp_i2flt` → fp16 takes 70–120 µm² logic for isize 10–16. The exact RTL
  converter (isize ≤ 12) is 53–73 µm², 11–25% smaller.
* **Item 10:** the pipelined `mac_mulint8_addfp16` has 1,046 µm² logic vs 1,763 µm²
  unpipelined (−41%), plus a 16-bit pipeline register. It still closes at 0 ps: the fp16
  add + accumulator loop is the critical path.
* **Item 11:** at 4 ns, `add_fp16` logic is 345 µm² (515 at 2 ns, −33%) and `mul_fp16` is
  346 µm² (384 at 2 ns, −10%). `add_fp16` still ends at ~0 ps slack, because area recovery
  under `set_max_area 0` uses up the extra slack.

## Results land in

* `buffer_sweep/lut_buffer_costs.csv` (`python buffer_sweep/scripts/collect_lut.py`): columns
  `model` (regfile / sram), `org`, `N`, `W`, `R`, area, `syn_ro_*_mW` (per variant, with
  `clk_transition_ns`) and `cacti_ro_*_mW`.
* `pe_sweep/pe_summary.csv` (`python pe_sweep/scripts/collect.py`): the new designs under
  the names `make_tables.py` expects; the 4 ns runs as `add_fp16@Periodclk4` and
  `mul_fp16@Periodclk4`.
* Copy both into `quantization_survey/hardware/mac_lut_tradeoff/results/` (that host is
  not reachable from here).

## Read-only power: `ro` profile overstates it (found 2026-10-23)

**Don't use the `ro` power columns for read-only LUT tables. Area is unaffected.**

* The `ro` profile sets `we` = 0, but leaves `wdata` (and `waddr` in 1W\<R\>R files) toggling
  at random every cycle. In a read-only LUT the write port is idle.
* Random data at every flip-flop's D pin costs internal power even with the clock gated
  off. Genus charges a net's switching power to its driver, and the input nets fan out to
  all N entries:
  * up to N = 128 they are driven by the wrapper's input flip-flops, outside `u_buf`;
  * from N = 256 Genus buffers them inside `u_buf`.
  So `u_buf` logic power jumps 4.6× from N = 128 to 256 while area doubles, in every port
  type (+1.1–1.4 mW for 16-bit files).
* New profile `roq` (`buffer_sweep/syn/synth/script/activity.tcl`): as `ro`, with `wdata`
  and `waddr` held. Two diagnostic runs end in `_roq_ct0.1`. The revised numbers come from
  the corner re-analysis above, not from `collect_lut.py`, which stays frozen.

Diagnostic, 16-bit 1RW, 0.1 ns (area identical in both profiles):

| N | `ro` u_buf | `roq` u_buf | flip-flops | logic | input-net power left outside `u_buf` |
|---|---|---|---|---|---|
| 128 | 1.134 mW | 0.559 mW | 0.610 → 0.034 | 0.372 → 0.372 | 0.637 → 0.030 |
| 256 | 3.192 mW | 0.824 mW | 1.185 → 0.035 | 1.708 → 0.490 | 0.062 → 0.038 |

With `roq`, only the address nets stay outside `u_buf` (~0.03 mW), so the boundary no
longer matters. The 80/20 sweep (`compare_summary.csv`) has the same N = 256 step (logic
0.40 → 1.76 mW): its `wdata` also toggles every cycle and crosses the `u_buf` boundary.

## Item 6 (multi-port register files) and item 7 (first widths)

* **Item 6:** a 1W\<R\>R register file is 0.29–0.63× the area of R single-port copies (the
  storage flip-flops are shared; R = 2: ~0.6, R = 8: ~0.3), the opposite of CACTI's SRAM
  (1.70–3.56×).
* **Item 7, linearity check: area is linear in W.** Fit area = a + b·W per N on W ≤ 32:
  within 1.8% at every N = 8 … 1024, and it predicts the W = 64 runs within 0.9%. Total
  power: within 4.9%, W = 64 within 1.8% (`ro` profile; recheck after a `roq` rerun). The
  W-independent part a is ~5% of a 16-bit file. The remaining widths (W = 40, 44, 80, 88,
  128) can be extrapolated.

## pe reruns at 0.1 ns

Logic area moves by up to ±10% against the 5 ns runs, for designs at ~0 ps slack
(timing-driven sizing): `mac_mulint8_addfp16_pipe` 1,046 → 949 µm², `cvt_int14_fp16` −9%,
`mul_int3xfp16` +10%. Designs with hundreds of ps of slack move < 2%. Compare MAC and LUT
rows at one setting; `mac_mulint8_addfp16`, `add_fp16`, `mul_fp16` and the other original
pe designs only have 5 ns runs.

## Open for the owner

* ~~Rerun the read-only register files with `roq`~~: replaced by the corner re-analysis
  (2026-10-23, queue `rf_corners`), which needs no re-synthesis.
* **pe_sweep rebuild** under the revised naming and MAC precision (assumption revisions 4–5):
  waiting for the open MAC questions. All rebuilt pe designs will run at 0.1 ns, which also
  settles the 5 ns-only MAC baselines.
* **CACTI configuration**, the **4 ns rows** (kept), and **item 7**: extrapolate
  W = 40, 44, 80, 88, 128, or synthesize those 28 designs.
* **Not done (optional in the todo):** a direct 11-bit × wq-bit multiplier for int × fp16
  (item 5, tighter than i2flt + `CW_fp_mult`); the LUT precompute builder (item 12).
