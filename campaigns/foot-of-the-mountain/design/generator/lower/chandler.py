#!/usr/bin/env python3
"""The ship chandler's: a long shop-and-store gable-end to the street, a
hoist loft over the store, and a yard of rope coils, barrels and a handcart.

Form, after harbour chandleries and community warehouse builds (references
in the node's `references[]`): the shop takes the street end, its door and
a bowed display window in the gable; the counter stands across the shop,
the goods behind it; a door in the cross wall leads to the long store,
racked with barrels, coils and blocks, with a loading door and a hoist beam
on the yard side. Stone below, weatherboard above, a deepslate roof.

    "$DELVEWRIGHT_PYTHON" chandler.py --allocation <allocation.json> --out <campaign>/programs/chandler.json --delvec <delvec>

Drawn into the skill's starter (`$DELVEWRIGHT_SKILL/scripts/starter.py`),
which binds the handing and asks the engine where a body goes.

Piece-local: +x east (the street), +z south; y 0 the ground course, y 1 the walk plane.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
from starter import Model, run  # noqa: E402


def hsh(*a):
    h = 2166136261
    for v in a:
        h = ((h ^ (v & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    return h


def st(name, facing, half="bottom"):
    return f"minecraft:{name}_stairs[facing={facing},half={half},shape=straight,waterlogged=false]"


def td(wood, facing, half="bottom", open_=False):
    return f"minecraft:{wood}_trapdoor[facing={facing},half={half},open={str(open_).lower()},powered=false,waterlogged=false]"


def door(m, x, y, z, block, facing, hinge="left"):
    for dy, half in ((0, "lower"), (1, "upper")):
        m.set(x, y + dy, z, f"{block}[facing={facing},half={half},hinge={hinge},open=false,powered=false]")


def gable_x(m, x0, x1, z0, z1, y0, stair, ridge, fill=None, ov=1):
    """A pitched roof over [x0..x1]x[z0..z1], the ridge along x, overhanging `ov`."""
    lo, hi, k = z0 - ov, z1 + ov, 0
    while lo <= hi:
        y = y0 + k
        if lo == hi:
            m.box(x0 - ov, x1 + ov, y, y, lo, lo, ridge)
        else:
            m.box(x0 - ov, x1 + ov, y, y, lo, lo, stair + "_s")
            m.box(x0 - ov, x1 + ov, y, y, hi, hi, stair + "_n")
            if fill and lo + 1 <= hi - 1:
                for x in (x0, x1):
                    m.box(x, x, y, y, max(lo + 1, z0), min(hi - 1, z1), fill)
        lo, hi, k = lo + 1, hi - 1, k + 1


def gable_z(m, x0, x1, z0, z1, y0, stair, ridge, fill=None, ov=1):
    """A pitched roof over [x0..x1]x[z0..z1], the ridge along z."""
    lo, hi, k = x0 - ov, x1 + ov, 0
    while lo <= hi:
        y = y0 + k
        if lo == hi:
            m.box(lo, lo, y, y, z0 - ov, z1 + ov, ridge)
        else:
            m.box(lo, lo, y, y, z0 - ov, z1 + ov, stair + "_e")
            m.box(hi, hi, y, y, z0 - ov, z1 + ov, stair + "_w")
            if fill and lo + 1 <= hi - 1:
                for z in (z0, z1):
                    m.box(max(lo + 1, x0), min(hi - 1, x1), y, y, z, z, fill)
        lo, hi, k = lo + 1, hi - 1, k + 1


PALETTE = {
    "turf": "minecraft:grass_block[snowy=false]",
    "pave": [{"weight": 5, "block": "minecraft:cobblestone"}, {"weight": 3, "block": "minecraft:stone_bricks"},
             {"weight": 1, "block": "minecraft:andesite"}],
    "yard": [{"weight": 4, "block": "minecraft:gravel"}, {"weight": 3, "block": "minecraft:packed_mud"},
             {"weight": 2, "block": "minecraft:coarse_dirt"}],
    "boards": "minecraft:spruce_planks",
    "rubble": [{"weight": 6, "block": "minecraft:cobblestone"}, {"weight": 4, "block": "minecraft:stone_bricks"},
               {"weight": 1, "block": "minecraft:mossy_cobblestone"}],
    "quoin": "minecraft:tuff_bricks",
    "weather": "minecraft:stripped_spruce_wood[axis=x]",
    "weather_z": "minecraft:stripped_spruce_wood[axis=z]",
    "post": "minecraft:spruce_log[axis=y]",
    "beam_x": "minecraft:spruce_log[axis=x]",
    "beam_z": "minecraft:spruce_log[axis=z]",
    "lintel": "minecraft:polished_tuff",
    "pane": "minecraft:glass_pane[east=false,north=false,south=false,waterlogged=false,west=false]",
    "roof_n": st("deepslate_tile", "north"), "roof_s": st("deepslate_tile", "south"),
    "roof_e": st("deepslate_tile", "east"), "roof_w": st("deepslate_tile", "west"),
    "ridge": "minecraft:deepslate_tile_slab[type=bottom,waterlogged=false]",
    "loft": "minecraft:spruce_planks",
    "hoist": "minecraft:dark_oak_fence[east=false,north=false,south=false,waterlogged=false,west=false]",
    "rope": "minecraft:iron_chain[axis=y,waterlogged=false]",
    "pulley": "minecraft:dark_oak_log[axis=z]",
    # the shop
    "counter": "minecraft:stripped_spruce_wood[axis=y]",
    "counter_top": "minecraft:spruce_slab[type=bottom,waterlogged=false]",
    "shelf": "minecraft:spruce_trapdoor[facing=east,half=top,open=false,powered=false,waterlogged=false]",
    "lantern": "minecraft:lantern[hanging=false,waterlogged=false]",
    "lantern_h": "minecraft:lantern[hanging=true,waterlogged=false]",
    "barrel": "minecraft:barrel[facing=up,open=false]",
    "barrel_e": "minecraft:barrel[facing=east,open=false]",
    "barrel_n": "minecraft:barrel[facing=north,open=false]",
    "coil": "minecraft:brown_wool",
    "coil_flat": "minecraft:brown_carpet",
    "canvas": "minecraft:white_wool",
    "block_pulley": "minecraft:stripped_oak_log[axis=y]",
    "chart": "minecraft:cartography_table",
    "bell": "minecraft:lantern[hanging=false,waterlogged=false]",
    # the yard: an anchor, rope coils, a handcart
    "anchor_shank": "minecraft:iron_bars[east=false,north=false,south=false,waterlogged=false,west=false]",
    "anchor_crown": "minecraft:iron_block",
    "cart_bed": "minecraft:spruce_slab[type=top,waterlogged=false]",
    "cart_wheel_n": td("dark_oak", "north", "bottom", True),
    "cart_wheel_s": td("dark_oak", "south", "bottom", True),
    "cart_handle": "minecraft:spruce_fence[east=false,north=false,south=false,waterlogged=false,west=false]",
    "pot_a": "minecraft:potted_red_tulip", "pot_b": "minecraft:potted_blue_orchid",
    "bush": "minecraft:azalea_leaves[distance=1,persistent=true,waterlogged=false]",
    "f1": "minecraft:poppy", "f2": "minecraft:oxeye_daisy", "f3": "minecraft:cornflower", "fern": "minecraft:fern",
    "tuft": "minecraft:short_grass", "bed_soil": "minecraft:rooted_dirt",
}

HOUSE = (6, 17, 3, 8)     # walls included; the street gable at x 17, its eave clear of the seam
CROSS = 12                # shop east of it, store west
TOP = 4                   # wall plate


def build(place):
    m = Model(place)
    m.palette.update(PALETTE)
    lo, hi = place.space
    X0, X1, Z0, Z1 = lo[0], hi[0], lo[2], hi[2]
    hx0, hx1, hz0, hz1 = HOUSE
    for x in range(X0, X1 + 1):
        for z in range(Z0, Z1 + 1):
            m.set(x, 0, z, "turf")
    m.box(hx1 + 1, X1, 0, 0, Z0 + 1, Z1 - 1, "pave")
    m.box(X0, hx0 - 1, 0, 0, Z0 + 1, Z1 - 1, "yard")
    m.box(hx0, hx1, 0, 0, hz1 + 1, Z1 - 1, "yard")

    # ---------- the range: rubble below, weatherboard above, tuff quoins
    m.box(hx0, hx1, 0, 0, hz0, hz1, "boards")
    for y in range(1, TOP + 1):
        role = "rubble" if y <= 2 else None
        for x in range(hx0, hx1 + 1):
            for z in (hz0, hz1):
                m.set(x, y, z, role or "weather")
        for z in range(hz0, hz1 + 1):
            for x in (hx0, hx1):
                m.set(x, y, z, role or "weather_z")
    for x in (hx0, hx1):
        for z in (hz0, hz1):
            m.box(x, x, 1, TOP, z, z, "quoin")
    m.box(hx0 + 1, hx1 - 1, TOP, TOP, hz0, hz0, "beam_x")
    m.box(hx0 + 1, hx1 - 1, TOP, TOP, hz1, hz1, "beam_x")
    # the cross wall with its door
    m.box(CROSS, CROSS, 1, TOP, hz0 + 1, hz1 - 1, "weather_z")
    door(m, CROSS, 1, 5, "minecraft:spruce_door", "east")
    # the street gable: the door and the display window, one lintel over both
    door(m, hx1, 1, 6, "minecraft:spruce_door", "west")
    m.box(hx1, hx1, 2, 3, 4, 4, "pane")
    m.box(hx1, hx1, 1, 1, 4, 4, "barrel_e")
    m.box(hx1, hx1, TOP, TOP, hz0 + 1, hz1 - 1, "lintel")
    # windows along the sides; the store's loading door to the yard, the hoist over it
    for x in (14, 16):
        m.box(x, x, 2, 3, hz0, hz0, "pane")
        m.box(x, x, 2, 3, hz1, hz1, "pane")
    m.box(8, 8, 2, 3, hz0, hz0, "pane")
    door(m, 9, 1, hz1, "minecraft:spruce_door", "north")
    # the roof: ridge along x; the store's half carries a loft with a hoist door
    gable_x(m, hx0, hx1, hz0, hz1, TOP + 1, "roof", "ridge", fill="weather_z")
    m.box(hx0 + 1, CROSS - 1, TOP + 1, TOP + 1, hz0 + 1, hz1 - 1, "loft")
    m.clear(7, 7, TOP + 2, TOP + 3, hz1, hz1)          # the loft door in the south slope's gable
    m.set(7, TOP + 2, hz1, td("spruce", "north", "bottom", True))
    m.set(7, TOP + 4, hz1 + 1, "hoist")
    m.set(7, TOP + 4, hz1, "pulley")
    m.set(7, TOP + 3, hz1 + 1, "rope")
    m.set(7, TOP + 2, hz1 + 1, "rope")

    # ---------- the shop: the counter across it, goods behind on the cross wall
    for z in range(hz0 + 1, hz1):
        if z != 6:
            m.set(15, 1, z, "counter")
    m.set(15, 2, 4, "lantern")
    m.set(13, 1, 4, "coil")
    m.set(13, 2, 4, "coil_flat")
    m.set(13, 1, 7, "barrel_n")
    m.set(14, 1, 7, "chart")
    m.set(13, 1, 6, "block_pulley")
    for z in (4, 7):
        m.set(CROSS + 1, 3, z, "shelf")
    m.box(hx0 + 1, hx1 - 1, TOP, TOP, 6, 6, "beam_x")
    m.set(16, TOP - 1, 6, "lantern_h")

    # ---------- the long store: barrels racked along both walls, coils, canvas
    for x in range(7, CROSS):
        m.set(x, 1, 4, "barrel_e" if x % 2 else "barrel")
        if x != 9:
            m.set(x, 1, 7, "barrel" if x % 2 else "barrel_n")
        if x % 2:
            m.set(x, 2, 4, "barrel")
    m.set(10, 1, 7, "coil")
    m.set(10, 2, 7, "coil")
    m.set(11, 1, 7, "canvas")
    m.set(9, TOP - 1, 5, "lantern_h")
    m.box(hx0 + 1, CROSS - 1, TOP, TOP, 5, 5, "beam_x")

    # ---------- the yard: an anchor, coils of rope, a handcart, barrels
    m.set(3, 1, 4, "anchor_crown")
    m.box(3, 3, 2, 3, 4, 4, "anchor_shank")
    m.set(2, 1, 7, "coil")
    m.set(2, 2, 7, "coil_flat")
    m.set(3, 1, 7, "coil")
    # the handcart: a slab bed on two wheels, its handle toward the store
    m.box(4, 5, 1, 1, 9, 9, "cart_bed")
    m.set(6, 1, 9, "cart_handle")
    for (x, z) in ((11, 9), (12, 9), (13, 9), (14, 9)):
        m.set(x, 1, z, "barrel")
    m.set(12, 2, 9, "barrel")
    m.set(2, 1, 2, "bush")
    m.set(19, 1, 2, "pot_a")
    m.set(19, 1, 9, "pot_b")
    for x in range(hx0, hx1):
        m.set(x, 0, Z0, "bed_soil")
        m.set(x, 1, Z0, ["f1", "f2", "f3", "fern"][hsh(x, 1, 3) % 4])

    m.finish()
    m.part(hx0, hx1, hz0, hz1, "shop")
    m.part(X0, hx0 - 1, Z0 + 1, Z1 - 1, "yard")
    m.part(hx0, 15, hz1 + 1, Z1 - 1, "yard")
    m.mark("node-chandler", 16, 5, "west")   # in the shop before the counter, facing the goods
    return m


if __name__ == "__main__":
    raise SystemExit(run(build, reason="the range's wall heads, its roof and the loft over the store: seen, never stood on"))
