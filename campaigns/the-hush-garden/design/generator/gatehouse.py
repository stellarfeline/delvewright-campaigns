#!/usr/bin/env python3
"""node/gatehouse of The Hush Garden: the gate tower's hall.

Scene: a tall pale-stone hall entered from the maze through an arch on the
west. A low screen wall with its own arch parts the entry (west) from the
gate bay (east), where the great gate stands in a dark-oak frame, barred by
its portcullis grille, the winch beside it and two chains running from
beside the gate up into the tower. A ladder climbs a pier up to the hatch
under the tower's top; above the screen the hall is empty to the roof,
crossed by dark-oak beams every five courses, lit by hanging lanterns and
arrow slits.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
import starter  # noqa: E402
from starter import Model, chain, full_state, ladder, lantern, pane, pillar, run, stairs  # noqa: E402

# The starter's survey stands `structure_void` on every cell the whole owns,
# the fixed ground under this place's openings included, so a body coming in
# through an opening has nothing to stand on and the survey reaches nothing.
# The world stands the whole's fixed ground there (`ground.fixed`, the
# allocation's own blocks): the survey is asked of that world.
_ask = starter.ask_engine


def _ask_with_fixed_ground(delvec, request):
    alloc = _ALLOC[0]
    # each fixed block written in the state the allocation hands its column
    states = {c["blocks"][-1].split("[")[0]: c["blocks"][-1] for c in alloc["ground"].get("columns", []) or [] if c["blocks"]}
    fixed = {tuple(f["cell"]): states.get(f["block"], f["block"]) for f in alloc["ground"].get("fixed", []) or []}
    blocks = []
    for b in request["blocks"]:
        c = tuple(b[:3])
        if b[3] == "minecraft:structure_void" and c in fixed:
            blocks.append([*c, fixed[c]])
        else:
            blocks.append(b)
    return _ask(delvec, {**request, "blocks": blocks})


starter.ask_engine = _ask_with_fixed_ground
_ALLOC = []

# measured with block-appearance.py --mix (mix C_mean ~0.06, hue ~95 deg, mean #dacda0)
WALL = "minecraft:smooth_sandstone"
BAND = "minecraft:chiseled_sandstone"
TRIM = "minecraft:cut_sandstone"
TIMBER = "dark_oak_log"


def seam(place, stem):
    s = next(s for s in place.seams if s["stem"] == stem)
    return [b.value for b in s["lo"]], [b.value for b in s["hi"]]


def build(place):
    _ALLOC[:] = [place.a]
    m = Model(place)
    # the bar's role, bound as the starter binds it for the program (its
    # survey reads the model's palette before the program's is written)
    for s in place.seams:
        if s["bar"] is not None:
            m.palette[f"bar-{s['stem']}"] = full_state(s["seam"]["bar_block"])
    m.palette.update({"wall": WALL, "floor": TRIM, "band": BAND, "trim": TRIM})
    (x0, y0, z0), (x1, y1, z1) = place.space
    d = place.datum.value
    top = y1
    w_lo, w_hi = seam(place, "into-the-gatehouse")   # the arch from the maze (west)
    g_lo, g_hi = seam(place, "the-great-gate")        # the great gate (east)
    gz0, gz1 = g_lo[2], g_hi[2] - 1
    gate_head = g_hi[1]                                # first course over the bars
    wz0, wz1 = w_lo[2], w_hi[2] - 1
    door_head = w_hi[1]

    # the floor: paved
    m.box(x0, x1, d - 1, d - 1, z0, z1, "floor")

    # the shell: smooth sandstone, with chiselled bands at the gate's head
    # course and again higher up
    xw, xe, zn, zs = x0 - 1, x1 + 1, z0 - 1, z1 + 1
    m.hollow(xw, xe, d, top, zn, zs, "wall")
    band_ys = (gate_head + 1, gate_head + 8)
    for y in band_ys:
        m.hollow(xw, xe, y, y, zn, zs, "band")

    # arrow slits: one wide, two high, glazed, high in every wall
    slit = pane("glass_pane")
    for y in (gate_head + 4, gate_head + 11):
        x = (x0 + x1) // 2
        m.box(x, x, y, y + 1, zn, zn, slit)
        m.box(x, x, y, y + 1, zs, zs, slit)
        for z in (z0 + 1, z1 - 1):
            m.box(xw, xw, y, y + 1, z, z, slit)
            m.box(xe, xe, y, y + 1, z, z, slit)

    # the great gate's dark-oak frame: posts either side, a lintel over
    for z in (gz0 - 1, gz1 + 1):
        m.box(xe, xe, d, gate_head, z, z, pillar(TIMBER, "y"))
    m.box(xe, xe, gate_head, gate_head, gz0, gz1, pillar(TIMBER, "z"))

    # the maze arch's reveal inside: jambs, springers, a head with a keystone
    for z in (wz0 - 1, wz1 + 1):
        m.box(x0, x0, d, door_head - 1, z, z, "trim")
    m.set(x0, door_head - 1, wz0 - 1, stairs("smooth_sandstone", "north", "top"))
    m.set(x0, door_head - 1, wz1 + 1, stairs("smooth_sandstone", "south", "top"))
    m.box(x0, x0, door_head, door_head, wz0 - 1, wz1 + 1, "trim")
    m.set(x0, door_head, wz0, "band")

    # the screen wall parting the entry from the gate bay, with its arch
    sx = x0 + 2
    m.box(sx, sx, d, gate_head + 1, z0, z1, "wall")
    m.box(sx, sx, gate_head + 1, gate_head + 1, z0, z1, "band")
    m.clear(sx, sx, d, d + 2, wz0, wz1)
    m.set(sx, d + 2, wz0, stairs("smooth_sandstone", "north", "top"))
    m.set(sx, d + 2, wz1, stairs("smooth_sandstone", "south", "top"))
    m.set(sx, d + 3, wz0, "band")
    m.set(sx, d + 3, wz1, "band")

    # the ladder up the inner wall's pier to the hatch: the pier stands one
    # cell north of the hatch's column, from the floor to the top course, and
    # the ladder hangs on its south face up to the course under the hatch
    h_lo, _ = seam(place, "up-the-gate-tower")
    hx, hy, hz = h_lo
    m.climbs_to("up-the-gate-tower")
    m.box(hx, hx, d, top, hz - 1, hz - 1, "wall")
    for y in band_ys:
        m.set(hx, y, hz - 1, "band")
    m.box(hx, hx, d, hy - 1, hz, hz, ladder("south"))
    # the hall's ceiling of dark-oak boards on the top course, the hatch open
    # in it (its cell is the seam's), so the hatch opens only upward
    m.palette["ceiling"] = "minecraft:dark_oak_planks"
    m.box(x0, x1, hy, hy, z0, z1, "ceiling")
    # over it the tower's top, which node/gate-top draws (void to this
    # place); painted solid here only so this place's room ends at its
    # ceiling and the hatch opens upward out of it
    m.box(x0, x1, hy + 1, hy + 1, z0, z1, "ceiling")

    # beams every five courses over the screen, along the hall, clear of the ladder
    for y in range(gate_head + 3, top - 1, 5):
        for z in (z0 + 1, z1 - 1):
            m.box(x0, x1, y, y, z, z, pillar(TIMBER, "x"))
    # lanterns hung under the lowest beams
    lb = gate_head + 3
    for z in (z0 + 1, z1 - 1):
        for x in (x0 + 1, x1 - 1):
            m.set(x, lb - 1, z, lantern(hanging=True))

    # the chains: from beside the gate up into the tower
    for z in (gz0 - 1, gz1 + 1):
        m.box(x1, x1, d + 2, top, z, z, chain("y"))

    # the owed names
    m.mark("winch", x1, gz1 + 1, facing="north")
    m.mark("node-gatehouse", x0 + 1, wz1, facing="east")
    m.finish()
    return m


raise SystemExit(run(build))
