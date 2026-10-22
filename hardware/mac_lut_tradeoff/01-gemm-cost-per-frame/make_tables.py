# Build README.md: MAC-GEMM vs LUT-GEMM cost, one table per quantization frame (wq, wa),
# from the sweep snapshot in ../results/. Edit this script, not README.md.
# Run with the system python3 (stdlib only): python3 make_tables.py
import csv
import datetime
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(os.path.dirname(HERE), 'results')
WQ = [3, 4, 6, 8]
WA = ['int8', 'fp16']
VS = [4, 6, 7, 8]
F_GHZ = 0.5  # both sweeps ran at 500 MHz

pe = {r['design']: r for r in csv.DictReader(open(f'{RES}/pe_sweep/pe_summary.csv'))}
buf = {int(r['N']): r for r in csv.DictReader(open(f'{RES}/buffer_sweep/compare_summary.csv'))
       if r['port'] == '1rw'}
LUT_NS = sorted({2 ** v for v in VS} | {2 ** (v - 1) for v in VS})
PRIMS = (['mul_fp16', 'add_fp16', 'mul_int8', 'add_int16']
         + [f'mul_int{wq}x{wa}' for wa in WA for wq in WQ if (wq, wa) != (8, 'int8')]
         + [f'{k}_lut_n{n}' for k in ('reg', 'sram') for n in LUT_NS])


def unit(name):
    """(area um2, power mW) of one primitive, or None if the snapshot has no data for it."""
    if name.startswith(('reg_lut_n', 'sram_lut_n')):
        r = buf.get(int(name.rsplit('_n', 1)[1]))
        if name.startswith('reg') and r:
            # whole u_buf of the 1RW flip-flop buffer: flops, decode, read mux, clock gating
            return float(r['syn_area_um2']), float(r['syn_total_mW'])
        if name.startswith('sram') and r and r['cacti_area_um2']:
            return float(r['cacti_area_um2']), float(r['cacti_total_mW'])
        return None
    r = pe.get(name)
    # logic-only u_core: these designs have no flops inside u_core
    return (float(r['logic_area_um2']), float(r['logic_power_mW'])) if r else None


def methods(wq, wa):
    """(row label, what it counts, v -> [(count, primitive)])"""
    mul = 'mul_int8' if (wq, wa) == (8, 'int8') else f'mul_int{wq}x{wa}'
    rows = [('MAC fp16', 'v × fp16 mul + v × fp16 add', lambda v: [(v, 'mul_fp16'), (v, 'add_fp16')]),
            ('MAC opt', f'v × int{wq}×{wa} mul + v × fp16 add', lambda v: [(v, mul), (v, 'add_fp16')]),
            ('MAC int8', 'v × int8 mul + v × int16 add', lambda v: [(v, 'mul_int8'), (v, 'add_int16')])]
    for kind, shown in (('reg', 'reg'), ('sram', 'SRAM')):
        rows += [(f'LUT {shown}, pre-ignore', f'{wq} × LUT[2^v] read + {wq} × fp16 add',
                  lambda v, k=kind: [(wq, f'{k}_lut_n{2 ** v}'), (wq, 'add_fp16')]),
                 (f'LUT {shown}, pre-ignore+symm', f'{wq} × LUT[2^v/2] read + {wq} × fp16 add',
                  lambda v, k=kind: [(wq, f'{k}_lut_n{2 ** (v - 1)}'), (wq, 'add_fp16')])]
    return rows


missing = {}  # primitive -> {'methods', 'frames', 'vs'}


def cell(parts, label, frame, v):
    area = power = 0.0
    gaps = [p for _, p in parts if unit(p) is None]
    for p in gaps:
        use = missing.setdefault(p, {'methods': set(), 'frames': set(), 'vs': set()})
        use['methods'].add(label), use['frames'].add(frame), use['vs'].add(v)
    if gaps:
        return '#'
    for n, p in parts:
        a, w = unit(p)
        area, power = area + n * a, power + n * w
    return f'{area:,.0f} / {power:.2f}'


def frame_table(wq, wa):
    lines = ['| Method | Counts | ' + ' | '.join(f'v = {v}' for v in VS) + ' |',
             '|---|---|' + '---|' * len(VS)]
    for label, counts, parts in methods(wq, wa):
        cells = [cell(parts(v), label, (wq, wa), v) for v in VS]
        lines.append(f'| {label} | {counts} | ' + ' | '.join(cells) + ' |')
    return '\n'.join(lines)


def source(name):
    if name.startswith('reg_lut_n'):
        n = int(name.rsplit('_n', 1)[1])
        return f'`buffer_n{n}` (synthesized, 1RW)', buf[n]['syn_slack_ps'] if n in buf else ''
    if name.startswith('sram_lut_n'):
        return f'CACTI 1RW, N = {name.rsplit("_n", 1)[1]}', ''
    return f'`{name}`', pe[name]['slack_ps'] if name in pe else ''


def unit_table():
    lines = ['| Primitive | Area (µm²) | Power (mW) | Source | Slack (ps) |', '|---|---|---|---|---|']
    for p in PRIMS:
        u = unit(p)
        src, slack = source(p)
        lines.append(f'| `{p}` | ' + (f'{u[0]:,.1f} | {u[1]:.3f}' if u else '# | #')
                     + f' | {src} | {slack} |')
    return '\n'.join(lines)


def missing_table():
    lines = ['| Primitive | Needed by | Frames | v | Why it is missing |', '|---|---|---|---|---|']
    for p in PRIMS:
        if p not in missing:
            continue
        use = missing[p]
        frames = ('every frame' if len(use['frames']) == len(WQ) * len(WA)
                  else ', '.join(f'wq={wq} wa={wa}' for wq, wa in sorted(use['frames'])))
        vs = 'all' if len(use['vs']) == len(VS) else ', '.join(map(str, sorted(use['vs'])))
        why = ('CACTI does not model arrays under 64 bytes (N < 32 at 16 bits)' if p.startswith('sram')
               else 'pe_sweep has only same-type multipliers (`mul_int4` is int4 × int4)')
        lines.append(f'| `{p}` | {", ".join(sorted(use["methods"]))} | {frames} | {vs} | {why} |')
    return '\n'.join(lines)


def sram_read_only():
    # a LUT is only read; CACTI gives E_read, so read-only power = static + f * E_read
    parts = []
    for n in LUT_NS:
        r = buf.get(n)
        if r and r['cacti_area_um2']:
            ro = float(r['cacti_static_mW']) + F_GHZ * float(r['cacti_rd_pJ'])
            parts.append(f'N = {n}: {ro:.3f} vs {float(r["cacti_total_mW"]):.3f} mW')
    return '; '.join(parts)


tables = '\n\n'.join(f'### wq = int{wq}, wa = {wa}\n\n{frame_table(wq, wa)}' for wa in WA for wq in WQ)
conv = pe['mac_mulint8_addfp16']
conv_area = float(conv['logic_area_um2'])
split_area = unit('mul_int8')[0] + unit('add_fp16')[0]

out = f"""# 01 — MAC-GEMM vs LUT-GEMM cost per quantization frame

Generated {datetime.date.today()} by `make_tables.py` from [`../results/`](../results/) (the
cmp00 sweep snapshot; see [`../README.md`](../README.md)). Edit the script, not this file.

**Cell format: area (µm²) / power (mW)** at 500 MHz, for hardware that consumes one
v-element slice of a dot product every cycle. Power × 2 = energy per cycle in pJ.

## Missing data

`#` in a cell means at least one primitive has no number in the snapshot:

{missing_table()}

The script looks for the multipliers under the names in the first column, so a pe_sweep
design with that name fills the cells on the next run.

## Methods and cost model

* **wq**: weight bits (int: 3, 4, 6, 8). **wa**: activation format (int8 or fp16).
  **v**: vector length, the number of activations combined per step.
* **MAC-GEMM**: v multipliers and v adders.
  * *fp16*: v × fp16 mul + v × fp16 add. Same in every frame.
  * *opt*: v × (int-wq × wa) mul + v × fp16 add.
  * *int8*: v × int8 mul + v × int16 add. Same in every frame.
* **LUT-GEMM** (lookup table): the table holds the partial sums of v activations for every
  v-bit weight pattern; each of the wq weight bit-planes reads one entry, and wq fp16 adders
  combine them. Entries are 16 bits (fp16), matching the 16-bit buffer sweep.
  * *pre-ignore*: 2^v entries; the cost of building the table is ignored.
  * *pre-ignore+symm*: 2^v / 2 entries; the other half is a sign flip of the stored half,
    and the flip is ignored.
  * *reg*: the table is a flip-flop register file (`buffer_n<N>`, synthesized).
    *SRAM*: the table is a CACTI 1RW SRAM.

| v | 4 | 6 | 7 | 8 |
|---|---|---|---|---|
| LUT entries, pre-ignore (2^v) | 16 | 64 | 128 | 256 |
| LUT entries, pre-ignore+symm (2^v / 2) | 8 | 32 | 64 | 128 |

* **Area** = Σ count × unit area. Adders and multipliers: logic-only area of `u_core` from
  pe_sweep. Reg LUT: the whole `u_buf` (flops, address decode, read mux, clock gating).
  SRAM LUT: CACTI area.
* **Power** = Σ count × unit power, every unit doing one operation per cycle.
* **Not counted:** table precompute, the sign flip, the 2^b weighting between bit-planes, and
  any int → fp conversion.

## Tables

{tables}

## Unit costs used

{unit_table()}

## Notes

1. **LUT area counts wq separate tables.** The spec counts wq LUT reads, and each read is
   costed as one whole table. All wq bit-planes of a weight index the *same* activation
   table, so one table with wq read ports, or one table shared across output channels,
   would need less storage. The sweep has no multi-read-port buffer, so that case is not
   costed. The LUT rows are an upper bound on area and on flop power.
2. **Reg LUT power is an upper bound.** It was measured with 80% reads / 20% writes; a LUT
   is read-only during the GEMM, and read-only power was not measured. The flow's 5 ns
   clock transition also inflates flip-flop power: on `buffer_n4`, 0.05 ns cut `u_buf` power
   from 0.375 to 0.153 mW (buffer REPORT note 2).
3. **SRAM LUT power** uses the same 80/20 mix. Read-only (static + 500 MHz × E_read) is a
   little lower: {sram_read_only()}.
4. **Reg LUT at N = 256** (v = 8, pre-ignore) carries the logic-power step that the
   buffer report flags in its note 4. Treat that column with care.
5. **The LUT rows do not depend on wa** because the spec uses 16-bit entries and fp16 adds in
   both frames. With wa = int8, the entries could be integer partial sums (8 + ⌈log2 v⌉ bits)
   added in int16. That variant is not in the spec and is not costed.
6. **MAC opt with wa = int8** adds an integer product in fp16, which needs an int → fp16
   conversion that the spec does not count. In pe_sweep it is not free:
   `mac_mulint8_addfp16` has {conv_area:,.0f} µm² of logic against {split_area:,.0f} µm² for
   `mul_int8` + `add_fp16`, although part of that gap is upsizing to close timing in one
   cycle (pe REPORT note 2).
7. **fp16 units close timing at ~0 ps slack** (`mul_fp16` {pe['mul_fp16']['slack_ps']} ps,
   `add_fp16` {pe['add_fp16']['slack_ps']} ps), so their area includes upsizing.
"""

with open(os.path.join(HERE, 'README.md'), 'w') as f:
    f.write(out)
print(f'wrote {os.path.join(HERE, "README.md")}; missing primitives: {", ".join(missing) or "none"}')
