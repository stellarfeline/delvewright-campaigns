#!/usr/bin/env python3
"""Write the six place programs of The Lane of Holdings.

    delvec allocation campaigns/the-lane-of-holdings --all > alloc.json
    python3 campaigns/the-lane-of-holdings/design/build_pieces.py alloc.json

`delvec detail` expands `programs/<place stem>.json` inside the frame the site
plan hands each place. Each piece is stated here as a cell grid in the frame's
own coordinates (x east, y up, z south, the frame's minimum corner at 0) and
written out as a grammar program; the machinery is The Four Trades' own. A
plot is drawn in its play space's coordinates (`px`, `pz` from the play space's
north-west corner, `c` the course over the walk plane): each part is built in
the outline drawn here, and the contract names each part on the spaces and
out-of-walk regions that are it, with `part`. The script prints each part's
claimed columns, which are the numbers the plan declares.
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
    """Holding Lane: a way place three wide, a verge on its south side with
    lamps, walls of the lane's full height on its ring, cut only where a
    holding's way in meets it: the north ring is the wall every holding shares
    with the lane, and no wall is low enough to climb onto from the verge."""
    p = Piece(a)
    sx, sy, sz = p.sx, p.sy, p.sz
    p.put((1, 0, 1), (sx - 2, 0, sz - 2), "road")
    p.put((1, 0, sz - 3), (sx - 2, 0, sz - 2), "verge")
    top = p.alloc["space"][1][1]
    for x in range(sx):
        for z in range(sz):
            if x in (0, sx - 1) or z in (0, sz - 1):
                p.put((x, 1, z), (x, top, z), "wall")
    regions = []
    for s in p.alloc["seams"]:
        stem = s["edge"].split("/", 1)[1]
        (s0, s1) = s["cells"]
        p.put(s0, s1, None)
        p.claim_box(s0, s1, stem)
        regions.append(stem)
    # Lamps, bushes and flowers on the verge.
    clear = range(0)
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
    return program("the-lane-of-holdings-lane", p, palette, contract, marks, ("east", "north", "south", "up", "west"))




# ---------------------------------------------------------------------------
# Plots
# ---------------------------------------------------------------------------

PANE_X = "minecraft:glass_pane[east=true,north=false,south=false,waterlogged=false,west=true]"
PANE_Z = "minecraft:glass_pane[east=false,north=true,south=true,waterlogged=false,west=false]"
FENCE = "minecraft:oak_fence[east=false,north=false,south=false,waterlogged=false,west=false]"
PARTS = {}


class Plot(Piece):
    """A piece drawn in its play space's coordinates."""

    def __init__(self, alloc):
        super().__init__(alloc)
        (self.lo, self.hi) = alloc["space"]
        self.w = self.hi[0] - self.lo[0] + 1
        self.d = self.hi[2] - self.lo[2] + 1
        self.air = self.hi[1] - self.lo[1] + 1

    def at(self, px, c, pz):
        return (self.lo[0] + px, self.lo[1] + c, self.lo[2] + pz)

    def rect(self, a, b, c0, c1, role):
        self.put(self.at(a[0], c0, a[1]), self.at(b[0], c1, b[1]), role)

    def cell_put(self, px, c, pz, role):
        self.put(self.at(px, c, pz), self.at(px, c, pz), role)

    def claim_rect(self, a, b, c0, c1, region, air_only=True):
        self.claim_box(self.at(a[0], c0, a[1]), self.at(b[0], c1, b[1]), region, air_only)

    def claim_cols(self, cols, c0, c1, region, air_only=True):
        for (px, pz) in cols:
            self.claim_rect((px, pz), (px, pz), c0, c1, region, air_only)

    def floor(self, role, a=None, b=None):
        a = a or (0, 0)
        b = b or (self.w - 1, self.d - 1)
        self.rect(a, b, -1, -1, role)

    def ring(self, role, height=3):
        """`role` on every ring cell this place owns, `height` courses high."""
        for x in range(self.sx):
            for z in range(self.sz):
                if x in (0, self.sx - 1) or z in (0, self.sz - 1):
                    for y in range(self.lo[1], self.lo[1] + height):
                        if (x, y, z) not in self.fixed:
                            self.block[(x, y, z)] = role

    def building(self, a, b, height, wall="wall", lid="lid", parapet=None):
        """Walls round `a`..`b` (play columns, inclusive) for courses
        0..height-1, the lid at `height`, air inside; returns the interior's
        columns."""
        (x0, z0), (x1, z1) = a, b
        for px in range(x0, x1 + 1):
            for pz in range(z0, z1 + 1):
                edge = px in (x0, x1) or pz in (z0, z1)
                self.rect((px, pz), (px, pz), 0, height - 1, wall if edge else None)
                self.cell_put(px, height, pz, lid)
                if parapet and edge:
                    # Two courses: the roof inside it is closed, and nobody
                    # leaves it for a neighbour's ground.
                    for c in (height + 1, height + 2):
                        if c < self.air:
                            self.cell_put(px, c, pz, parapet)
        return [(px, pz) for px in range(x0 + 1, x1) for pz in range(z0 + 1, z1)]

    def door_in(self, px, pz, facing, kind="oak", hinge="left"):
        self.cell_put(px, 0, pz, ("door", facing, kind, hinge))
        self.cell_put(px, 1, pz, ("door-top", facing, kind, hinge))

    def lamp(self, px, pz):
        """A lamp set flush in the ground: light with nothing to climb."""
        self.cell_put(px, -1, pz, "glow")

    def seam_cols(self, edge):
        (a, b) = self.seam(edge)["cells"]
        return a, b


def door_palette(p, palette):
    """Every door the plot placed, as its own role."""
    for (c, role) in list(p.block.items()):
        if isinstance(role, tuple):
            kind, facing, wood, hinge = role
            name = f"{kind}-{facing}-{wood}-{hinge}"
            half = "lower" if kind == "door" else "upper"
            palette[name] = door(facing, half, hinge=hinge, kind=wood)
            p.block[c] = name


def roof_and_tops(p, footprints, tall_roles):
    """The air over every lid is `roof`; the top of anything tall a body
    cannot climb onto is `tops`."""
    for (px, pz) in footprints:
        for c in range(0, p.air):
            x, y, z = p.at(px, c, pz)
            below = p.block.get((x, y - 1, z))
            if below in ("lid", "parapet", "chimney") and p.block.get((x, y, z)) is None:
                for cc in range(c, p.air):
                    p.claim_box(p.at(px, cc, pz), p.at(px, cc, pz), "roof", air_only=True)
                break
    for (x, y, z), role in list(p.block.items()):
        if role in tall_roles and p.block.get((x, y + 1, z)) is None and y + 1 <= p.hi[1]:
            p.claim_box((x, y + 1, z), (x, y + 1, z), "tops")


def ring_tops(p, role="hedge"):
    for (x, y, z), r in list(p.block.items()):
        if r == role and p.block.get((x, y + 1, z)) is None and y + 1 < p.sy:
            if x in (0, p.sx - 1) or z in (0, p.sz - 1):
                p.claim_box((x, y + 1, z), (x, y + 1, z), "tops")


def count(p, region):
    return len({(x, z) for (x, y, z), r in p.claim.items() if r == region})


def record(stem, p, parts):
    """The claimed columns of each part: the union of its regions'."""
    out = {}
    for part, regions in parts.items():
        out[part] = len({(x, z) for (x, y, z), r in p.claim.items() if r in regions})
    PARTS[stem] = out


def dwelling(a):
    p = Plot(a)
    p.floor("grass")
    p.ring("hedge")
    # The L: the house (walls px 1..12, pz 3..13) and the cart shed against
    # its east wall (px 12..18, pz 8..13), each walls of four courses under a
    # flat lid with a parapet.
    house = p.building((1, 3), (12, 13), 4, parapet="parapet")
    shed = p.building((12, 8), (18, 13), 4, parapet="parapet")
    p.floor("planks", (2, 4), (11, 12))
    p.floor("shed-floor", (13, 9), (17, 12))
    # Doors: the house's front door onto the front strip, the door through
    # the house's east wall into the shed, the shed's door onto the back yard.
    p.door_in(6, 13, "south")
    p.door_in(12, 11, "east", hinge="right")
    p.door_in(15, 8, "north", kind="spruce")
    # Windows.
    for x0 in (3, 9):
        p.rect((x0, 13), (x0 + 1, 13), 1, 2, "pane-x")
    for x0 in (4, 8):
        p.rect((x0, 3), (x0 + 1, 3), 1, 2, "pane-x")
    p.rect((1, 6), (1, 7), 1, 2, "pane-z")
    # The side paths' lamps, set in the house's west wall and the shed's east.
    p.cell_put(1, 2, 10, "glow")
    p.cell_put(18, 2, 10, "glow")
    # Inside the house: the hearth against the north wall under its hood, the
    # table, the beds, the lamps.
    p.cell_put(5, 0, 4, "brick")
    p.cell_put(7, 0, 4, "brick")
    p.cell_put(6, 0, 4, "fire")
    p.rect((5, 4), (7, 4), 2, 3, "brick")
    p.rect((5, 8), (7, 8), 0, 0, "table")
    p.cell_put(5, 0, 9, "chair")
    p.cell_put(7, 0, 9, "chair")
    p.rect((9, 11), (10, 12), 0, 0, "bedding")
    p.rect((2, 11), (3, 12), 0, 0, "bedding")
    for (x, z) in ((3, 6), (9, 6), (3, 10), (9, 10)):
        p.cell_put(x, 3, z, "hanging")
    # Inside the shed: the cart (a bed of slabs on its wheels) and the hay.
    p.rect((13, 9), (14, 10), 0, 0, "cart")
    p.rect((16, 9), (17, 9), 0, 1, "hay")
    p.cell_put(13, 0, 12, "composter")
    p.cell_put(15, 3, 11, "hanging")
    # The front strip: a path from the gate to the door; the flower bed under
    # the windows behind a low hedge.
    # The front is open to the lane along its whole width: its last row is
    # the crossing, and a path runs from it to the door.
    gate_a, gate_b = p.seam_cols("edge/dwelling-way")
    p.floor("path", (6, 14), (6, 19))
    bed = [(px, pz) for px in range(8, 13) for pz in (14, 15)]
    for i, (px, pz) in enumerate(bed):
        p.cell_put(px, 0, pz, ("poppy", "dandelion", "cornflower")[i % 3])
    p.rect((8, 16), (12, 16), 0, 0, "low-hedge")
    p.lamp(3, 17)
    p.lamp(12, 17)
    # The side paths, west and east of the house and the shed.
    p.floor("gravel", (0, 0), (0, 19))
    p.floor("gravel", (19, 0), (19, 19))
    # The back yard: the washing line's posts, the vegetable rows, a lamp.
    p.rect((3, 1), (3, 1), 0, 1, "fence")
    p.rect((8, 1), (8, 1), 0, 1, "fence")
    p.rect((13, 4), (16, 4), 0, 0, "pumpkin")
    p.rect((13, 6), (16, 6), 0, 0, "melon")
    p.lamp(11, 1)
    p.lamp(18, 1)
    # Regions, the narrow ones first.
    p.claim_box(gate_a, gate_b, "dwelling-way")
    p.claim_rect((6, 13), (6, 13), 0, 1, "house-door", air_only=False)
    p.claim_rect((12, 11), (12, 11), 0, 1, "inner-door", air_only=False)
    p.claim_rect((15, 8), (15, 8), 0, 1, "shed-door", air_only=False)
    ring_tops(p)
    roof_and_tops(p, [(x, z) for x in range(1, 19) for z in range(3, 14)],
                  ("hay", "fence", "lantern", "low-hedge"))
    p.claim_cols(bed, 0, 1, "bed", air_only=False)
    # The side paths join the front strip to the back yard through a gap at
    # the back yard's edge, one each side.
    p.claim_rect((0, 3), (0, 3), 0, 1, "west-gap", air_only=False)
    p.claim_rect((19, 8), (19, 8), 0, 1, "east-gap", air_only=False)
    p.claim_cols(house, 0, 3, "house")
    p.claim_cols(shed, 0, 3, "shed")
    front = [(x, z) for x in range(1, 19) for z in range(14, 19) if (x, z) not in bed and not (z == 16 and 8 <= x <= 12)]
    front += [(0, z) for z in range(4, 19)] + [(19, z) for z in range(9, 19)]
    p.claim_cols(front, 0, p.air - 1, "front")
    back = [(x, z) for x in range(0, 20) for z in range(0, 3)] + [(x, z) for x in range(13, 20) for z in range(3, 8)]
    p.claim_cols(back, 0, p.air - 1, "back")
    record("dwelling", p, {"part/house": {"house"}, "part/garage": {"shed"}, "part/front": {"front"},
                           "part/back": {"back"}, "part/bed": {"bed"}})
    palette = {
        "grass": "minecraft:grass_block[snowy=false]",
        "hedge": HEDGE, "low-hedge": HEDGE,
        "wall": "minecraft:stripped_oak_log[axis=y]",
        "lid": "minecraft:spruce_planks",
        "parapet": "minecraft:spruce_planks",
        "planks": "minecraft:oak_planks",
        "shed-floor": "minecraft:coarse_dirt",
        "brick": "minecraft:bricks",
        "fire": "minecraft:campfire[facing=south,lit=true,signal_fire=false,waterlogged=false]",
        "table": "minecraft:spruce_slab[type=top,waterlogged=false]",
        "chair": "minecraft:spruce_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]",
        "bedding": "minecraft:red_wool",
        "hanging": HANGING,
        "glow": "minecraft:sea_lantern",
        "cart": "minecraft:oak_slab[type=bottom,waterlogged=false]",
        "hay": "minecraft:hay_block[axis=y]",
        "composter": "minecraft:composter[level=0]",
        "path": "minecraft:dirt_path",
        "gravel": "minecraft:gravel",
        "poppy": "minecraft:poppy", "dandelion": "minecraft:dandelion", "cornflower": "minecraft:cornflower",
        "post": POST, "lantern": LANTERN,
        "fence": FENCE,
        "pumpkin": "minecraft:pumpkin", "melon": "minecraft:melon",
        "pane-x": PANE_X, "pane-z": PANE_Z,
    }
    door_palette(p, palette)
    contract = {
        "edges": [
            {"a": "front", "b": "exterior", "class": "walk", "via": "dwelling-way"},
            {"a": "front", "b": "house", "class": "walk", "via": "house-door"},
            {"a": "house", "b": "shed", "class": "walk", "via": "inner-door"},
            {"a": "shed", "b": "back", "class": "walk", "via": "shed-door"},
            {"a": "front", "b": "back", "class": "walk", "via": "west-gap"},
            {"a": "front", "b": "back", "class": "walk", "via": "east-gap"},
        ],
        "entry": "front",
        "no_body": {
            "bed": {"reason": "the flower bed behind the low hedge; nobody walks it", "part": "part/bed"},
            "roof": {"reason": "the flat roofs inside their parapets, which nobody walks"},
            "tops": {"reason": "the tops of the hedges, posts, lamps and hay, which nobody walks"},
        },
        "spaces": {
            "front": {"envelope": "open", "part": "part/front"},
            "back": {"envelope": "open", "part": "part/back"},
            "house": {"envelope": "enclosed", "part": "part/house"},
            "shed": {"envelope": "enclosed", "part": "part/garage"},
        },
    }
    marks = [("node-dwelling", p.at(4, 0, 18), "north")]
    return program("the-lane-of-holdings-dwelling", p, palette, contract, marks, ("east", "north", "up", "west"))


def forge(a):
    p = Plot(a)
    p.floor("yard-floor")
    p.ring("hedge")
    # The shop and workroom at the lane's edge (walls px 0..8, pz 3..13): its
    # front wall stands on the play space's last row, the door in the plan's
    # seam; a partition at pz 8 divides the shop a customer enters from the
    # workroom where the forge burns.
    p.building((0, 3), (8, 13), 4, wall="stone", parapet="parapet")
    p.floor("stone-floor", (1, 4), (7, 12))
    p.rect((1, 8), (7, 8), 0, 3, "stone")
    door_a, door_b = p.seam_cols("edge/forge-way")
    dx, dz = door_a[0] - p.lo[0], door_a[2] - p.lo[2]
    p.door_in(dx, dz, "south", kind="spruce")
    p.door_in(6, 8, "north", kind="spruce", hinge="right")
    p.door_in(8, 5, "east", kind="spruce")
    p.rect((1, 13), (2, 13), 1, 2, "pane-x")
    p.rect((6, 13), (7, 13), 1, 2, "pane-x")
    p.rect((2, 8), (3, 8), 1, 2, "pane-x")
    # The workroom: the forge against the back wall under its hood, the anvil
    # before it, the quench and the coal at hand.
    p.cell_put(1, 0, 4, "brick")
    p.cell_put(3, 0, 4, "brick")
    p.cell_put(2, 0, 4, "fire")
    p.rect((1, 4), (3, 4), 2, 3, "brick")
    p.cell_put(2, 0, 6, "anvil")
    p.cell_put(5, 0, 4, "quench")
    p.cell_put(7, 0, 4, "coal")
    # The shop: the counter across it with a pass at its east end to the
    # inner door, finished ironwork on a rack behind it.
    p.rect((1, 10), (5, 10), 0, 0, "counter")
    p.rect((1, 9), (3, 9), 0, 1, "rack")
    for (x, z) in ((3, 6), (3, 11), (6, 11)):
        p.cell_put(x, 3, z, "hanging")
    # The iron store in the yard's north-east corner: walls round four cells,
    # no door; seen, never entered.
    store = p.building((12, 0), (15, 3), 4, wall="stone", parapet="parapet")
    p.floor("stone-floor", (13, 1), (14, 2))
    p.cell_put(13, 0, 1, "iron")
    # The work yard: the grindstone, the quench trough, the wood stack, lamps.
    p.cell_put(10, 0, 7, "grindstone")
    p.cell_put(10, 0, 10, "quench")
    p.rect((11, 11), (12, 12), 0, 0, "logs")
    p.lamp(12, 8)
    p.lamp(4, 1)
    p.lamp(15, 5)
    p.claim_box(door_a, door_b, "forge-way")
    p.claim_rect((6, 8), (6, 8), 0, 1, "inner-door", air_only=False)
    p.claim_rect((8, 5), (8, 5), 0, 1, "back-door", air_only=False)
    ring_tops(p)
    roof_and_tops(p, [(x, z) for x in range(0, 16) for z in range(0, 14)], ("rack", "logs", "lantern"))
    p.claim_cols(store, 0, 3, "store")
    p.claim_cols([(x, z) for x in range(1, 8) for z in range(9, 13)], 0, 3, "shop")
    p.claim_cols([(x, z) for x in range(1, 8) for z in range(4, 8)], 0, 3, "work")
    shop_foot = {(x, z) for x in range(0, 9) for z in range(3, 14)}
    store_foot = {(x, z) for x in range(12, 16) for z in range(0, 4)}
    yard = [(x, z) for x in range(16) for z in range(14) if (x, z) not in shop_foot and (x, z) not in store_foot]
    p.claim_cols(yard, 0, p.air - 1, "yard")
    record("forge", p, {"part/shop": {"shop", "work"}, "part/yard": {"yard"}, "part/store": {"store"}})
    palette = {
        "yard-floor": "minecraft:coarse_dirt",
        "hedge": HEDGE,
        "stone": "minecraft:cobblestone",
        "stone-floor": "minecraft:stone_bricks",
        "lid": "minecraft:spruce_planks",
        "parapet": "minecraft:cobblestone",
        "brick": "minecraft:bricks",
        "fire": "minecraft:campfire[facing=south,lit=true,signal_fire=false,waterlogged=false]",
        "anvil": "minecraft:anvil[facing=east]",
        "quench": "minecraft:water_cauldron[level=3]",
        "coal": "minecraft:coal_block",
        "counter": "minecraft:stripped_spruce_wood[axis=x]",
        "rack": "minecraft:iron_bars[east=true,north=false,south=false,waterlogged=false,west=true]",
        "hanging": HANGING,
        "iron": "minecraft:iron_block",
        "glow": "minecraft:sea_lantern",
        "grindstone": "minecraft:grindstone[face=floor,facing=south]",
        "logs": "minecraft:oak_log[axis=x]",
        "post": POST, "lantern": LANTERN,
        "pane-x": PANE_X,
    }
    door_palette(p, palette)
    contract = {
        "edges": [
            {"a": "shop", "b": "exterior", "class": "walk", "via": "forge-way"},
            {"a": "shop", "b": "work", "class": "walk", "via": "inner-door"},
            {"a": "work", "b": "yard", "class": "walk", "via": "back-door"},
        ],
        "entry": "shop",
        "no_body": {
            "store": {"reason": "the iron store, shut; nobody goes in", "part": "part/store"},
            "roof": {"reason": "the flat roofs, which nobody walks"},
            "tops": {"reason": "the tops of the hedges, the rack, the logs and the lamps, which nobody walks"},
        },
        "spaces": {
            "shop": {"envelope": "enclosed", "part": "part/shop"},
            "work": {"envelope": "enclosed", "part": "part/shop"},
            "yard": {"envelope": "open", "part": "part/yard"},
        },
    }
    marks = [("node-forge", p.at(4, 0, 11), "north")]
    return program("the-lane-of-holdings-forge", p, palette, contract, marks, ("east", "north", "up", "west"))


CHAPEL_PALETTE = {
    "wall": "minecraft:stone_bricks",
    "floor": "minecraft:polished_andesite",
    "lid": "minecraft:dark_oak_planks",
    "altar": "minecraft:chiseled_stone_bricks",
    "candle": LANTERN,
    "pew": "minecraft:spruce_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]",
    "hanging": HANGING,
    "pane-z": PANE_Z,
    "pane-x": PANE_X,
    "parapet-wall": "minecraft:stone_bricks",
}


def chapel_inside(p, x0, x1, z0, z1, top):
    """The hall's furniture: the altar at the north end with its candles,
    two ranks of pews either side of the aisle, the lamps."""
    mid = (x0 + x1) // 2
    p.rect((mid - 1, z0), (mid + 1, z0), 0, 0, "altar")
    for z in (z0 + 3, z0 + 5, z0 + 7):
        if z < z1:
            p.rect((x0, z), (mid - 1, z), 0, 0, "pew")
            p.rect((mid + 1, z), (x1, z), 0, 0, "pew")
    for (x, z) in ((x0 + 1, z0 + 2), (x1 - 1, z0 + 2), (x0 + 1, z1 - 2), (x1 - 1, z1 - 2)):
        p.cell_put(x, top, z, "hanging")


def altar_top(p):
    """The lamp on the altar, and the air over the altar's ends: the
    altar's top, out of walk."""
    for (x, y, z), role in list(p.block.items()):
        if role == "altar" and p.block.get((x, y + 1, z)) in (None, "candle"):
            p.claim_box((x, y + 1, z), (x, y + 1, z), "altar", air_only=False)


def chapel(a):
    """The chapel that is the whole of its plot: its walls on the ring it owns
    (west, north and east) and on the play space's south row before the
    lane's wall, its lid over all, one hall inside."""
    p = Plot(a)
    p.floor("floor")
    h = 5
    # Walls on the ring cells this place owns — west, north and east — five
    # courses high; the south ring is the lane's.
    p.ring("wall", height=h)
    for x in range(p.sx):
        for y in range(p.lo[1], p.lo[1] + h):
            if (x, y, p.sz - 1) not in p.fixed:
                p.block.pop((x, y, p.sz - 1), None)
    p.rect((0, p.d - 1), (p.w - 1, p.d - 1), 0, h - 1, "wall")
    door_a, door_b = p.seam_cols("edge/chapel-way")
    dx, dz = door_a[0] - p.lo[0], door_a[2] - p.lo[2]
    p.door_in(dx, dz, "south", kind="dark_oak")
    # The lid over the ring and the hall, inside the frame's south edge.
    for x in range(p.sx):
        for z in range(p.sz):
            y = p.lo[1] + h
            if (x, y, z) not in p.fixed and z <= p.lo[2] + p.d - 1:
                p.block[(x, y, z)] = "lid"
    # A parapet of two courses round the roof: nobody leaves it.
    for x in range(p.sx):
        for z in range(p.lo[2] + p.d):
            if x in (0, p.sx - 1) or z in (0, p.lo[2] + p.d - 1):
                for c in (h + 1, h + 2):
                    y = p.lo[1] + c
                    if (x, y, z) not in p.fixed:
                        p.block[(x, y, z)] = "parapet-wall"
    # Tall windows in the side walls (the ring), a window either side of the door.
    for pz in (2, 5, 8):
        p.put((0, p.lo[1] + 1, p.lo[2] + pz), (0, p.lo[1] + 3, p.lo[2] + pz), "pane-z")
        p.put((p.sx - 1, p.lo[1] + 1, p.lo[2] + pz), (p.sx - 1, p.lo[1] + 3, p.lo[2] + pz), "pane-z")
    p.rect((1, p.d - 1), (2, p.d - 1), 1, 3, "pane-x")
    p.rect((p.w - 3, p.d - 1), (p.w - 2, p.d - 1), 1, 3, "pane-x")
    chapel_inside(p, 0, p.w - 1, 0, p.d - 2, h - 1)
    p.claim_box(door_a, door_b, "chapel-way")
    roof_and_tops(p, [(x, z) for x in range(-1, p.w + 1) for z in range(-1, p.d)], ())
    hall = [(x, z) for x in range(p.w) for z in range(p.d - 1)]
    p.claim_cols(hall, 0, h - 1, "hall")
    record("chapel", p, {"part/chapel": {"hall"}})
    palette = dict(CHAPEL_PALETTE)
    door_palette(p, palette)
    contract = {
        "edges": [{"a": "hall", "b": "exterior", "class": "walk", "via": "chapel-way"}],
        "entry": "hall",
        "no_body": {"roof": {"reason": "the chapel's flat roof, which nobody walks"}},
        "no_body_majority_ack": "a chapel that is its plot owns its roof, and its flat roof is more standable surface than the hall under it; nobody walks it",
        "spaces": {"hall": {"envelope": "enclosed", "part": "part/chapel"}},
    }
    marks = [("node-chapel", p.at(dx, 0, dz - 2), "north")]
    return program("the-lane-of-holdings-chapel", p, palette, contract, marks, ("east", "north", "up", "west"))


def chapel_lidded(a):
    """The same chapel cut as a lidded box: walls round the ring, the lid on
    the frame's top course, the same hall inside."""
    p = Plot(a)
    p.floor("floor")
    sx, sy, sz = p.sx, p.sy, p.sz
    lid = p.alloc["roof"]["lid_y"]
    for x in range(sx):
        for z in range(sz):
            if x in (0, sx - 1) or z in (0, sz - 1):
                p.put((x, 1, z), (x, lid - 1, z), "wall")
                p.put((x, lid + 1, z), (x, lid + 2, z), "parapet-wall")
    p.put((0, lid, 0), (sx - 1, lid, sz - 1), "lid")
    door_a, door_b = p.seam_cols("edge/chapel-lidded-way")
    p.put(door_a, door_a, ("door", "south", "dark_oak", "left"))
    p.put(door_b, door_b, ("door-top", "south", "dark_oak", "left"))
    for pz in (2, 5, 8):
        p.put((0, 2, p.lo[2] + pz), (0, 4, p.lo[2] + pz), "pane-z")
        p.put((sx - 1, 2, p.lo[2] + pz), (sx - 1, 4, p.lo[2] + pz), "pane-z")
    p.put((2, 2, sz - 1), (3, 4, sz - 1), "pane-x")
    p.put((sx - 4, 2, sz - 1), (sx - 3, 4, sz - 1), "pane-x")
    chapel_inside(p, 0, p.w - 1, 0, p.d - 1, p.air - 1)
    p.claim_box(door_a, door_b, "chapel-lidded-way")
    p.claim_box((0, lid + 1, 0), (sx - 1, sy - 1, sz - 1), "roof", air_only=True)
    p.claim_cols([(x, z) for x in range(p.w) for z in range(p.d)], 0, p.air - 1, "hall")
    palette = dict(CHAPEL_PALETTE)
    door_palette(p, palette)
    contract = {
        "edges": [{"a": "hall", "b": "exterior", "class": "walk", "via": "chapel-lidded-way"}],
        "entry": "hall",
        "no_body": {
            "roof": {"reason": "the flat roof inside its parapet, which nobody walks"},
        },
        "no_body_majority_ack": "a lidded chapel owns its roof, and its flat roof is more standable surface than the hall under it; nobody walks it",
        "spaces": {"hall": {"envelope": "enclosed"}},
    }
    dx = door_a[0] - p.lo[0]
    marks = [("node-chapel-lidded", p.at(dx, 0, p.d - 3), "north")]
    return program("the-lane-of-holdings-chapel-lidded", p, palette, contract, marks,
                   ("east", "north", "south", "up", "west"))


def byre(a):
    p = Plot(a)
    p.floor("pen-floor")
    p.ring("hedge")
    # The byre in the pen's north-west corner: walls px 0..7, pz 0..6 of five
    # courses under a lid, its door in the south wall onto the pen.
    # Its lid on the frame's top course: no roof inside the box to stand on.
    inside = p.building((0, 0), (7, 6), p.air - 1, wall="planks", parapet=None)
    p.floor("straw", (1, 1), (6, 5))
    p.door_in(4, 6, "south", kind="spruce")
    p.rect((2, 6), (2, 6), 1, 1, "pane-x")
    p.rect((6, 6), (6, 6), 1, 1, "pane-x")
    p.rect((1, 1), (2, 2), 0, 1, "hay")
    p.cell_put(6, 0, 1, "trough")
    p.rect((4, 1), (4, 3), 0, 0, "stall")
    for (x, z) in ((3, 3), (6, 4)):
        p.cell_put(x, p.air - 2, z, "hanging")
    # The pen: hay scattered, the trough, the lamps.
    p.rect((8, 9), (9, 9), 0, 0, "hay")
    p.cell_put(10, 0, 4, "trough")
    p.lamp(9, 1)
    p.lamp(3, 9)
    p.lamp(12, 9)
    gate_a, gate_b = p.seam_cols("edge/byre-way")
    p.claim_box(gate_a, gate_b, "byre-way")
    p.claim_rect((4, 6), (4, 6), 0, 1, "byre-door", air_only=False)
    ring_tops(p)
    roof_and_tops(p, [], ("hay", "lantern", "stall"))
    p.claim_cols(inside, 0, p.air - 2, "byre")
    foot = {(x, z) for x in range(0, 8) for z in range(0, 7)}
    pen = [(x, z) for x in range(14) for z in range(12) if (x, z) not in foot]
    p.claim_cols(pen, 0, p.air - 1, "pen")
    record("byre", p, {"part/byre": {"byre"}, "part/pen": {"pen"}})
    palette = {
        "pen-floor": "minecraft:grass_block[snowy=false]",
        "hedge": HEDGE,
        "planks": "minecraft:spruce_planks",
        "lid": "minecraft:dark_oak_planks",
        "straw": "minecraft:coarse_dirt",
        "hay": "minecraft:hay_block[axis=y]",
        "trough": "minecraft:water_cauldron[level=3]",
        "stall": FENCE,
        "glow": "minecraft:sea_lantern",
        "hanging": HANGING,
        "post": POST, "lantern": LANTERN,
        "pane-x": PANE_X,
    }
    door_palette(p, palette)
    contract = {
        "edges": [
            {"a": "pen", "b": "exterior", "class": "walk", "via": "byre-way"},
            {"a": "pen", "b": "byre", "class": "walk", "via": "byre-door"},
        ],
        "entry": "pen",
        "no_body": {
            "tops": {"reason": "the tops of the hedges, the hay, the stall and the lamps, which nobody walks"},
        },
        "spaces": {
            "byre": {"envelope": "enclosed", "part": "part/byre"},
            "pen": {"envelope": "open", "part": "part/pen"},
        },
    }
    marks = [("node-byre", p.at(10, 0, 7), "north")]
    return program("the-lane-of-holdings-byre", p, palette, contract, marks, ("east", "north", "up", "west"))


def main():
    alloc = {a["place"]: a for a in json.loads(pathlib.Path(sys.argv[1]).read_text())}
    here = pathlib.Path(__file__).resolve().parent.parent
    out = here / "programs"
    out.mkdir(exist_ok=True)
    builds = [("lane", lane), ("dwelling", dwelling), ("forge", forge), ("chapel", chapel),
              ("chapel-lidded", chapel_lidded), ("byre", byre)]
    for stem, build in builds:
        prog = build(alloc[f"node/{stem}"])
        path = out / f"{stem}.json"
        path.write_text(json.dumps(prog, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
        print(f"wrote {path}")
    for stem, parts in PARTS.items():
        print(stem, json.dumps(parts))


if __name__ == "__main__":
    main()
