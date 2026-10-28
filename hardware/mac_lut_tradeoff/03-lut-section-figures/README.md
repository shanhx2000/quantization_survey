# 03 — Figures for the LUT section (§5.1, stage3 T1)

Written 2026-10-23. Drawing scripts for the figures proposed in the section notes
(`latex/drafts/g3-lut/notes.md`, not in git). Each script writes a `.pdf` for LaTeX and a
`.png` preview here. **Nothing here is in the manuscript**; copying a figure into `latex/`
is the owner's step.

| Script | Output | What it shows |
|---|---|---|
| [`fig1_bitsplit_to_lut.py`](fig1_bitsplit_to_lut.py) | `fig1_bitsplit_to_lut` | Toy tile, v = 2 activations, 4-bit weights, N = 6 columns: (a) bit-splitting MAC-GEMM, (b) the partial sums repeat, (c) a 2^v-entry LUT built with one add, (d) LUT-GEMM. Every value is computed from the weights in the script |
| [`fig2_mac_vs_lut_sram.py`](fig2_mac_vs_lut_sram.py) `[v] [bs]` | `fig2a_area_v6_bs1`, `fig2b_power_v6_bs1` | Area and read-only power per v-slice of MAC-GEMM (fp16, int-wq × wa multiplier, int8) vs SRAM LUT-GEMM (full and sign-symmetric table), across weight formats, one panel per activation format |
| [`fig3_reg_vs_sram.py`](fig3_reg_vs_sram.py) `[W]` | `fig3_reg_vs_sram_w16` | Register-file vs SRAM table, area and read-only power against entries N, one panel per read-port count R; solid = one table with R read + 1 write ports, dashed = **the total** of R one-port copies |
| [`fig4_per_mac_vs_v_bs.py`](fig4_per_mac_vs_v_bs.py) `[q_W] [w_a]` | `fig4_per_mac_vs_v_bs_int4_fp16` | MAC-GEMM vs LUT-GEMM (SRAM and register-file tables, sign-symmetric) against v, one panel per batch size, **normalized per MAC**: area per MAC/cycle and energy per MAC |
| [`fig5_lut_mac_ratio_vs_v_bs.py`](fig5_lut_mac_ratio_vs_v_bs.py) `[q_W] [w_a] [opt\|fp16\|int8]` | `fig5_lut_mac_ratio_vs_v_bs_int4_fp16_opt` | LUT-GEMM / MAC-GEMM (default: the int-q_W × w_a multiplier MAC) against v, one line per batch size, for SRAM and register-file tables, area and energy |
| [`fig6_lut_mac_by_quant_pair.py`](fig6_lut_mac_by_quant_pair.py) `[sram\|reg] [bs] [opt\|fp16\|int8]` | `fig6_lut_mac_by_quant_pair_sram_bs{1,2,4,8}_opt`, `…_reg_bs1_opt` | **By quantization pair:** LUT-GEMM / MAC-GEMM for every weight format × v, one panel per activation format and metric (area, energy); each pair against its own int-q_W × w_a multiplier MAC; diverging blue (LUT cheaper) to red |
| [`fig7_op_counts.py`](fig7_op_counts.py) `[q_W] [v] [bs] [N]` | `fig7_op_counts_int4_fp16_v8_bs1_n64` | **Operation counts**, int4 × fp16, v = 8, bs = 1: (a) per output column and 8 activations, MAC-GEMM 8 multiplies + 8 adds vs LUT-GEMM 4 reads + 4 adds; (b) one 128-entry table shared by N = 64 columns: 512 + 512 vs 256 reads + 256 adds + 128 build adds |
| [`fig7_op_counts_slide.py`](fig7_op_counts_slide.py) `[q_W] [v] [bs] [N]` | `fig7_op_counts_slide_int4_fp16_v8_bs1_n64` | **Slide version of fig. 7 (16:9):** the steps behind the counts (MAC-GEMM: multiply, accumulate; LUT-GEMM: build the table once, bit-split the weights, look up, accumulate), each with its count, next to the two bar panels. Shares `draw_bars()` with `fig7_op_counts.py` |

Figures 2–6 import the cost model from
[`../01-gemm-cost-per-frame/make_tables.py`](../01-gemm-cost-per-frame/make_tables.py), so
they show exactly the numbers in its tables; `*` there is a hollow marker here. Rerun all
of them after every results sync:

```bash
cd hardware/mac_lut_tradeoff/03-lut-section-figures
python3 fig1_bitsplit_to_lut.py && python3 fig2_mac_vs_lut_sram.py && python3 fig3_reg_vs_sram.py
python3 fig4_per_mac_vs_v_bs.py && python3 fig5_lut_mac_ratio_vs_v_bs.py
for bs in 1 2 4 8; do python3 fig6_lut_mac_by_quant_pair.py sram $bs; done
python3 fig6_lut_mac_by_quant_pair.py reg
python3 fig7_op_counts.py && python3 fig7_op_counts_slide.py
```

They need matplotlib (installed for the user's `python3`; run without `-I`).

**Style.** `figstyle.py`: 7 pt sans text, TrueType fonts embedded in the PDF, categorical
slots blue / orange / aqua (+ yellow in fig. 2) in fixed order, validated with the dataviz
palette checker on a white surface (all checks pass; aqua is under 3:1 contrast, so every
aqua mark in fig. 1 carries a text label). Fig. 1 is 7.0 in wide (`figure*`); fig. 2 is
3.45 in (one column); fig. 3 and fig. 4 are 7.0 in; figs. 5 and 6 are 3.45 in. Fig. 4 adds
magenta (slot 5); fig. 6 uses the blue / grey / red diverging pair; fig. 5 uses a one-hue blue ramp for batch size (passes the ordinal checks).

**Data state at 2026-10-28** (the cmp00 sync of that day): LUT tables from
`buffer_costs_v2.csv` (register files at 0.1 ns clock transition, read-only corner with the
input nets; CACTI at 300 K). MAC units from `pe_sweep_v2/pe_summary_v2.csv`, also 0.1 ns.

## What figs. 4 and 5 show (int4 weights, fp16 activations, 2026-10-28 data)

Ratios are LUT-GEMM / the int4 × fp16 multiplier MAC at the same v and bs (below 1, LUT-GEMM
is cheaper). Both LUTs are sign-symmetric, one table copy per read; table build excluded.

| | v = 4 | v = 6 | v = 7 | v = 8 |
|---|---|---|---|---|
| SRAM LUT, area | 0.89–0.99* | 0.59–0.66 | 0.58–0.63 | 0.61–0.65 |
| SRAM LUT, energy | 0.73–0.74* | 0.49 | 0.42–0.43 | 0.38–0.39 |
| Register-file LUT, area | 1.17–1.18 | 1.62–1.65 | 2.34–2.40 | 3.73–3.82 |
| Register-file LUT, energy | 0.77–0.78 | 0.54–0.56 | 0.48–0.51 | 0.45–0.48 |

Ranges span bs = 1, 2, 4, 8; `*` = upper bound (CACTI cannot model the 8-entry table).

- **Energy:** LUT-GEMM wins at every v and gains with v. Per MAC, SRAM LUT-GEMM costs
  3.2 pJ at v = 4 and 1.7 pJ at v = 8, against 4.4 pJ for the int4 × fp16 MAC and 5.2 pJ for
  the fp16 MAC.
- **Area:** the SRAM LUT is smallest at v = 6–7. At v = 8 the 2^v table starts to cost more
  than the extra activations save. Register-file tables are larger than the MAC at every v
  and grow fast (3.7–3.8× at v = 8).
- **Batch size barely matters** (area ratios move by ≤ 0.1, energy by ≤ 0.03). Under the cost
  model a batch multiplies the MAC by bs and widens every LUT entry by bs, and table area is
  close to linear in entry width, so both sides scale together. The model counts no table
  build, which a batch does not amortize either (each batch row has its own activations).

## Fig. 3: why SRAM copies beat one multi-port SRAM (owner's question, 2026-10-28)

The dashed line is the **total** of R one-port tables (R × the one-port area). For SRAM it
lies below the one-table line because CACTI grows every cell in both directions with each port
(a wordline per port in the cell height, bitlines per port in its width). For a 64-entry
16-bit table: 1 port 34.4 × 7.1 µm = 242 µm²; 1 write + 8 read ports 130.0 × 39.8 µm =
5,172 µm², against 1,939 µm² for 8 copies. Area grows roughly with the square of the port count,
copies only linearly; the usual reason SRAM read bandwidth comes from replicated banks. Register
files share the flip-flops and add one read mux per port, so there one multi-port table wins
(0.29–0.63× of the copies). The comparison is not perfectly like for like: the one-table design
has a separate write port, each copy one shared read/write port.

## What fig. 6 shows (2026-10-28 data, bs = 1)

LUT-GEMM / the pair's own int-q_W × w_a multiplier MAC (adds only for binary and ternary).

- **SRAM tables, energy:** LUT-GEMM wins almost everywhere, most for binary, 2-bit and ternary
  weights (0.14–0.33× at v ≥ 6). It loses at v = 4 for int6–int8 weights with int8 activations
  and int8 weights with fp16 activations (all upper bounds), and for int8 × int8 at v = 6–7
  (1.20×, 1.04×).
- **SRAM tables, area:** with fp16 activations it wins up to int6 at v ≥ 6 (int8 ≈ parity).
  With int8 activations the int-q_W × int8 MAC is cheap, so it loses from int6 up. Ternary
  loses at v ≥ 7, where tables grow as 3^v.
- **Register-file tables:** they keep most of the energy win but lose area for most pairs at
  v ≥ 6 (up to 6.3× at int8, v = 8).

**Other batch sizes** (`…_sram_bs2/4/8_opt`, added 2026-10-28): the maps barely change.
Energy stays within ±0.02 of bs = 1 almost everywhere. Area moves for two reasons:
- **int8 activations gain with bs**, most for ternary weights (v = 8: 3.48× at bs = 1, 2.12× at
  bs = 8). CACTI stores whole bytes, so an 11-bit entry wastes 5 of 16 bits at bs = 1 and
  nothing at bs = 8 (88 bits = 11 bytes).
- **fp16 activations lose slightly with bs** (int8 weights, v = 6–8: 0.95–1.05× at bs = 1,
  1.01–1.06× at bs = 8), because CACTI area grows a little faster than entry width.

## Fig. 7: operation counts (int4 × fp16, v = 8, bs = 1)

Per output column and 8 activations, MAC-GEMM does 8 multiplies and 8 adds. LUT-GEMM does no
multiply, 4 table reads (one per bit-plane) and 4 adds. The sign-symmetric table has 2^(v−1) =
128 entries and costs about 128 adds to build, shared by every column that reads it. With
N = 64 columns: 512 multiplies + 512 adds against 256 reads + 384 adds (256 + 128 build). The
build pays for itself in adds alone once more than 32 columns share the table (128 build adds
/ 4 adds saved per column); the multiplies are saved from the first column.
