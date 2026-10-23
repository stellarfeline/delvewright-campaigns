#!/usr/bin/env python3
"""Emit programs/middle-street.json — the middle street of Saltstair.

Provenance only: the emitted program is the artifact of record. Every handed
number is read from `delvec allocation` and becomes a `handed/...` parameter
default; the rules read those parameters, never a copied literal.

Usage: middle-street.py <delvec> <campaign-dir>
"""
import json
import subprocess
import sys
from pathlib import Path

PLACE = "node/middle-street"
NORTH = "flight-2-middle-street"   # walk on the north face, plane not ours
SOUTH = "middle-street-flight-3"   # stair on the south face, plane ours
WEST = "middle-street-merchant"    # the merchant's east door, plane not ours


def allocation(delvec, campaign):
    out = subprocess.run([delvec, "allocation", campaign, PLACE],
                         check=True, capture_output=True, text=True).stdout
    obj, _ = json.JSONDecoder().raw_decode(out.lstrip())
    return obj


# ---- expression and node helpers -------------------------------------------
def I(v):
    return {"expr": "int", "value": v}


def P(name):
    return {"expr": "param", "name": "handed/" + name}


def sub(a, b):
    return {"expr": "arith", "op": "sub", "lhs": a, "rhs": b}


def add(a, b):
    return {"expr": "arith", "op": "add", "lhs": a, "rhs": b}


def div(a, b):
    return {"expr": "arith", "op": "div", "lhs": a, "rhs": b}


def span(seam, axis):
    """Inclusive cell count of a seam's opening along one axis."""
    return add(sub(P(f"seam/{seam}/{axis}1"), P(f"seam/{seam}/{axis}0")), I(1))


def A(e):
    return {"size": "absolute", "blocks": e if isinstance(e, dict) else I(e)}


R = {"size": "relative", "weight": I(1)}


def split(axis, sizes, children):
    return {"op": "split", "axis": axis, "sizes": sizes, "children": children}


def call(s):
    return {"op": "call", "symbol": s}


def fill(role):
    return {"op": "fill", "material": {"role": role}}


def claim(region, body):
    return {"op": "claim", "region": region, "body": body}


VOID = {"op": "void"}
SKIP = {"op": "skip"}


def rule(body):
    return [{"weight": 1, "body": body}]


def main():
    delvec, campaign = sys.argv[1], sys.argv[2]
    a = allocation(delvec, campaign)

    params = {"handed/datum-y": a["datum_y"],
              "handed/ground/bottom-y": a["ground"]["bottom_y"]}
    for s in a["seams"]:
        stem = s["edge"].removeprefix("edge/")
        (x0, y0, z0), (x1, y1, z1) = s["cells"]
        for k, v in zip(("x0", "y0", "z0", "x1", "y1", "z1"),
                        (x0, y0, z0, x1, y1, z1)):
            params[f"handed/seam/{stem}/{k}"] = v

    # The street's west edge is the north seam's x0 (first layer beside the
    # merchant's wall); its width is that seam's span. The street's south end
    # is the south seam's plane.
    street_x0 = P(f"seam/{NORTH}/x0")
    street_w = span(NORTH, "x")
    south_z = P(f"seam/{SOUTH}/z0")
    ground = sub(P("datum-y"), P("ground/bottom-y"))

    rules = {
        "place": rule({
            "op": "mark",
            "mark": {"anchor": "node-middle-street", "at": "offset",
                     "facing": "south",
                     "x": add(street_x0, div(sub(street_w, I(1)), I(2))),
                     "y": P("datum-y"),
                     "z": div(south_z, I(2))},
            "body": split("y", [A(P("ground/bottom-y")), A(ground), R],
                          [SKIP, call("ground-course"), call("above")])}),

        # ---- the floor course: paving between two kerbs --------------------
        "ground-course": rule(split(
            "x", [A(street_x0), A(street_w), R],
            [SKIP, call("street-floor"), SKIP])),
        "street-floor": rule(split(
            "z", [A(south_z), R], [call("paving-band"), SKIP])),
        "paving-band": rule(split(
            "x", [A(1), R, A(1)],
            [fill("kerb"), fill("paving"), fill("kerb")])),

        # ---- above the floor ------------------------------------------------
        "above": rule(split(
            "z", [A(south_z), R], [call("body"), call("south-wall")])),
        "body": rule(split(
            "x", [A(street_x0), A(street_w), R],
            [SKIP, call("street-air"), call("east-kerb")])),

        # the north seam: the whole face at the first layer
        "street-air": rule(split(
            "z", [A(P(f"seam/{NORTH}/z0")), A(span(NORTH, "z")), R],
            [SKIP, claim("seam-" + NORTH, VOID), call("street-rest")])),
        # the merchant's door: the first layer beside its wall
        "street-rest": rule(split(
            "x", [A(span(WEST, "x")), R],
            [call("west-lane"), claim("street", VOID)])),
        "west-lane": rule(split(
            "z",
            [A(sub(P(f"seam/{WEST}/z0"),
                   add(P(f"seam/{NORTH}/z1"), I(1)))),
             A(span(WEST, "z")), R],
            [claim("street", VOID), call("door-column"),
             claim("street", VOID)])),
        "door-column": rule(split(
            "y", [A(sub(P(f"seam/{WEST}/y0"), P("datum-y"))),
                  A(span(WEST, "y")), R],
            [claim("street", VOID), claim("seam-" + WEST, VOID),
             claim("street", VOID)])),

        # the east kerb: a parapet on the hillside ring, posts at the flight
        # foot and opposite the merchant's door
        "east-kerb": rule(split(
            "z",
            [A(P(f"seam/{NORTH}/z0")), A(span(NORTH, "z")),
             A(sub(P(f"seam/{WEST}/z0"),
                   add(P(f"seam/{NORTH}/z1"), I(1)))),
             A(span(WEST, "z")), R],
            [SKIP, call("post"), call("parapet"), call("post"),
             call("parapet")])),
        "parapet": rule(split("y", [A(1), R], [fill("parapet"), VOID])),
        "post": rule(split(
            "y", [A(1), A(1), A(1), A(1), R],
            [fill("post-foot"), fill("post"), fill("lamp"),
             claim("lamp-top", VOID), VOID])),

        # ---- the south wall: ours; the flight's opening cut in it ----------
        "south-wall": rule(split(
            "x", [A(P(f"seam/{SOUTH}/x0")), A(span(SOUTH, "x")), R],
            [call("post"), call("flight-mouth"), call("post")])),
        "flight-mouth": rule(split(
            "y", [A(sub(P(f"seam/{SOUTH}/y0"), P("datum-y"))),
                  A(span(SOUTH, "y")), R],
            [VOID, claim("seam-" + SOUTH, VOID), VOID])),
    }

    program = {
        "version": "1.9.0",
        "name": "saltstair-a-middle-street",
        "start": "place",
        "params": params,
        "palette": {
            "paving": [
                {"weight": 6, "block": "minecraft:cobblestone"},
                {"weight": 1, "block": "minecraft:mossy_cobblestone"},
                {"weight": 1, "block": "minecraft:andesite"},
            ],
            "kerb": "minecraft:stone_bricks",
            "post-foot": "minecraft:mossy_stone_bricks",
            "post": "minecraft:stone_bricks",
            "parapet": "minecraft:stone_brick_wall[east=none,north=low,"
                       "south=low,up=false,waterlogged=false,west=none]",
            "lamp": "minecraft:lantern[hanging=false,waterlogged=false]",
        },
        "rules": rules,
        "contract": {
            "entry": "street",
            "spaces": {"street": {"envelope": "open"}},
            "no_body": {"lamp-top": {
                "reason": "the air over a lantern on a kerb post; "
                          "nobody climbs a lamp to stand on it"}},
            "edges": [
                {"a": "street", "b": "exterior", "class": "walk",
                 "via": "seam-" + NORTH},
                {"a": "street", "b": "exterior", "class": "walk",
                 "via": "seam-" + SOUTH},
                {"a": "street", "b": "exterior", "class": "walk",
                 "via": "seam-" + WEST},
            ],
        },
        "shown_faces": ["east", "south"],
    }
    out = Path(campaign) / "programs" / "middle-street.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(program, indent=2, sort_keys=True) + "\n")
    print(out)


if __name__ == "__main__":
    main()
