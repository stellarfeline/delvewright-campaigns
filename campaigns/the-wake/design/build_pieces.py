#!/usr/bin/env python3
"""Write the two place programs of The Wake.

    python3 campaigns/the-wake/design/build_pieces.py [--light] [--map]

`delvec detail` expands `programs/<place stem>.json` inside the frame the site
plan hands each place (`delvec allocation campaigns/the-wake <place>` prints
it): the field 17 x 11 x 19 from (8191, 63, 8191), the shore 17 x 11 x 10 from
(8191, 63, 8210); in both the floor course is y 0 and the walk y 1. The field
meets the shore along its whole south side, the open ground of the seam, which
both pieces leave open. The piece is stated as a cell grid in the
frame's own coordinates (x east, y up, z south) and written out as a grammar
program: the grid is cut along x into runs of identical slices, each slice
along z, each column along y, so every leaf is one material over one box,
wrapped in the contract region it belongs to.

A cell is a palette role (a block), `None` (air the piece owns) or `SKIP` (a
cell the piece does not own: the ring's fixed ground), which the verb writes
as `structure_void`.

`--light` prints a rough block-light estimate of every walk cell (sky light
ignored), so the lamps are placed while the field is designed; the engine's
own proof is the judge. `--map` prints the walk course from above.
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


FENCE = "minecraft:spruce_fence[east=false,north=false,south=false,waterlogged=false,west=false]"
LANTERN = "minecraft:lantern[hanging=false,waterlogged=false]"
STONE = "minecraft:andesite_wall[east=none,north=none,south=none,up=true,waterlogged=false,west=none]"
TIDE_STONE = "minecraft:mossy_cobblestone_wall[east=low,north=none,south=none,up=false,waterlogged=false,west=low]"
DYKE = [
    {"block": "minecraft:cobblestone", "weight": 3},
    {"block": "minecraft:mossy_cobblestone", "weight": 2},
]

# The field. Lantern posts: (x, z) of a fence post whose top carries a lantern.
FIELD_POSTS = [(6, 2), (10, 2), (4, 7), (12, 7), (6, 12), (11, 13), (3, 15), (14, 16)]
# Headstones (x, z) with the mound running south of each, two cells long.
GRAVES = [(4, 9), (5, 9), (2, 13), (4, 13), (12, 9), (13, 9), (11, 15), (13, 15)]
CUT = [(2, 10), (2, 11)]          # the open cut, one course deep
CUT_STONE = (2, 9)                # its headstone, not yet cut with a name
FIELD_MARKS = [
    ("node-field", (8, 1, 14), "north"),
    ("keep-gate", (8, 1, 2), "south"),
    ("bier", (8, 1, 10), "north"),
    ("bier-side", (10, 1, 10), "west"),
    ("widow", (8, 1, 12), "north"),
    ("west-flank", (3, 1, 16), "east"),
    ("east-flank", (14, 1, 11), "west"),
    ("second-barrow", (11, 1, 11), "west"),
    ("warden-post", (3, 1, 10), "east"),
    ("row-head", (6, 1, 8), "south"),
]

# The shore.
SHORE_POSTS = [(10, 3), (5, 6), (12, 7)]
FIRE = (6, 2)
DRIFT = [(10, 5), (11, 5), (12, 5)]
SHORE_MARKS = [
    ("spawn", (8, 1, 6), "north"),
    ("node-shore", (8, 1, 4), "north"),
    ("shore-fire", (7, 1, 2), "east"),
    ("tide-line", (8, 1, 8), "south"),
]


def posts(p, where):
    for x, z in where:
        p.put((x, 1, z), (x, 1, z), "post")
        p.put((x, 2, z), (x, 2, z), "lantern")
        p.claim_box((x, 3, z), (x, 3, z), "tops")


def field():
    """The barrow field. Frame 17 x 11 x 19: the keep wall in the ring at z 0,
    the dykes at x 0 and x 16, the play space x 1-15, z 1-18; its south row
    (z 18) is the seam onto the shore and stays open."""
    p = Piece((17, 11, 19))
    p.skip((0, 0, 0), (0, 0, 18))
    p.skip((16, 0, 0), (16, 0, 18))
    p.skip((1, 0, 0), (15, 0, 0))
    # Floor: turf, and the gravel grave road from the gate to the beach.
    p.put((1, 0, 1), (15, 0, 18), "turf")
    p.put((8, 0, 3), (8, 0, 18), "road")
    p.put((7, 0, 1), (9, 0, 2), "road")
    # The foot of the keep: a curtain wall the whole width, eight courses,
    # merlons over it, and a timber gate shut in a dressed arch.
    p.put((0, 1, 0), (16, 8, 0), "keep")
    for x in range(0, 17, 2):
        p.put((x, 9, 0), (x, 9, 0), "keep")
    p.put((6, 1, 0), (10, 5, 0), "arch")
    p.put((7, 1, 0), (9, 4, 0), "gate")
    p.put((7, 4, 0), (7, 4, 0), "arch")
    p.put((9, 4, 0), (9, 4, 0), "arch")
    # The dykes: dry stone two courses high down both sides.
    for x in (0, 16):
        p.put((x, 1, 1), (x, 2, 18), "dyke")
    # Graves: a headstone and a mound south of it.
    for x, z in GRAVES:
        p.put((x, 1, z), (x, 1, z), "headstone")
        p.put((x, 0, z + 1), (x, 0, z + 2), "mound")
    # The open cut at the row's far end: one course deep, its headstone blank.
    p.put((CUT_STONE[0], 1, CUT_STONE[1]), (CUT_STONE[0], 1, CUT_STONE[1]), "headstone")
    for x, z in CUT:
        p.put((x, 0, z), (x, 0, z), None)
    # The black banner over the bier, on its own staff.
    p.put((8, 1, 8), (8, 1, 8), "staff")
    p.put((8, 2, 8), (8, 2, 8), "banner")
    posts(p, FIELD_POSTS)
    # The contract: the open seam row, and the field.
    for x in (0, 16):
        p.claim_box((x, 3, 1), (x, 3, 18), "tops")
    p.claim_box((0, 9, 0), (16, 10, 0), "tops")
    p.claim_box((1, 1, 18), (15, 10, 18), "grave-road")
    p.claim_box((1, 1, 1), (15, 10, 17), "field")
    palette = {
        "arch": "minecraft:polished_andesite",
        "banner": "minecraft:black_banner[rotation=8]",
        "dyke": DYKE,
        "gate": "minecraft:dark_oak_planks",
        "headstone": STONE,
        "keep": [
            {"block": "minecraft:stone_bricks", "weight": 5},
            {"block": "minecraft:mossy_stone_bricks", "weight": 2},
            {"block": "minecraft:cracked_stone_bricks", "weight": 1},
        ],
        "lantern": LANTERN,
        "mound": "minecraft:coarse_dirt",
        "post": FENCE,
        "road": "minecraft:gravel",
        "staff": FENCE,
        "turf": "minecraft:grass_block[snowy=false]",
    }
    contract = {
        "edges": [{"a": "field", "b": "exterior", "class": "walk", "via": "grave-road"}],
        "entry": "field",
        "no_body": {"tops": {"reason": "the tops of the keep wall, the dykes and the lantern posts, which nobody climbs"}},
        "spaces": {"field": {"envelope": "open"}},
    }
    solid = {"keep", "arch", "gate", "dyke", "headstone", "post", "staff", "turf", "road", "mound"}
    lamps = [((x, 2, z), 15) for x, z in FIELD_POSTS]
    dark = p.light_report(solid, lamps, 1, (1, 1, 15, 18))
    return program("the-wake-field", p, palette, contract, FIELD_MARKS, ["east", "north", "west"]), dark, p, FIELD_MARKS


def shore():
    """The beach. Frame 17 x 11 x 10: its north row (z 0) is the seam plane it
    owns, open ground onto the field; the play space x 1-15, z 1-8; the dykes
    at x 0 and x 16; a line of old tide stones along the waterline at z 9."""
    p = Piece((17, 11, 10))
    p.skip((0, 0, 0), (0, 0, 9))
    p.skip((16, 0, 0), (16, 0, 9))
    p.skip((1, 0, 0), (15, 0, 0))
    p.skip((1, 0, 9), (15, 0, 9))
    # Floor: sand, mud where the tide was, the grave road coming down.
    p.put((1, 0, 1), (15, 0, 8), "sand")
    p.put((1, 0, 7), (15, 0, 8), "wet-sand")
    p.put((8, 0, 1), (8, 0, 4), "road")
    # Dykes down both sides; the tide stones along the waterline.
    for x in (0, 16):
        p.put((x, 1, 0), (x, 2, 9), "dyke")
    p.put((1, 1, 9), (15, 1, 9), "tide-stone")
    # The shore fire and the driftwood.
    p.put((FIRE[0], 1, FIRE[1]), (FIRE[0], 1, FIRE[1]), "fire")
    for x, z in DRIFT:
        p.put((x, 1, z), (x, 1, z), "drift")
    posts(p, SHORE_POSTS)
    for x in (0, 16):
        p.claim_box((x, 3, 0), (x, 3, 9), "tops")
    p.claim_box((1, 2, 9), (15, 2, 9), "tops")
    p.claim_box((1, 1, 0), (15, 10, 0), "grave-road")
    p.claim_box((1, 1, 1), (15, 10, 8), "shore")
    palette = {
        "drift": "minecraft:stripped_oak_log[axis=x]",
        "dyke": DYKE,
        "fire": "minecraft:campfire[facing=north,lit=true,signal_fire=false,waterlogged=false]",
        "lantern": LANTERN,
        "post": FENCE,
        "road": "minecraft:gravel",
        "sand": "minecraft:sand",
        "tide-stone": TIDE_STONE,
        "wet-sand": "minecraft:mud",
    }
    contract = {
        "edges": [{"a": "exterior", "b": "shore", "class": "walk", "via": "grave-road"}],
        "entry": "shore",
        "no_body": {"tops": {"reason": "the tops of the dykes, the tide stones and the lantern posts, which nobody climbs"}},
        "spaces": {"shore": {"envelope": "open"}},
    }
    solid = {"dyke", "tide-stone", "post", "drift", "sand", "wet-sand", "road"}
    lamps = [((x, 2, z), 15) for x, z in SHORE_POSTS] + [((FIRE[0], 1, FIRE[1]), 15)]
    dark = p.light_report(solid, lamps, 1, (1, 1, 15, 8))
    return program("the-wake-shore", p, palette, contract, SHORE_MARKS, ["east", "south", "west"]), dark, p, SHORE_MARKS


def walk_map(p, marks):
    rows = []
    for z in range(p.sz):
        row = ""
        for x in range(p.sx):
            b1 = p.block.get((x, 1, z))
            b0 = p.block.get((x, 0, z))
            mark = next((s for s, pos, _ in marks if pos[0] == x and pos[2] == z), None)
            if mark:
                row += "@"
            elif b1 is None:
                row += " " if b0 is None else ("." if b0 != "road" else ":")
            else:
                row += {"keep": "#", "arch": "A", "gate": "G", "dyke": "=", "tide-stone": "-", "headstone": "+",
                        "post": "i", "staff": "|", "fire": "F", "drift": "~"}.get(b1, "?")
        rows.append(f"{z:2d} {row}")
    return "\n".join(rows)


def main():
    here = pathlib.Path(__file__).resolve().parent.parent
    out = here / "programs"
    out.mkdir(exist_ok=True)
    for stem, (prog, dark, p, marks) in (("field", field()), ("shore", shore())):
        path = out / f"{stem}.json"
        path.write_text(json.dumps(prog, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
        print(f"wrote {path}")
        if "--light" in sys.argv[1:]:
            print(f"  {stem}: {len(dark)} walk cell(s) estimated below block light 7: {dark}")
        if "--map" in sys.argv[1:]:
            print(walk_map(p, marks))


if __name__ == "__main__":
    main()
