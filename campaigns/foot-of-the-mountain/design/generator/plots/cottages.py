#!/usr/bin/env python3
"""node/cottages: a pair of fishermen's cottages on stretch 2's west side.

    DELVEWRIGHT_SKILL=<skill> python3 cottages.py --allocation <delvec allocation ... node/cottages> \\
        --out ../../../programs/cottages.json --delvec <delvec>

Form, after the fishermen's cottages of a harbour town (low, one storey and a
loft, whitewashed over a rubble base, the door to a small front garden, the
work of the sea — nets, pots, a boat's oars — about the yard behind): two
cottages gable-end to the street, staggered on the slope, each a front room
with its hearth and a back room with the bed through a door; front gardens
of flowers to the street, a shared back yard with a washing line, lobster
pots and a bench.

Piece-local axes: +x east (the street), +z south; the street's opening is the
play space's last column (x 20), kept clear with the verge beside it (x 19).
The lot is ten deep (z 1..10): each cottage five.
Drawn on the skill starter alone (its Model, its block constructors and
Model.roof); the engine says where a body goes.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
from starter import (Model, barrel, campfire, candle, chain, fence, grass_block, lantern, leaves,  # noqa: E402
                     pane, pillar, run, slab, stairs, trapdoor)

GRASS = grass_block()
GLASS = pane("glass_pane")
ROOF = "minecraft:deepslate_tile"


def cottage(m, x0, x1, z0, z1, wash, post, door_z, part_wall_x, colour, flip):
    """One cottage: a rubble base course, whitewash or timber walls, a loft
    under a tiled gable roof to the street; the front room (east) and the back
    room (west) through a door in the cross wall."""
    corners = {(x0, z0), (x1, z0), (x0, z1), (x1, z1)}
    outline = [(x, z) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1) if x in (x0, x1) or z in (z0, z1)]
    for (x, z) in outline:
        m.set(x, 1, z, "rubble")
        for y in (2, 3):
            m.set(x, y, z, post if (x, z) in corners else wash)
        m.set(x, 4, z, post if (x, z) in corners else wash)
    m.box(x0 + 1, x1 - 1, 4, 4, z0 + 1, z1 - 1, "minecraft:spruce_planks")       # the loft floor
    top = m.roof(x0, x1, z0, z1, 4, "x", ROOF, fill=wash)
    # the chimney at the back gable, from the front room's hearth
    for y in range(1, top + 2):
        m.set(part_wall_x, y, z1 if flip else z0, "rubble")
    # the street door into the front room, a window either side of it
    m.door(x1, 1, door_z, "spruce", "west")
    for z in range(z0 + 1, z1):
        if z != door_z:
            m.set(x1, 2, z, GLASS)
    m.set(x1, 3, door_z, wash)
    # the cross wall and its door
    for z in range(z0 + 1, z1):
        for y in (1, 2, 3):
            m.set(part_wall_x, y, z, wash)
    dz = (z0 + z1) // 2
    m.door(part_wall_x, 1, dz, "spruce", "east")
    m.set(part_wall_x, 3, dz, wash)
    # the back room's window to the yard
    m.set(x0, 2, dz, GLASS)
    # floors
    m.box(x0 + 1, x1 - 1, 0, 0, z0 + 1, z1 - 1, "minecraft:spruce_planks")
    # the front room: the hearth at the chimney, a table and a stool, a lantern
    hz = z1 - 1 if flip else z0 + 1
    m.set(part_wall_x + 1, 1, hz, campfire("east"))
    m.set(x1 - 1, 1, hz, slab("spruce", "top"))
    m.set(x1 - 1, 2, hz, candle(1, "white", True))
    m.set(part_wall_x + 1, 3, dz, lantern(True))
    # the back room: the bed, a chest-high shelf
    m.bed(x0 + 1, 1, z0 + 1 if not flip else z1 - 1, colour, "east")
    m.set(x0 + 1, 3, dz, lantern(True))
    return top


def build(place) -> Model:
    m = Model(place)
    m.palette.update({
        "floor": GRASS,
        "rubble": [{"weight": 6, "block": "minecraft:cobblestone"},
                   {"weight": 3, "block": "minecraft:mossy_cobblestone"},
                   {"weight": 1, "block": "minecraft:stone"}],
        "wash": "minecraft:calcite",
        "yard": [{"weight": 5, "block": "minecraft:grass_block[snowy=false]"},
                 {"weight": 2, "block": "minecraft:coarse_dirt"},
                 {"weight": 1, "block": "minecraft:dirt_path"}],
    })
    m.box(1, 18, 0, 0, 1, 10, "yard")

    # the first cottage, whitewashed, north; the second, timber and daub, a
    # cell back on the slope, south
    cottage(m, 10, 16, 1, 5, "wash", pillar("spruce_log", "y"), 3, 13, "blue", False)
    cottage(m, 9, 15, 6, 10, "minecraft:mud_bricks", pillar("dark_oak_log", "y"), 8, 12, "red", True)
    m.part(10, 16, 1, 5, "cottage-a")
    m.part(9, 15, 6, 10, "cottage-b")

    # the front gardens to the street: paths, flower beds, a low hedge
    for z in (3, 8):
        for x in range(17 if z == 3 else 16, 19):
            m.set(x, 0, z, "minecraft:dirt_path")
    for cells, blooms in (([(17, 2), (18, 2), (17, 5), (18, 5)],
                           ["minecraft:poppy", "minecraft:cornflower", "minecraft:oxeye_daisy"]),
                          ([(16, 7), (17, 7), (16, 10), (17, 10), (18, 10)],
                           ["minecraft:dandelion", "minecraft:allium", "minecraft:azure_bluet"])):
        for i, (x, z) in enumerate(cells):
            m.set(x, 0, z, GRASS)
            m.set(x, 1, z, blooms[i % len(blooms)])
    m.set(18, 1, 1, "minecraft:potted_red_tulip")
    m.set(18, 0, 6, GRASS); m.set(18, 1, 6, leaves("azalea"))
    m.part(17, 18, 1, 10, "gardens")

    # the shared back yard: a washing line between posts, lobster pots, oars,
    # a bench and a barrel of salt
    for z in (2, 8):
        for y in (1, 2, 3):
            m.set(3, y, z, fence("spruce"))
    for z in range(3, 8):
        m.set(3, 3, z, chain("z"))
    for (x, z) in ((6, 2), (7, 2)):
        m.set(x, 1, z, trapdoor("spruce", "north", "top"))    # a lobster pot on its frame
    m.set(6, 1, 10, stairs("spruce", "north")); m.set(7, 1, 10, stairs("spruce", "north"))
    m.set(5, 1, 10, barrel("up"))
    m.set(8, 1, 1, fence("spruce")); m.set(8, 2, 1, fence("spruce"))   # oars stood against the wall
    m.set(2, 0, 10, GRASS); m.set(2, 1, 10, leaves("oak"))
    m.set(2, 0, 1, GRASS); m.set(2, 1, 1, leaves("azalea"))
    for y in (1, 2, 3):
        m.set(6, y, 6, fence("spruce"))
    m.set(6, 4, 6, lantern(False))
    m.part(2, 7, 3, 8, "gardens")

    m.mark("node-cottages", 17, 3, "west")
    m.finish()
    return m


if __name__ == "__main__":
    raise SystemExit(run(build, reason="the roof slopes, the wall heads and the lofts: seen, never stood on"))
