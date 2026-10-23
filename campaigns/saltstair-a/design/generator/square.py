#!/usr/bin/env python3
"""Emit programs/square.json — the square at the top of Saltstair.

Provenance only: the JSON is the artifact of record. Every handed number is
read from `delvec allocation` and becomes a `handed/...` parameter default;
no handed value is typed here.
"""
import json, subprocess, sys, os

DELVEC = os.path.expanduser("~/.delvewright/bin/delvec")
CAMPAIGN = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT = os.path.join(CAMPAIGN, "programs", "square.json")

raw = subprocess.run([DELVEC, "allocation", CAMPAIGN, "node/square"],
                     check=True, capture_output=True, text=True).stdout
alloc, _ = json.JSONDecoder().raw_decode(raw.lstrip())

def stem(edge): return edge.split("/", 1)[1]
seams = {stem(s["edge"]): s for s in alloc["seams"]}
FLIGHT, CHAPEL, INN = "square-flight-1", "square-chapel", "square-inn"
assert set(seams) == {FLIGHT, CHAPEL, INN}, seams.keys()

params = {"handed/datum-y": alloc["datum_y"],
          "handed/ground/bottom-y": alloc["ground"]["bottom_y"]}
for name, s in seams.items():
    (x0, y0, z0), (x1, y1, z1) = s["cells"]
    for k, v in dict(x0=x0, y0=y0, z0=z0, x1=x1, y1=y1, z1=z1).items():
        params[f"handed/seam/{name}/{k}"] = v
# arguments of the one door rule, always bound by its caller
params.update({"door-z0": 0, "door-z1": 0, "door-y0": 0, "door-y1": 0, "door-side": 0})

# ---- expression helpers
def P(n): return {"expr": "param", "name": n}
def I(v): return {"expr": "int", "value": v}
def D(a): return {"expr": "dim", "dim": a}
def add(a, b): return {"expr": "arith", "lhs": a, "op": "add", "rhs": b}
def sub(a, b): return {"expr": "arith", "lhs": a, "op": "sub", "rhs": b}
def div(a, b): return {"expr": "arith", "lhs": a, "op": "div", "rhs": b}
def span(lo, hi): return add(sub(hi, lo), I(1))
def ab(e): return {"size": "absolute", "blocks": e if isinstance(e, dict) else I(e)}
def rel(w=1): return {"size": "relative", "weight": I(w)}
def split(axis, sizes, children, **kw):
    d = {"op": "split", "axis": axis, "sizes": sizes, "children": children}
    d.update(kw); return d
def fill(role): return {"op": "fill", "material": {"role": role}}
def call(s): return {"op": "call", "symbol": s}
def claim(r, body=None): return {"op": "claim", "region": r, "body": body or {"op": "void"}}
VOID = {"op": "void"}
SKIP = {"op": "skip"}
def rule(body, when=None):
    a = {"weight": 1, "body": body}
    if when: a["when"] = when
    return [a]

def seam(name, k): return P(f"handed/seam/{name}/{k}")
DATUM = P("handed/datum-y")

rules = {}

# Whole frame: the ground course under the square, then the open storey.
rules["square"] = rule(split("y",
    [ab(P("handed/ground/bottom-y")), ab(sub(DATUM, P("handed/ground/bottom-y"))), rel()],
    [SKIP, call("paving"), call("storey")]))

# Paving: the ring's ground is the whole's (void); inside it a stone-brick kerb
# band round cobblestone setts.
rules["paving"] = rule(split("x", [ab(1), rel(), ab(1)],
    [SKIP, split("z", [ab(1), rel(), ab(1)], [SKIP, call("kerbed"), SKIP]), SKIP]))
rules["kerbed"] = rule(split("x", [ab(1), rel(), ab(1)],
    [fill("kerb"), split("z", [ab(1), rel(), ab(1)],
                         [fill("kerb"), fill("setts"), fill("kerb")]), fill("kerb")]))

# Storey: north parapet row, the square between, south row with the flight.
rules["storey"] = rule(split("z", [ab(1), rel(), ab(1)],
    [call("north-row"), call("middle"), call("south-row")]))

# A parapet cell column: one course of masonry, open air over it.
rules["parapet"] = rule(split("y", [ab(1), rel()],
    [fill("wall"), claim("parapet-top")]))
# A kerb post: a dressed block with a lantern on it, open air over it.
rules["post"] = rule(split("y", [ab(1), ab(1), rel()],
    [fill("post"), fill("lamp"), claim("post-top")]))

rules["north-row"] = rule(split("x", [rel(1), ab(1), rel(2), ab(1), rel(1)],
    [call("parapet"), call("post"), call("parapet"), call("post"), call("parapet")]))

# South row: the parapet over the drop to the upper street, cut for the first
# flight at the handed cells, a post with its lantern either side.
rules["south-row"] = rule(split("x",
    [ab(sub(seam(FLIGHT, "x0"), I(1))), ab(1),
     ab(span(seam(FLIGHT, "x0"), seam(FLIGHT, "x1"))), ab(1), rel()],
    [call("parapet"), call("post"), call("flight-mouth"), call("post"), call("parapet")]))
rules["flight-mouth"] = rule(split("y",
    [ab(sub(seam(FLIGHT, "y0"), DATUM)), ab(span(seam(FLIGHT, "y0"), seam(FLIGHT, "y1"))), rel()],
    [claim("square"), claim(f"seam-{FLIGHT}"), claim("square")]))

# Middle band: the neighbours' walls at x 0 and x 19 (voids where they stand),
# the first layer beside each, where its door is answered, and the open square.
def door_layer(name, side):
    return {"op": "bind",
            "params": {"door-z0": seam(name, "z0"), "door-z1": seam(name, "z1"),
                       "door-y0": seam(name, "y0"), "door-y1": seam(name, "y1"),
                       "door-side": I(side)},
            "body": call("door-layer")}
rules["middle"] = rule(split("x", [ab(1), ab(1), rel(), ab(1), ab(1)],
    [call("parapet"), door_layer(CHAPEL, 0), call("core"), door_layer(INN, 1), call("parapet")]))

# The layer against a house front: posts with lanterns one cell either side of
# its door, the door's cells answered as the seam's opening.
rules["door-layer"] = rule(split("z",
    [ab(sub(P("door-z0"), I(3))), ab(1), ab(1),
     ab(span(P("door-z0"), P("door-z1"))), ab(1), ab(1), rel()],
    [claim("square"), call("post"), claim("square"), call("doorway"),
     claim("square"), call("post"), claim("square")]))
rules["doorway"] = rule(split("y",
    [ab(sub(P("door-y0"), DATUM)), ab(span(P("door-y0"), P("door-y1"))), rel()],
    [claim("square"), call("door-cells"), claim("square")]))
def eq(n, v): return {"cond": "cmp", "lhs": P(n), "op": "eq", "rhs": I(v)}
rules["door-cells"] = [
    {"weight": 1, "when": eq("door-side", 0), "body": claim(f"seam-{CHAPEL}")},
    {"weight": 1, "when": eq("door-side", 1), "body": claim(f"seam-{INN}")},
]

# The open square, with the place's body at its middle and the party's spawn
# at its north edge, looking south down the street between chapel and inn.
rules["core"] = rule({"op": "mark",
    "mark": {"anchor": "node-square", "at": "floor_center", "facing": "south"},
    "body": {"op": "mark",
             "mark": {"anchor": "spawn", "at": "offset", "facing": "south",
                      "x": div(D("x"), I(2)), "y": I(0), "z": I(1)},
             "body": claim("square")}})

program = {
    "version": "1.9.0",
    "name": "saltstair-square",
    "start": "square",
    "params": params,
    "palette": {
        "setts": [{"weight": 8, "block": "minecraft:cobblestone"},
                  {"weight": 1, "block": "minecraft:mossy_cobblestone"},
                  {"weight": 1, "block": "minecraft:andesite"}],
        "kerb": "minecraft:stone_bricks",
        "wall": [{"weight": 6, "block": "minecraft:stone_bricks"},
                 {"weight": 2, "block": "minecraft:mossy_stone_bricks"},
                 {"weight": 1, "block": "minecraft:cracked_stone_bricks"}],
        "post": "minecraft:chiseled_stone_bricks",
        "lamp": "minecraft:lantern[hanging=false,waterlogged=false]",
    },
    "rules": rules,
    "contract": {
        "entry": "square",
        "spaces": {"square": {"envelope": "open"}},
        "no_body": {
            "parapet-top": {"reason": "the coping of the parapet round the square's edge, over the drop and the hillside"},
            "post-top": {"reason": "the top of a lantern on its kerb post"},
        },
        "edges": [
            {"a": "square", "b": "exterior", "class": "walk", "via": f"seam-{FLIGHT}"},
            {"a": "square", "b": "exterior", "class": "walk", "via": f"seam-{CHAPEL}"},
            {"a": "square", "b": "exterior", "class": "walk", "via": f"seam-{INN}"},
        ],
    },
    "shown_faces": ["north", "south", "east", "west"],
}
with open(OUT, "w") as f:
    json.dump(program, f, indent=2, sort_keys=True); f.write("\n")
print(OUT)
