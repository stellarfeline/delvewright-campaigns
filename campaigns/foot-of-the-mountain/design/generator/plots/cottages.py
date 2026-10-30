#!/usr/bin/env python3
"""node/cottages: a pair of fishermen's cottages on stretch 2's west side.

    DELVEWRIGHT_SKILL=<skill> python3 cottages.py --allocation <delvec allocation ... node/cottages> \\
        --out ../../../programs/cottages.json --delvec <delvec>

Form, after the fishermen's cottages of a harbour town (low, one storey and a
loft, whitewashed over a rubble base, the door to a small front garden, the
work of the sea — nets, pots, a boat's oars — about the yard behind): two
cottages gable-end to the street, staggered on the slope, each a front room
with its hearth at the street end and the bed at the back; front gardens
of flowers to the street, a shared back yard with a washing line, lobster
pots and a bench.

Piece-local axes: +x east (the street), +z south; the street's opening is the
play space's last column (x 20), kept clear with the verge beside it (x 19).
Drawn on the skill starter's Model; the engine says where a body goes.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from starter import Model, run  # noqa: E402
from kit import (bed2, bed_of, campfire, candle, door2, fence, gable_roof, lantern, leaves, log, pane,  # noqa: E402
                 ring, slab, stairs, trapdoor, wall_torch, window)

GRASS = "minecraft:grass_block[snowy=false]"
GLASS = pane("minecraft:glass_pane")
ROOF = "minecraft:deepslate_tile"


def cottage(m, x0, x1, z0, z1, wash, post, door_z, part_wall_x, colour, flip):
    """One cottage: a rubble base course, whitewash or timber walls, a loft
    under a tiled gable roof to the street; one room, the hearth at its street
    end and the bed at its back."""
    corners = {(x0, z0), (x1, z0), (x0, z1), (x1, z1)}
    for (x, z) in ring(x0, x1, z0, z1):
        m.set(x, 1, z, "rubble")
        for y in (2, 3):
            m.set(x, y, z, post if (x, z) in corners else wash)
        m.set(x, 4, z, post if (x, z) in corners else wash)
    m.box(x0 + 1, x1 - 1, 4, 4, z0 + 1, z1 - 1, "minecraft:spruce_planks")       # the loft floor
    top = gable_roof(m, x0, x1, z0, z1, 4, "x", ROOF, fill=wash)
    # the chimney at the back gable, from the front room's hearth
    for y in range(1, top + 2):
        m.set(part_wall_x, y, z1 if flip else z0, "rubble")
    # the street door into the front room, a window either side of it
    door2(m, x1, door_z, "minecraft:spruce", "west")
    m.set(x1, 0, door_z, "minecraft:spruce_planks")              # the threshold
    for z in range(z0 + 1, z1):
        if z != door_z:
            m.set(x1, 2, z, GLASS)
    m.set(x1, 3, door_z, wash)
    # one room under the loft, the hearth at one end and the bed at the other
    dz = (z0 + z1) // 2
    # the back room's window to the yard
    m.set(x0, 2, dz, GLASS)
    # floors
    m.box(x0 + 1, x1 - 1, 0, 0, z0 + 1, z1 - 1, "minecraft:spruce_planks")
    # the front room: the hearth at the chimney, a table and a stool, a lantern
    hz = z1 - 1 if flip else z0 + 1
    m.set(part_wall_x + 1, 1, hz, campfire("east"))
    m.set(x1 - 1, 1, hz, slab("minecraft:spruce", "top"))
    m.set(x1 - 1, 2, hz, candle(1))
    m.set(part_wall_x + 1, 3, dz, lantern(True))
    # the back room: the bed, a chest-high shelf
    bed2(m, x0 + 1, z0 + 1 if not flip else z1 - 1, colour, "east")
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
    m.box(1, 18, 0, 0, 1, 12, "yard")

    # the first cottage, whitewashed, north; the second, timber and daub, a
    # cell back on the slope, south
    cottage(m, 10, 16, 1, 6, "wash", log("minecraft:spruce_log", "y"), 4, 13, "blue", False)
    cottage(m, 9, 15, 7, 11, "minecraft:mud_bricks", log("minecraft:dark_oak_log", "y"), 9, 12, "red", True)
    m.part(10, 16, 1, 6, "cottage-a")
    m.part(9, 15, 7, 11, "cottage-b")

    # the front gardens to the street: paths, flower beds, a low hedge
    for z in (4, 9):
        for x in range(17 if z == 4 else 16, 19):
            m.set(x, 0, z, "minecraft:dirt_path")
    bed_of(m, [(17, 2), (18, 2), (17, 6), (18, 6)],
           ["minecraft:poppy", "minecraft:cornflower", "minecraft:oxeye_daisy"])
    bed_of(m, [(16, 8), (17, 8), (16, 11), (17, 11), (18, 11)],
           ["minecraft:dandelion", "minecraft:allium", "minecraft:azure_bluet"])
    m.set(18, 1, 3, "minecraft:potted_red_tulip")
    m.set(18, 0, 7, GRASS); m.set(18, 1, 7, leaves("minecraft:azalea"))
    m.part(17, 18, 1, 3, "gardens")
    m.part(17, 18, 5, 12, "gardens")

    # the shared back yard: a washing line between posts, lobster pots, oars,
    # a bench and a barrel of salt
    for z in (3, 9):
        for y in (1, 2, 3):
            m.set(3, y, z, fence("minecraft:spruce"))
    for z in range(4, 9):
        m.set(3, 3, z, "minecraft:iron_chain[axis=z,waterlogged=false]")
    for (x, z) in ((6, 3), (7, 3)):
        m.set(x, 1, z, trapdoor("minecraft:spruce", "north", "top"))    # a lobster pot on its frame
    m.set(6, 1, 10, stairs("minecraft:spruce", "north")); m.set(7, 1, 10, stairs("minecraft:spruce", "north"))
    m.set(5, 1, 10, "minecraft:barrel[facing=up,open=false]")
    m.set(8, 1, 1, fence("minecraft:spruce")); m.set(8, 2, 1, fence("minecraft:spruce"))   # oars stood against the wall
    m.set(2, 0, 11, GRASS); m.set(2, 1, 11, leaves("minecraft:oak"))
    m.set(2, 0, 1, GRASS); m.set(2, 1, 1, leaves("minecraft:azalea"))
    for y in (1, 2, 3):
        m.set(6, y, 6, fence("minecraft:spruce"))
    m.set(6, 4, 6, lantern(False))
    m.part(2, 7, 3, 9, "gardens")

    m.mark("node-cottages", 17, 4, "west")
    m.finish()
    return m


if __name__ == "__main__":
    raise SystemExit(run(build, reason="the roof slopes, the wall heads and the lofts: seen, never stood on"))
