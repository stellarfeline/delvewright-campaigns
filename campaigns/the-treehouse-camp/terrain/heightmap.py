#!/usr/bin/env python3
"""The Treehouse Camp's forest floor: writes terrain/site.png (112 x 112, 8-bit grey).

The site plan reads each pixel as a surface block at `56 + value * 51 / 255`
(integer division), so every value written here is a multiple of 5 and the
surface is exactly `56 + value / 5`. No randomness beyond the stated SEED,
which feeds an integer hash; running this twice writes the same bytes.

Shape (DESIGN.md section 4.1):
- a high shelf under the Hearth Tree, surface 71;
- a mound under the Seed Tree, surface 69;
- middle ground under the Watch Tree, surface 65;
- gullies between them, surface 61, under the Loom Tree and under the two
  eastern and northern bridges, and a shallower one (65) under the Low Bridge;
- the edge of the region at 63, where it meets the valley's gap floor.

Every place's footprint and ring is flat at one height (`PADS`), so the ground a
place is handed is one height across its plot.
"""
import struct
import sys
import zlib
from pathlib import Path

SEED = 20261009
N = 112
BASE_Y = 56

# (x0, z0, x1, z1) inclusive, surface y. Footprint plus its one-cell ring.
PADS = [
    ((23, 23, 48, 48), 71),  # Root Glade (Hearth Tree)
    ((27, 69, 44, 86), 69),  # Seed House (Seed Tree)
    ((69, 71, 86, 88), 65),  # Watch Roots (Watch Tree)
    ((69, 27, 86, 44), 61),  # Loom House (Loom Tree)
    ((49, 33, 68, 38), 61),  # Long Bridge, inside the two tree rings
    ((33, 49, 38, 68), 65),  # Low Bridge
    ((75, 45, 80, 68), 61),  # High Bridge
]

# Plateaus over the base field: (cx, cz, flat radius, fade, surface).
PLATEAUS = [
    (35.5, 35.5, 17.0, 6.0, 71),
    (35.5, 77.5, 11.0, 6.0, 69),
    (77.5, 79.5, 12.0, 5.0, 65),
]


def hash01(x, z):
    h = (x * 374761393 + z * 668265263 + SEED * 2246822519) & 0xFFFFFFFF
    h = ((h ^ (h >> 13)) * 1274126177) & 0xFFFFFFFF
    return ((h ^ (h >> 16)) & 0xFFFF) / 65535.0


def noise(x, z):
    """Value noise on an 8-cell lattice, smoothly interpolated: 0..1."""
    gx, gz = x // 8, z // 8
    fx, fz = (x % 8) / 8.0, (z % 8) / 8.0
    sx, sz = fx * fx * (3 - 2 * fx), fz * fz * (3 - 2 * fz)
    a, b = hash01(gx, gz), hash01(gx + 1, gz)
    c, d = hash01(gx, gz + 1), hash01(gx + 1, gz + 1)
    top = a + (b - a) * sx
    bot = c + (d - c) * sx
    return top + (bot - top) * sz


def smooth(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def height(x, z):
    # The gully floor and the forest between, gently broken.
    base = 61.0 + 2.0 * noise(x, z)
    # The rim of the region meets the valley's gap floor at 63.
    edge = min(x, z, N - 1 - x, N - 1 - z)
    if edge < 10:
        base = base + (63.0 - base) * smooth((10 - edge) / 10.0)
    h = base
    for cx, cz, flat, fade, top in PLATEAUS:
        d = ((x + 0.5 - cx) ** 2 + (z + 0.5 - cz) ** 2) ** 0.5
        s = 1.0 - smooth((d - flat) / fade)
        h = max(h, base + (top - base) * s)
    y = int(round(h))
    for (x0, z0, x1, z1), top in PADS:
        if x0 <= x <= x1 and z0 <= z <= z1:
            y = top
    return y


def png(rows):
    raw = b"".join(b"\x00" + bytes(r) for r in rows)

    def chunk(kind, data):
        c = kind + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", N, N, 8, 0, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")


def main():
    out = Path(__file__).with_name("site.png")
    rows = []
    for z in range(N):
        row = []
        for x in range(N):
            y = height(x, z)
            v = (y - BASE_Y) * 5
            assert 0 <= v <= 255 and (BASE_Y + v * 51 // 255) == y, (x, z, y)
            row.append(v)
        rows.append(row)
    out.write_bytes(png(rows))
    lo = min(min(r) for r in rows) // 5 + BASE_Y
    hi = max(max(r) for r in rows) // 5 + BASE_Y
    print(f"wrote {out} ({N}x{N}); surface y {lo}..{hi}", file=sys.stderr)


if __name__ == "__main__":
    main()
