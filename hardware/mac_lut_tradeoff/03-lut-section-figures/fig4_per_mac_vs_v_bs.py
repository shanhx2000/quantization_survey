# Fig. 4: MAC-GEMM vs LUT-GEMM across vector length v and batch size bs, normalized per MAC
# (one activation x one weight x one batch row): area per MAC/cycle and energy per MAC, one
# panel per bs. Raw per-slice cost grows with v * bs for every method, so only the
# normalized cost compares across v and bs. Every point is make_tables' cost model (same data
# as ../01-gemm-cost-per-frame); hollow markers = an upper bound there (`*`).
# Usage: python3 fig4_per_mac_vs_v_bs.py [q_W] [w_a]   (default int4 fp16)
#        -> fig4_per_mac_vs_v_bs_<q_W>_<w_a>.{pdf,png}
import sys

from matplotlib.ticker import FuncFormatter

from figstyle import INK_2, SERIES, plt, save
import make_tables as mt  # noqa: E402  (path set by figstyle)

QW = sys.argv[1] if len(sys.argv) > 1 else 'int4'
WA = sys.argv[2] if len(sys.argv) > 2 else 'fp16'
YELLOW, MAGENTA = '#eda100', '#e87ba4'  # categorical slots 4 and 5, after figstyle's three

# (row label in make_tables, legend text, color, marker)
SHOWN = [('LUT SRAM dup, pre-ignore+symm', 'LUT-GEMM, SRAM table', SERIES[0], '^'),
         ('LUT reg dup, pre-ignore+symm', 'LUT-GEMM, register-file table', MAGENTA, 'D'),
         ('MAC fp16', 'MAC-GEMM fp16', SERIES[1], 'o'),
         ('MAC opt', f'MAC-GEMM, {QW} × {WA} multiplier', SERIES[2], 's')]
if WA == 'int8':
    SHOWN.append(('MAC int8', 'MAC-GEMM int8 (int16 accumulate)', YELLOW, 'v'))


def per_mac(label, v, bs):
    """(area per MAC/cycle um2, energy per MAC pJ, area bound?, power bound?) or None."""
    parts = {lab: p for lab, _, p in mt.methods(QW, WA, bs)}[label](v)
    if parts is None:
        return None
    area, power, ab, pb = mt.cost(parts, label)
    if area is None or power is None:
        return None
    macs = v * bs  # MACs per cycle for one output column
    return area / macs, power / mt.F_GHZ / macs, ab, pb  # mW / GHz = pJ per cycle


fig, axes = plt.subplots(2, len(mt.BS), figsize=(7.0, 3.3), sharex=True, sharey='row')
for col, bs in enumerate(mt.BS):
    for row in range(2):
        ax = axes[row][col]
        for label, legend, color, marker in SHOWN:
            pts = [(v, c) for v in mt.VS if (c := per_mac(label, v, bs))]
            if not pts:
                continue
            xs = [v for v, _ in pts]
            ys = [c[row] for _, c in pts]
            ax.plot(xs, ys, color=color, lw=1.3, label=legend if col == 0 and row == 0 else None, zorder=3)
            for (v, c), y in zip(pts, ys):
                bound = c[2 + row]
                ax.plot(v, y, marker, ms=3.6, color=color, mfc='white' if bound else color, mew=0.9, zorder=4)
        ax.set_xticks(mt.VS)
        ax.set_ylim(bottom=0)
        ax.grid(axis='x', visible=False)
        if row == 0:
            ax.set_title(f'bs = {bs}', color=INK_2)
        else:
            ax.set_xlabel('vector length $v$')
axes[0][0].set_ylabel('Area per MAC/cycle (µm²)')
axes[1][0].set_ylabel('Energy per MAC (pJ)')
axes[0][0].yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:,.0f}'))
handles, labels = axes[0][0].get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, 1.0), ncol=len(SHOWN),
           handlelength=2.0, columnspacing=1.2)
fig.text(0.995, -0.01, f'weights {QW}, activations {WA}; sign-symmetric LUTs, one table copy per read; '
         '28 nm, 500 MHz; LUT build excluded; hollow = upper bound', ha='right', va='top',
         fontsize=5.5, color=INK_2)
fig.tight_layout(h_pad=0.6, w_pad=0.4)
save(fig, f'fig4_per_mac_vs_v_bs_{QW}_{WA}')
