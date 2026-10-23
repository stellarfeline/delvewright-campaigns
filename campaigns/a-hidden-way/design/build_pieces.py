#!/usr/bin/env python3
"""Write the three place programs of A Hidden Way.

    delvec allocation campaigns/a-hidden-way --all --prefabs prefabs > alloc.json
    python3 campaigns/a-hidden-way/design/build_pieces.py alloc.json

`delvec detail` expands `programs/<place stem>.json` inside the frame the site
plan hands each place. Each piece is stated here as a cell grid in the frame's
own coordinates (x east, y up, z south, the frame's minimum corner at 0) and
written out as a grammar program: the grid is cut along x into runs of
identical slices, each slice along z, each column along y, so every leaf is one
material over one box, wrapped in the contract region it belongs to.

The allocation is read, never copied: the frame's extent, the voids (cells the
place does not own, written as `structure_void`) and every seam's handed cells
come from it, so a plan edit is followed by re-running the two commands above.
"""
import json
import pathlib
import sys

VERSION = "1.9.0"
SKIP = "__skip__"


class Piece:
    def __init__(self, alloc):
        self.sx, self.sy, self.sz = alloc["extent"]
        self.alloc = alloc
        self.block = {}
        self.claim = {}
        self.fixed = set()
        for v in alloc["voids"]:
            (a, b) = v["cells"]
            for c in box(a, b):
                self.block[c] = SKIP
                self.fixed.add(c)

    def seam(self, edge):
        for s in self.alloc["seams"]:
            if s["edge"] == edge:
                return s
        raise KeyError(edge)

    def put(self, lo, hi, role):
        for c in box(lo, hi):
            if c in self.fixed:
                continue
            self.block[c] = role

    def claim_box(self, lo, hi, region, air_only=False):
        for c in box(lo, hi):
            if c in self.fixed or c in self.claim:
                continue
            if air_only and self.block.get(c) is not None:
                continue
            self.claim[c] = region

    def cell(self, x, y, z):
        return (self.block.get((x, y, z)), self.claim.get((x, y, z)))

    @staticmethod
    def runs(keys):
        out = []
        for k in keys:
            if out and out[-1][0] == k:
                out[-1][1] += 1
            else:
                out.append([k, 1])
        return out

    @staticmethod
    def split(axis, runs, child):
        if len(runs) == 1:
            return child(runs[0])
        return {
            "axis": axis,
            "children": [child(r) for r in runs],
            "op": "split",
            "sizes": [{"blocks": {"expr": "int", "value": n}, "size": "absolute"} for _, n in runs],
        }

    @staticmethod
    def leaf(cell):
        role, region = cell
        if role == SKIP:
            body = {"op": "skip"}
        elif role is None:
            body = {"op": "void"}
        else:
            body = {"material": {"role": role}, "op": "fill"}
        if region is None:
            return body
        return {"body": body, "op": "claim", "region": region}

    def body(self):
        def column(x, z):
            cells = [self.cell(x, y, z) for y in range(self.sy)]
            return self.split("y", self.runs(cells), lambda r: self.leaf(r[0]))

        def slab(x):
            cols = [tuple(self.cell(x, y, z) for y in range(self.sy)) for z in range(self.sz)]
            starts, z = [], 0
            for key, n in self.runs(cols):
                starts.append((key, n, z))
                z += n
            return self.split("z", [[(k, z0), n] for k, n, z0 in starts],
                              lambda r: column(x, r[0][1]))

        slabs = [tuple(tuple(self.cell(x, y, z) for y in range(self.sy)) for z in range(self.sz))
                 for x in range(self.sx)]
        starts, x = [], 0
        for key, n in self.runs(slabs):
            starts.append((key, n, x))
            x += n
        return self.split("x", [[(k, x0), n] for k, n, x0 in starts], lambda r: slab(r[0][1]))

    def shell(self, wall="wall", floor="floor", lid="lid"):
        """Floor course, walls round the ring, lid; every play cell air in `room`."""
        sx, sy, sz = self.sx, self.sy, self.sz
        self.put((0, 0, 0), (sx - 1, 0, sz - 1), floor)
        self.put((0, sy - 1, 0), (sx - 1, sy - 1, sz - 1), lid)
        for x in range(sx):
            for z in range(sz):
                if x in (0, sx - 1) or z in (0, sz - 1):
                    self.put((x, 1, z), (x, sy - 2, z), wall)
        (lo, hi) = self.alloc["space"]
        self.put(lo, hi, None)

    def opening(self, edge, region=None):
        s = self.seam(edge)
        (a, b) = s["cells"]
        self.put(a, b, None)
        self.claim_box(a, b, region or edge.split("/", 1)[1])

    def bar(self, edge, role="bar"):
        s = self.seam(edge)
        (a, b) = s["bar"]
        self.put(a, b, role)
        self.claim_box(a, b, "seam-" + edge.split("/", 1)[1])


def box(a, b):
    return [(x, y, z)
            for x in range(min(a[0], b[0]), max(a[0], b[0]) + 1)
            for y in range(min(a[1], b[1]), max(a[1], b[1]) + 1)
            for z in range(min(a[2], b[2]), max(a[2], b[2]) + 1)]


def program(name, piece, palette, contract, marks):
    body = piece.body()
    for m in marks:
        stem, pos, facing = m[0], m[1], m[2]
        mark = {
            "anchor": stem, "at": "offset", "facing": facing,
            "x": {"expr": "int", "value": pos[0]},
            "y": {"expr": "int", "value": pos[1]},
            "z": {"expr": "int", "value": pos[2]},
        }
        if len(m) > 3:
            mark["role"] = m[3]
        body = {"body": body, "mark": mark, "op": "mark"}
    return {
        "contract": contract,
        "name": name,
        "palette": palette,
        "params": {},
        "rules": {"place": [{"body": body, "weight": 1}]},
        "shown_faces": [],
        "start": "place",
        "version": VERSION,
    }

HANGING = "minecraft:lantern[hanging=true,waterlogged=false]"
CHAIN = "minecraft:iron_chain[axis=y,waterlogged=false]"
BASE = {
    "chain": CHAIN,
    "floor": "minecraft:polished_andesite",
    "hanging": HANGING,
    "lid": "minecraft:dark_oak_planks",
    "wall": "minecraft:stone_bricks",
}


def lamps(p, cells, top):
    """Hanging lanterns at `cells`, each on a chain up to the course under `top`."""
    for (x, y, z) in cells:
        p.put((x, y, z), (x, y, z), "hanging")
        if y + 1 <= top:
            p.put((x, y + 1, z), (x, top, z), "chain")


def hall(a):
    p = Piece(a)
    p.shell()
    top = p.sy - 2
    # The great hearth in the north wall: its mouth is the way into the
    # passage, three wide, and the brick back of the firebox is the way's own
    # bar — a block the eye cannot see through, so nothing behind it shows
    # until the beat opens it. The recess before the back is the mouth's
    # approach, two high under the mantel; the fire burns on the hearth stone
    # before the recess, between the cheeks, and is a gate of its own the same
    # beat clears. Cheeks, mantel and chimney breast stand beside and above
    # the mouth.
    p.bar("edge/hearth-door")
    p.put((2, 1, 1), (2, 2, 2), "masonry")
    p.put((6, 1, 1), (6, 2, 2), "masonry")
    p.put((2, 3, 1), (6, 3, 2), "mantel")
    p.put((2, 4, 1), (6, top, 2), "masonry")
    p.claim_box((3, 1, 1), (5, 2, 1), "hearth")
    p.put((3, 1, 2), (5, 1, 2), "fire")
    p.claim_box((3, 1, 2), (5, 1, 2), "hearth-fire")
    # The porch door in the south wall.
    p.opening("edge/porch-door")
    lamps(p, [(1, 5, 4), (8, 6, 3), (11, 5, 8), (5, 6, 8), (9, 6, 6)], top)
    p.claim_box((1, 1, 1), (p.sx - 2, top, p.sz - 2), "room", air_only=True)
    palette = dict(BASE, **{
        "bar": "minecraft:bricks",
        "fire": "minecraft:campfire[facing=north,lit=true,signal_fire=false,waterlogged=false]",
        "mantel": "minecraft:polished_deepslate",
        "masonry": "minecraft:stone_bricks",
    })
    contract = {
        "edges": [
            {"a": "room", "b": "exterior", "class": "walk", "via": "porch-door"},
            {"a": "room", "b": "hearth", "bar": {"block": "fire", "region": "hearth-fire"}, "class": "barred"},
            {"a": "hearth", "b": "exterior", "bar": {"block": "bar", "region": "seam-hearth-door"}, "class": "barred"},
        ],
        "entry": "room",
        "spaces": {"hearth": {"envelope": "enclosed"}, "room": {"envelope": "enclosed"}},
    }
    marks = [
        ("node-hall", (6, 1, 7), "north"),
        ("valve", (p.sx - 2, 2, 5), "west"),
    ]
    return program("a-hidden-way-hall", p, palette, contract, marks)


def passage(a):
    p = Piece(a)
    p.shell()
    p.opening("edge/hearth-door")
    # The keeper's shelves at the passage's far end.
    p.put((1, 1, 1), (1, 2, 1), "shelf")
    p.put((3, 1, 1), (3, 2, 1), "shelf")
    p.put((2, 1, 1), (2, 1, 1), "lectern")
    lamps(p, [(2, 3, 4), (2, 3, 8)], 3)
    p.claim_box((1, 1, 1), (3, 3, p.sz - 2), "room", air_only=True)
    palette = dict(BASE, **{
        "lectern": "minecraft:lectern[facing=south,has_book=false,powered=false]",
        "shelf": "minecraft:bookshelf",
    })
    contract = {
        "edges": [{"a": "room", "b": "exterior", "class": "walk", "via": "hearth-door"}],
        "entry": "room",
        "spaces": {"room": {"envelope": "enclosed"}},
    }
    marks = [("node-passage", (2, 1, 6), "north")]
    return program("a-hidden-way-passage", p, palette, contract, marks)


def porch(a):
    p = Piece(a)
    p.shell()
    p.opening("edge/porch-door")
    lamps(p, [(3, 3, 2)], 4)
    p.claim_box((1, 1, 1), (5, 4, 4), "room", air_only=True)
    contract = {
        "edges": [{"a": "room", "b": "exterior", "class": "walk", "via": "porch-door"}],
        "entry": "room",
        "spaces": {"room": {"envelope": "enclosed"}},
    }
    marks = [("spawn", (3, 1, 3), "north", "entry"), ("node-porch", (2, 1, 2), "north")]
    return program("a-hidden-way-porch", p, dict(BASE), contract, marks)


def main():
    alloc = {a["place"]: a for a in json.loads(pathlib.Path(sys.argv[1]).read_text())}
    here = pathlib.Path(__file__).resolve().parent.parent
    out = here / "programs"
    out.mkdir(exist_ok=True)
    for stem, build in (("porch", porch), ("hall", hall), ("passage", passage)):
        prog = build(alloc[f"node/{stem}"])
        path = out / f"{stem}.json"
        path.write_text(json.dumps(prog, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
