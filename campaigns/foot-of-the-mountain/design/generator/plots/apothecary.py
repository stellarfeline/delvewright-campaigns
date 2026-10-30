#!/usr/bin/env python3
"""node/apothecary: the apothecary's, on stretch 1's east side, across from the bakery.

    python3 apothecary.py --allocation <delvec allocation ... node/apothecary> --out ../../../programs/apothecary.json

Form, after the apothecary's trade (remedies of herbs, minerals and animal
matter dispensed over a counter, weighed small; the shop with its jars and the
still room where they are made) and the medieval physic garden (the hortus
medicus, the garden's own section for medicinal plants): a narrow tall house
end-on to the street, the shop in front with jars on shelves and a counter, the
still room behind it through a door, its cauldron over a fire and herbs drying
from the beams; behind, the physic garden in raised beds with a gravel path
between them, an arbour seat at its far end, a hedge round it.

Piece-local axes: +x east, +z south; the street's opening is the play space's
first column (x 1), kept clear with the verge beside it (x 2).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plotlib import (Model, Plot, bed_of, candle, door2, fence, front, guard_seams, lantern, leaves, log,  # noqa: E402
                     pane, plot_main, ring, slab, stairs, trapdoor, wall_torch, window)

GRASS = "minecraft:grass_block[snowy=false]"
PALETTE = {"floor": GRASS, "wall": "minecraft:stone_bricks", "lid": "minecraft:spruce_planks",
           "lamp": "minecraft:lantern[hanging=false,waterlogged=false]", "turf": GRASS}
VARIANTS = {
    "stone": [{"weight": 12, "block": "minecraft:stone_bricks"},
              {"weight": 2, "block": "minecraft:cracked_stone_bricks"},
              {"weight": 1, "block": "minecraft:mossy_stone_bricks"}],
}
ROOF = "minecraft:deepslate_tile"
DRESS = "minecraft:tuff_bricks"
POST = log("minecraft:dark_oak_log", "y")
BEAM_X = log("minecraft:dark_oak_log", "x")
BEAM_Z = log("minecraft:dark_oak_log", "z")
PLASTER = "minecraft:mud_bricks"                  # an older, browner front: the apothecary's
PLINTH = "minecraft:polished_andesite"
GLASS = pane("minecraft:green_stained_glass_pane")   # bottle glass
CLEAR = pane("minecraft:glass_pane")
BOARDS = "minecraft:dark_oak_planks"

# the house: walls x 4..11, z 3..10, end-on to the street (gable west);
# ground y 1..4, floor y 5, upper storey y 6..8, roof from y 9
HX0, HX1, HZ0, HZ1 = 4, 11, 3, 10
FRONT_DX = -3              # the house's front wall on the lot's street edge (x 1)
STILL_WALL = 8


def build(a):
    m = Model(a["extent"])
    guard_seams(m, a)
    # the lot fronts the street: drawn as it stood, brought three cells west,
    # the house's front wall on the lot's edge, its doorway the lot's
    m.dx = FRONT_DX
    m.part(HX0, HX1, HZ0, HZ1, "house")
    m.part(12, 18, 2, 10, "garden")

    # ---- ground: a flagged step before the door, the garden's gravel paths

    # ---- the house: stone ground storey with tuff quoins, timber upper storey
    corners = {(HX0, HZ0), (HX1, HZ0), (HX0, HZ1), (HX1, HZ1)}
    for (x, z) in ring(HX0, HX1, HZ0, HZ1):
        m.set(x, 1, z, PLINTH)
        for y in (2, 3, 4):
            m.set(x, y, z, DRESS if (x, z) in corners else "stone")
    for (x, z) in ring(HX0, HX1, HZ0, HZ1):
        m.set(x, 5, z, BEAM_X if z in (HZ0, HZ1) else BEAM_Z)
    for y in (6, 7, 8):
        for (x, z) in ring(HX0, HX1, HZ0, HZ1):
            post = (x, z) in corners or (z in (HZ0, HZ1) and x in (6, 9)) or (x in (HX0, HX1) and z in (5, 8))
            m.set(x, y, z, POST if post else PLASTER)
    for (x, z) in ring(HX0, HX1, HZ0, HZ1):
        m.set(x, 9, z, BEAM_X if z in (HZ0, HZ1) else BEAM_Z)
    m.box(HX0 + 1, HX1 - 1, 5, 5, HZ0 + 1, HZ1 - 1, BOARDS)
    top = m.gable_roof(HX0, HX1, HZ0, HZ1, 9, "x", ROOF, fill=PLASTER)
    for y in range(9, top):
        m.set(HX0, y, 6, POST); m.set(HX0, y, 7, POST)
    m.set(HX0, 11, 6, GLASS); m.set(HX0, 11, 7, GLASS)
    # the still room's chimney on the north wall
    for y in range(1, top + 2):
        m.set(10, y, HZ0, "stone")
    # the front: the door under a little hood, the jar window beside it
    door2(m, HX0, 8, "minecraft:dark_oak", "east")
    m.set(HX0, 3, 8, DRESS)
    for z in (5, 6):
        window(m, HX0, z, GLASS)
    # over the street, on the upper storey's sill: a window box in flower
    for z in (5, 6):
        m.set(HX0 - 1, 5, z, slab("minecraft:dark_oak", "top"))
        m.set(HX0 - 1, 6, z, leaves("minecraft:flowering_azalea"))
    for (x, z) in ((6, HZ0), (6, HZ1), (9, HZ1)):
        window(m, x, z, GLASS)
    for (x, z) in ((5, HZ0), (7, HZ0), (5, HZ1), (7, HZ1), (10, HZ1), (HX0, 4), (HX0, 9), (HX1, 6), (HX1, 7)):
        m.set(x, 7, z, CLEAR)
    m.set(HX1, 2, 7, CLEAR); m.set(HX1, 3, 7, CLEAR)          # the still room over the garden
    door2(m, HX1, 9, "minecraft:dark_oak", "west")             # out to the garden
    m.set(HX1, 3, 9, "stone")

    # ---- inside: the shop and, through a door, the still room
    m.box(HX0 + 1, HX1 - 1, 0, 0, HZ0 + 1, HZ1 - 1, BOARDS)
    for z in range(HZ0 + 1, HZ1):
        for y in range(1, 5):
            m.set(STILL_WALL, y, z, "stone" if y < 4 else BEAM_Z)
    door2(m, STILL_WALL, 8, "minecraft:dark_oak", "east")
    m.set(STILL_WALL, 3, 8, "stone")
    # the shop: shelves of jars on the north wall, the counter, the scales
    for x in (5, 6, 7):
        m.set(x, 1, 4, "minecraft:bookshelf")
        m.set(x, 2, 4, slab("minecraft:dark_oak", "top"))
    m.set(5, 3, 4, "minecraft:flower_pot"); m.set(6, 3, 4, "minecraft:potted_fern"); m.set(7, 3, 4, "minecraft:flower_pot")
    for z in (6, 7):
        m.set(6, 1, z, stairs("minecraft:dark_oak", "west", "top"))
    m.set(6, 2, 6, candle(2)); m.set(6, 2, 7, "minecraft:potted_lily_of_the_valley")
    m.set(6, 1, 9, slab("minecraft:dark_oak", "top")); m.set(7, 1, 9, slab("minecraft:dark_oak", "top"))
    m.set(7, 2, 9, candle(3, "green"))
    m.set(6, 4, 7, lantern(True))
    # the still room: the cauldron over its fire at the chimney, the work
    # table, herbs drying (leaves hung from the beam), a lectern with the herbal
    m.set(10, 1, 4, "minecraft:campfire[facing=south,lit=true,signal_fire=false,waterlogged=false]")
    m.set(10, 2, 4, "minecraft:water_cauldron[level=3]")
    m.set(10, 1, 5, "minecraft:barrel[facing=up,open=false]")
    m.set(9, 1, 9, "minecraft:lectern[facing=north,has_book=false,powered=false]")
    m.set(9, 1, 4, "minecraft:crafting_table")
    m.set(10, 1, 7, "minecraft:cauldron")
    for (x, z) in ((9, 6), (10, 6), (9, 7)):
        m.set(x, 4, z, leaves("minecraft:azalea"))
    m.set(10, 4, 8, lantern(True))

    # ---- the physic garden: raised beds of herbs along gravel paths, a hedge
    # round it, an arbour seat at its far end
    m.box(12, 18, 0, 0, 2, 10, "minecraft:gravel")
    herbs = ["minecraft:allium", "minecraft:azure_bluet", "minecraft:lily_of_the_valley", "minecraft:fern",
             "minecraft:cornflower", "minecraft:oxeye_daisy", "minecraft:blue_orchid", "minecraft:white_tulip"]
    i = 0
    for (bx0, bz0) in ((13, 3), (16, 3), (13, 7), (16, 7)):
        for x in range(bx0, bx0 + 2):
            for z in range(bz0, bz0 + 2):
                m.set(x, 0, z, "minecraft:podzol[snowy=false]")
                m.set(x, 1, z, herbs[i % len(herbs)])
                i += 1
    for z in range(2, 11):
        m.set(18, 0, z, GRASS); m.set(18, 1, z, leaves("minecraft:oak"))
    for x in range(12, 18):
        m.set(x, 0, 11, GRASS); m.set(x, 1, 11, leaves("minecraft:oak"))
    m.set(15, 1, 10, stairs("minecraft:spruce", "north"))   # the arbour seat
    for (x, z) in ((14, 10), (16, 10)):
        for y in (1, 2, 3):
            m.set(x, y, z, fence("minecraft:spruce"))
    for x in (14, 15, 16):
        m.set(x, 4, 10, leaves("minecraft:flowering_azalea"))
    m.set(12, 1, 2, "minecraft:sweet_berry_bush[age=3]")
    m.set(12, 0, 2, GRASS)
    m.set(15, 1, 5, "minecraft:water_cauldron[level=3]")     # the watering trough

    # the street face: a bench, a bush

    m.marks["node-apothecary"] = (6 + FRONT_DX, 8, "east")
    # the street edge where the house does not stand: the yard wall
    front(m, 1, 1, a["extent"][2] - 2, gap=set(range(7, 10)))
    return m


class Apothecary(Plot):
    VARIANTS = VARIANTS


if __name__ == "__main__":
    raise SystemExit(plot_main(build, Apothecary, PALETTE,
                               "the roof slopes, the wall heads, the hedge tops and the sealed upper storey: seen, never stood on"))
