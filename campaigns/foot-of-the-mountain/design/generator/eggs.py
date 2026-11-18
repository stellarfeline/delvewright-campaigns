#!/usr/bin/env python3
"""The town's two side-story eggs: the places under the floor.

    DELVEWRIGHT_SKILL=<skill> python3 eggs.py --allocation <delvec allocation . node/<place>> \\
        --out ../../programs/<place>.json --delvec <delvec>

One generator, dispatched on the place's stem, drawn into the skill's starter:

- node/free-traders-cellar: the Kelderby Free Traders' cellar under the merchant's cloth store,
  after the smugglers' cellars under ordinary houses and the priest hole (the node's
  `references[]`): an old brick cellar with a vault faked by upside-down stairs along both long
  walls, casks two high along the north wall, sugar sacks along the south, a cask for a card table
  with candles in the middle, a coast chart and the members' ledger, the old sea door at the east
  end bricked up inside its timber frame, and the ladder up to the store in the north-west corner.
- node/nisse-hall: the terrace farm nisse's hall dug under the terrace cottage, after the nisse of Nordic
  folklore (the node's `references[]`): walls and roof of the cottage's earth, rooted and hung with
  roots, a hearth of field stones with a small fire, a table and stool at a child's knee, a box bed,
  shelves of the town's lost things, and the ladder up into the cottage's hay bay in the south-west
  corner.

Each ladder comes up the place's own column to the hole in the host's floor; the host owns the hole
and its top rung. Frame-local axes: +x east, +z south; y 0 the floor course, y 1 the walk plane;
the play space is 1..W by 1..D inside the ring.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
import starter  # noqa: E402
from starter import AIR, Model, run  # noqa: E402

# The starter's survey seeds a body only on a standable cell of a seam's opening, and a ladder's
# cells are not standable, so a room whose one way in is a ladder down from a hole in its roof is
# surveyed as reached nowhere. A body climbing down steps off at the ladder's foot: the cells beside
# the foot (piece-local, collected by `ladder_up`) are added to the survey's seeds.
FOOT_SEEDS: list = []
_ask = starter.ask_engine


def _ask_with_feet(delvec, request):
    request = dict(request, **{"from": list(request["from"]) + [c for c in FOOT_SEEDS if c not in request["from"]]})
    return _ask(delvec, request)


starter.ask_engine = _ask_with_feet

LADDER = "minecraft:ladder[facing=east,waterlogged=false]"
HANGING = "minecraft:lantern[hanging=true,waterlogged=false]"
LANTERN = "minecraft:lantern[hanging=false,waterlogged=false]"


def h(*a):
    v = 2166136261
    for n in a:
        v = ((v ^ (n & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    return v


def pick(seq, *a):
    return seq[h(*a) % len(seq)]


def shell(m, place, wall, floor, lid):
    """The frame's cells outside the play space walled, the floor course and the lid (the frame's
    top course) in the given block lists, the play space air; then the drawing is shifted so the
    play space is 1..W by 1..D, and (W, D) returned."""
    ex, ey, ez = m.ex, m.ey, m.ez
    (x0, _, z0), (x1, _, z1) = place.space
    # where the whole hands no ring on a side (a neighbour's ground owns it), the play space's own
    # edge on that side is walled
    x0, x1 = (x0 if x0 > 0 else x0 + 1), (x1 if x1 < ex - 1 else x1 - 1)
    z0, z1 = (z0 if z0 > 0 else z0 + 1), (z1 if z1 < ez - 1 else z1 - 1)
    for x in range(ex):
        for z in range(ez):
            for y in range(ey):
                ring = not (x0 <= x <= x1 and z0 <= z <= z1)
                if y == 0:
                    m.set(x, y, z, pick(floor, x, z, 1))
                elif y == ey - 1:
                    m.set(x, y, z, pick(lid, x, z, 2))
                elif ring:
                    m.set(x, y, z, pick(wall, x, y, z, 3))
                else:
                    m.set(x, y, z, AIR)
    m.shift(x0 - 1, z0 - 1)
    return x1 - x0 + 1, z1 - z0 + 1


def ladder_up(m, place, stem):
    """The ladder from the walk plane up the column under the host's hole, to the lid's course."""
    s = next(s for s in place.seams if s["stem"] == stem)
    lx, ly, lz = [b.value for b in s["lo"]]
    m.climbs_to(f"edge/{stem}")
    FOOT_SEEDS.extend([[lx + dx, 1, lz + dz] for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1))])
    lx, lz = lx - m.dx, lz - m.dz
    for y in range(1, ly + 1):   # up through the hole's own cell, to the host's top rung in its floor course
        m.set(lx, y, lz, LADDER)
    return lx, ly, lz


def landing(m, lx, ly, lz, block):
    """A stack two high beside the ladder's foot with its top open to the hole's course: a body
    climbing down the ladder can step off onto it, and the light probe, which is walked in from
    the standable cells round a seam's opening, finds one there."""
    m.set(lx + 1, 1, lz, block)
    m.set(lx + 1, 2, lz, block)
    for y in range(3, ly + 1):
        m.set(lx + 1, y, lz, AIR)


def cellar(m, place):
    """The Free Traders' working store: casks stacked along the north wall, this year's sugar
    sacks on the south, a lantern-lit table of papers in the middle, the coast chart and the
    members' ledger in the south-east corner, rope and chain hung from the vault, and the old sea
    door at the east end, its timber frame standing proud of the brick that fills it."""
    top = m.ey - 2                       # the walk courses are 1..top
    BRICK = ["minecraft:bricks"] * 5 + ["minecraft:mud_bricks", "minecraft:stone_bricks", "minecraft:cracked_stone_bricks"]
    FLOOR = ["minecraft:stone_bricks"] * 3 + ["minecraft:cracked_stone_bricks", "minecraft:cobblestone", "minecraft:mossy_stone_bricks"]
    W, D = shell(m, place, BRICK, FLOOR, ["minecraft:bricks"])
    lx, _ly, lz = ladder_up(m, place, "merchant-to-free-traders-cellar")
    # the vault: upside-down brick stairs along both long walls under the lid, a dark-oak rib
    # across it at every third bay
    for x in range(1, W + 1):
        if x not in (lx, lx + 1):
            m.set(x, top, 1, "minecraft:brick_stairs[facing=north,half=top,shape=straight,waterlogged=false]")
        m.set(x, top, D, "minecraft:brick_stairs[facing=south,half=top,shape=straight,waterlogged=false]")
    # casks stacked two and three high along the north wall, a gap where a stack was broached
    for x in range(lx + 2, W - 1):
        m.set(x, 1, 1, "minecraft:barrel[facing=south,open=false]")
        if x != 6:
            m.set(x, 2, 1, "minecraft:barrel[facing=south,open=false]")
    m.set(6, 2, 1, "minecraft:lantern[hanging=false,waterlogged=false]")
    # this year's sugar: sacks in a heap along the south wall, a coil of chain on the floor by them
    for x in range(5, W - 2):
        m.set(x, 1, D, "minecraft:white_wool")
    m.set(7, 2, D, "minecraft:white_wool")
    m.set(4, 1, D, "minecraft:iron_chain[axis=x,waterlogged=false]")
    # crates and casks heaped in the south-west corner
    for (x, y, z) in ((1, 1, D), (1, 2, D), (2, 1, D), (1, 1, D - 1)):
        m.set(x, y, z, "minecraft:barrel[facing=up,open=false]")
    # the table of papers: two casks on end, the papers spread on one, a lantern on the other;
    # a stool on its north side, Magnhild at its east end
    tz = 3
    m.set(5, 1, tz, "minecraft:barrel[facing=up,open=false]")
    m.set(6, 1, tz, "minecraft:barrel[facing=up,open=false]")
    m.set(5, 2, tz, "minecraft:lantern[hanging=false,waterlogged=false]")
    m.set(6, 2, tz, "minecraft:white_carpet")
    m.set(5, 1, tz - 1, "minecraft:spruce_slab[type=bottom,waterlogged=false]")
    m.mark("magnhild-seat", 7, tz, facing="west")
    # the coast chart, lit, and the members' ledger open on its stand, in the south-east corner
    m.set(W - 2, 1, D, "minecraft:cartography_table")
    m.set(W - 2, 2, D, "minecraft:candle[candles=2,lit=true,waterlogged=false]")
    m.set(W - 1, 1, D, "minecraft:lectern[facing=north,has_book=true,powered=false]")
    m.set(W, 1, D, "minecraft:barrel[facing=up,open=false]")
    m.set(W, 2, D, "minecraft:barrel[facing=up,open=false]")
    # the old sea door in the east wall: a dark-oak frame standing a course proud of the wall,
    # its opening bricked up with odd old bricks, a chain still hung across it
    sz0, sz1 = 2, 5
    for y in range(1, top):
        m.set(W, y, sz0, "minecraft:stripped_dark_oak_log[axis=y]")
        m.set(W, y, sz1, "minecraft:stripped_dark_oak_log[axis=y]")
    for z in range(sz0, sz1 + 1):
        m.set(W, top, z, "minecraft:dark_oak_log[axis=z]")
    for z in range(sz0 + 1, sz1):
        for y in range(1, top):
            m.set(W + 1, y, z, "minecraft:mud_bricks" if (y + z) % 2 else "minecraft:cracked_stone_bricks")
            m.set(W, y, z, AIR)
    m.set(W, 2, sz0 + 1, "minecraft:iron_chain[axis=z,waterlogged=false]")
    m.set(W, 2, sz0 + 2, "minecraft:iron_chain[axis=z,waterlogged=false]")
    # rope and chain hung from the vault, lamps down the middle
    for (x, z) in ((3, 2), (8, 5)):
        m.set(x, top, z, "minecraft:iron_chain[axis=y,waterlogged=false]")
    for (x, z) in ((3, 4), (8, 2)):
        m.set(x, top, z, HANGING)
    landing(m, lx, _ly, lz, "minecraft:barrel[facing=south,open=false]")
    m.mark("node-free-traders-cellar", 3, 4, facing="east")


def hall(m, place):
    """A folk creature's home dug under a cottage: walls of packed earth, field stone and mud
    brick between timber posts, roots coming through, a low ceiling crossed by two beams, the
    hearth in the east wall with its fire lit, a table and stools at a child's knee, a box bed,
    and shelves and heaps of the town's lost things along the far wall."""
    top = m.ey - 2
    EARTH = ["minecraft:packed_mud", "minecraft:mud_bricks", "minecraft:cobblestone", "minecraft:coarse_dirt",
             "minecraft:rooted_dirt", "minecraft:packed_mud", "minecraft:mossy_cobblestone", "minecraft:mud"]
    FLOOR = ["minecraft:packed_mud", "minecraft:coarse_dirt", "minecraft:packed_mud", "minecraft:mud_bricks", "minecraft:spruce_planks"]
    W, D = shell(m, place, EARTH, FLOOR, ["minecraft:rooted_dirt", "minecraft:dirt", "minecraft:rooted_dirt"])
    lx, _ly, lz = ladder_up(m, place, "terrace-cottage-to-nisse-hall")
    far = 1 if lz == D else D          # the wall across from the ladder
    near = lz
    face_in_far = "south" if far == 1 else "north"
    # timber: posts in the long walls and a beam across the ceiling over each pair
    for x in (3, 6):
        for z in (0, D + 1):
            for y in range(1, top + 1):
                m.set(x, y, z, "minecraft:stripped_spruce_log[axis=y]")
        for z in range(1, D + 1):
            if (x, z) != (lx, lz):
                m.set(x, top, z, "minecraft:spruce_log[axis=z]")
    # an uneven ceiling: lumps of earth hanging into the top course along the walls, roots
    for (x, z) in ((1, far), (2, far), (5, far), (8, far), (9, 2), (2, 3), (8, near), (9, near)):
        if 1 <= x <= W and 1 <= z <= D and m.get(x, top, z) in (None, AIR):
            m.set(x, top, z, "minecraft:rooted_dirt")
    for (x, z) in ((4, 2), (5, 5), (7, 4), (2, 4), (8, 3)):
        if m.get(x, top, z) in (None, AIR):
            m.set(x, top, z, "minecraft:hanging_roots[waterlogged=false]")
    # the hearth in the east wall: field stones round a fire, a hood over it, a pot on the hob
    hz = (D + 1) // 2
    for z in (hz - 1, hz + 1):
        m.set(W, 1, z, "minecraft:mossy_cobblestone")
        m.set(W, 2, z, "minecraft:cobblestone")
    m.set(W, 1, hz, "minecraft:campfire[facing=west,lit=true,signal_fire=false,waterlogged=false]")
    m.set(W, 2, hz, AIR)
    for z in (hz - 1, hz, hz + 1):
        m.set(W, top, z, "minecraft:cobblestone_wall[east=none,north=none,south=none,up=true,waterlogged=false,west=none]" if z == hz else "minecraft:cobblestone")
    m.set(W, 2, hz + 1, "minecraft:cauldron")
    # the table at a child's knee, its top a board on trestles, a stool either side, a candle
    tx, tz = W - 2, hz
    m.set(tx, 1, tz, "minecraft:spruce_trapdoor[facing=north,half=top,open=false,powered=false,waterlogged=false]")
    m.set(tx - 1, 1, tz, "minecraft:spruce_trapdoor[facing=north,half=top,open=false,powered=false,waterlogged=false]")
    m.set(tx, 2, tz, "minecraft:candle[candles=1,lit=true,waterlogged=false]")
    m.set(tx - 1, 2, tz, "minecraft:flower_pot")
    m.set(tx - 1, 1, tz - 1, "minecraft:spruce_slab[type=bottom,waterlogged=false]")
    m.mark("nisse-seat", tx, tz + 1, facing="north")
    for x in (tx - 1, tx + 1):
        if m.get(x, 1, tz + 1) in (None, AIR):
            m.set(x, 1, tz + 1, "minecraft:brown_carpet")
    # the box bed on the near wall past the ladder's landing, boarded at both ends
    m.set(lx + 3, 1, near, "minecraft:red_bed[facing=east,occupied=false,part=foot]")
    m.set(lx + 4, 1, near, "minecraft:red_bed[facing=east,occupied=false,part=head]")
    m.set(lx + 2, 1, near, "minecraft:spruce_planks")
    m.set(lx + 5, 1, near, "minecraft:spruce_planks")
    m.set(lx + 5, 2, near, "minecraft:candle[candles=3,lit=true,waterlogged=false]")
    # the lost things of the town along the far wall, each its own thing: a shelf of odd books with
    # a potted flower on it, a painted pot, a festival lantern on a cask, the clerk's book of
    # by-laws open on its stand, the guildhall bell's clapper (a bell), the lady's red scarf hung
    # on the wall, a jack-o'-lantern from the harvest, a slice of the baker's last cake
    things = [
        (1, f"minecraft:chiseled_bookshelf[facing={face_in_far},slot_0_occupied=true,slot_1_occupied=false,slot_2_occupied=true,slot_3_occupied=true,slot_4_occupied=false,slot_5_occupied=true]"),
        (2, f"minecraft:decorated_pot[cracked=false,facing={face_in_far},waterlogged=false]"),
        (3, "minecraft:barrel[facing=up,open=false]"),
        (4, f"minecraft:lectern[facing={face_in_far},has_book=true,powered=false]"),
        (5, f"minecraft:bell[attachment=floor,facing=east,powered=false]"),
        (7, f"minecraft:jack_o_lantern[facing={face_in_far}]"),
        (8, "minecraft:cake[bites=3]"),
    ]
    for x, b in things:
        m.set(x, 1, far, b)
    m.set(1, 2, far, "minecraft:potted_cornflower")
    m.set(3, 2, far, "minecraft:lantern[hanging=false,waterlogged=false]")
    m.set(6, 2, far, f"minecraft:red_wall_banner[facing={face_in_far}]")
    # the odd socks, sorted by colour, laid out along the west wall
    socks = ["minecraft:white_carpet", "minecraft:red_carpet", "minecraft:yellow_carpet", "minecraft:light_blue_carpet"]
    zs = [z for z in range(1, D + 1) if z not in (far, near)]
    for i, z in enumerate(zs[:len(socks)]):
        m.set(1, 1, z, socks[i])
    landing(m, lx, _ly, lz, "minecraft:hay_block[axis=y]")
    m.mark("node-nisse-hall", 4, (D + 1) // 2, facing="east")


def build(place):
    m = Model(place)
    stem = place.a["place"].removeprefix("node/")
    {"free-traders-cellar": cellar, "nisse-hall": hall}[stem](m, place)
    m.finish()
    return m


# Thin blocks hung in the room's own air where no body stands are the room's air with something in
# it; the starter writes such a block unclaimed where no body reaches it, which an enclosed room's
# closure reads as open air on its boundary. They are claimed the room's (as `den.py` does).
THIN = ("minecraft:lantern", "minecraft:hanging_roots", "minecraft:candle", "minecraft:iron_chain", "minecraft:flower_pot",
        "minecraft:potted_", "minecraft:red_wall_banner", "minecraft:white_carpet")


def claim_thin(out):
    with open(out, encoding="utf-8") as f:
        doc = json.load(f)
    roles = {k for k, v in doc["palette"].items() if isinstance(v, str) and v.split("[")[0].startswith(THIN)}
    n = [0]

    def walk(o, claimed):
        if isinstance(o, dict):
            if o.get("op") == "fill" and not claimed and o.get("material", {}).get("role") in roles:
                n[0] += 1
                return {"op": "claim", "region": "room", "body": o}
            return {k: walk(v, claimed or o.get("op") == "claim") for k, v in o.items()}
        if isinstance(o, list):
            return [walk(v, claimed) for v in o]
        return o
    doc["rules"] = walk(doc["rules"], False)
    with open(out, "w", encoding="utf-8") as f:
        f.write(json.dumps(doc, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    print(f"{os.path.basename(out)}: {n[0]} thin leaf(s) claimed the room's, over {len(roles)} state(s)")


if __name__ == "__main__":
    rc = run(build, reason="the casks' and shelves' tops and the hearth: seen, never stood on")
    if rc == 0:
        claim_thin(sys.argv[sys.argv.index("--out") + 1])
    raise SystemExit(rc)
