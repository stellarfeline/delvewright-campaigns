#!/usr/bin/env python3
"""Emit programs/flight-5.json — the fifth flight of Saltstair.

Provenance only: the emitted JSON is the artifact of record. Every handed
number is read from `delvec allocation` and lands in the program as a
`handed/...` parameter default; the rules read those parameters, never a copy.

Layout, north (z min) to south (z max):
  north layer   the shore street's opening, answered at this frame's first layer
  steps         one tread row per course of the north seam's rise; the last
                (northmost) row is the head landing
  foot          the landing at the quay's grade
  south layer   this place's own plane, cut by the quay opening
Across x: a kerb column on the ring each side, the walk between them, whose
tread course keeps its outermost columns as whole stone-brick kerbs.
"""
import json
import subprocess
import sys
from pathlib import Path

DELVEC = "/home/stella/.delvewright/bin/delvec"
CAMPAIGN = Path(__file__).resolve().parents[2]
PLACE = "node/flight-5"
NORTH = "shore-street-flight-5"
SOUTH = "flight-5-quay"


def allocation():
    out = subprocess.run([DELVEC, "allocation", str(CAMPAIGN), PLACE],
                         check=True, capture_output=True, text=True).stdout
    alloc, _ = json.JSONDecoder().raw_decode(out)
    return alloc


def i(v):
    return {"expr": "int", "value": v}


def p(name):
    return {"expr": "param", "name": name}


def add(a, b):
    return {"expr": "arith", "lhs": a, "op": "add", "rhs": b}


def sub(a, b):
    return {"expr": "arith", "lhs": a, "op": "sub", "rhs": b}


def ab(e):
    return {"size": "absolute", "blocks": e}


REL = {"size": "relative", "weight": i(1)}


def split(axis, pairs):
    return {"op": "split", "axis": axis,
            "sizes": [s for s, _ in pairs], "children": [c for _, c in pairs]}


def fill(role):
    return {"op": "fill", "material": {"role": role}}


def call(sym):
    return {"op": "call", "symbol": sym}


def claim(region, body=None):
    return {"op": "claim", "region": region, "body": body or {"op": "void"}}


def bind(params, body):
    return {"op": "bind", "params": params, "body": body}


def rule(body, when=None):
    alt = {"weight": 1, "body": body}
    if when is not None:
        alt["when"] = when
    return alt


def seam(stem, k):
    return p(f"handed/seam/{stem}/{k}")


def span(stem, a):
    """Inclusive cell count of a seam's opening along axis a."""
    return add(sub(seam(stem, f"{a}1"), seam(stem, f"{a}0")), i(1))


def main():
    a = allocation()
    params = {"handed/datum-y": a["datum_y"]}
    for s in a["seams"]:
        stem = s["edge"].split("/", 1)[1]
        (x0, y0, z0), (x1, y1, z1) = s["cells"]
        for k, v in (("x0", x0), ("y0", y0), ("z0", z0),
                     ("x1", x1), ("y1", y1), ("z1", z1), ("rise", s["rise"])):
            params[f"handed/seam/{stem}/{k}"] = v
    # local knobs: the tread course a row stands on (bound per row), and
    # whether a kerb column carries a lantern post (bound per row)
    params["lvl"] = 0
    params["post"] = 0
    params["head"] = 0

    # the y of the shore street's floor course, one under its walk plane
    north_floor = sub(seam(NORTH, "y0"), i(1))

    rules = {
        # ---- the whole: rows north to south ----
        "place": [rule(split("z", [
            (ab(span(NORTH, "z")), call("north-layer")),
            (ab(seam(NORTH, "rise")),
             bind({"lvl": p("handed/datum-y")}, call("steps"))),
            (REL, call("foot")),
            (ab(span(SOUTH, "z")), call("south-layer")),
        ]))],

        # a row across x: kerb column, walk, kerb column (the walk is the
        # seams' own width, read from the north seam's x cells)
        "row": [rule(split("x", [
            (ab(seam(NORTH, "x0")), call("kerb")),
            (ab(span(NORTH, "x")), call("walk")),
            (REL, call("kerb")),
        ]))],

        # ---- the steps: one row per course of rise, peeled off the south
        # end; the last row left is the head landing ----
        "steps": [
            rule(split("z", [
                (REL, bind({"lvl": add(p("lvl"), i(1))}, call("steps"))),
                (ab(i(1)), call("row")),
            ]), when={"cond": "cmp", "lhs": {"expr": "dim", "dim": "z"},
                      "op": "ge", "rhs": i(2)}),
            rule(bind({"head": i(1), "post": i(1)}, call("row")),
                 when={"cond": "otherwise"}),
        ],

        # the walk of a row: whichever row it is, by the bound knobs
        "walk": [
            rule(call("walk-north"),
                 when={"cond": "cmp", "lhs": p("lvl"), "op": "eq",
                       "rhs": {"expr": "int", "value": -1}}),
            rule(call("walk-flat"),
                 when={"cond": "cmp", "lhs": p("lvl"), "op": "eq", "rhs": i(0)}),
            rule(call("walk-tread"), when={"cond": "otherwise"}),
        ],

        # a tread row: masonry under, one tread course, air over
        "walk-tread": [rule(split("y", [
            (ab(p("lvl")), fill("fill")),
            (ab(i(1)), call("tread-course")),
            (REL, call("tread-air")),
        ]))],
        "tread-course": [rule(split("x", [
            (ab(i(1)), fill("kerb-tread")),
            (REL, fill("tread")),
            (ab(i(1)), fill("kerb-tread")),
        ]))],
        "tread-air": [
            rule({"op": "mark",
                  "mark": {"anchor": "node-flight-5", "at": "floor_center",
                           "facing": "south"},
                  "body": claim("head")},
                 when={"cond": "cmp", "lhs": p("head"), "op": "eq", "rhs": i(1)}),
            rule(claim("flight"), when={"cond": "otherwise"}),
        ],

        # ---- the foot landing, at the quay's grade ----
        "foot": [rule(bind({"lvl": i(0), "post": i(1)}, call("row")))],
        "walk-flat": [rule(split("y", [
            (ab(p("handed/datum-y")), fill("paving")),
            (REL, call("foot-air")),
        ]))],
        "foot-air": [rule(claim("foot"))],

        # ---- the north layer: paving at the shore street's floor course,
        # the opening over it ----
        "north-layer": [rule(bind({"lvl": i(-1)}, call("row")))],
        "walk-north": [rule(split("y", [
            (ab(north_floor), fill("fill")),
            (ab(i(1)), fill("paving")),
            (ab(span(NORTH, "y")), claim(f"seam-{NORTH}")),
            (REL, {"op": "void"}),
        ]))],

        # ---- the south layer: this place's own plane, cut by the quay
        # opening; nothing stands over the opening ----
        "south-layer": [rule(split("x", [
            (ab(seam(SOUTH, "x0")), bind({"lvl": i(0)}, call("kerb-end"))),
            (ab(span(SOUTH, "x")), call("south-walk")),
            (REL, bind({"lvl": i(0)}, call("kerb-end"))),
        ]))],
        "south-walk": [rule(split("y", [
            (ab(seam(SOUTH, "y0")), fill("paving")),
            (ab(span(SOUTH, "y")), claim(f"seam-{SOUTH}")),
            (REL, {"op": "void"}),
        ]))],

        # ---- kerb columns on the ring: mossy foot courses up to the tread,
        # a plain course at knee height, then a coping slab — or, where the
        # row carries a post, a chiseled post with a lantern on it ----
        "kerb": [
            rule(call("kerb-at-north"),
                 when={"cond": "cmp", "lhs": p("lvl"), "op": "eq",
                       "rhs": {"expr": "int", "value": -1}}),
            rule(call("kerb-body"), when={"cond": "otherwise"}),
        ],
        "kerb-at-north": [rule(bind({"lvl": north_floor}, call("kerb-body")))],
        "kerb-end": [rule(call("kerb-body"))],
        "kerb-body": [rule(split("y", [
            (ab(add(p("lvl"), i(1))), fill("kerb-foot")),
            (ab(i(1)), fill("kerb")),
            (REL, call("kerb-top")),
        ]))],
        "kerb-top": [
            rule(split("y", [
                (ab(i(1)), fill("post")),
                (ab(i(1)), fill("lamp")),
                (REL, claim("kerb")),
            ]), when={"cond": "cmp", "lhs": p("post"), "op": "eq", "rhs": i(1)}),
            rule(split("y", [
                (ab(i(1)), fill("coping")),
                (REL, claim("kerb")),
            ]), when={"cond": "otherwise"}),
        ],
    }

    rise = a["seams"][[s["edge"] for s in a["seams"]].index(f"edge/{NORTH}")]["rise"]
    program = {
        "version": "1.9.0",
        "name": "saltstair-a-flight-5",
        "start": "place",
        "params": params,
        "palette": {
            "paving": "minecraft:cobblestone",
            "fill": "minecraft:stone_bricks",
            "tread": "minecraft:stone_brick_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]",
            "kerb-tread": "minecraft:stone_bricks",
            "kerb-foot": [
                {"weight": 5, "block": "minecraft:mossy_stone_bricks"},
                {"weight": 3, "block": "minecraft:stone_bricks"},
                {"weight": 1, "block": "minecraft:cracked_stone_bricks"},
            ],
            "kerb": "minecraft:stone_bricks",
            "coping": "minecraft:stone_brick_slab[type=bottom,waterlogged=false]",
            "post": "minecraft:chiseled_stone_bricks",
            "lamp": "minecraft:lantern[hanging=false,waterlogged=false]",
        },
        "rules": rules,
        "contract": {
            "entry": "head",
            "spaces": {"head": {"envelope": "open"},
                       "foot": {"envelope": "open"}},
            "no_body": {"kerb": {"reason": "the tops of the kerb walls and their lantern posts beside the flight, which no one is meant to walk"}},
            "edges": [
                {"a": "head", "b": "exterior", "class": "walk",
                 "via": f"seam-{NORTH}"},
                {"a": "foot", "b": "head", "class": "stair", "rise": rise,
                 "via": "flight"},
                {"a": "foot", "b": "exterior", "class": "walk",
                 "via": f"seam-{SOUTH}"},
            ],
        },
        "shown_faces": ["east", "south", "west"],
    }
    out = CAMPAIGN / "programs" / "flight-5.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(program, indent=1, sort_keys=True) + "\n")
    print(out)


if __name__ == "__main__":
    sys.exit(main())
