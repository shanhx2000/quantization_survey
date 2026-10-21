# mac_lut_tradeoff — hardware cost of MAC vs. LUT datapaths

Created **2026-10-21** at the human's request. Discussions of the area and power trade-off
between MAC (multiply-accumulate) datapaths and LUT (lookup table) datapaths, backed by
synthesis and CACTI numbers from two sweeps on `cmp00`.

This folder is in git. Its siblings `../pe_sweep/` and `../buffer_sweep/` are **not**: they
are full working copies of the sweeps (~800 MB of synthesis runs, VCS builds and test
vectors), ignored by the repo's `.gitignore`. `results/` keeps the part worth versioning.

## Results snapshot (`results/`)

Copied on **2026-10-21** from `cmp00:~/isca26hw/micro26rcf/playground/` (the source is not a
git repo). Both reports were generated there on 2026-10-15. Setup for both: Genus 21.1,
TSMC 28nm HPC+ 9-track, TT 0.9 V 25 °C, 500 MHz (2 ns clock), Genus vectorless power.

| File | What it is |
|---|---|
| [`pe_sweep/REPORT.md`](results/pe_sweep/REPORT.md) | Logic-only area and power of add, mul, MAC (`mul<x>_add<y>`) and counters over int4/int8/fp8/int16/fp16/fp32 |
| [`pe_sweep/pe_summary.csv`](results/pe_sweep/pe_summary.csv) | The numbers behind that report, one row per design (39 designs) |
| [`pe_sweep/designs.txt`](results/pe_sweep/designs.txt), [`designs.json`](results/pe_sweep/designs.json) | Design list, with the product → accumulator conversion each MAC uses |
| [`pe_sweep/README.md`](results/pe_sweep/README.md) | How the sweep is built and run, and the traps in the flow |
| [`buffer_sweep/REPORT.md`](results/buffer_sweep/REPORT.md) | N × 16-bit buffer (N = 4 … 256), 1RW (one read/write port) and 1R1W (one read + one write port): flip-flop register file from Genus vs. SRAM from CACTI |
| [`buffer_sweep/compare_summary.csv`](results/buffer_sweep/compare_summary.csv) | Synthesized and CACTI numbers side by side, one row per (port, N) |
| [`buffer_sweep/cacti_exp/`](results/buffer_sweep/cacti_exp/) | CACTI summary, raw CACTI output (`cacti_stats.csv`) and its config (`sram_config.json`, 28nm) |
| [`buffer_sweep/designs.json`](results/buffer_sweep/designs.json), [`README.md`](results/buffer_sweep/README.md) | Design list; how the sweep is built and run |

**Paths inside the copied files are relative to the sweep folder** (`scripts/`, `src/`,
`work/synth/...`). They resolve in `../pe_sweep/` and `../buffer_sweep/`, not here.

**Caveats the reports carry**, restated so they are not lost when a number is quoted:
flip-flop power is an upper bound (the flow sets a 5 ns clock transition on a 2 ns clock);
22 of 39 PE designs close timing at ≤5 ps slack, so their area includes upsizing; and
CACTI cannot model arrays under 64 bytes, so there is no SRAM number for N < 32.

### Refreshing the snapshot

From `quantization_survey/hardware/`:

```bash
rsync -a cmp00:isca26hw/micro26rcf/playground/{buffer_sweep,pe_sweep} ./
cp -p pe_sweep/{README.md,REPORT.md,pe_summary.csv,designs.json,designs.txt} mac_lut_tradeoff/results/pe_sweep/
cp -p buffer_sweep/{README.md,REPORT.md,compare_summary.csv,designs.json} mac_lut_tradeoff/results/buffer_sweep/
cp -p buffer_sweep/cacti_exp/{buffer_cacti_summary.csv,cacti_stats.csv,sram_config.json} mac_lut_tradeoff/results/buffer_sweep/cacti_exp/
```

`rsync -a` without `--delete` keeps local files that were removed on `cmp00`. Update the
snapshot date above when you refresh.

## Discussions

One entry per discussion: a single file `NN-<slug>.md` for a note or report, or a subfolder
`NN-<slug>/` with its own `README.md` when it needs scripts or figures. Numbers are never
reused.

| # | Discussion | Status |
|---|---|---|
| — | *none yet* | |
