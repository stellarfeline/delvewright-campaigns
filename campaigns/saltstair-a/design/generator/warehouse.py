#!/usr/bin/env python3
"""Emit programs/warehouse.json — the grammar program for node/warehouse.

Provenance only: the emitted JSON is the artifact of record. Every handed value
is read from `delvec allocation` and declared as a `handed/...` parameter; the
rules read those parameters and never a retyped number.

Usage: warehouse.py <delvec> <campaign-dir>
"""
import json
import subprocess
import sys
from pathlib import Path

PLACE = "node/warehouse"
SEAM = "edge/quay-warehouse"


def allocation(delvec, campaign):
    out = subprocess.run([delvec, "allocation", campaign, PLACE],
                         check=True, capture_output=True, text=True).stdout
    # The allocation is one JSON object followed by plain ground listings.
    obj, _ = json.JSONDecoder().raw_decode(out.lstrip())
    return obj


# ---- expression and node helpers ------------------------------------------
def P(name):
    return {"expr": "param", "name": name}


def I(v):
    return {"expr": "int", "value": v}


def sub(a, b):
    return {"expr": "arith", "op": "sub", "lhs": a, "rhs": b}


def add(a, b):
    return {"expr": "arith", "op": "add", "lhs": a, "rhs": b}


def ab(e):
    return {"size": "absolute", "blocks": I(e) if isinstance(e, int) else e}


def rel(w=1):
    return {"size": "relative", "weight": I(w)}


def split(axis, parts, repeat=False):
    node = {"op": "split", "axis": axis,
            "sizes": [s for s, _ in parts], "children": [c for _, c in parts]}
    if repeat:
        node["repeat"] = True
    return node


def fill(role):
    return {"op": "fill", "material": {"role": role}}


VOID = {"op": "void"}


def call(sym):
    return {"op": "call", "symbol": sym}


def claim(region, body):
    return {"op": "claim", "region": region, "body": body}


def along_x(body):
    """Hand the callee a frame whose local Z runs along world X."""
    return {"op": "reorient", "orient": {"x": "local_z", "z": "local_x"}, "body": body}


def one(body, when=None):
    alt = {"weight": 1, "body": body}
    if when is not None:
        alt["when"] = when
    return [alt]


def main():
    delvec, campaign = sys.argv[1], sys.argv[2]
    a = allocation(delvec, campaign)
    seam = next(s for s in a["seams"] if s["edge"] == SEAM)
    stem = SEAM.split("/", 1)[1]
    (sx0, sy0, sz0), (sx1, sy1, sz1) = seam["cells"]

    params = {
        "handed/datum-y": a["datum_y"],
        "handed/roof/eaves": a["roof"]["eaves"],
        "handed/roof/lid-y": a["roof"]["lid_y"],
        f"handed/seam/{stem}/x0": sx0,
        f"handed/seam/{stem}/x1": sx1,
        f"handed/seam/{stem}/y0": sy0,
        f"handed/seam/{stem}/y1": sy1,
    }
    datum = P("handed/datum-y")
    eaves = P("handed/roof/eaves")
    lid = P("handed/roof/lid-y")
    x0, x1 = P(f"handed/seam/{stem}/x0"), P(f"handed/seam/{stem}/x1")
    y0, y1 = P(f"handed/seam/{stem}/y0"), P(f"handed/seam/{stem}/y1")
    # x of the first cell inside the west ring wall, measured from the frame
    inner_x0 = add(eaves, I(1))
    door_w = add(sub(x1, x0), I(1))
    door_h = add(sub(y1, y0), I(1))

    stair = "minecraft:deepslate_tile_stairs[facing={},half=bottom,shape=straight,waterlogged=false]"
    palette = {
        "floor": [
            {"weight": 6, "block": "minecraft:cobblestone"},
            {"weight": 2, "block": "minecraft:stone"},
            {"weight": 1, "block": "minecraft:andesite"},
        ],
        "plinth": "minecraft:cobblestone",
        "wall": [
            {"weight": 8, "block": "minecraft:stone_bricks"},
            {"weight": 1, "block": "minecraft:cracked_stone_bricks"},
            {"weight": 1, "block": "minecraft:mossy_stone_bricks"},
        ],
        "post": "minecraft:spruce_log[axis=y]",
        "beam_x": "minecraft:spruce_log[axis=x]",
        "beam_z": "minecraft:spruce_log[axis=z]",
        "pane": {"local": "minecraft:glass_pane[east=false,north=true,south=true,waterlogged=false,west=false]"},
        "ceiling": "minecraft:spruce_planks",
        "infill": "minecraft:calcite",
        "stair_e": stair.format("east"),
        "stair_w": stair.format("west"),
        "ridge": "minecraft:deepslate_tiles",
        "kelp": "minecraft:dried_kelp_block",
        "cargo_logs": "minecraft:spruce_log[axis=z]",
        "lamp": "minecraft:lantern[hanging=true,waterlogged=false]",
    }

    rules = {
        # floor course, the storey up to the lid, the roof zone above it
        "warehouse": one(split("y", [
            (ab(datum), fill("floor")),
            (ab(sub(lid, datum)), call("storey")),
            (rel(), call("roof")),
        ])),
        "storey": one(split("x", [
            (ab(eaves), VOID),
            (ab(1), call("side_col")),
            (rel(), call("middle")),
            (ab(1), call("side_col")),
            (ab(eaves), VOID),
        ])),
        # a long side wall: corner posts at both ends, the run between
        "side_col": one(split("z", [
            (ab(eaves), VOID),
            (ab(1), fill("post")),
            (rel(), call("side_run")),
            (ab(1), fill("post")),
            (ab(eaves), VOID),
        ])),
        # cobblestone plinth, stone, a window band, a top course
        "side_run": one(split("y", [
            (ab(1), fill("plinth")),
            (rel(), fill("wall")),
            (ab(2), call("window_band")),
            (ab(1), fill("wall")),
        ])),
        "window_band": one(split("z", [
            (ab(2), fill("wall")),
            (ab(1), fill("pane")),
        ], repeat=True)),
        "middle": one(split("z", [
            (ab(eaves), VOID),
            (ab(1), along_x(call("side_run"))),
            (rel(), call("hall")),
            (ab(1), call("south_wall")),
            (ab(eaves), VOID),
        ])),
        # the quay front: wall, the handed door, wall
        "south_wall": one(split("x", [
            (ab(sub(x0, inner_x0)), along_x(call("side_run"))),
            (ab(door_w), call("door_col")),
            (rel(), along_x(call("side_run"))),
        ])),
        "door_col": [
            {"weight": 1,
             "when": {"cond": "cmp", "op": "eq", "lhs": sub(y0, datum), "rhs": I(0)},
             "body": split("y", [
                 (ab(door_h), claim("quay-door", VOID)),
                 (rel(), call("over_door")),
             ])},
            {"weight": 1, "when": {"cond": "otherwise"},
             "body": split("y", [
                 (ab(sub(y0, datum)), fill("wall")),
                 (ab(door_h), claim("quay-door", VOID)),
                 (rel(), call("over_door")),
             ])},
        ],
        "over_door": one(split("y", [
            (ab(1), fill("beam_x")),
            (rel(), fill("wall")),
        ])),
        # the store: cargo along the walls at the floor, lanterns under the ceiling
        "hall": one(claim("hall", {
            "op": "mark",
            "mark": {"anchor": "node-warehouse", "at": "floor_center", "facing": "south"},
            "body": split("y", [
                (ab(1), call("cargo")),
                (rel(), VOID),
                (ab(1), call("lamps")),
            ]),
        })),
        "cargo": one(split("x", [
            (ab(1), call("cargo_west")),
            (rel(), VOID),
            (ab(1), call("cargo_east")),
        ])),
        "cargo_west": one(split("z", [
            (ab(1), VOID), (ab(3), fill("kelp")), (ab(2), VOID),
            (ab(2), fill("cargo_logs")), (rel(), VOID),
        ])),
        "cargo_east": one(split("z", [
            (ab(1), VOID), (ab(2), fill("cargo_logs")), (ab(2), VOID),
            (ab(3), fill("kelp")), (rel(), VOID),
        ])),
        "lamps": one(split("z", [
            (ab(2), VOID),
            (ab(1), split("x", [(ab(2), VOID), (ab(1), fill("lamp")), (rel(), VOID)])),
            (ab(1), split("x", [(ab(7), VOID), (ab(1), fill("lamp")), (rel(), VOID)])),
            (ab(4), VOID),
            (ab(1), split("x", [(ab(1), VOID), (ab(1), fill("lamp")), (ab(5), VOID),
                                (ab(1), fill("lamp")), (rel(), VOID)])),
            (rel(), VOID),
            # the lantern at the door, just inside it
            (ab(1), split("x", [(ab(sub(x0, inner_x0)), VOID), (ab(1), fill("lamp")),
                                (rel(), VOID)])),
        ])),
        # roof zone: lid course (eaves, wall plate, ceiling), then the gable
        "roof": one(claim("roof", split("y", [
            (ab(1), call("lid")),
            (rel(), call("upper")),
        ]))),
        "lid": one(split("x", [
            (ab(eaves), fill("stair_e")),
            (rel(), call("lid_mid")),
            (ab(eaves), fill("stair_w")),
        ])),
        "lid_mid": one(split("z", [
            (ab(eaves), VOID),
            (ab(1), fill("beam_x")),
            (rel(), call("lid_inner")),
            (ab(1), fill("beam_x")),
            (ab(eaves), VOID),
        ])),
        "lid_inner": one(split("x", [
            (ab(1), fill("beam_z")),
            (rel(), fill("ceiling")),
            (ab(1), fill("beam_z")),
        ])),
        "upper": one(split("x", [
            (ab(eaves), VOID),
            (rel(), call("slope")),
            (ab(eaves), VOID),
        ])),
        # 45-degree gable: one stair course per level, stepping in one a side
        "slope": [
            {"weight": 1,
             "when": {"cond": "cmp", "op": "ge", "lhs": {"expr": "dim", "dim": "y"}, "rhs": I(2)},
             "body": split("y", [
                 (ab(1), call("course_gable")),
                 (rel(), split("x", [(ab(1), VOID), (rel(), call("slope")), (ab(1), VOID)])),
             ])},
            {"weight": 1, "when": {"cond": "otherwise"}, "body": call("course_ridge")},
        ],
        "course_gable": one(split("x", [
            (ab(1), fill("stair_e")),
            (rel(), call("gable_row")),
            (ab(1), fill("stair_w")),
        ])),
        "course_ridge": one(split("x", [
            (ab(1), fill("stair_e")),
            (rel(), fill("ridge")),
            (ab(1), fill("stair_w")),
        ])),
        "gable_row": one(split("z", [
            (ab(eaves), VOID),
            (ab(1), call("gable_wall")),
            (rel(), VOID),
            (ab(1), call("gable_wall")),
            (ab(eaves), VOID),
        ])),
        # white infill either side of a spruce king post
        "gable_wall": one(split("x", [
            (rel(), fill("infill")),
            (ab(2), fill("post")),
            (rel(), fill("infill")),
        ])),
    }

    program = {
        "version": "1.9.0",
        "name": "saltstair-a-warehouse",
        "start": "warehouse",
        "params": params,
        "palette": palette,
        "rules": rules,
        "contract": {
            "entry": "hall",
            "spaces": {"hall": {"envelope": "enclosed"}},
            "no_body": {"roof": {"reason": "the slate roof and the loft under it, which no one is meant to walk"}},
            "no_body_majority_ack": "a house that draws its own roof carries more standable roof and loft than store floor; nobody walks them",
            "edges": [{"a": "exterior", "b": "hall", "class": "walk", "via": "quay-door"}],
        },
        "shown_faces": ["east", "north", "south", "up", "west"],
    }
    out = Path(campaign) / "programs" / "warehouse.json"
    out.write_text(json.dumps(program, indent=2) + "\n")
    print(out)


if __name__ == "__main__":
    main()
