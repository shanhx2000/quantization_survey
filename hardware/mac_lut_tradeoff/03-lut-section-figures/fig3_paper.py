# Fig. 3, paper version (survey S5.1, latex/figures/lut-table-ports.tex): same data as
# fig3_reg_vs_sram.py, drawn at the manuscript text width (430 pt = 5.95 in), no footnote (the
# LaTeX caption carries it), and the two table organizations named as in the text:
#   multi-ported = one table with R read ports (+ 1 write port)    -> solid
#   replicated   = R copies with one read port each, total cost    -> dashed
# The x-axis drops the symbol N, which the text uses for output columns.
# Usage: python3 fig3_paper.py [W]   (default W = 16)  ->  fig3_paper_reg_vs_sram_w<W>.{pdf,png}
import sys

from matplotlib.ticker import FuncFormatter

from figstyle import INK_2, SERIES, plt, save
import make_tables as mt  # noqa: E402  (path set by figstyle)

W = int(sys.argv[1]) if len(sys.argv) > 1 else 16
PORTS = [1, 2, 4, 8]
NS = [8, 16, 32, 64, 128, 256, 512, 1024]
KINDS = [('reg', 'Register file', SERIES[0]), ('sram', 'SRAM', SERIES[1])]


def points(kind, r, copies, metric):
    out = []
    for n in NS if r == 1 else [n for n in NS if n <= 256]:  # multi-port tables stop at 256
        area, power, ab, pb, _ = mt.lut(kind, n, W, 1 if copies else r)
        val, bound = (area, ab) if metric == 0 else (power, pb)
        if val is not None:
            out.append((n, val * (r if copies else 1), bound))
    return out


fig, axes = plt.subplots(2, len(PORTS), figsize=(5.9, 3.0), sharex=True, sharey='row')
for col, r in enumerate(PORTS):
    for row, ylabel in enumerate(['Area (µm²)', 'Read-only power (mW)']):
        ax = axes[row][col]
        for kind, name, color in KINDS:
            for copies in ([False] if r == 1 else [False, True]):
                pts = points(kind, r, copies, row)
                if not pts:
                    continue
                xs, ys, bounds = zip(*pts)
                label = f'{name}, {"replicated" if copies else "multi-ported"}' \
                    if col == len(PORTS) - 1 else None
                ax.plot(xs, ys, color=color, ls=(0, (3, 1.5)) if copies else '-', lw=1.3, label=label, zorder=3)
                for x, y, b in pts:
                    ax.plot(x, y, 'o', ms=3.0, color=color, mfc='white' if b else color, mew=0.9, zorder=4)
        ax.set_xscale('log', base=2)
        ax.set_yscale('log')
        ax.set_xticks(NS[::2])
        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x)}'))
        ax.minorticks_off()
        ax.grid(axis='x', visible=False)
        if row == 0:
            ax.set_title(f'$R = {r}$ read port{"s" if r > 1 else ""}', color=INK_2)
        else:
            ax.set_xlabel('Table entries')
        if col == 0:
            ax.set_ylabel(ylabel)
axes[0][0].yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:g}'))
axes[1][0].yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:g}'))
handles, labels = axes[0][-1].get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, 1.0), ncol=4,
           handlelength=2.2, columnspacing=1.2)
fig.tight_layout(h_pad=0.6, w_pad=0.4)
save(fig, f'fig3_paper_reg_vs_sram_w{W}')
