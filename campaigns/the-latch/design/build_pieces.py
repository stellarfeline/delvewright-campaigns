#!/usr/bin/env python3
"""Write the four place programs of The Latch.

    delvec allocation campaigns/the-latch --all > alloc.json
    python3 campaigns/the-latch/design/build_pieces.py alloc.json

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


def program(name, piece, palette, contract, marks, shown=()):
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

HANGING = "minecraft:lantern[hanging=true,waterlogged=false]"
STANDING = "minecraft:lantern[hanging=false,waterlogged=false]"

LANTERN = "minecraft:lantern[hanging=false,waterlogged=false]"
HANGING = "minecraft:lantern[hanging=true,waterlogged=false]"
HEDGE = "minecraft:oak_leaves[distance=1,persistent=true,waterlogged=false]"
POST = "minecraft:mossy_cobblestone_wall[east=none,north=none,south=none,up=true,waterlogged=false,west=none]"


def door(facing, half, hinge="left", kind="oak"):
    return f"minecraft:{kind}_door[facing={facing},half={half},hinge={hinge},open=false,powered=false]"


def lamp_post(p, x, z):
    p.put((x, 1, z), (x, 1, z), "post")
    p.put((x, 2, z), (x, 2, z), "lantern")


def claim_tops(p, region="tops"):
    """Claim every air cell standing on a block of the hedge or a lamp into an
    out-of-walk region: the top of a hedge or a lantern is not floor anyone
    walks."""
    for (x, y, z), role in list(p.block.items()):
        if role in ("hedge", "lantern") and p.block.get((x, y + 1, z)) is None:
            p.claim_box((x, y + 1, z), (x, y + 1, z), region)


def hedge_ring(p, sides):
    """Leaves two high on the ring cells of `sides` ('west', 'east', 'north', 'south')."""
    sx, sz = p.sx, p.sz
    for x in range(sx):
        for z in range(sz):
            ring = ((x == 0 and "west" in sides) or (x == sx - 1 and "east" in sides)
                    or (z == 0 and "north" in sides) or (z == sz - 1 and "south" in sides))
            if ring:
                p.put((x, 1, z), (x, 2, z), "hedge")


def yard(a):
    p = Piece(a)
    sx, sy, sz = p.sx, p.sy, p.sz
    p.put((0, 0, 0), (sx - 1, 0, sz - 1), "grass")
    p.put((3, 0, 0), (3, 0, sz - 2), "path")
    hedge_ring(p, ("west", "east", "south"))
    # The hedge across the yard with its wooden gate on the path.
    p.put((1, 1, 3), (sx - 2, 2, 3), "hedge")
    p.put((3, 1, 3), (3, 2, 3), None)
    p.put((3, 1, 3), (3, 1, 3), "gate")
    p.claim_box((3, 1, 3), (3, 2, 3), "yard-gate")
    p.opening("edge/front-door")
    for (x, z) in ((2, 1), (8, 1), (2, 6), (8, 6)):
        lamp_post(p, x, z)
    claim_tops(p)
    p.claim_box((1, 1, 0), (sx - 2, sy - 1, 2), "porch", air_only=True)
    p.claim_box((1, 1, 4), (sx - 2, sy - 1, 6), "front", air_only=True)
    p.claim_box((1, 3, 3), (sx - 2, sy - 1, 3), "front", air_only=True)
    palette = {
        "gate": "minecraft:oak_fence_gate[facing=north,in_wall=false,open=false,powered=false]",
        "grass": "minecraft:grass_block[snowy=false]",
        "hedge": HEDGE,
        "lantern": LANTERN,
        "path": "minecraft:dirt_path",
        "post": POST,
    }
    contract = {
        "edges": [
            {"a": "front", "b": "porch", "class": "walk", "via": "yard-gate"},
            {"a": "porch", "b": "exterior", "class": "walk", "via": "front-door"},
        ],
        "entry": "porch",
        "no_body": {"tops": {"reason": "the tops of the hedges and the lamps, which nobody walks"}},
        "spaces": {"front": {"envelope": "open"}, "porch": {"envelope": "open"}},
    }
    marks = [("spawn", (3, 1, 5), "north", "entry"), ("node-yard", (5, 1, 5), "north")]
    return program("the-latch-yard", p, palette, contract, marks, ("east", "south", "west"))


def cottage(a):
    p = Piece(a)
    sx, sy, sz = p.sx, p.sy, p.sz
    p.put((0, 0, 0), (sx - 1, 0, sz - 1), "floor")
    p.put((0, sy - 1, 0), (sx - 1, sy - 1, sz - 1), "lid")
    for x in range(sx):
        for z in range(sz):
            if x in (0, sx - 1) or z in (0, sz - 1):
                p.put((x, 1, z), (x, sy - 2, z), "wall")
    (lo, hi) = p.alloc["space"]
    p.put(lo, hi, None)
    # The wall between the two rooms, and the oak door in it.
    p.put((6, 1, 1), (6, sy - 2, sz - 2), "wall")
    p.put((6, 1, 3), (6, 1, 3), "inner-door")
    p.put((6, 2, 3), (6, 2, 3), "inner-door-top")
    p.claim_box((6, 1, 3), (6, 2, 3), "inner-door")
    # The front door from the yard into the kitchen.
    fd = p.seam("edge/front-door")
    (f0, f1) = fd["cells"]
    p.put(f0, f0, "front-door")
    p.put(f1, f1, "front-door-top")
    p.claim_box(f0, f1, "front-door")
    # The iron door to the garden: the way's own bar, shipped shut. The bar
    # is declared as the door's lower half; its upper half stands over it, and
    # the engine derives the same two states for the gate region.
    gd = p.seam("edge/garden-door")
    (g0, g1) = sorted(gd["bar"], key=lambda c: c[1])
    assert g0[1] + 1 == g1[1] and (g0[0], g0[2]) == (g1[0], g1[2]), gd["bar"]
    p.put(g0, g0, "garden-door")
    p.put(g1, g1, "garden-door-top")
    p.claim_box(g0, g1, "seam-garden-door")
    # The oak trapdoors over the cellar stair, flush with the floor, their
    # hinges on the hole's west side: open, each panel hangs against the west
    # face, along the climb, and a body comes up the stair past it and steps
    # off the top tread east onto the floor (docs/reference/doors-by-hand.md
    # in the engine, *A trapdoor over a stair*).
    cs = p.seam("edge/cellar-stair")
    (c0, c1) = cs["cells"]
    p.put(c0, c1, "trapdoor")
    p.claim_box(c0, c1, "cellar-stair")
    # A little furniture, against the walls and out of every way.
    p.put((1, 1, 1), (1, 1, 1), "smoker")
    p.put((2, 1, 1), (2, 1, 1), "table")
    p.put((11, 1, 6), (11, 1, 6), "store")
    p.put((11, 1, 5), (11, 1, 5), "store")
    p.put((3, 4, 3), (3, 4, 3), "hanging")
    p.put((10, 4, 4), (10, 4, 4), "hanging")
    p.claim_box((1, 1, 1), (5, sy - 2, sz - 2), "kitchen", air_only=True)
    p.claim_box((7, 1, 1), (sx - 2, sy - 2, sz - 2), "back", air_only=True)
    palette = {
        "store": "minecraft:hay_block[axis=y]",
        "floor": "minecraft:spruce_planks",
        "front-door": door("north", "lower"),
        "front-door-top": door("north", "upper"),
        "hanging": HANGING,
        "inner-door": door("east", "lower"),
        "inner-door-top": door("east", "upper"),
        "garden-door": door("north", "lower", kind="iron"),
        "garden-door-top": door("north", "upper", kind="iron"),
        "lid": "minecraft:dark_oak_planks",
        "smoker": "minecraft:cauldron",
        "table": "minecraft:crafting_table",
        "trapdoor": "minecraft:oak_trapdoor[facing=east,half=top,open=false,powered=false,waterlogged=false]",
        "wall": "minecraft:stripped_spruce_log[axis=y]",
    }
    contract = {
        "edges": [
            {"a": "kitchen", "b": "exterior", "class": "walk", "via": "front-door"},
            {"a": "kitchen", "b": "back", "class": "walk", "via": "inner-door"},
            {"a": "back", "b": "exterior", "class": "walk", "via": "cellar-stair"},
            {"a": "back", "b": "exterior", "bar": {"block": "garden-door", "region": "seam-garden-door"}, "class": "barred"},
        ],
        "entry": "kitchen",
        "spaces": {"back": {"envelope": "enclosed"}, "kitchen": {"envelope": "enclosed"}},
    }
    marks = [("node-cottage", (3, 1, 4), "north"), ("latch", (10, 1, 4), "north")]
    return program("the-latch-cottage", p, palette, contract, marks, ("east", "north", "south", "up", "west"))


def cellar(a):
    p = Piece(a)
    sx, sy, sz = p.sx, p.sy, p.sz
    p.put((0, 0, 0), (sx - 1, 0, sz - 1), "floor")
    (lo, hi) = p.alloc["space"]
    p.put(lo, hi, None)
    cs = p.seam("edge/cellar-stair")
    (s0, s1) = cs["cells"]
    x = s0[0]
    # The stair up under the trapdoors, climbing north: a step at each
    # course, the last in the course under the hole, so a body comes up
    # through it and steps off onto the back room's floor beside it.
    # Every rise but the first is jumped from under the hole, where there is
    # headroom: the first step stands at the hole's south edge, the last in the
    # course under it, and a body comes up through the trapdoors.
    p.put((x, 1, 2), (x, 1, 2), "tread")
    p.put((x, 1, 1), (x, 2, 1), "tread")
    p.put((x, 1, 0), (x, 2, 0), "masonry")
    p.put((x, 3, 0), (x, 3, 0), "tread")
    p.claim_box(s0, s1, "cellar-stair")
    for (bx, bz) in ((0, 5), (10, 5), (10, 4), (0, 0)):
        p.put((bx, 1, bz), (bx, 1, bz), "store")
    p.put((0, 2, 5), (0, 2, 5), "lantern")
    p.put((5, 1, 0), (5, 1, 0), "store")
    p.put((5, 2, 0), (5, 2, 0), "lantern")
    p.put((1, 1, 0), (2, 2, 0), "shelf")
    p.claim_box((0, 1, 0), (sx - 1, sy - 1, sz - 1), "room", air_only=True)
    p.claim_box((x, 1, 2), (x, 1, 2), "room")
    p.claim_box((x, 1, 1), (x, 2, 1), "room")
    p.claim_box((x, 1, 0), (x, 2, 0), "room")
    palette = {
        "store": "minecraft:hay_block[axis=y]",
        "floor": "minecraft:cobblestone",
        "lantern": LANTERN,
        "masonry": "minecraft:cobblestone",
        "shelf": "minecraft:bookshelf",
        "tread": "minecraft:cobblestone",
    }
    contract = {
        "edges": [{"a": "room", "b": "exterior", "class": "stair", "rise": 0, "via": "cellar-stair"}],
        "entry": "room",
        "spaces": {"room": {"envelope": "enclosed"}},
    }
    marks = [("node-cellar", (4, 1, 3), "north")]
    return program("the-latch-cellar", p, palette, contract, marks)


def garden(a):
    p = Piece(a)
    sx, sy, sz = p.sx, p.sy, p.sz
    p.put((0, 0, 0), (sx - 1, 0, sz - 1), "grass")
    hedge_ring(p, ("west", "east", "north"))
    p.opening("edge/garden-door")
    for (x, z) in ((2, 2), (8, 2), (2, 5), (8, 5)):
        lamp_post(p, x, z)
    for (x, z, f) in ((4, 2, "poppy"), (6, 2, "dandelion"), (4, 4, "cornflower"), (7, 4, "oxeye_daisy")):
        p.put((x, 1, z), (x, 1, z), f)
    claim_tops(p)
    p.claim_box((1, 1, 1), (sx - 2, sy - 1, sz - 1), "room", air_only=True)
    p.claim_box((4, 1, 2), (4, 1, 2), "room")
    p.claim_box((6, 1, 2), (6, 1, 2), "room")
    p.claim_box((4, 1, 4), (4, 1, 4), "room")
    p.claim_box((7, 1, 4), (7, 1, 4), "room")
    palette = {
        "cornflower": "minecraft:cornflower",
        "dandelion": "minecraft:dandelion",
        "grass": "minecraft:grass_block[snowy=false]",
        "hedge": HEDGE,
        "lantern": LANTERN,
        "oxeye_daisy": "minecraft:oxeye_daisy",
        "poppy": "minecraft:poppy",
        "post": POST,
    }
    contract = {
        "edges": [{"a": "room", "b": "exterior", "class": "walk", "via": "garden-door"}],
        "entry": "room",
        "no_body": {"tops": {"reason": "the tops of the hedges and the lamps, which nobody walks"}},
        "spaces": {"room": {"envelope": "open"}},
    }
    marks = [("node-garden", (5, 1, 3), "south")]
    return program("the-latch-garden", p, palette, contract, marks, ("east", "north", "west"))


def main():
    alloc = {a["place"]: a for a in json.loads(pathlib.Path(sys.argv[1]).read_text())}
    here = pathlib.Path(__file__).resolve().parent.parent
    out = here / "programs"
    out.mkdir(exist_ok=True)
    for stem, build in (("yard", yard), ("cottage", cottage), ("cellar", cellar), ("garden", garden)):
        prog = build(alloc[f"node/{stem}"])
        path = out / f"{stem}.json"
        path.write_text(json.dumps(prog, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
