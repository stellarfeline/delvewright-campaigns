"""The way in: the wayside shrine, the pilgrim road, the causeway tower, the
hanging causeway and the barbican with its portcullis and its postern."""
from . import layout as L
from .grid import room, crenels, flight, pyramid, hsh, stairs, slab, block, machicolate, tower, AIR
from .palette import (WALL, WALL_RUIN, TRIM, QUOIN, ROAD, FLAG, FLOOR, ROCK,
                      LANTERN, CANDLES, BARS_X, BARS_Z, GATE_WOOD, DARK_PLANKS, POST,
                      PLANKS, COBWEB, CHAIN, ROOF)

C, V = L.CASTLE, L.VALLEY
SB = "minecraft:stone_brick_stairs"


def shrine(g):
    p = L.P["wayside-shrine"]
    x0, x1, z0, z1 = p.box
    g.box(x0, x1, V - 1, V - 1, z0, z1, FLAG)
    # a roofless ring of wall, broken, open to the north toward the road
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            edge = x in (x0, x1) or z in (z0, z1)
            if not edge:
                continue
            if z == z0 and 85 <= x <= 90:
                continue                       # the way out toward the road
            h = 2 + int(3 * hsh(x, z, 41))
            if x in (x0, x1) and z in (z0, z1):
                h = 6
            g.box(x, x, V, V + h, z, z, WALL)
            if h >= 4 and hsh(x, z, 42) < .5:
                g.set(x, V + h + 1, z, WALL_RUIN)
    # the niche on the south wall: a faceless statue over the fire
    g.box(85, 90, V, V + 5, z1 - 2, z1, WALL)
    g.clear(86, 89, V, V + 3, z1 - 1, z1 - 1)
    g.box(87, 88, V, V + 2, z1 - 1, z1 - 1, block("minecraft:polished_andesite"))
    g.box(87, 88, V + 3, V + 3, z1 - 1, z1 - 1, block("minecraft:andesite"))
    g.box(85, 90, V + 6, V + 6, z1 - 2, z1, stairs(SB, "south"))
    # benches and bedrolls
    g.box(x0 + 2, x0 + 2, V, V, z0 + 3, z0 + 7, stairs("minecraft:spruce_stairs", "east"))
    g.box(x1 - 2, x1 - 2, V, V, z0 + 3, z0 + 7, stairs("minecraft:spruce_stairs", "west"))
    g.set(x0 + 1, V, z0 + 1, LANTERN)
    g.set(x1 - 1, V, z0 + 1, LANTERN)
    g.set(x0 + 1, V, z1 - 1, CANDLES)
    g.mark("wayside-shrine", 87, V, z0 + 6, "north", role="entry")
    g.mark("causeway-fire", 87, V, z1 - 4, "north")
    g.mark("tamsin-fire", 90, V, z1 - 5, "north")
    g.mark("pilgrim-road", 87, V, 256, "north")


def road(g):
    p = L.P["pilgrim-road"]
    x0, x1, z0, z1 = p.box
    g.box(x0, x1, V - 1, V - 1, z0, z1, ROAD)
    g.box(x0 + 2, x1 - 2, V - 1, V - 1, z0, z1, FLAG)
    # way-stones every twelve cells
    for z in range(z0 + 4, z1, 12):
        g.box(x0 - 2, x0 - 2, V, V + 1, z, z, WALL)
        g.set(x0 - 2, V + 2, z, LANTERN)
        g.box(x1 + 2, x1 + 2, V, V + 1, z + 6, z + 6, WALL)


def causeway_stair(g):
    """An open flight climbing sixteen courses from the road to the deck, on a
    solid ramp with blind arches in its flanks and stepped parapets."""
    p = L.P["causeway-stair"]
    x0, x1, z0, z1 = p.box
    for k in range(16):
        z = z1 - k                       # 235 .. 220
        y = V + k                        # tread course
        g.box(x0 - 1, x1 + 1, V - 1, y - 1, z, z, WALL)
        g.box(x0 + 1, x1 - 1, y, y, z, z, stairs(SB, "north"))
        g.clear(x0 + 1, x1 - 1, y + 1, y + 4, z, z)
        # parapets that step with the flight
        g.box(x0 - 1, x0, y, y + 1, z, z, WALL)
        g.box(x1, x1 + 1, y, y + 1, z, z, WALL)
        if k % 4 == 0:
            g.set(x0 - 1, y + 2, z, TRIM); g.set(x1 + 1, y + 2, z, TRIM)
    # blind arches in the ramp's flanks
    for zc in range(z0 + 2, z1 - 3, 5):
        depth = z1 - zc
        top = V + min(depth, 15) - 3
        if top > V + 2:
            for x in (x0 - 1, x1 + 1):
                g.clear(x, x, V, top - 1, zc, zc + 2)
                g.box(x, x, top, top, zc + 1, zc + 1, TRIM)
    # the foot: two newel posts with lanterns
    for x in (x0 - 1, x1 + 1):
        g.box(x, x, V, V + 2, z1 + 1, z1 + 1, QUOIN)
        g.set(x, V + 3, z1 + 1, LANTERN)
    g.mark("causeway-stair", 87, V, z1 + 2, "north")
    g.mark("causeway-stair-top", 87, C, 218, "north")


def causeway(g):
    p = L.P["hanging-causeway"]
    x0, x1, z0, z1 = p.box
    g.box(x0 - 1, x1 + 1, C - 2, C - 1, z0, z1, WALL)
    g.box(x0, x1, C - 1, C - 1, z0, z1, FLAG)
    # parapets, broken in places
    for z in range(z0, z1 + 1):
        for x in (x0 - 1, x1 + 1):
            g.set(x, C, z, WALL)
            g.set(x, C + 1, z, WALL if (z - z0) % 2 == 0 else BARS_Z)
    # piers every eight cells, with arches between
    for z in range(z0 + 2, z1 - 1, 8):
        g.box(x0 - 1, x1 + 1, L.VALLEY - 1, C - 3, z, z + 2, WALL)
        g.box(x0 - 2, x1 + 2, L.VALLEY - 1, L.VALLEY + 1, z - 1, z + 3, QUOIN)
    for z in range(z0, z1 + 1):
        k = (z - z0 - 2) % 8
        if k in (3, 7):
            g.box(x0 - 1, x1 + 1, C - 4, C - 3, z, z, WALL)
        elif k in (4, 5, 6):
            g.box(x0 - 1, x1 + 1, C - 3, C - 3, z, z, WALL)
    # lanterns on the parapet
    for z in range(z0 + 6, z1, 12):
        g.set(x0 - 1, C + 1, z, LANTERN)
        g.set(x1 + 1, C + 1, z + 6, LANTERN)
    g.mark("hanging-causeway", 87, C, 190, "north")


def barbican(g):
    p = L.P["barbican"]
    x0, x1, z0, z1 = p.box
    top = C + p.height
    room(g, x0, x1, z0, z1, C, p.height, WALL, FLOOR, ceiling=WALL)
    # the two gate towers, proud of the south face, the gate passage between
    for (tx0, tx1) in ((76, 82), (93, 99)):
        tower(g, tx0, tx1, 164, 177, V + 1, top + 10, WALL, ROOF, TRIM, quoin=QUOIN)
    # the west tower is hollow at the gate level: a guard room with the postern
    g.clear(77, 81, C, C + 3, 165, 175)
    g.box(77, 81, C - 1, C - 1, 165, 175, FLOOR)
    g.clear(78, 80, C, C + 2, 164, 164)                 # into the gate hall
    g.gate("postern", 76, 76, C, C + 1, 173, 173, "minecraft:dark_oak_planks", GATE_WOOD)
    g.box(76, 76, C + 2, C + 2, 172, 174, TRIM)
    # the passage: roofed, open to the causeway at its south end, a gable over it
    g.box(83, 92, V + 2, top + 6, 172, 177, WALL)
    g.clear(86, 89, C, C + 5, 172, 177)
    g.box(86, 89, C - 1, C - 1, 172, 177, FLOOR)
    for (xx, yy) in ((85, C + 5), (90, C + 5), (86, C + 6), (89, C + 6)):
        g.set(xx, yy, 177, AIR)
    g.box(86, 89, C + 7, C + 7, 177, 177, TRIM)
    g.box(84, 91, C + 9, C + 11, 177, 177, TRIM)
    machicolate(g, 83, 92, 172, 177, top + 7, WALL, "minecraft:stone_brick_stairs", sides="s")
    # the hall's roof walk
    machicolate(g, x0, x1, z0, z1, top + 1, WALL, "minecraft:stone_brick_stairs", sides="nwe")
    # the portcullis in the north wall: sealed, a shortcut opened from the ward
    g.gate("portcullis", 86, 90, C, C + 4, z0 - 1, z0 - 1, "minecraft:iron_bars", BARS_X)
    g.box(85, 91, C + 5, C + 5, z0 - 1, z0 - 1, TRIM)
    g.set(86, top - 1, z0, CHAIN); g.set(90, top - 1, z0, CHAIN)
    # wreckage inside: carts, chains, a rack
    g.box(x0 + 2, x0 + 4, C, C, z0 + 2, z0 + 3, DARK_PLANKS)
    g.box(x1 - 3, x1 - 2, C, C + 1, z0 + 8, z0 + 9, PLANKS)
    g.set(x0 + 1, C + p.height - 1, z0 + 1, COBWEB)
    g.set(x1 - 1, C + p.height - 1, z1 - 1, COBWEB)
    g.set(x0 + 1, C, z1 - 1, LANTERN); g.set(x1 - 1, C, z0 + 1, LANTERN)
    g.mark("barbican", 87, C, 162, "south")
    g.mark("porter", 87, C, 158, "south")
    g.mark("postern-key", 79, C, 169, "west")
    g.mark("postern-ledge", 60, C, 174, "west")
    g.mark("hanging-causeway-gate", 87, C, 177, "north")


def build(g):
    shrine(g)
    road(g)
    causeway_stair(g)
    causeway(g)
    barbican(g)
