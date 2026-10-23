#!/usr/bin/env python3
"""Emit programs/inn.json — the Lantern inn of saltstair-a.

Provenance only: the emitted JSON is the artifact of record. Every handed
value is read through a `handed/...` parameter whose default is taken from
`delvec allocation` at emit time; nothing handed is typed here.

Scene: a wide one-storey inn across the square from the chapel. A body comes
in at the west door under a hanging lantern, crosses a planked taproom between
two rows of tables to the counter on the east side, where the innkeeper
stands. Cobblestone ground course with stone-brick quoins, white calcite
upper band and gables framed in spruce, a deepslate-tile gable roof whose
ridge runs east-west so a gable faces the square over the door.
"""
import json
import os
import subprocess
import sys

CAMPAIGN = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DELVEC = os.path.expanduser("~/.delvewright/bin/delvec")
SEAM = "square-inn"


def allocation():
    out = subprocess.run(
        [DELVEC, "allocation", CAMPAIGN, "node/inn", "--json"],
        capture_output=True, text=True)
    if out.returncode == 0:
        try:
            return json.loads(out.stdout)
        except ValueError:
            pass
    out = subprocess.run([DELVEC, "allocation", CAMPAIGN, "node/inn"],
                         capture_output=True, text=True, check=True)
    text = out.stdout
    start = text.index("{")
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return json.loads(text[start:i + 1])
    raise SystemExit("could not read the allocation")


# ---- IR helpers -----------------------------------------------------------

def I(v):
    return {"expr": "int", "value": v}


def P(name):
    return {"expr": "param", "name": name}


def sub(a, b):
    return {"expr": "arith", "op": "sub", "lhs": a, "rhs": b}


def add(a, b):
    return {"expr": "arith", "op": "add", "lhs": a, "rhs": b}


def A(e):
    if isinstance(e, int):
        e = I(e)
    return {"size": "absolute", "blocks": e}


def R(w=1):
    return {"size": "relative", "weight": I(w)}


def split(axis, sizes, children, **kw):
    n = {"op": "split", "axis": axis, "sizes": sizes, "children": children}
    n.update(kw)
    return n


def fill(role):
    return {"op": "fill", "material": {"role": role}}


VOID = {"op": "void"}
SKIP = {"op": "skip"}


def call(sym):
    return {"op": "call", "symbol": sym}


def claim(region, body):
    return {"op": "claim", "region": region, "body": body}


def dim(axis):
    return {"expr": "dim", "dim": axis}


def cmp(lhs, op, rhs):
    return {"cond": "cmp", "lhs": lhs, "op": op, "rhs": rhs}


def alt(body, when=None):
    a = {"weight": 1, "body": body}
    if when is not None:
        a["when"] = when
    return a


OTHERWISE = {"cond": "otherwise"}

EAVES = P("handed/roof/eaves")
DATUM = P("handed/datum-y")
LID = P("handed/roof/lid-y")
SY0 = P(f"handed/seam/{SEAM}/y0")
SY1 = P(f"handed/seam/{SEAM}/y1")
SZ0 = P(f"handed/seam/{SEAM}/z0")
SZ1 = P(f"handed/seam/{SEAM}/z1")


def sparse(size, items, filler):
    """Nested x, z, y splits placing single-cell items in a box of `size`.

    `items` maps (x, y, z) local cells to a node; every other cell gets
    `filler`. The last piece of each split is relative, so the pattern
    covers its axis exactly.
    """
    def along(axis_i, axis, cells, extent, inner):
        keys = sorted({c[axis_i] for c in cells})
        if not keys:
            return filler
        sizes, children, cur = [], [], 0
        for k in keys:
            if k > cur:
                sizes.append(A(k - cur))
                children.append(filler)
            sizes.append(A(1))
            children.append(inner(k))
            cur = k + 1
        sizes.append(R())
        children.append(filler)
        return split(axis, sizes, children)

    X, Y, Z = size

    def at_x(x):
        sub_items = {c: v for c, v in items.items() if c[0] == x}

        def at_z(z):
            col = {c: v for c, v in sub_items.items() if c[2] == z}

            def at_y(y):
                return col[(x, y, z)]
            return along(1, "y", list(col), Y, at_y)
        return along(2, "z", list(sub_items), Z, at_z)
    return along(0, "x", list(items), X, at_x)


# ---- the program ----------------------------------------------------------

def program(al):
    seam = next(s for s in al["seams"] if s["edge"] == f"edge/{SEAM}")
    (x0, y0, z0), (x1, y1, z1) = seam["cells"]
    roof = al["roof"]
    params = {
        "handed/datum-y": al["datum_y"],
        "handed/roof/eaves": roof["eaves"],
        "handed/roof/lid-y": roof["lid_y"],
        f"handed/seam/{SEAM}/y0": y0,
        f"handed/seam/{SEAM}/y1": y1,
        f"handed/seam/{SEAM}/z0": z0,
        f"handed/seam/{SEAM}/z1": z1,
    }

    log_y = "minecraft:spruce_log[axis=y]"
    palette = {
        "floor": "minecraft:spruce_planks",
        "earth": "minecraft:dirt",
        "cobble": [
            {"weight": 8, "block": "minecraft:cobblestone"},
            {"weight": 1, "block": "minecraft:mossy_cobblestone"},
        ],
        "quoin": "minecraft:stone_bricks",
        "infill": "minecraft:calcite",
        "post": log_y,
        # a beam lying along the scope's own x
        "beam": {"local": "minecraft:stripped_spruce_log[axis=x]"},
        "beam_ns": "minecraft:stripped_spruce_log[axis=z]",
        "beam_ew": "minecraft:stripped_spruce_log[axis=x]",
        "pane": {"local": "minecraft:glass_pane[east=true,north=false,south=false,waterlogged=false,west=true]"},
        "ceiling": "minecraft:spruce_planks",
        "roof_n": "minecraft:deepslate_tile_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]",
        "roof_s": "minecraft:deepslate_tile_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]",
        "ridge": "minecraft:deepslate_tiles",
        "lantern_hung": "minecraft:lantern[hanging=true,waterlogged=false]",
        "counter": "minecraft:stripped_spruce_wood[axis=y]",
        "table": "minecraft:spruce_fence[east=false,north=false,south=false,waterlogged=false,west=false]",
        "table_top": "minecraft:spruce_pressure_plate[powered=false]",
        "chair_e": "minecraft:spruce_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]",
        "chair_w": "minecraft:spruce_stairs[facing=west,half=bottom,shape=straight,waterlogged=false]",
        "rug": "minecraft:red_carpet",
    }

    rules = {}

    # Whole frame: ground course(s), the storey, the roof zone.
    rules["inn"] = [alt(split("y", [A(DATUM), A(sub(LID, DATUM)), R()],
                              [call("ground"), call("storey"), call("roof")]))]

    # Ground: the floor over the plot only; the ring is the whole's.
    ring = lambda inner: split("x", [A(EAVES), A(1), R(), A(1), A(EAVES)],
                               [SKIP, SKIP, inner, SKIP, SKIP])
    rules["ground"] = [alt(ring(call("ground_row")))]
    rules["ground_row"] = [alt(split("z", [A(EAVES), A(1), R(), A(1), A(EAVES)],
                                     [SKIP, SKIP, call("ground_col"), SKIP, SKIP]))]
    rules["ground_col"] = [alt(split("y", [R(), A(1)], [fill("earth"), fill("floor")]))]

    # Storey: west wall (door), the middle band, east wall.
    rules["storey"] = [alt(split("x", [A(EAVES), A(1), R(), A(1), A(EAVES)],
                                 [SKIP, call("west_wall"), call("band"),
                                  call("east_wall"), SKIP]))]
    along_z = lambda body: {"op": "reorient", "orient": {"x": "local_z", "z": "local_x"},
                            "body": body}
    rules["west_wall"] = [alt(split(
        "z",
        [A(EAVES), A(1), A(sub(sub(SZ0, EAVES), I(1))),
         A(add(sub(SZ1, SZ0), I(1))), R(), A(1), A(EAVES)],
        [SKIP, call("corner"), along_z(call("run")), call("door"),
         along_z(call("run")), call("corner"), SKIP]))]
    rules["east_wall"] = [alt(split(
        "z", [A(EAVES), A(1), R(), A(1), A(EAVES)],
        [SKIP, call("corner"), along_z(call("run")), call("corner"), SKIP]))]
    rules["band"] = [alt(split(
        "z", [A(EAVES), A(1), R(), A(1), A(EAVES)],
        [SKIP, call("run"), call("room"), call("run"), SKIP]))]

    rules["corner"] = [alt(split("y", [A(2), R()], [fill("quoin"), fill("post")]))]

    # The door: the handed cells open, a lantern hung in the head, a lintel.
    rules["door"] = [alt(split(
        "y",
        [A(add(sub(SY1, SY0), I(1))), A(1), R()],
        [claim("west-door", VOID), fill("lantern_hung"), fill("beam_ns")]),
        when=cmp(SY0, "eq", DATUM)),
        alt(split("y", [A(sub(SY0, DATUM)), A(add(sub(SY1, SY0), I(1))), A(1), R()],
                  [fill("cobble"), claim("west-door", VOID), fill("lantern_hung"),
                   fill("beam_ns")]), when=OTHERWISE)]

    # A wall run, its local x along the wall: windows by length.
    rules["run"] = [
        alt(split("x", [R(2), A(3), R(1), A(3), R(2)],
                  [call("solid"), call("window"), call("solid"), call("window"),
                   call("solid")]),
            when=cmp(dim("x"), "ge", I(9))),
        alt(split("x", [R(), A(3), R()],
                  [call("solid"), call("window"), call("solid")]),
            when={"cond": "all", "of": [cmp(dim("x"), "ge", I(5)),
                                        cmp(dim("x"), "lt", I(9))]}),
        alt(call("solid"), when=OTHERWISE),
    ]
    rules["solid"] = [alt(split("y", [A(2), R()], [fill("cobble"), fill("infill")]))]
    rules["window"] = [alt(split("x", [A(1), A(1), A(1)],
                                 [call("light"), call("mullion"), call("light")]))]
    rules["light"] = [alt(split("y", [A(1), A(2), R()],
                                [fill("cobble"), fill("pane"), fill("beam")]))]
    rules["mullion"] = [alt(split("y", [A(1), A(2), R()],
                                  [fill("cobble"), fill("post"), fill("beam")]))]

    # The taproom: claimed as the hall, the innkeeper marked behind the counter.
    # Local cells of the 11 x 4 x 11 room (x east, z south, y up from the floor).
    items = {}
    # counter along the east side, gaps at both ends to get behind it
    for z in range(2, 9):
        items[(8, 0, z)] = fill("counter")
    items[(8, 3, 3)] = fill("lantern_hung")
    items[(8, 3, 7)] = fill("lantern_hung")
    # two rows of tables with a chair either side
    for z in (2, 8):
        items[(1, 0, z)] = fill("chair_w")
        items[(2, 0, z)] = fill("table")
        items[(2, 1, z)] = fill("table_top")
        items[(3, 0, z)] = fill("chair_e")
        items[(4, 0, z)] = fill("chair_w")
        items[(5, 0, z)] = fill("table")
        items[(5, 1, z)] = fill("table_top")
        items[(6, 0, z)] = fill("chair_e")
    # a runner from the door to the counter
    for x in range(0, 8):
        items[(x, 0, 5)] = fill("rug")
    # lanterns hung from the ceiling, staggered
    for c in [(2, 3, 3), (5, 3, 6), (3, 3, 9), (6, 3, 1), (6, 3, 10)]:
        items[c] = fill("lantern_hung")
    room_body = sparse((11, 4, 11), items, VOID)
    rules["room"] = [alt(claim("hall", {
        "op": "mark",
        "mark": {"anchor": "node-inn", "at": "offset", "facing": "west",
                 "x": I(9), "y": I(0), "z": I(5)},
        "body": room_body}))]

    # Roof zone: the lid course (wall plates, ceiling, eave stairs), then the
    # 45-degree gable courses tapering across z to a ridge.
    rules["roof"] = [alt(claim("roof", split("y", [A(1), R()],
                                             [call("lid"), call("gable_stack")])))]
    rules["lid"] = [alt(split("z", [A(EAVES), R(), A(EAVES)],
                              [fill("roof_n"), call("lid_mid"), fill("roof_s")]))]
    rules["lid_mid"] = [alt(split("x", [A(EAVES), A(1), R(), A(1), A(EAVES)],
                                  [VOID, fill("beam_ns"), call("lid_row"),
                                   fill("beam_ns"), VOID]))]
    rules["lid_row"] = [alt(split("z", [A(1), R(), A(1)],
                                  [fill("beam_ew"), fill("ceiling"), fill("beam_ew")]))]
    rules["gable_stack"] = [alt(split("z", [A(EAVES), R(), A(EAVES)],
                                      [VOID, call("slope"), VOID]))]
    rules["slope"] = [
        alt(split("y", [A(1), R()], [call("course"), call("slope_in")]),
            when={"cond": "all", "of": [cmp(dim("y"), "ge", I(2)),
                                        cmp(dim("z"), "ge", I(3))]}),
        alt(split("z", [A(1), R(), A(1)],
                  [fill("roof_n"), fill("ridge"), fill("roof_s")]),
            when={"cond": "all", "of": [cmp(dim("y"), "eq", I(1)),
                                        cmp(dim("z"), "ge", I(3))]}),
        alt(VOID, when=OTHERWISE),
    ]
    rules["slope_in"] = [alt(split("z", [A(1), R(), A(1)],
                                   [VOID, call("slope"), VOID]))]
    rules["course"] = [alt(split("z", [A(1), R(), A(1)],
                                 [fill("roof_n"), call("gable_row"), fill("roof_s")]))]
    rules["gable_row"] = [alt(split("x", [A(EAVES), A(1), R(), A(1), A(EAVES)],
                                    [VOID, call("gable"), VOID, call("gable"), VOID]))]
    rules["gable"] = [alt(split("z", [R(), A(1), R()],
                                [fill("infill"), fill("post"), fill("infill")]))]

    contract = {
        "entry": "hall",
        "spaces": {"hall": {"envelope": "enclosed"}},
        "no_body": {"roof": {"reason": "the roof and the loft under it, which nobody walks"}},
        "no_body_majority_ack": "a house that draws its own outside owns its roof, and a pitched roof is more standable surface than the taproom under it; nobody walks it",
        "edges": [{"a": "exterior", "b": "hall", "class": "walk", "via": "west-door"}],
    }

    return {
        "version": "1.9.0",
        "name": "saltstair-a-inn",
        "start": "inn",
        "params": params,
        "palette": palette,
        "rules": rules,
        "contract": contract,
        "shown_faces": ["north", "south", "east", "west", "up"],
    }


def main():
    al = allocation()
    out = os.path.join(CAMPAIGN, "programs", "inn.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f:
        json.dump(program(al), f, indent=1, sort_keys=True)
        f.write("\n")
    print(out)


if __name__ == "__main__":
    sys.exit(main())
