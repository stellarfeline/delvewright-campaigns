#!/usr/bin/env python3
"""node/potter: a potter's workshop and house, set back behind a front garden.

Drawn into the skill starter's `Model` (`$DELVEWRIGHT_SKILL/scripts/starter.py`).
Run as the handout prints it:

    python3 potter.py --allocation <handout dir>/allocation.json \
        --out <campaign>/programs/potter.json --delvec <delvec>

Piece-local coordinates: +x east, +z south, the walk plane at `place.datum`.
The lane is on the north face; its seam is cut across the whole north edge,
so the lot is not fronted at a doorway span and the house stands back behind
a garden (`street_seam(place, "north")` says so).

Layout (play space x 1..16, z 1..11):
- front garden z 1..3: a path to the door, flower beds, the ware set out;
- the house, walls x 2..12, z 4..10: the working room (west, wheel, shelves of
  ware, counter by the door) and the living room (east, bed, table, hearth
  corner) joined by a door in the partition at x 7;
- the yard x 13..16 and the back strip z 11: drying boards, clay heap, water;
- the bottle kiln x 13..15, z 8..10, its stoke mouth under a lean-to.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
from starter import (  # noqa: E402
    Model,
    run,
    stairs,
    slab,
    pillar,
    fence,
    lantern,
    wall_torch,
    campfire,
    pane,
    flower_bed,
    lamp,
    street_seam,
)

POT = "minecraft:decorated_pot[cracked=false,facing={f},waterlogged=false]"


def build(place):
    m = Model(place)
    y = place.datum.value  # walk plane
    g = y - 1  # ground course
    fronted, _ = street_seam(place, "north")
    assert not fronted, "the lane's seam spans the whole edge: a set-back front"

    m.palette.update({
        "plinth": [
            {"block": "minecraft:cobblestone", "weight": 3},
            {"block": "minecraft:mossy_cobblestone", "weight": 1},
        ],
        "infill": "minecraft:calcite",
        "post": pillar("minecraft:stripped_spruce_log", "y"),
        "plate_x": pillar("minecraft:stripped_spruce_log", "x"),
        "plate_z": pillar("minecraft:stripped_spruce_log", "z"),
        "work_floor": "minecraft:packed_mud",
        "home_floor": "minecraft:spruce_planks",
        "brick": "minecraft:bricks",
        "clay": "minecraft:clay",
        "path": "minecraft:dirt_path",
        # worn earth in the yard; the garden is the ground the plot is handed
        "yard_ground": [
            {"block": "minecraft:coarse_dirt", "weight": 3},
            {"block": "minecraft:gravel", "weight": 1},
            {"block": "minecraft:packed_mud", "weight": 1},
        ],
    })

    X0, X1, Z0, Z1, PX = 2, 12, 4, 10, 7  # house walls, partition column
    HEAD = y + 4  # wall plate course
    RAIL = y + 2  # the beam over every opening: the door and window heads stand under it

    # ---- the house ----
    m.box(X0, X1, g, g, Z0, Z1, "plinth")
    m.box(X0 + 1, PX - 1, g, g, Z0 + 1, Z1 - 1, "work_floor")
    m.box(PX + 1, X1 - 1, g, g, Z0 + 1, Z1 - 1, "home_floor")
    m.hollow(X0, X1, y, y, Z0, Z1, "plinth")
    m.hollow(X0, X1, y + 1, HEAD - 1, Z0, Z1, "infill")
    for yy in (RAIL, HEAD):
        for x in range(X0, X1 + 1):
            m.set(x, yy, Z0, "plate_x")
            m.set(x, yy, Z1, "plate_x")
        for z in range(Z0 + 1, Z1):
            m.set(X0, yy, z, "plate_z")
            m.set(X1, yy, z, "plate_z")
    for x in (X0, PX, X1):
        for z in (Z0, Z1):
            m.box(x, x, y, HEAD, z, z, "post")
    # the partition: a timber-framed wall with a door in it
    m.box(PX, PX, y, y, Z0 + 1, Z1 - 1, "plinth")
    m.box(PX, PX, y + 1, HEAD - 1, Z0 + 1, Z1 - 1, "infill")
    m.box(PX, PX, RAIL, RAIL, Z0 + 1, Z1 - 1, "plate_z")
    m.box(PX, PX, HEAD, HEAD, Z0 + 1, Z1 - 1, "plate_z")
    m.clear(X0 + 1, PX - 1, y, HEAD, Z0 + 1, Z1 - 1)
    m.clear(PX + 1, X1 - 1, y, HEAD, Z0 + 1, Z1 - 1)
    m.door(PX, y, 7, "spruce", "east", hinge="left")
    # front door, door to the yard
    m.door(5, y, Z0, "spruce", "north", hinge="right")
    m.door(X1, y, 6, "spruce", "east", hinge="left")
    # windows: one course, their heads at the door heads' course
    for (x, z) in ((3, Z0), (10, Z0), (4, Z1), (10, Z1), (X0, 7)):
        m.set(x, y + 1, z, pane("glass_pane"))
    for (x, z) in ((X1, 8),):
        m.set(x, y + 1, z, pane("glass_pane"))

    # roof: a gable along x, deepslate tiles, calcite gable ends
    m.roof(X0, X1, Z0, Z1, HEAD, "x", "deepslate_tile", fill="infill")

    # ---- the working room (x 3..6) ----
    # the wheel: a stone plate on a post, the potter's stool before it
    m.set(4, y, 7, fence("spruce"))
    m.set(4, y + 1, 7, slab("smooth_stone", "bottom"))
    m.set(4, y, 8, stairs("spruce", "south"))
    m.set(5, y, 7, "minecraft:water_cauldron[level=3]")
    m.set(6, y, 9, "minecraft:crafting_table")
    m.set(5, y, 9, "clay")
    # shelves of finished ware on the west wall
    for z in (6, 7, 8, 9):
        m.set(3, y + 1, z, slab("spruce", "top"))
    m.set(3, y + 2, 6, POT.format(f="east"))
    m.set(3, y + 2, 7, "minecraft:flower_pot")
    m.set(3, y + 2, 8, POT.format(f="east"))
    m.set(3, y + 2, 9, "minecraft:flower_pot")
    # the counter by the door, ware on it, a lamp
    m.set(3, y, 5, slab("spruce", "top"))
    m.set(4, y, 5, slab("spruce", "top"))
    m.set(3, y + 1, 5, lantern())
    m.set(4, y + 1, 5, POT.format(f="north"))
    m.set(6, y + 1, 6, wall_torch("west"))

    # ---- the living room (x 8..11) ----
    m.bed(11, y, 8, "red", "south")
    m.set(9, y, 6, fence("spruce"))
    m.set(9, y + 1, 6, "minecraft:spruce_pressure_plate[powered=false]")
    m.set(8, y, 6, stairs("spruce", "east"))
    m.set(10, y, 6, stairs("spruce", "west"))
    m.set(11, y, 5, campfire("west", lit=False))
    m.set(11, y + 1, 5, "brick")
    m.set(11, y + 2, 5, "brick")
    for (x, z) in ((8, 8), (9, 8), (8, 9), (9, 9)):
        m.set(x, y, z, "minecraft:red_carpet")
    m.set(8, y + 1, 9, wall_torch("east"))
    m.set(10, y + 1, 9, lantern())
    m.set(10, y, 9, slab("spruce", "top"))

    # ---- the front garden (z 1..3) ----
    for z in (1, 2, 3):
        m.set(5, g, z, "path")
    flower_bed(m, [(1, 2), (2, 2), (3, 2)], ["minecraft:poppy", "minecraft:oxeye_daisy", "minecraft:cornflower"])
    flower_bed(m, [(8, 2), (9, 2), (10, 2), (11, 2)], ["minecraft:allium", "minecraft:dandelion", "minecraft:azure_bluet", "minecraft:poppy"])
    m.set(4, y, 3, POT.format(f="north"))
    m.set(6, y, 3, POT.format(f="north"))
    m.set(3, y, 3, "minecraft:potted_red_tulip")
    m.set(9, y, 3, stairs("spruce", "south"))
    m.set(10, y, 3, stairs("spruce", "south"))
    lamp(m, 12, 2, post=fence("spruce"), light=lantern())

    # ---- the yard (x 13..16, and the back strip z 11) ----
    m.box(13, 16, g, g, 3, 11, "yard_ground")
    m.box(2, 12, g, g, 11, 11, "yard_ground")
    for z in (3, 4, 5):
        m.set(16, y, z, slab("spruce", "top"))
    m.set(16, y + 1, 3, POT.format(f="west"))
    m.set(16, y + 1, 4, "minecraft:flower_pot")
    m.set(16, y + 1, 5, POT.format(f="west"))
    m.set(16, y, 10, "clay")
    m.set(16, y, 11, "clay")
    m.set(16, y + 1, 11, "clay")
    m.set(15, y, 11, "minecraft:coarse_dirt")
    m.set(16, y, 6, "minecraft:water_cauldron[level=2]")
    m.box(16, 16, y, y + 1, 7, 7, pillar("minecraft:spruce_log", "x"))
    m.set(3, y, 11, "minecraft:potted_fern")

    # ---- the bottle kiln (x 13..15, z 8..10) ----
    m.box(13, 15, y, y + 2, 8, 10, "brick")
    m.set(14, y, 8, campfire("north", lit=True))
    for (x, z) in ((14, 8), (13, 9), (15, 9), (14, 10), (14, 9)):
        m.set(x, y + 3, z, "brick")
    for (x, z) in ((13, 8), (15, 8), (13, 10), (15, 10)):
        m.set(x, y + 3, z, slab("brick", "bottom"))
    m.set(14, y + 4, 9, "brick")
    m.set(14, y + 5, 9, "minecraft:brick_wall[east=none,north=none,south=none,up=true,waterlogged=false,west=none]")
    # the lean-to over the stoke mouth
    for x in (13, 15):
        m.box(x, x, y, y + 1, 7, 7, fence("spruce"))
    m.box(13, 15, y + 2, y + 2, 7, 7, slab("spruce", "bottom"))

    # ---- the parts ----
    m.part(X0 + 1, X1 - 1, Z0 + 1, Z1 - 1, "workshop")
    m.part(13, 15, 8, 10, "kiln")
    m.part(13, 16, 3, 7, "yard")
    m.part(16, 16, 8, 11, "yard")
    m.part(13, 15, 11, 11, "yard")
    m.part(2, 12, 11, 11, "yard")
    m.mark("node-potter", 5, 6)
    m.finish()
    return m


if __name__ == "__main__":
    raise SystemExit(run(build))
