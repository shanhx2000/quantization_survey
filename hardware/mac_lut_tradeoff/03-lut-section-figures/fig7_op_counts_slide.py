# Fig. 7, slide version (16:9): how the operation counts of MAC-GEMM and LUT-GEMM come about,
# step by step (left), next to the bar charts of fig7_op_counts.py (right). Default: int4
# weights, fp16 activations, v = 8, bs = 1, a tile of N = 64 output columns. The example weight
# column is only for the bit-split picture; every count follows from q_W, v, bs and N.
# Usage: python3 fig7_op_counts_slide.py [q_W] [v] [bs] [N]   (default 4 8 1 64)
#        -> fig7_op_counts_slide_int<q_W>_fp16_v<v>_bs<bs>_n<N>.{pdf,png}
import sys

from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

from figstyle import INK, INK_2, MUTED, NEUTRAL_FILL, plt, save
from fig7_op_counts import LUT, LUT_BUILD, MAC, config, counts, draw_bars

QW, V, BS, N = config(sys.argv[1:])
per_col, tile, BUILD = counts(QW, V, BS, N)
ENTRIES = 2 ** (V - 1)
EXAMPLE_W = [5, 12, 3, 9, 14, 7, 0, 10][:V] + [6] * max(0, V - 8)  # one weight column, for the picture

fig = plt.figure(figsize=(10.0, 5.625))
gs = fig.add_gridspec(2, 2, width_ratios=[1.75, 1], left=0.005, right=0.99, top=0.86, bottom=0.13,
                      wspace=0.10, hspace=0.55)
ax = fig.add_subplot(gs[:, 0])
ax.set_xlim(0, 62)
ax.set_ylim(0, 50)
ax.axis('off')


def box(x, y, w, h, edge, fill='white', lw=1.0):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle='round,pad=0.25,rounding_size=0.8',
                                facecolor=fill, edgecolor=edge, lw=lw))


def badge(x, y, text, color, w=11.6):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - 1.1), w, 2.2, boxstyle='round,pad=0.15,rounding_size=1.0',
                                facecolor=color, alpha=0.20, edgecolor=color, lw=1.0))
    ax.text(x, y, text, ha='center', va='center', fontsize=7.5, color=INK, weight='bold')


def arrow(x1, x2, y):
    ax.add_patch(FancyArrowPatch((x1, y), (x2, y), arrowstyle='-|>', mutation_scale=9, color=INK_2, lw=1.0))


def t(x, y, s, size=7.5, color=INK, **kw):
    ax.text(x, y, s, fontsize=size, color=color, **kw)


def cells(x, y, labels, w, h, fill, size=6.5):
    for i, lab in enumerate(labels):
        ax.add_patch(Rectangle((x + i * w, y), w, h, facecolor=fill, edgecolor='white', lw=0.8))
        ax.text(x + (i + 0.5) * w, y + h / 2, lab, ha='center', va='center', fontsize=size, color=INK)


# ---------------- MAC-GEMM -------------------------------------------------------------
t(0.4, 49.2, 'MAC-GEMM', size=10, color=MAC, weight='bold', va='top')
t(13.5, 49.0, f'per output column n: {V} activations × {V} int{QW} weights', size=7.5, color=INK_2, va='top')
Y0, H = 31.5, 13.5
box(0.6, Y0, 14.2, H, MUTED)
t(7.7, Y0 + H - 1.4, 'inputs', size=7.5, color=INK_2, ha='center', va='top')
cells(1.6, Y0 + 6.6, [f'$x_{k}$' for k in range(V)], 1.53, 2.2, NEUTRAL_FILL)
t(7.7, Y0 + 5.9, 'fp16 activations', size=6, color=INK_2, ha='center', va='top')
cells(1.6, Y0 + 1.6, [str(w) for w in EXAMPLE_W], 1.53, 2.2, '#fbe0d4')
t(7.7, Y0 + 0.9, f'int{QW} weights $w_{{k,n}}$', size=6, color=INK_2, ha='center', va='top')
arrow(15.4, 17.4, Y0 + H / 2)

box(18.0, Y0, 19.0, H, MAC)
t(27.5, Y0 + H - 1.4, '① multiply', size=8.5, weight='bold', ha='center', va='top')
t(27.5, Y0 + 7.6, r'$p_k = x_k \cdot w_{k,n}$', size=8.5, ha='center', va='center')
t(27.5, Y0 + 5.1, f'for k = 0 … {V - 1}', size=7, color=INK_2, ha='center', va='center')
badge(27.5, Y0 + 2.0, f'{per_col["MAC-GEMM"][0]} multiplies', MAC)
arrow(37.6, 39.6, Y0 + H / 2)

box(40.2, Y0, 21.0, H, MAC)
t(50.7, Y0 + H - 1.4, '② accumulate', size=8.5, weight='bold', ha='center', va='top')
t(50.7, Y0 + 7.6, r'$acc_n$ += $p_k$', size=8.5, ha='center', va='center')
t(50.7, Y0 + 5.1, f'one add per product', size=7, color=INK_2, ha='center', va='center')
badge(50.7, Y0 + 2.0, f'{per_col["MAC-GEMM"][1]} adds', MAC)

t(0.6, 28.4, f'per column: {per_col["MAC-GEMM"][0]} multiplies + {per_col["MAC-GEMM"][1]} adds     '
             f'→  × N = {N} columns: {tile["MAC-GEMM"][0]:,} multiplies + {tile["MAC-GEMM"][1]:,} adds',
  size=7.5, color=INK, va='center')
ax.plot([0.6, 61.2], [26.3, 26.3], color=NEUTRAL_FILL, lw=1.2)

# ---------------- LUT-GEMM -------------------------------------------------------------
t(0.4, 24.6, 'LUT-GEMM', size=10, color=LUT, weight='bold', va='top')
Y1, H1 = 5.6, 15.2
# step 1: once per activation slice, shared by all N columns
box(0.6, Y1, 14.2, H1, LUT, fill='#f1f6fd')
t(7.7, Y1 + H1 - 1.4, '① build the table', size=8.5, weight='bold', ha='center', va='top')
t(7.7, Y1 + 11.0, f'once per {V} activations,', size=6.5, color=INK_2, ha='center', va='center')
t(7.7, Y1 + 9.4, f'shared by all N columns', size=6.5, color=INK_2, ha='center', va='center')
t(7.7, Y1 + 7.3, r'$T[p] = \Sigma_k \pm x_k$', size=8.5, ha='center', va='center')
t(7.7, Y1 + 4.6, f'{ENTRIES} sign patterns p,\n≈ 1 add each (Hamming order)', size=6.3, color=INK_2,
  ha='center', va='center')
badge(7.7, Y1 + 1.9, f'{BUILD} adds', LUT_BUILD, w=11.0)

# per-column steps, grouped under a bracket
ax.add_patch(Rectangle((16.3, Y1 - 1.6), 45.2, H1 + 3.6, facecolor='none', edgecolor=NEUTRAL_FILL, lw=1.0,
                       ls=(0, (3, 2))))
t(38.9, Y1 + H1 + 1.4, 'per output column n', size=7, color=INK_2, ha='center', va='center',
  bbox=dict(facecolor='white', edgecolor='none', pad=1.0))

box(17.2, Y1, 14.0, H1, LUT)
t(24.2, Y1 + H1 - 1.4, '② bit-split $w_{k,n}$', size=8.5, weight='bold', ha='center', va='top')
cw, ch = 1.45, 1.55
for i, b in enumerate(range(QW - 1, -1, -1)):
    y = Y1 + 9.4 - i * ch
    t(18.6, y + ch / 2, f'b{b}', size=6, color=INK_2, ha='right', va='center')
    cells(18.8, y, [str((w >> b) & 1) for w in EXAMPLE_W], cw, ch, '#dbe8fb', size=6)
t(24.2, Y1 + 2.4, f'{QW} bit-planes; each row is\nan {V}-bit index $i_b$ (no op)', size=6.3, color=INK_2,
  ha='center', va='center')
arrow(31.8, 33.4, Y1 + H1 / 2)

box(34.0, Y1, 13.2, H1, LUT)
t(40.6, Y1 + H1 - 1.4, '③ look up', size=8.5, weight='bold', ha='center', va='top')
t(40.6, Y1 + 8.6, r'$T[\,i_b\,]$', size=9, ha='center', va='center')
t(40.6, Y1 + 5.4, f'one read per plane,\nb = 0 … {QW - 1}; the top bit\nof $i_b$ picks the sign', size=6.3, color=INK_2,
  ha='center', va='center')
badge(40.6, Y1 + 1.9, f'{per_col["LUT-GEMM"][2]} LUT reads', LUT, w=11.0)
arrow(47.8, 49.4, Y1 + H1 / 2)

box(50.0, Y1, 11.2, H1, LUT)
t(55.6, Y1 + H1 - 1.4, '④ accumulate', size=8.5, weight='bold', ha='center', va='top')
t(55.6, Y1 + 8.6, r'$acc_n$ += $2^b\, T[i_b]$', size=8.5, ha='center', va='center')
t(55.6, Y1 + 5.7, '2^b: an exponent\nadd, not counted', size=6.3, color=INK_2, ha='center', va='center')
badge(55.6, Y1 + 1.9, f'{per_col["LUT-GEMM"][1]} adds', LUT, w=9.6)

t(0.6, 1.2, f'per column: {per_col["LUT-GEMM"][2]} reads + {per_col["LUT-GEMM"][1]} adds     '
            f'→  × N = {N}: {tile["LUT-GEMM"][2]:,} reads + {tile["LUT-GEMM"][1]:,} adds, '
            f'+ {BUILD} build adds once', size=7.5, color=INK, va='center')

# ---------------- bars -------------------------------------------------------------------
ax_a, ax_b = fig.add_subplot(gs[0, 1]), fig.add_subplot(gs[1, 1])
draw_bars(ax_a, ax_b, QW, V, BS, N, size=7)
ax_b.set_ylabel('operations')
handles, labels = ax_b.get_legend_handles_labels()
fig.legend(handles, labels, loc='upper right', bbox_to_anchor=(0.99, 0.925), ncol=3, handlelength=1.2,
           fontsize=6.5)
fig.text(0.01, 0.975, f'MAC-GEMM vs LUT-GEMM: where the operation counts come from', fontsize=12,
         color=INK, weight='bold', va='top')
fig.text(0.01, 0.925, f'int{QW} weights × fp16 activations, v = {V}, bs = {BS}, tile of N = {N} output columns',
         fontsize=8.5, color=INK_2, va='top')
fig.text(0.99, 0.02, 'Same counting rules as the cost tables: the sign flip and the 2^b shift are not counted; '
         'the table build is the part those tables leave out ("pre-ignore").', fontsize=6.5, color=INK_2,
         ha='right', va='bottom')
save(fig, f'fig7_op_counts_slide_int{QW}_fp16_v{V}_bs{BS}_n{N}')
