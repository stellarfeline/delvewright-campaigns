#!/usr/bin/env python3
"""node/merchant: a rich cloth merchant's house round a front court, on stretch 2's east side.

    python3 merchant.py --allocation <delvec allocation ... node/merchant> --out ../../../programs/merchant.json

Form, after the merchant's town house (a counting room by the street, a store
behind it, the hall at the back, a passage along one side; Southampton's
Medieval Merchant's House) and the U-shaped courtyard manor (two wings round a
court): a U open to the street. The north wing holds
the counting room at the street end and the cloth store behind it, through a
door; the hall range closes the court's east side, two storeys of the town's
stone under deepslate tiles, the hall's great door on the court; the south side
is a hedge with flower beds and a bench. The court, five wide, is
paved, a fountain at its middle, and an arch spans its mouth on the street.

Piece-local axes: +x east, +z south; the street's opening is the play space's
first column (x 1), kept clear with the verge beside it (x 2).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plotlib import (Model, Plot, bed, candle, door, fence, lantern, leaves, log, pane, plot_main, slab,  # noqa: E402
                     stairs, trapdoor, wall, wall_torch)

GRASS = "minecraft:grass_block[snowy=false]"
PALETTE = {
    "floor": GRASS,
    "wall": "minecraft:stone_bricks",
    "lid": "minecraft:spruce_planks",
    "lamp": "minecraft:lantern[hanging=false,waterlogged=false]",
    "turf": GRASS,
}
VARIANTS = {
    "stone": [{"weight": 12, "block": "minecraft:stone_bricks"},
              {"weight": 2, "block": "minecraft:cracked_stone_bricks"},
              {"weight": 1, "block": "minecraft:mossy_stone_bricks"}],
    "pave": [{"weight": 5, "block": "minecraft:polished_andesite"},
             {"weight": 3, "block": "minecraft:stone_bricks"},
             {"weight": 1, "block": "minecraft:andesite"}],
}
DRESS = "minecraft:tuff_bricks"
QUOIN = "minecraft:chiseled_tuff_bricks"
PIER = "minecraft:polished_tuff"
PLINTH = "minecraft:polished_andesite"
ROOF = "minecraft:deepslate_tile"
FRAME = log("minecraft:dark_oak_log", "y")
BEAM_X = log("minecraft:stripped_dark_oak_log", "x")
BEAM_Z = log("minecraft:stripped_dark_oak_log", "z")
PLASTER = "minecraft:calcite"
GLASS = pane("minecraft:white_stained_glass_pane")
BOARDS = "minecraft:dark_oak_planks"

# the north wing: walls x 4..17, z 2..6; the hall range: x 18..25, z 2..11;
# the court: x 4..17, z 7..11, a hedge on its south edge (z 12)
NX0, NX1, NZ0, NZ1 = 4, 17, 2, 6
HX0, HX1, HZ0, HZ1 = 18, 25, 2, 11
WX0, WX1 = 4, 17
COUNT_WALL = 10            # the wall between the counting room (west) and the store


def window(m, x, z, y0=2, h=2):
    for y in range(y0, y0 + h):
        m.set(x, y, z, GLASS)


def build(a):
    m = Model(a["extent"])
    for s in a["seams"]:
        (x0, y0, z0), (x1, y1, z1) = s["cells"]
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                for z in range(z0, z1 + 1):
                    m.no_touch.add((x, y, z))

    m.part(NX0, NX1, NZ0, NZ1, "house")
    m.part(HX0, HX1, HZ0, HZ1, "house")
    m.part(WX0, WX1, 7, 11, "court")

    # ---- ground: the court paved, a stone kerb along the verge
    m.box(3, 17, 0, 0, 7, 9, "pave")
    m.box(NX0, HX1, 0, 0, 1, 12, "pave")

    # ---- the north wing: stone ground floor, timber-framed upper storey
    def ring(x0, x1, z0, z1):
        return [(x, z) for x in range(x0, x1 + 1) for z in (z0, z1)] + \
               [(x, z) for z in range(z0 + 1, z1) for x in (x0, x1)]

    wing = ring(NX0, NX1, NZ0, NZ1)
    corners = {(NX0, NZ0), (NX1, NZ0), (NX0, NZ1), (NX1, NZ1)}
    for (x, z) in wing:
        m.set(x, 1, z, PLINTH)
        for y in (2, 3, 4):
            m.set(x, y, z, QUOIN if (x, z) in corners and y == 4 else (DRESS if (x, z) in corners else "stone"))
        m.set(x, 5, z, BEAM_X if z in (NZ0, NZ1) else BEAM_Z)
        for y in (6, 7):
            post = (x, z) in corners or (z in (NZ0, NZ1) and x % 3 == 1) or (x in (NX0, NX1) and z == 4)
            m.set(x, y, z, FRAME if post else PLASTER)
    m.box(NX0 + 1, NX1 - 1, 5, 5, NZ0 + 1, NZ1 - 1, BOARDS)
    m.gable_roof(NX0, NX1, NZ0, NZ1, 7, "x", ROOF, fill=PLASTER)
    # the counting room | store wall, with its door
    for z in range(NZ0 + 1, NZ1):
        for y in range(1, 5):
            m.set(COUNT_WALL, y, z, "stone")
    m.set(COUNT_WALL, 1, 4, door("minecraft:dark_oak", "east", "lower"))
    m.set(COUNT_WALL, 2, 4, door("minecraft:dark_oak", "east", "upper"))
    # the counting room's door on the court, its windows on the street and court
    m.set(7, 1, NZ1, door("minecraft:dark_oak", "north", "lower"))
    m.set(7, 2, NZ1, door("minecraft:dark_oak", "north", "upper"))
    m.set(7, 3, NZ1, DRESS)
    m.set(6, 4, NZ1 + 1, wall_torch("south"))
    window(m, NX0, 3); window(m, NX0, 5)                 # onto the street
    window(m, 9, NZ1)                                    # onto the court
    window(m, 13, NZ1); window(m, 15, NZ1)               # the store, onto the court
    for x in (7, 13):
        window(m, x, NZ0)                                # north lights, to the hill
    for x in (6, 9, 12, 15):
        m.set(x, 6, NZ0, GLASS); m.set(x, 6, NZ1, GLASS)
    m.set(NX0, 6, 4, GLASS)
    # sills: tuff slabs under the ground-floor windows outside
    for (x, z) in ((9, NZ1 + 1), (13, NZ1 + 1), (15, NZ1 + 1)):
        m.set(x, 1, z, slab("minecraft:tuff_brick"))
    # the counting room: a desk, the ledger, the scales, money on the table
    m.box(5, 9, 0, 0, 3, 5, BOARDS)
    m.set(5, 1, 3, "minecraft:lectern[facing=east,has_book=false,powered=false]")
    m.set(8, 1, 3, slab("minecraft:dark_oak", "top"))
    m.set(9, 1, 3, slab("minecraft:dark_oak", "top"))
    m.set(8, 2, 3, candle(3))
    m.set(9, 2, 3, "minecraft:potted_white_tulip")
    m.set(8, 1, 4, stairs("minecraft:dark_oak", "north"))           # the clerk's chair, clear of the door
    m.set(5, 1, 5, "minecraft:cartography_table")
    m.set(6, 1, 3, "minecraft:bookshelf")
    m.set(7, 4, 4, lantern(True))
    m.set(5, 1, 4, "minecraft:blue_carpet")
    m.set(6, 1, 4, "minecraft:blue_carpet")
    # the cloth store: bolts of cloth on racks (wool), crates
    m.box(11, 16, 0, 0, 3, 5, "minecraft:spruce_planks")
    for x in (11, 12, 13):
        m.set(x, 1, 3, "minecraft:red_wool"); m.set(x, 2, 3, "minecraft:blue_wool")
    for x in (14, 15, 16):
        m.set(x, 1, 3, "minecraft:light_gray_wool"); m.set(x, 2, 3, "minecraft:brown_wool")
    for x in (11, 12, 13, 14, 15, 16):
        m.set(x, 3, 3, slab("minecraft:spruce", "bottom"))
    m.set(16, 1, 5, "minecraft:loom[facing=west]")
    m.set(15, 1, 5, "minecraft:spruce_planks")                     # a packing crate
    m.set(15, 2, 5, trapdoor("minecraft:spruce", "north"))
    m.set(14, 4, 4, lantern(True))

    # ---- the hall range: two storeys of stone, the hall's door on the court
    hall = ring(HX0, HX1, HZ0, HZ1)
    hc = {(HX0, HZ0), (HX1, HZ0), (HX0, HZ1), (HX1, HZ1)}
    for (x, z) in hall:
        m.set(x, 1, z, PLINTH)
        for y in range(2, 10):
            if (x, z) in hc:
                m.set(x, y, z, QUOIN if y % 2 == 0 else DRESS)
            else:
                m.set(x, y, z, DRESS if y == 6 else "stone")
    m.box(HX0 + 1, HX1 - 1, 6, 6, HZ0 + 1, HZ1 - 1, BOARDS)
    top = m.gable_roof(HX0, HX1, HZ0, HZ1, 9, "z", ROOF, fill="stone")
    # the great door, double, under a tuff head, steps up from the court
    for z in (7, 8):
        m.set(HX0, 1, z, door("minecraft:dark_oak", "west", "lower", "left" if z == 7 else "right"))
        m.set(HX0, 2, z, door("minecraft:dark_oak", "west", "upper", "left" if z == 7 else "right"))
        m.set(HX0, 3, z, DRESS)
        m.set(HX0, 4, z, stairs("minecraft:tuff_brick", "east", "top"))
    m.set(HX0, 3, 6, QUOIN); m.set(HX0, 3, 9, QUOIN)
    m.set(HX0 - 1, 3, 6, wall_torch("west")); m.set(HX0 - 1, 3, 9, wall_torch("west"))
    # a door from the store into the hall, and from the court's far end
    m.set(HX0, 1, 4, door("minecraft:dark_oak", "west", "lower"))
    m.set(HX0, 2, 4, door("minecraft:dark_oak", "west", "upper"))
    m.clear(NX1, NX1, 1, 2, 4, 4)                       # through the wing's end wall too
    m.set(HX0, 1, 10, door("minecraft:dark_oak", "west", "lower"))
    m.set(HX0, 2, 10, door("minecraft:dark_oak", "west", "upper"))
    # tall hall windows on the court and the hill, the upper storey's lights
    for z in (5,):
        window(m, HX0, z, 2, 3)
    for x in (20, 23):
        window(m, x, HZ0, 2, 3); window(m, x, HZ1, 2, 3)
        window(m, x, HZ0, 7, 2); window(m, x, HZ1, 7, 2)
    for z in (4, 9):
        window(m, HX1, z, 2, 3)
    for z in (4, 6, 9):
        window(m, HX0, z, 7, 2)
    for z in (5, 8):
        window(m, HX1, z, 7, 2)
    # the hall: a long table under a hanging lantern, the hearth on the east wall
    m.box(HX0 + 1, HX1 - 1, 0, 0, HZ0 + 1, HZ1 - 1, BOARDS)
    for z in range(4, 10):
        m.set(21, 1, z, slab("minecraft:dark_oak", "top") if z not in (4, 9) else fence("minecraft:dark_oak"))
        m.set(22, 1, z, slab("minecraft:dark_oak", "top") if z not in (4, 9) else fence("minecraft:dark_oak"))
    for z in (5, 7):
        m.set(20, 1, z, stairs("minecraft:spruce", "east")); m.set(23, 1, z, stairs("minecraft:spruce", "west"))
    m.set(21, 2, 6, candle(3)); m.set(22, 2, 8, candle(2))
    m.set(22, 2, 5, "minecraft:potted_azure_bluet"); m.set(21, 2, 8, "minecraft:potted_lily_of_the_valley")
    for x in (21, 22):
        for z in (3, 10):
            m.set(x, 1, z, "minecraft:red_carpet")
    # the hearth: a stone chimney breast on the east wall, a fire under a hood
    for y in range(1, top + 2):
        m.set(HX1, y, 6, "stone"); m.set(HX1, y, 7, "stone")
    m.set(HX1 - 1, 1, 6, "minecraft:campfire[facing=west,lit=true,signal_fire=false,waterlogged=false]")
    m.set(HX1 - 1, 1, 7, "minecraft:campfire[facing=west,lit=true,signal_fire=false,waterlogged=false]")
    m.set(HX1, 1, 6, "minecraft:bricks"); m.set(HX1, 1, 7, "minecraft:bricks")
    m.set(HX1 - 1, 3, 6, stairs("minecraft:stone_brick", "east", "top"))
    m.set(HX1 - 1, 3, 7, stairs("minecraft:stone_brick", "east", "top"))
    m.set(HX1 - 1, 4, 6, "stone"); m.set(HX1 - 1, 4, 7, "stone")
    m.set(HX1 - 1, 5, 6, "stone"); m.set(HX1 - 1, 5, 7, "stone")
    m.set(HX1 - 1, 2, 5, "minecraft:blue_wall_banner[facing=west]")
    m.set(HX1 - 1, 2, 8, "minecraft:blue_wall_banner[facing=west]")
    m.set(19, 1, 3, "minecraft:bookshelf"); m.set(19, 2, 3, "minecraft:bookshelf")
    m.set(24, 1, 3, "minecraft:bookshelf"); m.set(24, 2, 3, "minecraft:bookshelf")
    m.set(24, 1, 10, "minecraft:bookshelf")
    m.set(21, 5, 6, lantern(True)); m.set(22, 5, 8, lantern(True))
    m.set(20, 5, 3, lantern(True)); m.set(23, 5, 10, lantern(True))

    # ---- the court: five wide between the wing and a hedge on the south,
    # paved, the fountain at its middle, flower beds along the wing and the
    # hedge, a bench, goods waiting by the hall door
    m.box(WX0, WX1, 0, 0, 7, 11, "pave")
    for x in range(WX0, WX1 + 1):
        m.set(x, 0, 12, GRASS)
        m.set(x, 1, 12, leaves("minecraft:oak") if x % 4 else leaves("minecraft:azalea"))
    cx, cz = 10, 9
    m.set(cx, 1, cz, "minecraft:water_cauldron[level=3]")
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            if (dx, dz) != (0, 0):
                m.set(cx + dx, 1, cz + dz, slab("minecraft:stone_brick"))
    m.set(cx, 2, cz - 1, "minecraft:potted_white_tulip")
    for x in range(12, 17):
        m.set(x, 0, 7, GRASS)
    for x, fl in ((12, "minecraft:white_tulip"), (13, "minecraft:lily_of_the_valley"), (14, "minecraft:azure_bluet"),
                  (15, "minecraft:white_tulip"), (16, "minecraft:allium")):
        m.set(x, 1, 7, fl)
    for x, fl in ((6, "minecraft:poppy"), (7, "minecraft:cornflower"), (13, "minecraft:oxeye_daisy"), (14, "minecraft:poppy")):
        m.set(x, 0, 11, GRASS); m.set(x, 1, 11, fl)
    m.set(5, 0, 7, GRASS); m.set(5, 1, 7, leaves("minecraft:azalea"))
    for x in (8, 9):
        m.set(x, 1, 11, stairs("minecraft:dark_oak", "north"))           # a bench facing the fountain
    m.set(15, 1, 10, "minecraft:barrel[facing=up,open=false]")
    m.set(16, 1, 11, "minecraft:barrel[facing=up,open=false]")
    m.set(16, 1, 10, "minecraft:white_wool")                              # a bale for the next ship
    for (x, z) in ((5, 10), (12, 11)):
        for y in (1, 2):
            m.set(x, y, z, fence("minecraft:dark_oak"))
        m.set(x, 3, z, lantern(False))
    # the arch over the court's mouth: tuff piers at the wing and the hedge,
    # a stone lintel
    for y in range(1, 6):
        m.set(3, y, 6, PIER if y < 5 else QUOIN)
        m.set(3, y, 12, PIER if y < 5 else QUOIN)
    for z in range(6, 13):
        m.set(3, 5, z, DRESS if z in (6, 12) else "minecraft:tuff_brick_slab[type=top,waterlogged=false]")
        m.set(3, 6, z, slab(ROOF))
    m.set(3, 6, 9, "minecraft:chiseled_tuff_bricks")
    # the house's street face: a bench under the counting room's window
    m.set(3, 1, 4, stairs("minecraft:dark_oak", "east"))
    m.set(3, 1, 3, leaves("minecraft:oak"))

    m.marks["node-merchant"] = (8, 8, "east")
    return m


class Merchant(Plot):
    VARIANTS = VARIANTS


if __name__ == "__main__":
    raise SystemExit(plot_main(build, Merchant, PALETTE,
                               "the roof slopes, the wall heads and the sealed upper storeys: seen, never stood on"))
