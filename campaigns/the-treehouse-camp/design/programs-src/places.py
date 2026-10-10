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


def unhung_lanterns(m):
    """Every hanging lantern whose block above cannot hold it. The game drops
    a hanging lantern on the first update unless the block over it has a full
    face under it or is a chain, fence, wall or bar (vanilla `LanternBlock
    .canSurvive`, via `Block.canSupportCenter`); leaves, air, a lantern or a
    trapdoor do not hold one."""
    bad = []
    holds = ("_planks", "_log", "_wood", "chain", "_fence", "_wall", "_slab[type=top", "_slab[type=double",
             "hay_block", "cobblestone", "stone", "bricks", "_stairs")
    for (lx, ly, lz), b in m.cells.items():
        if not b.startswith("lantern[hanging=true"):
            continue
        x, y, z = lx + m.min[0], ly + m.min[1], lz + m.min[2]
        above = m.get(x, y + 1, z)
        if above is None or "leaves" in above or not any(t in above for t in holds) or "fence_gate" in above:
            bad.append(((x, y, z), above))
    return bad


def hang_lanterns(m):
    """Give every hanging lantern something to hang from: a leaf over it
    becomes a stub of branch; open air over it is chained up to the first block
    within five cells that holds a chain; a lantern with nothing over it stands
    on a post instead, down to the floor under it."""
    for (x, y, z), above in unhung_lanterns(m):
        if above is not None and "leaves" in above:
            m.set(x, y + 1, z, m.pick(x, y + 1, z, BARK_X, 43))
            continue
        top = None
        for dy in range(1, 6):
            b = m.get(x, y + dy, z)
            if b is not None:
                top = y + dy if (b and not any(t in b for t in ("leaves", "lantern", "trapdoor"))) else None
                break
        if top is not None:
            for yy in range(y + 1, top):
                m.set(x, yy, z, CHAIN_Y)
            continue
        m.set(x, y, z, None)
        fy = y - 1
        while fy > m.min[1] and m.get(x, fy, z) is None:
            fy -= 1
        for yy in range(fy + 1, fy + 3):
            m.set(x, yy, z, POST)
        m.set(x, fy + 3, z, LANTERN_STAND)


def write(m, stem):
    hang_lanterns(m)
    bad = unhung_lanterns(m)
    if bad:
        raise SystemExit(f"{stem}: {len(bad)} hanging lantern(s) with nothing to hang from: {sorted(bad)}")
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
    # body climbs them (a step of two from the knuckle to the root). Between
    # them the glade opens onto the forest floor on every side.
    roots = [
        (38, 29, 38, 26),   # north
        (41, 30, 44, 27),   # north-east
        (41, 37, 45, 37),   # east
        (33, 41, 33, 45),   # south
        (30, 41, 27, 44),   # south-west
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
    # Ferns and fallen logs scattered round the glade's edge, low enough to step over.
    for x in range(x0 + 1, x1):
        for z in range(z0 + 1, z1):
            edge = x in (x0 + 1, x1 - 1) or z in (z0 + 1, z1 - 1)
            if edge and m.get(x, floor, z) is None and (x * 3 + z) % 5 == 0:
                m.set(x, floor, z, "fern")
    for (lx, lz, axis, n) in ((25, 36, "z", 3), (46, 40, "z", 3)):
        for i in range(n):
            x, z = (lx + i, lz) if axis == "x" else (lx, lz + i)
            m.set(x, floor, z, f"mangrove_log[axis={axis}]")
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
    # Lamp posts all round the trunk under the platform overhead.
    for (lx, lz) in ((26, 25), (28, 30), (34, 25), (41, 25), (45, 30), (46, 36), (45, 45), (37, 46), (29, 46), (25, 40),
                     (26, 33), (40, 46)):
        lamp_post(m, lx, lz, floor, 2)
    # Lanterns hung on chains from the platform overhead: one beside the
    # ladder's top rungs, the rest round the trunk, so the glade under the
    # deck reads as a lit room among roots.
    hanging_lantern(m, 28, 37, y1, 2)
    for (lx, lz) in ((28, 28), (36, 28), (44, 28), (44, 36), (44, 44), (36, 44), (28, 44)):
        hanging_lantern(m, lx, lz, y1, 3)
    # Contract: the glade's floor out to its open edge, the ladder shaft, the top rung's cell.
    m.space("glade", "open", (x0, floor, z0, x1, floor + 2, z1), (30, floor + 3, 35, 30, y1 - 1, 36))
    m.via("glade-ladder", (30, y1, 35, 30, y1, 36))
    top = floor + 3
    m.nobody("over-the-glade", "the tops of the buttress roots and the hanging lanterns: nobody climbs up here",
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
    corners = {(x0, z0), (x0, z1), (x1, z0), (x1, z1)}
    for (px, pz) in corners:
        m.set(px, y, pz, RAIL)
        m.set(px, y + 1, pz, None)
    posts = set()
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


def platform_contract(m, x0, z0, x1, z1, floor, vias, space="room", reason=None, extra_space=(), holes=()):
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
    m.space(space, "open", *(thlib.subtract(lo, vias) + collars + list(extra_space)))
    top = m.wmax()[1]
    if top >= floor + 2:
        mn, mx = m.min, m.wmax()
        hi = (mn[0], floor + 2, mn[2], mx[0], top, mx[2])
        m.nobody("overhead", reason or "rail tops, posts, roofs and lanterns, all over a body's head",
                 *thlib.subtract(hi, list(vias) + collars + list(extra_space) + list(holes)))


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
    for (lx, lz) in ((24, 24), (24, 32), (24, 40), (24, 47), (31, 47), (47, 24), (47, 32), (47, 41), (39, 47)):
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
    rest_region(m, "around", "the beams under the deck, the stringers and the rail tops: no way onto any of them")
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
    bridge("long-bridge", "node/long-bridge", "x", (57, 70), [(56, 80), (55, 81), (54, 82), (53, 83), (52, 84), (51, 85)],
           "west", 50, 49, 85, 70, (34, 36), (34, 36), 80, DECK, (57, 69), "edge/hearth-long", "edge/loom-long")


def low_bridge():
    bridge("low-bridge", "node/low-bridge", "z", (55, 68), [(54, 82), (53, 83), (52, 84), (51, 85)],
           "north", 50, 49, 85, 68, (34, 36), (34, 36), 82, DECK_WORN, (55, 67), "edge/hearth-low", "edge/seed-low")


def high_bridge():
    bridge("high-bridge", "node/high-bridge", "z", (45, 60), [(61, 80), (62, 81), (63, 82), (64, 83)],
           "south", 65, 66, 83, 45, (78, 80), (78, 80), 80, DECK, (46, 60), "edge/watch-high", "edge/loom-high")


# ---------------------------------------------------------------- trees on the ground
def buttress_roots(m, cx, cz, r, ground, angles, reach, top_h=6, thick=2, salt=17):
    """Roots running out from the trunk's foot along the given compass
    angles (degrees, 0 = +x, 90 = +z), falling from top_h to one course at
    `reach` from the centre; moss carpets on their backs."""
    for ang in angles:
        t = math.radians(ang)
        dx, dz = math.cos(t), math.sin(t)
        n = int(reach - r) + 1
        for i in range(n):
            d = r - 0.5 + i
            px, pz = cx + dx * d, cz + dz * d
            hgt = max(1, round(top_h - (top_h - 1) * i / max(1, n - 1)))
            for ox in range(thick):
                for oz in range(thick):
                    x, z = math.floor(px - thick / 2 + 0.5) + ox, math.floor(pz - thick / 2 + 0.5) + oz
                    for dy in range(hgt):
                        if m.get(x, ground + dy, z) is None or m.get(x, ground + dy, z) == "moss_carpet":
                            P(m, x, ground + dy, z, BARK, salt)
                    if m.get(x, ground + hgt, z) is None:
                        m.set(x, ground + hgt, z, "moss_carpet")


def ground_plot(m, x0, z0, x1, z1, y):
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            P(m, x, y, z, FOREST_FLOOR, 3)


def ferns(m, x0, z0, x1, z1, y, every=3):
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if m.get(x, y, z) is None and m.get(x, y - 1, z) in (None,) and False:
                pass
            below = m.get(x, y - 1, z)
            if m.get(x, y, z) is None and below and thlib.bid_of(below) in ("minecraft:moss_block", "minecraft:podzol"):
                if m.pick(x, y, z, [(every, ""), (1, "f")], 21) == "f":
                    m.set(x, y, z, m.pick(x, y, z, [(3, "fern"), (1, "short_grass"), (1, "moss_carpet")], 22))


def gateway(m, along, fixed, a0, a1, y0, y1):
    """The head of a bridge's gateway over a mouth on a ring row: a beam on the
    gap posts, a plank course, a thatch cap. along = the axis the row runs on
    ('x' for a north or south row at z = fixed, 'z' for an east or west row)."""
    for a in range(a0, a1 + 1):
        x, z = (a, fixed) if along == "x" else (fixed, a)
        for y in range(y0, y1 + 1):
            if y == y0:
                m.set(x, y, z, f"stripped_spruce_log[axis={along}]")
            elif y == y1:
                m.set(x, y, z, THATCH)
            else:
                m.set(x, y, z, "spruce_planks")


# ---------------------------------------------------------------- the Loom House
LOOM = (80.0, 36.0)


def loom_house():
    h = thlib.handout(C, "node/loom-house", PREFABS)
    m = thlib.Model(h)
    (x0, y0, z0), (x1, y1, z1) = h["world_min"], m.wmax()
    cx, cz = LOOM
    ground = y0               # 59, the gully floor
    fy = 79                   # the floor course, the trunk's cut top
    floor = 80
    ground_plot(m, x0 + 1, z0 + 1, x1 - 1, z1 - 1, ground)
    # The topped trunk, flared at its foot, cut flat at the floor course.
    for y in range(ground, fy):
        r = 5.0 + (1.6 if y <= ground + 2 else (0.8 if y <= ground + 5 else 0.0))
        trunk_layer(m, cx, cz, r, y)
    buttress_roots(m, cx, cz, 5.0, ground + 1, (20, 70, 115, 160, 205, 250, 295, 340), 8.2, top_h=5)
    ferns(m, x0 + 1, z0 + 1, x1 - 1, z1 - 1, ground + 1)
    # Beams and knee braces from the trunk to the deck's edges.
    for ang, axis in ((0, "x"), (90, "z"), (180, "x"), (270, "z")):
        t = math.radians(ang)
        dx, dz = round(math.cos(t)), round(math.sin(t))
        for d in range(5, 10):
            for w in (-1, 0):
                x = int(cx + dx * d + (w if dz else 0) - (1 if dx < 0 else 0))
                z = int(cz + dz * d + (w if dx else 0) - (1 if dz < 0 else 0))
                m.set(x, fy - 1, z, f"spruce_log[axis={axis}]")
        for k, d in enumerate((5, 6, 7)):
            for w in (-1, 0):
                x = int(cx + dx * d + (w if dz else 0) - (1 if dx < 0 else 0))
                z = int(cz + dz * d + (w if dx else 0) - (1 if dz < 0 else 0))
                m.set(x, fy - 4 + k, z, f"spruce_log[axis={axis}]")
    # The deck, with the trunk's end grain flush in the middle of it.
    deck(m, x0, z0, x1, z1, fy, skip=lambda x, z: (x + 0.5 - cx) ** 2 + (z + 0.5 - cz) ** 2 <= 25)
    for x, z in m.disc_cells(cx, cz, 5.0):
        m.set(x, fy, z, "mangrove_log[axis=y]")
    # Rail, open at the Long Bridge's mouth; the High Bridge's mouth is the rope gate.
    west_gap = [(71, z) for z in (34, 35, 36)]
    gate = [(x, 44) for x in (78, 79, 80)]
    rail_ring(m, x0, z0, x1, z1, floor, west_gap + gate)
    gate_state = "oak_fence[east=true,north=false,south=false,waterlogged=false,west=true]"
    m.role_names[thlib.full_state(gate_state)] = "rope-gate"
    for (gx, gz) in gate:
        for dy in range(3):
            m.set(gx, floor + dy, gz, gate_state)
    gateway(m, "x", 44, 77, 81, floor + 3, floor + 5)
    gateway(m, "z", 71, 33, 37, floor + 3, floor + 5)
    m.set(77, floor + 2, 43, "brown_wool")     # the knot, tied round the gate's west post
    # The lean-to over the two looms, thatched, open to the south.
    for (px, pz, ph) in ((81, 28, 5), (87, 28, 5), (81, 32, 3), (87, 32, 3)):
        for dy in range(ph):
            m.set(px, floor + dy, pz, POST)
    for x in range(81, 88):
        m.set(x, floor + 5, 28, THATCH)
        for z in (29, 30):
            m.set(x, floor + 4, z, THATCH)
        for z in (31, 32):
            m.set(x, floor + 3, z, THATCH)
    m.set(83, floor, 29, "loom[facing=south]")
    m.set(85, floor, 29, "loom[facing=south]")
    for z in (29, 30):
        m.set(87, floor, z, "red_wool" if z == 29 else "cyan_wool")
    m.set(86, floor, 29, "white_wool")
    hanging_lantern(m, 84, 30, floor + 3, 1)
    # Cloth drying on lines: posts, a line, the cloth hanging under it.
    colours = ["white_wool", "red_wool", "light_gray_wool", "brown_wool", "cyan_wool", "yellow_wool", "white_wool", "green_wool"]
    for (lx0, lz0, lx1, lz1) in ((74, 29, 74, 33), (74, 39, 74, 42)):
        for (px, pz) in ((lx0, lz0 - 1), (lx1, lz1 + 1)):
            for dy in range(4):
                m.set(px, floor + dy, pz, "spruce_fence")
        for i, z in enumerate(range(lz0, lz1 + 1)):
            m.set(lx0, floor + 3, z, "iron_chain[axis=z]")
            if i % 2 == 0 or True:
                m.set(lx0, floor + 2, z, colours[(z * 3) % len(colours)])
    # Lamp posts.
    for (lx, lz) in ((72, 28), (72, 43), (87, 43), (87, 37), (77, 28)):
        lamp_post(m, lx, lz, floor)
    # Under the deck, the forest floor round the trunk is walked: lamp
    # posts stand on it all round the trunk.
    for (lx, lz) in ((73, 30), (80, 28), (87, 30), (87, 36), (87, 42), (80, 43), (73, 42), (73, 36)):
        lamp_post(m, lx, lz, ground + 1, 2)
    # Contract.
    v_long = (71, floor, 34, 71, floor + 2, 36)
    bar = (78, floor, 44, 80, floor + 2, 44)
    m.via("loom-long", v_long)
    m.region("seam-loom-high", *bar)
    platform_contract(m, x0, z0, x1, z1, floor, [v_long, bar])
    rest_region(m, "under-the-deck", "the gully floor under the deck, the roots and the braces: nobody goes down there")
    m.ack = "a house on a topped tree: most of its frame is the gully floor and the trunk under its deck"
    m.entry = "room"
    m.edge(a="room", b="exterior", **{"class": "walk", "via": "loom-long"})
    m.edge(a="room", b="exterior", **{"class": "barred", "bar": {"region": "seam-loom-high", "block": "rope-gate"}})
    m.mark("node-loom-house", 81, floor, 34, "west")
    m.mark("unlock-loom-high", 79, floor, 42, "south")
    light_marks(m, "node/loom-house")
    write(m, "loom-house")


# ---------------------------------------------------------------- crowns
def leaf_mass(m, x0, y0, z0, x1, y1, z1, salt=31):
    """A chunky cube of leaves with its corners and edges bitten: the
    style sheet's cubic leaf masses."""
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            for z in range(z0, z1 + 1):
                ex = x in (x0, x1)
                ey = y in (y0, y1)
                ez = z in (z0, z1)
                edges = ex + ey + ez
                if edges == 3:
                    continue
                if edges == 2 and m.pick(x, y, z, [(1, "cut"), (1, "keep")], salt) == "cut":
                    continue
                if m.get(x, y, z) is None:
                    P(m, x, y, z, LEAVES, salt)


def branch(m, x, y, z, axis, length, thick=2, choices=None):
    """A square branch of `thick` x `thick` logs running `length` cells from
    (x, y, z) along +axis (negative length runs along -axis)."""
    step = 1 if length > 0 else -1
    for i in range(0, length, step):
        for a in range(thick):
            for b in range(thick):
                if axis == "x":
                    c = (x + i, y + a, z + b)
                elif axis == "z":
                    c = (x + a, y + b, z + i)
                else:
                    c = (x + a, y + i, z + b)
                m.set(*c, m.pick(*c, choices or (BARK_X if axis == "x" else BARK_Z if axis == "z" else BARK), 41))


def scenery_contract(m, reason):
    """Scenery: built to be seen and never entered. The contract's one
    space is the top two cells of a column of the frame with open air under
    them, where nothing stands; every other cell is out of walk. A sealed
    piece's floor gates excuse its standable leaf tops, and scenery owes no
    light (spec-0098 departure 36)."""
    (x0, y0, z0), (x1, y1, z1) = m.h["world_min"], m.wmax()
    cols = sorted(((x, z) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1)),
                  key=lambda c: (min(c[0] - x0, x1 - c[0]) + min(c[1] - z0, z1 - c[1]), c))
    for x, z in cols:
        if all(m.get(x, y, z) is None for y in range(y1 - 2, y1 + 1)):
            m.space("sky", "open", (x, y1 - 1, z, x, y1, z))
            break
    else:
        raise SystemExit("scenery: no empty column in the frame")
    rest_region(m, "seen-from-outside", reason)
    m.ack = "scenery: built to be seen from the camp and never entered"
    m.entry = "sky"


def hearth_crown():
    h = thlib.handout(C, "node/hearth-crown", PREFABS)
    m = thlib.Model(h)
    (x0, y0, z0), (x1, y1, z1) = h["world_min"], m.wmax()
    cx, cz = HEARTH
    # The trunk rises out of the Hearth House and thins into the crown.
    for y in range(y0, y0 + 11):
        r = 5.0 if y < y0 + 4 else (4.2 if y < y0 + 8 else 3.2)
        trunk_layer(m, cx, cz, r, y)
    # Four great arms at the first fork, four lesser ones higher up.
    branch(m, 40, 96, 35, "x", 9)     # east
    branch(m, 32, 96, 35, "x", -10)   # west
    branch(m, 35, 97, 40, "z", 9)     # south
    branch(m, 35, 97, 32, "z", -10)   # north
    branch(m, 39, 100, 39, "x", 6)
    branch(m, 39, 100, 39, "z", 6)
    branch(m, 32, 100, 32, "x", -6)
    branch(m, 32, 100, 32, "z", -6)
    for y in range(y0 + 11, y0 + 13):
        trunk_layer(m, cx, cz, 2.5, y)
    # The leaf masses: at the arm ends, the higher arms, and the crown's head.
    masses = [
        (44, 97, 31, 51, 102, 40),   # east
        (20, 97, 31, 27, 102, 40),   # west
        (31, 98, 44, 40, 103, 51),   # south
        (31, 98, 20, 40, 103, 27),   # north
        (40, 101, 40, 48, 106, 48),  # south-east
        (23, 101, 23, 31, 106, 31),  # north-west
        (40, 100, 22, 47, 104, 29),  # north-east
        (24, 100, 41, 31, 104, 48),  # south-west
        (29, 102, 29, 43, 107, 43),  # the head
    ]
    for i, b in enumerate(masses):
        leaf_mass(m, *b, salt=31 + i)
    scenery_contract(m, "the Hearth Tree's crown, seen from the camp and never entered: branches and leaves only")
    write(m, "hearth-crown")


# ---------------------------------------------------------------- the Seed House
SEED = (36.0, 78.0)


def seed_house():
    h = thlib.handout(C, "node/seed-house", PREFABS)
    m = thlib.Model(h)
    (x0, y0, z0), (x1, y1, z1) = h["world_min"], m.wmax()
    cx, cz = SEED
    ground, fy, floor, lid = 69, 81, 82, 88
    ground_plot(m, 28, 70, 43, 85, ground)
    for y in range(ground, 99):
        r = 4.0 + (1.6 if y <= ground + 2 else (0.8 if y <= ground + 4 else 0.0))
        if y > 92:
            r = 3.0 if y <= 96 else 2.2
        trunk_layer(m, cx, cz, r, y)
    buttress_roots(m, cx, cz, 4.0, ground + 1, (30, 100, 150, 210, 260, 320), 7.4, top_h=4)
    ferns(m, 28, 70, 43, 85, ground + 1)
    # Beams under the deck.
    for (x, z, axis, n) in ((40, 77, "x", 4), (28, 77, "x", 4), (35, 82, "z", 4), (35, 70, "z", 4)):
        branch(m, x, fy - 1, z, axis, n, thick=2, choices=[(1, f"spruce_log[axis={axis}]")])
    deck(m, 27, 69, 44, 86, fy)
    rail_ring(m, 27, 69, 44, 86, floor, [(x, 69) for x in (34, 35, 36)])
    gateway(m, "x", 69, 33, 37, floor + 3, floor + 5)
    # The storehouse hut in the south-west corner.
    cabin(m, 28, 80, 33, 84, floor, 4, "x", doors=[(33, 82, 2)], windows=[(30, 84)])
    for x in (29, 30, 31):
        m.set(x, floor, 81, "composter[level=6]")
    m.set(29, floor, 83, "hay_block[axis=x]")
    m.set(30, floor, 83, "hay_block[axis=x]")
    hanging_lantern(m, 31, 82, floor + 3, 1)
    # Baskets of nuts along the east rail, drying racks on the west side.
    for z in (73, 74, 76, 78, 79):
        m.set(43, floor, z, "composter[level=6]")
    for z in (71, 74):
        m.set(28, floor, z, "spruce_fence")
    for z in range(71, 75):
        m.set(28, floor + 1, z, "spruce_slab[type=bottom]")
    # The log press: two posts, a beam, the weight, the oil pot.
    for (px, pz) in ((40, 83), (43, 83)):
        m.set(px, floor, pz, POST)
        m.set(px, floor + 1, pz, POST)
    for x in range(40, 44):
        m.set(x, floor + 2, 83, "stripped_oak_log[axis=x]")
    m.set(41, floor, 83, "smooth_stone")
    m.set(42, floor, 83, "smooth_stone")
    m.set(42, floor + 1, 83, "polished_andesite")
    m.set(41, floor, 84, "cauldron")
    # Lanterns: under the crown's lowest beams, and on posts.
    for (lx, lz) in ((30, 72), (40, 72), (31, 78), (41, 79), (37, 84)):
        m.set(lx, lid, lz, "spruce_log[axis=y]")
        hanging_lantern(m, lx, lz, lid - 1, 2)
    for (lx, lz) in ((28, 76), (43, 85), (28, 85), (34, 85), (43, 70)):
        lamp_post(m, lx, lz, floor)
    # Under the deck, the mound round the trunk is walked: lamp posts stand
    # on it all round the trunk.
    for (lx, lz) in ((30, 72), (36, 71), (42, 72), (43, 78), (42, 84), (36, 85), (30, 84), (29, 78)):
        lamp_post(m, lx, lz, ground + 1, 2)
    # The crown, in the declared roof zone: arms from the trunk, leaf masses.
    branch(m, 39, 90, 77, "x", 8)
    branch(m, 32, 90, 77, "x", -8)
    branch(m, 35, 91, 81, "z", 7)
    branch(m, 35, 91, 74, "z", -6)
    for b in ((41, 92, 72, 48, 97, 83), (23, 92, 72, 30, 97, 83), (30, 93, 82, 41, 98, 90),
              (30, 93, 69, 41, 98, 75), (28, 97, 70, 44, 103, 86)):
        leaf_mass(m, *b)
    v = (34, floor, 69, 36, floor + 2, 69)
    m.via("seed-low", v)
    platform_contract(m, 27, 69, 44, 86, floor, [v])
    rest_region(m, "under-the-deck", "the mound under the deck, the roots and the beams: nobody goes down there")
    m.ack = "a house in a tree: its frame is mostly the mound under the deck and the crown over it"
    m.entry = "room"
    m.edge(a="room", b="exterior", **{"class": "walk", "via": "seed-low"})
    m.mark("node-seed-house", 41, floor, 77, "north")
    light_marks(m, "node/seed-house")
    write(m, "seed-house")


# ---------------------------------------------------------------- the Watch Tree
WATCH = (80.0, 78.0)


def watch_roots():
    h = thlib.handout(C, "node/watch-roots", PREFABS)
    m = thlib.Model(h)
    (x0, y0, z0), (x1, y1, z1) = h["world_min"], m.wmax()
    cx, cz = WATCH
    ground = y0
    ground_plot(m, x0 + 1, z0 + 1, x1 - 1, z1 - 1, ground)
    for y in range(ground, y1 + 1):
        r = 5.0 + (2.0 if y <= ground + 3 else (1.0 if y <= ground + 6 else 0.0))
        trunk_layer(m, cx, cz, r, y)
    buttress_roots(m, cx, cz, 5.0, ground + 1, (0, 45, 90, 135, 180, 225, 270, 315), 7.6, top_h=7)
    # Bushes and mossy logs close the ring between the roots, three high:
    # the tree's foot is seen from the forest floor and never stood in.
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if x in (x0, x1) or z in (z0, z1):
                for dy in range(1, 4):
                    if m.get(x, ground + dy, z) is None:
                        P(m, x, ground + dy, z, BUSH, 11)
    ferns(m, x0 + 1, z0 + 1, x1 - 1, z1 - 1, ground + 1)
    scenery_contract(m, "the Watch Tree's foot and roots, seen from the bridges and the forest floor and never entered")
    write(m, "watch-roots")


def watch_house():
    h = thlib.handout(C, "node/watch-house", PREFABS)
    m = thlib.Model(h)
    (x0, y0, z0), (x1, y1, z1) = h["world_min"], m.wmax()
    cx, cz = WATCH
    fy, floor = y0, y0 + 1     # 83, 84
    for y in range(fy, y1 + 1):
        trunk_layer(m, cx, cz, 5.0, y)
    deck(m, x0, z0, x1, z1, fy)
    rail_ring(m, x0, z0, x1, z1, floor, [(x, z0) for x in (78, 79, 80)])
    # The ladder up the bark to the crown's landing; its top rung is the crown's.
    ladder(m, 74, 77, 78, floor, y1, "west")
    # The sentry hut, south-east of the trunk.
    cabin(m, 83, 81, 88, 86, floor, 4, "x", doors=[(85, 81, 2)], windows=[(88, 83), (83, 84)])
    m.set(87, floor, 84, "hay_block[axis=z]")
    m.set(87, floor, 85, "hay_block[axis=z]")
    m.set(84, floor, 85, "spruce_trapdoor[facing=north,half=top,open=false,powered=false,waterlogged=false]")
    hanging_lantern(m, 85, 83, floor + 3, 1)
    for (lx, lz) in ((70, 68), (70, 87), (89, 68), (77, 87), (89, 77), (70, 75), (82, 87), (89, 87), (82, 68), (76, 82)):
        lamp_post(m, lx, lz, floor)
    # The platform lives under the Watch Crown's canopy: lanterns hang on
    # chains from its underside all round the trunk, so the deck reads as a
    # lit room under the leaves.
    for (lx, lz) in ((72, 70), (80, 70), (87, 70), (72, 86), (79, 86), (71, 80), (87, 77)):
        hanging_lantern(m, lx, lz, y1, 3)
    v = (78, floor, z0, 80, floor + 2, z0)
    m.via("watch-high", v)
    shaft = (74, floor + 2, 77, 74, y1 - 1, 78)
    top = (74, y1, 77, 74, y1, 78)
    m.via("watch-ladder", top)
    platform_contract(m, x0, z0, x1, z1, floor, [v], extra_space=[shaft], holes=[top])
    m.entry = "room"
    m.edge(a="room", b="exterior", **{"class": "walk", "via": "watch-high"})
    m.edge(a="room", b="exterior", **{"class": "walk", "via": "watch-ladder"})
    m.mark("node-watch-house", 79, floor, 70, "north")
    light_marks(m, "node/watch-house")
    write(m, "watch-house")


def rail_around(m, cells, y, height, skip=()):
    """A fence rail on every cell beside a set of floor cells (8-neighbours)
    that is not itself floor, trunk or skipped."""
    cells = set(cells)
    out = set()
    for (x, z) in cells:
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                n = (x + dx, z + dz)
                if n in cells or n in skip:
                    continue
                if m.get(n[0], y, n[1]) is not None:
                    continue
                out.add(n)
    for (x, z) in out:
        for dy in range(height):
            m.set(x, y + dy, z, RAIL)
    return out


def watch_crown():
    h = thlib.handout(C, "node/watch-crown", PREFABS)
    m = thlib.Model(h)
    (x0, y0, z0), (x1, y1, z1) = h["world_min"], m.wmax()
    cx, cz = WATCH
    fy = y0                   # 92, the landing's planks
    landing_y = fy + 1        # 93
    ring_fy, ring_y = 111, 112
    LX = 74                   # the ladder's column, on the trunk's west face
    for y in range(fy, ring_fy + 1):
        trunk_layer(m, cx, cz, 5.0, y)
    for y in range(ring_fy + 1, 119):
        trunk_layer(m, cx, cz, 3.0 if y < 116 else 2.0, y)
    # The landing at the first fork, west of the trunk, round the ladder.
    land = [(x, z) for x in range(70, 75) for z in range(73, 84)
            if (x + 0.5 - cx) ** 2 + (z + 0.5 - cz) ** 2 > 25]
    for (x, z) in land:
        P(m, x, fy, z, DECK, 5)
    rail_around(m, land, landing_y, 2)
    for (lx, lz) in ((70, 73), (70, 83)):
        for dy in range(2):
            m.set(lx, landing_y + dy, lz, POST)
        m.set(lx, landing_y + 2, lz, LANTERN_STAND)
    # Branches out from the fork and the crown's leaf masses round the climb.
    branch(m, 85, 98, 77, "x", 5)
    branch(m, 75, 101, 80, "x", -4)
    branch(m, 79, 100, 83, "z", 5)
    branch(m, 79, 97, 73, "z", -5)
    masses = [
        (84, 96, 71, 89, 104, 84),   # east lobe
        (77, 98, 83, 88, 105, 87),   # south lobe
        (75, 95, 68, 86, 102, 72),   # north lobe
        (70, 99, 68, 74, 106, 72),   # north-west, over the landing
        (70, 99, 84, 74, 106, 87),   # south-west, over the landing
        (70, 103, 73, 73, 107, 83),  # west, round the climb
        (75, 104, 71, 88, 108, 85),  # the crown's top, under the lookout
    ]
    for i, b in enumerate(masses):
        leaf_mass(m, *b, salt=51 + i)
    # The Watch House's ladder tops out in the landing's hole; the crown's own
    # ladder starts on the landing beside it and climbs the bark to the ring.
    for z in (77, 78):
        m.set(LX, fy, z, "ladder[facing=west]")
    for y in range(landing_y, ring_fy + 1):
        m.set(LX, y, 79, "ladder[facing=west]")
    for (x, z) in land:
        for y in range(landing_y, landing_y + 3):
            if m.get(x, y, z) and "leaves" in m.get(x, y, z):
                m.set(x, y, z, None)
    # The ladder runs in a flute of the bark: ribs either side of it, clear
    # air west of it down to the landing, so a climber has nothing to step
    # off onto but the landing and the ring.
    for y in range(landing_y + 2, ring_fy + 1):
        for z in (78, 80):
            m.set(LX, y, z, m.pick(LX, y, z, BARK))
    for y in range(landing_y, ring_fy):
        m.set(LX - 1, y, 79, None)
    for y in range(landing_y + 4, ring_fy - 1, 4):
        for z in (78, 80):
            m.set(LX - 2, y + 1, z, m.pick(LX - 2, y + 1, z, LEAVES))
            m.set(LX - 2, y, z, LANTERN_HANG)
            m.set(LX - 2, y - 1, z, None)
    # The crown's floor course is its underside: leaves round the landing.
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if m.get(x, fy, z) is None:
                P(m, x, fy, z, LEAVES, 61)
    # The Crown Lookout: a ring of planks round the trunk, railed one fence high,
    # over every other crown in the camp.
    ring = [(x, z) for x, z in m.disc_cells(cx, cz, 7.5) if (x + 0.5 - cx) ** 2 + (z + 0.5 - cz) ** 2 > 9]
    for (x, z) in ring:
        if (x, z) == (LX, 79):
            continue
        if m.get(x, ring_fy, z) is None or (x + 0.5 - cx) ** 2 + (z + 0.5 - cz) ** 2 > 25:
            P(m, x, ring_fy, z, DECK, 7)
    for (x, z) in ring:
        for y in range(ring_y, ring_y + 4):
            m.set(x, y, z, None)
    rail_around(m, ring, ring_y, 1)
    for (lx, lz) in ((88, 78), (80, 86), (86, 72), (74, 84), (86, 84), (84, 70), (72, 82)):
        if m.get(lx, ring_y, lz) == RAIL:
            m.set(lx, ring_y + 1, lz, LANTERN_STAND)
    # The last branches over the ring, their leaves, and the lantern hook.
    branch(m, 74, 116, 73, "x", 5, thick=1)
    m.set(74, 115, 73, "iron_chain[axis=y]")
    branch(m, 78, 117, 74, "z", -3, thick=1)
    branch(m, 78, 117, 81, "z", 3, thick=1)
    for i, b in enumerate(((76, 118, 72, 84, 121, 84), (74, 117, 75, 77, 120, 81), (83, 118, 74, 87, 120, 77))):
        leaf_mass(m, *b, salt=71 + i)
    for (lx, lz) in ((82, 81), (78, 75), (82, 75), (78, 81)):
        hanging_lantern(m, lx, lz, 117, 4)
    for (x, z) in ring:
        for y in range(ring_y, ring_y + 2):
            if m.get(x, y, z) and "leaves" in m.get(x, y, z):
                m.set(x, y, z, None)
    m.set(74, 114, 73, None)
    # Contract: the landing, the lookout, and the ladder that climbs between them.
    land_boxes = [(x, landing_y, z, x, landing_y + 1, z) for (x, z) in land if (x, z) != (LX, 79)]
    m.space("landing", "open", *land_boxes)
    m.space("lookout", "open", *[(x, ring_y, z, x, ring_y + 2, z) for (x, z) in set(ring) | {(LX, 79)}])
    m.via("inner-ladder", (LX, landing_y, 79, LX, ring_fy, 79))
    m.via("watch-ladder", (LX, fy, 77, LX, fy, 78))
    rest_region(m, "leaves-and-bark", "the crown's leaves, branches and rails: the ladder is the only way through them")
    m.ack = "a tree's crown: most of what stands in it is leaves"
    m.entry = "landing"
    m.edge(a="landing", b="exterior", **{"class": "walk", "via": "watch-ladder"})
    m.edge(a="landing", b="lookout", **{"class": "climb", "rise": ring_y - landing_y, "via": "inner-ladder"})
    m.mark("node-watch-crown", 72, landing_y, 76, "east")
    m.mark("lantern-hook", 74, 114, 73, "south")
    write(m, "watch-crown")


PLACES = {"root-glade": root_glade, "hearth-house": hearth_house, "long-bridge": long_bridge,
          "low-bridge": low_bridge, "high-bridge": high_bridge, "loom-house": loom_house,
          "hearth-crown": hearth_crown, "seed-house": seed_house, "watch-roots": watch_roots,
          "watch-house": watch_house, "watch-crown": watch_crown}

if __name__ == "__main__":
    names = sys.argv[1:]
    if names == ["all"]:
        names = list(PLACES)
    for n in names:
        PLACES[n]()
