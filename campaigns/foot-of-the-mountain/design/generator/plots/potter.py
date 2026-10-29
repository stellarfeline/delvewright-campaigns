#!/usr/bin/env python3
"""node/potter: the potter's, on the south side of lane 3.

    python3 potter.py --allocation <delvec allocation ... node/potter> --out ../../../programs/potter.json

Form, after the medieval pottery workshop and its kiln (a thick-walled kiln
of brick or stone with its stoke-hole, the workshop beside it; wasters and
ware about the yard) and the masonry oven's fired brick: a low stone and
timber workshop to the lane, the shop in front where pots stand on the sill
and the shelves, the throwing room behind it through a door with the wheel,
the clay bin and the water; in the yard a brick bottle kiln with its stoke
hole under a lean-to, its wood beside it, the clay heap, and green ware drying
on boards.

Piece-local axes: +x east, +z south; the lane's opening is the play space's
first row (z 1), kept clear with the verge beside it (z 2).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plotlib import (Model, Plot, bed_of, candle, door2, fence, guard_seams, lantern, leaves, log,  # noqa: E402
                     pane, plot_main, ring, slab, stairs, trapdoor, wall_torch, window)

GRASS = "minecraft:grass_block[snowy=false]"
PALETTE = {"floor": GRASS, "wall": "minecraft:stone_bricks", "lid": "minecraft:spruce_planks",
           "lamp": "minecraft:lantern[hanging=false,waterlogged=false]", "turf": GRASS}
VARIANTS = {
    "stone": [{"weight": 12, "block": "minecraft:stone_bricks"},
              {"weight": 2, "block": "minecraft:cracked_stone_bricks"},
              {"weight": 1, "block": "minecraft:mossy_stone_bricks"}],
    "yard": [{"weight": 5, "block": "minecraft:coarse_dirt"},
             {"weight": 3, "block": "minecraft:packed_mud"},
             {"weight": 2, "block": "minecraft:gravel"}],
    "kiln": [{"weight": 6, "block": "minecraft:bricks"},
             {"weight": 2, "block": "minecraft:terracotta"}],
}
ROOF = "minecraft:deepslate_tile"
POST = log("minecraft:oak_log", "y")
BEAM_X = log("minecraft:oak_log", "x")
BEAM_Z = log("minecraft:oak_log", "z")
PLASTER = "minecraft:packed_mud"                  # clay daub: the potter's
PLINTH = "minecraft:polished_andesite"
GLASS = pane("minecraft:glass_pane")
BOARDS = "minecraft:oak_planks"

# the workshop: walls x 3..10, z 4..11, set back from the lane so its eave
# stays off the verge; one storey and a loft under the roof
HX0, HX1, HZ0, HZ1 = 3, 10, 4, 11
THROW_WALL = 8
# the kiln: x 12..14, z 6..8
KX0, KX1, KZ0, KZ1 = 12, 14, 6, 8


def build(a):
    m = Model(a["extent"])
    guard_seams(m, a)
    m.part(HX0, HX1, HZ0, HZ1, "workshop")
    m.part(KX0, KX1, KZ0, KZ1, "kiln")
    m.part(11, 16, 3, 5, "yard")
    m.part(15, 16, 6, 8, "yard")
    m.part(11, 16, 9, 11, "yard")

    m.box(11, 16, 0, 0, 3, 11, "yard")

    # ---- the workshop: stone ground course and quoins, clay daub in a frame
    corners = {(HX0, HZ0), (HX1, HZ0), (HX0, HZ1), (HX1, HZ1)}
    for (x, z) in ring(HX0, HX1, HZ0, HZ1):
        m.set(x, 1, z, PLINTH)
        for y in (2, 3, 4):
            post = (x, z) in corners or (z in (HZ0, HZ1) and x in (5, 8)) or (x in (HX0, HX1) and z == THROW_WALL)
            m.set(x, y, z, POST if post else PLASTER)
        m.set(x, 5, z, BEAM_X if z in (HZ0, HZ1) else BEAM_Z)
    m.box(HX0 + 1, HX1 - 1, 5, 5, HZ0 + 1, HZ1 - 1, BOARDS)
    top = m.gable_roof(HX0, HX1, HZ0, HZ1, 5, "z", ROOF, fill=PLASTER)
    for y in range(6, top):
        m.set(6, y, HZ0, POST)
    # the loft's door in the back gable, open, a hoist beam over it
    m.v[(6, 6, HZ1)] = "~air"; m.v[(6, 7, HZ1)] = "~air"
    m.set(6, 8, HZ1 + 1, log("minecraft:oak_log", "z"))
    # the shop front to the lane: the door, a window with pots on the sill
    door2(m, 7, HZ0, "minecraft:oak", "south")
    m.set(7, 3, HZ0, PLASTER)
    window(m, 4, HZ0, GLASS)
    m.set(9, 2, HZ0, GLASS); m.set(9, 3, HZ0, GLASS)
    window(m, HX0, 6, GLASS)
    window(m, HX0, 10, GLASS); window(m, HX1, 10, GLASS)
    # the throwing room's back door to the yard
    door2(m, HX1, 9, "minecraft:oak", "west")
    m.set(HX1, 3, 9, PLASTER)

    # ---- inside: the shop (north) and the throwing room (south)
    m.box(HX0 + 1, HX1 - 1, 0, 0, HZ0 + 1, THROW_WALL - 1, BOARDS)
    m.box(HX0 + 1, HX1 - 1, 0, 0, THROW_WALL + 1, HZ1 - 1, "minecraft:packed_mud")
    for x in range(HX0 + 1, HX1):
        for y in range(1, 5):
            m.set(x, y, THROW_WALL, PLASTER if y < 4 else BEAM_X)
    door2(m, 5, THROW_WALL, "minecraft:oak", "south")
    m.set(5, 3, THROW_WALL, PLASTER)
    # the shop: shelves of ware on the west wall, the counter, pots for sale
    for z in (5, 6, 7):
        m.set(4, 1, z, slab("minecraft:spruce", "top"))
        m.set(4, 2, z, "minecraft:flower_pot")
        m.set(4, 3, z, slab("minecraft:spruce", "top"))
    m.set(4, 4, 6, "minecraft:flower_pot")
    for x in (8, 9):
        m.set(x, 1, 6, stairs("minecraft:spruce", "north", "top"))
    m.set(9, 2, 6, "minecraft:flower_pot"); m.set(8, 2, 6, "minecraft:potted_red_tulip")
    m.set(9, 1, 5, "minecraft:terracotta"); m.set(9, 1, 7, "minecraft:orange_terracotta")
    m.set(7, 4, 6, lantern(True))
    # the throwing room: the wheel, the clay bin, water, wedging bench
    m.set(7, 1, 10, "minecraft:grindstone[face=floor,facing=north]")     # the wheel
    m.set(8, 1, 10, stairs("minecraft:oak", "west"))                     # the potter's seat
    m.set(4, 1, 9, "minecraft:clay"); m.set(4, 1, 10, "minecraft:clay"); m.set(4, 2, 10, "minecraft:clay")
    m.set(6, 1, 10, "minecraft:water_cauldron[level=3]")
    m.set(4, 4, 9, lantern(True))

    # ---- the kiln: a brick bottle on a square base, its stoke hole to the
    # west under a lean-to, the chimney necking up
    for (x, z) in ring(KX0, KX1, KZ0, KZ1):
        for y in range(1, 5):
            m.set(x, y, z, "kiln")
    m.box(KX0 + 1, KX0 + 1, 1, 4, KZ0 + 1, KZ0 + 1, "kiln")
    m.set(KX0 + 1, 1, KZ0 + 1, "minecraft:campfire[facing=west,lit=true,signal_fire=false,waterlogged=false]")
    m.v[(KX0, 1, KZ0 + 1)] = "~air"                    # the stoke hole
    m.set(KX0, 2, KZ0 + 1, stairs("minecraft:brick", "east", "top"))
    for (x, z) in ring(KX0, KX1, KZ0, KZ1):
        m.set(x, 5, z, slab("minecraft:brick"))          # the shoulder where the bottle necks in
    for y in range(5, 10):
        m.set(KX0 + 1, y, KZ0 + 1, "kiln")
    # the lean-to over the stoke side, its wood stacked under it
    for z in range(KZ0 - 2, KZ1 + 3):
        m.set(11, 4, z, BEAM_Z)
        m.set(11, 5, z, stairs(ROOF, "east"))
    for z in (KZ0 - 2, KZ1 + 2):
        for y in range(1, 4):
            m.set(11, y, z, POST)
        m.set(11, 4, z, POST)
    m.box(15, 16, 1, 1, 6, 8, log("minecraft:oak_log", "x"))
    m.set(15, 2, 7, log("minecraft:oak_log", "x"))

    # ---- the yard: the clay heap, green ware drying on boards, the wasters
    m.set(13, 1, 4, "minecraft:clay"); m.set(14, 1, 4, "minecraft:clay"); m.set(13, 1, 3, "minecraft:gravel")
    m.set(14, 2, 4, "minecraft:clay")
    for x in (12, 13, 14, 15):
        m.set(x, 1, 10, slab("minecraft:oak", "top"))
        m.set(x, 2, 10, "minecraft:flower_pot")
    m.set(16, 1, 11, "minecraft:barrel[facing=up,open=false]")
    m.set(12, 1, 11, "minecraft:white_terracotta"); m.set(13, 1, 11, "minecraft:light_gray_terracotta")
    m.set(11, 1, 11, "minecraft:water_cauldron[level=3]")
    # the lane front: a bench, a flower bed, bushes
    m.set(1, 1, 5, stairs("minecraft:oak", "east")); m.set(1, 1, 6, stairs("minecraft:oak", "east"))   # a bench by the lane
    bed_of(m, [(1, 8), (1, 9), (1, 10), (1, 11), (2, 11)],
           ["minecraft:poppy", "minecraft:dandelion", "minecraft:azure_bluet"])
    m.set(16, 0, 3, GRASS); m.set(16, 1, 3, leaves("minecraft:azalea"))

    m.marks["node-potter"] = (12, 3, "south")
    return m


class Potter(Plot):
    VARIANTS = VARIANTS


if __name__ == "__main__":
    raise SystemExit(plot_main(build, Potter, PALETTE,
                               "the roof slopes, the wall heads, the kiln's top and the loft: seen, never stood on"))
