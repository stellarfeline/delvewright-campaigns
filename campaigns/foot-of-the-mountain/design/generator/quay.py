#!/usr/bin/env python3
"""The quay: a long stone wharf at the foot of the street, its edge kerbed over the
open water, bollards along the edge for the boats' lines, lamps on posts along the
back, crates stacked and nets drying at the west end, barrels at the east by the
harbour.

Form, after the harbour references in the node's `references[]`: a paved waterfront
between the buildings and the edge, a stone quay edge, the cargo of the boats lying
about it.

    "$DELVEWRIGHT_PYTHON" quay.py --allocation <allocation.json> --out <campaign>/programs/quay.json --delvec <delvec>

Drawn into the skill's starter (`$DELVEWRIGHT_SKILL/scripts/starter.py`).
Piece-local: +x east, +z south (the water), y 0 the ground course, y 1 the walk plane.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
from starter import Model, fence, lantern, run, trapdoor, wall  # noqa: E402


PALETTE = {
    "pave": [{"weight": 6, "block": "minecraft:stone_bricks"}, {"weight": 3, "block": "minecraft:andesite"},
             {"weight": 2, "block": "minecraft:cobblestone"}, {"weight": 1, "block": "minecraft:mossy_cobblestone"}],
    "kerb": "minecraft:polished_andesite",
    "bollard": wall("polished_deepslate"),
    "lamp_post": fence("dark_oak"),
    "lantern": lantern(),
    "crate": "minecraft:spruce_wood[axis=y]",
    "crate_lid": trapdoor("spruce", "north", "top"),
    "rack": fence("spruce"),
    "net": "minecraft:brown_carpet",
    "rope": "minecraft:brown_wool",
    "anchor": "minecraft:anvil[facing=north]",
    "barrel": "minecraft:barrel[facing=up,open=false]",
}

LAMP_X = (6, 18, 44, 56)        # lamps along the back, clear of the flight's landing
BOLLARD_EVERY = 9               # a bollard every nine cells along the edge


def build(place):
    m = Model(place)
    m.palette.update(PALETTE)
    lo, hi = place.space
    X0, X1, Z0, Z1 = lo[0], hi[0], lo[2], hi[2]
    for x in range(X0, X1 + 1):
        for z in range(Z0, Z1 + 1):
            m.set(x, 0, z, "kerb" if z == Z1 else "pave")
    # bollards along the water's edge
    for x in range(X0 + 3, X1 - 1, BOLLARD_EVERY):
        m.set(x, 1, Z1, "bollard")
    # lamps on posts along the back of the quay
    for x in LAMP_X:
        m.set(x, 1, Z0, "lamp_post")
        m.set(x, 2, Z0, "lantern")
    # the west end: crates stacked, nets drying over a rack
    # (everything stands on the two edge rows, the back and the kerb: the quay is a way
    # eight clear across between them, DW1057)
    for (x, z, h) in ((X0 + 2, Z0, 2), (X0 + 3, Z0, 1), (X0 + 2, Z0 + 1, 1)):
        for y in range(1, h + 1):
            m.set(x, y, z, "crate")
        m.set(x, h + 1, z, "crate_lid")
    for x in range(X0 + 8, X0 + 13):
        m.set(x, 1, Z0, "rack")
        if (x - X0) % 2 == 0:
            m.set(x, 2, Z0, "net")
    # by the edge: an anchor and a coil of rope laid on the stones
    m.set(X0 + 42, 1, Z1, "anchor")
    m.set(X0 + 43, 1, Z1, "rope")
    # the east end, by the harbour: barrels of salt fish
    for (x, z) in ((X1 - 8, Z0), (X1 - 7, Z0), (X1 - 8, Z0 + 1)):
        m.set(x, 1, z, "barrel")
    m.finish()
    m.mark("node-quay", (X0 + X1) // 2, (Z0 + Z1) // 2, "south")
    return m


if __name__ == "__main__":
    raise SystemExit(run(build, reason="the crate tops and the racks' heads: seen, never stood on"))
