#!/usr/bin/env python3
"""The net loft: a tall, narrow, tarred-timber net store over a boat store,
gable-end to the yard, and the yard of net poles beside it.

Form, after the fishermen's net shops of the Channel coast and the net
sheds of the Baltic (references in the node's `references[]`): a tall shed
of dark weatherboarding on a stone plinth, gable-end on, a wide boat door in
the gable at the ground and a loft above it reached by a stair along the
inside wall; nets are stored in the loft, never dried there — they dry on
rows of poles in the open yard beside the shed. The ground floor holds a
hull on trestles, oars and floats; the loft holds the nets on their racks.

    python3 netloft.py --allocation <allocation.json> --out <campaign>/programs/netloft.json

Piece-local: +x east (the street), +z south; y 0 the ground course, y 1 the walk plane.
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
    "pot_a": "minecraft:potted_red_tulip", "pot_b": "minecraft:potted_cornflower",
    "pot_c": "minecraft:potted_azure_bluet", "pot_d": "minecraft:potted_fern",
    # ground: shingle and sand toward the harbour
    "shingle": [{"weight": 5, "block": "minecraft:gravel"}, {"weight": 2, "block": "minecraft:coarse_dirt"},
                {"weight": 2, "block": "minecraft:cobblestone"}],
    "slip": [{"weight": 3, "block": "minecraft:spruce_planks"}, {"weight": 1, "block": "minecraft:stripped_spruce_wood[axis=x]"}],
    "store_floor": [{"weight": 4, "block": "minecraft:cobblestone"}, {"weight": 2, "block": "minecraft:gravel"}],
    "plinth": [{"weight": 4, "block": "minecraft:cobblestone"}, {"weight": 2, "block": "minecraft:stone_bricks"},
               {"weight": 1, "block": "minecraft:mossy_cobblestone"}],
    # the tarred weatherboarding: dark oak boards between black posts
    "boards": "minecraft:dark_oak_planks",
    "post": "minecraft:dark_oak_log[axis=y]",
    "beam_x": "minecraft:dark_oak_log[axis=x]",
    "beam_z": "minecraft:dark_oak_log[axis=z]",
    "loft_floor": "minecraft:spruce_planks",
    "pane": "minecraft:glass_pane[east=false,north=false,south=false,waterlogged=false,west=false]",
    "frame_w": td("birch", "west", open_=True),
    "rail": "minecraft:spruce_fence[east=false,north=false,south=false,waterlogged=false,west=false]",
    "stair_w": st("spruce", "west"),
    # the roof: deepslate tiles, as the town's
    "roof_n": st("deepslate_tile", "north"), "roof_s": st("deepslate_tile", "south"),
    "ridge": "minecraft:deepslate_tile_slab[type=bottom,waterlogged=false]",
    "hoist": "minecraft:dark_oak_fence[east=false,north=false,south=false,waterlogged=false,west=false]",
    "rope": "minecraft:iron_chain[axis=y,waterlogged=false]",
    # the boat store
    "trestle": "minecraft:spruce_fence[east=false,north=false,south=false,waterlogged=false,west=false]",
    "hull_low": "minecraft:spruce_slab[type=top,waterlogged=false]",
    "hull_n": st("spruce", "north", "top"), "hull_s": st("spruce", "south", "top"),
    "keel": "minecraft:stripped_spruce_log[axis=x]",
    "oar": "minecraft:stripped_spruce_log[axis=y]",
    "float": "minecraft:white_wool",
    "float_r": "minecraft:red_wool",
    "lantern": "minecraft:lantern[hanging=false,waterlogged=false]",
    "lantern_h": "minecraft:lantern[hanging=true,waterlogged=false]",
    # the loft's nets on their racks
    "net": "minecraft:cobweb",
    "net_roll": "minecraft:brown_wool",
    "net_pile": "minecraft:brown_carpet",
    "rack": "minecraft:spruce_trapdoor[facing=north,half=top,open=false,powered=false,waterlogged=false]",
    # the yard: net poles, a capstan, crab pots, flowers
    "pole": "minecraft:spruce_fence[east=false,north=false,south=false,waterlogged=false,west=false]",
    "capstan": "minecraft:stripped_spruce_log[axis=y]",
    "capstan_bar": "minecraft:spruce_trapdoor[facing=north,half=top,open=false,powered=false,waterlogged=false]",
    "pot": "minecraft:spruce_trapdoor[facing=north,half=bottom,open=false,powered=false,waterlogged=false]",
    "pot_body": "minecraft:composter[level=0]",
    "bench": st("spruce", "west"),
    "bush": "minecraft:azalea_leaves[distance=1,persistent=true,waterlogged=false]",
    "tuft": "minecraft:short_grass", "fern": "minecraft:fern",
    "f1": "minecraft:cornflower", "f2": "minecraft:oxeye_daisy", "f3": "minecraft:dandelion",
    "beach_grass": "minecraft:fern",
}

# ---- the plan ----
SHED = (2, 10, 3, 8)      # x0, x1, z0, z1, walls included: gable-end to the east
GROUND_TOP = 4            # the boat store's courses y1..4
LOFT = 5                  # the loft floor's course
PLATE = 8                 # the wall plate
YARD = (12, 18, 2, 9)


def build(place) -> Model:
    m = Model(dict(PALETTE))
    lo, hi = place.space
    X0, X1, Z0, Z1 = lo[0], hi[0], lo[2], hi[2]
    for x in range(X0, X1 + 1):
        for z in range(Z0, Z1 + 1):
            m.set(x, 0, z, "turf")
    sx0, sx1, sz0, sz1 = SHED
    # the yard: shingle; a timber slip from the boat door toward the street
    m.box(sx1 + 1, X1, 0, 0, Z0 + 1, Z1 - 1, "shingle")
    m.box(sx1 + 1, X1, 0, 0, 5, 6, "slip")
    # ---------- the shed: plinth, posts at the corners and the storey line, boards
    m.box(sx0, sx1, 0, 0, sz0, sz1, "store_floor")
    for x in range(sx0, sx1 + 1):
        for z in range(sz0, sz1 + 1):
            if x not in (sx0, sx1) and z not in (sz0, sz1):
                continue
            corner = x in (sx0, sx1) and z in (sz0, sz1)
            for y in range(1, PLATE + 1):
                if y == 1:
                    role = "plinth"
                elif corner:
                    role = "post"
                elif y == LOFT:
                    role = "beam_x" if z in (sz0, sz1) else "beam_z"
                else:
                    role = "boards"
                m.set(x, y, z, role)
    # the loft floor, with the stairwell open along the north wall
    m.box(sx0 + 1, sx1 - 1, LOFT, LOFT, sz0 + 1, sz1 - 1, "loft_floor")
    m.box(sx0 + 2, sx0 + 6, LOFT, LOFT, sz0 + 1, sz0 + 1, "~air")
    # the stair: up the north wall from the boat door westward, landing on the loft
    for i in range(5):
        m.set(sx0 + 6 - i, 1 + i, sz0 + 1, "stair_w")
    # a rail along the stairwell's loft edge
    for x in range(sx0 + 2, sx0 + 7):
        m.set(x, LOFT + 1, sz0 + 2, "rail")
    # the roof: ridge along x, gable to the east and west, boarded
    gable(m, sx0, sx1, sz0, sz1, PLATE + 1, "x", "roof", "ridge", fill="boards")
    # the boat door in the east gable: two wide, three high, under a beam
    m.box(sx1, sx1, 1, 3, 5, 6, "~air")
    m.box(sx1, sx1, 4, 4, 4, 7, "beam_z")
    m.box(sx1, sx1, 0, 0, 5, 6, "slip")
    # the loft's gable window and the hoist beam over the boat door
    m.box(sx1, sx1, 7, 8, 5, 6, "pane")
    m.set(sx1 + 1, 10, 5, "hoist")
    m.set(sx1, 10, 5, "beam_x")
    m.set(sx1 + 1, 9, 5, "rope")
    m.set(sx1 + 1, 8, 5, "rope")
    # small windows along the south side, both storeys, birch-framed
    for x in (4, 7):
        m.box(x, x, 2, 3, sz1, sz1, "pane")
        m.box(x, x, 6, 7, sz1, sz1, "pane")
    m.box(sx0, sx0, 6, 7, 5, 6, "pane")
    # ---------- the boat store: a hull on trestles, oars, floats
    for x in (4, 7):
        m.set(x, 1, 6, "trestle")
    m.box(3, 8, 2, 2, 6, 6, "keel")
    m.box(4, 7, 2, 2, 5, 5, "hull_n")
    m.box(4, 7, 2, 2, 7, 7, "hull_s")
    m.set(sx0 + 1, 1, sz1 - 1, "oar")
    m.set(sx0 + 1, 2, sz1 - 1, "oar")
    m.set(sx0 + 1, 1, sz1 - 2, "float")
    m.set(sx0 + 1, 1, 5, "float_r")
    m.set(9, 1, 7, "lantern")
    # ---------- the loft: nets on racks, rolls of net, hanging from the beams
    m.set(3, LOFT + 1, 7, "net_roll")
    m.set(3, LOFT + 2, 7, "net_roll")
    m.set(3, LOFT + 1, 6, "net_roll")
    m.box(4, 8, LOFT + 1, LOFT + 1, 7, 7, "net_pile")
    for x in (4, 6, 8):
        m.set(x, PLATE, 6, "net")
        m.set(x, PLATE, 7, "net")
    m.set(9, LOFT + 1, 7, "lantern")
    m.set(3, LOFT + 1, 5, "lantern")
    # ---------- the yard: rows of net poles with nets slung between them
    yx0, yx1, yz0, yz1 = YARD
    for z in (3, 8):
        for x in range(yx0 + 1, yx1, 2):
            m.box(x, x, 1, 3, z, z, "pole")
            m.set(x, 4, z, "pole")
        for x in range(yx0 + 1, yx1 - 1):
            if m.get(x, 1, z) is None:
                m.set(x, 3, z, "net")
                m.set(x, 4, z, "pole")
    # a capstan by the slip, crab pots stacked, a bench by the shed
    m.set(12, 1, 4, "capstan")
    m.set(12, 2, 4, "capstan_bar")
    for (x, z) in ((17, 5), (17, 6), (18, 6)):
        m.set(x, 1, z, "pot_body")
    m.set(17, 2, 6, "pot_body")
    # life: beach grass, a bush at the shed's corners, a flower bed under the south windows
    for x in range(X0, X1 + 1):
        for z in range(Z0, Z1 + 1):
            if m.get(x, 1, z) is None and m.get(x, 0, z) in ("turf",) and hsh(x, z, 13) % 3 == 0:
                m.set(x, 1, z, "beach_grass" if hsh(x, z, 1) % 2 else "tuft")
    for x in range(3, 10):
        m.set(x, 0, 9, "turf")
        m.set(x, 1, 9, ["f1", "f2", "f3", "fern"][hsh(x, 9, 4) % 4])
    m.set(sx1 + 1, 1, sz0, "bush")
    m.set(sx1 + 1, 1, sz1, "bush")

    # potted flowers by the boat door and the bench
    m.set(11, 1, 4, "pot_a")
    m.set(11, 1, 7, "pot_d")
    finish(m)
    m.regions("loft", sx0, sx1, sz0, sz1)
    m.regions("yard", yx0, yx1, yz0, yz1)
    return m


class NetLoft(Plot):
    MODEL = staticmethod(build)
    MARK_AT = {"node-netloft": (8, 5, "west")}   # inside the boat door, facing the hull
    REASON = "the loft's wall heads, the roof and the net poles' tops: seen, never stood on"


if __name__ == "__main__":
    raise SystemExit(run(NetLoft))
