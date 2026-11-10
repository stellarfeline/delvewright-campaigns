#!/usr/bin/env python3
"""node/arm-north: the lookout's north arm, a railed walkway over the maze.

Spruce planks laid on dark oak beams (two stringers under the rails, a cross
beam under every lantern post), a one-course spruce fence rail down both sides
and across the far end so the lanes are seen over it, and a lantern on a
two-fence post every six cells from the far end.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
from starter import AIR, Model, fence, lantern, pillar, run  # noqa: E402

POST_EVERY = 6  # a lantern post every six cells, counted from the far end


def build(place):
    m = Model(place)
    (x0, _, z0), (x1, _, z1) = place.space
    w = place.datum.value          # the walk plane
    g = w - 1                      # the floor course
    rx0, rx1, rz0 = x0 - 1, x1 + 1, z0 - 1  # the rail's ring: both sides and the far end
    top = m.ey - 1

    m.palette["floor"] = "minecraft:spruce_planks"
    m.palette["boards"] = "minecraft:spruce_planks"
    # The ring above the rail is open air: the rail is one course, so the
    # eye looks over it at the lanes (a parapet is one course).
    m.palette["wall"] = "minecraft:air"
    m.palette["lamp"] = "minecraft:air"
    m.palette["rail"] = fence("spruce")
    m.palette["post"] = fence("spruce")
    m.palette["light"] = lantern(False)
    m.palette["stringer"] = pillar("minecraft:dark_oak_log", "z")
    m.palette["beam"] = pillar("minecraft:dark_oak_log", "x")

    # the deck boards over the whole floor course
    m.box(rx0, rx1, g, g, rz0, z1, "boards")
    # the beams the boards rest on: a stringer under each rail
    for x in (rx0, rx1):
        m.box(x, x, g, g, rz0, z1, "stringer")
    # the far end's beam under its rail
    m.box(x0, x1, g, g, rz0, rz0, "beam")

    # the rail, one course, on both sides and across the far end
    for z in range(rz0, z1 + 1):
        for x in (rx0, rx1):
            m.set(x, w, z, "rail")
    for x in range(x0, x1 + 1):
        m.set(x, w, rz0, "rail")
    # air over the rail up to the frame's top
    m.box(rx0, rx0, w + 1, top, rz0, z1, AIR)
    m.box(rx1, rx1, w + 1, top, rz0, z1, AIR)
    m.box(x0, x1, w + 1, top, rz0, rz0, AIR)

    # a lantern on a post every six cells from the far end, on both rails,
    # each over a cross beam
    for z in range(rz0, z1 + 1, POST_EVERY):
        if z > rz0:
            m.box(x0, x1, g, g, z, z, "beam")
        for x in (rx0, rx1):
            for y in range(w, top):
                m.set(x, y, z, "post")
            m.set(x, top, z, "light")
    m.show("up")

    # the walkway itself is the clear way: nothing stands on it
    m.clear(x0, x1, w, top, z0, z1)

    # where a body stands on the arm: at its far end, looking out
    m.mark("node-arm-north", (x0 + x1) // 2, z0, facing="north")
    m.finish()
    return m


raise SystemExit(run(build))
