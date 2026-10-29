#!/usr/bin/env python3
"""node/bakery: the baker's, on stretch 1's west side.

    python3 bakery.py --allocation <delvec allocation ... node/bakery> --out ../../../programs/bakery.json

Form, after the town bakery as builders make it (a shop front below with the
baker's rooms over it and the ovens out back) and the masonry oven (a brick
dome on a raised hearth, fired inside, under a roof against the weather): a
gable-fronted house to the street, its shop behind a striped awning and a
display window, the bake room behind it through a door with the kneading
table, flour and the water; in the yard behind, the domed bread oven under a
lean-to, its woodpile beside it.

Piece-local axes: +x east (the street), +z south; the street's opening is the
play space's last column (x 22), kept clear with the verge beside it (x 21).
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
             {"weight": 2, "block": "minecraft:dirt_path"}],
    "dome": [{"weight": 5, "block": "minecraft:bricks"},
             {"weight": 2, "block": "minecraft:mud_bricks"}],
}
ROOF = "minecraft:deepslate_tile"
POST = log("minecraft:stripped_oak_log", "y")
BEAM_X = log("minecraft:stripped_oak_log", "x")
BEAM_Z = log("minecraft:stripped_oak_log", "z")
PLASTER = "minecraft:smooth_sandstone"            # a warm limewash, the baker's
PLINTH = "minecraft:polished_andesite"
GLASS = pane("minecraft:glass_pane")
BOARDS = "minecraft:oak_planks"

# the house: walls x 9..19, z 3..9; gable to the street (east); ground floor
# y 1..4, the floor over it y 5, the upper storey y 6..8, roof from y 8
HX0, HX1, HZ0, HZ1 = 9, 19, 3, 9
SHOP_WALL = 14             # the wall between the bake room (west) and the shop


def build(a):
    m = Model(a["extent"])
    guard_seams(m, a)
    m.part(HX0, HX1, HZ0, HZ1, "shop")
    m.part(3, 7, 3, 5, "oven")
    for x in range(2, 9):
        for z in range(7, 13):
            m.region[(x, z)] = "yard"
    m.part(9, 20, 11, 12, "yard")

    m.box(2, 20, 0, 0, 1, 12, "yard")
    m.box(HX1 + 1, 20, 0, 0, HZ0, HZ1, "minecraft:stone_bricks")   # the step before the shop

    # ---- the house: stone plinth, timber frame, limewash, the upper storey
    corners = {(HX0, HZ0), (HX1, HZ0), (HX0, HZ1), (HX1, HZ1)}
    for (x, z) in ring(HX0, HX1, HZ0, HZ1):
        m.set(x, 1, z, PLINTH)
        for y in (2, 3, 4):
            post = (x, z) in corners or (z in (HZ0, HZ1) and x in (12, SHOP_WALL, 17)) or (x in (HX0, HX1) and z == 6)
            m.set(x, y, z, POST if post else PLASTER)
        m.set(x, 5, z, BEAM_X if z in (HZ0, HZ1) else BEAM_Z)
        for y in (6, 7):
            post = (x, z) in corners or (z in (HZ0, HZ1) and x % 3 == 0) or (x in (HX0, HX1) and z == 6)
            m.set(x, y, z, POST if post else PLASTER)
    m.box(HX0 + 1, HX1 - 1, 5, 5, HZ0 + 1, HZ1 - 1, BOARDS)
    top = m.gable_roof(HX0, HX1, HZ0, HZ1, 8, "x", ROOF, fill=PLASTER)
    for y in range(8, top):
        m.set(HX1, y, 6, POST)                          # the front gable's king post
    m.set(HX1, 9, 5, GLASS); m.set(HX1, 9, 7, GLASS)
    # the oven's flue rising past the yard gable
    for y in range(1, top + 2):
        m.set(HX0, y, 4, "stone")

    # the shop front: a door, a broad display window under a striped awning
    door2(m, HX1, 7, "minecraft:oak", "west")
    m.set(HX1, 3, 7, PLASTER)
    for z in (4, 5):
        for y in (2, 3):
            m.set(HX1, y, z, GLASS)
    for z in range(HZ0, HZ1 + 1):                     # the awning: slabs carrying red and white
        m.set(HX1 + 1, 4, z, slab("minecraft:spruce", "top"))
        m.set(HX1 + 1, 5, z, "minecraft:red_carpet" if z % 2 else "minecraft:white_carpet")
    m.set(HX1 + 1, 1, 4, "minecraft:hay_block[axis=z]")  # sheaves by the door
    m.set(HX1 + 1, 1, 5, slab("minecraft:spruce", "top"))
    m.set(HX1 + 1, 2, 5, "minecraft:potted_dandelion")
    m.set(HX1 + 1, 1, 8, stairs("minecraft:oak", "west"))  # a bench by the door
    m.set(HX1 + 1, 1, 9, stairs("minecraft:oak", "west"))
    # side and back lights
    for x in (11, 16):
        window(m, x, HZ0, GLASS); window(m, x, HZ1, GLASS)
        m.set(x, 6, HZ0, GLASS); m.set(x, 6, HZ1, GLASS)
    window(m, HX0, 7, GLASS)

    # ---- inside: the shop (east) and the bake room (west), a door between
    m.box(HX0 + 1, HX1 - 1, 0, 0, HZ0 + 1, HZ1 - 1, BOARDS)
    for z in range(HZ0 + 1, HZ1):
        for y in range(1, 5):
            m.set(SHOP_WALL, y, z, PLASTER if y < 4 else BEAM_Z)
    door2(m, SHOP_WALL, 6, "minecraft:oak", "east")
    m.set(SHOP_WALL, 3, 6, PLASTER)
    # the shop: a counter across, loaves on boards behind the window
    for z in (4, 5):
        m.set(16, 1, z, stairs("minecraft:spruce", "east", "top"))
    m.set(16, 1, 6, trapdoor("minecraft:spruce", "east"))
    m.set(15, 1, 4, "minecraft:hay_block[axis=x]")
    m.set(15, 1, 8, slab("minecraft:oak", "top")); m.set(16, 1, 8, slab("minecraft:oak", "top"))
    m.set(16, 2, 4, candle(2))
    m.set(18, 1, 4, slab("minecraft:oak", "top")); m.set(18, 1, 5, slab("minecraft:oak", "top"))
    m.set(18, 2, 5, "minecraft:potted_poppy")
    m.set(17, 4, 6, lantern(True))
    # the bake room: the kneading table, sacks of flour, water, the peel rack
    m.box(HX0 + 1, SHOP_WALL - 1, 0, 0, HZ0 + 1, HZ1 - 1, "minecraft:packed_mud")
    m.set(11, 1, 6, "minecraft:crafting_table"); m.set(12, 1, 6, slab("minecraft:oak", "top"))
    for (x, z) in ((10, 8), (11, 8), (10, 7)):
        m.set(x, 1, z, "minecraft:white_wool")
    m.set(10, 2, 8, "minecraft:white_wool")
    m.set(13, 1, 4, "minecraft:water_cauldron[level=3]")
    m.set(10, 1, 4, "minecraft:barrel[facing=up,open=false]")          # the meal barrel
    m.set(12, 4, 6, lantern(True))

    # ---- the oven house: a brick dome on a hearth under a tiled lean-to
    for x in range(3, 8):
        for z in range(3, 6):
            m.set(x, 1, z, "stone")
    for x in range(4, 7):
        m.set(x, 2, 3, "dome"); m.set(x, 2, 4, "dome"); m.set(x, 2, 5, "dome")
        m.set(x, 3, 4, "dome")
    m.set(3, 2, 4, "dome"); m.set(7, 2, 4, "dome")
    m.set(5, 2, 5, "minecraft:campfire[facing=south,lit=true,signal_fire=false,waterlogged=false]")   # its mouth
    m.set(5, 3, 5, stairs("minecraft:brick", "north"))
    for x in range(2, 9):                                 # the lean-to over it
        m.set(x, 5, 2, stairs(ROOF, "south"))
        m.set(x, 4, 6, stairs(ROOF, "north"))
        for z in (3, 4, 5):
            m.set(x, 5, z, slab(ROOF, "top"))
    for (x, z) in ((2, 6), (8, 6), (2, 2), (8, 2)):
        for y in range(1, 4):
            m.set(x, y, z, log("minecraft:spruce_log", "y"))
        m.set(x, 4, z, log("minecraft:spruce_log", "y"))
    for x in range(2, 9):
        m.set(x, 4, 2, BEAM_X)
    # the woodpile and faggots beside it, the peel against the post
    m.box(2, 2, 1, 2, 7, 9, log("minecraft:oak_log", "z"))
    m.set(3, 1, 9, log("minecraft:birch_log", "z"))
    m.set(8, 1, 7, "minecraft:barrel[facing=up,open=false]")
    # the yard: a bench, a flower bed, bushes, a lantern post
    m.set(5, 1, 11, stairs("minecraft:spruce", "north")); m.set(6, 1, 11, stairs("minecraft:spruce", "north"))
    bed_of(m, [(10, 11), (11, 11), (12, 11), (16, 11), (17, 11)],
           ["minecraft:poppy", "minecraft:dandelion", "minecraft:cornflower"])
    for (x, z) in ((3, 12), (8, 12), (14, 12), (19, 12)):
        m.set(x, 0, z, GRASS); m.set(x, 1, z, leaves("minecraft:azalea" if x % 2 else "minecraft:oak"))
    for y in (1, 2, 3):
        m.set(20, y, 11, fence("minecraft:spruce"))
    m.set(20, 4, 11, lantern(False))

    m.marks["node-bakery"] = (20, 6, "west")
    return m


class Bakery(Plot):
    VARIANTS = VARIANTS


if __name__ == "__main__":
    raise SystemExit(plot_main(build, Bakery, PALETTE,
                               "the roof slopes, the wall heads, the oven's lean-to and the sealed upper storey: seen, never stood on"))
