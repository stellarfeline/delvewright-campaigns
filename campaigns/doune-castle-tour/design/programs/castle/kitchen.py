"""The kitchen tower and the servery: the kitchen, the royal apartments and the bedchambers over them."""

from .common import *  # noqa: F401,F403

PALETTE = {}
ANCHORS = {
    (20, F1 + 1, 40): ("stop-kitchen", None),
    (30, F1 + 1, 38): ("servery", None),
    (20, KT_L2[0], 40): ("stop-royal-apartments", None),
}

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
    c.upto(None, KT_L1[1])
    c.upto("roof", KT_L1[1] + 2)
    c.air_to_top()
    return c

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
    c.add(None, CELLAR[1] - CELLAR[0] + 1)
    c.add("floor_hall", 1)
    west_strip = 14 <= x <= 16          # flights 1 and 3 climb north here
    east_strip = 18 <= x <= 20          # flight 2 climbs south here
    if west_strip and 32 <= z <= 43:
        c.upto("step", F1 + (43 - z))
        c.add(None, max(0, KT_F2 - c.y))
    else:
        c.upto(None, KT_L1[1])
        c.add("floor_upper", 1)
    if east_strip and 32 <= z <= 41:
        c.upto("step", KT_F2 + (z - 32))
        c.add(None, max(0, KT_F3 - c.y))
    else:
        c.upto(None, KT_L2[1])
        c.add("floor_upper", 1)
    if west_strip and 32 <= z <= 39:
        c.upto("step", KT_F3 + (39 - z))
        c.add(None, max(0, KT_PARAPET - c.y))
    else:
        c.upto(None, KT_L3[1])
        c.add("floor_stone", 1)
    gx0, gx1, gz0, gz1 = 17, 22, 35, 44
    if gx0 <= x <= gx1 and gz0 <= z <= gz1:
        dist = min(x - gx0, gx1 - x)
        top = KT_PARAPET + 1 + dist
        c.upto(None, top - 2)
        c.upto("roof", top)
    c.air_to_top()
    return c

