# Shared style for the LUT-section figures: print (light) palette, ink and rcParams.
# Categorical slots in fixed order, validated for this surface (dataviz validate_palette.js,
# --surface #ffffff: all checks pass; slot 3 is under 3:1 contrast, so its marks carry labels).
import os
import sys

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), '01-gemm-cost-per-frame'))

SERIES = ['#2a78d6', '#eb6834', '#1baf7a']  # blue, orange, aqua
SURFACE = '#ffffff'
INK = '#0b0b0b'
INK_2 = '#52514e'
MUTED = '#898781'
GRID = '#e1e0d9'
BASELINE = '#c3c2b7'
NEUTRAL_FILL = '#f0efec'  # "nothing here" cells

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans'],
    'font.size': 7,
    'axes.titlesize': 7,
    'axes.labelsize': 7,
    'xtick.labelsize': 6.5,
    'ytick.labelsize': 6.5,
    'legend.fontsize': 6.5,
    'axes.edgecolor': BASELINE,
    'axes.labelcolor': INK_2,
    'axes.titlecolor': INK,
    'xtick.color': MUTED,
    'ytick.color': MUTED,
    'xtick.labelcolor': INK_2,
    'ytick.labelcolor': INK_2,
    'axes.grid': True,
    'grid.color': GRID,
    'grid.linewidth': 0.5,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.facecolor': SURFACE,
    'figure.facecolor': SURFACE,
    'lines.linewidth': 1.5,
    'lines.markersize': 4,
    'legend.frameon': False,
    'pdf.fonttype': 42,  # embed TrueType, so Overleaf/ACM checks see real fonts
    'savefig.dpi': 300,
})


def save(fig, name):
    """Write <name>.pdf (for LaTeX) and <name>.png (for preview) next to the scripts."""
    for ext in ('pdf', 'png'):
        fig.savefig(os.path.join(HERE, f'{name}.{ext}'), bbox_inches='tight', pad_inches=0.02)
    print(f'wrote {name}.pdf, {name}.png')
