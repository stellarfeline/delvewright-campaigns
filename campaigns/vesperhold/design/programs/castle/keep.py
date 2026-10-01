"""The keep: the great hall, the antechamber and the throne hall, under one
tall mass with corner turrets, buttresses and a broken roof."""
from . import layout as L
from .grid import room, crenels, gable, pyramid, rose, hsh, stairs, slab, block, flight, AIR
from .palette import (KEEP, WALL, TRIM, QUOIN, FLOOR, FLOOR_HALL, PILLAR, GLASS, GLASS_DARK,
                      ROOF, ROOF_RUIN, ROOF_MAT, DARK_PLANKS, PLANKS, LANTERN, LANTERN_HANG,
                      CANDLES, COBWEB, CHAIN, GATE_WOOD, TRIM_TUFF, BEAM, ROSE_GLASS, WALL_RUIN)

C, D = L.CASTLE, L.DAIS
KS = "minecraft:stone_brick_stairs"


def turret(g, x, z, base, top, r=2):
    """A round-ish corner turret: a square core with its corners cut, a
    crenellated head and a spire."""
    g.box(x - r, x + r, base, top, z - r, z + r, KEEP)
    for (cx, cz) in ((x - r, z - r), (x + r, z - r), (x - r, z + r), (x + r, z + r)):
        g.box(cx, cx, base + 2, top, cz, cz, AIR)
    g.box(x - r - 1, x + r + 1, top + 1, top + 1, z - r - 1, z + r + 1, KEEP)
    crenels(g, x - r - 1, x + r + 1, z - r - 1, z + r + 1, top + 2, KEEP)
    pyramid(g, x - r, x + r, z - r, z + r, top + 2, ROOF, cap=TRIM)
    for k in range(base + 4, top - 2, 6):
        g.set(x, k, z - r, GLASS_DARK); g.set(x, k, z + r, GLASS_DARK)


def great_hall(g):
    p = L.P["great-hall"]
    x0, x1, z0, z1 = p.box
    top = C + p.height
    room(g, x0, x1, z0, z1, C, p.height, KEEP, FLOOR_HALL, t=2)
    # a timber roof, fallen in over the middle
    g.box(x0 - 2, x1 + 2, top, top, z0 - 2, z1 + 2, KEEP)
    ridge = gable(g, x0 - 2, x1 + 2, z0 - 2, z1 + 2, top + 1, ROOF_MAT, KEEP, along="z", eaves=1)
    for x in range(x0 + 10, x1 - 12):
        for z in range(z0 + 6, z1 - 4):
            if (x - 70) ** 2 / 90 + (z - 76) ** 2 / 60 < 1 + hsh(x, z, 171) * .6:
                g.clear(x, x, top, ridge + 1, z, z)
    # tall windows down both long walls, buttresses between
    for z in range(z0 + 2, z1, 6):
        for (xw, xb) in ((x0 - 2, x0 - 4), (x1 + 2, x1 + 3)):
            g.box(xw, xw, C + 4, top - 4, z + 1, z + 2, GLASS)
            g.box(xw - (0 if xw == x0 - 2 else 0), xw, top - 3, top - 3, z + 1, z + 1, GLASS)
        g.box(x1 + 3, x1 + 4, C - 1, top - 2, z - 1, z, KEEP)
    # the south front: buttresses, lancets, and a great window over the Keep Doors
    for bx in (62, 72, 94, 104):
        g.box(bx, bx + 1, C - 1, top + 2, z1 + 3, z1 + 4, QUOIN if bx in (62, 104) else KEEP)
        g.box(bx, bx + 1, top + 3, top + 5, z1 + 3, z1 + 3, KEEP)
        pyramid(g, bx, bx + 1, z1 + 3, z1 + 4, top + 3, ROOF)
    for lx in (66, 68, 98, 100):
        g.box(lx, lx, C + 5, top - 3, z1 + 2, z1 + 2, GLASS)
        g.box(lx, lx, C + 5, top - 3, z1 + 1, z1 + 1, AIR)
    g.box(64, 102, top - 1, top - 1, z1 + 3, z1 + 3, stairs("minecraft:stone_brick_stairs", "north", "top"))
    rose(g, 83, top - 4, z1 + 2, 6, "x", TRIM, ROSE_GLASS, PILLAR)
    for dx in range(-5, 6):
        for dy in range(-5, 6):
            if dx * dx + dy * dy <= 26:
                g.set(83 + dx, top - 4 + dy, z1 + 1, AIR)
    g.box(81, 85, C, C + 4, z1 + 1, z1 + 1, AIR)
    g.box(81, 85, C - 1, C - 1, z1 + 1, z1 + 2, FLOOR)
    # the Keep Doors: sealed until the bell rings
    g.gate("keep-doors", 81, 85, C, C + 4, z1 + 2, z1 + 2, "minecraft:dark_oak_planks", GATE_WOOD)
    g.box(80, 86, C + 5, C + 5, z1 + 2, z1 + 2, TRIM)
    # hall furniture: long tables, a dais, banners gone to rags
    for xt in (66, 98):
        g.box(xt, xt + 2, C, C, z0 + 6, z1 - 6, DARK_PLANKS)
        for z in range(z0 + 7, z1 - 6, 4):
            g.set(xt + 1, C + 1, z, CANDLES) if hsh(xt, z, 172) < .4 else None
    for x in range(x0 + 4, x1 - 3, 8):
        g.box(x, x, C + 6, C + 10, z0 - 1, z0 - 1, block("minecraft:black_wool")) if hsh(x, 1, 173) < .6 else None
    # the stair up to the antechamber, north end, climbing north
    flight(g, "z", 81, 85, z0 + 4, -1, C, 4, KS, KEEP)
    g.box(81, 85, D - 1, D - 1, z0, z0, FLOOR)
    g.clear(81, 85, D, D + 3, z0 - 2, z0 - 1)           # through the hall's north wall
    g.box(81, 85, D - 1, D - 1, z0 - 2, z0 - 1, FLOOR)
    # the Almoner's Door in the west wall, recessed on the lane side and barred for good:
    # the keep doors reach the hall sooner from the gate, so it can shorten no walk
    g.clear(x0 - 2, x0 - 2, C, C + 1, 75, 76)
    g.box(x0 - 1, x0 - 1, C, C + 1, 75, 76, GATE_WOOD)
    # light
    for (lx, lz) in ((x0, z0 + 2), (x1, z0 + 2), (x0, z1), (x1, z1), (x0, 76), (x1, 76)):
        g.set(lx, C, lz, LANTERN)
    g.mark("great-hall", 83, C, 86, "north")
    g.mark("unremembered-guard", 83, C, 72, "south")
    g.mark("great-hall-west", x0 + 4, C, 80, "east")


def antechamber(g):
    p = L.P["antechamber"]
    x0, x1, z0, z1 = p.box
    top = D + p.height
    g.box(x0 - 2, x1 + 2, C, D - 2, z0 - 2, z1 + 2, KEEP)   # no hollow under the floor
    room(g, x0, x1, z0, z1, D, p.height, KEEP, FLOOR, ceiling=KEEP, t=2)
    g.clear(81, 85, D, D + 3, z1 + 1, z1 + 4)          # from the hall stair
    g.box(81, 85, D - 1, D - 1, z1 + 1, z1 + 4, FLOOR)
    g.clear(81, 85, D, D + 4, z0 - 3, z0 - 1)          # into the throne hall
    g.box(81, 85, D - 1, D - 1, z0 - 3, z0 - 1, FLOOR)
    g.box(80, 86, D + 5, D + 5, z0 - 3, z0 - 1, TRIM)
    # rotted hangings and the brazier's plinth
    for x in (x0, x1):
        g.box(x, x, D + 1, D + 4, z0 + 2, z0 + 5, block("minecraft:red_wool")) if x == x0 else \
            g.box(x, x, D + 1, D + 4, z0 + 5, z0 + 8, block("minecraft:red_wool"))
    g.set(x0 + 2, D, z0 + 2, CANDLES)
    g.set(x1 - 1, D, z1 - 1, LANTERN)
    g.mark("antechamber", 83, D, 53, "north")
    g.mark("throne-fire", 78, D, 50, "east")
    g.mark("halvard-doorway", 83, D, 48, "north")


def throne_hall(g):
    p = L.P["throne-hall"]
    x0, x1, z0, z1 = p.box
    top = D + p.height
    # the keep's tall mass rises from the crag round the throne hall
    g.box(x0 - 3, x1 + 3, C - 1, D - 1, z0 - 3, z1 + 2, KEEP)
    room(g, x0, x1, z0, z1, D, p.height, KEEP, FLOOR_HALL, ceiling=KEEP, t=3)
    # two rows of great piers, and the throne on its steps at the north end
    for z in range(z0 + 4, z1 - 2, 6):
        for x in (x0 + 8, x1 - 8):
            g.box(x, x + 1, D, top - 1, z, z + 1, PILLAR)
            g.box(x - 1, x + 2, top - 3, top - 1, z - 1, z + 2, KEEP)
    tx = 83
    for k in range(3):
        g.box(tx - 5 + k, tx + 5 - k, D + k, D + k, z0, z0 + 4 - k, block("minecraft:polished_blackstone_bricks"))
    g.box(tx - 1, tx + 1, D + 3, D + 7, z0, z0, block("minecraft:gilded_blackstone"))
    g.set(tx, D + 3, z0 + 1, stairs("minecraft:polished_blackstone_brick_stairs", "north"))
    # tall windows, and a broken great window in the north wall
    for z in range(z0 + 3, z1 - 1, 6):
        g.box(x0 - 3, x0 - 1, D + 5, top - 5, z, z + 1, GLASS)
        g.box(x1 + 1, x1 + 3, D + 5, top - 5, z, z + 1, GLASS)
    # banners behind the throne
    for x in (tx - 4, tx + 4):
        g.box(x, x, D + 4, D + 12, z0, z0, block("minecraft:black_wool"))
    # the keep's head: crenellations, a pitched roof, corner turrets, buttresses
    g.box(x0 - 3, x1 + 3, top, top + 2, z0 - 3, z1 + 3, KEEP)
    crenels(g, x0 - 3, x1 + 3, z0 - 3, z1 + 3, top + 3, KEEP)
    ridge = gable(g, x0 - 1, x1 + 1, z0 - 1, z1 + 1, top + 3, ROOF_MAT, KEEP, along="x", eaves=0)
    for x in range(x0 + 4, x0 + 16):
        for z in range(z0 + 6, z1 - 6):
            if hsh(x, z, 181) < .4:
                g.clear(x, x, top + 3, ridge, z, z)
    for (cx, cz) in ((x0 - 4, z0 - 4), (x1 + 4, z0 - 4), (x0 - 4, z1 + 4), (x1 + 4, z1 + 4)):
        turret(g, cx, cz, C - 1, top + 12)
    # a tall central tower over the throne, the keep's landmark
    cx0, cx1, cz0, cz1 = 77, 89, 26, 38
    g.box(cx0, cx1, ridge - 6, ridge + 10, cz0, cz1, KEEP)
    for x in range(cx0 + 2, cx1 - 1, 3):
        g.box(x, x, ridge - 2, ridge + 6, cz0, cz0, GLASS_DARK)
        g.box(x, x, ridge - 2, ridge + 6, cz1, cz1, GLASS_DARK)
    crenels(g, cx0 - 1, cx1 + 1, cz0 - 1, cz1 + 1, ridge + 11, KEEP)
    g.box(cx0 - 1, cx1 + 1, ridge + 10, ridge + 10, cz0 - 1, cz1 + 1, KEEP)
    pyramid(g, cx0 + 1, cx1 - 1, cz0 + 1, cz1 - 1, ridge + 11, ROOF, cap=TRIM)
    # flying buttresses on the east and west flanks
    for z in range(z0 + 2, z1, 8):
        for (xa, xd) in ((x0 - 4, -1), (x1 + 4, 1)):
            for k in range(6):
                g.box(xa + xd * k, xa + xd * k + (1 if xd > 0 else 0), C - 1, top - 2 - k, z, z + 1, KEEP) if k in (4, 5) else \
                    g.box(xa + xd * k, xa + xd * k, top - 2 - k, top - 1 - k, z, z + 1, KEEP)
    # light
    for (lx, lz) in ((x0, z1), (x1, z1), (x0, z0 + 8), (x1, z0 + 8), (x0 + 12, z1), (x1 - 12, z1)):
        g.set(lx, D, lz, LANTERN)
    g.mark("throne-hall", 83, D, 40, "north")
    g.mark("king-oswin", 83, D + 3, 22, "south")
    g.mark("throne-arena", 83, D, 32, "north")
    g.mark("tamsin-throne", 88, D, 38, "north")


def build(g):
    throne_hall(g)
    antechamber(g)
    great_hall(g)
