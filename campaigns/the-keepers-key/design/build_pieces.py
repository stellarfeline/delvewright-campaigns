#!/usr/bin/env python3
"""Write the four place programs of The Keeper's Key.

    delvec allocation campaigns/the-keepers-key --all > alloc.json
    python3 campaigns/the-keepers-key/design/build_pieces.py alloc.json

`delvec detail` expands `programs/<place stem>.json` inside the frame the site
plan hands each place. Each piece is stated here as a cell grid in the frame's
own coordinates (x east, y up, z south, the frame's minimum corner at 0) and
written out as a grammar program. The pieces hold only what the hand cannot
work: walls, floors, the table, the hearth's hood, the punt, the lamps, and the
store door, which the hall owns because the door stands in the hall's wall.
"""
import json
import pathlib
import sys

VERSION = "1.13.0"
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
        """Floor course, walls round the ring, lid; every play cell air."""
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


ALL_SIDES = ("east", "north", "south", "up", "west")


def program(name, piece, palette, contract, marks, shown=ALL_SIDES):
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
        "shown_faces": sorted(shown),
        "start": "place",
        "version": VERSION,
    }


BAR = "minecraft:iron_bars[east=false,north=false,south=false,waterlogged=false,west=false]"
HANGING = "minecraft:lantern[hanging=true,waterlogged=false]"
CHAIN = "minecraft:iron_chain[axis=y,waterlogged=false]"
BASE = {
    "bar": BAR,
    "chain": CHAIN,
    "floor": "minecraft:spruce_planks",
    "hanging": HANGING,
    "lid": "minecraft:spruce_planks",
    "wall": "minecraft:stone_bricks",
}


def lamps(p, cells, top):
    """Hanging lanterns at `cells`, each on a chain up to the course under `top`."""
    for (x, y, z) in cells:
        p.put((x, y, z), (x, y, z), "hanging")
        if y + 1 <= top:
            p.put((x, y + 1, z), (x, top, z), "chain")


def yard(a):
    """The yard, open to the sky: cobbles, walls of the play space's full
    height on its own ring cells, lamps set flush in the ground."""
    p = Piece(a)
    sx, sy, sz = p.sx, p.sy, p.sz
    top = a["space"][1][1]
    p.put((0, 0, 0), (sx - 1, 0, sz - 1), "floor")
    for x in range(sx):
        for z in range(sz):
            if x in (0, sx - 1) or z in (0, sz - 1):
                p.put((x, 1, z), (x, top, z), "wall")
    (lo, hi) = a["space"]
    p.put(lo, hi, None)
    p.opening("edge/hall-door")
    p.opening("edge/shed-gate")
    for (x, z) in ((3, 4), (13, 4), (3, 10), (13, 10)):
        p.put((x, 0, z), (x, 0, z), "glow")
    p.claim_box((1, 1, 1), (sx - 2, top, sz - 2), "yard", air_only=True)
    palette = dict(BASE, **{
        "floor": "minecraft:cobblestone",
        "glow": "minecraft:sea_lantern",
        "wall": "minecraft:mossy_stone_bricks",
    })
    contract = {
        "edges": [
            {"a": "yard", "b": "exterior", "class": "walk", "via": "hall-door"},
            {"a": "yard", "b": "exterior", "class": "walk", "via": "shed-gate"},
        ],
        "entry": "yard",
        "spaces": {"yard": {"envelope": "open"}},
    }
    marks = [("spawn", (8, 1, 8), "north", "entry"), ("node-yard", (8, 1, 6), "north")]
    return program("the-keepers-key-yard", p, palette, contract, marks)


def door(facing, half):
    return f"minecraft:oak_door[facing={facing},half={half},hinge=left,open=false,powered=false]"


def hall(a):
    p = Piece(a)
    p.shell()
    p.opening("edge/hall-door")
    # The store door stands in the hall's own east wall: the leaf in the
    # seam's plane, its two halves the gate region the hall owes.
    s = p.seam("edge/store-door")
    (lo, hi) = s["bar"]
    p.put(lo, lo, "door")
    p.put(hi, hi, "door-top")
    p.claim_box(lo, hi, "seam-store-door")
    # The keeper's table along the north wall.
    p.put((4, 1, 2), (6, 1, 2), "table")
    # The hearth in the west wall: a hood of brick over the fire.
    p.put((1, 3, 7), (1, 5, 9), "brick")
    p.put((1, 0, 8), (1, 0, 8), "hearthstone")
    lamps(p, [(3, 4, 3), (9, 4, 3), (6, 4, 7), (10, 4, 8)], 5)
    p.claim_box((1, 1, 1), (12, 5, 10), "room", air_only=True)
    facing = s["bar_block"].split("facing=")[1].split(",")[0]
    palette = dict(BASE, **{
        "brick": "minecraft:bricks",
        "door": door(facing, "lower"),
        "door-top": door(facing, "upper"),
        "floor": "minecraft:polished_andesite",
        "hearthstone": "minecraft:smooth_stone",
        "table": "minecraft:spruce_planks",
    })
    contract = {
        "edges": [
            {"a": "room", "b": "exterior", "class": "walk", "via": "hall-door"},
            {"a": "room", "b": "exterior", "bar": {"block": "door", "region": "seam-store-door"}, "class": "barred"},
        ],
        "entry": "room",
        "spaces": {"room": {"envelope": "enclosed"}},
    }
    marks = [
        ("node-hall", (7, 1, 7), "north"),
        ("keeper", (5, 1, 3), "south"),
        ("hearth", (1, 1, 8), "east"),
        ("unlock-store-door", (12, 1, 6), "east"),
    ]
    return program("the-keepers-key-hall", p, palette, contract, marks)


def store(a):
    p = Piece(a)
    p.shell()
    p.opening("edge/store-door")
    # Hay and sacks in the corner by the door.
    p.put((1, 1, 9), (2, 1, 10), "hay")
    p.put((5, 1, 1), (6, 1, 1), "sacks")
    lamps(p, [(3, 3, 3), (3, 3, 8)], 4)
    p.claim_box((0, 1, 1), (6, 4, 10), "room", air_only=True)
    palette = dict(BASE, **{
        "hay": "minecraft:hay_block[axis=y]",
        "sacks": "minecraft:brown_wool",
    })
    contract = {
        "edges": [{"a": "room", "b": "exterior", "class": "walk", "via": "store-door"}],
        "entry": "room",
        "spaces": {"room": {"envelope": "enclosed"}},
    }
    marks = [
        ("node-store", (3, 1, 5), "east"),
        ("lever", (6, 2, 5), "west"),
    ]
    return program("the-keepers-key-store", p, palette, contract, marks)


def shed(a):
    p = Piece(a)
    p.shell()
    p.bar("edge/shed-gate")
    # The ford's punt on its stocks, bow to the far wall.
    p.put((5, 1, 3), (5, 1, 6), "hull-west")
    p.put((7, 1, 3), (7, 1, 6), "hull-east")
    p.put((6, 1, 3), (6, 1, 6), "keel")
    p.put((6, 1, 7), (6, 1, 7), "bow")
    lamps(p, [(3, 3, 2), (6, 3, 4)], 4)
    p.claim_box((1, 1, 1), (8, 4, 7), "room", air_only=True)
    palette = dict(BASE, **{
        "bow": "minecraft:spruce_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]",
        "floor": "minecraft:cobblestone",
        "hull-east": "minecraft:spruce_stairs[facing=west,half=bottom,shape=straight,waterlogged=false]",
        "hull-west": "minecraft:spruce_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]",
        "keel": "minecraft:spruce_slab[type=bottom,waterlogged=false]",
    })
    contract = {
        "edges": [{"a": "room", "b": "exterior", "bar": {"block": "bar", "region": "seam-shed-gate"}, "class": "barred"}],
        "entry": "room",
        "spaces": {"room": {"envelope": "enclosed"}},
    }
    (lo, hi) = p.seam("edge/shed-gate")["bar"]
    marks = [("node-shed", (3, 1, 4), "north"),
             ("shed-gate-low", tuple(lo), "north"), ("shed-gate-high", tuple(hi), "north")]
    return program("the-keepers-key-shed", p, palette, contract, marks)


def main():
    alloc = {a["place"]: a for a in json.loads(pathlib.Path(sys.argv[1]).read_text())}
    here = pathlib.Path(__file__).resolve().parent.parent
    out = here / "programs"
    out.mkdir(exist_ok=True)
    for stem, build in (("yard", yard), ("hall", hall), ("store", store), ("shed", shed)):
        prog = build(alloc[f"node/{stem}"])
        path = out / f"{stem}.json"
        path.write_text(json.dumps(prog, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
