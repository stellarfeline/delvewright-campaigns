#!/usr/bin/env python3
"""Emit programs/upper-street.json — the upper street of Saltstair.

Provenance only: the emitted JSON is the artifact of record. Every handed
number is read through a `handed/...` parameter whose default is the value
`delvec allocation` hands; this script computes structure, never a judgement.
"""
import json
import pathlib
import subprocess
import sys

DELVEC = "/home/stella/.delvewright/bin/delvec"
CAMPAIGN = pathlib.Path(__file__).resolve().parents[2]
OUT = CAMPAIGN / "programs" / "upper-street.json"

NORTH = "flight-1-upper-street"
SOUTH = "upper-street-flight-2"
SMITHY = "upper-street-smithy"
WEAVER = "upper-street-weaver"


def allocation():
    out = subprocess.run(
        [DELVEC, "allocation", str(CAMPAIGN), "node/upper-street"],
        check=True, capture_output=True, text=True).stdout
    return json.loads(out[out.index("{"):out.rindex("}") + 1])


def handed_params(a):
    p = {
        "handed/datum-y": a["datum_y"],
        "handed/ground/bottom-y": a["ground"]["bottom_y"],
    }
    for s in a["seams"]:
        stem = s["edge"].split("/", 1)[1]
        (x0, y0, z0), (x1, y1, z1) = s["cells"]
        for k, v in dict(x0=x0, y0=y0, z0=z0, x1=x1, y1=y1, z1=z1,
                         rise=s["rise"]).items():
            p[f"handed/seam/{stem}/{k}"] = v
    return p


# ---- expression and node helpers -------------------------------------------
def I(v):
    return {"expr": "int", "value": v}


def P(name):
    return {"expr": "param", "name": name}


def S(stem, k):
    return P(f"handed/seam/{stem}/{k}")


def add(a, b):
    return {"expr": "arith", "op": "add", "lhs": a, "rhs": b}


def sub(a, b):
    return {"expr": "arith", "op": "sub", "lhs": a, "rhs": b}


def span(stem, lo, hi):  # inclusive count of a seam box along one axis
    return add(sub(S(stem, hi), S(stem, lo)), I(1))


def ab(e):
    return {"size": "absolute", "blocks": e if isinstance(e, dict) else I(e)}


REL = {"size": "relative", "weight": I(1)}


def split(axis, pairs):
    return {"op": "split", "axis": axis,
            "sizes": [s for s, _ in pairs], "children": [c for _, c in pairs]}


def call(sym):
    return {"op": "call", "symbol": sym}


def fill(role):
    return {"op": "fill", "material": {"role": role}}


def claim(region, body):
    return {"op": "claim", "region": region, "body": body}


VOID = {"op": "void"}
SKIP = {"op": "skip"}

# the course of ground under the walk plane: from the claim's bottom up to it
GROUND = sub(P("handed/datum-y"), P("handed/ground/bottom-y"))


def rules():
    r = {}
    one = lambda body: [{"weight": 1, "body": body}]

    # x: the west ring, the street (the second flight's width), the east ring
    r["place"] = one(split("x", [
        (ab(S(SOUTH, "x0")), call("side")),
        (ab(span(SOUTH, "x0", "x1")), call("street-band")),
        (REL, {"op": "reorient", "orient": {"mirror": {"x": True}},
               "body": call("side")}),
    ]))

    # one ring column, reflected for the east side: a parapet along the
    # terrace edge (the neighbours' walls stand in most of it, as voids), and
    # a lamp post at the head of the second flight
    r["side"] = one(split("z", [
        (ab(S(SOUTH, "z0")), split("y", [
            (ab(GROUND), SKIP),
            (REL, claim("parapet", split("y", [
                (ab(1), fill("parapet-foot")),
                (ab(1), fill("parapet-cap")),
                (REL, VOID),
            ]))),
        ])),
        (REL, split("y", [
            (ab(GROUND), SKIP),
            (REL, claim("parapet", split("y", [
                (ab(2), fill("post")),
                (ab(1), fill("lamp")),
                (REL, VOID),
            ]))),
        ])),
    ]))

    # z: the terrace (paving and its air), then the plane the second flight's
    # opening is cut in
    r["street-band"] = one(split("z", [
        (ab(S(SOUTH, "z0")), split("y", [
            (ab(GROUND), call("paving")),
            (REL, call("street-air")),
        ])),
        (REL, split("y", [
            (ab(GROUND), SKIP),
            (ab(span(SOUTH, "y0", "y1")), claim("south-mouth", VOID)),
            (REL, VOID),
        ])),
    ]))

    # cobbles between flush stone-brick kerbs
    r["paving"] = one(split("x", [
        (ab(1), fill("kerb")),
        (REL, fill("paving")),
        (ab(1), fill("kerb")),
    ]))

    # the north face is answered at the first layer: the street runs on at grade
    r["street-air"] = one(split("z", [
        (ab(span(NORTH, "z0", "z1")), claim("north-mouth", VOID)),
        (REL, split("x", [
            (ab(1), call("west-lane")),
            (REL, {"op": "mark",
                   "mark": {"anchor": "node-upper-street", "at": "floor_center"},
                   "body": claim("street", VOID)}),
            (ab(1), call("east-lane")),
        ])),
    ]))

    after_north = add(S(NORTH, "z1"), I(1))  # first z of the lanes

    # the lane beside the smithy: its door, a lamp post a pace uphill of it
    r["west-lane"] = one(split("z", [
        (ab(sub(sub(S(SMITHY, "z0"), I(2)), after_north)), claim("street", VOID)),
        (ab(1), call("door-post")),
        (ab(1), claim("street", VOID)),
        (ab(span(SMITHY, "z0", "z1")), split("y", [
            (ab(span(SMITHY, "y0", "y1")), claim("smithy-door", VOID)),
            (REL, claim("street", VOID)),
        ])),
        (REL, claim("street", VOID)),
    ]))

    # the lane beside the weaver's house: its door, a lamp post a pace downhill
    r["east-lane"] = one(split("z", [
        (ab(sub(S(WEAVER, "z0"), after_north)), claim("street", VOID)),
        (ab(span(WEAVER, "z0", "z1")), split("y", [
            (ab(span(WEAVER, "y0", "y1")), claim("weaver-door", VOID)),
            (REL, claim("street", VOID)),
        ])),
        (ab(1), claim("street", VOID)),
        (ab(1), call("door-post")),
        (REL, claim("street", VOID)),
    ]))

    # a wall-post with a lantern standing on it
    r["door-post"] = one(claim("lamp-posts", split("y", [
        (ab(1), fill("door-post")),
        (ab(1), fill("lamp")),
        (REL, VOID),
    ])))
    return r


def program(a):
    return {
        "version": "1.9.0",
        "name": "saltstair-a-upper-street",
        "start": "place",
        "params": handed_params(a),
        "palette": {
            "paving": [
                {"weight": 9, "block": "minecraft:cobblestone"},
                {"weight": 1, "block": "minecraft:mossy_cobblestone"},
            ],
            "kerb": "minecraft:stone_bricks",
            "parapet-foot": "minecraft:mossy_stone_bricks",
            "parapet-cap": "minecraft:stone_bricks",
            "post": "minecraft:stone_bricks",
            "door-post": "minecraft:stone_brick_wall[east=none,north=none,south=none,up=true,waterlogged=false,west=none]",
            "lamp": "minecraft:lantern[hanging=false,waterlogged=false]",
        },
        "rules": rules(),
        "contract": {
            "entry": "street",
            "spaces": {"street": {"envelope": "open"}},
            "no_body": {
                "lamp-posts": {"reason": "the lantern on top of each door post, which nobody is meant to stand on"},
                "parapet": {"reason": "the tops of the parapet and the lamp posts at the terrace edge, which nobody is meant to walk"},
            },
            "edges": [
                {"a": "street", "b": "exterior", "class": "walk", "via": "north-mouth"},
                {"a": "street", "b": "exterior", "class": "walk", "via": "south-mouth"},
                {"a": "street", "b": "exterior", "class": "walk", "via": "smithy-door"},
                {"a": "street", "b": "exterior", "class": "walk", "via": "weaver-door"},
            ],
        },
    }


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(program(allocation()), indent=2, sort_keys=True) + "\n")
    print(OUT, file=sys.stderr)
