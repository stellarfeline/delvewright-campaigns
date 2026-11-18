#!/usr/bin/env python3
"""The cat's places on the island's flank: the path under the hill, the track up the seaward flank,
and Pip's lush cave in it.

    DELVEWRIGHT_SKILL=<skill> python3 cat_places.py --allocation <delvec allocation . node/<place>> \\
        --out ../../programs/<place>.json --delvec <delvec>

One generator, dispatched on the place's stem, drawn into the skill's starter. The lush cave is
built to the approved reference `design/reference/lush-cave` and after the vanilla lush cave (the
node's `references[]`): small, closed overhead, a natural hollow of stone, tuff and moss; a lower
pond sunk in a clay rim with big dripleaf standing in its water and small dripleaf on the rim,
where Pip sits; mossy steps up the back to a ledge holding an upper pond; azalea on the banks,
cave vines with glow berries, spore blossoms and hanging roots from the roof. Piece-local axes:
+x east, +z south; y 0 the ground course, y 1 the walk plane at the mouth.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
from starter import Model, fence, lantern, run  # noqa: E402

GRASS = "minecraft:grass_block[snowy=false]"
WATER = "minecraft:water[level=0]"
MOSS = "minecraft:moss_block"
CARPET = "minecraft:moss_carpet"
CLAY = "minecraft:clay"
ROOTED = "minecraft:rooted_dirt"
VINE = "minecraft:cave_vines_plant[berries=true]"
VINE_BARE = "minecraft:cave_vines_plant[berries=false]"
VINE_END = "minecraft:cave_vines[age=25,berries=true]"
ROCKS = ["minecraft:stone", "minecraft:stone", "minecraft:tuff", "minecraft:andesite", "minecraft:deepslate[axis=y]"]


def h(*a):
    v = 2166136261
    for n in a:
        v = ((v ^ (n & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    return v


def rock(x, y, z):
    return ROCKS[h(x, y, z, 7) % len(ROCKS)]


def lamp_post(m, x, z, d):
    m.set(x, d, z, fence("spruce"))
    m.set(x, d + 1, z, fence("spruce"))
    m.set(x, d + 2, z, lantern())


def cave_path(m, place):
    """The path under the hill: from the cathedral garden all the way along the foot of the hill to
    the island's seaward flank, gravel and worn turf, the hill's mossy rock face on its north side,
    lamps on the south side."""
    lo, hi = place.space
    X0, X1, Z0, Z1 = lo[0], hi[0], lo[2], hi[2]
    d = place.datum.value
    for x in range(X0, X1 + 1):
        for z in range(Z0, Z1 + 1):
            m.set(x, d - 1, z, GRASS)
        for z in range(Z0 + 1, Z1):
            if h(x, z, 3) % 5:
                m.set(x, d - 1, z, "minecraft:coarse_dirt" if h(x, z) % 3 else "minecraft:gravel")
    # ferns at the foot of the rock face
    for x in range(X0, X1 + 1):
        if h(x, 9) % 4 == 0:
            m.set(x, d, Z0, "minecraft:fern")
    for x in range(X0 + 4, X1 - 6, 10):
        lamp_post(m, x, Z1, d)
    m.mark("node-cave-path", 10, (Z0 + Z1) // 2, facing="east")
    m.show("up")   # the rock face's top shows where the hill behind it is low


def cave_track(m, place):
    """The track up the seaward flank: north from the end of the path under the hill, cut into the
    hill where it climbs, its west wall the cutting's rock face with the cave's mouth low in it,
    hung with moss and vines."""
    lo, hi = place.space
    X0, X1, Z0, Z1 = lo[0], hi[0], lo[2], hi[2]
    d = place.datum.value
    for x in range(X0, X1 + 1):
        for z in range(Z0, Z1 + 1):
            m.set(x, d - 1, z, "minecraft:gravel" if h(x, z, 4) % 3 == 0 else ("minecraft:coarse_dirt" if h(x, z, 5) % 2 else GRASS))
    mouth = [s for s in place.seams if s["stem"] == "cave-track-to-lush-cave"][0]
    mz0, mz1 = mouth["lo"][2].value, mouth["hi"][2].value - 1
    # moss on the ground before the mouth, ferns and a few moss carpets along the cutting's foot
    for z in range(mz0 - 1, mz1 + 2):
        m.set(X0, d - 1, z, MOSS)
        m.set(X0 + 1, d - 1, z, MOSS)
    for z in range(Z0, Z1 + 1):
        if not mz0 - 2 <= z <= mz1 + 2 and h(z, 21) % 3 == 0:
            m.set(X0, d - 1, z, MOSS)
            m.set(X0, d, z, "minecraft:fern" if h(z, 22) % 2 else CARPET)
    for z in range(Z0 + 8, Z1 - 4, 12):
        lamp_post(m, X1, z, d)
    m.mark("cave-mouth", X0 + 2, (mz0 + mz1) // 2, facing="west")
    m.mark("node-cave-track", X0 + 2, Z1 - 6, facing="north")
    m.show("up")


def lush_cave(m, place):
    """Pip's lush cave, after `design/reference/lush-cave`. The mouth is in the east wall (x 20);
    from it the floor steps up once onto the cave's floor round the lower pond, and the mossy steps
    at the back climb to the ledge with the upper pond."""
    lo, hi = place.space
    X0, X1, Z0, Z1 = lo[0], hi[0], lo[2], hi[2]   # 0..19, 0..11
    top = hi[1]                                    # the play space's top course (8); the lid is 9
    LID = top + 1
    W = {}                                         # (x, z) -> walk plane, the ground's top course + 1

    # the ground: by zones, from the mouth inward
    def walk(x, z):
        if x >= 17:
            return 1                               # the landing inside the mouth
        if x <= 6:
            return 6                               # the ledge at the back
        if 7 <= x <= 9 and 4 <= z <= 7:
            return {9: 3, 8: 4, 7: 5}[x]           # the mossy steps, two wide
        if (z <= 1 or z >= 10) and 10 <= x <= 15:
            return 3                               # the mossy banks either side of the pond
        if 7 <= x <= 9:
            return 4 if (z <= 2 or z >= 9) else 3  # the shoulders of the steps
        return 2                                   # the cave floor round the lower pond
    for x in range(X0, X1 + 1):
        for z in range(Z0, Z1 + 1):
            W[(x, z)] = walk(x, z)
    POND = {(x, z) for x in range(11, 16) for z in range(3, 9)} - {(11, 3), (15, 3), (11, 8), (15, 8), (12, 8)}
    UPPER = {(x, z) for x in range(1, 5) for z in range(3, 8)} - {(1, 3), (1, 7), (4, 7)}

    for (x, z), w in W.items():
        for y in range(0, w):
            if y == w - 1:
                b = MOSS
                if (x, z) in POND or (x, z) in UPPER:
                    b = None
                elif any((x + dx, z + dz) in POND | UPPER for dx in (-1, 0, 1) for dz in (-1, 0, 1)):
                    b = CLAY                       # the ponds' rims
                elif h(x, z, 31) % 7 == 0:
                    b = ROOTED
            else:
                b = ROOTED if h(x, y, z, 2) % 4 == 0 else ("minecraft:dirt" if y > 0 else rock(x, y, z))
            if b:
                m.set(x, y, z, b)
    # the ponds: a clay bed, still water a course under the rim
    for (x, z) in POND:
        m.set(x, 0, z, CLAY)
        m.set(x, 1, z, WATER)
    for (x, z) in UPPER:
        m.set(x, 4, z, CLAY)
        m.set(x, 5, z, WATER)
    # the walls and the roof: rock all round the play space, the roof coming down a course at the
    # edges and in knuckles over the floor, rooted dirt in the roof over the ponds
    for x in range(X0, X1 + 1):
        for z in range(Z0, Z1 + 1):
            edge = x == X0 or z in (Z0, Z1)
            if edge:
                for y in range(W[(x, z)], LID):
                    m.set(x, y, z, MOSS if h(x, y, z, 5) % 4 == 0 else rock(x, y, z))
            m.set(x, LID, z, ROOTED if (abs(x - 13) <= 3 and 2 <= z <= 9 and h(x, z, 8) % 3) else rock(x, LID, z))
            near = x in (X0 + 1,) or z in (Z0 + 1, Z1 - 1)
            if near and h(x, z, 6) % 3 == 0 and x < 17:
                m.set(x, top, z, MOSS if h(x, z, 9) % 2 else rock(x, top, z))
    # the mouth's frame: rock either side of the opening's three cells, so the landing is a passage
    for z in (Z0 + 1, Z0 + 2, Z1 - 1, Z1 - 2, Z1 - 3):
        for y in range(1, top + 1):
            if not (3 <= z <= 7):
                m.set(X1, y, z, rock(X1, y, z))
    # dressing: big dripleaf standing in the lower pond, small dripleaf on its rim
    for (x, z, f, n) in ((12, 4, "east", 2), (14, 6, "west", 3), (13, 7, "north", 1), (15, 5, "west", 2)):
        m.set(x, 1, z, f"minecraft:big_dripleaf_stem[facing={f},waterlogged=true]")
        for k in range(1, n):
            m.set(x, 1 + k, z, f"minecraft:big_dripleaf_stem[facing={f},waterlogged=false]")
        m.set(x, 1 + n, z, f"minecraft:big_dripleaf[facing={f},tilt=none,waterlogged=false]")
    for (x, z) in ((10, 3), (16, 7), (11, 9), (16, 2)):
        if W[(x, z)] == 2 and m.get(x, 1, z) == CLAY:
            m.set(x, 2, z, "minecraft:small_dripleaf[facing=east,half=lower,waterlogged=false]")
            m.set(x, 3, z, "minecraft:small_dripleaf[facing=east,half=upper,waterlogged=false]")
    # azalea and flowering azalea on the banks and the ledge, moss carpet between
    for (x, z) in ((11, 0), (14, 11), (16, 10), (12, 1), (2, 1), (5, 9), (8, 1), (3, 10)):
        b = "minecraft:flowering_azalea" if h(x, z, 4) % 2 else "minecraft:azalea"
        if m.get(x, W[(x, z)], z) is None:
            m.set(x, W[(x, z)], z, b)
    for (x, z), w in W.items():
        if m.get(x, w, z) is None and m.get(x, w - 1, z) == MOSS and h(x, z, 11) % 4 == 0 and not 7 <= x <= 9:
            m.set(x, w, z, CARPET)
    # cave vines with glow berries hung from the roof along the walls, spore blossoms under it,
    # hanging roots under the rooted dirt
    for (x, z, n) in ((15, 1, 4), (12, 10, 3), (9, 1, 2), (5, 10, 2), (16, 9, 4), (3, 1, 2), (10, 10, 3)):
        ceil = top if m.get(x, top, z) is None else top - 1
        floor = W[(x, z)]
        n = min(n, ceil - floor - 1)
        for k in range(n):
            y = ceil - k
            m.set(x, y, z, VINE_END if k == n - 1 else (VINE if h(x, y, z) % 3 else VINE_BARE))
    for (x, z) in ((13, 5), (6, 5), (14, 2)):
        if m.get(x, top, z) is None:
            m.set(x, top, z, "minecraft:spore_blossom")
    for x in range(X0 + 1, X1):
        for z in range(Z0 + 1, Z1):
            if m.get(x, LID, z) == ROOTED and m.get(x, top, z) is None and h(x, z, 12) % 2 == 0:
                m.set(x, top, z, "minecraft:hanging_roots[waterlogged=false]")
    m.mark("cat-cave", 10, 6, facing="east", y=2)
    m.mark("axolotl-low", 13, 5, facing="east", y=1)         # in the lower pond's water
    m.mark("upper-pond-rim", 2, 8, facing="north", y=6)
    m.mark("axolotl-high", 2, 5, facing="east", y=5)         # in the upper pond's water
    m.mark("node-lush-cave", 18, 5, facing="west")


def build(place):
    m = Model(place)
    stem = place.a["place"].removeprefix("node/")
    {"cave-path": cave_path, "cave-track": cave_track, "lush-cave": lush_cave}[stem](m, place)
    m.finish()
    return m


# The lush cave's plants hung from its roof and standing in its ponds (vines, spore blossoms,
# hanging roots, dripleaf) are thin blocks in the cave's own air, where no body stands; the
# starter writes such a block unclaimed, which the enclosed room's closure reads as open air on
# its boundary. They are the room's air with a plant in it, and are claimed so.
PLANTS = ("minecraft:cave_vines", "minecraft:spore_blossom", "minecraft:hanging_roots",
          "minecraft:big_dripleaf", "minecraft:small_dripleaf")


def claim_plants(out):
    import json
    with open(out, encoding="utf-8") as f:
        doc = json.load(f)
    roles = {k for k, v in doc["palette"].items() if isinstance(v, str) and v.split("[")[0].startswith(PLANTS)}
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
    print(f"lush cave: {n[0]} plant leaf(s) claimed the room's, over {len(roles)} plant state(s)")


if __name__ == "__main__":
    rc = run(build, reason="rock, roof and wall heads: seen, never stood on")
    out = sys.argv[sys.argv.index("--out") + 1]
    if rc == 0 and out.endswith("lush-cave.json"):
        claim_plants(out)
    raise SystemExit(rc)
