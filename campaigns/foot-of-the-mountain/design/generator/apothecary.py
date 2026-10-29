#!/usr/bin/env python3
"""The apothecary: a test plot started from the skill's starter alone, with one
small building in it — a narrow stone-and-timber house, its door to the
street, and the physic garden's ground behind it.

    "$DELVEWRIGHT_PYTHON" apothecary.py --allocation <allocation.json> --out <campaign>/programs/apothecary.json

Piece-local: +x east, +z south; y 0 the ground course, y 1 the walk plane.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
from starter import Model, run  # noqa: E402


def build(place) -> Model:
    m = Model(place)
    m.palette.update({
        "floor": "minecraft:grass_block[snowy=false]",
        "plinth": "minecraft:cobblestone",
        "boards": "minecraft:spruce_planks",
        "post": "minecraft:spruce_log[axis=y]",
        "pane": "minecraft:glass_pane[east=false,north=false,south=false,waterlogged=false,west=false]",
        "door_lo": "minecraft:spruce_door[facing=west,half=lower,hinge=left,open=false,powered=false]",
        "door_hi": "minecraft:spruce_door[facing=west,half=upper,hinge=left,open=false,powered=false]",
        "lantern": "minecraft:lantern[hanging=true,waterlogged=false]",
    })
    # the house: x 4..9, z 2..10 — walls a plinth course, then boards between
    # corner posts, a flat boarded roof at y 5
    x0, x1, z0, z1 = 4, 9, 2, 10
    m.hollow(x0, x1, 1, 1, z0, z1, "plinth")
    m.hollow(x0, x1, 2, 4, z0, z1, "boards")
    for x in (x0, x1):
        for z in (z0, z1):
            m.box(x, x, 2, 4, z, z, "post")
    m.box(x0, x1, 5, 5, z0, z1, "boards")
    m.set(x0, 1, 6, "door_lo")
    m.set(x0, 2, 6, "door_hi")
    for z in (4, 8):
        m.box(x0, x0, 3, 3, z, z, "pane")
    for x in (6, 7):
        m.box(x, x, 3, 3, z1, z1, "pane")
    m.set(6, 4, 6, "lantern")
    m.set(7, 4, 4, "lantern")
    m.set(7, 4, 8, "lantern")
    m.finish()
    m.part(x0, x1, z0, z1, "house")
    m.part(11, 16, 2, 10, "garden")
    return m


if __name__ == "__main__":
    raise SystemExit(run(build, reason="the house's roof and wall heads: seen, never stood on"))
