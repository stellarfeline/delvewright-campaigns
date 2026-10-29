#!/usr/bin/env python3
"""node/carpenter: the carpenter's lot on the north side of the lane off stretch 3.

Run on the place's saved allocation:

    python3 carpenter.py --allocation <delvec allocation ... node/carpenter> --out ../../../programs/carpenter.json

Form, after a village carpenter's yard: a gable-fronted timber-framed house to
the lane, the shop in front (where a commission is ordered and finished work
stands) and the workroom behind it through a door, the benches under the
windows that look onto the yard; beside it the timber yard, open to the lane,
logs racked between posts and boards stacked to season; at its back an
open-fronted saw shed after the pit-saw shed (corner posts, a rubble back
wall, a lean-to roof) with a log on trestles. The lodging is the upper floor.

Piece-local axes: +x east, +z south (the lane), y 0 the ground course, y 1 the
walk plane. The lane's opening is the last row of the play space (z 16), kept
clear; the uphill side is north.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plotlib import (AIR, Model, Plot, door, fence, gate, lantern, leaves, log, plot_main, slab,  # noqa: E402
                     stairs, trapdoor, wall, pane, candle, tall)

PALETTE = {
    "floor": "minecraft:grass_block[snowy=false]",
    "wall": "minecraft:stone_bricks",
    "lid": "minecraft:spruce_planks",
    "lamp": "minecraft:lantern[hanging=false,waterlogged=false]",
    "turf": "minecraft:grass_block[snowy=false]",
}

VARIANTS = {
    # one structural stone (the town's) for plinths, one rubble for the shed
    "stone": [{"weight": 10, "block": "minecraft:stone_bricks"},
              {"weight": 2, "block": "minecraft:cracked_stone_bricks"},
              {"weight": 1, "block": "minecraft:mossy_stone_bricks"}],
    "rubble": [{"weight": 6, "block": "minecraft:cobblestone"},
               {"weight": 3, "block": "minecraft:mossy_cobblestone"},
               {"weight": 1, "block": "minecraft:andesite"}],
    "yard": [{"weight": 6, "block": "minecraft:coarse_dirt"},
             {"weight": 3, "block": "minecraft:packed_mud"},
             {"weight": 2, "block": "minecraft:gravel"}],
    "path": [{"weight": 5, "block": "minecraft:dirt_path"},
             {"weight": 2, "block": "minecraft:coarse_dirt"}],
}

PLASTER = "minecraft:calcite"
POST = log("minecraft:stripped_spruce_log", "y")
BEAM_X = log("minecraft:stripped_spruce_log", "x")
BEAM_Z = log("minecraft:stripped_spruce_log", "z")
FLOOR = "minecraft:spruce_planks"
ROOF = "minecraft:deepslate_tile"
GLASS = pane("minecraft:glass_pane")

# the house: walls x 2..8, z 4..13; ground floor y 1..4, the floor of the
# lodging at y 5, its walls y 6..8, the roof from y 9
HX0, HX1, HZ0, HZ1 = 2, 8, 4, 13
WALL_Z = 8                     # the wall between the workroom (north) and the shop (south)
UP = 5


def framed_wall(m, cells, y0, y1, posts):
    """A timber-framed wall run: posts at `posts`, plaster between."""
    for (x, z) in cells:
        for y in range(y0, y1 + 1):
            m.set(x, y, z, POST if (x, z) in posts else PLASTER)


def build(a):
    m = Model(a["extent"])
    for s in a["seams"]:
        (x0, y0, z0), (x1, y1, z1) = s["cells"]
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                for z in range(z0, z1 + 1):
                    m.no_touch.add((x, y, z))

    # ---- the parts: the house and the yard with its saw shed
    m.part(HX0, HX1, HZ0, HZ1, "workshop")
    m.part(10, 15, 2, 14, "timber-yard")

    # ---- ground: the yard trodden, a path from the lane to the shop door
    m.box(10, 15, 0, 0, 2, 15, "yard")
    for z in range(14, 17):
        m.set(5, 0, z, "path")
    m.box(9, 9, 0, 0, 3, 15, "path")

    # ---- the house
    corners = {(HX0, HZ0), (HX1, HZ0), (HX0, HZ1), (HX1, HZ1)}
    posts = corners | {(HX0, WALL_Z), (HX1, WALL_Z), (5, HZ0), (5, HZ1), (HX0, 11), (HX1, 11), (HX0, 6), (HX1, 6)}
    ring = [(x, z) for x in range(HX0, HX1 + 1) for z in (HZ0, HZ1)] + \
           [(x, z) for z in range(HZ0 + 1, HZ1) for x in (HX0, HX1)]
    # a stone plinth course, then the frame
    for (x, z) in ring:
        m.set(x, 1, z, POST if (x, z) in corners else "stone")
    framed_wall(m, ring, 2, 4, posts)
    # the floor beam course round the house at the lodging's floor
    for (x, z) in ring:
        m.set(x, UP, z, POST if (x, z) in corners else (BEAM_X if z in (HZ0, HZ1) else BEAM_Z))
    m.box(HX0 + 1, HX1 - 1, UP, UP, HZ0 + 1, HZ1 - 1, FLOOR)
    # the lodging: jettied one cell over the lane front, timber-framed
    up_ring = [(x, z) for x in range(HX0, HX1 + 1) for z in (HZ0, HZ1 + 1)] + \
              [(x, z) for z in range(HZ0 + 1, HZ1 + 1) for x in (HX0, HX1)]
    up_posts = {(HX0, HZ0), (HX1, HZ0), (HX0, HZ1 + 1), (HX1, HZ1 + 1), (5, HZ1 + 1), (5, HZ0),
                (HX0, WALL_Z), (HX1, WALL_Z)}
    framed_wall(m, up_ring, UP + 1, UP + 3, up_posts)
    for x in range(HX0, HX1 + 1):          # the jetty's joists under the overhang
        m.set(x, UP, HZ1 + 1, stairs("minecraft:spruce", "south", "top"))
    m.box(HX0 + 1, HX1 - 1, UP, UP, HZ1, HZ1, FLOOR)
    # the roof: gable to the lane, ridge running north-south
    top = m.gable_roof(HX0, HX1, HZ0, HZ1 + 1, UP + 3, "z", ROOF, fill=PLASTER)
    # the gable's frame: a king post up the middle of each end
    for y in range(UP + 4, top):
        m.set(5, y, HZ1 + 1, POST)
        m.set(5, y, HZ0, POST)
    # the chimney: stone, up the west wall from the workroom hearth
    for y in range(1, top + 2):
        m.set(HX0 - 1, y, 6, "stone")

    # windows: two lights each side, sills of spruce trapdoor... the shop's
    # front window shows the work
    for (x, z) in ((3, HZ1), (4, HZ1), (6, HZ1), (7, HZ1)):          # shop front, either side of the door
        m.set(x, 2, z, GLASS)
        m.set(x, 3, z, GLASS)
    for z in (10, 12):                                                # shop, east and west
        m.set(HX1, 2, z, GLASS); m.set(HX1, 3, z, GLASS)
        m.set(HX0, 2, z, GLASS); m.set(HX0, 3, z, GLASS)
    for z in (5, 7):                                                  # workroom onto the yard (east)
        m.set(HX1, 2, z, GLASS); m.set(HX1, 3, z, GLASS)
    m.set(4, 2, HZ0, GLASS); m.set(4, 3, HZ0, GLASS)                  # workroom, north
    m.set(6, 2, HZ0, GLASS); m.set(6, 3, HZ0, GLASS)
    for (x, z) in ((3, HZ1 + 1), (4, HZ1 + 1), (6, HZ1 + 1), (7, HZ1 + 1), (HX1, 6), (HX1, 10), (HX0, 10), (HX0, 12)):
        m.set(x, UP + 2, z, GLASS)                                    # the lodging's lights

    # the shop door to the lane, under a little pent hood
    m.set(5, 1, HZ1, door("minecraft:spruce", "north", "lower"))
    m.set(5, 2, HZ1, door("minecraft:spruce", "north", "upper"))
    m.set(5, 3, HZ1, PLASTER)
    m.set(5, 4, HZ1, POST)
    # the inner wall between shop and workroom, with its door
    for x in range(HX0 + 1, HX1):
        for y in range(1, UP):
            m.set(x, y, WALL_Z, PLASTER if y < 4 else BEAM_X)
    m.set(5, 1, WALL_Z, door("minecraft:spruce", "north", "lower", "right"))
    m.set(5, 2, WALL_Z, door("minecraft:spruce", "north", "upper", "right"))
    m.set(5, 3, WALL_Z, PLASTER)

    # floors: the shop boarded, the workroom on beaten earth and boards
    m.box(HX0 + 1, HX1 - 1, 0, 0, WALL_Z + 1, HZ1 - 1, "minecraft:spruce_planks")
    m.box(HX0 + 1, HX1 - 1, 0, 0, HZ0 + 1, WALL_Z - 1, "minecraft:packed_mud")
    m.set(5, 0, WALL_Z, "minecraft:spruce_planks")
    m.set(5, 0, HZ1, "minecraft:spruce_planks")

    # ---- the shop: a counter across the back corner, finished work on show
    for z in (9, 10):
        m.set(7, 1, z, "minecraft:stripped_spruce_wood[axis=y]" if z == 9 else stairs("minecraft:spruce", "west", "top"))
    m.set(7, 2, 9, candle(2))
    # a finished chair and table by the window, for a customer to see
    m.set(3, 1, 12, stairs("minecraft:oak", "east"))
    m.set(4, 1, 12, "minecraft:oak_fence[east=false,north=false,south=false,waterlogged=false,west=false]")
    m.set(4, 2, 12, "minecraft:oak_pressure_plate[powered=false]")
    m.set(3, 1, 9, "minecraft:bookshelf")            # the pattern book and the order book
    m.set(3, 1, 10, "minecraft:cartography_table")   # drawings of the work
    m.set(5, 4, 11, lantern(True))

    # ---- the workroom: benches under the windows, the hearth, the lathe
    m.set(7, 1, 5, "minecraft:crafting_table")
    m.set(7, 1, 6, slab("minecraft:spruce", "top"))
    m.set(7, 1, 7, "minecraft:crafting_table")
    m.set(4, 1, 5, "minecraft:fletching_table")      # the joiner's bench with its clamps
    m.set(5, 1, 5, "minecraft:grindstone[face=floor,facing=south]")
    m.set(6, 1, 5, "minecraft:stonecutter[facing=south]")
    m.set(3, 1, 6, "minecraft:stripped_oak_log[axis=z]")   # a beam being dressed
    m.set(3, 1, 7, "minecraft:stripped_oak_log[axis=z]")
    m.set(3, 2, 7, "minecraft:oak_planks")                 # boards stacked on it
    m.set(5, 4, 6, lantern(True))
    m.set(3, 4, 5, lantern(True))

    # ---- behind the house: a log pile under the eave, a bush
    m.box(2, 4, 1, 2, 2, 2, log("minecraft:oak_log", "x"))
    m.set(6, 1, 2, leaves("minecraft:azalea"))
    m.set(7, 1, 2, leaves("minecraft:oak"))
    m.set(8, 1, 1, leaves("minecraft:oak"))

    # ---- the front garden: two flower beds by the path, a bench
    for x in (2, 3, 4, 6, 7, 8):
        m.set(x, 0, 14, "minecraft:podzol[snowy=false]" if x in (2, 8) else "minecraft:grass_block[snowy=false]")
    for x, fl in ((3, "minecraft:poppy"), (4, "minecraft:oxeye_daisy"), (6, "minecraft:cornflower"), (7, "minecraft:allium")):
        m.set(x, 1, 14, fl)
    m.set(2, 1, 14, leaves("minecraft:oak"))
    m.set(8, 1, 14, leaves("minecraft:azalea"))
    m.set(1, 1, 12, stairs("minecraft:spruce", "east"))  # a bench against the west wall
    m.set(1, 1, 11, stairs("minecraft:spruce", "east"))

    # ---- the saw shed: corner posts, a rubble back and east wall, lean-to roof
    SX0, SX1, SZ0, SZ1 = 11, 15, 2, 7
    for z in range(SZ0, SZ1 + 1):
        for y in range(1, 5):
            m.set(SX1, y, z, "rubble")
    for x in range(SX0, SX1 + 1):
        for y in range(1, 6):
            m.set(x, y, SZ0, "rubble")
    for (x, z) in ((SX0, SZ1), (SX0, SZ0)):
        for y in range(1, 5):
            m.set(x, y, z, log("minecraft:oak_log", "y"))
    m.set(SX0, 4, 4, log("minecraft:oak_log", "y"))
    # the lean-to roof: low over the open front, rising to the back wall
    for x in range(SX0 - 1, SX1 + 1):
        m.set(x, 5, SZ1 + 1, stairs("minecraft:spruce", "north"))
        for z in range(5, SZ1 + 1):
            m.set(x, 5, z, slab("minecraft:spruce", "top"))
        m.set(x, 6, 4, stairs("minecraft:spruce", "north"))
        m.set(x, 6, 3, slab("minecraft:spruce", "top"))
        m.set(x, 6, SZ0, slab("minecraft:spruce", "top"))
    for z in range(SZ0, SZ1 + 1):              # the eave beam on the open west side
        m.set(SX0, 5, z, BEAM_Z if z not in (SZ0, SZ1) else log("minecraft:oak_log", "y"))
    # inside: the log on its trestles, the long saw against the wall
    for x in (12, 14):
        m.set(x, 1, 4, fence("minecraft:spruce"))
        m.set(x, 1, 5, fence("minecraft:spruce"))
    for x in (12, 13, 14):
        m.set(x, 2, 4, log("minecraft:oak_log", "x"))
    m.set(13, 1, 3, "minecraft:spruce_trapdoor[facing=north,half=bottom,open=false,powered=false,waterlogged=false]")
    m.set(14, 2, 3, "minecraft:iron_chain[axis=y,waterlogged=false]")
    m.set(14, 3, 3, "minecraft:iron_chain[axis=y,waterlogged=false]")
    m.set(13, 4, 5, lantern(True))
    m.set(12, 1, 6, "minecraft:scaffolding[bottom=false,distance=0,waterlogged=false]")   # a half-made frame

    # ---- the timber yard: logs racked between posts, boards seasoning
    for (x, z) in ((11, 10), (11, 13), (14, 10), (14, 13)):
        for y in (1, 2, 3):
            m.set(x, y, z, fence("minecraft:spruce"))
    for x in (12, 13):                                # the rack: oak logs lying east-west
        for z in (10, 11, 12, 13):
            m.set(x, 1, z, log("minecraft:oak_log", "z"))
            if z in (11, 12):
                m.set(x, 2, z, log("minecraft:spruce_log", "z"))
    m.set(12, 3, 11, log("minecraft:birch_log", "z"))
    # boards in a stickered stack by the shed
    m.box(14, 15, 1, 1, 8, 8, slab("minecraft:oak", "bottom"))
    m.box(15, 15, 1, 1, 10, 12, "minecraft:stripped_oak_wood[axis=z]")   # one high: the gap by the rack is never a pit
    # a handcart: a bed of slabs on a wheel (a trapdoor end on), shafts of fence
    m.set(12, 1, 14, slab("minecraft:spruce", "top"))
    m.set(13, 1, 14, slab("minecraft:spruce", "top"))
    m.set(11, 1, 14, fence("minecraft:spruce"))
    # sawdust and chips: a little leaf litter on the yard
    for (x, z) in ((12, 8), (13, 9), (11, 8)):
        m.set(x, 1, z, "minecraft:leaf_litter[facing=north,segment_amount=3]")
    # a lantern post at the yard's mouth, over the lane
    for y in (1, 2, 3):
        m.set(10, y, 14, fence("minecraft:spruce"))
    m.set(10, 4, 14, lantern(False))

    m.marks["node-carpenter"] = (9, 12, "south")
    return m


class Carpenter(Plot):
    VARIANTS = VARIANTS


if __name__ == "__main__":
    raise SystemExit(plot_main(build, Carpenter, PALETTE,
                               "the roof slopes, the wall heads, the shed roof and the sealed lodging: seen, never stood on"))
