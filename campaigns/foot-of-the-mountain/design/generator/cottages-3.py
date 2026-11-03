#!/usr/bin/env python3
"""node/cottages-3: two fishermen's cottages, one room down and a loft up,
off a shared garden that opens east onto stretch 9 of the main street.

    DELVEWRIGHT_SKILL=<skill> python3 cottages-3.py --allocation <allocation.json> \
        --out ../../programs/cottages-3.json --delvec <delvec>

Piece-local: +x east, +z south, walk plane y 1. The street is the east side.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
from starter import Model, run, pillar, slab, stairs, fence, fence_gate  # noqa: E402

PAL = {
    "plinth": "minecraft:cobblestone",
    "wall": "minecraft:white_terracotta",
    "frame": "minecraft:stripped_spruce_log",
    "floor": "minecraft:spruce_planks",
    "path": "minecraft:dirt_path",
    "grass": "minecraft:grass_block[snowy=false]",
    "lamp": "minecraft:lantern[hanging=false,waterlogged=false]",
}


def cottage(m, x0, x1, z0, z1, door_z, name):
    """Walls [x0..x1] x [z0..z1], the door on the east wall at door_z."""
    m.box(x0, x1, 0, 0, z0, z1, "plinth")
    m.hollow(x0, x1, 1, 3, z0, z1, "wall")
    for x in (x0, x1):
        for z in (z0, z1):
            m.box(x, x, 1, 3, z, z, pillar("stripped_spruce_log"))
    m.box(x0 + 1, x1 - 1, 0, 0, z0 + 1, z1 - 1, "floor")
    m.clear(x0 + 1, x1 - 1, 1, 3, z0 + 1, z1 - 1)
    m.door(x1, 1, door_z, "spruce", "west")
    m.set(x0, 2, (z0 + z1) // 2, "minecraft:glass_pane[east=false,north=true,south=true,waterlogged=false,west=false]")
    m.bed(x0 + 1, 1, z0 + 1, "red", "east")
    m.set(x0 + 1, 1, z1 - 1, "minecraft:barrel[facing=up,open=false]")
    m.box(x0 + 1, x1 - 1, 4, 4, z0 + 1, z1 - 1, "floor")  # the loft's floor
    m.set(x1 - 1, 3, z0 + 1, "minecraft:lantern[hanging=true,waterlogged=false]")
    m.roof(x0, x1, z0, z1, 5, "z", "spruce", fill="minecraft:spruce_planks", overhang=0)
    m.part(x0, x1, z0, z1, name)


def build(place):
    m = Model(place)
    m.palette.update(PAL)
    # the shared garden: grass, a path from the street to each door
    m.box(1, 13, 0, 0, 1, 10, "grass")
    m.box(7, 13, 0, 0, 3, 3, "path")
    m.box(7, 13, 0, 0, 8, 8, "path")
    cottage(m, 2, 6, 1, 5, 3, "cottage-a")
    cottage(m, 2, 6, 6, 10, 8, "cottage-b")
    # beds of flowers and a low fence between the gardens
    for x in range(8, 13):
        m.set(x, 1, 5, fence("spruce"))
        m.set(x, 1, 6, fence("spruce"))
    for x, z in ((8, 1), (10, 1), (9, 10), (11, 10)):
        m.set(x, 1, z, "minecraft:poppy")
    m.set(12, 1, 1, "minecraft:lantern[hanging=false,waterlogged=false]")
    m.part(8, 12, 1, 7, "gardens")
    m.mark("node-cottages-3", 10, 3)
    return m


raise SystemExit(run(build))
