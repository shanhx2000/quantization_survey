# Fig. 6, paper version (survey S5.1, latex/figures/lut-mac-by-quant-pair.tex): the int8-activation
# half of fig6_lut_mac_by_quant_pair.py (sram, bs = 1, opt baseline), area and energy side by side,
# ternary weights dropped, no title or footnote (the LaTeX caption carries them). Each cell is
# LUT-GEMM / MAC-GEMM for one weight format (rows) and weight bit group mu (= v; columns), against
# the pair's own int-q_W x int8 multiplier MAC (adds only for binary weights).
# Usage: python3 fig6_paper_int8.py -> fig6_paper_lut_mac_int8act_sram_bs1.{pdf,png}
import math

from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.patches import Rectangle

from figstyle import INK, INK_2, NEUTRAL_FILL, plt, save
import make_tables as mt  # noqa: E402  (path set by figstyle)

BS = 1
WA = 'int8'
LUT_ROW = 'LUT SRAM dup, pre-ignore+symm'
BASE_ROW = 'MAC opt'
WQS = [w for w in mt.WQ if w != 'ter']
WQ_TEXT = {'binary': 'Binary'}  # the rest print as INT<q>
# same diverging map as fig6_lut_mac_by_quant_pair.py (blue = LUT cheaper)
CMAP = LinearSegmentedColormap.from_list(
    'lut_vs_mac', ['#184f95', '#6da7ec', NEUTRAL_FILL, '#f0a09f', '#a83232'])
SPAN = 2.0  # colour saturates at 2^-2 = 0.25x and 2^2 = 4x
NORM = Normalize(-SPAN, SPAN)


def ratio(wq, v, metric):
    """(LUT / MAC, upper bound?) for one cell, or None when the LUT row is not costed."""
    rows = {lab: p for lab, _, p in mt.methods(wq, WA, BS)}
    lut, base = rows[LUT_ROW](v), rows[BASE_ROW](v)
    if lut is None or base is None:
        return None
    lc, bc = mt.cost(lut, LUT_ROW), mt.cost(base, BASE_ROW)
    if lc[metric] is None or bc[metric] is None:
        return None
    return lc[metric] / bc[metric], lc[2 + metric] or bc[2 + metric]


fig, axes = plt.subplots(1, 2, figsize=(3.45, 1.75), sharey=True)
for metric, (ax, name) in enumerate(zip(axes, ['Area', 'Energy'])):
    for i, wq in enumerate(WQS):
        for j, v in enumerate(mt.VS):
            val, bound = ratio(wq, v, metric)
            z = max(-SPAN, min(SPAN, math.log2(val)))
            ax.add_patch(Rectangle((j, i), 1, 1, facecolor=CMAP(NORM(z)), edgecolor='white', lw=0.8))
            ink = 'white' if abs(z) > 1.1 else INK
            ax.text(j + 0.5, i + 0.5, f'{val:.2f}' + ('*' if bound else ''), ha='center', va='center',
                    fontsize=5.5, color=ink)
            print(f'{name:6s} {wq:6s} mu={v}: {val:.2f}{"*" if bound else ""}')
    ax.set_xlim(0, len(mt.VS))
    ax.set_ylim(len(WQS), 0)
    ax.set_xticks([j + 0.5 for j in range(len(mt.VS))])
    ax.set_xticklabels([str(v) for v in mt.VS])
    ax.set_yticks([i + 0.5 for i in range(len(WQS))])
    ax.set_yticklabels([WQ_TEXT.get(w, w.upper()) for w in WQS])
    ax.tick_params(length=0)
    ax.grid(False)
    for side in ('left', 'bottom'):
        ax.spines[side].set_visible(False)
    ax.set_title(name, color=INK_2)
    ax.set_xlabel(r'Weight bit group $\mu$')
axes[0].set_ylabel('Weights', color=INK_2)
fig.tight_layout(w_pad=0.6)
save(fig, f'fig6_paper_lut_mac_int8act_sram_bs{BS}')
