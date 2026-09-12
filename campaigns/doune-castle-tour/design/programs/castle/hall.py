"""The great hall, its dais and its three barrel cellars."""

from .common import *  # noqa: F401,F403

PALETTE = {
    # the hall's own furniture and light, all of it under this part's names
    "hall/dais": "minecraft:polished_andesite",
    "hall/table_leg": "minecraft:oak_fence[east=false,north=false,south=false,waterlogged=false,west=false]",
    "hall/table_top": "minecraft:oak_slab[type=bottom,waterlogged=false]",
    "hall/bench": "minecraft:spruce_slab[type=bottom,waterlogged=false]",
    "hall/hearth_kerb": "minecraft:cobblestone",
    "hall/fire": "minecraft:campfire[facing=north,lit=true,signal_fire=false,waterlogged=false]",
    "hall/screen": "minecraft:dark_oak_planks",
    "hall/gallery": "minecraft:dark_oak_slab[type=bottom,waterlogged=false]",
    "hall/lantern": "minecraft:lantern[hanging=false,waterlogged=false]",
    "hall/torch_n": "minecraft:wall_torch[facing=south]",
    "hall/torch_s": "minecraft:wall_torch[facing=north]",
    "hall/cupboard": "minecraft:bookshelf",
    "hall/canopy": "minecraft:red_wool",
    "hall/cask": "minecraft:spruce_log[axis=z]",
    "hall/sack": "minecraft:hay_block[axis=y]",
    "hall/cellar_lantern": "minecraft:lantern[hanging=false,waterlogged=false]",
}
ANCHORS = {
    (58, F1 + 1, 38): ("stop-great-hall", None),
    (48, WALK, 38): ("cellars", None),
}

def great_hall(c, x, z):
    x0, x1, z0, z1 = HALL
    if wall_face(x, z, HALL):
        c.add("plinth", 1)
        north = z <= z0 + 1
        south = z >= z1 - 1
        run = x if (north or south) else z
        cellar_door = south and 40 <= x <= 42
        west_door = south and 36 <= x <= 38
        hatch = x <= x0 + 1 and 38 <= z <= 40
        gh_door = x >= x1 - 1 and 38 <= z <= 40
        if cellar_door:
            c.add(None, 3)
            c.upto("wall", HALL_IN_TOP)
        elif west_door or gh_door:
            c.upto("wall", F1)
            c.add(None, 3)
            c.upto("wall", HALL_IN_TOP)
        elif hatch:
            c.upto("wall", F1 + 2)
            c.add(None, 2)                      # the serving hatches
            c.upto("wall", HALL_IN_TOP)
        else:
            c.upto("wall", F1 + 2)
            if (north or south) and run % 6 in (1, 2):
                c.add(None, 6)                  # the hall's tall windows
                c.upto("wall", HALL_IN_TOP)
            else:
                c.upto("wall", HALL_IN_TOP)
        # the gable roof: a stepped pitch, ridge running east-west
        dist = min(z - z0, z1 - z)
        c.upto("roof", HALL_IN_TOP + 1 + dist)
        c.air_to_top()
        return c
    # the interior: three barrel cellars under the hall floor
    c.add("floor_stone", 1)
    cross = x in (43, 44, 53, 54)
    if cross and not (38 <= z <= 40):
        c.upto("wall", F1)
    else:
        for role, n in cellar_contents(x, z):
            c.add(role, n)
        c.upto(None, CELLAR[1])
        c.add("floor_hall", 1)
    # the hall itself, furnished, then open to its roof
    for role, n in hall_contents(x, z):
        c.add(role, n)
    c.upto(None, HALL_IN_TOP)
    dist = min(z - z0, z1 - z)
    top = HALL_IN_TOP + 1 + dist
    if louvre(x, z):                    # the smoke hole over the hearth
        c.air_to_top()
        return c
    c.upto(None, top - 2)
    c.upto("roof", top)
    c.air_to_top()
    return c


# --------------------------------------------------------- what stands in it
DAIS_X = 56                    # the raised end, against the lord's hall door
HIGH_TABLE_X = 59
HEARTH = (45, 47, 37, 39)      # the open hearth, kerb and all
TABLES = ((35, 34, 36), (42, 41, 43))     # table row, and its two bench rows
TABLE_RUN = (40, 54)
SCREEN_X = (36, 37)
TORCH_X = (40, 46, 52, 58)


def louvre(x, z):
    """The hole in the ridge that the hearth smoke goes out of."""
    return 45 <= x <= 47 and 37 <= z <= 39


def hall_contents(x, z):
    """Spans laid on the hall floor at y16, bottom up. Air is `None`."""
    hx0, hx1, hz0, hz1 = HALL_IN
    spans = []
    on_dais = x >= DAIS_X
    if on_dais:
        spans.append(("hall/dais", 1))                       # y16: the step up
        if x == HIGH_TABLE_X and 34 <= z <= 41:
            spans += [("hall/table_leg", 1), ("hall/table_top", 1)]
            if z in (36, 39):
                spans.append(("hall/lantern", 1))
        elif x in (DAIS_X + 1, DAIS_X + 2) and z in (37, 38):
            spans.append(("hall/bench", 1))                  # the great chair's step
        # the cloth of estate hangs over the high table
        if 58 <= x <= 61 and 34 <= z <= 41:
            spans += [(None, 21 - (WALK + len(spans))), ("hall/canopy", 1)]
        return spans

    if HEARTH[0] <= x <= HEARTH[1] and HEARTH[2] <= z <= HEARTH[3]:
        centre = (x == 46 and z == 38)
        spans.append(("hall/fire" if centre else "hall/hearth_kerb", 1))
        return spans

    for table_z, bench_a, bench_b in TABLES:
        if TABLE_RUN[0] <= x <= TABLE_RUN[1]:
            if z == table_z:
                spans += [("hall/table_leg", 1), ("hall/table_top", 1)]
                if x in (44, 50):
                    spans.append(("hall/lantern", 1))
                return spans
            if z in (bench_a, bench_b):
                spans.append(("hall/bench", 1))
                return spans

    if SCREEN_X[0] <= x <= SCREEN_X[1]:
        if 36 <= z <= 38:                                    # the two openings
            spans.append((None, 4))
        else:
            spans.append(("hall/screen", 6))
        spans += [(None, 22 - (WALK + 8 + 1)), ("hall/gallery", 1)]
        return spans

    if x in (38, 39) and z in (32, 33):
        spans.append(("hall/cupboard", 2))                   # the plate cupboard
        return spans

    if x in TORCH_X and z in (hz0, hz1):
        spans += [(None, 3), ("hall/torch_n" if z == hz0 else "hall/torch_s", 1)]
        return spans
    return spans


def cellar_contents(x, z):
    """Casks and sacks in the three barrel cellars, and a lantern each."""
    spans = []
    if z in (34, 35, 41, 42) and x in (37, 38, 39, 47, 48, 49, 57, 58, 59):
        spans.append(("hall/cask", 1))
        return spans
    if z in (37, 38) and x in (40, 50, 60):
        spans.append(("hall/sack", 1))
        return spans
    if x in (41, 51, 61) and z == 39:
        spans.append(("hall/cellar_lantern", 1))
        return spans
    return spans

