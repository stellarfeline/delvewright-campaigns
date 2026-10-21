#!/usr/bin/env python3
"""Write the two place programs of The Sentinels.

    delvec allocation campaigns/the-sentinels --all --prefabs prefabs > alloc.json
    python3 campaigns/the-sentinels/design/build_pieces.py alloc.json [--map]

`delvec detail` expands `programs/<place stem>.json` inside the frame the site
plan hands each place: the lodge 9 x 6 x 7 (play space x 1-7, z 1-5), the
hall 13 x 8 x 26 (play space x 1-11, z 1-24, the lid at y 7); in both the
floor course is y 0 and the walk y 1. The lodge's south wall owns the doorway
into the hall's north end. The piece is stated as a cell grid
in the frame's own coordinates (x east, y up, z south, the frame's minimum
corner at 0) and written out as a grammar program: the grid is cut along x
into runs of identical slices, each slice along z, each column along y, so
every leaf is one material over one box, wrapped in the contract region it
belongs to.

The allocation is read, never copied: the frame's extent, the voids (cells the
place does not own, written as `structure_void`) and the play space come from
it, so a plan edit is followed by re-running the two commands above.

The hall: a red runner down the middle (x 3-9) from the keeper's end to a shut
iron door in the south wall; stone plinths against both walls, each figure on
its plinth's top within a sword's reach of the runner's edge; the iron golem on
the floor beside the runner; lanterns on chains from the lid.
"""
import json
import pathlib
import sys

VERSION = "1.9.0"
SKIP = "__skip__"


def box(a, b):
    return [(x, y, z)
            for x in range(min(a[0], b[0]), max(a[0], b[0]) + 1)
            for y in range(min(a[1], b[1]), max(a[1], b[1]) + 1)
            for z in range(min(a[2], b[2]), max(a[2], b[2]) + 1)]


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
        """Floor course, walls round the ring, lid; every play cell air."""
        sx, sy, sz = self.sx, self.sy, self.sz
        self.put((0, 0, 0), (sx - 1, 0, sz - 1), floor)
        self.put((0, sy - 1, 0), (sx - 1, sy - 1, sz - 1), lid)
        for x in range(sx):
            for z in range(sz):
                if x in (0, sx - 1) or z in (0, sz - 1):
                    self.put((x, 1, z), (x, sy - 2, z), wall)
        (lo, hi) = self.alloc["space"]
        self.put(lo, hi, None)

    def seam(self, edge):
        for s in self.alloc["seams"]:
            if s["edge"] == edge:
                return s
        raise KeyError(edge)

    def opening(self, edge, region=None):
        s = self.seam(edge)
        (a, b) = s["cells"]
        self.put(a, b, None)
        self.claim_box(a, b, region or edge.split("/", 1)[1])


def program(name, piece, palette, contract, marks):
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
        "shown_faces": [],
        "start": "place",
        "version": VERSION,
    }


HANGING = "minecraft:lantern[hanging=true,waterlogged=false]"
CHAIN = "minecraft:iron_chain[axis=y,waterlogged=false]"

# The plinths: (x, z) of a one-course stone plinth, the figure standing on top.
WEST = 1
EAST = 11
PLINTHS = {
    "plinth-w1": (WEST, 5, "east"),
    "plinth-e1": (EAST, 5, "west"),
    "plinth-w2": (WEST, 10, "east"),
    "plinth-e2": (EAST, 10, "west"),
    "plinth-e3": (EAST, 15, "west"),
}
# Empty plinths, so the rank reads as a rank and the captain's is not the only
# one on its row.
EMPTY_PLINTHS = [(WEST, 20), (EAST, 20)]
LAMPS = [(x, 5, z) for x in (3, 9) for z in (3, 8, 13, 18, 22)]
RUNNER = (3, 9)


def hall(a):
    p = Piece(a)
    p.shell()
    # The red runner down the middle, from the keeper's end to the far door.
    p.put((RUNNER[0], 0, 1), (RUNNER[1], 0, 24), "runner")
    # Plinths against both walls.
    for _, (x, z, _) in PLINTHS.items():
        p.put((x, 1, z), (x, 1, z), "plinth")
    for x, z in EMPTY_PLINTHS:
        p.put((x, 1, z), (x, 1, z), "plinth")
    # The doorway from the lodge at the runner's north end, and the shut iron
    # door in the south wall at its far end.
    p.opening("edge/hall-door")
    p.put((6, 1, 25), (6, 1, 25), "door-low")
    p.put((6, 2, 25), (6, 2, 25), "door-high")
    # Lanterns on chains from the lid.
    for (x, y, z) in LAMPS:
        p.put((x, y, z), (x, y, z), "hanging")
        p.put((x, y + 1, z), (x, 6, z), "chain")
    p.claim_box((1, 1, 1), (11, 6, 24), "room", air_only=True)
    palette = {
        "chain": CHAIN,
        "door-high": "minecraft:iron_door[facing=north,half=upper,hinge=left,open=false,powered=false]",
        "door-low": "minecraft:iron_door[facing=north,half=lower,hinge=left,open=false,powered=false]",
        "floor": "minecraft:polished_deepslate",
        "hanging": HANGING,
        "lid": "minecraft:dark_oak_planks",
        "plinth": "minecraft:polished_andesite",
        "runner": "minecraft:red_wool",
        "wall": "minecraft:stone_bricks",
    }
    contract = {
        "edges": [{"a": "room", "b": "exterior", "class": "walk", "via": "hall-door"}],
        "entry": "room",
        "spaces": {"room": {"envelope": "enclosed"}},
    }
    marks = [
        ("node-hall", (6, 1, 12), "south"),
        ("far-door", (6, 1, 23), "south"),
        ("door-ward", (8, 1, 24), "north"),
        ("golem-stand", (2, 1, 15), "east"),
    ] + [(stem, (x, 2, z), facing) for stem, (x, z, facing) in PLINTHS.items()]
    return program("the-sentinels-hall", p, palette, contract, marks), p, marks


def lodge(a):
    p = Piece(a)
    p.shell(wall="panel", floor="boards", lid="lid")
    p.opening("edge/hall-door")
    # The keeper's desk across the room's west half, the keeper behind it.
    p.put((1, 1, 3), (3, 1, 3), "desk")
    p.put((4, 3, 2), (4, 3, 2), "hanging")
    p.put((4, 4, 2), (4, 4, 2), "chain")
    p.put((6, 3, 4), (6, 3, 4), "hanging")
    p.put((6, 4, 4), (6, 4, 4), "chain")
    p.claim_box((1, 1, 1), (7, 4, 5), "room", air_only=True)
    palette = {
        "boards": "minecraft:spruce_planks",
        "chain": CHAIN,
        "desk": "minecraft:dark_oak_planks",
        "hanging": HANGING,
        "lid": "minecraft:dark_oak_planks",
        "panel": "minecraft:stripped_spruce_log[axis=y]",
    }
    contract = {
        "edges": [{"a": "room", "b": "exterior", "class": "walk", "via": "hall-door"}],
        "entry": "room",
        "spaces": {"room": {"envelope": "enclosed"}},
    }
    marks = [
        ("spawn", (5, 1, 2), "south", "entry"),
        ("node-lodge", (4, 1, 4), "south"),
        ("keeper-post", (2, 1, 2), "south"),
    ]
    return program("the-sentinels-lodge", p, palette, contract, marks), p, marks


def walk_map(p, marks):
    rows = []
    for z in range(p.sz):
        row = ""
        for x in range(p.sx):
            b1 = p.block.get((x, 1, z))
            b0 = p.block.get((x, 0, z))
            mark = next((s for s, pos, *_ in marks if pos[0] == x and pos[2] == z), None)
            if mark:
                row += "@"
            elif b1 is None:
                row += "=" if b0 == "runner" else "."
            else:
                row += {"wall": "#", "plinth": "P", "door-low": "D"}.get(b1, "?")
        rows.append(f"{z:2d} {row}")
    return "\n".join(rows)


def main():
    alloc = {a["place"]: a for a in json.loads(pathlib.Path(sys.argv[1]).read_text())}
    here = pathlib.Path(__file__).resolve().parent.parent
    out = here / "programs"
    out.mkdir(exist_ok=True)
    for stem, build in (("lodge", lodge), ("hall", hall)):
        prog, p, marks = build(alloc[f"node/{stem}"])
        path = out / f"{stem}.json"
        path.write_text(json.dumps(prog, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
        print(f"wrote {path}")
        if "--map" in sys.argv[2:]:
            print(walk_map(p, marks))


if __name__ == "__main__":
    main()
