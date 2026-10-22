# Status: MAC vs LUT data collection

Tracks `mac_lut_data_to_collect.md`. Started 2026-10-22. The missing (N, W, R) list was
rebuilt from that file's rules, because the cost-table repo is not on this machine. The
rules reproduce its explicit lists: item 2 (10 designs), item 3 (N = 512, 1024) and
item 7 (54 designs).

## Running

One sequential Genus queue (no two runs at once), in two chained tmux sessions:

| Session | Script | Contents |
|---|---|---|
| `lut_a` | `lut_queue_a.sh` | item 1: `buffer_n8 … buffer_n256` read-only, at 5 ns and at 0.05 ns clock transition; items 2–3: 10/11-bit register files and 16-bit N = 512, 1024 (read-only) |
| `lut_b` | `lut_queue_b.sh` | starts after `lut_a`. Items 5, 9, 10 (pe_sweep), item 11 (`add_fp16`, `mul_fp16` at 4 ns), item 6 (60 1W\<R\>R register files, `lut_multiport.list`), item 7 first widths W = 20, 22, 32, 64 (26 designs, `lut_wide_first.list`) |

Logs: `logs/lut_queue_a.log`, `logs/lut_queue_b.log`. Every new design passed its RTL test
(VCS against a Python golden model) before it was queued.

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

## Open for the owner

* **Item 7:** the remaining widths (W = 40, 44, 80, 88, 128; 28 designs) wait for the
  linearity check on the first widths.
* **Clock transition:** only item 1 is run at both 5 ns and 0.05 ns. Every other new register
  file uses the flow's 5 ns, which inflates flip-flop power about 4× (logic power is
  unaffected). If the tables use the 0.05 ns numbers, the others need the same rerun
  (`SYN_ACT=ro SYN_CLK_TRAN=0.05 buffer_sweep/scripts/run_syn.sh …`).
* **Not done (optional in the todo):** a direct 11-bit × wq-bit multiplier for int × fp16
  (item 5, tighter than i2flt + `CW_fp_mult`); the LUT precompute builder (item 12).
