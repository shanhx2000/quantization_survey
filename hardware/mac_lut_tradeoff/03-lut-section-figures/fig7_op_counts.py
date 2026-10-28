# Fig. 7: operation counts of MAC-GEMM vs LUT-GEMM for one configuration (default int4 weights,
# fp16 activations, v = 8, bs = 1). (a) per output column and v-slice: multiplies, adds, LUT
# reads; (b) one table shared by a tile of N output columns, now including the adds that
# build the table (which the cost tables leave out as "pre-ignore").
# Counting rules (the 01 cost model): MAC-GEMM = bs*v multiplies + bs*v adds per column.
# LUT-GEMM = q_W reads (one per weight bit-plane) + bs*q_W adds per column; a sign-symmetric
# table of 2^(v-1) entries, each built with about one add (Hamming order), bs sums per entry.
# Usage: python3 fig7_op_counts.py [q_W] [v] [bs] [N]   (default 4 8 1 64)
#        -> fig7_op_counts_int<q_W>_fp16_v<v>_bs<bs>_n<N>.{pdf,png}
import sys

from figstyle import INK, INK_2, SERIES, plt, save

QW = int(sys.argv[1]) if len(sys.argv) > 1 else 4
V = int(sys.argv[2]) if len(sys.argv) > 2 else 8
BS = int(sys.argv[3]) if len(sys.argv) > 3 else 1
N = int(sys.argv[4]) if len(sys.argv) > 4 else 64
LUT, LUT_BUILD, MAC = SERIES[0], '#9ec5f4', SERIES[1]  # blue, blue step 200, orange
ENTRIES = 2 ** (V - 1)

OPS = ['multiplies', 'adds', 'LUT reads']
per_col = {'MAC-GEMM': [BS * V, BS * V, 0], 'LUT-GEMM': [0, BS * QW, QW]}
tile = {'MAC-GEMM': [N * BS * V, N * BS * V, 0], 'LUT-GEMM': [0, N * BS * QW, N * QW]}
build = BS * ENTRIES  # adds to fill one table, shared by the N columns

fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.4))
W = 0.36
for ax, counts, title in ((axes[0], per_col, f'(a) per output column, per {V} activations'),
                          (axes[1], tile, f'(b) one table shared by N = {N} output columns')):
    for k, (name, color) in enumerate((('MAC-GEMM', MAC), ('LUT-GEMM', LUT))):
        xs = [i + (k - 0.5) * W for i in range(len(OPS))]
        ys = counts[name]
        ax.bar(xs, ys, W * 0.92, color=color, label=name, zorder=3)
        tops = list(ys)
        if name == 'LUT-GEMM' and counts is tile:
            ax.bar(xs[1], build, W * 0.92, bottom=ys[1], color=LUT_BUILD, zorder=3,
                   label=f'LUT-GEMM: table build ({ENTRIES} entries)')
            tops[1] += build
        for x, y, top in zip(xs, ys, tops):
            ax.text(x, top, f'{top:,}' if top else '0', ha='center', va='bottom', fontsize=6.5,
                    color=INK)
        if name == 'LUT-GEMM' and counts is tile:
            ax.text(xs[1] + W * 0.55, ys[1] + build / 2, f'+{build:,}\nbuild', ha='left', va='center',
                    fontsize=5.5, color=INK_2)
    ax.set_xticks(range(len(OPS)))
    ax.set_xticklabels(OPS)
    ax.set_title(title, color=INK_2)
    ax.grid(axis='x', visible=False)
    ax.set_ylim(0, max(max(v) for v in counts.values()) * 1.18 + (build if counts is tile else 0) * 0.2)
    ax.tick_params(axis='x', length=0)
axes[0].set_ylabel('operations')
handles, labels = axes[1].get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, 1.0), ncol=3, handlelength=1.4)
fig.text(0.995, -0.02,
         f'int{QW} weights × fp16 activations, v = {V}, bs = {BS}. MAC-GEMM: one multiply and one add per '
         f'weight (fp16 × fp16 or int{QW} × fp16 multiplier). LUT-GEMM: one read per weight bit-plane from a\n'
         f'sign-symmetric table of 2^(v−1) = {ENTRIES} entries, one fp16 add per read; the 2^b shift and the '
         'sign flip are not counted. Table build ≈ one add per entry, amortized over the N columns.',
         ha='right', va='top', fontsize=5.5, color=INK_2)
fig.tight_layout(w_pad=1.5)
save(fig, f'fig7_op_counts_int{QW}_fp16_v{V}_bs{BS}_n{N}')
