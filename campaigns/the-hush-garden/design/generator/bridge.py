#!/usr/bin/env python3
"""node/bridge — the plank bridge across the top of the maze.

A deck of spruce planks three wide, framed by dark oak stringers along both
edges and dark oak cross beams on a six-cell module; a spruce-fence rail on
each side, broken by stripped dark oak posts on the same module, each post
carrying a lantern; the gate-tower end framed by two full-height posts round
the iron grille. Every handed value is read through the starter.
"""

import json
import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
from starter import Model, run, fence, full_state, lantern, pillar  # noqa: E402

GRILLES: dict = {}  # bar role -> the handed bar block
MODULE = 6  # the bay: posts and cross beams stand on every sixth column


def build(place):
    m = Model(place)
    (x0, _, z0), (x1, _, z1) = place.space
    d = place.datum.value
    g = d - 1  # the deck course
    top = place.space[1][1]
    ex = place.ex
    zr0, zr1 = z0 - 1, z1 + 1  # the two rail lines (the ring)

    m.palette["deck"] = [
        {"weight": 7, "block": "minecraft:spruce_planks"},
        {"weight": 2, "block": pillar("minecraft:stripped_spruce_log", "z")},
    ]
    m.palette["stringer"] = pillar("minecraft:dark_oak_log", "x")
    m.palette["beam"] = pillar("minecraft:dark_oak_log", "z")
    m.palette["post"] = pillar("minecraft:stripped_dark_oak_log", "y")
    m.palette["rail"] = fence("spruce")
    m.palette["light"] = lantern()
    # each bar this place owns, in the block the seam hands (the survey reads
    # it before the starter binds it)
    for s in place.seams:
        if s["bar"] is not None:
            m.palette[f"bar-{s['stem']}"] = full_state(s["seam"]["bar_block"])
            GRILLES[f"bar-{s['stem']}"] = s["seam"]["bar_block"]

    # the deck: planks between two stringers, a cross beam every bay
    for x in range(x0, ex):
        for z in range(zr0, zr1 + 1):
            if x % MODULE == 0:
                m.set(x, g, z, "beam")
            elif z in (zr0, zr1):
                m.set(x, g, z, "stringer")
            elif x <= x1:
                m.set(x, g, z, "deck")

    # the rail: fence on both edges, a post with a lantern every bay, open above
    for x in range(x0, x1 + 1):
        for z in (zr0, zr1):
            if x % MODULE == 0:
                m.set(x, d, z, "post")
                m.set(x, d + 1, z, "light")
                for y in range(d + 2, top + 1):
                    m.set(x, y, z, "minecraft:air")
            else:
                m.set(x, d, z, "rail")
                for y in range(d + 1, top + 1):
                    m.set(x, y, z, "minecraft:air")

    # the gate-tower end: two posts the full height of the grille
    for z in (zr0, zr1):
        for y in range(d, top + 1):
            m.set(ex - 1, y, z, "post")
    m.show("up")  # the end posts' heads stand on the frame's top course, seen from the sky

    m.mark("node-bridge", (x0 + x1) // 2, (z0 + z1) // 2, facing="east")
    m.finish()
    return m


def join_grilles(path: str) -> None:
    """The starter binds a bar's role to its block with every arm false: a
    row of lone iron posts, 7/8 of a block apart, which a body slips between.
    The grille spans the opening north to south between the two end posts, so
    each bar is written joined along it, as the game joins a placed row."""
    with open(path, encoding="utf-8") as f:
        doc = json.load(f)
    n = 0
    for role, block in GRILLES.items():
        if not block.endswith("iron_bars"):
            continue
        doc["palette"][role] = "minecraft:iron_bars[east=false,north=true,south=true,waterlogged=false,west=false]"
        n += 1
    assert n == len(GRILLES) == 1, f"joined {n} grille(s) of {len(GRILLES)}"
    with open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(doc, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


status = run(build)
if status == 0:
    join_grilles(sys.argv[sys.argv.index("--out") + 1])
raise SystemExit(status)
