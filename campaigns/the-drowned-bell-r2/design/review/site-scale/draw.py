#!/usr/bin/env python3
"""Draw Halgrave to scale, with a body on it.

Five measured drawings. Every dimension on them comes from a file in this
campaign — `programs/map.json` for the boxes, `programs/zones.json` for what
each part declares, and `measured.json` for what the engine actually builds —
so a number that moves in a program moves on the page at the next run and
nothing here is transcribed by hand.

    python3 draw.py

Regenerating `measured.json` and `sweep.json` needs the engine and is a
separate step; see README.md. The drawings regenerate from those committed
records without it.
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import alloc                                                    # noqa: E402
import zonefacts as ZF                                          # noqa: E402
from svgkit import (Sheet, runs, PAPER, INK, GREY, FAINT, ALLOC,    # noqa: E402
                    ALLOC_FILL, PART, PART_FILL, OVER, SEA, BODY, GOLD,
                    GRID_MAJOR)

HERE = os.path.dirname(os.path.abspath(__file__))
PROG = os.path.normpath(os.path.join(HERE, '..', '..', 'programs'))

MAP = json.load(open(os.path.join(PROG, 'map.json')))
ZONES = {z['id']: z for z in
         json.load(open(os.path.join(PROG, 'zones.json')))['zones']}
MEAS = json.load(open(os.path.join(HERE, 'measured.json')))
MZ = MEAS['zones']
ATBOX = MEAS.get('at_allocation', {})

S = 6                    # px per block, sheets 1-4: one scale, so they compare
FLOOR = '#f4efe3'        # floor a body can stand on
VOID = '#e8e6e1'         # air over nothing
OVERH = '#c9bda6'        # what stands over a standing head

REGION = ZONES['map-halgrave']['region']
RX, RY, RZ = REGION
A = alloc.allocate(MAP, REGION)
BOX = {ZF.SYMBOL[s]: v for s, v in A.boxes.items()}
P = MAP['params']


def local_y(param):
    """A param of the massing table is a height above the standing tide; the
    region's own Y is `tide_y` plus it. `tide_y` is already the local layer."""
    return P[param] if param == 'tide_y' else P['tide_y'] + P[param]


# --------------------------------------------------------------------------
def best_fit(dx, dz, bx, bz):
    """The box's two horizontals, put the way round that most favours fitting.

    Which way a part actually turns in its box is a property of the rule that
    opens on the scope, not of the zone: `map-site-plan.md` §5 records Z2, Z5,
    Z6 and Z7 reading their box turned, while the engine's own refusal for Z4
    names its 33 on world z untuned. So these sheets assert no turn at all.
    They compare the part's footprint against the box **in whichever
    orientation fits best**, which needs no assumption and is still decisive:
    where the best case fails the part cannot fit either way round, and where
    the best case fits the sheet claims only that.
    """
    d = sorted((dx, dz))
    b = sorted((bx, bz))
    return (b[0], b[1]) if d[0] == dx else (b[1], b[0])


def crop(*masks):
    """Trim masks together to the extent anything is set in ANY of them."""
    ref = [''.join('#' if any(m[i][j] == '#' for m in masks) else '.'
                   for j in range(len(masks[0][0])))
           for i in range(len(masks[0]))]
    xs = [i for i, r in enumerate(ref) if '#' in r]
    if not xs:
        return 0, 0, [list(m) for m in masks]
    z0 = min(r.index('#') for r in ref if '#' in r)
    z1 = max(len(r) - r[::-1].index('#') for r in ref if '#' in r)
    out = [[r[z0:z1] for r in m[xs[0]:xs[-1] + 1]] for m in masks]
    return xs[0], z0, out


def paint_plan(sh, mask, ox, oy_bottom, cell, fill, op=1.0):
    """Plan mask indexed [x][z], drawn with z increasing UP the page."""
    nz = len(mask[0]) if mask else 0
    for i, row in enumerate(mask):
        for st, ln in runs(row):
            sh.rect(ox + i * cell, oy_bottom - (st + ln) * cell,
                    cell, ln * cell, fill, 'none', 0, op)
    return nz


def paint_section(sh, mask, ox, oy_bottom, cell, fill, op=1.0):
    """Section mask indexed [y][z], drawn with y increasing UP the page."""
    for i, row in enumerate(mask):
        for st, ln in runs(row):
            sh.rect(ox + st * cell, oy_bottom - (i + 1) * cell,
                    ln * cell, cell, fill, 'none', 0, op)


def title(sh, x, y, main, sub, note=None):
    sh.text(x, y, main, 22, INK, 'start', 'bold')
    sh.text(x, y + 21, sub, 12.5, GREY)
    if note:
        for i, ln in enumerate(wrap(note, 150)):
            sh.text(x, y + 40 + i * 15, ln, 10.5, FAINT, 'start', 'normal',
                    'italic')


def wrap(s, n):
    out, line = [], ''
    for wd in s.split():
        if len(line) + len(wd) + 1 > n:
            out.append(line)
            line = wd
        else:
            line = (line + ' ' + wd).strip()
    if line:
        out.append(line)
    return out


def key(sh, x, y, items, cols=1):
    per = math.ceil(len(items) / cols)
    for i, (colour, label, kind) in enumerate(items):
        cx = x + (i // per) * 300
        yy = y + (i % per) * 17
        if kind == 'fill':
            sh.rect(cx, yy - 8, 20, 10, colour, 'none', 0)
        else:
            sh.rect(cx, yy - 8, 20, 10, 'none', colour, 1.7, 1, kind)
        sh.text(cx + 27, yy, label, 10, GREY)


def declutter(want, gap):
    """Push labels apart without reordering them."""
    out = list(want)
    for i in range(1, len(out)):
        if out[i] < out[i - 1] + gap:
            out[i] = out[i - 1] + gap
    return out


def alloc_message(zid):
    """The engine's own words when the part is expanded at its box. On a
    build the line names the files it wrote, which is machinery and not a
    fact about the part, so only the measurement after the dash is kept."""
    m = ATBOX.get(zid, {}).get('message', '')
    if fits(zid):
        tail = m.split('—')[-1].strip() if '—' in m else m
        return 'it builds at this box, as ' + tail
    return m.replace('error: ', '').replace('%s-alloc: ' % zid, '') or '—'


def fits(zid):
    return ATBOX.get(zid, {}).get('exit') == 0


# ==========================================================================
# Sheet 1 — the site in plan, with a party of four standing on it
# ==========================================================================
def sheet1(path):
    ml, mt = 60, 175
    clip_pad = 15                       # blocks of overflow shown before cutoff
    plan_w = RX * S
    lab_x = ml + plan_w + clip_pad * S + 46
    w = lab_x + 560
    foot_h = 300
    h = mt + RZ * S + 120 + foot_h
    sh = Sheet(S, int(w), int(h), 'Halgrave — the site plan, to scale')

    def px(x):
        return ml + x * S

    def py(z):
        return mt + (RZ - z) * S

    title(sh, 40, 52,
          'Halgrave, in plan, to scale',
          'the whole region map.json declares — %d × %d × %d blocks — with the '
          'party the delve is built for standing on it' % (RX, RY, RZ),
          'Solid blue is the box the site plan hands each part. The dashed '
          'outline is what that part declares in zones.json, laid in that box '
          'at true scale, put the way round that fits best — cut off at the '
          'edge of the sheet where it runs past. Which way a part actually '
          'turns is a property of the rule that opens on the box, so no sheet '
          'here asserts one. A grammar program is '
          'region-polymorphic, so a part whose declared size disagrees with '
          'its box may still BUILD there: it builds a different piece from the '
          'one that was reviewed, which is what the plan’s own DW0806 debt is '
          'about.')

    sh.raw('<clipPath id="site"><rect x="%.1f" y="%.1f" width="%.1f" '
           'height="%.1f"/></clipPath>'
           % (px(-clip_pad), py(RZ) - clip_pad * S,
              (RX + 2 * clip_pad) * S, (RZ + 2 * clip_pad) * S))

    sh.rect(px(0), py(RZ), plan_w, RZ * S, '#ffffff', GRID_MAJOR, 1.4)
    sh.grid(px(0), py(RZ), RX, RZ, 10, 50)

    for sym, org, size in A.nodes:
        if sym == 'open_sea':
            so, ss = org, size
    sh.rect(px(so[0]), py(so[2] + ss[2]), ss[0] * S, ss[2] * S, SEA, 'none', 0, .5)
    sh.text(px(so[0]) + ss[0] * S / 2, py(so[2] + ss[2] / 2),
            'the open sea', 11, '#33627a', 'middle', 'normal', 'italic')
    sh.text(px(so[0]) + ss[0] * S / 2, py(so[2] + ss[2] / 2) + 14,
            '%d × %d' % (ss[0], ss[2]), 9.5, '#33627a', 'middle')

    for zid in ZF.ORDER:
        (ox, oy, oz), (bx, by, bz) = BOX[zid]
        sh.rect(px(ox), py(oz + bz), bx * S, bz * S, ALLOC_FILL, ALLOC, 1.8, .9)
        sh.text(px(ox) + 5, py(oz + bz) + 14,
                ZF.FACTS[zid]['tag'], 13, ALLOC, 'start', 'bold')

    # what each part declares, clipped where it runs off
    sh.raw('<g clip-path="url(#site)">')
    for zid in ZF.ORDER:
        (ox, oy, oz), (bx, by, bz) = BOX[zid]
        dx, dy, dz = ZONES[zid]['region']
        # drawn the way round that fits best, which is the only claim made
        wx, wz = (dx, dz) if (bx >= bz) == (dx >= dz) else (dz, dx)
        ok = fits(zid)
        sh.rect(px(ox), py(oz + wz), wx * S, wz * S, 'none',
                PART if ok else OVER, 1.7, .9, '6,4')
    sh.raw('</g>')

    # a party of four where the player wakes, and one on the crown
    sh.party_plan(px(17), py(5))
    sh.text(px(17) - 10, py(5) + 4, 'a party of four', 10.5, BODY, 'end',
            'bold')
    sh.text(px(17) - 10, py(5) + 17, '4 blocks abreast', 9.5, FAINT, 'end')
    (tx, ty, tz), (tbx, tby, tbz) = BOX['z7-bell-tower']
    sh.party_plan(px(tx + 15), py(tz + 4))

    # the order of arrival, through the centres of the boxes it visits
    pts = []
    for zid in ZF.JOURNEY:
        (ox, oy, oz), (bx, by, bz) = BOX[zid]
        pts.append((px(ox + bx * .38), py(oz + bz / 2)))
    sh.poly(pts, 'none', GOLD, 1.5, '3,4', .85)
    for i, (x, y) in enumerate(pts):
        sh.raw('<circle cx="%.2f" cy="%.2f" r="7.5" fill="%s" opacity="0.95"/>'
               % (x, y, GOLD))
        sh.text(x, y + 3.5, str(i + 1), 9, PAPER, 'middle', 'bold')

    # the label column, ordered north to south and pushed apart
    rows_ = sorted(ZF.ORDER, key=lambda z: -(BOX[z][0][2] + BOX[z][1][2] / 2))
    want = [py(BOX[z][0][2] + BOX[z][1][2] / 2) - 14 for z in rows_]
    got = declutter(want, 108)
    shift = min(0, mt + RZ * S - 20 - got[-1])
    for zid, ly in zip(rows_, got):
        ly += shift
        f = ZF.FACTS[zid]
        (ox, oy, oz), (bx, by, bz) = BOX[zid]
        dx, dy, dz = ZONES[zid]['region']
        ok = fits(zid)
        sh.line(px(ox + bx), py(oz + bz / 2), lab_x - 10, ly - 4, FAINT, .8,
                '2,3')
        sh.text(lab_x, ly, '%s  %s  %s' % (f['tag'], f['name'], f['cn']),
                13, INK, 'start', 'bold')
        sh.text(lab_x, ly + 16,
                'the plan gives it %d × %d × %d  ·  %d min of the run'
                % (bx, by, bz, f['minutes']), 10.5, ALLOC)
        sh.text(lab_x, ly + 31,
                'it declares %d × %d × %d  —  %s' %
                (dx, dy, dz, 'it builds here, at the box’s size' if ok
                 else 'it refuses here'), 10.5, PART if ok else OVER)
        abx, abz = best_fit(dx, dz, bx, bz)
        marks = []
        for got, need, ax in ((by, dy, 'high'), (abx, dx, 'one way'),
                              (abz, dz, 'the other')):
            marks.append('%s %d in %d %s' % ('OK' if got >= need else 'NO',
                                             need, got, ax))
        sh.text(lab_x, ly + 46, 'best case either way round:  ' +
                '   ·   '.join(marks), 9.8, PART if ok else OVER)
        sh.text(lab_x, ly + 60, 'the player ' + f['does'], 10.5, GREY)
        sh.text(lab_x, ly + 74, 'floor: ' + f['floor'], 9.5, FAINT)

    sh.north(px(RX) + 22, mt + 22)
    sh.scalebar(px(0), mt + RZ * S + 40, 50)
    key(sh, px(0) + 380, mt + RZ * S + 26, [
        (ALLOC, 'the box the site plan hands the part', None),
        (PART, 'what the part declares, where it builds', '6,4'),
        (OVER, 'what the part declares, where it refuses', '6,4'),
        (BODY, 'a player — one block in plan', 'fill'),
        (GOLD, 'the order of arrival (a sequence, not a path)', None),
        (SEA, 'sea', 'fill'),
    ], cols=2)

    fy = mt + RZ * S + 128
    sh.text(40, fy, 'What is in each box', 15, INK, 'start', 'bold')
    sh.text(190, fy, 'transcribed from beats.md, “What fills it” — nothing '
            'here is invented for the drawing', 10.5, GREY)
    fy += 22
    colw = (w - 100) / 4
    for i, zid in enumerate(ZF.ORDER):
        f = ZF.FACTS[zid]
        x = 40 + (i % 4) * colw
        y = fy + (i // 4) * 112
        sh.text(x, y, '%s %s' % (f['tag'], f['name']), 11, INK, 'start', 'bold')
        yy = y + 15
        for it in f['fills'][:6]:
            for ln in wrap('· ' + it, int(colw / 4.6))[:2]:
                sh.text(x, yy, ln, 8.8, GREY)
                yy += 10.5
            yy += 2
    sh.write(path)


# ==========================================================================
# Sheet 2 — the eight parts as the engine actually builds them
# ==========================================================================
def sheet2(path):
    colmin = 210
    gutter = 26
    cols = []
    for zid in ZF.ORDER:
        dx = MZ[zid]['region'][0]
        cols.append(max(colmin, dx * S))
    ml, mt = 50, 365
    w = ml * 2 + sum(cols) + gutter * (len(cols) - 1)
    maxz = max(MZ[z]['region'][2] for z in ZF.ORDER)
    base = mt + maxz * S
    h = base + 230
    sh = Sheet(S, int(w), int(h), 'The eight parts, measured, at one scale')

    title(sh, 40, 52,
          'The eight parts, as the engine builds them',
          'each part’s own floor plan, measured off an expansion of its program '
          'at the region zones.json declares — at the same scale as the site '
          'plan',
          'The storey drawn is the one with the most floor on it, chosen by '
          'count. Tone is wall; pale is floor a body can stand on. The heavy '
          'rectangle is the box the site plan hands that part, laid on the '
          'part corner to corner, put the way round that fits best. A grammar '
          'program is region-polymorphic, so where a part DOES build in its '
          'box it builds a different piece from the one drawn here — which is '
          'what the plan’s own DW0806 debt is about.')

    x = ml
    for zid, cw in zip(ZF.ORDER, cols):
        m = MZ[zid]
        f = ZF.FACTS[zid]
        dx, dy, dz = m['region']
        (ox, oy, oz), (bx, by, bz) = BOX[zid]
        ok = fits(zid)
        dw = dx * S
        gx = x + (cw - dw) / 2

        sh.rect(gx, base - dz * S, dw, dz * S, VOID, FAINT, 1, .9)
        lvl = m['principal_level']
        paint_plan(sh, m['floors'][lvl], gx, base, S, FLOOR)
        paint_plan(sh, m['levels'][lvl], gx, base, S, PART_FILL)

        abx, abz = best_fit(dx, dz, bx, bz)
        sh.rect(gx, base - abz * S, abx * S, abz * S, 'none',
                ALLOC if ok else OVER, 2.2, .95)

        sh.text(x, mt - 196, f['tag'], 16, INK, 'start', 'bold')
        sh.text(x + 28, mt - 196, f['name'], 12.5, INK)
        sh.text(x, mt - 178, f['cn'], 11, GREY)
        sh.text(x, mt - 138, 'declares  %d × %d × %d' % (dx, dy, dz), 10.5, PART)
        sh.text(x, mt - 124, 'is given  %d × %d × %d' % (bx, by, bz), 10.5,
                ALLOC if ok else OVER)
        sh.text(x, mt - 106, 'BUILDS in its box' if ok else 'REFUSES in its box',
                11.5, ALLOC if ok else OVER, 'start', 'bold')
        sh.text(x, mt - 88, 'storey drawn: y = %s' % lvl, 9.5, FAINT)
        sh.text(x, mt - 76, '%s standable cells here' %
                f"{m['standable_at_level'][lvl]:,}", 9.5, GREY)
        sh.text(x, mt - 64, '%s standable in the zone' %
                f"{m['standable_cells']:,}", 9.5, GREY)
        sh.text(x, mt - 52, '%s blocks placed' % f"{m['filled_cells']:,}",
                9.5, GREY)
        sh.text(x, mt - 40, '%s m² of plan' % f"{m['footprint_area']:,}",
                9.5, GREY)

        spot = party_spot(m['floors'][lvl])
        if spot:
            a, b = spot
            for k in range(4):
                sh.body_plan(gx + a * S, base - (b + k + 1) * S)

        chars = max(22, int(cw / 4.9))
        sh.text(x, base + 26, 'expanded at its box, the engine says:', 9, FAINT)
        for j, ln in enumerate(wrap(alloc_message(zid), chars)[:7]):
            sh.text(x, base + 39 + j * 11, ln, 8.6, ALLOC if ok else OVER)
        x += cw + gutter

    sh.scalebar(ml, base + 150, 50)
    sh.write(path)


def party_spot(floors):
    """Four standable cells in a line, as far from an edge as they can be."""
    best = None
    for a, r in enumerate(floors):
        for b in range(len(r) - 3):
            if r[b:b + 4] == '####':
                d = min(a, len(floors) - 1 - a, b, len(r) - 4 - b)
                if best is None or d > best[0]:
                    best = (d, a, b)
    return (best[1], best[2]) if best else None


# ==========================================================================
# Sheet 3 — the section: the planes, the hole, and the climb
# ==========================================================================
def sheet3(path):
    ml, mt = 330, 175
    w = ml + RZ * S + 400
    tower = MZ['z7-bell-tower']
    tz, ty2 = tower['region'][2], tower['region'][1]
    sec_top = mt + RY * S + 190
    h = sec_top + ty2 * S + 190
    sh = Sheet(S, int(w), int(h), 'Halgrave in section, south to north')

    def px(z):
        return ml + z * S

    def py(y):
        return mt + (RY - y) * S

    title(sh, 40, 52,
          'Halgrave in section, south to north',
          'the same %d blocks of depth as the plan, and the %d blocks of height '
          'the brief fixes' % (RZ, RY),
          'A plan hides the two things map-brief.md says a box plan loses — the '
          'ward is a hole, and the tower is a climb. Every plane of the brief’s '
          'massing table is drawn at the region-local layer map.json puts it '
          'at, which is tide_y plus the height above the tide.')

    sh.rect(px(0), py(RY), RZ * S, RY * S, '#ffffff', GRID_MAJOR, 1.4)
    sh.grid(px(0), py(RY), RZ, RY, 10, 50)

    for zid in ZF.ORDER:
        (ox, oy, oz), (bx, by, bz) = BOX[zid]
        sh.rect(px(oz), py(oy + by), bz * S, by * S, ALLOC_FILL, ALLOC, 1.4, .5)
    for zid in ZF.ORDER:
        (ox, oy, oz), (bx, by, bz) = BOX[zid]
        dy2 = 15 if (oz // 20) % 2 == 0 else 41
        sh.text(px(oz + bz / 2), py(oy + by) + dy2, ZF.FACTS[zid]['tag'],
                12, ALLOC, 'middle', 'bold')
        sh.text(px(oz + bz / 2), py(oy + by) + dy2 + 13,
                '%d deep · %d high' % (bz, by), 8.5, ALLOC, 'middle')

    sh.rect(px(0), py(P['tide_y']), 80 * S, P['tide_y'] * S, SEA, 'none', 0, .45)

    # the massing table, grouped by the block layer each plane lands on
    layers = {}
    for param, metres, what in ZF.PLANES:
        layers.setdefault(local_y(param), []).append((metres, what, param))
    want = [py(y) for y in sorted(layers, reverse=True)]
    got = declutter(want, 16)
    for y, ly in zip(sorted(layers, reverse=True), got):
        names = layers[y]
        heavy = any(p == 'tide_y' for _, _, p in names)
        sh.line(px(0) - 6, py(y), px(RZ) + 6, py(y), INK if heavy else FAINT,
                1.7 if heavy else .8, None if heavy else '3,3')
        if abs(ly - py(y)) > 2:
            sh.line(px(0) - 6, py(y), px(0) - 16, ly - 4, FAINT, .6)
        txt = ' · '.join('%s %s' % (m, wt) for m, wt, _ in names)
        sh.text(px(0) - 20, ly, txt, 9.5, INK if heavy else GREY, 'end',
                'bold' if heavy else 'normal')
        sh.text(px(RZ) + 12, ly, 'y = %d' % y, 9, INK if heavy else FAINT)
        if abs(ly - py(y)) > 2:
            sh.line(px(RZ) + 6, py(y), px(RZ) + 10, ly - 4, FAINT, .6)
        if len(names) > 1:
            sh.text(px(RZ) + 46, ly,
                    '← %d named planes land on this one block layer'
                    % len(names), 9, OVER, 'start', 'bold')

    stand = [('flat_floor_y', 8, 'wakes here'), ('road_y', 92, 'the ledge'),
             ('gate_y', 99, 'the gate'), ('causeway_y', 116, 'the causeway'),
             ('cistern_y', 126, 'the cistern'), ('cloister_y', 120, 'the cloister'),
             ('hall_y', 134, 'the hall'), ('upper_ward_y', 141, 'the tower foot'),
             ('belfry_y', 145, 'the belfry')]
    for param, z, label in stand:
        sh.body_elev(px(z), py(local_y(param)))
        sh.text(px(z) + S / 2, py(local_y(param)) + 12, label, 8.2, BODY,
                'middle')

    y0, y1 = local_y('upper_ward_y'), local_y('belfry_y')
    cx = px(RZ) + 250
    sh.line(cx, py(y0), cx, py(y1), GOLD, 2.2)
    sh.line(cx - 6, py(y0), cx + 6, py(y0), GOLD, 2.2)
    sh.line(cx - 6, py(y1), cx + 6, py(y1), GOLD, 2.2)
    mid = (py(y0) + py(y1)) / 2
    sh.text(cx + 10, mid - 6, '%d blocks of climb' % (y1 - y0), 11, GOLD,
            'start', 'bold')
    sh.text(cx + 10, mid + 8, 'tower foot to belfry floor', 9.5, GOLD)
    sh.text(cx + 10, mid + 21, '— eight bodies stacked', 9.5, GOLD)

    # the tower zone as built, at the same scale, against the site's own height
    sh.text(40, sec_top - 54, 'The tower zone, measured, at the same scale',
            16, INK, 'start', 'bold')
    for i, ln in enumerate(wrap(
            'the long section the engine builds at the region z7 declares '
            '(%d × %d × %d), cut at x = %d — the slice with the most floor in '
            'it. The dashed rectangle is the whole site’s height and depth, '
            'laid on it from the same base.'
            % (tower['region'][0], ty2, tz, tower['section_x']), 140)):
        sh.text(40, sec_top - 34 + i * 15, ln, 10.5, GREY)
    sb = sec_top + ty2 * S
    sh.rect(ml, sec_top, tz * S, ty2 * S, VOID, FAINT, 1)
    paint_section(sh, tower['section'], ml, sb, S, PART_FILL)
    sh.rect(ml, sb - RY * S, RZ * S, RY * S, 'none', OVER, 2.2, 1, '7,5')
    sh.body_elev(ml + 3 * S, sb)
    tx = ml + RZ * S + 24
    sh.text(tx, sb - RY * S + 4, 'the whole site is %d tall and %d deep'
            % (RY, RZ), 11, OVER, 'start', 'bold')
    sh.text(tx, sb - RY * S + 19, 'this one zone declares %d and %d'
            % (ty2, tz), 11, OVER)
    sh.text(tx, sb - RY * S + 34, 'and the plan gives it a box %d deep'
            % BOX['z7-bell-tower'][1][2], 11, OVER)
    sh.scalebar(ml, sb + 40, 50)
    sh.write(path)


# ==========================================================================
# Sheet 4 — the ruler: does a bigger rock change anything?
# ==========================================================================
def sheet4(path, sweep):
    picks = [70, 90, 97, 110]
    ml, mt = 55, 365
    gut = 70
    cols = [max(230, r * S) for r in picks]
    w = ml * 2 + sum(cols) + gut * (len(picks) - 1)
    maxdepth = 80 + max(picks)
    base = mt + maxdepth * S
    h = base + 330
    sh = Sheet(S, int(w), int(h), 'How big does the rock need to be?')

    title(sh, 40, 52,
          'The same site plan on a bigger rock',
          'map.json re-evaluated at rock_run = %s, at the scale of the other '
          'sheets, with every part expanded at the box each size gives it'
          % ', '.join(map(str, picks)),
          'The rock’s plan size is the one number in map.json the brief does '
          'not fix: 70 is a reading of the compactness sentence, not a fact of '
          'record. These are the ruler beside it. 90 is the mid-point; 97 is '
          'where the brief’s own belfry sightline runs out (80 + 97 = 177 m); '
          '110 is past it, and is drawn so that being past it is visible.')

    x = ml
    for rock, cw in zip(picks, cols):
        rz = 80 + rock
        aa = alloc.allocate(MAP, [rock, RY, rz], {'rock_run': rock})
        bx = {ZF.SYMBOL[s]: v for s, v in aa.boxes.items()}
        gx0 = x + (cw - rock * S) / 2
        legal = rz <= 177

        def gx(v):
            return gx0 + v * S

        def gy(z):
            return base - z * S

        sh.rect(gx(0), gy(rz), rock * S, rz * S, '#ffffff', GRID_MAJOR, 1.3)
        sh.grid(gx(0), gy(rz), rock, rz, 10, 50)
        for zid in ZF.ORDER:
            (ox, oy, oz), (bxx, byy, bzz) = bx[zid]
            ok = sweep[str(rock)][zid]['ok']
            sh.rect(gx(ox), gy(oz + bzz), bxx * S, bzz * S,
                    ALLOC_FILL if ok else '#f7ece9',
                    ALLOC if ok else OVER, 1.5, .92)
            sh.text(gx(ox + bxx / 2), gy(oz + bzz / 2) + 4,
                    ZF.FACTS[zid]['tag'], 10.5, ALLOC if ok else OVER,
                    'middle', 'bold')
        sh.party_plan(gx(rock // 2 - 2), gy(5))

        built = sum(1 for z in ZF.ORDER if sweep[str(rock)][z]['ok'])
        sh.text(x, mt - 158, 'rock %d × %d' % (rock, rock), 17, INK, 'start',
                'bold')
        sh.text(x, mt - 139, 'region %d × %d × %d' % (rock, RY, rz), 10.5, GREY)
        sh.text(x, mt - 125, 'rock plan area %s m²' % f'{rock * rock:,}',
                10.5, GREY)
        sh.text(x, mt - 104, '%d of 8 parts build' % built, 14,
                ALLOC if built > 1 else OVER, 'start', 'bold')
        sh.text(x, mt - 85,
                'belfry reach %d m %s 177' % (rz, '≤' if legal else '>'),
                10.5, GREY if legal else OVER, 'start',
                'normal' if legal else 'bold')
        sh.text(x, mt - 71,
                'the rock subtends %.1f° from the belfry' % subtend(rock),
                10.5, GREY)
        sh.text(x, mt - 57,
                '(27° reads as one object; 18° as an object in its setting)',
                9, FAINT)
        if not legal:
            sh.text(x, mt - 38, 'REFUSED by the brief’s own bound', 11, OVER,
                    'start', 'bold')
        sh.text(x, mt - 20, 'the tower’s box: %d deep'
                % bx['z7-bell-tower'][1][2], 10.5, GREY)
        x += cw + gut

    fy = base + 96
    sh.text(40, fy, 'What the sweep found', 17, INK, 'start', 'bold')
    sh.text(230, fy, 'every zone expanded at the box each rock size gives it, '
            'at rock_run 70 to 140, one block at a time', 10.5, GREY)
    lines = [
        ('From rock 70 to rock 140 — twice the rock, four times its plan area '
         '— the set of parts that build does not change. It is the cliff road, '
         'at every size, and nothing else.', INK, 'bold'),
        ('The plan halves the rock’s depth, halves it again, and halves it '
         'again, so the hall and the tower each get an eighth of it: 9 blocks '
         'at rock 70, 12 at rock 90, 18 at rock 140. The tower declares 125. '
         'Growing the rock grows an eighth of it.', GREY, 'normal'),
        ('Z0 never moves at all: the flat’s box is 40 × 8 × 80 at every rock '
         'size, because both its plan numbers are brief facts and its height is '
         'tide_y + road_y. It refuses on height, and the rock cannot reach it.',
         GREY, 'normal'),
        ('So the rock’s size is not what is stopping anything, and “is 70 × 70 '
         'big enough” has no answer in the direction it is asked. What the '
         'parts are too big for is the SUBDIVISION, not the rock.',
         OVER, 'bold'),
    ]
    yy = fy + 28
    for t, c, wt in lines:
        for ln in wrap(t, 130):
            sh.text(40, yy, ln, 11.5, c, 'start', wt)
            yy += 16
        yy += 8
    sh.scalebar(40, base + 30, 50)
    sh.write(path)


def subtend(rock):
    """The angle the rock subtends from the belfry, in the brief's own idiom:
    a 33.12 m drop from a standing eye at +31.62 to the ward floor at −1.5,
    seen across the rock's own run."""
    return math.degrees(math.atan(33.12 / rock))


# ==========================================================================
# Sheet 5 — a body in it
# ==========================================================================
PANELS = [
    ('z1-cliff-road', None, 'The ledge',
     'the whole of the route between the shore and the gate, and it is '
     'single file'),
    ('z3-drowned-ward', 'anchor/causeway-head', 'The causeway and the ward',
     'the raised spine, the arcades, and the water on both sides'),
    ('z4-chapel-ward', 'anchor/sexton-1', 'The cloister',
     'where the Two Sextons are fought, and the ward cannot be crossed '
     'around them'),
    ('z5-hall-keep', 'anchor/hall-door', 'The hall',
     'where Ridd blocks, waits, and takes the fight seriously'),
    ('z6-cistern-deep', 'anchor/founder', 'The cistern',
     'the delve’s largest interior, at the level the Founder is fought on'),
    ('z7-bell-tower', 'anchor/bell-walk', 'The belfry',
     'the room the bell is walked AROUND, at the level the bell-walk '
     'anchor stands at'),
]


def transpose(mask):
    """Swap a plan mask's two horizontal axes."""
    return [''.join(mask[i][j] for i in range(len(mask)))
            for j in range(len(mask[0]))]


def sheet5(path):
    ml, mt = 55, 330
    w = 1560
    U = 15
    # measure every panel first, so the page is exactly as tall as it needs
    panels = []
    for zid, anchor, name, sub in PANELS:
        m = MZ[zid]
        if anchor and anchor in m['anchors']:
            lvl = str(m['anchors'][anchor]['pos'][1])
            basis = 'the storey %s stands at' % anchor
        else:
            lvl = m['principal_level']
            basis = 'the storey with the most floor on it'
        x0, z0, (wc, fc, oc) = crop(m['levels'][lvl], m['floors'][lvl],
                                    m['overhead'][lvl])
        # what is over a standing head is only worth drawing where a body
        # can be standing: hatched floor is roofed floor
        oc = [''.join('#' if (o == '#' and f == '#') else '.'
                      for o, f in zip(orow, frow))
              for orow, frow in zip(oc, fc)]
        turned = len(wc[0]) > 2 * len(wc)
        if turned:
            wc, fc, oc = transpose(wc), transpose(fc), transpose(oc)
        nx, nz = len(wc), len(wc[0])
        cell = min(16.0, (w - 2 * ml) / max(1, nx), 520.0 / max(1, nz))
        panels.append((zid, m, lvl, basis, name, sub, wc, fc, oc, nx, nz,
                       cell, turned))
    h = mt + sum(p[10] * p[11] + 200 for p in panels) + 60
    sh = Sheet(U, int(w), int(h), 'A body in it')

    title(sh, 40, 52,
          'A body in it',
          'six rooms the engine actually builds, each at the storey its own '
          'anchors stand at, each with the party standing in it',
          'This is the one sheet not at the scale of the others: every panel is '
          'drawn as large as it fits and states its own scale, because this '
          'sheet is about whether a person fits rather than about how the parts '
          'compare. Dark tone is wall at this storey; pale is floor a body can '
          'stand on; hatched is floor with something over a standing head on '
          'it — a vault, a roof, an arcade, the bell. Four green dots are the '
          'party, and they are the ruler on every panel: where they stand in a '
          'line it is because a line is what the room allows.')

    sh.raw('<pattern id="over" width="7" height="7" '
           'patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
           '<rect width="7" height="7" fill="none"/>'
           '<line x1="0" y1="0" x2="0" y2="7" stroke="%s" stroke-width="2.6"/>'
           '</pattern>' % OVERH)

    # the unit
    ux, uy = ml, mt - 40
    sh.text(40, mt - 152, 'THE UNIT', 12, INK, 'start', 'bold')
    sh.rect(ux, uy - 6 * U, 46 * U, 6 * U, '#ffffff', GRID_MAJOR, 1.2)
    for i in range(47):
        sh.line(ux + i * U, uy - 6 * U, ux + i * U, uy,
                GRID_MAJOR if i % 5 == 0 else '#eeeae0', .7)
    for j in range(7):
        sh.line(ux, uy - j * U, ux + 46 * U, uy - j * U,
                GRID_MAJOR if j % 5 == 0 else '#eeeae0', .7)
    sh.s = U
    sh.body_elev(ux + 1 * U, uy)
    sh.text(ux + 2.6 * U, uy - 2.4 * U, 'one player — 1 wide, 2 tall',
            12, BODY, 'start', 'bold')
    sh.party_elev(ux + 9 * U, uy)
    sh.text(ux + 9 * U, uy + 17, 'the party of four — 4 blocks abreast',
            11, BODY)
    zp = json.load(open(os.path.join(PROG, 'z7-bell-tower.json')))['params']
    dx0 = ux + 22 * U
    sh.rect(dx0, uy - zp['door_height'] * U, zp['door_width'] * U,
            zp['door_height'] * U, '#ffffff', INK, 1.8)
    sh.body_elev(dx0 + U, uy)
    sh.text(dx0, uy + 17, 'the tower door — %d wide, %d high'
            % (zp['door_width'], zp['door_height']), 11, GREY)
    zw = json.load(open(os.path.join(PROG, 'z1-cliff-road.json')))['params']
    lx = ux + 34 * U
    sh.rect(lx, uy - U, zw['walk'] * U, U, PART_FILL, PART, 1.4)
    sh.body_elev(lx, uy - U)
    sh.text(lx, uy + 17, 'the cliff road’s walk — %d wide' % zw['walk'],
            11, GREY)
    sh.text(lx, uy + 31, 'a party of four does not fit abreast on it',
            11.5, OVER, 'start', 'bold')

    y = mt + 40
    for (zid, m, lvl, basis, name, sub, wc, fc, oc, nx, nz, cell,
         turned) in panels:
        sh.s = cell
        sh.text(ml, y, name, 18, INK, 'start', 'bold')
        sh.text(ml, y + 19, sub, 11.5, GREY)
        sh.text(ml, y + 35, '%s, y = %s — %s — %d × %d blocks%s'
                % (zid, lvl, basis, nx, nz,
                   '  ·  turned, long axis across the page' if turned else ''),
                10, FAINT)
        top = y + 48
        bot = top + nz * cell
        sh.rect(ml, top, nx * cell, nz * cell, VOID, FAINT, 1)
        paint_plan(sh, fc, ml, bot, cell, FLOOR)
        paint_plan(sh, oc, ml, bot, cell, 'url(#over)')
        paint_plan(sh, wc, ml, bot, cell, PART_FILL)
        spot = party_spot(fc)
        if spot:
            a, b = spot
            for k in range(4):
                sh.body_plan(ml + a * cell, bot - (b + k + 1) * cell)
        else:
            sh.text(ml, bot + 18, 'no four standable cells in a line at this '
                    'storey', 11, OVER, 'start', 'bold')
        sh.line(ml, bot + 26, ml + 10 * cell, bot + 26, INK, 1.6)
        for t in range(11):
            sh.line(ml + t * cell, bot + 22, ml + t * cell, bot + 30, INK, .9)
        sh.text(ml + 10 * cell + 8, bot + 30,
                '10 blocks  ·  1 block = %.1f px on this panel' % cell,
                10, GREY)
        sh.text(ml, bot + 48, '%s standable cells at this storey, %s in the '
                'whole zone' % (f"{m['standable_at_level'][lvl]:,}",
                                f"{m['standable_cells']:,}"), 10, GREY)
        y = bot + 152
    sh.write(path)


# ==========================================================================
def main():
    sweep = json.load(open(os.path.join(HERE, 'sweep.json')))
    sheet1(os.path.join(HERE, '01-site-plan.svg'))
    sheet2(os.path.join(HERE, '02-parts-at-scale.svg'))
    sheet3(os.path.join(HERE, '03-section.svg'))
    sheet4(os.path.join(HERE, '04-how-big-is-the-rock.svg'), sweep)
    sheet5(os.path.join(HERE, '05-a-body-in-it.svg'))
    print('drew five sheets in', HERE)


if __name__ == '__main__':
    main()
