#!/usr/bin/env python3
"""Write the five place programs of The Open Yard.

    delvec allocation campaigns/the-open-yard --all > alloc.json
    python3 campaigns/the-open-yard/design/build_pieces.py alloc.json

`delvec detail` expands `programs/<place stem>.json` inside the frame the site
plan hands each place. Each piece is stated here as a cell grid in the frame's
own coordinates (x east, y up, z south, the frame's minimum corner at 0) and
written out as a grammar program: the grid is cut along x into runs of
identical slices, each slice along z, each column along y, so every leaf is one
material over one box, wrapped in the contract region it belongs to.

The allocation is read, never copied: the frame's extent, the voids (cells the
place does not own, written as `structure_void`), every seam's handed cells and
every open side come from it, so a plan edit is followed by re-running the two
commands above.
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
        if role in ("hedge", "lantern", "lane-door-top") and p.block.get((x, y + 1, z)) is None:
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



TOPS = {"tops": {"reason": "the tops of the lamps, posts and stalls, which nobody walks"}}


def claim_tops_of(p, roles, region="tops"):
    for (x, y, z), role in list(p.block.items()):
        if role in roles and p.block.get((x, y + 1, z)) is None and y + 1 < p.sy:
            p.claim_box((x, y + 1, z), (x, y + 1, z), region)


def street(a):
    p = Piece(a)
    sx, sy, sz = p.sx, p.sy, p.sz
    p.put((1, 0, 1), (sx - 2, 0, sz - 2), "road")
    p.put((1, 0, sz - 2), (sx - 2, 0, sz - 2), "verge")
    # Low walls on the ring where nothing meets the street: its two ends, and
    # the stretches of its north and south sides between the places.
    for x in range(sx):
        for z in range(sz):
            if x in (0, sx - 1) or z in (0, sz - 1):
                p.put((x, 1, z), (x, 2, z), "wall")
    # The court's front is the street's own ring, open along the contact.
    cf = p.seam("edge/court-front")
    (c0, c1) = cf["cells"]
    p.put(c0, c1, None)
    p.claim_box(c0, c1, "court-front")
    for edge, region in (("edge/smithy-front", "smithy-front"), ("edge/market-front", "market-front"),
                         ("edge/house-door", "house-door")):
        s = p.seam(edge)
        (s0, s1) = s["cells"]
        p.put(s0, s1, None)
        p.claim_box(s0, s1, region)
    for x in (4, 10, 19, 24, 28):
        p.put((x, 1, sz - 2), (x, 1, sz - 2), "post")
        p.put((x, 2, sz - 2), (x, 2, sz - 2), "lantern")
    claim_tops_of(p, ("wall", "lantern"))
    p.claim_box((1, 1, 1), (sx - 2, sy - 1, sz - 2), "street", air_only=True)
    palette = {
        "lantern": LANTERN,
        "post": POST,
        "road": "minecraft:cobblestone",
        "verge": "minecraft:grass_block[snowy=false]",
        "wall": "minecraft:mossy_cobblestone",
    }
    contract = {
        "edges": [
            {"a": "street", "b": "exterior", "class": "walk", "via": "court-front"},
            {"a": "street", "b": "exterior", "class": "walk", "via": "smithy-front"},
            {"a": "street", "b": "exterior", "class": "walk", "via": "market-front"},
            {"a": "street", "b": "exterior", "class": "walk", "via": "house-door"},
        ],
        "entry": "street",
        "no_body": TOPS,
        "spaces": {"street": {"envelope": "open"}},
    }
    marks = [("spawn", (2, 1, 2), "east", "entry"), ("node-street", (4, 1, 2), "east")]
    return program("the-open-yard-street", p, palette, contract, marks, ("east", "north", "south", "west"))


def court(a):
    p = Piece(a)
    sx, sy, sz = p.sx, p.sy, p.sz
    (lo, hi) = p.alloc["space"]
    p.put((lo[0], 0, lo[2]), (hi[0], 0, hi[2]), "paving")
    # The fountain in the middle: a rim of stone round one cell of water.
    p.put((2, 1, 2), (4, 1, 4), "rim")
    p.put((3, 1, 3), (3, 1, 3), "water")
    for (x, z) in ((1, 1), (6, 1), (1, 5), (6, 5)):
        p.put((x, 1, z), (x, 1, z), "post")
        p.put((x, 2, z), (x, 2, z), "lantern")
    claim_tops_of(p, ("lantern",))
    cf = p.seam("edge/court-front")
    (c0, c1) = cf["cells"]
    p.claim_box(c0, c1, "court-front", air_only=True)
    p.claim_box((0, 1, 0), (sx - 1, sy - 1, sz - 1), "court", air_only=True)
    palette = {
        "lantern": LANTERN,
        "paving": "minecraft:polished_andesite",
        "post": POST,
        "rim": "minecraft:stone_bricks",
        "water": "minecraft:water[level=0]",
    }
    contract = {
        "edges": [{"a": "court", "b": "exterior", "class": "walk", "via": "court-front"}],
        "entry": "court",
        "no_body": TOPS,
        "spaces": {"court": {"envelope": "open"}},
    }
    marks = [("node-court", (5, 1, 5), "north")]
    return program("the-open-yard-court", p, palette, contract, marks)


def smithy(a):
    p = Piece(a)
    sx, sy, sz = p.sx, p.sy, p.sz
    (lo, hi) = p.alloc["space"]
    p.put((lo[0], 0, lo[2]), (hi[0], 0, hi[2]), "floor")
    p.put((0, sy - 1, 0), (sx - 1, sy - 1, sz - 1), "lid")
    # Three walls; the street side stands no wall (it is declared open), and
    # its two corners stand with the walls beside them.
    for z in range(sz):
        p.put((0, 1, z), (0, sy - 2, z), "wall")
        p.put((sx - 1, 1, z), (sx - 1, sy - 2, z), "wall")
    p.put((1, 1, 0), (sx - 2, sy - 2, 0), "wall")
    # The counter across the room one cell in from its open front, and the
    # door beside it; the row before the counter is the front a body leans
    # on, as wide as the front.
    cz = hi[2] - 1
    p.put((1, 1, cz), (hi[0] - 1, 1, cz), "counter")
    p.put((hi[0], 1, cz), (hi[0], 1, cz), "door")
    p.put((hi[0], 2, cz), (hi[0], 2, cz), "door-top")
    # The smith's things behind the counter.
    p.put((2, 1, 2), (2, 1, 2), "anvil")
    p.put((4, 1, 1), (4, 1, 1), "table")
    p.put((6, 1, 1), (6, 1, 1), "grindstone")
    p.claim_box((1, 1, hi[2]), (hi[0], sy - 2, hi[2]), "shop", air_only=True)
    p.put((3, sy - 2, 3), (3, sy - 2, 3), "hanging")
    p.put((6, sy - 2, 4), (6, sy - 2, 4), "hanging")
    sf = p.seam("edge/smithy-front")
    (f0, f1) = sf["cells"]
    p.claim_box(f0, f1, "smithy-front", air_only=True)
    # The counter and the door belong to the room they front.
    p.claim_box((1, 1, cz), (hi[0], 2, cz), "shop")
    p.claim_box((1, 1, 1), (sx - 2, sy - 2, hi[2]), "shop", air_only=True)
    palette = {
        "anvil": "minecraft:anvil[facing=east]",
        "counter": "minecraft:stripped_spruce_wood[axis=x]",
        "door": door("south", "lower", kind="spruce"),
        "door-top": door("south", "upper", kind="spruce"),
        "floor": "minecraft:stone_bricks",
        "grindstone": "minecraft:grindstone[face=floor,facing=south]",
        "hanging": HANGING,
        "lid": "minecraft:dark_oak_planks",
        "table": "minecraft:smithing_table",
        "wall": "minecraft:cobblestone",
    }
    contract = {
        "edges": [{"a": "shop", "b": "exterior", "class": "walk", "via": "smithy-front"}],
        "entry": "shop",
        "spaces": {"shop": {"envelope": "open"}},
    }
    marks = [("node-smithy", (3, 1, 3), "south")]
    return program("the-open-yard-smithy", p, palette, contract, marks, ("east", "north", "south", "up", "west"))


def market(a):
    p = Piece(a)
    sx, sy, sz = p.sx, p.sy, p.sz
    (lo, hi) = p.alloc["space"]
    p.put((lo[0], 0, lo[2]), (hi[0], 0, hi[2]), "floor")
    p.put((0, sy - 1, 0), (sx - 1, sy - 1, sz - 1), "lid")
    # The roof stands on a post at each corner of the ring; every side is open.
    for (x, z) in ((0, 0), (sx - 1, 0), (0, sz - 1), (sx - 1, sz - 1)):
        p.put((x, 1, z), (x, sy - 2, z), "post")
    # The stalls under it.
    for (x, z, r) in ((2, 2, "hay"), (2, 3, "hay"), (5, 2, "melon"), (5, 3, "pumpkin"), (3, 5, "hay"), (4, 5, "melon")):
        p.put((x, 1, z), (x, 1, z), r)
    p.put((2, sy - 2, 4), (2, sy - 2, 4), "hanging")
    p.put((5, sy - 2, 5), (5, sy - 2, 5), "hanging")
    claim_tops_of(p, ("hay", "melon", "pumpkin"))
    mf = p.seam("edge/market-front")
    (m0, m1) = mf["cells"]
    p.claim_box(m0, m1, "market-front", air_only=True)
    p.claim_box((0, 1, 0), (sx - 1, sy - 2, sz - 1), "market", air_only=True)
    palette = {
        "floor": "minecraft:spruce_planks",
        "hanging": HANGING,
        "hay": "minecraft:hay_block[axis=y]",
        "lid": "minecraft:spruce_planks",
        "melon": "minecraft:melon",
        "post": "minecraft:stripped_oak_log[axis=y]",
        "pumpkin": "minecraft:pumpkin",
    }
    contract = {
        "edges": [{"a": "market", "b": "exterior", "class": "walk", "via": "market-front"}],
        "entry": "market",
        "no_body": TOPS,
        "spaces": {"market": {"envelope": "open"}},
    }
    marks = [("node-market", (3, 1, 3), "south")]
    return program("the-open-yard-market", p, palette, contract, marks, ("east", "north", "south", "up", "west"))


def house(a):
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
    hd = p.seam("edge/house-door")
    (d0, d1) = hd["cells"]
    p.put(d0, d0, "door")
    p.put(d1, d1, "door-top")
    p.claim_box(d0, d1, "house-door")
    p.put((1, 1, hi[2]), (2, 1, hi[2]), "shelf")
    p.put((5, 1, hi[2]), (5, 1, hi[2]), "table")
    p.put((3, sy - 2, 3), (3, sy - 2, 3), "hanging")
    p.claim_box((1, 1, 1), (sx - 2, sy - 2, sz - 2), "room", air_only=True)
    palette = {
        "door": door("north", "lower"),
        "door-top": door("north", "upper"),
        "floor": "minecraft:oak_planks",
        "hanging": HANGING,
        "lid": "minecraft:dark_oak_planks",
        "shelf": "minecraft:bookshelf",
        "table": "minecraft:crafting_table",
        "wall": "minecraft:white_terracotta",
    }
    contract = {
        "edges": [{"a": "room", "b": "exterior", "class": "walk", "via": "house-door"}],
        "entry": "room",
        "spaces": {"room": {"envelope": "enclosed"}},
    }
    marks = [("node-house", (3, 1, 3), "north")]
    return program("the-open-yard-house", p, palette, contract, marks, ("east", "north", "south", "up", "west"))


def main():
    alloc = {a["place"]: a for a in json.loads(pathlib.Path(sys.argv[1]).read_text())}
    here = pathlib.Path(__file__).resolve().parent.parent
    out = here / "programs"
    out.mkdir(exist_ok=True)
    for stem, build in (("street", street), ("court", court), ("smithy", smithy), ("market", market), ("house", house)):
        prog = build(alloc[f"node/{stem}"])
        path = out / f"{stem}.json"
        path.write_text(json.dumps(prog, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
