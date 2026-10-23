#!/usr/bin/env python3
"""Emit programs/weaver.json — the weaver's house of Saltstair.

Provenance only: the emitted JSON is the artifact of record. Every handed
value is read through a `handed/...` parameter; nothing here retypes one.
"""
import json
import pathlib

SEAM = "handed/seam/upper-street-weaver"


def I(v):
    return {"expr": "int", "value": v}


def P(n):
    return {"expr": "param", "name": n}


def sub(a, b):
    return {"expr": "arith", "op": "sub", "lhs": a, "rhs": b}


def add(a, b):
    return {"expr": "arith", "op": "add", "lhs": a, "rhs": b}


def A(e):
    return {"size": "absolute", "blocks": I(e) if isinstance(e, int) else e}


def R(w=1):
    return {"size": "relative", "weight": I(w)}


def split(axis, pieces, repeat=False, rounding=None):
    node = {"op": "split", "axis": axis,
            "sizes": [s for s, _ in pieces],
            "children": [c for _, c in pieces]}
    if repeat:
        node["repeat"] = True
    if rounding:
        node["rounding"] = rounding
    return node


def fill(role):
    return {"op": "fill", "material": {"role": role}}


VOID = {"op": "void"}


def call(sym):
    return {"op": "call", "symbol": sym}


def claim(region, body):
    return {"op": "claim", "region": region, "body": body}


def swap_xz(body):
    return {"op": "reorient", "orient": {"x": "local_z", "z": "local_x"}, "body": body}


def mirror_z(body):
    return {"op": "reorient", "orient": {"mirror": {"z": True}}, "body": body}


def cmp(dim, op, v):
    return {"cond": "cmp", "lhs": {"expr": "dim", "dim": dim}, "op": op, "rhs": I(v)}


def one(body):
    return [{"weight": 1, "body": body}]


EAVES = P("handed/roof/eaves")
DATUM = P("handed/datum-y")
LID = P("handed/roof/lid-y")


def column(*courses):
    """A one-cell column: absolute courses from the floor, the rest void."""
    return split("y", [(A(1), fill(r)) for r in courses] + [(R(), VOID)])


rules = {
    # floor course, the storey up to the lid, the roof above it
    "house": one(split("y", [
        (A(DATUM), call("floor_course")),
        (A(sub(LID, DATUM)), call("storey")),
        (R(), claim("roof", call("roof"))),
    ])),
    # the cobbled floor under the house and its walls; the eaves' ring is not ours
    "floor_course": one(split("x", [
        (A(EAVES), VOID),
        (R(), split("z", [(A(EAVES), VOID), (R(), fill("floor")), (A(EAVES), VOID)])),
        (A(EAVES), VOID),
    ])),
    "storey": one(split("x", [
        (A(EAVES), VOID),
        (A(1), call("west_wall")),
        (R(), call("middle")),
        (A(1), call("east_wall")),
        (A(EAVES), VOID),
    ])),
    # ---- walls: stone-brick lower band, spruce posts with calcite above ----
    "panel": one(split("y", [(A(2), fill("stone")), (R(), fill("infill"))])),
    "post": one(split("y", [(A(2), fill("stone")), (R(), fill("post"))])),
    "window_col": one(split("y", [(A(1), fill("stone")), (A(2), fill("pane")),
                                  (R(), fill("infill"))])),
    "door_post": one(split("y", [(A(2), fill("stone")), (A(1), fill("lamp_stand")),
                                 (R(), fill("post"))])),
    "panel_window": one(split("z", [(A(1), call("panel")), (R(), call("window_col")),
                                    (A(1), call("panel"))])),
    "run_lit": one(split("z", [(A(3), call("panel_window")), (A(1), call("post"))],
                         repeat=True)),
    "run_plain": one(split("z", [(A(3), call("panel")), (A(1), call("post"))],
                           repeat=True)),
    # half of the street front, from the corner to the post beside the door
    "door_run": one(split("z", [(R(), call("panel")), (A(1), call("window_col")),
                                (R(), call("panel")), (A(1), call("door_post"))],
                          rounding="start")),
    "door": one(split("y", [
        (A(sub(P(SEAM + "/y0"), DATUM)), fill("stone")),
        (A(add(sub(P(SEAM + "/y1"), P(SEAM + "/y0")), I(1))),
         claim("upper-street-door", VOID)),
        (A(1), fill("lintel")),
        (R(), fill("infill")),
    ])),
    "west_wall": one(split("z", [
        (A(EAVES), VOID),
        (A(1), call("post")),
        (A(sub(P(SEAM + "/z0"), add(EAVES, I(1)))), call("door_run")),
        (A(add(sub(P(SEAM + "/z1"), P(SEAM + "/z0")), I(1))), call("door")),
        (R(), mirror_z(call("door_run"))),
        (A(1), call("post")),
        (A(EAVES), VOID),
    ])),
    "east_wall": one(split("z", [
        (A(EAVES), VOID),
        (A(1), call("post")),
        (R(), call("run_lit")),
        (A(1), call("post")),
        (A(EAVES), VOID),
    ])),
    "middle": one(split("z", [
        (A(EAVES), VOID),
        (A(1), swap_xz(call("run_plain"))),
        (R(), claim("hall", call("hall"))),
        (A(1), swap_xz(call("run_lit"))),
        (A(EAVES), VOID),
    ])),
    # ---- the room: looms and cloth at the north end, vat and bench south ----
    "hall": one(split("z", [
        (A(1), call("workrow")),
        (A(1), call("row2")),
        (R(), {"op": "mark",
               "mark": {"anchor": "node-weaver", "at": "offset", "facing": "east",
                        "x": I(2), "y": I(0), "z": I(3)},
               "body": call("open")}),
        (A(1), VOID),
        (A(1), call("southrow")),
    ])),
    "workrow": one(split("x", [
        (A(2), VOID), (A(1), column("loom")), (A(1), VOID), (A(1), column("loom")),
        (R(), VOID), (A(1), column("cloth_1", "cloth_2", "cloth_1")),
    ])),
    "row2": one(split("x", [(R(), VOID), (A(1), column("cloth_2", "cloth_3", "cloth_2"))])),
    "southrow": one(split("x", [
        (A(2), VOID), (A(1), column("vat")), (R(), VOID),
        (A(1), split("y", [(A(1), fill("bench")), (R(), VOID), (A(1), fill("lamp"))])),
        (A(1), column("cloth_3", "cloth_1", "cloth_3")),
    ])),
    "open": one(split("y", [(R(), VOID), (A(1), call("lamps"))])),
    "lamps": one(split("z", [
        (A(1), split("x", [(A(1), VOID), (A(1), fill("lamp")), (R(), VOID)])),
        (A(2), VOID),
        (A(1), split("x", [(R(), VOID), (A(1), fill("lamp")), (A(1), VOID)])),
        (A(2), VOID),
        (A(1), split("x", [(A(2), VOID), (A(1), fill("lamp")), (R(), VOID)])),
        (R(), VOID),
    ])),
    # ---- roof: lid with eaves, then 45-degree dark oak courses to a ridge ----
    "roof": one(split("y", [(A(1), call("lid_course")), (R(), call("gable_zone"))])),
    "lid_course": one(split("x", [(A(EAVES), fill("roof_e")), (R(), fill("lid")),
                                  (A(EAVES), fill("roof_w"))])),
    "gable_zone": one(split("x", [(A(EAVES), VOID), (R(), call("slope_first")),
                                  (A(EAVES), VOID)])),
    # the lowest course carries the bolts of cloth laid on the loft floor
    "slope_first": one(split("y", [
        (A(1), {"op": "bind", "palette": {"loft": {"role": "bolts"}}, "body": call("course")}),
        (R(), call("slope_up")),
    ])),
    "slope": [
        {"weight": 1,
         "when": {"cond": "all", "of": [cmp("x", "ge", 3), cmp("y", "ge", 1)]},
         "body": split("y", [(A(1), call("course")), (R(), call("slope_up"))])},
        {"weight": 1,
         "when": {"cond": "all", "of": [cmp("x", "eq", 1), cmp("y", "ge", 1)]},
         "body": split("y", [(A(1), fill("ridge")), (R(), VOID)])},
        {"weight": 1, "when": {"cond": "otherwise"}, "body": VOID},
    ],
    "slope_up": [
        {"weight": 1, "when": cmp("x", "ge", 3),
         "body": split("x", [(A(1), VOID), (R(), call("slope")), (A(1), VOID)])},
        {"weight": 1, "when": {"cond": "otherwise"}, "body": VOID},
    ],
    "course": one(split("x", [(A(1), fill("roof_e")), (R(), call("inner_row")),
                              (A(1), fill("roof_w"))])),
    "inner_row": one(split("z", [
        (A(EAVES), VOID),
        (A(1), call("gable_row")),
        (R(), fill("loft")),
        (A(1), call("gable_row")),
        (A(EAVES), VOID),
    ])),
    "gable_row": one(split("x", [(R(), fill("infill")), (A(1), fill("post")),
                                 (R(), fill("infill"))])),
}

program = {
    "version": "1.9.0",
    "name": "saltstair-a-weaver",
    "start": "house",
    "params": {
        "handed/datum-y": 1,
        "handed/roof/lid-y": 5,
        "handed/roof/eaves": 1,
        SEAM + "/y0": 1,
        SEAM + "/y1": 2,
        SEAM + "/z0": 7,
        SEAM + "/z1": 7,
    },
    "palette": {
        "floor": "minecraft:cobblestone",
        "stone": "minecraft:stone_bricks",
        "infill": "minecraft:calcite",
        "post": {"local": "minecraft:spruce_log[axis=y]"},
        "lintel": {"local": "minecraft:stripped_spruce_log[axis=z]"},
        "pane": {"local": "minecraft:glass_pane[east=false,north=true,south=true,waterlogged=false,west=false]"},
        "lid": "minecraft:spruce_planks",
        "roof_e": {"local": "minecraft:dark_oak_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]"},
        "roof_w": {"local": "minecraft:dark_oak_stairs[facing=west,half=bottom,shape=straight,waterlogged=false]"},
        "ridge": "minecraft:dark_oak_slab[type=bottom,waterlogged=false]",
        "lamp": "minecraft:lantern[hanging=true,waterlogged=false]",
        "lamp_stand": "minecraft:lantern[hanging=false,waterlogged=false]",
        "loom": {"local": "minecraft:loom[facing=south]"},
        "cloth_1": "minecraft:white_wool",
        "cloth_2": "minecraft:light_blue_wool",
        "cloth_3": "minecraft:light_gray_wool",
        "bolts": [
            {"weight": 2, "block": "minecraft:white_wool"},
            {"weight": 1, "block": "minecraft:light_blue_wool"},
            {"weight": 1, "block": "minecraft:light_gray_wool"},
            {"weight": 4, "block": "minecraft:air"},
        ],
        "loft": "minecraft:air",
        "bench": "minecraft:crafting_table",
        "vat": "minecraft:water_cauldron[level=3]",
    },
    "contract": {
        "entry": "hall",
        "spaces": {"hall": {"envelope": "enclosed"}},
        "no_body": {"roof": {"reason": "the roof and the cloth loft under it, which no one is meant to walk"}},
        "no_body_majority_ack": "a house that owns its outside owns its roof, and a pitched roof over a cloth loft is more standable surface than the room under it; nobody walks it",
        "edges": [{"a": "exterior", "b": "hall", "class": "walk", "via": "upper-street-door"}],
    },
    "shown_faces": ["east", "north", "south", "up"],
    "rules": rules,
}

out = pathlib.Path(__file__).resolve().parents[2] / "programs" / "weaver.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(program, indent=2, sort_keys=True) + "\n")
print(out)
