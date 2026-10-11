"""A greyscale 8-bit PNG writer, stdlib only (the site plan's heightmap)."""

import struct
import zlib


def write_grey(path, width, height, value_at):
    """`value_at(px, pz)` -> 0..255; row pz is the image's row."""
    raw = bytearray()
    for pz in range(height):
        raw.append(0)
        for px in range(width):
            v = int(value_at(px, pz))
            raw.append(max(0, min(255, v)))

    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 0, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(raw), 9))
    png += chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)
