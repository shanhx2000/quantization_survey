# Fig. 7: operation counts of MAC-GEMM vs LUT-GEMM for one configuration (default int4 weights,
# fp16 activations, v = 8, bs = 1). (a) per output column and v-slice: multiplies, adds, LUT
# reads; (b) one table shared by a tile of N output columns, now including the adds that
# build the table (which the cost tables leave out as "pre-ignore").
# Counting rules (the 01 cost model): MAC-GEMM = bs*v multiplies + bs*v adds per column.
# LUT-GEMM = q_W reads (one per weight bit-plane) + bs*q_W adds per column; a sign-symmetric
# table of 2^(v-1) entries, each built with about one add (Hamming order), bs sums per entry.
# fig7_op_counts_slide.py imports draw_bars() for the slide version with the step diagram.
# Usage: python3 fig7_op_counts.py [q_W] [v] [bs] [N]   (default 4 8 1 64)
#        -> fig7_op_counts_int<q_W>_fp16_v<v>_bs<bs>_n<N>.{pdf,png}
import sys

from figstyle import INK, INK_2, SERIES, plt, save

LUT, LUT_BUILD, MAC = SERIES[0], '#9ec5f4', SERIES[1]  # blue, blue step 200, orange
OPS = ['multiplies', 'adds', 'LUT reads']


def config(argv):
    qw, v, bs, n = (int(a) for a in (argv + ['4', '8', '1', '64'][len(argv):]))
    return qw, v, bs, n


def counts(qw, v, bs, n):
    """Per-column and per-tile counts, and the adds that build one table."""
    per_col = {'MAC-GEMM': [bs * v, bs * v, 0], 'LUT-GEMM': [0, bs * qw, qw]}
    tile = {'MAC-GEMM': [n * bs * v, n * bs * v, 0], 'LUT-GEMM': [0, n * bs * qw, n * qw]}
    return per_col, tile, bs * 2 ** (v - 1)


def draw_bars(ax_a, ax_b, qw, v, bs, n, size=6.5):
    per_col, tile, build = counts(qw, v, bs, n)
    w = 0.36
    for ax, cnt, title in ((ax_a, per_col, f'(a) per output column, per {v} activations'),
                           (ax_b, tile, f'(b) one table shared by N = {n} output columns')):
        for k, (name, color) in enumerate((('MAC-GEMM', MAC), ('LUT-GEMM', LUT))):
            xs = [i + (k - 0.5) * w for i in range(len(OPS))]
            ys = cnt[name]
            ax.bar(xs, ys, w * 0.92, color=color, label=name, zorder=3)
            tops = list(ys)
            if name == 'LUT-GEMM' and cnt is tile:
                ax.bar(xs[1], build, w * 0.92, bottom=ys[1], color=LUT_BUILD, zorder=3,
                       label=f'LUT-GEMM: table build ({2 ** (v - 1)} entries)')
                tops[1] += build
                ax.text(xs[1] + w * 0.55, ys[1] + build / 2, f'+{build:,}\nbuild', ha='left', va='center',
                        fontsize=size - 1, color=INK_2)
            for x, top in zip(xs, tops):
                ax.text(x, top, f'{top:,}', ha='center', va='bottom', fontsize=size, color=INK)
        ax.set_xticks(range(len(OPS)))
        ax.set_xticklabels(OPS)
        ax.set_title(title, color=INK_2)
        ax.grid(axis='x', visible=False)
        ax.set_ylim(0, max(max(c) for c in cnt.values()) * 1.18 + (build * 0.2 if cnt is tile else 0))
        ax.tick_params(axis='x', length=0)
    ax_a.set_ylabel('operations')


if __name__ == '__main__':
    QW, V, BS, N = config(sys.argv[1:])
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.4))
    draw_bars(axes[0], axes[1], QW, V, BS, N)
    handles, labels = axes[1].get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, 1.0), ncol=3, handlelength=1.4)
    fig.text(0.995, -0.02,
             f'int{QW} weights × fp16 activations, v = {V}, bs = {BS}. MAC-GEMM: one multiply and one add per '
             f'weight (fp16 × fp16 or int{QW} × fp16 multiplier). LUT-GEMM: one read per weight bit-plane from a\n'
             f'sign-symmetric table of 2^(v−1) = {2 ** (V - 1)} entries, one fp16 add per read; the 2^b shift and the '
             'sign flip are not counted. Table build ≈ one add per entry, amortized over the N columns.',
             ha='right', va='top', fontsize=5.5, color=INK_2)
    fig.tight_layout(w_pad=1.5)
    save(fig, f'fig7_op_counts_int{QW}_fp16_v{V}_bs{BS}_n{N}')
