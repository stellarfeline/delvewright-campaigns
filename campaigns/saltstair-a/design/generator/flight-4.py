#!/usr/bin/env python3
"""Emit programs/flight-4.json — the fourth flight of Saltstair.

Provenance only: the emitted JSON is the artifact of record. Every handed
number is a `handed/...` parameter whose default is copied from the
allocation `delvec allocation <campaign> node/flight-4` prints at run time;
nothing here retypes one.
"""
import json
import subprocess
import sys
from pathlib import Path

CAMPAIGN = Path(__file__).resolve().parents[2]
DELVEC = Path.home() / ".delvewright/bin/delvec"
NORTH = "lower-street-flight-4"   # stair seam, plane owned by node/lower-street
SOUTH = "flight-4-shore-street"   # walk seam, plane owned here


def allocation():
    prefabs = CAMPAIGN.parents[1] / "prefabs"
    out = subprocess.run([str(DELVEC), "--prefabs", str(prefabs), "allocation", str(CAMPAIGN), "node/flight-4"],
                         capture_output=True, text=True)
    if out.returncode != 0:
        sys.exit(out.stderr)
    # the JSON object comes first; the ground listings follow it as text
    return json.JSONDecoder().raw_decode(out.stdout)[0]


# ---- expression helpers -------------------------------------------------
def P(name):
    return {"expr": "param", "name": name}


def I(v):
    return {"expr": "int", "value": v}


def add(a, b):
    return {"expr": "arith", "op": "add", "lhs": a, "rhs": b}


def sub(a, b):
    return {"expr": "arith", "op": "sub", "lhs": a, "rhs": b}


def ab(e):
    return {"size": "absolute", "blocks": e}


REL = {"size": "relative", "weight": I(1)}


def split(axis, sizes, children):
    return {"op": "split", "axis": axis, "sizes": sizes, "children": children}


def fill(role):
    return {"op": "fill", "material": {"role": role}}


def call(sym):
    return {"op": "call", "symbol": sym}


def claim(region, body=None):
    return {"op": "claim", "region": region, "body": body or {"op": "void"}}


def eq(name, v):
    return {"cond": "cmp", "lhs": P(name), "op": "eq", "rhs": I(v)}


def seam(s, k):
    return P(f"handed/seam/{s}/{k}")


def span(s, a):  # inclusive extent of a seam along axis a
    return add(sub(seam(s, a + "1"), seam(s, a + "0")), I(1))


def build(alloc):
    seams = {s["edge"].split("/", 1)[1]: s for s in alloc["seams"]}
    params = {"handed/datum-y": alloc["datum_y"]}
    for stem in (NORTH, SOUTH):
        s = seams[stem]
        (x0, y0, z0), (x1, y1, z1) = s["cells"]
        for k, v in dict(x0=x0, y0=y0, z0=z0, x1=x1, y1=y1, z1=z1, rise=s["rise"]).items():
            params[f"handed/seam/{stem}/{k}"] = v
    # local controls, rebound per slice by `bind`
    params.update({"top": 0, "ring": 0, "zone": 0, "post": 0, "post_w": 0, "post_e": 0})

    datum = P("handed/datum-y")
    head_feet = seam(NORTH, "y0")          # walk plane at the head (lower street)
    # Tread block course per slice, north (z0) to south. The head pair is
    # pinned to the lower street's walk plane, the foot pair to the datum.
    top_head = sub(head_feet, I(1))          # top step, in the lower street's opening layer
    top_upper = sub(head_feet, I(2))         # upper landing and its riser
    top_lower = add(datum, I(1))             # lower landing and its riser
    top_foot = datum                         # first step off the shore street
    #            top        ring       zone tread     post_w post_e
    slices = [
        (top_head,  top_head,  0, "step",    1, 1),
        (top_upper, top_upper, 1, "landing", 0, 0),
        (top_upper, top_upper, 2, "step",    0, 0),
        (top_lower, top_lower, 3, "landing", 0, 0),
        (top_lower, top_lower, 4, "step",    1, 0),
        (top_foot,  top_foot,  5, "step",    0, 0),
        (top_foot,  datum,     6, "landing", 0, 1),
    ]
    children = []
    for top, ring, zone, tread, pw, pe in slices:
        children.append({
            "op": "bind",
            "params": {"top": top, "ring": ring, "zone": I(zone), "post_w": I(pw), "post_e": I(pe)},
            "palette": {"tread": {"role": tread}},
            "body": call("slice"),
        })

    rules = {
        # one-cell slices down the flight, north to south; the last is the
        # south face, whose opening this place owns
        "place": [{"weight": 1, "body": split("z", [ab(I(1))] * 6 + [REL], children)}],
        # west kerb | the lane the two seams share | east kerb
        "slice": [{"weight": 1, "body": split("x", [
            ab(seam(SOUTH, "x0")), ab(span(SOUTH, "x")), REL], [
            {"op": "bind", "params": {"post": P("post_w")}, "body": call("kerb")},
            call("lane"),
            {"op": "bind", "params": {"post": P("post_e")}, "body": call("kerb")},
        ])}],
        # a kerb course standing on the ring's ground; at a post, two more
        # courses and a lantern on top
        "kerb": [
            {"weight": 1, "when": eq("post", 1), "body": split("y", [
                ab(add(P("ring"), I(1))), ab(I(1)), ab(I(1)), ab(I(1)), REL], [
                {"op": "skip"}, fill("kerb"), fill("post"), fill("lamp"), claim("coping")])},
            {"weight": 1, "when": {"cond": "otherwise"}, "body": split("y", [
                ab(add(P("ring"), I(1))), ab(I(1)), REL], [
                {"op": "skip"}, fill("kerb"), claim("coping")])},
        ],
        "lane": [
            # the south face: the street runs on at grade through the whole opening
            {"weight": 1, "when": eq("zone", 6), "body": split("y", [
                ab(seam(SOUTH, "y0")), ab(span(SOUTH, "y")), REL], [
                {"op": "skip"}, claim("shore-street-way"), {"op": "void"}])},
            # the first step off the shore street: its tread is foot space too,
            # since the opening's lowest course meets the step, not the air over it
            {"weight": 1, "when": eq("zone", 5), "body": split("y", [
                ab(P("top")), REL], [
                fill("ground"), claim("foot", split("y", [ab(I(1)), REL], [fill("tread"), {"op": "void"}]))])},
            # every other slice: ground down to the terrain, one tread, air
            {"weight": 1, "when": {"cond": "otherwise"}, "body": split("y", [
                ab(P("top")), ab(I(1)), REL], [
                fill("ground"), fill("tread"), call("lane_air")])},
        ],
        "lane_air": [
            {"weight": 1, "when": eq("zone", 0), "body": split("y", [
                ab(span(NORTH, "y")), REL], [claim("lower-street-way"), {"op": "void"}])},
            {"weight": 1, "when": eq("zone", 1), "body": claim("head")},
            {"weight": 1, "when": eq("zone", 2), "body": claim("flight")},
            {"weight": 1, "when": eq("zone", 3), "body": {
                "op": "mark", "mark": {"anchor": "node-flight-4", "at": "floor_center", "facing": "north"},
                "body": claim("foot")}},
            {"weight": 1, "when": eq("zone", 4), "body": claim("foot")},
        ],
    }

    palette = {
        "ground": "minecraft:dirt",
        "step": {"local": "minecraft:stone_brick_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]"},
        "landing": "minecraft:stone_bricks",
        "tread": "minecraft:stone_bricks",
        "kerb": [
            {"weight": 6, "block": "minecraft:stone_bricks"},
            {"weight": 3, "block": "minecraft:mossy_stone_bricks"},
            {"weight": 1, "block": "minecraft:cracked_stone_bricks"},
        ],
        "post": "minecraft:stone_bricks",
        "lamp": "minecraft:lantern[hanging=false,waterlogged=false]",
    }

    contract = {
        "entry": "foot",
        "spaces": {"foot": {"envelope": "open"}, "head": {"envelope": "open"}},
        "no_body": {"coping": {"reason": "the top of the kerb walls and their lantern posts, beside the treads; nobody walks the kerb"}},
        "edges": [
            {"a": "foot", "b": "exterior", "class": "walk", "via": "shore-street-way"},
            {"a": "foot", "b": "head", "class": "stair", "rise": 3, "via": "flight"},
            {"a": "head", "b": "exterior", "class": "walk", "via": "lower-street-way"},
        ],
    }
    return {
        "version": "1.9.0",
        "name": "saltstair-a-flight-4",
        "start": "place",
        "params": params,
        "palette": palette,
        "rules": rules,
        "contract": contract,
    }


if __name__ == "__main__":
    prog = build(allocation())
    out = CAMPAIGN / "programs" / "flight-4.json"
    out.write_text(json.dumps(prog, indent=2, sort_keys=True) + "\n")
    print(out)
