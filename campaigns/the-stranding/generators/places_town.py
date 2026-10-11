"""Act 1, Wrackham: the town on its cliff terraces, its harbour and its arm.

Palette (block names chosen against the reference sheet's grey slate-and-rubble
fishing town, recorded in GENERATION.md): slate roofs in deepslate tiles, rubble
walls in cobblestone and stone bricks with mossy patches, timber in spruce and
dark oak, limewash in calcite, cobbled lanes, lanterns at doors."""

import random

import mapmodel as M
from kit import Piece, AIR, boxcells, ground, ring_cells, INWARD, seam_box
from blocks import S, stairs, slab, is_full
import arch
from common import (leftovers_no_body, space_claim, node_mark, station_mark, stations, wall_seams, shell_box,
                    roof, roof_no_body, chimney, lantern_post)

SLATE = "deepslate_tile"
COBBLE = S("minecraft:cobblestone")
MOSSY_COBBLE = S("minecraft:mossy_cobblestone")
STONE = S("minecraft:stone_bricks")
MOSSY = S("minecraft:mossy_stone_bricks")
CRACKED = S("minecraft:cracked_stone_bricks")
ANDESITE = S("minecraft:polished_andesite")
LIME = S("minecraft:calcite")
PLANK = S("minecraft:spruce_planks")
DARK = S("minecraft:dark_oak_planks")
LOG = S("minecraft:spruce_log", axis="y")
DLOG = S("minecraft:dark_oak_log", axis="y")
GRAVEL = S("minecraft:gravel")
PACKED = S("minecraft:packed_mud")
DIRT = S("minecraft:dirt")
GRASS = S("minecraft:grass_block", snowy=False)
WALL = S("minecraft:cobblestone_wall")
MWALL = S("minecraft:mossy_cobblestone_wall")
FENCE = S("minecraft:spruce_fence")
DFENCE = S("minecraft:dark_oak_fence")
PANE = S("minecraft:glass_pane")
GLASS = S("minecraft:glass")
BARREL = S("minecraft:barrel", facing="up", open=False)
SMOOTH_SLAB = slab("smooth_stone")


def rng(node, salt=0):
    return random.Random(hash((node, salt)) & 0xFFFFFFFF if False else (sum(map(ord, node)) * 7919 + salt))


def mix(r, items):
    tot = sum(w for _, w in items)
    v = r.random() * tot
    for b, w in items:
        v -= w
        if v <= 0:
            return b
    return items[-1][0]


RUBBLE = [(COBBLE, 5), (STONE, 3), (MOSSY_COBBLE, 1), (MOSSY, 1)]
COBBLES = [(COBBLE, 6), (S("minecraft:andesite"), 2), (GRAVEL, 1), (MOSSY_COBBLE, 1)]


def walls(pc, block_fn, y0, y1, corner=None):
    x0, z0, x1, z1 = shell_box(pc)
    for y in range(y0, y1 + 1):
        for (x, z) in [(x, z0) for x in range(x0, x1 + 1)] + [(x, z1) for x in range(x0, x1 + 1)] + \
                [(x0, z) for z in range(z0 + 1, z1)] + [(x1, z) for z in range(z0 + 1, z1)]:
            if corner and x in (x0, x1) and z in (z0, z1):
                pc.set(x, y, z, corner)
            else:
                pc.set(x, y, z, block_fn(x, y, z))


def lid(pc, block):
    x0, z0, x1, z1 = shell_box(pc)
    pc.box(x0, pc.roof["lid_y"] if pc.roof else pc.space[1][1] + 1, z0, x1,
           pc.roof["lid_y"] if pc.roof else pc.space[1][1] + 1, z1, block)


def windows(pc, face, positions, y, block=None, h=1):
    x0, z0, x1, z1 = shell_box(pc)
    block = block or PANE
    for p in positions:
        for k in range(h):
            if face == "north":
                pc.set(p, y + k, z0, block)
            elif face == "south":
                pc.set(p, y + k, z1, block)
            elif face == "west":
                pc.set(x0, y + k, p, block)
            else:
                pc.set(x1, y + k, p, block)


def door_lamps(pc, s, block=None):
    """a lantern on a bracket each side of a doorway, on the inside face of the
    place's own wall when it owns the plane"""
    pass


def hang(pc, x, y, z):
    pc.set(x, y, z, arch.lantern(True))


def finish_building(pc, entry="room"):
    stations(pc)
    space_claim(pc, entry)
    node_mark(pc)
    roof_no_body(pc)
    leftovers_no_body(pc)
    return pc.finish(entry, shown_faces=["north", "south", "east", "west", "up"])


# ---------------------------------------------------------------------------
def coach_road(node):
    pc = Piece(node)
    r = rng(node)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    fy = pc.dy
    ground(pc, lambda x, z: mix(r, COBBLES), lambda x, z: S("minecraft:stone"))
    # the rock bank behind (north) and the drystone parapet on the drop (south)
    for x in range(sx0 - 1, sx1 + 2):
        h = 2 + (r.random() < 0.4) + (r.random() < 0.2)
        for y in range(fy, fy + h):
            pc.set(x, y, sz0 - 1, mix(r, [(S("minecraft:stone"), 3), (S("minecraft:andesite"), 2), (COBBLE, 1), (S("minecraft:tuff"), 1)]))
        pc.set(x, fy + h, sz0 - 1, mix(r, [(GRASS, 3), (S("minecraft:short_grass"), 1)]) if False else GRASS)
        pc.set(x, fy, sz1 + 1, mix(r, [(WALL, 4), (MWALL, 1)]))
    for z in range(sz0, sz1 + 1):
        for x in (sx0 - 1, sx1 + 1):
            for y in range(fy, fy + 3):
                pc.set(x, y, z, mix(r, [(S("minecraft:stone"), 3), (S("minecraft:andesite"), 1), (COBBLE, 1)]))
    # the coach stop's timber shelter at the east end
    cx, _, cz = pc.L(*M.STATIONS["anchor/coach-stop"][:3])
    for (x, z) in [(cx - 4, sz0), (cx + 3, sz0), (cx - 4, sz0 + 3), (cx + 3, sz0 + 3)]:
        for y in range(fy, fy + 3):
            pc.set(x, y, z, LOG)
    pc.box(cx - 5, fy + 3, sz0 - 1, cx + 4, fy + 3, sz0 + 4, slab("spruce", "bottom"))
    pc.box(cx - 4, fy + 3, sz0, cx + 3, fy + 3, sz0 + 3, PLANK)
    for x in range(cx - 3, cx + 3):
        pc.set(x, fy, sz0, stairs("spruce", "north"))
    pc.set(cx - 4, fy + 2, sz0 + 4, arch.lantern(True)) if False else None
    pc.set(cx - 3, fy + 2, sz0 + 3, arch.lantern(True))
    # lantern posts along the road
    for x in range(sx0 + 6, sx1 - 10, 14):
        lantern_post(pc, x, sz1)
    wall_seams(pc, "road", tread_fam="cobblestone", fill=COBBLE)
    stations(pc)
    space_claim(pc, "road", "open", cap=fy + 2)
    node_mark(pc)
    sx, sy, sz = pc.L(265, 96, 10)
    pc.mark("spawn", (sx, sy, sz), facing="south", role="entry")
    leftovers_no_body(pc)
    return pc.finish("road", shown_faces=["north", "south", "east", "west"])


def cliff_steps(node):
    pc = Piece(node)
    r = rng(node)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    fy = pc.dy
    top = sy1 + 1  # the lid course
    ground(pc, COBBLE, S("minecraft:stone"))
    walls(pc, lambda x, y, z: mix(r, RUBBLE), fy, top, corner=STONE)
    built = wall_seams(pc, "room", tread_fam="cobblestone", fill=COBBLE)
    # a roof stepping down the cliff with the flight: the lid follows the treads
    x0, z0, x1, z1 = shell_box(pc)
    flight = built.get("edge/coach-to-steps", {})
    for z in range(z0 + 1, z1):
        # height of the ceiling over this row: 4 over the tread, or the low room
        ys = [y for (x, y, zz) in flight.get("flight", []) + flight.get("landing", []) if zz == z]
        ceil_y = (max(ys) + 2) if ys else fy + 4
        ceil_y = min(ceil_y, top)
        for x in range(x0 + 1, x1):
            for y in range(ceil_y + 1, top + 1):
                if (x, y, z) not in pc.prog.region:
                    pc.set(x, y, z, mix(r, RUBBLE))
            if (x, ceil_y, z) not in pc.prog.region:
                pc.set(x, ceil_y, z, PLANK)
    # slate over the top
    rr = pc.roof
    arch.gable(pc, x0 - 1, z0 - 1, x1 + 1, z1 + 1, rr["lid_y"], "z", SLATE, mix(r, RUBBLE), max_courses=rr["courses"] + 1)
    for z in range(sz0 + 2, sz1, 4):
        windows(pc, "west", [z], fy + 1)
    hang(pc, sx0 + 2, fy + 3, sz1 - 1)
    hang(pc, sx0 + 2, top - 1, sz0 + 1)
    space_claim(pc, "room")
    node_mark(pc)
    roof_no_body(pc)
    leftovers_no_body(pc)
    return pc.finish("room", shown_faces=["north", "south", "east", "west", "up"])



# -- enclosed buildings ------------------------------------------------------
def building(node, wall_fn, roof_kind, roof_axis, floor_block, ceiling_block, furnish,
             corner=None, plinth=None, wins=(), roof_fam=SLATE, gable_block=None, tread="stone_brick",
             bar=None, threshold=None, chimneys=()):
    pc = Piece(node)
    r = rng(node)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    fy = pc.dy
    lid_y = pc.roof["lid_y"]
    ground(pc, floor_block, COBBLE)
    walls(pc, lambda x, y, z: wall_fn(r, x, y, z), fy, lid_y - 1, corner=corner)
    if plinth:
        walls(pc, lambda x, y, z: plinth, fy, fy, corner=corner)
    lid(pc, ceiling_block)
    roof(pc, roof_kind, roof_axis, roof_fam, gable_block or wall_fn(r, 0, 0, 0))
    for (x, z) in chimneys:
        chimney(pc, x, z, COBBLE)
    for face, posl, y, h in wins:
        windows(pc, face, posl, y, h=h)
    wall_seams(pc, "room", tread_fam=tread, fill=COBBLE, threshold=threshold or STONE,
               bar_block=bar)
    furnish(pc, r)
    return pc


def rubble_fn(r, x, y, z):
    return mix(r, RUBBLE)


def harbour_office(node):
    def furnish(pc, r):
        (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
        fy = pc.dy
        # the desk, the chart table, the tide board stuck at low, the hearth
        for x in range(sx0 + 1, sx0 + 4):
            pc.set(x, fy, sz0 + 2, stairs("spruce", "north", "top"))
        pc.set(sx0 + 2, fy, sz0 + 1, stairs("spruce", "south"))
        pc.set(sx1 - 1, fy, sz0 + 1, S("minecraft:cartography_table"))
        pc.set(sx1, fy, sz0 + 2, S("minecraft:lectern", facing="west", has_book=False, powered=False))
        # the tide board: a tall board on the north wall, its marker at the bottom
        for y in range(fy, fy + 4):
            pc.set(sx0 + 5, y, sz0 - 1, DARK)
        pc.set(sx0 + 5, fy, sz0, S("minecraft:spruce_trapdoor", facing="south", half="bottom", open=True, powered=False))
        pc.set(sx1, fy, sz1 - 1, BARREL)
        pc.set(sx1, fy + 1, sz1 - 1, arch.candle(3))
        hang(pc, (sx0 + sx1) // 2, pc.roof["lid_y"] - 1, (sz0 + sz1) // 2)
        hang(pc, sx0 + 1, pc.roof["lid_y"] - 1, sz1 - 1)
    pc = building(node, rubble_fn, "gable", "x", PLANK, PLANK, furnish, corner=STONE,
                  wins=[("south", [2, 7], 2, 2), ("north", [3], 3, 1), ("east", [4], 2, 2)],
                  chimneys=[(1, 5)])
    return finish_building(pc)


def coyle_house(node):
    pc = Piece(node)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    fy = pc.dy
    wx0, wx1, wz0, wz1 = sx0 - 1, sx1 + 1, sz0 - 1, sz1 + 1
    lid_y = pc.roof["lid_y"]
    pc.box(sx0, 0, sz0, sx1, fy - 1, sz1, PLANK)
    arch.rect_walls(pc, wx0, wz0, wx1, wz1, fy, lid_y - 1, LIME, corner=LOG)
    arch.rect_walls(pc, wx0, wz0, wx1, wz1, fy, fy, COBBLE, corner=LOG)
    pc.box(sx0, lid_y, sz0, sx1, lid_y, sz1, PLANK)
    arch.gable(pc, wx0 - 1, wz0 - 1, wx1 + 1, wz1, lid_y, "x", SLATE, LIME, top_block=slab(SLATE, "bottom"))
    pc.box(wx1 - 1, fy, sz0 + 2, wx1 - 1, pc.Y - 1, sz0 + 2, COBBLE)
    pc.set(wx1 - 2, fy, sz0 + 2, S("minecraft:campfire", lit=False, facing="west", signal_fire=False))
    pc.set(sx0 + 1, fy + 1, wz1, PANE)
    pc.set(sx1 - 1, fy + 1, wz0, PANE)
    arch.bed(pc, sx0, fy, sz0 + 1, "light_blue", "north")
    pc.set(sx0 + 1, fy, sz0, BARREL)
    pc.set(sx0, fy, sz0 + 2, S("minecraft:blue_carpet"))
    for c in [(sx0 + 1, sz0 + 2), (sx0 + 2, sz0 + 3), (sx0 + 2, sz0 + 4), (sx0 + 3, sz0 + 5)]:
        pc.set(c[0], fy - 1, c[1], S("minecraft:mud"))
    pic = {(0, 1): "black", (1, 1): "black", (2, 1): "black", (0, 2): "gray", (1, 2): "light_gray",
           (2, 2): "black", (3, 1): "black", (3, 2): "white"}
    for (dx, dy), col in pic.items():
        pc.set(sx0 + 2 + dx, fy + dy, wz0, S("minecraft:%s_wool" % col))
    pc.set(sx1 - 1, lid_y - 1, sz0 + 3, arch.lantern(True))
    pc.set(sx1, fy, sz1 - 1, S("minecraft:chest", facing="west", type="single", waterlogged=False))
    pc.set(sx1, fy + 1, sz1 - 1, arch.candle(2))
    wall_seams(pc, "room")
    return finish_building(pc)


def net_lofts(node):
    def plank_fn(r, x, y, z):
        return mix(r, [(PLANK, 5), (S("minecraft:stripped_spruce_log", axis="y"), 1)])

    def furnish(pc, r):
        (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
        fy = pc.dy
        # nets and floats: cobweb nets hung from the beams, barrels of floats
        for x in range(sx0 + 1, sx1, 3):
            pc.set(x, pc.roof["lid_y"] - 1, sz0 + 1, S("minecraft:cobweb"))
            pc.set(x + 1, pc.roof["lid_y"] - 1, sz0 + 2, S("minecraft:cobweb"))
        for x in (sx0, sx0 + 1, sx1):
            pc.set(x, fy, sz0, BARREL)
        pc.set(sx1 - 1, fy, sz0, S("minecraft:chest", facing="south", type="single", waterlogged=False))
        pc.set(sx0 + 4, fy, sz0, S("minecraft:white_wool"))
        pc.set(sx0 + 5, fy, sz0, S("minecraft:light_gray_wool"))
        hang(pc, sx0 + 2, pc.roof["lid_y"] - 1, sz1 - 1)
        hang(pc, sx1 - 2, pc.roof["lid_y"] - 1, sz1 - 2)
    pc = building(node, plank_fn, "gable", "x", PLANK, PLANK, furnish, corner=LOG, plinth=COBBLE,
                  roof_fam="spruce", wins=[("south", [2, 9], 2, 1), ("east", [3], 2, 1)])
    return finish_building(pc)


def fish_market(node):
    def wall_fn(r, x, y, z):
        return mix(r, [(PLANK, 4), (S("minecraft:stripped_spruce_log", axis="y"), 1)])

    def furnish(pc, r):
        (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
        fy = pc.dy
        x0, z0, x1, z1 = shell_box(pc)
        # timber frame posts on a stone footing
        for x in range(x0, x1 + 1, 4):
            for z in (z0, z1):
                for y in range(fy, pc.roof["lid_y"]):
                    if (x, y, z) not in pc.prog.region:
                        pc.set(x, y, z, LOG)
        # the arcade to the seawall: rails between the posts, open over them
        for x in range(x0 + 1, x1):
            if (x, fy, z1) not in pc.prog.region and pc.get(x, fy, z1) != LOG:
                pc.set(x, fy, z1, DFENCE)
                for y in range(fy + 1, pc.roof["lid_y"] - 1):
                    if pc.get(x, y, z1) != LOG and (x, y, z1) not in pc.prog.region:
                        pc.set(x, y, z1, AIR)
        # stone slabs on cobble legs, barrels, nets
        for z in range(sz0 + 3, sz1 - 2, 5):
            for x in range(sx0 + 4, sx1 - 3):
                pc.set(x, fy, z, SMOOTH_SLAB if x % 3 else COBBLE)
        for (x, z) in [(sx0, sz0), (sx0, sz0 + 1), (sx1, sz1 - 1), (sx1 - 1, sz1), (sx1, sz0 + 6)]:
            pc.set(x, fy, z, BARREL)
        for x in range(sx0 + 2, sx1 - 1, 4):
            pc.set(x, pc.roof["lid_y"] - 1, sz0 + 4, S("minecraft:cobweb"))
        for x in range(sx0 + 3, sx1, 6):
            for z in range(sz0 + 3, sz1, 6):
                hang(pc, x, pc.roof["lid_y"] - 1, z)
    pc = building(node, wall_fn, "gable", "z", COBBLE, PLANK, furnish, corner=LOG, plinth=STONE)
    space_claim(pc, "room", "open")
    stations(pc)
    node_mark(pc)
    roof_no_body(pc)
    leftovers_no_body(pc)
    return pc.finish("room", shown_faces=["north", "south", "east", "west", "up"])


def seamens_chapel(node):
    def furnish(pc, r):
        (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
        fy = pc.dy
        lid_y = pc.roof["lid_y"]
        cx = (sx0 + sx1) // 2
        # the Rubbing: a four-panel relief on the north wall
        panels = [
            ["  T  ", " TTT ", "  T  ", "BBBBB"],
            [" T   ", "TTT W", " T WW", "BBBBB"],
            ["  T  ", " WWW ", "WWWWW", "BBBBB"],
            [" ... ", "     ", "     ", "     "],
        ]
        cols = {"T": "light_gray_terracotta", "B": "black_terracotta", "W": "gray_terracotta", ".": "cracked_stone_bricks"}
        y_top = fy + 6
        for pi, pan in enumerate(panels[:2]):
            for row, line in enumerate(pan):
                for col, ch in enumerate(line):
                    x = sx0 + 1 + pi * 5 + col
                    y = y_top - row
                    if x > sx1:
                        continue
                    b = S("minecraft:%s" % cols[ch]) if ch in cols and ch != " " else S("minecraft:white_terracotta")
                    pc.set(x, y, sz0 - 1, b)
        # pews facing north, an altar, candles in numbers
        for z in range(sz0 + 4, sz1 - 3, 2):
            for x in list(range(sx0, cx - 1)) + list(range(cx + 2, sx1 + 1)):
                pc.set(x, fy, z, stairs("spruce", "south"))
        for x in range(cx - 1, cx + 2):
            pc.set(x, fy, sz0 + 1, S("minecraft:chiseled_stone_bricks"))
        for x in (cx - 1, cx + 1):
            pc.set(x, fy + 1, sz0 + 1, arch.candle(4))
        pc.set(cx, fy + 1, sz0 + 1, arch.candle(3))
        for (x, z) in [(sx0, sz0), (sx1, sz0), (sx0, sz1 - 1), (sx1, sz1 - 1), (sx0, sz0 + 8), (sx1, sz0 + 8)]:
            pc.set(x, fy, z, arch.candle(3))
        for z in range(sz0 + 2, sz1, 5):
            hang(pc, cx, lid_y - 1, z)
    pc = building(node, rubble_fn, "gable", "z", STONE, PLANK, furnish, corner=MOSSY,
                  wins=[("west", [109, 113, 117, 121], 0, 0)] and [], gable_block=COBBLE)
    # tall narrow windows down both sides, a bell-cote on the south gable
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    x0, z0, x1, z1 = shell_box(pc)
    for z in range(sz0 + 2, sz1 - 1, 4):
        for y in range(pc.dy + 2, pc.dy + 6):
            pc.set(x0, y, z, PANE)
            pc.set(x1, y, z, PANE)
    cx = (sx0 + sx1) // 2
    top = pc.Y - 1
    for y in range(top - 3, top + 1):
        for x in (cx - 1, cx + 1):
            pc.set(x, y, z1, STONE)
    pc.set(cx, top - 2, z1, S("minecraft:bell", attachment="ceiling", facing="south", powered=False))
    pc.set(cx, top, z1, STONE)
    # the hole in the floor over the crypt stair, and the stairwell its head needs
    for s in pc.seams:
        if s["face"] == "down":
            (ax, ay, az), (bx, by, bz) = s["cells"]
            cells = list(boxcells((ax, ay, az), (bx, by, bz)))
            well = [(x + 1, y, z) for (x, y, z) in cells]
            for c in cells + well:
                pc.set(*c, AIR)
            pc.claim(cells, "door-chapel-to-crypt")
            pc.claim(well, "room")
            pc.edge(a="room", b="exterior", **{"class": "walk"}, via="door-chapel-to-crypt")
            # a rail round the hole
            for (x, y, z) in cells + well:
                for dz in (-1, 1):
                    c2 = (x, y + 1, z + dz)
                    if c2[2] not in [c[2] for c in cells] and pc.owned(c2):
                        pass
    return finish_building(pc)


def chapel_crypt(node):
    pc = Piece(node)
    r = rng(node)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    fy = pc.dy
    # the crypt is cut into the rock: every owned cell stone, the room carved
    pc.box(0, 0, 0, pc.X - 1, pc.Y - 1, pc.Z - 1, STONE)
    for c in boxcells((sx0 + 1, fy, sz0 + 1), (sx1 - 1, sy1 - 1, sz1 - 1)):
        pc.set(*c, AIR)
    pc.box(sx0 + 1, fy - 1, sz0 + 1, sx1 - 1, fy - 1, sz1 - 1, S("minecraft:polished_andesite"))
    # niches of the drowned cut back into the rock down the west wall, a body's
    # length deep (the probe walks in from them: the crypt has no door in a wall)
    for z in range(sz0 + 2, sz1 - 1, 3):
        pc.set(sx0, fy, z, AIR)
        pc.set(sx0, fy + 1, z, AIR)
        pc.set(sx0, fy - 1, z, S("minecraft:polished_andesite"))
        pc.set(sx0 + 1, fy, z, S("minecraft:skeleton_skull", rotation=12, powered=False)) if False else None
    for z in range(sz0 + 3, sz1 - 1, 3):
        pc.set(sx1, fy + 1, z, S("minecraft:bone_block", axis="z"))
        pc.set(sx1, fy + 2, z, S("minecraft:cobweb"))
    # the founders' cupboard and the town's oldest chart
    pc.set(sx0 + 2, fy, sz0 + 1, S("minecraft:chest", facing="south", type="single", waterlogged=False))
    pc.set(sx0 + 3, fy, sz0 + 1, BARREL)
    # the stair up into the chapel: its top tread under the hole, where a body
    # arrives in the hole and steps up onto the chapel floor
    entry = "room"
    for s in pc.seams:
        if s["face"] == "up":
            (ax, ay, az), (bx, by, bz) = s["cells"]
            top = ay
            zs = range(min(az, bz), max(az, bz) + 1)
            treads = {ax + k: top - k for k in range(0, top - fy + 1)}
            for x, ty in treads.items():
                for z in zs:
                    pc.set(x, ty, z, stairs("stone_brick", "west"))
                    for yy in range(fy - 1, ty):
                        pc.set(x, yy, z, STONE)
                    for yy in range(ty + 1, sy1 + 1):
                        pc.set(x, yy, z, AIR)
            opening, landing, flight = [], [], []
            for x, ty in treads.items():
                for z in zs:
                    if ty == top:
                        opening.append((x, top, z))              # the allocated cell, over the top tread
                    elif ty == top - 1:
                        landing += [(x, ty, z), (x, top, z)]
                    elif ty == top - 2:
                        landing += [(x, yy, z) for yy in range(ty + 1, sy1 + 1)]
                        flight.append((x, ty, z))
                    elif ty >= fy + 1:
                        flight += [(x, yy, z) for yy in range(ty, sy1 + 1)]
            pc.claim(opening, "door-chapel-to-crypt")
            pc.claim(landing, "landing-chapel-to-crypt")
            pc.claim([c for c in flight if c not in landing and c not in opening], "flight-chapel-to-crypt")
            pc.space_decl("landing-chapel-to-crypt", "open")
            pc.edge(a="room", b="landing-chapel-to-crypt", **{"class": "stair"},
                    rise=(top - 1) - fy, via="flight-chapel-to-crypt")
            pc.edge(a="landing-chapel-to-crypt", b="exterior", **{"class": "stair"}, rise=0,
                    via="door-chapel-to-crypt")
            entry = "landing-chapel-to-crypt"
    for (x, z) in [(sx0 + 1, sz1 - 1), (sx1 - 1, sz0 + 2), (sx1 - 1, sz1 - 2)]:
        pc.set(x, fy, z, arch.candle(3))
    pc.set(sx0 + 4, fy, sz0 + 6, arch.candle(2))
    stations(pc)
    space_claim(pc, "room", "open")
    node_mark(pc)
    leftovers_no_body(pc)
    return pc.finish(entry)


def customs_house(node):
    def wall_fn(r, x, y, z):
        return mix(r, [(STONE, 4), (S("minecraft:polished_andesite"), 1), (CRACKED, 1)])

    def furnish(pc, r):
        (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
        fy = pc.dy
        lid_y = pc.roof["lid_y"]
        # the counter across the room, shelves of records, the ledger
        for x in range(sx0, sx1 + 1):
            if x not in (sx0 + 3, sx0 + 4):
                pc.set(x, fy, sz0 + 6, stairs("dark_oak", "south", "top"))
        for x in range(sx0, sx1 + 1):
            for y in range(fy, lid_y):
                pc.set(x, y, sz0, S("minecraft:bookshelf"))
        pc.set(sx1, fy, sz0 + 3, S("minecraft:lectern", facing="west", has_book=False, powered=False))
        for z in (sz0 + 9, sz0 + 12):
            pc.set(sx0, fy, z, BARREL)
        for x in range(sx0 + 2, sx1, 5):
            for z in (sz0 + 3, sz0 + 10):
                hang(pc, x, lid_y - 1, z)
    pc = building(node, wall_fn, "hipped", "x", S("minecraft:polished_andesite"), DARK, furnish,
                  corner=S("minecraft:chiseled_stone_bricks"), wins=[("east", [112, 117], 2, 2), ("west", [112, 117], 2, 2)],
                  bar=DARK, gable_block=S("minecraft:deepslate_tiles"))
    return finish_building(pc)


def whalers_shed(node):
    def wall_fn(r, x, y, z):
        return mix(r, [(DARK, 3), (PLANK, 2), (S("minecraft:stripped_dark_oak_log", axis="y"), 1)])

    def furnish(pc, r):
        (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
        fy = pc.dy
        lid_y = pc.roof["lid_y"]
        # a jawbone and ribs of the last whale they flensed, the try-pot, the racks
        for x in range(sx0 + 4, sx1 - 4, 2):
            pc.set(x, fy, sz0 + 6, S("minecraft:bone_block", axis="y"))
        for x in range(sx0 + 3, sx1 - 3):
            pc.set(x, fy, sz0 + 7, S("minecraft:bone_block", axis="x"))
        pc.set(sx1 - 2, fy, sz1 - 2, S("minecraft:cauldron"))
        pc.set(sx1 - 2, fy - 1, sz1 - 2, S("minecraft:campfire", lit=False, facing="north", signal_fire=False)) if False else None
        for z in range(sz0 + 1, sz1, 3):
            pc.set(sx0 - 1, fy + 2, z, S("minecraft:iron_chain", axis="y")) if False else None
        for z in range(sz0, sz1 + 1):
            pc.set(sx1, fy, z, BARREL) if z in (sz0, sz0 + 1) else None
        for x in range(sx0 + 3, sx1, 6):
            for z in range(sz0 + 3, sz1, 6):
                hang(pc, x, lid_y - 1, z)
    pc = building(node, wall_fn, "gable", "x", PLANK, PLANK, furnish, corner=DLOG, plinth=COBBLE,
                  roof_fam="dark_oak", gable_block=DARK, wins=[("north", [6, 12], 3, 1)])
    return finish_building(pc)


def ropewalk(node):
    def wall_fn(r, x, y, z):
        return mix(r, [(PLANK, 4), (S("minecraft:stripped_spruce_log", axis="y"), 1)])

    def furnish(pc, r):
        (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
        fy = pc.dy
        lid_y = pc.roof["lid_y"]
        # lines of rope stretched along the shed on posts
        for z in range(sz0 + 2, sz1 - 1, 6):
            for x in (sx0 + 1, sx1 - 1):
                pc.set(x, fy, z, FENCE)
        for z in range(sz0 + 2, sz1 - 1):
            for x in (sx0 + 1, sx1 - 1):
                if pc.get(x, fy, z) != FENCE:
                    pc.set(x, fy + 1, z, S("minecraft:tripwire", attached=False, disarmed=False, east=False, north=True, powered=False, south=True, west=False)) if False else None
        for z in range(sz0 + 3, sz1, 7):
            hang(pc, (sx0 + sx1) // 2, lid_y - 1, z)
    pc = building(node, wall_fn, "gable", "z", PLANK, PLANK, furnish, corner=LOG, plinth=COBBLE,
                  roof_fam="spruce", gable_block=PLANK)
    return finish_building(pc)


# -- open places ---------------------------------------------------------------
def harbour_lane(node):
    pc = Piece(node)
    r = rng(node)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    fy = pc.dy
    ground(pc, lambda x, z: mix(r, COBBLES), lambda x, z: S("minecraft:stone"))
    built = wall_seams(pc, "lane", tread_fam="stone_brick", fill=STONE, threshold=STONE)
    door_cells = {c for b in built.values() for c in b["cells"]}
    # the quay edge over the basin: a kerb of wall, bollards
    for x in range(sx0 - 1, sx1 + 2):
        c = (x, fy, sz1 + 1)
        if c not in door_cells and pc.owned(c):
            pc.set(*c, WALL if x % 6 else S("minecraft:andesite_wall"))
    # the north side: low walls between the houses, the cliff behind
    for x in range(sx0 - 1, sx1 + 2):
        c = (x, fy, sz0 - 1)
        if c not in door_cells and pc.owned(c):
            pc.set(*c, MWALL if r.random() < 0.3 else WALL)
    for z in range(sz0, sz1 + 1):
        for x in (sx0 - 1, sx1 + 1):
            c = (x, fy, z)
            if c not in door_cells and pc.owned(c):
                pc.set(*c, WALL)
                pc.set(x, fy + 1, z, WALL)
    for x in range(sx0 + 3, sx1, 9):
        if (x, fy, sz1) not in pc.prog.region:
            lantern_post(pc, x, sz1)
    stations(pc)
    space_claim(pc, "lane", "open", cap=fy + 2)
    node_mark(pc)
    leftovers_no_body(pc)
    return pc.finish("lane", shown_faces=["north", "south", "east", "west"])


def seawall(node):
    pc = Piece(node)
    r = rng(node)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    fy = pc.dy
    ground(pc, lambda x, z: mix(r, [(STONE, 4), (S("minecraft:smooth_stone"), 1), (CRACKED, 1)]), lambda x, z: STONE)
    built = wall_seams(pc, "seawall", tread_fam="stone_brick", fill=STONE, threshold=STONE)
    door_cells = {c for b in built.values() for c in b["cells"]}
    # the parapet over the flat, with bollards; the end walls
    for x in range(sx0 - 1, sx1 + 2):
        c = (x, fy, sz1 + 1)
        if c not in door_cells and pc.owned(c):
            pc.set(*c, STONE if x % 7 == 0 else S("minecraft:stone_brick_wall"))
            if x % 7 == 0:
                pc.set(x, fy + 1, sz1 + 1, S("minecraft:stone_brick_wall"))
    for z in range(sz0 - 1, sz1 + 2):
        for x in (sx0 - 1, sx1 + 1):
            for y in (fy, fy + 1):
                c = (x, y, z)
                if c not in door_cells and pc.owned(c):
                    pc.set(*c, STONE)
    # the north side between the doors: the fronts of the harbour buildings
    for x in range(sx0 - 1, sx1 + 2):
        for y in range(fy, fy + 2):
            c = (x, y, sz0 - 1)
            if c not in door_cells and pc.owned(c):
                pc.set(*c, mix(r, RUBBLE))
    # lanterns along the parapet, a lamp each side of the Customs House door
    for x in range(sx0 + 2, sx1, 8):
        if pc.get(x, fy, sz1) == AIR and (x, fy, sz1) not in pc.prog.region:
            lantern_post(pc, x, sz1)
    stations(pc)
    space_claim(pc, "seawall", "open", cap=fy + 2)
    node_mark(pc)
    leftovers_no_body(pc)
    return pc.finish("seawall", shown_faces=["north", "south", "east", "west"])


def slipway_stair(node):
    pc = Piece(node)
    r = rng(node)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    fy = pc.dy
    ground(pc, lambda x, z: mix(r, [(STONE, 3), (MOSSY, 1), (CRACKED, 1)]), lambda x, z: STONE)
    built = wall_seams(pc, "stair", tread_fam="stone_brick", fill=STONE, threshold=STONE, bar_block=S("minecraft:iron_bars"))
    door_cells = {c for b in built.values() for c in b["cells"]}
    for z in range(sz0, sz1 + 1):
        for x in (sx0 - 1, sx1 + 1):
            for y in range(fy, fy + 3):
                if (x, y, z) not in door_cells and pc.owned((x, y, z)):
                    pc.set(x, y, z, mix(r, [(STONE, 3), (MOSSY, 1)]))
    for x in range(sx0 - 1, sx1 + 2):
        for y in range(fy, fy + 3):
            c = (x, y, sz1 + 1)
            if c not in door_cells and pc.owned(c):
                pc.set(*c, STONE)
    lantern_post(pc, sx0, sz1 - 1)
    lantern_post(pc, sx1, sz1 - 1)
    stations(pc)
    space_claim(pc, "stair", "open", cap=fy + 2)
    node_mark(pc)
    leftovers_no_body(pc)
    return pc.finish("stair", shown_faces=["north", "south", "east", "west"])


def pier(node):
    pc = Piece(node)
    r = rng(node)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    fy = pc.dy
    for x in range(sx0 - 1, sx1 + 2):
        for z in range(sz0 - 1, sz1 + 2):
            pc.set(x, fy - 1, z, mix(r, [(PLANK, 4), (S("minecraft:stripped_spruce_log", axis="x"), 1)]))
    built = wall_seams(pc, "pier", tread_fam="spruce", fill=PLANK)
    door_cells = {c for b in built.values() for c in b["cells"]}
    for x in range(sx0 - 1, sx1 + 2):
        for z in (sz0 - 1, sz1 + 1):
            if (x, fy, z) not in door_cells and pc.owned((x, fy, z)):
                pc.set(x, fy, z, FENCE)
    for z in range(sz0, sz1 + 1):
        if (sx0 - 1, fy, z) not in door_cells:
            pc.set(sx0 - 1, fy, z, FENCE)
    for x in range(sx0 + 2, sx1, 8):
        lantern_post(pc, x, sz0 - 1, y=fy)
    stations(pc)
    space_claim(pc, "pier", "open", cap=fy + 2)
    node_mark(pc)
    leftovers_no_body(pc)
    return pc.finish("pier", shown_faces=["north", "south", "east", "west"])


def breakwater(node):
    pc = Piece(node)
    r = rng(node)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    fy = pc.dy
    ground(pc, lambda x, z: mix(r, [(STONE, 4), (S("minecraft:smooth_stone"), 1), (MOSSY, 1)]),
           lambda x, z: mix(r, [(STONE, 3), (MOSSY, 1), (COBBLE, 1)]))
    built = wall_seams(pc, "arm", fill=STONE, threshold=STONE)
    door_cells = {c for b in built.values() for c in b["cells"]}
    for z in range(sz0 - 1, sz1 + 2):
        for x in (sx0 - 1, sx1 + 1):
            c = (x, fy, z)
            if c not in door_cells and pc.owned(c):
                pc.set(*c, S("minecraft:stone_brick_wall"))
    for z in range(sz0 + 3, sz1, 10):
        lantern_post(pc, sx0, z)
    stations(pc)
    space_claim(pc, "arm", "open", cap=fy + 2)
    node_mark(pc)
    leftovers_no_body(pc)
    return pc.finish("arm", shown_faces=["north", "south", "east", "west"])



def high_street(node):
    pc = Piece(node)
    r = rng(node)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    fy = pc.dy
    ground(pc, lambda x, z: mix(r, COBBLES), lambda x, z: S("minecraft:stone"))
    wx0, wx1 = sx0 + 6, sx1 - 6      # the street runs between the two rows of houses
    # the two terraces: houses 5-8 long, two and three storeys
    rows = []
    for side in ("west", "east"):
        z = sz0
        k = 0
        while z <= sz1:
            L = 5 + (k * 3 + (1 if side == "east" else 0)) % 4
            z2 = min(sz1, z + L - 1)
            if sz1 - z2 < 4:
                z2 = sz1
            storeys = 2 + ((k + (side == "east")) % 3 == 0)
            rows.append((side, z, z2, storeys, k))
            z = z2 + 1
            k += 1
    for side, z0, z1, storeys, k in rows:
        hx0, hx1 = (sx0 - 1, wx0 - 1) if side == "west" else (wx1 + 1, sx1 + 1)
        face_x = wx0 - 1 if side == "west" else wx1 + 1
        eave = fy + 4 * storeys
        wall = [(LIME, 3), (COBBLE, 1)] if k % 3 == 1 else RUBBLE
        for x in range(hx0, hx1 + 1):
            for zz in range(z0, z1 + 1):
                for y in range(fy, eave):
                    pc.set(x, y, zz, mix(r, wall))
        # a slate gable over the row, ridge along the street, chimneys at the party walls
        span = hx1 - hx0 + 1
        for i in range((span + 1) // 2):
            y = eave + i
            a, b = hx0 + i, hx1 - i
            for zz in range(z0, z1 + 1):
                if a == b:
                    pc.set(a, y, zz, slab(SLATE, "bottom"))
                else:
                    pc.set(a, y, zz, stairs(SLATE, "east"))
                    pc.set(b, y, zz, stairs(SLATE, "west"))
                    for x in range(a + 1, b):
                        pc.set(x, y, zz, mix(r, wall))
        for (x, zz) in ((hx0 + span // 2, z0), (hx0 + span // 2, z1)):
            for y in range(eave, eave + span // 2 + 2):
                pc.set(x, y, zz, COBBLE)
        # the street front: a door in a recess, windows, some lit
        dz = (z0 + z1) // 2
        inward = -1 if side == "west" else 1
        pc.set(face_x, fy, dz, AIR)
        pc.set(face_x, fy + 1, dz, AIR)
        pc.set(face_x, fy + 2, dz, stairs("stone_brick", "west" if side == "west" else "east", "top"))
        arch.door(pc, face_x + inward, fy, dz, "dark_oak", "east" if side == "west" else "west")
        for st in range(storeys):
            wy = fy + 1 + 4 * st + (1 if st else 0)
            for wz in (z0 + 1, z1 - 1):
                if wz == dz or wz < z0 or wz > z1:
                    continue
                lit = (wz * 7 + st * 3 + k) % 5 == 0
                pc.set(face_x, wy, wz, PANE)
                pc.set(face_x + inward, wy, wz, S("minecraft:shroomlight") if lit else DARK)
        # a lantern on a bracket by some of the doors
        if k % 2 == 0:
            bx = face_x - inward
            pc.set(bx, fy + 3, dz + 1, FENCE)
            pc.set(bx, fy + 2, dz + 1, arch.lantern(True))
    # the walls closing the two ends of the street
    built = wall_seams(pc, "street", tread_fam="cobblestone", fill=COBBLE, threshold=STONE)
    door_cells = {c for b in built.values() for c in b["cells"]}
    for x in range(sx0 - 1, sx1 + 2):
        for y in range(fy, fy + 2):
            for z in (sz0 - 1, sz1 + 1):
                c = (x, y, z)
                if c not in door_cells and pc.owned(c) and pc.get(*c) == AIR:
                    pc.set(*c, mix(r, [(WALL, 3), (MWALL, 1)]) if y == fy else AIR)
        for y in range(fy, fy + 10):
            c = (x, y, sz0 - 1)
            if c not in door_cells and pc.owned(c) and pc.get(*c) == AIR and wx0 <= x <= wx1:
                pc.set(*c, mix(r, RUBBLE))
    stations(pc)
    space_claim(pc, "street", "open", cap=fy + 2,
                box=((wx0 - 1, fy, sz0), (wx1 + 1, sy1, sz1)))
    node_mark(pc)
    leftovers_no_body(pc, reason="the roofs and chimneys of the terraces, which nobody walks")
    return pc.finish("street", shown_faces=["north", "south", "east", "west", "up"])


def boatyard(node):
    pc = Piece(node)
    r = rng(node)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    fy = pc.dy
    MUD = S("minecraft:mud")
    ground(pc, lambda x, z: mix(r, [(MUD, 6), (PACKED, 2), (S("minecraft:coarse_dirt"), 1)]), lambda x, z: PACKED)
    # puddles left by the sea, each a single walled source
    for (x, z) in [(sx0 + 5, sz0 + 20), (sx0 + 13, sz0 + 30), (sx1 - 6, sz0 + 26), (sx0 + 24, sz1 - 3), (sx1 - 12, sz0 + 6)]:
        pc.set(x, fy - 1, z, S("minecraft:water", level=0))
        pc.set(x, fy - 2, z, PACKED)
    built = wall_seams(pc, "basin", tread_fam="stone_brick", fill=STONE, threshold=STONE)
    door_cells = {c for b in built.values() for c in b["cells"]}
    # the harbour walls: the south wall shuts the mouth the flat closed
    for x in range(sx0 - 1, sx1 + 2):
        for y in range(fy, fy + 3):
            c = (x, y, sz1 + 1)
            if c not in door_cells and pc.owned(c):
                pc.set(*c, mix(r, [(STONE, 3), (MOSSY, 2), (CRACKED, 1)]))
    for z in range(sz0, sz1 + 2):
        for x in (sx0 - 1, sx1 + 1):
            for y in range(fy, fy + 3):
                c = (x, y, z)
                if c not in door_cells and pc.owned(c):
                    pc.set(*c, mix(r, [(STONE, 3), (MOSSY, 2)]))
    # the town's boats lying on the mud, some on their sides
    def boat(x0, z0, L, axis, tilt):
        for i in range(L):
            if axis == "z":
                xs, zz = (x0, x0 + 1, x0 + 2), z0 + i
            else:
                xs, zz = (z0, z0 + 1, z0 + 2), x0 + i
            end = i in (0, L - 1)
            for j, w in enumerate(xs):
                cx, cz = (w, zz) if axis == "z" else (zz, w)
                if tilt and j == 2:
                    continue
                if end:
                    if j == 1:
                        pc.set(cx, fy, cz, DLOG if axis == "y" else S("minecraft:dark_oak_log", axis="y"))
                        pc.set(cx, fy + 1, cz, FENCE)
                    continue
                if j == 1:
                    pc.set(cx, fy, cz, S("minecraft:dark_oak_log", axis=axis))
                else:
                    pc.set(cx, fy, cz, PLANK)
                    pc.set(cx, fy + 1, cz, stairs("spruce", ("west" if j == 0 else "east") if axis == "z" else ("north" if j == 0 else "south"), "top") if not tilt else PLANK)
    boats = [(sx0 + 4, sz0 + 6, 7, "z", False), (sx0 + 12, sz0 + 9, 8, "z", True), (sx0 + 30, sz0 + 12, 7, "x", False),
             (sx0 + 34, sz0 + 22, 6, "z", True), (sx0 + 7, sz0 + 26, 7, "x", False), (sx0 + 20, sz0 + 28, 6, "z", False)]
    for b in boats:
        boat(*b)
    for x in range(sx0 + 2, sx1, 10):
        lantern_post(pc, x, sz1, post=S("minecraft:spruce_fence"))
    stations(pc)
    space_claim(pc, "basin", "open", cap=fy + 1)
    node_mark(pc)
    leftovers_no_body(pc, reason="the hulls lying on the mud and the tops of the quay walls")
    return pc.finish("basin", shown_faces=["north", "south", "east", "west"])


def lighthouse(node):
    pc = Piece(node)
    r = rng(node)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    fy = pc.dy
    cx, cz = (sx0 + sx1) // 2, (sz0 + sz1) // 2
    WHITE = [(LIME, 4), (S("minecraft:smooth_quartz"), 1), (S("minecraft:polished_diorite"), 1)]
    lamp = M.STATIONS["anchor/lighthouse-lamp"]
    lx, ly, lz = pc.L(*lamp[:3])
    gal_y = ly - 1                   # the gallery's and lamp room's walk plane
    cheb = lambda x, z: max(abs(x - cx), abs(z - cz))
    # the foundation, the tower walls (round: the corners cut), the core
    for x in range(0, pc.X):
        for z in range(0, pc.Z):
            d = cheb(x, z)
            corner = abs(x - cx) + abs(z - cz) > 11
            for y in range(0, fy):
                pc.set(x, y, z, STONE if y < fy - 1 else S("minecraft:polished_andesite"))
            for y in range(fy, gal_y):
                if d == 6 and not corner:
                    pc.set(x, y, z, STONE if y < fy + 2 else mix(r, WHITE))
                elif d <= 4:
                    pc.set(x, y, z, mix(r, [(STONE, 3), (S("minecraft:stone"), 1)]))
            pc.set(x, gal_y - 1, z, S("minecraft:polished_andesite") if d <= 6 else AIR)
    # the stair: round the inside of the wall from the door, 22 treads up to the gallery
    path = []
    x, z = cx, sz0
    dirs = [("east", 1, 0), ("south", 0, 1), ("west", -1, 0), ("north", 0, -1)]
    di = 0
    rise = gal_y - fy
    while len(path) < rise:
        f, dx, dz = dirs[di]
        nx, nz = x + dx, z + dz
        if cheb(nx, nz) != 5:
            di = (di + 1) % 4
            continue
        x, z = nx, nz
        path.append((x, z, f))
    flight = []
    for k, (x, z, f) in enumerate(path):
        ty = fy + k
        pc.set(x, ty, z, stairs("stone_brick", f))
        for yy in range(fy, ty):
            pc.set(x, yy, z, STONE)
        for yy in range(ty + 1, min(ty + 4, gal_y + 3)):
            pc.set(x, yy, z, AIR)
        flight += [(x, yy, z) for yy in range(ty, min(ty + 4, gal_y))]
    # the ring passage the stair does not use is solid; the stair's headroom stays open
    pathset = {(x, z): k for k, (x, z, f) in enumerate(path)}
    for x in range(0, pc.X):
        for z in range(0, pc.Z):
            if cheb(x, z) == 5 and (x, z) not in pathset:
                for y in range(fy, gal_y - 1):
                    pc.set(x, y, z, mix(r, [(STONE, 3), (S("minecraft:stone"), 1)]))
    for k, (x, z, f) in enumerate(path):
        for yy in range(fy + k + 1, min(fy + k + 4, gal_y + 3)):
            pc.set(x, yy, z, AIR)
    # the landing inside the door
    door = [c for c in pc.seam_cells("edge/breakwater-to-lighthouse")]
    for c in door:
        pc.set(*c, AIR)
        pc.set(c[0], c[1] - 1 if c[1] == fy else c[1], c[2], STONE) if c[1] == fy else None
    base = []
    for (dx_, dz_) in ((0, 1), (1, 1), (-1, 1)):
        for c in door:
            if c[1] == fy:
                bx, bz = c[0] + dx_, c[2] + dz_
                if cheb(bx, bz) == 5 and (bx, bz) not in pathset and (bx, fy, bz) not in base:
                    pc.set(bx, fy, bz, AIR)
                    pc.set(bx, fy + 1, bz, AIR)
                    pc.set(bx, fy + 2, bz, AIR)
                    base += [(bx, fy, bz), (bx, fy + 1, bz), (bx, fy + 2, bz)]
    # lights let into the core beside the stair
    for k in range(2, len(path), 5):
        x, z, f = path[k]
        ix, iz = (cx - x), (cz - z)
        ix, iz = (ix // abs(ix) if ix else 0), (iz // abs(iz) if iz else 0)
        pc.set(x + ix, fy + k + 1, z + iz, arch.lantern(False))
    # the gallery and the glazed lamp room under its cap
    for x in range(0, pc.X):
        for z in range(0, pc.Z):
            d = cheb(x, z)
            corner = abs(x - cx) + abs(z - cz) > 11
            if d <= 6 and not corner:
                pc.set(x, gal_y - 1, z, S("minecraft:smooth_stone"))
            if d == 6 and not corner:
                pc.set(x, gal_y, z, S("minecraft:iron_bars"))
            if d == 3:
                for y in range(gal_y, gal_y + 4):
                    pc.set(x, y, z, PANE if (x != cx and z != cz) or y > gal_y + 1 else STONE)
                pc.set(x, gal_y + 4, z, S("minecraft:polished_andesite"))
            if d < 3:
                pc.set(x, gal_y + 4, z, S("minecraft:polished_andesite"))
    # the hole the stair comes up through
    top = path[-4:]
    for (x, z, f) in top:
        pc.set(x, gal_y - 1, z, AIR) if pc.get(x, gal_y - 1, z) != pc.get(x, gal_y - 1, z) else None
    for k, (x, z, f) in enumerate(path):
        if fy + k >= gal_y - 4:
            pc.set(x, gal_y - 1, z, AIR) if fy + k < gal_y - 1 else None
    # the lamp on its pedestal, the lamp room door to the gallery
    pc.set(lx, gal_y, lz, S("minecraft:polished_andesite"))
    lampdoor = [(cx, gal_y, cz - 3), (cx, gal_y + 1, cz - 3)]
    for c in lampdoor:
        pc.set(*c, AIR)
    # the cap
    rr = pc.roof
    for i in range(rr["courses"] + 1):
        y = rr["lid_y"] + i
        rad = 3 - i
        if rad < 0:
            break
        for x in range(cx - rad, cx + rad + 1):
            for z in range(cz - rad, cz + rad + 1):
                pc.set(x, y, z, S("minecraft:dark_prismarine") if rad else S("minecraft:lightning_rod", facing="up", powered=False, waterlogged=False))
    hang(pc, cx + 1, gal_y + 3, cz + 1)
    # the contract
    pc.claim(door, "door-breakwater-to-lighthouse")
    pc.claim(base, "base")
    pc.space_decl("base", "enclosed")
    pc.claim([c for c in flight if c not in base], "spiral")
    gallery, room = [], []
    for x in range(0, pc.X):
        for z in range(0, pc.Z):
            d = cheb(x, z)
            for y in range(gal_y, gal_y + 4):
                if pc.prog.get(x, y, z) in (AIR,) or not is_full(pc.prog.get(x, y, z)):
                    if (x, y, z) in pc.prog.region:
                        continue
                    if d in (4, 5, 6) and pc.owned((x, y, z)):
                        gallery.append((x, y, z))
                    elif d < 3:
                        room.append((x, y, z))
    pc.claim(gallery, "gallery")
    pc.space_decl("gallery", "open")
    pc.claim(lampdoor, "lamp-door")
    pc.claim([c for c in room if c not in lampdoor], "lamp-room")
    pc.space_decl("lamp-room", "enclosed")
    pc.edge(a="base", b="exterior", **{"class": "walk"}, via="door-breakwater-to-lighthouse")
    pc.edge(a="base", b="gallery", **{"class": "stair"}, rise=gal_y - fy, via="spiral")
    pc.edge(a="gallery", b="lamp-room", **{"class": "walk"}, via="lamp-door")
    pc.mark("node-lighthouse", base[0] if base else (cx, fy, sz0 + 1))
    station_mark(pc, "anchor/lighthouse-lamp", clear=True)
    leftovers_no_body(pc, reason="the top of the tower's walls and its cap")
    return pc.finish("base", shown_faces=["north", "south", "east", "west", "up"])


BUILDERS = {
    "node/coach-road": coach_road,
    "node/cliff-steps": cliff_steps,
    "node/harbour-office": harbour_office,
    "node/coyle-house": coyle_house,
    "node/net-lofts": net_lofts,
    "node/fish-market": fish_market,
    "node/seamens-chapel": seamens_chapel,
    "node/chapel-crypt": chapel_crypt,
    "node/customs-house": customs_house,
    "node/whalers-shed": whalers_shed,
    "node/ropewalk": ropewalk,
    "node/harbour-lane": harbour_lane,
    "node/seawall": seawall,
    "node/slipway-stair": slipway_stair,
    "node/pier": pier,
    "node/breakwater": breakwater,
    "node/high-street": high_street,
    "node/boatyard": boatyard,
    "node/lighthouse": lighthouse,
}
