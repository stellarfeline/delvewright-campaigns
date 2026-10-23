#!/usr/bin/env python3
"""Emit programs/harbourmaster.json — the harbourmaster's house.

Provenance only: the emitted JSON is the artifact of record. Every handed
value is read from `delvec allocation` and written as a `handed/...`
parameter default; no handed number is typed here.

Usage: harbourmaster.py <delvec> <prefabs> <campaign-dir>
"""
import json
import subprocess
import sys
from pathlib import Path

PLACE = "node/harbourmaster"
SEAM = "edge/shore-street-harbourmaster"
STEM = SEAM.split("/", 1)[1]


def allocation(delvec, prefabs, campaign):
    out = subprocess.run(
        [delvec, "--prefabs", prefabs, "allocation", campaign, PLACE],
        check=True, capture_output=True, text=True).stdout
    obj, _ = json.JSONDecoder().raw_decode(out.lstrip())
    return obj


# --- expression and node helpers -------------------------------------------
def P(n): return {"expr": "param", "name": n}
def I(v): return {"expr": "int", "value": v}
def add(a, b): return {"expr": "arith", "op": "add", "lhs": a, "rhs": b}
def sub(a, b): return {"expr": "arith", "op": "sub", "lhs": a, "rhs": b}
def D(axis): return {"expr": "dim", "dim": axis}
def A(e): return {"size": "absolute", "blocks": e if isinstance(e, dict) else I(e)}
def R(w=1): return {"size": "relative", "weight": I(w)}
def split(axis, parts):
    return {"op": "split", "axis": axis,
            "sizes": [s for s, _ in parts], "children": [c for _, c in parts]}
def fill(role): return {"op": "fill", "material": {"role": role}}
VOID = {"op": "void"}
def call(s): return {"op": "call", "symbol": s}
def claim(region, body): return {"op": "claim", "region": region, "body": body}
def one(body): return [{"weight": 1, "body": body}]
def cmp(lhs, op, rhs): return {"cond": "cmp", "lhs": lhs, "op": op, "rhs": rhs}

H = "handed/"
DATUM, BOTTOM = H + "datum-y", H + "ground/bottom-y"
LID, EAVES = H + "roof/lid-y", H + "roof/eaves"
SY0, SY1 = f"{H}seam/{STEM}/y0", f"{H}seam/{STEM}/y1"
SZ0, SZ1 = f"{H}seam/{STEM}/z0", f"{H}seam/{STEM}/z1"
EAVE = A(P(EAVES))
RING = A(1)  # the ring is one cell by definition of the frame


def program(alloc):
    seam = next(s for s in alloc["seams"] if s["edge"] == SEAM)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = seam["cells"]
    params = {
        DATUM: alloc["datum_y"],
        BOTTOM: alloc["ground"]["bottom_y"],
        LID: alloc["roof"]["lid_y"],
        EAVES: alloc["roof"]["eaves"],
        SY0: sy0, SY1: sy1, SZ0: sz0, SZ1: sz1,
        "lamp_z": 2,
    }
    stair = "minecraft:dark_oak_stairs[facing={},half=bottom,shape=straight,waterlogged=false]"
    palette = {
        "floor": "minecraft:cobblestone",
        "base": "minecraft:stone_bricks",
        "infill": "minecraft:calcite",
        "post": "minecraft:spruce_log[axis=y]",
        "beam": "minecraft:spruce_wood[axis=y]",
        "glass": "minecraft:glass",
        "ceiling": "minecraft:spruce_planks",
        "ridge": "minecraft:dark_oak_planks",
        "roof_n": stair.format("south"),
        "roof_s": stair.format("north"),
        "lantern": "minecraft:lantern[hanging=true,waterlogged=false]",
        "gable_lamp": "minecraft:air",
        "chart_table": "minecraft:cartography_table",
        "shelf": "minecraft:bookshelf",
    }
    rules = {}

    # The frame, bottom to top: ground course, the storey, the roof zone.
    rules["house"] = one(split("y", [
        (A(sub(P(DATUM), P(BOTTOM))), call("ground")),
        (A(sub(P(LID), P(DATUM))), call("storey")),
        (R(), claim("roof", call("roof"))),
    ]))
    # Cobblestone floor over the plot; the ring's ground is the whole's.
    rules["ground"] = one(split("x", [
        (EAVE, VOID), (RING, VOID),
        (R(), split("z", [(EAVE, VOID), (RING, VOID), (R(), fill("floor")),
                          (RING, VOID), (EAVE, VOID)])),
        (RING, VOID), (EAVE, VOID)]))

    # --- the storey: four walls on the ring, the room inside ----------------
    rules["storey"] = one(split("x", [
        (EAVE, VOID), (RING, call("wall_west")), (R(), call("mid")),
        (RING, call("wall_east")), (EAVE, VOID)]))
    rules["mid"] = one(split("z", [
        (EAVE, VOID), (RING, call("wall_long")), (R(), call("interior")),
        (RING, call("wall_long")), (EAVE, VOID)]))
    # north and south walls: the same run, turned to lie along x
    rules["wall_long"] = one({"op": "reorient", "orient": {"x": "local_z", "z": "local_x"},
                              "body": call("run")})
    rules["wall_west"] = one(split("z", [
        (EAVE, VOID), (RING, call("post")), (R(), call("run")),
        (RING, call("post")), (EAVE, VOID)]))
    # east wall: the door at the handed cells, a window beside it
    rules["wall_east"] = one(split("z", [
        (A(P(SZ0)), split("z", [(EAVE, VOID), (RING, call("post")), (R(), call("panel"))])),
        (A(add(sub(P(SZ1), P(SZ0)), I(1))), call("door_col")),
        (R(), split("z", [(R(), call("east_run")), (RING, call("post")), (EAVE, VOID)])),
    ]))
    rules["east_run"] = [
        {"weight": 1, "when": cmp(D("z"), "ge", I(4)),
         "body": split("z", [(A(1), call("panel")), (A(2), call("window")), (R(), call("panel"))])},
        {"weight": 1, "when": {"cond": "otherwise"}, "body": call("panel")},
    ]
    rules["door_col"] = one(split("y", [
        (A(sub(P(SY0), P(DATUM))), fill("base")),
        (A(add(sub(P(SY1), P(SY0)), I(1))), claim("east-door", VOID)),
        (R(), call("lintel")),
    ]))
    # the door lantern hangs in the head of the doorway, under the plate beam
    rules["lintel"] = [
        {"weight": 1, "when": cmp(D("y"), "ge", I(2)),
         "body": split("y", [(R(), fill("lantern")), (A(1), fill("beam"))])},
        {"weight": 1, "when": {"cond": "otherwise"}, "body": fill("beam")},
    ]
    # a wall run: two windows set symmetrically in panels
    rules["run"] = [
        {"weight": 1, "when": cmp(D("z"), "ge", I(7)),
         "body": split("z", [(R(), call("panel")), (A(2), call("window")), (R(), call("panel")),
                             (A(2), call("window")), (R(), call("panel"))])},
        {"weight": 1, "when": {"cond": "otherwise"}, "body": call("panel")},
    ]
    # stone-brick base, calcite infill, spruce plate beam
    rules["panel"] = one(split("y", [(A(2), fill("base")), (R(), fill("infill")), (A(1), fill("beam"))]))
    rules["window"] = one(split("y", [(A(1), fill("base")), (A(2), fill("glass")), (R(), fill("beam"))]))
    rules["post"] = one(split("y", [(A(2), fill("base")), (R(), fill("post"))]))

    # --- the room ------------------------------------------------------------
    rules["interior"] = one(claim("house", {
        "op": "mark",
        "mark": {"anchor": "node-harbourmaster", "at": "offset", "facing": "east",
                 "x": I(1), "y": I(0), "z": I(3)},
        "body": split("y", [(A(1), call("furnish")), (R(), VOID), (A(1), call("lamps"))]),
    }))
    # the harbourmaster's chart table and shelves against the west wall
    rules["furnish"] = one(split("x", [
        (A(1), split("z", [(A(1), VOID), (A(1), fill("chart_table")), (A(2), VOID),
                           (A(3), fill("shelf")), (R(), VOID)])),
        (R(), VOID)]))
    # two lanterns hung from the ceiling, staggered
    rules["lamps"] = one(split("x", [
        (A(2), VOID),
        (A(1), call("lamp_col")),
        (A(2), VOID),
        (A(1), {"op": "bind", "params": {"lamp_z": I(5)}, "body": call("lamp_col")}),
        (R(), VOID)]))
    rules["lamp_col"] = one(split("z", [(A(P("lamp_z")), VOID), (A(1), fill("lantern")), (R(), VOID)]))

    # --- the roof: dark oak shingles, ridge east-west, gables east and west -
    rules["roof"] = one(split("y", [(A(1), call("lid_course")), (R(), call("gable"))]))
    rules["lid_course"] = one(split("z", [(A(1), fill("roof_n")), (R(), fill("ceiling")),
                                          (A(1), fill("roof_s"))]))
    rules["gable"] = one(split("z", [(A(1), VOID), (R(), call("slope")), (A(1), VOID)]))
    rules["slope"] = [
        # the last course closes the ridge
        {"weight": 1, "when": {"cond": "all", "of": [cmp(D("y"), "eq", I(1)), cmp(D("z"), "ge", I(3))]},
         "body": split("z", [(A(1), fill("roof_n")), (R(), fill("ridge")), (A(1), fill("roof_s"))])},
        # the course under the ridge carries the gable lamp
        {"weight": 1, "when": {"cond": "all", "of": [cmp(D("y"), "eq", I(2)), cmp(D("z"), "ge", I(4))]},
         "body": split("y", [
             (A(1), {"op": "bind", "palette": {"gable_lamp": {"role": "lantern"}},
                     "body": call("course")}),
             (R(), call("slope_up"))])},
        {"weight": 1, "when": {"cond": "all", "of": [cmp(D("y"), "ge", I(3)), cmp(D("z"), "ge", I(4))]},
         "body": split("y", [(A(1), call("course")), (R(), call("slope_up"))])},
        {"weight": 1, "when": {"cond": "otherwise"}, "body": VOID},
    ]
    rules["slope_up"] = one(split("z", [(A(1), VOID), (R(), call("slope")), (A(1), VOID)]))
    rules["course"] = one(split("z", [(A(1), fill("roof_n")), (R(), call("gable_row")),
                                      (A(1), fill("roof_s"))]))
    rules["gable_row"] = one(split("x", [
        (EAVE, VOID), (RING, fill("infill")), (R(), VOID), (RING, fill("infill")),
        (EAVE, call("gable_out"))]))
    # under the east barge, hung from the ridge: the lamp in the gable
    rules["gable_out"] = one(split("z", [(R(), VOID), (A(2), fill("gable_lamp")), (R(), VOID)]))

    return {
        "version": "1.9.0",
        "name": "saltstair-a-harbourmaster",
        "start": "house",
        "params": params,
        "palette": palette,
        "shown_faces": ["east", "north", "south", "up", "west"],
        "contract": {
            "entry": "house",
            "spaces": {"house": {"envelope": "enclosed"}},
            "no_body": {"roof": {"reason": "the shingled roof and the attic under it, which no one is meant to walk"}},
            "no_body_majority_ack": "a house that owns its outside owns its roof, and a pitched roof is more standable surface than the room under it; nobody walks it",
            "edges": [{"a": "exterior", "b": "house", "class": "walk", "via": "east-door"}],
        },
        "rules": rules,
    }


def main():
    delvec, prefabs, campaign = sys.argv[1:4]
    prog = program(allocation(delvec, prefabs, campaign))
    out = Path(campaign) / "programs" / "harbourmaster.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(prog, indent=2, sort_keys=True) + "\n")
    print(out)


if __name__ == "__main__":
    main()
