#!/usr/bin/env python3
"""node/lookout — the caller's deck at the watchtower's top.

Scene: the caller climbs the shaft's ladder up through a hatch into a 5 x 5
deck floored in clear glass round a spruce rim, so the lanes 22 below show
through the floor; a one-course spruce fence rails it, broken by four 3-wide
gaps where the cross's arms run on, and four spruce posts at the corners carry
a small hipped roof of weathered copper. In each corner a stone counter one
course high carries its quarter's bell button, under a wool panel in the
quarter's colour (rose NW, yellow NE, blue SE, green SW) hung from the lid on
a fence; the bell card's shelf stands beside the north-west counter under a
hung spruce board. Every counter and the shelf have one course of headroom,
so nothing on the deck is a step a body can stand on to vault the rail.

Palette, measured with `tools/creator/block-appearance.py` against the pinned
1.21.11 client jar:
  deck floor      minecraft:glass                        #b0d6db (cov 65)
  rim, lid, board minecraft:spruce_planks                #735531
  posts           minecraft:spruce_log                   #543b20
  rail            minecraft:spruce_fence (spruce family)
  roof            minecraft:waxed_weathered_cut_copper   #6d916c (stairs, slab)
  counter         minecraft:smooth_stone                 #9f9f9f
  rose panel      minecraft:pink_wool                    #ee8dac
  yellow panel    minecraft:yellow_wool                  #f9c628
  blue panel      minecraft:blue_wool                    #35399d
  green panel     minecraft:green_wool                   #556e1c
"""

import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
import starter  # noqa: E402
from starter import Model, fence, ladder, lantern, pillar, run, slab  # noqa: E402

# The hatch: the down-face opening's cell holds the top rung of the shaft's
# ladder, hung on the plank frame's south side, claimed as the way it is.
# The starter keeps every opening air, which leaves a body on the shaft's
# last rung a course short of the deck (DW0986).
HATCH_LADDER = "ladder-hatch"
_base_cell = starter.Plot.base_cell


def _base_cell_with_ladder(self, x, y, z):
    kind = _base_cell(self, x, y, z)
    for s in self.seams:
        if s["seam"]["face"] == "down" and kind == ("claim", f"{s['stem']}-way", None):
            return ("claim", kind[1], HATCH_LADDER)
    return kind


starter.Plot.base_cell = _base_cell_with_ladder

# The deck is roofed and railed but open between rail and eave on every side:
# a covered space, so its envelope is `open` (grammar.md, `contract-closure`),
# where the starter declares every roofed room `enclosed`.
_contract = starter.contract


def _contract_open_deck(p):
    c = _contract(p)
    c["spaces"]["room"]["envelope"] = "open"
    return c


starter.contract = _contract_open_deck

COPPER = "waxed_weathered_cut_copper"

# The four buttons, each at the deck's corner over its own quarter of the
# maze, in its quarter's colour: x runs east, z runs south.
BUTTONS = [("button-nw", "pink_wool", 0, 0), ("button-ne", "yellow_wool", 1, 0),
           ("button-se", "blue_wool", 1, 1), ("button-sw", "green_wool", 0, 1)]
FACING = {(0, 0): "south", (1, 0): "west", (1, 1): "north", (0, 1): "east"}


def build(place):
    m = Model(place)
    m.palette.update({
        "glass": "minecraft:glass",
        "rim": "minecraft:spruce_planks",
        "lid": "minecraft:spruce_planks",
        "post": pillar("spruce_log", "y"),
        "rail": fence("spruce"),
        "counter": "minecraft:smooth_stone",
    })
    m.palette[HATCH_LADDER] = ladder("north")
    (sx0, _, sz0), (sx1, _, sz1) = place.a["space"]
    d = place.datum.value  # the walk plane
    rx0, rx1, rz0, rz1 = sx0 - 1, sx1 + 1, sz0 - 1, sz1 + 1  # the ring
    lid = place.a["roof"]["lid_y"]
    top = place.a["roof"]["top_y"]
    cx, cz = (sx0 + sx1) // 2, (sz0 + sz1) // 2  # the hatch's column

    # the deck: clear glass inside a spruce rim, and a spruce frame round the
    # hatch that the ladder's top rung hangs on
    # outside the ring the floor course is the arms' and the site's: air
    m.box(0, place.n[0] - 1, d - 1, d - 1, 0, place.n[2] - 1, "minecraft:air")
    m.box(rx0, rx1, d - 1, d - 1, rz0, rz1, "rim")
    m.box(sx0, sx1, d - 1, d - 1, sz0, sz1, "glass")
    m.box(cx - 1, cx + 1, d - 1, d - 1, cz - 1, cz + 1, "rim")

    # the ring: a fence rail one course high, open above it to the lid; the
    # arms' 3-wide gaps are the seams' openings, kept clear
    for x in range(rx0, rx1 + 1):
        for z in range(rz0, rz1 + 1):
            if x in (rx0, rx1) or z in (rz0, rz1):
                m.set(x, d, z, "rail")
                m.box(x, x, d + 1, lid - 1, z, z, "minecraft:air")
    # four corner posts carrying the roof
    for x in (rx0, rx1):
        for z in (rz0, rz1):
            m.box(x, x, d, lid - 1, z, z, "post")

    # the counters: one stone course in each corner of the deck, the arms'
    # lanes running between them; on each the button's place, and one course
    # over it the quarter's colour hung from the lid on a fence, so a counter
    # top has a single course of headroom and no body stands on it
    for stem, wool, i, k in BUTTONS:
        x, z = (sx0, sx1)[i], (sz0, sz1)[k]
        m.set(x, d, z, "counter")
        m.set(x, d + 1, z, starter.AIR)
        m.mark(stem, x, z, facing=FACING[(i, k)], y=d + 1)
        m.set(x, d + 2, z, f"minecraft:{wool}")
        m.box(x, x, d + 3, lid - 1, z, z, "rail")

    # the bell card's shelf, on the deck diagonally in from the north-west
    # counter (clear of the rows behind the arms' gaps), under a spruce board
    # hung from the lid: the shelf the story stands there has one course of
    # headroom too
    bbx, bbz = sx0 + 1, sz0 + 1
    m.mark("bell-book", bbx, bbz, facing="east", y=d)
    m.set(bbx, d + 2, bbz, "rim")
    m.box(bbx, bbx, d + 3, lid - 1, bbz, bbz, "rail")

    # light: lanterns hung from the lid over each arm's mouth
    for x, z in ((cx, sz0), (cx, sz1), (sx1, cz), (sx0, cz)):
        m.set(x, lid - 1, z, lantern(hanging=True))

    # the lid and a hipped copper roof on the posts, its eaves one out
    m.box(rx0, rx1, lid, lid, rz0, rz1, "lid")
    m.roof(rx0, rx1, rz0, rz1, lid, "x", COPPER, overhang=place.a["roof"]["eaves"], hip=True)
    if m.get(cx, top, cz) is None:
        m.set(cx, top, cz, slab(COPPER))
    m.show("up")  # the roof stands on the frame's top course in the open air

    # where the caller arrives: off the hatch, facing the gate tower (east)
    m.mark("node-lookout", cx + 1, cz, facing="east")

    m.finish()
    return m


raise SystemExit(run(build))
