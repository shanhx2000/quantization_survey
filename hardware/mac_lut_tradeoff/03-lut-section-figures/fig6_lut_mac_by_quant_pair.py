# Fig. 6: where LUT-GEMM beats MAC-GEMM, by weight x activation quantization pair. Each cell is
# LUT-GEMM / MAC-GEMM for one weight format (rows) and vector length v (columns); panels are the
# activation format (columns) and the metric, area or energy (rows). The MAC is the pair's own
# int-q_W x w_a multiplier MAC by default (adds only for binary and ternary weights). Blue: LUT
# cheaper; red: MAC cheaper; grey: parity. Data: make_tables' cost model (../01-gemm-cost-per-frame).
# Usage: python3 fig6_lut_mac_by_quant_pair.py [sram|reg] [bs] [opt|fp16|int8]
#        (default sram 1 opt) -> fig6_lut_mac_by_quant_pair_<kind>_bs<bs>_<baseline>.{pdf,png}
import math
import sys

from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.patches import Rectangle

from figstyle import INK, INK_2, NEUTRAL_FILL, plt, save
import make_tables as mt  # noqa: E402  (path set by figstyle)

KIND = sys.argv[1] if len(sys.argv) > 1 else 'sram'
BS = int(sys.argv[2]) if len(sys.argv) > 2 else 1
BASE = sys.argv[3] if len(sys.argv) > 3 else 'opt'
LUT_ROW = {'sram': 'LUT SRAM dup, pre-ignore+symm', 'reg': 'LUT reg dup, pre-ignore+symm'}[KIND]
BASE_ROW = {'opt': 'MAC opt', 'fp16': 'MAC fp16', 'int8': 'MAC int8'}[BASE]
BASE_TEXT = {'opt': 'its own int-$q_W$ × $w_a$ multiplier MAC', 'fp16': 'the fp16 MAC',
             'int8': 'the int8 MAC'}[BASE]
# diverging blue <-> red with a neutral grey midpoint (dataviz diverging pair; blue = LUT wins)
CMAP = LinearSegmentedColormap.from_list(
    'lut_vs_mac', ['#184f95', '#6da7ec', NEUTRAL_FILL, '#f0a09f', '#a83232'])
SPAN = 2.0  # colour saturates at 2^-2 = 0.25x and 2^2 = 4x
NORM = Normalize(-SPAN, SPAN)
WQ_TEXT = {'ter': 'ternary'}


def ratio(wq, wa, v, metric):
    """(LUT / MAC, upper bound?) for one cell, or None when the LUT row is not costed."""
    rows = {lab: p for lab, _, p in mt.methods(wq, wa, BS)}
    lut, base = rows[LUT_ROW](v), rows[BASE_ROW](v)
    if lut is None or base is None:
        return None
    lc, bc = mt.cost(lut, LUT_ROW), mt.cost(base, BASE_ROW)
    if lc[metric] is None or bc[metric] is None:
        return None
    return lc[metric] / bc[metric], lc[2 + metric] or bc[2 + metric]


fig, axes = plt.subplots(2, len(mt.WA), figsize=(3.45, 3.6), sharex=True, sharey=True)
for col, wa in enumerate(mt.WA):
    for metric, name in enumerate(['area', 'energy']):
        ax = axes[metric][col]
        for i, wq in enumerate(mt.WQ):
            for j, v in enumerate(mt.VS):
                r = ratio(wq, wa, v, metric)
                if r is None:
                    ax.add_patch(Rectangle((j, i), 1, 1, facecolor='white', edgecolor=NEUTRAL_FILL, lw=0.6))
                    ax.text(j + 0.5, i + 0.5, '—', ha='center', va='center', fontsize=5.5, color=INK_2)
                    continue
                val, bound = r
                z = max(-SPAN, min(SPAN, math.log2(val)))
                ax.add_patch(Rectangle((j, i), 1, 1, facecolor=CMAP(NORM(z)), edgecolor='white', lw=0.8))
                ink = 'white' if abs(z) > 1.1 else INK
                ax.text(j + 0.5, i + 0.5, f'{val:.2f}' + ('*' if bound else ''), ha='center', va='center',
                        fontsize=5.5, color=ink)
        ax.set_xlim(0, len(mt.VS))
        ax.set_ylim(len(mt.WQ), 0)
        ax.set_xticks([j + 0.5 for j in range(len(mt.VS))])
        ax.set_xticklabels([str(v) for v in mt.VS])
        ax.set_yticks([i + 0.5 for i in range(len(mt.WQ))])
        ax.set_yticklabels([WQ_TEXT.get(w, w) for w in mt.WQ])
        ax.tick_params(length=0)
        ax.grid(False)
        for side in ('left', 'bottom'):
            ax.spines[side].set_visible(False)
        if metric == 0:
            ax.set_title(f'activations {wa}', color=INK_2)
        else:
            ax.set_xlabel('vector length $v$')
        if col == 0:
            ax.set_ylabel(f'{name}: weights', color=INK_2)
where = {'sram': 'SRAM', 'reg': 'register-file'}[KIND]
fig.text(0.5, 1.0, f'LUT-GEMM ({where} table) / MAC-GEMM, bs = {BS}', ha='center', va='bottom',
         fontsize=7, color=INK, weight='bold')
fig.text(0.99, -0.01, f'Each pair against {BASE_TEXT}. Blue: LUT-GEMM cheaper; red: MAC-GEMM cheaper.\n'
         'Sign-symmetric LUT, one copy per read, build excluded; * = upper bound.'
         + ('\n— = not costed (ternary register files above v = 6).' if KIND == 'reg' else ''),
         ha='right', va='top',
         fontsize=5.5, color=INK_2)
fig.tight_layout(h_pad=0.8, w_pad=0.6)
save(fig, f'fig6_lut_mac_by_quant_pair_{KIND}_bs{BS}_{BASE}')
