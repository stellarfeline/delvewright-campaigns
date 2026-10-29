#!/usr/bin/env python3
"""node/inn: The Bell, a coaching inn on the square's west side.

    python3 inn.py --allocation <delvec allocation ... node/inn> --out ../../../programs/inn.json

Form, after the galleried coaching inn (the George, Southwark: a timber-framed
range of connected bars to the street, bedrooms over, a coach yard behind with
the stables) and the community's inn-with-stable builds (a common hall with a
serving counter and a hearth, the kitchen behind it through a door, an attached
stable of stalls under a hay loft): an L round a cobbled yard. The inn range
fronts the square, its upper storey jettied over a porch where the inn's bell
hangs for a sign; the taproom is entered from the porch and the kitchen lies
behind it through a door, with a back door to the yard. The stable range
closes the yard's north side, open-fronted, five stalls under a hay loft. A
small stone brewhouse stands in the yard's far corner. The yard holds the
trough, a cart, the mounting block and a tree.

Piece-local axes: +x east (the square), +z south; the square's opening is the
play space's last column (x 28), kept clear with the verge beside it (x 27).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from plotlib import (Model, Plot, candle, door, fence, lantern, leaves, log, pane, plot_main, slab,  # noqa: E402
                     stairs, trapdoor, wall_torch)

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
    "rubble": [{"weight": 6, "block": "minecraft:cobblestone"},
               {"weight": 3, "block": "minecraft:mossy_cobblestone"},
               {"weight": 1, "block": "minecraft:stone"}],
    "cobble": [{"weight": 6, "block": "minecraft:cobblestone"},
               {"weight": 2, "block": "minecraft:andesite"},
               {"weight": 2, "block": "minecraft:gravel"},
               {"weight": 1, "block": "minecraft:mossy_cobblestone"}],
}
ROOF = "minecraft:deepslate_tile"
POST = log("minecraft:dark_oak_log", "y")
BEAM_X = log("minecraft:dark_oak_log", "x")
BEAM_Z = log("minecraft:dark_oak_log", "z")
BRACE = "minecraft:stripped_dark_oak_log[axis=y]"
PLASTER = "minecraft:white_terracotta"
BOARDS = "minecraft:spruce_planks"
GLASS = pane("minecraft:glass_pane")
DRESS = "minecraft:tuff_bricks"
PLINTH = "minecraft:polished_andesite"

# the inn range: ground-floor walls x 15..25, z 2..14; the upper storey
# jettied one cell over the porch, x 15..26; ground floor y 1..4, the floor
# over it y 5, the upper storey y 6..9, the roof from y 9
IX0, IX1, IZ0, IZ1 = 15, 23, 2, 14
PX = IX1 + 3             # the porch's posts, two cells forward of the jetty's face
KITCHEN_WALL = 10
# the stable range: x 2..12, z 2..8, open to the yard on its south side
SX0, SX1, SZ0, SZ1 = 2, 12, 2, 8
# the brewhouse: x 2..7, z 17..22
BX0, BX1, BZ0, BZ1 = 2, 7, 17, 22


def ring(x0, x1, z0, z1):
    return [(x, z) for x in range(x0, x1 + 1) for z in (z0, z1)] + \
           [(x, z) for z in range(z0 + 1, z1) for x in (x0, x1)]


def window(m, x, z, y0=2, h=2):
    for y in range(y0, y0 + h):
        m.set(x, y, z, GLASS)


def door2(m, x, z, facing, hinge="left"):
    m.set(x, 1, z, door("minecraft:dark_oak", facing, "lower", hinge))
    m.set(x, 2, z, door("minecraft:dark_oak", facing, "upper", hinge))


def build(a):
    m = Model(a["extent"])
    a_ex, a_ey, a_ez = a["extent"]
    for s in a["seams"]:
        (x0, y0, z0), (x1, y1, z1) = s["cells"]
        for x in range(x0, x1 + 1):
            for y in range(y0, y1 + 1):
                for z in range(z0, z1 + 1):
                    m.no_touch.add((x, y, z))

    # ---- the parts
    m.part(IX0, IX1, IZ0, IZ1, "inn-house")
    m.part(BX0, BX1, BZ0, BZ1, "inn-house")
    m.part(SX0, SX1, SZ0, SZ1, "stables")
    for x in range(3, 15):
        for z in range(10, 23):
            if not (BX0 <= x <= BX1 and BZ0 <= z <= BZ1):
                m.region[(x, z)] = "inn-yard"
    m.part(15, 24, 16, 21, "inn-yard")

    # ---- ground: the yard cobbled, a cart way from the square
    m.box(3, 24, 0, 0, 9, 22, "cobble")
    m.box(15, 26, 0, 0, 15, 22, "cobble")
    m.box(SX0 + 1, SX1, 0, 0, SZ0 + 1, SZ1, "minecraft:coarse_dirt")

    # ---- the inn range
    gr = ring(IX0, IX1, IZ0, IZ1)
    corners = {(IX0, IZ0), (IX1, IZ0), (IX0, IZ1), (IX1, IZ1)}
    for (x, z) in gr:
        m.set(x, 1, z, PLINTH)
        for y in (2, 3, 4):
            post = (x, z) in corners or (z in (IZ0, IZ1) and x in (18, 22)) or (x in (IX0, IX1) and z in (5, 10, KITCHEN_WALL))
            m.set(x, y, z, POST if post else PLASTER)
    # the upper storey, jettied east over the porch
    ur = ring(IX0, IX1 + 1, IZ0, IZ1)
    ucorners = {(IX0, IZ0), (IX1 + 1, IZ0), (IX0, IZ1), (IX1 + 1, IZ1)}
    for (x, z) in ur:
        m.set(x, 5, z, BEAM_X if z in (IZ0, IZ1) else BEAM_Z)
        for y in (6, 7, 8):
            post = (x, z) in ucorners or (z in (IZ0, IZ1) and x in (18, 22)) or (x in (IX0, IX1 + 1) and z in (4, 6, 8, 10, 12))
            m.set(x, y, z, POST if post else PLASTER)
        m.set(x, 9, z, BEAM_X if z in (IZ0, IZ1) else BEAM_Z)
    for z in range(IZ0, IZ1 + 1):          # the jetty's joist ends over the porch
        m.set(IX1 + 1, 5, z, stairs("minecraft:dark_oak", "east", "top") if z not in (IZ0, IZ1) else BEAM_Z)
    m.box(IX0 + 1, IX1, 5, 5, IZ0 + 1, IZ1 - 1, BOARDS)
    # upper lights: casements between the studs
    for z in (3, 5, 7, 9, 11, 13):
        m.set(IX1 + 1, 7, z, GLASS); m.set(IX0, 7, z, GLASS)
    for x in (17, 20, 22):
        m.set(x, 7, IZ0, GLASS); m.set(x, 7, IZ1, GLASS)
    top = m.gable_roof(IX0, IX1 + 1, IZ0, IZ1, 9, "z", ROOF, fill=PLASTER)
    # a dormer-like gable vent and the gables' king posts
    for y in range(10, top):
        m.set(20, y, IZ0, POST if y < top - 1 else PLASTER)
        m.set(20, y, IZ1, POST if y < top - 1 else PLASTER)
    m.set(20, 11, IZ1, GLASS); m.set(20, 11, IZ0, GLASS)

    # the porch: two cells deep in front of the jetty, posts standing forward
    # of it under a lean-to of tiles, benches, the bell hung for a sign
    for z in (IZ0, 6, 10, IZ1):
        for y in range(1, 5):
            m.set(PX, y, z, POST)
    for z in range(IZ0 - 1, IZ1 + 2):
        m.set(PX, 5, z, stairs(ROOF, "east"))
        m.set(PX - 1, 5, z, slab(ROOF, "top"))
        m.set(PX - 1, 6, z, stairs(ROOF, "east"))
    for z in range(IZ0, IZ1 + 1):
        m.set(PX, 4, z, BEAM_Z if m.get(PX, 4, z) is None else POST)
    m.set(PX - 1, 5, 8, BEAM_Z)                          # the beam the bell hangs from
    m.set(PX - 1, 4, 8, "minecraft:bell[attachment=ceiling,facing=east,powered=false]")
    for z in (3, 4):
        m.set(PX, 1, z, stairs("minecraft:spruce", "west"))
    for z in (12, 13):
        m.set(PX, 1, z, stairs("minecraft:spruce", "west"))
    m.set(PX, 1, 5, "minecraft:potted_red_tulip")
    m.set(PX, 1, 11, "minecraft:potted_cornflower")
    m.box(IX1 + 1, PX, 0, 0, IZ0, IZ1, "minecraft:stone_bricks")
    # the front door from the porch, windows either side
    door2(m, IX1, 6, "west")
    m.set(IX1, 3, 6, PLASTER)
    m.set(IX1, 4, 6, BEAM_Z)
    for z in (3, 4, 8, 9):
        window(m, IX1, z)
    for z in (12, 13):
        window(m, IX1, z, 2, 2)

    # inside: the taproom (z 3..9) and the kitchen (z 11..13)
    m.box(IX0 + 1, IX1 - 1, 0, 0, IZ0 + 1, IZ1 - 1, BOARDS)
    for x in range(IX0 + 1, IX1):
        for y in range(1, 5):
            m.set(x, y, KITCHEN_WALL, PLASTER if y < 4 else BEAM_X)
    door2(m, 18, KITCHEN_WALL, "north")
    m.set(18, 3, KITCHEN_WALL, PLASTER)
    # the hearth in the north wall: a stone chimney breast and a fire
    for y in range(1, top + 2):
        for x in (20, 21):
            m.set(x, y, IZ0, "stone")
    for y in range(1, 4):
        m.set(19, y, IZ0, "stone") if y < 3 else None
        m.set(22, y, IZ0, "stone") if y < 3 else None
    m.set(20, 1, IZ0 + 1, "minecraft:campfire[facing=south,lit=true,signal_fire=false,waterlogged=false]")
    m.set(21, 1, IZ0 + 1, "minecraft:campfire[facing=south,lit=true,signal_fire=false,waterlogged=false]")
    m.set(20, 1, IZ0, "minecraft:bricks"); m.set(21, 1, IZ0, "minecraft:bricks")
    m.set(20, 3, IZ0 + 1, stairs("minecraft:stone_brick", "north", "top"))
    m.set(21, 3, IZ0 + 1, stairs("minecraft:stone_brick", "north", "top"))
    m.set(20, 4, IZ0 + 1, "stone"); m.set(21, 4, IZ0 + 1, "stone")
    # the serving counter across the taproom's west end, casks behind it
    for z in range(3, 9):
        m.set(18, 1, z, stairs("minecraft:spruce", "east", "top") if z != 8 else trapdoor("minecraft:spruce", "east"))
    for z in (3, 7):
        m.set(16, 1, z, "minecraft:barrel[facing=up,open=false]")                 # the ale casks
    m.set(16, 1, 5, log("minecraft:spruce_log", "x"))           # a cask on its side
    m.set(16, 2, 5, candle(1))
    m.set(16, 1, 4, "minecraft:spruce_planks"); m.set(16, 2, 4, slab("minecraft:spruce"))
    m.set(18, 2, 4, candle(2))
    m.set(18, 2, 7, "minecraft:potted_oxeye_daisy")
    # tables and stools
    for (tx, tz) in ((20, 5), (20, 8)):
        m.set(tx, 1, tz, fence("minecraft:dark_oak"))
        m.set(tx, 2, tz, "minecraft:dark_oak_pressure_plate[powered=false]")
        m.set(tx + 1, 1, tz, stairs("minecraft:spruce", "west"))
        m.set(tx - 1, 1, tz, stairs("minecraft:spruce", "east")) if tx - 1 != 18 else None
    m.set(22, 1, 7, stairs("minecraft:spruce", "west")); m.set(22, 1, 4, stairs("minecraft:spruce", "west"))
    for (lx, lz) in ((21, 4), (22, 7), (17, 6)):
        m.set(lx, 4, lz, lantern(True))
    # the kitchen: the cooking hearth on the west wall, the table, the cauldron
    m.set(16, 1, 12, "minecraft:campfire[facing=east,lit=true,signal_fire=false,waterlogged=false]")
    for y in range(1, top + 1):
        m.set(IX0, y, 12, "stone")
    m.set(16, 3, 12, stairs("minecraft:stone_brick", "west", "top"))
    m.set(16, 4, 12, "stone")
    m.set(16, 1, 11, "minecraft:water_cauldron[level=3]")
    m.set(16, 1, 13, "minecraft:crafting_table")
    for x in (20, 21, 22):
        m.set(x, 1, 12, slab("minecraft:spruce", "top"))
    m.set(21, 2, 12, candle(3))
    m.set(22, 1, 11, "minecraft:hay_block[axis=y]")             # sacks of meal
    m.set(22, 1, 13, "minecraft:smooth_stone_slab[type=top,waterlogged=false]")
    m.set(21, 1, 13, "minecraft:smooth_stone_slab[type=top,waterlogged=false]")
    m.set(20, 4, 12, lantern(True))
    # the kitchen's back door to the yard, and its window
    door2(m, 20, IZ1, "north")
    m.set(20, 3, IZ1, PLASTER)
    window(m, 17, IZ1); window(m, 23, IZ1)

    # ---- the stable range: stone back and end walls, open to the yard
    for x in range(SX0, SX1 + 1):
        for y in range(1, 6):
            m.set(x, y, SZ0, "rubble" if y < 5 else BEAM_X)
    for z in range(SZ0, SZ1 + 1):
        for y in range(1, 6):
            m.set(SX0, y, z, "rubble" if y < 5 else BEAM_Z)
            m.set(SX1, y, z, ("rubble" if y < 5 else BEAM_Z) if z < SZ1 else POST)
    for x in range(SX0, SX1 + 1, 2):
        for y in range(1, 5):
            m.set(x, y, SZ1, POST)
    for x in range(SX0, SX1 + 1):
        m.set(x, 5, SZ1, BEAM_X)
    # the loft floor and its open front, hay stacked in it
    m.box(SX0 + 1, SX1 - 1, 5, 5, SZ0 + 1, SZ1 - 1, BOARDS)
    for x in range(SX0 + 1, SX1):
        for z in (SZ0 + 1, SZ0 + 2):
            m.set(x, 6, z, "minecraft:hay_block[axis=x]")
        if x % 3 == 0:
            m.set(x, 7, SZ0 + 1, "minecraft:hay_block[axis=x]")
    m.gable_roof(SX0, SX1, SZ0, SZ1, 6, "x", ROOF, fill="rubble")
    # stalls: fence partitions, hay at the back of each, a manger
    for x in (4, 6, 8, 10):
        for z in range(SZ0 + 1, SZ1 - 1):
            m.set(x, 1, z, fence("minecraft:spruce"))
    for x in (3, 5, 7, 9, 11):
        m.set(x, 1, SZ0 + 1, "minecraft:hay_block[axis=z]")
        m.set(x, 1, SZ0 + 2, "minecraft:composter[level=0]") if x in (5, 9) else None
    for (x, z) in ((3, 6), (7, 5), (11, 6)):
        m.set(x, 1, z, "minecraft:leaf_litter[facing=north,segment_amount=2]")
    m.set(7, 4, 5, lantern(True)); m.set(3, 4, 5, lantern(True)); m.set(11, 4, 5, lantern(True))

    # ---- the brewhouse: a small stone house in the yard's corner
    for (x, z) in ring(BX0, BX1, BZ0, BZ1):
        for y in range(1, 5):
            m.set(x, y, z, "stone" if y > 1 else PLINTH)
    m.box(BX0 + 1, BX1 - 1, 0, 0, BZ0 + 1, BZ1 - 1, "minecraft:bricks")
    m.gable_roof(BX0, BX1, BZ0, BZ1, 5, "z", ROOF, fill="stone")
    door2(m, BX1, 19, "west")
    m.set(BX1, 3, 19, DRESS)
    window(m, 4, BZ0); window(m, BX1, 21)
    m.set(3, 1, 18, "minecraft:water_cauldron[level=3]")
    m.set(4, 1, 18, "minecraft:cauldron")
    m.set(3, 1, 20, "minecraft:campfire[facing=east,lit=true,signal_fire=false,waterlogged=false]")
    m.set(3, 1, 21, "minecraft:hay_block[axis=y]")           # malt in sacks
    m.set(5, 1, 21, log("minecraft:spruce_log", "z"))
    m.set(5, 1, 20, log("minecraft:spruce_log", "z"))
    m.set(5, 2, 21, log("minecraft:spruce_log", "z"))
    m.set(3, 3, 19, wall_torch("east"))
    for y in range(1, 9):
        m.set(BX0, y, 20, "stone")                          # its flue

    # ---- the yard: the trough, a cart, the mounting block, a tree
    for x in (10, 11):
        m.set(x, 1, 11, "minecraft:water_cauldron[level=3]")
    m.set(9, 1, 11, slab("minecraft:stone_brick")); m.set(12, 1, 11, slab("minecraft:stone_brick"))
    # a cart: its bed of slabs, wheels of open trapdoors, shafts of fence
    for z in (15, 16, 17):
        m.set(11, 1, z, slab("minecraft:spruce", "top")); m.set(12, 1, z, slab("minecraft:spruce", "top"))
    m.set(10, 1, 16, trapdoor("minecraft:dark_oak", "west", "bottom", True))
    m.set(13, 1, 16, trapdoor("minecraft:dark_oak", "east", "bottom", True))
    m.set(11, 1, 18, fence("minecraft:spruce")); m.set(12, 1, 18, fence("minecraft:spruce"))
    m.set(11, 2, 15, "minecraft:hay_block[axis=x]")
    # the mounting block by the stable
    m.set(13, 1, 9, stairs("minecraft:stone_brick", "west")); m.set(14, 1, 9, "stone")
    # a tree: an oak in the yard's south-east corner, a bench under it
    for y in range(1, 6):
        m.set(22, y, 20, log("minecraft:oak_log", "y"))
    for x in range(20, 25):
        for z in range(18, 23):
            for y in (5, 6, 7):
                d = abs(x - 22) + abs(z - 20) + (y - 5) * 2
                if d <= 3 and (x, z) != (22, 20) or (y == 7 and (x, z) == (22, 20)):
                    m.set(x, y, z, leaves("minecraft:oak"))
    m.set(22, 1, 21, stairs("minecraft:spruce", "north")); m.set(21, 1, 21, stairs("minecraft:spruce", "north"))
    # a hitching rail by the square, flower beds along the range's south wall
    for z in range(16, 20):
        m.set(25, 1, z, fence("minecraft:spruce"))
    for x in (16, 18, 22, 24):
        m.set(x, 0, IZ1 + 1, GRASS)
    for x, fl in ((16, "minecraft:poppy"), (18, "minecraft:dandelion"), (22, "minecraft:cornflower"),
                  (24, "minecraft:oxeye_daisy")):
        m.set(x, 1, IZ1 + 1, fl)
    # the yard's lantern post, bushes along the south and west, set back
    for y in (1, 2, 3):
        m.set(14, y, 14, fence("minecraft:spruce"))
    m.set(14, 4, 14, lantern(False))
    for (x, z) in ((9, 22), (10, 22), (14, 22), (2, 12), (2, 14), (17, 22)):
        m.set(x, 0, z, GRASS)
        m.set(x, 1, z, leaves("minecraft:azalea" if (x + z) % 2 else "minecraft:oak"))
    m.set(15, 0, 22, GRASS); m.set(12, 0, 22, GRASS)
    m.set(15, 1, 22, "minecraft:rose_bush[half=lower]"); m.set(15, 2, 22, "minecraft:rose_bush[half=upper]")
    m.set(12, 1, 22, "minecraft:lilac[half=lower]"); m.set(12, 2, 22, "minecraft:lilac[half=upper]")
    # the north eave strip behind the inn: a woodpile for the hearths
    m.box(16, 19, 1, 2, 1, 1, log("minecraft:oak_log", "x"))

    # where the lot's open north and south edges meet the square's corners,
    # a tall stone pier stands in the ring: the yard's gate pier on the south,
    # the gable chimney's foot on the north, so the inn and the square meet
    # only across the front the plan allocates
    for z in (0, a_ez - 1):
        for x in (IX1 + 3, IX1 + 4, IX1 + 5):
            for y in range(1, a_ey):
                m.set(x, y, z, "stone")
    m.marks["node-inn"] = (PX - 1, 8, "west")
    return m


class Inn(Plot):
    VARIANTS = VARIANTS


if __name__ == "__main__":
    raise SystemExit(plot_main(build, Inn, PALETTE,
                               "the roof slopes, the wall heads, the hay loft and the sealed upper storey: seen, never stood on"))
