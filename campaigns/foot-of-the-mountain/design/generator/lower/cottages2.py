#!/usr/bin/env python3
"""A pair of fishermen's cottages: two small houses side by side, front
gardens to the lane, a shared yard between and behind them.

Form, after fisherfolk cottages and community cottage builds (references in
the node's `references[]`): each cottage one room deep, its door in the
front between small windows, a hearth on the gable wall, a bed, a table;
the two told apart by their walls (one whitewashed under a timber frame, one
of rubble stone), sharing one roof line. The front gardens are flower beds
either side of a path to each door behind a low hedge; the yard between
holds the washing, the woodpile and the water butt.

    python3 cottages2.py --allocation <allocation.json> --out <campaign>/programs/cottages-2.json

Piece-local: +x east, +z south, the lane on the north; y 0 the ground course, y 1 the walk plane.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from plotkit import Model, Plot, door, door_roles, finish, frame_walls, gable, hsh, run  # noqa: E402


def st(name, facing, half="bottom"):
    return f"minecraft:{name}_stairs[facing={facing},half={half},shape=straight,waterlogged=false]"


PALETTE = {
    "floor": "minecraft:stone_bricks",
    "wall": "minecraft:stone_bricks",
    "lid": "minecraft:spruce_planks",
    "lamp": "minecraft:lantern[hanging=false,waterlogged=false]",
    "turf": "minecraft:grass_block[snowy=false]",
    "pot_a": "minecraft:potted_red_tulip", "pot_b": "minecraft:potted_azure_bluet",
    "barrel": "minecraft:barrel[facing=up,open=false]",
    "path": [{"weight": 3, "block": "minecraft:cobblestone"}, {"weight": 2, "block": "minecraft:gravel"},
             {"weight": 1, "block": "minecraft:mossy_cobblestone"}],
    "yard": [{"weight": 3, "block": "minecraft:coarse_dirt"}, {"weight": 2, "block": "minecraft:gravel"}],
    "boards": "minecraft:spruce_planks",
    "bed_soil": "minecraft:rooted_dirt",
    # cottage A: whitewash under a spruce frame
    "post": "minecraft:stripped_spruce_log[axis=y]",
    "beam_x": "minecraft:spruce_log[axis=x]",
    "beam_z": "minecraft:spruce_log[axis=z]",
    "white": "minecraft:white_terracotta",
    # cottage B: rubble stone with tuff corners
    "rubble": [{"weight": 5, "block": "minecraft:cobblestone"}, {"weight": 3, "block": "minecraft:stone_bricks"},
               {"weight": 2, "block": "minecraft:andesite"}, {"weight": 1, "block": "minecraft:mossy_cobblestone"}],
    "quoin": "minecraft:tuff_bricks",
    "plinth": "minecraft:cobblestone",
    "pane": "minecraft:glass_pane[east=false,north=false,south=false,waterlogged=false,west=false]",
    "roof_n": st("deepslate_tile", "north"), "roof_s": st("deepslate_tile", "south"),
    "ridge": "minecraft:deepslate_tile_slab[type=bottom,waterlogged=false]",
    "chimney": "minecraft:bricks",
    # inside
    "hearth": "minecraft:bricks",
    "fire": "minecraft:campfire[facing=north,lit=true,signal_fire=false,waterlogged=false]",
    "bed_a_foot": "minecraft:blue_bed[facing=south,occupied=false,part=foot]",
    "bed_a_head": "minecraft:blue_bed[facing=south,occupied=false,part=head]",
    "bed_b_foot": "minecraft:yellow_bed[facing=south,occupied=false,part=foot]",
    "bed_b_head": "minecraft:yellow_bed[facing=south,occupied=false,part=head]",
    "table": "minecraft:spruce_planks",
    "chair": st("spruce", "west"),
    "lantern": "minecraft:lantern[hanging=false,waterlogged=false]",
    "lantern_h": "minecraft:lantern[hanging=true,waterlogged=false]",
    "rug_a": "minecraft:light_blue_carpet",
    "rug_b": "minecraft:orange_carpet",
    "net": "minecraft:cobweb",
    # the gardens and the yard
    "hedge": "minecraft:oak_leaves[distance=1,persistent=true,waterlogged=false]",
    "line_post": "minecraft:spruce_fence[east=false,north=false,south=false,waterlogged=false,west=false]",
    "sheet_a": "minecraft:white_wool",
    "sheet_b": "minecraft:light_blue_wool",
    "logs": "minecraft:oak_log[axis=z]",
    "butt": "minecraft:water_cauldron[level=3]",
    "f1": "minecraft:poppy", "f2": "minecraft:oxeye_daisy", "f3": "minecraft:cornflower",
    "f4": "minecraft:allium", "f5": "minecraft:pink_tulip", "fern": "minecraft:fern",
    "tuft": "minecraft:short_grass",
    "rose": "minecraft:rose_bush[half=lower]", "rose_top": "minecraft:rose_bush[half=upper]",
}
door_roles(PALETTE, "door_a", "minecraft:spruce_door", "south")
door_roles(PALETTE, "door_b", "minecraft:oak_door", "south")

A = (2, 6, 5, 9)     # walls included
B = (9, 13, 5, 9)
PLATE = 4


def cottage(m, box, wall, door_role, bed, rug, hearth_x, frame):
    x0, x1, z0, z1 = box
    m.box(x0, x1, 0, 0, z0, z1, "boards")
    if frame:
        frame_walls(m, x0, x1, z0, z1, 1, PLATE, "post", wall, "beam_x", "beam_z", bay=2, plinth="plinth")
    else:
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                if x in (x0, x1) or z in (z0, z1):
                    corner = x in (x0, x1) and z in (z0, z1)
                    for y in range(1, PLATE + 1):
                        m.set(x, y, z, "quoin" if corner and y % 2 else wall)
    cx = (x0 + x1) // 2
    door(m, cx, 1, z0, door_role)
    for x in (x0 + 1, x1 - 1):
        m.box(x, x, 2, 3, z0, z0, "pane")
    m.box(cx, cx, 2, 3, z1, z1, "pane")
    gable(m, x0, x1, z0, z1, PLATE + 1, "x", "roof", "ridge", fill=wall if not frame else "white")
    # the hearth on the gable wall, its chimney through the roof
    m.box(hearth_x, hearth_x, 1, 10, 7, 7, "chimney")
    ix = hearth_x + (1 if hearth_x == x0 else -1)
    m.set(ix, 1, 7, "hearth")
    m.set(ix, 2, 7, "fire")
    # the bed against the back wall, a table, a rug, a lantern
    other = x1 - 1 if hearth_x == x0 else x0 + 1
    m.set(other, 1, z1 - 2, bed + "_foot")
    m.set(other, 1, z1 - 1, bed + "_head")
    m.set(cx, 1, z1 - 1, "table")
    m.set(cx, 2, z1 - 1, "lantern")
    m.set(cx, 1, z0 + 2, rug)
    m.set(cx, PLATE, z0 + 2, "beam_x")
    m.box(x0 + 1, x1 - 1, PLATE, PLATE, z0 + 2, z0 + 2, "beam_x")
    m.set(cx, PLATE - 1, z0 + 2, "lantern_h")
    m.set(ix, 1, z1 - 1, "barrel")          # the corner by the hearth holds the stores


def build(place) -> Model:
    m = Model(dict(PALETTE))
    lo, hi = place.space
    X0, X1, Z0, Z1 = lo[0], hi[0], lo[2], hi[2]
    for x in range(X0, X1 + 1):
        for z in range(Z0, Z1 + 1):
            m.set(x, 0, z, "turf")
    cottage(m, A, "white", "door_a", "bed_a", "rug_a", A[0], True)
    cottage(m, B, "rubble", "door_b", "bed_b", "rug_b", B[1], False)
    # ---------- the front gardens: a path to each door, flower beds either side, a low hedge
    for box in (A, B):
        x0, x1, z0, z1 = box
        cx = (x0 + x1) // 2
        for x in range(x0, x1 + 1):
            for z in (3, 4):
                if x == cx:
                    m.set(x, 0, z, "path")
                else:
                    m.set(x, 0, z, "bed_soil")
                    m.set(x, 1, z, ["f1", "f2", "f3", "f4", "f5", "fern"][hsh(x, z, 7) % 6])
        for x in range(x0, x1 + 1):
            if x != cx:
                m.set(x, 1, 3, "hedge")
        m.set(x0, 1, 4, "rose")
        m.set(x0, 2, 4, "rose_top")
    m.box(X0, X1, 0, 0, 2, 2, "path")
    # ---------- the shared yard between the cottages: washing line, woodpile, water butt
    m.box(7, 8, 0, 0, 3, 9, "yard")
    m.box(7, 7, 1, 3, 5, 5, "line_post")
    m.box(7, 7, 1, 3, 9, 9, "line_post")
    m.box(7, 7, 3, 3, 6, 8, "line_post")
    m.set(7, 2, 6, "sheet_a")
    m.set(7, 2, 8, "sheet_b")
    m.set(8, 1, 9, "logs")
    m.set(8, 2, 9, "logs")
    m.set(8, 1, 5, "butt")
    m.set(8, 1, 8, "barrel")
    for x in range(X0, X1 + 1):
        for z in (Z1,):
            if m.get(x, 1, z) is None and m.get(x, 0, z) == "turf" and hsh(x, z, 9) % 3 == 0:
                m.set(x, 1, z, "tuft")

    finish(m)
    m.regions("cottage-a", *A)
    m.regions("cottage-b", *B)
    m.regions("gardens", 2, 13, 3, 4)
    m.regions("gardens", 7, 8, 5, 9)
    return m


class Cottages(Plot):
    MODEL = staticmethod(build)
    MARK_AT = {"node-cottages-2": (7, 4, "south")}   # at the yard's gate between the gardens
    REASON = "the cottages' wall heads and roofs: seen, never stood on"


if __name__ == "__main__":
    raise SystemExit(run(Cottages))
