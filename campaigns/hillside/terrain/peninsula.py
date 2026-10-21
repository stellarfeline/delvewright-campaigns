#!/usr/bin/env python3
"""The hillside town's peninsula: writes terrain/peninsula.png (144 x 224,
8-bit grey) and terrain/peninsula.txt (a coarse contour picture of it).

Shared by both variants of the comparison (DESIGN.md section 4): the same
pixels are the `fill.terrain.heightmap` of `hillside-a` and `hillside-b`.

The site plan reads a pixel as a surface block at `48 + value * 51 // 255`, so
every value here is a multiple of 5 and the surface is `48 + value / 5`
(`heightfield.RANGE`). Region: min [0, 40, 0], extent [144, 96, 224]; x runs
east, z runs south; the land side is north (low z), the sea is south. The
ocean horizon's water tops at y 62 (spec-0013): a column whose surface is 62
is the walk plane 63, dry; a surface at 61 or under is sea.

The ground is the upper envelope of features (heightfield.py):
- one pad per place of the town, footprint plus ring, at the place's walk
  plane minus one (TOWN below), falling half a block per column beyond it;
  where two pads share a ring column the higher wins, and the lower place's
  wall stands on that ground;
- three hill tops on the mainland, falling half a block per column;
- a beach pad west of the quay at 62 — walk plane 63, the one place a
  swimmer climbs out of the sea;
- the sea bed, 54, under everything;
then two fixed overrides: the harbour floor in front of the quay wall at 60
(two blocks of water against the wall), and the region's rim at 54.

The island is where the envelope stands at 62 or higher; the shore is the
62-contour, and the sea bed goes on sloping under the water to the rim.

Check: no two neighbouring open-ground columns differ by more than one block
(every slope is one half, so the envelope cannot; the assertion is on the
rounded integers). A step over one where a pad's ring is one side is a wall's
footing and is counted, not refused.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import heightfield as hf  # noqa: E402

NX, NZ = 144, 224
BASE_Y = 48
SEA_BED = 54      # the ocean superflat's sea floor top (plan::SEA_FLOOR_TOP_Y)
SEA = 62          # the water top (plan::SEA_LEVEL)
HARBOUR_FLOOR = 60
BEACH = 62
SLOPE = 0.5

# The town, in world coordinates. Interior footprint x0..x1 × z0..z1 inclusive,
# the walk plane y, and the kind. DESIGN.md section 4 is the same table in prose
# and is the authority; this file is derived from it.
TOWN = [
    # way places (sky-open)
    ("square",        65, 96, 82, 109, 84, "way"),
    ("stair-upper",   71, 111, 76, 116, 80, "stair"),
    ("street-upper",  71, 118, 76, 129, 80, "way"),
    ("stair-mid",     71, 131, 76, 136, 76, "stair"),
    ("street-mid",    71, 138, 76, 149, 76, "way"),
    ("stair-lower",   71, 151, 76, 156, 72, "stair"),
    ("street-lower",  71, 158, 76, 169, 72, "way"),
    ("stair-shore",   71, 171, 76, 176, 68, "stair"),
    ("street-shore",  71, 178, 76, 185, 68, "way"),
    ("stair-quay",    71, 187, 76, 192, 64, "stair"),
    ("quay",          58, 194, 89, 200, 64, "way"),
    # houses (roofed)
    ("chapel",        54, 98, 63, 106, 84, "house"),
    ("inn",           84, 97, 94, 107, 84, "house"),
    ("smithy",        62, 119, 69, 126, 80, "house"),
    ("weaver",        78, 118, 84, 128, 80, "house"),
    ("merchant",      60, 139, 69, 148, 76, "house"),
    ("ropewalk",      78, 158, 84, 169, 72, "house"),
    ("harbourmaster", 62, 177, 69, 184, 68, "house"),
    ("warehouse",     80, 182, 89, 192, 64, "house"),
]

HILLS = [((72, 52), 84), ((48, 76), 76), ((98, 70), 76)]   # (column, surface)
BEACH_PAD = (50, 194, 56, 203)                             # x0 z0 x1 z1 at 62
HARBOUR = (57, 201, 90, 204)                               # fixed at 60


def rect(x0, z0, x1, z1):
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            yield x, z


def features():
    fs = []
    for name, x0, z0, x1, z1, floor, kind in TOWN:
        fs.append(hf.Pad(x0 - 1, z0 - 1, x1 + 1, z1 + 1, floor - 1, SLOPE))
    for (x, z), y in HILLS:
        fs.append(hf.Pad(x, z, x, z, y, SLOPE))
    x0, z0, x1, z1 = BEACH_PAD
    fs.append(hf.Pad(x0, z0, x1, z1, BEACH, SLOPE))
    return fs


def fixed_columns():
    fixed = {}
    for x in range(NX):
        for z in range(NZ):
            if x in (0, NX - 1) or z in (0, NZ - 1):
                fixed[(x, z)] = SEA_BED
    for x, z in rect(*HARBOUR):
        fixed[(x, z)] = HARBOUR_FLOOR
    return fixed


def pad_cells():
    pad = set()
    for name, x0, z0, x1, z1, floor, kind in TOWN:
        pad.update(rect(x0 - 1, z0 - 1, x1 + 1, z1 + 1))
    return pad


def main():
    fixed = fixed_columns()
    y = hf.rounded(hf.envelope(NX, NZ, features(), SEA_BED, fixed))
    pad = pad_cells()

    def land(x, z):
        return y[x][z] >= SEA

    steep = hf.steep_pairs(y, land)
    commons = [s for s in steep if s[0] not in pad and s[1] not in pad]
    walls = [s for s in steep if s[0] in pad or s[1] in pad]
    if commons:
        for a, b, d in commons[:20]:
            print(f"  open ground steps {d} between {a} and {b}", file=sys.stderr)
        raise SystemExit(f"{len(commons)} open-ground column pair(s) differ by more than one block")
    rim = [(x, z) for x in range(NX) for z in range(NZ) if land(x, z) and (x in (0, 1, NX - 2, NX - 1) or z in (0, 1, NZ - 2, NZ - 1))]
    if rim:
        raise SystemExit(f"{len(rim)} land column(s) within two of the region's rim: the island touches the edge")

    rows = hf.encode(y, BASE_Y)
    out = Path(__file__).with_name("peninsula.png")
    hf.write_png(out, rows)
    Path(__file__).with_name("peninsula.txt").write_text(hf.ascii_contours(y, SEA) + "\n")

    land_cells = sum(1 for x in range(NX) for z in range(NZ) if land(x, z))
    xs = [x for x in range(NX) for z in range(NZ) if land(x, z)]
    zs = [z for x in range(NX) for z in range(NZ) if land(x, z)]
    lo = min(min(c) for c in y)
    hi = max(max(c) for c in y)
    print(f"wrote {out} ({NX}x{NZ}); surface y {lo}..{hi}; land (surface >= {SEA}): {land_cells} columns, "
          f"x {min(xs)}..{max(xs)}, z {min(zs)}..{max(zs)}; {len(pad)} pad columns; "
          f"0 open-ground steps over one; {len(walls)} steps over one at a pad's ring (a wall's footing)",
          file=sys.stderr)


if __name__ == "__main__":
    main()
