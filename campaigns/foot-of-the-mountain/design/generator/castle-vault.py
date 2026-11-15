#!/usr/bin/env python3
"""node/castle-vault — the old lords' vault, an easter egg in the crag at the castle grounds'
west edge.

    DELVEWRIGHT_SKILL=<skill> python3 castle-vault.py --allocation <delvec allocation . node/castle-vault> \\
        --out ../../programs/castle-vault.json --delvec <delvec>

After the priest hole and the secret passage (the node's `references[]`): a hiding place built
into the fabric, its way in a stretch of stone that reads as the wall around it. A body stands
on the castle's grounds before a face of the crag; when the four levers are down, a stretch of
it three wide and three high swings away (the seam's bar, a block that hides) and a stone stair
runs down four into a small vaulted strongroom: four chests of arms along the far wall, lamps
on the piers between them, banners of the old lords over them. Piece-local: +x east (the castle), +z south, the
walk plane at y 1.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
from starter import Model, lantern, run, stairs  # noqa: E402

CHESTS = (2, 4, 6, 8)        # the four chests along the west wall, z
BAR = "bar-castle-vault"
HIDES = "minecraft:stone"    # the swinging stone: a block the game draws as a full opaque cube, the crag's own


def build(place):
    m = Model(place)
    m.palette["rock"] = [{"weight": 5, "block": "minecraft:stone"}, {"weight": 3, "block": "minecraft:andesite"},
                         {"weight": 2, "block": "minecraft:tuff"}, {"weight": 1, "block": "minecraft:cobblestone"}]
    m.palette["vault"] = [{"weight": 8, "block": "minecraft:stone_bricks"}, {"weight": 2, "block": "minecraft:cracked_stone_bricks"},
                          {"weight": 1, "block": "minecraft:mossy_stone_bricks"}]
    m.palette["vfloor"] = "minecraft:polished_deepslate"
    # surveyed open: the way's reach is judged with its door swung away (a gate's open state),
    # and the program binds the shut door after the run, below
    m.palette[BAR] = "minecraft:air"
    d = place.datum.value                     # the walk plane (y 1)
    lo, hi = place.space
    X0, X1, Z0, Z1 = lo[0], hi[0], lo[2], hi[2]
    top = hi[1]
    # the crag: rock through the whole play space, the room and the stair cut out of it
    m.box(X0, X1, d - 1, top, Z0, Z1, "rock")
    # the strongroom: x 1..6, z 1..8, its floor at the walk plane, a barrel vault over it
    m.box(1, 6, d - 1, d - 1, 1, 8, "vfloor")
    m.box(1, 6, d, d + 5, 1, 8, "vault")
    m.clear(2, 6, d, d + 3, 1, 8)
    m.clear(3, 5, d + 4, d + 4, 1, 8)
    m.clear(1, 1, d, d + 1, 1, 8)
    # the stair down from the door (x 11, walk y 5) to the room: a landing at x 10, treads x 9..7
    m.climbs_to("edge/castle-vault")
    m.clear(7, 10, d, d + 7, 4, 6)
    for z in range(4, 7):
        for y in range(d - 1, d + 4):
            m.set(10, y, z, "vault")            # the landing, built solid down to the floor
        for k, x in enumerate((9, 8, 7)):
            m.set(x, d + 2 - k, z, stairs("minecraft:stone_brick", "east"))
            for y in range(d - 1, d + 2 - k):
                m.set(x, y, z, "vault")
    for x in range(7, 11):
        for z in (3, 7):
            for y in range(d - 1, d + 8):
                m.set(x, y, z, "vault")
    # the four chests of arms along the west wall, a lantern on each, a banner over each
    for k, z in enumerate(CHESTS, start=1):
        m.set(1, d, z, "minecraft:chest[facing=east,type=single,waterlogged=false]")
        m.mark(f"vault-chest-{k}", 1, z, facing="east", y=d)
    for z in (1, 3, 5, 7):
        m.set(1, d, z, "vault")
        m.set(1, d + 1, z, "vault")
        if z > 1:
            m.set(1, d + 2, z, lantern())      # a lamp on the pier between two chests
    m.set(6, d + 3, 1, lantern(True))
    m.set(6, d + 3, 8, lantern(True))
    # the crag's crown, open to the sky over the grounds: rock grown over with moss
    m.palette["crown"] = [{"weight": 4, "block": "minecraft:stone"}, {"weight": 3, "block": "minecraft:moss_block"},
                          {"weight": 2, "block": "minecraft:andesite"}, {"weight": 1, "block": "minecraft:mossy_cobblestone"}]
    m.box(X0, X1, top, top, Z0, Z1, "crown")
    m.show("up")
    m.mark("node-castle-vault", 4, 5, facing="west")
    m.finish()
    return m


rc = run(build, reason="the crag's rock and the vault's wall heads: seen, never stood on")
# the hidden way is shut by a block that hides (spec-0118): the starter binds a seam's bar to the
# derivation's iron bars, which the eye looks through, so the program's bar is bound to the stone
if rc == 0:
    import json
    out = sys.argv[sys.argv.index("--out") + 1]
    doc = json.load(open(out, encoding="utf-8"))
    assert BAR in doc["palette"], "the program binds no bar"
    doc["palette"][BAR] = HIDES
    with open(out, "w", encoding="utf-8") as f:
        f.write(json.dumps(doc, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
raise SystemExit(rc)
