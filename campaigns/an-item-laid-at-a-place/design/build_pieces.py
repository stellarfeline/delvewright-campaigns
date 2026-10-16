#!/usr/bin/env python3
"""Write the two place programs of An Item Laid at a Place.

    python3 campaigns/an-item-laid-at-a-place/design/build_pieces.py [--light]

`delvec detail` expands `programs/<place stem>.json` inside the frame the site
plan hands each place (`delvec allocation <campaign> <place>` prints it). Each
piece is stated here as a cell grid in the frame's own coordinates (x east,
y up, z south, the frame's minimum corner at 0) and written out as a grammar
program: the grid is cut along x into runs of identical slices, each slice
along z, each column along y, so every leaf is one material over one box,
wrapped in the contract region it belongs to.

A cell is a palette role (a block), `None` (air the piece owns) or `SKIP` (a
cell the piece does not own: a neighbour's, the ring's fixed ground), which the
verb writes as `structure_void`.

`--light` prints, per piece, a rough block-light estimate of every walk cell
(light spread by steps through non-solid cells, sky light ignored), so the
lamps can be placed while the room is designed. The engine's own proof is the
judge; this only says where to look.
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
    {"block": "minecraft:mossy_stone_bricks", "weight": 1},
    {"block": "minecraft:cracked_stone_bricks", "weight": 1},
]
HANGING = "minecraft:lantern[hanging=true,waterlogged=false]"
STANDING = "minecraft:lantern[hanging=false,waterlogged=false]"
CHAIN = "minecraft:iron_chain[axis=y,waterlogged=false]"
PANE_NS = "minecraft:glass_pane[east=false,north=true,south=true,waterlogged=false,west=false]"
PANE_EW = "minecraft:glass_pane[east=true,north=false,south=false,waterlogged=false,west=true]"

# Hanging lanterns in the nave: (x, y, z) of the lantern; a chain runs from it
# up to the lid at y 10.
NAVE_LAMPS = [(2, 6, 3), (6, 6, 3), (2, 6, 8), (6, 6, 8), (6, 6, 11), (3, 6, 12)]
STAIR_X = (1, 2)
# The treads of the loft stair: (z, y) of each stair block, rising south.
TREADS = [(9, 1), (10, 2), (11, 3), (12, 4)]


def nave():
    """The nave. Frame 9 x 11 x 15 from (8187, 63, 8181): the walls in the ring
    (x 0, x 8, z 0, z 14), the floor course at y 0, the walk at y 1, the lid at
    y 10. The south wall (z 14) is the nave's except its y 5 course, the loft's
    floor; the stair opening into the loft is x 1-2, y 6-8 there."""
    p = Piece((9, 11, 15))
    # What the nave does not own.
    p.skip((0, 5, 14), (8, 5, 14))             # the loft's floor course
    p.skip((0, 0, 0), (0, 0, 14))              # the ring's fixed ground
    p.skip((8, 0, 0), (8, 0, 14))
    p.skip((1, 0, 0), (7, 0, 0))
    p.skip((1, 0, 14), (7, 0, 14))
    # Floor: flagstones, a polished aisle up the middle, a step before the altar.
    p.put((1, 0, 1), (7, 0, 13), "floor")
    p.put((4, 0, 4), (4, 0, 13), "aisle")
    # Walls, with quoins at the corners, and the lid.
    for x in (0, 8):
        p.put((x, 1, 0), (x, 9, 14), "wall")
    p.put((1, 1, 0), (7, 9, 0), "wall")
    p.put((1, 1, 14), (7, 4, 14), "wall")
    p.put((0, 6, 14), (8, 9, 14), "wall")
    for x, z in ((0, 0), (8, 0), (0, 14), (8, 14)):
        p.put((x, 1, z), (x, 4, z), "quoin")
        p.put((x, 6, z), (x, 9, z), "quoin")
    p.put((0, 10, 0), (8, 10, 14), "lid")
    # Windows: tall lights in both side walls, and a lancet over the altar.
    for z in (3, 7, 11):
        p.put((0, 3, z), (0, 6, z), "pane-ns")
        p.put((8, 3, z), (8, 6, z), "pane-ns")
    p.put((4, 3, 0), (4, 7, 0), "pane-ew")
    # The loft front: the stair opening, and a glazed screen along the rest
    # of it, so the loft looks down the nave through the glass.
    p.put((1, 6, 14), (2, 8, 14), None)
    p.put((4, 7, 14), (7, 8, 14), "pane-ew")
    p.put((8, 6, 14), (8, 9, 14), "quoin")
    # The altar at the north end, candles on it.
    p.put((3, 1, 1), (5, 1, 1), "altar")
    p.put((3, 2, 1), (3, 2, 1), "candles")
    p.put((5, 2, 1), (5, 2, 1), "candles")
    # The vestry chest beside the altar step, and the barrel at the foot of
    # the loft stair.
    p.put((7, 1, 2), (7, 1, 2), "chest")
    p.put((1, 1, 8), (1, 1, 8), "barrel")
    # Pews either side of the aisle; the west side stops short of the stair.
    for z in (5, 7):
        p.put((1, 1, z), (3, 1, z), "pew")
    for z in (5, 7, 9, 11):
        p.put((5, 1, z), (7, 1, z), "pew")
    # The loft stair up the west wall: treads rising south, solid under them,
    # and a landing at the top before the opening.
    for z, y in TREADS:
        p.put((STAIR_X[0], y, z), (STAIR_X[1], y, z), "tread")
        if y > 1:
            p.put((STAIR_X[0], 1, z), (STAIR_X[1], y - 1, z), "stair-body")
    p.put((STAIR_X[0], 1, 13), (STAIR_X[1], 4, 13), "stair-body")
    p.put((STAIR_X[0], 5, 13), (STAIR_X[1], 5, 13), "landing")
    # Hanging lanterns on chains from the lid.
    for x, y, z in NAVE_LAMPS:
        p.put((x, y, z), (x, y, z), "hanging")
        p.put((x, y + 1, z), (x, 9, z), "chain")
    # The contract.
    p.claim_box((1, 6, 14), (2, 8, 14), "loft-stair")
    flight = []
    for z, y in TREADS:
        flight += [(x, yy, z) for x in STAIR_X for yy in range(y, 10)]
    p.claim_cells(flight, "loft-flight")
    p.claim_box((1, 6, 13), (2, 9, 13), "landing")
    p.claim_box((1, 1, 1), (7, 9, 13), "room")
    palette = {
        "aisle": "minecraft:polished_andesite",
        "altar": "minecraft:chiseled_stone_bricks",
        "barrel": "minecraft:barrel[facing=up,open=false]",
        "candles": "minecraft:white_candle[candles=3,lit=true,waterlogged=false]",
        "chain": CHAIN,
        "chest": "minecraft:chest[facing=west,type=single,waterlogged=false]",
        "floor": [
            {"block": "minecraft:stone_bricks", "weight": 3},
            {"block": "minecraft:cracked_stone_bricks", "weight": 1},
        ],
        "hanging": HANGING,
        "landing": "minecraft:spruce_planks",
        "lid": "minecraft:dark_oak_planks",
        "pane-ew": PANE_EW,
        "pane-ns": PANE_NS,
        "pew": "minecraft:spruce_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]",
        "quoin": "minecraft:polished_andesite",
        "stair-body": "minecraft:spruce_planks",
        "tread": "minecraft:spruce_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]",
        "wall": WALL_MIX,
    }
    contract = {
        "edges": [
            {"a": "room", "b": "landing", "class": "stair", "rise": 5, "via": "loft-flight"},
            {"a": "landing", "b": "exterior", "class": "walk", "via": "loft-stair"},
        ],
        "entry": "landing",
        "spaces": {"landing": {"envelope": "enclosed"}, "room": {"envelope": "enclosed"}},
    }
    marks = [
        ("spawn", (4, 1, 12), "north"),
        ("node-nave", (4, 1, 8), "north"),
        ("roll-chest", (7, 1, 2), "west"),
        ("lantern-barrel", (1, 1, 8), "east"),
    ]
    solid = {"wall", "quoin", "lid", "floor", "aisle", "altar", "stair-body", "landing", "chest", "barrel"}
    lamps = [(pos, 15) for pos in NAVE_LAMPS] + [((3, 2, 1), 9), ((5, 2, 1), 9)]
    dark = p.light_report(solid, lamps, 1, (1, 1, 7, 13))
    return program("item-laid-nave", p, palette, contract, marks,
                   ["east", "north", "up", "west"]), dark


LOFT_LAMPS = [(1, 6, 4), (7, 6, 4)]


def loft():
    """The loft. Frame 9 x 12 x 6 from (8187, 63, 8195): its front (z 0) is the
    nave's south wall except the y 5 course, which is the loft's floor, and the
    y 11 course over the nave's lid; the other walls are x 0, x 8 and z 5; the
    floor course at y 5 over a solid undercroft, the walk at y 6, the lid at
    y 11."""
    p = Piece((9, 12, 6))
    p.skip((0, 1, 0), (8, 4, 0))               # the nave's
    p.skip((0, 6, 0), (8, 10, 0))
    p.skip((0, 0, 0), (0, 0, 5))               # the ring's fixed ground
    p.skip((8, 0, 0), (8, 0, 5))
    p.skip((1, 0, 0), (7, 0, 0))
    p.skip((1, 0, 5), (7, 0, 5))
    # The undercroft: solid under the loft floor.
    p.put((1, 0, 1), (7, 4, 4), "under")
    # Walls and lid.
    for x in (0, 8):
        p.put((x, 1, 1), (x, 10, 5), "wall")
    p.put((1, 1, 5), (7, 10, 5), "wall")
    for x in (0, 8):
        p.put((x, 1, 5), (x, 10, 5), "quoin")
    p.put((0, 11, 0), (8, 11, 5), "lid")
    # The floor, its front edge under the rail.
    p.put((0, 5, 0), (8, 5, 0), "beam")
    p.put((1, 5, 1), (7, 5, 4), "boards")
    # A window in the back wall onto the dusk.
    p.put((3, 7, 5), (5, 8, 5), "pane-ew")
    # Two lanterns standing in the back corners, and the chain the watch
    # lantern hangs from: three links from the lid; its hook, the bottom link,
    # is the objective's prop and is placed by the compiler.
    for x, y, z in LOFT_LAMPS:
        p.put((x, y, z), (x, y, z), "standing")
    p.put((3, 8, 1), (3, 10, 1), "chain")
    # The contract.
    p.claim_box((1, 6, 1), (2, 8, 1), "loft-stair")
    p.claim_box((1, 6, 1), (7, 10, 4), "loft")
    palette = {
        "beam": "minecraft:dark_oak_planks",
        "boards": "minecraft:spruce_planks",
        "chain": CHAIN,
        "lid": "minecraft:dark_oak_planks",
        "pane-ew": PANE_EW,
        "quoin": "minecraft:polished_andesite",
        "standing": STANDING,
        "under": "minecraft:stone_bricks",
        "wall": WALL_MIX,
    }
    contract = {
        "edges": [
            {"a": "exterior", "b": "loft", "class": "walk", "via": "loft-stair"},
        ],
        "entry": "loft",
        "spaces": {"loft": {"envelope": "enclosed"}},
    }
    marks = [
        ("node-loft", (4, 6, 3), "north"),
        ("lectern", (4, 6, 1), "south"),
        ("hook", (3, 7, 1), "south"),
    ]
    solid = {"wall", "quoin", "lid", "beam", "boards", "under"}
    lamps = [(pos, 15) for pos in LOFT_LAMPS]
    dark = p.light_report(solid, lamps, 6, (1, 1, 7, 4))
    return program("item-laid-loft", p, palette, contract, marks,
                   ["east", "south", "up", "west"]), dark


def main():
    here = pathlib.Path(__file__).resolve().parent.parent
    out = here / "programs"
    out.mkdir(exist_ok=True)
    for stem, (prog, dark) in (("nave", nave()), ("loft", loft())):
        path = out / f"{stem}.json"
        path.write_text(json.dumps(prog, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
        print(f"wrote {path}")
        if "--light" in sys.argv[1:]:
            print(f"  {stem}: {len(dark)} walk cell(s) estimated below block light 7: {dark}")


if __name__ == "__main__":
    main()
