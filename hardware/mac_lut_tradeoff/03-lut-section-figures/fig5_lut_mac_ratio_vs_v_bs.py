# Fig. 5: LUT-GEMM cost relative to a MAC-GEMM baseline, against vector length v, one line per
# batch size bs; columns = where the table lives (SRAM, register file), rows = area and
# energy. Below 1, LUT-GEMM is cheaper. The ratio is taken at equal work (same v and bs), so
# it is the same per slice or per MAC. Data: make_tables' cost model (../01-gemm-cost-per-frame);
# hollow markers = an upper bound there (`*`).
# Usage: python3 fig5_lut_mac_ratio_vs_v_bs.py [q_W] [w_a] [baseline]
#        (default int4 fp16 opt; baseline: opt = int-q_W x w_a multiplier MAC, fp16, int8)
#        -> fig5_lut_mac_ratio_vs_v_bs_<q_W>_<w_a>_<baseline>.{pdf,png}
import sys

from matplotlib.ticker import FixedLocator, FuncFormatter

from figstyle import BASELINE, INK_2, plt, save
import make_tables as mt  # noqa: E402  (path set by figstyle)

QW = sys.argv[1] if len(sys.argv) > 1 else 'int4'
WA = sys.argv[2] if len(sys.argv) > 2 else 'fp16'
BASE = sys.argv[3] if len(sys.argv) > 3 else 'opt'
BASE_ROW = {'opt': 'MAC opt', 'fp16': 'MAC fp16', 'int8': 'MAC int8'}[BASE]
BASE_TEXT = {'opt': f'{QW} × {WA} multiplier MAC', 'fp16': 'fp16 MAC', 'int8': 'int8 MAC'}[BASE]
# batch sizes as an ordinal blue ramp, light -> dark (dataviz palette steps 250 / 400 / 550 / 700;
# passes the ordinal checks on white)
RAMP = ['#86b6ef', '#3987e5', '#1c5cab', '#0d366b']
LUTS = [('LUT SRAM dup, pre-ignore+symm', 'LUT in SRAM'),
        ('LUT reg dup, pre-ignore+symm', 'LUT in register files')]


def cost(label, v, bs):
    parts = {lab: p for lab, _, p in mt.methods(QW, WA, bs)}[label](v)
    return None if parts is None else mt.cost(parts, label)


fig, axes = plt.subplots(2, len(LUTS), figsize=(3.45, 3.0), sharex=True, sharey=True)
for col, (lut, title) in enumerate(LUTS):
    for row, metric in enumerate(['area', 'energy']):
        ax = axes[row][col]
        ax.axhline(1, color=BASELINE, lw=1.0, zorder=1)
        for bs, color in zip(mt.BS, RAMP):
            pts = []
            for v in mt.VS:
                c, b = cost(lut, v, bs), cost(BASE_ROW, v, bs)
                if c and b and c[row] is not None and b[row] is not None:
                    pts.append((v, c[row] / b[row], c[2 + row] or b[2 + row]))
            if not pts:
                continue
            ax.plot([p[0] for p in pts], [p[1] for p in pts], color=color, lw=1.2,
                    label=f'bs = {bs}' if col == 0 and row == 0 else None, zorder=3)
            for v, y, bound in pts:
                ax.plot(v, y, 'o', ms=3.0, color=color, mfc='white' if bound else color, mew=0.9, zorder=4)
        ax.set_yscale('log', base=2)
        ax.yaxis.set_major_locator(FixedLocator([0.25, 0.5, 1, 2, 4]))
        ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:g}×'))
        ax.minorticks_off()
        ax.set_xticks(mt.VS)
        ax.grid(axis='x', visible=False)
        if row == 0:
            ax.set_title(title, color=INK_2)
        else:
            ax.set_xlabel('vector length $v$')
        if col == 0:
            ax.set_ylabel(f'LUT / MAC, {metric}')
handles, labels = axes[0][0].get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, 1.0), ncol=len(mt.BS),
           handlelength=1.6, columnspacing=1.0)
fig.text(0.99, -0.01, f'1× = the {BASE_TEXT} (grey line); below it, LUT-GEMM is cheaper.\n'
         f'Weights {QW}, activations {WA}; sign-symmetric LUTs, one copy per read;\n'
         'LUT build excluded; hollow = upper bound', ha='right',
         va='top', fontsize=5.5, color=INK_2)
fig.tight_layout(h_pad=0.6, w_pad=0.5)
save(fig, f'fig5_lut_mac_ratio_vs_v_bs_{QW}_{WA}_{BASE}')
