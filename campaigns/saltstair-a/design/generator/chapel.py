#!/usr/bin/env python3
"""Emit programs/chapel.json — the grammar program for node/chapel.

Provenance only: the emitted JSON is the artifact of record. Every handed value
is a `handed/...` parameter whose default is read from `delvec allocation`
(passed in as a JSON file); nothing handed is typed here.

Usage: chapel.py <allocation.json> <out program.json>
"""
import json
import sys

# --- expression / node helpers -------------------------------------------------

def I(v):
    return {"expr": "int", "value": v}


def P(n):
    return {"expr": "param", "name": n}


def D(axis):
    return {"expr": "dim", "dim": axis}


def A(lhs, op, rhs):
    return {"expr": "arith", "lhs": lhs, "op": op, "rhs": rhs}


def ab(e):
    return {"size": "absolute", "blocks": I(e) if isinstance(e, int) else e}


def rel(w=1):
    return {"size": "relative", "weight": I(w)}


def split(axis, parts, rounding=None):
    node = {"op": "split", "axis": axis,
            "sizes": [s for s, _ in parts], "children": [c for _, c in parts]}
    if rounding:
        node["rounding"] = rounding
    return node


def fill(role):
    return {"op": "fill", "material": {"role": role}}


VOID = {"op": "void"}


def call(sym):
    return {"op": "call", "symbol": sym}


def claim(region, body):
    return {"op": "claim", "region": region, "body": body}


def bind(body, params=None, palette=None):
    node = {"op": "bind", "body": body}
    if params:
        node["params"] = params
    if palette:
        node["palette"] = palette
    return node


def cmp(lhs, op, rhs):
    return {"cond": "cmp", "lhs": lhs, "op": op, "rhs": rhs}


def alt(body, when=None):
    a = {"weight": 1, "body": body}
    if when is not None:
        a["when"] = when
    return a


OTHERWISE = {"cond": "otherwise"}

# handed names
DATUM = P("handed/datum-y")
BOTTOM = P("handed/ground/bottom-y")
EAVES = P("handed/roof/eaves")
LID = P("handed/roof/lid-y")
SX0 = P("handed/seam/square-chapel/x0")
SY0 = P("handed/seam/square-chapel/y0")
SY1 = P("handed/seam/square-chapel/y1")
SZ0 = P("handed/seam/square-chapel/z0")
SZ1 = P("handed/seam/square-chapel/z1")
COURSE = P("course")
PART = P("tower_part")

DOOR_W = A(A(SZ1, "sub", SZ0), "add", I(1))
DOOR_H = A(A(SY1, "sub", SY0), "add", I(1))
EAVES_RING = A(EAVES, "add", I(1))


def main(alloc_path, out_path):
    alloc = json.load(open(alloc_path))
    seam = next(s for s in alloc["seams"] if s["edge"] == "edge/square-chapel")
    (x0, y0, z0), (x1, y1, z1) = seam["cells"]
    params = {
        "handed/datum-y": alloc["datum_y"],
        "handed/ground/bottom-y": alloc["ground"]["bottom_y"],
        "handed/roof/eaves": alloc["roof"]["eaves"],
        "handed/roof/lid-y": alloc["roof"]["lid_y"],
        "handed/seam/square-chapel/x0": x0,
        "handed/seam/square-chapel/y0": y0,
        "handed/seam/square-chapel/y1": y1,
        "handed/seam/square-chapel/z0": z0,
        "handed/seam/square-chapel/z1": z1,
        "course": 0,
        "tower_part": 0,
    }

    def stair(block, facing):
        return {"local": f"minecraft:{block}_stairs[facing={facing},half=bottom,shape=straight,waterlogged=false]"}

    palette = {
        # ground floor and walls: stone brick, a little weathered
        "floor": [{"weight": 6, "block": "minecraft:cobblestone"},
                  {"weight": 1, "block": "minecraft:mossy_cobblestone"}],
        "wall": [{"weight": 10, "block": "minecraft:stone_bricks"},
                 {"weight": 2, "block": "minecraft:cracked_stone_bricks"},
                 {"weight": 1, "block": "minecraft:mossy_stone_bricks"}],
        "plinth": "minecraft:cobblestone",
        "quoin": "minecraft:chiseled_stone_bricks",
        "glass_x": "minecraft:glass_pane[east=true,north=false,south=false,waterlogged=false,west=true]",
        "glass_z": "minecraft:glass_pane[east=false,north=true,south=true,waterlogged=false,west=false]",
        "lamp": "minecraft:lantern[hanging=true,waterlogged=false]",
        # timber framing above, white infill
        "plate": "minecraft:spruce_log[axis=x]",
        "beam": "minecraft:spruce_log[axis=z]",
        "post": "minecraft:spruce_log[axis=y]",
        "infill": "minecraft:calcite",
        "ceiling": "minecraft:spruce_planks",
        # slate roof
        "roof_s": stair("deepslate_tile", "south"),
        "roof_n": stair("deepslate_tile", "north"),
        "ridge": "minecraft:deepslate_tiles",
        # tower
        "tower": "minecraft:stone_bricks",
        "cap_s": stair("deepslate_tile", "south"),
        "cap_n": stair("deepslate_tile", "north"),
        "cap_e": stair("deepslate_tile", "east"),
        "cap_w": stair("deepslate_tile", "west"),
        "cap_corner": "minecraft:deepslate_tile_slab[type=bottom,waterlogged=false]",
        "cap_top": "minecraft:deepslate_tiles",
        # furnishing
        "pew": stair("spruce", "east"),
        "altar": "minecraft:chiseled_stone_bricks",
        # bound per column kind in the roof band
        "air": "minecraft:air",
        "slope": stair("deepslate_tile", "south"),
        "lidfill": "minecraft:spruce_planks",
        "atticfill": "minecraft:air",
        "gable_attic": "minecraft:calcite",
    }

    R = {}

    # --- top: ground band / storey / roof band ---------------------------------
    R["chapel"] = [alt(split("y", [
        (ab(A(DATUM, "sub", BOTTOM)), call("ground")),
        (ab(A(LID, "sub", DATUM)), call("storey")),
        (rel(), claim("roof", bind(call("roof_band"), params={"course": I(0)}))),
    ]))]

    # ground: cobble floor over the plot; ring and outside are not ours
    R["ground"] = [alt(split("x", [
        (ab(EAVES_RING), VOID),
        (ab(A(SX0, "sub", EAVES_RING)), split("z", [
            (ab(EAVES_RING), VOID),
            (rel(), fill("floor")),
            (ab(EAVES_RING), VOID),
        ])),
        (rel(), VOID),
    ]))]

    # storey: west wall | nave | east wall (cut by the seam) | outside
    R["storey"] = [alt(split("x", [
        (ab(EAVES), VOID),
        (ab(1), call("west_wall")),
        (ab(A(SX0, "sub", EAVES_RING)), call("inner")),
        (ab(1), call("east_wall")),
        (rel(), VOID),
    ]))]

    def ring_z(body):
        """z: eaves | corner | body | corner | eaves"""
        return split("z", [
            (ab(EAVES), VOID),
            (ab(1), call("corner")),
            (rel(), body),
            (ab(1), call("corner")),
            (ab(EAVES), VOID),
        ])

    R["corner"] = [alt(split("y", [(ab(1), fill("plinth")), (rel(), fill("quoin"))]))]

    # a wall face: plinth course, then masonry
    R["wall_face"] = [alt(split("y", [(ab(1), fill("plinth")), (rel(), fill("wall"))]))]

    # window column: plinth, sill, glass, head; glass role bound by caller
    R["window_col"] = [alt(split("y", [
        (ab(1), fill("plinth")),
        (ab(1), fill("wall")),
        (ab(3), fill("glazing")),
        (rel(), fill("wall")),
    ]))]
    palette["glazing"] = palette["glass_x"]

    # west wall: one tall window behind the altar, centred on the aisle
    R["west_wall"] = [alt(ring_z(split("z", [
        (ab(A(SZ0, "sub", EAVES_RING)), call("wall_face")),
        (ab(DOOR_W), bind(split("y", [
            (ab(1), fill("plinth")),
            (ab(2), fill("wall")),
            (ab(3), fill("glazing")),
            (rel(), fill("wall")),
        ]), palette={"glazing": {"role": "glass_z"}})),
        (rel(), call("wall_face")),
    ])))]

    # inner: north wall | nave | south wall
    R["inner"] = [alt(split("z", [
        (ab(EAVES), VOID),
        (ab(1), call("side_wall")),
        (rel(), claim("nave", call("nave"))),
        (ab(1), call("side_wall")),
        (ab(EAVES), VOID),
    ]))]

    # side wall: two pairs of windows along x
    R["side_wall"] = [alt(split("x", [
        (rel(), call("wall_face")),
        (ab(2), bind(call("window_col"), palette={"glazing": {"role": "glass_x"}})),
        (ab(2), call("wall_face")),
        (ab(2), bind(call("window_col"), palette={"glazing": {"role": "glass_x"}})),
        (rel(), call("wall_face")),
    ], rounding="middle"))]

    # east wall: the door onto the square at the handed cells, lantern above it
    R["east_wall"] = [alt(ring_z(split("z", [
        (ab(A(SZ0, "sub", EAVES_RING)), call("wall_face")),
        (ab(DOOR_W), split("y", [
            (ab(A(SY0, "sub", DATUM)), fill("plinth")),
            (ab(DOOR_H), claim("door-square-chapel", VOID)),
            (ab(1), fill("lamp")),
            (rel(), fill("quoin")),
        ])),
        (rel(), call("wall_face")),
    ])))]

    # nave: floor level furnishing, and the lamp course under the ceiling
    R["nave"] = [alt(split("y", [
        (rel(), call("nave_floor")),
        (ab(1), call("lamps")),
    ]))]

    # x: altar | sanctuary | pews | entry
    R["nave_floor"] = [alt(split("x", [
        (ab(1), call("altar_col")),
        (ab(2), {"op": "mark", "mark": {
            "anchor": "node-chapel", "at": "offset", "facing": "west",
            "x": I(1), "y": I(0), "z": A(SZ0, "sub", EAVES_RING)},
            "body": VOID}),
        (rel(), call("pews")),
        (ab(1), VOID),
    ]))]

    R["altar_col"] = [alt(split("z", [
        (ab(A(A(SZ0, "sub", EAVES_RING), "sub", I(1))), VOID),
        (ab(A(DOOR_W, "add", I(2))), split("y", [
            (ab(1), fill("altar")),
            (rel(), VOID),
        ])),
        (rel(), VOID),
    ]))]

    # pews either side of the aisle that runs from the door to the altar
    R["pews"] = [alt(split("z", [
        (ab(A(SZ0, "sub", EAVES_RING)), split("z", [(ab(1), VOID), (rel(), call("pew_rows"))])),
        (ab(DOOR_W), VOID),
        (rel(), split("z", [(rel(), call("pew_rows")), (ab(1), VOID)])),
    ]))]

    R["pew_rows"] = [alt({"op": "split", "axis": "x", "repeat": True,
                          "sizes": [ab(1), ab(1)],
                          "children": [split("y", [(ab(1), fill("pew")), (rel(), VOID)]), VOID]})]

    # four lanterns hung from the ceiling, near the windows
    R["lamps"] = [alt(split("x", [
        (ab(2), VOID),
        (ab(1), call("lamp_row")),
        (ab(3), VOID),
        (ab(1), call("lamp_row")),
        (rel(), VOID),
    ]))]
    R["lamp_row"] = [alt(split("z", [
        (ab(2), VOID), (ab(1), fill("lamp")), (rel(), VOID), (ab(1), fill("lamp")), (ab(2), VOID),
    ]))]

    # --- roof band: a gable over z, one stripe per course, counted -------------
    R["roof_band"] = [
        alt(split("z", [
            (ab(1), bind(call("stripe_n"), palette={"slope": {"role": "roof_s"}})),
            (rel(), bind(call("roof_band"), params={"course": A(COURSE, "add", I(1))})),
            (ab(1), bind(call("stripe"), palette={"slope": {"role": "roof_n"}})),
        ]), cmp(D("z"), "ge", I(3))),
        alt(bind(call("stripe"), palette={"slope": {"role": "ridge"},
                                          "gable_attic": {"role": "post"}}),
            cmp(D("z"), "eq", I(1))),
        alt(split("z", [
            (ab(1), bind(call("stripe_n"), palette={"slope": {"role": "roof_s"}})),
            (ab(1), bind(call("stripe"), palette={"slope": {"role": "roof_n"}})),
        ]), OTHERWISE),
    ]

    # the north stripes of the ring and the two courses inside it carry the tower
    in_tower = {"cond": "all", "of": [
        cmp(COURSE, "ge", EAVES),
        cmp(COURSE, "lt", A(EAVES, "add", I(3))),
    ]}
    R["stripe_n"] = [
        alt(bind(call("tower_stripe"), params={"tower_part": A(COURSE, "sub", EAVES)}), in_tower),
        alt(call("stripe"), OTHERWISE),
    ]

    eave_k = lambda: bind(call("profile"), palette={"lidfill": {"role": "air"}, "atticfill": {"role": "air"}})
    gable_k = lambda: bind(call("profile"), palette={"lidfill": {"role": "beam"}, "atticfill": {"role": "gable_attic"}})
    inner_k = lambda: call("inner_profile")

    R["stripe"] = [alt(split("x", [
        (ab(EAVES), eave_k()),
        (ab(1), gable_k()),
        (rel(), inner_k()),
        (ab(1), gable_k()),
        (ab(EAVES), eave_k()),
    ]))]

    R["tower_stripe"] = [alt(split("x", [
        (ab(EAVES), eave_k()),
        (ab(1), gable_k()),
        (rel(), inner_k()),
        (ab(3), call("tower")),
        (ab(EAVES), eave_k()),
    ]))]

    R["inner_profile"] = [
        alt(bind(call("profile"), palette={"lidfill": {"role": "plate"}, "atticfill": {"role": "air"}}),
            cmp(COURSE, "eq", EAVES)),
        alt(bind(call("profile"), palette={"lidfill": {"role": "ceiling"}, "atticfill": {"role": "air"}}),
            OTHERWISE),
    ]

    # one column of a course: what stands under the slope, the slope, sky
    R["profile"] = [
        alt(split("y", [
            (ab(1), fill("lidfill")),
            (ab(A(COURSE, "sub", I(1))), fill("atticfill")),
            (ab(1), fill("slope")),
            (rel(), VOID),
        ]), cmp(COURSE, "ge", EAVES)),
        alt(split("y", [
            (ab(COURSE), VOID),
            (ab(1), fill("slope")),
            (rel(), VOID),
        ]), OTHERWISE),
    ]

    # the short tower: masonry through the roof, an open belfry, a slate cap
    R["tower"] = [alt(split("y", [
        (rel(), fill("tower")),
        (ab(2), call("belfry")),
        (ab(1), call("cap")),
    ]))]
    face = lambda: split("x", [(ab(1), fill("tower")), (ab(1), VOID), (ab(1), fill("tower"))])
    R["belfry"] = [
        alt(split("x", [
            (ab(1), VOID),
            (ab(1), split("y", [(ab(1), VOID), (ab(1), fill("lamp"))])),
            (ab(1), VOID),
        ]), cmp(PART, "eq", I(1))),
        alt(face(), OTHERWISE),
    ]
    R["cap"] = [
        alt(split("x", [(ab(1), fill("cap_corner")), (ab(1), fill("cap_s")), (ab(1), fill("cap_corner"))]),
            cmp(PART, "eq", I(0))),
        alt(split("x", [(ab(1), fill("cap_e")), (ab(1), fill("cap_top")), (ab(1), fill("cap_w"))]),
            cmp(PART, "eq", I(1))),
        alt(split("x", [(ab(1), fill("cap_corner")), (ab(1), fill("cap_n")), (ab(1), fill("cap_corner"))]),
            OTHERWISE),
    ]

    program = {
        "version": "1.9.0",
        "name": "saltstair-a-chapel",
        "start": "chapel",
        "params": params,
        "palette": palette,
        "rules": R,
        "contract": {
            "entry": "nave",
            "spaces": {"nave": {"envelope": "enclosed"}},
            "no_body": {"roof": {"reason": "the slate roof, the attic under it and the belfry of the tower, which nobody is meant to walk"}},
            "no_body_majority_ack": "a house that owns its outside owns its roof, and a pitched roof with a tower on it is more standable surface than the nave under it; nobody walks it",
            "edges": [
                {"a": "exterior", "b": "nave", "class": "walk", "via": "door-square-chapel"},
            ],
        },
        "shown_faces": ["east", "north", "south", "up", "west"],
    }
    with open(out_path, "w") as f:
        json.dump(program, f, indent=1)
        f.write("\n")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
