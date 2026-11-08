#!/usr/bin/env python3
"""node/poi-spring — a wayside spring on the castle road.

Scene: a body steps off the road onto a worn path, stops at a long stone
trough set against a low mossy headwall in the bank, where a stone lip spouts
over the water; a spruce bench beside it, ferns and wildflowers round the wet
stones. Palette measured with block-appearance.py --mix: masonry
mossy_stone_bricks 4 / stone_bricks 3 / cracked 1 / mossy_cobblestone 2
(mean #74786d, chroma_mass 0.019); path dirt_path 4 / coarse_dirt 2 / gravel 2
/ cobblestone 2 (mean #846e59, chroma_mass 0.042).
"""
import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
from starter import Model, run, stairs, trapdoor, lantern, grass_block  # noqa: E402

WATER = "minecraft:water[level=0]"


def build(place):
    m = Model(place)
    m.palette["stone"] = [
        {"weight": 4, "block": "minecraft:mossy_stone_bricks"},
        {"weight": 3, "block": "minecraft:stone_bricks"},
        {"weight": 1, "block": "minecraft:cracked_stone_bricks"},
        {"weight": 2, "block": "minecraft:mossy_cobblestone"},
    ]
    m.palette["path"] = [
        {"weight": 4, "block": "minecraft:dirt_path"},
        {"weight": 2, "block": "minecraft:coarse_dirt"},
        {"weight": 2, "block": "minecraft:gravel"},
        {"weight": 2, "block": "minecraft:cobblestone"},
    ]
    m.palette["grass"] = grass_block()
    lo, hi = place.space
    x0, x1 = lo[0], hi[0]          # 1..6
    z0, z1 = lo[2], hi[2]          # 0..6
    g = place.datum.value - 1      # ground course
    w = place.datum.value          # walk plane

    # ground: grass, a worn path from the road to the trough
    m.box(x0, x1, g, g, z0, z1, "grass")
    m.box(x0 + 1, x0 + 3, g, g, z0, z1 - 3, "path")

    # the trough: a stone rim round three cells of water, against the bank
    tz = z1 - 1
    m.box(x0, x0 + 4, w, w, tz - 1, tz, "stone")
    m.box(x0 + 1, x0 + 3, g, g, tz, tz, "minecraft:stone")
    m.box(x0 + 1, x0 + 3, w, w, tz, tz, WATER)
    # the headwall in the bank, its earth cap, the spout lip over the water
    m.box(x0, x0 + 4, w, w + 1, z1, z1, "stone")
    m.box(x0 + 1, x0 + 3, w + 2, w + 2, z1, z1, "grass")
    m.set(x0, w + 1, z1, "grass")  # the bank steps down at its west end
    m.set(x0, w + 2, z1, "minecraft:fern")
    m.set(x0 + 2, w + 1, tz, stairs("stone_brick", "south", "top"))
    m.set(x0 + 4, w + 2, z1, lantern())
    m.set(x0 + 1, w + 3, z1, "minecraft:wildflowers[facing=north,flower_amount=4]")
    m.set(x0 + 3, w + 3, z1, "minecraft:fern")
    m.part(x0 + 1, x0 + 4, tz - 1, tz, "spring")

    # the green: a bench facing the path, ferns at the wet end, flowers west
    bx = x1
    m.set(bx, w, z0 + 1, trapdoor("spruce", "north", open=True))
    m.set(bx, w, z0 + 2, stairs("spruce", "east"))
    m.set(bx, w, z0 + 3, stairs("spruce", "east"))
    m.set(bx, w, tz - 1, trapdoor("spruce", "south", open=True))
    m.set(bx, w, tz, "minecraft:mossy_cobblestone")
    m.set(bx, w + 1, tz, "minecraft:moss_carpet")
    m.tall(bx, w, z1, "large_fern")
    m.set(x0, w, z0 + 1, "minecraft:poppy")
    m.set(x0, w, z0 + 2, "minecraft:wildflowers[facing=east,flower_amount=3]")
    m.set(x0, w, z0 + 3, "minecraft:fern")
    m.set(x0 + 4, w, z0 + 3, "minecraft:pink_petals[facing=south,flower_amount=2]")
    m.part(x0, x1, z0 + 2, tz - 2, "spring-green")
    m.part(x0, x0, tz - 1, z1, "spring-green")
    m.part(x1, x1, tz - 1, z1, "spring-green")

    # the stand before the trough: worn stone flags the bucket is set down on,
    # never dirt_path (a path under a solid block reverts to dirt)
    m.set(x0 + 2, g, tz - 2, "minecraft:cobblestone")
    m.mark("node-poi-spring", x0 + 2, tz - 2, facing="south")
    m.finish()
    return m


raise SystemExit(run(build))
