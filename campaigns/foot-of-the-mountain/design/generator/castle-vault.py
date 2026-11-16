#!/usr/bin/env python3
"""node/castle-vault — the old lords' vault, an easter egg under the castle yard.

    python3 castle-vault.py --allocation <delvec allocation . node/castle-vault> --out ../../programs/castle-vault.json

After the priest hole and the secret passage (the node's `references[]`): a hiding place built
into the fabric, its way in a stretch of floor that reads as the floor around it. The vault lies
under the castle yard; when the four levers are down, a square of the yard's cobbles three by
three slides away (the castle's hatch: the seam's bar lies in the castle's own floor) over a
stone stair that runs down seven into a small vaulted strongroom: four chests of arms along the
far wall, lamps on the piers between them.

Written cell by cell as a grammar of absolute sizes, as the castle's own program is, because
the stair's last treads stand in the opening itself, under the hatch, as a stair through a hole
in a floor does (the gallery's undercroft stair), and the starter keeps an opening's cells for
the connection and surveys no body standing in its top course. Frame-local: +x toward the
stair's head, +z south, the floor course at y 0 and the walk plane at y 1; the opening is the
allocation's seam cells (x 8..10, y 6, z 4..6).
"""
import json
import sys

A = json.load(open(sys.argv[sys.argv.index("--allocation") + 1]))
OUT = sys.argv[sys.argv.index("--out") + 1]
EX, EY, EZ = A["extent"]
(LX, LY, LZ), (HX, HY, HZ) = A["space"]
D = A["datum_y"]
SEAM = next(s for s in A["seams"] if s["edge"] == "edge/castle-vault")
(OX0, OY, OZ0), (OX1, _, OZ1) = SEAM["cells"]
VOIDS = set()
for v in A.get("voids", []):
    (a, b, c), (d, e, f) = v["cells"]
    VOIDS |= {(x, y, z) for x in range(a, d + 1) for y in range(b, e + 1) for z in range(c, f + 1)}

PALETTE = {
    "vault": [{"weight": 8, "block": "minecraft:stone_bricks"}, {"weight": 2, "block": "minecraft:cracked_stone_bricks"},
              {"weight": 1, "block": "minecraft:mossy_stone_bricks"}],
    "vfloor": "minecraft:polished_deepslate",
    "tread": "minecraft:stone_brick_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]",
    "chest": "minecraft:chest[facing=east,type=single,waterlogged=false]",
    "lamp": "minecraft:lantern[hanging=false,waterlogged=false]",
}
STAIR_Z = range(OZ0, OZ1 + 1)          # the stair's width, under the hatch
CHESTS = (2, 4, 6, 8)                  # the four chests along the far wall, z

cells = {}      # (x, y, z) -> (kind, role, region): kind fill | void | skip
for x in range(EX):
    for y in range(EY):
        for z in range(EZ):
            inside = LX <= x <= HX and LZ <= z <= HZ
            if (x, y, z) in VOIDS:
                cells[(x, y, z)] = ("skip", None, None)
            elif not inside:
                cells[(x, y, z)] = ("fill", "vault", None)            # the walls
            elif y < D:
                cells[(x, y, z)] = ("fill", "vfloor", None)           # the floor course
            else:
                cells[(x, y, z)] = ("void", None, "room")
# the stair: treads climbing toward the hatch, one course a column, flanked and built solid under
top = HY
first = OX0 - (top - D) + 1                                           # x of the tread at the walk plane
for z in range(OZ0 - 1, OZ1 + 2):
    for x in range(first, OX0 + 1):
        y = D + (x - first)
        for yy in range(D, y):
            cells[(x, yy, z)] = ("fill", "vault", None)
        cells[(x, y, z)] = ("fill", "tread", "room") if z in STAIR_Z else ("fill", "vault", None)
    for x in range(OX0 + 1, OX1 + 1):
        for yy in range(D, top):
            cells[(x, yy, z)] = ("fill", "vault", None)
        if z in STAIR_Z:
            cells[(x, top, z)] = ("fill", "tread" if x == OX0 + 1 else "vault", "castle-vault")
        else:
            cells[(x, top, z)] = ("fill", "vault", None)
for z in STAIR_Z:
    cells[(OX0, top, z)] = ("void", None, "castle-vault")              # the opening over the tread below
# the four chests of arms along the far wall, a lamp on each pier between them
for z in CHESTS:
    cells[(LX, D, z)] = ("fill", "chest", "room")
for z in (1, 3, 5, 7, 9):
    cells[(LX, D, z)] = ("fill", "vault", None)
    cells[(LX, D + 1, z)] = ("fill", "lamp", "room")
for z in (2, 8):
    cells[(first + 1, D, z)] = ("fill", "lamp", "room")             # at the stair's foot on either side
MARKS = {(LX, D, z): (f"vault-chest-{k}", "east") for k, z in enumerate(CHESTS, start=1)}
MARKS[(3, D, 5)] = ("node-castle-vault", "east")


def leaf(cell, xyz):
    kind, role, region = cell
    body = {"op": "skip"} if kind == "skip" else ({"op": "void"} if kind == "void" else {"op": "fill", "material": {"role": role}})
    if region:
        body = {"op": "claim", "region": region, "body": body}
    if xyz in MARKS:
        a, f = MARKS[xyz]
        body = {"op": "mark", "mark": {"anchor": a, "at": "floor_center", "facing": f}, "body": body}
    return body


def sz(n):
    return {"size": "absolute", "blocks": {"expr": "int", "value": n}}


def split(axis, runs):
    if len(runs) == 1:
        return runs[0][1]
    return {"op": "split", "axis": axis, "sizes": [sz(n) for n, _ in runs], "children": [c for _, c in runs]}


def merge(items):
    out = []
    for it in items:
        k = json.dumps(it, sort_keys=True)
        if out and out[-1][0] == k:
            out[-1][1] += 1
        else:
            out.append([k, 1, it])
    return [(n, it) for _, n, it in out]


rows = []
for z in range(EZ):
    cols = []
    for x in range(EX):
        cols.append(split("y", merge([leaf(cells[(x, y, z)], (x, y, z)) for y in range(EY)])))
    rows.append(split("x", merge(cols)))
PROGRAM = {
    "version": "1.9.0", "name": "castle_vault", "start": "place", "params": {}, "palette": PALETTE,
    "rules": {"place": [{"weight": 1, "body": split("z", merge(rows))}]},
    "contract": {"entry": "room", "spaces": {"room": {"envelope": "enclosed"}},
                 "edges": [{"a": "room", "b": "exterior", "class": "stair", "rise": 0, "via": "castle-vault"}]},
    "shown_faces": [],
}
with open(OUT, "w", encoding="utf-8") as f:
    f.write(json.dumps(PROGRAM, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
print(f"wrote {OUT}")
