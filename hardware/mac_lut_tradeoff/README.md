# mac_lut_tradeoff — hardware cost of MAC vs. LUT datapaths

Created **2026-10-21** at the human's request. Discussions of the area and power trade-off
between MAC (multiply-accumulate) datapaths and LUT (lookup table) datapaths, backed by
synthesis and CACTI numbers from two sweeps on `cmp00`.

This folder is in git. Its siblings `../pe_sweep/` and `../buffer_sweep/` are **not**: they
are full working copies of the sweeps (4.6 GB of synthesis runs, VCS builds and test
vectors; 14 GB on 2026-10-23), ignored by the repo's `.gitignore`, as is `../todo/` (the data
collection's queue scripts and logs). `results/` keeps the part worth versioning.

## Results snapshot (`results/`)

Last synced **2026-10-23 12:15** from `cmp00:~/isca26hw/micro26rcf/playground/` (not a git
repo), **while the cmp00 agent was revising the register-file power** (queue `rf_corners`
had just started): see [`todo/mac_lut_status.md`](results/todo/mac_lut_status.md),
section *Assumption revisions*, for the owner's 2026-10-23 decisions. Earlier syncs:
2026-10-21, 2026-10-22 19:00. Setup: Genus 21.1, TSMC 28nm HPC+ 9-track, TT 0.9 V 25 °C,
500 MHz (2 ns clock), Genus vectorless power. The flow's clock transition changed from 5 ns
to 0.1 ns on 2026-10-22 at 16:40; every run records which one it used.

**Old vs revised results (cmp00, 2026-10-23).** `compare_summary.csv`, `lut_buffer_costs.csv`
and `pe_summary.csv` are frozen as the *old* results and their collectors are not rerun.
Revised results go to new files: so far `rf_corner_costs.csv`; a rebuilt pe_sweep with new
design names (and a `legacy_name` column) is pending.

| File | What it is |
|---|---|
| [`pe_sweep/REPORT.md`](results/pe_sweep/REPORT.md) | Logic-only area and power of add, mul, MAC (`mul<x>_add<y>`) and counters over int4/int8/fp8/int16/fp16/fp32 |
| [`pe_sweep/pe_summary.csv`](results/pe_sweep/pe_summary.csv) | The numbers behind that report, one row per design: the 39 designs of the report, plus (2026-10-22) mixed int × int8 / int × fp16 multipliers, int → fp16 converters, a pipelined MAC, and `add_fp16` / `mul_fp16` at 4 ns (`@Periodclk4`) |
| [`pe_sweep/designs.txt`](results/pe_sweep/designs.txt), [`designs.json`](results/pe_sweep/designs.json) | Design list, with the product → accumulator conversion each MAC uses |
| [`pe_sweep/README.md`](results/pe_sweep/README.md) | How the sweep is built and run, and the traps in the flow |
| [`buffer_sweep/REPORT.md`](results/buffer_sweep/REPORT.md) | N × 16-bit buffer (N = 4 … 256), 1RW (one read/write port) and 1R1W (one read + one write port): flip-flop register file from Genus vs. SRAM from CACTI |
| [`buffer_sweep/compare_summary.csv`](results/buffer_sweep/compare_summary.csv) | Synthesized and CACTI numbers side by side, one row per (port, N), at 80% read / 20% write |
| [`buffer_sweep/lut_buffer_costs.csv`](results/buffer_sweep/lut_buffer_costs.csv) | **Every LUT table** (old results, frozen): register files (one row per clock-transition variant, `primary` = the 0.1 ns run) and CACTI SRAM, by `N` entries, `W` bits and `R` read ports. `01` reads its areas and SRAM rows; **its register-file `ro` power overstates read-only power 2–4× and is not used** |
| [`buffer_sweep/rf_corner_costs.csv`](results/buffer_sweep/rf_corner_costs.csv) | **Revised register-file power**: per design, the read-only (`ro_*`), write-only (`wo_*`) and idle (`idle_*`) corners of a power-only re-analysis of the 0.1 ns netlist, plus per-access energies. Growing while queue `rf_corners` runs. `01` reads `ro_total_mW` |
| [`buffer_sweep/cacti_exp/`](results/buffer_sweep/cacti_exp/) | CACTI LUT grid (`lut_cacti_grid.csv`), the older 16-bit summary, raw CACTI output (`cacti_stats.csv`) and its config (`sram_config.json`, 28nm) |
| [`buffer_sweep/designs.json`](results/buffer_sweep/designs.json), [`README.md`](results/buffer_sweep/README.md) | Design list; how the sweep is built and run |
| [`todo/`](results/todo/) | The data-collection plan (`mac_lut_data_to_collect.md`), the collector's status at sync time (`mac_lut_status.md`), and the activity and modeling assumptions with the owner's decisions (`activity_assumptions.md`) |

**Paths inside the copied files are relative to the sweep folder** (`scripts/`, `src/`,
`work/synth/...`). They resolve in `../pe_sweep/` and `../buffer_sweep/`, not here.

**Caveats the reports carry**, restated so they are not lost when a number is quoted:
flip-flop power from a 5 ns clock-transition run is an upper bound (0.05 ns gives 0.49–0.83×
of it); 22 of the 39 original PE designs close timing at ≤5 ps slack, so their area includes
upsizing; and CACTI cannot model arrays under 64 bytes, nor N = 8 or 16 at any width.

### Refreshing the snapshot

From `quantization_survey/hardware/`:

```bash
rsync -a cmp00:isca26hw/micro26rcf/playground/{buffer_sweep,pe_sweep,todo} ./
cp -p pe_sweep/{README.md,REPORT.md,pe_summary.csv,designs.json,designs.txt} mac_lut_tradeoff/results/pe_sweep/
cp -p buffer_sweep/{README.md,REPORT.md,compare_summary.csv,designs.json,lut_buffer_costs.csv,rf_corner_costs.csv} mac_lut_tradeoff/results/buffer_sweep/
cp -p buffer_sweep/cacti_exp/{buffer_cacti_summary.csv,cacti_stats.csv,sram_config.json,lut_cacti_grid.csv} mac_lut_tradeoff/results/buffer_sweep/cacti_exp/
cp -p todo/*.md mac_lut_tradeoff/results/todo/
python3 mac_lut_tradeoff/01-gemm-cost-per-frame/make_tables.py
```

`rsync -a` without `--delete` keeps local files that were removed on `cmp00`; a run that is
in progress during the copy may report vanished files, which is harmless.
**Before a sync, read `todo/mac_lut_status.md` on cmp00**: the agent there revises
assumptions and moves results to new files, and `make_tables.py` may need to follow.
Update the snapshot date above when you refresh.

## Discussions

One entry per discussion: a single file `NN-<slug>.md` for a note or report, or a subfolder
`NN-<slug>/` with its own `README.md` when it needs scripts or figures. Numbers are never
reused.

| # | Discussion | Status |
|---|---|---|
| 01 | [MAC-GEMM vs LUT-GEMM cost per quantization frame](01-gemm-cost-per-frame/README.md): area / read-only power for wq ∈ {int1, ter, int2, int3, int4, int6, int8} × wa ∈ {int8, fp16} × bs ∈ {1, 2, 4, 8}, v ∈ {4, 6, 7, 8}; LUT as duplicated or multi-port tables, register file or SRAM. Built by `make_tables.py` | 2026-10-23 sync: all MAC and SRAM cells and all register-file areas up to W = 32 and 64 filled; register-file power waits for the read-only corner (queue `rf_corners`); W = 40, 44, 80, 88, 128 wait for an owner decision (extrapolate or synthesize) |
| 02 | [How large is the int → fp16 converter after the multiplier?](02-int-to-fp-converter-cost/README.md) | Answered: 272 µm² of 1,763 in the single-cycle `mac_mulint8_addfp16`, 120 µm² standalone; the rest of the gap is timing upsizing |
