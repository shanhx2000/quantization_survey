# Fig. 3: register-file LUT vs SRAM LUT, area and read-only power against table size N, one
# panel per read-port count R. Solid: one table with R read ports and one write port. Dashed:
# the total of R single-port copies (the "dup" organization). Entries are W bits (16 = fp16
# partial sums). Data: the same unit costs as ../01-gemm-cost-per-frame (make_tables.lut).
# Hollow markers = upper bound (an SRAM table CACTI cannot model, costed as the smallest one
# it can).
# Usage: python3 fig3_reg_vs_sram.py [W]   (default W = 16)  ->  fig3_reg_vs_sram_w<W>.{pdf,png}
import sys

from matplotlib.ticker import FuncFormatter

from figstyle import INK_2, SERIES, plt, save
import make_tables as mt  # noqa: E402  (path set by figstyle)

W = int(sys.argv[1]) if len(sys.argv) > 1 else 16
PORTS = [1, 2, 4, 8]
NS = [8, 16, 32, 64, 128, 256, 512, 1024]
KINDS = [('reg', 'register file', SERIES[0]), ('sram', 'SRAM (CACTI)', SERIES[1])]


def points(kind, r, copies, metric):
    out = []
    for n in NS if r == 1 else [n for n in NS if n <= 256]:  # multi-port tables stop at 256
        area, power, ab, pb, _ = mt.lut(kind, n, W, 1 if copies else r)
        val, bound = (area, ab) if metric == 0 else (power, pb)
        if val is not None:
            out.append((n, val * (r if copies else 1), bound))
    return out


fig, axes = plt.subplots(2, len(PORTS), figsize=(7.0, 3.3), sharex=True, sharey='row')
for col, r in enumerate(PORTS):
    for row, ylabel in enumerate(['Area (µm²)', 'Read-only power (mW)']):
        ax = axes[row][col]
        for kind, name, color in KINDS:
            for copies in ([False] if r == 1 else [False, True]):
                pts = points(kind, r, copies, row)
                if not pts:
                    continue
                xs, ys, bounds = zip(*pts)
                label = (f'{name}: R one-port copies, total' if copies else
                         f'{name}: one table, R read + 1 write ports') if col == len(PORTS) - 1 else None
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
            ax.set_title(f'R = {r} read port{"s" if r > 1 else ""}', color=INK_2)
        else:
            ax.set_xlabel('table entries N')
        if col == 0:
            ax.set_ylabel(ylabel)
axes[0][0].yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:g}'))
axes[1][0].yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:g}'))
handles, labels = axes[0][-1].get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, 1.0), ncol=2,
           handlelength=2.2, columnspacing=1.2)
fig.text(0.995, -0.01, f'{W}-bit entries; register files: Genus, TSMC 28 nm, 500 MHz, 0.1 ns clock '
         'transition; SRAM: CACTI 28 nm, 300 K; hollow = upper bound.\nDashed = R x the one-port table. '
         'In SRAM every extra port widens and heightens each cell, so one R-port table outgrows R copies; '
         'register files share their flip-flops and add only read muxes.', ha='right', va='top',
         fontsize=5.5, color=INK_2)
fig.tight_layout(h_pad=0.6, w_pad=0.4)
save(fig, f'fig3_reg_vs_sram_w{W}')
