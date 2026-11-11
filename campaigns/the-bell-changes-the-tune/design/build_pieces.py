#!/usr/bin/env python3
"""Write the two place programs of The Bell Changes the Tune.

    python3 campaigns/the-bell-changes-the-tune/design/build_pieces.py

`delvec detail` expands `programs/<place stem>.json` inside the frame the site
plan hands each place (`delvec allocation <campaign> <place>` prints it). Each
piece is stated here as a cell grid in the frame's own coordinates (x east,
y up, z south, the frame's minimum corner at 0) and written out as a grammar
program: the grid is cut along x into runs of identical slices, each slice
along z, each column along y, so every leaf is one material over one box,
wrapped in the contract region it belongs to.

A cell is a palette role (a block), `None` (air the piece owns) or `SKIP` (a
cell the piece does not own: a neighbour's, the ring's fixed ground, the
site's fill), which the verb writes as `structure_void`.

`--light` prints, per piece, a rough block-light estimate of every walk cell
(light spread by steps through non-solid cells, sky light ignored), so the
lamps can be placed while the room is designed. The engine's own proof is
the judge; this only says where to look.
"""
import json
import pathlib
import sys

VERSION = "1.9.0"
SKIP = "__skip__"


class Piece:
    def __init__(self, size):
        self.sx, self.sy, self.sz = size
        self.block = {}
        self.claim = {}

    def put(self, lo, hi, role):
        for x in range(lo[0], hi[0] + 1):
            for y in range(lo[1], hi[1] + 1):
                for z in range(lo[2], hi[2] + 1):
                    self.block[(x, y, z)] = role

    def skip(self, lo, hi):
        self.put(lo, hi, SKIP)

    def claim_cells(self, cells, region):
        for c in cells:
            if self.block.get(c) == SKIP or c in self.claim:
                continue
            self.claim[c] = region

    def claim_box(self, lo, hi, region):
        self.claim_cells(
            [(x, y, z)
             for x in range(lo[0], hi[0] + 1)
             for y in range(lo[1], hi[1] + 1)
             for z in range(lo[2], hi[2] + 1)],
            region,
        )

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

    def light_report(self, solid_roles, lamps, floor_y, space):
        """Rough block light at every walk cell inside `space` (x0,z0,x1,z1)."""
        level = {}
        frontier = []
        for pos, lum in lamps:
            level[pos] = lum
            frontier.append(pos)
        while frontier:
            nxt = []
            for (x, y, z) in frontier:
                lum = level[(x, y, z)] - 1
                if lum <= 0:
                    continue
                for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
                    n = (x + d[0], y + d[1], z + d[2])
                    if not (0 <= n[0] < self.sx and 0 <= n[1] < self.sy and 0 <= n[2] < self.sz):
                        continue
                    if self.block.get(n) in solid_roles:
                        continue
                    if level.get(n, 0) < lum:
                        level[n] = lum
                        nxt.append(n)
            frontier = nxt
        x0, z0, x1, z1 = space
        dark = []
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                c = (x, floor_y, z)
                if self.block.get(c) is not None:
                    continue
                if level.get(c, 0) < 7:
                    dark.append((x, z, level.get(c, 0)))
        return dark


def program(name, piece, palette, contract, marks, shown_faces):
    body = piece.body()
    for stem, pos, facing in marks:
        body = {"body": body, "mark": {
            "anchor": stem, "at": "offset", "facing": facing,
            "x": {"expr": "int", "value": pos[0]},
            "y": {"expr": "int", "value": pos[1]},
            "z": {"expr": "int", "value": pos[2]},
        }, "op": "mark"}
    return {
        "contract": contract,
        "name": name,
        "palette": palette,
        "params": {},
        "rules": {"piece": [{"body": body, "weight": 1}]},
        "shown_faces": shown_faces,
        "start": "piece",
        "version": VERSION,
    }


WALL_MIX = [
    {"block": "minecraft:stone_bricks", "weight": 6},
    {"block": "minecraft:mossy_stone_bricks", "weight": 2},
    {"block": "minecraft:cracked_stone_bricks", "weight": 1},
]
LANTERN = "minecraft:lantern[hanging=false,waterlogged=false]"
HANGING = "minecraft:lantern[hanging=true,waterlogged=false]"
POST = "minecraft:dark_oak_fence[east=false,north=false,south=false,waterlogged=false,west=false]"

# Yard lamp posts: a fence post with a lantern on it (local x, z).
YARD_LAMPS = [
    (11, 5), (14, 5), (11, 11), (14, 11), (11, 17), (14, 17),
    (4, 3), (7, 8), (4, 13), (7, 18),
    (21, 8), (18, 13), (21, 18), (18, 3), (2, 18), (24, 5),
]
# Headstones (local x, z): one block each, a grave mound of coarse dirt south
# of it in the ground course.
YARD_STONES = [
    (3, 6), (5, 6), (8, 5),
    (3, 10), (5, 10), (8, 11),
    (3, 16), (5, 15), (9, 14),
    (17, 6), (19, 7),
    (16, 9), (19, 10), (22, 11),
    (16, 15), (20, 15), (22, 14),
    (17, 19), (19, 17), (4, 19),
]


def yard():
    """The churchyard. Frame 26 x 11 x 22 from (8183, 63, 8199); the plot is
    x 1-24, z 1-20 with its ground at local y 0 and the walk at y 1; the ring
    (x 0, x 25, z 0, z 21) is where the churchyard wall stands, except the
    north ring over x 9-17, which is the chapel's."""
    p = Piece((26, 11, 22))
    # What the yard does not own.
    p.skip((9, 1, 0), (17, 10, 0))             # the chapel's front
    p.skip((0, 0, 0), (0, 0, 21))              # the ring's fixed ground
    p.skip((1, 0, 0), (25, 0, 0))
    p.skip((1, 0, 21), (25, 0, 21))
    p.skip((25, 0, 1), (25, 0, 20))
    # The handed ground: grass, with the flagstone path up the middle.
    p.put((1, 0, 1), (24, 0, 20), "grass")
    p.put((12, 0, 1), (13, 0, 20), "flag")
    # The churchyard wall: two courses of stone and a capping slab.
    def wall(lo, hi):
        p.put((lo[0], 1, lo[1]), (hi[0], 2, hi[1]), "wall")
        p.put((lo[0], 3, lo[1]), (hi[0], 3, hi[1]), "coping")
    wall((0, 0), (0, 21))
    wall((25, 0), (25, 21))
    wall((1, 21), (24, 21))
    wall((1, 0), (8, 0))
    wall((18, 0), (24, 0))
    # The lychgate in the south wall: two timber posts, a rail across the
    # gateway (shut: the party has come in), and a small pitched roof.
    p.put((12, 1, 21), (13, 3, 21), None)
    p.put((11, 1, 21), (11, 3, 21), "gatepost")
    p.put((14, 1, 21), (14, 3, 21), "gatepost")
    p.put((12, 1, 21), (13, 2, 21), "rail")
    p.put((12, 3, 21), (13, 3, 21), "gate-head")
    p.put((10, 4, 20), (15, 4, 21), "gate-roof")
    p.put((11, 3, 20), (11, 3, 20), "bracket")
    p.put((14, 3, 20), (14, 3, 20), "bracket")
    # Headstones and their mounds.
    for x, z in YARD_STONES:
        p.put((x, 1, z), (x, 1, z), "stone")
        if z + 1 <= 20:
            p.put((x, 0, z + 1), (x, 0, z + 1), "mound")
    # The old yew in the north-east corner: a thick trunk and a dark crown.
    p.put((22, 1, 2), (22, 6, 2), "trunk")
    for y, r in ((3, 2), (4, 2), (5, 2), (6, 1), (7, 1), (8, 0)):
        for x in range(22 - r, 22 + r + 1):
            for z in range(2 - r, 2 + r + 1):
                if not (1 <= x <= 24 and 1 <= z <= 20):
                    continue
                if abs(x - 22) + abs(z - 2) > r + 1:
                    continue
                if (x, z) == (22, 2) and y <= 6:
                    continue
                p.put((x, y, z), (x, y, z), "leaves")
    # Lamp posts.
    for x, z in YARD_LAMPS:
        p.put((x, 1, z), (x, 1, z), "post")
        p.put((x, 2, z), (x, 2, z), "lantern")
    # The contract: the doorway into the chapel is the one way out.
    p.claim_box((12, 1, 1), (13, 3, 1), "chapel-door")
    high = []
    for x in range(26):
        for z in range(22):
            for y in range(1, 11):
                below = p.block.get((x, y - 1, z))
                if p.block.get((x, y, z)) is None and below not in (None, SKIP) and y - 1 >= 2:
                    high.append((x, y, z))
    p.claim_cells(high, "out-of-reach")
    p.claim_box((0, 1, 0), (25, 10, 21), "yard")
    palette = {
        "bracket": "minecraft:spruce_planks",
        "coping": "minecraft:stone_brick_slab[type=bottom,waterlogged=false]",
        "flag": [
            {"block": "minecraft:stone_bricks", "weight": 4},
            {"block": "minecraft:cracked_stone_bricks", "weight": 1},
            {"block": "minecraft:polished_andesite", "weight": 2},
        ],
        "gate-roof": "minecraft:dark_oak_slab[type=bottom,waterlogged=false]",
        "gate-head": "minecraft:spruce_slab[type=top,waterlogged=false]",
        "gatepost": "minecraft:spruce_log[axis=y]",
        "grass": "minecraft:grass_block[snowy=false]",
        "lantern": LANTERN,
        "leaves": "minecraft:spruce_leaves[distance=1,persistent=true,waterlogged=false]",
        "mound": "minecraft:coarse_dirt",
        "post": POST,
        "rail": "minecraft:spruce_fence[east=true,north=false,south=false,waterlogged=false,west=true]",
        "stone": [
            {"block": "minecraft:chiseled_stone_bricks", "weight": 2},
            {"block": "minecraft:mossy_stone_bricks", "weight": 2},
            {"block": "minecraft:cracked_stone_bricks", "weight": 1},
            {"block": "minecraft:mossy_cobblestone", "weight": 1},
        ],
        "trunk": "minecraft:spruce_log[axis=y]",
        "wall": WALL_MIX,
    }
    contract = {
        "edges": [
            {"a": "yard", "b": "exterior", "class": "walk", "via": "chapel-door"},
        ],
        "entry": "yard",
        "no_body": {
            "out-of-reach": {
                "reason": "the tops of the churchyard wall, the lychgate roof, the lamp posts and the yew's crown: nothing anybody climbs",
            },
        },
        "spaces": {"yard": {"envelope": "open"}},
    }
    marks = [
        ("spawn", (12, 1, 18), "north"),
        ("node-yard", (13, 1, 11), "north"),
        ("yew", (20, 1, 4), "west"),
    ]
    solid = {"wall", "coping", "gatepost", "stone", "trunk", "flag", "grass", "mound", "gate-roof", "bracket", "gate-head"}
    lamps = [((x, 2, z), 15) for x, z in YARD_LAMPS]
    dark = p.light_report(solid, lamps, 1, (1, 1, 24, 20))
    return program("bell-tune-yard", p, palette, contract, marks,
                   ["east", "north", "south", "up", "west"]), dark


CHAPEL_LAMPS = [(3, 5, 5), (7, 5, 5), (3, 5, 10), (7, 5, 10), (5, 5, 13)]


def chapel():
    """The chapel. Frame 11 x 11 x 16 from (8191, 63, 8184): the walls in the
    ring (x 1, x 9, z 1, z 15), the floor at y 0, the lid at y 6, and a pitched
    roof running north-south up to y 10 over one course of eaves; the south
    front's eave columns (x 0 and x 10 at z 15) are the yard's."""
    p = Piece((11, 11, 16))
    p.skip((0, 1, 15), (0, 10, 15))            # the yard's
    p.skip((10, 1, 15), (10, 10, 15))
    p.skip((0, 0, 15), (10, 0, 15))            # the ring's fixed ground
    p.skip((1, 0, 1), (1, 0, 14))
    p.skip((2, 0, 1), (9, 0, 1))
    p.skip((9, 0, 2), (9, 0, 14))
    p.skip((0, 0, 0), (0, 5, 14))              # the site's fill, under the eaves
    p.skip((1, 0, 0), (10, 5, 0))
    p.skip((10, 0, 1), (10, 5, 14))
    # Floor.
    p.put((2, 0, 2), (8, 0, 14), "floor")
    p.put((4, 0, 3), (6, 0, 14), "aisle")
    # Walls, with stone quoins at the corners.
    for x in (1, 9):
        p.put((x, 1, 1), (x, 5, 15), "wall")
    for z in (1, 15):
        p.put((1, 1, z), (9, 5, z), "wall")
    for x, z in ((1, 1), (9, 1), (1, 15), (9, 15)):
        p.put((x, 1, z), (x, 5, z), "quoin")
    # The doorway, open, under a lintel.
    p.put((4, 1, 15), (5, 3, 15), None)
    p.put((4, 4, 15), (5, 4, 15), "lintel")
    # Windows: three a side, and a tall lancet behind the altar.
    for z in (5, 8, 11):
        p.put((1, 2, z), (1, 3, z), "pane-ns")
        p.put((9, 2, z), (9, 3, z), "pane-ns")
    p.put((5, 2, 1), (5, 4, 1), "pane-ew")
    # The lid.
    p.put((1, 6, 0), (9, 6, 15), "lid")
    # The roof: eaves at y 6 over x 0 and x 10, then a slope up each side to
    # the ridge at y 10, the gable filled with stone.
    for z in range(0, 16):
        for x in range(0, 11):
            if z == 15 and x in (0, 10):
                continue
            step = min(x, 10 - x)
            y_slope = 6 + step
            if y_slope > 10:
                y_slope = 10
            if x == 5:
                p.put((x, 7, z), (x, 9, z), "gable")
                p.put((x, 10, z), (x, 10, z), "ridge")
                continue
            if y_slope > 7:
                p.put((x, 7, z), (x, y_slope - 1, z), "gable")
            p.put((x, y_slope, z), (x, y_slope, z), "slope-w" if x < 5 else "slope-e")
    # Pews either side of the aisle, the altar and its candles.
    for z in (6, 8, 10, 12):
        p.put((2, 1, z), (3, 1, z), "pew")
        p.put((7, 1, z), (8, 1, z), "pew")
    p.put((4, 1, 2), (6, 1, 2), "altar")
    p.put((4, 2, 2), (4, 2, 2), "candles")
    p.put((6, 2, 2), (6, 2, 2), "candles")
    # Hanging lanterns from the lid.
    for x, y, z in CHAPEL_LAMPS:
        p.put((x, y, z), (x, y, z), "hanging")
    # The contract.
    p.claim_box((4, 1, 15), (5, 3, 15), "chapel-door")
    p.claim_box((0, 6, 0), (10, 10, 15), "roof")
    roof_air = [(x, y, z) for x in range(11) for y in range(6, 11) for z in range(16)
                if p.block.get((x, y, z)) is None]
    p.claim_cells(roof_air, "roof")
    p.claim_box((2, 1, 2), (8, 5, 14), "nave")
    palette = {
        "aisle": "minecraft:polished_andesite",
        "altar": "minecraft:chiseled_stone_bricks",
        "candles": "minecraft:white_candle[candles=4,lit=true,waterlogged=false]",
        "floor": [
            {"block": "minecraft:stone_bricks", "weight": 3},
            {"block": "minecraft:cracked_stone_bricks", "weight": 1},
        ],
        "gable": "minecraft:stone_bricks",
        "hanging": HANGING,
        "lid": "minecraft:spruce_planks",
        "lintel": "minecraft:chiseled_stone_bricks",
        "pane-ew": "minecraft:glass_pane[east=true,north=false,south=false,waterlogged=false,west=true]",
        "pane-ns": "minecraft:glass_pane[east=false,north=true,south=true,waterlogged=false,west=false]",
        "pew": "minecraft:spruce_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]",
        "quoin": "minecraft:polished_andesite",
        "ridge": "minecraft:deepslate_tiles",
        "slope-e": "minecraft:deepslate_tile_stairs[facing=west,half=bottom,shape=straight,waterlogged=false]",
        "slope-w": "minecraft:deepslate_tile_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]",
        "wall": WALL_MIX,
    }
    contract = {
        "edges": [
            {"a": "exterior", "b": "nave", "class": "walk", "via": "chapel-door"},
        ],
        "entry": "nave",
        "no_body": {
            "roof": {"reason": "the chapel's roof and eaves: weather on the outside of the building"},
        },
        "no_body_majority_ack": "A one-room chapel under a pitched roof: most of what a body could stand on is the outside of the roof, its slopes and eaves, which nobody reaches.",
        "spaces": {"nave": {"envelope": "enclosed"}},
    }
    marks = [
        ("node-chapel", (5, 1, 8), "north"),
        ("bell", (5, 1, 4), "south"),
        ("threshold", (5, 1, 13), "north"),
    ]
    solid = {"wall", "quoin", "lintel", "lid", "gable", "ridge", "floor", "aisle", "altar", "slope-e", "slope-w"}
    lamps = [(pos, 15) for pos in CHAPEL_LAMPS] + [((4, 2, 2), 12), ((6, 2, 2), 12)]
    dark = p.light_report(solid, lamps, 1, (2, 2, 8, 14))
    return program("bell-tune-chapel", p, palette, contract, marks,
                   ["east", "north", "south", "up", "west"]), dark


def main():
    here = pathlib.Path(__file__).resolve().parent.parent
    out = here / "programs"
    out.mkdir(exist_ok=True)
    for stem, (prog, dark) in (("yard", yard()), ("chapel", chapel())):
        path = out / f"{stem}.json"
        path.write_text(json.dumps(prog, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
        print(f"wrote {path}")
        if "--light" in sys.argv[1:]:
            print(f"  {stem}: {len(dark)} walk cell(s) estimated below block light 7: {dark}")


if __name__ == "__main__":
    main()
