#!/usr/bin/env python3
"""The town's streets, flights, lanes and square: one generator, read off each
place's allocation.

    DELVEWRIGHT_SKILL=<skill> python3 street.py --allocation <delvec allocation ... node/<street>> \\
        --out ../../../programs/<street>.json --delvec <delvec>

Form, after the medieval town street (cobbles of field and river stone set in
sand, a central kennel the rain runs down, the paving re-laid and worn in
patches; Brasenose Lane's kennel, Viljandi's Sepa street) and the stepped
street of a harbour town (Clovelly's cobbled main street falling to the
pier, broken by steps and side alleys):

- a stretch is cobbled, its kennel of dressed stone wandering a cell either
  side of the middle and broken where the paving was re-laid, a band of setts
  where each flight lands, the centre worn in patches; its verge either side,
  worn into the ground, holds lamps, benches, barrels, a cart and beds of
  flowers clear of the lots' fronts, and before the guildhall a market of
  stalls; a lane is cobbled with its kennel and setts laid flush (the kerb is
  in the paving, never at its edge); no line shows where a box ends;
- a flight carries the street down two courses in half-steps of stone, a
  landing at its foot;
- the square is paved in setts round a covered well, two trees with benches
  under them, a market stall, lamps at its corners;
- a lamp post (an oak post, a lantern on it) at the foot of every flight, side
  alternating (a stretch's edges are all doorways), and along the lanes; a cart, barrels, a bench where no
  doorway or opening needs the ground.

Nothing stands in a way's clear width, nor beside any opening a neighbour
crosses. Piece-local axes: +x east, +z south; y 0 the ground course, y 1 the
walk plane. Drawn on the skill starter's Model; the engine says where a body goes.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from starter import Model, fence, lantern, leaves, run, slab, stairs, wall  # noqa: E402
from starter import pillar as log  # noqa: E402

COBBLE = [{"weight": 7, "block": "minecraft:cobblestone"},
          {"weight": 3, "block": "minecraft:stone"},
          {"weight": 2, "block": "minecraft:andesite"},
          {"weight": 1, "block": "minecraft:mossy_cobblestone"},
          {"weight": 1, "block": "minecraft:tuff"}]
WORN = [{"weight": 4, "block": "minecraft:cobblestone"},
        {"weight": 3, "block": "minecraft:coarse_dirt"},
        {"weight": 2, "block": "minecraft:tuff"},
        {"weight": 3, "block": "minecraft:grass_block[snowy=false]"},
        {"weight": 1, "block": "minecraft:mossy_cobblestone"},
        {"weight": 1, "block": "minecraft:packed_mud"}]
SETTS = [{"weight": 6, "block": "minecraft:stone_bricks"},
         {"weight": 2, "block": "minecraft:cracked_stone_bricks"},
         {"weight": 1, "block": "minecraft:mossy_stone_bricks"}]
SQUARE = [{"weight": 5, "block": "minecraft:stone_bricks"},
          {"weight": 3, "block": "minecraft:polished_andesite"},
          {"weight": 2, "block": "minecraft:cobblestone"},
          {"weight": 1, "block": "minecraft:cracked_stone_bricks"},
          {"weight": 1, "block": "minecraft:mossy_cobblestone"}]
KENNEL = "minecraft:polished_andesite"
STEP = "minecraft:stone_brick"
POST = "minecraft:oak_fence"


def palette(m):
    m.palette.update({"floor": WORN, "cobble": COBBLE, "worn": WORN, "setts": SETTS, "square": SQUARE,
                      "kennel": KENNEL, "road": ROAD, "trodden": TRODDEN})


def seam_cols(place):
    """Every column a neighbour's opening stands in or touches: furniture keeps off."""
    out = set()
    for s in place.seams:
        lo, hi = [b.value for b in s["lo"]], [b.value for b in s["hi"]]
        for x in range(lo[0] - 1, hi[0] + 1):
            for z in range(lo[2] - 1, hi[2] + 1):
                out.add((x, z))
    return out


# the trades whose fronts stand on the street, and the wood of the sign each hangs
SIGNS = {"node/bakery": "spruce", "node/apothecary": "birch", "node/merchant": "dark_oak",
         "node/weaver": "cherry", "node/tavern": "oak", "node/smithy": "spruce",
         "node/chandler": "birch", "node/fishmonger": "mangrove", "node/netloft": "oak"}
# which way a sign hung before a front on each face looks: back at the street
SIGN_ROT = {"west": 12, "east": 4, "north": 0, "south": 8}


def bracket(m, place, s, top):
    """A shop sign on the street's own bracket, before a front's doorway: an oak
    post in the verge beside the doorway, a stripped log beam in the top course
    from the post over the doorway's first column, and the trade's hanging sign
    under the beam, a course above any head. Post, beam and sign are the
    street's blocks, so the sign hangs on nothing another piece places.
    Returns the columns it takes, or None where the doorway has no room beside it."""
    seam = s["seam"]
    face, wood = seam["face"], SIGNS.get(seam["other"])
    if wood is None:
        return None
    (lx, _, lz), (hx, _, hz) = seam["cells"]
    (x0, _, z0), (x1, _, z1) = place.space
    if face in ("west", "east"):
        u = lx + 1 if face == "west" else lx - 1
        lo, hi, amin, amax = lz, hz, z0 + 2, z1 - 2
        cell = lambda a: (u, a)                      # noqa: E731
        axis = "z"
    else:
        u = lz + 1 if face == "north" else lz - 1
        lo, hi, amin, amax = lx, hx, x0 + 2, x1 - 2
        cell = lambda a: (a, u)                      # noqa: E731
        axis = "x"
    if lo - 1 >= amin:
        post, hang = lo - 1, lo
    elif hi + 1 <= amax:
        post, hang = hi + 1, hi
    else:
        return None
    px, pz = cell(post)
    sx, sz = cell(hang)
    for y in range(1, top):
        m.set(px, y, pz, fence("minecraft:oak"))
    for x, z in ((px, pz), (sx, sz)):
        m.set(x, top, z, f"minecraft:stripped_spruce_log[axis={axis}]")
    m.set(sx, top - 1, sz, f"minecraft:{wood}_hanging_sign[attached=false,rotation={SIGN_ROT[face]},waterlogged=false]")
    # the sign's own cell, named for the trade: the campaign's `signs` entry
    # writes the trade's name on it
    m.mark(f"sign-{seam['other'].removeprefix('node/')}", sx, sz, y=top - 1)
    return {(px, pz), (sx, sz)}


def lamp(m, x, z, y=1):
    for dy in (0, 1, 2):
        m.set(x, y + dy, z, fence("minecraft:oak"))
    m.set(x, y + 3, z, lantern(False))


def pave_way(m, x0, x1, z0, z1, axis):
    """A street or a lane: cobble across, a kennel down the middle, setts flush
    at the way's edges, the outer column worn into the ground beyond."""
    if axis == "z":
        a0, a1, b0, b1 = z0, z1, x0, x1
    else:
        a0, a1, b0, b1 = x0, x1, z0, z1
    mid = (b0 + b1) // 2
    for a in range(a0, a1 + 1):
        for b in range(b0, b1 + 1):
            if b in (b0, b1):
                role = "worn"
            elif b == mid:
                role = "kennel"
            elif b in (b0 + 1, b1 - 1) and b1 - b0 >= 4:
                role = "setts"
            else:
                role = "cobble"
            if axis == "z":
                m.set(b, 0, a, role)
            else:
                m.set(a, 0, b, role)


def hsh(*v):
    """A fixed hash of integers into [0, 1): the street's own wear, the same on every run."""
    h = 2166136261
    for x in v:
        h = ((h ^ (x & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    return (h >> 8) / float(1 << 24)


def stretch(m, place, stem):
    """A stretch of the main street: the way five wide and centred, cobbled,
    its kennel wandering a cell either side of the middle and broken where
    the paving was re-laid, a band of setts at each end where the flights
    land, the centre worn in patches; the verge either side, clear of the
    lots' fronts, holds the street's life — lamps, benches, barrels, a cart,
    beds of flowers in the worn ground — and at the guildhall a market."""
    (x0, _, z0), (x1, _, z1) = place.space
    k = int(stem.split("-")[1])
    w = x1 - x0 + 1
    c0 = x0 + (w - 5) // 2                   # the clear way: c0 .. c0 + 4
    c1 = c0 + 4
    mid = (c0 + c1) // 2
    for z in range(z0, z1 + 1):
        band = z in (z0, z0 + 1, z1 - 1, z1)    # where the flights land
        wander = (-1, 0, 0, 1)[int(hsh(k, z // 3, 7) * 4)] if not band else 0
        broken = hsh(k, z, 11) < 0.18
        for x in range(x0, x1 + 1):
            if x < c0 or x > c1:
                role = "worn"
            elif band:
                role = "setts"
            elif x == mid + wander and not broken:
                role = "kennel"
            elif hsh(k, x, z, 3) < 0.22:
                role = "worn" if hsh(k, x, z, 5) < 0.4 else "setts"
            else:
                role = "cobble"
            m.set(x, 0, z, role)
    keep = seam_cols(place)
    # a front's doorway: its sign on the street's bracket, and the verge in
    # front of the doorway kept clear for the way in
    for s in place.seams:
        if s["seam"]["other"] not in SIGNS:
            continue
        took = bracket(m, place, s, m.ey - 1)
        if took:
            keep |= took
        (lx, _, lz), (hx, _, hz) = s["seam"]["cells"]
        face = s["seam"]["face"]
        for a in range(min(lz, hz) if face in ("west", "east") else min(lx, hx),
                       (max(lz, hz) if face in ("west", "east") else max(lx, hx)) + 1):
            if face == "west":
                keep.add((lx + 1, a))
            elif face == "east":
                keep.add((lx - 1, a))
            elif face == "north":
                keep.add((a, lz + 1))
            else:
                keep.add((a, lz - 1))
    # the verge's own columns, off the lots' fronts and off the way
    lanes = [x for x in range(x0, x1 + 1) if (x < c0 or x > c1)]
    free = {(x, z) for x in lanes for z in range(z0 + 2, z1 - 1) if (x, z) not in keep}
    if k == 4:
        market(m, free, c0, c1, z0, z1)
        return
    things = ("lamp", "bed", "bench", "barrel", "cart", "bed", "lamp", "bench")
    i = 0
    for z in range(z0 + 2, z1 - 1, 3):
        for side, x in enumerate((c0 - 1, c1 + 1)):
            if (x, z) not in free:
                continue
            kind = things[(i + k + side * 3) % len(things)]
            i += 1
            if kind == "lamp":
                lamp(m, x, z)
            elif kind == "bed":
                m.set(x, 0, z, "minecraft:grass_block[snowy=false]")
                m.set(x, 1, z, ("minecraft:poppy", "minecraft:cornflower", "minecraft:oxeye_daisy",
                                "minecraft:allium", "minecraft:dandelion")[(k + z) % 5])
                if (x, z + 1) in free:
                    m.set(x, 0, z + 1, "minecraft:grass_block[snowy=false]")
                    m.set(x, 1, z + 1, "minecraft:short_grass")
            elif kind == "bench":
                face = "west" if x < c0 else "east"     # its back to the lot, facing the way
                m.set(x, 1, z, stairs("minecraft:spruce", face))
                if (x, z + 1) in free:
                    m.set(x, 1, z + 1, stairs("minecraft:spruce", face))
            elif kind == "barrel":
                m.set(x, 1, z, "minecraft:barrel[facing=up,open=false]")
            elif kind == "cart" and (x, z + 1) in free:
                m.set(x, 1, z, slab("minecraft:spruce", "top")); m.set(x, 1, z + 1, slab("minecraft:spruce", "top"))
                m.set(x, 2, z, "minecraft:hay_block[axis=z]")


def market(m, free, c0, c1, z0, z1):
    """The market before the guildhall: stalls under striped awnings along both
    verges, crates and a barrel between them, lamps at the market's ends."""
    cols = sorted({x for x, _ in free})
    left = [x for x in cols if x < c0]
    right = [x for x in cols if x > c1]
    colours = ("red", "yellow", "blue", "green")
    n = 0
    for side in (left, right):
        if not side:
            continue
        inner = max(side) if side is left else min(side)
        for z in range(z0 + 2, z1 - 1, 4):
            span = [zz for zz in range(z, z + 3) if all((x, zz) in free for x in side)]
            if len(span) < 2:
                continue
            col = colours[n % len(colours)]
            n += 1
            for zz in span:
                m.set(inner, 1, zz, slab("minecraft:spruce", "top"))
                for x in side:
                    m.set(x, 4, zz, f"minecraft:{col}_wool" if zz % 2 else "minecraft:white_wool")
            for zz in (span[0], span[-1]):
                for y in (1, 2, 3):
                    for x in side:
                        if x != inner:
                            m.set(x, y, zz, fence("minecraft:spruce"))
            m.set(inner, 2, span[0], "minecraft:potted_red_tulip" if n % 2 else "minecraft:potted_dandelion")
            m.set(inner, 2, span[-1], "minecraft:hay_block[axis=z]" if n % 3 else "minecraft:melon")
    for x in (left[:1] + right[-1:]):
        for z in (z0 + 2, z1 - 2):
            if (x, z) in free and m.get(x, 1, z) is None:
                lamp(m, x, z)


def flight(m, place, stem):
    """Two courses down in half-steps, the top landing at the opening above,
    the foot landing at the street below."""
    (x0, _, z0), (x1, _, z1) = place.space
    up = [s for s in place.seams if s["seam"].get("rise", 0) > 0]
    face = up[0]["seam"]["face"] if up else "north"
    # rows counted from the top (the opening above) to the foot
    rows = list(range(z0, z1 + 1)) if face == "north" else list(range(z1, z0 - 1, -1))
    climb = "north" if face == "north" else "south"
    if up and up[0].get("approach") is not None and up[0]["approach"]["ladder"] is not None:
        m.climbs_to(up[0]["stem"])       # the steps are the way up: no ladder under the opening
    for x in range(x0, x1 + 1):
        top, half_hi, mid, half_lo = rows[0], rows[1], rows[2], rows[3]
        m.set(x, 1, top, "setts"); m.set(x, 2, top, "setts")
        m.set(x, 1, half_hi, "setts"); m.set(x, 2, half_hi, stairs(STEP, climb))
        # below the opening's landing every step is a stair block, never a
        # full block standing in the way at its walk plane (the clear width)
        m.set(x, 1, mid, stairs(STEP, climb))
        m.set(x, 1, half_lo, stairs(STEP, climb))
        for r in rows[4:]:
            m.set(x, 0, r, "worn" if x in (x0, x1) else "cobble")
        for r in rows[:4]:
            m.set(x, 0, r, "setts")
    # a lamp at the foot landing, the side alternating down the street; the
    # stretches' own edges are all doorways and openings, so the street's
    # lamps stand here, one every stretch and flight
    k = int(stem.split("-")[1])
    keep = seam_cols(place)
    lamp_x, bed_x = (x0, x1) if k % 2 else (x1, x0)
    if (lamp_x, rows[4]) not in keep:
        lamp(m, lamp_x, rows[4])
    if (bed_x, rows[4]) not in keep:
        m.set(bed_x, 0, rows[4], "minecraft:grass_block[snowy=false]")
        m.set(bed_x, 1, rows[4], ("minecraft:cornflower", "minecraft:poppy", "minecraft:allium")[k % 3])


def square(m, place):
    (x0, _, z0), (x1, _, z1) = place.space
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            edge = x in (x0, x1) or z in (z0, z1)
            m.set(x, 0, z, "worn" if edge else "square")
    keep = seam_cols(place)
    cx, cz = (x0 + x1) // 2, (z0 + z1) // 2
    # paths of setts from each way in to the well
    for s in place.seams:
        lo, hi = [b.value for b in s["lo"]], [b.value for b in s["hi"]]
        mx, mz = (lo[0] + hi[0] - 1) // 2, (lo[2] + hi[2] - 1) // 2
        mx, mz = min(max(mx, x0 + 1), x1 - 1), min(max(mz, z0 + 1), z1 - 1)
        for x in range(min(mx, cx), max(mx, cx) + 1):
            m.set(x, 0, mz, KENNEL)
        for z in range(min(mz, cz), max(mz, cz) + 1):
            m.set(cx, 0, z, KENNEL)
    # the well: a cobble curb round the water, posts, a tiled cap, a bucket chain
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            if (dx, dz) != (0, 0):
                m.set(cx + dx, 1, cz + dz, "minecraft:cobblestone_wall")
    m.set(cx, 1, cz, "minecraft:water_cauldron[level=3]")
    for dx, dz in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        m.set(cx + dx, 2, cz + dz, fence("minecraft:spruce")); m.set(cx + dx, 3, cz + dz, fence("minecraft:spruce"))
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            m.set(cx + dx, 4, cz + dz, slab("minecraft:deepslate_tile"))
    m.set(cx, 4, cz, "minecraft:deepslate_tiles")
    m.set(cx, 3, cz, "minecraft:iron_chain[axis=y,waterlogged=false]")
    # two trees, benches round them
    for (tx, tz) in ((x0 + 6, z0 + 6), (x1 - 6, z1 - 6)):
        if any((tx + dx, tz + dz) in keep for dx in range(-3, 4) for dz in range(-3, 4)):
            continue
        m.set(tx, 0, tz, "minecraft:grass_block[snowy=false]")
        for y in range(1, 6):
            m.set(tx, y, tz, log("minecraft:oak_log", "y"))
        for dx in range(-2, 3):
            for dz in range(-2, 3):
                for y in (5, 6, 7):
                    if abs(dx) + abs(dz) + (y - 5) <= 3 and (dx, dz) != (0, 0) or (y == 7 and (dx, dz) == (0, 0)):
                        m.set(tx + dx, y, tz + dz, leaves("minecraft:oak"))
        m.set(tx, 1, tz + 2, stairs("minecraft:spruce", "north")); m.set(tx + 1, 1, tz + 2, stairs("minecraft:spruce", "north"))
        m.set(tx - 2, 1, tz, stairs("minecraft:spruce", "east")); m.set(tx - 2, 1, tz - 1, stairs("minecraft:spruce", "east"))
    # a market stall on the square's north side: a counter under a striped awning
    sx, sz = x0 + 4, z0 + 3
    if not any((sx + dx, sz + dz) in keep for dx in range(-1, 5) for dz in range(-1, 3)):
        for dx in range(4):
            m.set(sx + dx, 1, sz, slab("minecraft:spruce", "top"))
            m.set(sx + dx, 4, sz, "minecraft:red_wool" if dx % 2 else "minecraft:white_wool")
            m.set(sx + dx, 4, sz + 1, "minecraft:red_wool" if dx % 2 else "minecraft:white_wool")
        for dx in (0, 3):
            for y in (1, 2, 3):
                m.set(sx + dx, y, sz + 1, fence("minecraft:spruce"))
        m.set(sx + 1, 2, sz, "minecraft:hay_block[axis=x]")
        m.set(sx + 2, 2, sz, "minecraft:potted_red_tulip")
        m.set(sx - 1, 1, sz + 1, "minecraft:barrel[facing=up,open=false]")
    # lamps at the four quarters
    for (lx, lz) in ((x0 + 3, z1 - 3), (x1 - 3, z0 + 3), (cx - 4, cz + 4), (cx + 4, cz - 4)):
        if (lx, lz) not in keep and m.get(lx, 1, lz) is None:
            lamp(m, lx, lz)


def lane(m, place, stem):
    (x0, _, z0), (x1, _, z1) = place.space
    axis = "x" if (x1 - x0) >= (z1 - z0) else "z"
    pave_way(m, x0, x1, z0, z1, axis)
    keep = seam_cols(place)
    # a lane's clear width is its width less one, laid from its low edge (the
    # plan's way, centred): its verge is the high edge only
    if axis == "x":
        spots = [(x, z1) for x in range(x0 + 2, x1 - 1, 5)]
    else:
        spots = [(x1, z) for z in range(z0 + 2, z1 - 1, 5)]
    n = 0
    for i, (x, z) in enumerate(spots):
        if (x, z) in keep or m.get(x, 1, z) is not None:
            continue
        if n % 2 == 0:
            lamp(m, x, z)
        else:
            # a handcart, a barrel or a bench, in turn
            kind = (n // 2) % 3
            if kind == 0:
                m.set(x, 1, z, slab("minecraft:spruce", "top"))
                nx, nz = (x + 1, z) if axis == "x" else (x, z + 1)
                if (nx, nz) not in keep:
                    m.set(nx, 1, nz, slab("minecraft:spruce", "top"))
            elif kind == 1:
                m.set(x, 1, z, "minecraft:barrel[facing=up,open=false]")
            else:
                face = "south" if axis == "x" else "east"   # its back to the lane's edge
                m.set(x, 1, z, stairs("minecraft:spruce", face))
        n += 1


ROAD = [{"weight": 6, "block": "minecraft:cobblestone"},
        {"weight": 3, "block": "minecraft:mossy_cobblestone"},
        {"weight": 2, "block": "minecraft:andesite"},
        {"weight": 2, "block": "minecraft:stone"},
        {"weight": 1, "block": "minecraft:coarse_dirt"}]
TRODDEN = [{"weight": 5, "block": "minecraft:coarse_dirt"},
           {"weight": 3, "block": "minecraft:stone"},
           {"weight": 2, "block": "minecraft:rooted_dirt"},
           {"weight": 2, "block": "minecraft:grass_block[snowy=false]"},
           {"weight": 1, "block": "minecraft:tuff"}]
PARAPET = ("minecraft:cobblestone", "minecraft:mossy_cobblestone")


def frame(place):
    """A way's frame: (along, across, length, width, cell) — `cell(a, b)` gives
    (x, z) for row `a` along the way and column `b` across it."""
    (x0, _, z0), (x1, _, z1) = place.space
    if (x1 - x0) >= (z1 - z0):
        return list(range(x0, x1 + 1)), list(range(z0, z1 + 1)), lambda a, b: (a, b)
    return list(range(z0, z1 + 1)), list(range(x0, x1 + 1)), lambda a, b: (b, a)


def road(m, place, stem):
    """The castle road up the mountain's flank, five wide: cobbles worn and
    mossed, its clear way four, laid from its low edge, so the high edge is a
    verge carrying a low parapet broken where the hillside comes down, a lamp
    at each turn and, on the long climbs, a wayside shrine. A ramp climbs its
    four courses one step every two cells — a stair, then a landing — the
    whole width, the verge stepping with it."""
    rows, cols, cell = frame(place)
    verge = cols[-1]
    keep = seam_cols(place)
    up = [s for s in place.seams if s["seam"].get("rise", 0) > 0]
    k = int(stem.split("-")[1]) if stem.split("-")[1].isdigit() else 0
    if up:
        face = up[0]["seam"]["face"]
        top_end = {"north": rows[0], "west": rows[0], "south": rows[-1], "east": rows[-1]}[face]
        order = rows if top_end == rows[-1] else rows[::-1]      # from the foot up
        climb = face
        rise = up[0]["seam"]["rise"]
        if up[0].get("approach") is not None and up[0]["approach"]["ladder"] is not None:
            m.climbs_to(up[0]["stem"])   # the ramp is the way up: no ladder under the opening
        for i, a in enumerate(order):
            # rows 0..1 at grade; then stair, landing, stair, landing ... to the top
            if i < 2:
                h, step = 0, False
            else:
                j = i - 2
                h, step = min(j // 2 + 1, rise), (j % 2 == 0 and j // 2 + 1 <= rise)
            for b in cols:
                x, z = cell(a, b)
                m.set(x, 0, z, "road")
                for y in range(1, h):
                    m.set(x, y, z, "road")
                if h:
                    m.set(x, h, z, stairs(STEP, climb) if step else "setts")
        return
    for a in rows:
        for b in cols:
            x, z = cell(a, b)
            m.set(x, 0, z, "worn" if b == verge else "road")
    if stem == "gate-road":
        return
    n = len(rows)
    # the verge: parapet in runs, broken every few cells; a lamp at each end of a
    # leg that turns; a shrine at the middle of a long climb
    for i, a in enumerate(rows):
        x, z = cell(a, verge)
        if (x, z) in keep or i in (0, n - 1):
            continue
        if stem == "road-top" and i % 16 in (3, 4, 12):
            # under Doune's wall the verge is the terrace's edge: beds of
            # flowers in the turf, a bench facing the way
            m.set(x, 0, z, "minecraft:grass_block[snowy=false]")
            m.set(x, 1, z, ("minecraft:cornflower", "minecraft:oxeye_daisy", "minecraft:poppy",
                            "minecraft:allium")[(i // 16 + i) % 4])
        elif stem == "road-top" and i % 16 == 13:
            out = {"x": "south", "z": "east"}["x" if cell(1, 0)[1] == 0 else "z"]
            m.set(x, 1, z, stairs("minecraft:spruce", out))
        elif n >= 10 and i == n // 2 and k % 2 == 0:
            m.set(x, 1, z, "minecraft:chiseled_stone_bricks")
            m.set(x, 2, z, lantern(False))
        elif (i in (1, n - 2) and n >= 6) or (n > 20 and i % 16 == 8):
            lamp(m, x, z)
        elif hsh(k, i, 13) < 0.72:
            m.set(x, 1, z, wall(PARAPET[int(hsh(k, i, 17) * 2)]))


def cliff(m, place, stem):
    """The cliff path to the lighthouse: trodden earth and rock, its clear way
    four from the low edge, a low rail of fence along the high edge, broken at
    a bench and at every opening."""
    rows, cols, cell = frame(place)
    verge = cols[-1]
    keep = seam_cols(place)
    for i, a in enumerate(rows):
        for b in cols:
            x, z = cell(a, b)
            m.set(x, 0, z, "trodden")
        x, z = cell(a, verge)
        if (x, z) in keep or i in (0, len(rows) - 1):
            continue
        if i % 9 == 4:
            lamp(m, x, z)
        else:
            m.set(x, 1, z, fence("minecraft:spruce"))


def build(place) -> Model:
    m = Model(place)
    palette(m)
    stem = place.a["place"].removeprefix("node/")
    kind = stem.split("-")[0]
    if kind == "square":
        square(m, place)
    elif kind == "flight":
        flight(m, place, stem)
    elif kind == "street":
        stretch(m, place, stem)
    elif kind in ("road", "gate"):
        road(m, place, stem)
    elif kind == "cliff":
        cliff(m, place, stem)
    else:
        lane(m, place, stem)
    # where the place's air is low (four courses), a lamp's lantern stands in
    # its top course under the open sky: that face is meant to be seen
    if any(y == m.ey - 1 and r != "~air" for (_, y, _), r in m.v.items()):
        m.show("up")
    m.finish()
    return m


if __name__ == "__main__":
    raise SystemExit(run(build, reason="lamp tops, the well's cap and the tree crowns: seen, never stood on"))
