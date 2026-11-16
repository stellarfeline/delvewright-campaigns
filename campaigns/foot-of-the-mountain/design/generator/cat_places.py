#!/usr/bin/env python3
"""The cat's places: the path under the hill and the lush cave in its flank; the track to the old
miner's hut and the hut on the high ground west of the castle.

    DELVEWRIGHT_SKILL=<skill> python3 cat_places.py --allocation <delvec allocation . node/<place>> \\
        --out ../../programs/<place>.json --delvec <delvec>

One generator, dispatched on the place's stem, drawn into the skill's starter. After the lush cave
(the node's `references[]`: moss and azalea, clay and dripleaf round still pools, vines of glow
berries from the roof) and the miner's cottage (one room of rough stone, a hearth, a bunk). Piece-
local axes: +x east, +z south; y 0 the ground course, y 1 the walk plane.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
from starter import Model, fence, lantern, run, slab, stairs, wall  # noqa: E402

GRASS = "minecraft:grass_block[snowy=false]"
WATER = "minecraft:water[level=0]"
MOSS = "minecraft:moss_block"
VINE_TOP = "minecraft:cave_vines_plant[berries=true]"
VINE_END = "minecraft:cave_vines[age=25,berries=true]"  # a vine head, hung from the roof


def h(*a):
    v = 2166136261
    for n in a:
        v = ((v ^ (n & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    return v


def lamp_post(m, x, z, d):
    m.set(x, d, z, fence("spruce"))
    m.set(x, d + 1, z, fence("spruce"))
    m.set(x, d + 2, z, lantern())


def cave_path(m, place):
    lo, hi = place.space
    X0, X1, Z0, Z1 = lo[0], hi[0], lo[2], hi[2]
    d = place.datum.value
    m.palette["wall"] = [{"weight": 5, "block": "minecraft:stone"}, {"weight": 3, "block": "minecraft:mossy_cobblestone"},
                         {"weight": 2, "block": "minecraft:andesite"}, {"weight": 2, "block": MOSS}]
    for x in range(X0, X1 + 1):
        for z in range(Z0, Z1 + 1):
            m.set(x, d - 1, z, GRASS)
        for z in range(Z0 + 1, Z1):
            if h(x, z, 3) % 5:
                m.set(x, d - 1, z, "minecraft:coarse_dirt" if h(x, z) % 3 else "minecraft:gravel")
    # moss and vines hang down the rock face beside the mouth; ferns at its foot
    for x in range(X0, X1 + 1):
        if h(x, 9) % 4 == 0 and not 21 <= x <= 25:
            m.set(x, d, Z0, "minecraft:fern")
    for x in range(X0 + 4, X1, 8):
        lamp_post(m, x, Z1, d)
    mx = 23
    m.mark("cave-mouth", mx, Z0 + 1, facing="north")
    m.mark("node-cave-path", 10, (Z0 + Z1) // 2, facing="east")
    m.show("up")   # the rock face's top shows where the hill behind it is low


def lush_cave(m, place):
    lo, hi = place.space
    X0, X1, Z0, Z1 = lo[0], hi[0], lo[2], hi[2]
    d = place.datum.value
    top = hi[1]
    m.palette["wall"] = [{"weight": 5, "block": "minecraft:stone"}, {"weight": 3, "block": MOSS},
                         {"weight": 2, "block": "minecraft:mossy_cobblestone"}, {"weight": 1, "block": "minecraft:clay"}]
    m.palette["lid"] = [{"weight": 4, "block": "minecraft:stone"}, {"weight": 3, "block": MOSS}, {"weight": 1, "block": "minecraft:tuff"}]
    # the floor: moss with clay patches
    for x in range(X0, X1 + 1):
        for z in range(Z0, Z1 + 1):
            m.set(x, d - 1, z, "minecraft:clay" if h(x, z, 5) % 6 == 0 else MOSS)
    # the upper level at the back: a mossy shelf three high, its pond set into it
    UP = 4                                    # rows z0..z3 are the shelf
    sh = d + 2                                # the shelf's top course
    for x in range(X0, X1 + 1):
        for z in range(Z0, Z0 + UP):
            m.box(x, x, d, sh, z, z, MOSS)
    for x in range(X0 + 9, X0 + 14):
        for z in range(Z0, Z0 + 3):
            m.set(x, sh, z, WATER)
    # the steps up at the east end: three moss blocks climbing to the shelf
    for i, z in enumerate((Z0 + UP + 2, Z0 + UP + 1, Z0 + UP)):
        for x in (X1 - 1, X1):
            m.box(x, x, d, d + i, z, z, MOSS)
    # the lower pond in the middle of the floor
    for x in range(X0 + 5, X0 + 11):
        for z in range(Z0 + 6, Z0 + 10):
            m.set(x, d - 1, z, WATER)
    # dripleaf at the pond's edge, azalea bushes, moss carpet
    m.set(X0 + 4, d, Z0 + 7, "minecraft:big_dripleaf[facing=east,tilt=none,waterlogged=false]")
    m.set(X0 + 11, d, Z0 + 8, "minecraft:big_dripleaf[facing=west,tilt=none,waterlogged=false]")
    for (x, z) in ((X0 + 1, Z0 + UP + 1), (X1 - 4, Z1 - 1), (X0 + 15, Z0 + 6)):
        m.set(x, d, z, "minecraft:flowering_azalea")
    for x in range(X0, X1 + 1):
        for z in range(Z0 + UP, Z1 + 1):
            if m.get(x, d, z) is None and m.get(x, d - 1, z) == MOSS and h(x, z, 11) % 5 == 0:
                m.set(x, d, z, "minecraft:moss_carpet")
    # glowing knots of roots in the roof, every few cells over the floor and the shelf (a hanging vine
    # is open air on the room's boundary, which the enclosed room's closure refuses)
    for x in range(X0 + 1, X1, 3):
        for z in range(Z0 + 1, Z1, 3):
            m.set(x, top + 1, z, "minecraft:shroomlight")   # a glowing knot of roots in the roof
    m.mark("cat-cave", X0 + 13, Z0 + 8, facing="west")
    m.mark("axolotl-low", X0 + 7, Z0 + 8, facing="south")
    m.mark("upper-pond-rim", X0 + 11, Z0 + 3, facing="north", y=sh + 1)
    m.mark("axolotl-high", X0 + 11, Z0 + 1, facing="south", y=sh)    # in the upper pond's water
    m.mark("node-lush-cave", X0 + 4, Z1 - 1, facing="north")
    m.show("up")   # the cave's roof of moss and rock shows where the hill over it is low, by the mouth


def hut_path(m, place):
    lo, hi = place.space
    X0, X1, Z0, Z1 = lo[0], hi[0], lo[2], hi[2]
    d = place.datum.value
    for x in range(X0, X1 + 1):
        for z in range(Z0, Z1 + 1):
            m.set(x, d - 1, z, GRASS)
        for z in range(Z0 + 1, Z1):
            m.set(x, d - 1, z, "minecraft:gravel" if h(x, z) % 3 else "minecraft:coarse_dirt")
    lamp_post(m, X1 - 1, Z0, d)
    lamp_post(m, X0 + 9, Z1, d)
    m.mark("node-hut-path", (X0 + X1) // 2, (Z0 + Z1) // 2, facing="east")


def miners_hut(m, place):
    lo, hi = place.space
    X0, X1, Z0, Z1 = lo[0], hi[0], lo[2], hi[2]
    d = place.datum.value
    m.palette["bar-miners-hut-to-cat-den"] = "minecraft:loom[facing=north]"
    for x in range(X0, X1 + 1):
        for z in range(Z0, Z1 + 1):
            m.set(x, d - 1, z, "minecraft:gravel" if h(x, z, 2) % 3 else GRASS)
    # the hut: rough stone walls four high, a door toward the track, a flat roof of old planks
    hx0, hx1, hz0, hz1 = 5, 11, 5, 11
    stone = [{"weight": 4, "block": "minecraft:cobblestone"}, {"weight": 2, "block": "minecraft:mossy_cobblestone"},
             {"weight": 1, "block": "minecraft:stone"}]
    m.palette["rubble"] = stone
    m.box(hx0, hx1, d - 1, d - 1, hz0, hz1, "minecraft:spruce_planks")
    m.hollow(hx0, hx1, d, d + 3, hz0, hz1, "rubble")
    m.box(hx0, hx1, d + 4, d + 4, hz0, hz1, slab("spruce", "bottom"))
    m.door(hx0, d, 7, "spruce", "west")
    m.set(hx1, d + 1, 8, "minecraft:glass_pane[east=false,north=true,south=true,waterlogged=false,west=false]")
    m.set(8, d + 1, hz0, "minecraft:glass_pane[east=true,north=false,south=false,waterlogged=false,west=true]")
    # inside: a cold hearth, a bunk, a table, a lantern; the loom in the back corner is the bar
    m.set(10, d, 6, "minecraft:campfire[facing=west,lit=false,signal_fire=false,waterlogged=false]")
    m.bed(9, d, 10, "brown", "east")
    m.set(8, d, 7, fence("spruce"))
    m.set(8, d + 1, 7, "minecraft:brown_carpet")
    m.set(7, d, 7, stairs("spruce", "east"))
    m.set(9, d, 7, lantern())
    # the top rung of the ladder up from the chasm stands in the hole through the hut's floor: the
    # rung in a floor's hole is the hole owner's, and the hut owns this one (the den's ladder ends
    # under it). The starter leaves a floor hole empty (a body drops through it), so the hole's
    # cell is taken as the drawing's, as for a stair through a hole in a lid, and holds the rung,
    # hung on the floor's planks to its west
    ox, oy, oz = next([b.value for b in s_["lo"]] for s_ in place.seams if s_["stem"] == "miners-hut-to-cat-den")
    m.drawn_openings.add((ox, oy, oz))
    m.set(ox, oy, oz, "minecraft:ladder[facing=east,waterlogged=false]")
    # the yard's lamp
    lamp_post(m, 3, 12, d)
    m.mark("node-miners-hut", 3, 10, facing="east")


def build(place):
    m = Model(place)
    stem = place.a["place"].removeprefix("node/")
    {"cave-path": cave_path, "lush-cave": lush_cave, "hut-path": hut_path, "miners-hut": miners_hut}[stem](m, place)
    m.finish()
    return m


if __name__ == "__main__":
    raise SystemExit(run(build, reason="rock, roof and wall heads: seen, never stood on"))
