#!/usr/bin/env python3
"""The chasm under the cat's den and the stone Cthulhu standing in it: a piece the world edits stamp.

    python3 den-chasm.py --out foot-of-the-mountain-den-chasm.json
    delvec grammar expand --file foot-of-the-mountain-den-chasm.json --region 61x85x79 --out <the content prefabs directory>

writes `prefab/foot-of-the-mountain-den-chasm`.

Written cell by cell from `den_shape`, as the den is: the chasm's rock under the den's floor course
(`den_shape.rock_at`, y -43..-1 of the den's frame), the statue whole (`den_shape.statue_parts`:
its body in the chasm, its head and wings over the bridge, in the air the den keeps clear for
them), and glow lichen on the chasm's walls and on the statue's face, beard and claws, each on the
face of a block this piece lays. No place stands its walk plane under the sea's surface, so the
chasm is not a place: it is air the site plan keeps under the den (`volume/den-chasm`), and this
piece is stamped into it by `batch/the-chasm`, unrotated, its first course at world y 28, its x and
z the den's frame. A fragment writes only what is not air, so the den's own cave stands as the den
draws it.

After `design/reference/cat-den`: grey stone, mossy, the head bent forward over the bridge, the
wings spread as wide as the bridge is long, the body falling away into the dark.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import den_shape as S  # noqa: E402

D = S.DEPTH
EX, EY, EZ = S.EX, S.DEPTH + S.LID, S.EZ - 1     # 61 x 85 x 79

PALETTE = {
    "rock": [{"weight": 4, "block": "minecraft:stone"}, {"weight": 2, "block": "minecraft:tuff"},
             {"weight": 1, "block": "minecraft:andesite"}, {"weight": 2, "block": "minecraft:cobbled_deepslate"},
             {"weight": 1, "block": "minecraft:dripstone_block"}],
    "deep": [{"weight": 3, "block": "minecraft:deepslate[axis=y]"}, {"weight": 2, "block": "minecraft:cobbled_deepslate"},
             {"weight": 1, "block": "minecraft:tuff"}],
    # the statue in pale stone, as the reference has it, set off from the cave's dark rock: calcite,
    # diorite and smooth stone, with moss in its folds
    "body": [{"weight": 3, "block": "minecraft:diorite"}, {"weight": 3, "block": "minecraft:calcite"},
             {"weight": 2, "block": "minecraft:smooth_stone"}, {"weight": 1, "block": "minecraft:moss_block"}],
    "head": [{"weight": 4, "block": "minecraft:calcite"}, {"weight": 3, "block": "minecraft:polished_diorite"},
             {"weight": 2, "block": "minecraft:smooth_stone"}, {"weight": 1, "block": "minecraft:mossy_stone_bricks"}],
    "feeler": [{"weight": 3, "block": "minecraft:polished_diorite"}, {"weight": 2, "block": "minecraft:calcite"},
               {"weight": 1, "block": "minecraft:moss_block"}, {"weight": 1, "block": "minecraft:mossy_stone_bricks"}],
    "bone": [{"weight": 3, "block": "minecraft:smooth_stone"}, {"weight": 2, "block": "minecraft:calcite"}],
    "eye": "minecraft:sea_lantern",
    "membrane": [{"weight": 3, "block": "minecraft:diorite"}, {"weight": 2, "block": "minecraft:calcite"},
                 {"weight": 1, "block": "minecraft:andesite"}],
}
KIND_ORDER = ("feeler", "head", "bone", "body", "membrane")


def statue_kind(x, y, z):
    """The statue's material at a cell of the den's frame, or None; the eyes are cut dark."""
    p = (x + 0.5, y + 0.5, z + 0.5)
    for dz in (-4.0, 4.0):
        if S._ell(p[0], p[1], p[2], (22.0, 21.0, S.STATUE_Z + dz), (2.5, 1.6, 2.0)) <= 1.0:
            return "eye" if p[0] < 20.5 else None
    hit = set()
    for kind, prim in S.statue_parts():
        if prim[0] == "capsule":
            _, a, b, ra, rb = prim
            d, t = S._seg_dist(p, a, b)
            if d <= ra + (rb - ra) * t:
                hit.add(kind)
        elif prim[0] == "ellipsoid":
            _, c, r = prim
            if S._ell(p[0], p[1], p[2], c, r) <= 1.0:
                hit.add(kind)
    for (a, b) in S.membrane_boxes():
        if a[0] <= p[0] <= b[0] and a[1] <= p[1] <= b[1] and a[2] <= p[2] <= b[2]:
            hit.add("membrane")
    for k in KIND_ORDER:
        if k in hit:
            return k
    return None


def cells():
    c = {}
    for x in range(EX):
        for z in range(EZ):
            for yb in range(EY):
                y = yb - D
                k = None
                if x <= 33 and 8 <= z <= 78:
                    k = statue_kind(x, y, z)
                if k is not None:
                    c[(x, yb, z)] = k
                elif y < -1 and S.rock_at(x, y, z):
                    c[(x, yb, z)] = "deep" if y < -20 else "rock"
    # glow lichen: in clusters on the chasm's walls, and on the statue's face, beard and claws
    def solid(x, y, z):
        return c.get((x, y + D, z)) is not None
    def open_rock(x, y, z):
        return y < -1 and c.get((x, y + D, z)) is None and 0 <= x < EX and 0 <= z < EZ
    lich = S.lichen_cells(-D + 1, -2, solid, open_rock, salt=53)
    for (x, y, z), st in lich.items():
        c[(x, y + D, z)] = st
    Z = S.STATUE_Z
    for x in range(9, 28):
        for y in range(-16, 30):
            for z in range(Z - 31, Z + 32):
                yb = y + D
                if c.get((x, yb, z)) is not None or c.get((x - 1, yb, z)) not in ("head", "feeler", "body", "bone", "membrane"):
                    continue
                if S.h(x, y, z, 71) % 2 or S.noise(x, y, z, 3.0, 73) < 0.45:
                    continue
                c[(x, yb, z)] = S.lichen("west")
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
