"""The cat's den and its chasm, as one shape: read by `den.py` (the den, a place) and by
`den-chasm.py` (the statue and the chasm under the den, a piece the world edits stamp).

Den frame: x 0..48 (world 106..154), y 0..42 (world 71..113; y 0 the floor course, y 1 the walk
plane of the ledges and the bridge, y 42 the lid), z 0..78 (world 98..176). The chasm under the den
is the same x and z, y -43..-1 (world 28..70). The tunnel comes in at the south face (z 78),
x 28..30; the bridge runs north from it across the chasm to the den's ledge; the statue stands
west of the bridge, facing it, its wings spread along the bridge.

The cave is a union of ellipsoids carved out of rock, its walls broken by a seeded value noise (the
1.18+ noise caves' look: no straight wall, overhangs and knuckles at every height), with the
walked ledges, the bridge's corridor and the statue (and a margin round it) kept clear.
"""
import math

EX, EY, EZ = 49, 43, 80
LID = 42
BRIDGE_X = (28, 29, 30)
RAIL_X = (27, 31)
BZ0, BZ1 = 17, 71               # the bridge's deck, south of the den's ledge, north of the tunnel's
SOUTH_Z0 = 72                   # the tunnel's ledge, z 72..78
NORTH_Z1 = 16                   # the den's ledge, z 1..16
STATUE_Z = 44                   # the statue's middle, level with the bridge's middle
DEPTH = 43                      # the chasm's depth under the den's floor course


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
    ((27.0, 16.0, 41.0), (21.0, 26.0, 40.0)),    # the great hall over the bridge
    ((13.0, 18.0, 44.0), (14.0, 26.0, 33.0)),    # the alcove the statue stands in
    ((30.0, 5.0, 74.0), (10.0, 7.0, 9.0)),       # the tunnel's ledge
    ((31.0, 8.0, 8.0), (16.0, 11.0, 10.0)),      # the den's bay
    ((19.0, -20.0, 44.0), (17.0, 25.0, 31.0)),   # the chasm under the bridge and the statue
]


def hollow(x, y, z):
    """True where the cave is air (before the ledges, the bridge and the statue are laid)."""
    best = min(_ell(x, y, z, c, r) for c, r in HOLLOWS)
    n = noise(x, y, z, 7.0, 17) - 0.5 + 0.5 * (noise(x, y, z, 3.0, 29) - 0.5)
    return best + 0.55 * n < 1.0


# ---- the statue, in the den frame ----
def _cap(a, b, ra, rb):
    return ("capsule", a, b, ra, rb)


def statue_parts():
    """The statue as (kind, ...) primitives in den-frame coordinates: a cephalopod head bent
    forward with no neck, a beard of feelers, clawed arms, long bat wings spread along the bridge,
    the body falling away into the chasm (after Lovecraft's description as `references/the-thing-
    beyond-the-fog/HOW-IT-IS-BUILT.md` cites it, drawn to `design/reference/cat-den`)."""
    Z = STATUE_Z
    P = []
    # the body, sinking into the chasm
    P.append(("body", _cap((12, -43, Z), (13, -8, Z), 8.5, 8.0)))
    P.append(("body", _cap((13, -8, Z), (13, 8, Z), 8.0, 7.5)))
    for dz, dx in ((-6, 3), (6, 3), (-3, 5), (3, 5), (0, 6)):
        P.append(("body", _cap((12 + dx, -43, Z + dz), (13 + dx // 2, 4, Z + dz), 2.2, 1.6)))   # folds of the robe
    # shoulders and the mantle of the head, bent forward
    P.append(("head", ("ellipsoid", (13, 8, Z), (7.0, 6.0, 13.0))))
    P.append(("head", ("ellipsoid", (15, 24, Z), (8.0, 13.0, 10.0))))
    P.append(("head", ("ellipsoid", (19, 22, Z), (3.5, 4.0, 8.0))))     # the brow
    # the beard of feelers, alternate ones forward, the middle ones longest
    for i, dz in enumerate((-8, -6, -4, -2, 0, 2, 4, 6, 8)):
        fwd = 1.5 if i % 2 else 0.0
        drop = 14 - abs(dz)
        P.append(("feeler", _cap((20.0, 18.0, Z + dz * 0.8), (21.5 + fwd, 18.0 - drop, Z + dz * 1.15), 1.7, 0.7)))
    # the arms, clawed hands held before the chest under the beard
    for s in (-1, 1):
        P.append(("body", _cap((13, 8, Z + 12 * s), (19, -2, Z + 13 * s), 3.2, 2.6)))
        P.append(("body", _cap((19, -2, Z + 13 * s), (22, -10, Z + 8 * s), 2.6, 2.2)))
        for f in (-2, 0, 2):
            P.append(("feeler", _cap((22, -10, Z + 8 * s + f), (24, -14, Z + 7 * s + f), 1.0, 0.5)))
    # the wings: an arm from the shoulder blade to the wrist, four fingers to the tips, a membrane
    # between them, scalloped
    for s in (-1, 1):
        root = (8.0, 12.0, Z + 7 * s)
        wrist = (7.0, 33.0, Z + 21 * s)
        tips = [(6.0, 38.0, Z + 27 * s), (6.0, 30.0, Z + 27 * s), (6.0, 20.0, Z + 26 * s), (6.0, 9.0, Z + 24 * s)]
        P.append(("bone", _cap(root, wrist, 2.2, 1.4)))
        for t in tips:
            P.append(("bone", _cap(wrist, t, 1.2, 0.6)))
        P.append(("bone", _cap(root, (7.0, 2.0, Z + 18 * s), 1.6, 0.6)))
        fan = [wrist] + tips + [(7.0, 2.0, Z + 18 * s)]
        P.append(("membrane", ("fan", root, wrist, tips + [(7.0, 2.0, Z + 18 * s)], s)))
    return P


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


def membrane_boxes():
    """The wings' membranes as thin boxes, one per column of z: the fan of triangles from the
    shoulder blade over the wrist and between the fingers, its lower edge scalloped between the
    tips. Den frame, box corners [x0, y0, z0], [x1, y1, z1]."""
    out = []
    for kind, prim in statue_parts():
        if kind != "membrane":
            continue
        _, root, wrist, tips, s = prim
        ring = [wrist] + tips
        zs = [p[2] for p in ring] + [root[2]]
        for z in range(int(min(zs)), int(max(zs)) + 1):
            zc = z + 0.5
            lo, hi = None, None
            for i in range(len(ring) - 1):
                sp = _tri_z_span(root, ring[i], ring[i + 1], zc)
                if sp is None:
                    continue
                a, b = sp
                # the scallop: the edge between two tips sags toward the root
                if i >= 1:
                    mid = (ring[i][2] + ring[i + 1][2]) / 2.0
                    w = abs(ring[i][2] - ring[i + 1][2]) / 2.0 + 0.01
                    a = a + 2.0 * max(0.0, 1.0 - abs(zc - mid) / w)
                lo = a if lo is None else min(lo, a)
                hi = b if hi is None else max(hi, b)
            if lo is None or hi - lo < 1.0:
                continue
            out.append(([5.5, round(lo, 2), z], [7.5, round(hi, 2), z + 1]))
    return out


def statue_occupied(x, y, z, margin=0.0):
    """Whether a cell's centre lies in the statue grown by `margin` (den frame)."""
    p = (x + 0.5, y + 0.5, z + 0.5)
    for kind, prim in statue_parts():
        if prim[0] == "capsule":
            _, a, b, ra, rb = prim
            d, t = _seg_dist(p, a, b)
            if d <= ra + (rb - ra) * t + margin:
                return True
        elif prim[0] == "ellipsoid":
            _, c, r = prim
            if _ell(p[0], p[1], p[2], c, (r[0] + margin, r[1] + margin, r[2] + margin)) <= 1.0:
                return True
    for (a, b) in membrane_boxes():
        if a[0] - margin <= p[0] <= b[0] + margin and a[1] - margin <= p[1] <= b[1] + margin and a[2] - margin <= p[2] <= b[2] + margin:
            return True
    return False


_STATUE_CACHE = {}


def statue_near(x, y, z):
    k = (x, y, z)
    if k not in _STATUE_CACHE:
        _STATUE_CACHE[k] = statue_occupied(x, y, z, margin=2.0)
    return _STATUE_CACHE[k]


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


def ground(x, z):
    return north_ledge(x, z) or south_ledge(x, z) or deck(x, z) or (x in RAIL_X and BZ0 <= z <= BZ1)


def kept_clear(x, y, z):
    """Air the cave must have whatever the noise says: over the walked ground (four courses), the
    bridge's corridor, and the statue with two cells round it."""
    if y >= 1 and y <= 5 and (ground(x, z) or (26 <= x <= 32 and BZ0 - 1 <= z <= BZ1 + 1)):
        return True
    if y >= -DEPTH and 0 <= x <= 27 and 10 <= z <= 78 and statue_near(x, y, z):
        return True
    return False


def rock_at(x, y, z):
    """Rock in the den frame (y 0..LID) or in the chasm (y < 0)."""
    if x <= 0 or x >= EX - 1 or z <= 0 or z >= EZ - 2 or y >= LID:
        return not (y >= 1 and y <= 3 and x in BRIDGE_X and z >= EZ - 2)   # the tunnel's mouth
    if kept_clear(x, y, z):
        return False
    return not hollow(x, y, z)


# ---- the den as cells ----
ROCKS = ["minecraft:stone", "minecraft:stone", "minecraft:tuff", "minecraft:andesite",
         "minecraft:deepslate[axis=y]", "minecraft:cobbled_deepslate", "minecraft:dripstone_block"]
LEDGE = ["minecraft:stone", "minecraft:cobblestone", "minecraft:tuff", "minecraft:andesite"]
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
    for x in range(1, EX - 1):
        for z in range(1, EZ - 2):
            for y in range(lo_y, hi_y + 1):
                if not open_cell(x, y, z) or noise(x, y, z, 5.0, salt) < 0.66 or h(x, y, z, salt) % 3:
                    continue
                for f, dx, dy, dz in FACES:
                    if solid(x + dx, y + dy, z + dz):
                        out[(x, y, z)] = lichen(f)
                        break
    return out


def den_cells(ex, ey, ez):
    assert (ex, ey, ez) == (EX, EY, EZ), (ex, ey, ez)
    c = {}
    for x in range(EX):
        for z in range(EZ - 1):
            for y in range(0, LID + 1):
                if y == 0:
                    if deck(x, z) or (x in RAIL_X and BZ0 <= z <= BZ1):
                        c[(x, 0, z)] = "minecraft:spruce_planks" if z % 2 else "minecraft:oak_planks"
                    elif north_ledge(x, z) or south_ledge(x, z):
                        c[(x, 0, z)] = LEDGE[h(x, z, 5) % len(LEDGE)]
                    elif rock_at(x, 0, z):
                        c[(x, 0, z)] = rock_block(x, 0, z)
                    else:
                        c[(x, 0, z)] = AIR             # open over the chasm
                elif rock_at(x, y, z):
                    c[(x, y, z)] = rock_block(x, y, z)
                else:
                    c[(x, y, z)] = AIR

    def solid(x, y, z):
        return c.get((x, y, z), AIR) != AIR and c.get((x, y, z)) is not None

    # the rails: one fence high along the bridge and every ledge's edge over the chasm
    for z in range(BZ0, BZ1 + 1):
        for x in RAIL_X:
            c[(x, 1, z)] = FENCE
    for x in range(EX):
        for z in range(EZ - 1):
            if not (north_ledge(x, z) or south_ledge(x, z)) or c.get((x, 1, z)) != AIR:
                continue
            if any(c.get((x + dx, 0, z + dz)) == AIR for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                c[(x, 1, z)] = FENCE
    # where a ledge meets the cave's rock, the rock stands three high, so no body climbs off the
    # walked ground onto the rock beyond it
    for x in range(EX):
        for z in range(EZ - 1):
            if not ground(x, z):
                continue
            for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
                nx, nz = x + dx, z + dz
                if ground(nx, nz) or not (0 <= nx < EX and 0 <= nz < EZ - 1) or c.get((nx, 0, nz)) == AIR:
                    continue
                if nz >= EZ - 2 and nx in BRIDGE_X:
                    continue                       # the tunnel's mouth
                for y in (1, 2, 3):
                    c[(nx, y, nz)] = rock_block(nx, y, nz)
    # the rails turn the corners where the bridge leaves each ledge
    for x in RAIL_X:
        for z in (BZ0 - 1, BZ1 + 1):
            if c.get((x, 1, z)) == AIR:
                c[(x, 1, z)] = FENCE
    # the bridge's posts at both ends, lanterns on them; a cable of chain along each side over the
    # rail, hangers down to it, and a lantern hung under the cable every six cells
    for z in (BZ0, BZ1):
        for x in RAIL_X:
            for y in (1, 2, 3):
                c[(x, y, z)] = POST
            c[(x, 4, z)] = LANTERN
    for z in range(BZ0 + 1, BZ1):
        for x in RAIL_X:
            c[(x, 3, z)] = CHAIN_Z
            k = z - BZ0
            if k % 6 == 3 and (x == RAIL_X[0]) == ((k // 6) % 2 == 0):
                c[(x, 3, z)] = CHAIN_Y          # the hanger the lantern hangs from
                c[(x, 2, z)] = HANGING
            elif k % 3 == 0:
                c[(x, 2, z)] = CHAIN_Y
    # the den on the far ledge
    put = lambda x, y, z, b: c.__setitem__((x, y, z), b)  # noqa: E731
    put(34, 1, 5, "minecraft:red_bed[facing=north,occupied=false,part=head]")
    put(34, 1, 6, "minecraft:red_bed[facing=north,occupied=false,part=foot]")
    for (x, z) in ((33, 5), (33, 6), (35, 5), (35, 6), (33, 7), (34, 7), (35, 7)):
        put(x, 1, z, "minecraft:red_carpet")
    # keepsakes of the End on a pedestal: an end rod on a purpur pillar (the dragon's egg the
    # reference shows is a block the building palette refuses, DW0730)
    put(24, 1, 4, "minecraft:purpur_pillar[axis=y]")
    put(24, 2, 4, "minecraft:end_rod[facing=up]")
    # the dragon's head on the wall over the bed
    put(34, 3, 1, "minecraft:dragon_wall_head[facing=south,powered=false]")
    # shelves of keepsakes from every corner of the world along the back wall
    for x in range(37, 44):
        put(x, 1, 1, "minecraft:bookshelf")
        put(x, 3, 1, "minecraft:dark_oak_slab[type=top,waterlogged=false]")
    low = ["minecraft:amethyst_cluster[facing=up,waterlogged=false]", "minecraft:potted_cactus",
           "minecraft:potted_cherry_sapling", "minecraft:sculk",
           "minecraft:potted_mangrove_propagule", "minecraft:sea_lantern", "minecraft:potted_bamboo"]
    high = ["minecraft:blue_ice", "minecraft:potted_dead_bush", "minecraft:potted_crimson_fungus",
            "minecraft:potted_brown_mushroom", "minecraft:potted_azalea_bush", "minecraft:potted_warped_fungus",
            "minecraft:skeleton_skull[powered=false,rotation=8]"]
    for i, x in enumerate(range(37, 44)):
        put(x, 2, 1, low[i])
        put(x, 4, 1, high[i])
    put(44, 1, 3, "minecraft:chest[facing=west,type=single,waterlogged=false]")
    put(31, 2, 1, "minecraft:spruce_wall_sign[facing=south,waterlogged=false]")
    for (x, z) in ((22, 2), (43, 7), (27, 2)):
        put(x, 1, z, LANTERN)
    # lanterns hung on chains from the roof over the den and the tunnel's ledge
    for (x, z, low_y) in ((29, 9, 5), (39, 10, 5), (21, 11, 5), (26, 75, 4), (33, 75, 4)):
        y = low_y
        while y < LID and c.get((x, y, z)) == AIR:
            y += 1
        if y >= LID or y - low_y < 1:
            continue
        put(x, low_y, z, HANGING)
        for yy in range(low_y + 1, y):
            put(x, yy, z, CHAIN_Y)
    # glow lichen on the rock, never on the walked ground or over it within reach
    walked = lambda x, z: ground(x, z)  # noqa: E731
    lich = lichen_cells(1, LID - 1, solid,
                        lambda x, y, z: c.get((x, y, z)) == AIR and not (walked(x, z) and y <= 4), salt=51)
    for k, v in lich.items():
        c[k] = v
    # dripstone hanging from the roof
    for x in range(1, EX - 1):
        for z in range(1, EZ - 2):
            for y in range(12, LID):
                if c.get((x, y, z)) == AIR and c.get((x, y + 1, z), AIR) in ROCKS and h(x, y, z, 61) % 13 == 0:
                    c[(x, y, z)] = "minecraft:pointed_dripstone[thickness=tip,vertical_direction=down,waterlogged=false]"
    return {k: v for k, v in c.items()}


def den_marks():
    return {"cat-bed": (34, 6, "south", 1), "den-chest": (44, 3, "west", 1), "den-sign": (31, 1, "south", 2),
            "node-cat-den": (30, 13, "north", None)}
