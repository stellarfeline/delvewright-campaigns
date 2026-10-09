"""Act 2 — the Crossing, and the body's bank: the detail builders of the flat's places.

    python3 generators/places_act2.py "$(command -v delvec)" "$DELVEWRIGHT_PREFABS" [stem ...]

Every frame, seam and owed name comes from `delvec allocation`. Local x runs east,
y up from the floor course (the mud's top course), z south.

The flat is wet black mud over the sea; the Pilgrims' Way is the old road's
stones; its marker stakes carry the lamps the lighthouse lit. Every open place
holds one roofed thing a body can step under (a hull's belly, a refuge, a
shelter), so the contract's closure has something real to judge.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *  # noqa: F401,F403
import kit
from places_act1 import (TOWN_STONE, RUBBLE, MUD, room_shell, hang, lamp_post, flight,
                         stair_head, landing)

ROAD = [{"weight": 5, "block": "minecraft:mossy_stone_bricks"},
        {"weight": 3, "block": "minecraft:cracked_stone_bricks"},
        {"weight": 2, "block": "minecraft:mossy_cobblestone"},
        {"weight": 2, "block": "minecraft:gray_terracotta"}]
# wet black mud, measured (block-appearance.py): mud #3c393d, muddy mangrove roots #453b2f,
# grey terracotta #3a2a24, black terracotta #251710 — packed mud (#8e6b50) reads orange, so not here
FLATMUD = [{"weight": 7, "block": "minecraft:mud"}, {"weight": 1, "block": "minecraft:muddy_mangrove_roots[axis=y]"},
           {"weight": 1, "block": "minecraft:gray_terracotta"}, {"weight": 1, "block": "minecraft:black_terracotta"}]
BANKMUD = [{"weight": 6, "block": "minecraft:mud"}, {"weight": 2, "block": "minecraft:gray_terracotta"},
           {"weight": 1, "block": "minecraft:muddy_mangrove_roots[axis=y]"}, {"weight": 1, "block": "minecraft:black_terracotta"}]
HULL = "minecraft:dark_oak_planks"
ROT = [{"weight": 4, "block": "minecraft:dark_oak_planks"}, {"weight": 2, "block": "minecraft:spruce_planks"},
       {"weight": 1, "block": "minecraft:stripped_dark_oak_wood[axis=y]"}]


def h(*a):
    """A small deterministic hash for scattering (no RNG: ADR-0006)."""
    v = 2166136261
    for x in a:
        v = ((v ^ (x & 0xffffffff)) * 16777619) & 0xffffffff
    return v


def stake(p, x, z, lit_=True, h_=2, y0=1):
    """A marker stake of the old road: a weathered post, its lamp on top."""
    for y in range(y0, y0 + h_):
        p.put(x, y, z, log("stripped_spruce_log"))
    if lit_:
        p.put(x, y0 + h_, z, LANTERN)


def low_lamp(p, x, z):
    """A crew's lamp on a short stake in the mud."""
    p.put(x, 1, z, fence("spruce"))
    p.put(x, 2, z, LANTERN)


def mud_floor(p, role, puddles=0.06, salt=0):
    W, L = p.W, p.L
    for x in range(W):
        for z in range(L):
            p.put(x, 0, z, role)
            if (h(x, z, salt) % 1000) < puddles * 1000:
                p.put(x, 0, z, WATER)


def litter(p, x0, z0, x1, z1, salt, n=12, keep=()):
    """What the mud brought up: kelp heaps, bones, driftwood, a lost crate."""
    things = ["minecraft:dried_kelp_block", bone("x"), bone("z"), log("spruce_log", "x"),
              log("dark_oak_log", "z"), "minecraft:black_terracotta", "minecraft:brain_coral_block",
              "minecraft:dead_tube_coral_block"]
    placed = 0
    i = 0
    while placed < n and i < n * 20:
        i += 1
        x = x0 + h(i, salt, 1) % max(1, x1 - x0 + 1)
        z = z0 + h(i, salt, 2) % max(1, z1 - z0 + 1)
        if (x, z) in keep or p.get(x, 1, z) is not None or p.get(x, 0, z) == WATER:
            continue
        p.put(x, 1, z, things[h(i, salt, 3) % len(things)])
        placed += 1


def hull(p, x0, z0, length, beam, heel, along="z", depth=3, broken=(), roofed=False):
    """A wooden hull lying in the mud: planked sides, ribs standing over the gunwale, a stem
    and a sternpost; heeled so one side stands a course higher. `roofed` lays the upper
    side over as a deck, so a body can step in under it."""
    hb = beam // 2
    for i in range(length):
        taper = 1 if i in (0, length - 1) else (0 if 1 < i < length - 2 else 0)
        w = max(1, hb - (1 if i in (0, length - 1) else 0))
        for j in range(-w, w + 1):
            x, z = (x0 + j, z0 + i) if along == "z" else (x0 + i, z0 + j)
            side = abs(j) == w
            p.put(x, 0, z, HULL)
            if side:
                top = depth + (1 if (j > 0) == (heel > 0) else 0)
                for y in range(1, top + 1):
                    if (i, y) in broken:
                        continue
                    p.put(x, y, z, HULL if (i + y) % 3 else log("stripped_dark_oak_log", "y"))
                if i % 2 == 0:
                    p.put(x, top + 1, z, log("dark_oak_log", "y"))
            elif roofed and 2 <= i <= length - 3:
                p.put(x, depth + 1, z, slab("dark_oak", "top"))
        if i in (0, length - 1):
            x, z = (x0, z0 + i) if along == "z" else (x0 + i, z0)
            for y in range(1, depth + 3):
                p.put(x, y, z, log("dark_oak_log", "y"))


# =============================================================================
def pilgrims_way():
    """The Pilgrims' Way: the old road's worn stones running out over the black mud, the
    marker stakes on both sides with the lamps the lighthouse lit, the town's lights behind;
    halfway, the old refuge box for anyone the tide caught."""
    p = Place("pilgrims-way", envelope="open")
    W, H, L = p.W, p.H, p.L
    mud = p.role("mud", FLATMUD)
    road = p.role("road", ROAD)
    mud_floor(p, mud, 0.05, 3)
    for z in range(L):
        for x in range(1, 6):
            p.put(x, 0, z, road)
    for z in range(4, L - 2, 9):
        stake(p, 0, z); stake(p, 6, z + 4)
    for z in range(9, L - 2, 18):
        p.put(7, 1, z, log("stripped_spruce_log", "x"))     # a stake that fell
    # the refuge box: a timber hut on the way's west edge
    rz = 60
    for z in range(rz, rz + 4):
        for x in (0, 1):
            p.put(x, 0, z, "minecraft:spruce_planks")
            p.put(x, 3, z, "minecraft:spruce_planks")
            p.put(x, 4, z, slab("spruce"))
        for y in (1, 2):
            p.put(0, y, z, "minecraft:spruce_planks")
    for y in (1, 2):
        p.put(1, y, rz, log("spruce_log")); p.put(1, y, rz + 3, log("spruce_log"))
    p.put(0, 1, rz + 1, stair("spruce", "east"))
    litter(p, 6, 2, 7, L - 3, 31, 10)
    litter(p, 0, 2, 0, L - 3, 37, 6)
    p.cut_seams(floor=road)
    p.mark("node-pilgrims-way", (3, 1, 63), "south")
    return p


def wreck_field():
    """The wreck field: old hulls the rising brought up, lying on the mud on either side of
    the old road, their ribs standing out of the wet black; the Drowned climb out of them;
    on one, its name board."""
    p = Place("wreck-field", envelope="open")
    W, H, L = p.W, p.H, p.L
    mud = p.role("mud", FLATMUD)
    road = p.role("road", ROAD)
    mud_floor(p, mud, 0.06, 5)
    n = p.seam("way-to-wrecks"); nlo, nhi = p.seam_box(n)
    for z in range(L):
        for x in range(nlo[0], nhi[0] + 1):
            if h(x, z, 9) % 7:
                p.put(x, 0, z, road)
    hull(p, 9, 6, 13, 6, 1, "z", 3, broken={(4, 3), (5, 3), (5, 2), (9, 1)}, roofed=True)
    hull(p, 30, 8, 11, 6, -1, "z", 3, broken={(3, 3), (7, 2), (7, 3)})
    hull(p, 6, 27, 12, 5, 1, "x", 2, broken={(6, 2)})
    hull(p, 26, 26, 12, 6, -1, "x", 3, broken={(2, 3), (3, 3), (9, 2)})
    for z in range(3, L - 2, 8):
        stake(p, nlo[0] - 1, z); stake(p, nhi[0] + 1, z + 4)
    for (x, z) in ((5, 4), (14, 21), (34, 22), (3, 36), (25, 37), (36, 3), (5, 16), (35, 34)):
        low_lamp(p, x, z)
    litter(p, 0, 0, W - 1, L - 1, 13, 24, keep={(x, z) for x in range(nlo[0] - 1, nhi[0] + 2) for z in range(L)})
    p.cut_seams(floor=road)
    p.mark("node-wreck-field", (19, 1, 19), "south")
    p.mark("wreck-nameboard", (16, 1, 12), "west")
    return p


def mast_platform():
    """Marrack's mast platform: a railed timber top over the launch's deck, a hood over its
    corner for the lookout, a lamp; it looks along the body's flank."""
    p = Place("mast-platform", envelope="open")
    W, H, L = p.W, p.H, p.L
    p.box(0, 0, 0, W - 1, 0, L - 1, "minecraft:spruce_planks")
    s = p.seam("launch-to-mast"); lo, hi = p.seam_box(s)
    for x in range(W):
        for z in range(L):
            if (x in (0, W - 1) or z in (0, L - 1)) and not (x == 0 and lo[2] <= z <= hi[2]):
                p.put(x, 1, z, fence("spruce", n=z > 0 and x in (0, W - 1), s=z < L - 1 and x in (0, W - 1),
                                     e=x < W - 1 and z in (0, L - 1), w=x > 0 and z in (0, L - 1)))
    p.put(W - 1, 1, L - 1, log("spruce_log")); p.put(W - 1, 2, L - 1, LANTERN)
    for x in (W - 2, W - 1):
        for z in (0, 1):
            p.put(x, 3, z, slab("spruce", "top"))
    p.put(W - 1, 2, 0, log("spruce_log"))
    p.cut_seams(floor="minecraft:spruce_planks")
    p.mark("node-mast-platform", (1, 1, 2), "east")
    return p


def carved_pillars():
    """The carved pillars of the old road: two rows of standing stones flanking the way,
    their faces cut with the same pictures as the Rubbing and less worn; a fallen lintel
    still bridging one pair; the carvers' script at a pillar's foot."""
    p = Place("carved-pillars", envelope="open")
    W, H, L = p.W, p.H, p.L
    mud = p.role("mud", FLATMUD)
    road = p.role("road", ROAD)
    mud_floor(p, mud, 0.04, 7)
    for z in range(L):
        for x in range(5, 10):
            p.put(x, 0, z, road)
    faces = ["minecraft:chiseled_stone_bricks", "minecraft:chiseled_deepslate", "minecraft:chiseled_sandstone",
             "minecraft:chiseled_tuff", "minecraft:polished_blackstone", "minecraft:chiseled_polished_blackstone"]
    for k, z in enumerate((3, 10, 17, 24)):
        for x0, face_x in ((2, 3), (11, 11)):
            ht = 6 - (1 if (k + x0) % 3 == 0 else 0)
            for x in (x0, x0 + 1):
                for zz in (z, z + 1):
                    for y in range(1, ht + 1):
                        p.put(x, y, zz, "minecraft:stone_bricks" if (y + zz) % 4 else "minecraft:mossy_stone_bricks")
            for y in range(2, ht):
                for zz in (z, z + 1):
                    p.put(face_x, y, zz, faces[(k * 3 + y + zz + x0) % len(faces)])
            p.put(x0, ht + 1, z, slab("stone_brick")) if ht < 6 else None
    # the lintel still over the third pair, across the way
    for x in range(2, 14):
        p.put(x, 6, 17, "minecraft:stone_bricks"); p.put(x, 6, 18, "minecraft:stone_bricks")
    for z in (2, 8, 13, 22, 28):
        stake(p, 4, z)
    for z in (5, 11, 24, 30):
        stake(p, 10, z)
    p.put(4, 1, 2, None)
    litter(p, 0, 0, 1, L - 1, 41, 5); litter(p, 14, 0, 15, L - 1, 43, 5)
    p.cut_seams(floor=road)
    p.mark("node-carved-pillars", (7, 1, 14), "south")
    p.mark("pillar-script", (4, 1, 10), "west")
    return p


def narrows():
    """NOT DETAILED (GENERATION.md round 7, engine finding 3): the plan hands this place two
    seams that share their corner cells, which no piece can answer; the builder stands ready
    for the day the allocation does not.

    The Narrows: the old road's ridge, three stones wide between open water; stakes on its
    edge; halfway an arch of the old road stands over it, where the shelf opens to the east
    and the first tentacle's pit lies beyond."""
    p = Place("narrows", envelope="open")
    W, H, L = p.W, p.H, p.L
    road = p.role("road", ROAD)
    mud = p.role("mud", FLATMUD)
    sh = p.seam("narrows-to-shelf"); slo, shi = p.seam_box(sh)
    for z in range(L):
        for x in range(3):
            p.put(x, 0, z, road)
        if slo[2] <= z <= shi[2]:
            p.put(3, 0, z, mud)
        else:
            p.put(3, 0, z, WATER)
            if z % 5 == 2:
                p.put(3, 0, z, "minecraft:mud")
    for z in (4, 15, 27, 39, 51, 60):
        stake(p, 0, z)
    for z in range(0, L, 9):
        if not (slo[2] <= z <= shi[2]):
            p.put(3, 1, z, log("stripped_spruce_log")); p.put(3, 2, z, LANTERN)
    # the lamp stone of the Narrows: a post of the old road with its hooded niche over the way
    az = 50
    for z in (az - 1, az, az + 1):
        p.put(3, 0, z, "minecraft:mossy_stone_bricks")
        for y in (1, 2, 3):
            p.put(3, y, z, "minecraft:mossy_stone_bricks")
    p.put(3, 2, az, LANTERN)
    p.put(2, 3, az, slab("stone_brick", "top"))
    p.cut_seams(floor=road)
    p.mark("node-narrows", (1, 1, 31), "east")
    p.mark("narrows-pit", (2, 1, 29), "east")
    return p


def skiff_stage():
    """The skiff stage: the old road's stone stage at the edge of the black water, the near
    ferry house on its south side, its ferry bell by the land door; mooring posts, coping,
    a bench under a hood at the west end, lamps."""
    p = Place("skiff-stage", envelope="open")
    W, H, L = p.W, p.H, p.L
    stone = p.role("stone", TOWN_STONE)
    p.box(0, 0, 0, W - 1, 0, L - 1, stone)
    d = p.seam("stage-to-near-house"); dlo, dhi = p.seam_box(d)
    for x in range(W):
        for z in range(L):
            if x in (0, W - 1) and z % 3 == 0:
                p.put(x, 1, z, slab("stone_brick"))
    for (x, z) in ((0, 1), (W - 1, 1), (0, 14), (W - 1, 14), (W - 1, 7)):
        p.put(x, 1, z, log("dark_oak_log")); p.put(x, 2, z, LANTERN)
    p.put(7, 1, 2, "minecraft:chiseled_stone_bricks")     # the road's end stone
    for z in range(5, 9):
        p.put(1, 4, z, slab(SLATE_SLAB, "top"))
    for z in (5, 8):
        for y in (1, 2, 3):
            p.put(1, y, z, log("dark_oak_log"))
    p.put(1, 1, 6, stair("spruce", "west")); p.put(1, 1, 7, stair("spruce", "west"))
    for (x, z) in ((12, 4), (13, 4), (12, 5)):
        p.put(x, 1, z, barrel("up"))
    p.put(dlo[0] + 2, 1, L - 2, LANTERN)
    p.cut_seams(floor=stone)
    p.mark("node-skiff-stage", (dlo[0] - 1, 1, L - 3), "south")
    p.mark("near-bell", (dlo[0] - 1, 1, L - 2), "south")
    return p


SLATE_SLAB = "deepslate_tile"


def mud_field(stem, salt, node, hull_at=None, pillars=False):
    """Open mud beside the marked way: wet black mud, standing pools, what the rising brought
    up; a hull's belly or a fallen stone to step under; low lamps on crew stakes."""
    def build():
        p = Place(stem, envelope="open")
        W, H, L = p.W, p.H, p.L
        mud = p.role("mud", FLATMUD)
        mud_floor(p, mud, 0.09, salt)
        if hull_at:
            x0, z0, ln, along = hull_at
            hull(p, x0, z0, ln, 5, 1 if salt % 2 else -1, along, 2, broken={(3, 2)}, roofed=True)
            for k in range(3, ln - 2, 3):     # the crew's lamps hung under the deck
                cx, cz = (x0, z0 + k) if along == "z" else (x0 + k, z0)
                p.put(cx, 2, cz, LANTERN_HANG)
        if pillars:
            for z in range(10, 14):
                for x in range(10, 18):
                    p.put(x, 1 if x in (10, 17) else 3, z, "minecraft:stone_bricks")
                p.put(10, 2, z, "minecraft:mossy_stone_bricks"); p.put(17, 2, z, "minecraft:mossy_stone_bricks")
                for x in range(11, 17):
                    if z in (10, 13):
                        p.put(x, 3, z, "minecraft:chiseled_stone_bricks")
        for i in range(max(3, W * L // 260)):
            x = 3 + h(i, salt, 11) % (W - 6); z = 3 + h(i, salt, 12) % (L - 6)
            if p.get(x, 1, z) is None and p.get(x, 0, z) != WATER:
                low_lamp(p, x, z)
        litter(p, 1, 1, W - 2, L - 2, salt, W * L // 60)
        p.cut_seams(floor=mud)
        p.mark(f"node-{stem}", node, "south")
        return p
    return build


def narrows_shelf():
    """The mud shelf beside the Narrows: a flat of packed mud the first tentacle strikes, its
    pit at the north end ringed by heaped mud and old timbers; a rib of an old hull arched
    over the shelf's south corner; lamps on crew stakes round its edge."""
    p = Place("narrows-shelf", envelope="open")
    W, H, L = p.W, p.H, p.L
    mud = p.role("mud", BANKMUD)
    mud_floor(p, mud, 0.03, 19)
    cx, cz = 13, 1
    for dx in range(-2, 3):
        for dz in range(-1, 3):
            x, z = cx + dx, cz + dz
            if abs(dx) <= 1 and dz <= 1:
                p.put(x, 0, z, "minecraft:soul_soil")
            elif p.inb(x, 0, z):
                p.put(x, 1, z, slab("blackstone") if (dx + dz) % 2 else "minecraft:black_terracotta")
    for (x, z) in ((10, 0), (16, 0), (10, 3), (16, 3)):
        p.put(x, 1, z, log("dark_oak_log")); p.put(x, 2, z, log("dark_oak_log"))
    for (x, z) in ((2, 2), (25, 2), (2, 25), (25, 25), (2, 13), (25, 13), (13, 25), (7, 6), (20, 6)):
        low_lamp(p, x, z)
    for x in range(20, 27):
        p.put(x, 4, 24, log("stripped_dark_oak_log", "x"))
    for y in range(1, 4):
        p.put(20, y, 24, log("stripped_dark_oak_log")); p.put(26, y, 24, log("stripped_dark_oak_log"))
    litter(p, 1, 20, W - 2, L - 2, 23, 8)
    litter(p, 22, 4, W - 2, 18, 29, 4)
    p.cut_seams(floor=mud)
    p.mark("node-narrows-shelf", (13, 1, 13), "north")
    return p


def far_landing():
    """The far landing: the bank where the skiff lands, a stone apron at the far ferry
    house's door and its bell, the crew's tarp on poles over their stores, and their lamp
    stakes running east along the bank to where the Run comes in."""
    p = Place("far-landing", envelope="open")
    W, H, L = p.W, p.H, p.L
    mud = p.role("mud", BANKMUD)
    stone = p.role("stone", TOWN_STONE)
    mud_floor(p, mud, 0.04, 61)
    d = p.seam("far-house-door"); dlo, dhi = p.seam_box(d)
    for x in range(dlo[0] - 4, dlo[0] + 5):
        for z in range(0, 4):
            p.put(x, 0, z, stone)
    for x in range(20, 25):
        p.put(x, 3, 1, slab("spruce", "top")); p.put(x, 3, 2, slab("spruce", "top"))
    for x in (20, 24):
        for y in (1, 2):
            p.put(x, y, 1, fence("spruce"))
    p.put(21, 1, 1, barrel("up")); p.put(22, 1, 1, "minecraft:chest[facing=south,type=single,waterlogged=false]")
    for x in range(4, W - 2, 8):
        stake(p, x, L - 2 if (x // 8) % 2 else 1)
    p.put(dlo[0] + 3, 1, 1, LANTERN); p.put(dlo[0] - 3, 1, 1, LANTERN)
    litter(p, 26, 1, W - 2, L - 2, 67, 14)
    p.cut_seams(floor=mud)
    # the landing's own mark stays where the plan stood it: the body's stamp is placed from it
    # (generators/body_place.json), so it is the body's anchor as much as the landing's
    p.mark("node-far-landing", (35, 1, 3), "north")
    p.mark("far-bell", (dlo[0] - 1, 1, 1), "north")
    p.mark("far-bell-stand", (dlo[0] - 1, 1, 2), "north")
    p.mark("davey-wait", (dlo[0] + 1, 1, 2), "north")
    return p


def jaw_bank():
    """The Jaw Bank: the mud under the head, the lower jaw's peg teeth standing like posts
    either side of the way into the mouth; a pit on each side where a tentacle rises, each
    with a mud flat beside it that its blows come down on; the crew's lamps; Marrack's
    chalk arrow on a tooth."""
    p = Place("jaw-bank", envelope="open")
    W, H, L = p.W, p.H, p.L
    mud = p.role("mud", BANKMUD)
    mud_floor(p, mud, 0.03, 71)
    s = p.seam("jaw-to-mouth"); slo, shi = p.seam_box(s)
    # the teeth: bone posts in a curve either side of the mouth's way
    for (x, z, ht) in ((slo[0] - 2, L - 2, 4), (slo[0] - 3, L - 4, 3), (slo[0] - 4, L - 6, 3),
                       (shi[0] + 2, L - 2, 4), (shi[0] + 3, L - 4, 3), (shi[0] + 4, L - 6, 3)):
        for y in range(1, ht + 1):
            p.put(x, y, z, bone())
    # a rib of the body standing loose on the bank, arched over a hollow by the west pit
    for y in range(1, 5):
        p.put(3, y, 3, bone()); p.put(7, y, 3, bone())
    for x in range(3, 8):
        p.put(x, 5, 3, bone("x"))
    # the two pits: soul soil hollows ringed with heaped mud
    for (cx, cz) in ((12, 11), (29, 8)):
        for dx in range(-2, 3):
            for dz in range(-2, 3):
                x, z = cx + dx, cz + dz
                if not p.inb(x, 0, z):
                    continue
                if abs(dx) <= 1 and abs(dz) <= 1:
                    p.put(x, 0, z, "minecraft:soul_soil")
                elif (dx + dz) % 2 == 0:
                    p.put(x, 1, z, "minecraft:black_terracotta")
    for (x, z) in ((1, 1), (17, 3), (2, 14), (18, 12), (31, 13), (31, 5), (9, 7), (25, 5)):
        low_lamp(p, x, z)
    p.put(slo[0] - 1, 1, L - 3, LANTERN); p.put(shi[0] + 1, 1, L - 3, LANTERN)
    litter(p, 9, 1, 14, 4, 73, 3)
    p.cut_seams(floor=mud)
    p.mark("node-jaw-bank", (15, 1, 7), "south")
    p.mark("chalk-arrow", (slo[0] - 1, 1, L - 2), "south")
    p.mark("jaw-west-pit", (12, 1, 11), "south")
    p.mark("jaw-east-pit", (29, 1, 8), "south")
    p.mark("jaw-west-landing", (5, 1, 12), "south")
    p.mark("jaw-east-landing", (29, 1, 2), "south")
    return p


def flank_ridge():
    """The Flank Ridge: a ridge of mud along the body's west side, the crew's lamp stakes on
    it; halfway, the spotter's post, a timber lookout under a hood, from which the three
    wounds on the flank are in plain sight."""
    p = Place("flank-ridge", envelope="open")
    W, H, L = p.W, p.H, p.L
    mud = p.role("mud", BANKMUD)
    mud_floor(p, mud, 0.02, 83)
    for z in range(L):
        p.put(3, 0, z, "minecraft:gray_terracotta"); p.put(4, 0, z, "minecraft:gray_terracotta")
    for z in range(4, L - 2, 12):
        stake(p, 0, z)
    # the spotter's post: posts, a hood, a bench facing the flank
    sz = 70
    for z in range(sz, sz + 4):
        p.put(0, 3, z, slab("spruce", "top")); p.put(1, 3, z, slab("spruce", "top"))
    for z in (sz, sz + 3):
        p.put(0, 1, z, log("spruce_log")); p.put(0, 2, z, log("spruce_log"))
    p.put(0, 1, sz + 1, stair("spruce", "west")); p.put(0, 1, sz + 2, stair("spruce", "west"))
    p.put(1, 2, sz, LANTERN) if False else p.put(0, 1, sz - 1, LANTERN)
    litter(p, 0, 0, 1, L - 1, 89, 10)
    p.cut_seams(floor=mud)
    p.mark("node-flank-ridge", (3, 1, 73), "east")
    p.mark("spotter-post", (1, 1, 72), "east")
    return p


BUILDERS = {
    "pilgrims-way": pilgrims_way, "wreck-field": wreck_field, "mast-platform": mast_platform,
    "carved-pillars": carved_pillars, "narrows": narrows, "skiff-stage": skiff_stage,
    "mud-wrecks-west": mud_field("mud-wrecks-west", 101, (15, 1, 19), (8, 8, 12, "z")),
    "mud-wrecks-east": mud_field("mud-wrecks-east", 102, (15, 1, 19), (22, 20, 11, "z")),
    "mud-pillars-west": mud_field("mud-pillars-west", 103, (15, 1, 15), pillars=True),
    "mud-pillars-east": mud_field("mud-pillars-east", 104, (15, 1, 15), pillars=True),
    "mud-narrows-west": mud_field("mud-narrows-west", 105, (15, 1, 31), (10, 40, 12, "z")),
    "narrows-shelf": narrows_shelf, "far-landing": far_landing, "jaw-bank": jaw_bank,
    "flank-ridge": flank_ridge,
}

if __name__ == "__main__":
    kit.main(BUILDERS)
