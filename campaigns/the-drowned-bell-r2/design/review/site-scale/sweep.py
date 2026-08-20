import json, subprocess, os, sys, shutil
sys.path.insert(0, '.')
import alloc
P = '../content/campaigns/the-drowned-bell-r2/design/programs'
prog = json.load(open(P + '/map.json'))
zones = {z['id']: z for z in json.load(open(P + '/zones.json'))['zones']}
SYM = {'z0/barrow_shore': 'z0-barrow-shore', 'z1/cliff_road': 'z1-cliff-road',
       'z2/gate_ward': 'z2-gate-ward', 'z3/drowned_ward': 'z3-drowned-ward',
       'z4/chapel_ward': 'z4-chapel-ward', 'z5/keep': 'z5-hall-keep',
       'z6/cistern_deep': 'z6-cistern-deep', 'z7/zone': 'z7-bell-tower'}
B = os.path.abspath('target/release/delve-grammar')
TMP = 'sweepout'
res = {}
for rock in range(70, 141):
    a = alloc.allocate(prog, [rock, 44, 80 + rock], {'rock_run': rock})
    row = {}
    for sym, (org, size) in a.boxes.items():
        zid = SYM[sym]
        z = zones[zid]
        r = '%dx%dx%d' % tuple(size)
        shutil.rmtree(TMP, ignore_errors=True)
        os.makedirs(TMP)
        p = subprocess.run([B, 'expand', '--file', P + '/' + z['program'],
                            '--region', r, '--seed', str(z['seed']),
                            '--out', TMP, '--id', zid + '-s'],
                           capture_output=True, text=True)
        txt = (p.stdout + p.stderr).strip()
        row[zid] = {'box': list(size), 'origin': list(org), 'ok': p.returncode == 0,
                    'message': (txt.splitlines()[0] if txt else '')}
    res[str(rock)] = row
    print(rock, ''.join('+' if row[z]['ok'] else '.' for z in sorted(row)), flush=True)
shutil.rmtree(TMP, ignore_errors=True)
json.dump(res, open('sweep.json', 'w'), indent=1, sort_keys=True)
