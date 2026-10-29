#!/usr/bin/env python3
"""The boatwright's: a tall open boat shed gable-end to the lane, a hull on
the stocks inside it, and a yard of seasoning timber with a winch.

Form, after boatbuilders' sheds and slips (references in the node's
`references[]`): a plain rectangular timber shed on posts, its end to the
water-side lane wide open so a hull goes in and out; the keel lies on
blocks down the middle, ribs rising from it, half planked; the bench and the
steaming fire along one wall. Beside the shed, the timber stacks to season
under the sky, and the winch that hauls a hull up the slip.

    python3 boatwright.py --allocation <allocation.json> --out <campaign>/programs/boatwright.json

Piece-local: +x east, +z south, the lane on the south; y 0 the ground course, y 1 the walk plane.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from plotkit import Model, Plot, finish, gable, hsh, run  # noqa: E402


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
    "pot_a": "minecraft:potted_cornflower",
    "barrel": "minecraft:barrel[facing=up,open=false]",
    # ground: a timber slip down the middle of the shed to the lane, shingle round it
    "slip": [{"weight": 3, "block": "minecraft:spruce_planks"}, {"weight": 1, "block": "minecraft:stripped_spruce_wood[axis=z]"}],
    "yard": [{"weight": 4, "block": "minecraft:gravel"}, {"weight": 2, "block": "minecraft:coarse_dirt"},
             {"weight": 2, "block": "minecraft:cobblestone"}],
    "shed_floor": [{"weight": 3, "block": "minecraft:coarse_dirt"}, {"weight": 2, "block": "minecraft:gravel"},
                   {"weight": 1, "block": "minecraft:spruce_planks"}],
    "plinth": "minecraft:cobblestone",
    # the shed: spruce posts, dark boards, a deepslate roof
    "post": "minecraft:spruce_log[axis=y]",
    "beam_x": "minecraft:spruce_log[axis=x]",
    "beam_z": "minecraft:spruce_log[axis=z]",
    "boards": "minecraft:dark_oak_planks",
    "board_light": "minecraft:spruce_planks",
    "brace_e": st("spruce", "east", "top"),
    "brace_w": st("spruce", "west", "top"),
    "roof_e": st("deepslate_tile", "east"), "roof_w": st("deepslate_tile", "west"),
    "ridge": "minecraft:deepslate_tile_slab[type=bottom,waterlogged=false]",
    "pane": "minecraft:glass_pane[east=false,north=false,south=false,waterlogged=false,west=false]",
    # the hull on the stocks
    "stock": "minecraft:stripped_spruce_wood[axis=y]",
    "keel": "minecraft:stripped_oak_log[axis=z]",
    "rib": "minecraft:oak_fence[east=false,north=false,south=false,waterlogged=false,west=false]",
    "plank_w": st("oak", "west", "top"),
    "plank_e": st("oak", "east", "top"),
    "plank_low": "minecraft:oak_slab[type=top,waterlogged=false]",
    "stem": "minecraft:stripped_oak_log[axis=y]",
    # the work along the wall
    "bench": "minecraft:crafting_table",
    "steam": "minecraft:campfire[facing=east,lit=true,signal_fire=false,waterlogged=false]",
    "steam_box": "minecraft:spruce_trapdoor[facing=east,half=top,open=false,powered=false,waterlogged=false]",
    "tar": "minecraft:cauldron",
    "chain": "minecraft:iron_chain[axis=y,waterlogged=false]",
    "lantern": "minecraft:lantern[hanging=false,waterlogged=false]",
    "lantern_h": "minecraft:lantern[hanging=true,waterlogged=false]",
    # the yard: timber stacks, a sawhorse, the winch
    "timber_z": "minecraft:stripped_spruce_log[axis=z]",
    "timber_x": "minecraft:spruce_log[axis=x]",
    "plank_stack": "minecraft:spruce_slab[type=bottom,waterlogged=false]",
    "sawhorse": "minecraft:spruce_fence[east=false,north=false,south=false,waterlogged=false,west=false]",
    "sawtop": "minecraft:spruce_slab[type=top,waterlogged=false]",
    "winch": "minecraft:stripped_oak_log[axis=y]",
    "winch_bar": td("oak", "north", "top", False),
    # life
    "bush": "minecraft:azalea_leaves[distance=1,persistent=true,waterlogged=false]",
    "tuft": "minecraft:short_grass", "fern": "minecraft:fern",
}

SHED = (2, 8, 2, 8)       # walls included; the open end at z 8 faces the lane
PLATE = 5


def build(place) -> Model:
    m = Model(dict(PALETTE))
    lo, hi = place.space
    X0, X1, Z0, Z1 = lo[0], hi[0], lo[2], hi[2]
    for x in range(X0, X1 + 1):
        for z in range(Z0, Z1 + 1):
            m.set(x, 0, z, "turf")
    sx0, sx1, sz0, sz1 = SHED
    m.box(X0, X1, 0, 0, sz1 + 1, Z1, "yard")
    m.box(sx1 + 1, X1 - 1, 0, 0, Z0, Z1, "yard")
    m.box(sx0, sx1, 0, 0, sz0, sz1, "shed_floor")
    m.box(4, 6, 0, 0, sz0 + 1, Z1, "slip")

    # ---------- the shed: posts every three, boards between, the lane end open
    for x in range(sx0, sx1 + 1):
        for z in range(sz0, sz1 + 1):
            if x not in (sx0, sx1) and z != sz0:
                continue
            postcol = (x in (sx0, sx1) and (z - sz0) % 3 == 0) or (z == sz0 and x in (sx0, 5, sx1)) or (z == sz1)
            for y in range(1, PLATE + 1):
                if z == sz1 and x not in (sx0, sx1):
                    continue                    # the open end
                if y == 1 and not postcol:
                    role = "plinth"
                elif postcol:
                    role = "post"
                elif y == PLATE:
                    role = "beam_z" if x in (sx0, sx1) else "beam_x"
                else:
                    role = "boards" if (x + z) % 4 else "board_light"
                m.set(x, y, z, role)
    # the beam over the open end, braced from the corner posts
    m.box(sx0, sx1, PLATE, PLATE, sz1, sz1, "beam_x")
    m.set(sx0 + 1, PLATE - 1, sz1, "brace_w")
    m.set(sx1 - 1, PLATE - 1, sz1, "brace_e")
    # windows high in the side walls
    for z in (4, 6):
        m.set(sx0, 3, z, "pane")
        m.set(sx1, 3, z, "pane")
    # the roof: ridge along z, the gable to the lane boarded over the beam
    gable(m, sx0, sx1, sz0, sz1 - 1, PLATE + 1, "z", "roof", "ridge", fill="board_light")
    for x in range(sx0 + 1, sx1):
        for y in range(PLATE + 1, PLATE + 6):
            if m.get(x, y, sz1 - 1) == "board_light":
                m.set(x, y, sz1, "board_light")
    # tie beams, a lantern hung from each
    for z in (4, 6):
        m.box(sx0 + 1, sx1 - 1, PLATE, PLATE, z, z, "beam_x")
        m.set(3, PLATE - 1, z, "lantern_h")
    # ---------- the hull on the stocks: keel on blocks, ribs, half planked, a stem post
    for z in (3, 5, 7):
        m.set(5, 1, z, "stock")
    m.box(5, 5, 2, 2, 3, 7, "keel")
    m.box(5, 5, 2, 4, 7, 7, "stem")
    for z in (3, 4, 5, 6):
        m.set(4, 3, z, "plank_w")          # planked on the west side
        m.set(4, 2, z, "plank_low") if z in (4, 5) else None
        m.set(6, 3, z, "rib") if z % 2 == 0 else None
        m.set(6, 4, z, "rib") if z % 2 == 0 else None
    # the bench, the steaming fire under its box, the tar pot, along the east wall
    m.set(7, 1, 3, "bench")
    m.set(7, 1, 5, "steam")
    m.set(7, 2, 5, "~air")
    m.set(7, 3, 5, "steam_box")
    m.set(3, 1, 3, "tar")
    m.set(3, 1, 4, "barrel")
    m.set(7, 1, 7, "lantern")
    m.set(6, PLATE - 1, 6, "chain")

    # ---------- the yard: timber stacked to season, a sawhorse, the winch at the slip head
    m.box(11, 12, 1, 1, 2, 6, "timber_z")
    m.box(11, 12, 2, 2, 2, 5, "timber_z")
    m.box(11, 11, 3, 3, 3, 4, "timber_z")
    m.box(13, 13, 1, 1, 2, 3, "plank_stack")
    m.set(10, 1, 8, "sawhorse")
    m.set(12, 1, 8, "sawhorse")
    m.box(10, 12, 2, 2, 8, 8, "sawtop")
    m.set(9, 1, 2, "winch")
    m.set(9, 2, 2, "winch_bar")
    m.set(13, 1, 6, "barrel")
    m.set(13, 1, 7, "barrel")
    m.set(13, 2, 7, "barrel")
    m.set(9, 1, 7, "pot_a")
    m.set(10, 1, 5, "bush")
    for x in range(X0, X1 + 1):
        for z in (Z0, Z1 - 1):
            if m.get(x, 1, z) is None and m.get(x, 0, z) == "turf" and hsh(x, z, 9) % 3 == 0:
                m.set(x, 1, z, "tuft")

    finish(m)
    m.regions("shed", sx0, sx1, sz0, sz1)
    m.regions("yard", 9, 13, 1, 8)
    return m


class Boatwright(Plot):
    MODEL = staticmethod(build)
    MARK_AT = {"node-boatwright": (3, 7, "east")}   # at the shed's mouth, facing the hull
    REASON = "the shed's wall heads, roof and the hull's gunwale: seen, never stood on"


if __name__ == "__main__":
    raise SystemExit(run(Boatwright))
