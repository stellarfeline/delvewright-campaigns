#!/usr/bin/env python3
"""The Treehouse Camp's forest floor: writes terrain/site.png (112 x 112, 8-bit grey).

The site plan reads each pixel as a surface block at `56 + value * 51 / 255`
(integer division), so every value written here is a multiple of 5 and the
surface is exactly `56 + value / 5`. Deterministic: no randomness at all, and
a fixed number of relaxation sweeps.

Shape (DESIGN.md section 4.1):
- four flat pads, one per ground place, each its footprint and ring: the
  Root Glade on the Hearth Tree's high shelf (surface 71), the Seed House on
  its mound (69), the Watch Roots on the middle ground (65), the Loom House in
  the gully (59);
- the region's rim at 63, where it meets the valley's gap floor;
- every other column a harmonic interpolation of those (sweeps of the
  four-neighbour mean), so the forest floor has no pit and every slope is
  walkable: the script asserts no two neighbouring columns differ by more
  than one block.
"""
import struct
import sys
import zlib
from pathlib import Path

N = 112
BASE_Y = 56
SWEEPS = 4000

# (x0, z0, x1, z1) inclusive, surface y: each ground place's footprint and ring.
PADS = [
    ((21, 21, 50, 50), 71),  # Root Glade (Hearth Tree)
    ((27, 69, 44, 86), 69),  # Seed House (Seed Tree)
    ((71, 69, 88, 86), 65),  # Watch Roots (Watch Tree)
    ((71, 27, 88, 44), 59),  # Loom House (Loom Tree)
]
RIM = 63


def fixed_cells():
    fixed = {}
    for x in range(N):
        for z in range(N):
            if x in (0, N - 1) or z in (0, N - 1):
                fixed[(x, z)] = float(RIM)
    for (x0, z0, x1, z1), top in PADS:
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                fixed[(x, z)] = float(top)
    return fixed


def relax():
    fixed = fixed_cells()
    h = [[fixed.get((x, z), 64.0) for z in range(N)] for x in range(N)]
    for _ in range(SWEEPS):
        for x in range(1, N - 1):
            for z in range(1, N - 1):
                if (x, z) in fixed:
                    continue
                h[x][z] = (h[x - 1][z] + h[x + 1][z] + h[x][z - 1] + h[x][z + 1]) / 4.0
    return [[int(round(h[x][z])) for z in range(N)] for x in range(N)]


def png(rows):
    raw = b"".join(b"\x00" + bytes(r) for r in rows)

    def chunk(kind, data):
        c = kind + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", N, N, 8, 0, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")


def main():
    y = relax()
    steep = 0
    for x in range(N):
        for z in range(N):
            for dx, dz in ((1, 0), (0, 1)):
                if x + dx < N and z + dz < N and abs(y[x][z] - y[x + dx][z + dz]) > 1:
                    steep += 1
    assert steep == 0, f"{steep} neighbouring column pair(s) differ by more than one block"
    rows = []
    for z in range(N):
        row = []
        for x in range(N):
            v = (y[x][z] - BASE_Y) * 5
            assert 0 <= v <= 255 and (BASE_Y + v * 51 // 255) == y[x][z], (x, z, y[x][z])
            row.append(v)
        rows.append(row)
    out = Path(__file__).with_name("site.png")
    out.write_bytes(png(rows))
    lo = min(min(r) for r in y)
    hi = max(max(r) for r in y)
    print(f"wrote {out} ({N}x{N}); surface y {lo}..{hi}; 0 steps over one block", file=sys.stderr)


if __name__ == "__main__":
    main()
