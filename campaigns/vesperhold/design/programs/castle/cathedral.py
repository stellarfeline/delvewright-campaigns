"""The cathedral quarter: the cloister and its well-house, the Chapel of Hours,
the scriptorium with the Psalter Wall, and the annex the wall hides."""
from . import layout as L
from .grid import room, crenels, gable, pyramid, rose, lancet, hsh, stairs, slab, block, AIR
from .palette import (WALL, TRIM, TRIM_TUFF, QUOIN, FLAG, FLOOR, FLOOR_HALL, LANTERN,
                      LANTERN_HANG, CHAPEL, PILLAR, GLASS, GLASS_DARK, ROSE_GLASS, TURF,
                      ROOF, ROOF_MAT, DARK_PLANKS, PLANKS, BOOKS, CANDLES, COBWEB, POST,
                      GATE_WOOD, PSALTER, ROCK_MOSS, BEAM, CHAIN)

C = L.CASTLE
TS = "minecraft:tuff_brick_stairs"


def cloister(g):
    p = L.P["cloister-garth"]
    x0, x1, z0, z1 = p.box
    # the outer walls: north shared with the chapel, south with the scriptorium
    g.box(x0 - 4, x1 + 4, C - 1, C + 6, z0 - 4, z1 + 4, CHAPEL)
    g.clear(x0, x1, C, C + 6, z0, z1)
    g.box(x0, x1, C - 1, C - 1, z0, z1, FLOOR)
    # the garth: lawn inside an arcade four wide
    gx0, gx1, gz0, gz1 = x0 + 5, x1 - 5, z0 + 5, z1 - 5
    g.box(gx0, gx1, C - 1, C - 1, gz0, gz1, TURF)
    for x in range(gx0 - 1, gx1 + 2):
        for z in (gz0 - 1, gz1 + 1):
            g.box(x, x, C, C + 3, z, z, PILLAR if (x - gx0) % 3 == 2 else AIR)
            g.set(x, C, z, PILLAR if (x - gx0) % 3 == 2 else slab("minecraft:tuff_brick_slab"))
    for z in range(gz0 - 1, gz1 + 2):
        for x in (gx0 - 1, gx1 + 1):
            g.box(x, x, C, C + 3, z, z, PILLAR if (z - gz0) % 3 == 2 else AIR)
            g.set(x, C, z, PILLAR if (z - gz0) % 3 == 2 else slab("minecraft:tuff_brick_slab"))
    # arcade lintel and its lean-to roof
    for x in range(gx0 - 1, gx1 + 2):
        for z in (gz0 - 1, gz1 + 1):
            g.box(x, x, C + 4, C + 4, z, z, TRIM_TUFF)
    for z in range(gz0 - 1, gz1 + 2):
        for x in (gx0 - 1, gx1 + 1):
            g.box(x, x, C + 4, C + 4, z, z, TRIM_TUFF)
    g.box(x0, x1, C + 5, C + 5, z0, z1, PLANKS)
    g.clear(gx0, gx1, C + 5, C + 5, gz0, gz1)
    for k in range(4):
        y = C + 6 + k
        g.box(x0 + k, x1 - k, y, y, z0 + k, z0 + k, stairs(ROOF_MAT, "south"))
        g.box(x0 + k, x1 - k, y, y, z1 - k, z1 - k, stairs(ROOF_MAT, "north"))
        g.box(x0 + k, x0 + k, y, y, z0 + k + 1, z1 - k - 1, stairs(ROOF_MAT, "east"))
        g.box(x1 - k, x1 - k, y, y, z0 + k + 1, z1 - k - 1, stairs(ROOF_MAT, "west"))
        g.box(x0 - 4, x1 + 4, y, y, z0 - 4, z0 - 1 - 0, CHAPEL) if k == 0 else None
    # the gnarled tree in the garth
    tx, tz = 34, 78
    g.box(tx, tx, C, C + 4, tz, tz, block("minecraft:dark_oak_log[axis=y]"))
    for dx in range(-2, 3):
        for dz in range(-2, 3):
            if abs(dx) + abs(dz) <= 3 and hsh(dx, dz, 121) < .8:
                g.set(tx + dx, C + 5, tz + dz, block("minecraft:dark_oak_leaves[distance=1,persistent=true,waterlogged=false]"))
    # doors: east to the lane, north to the chapel, south to the scriptorium
    g.clear(x1 + 1, x1 + 4, C, C + 3, 74, 76)
    g.box(x1 + 1, x1 + 4, C - 1, C - 1, 74, 76, FLOOR)
    g.clear(30, 32, C, C + 3, z0 - 4, z0 - 1)
    g.box(30, 32, C - 1, C - 1, z0 - 4, z0 - 1, FLOOR)
    g.clear(22, 24, C, C + 2, z1 + 1, z1 + 4)
    g.box(22, 24, C - 1, C - 1, z1 + 1, z1 + 4, FLOOR)
    # the Cloister Fire's corner, and light
    g.set(x1, C, z1, CANDLES)
    for (lx, lz) in ((x0 + 1, z1 - 1), (x1 - 1, z0 + 1), (x1 - 1, z1 - 1), (x0 + 12, z0 + 1)):
        g.set(lx, C, lz, LANTERN)
    g.mark("cloister-garth", 34, C, 70, "south")
    g.mark("cloister-fire", 44, C, 88, "west")
    g.mark("halvard-cloister", 46, C, 76, "west")
    g.mark("tamsin-cloister", 44, C, 62, "south")
    g.mark("chapel-door", 31, C, 61, "north")


def well_house(g):
    p = L.P["well-house"]
    x0, x1, z0, z1 = p.box
    room(g, x0, x1, z0, z1, C, p.height, CHAPEL, FLOOR, ceiling=PLANKS)
    gable(g, x0 - 1, x1 + 1, z0 - 1, z1 + 1, C + p.height + 1, ROOF_MAT, ROOF, along="z")
    # the stair shaft down to the pool passage
    s = L.P["well-stair"]
    g.clear(18, 20, C - 1, C - 1, 64, 69)
    for k in range(12):
        z = 64 + k
        y = C - 2 - k
        g.box(18, 20, y - 6, y - 1, z, z, block("minecraft:stone"))
        g.box(18, 20, y, y, z, z, stairs("minecraft:cobblestone_stairs", "north"))
        g.clear(18, 20, y + 1, y + 3, z, z)
    g.clear(18, 20, L.UNDER, L.UNDER + 3, 76, 79)
    g.box(18, 20, L.UNDER - 1, L.UNDER - 1, 76, 79, FLOOR)
    g.clear(21, 23, L.UNDER, L.UNDER + 2, 76, 79)
    g.box(21, 23, L.UNDER - 1, L.UNDER - 1, 76, 79, FLOOR)
    # the shortcut door onto the garth, and the lever side inside
    g.gate("well-house-door", x1 + 1, x1 + 1, C, C + 1, 65, 66, "minecraft:dark_oak_planks", GATE_WOOD)
    g.set(x0 + 5, C, z0, LANTERN)
    g.set(19, L.UNDER, 78, LANTERN)
    g.mark("well-house", 23, C, 66, "east")
    g.mark("unlock-well-house-door", 24, C, 67, "east")
    g.mark("well-stair", 19, L.UNDER, 77, "north")


def chapel(g):
    p = L.P["chapel-of-hours"]
    x0, x1, z0, z1 = p.box
    top = C + p.height
    room(g, x0, x1, z0, z1, C, p.height, CHAPEL, FLOOR_HALL)
    # the west front stands on the curtain line and is taller than the nave
    g.box(x0 - 4, x0 - 1, C - 1, top + 12, z0 - 2, z1 + 2, CHAPEL)
    for z in (z0 - 2, z1 + 2):
        g.box(x0 - 4, x0 - 1, C - 1, top + 16, z, z, QUOIN)
    # twin spirelets on the west front
    for (sz0, sz1) in ((z0 - 3, z0), (z1, z1 + 3)):
        g.box(x0 - 4, x0 - 1, top + 12, top + 18, sz0, sz1, CHAPEL)
        pyramid(g, x0 - 4, x0 - 1, sz0, sz1, top + 19, ROOF, cap=TRIM)
    # the gable of the west front, stepped
    for k in range(0, 12):
        lo, hi = z0 + k, z1 - k
        if lo > hi:
            break
        g.box(x0 - 4, x0 - 1, top + 12 + k, top + 12 + k, lo, hi, CHAPEL)
    # the rose window in the west front, seen from the valley
    cz, cy = (z0 + z1) // 2, top - 5
    rose(g, cz, cy, x0 - 4, 6, "z", TRIM_TUFF, ROSE_GLASS, PILLAR)
    g.clear(x0 - 3, x0 - 1, cy - 5, cy + 5, cz - 5, cz + 5)
    for dz in range(-5, 6):
        for dy in range(-5, 6):
            if dz * dz + dy * dy <= 30:
                g.set(x0 - 3, cy + dy, cz + dz, AIR)
                g.set(x0 - 2, cy + dy, cz + dz, AIR)
                g.set(x0 - 1, cy + dy, cz + dz, AIR)
    # lancets under the rose, and the west door (sealed by the curtain: blind arcade)
    for dz in (-6, -3, 3, 6):
        g.box(x0 - 4, x0 - 4, C + 2, C + 8, cz + dz, cz + dz, GLASS_DARK)
    # buttresses along both long sides, with flying arches to the clerestory
    for x in range(x0 + 3, x1, 6):
        for (zb, zs) in ((z0 - 2, -1), (z1 + 2, 1)):
            zz0, zz1 = (zb - 2, zb) if zs < 0 else (zb, zb + 2)
            g.box(x, x + 1, C - 1, top - 4, zz0, zz1, CHAPEL)
            for k in range(3):
                g.box(x, x + 1, top - 4 + k, top - 4 + k, zz0 + (k if zs < 0 else 0), zz1 - (0 if zs < 0 else k), CHAPEL)
            pyramid(g, x, x + 1, zz0 + (1 if zs < 0 else 0), zz0 + (1 if zs < 0 else 0), top - 1, TRIM_TUFF)
    # tall lancet windows between the buttresses
    for x in range(x0 + 1, x1 - 1, 6):
        for zw in (z0 - 1, z1 + 1):
            g.box(x + 1, x + 2, C + 4, top - 5, zw, zw, GLASS)
            g.box(x + 1, x + 1, top - 4, top - 4, zw, zw, GLASS)
            g.set(x + 3, top - 4, zw, CHAPEL)
    # the nave: two rows of piers, the altar at the east end
    for x in range(x0 + 3, x1 - 4, 6):
        for zp in (z0 + 5, z1 - 5):
            g.box(x, x + 1, C, top - 1, zp, zp + (1 if zp < z1 - 5 else -1) * 0, PILLAR)
    g.box(x1 - 3, x1, C, C, z0 + 8, z1 - 8, block("minecraft:polished_tuff"))
    g.box(x1 - 2, x1 - 1, C + 1, C + 1, z0 + 10, z1 - 10, block("minecraft:polished_tuff"))
    g.set(x1, C + 2, (z0 + z1) // 2 + 3, block("minecraft:iron_chain[axis=x,waterlogged=false]"))
    for z in (z0 + 9, z1 - 9):
        g.set(x1 - 3, C + 1, z, CANDLES)
    # broken pews
    pew = stairs("minecraft:dark_oak_stairs", "east")
    for x in range(x0 + 6, x1 - 8, 3):
        for z in list(range(z0 + 8, z0 + 11)) + list(range(z1 - 10, z1 - 7)):
            if hsh(x, z, 131) < .75:
                g.set(x, C, z, pew)
    # the east window over the altar
    g.box(x1 + 1, x1 + 1, C + 5, top - 4, (z0 + z1) // 2 - 2, (z0 + z1) // 2 + 2, GLASS)
    g.clear(x1 + 1, x1 + 1, top - 3, top - 3, (z0 + z1) // 2 - 1, (z0 + z1) // 2 + 1)
    g.box(x1 + 1, x1 + 1, top - 3, top - 3, (z0 + z1) // 2 - 1, (z0 + z1) // 2 + 1, GLASS)
    # the steep roof, holed over the nave
    g.box(x0 - 1, x1 + 1, top, top, z0 - 1, z1 + 1, CHAPEL)
    ridge = gable(g, x0 - 1, x1 + 2, z0 - 1, z1 + 1, top + 1, ROOF_MAT, CHAPEL, along="x")
    for x in range(x0 + 8, x0 + 20):
        for z in range(z0 + 2, z1 - 1):
            if hsh(x, z, 141) < .35:
                g.clear(x, x, top, ridge, z, z)
    # a slender fleche on the crossing
    fx = x0 + 22
    g.box(fx, fx + 3, ridge - 2, ridge + 5, (z0 + z1) // 2 - 1, (z0 + z1) // 2 + 2, CHAPEL)
    g.clear(fx + 1, fx + 2, ridge + 1, ridge + 4, (z0 + z1) // 2 - 1, (z0 + z1) // 2 + 2)
    pyramid(g, fx, fx + 3, (z0 + z1) // 2 - 1, (z0 + z1) // 2 + 2, ridge + 6, ROOF, cap=TRIM)
    # light
    for (lx, lz) in ((x0 + 1, z0), (x0 + 1, z1), (x1 - 5, z0), (x1 - 5, z1), (x0 + 14, z0), (x0 + 14, z1)):
        g.set(lx, C, lz, LANTERN)
    g.mark("chapel-of-hours", 30, C, 44, "west")
    g.mark("chapel-shard", x1 - 4, C, 44, "west")
    g.mark("echo-hesk", x1 - 5, C, 42, "west")
    g.mark("echo-court-1", 30, C, 41, "east")
    g.mark("echo-court-2", 30, C, 47, "east")
    g.mark("echo-court-3", 36, C, 41, "east")
    g.mark("echo-court-4", 36, C, 47, "east")
    g.mark("echo-apprentice-chapel", x1 - 6, C, 46, "west")
    g.mark("wardens-key-hook", x1 - 4, C, 38, "east")


def scriptorium(g):
    p = L.P["scriptorium"]
    x0, x1, z0, z1 = p.box
    top = C + p.height
    room(g, x0, x1, z0, z1, C, p.height, CHAPEL, FLOOR, ceiling=PLANKS)
    g.clear(22, 24, C, C + 2, z0 - 1, z0 - 1)             # the door from the cloister
    g.box(22, 24, C - 1, C - 1, z0 - 1, z0 - 1, FLOOR)
    gable(g, x0 - 1, x1 + 1, z0 - 1, z1 + 1, top + 1, ROOF_MAT, CHAPEL, along="z")
    # shelves on the walls, desks in the middle, the lectern
    for x in range(x0, x1 + 1):
        if x not in (22, 23, 24):
            g.box(x, x, C, C + 2, z0, z0, BOOKS)
    for z in range(z0 + 2, z1 - 1):
        g.box(x1, x1, C, C + 2, z, z, BOOKS)
    for (dx, dz) in ((x0 + 3, z0 + 5), (x0 + 3, z0 + 10), (x0 + 9, z0 + 5), (x0 + 9, z0 + 10)):
        g.box(dx, dx + 1, C, C, dz, dz, DARK_PLANKS)
        g.set(dx, C + 1, dz, CANDLES)
    g.set(x0 + 7, C, z0 + 8, block("minecraft:polished_andesite"))
    # windows onto the cliff
    for z in (z0 + 4, z0 + 11):
        g.box(x1 + 1, x1 + 1, C + 2, C + 5, z, z, GLASS)
    # the Psalter Wall: shelves across the south wall, cracked; the middle is a gate
    g.box(x0, x1, C, C + 3, z1 + 1, z1 + 1, CHAPEL)
    g.box(x0 + 1, x0 + 7, C, C + 2, z1, z1, BOOKS)
    g.clear(17, 19, C, C + 2, z1, z1)
    g.gate("psalter-wall", 17, 19, C, C + 2, z1 + 1, z1 + 1, "minecraft:bookshelf", PSALTER)
    g.box(16, 20, C + 3, C + 3, z1 + 1, z1 + 1, block("minecraft:cracked_stone_bricks"))
    g.set(x1 - 1, C, z1 - 1, LANTERN)
    g.set(x1 - 1, C, z0 + 1, LANTERN)
    g.mark("scriptorium", 24, C, 104, "north")
    g.mark("wardens-ledger", 23, C, 102, "south")
    g.mark("psalter-face", 18, C, 110, "south")


def psalter_annex(g):
    """Behind the Psalter Wall: a closed stone annex, and the stair cut down
    through the rock to the crypt."""
    g.box(15, 21, C - 1, C + 5, 113, 119, CHAPEL)
    g.box(15, 21, C + 6, C + 6, 113, 119, block("minecraft:polished_tuff"))
    g.clear(17, 19, C, C + 3, 113, 118)
    # the flight: from the wall's foot down to the undercroft
    for k in range(12):
        z = 113 + k
        y = C - 2 - k
        g.box(16, 20, y - 3, y + 4, z, z, block("minecraft:stone")) if k > 3 else None
        g.box(17, 19, y, y, z, z, stairs("minecraft:cobblestone_stairs", "north"))
        g.clear(17, 19, y + 1, y + 3, z, z)
    # landing and the way east into the crypt
    g.clear(17, 19, L.UNDER, L.UNDER + 3, 125, 127)
    g.box(17, 19, L.UNDER - 1, L.UNDER - 1, 125, 127, FLOOR)
    g.clear(20, 25, L.UNDER, L.UNDER + 2, 125, 127)
    g.box(20, 25, L.UNDER - 1, L.UNDER - 1, 125, 127, FLOOR)
    g.set(19, L.UNDER, 127, CANDLES)
    g.set(19, C, 117, LANTERN)
    g.mark("psalter-stair", 18, L.UNDER, 126, "east")


def build(g):
    chapel(g)
    cloister(g)
    well_house(g)
    scriptorium(g)
    psalter_annex(g)
