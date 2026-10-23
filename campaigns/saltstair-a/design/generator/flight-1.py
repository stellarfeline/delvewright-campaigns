#!/usr/bin/env python3
"""Emit programs/flight-1.json — the first flight of Saltstair.

Provenance only: the emitted JSON is the artifact of record. Every handed
number is read from `delvec allocation` and declared as a `handed/...`
parameter default; the rules read them through those parameters.

Usage: flight-1.py <delvec> <prefabs> <campaign-dir>
"""
import json
import subprocess
import sys

DELVEC, PREFABS, CAMPAIGN = sys.argv[1:4]
PLACE = "node/flight-1"
TOP = "square-flight-1"          # north seam: the head of the flight
FOOT = "flight-1-upper-street"   # south seam: the street runs on at grade

raw = subprocess.run([DELVEC, "--prefabs", PREFABS, "allocation", CAMPAIGN, PLACE],
                     check=True, capture_output=True, text=True).stdout
alloc, _ = json.JSONDecoder().raw_decode(raw.lstrip())

params = {"handed/datum-y": alloc["datum_y"]}
for seam in alloc["seams"]:
    stem = seam["edge"].split("/", 1)[1]
    (x0, y0, z0), (x1, y1, z1) = seam["cells"]
    for k, v in dict(x0=x0, y0=y0, z0=z0, x1=x1, y1=y1, z1=z1, rise=seam["rise"]).items():
        params[f"handed/seam/{stem}/{k}"] = v
params["h"] = 0  # the course a tread stands at; counted up the flight by bind


def I(v):
    return {"expr": "int", "value": v}


def P(name):
    return {"expr": "param", "name": name}


def S(stem, k):
    return P(f"handed/seam/{stem}/{k}")


def add(a, b):
    return {"expr": "arith", "lhs": a, "op": "add", "rhs": b}


def sub(a, b):
    return {"expr": "arith", "lhs": a, "op": "sub", "rhs": b}


def div(a, b):
    return {"expr": "arith", "lhs": a, "op": "div", "rhs": b}


def span(stem, a):  # cells an inclusive handed range covers on axis a
    return add(sub(S(stem, a + "1"), S(stem, a + "0")), I(1))


def ab(e):
    return {"size": "absolute", "blocks": e}


REL = {"size": "relative", "weight": I(1)}


def split(axis, sizes, children):
    return {"op": "split", "axis": axis, "sizes": sizes, "children": children}


def call(s):
    return {"op": "call", "symbol": s}


def fill(role):
    return {"op": "fill", "material": {"role": role}}


def claim(region, body=None):
    return {"op": "claim", "region": region, "body": body or {"op": "void"}}


def bind(params_, body):
    return {"op": "bind", "params": params_, "body": body}


def rule(body, when=None):
    alt = {"weight": 1, "body": body}
    if when:
        alt["when"] = when
    return [alt]


def across(stem, west, street, east):
    """A z-band cut across x: the west ring, the street the seam spans, the east ring."""
    return split("x", [ab(S(stem, "x0")), ab(span(stem, "x")), REL], [west, street, east])


H = P("h")
W = add(H, I(1))  # the walk course over a tread at course h

rules = {
    # North to south: the head landing (the square's opening stands over it),
    # the treads, the foot landing, and the south ring the street runs on through.
    "place": rule({
        "op": "mark",
        "mark": {"anchor": "node-flight-1", "at": "offset", "facing": "north",
                 "x": div(add(S(FOOT, "x0"), S(FOOT, "x1")), I(2)),
                 "y": P("handed/datum-y"),
                 "z": sub(S(FOOT, "z0"), I(1))},
        "body": split("z",
                      [ab(span(TOP, "z")), ab(S(TOP, "rise")), REL, ab(span(FOOT, "z"))],
                      [call("head"),
                       bind({"h": P("handed/datum-y")}, call("flight")),
                       call("foot"),
                       call("mouth")]),
    }),

    # The head landing: paved at the course under the square's walk plane,
    # its air the opening the square cuts.
    "head": rule(across(TOP, call("post-head"), call("head-street"), call("post-head"))),
    "head-street": rule(split("y",
                              [ab(sub(S(TOP, "y0"), I(1))), ab(I(1)), REL],
                              [fill("ground"), fill("paving"), claim("north-mouth")])),
    "post-head": rule(bind({"h": sub(S(TOP, "y0"), I(1))}, call("post"))),

    # One tread per course, peeled off the south end; the remainder climbs one more.
    # The topmost tread is the head of the flight: the air over it is where a
    # body stands under the square's opening.
    "flight": [
        {"weight": 1,
         "when": {"cond": "cmp", "lhs": {"expr": "dim", "dim": "z"}, "op": "ge", "rhs": I(2)},
         "body": split("z", [REL, ab(I(1))],
                       [bind({"h": add(H, I(1))}, call("flight")), call("tread")])},
        {"weight": 1,
         "when": {"cond": "cmp", "lhs": {"expr": "dim", "dim": "z"}, "op": "eq", "rhs": I(1)},
         "body": call("tread-top")},
        {"weight": 1, "when": {"cond": "otherwise"}, "body": {"op": "void"}},
    ],
    "tread": rule(across(TOP, call("kerb"), call("tread-street"), call("kerb"))),
    "tread-top": rule(across(TOP, call("kerb"), call("tread-head"), call("kerb"))),
    "tread-head": rule(split("y", [ab(H), ab(I(1)), REL],
                             [fill("ground"), fill("tread"), claim("head")])),
    "tread-street": rule(split("y", [ab(H), REL],
                               [fill("ground"),
                                claim("flight", split("y", [ab(I(1)), REL],
                                                      [fill("tread"), {"op": "void"}]))])),

    # The foot landing: paved at grade, the body's place.
    "foot": rule(across(FOOT, call("post-foot"), call("foot-street"), call("post-foot"))),
    "foot-street": rule(split("y", [ab(P("handed/datum-y")), REL],
                              [fill("paving"), claim("foot")])),
    "post-foot": rule(bind({"h": sub(P("handed/datum-y"), I(1))}, call("post"))),

    # The south ring: the whole face is the opening onto the upper street.
    "mouth": rule(across(FOOT, {"op": "void"},
                         split("y", [ab(S(FOOT, "y0")), ab(span(FOOT, "y")), REL],
                               [{"op": "skip"}, claim("foot-mouth"), {"op": "void"}]),
                         {"op": "void"})),

    # The kerb walls: stone brick up to the walk course of the tread beside them.
    "kerb": rule(split("y", [ab(add(W, I(1))), REL], [fill("kerb"), claim("kerb")])),
    # A kerb post one course higher, with its lantern standing on it.
    "post": rule(split("y", [ab(add(W, I(2))), ab(I(1)), REL],
                       [fill("kerb"), fill("lamp"), claim("kerb")])),
}

program = {
    "version": "1.9.0",
    "name": "saltstair-a-flight-1",
    "start": "place",
    "params": params,
    "palette": {
        "ground": "minecraft:stone_bricks",
        "paving": "minecraft:cobblestone",
        "tread": {"local": "minecraft:stone_brick_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]"},
        "kerb": "minecraft:stone_bricks",
        "lamp": "minecraft:lantern[hanging=false,waterlogged=false]",
    },
    "rules": rules,
    "contract": {
        "entry": "foot",
        "spaces": {"foot": {"envelope": "open"}, "head": {"envelope": "open"}},
        "no_body": {"kerb": {"reason": "the tops of the kerb walls and posts beside the flight, which nobody is meant to walk"}},
        "edges": [
            {"a": "foot", "b": "exterior", "class": "walk", "via": "foot-mouth"},
            {"a": "foot", "b": "head", "class": "stair",
             "rise": params[f"handed/seam/{TOP}/rise"], "via": "flight"},
            {"a": "head", "b": "exterior", "class": "walk", "via": "north-mouth"},
        ],
    },
}

out = f"{CAMPAIGN}/programs/flight-1.json"
with open(out, "w") as f:
    json.dump(program, f, indent=2, sort_keys=True)
    f.write("\n")
print(out)
