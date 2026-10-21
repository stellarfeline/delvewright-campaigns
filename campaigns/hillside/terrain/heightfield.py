#!/usr/bin/env python3
"""A deterministic heightfield for a site plan's `fill.terrain.heightmap`.

The site plan reads each pixel as a surface block at
`base_y + value * range // 255`; with `range = 51` every value written here is
a multiple of 5 and the surface is exactly `base_y + value / 5`, so a height
round-trips without loss (the Treehouse Camp's encoding).

Shape: the ground is the upper envelope of FEATURES — a flat pad (a rectangle
at one height), a ramp (a rectangle sloping along z) or a peak (a pad of one
column), each falling away at a
declared slope, in blocks per column of Euclidean distance from its edge —
floored at the sea bed, with FIXED columns overriding it (a harbour floor, a
beach). The envelope of cones has no pit: from every column some feature's cone
descends, so a body walks downhill until it meets the sea or a pad. With every
slope at most one, no two neighbouring open-ground columns differ by more than
one block, and `steep_pairs` is the assertion that the rounding kept it so.

Stdlib only; no randomness.
"""
import math
import struct
import zlib
from pathlib import Path

RANGE = 51  # the site plan's `range`; a height step of one is a value step of 5


class Pad:
    """A flat rectangle x0..x1 × z0..z1 (inclusive) at `top`, falling `slope`
    blocks per column beyond its edge."""

    def __init__(self, x0, z0, x1, z1, top, slope):
        self.x0, self.z0, self.x1, self.z1, self.top, self.slope = x0, z0, x1, z1, top, slope

    def at(self, x, z):
        dx = max(self.x0 - x, 0, x - self.x1)
        dz = max(self.z0 - z, 0, z - self.z1)
        return self.top - self.slope * math.hypot(dx, dz)

    def covers(self, x, z):
        return self.x0 <= x <= self.x1 and self.z0 <= z <= self.z1


class Ramp(Pad):
    """A rectangle whose top falls `grade` blocks per column from `top` at
    `z0` toward `z1` (a sloping street), falling `slope` per column beyond
    its edge like a pad."""

    def __init__(self, x0, z0, x1, z1, top, grade, slope):
        super().__init__(x0, z0, x1, z1, top, slope)
        self.grade = grade

    def at(self, x, z):
        zc = min(max(z, self.z0), self.z1)
        top = self.top - self.grade * (zc - self.z0)
        dx = max(self.x0 - x, 0, x - self.x1)
        dz = max(self.z0 - z, 0, z - self.z1)
        return top - self.slope * math.hypot(dx, dz)


def envelope(nx, nz, features, floor, fixed):
    """`h[x][z]`: the highest feature at each column, floored, then `fixed`
    ({(x, z): height}) written over it. Floats."""
    h = []
    for x in range(nx):
        col = []
        for z in range(nz):
            v = floor
            for f in features:
                fv = f.at(x, z)
                if fv > v:
                    v = fv
            col.append(float(fixed.get((x, z), v)))
        h.append(col)
    return h


def rounded(h):
    # round half up, so a 0.5 slope reads as one step every two columns
    return [[int(math.floor(v + 0.5)) for v in col] for col in h]


def steep_pairs(y, inside):
    """Neighbouring column pairs, both inside `inside(x, z)`, differing by more
    than one block: ((x, z), (x2, z2), dy)."""
    nx, nz = len(y), len(y[0])
    out = []
    for x in range(nx):
        for z in range(nz):
            if not inside(x, z):
                continue
            for dx, dz in ((1, 0), (0, 1)):
                x2, z2 = x + dx, z + dz
                if x2 < nx and z2 < nz and inside(x2, z2):
                    d = y[x2][z2] - y[x][z]
                    if abs(d) > 1:
                        out.append(((x, z), (x2, z2), d))
    return out


def encode(y, base_y):
    """Rows of pixel values (z-major, x along the row) for `write_png`; refuses
    a height the encoding cannot carry."""
    nx, nz = len(y), len(y[0])
    rows = []
    for z in range(nz):
        row = []
        for x in range(nx):
            v = (y[x][z] - base_y) * 5
            if not (0 <= v <= 255) or base_y + v * RANGE // 255 != y[x][z]:
                raise SystemExit(f"height {y[x][z]} at ({x}, {z}) is outside {base_y}..{base_y + 51}")
            row.append(v)
        rows.append(row)
    return rows


def write_png(path, rows):
    nz, nx = len(rows), len(rows[0])
    raw = b"".join(b"\x00" + bytes(r) for r in rows)

    def chunk(kind, data):
        c = kind + data
        return struct.pack(">I", len(data)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", nx, nz, 8, 0, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")
    Path(path).write_bytes(png)
    return png


def ascii_contours(y, sea, every=4, step_x=2, step_z=4):
    """A coarse text picture of the field, one character per `step_x` × `step_z`
    columns: `~` is water (surface under `sea`), digits are bands of `every`
    blocks above it."""
    nx, nz = len(y), len(y[0])
    lines = []
    for z in range(0, nz, step_z):
        s = []
        for x in range(0, nx, step_x):
            v = y[x][z]
            s.append("~" if v < sea else str(((v - sea) // every) % 10))
        lines.append("".join(s))
    return "\n".join(lines)
