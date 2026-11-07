#!/usr/bin/env python3
"""node/poi-lookout — the lookout on a bend of the castle road.

Scene: a small stone platform built out from the falling slope below the
castle road, paved in worn stone brick on a rubble retaining wall, a stone
parapet round its three open sides with a lantern on each seaward corner,
a spruce bench facing south over the rail, and a walkers' cairn heaped in
the south-east corner; a body steps off the road onto it, sits, and looks
down over the town, the harbour and the sea.

Palette, measured with tools/creator/block-appearance.py --mix:
  paving   stone_bricks 6 / cracked 2 / mossy 2   mean #787976, chroma_mass 0.0076
  rubble   cobblestone 5 / mossy 3 / andesite 2   mean #7c7e78, chroma_mass 0.0121
  bench    spruce_planks family                   mean #735531
"""

import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
from starter import Model, run, stairs, slab, wall, lantern  # noqa: E402


def build(place):
    m = Model(place)
    m.palette["paving"] = [
        {"weight": 6, "block": "minecraft:stone_bricks"},
        {"weight": 2, "block": "minecraft:cracked_stone_bricks"},
        {"weight": 2, "block": "minecraft:mossy_stone_bricks"},
    ]
    m.palette["rubble"] = [
        {"weight": 5, "block": "minecraft:cobblestone"},
        {"weight": 3, "block": "minecraft:mossy_cobblestone"},
        {"weight": 2, "block": "minecraft:andesite"},
    ]
    m.palette["kerb"] = "minecraft:stone_bricks"
    m.palette["rail"] = wall("stone_brick")

    lo, hi = place.space
    x0, x1 = lo[0], hi[0]
    z0, z1 = lo[2], hi[2]
    w = place.datum.value          # the walk plane
    g = w - 1                      # the platform's paving course

    # The platform, built out from the slope: a rubble retaining wall under
    # the whole frame (the ring included, so its outer faces are masonry where
    # the slope falls away), a coping of whole stone brick on the ring, worn
    # paving inside. Cells under the terrain are the whole's and stay so.
    for x in range(m.ex):
        for z in range(m.ez):
            inside = x0 <= x <= x1 and z0 <= z <= z1
            for y in range(0, g):
                m.set(x, y, z, "rubble")
            m.set(x, g, z, "paving" if inside else "kerb")

    # The parapet round the three open sides; the north stays open to the road.
    for z in range(z0 + 1, z1 + 1):
        m.set(x0, w, z, "rail")
        m.set(x1, w, z, "rail")
    for x in range(x0, x1 + 1):
        m.set(x, w, z1, "rail")
    # a lantern standing on each seaward corner post
    m.set(x0, w + 1, z1, lantern(False))
    m.set(x1, w + 1, z1, lantern(False))

    # A planter each side of the way in, flowers in soil let into the paving.
    for x, flower in ((x0 + 1, "minecraft:cornflower"), (x1 - 1, "minecraft:poppy")):
        m.set(x, g, z0 + 1, "minecraft:grass_block[snowy=false]")
        m.set(x, w, z0 + 1, flower)

    # The bench: two spruce stairs, backs to the road, facing the view.
    by = z1 - 2
    for x in (x0 + 1, x0 + 2):
        m.set(x, w, by, stairs("spruce", "north"))

    # The cairn in the south-east corner: a heap of field stones, one upright on top.
    cx, cz = x1 - 1, z1 - 1
    m.set(cx, w, cz, "minecraft:mossy_cobblestone")
    m.set(cx, w + 1, cz, wall("cobblestone"))
    m.set(cx, w, cz - 1, slab("cobblestone"))
    m.set(cx - 1, w, cz, slab("andesite"))

    m.part(x0, x1, z0 + 2, z1, "lookout")  # the row behind the way in stays the room
    m.mark("node-poi-lookout", x0 + 2, z0 + 2, facing="south")
    m.finish()
    return m


raise SystemExit(run(build))
