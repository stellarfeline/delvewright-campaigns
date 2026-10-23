#!/usr/bin/env python3
"""Emit programs/upper-town.json — the grammar program of node/upper-town.

Provenance only: the emitted Program is the artifact of record. Every handed
value (frame, datum, seam cells, terrain, voids) is read from `delvec
allocation` at run time and is never typed here; the program reads the datum
and the seam through `handed/...` parameters. Everything else below is the
place's own design: the street, the terraces, the five houses, in piece-local
cells (x east, z south; local = world - frame origin, origin read from the
allocation).

Usage: upper-town.py <delvec> <campaign-dir> <out.json>
"""
import json
import subprocess
import sys

DELVEC, CAMPAIGN, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
alloc = json.loads(subprocess.run(
    [DELVEC, "allocation", CAMPAIGN, "node/upper-town"],
    check=True, capture_output=True, text=True).stdout)

EX, EY, EZ = alloc["extent"]
D = alloc["datum_y"]                      # walk plane of the middle terrace
OX, OY, OZ = alloc["world_min"]
(SX0, SY0, SZ0), (SX1, SY1, SZ1) = alloc["space"]
seam = alloc["seams"][0]
(FX0, FY0, FZ0), (FX1, FY1, FZ1) = seam["cells"]
SEAM = "upper-lower"

def lx(wx): return wx - OX
def lz(wz): return wz - OZ

# Walk planes (standing level, piece-local y) — the design's terraces, four apart.
STEP = 4
L_MID, L_UP, L_SQ = D, D + STEP, D + 2 * STEP

void = set()
for v in alloc["voids"]:
    (a, b, c), (d, e, f) = v["cells"]
    for x in range(a, d + 1):
        for y in range(b, e + 1):
            for z in range(c, f + 1):
                void.add((x, y, z))
T = {(c["x"], c["z"]): c["top"] for c in alloc["ground"]["columns"]}
PER = {(x, z): t for x, t, z in alloc["ground"]["perimeter"]}

# ---------------------------------------------------------------- grid
role = {}     # (x,y,z) -> role name ; absent = air
region = {}   # (x,y,z) -> claim region

def put(x, y, z, r):
    role[(x, y, z)] = r

def air(x, y, z):
    role.pop((x, y, z), None)

def rect(x0, x1, z0, z1):
    return [(x, z) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1)]

# ---------------------------------------------------------------- plan
# pad cells: (x,z) -> standing level ; street cells are paved
pad = {}
paved = set()
kerb = set()
STREET_X0, STREET_X1 = lx(71), lx(76)

def add_pad(cells, L, pave=False):
    for c in cells:
        pad[c] = L
        if pave:
            paved.add(c)

# the square and its ring onto flight 1
add_pad(rect(lx(65), lx(82), lz(96), lz(109)), L_SQ, True)
add_pad(rect(STREET_X0, STREET_X1, lz(110), lz(110)), L_SQ, True)
# middle terrace: the whole front, at the datum
add_pad(rect(SX0, SX1, lz(137), SZ1), L_MID)
add_pad(rect(STREET_X0, STREET_X1, lz(137), SZ1), L_MID, True)
# upper street and its rings
add_pad(rect(STREET_X0, STREET_X1, lz(117), lz(130)), L_UP, True)

# houses: interior footprint (world), floor level, clearance, roof courses, roof kind,
# door side and door z/x (world), style
HOUSES = [
    dict(name="chapel", ix=(54, 63), iz=(98, 106), L=L_SQ, C=6, N=6, roof="slate",
         door=("east", 102), style="stone", ridge="z"),
    dict(name="inn", ix=(84, 94), iz=(97, 107), L=L_SQ, C=4, N=6, roof="slate",
         door=("west", 102), style="timber", ridge="z"),
    dict(name="smithy", ix=(62, 69), iz=(119, 126), L=L_UP, C=4, N=4, roof="shingle",
         door=("east", 122), style="timber", ridge="z"),
    dict(name="weaver", ix=(78, 84), iz=(118, 128), L=L_UP, C=4, N=5, roof="shingle",
         door=("west", 123), style="timber", ridge="z"),
    dict(name="merchant", ix=(60, 69), iz=(139, 148), L=L_MID, C=5, N=5, roof="slate",
         door=("east", 143), style="timber", ridge="z"),
]
for h in HOUSES:
    # walls stand outside the interior; a wall that would fall in the ring stands
    # on the frame's first layer instead (the frame allows no further)
    wx0 = max(SX0, lx(h["ix"][0]) - 1)
    wx1 = min(SX1, lx(h["ix"][1]) + 1)
    wz0 = max(SZ0, lz(h["iz"][0]) - 1)
    wz1 = min(SZ1, lz(h["iz"][1]) + 1)
    h["w"] = (wx0, wx1, wz0, wz1)
    ring = rect(max(SX0, wx0 - 1), min(SX1, wx1 + 1), max(SZ0, wz0 - 1), min(SZ1, wz1 + 1))
    add_pad([c for c in ring if c not in pad], h["L"])

# flights: x street, 6 long; treads rise to the north end
FLIGHTS = [
    dict(name="flight-1", z0=lz(111), lower=L_UP, upper=L_SQ),
    dict(name="flight-2", z0=lz(131), lower=L_MID, upper=L_UP),
]
flight_top = {}   # (x,z) -> top block y of tread or floor
for f in FLIGHTS:
    for i in range(6):
        z = f["z0"] + i
        for x in range(STREET_X0, STREET_X1 + 1):
            if i < STEP:
                flight_top[(x, z)] = f["upper"] - 1 - i      # stair block y
            else:
                pad[(x, z)] = f["lower"]
                paved.add((x, z))
    f["tread_z"] = (f["z0"], f["z0"] + STEP - 1)

for (x, z) in list(paved):
    if x in (STREET_X0, STREET_X1):
        kerb.add((x, z))

# ---------------------------------------------------------------- ground surface
play = rect(SX0, SX1, SZ0, SZ1)
S = {}
for c in play:
    if c in pad:
        S[c] = pad[c] - 1
    elif c in flight_top:
        S[c] = flight_top[c]
    else:
        S[c] = T[c]

def P(c):
    """top block y of a walked cell (pad surface or tread)."""
    if c in pad:
        return pad[c] - 1
    return flight_top[c]

walked = set(pad) | set(flight_top)
hill = [c for c in play if c not in walked]
fence = set()
retain = {}   # hillside column -> lowest pad top it retains against
for (x, z) in hill:
    adj = [(x + dx, z + dz) for dx in (-1, 0, 1) for dz in (-1, 0, 1)
           if (dx or dz) and (x + dx, z + dz) in walked]
    if not adj:
        continue
    hi = max(P(a) for a in adj)
    lo = min(P(a) for a in adj)
    S[(x, z)] = max(T[(x, z)], hi)
    fence.add((x, z))
    if S[(x, z)] > lo:
        retain[(x, z)] = lo

# the play-space border of a walked pad, other than the front: fenced, so no way
# leaves the place the plan did not allocate
in_house = set()
for h in HOUSES:
    wx0, wx1, wz0, wz1 = h["w"]
    in_house |= set(rect(wx0, wx1, wz0, wz1))
for (x, z), L in list(pad.items()):
    if (x, z) in in_house:
        continue
    if (x in (SX0, SX1) or z == SZ0) and z != SZ1:
        fence.add((x, z))
    elif x in (SX0, SX1) and z == SZ1:
        fence.add((x, z))

# ---------------------------------------------------------------- paint ground
for (x, z) in play:
    s = S[(x, z)]
    for y in range(0, s + 1):
        put(x, y, z, "dirt")
    if (x, z) in flight_top:
        put(x, s, z, "tread_n")
        continue
    if (x, z) in pad:
        if (x, z) in kerb:
            put(x, s, z, "kerb")
        elif (x, z) in paved:
            put(x, s, z, "paving")
        else:
            put(x, s, z, "grass")
    else:
        put(x, s, z, "grass")
        if (x, z) in retain:
            lo = retain[(x, z)]
            for y in range(lo + 1, s + 1):
                put(x, y, z, "kerb")
            put(x, lo + 1, z, "mossy")
for (x, z), t in PER.items():
    for y in range(0, t + 1):
        put(x, y, z, "dirt")

# exposed faces of the terraces (pad and retaining columns) are stone-brick walls
def solid(x, y, z):
    if (x, y, z) in void:
        return True
    return (x, y, z) in role

for (x, z) in play:
    if (x, z) not in pad and (x, z) not in retain:
        continue
    s = S[(x, z)]
    exposed = []
    for y in range(0, s):
        if (x, y, z) in void:
            continue
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, nz = x + dx, z + dz
            if not (0 <= nx < EX and 0 <= nz < EZ):
                continue
            if not solid(nx, y, nz):
                exposed.append(y)
                break
    for y in exposed:
        put(x, y, z, "mossy" if (y - 1) not in exposed else "kerb")

# ---------------------------------------------------------------- flights
for f in FLIGHTS:
    for x in range(STREET_X0, STREET_X1 + 1):
        for i in range(STEP):
            z = f["z0"] + i
            y = f["upper"] - 1 - i
            for yy in range(0, y):
                if role.get((x, yy, z)) == "dirt" or (x, yy, z) not in role:
                    put(x, yy, z, "dirt")
            put(x, y - 1, z, "kerb")
            put(x, y, z, "tread_n")

# ---------------------------------------------------------------- houses
ROOF = {"slate": ("roof_slate_e", "roof_slate_w", "slate"),
        "shingle": ("roof_shingle_e", "roof_shingle_w", "shingle")}
houses_roofbox = []

def wall_role(h, c, along_x, pos, x, z):
    """c = course above floor; pos = index along the wall."""
    if h["style"] == "stone":
        return "chapel_base" if c == 0 else "chapel_wall"
    if c <= 1:
        return "cobble"
    if c == 2:
        return "beam_x" if along_x else "beam_z"
    return "post" if pos % 3 == 0 else "infill"

for h in HOUSES:
    wx0, wx1, wz0, wz1 = h["w"]
    L, C, N = h["L"], h["C"], h["N"]
    F = L  # first air course inside
    for x in range(wx0, wx1 + 1):
        for z in range(wz0, wz1 + 1):
            edge_x = x in (wx0, wx1)
            edge_z = z in (wz0, wz1)
            put(x, L - 1, z, "floor_" + h["name"] if not (edge_x or edge_z) else "cobble")
            for c in range(C):
                y = F + c
                if edge_x or edge_z:
                    if edge_x and edge_z:
                        r = "chapel_wall" if h["style"] == "stone" else (
                            "cobble" if c <= 1 else "post")
                    else:
                        along_x = edge_z
                        pos = (x - wx0) if along_x else (z - wz0)
                        r = wall_role(h, c, along_x, pos, x, z)
                    put(x, y, z, r)
                else:
                    air(x, y, z)
    # windows: glass panes, ground course 1 and upper course 3 (where C allows)
    def windows(cells, along_x):
        pane = "pane_x" if along_x else "pane_z"
        for i, (x, z) in enumerate(cells):
            if i == 0 or i == len(cells) - 1:
                continue
            if i % 3 != 2 and h["style"] != "stone":
                continue
            if h["style"] == "stone" and i % 3 != 1:
                continue
            for c in ((1, 3) if h["style"] != "stone" else (1, 2, 3)):
                if c < C - (0 if h["style"] != "stone" else 1):
                    put(x, F + c, z, pane)
    windows([(x, wz0) for x in range(wx0, wx1 + 1)], True)
    windows([(x, wz1) for x in range(wx0, wx1 + 1)], True)
    windows([(wx0, z) for z in range(wz0, wz1 + 1)], False)
    windows([(wx1, z) for z in range(wz0, wz1 + 1)], False)
    # door: centred on its street face, 1 x 2
    side, dw = h["door"]
    dz = lz(dw)
    dx = wx1 if side == "east" else wx0
    for zz in (dz - 1, dz, dz + 1):     # door reveal: no pane beside it
        for c in range(C):
            if role.get((dx, F + c, zz), "").startswith("pane"):
                put(dx, F + c, zz, "cobble" if c <= 1 else "infill")
    # the doorway: the engine's walk reads every door block as solid, so the
    # 1 x 2 opening is left open under its lintel
    air(dx, F, dz)
    air(dx, F + 1, dz)
    h["door_cell"] = (dx, dz)
    # roof: 45-degree stairs over the eave span; slopes face east and west
    ex0 = max(SX0, wx0 - 1)
    ex1 = min(SX1, wx1 + 1)
    ez0 = max(SZ0, wz0 - 1)
    ez1 = min(SZ1, wz1 + 1)
    se, sw, block = ROOF[h["roof"]]
    top = 0
    for k in range(N):
        y = F + C + k
        if y >= EY:
            break
        a, b = ex0 + k, ex1 - k
        if a > b:
            break
        for z in range(ez0, ez1 + 1):
            gable = z in (wz0, wz1)
            for x in range(a, b + 1):
                # no eave over the plot's edge: the ground there stitches to the
                # whole's ring, and an overhang is air under the higher edge
                on_edge = x in (SX0, SX1) or z in (SZ0, SZ1)
                if on_edge and not (wx0 <= x <= wx1 and wz0 <= z <= wz1):
                    continue
                if a < b and x == a:
                    put(x, y, z, se)
                elif a < b and x == b:
                    put(x, y, z, sw)
                else:
                    if k == 0 and wx0 < x < wx1 and wz0 < z < wz1:
                        r = "ceiling_" + h["name"]
                    elif gable and wx0 <= x <= wx1:
                        r = "chapel_wall" if h["style"] == "stone" else "infill"
                    else:
                        r = block
                    put(x, y, z, r)
        top = y
    # a lantern hung under the middle of each eave, lighting the yard below it
    for (x, z) in ((ex0, (wz0 + wz1) // 2), (ex1, (wz0 + wz1) // 2),
                   ((wx0 + wx1) // 2, ez0), ((wx0 + wx1) // 2, ez1)):
        if wx0 <= x <= wx1 and wz0 <= z <= wz1:
            continue
        if x in (SX0, SX1) or z in (SZ0, SZ1):
            continue
        put(x, F + C - 1, z, "lantern_hung")
    houses_roofbox.append((ex0, ex1, F + C, EY - 1, ez0, ez1))
    # interior light: lanterns hung from the ceiling, every 4 or so
    ix0, ix1, iz0, iz1 = wx0 + 1, wx1 - 1, wz0 + 1, wz1 - 1
    xs = list(range(ix0 + 1, ix1, 4)) or [(ix0 + ix1) // 2]
    zs = list(range(iz0 + 1, iz1, 4)) or [(iz0 + iz1) // 2]
    for x in xs:
        for z in zs:
            put(x, F + C - 1, z, "lantern_hung")
    h["interior"] = (ix0, ix1, iz0, iz1)

H = {h["name"]: h for h in HOUSES}

# chapel: altar at the west end, pews facing it, a short tower at the north-east
ch = H["chapel"]; ix0, ix1, iz0, iz1 = ch["interior"]; F = ch["L"]
mid = (iz0 + iz1) // 2
for z in range(mid - 1, mid + 2):
    put(ix0, F, z, "altar")
for x in (ix0 + 3, ix0 + 5):
    for z in list(range(iz0 + 1, mid - 1)) + list(range(mid + 2, iz1)):
        put(x, F, z, "pew")
wx0, wx1, wz0, wz1 = ch["w"]
for x in range(wx1 - 2, wx1 + 1):
    for z in range(wz0, wz0 + 3):
        for y in range(F, EY):
            edge = x in (wx1 - 2, wx1) or z in (wz0, wz0 + 2)
            if y < F + ch["C"] and not edge:
                put(x, y, z, "chapel_wall")
            elif y == EY - 1:
                if x in (wx1 - 2, wx1) and z in (wz0, wz0 + 2):
                    put(x, y, z, "merlon")
                else:
                    air(x, y, z)
            elif y in (EY - 3, EY - 4) and (x, z) in ((wx1 - 1, wz0), (wx1, wz0 + 1)):
                air(x, y, z)          # belfry openings, north and east
            else:
                put(x, y, z, "chapel_wall")
for z in range(wz0, wz0 + 3):
    for x in range(wx1 - 2, wx1 + 1):
        if role.get((x, F + ch["C"] - 1, z)) == "lantern_hung":
            put(x, F + ch["C"] - 1, z, "chapel_wall")

# inn: benches along the east wall facing in, a red runner from the door
inn = H["inn"]; ix0, ix1, iz0, iz1 = inn["interior"]; F = inn["L"]
for z in range(iz0 + 1, iz1):
    if z % 3 != 0:
        put(ix1, F, z, "bench_w")
for x in range(ix0, ix1):
    put(x, F, (iz0 + iz1) // 2, "runner")

# smithy: open forge front on the street, forge and chimney at the west wall
sm = H["smithy"]; ix0, ix1, iz0, iz1 = sm["interior"]; F = sm["L"]
wx0, wx1, wz0, wz1 = sm["w"]
dz = sm["door_cell"][1]
for z in range(dz + 2, wz1):
    for c in range(sm["C"] - 1):
        air(wx1, F + c, z)
fz = (iz0 + iz1) // 2
put(ix0, F, fz - 1, "brick"); put(ix0, F, fz + 1, "brick")
put(ix0, F, fz, "forge")
for y in range(F + 1, min(EY, F + sm["C"] + sm["N"] + 2)):
    put(ix0, y, fz, "brick")
put(ix0 + 3, F, fz, "anvil")
put(ix1 - 1, F, iz1, "grindstone")
put(ix1 - 1, F, iz0, "smithing")

# weaver: looms by the windows, bolts of cloth along the east wall
wv = H["weaver"]; ix0, ix1, iz0, iz1 = wv["interior"]; F = wv["L"]
for z in (iz0 + 1, iz0 + 4):
    put(ix0 + 2, F, z, "loom")
cloth = ["wool_white", "wool_blue", "wool_red", "wool_white", "wool_yellow"]
for i, z in enumerate(range(iz0, iz1 + 1)):
    if i % 2 == 0:
        put(ix1, F, z, cloth[(i // 2) % len(cloth)])

# merchant: a counting room behind a partition at the south end
me = H["merchant"]; ix0, ix1, iz0, iz1 = me["interior"]; F = me["L"]
pz = iz1 - 4
door_x = (ix0 + ix1) // 2
for x in range(ix0, ix1 + 1):
    for c in range(me["C"]):
        if x == door_x and c <= 1:
            air(x, F + c, pz)
        else:
            put(x, F + c, pz, "partition")
for x in range(ix0 + 1, ix1):
    if x != door_x:
        put(x, F, iz1, "shelf")
put(door_x, F, iz1 - 1, "counting")
for x in range(ix0, ix1 + 1):
    if role.get((x, F + me["C"] - 1, pz)) == "lantern_hung":
        put(x, F + me["C"] - 1, pz, "partition")
put(ix0 + 1, F + me["C"] - 1, iz1 - 1, "lantern_hung")

# ---------------------------------------------------------------- kerb posts
posts = []
for f in FLIGHTS:
    for x in (STREET_X0 - 1, STREET_X1 + 1):
        posts.append((x, f["z0"]))
        posts.append((x, f["z0"] + 5))
for h in HOUSES:
    dx, dz = h["door_cell"]
    out = dx + 1 if h["door"][0] == "east" else dx - 1
    posts.append((out, dz - 1))
sqx = (lx(65) + lx(82)) // 2
posts.append((sqx + 1, lz(96) + 9))       # the square's lamp standard
# lamp standards for the night: the yards beside the houses and the open terrace
for wxz in ((66, 109), (80, 109), (56, 143), (85, 143), (91, 139)):
    posts.append((lx(wxz[0]), lz(wxz[1])))
for (x, z) in posts:
    fence.discard((x, z))
    s = S[(x, z)]
    put(x, s + 1, z, "post")
    put(x, s + 2, z, "lantern")

for (x, z) in fence:
    put(x, S[(x, z)] + 1, z, "FENCE")

# ---------------------------------------------------------------- connection states
def is_full(r):
    return r is not None and r not in ("FENCE", "post", "lantern", "lantern_hung") and \
        not r.startswith(("pane", "door", "tread", "roof", "pew", "bench", "runner")) and \
        r not in ("anvil", "grindstone", "forge")

def conn_state(kind, x, y, z):
    def c(nx, nz):
        r = role.get((nx, y, nz))
        if kind == "fence":
            return r == "FENCE" or is_full(r)
        return r is not None and (r.startswith("pane") or is_full(r))
    return dict(east=c(x + 1, z), west=c(x - 1, z), south=c(x, z + 1), north=c(x, z - 1))

palette_extra = {}
for (x, y, z), r in list(role.items()):
    if r == "FENCE":
        st = conn_state("fence", x, y, z)
        name = "fence_" + "".join(k[0] for k in ("north", "east", "south", "west") if st[k]) if any(st.values()) else "fence_post"
        palette_extra[name] = ("minecraft:spruce_fence[east=%s,north=%s,south=%s,waterlogged=false,west=%s]"
                               % tuple(str(st[k]).lower() for k in ("east", "north", "south", "west")))
        role[(x, y, z)] = name
    elif r.startswith("pane"):
        st = conn_state("pane", x, y, z)
        name = "pane_" + "".join(k[0] for k in ("north", "east", "south", "west") if st[k])
        palette_extra[name] = ("minecraft:glass_pane[east=%s,north=%s,south=%s,waterlogged=false,west=%s]"
                               % tuple(str(st[k]).lower() for k in ("east", "north", "south", "west")))
        role[(x, y, z)] = name

# ---------------------------------------------------------------- claims
SPACE = {L_SQ: "square", L_UP: "upper", L_MID: "middle"}
HEAD = 4
for (x, z), L in pad.items():
    for y in range(L, L + HEAD):
        region[(x, y, z)] = SPACE[L]
# a lantern on a kerb post: the cell over it is nobody's floor
for (x, z) in posts:
    s = S[(x, z)]
    for y in range(s + 3, EY):
        if region.get((x, y, z)) in SPACE.values():
            region[(x, y, z)] = "lamps"
for f in FLIGHTS:
    for x in range(STREET_X0, STREET_X1 + 1):
        for z in range(f["tread_z"][0], f["tread_z"][1] + 1):
            for y in range(f["lower"], f["upper"] + 2):
                region[(x, y, z)] = f["name"]
for (x, z) in hill:
    for y in range(S[(x, z)] + 1, EY):
        region[(x, y, z)] = "hillside"
for (a, b, y0, y1, c, d) in houses_roofbox:
    for x in range(a, b + 1):
        for z in range(c, d + 1):
            for y in range(y0, y1 + 1):
                region[(x, y, z)] = "roofs"
# the ring above the whole's fixed ground is open air, stood on by nobody: it
# stands over structure_void, so it is claimed by no region
# the front: the seam's cells are claimed by the seam slice itself
for x in range(FX0, FX1 + 1):
    for y in range(FY0, FY1 + 1):
        region.pop((x, y, FZ0), None)
        air(x, y, FZ0)

# void cells: paint whatever merges best (they are replaced after expansion)
for (x, y, z) in void:
    region.pop((x, y, z), None)

# ---------------------------------------------------------------- palette
PALETTE = {
    "dirt": "minecraft:dirt",
    "grass": "minecraft:grass_block[snowy=false]",
    "paving": [{"weight": 8, "block": "minecraft:cobblestone"},
               {"weight": 1, "block": "minecraft:mossy_cobblestone"},
               {"weight": 1, "block": "minecraft:andesite"}],
    "kerb": "minecraft:stone_bricks",
    "mossy": [{"weight": 3, "block": "minecraft:mossy_stone_bricks"},
              {"weight": 1, "block": "minecraft:stone_bricks"}],
    "tread_n": "minecraft:stone_brick_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]",
    "cobble": [{"weight": 6, "block": "minecraft:cobblestone"},
               {"weight": 1, "block": "minecraft:mossy_cobblestone"}],
    "beam_x": "minecraft:spruce_log[axis=x]",
    "beam_z": "minecraft:spruce_log[axis=z]",
    "post": "minecraft:spruce_log[axis=y]",
    "infill": "minecraft:calcite",
    "chapel_base": "minecraft:cobblestone",
    "chapel_wall": [{"weight": 8, "block": "minecraft:stone_bricks"},
                    {"weight": 1, "block": "minecraft:mossy_stone_bricks"},
                    {"weight": 1, "block": "minecraft:cracked_stone_bricks"}],
    "merlon": "minecraft:stone_brick_wall[east=none,north=none,south=none,up=true,waterlogged=false,west=none]",
    "roof_slate_e": "minecraft:deepslate_tile_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]",
    "roof_slate_w": "minecraft:deepslate_tile_stairs[facing=west,half=bottom,shape=straight,waterlogged=false]",
    "slate": "minecraft:deepslate_tiles",
    "roof_shingle_e": "minecraft:dark_oak_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]",
    "roof_shingle_w": "minecraft:dark_oak_stairs[facing=west,half=bottom,shape=straight,waterlogged=false]",
    "shingle": "minecraft:dark_oak_planks",
    "door_lo_east": "minecraft:spruce_door[facing=west,half=lower,hinge=left,open=true,powered=false]",
    "door_hi_east": "minecraft:spruce_door[facing=west,half=upper,hinge=left,open=true,powered=false]",
    "door_lo_west": "minecraft:spruce_door[facing=east,half=lower,hinge=left,open=true,powered=false]",
    "door_hi_west": "minecraft:spruce_door[facing=east,half=upper,hinge=left,open=true,powered=false]",
    "lantern": "minecraft:lantern[hanging=false,waterlogged=false]",
    "lantern_hung": "minecraft:lantern[hanging=true,waterlogged=false]",
    "post": "minecraft:spruce_log[axis=y]",
    "altar": "minecraft:chiseled_stone_bricks",
    "pew": "minecraft:spruce_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]",
    "bench_w": "minecraft:spruce_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]",
    "runner": "minecraft:red_carpet",
    "brick": "minecraft:bricks",
    "forge": "minecraft:magma_block",
    "anvil": "minecraft:anvil[facing=north]",
    "grindstone": "minecraft:grindstone[face=floor,facing=north]",
    "smithing": "minecraft:smithing_table",
    "loom": "minecraft:loom[facing=west]",
    "wool_white": "minecraft:white_wool",
    "wool_blue": "minecraft:blue_wool",
    "wool_red": "minecraft:red_wool",
    "wool_yellow": "minecraft:yellow_wool",
    "partition": "minecraft:spruce_planks",
    "shelf": "minecraft:bookshelf",
    "counting": "minecraft:cartography_table",
    "floor_chapel": "minecraft:polished_andesite",
    "floor_inn": "minecraft:spruce_planks",
    "floor_smithy": "minecraft:cobblestone",
    "floor_weaver": "minecraft:spruce_planks",
    "floor_merchant": "minecraft:spruce_planks",
    "ceiling_chapel": "minecraft:spruce_planks",
    "ceiling_inn": "minecraft:spruce_planks",
    "ceiling_smithy": "minecraft:spruce_planks",
    "ceiling_weaver": "minecraft:spruce_planks",
    "ceiling_merchant": "minecraft:spruce_planks",
}
# kerb posts carrying a lantern: a stone-brick wall post
PALETTE["kerb_post"] = "minecraft:stone_brick_wall[east=none,north=none,south=none,up=true,waterlogged=false,west=none]"
for (x, z) in posts:
    put(x, S[(x, z)] + 1, z, "kerb_post")
PALETTE.update(palette_extra)
used = set(role.values())
PALETTE = {k: v for k, v in PALETTE.items() if k in used}
missing = used - set(PALETTE)
assert not missing, missing

# ---------------------------------------------------------------- emit
rules = {}
cache = {}

def I(v): return {"expr": "int", "value": v}
def A(e): return {"size": "absolute", "blocks": e}
def REL(): return {"size": "relative", "weight": I(1)}
def PARAM(n): return {"expr": "param", "name": n}
def ADD(a, b): return {"expr": "arith", "lhs": a, "op": "add", "rhs": b}
def SUB(a, b): return {"expr": "arith", "lhs": a, "op": "sub", "rhs": b}

def leaf(cell):
    r, g = cell
    body = {"op": "fill", "material": {"role": r}} if r else {"op": "void"}
    if g:
        body = {"op": "claim", "region": g, "body": body}
    return body

def rule(body, hint):
    key = json.dumps(body, sort_keys=True)
    if key not in cache:
        name = "%s-%d" % (hint, len(cache) + 1)
        cache[key] = name
        rules[name] = [{"weight": 1, "body": body}]
    return {"op": "call", "symbol": cache[key]}

def runs(seq):
    out = []
    for v in seq:
        if out and out[-1][0] == v:
            out[-1][1] += 1
        else:
            out.append([v, 1])
    return out

def split(axis, items, hint):
    rs = runs(items)
    if len(rs) == 1:
        return rs[0][0]
    sizes = [A(I(n)) for _, n in rs[:-1]] + [REL()]
    return {"op": "split", "axis": axis, "sizes": sizes, "children": [c for c, _ in rs]}

def cell(x, y, z):
    if (x, y, z) in void:
        return ("dirt", None)
    return (role.get((x, y, z)), region.get((x, y, z)))

def column(x, z, y0, y1):
    cells = [cell(x, y, z) for y in range(y0, y1 + 1)]
    body = split("y", [json.dumps(c) for c in cells], "col")
    if isinstance(body, str):
        return rule(leaf(json.loads(body)), "c")
    body["children"] = [leaf(json.loads(c)) for c in body["children"]]
    return rule(body, "c")

def box(x0, x1, y0, y1, z0, z1, hint):
    slices = []
    for x in range(x0, x1 + 1):
        cols = [json.dumps(column(x, z, y0, y1)) for z in range(z0, z1 + 1)]
        b = split("z", cols, "s")
        if isinstance(b, str):
            slices.append(json.dumps(json.loads(b)))
        else:
            b["children"] = [json.loads(c) for c in b["children"]]
            slices.append(json.dumps(rule(b, "s")))
    b = split("x", slices, hint)
    if isinstance(b, str):
        return json.loads(b)
    b["children"] = [json.loads(c) for c in b["children"]]
    return rule(b, hint)

hp = lambda k: PARAM("handed/seam/%s/%s" % (SEAM, k))
datum = PARAM("handed/datum-y")

body_part = {"op": "split", "axis": "y", "sizes": [A(datum), REL()],
             "children": [box(0, EX - 1, 0, D - 1, 0, FZ0 - 1, "below"),
                          box(0, EX - 1, D, EY - 1, 0, FZ0 - 1, "above")]}
front_open = {"op": "split", "axis": "x",
              "sizes": [A(hp("x0")), A(ADD(SUB(hp("x1"), hp("x0")), I(1))), REL()],
              "children": [box(0, FX0 - 1, FY0, FY1, FZ0, FZ0, "frontw"),
                           {"op": "claim", "region": "front", "body": {"op": "void"}},
                           box(FX1 + 1, EX - 1, FY0, FY1, FZ0, FZ0, "fronte")]}
front_plane = {"op": "split", "axis": "y",
               "sizes": [A(hp("y0")), A(ADD(SUB(hp("y1"), hp("y0")), I(1))), REL()],
               "children": [box(0, EX - 1, 0, FY0 - 1, FZ0, FZ0, "frontlo"),
                            front_open,
                            box(0, EX - 1, FY1 + 1, EY - 1, FZ0, FZ0, "fronthi")]}
town = {"op": "split", "axis": "z",
        "sizes": [A(hp("z0")), A(ADD(SUB(hp("z1"), hp("z0")), I(1))), REL()],
        "children": [rule(body_part, "terraces"), rule(front_plane, "front-plane"), {"op": "skip"}]}

sp_x, sp_z = sqx - 1, lz(96) + 5
nd_x, nd_z = sqx + 1, lz(96) + 11
start = {"op": "mark",
         "mark": {"anchor": "spawn", "at": "offset", "facing": "south",
                  "x": I(sp_x), "y": ADD(datum, I(2 * STEP)), "z": I(sp_z)},
         "body": {"op": "mark",
                  "mark": {"anchor": "node-upper-town", "at": "offset", "facing": "south",
                           "x": I(nd_x), "y": ADD(datum, I(2 * STEP)), "z": I(nd_z)},
                  "body": town}}
rules["place"] = [{"weight": 1, "body": start}]

params = {"handed/datum-y": D}
for k, v in zip(("x0", "y0", "z0", "x1", "y1", "z1"), (FX0, FY0, FZ0, FX1, FY1, FZ1)):
    params["handed/seam/%s/%s" % (SEAM, k)] = v

contract = {
    "entry": "middle",
    "spaces": {"square": {"envelope": "open"}, "upper": {"envelope": "open"},
               "middle": {"envelope": "open"}},
    "no_body": {
        "hillside": {"reason": "the stepped turf between the terraces, fenced off the street; nobody walks it"},
        "roofs": {"reason": "the roofs and the chapel tower's top; nobody walks them"},
        "lamps": {"reason": "the top of a lantern on a kerb post"},
    },
    "edges": [
        {"a": "middle", "b": "exterior", "class": "walk", "via": "front"},
        {"a": "middle", "b": "upper", "class": "stair", "rise": STEP, "via": "flight-2"},
        {"a": "upper", "b": "square", "class": "stair", "rise": STEP, "via": "flight-1"},
    ],
    "no_body_majority_ack": "an open hillside town owns its slopes and roofs, which are more standable surface than its streets; they are fenced off and nobody walks them",
}

program = {
    "version": "1.12.0",
    "name": "upper-town",
    "start": "place",
    "params": params,
    "palette": PALETTE,
    "rules": rules,
    "contract": contract,
    # An open hillside town is looked at from every side but its front (the
    # front's plane stands against the lower town's box). Its north, east and
    # west sides are the hill's own turf edge at the plot's ring, stepping down
    # past the commons ground outside: finished ground surface, not a buried cut.
    "shown_faces": ["east", "north", "up", "west"],
}
with open(OUT, "w") as fh:
    json.dump(program, fh, indent=1, sort_keys=True)
    fh.write("\n")
print("rules", len(rules), "roles", len(PALETTE), file=sys.stderr)
