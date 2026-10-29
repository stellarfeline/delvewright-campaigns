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

- a stretch or a lane is cobbled across its width, a kennel of dressed stone
  down its middle and a line of setts laid flush either side of the way (the
  kerb is in the paving, never at its edge); its outer column is worn — cobble
  broken by gravel, earth and turf — so the street runs into the lots and the
  hillside with no line where its box ends;
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
from starter import Model, run  # noqa: E402
from kit import fence, lantern, leaves, log, slab, stairs  # noqa: E402

COBBLE = [{"weight": 7, "block": "minecraft:cobblestone"},
          {"weight": 3, "block": "minecraft:stone"},
          {"weight": 2, "block": "minecraft:andesite"},
          {"weight": 1, "block": "minecraft:mossy_cobblestone"},
          {"weight": 1, "block": "minecraft:gravel"}]
WORN = [{"weight": 4, "block": "minecraft:cobblestone"},
        {"weight": 3, "block": "minecraft:coarse_dirt"},
        {"weight": 2, "block": "minecraft:gravel"},
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
                      "kennel": KENNEL})


def seam_cols(place):
    """Every column a neighbour's opening stands in or touches: furniture keeps off."""
    out = set()
    for s in place.seams:
        lo, hi = [b.value for b in s["lo"]], [b.value for b in s["hi"]]
        for x in range(lo[0] - 1, hi[0] + 1):
            for z in range(lo[2] - 1, hi[2] + 1):
                out.add((x, z))
    return out


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


def stretch(m, place, stem):
    (x0, _, z0), (x1, _, z1) = place.space
    pave_way(m, x0, x1, z0, z1, "z")
    keep = seam_cols(place)
    # a lamp where the stretch's edge is free of doorways and openings
    for x in (x0, x1):
        for z in range(z0, z1 + 1):
            if (x, z) not in keep:
                lamp(m, x, z)
                return


def flight(m, place, stem):
    """Two courses down in half-steps, the top landing at the opening above,
    the foot landing at the street below."""
    (x0, _, z0), (x1, _, z1) = place.space
    up = [s for s in place.seams if s["seam"].get("rise", 0) > 0]
    face = up[0]["seam"]["face"] if up else "north"
    # rows counted from the top (the opening above) to the foot
    rows = list(range(z0, z1 + 1)) if face == "north" else list(range(z1, z0 - 1, -1))
    climb = "north" if face == "north" else "south"
    for x in range(x0, x1 + 1):
        top, half_hi, mid, half_lo = rows[0], rows[1], rows[2], rows[3]
        m.set(x, 1, top, "setts"); m.set(x, 2, top, "setts")
        m.set(x, 1, half_hi, "setts"); m.set(x, 2, half_hi, stairs(STEP, climb))
        m.set(x, 1, mid, "setts")
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
    for x in ((x0, x1) if k % 2 else (x1, x0)):
        if (x, rows[4]) not in keep and len(rows) > 4:
            lamp(m, x, rows[4])
            break


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
    if axis == "x":
        spots = [(x, z) for x in range(x0 + 2, x1 - 1, 9) for z in (z0, z1)]
    else:
        spots = [(x, z) for z in range(z0 + 2, z1 - 1, 9) for x in (x0, x1)]
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
                face = ("south" if z == z0 else "north") if axis == "x" else ("east" if x == x0 else "west")
                m.set(x, 1, z, stairs("minecraft:spruce", face))
        n += 1


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
    else:
        lane(m, place, stem)
    # PLANT: a slab where the starter's ladder hangs (its backing)
    back = {"south": (0, -1), "north": (0, 1), "east": (-1, 0), "west": (1, 0)}
    for se in place.seams:
        ap = se.get("approach")
        if ap is not None and ap.get("ladder") is not None:
            bx, bz = back[ap["ladder"]["facing"]]
            for y in range(place.datum.value, ap["sill"].value):
                m.set(ap["ladder"]["lo"][0] + bx, y, ap["ladder"]["lo"][2] + bz, slab("minecraft:spruce"))
    m.finish()
    return m


if __name__ == "__main__":
    raise SystemExit(run(build, reason="lamp tops, the well's cap and the tree crowns: seen, never stood on"))
