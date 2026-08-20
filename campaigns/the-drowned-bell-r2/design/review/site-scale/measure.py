"""Read the expanded tile sets and write a compact measured record."""
import json, os, sys
import nbt

OUT = sys.argv[1]
ENGINE_REV = sys.argv[2]

here = os.path.dirname(os.path.abspath(__file__))
outdir = os.path.join(here, 'out')

def load_zone(base):
    man = json.load(open(os.path.join(outdir, base + '.json')))
    if 'structure_set' in man:
        ss = man['structure_set']
        parts = ss['parts']
        sx, sy, sz = ss['size']
    else:
        st = man['structure']
        sx, sy, sz = st['size']
        parts = [{'file': st['file'], 'offset': [0, 0, 0]}]
    filled = [[[False] * sz for _ in range(sy)] for _ in range(sx)]
    for part in parts:
        d = nbt.load(os.path.join(outdir, part['file']))
        pal = [p['Name'] for p in d['palette']]
        ox, oy, oz = part['offset']
        for b in d['blocks']:
            name = pal[b['state']]
            if name == 'minecraft:air':
                continue
            x, y, z = b['pos']
            filled[x + ox][y + oy][z + oz] = True
    return (sx, sy, sz), filled, man

def rows(grid):
    return [''.join('#' if c else '.' for c in r) for r in grid]

rec = {'engine_revision': ENGINE_REV, 'zones': {}}
for base in sorted(f[:-5] for f in os.listdir(outdir)
                   if f.endswith('.json') and not f.endswith('.report.json')):
    (sx, sy, sz), filled, man = load_zone(base)
    rep = json.load(open(os.path.join(outdir, base + '.report.json')))
    # plan mask: any filled cell in the column, indexed [x][z]
    plan = [[any(filled[x][y][z] for y in range(sy)) for z in range(sz)]
            for x in range(sx)]
    # the x-slice with the most floor in it -- a cell of air standing on a
    # solid cell. Chosen by count so no slice is picked by eye, and chosen on
    # floor rather than on mass so it cuts an interior and not an outer wall.
    counts = [sum(1 for y in range(1, sy) for z in range(sz)
                  if not filled[x][y][z] and filled[x][y - 1][z])
              for x in range(sx)]
    cut = counts.index(max(counts))
    # long section at that x, indexed [y][z]
    sect = [[filled[cut][y][z] for z in range(sz)] for y in range(sy)]
    # top of the built mass per z, over all x (the elevation the site reads as)
    prof = []
    for z in range(sz):
        h = 0
        for y in range(sy):
            if any(filled[x][y][z] for x in range(sx)):
                h = y + 1
        prof.append(h)
    # a plan at every height an anchor stands at: the levels where the zone
    # says play happens, so the set is chosen by the zone and not by the drawer
    # the storeys a DECLARED SPACE stands at -- a place the contract says a
    # body is, rather than a stair tread or a piece of scenery
    ys = sorted({a['pos'][1] for a in man.get('anchors', {}).values()
                 if str(a.get('resolves_to', '')).startswith('space:')})
    levels, floors, stand_at, overs = {}, {}, {}, {}
    for y in ys:
        levels[str(y)] = rows([[filled[x][y][z] for z in range(sz)]
                               for x in range(sx)])
        fl = [[(not filled[x][y][z]) and y > 0 and filled[x][y - 1][z]
               for z in range(sz)] for x in range(sx)]
        floors[str(y)] = rows(fl)
        stand_at[str(y)] = sum(1 for r in fl for c in r if c)
        # what is over a standing head in this room: anything solid from three
        # above the floor up to nine above it -- high enough to clear a body
        # and a lintel, low enough to be this room's own ceiling rather than
        # whatever stands on the roof
        hi = range(y + 3, min(sy, y + 10))
        overs[str(y)] = rows([[any(filled[x][k][z] for k in hi)
                               for z in range(sz)] for x in range(sx)])
    # the level with the most floor on it: the storey this zone is mostly about
    principal = max(stand_at, key=lambda k: stand_at[k]) if stand_at else None
    rec['zones'][base] = {
        'levels': levels,
        'floors': floors,
        'overhead': overs,
        'standable_at_level': stand_at,
        'principal_level': principal,
        'region': [sx, sy, sz],
        'filled_cells': rep['measurements']['filled_cells'],
        'footprint_area': rep['measurements']['footprint_area'],
        'standable_cells': rep['measurements']['standable_cells'],
        'plan_area': sum(1 for r in plan for c in r if c),
        'plan': rows(plan),          # sx rows of sz chars, [x][z]
        'section_x': cut,
        'section': rows(sect),       # sy rows of sz chars, [y][z]
        'profile': prof,             # sz ints
        'anchors': {k: v for k, v in man.get('anchors', {}).items()},
    }
json.dump(rec, open(OUT, 'w'), indent=1, sort_keys=True)
print('wrote', OUT, sum(len(v['plan']) for v in rec['zones'].values()), 'plan rows')
