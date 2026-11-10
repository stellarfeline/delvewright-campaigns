#!/usr/bin/env python3
"""node/lookout — the caller's deck at the watchtower's top.

Scene: a 5 x 5 spruce deck 22 above the lanes, railed in spruce fence, four
spruce posts carrying a small hipped roof of light-green weathered cut copper.
The ladder comes up through a hatch in the middle of the deck. Toward the gate
tower (east) a stone counter one course high carries the four bell buttons,
and over each button, hung from a spruce beam under the roof, a cloth panel in
its quarter's colour (rose, yellow, blue, green). Behind the counter the deck
runs to the east rail, where the bridge leaves through a barred gap.

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
from starter import AIR, Model, fence, ladder, lantern, pane, pillar, run, slab  # noqa: E402

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

# The buttons in the story's order, north to south along the counter, each
# with its quarter's colour.
BUTTONS = [("button-nw", "pink_wool"), ("button-ne", "yellow_wool"), ("button-se", "blue_wool"), ("button-sw", "green_wool")]


def build(place):
    _PLACE["place"] = place
    m = Model(place)
    m.palette.update({
        "floor": "minecraft:spruce_planks",
        "deck": "minecraft:spruce_planks",
        "lid": "minecraft:spruce_planks",
        "post": pillar("spruce_log", "y"),
        "beam": pillar("spruce_log", "z"),
        "rail": fence("spruce"),
        "counter": "minecraft:smooth_stone",
    })
    m.palette[HATCH_LADDER] = ladder("north")
    # the bar each barred seam is filled with, bound here because the survey
    # writes the drawing before the program's palette binds it
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

    # the ring: a fence rail one course high, open above it to the lid
    for x in range(rx0, rx1 + 1):
        for z in range(rz0, rz1 + 1):
            if x in (rx0, rx1) or z in (rz0, rz1):
                m.set(x, d, z, "rail")
                m.box(x, x, d + 1, lid - 1, z, z, "minecraft:air")  # the ring is the wall's unless written
    # four corner posts carrying the roof
    for x in (rx0, rx1):
        for z in (rz0, rz1):
            m.box(x, x, d, lid - 1, z, z, "post")

    # the counter toward the gate tower, one course high, with the bridge
    # deck running behind it to the east rail
    cx = sx1 - 1
    for i, (stem, _) in enumerate(BUTTONS):
        z = sz0 + i
        m.set(cx, d, z, "counter")
        m.clear(cx, cx, d + 1, d + 1, z, z)
        m.mark(stem, cx, z, facing="west", y=d + 1)
    # the beam under the lid straight over the counter, and the quarter's
    # colour hung from it one course over each button: the counter's top has
    # a single course of headroom, so no body stands on it to vault the rail
    m.box(cx, cx, d + 3, lid - 1, sz0, sz0 + len(BUTTONS) - 1, "beam")
    for i, (_, wool) in enumerate(BUTTONS):
        m.set(cx, d + 2, sz0 + i, f"minecraft:{wool}")

    # the bell book's place, on the deck beside the counter's south end, under
    # a spruce card board hung from the lid on a fence: the shelf the story
    # stands there has one course of headroom too
    bbx, bbz = cx - 1, sz0 + len(BUTTONS) - 1
    m.mark("bell-book", bbx, bbz, facing="west", y=d)
    m.set(bbx, d + 2, bbz, "minecraft:spruce_planks")
    m.box(bbx, bbx, d + 3, lid - 1, bbz, bbz, "rail")

    # light: lanterns hung from the lid
    for x, z in ((sx0, sz0), (sx0, sz1), (sx0 + 2, sz0 + 2)):
        m.set(x, lid - 1, z, lantern(hanging=True))

    # the lid and a hipped copper roof on the posts, its eaves one out
    m.box(rx0, rx1, lid, lid, rz0, rz1, "lid")
    m.roof(rx0, rx1, rz0, rz1, lid, "x", COPPER, overhang=place.a["roof"]["eaves"], hip=True)
    c = (rx0 + rx1) // 2
    if m.get(c, top, c) is None:
        m.set(c, top, c, slab(COPPER))
    m.show("up")  # the roof stands on the frame's top course in the open air

    # where the caller arrives, and where a body stands at the bar
    m.mark("node-lookout", sx0 + 1, (sz0 + sz1) // 2, facing="east")
    m.mark("bridge-bar-deck", sx1, (sz0 + sz1) // 2, facing="east")

    m.finish()
    return m


raise SystemExit(run(build))
