"""The ground, the approach, the courtyard and the curtain wall."""

from .common import *  # noqa: F401,F403

PALETTE = {}
ANCHORS = {
    (77, WALK, 1): ("arrival", "entry"),
    (77, WALK, 19): ("stop-approach", None),
    (46, WALK, 62): ("stop-courtyard", None),
    (50, 23, 90): ("stop-wall-walk", None),
}

def approach_column(c, x, z):
    """The road, the three stepped ditches and the ramparts between them."""
    for z0, z1 in ditch_bands():
        if z0 <= z <= z1:
            if on_road(x):                      # the timber bridge over it
                c.spans = [("rock", 4)]
                c.y = 4
                c.add(None, 3)
                c.add("deck", 1)
                c.air_to_top()
                return c
            depth = DITCH_PROFILE[z - z0]
            c.spans = [("rock", GRADE - depth)]
            c.y = GRADE - depth
            c.add("earth", 1)
            c.air_to_top()
            return c
    c.add("road" if on_road(x) else "turf", 1)
    c.air_to_top()
    return c


def outside_column(c, x, z):
    """The ground the castle stands in, beyond its walls."""
    c.add("turf", 1)
    c.air_to_top()
    return c


def curtain_column(c, x, z):
    """The curtain wall: solid to the walk, crenels on its outer course."""
    west = CX0 <= x <= CX0 + 2 and z >= COURT_Z0
    east = CX1 - 2 <= x <= CX1
    south = SCURT_Z0 <= z <= SCURT_Z1
    corner = (x - 15) ** 2 + (z - 88) ** 2 <= 16 or (x - 88) ** 2 + (z - 88) ** 2 <= 16
    if not (west or east or south or corner):
        return None
    c.add("cobble", 1)
    outer = (west and x == CX0) or (east and x == CX1) or (south and z == SCURT_Z1)
    c.upto("wall", CURTAIN_TOP)
    if outer or corner:
        run = x + z if corner else (z if (west or east) else x)
        c.upto("wall", CURTAIN_CRENEL if crenel(run) else CURTAIN_TOP + 1)
    c.air_to_top()
    return c


def courtyard_column(c, x, z):
    # the three external stairs, each climbing north toward its own door
    flights = [
        (67, 70, 50, 57, WALK, F1),        # up to the lord's hall
        (36, 39, 46, 53, WALK, F1),        # up to the great hall's west door
        (16, 19, 50, 57, WALK, F1),        # up the kitchen tower's turret
    ]
    for x0, x1, z0, z1, y0, y1 in flights:
        if x0 <= x <= x1:
            h = stair_height(z, z0, z1, y0, y1)
            if h is not None:
                c.add("cobble", 1)
                c.upto("step", h)
                c.air_to_top()
                return c
    # the long flight up onto the east wall-walk
    if 86 <= x <= 88 and 56 <= z <= 84:
        c.add("cobble", 1)
        c.upto("step", WALK + (84 - z) // 2)
        c.air_to_top()
        return c
    # the well: a ring of cobble with its shaft open at the walk plane
    if 49 <= x <= 51 and 61 <= z <= 63:
        c.add("cobble", 1)
        if not (x == 50 and z == 62):
            c.add("wall", 1)
        c.air_to_top()
        return c
    c.add("cobble", 1)
    c.air_to_top()
    return c

