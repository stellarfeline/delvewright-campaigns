#!/usr/bin/env python3
"""Write the four place programs of Three Buttons and a Bell.

    delvec allocation campaigns/three-buttons-and-a-bell --all --prefabs prefabs > alloc.json
    python3 campaigns/three-buttons-and-a-bell/design/build_pieces.py alloc.json

`delvec detail` expands `programs/<place stem>.json` inside the frame the site
plan hands each place. Each piece is stated here as a cell grid in the frame's
own coordinates (x east, y up, z south, the frame's minimum corner at 0) and
written out as a grammar program: the grid is cut along x into runs of
identical slices, each slice along z, each column along y, so every leaf is one
material over one box, wrapped in the contract region it belongs to.

The allocation is read, never copied: the frame's extent, the voids (cells the
place does not own, written as `structure_void`) and every seam's handed cells
come from it, so a plan edit is followed by re-running the two commands above.

Nothing a player could press is placed by a piece: every pressable block (the
bell, the store door, the chest, the lever, the buttons, the bolt, the candles,
the boulder) is the campaign's `prop`, laid by the engine at its anchor. The
pieces hold only what the hand cannot work: walls, floors, the counter, the
bell's post, the boat on its stocks, the lamps.
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
HANGING = "minecraft:lantern[hanging=true,waterlogged=false]"
STANDING = "minecraft:lantern[hanging=false,waterlogged=false]"
CHAIN = "minecraft:iron_chain[axis=y,waterlogged=false]"
BASE = {
    "bar": BAR,
    "chain": CHAIN,
    "floor": "minecraft:spruce_planks",
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


def jetty(a):
    p = Piece(a)
    p.shell()
    # The doorway into the keeper's hall, open.
    p.opening("edge/hall-door")
    # The store's door onto the jetty: two wide, boarded and barred from the
    # store's side. Its boards are the shortcut's bar.
    p.bar("edge/jetty-door", "boards")
    # Mooring posts along the jetty's open edge, where the boats tie up.
    p.put((1, 1, 7), (16, 1, 7), "rail")
    for x in (3, 7, 11, 15):
        p.put((x, 1, 7), (x, 1, 7), "post")
    lamps(p, [(4, 3, 3), (10, 3, 4), (14, 3, 3)], 4)
    p.claim_box((1, 1, 1), (16, 4, 7), "room", air_only=True)
    palette = dict(BASE, **{
        "boards": "minecraft:dark_oak_planks",
        "post": "minecraft:stripped_spruce_log[axis=y]",
        "rail": "minecraft:spruce_fence[east=true,north=false,south=false,waterlogged=false,west=true]",
    })
    contract = {
        "edges": [
            {"a": "room", "b": "exterior", "class": "walk", "via": "hall-door"},
            {"a": "room", "b": "exterior", "bar": {"block": "boards", "region": "seam-jetty-door"}, "class": "barred"},
        ],
        "entry": "room",
        "spaces": {"room": {"envelope": "enclosed"}},
    }
    marks = [
        ("spawn", (8, 1, 5), "north", "entry"),
        ("node-jetty", (8, 1, 4), "north"),
        ("jetty-door-leaf", (15, 2, 0), "south"),
    ]
    return program("three-buttons-and-a-bell-jetty", p, palette, contract, marks)


def hall(a):
    p = Piece(a)
    p.shell()
    p.opening("edge/hall-door")
    p.opening("edge/store-door", "store-doorway")
    p.bar("edge/shed-gate")
    # The keeper's counter, one block high, open at both ends so the lever
    # on the wall behind her is reached round it.
    p.put((7, 1, 6), (9, 1, 6), "counter")
    # A hearth in the corner by the candles: a hood of brick over it.
    p.put((11, 1, 12), (12, 1, 12), "hearth")
    p.put((11, 3, 12), (12, 5, 12), "brick")
    lamps(p, [(3, 4, 3), (10, 4, 3), (6, 4, 7), (3, 4, 11), (10, 4, 9)], 5)
    p.claim_box((1, 1, 1), (12, 5, 12), "room", air_only=True)
    palette = dict(BASE, **{
        "brick": "minecraft:bricks",
        "counter": "minecraft:spruce_planks",
        "floor": "minecraft:polished_andesite",
        "hearth": "minecraft:smooth_stone",
    })
    contract = {
        "edges": [
            {"a": "room", "b": "exterior", "class": "walk", "via": "hall-door"},
            {"a": "room", "b": "exterior", "class": "walk", "via": "store-doorway"},
            {"a": "room", "b": "exterior", "bar": {"block": "bar", "region": "seam-shed-gate"}, "class": "barred"},
        ],
        "entry": "room",
        "spaces": {"room": {"envelope": "enclosed"}},
    }
    marks = [
        ("node-hall", (5, 1, 9), "north"),
        ("keeper", (8, 1, 4), "south"),
        ("lever", (8, 2, 1), "south"),
        ("bell", (3, 1, 9), "east"),
        ("store-door", (12, 1, 5), "west"),
        ("chest", (12, 1, 9), "west"),
        ("bolt", (6, 1, 1), "south"),
        ("button-one", (1, 1, 3), "east"),
        ("button-two", (1, 1, 5), "east"),
        ("button-three", (1, 1, 7), "east"),
        ("candles", (10, 1, 11), "north"),
        ("boulder", (1, 1, 11), "east"),
    ]
    return program("three-buttons-and-a-bell-hall", p, palette, contract, marks)


def store(a):
    p = Piece(a)
    p.shell()
    p.opening("edge/store-door", "store-doorway")
    p.opening("edge/jetty-door")
    # A shelf of slabs along the far wall, a lantern standing on it.
    p.put((5, 3, 3), (5, 3, 8), "shelf")
    p.put((5, 4, 5), (5, 4, 5), "standing")
    lamps(p, [(2, 3, 3), (2, 3, 9)], 4)
    p.claim_box((0, 1, 1), (5, 4, 12), "room", air_only=True)
    palette = dict(BASE, **{
        "floor": "minecraft:spruce_planks",
        "shelf": "minecraft:spruce_slab[type=top,waterlogged=false]",
    })
    contract = {
        "edges": [
            {"a": "room", "b": "exterior", "class": "walk", "via": "store-doorway"},
            {"a": "room", "b": "exterior", "class": "walk", "via": "jetty-door"},
        ],
        "entry": "room",
        "spaces": {"room": {"envelope": "enclosed"}},
    }
    marks = [
        ("node-store", (2, 1, 6), "south"),
        ("unlock-jetty-door", (3, 2, 12), "north"),
    ]
    return program("three-buttons-and-a-bell-store", p, palette, contract, marks)


def shed(a):
    p = Piece(a)
    p.shell()
    p.opening("edge/shed-gate")
    # The keeper's boat on its stocks: a hull of spruce, bow to the far wall.
    p.put((5, 1, 2), (5, 1, 5), "hull-west")
    p.put((7, 1, 2), (7, 1, 5), "hull-east")
    p.put((6, 1, 2), (6, 1, 5), "keel")
    p.put((6, 1, 1), (6, 1, 1), "bow")
    lamps(p, [(3, 3, 2), (6, 3, 4)], 4)
    p.claim_box((1, 1, 1), (8, 4, 6), "room", air_only=True)
    palette = dict(BASE, **{
        "bow": "minecraft:spruce_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]",
        "floor": "minecraft:cobblestone",
        "hull-east": "minecraft:spruce_stairs[facing=west,half=bottom,shape=straight,waterlogged=false]",
        "hull-west": "minecraft:spruce_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]",
        "keel": "minecraft:spruce_slab[type=bottom,waterlogged=false]",
    })
    contract = {
        "edges": [{"a": "room", "b": "exterior", "class": "walk", "via": "shed-gate"}],
        "entry": "room",
        "spaces": {"room": {"envelope": "enclosed"}},
    }
    marks = [("node-shed", (3, 1, 4), "north")]
    return program("three-buttons-and-a-bell-shed", p, palette, contract, marks)


def main():
    alloc = {a["place"]: a for a in json.loads(pathlib.Path(sys.argv[1]).read_text())}
    here = pathlib.Path(__file__).resolve().parent.parent
    out = here / "programs"
    out.mkdir(exist_ok=True)
    for stem, build in (("jetty", jetty), ("hall", hall), ("store", store), ("shed", shed)):
        prog = build(alloc[f"node/{stem}"])
        path = out / f"{stem}.json"
        path.write_text(json.dumps(prog, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
