"""The kitchen tower and the servery: the kitchen, the royal apartments and the bedchambers over them.

The tower carries the household's working end. Its vaulted kitchen fills the
hall storey, with the larder walled off its south-east corner and the servery
beyond the east wall passing food to the great hall through two hatches. The
guest lodgings — the Royal Apartments — stack above the kitchen, the plainer
bedchambers above those, and the parapet walk over all of it.

Every room is furnished from one rule: a column of the tower is a stack of
courses, so each storey hands back its own spans and `lay` puts them down. A
span height of `None` means "fill to this storey's ceiling".

**Fire is never a cell a body can enter.** Every campfire here burns inside a
kerb of full blocks, and something solid closes the course two above the flame
— the iron spit bar over the kitchen hearth, the chimney breast over each
lodging fireplace, the oven's own masonry over its embers — so the cell above
the fire has less than a body's clearance and neither the walk nor the game
will put a player in it. The parapet brazier stands instead inside a ring of
wall posts, which are a block and a half tall and so cannot be stepped over.

**Light is placed with the rooms, not swept over them afterwards.** The cellar,
the servery and the bedchambers carry no window at all, so every one of their
floor cells is lit to block light 8 or better by lantern, torch and fire alone;
so is every other roofed room in the tower, before any daylight is counted.
"""

from .common import *  # noqa: F401,F403

PALETTE = {
    # masonry the tower's own furniture is built from
    "kt/vault": "minecraft:stone_bricks",
    "kt/breast": "minecraft:polished_andesite",
    "kt/arch": "minecraft:chiseled_stone_bricks",
    "kt/soot": "minecraft:deepslate_bricks",
    "kt/hearth": "minecraft:cobblestone",
    "kt/partition": "minecraft:stone_bricks",
    "kt/oven": "minecraft:smooth_stone",
    "kt/oven_cap": "minecraft:smooth_stone_slab[type=bottom,waterlogged=false]",
    "kt/drain": "minecraft:deepslate_tile_slab[type=bottom,waterlogged=false]",
    "kt/dais": "minecraft:polished_andesite",
    # fire, and the iron over it
    "kt/fire": "minecraft:campfire[facing=north,lit=true,signal_fire=false,waterlogged=false]",
    "kt/embers": "minecraft:campfire[facing=east,lit=true,signal_fire=false,waterlogged=false]",
    "kt/cauldron": "minecraft:cauldron",
    "kt/chain": "minecraft:iron_chain[axis=y,waterlogged=false]",
    "kt/spit": "minecraft:iron_chain[axis=x,waterlogged=false]",
    # light: a lantern hangs on a chain, a lamp stands, a torch faces off its wall
    "kt/lantern": "minecraft:lantern[hanging=true,waterlogged=false]",
    "kt/lamp": "minecraft:lantern[hanging=false,waterlogged=false]",
    "kt/torch_n": "minecraft:wall_torch[facing=north]",
    "kt/torch_s": "minecraft:wall_torch[facing=south]",
    "kt/torch_e": "minecraft:wall_torch[facing=east]",
    "kt/torch_w": "minecraft:wall_torch[facing=west]",
    "kt/candles": "minecraft:candle[candles=3,lit=true,waterlogged=false]",
    # the kitchen's own stuff
    "kt/table_leg": "minecraft:stripped_oak_log[axis=y]",
    "kt/table_top": "minecraft:oak_slab[type=bottom,waterlogged=false]",
    "kt/stool": "minecraft:spruce_log[axis=y]",
    "kt/cask_x": "minecraft:spruce_log[axis=x]",
    "kt/cask_z": "minecraft:spruce_log[axis=z]",
    "kt/sack": "minecraft:hay_block[axis=y]",
    "kt/shelf": "minecraft:oak_slab[type=top,waterlogged=false]",
    "kt/counter": "minecraft:smooth_stone",
    "kt/counter_top": "minecraft:smooth_stone_slab[type=bottom,waterlogged=false]",
    "kt/vessel": "minecraft:flower_pot",
    # the lodgings
    "kt/beam": "minecraft:dark_oak_log[axis=x]",
    "kt/rail": "minecraft:dark_oak_fence[east=false,north=true,south=true,waterlogged=false,west=false]",
    "kt/rail_x": "minecraft:dark_oak_fence[east=true,north=false,south=false,waterlogged=false,west=true]",
    "kt/bench": "minecraft:spruce_slab[type=bottom,waterlogged=false]",
    "kt/post": "minecraft:dark_oak_fence[east=false,north=false,south=false,waterlogged=false,west=false]",
    "kt/chair": "minecraft:oak_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]",
    "kt/lectern": "minecraft:lectern[facing=south,has_book=false,powered=false]",
    "kt/coffer": "minecraft:stripped_dark_oak_log[axis=x]",
    "kt/cloth_red": "minecraft:red_wool",
    "kt/cloth_gold": "minecraft:yellow_wool",
    "kt/banner": "minecraft:red_wall_banner[facing=south]",
    "kt/rug_edge": "minecraft:red_carpet",
    "kt/rug_field": "minecraft:blue_carpet",
    "kt/rug_star": "minecraft:yellow_carpet",
    "kt/bed_head": "minecraft:red_bed[facing=north,occupied=false,part=head]",
    "kt/bed_foot": "minecraft:red_bed[facing=north,occupied=false,part=foot]",
    # the parapet brazier: fire in a ring of posts nothing steps over
    "kt/brazier": "minecraft:cobblestone_wall[east=none,north=none,south=none,up=true,waterlogged=false,west=none]",
}
ANCHORS = {
    (20, F1 + 1, 40): ("stop-kitchen", None),
    (30, F1 + 1, 38): ("servery", None),
    (20, KT_L2[0], 40): ("stop-royal-apartments", None),
}


def lay(c, spans, top):
    """Lay one storey's spans from the current course, then air to `top`.

    A span height of `None` fills the rest of the storey with that role, which
    is how a chimney breast or a partition reaches the ceiling without each
    site having to know how tall the storey is.
    """
    for role, n in spans:
        if n is None:
            c.upto(role, top)
        else:
            c.add(role, n)
    c.upto(None, top)


# =========================================================== the servery

# The servery is three cells wide: a dresser down its east side, shelves down
# its west, and one walk between them. The two doorways (z36..38) stay clear.
SV_COUNTER_X = 31
SV_COUNTER_Z = (39, 42)                 # the run under the two serving hatches
SV_COUNTER_STEP = (31, 43)              # a cask to step up by
SV_DRESSER_Z = (32, 35)                 # the low dresser north of the doors
SV_SHELF_X = 29
SV_SHELF_Z = ((32, 35), (39, 42))
SV_POTS = {(31, 33)}
SV_VESSELS = {(31, 32), (31, 34), (31, 39), (31, 41)}
SV_LAMPS = {(30, 34), (30, 36), (30, 38), (30, 42)}
SV_TORCHES = {(30, 31): "kt/torch_s", (30, 44): "kt/torch_n"}


def sv_vault(x):
    """Courses of stone hung under the servery's roof, so the room reads small."""
    return 4 - min(x - SV_IN[0], SV_IN[1] - x)


def servery_contents(x, z):
    """Spans laid on the servery floor at y16, bottom up."""
    spans = []
    if (x, z) in SV_LAMPS:
        return [(None, 4), ("kt/lantern", 1), ("kt/chain", None)]
    if x == SV_COUNTER_X and SV_COUNTER_Z[0] <= z <= SV_COUNTER_Z[1]:
        spans += [("kt/counter", 1), ("kt/counter_top", 1)]
        if (x, z) in SV_VESSELS:
            spans.append(("kt/vessel", 1))
        return spans
    if (x, z) == SV_COUNTER_STEP:
        return [("kt/cask_x", 1)]
    if x == SV_COUNTER_X and SV_DRESSER_Z[0] <= z <= SV_DRESSER_Z[1]:
        spans = [("kt/counter", 1)]                 # a low dresser, walked onto
        if (x, z) in SV_POTS:
            spans.append(("kt/cauldron", 1))
        elif (x, z) in SV_VESSELS:
            spans.append(("kt/vessel", 1))
        return spans
    if x == SV_SHELF_X and any(a <= z <= b for a, b in SV_SHELF_Z):
        # a cask on the floor and two boards over it; the ceiling sits close
        # enough over the top board that nothing stands on either
        return [("kt/cask_x", 1), (None, 1), ("kt/shelf", 1), (None, 1), ("kt/shelf", 1)]
    if (x, z) in SV_TORCHES:
        return [(None, 3), (SV_TORCHES[(x, z)], 1)]
    return spans


def servery(c, x, z):
    x0, x1, z0, z1 = SV
    if wall_face(x, z, SV, inset=1):
        c.add("plinth", 1)
        door = (x == x0 or x == x1) and 36 <= z <= 38
        hatch = x == x1 and 39 <= z <= 41
        if door:
            c.upto("wall", F1)
            c.add(None, 3)
            c.upto("wall", KT_L1[1] + 1)
        elif hatch:
            c.upto("wall", F1 + 2)
            c.add(None, 2)
            c.upto("wall", KT_L1[1] + 1)
        else:
            c.upto("wall", KT_L1[1] + 1)
        c.upto("roof", KT_L1[1] + 2)
        c.air_to_top()
        return c
    c.add("floor_stone", 1)
    c.upto("wall", F1)                          # solid base, no doorless room
    lay(c, servery_contents(x, z), KT_L1[1] - sv_vault(x))
    c.upto("kt/vault", KT_L1[1])
    c.upto("roof", KT_L1[1] + 2)
    c.air_to_top()
    return c


# ====================================================== the cellar, under all

CE_CASK_X = (15, 17)
CE_CASK_Z = (34, 35, 38, 39, 42, 43)
CE_CASK_TALL = 16                       # the middle of the row is stacked two high
CE_SACK_X = (22, 24)
CE_SACK_Z = (33, 34, 37, 38)
CE_SACK_TALL = 23
# The cellar has no window at all, so its light is all lantern and torch: eleven
# lanterns hung low over the casks, on a six-cell grid, and six wall torches.
CE_LAMPS = {(15, 33), (15, 45), (18, 33), (18, 37), (18, 41), (18, 45),
            (21, 35), (21, 40), (21, 45), (24, 41), (24, 45)}
CE_TORCHES = {
    (25, 36): "kt/torch_w", (25, 42): "kt/torch_w",
    (14, 36): "kt/torch_e", (14, 42): "kt/torch_e",
    (17, 32): "kt/torch_s", (22, 32): "kt/torch_s",
}


def cellar_contents(x, z):
    """Casks and sacks in the tower's cellar, and the light over them."""
    if (x, z) in CE_LAMPS:
        return [(None, 3), ("kt/lantern", 1), ("kt/chain", None)]
    if (x, z) in CE_TORCHES:
        return [(None, 3), (CE_TORCHES[(x, z)], 1)]
    if CE_CASK_X[0] <= x <= CE_CASK_X[1] and z in CE_CASK_Z:
        return [("kt/cask_z", 2 if x == CE_CASK_TALL else 1)]
    if CE_SACK_X[0] <= x <= CE_SACK_X[1] and z in CE_SACK_Z:
        return [("kt/sack", 2 if x == CE_SACK_TALL else 1)]
    return []


# =========================================================== the kitchen

# The great fireplace fills the kitchen's whole north end: one pier each side, a
# seven-block mouth between them under a stepped arch, the fire raised on its own
# hearth course a cell behind the lip, and cold hearth shoulders a body can stand
# on either side of it.
FIRE_Z, MOUTH_Z = 32, 33
FIRE_WALL = (17, 25)                    # every interior column of the north end
FIRE_JAMB = (17, 25)                    # the piers, and the breast over them
FIRE_BED = (20, 22)                     # the burning cells
FIRE_POT = 21                           # the cauldron hangs on its crane here
ARCH_TOP = {18: 19, 19: 20, 20: 21, 21: 21, 22: 21, 23: 20, 24: 19}

OVEN = (24, 25, 34, 35)                 # the bread oven, beside the fireplace
OVEN_MOUTH = (24, 34)
OVEN_FIRE = (25, 34)

# The work table stands west of the door-to-hearth line, so a body at the
# kitchen stop looks straight down the room at the fire.
TABLE = (17, 19, 36, 38)
KT_TABLE_WARE = {(18, 37): "kt/candles", (17, 38): "kt/vessel", (19, 36): "kt/vessel"}
KT_STOOLS = {(19, 39), (17, 35)}
DRAIN_X = 23
DRAIN_Z = (34, 42)
DRESSER_X = 25
DRESSER_Z = (39, 42)
DRESSER_STEP = (24, 42)

LARDER = (22, 25, 44, 47)               # walled off the kitchen's south-east
LARDER_WALL_Z = 43                      # its north wall, x22..25
LARDER_WALL_X = 21                      # its west wall, z44..47
LARDER_DOOR_X = (23, 24)
LARDER_SHELF_X = 25
LARDER_SACKS = {(22, 46): 2, (22, 47): 1, (23, 47): 1}

KT_LOGS = {(24, 37): 2, (24, 38): 1}    # the log pile by the drain
KT_SACKS = {(17, 34): 1, (18, 34): 1, (14, 46): 1, (15, 46): 2}
KT_CASKS = {(14, 44): 1, (14, 45): 2, (15, 44): 1}
KT_LAMPS = {(18, 35), (22, 35), (18, 41), (22, 41), (15, 45), (19, 45), (23, 46), (17, 42), (24, 45), (24, 39)}
KT_TORCHES = {
    (17, 39): "kt/torch_e",
    (22, 42): "kt/torch_n", (20, 45): "kt/torch_w",
    (14, 47): "kt/torch_n", (20, 47): "kt/torch_n", (22, 47): "kt/torch_n",
}


def kt_vault(x):
    """Courses of the barrel vault hung over the kitchen, by distance from the wall."""
    return max(0, 4 - min(x - KT_IN[0], KT_IN[1] - x))


def kitchen_floor_role(x, z):
    """The floor course under the kitchen: a sunk channel where the drain runs."""
    if x == DRAIN_X and DRAIN_Z[0] <= z <= DRAIN_Z[1]:
        return "kt/drain"
    return "floor_hall"


def kitchen_contents(x, z):
    """Spans laid on the kitchen floor at y16, bottom up."""
    # ---- the great fireplace, and the oven beside it
    if z == FIRE_Z and FIRE_WALL[0] <= x <= FIRE_WALL[1]:
        # The spit bar closes the course two above every burning cell, so a body
        # can stand on the hearth's cold shoulders and never in the fire.
        if x in FIRE_JAMB:
            return [("kt/breast", None)]
        if x == FIRE_POT:
            return [("kt/hearth", 1), ("kt/fire", 1), ("kt/cauldron", 1),
                    ("kt/spit", 1), (None, 1), ("kt/soot", None)]
        if FIRE_BED[0] <= x <= FIRE_BED[1]:
            return [("kt/hearth", 1), ("kt/fire", 1), (None, 1),
                    ("kt/spit", 1), (None, 1), ("kt/soot", None)]
        return [("kt/hearth", 1), (None, 2), ("kt/spit", 1),
                (None, 1), ("kt/soot", None)]                   # the hearth's ends
    if z == MOUTH_Z and FIRE_WALL[0] <= x <= FIRE_WALL[1]:
        if x in FIRE_JAMB:
            return [("kt/breast", None)]
        top = ARCH_TOP[x]
        return [("kt/hearth", 1), (None, top - F1 - 1), ("kt/arch", 1), ("kt/breast", None)]
    if inside(x, z, OVEN):
        if (x, z) == OVEN_MOUTH:
            return [("kt/oven", 1), (None, 1), ("kt/oven", 3), ("kt/oven_cap", 1)]
        if (x, z) == OVEN_FIRE:
            return [("kt/oven", 1), ("kt/embers", 1), ("kt/oven", 3), ("kt/oven_cap", 1)]
        return [("kt/oven", 5), ("kt/oven_cap", 1)]

    # ---- the larder's two partitions, and what stands inside it
    if z == LARDER_WALL_Z and LARDER[0] <= x <= LARDER[1]:
        if LARDER_DOOR_X[0] <= x <= LARDER_DOOR_X[1]:
            return [(None, 3), ("kt/partition", None)]
        return [("kt/partition", None)]
    if x == LARDER_WALL_X and LARDER[2] <= z <= LARDER[3]:
        return [("kt/partition", None)]
    if x == LARDER_SHELF_X and LARDER[2] <= z <= LARDER[3]:
        return [("kt/cask_x", 1), (None, 1), ("kt/shelf", 1), (None, 1), ("kt/shelf", 1)]
    if (x, z) in LARDER_SACKS:
        return [("kt/sack", LARDER_SACKS[(x, z)])]

    # ---- light, laid before the furniture so nothing stands under a chain
    if (x, z) in KT_LAMPS:
        return [(None, 4), ("kt/lantern", 1), ("kt/chain", None)]

    # ---- the work table, its stools, the dresser and the stores
    if inside(x, z, TABLE):
        spans = [("kt/table_leg", 1), ("kt/table_top", 1)]
        if (x, z) in KT_TABLE_WARE:
            spans.append((KT_TABLE_WARE[(x, z)], 1))
        return spans
    if (x, z) in KT_STOOLS:
        return [("kt/stool", 1)]
    if x == DRESSER_X and DRESSER_Z[0] <= z <= DRESSER_Z[1]:
        return [("kt/counter", 1), ("kt/counter_top", 1)]
    if (x, z) == DRESSER_STEP:
        return [("kt/cask_x", 1)]
    if (x, z) in KT_SACKS:
        return [("kt/sack", KT_SACKS[(x, z)])]
    if (x, z) in KT_CASKS:
        return [("kt/cask_z", KT_CASKS[(x, z)])]
    if (x, z) in KT_LOGS:
        spans = [("kt/cask_z", KT_LOGS[(x, z)])]
        if (x, z) in KT_TORCHES:
            spans += [(None, 3 - KT_LOGS[(x, z)]), (KT_TORCHES[(x, z)], 1)]
        return spans
    if (x, z) in KT_TORCHES:
        return [(None, 3), (KT_TORCHES[(x, z)], 1)]
    return []


# =================================================== the royal apartments

RA_RAIL_X = 17                          # a balustrade along the open stair well
RA_RAIL_Z = (33, 43)
RA_RAIL_SOUTH = (14, 16, 44)            # and across its south end, x14..16
RA_SEATS = {(25, 36), (25, 41)}         # window seats under the east lights
RA_BED_RUG = (15, 19, 45, 46)
RA_BED_COFFER = (17, 47)
RA_DAIS = (21, 23, 33, 35)              # the low step the chair of state stands on
RA_CHAIR = (22, 34)
RA_TESTER_Z = (33, 35)                  # the cloth canopy over it
RA_BANNERS = {(20, 32), (21, 32), (22, 32), (23, 32), (24, 32)}
RA_FIRE_X = 25
RA_FIRE_Z = (37, 39)
RA_RUG = (21, 24, 37, 42)
RA_DESK = {(25, 33), (25, 34)}
RA_LECTERN = (25, 35)
RA_PART_Z = 43                          # the bedchamber wall
RA_PART_X = (18, 25)
RA_DOOR_X = (21, 22)
RA_BED = (23, 45)                       # head; the foot lies one cell south
RA_POSTS = {(22, 45), (22, 46), (24, 45), (24, 46)}
RA_COFFER = (21, 47)
RA_BED_FIRE_X = 25
RA_BED_FIRE_Z = (45, 47)
RA_LAMPS = {(21, 36), (20, 42), (18, 44), (20, 45), (24, 44), (15, 47)}
RA_TORCHES = {
    (17, 32): "kt/torch_s", (25, 32): "kt/torch_s",
    (16, 47): "kt/torch_n", (20, 47): "kt/torch_n",
    (25, 42): "kt/torch_w", (25, 44): "kt/torch_w",
}
RA_BEAM_Z = (36, 40, 44, 47)
# The flight to the bedchambers is a blind stone flank down the middle of this
# storey; these hang on its east face, each at the height of the tread behind it,
# so the wall the stop looks past carries light of its own.
RA_STAIR_X = 20
RA_STAIR_TORCH_Z = (34, 36, 38)


def royal_contents(x, z):
    """Spans laid on the royal apartments' floor at y27, bottom up."""
    top = KT_L2[1]                                      # 34: the last open course
    if 14 <= x <= 16 and 32 <= z <= 43:
        return []                   # the well the kitchen stair climbs through
    if x == RA_RAIL_X and RA_RAIL_Z[0] <= z <= RA_RAIL_Z[1]:
        return [("kt/rail", 1)]
    if RA_RAIL_SOUTH[0] <= x <= RA_RAIL_SOUTH[1] and z == RA_RAIL_SOUTH[2]:
        return [("kt/rail_x", 1)]
    if z == RA_PART_Z and RA_PART_X[0] <= x <= RA_PART_X[1]:
        if RA_DOOR_X[0] <= x <= RA_DOOR_X[1]:
            return [(None, 3), ("kt/partition", None)]
        return [("kt/partition", None)]
    if x == RA_STAIR_X and z in RA_STAIR_TORCH_Z:
        return [(None, z - 33), ("kt/torch_e", 1)]

    # ---- the chair of state, its cloth and the hanging behind it
    if (x, z) in RA_BANNERS:
        return [(None, 5), ("kt/banner", 1)]
    if inside(x, z, RA_DAIS):
        spans = [("kt/dais", 1)]
        if (x, z) == RA_CHAIR:
            spans.append(("kt/chair", 1))
        if RA_TESTER_Z[0] <= z <= RA_TESTER_Z[1]:
            # the cloth of estate: two courses of it hung against the ceiling,
            # so nothing can stand on top of the canopy
            spans += [(None, top - 1 - (KT_L2[0] + len(spans))),
                      ("kt/cloth_gold", 1), ("kt/cloth_red", 1)]
        return spans

    # ---- the fireplace, one cell deep in the east wall
    if x == RA_FIRE_X and RA_FIRE_Z[0] <= z <= RA_FIRE_Z[1]:
        lit = z == (RA_FIRE_Z[0] + RA_FIRE_Z[1]) // 2
        return [("kt/fire" if lit else "kt/hearth", 1), (None, 1), ("kt/breast", None)]

    # ---- light
    if (x, z) in RA_LAMPS:
        return [(None, 3), ("kt/lantern", 1), ("kt/chain", None)]
    if (x, z) in RA_TORCHES:
        return [(None, 3), (RA_TORCHES[(x, z)], 1)]

    # ---- the writing table
    if (x, z) == RA_LECTERN:
        return [("kt/lectern", 1)]
    if (x, z) in RA_DESK:
        return [("kt/table_leg", 1), ("kt/table_top", 1)]

    # ---- the great bed through the door, curtained between four posts
    if x == RA_BED[0] and RA_BED[1] <= z <= RA_BED[1] + 1:
        head = ("kt/bed_head" if z == RA_BED[1] else "kt/bed_foot", 1)
        return [head, (None, top - 1 - KT_L2[0]), ("kt/cloth_red", 1)]
    if (x, z) in RA_POSTS:
        return [("kt/post", 3), ("kt/cloth_red", None)]
    if (x, z) in (RA_COFFER, RA_BED_COFFER):
        return [("kt/coffer", 1)]
    if (x, z) in RA_SEATS:
        return [("kt/bench", 1)]
    if inside(x, z, RA_BED_RUG):
        return [("kt/rug_field", 1)]
    if x == RA_BED_FIRE_X and RA_BED_FIRE_Z[0] <= z <= RA_BED_FIRE_Z[1]:
        lit = z == (RA_BED_FIRE_Z[0] + RA_BED_FIRE_Z[1]) // 2
        return [("kt/fire" if lit else "kt/hearth", 1), (None, 1), ("kt/breast", None)]

    # ---- the rug, and the beams over everything else
    spans = []
    if inside(x, z, RA_RUG):
        x0, x1, z0, z1 = RA_RUG
        edge = x in (x0, x1) or z in (z0, z1)
        star = (x, z) in ((x0 + 1, z0 + 1), (x1 - 1, z1 - 1))
        spans.append(("kt/rug_edge" if edge else "kt/rug_star" if star else "kt/rug_field", 1))
    if z in RA_BEAM_Z:
        spans += [(None, top - (KT_L2[0] + len(spans))), ("kt/beam", 1)]
    return spans


# ======================================================= the bedchambers

BC_PART_Z = 42
BC_PART_X = (17, 25)
BC_DOOR_X = (21, 22)
BC_BEDS = ((24, 33), (24, 44))          # head cells; the foot lies one cell south
BC_FIRES = ((25, 36, 38), (25, 44, 46))  # x, z0, z1 — the middle cell is lit
BC_COFFERS = {(22, 33), (22, 46)}
BC_TABLES = {(21, 34), (21, 35), (17, 45), (17, 46)}
BC_STOOLS = {(21, 36), (17, 47)}
BC_RUGS = ((21, 23, 37, 39), (21, 23, 43, 45))
BC_LAMPS = {(20, 34), (20, 38), (20, 43), (20, 46), (16, 44), (17, 34), (17, 38), (24, 47)}
BC_TORCHES = {
    (17, 32): "kt/torch_s", (24, 32): "kt/torch_s",
    (17, 47): "kt/torch_n", (21, 47): "kt/torch_n",
    (14, 44): "kt/torch_e", (25, 47): "kt/torch_w",
}


def bed_contents(x, z):
    """Spans laid on the bedchamber floor at y36, bottom up."""
    if 18 <= x <= 19 and 32 <= z <= 41:
        return []        # the well the royal-apartments stair climbs through
    if z == BC_PART_Z and BC_PART_X[0] <= x <= BC_PART_X[1]:
        if BC_DOOR_X[0] <= x <= BC_DOOR_X[1]:
            return [(None, 3), ("kt/partition", None)]
        return [("kt/partition", None)]
    for bx, bz in BC_BEDS:
        if (x, z) == (bx, bz):
            return [("kt/bed_head", 1)]
        if (x, z) == (bx, bz + 1):
            return [("kt/bed_foot", 1)]
    for fx, fz0, fz1 in BC_FIRES:
        if x == fx and fz0 <= z <= fz1:
            lit = z == (fz0 + fz1) // 2
            return [("kt/fire" if lit else "kt/hearth", 1), (None, 1), ("kt/breast", None)]
    if (x, z) in BC_COFFERS:
        return [("kt/coffer", 1)]
    if (x, z) in BC_TABLES:
        return [("kt/table_leg", 1), ("kt/table_top", 1)]
    if (x, z) in BC_STOOLS:
        return [("kt/stool", 1)]
    if any(inside(x, z, r) for r in BC_RUGS):
        return [("kt/rug_edge", 1)]
    if (x, z) in BC_LAMPS:
        return [(None, 2), ("kt/lantern", 1), ("kt/chain", None)]
    if (x, z) in BC_TORCHES:
        return [(None, 3), (BC_TORCHES[(x, z)], 1)]
    return []


# ======================================================= the parapet walk

# The brazier and its lamps stand a cell clear of the walk's outer ring, so no
# post ever cuts a crenel gap off from the walk.
PA_BRAZIER = (23, 34)
PA_RING = {(22, 34), (24, 34), (23, 33), (23, 35)}
PA_LAMPS = {(15, 41), (15, 46), (19, 46), (24, 46), (24, 36), (24, 33), (17, 32)}


def parapet_contents(x, z):
    """What stands on the walk at y43: one brazier, and lamps along the round."""
    if (x, z) == PA_BRAZIER:
        return [("kt/hearth", 1), ("kt/fire", 1)]
    if (x, z) in PA_RING:
        return [("kt/brazier", 1)]
    if (x, z) in PA_LAMPS:
        return [("kt/lamp", 1)]
    return []


# ======================================================= the tower itself

def kitchen_tower(c, x, z):
    x0, x1, z0, z1 = KT
    if wall_face(x, z, KT):
        c.add("plinth", 1)
        north = z <= z0 + 1
        south = z >= z1 - 1
        run = x if (north or south) else z
        door = south and 16 <= x <= 19
        cellar_door = south and 22 <= x <= 24
        east_door = x >= x1 - 1 and 36 <= z <= 38
        if cellar_door:
            c.add(None, 3)
            c.upto("wall", KT_WALL_TOP)
        elif door or east_door:
            c.upto("wall", F1)
            c.add(None, 3)
            c.upto("wall", KT_WALL_TOP)
        else:
            c.upto("wall", F1 + 2)
            if run % 5 == 1:
                c.add(None, 3)
                c.upto("wall", KT_F2 + 2)
            else:
                c.upto("wall", KT_F2 + 2)
            if run % 5 == 1:
                c.add(None, 3)
                c.upto("wall", KT_PARAPET - 1)
            else:
                c.upto("wall", KT_PARAPET - 1)
            c.upto("wall", KT_WALL_TOP if crenel(run) else KT_PARAPET)
        c.air_to_top()
        return c
    # the interior: cellar, kitchen, royal apartments, bedchambers
    c.add("floor_stone", 1)
    lay(c, cellar_contents(x, z), CELLAR[1])
    c.add(kitchen_floor_role(x, z), 1)
    west_strip = 14 <= x <= 16          # flights 1 and 3 climb north here
    # Flight 2 is two cells wide, not three: the `stop-royal-apartments` anchor
    # stands at (20, 27, 40), and a three-wide flight buries it in its own
    # treads. x20 carries the landing strip the anchor stands on instead.
    east_strip = 18 <= x <= 19          # flight 2 climbs south here
    if west_strip and 32 <= z <= 43:
        c.upto("step", F1 + (43 - z))
        c.add(None, max(0, KT_F2 - c.y))
    else:
        lay(c, kitchen_contents(x, z), KT_L1[1] - kt_vault(x))
        c.upto("kt/vault", KT_L1[1])
        c.add("floor_upper", 1)
    if east_strip and 32 <= z <= 41:
        c.upto("step", KT_F2 + (z - 32))
        c.add(None, max(0, KT_F3 - c.y))
    else:
        lay(c, royal_contents(x, z), KT_L2[1])
        c.add("floor_upper", 1)
    if west_strip and 32 <= z <= 39:
        c.upto("step", KT_F3 + (39 - z))
        c.add(None, max(0, KT_PARAPET - c.y))
    else:
        lay(c, bed_contents(x, z), KT_L3[1])
        c.add("floor_stone", 1)
        for role, n in parapet_contents(x, z):
            c.add(role, n)
    gx0, gx1, gz0, gz1 = 17, 22, 35, 44
    if gx0 <= x <= gx1 and gz0 <= z <= gz1:
        dist = min(x - gx0, gx1 - x)
        top = KT_PARAPET + 1 + dist
        c.upto(None, top - 2)
        c.upto("roof", top)
    c.air_to_top()
    return c
