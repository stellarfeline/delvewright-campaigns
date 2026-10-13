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


def write(m, stem):
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


PLACES = {"glasshouse": glasshouse, "potting-room": potting_room, "stoke-hole": stoke_hole}

if __name__ == "__main__":
    names = sys.argv[1:]
    if names == ["all"]:
        names = list(PLACES)
    for n in names:
        PLACES[n]()
