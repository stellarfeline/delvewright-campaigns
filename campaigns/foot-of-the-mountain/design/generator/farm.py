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


def track_side(place):
    """The side of the plot the farm track runs along: south for the plots north of it."""
    for s in place.seams:
        if "farm-lane" in s["stem"]:
            return s["seam"]["face"]
    return None


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
    m.set(x0 + 3, d, fz + 1, "minecraft:hay_block[axis=x]")
    m.set(x0 + 4, d, fz + 1, "minecraft:hay_block[axis=x]")
    m.set(x0 + 3, d + 1, fz + 1, lantern())
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
    FREE_ROWS.update({D} if side == "south" else {1, 2})
    if stem == "farm-lane":
        farm_lane(m, W, D, d, g)
    elif stem == "wheat-field":
        wheat_field(m, W, D, d, g)
    elif stem == "orchard":
        orchard(m, W, D, d, g)
    elif stem == "sheep-pen":
        pen(m, W, D, d, g, side, "minecraft:grass_block[snowy=false]", "fold", "shelter")
    elif stem == "cattle-pen":
        pen(m, W, D, d, g, side, "minecraft:coarse_dirt", "yard", "byre")
    elif stem == "pond":
        pond(m, W, D, d, g, side)
    elif stem == "barn":
        barn(m, W, D, d, g, side)
    else:
        sys.exit(f"farm.py: no drawing for {stem}")
    m.mark(f"node-{stem}", *(free_mark(m, W, D, d) if stem != "barn" else yard_mark(m, W, D, d, side)), facing="south")
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
