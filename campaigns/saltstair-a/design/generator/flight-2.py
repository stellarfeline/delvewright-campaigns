#!/usr/bin/env python3
"""Emit programs/flight-2.json: the second flight of Saltstair.

Provenance only: the emitted JSON is the artifact of record. Every handed value
is read from `delvec allocation` and becomes a `handed/...` parameter default;
the rules read geometry through those parameters and the box's own extents.

Layout (local z runs north -> south): the head course answering the north seam,
the top tread (the head space), the remaining treads (the flight's transit
volume, peeled one per course by recursion), the foot landing, and the south
plane cut open as the street running on at grade. Kerb walls stand in the ring
columns either side; lanterns stand on kerb posts at the head and the foot.
"""
import json
import pathlib
import subprocess
import sys

DELVEC = "/home/stella/.delvewright/bin/delvec"
CAMPAIGN = pathlib.Path(__file__).resolve().parents[2]
PLACE = "node/flight-2"
NORTH = "upper-street-flight-2"
SOUTH = "flight-2-middle-street"


def allocation():
    out = subprocess.run([DELVEC, "allocation", str(CAMPAIGN), PLACE],
                         check=True, capture_output=True, text=True).stdout
    obj, _ = json.JSONDecoder().raw_decode(out.lstrip())
    return obj


A = allocation()


# ---- expression helpers -------------------------------------------------
def I(v):
    return {"expr": "int", "value": v}


def P(n):
    return {"expr": "param", "name": n}


def D(axis):
    return {"expr": "dim", "dim": axis}


def ar(op, l, r):
    return {"expr": "arith", "op": op, "lhs": l, "rhs": r}


def add(l, r):
    return ar("add", l, r)


def sub(l, r):
    return ar("sub", l, r)


def span(stem, a):  # inclusive extent of a handed box along one axis
    return add(sub(P(f"handed/seam/{stem}/{a}1"), P(f"handed/seam/{stem}/{a}0")), I(1))


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


def bind(params, body):
    return {"op": "bind", "params": params, "body": body}


def rule(body, when=None):
    alt = {"weight": 1, "body": body}
    if when:
        alt["when"] = when
    return [alt]


def cmp(l, op, r):
    return {"cond": "cmp", "lhs": l, "op": op, "rhs": r}


# ---- parameters: every handed value used, defaulted to the allocation ----
params = {"handed/datum-y": A["datum_y"], "walk": 0}
for seam in A["seams"]:
    stem = seam["edge"].split("/", 1)[1]
    (x0, y0, z0), (x1, y1, z1) = seam["cells"]
    for k, v in dict(x0=x0, y0=y0, z0=z0, x1=x1, y1=y1, z1=z1).items():
        params[f"handed/seam/{stem}/{k}"] = v
    if stem == NORTH:
        params[f"handed/seam/{stem}/rise"] = seam["rise"]

DATUM = P("handed/datum-y")
RISE = P(f"handed/seam/{NORTH}/rise")
WALK = P("walk")
FX0 = P(f"handed/seam/{NORTH}/x0")      # the flight's lane is the seam's width
FW = span(NORTH, "x")

rules = {}

# A column of ground under a walk course: solid to the course below the walk,
# the walked block on top. `top` names the rule that lays that block.
for top in ("paving", "tread"):
    rules[f"under-{top}"] = rule(split("y", [REL, ab(I(1))],
                                       [call("fill"), call(top)]))
rules["fill"] = rule(fill("fill"))
rules["paving"] = rule(fill("paving"))
rules["tread"] = rule(fill("tread"))
rules["air"] = rule({"op": "void"})

# Kerb: masonry up to the course below the walk, a wall course at body height.
rules["kerb"] = rule(split("y", [ab(WALK), ab(I(1)), REL],
                           [call("kerb-fill"), call("kerb-wall"), call("air")]))
# Kerb post: two wall courses and a lantern on top.
# The cell on the lantern's cap is claimed out of the walk: nobody stands there.
rules["post"] = rule(split("y", [ab(WALK), ab(I(2)), ab(I(1)), ab(I(1)), REL],
                           [call("kerb-fill"), call("post-wall"), call("lamp"),
                            claim("lamp-caps"), call("air")]))
rules["kerb-fill"] = rule(fill("kerb"))
rules["kerb-wall"] = rule(fill("kerb_wall"))
rules["post-wall"] = rule(fill("post_wall"))
rules["lamp"] = rule(fill("lamp"))


def lane(ring, middle):
    """x: ring column, the flight's lane at the seam's width, ring column."""
    return split("x", [ab(FX0), ab(FW), REL], [call(ring), middle, call(ring)])


def walked(top, region, mark=None):
    """y: ground to the walk, then the claimed air of `region` above it."""
    air = claim(region)
    if mark:
        air = {"op": "mark", "mark": mark, "body": air}
    return split("y", [ab(WALK), REL], [call(f"under-{top}"), air])


# Head course: paved at the upper street's walk; the north seam's cells open.
rules["head"] = rule(bind({"walk": add(DATUM, RISE)}, lane("post", split(
    "y",
    [ab(P(f"handed/seam/{NORTH}/y0")), ab(span(NORTH, "y")), REL],
    [call("under-paving"), claim("seam-north"), call("air")]))))

# Top tread: its walk is the upper street's; the air above it is the head space.
rules["top-tread"] = rule(bind({"walk": add(DATUM, RISE)},
                               lane("kerb", walked("tread", "head"))))

# The rest of the treads: peel the northmost course, whose walk stands as many
# courses above the datum as there are treads left, and recurse on the rest.
rules["treads"] = [
    {"weight": 1,
     "when": cmp(D("z"), "ge", I(1)),
     "body": bind({"walk": add(DATUM, D("z"))}, split("z", [ab(I(1)), REL], [
         lane("kerb", walked("tread", "flight")),
         call("treads")]))},
    {"weight": 1, "when": {"cond": "otherwise"}, "body": {"op": "skip"}},
]

# Foot landing: paved at the middle street's walk; the place's body stands here.
rules["foot"] = rule(bind({"walk": DATUM}, lane("post", walked(
    "paving", "foot",
    mark={"anchor": "node-flight-2", "at": "floor_center", "facing": "north"}))))

# South plane: the street runs on at grade, the seam's whole face open.
rules["south"] = rule(split("x", [ab(P(f"handed/seam/{SOUTH}/x0")), ab(span(SOUTH, "x")), REL], [
    call("air"),
    split("y", [ab(P(f"handed/seam/{SOUTH}/y0")), ab(span(SOUTH, "y")), REL],
          [call("air"), claim("seam-south"), call("air")]),
    call("air")]))

rules["place"] = rule(split("z", [
    ab(span(NORTH, "z")),
    ab(I(1)),
    ab(sub(RISE, I(1))),
    REL,
    ab(span(SOUTH, "z")),
], [call("head"), call("top-tread"), call("treads"), call("foot"), call("south")]))

program = {
    "version": "1.9.0",
    "name": "saltstair-a-flight-2",
    "start": "place",
    "params": params,
    "palette": {
        "fill": "minecraft:stone_bricks",
        "paving": [
            {"weight": 6, "block": "minecraft:cobblestone"},
            {"weight": 1, "block": "minecraft:mossy_cobblestone"},
        ],
        "tread": {"local": "minecraft:stone_brick_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]"},
        "kerb": [
            {"weight": 6, "block": "minecraft:stone_bricks"},
            {"weight": 2, "block": "minecraft:mossy_stone_bricks"},
            {"weight": 1, "block": "minecraft:cracked_stone_bricks"},
        ],
        "kerb_wall": {"local": "minecraft:stone_brick_wall[east=none,north=low,south=low,up=false,waterlogged=false,west=none]"},
        "post_wall": "minecraft:stone_brick_wall[east=none,north=none,south=none,up=true,waterlogged=false,west=none]",
        "lamp": "minecraft:lantern[hanging=false,waterlogged=false]",
    },
    "contract": {
        "entry": "foot",
        "spaces": {"foot": {"envelope": "open"}, "head": {"envelope": "open"}},
        "no_body": {"lamp-caps": {"reason": "the top of a lantern on a kerb post, which nobody climbs onto"}},
        "edges": [
            {"a": "foot", "b": "exterior", "class": "walk", "via": "seam-south"},
            {"a": "foot", "b": "head", "class": "stair", "rise": params[f"handed/seam/{NORTH}/rise"], "via": "flight"},
            {"a": "head", "b": "exterior", "class": "walk", "via": "seam-north"},
        ],
    },
    # The kerb walls and their lantern posts stand in the ring columns on the
    # east and west, a stone-brick parapet above the stepped turf on either
    # side of the flight: finished exterior masonry, meant to be seen from the
    # hillside beside the street (grammar.md section 2f; DW0885).
    "shown_faces": ["east", "west"],
    "rules": rules,
}

out = CAMPAIGN / "programs" / "flight-2.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(program, indent=2, sort_keys=True) + "\n")
print(out, file=sys.stderr)
