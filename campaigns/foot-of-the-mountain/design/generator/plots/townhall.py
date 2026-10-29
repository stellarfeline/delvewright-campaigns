#!/usr/bin/env python3
"""node/townhall: the guildhall, on stretch 4's west side.

    DELVEWRIGHT_SKILL=<skill> python3 townhall.py --allocation <delvec allocation ... node/townhall> \\
        --out ../../../programs/townhall.json --delvec <delvec>

Form, after the market hall and guildhall of a medieval town (an open
arcade on stone piers where the market stands under cover, the guild's hall
over it, timber-framed with a long run of windows, a clock or a bell in a
turret over the front, the guild's office closed off at the back): the hall
end-on to the street, its arcade open on three sides with market stalls under
it, the clerk's office behind the arcade through a door, the hall over the
arcade under a high tiled roof, a clock face in the front gable and a bell
turret on the ridge; a paved forecourt with a market cross before it.

Piece-local axes: +x east (the street), +z south; the street's opening is the
play space's last column (x 24), kept clear with the verge beside it (x 23).
Drawn on the skill starter's Model; the engine says where a body goes.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from starter import Model, run  # noqa: E402
from kit import (bed_of, candle, door2, fence, gable_roof, lantern, leaves, log, pane, ring, slab,  # noqa: E402
                 stairs, wall_torch, window)

GRASS = "minecraft:grass_block[snowy=false]"
ROOF = "minecraft:deepslate_tile"
PIER = "minecraft:polished_tuff"
DRESS = "minecraft:tuff_bricks"
QUOIN = "minecraft:chiseled_tuff_bricks"
POST = log("minecraft:dark_oak_log", "y")
BEAM_X = log("minecraft:dark_oak_log", "x")
BEAM_Z = log("minecraft:dark_oak_log", "z")
PLASTER = "minecraft:calcite"
GLASS = pane("minecraft:glass_pane")

# the hall: x 6..19, z 2..9. The arcade y 1..4 under the hall's floor at y 5,
# the hall's walls y 6..9, the roof from the wall head at 9. The office: the
# arcade's west bay, x 6..9, walled.
HX0, HX1, HZ0, HZ1 = 6, 19, 2, 9
OFFICE_X = 9


def build(place) -> Model:
    m = Model(place)
    m.palette.update({
        "floor": GRASS,
        "stone": [{"weight": 12, "block": "minecraft:stone_bricks"},
                  {"weight": 2, "block": "minecraft:cracked_stone_bricks"},
                  {"weight": 1, "block": "minecraft:mossy_stone_bricks"}],
        "pave": [{"weight": 5, "block": "minecraft:polished_andesite"},
                 {"weight": 3, "block": "minecraft:stone_bricks"},
                 {"weight": 1, "block": "minecraft:andesite"}],
    })
    m.part(HX0, HX1, HZ0, HZ1, "hall")
    m.part(20, 22, 2, 9, "forecourt")
    m.part(HX0, HX1, 10, 11, "forecourt")

    # ---- ground: the arcade and the forecourt paved
    m.box(HX0, 22, 0, 0, HZ0, 11, "pave")

    # ---- the arcade: tuff piers every three cells round the hall's footprint,
    # arches of stairs between them under a beam
    piers = sorted(set([(x, z) for (x, z) in ring(HX0, HX1, HZ0, HZ1)
                        if ((x - HX0) % 3 == 0 and z in (HZ0, HZ1)) or (x in (HX0, HX1) and (z - HZ0) % 3 == 0)]
                       + [(HX1, HZ1), (HX0, HZ1)]))
    for (x, z) in piers:
        for y in (1, 2, 3):
            m.set(x, y, z, PIER)
        m.set(x, 4, z, QUOIN)
    for (x, z) in ring(HX0, HX1, HZ0, HZ1):
        if m.get(x, 4, z) is None:
            m.set(x, 4, z, "stone")
    # the arch heads: an upside-down stair either side of each pier at course 3
    for (x, z) in piers:
        for dx, dz, face in ((1, 0, "west"), (-1, 0, "east"), (0, 1, "north"), (0, -1, "south")):
            nx, nz = x + dx, z + dz
            if (nx, nz) in set(ring(HX0, HX1, HZ0, HZ1)) and m.get(nx, 3, nz) is None:
                m.set(nx, 3, nz, stairs(DRESS, face, "top"))
    # the hall's floor over the arcade
    m.box(HX0 + 1, HX1 - 1, 5, 5, HZ0 + 1, HZ1 - 1, "minecraft:dark_oak_planks")
    m.box(HX0, HX1, 5, 5, HZ0, HZ0, BEAM_X); m.box(HX0, HX1, 5, 5, HZ1, HZ1, BEAM_X)
    m.box(HX0, HX0, 5, 5, HZ0 + 1, HZ1 - 1, BEAM_Z); m.box(HX1, HX1, 5, 5, HZ0 + 1, HZ1 - 1, BEAM_Z)

    # ---- the office: the arcade's west bay walled, a door from the arcade
    for z in range(HZ0, HZ1 + 1):
        for y in (1, 2, 3):
            m.set(OFFICE_X, y, z, "stone")
    for x in range(HX0, OFFICE_X + 1):
        for z in (HZ0, HZ1):
            for y in (1, 2, 3):
                m.set(x, y, z, PIER if (x, z) in piers else "stone")
    for z in range(HZ0, HZ1 + 1):
        for y in (1, 2, 3):
            m.set(HX0, y, z, PIER if (HX0, z) in piers else "stone")
    door2(m, OFFICE_X, 6, "minecraft:dark_oak", "east")
    window(m, HX0, 4, GLASS, 2, 1); window(m, HX0, 7, GLASS, 2, 1)
    m.box(HX0 + 1, OFFICE_X - 1, 0, 0, HZ0 + 1, HZ1 - 1, "minecraft:dark_oak_planks")
    m.set(7, 1, 3, "minecraft:lectern[facing=east,has_book=false,powered=false]")      # the guild's book
    m.set(7, 1, 8, slab("minecraft:dark_oak", "top")); m.set(8, 1, 8, slab("minecraft:dark_oak", "top"))
    m.set(8, 2, 8, candle(3))
    m.set(7, 1, 5, "minecraft:bookshelf"); m.set(7, 2, 5, "minecraft:bookshelf")
    m.set(8, 4, 6, lantern(True))

    # ---- under the arcade: market stalls, sacks, a weigh-beam
    for (x, z) in ((11, 3), (12, 3), (14, 3), (15, 3)):
        m.set(x, 1, z, slab("minecraft:spruce", "top"))
    m.set(12, 2, 3, "minecraft:potted_red_tulip"); m.set(15, 2, 3, "minecraft:potted_dandelion")
    for (x, z) in ((11, 8), (12, 8)):
        m.set(x, 1, z, "minecraft:hay_block[axis=x]")
    m.set(15, 1, 8, "minecraft:barrel[facing=up,open=false]"); m.set(16, 1, 8, "minecraft:barrel[facing=up,open=false]")
    for x in (11, 15):
        m.set(x, 4, 6, lantern(True))

    # ---- the hall over the arcade: timber frame, plaster, a long run of windows
    corners = {(HX0, HZ0), (HX1, HZ0), (HX0, HZ1), (HX1, HZ1)}
    for (x, z) in ring(HX0, HX1, HZ0, HZ1):
        for y in (6, 7, 8):
            post = (x, z) in corners or ((x - HX0) % 3 == 0 and z in (HZ0, HZ1)) or ((z - HZ0) % 3 == 0 and x in (HX0, HX1))
            m.set(x, y, z, POST if post else (GLASS if y in (7, 8) else PLASTER))
        m.set(x, 9, z, BEAM_X if z in (HZ0, HZ1) else BEAM_Z)
    top = gable_roof(m, HX0, HX1, HZ0, HZ1, 9, "x", ROOF, fill=PLASTER)
    # the clock face in the street gable, the guild's banners under it
    cx, cz = HX1, (HZ0 + HZ1) // 2
    for dz in (-1, 0, 1, 2):
        for dy in (0, 1, 2):
            if dz in (0, 1) or dy == 1:
                m.set(cx, 11 + dy, cz + dz, QUOIN if (dz in (0, 1) and dy == 1) else DRESS)
    m.set(cx, 12, cz, "minecraft:yellow_stained_glass"); m.set(cx, 12, cz + 1, "minecraft:yellow_stained_glass")
    # the bell turret on the ridge over the hall's middle: four posts, a cap,
    # the bell hung from it
    bx, bz = (HX0 + HX1) // 2, (HZ0 + HZ1) // 2
    if top + 3 < m.ey:
        for (x, z) in ((bx, bz), (bx + 1, bz), (bx, bz + 1), (bx + 1, bz + 1)):
            m.set(x, top + 1, z, POST)
        m.set(bx, top + 2, bz, "minecraft:dark_oak_planks"); m.set(bx + 1, top + 2, bz, "minecraft:dark_oak_planks")
        m.set(bx, top + 2, bz + 1, "minecraft:dark_oak_planks"); m.set(bx + 1, top + 2, bz + 1, "minecraft:dark_oak_planks")

    # ---- the forecourt: a market cross, benches, beds, a lantern post
    for y in (1, 2, 3):
        m.set(21, y, 6, "stone" if y == 1 else "minecraft:stone_brick_wall[east=none,north=none,south=none,up=true,waterlogged=false,west=none]")
    m.set(21, 4, 6, lantern(False))
    m.set(20, 1, 6, stairs("minecraft:stone_brick", "west")); m.set(22, 1, 6, stairs("minecraft:stone_brick", "east"))
    m.set(21, 1, 5, stairs("minecraft:stone_brick", "north")); m.set(21, 1, 7, stairs("minecraft:stone_brick", "south"))
    for x in (8, 9):
        m.set(x, 1, 11, stairs("minecraft:spruce", "north"))
    bed_of(m, [(12, 11), (13, 11), (14, 11), (16, 11), (17, 11)],
           ["minecraft:poppy", "minecraft:cornflower", "minecraft:oxeye_daisy"])
    for (x, z) in ((20, 2), (22, 9), (19, 11), (6, 11)):
        m.set(x, 0, z, GRASS); m.set(x, 1, z, leaves("minecraft:azalea" if x % 2 else "minecraft:oak"))
    # behind the hall: a lean-to woodstore against the office
    for z in range(3, 9):
        m.set(4, 1, z, log("minecraft:oak_log", "z")); m.set(4, 2, z, log("minecraft:oak_log", "z"))
    m.mark("node-townhall", 13, 6, "east")
    m.finish()
    return m


if __name__ == "__main__":
    raise SystemExit(run(build, reason="the roof slopes, the wall heads, the sealed hall over the arcade and the bell turret: seen, never stood on"))
