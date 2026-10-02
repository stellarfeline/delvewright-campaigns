#!/usr/bin/env python3
"""Writes whale-fall.program.json — the grammar program for the whale-fall skeleton.

This script only spells JSON: every node it emits is a grammar construct the
engine reads, expands and judges (`delvec grammar check|expand`). It places no
block and computes no geometry; it exists because the program is ~40 rules of
deeply nested expressions and a typo in hand-written JSON is the likeliest bug.

Region: 45 (X, width) x 48 (Y) x 128 (Z, length). Head at low Z (north),
tail at high Z (south). Usage: python3 build_program.py > whale-fall.program.json
"""

import json
import sys

# --- expressions -------------------------------------------------------------


def I(v):
    return {"expr": "int", "value": v}


def P(n):
    return {"expr": "param", "name": n}


def D(a):
    return {"expr": "dim", "dim": a}


def ar(lhs, op, rhs):
    lhs = I(lhs) if isinstance(lhs, int) else lhs
    rhs = I(rhs) if isinstance(rhs, int) else rhs
    return {"expr": "arith", "lhs": lhs, "op": op, "rhs": rhs}


def cmp(lhs, op, rhs):
    lhs = I(lhs) if isinstance(lhs, int) else lhs
    rhs = I(rhs) if isinstance(rhs, int) else rhs
    return {"cond": "cmp", "lhs": lhs, "op": op, "rhs": rhs}


def all_(*c):
    return {"cond": "all", "of": list(c)}


OTHERWISE = {"cond": "otherwise"}

# --- sizes and nodes ----------------------------------------------------------


def A(n):
    return {"size": "absolute", "blocks": I(n) if isinstance(n, int) else n}


def R(w=1):
    return {"size": "relative", "weight": I(w)}


def split(axis, sizes, children, rounding=None, repeat=False):
    node = {"op": "split", "axis": axis, "sizes": sizes, "children": children}
    if rounding:
        node["rounding"] = rounding
    if repeat:
        node["repeat"] = True
    return node


def fill(role):
    return {"op": "fill", "material": {"role": role}}


VOID = {"op": "void"}


def call(s):
    return {"op": "call", "symbol": s}


def bind(params, body):
    return {"op": "bind", "params": params, "body": body}


def mirror(axes, body):
    return {"op": "reorient", "orient": {"mirror": {a: True for a in axes}}, "body": body}


def mark(anchor, x, y, z, facing, body):
    return {
        "op": "mark",
        "mark": {"anchor": anchor, "at": "offset", "x": I(x), "y": I(y), "z": I(z), "facing": facing},
        "body": body,
    }


def alt(body, when=None, weight=1):
    a = {"weight": weight, "body": body}
    if when is not None:
        a["when"] = when
    return a


def one(body):
    return [alt(body)]


# --- the program ----------------------------------------------------------------

N1 = ar(P("n"), "add", 1)
rules = {}

# Top level: the whale, head to tail, along Z.
rules["whale"] = one(
    split(
        "z",
        [A(30), A(4), A(40), A(24), A(30)],
        [call("skull"), call("neck"), call("thorax"), call("lumbar"), call("tail")],
    )
)

# ---- the spine, shared by neck / thorax / lumbar --------------------------------
# A vertebra is 3 blocks of centrum and 1 of disc, repeated. The walkway is the
# centrum's top course (7 wide); the disc is inset one block a side below its top
# course so the segmentation reads from the flank while the walkway stays whole.
rules["centrum_band"] = one(
    split("z", [A(3), A(1)], [fill("spine"), call("disc")], repeat=True)
)
rules["disc"] = one(
    split(
        "y",
        [R(), A(1)],
        [split("x", [A(1), R(), A(1)], [VOID, fill("cartilage"), VOID]), fill("cartilage")],
    )
)
# Two blades per vertebra at the walkway's edges (a departure from the single
# central neural spine, so the walkway between them stays clear).
rules["blade_band"] = one(
    split(
        "z",
        [A(3), A(1)],
        [
            split(
                "z",
                [A(1), A(1), A(1)],
                [VOID, split("x", [A(1), R(), A(1)], [fill("spine"), VOID, fill("spine")]), VOID],
            ),
            VOID,
        ],
        repeat=True,
    )
)


def spine_column(below, blade):
    """X-centred 7-wide spine over a 45-wide box; `below` is the node under it."""
    return split(
        "y",
        [A(28), A(5), A(blade), R()],
        [
            below,
            split("x", [A(19), A(7), R()], [VOID, call("centrum_band"), VOID]),
            split("x", [A(19), A(7), R()], [VOID, call("blade_band"), VOID]),
            VOID,
        ],
    )


rules["neck"] = one(
    mark("skull-rear", 22, 33, 3, "north", spine_column(VOID, 2))
)

# ---- thorax: ribs, catwalk, flippers ----------------------------------------------
rules["thorax"] = one(
    mark(
        "cage",
        22,
        13,
        25,
        "north",
        split(
            "x",
            [A(6), A(33), A(6)],
            [
                mirror("x", call("flipper_margin")),
                call("thorax_middle"),
                call("flipper_margin"),
            ],
        ),
    )
)
rules["thorax_middle"] = one(
    split(
        "y",
        [A(7), A(21), A(5), A(4), R()],
        [
            VOID,
            call("rib_band"),
            split("x", [A(13), A(7), A(13)], [VOID, call("centrum_band"), VOID]),
            split("x", [A(13), A(7), A(13)], [VOID, call("blade_band"), VOID]),
            VOID,
        ],
    )
)
# The largest rib pair is mid-thorax; each half tapers outward from the middle.
rules["rib_band"] = one(
    split(
        "z",
        [R(), R()],
        [
            mirror("z", call("rib_half")),
            split("z", [A(2), R()], [call("gap_slice"), call("rib_half")]),
        ],
    )
)
rules["rib_half"] = [
    alt(
        split(
            "z",
            [A(2), A(2), R()],
            [
                call("rib_slice"),
                call("gap_slice"),
                split(
                    "x",
                    [A(1), R(), A(1)],
                    [VOID, split("y", [A(1), R()], [VOID, call("rib_half")]), VOID],
                ),
            ],
        ),
        when=cmp(D("z"), "ge", 4),
    ),
    alt(call("gap_slice"), when=all_(cmp(D("z"), "ge", 1), cmp(D("z"), "lt", 4))),
    alt(VOID, when=OTHERWISE),
]
# Between ribs only the catwalk runs, pinned to the band's top so it holds one
# world height whatever the rib's own taper did to the bottom.
rules["gap_slice"] = one(
    split(
        "y",
        [R(), A(1), A(15)],
        [VOID, split("x", [R(), A(5), R()], [VOID, fill("walk"), VOID]), VOID],
    )
)
# One rib pair, in cross-section: a lower half (courses from the equator down,
# mirrored) and an upper half of 11 courses (equator up to the cap under the spine).
rules["rib_slice"] = one(
    split(
        "y",
        [R(), A(11)],
        [
            mirror("y", bind({"n": I(0), "lower": I(1)}, call("ring"))),
            bind({"n": I(0), "lower": I(0)}, call("ring")),
        ],
    )
)
S = ar(P("n"), "div", 3)  # the inset after course n
B = ar(I(2), "max", ar(S, "add", 1))  # the rib's thickness at course n
rules["ring"] = [
    alt(
        split("y", [A(1), R()], [call("ring_course"), call("ring_step")], rounding="start"),
        when=all_(cmp(D("y"), "ge", 2), cmp(D("x"), "ge", ar(ar(B, "mul", 2), "add", 2))),
    ),
    alt(
        call("ring_course"),
        when=all_(
            cmp(P("lower"), "eq", 1),
            cmp(D("x"), "ge", ar(ar(B, "mul", 2), "add", 1)),
            {"cond": "any", "of": [cmp(D("y"), "lt", 2), cmp(D("x"), "lt", ar(ar(B, "mul", 2), "add", 2))]},
        ),
    ),
    alt(fill("bone"), when=OTHERWISE),
]
rules["ring_course"] = [
    alt(
        split("x", [A(B), R(), A(B)], [fill("bone"), fill("walk"), fill("bone")]),
        when=all_(cmp(P("lower"), "eq", 1), cmp(P("n"), "eq", P("walk_n"))),
    ),
    alt(split("x", [A(B), R(), A(B)], [fill("bone"), VOID, fill("bone")]), when=OTHERWISE),
]
rules["ring_step"] = one(
    split("x", [A(S), R(), A(S)], [VOID, bind({"n": N1}, call("ring")), VOID])
)

# A flipper hangs from the shoulder at the front of the thorax. Local low X is the
# side toward the body (the left margin is mirrored), courses run top-down.
rules["flipper_margin"] = one(
    split(
        "z",
        [A(2), A(12), R()],
        [
            VOID,
            split("y", [A(2), A(16), R()], [VOID, mirror("y", bind({"n": I(0)}, call("flipper"))), VOID]),
            VOID,
        ],
    )
)
rules["flipper"] = [
    alt(
        split("y", [A(1), R()], [call("flipper_course"), bind({"n": N1}, call("flipper"))], rounding="start"),
        when=cmp(D("y"), "ge", 2),
    ),
    alt(call("flipper_course"), when=OTHERWISE),
]
XO = ar(I(5), "min", ar(P("n"), "div", 3))
ZO = ar(I(5), "min", ar(P("n"), "div", 2))
rules["flipper_course"] = [
    alt(  # humerus
        split("x", [A(XO), A(3), R()], [VOID, split("z", [A(ZO), A(3), R()], [VOID, fill("bone"), VOID]), VOID]),
        when=cmp(P("n"), "lt", 4),
    ),
    alt(  # radius and ulna
        split(
            "x",
            [A(XO), A(2), R()],
            [VOID, split("z", [A(ZO), A(1), A(1), A(1), R()], [VOID, fill("bone"), VOID, fill("bone"), VOID]), VOID],
        ),
        when=all_(cmp(P("n"), "ge", 4), cmp(P("n"), "lt", 9)),
    ),
    alt(  # four digits
        split(
            "x",
            [A(XO), A(1), R()],
            [
                VOID,
                split(
                    "z",
                    [A(ZO), A(1), A(1), A(1), A(1), A(1), A(1), A(1), R()],
                    [VOID, fill("bone"), VOID, fill("bone"), VOID, fill("bone"), VOID, fill("bone"), VOID],
                ),
                VOID,
            ],
        ),
        when=OTHERWISE,
    ),
]

# ---- lumbar: tall blades, transverse processes, the pilgrims' stair ----------------
# Columns across X: margin 6 | left 13 | spine 7 | processes 5 | stair lane 3 | rest 11.
rules["lumbar"] = one(
    mark(
        "spine-walk",
        22,
        33,
        18,
        "north",
        split(
            "x",
            [A(6), A(13), A(7), A(5), A(3), A(11)],
            [
                VOID,
                mirror("x", call("process_column")),
                call("lumbar_spine"),
                call("process_column_stair"),
                call("stair_lane"),
                VOID,
            ],
        ),
    )
)
rules["lumbar_spine"] = one(
    split(
        "y",
        [A(12), A(1), A(15), A(5), A(6), R()],
        [
            VOID,
            split("z", [A(3), R()], [split("x", [A(1), A(5), A(1)], [fill("walk"), fill("walk"), fill("walk")]), VOID]),
            VOID,
            call("centrum_band"),
            call("blade_band"),
            VOID,
        ],
    )
)
PROCESS = split(
    "z",
    [A(3), A(1)],
    [split("z", [A(1), A(1), A(1)], [VOID, split("y", [A(2), A(1), A(2)], [VOID, fill("spine"), VOID]), VOID]), VOID],
    repeat=True,
)
# Left side (mirrored): 8 air then 5 of process, low X toward the spine after mirroring.
rules["process_column"] = one(
    split("y", [A(28), A(5), R()], [VOID, split("x", [A(5), R()], [PROCESS, VOID]), VOID])
)
# Right side: processes, the low landing at the catwalk's height, the top landing.
rules["process_column_stair"] = one(
    split(
        "y",
        [A(12), A(1), A(15), A(5), R()],
        [
            VOID,
            split("z", [A(3), R()], [fill("walk"), VOID]),
            VOID,
            split("z", [A(23), A(1)], [PROCESS, split("y", [A(4), A(1)], [VOID, fill("walk")])]),
            VOID,
        ],
    )
)
rules["stair_lane"] = one(
    split(
        "y",
        [A(12), A(1), R()],
        [
            VOID,
            split("z", [A(3), R()], [fill("walk"), VOID]),
            split(
                "z",
                [A(3), A(20), A(1)],
                [
                    VOID,
                    split("y", [A(20), R()], [call("stair"), VOID]),
                    split("y", [A(19), A(1), R()], [VOID, fill("walk"), VOID]),
                ],
            ),
        ],
    )
)
rules["stair"] = [
    alt(
        split(
            "z",
            [A(1), R()],
            [
                split("y", [A(1), R()], [fill("stair_south"), VOID]),
                split("y", [A(1), R()], [fill("walk"), call("stair")]),
            ],
        ),
        when=cmp(D("z"), "ge", 2),
    ),
    alt(split("y", [A(1), R()], [fill("stair_south"), VOID]), when=OTHERWISE),
]

# ---- tail: caudal vertebrae shrinking toward the tip, chevrons below ----------------
rules["tail"] = one(
    split(
        "x",
        [A(19), A(7), R()],
        [
            VOID,
            split("y", [A(26), A(7), R()], [VOID, bind({"n": I(0)}, call("caudal")), VOID]),
            VOID,
        ],
    )
)
ODD = cmp(ar(P("n"), "rem", 2), "eq", 1)
rules["caudal"] = [
    alt(
        split(
            "z",
            [A(3), A(1), R()],
            [call("caudal_vertebra"), call("caudal_disc"), call("caudal_rest")],
        ),
        when=all_(cmp(D("z"), "ge", 4), cmp(D("y"), "ge", 3)),
    ),
    alt(VOID, when=OTHERWISE),
]
rules["caudal_vertebra"] = one(
    split(
        "y",
        [A(2), R()],
        [
            split("z", [A(1), A(1), A(1)], [VOID, split("x", [R(), A(1), R()], [VOID, fill("bone"), VOID]), VOID]),
            fill("spine"),
        ],
    )
)
# A disc after an odd vertebra is where the walkway drops a course: its top is a
# stair, ascending north toward the head, flush with this vertebra's top.
rules["caudal_disc"] = [
    alt(
        split("y", [A(2), R(), A(1)], [VOID, fill("cartilage"), fill("stair_north")]),
        when=ODD,
    ),
    alt(split("y", [A(2), R()], [VOID, fill("cartilage")]), when=OTHERWISE),
]
rules["caudal_rest"] = [
    alt(
        split(
            "y",
            [R(), A(1)],
            [split("x", [A(1), R(), A(1)], [VOID, bind({"n": N1}, call("caudal")), VOID]), VOID],
        ),
        when=all_(ODD, cmp(D("x"), "ge", 3)),
    ),
    alt(bind({"n": N1}, call("caudal")), when=OTHERWISE),
]

# ---- skull: braincase holding the temple, rostrum, open lower jaw -------------------
rules["skull"] = one(
    mark(
        "temple",
        22,
        33,
        26,
        "north",
        split(
            "y",
            [A(7), A(11), A(27), R()],
            [VOID, call("jaw_band"), call("skull_band"), VOID],
        ),
    )
)
rules["jaw_band"] = one(
    split(
        "x",
        [A(17), R(), A(17)],
        [mirror("x", call("mandible_zone")), VOID, call("mandible_zone")],
    )
)
rules["mandible_zone"] = one(
    split("z", [A(28), R()], [mirror("z", bind({"n": I(0)}, call("mandible"))), VOID])
)
OFF = ar(
    ar(I(3), "add", ar(ar(P("n"), "mul", 11), "div", 4)),
    "min",
    ar(I(14), "sub", ar(ar(ar(P("n"), "sub", 4), "mul", 11), "div", 4)),
)
OFF = ar(I(0), "max", OFF)
rules["mandible"] = [
    alt(
        split(
            "z",
            [A(3), R()],
            [
                split(
                    "x",
                    [A(OFF), A(2), R()],
                    [VOID, split("y", [R(), A(ar(I(3), "min", D("y")))], [VOID, fill("bone")]), VOID],
                ),
                split("y", [R(), A(1)], [bind({"n": N1}, call("mandible")), VOID]),
            ],
        ),
        when=all_(cmp(D("z"), "ge", 3), cmp(D("y"), "ge", 2)),
    ),
    alt(VOID, when=OTHERWISE),
]
rules["skull_band"] = one(
    split("z", [A(16), A(14)], [call("rostrum_box"), call("braincase_box")])
)
rules["rostrum_box"] = one(
    split(
        "y",
        [A(13), R()],
        [split("x", [A(10), A(25), A(10)], [VOID, mirror("z", call("rostrum")), VOID]), VOID],
    )
)
rules["rostrum"] = [
    alt(
        split(
            "z",
            [A(2), R()],
            [
                fill("bone"),
                split("x", [A(1), R(), A(1)], [VOID, split("y", [R(), A(1)], [call("rostrum"), VOID]), VOID]),
            ],
        ),
        when=all_(cmp(D("z"), "ge", 2), cmp(D("x"), "ge", 3), cmp(D("y"), "ge", 2)),
    ),
    alt(fill("bone"), when=OTHERWISE),
]
rules["braincase_box"] = one(
    split("x", [A(9), A(27), A(9)], [VOID, call("braincase"), VOID])
)
rules["braincase"] = one(
    split(
        "y",
        [A(6), A(8), A(1), A(6), R()],
        [
            mirror("y", call("taper_solid")),
            fill("bone"),
            split(
                "x",
                [A(2), R(), A(2)],
                [fill("bone"), split("z", [A(2), R(), A(2)], [fill("bone"), fill("paving"), fill("bone")]), fill("bone")],
            ),
            call("chamber_walls"),
            call("vault"),
        ],
    )
)
# The underside: a solid taper, one block in a side per course.
rules["taper_solid"] = [
    alt(
        split(
            "y",
            [A(1), R()],
            [fill("bone"), split("x", [A(1), R(), A(1)], [VOID, call("taper_solid"), VOID])],
            rounding="start",
        ),
        when=all_(cmp(D("x"), "ge", 5), cmp(D("y"), "ge", 2)),
    ),
    alt(fill("bone"), when=OTHERWISE),
]
rules["chamber_walls"] = one(
    split(
        "x",
        [A(2), R(), A(2)],
        [
            call("side_wall"),
            split("z", [A(2), R(), A(2)], [fill("bone"), call("temple"), call("rear_wall")]),
            call("side_wall"),
        ],
    )
)
# The foramen magnum: the hole the spinal cord ran through is the way in from the spine.
rules["rear_wall"] = one(
    split("x", [R(), A(5), R()], [fill("bone"), split("y", [A(3), R()], [VOID, fill("bone")]), fill("bone")])
)
# The orbits: an eye socket each side lets light into the temple.
rules["side_wall"] = one(
    split("z", [A(3), A(3), R()], [fill("bone"), split("y", [A(3), A(3)], [fill("bone"), VOID]), fill("bone")])
)
# Temple interior 23 x 6 x 10: dais at the north end, a flight onto it, two rows of columns.
rules["temple"] = one(
    split(
        "z",
        [A(3), A(1), R()],
        [
            split("y", [A(1), R()], [split("x", [A(6), A(11), A(6)], [VOID, fill("paving"), VOID]), VOID]),
            split("y", [A(1), R()], [split("x", [A(6), A(11), A(6)], [VOID, fill("stair_north_stone"), VOID]), VOID]),
            split("z", [A(1), A(1), A(3), A(1), R()], [VOID, call("column_row"), VOID, call("column_row"), VOID]),
        ],
    )
)
rules["column_row"] = one(
    split("x", [A(4), A(1), A(13), A(1), A(4)], [VOID, call("column"), VOID, call("column"), VOID])
)
rules["column"] = one(
    split("y", [A(4), A(1), R()], [fill("column"), fill("lamp"), fill("column_ruin")])
)
# The cranial vault: a hollow taper across X between solid gable ends.
rules["vault"] = one(
    split("z", [A(2), R(), A(2)], [call("taper_solid_up"), call("vault_ring"), call("taper_solid_up")])
)
rules["taper_solid_up"] = [
    alt(
        split(
            "y",
            [A(1), R()],
            [fill("bone"), split("x", [A(2), R(), A(2)], [VOID, call("taper_solid_up"), VOID])],
            rounding="start",
        ),
        when=all_(cmp(D("x"), "ge", 5), cmp(D("y"), "ge", 2)),
    ),
    alt(fill("bone"), when=OTHERWISE),
]
rules["vault_ring"] = [
    alt(
        split(
            "y",
            [A(1), R()],
            [
                split("x", [A(3), R(), A(3)], [fill("bone"), VOID, fill("bone")]),
                split("x", [A(2), R(), A(2)], [VOID, call("vault_ring"), VOID]),
            ],
            rounding="start",
        ),
        when=all_(cmp(D("x"), "ge", 8), cmp(D("y"), "ge", 2)),
    ),
    alt(fill("bone"), when=OTHERWISE),
]

BONE_MIX = [
    {"weight": 6, "block": "minecraft:bone_block[axis=y]"},
    {"weight": 3, "block": "minecraft:calcite"},
    {"weight": 1, "block": "minecraft:diorite"},
]
program = {
    "version": "1.9.0",
    "name": "whale-fall",
    "start": "whale",
    "params": {"n": 0, "lower": 0, "walk_n": 4},
    "palette": {
        "bone": BONE_MIX,
        "spine": [
            {"weight": 7, "block": "minecraft:bone_block[axis=z]"},
            {"weight": 2, "block": "minecraft:calcite"},
            {"weight": 1, "block": "minecraft:diorite"},
        ],
        "cartilage": "minecraft:calcite",
        "walk": [
            {"weight": 5, "block": "minecraft:stone_bricks"},
            {"weight": 3, "block": "minecraft:mossy_stone_bricks"},
            {"weight": 2, "block": "minecraft:cracked_stone_bricks"},
        ],
        "paving": [
            {"weight": 5, "block": "minecraft:stone_bricks"},
            {"weight": 3, "block": "minecraft:mossy_stone_bricks"},
            {"weight": 2, "block": "minecraft:cracked_stone_bricks"},
        ],
        "column": "minecraft:chiseled_stone_bricks",
        "column_ruin": [
            {"weight": 3, "block": "minecraft:chiseled_stone_bricks"},
            {"weight": 2, "block": "minecraft:air"},
        ],
        "lamp": "minecraft:pearlescent_froglight[axis=y]",
        "stair_south": "minecraft:stone_brick_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]",
        "stair_north": "minecraft:smooth_quartz_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]",
        "stair_north_stone": "minecraft:stone_brick_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]",
    },
    "rules": rules,
}

json.dump(program, sys.stdout, indent=2, sort_keys=True)
sys.stdout.write("\n")
