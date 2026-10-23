#!/usr/bin/env python3
"""Emit programs/smithy.json — the grammar program for node/smithy.

Provenance only: the emitted JSON is the artifact of record. Every handed value
is read from `delvec allocation` and written as a `handed/...` parameter
default; the rules read those parameters and never a retyped number.

Usage: smithy.py <delvec> <campaign-dir>
"""
import json
import subprocess
import sys
from pathlib import Path

DELVEC, CAMPAIGN = sys.argv[1], Path(sys.argv[2])
alloc = json.loads(subprocess.run(
    [DELVEC, "allocation", str(CAMPAIGN), "node/smithy"],
    check=True, capture_output=True, text=True).stdout)

seam = next(s for s in alloc["seams"] if s["edge"] == "edge/upper-street-smithy")
(sx0, sy0, sz0), (sx1, sy1, sz1) = seam["cells"]
SEAM = "upper-street-smithy"


# ---------------------------------------------------------------- helpers
def P(name):
    return {"expr": "param", "name": name}


def I(n):
    return {"expr": "int", "value": n}


def add(a, b):
    return {"expr": "arith", "op": "add", "lhs": a, "rhs": b}


def sub(a, b):
    return {"expr": "arith", "op": "sub", "lhs": a, "rhs": b}


def D(axis):
    return {"expr": "dim", "dim": axis}


def A(e):
    if isinstance(e, int):
        e = I(e)
    return {"size": "absolute", "blocks": e}


def R(w=1):
    return {"size": "relative", "weight": I(w)}


def split(axis, sizes, children):
    return {"op": "split", "axis": axis, "sizes": sizes, "children": children}


def fill(role):
    return {"op": "fill", "material": {"role": role}}


SKIP = {"op": "skip"}
VOID = {"op": "void"}


def call(sym):
    return {"op": "call", "symbol": sym}


def claim(region, body):
    return {"op": "claim", "region": region, "body": body}


def bind(body, palette=None, params=None):
    n = {"op": "bind", "body": body}
    if palette:
        n["palette"] = {k: {"role": v} for k, v in palette.items()}
    if params:
        n["params"] = params
    return n


def rule(body, when=None):
    alt = {"weight": 1, "body": body}
    if when is not None:
        alt["when"] = when
    return alt


def cmp(lhs, op, rhs):
    return {"cond": "cmp", "lhs": lhs, "op": op, "rhs": rhs}


def all_(*c):
    return {"cond": "all", "of": list(c)}


OTHERWISE = {"cond": "otherwise"}

E = P("handed/roof/eaves")
RING = add(E, I(1))  # eave cell + wall plane
CW = P("chimney_w")


def place(points, size, default=VOID):
    """A box of the given local size with single cells painted at points.

    points: {(x, y, z): node}. Creative positions inside the room, in the room
    scope's own coordinates (none of them is a handed value)."""
    sx, sy, sz = size

    def along(axis, n, items, inner):
        # items: sorted distinct coordinates that carry something
        if not items:
            return default
        sizes, children, cur = [], [], 0
        for c in items:
            if c > cur:
                sizes.append(A(c - cur))
                children.append(default)
            sizes.append(A(1))
            children.append(inner(c))
            cur = c + 1
        sizes.append(R())
        children.append(default)
        return split(axis, sizes, children)

    xs = sorted({p[0] for p in points})

    def at_x(x):
        zs = sorted({p[2] for p in points if p[0] == x})

        def at_z(z):
            ys = sorted({p[1] for p in points if p[0] == x and p[2] == z})
            return along("y", sy, ys, lambda y: points[(x, y, z)])
        return along("z", sz, zs, at_z)
    return along("x", sx, xs, at_x)


# ---------------------------------------------------------------- palette
pane = "minecraft:glass_pane[east={e},north={n},south={s},waterlogged=false,west={w}]"
palette = {
    "floor": [
        {"weight": 6, "block": "minecraft:cobblestone"},
        {"weight": 3, "block": "minecraft:stone"},
        {"weight": 1, "block": "minecraft:andesite"},
    ],
    "plinth": [
        {"weight": 7, "block": "minecraft:stone_bricks"},
        {"weight": 2, "block": "minecraft:cobblestone"},
        {"weight": 1, "block": "minecraft:cracked_stone_bricks"},
    ],
    "infill": "minecraft:calcite",
    "post": "minecraft:spruce_log[axis=y]",
    "lintel_z": "minecraft:stripped_spruce_log[axis=z]",
    "sill": "minecraft:polished_andesite",
    # the forge window on the street: an open front barred, because any other
    # air in this wall is a second way out the plan did not allocate
    "hatch": "minecraft:iron_bars[east=false,north=true,south=true,waterlogged=false,west=false]",
    # panes run along the wall's own local x (see `run`)
    "pane": {"local": pane.format(e="true", n="false", s="false", w="true")},
    "chimney": [
        {"weight": 5, "block": "minecraft:stone_bricks"},
        {"weight": 3, "block": "minecraft:cobblestone"},
        {"weight": 1, "block": "minecraft:mossy_cobblestone"},
    ],
    "plank": "minecraft:spruce_planks",
    "lid": "minecraft:spruce_planks",
    "gable_in": "minecraft:air",
    "nothing": "minecraft:air",
    "gable": "minecraft:calcite",
    "cap": "minecraft:dark_oak_planks",
    "roof_e": "minecraft:dark_oak_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]",
    "roof_w": "minecraft:dark_oak_stairs[facing=west,half=bottom,shape=straight,waterlogged=false]",
    "lamp": "minecraft:lantern[hanging=true,waterlogged=false]",
    "crucible": "minecraft:campfire[facing=west,lit=true,signal_fire=false,waterlogged=false]",
    "quench": "minecraft:water_cauldron[level=3]",
    "anvil": "minecraft:anvil[facing=north]",
    "grindstone": "minecraft:grindstone[face=floor,facing=north]",
    "smithing": "minecraft:smithing_table",
    "bench": "minecraft:spruce_slab[type=bottom,waterlogged=false]",
}

# ---------------------------------------------------------------- rules
rules = {}

# whole frame: ground course | storey | roof
rules["smithy"] = [rule(split("y", [
    A(P("handed/datum-y")),
    A(sub(P("handed/roof/lid-y"), P("handed/datum-y"))),
    R(),
], [call("ground"), call("storey"), call("roof")]))]

# ground course: the plot inside the ring is the smithy's floor
rules["ground"] = [rule(split("x", [A(RING), R(), A(RING)], [
    SKIP,
    split("z", [A(RING), R(), A(RING)], [SKIP, fill("floor"), SKIP]),
    SKIP,
]))]

# ------------------------------------------------ storey (datum .. lid)
rules["storey"] = [rule(split("x", [A(E), A(1), R(), A(1), A(E)], [
    SKIP, call("west_wall"), call("mid"), call("east_wall"), SKIP,
]))]

# wall columns
rules["wall_col"] = [rule(split("y", [A(P("plinth_h")), R()],
                                [fill("plinth"), fill("infill")]))]
rules["win_col"] = [rule(split("y", [A(1), A(2), R()],
                               [fill("plinth"), fill("pane"), fill("infill")]))]
# a run of wall along its own local x, two windows in it; a wall running along
# world z calls it turned (reorient), never a copy
rules["run"] = [rule(split("x", [R(), A(1), A(2), A(1), R()], [
    call("wall_col"), call("win_col"), call("wall_col"),
    call("win_col"), call("wall_col"),
]))]
TURNED_RUN = {"op": "reorient", "orient": {"x": "local_z"}, "body": call("run")}

rules["west_wall"] = [rule(split("z", [A(E), A(1), R(), A(1), A(E)], [
    SKIP, fill("post"), TURNED_RUN,
    fill("post"), SKIP,
]))]

# east wall: the street front — hatch, door, chimney
rules["east_wall"] = [rule(split("z", [
    A(P(f"handed/seam/{SEAM}/z0")),
    A(add(sub(P(f"handed/seam/{SEAM}/z1"), P(f"handed/seam/{SEAM}/z0")), I(1))),
    R(),
], [call("east_n"), call("door_col"), call("east_s")]))]

rules["east_n"] = [rule(split("z", [A(E), A(1), R()], [
    SKIP, fill("post"), call("hatch"),
]))]
rules["hatch"] = [rule(split("y", [A(1), A(2), R()], [
    fill("sill"), fill("hatch"), fill("lintel_z"),
]))]
# the door, and its lantern hung from the lintel in the reveal above it
rules["door_col"] = [rule(split("y", [
    A(add(sub(P(f"handed/seam/{SEAM}/y1"), P(f"handed/seam/{SEAM}/y0")), I(1))),
    A(1),
    R(),
], [claim("east-door", VOID), fill("lamp"), fill("lintel_z")]))]
rules["east_s"] = [rule(split("z", [R(), A(CW), A(1), A(E)], [
    call("wall_col"), fill("chimney"), fill("post"), SKIP,
]))]

# middle band: north wall | room | south wall
rules["mid"] = [rule(split("z", [A(E), A(1), R(), A(1), A(E)], [
    SKIP,
    call("run"),
    call("room"),
    call("run"),
    SKIP,
]))]

# the room: the play space, the smith's floor
room_points = {
    # west strip: grindstone, smithing table, a bench
    (0, 0, 1): fill("grindstone"),
    (0, 0, 3): fill("smithing"),
    (0, 0, 5): fill("bench"),
    (0, 0, 6): fill("bench"),
    # anvil before the forge, quench trough beside it
    (5, 0, 6): fill("anvil"),
    (6, 0, 5): fill("quench"),
    # lanterns hung from the ceiling
    (2, 3, 2): fill("lamp"),
    (3, 3, 6): fill("lamp"),
    (6, 3, 4): fill("lamp"),
}
rules["room"] = [rule(claim("smithy", {
    "op": "mark",
    "mark": {"anchor": "node-smithy", "at": "offset", "facing": "east",
             "x": I(4), "y": I(0), "z": I(3)},
    "body": split("x", [R(), A(1)], [
        place(room_points, (7, 4, 8)),
        call("east_strip"),
    ]),
}))]
# x = last column of the room, against the street wall: the forge at its south end
rules["east_strip"] = [rule(split("z", [R(), A(CW)], [
    VOID,
    split("y", [A(1), A(1), R()], [fill("crucible"), VOID, fill("chimney")]),
]))]

# ------------------------------------------------ roof (lid .. top)
rules["roof"] = [rule(claim("roof", split("z", [A(E), A(1), R(), A(1), A(E)], [
    bind(call("roof_band"), palette={"lid": "nothing", "gable_in": "nothing"}),
    bind(call("roof_band"), palette={"gable_in": "gable"}),
    split("z", [R(), A(CW)], [
        call("roof_band"),
        bind(call("roof_band"), params={"chim": I(1)}),
    ]),
    bind(call("roof_band"), palette={"gable_in": "gable"}),
    bind(call("roof_band"), palette={"lid": "nothing", "gable_in": "nothing"}),
])))]

rules["roof_band"] = [rule(split("y", [A(1), R()], [
    call("lid_course"),
    split("x", [A(E), R(), A(E)], [SKIP, call("slope"), SKIP]),
]))]

rules["lid_course"] = [rule(split("x", [A(E), R(), A(E)], [
    fill("roof_e"), call("lid_mid"), fill("roof_w"),
]))]
rules["lid_mid"] = [
    rule(split("x", [R(), A(CW)], [fill("lid"), fill("chimney")]),
         when=cmp(P("chim"), "eq", I(1))),
    rule(fill("lid"), when=OTHERWISE),
]

CHIM_LVL = cmp(P("chim"), "eq", I(1))
# one course of the slope, then the next course one cell in on each side
rules["slope"] = [
    rule(split("y", [A(1), R()], [
        call("course"),
        split("x", [A(1), R(), A(1)], [
            SKIP,
            bind(call("slope"), params={"lvl": add(P("lvl"), I(1))}),
            call("margin_e"),
        ]),
    ]), when=all_(cmp(D("y"), "ge", I(2)), cmp(D("x"), "ge", I(4)))),
    rule(split("x", [A(1), R(), A(1)], [fill("roof_e"), fill("cap"), fill("roof_w")]),
         when=all_(cmp(D("y"), "eq", I(1)), cmp(D("x"), "ge", I(3)))),
    rule(fill("cap"), when=OTHERWISE),
]
# the column the next course steps in from on the east side: the chimney
# stack stands in it at the first CW levels of the chimney band
rules["margin_e"] = [
    rule(fill("chimney"), when=all_(CHIM_LVL, cmp(P("lvl"), "lt", CW))),
    rule(SKIP, when=OTHERWISE),
]
rules["course"] = [
    rule(split("x", [A(1), R(), A(1)], [
        fill("roof_e"), call("attic_row"), call("course_e"),
    ])),
]
rules["course_e"] = [
    rule(fill("chimney"), when=all_(CHIM_LVL, cmp(P("lvl"), "lt", CW))),
    rule(fill("roof_w"), when=OTHERWISE),
]
rules["attic_row"] = [
    rule(split("x", [R(), A(sub(CW, add(P("lvl"), I(1))))], [
        fill("gable_in"), fill("chimney"),
    ]), when=all_(CHIM_LVL, cmp(add(P("lvl"), I(1)), "lt", CW))),
    rule(fill("gable_in"), when=OTHERWISE),
]

params = {
    "handed/datum-y": alloc["datum_y"],
    "handed/roof/eaves": alloc["roof"]["eaves"],
    "handed/roof/lid-y": alloc["roof"]["lid_y"],
    f"handed/seam/{SEAM}/y0": sy0,
    f"handed/seam/{SEAM}/y1": sy1,
    f"handed/seam/{SEAM}/z0": sz0,
    f"handed/seam/{SEAM}/z1": sz1,
    "plinth_h": 2,
    "chimney_w": 2,
    "chim": 0,
    "lvl": 0,
}

program = {
    "version": "1.9.0",
    "name": "saltstair-a-smithy",
    "start": "smithy",
    "params": params,
    "palette": palette,
    "rules": rules,
    "contract": {
        "entry": "smithy",
        "spaces": {"smithy": {"envelope": "enclosed"}},
        "no_body": {"roof": {"reason": "the shingle roof and the loft under it, which nobody is meant to walk"}},
        "no_body_majority_ack": "a house that owns its outside owns its roof, and a pitched roof is more standable surface than the room under it; nobody walks it",
        "edges": [{"a": "exterior", "b": "smithy", "class": "walk", "via": "east-door"}],
    },
    "shown_faces": ["north", "south", "up", "west"],
}

out = CAMPAIGN / "programs" / "smithy.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(program, indent=2) + "\n")
print(out)
