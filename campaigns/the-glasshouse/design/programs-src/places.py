#!/usr/bin/env python3
"""Draws each place of The Glasshouse and writes programs/<place>.json.

    python3 places.py <place-stem> [...]     (or `all`)

Every frame comes from the place's handout (`delvec allocation`), fetched at
run time; the design is written in world coordinates, the same as DESIGN.md
section 3. `vox.py` compiles the drawing into a grammar program.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import vox  # noqa: E402

C = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PREFABS = os.environ.get("DELVEWRIGHT_PREFABS", "")
CAMPAIGN = "the-glasshouse"
G = 64  # datum/grade: the walk plane

# ---------------------------------------------------------------- materials
BRICK = "bricks"
COPING = "smooth_stone_slab[type=bottom]"
STONE = "stone_bricks"
PALE = "smooth_sandstone"
PALE_SLAB = "smooth_sandstone_slab[type=bottom]"
FRAME = "smooth_quartz"
GLASS = "glass"
PLANK = "oak_planks"
GRAVEL_PATH = [(5, "dirt_path"), (1, "gravel")]
LAWN = "grass_block[snowy=false]"
LEAVES = [(5, "oak_leaves[persistent=true]"), (2, "birch_leaves[persistent=true]")]
LIME_LEAVES = [(4, "birch_leaves[persistent=true]"), (2, "oak_leaves[persistent=true]")]
HEDGE = "spruce_leaves[persistent=true]"
LANTERN_HANG = "lantern[hanging=true]"
LANTERN_STAND = "lantern[hanging=false]"
CHAIN = "iron_chain[axis=y]"


def P(m, x, y, z, choices, salt=0):
    m.set(x, y, z, m.pick(x, y, z, choices, salt) if isinstance(choices, list) else choices)


def hang(m, x, z, y_from, drop):
    """A lantern on a chain, hung from the block at y_from + 1."""
    for y in range(y_from - drop + 2, y_from + 1):
        m.set(x, y, z, CHAIN)
    m.set(x, y_from - drop + 1, z, LANTERN_HANG)


def settle_paths(m):
    """A dirt path stays a path only under air: the game turns one with a block
    over it to dirt, so a path cell under a step, a post or a bench is laid as
    coarse dirt, which is what the game would leave there."""
    for (lx, ly, lz), b in list(m.cells.items()):
        if b.startswith("dirt_path") and m.cells.get((lx, ly + 1, lz)) not in (None, "air"):
            m.cells[(lx, ly, lz)] = "coarse_dirt"


def write(m, stem):
    settle_paths(m)
    prog = m.program(f"{CAMPAIGN}-{stem}")
    path = os.path.join(C, "programs", f"{stem}.json")
    json.dump(prog, open(path, "w"), indent=1)
    print(f"{stem}: {len(m.cells)} blocks, {len(prog['rules'])} rules, {len(prog['palette'])} roles, "
          f"faces {prog['shown_faces']}, {os.path.getsize(path)} bytes")


def frame(place):
    h = vox.handout(C, place, PREFABS)
    m = vox.Model(h)
    (x0, y0, z0), (x1, y1, z1) = h["world_min"], m.wmax()
    return h, m, x0, y0, z0, x1, y1, z1


# ---------------------------------------------------------------- the conservatory
def glass_roof_y(z):
    """The lean-to's glass, from the eaves over the front (z 14) to the back wall (z 3)."""
    return {14: 71, 13: 71, 12: 71, 11: 72, 10: 72, 9: 73, 8: 73, 7: 73, 6: 74, 5: 74, 4: 75}[z]


def glasshouse():
    h, m, x0, y0, z0, x1, y1, z1 = frame("node/glasshouse")
    fz = z1  # the front wall plane, z 14
    # Tiled floor.
    for x in range(x0 + 1, x1):
        for z in range(z0 + 1, z1):
            m.set(x, G - 1, z, "terracotta" if (x + z) % 2 else "brown_terracotta")
    # The back wall: the garden's tall north wall, brick to the top of the frame.
    m.box(x0, G, z0, x1, y1, z0, BRICK)
    # Front and ends: a brick plinth, then glass in white frames to the eaves.
    posts = {x0, x0 + 4, x0 + 8, x0 + 13, x0 + 17, x1}
    for x in range(x0, x1 + 1):
        m.set(x, G, fz, BRICK)
        for y in range(G + 1, 71):
            m.set(x, y, fz, FRAME if x in posts else GLASS)
        m.set(x, 71, fz, FRAME)
    for x in (x0, x1):
        for z in range(z0 + 1, fz):
            m.set(x, G, z, BRICK)
            top = glass_roof_y(z)
            for y in range(G + 1, top + 1):
                m.set(x, y, z, FRAME if z in (z0 + 1, z0 + 5, fz - 1) or y == top else GLASS)
    # The double door, 2 wide, in the middle of the front, framed.
    for x in (27, 28):
        for y in range(G, G + 3):
            m.set(x, y, fz, None)
    m.box(26, G, fz, 26, G + 3, fz, FRAME)
    m.box(29, G, fz, 29, G + 3, fz, FRAME)
    m.box(27, G + 3, fz, 28, G + 3, fz, FRAME)
    # The glass roof, stepped down from the back wall to the eaves, with white rafters.
    rafters = {x0 + 4, x0 + 8, x0 + 13, x0 + 17}
    for x in range(x0 + 1, x1):
        prev = None
        for z in range(z0 + 1, fz):
            top = glass_roof_y(z)
            m.set(x, top, z, FRAME if x in rafters else GLASS)
            if prev is not None and prev > top:
                for y in range(top + 1, prev):
                    m.set(x, y, z, FRAME if x in rafters else GLASS)
            prev = top
    # Plant staging along the back wall and under the front glass: oak plank
    # benches with flower pots, between beds of moss planted with ferns and flowers.
    plants = ["fern", "red_tulip", "cornflower", "fern", "lily_of_the_valley", "white_tulip", "oxeye_daisy"]

    def staging(x, z, i):
        if i % 3 == 0:
            m.set(x, G, z, PLANK)
            m.set(x, G + 1, z, "flower_pot")
        else:
            m.set(x, G, z, "moss_block")
            m.set(x, G + 1, z, plants[(x * 3 + z) % len(plants)])
    for i, x in enumerate(range(x0 + 2, x1 - 3)):
        staging(x, z0 + 1, i)
    for i, x in enumerate(list(range(x0 + 2, 25)) + list(range(31, x1 - 1))):
        staging(x, fz - 1, i)
    # The old lemon tree in its tub, in the middle of the house.
    tx, tz = 28, 8
    for x in range(tx - 1, tx + 2):
        for z in range(tz - 1, tz + 2):
            m.set(x, G, z, "spruce_planks")
    m.set(tx, G, tz, "rooted_dirt")
    for y in range(G + 1, G + 4):
        m.set(tx, y, tz, "oak_log[axis=y]")
    for x in range(tx - 2, tx + 3):
        for z in range(tz - 2, tz + 3):
            if abs(x - tx) == 2 and abs(z - tz) == 2:
                continue
            for y in range(G + 3, glass_roof_y(z)):
                if (x, z) == (tx, tz) and y < G + 4:
                    continue
                m.set(x, y, z, m.pick(x, y, z, [(6, "oak_leaves[persistent=true]"),
                                                (2, "flowering_azalea_leaves[persistent=true]")], 11))
    # The vent winding wheel: a geared wheel on the floor against the back wall at the east end.
    for x in (36, 37, 38):
        m.set(x, G, z0 + 1, None)
        m.set(x, G + 1, z0 + 1, None)
    m.set(37, G, z0 + 1, "grindstone[face=floor,facing=south]")
    m.set(37, G + 1, z0, "iron_bars")
    m.set(37, G + 2, z0, "iron_bars")
    # Two lanterns hung from the roof for the night.
    hang(m, 23, 9, glass_roof_y(9) - 1, 3)
    hang(m, 33, 9, glass_roof_y(9) - 1, 3)
    # Contract: one covered space under glass, the door to the garden.
    m.space("glass", "open", (x0 + 1, G, z0 + 1, x1 - 1, 70, fz - 1))
    m.nobody("roof", "the glass roof and the tops of the walls, over every body's head", (x0, 71, z0 + 1, x1, y1, fz))
    m.via("glass-door", (27, G, fz, 28, G + 2, fz))
    m.entry = "glass"
    m.edge(a="glass", b="exterior", **{"class": "walk", "via": "glass-door"})
    m.mark("node-glasshouse", 28, G, 12, "north")
    m.mark("vent-wheel", 37, G, z0 + 1, "south")
    write(m, "glasshouse")



# ---------------------------------------------------------------- the potting room
ROOF_TILE = "polished_granite_stairs"


def potting_room():
    h, m, x0, y0, z0, x1, y1, z1 = frame("node/potting-room")
    fz = z1          # front wall, z 14
    lid = 68         # the ceiling course
    hole = (43, 44, 7, 9)
    # Oak plank floor, the cellar hatch left open.
    for x in range(x0 + 1, x1):
        for z in range(z0 + 1, fz):
            if hole[0] <= x <= hole[1] and hole[2] <= z <= hole[3]:
                m.set(x, G - 1, z, "air")
                continue
            m.set(x, G - 1, z, "spruce_planks" if (x == hole[0] - 1 or x == hole[1] + 1) and hole[2] <= z <= hole[3] else PLANK)
    # Brick walls and a plank ceiling.
    for y in range(G, lid):
        for x in range(x0, x1 + 1):
            m.set(x, y, z0, BRICK)
            m.set(x, y, fz, BRICK)
        for z in range(z0, fz + 1):
            m.set(x0, y, z, BRICK)
            m.set(x1, y, z, BRICK)
    m.box(x0 + 1, lid, z0 + 1, x1 - 1, lid, fz - 1, "spruce_planks")
    # A tiled lean-to roof rising from the front eaves to the garden's north wall.
    def roof_y(z):
        return {14: 68, 13: 68, 12: 68, 11: 69, 10: 69, 9: 70, 8: 70, 7: 71, 6: 71, 5: 71}[z]
    for x in range(x0, x1 + 1):
        for z in range(z0, fz + 1):
            top = roof_y(z)
            for y in range(lid, top):
                m.set(x, y, z, BRICK if x in (x0, x1) or z == z0 else "spruce_planks")
            nxt = roof_y(z - 1) if z > z0 else top
            m.set(x, top, z, ROOF_TILE + "[facing=north,half=bottom]" if nxt > top or z == fz else "polished_granite_slab[type=bottom]")
    m.box(x0, lid, z0, x1, 71, z0, BRICK)
    # The door to the garden and a window beside it.
    m.set(44, G, fz, None)
    m.set(44, G + 1, fz, None)
    m.set(48, G + 1, fz, "glass_pane")
    m.set(49, G + 1, fz, "glass_pane")
    m.set(48, G + 2, fz, "glass_pane")
    m.set(49, G + 2, fz, "glass_pane")
    # A rail along the hatch's east side and its south end.
    for z in range(hole[2], hole[3] + 1):
        m.set(hole[1] + 1, G, z, "spruce_fence")
    for x in range(hole[0], hole[1] + 2):
        m.set(x, G, hole[3] + 1, "spruce_fence")
    # The potting bench along the back wall: oak planks, pots and candles;
    # seed drawers on the wall above it.
    for x in range(46, x1):
        m.set(x, G, z0 + 1, PLANK)
        m.set(x, G + 2, z0 + 1, "chiseled_bookshelf[facing=south,slot_0_occupied=false,slot_1_occupied=false,slot_2_occupied=false,slot_3_occupied=false,slot_4_occupied=false,slot_5_occupied=false]")
    for x, b in ((46, "flower_pot"), (47, "white_candle[candles=3,lit=true]"), (48, "flower_pot"), (49, "flower_pot"),
                 (50, "white_candle[candles=2,lit=true]"), (51, "flower_pot")):
        m.set(x, G + 1, z0 + 1, b)
    # Barrels of compost and a shelf of pots along the east wall.
    for z in (8, 9, 10):
        m.set(x1 - 1, G, z, "barrel[facing=up,open=false]")
    m.set(x1 - 1, G + 1, 9, "flower_pot")
    # The window sill with candles on it.
    m.set(48, G, fz - 1, PLANK)
    m.set(49, G, fz - 1, PLANK)
    m.set(48, G + 1, fz - 1, "white_candle[candles=4,lit=true]")
    m.set(49, G + 1, fz - 1, "flower_pot")
    # A lantern over the bench, a torch on the wall by the hatch.
    m.set(48, lid - 1, 8, LANTERN_HANG)
    m.set(x0 + 1, G + 2, 8, "wall_torch[facing=east]")
    # Contract.
    m.space("room", "enclosed", (x0 + 1, G, z0 + 1, x1 - 1, lid - 1, fz - 1))
    m.via("potting-door", (44, G, fz, 44, G + 1, fz))
    m.via("cellar-stair", (hole[0], G - 1, hole[2], hole[1], G - 1, hole[3]))
    m.nobody("roof", "the tiled roof over the ceiling", (x0, lid + 1, z0, x1, y1, fz))
    m.ack = "a small one-room house: the tiled roof over it holds more standable tops than its floor"
    m.entry = "room"
    m.edge(a="room", b="exterior", **{"class": "walk", "via": "potting-door"})
    m.edge(a="room", b="exterior", **{"class": "walk", "via": "cellar-stair"})
    m.mark("node-potting-room", 48, G, 10, "south")
    write(m, "potting-room")


# ---------------------------------------------------------------- the stove cellar
def stoke_hole():
    h, m, x0, y0, z0, x1, y1, z1 = frame("node/stoke-hole")
    F = 59
    # Stone floor and stone walls lining the earth.
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            m.set(x, F - 1, z, m.pick(x, F - 1, z, [(4, "stone_bricks"), (2, "cobblestone"), (1, "mossy_cobblestone")], 3))
            if x in (x0, x1) or z in (z0, z1):
                for y in range(F, F + 4):
                    m.set(x, y, z, m.pick(x, y, z, [(4, "stone_bricks"), (2, "cracked_stone_bricks"), (2, "cobblestone")], 5))
    # The stair up to the hatch: four treads rising north under the hole.
    for i, z in enumerate((10, 9, 8, 7)):
        for x in (43, 44):
            for y in range(F, F + i):
                m.set(x, y, z, "stone_bricks")
            m.set(x, F + i, z, "stone_bricks")
    # A stone wall between the stair and the cellar, open at the stair's foot.
    for z in (7, 8, 9):
        for y in range(F, F + 4):
            m.set(45, y, z, "stone_bricks")
    # The furnace against the north wall, its flue going up the wall; the coal heap.
    m.set(47, F, 7, "furnace[facing=south,lit=false]")
    for y in range(F + 1, F + 4):
        m.set(47, y, 7, "iron_bars")
    m.set(49, F, 7, "coal_block")
    m.set(50, F, 7, "coal_block")
    m.set(50, F, 8, "coal_block")
    # One lantern, hung at the foot of the stair.
    m.set(46, F + 3, 11, LANTERN_HANG)
    # Contract.
    m.space("cellar", "enclosed", (46, F, 7, 50, F + 3, 12), (43, F, 11, 45, F + 3, 12))
    m.space("stairhead", "enclosed", (43, F + 2, 7, 44, F + 2, 9))
    m.via("lower-flight", (43, F, 10, 45, F + 3, 10))
    m.via("hatch", (43, F + 3, 7, 44, F + 3, 9))
    m.entry = "stairhead"
    m.edge(a="cellar", b="stairhead", **{"class": "stair", "rise": 2, "via": "lower-flight"})
    m.edge(a="stairhead", b="exterior", **{"class": "stair", "rise": 0, "via": "hatch"})
    m.mark("node-stoke-hole", 48, F, 10, "north")
    m.mark("furnace", 47, F, 7, "south")
    write(m, "stoke-hole")



# ---------------------------------------------------------------- the walled garden
POOL = (25, 42, 28, 32)          # x0, x1, z0, z1 of the water
FRUIT_TREES = ((19, 20), (49, 20), (19, 39), (49, 39))
POSTS = ((23, 26), (44, 26), (23, 34), (44, 34), (26, 17), (29, 17), (43, 17), (45, 17), (51, 27), (51, 31),
         (33, 43), (35, 43))


def fruit_tree(m, tx, tz, salt):
    for y in range(G, G + 3):
        m.set(tx, y, tz, "oak_log[axis=y]")
    for y, r in ((G + 2, 2.3), (G + 3, 2.5), (G + 4, 2.3), (G + 5, 1.5)):
        for x, z in m.disc_cells(tx + 0.5, tz + 0.5, r):
            if (x, z) == (tx, tz) and y < G + 3:
                continue
            m.set(x, y, z, m.pick(x, y, z, LEAVES, salt))
    # A lantern hung from a low branch on the path side, for the evening.
    m.set(tx + 1, G + 2, tz, "oak_log[axis=x]")
    m.set(tx + 1, G + 1, tz, LANTERN_HANG)


def lantern_post(m, x, z):
    m.set(x, G, z, "stone_brick_wall")
    m.set(x, G + 1, z, LANTERN_STAND)


def garden():
    h, m, x0, y0, z0, x1, y1, z1 = frame("node/garden")
    W = 68                      # the wall's top course, under its coping
    px0, px1, pz0, pz1 = POOL
    # The walls: brick on the ring with a stone coping, where the ring is the garden's.
    def wall(x, z, top=W, skip=()):
        for y in range(G, top + 1):
            if y not in skip:
                m.set(x, y, z, BRICK)
        if top + 1 not in skip:
            m.set(x, top + 1, z, COPING)
    for x in range(x0, x1 + 1):
        if not (18 <= x <= 39 or 41 <= x <= 52):
            wall(x, z0)
        wall(x, z1)
    for z in range(z0 + 1, z1):
        if not (22 <= z <= 37):
            wall(x1, z)
        if 25 <= z <= 34:
            # Under the belvedere: brick to its floor course; over it a clipped
            # yew screen between the terrace and the garden, arched over the
            # opening at the head of the steps.
            for y in range(G, 67):
                m.set(x0, y, z, BRICK)
            for y in range(68, y1 + 1):
                if not 28 <= z <= 30:
                    m.set(x0, y, z, HEDGE)
        else:
            wall(x0, z)
    # Paths: round the pool, along the axis, to each door, and south.
    def path(xa, za, xb, zb):
        for x in range(min(xa, xb), max(xa, xb) + 1):
            for z in range(min(za, zb), max(za, zb) + 1):
                m.set(x, G - 1, z, m.pick(x, G - 1, z, GRAVEL_PATH, 2))
    path(px0 - 3, pz0 - 3, px1 + 3, pz1 + 3)      # the pool surround
    path(px1 + 3, 28, x1 - 1, 30)                   # to the east gate
    path(x0 + 1, 28, px0 - 3, 30)                   # to the belvedere steps
    path(27, z0 + 1, 28, pz0 - 3)                   # to the conservatory door
    path(43, z0 + 1, 45, pz0 - 3)                   # to the potting room door
    path(33, pz1 + 3, 35, z1 - 1)                   # south, to the wall
    # The reflecting pool: one course of still water edged in pale stone.
    for x in range(px0 - 1, px1 + 2):
        for z in range(pz0 - 1, pz1 + 2):
            edge = x in (px0 - 1, px1 + 1) or z in (pz0 - 1, pz1 + 1)
            m.set(x, G - 1, z, PALE if edge else "water[level=0]")
    # Low clipped hedges framing the four lawn quarters, open where a path crosses.
    def hedge(xa, za, xb, zb):
        for x in range(min(xa, xb), max(xa, xb) + 1):
            for z in range(min(za, zb), max(za, zb) + 1):
                if m.get(x, G - 1, z) is None:
                    m.set(x, G, z, HEDGE)
    for zz in (pz0 - 4, pz1 + 4):
        hedge(x0 + 2, zz, px0 - 5, zz)
        hedge(px0, zz, 26, zz)
        hedge(29, zz, 32, zz)
        hedge(36, zz, 42, zz)
        hedge(46, zz, x1 - 2, zz)
    # An oak bench against the potting room's front, between the two doors.
    for x in (31, 32, 33):
        m.set(x, G, z0 + 1, "oak_stairs[facing=north,half=bottom]")
    # The fruit trees, one to a quarter.
    for i, (tx, tz) in enumerate(FRUIT_TREES):
        fruit_tree(m, tx, tz, 20 + i)
    # Lanterns on short posts along the paths.
    for (x, z) in POSTS:
        lantern_post(m, x, z)
    # The steps up to the belvedere, against the west wall, 5 wide.
    for i, x in enumerate((17, 16, 15, 14)):
        for z in range(27, 32):
            for y in range(G, G + i + 1):
                m.set(x, y, z, PALE if z in (27, 31) else "smooth_sandstone")
    for z in range(27, 32):
        m.set(18, G - 1, z, PALE)
    # Contract: one open garden; the steps are a flight up to a landing at the wall.
    crowns = [(tx - 3, G + 2, tz - 3, tx + 3, y1, tz + 3) for (tx, tz) in FRUIT_TREES]
    posts = [(x, G, z, x, y1, z) for (x, z) in POSTS]
    flight = (15, G, 27, 17, y1, 31)
    top = (14, 68, 27, 14, y1, 31)
    under_top = (14, G, 27, 14, 67, 31)
    interior = (x0 + 1, G, z0 + 1, x1 - 1, y1, z1 - 1)
    doors = {"east-gate": (x1 - 1, G, 28, x1 - 1, G + 3, 30),
             "glass-door": (27, G, z0 + 1, 28, G + 2, z0 + 1),
             "potting-door": (44, G, z0 + 1, 44, G + 1, z0 + 1)}
    m.space("garden", "open", *vox.subtract(interior, posts + [flight, top, under_top] + list(doors.values())))
    for name, box in doors.items():
        m.via(name, box)
    m.space("steps-top", "open", top)
    m.via("flight", flight, under_top)
    m.via("terrace-steps", (x0, 68, 28, x0, 69, 30))
    m.nobody("posts", "the lantern posts along the paths: a wall post with a lantern on it, too tall to stand on", *posts)
    m.entry = "garden"
    m.edge(a="garden", b="steps-top", **{"class": "stair", "rise": 4, "via": "flight"})
    m.edge(a="steps-top", b="exterior", **{"class": "walk", "via": "terrace-steps"})
    for name in doors:
        m.edge(a="garden", b="exterior", **{"class": "walk", "via": name})
    m.mark("node-garden", 33, G, 37, "north")
    write(m, "garden")



# ---------------------------------------------------------------- the belvedere
def belvedere():
    h, m, x0, y0, z0, x1, y1, z1 = frame("node/belvedere")
    F = 68                      # the terrace's walk plane
    gx = x1                     # x 13: the garden's wall column, of which the terrace owns its floor course
    # The raised terrace: a stone-faced platform up to its paving.
    for x in range(x0, gx):
        for z in range(z0, z1 + 1):
            ring = x == x0 or z in (z0, z1)
            for y in range(G, F - 1):
                m.set(x, y, z, m.pick(x, y, z, [(5, STONE), (1, "mossy_stone_bricks"), (1, "cracked_stone_bricks")], 9)
                      if ring else "dirt")
            m.set(x, F - 1, z, STONE if ring else ("smooth_stone" if (x + z) % 2 else PALE))
    for z in range(z0, z1 + 1):
        m.set(gx, F - 1, z, PALE if 28 <= z <= 30 else STONE)
    # The balustrade on the three open sides, with lanterns on its west corners.
    for x in range(x0, gx):
        m.set(x, F, z0, "sandstone_wall")
        m.set(x, F, z1, "sandstone_wall")
    for z in range(z0, z1 + 1):
        m.set(x0, F, z, "sandstone_wall")
    m.set(x0, F + 1, z0, LANTERN_STAND)
    m.set(x0, F + 1, z1, LANTERN_STAND)
    # Two stone urns and an oak bench looking west.
    m.set(x0 + 1, F, z0 + 1, "decorated_pot[cracked=false,facing=east,waterlogged=false]")
    m.set(x0 + 1, F, z1 - 1, "decorated_pot[cracked=false,facing=east,waterlogged=false]")
    for z in (29, 30, 31):
        m.set(9, F, z, "oak_stairs[facing=east,half=bottom]")
    # Contract.
    steps = (gx - 1, F, 28, gx - 1, F + 1, 30)
    terrace = (x0 + 1, F, z0 + 1, gx - 1, y1, z1 - 1)
    m.space("terrace", "open", *vox.subtract(terrace, [steps]))
    m.via("terrace-steps", steps)
    m.nobody("balustrade", "the balustrade's top and the lanterns on it, at the terrace's edge over the drop",
             (x0, F, z0, gx - 1, y1, z0), (x0, F, z1, gx - 1, y1, z1), (x0, F, z0 + 1, x0, y1, z1 - 1))
    m.entry = "terrace"
    m.edge(a="terrace", b="exterior", **{"class": "walk", "via": "terrace-steps"})
    m.mark("node-belvedere", 7, F, 30, "west")
    write(m, "belvedere")



# ---------------------------------------------------------------- the lime walk
LIMES = ((58, 26), (62, 26), (66, 26), (58, 33), (62, 33), (66, 33))


def lime_tree(m, tx, tz, salt, lamp_dz=0):
    for y in range(G, G + 4):
        m.set(tx, y, tz, "birch_log[axis=y]")
    for y, r in ((G + 3, 2.0), (G + 4, 2.5), (G + 5, 2.5), (G + 6, 2.3), (G + 7, 1.8), (G + 8, 1.0)):
        for x, z in m.disc_cells(tx + 0.5, tz + 0.5, r):
            if (x, z) == (tx, tz) and y < G + 4:
                continue
            m.set(x, y, z, m.pick(x, y, z, LIME_LEAVES, salt))
    if lamp_dz:
        m.set(tx, G + 3, tz + lamp_dz, "birch_log[axis=z]")
        m.set(tx, G + 2, tz + lamp_dz, LANTERN_HANG)


def lime_walk():
    h, m, x0, y0, z0, x1, y1, z1 = frame("node/lime-walk")
    gx = x0                     # x 54: the garden's east wall, which the lime walk owns here
    # The garden wall and its gateway: brick, stone-capped piers with lanterns.
    for z in range(z0, z1 + 1):
        if 28 <= z <= 30:
            m.set(gx, 68, z, BRICK)
            m.set(gx, 69, z, COPING)
            continue
        pier = z in (27, 31)
        top = 70 if pier else 69
        for y in range(G, top):
            m.set(gx, y, z, PALE if pier else BRICK)
        m.set(gx, top, z, "smooth_stone" if pier else COPING)
        if pier:
            m.set(gx, top + 1, z, LANTERN_STAND)
    # The gravel walk from the open grass to the gate.
    for x in range(gx + 1, x1):
        for z in range(28, 31):
            m.set(x, G - 1, z, m.pick(x, G - 1, z, GRAVEL_PATH, 4))
    # Lime trees either side of it, two with lanterns hung toward the walk.
    for i, (tx, tz) in enumerate(LIMES):
        dz = (2 if tz < 29 else -2) if tx == 62 else 0
        lime_tree(m, tx, tz, 30 + i, dz)
    # Contract.
    crowns = [(gx + 1, G + 4, z0, x1, y1, 29), (gx + 1, G + 4, 30, x1, y1, z1)]
    trunks = [(tx, G, tz, tx, G + 2, tz) for (tx, tz) in LIMES]
    walk = (gx + 1, G, z0 + 1, x1 - 1, y1, z1 - 1)
    m.space("walk", "open", *vox.subtract(walk, crowns + trunks))
    m.via("east-gate", (gx, G, 28, gx, G + 3, 30))
    m.nobody("crowns", "the lime trees' crowns over the walk", *(crowns + trunks))
    m.nobody("wall", "the top of the garden wall and its gate piers", (gx, G, z0, gx, y1, 27), (gx, G, 31, gx, y1, z1),
             (gx, G + 4, 28, gx, y1, 30))
    m.ack = "an avenue of trees: their crowns hold more standable tops than the walk under them"
    m.entry = "walk"
    m.edge(a="walk", b="exterior", **{"class": "walk", "via": "east-gate"})
    m.mark("spawn", 67, G, 29, "west", role="entry")
    m.mark("node-lime-walk", 60, G, 29, "west")
    write(m, "lime-walk")


PLACES = {"lime-walk": lime_walk, "belvedere": belvedere, "garden": garden, "glasshouse": glasshouse, "potting-room": potting_room, "stoke-hole": stoke_hole}

if __name__ == "__main__":
    names = sys.argv[1:]
    if names == ["all"]:
        names = list(PLACES)
    for n in names:
        PLACES[n]()
