#!/usr/bin/env python3
"""The way to the cat's den: the shaft under the apothecary, the long tunnel, and the chasm.

    DELVEWRIGHT_SKILL=<skill> python3 den.py --allocation <delvec allocation . node/<place>> \\
        --out ../../programs/<place>.json --delvec <delvec>

One generator, dispatched on the place's stem, drawn into the skill's starter, after the approved
reference `design/reference/cat-den` and the owner's section sketch (a ladder down in the corner
of a town house, a long level tunnel to the foot of the mountain, opening all at once onto the
bridge and the statue):

- node/den-shaft: rock under the apothecary's lot, a ladder down from the trapdoor in the still
  room's corner, a short passage from its foot to the tunnel;
- node/den-tunnel: a long, level, narrow tunnel of rough rock, timbered every few steps like an
  old mine (the node's `references[]`), lanterns hung under its roof;
- node/cat-den: the cave under the mountain, a natural irregular hollow (the 1.18+ noise caves,
  the node's `references[]`): the tunnel's mouth on a ledge, a long bridge of planks, fence rails
  and chains on posts with lanterns across the chasm, and on the far ledge the cat's den, a red
  bed and a hoard of rare keepsakes. The stone Cthulhu that stands in the chasm behind the bridge
  and the chasm under it are not drawn here: they are the piece
  `prefab/foot-of-the-mountain-den-chasm` (`den-chasm.py`), stamped in by the world edits
  (`batch/the-chasm`) into the air the den leaves for it and the volume under the den.

Piece-local axes: +x east, +z south; y 0 the ground course, y 1 the walk plane.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
from starter import AIR, Model, run  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import den_shape as S  # noqa: E402

ROCKS = ["minecraft:stone", "minecraft:stone", "minecraft:tuff", "minecraft:andesite",
         "minecraft:deepslate[axis=y]", "minecraft:cobbled_deepslate"]
LANTERN = "minecraft:lantern[hanging=false,waterlogged=false]"
HANGING = "minecraft:lantern[hanging=true,waterlogged=false]"
CHAIN_Y = "minecraft:chain[axis=y,waterlogged=false]"
CHAIN_Z = "minecraft:chain[axis=z,waterlogged=false]"
FENCE = "minecraft:oak_fence"          # arms derived by `Model.finish`
POST = "minecraft:spruce_fence"
LOG_Y = "minecraft:stripped_spruce_log[axis=y]"
LOG_X = "minecraft:stripped_spruce_log[axis=x]"


def h(*a):
    v = 2166136261
    for n in a:
        v = ((v ^ (n & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    return v


def rock(x, y, z):
    return ROCKS[h(x, y, z, 7) % len(ROCKS)]


def den_shaft(m, place):
    """Rock under the lot; the ladder down from the hatch (the climb seam's cell over it), a
    passage three wide from its foot to the tunnel's mouth in the north face."""
    ex, ey, ez = m.ex, m.ey, m.ez
    up = next(s for s in place.seams if s["stem"] == "apothecary-to-den-shaft")
    lx, ly, lz = [b.value for b in up["lo"]]
    tun = next(s for s in place.seams if s["stem"] == "den-shaft-to-den-tunnel")
    tx0, tx1 = tun["lo"][0].value, tun["hi"][0].value - 1
    # the drawing climbs to the hatch itself: one ladder from the passage's floor up through the
    # opening's own cell, hung on the rock to its west, under the apothecary's top rung
    m.climbs_to("edge/apothecary-to-den-shaft")
    well = {(lx, lz)}
    for x in range(ex):
        for y in range(0, ey):
            for z in range(1, ez):
                if (x, z) in well and y >= 1:
                    continue
                m.set(x, y, z, rock(x, y, z))
    passage = {(x, z) for x in range(tx0, tx1 + 1) for z in range(1, lz + 1)} | \
        {(x, z) for x in range(lx + 1, tx1 + 1) for z in (lz - 1, lz)}
    for (x, z) in sorted(passage):
        for y in (1, 2, 3):
            if (x, z) not in well:
                m.set(x, y, z, AIR)
        m.set(x, 0, z, "minecraft:gravel" if h(x, z) % 3 == 0 else "minecraft:stone")
    for y in range(1, ly + 1):
        m.set(lx, y, lz, "minecraft:ladder[facing=east,waterlogged=false]")
    m.set(tx1, 3, lz - 2, HANGING)
    m.set(tx1, 3, 2, HANGING)
    m.mark("shaft-foot", tx0, lz - 1, facing="north")
    m.mark("node-den-shaft", tx0 + 1, 4, facing="north")


def den_tunnel(m, place):
    """Rough rock walls, a floor of stone and gravel, a frame of stripped spruce every six steps
    with a lantern hung beside it."""
    ex, ey, ez = m.ex, m.ey, m.ez
    for z in range(ez):
        for y in range(ey):
            for x in (0, ex - 1):
                m.set(x, y, z, rock(x, y, z))
        for x in range(1, ex - 1):
            m.set(x, 0, z, "minecraft:gravel" if h(x, z, 3) % 4 == 0 else ("minecraft:coarse_dirt" if h(x, z, 4) % 5 == 0 else "minecraft:stone"))
            m.set(x, ey - 1, z, rock(x, ey - 1, z))
    for z in range(4, ez - 3, 6):
        for y in (1, 2):
            m.set(0, y, z, LOG_Y)
            m.set(ex - 1, y, z, LOG_Y)
        for x in range(0, ex):
            m.set(x, 3, z, LOG_X)
        if (z // 6) % 2 == 0:
            m.set(1 if (z // 12) % 2 else ex - 2, 3, z + 3, HANGING)
    m.mark("node-den-tunnel", 2, ez // 2, facing="north")


def cat_den(m, place):
    """The cave: rock where `den_shape` says rock, the ledges and the bridge, the den."""
    ex, ey, ez = m.ex, m.ey, m.ez
    cells = S.den_cells(ex, ey, ez)
    for (x, y, z), b in cells.items():
        m.set(x, y, z, b)
    for k, (x, z, facing, y) in S.den_marks().items():
        m.mark(k, x, z, facing=facing, y=y)
    m.show("down")   # the chasm under the bridge is seen through the den's open floor


def build(place):
    m = Model(place)
    stem = place.a["place"].removeprefix("node/")
    {"den-shaft": den_shaft, "den-tunnel": den_tunnel, "cat-den": cat_den}[stem](m, place)
    m.finish()
    return m


# Thin blocks hung in a cave's own air where no body stands (lanterns on chains, glow lichen,
# dripstone, chains) are the room's air with something in it; the starter writes such a block
# unclaimed where no body reaches it, which an enclosed room's closure reads as open air on its
# boundary. They are claimed the room's.
THIN = ("minecraft:glow_lichen", "minecraft:pointed_dripstone", "minecraft:iron_chain", "minecraft:lantern",
        "minecraft:hanging_roots", "minecraft:cave_vines", "minecraft:potted_", "minecraft:spruce_wall_sign",
        "minecraft:amethyst_cluster", "minecraft:skeleton_skull", "minecraft:dragon_wall_head", "minecraft:end_rod",
        "minecraft:red_bed", "minecraft:red_carpet")


def claim_thin(out):
    with open(out, encoding="utf-8") as f:
        doc = json.load(f)
    roles = {k for k, v in doc["palette"].items() if isinstance(v, str) and v.split("[")[0].startswith(THIN)}
    n = [0]

    def walk(o, claimed):
        if isinstance(o, dict):
            if o.get("op") == "fill" and not claimed and o.get("material", {}).get("role") in roles:
                n[0] += 1
                return {"op": "claim", "region": "room", "body": o}
            return {k: walk(v, claimed or o.get("op") == "claim") for k, v in o.items()}
        if isinstance(o, list):
            return [walk(v, claimed) for v in o]
        return o
    doc["rules"] = walk(doc["rules"], False)
    with open(out, "w", encoding="utf-8") as f:
        f.write(json.dumps(doc, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    print(f"{os.path.basename(out)}: {n[0]} thin leaf(s) claimed the room's, over {len(roles)} state(s)")


if __name__ == "__main__":
    rc = run(build, reason="the chasm's rock, the bridge's posts and the den's shelves: seen, never stood on")
    if rc == 0:
        claim_thin(sys.argv[sys.argv.index("--out") + 1])
    raise SystemExit(rc)
