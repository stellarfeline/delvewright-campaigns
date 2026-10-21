#!/usr/bin/env python3
"""Write the six place programs of Three Ways Shut.

    delvec allocation campaigns/three-ways-shut --all --prefabs prefabs > alloc.json
    python3 campaigns/three-ways-shut/design/build_pieces.py alloc.json

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


BAR = "minecraft:iron_bars[east=false,north=false,south=false,waterlogged=false,west=false]"
HATCH = "minecraft:iron_trapdoor[facing=north,half=top,open=false,powered=false,waterlogged=false]"
HANGING = "minecraft:lantern[hanging=true,waterlogged=false]"
STANDING = "minecraft:lantern[hanging=false,waterlogged=false]"
CHAIN = "minecraft:iron_chain[axis=y,waterlogged=false]"
BASE = {
    "bar": BAR,
    "chain": CHAIN,
    "floor": "minecraft:cobblestone",
    "hanging": HANGING,
    "lid": "minecraft:spruce_planks",
    "standing": STANDING,
    "wall": "minecraft:stone_bricks",
}


def lamps(p, cells, top):
    """Hanging lanterns at `cells`, each on a chain up to the course under `top`."""
    for (x, y, z) in cells:
        p.put((x, y, z), (x, y, z), "hanging")
        if y + 1 <= top:
            p.put((x, y + 1, z), (x, top, z), "chain")


def yard(a):
    p = Piece(a)
    p.shell()
    # The arch to the court: bars in the far wall, seen across the yard.
    p.bar("edge/court-arch")
    # The passage door: an open doorway in the east wall.
    p.opening("edge/passage-door")
    # The keeper's stair up the wall beside the gate: four treads rising
    # west at z 12..14, a landing at y 5 under the opening into the ledge.
    treads = [(9, 1), (8, 2), (7, 3), (6, 4)]
    for x, y in treads:
        p.put((x, y, 12), (x, y, 14), "tread")
        if y > 1:
            p.put((x, 1, 12), (x, y - 1, 14), "masonry")
    p.put((2, 1, 12), (5, 5, 14), "masonry")
    for x, y in treads:
        p.claim_box((x, y, 12), (x, 9, 14), "keeper-flight")
    p.claim_box((2, 6, 12), (5, 9, 14), "landing")
    p.opening("edge/keeper-stair")
    # The cart road's mouth in the same wall: its bars, a one-cell recess in
    # front of them, and the timber barricade across the recess.
    p.bar("edge/cart-road")
    p.put((10, 1, 14), (12, 3, 14), "masonry")
    p.put((11, 1, 14), (11, 2, 14), None)
    p.claim_box((11, 1, 14), (11, 2, 14), "mouth")
    p.put((10, 3, 14), (12, 9, 14), "masonry")
    p.put((10, 4, 13), (12, 9, 13), "masonry")
    p.put((10, 1, 13), (12, 3, 13), "barricade")
    p.claim_box((10, 1, 13), (12, 3, 13), "barricade")
    # Lanterns hung from the roof beams, clear of the line from the gate side
    # to the arch.
    lamps(p, [(3, 7, 3), (14, 7, 3), (3, 7, 9), (14, 7, 9), (9, 8, 6)], 9)
    p.claim_box((1, 1, 1), (16, 9, 14), "room", air_only=True)
    palette = dict(BASE, **{
        "barricade": "minecraft:stripped_spruce_log[axis=x]",
        "masonry": "minecraft:stone_bricks",
        "tread": "minecraft:stone_brick_stairs[facing=west,half=bottom,shape=straight,waterlogged=false]",
    })
    contract = {
        "edges": [
            {"a": "room", "b": "exterior", "bar": {"block": "bar", "region": "seam-court-arch"}, "class": "barred"},
            {"a": "room", "b": "exterior", "class": "walk", "via": "passage-door"},
            {"a": "room", "b": "landing", "class": "stair", "rise": 5, "via": "keeper-flight"},
            {"a": "landing", "b": "exterior", "class": "walk", "via": "keeper-stair"},
            {"a": "room", "b": "mouth", "bar": {"block": "barricade", "region": "barricade"}, "class": "barred"},
            {"a": "mouth", "b": "exterior", "bar": {"block": "bar", "region": "seam-cart-road"}, "class": "barred"},
        ],
        "entry": "room",
        "spaces": {"landing": {"envelope": "open"}, "mouth": {"envelope": "enclosed"}, "room": {"envelope": "enclosed"}},
    }
    marks = [
        ("spawn", (13, 1, 11), "north", "entry"),
        ("node-yard", (9, 1, 8), "north"),
    ]
    return program("three-ways-shut-yard", p, palette, contract, marks)


def court(a):
    p = Piece(a)
    p.shell()
    # The court has no wall of its own on the yard's side: the yard's wall.
    p.opening("edge/court-arch")
    lamps(p, [(3, 4, 3), (8, 4, 3), (5, 4, 6)], 5)
    p.put((4, 1, 1), (6, 1, 1), "bench")
    p.claim_box((1, 1, 1), (10, 5, 8), "room", air_only=True)
    palette = dict(BASE, **{"bench": "minecraft:spruce_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]"})
    contract = {
        "edges": [{"a": "room", "b": "exterior", "class": "walk", "via": "court-arch"}],
        "entry": "room",
        "spaces": {"room": {"envelope": "enclosed"}},
    }
    marks = [("node-court", (5, 1, 4), "north")]
    return program("three-ways-shut-court", p, palette, contract, marks)


def passage(a):
    p = Piece(a)
    p.shell()
    # Three wide: the far two rows are wall.
    p.put((0, 1, 4), (7, 4, 5), "wall")
    p.opening("edge/passage-door")
    p.bar("edge/toll-door")
    lamps(p, [(4, 4, 1)], 4)
    p.claim_box((0, 1, 1), (7, 4, 3), "room", air_only=True)
    contract = {
        "edges": [
            {"a": "room", "b": "exterior", "class": "walk", "via": "passage-door"},
            {"a": "room", "b": "exterior", "bar": {"block": "bar", "region": "seam-toll-door"}, "class": "barred"},
        ],
        "entry": "room",
        "spaces": {"room": {"envelope": "enclosed"}},
    }
    marks = [("node-passage", (4, 1, 2), "east")]
    return program("three-ways-shut-passage", p, dict(BASE), contract, marks)


def hall(a):
    p = Piece(a)
    p.shell()
    p.opening("edge/toll-door")
    p.opening("edge/road-end")
    lamps(p, [(3, 4, 3), (8, 4, 3), (3, 4, 11), (8, 4, 11)], 5)
    p.put((9, 1, 9), (10, 1, 12), "desk")
    p.claim_box((1, 1, 1), (10, 5, 14), "room", air_only=True)
    palette = dict(BASE, **{"desk": "minecraft:spruce_planks"})
    contract = {
        "edges": [
            {"a": "room", "b": "exterior", "class": "walk", "via": "toll-door"},
            {"a": "room", "b": "exterior", "class": "walk", "via": "road-end"},
        ],
        "entry": "room",
        "spaces": {"room": {"envelope": "enclosed"}},
    }
    marks = [
        ("node-hall", (5, 1, 7), "west"),
        ("arch-lever", (9, 1, 4), "north"),
        ("unlock-toll-door", (3, 1, 7), "west"),
    ]
    return program("three-ways-shut-hall", p, palette, contract, marks)


def ledge(a):
    p = Piece(a)
    p.shell()
    p.opening("edge/keeper-stair")
    p.bar("edge/keeper-hatch", "hatch")
    p.put((5, 1, 2), (5, 1, 2), "chest")
    p.claim_box((5, 1, 2), (5, 1, 2), "room")
    for x, z in ((1, 4), (8, 4), (8, 0)):
        p.put((x, 1, z), (x, 1, z), "standing")
    p.claim_box((1, 1, 0), (8, 3, 4), "room", air_only=True)
    palette = dict(BASE, **{
        "chest": "minecraft:chest[facing=west,type=single,waterlogged=false]",
        "floor": "minecraft:spruce_planks",
        "hatch": HATCH,
    })
    contract = {
        "edges": [
            {"a": "room", "b": "exterior", "class": "walk", "via": "keeper-stair"},
            {"a": "room", "b": "exterior", "bar": {"block": "hatch", "region": "seam-keeper-hatch"}, "class": "barred"},
        ],
        "entry": "room",
        "spaces": {"room": {"envelope": "enclosed"}},
    }
    marks = [
        ("node-ledge", (2, 1, 3), "east"),
        ("key-chest", (5, 1, 2), "west"),
    ]
    return program("three-ways-shut-ledge", p, palette, contract, marks)


def corridor(a):
    p = Piece(a)
    p.shell()
    # Five wide under the keeper's walk, where the hatch drops in; three wide
    # beyond it, the far two rows wall.
    p.put((10, 1, 4), (34, 4, 5), "wall")
    p.opening("edge/keeper-hatch")
    p.opening("edge/cart-road")
    p.opening("edge/road-end")
    lamps(p, [(x, 4, 2) for x in (7, 14, 20, 26, 32)], 4)
    p.claim_box((1, 1, 1), (34, 4, 5), "room", air_only=True)
    contract = {
        "edges": [
            {"a": "room", "b": "exterior", "class": "walk", "via": "keeper-hatch"},
            {"a": "room", "b": "exterior", "class": "walk", "via": "cart-road"},
            {"a": "room", "b": "exterior", "class": "walk", "via": "road-end"},
        ],
        "entry": "room",
        "spaces": {"room": {"envelope": "enclosed"}},
    }
    marks = [("node-corridor", (20, 1, 2), "east")]
    return program("three-ways-shut-corridor", p, dict(BASE), contract, marks)


def main():
    alloc = {a["place"]: a for a in json.loads(pathlib.Path(sys.argv[1]).read_text())}
    here = pathlib.Path(__file__).resolve().parent.parent
    out = here / "programs"
    out.mkdir(exist_ok=True)
    for stem, build in (("yard", yard), ("court", court), ("passage", passage),
                        ("hall", hall), ("ledge", ledge), ("corridor", corridor)):
        prog = build(alloc[f"node/{stem}"])
        path = out / f"{stem}.json"
        path.write_text(json.dumps(prog, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
