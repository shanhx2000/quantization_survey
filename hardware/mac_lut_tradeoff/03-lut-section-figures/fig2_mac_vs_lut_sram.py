# Fig. 2a / 2b: area and read-only power of MAC-GEMM vs SRAM LUT-GEMM, per v-slice and cycle at
# 500 MHz, across weight formats, for one vector length v and batch size bs. Every point is the
# cost model of ../01-gemm-cost-per-frame (make_tables.py), so the figure and the tables agree.
# Hollow markers = an upper bound there (`*`: an SRAM table CACTI cannot model).
# Usage: python3 fig2_mac_vs_lut_sram.py [v] [bs]   (default v = 6, bs = 1)
#        -> fig2a_area_v<v>_bs<bs>.{pdf,png}, fig2b_power_v<v>_bs<bs>.{pdf,png}
import sys

from matplotlib.ticker import FuncFormatter

from figstyle import INK_2, SERIES, plt, save
import make_tables as mt  # noqa: E402  (path set by figstyle)

V = int(sys.argv[1]) if len(sys.argv) > 1 else 6
BS = int(sys.argv[2]) if len(sys.argv) > 2 else 1
YELLOW = '#eda100'  # categorical slot 4, after figstyle's three

# (row label in make_tables, legend text, color, dashed?)
SHOWN = [('LUT SRAM dup, pre-ignore+symm', 'LUT-GEMM, SRAM (sign-symmetric)', SERIES[0], False),
         ('LUT SRAM dup, pre-ignore', 'LUT-GEMM, SRAM (full table)', SERIES[0], True),
         ('MAC fp16', 'MAC-GEMM fp16', SERIES[1], False),
         ('MAC opt', 'MAC-GEMM, int-$q_W$ × $w_a$ multiplier', SERIES[2], False),
         ('MAC int8', 'MAC-GEMM int8 (int16 accumulate)', YELLOW, False)]


def series(wa, metric):
    """{row label: [(x, value, upper bound?)]} over the weight formats."""
    out = {label: [] for label, *_ in SHOWN}
    for x, wq in enumerate(mt.WQ):
        rows = {label: parts for label, _, parts in mt.methods(wq, wa, BS)}
        for label, *_ in SHOWN:
            parts = rows[label](V)
            if parts is None:
                continue
            area, power, ab, pb = mt.cost(parts, label)
            val, bound = (area, ab) if metric == 'area' else (power, pb)
            if val is not None:
                out[label].append((x, val, bound))
    return out


def figure(metric, ylabel, name, fmt):
    fig, axes = plt.subplots(1, 2, figsize=(3.45, 2.05), sharey=True)
    for ax, wa in zip(axes, mt.WA):
        data = series(wa, metric)
        for label, legend, color, dashed in SHOWN:
            pts = data[label]
            if not pts:
                continue
            xs, ys, bounds = zip(*pts)
            ax.plot(xs, ys, color=color, ls=(0, (3, 1.5)) if dashed else '-', lw=1.4, label=legend, zorder=3)
            for x, y, b in pts:
                ax.plot(x, y, 'o', ms=3.4, color=color, mfc='white' if b else color, mew=1.0, zorder=4)
        ax.set_title(f'$w_a$ = {wa}', color=INK_2)
        ax.set_xticks(range(len(mt.WQ)))
        ax.set_xticklabels([{'ter': 'ternary'}.get(w, w) for w in mt.WQ], rotation=40, ha='right',
                           rotation_mode='anchor')
        ax.set_xlabel('weight format')
        ax.set_ylim(bottom=0)
        ax.grid(axis='x', visible=False)
        ax.yaxis.set_major_formatter(FuncFormatter(fmt))
    axes[0].set_ylabel(ylabel)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, 1.0), ncol=2,
               handlelength=2.2, columnspacing=1.0)
    fig.text(0.99, -0.02, f'$v$ = {V}, bs = {BS}; per $v$-slice, 500 MHz; hollow = upper bound',
             ha='right', va='top', fontsize=5.5, color=INK_2)
    fig.tight_layout(w_pad=0.6)
    save(fig, f'{name}_v{V}_bs{BS}')


figure('area', 'Area (µm²)', 'fig2a_area', lambda y, _: f'{y / 1000:g}k' if y else '0')
figure('power', 'Power (mW)', 'fig2b_power', lambda y, _: f'{y:g}')
