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
    top = m.ey - 2                       # the walk courses are 1..top
    BRICK = ["minecraft:bricks"] * 5 + ["minecraft:mud_bricks", "minecraft:stone_bricks"]
    FLOOR = ["minecraft:stone_bricks"] * 3 + ["minecraft:cracked_stone_bricks", "minecraft:cobblestone"]
    W, D = shell(m, place, BRICK, FLOOR, ["minecraft:bricks"])
    lx, _ly, lz = ladder_up(m, place, "merchant-to-free-traders-cellar")
    # the vault: upside-down brick stairs along both long walls under the lid
    for x in range(1, W + 1):
        if (x, 1) != (lx, lz):
            m.set(x, top, 1, "minecraft:brick_stairs[facing=north,half=top,shape=straight,waterlogged=false]")
        m.set(x, top, D, "minecraft:brick_stairs[facing=south,half=top,shape=straight,waterlogged=false]")
    # casks two high along the north wall, past the ladder
    for x in range(lx + 2, W + 1):
        if x == W - 3:
            continue
        m.set(x, 1, 1, "minecraft:barrel[facing=south,open=false]")
        if x % 3 != 0:
            m.set(x, 2, 1, "minecraft:barrel[facing=south,open=false]")
    # the sugar: sacks along the south wall, this year's eleven pounds in a heap by the table
    for x in range(2, W - 2):
        m.set(x, 1, D, "minecraft:white_wool")
        if x % 2 == 0:
            m.set(x, 2, D, "minecraft:white_wool")
    # the card table: a cask on end, candles, two casks for stools
    tx, tz = W // 2, D // 2
    m.set(tx, 1, tz, "minecraft:barrel[facing=up,open=false]")
    m.set(tx, 2, tz, "minecraft:candle[candles=3,lit=true,waterlogged=false]")
    m.set(tx - 1, 1, tz, "minecraft:spruce_stairs[facing=west,half=bottom,shape=straight,waterlogged=false]")
    m.set(tx, 1, tz - 1, "minecraft:spruce_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]")
    m.mark("magnhild-seat", tx + 1, tz, facing="west")
    # the chart and the members' ledger in the south-east corner
    m.set(W, 1, D - 1, "minecraft:cartography_table")
    m.set(W - 1, 1, D - 1, "minecraft:lectern[facing=north,has_book=false,powered=false]")
    # the old sea door: bricked up inside its timber frame in the east wall
    for z in range(tz - 1, tz + 2):
        for y in range(1, 3):
            m.set(W, y, z, "minecraft:mud_bricks")
        m.set(W, 3, z, "minecraft:stripped_dark_oak_log[axis=z]")
    for y in range(1, 3):
        m.set(W, y, tz - 2, "minecraft:stripped_dark_oak_log[axis=y]")
        m.set(W, y, tz + 2, "minecraft:stripped_dark_oak_log[axis=y]")
    # lamps: hung from the lid down the middle
    for x in (3, W - 2):
        m.set(x, top, tz, HANGING)
    landing(m, lx, _ly, lz, "minecraft:barrel[facing=south,open=false]")
    m.mark("node-free-traders-cellar", tx - 2, tz + 1, facing="east")


def hall(m, place):
    top = m.ey - 2
    EARTH = ["minecraft:rooted_dirt", "minecraft:dirt", "minecraft:coarse_dirt", "minecraft:rooted_dirt", "minecraft:packed_mud"]
    FLOOR = ["minecraft:packed_mud", "minecraft:coarse_dirt", "minecraft:packed_mud", "minecraft:mud_bricks"]
    W, D = shell(m, place, EARTH, FLOOR, ["minecraft:rooted_dirt"])
    lx, _ly, lz = ladder_up(m, place, "terrace-cottage-to-nisse-hall")
    # roots through the roof, clear of the ladder and of the way round the room
    for (x, z) in ((3, 3), (5, 6), (7, 2), (9, 5), (2, 5), (W - 1, 3)):
        if 1 <= x <= W and 1 <= z <= D and (x, z) != (lx, lz):
            m.set(x, top, z, "minecraft:hanging_roots[waterlogged=false]")
    # the hearth of field stones against the east wall, a small fire in it
    hz = D // 2
    m.set(W, 1, hz, "minecraft:campfire[facing=west,lit=true,signal_fire=false,waterlogged=false]")
    m.set(W, 1, hz - 1, "minecraft:mossy_cobblestone")
    m.set(W, 1, hz + 1, "minecraft:mossy_cobblestone")
    for z in (hz - 1, hz, hz + 1):
        m.set(W, 2, z, "minecraft:cobblestone")
    # the table at a child's knee and its stool, a bowl on the table
    tx = W - 3
    m.set(tx, 1, hz, "minecraft:spruce_slab[type=bottom,waterlogged=false]")
    m.set(tx, 1, hz - 1, "minecraft:spruce_trapdoor[facing=south,half=bottom,open=false,powered=false,waterlogged=false]")
    m.mark("nisse-seat", tx, hz + 1, facing="north")
    # the far end from the ladder (`fz`) and the ladder's own end (`nz`)
    nz = lz
    fz = 1 if lz == D else D
    face_far = "north" if fz == 1 else "south"
    face_near = "south" if fz == 1 else "north"
    # the box bed in the far west corner, boxed in planks
    m.set(2, 1, fz, "minecraft:red_bed[facing=east,occupied=false,part=foot]")
    m.set(3, 1, fz, "minecraft:red_bed[facing=east,occupied=false,part=head]")
    m.set(4, 1, fz, "minecraft:spruce_planks")
    m.set(1, 1, fz, "minecraft:spruce_planks")
    # the lost things of the town along the ladder's end: odd socks sorted by colour, the bell's
    # clapper (a bell), a pot, a candle on a cask, a shelf of odd books
    socks = ["minecraft:white_wool", "minecraft:red_wool", "minecraft:yellow_wool", "minecraft:blue_wool", "minecraft:green_wool",
             "minecraft:light_gray_wool", "minecraft:brown_wool"]
    for i, x in enumerate(range(lx + 2, min(lx + 2 + len(socks), W - 1))):
        m.set(x, 1, nz, socks[i])
    m.set(W - 1, 1, nz, f"minecraft:bell[attachment=floor,facing={face_far},powered=false]")
    m.set(W, 1, nz, f"minecraft:decorated_pot[cracked=false,facing={face_far},waterlogged=false]")
    m.set(W, 1, fz, "minecraft:barrel[facing=up,open=false]")
    m.set(W, 2, fz, "minecraft:candle[candles=4,lit=true,waterlogged=false]")
    m.set(W - 1, 1, fz, f"minecraft:chiseled_bookshelf[facing={face_near},slot_0_occupied=true,slot_1_occupied=false,slot_2_occupied=true,slot_3_occupied=true,slot_4_occupied=false,slot_5_occupied=false]")
    # light: a lantern hung over the middle of the room
    m.set(W // 2, top, D // 2, HANGING)
    m.set(3, top, D // 2 - 1, HANGING)
    landing(m, lx, _ly, lz, "minecraft:hay_block[axis=y]")
    m.mark("node-nisse-hall", W // 2, D // 2 + 1, facing="east")


def build(place):
    m = Model(place)
    stem = place.a["place"].removeprefix("node/")
    {"free-traders-cellar": cellar, "nisse-hall": hall}[stem](m, place)
    m.finish()
    return m


# Thin blocks hung in the room's own air where no body stands are the room's air with something in
# it; the starter writes such a block unclaimed where no body reaches it, which an enclosed room's
# closure reads as open air on its boundary. They are claimed the room's (as `den.py` does).
THIN = ("minecraft:lantern", "minecraft:hanging_roots", "minecraft:candle")


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
