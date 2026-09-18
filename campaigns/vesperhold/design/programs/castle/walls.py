"""The curtain, its corner towers, the east rampart with its stair tower and
spur, the watch tower, and the buttress walk along the north edge."""
from . import layout as L
from .grid import room, crenels, flight, hsh, stairs, slab, pyramid, tower, AIR
from .palette import (WALL, WALL_RUIN, TRIM, QUOIN, FLAG, FLOOR, LANTERN,
                      DARK_PLANKS, PLANKS, COBWEB, POST, CANDLES, ROOF, BARS_X, BARS_Z)

C, W = L.CASTLE, L.WALK
SB = "minecraft:stone_brick_stairs"
CURTAIN_TOP = 35          # solid to here on the outer ring


def ring(g):
    """The outer curtain on the crag's edge, three thick, crenellated,
    ruined in places, with a string course and arrow slits."""
    x0, x1, z0, z1 = L.CRAG
    t = 3
    segs = [(x0, x1, z0, z0 + t - 1), (x0, x1, z1 - t + 1, z1),
            (x0, x0 + t - 1, z0, z1), (x1 - t + 1, x1, z0, z1)]
    for (a0, a1, b0, b1) in segs:
        g.box(a0, a1, C - 1, CURTAIN_TOP, b0, b1, WALL)
    # the barbican stands in the south curtain's place
    bx0, bx1, _, _ = L.P["barbican"].box
    g.clear(bx0 - 1, bx1 + 1, C - 1, CURTAIN_TOP + 1, z1 - t + 1, z1)
    # string course and plinth on the outer face
    for (a0, a1, b0, b1) in segs:
        for a in range(a0, a1 + 1):
            for b in range(b0, b1 + 1):
                if g.get(a, C + 1, b) != AIR:
                    g.set(a, C + 2, b, TRIM)
    # crenels on the outer edge, ruin on the tops
    for x in range(x0, x1 + 1):
        for z in (z0, z1):
            if (x - x0) % 2 == 0 and g.get(x, CURTAIN_TOP, z) != AIR:
                g.set(x, CURTAIN_TOP + 1, z, WALL)
    for z in range(z0, z1 + 1):
        for x in (x0, x1):
            if (z - z0) % 2 == 0:
                g.set(x, CURTAIN_TOP + 1, z, WALL)
    for (a0, a1, b0, b1) in segs:
        for a in range(a0, a1 + 1):
            for b in range(b0, b1 + 1):
                if hsh(a, b, 61) < .12 and b > 30:
                    h = 1 + int(4 * hsh(a, b, 62))
                    g.clear(a, a, CURTAIN_TOP + 2 - h, CURTAIN_TOP + 1, b, b)
    # arrow slits on the outer faces
    for x in range(x0 + 6, x1 - 5, 9):
        g.clear(x, x, C + 5, C + 7, z0, z0 + t - 1)
    for z in range(z0 + 6, z1 - 5, 9):
        g.clear(x0, x0 + t - 1, C + 5, C + 7, z, z)
        g.clear(x1 - t + 1, x1, C + 5, C + 7, z, z)
    # round-cornered bastions at the south-west and south-east corners
    for (bx, bz) in ((x0 - 2, z1 - 6), (x1 - 6, z1 - 6)):
        g.box(bx, bx + 8, C - 1, CURTAIN_TOP + 4, bz, bz + 8, WALL)
        crenels(g, bx, bx + 8, bz, bz + 8, CURTAIN_TOP + 5, WALL)
        g.box(bx + 1, bx + 7, CURTAIN_TOP + 4, CURTAIN_TOP + 4, bz + 1, bz + 7, FLAG)
        for q in (bx, bx + 8):
            g.box(q, q, L.VALLEY + 2, CURTAIN_TOP + 5, bz, bz, QUOIN)
        g.box(bx, bx + 8, L.VALLEY + 2, C - 2, bz, bz + 8, WALL)
    # mural towers standing proud of the curtain, and corbels under the parapet
    for (tx0, tx1, tz0, tz1) in ((114, 122, 165, 176), (140, 148, 165, 176),
                                 (5, 15, 64, 72), (5, 15, 98, 106),
                                 (48, 56, 0, 7), (116, 124, 0, 7),
                                 (162, 171, 56, 64), (162, 171, 96, 104)):
        tower(g, tx0, tx1, tz0, tz1, L.VALLEY + 1, CURTAIN_TOP + 4, WALL, ROOF, TRIM, quoin=QUOIN)
    corbel_s = stairs(SB, "north", "top")
    corbel_n = stairs(SB, "south", "top")
    corbel_w = stairs(SB, "east", "top")
    corbel_e = stairs(SB, "west", "top")
    for x in range(x0, x1 + 1):
        if g.get(x, CURTAIN_TOP, z1) != AIR and g.get(x, CURTAIN_TOP - 1, z1 + 1) == AIR:
            g.set(x, CURTAIN_TOP - 1, z1 + 1, corbel_s)
        if g.get(x, CURTAIN_TOP, z0) != AIR and g.get(x, CURTAIN_TOP - 1, z0 - 1) == AIR:
            g.set(x, CURTAIN_TOP - 1, z0 - 1, corbel_n)
    for z in range(z0, z1 + 1):
        if g.get(x0, CURTAIN_TOP, z) != AIR and g.get(x0 - 1, CURTAIN_TOP - 1, z) == AIR:
            g.set(x0 - 1, CURTAIN_TOP - 1, z, corbel_w)
    # the stables' back door through the west curtain
    g.clear(x0, x0 + t - 1, C, C + 2, 138, 140)
    g.box(x0, x0, C + 3, C + 3, 137, 141, TRIM)


def east_rampart(g):
    """A wall walk eight wide on the thickened east curtain."""
    p = L.P["east-rampart"]
    x0, x1, z0, z1 = p.box
    top = W - 1
    g.box(x0, L.CRAG[1], C - 1, top, z0, z1, WALL)
    g.box(x0, x1, top, top, z0, z1, FLAG)
    # inner parapet low and broken; the outer curtain rises above the walk
    for z in range(z0, z1 + 1):
        g.box(x0 - 1, x0 - 1, C - 1, W, z, z, WALL)
        g.set(x0 - 1, W + 1, z, WALL if z % 4 == 0 else BARS_Z)
    g.box(x1 + 1, L.CRAG[1], top, W + 1, z0, z1, WALL)
    for z in range(z0, z1 + 1, 2):
        g.set(L.CRAG[1], W + 2, z, WALL)
    # buttresses on the ward side every twelve cells, and lanterns
    for z in range(z0 + 4, z1, 12):
        g.box(x0 - 3, x0 - 2, C - 1, top + 1, z, z + 1, QUOIN)
        g.set(x1, W, z + 6, LANTERN)
    g.mark("east-rampart", 155, W, 70, "north")
    g.mark("rampart-archers", 155, W, 45, "south")
    g.mark("rampart-volley", 155, W, 90, "north")
    g.mark("rampart-volley-battery", 155, W, 60, "south")


def rampart_stair(g):
    p = L.P["rampart-stair"]
    x0, x1, z0, z1 = p.box
    top = C + p.height
    room(g, x0, x1, z0, z1, C, p.height, WALL, FLOOR, ceiling=WALL)
    # door from the ward in the west wall
    g.clear(x0 - 1, x0 - 1, C, C + 3, 126, 129)
    g.box(x0 - 1, x0 - 1, C + 4, C + 4, 125, 130, TRIM)
    # one flight up the south wall climbing east, landing, one up the east wall climbing north
    flight(g, "x", 132, 134, x0 + 1, 1, C, 6, SB, WALL)             # 24 -> 30, x126..131
    g.box(x0 + 1, x0 + 1, C, C + 1, 131, 131, WALL)                 # newel: taken from the west
    g.box(x0 + 7, x1, C + 5, C + 5, 131, 135, FLOOR)                # landing at 30
    g.box(x0 + 7, x1, C, C + 4, 131, 135, WALL)
    flight(g, "z", 138, 140, 130, -1, C + 6, 6, SB, WALL)           # 30 -> 36, z130..125
    g.box(x0, x1, W - 1, W - 1, z0, z0 + 4, FLOOR)                  # top gallery at 36 (z120..124)
    # the top: crenellated roof, a door east onto the spur
    g.box(x0 - 1, x1 + 1, top + 1, top + 1, z0 - 1, z1 + 1, WALL)
    crenels(g, x0 - 1, x1 + 1, z0 - 1, z1 + 1, top + 2, WALL)
    g.clear(x1 + 1, x1 + 1, W, W + 2, 121, 123)
    g.set(x0 + 1, C, z1 - 1, LANTERN)
    g.set(x1 - 1, W, z0, LANTERN)
    g.mark("rampart-stair", x0 + 3, C, 128, "east")
    # the spur: a short wall walk from the tower's top to the rampart
    g.box(x1 + 1, 151, C - 1, W - 1, 120, 125, WALL)
    g.box(x1 + 2, 151, W - 1, W - 1, 121, 123, FLAG)
    g.box(x1 + 2, 151, W, W, 120, 120, WALL)
    g.box(x1 + 2, 151, W, W, 124, 124, WALL)
    g.box(x1 + 2, 151, W + 1, W + 1, 120, 120, BARS_X)
    g.box(x1 + 2, 151, W + 1, W + 1, 124, 124, BARS_X)
    g.clear(x1 + 2, 151, W, W + 3, 121, 123)
    g.clear(151, 151, W, W + 3, 121, 123)


def watch_tower(g):
    p = L.P["watch-tower"]
    x0, x1, z0, z1 = p.box
    top = W + p.height
    # the tower rises from the crag; its lower storey is solid masonry
    g.box(x0 - 1, x1 + 1, C - 1, W - 1, z0 - 1, z1 + 1, WALL)
    room(g, x0, x1, z0, z1, W, p.height, WALL, FLOOR, ceiling=WALL)
    for q in ((x0 - 1, z0 - 1), (x1 + 1, z0 - 1), (x0 - 1, z1 + 1), (x1 + 1, z1 + 1)):
        g.box(q[0], q[0], C - 1, top + 3, q[1], q[1], QUOIN)
    g.box(x0 - 1, x1 + 1, top, top, z0 - 1, z1 + 1, WALL)
    crenels(g, x0 - 1, x1 + 1, z0 - 1, z1 + 1, top + 1, WALL)
    # a pointed cap over the roof
    pyramid(g, x0 + 1, x1 - 1, z0 + 1, z1 - 1, top + 1, ROOF, cap=QUOIN)
    # doors: south onto the rampart, west onto the buttress walk
    g.clear(154, 157, W, W + 2, z1 + 1, z1 + 1)
    g.clear(x0 - 1, x0 - 1, W, W + 2, 13, 14)
    # windows
    for z in (8, 15):
        g.clear(x1 + 1, x1 + 1, W + 2, W + 4, z, z)
    g.clear(155, 156, W + 2, W + 4, z0 - 1, z0 - 1)
    # Pellam's stall: a counter of planks and his wares
    g.box(x0 + 2, x0 + 7, W, W, 11, 11, DARK_PLANKS)
    g.set(x0 + 2, W + 1, 11, CANDLES)
    g.set(x1 - 1, W, z0, LANTERN)
    g.set(x0, W, z1, LANTERN)
    g.mark("watch-tower", 156, W, 17, "south")
    g.mark("watch-fire", 161, W, 6, "west")
    g.mark("pellam-stall", 153, W, 10, "south")
    g.mark("pellam-counter", 151, W, 13, "north")
    g.mark("halvard-tower", 159, W, 15, "west")


def buttress_walk(g):
    """A deck on an arcade of piers, along the north edge at wall-walk height."""
    p = L.P["buttress-walk"]
    x0, x1, z0, z1 = p.box
    top = W - 1
    g.clear(x0, x1, W, W + 3, z0 - 1, z1 + 1)       # tunnels through the keep's turrets
    g.box(x0, x1, top - 1, top, z0 - 1, z1 + 1, WALL)
    g.box(x0, x1, top, top, z0, z1, FLAG)
    for x in range(x0, x1 + 1):
        for z in (z0 - 1, z1 + 1):
            g.set(x, W, z, WALL)
            g.set(x, W + 1, z, WALL if x % 4 == 0 else BARS_X)
    # piers down to the crag with pointed arches between them
    for x in range(x0 + 3, x1, 10):
        g.box(x, x + 1, C - 1, top - 2, z0 - 1, z1 + 1, WALL)
        g.box(x - 1, x + 2, C - 1, C + 1, z0 - 2, z1 + 2, QUOIN)
        for k in range(1, 4):
            g.box(x - k, x - k, top - 2 - (3 - k), top - 2, z0 - 1, z1 + 1, WALL)
            g.box(x + 1 + k, x + 1 + k, top - 2 - (3 - k), top - 2, z0 - 1, z1 + 1, WALL)
    # lanterns and a few wreck spots
    for x in range(x0 + 8, x1, 16):
        g.set(x, W, z0, LANTERN)
    # a roofed arch over the walk below the keep: under it the parapet is no floor
    g.box(88, 92, W + 2, W + 2, z0 - 1, z0 - 1, WALL)
    g.box(88, 92, W + 2, W + 2, z1 + 1, z1 + 1, WALL)
    g.box(87, 93, W + 3, W + 3, z0 - 2, z1 + 2, WALL)
    g.mark("buttress-walk", 90, W, 13, "west")
    g.mark("wardens-door-key", 36, W, 13, "west")


def build(g):
    ring(g)
    east_rampart(g)
    rampart_stair(g)
    watch_tower(g)
