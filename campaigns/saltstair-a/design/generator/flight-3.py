#!/usr/bin/env python3
"""Emit programs/flight-3.json — the third flight of Saltstair.

Every handed number is read from `delvec allocation` and written only as a
`handed/...` parameter default; the rules read those parameters, never a
literal. Run from anywhere:

    python3 design/generator/flight-3.py [path/to/delvec]
"""
import json
import pathlib
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve()
CAMPAIGN = HERE.parents[2]
REPO = CAMPAIGN.parents[1]
DELVEC = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path.home() / ".delvewright/bin/delvec")
PLACE = "node/flight-3"
NORTH = "middle-street-flight-3"
SOUTH = "flight-3-lower-street"

out = subprocess.run(
    [DELVEC, "--prefabs", str(REPO / "prefabs"), "allocation", str(CAMPAIGN), PLACE],
    check=True, capture_output=True, text=True).stdout
alloc, _ = json.JSONDecoder().raw_decode(out)

params = {"handed/datum-y": alloc["datum_y"], "lift": 0}
for seam in alloc["seams"]:
    stem = seam["edge"].split("/", 1)[1]
    (x0, y0, z0), (x1, y1, z1) = seam["cells"]
    for k, v in dict(x0=x0, y0=y0, z0=z0, x1=x1, y1=y1, z1=z1, rise=seam["rise"]).items():
        params[f"handed/seam/{stem}/{k}"] = v
NORTH_RISE = alloc["seams"][[s["edge"] for s in alloc["seams"]].index("edge/" + NORTH)]["rise"]


# ---- expression helpers ---------------------------------------------------
def P(name):
    return {"expr": "param", "name": name}


def H(stem, k):
    return P(f"handed/seam/{stem}/{k}")


def I(v):
    return {"expr": "int", "value": v}


def add(a, b):
    return {"expr": "arith", "op": "add", "lhs": a, "rhs": b}


def sub(a, b):
    return {"expr": "arith", "op": "sub", "lhs": a, "rhs": b}


def span(stem, axis):  # inclusive count of a seam's cells along an axis
    return add(sub(H(stem, axis + "1"), H(stem, axis + "0")), I(1))


DATUM = P("handed/datum-y")
LIFT = P("lift")


def ab(e):
    return {"size": "absolute", "blocks": e}


REL = {"size": "relative", "weight": I(1)}


def split(axis, sizes, children):
    return {"op": "split", "axis": axis, "sizes": sizes, "children": children}


def fill(role):
    return {"op": "fill", "material": {"role": role}}


VOID = {"op": "void"}
SKIP = {"op": "skip"}


def claim(region, body):
    return {"op": "claim", "region": region, "body": body}


def call(sym):
    return {"op": "call", "symbol": sym}


def rule(body, when=None):
    alt = {"weight": 1, "body": body}
    if when is not None:
        alt["when"] = when
    return alt


def lanes(stem, west, lane, east):
    """The x cut every row shares: the west ring, the six-wide lane, the east ring."""
    return split("x", [ab(H(stem, "x0")), ab(span(stem, "x")), REL], [west, lane, east])


def ring(side, kerb_top, post):
    """A ring column: kerb masonry from the claim's bottom up to kerb_top
    inclusive (the whole's fixed ground voids its lower cells), then — on a
    post row — a chiselled post and a lantern; everything above the kerb is
    out of the walk."""
    above = split("y", [ab(I(1)), ab(I(1)), REL], [fill("post"), fill("lamp"), VOID]) if post else VOID
    return split("y", [ab(add(kerb_top, I(1))), REL], [fill("kerb"), claim(f"kerb-{side}", above)])


rules = {}

# the whole frame, north to south
rules["place"] = [rule(split("z", [
    ab(H(NORTH, "z0")),
    ab(span(NORTH, "z")),
    ab(I(1)),
    ab(sub(H(NORTH, "rise"), I(1))),
    ab(sub(sub(sub(H(SOUTH, "z0"), H(NORTH, "z1")), I(1)), H(NORTH, "rise"))),
    ab(span(SOUTH, "z")),
    REL,
], [SKIP, call("head-row"),
    {"op": "bind", "params": {"lift": H(NORTH, "rise")}, "body": call("top-tread-row")},
    call("flight"), call("foot-row"), call("south-row"), SKIP]))]

# the head of the flight: the top step stands under the middle street's hole
NB = H(NORTH, "y0")  # body level at the head
rules["head-row"] = [rule(lanes(
    NORTH,
    ring("west", NB, True),
    split("y", [ab(sub(NB, I(1))), ab(I(1)), ab(span(NORTH, "y")), REL],
          [fill("fill"), fill("paving"), claim("middle-street-way", VOID), VOID]),
    ring("east", NB, True)))]

# the treads: peel one row off the north end; the box that is left is the index
rules["flight"] = [
    rule({"op": "bind", "params": {"lift": {"expr": "dim", "dim": "z"}},
          "body": split("z", [ab(I(1)), REL], [call("tread-row"), call("flight")])},
         when={"cond": "cmp", "lhs": {"expr": "dim", "dim": "z"}, "op": "ge", "rhs": I(2)}),
    rule({"op": "bind", "params": {"lift": {"expr": "dim", "dim": "z"}}, "body": call("tread-row")},
         when={"cond": "otherwise"}),
]
TREAD_Y = sub(add(DATUM, LIFT), I(1))  # the tread block's own course
rules["tread-row"] = [rule(lanes(
    SOUTH,
    ring("west", add(DATUM, LIFT), False),
    split("y", [ab(TREAD_Y), ab(I(1)), REL],
          [fill("fill"), claim("flight", fill("tread")), claim("flight", VOID)]),
    ring("east", add(DATUM, LIFT), False)))]
# the fourth step, at the top: its tread is the head landing under the hole
rules["top-tread-row"] = [rule(lanes(
    SOUTH,
    ring("west", add(DATUM, LIFT), False),
    split("y", [ab(TREAD_Y), ab(I(1)), REL],
          [fill("fill"), fill("tread"), claim("head", VOID)]),
    ring("east", add(DATUM, LIFT), False)))]

# the foot: the lower street's grade, where the place's body stands
rules["foot-row"] = [rule(lanes(
    SOUTH,
    ring("west", DATUM, True),
    split("y", [ab(DATUM), REL], [fill("paving"), {
        "op": "mark", "mark": {"anchor": "node-flight-3", "at": "floor_center", "facing": "north"},
        "body": claim("street", VOID)}]),
    ring("east", DATUM, True)))]

# the south plane, ours: the street runs on at grade through the whole face
rules["south-row"] = [rule(lanes(
    SOUTH,
    ring("west", DATUM, False),
    split("y", [ab(H(SOUTH, "y0")), ab(span(SOUTH, "y")), REL],
          [fill("paving"), claim("lower-street-way", VOID), VOID]),
    ring("east", DATUM, False)))]

program = {
    "version": "1.9.0",
    "name": "saltstair-a-flight-3",
    "start": "place",
    "params": params,
    "palette": {
        "paving": "minecraft:cobblestone",
        "fill": "minecraft:stone_bricks",
        "tread": "minecraft:stone_brick_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]",
        "kerb": [
            {"weight": 5, "block": "minecraft:stone_bricks"},
            {"weight": 1, "block": "minecraft:mossy_stone_bricks"},
        ],
        "post": "minecraft:chiseled_stone_bricks",
        "lamp": "minecraft:lantern[hanging=false,waterlogged=false]",
    },
    "rules": rules,
    "contract": {
        "entry": "street",
        "spaces": {"street": {"envelope": "open"}, "head": {"envelope": "open"}},
        "no_body": {
            "kerb-west": {"reason": "the top of the west kerb wall and its lantern posts, beside the flight"},
            "kerb-east": {"reason": "the top of the east kerb wall and its lantern posts, beside the flight"},
        },
        "edges": [
            {"a": "street", "b": "exterior", "class": "walk", "via": "lower-street-way"},
            {"a": "street", "b": "head", "class": "stair", "rise": NORTH_RISE, "via": "flight"},
            {"a": "head", "b": "exterior", "class": "stair", "rise": 0, "via": "middle-street-way"},
        ],
    },
}

dest = CAMPAIGN / "programs" / "flight-3.json"
dest.parent.mkdir(exist_ok=True)
dest.write_text(json.dumps(program, indent=2, sort_keys=True) + "\n")
print(dest)
