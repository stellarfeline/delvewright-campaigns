#!/usr/bin/env python3
"""Feasibility case A: two houses at different floors joined through a way box
on a slope, on a small island, over the shared heightfield module
(../../hillside/terrain/heightfield.py).

Writes terrain/site.png, 80 x 96, surface `48 + value / 5`. Region min
[0, 40, 0], extent [80, 48, 96]; the land side is north, the sea south.

Features: the high house's pad (x 35..43, z 39..47 at 73), the way box's pad
(x 36..42, z 47..56 at 69; the shared row z 47 takes 73), the low house's pad
(x 35..43, z 56..64 at 69), one hill on the mainland, half a block per column
everywhere beyond.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "hillside" / "terrain"))
import heightfield as hf  # noqa: E402

NX, NZ, BASE_Y, SEA_BED, SEA = 80, 96, 48, 54, 62


def main():
    features = [
        hf.Pad(35, 39, 43, 47, 73, 0.5),   # the high house, footprint and ring
        hf.Pad(36, 47, 42, 56, 69, 0.5),   # the way box, footprint and ring
        hf.Pad(35, 56, 43, 64, 69, 0.5),   # the low house, footprint and ring
        hf.Pad(40, 26, 40, 26, 72, 0.5),   # the mainland's hill
    ]
    fixed = {(x, z): SEA_BED for x in range(NX) for z in range(NZ) if x in (0, NX - 1) or z in (0, NZ - 1)}
    y = hf.rounded(hf.envelope(NX, NZ, features, SEA_BED, fixed))
    pad = {(x, z) for x in range(35, 44) for z in range(39, 65)}
    steep = [s for s in hf.steep_pairs(y, lambda x, z: y[x][z] >= SEA) if s[0] not in pad and s[1] not in pad]
    if steep:
        raise SystemExit(f"{len(steep)} open-ground step(s) over one: {steep[:5]}")
    rows = hf.encode(y, BASE_Y)
    out = Path(__file__).with_name("site.png")
    hf.write_png(out, rows)
    Path(__file__).with_name("site.txt").write_text(hf.ascii_contours(y, SEA, step_x=1, step_z=2) + "\n")
    land = [(x, z) for x in range(NX) for z in range(NZ) if y[x][z] >= SEA]
    print(f"wrote {out} ({NX}x{NZ}); surface y {min(min(c) for c in y)}..{max(max(c) for c in y)}; "
          f"land x {min(x for x, _ in land)}..{max(x for x, _ in land)}, z {min(z for _, z in land)}..{max(z for _, z in land)}; "
          f"way box row z 48: {y[39][48]}, z 55: {y[39][55]}; 0 open-ground steps over one", file=sys.stderr)


if __name__ == "__main__":
    main()
