#!/usr/bin/env python3
"""The boatwright's: a boat on the stocks in the open yard before the lane,
half planked and half in bare ribs, with the open-fronted shed behind it and
the timber stacked to season beside.

Form, after boatbuilders' yards and community boat-under-construction builds
(references in the node's `references[]`): small boats are built in the
open in front of the shed, on blocks along a keel, the stem rising at the
bow and a raked transom at the stern; the ribs go up first and the strakes
are fastened to them from the keel up, so a boat in progress shows planking
on one part and bare frames on the rest. The shed behind is open along its
front: the bench, the steam box over its fire, tar, timber and oars.

    "$DELVEWRIGHT_PYTHON" boatwright.py --allocation <allocation.json> --out <campaign>/programs/boatwright.json --delvec <delvec>

Drawn into the skill's starter (`$DELVEWRIGHT_SKILL/scripts/starter.py`).

Piece-local: +x east, +z south, the lane on the south; y 0 the ground course, y 1 the walk plane.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
from starter import Model, run, stairs, trapdoor  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # the town kit, one up
import townkit  # noqa: E402


def hsh(*a):
    h = 2166136261
    for v in a:
        h = ((h ^ (v & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    return h






PALETTE = {
    "turf": "minecraft:grass_block[snowy=false]",
    "yard": [{"weight": 4, "block": "minecraft:gravel"}, {"weight": 2, "block": "minecraft:coarse_dirt"},
             {"weight": 2, "block": "minecraft:cobblestone"}],
    "chips": [{"weight": 3, "block": "minecraft:coarse_dirt"}, {"weight": 2, "block": "minecraft:stripped_oak_wood[axis=y]"},
              {"weight": 1, "block": "minecraft:gravel"}],
    "shed_floor": [{"weight": 3, "block": "minecraft:spruce_planks"}, {"weight": 1, "block": "minecraft:coarse_dirt"}],
    "plinth": "minecraft:cobblestone",
    "post": "minecraft:spruce_log[axis=y]",
    "beam_x": "minecraft:spruce_log[axis=x]",
    "boards": "minecraft:dark_oak_planks",
    "roof_n": stairs("deepslate_tile", "north"), "roof_s": stairs("deepslate_tile", "south"),
    "ridge": "minecraft:deepslate_tile_slab[type=bottom,waterlogged=false]",
    "pane": "minecraft:glass_pane[east=false,north=false,south=false,waterlogged=false,west=false]",
    # the boat
    "stock": "minecraft:stripped_spruce_wood[axis=y]",
    "keel": "minecraft:stripped_oak_log[axis=x]",
    "stem": "minecraft:stripped_oak_log[axis=y]",
    "stem_tip": "minecraft:oak_fence[east=false,north=false,south=false,waterlogged=false,west=false]",
    "bilge_n": stairs("oak", "south", "top"),
    "bilge_s": stairs("oak", "north", "top"),
    "strake": "minecraft:oak_planks",
    "lap_n": trapdoor("oak", "south", "bottom", True),
    "lap_s": trapdoor("oak", "north", "bottom", True),
    "bow_plate_n": trapdoor("oak", "north", "bottom", True),   # on the inner (south) face
    "bow_plate_s": trapdoor("oak", "south", "bottom", True),   # on the inner (north) face
    "stem_post": "minecraft:oak_fence[east=false,north=false,south=false,waterlogged=false,west=true]",
    "gunwale": "minecraft:oak_slab[type=bottom,waterlogged=false]",
    "gunwale_hi": "minecraft:oak_slab[type=top,waterlogged=false]",
    "rib": "minecraft:oak_fence[east=false,north=false,south=false,waterlogged=false,west=false]",
    "bow_n": stairs("oak", "south", "bottom"),
    "bow_s": stairs("oak", "north", "bottom"),
    "transom": "minecraft:oak_planks",
    "transom_rake": stairs("oak", "east", "top"),
    "transom_top": stairs("oak", "west", "bottom"),
    # the shed's work
    "bench": "minecraft:crafting_table",
    "vice": "minecraft:grindstone[face=floor,facing=south]",
    "steam": "minecraft:campfire[facing=south,lit=true,signal_fire=false,waterlogged=false]",
    "steam_box": "minecraft:spruce_trapdoor[facing=south,half=top,open=false,powered=false,waterlogged=false]",
    "tar": "minecraft:cauldron",
    "oars": "minecraft:stripped_spruce_log[axis=y]",
    "planks_stack": "minecraft:spruce_slab[type=bottom,waterlogged=false]",
    "lantern": "minecraft:lantern[hanging=false,waterlogged=false]",
    "lantern_h": "minecraft:lantern[hanging=true,waterlogged=false]",
    "barrel": "minecraft:barrel[facing=up,open=false]",
    # the yard
    "timber_z": "minecraft:stripped_spruce_log[axis=z]",
    "timber_x": "minecraft:spruce_log[axis=x]",
    "winch": "minecraft:stripped_oak_log[axis=y]",
    "winch_bar": trapdoor("oak", "north", "bottom"),
    "pot_a": "minecraft:potted_cornflower",
    "tuft": "minecraft:short_grass", "fern": "minecraft:fern",
}

SHED = (2, 9, 1, 5)     # walls on the north, west and east; open along the south
PLATE = 4
HULL_X = (3, 13)        # transom at x 3, stem at x 13
KZ = 7                  # the keel's line


def build(place):
    m = Model(place)
    m.palette.update(PALETTE)
    lo, hi = place.space
    X0, X1, Z0, Z1 = lo[0], hi[0], lo[2], hi[2]
    for x in range(X0, X1 + 1):
        for z in range(Z0, Z1 + 1):
            m.set(x, 0, z, "turf")
    sx0, sx1, sz0, sz1 = SHED
    m.box(X0, X1, 0, 0, sz1 + 1, Z1, "yard")
    m.box(sx1 + 1, X1, 0, 0, Z0, sz1, "yard")
    m.box(HULL_X[0], HULL_X[1], 0, 0, KZ - 1, KZ + 1, "chips")

    # ---------- the shed: a boarded back and ends on posts, open to the boat
    m.box(sx0, sx1, 0, 0, sz0, sz1, "shed_floor")
    for x in range(sx0, sx1 + 1):
        for y in range(1, PLATE + 1):
            m.set(x, y, sz0, "plinth" if y == 1 else ("post" if x in (sx0, sx1, 5) else "boards"))
    for z in range(sz0, sz1 + 1):
        for x in (sx0, sx1):
            for y in range(1, PLATE + 1):
                m.set(x, y, z, "plinth" if y == 1 and z < sz1 else ("post" if z in (sz0, sz1) else "boards"))
    for x in (sx0, 5, sx1):
        m.box(x, x, 1, PLATE - 1, sz1, sz1, "post")
    m.box(sx0, sx1, PLATE, PLATE, sz1, sz1, "beam_x")
    m.box(sx1, sx1, 2, 3, 3, 3, "pane")
    # the roof: ridge along x, its eave level with the wall heads, the north eave clipped at the plot's edge
    m.roof(sx0, sx1, sz0, sz1, PLATE, "x", "deepslate_tile", fill="boards", ridge="ridge")
    for c in [c for c in list(m.v) if c[2] < Z0 or (c[0] < X0 and c[1] > 0)]:
        del m.v[c]
    # inside: the bench and vice, the steam box over its fire, tar, oars, plank stock
    m.set(3, 1, 2, "bench")
    m.set(4, 1, 2, "vice")
    m.set(7, 1, 2, "steam")
    m.set(7, 3, 2, "steam_box")
    m.set(8, 3, 2, "steam_box")
    m.set(8, 1, 2, "tar")
    m.box(3, 3, 1, 3, 4, 4, "oars")
    m.box(6, 8, 1, 1, 4, 4, "planks_stack")
    m.set(4, 1, 4, "barrel")
    m.box(sx0 + 1, sx1 - 1, PLATE, PLATE, 3, 3, "beam_x")
    m.set(5, PLATE - 1, 3, "lantern_h")

    # ---------- the boat on its stocks, side-on to the lane: a long narrow hull, its stem
    # rising to a point at the bow (east), a raked transom at the stern (west); the sheer
    # climbs toward both ends in half steps (slabs on the gunwale), the turn of the bilge is
    # upturned stairs, and the stern half still stands in bare frames on its ribband
    townkit.hull_on_stocks(m, "x", HULL_X[0] + 1, HULL_X[1], KZ, 2, framed=3, stocks=(5, 8, 11))
    m.set(12, 1, 5, "lantern")            # a lantern on the yard's timber, by the bow

    # ---------- the yard: timber stacked to season, the winch at the slip head
    m.box(11, 12, 1, 1, 1, 4, "timber_z")
    m.box(11, 12, 2, 2, 1, 3, "timber_z")
    m.box(11, 11, 3, 3, 2, 3, "timber_z")
    m.box(13, 13, 1, 1, 1, 2, "timber_x")
    m.set(13, 1, 5, "winch")
    m.set(13, 2, 5, "winch_bar")
    m.set(13, 1, 4, "barrel")
    m.set(10, 1, 4, "barrel")
    m.set(10, 2, 4, "barrel")
    m.set(1, 1, 9, "pot_a")

    townkit.close_edge_gaps(m, X0, X1, Z0, Z1, "boards")
    m.finish()
    m.part(sx0, sx1, sz0, sz1, "shed")
    m.part(10, 13, 1, 5, "yard")
    m.part(2, 13, 6, 7, "yard")
    m.mark("node-boatwright", 6, 3, "south")
    return m


if __name__ == "__main__":
    raise SystemExit(run(build, reason="the shed's wall heads and roof and the boat's gunwale: seen, never stood on"))
