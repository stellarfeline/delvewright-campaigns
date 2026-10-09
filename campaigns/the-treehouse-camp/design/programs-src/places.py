#!/usr/bin/env python3
"""Draws each place of The Treehouse Camp and writes programs/<place>.json.

    python3 places.py <place-stem> [...]     (or `all`)

Every position comes from the place's handout, fetched at run time; the
design itself is in world coordinates, the same as DESIGN.md section 4.
"""
import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import thlib  # noqa: E402
import lights  # noqa: E402

C = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PREFABS = os.environ.get("DELVEWRIGHT_PREFABS", "")
CAMPAIGN = "the-treehouse-camp"

# ---------------------------------------------------------------- materials
BARK = [(6, "mangrove_wood[axis=y]"), (3, "spruce_wood[axis=y]"), (1, "dark_oak_wood[axis=y]")]
BARK_X = [(6, "mangrove_wood[axis=x]"), (3, "spruce_wood[axis=x]")]
BARK_Z = [(6, "mangrove_wood[axis=z]"), (3, "spruce_wood[axis=z]")]
LEAVES = [(5, "oak_leaves[persistent=true]"), (3, "dark_oak_leaves[persistent=true]"), (1, "azalea_leaves[persistent=true]")]
BUSH = [(4, "azalea_leaves[persistent=true]"), (2, "oak_leaves[persistent=true]"), (1, "flowering_azalea_leaves[persistent=true]")]
FOREST_FLOOR = [(6, "moss_block"), (2, "podzol[snowy=false]"), (1, "coarse_dirt"), (1, "rooted_dirt")]
DECK = [(7, "oak_planks"), (2, "spruce_planks"), (1, "stripped_oak_wood[axis=y]")]
DECK_WORN = [(5, "oak_planks"), (3, "spruce_planks"), (2, "stripped_oak_wood[axis=y]"), (1, "mossy_cobblestone")]
RAIL = "oak_fence"
POST = "stripped_oak_log[axis=y]"
THATCH = "hay_block[axis=y]"
CABIN_WALL = [(4, "spruce_planks"), (1, "stripped_spruce_wood[axis=y]")]
LANTERN_HANG = "lantern[hanging=true]"
LANTERN_STAND = "lantern[hanging=false]"
CHAIN_Y = "iron_chain[axis=y]"


def P(m, x, y, z, choices, salt=0):
    m.set(x, y, z, m.pick(x, y, z, choices, salt))


def trunk_layer(m, cx, cz, r, y, choices=BARK, keep=None):
    for x, z in m.disc_cells(cx, cz, r):
        if keep and keep(x, z):
            continue
        P(m, x, y, z, choices)


def ladder(m, x, z0, z1, y0, y1, facing):
    for y in range(y0, y1 + 1):
        for z in range(z0, z1 + 1):
            m.set(x, y, z, f"ladder[facing={facing}]")


def root(m, cells, heights, base_y, salt=1):
    """A buttress root: a list of (x, z) cells and a height for each."""
    for (x, z), h in zip(cells, heights):
        for dy in range(h):
            P(m, x, base_y + dy, z, BARK, salt)
        top = base_y + h
        if m.get(x, top, z) is None and h >= 1:
            m.set(x, top, z, "moss_carpet")


def line_cells(x0, z0, x1, z1, thick=2):
    """Cells of a thick straight line, ordered from (x0, z0) outward."""
    n = max(abs(x1 - x0), abs(z1 - z0))
    out = []
    for i in range(n + 1):
        t = i / n if n else 0
        x = round(x0 + (x1 - x0) * t)
        z = round(z0 + (z1 - z0) * t)
        step = []
        for dx in range(thick):
            for dz in range(thick):
                step.append((x + dx, z + dz))
        out.append(step)
    return out


def hanging_lantern(m, x, z, y_top, drop):
    """A lantern on a chain hanging `drop` cells under the block at y_top + 1."""
    for y in range(y_top - drop + 2, y_top + 1):
        m.set(x, y, z, CHAIN_Y)
    m.set(x, y_top - drop + 1, z, LANTERN_HANG)


def light_marks(m, node):
    for anchor, n, (x, y, z), _ in lights.for_node(node):
        m.mark(anchor.split("/", 1)[1], x, y, z, "south")


def write(m, stem):
    prog = m.program(f"{CAMPAIGN}-{stem}")
    path = os.path.join(C, "programs", f"{stem}.json")
    json.dump(prog, open(path, "w"), indent=1)
    cells = len(m.cells)
    print(f"{stem}: {cells} blocks, {len(prog['rules'])} rules, {len(prog['palette'])} roles, "
          f"faces {prog['shown_faces']}, {os.path.getsize(path)} bytes")


# ---------------------------------------------------------------- the Hearth Tree
HEARTH = (36.0, 36.0)


def hearth_trunk_keep_ladder(x, z):
    # The west face beside the ladder (x 30, z 35..36) stays flat bark.
    return False


def root_glade():
    h = thlib.handout(C, "node/root-glade", PREFABS)
    m = thlib.Model(h)
    (x0, y0, z0), (x1, y1, z1) = h["world_min"], m.wmax()
    floor = 72
    cx, cz = HEARTH
    # Ground of the glade: the handed level, y 71, inside the ring.
    for x in range(x0 + 1, x1):
        for z in range(z0 + 1, z1):
            P(m, x, floor - 1, z, FOREST_FLOOR, 3)
    # The trunk, straight 10 across, flared at its foot except on the ladder face.
    for y in range(floor - 1, y1 + 1):
        trunk_layer(m, cx, cz, 5.0, y)
    for y in range(floor, floor + 3):
        trunk_layer(m, cx, cz, 6.0, y, keep=lambda x, z: x <= 31 and 33 <= z <= 38)
    # Buttress roots: tall walls of bark that end in one low knuckle, so no
    # body climbs them (a step of two from the knuckle to the root).
    roots = [
        (38, 29, 38, 27),   # north
        (41, 30, 43, 28),   # north-east
        (41, 37, 43, 37),   # east
        (33, 41, 33, 43),   # south
        (30, 41, 28, 43),   # south-west
    ]
    for rx0, rz0, rx1, rz1 in roots:
        steps = line_cells(rx0, rz0, rx1, rz1, 2)
        for i, step in enumerate(steps):
            hgt = 1 if i == len(steps) - 1 else max(3, 6 - i)
            for (x, z) in step:
                if (x - cx + 0.5) ** 2 + (z - cz + 0.5) ** 2 <= 25:
                    continue
                for dy in range(hgt):
                    P(m, x, floor + dy, z, BARK, 7)
                if m.get(x, floor + hgt, z) is None:
                    m.set(x, floor + hgt, z, "moss_carpet")
    # The hedge round the glade: fallen logs and bushes three high on the
    # ring, so the glade is a room with open sky-light above its walls.
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if x in (x0, x1) or z in (z0, z1):
                for dy in range(3):
                    if dy < 2 and (x + z) % 7 in (0, 1, 2):
                        axis = "x" if z in (z0, z1) else "z"
                        m.set(x, floor + dy, z, f"mangrove_log[axis={axis}]")
                    else:
                        P(m, x, floor + dy, z, BUSH, 11)
    # Ferns along the inside of the hedge.
    for x in range(x0 + 1, x1):
        for z in range(z0 + 1, z1):
            edge = x in (x0 + 1, x1 - 1) or z in (z0 + 1, z1 - 1)
            if edge and m.get(x, floor, z) is None and (x * 3 + z) % 4 != 0:
                m.set(x, floor, z, "fern")
    # The fire ring, south-east of the trunk, and two log seats.
    fx, fz = 42, 42
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            if dx or dz:
                m.set(fx + dx, floor, fz + dz, "mossy_cobblestone_slab[type=bottom]")
    m.set(fx, floor, fz, "campfire[lit=true,facing=north]")
    for z in (40, 41):
        m.set(44, floor, z, "stripped_spruce_log[axis=z]")
    for x in (40, 41):
        m.set(x, floor, 44, "stripped_spruce_log[axis=x]")
    # The rope ladder up the bark to the Hearth House (its top rung is the house's).
    ladder(m, 30, 35, 36, floor, y1, "west")
    # Lanterns hanging on chains from the platform overhead, all round the trunk.
    for (lx, lz) in ((28, 30), (34, 27), (40, 29), (45, 30), (44, 36), (43, 44), (37, 44), (28, 44), (27, 36)):
        hanging_lantern(m, lx, lz, y1, 8)
    # Contract: the glade's floor, the ladder shaft above it, the top rung's cell.
    m.space("glade", "open", (x0 + 1, floor, z0 + 1, x1 - 1, floor + 2, z1 - 1),
            (30, floor + 3, 35, 30, y1 - 1, 36))
    m.via("glade-ladder", (30, y1, 35, 30, y1, 36))
    top = floor + 3
    m.nobody("over-the-glade", "the tops of the buttress roots, the hedge and the hanging lanterns: nobody climbs up here",
             (x0, top, z0, 29, y1, z1), (31, top, z0, x1, y1, z1),
             (30, top, z0, 30, y1, 34), (30, top, 37, 30, y1, z1))
    m.entry = "glade"
    m.edge(a="glade", b="exterior", **{"class": "walk", "via": "glade-ladder"})
    m.mark("spawn", 28, floor, 28, "south", role="entry")
    m.mark("node-root-glade", 28, floor, 38, "north")
    light_marks(m, "node/root-glade")
    write(m, "root-glade")


# ---------------------------------------------------------------- shared parts
def deck(m, x0, z0, x1, z1, y, choices=DECK, skip=None, salt=5):
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if skip and skip(x, z):
                continue
            if m.get(x, y, z) is None:
                P(m, x, y, z, choices, salt)


def rail_ring(m, x0, z0, x1, z1, y, gaps=()):
    """A fence rail round a rectangle (the ring row), with gaps [(x, z), ...]
    left open for a seam; stripped-log posts two high at the corners and at
    each side of a gap."""
    gaps = set(gaps)
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if x in (x0, x1) or z in (z0, z1):
                if (x, z) in gaps:
                    continue
                m.set(x, y, z, RAIL)
                m.set(x, y + 1, z, RAIL)
    posts = {(x0, z0), (x0, z1), (x1, z0), (x1, z1)}
    for (gx, gz) in gaps:
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (gx + dx, gz + dz)
            if n not in gaps and (n[0] in (x0, x1) or n[1] in (z0, z1)):
                posts.add(n)
    for (px, pz) in posts:
        for dy in range(3):
            m.set(px, y + dy, pz, POST)


def lamp_post(m, x, z, y, height=3):
    for dy in range(height):
        m.set(x, y + dy, z, POST)
    m.set(x, y + height, z, LANTERN_STAND)


def cabin(m, x0, z0, x1, z1, y, wall_h, ridge_axis, doors=(), windows=()):
    """A timber cabin with a stepped thatch gable over it.

    Walls x0..x1 x z0..z1 from y up wall_h courses; the roof starts on the
    course over the walls, overhangs one cell on the eaves sides, and its
    gable ends are infilled with planks."""
    top = y + wall_h - 1
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            edge = x in (x0, x1) or z in (z0, z1)
            for yy in range(y, top + 1):
                if edge:
                    corner = x in (x0, x1) and z in (z0, z1)
                    m.set(x, yy, z, "stripped_spruce_log[axis=y]" if corner else m.pick(x, yy, z, CABIN_WALL, 9))
                else:
                    m.set(x, yy, z, None)
    for (dx, dz, dh) in doors:
        for yy in range(y, y + dh):
            m.set(dx, yy, dz, None)
    for (wx, wz) in windows:
        m.set(wx, y + 1, wz, "spruce_fence")
    # the gable
    if ridge_axis == "x":
        lo, hi = z0 - 1, z1 + 1
        k = 0
        while lo <= hi:
            yy = top + 1 + k
            for x in range(x0 - 1, x1 + 2):
                for z in (lo, hi):
                    m.set(x, yy, z, THATCH)
            for z in range(lo + 1, hi):
                for x in (x0, x1):
                    m.set(x, yy, z, m.pick(x, yy, z, CABIN_WALL, 9))
            lo, hi, k = lo + 1, hi - 1, k + 1
    else:
        lo, hi = x0 - 1, x1 + 1
        k = 0
        while lo <= hi:
            yy = top + 1 + k
            for z in range(z0 - 1, z1 + 2):
                for x in (lo, hi):
                    m.set(x, yy, z, THATCH)
            for x in range(lo + 1, hi):
                for z in (z0, z1):
                    m.set(x, yy, z, m.pick(x, yy, z, CABIN_WALL, 9))
            lo, hi, k = lo + 1, hi - 1, k + 1


def platform_contract(m, x0, z0, x1, z1, floor, vias, space="room", reason=None):
    """The floor of a platform with its rail: one space two cells tall over
    the footprint and the ring rows (the rail's lower course, and the top
    course a lantern line replaces), minus every via; everything above it to
    the frame's top is out of walk (rail tops, posts, roofs)."""
    lo = (x0, floor, z0, x1, floor + 1, z1)
    # Each via is three tall; its top row meets the space through a collar,
    # the row of air just inside the ring beside it.
    collars = []
    for v in vias:
        if v[4] < floor + 2:
            continue
        dx = -1 if v[0] == v[3] == x1 else (1 if v[0] == v[3] == x0 else 0)
        dz = -1 if v[2] == v[5] == z1 else (1 if v[2] == v[5] == z0 else 0)
        collars.append((v[0] + dx, floor + 2, v[2] + dz, v[3] + dx, floor + 2, v[5] + dz))
    m.space(space, "open", *(thlib.subtract(lo, vias) + collars))
    top = m.wmax()[1]
    if top >= floor + 2:
        mn, mx = m.min, m.wmax()
        hi = (mn[0], floor + 2, mn[2], mx[0], top, mx[2])
        m.nobody("overhead", reason or "rail tops, posts, roofs and lanterns, all over a body's head",
                 *thlib.subtract(hi, list(vias) + collars))


# ---------------------------------------------------------------- the Hearth House
def hearth_house():
    h = thlib.handout(C, "node/hearth-house", PREFABS)
    m = thlib.Model(h)
    (x0, y0, z0), (x1, y1, z1) = h["world_min"], m.wmax()
    cx, cz = HEARTH
    fy = y0           # the floor course, 85
    floor = fy + 1    # 86
    # The trunk passes through, the whole height of the box.
    for y in range(fy, y1 + 1):
        trunk_layer(m, cx, cz, 5.0, y)
    # The deck over the whole shell footprint, and the ladder's hole.
    deck(m, x0, z0, x1, z1, fy)
    ladder(m, 30, 35, 36, fy, fy, "west")
    # Rails on the ring, open at the two bridge mouths.
    gaps = [(48, z) for z in (34, 35, 36)] + [(x, 48) for x in (34, 35, 36)]
    rail_ring(m, x0, z0, x1, z1, floor, gaps)
    # Cabin A, the long one against the trunk's north face; cabin B to the south-east.
    cabin(m, 29, 25, 42, 30, floor, 4, "x", doors=[(41, 30, 2), (29, 27, 2)], windows=[(33, 25), (38, 25)])
    cabin(m, 41, 39, 46, 46, floor, 4, "z", doors=[(41, 43, 2)], windows=[(46, 42), (43, 46)])
    # Inside the cabins: woven mats, a low table, a hanging lantern.
    for x in (31, 32, 33):
        m.set(x, floor, 26, "brown_carpet")
    m.set(35, floor, 26, "spruce_trapdoor[facing=north,half=top,open=false,powered=false,waterlogged=false]")
    m.set(39, floor, 26, "white_carpet")
    m.set(40, floor, 26, "white_carpet")
    hanging_lantern(m, 36, 27, floor + 3, 1)
    hanging_lantern(m, 43, 42, floor + 3, 1)
    hanging_lantern(m, 33, 31, floor + 3, 1)
    hanging_lantern(m, 39, 31, floor + 3, 1)
    for lx in (30, 35, 41):
        hanging_lantern(m, lx, 24, floor + 3, 1)
    for z in (44, 45):
        m.set(44, floor, z, "red_carpet")
    # The stone hearth against the trunk's south face, its chimney up the bark.
    for x in range(33, 40):
        for y in range(floor, floor + 3):
            m.set(x, y, 41, m.pick(x, y, 41, [(4, "stone_bricks"), (2, "mossy_stone_bricks"), (1, "cobblestone")], 13))
    m.set(36, floor, 41, "campfire[lit=true,facing=south]")
    m.set(36, floor + 1, 41, None)
    for x in (35, 36, 37):
        m.set(x, floor, 42, "stone_brick_slab[type=bottom]")
    for y in range(floor + 3, y1 + 1):
        for x in (35, 36, 37):
            m.set(x, y, 41, m.pick(x, y, 41, [(3, "stone_bricks"), (1, "mossy_stone_bricks")], 14))
    # Benches either side of the fire.
    for z in (43, 44, 45):
        m.set(33, floor, z, "spruce_stairs[facing=west,half=bottom,shape=straight]")
        m.set(39, floor, z, "spruce_stairs[facing=east,half=bottom,shape=straight]")
    # Lamp posts inside the rail.
    for (lx, lz) in ((24, 24), (24, 32), (24, 40), (24, 47), (31, 47), (47, 24), (47, 32), (47, 38), (39, 47)):
        lamp_post(m, lx, lz, floor)
    # Contract.
    v_long = (48, floor, 34, 48, floor + 2, 36)
    v_low = (34, floor, 48, 36, floor + 2, 48)
    m.via("hearth-long", v_long)
    m.via("hearth-low", v_low)
    m.via("glade-ladder", (30, fy, 35, 30, fy, 36))
    platform_contract(m, x0, z0, x1, z1, floor, [v_long, v_low])
    m.entry = "room"
    for v in ("hearth-long", "hearth-low", "glade-ladder"):
        m.edge(a="room", b="exterior", **{"class": "walk", "via": v})
    m.mark("node-hearth-house", 30, floor, 42, "north")
    light_marks(m, "node/hearth-house")
    write(m, "hearth-house")


# ---------------------------------------------------------------- the rope bridges
def rest_region(m, name, reason):
    """Everything of the frame no other region claims, as one out-of-walk
    region: the forest floor under a deck, the rail tops, the stringers."""
    mn, mx = m.min, m.wmax()
    held = []
    for boxes in m.regions.values():
        for b in boxes:
            held.append(tuple(b[i] + m.min[i % 3] for i in range(6)))
    m.nobody(name, reason, *thlib.subtract((mn[0], mn[1], mn[2], mx[0], mx[1], mx[2]), held))


def bridge(stem, node, axis, level, flight, facing, landing, via_top, top_y, end, seam_b, play_b,
           floor, deck_mix, posts_at, edge_top, edge_end, end_class="walk"):
    """A rope bridge: a plank deck between post-and-rope rails, a flight of
    plank steps at one end climbing to a landing and the seam beside it.

    axis: the axis the bridge runs along ('x' or 'z'); a is the coordinate
    along it, b across it. level: (a0, a1) of the level deck. flight: [(a, y)]
    treads. landing/via_top: the a of the landing and of the seam cells at the
    top. end: the a of the seam cells at the level end."""
    h = thlib.handout(C, node, PREFABS)
    m = thlib.Model(h)
    (x0, y0, z0), (x1, y1, z1) = h["world_min"], m.wmax()

    def W(a, y, b):
        return (a, y, b) if axis == "x" else (b, y, a)

    def put(a, y, b, block):
        x, yy, z = W(a, y, b)
        m.set(x, yy, z, block)

    def pick(a, y, b, choices, salt=0):
        x, yy, z = W(a, y, b)
        return m.pick(x, yy, z, choices, salt)

    b0, b1 = play_b
    rb0, rb1 = b0 - 1, b1 + 1
    a_all = sorted([level[0], level[1], landing, via_top] + [a for a, _ in flight])
    a_lo, a_hi = a_all[0], a_all[-1]
    # The forest floor under the bridge: the handed ground, one level.
    for a in range(a_lo, a_hi + 1):
        for b in range(b0, b1 + 1):
            put(a, y0, b, pick(a, y0, b, FOREST_FLOOR, 3))
    # The level deck, the ring rows included, with its rail.
    for a in range(min(level), max(level) + 1):
        for b in range(rb0, rb1 + 1):
            put(a, floor - 1, b, pick(a, floor - 1, b, deck_mix, 5))
        for b in (rb0, rb1):
            put(a, floor, b, RAIL)
            put(a, floor + 1, b, RAIL)
    # Cross-beams under the deck every five blocks.
    for a in range(min(level), max(level) + 1):
        if (a - min(level)) % 5 == 2:
            for b in range(rb0, rb1 + 1):
                put(a, floor - 2, b, "spruce_wood[axis=%s]" % ("z" if axis == "x" else "x"))
    # The flight: plank stairs, a stringer under each rail, rails stepping up.
    for a, ty in flight:
        for b in range(b0, b1 + 1):
            put(a, ty, b, f"oak_stairs[facing={facing},half=bottom,shape=straight]")
            put(a, ty - 1, b, "oak_planks")
        for b in (rb0, rb1):
            put(a, ty, b, "spruce_planks")
            put(a, ty - 1, b, "spruce_planks")
            put(a, ty + 1, b, RAIL)
            put(a, ty + 2, b, RAIL)
    # The landing and the seam's floor at the top of the flight.
    for a in (landing, via_top):
        for b in range(rb0, rb1 + 1):
            put(a, top_y, b, pick(a, top_y, b, deck_mix, 5))
        put(a, top_y - 1, b0, "spruce_planks")
        put(a, top_y - 1, b1, "spruce_planks")
    for b in (rb0, rb1):
        for dy in (1, 2):
            put(landing, top_y + dy, b, RAIL)
            put(via_top, top_y + dy, b, RAIL)
    # Posts with lanterns: at the ends of the level deck and at the landing.
    for a in posts_at:
        for b in (rb0, rb1):
            for dy in range(3):
                put(a, floor + dy, b, POST)
            put(a, floor + 3, b, LANTERN_STAND)
    for b in (rb0, rb1):
        for dy in range(3):
            put(landing, top_y + 1 + dy, b, POST)
        put(landing, top_y + 4, b, LANTERN_STAND)
    # Contract: the deck, the landing, the flight between them, the two seams.
    sb0, sb1 = seam_b

    def box(a0, ya, b0_, a1, yb, b1_):
        p, q = W(a0, ya, b0_), W(a1, yb, b1_)
        return (min(p[0], q[0]), min(p[1], q[1]), min(p[2], q[2]), max(p[0], q[0]), max(p[1], q[1]), max(p[2], q[2]))

    v_end = box(end, floor, sb0, end, floor + 2, sb1)
    v_top = box(via_top, top_y + 1, sb0, via_top, top_y + 3, sb1)
    inward = 1 if end == min(level) else -1
    collar_end = box(end + inward, floor + 2, sb0, end + inward, floor + 2, sb1)
    deck_box = box(min(level), floor, rb0, max(level), floor + 1, rb1)
    m.space("deck", "open", *(thlib.subtract(deck_box, [v_end]) + [collar_end]))
    land_box = box(landing, top_y + 1, rb0, landing, top_y + 2, rb1)
    collar_top = box(landing, top_y + 3, sb0, landing, top_y + 3, sb1)
    m.space("landing", "open", land_box, collar_top)
    fa = [a for a, _ in flight]
    m.region("flight", *box(min(fa), floor, b0, max(fa), top_y + 3, b1))
    m.via(edge_end.split("/")[1], v_end)
    m.via(edge_top.split("/")[1], v_top)
    rest_region(m, "around", "the forest floor under the deck, the stringers and the rail tops: no way onto any of them")
    m.ack = "a bridge is a narrow deck over open air: most of what it covers is the forest floor far below it"
    m.entry = "deck"
    m.edge(a="deck", b="landing", **{"class": "stair", "rise": (top_y + 1) - floor, "via": "flight"})
    m.edge(a="landing", b="exterior", **{"class": "walk", "via": edge_top.split("/")[1]})
    m.edge(a="deck", b="exterior", **{"class": end_class, "via": edge_end.split("/")[1]})
    mid = (min(level) + max(level)) // 2
    x, y, z = W(mid, floor, (b0 + b1) // 2)
    m.mark(f"node-{stem}", x, y, z, "north" if axis == "z" else "east")
    light_marks(m, node)
    write(m, stem)


def long_bridge():
    bridge("long-bridge", "node/long-bridge", "x", (57, 68), [(56, 80), (55, 81), (54, 82), (53, 83), (52, 84), (51, 85)],
           "west", 50, 49, 85, 68, (34, 36), (34, 37), 80, DECK, (57, 67), "edge/hearth-long", "edge/loom-long")


def low_bridge():
    bridge("low-bridge", "node/low-bridge", "z", (55, 68), [(54, 82), (53, 83), (52, 84), (51, 85)],
           "north", 50, 49, 85, 68, (34, 36), (34, 37), 82, DECK_WORN, (55, 67), "edge/hearth-low", "edge/seed-low")


def high_bridge():
    bridge("high-bridge", "node/high-bridge", "z", (45, 62), [(63, 80), (64, 81), (65, 82), (66, 83)],
           "south", 67, 68, 83, 45, (76, 78), (76, 79), 80, DECK, (46, 62), "edge/watch-high", "edge/loom-high")


PLACES = {"root-glade": root_glade, "hearth-house": hearth_house, "long-bridge": long_bridge,
          "low-bridge": low_bridge, "high-bridge": high_bridge}

if __name__ == "__main__":
    names = sys.argv[1:]
    if names == ["all"]:
        names = list(PLACES)
    for n in names:
        PLACES[n]()
