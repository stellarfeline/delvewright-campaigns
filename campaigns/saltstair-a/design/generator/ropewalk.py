#!/usr/bin/env python3
"""Emit programs/ropewalk.json — the rope walk of Saltstair.

Provenance only: the emitted JSON is the artifact of record. Every number the
whole hands is read through a `handed/...` parameter; the defaults are filled
from `delvec allocation` at emit time, never typed here.
"""
import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
CAMPAIGN = HERE.parent.parent
DELVEC = pathlib.Path.home() / ".delvewright/bin/delvec"
SEAM = "lower-street-ropewalk"


def allocation():
    out = subprocess.run(
        [str(DELVEC), "allocation", str(CAMPAIGN), "node/ropewalk"],
        check=True, capture_output=True, text=True).stdout
    start = out.index("{")
    return json.JSONDecoder().raw_decode(out[start:])[0]


# --- expression helpers -----------------------------------------------------
def I(n): return {"expr": "int", "value": n}
def P(n): return {"expr": "param", "name": n}
def D(axis): return {"expr": "dim", "dim": axis}
def ar(a, op, b): return {"expr": "arith", "lhs": a, "op": op, "rhs": b}
def add(a, b): return ar(a, "add", b)
def sub(a, b): return ar(a, "sub", b)
def S(name): return P(f"handed/seam/{SEAM}/{name}")
def span(lo, hi): return add(sub(hi, lo), I(1))   # inclusive count


def A(e): return {"size": "absolute", "blocks": e if isinstance(e, dict) else I(e)}
def R(w=1): return {"size": "relative", "weight": I(w)}


def split(axis, sizes, children, repeat=False):
    n = {"op": "split", "axis": axis, "sizes": sizes, "children": children}
    if repeat:
        n["repeat"] = True
    return n


def fill(role): return {"op": "fill", "material": {"role": role}}
VOID = {"op": "void"}
def call(s): return {"op": "call", "symbol": s}
def claim(region, body): return {"op": "claim", "region": region, "body": body}
def alt(body, when=None):
    a = {"weight": 1, "body": body}
    if when is not None:
        a["when"] = when
    return a
def cmp(lhs, op, rhs): return {"cond": "cmp", "lhs": lhs, "op": op, "rhs": rhs}
def all_(*c): return {"cond": "all", "of": list(c)}
OTHERWISE = {"cond": "otherwise"}
# turn a wall run laid along local z so that it runs along world x
TURN = {"x": "local_z", "z": "local_x"}


def program(alloc):
    eaves = P("handed/roof/eaves")
    datum = P("handed/datum-y")
    rules = {
        # y: floor course | storey up to the lid | roof
        "ropewalk": [alt(split("y", [A(datum), A(sub(P("handed/roof/lid-y"), datum)), R()],
                               [call("floor"), call("storey"), call("roof")]))],
        # the floor course stops at the eaves: nothing outside the walls is this house's
        "floor": [alt(split("x", [A(S("x0")), R(), A(eaves)],
                            [VOID, split("z", [A(eaves), R(), A(eaves)], [VOID, fill("floor"), VOID]), VOID]))],
        # x: west eave | west wall (the seam's plane) | middle | east wall | east eave
        "storey": [alt(split("x", [A(S("x0")), A(1), R(), A(1), A(eaves)],
                             [VOID, call("west_wall"), call("middle"), call("east_wall"), VOID]))],
        "west_wall": [alt(split("z",
            [A(eaves), A(1), A(sub(sub(S("z0"), eaves), I(1))), A(span(S("z0"), S("z1"))),
             R(), A(1), A(eaves)],
            [VOID, fill("post"), call("wall_run"), call("door"), call("wall_run"),
             fill("post"), VOID]))],
        "door": [alt(split("y", [A(sub(S("y0"), datum)), A(span(S("y0"), S("y1"))), R()],
                           [fill("plinth"), claim("west-door", VOID), fill("beam")]))],
        "east_wall": [alt(split("z", [A(eaves), A(1), R(), A(1), A(eaves)],
                                [VOID, fill("post"), call("wall_run"), fill("post"), VOID]))],
        # z: south eave | north gable wall | hall | south gable wall | eave
        "middle": [alt(split("z", [A(eaves), A(1), R(), A(1), A(eaves)],
            [VOID,
             {"op": "reorient", "orient": TURN, "body": call("end_run")},
             claim("hall", {"op": "mark",
                            "mark": {"anchor": "node-ropewalk", "at": "offset", "facing": "west",
                                     "x": ar(D("x"), "div", I(2)), "y": I(0),
                                     "z": ar(D("z"), "div", I(2))},
                            "body": call("hall")}),
             {"op": "reorient", "orient": TURN, "body": call("end_run")},
             VOID]))],
        # a wall run along local z: stone plinth | framed band | spruce wall plate
        "wall_run": [alt(split("y", [A(1), R(), A(1)],
                               [fill("plinth"), call("band"), fill("beam")]))],
        "end_run": [alt(split("y", [A(1), R(), A(1)],
                              [fill("plinth"), call("end_band"), fill("beam")]))],
        # post | infill | window | infill, repeated from the run's start
        "band": [
            alt(split("z", [A(1), A(1), A(1), A(1)],
                      [fill("post"), fill("infill"), fill("pane"), fill("infill")], repeat=True),
                cmp(D("z"), "ge", I(4))),
            alt(fill("infill"), OTHERWISE),
        ],
        # a gable end: infill | post | window | post | infill, centred
        "end_band": [
            alt(split("z", [R(), A(1), A(1), A(1), R()],
                      [fill("infill"), fill("post"), fill("pane"), fill("post"), fill("infill")]),
                cmp(D("z"), "ge", I(5))),
            alt(fill("infill"), OTHERWISE),
        ],
        # the walk: rope lines either side of the middle, a lantern over the door,
        # tar and hemp along the east wall
        "hall": [alt(split("x", [A(1), R(), A(1), A(1), A(1), R(), A(1)],
                           [call("door_side"), VOID, call("rope_line"), call("mid_line"),
                            call("rope_line"), VOID, call("east_side")]))],
        "door_side": [alt(split("z",
            [A(sub(sub(S("z0"), eaves), I(1))), A(span(S("z0"), S("z1"))), R()],
            [VOID, call("lamp_col"), VOID]))],
        "lamp_col": [alt(split("y", [R(), A(1)], [VOID, fill("lamp")]))],
        "rope_line": [alt(split("z", [A(1), R(), A(1)],
                                [call("jack"), call("rope_span"), call("jack")]))],
        "jack": [alt(split("y", [A(2), A(1), R()], [fill("jack"), fill("rope"), VOID]))],
        "rope_span": [alt(split("y", [A(2), A(1), R()], [VOID, fill("rope"), VOID]))],
        "mid_line": [alt(split("z", [R(1), A(1), R(2), A(1), R(1)],
                               [VOID, call("lamp_col"), VOID, call("lamp_col"), VOID]))],
        "east_side": [alt(split("z", [A(1), A(1), R(), A(2), A(1), A(1)],
                                [VOID, call("tar_col"), VOID, call("hemp_col"),
                                 call("lamp_col"), VOID]))],
        "tar_col": [alt(split("y", [A(1), R()], [fill("tar"), VOID]))],
        "hemp_col": [alt(split("y", [A(1), R()], [fill("hemp"), VOID]))],
        # roof: lid course, then a 45-degree gable of dark oak stairs
        "roof": [alt(claim("roof", split("y", [A(1), R()], [call("lid_course"), call("gable")])))],
        "lid_course": [alt(split("x", [A(1), R(), A(1)],
                                 [fill("roof_e"), fill("ceiling"), fill("roof_w")]))],
        "gable": [alt(split("x", [A(1), R(), A(1)], [VOID, call("slope"), VOID]))],
        "slope": [
            alt(split("x", [A(1), R(), A(1)], [fill("roof_e"), fill("ridge"), fill("roof_w")]),
                all_(cmp(D("x"), "ge", I(3)), cmp(D("y"), "eq", I(1)))),
            alt(split("y", [A(1), R()], [call("course"), call("slope_up")]),
                all_(cmp(D("x"), "ge", I(3)), cmp(D("y"), "ge", I(2)))),
            alt(split("y", [A(1), R()], [fill("ridge"), VOID]),
                all_(cmp(D("x"), "ge", I(1)), cmp(D("x"), "le", I(2)), cmp(D("y"), "ge", I(1)))),
            alt(VOID, OTHERWISE),
        ],
        "slope_up": [alt(split("x", [A(1), R(), A(1)], [VOID, call("slope"), VOID]))],
        "course": [alt(split("x", [A(1), R(), A(1)],
                             [fill("roof_e"), call("gable_row"), fill("roof_w")]))],
        "gable_row": [alt(split("z", [A(eaves), A(1), R(), A(1), A(eaves)],
                                [VOID, fill("infill"), VOID, fill("infill"), VOID]))],
    }

    seam = next(s for s in alloc["seams"] if s["edge"] == f"edge/{SEAM}")
    (x0, y0, z0), (x1, y1, z1) = seam["cells"]
    params = {
        "handed/datum-y": alloc["datum_y"],
        "handed/roof/eaves": alloc["roof"]["eaves"],
        "handed/roof/lid-y": alloc["roof"]["lid_y"],
        f"handed/seam/{SEAM}/x0": x0,
        f"handed/seam/{SEAM}/y0": y0,
        f"handed/seam/{SEAM}/y1": y1,
        f"handed/seam/{SEAM}/z0": z0,
        f"handed/seam/{SEAM}/z1": z1,
    }
    palette = {
        "floor": "minecraft:cobblestone",
        "plinth": "minecraft:stone_bricks",
        "infill": "minecraft:calcite",
        "post": "minecraft:spruce_log[axis=y]",
        "beam": {"local": "minecraft:spruce_log[axis=z]"},
        "pane": {"local": "minecraft:glass_pane[east=false,north=true,south=true,waterlogged=false,west=false]"},
        "ceiling": "minecraft:spruce_planks",
        "roof_e": {"local": "minecraft:dark_oak_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]"},
        "roof_w": {"local": "minecraft:dark_oak_stairs[facing=west,half=bottom,shape=straight,waterlogged=false]"},
        "ridge": "minecraft:dark_oak_slab[type=bottom,waterlogged=false]",
        "lamp": "minecraft:lantern[hanging=true,waterlogged=false]",
        "jack": "minecraft:spruce_fence[east=false,north=false,south=false,waterlogged=false,west=false]",
        "rope": {"local": "minecraft:iron_chain[axis=z,waterlogged=false]"},
        "tar": "minecraft:cauldron",
        "hemp": "minecraft:hay_block[axis=y]",
    }
    contract = {
        "entry": "hall",
        "spaces": {"hall": {"envelope": "enclosed"}},
        "no_body": {"roof": {"reason": "the shingled roof and the loft under it, which no one is meant to walk"}},
        "edges": [{"a": "exterior", "b": "hall", "class": "walk", "via": "west-door"}],
        "no_body_majority_ack": "a house that owns its outside owns its roof, and a pitched roof is more standable surface than the long room under it; nobody walks it",
    }
    return {
        "version": "1.12.0",
        "name": "saltstair-a-ropewalk",
        "start": "ropewalk",
        "params": params,
        "palette": palette,
        "rules": rules,
        "contract": contract,
        "shown_faces": ["north", "south", "east", "west", "up"],
    }


def main():
    out = CAMPAIGN / "programs" / "ropewalk.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(program(allocation()), indent=2, sort_keys=True) + "\n")
    print(out)


if __name__ == "__main__":
    sys.exit(main())
