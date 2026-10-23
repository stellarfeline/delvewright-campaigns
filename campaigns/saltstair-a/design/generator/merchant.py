#!/usr/bin/env python3
"""Emit programs/merchant.json — the merchant's house of saltstair-a.

Provenance only: the emitted JSON is the artifact of record. Every handed value
is read from `delvec allocation` and written as a `handed/...` parameter default;
no handed number is typed here.

Usage: merchant.py <delvec> <campaign-dir>
"""
import json
import subprocess
import sys
from pathlib import Path

delvec, campaign = sys.argv[1], Path(sys.argv[2])
alloc = json.loads(subprocess.run(
    [delvec, "allocation", str(campaign), "node/merchant"],
    check=True, capture_output=True, text=True).stdout)

SEAM = "middle-street-merchant"
seam = next(s for s in alloc["seams"] if s["edge"] == f"edge/{SEAM}")
(sx0, sy0, sz0), (sx1, sy1, sz1) = seam["cells"]

params = {
    "handed/datum-y": alloc["datum_y"],
    "handed/roof/lid-y": alloc["roof"]["lid_y"],
    "handed/roof/eaves": alloc["roof"]["eaves"],
    f"handed/seam/{SEAM}/y0": sy0,
    f"handed/seam/{SEAM}/y1": sy1,
    f"handed/seam/{SEAM}/z0": sz0,
    f"handed/seam/{SEAM}/z1": sz1,
}


# ---- expression / node helpers -------------------------------------------
def I(v):
    return {"expr": "int", "value": v}


def P(name):
    return {"expr": "param", "name": name}


def sub(a, b):
    return {"expr": "arith", "op": "sub", "lhs": a, "rhs": b}


def add(a, b):
    return {"expr": "arith", "op": "add", "lhs": a, "rhs": b}


def span(a, b):  # inclusive count b - a + 1
    return add(sub(b, a), I(1))


EAVES = P("handed/roof/eaves")


def size(s):
    if s == "r":
        return {"size": "relative", "weight": I(1)}
    if isinstance(s, tuple) and s[0] == "r":
        return {"size": "relative", "weight": I(s[1])}
    if isinstance(s, int):
        return {"size": "absolute", "blocks": I(s)}
    return {"size": "absolute", "blocks": s}


def split(axis, parts):
    return {"op": "split", "axis": axis,
            "sizes": [size(s) for s, _ in parts],
            "children": [c for _, c in parts]}


def fill(role):
    return {"op": "fill", "material": {"role": role}}


def call(sym):
    return {"op": "call", "symbol": sym}


VOID = {"op": "void"}
SKIP = {"op": "skip"}


def claim(region, body):
    return {"op": "claim", "region": region, "body": body}


def rule(body, when=None):
    alt = {"weight": 1, "body": body}
    if when is not None:
        alt["when"] = when
    return [alt]


def dim(a):
    return {"expr": "dim", "dim": a}


def cmp(lhs, op, rhs):
    return {"cond": "cmp", "lhs": lhs, "op": op, "rhs": rhs}


rules = {}

# ---- the whole: ground course, the storey, the roof zone -------------------
rules["house"] = rule(split("y", [
    (P("handed/datum-y"), call("ground")),
    (sub(P("handed/roof/lid-y"), P("handed/datum-y")), call("storey")),
    ("r", call("roof")),
]))

# ground course: the ring's ground is the whole's (fixed); the plot is the floor
rules["ground"] = rule(split("x", [
    (EAVES, SKIP), (1, SKIP), ("r", call("ground_row")), (1, SKIP), (EAVES, SKIP),
]))
rules["ground_row"] = rule(split("z", [
    (EAVES, SKIP), (1, SKIP), ("r", fill("floor")), (1, SKIP), (EAVES, SKIP),
]))

# ---- the storey: four walls on the ring, the interior inside --------------
rules["storey"] = rule(split("x", [
    (EAVES, SKIP),
    (1, call("west_wall")),
    ("r", call("mid")),
    (1, call("east_wall")),
    (EAVES, SKIP),
]))
rules["west_wall"] = rule(split("z", [
    (EAVES, SKIP), (1, call("corner")), ("r", call("wall_run")),
    (1, call("corner")), (EAVES, SKIP),
]))
# north and south walls run along world x: the same wall, turned
TURNED = {"op": "reorient", "orient": {"z": "local_x"}, "body": call("wall_run")}
rules["mid"] = rule(split("z", [
    (EAVES, SKIP),
    (1, TURNED),
    ("r", claim("house", call("rooms"))),
    (1, TURNED),
    (EAVES, SKIP),
]))
# east wall: the street door at the handed cells, a lantern over it
z0 = P(f"handed/seam/{SEAM}/z0")
z1 = P(f"handed/seam/{SEAM}/z1")
y0 = P(f"handed/seam/{SEAM}/y0")
y1 = P(f"handed/seam/{SEAM}/y1")
rules["east_wall"] = rule(split("z", [
    (EAVES, SKIP),
    (1, call("corner")),
    (sub(sub(z0, EAVES), I(1)), call("east_left")),
    (span(z0, z1), call("door_col")),
    ("r", call("east_right")),
    (1, call("corner")),
    (EAVES, SKIP),
]))
rules["east_left"] = rule(split("z", [
    ("r", call("plain")), (1, call("window")), (1, call("plain")),
]))
rules["east_right"] = rule(split("z", [
    (1, call("plain")), (1, call("window")), ("r", call("plain")),
]))
rules["door_col"] = rule(split("y", [
    (sub(y0, P("handed/datum-y")), fill("footing")),
    (span(y0, y1), claim("street-door", VOID)),
    ("r", call("over_door")),
]))
rules["over_door"] = rule(split("y", [(1, fill("lamp")), ("r", fill("infill"))]))

# a wall run, local z along the wall: windows symmetric about its middle
rules["wall_run"] = rule(split("z", [
    ("r", call("plain")), (1, call("window")), (2, call("plain")),
    (1, call("window")), ("r", call("plain")),
]))
# bands: cobblestone footing, stone-brick course, spruce beam, calcite infill
rules["plain"] = rule(split("y", [
    (1, fill("footing")), (1, fill("masonry")), (1, fill("beam")), ("r", fill("infill")),
]))
rules["window"] = rule(split("y", [
    (1, fill("footing")), (1, fill("pane")), (1, fill("beam")),
    (1, fill("pane")), ("r", fill("infill")),
]))
rules["corner"] = rule(split("y", [(2, fill("quoin")), ("r", fill("post"))]))

# ---- the interior: counting room west, hall east, a partition between ------
rules["rooms"] = rule(split("x", [
    (("r", 4), call("counting")),
    (1, call("partition")),
    (("r", 5), call("hall")),
]))
rules["counting"] = rule({
    "op": "mark",
    "mark": {"anchor": "node-merchant", "at": "offset", "facing": "south",
             "x": I(2), "y": I(0), "z": I(1)},
    "body": split("z", [
        (1, call("shelf_row")), ("r", call("lamps_two")), (1, call("shelf_row")),
    ]),
})
rules["shelf_row"] = rule(split("x", [("r", fill("shelf")), (1, VOID)]))
rules["partition"] = rule(split("z", [
    ("r", fill("partition")), (2, call("doorway")), (1, fill("partition")),
]))
rules["doorway"] = rule(split("y", [(3, VOID), ("r", fill("partition"))]))
rules["hall"] = rule(split("z", [(1, VOID), ("r", call("lamps_two")), (1, VOID)]))
# two lanterns hung under the ceiling, one toward each end of the room
rules["lamps_two"] = rule(split("y", [("r", VOID), (1, call("lamp_layer"))]))
rules["lamp_layer"] = rule(split("z", [
    (1, VOID), (1, call("lamp_row")), ("r", VOID), (1, call("lamp_row")), (1, VOID),
]))
rules["lamp_row"] = rule(split("x", [
    ("r", VOID), (1, fill("lamp")), ("r", VOID),
]))

# ---- the roof: lid with eaves, then 45-degree slate courses to a ridge -----
rules["roof"] = rule(claim("roof", split("y", [
    (1, call("lid_course")), ("r", call("slope_zone")),
])))
rules["lid_course"] = rule(split("x", [
    (EAVES, fill("roof_e")), ("r", fill("ceiling")), (EAVES, fill("roof_w")),
]))
rules["slope_zone"] = rule(split("x", [(EAVES, VOID), ("r", call("slope")), (EAVES, VOID)]))
rules["slope"] = [
    {"weight": 1, "when": cmp(dim("y"), "eq", I(1)),
     "body": split("x", [(1, fill("roof_e")), ("r", fill("ridge")), (1, fill("roof_w"))])},
    {"weight": 1, "when": {"cond": "all", "of": [
        cmp(dim("y"), "ge", I(2)), cmp(dim("x"), "ge", I(3))]},
     "body": split("y", [(1, call("course")), ("r", call("slope_up"))])},
    {"weight": 1, "when": {"cond": "otherwise"}, "body": VOID},
]
rules["slope_up"] = rule(split("x", [(1, VOID), ("r", call("slope")), (1, VOID)]))
rules["course"] = rule(split("x", [
    (1, fill("roof_e")), ("r", call("gable_row")), (1, fill("roof_w")),
]))
rules["gable_row"] = rule(split("z", [
    (EAVES, VOID), (1, fill("gable")), ("r", VOID), (1, fill("gable")), (EAVES, VOID),
]))

palette = {
    "floor": "minecraft:spruce_planks",
    "footing": "minecraft:cobblestone",
    "masonry": "minecraft:stone_bricks",
    "quoin": "minecraft:stone_bricks",
    "beam": {"local": "minecraft:spruce_log[axis=z]"},
    "post": "minecraft:spruce_log[axis=y]",
    "infill": "minecraft:calcite",
    "gable": "minecraft:calcite",
    "pane": {"local": "minecraft:glass_pane[east=false,north=true,south=true,waterlogged=false,west=false]"},
    "lamp": "minecraft:lantern[hanging=true,waterlogged=false]",
    "shelf": "minecraft:bookshelf",
    "partition": "minecraft:spruce_planks",
    "ceiling": "minecraft:spruce_planks",
    "roof_e": {"local": "minecraft:deepslate_tile_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]"},
    "roof_w": {"local": "minecraft:deepslate_tile_stairs[facing=west,half=bottom,shape=straight,waterlogged=false]"},
    "ridge": "minecraft:deepslate_tile_slab[type=bottom,waterlogged=false]",
}

program = {
    "version": "1.9.0",
    "name": "saltstair-a-merchant",
    "start": "house",
    "params": params,
    "palette": palette,
    "rules": rules,
    "contract": {
        "entry": "house",
        "spaces": {"house": {"envelope": "enclosed"}},
        "no_body": {"roof": {"reason": "the slate roof and the loft under it, which no one is meant to walk"}},
        "no_body_majority_ack": "a house that owns its outside owns its roof, and a steep pitched roof is more standable surface than the room under it; nobody walks it",
        "edges": [{"a": "exterior", "b": "house", "class": "walk", "via": "street-door"}],
    },
    "shown_faces": ["north", "south", "up", "west"],
}

out = campaign / "programs" / "merchant.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(program, indent=2, sort_keys=True) + "\n")
print(out)
