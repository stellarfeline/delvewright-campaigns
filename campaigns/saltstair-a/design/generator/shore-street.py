#!/usr/bin/env python3
"""Emit programs/shore-street.json — the shore street of Saltstair.

Provenance only: the emitted JSON is the artifact of record. Every handed
value is read through a `handed/...` parameter; the defaults are copied from
`delvec allocation <campaign> node/shore-street` at generation time.
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve()
CAMPAIGN = HERE.parents[2]
DELVEC = Path.home() / ".delvewright/bin/delvec"


def allocation():
    out = subprocess.run(
        [str(DELVEC), "allocation", str(CAMPAIGN), "node/shore-street", "--json"],
        capture_output=True, text=True)
    if out.returncode == 0:
        try:
            return json.JSONDecoder().raw_decode(out.stdout.lstrip())[0]
        except json.JSONDecodeError:
            pass
    return None


def I(v):
    return {"expr": "int", "value": v}


def P(n):
    return {"expr": "param", "name": n}


def ar(a, op, b):
    return {"expr": "arith", "lhs": a, "op": op, "rhs": b}


def add(a, b):
    return ar(a, "add", b)


def sub(a, b):
    return ar(a, "sub", b)


def ab(e):
    return {"size": "absolute", "blocks": e}


REL = {"size": "relative", "weight": I(1)}


def split(axis, sizes, children):
    return {"op": "split", "axis": axis, "sizes": sizes, "children": children}


def call(s):
    return {"op": "call", "symbol": s}


def fill(role):
    return {"op": "fill", "material": {"role": role}}


def claim(region, body):
    return {"op": "claim", "region": region, "body": body}


VOID = {"op": "void"}
SKIP = {"op": "skip"}


def rule(body):
    return [{"weight": 1, "body": body}]


N = "handed/seam/flight-4-shore-street/"
S = "handed/seam/shore-street-flight-5/"
W = "handed/seam/shore-street-harbourmaster/"
SEAMS = {
    "flight-4-shore-street": "north",
    "shore-street-flight-5": "south",
    "shore-street-harbourmaster": "west",
}


def span(prefix, a):
    """Cell count of a handed seam's inclusive span along axis a."""
    return add(sub(P(prefix + a + "1"), P(prefix + a + "0")), I(1))


def build(alloc):
    params = {}
    # defaults: the handed values (read from the allocation, never typed)
    params["handed/datum-y"] = alloc["datum_y"]
    params["handed/ground/bottom-y"] = alloc["ground"]["bottom_y"]
    for seam in alloc["seams"]:
        stem = seam["edge"].split("/", 1)[1]
        (x0, y0, z0), (x1, y1, z1) = seam["cells"]
        for k, v in zip(("x0", "y0", "z0", "x1", "y1", "z1"), (x0, y0, z0, x1, y1, z1)):
            params[f"handed/seam/{stem}/{k}"] = v
        params[f"handed/seam/{stem}/rise"] = seam["rise"]

    rules = {}
    # --- the whole frame: ground course under the walk plane, air above ---
    rules["place"] = rule(split("y", [
        ab(sub(P("handed/datum-y"), P("handed/ground/bottom-y"))), REL,
    ], [call("ground-course"), call("upper")]))

    # --- ground course: paving over the plot, the ring left to the whole ---
    rules["ground-course"] = rule(split("x", [
        ab(P(N + "x0")), ab(span(N, "x")), REL,
    ], [SKIP, call("pave-band"), SKIP]))
    rules["pave-band"] = rule(split("z", [ab(P(S + "z0")), REL],
                                    [call("pave-strip"), SKIP]))
    rules["pave-strip"] = rule(split("x", [ab(I(1)), REL, ab(I(1))],
                                     [fill("kerb"), fill("paving"), fill("kerb")]))

    # --- above the walk plane: north seam band, the street, the south head ---
    rules["upper"] = rule(split("z", [
        ab(add(P(N + "z1"), I(1))),
        ab(sub(sub(P(S + "z0"), P(N + "z1")), I(1))),
        REL,
    ], [call("north-band"), call("mid-band"), call("south-band")]))

    rules["north-band"] = rule(split("x", [
        ab(P(N + "x0")), ab(span(N, "x")), REL,
    ], [SKIP, call("north-mouth"), call("post")]))
    rules["north-mouth"] = rule(split("y", [ab(span(N, "y")), REL],
                                      [claim("flight-4-shore-street", VOID), VOID]))

    rules["mid-band"] = rule(split("x", [
        ab(P(W + "x0")),
        ab(span(W, "x")),
        ab(sub(P(N + "x1"), P(W + "x1"))),
        REL,
    ], [SKIP, call("west-lane"), call("street-main"), call("east-wall")]))

    # the lane beside the harbourmaster's facade, with its door
    rules["west-lane"] = rule(split("z", [
        ab(sub(sub(P(W + "z0"), P(N + "z1")), I(1))),
        ab(span(W, "z")),
        REL,
    ], [call("street-air"), call("door-column"), call("street-air")]))
    rules["door-column"] = rule(split("y", [ab(span(W, "y")), REL],
                                      [claim("shore-street-harbourmaster", VOID),
                                       call("street-air")]))

    rules["street-air"] = rule(claim("street", VOID))
    rules["street-main"] = rule({
        "op": "mark",
        "mark": {"anchor": "node-shore-street", "at": "floor_center", "facing": "south"},
        "body": call("street-air"),
    })

    # the east kerb wall against the turf, a lantern post across from the door
    rules["east-wall"] = rule(split("z", [
        ab(sub(sub(P(W + "z0"), P(N + "z1")), I(1))),
        ab(span(W, "z")),
        REL,
    ], [call("kerb-wall"), call("post"), call("kerb-wall")]))
    rules["kerb-wall"] = rule(split("y", [ab(I(1)), ab(I(1)), REL],
                                    [fill("foot"), fill("wall"), claim("kerb-top", VOID)]))
    rules["post"] = rule(split("y", [ab(I(1)), ab(I(1)), ab(I(1)), ab(I(1)), REL],
                               [fill("foot"), fill("wall"), fill("cap"), fill("lamp"),
                                claim("kerb-top", VOID)]))

    # the head of the fifth flight: posts either side, the stair mouth between
    rules["south-band"] = rule(split("x", [
        ab(P(S + "x0")), ab(span(S, "x")), REL,
    ], [call("post"), call("south-mouth"), call("post")]))
    rules["south-mouth"] = rule(split("y", [ab(span(S, "y")), REL],
                                      [claim("shore-street-flight-5", VOID), VOID]))

    contract = {
        "entry": "street",
        "spaces": {"street": {"envelope": "open"}},
        "no_body": {"kerb-top": {"reason": "the tops of the kerb wall and the lantern posts, dressing beside the street"}},
        "edges": [
            {"a": "street", "b": "exterior", "class": "walk", "via": stem}
            for stem in SEAMS
        ],
    }

    palette = {
        # measured with block-appearance.py --mix (chroma_mass 0.0047, mossy 10%)
        "paving": [
            {"weight": 8, "block": "minecraft:cobblestone"},
            {"weight": 1, "block": "minecraft:mossy_cobblestone"},
            {"weight": 1, "block": "minecraft:andesite"},
        ],
        "kerb": "minecraft:stone_bricks",
        "wall": "minecraft:stone_bricks",
        "foot": "minecraft:mossy_stone_bricks",
        "cap": "minecraft:chiseled_stone_bricks",
        "lamp": "minecraft:lantern[hanging=false,waterlogged=false]",
    }

    return {
        "version": "1.9.0",
        "name": "saltstair-a-shore-street",
        "start": "place",
        "params": params,
        "palette": palette,
        "rules": rules,
        "contract": contract,
    }


def main():
    alloc = allocation()
    if alloc is None:
        sys.exit("delvec allocation did not give JSON; pass it on stdin")
    out = CAMPAIGN / "programs/shore-street.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(build(alloc), indent=2, sort_keys=True) + "\n")
    print(out)


if __name__ == "__main__":
    main()
