"""The cat's den and its chasm, as one shape: read by `den.py` (the den, a place) and by
`den-chasm.py` (the chasm under the den, a piece the world edits stamp). The stone figure in it is
its own piece (`den_thing.py`).

Coordinates: x XMIN..EX-1 (world 85..178, x 0 at world 107), z ZMIN..EZ-2 (world 76..176, z 0 at
world 98); the den's frame starts at (XMIN, ZMIN). Heights are counted as courses u from the
ledges' top course, u 0 at world y 71: the ledges and the bridge's ends are walked at u 1 (world y
72, the tunnel's floor), the bridge sags to u 0 across its middle, the den's floor course is u -1
(world y 70), its lid u LID (world y 110). The chasm under the den is the same x and z, u -57..-2
(world 14..69). The tunnel comes in at the south face (z 78), x 28..30; the bridge runs north from
it across the chasm to the den's ledge; the figure stands west of the bridge across a dark gap,
facing it, its wings spread along the bridge, its crown under the lid, its feet in the sea's water
at the chasm's floor.

The cave is a union of ellipsoids carved out of rock, its walls broken by a seeded value noise (the
1.18+ noise caves' look: no straight wall, overhangs and knuckles at every height), with the
walked ledges, the bridge's corridor and the figure (and a margin round it) kept clear.
"""
import math

EX, EY, EZ = 72, 40, 80
LID = 39               # the frame ends at world y 110, under the mountain road over the den (its ground course y 111)
# the frame runs west and north of the bridge's own coordinates, to hold the figure whole: x
# XMIN..EX-1, z ZMIN..EZ-1; the coordinates below keep x 0 at world 107 and z 0 at world 98
XMIN, ZMIN = -22, -22
BRIDGE_X = (28, 29, 30)
RAIL_X = (27, 31)
BZ0, BZ1 = 17, 71               # the bridge's deck, south of the den's ledge, north of the tunnel's
SOUTH_Z0 = 72                   # the tunnel's ledge, z 72..78
NORTH_Z1 = 16                   # the den's ledge, z 1..16
STATUE_Z = 41                   # the figure's middle along the bridge
DEPTH = 57                      # the chasm's depth under the den's floor course


def h(*a):
    v = 2166136261
    for n in a:
        v = ((v ^ (n & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    return v


def _lattice(ix, iy, iz, salt):
    return (h(ix, iy, iz, salt) % 10007) / 10007.0


def noise(x, y, z, cell=6.0, salt=17):
    """Trilinear value noise in [0, 1], deterministic (no RNG, no float order beyond the obvious)."""
    fx, fy, fz = x / cell, y / cell, z / cell
    ix, iy, iz = math.floor(fx), math.floor(fy), math.floor(fz)
    tx, ty, tz = fx - ix, fy - iy, fz - iz
    tx, ty, tz = tx * tx * (3 - 2 * tx), ty * ty * (3 - 2 * ty), tz * tz * (3 - 2 * tz)
    acc = 0.0
    for dx in (0, 1):
        for dy in (0, 1):
            for dz in (0, 1):
                w = (tx if dx else 1 - tx) * (ty if dy else 1 - ty) * (tz if dz else 1 - tz)
                acc += w * _lattice(ix + dx, iy + dy, iz + dz, salt)
    return acc


def _ell(x, y, z, c, r):
    return ((x - c[0]) / r[0]) ** 2 + ((y - c[1]) / r[1]) ** 2 + ((z - c[2]) / r[2]) ** 2


# the hollows, den frame (y may be negative: the chasm)
HOLLOWS = [
    ((27.0, 14.0, 38.0), (24.0, 30.0, 44.0)),    # the great hall over the bridge
    ((0.0, -6.0, 25.0), (24.0, 52.0, 52.0)),     # the hall the figure stands in, west of the bridge
    ((30.0, 5.0, 74.0), (10.0, 7.0, 9.0)),       # the tunnel's ledge
    ((31.0, 8.0, 8.0), (16.0, 11.0, 10.0)),      # the den's bay
    ((19.0, -20.0, 44.0), (17.0, 25.0, 31.0)),   # the chasm under the bridge and the statue
    ((52.0, 14.0, 40.0), (20.0, 20.0, 38.0)),    # the hall's far side, east of the bridge, where the eye stands
]


def hollow(x, y, z):
    """True where the cave is air (before the ledges, the bridge and the statue are laid)."""
    best = min(_ell(x, y, z, c, r) for c, r in HOLLOWS)
    n = noise(x, y, z, 7.0, 17) - 0.5 + 0.5 * (noise(x, y, z, 3.0, 29) - 0.5)
    return best + 0.55 * n < 1.0


def _seg_dist(p, a, b):
    ab = [b[i] - a[i] for i in range(3)]
    ap = [p[i] - a[i] for i in range(3)]
    L = sum(v * v for v in ab)
    t = 0.0 if L == 0 else max(0.0, min(1.0, sum(ap[i] * ab[i] for i in range(3)) / L))
    q = [a[i] + ab[i] * t for i in range(3)]
    return math.sqrt(sum((p[i] - q[i]) ** 2 for i in range(3))), t


def _tri_z_span(root, a, b, z):
    """The y span (lo, hi) of the triangle root-a-b cut at z (in the yz plane), or None."""
    pts = [root, a, b]
    ys = []
    for i in range(3):
        p, q = pts[i], pts[(i + 1) % 3]
        if (p[2] - z) * (q[2] - z) <= 0 and p[2] != q[2]:
            t = (z - p[2]) / (q[2] - p[2])
            ys.append(p[1] + t * (q[1] - p[1]))
    if len(ys) < 2:
        return None
    return min(ys), max(ys)


# the stone Cthulhu: `prefab/foot-of-the-mountain-den-thing` (`den_thing.py`, the reference level's
# figure turned to face the bridge), stamped by `batch/the-thing` with its piece's corner here, in
# the den's frame (u the den's course): its front stands back from the bridge's rail across a dark gap
THING_AT = (-18, -56, -20)


def _thing_cells():
    import json as _json
    import os as _os
    form = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "../../forms/den-thing.json")))
    cells = set()
    for sd in form["solids"]:
        if sd["shape"] == "box":
            lo, hi = sd["from"], sd["to"]
            test = lambda p, lo=lo, hi=hi: all(lo[i] <= p[i] <= hi[i] for i in range(3))  # noqa: E731
            r = 0.0
        elif sd["shape"] == "capsule":
            a, b, ra, rb = sd["from"], sd["to"], sd["radius_from"], sd["radius_to"]
            def test(p, a=a, b=b, ra=ra, rb=rb):
                d, t = _seg_dist(p, a, b)
                return d <= ra + (rb - ra) * t
            lo = [min(a[i], b[i]) - max(ra, rb) for i in range(3)]
            hi = [max(a[i], b[i]) + max(ra, rb) for i in range(3)]
        else:
            c, rr = sd["centre"], sd["radii"]
            test = lambda p, c=c, rr=rr: _ell(p[0], p[1], p[2], c, rr) <= 1.0  # noqa: E731
            lo = [c[i] - rr[i] for i in range(3)]
            hi = [c[i] + rr[i] for i in range(3)]
        hit = set()
        for bx in range(int(math.floor(lo[0])) - 1, int(math.ceil(hi[0])) + 1):
            for by in range(int(math.floor(lo[1])) - 1, int(math.ceil(hi[1])) + 1):
                for bz in range(int(math.floor(lo[2])) - 1, int(math.ceil(hi[2])) + 1):
                    if test((bx + 0.5, by + 0.5, bz + 0.5)):
                        hit.add((bx, by, bz))
        if sd["op"] == "add":
            cells |= hit
        else:
            cells -= hit
    x0, u0, z0 = THING_AT
    # piece y = body y + 1 (the apron is the piece's first course), so body y 0 is u -42
    return {(x0 + bx, u0 + 1 + by, z0 + bz) for (bx, by, bz) in cells}


_NEAR = None


def statue_near(x, y, z):
    """Within two cells of the figure: the air the cave keeps round it."""
    global _NEAR
    if _NEAR is None:
        _NEAR = set()
        for (a, b, c) in _thing_cells():
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    for dz in range(-2, 3):
                        _NEAR.add((a + dx, b + dy, c + dz))
    return (x, y, z) in _NEAR


# ---- the walked ground ----
def north_ledge(x, z):
    """The den's ledge: z 1..16 between the walls, its edge over the chasm broken."""
    edge = NORTH_Z1 - (1 if h(x, 41) % 3 == 0 and not 25 <= x <= 33 else 0)
    return 17 <= x <= 45 and 1 <= z <= edge


def south_ledge(x, z):
    edge = SOUTH_Z0 + (1 if h(x, 43) % 3 == 0 and not 25 <= x <= 33 else 0)
    return 23 <= x <= 36 and edge <= z <= 78


def deck(x, z):
    return x in BRIDGE_X and BZ0 <= z <= BZ1


def sag(z):
    """The bridge's deck at row z, as a rope bridge sags: (the deck block's course, the block, the
    walk plane). Planks level with the ledges for six rows from each end, a half step down for
    four, then planks a course lower across the middle. Courses are the den's: 0 the ledges' top."""
    m = min(z - BZ0, BZ1 - z)
    if m <= 5:
        return 0, "minecraft:spruce_planks" if z % 2 else "minecraft:oak_planks", 1
    if m <= 9:
        return 0, "minecraft:spruce_slab[type=bottom,waterlogged=false]", 1
    return -1, "minecraft:spruce_planks" if z % 2 else "minecraft:oak_planks", 0


def ground(x, z):
    return north_ledge(x, z) or south_ledge(x, z) or deck(x, z) or (x in RAIL_X and BZ0 <= z <= BZ1)


def kept_clear(x, y, z):
    """Air the cave must have whatever the noise says: over the walked ground (four courses), the
    bridge's corridor, and the statue with two cells round it."""
    if y >= 0 and y <= 5 and (ground(x, z) or (26 <= x <= 32 and BZ0 - 1 <= z <= BZ1 + 1)):
        return True
    # a moat of air six cells either side of the bridge, from under its deck to over its lanterns:
    # no shelf of rock within a jump of its rails, cable or post lanterns
    if -3 <= y <= 9 and 20 <= x <= 38 and BZ0 - 1 <= z <= BZ1 + 1 and not ground(x, z):
        return True
    # the figure's room, two cells round it, from the chasm's floor to its crown (the chasm holds
    # the sea's water, authored by `den-chasm.py`, so the room cut under the sea's level is water)
    if y > -DEPTH and XMIN <= x <= 27 and statue_near(x, y, z):
        return True
    return False


# the cells of other places over the den (the mountain road's switchbacks run over its roof), in
# these coordinates: `den.py` reads them from the den's allocation (`set_overhead`); the rock stands
# OVERHEAD_MARGIN thick under them, so the road keeps a floor of rock and nothing hangs from it
OVERHEAD = set()
OVERHEAD_MARGIN = 3


def set_overhead(cells):
    OVERHEAD.clear()
    for (x, u, z) in cells:
        for dy in range(OVERHEAD_MARGIN + 1):
            for dx in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    OVERHEAD.add((x + dx, u - dy, z + dz))


def rock_at(x, y, z):
    """Rock in the den frame (y 0..LID) or in the chasm (y < 0)."""
    if (x, y, z) in OVERHEAD:
        return True
    if y <= -DEPTH:      # the chasm's floor course is whole rock: under it is the sea's
        return True
    if x <= XMIN or x >= EX - 1 or z <= ZMIN or z >= EZ - 2 or y >= LID:
        return not (y >= 1 and y <= 3 and x in BRIDGE_X and z >= EZ - 2)   # the tunnel's mouth
    if z <= 0 and x >= 18:
        return True          # north of the den's ledge the rock is whole: no shelf to climb onto
    if kept_clear(x, y, z):
        return False
    return not hollow(x, y, z)


# ---- the den as cells ----
# the cave is dark rock, so the figure is the one pale thing in it
ROCKS = ["minecraft:deepslate[axis=y]", "minecraft:deepslate[axis=y]", "minecraft:cobbled_deepslate",
         "minecraft:tuff", "minecraft:cobbled_deepslate", "minecraft:deepslate_bricks"]
LEDGE = ["minecraft:polished_deepslate", "minecraft:tuff", "minecraft:cobbled_deepslate", "minecraft:deepslate_tiles"]
AIR = "~air"
FENCE = "minecraft:oak_fence"
POST = "minecraft:spruce_fence"
LANTERN = "minecraft:lantern[hanging=false,waterlogged=false]"
HANGING = "minecraft:lantern[hanging=true,waterlogged=false]"
CHAIN_Y = "minecraft:iron_chain[axis=y,waterlogged=false]"
CHAIN_Z = "minecraft:iron_chain[axis=z,waterlogged=false]"
FACES = (("west", -1, 0, 0), ("east", 1, 0, 0), ("north", 0, 0, -1), ("south", 0, 0, 1), ("up", 0, 1, 0), ("down", 0, -1, 0))


def rock_block(x, y, z):
    return ROCKS[h(x, y, z, 7) % len(ROCKS)]


def lichen(face):
    props = {f: "false" for f, *_ in FACES}
    props[face] = "true"
    return "minecraft:glow_lichen[" + ",".join(f"{k}={props[k]}" for k in ("down", "east", "north", "south", "up")) + \
        ",waterlogged=false," + f"west={props['west']}]"


def lichen_cells(lo_y, hi_y, solid, open_cell, salt):
    """Glow lichen in clusters on the rock faces that air meets, the clusters where a seeded noise
    is high: {cell: state}. `solid(x, y, z)` and `open_cell(x, y, z)` read the shape."""
    out = {}
    for x in range(XMIN + 1, EX - 1):
        for z in range(ZMIN + 1, EZ - 2):
            for y in range(lo_y, hi_y + 1):
                if not open_cell(x, y, z) or noise(x, y, z, 5.0, salt) < 0.66 or h(x, y, z, salt) % 3:
                    continue
                for f, dx, dy, dz in FACES:
                    if solid(x + dx, y + dy, z + dz):
                        out[(x, y, z)] = lichen(f)
                        break
    return out


# (x, z, the lantern's course): in front of each wing, over the hood and by the raised hand, each
# clear of the figure's body to the roof: a white figure in a dark cave is lit, or it reads as rock
FIGURE_LANTERNS = ((-11, -4, 22), (-11, 54, 22), (-11, -4, 10), (-11, 54, 10), (-11, 6, 30), (-11, 44, 30),
                   (-5, 25, 35), (-4, 19, 33), (-4, 31, 33), (2, 12, 24), (2, 38, 24), (8, 8, 28), (8, 42, 28), (13, 0, 16), (14, 50, 10))


def den_cells():
    """The den's cells, keyed by (x, u, z): u is the den's course, 0 the ledges' top course (world
    y 71), -1 the den's floor course under the bridge's sagging middle (world y 70), LID its lid."""
    c = {}
    for x in range(XMIN, EX):
        for z in range(ZMIN, EZ - 1):
            for y in range(-1, LID + 1):
                if y <= 0 and (x in BRIDGE_X or x in RAIL_X) and BZ0 <= z <= BZ1:
                    du, blk, _ = sag(z)
                    c[(x, y, z)] = blk if y == du else AIR
                elif y == 0 and (north_ledge(x, z) or south_ledge(x, z)):
                    c[(x, 0, z)] = LEDGE[h(x, z, 5) % len(LEDGE)]
                elif y == -1 and (north_ledge(x, z) or south_ledge(x, z)):
                    c[(x, -1, z)] = rock_block(x, -1, z)
                elif y <= 0 and rock_at(x, y, z):
                    c[(x, y, z)] = rock_block(x, y, z)
                elif y <= 0:
                    c[(x, y, z)] = AIR             # open over the chasm
                elif rock_at(x, y, z):
                    c[(x, y, z)] = rock_block(x, y, z)
                else:
                    c[(x, y, z)] = AIR

    def solid(x, y, z):
        return c.get((x, y, z), AIR) != AIR and c.get((x, y, z)) is not None

    # just off the walked ground, where the rock does not rise as a wall, the ground falls away
    # into the chasm: no shelf a course down stands beside a ledge for a body to drop onto
    for x in range(XMIN, EX):
        for z in range(ZMIN, EZ - 1):
            if ground(x, z) or c.get((x, 0, z)) != AIR:
                continue
            if any(ground(x + dx, z + dz) for dx in (-1, 0, 1) for dz in (-1, 0, 1)):
                c[(x, -1, z)] = AIR

    # the rails: one fence high along the bridge, on its sagging deck, and along every ledge's
    # edge over the chasm
    for z in range(BZ0, BZ1 + 1):
        du, _, w = sag(z)
        for x in RAIL_X:
            c[(x, du + 1, z)] = FENCE
    for x in range(XMIN, EX):
        for z in range(ZMIN, EZ - 1):
            if not (north_ledge(x, z) or south_ledge(x, z)) or c.get((x, 1, z)) != AIR:
                continue
            # (a diagonal drop too: a body slips off a ledge's corner between a rail and a wall)
            if any(c.get((x + dx, 0, z + dz)) == AIR and not deck(x + dx, z + dz)
                   for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1))):
                c[(x, 1, z)] = FENCE
    # where a ledge meets the cave's rock, the rock stands eight high, so no body climbs off the
    # walked ground onto the rock beyond it, from the floor or from anything standing on it
    for x in range(XMIN, EX):
        for z in range(ZMIN, EZ - 1):
            if not ground(x, z):
                continue
            for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
                nx, nz = x + dx, z + dz
                if ground(nx, nz) or not (XMIN <= nx < EX and ZMIN <= nz < EZ - 1) or c.get((nx, 0, nz)) == AIR:
                    continue
                if nz >= EZ - 2 and nx in BRIDGE_X:
                    continue                       # the tunnel's mouth
                for y in range(1, 9):
                    c[(nx, y, nz)] = rock_block(nx, y, nz)
    # the rails turn the corners where the bridge leaves each ledge
    for x in RAIL_X:
        for z in (BZ0 - 1, BZ1 + 1):
            if c.get((x, 1, z)) == AIR:
                c[(x, 1, z)] = FENCE
    # the bridge's cable: a chain along each side two courses over the rail, sagging with the
    # deck, a hanger down to the rail every third row and a lantern hung under it every sixth;
    # a post at each end and every ninth row, a lantern on it over the cable
    for z in range(BZ0, BZ1 + 1):
        du, _, w = sag(z)
        cable = du + 3
        for x in RAIL_X:
            k = z - BZ0
            if z in (BZ0, BZ1) or k % 9 == 0:
                for y in range(du + 1, cable + 1):
                    c[(x, y, z)] = POST
                c[(x, cable + 1, z)] = LANTERN
                continue
            c[(x, cable, z)] = CHAIN_Z
            if k % 6 == 3 and (x == RAIL_X[0]) == ((k // 6) % 2 == 0):
                c[(x, cable, z)] = CHAIN_Y
                c[(x, cable - 1, z)] = HANGING
            elif k % 3 == 0:
                c[(x, cable - 1, z)] = CHAIN_Y
    # the den on the far ledge
    put = lambda x, y, z, b: c.__setitem__((x, y, z), b)  # noqa: E731
    # the den gathered at the bridge's far end, where the bridge comes onto the ledge: the red bed,
    # the keepsakes on a run of bookshelves, the dragon's head, the egg in its case, the conduit
    # (a bed's top is a step: from it a body jumps onto a one-high rail, so it stands six cells
    # back from the ledge's edge)
    put(34, 1, 8, "minecraft:red_bed[facing=north,occupied=false,part=head]")
    put(34, 1, 9, "minecraft:red_bed[facing=north,occupied=false,part=foot]")
    for (x, z) in ((33, 8), (33, 9), (35, 8), (35, 9), (33, 10), (34, 10), (35, 10)):
        put(x, 1, z, "minecraft:red_carpet")
    # nothing a body can stand on within reach of a rail: the rails are one fence high, and a
    # block beside one is a step over it
    put(37, 1, 9, "minecraft:dragon_head[powered=false,rotation=4]")
    # the dragon's egg on a pedestal under a glass case
    put(43, 1, 4, "minecraft:chiseled_stone_bricks")
    for (x, y, z) in ((42, 2, 4), (44, 2, 4), (43, 2, 3), (43, 2, 5), (43, 3, 4)):
        put(x, y, z, "minecraft:glass")
    put(43, 2, 4, "minecraft:dragon_egg")
    keep = ["minecraft:amethyst_cluster[facing=up,waterlogged=false]", "minecraft:potted_cactus",
            "minecraft:potted_cherry_sapling", "minecraft:sculk", "minecraft:potted_mangrove_propagule",
            "minecraft:sea_lantern", "minecraft:potted_bamboo", "minecraft:blue_ice", "minecraft:potted_dead_bush",
            "minecraft:potted_crimson_fungus", "minecraft:end_rod[facing=up]"]
    for i, x in enumerate(range(37, 44)):
        put(x, 1, 7, "minecraft:bookshelf")
        put(x, 2, 7, keep[i])
    for i, x in enumerate(range(37, 41)):
        put(x, 1, 3, "minecraft:bookshelf")
        put(x, 2, 3, keep[7 + i])
    # and at the shelf's end, the conduit out of the sea's drowned temple
    put(41, 1, 3, "minecraft:bookshelf")
    put(41, 2, 3, "minecraft:conduit[waterlogged=false]")
    put(44, 1, 6, "minecraft:chest[facing=west,type=single,waterlogged=false]")
    put(31, 2, 1, "minecraft:spruce_wall_sign[facing=south,waterlogged=false]")
    for (x, z) in ((25, 2), (36, 5)):
        put(x, 1, z, LANTERN)
    # lanterns hung on chains from the roof over the den and the tunnel's ledge
    for (x, z, low_y) in ((29, 9, 5), (39, 10, 5), (21, 11, 5), (33, 4, 5), (31, 12, 4), (36, 12, 4), (26, 75, 4), (33, 75, 4), (30, 74, 6),
                            (47, 60, 4), (49, 65, 4), (45, 69, 4), (54, 55, 3), (8, 61, 4), (52, 14, 4), (50, 45, 4), (56, 48, 4), (20, 74, 13)):
        y = low_y
        while y < LID and c.get((x, y, z)) == AIR:
            y += 1
        if y >= LID or y - low_y < 1:
            continue
        put(x, low_y, z, HANGING)
        for yy in range(low_y + 1, y):
            put(x, yy, z, CHAIN_Y)
    # lanterns hung on long chains from the roof over the figure's shoulders and wings, behind it
    # and in the dark between it and the bridge, clear of its body: the figure's ledges a fall can
    # land on are lit (a lantern under the den's floor course is the chasm's, `den-chasm.py`)
    for (x, z, low_y) in FIGURE_LANTERNS:
        y = max(low_y, -1)
        top = y
        while top < LID and c.get((x, top, z)) == AIR:
            top += 1
        if low_y >= -1:
            put(x, low_y, z, HANGING)
        for yy in range(y if low_y < -1 else low_y + 1, top):
            put(x, yy, z, CHAIN_Y)
    # crystals in the walls: clusters of sea lantern set into the rock's face where it meets the
    # air of the hall, cold blue-white, glow lichen round each
    crystals = []
    for x in range(XMIN + 1, EX - 1):
        for z in range(ZMIN + 1, EZ - 2):
            for y in range(2, LID - 2):
                if c.get((x, y, z)) not in ROCKS or ground(x, z):
                    continue
                if not any(c.get((x + dx, y + dy, z + dz)) == AIR for _, dx, dy, dz in FACES):
                    continue
                if h(x, y, z, 91) % 23 or noise(x, y, z, 6.0, 93) < 0.55:
                    continue
                if any(abs(x - a) + abs(y - b) + abs(z - d) < 6 for a, b, d in crystals):
                    continue
                crystals.append((x, y, z))
                c[(x, y, z)] = "minecraft:sea_lantern"
    # glow lichen on the rock, never on the walked ground or over it within reach
    walked = lambda x, z: ground(x, z)  # noqa: E731
    near_crystal = lambda x, y, z: any(abs(x - a) + abs(y - b) + abs(z - d) <= 3 for a, b, d in crystals)  # noqa: E731
    for (a, b, d) in crystals:
        for _, dx, dy, dz in FACES:
            k = (a + dx, b + dy, d + dz)
            if c.get(k) != AIR or (walked(k[0], k[2]) and k[1] <= 4):
                continue
            for f, ex_, ey_, ez_ in FACES:
                if solid(k[0] + ex_, k[1] + ey_, k[2] + ez_) and c.get((k[0] + ex_, k[1] + ey_, k[2] + ez_)) in ROCKS:
                    c[k] = lichen(f)
                    break
    # dripstone hanging from the roof
    for x in range(XMIN + 1, EX - 1):
        for z in range(ZMIN + 1, EZ - 2):
            for y in range(12, LID):
                if c.get((x, y, z)) == AIR and c.get((x, y + 1, z), AIR) in ROCKS and h(x, y, z, 61) % 13 == 0:
                    c[(x, y, z)] = "minecraft:pointed_dripstone[thickness=tip,vertical_direction=down,waterlogged=false]"
    return c


def den_marks():
    """The den's marks, (x, z, facing, u): u the course of the cell named (the ledges' walk plane
    is u 1)."""
    return {"cat-bed": (34, 9, "south", 1), "den-chest": (44, 6, "west", 1), "den-sign": (31, 1, "south", 2),
            "node-cat-den": (30, 13, "north", 1)}
