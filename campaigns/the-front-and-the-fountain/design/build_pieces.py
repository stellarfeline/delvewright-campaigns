#!/usr/bin/env python3
"""Write the six place programs of The Front and the Fountain.

    delvec allocation campaigns/the-front-and-the-fountain --all > alloc.json
    python3 campaigns/the-front-and-the-fountain/design/build_pieces.py alloc.json

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


def row(a):
    """Tanner's Row: a way place three wide, a verge on its south side with
    lamps, low walls on its ring where no front meets it."""
    p = Piece(a)
    sx, sy, sz = p.sx, p.sy, p.sz
    p.put((1, 0, 1), (sx - 2, 0, sz - 2), "road")
    p.put((1, 0, sz - 2), (sx - 2, 0, sz - 2), "verge")
    for x in range(sx):
        for z in range(sz):
            if x in (0, sx - 1) or z in (0, sz - 1):
                p.put((x, 1, z), (x, 2, z), "wall")
    regions = []
    for s in p.alloc["seams"]:
        region = s["edge"].split("/", 1)[1]
        (s0, s1) = s["cells"]
        p.put(s0, s1, None)
        p.claim_box(s0, s1, region)
        regions.append(region)
    for x in (3, 13, 29, 33, 43):
        p.put((x, 1, sz - 2), (x, 1, sz - 2), "post")
        p.put((x, 2, sz - 2), (x, 2, sz - 2), "lantern")
    claim_tops_of(p, ("wall", "lantern"))
    p.claim_box((1, 1, 1), (sx - 2, sy - 1, sz - 2), "row", air_only=True)
    palette = {
        "lantern": LANTERN,
        "post": POST,
        "road": "minecraft:cobblestone",
        "verge": "minecraft:grass_block[snowy=false]",
        "wall": "minecraft:mossy_cobblestone",
    }
    contract = {
        "edges": [{"a": "row", "b": "exterior", "class": "walk", "via": r} for r in regions],
        "entry": "row",
        "no_body": TOPS,
        "spaces": {"row": {"envelope": "open"}},
    }
    marks = [("spawn", (2, 1, 2), "east", "entry"), ("node-row", (4, 1, 2), "east")]
    return program("the-front-and-the-fountain-row", p, palette, contract, marks, ("east", "north", "south", "west"))


def three_walls(p):
    """Floor, lid over the whole frame, and walls on the west, east and north
    rings from the floor course to the lid; the south side is open."""
    sx, sy, sz = p.sx, p.sy, p.sz
    (lo, hi) = p.alloc["space"]
    p.put((0, 0, 0), (sx - 1, 0, sz - 1), "floor")
    p.put((0, sy - 1, 0), (sx - 1, sy - 1, sz - 1), "lid")
    for z in range(sz):
        p.put((0, 1, z), (0, sy - 2, z), "wall")
        p.put((sx - 1, 1, z), (sx - 1, sy - 2, z), "wall")
    p.put((1, 1, 0), (sx - 2, sy - 2, 0), "wall")
    return lo, hi


def smithy(a):
    """The new smithy. Behind the open front's first row — the row the row's
    contact crosses onto, which its clear width keeps clear (`DW1057`) —
    stands the frame the wall would have been: a post at each end and
    between the bays, a beam across the whole front two courses up, and wall
    over the beam to the lid. Under the beam: the counter bay — a one-course
    counter with the beam over it — and the door bay, a door between two posts
    with the beam its head. The counter's top and the door's head share the
    beam's line."""
    p = Piece(a)
    sx, sy, sz = p.sx, p.sy, p.sz
    lo, hi = three_walls(p)
    fz = hi[2] - 1  # the frame's row, behind the clear front row
    top = sy - 2
    for x in (1, 5, 7, sx - 2):
        p.put((x, 1, fz), (x, 2, fz), "post")
    p.put((1, 3, fz), (sx - 2, 3, fz), "beam")
    p.put((1, 4, fz), (sx - 2, top, fz), "infill")
    p.put((2, 1, fz), (4, 1, fz), "counter")
    p.put((6, 1, fz), (6, 1, fz), "door")
    p.put((6, 2, fz), (6, 2, fz), "door-top")
    p.put((8, 1, fz), (8, 2, fz), "infill")
    # The smith's work behind the frame: the forge against the back wall with
    # its hood, the anvil before it, the quench at hand, the bench and the
    # grindstone along the side walls.
    p.put((3, 1, 1), (5, 1, 1), "forge-base")
    p.put((4, 1, 1), (4, 1, 1), "forge")
    p.put((3, 2, 1), (5, 3, 1), "hood")
    p.put((4, 3, 2), (4, 3, 2), "chain")
    p.put((4, 1, 3), (4, 1, 3), "anvil")
    p.put((6, 1, 2), (6, 1, 2), "quench")
    p.put((1, 1, 3), (1, 1, 3), "table")
    p.put((1, 1, 4), (1, 1, 4), "barrel")
    p.put((sx - 2, 1, 2), (sx - 2, 1, 2), "grindstone")
    p.put((sx - 2, 1, 3), (sx - 2, 1, 4), "rack")
    p.put((2, top, 4), (2, top, 4), "hanging")
    p.put((7, top, 3), (7, top, 3), "hanging")
    p.put((4, top, 5), (4, top, 5), "hanging")
    claim_tops_of(p, ("hood", "chain"))
    sf = p.seam("edge/smithy-front")
    (f0, f1) = sf["cells"]
    p.claim_box(f0, f1, "smithy-front", air_only=True)
    # The whole frame belongs to the room it fronts: posts, beam and infill.
    p.claim_box((1, 1, fz), (sx - 2, top, fz), "shop")
    p.claim_box((1, 1, 1), (sx - 2, top, hi[2]), "shop", air_only=True)
    palette = {
        "anvil": "minecraft:anvil[facing=east]",
        "barrel": "minecraft:oak_log[axis=y]",
        "beam": "minecraft:stripped_dark_oak_log[axis=x]",
        "chain": "minecraft:iron_chain[axis=y,waterlogged=false]",
        "counter": "minecraft:stripped_spruce_wood[axis=x]",
        "door": door("south", "lower", kind="spruce"),
        "door-top": door("south", "upper", kind="spruce"),
        "floor": "minecraft:stone_bricks",
        "forge": "minecraft:campfire[facing=south,lit=true,signal_fire=false,waterlogged=false]",
        "forge-base": "minecraft:bricks",
        "grindstone": "minecraft:grindstone[face=floor,facing=west]",
        "hanging": HANGING,
        "hood": "minecraft:bricks",
        "infill": "minecraft:white_terracotta",
        "lid": "minecraft:dark_oak_planks",
        "post": "minecraft:stripped_dark_oak_log[axis=y]",
        "quench": "minecraft:water_cauldron[level=3]",
        "rack": "minecraft:smithing_table",
        "table": "minecraft:crafting_table",
        "wall": "minecraft:cobblestone",
    }
    contract = {
        "edges": [{"a": "shop", "b": "exterior", "class": "walk", "via": "smithy-front"}],
        "entry": "shop",
        "no_body": {"tops": {"reason": "the top of the forge's hood and its chain, which nobody walks"}},
        "spaces": {"shop": {"envelope": "open"}},
    }
    marks = [("node-smithy", (2, 1, 4), "south")]
    return program("the-front-and-the-fountain-smithy", p, palette, contract, marks, ("east", "north", "south", "up", "west"))


def stall(a):
    """The old stall: the ruling's shape. Behind the open front's first row a
    one-course counter and, beside it, a two-course door, with nothing over
    either — no post, no beam, no wall — under the five-course open face."""
    p = Piece(a)
    sx, sy, sz = p.sx, p.sy, p.sz
    lo, hi = three_walls(p)
    fz = hi[2] - 1
    top = sy - 2
    p.put((2, 1, fz), (4, 1, fz), "counter")
    p.put((6, 1, fz), (6, 1, fz), "door")
    p.put((6, 2, fz), (6, 2, fz), "door-top")
    # Goods behind the counter.
    p.put((2, 1, 2), (3, 1, 2), "barrel")
    p.put((sx - 2, 1, 1), (sx - 2, 2, 1), "bale")
    p.put((1, 1, 1), (1, 1, 1), "chest")
    p.put((3, top, 3), (3, top, 3), "hanging")
    p.put((6, top, 4), (6, top, 4), "hanging")
    claim_tops_of(p, ("door-top", "bale"))
    # Over the free-standing door nothing stands, so the cell over its top and
    # the front cell beside that are one air nobody walks.
    sf = p.seam("edge/stall-front")
    (f0, f1) = sf["cells"]
    p.claim_box(f0, f1, "stall-front", air_only=True)
    p.claim_box((1, 1, fz), (sx - 2, top, fz), "shop")
    p.claim_box((1, 1, 1), (sx - 2, top, hi[2]), "shop", air_only=True)
    palette = {
        "bale": "minecraft:hay_block[axis=y]",
        "barrel": "minecraft:pumpkin",
        "chest": "minecraft:melon",
        "counter": "minecraft:stripped_spruce_wood[axis=x]",
        "door": door("south", "lower", kind="spruce"),
        "door-top": door("south", "upper", kind="spruce"),
        "floor": "minecraft:stone_bricks",
        "hanging": HANGING,
        "lid": "minecraft:dark_oak_planks",
        "wall": "minecraft:cobblestone",
    }
    contract = {
        "edges": [{"a": "shop", "b": "exterior", "class": "walk", "via": "stall-front"}],
        "entry": "shop",
        "no_body": {"tops": {"reason": "the top of the stall's door and of its bales, which nobody walks"}},
        "spaces": {"shop": {"envelope": "open"}},
    }
    marks = [("node-stall", (4, 1, 4), "south")]
    return program("the-front-and-the-fountain-stall", p, palette, contract, marks, ("east", "north", "south", "up", "west"))


def square(a):
    """The fountain square, open on every side. Its fountain stands in the
    middle: a basin five wide held by a one-course rim, a stack in the basin's
    middle two courses high, and on the stack a bowl — a ring of stone round a
    cell of water — so the water stands above the ground, over the basin's
    water. Every water cell is a source walled on every side and below: a
    piece's water is still (`DW0800`), so the bowl's water stands and does not
    fall."""
    p = Piece(a)
    sx, sy, sz = p.sx, p.sy, p.sz
    (lo, hi) = p.alloc["space"]
    p.put((lo[0], 0, lo[2]), (hi[0], 0, hi[2]), "paving")
    cx, cz = (lo[0] + hi[0]) // 2, (lo[2] + hi[2]) // 2
    for x in range(cx - 2, cx + 3):
        for z in range(cz - 2, cz + 3):
            if max(abs(x - cx), abs(z - cz)) == 2:
                p.put((x, 1, z), (x, 1, z), "rim")
            else:
                p.put((x, 0, z), (x, 0, z), "basin")
                p.put((x, 1, z), (x, 1, z), "water")
    p.put((cx, 1, cz), (cx, 2, cz), "stack")
    p.put((cx - 1, 3, cz - 1), (cx + 1, 3, cz + 1), "bowl")
    p.put((cx, 3, cz), (cx, 3, cz), "water")
    # Lamp posts in from each corner, off every side's approach row and off
    # the row the front's crossing lands on.
    for (x, z) in ((lo[0] + 1, lo[2] + 1), (hi[0] - 1, lo[2] + 1), (lo[0] + 1, hi[2] - 2), (hi[0] - 1, hi[2] - 2)):
        p.put((x, 1, z), (x, 1, z), "post")
        p.put((x, 2, z), (x, 2, z), "lantern")
    claim_tops_of(p, ("lantern", "rim", "bowl"))
    sf = p.seam("edge/square-front")
    (c0, c1) = sf["cells"]
    p.claim_box(c0, c1, "square-front", air_only=True)
    p.claim_box((0, 1, 0), (sx - 1, sy - 1, sz - 1), "square", air_only=True)
    palette = {
        "basin": "minecraft:smooth_stone",
        "bowl": "minecraft:stone_brick_slab[type=bottom,waterlogged=false]",
        "lantern": LANTERN,
        "paving": "minecraft:polished_andesite",
        "post": POST,
        "rim": "minecraft:stone_bricks",
        "stack": "minecraft:chiseled_stone_bricks",
        "water": "minecraft:water[level=0]",
    }
    contract = {
        "edges": [{"a": "square", "b": "exterior", "class": "walk", "via": "square-front"}],
        "entry": "square",
        "no_body": TOPS,
        "spaces": {"square": {"envelope": "open"}},
    }
    marks = [("node-square", (lo[0] + 2, 1, hi[2] - 1), "north")]
    return program("the-front-and-the-fountain-square", p, palette, contract, marks)


def ring(a):
    """The old well-yard, open on every side: a flat ring of stone round one
    cell of water, the water at the ring's own height."""
    p = Piece(a)
    sx, sy, sz = p.sx, p.sy, p.sz
    (lo, hi) = p.alloc["space"]
    p.put((lo[0], 0, lo[2]), (hi[0], 0, hi[2]), "paving")
    cx, cz = (lo[0] + hi[0]) // 2, (lo[2] + hi[2]) // 2
    p.put((cx - 1, 1, cz - 1), (cx + 1, 1, cz + 1), "rim")
    p.put((cx, 1, cz), (cx, 1, cz), "water")
    # Lamp posts in from each corner, off every side's approach row and off
    # the row the front's crossing lands on.
    for (x, z) in ((lo[0] + 1, lo[2] + 1), (hi[0] - 1, lo[2] + 1), (lo[0] + 1, hi[2] - 2), (hi[0] - 1, hi[2] - 2)):
        p.put((x, 1, z), (x, 1, z), "post")
        p.put((x, 2, z), (x, 2, z), "lantern")
    claim_tops_of(p, ("lantern", "rim"))
    sf = p.seam("edge/ring-front")
    (c0, c1) = sf["cells"]
    p.claim_box(c0, c1, "ring-front", air_only=True)
    p.claim_box((0, 1, 0), (sx - 1, sy - 1, sz - 1), "yard", air_only=True)
    palette = {
        "lantern": LANTERN,
        "paving": "minecraft:polished_andesite",
        "post": POST,
        "rim": "minecraft:stone_bricks",
        "water": "minecraft:water[level=0]",
    }
    contract = {
        "edges": [{"a": "yard", "b": "exterior", "class": "walk", "via": "ring-front"}],
        "entry": "yard",
        "no_body": TOPS,
        "spaces": {"yard": {"envelope": "open"}},
    }
    marks = [("node-ring", (lo[0] + 2, 1, hi[2] - 1), "north")]
    return program("the-front-and-the-fountain-ring", p, palette, contract, marks)


def lodge(a):
    """The warden's lodge across the row: walled all round, an open doorway
    on the row, a table and a shelf inside."""
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
    # An open doorway: the census's door line counts the row's two fronts.
    hd = p.seam("edge/lodge-door")
    (d0, d1) = hd["cells"]
    p.put(d0, d1, None)
    p.claim_box(d0, d1, "lodge-door")
    p.put((1, 1, hi[2]), (2, 1, hi[2]), "shelf")
    p.put((5, 1, hi[2]), (5, 1, hi[2]), "table")
    p.put((3, sy - 2, 3), (3, sy - 2, 3), "hanging")
    p.claim_box((1, 1, 1), (sx - 2, sy - 2, sz - 2), "room", air_only=True)
    palette = {
        "floor": "minecraft:oak_planks",
        "hanging": HANGING,
        "lid": "minecraft:dark_oak_planks",
        "shelf": "minecraft:bookshelf",
        "table": "minecraft:crafting_table",
        "wall": "minecraft:white_terracotta",
    }
    contract = {
        "edges": [{"a": "room", "b": "exterior", "class": "walk", "via": "lodge-door"}],
        "entry": "room",
        "spaces": {"room": {"envelope": "enclosed"}},
    }
    marks = [("node-lodge", (3, 1, 2), "north")]
    return program("the-front-and-the-fountain-lodge", p, palette, contract, marks, ("east", "north", "south", "up", "west"))


def main():
    alloc = {a["place"]: a for a in json.loads(pathlib.Path(sys.argv[1]).read_text())}
    here = pathlib.Path(__file__).resolve().parent.parent
    out = here / "programs"
    out.mkdir(exist_ok=True)
    for stem, build in (("row", row), ("smithy", smithy), ("square", square), ("stall", stall), ("ring", ring), ("lodge", lodge)):
        prog = build(alloc[f"node/{stem}"])
        path = out / f"{stem}.json"
        path.write_text(json.dumps(prog, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
