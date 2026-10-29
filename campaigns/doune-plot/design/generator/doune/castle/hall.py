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
    "hall/banner_n": "minecraft:red_wall_banner[facing=south]",
    "hall/banner_s": "minecraft:red_wall_banner[facing=north]",
    "hall/chandelier": "minecraft:lantern[hanging=true,waterlogged=false]",
    "hall/chain": "minecraft:iron_chain[axis=y,waterlogged=false]",
    "hall/cask": "minecraft:spruce_log[axis=z]",
    "hall/sack": "minecraft:hay_block[axis=y]",
    "hall/cellar_lantern": "minecraft:lantern[hanging=false,waterlogged=false]",
}
ANCHORS = {
    (58, F1 + 2, 39): ("stop-great-hall", None),   # ON the dais, beside the
                                                  # high table, not inside
                                                  # the great chair's step
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
        # the screens-end doorway through to the servery, which is how food
        # reaches this room: the servery's own east door opens on these cells
        servery_door = x <= x0 + 1 and 36 <= z <= 38
        hatch = x <= x0 + 1 and 38 <= z <= 40
        gh_door = x >= x1 - 1 and 38 <= z <= 40
        if cellar_door:
            c.add(None, 3)
            c.upto("wall", HALL_IN_TOP)
        elif west_door or gh_door or servery_door:
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
    """What stands on the hall floor, cell by cell from y16 up.

    Written as a map from course to block rather than as a running total: the
    canopy hangs at y21 whatever is under it, and a hall whose cloth of estate
    moves when somebody adds a lantern is a hall nobody can reason about.
    """
    hz0, hz1 = HALL_IN[2], HALL_IN[3]
    z0, z1 = HALL[2], HALL[3]
    cells = {}                                  # course offset from y16 -> role

    on_dais = x >= DAIS_X
    if on_dais:
        cells[0] = "hall/dais"                                   # the step up
        if x == HIGH_TABLE_X and 34 <= z <= 41:
            cells[1], cells[2] = "hall/table_leg", "hall/table_top"
            if z in (36, 39):
                cells[3] = "hall/lantern"
        if x in (DAIS_X + 1, DAIS_X + 2) and z in (37, 38):
            cells[1] = "hall/bench"                              # the great chair
        if 58 <= x <= 61 and 34 <= z <= 41:
            cells[5] = "hall/canopy"                             # cloth of estate
    elif HEARTH[0] <= x <= HEARTH[1] and HEARTH[2] <= z <= HEARTH[3]:
        centre = (x == 46 and z == 38)
        cells[0] = "hall/fire" if centre else "hall/hearth_kerb"
    elif SCREEN_X[0] <= x <= SCREEN_X[1]:
        if not 36 <= z <= 38:                                    # the two openings
            for c in range(0, 6):
                cells[c] = "hall/screen"
        cells[6] = "hall/gallery"                                # the gallery over it
    elif TABLE_RUN[0] <= x <= TABLE_RUN[1] and any(
            z in row for row in ((34, 35, 36), (41, 42, 43))):
        if z in (35, 42):
            cells[0], cells[1] = "hall/table_leg", "hall/table_top"
            if x in (44, 50):
                cells[2] = "hall/lantern"
        else:
            cells[0] = "hall/bench"
    elif x in (38, 39) and z in (32, 33):
        cells[0] = cells[1] = "hall/cupboard"                    # plate cupboard
    elif x == 35 and z in (34, 41):
        cells[0] = "hall/lantern"        # the strip behind the screen, else dark

    # light and hangings against the two long walls
    if z in (hz0, hz1):
        wall_torch = "hall/torch_n" if z == hz0 else "hall/torch_s"
        wall_banner = "hall/banner_n" if z == hz0 else "hall/banner_s"
        if x in TORCH_X:
            cells[3] = wall_torch
        if x in (42, 50, 56):
            cells[5] = cells[6] = wall_banner

    # two chandeliers on chains from the roof, over the body of the hall
    if x in (44, 54) and z == 38:
        # great_hall lays air up to `top - 2` and the roof on the two courses
        # above it, so the chain stops at `top - 2` or it comes out of the roof.
        top = HALL_IN_TOP + 1 + min(z - z0, z1 - z)              # this bay's ridge
        cells[8] = "hall/chandelier"                             # y24
        for c in range(9, (top - 2) - (WALK + 8) + 1):           # y25 .. top-2
            cells[c] = "hall/chain"

    if not cells:
        return []
    spans, run_role, run_len = [], None, 0
    for c in range(0, max(cells) + 1):
        role = cells.get(c)
        if role == run_role:
            run_len += 1
        else:
            if run_len:
                spans.append((run_role, run_len))
            run_role, run_len = role, 1
    spans.append((run_role, run_len))
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
    if x == 36 and z == 32:
        spans.append(("hall/cellar_lantern", 1))   # the west cellar's dark corner
        return spans
    return spans

