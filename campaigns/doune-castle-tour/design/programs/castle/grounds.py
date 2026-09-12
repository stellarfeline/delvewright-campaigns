"""The ground, the approach, the courtyard and the curtain wall.

Everything the ranges do not stand on: the road that crosses the three dry
ditches on its timber bridges, the turf and wildflowers it runs through, the
cobbled courtyard with its well, its cart and its stores, and the curtain wall
with its walk, its lanterns, its corbelled bartizans and the two stepped corner
rounds at the south angles.

Two shapes decide what a wall column is, and both are read off the neighbours
rather than written down per run. A cell is **parapet** when a body standing on
it could step off the castle's own ground, so the crenels follow the wall's
exposed face wherever it goes — round a bartizan, round a corner round — and no
outward edge is ever left open. A cell is **rail** when the step off it is into
the courtyard fifteen courses below, so the timber rail follows the walk's inner
edge and the rounds keep their open floor to stand on.
"""

from .common import *  # noqa: F401,F403

PALETTE = {
    # ground cover: the meadow the castle stands in
    "yard/tuft": "minecraft:short_grass",
    "yard/fern": "minecraft:fern",
    "yard/poppy": "minecraft:poppy",
    "yard/daisy": "minecraft:oxeye_daisy",
    "yard/dandelion": "minecraft:dandelion",
    "yard/cornflower": "minecraft:cornflower",
    # the bridges, the wall-walk and their light
    "yard/rail": "minecraft:dark_oak_fence[east=false,north=false,south=false,waterlogged=false,west=false]",
    "yard/lantern": "minecraft:lantern[hanging=false,waterlogged=false]",
    # the boundary stone and the standards either side of the gate
    "yard/marker": "minecraft:stone_bricks",
    "yard/marker_head": "minecraft:chiseled_stone_bricks",
    "yard/marker_cap": "minecraft:stone_brick_slab[type=bottom,waterlogged=false]",
    "yard/pier": "minecraft:stone_bricks",
    "yard/banner": "minecraft:red_banner[rotation=8]",
    # the well and its winding frame
    "yard/well_apron": "minecraft:mossy_cobblestone",
    "yard/well_post": "minecraft:stripped_oak_log[axis=y]",
    "yard/well_beam": "minecraft:stripped_oak_log[axis=x]",
    "yard/well_chain": "minecraft:iron_chain[axis=y,waterlogged=false]",
    "yard/well_bucket": "minecraft:cauldron",
    # the cart and the stores by the kitchen door
    "yard/cart_bed": "minecraft:oak_planks",
    "yard/cart_side": "minecraft:oak_slab[type=bottom,waterlogged=false]",
    "yard/cart_wheel": "minecraft:oak_log[axis=x]",
    "yard/cart_shaft": "minecraft:oak_fence[east=false,north=false,south=false,waterlogged=false,west=false]",
    "yard/hay": "minecraft:hay_block[axis=y]",
    "yard/cordwood": "minecraft:spruce_log[axis=x]",
    "yard/crate": "minecraft:stripped_oak_wood[axis=y]",
    # the lean-to oven against the south wall
    "yard/footing": "minecraft:stone_bricks",
    "yard/oven": "minecraft:cobblestone",
    "yard/oven_post": "minecraft:oak_fence[east=false,north=false,south=false,waterlogged=false,west=false]",
    # the wooded valley edge
    "yard/oak_log": "minecraft:oak_log[axis=y]",
    "yard/oak_leaf": "minecraft:oak_leaves[distance=7,persistent=true,waterlogged=false]",
    "yard/spruce_log": "minecraft:spruce_log[axis=y]",
    "yard/spruce_leaf": "minecraft:spruce_leaves[distance=7,persistent=true,waterlogged=false]",
}
ANCHORS = {
    (77, WALK, 1): ("arrival", "entry"),
    (77, WALK, 19): ("stop-approach", None),
    (46, WALK, 62): ("stop-courtyard", None),
    (50, 23, 90): ("stop-wall-walk", None),
}
ANCHOR_CELLS = {(ax, az) for (ax, _, az) in ANCHORS}


# ------------------------------------------------------------ the dice we roll
def _hash(a, b, salt):
    """A stable integer scatter: same coordinates, same answer, every run.

    Python's own `hash` is salted per process, so it is never asked here —
    the same program and the same seed owe byte-identical output (ADR-0006).
    """
    n = (a * 73856093) ^ (b * 19349663) ^ (salt * 83492791)
    n &= 0xFFFFFFFF
    n = (n ^ (n >> 13)) * 1274126177 & 0xFFFFFFFF
    return n ^ (n >> 16)


def _meadow(c, x, z):
    """Grass and wildflowers on turf, in small clumps rather than pixel noise.

    Keyed to a two-by-two patch so equal columns still merge along both axes: a
    per-cell roll would give every row a key of its own and multiply the
    partition the emitter has to write.
    """
    roll = _hash(x // 2, z // 2, 11) % 100
    if roll < 22:
        c.add("yard/tuft", 1)
    elif roll < 27:
        c.add("yard/fern", 1)
    elif roll < 30:
        c.add("yard/poppy", 1)
    elif roll < 33:
        c.add("yard/daisy", 1)
    elif roll < 36:
        c.add("yard/dandelion", 1)
    elif roll < 38:
        c.add("yard/cornflower", 1)


# ------------------------------------------------------- the approach and road
APRON = (71, 83, 27, 29)       # the packed road widens into an apron at the gate
PIER_X = (74, 80)              # a standard either side of the gate arch
LAMP_Z = 27                    # and a lamp bollard in front of each
MARKER = (82, 19)              # the boundary stone, beside the middle rampart


def approach_column(c, x, z):
    """The road, the three stepped ditches and the ramparts between them."""
    for z0, z1 in ditch_bands():
        if z0 <= z <= z1:
            if on_road(x):                      # the timber bridge over it
                c.spans = [("rock", 4)]
                c.y = 4
                c.add(None, 3)
                c.add("deck", 1)                # y7: the deck, flush with the road
                if x in ROAD:                   # a rail down each edge of the deck
                    c.add("yard/rail", 1)
                    if z in (z0, z1):           # a lamp on each end post
                        c.add("yard/lantern", 1)
                c.air_to_top()
                return c
            depth = DITCH_PROFILE[z - z0]
            c.spans = [("rock", GRADE - depth - 1)]
            c.y = GRADE - depth - 1
            c.add("earth", 1)                   # the bare riser of the step
            c.add("turf", 1)                    # grassed over, as a dry ditch is
            _meadow(c, x, z)
            c.air_to_top()
            return c
    if inside(x, z, APRON):
        c.add("road", 1)
        if z == APRON[3] and x in PIER_X:
            c.add("yard/pier", 2)
            c.add("yard/marker_head", 1)
            c.add("yard/banner", 1)             # the banners at the gate
        elif z == LAMP_Z and x in PIER_X:
            c.add("yard/pier", 1)
            c.add("yard/lantern", 1)
        c.air_to_top()
        return c
    if on_road(x):
        c.add("road", 1)
        c.air_to_top()
        return c
    c.add("turf", 1)
    if (x, z) == MARKER:
        c.add("yard/marker", 2)
        c.add("yard/marker_head", 1)
        c.add("yard/marker_cap", 1)
    else:
        _meadow(c, x, z)
    c.air_to_top()
    return c


# -------------------------------------------- what the curtain wall is made of
ROUNDS = ((15, 88), (88, 88))      # the stepped rounds at the two south angles
ROUND_R2 = 16
BARTIZAN_X = (35, 68)              # corbelled out at the south wall's mid-points
BARTIZAN_Z = (92, 94)
BARTIZAN_TOP = CURTAIN_CRENEL + 2  # its cap stands clear above the curtain's
STAIR_HEAD = (89, 56, 57)          # where the long east flight lands on the walk


def in_round(x, z):
    return any((x - cx) ** 2 + (z - cz) ** 2 <= ROUND_R2 for cx, cz in ROUNDS)


def in_bartizan(x, z):
    return BARTIZAN_Z[0] <= z <= BARTIZAN_Z[1] and any(
        abs(x - bx) <= 1 for bx in BARTIZAN_X
    )


def in_curtain(x, z):
    """The three straight runs of curtain: west, east and south."""
    if not (COURT_Z0 <= z <= SCURT_Z1 and CX0 <= x <= CX1):
        return False
    return x <= CX0 + 2 or x >= CX1 - 2 or z >= SCURT_Z0


def on_walk(x, z):
    """Every column whose top is the wall-walk."""
    return in_curtain(x, z) or in_round(x, z) or in_bartizan(x, z)


def _beyond(x, z):
    """Off the castle's own ground — what a parapet has to stand against."""
    return not (CX0 <= x <= CX1 and CZ0 <= z <= CZ1)


def _yard_ground(x, z):
    """The courtyard floor: fifteen courses below the walk, and no way down."""
    return CX0 <= x <= CX1 and COURT_Z0 <= z <= SCURT_Z1 and not on_walk(x, z)


def _neighbours(x, z):
    return ((x + 1, z), (x - 1, z), (x, z + 1), (x, z - 1))


def is_parapet(x, z):
    """Crenels stand wherever a body could step off the wall into open air."""
    return any(
        not on_walk(nx, nz) and _beyond(nx, nz) for nx, nz in _neighbours(x, z)
    )


def is_rail(x, z):
    """The rail stands wherever the step off the walk is into the courtyard."""
    if x == STAIR_HEAD[0] and STAIR_HEAD[1] <= z <= STAIR_HEAD[2]:
        return False                            # the flight has to land somewhere
    return any(_yard_ground(nx, nz) for nx, nz in _neighbours(x, z))


def _side(x):
    return x <= CX0 + 2 or x >= CX1 - 2


def wall_column(c, x, z):
    """One column of curtain or corner round, from its footing to its crenels.

    Only the exposed face is raised. Everything behind it tops out at the walk
    course, so a body stands at `CURTAIN_TOP + 1` and walks the whole circuit —
    east flight, south wall, both rounds, west wall — without a step over.
    """
    c.add("cobble", 1)
    c.upto("wall", CURTAIN_TOP)
    if is_parapet(x, z):
        run = x + z if in_round(x, z) else (z if _side(x) else x)
        c.upto("wall", CURTAIN_CRENEL if crenel(run) else CURTAIN_TOP + 1)
        c.air_to_top()
        return c
    if is_rail(x, z):
        c.add("yard/rail", 1)
        if (x + z) % 8 == 0:                    # a lamp on the post, at intervals
            c.add("yard/lantern", 1)
    c.air_to_top()
    return c


def bartizan_column(c, x, z):
    """A turret corbelled out over nothing, entered from the walk behind it.

    The courses under it step out one at a time — a corbel bracket, not a
    buttress: the ground beneath a bartizan is meadow and stays meadow. Its cap
    stands two courses over the curtain's own crenels, so the turret reads as a
    turret in silhouette and not as more wall.
    """
    centre = min(BARTIZAN_X, key=lambda bx: abs(x - bx))
    z0, z1 = BARTIZAN_Z
    c.add("turf", 1)
    c.upto(None, CURTAIN_TOP - 4)
    c.add("wall" if (x == centre and z == z0) else None, 1)     # the first corbel
    c.add("wall" if z == z0 else None, 1)                       # the second
    c.add("wall" if z <= z0 + 1 else None, 1)                   # the third
    c.add("wall", 1)                                            # the turret floor
    if x == centre and z < z1:
        c.air_to_top()                          # the chamber a body stands in
        return c
    c.upto("wall", CURTAIN_CRENEL)
    if crenel(x + z):
        c.upto("wall", BARTIZAN_TOP)            # the cap's own merlons
    c.air_to_top()
    return c


def curtain_column(c, x, z):
    """The curtain inside the castle's own footprint; `None` where there is none."""
    if in_curtain(x, z) or in_round(x, z):
        return wall_column(c, x, z)
    return None


def outside_column(c, x, z):
    """The ground the castle stands in, beyond its walls."""
    if in_round(x, z):
        return wall_column(c, x, z)             # the rounds project past the line
    if in_bartizan(x, z):
        return bartizan_column(c, x, z)
    c.add("turf", 1)
    tree = _tree_span(x, z)
    if tree is not None:
        for role, n in tree:
            c.add(role, n)
    else:
        _meadow(c, x, z)
    c.air_to_top()
    return c


# ----------------------------------------------------- the wooded valley edge
TREE_LAT = 8            # one candidate per eight-cell square of open ground
TREE_DENSITY = 60       # per cent of those squares that carry a tree
TREE_MARGIN = 1         # never within this many cells of the region's own edge
TREE_STANDOFF = 8       # nor this close to the castle's own north lawn
CANOPY = 1              # crown radius: a crown three cells across

# Why a three-cell crown and sixty per cent, and not a forest: every canopy
# column puts one standable cell above its topmost leaf that no body can walk
# to, so a wood costs the reachability gate its own footprint in area. A
# five-cell crown costs twenty-one cells a tree against a budget of a couple of
# hundred; a three-cell crown costs nine, and buys three times the trees. The
# measured cost of this wood is 21 trees, 189 cells, and the piece still reads
# 91.78% reachable against a floor of 91%.


def _tree_zone(x, z):
    """Ground a tree may stand on: open, flat, and well back from the road."""
    if not (TREE_MARGIN <= x < X - TREE_MARGIN and TREE_MARGIN <= z < Z - TREE_MARGIN):
        return False
    if z < CZ0 + TREE_STANDOFF:
        return False                            # the approach is ditched, not flat
    if in_round(x, z) or in_bartizan(x, z):
        return False
    return not (CX0 - 3 <= x <= CX1 + 3 and CZ0 - 3 <= z <= CZ1 + 3)


def _tree_stands(cx, cz):
    return all(
        _tree_zone(cx + dx, cz + dz)
        for dx in range(-CANOPY, CANOPY + 1)
        for dz in range(-CANOPY, CANOPY + 1)
    )


def _tree_centre(x, z):
    """The tree this column belongs to, if any. At most one ever claims it."""
    for gx in (x // TREE_LAT - 1, x // TREE_LAT, x // TREE_LAT + 1):
        for gz in (z // TREE_LAT - 1, z // TREE_LAT, z // TREE_LAT + 1):
            h = _hash(gx, gz, 23)
            if h % 100 >= TREE_DENSITY:
                continue
            # offsets 2..5 inside a lattice of 8: two centres are never closer
            # than five cells, so no column is ever claimed by two canopies.
            cx = gx * TREE_LAT + 2 + (h >> 5) % 4
            cz = gz * TREE_LAT + 2 + (h >> 9) % 4
            if max(abs(x - cx), abs(z - cz)) > CANOPY:
                continue
            if not _tree_stands(cx, cz):
                continue
            return cx, cz, h
    return None


def _tree_span(x, z):
    """The spans this column of a tree lays above the turf, or `None`."""
    hit = _tree_centre(x, z)
    if hit is None:
        return None
    cx, cz, h = hit
    d = max(abs(x - cx), abs(z - cz))
    if h % 3:                                   # an oak: a small round crown
        trunk = 5 + (h >> 13) % 3
        if d == 0:
            return [("yard/oak_log", trunk), ("yard/oak_leaf", 2)]
        return [(None, trunk - 2), ("yard/oak_leaf", 3)]
    trunk = 8 + (h >> 13) % 3                   # a spruce: a tall narrow spire
    if d == 0:
        return [("yard/spruce_log", trunk), ("yard/spruce_leaf", 1)]
    return [(None, trunk - 6), ("yard/spruce_leaf", 6)]


# --------------------------------------------------- what stands in the yard
WELL = (49, 51, 61, 63)             # the well head
WELL_APRON = (48, 52, 60, 64)       # the worn stone ring worn around it
SHAFT = (50, 62)


def _well(put):
    x0, x1, z0, z1 = WELL_APRON
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if not inside(x, z, WELL):
                put(x, z, ("yard/well_apron", 1))
                continue
            if (x, z) == SHAFT:                 # the dry shaft, open to step into
                put(x, z, ("cobble", 1), (None, 2),
                    ("yard/well_bucket", 1),    # the bucket, on its chain
                    ("yard/well_chain", 1),
                    ("yard/well_beam", 1))
                continue
            put(x, z, ("cobble", 1), ("wall", 1))
            if z == SHAFT[1]:                   # the two posts of the winding frame
                put(x, z, ("yard/well_post", 3), ("yard/well_beam", 1))
            elif (x, z) in ((WELL[0], WELL[2]), (WELL[1], WELL[3])):
                put(x, z, ("yard/lantern", 1))


CART = (26, 28, 53, 55)             # the cart, drawn up by the kitchen door
CART_WHEEL_X = (25, 29)
CART_LOAD = (27, 54)


def _cart(put):
    x0, x1, z0, z1 = CART
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            put(x, z, ("cobble", 1), ("yard/cart_bed", 1))
            if (x, z) == CART_LOAD:
                put(x, z, ("yard/hay", 1))      # a bale still in the bed
            elif x in (x0, x1) or z == z1:
                put(x, z, ("yard/cart_side", 1))
    for x in CART_WHEEL_X:
        put(x, CART_LOAD[1], ("cobble", 1), ("yard/cart_wheel", 2))
    for x in (x0, x1):
        put(x, z0 - 1, ("cobble", 1), ("yard/cart_shaft", 1))


STORES = (21, 23, 54, 57)           # cordwood and hay, stacked clear of the door


def _stores(put):
    x0, x1, z0, z1 = STORES
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            role = "yard/cordwood" if z <= z0 + 1 else "yard/hay"
            put(x, z, ("cobble", 1), (role, 1))
            if x <= x0 + 1 and z in (z0, z1):   # a second tier, one step up
                put(x, z, (role, 1))
    put(25, 56, ("cobble", 1), ("yard/crate", 2))
    put(25, 57, ("cobble", 1), ("yard/crate", 1))


OVEN = (29, 34, 85, 88)             # the lean-to's footing against the south wall
OVEN_MOUTH = 31


def _oven(put):
    x0, x1, z0, z1 = OVEN
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            put(x, z, ("cobble", 1), ("yard/footing", 1))
    for x in (30, 31, 32):                      # the oven itself, built up in steps
        put(x, z1, ("yard/oven", 2))
        if x != OVEN_MOUTH:
            put(x, z1 - 1, ("yard/oven", 1))
    for x in (x0, x1):                          # the posts the lean-to stood on
        put(x, z0, ("yard/oven_post", 1))


def _furniture():
    stacks = {}

    def put(x, z, *spans):
        stacks.setdefault((x, z), []).extend(spans)

    _well(put)
    _cart(put)
    _stores(put)
    _oven(put)
    return stacks


FURNITURE = _furniture()


# ------------------------------------------------------------- the courtyard
FLIGHTS = (
    (67, 70, 50, 57, WALK, F1),        # up to the lord's hall
    (36, 39, 46, 53, WALK, F1),        # up to the great hall's west door
    (16, 19, 50, 57, WALK, F1),        # up the kitchen tower's turret
)
EAST_FLIGHT = (86, 88, 56, 84)         # the long climb onto the east wall-walk


def _joint(x, z):
    """Grass in the cobble joints, close under a wall where no foot falls."""
    if (x, z) in ANCHOR_CELLS:
        return False
    near = (x <= CX0 + 5 or x >= CX1 - 5
            or z >= COURT_Z1 - 2 or z <= COURT_Z0 + 2)
    return near and _hash(x // 2, z // 2, 7) % 100 < 30


def courtyard_column(c, x, z):
    # the three external stairs, each climbing north toward its own door
    for x0, x1, z0, z1, y0, y1 in FLIGHTS:
        if x0 <= x <= x1:
            h = stair_height(z, z0, z1, y0, y1)
            if h is not None:
                c.add("cobble", 1)
                c.upto("step", h)
                c.air_to_top()
                return c
    # the long flight up onto the east wall-walk
    if inside(x, z, EAST_FLIGHT):
        c.add("cobble", 1)
        c.upto("step", WALK + (EAST_FLIGHT[3] - z) // 2)
        c.air_to_top()
        return c
    stack = FURNITURE.get((x, z))
    if stack is not None:
        for role, n in stack:
            c.add(role, n)
        c.air_to_top()
        return c
    if _joint(x, z):
        c.add("turf", 1)
        if _hash(x, z, 19) % 3:
            c.add("yard/tuft", 1)
    else:
        c.add("cobble", 1)
    c.air_to_top()
    return c
