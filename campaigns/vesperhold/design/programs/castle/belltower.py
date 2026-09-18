"""The bell tower on the north-west corner: the stair hall behind the
Warden's Door, the open belfry, and the spire over it."""
from . import layout as L
from .grid import room, crenels, pyramid, hsh, stairs, slab, block, flight, AIR
from .palette import (WALL, KEEP, CHAPEL, TRIM, TRIM_TUFF, QUOIN, FLOOR, PILLAR, ROOF,
                      LANTERN, CANDLES, CHAIN, GATE_WOOD, COBWEB, GLASS_DARK, DARK_PLANKS, BEAM)

C, W, B = L.CASTLE, L.WALK, L.BELL
SB = "minecraft:stone_brick_stairs"


def build(g):
    p = L.P["bell-tower-stair"]
    x0, x1, z0, z1 = p.box          # 16..31, 8..23
    # the shaft from the crag to the belfry: solid below the stair hall
    g.box(x0 - 2, x1 + 2, C - 1, W - 1, z0 - 2, z1 + 2, CHAPEL)
    room(g, x0, x1, z0, z1, W, p.height, CHAPEL, FLOOR, ceiling=FLOOR, t=2)
    top = W + p.height                 # 51, the belfry's floor course
    # quoins and a string course at every stage
    for (qx, qz) in ((x0 - 2, z0 - 2), (x1 + 2, z0 - 2), (x0 - 2, z1 + 2), (x1 + 2, z1 + 2)):
        g.box(qx, qx, C - 1, B + 12, qz, qz, QUOIN)
    for y in (C + 2, W - 1, top):
        g.box(x0 - 2, x1 + 2, y, y, z0 - 2, z1 + 2, TRIM_TUFF)
    # the stair: round the walls, four flights of four; the last one climbs
    # over the Warden's Door and through the belfry deck
    flight(g, "x", z1 - 2, z1, x1 - 3, -1, W, 4, SB, CHAPEL)          # south side, west, 36->40
    g.box(x1 - 3, x1 - 3, W, W + 1, z1 - 3, z1 - 3, CHAPEL)            # newel: the flight is taken from the east
    g.box(x0, x1 - 7, W + 3, W + 3, z1 - 2, z1, FLOOR)
    g.box(x0, x1 - 7, W, W + 2, z1 - 2, z1, CHAPEL)
    flight(g, "z", x0, x0 + 2, z1 - 3, -1, W + 4, 4, SB, CHAPEL)      # west side, north, 40->44
    g.box(x0, x0 + 2, W + 7, W + 7, z0, z0 + 8, FLOOR)
    g.box(x0, x0 + 2, W, W + 6, z0, z0 + 8, CHAPEL)
    flight(g, "x", z0, z0 + 2, x0 + 3, 1, W + 8, 4, SB, CHAPEL)       # north side, east, 44->48
    g.box(x0 + 7, x1, W + 11, W + 11, z0, z0 + 2, FLOOR)
    g.box(x0 + 7, x1, W, W + 10, z0, z0 + 2, CHAPEL)
    flight(g, "z", x1 - 2, x1, z0 + 3, 1, W + 12, 4, SB, CHAPEL)      # east side, south, 48->52
    # the Warden's Door in the east wall, onto the buttress walk
    g.clear(x1 + 1, x1 + 2, W, W + 1, 13, 14)
    g.gate("wardens-door", x1 + 2, x1 + 2, W, W + 1, 13, 14, "minecraft:dark_oak_planks", GATE_WOOD)
    g.box(x1 + 2, x1 + 2, W + 2, W + 2, 12, 15, TRIM)
    # slit windows
    from .palette import BARS_X, BARS_Z
    for y in (W + 3, W + 9):
        g.box(x0 - 2, x0 - 1, y, y + 2, 15, 15, BARS_Z)
        g.box(24, 24, y, y + 2, z0 - 2, z0 - 1, BARS_X)
    g.set(24, W, 16, LANTERN)
    g.set(x0 + 5, W + 12, z1, LANTERN)
    g.mark("bell-tower-stair", 26, W, 18, "west")
    g.mark("tower-fire", 30, W, 17, "west")
    g.mark("tower-shard", 24, W, 15, "south")
    g.mark("echo-apprentice", 17, W + 7, 18, "north")

    # the belfry: an open deck behind arches on all four sides
    bp = L.P["belfry"]
    g.box(x0 - 2, x1 + 2, B, B + bp.height, z0 - 2, z1 + 2, CHAPEL)
    g.clear(x0, x1, B, B + bp.height - 1, z0, z1)
    g.box(x0, x1, top, top, z0, z1, block("minecraft:dark_oak_planks"))
    flight(g, "z", x1 - 2, x1, z0 + 3, 1, W + 12, 4, SB, CHAPEL)      # re-cut the last flight through the deck
    for (a0, a1, fixed, axis) in ((z0 + 1, z1 - 1, x0 - 2, "x"), (z0 + 1, z1 - 1, x1 + 2, "x"),
                                  (x0 + 1, x1 - 1, z0 - 2, "z"), (x0 + 1, x1 - 1, z1 + 2, "z")):
        for k in range(3):
            lo = a0 + k * 5
            for u in range(lo, lo + 4):
                for y in range(B + 1, B + 8 + (1 if u in (lo + 1, lo + 2) else 0)):
                    if axis == "x":
                        g.box(min(fixed, fixed + (1 if fixed < x0 else -1)), max(fixed, fixed + (1 if fixed < x0 else -1)), y, y, u, u, AIR)
                    else:
                        g.box(u, u, y, y, min(fixed, fixed + (1 if fixed < z0 else -1)), max(fixed, fixed + (1 if fixed < z0 else -1)), AIR)
    # bars across the lower arches, so the deck keeps its ringers
    from .palette import BARS_X, BARS_Z
    for x in range(x0 - 2, x1 + 3):
        for z in (z0 - 2, z0 - 1, z1 + 1, z1 + 2):
            for y in (B + 1, B + 2):
                if g.get(x, y, z) == AIR and x0 - 1 <= x <= x1 + 1:
                    g.set(x, y, z, BARS_X)
    for z in range(z0 - 2, z1 + 3):
        for x in (x0 - 2, x0 - 1, x1 + 1, x1 + 2):
            for y in (B + 1, B + 2):
                if g.get(x, y, z) == AIR and z0 - 1 <= z <= z1 + 1:
                    g.set(x, y, z, BARS_Z)
    # low parapet in the arches
    for x in range(x0 - 2, x1 + 3):
        for z in (z0 - 2, z1 + 2):
            if g.get(x, B + 1, z) == AIR:
                g.set(x, B, z, slab("minecraft:tuff_brick_slab"))
    for z in range(z0 - 2, z1 + 3):
        for x in (x0 - 2, x1 + 2):
            if g.get(x, B + 1, z) == AIR:
                g.set(x, B, z, slab("minecraft:tuff_brick_slab"))
    # the bell frame: two posts and a beam; the bell itself is hung by the campaign
    g.box(x0 + 3, x0 + 3, B, B + 8, 15, 16, DARK_PLANKS)
    g.box(x1 - 3, x1 - 3, B, B + 8, 15, 16, DARK_PLANKS)
    g.box(x0 + 3, x1 - 3, B + 9, B + 9, 15, 16, BEAM)
    g.set(24, B + 8, 15, CHAIN)
    g.set(x0 + 1, B, z0 + 1, LANTERN)
    g.mark("belfry", 24, B, 20, "north")
    g.mark("vesper-bell", 24, B + 7, 15, "south", stand=False)
    g.mark("ringer", 24, B, 12, "south")
    g.mark("belfry-echo", 21, B, 16, "east")
    # the tower's head and its spire, the tallest thing on the crag
    head = B + bp.height
    g.box(x0 - 3, x1 + 3, head, head + 1, z0 - 3, z1 + 3, CHAPEL)
    crenels(g, x0 - 3, x1 + 3, z0 - 3, z1 + 3, head + 2, CHAPEL)
    for (px, pz) in ((x0 - 3, z0 - 3), (x1 + 1, z0 - 3), (x0 - 3, z1 + 1), (x1 + 1, z1 + 1)):
        g.box(px, px + 2, head + 2, head + 6, pz, pz + 2, CHAPEL)
        pyramid(g, px, px + 2, pz, pz + 2, head + 7, ROOF, cap=TRIM)
    y = head + 2
    lo, hi = x0 - 1, x1 + 1
    zlo, zhi = z0 - 1, z1 + 1
    while lo <= hi:
        g.box(lo, hi, y, y + 1, zlo, zlo, ROOF); g.box(lo, hi, y, y + 1, zhi, zhi, ROOF)
        g.box(lo, lo, y, y + 1, zlo, zhi, ROOF); g.box(hi, hi, y, y + 1, zlo, zhi, ROOF)
        lo += 1; hi -= 1; zlo += 1; zhi -= 1; y += 2
    g.box((x0 + x1) // 2, (x0 + x1) // 2 + 1, y, y + 3, (z0 + z1) // 2, (z0 + z1) // 2 + 1, TRIM)
