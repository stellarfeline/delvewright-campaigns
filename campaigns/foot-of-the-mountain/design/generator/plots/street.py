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
from starter import Model, fence, lantern, leaves, run, slab, stairs, wall  # noqa: E402
from starter import pillar as log  # noqa: E402
# the street mechanisms are the skill's (town.py, re-exported by the starter);
# what is this town's is below: its palettes, its signs, its square, its road
from starter import (flight as lay_flight, lamp, lane as lay_lane, market, ramp, rail,  # noqa: E402
                     seam_cols, square as pave_square, stretch as lay_stretch, way_frame)

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
# the street's roles, by the names the skill's ways paint
WAY = {"verge": "worn", "kennel": "kennel", "kerb": "setts", "paving": "cobble"}


def palette(m):
    m.palette.update({"floor": WORN, "cobble": COBBLE, "worn": WORN, "setts": SETTS, "square": SQUARE,
                      "kennel": KENNEL, "road": ROAD, "trodden": TRODDEN})


# the trades whose fronts stand on the street, and the wood of the sign each hangs
SIGNS = {"node/bakery": "spruce", "node/apothecary": "birch", "node/merchant": "dark_oak",
         "node/weaver": "cherry", "node/tavern": "oak", "node/smithy": "spruce",
         "node/chandler": "birch", "node/fishmonger": "mangrove", "node/netloft": "oak"}
MARKET = 4      # the stretch before the guildhall holds the market


def stretch(m, place, k):
    """A stretch of the main street, five wide and centred, its kennel wandering
    (the skill's `stretch`, seeded by the stretch's number); the fronts' signs on
    the street's brackets; the verge's life, and before the guildhall a market."""
    lay_stretch(m, place, "z", k, clear=5, roles=WAY,
                fronts={n: f"minecraft:{w}_hanging_sign" for n, w in SIGNS.items()},
                verge=market if k == MARKET else None)


def flight(m, place, k):
    """Two courses down in half-steps; a lamp at the foot landing, the side
    alternating down the street (the stretches' own edges are all doorways)."""
    lay_flight(m, place, WAY, step=STEP, lamp_side="low" if k % 2 else "high",
               flower=("minecraft:cornflower", "minecraft:poppy", "minecraft:allium")[k % 3])


def square(m, place):
    pave_square(m, place, {"verge": "worn", "paving": "square"}, path=KENNEL)
    (x0, _, z0), (x1, _, z1) = place.space
    keep = seam_cols(place)
    cx, cz = (x0 + x1) // 2, (z0 + z1) // 2
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


def lane(m, place):
    """A side street: its clear width laid from its low edge (the plan's way,
    centred), so its verge is the high edge."""
    (x0, _, z0), (x1, _, z1) = place.space
    lay_lane(m, place, "x" if (x1 - x0) >= (z1 - z0) else "z", edge="high", roles=WAY)


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


def axis_of(place):
    """A way's run, as this town's plan lays its roads and paths: the longer side."""
    (x0, _, z0), (x1, _, z1) = place.space
    return "x" if (x1 - x0) >= (z1 - z0) else "z"


def road(m, place, stem, k):
    """The castle road up the mountain's flank, five wide: cobbles worn and
    mossed, its clear way four, laid from its low edge, so the high edge is a
    verge carrying a low parapet broken where the hillside comes down, a lamp
    at each turn and, on the long climbs, a wayside shrine. A ramp climbs its
    four courses one step every two cells — a stair, then a landing — the
    whole width, the verge stepping with it."""
    axis = axis_of(place)
    if ramp(m, place, axis, WAY, step=STEP, fill="road"):
        return
    rows, cols, cell = way_frame(place, axis)
    verge = cols[-1]
    for a in rows:
        for b in cols:
            x, z = cell(a, b)
            m.set(x, 0, z, "worn" if b == verge else "road")
    if stem == "gate-road":
        return

    def special(m, i, n, x, z):
        if stem == "road-top" and i % 16 in (3, 4, 12):
            # under Doune's wall the verge is the terrace's edge: beds of
            # flowers in the turf, a bench facing the way
            m.set(x, 0, z, "minecraft:grass_block[snowy=false]")
            m.set(x, 1, z, ("minecraft:cornflower", "minecraft:oxeye_daisy", "minecraft:poppy",
                            "minecraft:allium")[(i // 16 + i) % 4])
            return True
        if stem == "road-top" and i % 16 == 13:
            out = {"x": "south", "z": "east"}["x" if cell(1, 0)[1] == 0 else "z"]
            m.set(x, 1, z, stairs("minecraft:spruce", out))
            return True
        if n >= 10 and i == n // 2 and k % 2 == 0:
            m.set(x, 1, z, "minecraft:chiseled_stone_bricks")
            m.set(x, 2, z, lantern(False))
            return True
        return False

    rail(m, place, axis, "high", k, [wall(b) for b in PARAPET],
         lamp_at=lambda i, n: (i in (1, n - 2) and n >= 6) or (n > 20 and i % 16 == 8), gap=0.28, special=special)


def cliff(m, place):
    """The cliff path to the lighthouse: trodden earth and rock, its clear way
    four from the low edge, a low rail of fence along the high edge, broken at
    a lamp and at every opening."""
    axis = axis_of(place)
    rows, cols, cell = way_frame(place, axis)
    for a in rows:
        for b in cols:
            x, z = cell(a, b)
            m.set(x, 0, z, "trodden")
    rail(m, place, axis, "high", 0, fence("minecraft:spruce"), lamp_at=lambda i, n: i % 9 == 4)


def build(place) -> Model:
    m = Model(place)
    palette(m)
    stem = place.a["place"].removeprefix("node/")
    kind = stem.split("-")[0]
    num = stem.split("-")[1] if "-" in stem else ""
    k = int(num) if num.isdigit() else 0     # this town names its stretches and flights by number
    if kind == "square":
        square(m, place)
    elif kind == "flight":
        flight(m, place, k)
    elif kind == "street":
        stretch(m, place, k)
    elif kind in ("road", "gate"):
        road(m, place, stem, k)
    elif kind == "cliff":
        cliff(m, place)
    else:
        lane(m, place)
    # where the place's air is low (four courses), a lamp's lantern stands in
    # its top course under the open sky: that face is meant to be seen
    if any(y == m.ey - 1 and r != "~air" for (_, y, _), r in m.v.items()):
        m.show("up")
    m.finish()
    return m


if __name__ == "__main__":
    raise SystemExit(run(build, reason="lamp tops, the well's cap and the tree crowns: seen, never stood on"))
