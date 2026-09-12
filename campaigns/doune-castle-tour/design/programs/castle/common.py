"""Shared vocabulary for the Doune site generator.

Every module describes its own part of the site one column at a time: what
stands at each course, from the ground up. `Col` is that column, the constants
below are the storey heights every part shares, and the emitter turns the
columns into the grammar's partition.

Local axes: x east, y up, z south. World north is -z, so the approach (low z)
is the castle's north front. A body's feet stand at y=8; y=7 is the surface.
"""

X, Y, Z = 104, 56, 120
GRADE = 7            # the surface course
WALK = 8             # where feet stand

# ------------------------------------------------------------ the footprint
CX0, CX1 = 12, 91          # the castle, east-west
CZ0, CZ1 = 30, 91          # the castle, north-south
RANGE_Z1 = 49              # the north range ends here
COURT_Z0, COURT_Z1 = 50, 88
SCURT_Z0, SCURT_Z1 = 89, 91

KT = (12, 27, 30, 49)      # kitchen tower   x0,x1,z0,z1
SV = (28, 32, 30, 45)      # servery
HALL = (33, 64, 30, 45)    # great hall
GH = (65, 91, 30, 49)      # gatehouse

KT_IN = (14, 25, 32, 47)
SV_IN = (29, 31, 32, 43)
HALL_IN = (35, 62, 32, 43)
GH_IN = (67, 89, 32, 47)
PASSAGE = (75, 79)         # the gate passage runs the gatehouse's whole depth

# storey courses: the floor course, then the air above it
CELLAR = (8, 14)
F1 = 15                    # hall / kitchen / lord's hall floor course
HALL_IN_TOP = 27           # the hall is open to its roof
GH_L1 = (16, 25)
GH_F2 = 26
GH_L2 = (27, 35)
GH_F3 = 36
GH_L3 = (37, 43)
GH_PARAPET = 44            # the walk surface; crenels stand on it
GH_WALL_TOP = 47
KT_L1 = (16, 25)
KT_F2 = 26
KT_L2 = (27, 34)
KT_F3 = 35
KT_L3 = (36, 41)
KT_PARAPET = 42
KT_WALL_TOP = 45
CURTAIN_TOP = 22           # solid to here; a body walks at y23
CURTAIN_CRENEL = 25

ROAD = (75, 79)            # the road runs at the gate passage's own width


def ditch_bands():
    """Three dry ditches on the north approach, with ramparts between them.

    Each is six rows wide and cut in steps, so a body that walks down into one
    walks out of it again: a dry ditch nobody can be trapped in.
    """
    return [(3, 8), (12, 17), (21, 26)]

DITCH_PROFILE = [1, 2, 3, 3, 2, 1]      # courses below grade, row by row


def inside(x, z, box):
    x0, x1, z0, z1 = box
    return x0 <= x <= x1 and z0 <= z <= z1


def on_road(x):
    return ROAD[0] <= x <= ROAD[1]


def crenel(coord):
    """Merlons on even cells, gaps on odd: the parapet's tooth pattern."""
    return coord % 2 == 0


def wall_face(x, z, box, inset=2):
    """True on a building's wall ring."""
    x0, x1, z0, z1 = box
    return not (x0 + inset <= x <= x1 - inset and z0 + inset <= z <= z1 - inset)


def stair_height(z, z_low, z_high, y_low, y_high):
    """A straight flight: one course per cell, climbing toward z_high."""
    if not (z_low <= z <= z_high):
        return None
    return y_low + (z_high - z)


class Col:
    """A column of the site, built bottom to top."""

    def __init__(self):
        self.spans = []
        self.y = 0

    def add(self, role, n):
        if n <= 0:
            return
        self.spans.append((role, n))
        self.y += n

    def upto(self, role, top):
        self.add(role, top - self.y + 1)

    def air_to_top(self):
        self.add(None, Y - self.y)

    def key(self):
        return tuple(self.spans)


# The masonry and ground vocabulary every part of the site shares. A part that
# needs its own materials declares them in its own PALETTE, under its own
# prefix, so two parts can never disagree about one role.
PALETTE = {
    "rock": "minecraft:stone",
    "earth": "minecraft:dirt",
    "turf": "minecraft:grass_block[snowy=false]",
    "road": "minecraft:packed_mud",
    "deck": "minecraft:dark_oak_planks",
    "cobble": [
        {"weight": 8, "block": "minecraft:cobblestone"},
        {"weight": 2, "block": "minecraft:andesite"},
        {"weight": 1, "block": "minecraft:stone_bricks"},
    ],
    "plinth": "minecraft:stone_bricks",
    "step": "minecraft:stone_bricks",
    "wall": [
        {"weight": 10, "block": "minecraft:stone_bricks"},
        {"weight": 2, "block": "minecraft:cracked_stone_bricks"},
        {"weight": 2, "block": "minecraft:cobblestone"},
        {"weight": 1, "block": "minecraft:andesite"},
    ],
    "roof": [
        {"weight": 8, "block": "minecraft:deepslate_tiles"},
        {"weight": 2, "block": "minecraft:cracked_deepslate_tiles"},
    ],
    "floor_stone": "minecraft:stone_bricks",
    "floor_hall": "minecraft:polished_andesite",
    "floor_upper": "minecraft:spruce_planks",
}
