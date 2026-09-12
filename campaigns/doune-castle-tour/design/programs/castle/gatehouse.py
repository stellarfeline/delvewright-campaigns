"""The gatehouse: the gate passage, the guardroom and prison, the lord's and duchess's halls, the chambers and the parapet."""

from .common import *  # noqa: F401,F403

PALETTE = {}
ANCHORS = {
    (77, WALK, 40): ("stop-gate", None),
    (70, WALK, 40): ("guardroom", None),
    (85, WALK, 40): ("pit-prison", None),
    (72, GH_L1[0], 40): ("stop-lords-hall", None),
    (72, GH_L2[0], 40): ("stop-duchess-hall", None),
    (72, GH_L2[0], 46): ("oratory", None),
    (84, GH_L2[0], 34): ("bedchamber", None),
}

def window(c, sill, height, top, role="wall"):
    """A wall column carrying an opening: masonry, void, masonry."""
    c.upto(role, sill - 1)
    c.add(None, height)
    c.upto(role, top)

def gatehouse(c, x, z):
    x0, x1, z0, z1 = GH
    ix0, ix1, iz0, iz1 = GH_IN
    px0, px1 = PASSAGE
    in_passage = px0 <= x <= px1

    # --- the gate passage runs through both walls at ground level
    if in_passage and CZ0 <= z <= RANGE_Z1:
        c.add("floor_stone", 1)
        arch = 13 if x in (px0, px1) else 14      # a stepped arch head
        c.add(None, arch - WALK + 1)
        c.upto("wall", F1)
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
        door = 36 <= z <= 38
        if door:
            c.add(None, 3)
            c.upto("wall", F1)
        else:
            c.upto("wall", F1)
    else:
        c.add(None, CELLAR[1] - CELLAR[0] + 1)
        c.add("floor_stone", 1)
    return gatehouse_upper(c, x, z, from_y=F1 + 1)

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
        c.upto(None, GH_L1[1])
        c.add("floor_upper", 1)
    # level 2: the duchess's hall, and the flight up to the chambers
    if mid_strip and 33 <= z <= 43:
        c.upto("step", GH_F2 + (z - 33))
        c.add(None, max(0, GH_F3 - c.y))
    else:
        c.upto(None, GH_L2[1])
        c.add("floor_upper", 1)
    # level 3: the chambers, and the flight out onto the parapet
    if east_strip and 33 <= z <= 40:
        c.upto("step", GH_F3 + (40 - z))
        c.add(None, max(0, GH_PARAPET - c.y))
    else:
        c.upto(None, GH_L3[1])
        c.add("floor_stone", 1)
    # the garret stands inside the parapet walk, which runs all round it
    gx0, gx1, gz0, gz1 = 71, 83, 35, 44
    if gx0 <= x <= gx1 and gz0 <= z <= gz1:
        dist = min(z - gz0, gz1 - z)
        top = GH_PARAPET + 1 + dist
        c.upto(None, top - 2)
        c.upto("roof", top)
    c.air_to_top()
    return c

