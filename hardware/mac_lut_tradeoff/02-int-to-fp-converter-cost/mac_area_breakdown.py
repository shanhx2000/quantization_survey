# Split the u_core cell area of pe_sweep MACs into multiplier / converter / adder / accumulator
# flops / unattributed glue, by instance name in the Genus gate netlist. Needs the full sweep
# copy (not in git), e.g. from hardware/:
#   python3 mac_lut_tradeoff/02-int-to-fp-converter-cost/mac_area_breakdown.py pe_sweep mac_mulint8_addfp16
import collections
import csv
import os
import re
import sys

root = sys.argv[1]
csv_path = f'{root}/pe_summary_v2.csv' if os.path.exists(f'{root}/pe_summary_v2.csv') else f'{root}/pe_summary.csv'
summary = {r['design']: r for r in csv.DictReader(open(csv_path))}
for design in sys.argv[2:]:
    run = f"{root}/{summary[design]['syn_run']}"
    area = {}  # library cell -> area of one instance
    for line in open(f'{run}/rpt/{design}.gates.rpt'):
        m = re.match(r'^(\S+)\s+(\d+)\s+([\d.]+)\s+tcbn', line)
        if m:
            area[m[1]] = float(m[3]) / int(m[2])
    modules, cur = {}, None  # module -> [(cell or submodule, instance)]
    for line in open(f'{run}/gate/{design}.v'):
        m = re.match(r'^module (\S+)\(', line)
        if m:
            cur = modules.setdefault(m[1], [])
            continue
        # flops are escaped identifiers: \acc_reg[14] (
        m = re.match(r'^\s+([A-Za-z]\w*)\s+\\?([\w\[\]]+)\s*\(', line)
        if cur is not None and m and m[1] not in ('module', 'input', 'output', 'wire', 'assign'):
            cur.append((m[1], m[2]))

    def total(mod):
        return sum(area[c] if c in area else total(c) for c, _ in modules.get(mod, []))

    core = next(k for k in modules if k.startswith('mac_core_'))
    groups = collections.Counter()
    for cell, inst in modules[core]:
        if inst.startswith(('u_mul', 'mul_')):
            key = 'mul'
        elif inst.startswith(('u_cvt', 'u_up', 'u_dn')):
            key = 'cvt'
        elif inst.startswith('u_add'):
            key = 'add'
        elif 'reg' in inst:
            key = 'acc flops'
        else:
            key = 'glue (renamed by Genus, crosses block boundaries)'
        groups[key] += area[cell] if cell in area else total(cell)
    s = summary[design]
    print(f"== {design}: sum {sum(groups.values()):.1f}, csv u_core {float(s['core_area_um2']):.1f} "
          f"(logic {float(s['logic_area_um2']):.1f}), slack {s['slack_ps']} ps, "
          f"conversion: {s['conversion'] or 'none'}")
    for k, v in groups.most_common():
        print(f'   {k:52s} {v:8.1f}')
