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

Drawn into the skill's starter alone (`$DELVEWRIGHT_SKILL/scripts/starter.py`:
its Model, its block constructors and Model.roof), which binds the handing
and asks the engine where a body goes.

Piece-local: +x east (the street), +z south; y 0 the ground course, y 1 the walk plane.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
from starter import (Model, barrel, chain, fence, grass_block, lantern, leaves, pane, pillar, run,  # noqa: E402
                     slab, trapdoor)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # the town kit, one up
import townkit  # noqa: E402


PALETTE = {
    "turf": grass_block(),
    "pave": [{"weight": 5, "block": "minecraft:cobblestone"}, {"weight": 3, "block": "minecraft:stone_bricks"},
             {"weight": 1, "block": "minecraft:andesite"}],
    "yard": [{"weight": 4, "block": "minecraft:gravel"}, {"weight": 3, "block": "minecraft:packed_mud"},
             {"weight": 2, "block": "minecraft:coarse_dirt"}],
    "boards": "minecraft:spruce_planks",
    "rubble": [{"weight": 6, "block": "minecraft:cobblestone"}, {"weight": 4, "block": "minecraft:stone_bricks"},
               {"weight": 1, "block": "minecraft:mossy_cobblestone"}],
    "quoin": "minecraft:tuff_bricks",
    "weather": pillar("stripped_spruce_wood", "x"),
    "weather_z": pillar("stripped_spruce_wood", "z"),
    "post": pillar("spruce_log", "y"),
    "beam_x": pillar("spruce_log", "x"),
    "beam_z": pillar("spruce_log", "z"),
    "lintel": "minecraft:polished_tuff",
    "coping": "minecraft:stone_brick_wall[east=none,north=none,south=none,up=true,waterlogged=false,west=none]",
    "pane": pane("glass_pane"),
    "ridge": slab("deepslate_tile"),
    "loft": "minecraft:spruce_planks",
    "hoist": fence("dark_oak"),
    "rope": chain("y"),
    # the shop
    "counter": pillar("stripped_spruce_wood", "y"),
    "counter_top": slab("spruce"),
    "shelf": trapdoor("spruce", "east", "top"),
    "lantern": lantern(),
    "lantern_h": lantern(hanging=True),
    "barrel": barrel("up"),
    "barrel_e": barrel("east"),
    "barrel_n": barrel("north"),
    "coil": "minecraft:brown_wool",
    "coil_flat": "minecraft:brown_carpet",
    "canvas": "minecraft:white_wool",
    "block_pulley": "minecraft:stripped_oak_log[axis=y]",
    "chart": "minecraft:cartography_table",
    "bell": lantern(),
    # the yard: an anchor, rope coils, a handcart
    "anchor_shank": pane("iron_bars"),
    "anchor_crown": "minecraft:iron_block",
    "cart_bed": slab("spruce", "top"),
    "cart_wheel_n": trapdoor("dark_oak", "north", "bottom", True),
    "cart_wheel_s": trapdoor("dark_oak", "south", "bottom", True),
    "cart_handle": fence("spruce"),
    "pot_a": "minecraft:potted_red_tulip", "pot_b": "minecraft:potted_blue_orchid",
    "bush": leaves("azalea"),
    "f1": "minecraft:poppy", "f2": "minecraft:oxeye_daisy", "f3": "minecraft:cornflower", "fern": "minecraft:fern",
    "tuft": "minecraft:short_grass", "bed_soil": "minecraft:rooted_dirt",
}

HOUSE = (6, 17, 3, 8)     # walls included; the street gable at x 17, its eave clear of the seam
CROSS = 11                # shop east of it, store west
TOP = 4                   # wall plate
FRONT_DX = 3              # fronted, the street gable is the lot's street edge


def build(place):
    m = Model(place)
    m.palette.update(PALETTE)
    lo, hi = place.space
    X0, X1, Z0, Z1 = lo[0], hi[0], lo[2], hi[2]
    hx0, hx1, hz0, hz1 = HOUSE
    for x in range(X0, X1 + 1):
        for z in range(Z0, Z1 + 1):
            m.set(x, 0, z, "turf")
    front, sf = townkit.street_seam(place, "east")
    townkit.shift(m, FRONT_DX if front else 0)
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
    m.door(CROSS, 1, 5, "spruce", "east")
    # the street gable: the door and the display window, one lintel over both
    if not front:
        m.door(hx1, 1, 6, "spruce", "west")
        m.box(hx1, hx1, 2, 3, 4, 4, "pane")
        m.box(hx1, hx1, 1, 1, 4, 4, "barrel_e")
    m.box(hx1, hx1, TOP, TOP, hz0 + 1, hz1 - 1, "lintel")
    # windows along the sides; the store's loading door to the yard, the hoist over it
    for x in (14, 16):
        m.box(x, x, 2, 3, hz0, hz0, "pane")
        m.box(x, x, 2, 3, hz1, hz1, "pane")
    m.box(8, 8, 2, 3, hz0, hz0, "pane")
    m.door(9, 1, hz1, "spruce", "north")
    # the roof: ridge along x, its eave level with the wall plate so the loft
    # under it closes; the store's half carries the loft, a hoist beam out of
    # the west gable over the yard
    m.roof(hx0, hx1, hz0, hz1, TOP, "x", "deepslate_tile", fill="weather_z", ridge="ridge")
    m.box(hx0 + 1, CROSS - 1, TOP + 1, TOP + 1, hz0 + 1, hz1 - 1, "loft")
    m.box(hx0 - 2, hx0 - 1, TOP + 2, TOP + 2, 5, 5, "hoist")
    m.box(hx0 - 2, hx0 - 2, TOP, TOP + 1, 5, 5, "rope")

    # ---------- the shop: the counter across it, the goods behind on the cross wall,
    # the chart table in the street window for the masters who come to buy
    for z in (4, 5, 6):
        m.set(14, 1, z, "counter")
    m.set(14, 2, 4, "lantern")
    m.set(14, 2, 6, "coil_flat")
    m.set(12, 1, 4, "coil")
    m.set(12, 2, 4, "coil")
    m.set(13, 1, 4, "coil")
    m.set(12, 1, 7, "block_pulley")
    m.set(12, 2, 7, "block_pulley")
    m.set(13, 1, 7, "barrel_n")
    for z in (4, 5, 6, 7):
        m.set(CROSS + 1, 3, z, "shelf")
    m.set(16, 1, 4, "chart")
    m.set(16, 1, 7, "barrel")
    m.set(16, 2, 7, "coil_flat")
    m.box(hx0 + 1, hx1 - 1, TOP, TOP, 6, 6, "beam_x")
    m.set(15, TOP - 1, 6, "lantern_h")
    m.set(13, TOP - 1, 6, "rope")
    m.set(13, TOP - 2, 6, "rope")

    # ---------- the long store: barrels racked along both walls, coils, canvas
    for x in range(7, CROSS):
        m.set(x, 1, 4, "barrel_e" if x % 2 else "barrel")
        if x != 9:
            m.set(x, 1, 7, "barrel" if x % 2 else "barrel_n")
        if x % 2:
            m.set(x, 2, 4, "barrel")
    m.set(10, 1, 7, "coil")
    m.set(10, 2, 7, "coil")
    m.set(8, 2, 7, "canvas")
    m.box(hx0 + 1, CROSS - 1, TOP, TOP, 5, 5, "beam_x")
    m.set(8, TOP - 1, 5, "lantern_h")

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
        m.set(x, 1, Z0, ["f1", "f2", "f3", "fern"][(x * 7 + 3) % 4])

    m.finish()
    m.part(hx0, hx1, hz0, hz1, "shop")
    m.part(X0, hx0 - 1, Z0 + 1, Z1 - 1, "yard")
    m.part(hx0, 15, hz1 + 1, Z1 - 1, "yard")
    m.mark("node-chandler", 15, 5, "west")   # in the shop before the counter, facing the goods
    townkit.shift(m, 0)
    if front:
        townkit.clip_beyond(m, X0, X1, Z0, Z1, above=-1)
        for c in [c for c in m.region if not (X0 <= c[0] <= X1)]:
            del m.region[c]
        edge, rows, door_h, air = sf
        townkit.street_front(m, edge, Z0, Z1, rows, air, {"wall": "weather_z", "lintel": "lintel", "coping": "coping"},
                             door_h=door_h, inward=-1)
        m.finish()
    return m


if __name__ == "__main__":
    raise SystemExit(run(build, reason="the range's wall heads, its roof and the loft over the store: seen, never stood on"))
