#!/usr/bin/env python3
"""Write the shore's terrain, `design/heightmap.png`, from the numbers below.

    python3 campaigns/the-ferry-bell/design/heightmap.py

The site plan's `fill` reads this image: one 8-bit grey pixel per column of the
region (64 x 48, x east, z south), the surface block standing at
`base_y + value * range / 255` with `base_y` 56 and `range` 7. No randomness:
the shore is three bands, written as rules.

- land, surface y 63 (walked at 64): the south shore (z >= 8209) and the spit
  that closes the cove on the east (x >= 8224);
- the shelf, surface y 60: three cells of shallows along the foot of each bank;
- the cove floor, surface y 56: everything else, under six courses of water.

The water itself is the site plan's three `volumes[]`; the sea outside the
region is the ocean horizon at y 62.
"""
import pathlib
import struct
import zlib

REGION_MIN_X, REGION_MIN_Z = 8176, 8176
WIDTH, DEPTH = 64, 48
BASE_Y, RANGE = 56, 7


def value_for(top):
    """The smallest grey whose `base_y + v * range / 255` is `top`."""
    for v in range(256):
        if BASE_Y + (v * RANGE) // 255 == top:
            return v
    raise ValueError(top)


def top_at(x, z):
    if z >= 8209 or x >= 8224:
        return 63
    if z >= 8204 or x >= 8221:
        return 60
    return 56


def png(width, depth, rows):
    def chunk(kind, data):
        body = kind + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)

    raw = b"".join(b"\x00" + bytes(r) for r in rows)
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", width, depth, 8, 0, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(raw, 9))
            + chunk(b"IEND", b""))


def main():
    rows = []
    for pz in range(DEPTH):
        rows.append([value_for(top_at(REGION_MIN_X + px, REGION_MIN_Z + pz)) for px in range(WIDTH)])
    out = pathlib.Path(__file__).resolve().parent / "heightmap.png"
    out.write_bytes(png(WIDTH, DEPTH, rows))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
