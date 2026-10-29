#!/usr/bin/env python3
"""The tavern: a low sailors' tavern on the street, a beer garden under a vine
pergola behind it.

Form, after community taverns (references in the node's `references[]`): a
long low house under a hipped roof of deepslate tiles, its walls of rubble
stone dressed with tuff at the corners and openings, the front to the street
with the door between two wide windows and benches under the eaves. Inside,
the taproom a visitor enters holds the bar counter and the tables; a door in
the cross wall leads to the back room where the ale is brewed and the cellar
hatch stands; a back door opens onto the garden, where tables stand under a
pergola of posts and beams roofed in leaves, edged with flower beds.

    python3 tavern.py --allocation <allocation.json> --out <campaign>/programs/tavern.json

Piece-local: +x east, +z south, the street on the west; y 0 the ground course, y 1 the walk plane.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from plotkit import Model, Plot, door, door_roles, finish, gable, hsh, run  # noqa: E402


def st(name, facing, half="bottom"):
    return f"minecraft:{name}_stairs[facing={facing},half={half},shape=straight,waterlogged=false]"


def td(wood, facing, half="bottom", open_=False):
    return f"minecraft:{wood}_trapdoor[facing={facing},half={half},open={str(open_).lower()},powered=false,waterlogged=false]"


PALETTE = {
    "floor": "minecraft:stone_bricks",
    "wall": "minecraft:stone_bricks",
    "lid": "minecraft:spruce_planks",
    "lamp": "minecraft:lantern[hanging=false,waterlogged=false]",
    "turf": "minecraft:grass_block[snowy=false]",
    "pot_a": "minecraft:potted_red_tulip", "pot_b": "minecraft:potted_cornflower",
    "pot_c": "minecraft:potted_azure_bluet", "pot_d": "minecraft:potted_fern",
    # ground
    "pave": [{"weight": 6, "block": "minecraft:cobblestone"}, {"weight": 3, "block": "minecraft:stone_bricks"},
             {"weight": 1, "block": "minecraft:mossy_cobblestone"}],
    "gravel": [{"weight": 4, "block": "minecraft:gravel"}, {"weight": 2, "block": "minecraft:coarse_dirt"},
               {"weight": 1, "block": "minecraft:packed_mud"}],
    "boards": "minecraft:spruce_planks",
    "flags": "minecraft:polished_andesite",
    "bed_soil": "minecraft:rooted_dirt",
    # rubble walls, tuff dressings
    "rubble": [{"weight": 6, "block": "minecraft:cobblestone"}, {"weight": 4, "block": "minecraft:stone_bricks"},
               {"weight": 2, "block": "minecraft:andesite"}, {"weight": 1, "block": "minecraft:mossy_cobblestone"}],
    "quoin": "minecraft:tuff_bricks",
    "lintel": "minecraft:polished_tuff",
    "beam_x": "minecraft:dark_oak_log[axis=x]",
    "beam_z": "minecraft:dark_oak_log[axis=z]",
    "post": "minecraft:stripped_spruce_log[axis=y]",
    "pane": "minecraft:glass_pane[east=false,north=false,south=false,waterlogged=false,west=false]",
    "sill_w": st("tuff_brick", "east", "top"),
    "shutter_n": td("spruce", "north", open_=True),
    "shutter_s": td("spruce", "south", open_=True),
    # the hipped roof
    "roof_n": st("deepslate_tile", "north"), "roof_s": st("deepslate_tile", "south"),
    "roof_e": st("deepslate_tile", "east"), "roof_w": st("deepslate_tile", "west"),
    "ridge": "minecraft:deepslate_tile_slab[type=bottom,waterlogged=false]",
    "chimney": "minecraft:bricks",
    # the taproom
    "counter": "minecraft:stripped_spruce_wood[axis=y]",
    "counter_top": "minecraft:spruce_slab[type=bottom,waterlogged=false]",
    "table_leg": "minecraft:spruce_fence[east=false,north=false,south=false,waterlogged=false,west=false]",
    "table_top": "minecraft:spruce_pressure_plate[powered=false]",
    "stool_e": st("spruce", "east"), "stool_w": st("spruce", "west"),
    "stool_n": st("spruce", "north"), "stool_s": st("spruce", "south"),
    "keg": "minecraft:spruce_log[axis=x]",
    "tap": "minecraft:tripwire_hook[attached=false,facing=west,powered=false]",
    "candle": "minecraft:candle[candles=3,lit=true,waterlogged=false]",
    "lantern": "minecraft:lantern[hanging=false,waterlogged=false]",
    "lantern_h": "minecraft:lantern[hanging=true,waterlogged=false]",
    "hearth": "minecraft:bricks",
    "fire": "minecraft:campfire[facing=east,lit=true,signal_fire=false,waterlogged=false]",
    "rug": "minecraft:brown_carpet",
    # the back room
    "vat": "minecraft:water_cauldron[level=3]",
    "mash": "minecraft:cauldron",
    "barrel": "minecraft:barrel[facing=up,open=false]",
    "barrel_side": "minecraft:barrel[facing=east,open=false]",
    "hatch": td("spruce", "north"),
    "sack": "minecraft:hay_block[axis=y]",
    "worktop": "minecraft:crafting_table",
    # the garden and its pergola
    "pg_post": "minecraft:spruce_fence[east=false,north=false,south=false,waterlogged=false,west=false]",
    "pg_beam_x": "minecraft:stripped_spruce_log[axis=x]",
    "pg_slat": "minecraft:spruce_slab[type=top,waterlogged=false]",
    "vine_leaf": "minecraft:azalea_leaves[distance=1,persistent=true,waterlogged=false]",
    "vine_bloom": "minecraft:flowering_azalea_leaves[distance=1,persistent=true,waterlogged=false]",
    "bench_n": st("spruce", "north"), "bench_s": st("spruce", "south"),
    "bench_w": st("spruce", "west"),
    "arm_n": td("spruce", "north", open_=True), "arm_s": td("spruce", "south", open_=True),
    "bush": "minecraft:oak_leaves[distance=1,persistent=true,waterlogged=false]",
    "f1": "minecraft:poppy", "f2": "minecraft:oxeye_daisy", "f3": "minecraft:blue_orchid",
    "f4": "minecraft:pink_tulip", "f5": "minecraft:azure_bluet", "fern": "minecraft:fern",
    "tuft": "minecraft:short_grass",
    "lilac": "minecraft:lilac[half=lower]", "lilac_top": "minecraft:lilac[half=upper]",
}
door_roles(PALETTE, "door_front", "minecraft:spruce_door", "east")
door_roles(PALETTE, "door_inner", "minecraft:spruce_door", "west", hinge="right")
door_roles(PALETTE, "door_back", "minecraft:spruce_door", "west")

# ---- the plan ----
HOUSE = (4, 12, 2, 11)     # the taproom's range, walls included; the street gable faces west
WING = (12, 15, 3, 9)      # the back room's cross wing, sharing the range's east wall
GARDEN = (17, 23, 2, 11)   # the pergola's posts
TOP = 4                    # wall plate course


def rubble_box(m, x0, x1, z0, z1):
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if x in (x0, x1) or z in (z0, z1):
                corner = x in (x0, x1) and z in (z0, z1)
                for y in range(1, TOP + 1):
                    m.set(x, y, z, "quoin" if corner and (y % 2 == 1) else "rubble")


def table(m, x, z, n=4):
    """A table with a stool on each of its free sides."""
    m.set(x, 1, z, "table_leg")
    m.set(x, 2, z, "table_top")
    for (dx, dz, r) in ((-1, 0, "stool_e"), (1, 0, "stool_w"), (0, -1, "stool_s"), (0, 1, "stool_n"))[:n]:
        if m.get(x + dx, 1, z + dz) is None:
            m.set(x + dx, 1, z + dz, r)


def build(place) -> Model:
    m = Model(dict(PALETTE))
    lo, hi = place.space
    X0, X1, Z0, Z1 = lo[0], hi[0], lo[2], hi[2]
    for x in range(X0, X1 + 1):
        for z in range(Z0, Z1 + 1):
            m.set(x, 0, z, "turf")
    hx0, hx1, hz0, hz1 = HOUSE
    wx0, wx1, wz0, wz1 = WING
    gx0, gx1, gz0, gz1 = GARDEN
    # the forecourt: paving from the street to the door, benches under the eave
    m.box(X0, hx0 - 1, 0, 0, Z0 + 1, Z1 - 1, "pave")

    # ---------- the range: rubble walls, tuff quoins, the street gable over the door
    m.box(hx0, hx1, 0, 0, hz0, hz1, "boards")
    rubble_box(m, hx0, hx1, hz0, hz1)
    m.box(hx0, hx0, 0, 0, hz0, hz1, "rubble")
    # the back room's wing on the east, its door through the range's east wall
    m.box(wx0, wx1, 0, 0, wz0, wz1, "flags")
    for x in range(wx0 + 1, wx1 + 1):
        for z in range(wz0, wz1 + 1):
            if x == wx1 or z in (wz0, wz1):
                for y in range(1, TOP + 1):
                    m.set(x, y, z, "quoin" if x == wx1 and z in (wz0, wz1) and y % 2 else "rubble")
    door(m, hx1, 1, 6, "door_inner")
    # the front: the door between two wide windows, one lintel course over all
    door(m, hx0, 1, 6, "door_front")
    for z in (3, 4, 8, 9):
        m.box(hx0, hx0, 2, 3, z, z, "pane")
    m.box(hx0, hx0, TOP, TOP, hz0 + 1, hz1 - 1, "lintel")
    # side windows onto the open north and south, a window from the wing onto the garden
    for x in (6, 9):
        m.box(x, x, 2, 3, hz0, hz0, "pane")
    m.box(10, 10, 2, 3, hz1, hz1, "pane")
    m.box(wx1, wx1, 2, 3, 5, 5, "pane")
    door(m, wx1, 1, 7, "door_back")
    # the fireplace in the south wall, its chimney through the roof
    m.box(7, 7, 1, 12, hz1, hz1, "chimney")
    m.set(7, 1, hz1 - 1, "hearth")
    m.set(7, 2, hz1 - 1, "fire")
    m.set(7, TOP, hz1 - 1, "hearth")
    # the roofs: the range's ridge along the street, a cross gable over the front door,
    # the wing's ridge along x into the range's slope
    gable(m, hx0, hx1, hz0, hz1, TOP + 1, "z", "roof", "ridge", fill="rubble")
    gable(m, wx0, wx1, wz0, wz1, TOP + 1, "x", "roof", "ridge", fill="rubble")
    gable(m, hx0, hx0 + 3, 5, 7, TOP + 1, "x", "roof", "ridge", fill="beam_z")
    # tie beams, lanterns hung from them
    for z in (5, 8):
        m.box(hx0 + 1, hx1 - 1, TOP, TOP, z, z, "beam_x")
        m.set(6, TOP - 1, z, "lantern_h")
        m.set(10, TOP - 1, z, "lantern_h")

    # ---------- the taproom: the bar along the north wall, barrels behind, tables round the room
    for x in range(8, 12):
        m.set(x, 1, 5, "counter")
    m.set(8, 2, 5, "lantern")
    for x in range(8, 12):
        m.set(x, 1, 3, "barrel_side")
    m.set(9, 2, 3, "barrel_side")
    m.set(11, 2, 3, "barrel_side")
    table(m, 6, 8)
    table(m, 10, 9)
    m.box(5, 5, 1, 1, 4, 5, "stool_e")
    m.set(6, 1, 4, "table_leg")
    m.set(6, 2, 4, "table_top")
    m.box(8, 9, 1, 1, 7, 7, "rug")

    # ---------- the back room: the vats, the mash tun, sacks, the cellar hatch
    m.set(13, 1, 4, "vat")
    m.set(14, 1, 4, "vat")
    m.set(14, 1, 8, "mash")
    m.set(13, 1, 8, "sack")
    m.set(13, 2, 8, "sack")
    m.set(14, 1, 6, "hatch")
    m.set(13, TOP - 1, 6, "lantern_h")
    m.box(wx0 + 1, wx1 - 1, TOP, TOP, 6, 6, "beam_z")

    # ---------- the front: benches under the eave either side of the door, potted flowers
    m.set(hx0 - 1, 1, 3, "bench_w")
    m.set(hx0 - 1, 1, 9, "bench_w")
    m.set(hx0 - 1, 1, 2, "arm_n")
    m.set(hx0 - 1, 1, 4, "arm_s")
    m.set(hx0 - 1, 1, 8, "arm_n")
    m.set(hx0 - 1, 1, 10, "arm_s")
    m.set(hx0 - 1, 1, 5, "pot_a")
    m.set(hx0 - 1, 1, 7, "pot_b")

    # ---------- the garden: gravel, a pergola of posts and beams roofed in leaves
    m.box(wx1 + 1, gx1, 0, 0, gz0, gz1, "gravel")
    m.box(wx1 + 1, wx1 + 1, 0, 0, 6, 8, "flags")
    for x in (gx0, 20, gx1):
        for z in (gz0, 6, gz1):
            if (x, z) == (20, 6):
                continue
            m.box(x, x, 1, 3, z, z, "pg_post")
    for z in (gz0, 6, gz1):
        m.box(gx0, gx1, 4, 4, z, z, "pg_beam_x")
    for x in range(gx0, gx1 + 1):
        if (x - gx0) % 2 == 1:
            m.box(x, x, 4, 4, gz0 + 1, gz1 - 1, "pg_slat")
    for x in range(gx0, gx1 + 1):
        for z in range(gz0, gz1 + 1):
            if m.get(x, 4, z) and hsh(x, z, 11) % 5 < 3:
                m.set(x, 5, z, "vine_bloom" if hsh(x, z, 2) % 4 == 0 else "vine_leaf")
    for (tx, tz) in ((18, 4), (22, 4), (18, 9), (22, 9)):
        m.set(tx, 1, tz, "table_leg")
        m.set(tx, 2, tz, "table_top")
        m.set(tx, 1, tz - 1, "bench_s")
        m.set(tx, 1, tz + 1, "bench_n")
    for (x, z) in ((20, 4), (20, 9)):
        m.set(x, 4, z, "pg_beam_x")   # a hanging lantern needs a full face above it
        m.set(x, 3, z, "lantern_h")
    m.set(gx1, 1, 7, "barrel")
    m.set(gx1, 1, 8, "barrel")
    # flower edges along the garden's open sides, a lilac by the back door
    for x in range(wx1 + 1, gx1 + 1):
        for z in (Z0, Z1):
            m.set(x, 0, z, "bed_soil")
            m.set(x, 1, z, ["f1", "f2", "f3", "f4", "f5", "fern", "tuft"][hsh(x, z, 5) % 7])
    m.set(16, 0, 3, "turf")
    m.set(16, 1, 3, "lilac")
    m.set(16, 2, 3, "lilac_top")
    m.set(16, 1, 10, "bush")
    for x in range(X0, X1 + 1):
        for z in (Z0, Z1):
            if m.get(x, 1, z) is None and m.get(x, 0, z) == "turf" and hsh(x, z, 9) % 3 == 0:
                m.set(x, 1, z, "tuft")

    finish(m)
    m.regions("tavern", hx0, hx1, hz0, hz1)
    m.regions("tavern", wx0 + 1, wx1, wz0, wz1)
    m.regions("garden", wx1 + 1, gx1, gz0, gz1)
    return m


class Tavern(Plot):
    MODEL = staticmethod(build)
    MARK_AT = {"node-tavern": (6, 6, "east")}    # in the taproom, facing the bar
    REASON = "the tavern's wall heads, roof and the pergola's top: seen, never stood on"


if __name__ == "__main__":
    raise SystemExit(run(Tavern))
