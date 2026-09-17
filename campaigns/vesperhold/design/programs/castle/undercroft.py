"""Under the rock: the Crypt of Wardens, the passage, and the Undertide Pool."""
from . import layout as L
from .grid import hsh, stairs, slab, block, AIR
from .palette import (ROCK, ROCK_MOSS, FLOOR, PILLAR, TRIM, CHAPEL, WATER, CANDLES,
                      SOUL_LANTERN, LANTERN, COBWEB, BARS_Z, CHAIN, GLASS_DARK)

U = L.UNDER
VAULT = None


def vaulted(g, x0, x1, z0, z1, height, wall, floor, bay=6):
    """A room cut into rock with a ribbed vault: the walls and the ceiling
    are masonry, the corners of each bay stepped in."""
    top = U + height
    g.box(x0 - 1, x1 + 1, U - 1, top, z0 - 1, z1 + 1, wall)
    g.box(x0, x1, U - 1, U - 1, z0, z1, floor)
    g.clear(x0, x1, U, top - 1, z0, z1)
    # ribs: every bay a transverse arch stepping down from the ceiling
    for x in range(x0 + bay - 1, x1, bay):
        g.box(x, x, top - 1, top - 1, z0, z1, wall)
        g.box(x, x, top - 2, top - 2, z0, z0 + 1, wall)
        g.box(x, x, top - 2, top - 2, z1 - 1, z1, wall)
        g.box(x, x, U, top - 3, z0, z0, PILLAR)
        g.box(x, x, U, top - 3, z1, z1, PILLAR)


def crypt(g):
    p = L.P["crypt-of-wardens"]
    x0, x1, z0, z1 = p.box
    stone = block("minecraft:polished_deepslate")
    vaulted(g, x0, x1, z0, z1, p.height, block("minecraft:deepslate_bricks"), FLOOR)
    # tombs in two rows, each lid carved with a bell
    for x in range(x0 + 2, x1 - 1, 6):
        for z in (z0 + 3, z1 - 5):
            g.box(x, x + 2, U, U, z, z + 2, stone)
            g.set(x + 1, U + 1, z + 1, block("minecraft:chiseled_deepslate"))
            if hsh(x, z, 151) < .5:
                g.set(x, U + 1, z, CANDLES)
    # the kneeling knight's dais at the far end
    g.box(x1 - 4, x1, U, U, 113, 118, stone)
    g.clear(x1 - 3, x1 - 1, U + 1, U + 3, 114, 117)
    # the way in (from the psalter stair, west), the way on (north, to the pool)
    g.clear(x0 - 1, x0 - 1, U, U + 2, 125, 127)
    g.clear(30, 33, U, U + 3, z0 - 1, z0 - 1)
    for (lx, lz) in ((x0, z0), (x1, z0), (x0, z1 - 3), (x1, z1), (x0 + 11, z0 + 11)):
        g.set(lx, U, lz, SOUL_LANTERN)
    g.set(x0 + 5, U + p.height - 2, z0 + 3, COBWEB)
    g.mark("crypt-of-wardens", 38, U, 122, "north")
    g.mark("warden-knight", x1 - 2, U + 1, 115, "west")
    g.mark("crypt-drop", 38, U, 110, "north")


def passage(g):
    g.box(29, 34, U - 1, U + 4, 92, 103, block("minecraft:deepslate_bricks"))
    g.clear(30, 33, U, U + 3, 92, 103)
    g.box(30, 33, U - 1, U - 1, 92, 103, FLOOR)
    g.set(30, U, 97, SOUL_LANTERN)


def pool(g):
    p = L.P["undertide-pool"]
    x0, x1, z0, z1 = p.box
    top = U + p.height
    # a rough cavern, its walls rock rather than masonry
    g.box(x0 - 2, x1 + 2, U - 3, top, z0 - 2, z1 + 2, ROCK)
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            h = p.height - (1 if hsh(x, z, 161) < .25 else 0) - (1 if hsh(x, z, 162) < .1 else 0)
            g.clear(x, x, U, U + h - 1, z, z)
            g.set(x, U - 1, z, ROCK_MOSS if hsh(x, z, 163) < .3 else FLOOR)
    # the well at the centre: a stone lip, grey water, three deep
    cx, cz = 36, 80
    for x in range(cx - 5, cx + 6):
        for z in range(cz - 5, cz + 6):
            d2 = (x - cx) ** 2 + (z - cz) ** 2
            if d2 <= 16:
                g.box(x, x, U - 4, U - 2, z, z, WATER)
                g.set(x, U - 1, z, WATER)
            elif d2 <= 26:
                g.set(x, U, z, slab("minecraft:polished_deepslate_slab"))
    g.box(cx - 5, cx + 5, U - 5, U - 5, cz - 5, cz + 5, ROCK)
    # choir stalls round the well, and the fallen tongue at its lip
    for (sx, sz) in ((cx - 8, cz), (cx + 8, cz), (cx, cz - 8), (cx, cz + 8)):
        g.set(sx, U, sz, stairs("minecraft:polished_deepslate_stairs", "south"))
    g.box(cx + 6, cx + 8, U, U, cz - 7, cz - 7, block("minecraft:iron_block"))
    g.set(cx + 6, U + 1, cz - 7, block("minecraft:iron_block"))
    # openings to the passage (south) and the well stair (west)
    g.clear(30, 33, U, U + 3, z1 + 1, z1 + 2)
    g.clear(x0 - 2, x0 - 1, U, U + 2, 76, 79)
    # barred windows through the crag's west face would be here if the pool
    # reached it; instead a light shaft from the garth drips in
    g.box(cx - 1, cx + 1, top, L.CASTLE - 2, cz - 1, cz + 1, AIR)
    g.box(cx - 1, cx + 1, L.CASTLE - 1, L.CASTLE - 1, cz - 1, cz + 1,
          block("minecraft:iron_trapdoor[facing=north,half=top,open=false,powered=false,waterlogged=false]"))
    for (lx, lz) in ((x0, z0), (x1, z0), (x0, z1), (x1, z1), (x0 + 4, 78), (x1 - 2, 70)):
        g.set(lx, U, lz, SOUL_LANTERN)
    g.mark("undertide-pool", 36, U, 90, "north")
    g.mark("drowned-choir", 36, U, 70, "south")
    g.mark("bell-tongue", 42, U, 74, "west")
    g.mark("undertide-well", 36, U, 80, "north", stand=False)


def build(g):
    crypt(g)
    passage(g)
    pool(g)
