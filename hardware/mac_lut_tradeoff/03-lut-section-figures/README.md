# 03 — Figures for the LUT section (§5.1, stage3 T1)

Written 2026-10-23. Drawing scripts for the figures proposed in the section notes
(`latex/drafts/g3-lut/notes.md`, not in git). Each script writes a `.pdf` for LaTeX and a
`.png` preview here. **Nothing here is in the manuscript**; copying a figure into `latex/`
is the owner's step.

| Script | Output | What it shows |
|---|---|---|
| [`fig1_bitsplit_to_lut.py`](fig1_bitsplit_to_lut.py) | `fig1_bitsplit_to_lut` | Toy tile, v = 2 activations, 4-bit weights, N = 6 columns: (a) bit-splitting MAC-GEMM, (b) the partial sums repeat, (c) a 2^v-entry LUT built with one add, (d) LUT-GEMM. Every value is computed from the weights in the script |
| [`fig2_mac_vs_lut_sram.py`](fig2_mac_vs_lut_sram.py) `[v] [bs]` | `fig2a_area_v6_bs1`, `fig2b_power_v6_bs1` | Area and read-only power per v-slice of MAC-GEMM (fp16, int-wq × wa multiplier, int8) vs SRAM LUT-GEMM (full and sign-symmetric table), across weight formats, one panel per activation format |
| [`fig3_reg_vs_sram.py`](fig3_reg_vs_sram.py) `[W]` | `fig3_reg_vs_sram_w16` | Register-file vs SRAM table, area and read-only power against entries N, one panel per read-port count R; one R-port table (solid) vs R single-port copies (dashed) |

Figures 2 and 3 import the cost model from
[`../01-gemm-cost-per-frame/make_tables.py`](../01-gemm-cost-per-frame/make_tables.py), so
they show exactly the numbers in its tables; `*` there is a hollow marker here. Rerun all
three after every results sync:

```bash
cd hardware/mac_lut_tradeoff/03-lut-section-figures
python3 fig1_bitsplit_to_lut.py && python3 fig2_mac_vs_lut_sram.py && python3 fig3_reg_vs_sram.py
```

They need matplotlib (installed for the user's `python3`; run without `-I`).

**Style.** `figstyle.py`: 7 pt sans text, TrueType fonts embedded in the PDF, categorical
slots blue / orange / aqua (+ yellow in fig. 2) in fixed order, validated with the dataviz
palette checker on a white surface (all checks pass; aqua is under 3:1 contrast, so every
aqua mark in fig. 1 carries a text label). Fig. 1 is 7.0 in wide (`figure*`); fig. 2 is
3.45 in (one column); fig. 3 is 7.0 in.

**Data state at 2026-10-23 13:30** (the cmp00 sync of that time): LUT tables from
`buffer_costs_v2.csv` (register files at 0.1 ns clock transition, read-only corner; CACTI at
300 K). MAC baselines from the old `pe_summary.csv`, still at 5 ns clock transition; the
0.1 ns rebuild (`pe_sweep_v2`) was running. Rerun once it lands.
