"""The castle's off-road pockets along the whole route, each branching from a
place on or beside the road: the Sally Tower on the valley floor, the Hall of
Arms in the barbican's east tower, the Bastion off the cliff shelf, the
Ossuary under the ward's dry fountain, the Founders' Yard north of the chapel
(and the Ringers' Stair that comes down into it from the bell tower), the
Arbalest Turret off the east rampart, the Gallows Walk under the north
curtain, and the Buttery off the great hall."""
from . import layout as L
from .grid import room, crenels, flight, gable, pyramid, hsh, stairs, slab, block, rail, AIR
from .palette import (WALL, TRIM, TRIM_TUFF, QUOIN, FLAG, FLOOR, PILLAR, PLANKS, DARK_PLANKS,
                      POST, BEAM, BEAM_Z, CHAPEL, KEEP, ROCK, ROCK_MOSS, ROAD, LANTERN,
                      LANTERN_HANG, SOUL_LANTERN, CANDLES, CHAIN, COBWEB, BARS_X, BARS_Z,
                      GATE_WOOD, ROOF, ROOF_MAT, HAY, STRAW)

C, V, W, U = L.CASTLE, L.VALLEY, L.WALK, L.UNDER
SB = "minecraft:stone_brick_stairs"
BONES = block("minecraft:bone_block[axis=y]")
SKULL = block("minecraft:skeleton_skull[powered=false,rotation=8]")


def chest(facing):
    return block(f"minecraft:chest[facing={facing},type=single,waterlogged=false]")


def lectern(facing):
    return block(f"minecraft:lectern[facing={facing},has_book=false,powered=false]")


def sally_tower(g):
    """The south mural tower east of the causeway, on the valley floor: a door
    in its foot, a tall dim room, a chest in plain sight on the flags and a
    timber gallery over it where the lurkers crouch."""
    p = L.P["sally-tower"]
    x0, x1, z0, z1 = p.box                        # 116..120, 167..174
    g.clear(x0, x1, V, V + p.height - 1, z0, z1)
    g.box(x0, x1, V - 1, V - 1, z0, z1, FLOOR)
    # the door in the tower's south face, onto the valley floor
    g.clear(118, 119, V, V + 2, z1 + 1, z1 + 2)
    g.box(118, 119, V - 1, V - 1, z1 + 1, z1 + 2, FLOOR)
    g.box(117, 120, V + 3, V + 3, z1 + 2, z1 + 2, TRIM)
    g.set(117, V, z1 + 3, LANTERN)
    g.set(120, V, z1 + 3, LANTERN)
    # the gallery: planks on beams along the north wall, four over the floor
    gy = V + 4
    g.box(x0, x1, gy - 1, gy - 1, z0, z0 + 2, PLANKS)
    g.box(x0, x1, gy - 2, gy - 2, z0 + 2, z0 + 2, BEAM)
    for x in (x0, x1):
        g.box(x, x, V, gy - 2, z0 + 2, z0 + 2, POST)
    g.set(x0 + 2, gy, z0, block("minecraft:barrel[facing=up,open=false]"))
    g.set(x0 + 1, gy + 3, z0 + 1, LANTERN_HANG)
    # beggars' leavings on the floor, the chest in the middle of it
    g.set(x0, V, z1, HAY)
    g.set(x0, V, z1 - 1, block("minecraft:white_carpet"))
    g.set(x1, V, z1 - 2, CANDLES)
    g.set(118, V, 171, chest("south"))
    g.set(x0, V, 169, lectern("east"))
    g.set(x1, V + p.height - 2, z1, COBWEB)
    g.mark("sally-tower", 118, V, z1, "north")
    g.mark("sally-chest", 118, V, 171, "south", holds=True)
    g.mark("sally-tally", x0, V, 169, "east", holds=True)
    g.mark("sally-lurker-1", x0 + 1, gy, z0 + 1, "south")
    g.mark("sally-lurker-2", 118, gy, z0 + 1, "south")
    g.mark("sally-lurker-3", x1 - 1, gy, z0 + 1, "south")


def hall_of_arms(g):
    """The barbican's east gate tower, hollowed at the gate level as the west
    one is: a long guard room lined with stands of arms, a chest at its end."""
    p = L.P["hall-of-arms"]
    x0, x1, z0, z1 = p.box                        # 94..98, 165..175
    g.clear(x0, x1, C, C + p.height - 1, z0, z1)
    g.box(x0, x1, C - 1, C - 1, z0, z1, FLOOR)
    g.clear(95, 97, C, C + 2, z0 - 1, z0 - 1)          # into the gate hall
    g.box(95, 97, C - 1, C - 1, z0 - 1, z0 - 1, FLOOR)
    # racks between the stands, a lantern at each end
    for z in (166, 170, 174):
        g.set(x0, C + 1, z, block("minecraft:dark_oak_fence_gate[facing=east,in_wall=false,open=false,powered=false]"))
        g.set(x1, C + 1, z, block("minecraft:dark_oak_fence_gate[facing=west,in_wall=false,open=false,powered=false]"))
    g.set(x0, C, z0, LANTERN)
    g.set(x1, C, z1 - 1, LANTERN)
    g.set(96, C, z1, chest("north"))
    g.mark("hall-of-arms", 96, C, z0 + 1, "south")
    g.mark("arms-chest", 96, C, z1, "north", holds=True)
    g.mark("arms-end", 96, C, z1 - 2, "south")
    for k, z in enumerate((167, 169, 171, 173)):
        g.mark(f"arms-stand-w{k + 1}", x0, C, z, "east")
        if z != 171:
            g.mark(f"arms-stand-e{k + 1}", x1, C, z, "west")
    g.mark("gate-sergeant", x1, C, 171, "west")


def bastion(g):
    """A storeroom in the south-west bastion at the shelf's level, its door
    onto the west shelf, arrow slits over the valley."""
    p = L.P["bastion"]
    x0, x1, z0, z1 = p.box                        # 12..16, 166..171
    g.clear(x0, x1, C, C + p.height - 1, z0, z1)
    g.box(x0, x1, C - 1, C - 1, z0, z1, FLOOR)
    g.clear(10, 11, C, C + 1, 168, 169)                # the door off the west shelf
    g.box(10, 11, C - 1, C - 1, 168, 169, FLOOR)
    g.box(10, 10, C + 2, C + 2, 167, 170, TRIM)
    # slits in the south face, looking down the valley
    for x in (13, 15):
        g.clear(x, x, C + 1, C + 2, z1 + 1, z1 + 2)
    g.box(x0, x0 + 1, C, C, z0, z0, BONES)
    g.set(x0, C + 1, z0, SKULL)
    g.set(x1, C, z0, block("minecraft:barrel[facing=up,open=false]"))
    g.set(x1, C, z1, chest("west"))
    g.set(x0, C, z1, LANTERN)
    g.set(x1 - 1, C + p.height - 1, z0, COBWEB)
    g.mark("bastion", 13, C, 169, "east")
    g.mark("bastion-chest", x1, C, z1, "west", holds=True)


def ossuary(g):
    """Under the ward: a winding stair down beside the dry fountain into a vaulted
    gallery lined with the castle's bones, running west to the charnel
    chamber where the bone-wardens keep the Sexton's chest."""
    # the gallery: west from the stair's foot, under the ward
    p = L.P["ossuary"]
    gx0, gx1, gz0, gz1 = 72, 88, 120, 124
    g.box(gx0 - 1, gx1 + 1, U - 1, U + 5, gz0 - 1, gz1 + 2, block("minecraft:deepslate_bricks"))
    g.clear(gx0, gx1, U, U + 4, gz0, gz1)
    g.box(gx0, gx1, U - 1, U - 1, gz0, gz1, FLOOR)
    # the stair: a winding stair round a newel, beside the dry fountain,
    # one turn of twelve steps from the gallery up to the ward's flags
    ring = [(83, 125), (82, 125), (81, 125), (80, 125), (80, 126), (80, 127), (80, 128),
            (81, 128), (82, 128), (83, 128), (83, 127), (83, 126)]
    g.box(79, 84, U - 1, C - 1, 124, 129, block("minecraft:deepslate_bricks"))
    g.clear(80, 83, U, C + 3, 125, 128)
    for k, (sx, sz) in enumerate(ring):
        g.box(sx, sx, U - 1, U + k - 1, sz, sz, block("minecraft:deepslate_bricks"))
    g.box(81, 82, U - 1, C + 1, 126, 127, PILLAR)                 # the newel
    g.set(81, C + 2, 126, LANTERN)
    g.box(83, 83, U + 3, C + 1, 125, 125, PILLAR)                 # over the first step: no drop from the last
    g.clear(80, 83, U, U + 2, 124, 124)                           # the stair's foot opens on the gallery
    edge = rail("minecraft:polished_deepslate_wall")
    for x in range(79, 85):
        g.set(x, C, 124, edge)
        g.set(x, C, 129, edge)
    for z in range(124, 130):
        g.set(79, C, z, edge)
        if z != 126:
            g.set(84, C, z, edge)
    g.box(84, 84, C - 1, C - 1, 126, 126, FLAG)
    # niches of bones along both walls, skulls on the shelves
    for x in range(gx0 + 1, gx1 - 2, 3):
        for z in (gz0 - 1, gz1 + 1):
            if x <= 84 and not (z == gz1 + 1 and 78 <= x <= 84):
                g.box(x, x + 1, U, U + 2, z, z, BONES)
                g.set(x, U + 3, z, block("minecraft:polished_deepslate"))
        g.set(x, U, gz0, SKULL) if hsh(x, 1, 301) < .5 else None
    for x in range(gx0 + 2, gx1, 5):
        g.set(x, U + 4, (gz0 + gz1) // 2, block("minecraft:soul_lantern[hanging=true,waterlogged=false]"))
    # the charnel chamber at the gallery's west end
    x0, x1, z0, z1 = p.box                        # 58..70, 115..129
    g.box(x0 - 1, x1 + 1, U - 1, U + p.height, z0 - 1, z1 + 1, block("minecraft:deepslate_bricks"))
    g.clear(x0, x1, U, U + p.height - 1, z0, z1)
    g.box(x0, x1, U - 1, U - 1, z0, z1, FLOOR)
    g.clear(x1 + 1, gx0 - 1, U, U + 3, 121, 123)
    g.box(x1 + 1, gx0 - 1, U - 1, U - 1, 121, 123, FLOOR)
    for (px, pz) in ((x0 + 3, z0 + 3), (x1 - 3, z0 + 3), (x0 + 3, z1 - 3), (x1 - 3, z1 - 3)):
        g.box(px, px, U, U + p.height - 1, pz, pz, PILLAR)
    for z in range(z0, z1 + 1, 2):
        g.box(x0, x0, U, U + 2, z, z, BONES)
        g.set(x0, U + 3, z, SKULL)
    g.box(x0 + 1, x0 + 2, U, U, 121, 123, block("minecraft:polished_deepslate"))
    g.set(x0 + 1, U, 122, chest("east"))
    g.set(x0 + 2, U + 1, 121, CANDLES)
    g.set(x0 + 2, U + 1, 123, CANDLES)
    for (lx, lz) in ((x1, z0), (x1, z1), (x0 + 6, z0), (x0 + 6, z1)):
        g.set(lx, U, lz, SOUL_LANTERN)
    g.mark("ossuary-stair", 82, U, 123, "south")
    g.mark("ossuary", 80, U, 122, "west")
    g.mark("bone-wardens", 64, U, 122, "east")
    g.mark("sexton-chest", x0 + 1, U, 122, "east", holds=True)
    g.mark("ossuary-stairhead", 84, C, 126, "west")


def ringers_stair(g):
    """The ringers' own stair down the bell tower's foot: from the stair hall
    through the floor, two flights inside the masonry, and a door in the
    tower's east face into the Founders' Yard — barred on the tower side."""
    # the landing inside the door
    g.clear(30, 31, C, C + 4, 20, 23)
    g.box(30, 31, C - 1, C - 1, 20, 23, FLOOR)
    # the first flight climbs west, the second north, up through the hall floor
    flight(g, "x", 21, 23, 29, -1, C, 6, SB, CHAPEL)          # 24 -> 30, x29..24
    g.clear(21, 23, C + 6, C + 9, 20, 23)                     # the turn
    g.box(21, 23, C + 5, C + 5, 20, 23, FLOOR)
    flight(g, "z", 21, 23, 20, -1, C + 6, 6, SB, CHAPEL)      # 30 -> 36, z20..15
    g.box(20, 20, W, W, 16, 19, rail("minecraft:polished_deepslate_wall"))   # a rail on the open side
    g.box(24, 24, W, W, 16, 19, rail("minecraft:polished_deepslate_wall"))
    g.box(21, 23, W, W, 20, 20, rail("minecraft:polished_deepslate_wall"))
    g.set(30, C + 3, 23, LANTERN_HANG)
    g.set(22, C + 9, 21, LANTERN_HANG)
    # the door east into the yard: sealed, a shortcut opened from within
    g.clear(32, 33, C, C + 1, 21, 22)
    g.box(32, 32, C - 1, C - 1, 21, 22, FLOOR)
    g.gate("ringers-stair", 33, 33, C, C + 1, 21, 22, "minecraft:dark_oak_planks", GATE_WOOD)
    g.box(33, 33, C + 2, C + 2, 20, 23, TRIM_TUFF)
    g.mark("unlock-ringers-stair", 31, C, 22, "east")


def founders_yard(g):
    """North of the chapel, under the buttress walk: the yard where the Vesper
    was cast — the casting pit with the broken mould of a second bell, the
    furnace against the bell tower, the founders' anvil and their ledger."""
    p = L.P["founders-yard"]
    x0, x1, z0, z1 = p.box                        # 34..52, 18..30
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            g.set(x, C - 1, z, ROAD if hsh(x, z, 311) < .5 else FLAG)
    # the casting pit: four deep, lined with brick, a stair up its east side
    px0, px1, pz0, pz1 = 42, 48, 20, 25
    brick = block("minecraft:bricks")
    mud = block("minecraft:packed_mud")
    g.box(px0 - 1, px1 + 1, C - 6, C - 1, pz0 - 1, pz1 + 1, brick)
    g.clear(px0, px1, C - 4, C + 1, pz0, pz1)
    g.box(px0, px1, C - 5, C - 5, pz0, pz1, mud)
    for k in range(4):                          # treads climbing east, pit floor to rim
        x = px1 - 3 + k
        g.box(x, x, C - 5, C - 5 + k, 21, 23, brick)
        g.box(x, x, C - 4 + k, C - 4 + k, 21, 23, stairs("minecraft:brick_stairs", "east"))
        g.clear(x, x, C - 3 + k, C + 1, 21, 23)
    # a rail round the rim where there is no stair
    rim = rail("minecraft:brick_wall")
    for x in range(px0 - 1, px1 + 2):
        for z in (pz0 - 1, pz1 + 1):
            g.set(x, C, z, rim)
    for z in range(pz0 - 1, pz1 + 2):
        g.set(px0 - 1, C, z, rim)
        if not 21 <= z <= 23:
            g.set(px1 + 1, C, z, rim)
    # the mould of the second bell, cracked open on the pit floor; the bell
    # that came out of it lies beside it, never hung
    for (mx, mz, h) in ((42, 21, 3), (43, 21, 3), (44, 21, 2), (42, 22, 2), (42, 23, 1)):
        g.box(mx, mx, C - 4, C - 5 + h, mz, mz, mud)
    g.set(42, C - 4, 25, block("minecraft:bell[attachment=floor,facing=east,powered=false]"))
    g.set(px1, C - 4, pz0, LANTERN)
    g.set(px0, C - 4, pz1 - 1, LANTERN)
    # the furnace against the tower: furnaces under a brick chimney
    g.box(34, 36, C, C + 2, 25, 28, brick)
    g.set(37, C, 26, block("minecraft:furnace[facing=east,lit=false]"))
    g.set(37, C, 27, block("minecraft:furnace[facing=east,lit=false]"))
    g.box(34, 36, C + 3, C + 12, 26, 28, brick)
    # the founders' anvil and their ledger on the yard's east side
    g.set(51, C, 19, block("minecraft:anvil[facing=north]"))
    g.set(52, C, 19, block("minecraft:barrel[facing=up,open=false]"))
    g.set(51, C, 26, lectern("west"))
    for (lx, lz) in ((39, 19), (39, 27), (51, 27)):
        g.box(lx, lx, C, C + 1, lz, lz, POST)
        g.set(lx, C + 2, lz, LANTERN)
    g.mark("founders-yard", 38, C, 22, "east")
    g.mark("bellfounder", 43, C - 4, 23, "east")
    g.mark("casting-pit", 47, C - 1, 22, "west")
    g.mark("casting-ledger", 51, C, 26, "west", holds=True)


def arbalest_turret(g):
    """The mural tower on the east curtain opposite the volley's battery,
    hollowed at the walk's level: its door through the rampart's outer wall."""
    p = L.P["arbalest-turret"]
    x0, x1, z0, z1 = p.box                        # 163..169, 97..103
    g.clear(x0, x1, W, W + p.height - 1, z0, z1)
    g.box(x0, x1, W - 1, W - 1, z0, z1, FLOOR)
    g.clear(160, 162, W, W + 1, 99, 101)
    g.box(160, 162, W - 1, W - 1, 99, 101, FLOOR)
    g.box(160, 160, W + 2, W + 2, 98, 102, TRIM)
    # a spare engine: a windlass and racks of bolts, loops over the valley
    g.box(x1, x1, W, W + 1, z0 + 1, z0 + 1, POST)
    g.box(x1, x1, W, W + 1, z1 - 1, z1 - 1, POST)
    g.box(x1, x1, W + 1, W + 1, z0 + 2, z1 - 2, BEAM_Z)
    g.clear(x1 + 1, x1 + 2, W + 1, W + 2, 100, 100)
    for z in (z0, z1):
        g.set(x0 + 2, W, z, block("minecraft:barrel[facing=up,open=false]"))
    g.set(x0 + 4, W, z1, chest("north"))
    g.set(x0, W, z0, LANTERN)
    g.mark("arbalest-turret", x0 + 1, W, 100, "east")
    g.mark("arbalest-chest", x0 + 4, W, z1, "north", holds=True)


def gallows_walk(g):
    """The ground under the north curtain, behind the keep: the castle's
    gallows, the posts still standing, the hanged men not all still."""
    x0, x1, z0, z1 = 84, 108, 5, 9
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if hsh(x, z, 321) < .4:
                g.set(x, C - 1, z, ROAD)
    # three gallows: two posts and a beam, a chain from the beam
    for gx in (88, 96, 104):
        g.box(gx, gx, C, C + 4, 6, 6, POST)
        g.box(gx + 2, gx + 2, C, C + 4, 6, 6, POST)
        g.box(gx, gx + 2, C + 5, C + 5, 6, 6, BEAM)
        g.box(gx + 1, gx + 1, C + 3, C + 4, 6, 6, CHAIN)
    g.box(92, 93, C, C, 8, 8, DARK_PLANKS)                     # the cart they came in
    g.set(100, C, 5, chest("south"))
    g.box(99, 99, C, C + 1, 5, 5, POST)
    g.set(99, C + 2, 5, LANTERN)
    g.set(108, C, 9, LANTERN)
    g.mark("gallows-walk", 96, C, 8, "west")
    g.mark("hanged-men", 101, C, 8, "west")
    g.mark("gallows-chest", 100, C, 5, "south", holds=True)


def buttery(g):
    """Off the great hall's east wall: the buttery and the king's cellar door,
    reached from the hall alone."""
    p = L.P["buttery"]
    x0, x1, z0, z1 = p.box                        # 112..120, 72..81
    room(g, x0, x1, z0, z1, C, p.height, KEEP, FLOOR, ceiling=KEEP)
    gable(g, x0 - 1, x1 + 1, z0 - 1, z1 + 1, C + p.height + 1, ROOF_MAT, ROOF, along="x")
    g.clear(108, x0 - 1, C, C + 2, 76, 77)                    # the door through the hall's east wall
    g.box(108, x0 - 1, C - 1, C - 1, 76, 77, FLOOR)
    g.box(108, 111, C + 3, C + 3, 76, 77, KEEP)
    g.box(110, 111, C, C + 2, 75, 75, KEEP)
    g.box(110, 111, C, C + 2, 78, 78, KEEP)
    g.box(110, 111, C + 3, C + 3, 75, 78, KEEP)
    # casks along the walls, the steward's table, the king's cup
    for z in range(z0, z1 + 1, 2):
        g.set(x1, C, z, block("minecraft:barrel[facing=west,open=false]"))
        g.set(x1, C + 1, z, block("minecraft:barrel[facing=west,open=false]")) if z % 4 == 0 else None
    g.box(x0 + 2, x0 + 4, C, C, 79, 79, DARK_PLANKS)
    g.set(x0 + 3, C + 1, 79, CANDLES)
    g.set(x0 + 1, C, z0, chest("south"))
    g.set(x0, C, z1, LANTERN)
    g.set(x1 - 1, C, z0, LANTERN)
    g.mark("buttery", x0 + 2, C, 76, "east")
    g.mark("buttery-chest", x0 + 1, C, z0, "south", holds=True)


def build(g):
    sally_tower(g)
    hall_of_arms(g)
    bastion(g)
    ossuary(g)
    ringers_stair(g)
    founders_yard(g)
    arbalest_turret(g)
    gallows_walk(g)
    buttery(g)
