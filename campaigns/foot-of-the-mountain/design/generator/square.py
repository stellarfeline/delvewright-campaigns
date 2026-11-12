#!/usr/bin/env python3
"""node/square: the cathedral square of Kelderby on the afternoon of the Founders' Play.

Cobbled, a well at its middle, two trees with benches under them in the west
half, rows of audience benches facing east, and a timber stage on the east
half: its deck a body's height up on trestles, its front facing west toward
the inn, steps up at its south end, lanterns along its front edge and painted
flats at its back. A clear walk of four cells runs between the stage and the
cathedral's close; the north-south way from the castle road to the main street
runs clear past the well.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
from starter import Model, run, fence, lantern, leaves, slab, stairs, chain  # noqa: E402

SPRUCE = "minecraft:spruce"


def build(place):
    m = Model(place)
    w = place.datum.value          # the walk plane
    g = w - 1                      # the ground course
    (x0, _, z0), (x1, _, z1) = place.space

    m.palette.update({
        "paving": [
            {"weight": 6, "block": "minecraft:cobblestone"},
            {"weight": 2, "block": "minecraft:andesite"},
            {"weight": 1, "block": "minecraft:stone"},
            {"weight": 1, "block": "minecraft:mossy_cobblestone"},
        ],
        "kennel": "minecraft:polished_andesite",
        "setts": "minecraft:stone_bricks",
        "boards": "minecraft:spruce_planks",
        "beam": "minecraft:stripped_spruce_log[axis=z]",
        "trunk": "minecraft:oak_log[axis=y]",
        "crown": leaves("minecraft:oak"),
    })

    # ---- the cobbles: the whole ground course, the ring included ----
    for x in range(0, m.ex):
        for z in range(0, m.ez):
            m.set(x, g, z, "paving")
    # the kennel down the north-south way, from the castle road to the main street
    for z in range(0, m.ez):
        m.set(16, g, z, "kennel")

    # ---- the well at the middle: a stone kerb, water, posts and a little roof ----
    wx, wz = 15, 12
    m.box(wx - 1, wx + 1, w, w, wz - 1, wz + 1, "setts")
    m.set(wx, g, wz, "setts")
    m.set(wx, w, wz, "minecraft:water[level=0]")
    for cx, cz in ((wx - 1, wz - 1), (wx + 1, wz - 1), (wx - 1, wz + 1), (wx + 1, wz + 1)):
        m.box(cx, cx, w + 1, w + 2, cz, cz, fence(SPRUCE))
    m.box(wx - 1, wx + 1, w + 3, w + 3, wz - 1, wz + 1, slab(SPRUCE))
    m.set(wx, w + 2, wz, chain("y"))

    # ---- two trees in the west half, a bench on two sides of each ----
    for tx, tz, bz in ((4, 4, 6), (4, 21, 19)):
        m.box(tx, tx, w, w + 3, tz, tz, "trunk")
        for x in range(tx - 2, tx + 3):
            for z in range(tz - 2, tz + 3):
                for y in range(w + 3, w + 6):
                    d = abs(x - tx) + abs(z - tz)
                    top = y - (w + 3)
                    if (top == 0 and d <= 3) or (top == 1 and d <= 3) or (top == 2 and d <= 1):
                        if not (x == tx and z == tz and y <= w + 3):
                            m.set(x, y, z, "crown")
        m.set(tx, w + 6, tz, "crown")
        # festival lanterns hung under the crown on both sides of the trunk, so the
        # benches in its shade read at night
        for lx, lz in ((tx - 1, tz + (1 if bz > tz else -1)), (tx + 1, tz + (1 if bz > tz else -1))):
            m.set(lx, w + 3, lz, chain("y"))
            m.set(lx, w + 2, lz, lantern(True))
        # a bench under the crown, its back to the trunk side
        facing = "north" if bz > tz else "south"
        for x in range(tx - 1, tx + 2):
            m.set(x, w, bz, stairs(SPRUCE, facing))

    # ---- rows of audience benches in the west half, facing the stage ----
    for bx in (6, 8, 10):
        for zs in (range(5, 11), range(15, 19)):
            for z in zs:
                m.set(bx, w, z, stairs(SPRUCE, "west"))

    # ---- the stage: deck a body's height up, front on the west ----
    sx0, sx1, sz0, sz1 = 20, 26, 6, 18
    deck = w + 1                    # the deck course; a body stands on it at w + 2
    m.box(sx0, sx1, deck, deck, sz0, sz1, "boards")
    # trestles under the deck: posts every other cell along each long side and the middle
    for x in (sx0, (sx0 + sx1) // 2, sx1):
        for z in range(sz0, sz1 + 1, 2):
            m.set(x, w, z, fence(SPRUCE))
    for z in (sz0, sz1):
        for x in range(sx0, sx1 + 1, 2):
            m.set(x, w, z, fence(SPRUCE))
    # a front beam on the deck edge, and lanterns along it
    for z in range(sz0, sz1 + 1, 3):
        m.set(sx0, deck + 1, z, lantern(False))
    # the steps up at the south end: two treads rising north onto the deck
    for x in (22, 23):
        m.set(x, w, sz1 + 2, stairs(SPRUCE, "north"))
        m.set(x, w, sz1 + 1, "boards")
        m.set(x, deck, sz1 + 1, stairs(SPRUCE, "north"))
    # the painted flats standing at the back: hills, sky and the castle on its mountain
    fx = sx1 - 1
    for z in range(sz0 + 2, sz1 - 1):
        for y in range(deck + 1, deck + 5):
            h = y - (deck + 1)
            hill = 1 + (1 if (z % 5) in (1, 2, 3) else 0)
            if h < hill:
                role = "minecraft:green_wool" if h == 0 else "minecraft:lime_wool"
            elif h == 3 and z in (8, 9, 15):
                role = "minecraft:white_wool"
            else:
                role = "minecraft:light_blue_wool"
            m.set(fx, y, z, role)
    # the castle painted on the flats
    for y in range(deck + 2, deck + 5):
        m.set(fx, y, 12, "minecraft:light_gray_wool")
    m.set(fx, deck + 2, 11, "minecraft:light_gray_wool")
    m.set(fx, deck + 2, 13, "minecraft:light_gray_wool")
    m.set(fx, deck + 4, 12, "minecraft:red_wool")
    # the flats' braces behind them, on the back of the deck
    for z in range(sz0 + 2, sz1 - 1, 3):
        m.box(sx1, sx1, deck + 1, deck + 2, z, z, fence(SPRUCE))
    # props stacked at the stage's north foot, clear of the cathedral walk: a hay bale and an empty wooden tub
    m.set(sx0 + 1, w, sz0 - 1, "minecraft:hay_block[axis=y]")
    m.set(sx0 + 2, w, sz0 - 1, "minecraft:composter[level=0]")
    # the third defence line's supply chest beside them, and a cart of hay bales for cover
    m.set(sx0 + 3, w, sz0 - 1, "minecraft:chest[facing=south,type=single,waterlogged=false]")
    m.mark("supply-stage", sx0 + 3, sz0 - 1, facing="south", y=w)
    # the cake table on the deck: a trestle under a white cloth, the festival
    # cake on it (the `cake-table` mark, which the cake's theft clears)
    ct = (sx0 + 2, (sz0 + sz1) // 2)
    m.set(ct[0], deck + 1, ct[1], "minecraft:spruce_fence[east=false,north=false,south=false,waterlogged=false,west=false]")
    m.set(ct[0], deck + 1, ct[1] - 1, "minecraft:spruce_fence[east=false,north=false,south=false,waterlogged=false,west=false]")
    m.set(ct[0], deck + 1, ct[1] + 1, "minecraft:spruce_fence[east=false,north=false,south=false,waterlogged=false,west=false]")
    for dz in (-1, 1):
        m.set(ct[0], deck + 2, ct[1] + dz, "minecraft:white_carpet")
    # the cake itself is the campaign's: set on the cloth when the festival
    # opens, and cleared by the raider who takes it (a cake is not a block a
    # piece may hold, DW0730)

    # ---- lamp posts at the square's four quarters ----
    for lx, lz in ((11, 3), (19, 3), (11, 22), (19, 22)):
        m.box(lx, lx, w, w + 2, lz, lz, fence(SPRUCE))
        m.set(lx, w + 3, lz, lantern(False))

    # ---- flowers in pots along the north edge, clear of the castle road ----
    for x in list(range(3, 12, 3)) + list(range(21, 30, 3)):
        m.set(x, w, z0, "minecraft:potted_red_tulip")

    m.finish()

    # ---- the owed names ----
    # the square's body: outside The Bell, with room round it for the cast
    m.mark("node-square", 12, 13, facing="east")
    # the stage's station: before the stage's front, at its middle
    m.mark("stage", sx0 - 1, (sz0 + sz1) // 2, facing="east")
    # the cake on the table, between the two ends of its cloth
    m.mark("cake-table", sx0 + 2, (sz0 + sz1) // 2, facing="west", y=w + 3)
    # the party come up the main street and spawn at its head
    m.mark("spawn", 15, 21, facing="north")
    return m


raise SystemExit(run(build, reason="the stage's trestle gap, the well's roof and the tree crowns: seen, never stood on"))
