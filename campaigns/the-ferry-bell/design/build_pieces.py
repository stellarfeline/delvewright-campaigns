#!/usr/bin/env python3
"""Write the four place programs of The Ferry Bell.

    python3 campaigns/the-ferry-bell/design/build_pieces.py [--lever-on-rail]

`delvec detail` expands `programs/<place stem>.json` inside the frame the site
plan hands each place (`delvec allocation <campaign> <place>` prints it). This
script states each piece as a cell grid in the frame's own coordinates (x east,
y up, z south, the frame's minimum corner at 0) and writes it out as a grammar
program: the grid is cut along x into runs of identical slices, each run along
z, and each column along y, so every leaf is one material over one box,
wrapped in the contract region it belongs to.

Three cell states: a palette role (a block), `None` (air the piece owns), and
`SKIP` (a cell the piece does not own — a neighbour's, the ring's fixed ground,
the site's fill — which the verb writes as `structure_void`).

`--lever-on-rail` writes the jetty with the bolt lever's mark on the west rail,
among the rail's fence posts, instead of on the deck beside the door: the
first build of the level, which is refused.
"""
import json
import pathlib
import sys

VERSION = "1.9.0"
SKIP = "__skip__"


class Piece:
    def __init__(self, size):
        self.sx, self.sy, self.sz = size
        self.block = {}  # (x, y, z) -> role or SKIP
        self.claim = {}  # (x, y, z) -> region

    def put(self, lo, hi, role):
        for x in range(lo[0], hi[0] + 1):
            for y in range(lo[1], hi[1] + 1):
                for z in range(lo[2], hi[2] + 1):
                    self.block[(x, y, z)] = role

    def skip(self, lo, hi):
        self.put(lo, hi, SKIP)

    def claim_box(self, lo, hi, region, only_air=False):
        for x in range(lo[0], hi[0] + 1):
            for y in range(lo[1], hi[1] + 1):
                for z in range(lo[2], hi[2] + 1):
                    b = self.block.get((x, y, z))
                    if b == SKIP:
                        continue
                    if only_air and b is not None:
                        continue
                    if (x, y, z) in self.claim:
                        continue
                    self.claim[(x, y, z)] = region

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


def program(name, piece, palette, contract, marks, shown_faces=None):
    body = piece.body()
    for stem, pos, facing in marks:
        body = {"body": body, "mark": {
            "anchor": stem, "at": "offset", "facing": facing,
            "x": {"expr": "int", "value": pos[0]},
            "y": {"expr": "int", "value": pos[1]},
            "z": {"expr": "int", "value": pos[2]},
        }, "op": "mark"}
    out = {
        "contract": contract,
        "name": name,
        "palette": palette,
        "params": {},
        "rules": {"piece": [{"body": body, "weight": 1}]},
        "start": "piece",
        "version": VERSION,
    }
    if shown_faces:
        out["shown_faces"] = shown_faces
    return out


PLANKS = [
    {"block": "minecraft:spruce_planks", "weight": 5},
    {"block": "minecraft:oak_planks", "weight": 1},
]
FENCE = "minecraft:spruce_fence[east=false,north=true,south=true,waterlogged=false,west=false]"
POST = "minecraft:spruce_fence[east=false,north=false,south=false,waterlogged=false,west=false]"
LANTERN = "minecraft:lantern[hanging=false,waterlogged=false]"
HANGING = "minecraft:lantern[hanging=true,waterlogged=false]"


def shore():
    """The beach at the jetty foot. Frame 42 x 9 x 12 from (8195, 61, 8208);
    the walk is local y 3 (world 64) over sand at y 2."""
    p = Piece((42, 9, 12))
    # What the shore does not own (the allocation's voids).
    p.skip((0, 0, 1), (41, 1, 11))           # the site's fill under the plot
    p.skip((29, 0, 0), (41, 1, 0))
    p.skip((0, 2, 1), (0, 2, 11))            # the ring's fixed ground
    p.skip((1, 2, 11), (41, 2, 11))
    p.skip((29, 2, 0), (41, 2, 0))
    p.skip((41, 2, 1), (41, 2, 10))
    # The handed ground: sand over the plot.
    p.put((1, 2, 1), (40, 2, 10), "sand")
    # The north ring over the shallows: a sand step one course down, flush
    # with the sea, so a swimmer wades out onto the beach; the jetty's first
    # planks run over it at the jetty foot.
    p.put((0, 0, 0), (28, 0, 0), "bank")
    p.put((0, 1, 0), (28, 1, 0), "sand")
    p.put((14, 0, 0), (16, 1, 0), "pile")
    p.put((14, 2, 0), (16, 2, 0), "deck")
    # Two lamp posts either side of the jetty mouth.
    for x in (12, 18):
        p.put((x, 3, 2), (x, 4, 2), "post")
        p.put((x, 5, 2), (x, 5, 2), "lantern")
    # An upturned rowing boat on the sand to the west, and a stack of crates
    # and a barrel to the east of the notice.
    p.put((4, 3, 5), (8, 3, 7), "hull")
    p.put((3, 3, 6), (3, 3, 6), "hull")
    p.put((9, 3, 6), (9, 3, 6), "hull")
    p.put((22, 3, 2), (23, 3, 2), "crate")
    p.put((24, 3, 3), (24, 3, 3), "barrel")
    # The contract: the jetty foot and the spit's neck are the two ways out.
    p.claim_box((14, 3, 0), (16, 6, 0), "jetty-foot")
    p.claim_box((31, 3, 0), (40, 6, 0), "spit-neck")
    p.claim_box((12, 6, 2), (12, 6, 2), "lamp-caps")
    p.claim_box((18, 6, 2), (18, 6, 2), "lamp-caps")
    p.claim_box((0, 2, 0), (28, 2, 0), "strand", only_air=True)
    p.claim_box((0, 3, 0), (41, 8, 11), "beach")
    palette = {
        "bank": "minecraft:sandstone",
        "barrel": "minecraft:barrel[facing=up,open=false]",
        "crate": "minecraft:spruce_planks",
        "deck": "minecraft:spruce_planks",
        "hull": "minecraft:dark_oak_slab[type=bottom,waterlogged=false]",
        "lantern": LANTERN,
        "pile": "minecraft:spruce_log[axis=y]",
        "post": POST,
        "sand": "minecraft:sand",
    }
    contract = {
        "edges": [
            {"a": "exterior", "b": "beach", "class": "walk", "via": "jetty-foot"},
            {"a": "beach", "b": "exterior", "class": "walk", "via": "spit-neck"},
            {"a": "beach", "b": "strand", "class": "walk", "rise": -1},
        ],
        "entry": "beach",
        "no_body": {"lamp-caps": {"reason": "the cap of a lantern on its post: a lamp, not somewhere anybody stands"}},
        "spaces": {"beach": {"envelope": "open"}, "strand": {"envelope": "open"}},
    }
    marks = [
        ("spawn", (19, 3, 7), "north"),
        ("node-shore", (20, 3, 6), "north"),
        ("nell", (13, 3, 1), "south"),
        ("notice", (17, 3, 1), "south"),
    ]
    return program("ferry-bell-shore", p, palette, contract, marks, ["east", "north", "west"])


def jetty(lever_on_rail):
    """The jetty. Frame 5 x 5 x 16 from (8208, 63, 8192); the deck is local
    y 0, the rails stand in the ring at x 0 and x 4."""
    p = Piece((5, 5, 16))
    p.put((0, 0, 0), (4, 0, 15), "deck")
    p.put((0, 1, 0), (0, 1, 15), "rail")
    p.put((4, 1, 0), (4, 1, 15), "rail")
    # A lantern on the rail at each end.
    lamps = ((0, 15), (4, 15), (0, 1), (4, 1))
    for x, z in lamps:
        p.put((x, 2, z), (x, 2, z), "lantern")
    p.claim_box((1, 1, 15), (3, 4, 15), "foot")
    for x, z in lamps:
        p.claim_box((x, 3, z), (x, 3, z), "lamp-caps")

    p.claim_box((2, 1, 0), (2, 2, 0), "door")
    p.claim_box((0, 1, 0), (4, 4, 15), "deck-walk")
    palette = {
        "deck": PLANKS,
        "lantern": LANTERN,
        "rail": FENCE,
    }
    contract = {
        "edges": [
            {"a": "exterior", "b": "deck-walk", "class": "walk", "via": "foot"},
            {"a": "deck-walk", "b": "exterior", "class": "walk", "via": "door"},
        ],
        "entry": "deck-walk",
        "no_body": {
            "lamp-caps": {"reason": "the cap of a lantern on the rail: a lamp, not somewhere anybody stands"},
        },
        "spaces": {"deck-walk": {"envelope": "open"}},
    }
    lever = (0, 1, 6) if lever_on_rail else (1, 1, 0)
    marks = [
        ("node-jetty", (2, 1, 8), "north"),
        ("bolt-lever", lever, "north"),
    ]
    return program("ferry-bell-jetty", p, palette, contract, marks, ["east", "west"])


def ferry_house():
    """The ferry house. Frame 11 x 9 x 10 from (8205, 63, 8183): the walls in
    the ring (x 1, x 9, z 1, z 8), the floor at y 0, the lid at y 5, and a
    gabled roof running north-south up to y 8 over one course of eaves."""
    p = Piece((11, 9, 10))
    # Voids below the roof zone: the eaves' columns belong to nobody, and the
    # jetty owns its first row under the south eave.
    p.skip((0, 0, 0), (0, 4, 9))
    p.skip((10, 0, 0), (10, 4, 9))
    p.skip((1, 0, 0), (9, 4, 0))
    p.skip((1, 0, 9), (9, 4, 9))
    # Floor, walls, lid.
    p.put((1, 0, 1), (9, 0, 8), "floor")
    for x in (1, 9):
        p.put((x, 1, 1), (x, 4, 8), "wall")
    for z in (1, 8):
        p.put((1, 1, z), (9, 4, z), "wall")
    for x, z in ((1, 1), (9, 1), (1, 8), (9, 8)):
        p.put((x, 1, z), (x, 4, z), "corner")
    p.put((1, 5, 1), (9, 5, 8), "lid")
    # The door: its bar fills the opening the seam allocated.
    p.put((5, 1, 8), (5, 2, 8), "door-bar")
    # Windows: the east one an open shutter-hole high in the wall, over the
    # cove to the spit (a body cannot climb to it; the bell is rung beside
    # it); the west one glazed, over the open water.
    p.put((9, 3, 3), (9, 4, 5), None)
    p.put((1, 2, 3), (1, 3, 5), "pane-ns")
    # The beam the bell hangs from, and two lanterns hung from the lid.
    p.put((2, 3, 4), (8, 3, 4), "beam")
    p.put((3, 4, 6), (3, 4, 6), "hanging")
    p.put((7, 4, 6), (7, 4, 6), "hanging")
    # A bench along the west wall, and a coil of rope by the door.
    p.put((2, 1, 2), (2, 1, 3), "bench")
    p.put((7, 1, 7), (7, 1, 7), "rope")
    # The roof: eaves at y 5, then a gable stepping in from east and west.
    for z in range(0, 10):
        for x in (0, 10):
            p.put((x, 5, z), (x, 5, z), "eave")
        if z in (0, 9):
            p.put((1, 5, z), (9, 5, z), "eave")
        p.put((1, 6, z), (1, 6, z), "slope")
        p.put((9, 6, z), (9, 6, z), "slope")
        p.put((2, 6, z), (8, 6, z), "roof")
        p.put((2, 7, z), (2, 7, z), "slope")
        p.put((8, 7, z), (8, 7, z), "slope")
        p.put((3, 7, z), (7, 7, z), "roof")
        p.put((3, 8, z), (3, 8, z), "slope")
        p.put((7, 8, z), (7, 8, z), "slope")
        p.put((4, 8, z), (6, 8, z), "roof")
    # The contract.
    p.claim_box((5, 1, 8), (5, 2, 8), "seam-ferry-door")
    p.claim_box((2, 1, 2), (8, 4, 7), "hall", only_air=False)
    p.claim_box((9, 3, 3), (9, 4, 5), "window-sill", only_air=True)
    p.claim_box((0, 5, 0), (10, 8, 9), "roof-top", only_air=True)
    palette = {
        "beam": "minecraft:stripped_spruce_log[axis=x]",
        "bench": "minecraft:spruce_stairs[facing=west,half=bottom,shape=straight,waterlogged=false]",
        "corner": "minecraft:spruce_log[axis=y]",
        "door-bar": "minecraft:dark_oak_planks",
        "eave": "minecraft:dark_oak_slab[type=bottom,waterlogged=false]",
        "floor": "minecraft:spruce_planks",
        "hanging": HANGING,
        "lid": "minecraft:spruce_planks",
        "pane-ns": "minecraft:glass_pane[east=false,north=true,south=true,waterlogged=false,west=false]",
        "roof": "minecraft:dark_oak_planks",
        "rope": "minecraft:barrel[facing=up,open=false]",
        "slope": "minecraft:dark_oak_slab[type=bottom,waterlogged=false]",
        "wall": "minecraft:stripped_spruce_wood[axis=y]",
    }
    contract = {
        "edges": [
            {"a": "exterior", "b": "hall", "bar": {"block": "door-bar", "region": "seam-ferry-door"},
             "class": "barred"},
        ],
        "entry": "hall",
        "no_body_majority_ack": "A one-room house under a gabled roof: most of what a body could stand on is the outside of the roof, its slopes and eaves, which nobody reaches.",
        "no_body": {
            "roof-top": {"reason": "the ferry house's roof and eaves: weather on the outside of the building"},
            "window-sill": {"reason": "the sill of the east shutter-hole, two courses above the floor: a window, not a way"},
        },
        "spaces": {"hall": {"envelope": "open"}},
    }
    marks = [
        ("node-ferry-house", (5, 1, 5), "south"),
        ("bell", (7, 2, 4), "east"),
    ]
    return program("ferry-bell-ferry-house", p, palette, contract, marks,
                   ["east", "north", "south", "up", "west"])


def far_bank():
    """The spit. Frame 12 x 5 x 23 from (8225, 63, 8185); sand at y 0, the
    walk at y 1; the ring's sand is the whole's fixed ground."""
    p = Piece((12, 5, 23))
    p.skip((0, 0, 0), (0, 0, 22))
    p.skip((1, 0, 0), (11, 0, 0))
    p.skip((11, 0, 1), (11, 0, 22))
    p.put((1, 0, 1), (10, 0, 22), "sand")
    # A post-and-rail fence round the spit's west, north and east edges, where
    # the net-menders dry their nets: it keeps a body on the spit off the
    # region's edge, and leaves the neck to the shore open.
    p.put((0, 1, 0), (0, 1, 22), "fence-ns")
    p.put((11, 1, 0), (11, 1, 22), "fence-ns")
    p.put((1, 1, 0), (10, 1, 0), "fence-ew")
    for x, z in ((0, 0), (11, 0)):
        p.put((x, 1, z), (x, 1, z), "fence-corner")
    # Driftwood and dry bushes on the spit.
    p.put((6, 1, 6), (9, 1, 6), "driftwood")
    p.put((4, 1, 15), (4, 1, 17), "driftwood-z")
    for x, z in ((8, 10), (3, 9), (9, 18), (6, 20)):
        p.put((x, 1, z), (x, 1, z), "bush")
    p.claim_box((1, 1, 22), (10, 4, 22), "neck")
    p.claim_box((0, 1, 0), (11, 4, 22), "spit")
    palette = {
        "bush": "minecraft:dead_bush",
        "driftwood": "minecraft:stripped_oak_log[axis=x]",
        "driftwood-z": "minecraft:stripped_oak_log[axis=z]",
        "fence-corner": "minecraft:oak_fence[east=false,north=false,south=false,waterlogged=false,west=false]",
        "fence-ew": "minecraft:oak_fence[east=true,north=false,south=false,waterlogged=false,west=true]",
        "fence-ns": "minecraft:oak_fence[east=false,north=true,south=true,waterlogged=false,west=false]",
        "sand": "minecraft:sand",
    }
    contract = {
        "edges": [{"a": "exterior", "b": "spit", "class": "walk", "via": "neck"}],
        "entry": "spit",
        "no_body": {},
        "spaces": {"spit": {"envelope": "open"}},
    }
    marks = [
        ("node-far-bank", (5, 1, 11), "west"),
        ("muster", (2, 1, 3), "west"),
    ]
    return program("ferry-bell-far-bank", p, palette, contract, marks, ["east", "north", "west"])


def main():
    lever_on_rail = "--lever-on-rail" in sys.argv[1:]
    here = pathlib.Path(__file__).resolve().parent.parent
    out = here / "programs"
    out.mkdir(exist_ok=True)
    for stem, prog in (("shore", shore()), ("jetty", jetty(lever_on_rail)),
                       ("ferry-house", ferry_house()), ("far-bank", far_bank())):
        path = out / f"{stem}.json"
        path.write_text(json.dumps(prog, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
