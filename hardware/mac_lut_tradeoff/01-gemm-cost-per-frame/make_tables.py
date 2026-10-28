# Build README.md and tables-bs<bs>.md: MAC-GEMM vs LUT-GEMM cost, one table per quantization
# frame (wq, wa) and batch size, from the sweep snapshot in ../results/. Edit this script, not
# the .md files. Run with the system python3 (stdlib only): python3 make_tables.py
import csv
import datetime
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(os.path.dirname(HERE), 'results')
WQ = ['binary', 'ter', 'int2', 'int3', 'int4', 'int6', 'int8']  # binary {-1, +1}, ternary {-1, 0, +1}
NO_MUL = ('binary', 'ter')  # a weight of +-1 (or 0) selects or negates the activation
WA = ['int8', 'fp16']
VS = [4, 6, 7, 8]
BS = [1, 2, 4, 8]
F_GHZ = 0.5  # both sweeps ran at 500 MHz
TER_REG_MAX_V = 6  # owner, 2026-10-22: ternary register-file tables only up to v = 6
LUT_RE = r'(reg|sram)_lut_n(\d+)_w(\d+)_r(\d+)'
LUT_ORG = r'1rw|1w\d+r'  # one read port, or one write + R read ports; other port types are 80/20-only
STATUS = '../results/todo/mac_lut_status.md'
TOO_LARGE = {(1024, 88), (1024, 128)}  # (N, W) skipped by the owner's size limit (2026-10-23)

# MAC units from the rebuilt pe sweep (cmp00, 2026-10-23: all at 0.1 ns clock transition, the
# owner's MAC precision and op_{a}x{b}_{out} names), looked up by their old names.
pe = {r['legacy_name']: r for r in csv.DictReader(open(f'{RES}/pe_sweep_v2/pe_summary_v2.csv'))}
# Tables from the revised buffer results: register files at 0.1 ns clock transition and CACTI
# SRAM at 300 K, both with power in activity corners. A LUT is read-only, so its power is the
# read-only corner (`ro_total_mW`: every read port reads every cycle, the write port idle; for
# register files, u_buf plus the input nets into it, the owner's boundary). The older
# lut_buffer_costs.csv overstated register-file read-only power 2-4x and is not used.
reg, sram = {}, {}  # (N, W bits, read ports) -> row of buffer_costs_v2.csv
for r in csv.DictReader(open(f'{RES}/buffer_sweep/buffer_costs_v2.csv')):
    if not re.fullmatch(LUT_ORG, r['org']):
        continue
    key = (int(r['N']), int(r['W']), int(r['R']))
    if r['model'] == 'sram':
        sram[key] = r
    elif r['status'] == 'ok':
        reg[key] = r


def lut(kind, n, w, r):
    """(area um2, read-only power mW, area bound?, power bound?, source) of one N-entry, W-bit
    table read through r ports every cycle; area and power are None when there is no data."""
    key = (n, w, r)
    if kind == 'reg':
        row = reg.get(key)
        if not row:
            return None, None, False, False, ''
        return (float(row['area_um2']), float(row['ro_total_mW']), False, False,
                f"`{row['design']}`, {row['clk_transition_ns']} ns clock transition")
    row, bound = sram.get(key), False
    modelled = sorted(m for (m, ww, rr), s in sram.items() if (ww, rr) == (w, r) and s['area_um2'])
    if (not row or not row['area_um2']) and modelled and n < modelled[0]:
        # below what CACTI can model (under 64 bytes, or N = 8, 16): the smallest modelled table
        # of the same width and ports stands in, as an upper bound
        row, bound = sram[(modelled[0], w, r)], True
    elif not row or not row['area_um2']:
        return None, None, False, False, ''
    src = f"CACTI {float(row['temperature_K']):.0f} K, {w // 8} B/entry" + (f"; N = {row['N']} stands in" if bound else '')
    return float(row['area_um2']), float(row['ro_total_mW']), bound, bound, src


def unit(name):
    """(area um2, power mW, area bound?, power bound?, source) of one primitive."""
    m = re.fullmatch(LUT_RE, name)
    if m:
        return lut(m[1], int(m[2]), int(m[3]), int(m[4]))
    r = pe.get(name)
    # logic-only u_core: these designs have no flops inside u_core
    if not r:
        return None, None, False, False, ''
    return float(r['logic_area_um2']), float(r['logic_power_mW']), False, False, f"`{r['design']}`, logic only"


def reads(wq):
    """LUT reads per v-slice: one per weight bit-plane; binary has one plane, and ternary indexes
    one table with all v trits."""
    return 1 if wq in NO_MUL else int(wq[3:])


def entries(wq, v, symm):
    if wq == 'ter':
        need = 3 ** v // 2 if symm else 3 ** v
        return 1 << (need - 1).bit_length()  # smallest 2^k >= need
    return 2 ** (v - 1) if symm else 2 ** v


def entry_bits(wa, v):
    """Bits per batch row in one LUT entry: fp16, or the exact sum of v int8 activations."""
    return 16 if wa == 'fp16' else 8 + (v - 1).bit_length()  # 8 + ceil(log2 v)


def sram_bits(w):
    return 8 * -(-w // 8)  # CACTI sizes entries in whole bytes


def lut_parts(wq, wa, bs, v, kind, copies, ports, symm):
    if kind == 'reg' and wq == 'ter' and v > TER_REG_MAX_V:
        return None  # not costed
    w = bs * entry_bits(wa, v)  # one entry holds bs partial sums
    if kind == 'sram':
        w = sram_bits(w)
    return [(copies, f'{kind}_lut_n{entries(wq, v, symm)}_w{w}_r{ports}'), (reads(wq) * bs, 'add_fp16')]


def methods(wq, wa, bs):
    """(row label, what it counts, v -> [(count, primitive)] or None when not costed)"""
    q = reads(wq)
    k = '' if bs == 1 else f'{bs}·'

    def mac(label, mul, add, mul_text, add_text):
        if wq in NO_MUL:
            return label, f'{k}v × {add_text} add', lambda v: [(bs * v, add)]
        return (label, f'{k}v × {mul_text} mul + {k}v × {add_text} add',
                lambda v: [(bs * v, mul), (bs * v, add)])

    opt = 'mul_int8' if (wq, wa) == ('int8', 'int8') else f'mul_{wq}x{wa}'
    rows = [mac('MAC fp16', 'mul_fp16', 'add_fp16', 'fp16', 'fp16'),
            mac('MAC opt', opt, 'add_fp16', f'{wq}×{wa}', 'fp16'),
            mac('MAC int8', 'mul_int8', 'add_int16', 'int8', 'int16')]
    size = {False: '2^⌈log2 3^v⌉', True: '2^⌈log2 ⌊3^v/2⌋⌉'} if wq == 'ter' else {False: '2^v', True: '2^v/2'}
    width = f'{k}16b' if wa == 'fp16' else f'{k}(8+⌈log2 v⌉)b'
    for kind, shown in (('reg', 'reg'), ('sram', 'SRAM')):
        for org, copies, ports in (('dup', q, 1), ('multi-port', 1, q)):
            for sym, symm in (('pre-ignore', False), ('pre-ignore+symm', True)):
                rows.append((f'LUT {shown} {org}, {sym}',
                             f'{copies} × LUT[{size[symm]} × {width}, {ports}R] + {q * bs} × fp16 add',
                             lambda v, kd=kind, c=copies, r=ports, s=symm:
                             lut_parts(wq, wa, bs, v, kd, c, r, s)))
    return rows


missing = {}  # (primitive, 'area' | 'power') -> labels of the rows that need it
used = set()


def fmt(val, spec, bound):
    return '#' if val is None else f'{val:{spec}}' + ('*' if bound else '')


def cost(parts, label=''):
    """(area um2, power mW, area bound?, power bound?) of a list of (count, primitive); area or
    power is None when a primitive has no number."""
    area = power = 0.0
    abound = pbound = False
    for n, p in parts:
        used.add(p)
        a, w, ab, pb, _ = unit(p)
        abound, pbound = abound or ab, pbound or pb
        for metric, val in (('area', a), ('power', w)):
            if val is None:
                missing.setdefault((p, metric), set()).add(label)
        area = None if a is None or area is None else area + n * a
        power = None if w is None or power is None else power + n * w
    return area, power, abound, pbound


def cell(parts, label):
    if parts is None:
        return '—'
    area, power, abound, pbound = cost(parts, label)
    return f"{fmt(area, ',.0f', abound)} / {fmt(power, '.2f', pbound)}"


def frame_table(wq, wa, bs):
    lines = ['| Method | Counts | ' + ' | '.join(f'v = {v}' for v in VS) + ' |',
             '|---|---|' + '---|' * len(VS)]
    for label, counts, parts in methods(wq, wa, bs):
        lines.append(f'| {label} | {counts} | ' + ' | '.join(cell(parts(v), label) for v in VS) + ' |')
    return '\n'.join(lines)


def reason(p):
    """(data family, why it is missing) for one missing primitive."""
    m = re.fullmatch(LUT_RE, p)
    if not m:
        return 'Multiplier or adder', 'not in pe_sweep_v2'
    family = f"{'Reg' if m[1] == 'reg' else 'SRAM'} LUT, {'1 read port' if m[4] == '1' else 'wq read ports'}"
    if m[1] == 'sram':
        return family, 'not in the CACTI grid'
    if (int(m[2]), int(m[3])) in TOO_LARGE:
        return family, f'skipped as too large by the owner; model estimate in [`mac_lut_status.md`]({STATUS})'
    return family, 'not queued (multi-port register files were run at W = 10, 11, 16 only)'


def configs(prims):
    if not re.fullmatch(LUT_RE, prims[0]):
        return ', '.join(f'`{p}`' for p in sorted(prims))
    by_w = {}
    for p in prims:
        _, n, w, r = re.fullmatch(LUT_RE, p).groups()
        by_w.setdefault(int(w), (set(), set()))
        by_w[int(w)][0].add(int(n)), by_w[int(w)][1].add(int(r))
    out = []
    for w, (ns, rs) in sorted(by_w.items()):
        ports = '' if rs == {1} else f', R = {"/".join(map(str, sorted(rs)))}'
        out.append(f'W = {w}: N = {", ".join(map(str, sorted(ns)))}{ports}')
    return '<br>'.join(out)


def missing_table():
    if not missing:
        return 'Nothing: every cell has a number.'
    groups = {}
    for p in sorted({p for p, _ in missing}):
        metrics = ' + '.join(m for m in ('area', 'power') if (p, m) in missing)
        groups.setdefault(reason(p) + (metrics,), []).append(p)
    lines = ['| Data | Missing | Configurations | Why |', '|---|---|---|---|']
    for (family, why, metrics), prims in sorted(groups.items()):
        lines.append(f'| {family} | {metrics} | {configs(prims)} | {why} |')
    return '\n'.join(lines)


def unit_table():
    def order(p):
        m = re.fullmatch(LUT_RE, p)
        return (1, m[1], int(m[3]), int(m[4]), int(m[2])) if m else (0, p)
    lines = ['| Primitive | Area (µm²) | Power (mW) | Source |', '|---|---|---|---|']
    for p in sorted(used, key=order):
        a, w, ab, pb, src = unit(p)
        if a is None and w is None:
            continue
        lines.append(f"| `{p}` | {fmt(a, ',.1f', ab)} | {fmt(w, '.3f', pb)} | {src} |")
    return '\n'.join(lines)


def span(vals, spec='.2f'):
    return f'{min(vals):{spec}}–{max(vals):{spec}}'


# multi-port vs copies: one table with R read ports / R single-port tables, same N and W
def vs_copies(tables, col):
    return [float(tables[k][col]) / (k[2] * float(tables[(k[0], k[1], 1)][col])) for k in tables
            if k[2] > 1 and (k[0], k[1], 1) in tables and tables[k][col] and tables[(k[0], k[1], 1)][col]]


reg_mp, reg_mp_power = vs_copies(reg, 'area_um2'), vs_copies(reg, 'ro_total_mW')
sram_mp_area, sram_mp_power = vs_copies(sram, 'area_um2'), vs_copies(sram, 'ro_total_mW')
pe_ct = sorted({pe[d]['clk_transition_ns'] for d in ('add_fp16', 'mul_fp16', 'mul_int8', 'add_int16')})
reg_ct = sorted({r['clk_transition_ns'] for r in reg.values()})
sram_k = sorted({f"{float(r['temperature_K']):.0f}" for r in sram.values()})
cvt = [float(pe[f'cvt_int{i}_fp16']['logic_area_um2']) for i in (10, 11, 12, 14, 16) if f'cvt_int{i}_fp16' in pe]
cvt_rtl = [float(pe[f'cvt_int{i}_fp16_rtl']['logic_area_um2']) for i in (10, 11, 12) if f'cvt_int{i}_fp16_rtl' in pe]

today = datetime.date.today()
LEGEND = ('`#` = no data yet. `*` = upper bound: an SRAM table CACTI cannot model (under 64 bytes, '
          'or N = 8, 16), costed as the smallest modelled table of the same width and ports. '
          f'`—` = not costed: ternary register-file tables above v = {TER_REG_MAX_V}.')
pages = {}  # file name -> text; written only when run as a script, so figures can import this
for bs in BS:
    tables = '\n\n'.join(f'## wq = {wq}, wa = {wa}\n\n{frame_table(wq, wa, bs)}' for wa in WA for wq in WQ)
    pages[f'tables-bs{bs}.md'] = (f"""# 01 — MAC-GEMM vs LUT-GEMM cost, batch size {bs}

Generated {today} by `make_tables.py`. Cost model, missing data and notes:
[README.md](README.md). **Cell: area (µm²) / read-only power (mW)** at 500 MHz. {LEGEND}
LUT entries per batch row: 16 bits for wa = fp16, 8 + ⌈log2 v⌉ bits for wa = int8; × {bs}.

{tables}
""")

links =' · '.join(f'[bs = {bs}](tables-bs{bs}.md)' for bs in BS)
out = f"""# 01 — MAC-GEMM vs LUT-GEMM cost per quantization frame

Generated {today} by `make_tables.py` from [`../results/`](../results/) (the cmp00 sweep
snapshot; see [`../README.md`](../README.md)). Edit the script, not this file.

**Tables, one file per batch size: {links}.** Each file has one table per frame
(wq ∈ {{{", ".join(WQ)}}} × wa ∈ {{{", ".join(WA)}}}), one row per method and one column per
v. **Cell: area (µm²) / power (mW)** at 500 MHz, for hardware that consumes one v-element
slice of a dot product for every batch row each cycle. Power × 2 = energy per cycle in pJ.
{LEGEND} `#` and `*` apply to area and power separately.

## Missing data

{missing_table()}

The data is being collected on cmp00; the snapshot of its plan and status is in
[`../results/todo/`](../results/todo/).

## Methods and cost model

* **wq**: weight format: {", ".join(WQ)}. binary = 1-bit weights {{−1, +1}}; int-b = b-bit integer; **ter** = ternary
  {{−1, 0, +1}}. **wa**: activation format (int8 or fp16). **v**: vector length, the number of
  activations combined per step. **bs**: batch size ({", ".join(map(str, BS))}).
* **MAC-GEMM**: bs·v multipliers and bs·v adders (a batch of bs needs bs times the resources).
  * *fp16*: v × fp16 mul + v × fp16 add.
  * *opt*: v × (int-wq × wa) mul + v × fp16 add. int × fp16 multipliers output fp16. The
    int → fp16 conversion that wa = int8 needs is not counted (note 6).
  * *int8*: v × int8 mul + v × int16 add.
  * **wq = binary and ter: no multiplier in any MAC row**, only the adds. The weight just
    selects, negates or zeroes the activation, and that is not counted. So for these two,
    *fp16* and *opt* are the same row.
* **LUT-GEMM** (lookup table): the table holds the partial sums of v activations for every
  weight pattern. **Reads per slice:** int-b weights read once per bit-plane (b reads, b fp16
  adds); binary weights read once; ternary weights index one table with all v trits (1 read, 1 add).
  * *pre-ignore*: the cost of building the table is ignored. *pre-ignore+symm*: half the
    table is stored and the other half is a sign flip of it; the flip is ignored.
  * **Entries**: int-b: 2^v, or 2^v / 2 with symm. ter: the smallest 2^k ≥ 3^v, or ≥ ⌊3^v / 2⌋
    with symm.
  * *dup*: one table copy per read, one read port each. *multi-port*: one table with one read
    port per read (plus one write port). With one read (binary, ter) the two are the same.
  * **Entry width** per batch row: 16 bits for wa = fp16; 8 + ⌈log2 v⌉ bits for wa = int8,
    which holds the exact sum of v int8 activations
    ({", ".join(f"{entry_bits('int8', v)} bits at v = {v}" for v in VS)}). Times bs: one entry
    holds the partial sums of all bs batch rows, so a batch makes entries bs times wider, keeps
    the number of tables and reads, and multiplies the fp16 adds by bs.
  * *reg*: flip-flop register file (synthesized) at the exact entry width. Ternary
    register-file tables are costed only up to v = {TER_REG_MAX_V} (`—` above).
  * *SRAM*: CACTI, which sizes entries in whole bytes, so widths round up
    ({", ".join(sorted({f"{w} → {sram_bits(w)}" for w in (bs * entry_bits('int8', v) for bs in BS for v in VS)
                        if sram_bits(w) != w}, key=lambda s: int(s.split()[0])))} bits).

| LUT entries | {" | ".join(f"v = {v}" for v in VS)} |
|---|{"---|" * len(VS)}
{chr(10).join(f"| {name} | " + " | ".join(f"{entries(wq, v, s):,}" for v in VS) + " |"
              for name, wq, s in (("binary / int-b, pre-ignore", "int2", False), ("binary / int-b, pre-ignore+symm", "int2", True),
                                  ("ter, pre-ignore", "ter", False), ("ter, pre-ignore+symm", "ter", True)))}

* **Area** = Σ count × unit area. Adders, multipliers: logic-only area of `u_core` from
  pe_sweep_v2. Register file: the whole `u_buf` (flops, address decode, read muxes, clock gating).
  SRAM: CACTI area.
* **Power** = Σ count × unit power, every unit busy every cycle. **LUT power is read-only**,
  the read-only corner of `buffer_costs_v2.csv`: every read port reads every cycle, the write
  port is idle with its data and address held. Register files: a power-only Genus
  re-analysis of the {"/".join(reg_ct)} ns netlist, `u_buf` plus the input nets that fan out
  into it. SRAM: CACTI at
  {"/".join(sram_k)} K, leakage + R × 500 MHz × E_read.
* **Not counted:** table precompute, the sign flip, the 2^b weighting between bit-planes, and
  any int → fp conversion.

## Unit costs used

Only primitives with at least one number; the rest are in *Missing data*.

{unit_table()}

## Notes

1. **LUT numbers are the revised (2026-10-23) results.** The earlier read-only register-file
   runs left the idle write port's data toggling every cycle and overstated read-only power
   2–4×; they are no longer used. CACTI moved from 360 K to {"/".join(sram_k)} K (the owner's
   choice, matched to the synthesis library's 25 °C): same area and access energy, 0.31–0.35×
   the leakage. Register-file power counts the input nets that fan out into the table at every
   size (the owner's boundary); in the read-only corner only the address nets toggle.
   `buffer_n512_w128` (ternary, v = 6, sign-symmetric, w_a = fp16, bs = 8) is the synthesized
   value, which carries ≈ 11,900 high-fanout buffers that its neighbours do not: 1.13× the
   area and 1.24× the read-only power of the width model. Keep it, use the model, or rerun
   it without that step: the owner's decision, open on cmp00.
2. **One clock transition throughout.** Every unit here is a {"/".join(pe_ct)} ns run
   (`pe_sweep_v2`), like the register files ({"/".join(reg_ct)} ns). The rebuild also changed
   MAC precision and names, which do not touch the add and multiply units these rows use.
3. **CACTI cannot model N = 8 or 16 at any width** ("no valid data array organizations
   found"), nor tables under 64 bytes. Those cells use the smallest modelled table (`*`).
4. **Multi-port vs copies.** In CACTI, one table with R read ports has {span(sram_mp_area)}×
   the area of R single-port copies ({len(sram_mp_area)} cases) and {span(sram_mp_power)}× the
   read-only power. For register files it is the other way round: {span(reg_mp)}× the area and
   {span(reg_mp_power)}× the read-only power of R copies ({len(reg_mp)} cases), because the
   flip-flops are shared and only the read muxes are replicated.
5. **wa = int8 entries are exact** (8 + ⌈log2 v⌉ bits), so no partial sum overflows. The adds
   stay fp16, as specified.
6. **The converter MAC opt leaves out is small.** A standalone `CW_fp_i2flt` → fp16 is
   {span(cvt, '.0f')} µm² of logic for the int-wq × int8 products (10 to 16 bits), and an
   exact RTL converter {span(cvt_rtl, '.0f')} µm² where no rounding is needed (≤ 12 bits).
   See [02](../02-int-to-fp-converter-cost/README.md).
7. **`mul_int2xfp16` is only {float(pe['mul_int2xfp16']['logic_area_um2']):.0f} µm²**: every int2
   value converts to fp16 with an all-zero mantissa, so Genus removes the significand
   multiplier and only sign and exponent logic remain. From int3 up there is a real multiplier.
8. **Ternary tables are large**: {", ".join(f"{entries('ter', v, False):,}" for v in VS)} entries
   at v = {", ".join(map(str, VS))} (half with symm). Register files are costed only up to
   v = {TER_REG_MAX_V} ({entries('ter', TER_REG_MAX_V, False):,} entries); SRAM at every v.
9. **fp16 units close timing at ~0 ps slack** at 2 ns (`mul_fp16` {pe['mul_fp16']['slack_ps']} ps,
   `add_fp16` {pe['add_fp16']['slack_ps']} ps), so their area includes upsizing.
"""

pages['README.md'] = out

if __name__ == '__main__':
    for name, text in pages.items():
        with open(os.path.join(HERE, name), 'w') as f:
            f.write(text)
    print(f'wrote {", ".join(pages)}; {len(missing)} missing (primitive, metric) pairs')
