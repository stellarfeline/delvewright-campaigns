#!/usr/bin/env python3
"""Emit programs/quay.json — the grammar program for node/quay of saltstair-a.

Provenance only: the emitted JSON is the artifact of record. Every handed
value is read from `delvec allocation` and declared as a `handed/...`
parameter; the geometry is written as expressions over those parameters and
the scope's own extents, so no handed number is retyped here.

Scene: a straight stone quay at the water. Stone-brick paving banded with
polished andesite, a polished-andesite coping on a stone wall whose foot is
weathered mossy at the waterline, spruce-log bollards along the water edge,
a low stone-brick parapet on the landward ring, and lanterns on kerb posts
flanking the foot of the fifth flight and the warehouse door.

Usage: quay.py <delvec> <campaign-dir> <out.json>
"""
import json
import subprocess
import sys

DELVEC, CAMPAIGN, OUT = sys.argv[1:4]
PLACE = "node/quay"

raw = subprocess.run([DELVEC, "allocation", CAMPAIGN, PLACE], check=True,
                     capture_output=True, text=True).stdout
alloc, _ = json.JSONDecoder().raw_decode(raw)

params = {"handed/datum-y": alloc["datum_y"]}
seam_stem = {}
for seam in alloc["seams"]:
    stem = seam["edge"].split("/", 1)[1]
    (x0, y0, z0), (x1, y1, z1) = seam["cells"]
    for k, v in (("x0", x0), ("y0", y0), ("z0", z0), ("x1", x1), ("y1", y1), ("z1", z1), ("rise", seam["rise"])):
        params[f"handed/seam/{stem}/{k}"] = v
    seam_stem[seam["other"]] = stem
FLIGHT = seam_stem["node/flight-5"]
DOOR = seam_stem["node/warehouse"]
(OWED,) = [a.split("/", 1)[1] for a in alloc["owed_anchors"]]


# ---- expression helpers -------------------------------------------------
def I(v):
    return {"expr": "int", "value": v}


def P(name):
    return {"expr": "param", "name": name}


def S(stem, k):
    return P(f"handed/seam/{stem}/{k}")


def ar(op, a, b):
    return {"expr": "arith", "lhs": a, "op": op, "rhs": b}


def add(a, b):
    return ar("add", a, b)


def sub(a, b):
    return ar("sub", a, b)


def div(a, b):
    return ar("div", a, b)


def dim(d):
    return {"expr": "dim", "dim": d}


def ab(e):
    return {"size": "absolute", "blocks": e if isinstance(e, dict) else I(e)}


def rel(w=1):
    return {"size": "relative", "weight": I(w)}


def call(sym):
    return {"op": "call", "symbol": sym}


def fill(role):
    return {"op": "fill", "material": {"role": role}}


def void():
    return {"op": "void"}


def claim(region, body):
    return {"op": "claim", "region": region, "body": body}


def split(axis, sizes, children, repeat=False):
    node = {"op": "split", "axis": axis, "sizes": sizes, "children": children}
    if repeat:
        node["repeat"] = True
    return node


def width(stem):  # inclusive cell count of a seam along x
    return add(sub(S(stem, "x1"), S(stem, "x0")), I(1))


def height(stem):  # inclusive cell count of a seam along y
    return add(sub(S(stem, "y1"), S(stem, "y0")), I(1))


def one(body):
    return [{"weight": 1, "body": body}]


WALL_RUN = {"local": "minecraft:stone_brick_wall[east=low,north=none,south=none,up=true,waterlogged=false,west=low]"}

palette = {
    "pave": [
        {"weight": 8, "block": "minecraft:stone_bricks"},
        {"weight": 1, "block": "minecraft:cracked_stone_bricks"},
        {"weight": 1, "block": "minecraft:mossy_stone_bricks"},
    ],
    "band": "minecraft:polished_andesite",
    "coping": "minecraft:polished_andesite",
    "quay-wall": [
        {"weight": 3, "block": "minecraft:stone_bricks"},
        {"weight": 2, "block": "minecraft:mossy_stone_bricks"},
    ],
    "bollard": "minecraft:spruce_log[axis=y]",
    "parapet": WALL_RUN,
    "post": "minecraft:stone_brick_wall[east=none,north=none,south=none,up=true,waterlogged=false,west=none]",
    "lamp": "minecraft:lantern[hanging=false,waterlogged=false]",
}

R = {}

# The quay's open walk: every cell a body stands in lies in this one space.
R["quay-air"] = one(claim("quay", void()))
R["flight-opening"] = one(claim(FLIGHT, void()))
R["door-opening"] = one(claim(DOOR, void()))

# Courses below the walk plane: the site's fill (voided) and, on the water
# ring, the quay wall standing down to the harbour floor.
R["foundation"] = one(split("z", [rel(), ab(1)], [void(), fill("quay-wall")]))

# The paving course: banded field, polished-andesite coping at the water.
R["field-band"] = one(split("x", [ab(1), ab(1), ab(2)], [fill("pave"), fill("band"), fill("pave")], repeat=True))
R["field"] = one(split("x", [ab(1), rel(), ab(1)], [fill("pave"), call("field-band"), fill("pave")]))
R["pave-course"] = one(split("z", [rel(), ab(1)], [call("field"), fill("coping")]))

# A lantern on a kerb post: the post one course, the lantern on it, open air above.
# The air over the lantern is out of the walk: a lantern's top is a foothold
# no route uses, and it stands proud of the walk plane by two courses.
R["lamp-head"] = one(claim("lamp-head", void()))
R["lamp-post"] = one(split("y", [ab(1), ab(1), rel()], [fill("post"), fill("lamp"), call("lamp-head")]))

# The flight's foot: the opening the street comes out of, at its handed cells.
R["flight-foot"] = one(split("y", [ab(height(FLIGHT)), rel()], [call("flight-opening"), call("quay-air")]))
# The warehouse door: its handed cells open, the space above it the quay's.
R["door-foot"] = one(split("y", [ab(height(DOOR)), rel()], [call("door-opening"), call("quay-air")]))

# The first layer beside the north party plane, along x:
#   ring | quay | post | flight opening | post | quay | post | door | post | quay | ring
R["first-layer"] = one(split("x", [
    ab(1),
    ab(sub(S(FLIGHT, "x0"), I(2))),
    ab(1),
    ab(width(FLIGHT)),
    ab(1),
    ab(sub(sub(S(DOOR, "x0"), S(FLIGHT, "x1")), I(3))),
    ab(1),
    ab(width(DOOR)),
    ab(1),
    rel(),
    ab(1),
], [
    call("ring-end"),
    call("quay-air"),
    call("lamp-post"),
    call("flight-foot"),
    call("lamp-post"),
    call("quay-air"),
    call("lamp-post"),
    call("door-foot"),
    call("lamp-post"),
    call("quay-air"),
    call("ring-end"),
]))

# The landward ring: a low parapet course, open air above.
R["parapet-course"] = one(split("y", [ab(1), rel()], [fill("parapet"), void()]))
R["ring-end"] = one({"op": "reorient", "orient": {"x": "world_z", "z": "world_x"},
                     "body": call("parapet-course")})
R["north-ring"] = one(call("parapet-course"))

# The water edge: spruce-log bollards along the coping, every fourth cell.
R["bollard-run"] = one(split("x", [ab(1), ab(1), ab(2)], [call("quay-air"), fill("bollard"), call("quay-air")], repeat=True))
R["bollard-course"] = one(split("x", [ab(1), rel(), ab(1)], [call("ring-end"), call("bollard-run"), call("ring-end")]))
R["water-edge"] = one(split("y", [ab(1), rel()], [call("bollard-course"), call("quay-air")]))

R["interior"] = one(split("x", [ab(1), rel(), ab(1)], [call("ring-end"), call("quay-air"), call("ring-end")]))

R["air-band"] = one(split("z", [ab(1), ab(1), rel(), ab(1)],
                          [call("north-ring"), call("first-layer"), call("interior"), call("water-edge")]))

R["place"] = one({
    "op": "mark",
    "mark": {"anchor": OWED, "at": "offset", "facing": "south",
             "x": div(add(S(FLIGHT, "x0"), S(FLIGHT, "x1")), I(2)),
             "y": P("handed/datum-y"),
             "z": div(dim("z"), I(2))},
    "body": split("y", [ab(sub(P("handed/datum-y"), I(1))), ab(1), rel()],
                  [call("foundation"), call("pave-course"), call("air-band")]),
})

program = {
    "version": "1.9.0",
    "name": "saltstair-a-quay",
    "start": "place",
    "params": params,
    "palette": palette,
    "rules": R,
    "contract": {
        "entry": "quay",
        "spaces": {"quay": {"envelope": "open"}},
        "no_body": {"lamp-head": {"reason": "the top of a lantern on its kerb post, a foothold two courses above the walk that no one is meant to stand on"}},
        "edges": [
            {"a": "quay", "b": "exterior", "class": "walk", "via": FLIGHT},
            {"a": "quay", "b": "exterior", "class": "walk", "via": DOOR},
        ],
    },
    "shown_faces": ["east", "north", "south", "west"],
}

with open(OUT, "w") as f:
    json.dump(program, f, indent=2, sort_keys=True)
    f.write("\n")
