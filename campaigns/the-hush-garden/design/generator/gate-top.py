#!/usr/bin/env python3
"""node/gate-top: the gate tower's flat roof.

Pale sandstone paving inside a crenellated parapet: a sandstone parapet course,
smooth-sandstone merlons on every other cell with half-height slab crenels
between (too high to climb from the deck), lanterns on the corner and middle
merlons. The bridge lands through the gap in the west parapet; the hatch the
ladder comes up through stands open in the deck. A garden flag on a spruce
pole stands in the north-east corner. Nothing on the deck is a step a body
can stand on: from any step a sprint jump clears a crenel and the tower.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
import starter  # noqa: E402
from starter import Model, fence, ladder, lantern, run, slab, stairs  # noqa: E402

# The climb up the gate tower comes through a hole in this deck, and the plane
# is this place's: the rung in the hole is the hole owner's to hang (the lower
# place hangs its ladder only up to its own ceiling), or a body on the top
# rung below meets the deck's underside and nothing to hold. The starter keeps
# every opening cell air, so the hole's cells are answered here with the rung,
# still claimed as the seam's way.
HATCH = "up-the-gate-tower"
_base_cell = starter.Place.base_cell


def _hatch_cell(self, x, y, z):
    kind = _base_cell(self, x, y, z)
    if kind[0] == "claim" and kind[1] == f"{HATCH}-way":
        return ("claim", kind[1], "hatch-rung")
    return kind


starter.Place.base_cell = _hatch_cell


def build(place):
    m = Model(place)
    ex, ez = m.ex, m.ez
    x1, z1 = ex - 1, ez - 1
    d = place.datum.value
    m.palette.update({
        "paving": [
            {"weight": 8, "block": "minecraft:smooth_sandstone"},
            {"weight": 2, "block": "minecraft:sandstone"},
        ],
        "worn": [
            {"weight": 5, "block": "minecraft:smooth_sandstone"},
            {"weight": 4, "block": "minecraft:sandstone"},
            {"weight": 1, "block": "minecraft:cut_sandstone"},
        ],
        "kerb": "minecraft:cut_sandstone",
        "parapet": "minecraft:sandstone",
        "merlon": "minecraft:smooth_sandstone",
        "corner": "minecraft:chiseled_sandstone",
        "crenel": slab("smooth_sandstone"),
        "lantern": lantern(),
        # the top rung, in the hatch, hung on the paving east of it
        "hatch-rung": ladder("west"),
        # the starter's ring wall stands where the drawing leaves a ring cell
        # unwritten or cleared; over the parapet that is open sky
        "wall": "minecraft:air",
    })

    # The deck: a kerb of cut sandstone under the parapet, paving inside, and
    # a worn strip where feet pass from the bridge's landing to the hatch.
    m.box(0, x1, d - 1, d - 1, 0, z1, "kerb")
    m.box(1, x1 - 1, d - 1, d - 1, 1, z1 - 1, "paving")
    m.box(1, 6, d - 1, d - 1, 5, 7, "worn")

    # The parapet: one full course, then merlons on every other cell (the
    # corners always), a half-height crenel between, nothing above.
    ring = [(x, z) for x in range(ex) for z in range(ez) if x in (0, x1) or z in (0, z1)]
    for x, z in ring:
        m.set(x, d, z, "parapet")
        along = z if x in (0, x1) else x
        corner = x in (0, x1) and z in (0, z1)
        if corner:
            m.set(x, d + 1, z, "corner")
        elif along % 2 == 0:
            m.set(x, d + 1, z, "merlon")
        else:
            m.set(x, d + 1, z, "crenel")

    # Lanterns on the corner merlons and the middle merlons of the long sides.
    for x, z in [(0, 0), (x1, 0), (0, z1), (x1, z1), (x1, 4), (x1, 6), (4, 0), (4, z1)]:
        m.set(x, d + 2, z, "lantern")
    m.show("up")

    # A garden flag on a spruce pole in the north-east corner: a fence post
    # is too tall to stand on from the deck, so it is no step over a crenel.
    m.box(x1 - 1, x1 - 1, d, d + 1, 1, 1, fence("spruce"))
    m.set(x1 - 1, d + 2, 1, "minecraft:light_blue_banner[rotation=4]")

    m.mark("bridge-bar-far", 2, 6, facing="east")
    m.mark("node-gate-top", 4, 6, facing="west")
    m.finish()
    return m


raise SystemExit(run(build))
