# Build README.md and tables-bs<bs>.md: MAC-GEMM vs LUT-GEMM cost, one table per quantization
# frame (wq, wa) and batch size, from the sweep snapshot in ../results/. Edit this script, not
# the .md files. Run with the system python3 (stdlib only): python3 make_tables.py
import csv
import datetime
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(os.path.dirname(HERE), 'results')
WQ = ['int1', 'ter', 'int2', 'int3', 'int4', 'int6', 'int8']  # ter = ternary {-1, 0, +1}
NO_MUL = ('int1', 'ter')  # a weight of +-1 (or 0) selects or negates the activation
WA = {'int8': 8, 'fp16': 16}  # LUT entry bits per batch row
VS = [4, 6, 7, 8]
BS = [1, 2, 4, 8]
F_GHZ = 0.5  # both sweeps ran at 500 MHz
CACTI_MIN_BYTES = 64
LUT_RE = r'(reg|sram)_lut_n(\d+)_w(\d+)_r(\d+)'
TODO = 'cmp00:~/isca26hw/micro26rcf/playground/todo/mac_lut_data_to_collect.md'

pe = {r['design']: r for r in csv.DictReader(open(f'{RES}/pe_sweep/pe_summary.csv'))}
# every buffer_sweep design is 16 bits wide; 1RW is the one-read-port table
buf = {int(r['N']): r for r in csv.DictReader(open(f'{RES}/buffer_sweep/compare_summary.csv'))
       if r['port'] == '1rw'}


def lut(kind, n, w, r):
    """(area um2, read-only power mW) of one N-entry, W-bit table read through r ports every cycle."""
    row = buf.get(n) if (w, r) == (16, 1) else None
    if kind == 'reg':
        # whole u_buf: flops, decode, read mux, clock gating. Its power was measured at
        # 80% read / 20% write, so there is no read-only number yet.
        return (float(row['syn_area_um2']) if row else None), None
    if row and row['cacti_area_um2']:
        # pJ x GHz = mW
        return float(row['cacti_area_um2']), float(row['cacti_static_mW']) + F_GHZ * float(row['cacti_rd_pJ'])
    return None, None


def unit(name):
    """(area um2, power mW) of one primitive; either is None when the snapshot has no number."""
    m = re.fullmatch(LUT_RE, name)
    if m:
        return lut(m[1], int(m[2]), int(m[3]), int(m[4]))
    r = pe.get(name)
    # logic-only u_core: these designs have no flops inside u_core
    return (float(r['logic_area_um2']), float(r['logic_power_mW'])) if r else (None, None)


def reads(wq):
    """LUT reads per v-slice: one per weight bit-plane; ternary indexes one table with all v trits."""
    return 1 if wq == 'ter' else int(wq[3:])


def entries(wq, v, symm):
    if wq == 'ter':
        need = 3 ** v // 2 if symm else 3 ** v
        return 1 << (need - 1).bit_length()  # smallest 2^k >= need
    return 2 ** (v - 1) if symm else 2 ** v


def methods(wq, wa, bs):
    """(row label, what it counts, v -> [(count, primitive)])"""
    q = reads(wq)
    w = WA[wa] * bs  # one entry holds bs partial sums
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
    for kind, shown in (('reg', 'reg'), ('sram', 'SRAM')):
        for org, copies, ports in (('dup', q, 1), ('multi-port', 1, q)):
            for sym, symm in (('pre-ignore', False), ('pre-ignore+symm', True)):
                rows.append((f'LUT {shown} {org}, {sym}',
                             f'{copies} × LUT[{size[symm]} × {w}b, {ports}R] + {q * bs} × fp16 add',
                             lambda v, c=copies, s=symm, t=f'{kind}_lut_n{{}}_w{w}_r{ports}':
                             [(c, t.format(entries(wq, v, s))), (q * bs, 'add_fp16')]))
    return rows


missing = {}  # (primitive, 'area' | 'power') -> labels of the rows that need it
used = set()


def cell(parts, label):
    area = power = 0.0
    for n, p in parts:
        used.add(p)
        a, w = unit(p)
        for metric, val in (('area', a), ('power', w)):
            if val is None:
                missing.setdefault((p, metric), set()).add(label)
        area = None if a is None or area is None else area + n * a
        power = None if w is None or power is None else power + n * w
    return f"{'#' if area is None else f'{area:,.0f}'} / {'#' if power is None else f'{power:.2f}'}"


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
        return 'Mixed-type multiplier', 'pe_sweep has only same-type multipliers (`mul_int4` is int4 × int4)'
    kind, n, w, r = m[1], int(m[2]), int(m[3]), int(m[4])
    family = f"{'Reg' if kind == 'reg' else 'SRAM'} LUT, {'1 read port' if r == 1 else 'wq read ports'}"
    if kind == 'sram' and n * w < 8 * CACTI_MIN_BYTES:
        return family, 'below the CACTI floor of 64 bytes'
    if r > 1:
        return family, 'no multi-read-port table was run'
    if w != 16 or n > max(buf):
        return family, f'only W = 16, N ≤ {max(buf)} tables were run'
    return family, 'no read-only power run (measured at 80% read / 20% write)'


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
        a, w = unit(p)
        if a is None and w is None:
            continue
        m = re.fullmatch(LUT_RE, p)
        src = (f'`{p}`, logic only' if not m else f'`buffer_n{m[2]}` (synthesized u_buf)' if m[1] == 'reg'
               else f'CACTI 1RW, N = {m[2]}: leakage + 500 MHz × E_read')
        lines.append(f"| `{p}` | {'#' if a is None else f'{a:,.1f}'} | {'#' if w is None else f'{w:.3f}'} | {src} |")
    return '\n'.join(lines)


today = datetime.date.today()
for bs in BS:
    tables = '\n\n'.join(f'## wq = {wq}, wa = {wa}\n\n{frame_table(wq, wa, bs)}' for wa in WA for wq in WQ)
    with open(os.path.join(HERE, f'tables-bs{bs}.md'), 'w') as f:
        f.write(f"""# 01 — MAC-GEMM vs LUT-GEMM cost, batch size {bs}

Generated {today} by `make_tables.py`. Cost model, missing data and notes:
[README.md](README.md). **Cell: area (µm²) / read-only power (mW)** at 500 MHz; `#` = no data
yet. LUT entries are {", ".join(f"{WA[wa] * bs} bits for wa = {wa}" for wa in WA)}.

{tables}
""")

links = ' · '.join(f'[bs = {bs}](tables-bs{bs}.md)' for bs in BS)
out = f"""# 01 — MAC-GEMM vs LUT-GEMM cost per quantization frame

Generated {today} by `make_tables.py` from [`../results/`](../results/) (the cmp00 sweep
snapshot; see [`../README.md`](../README.md)). Edit the script, not this file.

**Tables, one file per batch size: {links}.** Each file has one table per frame
(wq ∈ {{{", ".join(map(str, WQ))}}} × wa ∈ {{{", ".join(WA)}}}), one row per method and one
column per v. **Cell: area (µm²) / power (mW)** at 500 MHz, for hardware that consumes one
v-element slice of a dot product for every batch row each cycle. Power × 2 = energy per cycle in
pJ. **`#` = no data yet**, for area and power separately.

## Missing data

{missing_table()}

What to run to fill these: `{TODO}`.

## Methods and cost model

* **wq**: weight format: {", ".join(WQ)}. int-b = b-bit integer; **ter** = ternary
  {{−1, 0, +1}}. **wa**: activation format (int8 or fp16). **v**: vector length, the number of
  activations combined per step. **bs**: batch size ({", ".join(map(str, BS))}).
* **MAC-GEMM**: bs·v multipliers and bs·v adders (a batch of bs needs bs times the resources).
  * *fp16*: v × fp16 mul + v × fp16 add.
  * *opt*: v × (int-wq × wa) mul + v × fp16 add. The int → fp16 conversion that wa = int8
    needs is not counted; see
    [02-int-to-fp-converter-cost](../02-int-to-fp-converter-cost/README.md) for its size.
  * *int8*: v × int8 mul + v × int16 add.
  * **wq = int1 and ter: no multiplier in any MAC row**, only the adds. The weight just
    selects, negates or zeroes the activation, and that is not counted. So for these two,
    *fp16* and *opt* are the same row.
* **LUT-GEMM** (lookup table): the table holds the partial sums of v activations for every
  weight pattern. **Reads per slice:** int-b weights read once per bit-plane (b reads, b fp16
  adds; one for int1); ternary weights index one table with all v trits (1 read, 1 add).
  * *pre-ignore*: the cost of building the table is ignored. *pre-ignore+symm*: half the
    table is stored and the other half is a sign flip of it; the flip is ignored.
  * **Entries**: int-b: 2^v, or 2^v / 2 with symm. ter: the smallest 2^k ≥ 3^v, or ≥ ⌊3^v / 2⌋
    with symm.
  * *dup*: one table copy per read, one read port each. *multi-port*: one table with one read
    port per read. With one read (int1, ter) the two are the same.
  * *reg*: flip-flop register file (synthesized). *SRAM*: CACTI.
  * **Entry width**: 8 bits for wa = int8, 16 bits for wa = fp16, times bs: one entry holds the
    partial sums of all bs batch rows, so a batch makes entries bs times wider, keeps the
    number of tables and reads, and multiplies the fp16 adds by bs.

| LUT entries | {" | ".join(f"v = {v}" for v in VS)} |
|---|{"---|" * len(VS)}
{chr(10).join(f"| {name} | " + " | ".join(f"{entries(wq, v, s):,}" for v in VS) + " |"
              for name, wq, s in (("int-b, pre-ignore", "int1", False), ("int-b, pre-ignore+symm", "int1", True),
                                  ("ter, pre-ignore", "ter", False), ("ter, pre-ignore+symm", "ter", True)))}

* **Area** = Σ count × unit area. Adders and multipliers: logic-only area of `u_core` from
  pe_sweep. Reg LUT: the whole `u_buf` (flops, address decode, read mux, clock gating).
  SRAM LUT: CACTI area.
* **Power** = Σ count × unit power, every unit busy every cycle. **LUT power is read-only**:
  for SRAM, leakage + 500 MHz × E_read per read port; for reg, not measured yet (`#`).
* **Not counted:** table precompute, the sign flip, the 2^b weighting between bit-planes, and
  any int → fp conversion.

## Unit costs used

Only primitives with at least one number; the rest are in *Missing data*.

{unit_table()}

## Notes

1. **Reg LUT power is `#` everywhere.** The buffer sweep measured 80% reads / 20% writes; a
   LUT is read-only during the GEMM. When a read-only run is added, check the clock
   transition too: the flow's 5 ns setting inflates flip-flop power (on `buffer_n4`, 0.05 ns
   cut `u_buf` power from 0.375 to 0.153 mW; buffer REPORT note 2).
2. **SRAM read-only power** is a few percent under the 80/20 number the earlier version used
   (N = 32: 0.110 vs 0.114 mW; N = 256: 0.469 vs 0.482 mW), because CACTI's write energy is
   higher than its read energy.
3. **8-bit entries for wa = int8.** An exact partial sum of v int8 activations needs
   8 + ⌈log2 v⌉ bits (11 at v = 8), so 8-bit entries assume the partial sums are requantized.
   The adds stay fp16, as specified.
4. **MAC opt with wa = int8 excludes the converter**, as specified. It is not what made the
   pe_sweep MAC large: inside `mac_mulint8_addfp16` the converter's cells are 272 µm² of
   1,763 µm², and most of the rest is upsizing to close timing in one cycle
   ([02](../02-int-to-fp-converter-cost/README.md)).
5. **Ternary tables are large**: {", ".join(f"{entries('ter', v, False):,}" for v in VS)} entries
   at v = {", ".join(map(str, VS))} (half with symm), so most ternary LUT cells need tables
   beyond the {max(buf)}-entry sweep.
6. **fp16 units close timing at ~0 ps slack** (`mul_fp16` {pe['mul_fp16']['slack_ps']} ps,
   `add_fp16` {pe['add_fp16']['slack_ps']} ps), so their area includes upsizing.
"""

with open(os.path.join(HERE, 'README.md'), 'w') as f:
    f.write(out)
print(f'wrote README.md and {len(BS)} table files; {len(missing)} missing (primitive, metric) pairs')
