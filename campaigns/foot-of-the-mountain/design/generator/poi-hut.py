#!/usr/bin/env python3
"""node/poi-hut — the herder's hut above the castle road.

A rubble-stone bothy, one snug room (a bunk, a little stove), its back to the
slope and its door to the road; against its east wall a plank lean-to over
hay, a milking stool and a pail. A pot of flowers by the step.

Palette, measured with block-appearance.py --mix (pinned 1.21.11 jar):
cobblestone C 0.0008, mossy_cobblestone C 0.037 (13 % of area, the loudest),
stripped_spruce_log C 0.062, spruce planks/stairs C 0.065; mean #766752.
One structural material (rubble stone) and one infill (spruce boards).
"""
import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
from starter import Model, run, slab, pillar, fence, pane, lantern, leaves  # noqa: E402

WOOD = "spruce"


def build(place):
    m = Model(place)
    m.palette["rubble"] = [
        {"weight": 5, "block": "minecraft:cobblestone"},
        {"weight": 2, "block": "minecraft:mossy_cobblestone"},
    ]
    m.palette["boards"] = "minecraft:spruce_planks"
    d = place.datum.value          # the walk plane; the floor course is d - 1
    g = d - 1
    head = d + 2                   # the wall plate: door head, window head, eave line

    # ---- the hut: rubble walls on x1..4, z1..4; a 2x2 room inside ----
    x0, x1, z0, z1 = 1, 4, 1, 4
    m.box(x0, x1, g, g, z0, z1, "rubble")              # footing
    m.box(x0 + 1, x1 - 1, g, g, z0 + 1, z1 - 1, "boards")  # board floor
    m.hollow(x0, x1, d, head - 1, z0, z1, "rubble")
    # the wall plate: a spruce beam over every opening, posts at the corners
    for x in range(x0, x1 + 1):
        for z in (z0, z1):
            m.set(x, head, z, pillar("minecraft:stripped_spruce_log", "x"))
    for z in range(z0 + 1, z1):
        for x in (x0, x1):
            m.set(x, head, z, pillar("minecraft:stripped_spruce_log", "z"))
    for x in (x0, x1):
        for z in (z0, z1):
            for y in range(d, head + 1):
                m.set(x, y, z, pillar("minecraft:spruce_log", "y"))
    m.clear(x0 + 1, x1 - 1, d, head, z0 + 1, z1 - 1)
    # the gable roof, ridge running north-south, boards in the gables
    m.roof(x0, x1, z0, z1, head, "z", WOOD, fill="boards", overhang=0)
    # the chimney off the stove, up the north gable
    for y in range(head + 1, head + 4):
        m.set(3, y, z0, "rubble")
    m.set(3, head + 4, z0, "minecraft:cobblestone_wall[east=none,north=none,south=none,up=true,waterlogged=false,west=none]")
    # the door to the road, a window beside it and one to the west
    m.door(3, d, z1, WOOD, "north")
    m.set(2, d + 1, z1, pane())
    m.set(x0, d + 1, 3, pane())
    # inside: the bunk along the west wall, the stove against the north wall
    m.bed(2, d, 3, "brown", "north")
    m.set(3, d, 2, "minecraft:smoker[facing=south,lit=true]")
    m.set(3, d + 1, 3, "minecraft:air")
    m.part(x0, x1, z0, z1, "hut")

    # ---- the lean-to and its yard: x5..6 against the hut's east wall ----
    m.box(5, 6, g, g, 1, 4, "minecraft:coarse_dirt")
    for z in range(1, 5):
        m.set(5, head, z, slab(WOOD, "top"))
        m.set(6, head, z, slab(WOOD, "bottom"))
    # the open east side railed: posts at the corners, a rail between, the
    # roof's outer edge standing on something all along
    for z in (1, 3, 4):
        for y in (d, d + 1):
            m.set(6, y, z, fence(WOOD))
    for c in ((5, d, 1), (5, d + 1, 1), (6, d, 2)):
        m.set(*c, pillar("minecraft:hay_block", "y"))
    m.set(6, d + 1, 2, lantern())                          # on the hay, under the boards
    m.set(5, d, 2, "minecraft:cauldron")                    # the pail
    m.set(5, d, 3, slab(WOOD, "bottom"))                   # the milking stool beside it
    # the front of the plot: the worn path to the door, the pot on the step, a bush
    for z in range(5, 8):
        m.set(3, g, z, "minecraft:dirt_path")
    m.set(2, d, 5, "minecraft:potted_red_tulip")
    m.set(1, d, 5, leaves(WOOD))
    m.set(6, g, 5, "minecraft:podzol[snowy=false]")
    m.tall(6, d, 5, "minecraft:large_fern")
    m.part(5, 6, 1, 4, "hut-yard")
    m.part(1, 6, 5, 5, "hut-yard")

    m.mark("node-poi-hut", 4, 5, facing="north")
    m.finish()
    return m


raise SystemExit(run(build, reason="the hut's roof slopes, the lean-to's boards, the hay and the wall heads: seen, never stood on"))
