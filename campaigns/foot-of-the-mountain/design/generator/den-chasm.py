#!/usr/bin/env python3
"""The chasm under the cat's den: a piece the world edits stamp.

    python3 den-chasm.py --out foot-of-the-mountain-den-chasm.json
    delvec grammar expand --file foot-of-the-mountain-den-chasm.json --region 61x42x79 --out <the content prefabs directory>

writes `prefab/foot-of-the-mountain-den-chasm`: the chasm's rock under the den's floor course
(`den_shape.rock_at`, u -43..-2, the cave's dark rock) with crystals of sea lantern in its walls and
glow lichen round them. No place stands its walk plane under the sea's surface, so the chasm is not
a place: it is air the site plan keeps under the den (`volume/den-chasm`), and this piece is
stamped into it by `batch/the-chasm`, unrotated, its first course at world y 28, its x and z the
den's frame. The stone Cthulhu standing in it is its own piece (`den_thing.py`, `batch/the-thing`).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import den_shape as S  # noqa: E402

D = S.DEPTH
EX, EY, EZ = S.EX, S.DEPTH - 1, S.EZ - 1     # 61 x 42 x 79: the chasm, u -43..-2

PALETTE = {
    # the chasm's rock is the cave's dark rock
    "rock": [{"weight": 3, "block": "minecraft:deepslate[axis=y]"}, {"weight": 2, "block": "minecraft:cobbled_deepslate"},
             {"weight": 2, "block": "minecraft:tuff"}],
    "deep": [{"weight": 3, "block": "minecraft:deepslate[axis=y]"}, {"weight": 2, "block": "minecraft:cobbled_deepslate"},
             {"weight": 1, "block": "minecraft:tuff"}],
    "crystal": "minecraft:sea_lantern",
}


def cells():
    c = {}
    for x in range(EX):
        for z in range(EZ):
            for yb in range(D - 1):          # the chasm's rock, under the den's floor course
                y = yb - D
                if S.rock_at(x, y, z):
                    c[(x, yb, z)] = "deep" if y < -20 else "rock"

    def is_rock(x, yb, z):
        return c.get((x, yb, z)) in ("rock", "deep")
    # crystals in the chasm's walls: cold light on the figure's body from below, glow lichen round each
    crystals = []
    for x in range(1, EX - 1):
        for z in range(1, EZ - 1):
            for yb in range(2, D - 2):
                if not is_rock(x, yb, z) or S.h(x, yb, z, 97) % 17:
                    continue
                if not any(c.get((x + dx, yb + dy, z + dz)) is None and 0 <= x + dx < EX and 0 <= z + dz < EZ
                           for _, dx, dy, dz in S.FACES):
                    continue
                if any(abs(x - a) + abs(yb - b) + abs(z - d) < 7 for a, b, d in crystals):
                    continue
                crystals.append((x, yb, z))
                c[(x, yb, z)] = "crystal"
    for (a, b, d) in crystals:
        for _, dx, dy, dz in S.FACES:
            k = (a + dx, b + dy, d + dz)
            if c.get(k) is not None or not (0 <= k[0] < EX and 0 <= k[2] < EZ and 0 <= k[1] < D - 1):
                continue
            for f, ex_, ey_, ez_ in S.FACES:
                if is_rock(k[0] + ex_, k[1] + ey_, k[2] + ez_):
                    c[k] = S.lichen(f)
                    break
    return c


def leaf(v):
    if v is None:
        return {"op": "void"}
    return {"op": "fill", "material": {"role": v}}


def sz(n):
    return {"size": "absolute", "blocks": {"expr": "int", "value": n}}


def split(axis, runs):
    if len(runs) == 1:
        return runs[0][1]
    return {"op": "split", "axis": axis, "sizes": [sz(n) for n, _ in runs], "children": [ch for _, ch in runs]}


def merge(items):
    out = []
    for it in items:
        k = json.dumps(it, sort_keys=True)
        if out and out[-1][0] == k:
            out[-1][1] += 1
        else:
            out.append([k, 1, it])
    return [(n, it) for _, n, it in out]


def main():
    out = sys.argv[sys.argv.index("--out") + 1]
    c = cells()
    palette = dict(PALETTE)
    for v in sorted({v for v in c.values() if v.startswith("minecraft:")}):
        palette[v] = v
    rows = []
    for z in range(EZ):
        cols = []
        for x in range(EX):
            cols.append(split("y", merge([leaf(c.get((x, y, z))) for y in range(EY)])))
        rows.append(split("x", merge(cols)))
    program = {
        "version": "1.10.0", "name": "foot_of_the_mountain_den_chasm", "start": "place", "params": {}, "palette": palette,
        "rules": {"place": [{"weight": 1, "body": split("z", merge(rows))}]},
    }
    with open(out, "w", encoding="utf-8") as f:
        f.write(json.dumps(program, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    n = sum(1 for v in c.values() if v.startswith("minecraft:glow_lichen"))
    print(f"wrote {out}: {len(c)} block(s), {n} glow lichen")


if __name__ == "__main__":
    main()
