#!/usr/bin/env python3
"""node/meadow: a flower meadow beyond the great gate, walled in low red brick.

Scene: a body steps out of the gate tower's great gate onto a gravel path that
runs east to a round gravel patch in the meadow's middle, where Wren stands by
a watering cauldron, a bench and her wheelbarrow; grass and drifts of poppies,
cornflowers, oxeye daisies and tulips fill the rest, under four round oaks,
inside a low red-brick wall with brick piers and a clipped hedge on it.

Palette, measured with tools/creator/block-appearance.py --mix:
  wall   minecraft:bricks       #976253 (C_mean 0.074, hue 36)
  path   gravel, one cell in five coarse_dirt (measured 3:1 mix #81756e, chroma_mass 0.019)
"""
import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
from starter import Model, run, slab, stairs, pillar, leaves, lantern, fence, trapdoor  # noqa: E402

AIRB = "minecraft:air"
FLOWERS = ["minecraft:poppy", "minecraft:cornflower", "minecraft:oxeye_daisy",
           "minecraft:red_tulip", "minecraft:orange_tulip", "minecraft:pink_tulip",
           "minecraft:white_tulip"]


def h(x: int, z: int, k: int) -> int:
    """A fixed hash of a column: the drift pattern, the same on every run."""
    v = (x * 73856093) ^ (z * 19349663) ^ (k * 83492791)
    v = (v ^ (v >> 13)) * 1274126177
    return (v ^ (v >> 16)) & 0xFFFF


def build(place):
    m = Model(place)
    ex, ey, ez = place.n
    (x0, d, z0), (x1, ytop, z1) = place.space
    g = place.seams[0]
    glo, ghi = [b.value for b in g["lo"]], [b.value for b in g["hi"]]
    gz0, gz1 = glo[2], ghi[2] - 1          # the gate's columns on z
    cx, cz = (x0 + x1) // 2 + 1, (gz0 + gz1) // 2  # the meadow's middle, on the gate's line
    m.palette["wall"] = "minecraft:bricks"

    # -- the low red-brick wall on the ring: three courses of brick, a brick
    # pier every five cells, and a clipped hedge on the wall between the piers
    # up to the frame's top course (the wall's head is never open floor)
    m.palette["hedge"] = leaves("oak")
    ring = [(x, z) for x in range(0, ex) for z in range(0, ez)
            if (x in (0, ex - 1) or z in (0, ez - 1))]
    for x, z in ring:
        along = z if x in (0, ex - 1) else x
        pier = along % 5 == 0 or (x in (0, ex - 1) and z in (0, ez - 1))
        m.box(x, x, d, d + 2, z, z, "wall")
        m.box(x, x, d + 3, ey - 1, z, z, "wall" if pier else "hedge")

    # -- the gravel path from the gate to the middle, and the round patch there
    path = set()
    for x in range(x0, cx + 1):
        for z in range(gz0, gz1 + 1):
            path.add((x, z))
    for x in range(cx - 3, cx + 4):
        for z in range(cz - 3, cz + 4):
            if (x - cx) ** 2 + (z - cz) ** 2 <= 10:
                path.add((x, z))
    for x, z in path:
        m.set(x, d - 1, z, "minecraft:coarse_dirt" if h(x, z, 4) % 5 == 0 else "minecraft:gravel")

    # lantern posts along the path, either side
    for x in range(x0 + 2, cx - 3, 4):
        for z in (gz0 - 1, gz1 + 1):
            m.set(x, d, z, fence("oak"))
            m.set(x, d + 1, z, lantern())

    # -- Wren's corner of the patch: a watering cauldron, a bench, the barrow
    m.set(cx + 2, d, cz - 2, "minecraft:water_cauldron[level=3]")
    m.set(cx + 3, d, cz, stairs("oak", "east"))
    m.set(cx + 3, d, cz + 1, stairs("oak", "east"))
    # the wheelbarrow: a tub, a wheel in front, two handles behind
    bx, bz = cx - 1, cz + 4
    m.set(bx, d, bz, "minecraft:composter[level=4]")
    m.set(bx - 1, d, bz, trapdoor("spruce", "west", open=True))
    m.set(bx + 1, d, bz, slab("spruce", "top"))
    m.mark("gardener", cx, cz, facing="west")
    m.mark("node-meadow", cx - 2, cz, facing="west")

    # -- four round oaks, one in each quarter
    trees = [(x0 + 4, z0 + 7), (x1 - 4, z0 + 7), (x0 + 4, z1 - 7), (x1 - 4, z1 - 7)]
    trunk = set()
    for tx, tz in trees:
        for y in range(d, d + 4):
            m.set(tx, y, tz, pillar("oak_log"))
        trunk.add((tx, tz))
        for y, r2 in ((d + 2, 5), (d + 3, 8), (d + 4, 5), (d + 5, 2)):
            for x in range(tx - 2, tx + 3):
                for z in range(tz - 2, tz + 3):
                    if (x - tx) ** 2 + (z - tz) ** 2 <= r2 and m.get(x, y, z) is None:
                        m.set(x, y, z, leaves("oak"))
    m.show("up")

    # -- the meadow: grass everywhere, drifts of flowers
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if (x, z) in path or m.get(x, d, z) is not None:
                continue
            if any(abs(x - tx) <= 1 and abs(z - tz) <= 1 for tx, tz in trees):
                continue
            n = h(x, z, 1) % 100
            drift = FLOWERS[h(x // 4, z // 5, 2) % len(FLOWERS)]
            if n < 30:
                m.set(x, d, z, drift)
            elif n < 36:
                m.set(x, d, z, FLOWERS[h(x, z, 3) % len(FLOWERS)])
            elif n < 70:
                m.set(x, d, z, "minecraft:short_grass")
    m.finish()
    return m


raise SystemExit(run(build))
