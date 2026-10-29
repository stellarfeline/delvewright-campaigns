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
from plotkit import Model, Plot, door, door_roles, finish, flower_bed, hip, hsh, run  # noqa: E402


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
    "smoker": "minecraft:smoker[facing=west,lit=false]",
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
HOUSE = (4, 15, 2, 8)      # walls included
CROSS = 11                 # the cross wall: taproom west, back room east
GARDEN = (17, 23, 2, 9)    # the pergola's posts
TOP = 4                    # wall plate course


def build(place) -> Model:
    m = Model(dict(PALETTE))
    lo, hi = place.space
    X0, X1, Z0, Z1 = lo[0], hi[0], lo[2], hi[2]
    for x in range(X0, X1 + 1):
        for z in range(Z0, Z1 + 1):
            m.set(x, 0, z, "turf")
    hx0, hx1, hz0, hz1 = HOUSE
    # the forecourt: paving from the street to the door, benches under the eave
    m.box(X0, hx0 - 1, 0, 0, Z0 + 1, Z1 - 1, "pave")
    # ---------- the house: rubble walls, tuff quoins
    m.box(hx0, hx1, 0, 0, hz0, hz1, "boards")
    for x in range(hx0, hx1 + 1):
        for z in range(hz0, hz1 + 1):
            if x in (hx0, hx1) or z in (hz0, hz1):
                corner = x in (hx0, hx1) and z in (hz0, hz1)
                for y in range(1, TOP + 1):
                    m.set(x, y, z, "quoin" if corner and (y % 2 == 1) else "rubble")
    m.box(hx0, hx0, 0, 0, hz0, hz1, "rubble")
    # the cross wall in timber and plaster-coloured stone, with its door
    for z in range(hz0 + 1, hz1):
        for y in range(1, TOP + 1):
            m.set(CROSS, y, z, "post" if z in (hz0 + 1, hz1 - 1) else "rubble")
    door(m, CROSS, 1, 5, "door_inner")
    # the front: the door between two wide windows, one lintel course over all
    door(m, hx0, 1, 5, "door_front")
    for z in (3, 4, 6, 7):
        m.box(hx0, hx0, 2, 3, z, z, "pane")
    m.box(hx0, hx0, TOP, TOP, hz0 + 1, hz1 - 1, "lintel")
    # side and back windows onto the open sides and the garden
    for x in (6, 13):
        m.box(x, x, 2, 3, hz0, hz0, "pane")
    for x in (6, 8, 13):
        m.box(x, x, 2, 3, hz1, hz1, "pane")
    m.box(hx1, hx1, 2, 3, 3, 3, "pane")
    door(m, hx1, 1, 6, "door_back")
    # the taproom's fireplace in the north wall, its chimney through the roof
    m.box(8, 8, 1, 11, hz0, hz0, "chimney")
    m.set(8, 1, hz0 + 1, "hearth")
    m.set(8, 2, hz0 + 1, "fire")
    m.set(8, TOP, hz0 + 1, "hearth")
    # the hipped roof
    hip(m, hx0, hx1, hz0, hz1, TOP + 1, "roof", "ridge")
    # tie beams across under the plate
    for x in (7, 13):
        m.box(x, x, TOP, TOP, hz0 + 1, hz1 - 1, "beam_z")
        m.set(x, TOP - 1, 5, "lantern_h")

    # ---------- the taproom: bar counter along the cross wall, kegs behind
    for z in (4, 6):
        m.set(9, 1, z, "counter")
    m.set(9, 2, 4, "lantern")
    for z in (3, 4, 6, 7):
        m.set(10, 1, z, "keg")
    m.set(10, 2, 3, "keg")
    m.set(10, 2, 7, "lantern")
    # tables and stools
    for (tx, tz) in ((6, 3), (6, 7)):
        m.set(tx, 1, tz, "table_leg")
        m.set(tx, 2, tz, "table_top")
        m.set(tx - 1, 1, tz, "stool_e")
        m.set(tx + 1, 1, tz, "stool_w")
    m.box(6, 7, 1, 1, 5, 5, "rug")
    # ---------- the back room: the vats, the mash tun, the cellar hatch
    m.set(14, 1, 3, "vat")
    m.set(14, 1, 4, "vat")
    m.set(12, 1, 3, "mash")
    m.set(14, 1, 7, "sack")
    m.set(14, 2, 7, "sack")
    m.set(13, 1, 7, "worktop")
    m.set(12, 1, 7, "hatch")
    m.set(13, 2, 7, "lantern")

    # ---------- the front: benches under the eave either side of the door
    m.set(hx0 - 1, 1, 3, "bench_w")
    m.set(hx0 - 1, 1, 7, "bench_w")
    m.set(hx0 - 1, 1, 2, "arm_n")
    m.set(hx0 - 1, 1, 8, "arm_s")

    # ---------- the garden: gravel, a pergola of posts and beams roofed in leaves
    gx0, gx1, gz0, gz1 = GARDEN
    m.box(hx1 + 1, gx1, 0, 0, gz0, gz1, "gravel")
    m.box(hx1 + 1, hx1 + 1, 0, 0, 5, 7, "flags")
    for x in (gx0, 20, gx1):
        for z in (gz0, 5, gz1):
            if (x, z) == (20, 5):
                continue
            m.box(x, x, 1, 3, z, z, "pg_post")
    for z in (gz0, 5, gz1):
        m.box(gx0, gx1, 4, 4, z, z, "pg_beam_x")
    for x in range(gx0, gx1 + 1):
        if (x - gx0) % 2 == 1:
            m.box(x, x, 4, 4, gz0 + 1, gz1 - 1, "pg_slat")
            for z in (gz0 + 1, gz1 - 1):
                m.set(x, 4, z, "pg_slat")
    for x in range(gx0, gx1 + 1):
        for z in range(gz0, gz1 + 1):
            if m.get(x, 4, z) and hsh(x, z, 11) % 5 < 3:
                m.set(x, 5, z, "vine_bloom" if hsh(x, z, 2) % 4 == 0 else "vine_leaf")
    # tables under the pergola, benches either side
    for (tx, tz) in ((18, 3), (22, 3), (18, 7), (22, 7)):
        m.set(tx, 1, tz, "table_leg")
        m.set(tx, 2, tz, "table_top")
        m.set(tx, 1, tz - 1, "bench_s")
        m.set(tx, 1, tz + 1, "bench_n")
    for (x, z) in ((20, 3), (20, 7)):
        m.set(x, 3, z, "lantern_h")
        m.set(x, 4, z, "pg_beam_x") if m.get(x, 4, z) is None else None
    # flower beds along the garden's north and south edges, a lilac at the gate
    for x in range(16, 24):
        for z in (1, 10):
            m.set(x, 0, z, "bed_soil")
            m.set(x, 1, z, ["f1", "f2", "f3", "f4", "f5", "fern", "tuft"][hsh(x, z, 5) % 7])
    m.set(16, 1, 3, "lilac")
    m.set(16, 2, 3, "lilac_top")
    m.set(16, 1, 8, "bush")
    for x in range(X0, X1 + 1):
        for z in (Z0, Z1):
            if m.get(x, 1, z) is None and m.get(x, 0, z) == "turf" and hsh(x, z, 9) % 3 == 0:
                m.set(x, 1, z, "tuft")

    # potted flowers along the front, either side of the door, and on the garden tables
    m.set(3, 1, 4, "pot_a")
    m.set(3, 1, 6, "pot_b")
    m.set(16, 1, 7, "pot_d")
    m.set(16, 1, 4, "pot_c")
    finish(m)
    m.regions("tavern", hx0, hx1, hz0, hz1)
    m.regions("garden", hx1 + 1, gx1, gz0, gz1)
    return m


class Tavern(Plot):
    MODEL = staticmethod(build)
    MARK_AT = {"node-tavern": (8, 5, "east")}    # in the taproom, facing the bar
    REASON = "the tavern's wall heads, roof and the pergola's top: seen, never stood on"


if __name__ == "__main__":
    raise SystemExit(run(Tavern))
