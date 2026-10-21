# Buffer sweep: N x 16-bit buffer, 1RW and 1R1W (28nm, 500 MHz)

Two models of the same buffer, N = 4 ... 256, 16-bit elements, 1-cycle read/write:

* **CACTI SRAM** (`cacti_exp/`): CACTI copied from `crisscross/EVA/memory`, built locally
  and run with the EVA `sram_config.json` at 28nm. 1RW = one read/write port; 1R1W =
  one exclusive read port + one exclusive write port. CACTI rejects arrays under
  64 bytes, so there are no CACTI numbers for N < 32.
* **Synthesized RTL** (`src/buffer/`): flip-flop register file through the
  `micro26rcf/scripts/run_syn.sh` Genus flow (copied into `syn/synth`). Each top registers
  every input and output around the measured module `u_buf`. See `REPORT.md`.

Power assumes one 16-bit access per cycle at 500 MHz, 80% reads / 20% writes:

* CACTI: dynamic = 500 MHz x (0.8 E_read + 0.2 E_write); the range runs from all reads to
  all writes; static = leakage + gate leakage.
* Genus: vectorless, with `syn/synth/script/activity.tcl` (1RW: `cs`=1, `we` P=0.2;
  1R1W: `re` P=0.8, `we` P=0.2; addresses and data random). Static = leakage,
  dynamic = internal + switching.

## Commands (run from this folder)

```bash
python cacti_exp/run_buffer_sweep.py   # -> cacti_exp/buffer_cacti_summary.csv
python scripts/gen_rtl.py              # src/buffer/buffer_tops.v, tb/, designs.json
scripts/run_test.sh [design ...]       # RTL tests: golden generate -> VCS -> golden check
scripts/run_syn.sh  [design ...]       # Genus, one design after another (use tmux)
python scripts/collect.py              # -> compare_summary.csv
python scripts/make_report.py          # -> REPORT.md
```

Designs: `buffer_n<N>` (1RW) and `buffer1r1w_n<N>` (1R1W). See `../pe_sweep/README.md`
for notes on the flow: no parallel runs from one `syn/synth`, Genus input from
`/dev/null`, and black-box flagging.
