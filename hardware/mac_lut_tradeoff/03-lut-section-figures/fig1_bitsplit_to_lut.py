# Fig. 1: from bit-splitting MAC-GEMM to LUT-GEMM, on a toy tile: v = 2 activations,
# mu = 4-bit weights, N = 6 output columns. (a) the weights split into bit-planes; (b) the
# bit-serial GEMM forms one partial sum per (plane, column) and recomputes x0 + x1 every time
# both bits are set; (c) the 2^v distinct sums, precomputed once; (d) LUT-GEMM looks them up
# and shift-adds over the planes. Everything drawn is computed from W below.
# Usage: python3 fig1_bitsplit_to_lut.py   ->  fig1_bitsplit_to_lut.{pdf,png}
from matplotlib.patches import FancyArrowPatch, Rectangle

from figstyle import INK, INK_2, MUTED, NEUTRAL_FILL, SERIES, plt, save

V, MU = 2, 4
W = [[13, 7, 10, 15, 6, 9],   # weights that multiply x0
     [11, 7, 12, 13, 3, 14]]  # weights that multiply x1
N = len(W[0])
PLANES = list(range(MU - 1, -1, -1))  # b = 3 (MSB) at the top

# pattern (bit of w0, bit of w1) -> partial sum and fill
SUM = {(0, 0): '0', (1, 0): '$x_0$', (0, 1): '$x_1$', (1, 1): '$x_0{+}x_1$'}
FILL = {(0, 0): NEUTRAL_FILL, (1, 0): SERIES[0], (0, 1): SERIES[1], (1, 1): SERIES[2]}
ALPHA = {(0, 0): 1.0, (1, 0): 0.28, (0, 1): 0.28, (1, 1): 0.55}

pats = {(b, n): ((W[0][n] >> b) & 1, (W[1][n] >> b) & 1) for b in PLANES for n in range(N)}
repeats = sum(p == (1, 1) for p in pats.values())

fig, ax = plt.subplots(figsize=(7.0, 3.92))
ax.set_xlim(0, 100)
ax.set_ylim(0, 56)  # 1 unit = 0.07 in on both axes
ax.set_aspect('equal')
ax.axis('off')

CH = 2.7      # cell height
CW_BITS = 3.6  # cells holding "11"
CW_SUM = 5.4   # cells holding "x0+x1"


def cell(x, y, label, pat=None, w=CW_BITS, h=CH):
    if pat is not None:
        ax.add_patch(Rectangle((x, y), w, h, facecolor=FILL[pat], alpha=ALPHA[pat], edgecolor='none'))
    ax.add_patch(Rectangle((x, y), w, h, facecolor='none', edgecolor='white' if pat else MUTED, lw=0.8))
    ax.text(x + w / 2, y + h / 2, label, ha='center', va='center', fontsize=6.5, color=INK)


def grid(x0, y_top, label_of, cw, col_labels=False):
    """One cell per (plane, column), MSB plane on top; returns the bottom y."""
    for i, b in enumerate(PLANES):
        y = y_top - (i + 1) * CH
        ax.text(x0 - 0.6, y + CH / 2, f'$b{b}$', ha='right', va='center', fontsize=6.5, color=INK_2)
        for n in range(N):
            cell(x0 + n * cw, y, label_of(b, n), pats[(b, n)], w=cw)
    if col_labels:
        for n in range(N):
            ax.text(x0 + (n + 0.5) * cw, y_top + 0.4, f'$n{n}$', ha='center', va='bottom', fontsize=6, color=MUTED)
    return y_top - MU * CH


def text(x, y, s, size=6.5, color=INK_2, **kw):
    ax.text(x, y, s, fontsize=size, color=color, **kw)


def head(x, y, s):
    text(x, y, s, size=7, color=INK, weight='bold', va='top')


def arrow(p, q):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle='-|>', mutation_scale=7, color=INK_2, lw=0.9))


def bits(b, n):
    return f'{pats[(b, n)][0]}{pats[(b, n)][1]}'


# ---- row 1: (a) weights and bit-planes, (b) the partial sums ----------------------------
XA, XB = 5.0, 52.0
head(0.3, 55.5, '(a) Bit-splitting MAC-GEMM')
text(0.3, 52.6, f'activations $x = (x_0, x_1)$, $v$ = {V}; {MU}-bit weights, $N$ = {N} columns',
     size=6, va='top')
for k in range(V):
    text(XA - 0.6, 48.4 - (k + 0.5) * CH, f'$w_{{{k},n}}$', ha='right', va='center')
    for n in range(N):
        cell(XA + n * CW_BITS, 48.4 - (k + 1) * CH, str(W[k][n]))
text(XA, 42.4, f'$\\downarrow$ split into {MU} bit-planes', size=6, va='top')
G1 = 39.6
bottom_a = grid(XA, G1, bits, CW_BITS)
text(XA, bottom_a - 0.6, 'cell: bit of $w_{0,n}$, bit of $w_{1,n}$', size=6, color=MUTED, va='top')
text(XA + N * CW_BITS + 1.6, G1 - 2 * CH, 'per plane $b$ and\ncolumn $n$:\nAND, then add',
     size=6, va='center')
arrow((XA + N * CW_BITS + 13.4, G1 - 2 * CH), (XB - 3.6, G1 - 2 * CH))

head(XB - 3.6, 55.5, '(b) The partial sums repeat')
text(XB - 3.6, 52.6, 'each cell: $x_0 w^{(b)}_{0,n} + x_1 w^{(b)}_{1,n}$', size=6, va='top')
text(XB - 3.6, 48.6,
     f'{MU * N} partial sums, but only $2^v$ = {2 ** V} distinct values:\n'
     f'$x_0{{+}}x_1$ is added again in {repeats} cells', size=6.5, color=INK, va='top')
bottom_b = grid(XB, G1, lambda b, n: SUM[pats[(b, n)]], CW_SUM, col_labels=True)

# ---- row 2: (c) the LUT, (d) LUT-GEMM -----------------------------------------------------
XC, XD = 5.0, 41.0
head(0.3, 23.6, '(c) Precompute once: a LUT')
text(XC + 1.8, 19.4, 'index', size=6, color=MUTED, ha='center', va='bottom')
text(XC + 3.6 + 3.3, 19.4, 'entry', size=6, color=MUTED, ha='center', va='bottom')
for i, p in enumerate([(0, 0), (0, 1), (1, 0), (1, 1)]):
    y = 19.0 - (i + 1) * CH
    cell(XC, y, f'{p[0]}{p[1]}', p)
    cell(XC + CW_BITS, y, SUM[p], p, w=6.6)
text(XC + 11.6, 19.0 - 2 * CH, f'$2^v$ = {2 ** V} entries,\nbuilt with 1 add,\nread by all {MU * N}\ncells',
     size=6.5, color=INK, va='center')
arrow((XC + 24.0, 19.0 - 2 * CH), (XD - 3.6, 19.0 - 2 * CH))

head(XD - 3.6, 23.6, '(d) LUT-GEMM')
text(XD - 3.6, 20.8, 'each cell is now an index into the LUT', size=6, va='top')
G2 = 17.4
bottom_d = grid(XD, G2, bits, CW_BITS)
for n in range(N):
    arrow((XD + (n + 0.5) * CW_BITS, bottom_d - 0.1), (XD + (n + 0.5) * CW_BITS, bottom_d - 1.3))
    cell(XD + n * CW_BITS, bottom_d - 1.4 - CH, f'$y_{n}$')
text(XD + N * CW_BITS + 3.0, G2 - 2 * CH,
     r'$y_n = \sum_b \, 2^b \cdot \mathrm{LUT}[\,w^{(b)}_{0,n} w^{(b)}_{1,n}\,]$' '\n\n'
     f'{MU * N} lookups and shift-adds:\nno multiplies, no repeated sums',
     size=6.5, color=INK, va='center')

# (b) -> (c): the distinct values of (b) become the LUT
arrow((XB + 1.0, bottom_b - 0.6), (XC + 10.6, 19.6))
text(38.5, 27.6, 'keep the distinct sums', size=6, ha='center', va='center')

save(fig, 'fig1_bitsplit_to_lut')
