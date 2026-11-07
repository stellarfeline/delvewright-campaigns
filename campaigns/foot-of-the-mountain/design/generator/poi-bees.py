#!/usr/bin/env python3
"""node/poi-bees: the bee garden off the castle road.

A row of three hives on post stands among lavender (allium, lilac) and
flowers, a birch picket fence along the road front and the low west side
with an open gate off the road's path, and a tiny honesty honey stall on
spruce posts at the road edge: a shelf of a crate and a jar under its
own little gable, a lantern hung from the ridge.

    python3 poi-bees.py --allocation <delvec allocation ... node/poi-bees> \
        --out ../../programs/poi-bees.json --delvec <delvec>

Palette, measured with block-appearance.py against the pinned 1.21.11 jar:
stripped_spruce_log #6f5532 (posts), spruce_planks #735531 (shelf board),
spruce stairs (roof), birch fence #c0af79 (pale picket), coarse_dirt
#77563b (worn path), grass_block (garden soil), beehive #a68651, decorated
pot #985e44 (the jar), allium #9f89b8 and lilac #897c7f (the lavender),
cornflower #507993, oxeye daisy, dandelion.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
from starter import Model, run, fence, fence_gate, pillar, lantern, barrel, tall_plant  # noqa: E402

GRASS = "minecraft:grass_block[snowy=false]"
PATH = "minecraft:coarse_dirt"
POST = pillar("stripped_spruce_log")
PICKET = fence("birch")
STAND = fence("spruce")
POT = "minecraft:decorated_pot[cracked=false,facing=north,waterlogged=false]"


def hive(level: int) -> str:
    return f"minecraft:beehive[facing=north,honey_level={level}]"


def build(place):
    m = Model(place)
    w = place.datum.value  # the walk plane
    g = w - 1  # the ground course

    # -- the ground: garden soil to the frame's edge, a worn path off the road
    for x in range(0, m.ex):
        for z in range(0, m.ez):
            m.set(x, g, z, GRASS)
    path = [(2, 0), (5, 0), (2, 1), (5, 1), (5, 2), (2, 2), (2, 3), (2, 4), (3, 4), (4, 4), (5, 4)]
    for x, z in path:
        m.set(x, g, z, PATH)

    # The row under the road's opening (z 1) stays open ground, the room the
    # path steps into; fence, stall and garden stand behind it.

    # -- the picket fence: the road front and the low west side, a gate on the path
    for z in range(2, 7):
        m.set(1, w, z, PICKET)
    m.set(3, w, 2, PICKET)
    m.set(2, w, 2, fence_gate("birch", "north", open=True))
    m.set(3, w + 1, 2, lantern(False))  # a lantern on the gate post

    # -- the honey stall: four posts, a shelf at the back, a little gable roof
    # a post-and-beam front: slim fence posts at the open front, logs at the back
    for x in (4, 6):
        for y in range(w, w + 3):
            m.set(x, y, 2, STAND)
            m.set(x, y, 3, POST)
    m.set(5, w, 3, barrel("north"))  # the crate of jars, the shelf's foot
    m.set(5, w + 1, 3, POT)  # a jar of honey on the shelf
    m.set(5, w + 2, 3, "minecraft:spruce_planks")  # the shelf's head board
    m.roof(4, 6, 2, 3, head=w + 2, along="x", mat="spruce", overhang=0)
    m.set(5, w + 2, 2, lantern(True))  # hung from the roof over the stall's floor
    m.part(4, 6, 2, 3, "honey-stall")

    # -- the hives in a row on post stands, flowers all round them
    for x, lvl in ((2, 3), (4, 5), (6, 2)):
        m.set(x, w, 5, STAND)
        m.set(x, w + 1, 5, hive(lvl))
    flowers = {
        (3, 3): "minecraft:allium",
        (6, 4): "minecraft:cornflower",
        (3, 5): "minecraft:allium",
        (5, 5): "minecraft:oxeye_daisy",
        (3, 6): "minecraft:allium",
        (5, 6): "minecraft:dandelion",
    }
    # flowers at the fence's foot along the open ground before it
    flowers.update({(1, 1): "minecraft:allium", (3, 1): "minecraft:oxeye_daisy", (4, 1): "minecraft:allium",
                    (6, 1): "minecraft:cornflower"})
    for (x, z), f in flowers.items():
        m.set(x, w, z, f)
    for x in (2, 4, 6):
        m.tall(x, w, 6, "lilac")
    m.part(1, 3, 2, 6, "hives")
    m.part(4, 6, 4, 6, "hives")

    m.mark("node-poi-bees", 3, 4, facing="north")
    m.finish()
    return m


raise SystemExit(run(build))
