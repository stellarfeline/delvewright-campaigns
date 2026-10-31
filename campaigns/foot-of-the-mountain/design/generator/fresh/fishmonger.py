#!/usr/bin/env python3
"""node/fishmonger: a fishmonger's shop and house on the lower street, its smokehouse and drying yard behind.

The house stands its gable front on the street edge: a five-wide open stall
front (the seam's doorway span) with an ice-and-slab counter just inside,
the shop behind it, and a door through a timber partition to the living room.
A back door gives onto the yard, where nets dry on racks, and the smokehouse
stands at the back of the lot, one cell off the yard.

Run as the starter is run, with the place's allocation:

    "$DELVEWRIGHT_PYTHON" fishmonger.py --allocation <allocation.json> \
        --out <campaign>/programs/fishmonger.json --delvec <delvec>
"""

import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
from starter import (  # noqa: E402
    AIR, Model, run, stairs, slab, pillar, fence, fence_gate, pane, lantern, trapdoor, campfire, chain,
    leaves, wall_torch, street_seam, street_front, clip_beyond, close_edge_gaps, flower_bed,
)

SPRUCE = "spruce"
ROOF = "deepslate_tile"  # the town's dark tile roofs


def build(place):
    m = Model(place)
    p = m.palette
    # One palette family with the street: spruce frame, cobble footing, white daub.
    p["post"] = pillar("spruce_log")
    p["beam"] = pillar("stripped_spruce_log", "z")
    p["beam-x"] = pillar("stripped_spruce_log", "x")
    p["sill"] = "minecraft:cobblestone"
    p["daub"] = "minecraft:white_terracotta"
    p["boards"] = "minecraft:spruce_planks"
    p["floor-house"] = "minecraft:spruce_planks"
    p["floor-smoke"] = "minecraft:cobblestone"
    p["path"] = "minecraft:gravel"
    p["glass"] = pane("glass_pane")
    p["wall"] = "minecraft:white_terracotta"
    p["lintel"] = pillar("stripped_spruce_log", "z")
    p["coping"] = slab("cobblestone", "bottom")

    w = place.datum.value          # walk plane
    g = w - 1                      # ground course
    (x0, _, z0), (x1, _, z1) = place.space

    # ── the house: walls x 12..20, z 2..9; front on the street edge x = 20 ──
    hx0, hx1, hz0, hz1 = 12, x1, z0 + 1, z1 - 1
    head = w + 3                   # wall heads: four courses (door two, a course of daub, the plate)
    for x in range(hx0, hx1 + 1):
        for z in range(hz0, hz1 + 1):
            m.set(x, g, z, "floor-house")
    # sill course of cobble, daub panels framed by spruce posts at corners and every third cell
    m.hollow(hx0, hx1, w, w, hz0, hz1, "sill")
    m.hollow(hx0, hx1, w + 1, head - 1, hz0, hz1, "daub")
    m.hollow(hx0, hx1, head, head, hz0, hz1, "boards")
    for x in (hx0, 14, 16, 18, hx1):
        for z in (hz0, hz1):
            m.box(x, x, w, head, z, z, "post")
    for z in (hz0, 5, hz1):
        m.box(hx0, hx0, w, head, z, z, "post")
    # the plate beam along the long walls
    for z in (hz0, hz1):
        m.box(hx0, hx1, head, head, z, z, "beam-x")
    # ceiling over both rooms; the loft under the roof is closed
    m.box(hx0 + 1, hx1 - 1, head + 1, head + 1, hz0 + 1, hz1 - 1, "boards")
    # windows: two-course panes in the long walls, looking onto the yard ground and the lot's open sides
    for x in (13, 15, 17, 19):
        for z in (hz0, hz1):
            m.box(x, x, w + 1, w + 2, z, z, "glass")

    # the partition between shop (x 17..19) and living room (x 13..15), a door at its middle
    m.box(16, 16, w, head, hz0 + 1, hz1 - 1, "boards")
    m.box(16, 16, w, head, hz0 + 1, hz0 + 1, "post")
    m.box(16, 16, w, head, hz1 - 1, hz1 - 1, "post")
    m.door(16, w, 5, SPRUCE, "east", hinge="left")
    m.set(16, w + 2, 5, "beam")
    # the back door to the yard
    m.door(hx0, w, 6, SPRUCE, "west", hinge="right")
    m.set(hx0, w + 2, 6, "beam")
    m.set(hx0, w, 5, "post")

    # shop: the counter along the front, the customer standing in the doorway strip x = 19
    for z in (3, 4, 5, 6):
        m.set(18, w, z, "minecraft:packed_ice")              # the catch laid on ice
    m.set(18, w, 3, "minecraft:spruce_planks")
    for z in (3, 4, 5, 6):
        m.set(18, w + 1, z, "minecraft:sea_pickle[pickles=3,waterlogged=false]" if z in (4, 6) else slab("smooth_stone", "bottom"))
    # behind the counter: the gutting block, the wash, the knife rack on the wall
    m.set(17, w, 8, "minecraft:cauldron")
    m.set(17, w, 3, pillar("stripped_spruce_log", "y"))      # the gutting block
    m.set(17, w + 1, 3, "minecraft:stone_pressure_plate[powered=false]")
    m.set(18, w, 8, stairs(SPRUCE, "west"))                  # the fishmonger's stool
    # hanging lamps from the ceiling
    m.set(18, head, 5, lantern(True))
    m.set(14, head, 5, lantern(True))

    # living room: bed, table and chairs, a chest dresser of drawers (bookshelf-free), rug
    m.bed(13, w, 3, "blue", "north")
    m.set(14, w, 7, fence(SPRUCE))
    m.set(14, w + 1, 7, "minecraft:spruce_pressure_plate[powered=false]")
    m.set(15, w, 7, stairs(SPRUCE, "west"))
    m.set(14, w, 8, stairs(SPRUCE, "north"))
    m.set(13, w, 8, "minecraft:flower_pot")
    m.set(13, w + 1, 8, AIR)
    m.set(13, w, 6, "minecraft:white_carpet")
    m.set(14, w, 4, "minecraft:blue_carpet")
    m.set(15, w, 4, "minecraft:blue_carpet")
    m.set(14, w, 3, "minecraft:loom[facing=south]")         # the net-mending frame

    # roof: a gable along x, its gable end the front on the street
    m.roof(hx0, hx1, hz0, hz1, head, "x", ROOF, fill="boards")

    m.part(17, 19, hz0 + 1, hz1 - 1, "stall")
    m.part(13, 15, hz0 + 1, hz1 - 1, "stall")
    m.part(16, 16, 5, 5, "stall")

    # ── the smokehouse: walls x 2..8, z 2..7, behind the yard ──
    sx0, sx1, sz0, sz1 = x0 + 1, 8, z0 + 1, 7
    shead = w + 5
    for x in range(sx0, sx1 + 1):
        for z in range(sz0, sz1 + 1):
            m.set(x, g, z, "floor-smoke")
    m.hollow(sx0, sx1, w, shead, sz0, sz1, "minecraft:cobblestone")
    m.hollow(sx0, sx1, w + 2, shead, sz0, sz1, "boards")
    for x in (sx0, sx1):
        for z in (sz0, sz1):
            m.box(x, x, w, shead, z, z, "post")
    m.door(sx1, w, 5, SPRUCE, "east", hinge="left")
    m.set(sx1, w + 2, 5, "beam")
    # smoking: a bed of embers, racks of fish over it on chains
    for x in (3, 5, 7):
        m.set(x, w, sz0 + 1, campfire("south", lit=True))
    for x in range(sx0 + 1, sx1):
        m.set(x, shead, sz0 + 1, "beam-x")
        for x2 in (3, 5, 7):
            if x == x2:
                m.set(x, shead - 1, sz0 + 1, chain("y"))
    m.box(sx0 + 1, sx1 - 1, shead + 1, shead + 1, sz0 + 1, sz1 - 1, "boards")
    m.set(4, shead - 2, 3, "minecraft:dried_kelp_block")
    m.set(6, shead - 2, 3, "minecraft:dried_kelp_block")
    m.set(4, shead - 1, 3, chain("y"))
    m.set(6, shead - 1, 3, chain("y"))
    m.set(3, w, sz1 - 1, "minecraft:dried_kelp_block")
    m.set(3, w + 1, sz1 - 1, "minecraft:dried_kelp_block")
    m.roof(sx0, sx1, sz0, sz1, shead, "x", ROOF, fill="boards")
    # the smoke goes out by a brick stack over the embers
    m.box(4, 4, shead + 1, shead + 6, 4, 4, "minecraft:bricks")
    m.set(4, shead, 4, "minecraft:bricks")
    m.part(sx0 + 1, sx1 - 1, sz0 + 1, sz1 - 1, "smokehouse")
    m.part(sx1, sx1, 5, 5, "smokehouse")

    # ── the yard between them, and the strip behind the smokehouse ──
    for x in range(9, hx0):
        for z in range(z0, z1 + 1):
            if (x, z) in ((9, 5), (10, 5), (11, 5), (10, 6), (11, 6), (9, 6)):
                m.set(x, g, z, "path")
    # drying racks: posts and a rail, nets hung on it
    for x in (2, 4, 6, 8):
        m.box(x, x, w, w + 2, 9, 9, fence(SPRUCE))
    for x in range(3, 8):
        m.set(x, w + 2, 9, fence(SPRUCE))
        if x in (3, 5, 7):
            m.set(x, w + 1, 9, "minecraft:cobweb")
    m.box(10, 10, w, w + 2, 9, 9, fence(SPRUCE))
    m.box(10, 10, w, w + 2, z0 + 1, z0 + 1, fence(SPRUCE))
    for z in range(z0 + 2, z0 + 3):
        m.set(10, w + 2, z, fence(SPRUCE))
    # yard life: a water trough, a grindstone for the knives, pots by the back door
    m.set(9, w, 3, "minecraft:water_cauldron[level=3]")
    m.set(11, w, 3, "minecraft:grindstone[face=floor,facing=north]")
    m.set(11, w, 8, "minecraft:potted_red_tulip")
    m.set(11, w, 9, "minecraft:potted_cornflower")
    m.set(9, w, 8, "minecraft:composter[level=0]")
    m.part(9, 11, z0, z1, "yard")
    m.part(x0 + 1, 8, 9, z1, "yard")

    # ── life round the house: a hedge on the house's long sides and a bed of flowers ──
    for x in range(13, 20, 2):
        m.set(x, w, z0, leaves("oak"))
    flower_bed(m, [(x, z1) for x in range(14, 20, 2)], ["minecraft:poppy", "minecraft:oxeye_daisy", "minecraft:cornflower"])

    # ── the street edge: the house front stands on it; close it as the street's air asks ──
    fronted, edge = street_seam(place, "east")
    if fronted:
        ex, rows, door_top, air = edge
        street_front(m, ex, z0, z1, rows, air, {"wall": "daub", "lintel": "beam", "coping": "coping"},
                     door_h=door_top, inward=-1, axis="x")
    clip_beyond(m, x0, x1, z0, z1)
    m.finish()
    return m


raise SystemExit(run(build))
