"""The castle's east side, off the road: the Chandlery yard behind the garden
gate, the passage under the rampart spur, and the Hedge Garden east of the
keep with its fountain plinth and its summerhouse."""
from . import layout as L
from .grid import hsh, stairs, slab, block, pyramid, tree, AIR
from .palette import (WALL, TRIM, QUOIN, FLAG, FLOOR, PILLAR, PLANKS, DARK_PLANKS, POST,
                      BEAM_Z, ROAD, TURF, LANTERN, LANTERN_HANG, CANDLES, CHAIN, ROOF,
                      COBWEB)

C = L.CASTLE
SB = "minecraft:stone_brick_stairs"
HEDGE = block("minecraft:azalea_leaves[distance=1,persistent=true,waterlogged=false]")
BED = block("minecraft:coarse_dirt")


def lamp_post(g, x, z):
    g.box(x, x, C, C + 1, z, z, POST)
    g.set(x, C + 2, z, LANTERN)


def chandlery(g):
    """A lean-to against the east curtain where the castle's dead are
    rendered into tallow: vats, a smoker, barrels of fat, candles drying."""
    _, x1, z0, z1 = L.P["chandlery-yard"].box
    x0, z0, z1 = x1 - 5, z0 + 1, z1 - 1          # the lean-to's floor, against the curtain
    g.box(x0, x1, C - 1, C - 1, z0, z1, DARK_PLANKS)
    for z in (z0, 135, 139, z1):
        g.box(x0 - 1, x0 - 1, C, C + 3, z, z, POST)
    # the lean-to: planks on beams, a slate edge on the yard side
    g.box(x0 - 1, x1, C + 4, C + 4, z0, z1, PLANKS)
    g.box(x0 - 2, x0 - 2, C + 4, C + 4, z0 - 1, z1 + 1, stairs("minecraft:deepslate_tile_stairs", "east"))
    g.box(x0 - 1, x0 - 1, C + 4, C + 4, z0 - 1, z1 + 1, BEAM_Z)
    # the rendering vats and the oven
    for z in (132, 134, 136):
        g.set(x1, C, z, block("minecraft:cauldron"))
    g.set(x1, C, 138, block("minecraft:smoker[facing=west,lit=false]"))
    # barrels of tallow with candles set to harden on them
    for z in (140, 141):
        g.set(x1, C, z, block("minecraft:barrel[facing=up,open=false]"))
        g.set(x1, C + 1, z, CANDLES)
    g.set(x1 - 1, C, 142, block("minecraft:barrel[facing=up,open=false]"))
    # a hoist over the vats
    g.box(162, 162, C + 2, C + 3, 134, 134, CHAIN)
    g.set(161, C + 3, 138, LANTERN_HANG)
    g.set(x0, C + 3, z0, COBWEB)


def east_yard(g):
    """The yard between the barracks and the rampart: the Chandler stands at
    his work in the middle of it."""
    # flagstones worn to earth round the chandlery, and a dead cart
    x0, x1, z0, z1 = L.P["chandlery-yard"].box
    for x in range(x0, x1 - 5):
        for z in range(z0, z1 + 1):
            if hsh(x, z, 201) < .35:
                g.set(x, C - 1, z, ROAD)
    g.box(146, 148, C, C, 141, 142, DARK_PLANKS)
    g.set(147, C + 1, 141, PLANKS)
    # the Chandler's block and trestle
    g.box(151, 152, C, C, 133, 133, DARK_PLANKS)
    g.set(154, C, 133, block("minecraft:cauldron"))
    lamp_post(g, 143, 131)
    lamp_post(g, 157, 143)
    lamp_post(g, 163, 152)
    lamp_post(g, 163, 162)
    g.mark("east-yard", 132, C, 140, "east")
    g.mark("chandlery-hands", 160, C, 140, "west")
    g.mark("chandler", 153, C, 135, "west")


def spur_passage(g):
    """A vaulted way through the rampart spur's footing, from the yard north
    into the Hedge Garden."""
    p = L.P["spur-passage"]
    x0, x1, z0, z1 = p.box
    g.clear(x0, x1, C, C + p.height - 1, z0, z1)
    g.box(x0, x1, C - 1, C - 1, z0, z1, FLAG)
    for z in (z0, z1):
        g.box(x0 - 1, x1 + 1, C + p.height, C + p.height, z, z, TRIM)
    g.set(x0 + 1, C + p.height - 1, (z0 + z1) // 2 - 1, LANTERN_HANG)
    g.mark("spur-passage", x0 + 1, C, (z0 + z1) // 2, "north")


def hedge_row(g, x0, x1, z0, z1):
    g.box(x0, x1, C, C + 1, z0, z1, HEDGE)


def parterre(g):
    """The south end of the garden: box hedges round dead beds, the dry
    fountain with the plinth the bowman stands on, and the hedge alcoves."""
    # the gravel walk from the passage to the fountain and on north
    g.box(144, 148, C - 1, C - 1, 92, 118, ROAD)
    g.box(128, 144, C - 1, C - 1, 106, 108, ROAD)
    # beds: coarse earth with dead growth, hedged on every side but one
    for (bx0, bx1, bz0, bz1) in ((126, 133, 110, 116), (136, 142, 110, 116),
                                 (125, 129, 92, 103), (139, 143, 92, 103)):
        g.box(bx0, bx1, C - 1, C - 1, bz0, bz1, BED)
        hedge_row(g, bx0, bx1, bz0, bz0)
        hedge_row(g, bx0, bx1, bz1, bz1)
        hedge_row(g, bx0, bx0, bz0, bz1)
        hedge_row(g, bx1, bx1, bz0, bz1)
        for x in range(bx0 + 1, bx1):
            for z in range(bz0 + 1, bz1):
                if hsh(x, z, 211) < .3:
                    g.set(x, C, z, block("minecraft:dead_bush"))
    # the alcoves: a hedge nook opening on the walk, a body's width deep
    for (ax, az, face) in ((143, 113, "east"), (149, 110, "west"), (143, 117, "east")):
        g.box(ax - 1, ax + 1, C, C + 2, az - 1, az + 1, HEDGE)
        g.clear(ax, ax, C, C + 1, az, az)
        opening = {"west": (ax - 1, az), "east": (ax + 1, az)}[face]
        g.clear(opening[0], opening[0], C, C + 1, opening[1], opening[1])
    g.mark("hedge-lurker-1", 143, C, 113, "east")
    g.mark("hedge-lurker-2", 149, C, 110, "west")
    g.mark("hedge-lurker-3", 143, C, 117, "east")
    # the dry fountain: a basin ring round a plinth four high, a ladder up
    # its north face — the bowman on it cannot come down, a body can go up
    cx, cz = L.FOUNTAIN
    for x in range(cx - 4, cx + 5):
        for z in range(cz - 4, cz + 5):
            d2 = (x - cx) ** 2 + (z - cz) ** 2
            if 9 < d2 <= 18:
                g.set(x, C, z, slab("minecraft:stone_brick_slab"))
            elif d2 <= 9:
                g.set(x, C - 1, z, FLOOR)
    g.box(cx - 1, cx + 1, C, C + 3, cz - 1, cz + 1, WALL)
    for (qx, qz) in ((cx - 1, cz - 1), (cx + 1, cz - 1), (cx - 1, cz + 1), (cx + 1, cz + 1)):
        g.box(qx, qx, C, C + 3, qz, qz, QUOIN)
    g.box(cx - 1, cx + 1, C + 3, C + 3, cz - 1, cz + 1, TRIM)
    g.box(cx, cx, C, C + 3, cz - 2, cz - 2, block("minecraft:ladder[facing=north,waterlogged=false]"))
    g.clear(cx - 1, cx + 1, C + 4, C + 6, cz - 1, cz + 1)
    g.mark("garden-plinth", cx, C + 4, cz, "south")
    g.mark("garden-plinth-foot", 139, C, 104, "north")
    lamp_post(g, 150, 118)
    lamp_post(g, 137, 105)


def summerhouse(g):
    """The garden's north end: an open pavilion under a slate cap, where the
    Hedge Knight keeps a watch nobody set him."""
    p = L.P["summerhouse"]
    x0, x1, z0, z1 = p.box
    g.box(x0, x1, C - 1, C - 1, z0, z1, FLOOR)
    for (px, pz) in ((x0, z0), (x1, z0), (x0, z1), (x1, z1)):
        g.box(px, px, C, C + p.height - 1, pz, pz, PILLAR)
    g.box(x0, x1, C + p.height, C + p.height, z0, z1, WALL)
    pyramid(g, x0, x1, z0, z1, C + p.height + 1, ROOF, cap=TRIM)
    # a stone bench on three sides, the south open to the garden
    g.box(x0 + 1, x1 - 1, C, C, z0, z0, stairs(SB, "north"))
    g.box(x0, x0, C, C, z0 + 1, z1 - 2, stairs(SB, "west"))
    g.box(x1, x1, C, C, z0 + 1, z1 - 2, stairs(SB, "east"))
    g.set(x0 + 1, C + 4, z0 + 1, LANTERN_HANG)
    g.set(x1 - 1, C + 4, z1 - 1, LANTERN_HANG)
    g.mark("hedge-knight", (x0 + x1) // 2, C, (z0 + z1) // 2 - 1, "south")


def orchard(g):
    """Between the parterre and the summerhouse: the gravel walk north
    through the dead orchard, where the gardeners still work."""
    g.box(128, 130, C - 1, C - 1, 34, 91, ROAD)
    g.box(130, 146, C - 1, C - 1, 89, 91, ROAD)
    g.box(130, 142, C - 1, C - 1, 34, 36, ROAD)
    for z in range(40, 90, 12):
        lamp_post(g, 131, z)
    # the orchard itself: old fruit trees in rows either side of the walk
    oak = (block("minecraft:oak_log[axis=y]"), block("minecraft:oak_wood[axis=y]"),
           block("minecraft:oak_leaves[distance=1,persistent=true,waterlogged=false]"))
    for tx in (114, 122, 137, 145):
        for tz in (46, 58, 70, 82):
            if (tx, tz) in ((114, 82), (137, 58)):
                continue                  # an older tree, or the gardeners, stand there
            tree(g, tx, tz, C, *oak, trunk=1, height=4, spread=3, seed=tx * 31 + tz)
    # lamps on the lawns either side of the rows
    for z in range(30, 92, 14):
        lamp_post(g, 112, z)
        lamp_post(g, 149, z + 6)
    lamp_post(g, 136, 37)
    g.mark("orchard", 129, C, 72, "north")
    g.mark("gardeners", 134, C, 58, "west")


def build(g):
    chandlery(g)
    east_yard(g)
    spur_passage(g)
    parterre(g)
    orchard(g)
    summerhouse(g)
