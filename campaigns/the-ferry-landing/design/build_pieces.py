#!/usr/bin/env python3
"""Write the two place programs of The Ferry Landing.

    python3 campaigns/the-ferry-landing/design/build_pieces.py

`delvec detail` expands `programs/<place stem>.json` inside the box the site plan
hands each place, so the landing stage and the quay top are pieces with their
own spatial contracts. This script states each piece as a cell grid in the
piece's own coordinates (x east, y up, z south, the box's minimum corner at 0)
and writes it out as a grammar program: the grid is cut along x into runs of
identical slices, each run along z, and each column along y, so every leaf is
one material over one box, wrapped in the contract region it belongs to.

What stands outside the two boxes (the rail, the piles, the quay body, the wall
line with its gateway and bollards, the shore and the buildings) stays in
`world-edits.json`, which `build_quay.py` writes.

The landing box: x 8200..8215, y 63..71, z 8188..8195 (16 x 9 x 8), walked at y 64.
The quay box:    x 8200..8215, y 67..71, z 8197..8204 (16 x 5 x 8), walked at y 68.
"""
import json
import pathlib

VERSION = "1.9.0"


class Piece:
    def __init__(self, size):
        self.sx, self.sy, self.sz = size
        self.block = {}  # (x, y, z) -> role
        self.claim = {}  # (x, y, z) -> region

    def put(self, lo, hi, role):
        for x in range(lo[0], hi[0] + 1):
            for y in range(lo[1], hi[1] + 1):
                for z in range(lo[2], hi[2] + 1):
                    self.block[(x, y, z)] = role

    def claim_box(self, lo, hi, region, only_air=False):
        for x in range(lo[0], hi[0] + 1):
            for y in range(lo[1], hi[1] + 1):
                for z in range(lo[2], hi[2] + 1):
                    if only_air and (x, y, z) in self.block:
                        continue
                    if (x, y, z) in self.claim:
                        continue
                    self.claim[(x, y, z)] = region

    def cell(self, x, y, z):
        return (self.block.get((x, y, z)), self.claim.get((x, y, z)))

    # ---- the grid as nested splits ----

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
        body = {"op": "void"} if role is None else {"material": {"role": role}, "op": "fill"}
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


def program(name, piece, palette, contract, marks):
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
        "start": "piece",
        "version": VERSION,
    }


STONE = [
    {"block": "minecraft:stone_bricks", "weight": 6},
    {"block": "minecraft:mossy_stone_bricks", "weight": 2},
    {"block": "minecraft:cracked_stone_bricks", "weight": 1},
]


def lamp_post(p, x, z, post, cap_out_of_walk):
    """A post two courses high on the walk, a lantern on its head.

    Where the box stands tall enough for a body on the lantern's cap, the cap is
    claimed out of walk; under the quay box's lid it is ordinary air.
    """
    p.put((x, 1, z), (x, 2, z), post)
    p.put((x, 3, z), (x, 3, z), "lantern")
    if cap_out_of_walk:
        p.claim_box((x, 4, z), (x, 4, z), "lamp-caps")


def landing():
    p = Piece((16, 9, 8))
    p.put((0, 0, 0), (15, 0, 7), "deck")
    # Lantern posts at the rail, and three more at the foot of the wall and the steps.
    for x, z in ((0, 0), (7, 0), (15, 0), (0, 7), (9, 7), (13, 7)):
        lamp_post(p, x, z, "post", True)
    # The steps: a two-wide flight against the wall face, climbing west to a head
    # at x 1..3 that opens south through the gateway onto the quay top.
    p.put((1, 1, 6), (3, 4, 7), "stone")
    p.put((4, 1, 6), (4, 2, 7), "stone")
    p.put((4, 3, 6), (4, 3, 7), "stair")
    p.put((5, 1, 6), (5, 1, 7), "stone")
    p.put((5, 2, 6), (5, 2, 7), "stair")
    p.put((6, 1, 6), (6, 1, 7), "stair")
    # A low balustrade along the foot of the flight.
    p.put((1, 1, 5), (6, 1, 5), "balustrade")
    # The contract regions, most specific first (a cell takes the first claim).
    p.claim_box((1, 5, 7), (2, 7, 7), "steps-top")       # the seam to the quay top
    for box in (((6, 2, 6), (6, 2, 7)), ((5, 3, 6), (5, 3, 7)),
                ((4, 4, 6), (4, 4, 7)), ((4, 5, 7), (4, 5, 7)), ((3, 6, 7), (3, 8, 7))):
        p.claim_box(*box, "flight")
    p.claim_box((4, 5, 7), (15, 8, 7), "edge-fall")      # the air a body drops through from the quay edge
    p.claim_box((1, 5, 6), (3, 8, 6), "stair-head", only_air=True)
    p.claim_box((3, 5, 7), (3, 8, 7), "stair-head", only_air=True)
    p.claim_box((1, 8, 7), (2, 8, 7), "stair-head", only_air=True)
    p.claim_box((0, 5, 6), (0, 8, 7), "stair-head", only_air=True)
    # Every other air cell of the box is the deck's: open to the sky, its sides the box.
    p.claim_box((0, 1, 0), (15, 8, 7), "deck-walk", only_air=True)
    palette = {
        "balustrade": "minecraft:stone_brick_wall[east=low,north=none,south=none,up=true,waterlogged=false,west=low]",
        "deck": [
            {"block": "minecraft:spruce_planks", "weight": 6},
            {"block": "minecraft:dark_oak_planks", "weight": 1},
        ],
        "lantern": "minecraft:lantern[hanging=false,waterlogged=false]",
        "post": "minecraft:spruce_fence[east=false,north=false,south=false,waterlogged=false,west=false]",
        "stair": "minecraft:stone_brick_stairs[facing=west,half=bottom,shape=straight,waterlogged=false]",
        "stone": STONE,
    }
    contract = {
        "edges": [
            {"a": "exterior", "b": "deck-walk", "class": "walk", "via": "edge-fall"},
            {"a": "deck-walk", "b": "stair-head", "class": "stair", "rise": 4, "via": "flight"},
            {"a": "stair-head", "b": "exterior", "class": "walk", "via": "steps-top"},
        ],
        "entry": "deck-walk",
        "no_body": {
            "lamp-caps": {"reason": "the cap of a lantern on its post: a lamp, not somewhere anybody stands"},
        },
        "spaces": {
            "deck-walk": {"envelope": "open_top"},
            "stair-head": {"envelope": "open_top"},
        },
    }
    marks = [("node-landing", (7, 1, 3), "north"), ("spawn", (7, 1, 3), "north")]
    return program("ferry-landing-stage", p, palette, contract, marks)


def quay():
    p = Piece((16, 5, 8))
    p.put((0, 0, 0), (15, 0, 7), "paving")
    # Lantern posts a step back from the open edge, and lamp standards at the back.
    for x, z in ((0, 2), (7, 2), (13, 2)):
        lamp_post(p, x, z, "standard", False)
    for x, z in ((2, 7), (9, 7), (15, 7)):
        lamp_post(p, x, z, "standard", False)
    # A bench facing the water, and barrels where the carts unload.
    p.put((5, 1, 5), (7, 1, 5), "bench")
    p.put((12, 1, 4), (13, 1, 5), "barrel")
    p.claim_box((1, 1, 0), (2, 3, 0), "gate-way")        # the seam from the head of the steps
    p.claim_box((4, 1, 0), (15, 4, 0), "edge-drop")      # the open edge over the landing
    p.claim_box((0, 1, 0), (15, 4, 7), "top", only_air=True)
    palette = {
        "barrel": "minecraft:barrel[facing=up,open=false]",
        "bench": "minecraft:spruce_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]",
        "lantern": "minecraft:lantern[hanging=false,waterlogged=false]",
        "paving": [
            {"block": "minecraft:stone_bricks", "weight": 3},
            {"block": "minecraft:polished_andesite", "weight": 2},
            {"block": "minecraft:andesite", "weight": 1},
        ],
        "standard": "minecraft:polished_blackstone_wall[east=none,north=none,south=none,up=true,waterlogged=false,west=none]",
    }
    contract = {
        "edges": [
            {"a": "exterior", "b": "top", "class": "walk", "via": "gate-way"},
            {"a": "top", "b": "exterior", "class": "drop", "rise": 0, "via": "edge-drop"},
        ],
        "entry": "top",
        "no_body": {},
        "spaces": {"top": {"envelope": "open_top"}},
    }
    marks = [("node-quay", (7, 1, 3), "north")]
    return program("ferry-quay-top", p, palette, contract, marks)


def main():
    here = pathlib.Path(__file__).resolve().parent.parent
    out = here / "programs"
    out.mkdir(exist_ok=True)
    for stem, prog in (("landing", landing()), ("quay", quay())):
        path = out / f"{stem}.json"
        path.write_text(json.dumps(prog, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
