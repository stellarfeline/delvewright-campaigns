#!/usr/bin/env python3
"""Feasibility case B: one sloping street box on a small island, over the
shared heightfield module (../../hillside/terrain/heightfield.py).

Writes terrain/site.png, 80 x 96, surface `48 + value / 5`. Region min
[0, 40, 0], extent [80, 48, 96]; the land side is north, the sea south.

Features: the street in three terraces (x 31..48: z 43..49 at 73, z 50..56
at 71, z 57..64 at 69 — the seam row z 64 is the sill minus one), the
landing's pad (x 31..48, z 64..73 at 65; the shared row z 64 takes 69), one
hill on the mainland, half a block per column everywhere beyond. A terrace is
flat because a piece's space is one floor (`contract-well-formed`): the street
piece draws each terrace as a space and the step between two as a `stair`
edge, and the ring's ground follows the same terraces.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "hillside" / "terrain"))
import heightfield as hf  # noqa: E402

NX, NZ, BASE_Y, SEA_BED, SEA = 80, 96, 48, 54, 62


def main():
    features = [
        hf.Pad(31, 43, 48, 49, 73, 0.5),           # the street's upper terrace, ring row z 43 included
        hf.Pad(31, 50, 48, 56, 71, 0.5),           # its middle terrace
        hf.Pad(31, 57, 48, 64, 69, 0.5),           # its lower terrace, the seam row z 64 included
        hf.Pad(31, 64, 48, 73, 65, 0.5),           # the landing, footprint and ring
        hf.Pad(40, 34, 40, 34, 74, 0.5),           # the mainland's hill
    ]
    fixed = {(x, z): SEA_BED for x in range(NX) for z in range(NZ) if x in (0, NX - 1) or z in (0, NZ - 1)}
    # The terraces are flat to their rings: a higher pad's cone would otherwise
    # lift the first column of the next terrace by one.
    for (z0, z1, top) in ((43, 49, 73), (50, 56, 71), (57, 64, 69)):
        for x in range(31, 49):
            for z in range(z0, z1 + 1):
                fixed[(x, z)] = top
    y = hf.rounded(hf.envelope(NX, NZ, features, SEA_BED, fixed))
    pad = {(x, z) for x in range(31, 49) for z in range(43, 74)}
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
          f"street ring z 43: {y[31][43]}, z 50: {y[31][50]}, z 57: {y[31][57]}, seam row z 64: {y[31][64]}; "
          f"landing z 65: {y[40][65]}; 0 open-ground steps over one", file=sys.stderr)


if __name__ == "__main__":
    main()
