# PE sweep v2: add / mul / MAC under the revised assumptions (TSMC 28nm HPC+, 500 MHz)

Rebuild of `../pe_sweep` with the owner's revisions of 2026-10-23
(`../todo/mac_lut_status.md`, *Assumption revisions*). `../pe_sweep` and its results stay
unchanged as the old results. Same flow as `pe_sweep`: the `micro26rcf/scripts/run_syn.sh`
Genus steps, copied into `syn/synth`.

## What changed from pe_sweep

* **Names:** `op_{a}x{b}_{out}`, e.g.
  * `mul_int8xint8_int16` (was `mul_int8`)
  * `mul_int4xfp16_fp16` (was `mul_int4xfp16`)
  * `mac_int8xint8_fp16` (was `mac_mulint8_addfp16`)

  `designs.json` and `pe_summary_v2.csv` keep the old name in `legacy_name`, which
  `make_tables.py` reads. Converters keep their names (`cvt_int<k>_fp16[_rtl]`).
* **MAC product at full precision:**
  * **int × int:** the product is exact, then converted once to the accumulator format, e.g.
    int8 × int8 → int16 → fp16, then fp16 + fp16 → fp16. This is the owner's chain, the same
    structure as pe_sweep.
  * **fp × fp with a wider accumulator:** `a` and `b` are widened exactly (`fp_up`) and
    multiplied in the accumulator format, so the product is exact. This covers fp8 × fp8 →
    fp16 / fp32 and fp16 × fp16 → fp32. pe_sweep rounded the product to the input format
    first.
  * **Same format** (fp16 × fp16 → fp16, fp32 × fp32 → fp32): unchanged.
* **Dropped:**
  * MACs whose integer accumulator can't hold the exact product: `int16 × int16 → int16`,
    and every fp → int16;
  * `int16 × int16 → fp16` and `fp32 × fp32 → fp16`;
  * counters (not needed);
  * the 4 ns runs (500 MHz only).
* **Synthesis setting:** every design runs at 0.1 ns clock transition. Run folders end in
  `_Periodclk2_ct0.1`.

## Confirmed modeling assumptions

* Data inputs random: P = 0.5, 0.5 toggles/cycle (`syn/synth/script/activity.tcl`).
* fp8 = IEEE-style E4M3 (max 240, exponent all-ones = Inf/NaN).
* FP units use `ieee_compliance=0` (subnormals read as zero, no NaN handling), round to
  nearest even.

## Commands (run from this folder)

```bash
python scripts/gen_rtl.py         # src/pe/pe_gen.v, tb/, designs.txt, designs.json (43 designs)
scripts/run_test.sh [design ...]  # RTL tests: golden generate -> VCS -> golden check
scripts/run_syn.sh  [design ...]  # Genus, one design after another (use tmux)
python scripts/collect.py         # -> pe_summary_v2.csv
```
