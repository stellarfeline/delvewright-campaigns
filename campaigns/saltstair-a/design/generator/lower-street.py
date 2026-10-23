#!/usr/bin/env python3
"""Emit programs/lower-street.json — the lower street of Saltstair.

Every handed number is read from `delvec allocation` and declared as a
`handed/...` parameter default; the rules read those parameters, never literals.
"""
import json, subprocess, sys
from pathlib import Path

CAMPAIGN = Path(__file__).resolve().parents[2]
DELVEC = str(Path.home() / ".delvewright/bin/delvec")
PLACE = "node/lower-street"

N, S, E = "flight-3-lower-street", "lower-street-flight-4", "lower-street-ropewalk"


def allocation():
    out = subprocess.run([DELVEC, "allocation", str(CAMPAIGN), PLACE, "--json"],
                         capture_output=True, text=True)
    if out.returncode == 0 and out.stdout.lstrip().startswith("{"):
        return json.loads(out.stdout)
    out = subprocess.run([DELVEC, "allocation", str(CAMPAIGN), PLACE],
                         capture_output=True, text=True, check=True)
    s = out.stdout
    i = s.index("{")
    return json.JSONDecoder().raw_decode(s[i:])[0]


def i(v): return {"expr": "int", "value": v}
def p(n): return {"expr": "param", "name": n}
def ar(op, a, b): return {"expr": "arith", "op": op, "lhs": a, "rhs": b}
def sp(n, c): return p(f"handed/seam/{n}/{c}")
def span(n, a):  # inclusive extent of a seam along axis a
    return ar("add", ar("sub", sp(n, a + "1"), sp(n, a + "0")), i(1))
def ab(e): return {"size": "absolute", "blocks": e if isinstance(e, dict) else i(e)}
def rel(w=1): return {"size": "relative", "weight": i(w)}
def split(axis, sizes, children):
    return {"op": "split", "axis": axis, "sizes": sizes, "children": children}
def call(s): return {"op": "call", "symbol": s}
def fill(r): return {"op": "fill", "material": {"role": r}}
def claim(region, body=None): return {"op": "claim", "region": region, "body": body or {"op": "void"}}
VOID = {"op": "void"}
SKIP = {"op": "skip"}
def rule(body): return [{"weight": 1, "body": body}]


def main():
    a = allocation()
    params = {
        "handed/datum-y": a["datum_y"],
        "handed/ground/bottom-y": a["ground"]["bottom_y"],
    }
    for s in a["seams"]:
        stem = s["edge"].split("/", 1)[1]
        (x0, y0, z0), (x1, y1, z1) = s["cells"]
        for k, v in dict(x0=x0, y0=y0, z0=z0, x1=x1, y1=y1, z1=z1, rise=s["rise"]).items():
            params[f"handed/seam/{stem}/{k}"] = v

    ground_h = ar("sub", p("handed/datum-y"), p("handed/ground/bottom-y"))
    west_w = sp(N, "x0")                      # the west ring: columns west of the street
    door_off = ar("sub", sp(E, "z0"), ar("add", sp(N, "z0"), i(1)))  # street rows before the door

    rules = {
        "place": rule({
            "op": "mark",
            "mark": {"anchor": "node-lower-street", "at": "offset", "facing": "south",
                     "x": ar("div", ar("add", sp(N, "x0"), sp(N, "x1")), i(2)),
                     "y": p("handed/datum-y"),
                     "z": ar("div", sp(S, "z0"), i(2))},
            "body": split("y", [ab(ground_h), rel()], [call("ground"), call("above")]),
        }),
        # --- the ground course: cobbles between stone-brick kerbs ---------------
        "ground": rule(split("x", [ab(west_w), rel()], [SKIP, call("ground-street")])),
        "ground-street": rule(split("z", [rel(), ab(1)], [call("paving"), SKIP])),
        "paving": rule(split("x", [ab(1), rel(), ab(1)],
                             [fill("kerb"), fill("paving"), fill("kerb")])),
        # --- above the ground: the west parapet and the street's air ------------
        "above": rule(split("x", [ab(west_w), rel()], [call("west-parapet"), call("street")])),
        "west-parapet": rule(split("z",
            [ab(1), ab(door_off), ab(span(E, "z")), rel(), ab(1)],
            [call("post"), call("parapet"), call("post"), call("parapet"), call("post")])),
        "post": rule(split("y", [ab(1), ab(1), ab(1), ab(1), rel()],
                           [fill("foot"), fill("kerb"), fill("lamp"), claim("lamp-head"), VOID])),
        "parapet": rule(split("y", [ab(1), ab(1), rel()],
                              [fill("foot"), fill("coping"), VOID])),
        "street": rule(split("z",
            [ab(span(N, "z")), rel(), ab(span(S, "z"))],
            [claim(N), call("street-run"), call("south-face")])),
        "street-run": rule(split("x", [rel(), ab(span(E, "x"))],
                                 [claim("street"), call("east-lane")])),
        "east-lane": rule(split("z", [ab(door_off), ab(span(E, "z")), rel()],
                                [claim("street"), call("door-column"), claim("street")])),
        "door-column": rule(split("y", [ab(span(E, "y")), rel()],
                                  [claim(E), claim("street")])),
        "south-face": rule(split("y", [ab(span(S, "y")), rel()], [claim(S), VOID])),
    }

    prog = {
        "version": "1.12.0",
        "name": "saltstair-a-lower-street",
        "start": "place",
        "params": params,
        "palette": {
            "paving": [{"weight": 7, "block": "minecraft:cobblestone"},
                       {"weight": 1, "block": "minecraft:mossy_cobblestone"}],
            "kerb": "minecraft:stone_bricks",
            "foot": "minecraft:mossy_stone_bricks",
            "coping": "minecraft:stone_brick_wall[east=none,north=low,south=low,up=false,waterlogged=false,west=none]",
            "lamp": "minecraft:lantern[hanging=false,waterlogged=false]",
        },
        "rules": rules,
        "contract": {
            "entry": "street",
            "spaces": {"street": {"envelope": "open"}},
            "no_body": {"lamp-head": {"reason": "the air over a kerb-post lantern, which nobody is meant to stand on"}},
            "edges": [
                {"a": "exterior", "b": "street", "class": "walk", "via": N},
                {"a": "street", "b": "exterior", "class": "walk", "via": S},
                {"a": "street", "b": "exterior", "class": "walk", "via": E},
            ],
        },
        "shown_faces": ["west"],
    }
    out = CAMPAIGN / "programs" / "lower-street.json"
    out.write_text(json.dumps(prog, indent=2, sort_keys=True) + "\n")
    print(out)


if __name__ == "__main__":
    main()
