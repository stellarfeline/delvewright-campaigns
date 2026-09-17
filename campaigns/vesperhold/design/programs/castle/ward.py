"""The outer ward and what stands round it: the stables, the barracks and
armory, the keep steps, the cloister lane, the inner walls and the gardens."""
from . import layout as L
from .grid import room, crenels, gable, hsh, stairs, slab, block, AIR
from .palette import (WALL, WALL_RUIN, TRIM, QUOIN, FLAG, FLOOR, LANTERN, LANTERN_HANG,
                      DARK_PLANKS, PLANKS, COBWEB, POST, BEAM, BEAM_Z, HAY, STRAW,
                      TURF, ROCK_MOSS, ROOF, ROOF_RUIN, ROOF_MAT, CANDLES, CHAIN,
                      GATE_WOOD, KEEP, WATER, LOG, DARK_LEAVES, PILLAR)

C = L.CASTLE
SB = "minecraft:stone_brick_stairs"


def grounds(g):
    """Everything inside the curtain that is not a building: flagstones in the
    ward, grass and rubble elsewhere."""
    x0, x1, z0, z1 = L.CRAG
    g.box(x0 + 3, x1 - 3, C - 1, C - 1, z0 + 3, z1 - 3, TURF)
    for x in range(x0 + 3, x1 - 2):
        for z in range(z0 + 3, z1 - 2):
            if hsh(x, z, 91) < .025:
                g.set(x, C, z, ROCK_MOSS)
    # gardens: a few dark trees behind the keep and east of it
    for (tx, tz) in ((118, 40), (126, 64), (116, 84), (134, 30), (40, 124), (132, 88)):
        g.box(tx, tx, C, C + 5, tz, tz, LOG)
        for dy in range(3, 7):
            r = 2 if dy < 6 else 1
            for dx in range(-r, r + 1):
                for dz in range(-r, r + 1):
                    if (dx or dz) and abs(dx) + abs(dz) <= r + 1 and hsh(tx + dx, tz + dz, dy) < .85:
                        if g.get(tx + dx, C + dy, tz + dz) == AIR:
                            g.set(tx + dx, C + dy, tz + dz, DARK_LEAVES)


def ward(g):
    p = L.P["outer-ward"]
    x0, x1, z0, z1 = p.box
    g.box(x0, x1, C - 1, C - 1, z0, z1, FLAG)
    # a broad paved cross and a dry fountain in the middle
    cx, cz = 88, 126
    g.box(cx - 5, cx + 5, C - 1, C - 1, cz - 5, cz + 5, FLOOR)
    g.box(cx - 3, cx + 3, C, C, cz - 3, cz + 3, PILLAR)
    g.clear(cx - 2, cx + 2, C, C, cz - 2, cz + 2)
    g.box(cx - 2, cx + 2, C - 1, C - 1, cz - 2, cz + 2, ROCK_MOSS)
    g.box(cx, cx, C, C + 3, cz, cz, PILLAR)
    g.set(cx, C + 4, cz, TRIM)
    # the inner wall on the ward's open sides, eight high, crenellated
    for (a0, a1, b0, b1) in ((108, 123, 92, 99), (124, 124, 100, 119), (124, 124, 136, 151),
                             (52, 74, 152, 152), (101, 123, 152, 152), (49, 51, 100, 131)):
        g.box(a0, a1, C - 1, C + 7, b0, b1, WALL)
    for x in range(108, 124, 2):
        g.set(x, C + 8, 92, WALL)
    for z in range(100, 152, 2):
        if not 120 <= z <= 135:
            g.set(124, C + 8, z, WALL)
    # the winch for the portcullis, against the south wall
    g.box(84, 84, C, C + 2, 150, 150, POST)
    g.box(92, 92, C, C + 2, 150, 150, POST)
    g.box(84, 92, C + 2, C + 2, 150, 150, BEAM)
    g.box(86, 90, C + 1, C + 1, 150, 150, DARK_PLANKS)
    # lanterns on posts round the ward
    for (lx, lz) in ((56, 104), (56, 146), (120, 104), (120, 146), (70, 126), (106, 126)):
        g.box(lx, lx, C, C + 1, lz, lz, POST)
        g.set(lx, C + 2, lz, LANTERN)
    # rubble and a fallen cart
    g.box(100, 102, C, C, 138, 139, DARK_PLANKS)
    g.set(101, C + 1, 138, PLANKS)
    for (rx, rz) in ((62, 110), (63, 111), (114, 143), (76, 144)):
        g.set(rx, C, rz, ROCK_MOSS)
    g.mark("outer-ward", 88, C, 140, "north")
    g.mark("portcullis-winch", 88, C, 148, "north")
    g.mark("ward-patrol", 72, C, 118, "south")
    g.mark("ward-patrol-east", 108, C, 132, "west")


def stables(g):
    p = L.P["stables"]
    x0, x1, z0, z1 = p.box
    top = C + p.height
    room(g, x0, x1, z0, z1, C, p.height, WALL, STRAW)
    # timber posts and beams, stalls down both long sides
    for x in range(x0 + 1, x1, 4):
        for z in (z0 + 3, z1 - 3):
            g.box(x, x, C, top - 1, z, z, POST)
        g.box(x, x, top - 1, top - 1, z0, z1, BEAM_Z)
        for z in range(z0, z0 + 3):
            g.set(x, C, z, DARK_PLANKS)
        for z in range(z1 - 2, z1 + 1):
            g.set(x, C, z, DARK_PLANKS)
    for x in range(x0 + 2, x1, 8):
        g.set(x, C, z0, HAY)
        g.set(x + 1, C, z1, HAY)
    # doors: west through the curtain, east into the ward
    g.clear(x0 - 1, x0 - 1, C, C + 2, 138, 140)
    g.clear(x1 + 1, x1 + 4, C, C + 3, 137, 141)
    g.box(x1 + 1, x1 + 4, C - 1, C - 1, 137, 141, FLAG)
    g.box(x1 + 1, x1 + 4, C - 1, C + 7, 132, 136, WALL)
    g.box(x1 + 1, x1 + 4, C - 1, C + 7, 142, 147, WALL)
    g.box(x1 + 1, x1 + 4, C + 4, C + 7, 137, 141, WALL)
    # a slate roof, holed
    g.box(x0 - 1, x1 + 1, top, top, z0 - 1, z1 + 1, PLANKS)
    gable(g, x0 - 1, x1 + 1, z0 - 1, z1 + 1, top + 1, ROOF_MAT, ROOF, along="x")
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if hsh(x, z, 101) < .08:
                g.clear(x, x, top, top + 12, z, z)
    g.set(x0 + 1, C, 139, LANTERN)
    g.set(x1 - 1, C, 139, LANTERN)
    g.mark("stables", 32, C, 139, "west")
    g.mark("stables-grooms", 30, C, 136, "west")
    g.mark("stable-horse-1", 19, C, z0 + 1, "south")
    g.mark("stable-horse-2", 31, C, z0 + 1, "south")
    g.mark("stable-horse-3", 23, C, z1 - 1, "north")
    g.mark("stable-horse-4", 35, C, z1 - 1, "north")


def barracks(g):
    p = L.P["barracks"]
    x0, x1, z0, z1 = p.box
    top = C + p.height
    room(g, x0, x1, z0, z1, C, p.height, WALL, FLOOR, ceiling=PLANKS)
    # bunks along both long walls, blank plates above them
    bunk = slab("minecraft:spruce_slab")
    for x in range(x0 + 1, x1, 3):
        for z in (z0, z1):
            g.set(x, C, z, DARK_PLANKS)
            g.set(x, C + 2, z, bunk)
            g.set(x + 1, C, z, bunk)
        g.set(x, C + 4, z0 - 1, block("minecraft:polished_andesite"))
    # the long table
    g.box(x0 + 5, x1 - 5, C, C, 153, 154, DARK_PLANKS)
    for x in range(x0 + 5, x1 - 4, 2):
        g.set(x, C + 1, 153, CANDLES) if hsh(x, 153, 111) < .3 else None
    # the gable roof over it
    gable(g, x0 - 1, x1 + 1, z0 - 1, z1 + 1, top + 1, ROOF_MAT, ROOF, along="x")
    # door from the ward (west), door to the armory (east)
    g.box(124, 125, C - 1, C + 7, 144, 151, WALL)
    g.clear(124, 125, C, C + 2, 146, 148)
    g.box(124, 125, C - 1, C - 1, 146, 148, FLOOR)
    g.box(x1 + 1, x1 + 2, C - 1, C + 6, 144, 163, WALL)
    g.clear(x1 + 1, x1 + 2, C, C + 1, 150, 150)
    g.box(x1 + 1, x1 + 2, C - 1, C - 1, 150, 150, FLOOR)
    for z in (z0 + 4, z1 - 4):
        g.set(x0 + 1, C, z, LANTERN)
    g.set(x1 - 1, C, z1 - 8, LANTERN)
    g.mark("barracks", 138, C, 150, "west")
    g.mark("barracks-guard", 142, C, 152, "west")


def armory(g):
    p = L.P["armory"]
    x0, x1, z0, z1 = p.box
    room(g, x0, x1, z0, z1, C, p.height, WALL, FLOOR, ceiling=WALL)
    g.clear(x0 - 1, x0 - 1, C, C + 1, 150, 150)          # the door from the barracks
    # racks on the walls
    for z in range(z0 + 1, z1, 2):
        g.set(x1, C + 1, z, block("minecraft:dark_oak_fence_gate[facing=west,in_wall=false,open=false,powered=false]"))
    g.box(x0 + 1, x0 + 3, C, C, z0, z0, DARK_PLANKS)
    g.box(x0 + 1, x0 + 3, C, C, z1, z1, DARK_PLANKS)
    g.set(x1 - 1, C, z0, LANTERN)
    g.set(x0, C + p.height - 1, z1, COBWEB)
    g.mark("armory", 155, C, 150, "west")
    g.mark("false-chest", 157, C, 152, "west")
    g.mark("armory-ambush", 154, C, 148, "east")


def keep_steps(g):
    p = L.P["keep-steps"]
    x0, x1, z0, z1 = p.box
    top = C + p.height
    # a vaulted porch open to the ward on its south side
    room(g, x0, x1, z0, z1, C, p.height, KEEP, FLOOR, ceiling=KEEP)
    g.clear(x0, x1, C, top - 3, z1 + 1, z1 + 1)
    for x in (x0 - 1, x1 + 1):
        g.box(x, x, C - 1, top + 2, z1 + 1, z1 + 2, QUOIN)
    for x in range(x0 + 1, x1, 4):
        g.box(x, x, C, top - 3, z1 + 1, z1 + 1, PILLAR)
    g.box(x0, x1, top - 2, top - 1, z1 + 1, z1 + 1, KEEP)
    crenels(g, x0 - 1, x1 + 1, z0 - 1, z1 + 1, top + 1, KEEP)
    # the Keep Doors in the north wall are the great hall's (keep.py)
    g.set(x0, C, z1, LANTERN); g.set(x1, C, z1, LANTERN)
    g.mark("keep-steps", 83, C, 97, "north")


def lane(g):
    p = L.P["cloister-lane"]
    x0, x1, z0, z1 = p.box
    g.box(x0, x1, C - 1, C - 1, z0, z1, FLAG)
    # walls on both sides, the lane open overhead
    g.box(x0 - 4, x0 - 1, C - 1, C + 7, z0, z1, WALL)
    g.box(x1 + 1, x1 + 2, C - 1, C + 7, z0, z1, WALL)
    for z in range(z0, z1 + 1, 2):
        g.set(x0 - 4, C + 8, z, WALL); g.set(x1 + 2, C + 8, z, WALL)
    # arches across the lane every ten cells
    for z in range(z0 + 5, z1, 10):
        g.box(x0, x1, C + 5, C + 6, z, z, WALL)
        g.set(x0, C + 4, z, WALL); g.set(x1, C + 4, z, WALL)
    g.box(x0 - 4, x0 - 1, C - 1, C + 7, z0 - 4, z0 - 1, WALL)
    g.set(x0 + 1, C, 80, LANTERN)
    g.mark("cloister-lane", 54, C, 90, "north")


def build(g):
    ward(g)
    stables(g)
    barracks(g)
    armory(g)
    keep_steps(g)
    lane(g)
