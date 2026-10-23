#!/usr/bin/env python3
"""Emit programs/lower-town.json — the lower town of Saltstair.

Provenance only: the emitted Program is the artifact of record. Every handed
value is read from `delvec allocation` (never typed here) and the values the
program itself uses are declared as `handed/...` parameters whose defaults are
those handed values. Design positions come from the place's brief, written in
world coordinates and converted with the handed frame origin.

Usage: lower-town.py <delvec> <campaign-dir> <out.json>
"""
import json
import math
import subprocess
import sys

DELVEC, CAMPAIGN, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
ALLOC = json.loads(subprocess.run(
    [DELVEC, "allocation", CAMPAIGN, "node/lower-town"],
    check=True, capture_output=True, text=True).stdout)

EX, EY, EZ = ALLOC["extent"]
WMIN = ALLOC["world_min"]
D = ALLOC["datum_y"]                      # walk plane of the quay
SEAM = ALLOC["seams"][0]
SEAM_STEM = SEAM["edge"].split("/", 1)[1]
(SX0, SY0, SZ0), (SX1, SY1, SZ1) = SEAM["cells"]
GROUND = ALLOC["ground"]
TOP = {(c["x"], c["z"]): c["top"] for c in GROUND["columns"]}
PERIM_N = {c[0]: c[1] for c in GROUND["perimeter"] if c[2] == -1}
VOID = set()
for v in ALLOC["voids"]:
    (a, b, c), (d, e, f) = v["cells"]
    for x in range(a, d + 1):
        for y in range(b, e + 1):
            for z in range(c, f + 1):
                VOID.add((x, y, z))


def lx(wx): return wx - WMIN[0]
def ly(wy): return wy - WMIN[1]
def lz(wz): return wz - WMIN[2]


# Terraces: four blocks apart, the quay's walk plane being the datum.
L3, L7, L11, L15 = D, D + 4, D + 8, D + 12
SX = range(lx(71), lx(76) + 1)            # the street, six wide
KERB = (lx(71), lx(76))

# ---------------------------------------------------------------- blocks
def st(name, **p):
    if not p:
        return "minecraft:" + name
    return "minecraft:%s[%s]" % (name, ",".join("%s=%s" % kv for kv in sorted(p.items())))

def stair(name, facing):
    return st(name, facing=facing, half="bottom", shape="straight", waterlogged="false")

def wall_state(name, n="none", e="none", s="none", w="none", up="true"):
    return st(name, north=n, east=e, south=s, west=w, up=up, waterlogged="false")

STONE = st("stone_bricks"); MOSSY = st("mossy_stone_bricks")
COBBLE = st("cobblestone"); DIRT = st("dirt"); GRASS = st("grass_block", snowy="false")
SAND = st("sand"); ANDESITE = st("polished_andesite"); CALCITE = st("calcite")
LOG_Y = st("spruce_log", axis="y"); LOG_X = st("spruce_log", axis="x"); LOG_Z = st("spruce_log", axis="z")
PLANKS = st("spruce_planks"); DO_PLANKS = st("dark_oak_planks"); TILES = st("deepslate_tiles")
GLASS = st("glass"); WATER = st("water", level="0")
LANTERN = st("lantern", hanging="false", waterlogged="false")
LANTERN_H = st("lantern", hanging="true", waterlogged="false")
TREAD = stair("stone_brick_stairs", "north")
BRICK_SLAB = st("stone_brick_slab", type="bottom", waterlogged="false")
SAND_SLAB = st("smooth_sandstone_slab", type="bottom", waterlogged="false")

# Mixed roles: what a block of the grid is painted with when it is one of these.
MIX = {
    "retaining": [(STONE, 6), (MOSSY, 2), (st("cracked_stone_bricks"), 1)],
    "retaining-foot": [(MOSSY, 3), (STONE, 1)],
    "paving": [(COBBLE, 7), (st("mossy_cobblestone"), 1)],
}

G = {}          # (x,y,z) -> state or mix-role name; absent = air
REG = {}        # (x,y,z) -> region name (air cells only)


def put(x, y, z, s):
    if 0 <= x < EX and 0 <= y < EY and 0 <= z < EZ:
        G[(x, y, z)] = s


def column(x, z, top, surface, under=DIRT, bottom=0):
    for y in range(bottom, top):
        put(x, y, z, under)
    put(x, top, z, surface)


# ---------------------------------------------------------------- walk map
H = {}          # (x,z) -> walk height (may be .5 on a slab)
SPACE = {}      # (x,z) -> space or via name
CAT = {}        # (x,z) -> 'walk' | 'bld' | 'post'

def walk(x, z, h, space):
    H[(x, z)] = h
    SPACE[(x, z)] = space
    CAT[(x, z)] = "walk"


def ground_under(x, z, h, surface):
    """A walked column: solid to the walk plane, its own surface on top."""
    if h != int(h):
        n = int(h)
        column(x, z, n - 1, STONE)
        put(x, n, z, BRICK_SLAB)
    else:
        column(x, z, int(h) - 1, surface)


# The front lane, z 151..152, level with the seam's opening across the whole
# width: below the opening this face is solid, so the only way between the two
# places is the one the plan allocated.
assert SY0 == L15
LANE_Z = (lz(151), lz(152))
for z in LANE_Z:
    for x in range(1, EX - 1):
        walk(x, z, SY0, "head")
        ground_under(x, z, SY0, STONE if x in KERB else ("paving" if x in SX else COBBLE))
# the ring at either end of the lane is raised to it and walled, on top of the
# ground the whole fixed there
for x in (0, EX - 1):
    for z in LANE_Z:
        for y in range(0, SY0):
            if (x, y, z) not in VOID:
                put(x, y, z, "retaining")
        put(x, SY0, z, wall_state("stone_brick_wall", n="none", s="none", up="true"))

# The street: terraces and flights of four treads.
def street_run(z0, z1, h, space):
    for z in range(lz(z0), lz(z1) + 1):
        for x in SX:
            walk(x, z, h, space)
            ground_under(x, z, h, STONE if x in KERB else "paving")


def flight(z_top, upper, via):
    """Four treads, the first one row south of the upper terrace's last row."""
    for i in range(4):
        z = z_top + i
        y = upper - 1 - i
        for x in SX:
            H[(x, z)] = y + 1
            SPACE[(x, z)] = via
            CAT[(x, z)] = "walk"
            column(x, z, y - 1, STONE)
            put(x, y, z, TREAD)


flight(lz(153), L15, "flight-3")
street_run(157, 170, L11, "lower")
flight(lz(171), L11, "flight-4")
street_run(175, 186, L7, "shore")
flight(lz(187), L7, "flight-5")
street_run(191, 193, L3, "quay")

# The quay, a straight stone wall at the water; the beach west of it.
QX = range(lx(58), lx(89) + 1)
QZ = range(lz(194), lz(200) + 1)
for z in QZ:
    for x in range(1, lx(89) + 1):
        if x <= lx(55):
            walk(x, z, L3 - 1, "quay")
            column(x, z, L3 - 2, SAND, under=SAND)
        elif x == lx(56):
            walk(x, z, L3 - 0.5, "quay")
            column(x, z, L3 - 2, SAND, under=SAND)
            put(x, L3 - 1, z, SAND_SLAB)
        else:
            walk(x, z, L3, "quay")
            edge = z == QZ[-1]
            band = (x - QX[0]) % 8 == 0 or z == QZ[0]
            column(x, z, L3 - 1, STONE if (edge or band) else ANDESITE, under=STONE)

# The sea beyond the quay wall is the whole's: no water is painted here. The
# quay wall's footing course fills the ring below the water's top, so no cell
# of this piece stands a body under the sea.
for x in range(EX):
    for y in range(0, ly(62) + 1):
        if (x, y, EZ - 1) not in VOID:
            put(x, y, EZ - 1, "retaining-foot")

# ---------------------------------------------------------------- buildings
BLD = set()

def roof(x0, x1, z0, z1, base, along, block, cap, eave_cols=True):
    """Gabled roof, 45-degree stair courses over the span across `along`'s
    other axis: ceil((W-1)/2) courses. Eaves one block out at the first
    course. Returns the y of each course per cross position."""
    if along == "z":
        W = x1 - x0 + 1
        n = math.ceil((W - 1) / 2)
        for k in range(n):
            y = base + k
            for z in range(z0, z1 + 1):
                put(x0 + k, y, z, stair(block, "east"))
                put(x1 - k, y, z, stair(block, "west"))
        if W % 2 == 1:
            for z in range(z0, z1 + 1):
                put(x0 + n, base + n - 1, z, cap)
        if eave_cols:
            for z in range(z0, z1 + 1):
                put(x0 - 1, base, z, stair(block, "east"))
                put(x1 + 1, base, z, stair(block, "west"))
        return n
    W = z1 - z0 + 1
    n = math.ceil((W - 1) / 2)
    for k in range(n):
        y = base + k
        for x in range(x0, x1 + 1):
            put(x, y, z0 + k, stair(block, "south"))
            put(x, y, z1 - k, stair(block, "north"))
    if W % 2 == 1:
        for x in range(x0, x1 + 1):
            put(x, base + n - 1, z0 + n, cap)
    if eave_cols:
        for x in range(x0, x1 + 1):
            put(x, base - 1, z0 - 1, stair(block, "south"))
            put(x, base - 1, z1 + 1, stair(block, "north"))
    return n


def foundation(x, z, floor_y, mat=STONE):
    column(x, z, floor_y - 1, mat)
    BLD.add((x, z)); CAT[(x, z)] = "bld"


def gable(x0, x1, z0, z1, base, along, fill_fn):
    """Fill the triangle under the roof at both gable ends."""
    if along == "z":
        n = math.ceil((x1 - x0) / 2)
        for k in range(n + 1):
            for x in range(x0 + k + 1, x1 - k):
                for z in (z0, z1):
                    fill_fn(x, base + k, z)
    else:
        n = math.ceil((z1 - z0) / 2)
        for k in range(n + 1):
            for z in range(z0 + k + 1, z1 - k):
                for x in (x0, x1):
                    fill_fn(x, base + k, z)


# 6 — the rope walk: a long low shed open along its street side.
RW = (lx(77), lx(85), lz(157), lz(170))      # walls, from the interior x 78..84 z 158..169
x0, x1, z0, z1 = RW
for x in range(x0, x1 + 1):
    for z in range(z0, z1 + 1):
        foundation(x, z, L11, COBBLE if (x0 < x < x1 and z0 < z < z1) else STONE)
        if x0 < x < x1 and z0 < z < z1:
            walk(x, z, L11, "lower")
posts_w = {z0, z0 + 3, z1 - 3, z1}
for z in range(z0, z1 + 1):
    # west, the street side: open bays between spruce posts
    if z in posts_w:
        for y in (L11, L11 + 1):
            put(x0, y, z, LOG_Y)
    else:
        walk(x0, z, L11, "lower")
        put(x0, L11 - 1, z, COBBLE)
    # east wall: a stone plinth course, calcite between posts above
    put(x1, L11, z, STONE)
    put(x1, L11 + 1, z, LOG_Y if (z - z0) % 4 == 0 or z == z1 else CALCITE)
for x in range(x0, x1 + 1):
    for z in (z0, z1):
        if x != x0:
            put(x, L11, z, STONE)
            put(x, L11 + 1, z, LOG_Y if x == x1 or (x - x0) % 4 == 0 else CALCITE)
RW_BASE = L11 + 2
roof(x0, x1, z0, z1, RW_BASE, "z", "dark_oak_stairs", DO_PLANKS, eave_cols=False)
for z in range(z0, z1 + 1):                    # eaves at the first course
    put(x0 - 1, RW_BASE, z, stair("dark_oak_stairs", "east"))
    put(x1 + 1, RW_BASE, z, stair("dark_oak_stairs", "west"))
gable(x0, x1, z0, z1, RW_BASE, "z",
      lambda x, y, z: put(x, y, z, CALCITE if (x - x0) % 2 else PLANKS))
ridge_x = x0 + math.ceil((x1 - x0) / 2)
for z in range(z0 + 2, z1 - 1, 4):
    put(ridge_x, EY - 2, z, LANTERN_H)
for z in range(z0 + 1, z1):                    # coiled rope on the floor? no: a clear walk
    pass

# 7 — the harbourmaster's house: narrow, a lamp in its gable, door east.
HM = (lx(61), lx(70), lz(176), lz(185))
x0, x1, z0, z1 = HM
HM_CLEAR = 4
for x in range(x0, x1 + 1):
    for z in range(z0, z1 + 1):
        foundation(x, z, L7, COBBLE if (x0 < x < x1 and z0 < z < z1) else STONE)
        if x0 < x < x1 and z0 < z < z1:
            walk(x, z, L7, "shore")
HM_DOOR = (x1, lz(180))
def frame_wall(x, z, floor, clear, corner, post):
    for y in range(floor, floor + clear):
        if corner:
            s = LOG_Y
        elif y < floor + 2:
            s = STONE
        else:
            s = LOG_Y if post else CALCITE
        put(x, y, z, s)
for x in range(x0, x1 + 1):
    for z in range(z0, z1 + 1):
        if x in (x0, x1) or z in (z0, z1):
            corner = x in (x0, x1) and z in (z0, z1)
            post = ((x - x0) % 3 == 0) if z in (z0, z1) else ((z - z0) % 3 == 0)
            frame_wall(x, z, L7, HM_CLEAR, corner, post)
for x in range(x0, x1 + 1):                    # a spruce beam at the wall head
    for z in (z0, z1):
        put(x, L7 + HM_CLEAR - 1, z, LOG_X)
HM_BASE = L7 + HM_CLEAR
roof(x0, x1, z0, z1, HM_BASE, "x", "dark_oak_stairs", DO_PLANKS)
gable(x0, x1, z0, z1, HM_BASE, "x",
      lambda x, y, z: put(x, y, z, LOG_Y if (z - z0) % 3 == 0 else CALCITE))
# the door, centred on the street face
dx, dz = HM_DOOR
# a doorway 1 x 2 in a spruce frame: the walk model passes no door leaf
def doorway(x, z, floor, frame_axis):
    for y in (floor, floor + 1):
        G.pop((x, y, z), None)
    put(x, floor + 2, z, LOG_X if frame_axis == "x" else LOG_Z)
doorway(dx, dz, L7, "z")
walk(dx, dz, L7, "shore"); CAT[(dx, dz)] = "walk"
# the lamp in the street gable
put(x1, HM_BASE + 1, lz(180), LANTERN)
put(x1, HM_BASE + 2, lz(180), GLASS)
# windows lit from inside: a lantern on the sill, glass over it
for (x, z) in [(x0 + 2, z0), (x1 - 2, z0), (x0 + 2, z1), (x1 - 2, z1),
               (x0, z0 + 3), (x0, z1 - 3), (x1, z0 + 2), (x1, z1 - 2)]:
    put(x, L7 + 1, z, LANTERN)
    put(x, L7 + 2, z, GLASS)

# 8 — the warehouse: a long stone store, door south onto the quay.
WH = (lx(79), lx(90), lz(181), lz(193))
x0, x1, z0, z1 = WH
WH_CLEAR = 5
for x in range(x0, x1 + 1):
    for z in range(z0, z1 + 1):
        inner = x0 < x < x1 and z0 < z < z1
        foundation(x, z, L3, COBBLE if inner else STONE)
        if inner:
            walk(x, z, L3, "quay")
        elif True:
            for y in range(L3, L3 + WH_CLEAR):
                corner = x in (x0, x1) and z in (z0, z1)
                put(x, y, z, ANDESITE if (corner or y == L3) else STONE)
WH_BASE = L3 + WH_CLEAR
roof(x0, x1, z0, z1, WH_BASE, "z", "deepslate_tile_stairs", TILES, eave_cols=False)
for z in range(z0, z1 + 1):
    put(x0 - 1, WH_BASE, z, stair("deepslate_tile_stairs", "east"))
    put(x1 + 1, WH_BASE, z, stair("deepslate_tile_stairs", "west"))
gable(x0, x1, z0, z1, WH_BASE, "z", lambda x, y, z: put(x, y, z, STONE))
WH_DOOR = (lx(84), z1)
dx, dz = WH_DOOR
doorway(dx, dz, L3, "x")
walk(dx, dz, L3, "quay")
for z in range(z0 + 2, z1 - 1, 3):
    for x in (x0, x1):
        put(x, L3 + 1, z, LANTERN)
        put(x, L3 + 2, z, GLASS)
for x in (x0 + 3, x1 - 3):
    for z in (z0, z1):
        put(x, L3 + 1, z, LANTERN)
        put(x, L3 + 2, z, GLASS)

# ---------------------------------------------------------------- posts
POSTS = set()
POST_H = {}     # (x,z) -> the walk height a post stands on
def kerb_post(x, z):
    h = H[(x, z)]
    del H[(x, z)], SPACE[(x, z)]
    CAT[(x, z)] = "post"
    POSTS.add((x, z))
    POST_H[(x, z)] = h
    put(x, int(h), z, wall_state("stone_brick_wall"))
    put(x, int(h) + 1, z, LANTERN)

for zw in (157, 170, 175, 186, 191):
    for x in KERB:
        kerb_post(x, lz(zw))
kerb_post(lx(71), lz(178))                     # at the harbourmaster's door
kerb_post(lx(76), lz(161))                     # at the rope walk's door
# spruce-log bollards on the quay's edge, a lantern on every other one
for i, x in enumerate(range(QX[0] + 2, QX[-1], 5)):
    if x in SX:
        continue
    z = QZ[-1]
    POST_H[(x, z)] = H[(x, z)]
    del H[(x, z)], SPACE[(x, z)]
    CAT[(x, z)] = "post"
    put(x, L3, z, LOG_Y)
    if i % 2 == 0:
        put(x, L3 + 1, z, LANTERN)

# ---------------------------------------------------------------- hillside
LANTERN_AT = set()
def parapet_lanterns():
    pass

for x in range(1, EX - 1):
    for z in range(0, EZ - 1):
        if (x, z) in CAT:
            continue
        top = max(TOP[(x, z)], ly(62))          # no turf at or below the sea's top
        column(x, z, top, GRASS)
        CAT[(x, z)] = "hill"

# The ring the whole left unfixed is filled to the sea's top where it lies
# lower, on whatever ground the whole fixed there.
for x in (0, EX - 1):
    for z in range(EZ):
        for y in range(0, ly(62) + 1):
            if (x, y, z) not in VOID and G.get((x, y, z)) is None:
                below_fixed = all((x, yy, z) in VOID or G.get((x, yy, z)) for yy in range(0, y))
                if below_fixed:
                    put(x, y, z, GRASS if y == ly(62) else DIRT)

# Pads under each house's one-cell ring, level with its floor where the
# hill falls below it.
for (bx0, bx1, bz0, bz1), floor in ((RW, L11), (HM, L7), (WH, L3)):
    for x in range(bx0 - 1, bx1 + 2):
        for z in range(bz0 - 1, bz1 + 2):
            if CAT.get((x, z)) == "hill" and TOP[(x, z)] < floor - 1:
                column(x, z, floor - 1, GRASS)

def surface_top(x, z):
    y = EY - 1
    while y >= 0 and G.get((x, y, z)) is None:
        y -= 1
    return y

# Every hill column beside a walked one stands up to the walk and carries a
# low wall: the hillside is fenced, never walked. A kerb post or bollard stands
# in the walk, so a column beside one is fenced as if beside the street: left
# open, it is a pit between two walls a body dropping off a roof cannot leave.
NB = ((1, 0), (-1, 0), (0, 1), (0, -1))
PARAPET = {}
for x in range(1, EX - 1):
    for z in range(0, EZ - 1):
        if CAT.get((x, z)) != "hill":
            continue
        hs = [H.get((x + dx, z + dz), POST_H.get((x + dx, z + dz))) for dx, dz in NB
              if (x + dx, z + dz) in H or (x + dx, z + dz) in POST_H]
        if not hs:
            continue
        c = max(math.ceil(h) for h in hs)
        top = surface_top(x, z)
        s = max(top, c - 1)
        for y in range(0, s + 1):
            put(x, y, z, DIRT if y < top else ("retaining-foot" if y == top else "retaining"))
        put(x, s, z, STONE)
        if s + 1 < c + 2 and s + 1 < EY:
            PARAPET[(x, z)] = s + 1

def wall_neighbours(x, y, z):
    out = {}
    for name, (dx, dz) in (("east", (1, 0)), ("west", (-1, 0)), ("south", (0, 1)), ("north", (0, -1))):
        out[name] = "low" if PARAPET.get((x + dx, z + dz)) == y else "none"
    return out

# The town's edge: the ring beside the hillside is walled on top of whatever
# stands there, so the hillside is left only as the town is. The beach and the
# quay stay open to the sea: a swimmer climbs out where the beach runs on west.
BEACH_Z = lz(194)
for z in range(EZ - 1):
    if z in LANE_Z:
        continue
    for x in (0, EX - 1):
        if x == 0 and z >= BEACH_Z - 1:
            continue
        y = EY - 1
        while y >= 0 and G.get((x, y, z)) is None and (x, y, z) not in VOID:
            y -= 1
        if y + 1 < EY:
            PARAPET[(x, z)] = y + 1

LAMP_EVERY = 5
for (x, z), y in sorted(PARAPET.items()):
    n = wall_neighbours(x, y, z)
    lamp = ((x + z) % LAMP_EVERY == 0) and y + 1 < EY and z != 0
    straight = (n["east"] == n["west"] == "low" and n["north"] == n["south"] == "none") or \
               (n["north"] == n["south"] == "low" and n["east"] == n["west"] == "none")
    put(x, y, z, wall_state("stone_brick_wall", n["north"], n["east"], n["south"], n["west"],
                            "false" if straight and not lamp else "true"))
    if lamp:
        put(x, y + 1, z, LANTERN)
# the head of the flight carries its lanterns on the parapets either side
for x in (KERB[0] - 1, KERB[1] + 1):
    z = lz(153)
    if (x, z) in PARAPET and PARAPET[(x, z)] + 1 < EY:
        y = PARAPET[(x, z)]
        put(x, y, z, wall_state("stone_brick_wall", "none", "none", "none", "none", "true"))
        put(x, y + 1, z, LANTERN)

# ---------------------------------------------------------------- regions
PASSABLE_PREFIX = ("minecraft:spruce_door",)
def is_air(s):
    return s is None

for x in range(EX):
    for z in range(EZ):
        sp = SPACE.get((x, z))
        if sp is not None:
            h = H[(x, z)]
            y = int(h) if h != int(h) else int(h)
            if G.get((x, int(h) - 1, z), "").startswith("minecraft:stone_brick_stairs") if False else False:
                pass
            # treads: the tread cell itself is in the flight's volume
            ystart = int(h) - 1 if SPACE[(x, z)].startswith("flight") else (int(h) if h == int(h) else int(h))
            yy = ystart
            while yy < EY:
                s = G.get((x, yy, z))
                if yy > ystart and not (s is None or s.startswith(PASSABLE_PREFIX)):
                    break
                REG[(x, yy, z)] = sp
                yy += 1
            for y2 in range(yy, EY):
                if G.get((x, y2, z)) is None:
                    REG[(x, y2, z)] = "grounds"
        else:
            for y in range(EY):
                if G.get((x, y, z)) is None and (x, y, z) not in VOID:
                    REG[(x, y, z)] = "grounds"

# the seam's opening: emitted through the handed parameters, not the grid
OPEN = set()
for x in range(SX0, SX1 + 1):
    for y in range(SY0, SY1 + 1):
        for z in range(SZ0, SZ1 + 1):
            assert G.get((x, y, z)) is None, ("opening cell painted", x, y, z)
            OPEN.add((x, y, z))
            REG.pop((x, y, z), None)

# ---------------------------------------------------------------- emit
ROLES = {}
def role_of(s):
    if s in MIX:
        ROLES[s] = [{"weight": w, "block": b} for b, w in MIX[s]]
        return s
    name = s.replace("minecraft:", "")
    if "[" in name:
        base, props = name[:-1].split("[")
        bits = []
        for kv in props.split(","):
            k, v = kv.split("=")
            if v in ("false", "none", "bottom", "straight", "0") and k not in ("open",):
                continue
            bits.append(v if k not in ("north", "east", "south", "west", "up") else k[0] + v[0])
        name = base + ("-" + "-".join(bits) if bits else "")
    name = name.replace("_", "-")
    ROLES.setdefault(name, s)
    assert ROLES[name] == s or isinstance(ROLES[name], list), (name, s, ROLES[name])
    return name


def leaf(s, r):
    if s is None:
        node = {"op": "void"}
    else:
        node = {"op": "fill", "material": {"role": role_of(s)}}
    if r is not None:
        node = {"op": "claim", "region": r, "body": node}
    return node


def I(v): return {"expr": "int", "value": v}
def P(n): return {"expr": "param", "name": n}
def A(l, op, r): return {"expr": "arith", "lhs": l, "op": op, "rhs": r}
def absz(e): return {"size": "absolute", "blocks": e}
REL = {"size": "relative", "weight": I(1)}

RULES = {}
CACHE = {}
def rule(prefix, body):
    key = json.dumps(body, sort_keys=True)
    if key not in CACHE:
        name = "%s-%d" % (prefix, len([k for k in RULES if k.startswith(prefix + "-")]) + 1)
        RULES[name] = [{"weight": 1, "body": body}]
        CACHE[key] = name
    return {"op": "call", "symbol": CACHE[key]}


def cell(x, y, z):
    return (G.get((x, y, z)), REG.get((x, y, z)))


def runs(seq):
    out = []
    for v in seq:
        if out and out[-1][0] == v:
            out[-1][1] += 1
        else:
            out.append([v, 1])
    return out


def split(axis, parts):
    if len(parts) == 1:
        return parts[0][0]
    return {"op": "split", "axis": axis,
            "sizes": [absz(I(n)) for _, n in parts],
            "children": [c for c, _ in parts]}


def col_node(x, z, ys):
    rs = runs([cell(x, y, z) for y in ys])
    return split("y", [(leaf(*v), n) for v, n in rs])


def box_node(xs, ys, zs, tag):
    """x slices of z runs of y columns, every distinct column one rule."""
    slices = []
    for x in xs:
        cols = [rule("col", col_node(x, z, ys)) for z in zs]
        rz = runs([json.dumps(c, sort_keys=True) for c in cols])
        slices.append(json.dumps(split("z", [(json.loads(c), n) for c, n in rz]), sort_keys=True))
    rx = runs(slices)
    return split("x", [(rule(tag, json.loads(s)), n) for s, n in rx])


# z 151 (the seam's layer) is split in y by the handed seam; the rest is the grid
z_open = range(SZ0, SZ1 + 1)
below = box_node(range(EX), range(0, SY0), z_open, "front")
opening_layer = {"op": "split", "axis": "x",
                 "sizes": [absz(P("handed/seam/%s/x0" % SEAM_STEM)),
                           absz(A(A(P("handed/seam/%s/x1" % SEAM_STEM), "sub", P("handed/seam/%s/x0" % SEAM_STEM)), "add", I(1))),
                           REL],
                 "children": [box_node([0], range(SY0, SY1 + 1), z_open, "front"),
                              {"op": "claim", "region": "seam-" + SEAM_STEM, "body": {"op": "void"}},
                              box_node([EX - 1], range(SY0, SY1 + 1), z_open, "front")]}
front = {"op": "split", "axis": "y",
         "sizes": [absz(P("handed/seam/%s/y0" % SEAM_STEM)), REL],
         "children": [below,
                      {"op": "split", "axis": "y",
                       "sizes": [absz(A(A(P("handed/seam/%s/y1" % SEAM_STEM), "sub", P("handed/seam/%s/y0" % SEAM_STEM)), "add", I(1))), REL],
                       "children": [opening_layer, {"op": "void"}]}]}
rest = box_node(range(EX), range(EY), range(SZ1 + 1, EZ), "slice")
body = {"op": "split", "axis": "z",
        "sizes": [absz(A(A(P("handed/seam/%s/z1" % SEAM_STEM), "sub", P("handed/seam/%s/z0" % SEAM_STEM)), "add", I(1))), REL],
        "children": [rule("front-layer", front), rule("town", rest)]}

QUAY_MARK = (lx(73), lz(195))
NODE_MARK = (lx(74), lz(181))
assert SPACE.get(QUAY_MARK) == "quay" and SPACE.get(NODE_MARK) == "shore"
start = {"op": "mark",
         "mark": {"anchor": "quay", "at": "offset", "facing": "south",
                  "x": I(QUAY_MARK[0]), "y": P("handed/datum-y"), "z": I(QUAY_MARK[1])},
         "body": {"op": "mark",
                  "mark": {"anchor": "node-lower-town", "at": "offset", "facing": "south",
                           "x": I(NODE_MARK[0]), "y": A(P("handed/datum-y"), "add", I(L7 - D)),
                           "z": I(NODE_MARK[1])},
                  "body": body}}
RULES["lower-town"] = [{"weight": 1, "body": start}]


def miny(region):
    ys = [k[1] for k, v in REG.items() if v == region]
    return min(ys)

spaces = ["head", "lower", "shore", "quay"]
edges = [
    {"a": "exterior", "b": "head", "class": "walk", "via": "seam-" + SEAM_STEM},
    {"a": "lower", "b": "head", "class": "stair", "rise": miny("head") - miny("lower"), "via": "flight-3"},
    {"a": "shore", "b": "lower", "class": "stair", "rise": miny("lower") - miny("shore"), "via": "flight-4"},
    {"a": "quay", "b": "shore", "class": "stair", "rise": miny("shore") - miny("quay"), "via": "flight-5"},
]
params = {"handed/datum-y": D}
for k, v in zip(("x0", "y0", "z0", "x1", "y1", "z1"), (SX0, SY0, SZ0, SX1, SY1, SZ1)):
    params["handed/seam/%s/%s" % (SEAM_STEM, k)] = v

program = {
    "version": "1.10.0",
    "name": "saltstair-lower-town",
    "start": "lower-town",
    "params": params,
    "palette": dict(sorted(ROLES.items())),
    "shown_faces": ["east", "north", "south", "up", "west"],
    "contract": {
        "entry": "head",
        "spaces": {s: {"envelope": "open"} for s in spaces},
        "no_body": {"grounds": {"reason": "the fenced hillside, the gardens, the walls' and roofs' tops: the town's ground nobody walks"}},
        "edges": edges,
        "no_body_majority_ack": "a hillside town owns its ground, and its stepped turf, its garden walls and its roofs are more standable surface than its street; every such cell is fenced off the walk and open to the sky",
    },
    "rules": RULES,
}
with open(OUT, "w") as f:
    json.dump(program, f, indent=1, sort_keys=True)
    f.write("\n")
print("rules", len(RULES), "roles", len(ROLES), "edges", [(e["a"], e["b"], e.get("rise")) for e in edges])
