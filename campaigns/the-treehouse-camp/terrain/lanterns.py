#!/usr/bin/env python3
"""Writes world-edits.json: the lantern posts on the forest floor.

The forest floor is the commons, which no place owns; the camp lights its
paths under the bridges and round the trees' feet with lanterns on posts,
set in the stage-7 edit script (spec-0098 section 10: dressing the commons is
the edit script's). Each post is two spruce fences on the ground with a
lantern on top, at the column's surface read from terrain/heightmap.py.

Positions are world (x, z); the edit script states them relative to
`anchor/node-root-glade`, which stands at world (28, 72, 38).
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import heightmap  # noqa: E402

SPAWN = (28, 72, 38)
POSTS = [
    # the gully under the Long Bridge
    (52, 31), (58, 40), (64, 31), (69, 40),
    # under the Low Bridge
    (31, 52), (40, 58), (31, 64), (40, 66),
    # under the High Bridge, between the Loom and Watch Trees
    (75, 47), (85, 50), (75, 55), (85, 58), (75, 63), (85, 66),
    # round the Watch Tree's foot
    (69, 74), (69, 82), (90, 74), (90, 82), (76, 88), (84, 88), (80, 67),
    # north of the Root Glade
    (31, 22), (38, 22),
    # west of the Root Glade and of the Seed Tree
    (20, 32), (20, 39), (23, 74), (23, 81),
    # south and east of the Seed Tree
    (36, 90), (48, 78),
]


def main():
    y = heightmap.relax()
    edits = []
    for i, (x, z) in enumerate(POSTS):
        top = y[x][z]
        rel = lambda wy: [x - SPAWN[0], wy - SPAWN[1], z - SPAWN[2]]
        frame = {"kind": "anchor-relative", "anchor": "anchor/node-root-glade"}
        edits.append({"verb": "select", "name": f"region/post-{i + 1}",
                      "shape": {"kind": "box", "frame": frame, "min": rel(top + 1), "max": rel(top + 2)}})
        edits.append({"verb": "fill", "region": f"region/post-{i + 1}",
                      "recipe": {"blocks": [{"block": "minecraft:spruce_fence", "weight": 1.0}]}})
        edits.append({"verb": "select", "name": f"region/lamp-{i + 1}",
                      "shape": {"kind": "box", "frame": frame, "min": rel(top + 3), "max": rel(top + 3)}})
        edits.append({"verb": "fill", "region": f"region/lamp-{i + 1}",
                      "recipe": {"blocks": [{"block": "minecraft:lantern[hanging=false,waterlogged=false]", "weight": 1.0}]}})
    doc = {"dsl_version": "0.38.0", "campaign_id": "the-treehouse-camp", "stage": "world-edits",
           "content": {"batches": [{"id": "batch/forest-floor-lanterns", "area": "area/site",
                                    "note": "Lantern posts on the forest floor under the bridges and round the trees' feet.",
                                    "edits": edits}]}}
    out = os.path.join(os.path.dirname(HERE), "world-edits.json")
    json.dump(doc, open(out, "w"), indent=2)
    print(f"wrote {out}: {len(POSTS)} lantern posts", file=sys.stderr)


if __name__ == "__main__":
    main()
