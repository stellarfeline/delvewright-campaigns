#!/usr/bin/env python3
"""The farm district on the east flank: the farm track and the six plots off it.

    DELVEWRIGHT_SKILL=<skill> python3 farm.py --allocation <delvec allocation . node/<place>> \\
        --out ../../programs/<place>.json --delvec <delvec>

One generator, dispatched on the place's stem. After the open-field village
(strips of crops behind the houses, a track out to them) and the farmyard
(the barn, the byre and the pens round a yard): a wheat field in strips with
walks between them, an apple orchard in rows, a sheep fold, a duck pond, a
cattle pen with an open byre, and the big barn with its yard. Every plot is
open to the commons; fences and hedges stand inside it, each pen with a field
gate onto the track. Lamps stand where a canopy or a roof shades the ground,
so the plots read at night. Piece-local axes: +x east, +z south; the play
space is 1..W by 1..D.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
from starter import Model, fence, fence_gate, lantern, leaves, pillar, run, slab, stairs  # noqa: E402

WOOD = "spruce"


LAMPS = set()
FREE_ROWS = set()   # the rows behind the track's opening: the plot's own ground, never a part


def part(m, x0, x1, z0, z1, stem):
    """Name the columns for a part, leaving out every lamp post (its lantern's
    top is a cell no body reaches, which the starter claims out of walk)."""
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if (x, z) not in LAMPS and z not in FREE_ROWS:
                m.part(x, x, z, z, stem)


def lamp_post(m, x, z, d):
    LAMPS.add((x, z))
    m.set(x, d, z, fence(WOOD))
    m.set(x, d + 1, z, fence(WOOD))
    m.set(x, d + 2, z, lantern())


def ground(m, W, D, g, block):
    m.box(1, W, g, g, 1, D, block)


OLD_PLOTS = ("wheat-field", "orchard", "sheep-pen", "goat-pen", "net-green", "beacon-point", "bay", "shoals")
TRACKS = ("farm-lane", "west-track", "meadow-track", "lane-8", "cathedral", "terrace-track")


def track_side(place):
    """The side of the plot the track it opens off runs along: south for the plots north of it."""
    for s in place.seams:
        if any(t in s["stem"] for t in TRACKS):
            return s["seam"]["face"]
    return None


STRIPES = (("minecraft:red_wool", "minecraft:white_wool"), ("minecraft:blue_wool", "minecraft:yellow_wool"),
           ("minecraft:lime_wool", "minecraft:white_wool"), ("minecraft:orange_wool", "minecraft:yellow_wool"),
           ("minecraft:pink_wool", "minecraft:white_wool"))


def stall(m, x0, z0, d, k, facing_z):
    """A festival stall three wide and two deep: corner posts, a striped awning, a
    counter of barrels and a slab along its front (the side toward facing_z)."""
    a, b = STRIPES[k % len(STRIPES)]
    zf, zb = (z0, z0 + 1) if facing_z < z0 else (z0 + 1, z0)
    for x in (x0, x0 + 2):
        for z in (z0, z0 + 1):
            m.set(x, d, z, fence(WOOD)); m.set(x, d + 1, z, fence(WOOD))
    for x in range(x0, x0 + 3):
        for z in (z0, z0 + 1):
            m.set(x, d + 2, z, a if (x + z) % 2 else b)
    m.set(x0 + 1, d, zf, "minecraft:barrel[facing=up,open=false]")
    m.set(x0 + 1, d, zb, "minecraft:spruce_slab[type=top,waterlogged=false]")


def target(m, x, z, d):
    """A straw butt: two bales stacked, a red mark painted on the top one's face."""
    m.set(x, d, z, "minecraft:hay_block[axis=y]")
    m.set(x, d + 1, z, "minecraft:hay_block[axis=y]")
    m.set(x, d + 2, z, "minecraft:red_wool")


def bench(m, x0, x1, z, d, facing):
    for x in range(x0, x1 + 1):
        m.set(x, d, z, stairs(WOOD, facing))


def butts(m, W, D, d, g, side):
    """The archery butts: a mown range, the targets at the far end, the shooting
    line of rails by the track with a gap to walk through, the bow stall."""
    ground(m, W, D, g, "minecraft:grass_block[snowy=false]")
    far, near = (2, D - 2) if side == "south" else (D - 1, 3)
    for x in range(4, W - 2, 6):
        target(m, x, far, d)
    for x in range(2, W):
        if x % 6 not in (0, 1):
            m.set(x, d, near, fence(WOOD))
    for x in range(2, W, 2):
        m.set(x, g, near + (1 if side == "north" else -1), "minecraft:dirt_path")
    stall(m, W - 4, near - 3 if side == "south" else near + 2, d, 0, near)
    lamp_post(m, 1, far, d)
    lamp_post(m, W, far, d)
    lamp_post(m, 1, near, d)
    lamp_post(m, W, near, d)
    part(m, 1, W, 2, D - 1, "range")


def allotments(m, W, D, d, g, side):
    """Beds of pumpkins and melons in rows, paths between them, compost heaps, a
    scarecrow in a festival hat, a lean-to for the tools."""
    ground(m, W, D, g, "minecraft:grass_block[snowy=false]")
    rows = range(3, D - 2, 4)
    for z in rows:
        for x in range(2, W):
            if x % 5 == 1:
                continue
            m.set(x, g, z, "minecraft:coarse_dirt")
            m.set(x, g, z + 1, "minecraft:podzol[snowy=false]")
            if (x + z) % 3 == 0:
                m.set(x, d, z, "minecraft:pumpkin")
            elif (x + z) % 3 == 1:
                m.set(x, d, z + 1, "minecraft:melon")
        for x in range(1, W + 1):
            m.set(x, g, z + 2, "minecraft:dirt_path")
    back = 1 if side != "north" else D       # the row away from the track's opening
    m.set(2, d, back, "minecraft:composter[level=8]")
    m.set(W - 1, d, back, "minecraft:composter[level=4]")
    sx, sz = W // 2, rows[0] + 1
    m.set(sx, d, sz, fence(WOOD)); m.set(sx, d + 1, sz, "minecraft:hay_block[axis=y]")
    m.set(sx, d + 2, sz, "minecraft:carved_pumpkin[facing=south]")
    near = 3 if side == "north" else 1
    lamp_post(m, 1, near, d)
    lamp_post(m, W, near, d)
    lamp_post(m, 1, D, d)
    lamp_post(m, W, D, d)
    part(m, 1, W, 2, D - 1, "beds")


def fair(m, W, D, d, g, side):
    """The festival fair: a maypole hung with ribbons at the middle, a ring of
    striped stalls and an open tent, benches and bales to sit on, lamps on posts."""
    ground(m, W, D, g, "minecraft:grass_block[snowy=false]")
    cx, cz = (W + 1) // 2, (D + 1) // 2
    for y in range(d, d + 9):
        m.set(cx, y, cz, pillar("minecraft:stripped_birch_log"))
    m.set(cx, d + 9, cz, "minecraft:white_banner[rotation=0]")
    for k, (dx, dz) in enumerate(((1, 0), (-1, 0), (0, 1), (0, -1))):
        m.set(cx + dx, d + 8, cz + dz, STRIPES[k][0].replace("_wool", "_carpet") if False else STRIPES[k][0])
    for x in range(1, W + 1):
        for z in range(1, D + 1):
            if abs(x - cx) + abs(z - cz) in (4, 5) and (x + z) % 2 == 0:
                m.set(x, g, z, "minecraft:dirt_path")
    k = 0
    for x0 in range(2, W - 3, 5):
        stall(m, x0, 3, d, k, D); k += 1
        stall(m, x0, D - 4, d, k, 1); k += 1
    # the tent: an open canopy on posts at the west end, benches under it
    for z in (cz - 2, cz + 2):
        for x in (2, 5):
            m.set(x, d, z, fence(WOOD)); m.set(x, d + 1, z, fence(WOOD)); m.set(x, d + 2, z, fence(WOOD))
    for x in range(2, 6):
        for z in range(cz - 2, cz + 3):
            m.set(x, d + 3, z, "minecraft:white_wool" if z % 2 else "minecraft:red_wool")
    m.set(3, d + 2, cz, lantern(hanging=True))
    bench(m, 3, 4, cz - 1, d, "north")
    bench(m, 3, 4, cz + 1, d, "south")
    for (x, z) in ((W - 3, cz - 1), (W - 3, cz + 1), (W - 2, cz)):
        m.set(x, d, z, "minecraft:hay_block[axis=x]")
    for (x, z) in ((cx - 3, cz - 3), (cx + 3, cz - 3), (cx - 3, cz + 3), (cx + 3, cz + 3), (1, 1), (W, 1), (1, D), (W, D)):
        lamp_post(m, x, z, d)
    part(m, 1, W, 2, D - 1, "fair")


def picnic(m, W, z0, z1, d, g):
    """The fair's lower field toward the beach: trestle tables with benches in rows,
    a bonfire ringed with log seats, and a dance floor of boards with lamps at its corners."""
    for x0 in range(3, W - 3, 6):
        for z in range(z0 + 2, z0 + 12, 5):
            for x in (x0, x0 + 1, x0 + 2):
                m.set(x, d, z, "minecraft:spruce_slab[type=top,waterlogged=false]")
                m.set(x, d, z - 1, stairs(WOOD, "south"))
                m.set(x, d, z + 1, stairs(WOOD, "north"))
    bx, bz = W // 3, (z0 + 14 + z1) // 2
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            m.set(bx + dx, g, bz + dz, "minecraft:cobblestone")
    m.set(bx, d, bz, "minecraft:campfire[facing=north,lit=true,signal_fire=false,waterlogged=false]")
    for x in (bx - 3, bx + 3):
        m.set(x, d, bz, pillar("minecraft:stripped_oak_log", "z"))
    for z in (bz - 3, bz + 3):
        m.set(bx, d, z, pillar("minecraft:stripped_oak_log", "x"))
    fx0, fz0 = W // 2 + 2, z0 + 14
    for x in range(fx0, min(W, fx0 + 8)):
        for z in range(fz0, min(z1, fz0 + 8)):
            m.set(x, g, z, "minecraft:oak_planks")
    for (x, z) in ((fx0 - 1, fz0 - 1), (min(W, fx0 + 8), fz0 - 1), (fx0 - 1, min(z1, fz0 + 8)), (min(W, fx0 + 8), min(z1, fz0 + 8)), (bx - 4, bz - 4)):
        if 1 <= x <= W and z <= z1:
            lamp_post(m, x, z, d)


def bonfire(m, W, D, d, g, side):
    """The bonfire green on the shore below the west track: the festival's bonfire
    in a ring of stones with log seats, two upturned boats on trestles, lobster pots
    and a lamp at each corner."""
    ground(m, W, D, g, "minecraft:grass_block[snowy=false]")
    for x in range(1, W + 1):
        for z in range(D - 3, D + 1):
            m.set(x, g, z, "minecraft:sand")
    bx, bz = W // 2, D // 2
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            m.set(bx + dx, g, bz + dz, "minecraft:cobblestone")
    m.set(bx, d, bz, "minecraft:campfire[facing=north,lit=true,signal_fire=false,waterlogged=false]")
    for x in (bx - 3, bx + 3):
        m.set(x, d, bz - 1, pillar("minecraft:stripped_oak_log", "z"))
        m.set(x, d, bz + 1, pillar("minecraft:stripped_oak_log", "z"))
    for z in (bz - 3, bz + 3):
        m.set(bx - 1, d, z, pillar("minecraft:stripped_oak_log", "x"))
        m.set(bx + 1, d, z, pillar("minecraft:stripped_oak_log", "x"))
    for x0 in (3, W - 6):
        for x in range(x0, x0 + 4):
            m.set(x, d, D - 5, stairs("minecraft:dark_oak", "south", "top"))
    for (x, z) in ((2, D - 2), (3, D - 2), (W - 2, D - 2)):
        m.set(x, d, z, "minecraft:barrel[facing=up,open=false]")
    for (x, z) in ((1, 3), (W, 3), (1, D - 1), (W, D - 1)):
        lamp_post(m, x, z, d)
    part(m, 1, W, 2, D - 1, "green")


def bees(m, W, D, d, g, side):
    """Hives in rows among wildflowers, a honey stand on trestles, a bench."""
    ground(m, W, D, g, "minecraft:grass_block[snowy=false]")
    flowers = ("minecraft:cornflower", "minecraft:oxeye_daisy", "minecraft:poppy", "minecraft:allium",
               "minecraft:azure_bluet", "minecraft:dandelion", "minecraft:lily_of_the_valley")
    for x in range(1, W + 1):
        for z in range(2, D):
            if (x * 3 + z * 5) % 7 == 0:
                m.set(x, d, z, flowers[(x + z) % len(flowers)])
    for x in range(3, W - 1, 4):
        for z in range(4, D - 3, 5):
            m.set(x, d, z, "minecraft:beehive[facing=south,honey_level=0]")
    stall(m, W // 2 - 1, 2 if side == "north" else D - 3, d, 3, D if side == "north" else 1)
    bench(m, 2, 3, D - 1 if side == "north" else 2, d, "north" if side == "north" else "south")
    for (x, z) in ((1, 3), (W, 3), (1, D), (W, D), (W // 2, D // 2)):
        lamp_post(m, x, z, d)
    part(m, 1, W, 2, D - 1, "meadow")


def garden(m, W, D, d, g, side):
    """The cathedral's garth: square herb beds with paths to a stone fountain at the
    middle, benches, a stall where the herbs are sold, lamps."""
    ground(m, W, D, g, "minecraft:grass_block[snowy=false]")
    cx, cz = (W + 1) // 2, (D + 1) // 2
    herbs = ("minecraft:allium", "minecraft:azure_bluet", "minecraft:lily_of_the_valley", "minecraft:cornflower",
             "minecraft:oxeye_daisy", "minecraft:fern", "minecraft:short_grass")
    for x in range(1, W + 1):
        for z in range(1, D + 1):
            if x in (cx - 1, cx, cx + 1) or z in (cz - 1, cz, cz + 1) or x in (1, W) or z in (1, D):
                m.set(x, g, z, "minecraft:gravel" if (x + z) % 3 else "minecraft:dirt_path")
            elif (x + z) % 2 == 0:
                m.set(x, g, z, "minecraft:podzol[snowy=false]")
                m.set(x, d, z, herbs[(x * 3 + z) % len(herbs)])
    # the fountain: a stone rim round water at the middle, a lamp on each corner
    for x in range(cx - 1, cx + 2):
        for z in range(cz - 1, cz + 2):
            m.set(x, g, z, "minecraft:stone_bricks")
            if (x, z) != (cx, cz):
                m.set(x, d, z, "minecraft:stone_brick_slab[type=bottom,waterlogged=false]")
    m.set(cx, d, cz, "minecraft:water_cauldron[level=3]")
    for (x, z) in ((cx - 2, cz - 2), (cx + 2, cz + 2), (1, 1), (W, D), (W, 1), (1, D)):
        lamp_post(m, x, z, d)
    stall(m, W - 4, 2 if side == "north" else D - 3, d, 2, D if side == "north" else 1)
    bench(m, 3, 5, cz + 2, d, "north")
    part(m, 1, W, 2, D - 1, "garth")


def games(m, W, D, d, g, side):
    """The games yard: stalls for the ring toss and the coconut shy, tubs for
    apple bobbing, a row of straw targets, benches."""
    ground(m, W, D, g, "minecraft:grass_block[snowy=false]")
    for x in range(1, W + 1):
        for z in range(1, D + 1):
            if (x + 2 * z) % 5 == 0:
                m.set(x, g, z, "minecraft:dirt_path")
    back = D - 2 if side == "north" else 2
    for k, x0 in enumerate(range(2, W - 3, 5)):
        stall(m, x0, back if side == "north" else back, d, k, 1 if side == "north" else D)
    mid = D // 2
    for x in (4, 7, 10):
        m.set(x, d, mid, "minecraft:water_cauldron[level=3]")
    for x in (W - 6, W - 3):
        target(m, x, mid, d)
    bench(m, 3, 5, mid + 2 if side == "north" else mid - 2, d, "north")
    for (x, z) in ((1, mid), (W, mid), (W // 2, mid + 2)):
        lamp_post(m, x, z, d)
    part(m, 1, W, 2, D - 1, "games")


def wheat_field(m, W, D, d, g):
    ground(m, W, D, g, "minecraft:grass_block[snowy=false]")
    # strips of wheat four wide, a trodden walk between each, the walks running
    # from the track's edge to the far hedge
    walks = set(range(1, W + 1, 5))
    for x in range(1, W + 1):
        for z in range(2, D - 1):
            if x in walks:
                m.set(x, g, z, "minecraft:dirt_path")
            else:
                # the field is cut for the festival: stubble in rows, the
                # sheaves stood up in stooks along each strip (crops are not
                # a block a piece may hold: the engine refuses farmland and
                # wheat, DW0730, so the harvest is drawn in hay)
                m.set(x, g, z, "minecraft:coarse_dirt" if z % 2 else "minecraft:podzol[snowy=false]")
                if x % 5 == 3 and z % 4 == 2:
                    m.set(x, d, z, "minecraft:hay_block[axis=y]")
                elif (x * 7 + z * 3) % 5 == 0:
                    m.set(x, d, z, "minecraft:leaf_litter[facing=north,segment_amount=3]")
    for x in range(1, W + 1):
        m.set(x, g, D - 1, "minecraft:dirt_path")
        m.set(x, g, D, "minecraft:dirt_path")
    # the far hedge
    for x in range(1, W + 1):
        if x not in walks:
            m.set(x, d, 1, leaves("oak"))
    # the scarecrow in the middle strip
    sx, sz = W // 2 + (1 if (W // 2) in walks else 0), D // 2
    m.set(sx, d, sz, fence(WOOD))
    m.set(sx, d + 1, sz, "minecraft:hay_block[axis=y]")
    m.set(sx, d + 2, sz, "minecraft:carved_pumpkin[facing=south]")
    m.set(sx - 1, d + 1, sz, fence(WOOD))
    m.set(sx + 1, d + 1, sz, fence(WOOD))
    # the hayrick and the hay cart by the track
    for (x, y, z) in ((W - 2, d, D - 2), (W - 1, d, D - 2), (W - 2, d + 1, D - 2), (W - 2, d, D - 3), (W - 1, d, D - 3)):
        m.set(x, y, z, "minecraft:hay_block[axis=x]")
    m.part(W - 2, W - 1, D - 3, D - 2, "hayrick")
    m.set(3, d, D - 2, stairs(WOOD, "east", "top"))
    m.set(4, d, D - 2, stairs(WOOD, "west", "top"))
    m.set(3, d + 1, D - 2, "minecraft:hay_block[axis=x]")
    lamp_post(m, 6, D, d)
    lamp_post(m, W - 4, D, d)
    part(m, 1, W, 1, D - 4, "field")
    part(m, 1, W - 3, D - 3, D - 1, "field")
    part(m, W, W, D - 3, D - 1, "field")


def orchard(m, W, D, d, g):
    ground(m, W, D, g, "minecraft:grass_block[snowy=false]")
    trees = [(x, z) for x in range(3, W - 1, 5) for z in range(3, D - 2, 5)]
    for (x, z) in trees:
        m.set(x, d, z, pillar("minecraft:oak_log"))
        m.set(x, d + 1, z, pillar("minecraft:oak_log"))
        m.set(x, d + 2, z, pillar("minecraft:oak_log"))
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                for y in (d + 3, d + 4):
                    if (dx, dz) != (0, 0) or y == d + 4:
                        if y == d + 4 and abs(dx) + abs(dz) == 2:
                            continue
                        m.set(x + dx, y, z + dz, "minecraft:flowering_azalea_leaves[distance=1,persistent=true,waterlogged=false]")
        m.set(x, d + 3, z, pillar("minecraft:oak_log"))
    # lanterns on posts between the rows, so the ground under the crowns reads at night
    for (x, z) in trees:
        if x + 2 <= W and z + 2 <= D:
            lamp_post(m, x + 2, z + 2, d)
    for (x, z) in ((2, 2), (W - 1, D - 1)):
        m.set(x, d, z, "minecraft:composter[level=8]")
    for x in range(1, W + 1, 3):
        if m.get(x, d, 1) is None:
            m.set(x, d, 1, "minecraft:poppy" if x % 2 else "minecraft:dandelion")
    part(m, 1, W, 2, D - 1, "orchard")


def pen(m, W, D, d, g, side, floor_block, animal_part, shelter_part):
    ground(m, W, D, g, floor_block)
    # the fence round the pen, one cell inside the plot's edge, a field gate on the track's side
    x0, x1, z0, z1 = 2, W - 1, (2 if side == "south" else 3), D - 1
    gz = z1 if side == "south" else z0
    gx = (x0 + x1) // 2
    for x in range(x0, x1 + 1):
        for z in (z0, z1):
            m.set(x, d, z, fence(WOOD))
    for z in range(z0, z1 + 1):
        for x in (x0, x1):
            m.set(x, d, z, fence(WOOD))
    for x in (gx, gx + 1):
        m.set(x, d, gz, fence_gate(WOOD, "north" if side == "north" else "south", open=True))
    # the shelter: a lean-to roof on posts in the pen's far corner, a hay rack under it
    fz = z0 + 1 if side == "south" else z1 - 3
    # one clear column between the pen's fence and the shelter's posts, so
    # nothing a body steps into beside the fence is a pocket
    for (x, z) in ((x0 + 2, fz), (x0 + 5, fz), (x0 + 2, fz + 2), (x0 + 5, fz + 2)):
        for y in (d, d + 1, d + 2):
            m.set(x, y, z, fence(WOOD))
    # the roof a course higher than a body standing on the hay needs
    for x in range(x0 + 2, x0 + 6):
        for z in range(fz, fz + 3):
            m.set(x, d + 3, z, slab(WOOD, "bottom"))
    # under the roof: a lantern hung from it and nothing on the ground a
    # body climbs onto (a block there leaves a pocket between it and the
    # pen's fence)
    m.set(x0 + 3, d + 2, fz + 1, lantern(hanging=True))
    m.set(x1 - 3, d, (z0 + z1) // 2, "minecraft:water_cauldron[level=3]")
    part(m, x0 + 2, x0 + 5, fz, fz + 2, shelter_part)
    if side == "south":
        lamp_post(m, gx - 1, gz + 1, d)
    for z in range(1, D + 1):
        for x in range(1, W + 1):
            if not (x0 + 2 <= x <= x0 + 5 and fz <= z <= fz + 2) and 1 < z < D:
                part(m, x, x, z, z, animal_part)


def pond(m, W, D, d, g, side):
    ground(m, W, D, g, "minecraft:grass_block[snowy=false]")
    cx, cz, rx, rz = (W + 1) / 2, (D + 1) / 2 + (1 if side == "north" else -1), W / 2 - 3, D / 2 - 4
    water = set()
    for x in range(1, W + 1):
        for z in range(1, D + 1):
            q = ((x - cx) / rx) ** 2 + ((z - cz) / rz) ** 2
            if q <= 1.0:
                water.add((x, z))
                m.set(x, g, z, "minecraft:water[level=0]")
                m.set(x, g - 1, z, "minecraft:clay" if q > 0.5 else "minecraft:mud")
            elif q <= 1.6:
                m.set(x, g, z, "minecraft:sand")
    for i, (x, z) in enumerate(sorted(water)):
        if i % 7 == 3:
            m.set(x, d, z, "minecraft:lily_pad")
    for (x, z) in sorted(water):
        for nx, nz in ((x + 1, z), (x - 1, z), (x, z + 1), (x, z - 1)):
            if (nx, nz) not in water and 1 <= nx <= W and 1 <= nz <= D and (nx + nz) % 4 == 0:
                m.set(nx, d, nz, "minecraft:sugar_cane[age=0]")
    # the bench under a willow on the far bank, a lamp beside it
    bz = 2 if side == "north" else D - 1
    m.set(3, d, bz, stairs(WOOD, "north" if side == "north" else "south"))
    m.set(4, d, bz, stairs(WOOD, "north" if side == "north" else "south"))
    lamp_post(m, 2, bz, d)
    lamp_post(m, W - 1, D + 1 - bz, d)
    part(m, 1, W, 2, D - 1, "pond-bank")


def barn(m, W, D, d, g, side):
    ground(m, W, D, g, "minecraft:grass_block[snowy=false]")
    # the barn on the far half of the plot, its doors toward the track
    bx0, bx1 = 3, W - 2
    bz0, bz1 = (2, 9) if side == "south" else (D - 8, D - 1)
    dz = bz1 if side == "south" else bz0
    m.box(bx0, bx1, g, g, bz0, bz1, "minecraft:cobblestone")
    m.box(bx0 + 1, bx1 - 1, g, g, bz0 + 1, bz1 - 1, "minecraft:spruce_planks")
    top = d + 4
    m.hollow(bx0, bx1, d, top, bz0, bz1, "minecraft:spruce_planks")
    for x in (bx0, bx1):
        for z in (bz0, bz1):
            for y in range(d, top + 1):
                m.set(x, y, z, pillar("minecraft:stripped_spruce_log"))
    for x in range(bx0, bx1 + 1):
        m.set(x, d, bz0, "minecraft:cobblestone")
        m.set(x, d, bz1, "minecraft:cobblestone")
    for z in range(bz0, bz1 + 1):
        m.set(bx0, d, z, "minecraft:cobblestone")
        m.set(bx1, d, z, "minecraft:cobblestone")
    m.clear(bx0 + 1, bx1 - 1, d, top, bz0 + 1, bz1 - 1)
    m.roof(bx0, bx1, bz0, bz1, top, "x", WOOD, fill="minecraft:spruce_planks", overhang=1)
    mid = (bx0 + bx1) // 2
    m.box(mid - 1, mid + 1, d, d + 2, dz, dz, "minecraft:air")
    m.set(mid - 1, g, dz, "minecraft:cobblestone")
    m.set(mid, g, dz, "minecraft:cobblestone")
    m.set(mid + 1, g, dz, "minecraft:cobblestone")
    # hay in the bays either side of the threshing floor, lamps on the posts
    for x in (bx0 + 1, bx1 - 1):
        for z in range(bz0 + 1, bz1):
            m.set(x, d, z, "minecraft:hay_block[axis=z]")
    for x in (bx0 + 1, bx1 - 1):
        m.set(x, d + 1, bz0 + 1, "minecraft:hay_block[axis=z]")
    for x in (bx0 + 1, bx1 - 1):
        for z in range(bz0 + 2, bz1, 2):
            m.set(x, d + 1, z, lantern())
    part(m, bx0, bx1, bz0, bz1, "barn")
    # the yard: cobbles before the doors, a cart and a woodpile
    yz = range(1, bz0) if side == "north" else range(bz1 + 1, D + 1)
    for z in yz:
        for x in range(1, W + 1):
            m.set(x, g, z, "minecraft:cobblestone" if (x + z) % 3 else "minecraft:gravel")
    yl = list(yz)
    cz = yl[len(yl) // 2]
    m.set(2, d, cz, stairs(WOOD, "east", "top"))
    m.set(3, d, cz, stairs(WOOD, "west", "top"))
    for x in (W - 2, W - 1):
        m.set(x, d, cz, pillar("minecraft:oak_log", "z"))
    lamp_post(m, 1, yl[0], d)
    lamp_post(m, W, yl[0], d)
    part(m, 1, W, max(yl[0], 2), min(yl[-1], D - 1), "barn-yard")
    for z in range(1, D + 1):
        for x in (1, 2, W - 1, W):
            if bz0 <= z <= bz1 and 1 < z < D:
                part(m, x, x, z, z, "barn-yard")


def goat_pen(m, W, D, d, g):
    """Kettil's goat pen on the main street (the festival day's task B): the
    street is its west edge (x 1, kept clear), a fence round a yard of trodden
    earth with a field gate to the street, the lean-to and hay rack in the far
    corner, a trough, and the latch on the gatepost by the street."""
    ground(m, W, D, g, "minecraft:coarse_dirt")
    for z in range(1, D + 1):
        m.set(1, g, z, "minecraft:dirt_path")
    x0, x1, z0, z1 = 3, W - 1, 1, D
    # the gate faces the stretch of street the pen's seam opens on: its south end
    gz = z1 - 2
    for x in range(x0, x1 + 1):
        for z in (z0, z1):
            m.set(x, d, z, fence(WOOD))
    for z in range(z0, z1 + 1):
        for x in (x0, x1):
            m.set(x, d, z, fence(WOOD))
    # the gate to the street, two leaves, left open for the goats to come in
    for z in (gz, gz + 1):
        m.set(x0, d, z, fence_gate(WOOD, "east", open=True))
    # the lean-to in the far north-east corner, one clear column off the fence
    for (x, z) in ((x1 - 4, z0 + 2), (x1 - 2, z0 + 2)):
        for y in (d, d + 1, d + 2):
            m.set(x, y, z, fence(WOOD))
    for x in range(x1 - 4, x1):
        for z in range(z0 + 1, z0 + 3):
            m.set(x, d + 3, z, slab(WOOD, "bottom"))
    m.set(x1 - 3, d + 2, z0 + 1, lantern(hanging=True))
    # the hay up on the lean-to's rack under its roof, out of a goat's reach: a bale on the
    # ground beside the fence is a step a goat climbs to jump the fence
    m.set(x1 - 2, d + 2, z0 + 1, "minecraft:hay_block[axis=x]")
    # the trough in the open yard, three cells clear of every fence for the same reason
    m.set(x0 + 3, d, (z0 + z1) // 2, "minecraft:water_cauldron[level=3]")
    m.part(x1 - 4, x1 - 1, z0 + 1, z0 + 2, "lean-to")
    # lamps: one on the street side, one in the pen's corner by the gate, so the pen reads at night
    lamp_post(m, 2, z0, d)
    # the second defence line's supply chest on the street side of the fence, a hay bale for cover
    m.set(2, d, z0 + 2, "minecraft:chest[facing=west,type=single,waterlogged=false]")
    m.set(2, d, z0 + 3, "minecraft:hay_block[axis=y]")
    lamp_post(m, x0 + 1, z1 - 1, d)
    for x in range(x0 + 1, x1):
        for z in range(z0 + 1, z1):
            if not (x1 - 4 <= x <= x1 - 1 and z0 + 1 <= z <= z0 + 2) and (x, z) not in LAMPS:
                m.part(x, x, z, z, "pen")
    # a lamp post's head is seen, never stood on: the lean-to's part holds it
    for (x, z) in sorted(LAMPS):
        m.part(x, x, z, z, "lean-to")
    return gz


def net_green(m, W, D, d, g):
    """The fishermen's drying green west of the cliff path (its east edge, x W,
    kept clear): net poles with lines strung between them, an upturned boat on
    trestles, pots and barrels, and the tarred gear shed at the south end."""
    ground(m, W, D, g, "minecraft:grass_block[snowy=false]")
    for z in range(1, D + 1):
        m.set(W, g, z, "minecraft:coarse_dirt" if z % 3 else "minecraft:gravel")
    # the net poles: two rows down the green, a line of chain between each pair
    for z in range(3, D - 8, 4):
        for x in (2, 4):
            for y in (d, d + 1, d + 2):
                m.set(x, y, z, fence(WOOD))
        m.set(3, d + 2, z, "minecraft:iron_chain[axis=x,waterlogged=false]")
    # the upturned boat on its trestles, halfway down
    bz = D - 9
    for x in (2, 3, 4):
        m.set(x, d, bz, fence(WOOD))
        m.set(x, d, bz + 3, fence(WOOD))
    for z in range(bz, bz + 4):
        m.set(2, d + 1, z, stairs(WOOD, "west", "top"))
        m.set(3, d + 1, z, "minecraft:spruce_planks")
        m.set(4, d + 1, z, stairs(WOOD, "east", "top"))
    # pots and barrels along the west edge
    for z in (2, 6, 10):
        m.set(1, d, z, "minecraft:barrel[facing=up,open=false]")
    # the tarred gear shed at the south end, its door to the path
    sx0, sx1, sz0, sz1 = 1, W - 3, D - 4, D
    m.hollow(sx0, sx1, d, d + 2, sz0, sz1, "minecraft:dark_oak_planks")
    m.clear(sx0 + 1, sx1 - 1, d, d + 2, sz0 + 1, sz1 - 1)
    m.box(sx0, sx1, d + 3, d + 3, sz0, sz1, slab("dark_oak", "bottom"))
    m.set(sx1, d, sz0 + 2, "minecraft:air")
    m.set(sx1, d + 1, sz0 + 2, "minecraft:air")
    m.set(sx0 + 1, d + 2, sz0 + 1, lantern(hanging=True))
    m.set(sx0 + 1, d, sz1 - 1, "minecraft:barrel[facing=up,open=false]")
    m.part(sx0, sx1, sz0, sz1, "shed")
    lamp_post(m, 1, bz - 2, d)
    lamp_post(m, 1, 1, d)
    for x in range(1, W - 1):
        for z in range(1, sz0):
            if (x, z) not in LAMPS:
                m.part(x, x, z, z, "green")


def beacon_point(m, W, D, d, g):
    """The headland's point east of the cliff path (its west edge, x 1, kept
    clear): the beacon's raised stone platform with its fire basket, benches to
    the sea, the flagpole, flowers."""
    ground(m, W, D, g, "minecraft:grass_block[snowy=false]")
    for z in range(1, D + 1):
        m.set(1, g, z, "minecraft:coarse_dirt" if z % 2 else "minecraft:gravel")
    cx, cz = W // 2 + 2, D // 2
    px0, px1, pz0, pz1 = cx - 3, cx + 3, cz - 3, cz + 3
    # the platform, one course up, a stair up on its west side
    m.box(px0, px1, d, d, pz0, pz1, "minecraft:stone_bricks")
    for z in (cz - 1, cz, cz + 1):
        m.set(px0 - 1, d, z, stairs("stone_brick", "east"))
    # the iron fire basket on its plinth in the middle, lit for the festival
    m.set(cx, d + 1, cz, "minecraft:chiseled_stone_bricks")
    m.set(cx, d + 2, cz, "minecraft:campfire[facing=north,lit=true,signal_fire=false,waterlogged=false]")
    for (x, z) in ((cx - 1, cz), (cx + 1, cz), (cx, cz - 1), (cx, cz + 1)):
        m.set(x, d + 1, z, "minecraft:iron_bars[east=false,north=false,south=false,waterlogged=false,west=false]")
    # lanterns at the platform's corners
    for (x, z) in ((px0, pz0), (px1, pz0), (px0, pz1), (px1, pz1)):
        m.set(x, d + 1, z, lantern())
    # benches looking out to sea (east), the flagpole, flower beds
    for z in (2, 3, D - 2, D - 1):
        m.set(W - 1, d, z, stairs(WOOD, "west"))
    for y in range(d, d + 5):
        m.set(W - 2, y, cz, fence(WOOD))
    m.set(W - 2, d + 5, cz, "minecraft:white_wool")
    for x in range(3, W - 3, 2):
        m.set(x, d, 1, "minecraft:poppy" if x % 4 == 1 else "minecraft:cornflower")
        m.set(x, d, D, "minecraft:oxeye_daisy" if x % 4 == 1 else "minecraft:dandelion")
    # lanterns set on the grass along the path side, so the point reads at night
    for z in (3, cz, D - 2):
        m.set(4, d, z, lantern())
    m.part(px0 - 1, px1, pz0, pz1, "beacon")
    m.part(W - 2, W - 2, cz, cz, "beacon")
    for x in range(3, W + 1):
        for z in range(1, D + 1):
            if (x, z) not in LAMPS and not (px0 - 1 <= x <= px1 and pz0 <= z <= pz1) and (x, z) != (W - 2, cz):
                m.part(x, x, z, z, "point")


def salvage_depths(W, D):
    """The salvage ground's water depth per column, 0 (a sand crest at the surface) to 8 (the
    open sea's floor), after the owner's approved reference (`design/reference/salvage-ground`):
    a band of open deep water from the cove, then one irregular shallow patch where curving
    sandbars break the surface, the water shading from pale turquoise over the sand to the deep
    blue, a curving broken outer bar on the seaward side with a gap and a channel at its west
    end. Every flank shelves at about a block for every two across; no edge runs straight (the
    coordinates are warped by a smooth noise before the bars are measured). Returns
    (depth, crest)."""
    import math

    def n(x, z, salt):
        return (math.sin(x * 0.11 + salt) * 0.45 + math.sin(z * 0.13 + salt * 1.7) * 0.35
                + math.sin((x + z) * 0.07 + salt * 0.6) * 0.2 + math.sin((x - z) * 0.23 + salt * 2.3) * 0.15)
    BAND = 24
    OX = (W - 150) // 2
    BARS = [
        [(14, 40, 2.5), (24, 34, 3.5), (36, 33, 3.0), (46, 36, 2.0)],
        [(58, 38, 1.5), (70, 33, 3.0), (86, 31, 3.5), (100, 35, 2.5), (110, 41, 1.5)],
        [(118, 38, 2.0), (126, 35, 3.0), (134, 39, 2.0)],
        [(30, 58, 2.0), (44, 52, 3.5), (58, 52, 4.0), (70, 58, 2.5), (76, 66, 1.5)],
        [(92, 56, 2.0), (104, 52, 3.0), (116, 56, 3.5), (124, 64, 2.5)],
        [(10, 64, 2.5), (14, 78, 3.5), (22, 90, 2.5)],
        [(40, 80, 2.0), (52, 84, 3.0), (60, 80, 2.0)],
        [(96, 80, 2.0), (106, 78, 3.0), (116, 84, 2.0)],
        # the outer bar, broken in two, the channel at its west end
        [(34, 106, 2.0), (48, 110, 3.5), (64, 112, 3.5), (76, 110, 2.0)],
        [(86, 109, 2.0), (98, 106, 3.5), (112, 101, 3.0), (124, 94, 2.5), (132, 84, 2.0)],
    ]
    BARS = [[(x + OX, z, r) for (x, z, r) in bar] for bar in BARS]

    def seg_dist(px, pz, a, b):
        ax, az, ar = a
        bx, bz, br = b
        vx, vz = bx - ax, bz - az
        L2 = vx * vx + vz * vz
        t = max(0.0, min(1.0, ((px - ax) * vx + (pz - az) * vz) / L2)) if L2 else 0.0
        return math.hypot(px - (ax + t * vx), pz - (az + t * vz)) - (ar + t * (br - ar))

    cx, cz = W / 2 + 2, BAND + (D - BAND) * 0.5
    ax, az = 65, (D - BAND) / 2 - 7
    depth, crest = {}, set()
    for z in range(1, D + 1):
        for x in range(1, W + 1):
            wx = x + 3.0 * n(x, z, 1.3)
            wz = z + 3.0 * n(z, x, 4.1)
            db = min(seg_dist(wx, wz, bar[i], bar[i + 1]) for bar in BARS for i in range(len(bar) - 1))
            th = math.atan2((wz - cz) / az, (wx - cx) / ax)
            rr = 1.0 + 0.10 * math.sin(3 * th + 0.7) + 0.06 * math.sin(5 * th + 2.1) + 0.04 * math.sin(8 * th + 4.0)
            e = (math.hypot((wx - cx) / ax, (wz - cz) / az) - rr) * min(ax, az)
            base = 2.0 + 1.2 * (n(x * 1.3, z * 1.3, 9.9) + 1)
            env = base if e < 0 else base + e / 1.3
            dep = 0 if db <= 0 else 1 + db / (1.8 + 0.8 * (n(x, z, 2.2) + 1) / 2)
            dep = min(dep, env, 8.0)
            edge = min(x - 1, W - x, z - 1, D - z)
            dep = max(dep, 8.0 - edge * 0.6)
            depth[(x, z)] = max(0, min(8, int(round(dep))))
            if depth[(x, z)] == 0:
                crest.add((x, z))
    return depth, crest


SALVAGE_CRATES = [(40, 46), (72, 84), (114, 46), (100, 92), (56, 126), (124, 112)]   # 5 and 6 past the outer bar


def bay(m, W, D, d, g, place, field=False):
    """The water task A is rowed on, drawn as the sea itself: a place two courses tall with
    its sides open, its lower course the sea's surface and water through, over the seabed as
    the whole lays it (the allocation's ground columns), so no rim, wall or cut shows.

    `node/bay` is the natural cove below the quay: open water, the quay's steps down into
    it and Sverre's two boats at their foot. `node/shoals` (field) is the salvage ground out
    past a band of open deep water, drawn to the owner's approved reference
    (`salvage_depths`): the six crates float in the channels between the sandbars, two out
    past the outer bar. Returns the marks."""
    WATER = "minecraft:water[level=0]"
    top = {}
    gr = place.a.get("ground") or {}
    for c in gr.get("columns", []):
        top[(c["x"], c["z"])] = c["top"]
    marks = {}
    if not field:
        for z in range(1, D + 1):
            for x in range(1, W + 1):
                t = top.get((x, z), g - 3)
                for y in range(min(t + 1, g), g + 1):
                    m.set(x, y, z, WATER)
        # the quay's steps come down into the cove where the seam meets it: a flight of
        # sandstone from under the seam's opening to the water's edge
        for s in place.a.get("seams", []):
            if s["edge"] != "edge/quay-to-bay":
                continue
            if any(ps["seam"]["edge"] == s["edge"] and ps.get("approach") and ps["approach"]["ladder"] for ps in place.seams):
                m.climbs_to(s["edge"])
            (x0, y0, z0), (x1, y1, z1) = s["cells"]
            for x in range(x0, x1 + 1):
                for k, y in enumerate(range(y0 - 1, g, -1)):
                    z = z0 + k
                    if z > D:
                        break
                    m.set(x, y, z, "minecraft:sandstone")
                    if k:
                        for yy in range(y + 1, y0 + 3):
                            m.set(x, yy, z, "~air")
        # the boats ride off the foot of the quay's step, a row out from the kerb's ledge
        marks["slip-1"] = (9, 3, g)
        marks["slip-2"] = (12, 2, g)
        marks["node-bay"] = (15, 15, None)
        return marks
    depth, crest = salvage_depths(W, D)
    for z in range(1, D + 1):
        for x in range(1, W + 1):
            t = top.get((x, z), g - 8)
            if t >= g:
                continue                       # the coast's own ground
            s_top = g - depth[(x, z)]
            if s_top > t:
                for y in range(t + 1, s_top + 1):
                    m.set(x, y, z, "minecraft:sand")
            for y in range(max(t, s_top) + 1, g + 1):
                m.set(x, y, z, WATER)
    for (x, z) in sorted(crest):
        if top.get((x, z), g - 8) < g:
            m.part(x, x, z, z, "shoals")
    # the feast's six crates are barrels afloat in the channels, a cell above the water and
    # touching it, each opened from the boat: two cells of open water on every side
    OX = (W - 150) // 2

    def open_water(x, z):
        if not (3 <= x <= W - 2 and 3 <= z <= D - 2):
            return False
        return all(depth[(x + dx, z + dz)] >= 1 and top.get((x + dx, z + dz), g - 8) < g - 1
                   for dx in (-2, -1, 0, 1, 2) for dz in (-2, -1, 0, 1, 2))
    for k, (tx, tz) in enumerate(SALVAGE_CRATES):
        cx, cz = tx + OX, tz
        best = None
        for r in range(0, 12):
            for dz in range(-r, r + 1):
                for dx in range(-r, r + 1):
                    if best is None and max(abs(dx), abs(dz)) == r and open_water(cx + dx, cz + dz):
                        best = (cx + dx, cz + dz)
            if best:
                break
        assert best is not None, f"no open water for crate {k + 1}"
        m.set(best[0], g + 1, best[1], "minecraft:barrel[facing=up,open=false]")
        marks[f"crate-{k + 1}"] = (best[0], best[1], g + 1)
        # where the boat lies alongside to open it: the water cell beside it toward the field's middle
        sx = 1 if best[0] < W // 2 else -1
        marks[f"crate-{k + 1}-alongside"] = (best[0] + sx, best[1], g)
    marks["node-shoals"] = (W // 2, D // 2, None)
    return marks


def farm_lane(m, W, D, d, g):
    for x in range(1, W + 1):
        for z in range(1, D + 1):
            m.set(x, g, z, "minecraft:dirt_path" if z != (D + 1) // 2 or x % 4 == 0 else "minecraft:grass_block[snowy=false]")


def build(place):
    m = Model(place)
    cells = [(x, z) for x in range(place.n[0]) for z in range(place.n[2]) if place.in_space_xz(x, z)]
    # the track's seam row is the connection's, not the plot's: the play
    # space is 1..W by 1..D inside it
    W = max(c[0] for c in cells if c[0] < place.n[0] - 1)
    D = max(c[1] for c in cells if c[1] < place.n[2] - 1)
    d = place.datum.value
    g = d - 1
    stem = place.a["place"].removeprefix("node/")
    side = track_side(place)
    FREE_ROWS.clear()
    FREE_ROWS.update(({D} if stem in OLD_PLOTS else {D - 1, D}) if side == "south" else {1, 2})
    if stem in ("farm-lane", "west-track", "meadow-track", "terrace-track"):
        farm_lane(m, W, D, d, g)
    elif stem == "wheat-field":
        wheat_field(m, W, D, d, g)
    elif stem in ("orchard", "west-orchard"):
        orchard(m, W, D, d, g)
    elif stem in ("sheep-pen", "sheep-terrace"):
        pen(m, W, D, d, g, side, "minecraft:grass_block[snowy=false]", "fold", "shelter")
    elif stem == "cattle-pen":
        pen(m, W, D, d, g, side, "minecraft:coarse_dirt", "yard", "byre")
    elif stem == "pond":
        pond(m, W, D, d, g, side)
    elif stem in ("barn", "croft", "dune-cottage", "lantern-yard", "terrace-cottage"):
        barn(m, W, D, d, g, side)
        if stem == "lantern-yard":
            # finished lanterns set out along the yard's far edge to be looked over
            yz = D if side == "north" else 1
            for x in range(4, W - 2, 3):
                m.set(x, d, yz, "minecraft:spruce_slab[type=top,waterlogged=false]")
                m.set(x, d + 1, yz, lantern())
    elif stem == "butts":
        butts(m, W, D, d, g, side)
    elif stem in ("allotments", "kitchen-garden"):
        allotments(m, W, D, d, g, side)
    elif stem == "fair-field":
        if D > 40:
            fair(m, W, 30, d, g, side)
            for x in range(1, W + 1):
                for z in range(31, D + 1):
                    m.set(x, g, z, "minecraft:grass_block[snowy=false]")
            picnic(m, W, 31, D - 1, d, g)
            part(m, 1, W, 30, D - 1, "fair")
        else:
            fair(m, W, D, d, g, side)
    elif stem == "bonfire-green":
        bonfire(m, W, D, d, g, side)
    elif stem == "bee-meadow":
        bees(m, W, D, d, g, side)
    elif stem == "cathedral-garden":
        garden(m, W, D, d, g, side)
    elif stem == "games-yard":
        games(m, W, D, d, g, side)
    elif stem == "net-green":
        net_green(m, W, D, d, g)
    elif stem == "beacon-point":
        beacon_point(m, W, D, d, g)
    elif stem in ("bay", "shoals"):
        for name, (x, z, y) in bay(m, W, D, d, g, place, field=(stem == "shoals")).items():
            m.mark(name, x, z, facing="south", y=y)
        m.finish()
        return m
    elif stem == "goat-pen":
        gz = goat_pen(m, W, D, d, g)
        # the latch: on the street before the gatepost, where a body stands to drop it
        m.mark("goat-pen-gate", 2, gz - 1, facing="east")
        m.mark("supply-pen", 2, 3, facing="west", y=d)
        m.mark("node-goat-pen", (W + 4) // 2, gz, facing="west")
        # the middle of the yard inside the fence (x 4..W-2, z 2..D-1): the goats' census box
        m.mark("goat-pen-yard", (4 + W - 2) // 2, (2 + D - 1) // 2, facing="west")
        m.finish()
        return m
    else:
        sys.exit(f"farm.py: no drawing for {stem}")
    m.mark(f"node-{stem}", *(free_mark(m, W, D, d) if stem not in ("barn", "croft", "dune-cottage", "lantern-yard", "terrace-cottage") else yard_mark(m, W, D, d, side)), facing="south")
    m.finish()
    return m


def yard_mark(m, W, D, d, side):
    """The barn's mark: in the yard before its doors, where the party arrives."""
    z = 3 if side == "north" else D - 2
    return (W + 1) // 2, z


def free_mark(m, W, D, d):
    cx, cz = (W + 1) // 2, (D + 1) // 2
    for r in range(0, max(W, D)):
        for x in range(cx - r, cx + r + 1):
            for z in range(cz - r, cz + r + 1):
                if 1 <= x <= W and 1 <= z <= D and m.get(x, d, z) in (None, "minecraft:air") \
                        and m.get(x, d + 1, z) in (None, "minecraft:air") and m.get(x, d - 1, z) not in ("minecraft:water",) \
                        and True:
                    return x, z
    sys.exit("farm.py: no free cell for the node's mark")


raise SystemExit(run(build, reason="the barn's and the shelters' roofs, the hay stacks and the fence tops: seen, never stood on"))
