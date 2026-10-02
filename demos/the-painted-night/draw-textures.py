#!/usr/bin/env python3
"""Draw the two textures The Painted Night replaces, from nothing.

    python3 demos/the-painted-night/draw-textures.py

writes

    campaigns/the-painted-night/textures/red-moon.png      32x32
    campaigns/the-painted-night/textures/shore-walker.png  64x64

Both are original work, made by this script and licensed with the campaign:
no vanilla pixel is read, copied or traced. `red-moon` is a plain red disc on a
transparent ground, the size of the full-moon texture it replaces.
`shore-walker` is flat bands of colour laid on the 64x64 zombie-model grid the
drowned is drawn from; it follows the grid's dimensions and nothing else, so
the mob reads as "painted" rather than as a drawing of anything.

The PNG is written by hand — signature, IHDR, one IDAT of STORED deflate
blocks, IEND — so every byte is fixed by the PNG and zlib specifications given
the pixels, and the files are the same on every machine (no compressor is
called). Run it twice and compare: the bytes do not move.
"""

from __future__ import annotations

import struct
import zlib
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parents[1] / "campaigns" / "the-painted-night" / "textures"


def chunk(kind: bytes, data: bytes) -> bytes:
    return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)


def stored_zlib(raw: bytes) -> bytes:
    """A zlib stream of stored (uncompressed) deflate blocks — RFC 1950/1951."""
    out = bytearray(b"\x78\x01")
    i = 0
    while True:
        block = raw[i : i + 65535]
        i += len(block)
        final = 1 if i >= len(raw) else 0
        out += bytes([final]) + struct.pack("<HH", len(block), len(block) ^ 0xFFFF) + block
        if final:
            break
    out += struct.pack(">I", zlib.adler32(raw) & 0xFFFFFFFF)
    return bytes(out)


def png(width: int, height: int, pixel) -> bytes:
    rows = bytearray()
    for y in range(height):
        rows.append(0)  # filter type 0 on every scanline
        for x in range(width):
            rows += bytes(pixel(x, y))
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)  # 8-bit RGBA
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", stored_zlib(bytes(rows))) + chunk(b"IEND", b"")


def red_moon(x: int, y: int) -> tuple[int, int, int, int]:
    # A disc of radius 11 centred in the 32x32 cell; everything else transparent.
    dx, dy = x - 15.5, y - 15.5
    if dx * dx + dy * dy <= 11.0 * 11.0:
        return (210, 28, 28, 255)
    return (0, 0, 0, 0)


def shore_walker(x: int, y: int) -> tuple[int, int, int, int]:
    # Horizontal bands every four rows in two pale lilacs, with a darker band
    # each eighth row — opaque everywhere, so every face of the model is painted.
    if (y // 4) % 8 == 7:
        return (70, 40, 110, 255)
    if (y // 4) % 2 == 0:
        return (196, 170, 232, 255)
    return (160, 128, 210, 255)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, w, h, fn in (("red-moon", 32, 32, red_moon), ("shore-walker", 64, 64, shore_walker)):
        path = OUT / f"{name}.png"
        path.write_bytes(png(w, h, fn))
        print(f"wrote {path.relative_to(HERE.parents[1])} ({w}x{h}, {path.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
