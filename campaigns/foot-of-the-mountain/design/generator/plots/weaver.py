#!/usr/bin/env python3
"""node/weaver: the weaver's house, on stretch 3's east side.

    python3 weaver.py --allocation <delvec allocation ... node/weaver> --out ../../../programs/weaver.json

Form, after the weavers' cottage (a tall house, the loomshop lit by a long row
of many-light windows along one wall, storage beside it): a tall timber house
end-on to the street, the cloth shop in front where bolts are shown and sold,
the loom room behind it through a door, its looms under a long window wall
that looks over the drying yard; beside the yard an open dye shed of vats
under a lean-to; in the yard, posts and beams hung with dyed cloth drying.

Piece-local axes: +x east, +z south; the street's opening is the play space's
first column (x 1), kept clear with the verge beside it (x 2).
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
    "yard": [{"weight": 6, "block": "minecraft:grass_block[snowy=false]"},
             {"weight": 2, "block": "minecraft:coarse_dirt"},
             {"weight": 1, "block": "minecraft:dirt_path"}],
}
ROOF = "minecraft:deepslate_tile"
POST = log("minecraft:spruce_log", "y")
BEAM_X = log("minecraft:spruce_log", "x")
BEAM_Z = log("minecraft:spruce_log", "z")
PLASTER = "minecraft:calcite"
PLINTH = "minecraft:polished_andesite"
GLASS = pane("minecraft:glass_pane")
BOARDS = "minecraft:spruce_planks"

# the house: walls x 4..12, z 2..10, end-on to the street; ground y 1..4,
# floor y 5, the upper storey y 6..8 jettied one cell over the yard (south)
HX0, HX1, HZ0, HZ1 = 4, 12, 2, 10
LOOM_WALL = 7


def build(a):
    m = Model(a["extent"])
    guard_seams(m, a)
    m.part(HX0, HX1, HZ0, HZ1, "house")
    m.part(15, 21, 2, 4, "dye-shed")
    m.part(14, 21, 6, 12, "drying-yard")

    m.box(13, 21, 0, 0, 1, 12, "yard")
    m.box(3, 3, 0, 0, HZ0, HZ1, "minecraft:stone_bricks")

    # ---- the house: a stone plinth, a spruce frame, the upper storey jettied
    corners = {(HX0, HZ0), (HX1, HZ0), (HX0, HZ1), (HX1, HZ1)}
    for (x, z) in ring(HX0, HX1, HZ0, HZ1):
        m.set(x, 1, z, PLINTH)
        for y in (2, 3, 4):
            post = (x, z) in corners or (z in (HZ0, HZ1) and x in (LOOM_WALL, 10)) or (x in (HX0, HX1) and z in (6,))
            m.set(x, y, z, POST if post else PLASTER)
    uz1 = HZ1 + 1
    for (x, z) in ring(HX0, HX1, HZ0, uz1):
        m.set(x, 5, z, BEAM_X if z in (HZ0, uz1) else BEAM_Z)
        for y in (6, 7, 8):
            post = (x, z) in {(HX0, HZ0), (HX1, HZ0), (HX0, uz1), (HX1, uz1)} or (z in (HZ0, uz1) and x in (LOOM_WALL, 10)) or (x in (HX0, HX1) and z == 6)
            m.set(x, y, z, POST if post else PLASTER)
    for x in range(HX0, HX1 + 1):
        m.set(x, 5, uz1, stairs("minecraft:spruce", "south", "top") if HX0 < x < HX1 else BEAM_Z)
    m.box(HX0 + 1, HX1 - 1, 5, 5, HZ0 + 1, uz1 - 1, BOARDS)
    top = m.gable_roof(HX0, HX1, HZ0, uz1, 9, "x", ROOF, fill=PLASTER)
    # no rake over the street gable: the roof's edge stands back with the
    # wall, three cells off the street's opening
    m.clear(HX0 - 1, HX0 - 1, 9, 16, 0, 13)
    for y in range(9, top):
        m.set(HX0, y, 6, POST)
    m.set(HX0, 11, 5, GLASS); m.set(HX0, 11, 7, GLASS)
    # the loomshop's long window wall over the yard: every cell between posts
    for x in range(LOOM_WALL + 1, HX1):
        if x != 10:
            window(m, x, HZ1, GLASS)
        m.set(x, 7, uz1, GLASS)
    for x in (5, 6):
        window(m, x, HZ0, GLASS); m.set(x, 7, HZ0, GLASS)
        m.set(x, 7, uz1, GLASS)
    for z in (4, 8):
        window(m, HX0, z, GLASS); m.set(HX0, 7, z, GLASS)
    for z in (4, 8):
        m.set(HX1, 7, z, GLASS)
    # the shop door to the street, a bolt of cloth shown on the sill
    door2(m, HX0, 6, "minecraft:spruce", "east")
    m.set(HX0, 3, 6, PLASTER)
    m.set(HX0 - 1, 1, 4, slab("minecraft:spruce", "top")); m.set(HX0 - 1, 2, 4, "minecraft:red_wool")
    m.set(HX0 - 1, 1, 8, slab("minecraft:spruce", "top")); m.set(HX0 - 1, 2, 8, "minecraft:blue_wool")
    m.set(HX0 - 1, 3, 6, wall_torch("west"))
    # the chimney on the north wall
    for y in range(1, top + 2):
        m.set(10, y, HZ0, "stone")

    # ---- inside: the shop (west) and the loom room (east), a door between
    m.box(HX0 + 1, HX1 - 1, 0, 0, HZ0 + 1, HZ1 - 1, BOARDS)
    for z in range(HZ0 + 1, HZ1):
        for y in range(1, 5):
            m.set(LOOM_WALL, y, z, PLASTER if y < 4 else BEAM_Z)
    door2(m, LOOM_WALL, 6, "minecraft:spruce", "east")
    m.set(LOOM_WALL, 3, 6, PLASTER)
    # the shop: bolts of cloth racked by colour, the cutting table, a stool
    for i, col in enumerate(("red", "yellow", "blue", "light_gray")):
        m.set(5 + i % 2, 1 + i // 2, 3, f"minecraft:{col}_wool")
    m.set(5, 1, 9, slab("minecraft:spruce", "top")); m.set(6, 1, 9, slab("minecraft:spruce", "top"))
    m.set(5, 2, 9, "minecraft:white_carpet"); m.set(6, 2, 9, candle(2))
    m.set(6, 1, 7, stairs("minecraft:spruce", "north"))
    m.set(5, 4, 6, lantern(True))
    # the loom room: three looms facing the window wall, the wool bale, a wheel
    for x in (8, 9, 11):
        m.set(x, 1, 9, "minecraft:loom[facing=north]")
    m.set(8, 1, 3, "minecraft:white_wool"); m.set(9, 1, 3, "minecraft:white_wool"); m.set(8, 2, 3, "minecraft:white_wool")
    m.set(11, 1, 3, "minecraft:grindstone[face=floor,facing=west]")    # the spinning wheel
    m.set(11, 1, 5, "minecraft:barrel[facing=up,open=false]")
    m.set(9, 4, 6, lantern(True))
    # a door from the loom room to the yard
    door2(m, HX1, 8, "minecraft:spruce", "west")
    m.set(HX1, 3, 8, PLASTER)

    # ---- the dye shed: posts, a back wall to the hill, a lean-to, the vats
    for x in range(15, 22):
        for y in range(1, 5):
            m.set(x, y, 2, "stone" if y < 4 else BEAM_X)
    for (x, z) in ((15, 4), (18, 4), (21, 4), (21, 3)):
        for y in range(1, 4):
            m.set(x, y, z, POST)
    for x in range(14, 23):
        if x == 22:
            continue
        m.set(x, 4, 4, BEAM_X if x not in (15, 18, 21) else POST)
        m.set(x, 5, 5, stairs(ROOF, "north"))
        m.set(x, 5, 4, slab(ROOF, "top")); m.set(x, 5, 3, slab(ROOF, "top"))
        m.set(x, 5, 2, slab(ROOF, "top"))
    for x, col in ((16, "blue"), (17, "red"), (19, "yellow")):
        m.set(x, 1, 3, "minecraft:water_cauldron[level=3]")
    m.set(20, 1, 3, "minecraft:barrel[facing=up,open=false]")
    m.set(17, 5, 3, "stone"); m.set(17, 4, 3, lantern(True))          # a lantern on the ridge beam

    # ---- the drying yard: posts and beams, dyed cloth hung on both faces
    for (x, z) in ((14, 7), (21, 7), (14, 10), (21, 10)):
        for y in (1, 2, 3):
            m.set(x, y, z, POST)
    for z in (7, 10):
        for x in range(15, 21):
            m.set(x, 3, z, BEAM_X)
    colours = ("red", "blue", "yellow", "white", "light_blue", "orange")
    for i, x in enumerate(range(15, 21)):
        m.set(x, 3, 8, f"minecraft:{colours[i % 6]}_wall_banner[facing=south]")
        m.set(x, 3, 9, f"minecraft:{colours[(i + 3) % 6]}_wall_banner[facing=north]")
    # a bench under the window wall, flower beds, a bush, a lantern post
    bed_of(m, [(5, 12), (6, 12), (8, 12), (9, 12), (11, 12)],
           ["minecraft:cornflower", "minecraft:poppy", "minecraft:oxeye_daisy", "minecraft:allium"])
    m.set(13, 0, 12, GRASS); m.set(13, 1, 12, leaves("minecraft:azalea"))
    m.set(3, 0, 12, GRASS); m.set(3, 1, 12, leaves("minecraft:oak"))
    for y in (1, 2, 3):
        m.set(13, y, 5, fence("minecraft:spruce"))
    m.set(13, 4, 5, lantern(False))

    m.marks["node-weaver"] = (3, 6, "east")
    return m


class Weaver(Plot):
    VARIANTS = VARIANTS


if __name__ == "__main__":
    raise SystemExit(plot_main(build, Weaver, PALETTE,
                               "the roof slopes, the wall heads, the dye shed's roof and the sealed upper storey: seen, never stood on"))
