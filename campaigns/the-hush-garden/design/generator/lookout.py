#!/usr/bin/env python3
"""node/lookout — the caller's deck at the watchtower's top.

Scene: a 5 x 5 spruce deck 22 above the lanes, railed in spruce fence, four
spruce posts carrying a small hipped roof of light-green weathered cut copper.
The ladder comes up through a hatch in the middle of the deck. Four railed
arms leave through 3-wide gaps in the middle of each side. In each corner of
the deck a stone counter one course high carries that quarter's bell button,
and over each, hung from the lid on a fence, a cloth panel in its quarter's
colour (rose NW, yellow NE, blue SE, green SW).

Palette, measured with `tools/creator/block-appearance.py` against the pinned
1.21.11 client jar:
  deck, lid       minecraft:spruce_planks                #735531
  posts, beam     minecraft:spruce_log                   #543b20
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
from starter import Model, fence, ladder, lantern, pane, pillar, run, slab  # noqa: E402

# The starter starts the survey's walk in a down-face opening's own cells, a
# hole with nothing under it in this frame, so a body climbing up through the
# hatch reaches no deck. A body leaves the ladder onto the deck beside the
# hatch: those walk-plane cells are handed to the survey as where it comes in.
_ask = starter.ask_engine
_PLACE = {}


def _ask_from_the_hatch(delvec, request):
    p = _PLACE["place"]
    d = p.datum.value
    for s in p.seams:
        if s["seam"]["face"] != "down":
            continue
        lo, hi = [b.value for b in s["lo"]], [b.value for b in s["hi"]]
        hole = {(x, z) for x in range(lo[0], hi[0]) for z in range(lo[2], hi[2])}
        for x, z in sorted(hole):
            for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                c = (x + dx, z + dz)
                if c not in hole and p.in_space_xz(*c):
                    request["from"].append([c[0], d, c[1]])
    return _ask(delvec, request)


starter.ask_engine = _ask_from_the_hatch

# The deck is roofed and railed, open between rail and eave: a covered space,
# so its envelope is `open` (grammar.md, `contract-closure`), where the
# starter declares every roofed room `enclosed`.
_contract = starter.contract


def _contract_open_deck(p):
    c = _contract(p)
    c["spaces"]["room"]["envelope"] = "open"
    return c


starter.contract = _contract_open_deck

# The ladder runs up through the hatch: the down-face opening's cells hold a
# ladder on the hatch's south jamb, claimed as the way it is (the starter
# keeps every opening air, which leaves a body on the shaft's last rung a
# course short of the deck).
HATCH_LADDER = "ladder-hatch"  # bound in build()
_base_cell = starter.Plot.base_cell


def _base_cell_with_ladder(self, x, y, z):
    kind = _base_cell(self, x, y, z)
    for s in self.seams:
        if s["seam"]["face"] == "down" and kind == ("claim", f"{s['stem']}-way", None):
            return ("claim", kind[1], HATCH_LADDER)
    return kind


starter.Plot.base_cell = _base_cell_with_ladder

COPPER = "waxed_weathered_cut_copper"

# The four buttons, each at the deck's corner over its own quarter of the
# maze, in its quarter's colour: x runs east, z runs south.
BUTTONS = [("button-nw", "pink_wool", 0, 0), ("button-ne", "yellow_wool", 1, 0),
           ("button-se", "blue_wool", 1, 1), ("button-sw", "green_wool", 0, 1)]
FACING = {(0, 0): "south", (1, 0): "west", (1, 1): "north", (0, 1): "east"}


def build(place):
    _PLACE["place"] = place
    m = Model(place)
    m.palette.update({
        "floor": "minecraft:spruce_planks",
        "deck": "minecraft:spruce_planks",
        "lid": "minecraft:spruce_planks",
        "post": pillar("spruce_log", "y"),
        "rail": fence("spruce"),
        "counter": "minecraft:smooth_stone",
    })
    m.palette[HATCH_LADDER] = ladder("north")
    for seam in place.seams:
        if seam["bar"] is not None:
            m.palette[f"bar-{seam['stem']}"] = pane(seam["seam"]["bar_block"].removeprefix("minecraft:"))
    (sx0, sy0, sz0), (sx1, sy1, sz1) = place.a["space"]
    d = place.datum.value  # the walk plane
    rx0, rx1, rz0, rz1 = sx0 - 1, sx1 + 1, sz0 - 1, sz1 + 1  # the ring
    lid = place.a["roof"]["lid_y"]
    top = place.a["roof"]["top_y"]

    # the deck: one course of planks under the walk plane, ring included
    m.box(rx0, rx1, d - 1, d - 1, rz0, rz1, "deck")

    # the ring: a fence rail one course high, open above it to the lid; the
    # starter cuts each arm's 3-wide gap out of it
    for x in range(rx0, rx1 + 1):
        for z in range(rz0, rz1 + 1):
            if x in (rx0, rx1) or z in (rz0, rz1):
                m.set(x, d, z, "rail")
                m.box(x, x, d + 1, lid - 1, z, z, "minecraft:air")
    # four corner posts carrying the roof
    for x in (rx0, rx1):
        for z in (rz0, rz1):
            m.box(x, x, d, lid - 1, z, z, "post")

    # the counter: one stone course in each corner of the deck, the arms'
    # lanes running between them; on it the button's place, and one course
    # over it the quarter's colour hung from the lid on a fence, so the
    # counter's top has a single course of headroom and no body stands on it
    # to vault the rail
    for stem, wool, i, k in BUTTONS:
        x, z = (sx0, sx1)[i], (sz0, sz1)[k]
        m.set(x, d, z, "counter")
        m.clear(x, x, d + 1, d + 1, z, z)
        m.mark(stem, x, z, facing=FACING[(i, k)], y=d + 1)
        m.set(x, d + 2, z, f"minecraft:{wool}")
        m.box(x, x, d + 3, lid - 1, z, z, "rail")

    # the bell book's place, on the deck one in from the north-west counter
    # (clear of the rows behind the arms' gaps), under a spruce card board hung
    # from the lid: the shelf the story stands there has one course of
    # headroom too
    bbx, bbz = sx0 + 1, sz0 + 1
    m.mark("bell-book", bbx, bbz, facing="east", y=d)
    m.set(bbx, d + 2, bbz, "minecraft:spruce_planks")
    m.box(bbx, bbx, d + 3, lid - 1, bbz, bbz, "rail")

    # light: lanterns hung from the lid over each arm's mouth
    cx, cz = (sx0 + sx1) // 2, (sz0 + sz1) // 2
    for x, z in ((cx, sz0), (cx, sz1), (sx1, cz), (sx0 + 1, cz)):
        m.set(x, lid - 1, z, lantern(hanging=True))

    # the lid and a hipped copper roof on the posts, its eaves one out
    m.box(rx0, rx1, lid, lid, rz0, rz1, "lid")
    m.roof(rx0, rx1, rz0, rz1, lid, "x", COPPER, overhang=place.a["roof"]["eaves"], hip=True)
    c = (rx0 + rx1) // 2
    if m.get(c, top, c) is None:
        m.set(c, top, c, slab(COPPER))
    m.show("up")  # the roof stands on the frame's top course in the open air

    # where the caller arrives: off the hatch, facing the gate tower (east)
    m.mark("node-lookout", cx + 1, cz, facing="east")

    m.finish()
    return m


raise SystemExit(run(build))
