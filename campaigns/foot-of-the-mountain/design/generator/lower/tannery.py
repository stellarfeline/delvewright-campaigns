#!/usr/bin/env python3
"""The tannery: a long open drying shed with hides stretched on racks, a yard
of tanning pits and lime vats before it, and the tanner's cottage at the end.

Form, after the tanyards of the trade and community tannery builds
(references in the node's `references[]`): the work is out of doors and
down-wind, the pits sunk in rows in a cobbled yard with walks between them,
the vats of lime and bark liquor beside; the long shed is a roof on posts,
open to the yard, its racks hung with hides; the tanner lives in a small
house at the yard's far end, a little apart from the smell.

    "$DELVEWRIGHT_PYTHON" tannery.py --allocation <allocation.json> --out <campaign>/programs/tannery.json --delvec <delvec>

Drawn into the skill's starter (`$DELVEWRIGHT_SKILL/scripts/starter.py`),
which binds the handing and asks the engine where a body goes.

Piece-local: +x east, +z south, the street on the west; y 0 the ground course, y 1 the walk plane.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
from starter import Model, run, stairs, trapdoor  # noqa: E402


def hsh(*a):
    h = 2166136261
    for v in a:
        h = ((h ^ (v & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    return h










PALETTE = {
    "turf": "minecraft:grass_block[snowy=false]",
    "pave": [{"weight": 5, "block": "minecraft:cobblestone"}, {"weight": 2, "block": "minecraft:mossy_cobblestone"},
             {"weight": 2, "block": "minecraft:stone_bricks"}],
    "yard": [{"weight": 4, "block": "minecraft:cobblestone"}, {"weight": 3, "block": "minecraft:packed_mud"},
             {"weight": 2, "block": "minecraft:coarse_dirt"}, {"weight": 1, "block": "minecraft:mud_bricks"}],
    "shed_floor": [{"weight": 3, "block": "minecraft:packed_mud"}, {"weight": 2, "block": "minecraft:coarse_dirt"}],
    # the shed: posts and a roof, open to the yard; a boarded back wall
    "post": "minecraft:oak_log[axis=y]",
    "beam_x": "minecraft:oak_log[axis=x]",
    "beam_z": "minecraft:oak_log[axis=z]",
    "back": "minecraft:dark_oak_planks",
    "thatch_n": stairs("dark_oak", "north"), "thatch_s": stairs("dark_oak", "south"),
    "thatch_ridge": "minecraft:dark_oak_slab[type=bottom,waterlogged=false]",
    "rack": "minecraft:spruce_fence[east=false,north=false,south=false,waterlogged=false,west=false]",
    "rail": "minecraft:spruce_slab[type=top,waterlogged=false]",
    "hide_a": "minecraft:brown_wool",
    "hide_b": "minecraft:white_wool",
    "hide_c": "minecraft:orange_terracotta",
    "bench": "minecraft:stripped_oak_wood[axis=x]",
    "knife_block": "minecraft:stripped_spruce_wood[axis=y]",
    "bark": "minecraft:spruce_wood[axis=y]",
    "lantern": "minecraft:lantern[hanging=false,waterlogged=false]",
    "lantern_h": "minecraft:lantern[hanging=true,waterlogged=false]",
    # the pits: sunk in mud, rimmed in plank, with walks between; lime vats
    "pit": "minecraft:mud",
    "pit_dark": "minecraft:muddy_mangrove_roots[axis=y]",
    "rim_n": "minecraft:spruce_trapdoor[facing=south,half=bottom,open=true,powered=false,waterlogged=false]",
    "vat": "minecraft:water_cauldron[level=3]",
    "lime": "minecraft:white_concrete_powder",
    "barrel": "minecraft:barrel[facing=up,open=false]",
    "barrel_n": "minecraft:barrel[facing=north,open=false]",
    # the cottage: rubble stone, a deepslate roof
    "rubble": [{"weight": 6, "block": "minecraft:cobblestone"}, {"weight": 3, "block": "minecraft:stone_bricks"},
               {"weight": 1, "block": "minecraft:tuff"}],
    "quoin": "minecraft:tuff_bricks",
    "boards": "minecraft:spruce_planks",
    "pane": "minecraft:glass_pane[east=false,north=false,south=false,waterlogged=false,west=false]",
    "roof_e": stairs("deepslate_tile", "east"), "roof_w": stairs("deepslate_tile", "west"),
    "ridge": "minecraft:deepslate_tile_slab[type=bottom,waterlogged=false]",
    "chimney": "minecraft:bricks",
    "hearth": "minecraft:bricks",
    "fire": "minecraft:campfire[facing=west,lit=true,signal_fire=false,waterlogged=false]",
    "bed_foot": "minecraft:brown_bed[facing=north,occupied=false,part=foot]",
    "bed_head": "minecraft:brown_bed[facing=north,occupied=false,part=head]",
    "table": "minecraft:spruce_planks",
    "chair": stairs("spruce", "east"),
    "rug": "minecraft:brown_carpet",
    # life
    "bush": "minecraft:oak_leaves[distance=1,persistent=true,waterlogged=false]",
    "pot_a": "minecraft:potted_dandelion", "pot_b": "minecraft:potted_fern",
    "f1": "minecraft:dandelion", "f2": "minecraft:oxeye_daisy", "fern": "minecraft:fern",
    "tuft": "minecraft:short_grass", "bed_soil": "minecraft:rooted_dirt",
}

SHED = (4, 14, 2, 6)      # the shed's posts; open to the yard on the south, a working aisle inside
COTTAGE = (17, 21, 2, 7)  # walls included
PITS = (4, 15, 7, 10)
PLATE = 4


def build(place):
    m = Model(place)
    m.palette.update(PALETTE)
    lo, hi = place.space
    X0, X1, Z0, Z1 = lo[0], hi[0], lo[2], hi[2]
    for x in range(X0, X1 + 1):
        for z in range(Z0, Z1 + 1):
            m.set(x, 0, z, "turf")
    m.box(X0, 3, 0, 0, Z0 + 1, Z1 - 1, "pave")
    sx0, sx1, sz0, sz1 = SHED
    cx0, cx1, cz0, cz1 = COTTAGE
    px0, px1, pz0, pz1 = PITS
    m.box(sx0, cx0 - 1, 0, 0, sz1 + 1, Z1, "yard")

    # ---------- the shed: posts every three, a beam, a dark roof; boarded behind
    m.box(sx0, sx1, 0, 0, sz0, sz1, "shed_floor")
    # posts at the ends and the middle only, so the front stands open to the pits
    for x in (sx0, (sx0 + sx1) // 2, sx1):
        for z in (sz0, sz1):
            m.box(x, x, 1, PLATE - 1, z, z, "post")
    for x in (sx0, sx1):
        for z in (sz0, sz1):
            m.box(x, x, 1, PLATE - 1, z, z, "post")
    m.box(sx0, sx1, PLATE, PLATE, sz0, sz0, "beam_x")
    m.box(sx0, sx1, PLATE, PLATE, sz1, sz1, "beam_x")
    m.box(sx0 + 1, sx1 - 1, 1, 2, sz0, sz0, "back")
    m.roof(sx0, sx1, sz0, sz1, PLATE, "x", "dark_oak", fill="back", ridge="thatch_ridge")
    m.clear(sx0, sx0, 1, PLATE - 1, sz0 + 1, sz1 - 1)      # the street end open
    # racks of hides down the shed: a rail on posts, hides hung from it
    for x in range(sx0 + 1, sx1, 2):
        m.box(x, x, 1, 2, 3, 3, "rack")
        m.set(x, 3, 3, "rail")
    for x in range(sx0 + 2, sx1, 2):
        m.set(x, 3, 3, "rail")
        m.set(x, 2, 3, ["hide_a", "hide_b", "hide_c"][hsh(x, 3, 1) % 3])
    m.set(sx1 - 1, 1, 5, "bench")             # the beam and scraping bench at the aisle's end
    m.set(sx1 - 2, 1, 5, "knife_block")
    m.box(sx1 - 1, sx1 - 1, 1, 2, sz0 + 1, sz0 + 1, "bark")
    for x in (6, 10):
        m.box(x, x, PLATE, PLATE, sz0, sz1, "beam_z")
        m.set(x, PLATE - 1, 5, "lantern_h")

    # ---------- the pits: three rows of sunk pits, rimmed, walks between; lime vats and barrels
    for x0 in (5, 9, 13):
        for x in (x0, x0 + 1):
            for z in (8, 9):
                m.set(x, 0, z, "pit" if (x + z) % 3 else "pit_dark")
        for x in (x0, x0 + 1):
            m.set(x, 1, 7, "rim_n")
    m.set(16, 1, 8, "vat")
    m.set(16, 1, 9, "vat")
    m.set(4, 1, 10, "barrel")
    m.set(5, 1, 10, "barrel_n")
    m.set(4, 2, 10, "barrel")
    m.set(12, 1, 10, "bark")

    # ---------- the cottage: rubble, tuff corners, one room with hearth, bed and table
    m.box(cx0, cx1, 0, 0, cz0, cz1, "boards")
    for y in range(1, PLATE + 1):
        for x in range(cx0, cx1 + 1):
            for z in range(cz0, cz1 + 1):
                if x in (cx0, cx1) or z in (cz0, cz1):
                    corner = x in (cx0, cx1) and z in (cz0, cz1)
                    m.set(x, y, z, "quoin" if corner and y % 2 else "rubble")
    m.door(cx0, 1, 5, "spruce", "east")
    m.box(cx0, cx0, 2, 3, 3, 3, "pane")
    m.box(19, 19, 2, 3, cz1, cz1, "pane")
    m.box(cx1, cx1, 2, 3, 4, 5, "pane")
    m.roof(cx0, cx1, cz0, cz1, PLATE, "z", "deepslate_tile", fill="rubble", ridge="ridge")
    m.box(19, 19, 1, 10, cz0, cz0, "chimney")
    m.set(19, 1, cz0 + 1, "hearth")
    m.set(19, 2, cz0 + 1, "fire")
    m.set(20, 1, 5, "bed_foot")
    m.set(20, 1, 4, "bed_head")
    m.set(18, 1, 6, "table")
    m.set(18, 2, 6, "lantern")
    m.set(19, 1, 5, "rug")
    m.box(cx0 + 1, cx1 - 1, PLATE, PLATE, 5, 5, "beam_x")
    m.set(19, PLATE - 1, 5, "lantern_h")
    # life: a bush and flowers by the cottage, potted flowers at its door
    m.set(16, 1, 4, "pot_a")
    m.set(16, 1, 6, "pot_b")
    for x in range(cx0, cx1 + 1):
        m.set(x, 0, Z1, "bed_soil")
        m.set(x, 1, Z1, ["f1", "f2", "fern"][hsh(x, 9, 2) % 3])

    m.finish()
    m.part(sx0, sx1, sz0, sz1, "shed")
    m.part(cx0, cx1, cz0, cz1, "cottage")
    m.part(px0, px1, pz0, pz1, "pits")
    m.mark("node-tannery", 6, 5, "east")     # in the shed, looking down the racks
    return m


if __name__ == "__main__":
    raise SystemExit(run(build, reason="the shed's and the cottage's wall heads and roofs: seen, never stood on"))
