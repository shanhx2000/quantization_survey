# Switching activity and other modeling assumptions (2026-10-23)

> **Owner decisions, 2026-10-23** (tracked in `mac_lut_status.md`, *Assumption revisions*):
> * register files use three corners (read-only, write-only, idle) and interpolate;
> * data stays random at 0.5 toggles/cycle;
> * the MAC product keeps full precision, and MACs whose integer accumulator can't hold it
>   are dropped;
> * names become `op_{a}x{b}_{out}`;
> * fp8 stays IEEE-style E4M3.
>
> The old results are kept unchanged.

The playground sweeps (`buffer_sweep`, `pe_sweep`) source `syn/synth/script/activity.tcl`.
I (Claude) wrote that file on 2026-10-14 without a template, and the owner never confirmed its
values. The original micro26rcf flow sets no activity. This note records how much the file
changes the results, and which modeling assumptions are still open.

## With vs without `activity.tcl`

Same RTL and flow; 500 MHz; 0.1 ns clock transition. Runs from `todo/act_compare.sh`:
`…_Periodclk2_ct0.1` (with the file, profile `rw`) vs `…_Periodclk2_none_ct0.1` (without it).
The power column covers the measured instance only (`u_buf` / `u_core`).

| Design | Area (µm²) | Power without (mW) | Power with (mW) | With ÷ without |
|---|---|---|---|---|
| `buffer_n16` | 682 | 0.138 | 0.286 | 2.1 |
| `buffer_n128` | 5,192 | 0.586 | 1.169 | 2.0 |
| `buffer1r1w_n128` | 5,191 | 0.609 | 1.167 | 1.9 |
| `add_int8` | 15.5 | 0.0102 | 0.0242 | 2.4 |
| `mul_int8` | 144 | 0.125 | 0.262 | 2.1 |
| `add_fp16` | 526 | 1.221 | 1.545 | 1.3 |
| `mul_fp16` | 398 | 0.628 | 1.072 | 1.7 |
| `mac_mulint8_addfp16` | 1,545 | 3.012 | 3.483 | 1.2 |
| `cnt_up_w8` | 27.7 | 0.0198 | 0.0274 | 1.4 |

* **Area, slack and leakage are identical** in every pair. Activity changes only the power
  estimate, not the netlist.
* **Dynamic power is 1.2–2.4× higher with the file.** The FP units and the MAC are already
  busy at the lower input rate, so their ratio is smallest.
* **Genus's default activity, read back from a netlist with `lp_computed_toggle_rate`:**
  every input has P = 0.5 and 0.1 toggles/ns, i.e. 0.2 toggles/cycle. That rate is
  `lp_default_toggle_percentage` (0.2) × the clock rate. The other default,
  `lp_default_toggle_rate` (0.02/ns), does not apply when the design has a clock.
* **Without the file, control inputs are random too.** `cs` and `we` get the same default,
  so a buffer is accessed on about half the cycles and writes on half of those. It is not
  the 80/20 workload.

## What `activity.tcl` assumes (unconfirmed)

| Input | Setting |
|---|---|
| Data and address bits | P = 0.5, 0.5 toggles/cycle (a new random value every cycle) |
| `we` | P = 0.2, 0.32 toggles/cycle (independent each cycle) |
| `re` | P = 0.8, 0.32 toggles/cycle |
| `rst_n`, `cs`, `en` | held at 1 |
| `dir` | P = 0.5, 0.02 toggles/cycle |
| Profile `ro` | `we` = 0, `re` = 1; write data still random (a bug, see `mac_lut_status.md`) |
| Profile `roq` | as `ro`, with `wdata` / `waddr` held |
| Profile `none` | nothing set (the original flow) |

## Other modeling assumptions waiting for confirmation

* **MAC:** the FP product is rounded to the input format before accumulation (fp8×fp8 → fp8,
  then widened). FP → int16 accumulation rounds the product to an integer with no scaling.
  The `int16 × int16 → int16` MAC keeps the low 16 product bits. Integer accumulators wrap.
  Everything is single-cycle (except `_pipe`).
* **fp8:** IEEE-style E4M3 (max 240, Inf/NaN at exponent all-ones), not OCP E4M3 (max 448).
  All FP units use `ieee_compliance=0`, so subnormals flush to zero. `add_fp8` is a custom RTL
  adder, because Genus 21.1 has no `CW_fp8_add`.
* **Register files:** built from flip-flops (not latches or a memory macro), with a registered
  read port and per-entry clock gating from the flow.
* **CACTI:** EVA `sram_config.json` used unchanged: 360 K, ECC on, `itrs-hp`, L3 settings.
  Entries are rounded up to whole bytes (10- and 11-bit entries modeled as 16-bit).
* **Workload details:** 1R1W `re` and `we` are independent, so 16% of cycles do both and 16%
  do neither. Extra read ports read on 80% of cycles. Counters count every cycle.
* **LUT list:** rebuilt from the todo's rules, because the cost-table repo isn't on this machine.
