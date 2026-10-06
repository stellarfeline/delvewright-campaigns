#!/usr/bin/env python3
"""Draw the textures The Painted Night replaces, from nothing.

    python3 demos/the-painted-night/draw-textures.py

writes

    campaigns/the-painted-night/textures/red-moon.png           32x32
    campaigns/the-painted-night/textures/shore-walker.png       64x64
    campaigns/the-painted-night/textures/shore-walker-garb.png  64x64

All three are original work, made by this script and licensed with the
campaign: no vanilla pixel is read, copied or traced.

- `red-moon` is a plain red disc on a transparent ground, the size of the
  full-moon texture it replaces.
- `shore-walker` is the drowned's skin (`entity/zombie/drowned`): a deep-sea
  fish-folk. Dusk-blue scales over a pale belly, two round glowing eyes and a
  wide toothed mouth, gill slits behind the jaw, a coral dorsal fin running from
  the crown down the spine, coral fins on the outer forearms and calves, webbed
  clawed hands and feet, and a lateral line of glowing spots along each flank.
- `shore-walker-garb` is what it wears (`entity/zombie/drowned_outer_layer`,
  drawn over the skin on a slightly larger copy of the same model): a fishing
  net thrown over the shoulders, a rope belt, a skirt of kelp strands that runs
  on down the thighs, shell-and-coral bracelets, ankle cords, and barnacles and
  a trailing strand of kelp on the head. Everything else on that sheet is
  transparent, so the face and the fins show through; the net parts around the
  dorsal fin on the back.

Both drowned sheets follow the zombie-model box layout the drowned is drawn
with (a box of width w, height h and depth d at (u, v) unwraps to top and
bottom across the first d rows, then right side, front, left side and back
across the next h rows): head 8x8x8 at (0, 0), body 8x12x4 at (16, 16), right
arm 4x12x4 at (40, 16), right leg 4x12x4 at (0, 16), left arm at (32, 48) and
left leg at (16, 48). Every face of every box is painted; cells of the sheet no
box reads stay transparent. Variation inside a face comes from an integer hash
of the cell, never from a random generator.

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

Colour = tuple[int, int, int, int]
CLEAR: Colour = (0, 0, 0, 0)


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


def red_moon(x: int, y: int) -> Colour:
    # A disc of radius 11 centred in the 32x32 cell; everything else transparent.
    dx, dy = x - 15.5, y - 15.5
    if dx * dx + dy * dy <= 11.0 * 11.0:
        return (210, 28, 28, 255)
    return CLEAR


# --- the drowned -------------------------------------------------------------


def hash3(x: int, y: int, salt: int) -> int:
    """A fixed integer hash of a cell, 0..65535 — the only source of variation."""
    n = (x * 374761393 + y * 668265263 + salt * 1442695041) & 0xFFFFFFFF
    n = ((n ^ (n >> 13)) * 1274126177) & 0xFFFFFFFF
    return (n ^ (n >> 16)) & 0xFFFF


def rgb(r: int, g: int, b: int) -> Colour:
    return (r, g, b, 255)


# Skin
SKIN_DEEP = rgb(38, 44, 82)
SKIN_DARK = rgb(52, 60, 104)
SKIN = rgb(70, 82, 134)
SKIN_LIGHT = rgb(96, 110, 164)
BELLY = rgb(150, 162, 198)
BELLY_SHADE = rgb(124, 136, 180)
GLOW = rgb(120, 236, 214)
EYE = rgb(222, 240, 150)
EYE_RIM = rgb(150, 170, 80)
PUPIL = rgb(14, 12, 28)
MOUTH = rgb(22, 12, 30)
TOOTH = rgb(236, 230, 212)
GILL = rgb(26, 18, 44)
GILL_RED = rgb(186, 72, 96)
FIN = rgb(196, 92, 112)
FIN_RAY = rgb(150, 58, 86)
CLAW = rgb(222, 214, 186)
# Garb
ROPE = rgb(182, 160, 112)
KNOT = rgb(128, 104, 68)
KELP = (rgb(30, 76, 52), rgb(48, 112, 72), rgb(84, 148, 86))
SHELL = rgb(232, 220, 190)
CORAL = rgb(208, 98, 112)
BARNACLE = rgb(214, 206, 180)
BARNACLE_HOLE = rgb(72, 64, 58)

SIDES = ("front", "right", "left", "back")


def scales(x: int, y: int, base: Colour = SKIN, light: Colour = SKIN_LIGHT, dark: Colour = SKIN_DARK) -> Colour:
    """Offset rows of one-pixel scales: a lit top, a shaded underside."""
    if (x + y // 2) % 2 == 0:
        return light if y % 2 == 0 else dark
    return base


def box(u: int, v: int, w: int, h: int, d: int) -> dict[str, tuple[int, int, int, int]]:
    """The six faces of a box on the model sheet, as (x0, y0, width, height)."""
    return {
        "top": (u + d, v, w, d),
        "bottom": (u + d + w, v, w, d),
        "right": (u, v + d, d, h),
        "front": (u + d, v + d, w, h),
        "left": (u + d + w, v + d, d, h),
        "back": (u + 2 * d + w, v + d, w, h),
    }


def from_front(face: str, x: int, d: int) -> int:
    """A side face's column counted from its front edge: the entity's right side
    unwraps back-to-front, its left side front-to-back."""
    return (d - 1) - x if face == "right" else x


def head_skin(face: str, x: int, y: int) -> Colour:
    if face == "front":
        if y in (2, 3) and x in (1, 2, 5, 6):
            pupil_x = 2 if x < 4 else 5
            return PUPIL if (y == 3 and x == pupil_x) else EYE
        if y == 1 and x in (1, 2, 5, 6):
            return SKIN_DEEP  # a heavy brow over each eye
        if y == 4 and x in (3, 4):
            return SKIN_DEEP  # nostril pits
        if y == 5:
            return TOOTH if x in (1, 3, 4, 6) else MOUTH
        if y == 6:
            if x in (0, 7):
                return SKIN_DARK
            return TOOTH if x in (2, 5) else MOUTH
        if y == 7:
            return BELLY
        if y == 0 and x in (3, 4):
            return FIN  # the crest's leading edge
        return scales(x, y)
    if face in ("right", "left"):
        f = from_front(face, x, 8)
        if f == 0 and y in (2, 3):
            return EYE_RIM  # the eye bulges round the corner
        if f == 0 and y in (5, 6):
            return MOUTH  # the mouth runs round to the jaw hinge
        if f in (3, 5) and y in (3, 4, 5):
            return GILL
        if f == 4 and y == 4:
            return GILL_RED
        if y == 7:
            return BELLY_SHADE
        if (f, y) in ((6, 2), (2, 1), (7, 4)):
            return GLOW
        return scales(x, y)
    if face == "top":  # rows run back (0) to front (7)
        if x in (3, 4):
            return FIN_RAY if y % 2 == 0 else FIN
        if (x, y) in ((1, 2), (6, 5), (2, 6)):
            return GLOW
        return scales(x, y)
    if face == "back":
        if x in (3, 4):
            return FIN_RAY if y % 2 == 0 else FIN
        if y == 7:
            return SKIN_DARK
        return scales(x, y)
    # bottom: the throat
    return BELLY_SHADE if (x + y) % 3 == 0 else BELLY


def body_skin(face: str, x: int, y: int) -> Colour:
    if face == "front":
        if 2 <= x <= 5:
            return BELLY_SHADE if y % 2 == 1 else BELLY  # ventral plates
        if x in (0, 7) and y in (2, 5, 8, 11):
            return GLOW
        return scales(x, y)
    if face == "back":
        if x in (3, 4):
            return FIN_RAY if y % 2 == 0 else FIN
        return scales(x, y)
    if face in ("right", "left"):
        f = from_front(face, x, 4)
        if f == 1 and y in (2, 5, 8, 11):
            return GLOW  # the lateral line
        if f == 0:
            return scales(x, y, SKIN, BELLY_SHADE, SKIN)
        return scales(x, y)
    if face == "top":
        if x in (3, 4) and y == 0:
            return FIN
        return scales(x, y)
    return SKIN_DARK


def limb_skin(face: str, x: int, y: int, outer: str, extremity_rows: int, fin_rows: range) -> Colour:
    """An arm or a leg: scales, a coral fin on the outer side, webbed claws at the end."""
    if face == "top":
        return scales(x, y)
    if face == "bottom":  # palm or sole, claws at the corners
        if x in (0, 3) and y in (0, 3):
            return CLAW
        return SKIN_DEEP if extremity_rows == 2 else BELLY_SHADE
    if y >= 12 - extremity_rows:
        if y == 11 and x % (2 if face == "front" else 3) == 0:
            return CLAW
        return SKIN_DEEP if x % 2 == 0 else SKIN_DARK  # fingers or toes and the web between
    if face == outer and from_front(face, x, 4) >= 2 and y in fin_rows:
        return FIN_RAY if y % 2 == 0 else FIN
    if face in ("right", "left") and face != outer:
        return scales(x, y, SKIN, BELLY_SHADE, SKIN_DARK)  # the paler inner side
    return scales(x, y)


def net(x: int, y: int) -> Colour | None:
    """A diamond-mesh net: rope on the diagonals, a knot where two cross."""
    a, b = (x + y) % 4 == 0, (x - y) % 4 == 0
    if a and b:
        return KNOT
    if a or b:
        return ROPE
    return None


def kelp_strand(x: int, y: int, top: int, salt: int, longest: int) -> Colour | None:
    """A ragged strand per column hanging from row `top`; its length comes from the hash."""
    length = 1 + hash3(x, 0, salt) % longest
    if hash3(x, 1, salt) % 5 == 0:
        length = 0  # a gap between strands
    if top <= y < top + length:
        return KELP[(x + hash3(x, y, salt + 7)) % 3]
    return None


def head_garb(face: str, x: int, y: int) -> Colour | None:
    if face == "top":
        if (x, y) in ((1, 1), (2, 1), (1, 2), (6, 5), (5, 6)):
            return BARNACLE_HOLE if (x, y) in ((1, 1), (6, 5)) else BARNACLE
        if x == 6 and y <= 3:
            return KELP[y % 3]  # a strand of kelp caught on the crown, trailing back
        return None
    if face == "back":  # the kelp from the crown falls down the back of the head
        if x == 1 and y <= 6:
            return KELP[(y + 1) % 3]
        if x == 2 and 2 <= y <= 4:
            return KELP[0]
        if (x, y) in ((6, 3), (5, 4)):
            return BARNACLE
        return None
    if face in ("right", "left"):
        f = from_front(face, x, 8)
        if face == "right" and f == 7 and y <= 5:
            return KELP[y % 3]
        if face == "left" and (f, y) in ((5, 1), (6, 1), (6, 2)):
            return BARNACLE_HOLE if (f, y) == (6, 1) else BARNACLE
        return None
    return None  # the face and the throat stay bare


def body_garb(face: str, x: int, y: int) -> Colour | None:
    if face == "bottom":
        return None
    if face == "top":
        if x in (3, 4) and y == 0:
            return None  # the net parts round the dorsal fin
        return net(x, y)
    if face == "back" and x in (3, 4) and y <= 6:
        return None
    if y <= 3:
        return net(x, y)
    if y == 4:
        return ROPE if x % 2 == 0 else None  # the net's ragged hem
    if y == 9:
        return KNOT if x % 4 == 1 else ROPE  # a rope belt
    if y >= 10:
        return kelp_strand(x + 16 * SIDES.index(face), y, 10, 31, 2)
    return None


def arm_garb(face: str, x: int, y: int) -> Colour | None:
    if face == "bottom":
        return None
    if face == "top" or y <= 2:
        return net(x, y)
    if y == 5:
        return ROPE
    if y == 6:
        return SHELL if x % 2 == 0 else CORAL  # a shell-and-coral bracelet on the forearm
    return None


def leg_garb(face: str, x: int, y: int) -> Colour | None:
    if face in ("top", "bottom"):
        return None
    if y <= 3:
        return kelp_strand(x + 8 * SIDES.index(face), y, 0, 53, 4)
    if y == 9:
        return KNOT if x % 2 == 0 else ROPE  # an ankle cord
    return None


HEAD = (0, 0, 8, 8, 8)
BODY = (16, 16, 8, 12, 4)
RIGHT_ARM = (40, 16, 4, 12, 4)
RIGHT_LEG = (0, 16, 4, 12, 4)
LEFT_ARM = (32, 48, 4, 12, 4)
LEFT_LEG = (16, 48, 4, 12, 4)

ARM_FIN = range(2, 8)
LEG_FIN = range(4, 9)

SKIN_PARTS = (
    (HEAD, head_skin),
    (BODY, body_skin),
    (RIGHT_ARM, lambda f, x, y: limb_skin(f, x, y, "right", 3, ARM_FIN)),
    (LEFT_ARM, lambda f, x, y: limb_skin(f, x, y, "left", 3, ARM_FIN)),
    (RIGHT_LEG, lambda f, x, y: limb_skin(f, x, y, "right", 2, LEG_FIN)),
    (LEFT_LEG, lambda f, x, y: limb_skin(f, x, y, "left", 2, LEG_FIN)),
)

GARB_PARTS = (
    (HEAD, head_garb),
    (BODY, body_garb),
    (RIGHT_ARM, arm_garb),
    (LEFT_ARM, arm_garb),
    (RIGHT_LEG, leg_garb),
    (LEFT_LEG, leg_garb),
)


def sheet(parts):
    """A pixel function over the 64x64 sheet: each cell a box face reads is
    painted by that box's painter in face-local coordinates; the rest is clear."""

    def pixel(x: int, y: int) -> Colour:
        for (u, v, w, h, d), paint in parts:
            for face, (x0, y0, fw, fh) in box(u, v, w, h, d).items():
                if x0 <= x < x0 + fw and y0 <= y < y0 + fh:
                    c = paint(face, x - x0, y - y0)
                    return CLEAR if c is None else c
        return CLEAR

    return pixel


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, w, h, fn in (
        ("red-moon", 32, 32, red_moon),
        ("shore-walker", 64, 64, sheet(SKIN_PARTS)),
        ("shore-walker-garb", 64, 64, sheet(GARB_PARTS)),
    ):
        path = OUT / f"{name}.png"
        path.write_bytes(png(w, h, fn))
        print(f"wrote {path.relative_to(HERE.parents[1])} ({w}x{h}, {path.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
