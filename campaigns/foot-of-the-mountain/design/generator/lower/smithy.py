#!/usr/bin/env python3
"""The smithy: an open-walled forge shed under a deep roof, the smith's house
behind it, and the work yard between them.

Form, after community smithies (references in the node's `references[]`):
the forge is a shed of posts and a beam, open to the street and to the yard,
with a solid masonry back wall that carries the hearth, its hood and the
chimney; the anvil stands in front of the hearth with the grindstone and the
smithing table to hand, the quench trough at the shed's edge where the yard
begins. The house stands behind, a stone plinth and a timber frame with
plaster infill, a front room entered from the yard through a porch and a
back kitchen through an inner door. The yard between them holds the stacked
iron and the coal, a bench and flower beds by the house wall.

    python3 smithy.py --allocation <allocation.json> --out <campaign>/programs/smithy.json

Piece-local: +x east (the street), +z south; y 0 the ground course, y 1 the walk plane.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from plotkit import Model, Plot, door, door_roles, finish, flower_bed, frame_walls, gable, hsh, run  # noqa: E402


def st(name, facing, half="bottom"):
    return f"minecraft:{name}_stairs[facing={facing},half={half},shape=straight,waterlogged=false]"


PALETTE = {
    # the starter's roles
    "floor": "minecraft:stone_bricks",
    "wall": "minecraft:stone_bricks",
    "lid": "minecraft:spruce_planks",
    "lamp": "minecraft:lantern[hanging=false,waterlogged=false]",
    "turf": "minecraft:grass_block[snowy=false]",
    "pot_a": "minecraft:potted_red_tulip", "pot_b": "minecraft:potted_cornflower",
    "pot_c": "minecraft:potted_azure_bluet", "pot_d": "minecraft:potted_fern",
    # ground
    "yard": [{"weight": 5, "block": "minecraft:coarse_dirt"}, {"weight": 3, "block": "minecraft:gravel"},
             {"weight": 2, "block": "minecraft:cobblestone"}, {"weight": 1, "block": "minecraft:packed_mud"}],
    "pave": [{"weight": 6, "block": "minecraft:cobblestone"}, {"weight": 3, "block": "minecraft:stone_bricks"},
             {"weight": 1, "block": "minecraft:andesite"}],
    "forge_floor": [{"weight": 4, "block": "minecraft:cobblestone"}, {"weight": 2, "block": "minecraft:cobbled_deepslate"},
                    {"weight": 1, "block": "minecraft:tuff"}],
    "boards": "minecraft:spruce_planks",
    "bed_soil": "minecraft:rooted_dirt",
    # masonry: the town's stone brick, tuff dressings
    "stone": [{"weight": 10, "block": "minecraft:stone_bricks"}, {"weight": 2, "block": "minecraft:cracked_stone_bricks"},
              {"weight": 1, "block": "minecraft:mossy_stone_bricks"}],
    "quoin": "minecraft:tuff_bricks",
    "plinth": "minecraft:cobblestone",
    "brick": "minecraft:bricks",
    "hearth": "minecraft:polished_blackstone_bricks",
    "hood_e": st("brick", "east", "top"),
    # timber and plaster
    "post": "minecraft:stripped_dark_oak_log[axis=y]",
    "beam_x": "minecraft:dark_oak_log[axis=x]",
    "beam_z": "minecraft:dark_oak_log[axis=z]",
    "plaster": "minecraft:white_terracotta",
    "gable_boards": "minecraft:spruce_planks",
    "pane": "minecraft:glass_pane[east=false,north=false,south=false,waterlogged=false,west=false]",
    "sill_n": st("spruce", "north", "top"),
    "shutter": "minecraft:spruce_trapdoor[facing=north,half=bottom,open=true,powered=false,waterlogged=false]",
    # roofs: deepslate tiles over the house, as the cathedral's; the forge in spruce shingle
    "roof_n": st("deepslate_tile", "north"), "roof_s": st("deepslate_tile", "south"),
    "roof_e": st("deepslate_tile", "east"), "roof_w": st("deepslate_tile", "west"),
    "ridge": "minecraft:deepslate_tile_slab[type=bottom,waterlogged=false]",
    "shed_n": st("spruce", "north"), "shed_s": st("spruce", "south"),
    "shed_ridge": "minecraft:spruce_slab[type=bottom,waterlogged=false]",
    "porch_roof": "minecraft:spruce_slab[type=bottom,waterlogged=false]",
    "fence": "minecraft:dark_oak_fence[east=false,north=false,south=false,waterlogged=false,west=false]",
    # the forge's working objects
    "fire": "minecraft:campfire[facing=east,lit=true,signal_fire=false,waterlogged=false]",
    "anvil": "minecraft:anvil[facing=north]",
    "grindstone": "minecraft:grindstone[face=floor,facing=east]",
    "smithing": "minecraft:smithing_table",
    "quench": "minecraft:water_cauldron[level=3]",
    "coal": "minecraft:coal_block",
    "iron": "minecraft:iron_block",
    "bars": "minecraft:iron_bars[east=false,north=false,south=false,waterlogged=false,west=false]",
    "chain": "minecraft:iron_chain[axis=y,waterlogged=false]",
    "bellows": "minecraft:brown_wool",
    "bellows_top": "minecraft:spruce_trapdoor[facing=west,half=bottom,open=false,powered=false,waterlogged=false]",
    "lantern": "minecraft:lantern[hanging=false,waterlogged=false]",
    "lantern_h": "minecraft:lantern[hanging=true,waterlogged=false]",
    # the house's rooms
    "table": "minecraft:spruce_planks",
    "table_top": "minecraft:spruce_pressure_plate[powered=false]",
    "chair_w": st("spruce", "west"), "chair_e": st("spruce", "east"),
    "chair_n": st("spruce", "north"), "chair_s": st("spruce", "south"),
    "barrel": "minecraft:barrel[facing=up,open=false]",
    "barrel_side": "minecraft:barrel[facing=east,open=false]",
    "pot": "minecraft:cauldron",
    "worktop": "minecraft:crafting_table",
    "shelf": "minecraft:bookshelf",
    "rug": "minecraft:red_carpet",
    "bed_foot": "minecraft:red_bed[facing=south,occupied=false,part=foot]",
    "bed_head": "minecraft:red_bed[facing=south,occupied=false,part=head]",
    "hay": "minecraft:hay_block[axis=y]",
    "log_z": "minecraft:spruce_log[axis=z]",
    # life outside
    "bush": "minecraft:azalea_leaves[distance=1,persistent=true,waterlogged=false]",
    "bush_f": "minecraft:flowering_azalea_leaves[distance=1,persistent=true,waterlogged=false]",
    "bench": st("spruce", "west"),
    "bench_arm_n": "minecraft:spruce_trapdoor[facing=north,half=bottom,open=true,powered=false,waterlogged=false]",
    "bench_arm_s": "minecraft:spruce_trapdoor[facing=south,half=bottom,open=true,powered=false,waterlogged=false]",
    "f1": "minecraft:poppy", "f2": "minecraft:oxeye_daisy", "f3": "minecraft:cornflower",
    "f4": "minecraft:red_tulip", "f5": "minecraft:allium",
    "tuft": "minecraft:short_grass", "fern": "minecraft:fern",
}
door_roles(PALETTE, "door_front", "minecraft:spruce_door", "west")
door_roles(PALETTE, "door_inner", "minecraft:spruce_door", "east", hinge="right")

# ---- the plan, piece-local ----
HOUSE = (2, 10, 2, 7)        # x0, x1, z0, z1: walls included
BAY = (6, 10, 8, 9)          # the front bay toward the yard, its south gable at z 9
PARTITION = 6                # the timber wall between kitchen (west) and front room (east)
FORGE = (14, 20, 2, 7)       # the shed's posts
PORCH = (11, 12, 4, 6)
WALL_TOP = 4                 # the house's wall plate course
SHED_PLATE = 4


def build(place) -> Model:
    m = Model(dict(PALETTE))
    lo, hi = place.space
    X0, X1, Z0, Z1 = lo[0], hi[0], lo[2], hi[2]

    # ---------- the ground
    for x in range(X0, X1 + 1):
        for z in range(Z0, Z1 + 1):
            m.set(x, 0, z, "turf")
    # the way in from the street: paving up to the forge front and into the yard
    m.box(21, X1, 0, 0, 3, 10, "pave")
    m.box(11, 21, 0, 0, 8, 11, "yard")
    m.box(13, 13, 0, 0, 4, 6, "yard")
    m.box(PORCH[0], PORCH[1], 0, 0, PORCH[2], PORCH[3], "pave")

    # ---------- the house: plinth, timber frame, plaster; an L of the main range
    # and a gabled front bay toward the yard
    hx0, hx1, hz0, hz1 = HOUSE
    bx0, bx1, bz0, bz1 = BAY
    m.box(hx0, hx1, 0, 0, hz0, hz1, "stone")
    m.box(bx0, bx1, 0, 0, bz0, bz1, "stone")
    frame_walls(m, hx0, hx1, hz0, hz1, 1, WALL_TOP, "post", "plaster", "beam_x", "beam_z", bay=4, plinth="plinth")
    frame_walls(m, bx0, bx1, hz1, bz1, 1, WALL_TOP, "post", "plaster", "beam_x", "beam_z", bay=2, plinth="plinth")
    m.box(hx0 + 1, hx1 - 1, 0, 0, hz0 + 1, hz1 - 1, "boards")
    m.box(bx0 + 1, bx1 - 1, 0, 0, hz1, bz1 - 1, "boards")
    # the front room runs on into the bay: the main range's south wall opens there
    m.box(bx0 + 1, bx1 - 1, 1, WALL_TOP - 1, hz1, hz1, "~air")
    # the partition, with its door
    frame_walls(m, PARTITION, PARTITION, hz0, hz1, 1, WALL_TOP, "post", "plaster", "beam_x", "beam_z", bay=8)
    door(m, PARTITION, 1, 5, "door_inner")
    # the front door in the east wall, onto the porch
    door(m, hx1, 1, 5, "door_front")
    # windows: two courses of glazing; onto the open sides and the yard
    for x in (4, 8):
        m.box(x, x, 2, 3, hz0, hz0, "pane")
    m.box(4, 4, 2, 3, hz1, hz1, "pane")
    for x in (bx0 + 1, bx1 - 1):
        m.box(x, x, 2, 3, bz1, bz1, "pane")
    m.box(bx1, bx1, 2, 3, bz0, bz0, "pane")
    for z in (4, 6):
        m.box(hx0, hx0, 2, 3, z, z, "pane")
    m.box(hx1, hx1, 2, 3, 3, 3, "pane")
    # the roofs: deepslate tiles, the main ridge along x, the bay's along z, plaster gables
    gable(m, hx0, hx1, hz0, hz1, WALL_TOP + 1, "x", "roof", "ridge", fill="plaster")
    gable(m, bx0, bx1, bz0, bz1, WALL_TOP + 1, "z", "roof", "ridge", fill="plaster")
    m.box(bx0 + 1, bx1 - 1, WALL_TOP + 1, WALL_TOP + 1, hz1, hz1, "~air")
    # the kitchen chimney on the west gable
    m.box(hx0, hx0, 1, 10, 5, 5, "brick")

    # ---------- the house's rooms
    # kitchen (west): smoker and pot at the hearth wall, a worktop and a table
    m.set(3, 1, 3, "hearth")
    m.set(3, 2, 3, "fire")
    m.set(3, 1, 4, "pot")
    m.set(3, 1, 6, "worktop")
    m.set(5, 1, 3, "shelf")
    m.set(4, 1, 6, "table")
    m.set(4, 2, 6, "lantern")
    m.set(5, 1, 6, "chair_w")
    # front room (east), running into the bay: the table by the bay window, a shelf, a rug
    m.set(8, 1, 8, "table")
    m.set(8, 2, 8, "lantern")
    m.set(7, 1, 8, "chair_e")
    m.set(9, 1, 8, "chair_w")
    m.set(7, 1, 3, "shelf")
    m.set(8, 1, 3, "shelf")
    m.box(7, 8, 1, 1, 5, 6, "rug")
    # hanging lanterns from a tie beam
    m.box(hx0 + 1, hx1 - 1, WALL_TOP, WALL_TOP, 4, 4, "beam_x")
    m.set(4, WALL_TOP - 1, 4, "lantern_h")
    m.set(8, WALL_TOP - 1, 4, "lantern_h")

    # ---------- the porch on the front door: two posts and a slab roof
    px0, px1, pz0, pz1 = PORCH
    for z in (pz0, pz1):
        m.box(px1, px1, 1, 3, z, z, "fence")
        m.set(px1, 4, z, "post")
    m.box(px0, px1, 4, 4, pz0, pz1, "porch_roof")
    m.box(px1, px1, 4, 4, pz0 + 1, pz1 - 1, "beam_z")
    m.set(px0, 1, pz0, "bench_arm_n")

    # ---------- the forge: posts and a beam, open to the street and the yard
    fx0, fx1, fz0, fz1 = FORGE
    m.box(fx0, fx1, 0, 0, fz0, fz1, "forge_floor")
    for x in (fx0, 17, fx1):
        for z in (fz0, fz1):
            m.box(x, x, 1, SHED_PLATE - 1, z, z, "post")
    m.box(fx0, fx1, SHED_PLATE, SHED_PLATE, fz0, fz0, "beam_x")
    m.box(fx0, fx1, SHED_PLATE, SHED_PLATE, fz1, fz1, "beam_x")
    m.box(fx1, fx1, SHED_PLATE, SHED_PLATE, fz0, fz1, "beam_z")
    # the back wall: masonry carrying the hearth, quoined in tuff
    m.box(fx0, fx0, 1, SHED_PLATE, fz0, fz1, "stone")
    for z in (fz0, fz1):
        m.box(fx0, fx0, 1, SHED_PLATE, z, z, "quoin")
    # the north side: a breast-high wall of stone to the beam's first post
    m.box(fx0 + 1, 16, 1, 1, fz0, fz0, "stone")
    # the hearth: a raised fire bed of blackstone with the fire in it, a brick hood
    m.box(fx0 + 1, fx0 + 1, 1, 1, 3, 5, "hearth")
    m.set(fx0 + 1, 2, 4, "fire")
    m.set(fx0 + 1, 2, 3, "bellows")
    m.set(fx0 + 1, 3, 3, "bellows_top")
    m.box(fx0 + 1, fx0 + 1, SHED_PLATE, SHED_PLATE, 3, 5, "hood_e")
    m.set(fx0 + 1, 3, 4, "~air")
    # the chimney rises from the back wall through the roof
    m.box(fx0, fx0, 1, 10, 4, 4, "brick")
    # the working objects: the anvil before the hearth, the tools to hand
    m.set(17, 1, 4, "anvil")
    m.set(fx0 + 1, 1, 6, "coal")
    m.set(19, 1, 3, "grindstone")
    m.set(19, 1, 7, "quench")
    m.set(18, 1, 7, "quench")
    # tongs and hammers: chains from the beam, a lantern hung over the anvil
    m.set(17, 3, 2, "chain")
    m.set(18, SHED_PLATE, 4, "beam_z")
    m.box(18, 18, SHED_PLATE, SHED_PLATE, fz0, fz1, "beam_z")
    m.set(18, SHED_PLATE - 1, 4, "lantern_h")
    # the shed roof: spruce, ridge along x, deep overhang, boarded gable to the street
    gable(m, fx0, fx1, fz0, fz1, SHED_PLATE, "x", "shed", "shed_ridge", fill=None)
    for k, y in enumerate(range(SHED_PLATE + 1, SHED_PLATE + 4)):
        for z in range(fz0 + 1 + k, fz1 - k):
            if m.get(fx1, y, z) is None:
                m.set(fx1, y, z, "gable_boards")
                m.set(fx0, y, z, "stone")
    m.box(fx0, fx0, 1, 10, 4, 4, "brick")

    # ---------- the work yard: stacked iron, coal, the smithing table, a bench
    m.set(12, 1, 10, "iron")
    m.set(13, 1, 10, "iron")
    m.set(12, 2, 10, "bars")
    m.set(14, 1, 10, "coal")
    m.set(15, 1, 10, "coal")
    m.set(14, 2, 10, "coal")
    m.set(17, 1, 10, "smithing")
    m.set(20, 1, 10, "hay")
    m.set(19, 1, 10, "barrel")
    m.set(18, 1, 10, "barrel")
    m.set(19, 2, 10, "barrel")
    m.set(20, 2, 10, "lantern")
    # a bench facing the street under the forge eave
    m.set(22, 1, 2, "bench")
    m.set(22, 1, 1, "bench_arm_n")
    m.set(22, 1, 3, "bench_arm_s")

    # ---------- life: flower beds under the house windows, bushes, the woodpile
    flower_bed(m, 3, 5, 8, 9, ["f1", "f2", "f3", "f4", "f5", "fern"])
    flower_bed(m, 3, 9, 11, 11, ["f2", "f4", "fern", "f1"])
    flower_bed(m, 3, 9, 1, 1, ["f2", "f3", "fern", "tuft", "f5"])
    m.box(13, 13, 1, 2, 2, 3, "log_z")
    for (x, z, r) in ((2, 10, "bush"), (11, 10, "bush_f"), (11, 2, "bush_f"), (22, 10, "bush")):
        m.set(x, 1, z, r)
    for x in range(1, 24):
        for z in (1, 10):
            if m.get(x, 1, z) is None and m.get(x, 0, z) == "turf" and hsh(x, z, 3) % 3 == 0:
                m.set(x, 1, z, "tuft")

    # potted flowers: on the porch either side of the door, on the bay's sill wall, by the bench
    m.set(11, 1, 6, "pot_a")
    m.set(8, 2, 3, "pot_b")
    m.set(22, 1, 4, "pot_c")
    finish(m)

    # ---------- the parts: which columns are which
    m.regions("house", hx0, hx1, hz0, hz1)
    m.regions("house", bx0, bx1, bz0, bz1)
    m.regions("forge", fx0, fx1, fz0, fz1)
    m.regions("work-yard", 11, 21, 8, 11)
    m.regions("work-yard", 13, 13, 4, 7)
    m.regions("work-yard", 21, 22, 2, 7)
    return m


class Smithy(Plot):
    MODEL = staticmethod(build)
    MARK_AT = {"node-smithy": (18, 4, "west")}    # at the anvil, facing the hearth
    REASON = "the house's and the forge's wall heads, roof slopes and sills: seen, never stood on"


if __name__ == "__main__":
    raise SystemExit(run(Smithy))
