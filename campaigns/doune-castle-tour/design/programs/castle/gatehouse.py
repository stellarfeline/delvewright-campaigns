"""The gatehouse: the gate passage, the guardroom and prison, the lord's and duchess's halls, the chambers and the parapet."""

from .common import *  # noqa: F401,F403

PALETTE = {
    # dressed masonry, the stone the gatehouse furnishes itself with
    "gate/dressed": "minecraft:polished_andesite",
    "gate/carved": "minecraft:chiseled_stone_bricks",
    "gate/lintel": "minecraft:smooth_stone",
    "gate/sooty": "minecraft:deepslate_bricks",
    "gate/rail_x": "minecraft:dark_oak_fence[east=true,north=false,south=false,waterlogged=false,west=true]",
    "gate/kerb": "minecraft:cobblestone",
    "gate/fire": "minecraft:campfire[facing=north,lit=true,signal_fire=false,waterlogged=false]",
    "gate/seat": "minecraft:smooth_stone_slab[type=bottom,waterlogged=false]",
    "gate/shelf": "minecraft:smooth_stone_slab[type=top,waterlogged=false]",
    "gate/altar": "minecraft:smooth_quartz",
    "gate/basin": "minecraft:cauldron",
    "gate/privy": "minecraft:stone_brick_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]",
    # iron
    "gate/portcullis": "minecraft:iron_bars[east=true,north=false,south=false,waterlogged=false,west=true]",
    "gate/yett": "minecraft:iron_bars[east=false,north=true,south=true,waterlogged=false,west=false]",
    "gate/grate": "minecraft:iron_bars[east=true,north=true,south=true,waterlogged=false,west=true]",
    "gate/spear": "minecraft:iron_bars[east=false,north=false,south=false,waterlogged=false,west=false]",
    "gate/chain": "minecraft:iron_chain[axis=y,waterlogged=false]",
    # timber
    "gate/table_leg": "minecraft:oak_fence[east=false,north=false,south=false,waterlogged=false,west=false]",
    "gate/table_top": "minecraft:oak_slab[type=bottom,waterlogged=false]",
    "gate/round_leg": "minecraft:dark_oak_fence[east=false,north=false,south=false,waterlogged=false,west=false]",
    "gate/round_top": "minecraft:dark_oak_slab[type=bottom,waterlogged=false]",
    "gate/bench": "minecraft:spruce_slab[type=bottom,waterlogged=false]",
    "gate/stool": "minecraft:spruce_slab[type=bottom,waterlogged=false]",
    "gate/chair": "minecraft:dark_oak_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]",
    "gate/chair_back": "minecraft:dark_oak_planks",
    "gate/screen": "minecraft:dark_oak_planks",
    "gate/gallery": "minecraft:dark_oak_planks",
    "gate/beam": "minecraft:dark_oak_log[axis=x]",
    "gate/rail": "minecraft:dark_oak_fence[east=false,north=true,south=true,waterlogged=false,west=false]",
    "gate/cupboard": "minecraft:bookshelf",
    "gate/vessel": "minecraft:flower_pot",
    "gate/coffer": "minecraft:dark_oak_planks",
    "gate/cask": "minecraft:spruce_log[axis=z]",
    "gate/sack": "minecraft:hay_block[axis=y]",
    "gate/matting": "minecraft:brown_carpet",
    # cloth
    "gate/curtain": "minecraft:red_wool",
    "gate/bed_head": "minecraft:red_bed[facing=north,occupied=false,part=head]",
    "gate/bed_foot": "minecraft:red_bed[facing=north,occupied=false,part=foot]",
    "gate/banner_red_s": "minecraft:red_wall_banner[facing=south]",
    "gate/banner_blue_s": "minecraft:blue_wall_banner[facing=south]",
    "gate/banner_yellow_s": "minecraft:yellow_wall_banner[facing=south]",
    "gate/banner_red_e": "minecraft:red_wall_banner[facing=east]",
    "gate/banner_blue_e": "minecraft:blue_wall_banner[facing=east]",
    "gate/banner_yellow_e": "minecraft:yellow_wall_banner[facing=east]",
    "gate/banner_red_w": "minecraft:red_wall_banner[facing=west]",
    "gate/banner_blue_w": "minecraft:blue_wall_banner[facing=west]",
    # light — a wall torch always points away from the wall it hangs on
    "gate/torch_n": "minecraft:wall_torch[facing=south]",
    "gate/torch_s": "minecraft:wall_torch[facing=north]",
    "gate/torch_w": "minecraft:wall_torch[facing=east]",
    "gate/torch_e": "minecraft:wall_torch[facing=west]",
    "gate/lantern": "minecraft:lantern[hanging=false,waterlogged=false]",
    "gate/lantern_hung": "minecraft:lantern[hanging=true,waterlogged=false]",
    "gate/bracket_w": "minecraft:oak_fence[east=false,north=false,south=false,waterlogged=false,west=true]",
    "gate/bracket_e": "minecraft:oak_fence[east=true,north=false,south=false,waterlogged=false,west=false]",
    "gate/candle2": "minecraft:candle[candles=2,lit=true,waterlogged=false]",
    "gate/candle3": "minecraft:candle[candles=3,lit=true,waterlogged=false]",
}
ANCHORS = {
    (77, WALK, 40): ("stop-gate", None),
    (70, WALK, 40): ("guardroom", None),
    (85, WALK, 40): ("pit-prison", None),
    (72, GH_L1[0], 40): ("stop-lords-hall", None),
    (72, GH_L2[0], 40): ("stop-duchess-hall", None),
    (72, GH_L2[0], 46): ("oratory", None),
    (84, GH_L2[0], 34): ("bedchamber", None),
}

MATTING = True          # rush matting over the lord's hall flags


def window(c, sill, height, top, role="wall"):
    """A wall column carrying an opening: masonry, void, masonry."""
    c.upto(role, sill - 1)
    c.add(None, height)
    c.upto(role, top)


def lay(c, cells, top):
    """Lay one column's furniture from where the column stands up to `top`.

    `cells` maps a y course to the role standing in it; a course it does not
    name is air. Equal neighbours merge into one span.
    """
    y = c.y
    while y <= top:
        role = cells.get(y)
        n = 1
        while y + n <= top and cells.get(y + n) == role:
            n += 1
        c.add(role, n)
        y += n

def gatehouse(c, x, z):
    x0, x1, z0, z1 = GH
    ix0, ix1, iz0, iz1 = GH_IN
    px0, px1 = PASSAGE
    in_passage = px0 <= x <= px1

    # --- the gate passage runs through both walls at ground level
    if in_passage and CZ0 <= z <= RANGE_Z1:
        c.add("floor_stone", 1)
        arch = 13 if x in (px0, px1) else 14      # a stepped arch head
        lay(c, passage_cells(x, z, arch), arch)
        if murder_hole(x, z):
            c.upto("wall", F1 - 1)
            c.add("gate/grate", 1)                # a murder hole, barred over
        else:
            c.upto("wall", F1)
        if z <= z0 + 1 or z >= z1 - 1:
            return gate_front(c, x)               # the front carries on over the arch
        return gatehouse_upper(c, x, z, from_y=F1 + 1)

    if wall_face(x, z, GH):
        c.add("plinth", 1)
        north = z <= z0 + 1
        south = z >= z1 - 1
        run = x if (north or south) else z
        # arrow loops at ground level, windows on the two hall floors
        door_courtyard = south and 67 <= x <= 70
        hall_door = x <= x0 + 1 and 38 <= z <= 40
        if door_courtyard or hall_door:
            c.upto("wall", F1)
            c.add(None, 3)
            c.upto("wall", GH_WALL_TOP)
        else:
            c.upto("wall", WALK + 3)
            if (north or south) and run % 6 == 2:
                c.add(None, 2)                      # an arrow loop
                c.upto("wall", F1)
            else:
                c.upto("wall", F1)
            c.upto("wall", GH_L1[0] + 2)
            if run % 5 == 1:
                c.add(None, 3)                      # a hall window
                c.upto("wall", GH_L2[0] + 2)
            else:
                c.upto("wall", GH_L2[0] + 2)
            if run % 5 == 1:
                c.add(None, 3)
                c.upto("wall", GH_L3[0] + 2)
            else:
                c.upto("wall", GH_L3[0] + 2)
            c.upto("wall", GH_PARAPET - 1)
            c.upto("wall", GH_WALL_TOP if crenel(run) else GH_PARAPET)
        c.air_to_top()
        return c

    # --- the interior, floor by floor
    c.add("floor_stone", 1)
    # ground floor: guardroom west of the passage, the prison pit east of it
    if x == px0 - 1 or x == px1 + 1:
        if 36 <= z <= 38:                           # the two room doors
            c.add(None, 3)
            c.upto("wall", F1)
        elif z in (34, 43):                         # arrow loops onto the passage
            c.upto("wall", WALK + 2)
            c.add(None, 1)
            c.upto("wall", F1)
        else:
            c.upto("wall", F1)
    else:
        if pit(x, z):
            sink_pit(c)                             # the prison pit, cut below the floor
        lay(c, ground_cells(x, z), CELLAR[1])
        c.add("floor_stone", 1)
    return gatehouse_upper(c, x, z, from_y=F1 + 1)


def gate_front(c, x):
    """Over the gate arch the front is blank wall, then the parapet's own teeth."""
    c.upto("wall", GH_PARAPET - 1)
    c.upto("wall", GH_WALL_TOP if crenel(x) else GH_PARAPET)
    c.air_to_top()
    return c


def sink_pit(c):
    """Cut the ground under a pit column away and bar the floor course over it."""
    c.spans.pop()                                   # the floor course just laid
    c.y -= 1
    rock_role, rock_n = c.spans.pop()
    c.y -= rock_n
    c.add(rock_role, rock_n - 1)                    # one dark course under the bars
    c.add(None, 1)
    c.add("gate/grate", 1)

def gatehouse_upper(c, x, z, from_y):
    """The lord's hall, the duchess's hall, the chambers, the parapet.

    Three flights, doglegged: each turns onto its own strip so one flight's
    landing is never the next flight's masonry.
    """
    east_strip = 86 <= x <= 88          # flights 1 and 3 climb north here
    mid_strip = 82 <= x <= 84           # flight 2 climbs south here
    # level 1: the lord's hall, and the first flight up to the duchess's
    if east_strip and 33 <= z <= 44:
        c.upto("step", F1 + (44 - z))
        c.add(None, max(0, GH_F2 - c.y))
    else:
        lay(c, lords_hall_cells(x, z), GH_L1[1])
        c.add("floor_upper", 1)
    # level 2: the duchess's hall, and the flight up to the chambers
    if mid_strip and 33 <= z <= 43:
        c.upto("step", GH_F2 + (z - 33))
        c.add(None, max(0, GH_F3 - c.y))
    else:
        lay(c, duchess_hall_cells(x, z), GH_L2[1])
        c.add("floor_upper", 1)
    # level 3: the chambers, and the flight out onto the parapet
    if east_strip and 33 <= z <= 40:
        c.upto("step", GH_F3 + (40 - z))
        c.add(None, max(0, GH_PARAPET - c.y))
    else:
        lay(c, chamber_cells(x, z), GH_L3[1])
        c.add("floor_stone", 1)
    # the garret stands inside the parapet walk, which runs all round it
    gx0, gx1, gz0, gz1 = 71, 83, 35, 44
    if gx0 <= x <= gx1 and gz0 <= z <= gz1:
        dist = min(z - gz0, gz1 - z)
        top = GH_PARAPET + 1 + dist
        c.upto(None, top - 2)
        c.upto("roof", top)
    elif (x, z) in WALK_LANTERNS and c.y == GH_PARAPET + 1:
        c.add("gate/lantern", 1)
    c.air_to_top()
    return c


# ---------------------------------------------------------------- the gate passage
PORTCULLIS_Z = 33               # the slot the raised grid hangs in
YETT_Z = (42, 45)               # the iron gate, folded back against the west wall
MURDER_Z = (35, 40, 45)         # holes in the vault, barred over from the hall above
BRACKET_Z = (36, 41, 46)        # lantern brackets down both passage walls


def murder_hole(x, z):
    return x == 77 and z in MURDER_Z


def passage_cells(x, z, arch):
    """{y: role} in the gate passage. Feet stand at y8, the vault head at `arch`."""
    px0, px1 = PASSAGE
    f = {}
    folded = x == px0 and YETT_Z[0] <= z <= YETT_Z[1]
    if z == PORTCULLIS_Z:                           # raised, and clear overhead
        for y in range(13, arch + 1):
            f[y] = "gate/portcullis"
    if folded:                                      # the yett, back against the wall
        for y in range(WALK, WALK + 5):
            f[y] = "gate/yett"
    if z in BRACKET_Z and x in (px0, px1) and not folded:
        f[11] = "gate/lantern_hung"
        f[12] = "gate/bracket_w" if x == px0 else "gate/bracket_e"
    return f


# ---------------------------------------------------------- the guardroom and the pit
PIT = (84, 86, 36, 38)          # the prison pit, under its barred hatch
PIT_LAMP = (85, 37)             # a lamp on a chain, hung over the shaft
BRAZIER_FIRE = (71, 36)         # the guardroom brazier, in a kerb of full blocks


def pit(x, z):
    return PIT[0] <= x <= PIT[1] and PIT[2] <= z <= PIT[3]


def brazier(x, z, fire):
    """A fire in a kerb of full blocks: the four sides, so nothing walks in."""
    if (x, z) == fire:
        return "gate/fire"
    if abs(x - fire[0]) + abs(z - fire[1]) == 1:
        return "gate/carved"
    return None


def ground_cells(x, z):
    """{y: role} on the ground floor: the guardroom west, the prison east."""
    f = {}
    if pit(x, z):
        if (x, z) == PIT_LAMP:                      # a lamp on a chain over the shaft
            f[WALK + 3] = "gate/lantern_hung"
            for y in range(WALK + 4, CELLAR[1] + 1):
                f[y] = "gate/chain"
        return f                                    # the hatch is the floor course
    # --- the guardroom, west of the passage
    if x <= 73:
        surround = brazier(x, z, BRAZIER_FIRE)
        if surround:
            f[WALK] = surround
            return f
        if x == 67 and (33 <= z <= 38 or 41 <= z <= 46):
            f[WALK] = "gate/bench"                  # benches down the wall
        if 69 <= x <= 71 and z == 32:
            for y in range(WALK, CELLAR[1] + 1):
                f[y] = "gate/screen"                # the weapon rack, panelled to the vault
        if 69 <= x <= 71 and z == 33:
            f[WALK] = "gate/spear"                  # arms stacked against the panel
            f[WALK + 1] = "gate/rail_x"             # the rack's own rail
        if 72 <= x <= 73 and 43 <= z <= 46:
            f[WALK] = "gate/cask"
        if x == 67 and z in (35, 40, 45):
            f[WALK + 3] = "gate/torch_w"
        if x == 73 and z in (34, 39, 44):
            f[WALK + 3] = "gate/torch_e"
        return f
    # --- the pit prison and its store, east of the passage
    if x in (87, 88) and (33 <= z <= 34 or 44 <= z <= 46):
        f[WALK] = "gate/sack" if x == 87 else "gate/cask"
    if x in (83, 87) and z == 40:                   # chains, hung from the vault
        for y in range(WALK + 4, CELLAR[1] + 1):
            f[y] = "gate/chain"
    if x == 81 and z in (34, 39, 44):
        f[WALK + 3] = "gate/torch_w"
    if x == 89 and z in (35, 40, 45):
        f[WALK + 3] = "gate/torch_e"
    if x == 82 and z in (33, 46):
        f[WALK] = "gate/lantern"
    return f


# ------------------------------------------------------------------ the lord's hall
L1 = GH_L1[0]                   # y16, the course a body stands in
BREAST_X = (72, 78)             # the great double fireplace, on the north wall
FIRE_X = (73, 77)
MOUTH_X = (73, 74, 76, 77)      # the two hearth mouths, between three piers
TABLE_X = 76                    # off the door's sight line, so the fire is seen
TABLE_Z = (36, 45)
BREAST_Z = (32, 33)             # the sooted chamber, then the projecting hood
SCREEN_X = 80                   # the carved screen, and the gallery over it
SCREEN_OPEN = (38, 40)
GALLERY_X = (81, 85)
GALLERY_Z = (32, 47)
GALLERY_Y = 22
GALLERY_EDGE_Z = (32, 45, 46, 47)   # where the gallery looks down into the hall


def breast_cells(x, z):
    """One column of the great double fireplace.

    The two hearths sit at z32 in a sooted chamber; z33 carries the hood that
    projects into the hall, with the lintel and the carved overmantel over it.
    Each fire is boxed at its own course by full blocks on all four sides.
    """
    f = {}
    mouth = x in MOUTH_X
    for y in range(L1, GH_L1[1] + 1):
        f[y] = "gate/dressed"
    if z == BREAST_Z[1]:
        if mouth:
            f[L1] = "gate/kerb"                      # the raised hearthstone
            f[L1 + 1] = None
            f[L1 + 2] = None
        f[L1 + 3] = "gate/lintel"
        if 74 <= x <= 76:
            f[L1 + 4] = "gate/carved"
            f[L1 + 5] = "gate/carved"
        return f
    if x in FIRE_X:
        f[L1] = "gate/fire"
    elif mouth:
        f[L1] = "gate/sooty"                         # the jambs, boxing each fire
    if mouth:
        f[L1 + 1] = None
        f[L1 + 2] = None
    return f


def lords_hall_cells(x, z):
    """{y: role} in the lord's hall: floor course y15, room y16..25."""
    f = {}
    # --- the great double fireplace and its carved overmantel
    if BREAST_X[0] <= x <= BREAST_X[1] and BREAST_Z[0] <= z <= BREAST_Z[1]:
        return breast_cells(x, z)
    # --- the carved screen across the east end, and the gallery over it
    if x == SCREEN_X and GALLERY_Z[0] <= z <= GALLERY_Z[1]:
        start = L1 + 3 if SCREEN_OPEN[0] <= z <= SCREEN_OPEN[1] else L1
        for y in range(start, GALLERY_Y + 1):
            f[y] = "gate/screen"
        f[GALLERY_Y + 1] = "gate/rail"
        f[GALLERY_Y + 2] = "gate/rail"
        if z in (34, 44):
            f[L1 + 5] = "gate/lantern_hung"
        return f
    if GALLERY_X[0] <= x <= GALLERY_X[1] and GALLERY_Z[0] <= z <= GALLERY_Z[1]:
        f[GALLERY_Y] = "gate/gallery"                # the gallery floor
        if x == GALLERY_X[1] and z in GALLERY_EDGE_Z:
            f[GALLERY_Y + 1] = "gate/rail"
            f[GALLERY_Y + 2] = "gate/rail"
        if x == 83 and z in (35, 41, 46):
            f[GALLERY_Y + 1] = "gate/lantern"
        if x == 82 and z in (34, 45):
            f[L1] = "gate/cask"
        return f
    # --- the lord's table, his great chair, and the benches down both sides
    if x == TABLE_X:
        if z == 34:
            for y in range(L1, L1 + 2):
                f[y] = "gate/chair_back"             # the great chair's high back
            return f
        if z == 35:
            f[L1] = "gate/chair"
            return f
        if TABLE_Z[0] <= z <= TABLE_Z[1]:
            f[L1] = "gate/table_leg"
            f[L1 + 1] = "gate/table_top"
            if z in (41, 44):
                f[L1 + 2] = "gate/lantern"
            return f
    if x in (TABLE_X - 1, TABLE_X + 1) and TABLE_Z[0] <= z <= TABLE_Z[1]:
        f[L1] = "gate/bench"
        return f
    # --- the sideboard, with its plate and its candles
    if 68 <= x <= 70 and z == 33:
        f[L1] = "gate/cupboard"
        f[L1 + 1] = "gate/candle3" if x == 69 else "gate/vessel"
        return f
    # --- window seats in the deep embrasures of both side walls
    if x in (67, 89) and z in (35, 36, 37, 40, 41, 42, 45, 46, 47):
        f[L1] = "gate/seat"
    # --- banners, and the wall lights between them
    if x == 67 and z in (34, 43):
        f[L1 + 4] = "gate/banner_red_e" if z == 34 else "gate/banner_blue_e"
    if x == 89 and z in (34, 43):
        f[L1 + 4] = "gate/banner_blue_w" if z == 34 else "gate/banner_red_w"
    if z == 32 and x in (68, 70):
        f[L1 + 4] = "gate/banner_blue_s" if x == 68 else "gate/banner_red_s"
    if x == 67 and z in (39, 44):
        f[L1 + 3] = "gate/torch_w"
    if x == 89 and z in (39, 44):
        f[L1 + 3] = "gate/torch_e"
    if z == 47 and x in (69, 74, 78):
        f[L1 + 3] = "gate/torch_s"
    if z == 32 and x in (69, 71):
        f[L1 + 3] = "gate/torch_n"
    # --- rush matting over the stone flags, where the hall is walked
    if (MATTING and 68 <= x <= 79 and 34 <= z <= 46 and L1 not in f
            and not murder_hole(x, z) and (x, z) != (72, 40)):
        f[L1] = "gate/matting"
    return f


# --------------------------------------------------------------- the duchess's hall
L2 = GH_L2[0]                   # y27
D_BREAST_X = (72, 75)
D_FIRE_X = 73
ROUND_X = (75, 77)              # the round table and its cushioned stools
ROUND_Z = (34, 36)
ORATORY_X = (70, 74)            # the oratory alcove, in the south wall
BEAM_Z = (34, 38, 42, 46)


def duchess_hall_cells(x, z):
    """{y: role} in the duchess's hall: floor course y26, room y27..35."""
    f = _duchess(x, z)
    if z in BEAM_Z and 67 <= x <= 89 and GH_L2[1] not in f:
        f[GH_L2[1]] = "gate/beam"                   # the timber ceiling, on its beams
    return f


def _duchess(x, z):
    f = {}
    # --- the fireplace, its mantel, and the tapered hood over it
    if z == 32 and D_BREAST_X[0] <= x <= D_BREAST_X[1]:
        for y in range(L2, GH_L2[1] + 1):
            f[y] = "gate/dressed"
        if x == D_FIRE_X:
            f[L2] = "gate/fire"
        if D_FIRE_X - 1 <= x <= D_FIRE_X + 1:
            f[L2 + 1] = None
            f[L2 + 2] = None
        f[L2 + 3] = "gate/lintel"
        if x in (73, 74):
            f[L2 + 4] = "gate/carved"
        return f
    if z == 33 and D_BREAST_X[0] <= x <= D_BREAST_X[1]:
        f[L2] = "gate/kerb"
        return f
    # --- the oratory: an arched alcove, an altar, a piscina, a credence niche
    if ORATORY_X[0] <= x <= ORATORY_X[1] and z in (46, 47):
        for y in range(L2 + 5, GH_L2[1] + 1):
            f[y] = "gate/dressed"                   # the alcove's own low vault
        if z == 46:
            if x in ORATORY_X:
                for y in range(L2, L2 + 5):
                    f[y] = "gate/carved"            # the arch's two piers
            else:
                f[L2 + 4] = "gate/lintel"           # the arch itself
                if x == 72:
                    f[L2 + 3] = "gate/lantern_hung"  # the lamp in the arch
            return f
        if x == 71:
            f[L2] = "gate/dressed"
            f[L2 + 1] = "gate/shelf"                # the credence niche, hooded
            f[L2 + 2] = "gate/vessel"
            for y in range(L2 + 3, GH_L2[1] + 1):
                f[y] = "gate/dressed"
        elif x == 72:
            f[L2] = "gate/altar"
            f[L2 + 1] = "gate/candle2"
        elif x == 73:
            f[L2] = "gate/dressed"
            f[L2 + 1] = "gate/basin"                # the piscina, in its own recess
            for y in range(L2 + 3, GH_L2[1] + 1):
                f[y] = "gate/dressed"
        else:
            f[L2] = "gate/lantern"
        return f
    # --- the round table and its stools
    if ROUND_X[0] <= x <= ROUND_X[1] and ROUND_Z[0] <= z <= ROUND_Z[1]:
        if x in ROUND_X and z in ROUND_Z:
            f[L2] = "gate/round_leg"
        f[L2 + 1] = "gate/round_top"
        if (x, z) == (76, 35):
            f[L2 + 2] = "gate/candle3"
        return f
    if (x, z) in ((74, 35), (78, 35), (76, 33), (76, 37)):
        f[L2] = "gate/stool"
        return f
    # --- the bedchamber, in the corner under the round tower
    bed = bedchamber_cells(x, z)
    if bed is not None:
        return bed
    # --- window seats, woven hangings, and the wall lights
    if x == 67 and z in (35, 36, 37, 40, 41, 42, 45, 46, 47):
        f[L2] = "gate/seat"
    if x == 89 and z in (40, 41, 42, 45, 46, 47):
        f[L2] = "gate/seat"
    if x == 67 and z in (34, 39, 44):
        f[L2 + 4] = ("gate/banner_yellow_e" if z == 34 else
                     "gate/banner_red_e" if z == 39 else "gate/banner_blue_e")
    if x == 89 and z == 44:
        f[L2 + 4] = "gate/banner_blue_w"
    if z == 32 and x in (68, 70, 78):               # woven hangings, at eye height
        f[L2 + 2] = ("gate/banner_blue_s" if x == 68 else
                     "gate/banner_yellow_s" if x == 70 else "gate/banner_red_s")
    if x == 67 and z in (38, 43):
        f[L2 + 3] = "gate/torch_w"
    if x == 89 and z == 43:
        f[L2 + 3] = "gate/torch_e"
    if z == 47 and x in (68, 78, 82):
        f[L2 + 3] = "gate/torch_s"
    if z == 32 and x in (69, 79, 85):
        f[L2 + 3] = "gate/torch_n"
    if (x, z) in ((70, 40), (80, 44), (68, 35)):
        f[L2] = "gate/lantern"
    return f


BED_BAY = (85, 87, 32, 33)      # the bed stands in a low-vaulted corner recess
BED_BAY_Y = 3                   # courses of headroom before the vault closes


def bedchamber_cells(x, z):
    """The duke's chamber in the corner: a curtained bed in its recess, a
    fireplace, a coffer, a garderobe. `None` where the column holds nothing.

    The stair from the lord's hall comes up an open well at x86..88, so the
    only floor east of the bed is the strip at x89: everything there stays
    walked-over, and nothing is built where the well has no floor.
    """
    f = {}
    in_bay = (BED_BAY[0] <= x <= BED_BAY[1] and BED_BAY[2] <= z <= BED_BAY[3])
    if (x, z) in ((85, 32), (86, 32)):
        f[L2] = "gate/dressed"                      # the bed stands on its dais
        f[L2 + 1] = "gate/bed_head"
    elif (x, z) in ((85, 33), (86, 33)):
        f[L2] = "gate/dressed"
        f[L2 + 1] = "gate/bed_foot"
    elif (x, z) in ((87, 32), (87, 33)):
        for dy in range(0, BED_BAY_Y):
            f[L2 + dy] = "gate/curtain"             # the bed's drawn curtain
    elif (x, z) == (88, 32):
        for dy in range(0, 9):
            f[L2 + dy] = "gate/dressed"
    elif (x, z) == (89, 32):
        f[L2] = "gate/fire"
        for dy in range(3, 9):
            f[L2 + dy] = "gate/dressed"
    elif (x, z) == (88, 33):
        f[L2] = "gate/kerb"
        f[L2 + 1] = "gate/lantern"
    elif (x, z) == (89, 33):
        f[L2] = "gate/kerb"
    elif (x, z) == (89, 34):
        f[L2] = "gate/coffer"
    elif (x, z) == (89, 36):
        f[L2] = "gate/privy"                        # the garderobe, in its recess
        f[L2 + 2] = "gate/torch_e"
    elif (x, z) in ((83, 32), (84, 32)):
        f[L2 + 1] = "gate/banner_red_s" if x == 84 else "gate/banner_blue_s"
        if x == 84:
            f[L2] = "gate/lantern"
    elif (x, z) == (85, 35):
        f[L2] = "gate/lantern"
    elif not in_bay:
        return None
    if in_bay:
        for y in range(L2 + BED_BAY_Y, GH_L2[1] + 1):
            f[y] = "gate/dressed"                   # the recess's low vault
    return f


# ------------------------------------------------ the chambers and the parapet walk
L3 = GH_L3[0]                   # y37
C_BRAZIER_FIRE = (72, 39)
WALK_LANTERNS = {
    (68, 33), (68, 40), (68, 46), (85, 33), (85, 45),
    (73, 33), (78, 33), (73, 46), (78, 46),
}


def chamber_cells(x, z):
    """{y: role} in the plain upper chambers: floor course y36, room y37..43."""
    f = {}
    surround = brazier(x, z, C_BRAZIER_FIRE)
    if surround:
        f[L3] = surround
        return f
    if 75 <= x <= 77 and 34 <= z <= 36:
        f[L3] = "gate/sack"
        if (x, z) == (76, 35):
            f[L3 + 1] = "gate/sack"
        return f
    if 78 <= x <= 80 and 42 <= z <= 44:
        f[L3] = "gate/cask"
        return f
    if x == 67 and z in (35, 40, 45):
        f[L3 + 3] = "gate/torch_w"
    if x == 89 and z in (35, 40, 45):
        f[L3 + 3] = "gate/torch_e"
    if z == 32 and x in (70, 78, 85):
        f[L3 + 3] = "gate/torch_n"
    if z == 47 and x in (70, 78, 85):
        f[L3 + 3] = "gate/torch_s"
    if (x, z) in ((69, 38), (69, 43), (84, 36), (84, 44)):
        f[L3] = "gate/lantern"
    return f
