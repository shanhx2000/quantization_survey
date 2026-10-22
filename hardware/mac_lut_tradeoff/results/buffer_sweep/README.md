# Buffer sweep: N x 16-bit buffer, 1RW / 1R1W / 1RW1R / 1RW3R (28nm, 500 MHz)

Two models of the same buffer, N = 4 ... 256, 16-bit elements, 1-cycle read/write:

* **CACTI SRAM** (`cacti_exp/`): CACTI copied from `crisscross/EVA/memory`, built locally
  and run with the EVA `sram_config.json` at 28nm. 1RW = one read/write port; 1R1W =
  one exclusive read port + one exclusive write port; 1RW1R / 1RW3R = one read/write
  port + one / three exclusive read ports. CACTI rejects arrays under 64 bytes, so there
  are no CACTI numbers for N < 32.
* **Synthesized RTL** (`src/buffer/`): flip-flop register file through the
  `micro26rcf/scripts/run_syn.sh` Genus flow (copied into `syn/synth`). Each top registers
  every input and output around the measured module `u_buf`. See `REPORT.md`.

Power at 500 MHz: a read/write port reads on 80% and writes on 20% of cycles, a read-only
port reads on 80%, a write-only port writes on 20%:

* CACTI: dynamic = 500 MHz x (0.8 E_read + 0.2 E_write + 0.8 E_read per extra read port);
  the range lets the read/write access be all reads or all writes; static = leakage +
  gate leakage.
* Genus: vectorless, with `syn/synth/script/activity.tcl` (`cs`=1, `we` P=0.2, every `re`
  P=0.8; addresses and data random). Static = leakage, dynamic = internal + switching.

## Commands (run from this folder)

```bash
python cacti_exp/run_buffer_sweep.py   # -> cacti_exp/buffer_cacti_summary.csv
python scripts/gen_rtl.py              # src/buffer/buffer_tops.v, tb/, designs.json
scripts/run_test.sh [design ...]       # RTL tests: golden generate -> VCS -> golden check
scripts/run_syn.sh  [design ...]       # Genus, one design after another (use tmux)
python scripts/collect.py              # -> compare_summary.csv
python scripts/make_report.py          # -> REPORT.md
```

Designs: `buffer_n<N>` (1RW), `buffer1r1w_n<N>` (1R1W), `buffer1rw1r_n<N>` (1RW1R) and
`buffer1rw3r_n<N>` (1RW3R). See `../pe_sweep/README.md`
for notes on the flow: no parallel runs from one `syn/synth`, Genus input from
`/dev/null`, and black-box flagging.

## LUT tables (`../todo/mac_lut_data_to_collect.md`)

* Register files `buffer_n<N>_w<W>` (1RW, W-bit entries; 16-bit ones keep `buffer_n<N>`) and
  `buffer1w<R>r_n<N>[_w<W>]` (one write port + R read ports, core `buffer_1w_nr`).
* Run variants, set from the environment of `scripts/run_syn.sh` and appended to the run
  folder name: `SYN_ACT=ro` (read-only: no writes, every read port reads every cycle),
  `SYN_CLK_TRAN=0.05` (clock transition in ns; the flow's default is 5), `SYN_PERIOD=4`
  (clock period in ns). Example: `SYN_ACT=ro scripts/run_syn.sh buffer_n512`.
* `python cacti_exp/run_lut_grid.py` -> `cacti_exp/lut_cacti_grid.csv` (CACTI, entry sizes
  2 ... 16 bytes, N = 8 ... 8192 single-port, R = 2 ... 8 read ports for N <= 256).
* `python scripts/collect_lut.py` -> `lut_buffer_costs.csv` (columns N, W, R, area and
  read-only power `syn_ro_*` / `cacti_ro_*`, one row per register file x variant and per
  CACTI table). `compare_summary.csv` stays the 16-bit sweep at the 80/20 workload.
