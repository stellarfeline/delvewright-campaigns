#!/usr/bin/env python3
"""node/cat-den — the chasm under the castle, its bridge, and the cat's den on the far ledge.

    python3 cat-den.py --allocation <delvec allocation . node/cat-den> --out ../../programs/cat-den.json

A chasm hollowed out of the mountain under the castle. The ladder from the old miner's hut comes
down onto a rock ledge along the chasm's west side; from the ledge a long bridge of planks, fence
rails and lanterns on its posts (after the abandoned mineshaft, the node's `references[]`) is slung
across to a ledge on the far side, where the cat has her den: a plank wall, a cushion, a
grindstone, her old dish, a board of fishes and a chest. Far below the bridge the chasm's floor is
lit by soul fire, cold and blue; the old stone figure that stands on it is not drawn here: it is the
demo level's statue, stamped in by the campaign's world edits (`batch/the-thing`), set out
from `anchor/node-cat-den`.

Written cell by cell as a grammar of absolute sizes, as the castle's vault is, because the ladder
stands in the opening itself, under the hut's hatch, and the starter does not answer a way through
a floor this place does not own. Frame-local: +x east, +z south, the floor course at y 0, the walk
plane at y 1, the lid at the frame's top course; the opening the allocation's seam cell.
"""
import json
import sys

A = json.load(open(sys.argv[sys.argv.index("--allocation") + 1]))
OUT = sys.argv[sys.argv.index("--out") + 1]
EX, EY, EZ = A["extent"]
(LX, LY, LZ), (HX, HY, HZ) = A["space"]
D = A["datum_y"]
SEAM = next(s for s in A["seams"] if s["edge"] == "edge/miners-hut-to-cat-den")
(OX, OY, OZ), _ = SEAM["cells"]
VOIDS = set()
for v in A.get("voids", []):
    (a, b, c), (d, e, f) = v["cells"]
    VOIDS |= {(x, y, z) for x in range(a, d + 1) for y in range(b, e + 1) for z in range(c, f + 1)}

PALETTE = {
    "rock": [{"weight": 6, "block": "minecraft:stone"}, {"weight": 3, "block": "minecraft:deepslate[axis=y]"},
             {"weight": 2, "block": "minecraft:tuff"}, {"weight": 1, "block": "minecraft:andesite"}],
    "bed": [{"weight": 3, "block": "minecraft:deepslate[axis=y]"}, {"weight": 1, "block": "minecraft:cobbled_deepslate"}],
    "deck": [{"weight": 5, "block": "minecraft:spruce_planks"}, {"weight": 2, "block": "minecraft:oak_planks"}],
    "rail": "minecraft:oak_fence[east=false,north=false,south=false,waterlogged=false,west=false]",
    "post": "minecraft:oak_log[axis=y]",
    "lamp": "minecraft:lantern[hanging=false,waterlogged=false]",
    "soulfire": "minecraft:soul_campfire[facing=south,lit=true,signal_fire=false,waterlogged=false]",
    "ladder": "minecraft:ladder[facing=east,waterlogged=false]",
    "wallboards": "minecraft:spruce_planks",
    "chest": "minecraft:chest[facing=north,type=single,waterlogged=false]",
    "sign": "minecraft:spruce_wall_sign[facing=north,waterlogged=false]",
    "cushion": "minecraft:red_carpet",
    "grindstone": "minecraft:grindstone[face=floor,facing=north]",
    "dish": "minecraft:cauldron",
}
TOP = HY                       # the headroom's top course; the lid is the course over it
LEDGE = 64                     # the ledges' and the bridge's walk plane (frame-local)
WEST = range(1, 10)            # the west ledge's columns
EAST = range(101, 111)         # the east ledge's columns
BRIDGE_Z = range(48, 51)       # the bridge's deck, three wide
assert OX in WEST and LEDGE < OY, "the ladder comes down onto the west ledge"


ADIT = 30                      # an old miners' adit runs back into the rock from the west shelf, here


def solid(x, y, z):
    """The chasm's rock: its shell, the floor course, the two cliffs under the ledges."""
    if x in (0, EX - 1) or z in (0, EZ - 1) or y == 0 or y > TOP:
        return True
    if (x in WEST or x in EAST) and y < LEDGE:
        return True
    # under the hut: the chasm's roof is a course of rock beneath the hut's floor wherever the hut
    # stands over it (the hut's own courses are the allocation's voids), so the hut's yard of
    # gravel lies on rock and not over the drop; only the shaft's cell, the ladder's, goes through
    if y == TOP and (x, TOP + 1, z) in VOIDS and not (x == OX and z == OZ):
        return True
    # over the ledges the chasm's walls come in close: a ledge is a shelf four wide along the rock,
    # from under the hut's shaft to the bridge on the west, and the den's shelf on the east; the
    # rest of the cliffs' tops is rock to the roof
    if x in WEST and y >= LEDGE and not (x >= 6 and 4 <= z <= BRIDGE_Z[-1] + 2) and not (x == OX and z == OZ) \
            and not (x == OX + 1 and z == OZ and y <= LEDGE + 1) and not (z == ADIT and y <= LEDGE + 1):
        return True
    if x in EAST and y >= LEDGE and not (x <= 104 and BRIDGE_Z[0] - 2 <= z <= EZ - 2) and not (BRIDGE_Z[0] - 2 <= z <= EZ - 2 and y <= LEDGE + 4):
        return True
    return False


cells = {}
for x in range(EX):
    for y in range(EY):
        for z in range(EZ):
            if (x, y, z) in VOIDS:
                cells[(x, y, z)] = ("skip", None, None)
            elif solid(x, y, z):
                cells[(x, y, z)] = ("fill", "bed" if y == 0 else "rock", None)
            elif y < LEDGE:
                cells[(x, y, z)] = ("void", None, "abyss")     # the chasm below the bridge: seen, never walked
            else:
                cells[(x, y, z)] = ("void", None, "room")


def put(x, y, z, role, region="room"):
    cells[(x, y, z)] = ("fill", role, region)


# the bridge: a deck of planks over the abyss, fence rails two high either side (a body standing
# on a lantern or a chest clears a rail one high, and the chasm is not to be fallen into), a post with a lantern
# every six cells, alternating sides
for x in range(10, 101):
    for z in BRIDGE_Z:
        put(x, LEDGE - 1, z, "deck", None)
    for y in (LEDGE, LEDGE + 1):        # two high: nothing a body stands on clears it
        put(x, y, BRIDGE_Z[0] - 1, "rail")
        put(x, y, BRIDGE_Z[-1] + 1, "rail")
    for z in (BRIDGE_Z[0] - 1, BRIDGE_Z[-1] + 1):
        put(x, LEDGE - 1, z, "deck", None)
for i, x in enumerate(range(13, 100, 6)):
    z = BRIDGE_Z[0] - 1 if i % 2 == 0 else BRIDGE_Z[-1] + 1
    put(x, LEDGE, z, "post")
    put(x, LEDGE + 1, z, "lamp")
    cells[(x, LEDGE + 2, z)] = ("void", None, "lamp-tops")   # over a lantern on its post: seen, never stood on
# rails along the ledges' edges, open where the bridge leaves them
for z in range(1, EZ - 1):
    if z not in range(BRIDGE_Z[0] - 1, BRIDGE_Z[-1] + 2):
        if 4 <= z <= BRIDGE_Z[-1] + 2:
            put(WEST[-1], LEDGE, z, "rail")
            put(WEST[-1], LEDGE + 1, z, "rail")
        if BRIDGE_Z[0] - 2 <= z <= EZ - 2:
            put(EAST[0], LEDGE, z, "rail")
            put(EAST[0], LEDGE + 1, z, "rail")
# lanterns along the west ledge, every six cells, against the wall
for z in range(5, BRIDGE_Z[0] - 1, 6):
    put(6, LEDGE, z, "lamp")
# the ladder up to the hut, on a rock pillar, in the column under the hatch; its top rung, in the
# opening itself, is the way's
for y in range(LEDGE, TOP + 1):
    put(OX - 1, y, OZ, "rock", None)
    put(OX, y, OZ, "ladder", "miners-hut-to-cat-den" if y == TOP else "room")
# the shaft's throat round the ladder's top rung, under the hut's floor, is rock: the way's face is
# the one it rises through, up into the hut
for (tx, tz) in ((OX + 1, OZ), (OX, OZ - 1), (OX, OZ + 1)):
    put(tx, TOP, tz, "rock", None)
# the old adit's blind end, where it was given up at the chasm's wall
cells[(0, LEDGE, ADIT)] = ("void", None, "niche")
cells[(0, LEDGE + 1, ADIT)] = ("void", None, "niche")
put(1, LEDGE, ADIT, "lamp")
# soul fire on the chasm's floor, cold and blue, every eight cells
for x in range(14, 100, 8):
    for z in range(4, EZ - 2, 8):
        put(x, 1, z, "soulfire", "abyss")
# the cat's den on the east ledge: a plank wall at its back, the chest, the board of fishes, the
# cushion, the grindstone, her old dish, a lantern
for x in range(EAST[0] + 1, EAST[-1] + 1):
    for y in range(LEDGE, LEDGE + 4):
        put(x, y, EZ - 2, "wallboards", None)
    cells[(x, LEDGE + 4, EZ - 2)] = ("void", None, "lamp-tops")      # over the den's wall: seen, never stood on
put(109, LEDGE, EZ - 3, "chest")
put(106, LEDGE + 1, EZ - 3, "sign")
put(104, LEDGE, EZ - 3, "cushion")
put(103, LEDGE, EZ - 3, "grindstone")
put(107, LEDGE, EZ - 3, "dish")
put(110, LEDGE, EZ - 5, "lamp")
put(102, LEDGE, EZ - 8, "lamp")

MARKS = {(109, LEDGE, EZ - 3): ("den-chest", "north"), (106, LEDGE + 1, EZ - 3): ("den-sign", "north"),
         (106, LEDGE, EZ - 6): ("node-cat-den", "west")}


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
    "version": "1.10.0", "name": "cat_den", "start": "place", "params": {}, "palette": PALETTE,
    "rules": {"place": [{"weight": 1, "body": split("z", merge(rows))}]},
    "contract": {"entry": "room", "spaces": {"room": {"envelope": "enclosed"}},
                 "no_body": {"abyss": {"reason": "the chasm under the bridge, its floor far below: seen, never walked"},
                             "niche": {"reason": "the blind end of an old adit off the west shelf, given up at the rock: a body steps into it and no further"},
                             "lamp-tops": {"reason": "the tops of the bridge's lanterns on their posts and of the den's wall: seen, never stood on"}},
                 "no_body_majority_ack": "a chasm: the ledges and the bridge across it are the play space, and the depth under them is the view",
                 "edges": [{"a": "room", "b": "exterior", "class": "walk", "via": "miners-hut-to-cat-den"}]},
    "shown_faces": ["up"],   # the roof of rock shows where the high ground over it lies at its own height
}
with open(OUT, "w", encoding="utf-8") as f:
    f.write(json.dumps(PROGRAM, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
print(f"wrote {OUT}")
