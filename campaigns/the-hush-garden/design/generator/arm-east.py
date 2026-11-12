#!/usr/bin/env python3
"""node/arm-east: the east arm of the lookout's cross.

A walkway three wide running east from the deck over the maze, floored in
clear glass so the caller sees the lanes straight below: the glass rests on
two dark oak beams that run under the rails and nowhere under the walk, a low
spruce rail stands on each beam at hand height, a lantern sits on the rail's
post every six cells on both rails, and at the far end a dark oak gate frame
holds the bar the bridge's end is closed with until the gate is wound.

Palette measured with `tools/creator/block-appearance.py` against the pinned
client jar: glass #b0d6db at 65/255 coverage (the floor reads clear), dark oak
log #402e18, spruce fence #735531, lantern, iron chain, iron bars.

The rail is one course: a body cannot jump a fence, and the eye stands over
it, so the lanes below are seen across it as well as through the floor. Above
the rail the ring is the arm's open air (the starter would stand a full-height
wall on every ring cell the drawing leaves; `open_rail` below hands those
cells back as the room's air, as the starter itself does for an open place's
corner posts).
"""

import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
import starter  # noqa: E402
from starter import Model, run, chain, fence, lantern, pillar  # noqa: E402

PERIOD = 6  # a lantern on each rail every six cells


def build(place):
    m = Model(place)
    (x0, _, z0), (x1, _, z1) = place.space  # the walkway, piece-local
    d = place.datum.value
    fy = d - 1  # the floor course
    zn, zs = z0 - 1, z1 + 1  # the two rail lines (the ring's north and south runs)
    xe = x1 + 1  # the far end's plane, where the bar stands

    m.palette["glass"] = "minecraft:glass"
    m.palette["beam"] = pillar("minecraft:dark_oak_log", "x")
    m.palette["sill"] = pillar("minecraft:dark_oak_log", "z")
    m.palette["post"] = pillar("minecraft:dark_oak_log", "y")
    m.palette["lintel"] = pillar("minecraft:dark_oak_log", "x")
    m.palette["rail"] = fence("minecraft:spruce")
    for s in place.seams:
        if s["bar"] is not None:
            # the bar's block as the seam hands it, bound for the survey too
            m.palette[f"bar-{s['stem']}"] = starter.full_state(s["seam"]["bar_block"])

    lamps = [x for x in range(x0, x1 + 1) if x % PERIOD == PERIOD // 2]

    # the floor: glass across the whole walk, carried by the two beams under
    # the rails, run on to the far end; the far end's sill under the bar ties
    # the beams' ends together
    for x in range(x0, xe + 1):
        m.set(x, fy, zn, "beam")
        m.set(x, fy, zs, "beam")
        for z in range(z0, z1 + 1):
            m.set(x, fy, z, "sill" if x == xe else "glass")

    # the rail, one course high along both sides
    for x in range(x0, x1 + 1):
        m.set(x, d, zn, "rail")
        m.set(x, d, zs, "rail")
    # a lantern on the rail's post every six cells, on both rails: set on the
    # rail itself, so its top is no step up from the rail's top
    for x in lamps:
        for z in (zn, zs):
            m.set(x, d + 1, z, lantern(False))

    # the far end's frame: on each rail a pair of dark oak posts the full
    # height of the bar, one at the corner and one two cells back, under a
    # dark oak lintel on the pair, a chain hung from the lintel to the rail
    # between them, so nothing there is a step a body can stand on
    for z in (zn, zs):
        for y in range(d, d + 3):
            m.set(xe, y, z, "post")
            m.set(x1 - 1, y, z, "post")
        m.set(x1, d + 2, z, "lintel")
        m.set(x1, d + 1, z, chain("y"))
    # the chain post the bridge hangs from is the foot of the south corner
    # post: a chain under the post's head, in the bar's own plane and
    # face-adjacent to the bar, so a press on it answers for the bar, and
    # outside the way's three columns
    m.set(xe, d, zs, chain("y"))
    m.show("up")  # the posts' heads stand on the frame's top course

    m.mark("node-arm-east", (x0 + x1) // 2, (z0 + z1) // 2, facing="east")
    # the name is that chain's cell, beside the bar in its plane, outside the
    # way's clear width, never a cell a body stands in
    m.mark("bridge-bar-deck", xe, zs, facing="north", y=d)
    m.finish()
    return m


# ---- the rail is low: the ring over it is the arm's air, not a wall; a
# named block in the rail is claimed in that air ----

_base_cell = starter.Plot.base_cell


def open_rail(self, x, y, z):
    kind = _base_cell(self, x, y, z)
    if kind[0] == "fill" and any((mx, my, mz) == (x, y, z) for mx, mz, _, my in self.model.marks.values()):
        return ("claim", "room", kind[1])
    if kind in (("fill", "wall"), ("fill", "lamp")) and y >= self.datum.value and self.model.get(x, y, z) is None:
        return ("claim", "room", None)
    return kind


starter.Plot.base_cell = open_rail


# ---- the bar is a grille joined across the opening, never a row of posts ----
# The starter writes the bar's block with every arm off, which the game places
# as isolated posts a body slips between; the bar here stands in an east/west
# face, so its arms run north and south, joining each other and the posts.

_full_state = starter.full_state


def joined_bar(block: str) -> str:
    if block == "minecraft:iron_bars":
        return "minecraft:iron_bars[east=false,north=true,south=true,waterlogged=false,west=false]"
    return _full_state(block)


starter.full_state = joined_bar

raise SystemExit(run(build))
