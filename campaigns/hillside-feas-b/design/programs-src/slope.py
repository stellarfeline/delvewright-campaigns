#!/usr/bin/env python3
"""Feasibility case B's one piece: the street, a sloping surface drawn ABOVE the
box's floor, meeting the heightmap at the ring.

    D=<delvec> DELVEWRIGHT_PREFABS=<prefabs dir> python3 slope.py

Reads the place's handout (`delvec allocation`), draws the street in world
coordinates into a voxel model and writes `programs/street.json` through the
Treehouse Camp's voxel-to-program compiler (`campaigns/hillside/design/thlib.py`,
copied from `campaigns/the-treehouse-camp/design/programs-src/thlib.py`).

What it draws, per footprint column: dirt from the claim's bottom up to one
under the ring's own terrain height at that row (the handout's `perimeter`,
read at the west ring, so the street's surface IS the heightmap's — the
stitching is by construction and `DW0990`'s crack check measures it), then a
paved surface at that height. A row where the surface rises by one is a
one-block step a body walks. The seam's opening is left open; the rest of the
south ring row above its fixed ground is a two-high parapet, so the only way
onto the landing is the seam (`DW0838`). Marks: every owed anchor at a cell a
body stands in; `spawn` carries `role: entry`.
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
    ring = {(p[0], p[1]): p[2] for p in h["ground"]["perimeter"]}
    surface = {}
    for lz in range(sz0, sz1 + 1):
        s = ring.get((0, lz))
        if s is None:
            raise SystemExit(f"no perimeter height at the west ring, row {lz}")
        surface[wz0 + lz] = s
    for z, s in surface.items():
        if s + 1 < floor:
            raise SystemExit(f"the ring's ground at z {z} ({s}) stands under the floor course {floor - 1}")

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
    # fixed ground is a parapet two high.
    seam = h["seams"][0]
    (c0, c1) = seam["cells"]
    open_x = set(range(wx0 + min(c0[0], c1[0]), wx0 + max(c0[0], c1[0]) + 1))
    ring_z = wz0 + c0[2]
    ground_z = surface[z1]  # the row inside; the seam's ring ground is the sill minus one
    for x in range(x0 - 1, x1 + 2):
        if x in open_x:
            continue
        for y in (ground_z + 1, ground_z + 2):
            m.set(x, y, ring_z, PARAPET)

    # Contract: one open space over the whole play space minus the opening, the
    # opening as the exterior edge's via.
    via = (wx0 + c0[0], wy0 + c0[1], wz0 + c0[2], wx0 + c1[0], wy0 + c1[1], wz0 + c1[2])
    play = (x0, floor, z0, x1, top, z1)
    m.space("street", "open", *thlib.subtract(play, [via]))
    m.via("street-landing", via)
    m.entry = "street"
    cls = seam.get("answers", ["walk"])[0]
    m.edge(a="street", b="exterior", **{"class": cls, "via": "street-landing"})

    # Owed names, each at a cell a body stands in.
    mid_x = (x0 + x1) // 2
    for i, name in enumerate(h["owed_anchors"]):
        stem = name.split("/", 1)[1] if "/" in name else name
        z = z0 + 3 + 3 * i
        m.mark(stem, mid_x, surface[z] + 1, z, "south", role="entry" if name == "spawn" else None)

    prog = m.program(f"{CAMPAIGN}-street")
    path = Path(C) / "programs" / "street.json"
    path.write_text(json.dumps(prog, indent=1) + "\n")
    print(f"street: {len(m.cells)} blocks, {len(prog['rules'])} rules, {len(prog['palette'])} roles, "
          f"faces {prog['shown_faces']}, surface {min(surface.values())}..{max(surface.values())} over floor {floor}, "
          f"owed {h['owed_anchors']}, {path.stat().st_size} bytes")


if __name__ == "__main__":
    main()
