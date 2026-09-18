#!/usr/bin/env python3
"""Emits vesperhold.json, the grammar program that builds the whole site.

Every part of the site paints roles into one voxel grid (castle/*.py); this
driver turns the grid into the grammar's partition — one column per cell as a
stack of spans, equal columns merged along x, equal rows merged along z — and
writes the gate regions the program cannot declare into gates.json, which
`finish.py` writes into the prefab metadata after every expansion.

Run it to regenerate vesperhold.json. The JSON is the artifact the engine reads.
"""
import json, os, pathlib, sys

HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))

from castle.layout import X, Y, Z
from castle.grid import Grid, PAL, AIR, settle_stairs, settle_rails
from castle import palette  # noqa: F401  (declares the shared roles)
from castle import terrain, approach, walls, ward, cathedral, undercroft, keep, belltower, gardens, pockets


class Step:
    def __init__(self, fn):
        self.build = fn


PARTS = [terrain, Step(ward.grounds), walls, approach, ward, cathedral, undercroft,
         keep, belltower, Step(walls.buttress_walk), gardens, pockets, Step(terrain.parapets)]


def sz(n):
    return {"size": "absolute", "blocks": {"expr": "int", "value": n}}


def split(axis, spans):
    if len(spans) == 1:
        return spans[0][1]
    return {"op": "split", "axis": axis, "sizes": [sz(n) for n, _ in spans],
            "children": [c for _, c in spans]}


VOID = {"op": "void"}


def fill(r):
    return VOID if r == AIR else {"op": "fill", "material": {"role": PAL.names[r]}}


def mark(name, facing, role, body):
    m = {"anchor": name, "at": "floor_center", "facing": facing}
    if role:
        m["role"] = role
    return {"op": "mark", "mark": m, "body": body}


# Built open, and sealed by the campaign at its first beat (GENERATION.md says why).
BUILT_OPEN = ("postern", "keep-doors", "wardens-door")


def build():
    g = Grid()
    for part in PARTS:
        part.build(g)
    for name in BUILT_OPEN:
        a, b, _ = g.gates[name]
        g.clear(a[0], b[0], a[1], b[1], a[2], b[2])
    if "--open-gates" in sys.argv:
        only = os.environ.get("OPEN_GATES")
        for name, (a, b, _) in g.gates.items():
            if only and name not in only.split(","):
                continue
            g.clear(a[0], b[0], a[1], b[1], a[2], b[2])
    settled = settle_stairs(g)
    print(f"stairs: {settled} shape(s) derived from their neighbours")
    sturdy = {PAL[n] for n in ("wall", "rock", "rock_moss", "road", "keep", "chapel", "trim",
                                "quoin", "pillar", "flag", "floor")}
    railed = settle_rails(g, sturdy)
    print(f"wall blocks: {railed} side(s) and post(s) derived from their neighbours")
    marks, bad = {}, []
    for name, (x, y, z, facing, role) in g.anchors.items():
        if name in g.furniture:
            if g.get(x, y, z) == AIR:
                bad.append(f"anchor {name} at {(x, y, z)} names furniture and holds none")
        elif name in g.points:
            if g.get(x, y, z) not in (AIR, PAL["water"]):
                bad.append(f"anchor {name} at {(x, y, z)} is inside a block")
        elif g.get(x, y, z) != AIR or g.get(x, y + 1, z) != AIR:
            bad.append(f"anchor {name} at {(x, y, z)} has no room to stand: {PAL.names[g.get(x, y, z)]}, {PAL.names[g.get(x, y + 1, z)]}")
        elif g.get(x, y - 1, z) == AIR:
            bad.append(f"anchor {name} at {(x, y, z)} stands on air")
        cell = marks.setdefault((x, z), {})
        if y in cell:
            bad.append(f"anchors {cell[y][0]} and {name} share the cell {(x, y, z)}; the partition keeps one mark a cell")
        cell[y] = (name, facing, role)
    if bad:
        raise SystemExit("\n".join(bad))

    cells = g.cells
    rows = []
    for z in range(Z):
        keys, nodes = [], []
        for x in range(X):
            spans, y = [], 0
            base = z * Y
            prev, start = None, 0
            col = bytes(cells[(base + yy) * X + x] for yy in range(Y))
            runs = []
            for yy in range(1, Y + 1):
                if yy == Y or col[yy] != col[start]:
                    runs.append((col[start], yy - start))
                    start = yy
            mk = marks.get((x, z))
            keys.append((col, tuple(sorted(mk.items())) if mk else ()))
        # merge equal columns along x
        runs_x, s = [], 0
        for x in range(1, X + 1):
            if x == X or keys[x] != keys[s]:
                runs_x.append((s, x - s))
                s = x
        row_nodes = []
        for x0, n in runs_x:
            col, mk = keys[x0]
            row_nodes.append((n, column_node(col, dict(mk))))
        rows.append((keys, row_nodes))
    z_spans, s = [], 0
    for z in range(1, Z + 1):
        if z == Z or rows[z][0] != rows[s][0]:
            z_spans.append((z - s, split("x", rows[s][1])))
            s = z
    return g, split("z", z_spans)


def column_node(col, mk):
    spans, start = [], 0
    for yy in range(1, Y + 1):
        if yy == Y or col[yy] != col[start]:
            r, n, y0 = col[start], yy - start, start
            cuts = sorted(y for y in mk if y0 <= y < y0 + n)
            y = y0
            for c in cuts:
                if c > y:
                    spans.append((c - y, fill(r)))
                name, facing, role = mk[c]
                spans.append((1, mark(name, facing, role, fill(r))))
                y = c + 1
            if y < y0 + n:
                spans.append((y0 + n - y, fill(r)))
            start = yy
    return split("y", spans)


def main():
    g, body = build()
    palette_out = {PAL.names[i]: PAL.blocks[i] for i in range(1, len(PAL.names))}
    program = {
        "version": "1.9.0",
        "name": "vesperhold",
        "start": "site",
        "params": {},
        "palette": palette_out,
        "rules": {"site": [{"weight": 1, "body": body}]},
        "shown_faces": ["north", "south", "east", "west"],
    }
    out = (pathlib.Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv
           else HERE / "vesperhold.json")
    out.write_text(json.dumps(program, separators=(",", ":")) + "\n", encoding="utf-8")
    gates = {f"anchor/gate-{k}": {"from": list(a), "to": list(b), "block": bid}
             for k, (a, b, bid) in sorted(g.gates.items())}
    if "--open-gates" not in sys.argv:
        (HERE / "gates.json").write_text(json.dumps(gates, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out.name} ({out.stat().st_size} bytes), region {X}x{Y}x{Z}, "
          f"{len(g.anchors)} anchor(s), {len(g.gates)} gate(s), {len(PAL.names) - 1} role(s)")


if __name__ == "__main__":
    main()
