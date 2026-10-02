#!/usr/bin/env python3
"""Writes whale-fall.program.json — the grammar program for the whale-fall skeleton.

This script only spells JSON: every node it emits is a grammar construct the
engine reads, expands and judges (`delvec grammar check|expand`). It places no
block and computes no geometry; it exists because the program is ~50 rules of
deeply nested expressions and a typo in hand-written JSON is the likeliest bug.

Region: 45 (X, width) x 48 (Y) x 128 (Z, length). Head at low Z (north),
tail at high Z (south). Usage: python3 build_program.py > whale-fall.program.json

Where a shape has to vary along its length (the skull's taper, the mandible's
bow, the rib cage's swell) the rule carries a counter `n` (or `k`) that a
self-call rebinds to n + 1 — the grammar's only index into a recursion — and
sizes are arithmetic over it.
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


def ex(v):
    return I(v) if isinstance(v, int) else v


def ar(lhs, op, rhs):
    return {"expr": "arith", "lhs": ex(lhs), "op": op, "rhs": ex(rhs)}


def cmp(lhs, op, rhs):
    return {"cond": "cmp", "lhs": ex(lhs), "op": op, "rhs": ex(rhs)}


def all_(*c):
    return {"cond": "all", "of": list(c)}


def any_(*c):
    return {"cond": "any", "of": list(c)}


OTHERWISE = {"cond": "otherwise"}

# --- sizes and nodes ----------------------------------------------------------


def A(n):
    return {"size": "absolute", "blocks": ex(n)}


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
    return {"op": "bind", "params": {k: ex(v) for k, v in params.items()}, "body": body}


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


def n_plus(name="n"):
    return ar(P(name), "add", 1)


# --- the program ----------------------------------------------------------------

rules = {}

# Top level: the whale, head to tail, along Z. Proportions follow a balaenopterid
# skeleton: skull ~23% of length, a short neck, a rib-bearing thorax, the lumbar
# run, and a caudal series shrinking to the tip (README, "Anatomy").
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
# The neural spine: one sagittal plate per vertebra on the midline, raked back —
# its upper half stands one block further tailward than its lower half. The
# walkway is the two 3-wide lanes either side of it.
PLATE = split("x", [R(), A(1), R()], [VOID, fill("spine"), VOID])
PLATE_LOW = split("z", [A(2), A(2)], [PLATE, VOID], repeat=True)
PLATE_HIGH = split("z", [A(1), A(2), A(1)], [VOID, PLATE, VOID], repeat=True)
rules["blade_band"] = one(split("y", [R(), R()], [PLATE_LOW, PLATE_HIGH], rounding="start"))


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


rules["neck"] = one(mark("skull-rear", 20, 33, 3, "north", spine_column(VOID, 2)))

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
            [mirror("x", call("flipper_margin")), call("thorax_middle"), call("flipper_margin")],
        ),
    )
)
rules["thorax_middle"] = one(
    split(
        "y",
        [A(7), A(21), A(5), A(4), R()],
        [
            VOID,
            bind({"k": 0}, call("ribs")),
            split("x", [A(13), A(7), A(13)], [VOID, call("centrum_band"), VOID]),
            split("x", [A(13), A(7), A(13)], [VOID, call("blade_band"), VOID]),
            VOID,
        ],
    )
)
# Ten rib pairs, one per 4-block bay. Bay k is inset by its distance from the
# largest pair (k = 5): narrower and shallower toward both ends of the thorax.
DIST = ar(ar(I(5), "sub", P("k")), "max", ar(P("k"), "sub", 5))
rules["ribs"] = [
    alt(
        split(
            "z",
            [A(4), R()],
            [
                split(
                    "x",
                    [A(DIST), R(), A(DIST)],
                    [VOID, split("y", [A(DIST), R()], [VOID, call("rib_bay")]), VOID],
                ),
                bind({"k": n_plus("k")}, call("ribs")),
            ],
        ),
        when=cmp(D("z"), "ge", 4),
    ),
    alt(VOID, when=OTHERWISE),
]
# One bay, in cross-section: a lower half (courses from the equator down, mirrored)
# and an upper half of 11 courses (equator up to the cap under the spine). The top
# is pinned, so the catwalk course (lower n = walk_n) holds one world height in
# every bay.
rules["rib_bay"] = one(
    split(
        "y",
        [R(), A(11)],
        [
            mirror("y", bind({"n": 0, "lower": 1}, call("ring"))),
            bind({"n": 0, "lower": 0}, call("ring")),
        ],
    )
)
S = ar(P("n"), "div", 3)  # the inset after course n
B = ar(I(2), "max", ar(S, "add", 1))  # the rib's thickness at course n
# The rake: the rib (one block thick) sits at z offset 0 near the spine, 1 at
# the equator and 2 at the tips — each rib sweeps tailward as it descends.
ZO = ar(
    ar(P("lower"), "mul", ar(I(2), "min", ar(I(1), "add", ar(P("n"), "div", 5)))),
    "add",
    ar(ar(I(1), "sub", P("lower")), "mul", ar(I(0), "max", ar(I(1), "sub", ar(P("n"), "div", 5)))),
)
RIB_CELL = split("z", [A(ZO), A(1), R()], [VOID, fill("bone"), VOID])
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
            any_(cmp(D("y"), "lt", 2), cmp(D("x"), "lt", ar(ar(B, "mul", 2), "add", 2))),
        ),
    ),
    alt(RIB_CELL, when=OTHERWISE),
]
# On the catwalk course the rib carries a stone beam across to the catwalk, which
# runs the whole bay; everywhere else the inside of the ring is air.
CATWALK_ROW = split(
    "x",
    [R(), A(5), R()],
    [
        split("z", [A(ZO), A(1), R()], [VOID, fill("walk"), VOID]),
        fill("walk"),
        split("z", [A(ZO), A(1), R()], [VOID, fill("walk"), VOID]),
    ],
)
rules["ring_course"] = [
    alt(
        split("x", [A(B), R(), A(B)], [RIB_CELL, CATWALK_ROW, RIB_CELL]),
        when=all_(cmp(P("lower"), "eq", 1), cmp(P("n"), "eq", P("walk_n"))),
    ),
    alt(split("x", [A(B), R(), A(B)], [RIB_CELL, VOID, RIB_CELL]), when=OTHERWISE),
]
rules["ring_step"] = one(split("x", [A(S), R(), A(S)], [VOID, bind({"n": n_plus()}, call("ring")), VOID]))

# A flipper hangs from the shoulder at the front of the thorax. Local low X is the
# side toward the body (the left margin is mirrored), courses run top-down.
rules["flipper_margin"] = one(
    split(
        "z",
        [A(2), A(12), R()],
        [
            VOID,
            split("y", [A(2), A(16), R()], [VOID, mirror("y", bind({"n": 0}, call("flipper"))), VOID]),
            VOID,
        ],
    )
)
rules["flipper"] = [
    alt(
        split("y", [A(1), R()], [call("flipper_course"), bind({"n": n_plus()}, call("flipper"))], rounding="start"),
        when=cmp(D("y"), "ge", 2),
    ),
    alt(call("flipper_course"), when=OTHERWISE),
]
FXO = ar(I(5), "min", ar(P("n"), "div", 3))
FZO = ar(I(5), "min", ar(P("n"), "div", 2))
rules["flipper_course"] = [
    alt(  # humerus
        split("x", [A(FXO), A(3), R()], [VOID, split("z", [A(FZO), A(3), R()], [VOID, fill("bone"), VOID]), VOID]),
        when=cmp(P("n"), "lt", 4),
    ),
    alt(  # radius and ulna
        split(
            "x",
            [A(FXO), A(2), R()],
            [VOID, split("z", [A(FZO), A(1), A(1), A(1), R()], [VOID, fill("bone"), VOID, fill("bone"), VOID]), VOID],
        ),
        when=all_(cmp(P("n"), "ge", 4), cmp(P("n"), "lt", 9)),
    ),
    alt(  # four digits
        split(
            "x",
            [A(FXO), A(1), R()],
            [
                VOID,
                split(
                    "z",
                    [A(FZO), A(1), A(1), A(1), A(1), A(1), A(1), A(1), R()],
                    [VOID, fill("bone"), VOID, fill("bone"), VOID, fill("bone"), VOID, fill("bone"), VOID],
                ),
                VOID,
            ],
        ),
        when=OTHERWISE,
    ),
]

# ---- lumbar: tall plates, transverse processes, the pilgrims' stair ----------------
# Columns across X: margin 6 | left 13 | spine 7 | processes 5 | stair lane 3 | rest 11.
rules["lumbar"] = one(
    mark(
        "spine-walk",
        20,
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
            split("z", [A(3), R()], [fill("walk"), VOID]),
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
rules["process_column"] = one(
    split("y", [A(28), A(5), R()], [VOID, split("x", [A(5), R()], [PROCESS, VOID]), VOID])
)
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
# One tread per course, each stair block standing alone on the diagonal: a flight
# hung in the air rather than a solid wedge under it.
rules["stair"] = [
    alt(
        split(
            "z",
            [A(1), R()],
            [
                split("y", [A(1), R()], [fill("stair_south"), VOID]),
                split("y", [A(1), R()], [VOID, call("stair")]),
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
        [VOID, split("y", [A(26), A(7), R()], [VOID, bind({"n": 0}, call("caudal")), VOID]), VOID],
    )
)
ODD = cmp(ar(P("n"), "rem", 2), "eq", 1)
rules["caudal"] = [
    alt(
        split("z", [A(3), A(1), R()], [call("caudal_vertebra"), call("caudal_disc"), call("caudal_rest")]),
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
    alt(split("y", [A(2), R(), A(1)], [VOID, fill("cartilage"), fill("stair_north")]), when=ODD),
    alt(split("y", [A(2), R()], [VOID, fill("cartilage")]), when=OTHERWISE),
]
rules["caudal_rest"] = [
    alt(
        split(
            "y",
            [R(), A(1)],
            [split("x", [A(1), R(), A(1)], [VOID, bind({"n": n_plus()}, call("caudal")), VOID]), VOID],
        ),
        when=all_(ODD, cmp(D("x"), "ge", 3)),
    ),
    alt(bind({"n": n_plus()}, call("caudal")), when=OTHERWISE),
]

# ---- skull: one tapering wedge, hollow at the back, open lower jaw ------------------
rules["skull"] = one(
    mark(
        "temple",
        22,
        33,
        26,
        "north",
        split("y", [A(7), A(11), A(24), R()], [VOID, call("jaw_band"), call("skull_band"), VOID]),
    )
)
# The lower jaw: two mandibles hinged under the back of the skull, each bowing out
# and back in along its length and dropping as it runs forward — the mouth open.
rules["jaw_band"] = one(
    split("x", [A(17), R(), A(17)], [mirror("x", call("mandible_zone")), VOID, call("mandible_zone")])
)
rules["mandible_zone"] = one(
    split("z", [A(28), R()], [mirror("z", bind({"n": 0}, call("mandible"))), VOID])
)
BOW = ar(I(2), "add", ar(ar(P("n"), "mul", ar(I(27), "sub", P("n"))), "div", 14))
DROP = ar(I(8), "min", ar(P("n"), "div", 3))
rules["mandible"] = [
    alt(
        split(
            "z",
            [A(1), R()],
            [
                split(
                    "x",
                    [A(BOW), A(2), R()],
                    [VOID, split("y", [R(), A(3), A(DROP)], [VOID, fill("bone"), VOID]), VOID],
                ),
                bind({"n": n_plus()}, call("mandible")),
            ],
        ),
        when=cmp(D("z"), "ge", 1),
    ),
    alt(VOID, when=OTHERWISE),
]
# The cranium and rostrum are one wedge, built from the back of the skull forward
# (mirrored on Z) in 2-block slices: the top drops a course and the sides come in
# one block every other slice over the hall and every slice in front of it, and the
# underside rises once the rostrum begins.
rules["skull_band"] = one(
    split("x", [A(7), A(31), A(7)], [VOID, mirror("z", bind({"n": 0}, call("cranium"))), VOID])
)
SIDE = ar(
    ar(P("n"), "rem", 2), "max", ar(I(0), "max", ar(I(1), "min", ar(P("n"), "sub", 5)))
)  # 1 on odd slices, and on every slice from n = 6
BOTTOM = ar(I(0), "max", ar(I(1), "min", ar(P("n"), "sub", 6)))  # 1 from n = 7
rules["cranium"] = [
    alt(
        split(
            "z",
            [A(2), R()],
            [
                call("cranium_slice"),
                split(
                    "x",
                    [A(SIDE), R(), A(SIDE)],
                    [
                        VOID,
                        split("y", [A(BOTTOM), R(), A(SIDE)], [VOID, bind({"n": n_plus()}, call("cranium")), VOID]),
                        VOID,
                    ],
                ),
            ],
        ),
        when=all_(cmp(D("z"), "ge", 3), cmp(D("y"), "ge", 4), cmp(D("x"), "ge", 7)),
    ),
    alt(call("cranium_slice"), when=OTHERWISE),
]
# Slices 0-6 are the temple hall: 14 courses of bone under a paved floor at the
# walkway's height, walls, and a vault. The rest is solid rostrum.
rules["cranium_slice"] = [
    alt(
        split("y", [A(14), A(1), R()], [call("skull_underside"), call("hall_floor"), call("hall_upper")]),
        when=all_(cmp(P("n"), "lt", 7), cmp(D("y"), "ge", 20)),
    ),
    alt(
        split(
            "y",
            [A(ar(I(3), "min", ar(D("y"), "div", 3))), R(), A(ar(I(4), "min", ar(D("y"), "div", 3)))],
            [mirror("y", call("taper1")), fill("skull"), call("taper2")],
        ),
        when=OTHERWISE,
    ),
]
rules["skull_underside"] = one(split("y", [A(4), R()], [mirror("y", call("taper1")), fill("skull")]))
rules["taper1"] = [
    alt(
        split("y", [A(1), R()], [fill("skull"), split("x", [A(1), R(), A(1)], [VOID, call("taper1"), VOID])], rounding="start"),
        when=all_(cmp(D("x"), "ge", 3), cmp(D("y"), "ge", 2)),
    ),
    alt(fill("skull"), when=OTHERWISE),
]
# The back slice is the occipital wall all the way down; the paving starts inside it.
rules["hall_floor"] = [
    alt(fill("skull"), when=cmp(P("n"), "eq", 0)),
    alt(split("x", [A(2), R(), A(2)], [fill("skull"), fill("paving"), fill("skull")]), when=OTHERWISE),
]
# Above the floor: a band of wall four courses high holding the colonnade, then the
# vault. The back slice is the occipital wall, pierced by the foramen magnum — the
# opening the spinal cord ran through, and the way in from the spine.
rules["hall_upper"] = [
    alt(
        split(
            "y",
            [A(3), R()],
            [split("x", [R(), A(5), R()], [fill("skull"), VOID, fill("skull")]), call("taper2")],
        ),
        when=cmp(P("n"), "eq", 0),
    ),
    alt(split("y", [A(4), R()], [call("hall_walls"), call("vault")]), when=OTHERWISE),
]
rules["hall_walls"] = one(
    split(
        "x",
        [A(2), R(), A(1), A(9), A(1), R(), A(2)],
        [call("hall_wall"), VOID, call("colonnade"), call("hall_nave"), call("colonnade"), VOID, call("hall_wall")],
    )
)
# The orbits: slices 3 and 4 open an eye socket in each side wall.
rules["hall_wall"] = [
    alt(split("y", [A(1), R()], [fill("skull"), VOID]), when=any_(cmp(P("n"), "eq", 3), cmp(P("n"), "eq", 4))),
    alt(fill("skull"), when=OTHERWISE),
]
rules["colonnade"] = [
    alt(
        split("z", [A(1), R()], [split("y", [A(3), R()], [fill("column"), fill("lamp")]), VOID]),
        when=cmp(ar(P("n"), "rem", 2), "eq", 1),
    ),
    alt(VOID, when=OTHERWISE),
]
# The front slice of the hall carries the dais: a stair up onto one paved course,
# and an altar on it — a column drum with a lamp.
rules["hall_nave"] = [
    alt(
        split(
            "z",
            [A(1), R()],
            [
                split("y", [A(1), R()], [fill("stair_dais"), VOID]),
                split(
                    "x",
                    [R(), A(1), R()],
                    [
                        split("y", [A(1), R()], [fill("paving"), VOID]),
                        split("y", [A(1), A(1), A(1), R()], [fill("paving"), fill("column"), fill("lamp"), VOID]),
                        split("y", [A(1), R()], [fill("paving"), VOID]),
                    ],
                ),
            ],
        ),
        when=cmp(P("n"), "eq", 6),
    ),
    alt(VOID, when=OTHERWISE),
]
rules["vault"] = [
    alt(
        split(
            "y",
            [A(1), R()],
            [
                split("x", [A(3), R(), A(3)], [fill("skull"), VOID, fill("skull")]),
                split("x", [A(2), R(), A(2)], [VOID, call("vault"), VOID]),
            ],
            rounding="start",
        ),
        when=all_(cmp(D("x"), "ge", 8), cmp(D("y"), "ge", 2)),
    ),
    alt(fill("skull"), when=OTHERWISE),
]
rules["taper2"] = [
    alt(
        split("y", [A(1), R()], [fill("skull"), split("x", [A(2), R(), A(2)], [VOID, call("taper2"), VOID])], rounding="start"),
        when=all_(cmp(D("x"), "ge", 5), cmp(D("y"), "ge", 2)),
    ),
    alt(fill("skull"), when=OTHERWISE),
]

program = {
    "version": "1.9.0",
    "name": "whale-fall",
    "start": "whale",
    "params": {"n": 0, "k": 0, "lower": 0, "walk_n": 4},
    "palette": {
        "bone": [
            {"weight": 8, "block": "minecraft:bone_block[axis=y]"},
            {"weight": 2, "block": "minecraft:calcite"},
        ],
        "spine": [
            {"weight": 9, "block": "minecraft:bone_block[axis=z]"},
            {"weight": 1, "block": "minecraft:calcite"},
        ],
        # The skull is laid with the grain along its length, as the bone of a skull runs.
        "skull": [
            {"weight": 8, "block": "minecraft:bone_block[axis=z]"},
            {"weight": 2, "block": "minecraft:calcite"},
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
        "lamp": "minecraft:pearlescent_froglight[axis=y]",
        "stair_south": "minecraft:stone_brick_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]",
        "stair_north": "minecraft:smooth_quartz_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]",
        # Written in the scope's own frame: the hall is built mirrored on Z, where
        # local south is world north — the climb onto the dais at the front.
        "stair_dais": {"local": "minecraft:stone_brick_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]"},
    },
    "rules": rules,
}

json.dump(program, sys.stdout, indent=2, sort_keys=True)
sys.stdout.write("\n")
