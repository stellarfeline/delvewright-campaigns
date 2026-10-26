#!/usr/bin/env python3
"""Write the six place programs of The Four Trades.

    delvec allocation campaigns/the-four-trades --all > alloc.json
    python3 campaigns/the-four-trades/design/build_pieces.py alloc.json

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


def lane(a):
    """Craft Lane: a way place three wide, a verge on its south side with
    lamps, low walls on its ring where no door or front meets it."""
    p = Piece(a)
    sx, sy, sz = p.sx, p.sy, p.sz
    p.put((1, 0, 1), (sx - 2, 0, sz - 2), "road")
    p.put((1, 0, sz - 3), (sx - 2, 0, sz - 2), "verge")
    for x in range(sx):
        for z in range(sz):
            if x in (0, sx - 1) or z in (0, sz - 1):
                p.put((x, 1, z), (x, 2, z), "wall")
    regions = []
    for s in p.alloc["seams"]:
        stem = s["edge"].split("/", 1)[1]
        (s0, s1) = s["cells"]
        p.put(s0, s1, None)
        p.claim_box(s0, s1, stem)
        regions.append(stem)
    # Lamps, bushes and flowers on the verge, clear of the well-yard's front.
    front = [c[0] for s in p.alloc["seams"] if s["edge"] == "edge/well-front" for c in s["cells"]]
    clear = range(min(front) - 1, max(front) + 2)
    flowers = []
    for x in range(4, sx - 3, 6):
        if x not in clear:
            p.put((x, 1, sz - 2), (x, 1, sz - 2), "post")
            p.put((x, 2, sz - 2), (x, 2, sz - 2), "lantern")
    for x in range(7, sx - 3, 6):
        if x not in clear and x + 1 not in clear:
            p.put((x, 1, sz - 2), (x, 1, sz - 2), "bush")
            p.put((x + 1, 1, sz - 3), (x + 1, 1, sz - 3), "flower")
            flowers.append((x + 1, 1, sz - 3))
    claim_tops_of(p, ("wall", "lantern", "bush"))
    for c in flowers:
        p.claim_box(c, c, "lane")
    p.claim_box((1, 1, 1), (sx - 2, sy - 1, sz - 2), "lane", air_only=True)
    palette = {
        "bush": "minecraft:oak_leaves[distance=1,persistent=true,waterlogged=false]",
        "flower": "minecraft:poppy",
        "lantern": LANTERN,
        "post": POST,
        "road": "minecraft:cobblestone",
        "verge": "minecraft:grass_block[snowy=false]",
        "wall": "minecraft:mossy_cobblestone",
    }
    contract = {
        "edges": [{"a": "lane", "b": "exterior", "class": "walk", "via": r} for r in regions],
        "entry": "lane",
        "no_body": {"tops": {"reason": "the tops of the lane's walls, lamps and bushes, which nobody walks"}},
        "spaces": {"lane": {"envelope": "open"}},
    }
    marks = [("spawn", (2, 1, 2), "east", "entry"), ("node-lane", (4, 1, 2), "east")]
    return program("the-four-trades-lane", p, palette, contract, marks, ("east", "north", "south", "west"))


# Every trade is one frame of 16 x 9 x 16: the floor course at y 0, the play
# space x 1..14, y 1..4, z 1..14, the lid at y 5, a roof zone y 6..8. The front
# door is the plan's seam in the south wall at x 7. A partition at z 8 divides
# the front shop (z 9..14), which a customer enters, from the workroom (z 1..7)
# where the trade is worked; it holds a window onto the work at x 3..5 and the
# inner door at x 10.
PART_Z = 8
INNER_X = 10
COUNTER_Z = 11


def trade(a, stem, kind, spec):
    p = Piece(a)
    sx, sy, sz = p.sx, p.sy, p.sz
    lid = 5
    p.put((0, 0, 0), (sx - 1, 0, sz - 1), "floor")
    for x in range(sx):
        for z in range(sz):
            if x in (0, sx - 1) or z in (0, sz - 1):
                corner = x in (0, sx - 1) and z in (0, sz - 1)
                p.put((x, 1, z), (x, lid - 1, z), "post" if corner else "wall")
    p.put((0, lid, 0), (sx - 1, lid, sz - 1), "lid")
    # The roof: a parapet round the lid's edge, and whatever the trade raises.
    for x in range(sx):
        for z in range(sz):
            if x in (0, sx - 1) or z in (0, sz - 1):
                p.put((x, lid + 1, z), (x, lid + 1, z), "parapet")
    # The front: two windows either side of the door.
    for x0 in (3, 10):
        p.put((x0, 2, sz - 1), (x0 + 1, 3, sz - 1), "window")
    # The partition between the shop and the workroom.
    p.put((1, 1, PART_Z), (sx - 2, lid - 1, PART_Z), "partition")
    p.put((3, 2, PART_Z), (5, 3, PART_Z), "window")
    p.put((INNER_X, 1, PART_Z), (INNER_X, 1, PART_Z), "inner-door")
    p.put((INNER_X, 2, PART_Z), (INNER_X, 2, PART_Z), "inner-door-top")
    # The front door, in the plan's seam.
    s = p.seam(f"edge/{stem}-door")
    (d0, d1) = s["cells"]
    p.put(d0, d0, "door")
    p.put(d1, d1, "door-top")
    # The counter across the shop, a pass at its east end to the inner door.
    p.put((2, 1, COUNTER_Z), (8, 1, COUNTER_Z), "counter")
    # Light: two lanterns in each room.
    for (x, z) in ((4, 4), (11, 4), (4, 12), (11, 12)):
        p.put((x, lid - 1, z), (x, lid - 1, z), "hanging")
    for role, lo, hi in spec["place"]:
        p.put(lo, hi, role)
    # The top of anything a body could stand on with headroom is out of walk.
    for (x, y, z), role in list(p.block.items()):
        if role in spec.get("tall", ()) and y + 2 <= lid - 1 \
                and p.block.get((x, y + 1, z)) is None and p.block.get((x, y + 2, z)) is None:
            p.claim_box((x, y + 1, z), (x, y + 1, z), "tops")
    # A carpet, a banner or a runner is no wall: the room it lies in claims it.
    for (x, y, z), role in list(p.block.items()):
        if role in spec.get("soft", ()):
            p.claim_box((x, y, z), (x, y, z), "shop" if z > PART_Z else "work")
    # Regions: the doors, the two rooms, the roof zone.
    p.claim_box(d0, d1, f"{stem}-door")
    p.claim_box((INNER_X, 1, PART_Z), (INNER_X, 2, PART_Z), "inner-door")
    p.claim_box((1, 1, PART_Z + 1), (sx - 2, lid - 1, sz - 2), "shop", air_only=True)
    p.claim_box((1, 1, 1), (sx - 2, lid - 1, PART_Z - 1), "work", air_only=True)
    p.claim_box((0, lid + 1, 0), (sx - 1, sy - 1, sz - 1), "roof")
    palette = dict(spec["palette"])
    palette.update({
        "door": door("north", "lower", kind=spec["door"]),
        "door-top": door("north", "upper", kind=spec["door"]),
        "inner-door": door("north", "lower", hinge="right", kind=spec["door"]),
        "inner-door-top": door("north", "upper", hinge="right", kind=spec["door"]),
        "hanging": HANGING,
        "window": "minecraft:glass_pane[east=true,north=false,south=false,waterlogged=false,west=true]",
    })
    no_body = {"roof": {"reason": "the flat roof inside its parapet, which nobody walks"}}
    if "tops" in set(p.claim.values()):
        no_body["tops"] = {"reason": "the tops of the stacks and shelves, which nobody walks"}
    contract = {
        "edges": [
            {"a": "shop", "b": "exterior", "class": "walk", "via": f"{stem}-door"},
            {"a": "shop", "b": "work", "class": "walk", "via": "inner-door"},
        ],
        "entry": "shop",
        "no_body": no_body,
        "no_body_majority_ack": "a building that owns its outside owns its roof, and its flat roof is more standable surface than the rooms under it; nobody walks it",
        "spaces": {"shop": {"envelope": "enclosed"}, "work": {"envelope": "enclosed"}},
    }
    marks = [(f"node-{stem}", (7, 1, 13), "north")]
    # The top of the frame is the roof zone's last course: shown where a
    # chimney reaches it, empty (and so not a side at all) where none does.
    top = any(y == sy - 1 and role is not None and role != SKIP for (x, y, z), role in p.block.items())
    shown = ("east", "north", "south", "west") + (("up",) if top else ())
    return program(f"the-four-trades-{stem}", p, palette, contract, marks, shown)


def wool(color):
    return f"minecraft:{color}_wool"


SMITHY = {
    "door": "spruce",
    "palette": {
        "floor": "minecraft:stone_bricks",
        "wall": "minecraft:cobblestone",
        "post": "minecraft:stone_bricks",
        "lid": "minecraft:spruce_planks",
        "parapet": "minecraft:stone_brick_wall[east=none,north=none,south=none,up=true,waterlogged=false,west=none]",
        "partition": "minecraft:stone_bricks",
        "counter": "minecraft:stripped_spruce_wood[axis=x]",
        "forge-side": "minecraft:bricks",
        "fire": "minecraft:campfire[facing=south,lit=true,signal_fire=false,waterlogged=false]",
        "hood": "minecraft:bricks",
        "chimney": "minecraft:bricks",
        "anvil": "minecraft:anvil[facing=east]",
        "quench": "minecraft:water_cauldron[level=3]",
        "grindstone": "minecraft:grindstone[face=floor,facing=south]",
        "bench": "minecraft:smithing_table",
        "coal": "minecraft:coal_block",
        "iron": "minecraft:iron_block",
        "rack": "minecraft:iron_bars[east=true,north=false,south=false,waterlogged=false,west=true]",
        "chain": "minecraft:iron_chain[axis=y,waterlogged=false]",
        "worn": "minecraft:chipped_anvil[facing=east]",
    },
    "place": [
        # The workroom: the forge against the back wall, its fire in a hearth
        # of brick under a hood, the chimney through the roof; the anvil
        # before it, the quench at hand, the grindstone and the bench by the
        # side walls, the coal heaped in the corner.
        ("forge-side", (2, 1, 1), (2, 1, 1)), ("forge-side", (4, 1, 1), (4, 1, 1)),
        ("fire", (3, 1, 1), (3, 1, 1)),
        ("hood", (2, 3, 1), (4, 3, 1)), ("chimney", (3, 4, 1), (3, 4, 1)),
        ("chimney", (3, 6, 1), (3, 7, 1)), ("fire", (3, 8, 1), (3, 8, 1)),
        ("anvil", (3, 1, 3), (3, 1, 3)),
        ("quench", (5, 1, 2), (5, 1, 2)),
        ("grindstone", (8, 1, 1), (8, 1, 1)),
        ("bench", (10, 1, 1), (10, 1, 1)),
        ("coal", (13, 1, 1), (13, 1, 2)), ("coal", (12, 1, 1), (12, 1, 1)),
        ("iron", (13, 1, 5), (13, 2, 5)),
        # The shop: finished ironwork behind the counter — a rack of bars and
        # hanging chain against the partition, a worn anvil for sale.
        ("rack", (6, 1, 9), (8, 2, 9)),
        ("chain", (2, 3, 9), (2, 4, 9)), ("chain", (4, 3, 9), (4, 4, 9)),
        ("worn", (3, 1, 10), (3, 1, 10)),
        ("iron", (6, 1, 10), (6, 1, 10)),
    ],
    "tall": ("rack", "iron", "hood"),
}

WEAVER = {
    "door": "oak",
    "palette": {
        "floor": "minecraft:spruce_planks",
        "wall": "minecraft:white_terracotta",
        "post": "minecraft:stripped_oak_log[axis=y]",
        "lid": "minecraft:oak_planks",
        "parapet": "minecraft:oak_fence[east=false,north=false,south=false,waterlogged=false,west=false]",
        "partition": "minecraft:white_terracotta",
        "counter": "minecraft:stripped_oak_wood[axis=x]",
        "loom": "minecraft:loom[facing=south]",
        "seat": "minecraft:spruce_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]",
        "fleece": wool("white"),
        "red": wool("red"), "blue": wool("blue"), "yellow": wool("yellow"), "green": wool("green"),
        "purple": wool("purple"), "orange": wool("orange"),
        "vat": "minecraft:water_cauldron[level=3]",
        "cloth-red": "minecraft:red_carpet", "cloth-blue": "minecraft:blue_carpet",
        "cloth-yellow": "minecraft:yellow_carpet", "runner": "minecraft:red_carpet",
        "banner-red": "minecraft:red_wall_banner[facing=south]",
        "banner-blue": "minecraft:blue_wall_banner[facing=south]",
    },
    "place": [
        # The workroom: three looms against the back wall, each with its
        # weaver's seat before it; the fleece heaped by the east wall, the dyed
        # wool by the west, the dye vats.
        ("loom", (3, 1, 2), (3, 1, 2)), ("loom", (7, 1, 2), (7, 1, 2)), ("loom", (11, 1, 2), (11, 1, 2)),
        ("seat", (3, 1, 3), (3, 1, 3)), ("seat", (7, 1, 3), (7, 1, 3)), ("seat", (11, 1, 3), (11, 1, 3)),
        ("fleece", (13, 1, 1), (13, 2, 2)), ("fleece", (12, 1, 1), (12, 1, 1)),
        ("red", (1, 1, 1), (1, 1, 1)), ("blue", (1, 1, 2), (1, 1, 2)), ("yellow", (1, 1, 3), (1, 1, 3)),
        ("vat", (5, 1, 6), (6, 1, 6)),
        # The shop: bolts of cloth stacked on both side walls, cloth laid out
        # on the counter, a runner from the door, banners of the weaver's
        # colours on the partition.
        ("red", (1, 1, 9), (1, 2, 9)), ("blue", (1, 1, 10), (1, 2, 10)), ("yellow", (1, 1, 11), (1, 2, 11)),
        ("green", (14, 1, 9), (14, 2, 9)), ("purple", (14, 1, 10), (14, 2, 10)), ("orange", (14, 1, 11), (14, 2, 11)),
        ("cloth-red", (2, 2, COUNTER_Z), (3, 2, COUNTER_Z)), ("cloth-blue", (5, 2, COUNTER_Z), (6, 2, COUNTER_Z)),
        ("cloth-yellow", (8, 2, COUNTER_Z), (8, 2, COUNTER_Z)),
        ("runner", (7, 1, 12), (7, 1, 14)),
        ("banner-red", (2, 3, 9), (2, 3, 9)), ("banner-blue", (6, 3, 9), (6, 3, 9)),
    ],
    "tall": ("red", "blue", "yellow", "green", "purple", "orange", "fleece"),
    "soft": ("cloth-red", "cloth-blue", "cloth-yellow", "runner", "banner-red", "banner-blue"),
}

BAKERY = {
    "door": "birch",
    "palette": {
        "floor": "minecraft:terracotta",
        "wall": "minecraft:bricks",
        "post": "minecraft:stripped_spruce_log[axis=y]",
        "lid": "minecraft:spruce_planks",
        "parapet": "minecraft:brick_wall[east=none,north=none,south=none,up=true,waterlogged=false,west=none]",
        "partition": "minecraft:smooth_sandstone",
        "counter": "minecraft:stripped_birch_wood[axis=x]",
        "oven": "minecraft:bricks",
        "fire": "minecraft:campfire[facing=south,lit=true,signal_fire=false,waterlogged=false]",
        "chimney": "minecraft:bricks",
        "table": "minecraft:birch_slab[type=top,waterlogged=false]",
        "wheat": "minecraft:hay_block[axis=y]",
        "flour": wool("white"),
        "water": "minecraft:water_cauldron[level=3]",
        "shelf": "minecraft:spruce_slab[type=top,waterlogged=false]",
        "sheaf": "minecraft:hay_block[axis=x]",
    },
    "place": [
        # The bakehouse: the brick oven against the back wall, its fire in
        # the mouth, its chimney through the roof; the kneading table before
        # it, the wheat and the flour sacks by the walls, the water at hand.
        ("oven", (3, 1, 1), (7, 3, 2)), ("fire", (5, 1, 2), (5, 1, 2)),
        ("chimney", (5, 4, 1), (5, 4, 1)), ("chimney", (5, 6, 1), (5, 7, 1)), ("fire", (5, 8, 1), (5, 8, 1)),
        ("table", (4, 1, 4), (7, 1, 4)),
        ("wheat", (12, 1, 1), (13, 2, 1)), ("wheat", (13, 1, 2), (13, 1, 2)),
        ("flour", (1, 1, 1), (1, 2, 2)),
        ("water", (9, 1, 1), (9, 1, 1)),
        # The shop: loaves are sold over the counter; flour sacks and wheat
        # sheaves stand behind it, bread shelves along the partition.
        ("shelf", (1, 2, 9), (8, 2, 9)), ("shelf", (12, 2, 9), (13, 2, 9)),
        ("flour", (2, 1, 10), (3, 1, 10)), ("sheaf", (6, 1, 10), (7, 1, 10)),
    ],
    "tall": ("wheat", "flour", "oven", "shelf"),
}

CARTOGRAPHER = {
    "door": "dark_oak",
    "palette": {
        "floor": "minecraft:dark_oak_planks",
        "wall": "minecraft:oak_planks",
        "post": "minecraft:dark_oak_log[axis=y]",
        "lid": "minecraft:spruce_planks",
        "parapet": "minecraft:dark_oak_fence[east=false,north=false,south=false,waterlogged=false,west=false]",
        "partition": "minecraft:oak_planks",
        "counter": "minecraft:stripped_dark_oak_wood[axis=x]",
        "drafting": "minecraft:cartography_table",
        "lectern": "minecraft:lectern[facing=north,has_book=false,powered=false]",
        "shelves": "minecraft:bookshelf",
        "stool": "minecraft:dark_oak_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]",
        "chart-blue": "minecraft:light_blue_wall_banner[facing=south]",
        "chart-white": "minecraft:white_wall_banner[facing=south]",
        "chart-green": "minecraft:lime_wall_banner[facing=south]",
        "globe": "minecraft:lectern[facing=south,has_book=false,powered=false]",
    },
    "place": [
        # The map room: two drawing tables side by side in the light, a stool
        # before each, the lectern with the survey open on it, shelves of
        # surveys along the back wall.
        ("drafting", (6, 1, 3), (7, 1, 3)),
        ("stool", (6, 1, 4), (7, 1, 4)),
        ("lectern", (10, 1, 4), (10, 1, 4)),
        ("shelves", (1, 1, 1), (5, 3, 1)), ("shelves", (9, 1, 1), (13, 3, 1)),
        ("shelves", (1, 1, 2), (1, 3, 5)),
        # The reception room: charts hung on the partition, a table to show a
        # map on with the lectern beside it, shelves by the east wall.
        ("chart-blue", (2, 3, 9), (2, 3, 9)), ("chart-white", (4, 3, 9), (4, 3, 9)), ("chart-green", (6, 3, 9), (6, 3, 9)),
        ("drafting", (4, 1, 10), (4, 1, 10)),
        ("globe", (7, 1, 10), (7, 1, 10)),
        ("shelves", (14, 1, 9), (14, 3, 12)),
    ],
    "tall": ("shelves",),
    "soft": ("chart-blue", "chart-white", "chart-green"),
}


def well(a):
    """The old well-yard at the lane's end, open on every side: a well — a
    stone ring round its water, a roof on posts over."""
    p = Piece(a)
    sx, sy, sz = p.sx, p.sy, p.sz
    (lo, hi) = p.alloc["space"]
    p.put((lo[0], 0, lo[2]), (hi[0], 0, hi[2]), "paving")
    cx, cz = (lo[0] + hi[0]) // 2, (lo[2] + hi[2]) // 2
    p.put((cx - 1, 1, cz - 1), (cx + 1, 1, cz + 1), "rim")
    # The well's mouth holds its water in a cauldron, so nobody falls in.
    p.put((cx, 1, cz), (cx, 1, cz), "water")
    for (x, z) in ((cx - 1, cz - 1), (cx + 1, cz - 1), (cx - 1, cz + 1), (cx + 1, cz + 1)):
        p.put((x, 2, z), (x, 3, z), "post")
    p.put((cx - 1, 4, cz - 1), (cx + 1, 4, cz + 1), "roof")
    claim_tops_of(p, ("rim", "roof", "post"))
    sf = p.seam("edge/well-front")
    (c0, c1) = sf["cells"]
    p.claim_box(c0, c1, "well-front", air_only=True)
    p.claim_box((0, 1, 0), (sx - 1, sy - 1, sz - 1), "yard", air_only=True)
    palette = {
        "paving": "minecraft:polished_andesite",
        "post": "minecraft:oak_fence[east=false,north=false,south=false,waterlogged=false,west=false]",
        "rim": "minecraft:cobblestone",
        "roof": "minecraft:oak_slab[type=bottom,waterlogged=false]",
        "water": "minecraft:water_cauldron[level=3]",
    }
    contract = {
        "edges": [{"a": "yard", "b": "exterior", "class": "walk", "via": "well-front"}],
        "entry": "yard",
        "no_body": {"tops": {"reason": "the tops of the well's ring and roof, which nobody walks"}},
        "spaces": {"yard": {"envelope": "open"}},
    }
    marks = [("node-well", (lo[0] + 1, 1, hi[2] - 1), "north")]
    return program("the-four-trades-well", p, palette, contract, marks, ("up",))


def main():
    alloc = {a["place"]: a for a in json.loads(pathlib.Path(sys.argv[1]).read_text())}
    here = pathlib.Path(__file__).resolve().parent.parent
    out = here / "programs"
    out.mkdir(exist_ok=True)
    builds = [("lane", lambda a: lane(a)), ("well", lambda a: well(a))]
    for stem, kind, spec in (("smithy", "smithy", SMITHY), ("weaver", "weaver's", WEAVER),
                             ("bakery", "bakery", BAKERY), ("cartographer", "cartographer's", CARTOGRAPHER)):
        builds.append((stem, lambda a, s=stem, k=kind, sp=spec: trade(a, s, k, sp)))
    for stem, build in builds:
        prog = build(alloc[f"node/{stem}"])
        path = out / f"{stem}.json"
        path.write_text(json.dumps(prog, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
