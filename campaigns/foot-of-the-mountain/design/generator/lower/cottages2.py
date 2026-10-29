#!/usr/bin/env python3
"""A pair of fishermen's cottages: two small houses side by side, front
gardens to the lane, a shared yard between them; each one room below and a
sleeping loft above, up a ladder.

Form, after fisherfolk cottages and community cottage builds (references in
the node's `references[]`): one room down and one up, the hearth on the
gable wall, the door in the front between small windows, the bed in the
loft under the roof; the two told apart by their walls (one whitewashed in
a timber frame, one of rubble stone) under one roof line. Front gardens of
flowers behind a low hedge; between the houses, the washing, the woodpile,
the water butt.

    "$DELVEWRIGHT_PYTHON" cottages2.py --allocation <allocation.json> --out <campaign>/programs/cottages-2.json --delvec <delvec>

Drawn into the skill's starter (`$DELVEWRIGHT_SKILL/scripts/starter.py`).

Piece-local: +x east, +z south, the lane on the north; y 0 the ground course, y 1 the walk plane.
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


def door(m, x, y, z, block, facing, hinge="left"):
    for dy, half in ((0, "lower"), (1, "upper")):
        m.set(x, y + dy, z, f"{block}[facing={facing},half={half},hinge={hinge},open=false,powered=false]")


def gable_x(m, x0, x1, z0, z1, y0, stair, ridge, fill=None, ov=1):
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


def close_edge_gaps(m, X0, X1, Z0, Z1, role):
    """On a column at the plot's edge, the ground the whole stitches to is its top:
    close any air between a wall and the eave above it, so no edge stands over air."""
    for x in range(X0, X1 + 1):
        for z in range(Z0, Z1 + 1):
            if x not in (X0, X1) and z not in (Z0, Z1):
                continue
            ys = sorted(y for (cx, y, cz) in m.v if cx == x and cz == z and y > 0 and m.v[(cx, y, cz)] != "~air")
            if len(ys) < 2:
                continue
            for y in range(ys[0], ys[-1]):
                if (x, y, z) not in m.v or m.v[(x, y, z)] == "~air":
                    m.set(x, y, z, role(x, z) if callable(role) else role)


PALETTE = {
    "turf": "minecraft:grass_block[snowy=false]",
    "path": [{"weight": 3, "block": "minecraft:cobblestone"}, {"weight": 2, "block": "minecraft:gravel"},
             {"weight": 1, "block": "minecraft:mossy_cobblestone"}],
    "yard": [{"weight": 3, "block": "minecraft:coarse_dirt"}, {"weight": 2, "block": "minecraft:gravel"}],
    "boards": "minecraft:spruce_planks",
    "loft": "minecraft:spruce_planks",
    "bed_soil": "minecraft:rooted_dirt",
    "post": "minecraft:stripped_spruce_log[axis=y]",
    "beam_x": "minecraft:spruce_log[axis=x]",
    "beam_z": "minecraft:spruce_log[axis=z]",
    "white": "minecraft:white_terracotta",
    "rubble": [{"weight": 5, "block": "minecraft:cobblestone"}, {"weight": 3, "block": "minecraft:stone_bricks"},
               {"weight": 2, "block": "minecraft:andesite"}, {"weight": 1, "block": "minecraft:mossy_cobblestone"}],
    "quoin": "minecraft:tuff_bricks",
    "plinth": "minecraft:cobblestone",
    "pane": "minecraft:glass_pane[east=false,north=false,south=false,waterlogged=false,west=false]",
    "roof_n": st("deepslate_tile", "north"), "roof_s": st("deepslate_tile", "south"),
    "ridge": "minecraft:deepslate_tile_slab[type=bottom,waterlogged=false]",
    "chimney": "minecraft:bricks",
    "hearth": "minecraft:bricks",
    "fire": "minecraft:campfire[facing=south,lit=true,signal_fire=false,waterlogged=false]",
    "ladder": "minecraft:ladder[facing=south,waterlogged=false]",
    "table": "minecraft:spruce_planks",
    "chair_e": st("spruce", "east"), "chair_w": st("spruce", "west"),
    "shelf": "minecraft:bookshelf",
    "lantern": "minecraft:lantern[hanging=false,waterlogged=false]",
    "lantern_h": "minecraft:lantern[hanging=true,waterlogged=false]",
    "barrel": "minecraft:barrel[facing=up,open=false]",
    "rug_a": "minecraft:light_blue_carpet",
    "rug_b": "minecraft:orange_carpet",
    "nets": "minecraft:cobweb",
    "hedge": "minecraft:oak_leaves[distance=1,persistent=true,waterlogged=false]",
    "line_post": "minecraft:spruce_fence[east=false,north=false,south=false,waterlogged=false,west=false]",
    "sheet_a": "minecraft:white_wool",
    "sheet_b": "minecraft:light_blue_wool",
    "logs": "minecraft:oak_log[axis=z]",
    "butt": "minecraft:water_cauldron[level=3]",
    "pot_a": "minecraft:potted_red_tulip", "pot_b": "minecraft:potted_azure_bluet",
    "f1": "minecraft:poppy", "f2": "minecraft:oxeye_daisy", "f3": "minecraft:cornflower",
    "f4": "minecraft:allium", "f5": "minecraft:pink_tulip", "fern": "minecraft:fern",
    "tuft": "minecraft:short_grass",
    "rose": "minecraft:rose_bush[half=lower]", "rose_top": "minecraft:rose_bush[half=upper]",
}

A = (1, 6, 5, 10)    # walls included: 6 x 6, a 4 x 4 room inside
B = (9, 14, 5, 10)
TOP = 6              # wall plate: a loft under the roof
LOFT = 4             # the loft floor's course


def cottage(m, box, frame, hearth_east, bed, rug, door_block):
    x0, x1, z0, z1 = box
    wall = "white" if frame else "rubble"
    m.box(x0, x1, 0, 0, z0, z1, "boards")
    for y in range(1, TOP + 1):
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                if not (x in (x0, x1) or z in (z0, z1)):
                    continue
                corner = x in (x0, x1) and z in (z0, z1)
                if not frame:
                    role = "quoin" if corner and y % 2 else wall
                elif y == 1:
                    role = "plinth"
                elif corner or (z in (z0, z1) and (x - x0) % 2 == 0):
                    role = "post"
                elif y == LOFT:
                    role = "beam_x" if z in (z0, z1) else "beam_z"
                else:
                    role = wall
                m.set(x, y, z, role)
    cx = (x0 + x1) // 2                             # the door's column
    hx = x1 - 1 if hearth_east else x0 + 1          # the hearth's column inside
    lx = x0 + 1 if hearth_east else x1 - 1          # the ladder's column
    ox = cx + 1                                     # the column beside the door
    gx = x1 if hearth_east else x0                  # the hearth's gable wall
    hz = z0 + 3                                     # the hearth's row
    door(m, cx, 1, z0, door_block, "south")
    m.box(hx, hx, 2, 3, z0, z0, "pane")
    m.box(ox, ox, 2, 3, z0, z0, "pane")
    m.box(cx, ox, 2, 3, z1, z1, "pane")
    m.box(gx, gx, LOFT + 1, LOFT + 2, z1 - 1, z1 - 1, "pane")
    gable_x(m, x0, x1, z0, z1, TOP + 1, "roof", "ridge", fill=wall)
    # the hearth on the gable wall under the loft, the chimney through the roof
    m.box(gx, gx, 1, TOP + 6, hz, hz, "chimney")
    m.set(hx, 1, hz, "hearth")
    m.set(hx, 2, hz, "fire")
    # the loft over the back two-thirds of the room, a ladder up to it inside the door
    m.box(x0 + 1, x1 - 1, LOFT, LOFT, z0 + 2, z1 - 1, "loft")
    m.box(lx, lx, 1, LOFT, z0 + 1, z0 + 1, "ladder")
    # the room: a table with two chairs under the back window, a rug, a shelf, the stores
    m.set(ox, 1, z1 - 1, "table")
    m.set(ox, 2, z1 - 1, "lantern")
    m.set(cx, 1, z1 - 1, "chair_e" if ox > cx else "chair_w")
    m.set(lx, 1, z1 - 1, "chair_w" if lx > ox else "chair_e")
    m.box(cx, ox, 1, 1, z0 + 2, z0 + 2, rug)
    m.set(hx, 1, z1 - 1, "barrel")
    m.set(hx, 1, z0 + 1, "shelf")
    m.set(cx, LOFT - 1, z0 + 2, "lantern_h")    # hung under the loft's edge
    # the loft: the bed under the roof, nets stored by the gable, a sea chest
    colour = "blue" if frame else "yellow"
    m.palette[bed + "_head"] = f"minecraft:{colour}_bed[facing=south,occupied=false,part=head]"
    m.palette[bed + "_foot"] = f"minecraft:{colour}_bed[facing=south,occupied=false,part=foot]"
    m.set(ox, LOFT + 1, z1 - 1, bed + "_head")
    m.set(ox, LOFT + 1, z1 - 2, bed + "_foot")
    m.set(hx, LOFT + 1, z1 - 1, "nets")
    m.set(hx, LOFT + 1, z1 - 2, "lantern")
    m.set(cx, LOFT + 1, z1 - 1, "barrel")


def build(place):
    m = Model(place)
    m.palette.update(PALETTE)
    lo, hi = place.space
    X0, X1, Z0, Z1 = lo[0], hi[0], lo[2], hi[2]
    for x in range(X0, X1 + 1):
        for z in range(Z0, Z1 + 1):
            m.set(x, 0, z, "turf")
    m.box(X0, X1, 0, 0, Z0, Z0 + 1, "path")
    cottage(m, A, True, False, "bed_a", "rug_a", "minecraft:spruce_door")
    cottage(m, B, False, True, "bed_b", "rug_b", "minecraft:oak_door")
    # ---------- the front gardens: a path to each door, flower beds, a low hedge
    for box in (A, B):
        x0, x1, z0, z1 = box
        cx = (x0 + x1) // 2
        for x in range(x0, x1 + 1):
            for z in (3, 4):
                if x == cx:
                    m.set(x, 0, z, "path")
                    continue
                m.set(x, 0, z, "bed_soil")
                m.set(x, 1, z, ["f1", "f2", "f3", "f4", "f5", "fern"][hsh(x, z, 7) % 6])
            if x != cx:
                m.set(x, 1, 3, "hedge")
        m.set(x0, 1, 4, "rose")
        m.set(x0, 2, 4, "rose_top")
        m.set(cx + 1, 1, 4, "pot_a" if x0 == A[0] else "pot_b")
    # ---------- the shared yard between the cottages
    m.box(7, 8, 0, 0, 3, 10, "yard")
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
        if m.get(x, 1, Z1) is None and hsh(x, Z1, 9) % 3 == 0:
            m.set(x, 1, Z1, "tuft")

    # the eaves stop at the plot's edge: nothing is drawn beyond the play space above the ground
    for c in [c for c in list(m.v) if c[1] > 0 and not (X0 <= c[0] <= X1 and Z0 <= c[2] <= Z1)]:
        del m.v[c]
    close_edge_gaps(m, X0, X1, Z0, Z1, lambda x, z: "white" if x <= A[1] else "rubble")
    m.finish()
    m.part(*A, "cottage-a")
    m.part(*B, "cottage-b")
    m.part(X0, X1, 3, 4, "gardens")
    m.part(7, 8, 5, Z1, "gardens")
    m.mark("node-cottages-2", 7, 4, "south")
    return m


if __name__ == "__main__":
    raise SystemExit(run(build, reason="the cottages' wall heads and roofs: seen, never stood on"))
