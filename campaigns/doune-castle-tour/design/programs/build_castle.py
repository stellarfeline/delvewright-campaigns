#!/usr/bin/env python3
"""Emits castle.json, the grammar program that builds the whole Doune site.

The grammar partitions space: every cell belongs to exactly one leaf of the
split tree and nothing paints over anything. A castle is a 2.5-D thing — each
column is a stack of courses — so each part of the site describes its own
columns (castle/*.py) and this driver asks the right part for each column,
merges the palettes and anchors, and emits the partition: equal columns merge
along x, equal rows merge along z.

Run it to regenerate castle.json. The JSON is the artifact the engine reads.
"""
import json, pathlib

from castle.common import (X, Y, Z, GRADE, WALK, CX0, CX1, CZ0, CZ1, COURT_Z0,
                           SCURT_Z1, RANGE_Z1, KT, SV, HALL, GH, Col, inside,
                           PALETTE as BASE_PALETTE)
from castle import grounds, gatehouse, hall, kitchen

PARTS = [grounds, gatehouse, hall, kitchen]

PALETTE = dict(BASE_PALETTE)
ANCHORS = {}
for part in PARTS:
    PALETTE.update(part.PALETTE)
    ANCHORS.update(part.ANCHORS)


def column(x, z):
    c = Col()
    c.add("rock", GRADE)                       # y0..y6 under everything
    if z < CZ0:
        return grounds.approach_column(c, x, z)
    if not (CX0 <= x <= CX1 and CZ0 <= z <= CZ1):
        return grounds.outside_column(c, x, z)
    if COURT_Z0 <= z <= SCURT_Z1:
        wall = grounds.curtain_column(c, x, z)
        return wall if wall is not None else grounds.courtyard_column(c, x, z)
    if inside(x, z, GH):
        return gatehouse.gatehouse(c, x, z)
    if inside(x, z, HALL):
        return hall.great_hall(c, x, z)
    if inside(x, z, SV):
        return kitchen.servery(c, x, z)
    if inside(x, z, KT):
        return kitchen.kitchen_tower(c, x, z)
    return grounds.courtyard_column(c, x, z)   # the apron before hall and servery


def sz(n):
    return {"size": "absolute", "blocks": {"expr": "int", "value": n}}

def split(axis, spans):
    return {"op": "split", "axis": axis, "sizes": [sz(n) for n, _ in spans],
            "children": [c for _, c in spans]}

def fill(role):
    return {"op": "fill", "material": {"role": role}}

def void():
    return {"op": "void"}

def mark(anchor, role=None):
    m = {"anchor": anchor, "at": "floor_center"}
    if role:
        m["role"] = role
    return {"op": "mark", "mark": m, "body": void()}

def column_node(x, z, col):
    """One column's spans, with any anchor cell split out and marked."""
    marks = {y: ANCHORS[(x, y, z)] for (mx, y, mz) in ANCHORS if (mx, mz) == (x, z)
             for _ in [0]} if any((mx, mz) == (x, z) for (mx, _, mz) in ANCHORS) else {}
    spans, y = [], 0
    for role, n in col.spans:
        if marks:
            for cell in range(y, y + n):
                if cell in marks:
                    anchor, arole = marks[cell]
                    before = cell - y
                    if before:
                        spans.append((before, fill(role) if role else void()))
                    spans.append((1, mark(anchor, arole)))
                    rest = y + n - cell - 1
                    if rest:
                        spans.append((rest, fill(role) if role else void()))
                    break
            else:
                spans.append((n, fill(role) if role else void()))
        else:
            spans.append((n, fill(role) if role else void()))
        y += n
    if len(spans) == 1 and spans[0][0] == Y:
        return spans[0][1]
    return split("y", spans)

def build():
    # one column per cell, then merge equal columns along x, then equal rows
    rows = []
    for z in range(Z):
        cells = [column(x, z) for x in range(X)]
        keys = [(c.key(), tuple(sorted(a for (ax, _, az), a in ANCHORS.items()
                                       if (ax, az) == (x, z))))
                for x, c in enumerate(cells)]
        runs, start = [], 0
        for x in range(1, X + 1):
            if x == X or keys[x] != keys[start]:
                runs.append((start, x - start))
                start = x
        rows.append((keys, [(x0, n, column_node(x0, z, cells[x0])) for x0, n in runs]))

    z_spans, start = [], 0
    for z in range(1, Z + 1):
        if z == Z or rows[z][0] != rows[start][0]:
            node = split("x", [(n, body) for _, n, body in rows[start][1]])
            z_spans.append((z - start, node))
            start = z
    return split("z", z_spans)


PROGRAM = {
    "version": "1.9.0",
    "name": "doune_castle",
    "start": "site",
    "params": {},
    "palette": PALETTE,
    "rules": {"site": [{"weight": 1, "body": build()}]},
    "shown_faces": ["north", "south", "east", "west"],
}

if __name__ == "__main__":
    out = pathlib.Path(__file__).with_name("castle.json")
    out.write_text(json.dumps(PROGRAM, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size} bytes), region {X}x{Y}x{Z}, "
          f"{len(ANCHORS)} anchor(s), {len(PALETTE)} role(s)")
