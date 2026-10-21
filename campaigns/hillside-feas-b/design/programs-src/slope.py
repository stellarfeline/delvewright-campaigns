#!/usr/bin/env python3
"""Feasibility case B's one piece: the street, a sloping surface drawn ABOVE the
box's floor, meeting the heightmap at the ring.

    D=<delvec> DELVEWRIGHT_PREFABS=<prefabs dir> python3 slope.py

Reads the place's handout (`delvec allocation`), draws the street in world
coordinates into a voxel model and writes `programs/street.json` through the
Treehouse Camp's voxel-to-program compiler (`campaigns/hillside/design/thlib.py`,
copied from `campaigns/the-treehouse-camp/design/programs-src/thlib.py`).

What it draws: three flat terraces at the heights the ring's own terrain has
at those rows (the handout's `perimeter`, read at the west ring, so the
street's surface IS the heightmap's where they meet — the stitching is by
construction and `DW0990`'s crack check measures it), earth under them from
the claim's bottom, paving on top, kerbs at the sides, and one tread row
between each two terraces. A piece's space is ONE floor (at most two
consecutive levels, `contract-well-formed`), so a sloping street cannot be one
space: each terrace is a space and each step a `stair` edge whose via is its
tread row — the first shape of this piece, a 0.3 ramp in one space, was
refused with "7 levels". The seam's opening is left open; the rest of the
south ring row above its fixed ground is a two-high parapet whose top is
declared out of walk, so the only way onto the landing is the seam (`DW0838`).
Marks: every owed anchor at a cell a body stands in; `spawn` carries
`role: entry`.
"""
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "hillside" / "design"))
import thlib  # noqa: E402

C = str(HERE.parents[1])
PREFABS = os.environ.get("DELVEWRIGHT_PREFABS", "")
CAMPAIGN = "hillside-feas-b"
PLACE = "node/street"

PAVING = [(6, "cobblestone"), (2, "mossy_cobblestone"), (1, "stone_bricks")]
KERB = "polished_andesite"
EARTH = "dirt"
PARAPET = "stone_bricks"


def main():
    h = thlib.handout(C, PLACE, PREFABS)
    m = thlib.Model(h)
    (wx0, wy0, wz0) = h["world_min"]
    ex, ey, ez = h["extent"]
    floor = wy0 + h["datum_y"]
    top = wy0 + ey - 1
    (sx0, sy0, sz0), (sx1, sy1, sz1) = h["space"]           # piece-local play space corners
    x0, x1 = wx0 + sx0, wx0 + sx1
    z0, z1 = wz0 + sz0, wz0 + sz1
    bottom = wy0 + h["ground"]["bottom_y"]

    # The ring's terrain height per row, read at the west ring column (local x 0).
    # A perimeter entry is `[x, top, z]`, all piece-local (the handout's doc
    # comment says `[x, z, top]`; the bytes say otherwise).
    ring = {(p[0], p[2]): wy0 + p[1] for p in h["ground"]["perimeter"]}

    # The street's three terraces, as the heightmap steps them at the ring
    # (terrain/site.py), with one tread row between each two: a space is ONE
    # floor (`contract-well-formed`), so each terrace is a space and each step
    # is a `stair` edge whose via is its tread row.
    upper = [z for z in range(z0, z1 + 1) if ring[(0, z - wz0)] == floor + 3]
    middle = [z for z in range(z0, z1 + 1) if ring[(0, z - wz0)] == floor + 1]
    lower = [z for z in range(z0, z1 + 1) if ring[(0, z - wz0)] == floor - 1]
    if not (upper and middle and lower) or len(upper) + len(middle) + len(lower) != z1 - z0 + 1:
        raise SystemExit(f"the ring does not step in three terraces: {sorted(set(ring[(0, z - wz0)] for z in range(z0, z1 + 1)))}")
    tread_2, tread_1 = middle[0], lower[0]          # the first row of each lower terrace is its tread
    surface = {}
    for z in upper:
        surface[z] = floor + 3
    for z in middle:
        surface[z] = floor + 1
    for z in lower:
        surface[z] = floor - 1
    surface[tread_2] = floor + 2
    surface[tread_1] = floor

    # The street: earth up to the surface, paving at the surface, kerbs at the sides.
    for z in range(z0, z1 + 1):
        s = surface[z]
        for x in range(x0, x1 + 1):
            for y in range(bottom, s):
                m.set(x, y, z, EARTH)
            if x in (x0, x1):
                m.set(x, s, z, KERB)
            else:
                m.set(x, s, z, m.pick(x, s, z, PAVING))

    # The seam: its cells stay open; the rest of the south ring row above the
    # fixed ground is a parapet two high, and its top is declared out of walk.
    seam = h["seams"][0]
    (c0, c1) = seam["cells"]
    open_x = set(range(wx0 + min(c0[0], c1[0]), wx0 + max(c0[0], c1[0]) + 1))
    ring_z = wz0 + c0[2]
    ground_z = wy0 + seam["ground_y"]
    parapet_top = []
    for x in range(x0 - 1, x1 + 2):
        if x in open_x:
            continue
        for y in (ground_z + 1, ground_z + 2):
            m.set(x, y, ring_z, PARAPET)
        parapet_top.append((x, ground_z + 3, ring_z, x, ground_z + 3, ring_z))

    # Contract: three one-floor spaces, two flights between them, the seam as
    # the lower terrace's exterior edge, the parapet's top out of walk.
    via = (wx0 + c0[0], wy0 + c0[1], wz0 + c0[2], wx0 + c1[0], wy0 + c1[1], wz0 + c1[2])
    lower_box = (x0, floor, lower[1], x1, top, z1)
    m.space("lower", "open", *thlib.subtract(lower_box, [via]))
    m.space("middle", "open", (x0, floor + 2, middle[1], x1, top, middle[-1]))
    m.space("upper", "open", (x0, floor + 4, z0, x1, top, upper[-1]))
    m.via("flight-1", (x0, floor + 1, tread_1, x1, floor + 3, tread_1))
    m.via("flight-2", (x0, floor + 3, tread_2, x1, floor + 5, tread_2))
    m.via("street-landing", via)
    m.entry = "lower"
    cls = seam.get("answer_with", ["walk"])[0]
    m.edge(a="lower", b="exterior", **{"class": cls, "via": "street-landing"})
    m.edge(a="lower", b="middle", **{"class": "stair", "rise": 2, "via": "flight-1"})
    m.edge(a="middle", b="upper", **{"class": "stair", "rise": 2, "via": "flight-2"})
    west = [b for b in parapet_top if b[0] < min(open_x)]
    east = [b for b in parapet_top if b[0] > max(open_x)]
    m.nobody("parapet-top", "the top of the parapet at the street's foot: nobody climbs up here",
             (west[0][0], west[0][1], ring_z, west[-1][0], west[-1][1], ring_z),
             (east[0][0], east[0][1], ring_z, east[-1][0], east[-1][1], ring_z))

    # Owed names: the spawn at the top of the street (the walk comes down the
    # whole piece), the node anchor on the middle terrace.
    mid_x = (x0 + x1) // 2
    for name in h["owed_anchors"]:
        stem = name.split("/", 1)[1] if "/" in name else name
        if name == "spawn":
            m.mark(stem, mid_x, floor + 4, upper[len(upper) // 2], "south", role="entry")
        else:
            m.mark(stem, mid_x, floor + 2, middle[len(middle) // 2], "south")

    prog = m.program(f"{CAMPAIGN}-street")
    path = Path(C) / "programs" / "street.json"
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(prog, indent=1) + "\n")
    print(f"street: {len(m.cells)} blocks, {len(prog['rules'])} rules, {len(prog['palette'])} roles, "
          f"faces {prog['shown_faces']}, surface {min(surface.values())}..{max(surface.values())} over floor {floor}, "
          f"owed {h['owed_anchors']}, {path.stat().st_size} bytes")


if __name__ == "__main__":
    main()
