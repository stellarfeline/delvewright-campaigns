#!/usr/bin/env python3
"""The fishmonger's: an open stall-front to the street with a slab counter,
the smokehouse behind it, and a yard of drying racks between.

Form, after medieval shopfronts and the fisherfolk's front-shop-and-smokehouse
(references in the node's `references[]`): the shop's street wall is a wide
unglazed opening over a counter, its shutter hooked up as an awning; the fish
lie on the counter and in tubs inside; a door at the side lets the fishmonger
through to the yard, and the smokehouse stands at the back, a small, tall,
blind brick house where the catch hangs over a smouldering fire.

    python3 fishmonger.py --allocation <allocation.json> --out <campaign>/programs/fishmonger.json

Piece-local: +x east (the street), +z south; y 0 the ground course, y 1 the walk plane.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from plotkit import Model, Plot, clip_to_space, door, door_roles, finish, frame_walls, fronted, gable, hsh, run  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))  # the town kit, one up
import townkit  # noqa: E402


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
    "pot_a": "minecraft:potted_blue_orchid", "pot_b": "minecraft:potted_fern",
    "barrel": "minecraft:barrel[facing=up,open=false]",
    "barrel_side": "minecraft:barrel[facing=north,open=false]",
    # ground
    "pave": [{"weight": 5, "block": "minecraft:cobblestone"}, {"weight": 3, "block": "minecraft:stone_bricks"},
             {"weight": 1, "block": "minecraft:mossy_cobblestone"}],
    "yard": [{"weight": 4, "block": "minecraft:gravel"}, {"weight": 3, "block": "minecraft:coarse_dirt"},
             {"weight": 2, "block": "minecraft:packed_mud"}],
    "shop_floor": [{"weight": 3, "block": "minecraft:polished_andesite"}, {"weight": 2, "block": "minecraft:stone_bricks"}],
    "ash_floor": [{"weight": 3, "block": "minecraft:coarse_dirt"}, {"weight": 1, "block": "minecraft:cobblestone"}],
    # the shop: stone ground course, a timber frame with blue-grey board infill
    "plinth": "minecraft:cobblestone",
    "post": "minecraft:stripped_spruce_log[axis=y]",
    "beam_x": "minecraft:spruce_log[axis=x]",
    "beam_z": "minecraft:spruce_log[axis=z]",
    "infill": "minecraft:light_gray_terracotta",
    "coping": "minecraft:stone_brick_wall[east=none,north=none,south=none,up=true,waterlogged=false,west=none]",
    "gable": "minecraft:spruce_planks",
    "pane": "minecraft:glass_pane[east=false,north=false,south=false,waterlogged=false,west=false]",
    "roof_n": st("deepslate_tile", "north"), "roof_s": st("deepslate_tile", "south"),
    "roof_e": st("deepslate_tile", "east"), "roof_w": st("deepslate_tile", "west"),
    "ridge": "minecraft:deepslate_tile_slab[type=bottom,waterlogged=false]",
    # the stall-front: a counter of boards under a slab, the shutter hooked up as an awning
    "counter": "minecraft:spruce_planks",
    "counter_top": "minecraft:smooth_stone_slab[type=bottom,waterlogged=false]",
    "awning": td("spruce", "east", "top", True),
    "ice": "minecraft:packed_ice",
    "tub": "minecraft:water_cauldron[level=3]",
    "block_table": "minecraft:stripped_spruce_wood[axis=y]",
    "lantern": "minecraft:lantern[hanging=false,waterlogged=false]",
    "lantern_h": "minecraft:lantern[hanging=true,waterlogged=false]",
    "chain": "minecraft:iron_chain[axis=y,waterlogged=false]",
    # the smokehouse: blind brick, a steep roof, fish hung over a smouldering fire
    "brick": "minecraft:bricks",
    "brick_dark": "minecraft:mud_bricks",
    "smoke_fire": "minecraft:campfire[facing=north,lit=true,signal_fire=false,waterlogged=false]",
    "smoked": "minecraft:dried_kelp_block",
    "rack": "minecraft:spruce_fence[east=false,north=false,south=false,waterlogged=false,west=false]",
    "rack_bar": "minecraft:spruce_slab[type=top,waterlogged=false]",
    "vent": "minecraft:spruce_trapdoor[facing=north,half=top,open=false,powered=false,waterlogged=false]",
    "logpile": "minecraft:oak_log[axis=z]",
    # life
    "bush": "minecraft:azalea_leaves[distance=1,persistent=true,waterlogged=false]",
    "f1": "minecraft:cornflower", "f2": "minecraft:oxeye_daisy", "f3": "minecraft:dandelion",
    "fern": "minecraft:fern", "tuft": "minecraft:short_grass", "bed_soil": "minecraft:rooted_dirt",
}
door_roles(PALETTE, "door_side", "minecraft:spruce_door", "north")
door_roles(PALETTE, "door_back", "minecraft:spruce_door", "east")
door_roles(PALETTE, "door_smoke", "minecraft:spruce_door", "west")

SHOP = (11, 17, 2, 8)      # walls included; the street wall at x 17 is the stall-front
SMOKE = (3, 7, 3, 7)       # the smokehouse, walls included
PLATE = 4
FRONT_DX = 3               # fronted, the shop's stall-front wall is the lot's street edge


def build(place) -> Model:
    m = Model(dict(PALETTE))
    lo, hi = place.space
    X0, X1, Z0, Z1 = lo[0], hi[0], lo[2], hi[2]
    for x in range(X0, X1 + 1):
        for z in range(Z0, Z1 + 1):
            m.set(x, 0, z, "turf")
    front, sf = fronted(place, "east")
    m.dx = FRONT_DX if front else 0
    sx0, sx1, sz0, sz1 = SHOP
    kx0, kx1, kz0, kz1 = SMOKE
    # paving before the stall on the street side; the yard behind
    m.box(sx1 + 1, X1, 0, 0, Z0 + 1, Z1 - 1, "pave")
    m.box(kx0, sx0 - 1, 0, 0, Z0 + 1, Z1 - 1, "yard")
    m.box(sx0, sx1, 0, 0, sz1 + 1, Z1 - 1, "yard")

    # ---------- the shop: plinth, frame, infill; the street wall open over the counter
    m.box(sx0, sx1, 0, 0, sz0, sz1, "shop_floor")
    frame_walls(m, sx0, sx1, sz0, sz1, 1, PLATE, "post", "infill", "beam_x", "beam_z", bay=3, plinth="plinth")
    # the stall-front: a five-wide opening, the counter in it, the shutter up as an awning
    m.box(sx1, sx1, 1, PLATE - 1, sz0 + 1, sz1 - 1, "~air")
    if not front:
        m.box(sx1, sx1, 1, 1, sz0 + 1, sz1 - 1, "counter")
        for z in range(sz0 + 1, sz1):
            m.set(sx1, 2, z, "counter_top")
            m.set(sx1 + 1, PLATE, z, "awning")
    else:
        # the street walks into the stall: the counter stands a cell in, a flap left in its middle
        for z in range(sz0 + 1, sz1):
            if z != (sz0 + sz1) // 2:
                m.set(sx1 - 1, 1, z, "counter")
                m.set(sx1 - 1, 2, z, "counter_top")
    # fish on ice inside the counter, tubs, the gutting block
    m.box(sx1 - 2, sx1 - 2, 1, 1, sz0 + 1, sz0 + 2, "ice")
    m.set(sx1 - 2, 1, sz1 - 1, "tub")
    m.set(13, 1, 3, "block_table")
    m.set(12, 1, 3, "barrel")
    m.set(12, 1, 4, "barrel")
    m.set(12, 2, 3, "barrel")
    m.set(12, 1, 7, "barrel_side")
    m.set(13, 2, 3, "lantern")
    m.set(14, PLATE - 1, 5, "lantern_h")
    m.box(sx0 + 1, sx1 - 1, PLATE, PLATE, 5, 5, "beam_x")
    # the side door to the yard, and the back door toward the smokehouse
    door(m, 14, 1, sz1, "door_side")
    door(m, sx0, 1, 5, "door_back")
    # windows onto the open north side
    m.box(13, 13, 2, 3, sz0, sz0, "pane")
    m.box(15, 15, 2, 3, sz0, sz0, "pane")
    gable(m, sx0, sx1, sz0, sz1, PLATE + 1, "x", "roof", "ridge", fill="gable")

    # ---------- the smokehouse: blind brick, a steep gable, a vent at the ridge
    m.box(kx0, kx1, 0, 0, kz0, kz1, "ash_floor")
    for x in range(kx0, kx1 + 1):
        for z in range(kz0, kz1 + 1):
            if x in (kx0, kx1) or z in (kz0, kz1):
                for y in range(1, 6):
                    m.set(x, y, z, "brick_dark" if (x + y + z) % 5 == 0 else "brick")
    door(m, kx1, 1, 5, "door_smoke")
    gable(m, kx0, kx1, kz0, kz1, 6, "z", "roof", "ridge", fill="brick")
    # inside: the fire in the corner, the catch hung from racks overhead
    m.set(kx0 + 1, 1, kz0 + 1, "smoke_fire")
    for x in (kx0 + 1, kx0 + 3):
        m.box(x, x, 1, 2, kz1 - 1, kz1 - 1, "rack")
    m.box(kx0 + 1, kx1 - 1, 4, 4, kz0 + 1, kz1 - 1, "rack_bar")
    for (x, z) in ((kx0 + 1, kz0 + 2), (kx0 + 2, kz0 + 1), (kx0 + 3, kz0 + 2), (kx0 + 2, kz0 + 3)):
        m.set(x, 3, z, "smoked")
    m.set(kx0 + 2, 1, kz1 - 1, "lantern")

    # ---------- the yard: drying racks along the south, a log pile, barrels by the back door
    for x in range(4, 10):
        m.set(x, 1, 9, "rack") if x % 2 == 0 else None
    m.box(4, 9, 3, 3, 9, 9, "rack_bar")
    for x in (5, 7, 9):
        m.set(x, 2, 9, "smoked")
    m.box(9, 9, 1, 1, 2, 3, "logpile")
    m.set(10, 1, 6, "barrel")
    m.set(10, 1, 7, "barrel")
    m.set(10, 2, 7, "barrel")
    # life: a bush and flowers by the shop's north wall, potted flowers by the stall
    for x in range(sx0, sx1):
        m.set(x, 0, 1, "bed_soil")
        m.set(x, 1, 1, ["f1", "f2", "f3", "fern"][hsh(x, 1, 3) % 4])
    m.set(18, 1, 1, "pot_a")
    m.set(18, 1, 9, "pot_b")
    m.set(2, 1, 2, "bush")
    for x in range(X0, X1 + 1):
        for z in (Z0, Z1):
            if m.get(x, 1, z) is None and m.get(x, 0, z) == "turf" and hsh(x, z, 9) % 3 == 0:
                m.set(x, 1, z, "tuft")

    m.regions("stall", sx0, sx1, sz0, sz1)
    m.regions("smokehouse", kx0, kx1, kz0, kz1)
    m.regions("yard", 8, 10, 2, 8)
    m.regions("yard", 3, 16, 9, 9)
    m.regions("yard", 3, 7, 2, 2)
    m.dx = 0
    if front:
        clip_to_space(m, place)
        edge, rows, door_h, air = sf
        townkit.street_front(m, edge, Z0, Z1, rows, air, {"wall": "infill", "lintel": "beam_z", "coping": "coping"},
                             door_h=door_h, inward=-1)
    finish(m)
    return m


class Fishmonger(Plot):
    MODEL = staticmethod(build)
    MARK_AT = {"node-fishmonger": (15, 5, "east")}   # behind the counter, facing the street

    def lay_parts(self, parts):
        if fronted(self, "east")[0]:
            self.MARK_AT = {k: (x + FRONT_DX, z, f) for k, (x, z, f) in type(self).MARK_AT.items()}
        super().lay_parts(parts)
    REASON = "the shop's and the smokehouse's wall heads and roofs: seen, never stood on"


if __name__ == "__main__":
    raise SystemExit(run(Fishmonger))
