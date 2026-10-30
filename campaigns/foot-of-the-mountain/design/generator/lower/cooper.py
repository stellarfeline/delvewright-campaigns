#!/usr/bin/env python3
"""The cooper's: an open-fronted cooperage on the street, the family house
beside it, and the barrel yard behind both.

Form, after community coopers' workshops and the cooper's work sequence
(references in the node's `references[]`): the workshop is a shed of posts
and a beam, its front open to the street so the work is seen from the way:
the shaving horse where staves are shaped, the truss of staves standing in
its hoop, the cresset fire a barrel is bent over, finished casks by the
wall. The house beside it is stone below and timber above, a hall and a
kitchen joined by a door. The yard behind holds the barrels, stacked.

    python3 cooper.py --allocation <allocation.json> --out <campaign>/programs/cooper.json

Piece-local: +x east, +z south, the street on the west; y 0 the ground course, y 1 the walk plane.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from plotkit import Model, Plot, door, door_roles, finish, frame_walls, gable, hsh, run  # noqa: E402


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
    "pot_a": "minecraft:potted_red_tulip", "pot_b": "minecraft:potted_dandelion",
    "barrel": "minecraft:barrel[facing=up,open=false]",
    "barrel_e": "minecraft:barrel[facing=east,open=false]",
    "barrel_n": "minecraft:barrel[facing=north,open=false]",
    # ground
    "pave": [{"weight": 5, "block": "minecraft:cobblestone"}, {"weight": 3, "block": "minecraft:stone_bricks"},
             {"weight": 1, "block": "minecraft:andesite"}],
    "yard": [{"weight": 4, "block": "minecraft:packed_mud"}, {"weight": 3, "block": "minecraft:coarse_dirt"},
             {"weight": 2, "block": "minecraft:gravel"}],
    "shavings": [{"weight": 3, "block": "minecraft:spruce_planks"}, {"weight": 2, "block": "minecraft:stripped_oak_wood[axis=y]"},
                 {"weight": 2, "block": "minecraft:coarse_dirt"}],
    "boards": "minecraft:oak_planks",
    # the workshop: oak posts and beam, a solid back wall of boards
    "post": "minecraft:oak_log[axis=y]",
    "hpost": "minecraft:dark_oak_log[axis=y]",
    "hbeam_x": "minecraft:dark_oak_log[axis=x]",
    "hbeam_z": "minecraft:dark_oak_log[axis=z]",
    "beam_x": "minecraft:oak_log[axis=x]",
    "beam_z": "minecraft:oak_log[axis=z]",
    "back": "minecraft:dark_oak_planks",
    "shingle_n": st("spruce", "north"), "shingle_s": st("spruce", "south"),
    "shingle_ridge": "minecraft:spruce_slab[type=bottom,waterlogged=false]",
    # the house: stone below, oak frame and plaster above
    "stone": [{"weight": 8, "block": "minecraft:stone_bricks"}, {"weight": 3, "block": "minecraft:cobblestone"},
              {"weight": 1, "block": "minecraft:tuff"}],
    "quoin": "minecraft:tuff_bricks",
    "plaster": "minecraft:white_terracotta",
    "pane": "minecraft:glass_pane[east=false,north=false,south=false,waterlogged=false,west=false]",
    "roof_n": st("deepslate_tile", "north"), "roof_s": st("deepslate_tile", "south"),
    "roof_e": st("deepslate_tile", "east"), "roof_w": st("deepslate_tile", "west"),
    "ridge": "minecraft:deepslate_tile_slab[type=bottom,waterlogged=false]",
    "chimney": "minecraft:bricks",
    # the cooper's work
    "horse_seat": st("oak", "east"),
    "horse_clamp": td("oak", "west", "top", False),
    "staves": "minecraft:stripped_spruce_log[axis=x]",
    "stave_stack": "minecraft:spruce_slab[type=bottom,waterlogged=false]",
    "truss": "minecraft:iron_chain[axis=y,waterlogged=false]",
    "hoop": "minecraft:iron_bars[east=false,north=false,south=false,waterlogged=false,west=false]",
    "cresset": "minecraft:campfire[facing=east,lit=true,signal_fire=false,waterlogged=false]",
    "jointer": "minecraft:stripped_oak_wood[axis=x]",
    "bench": "minecraft:crafting_table",
    "tub": "minecraft:water_cauldron[level=3]",
    "lantern": "minecraft:lantern[hanging=false,waterlogged=false]",
    "lantern_h": "minecraft:lantern[hanging=true,waterlogged=false]",
    # the house's rooms
    "table": "minecraft:oak_planks",
    "chair_e": st("oak", "east"), "chair_w": st("oak", "west"),
    "hearth": "minecraft:bricks",
    "fire": "minecraft:campfire[facing=south,lit=true,signal_fire=false,waterlogged=false]",
    "rug": "minecraft:green_carpet",
    "shelf": "minecraft:bookshelf",
    "bed_foot": "minecraft:green_bed[facing=north,occupied=false,part=foot]",
    "bed_head": "minecraft:green_bed[facing=north,occupied=false,part=head]",
    "pot": "minecraft:cauldron",
    "worktop": "minecraft:crafting_table",
    # life
    "bush": "minecraft:oak_leaves[distance=1,persistent=true,waterlogged=false]",
    "f1": "minecraft:poppy", "f2": "minecraft:allium", "f3": "minecraft:oxeye_daisy",
    "fern": "minecraft:fern", "tuft": "minecraft:short_grass", "bed_soil": "minecraft:rooted_dirt",
    "bench_out": st("oak", "west"),
}
door_roles(PALETTE, "door_front", "minecraft:oak_door", "east")
door_roles(PALETTE, "door_inner", "minecraft:oak_door", "west", hinge="right")
door_roles(PALETTE, "door_yard", "minecraft:oak_door", "north")

SHOP = (4, 9, 2, 7)        # the workshop's posts; open to the street at x 4
HOUSE = (12, 19, 2, 7)     # walls included
PARTITION = 16             # hall west, kitchen east
PLATE = 4


def build(place) -> Model:
    m = Model(dict(PALETTE))
    lo, hi = place.space
    X0, X1, Z0, Z1 = lo[0], hi[0], lo[2], hi[2]
    for x in range(X0, X1 + 1):
        for z in range(Z0, Z1 + 1):
            m.set(x, 0, z, "turf")
    wx0, wx1, wz0, wz1 = SHOP
    hx0, hx1, hz0, hz1 = HOUSE
    m.box(X0, wx0 - 1, 0, 0, Z0 + 1, Z1 - 1, "pave")
    m.box(wx1 + 1, hx0 - 1, 0, 0, Z0 + 1, Z1 - 1, "yard")
    m.box(wx0, X1 - 1, 0, 0, 8, 9, "yard")

    # ---------- the workshop: posts and a beam, open to the street, a boarded back wall
    m.box(wx0, wx1, 0, 0, wz0, wz1, "shavings")
    for x in (wx0, 7, wx1):
        for z in (wz0, wz1):
            m.box(x, x, 1, PLATE - 1, z, z, "post")
    for z in (wz0, wz1):
        m.box(wx0, wx1, PLATE, PLATE, z, z, "beam_x")
    m.box(wx0, wx0, PLATE, PLATE, wz0, wz1, "beam_z")
    m.box(wx1, wx1, 1, PLATE, wz0 + 1, wz1 - 1, "back")
    m.box(wx1, wx1, 1, 2, wz0 + 1, wz1 - 1, "stone")      # a stone footing under the boards
    # the north side half-boarded, the south side open to the yard
    m.box(wx0 + 1, wx1 - 1, 1, 2, wz0, wz0, "stone")
    gable(m, wx0, wx1, wz0, wz1, PLATE + 1, "x", "shingle", "shingle_ridge", fill="back")
    # clear the street gable under the beam: the front stays open
    m.box(wx0, wx0, 1, PLATE - 1, wz0 + 1, wz1 - 1, "~air")
    # the work: shaving horse, stave truss in its hoop over the cresset, the jointer, casks
    m.set(5, 1, 3, "horse_seat")
    m.set(6, 1, 3, "horse_clamp")
    m.set(6, 1, 5, "cresset")
    m.set(6, 2, 5, "~air")
    m.set(6, 3, 5, "hoop")
    m.set(6, PLATE, 5, "beam_z")
    m.box(6, 6, PLATE, PLATE, wz0, wz1, "beam_z")
    m.set(8, 1, 3, "jointer")
    m.set(8, 1, 6, "barrel")
    m.set(8, 2, 6, "barrel")
    m.set(7, 1, 6, "barrel_e")
    m.set(8, 1, 5, "tub")
    m.set(6, PLATE - 1, 4, "lantern_h")      # hung from the tie beam over the work (DW1002: it needs a beam above)

    # ---------- the house: stone ground course, oak frame and plaster, deepslate roof
    m.box(hx0, hx1, 0, 0, hz0, hz1, "boards")
    # the house: a stone ground storey to the sill, plaster in a dark frame above,
    # so it reads apart from the oak workshop
    frame_walls(m, hx0, hx1, hz0, hz1, 1, PLATE, "hpost", "plaster", "hbeam_x", "hbeam_z", bay=3, plinth="stone")
    for x in range(hx0, hx1 + 1):
        for z in range(hz0, hz1 + 1):
            if x in (hx0, hx1) or z in (hz0, hz1):
                m.set(x, 2, z, "stone")
    for x in (hx0, hx1):
        for z in (hz0, hz1):
            m.box(x, x, 1, 2, z, z, "quoin")
    frame_walls(m, PARTITION, PARTITION, hz0, hz1, 1, PLATE, "post", "plaster", bay=8)
    door(m, hx0, 1, 5, "door_front")
    door(m, PARTITION, 1, 4, "door_inner")
    door(m, 17, 1, hz1, "door_yard")
    for x in (14, 18):
        m.box(x, x, 2, 3, hz0, hz0, "pane")
    m.box(14, 14, 2, 3, hz1, hz1, "pane")
    m.box(hx1, hx1, 2, 3, 4, 5, "pane")
    gable(m, hx0, hx1, hz0, hz1, PLATE + 1, "x", "roof", "ridge", fill="plaster")
    m.box(17, 17, 1, 10, hz0, hz0, "chimney")
    # hall: table and chairs by the window, a rug, the bed in the corner
    m.set(14, 1, 3, "table")
    m.set(14, 2, 3, "lantern")
    m.set(13, 1, 3, "chair_e")
    m.set(15, 1, 3, "chair_w")
    m.box(13, 14, 1, 1, 5, 5, "rug")
    m.set(15, 1, 6, "bed_foot")
    m.set(15, 1, 5, "bed_head")
    m.set(13, 1, 6, "shelf")
    # kitchen: the hearth under the chimney, the pot, the worktop
    m.set(17, 1, 3, "hearth")
    m.set(17, 2, 3, "fire")
    m.set(18, 1, 5, "worktop")
    m.set(18, 1, 6, "barrel")
    m.box(hx0 + 1, hx1 - 1, PLATE, PLATE, 4, 4, "beam_x")
    m.set(14, PLATE - 1, 4, "lantern_h")
    m.set(18, PLATE - 1, 4, "lantern_h")

    # ---------- the barrel yard: casks stacked two high along the back, a path to the yard door
    for x in range(wx0 + 1, 15):
        if x in (10, 11):
            continue
        m.set(x, 1, 9, "barrel_n" if x % 3 else "barrel")
        if x % 2 == 0:
            m.set(x, 2, 9, "barrel")
    for x in (20, 21):
        m.set(x, 1, 8, "barrel")
        m.set(x, 1, 9, "barrel")
    m.set(20, 2, 9, "barrel")
    # staves stacked to season between the workshop and the house
    m.box(10, 11, 1, 1, 2, 3, "staves")
    m.box(10, 11, 2, 2, 2, 2, "stave_stack")
    # life: flower beds under the house windows, a bench by the front door, potted flowers
    for x in range(hx0, hx1 + 1):
        m.set(x, 0, 1, "bed_soil")
        m.set(x, 1, 1, ["f1", "f2", "f3", "fern"][hsh(x, 1, 5) % 4])
    m.set(11, 1, 6, "pot_a")
    m.set(11, 1, 4, "pot_b")
    m.set(21, 1, 3, "bush")
    m.set(21, 1, 6, "bush")
    for x in range(X0, X1 + 1):
        for z in (Z0, Z1):
            if m.get(x, 1, z) is None and m.get(x, 0, z) == "turf" and hsh(x, z, 9) % 3 == 0:
                m.set(x, 1, z, "tuft")

    finish(m)
    m.regions("workshop", wx0, wx1, wz0, wz1)
    m.regions("house", hx0, hx1, hz0, hz1)
    m.regions("yard", 10, 11, 2, 7)
    m.regions("yard", wx0, 21, 8, 9)
    return m


class Cooper(Plot):
    MODEL = staticmethod(build)
    MARK_AT = {"node-cooper": (5, 5, "east")}    # in the open front, facing the cresset
    REASON = "the workshop's and the house's wall heads and roofs: seen, never stood on"


if __name__ == "__main__":
    raise SystemExit(run(Cooper))
