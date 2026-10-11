"""Act 2, the crossing: the flat, its mud fields, the way, the wrecks, the launch,
the pillars, the narrows, the skiff stage and the ferry houses with the skiff."""

import mapmodel as M
from kit import Piece, AIR, boxcells, ground, seam_box, INWARD
from blocks import S, stairs, slab, is_full
import arch
from common import (leftovers_no_body, space_claim, node_mark, station_mark, stations, wall_seams,
                    shell_box, roof, roof_no_body, chimney, lantern_post)
from places_town import rng, mix, walls, lid, windows, hang, COBBLE, STONE, MOSSY, CRACKED, PLANK, DARK, \
    LOG, DLOG, FENCE, DFENCE, PACKED, RUBBLE, SLATE, PANE, BARREL, rubble_fn

MUD = S("minecraft:mud")
WET = [(MUD, 7), (PACKED, 1), (S("minecraft:mud_bricks"), 0)]
MUDDY = [(MUD, 8), (S("minecraft:packed_mud"), 1)]
OLD_ROAD = [(S("minecraft:packed_mud"), 4), (COBBLE, 2), (S("minecraft:mossy_cobblestone"), 2), (STONE, 1),
            (S("minecraft:mud_bricks"), 2)]
WATER = S("minecraft:water", level=0)


def wet(r):
    return mix(r, [(MUD, 9), (PACKED, 1)])


def ledge_ring(pc, r, sides=("north", "south", "east", "west"), skip=()):
    """the place's ring a step down at the water's edge, so a swimmer climbs out
    onto it (one over the sea) and then up onto the place"""
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    fy = pc.dy
    cells = []
    if "north" in sides:
        cells += [(x, sz0 - 1) for x in range(sx0 - 1, sx1 + 2)]
    if "south" in sides:
        cells += [(x, sz1 + 1) for x in range(sx0 - 1, sx1 + 2)]
    if "west" in sides:
        cells += [(sx0 - 1, z) for z in range(sz0, sz1 + 1)]
    if "east" in sides:
        cells += [(sx1 + 1, z) for z in range(sz0, sz1 + 1)]
    for (x, z) in cells:
        if (x, fy - 1, z) in skip or not pc.owned((x, fy - 1, z)):
            continue
        pc.set(x, fy - 1, z, AIR)
        pc.set(x, fy - 2, z, mix(r, [(MUD, 3), (PACKED, 1)]))


def stake(pc, x, z, y=None, lamp=True):
    y = pc.dy if y is None else y
    pc.set(x, y, z, S("minecraft:spruce_fence"))
    pc.set(x, y + 1, z, S("minecraft:spruce_fence"))
    if lamp:
        pc.set(x, y + 2, z, arch.lantern(False))


def contact_cells(pc):
    out = set()
    for s in pc.seams:
        (x0, y0, z0), (x1, y1, z1) = s["cells"]
        out |= set(boxcells((x0, y0, z0), (x1, y1, z1)))
    return out


# ---------------------------------------------------------------------------
def mud_field(node):
    pc = Piece(node)
    r = rng(node)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    fy = pc.dy
    # a crust of wet mud one course over the sea water under it: it goes when the flat sinks
    for x in range(0, pc.X):
        for z in range(0, pc.Z):
            if pc.owned((x, fy - 1, z)):
                pc.set(x, fy - 1, z, mix(r, MUDDY))
    # a few old stakes and weed in the mud
    for x in range(sx0 + 3, sx1 - 2, 11):
        for z in range(sz0 + 4, sz1 - 3, 13):
            if r.random() < 0.35:
                pc.set(x, fy, z, S("minecraft:spruce_fence"))
            elif r.random() < 0.3:
                pc.set(x, fy, z, S("minecraft:dead_bush"))
    wall_seams(pc, "mud", fill=MUD)
    stations(pc)
    space_claim(pc, "mud", "open", cap=fy + 1)
    node_mark(pc)
    leftovers_no_body(pc, reason="the tops of old stakes in the mud")
    return pc.finish("mud", shown_faces=["north", "south", "east", "west"])


def pilgrims_way(node):
    pc = Piece(node)
    r = rng(node)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    fy = pc.dy
    ground(pc, lambda x, z: mix(r, OLD_ROAD), lambda x, z: mix(r, [(PACKED, 3), (S("minecraft:stone"), 1)]))
    built = wall_seams(pc, "way", fill=PACKED)
    # the shoulders: a step down either side, which the water reaches when the mud goes
    x0, z0, x1, z1 = shell_box(pc)
    for z in range(sz0 + 2, sz1 + 1):
        for x in (x0, x1):
            if pc.owned((x, fy - 1, z)):
                pc.set(x, fy - 1, z, AIR)
                pc.set(x, fy - 2, z, mix(r, [(MUD, 2), (COBBLE, 1)]))
    # the marker stakes along its east edge
    for z in range(sz0 + 4, sz1 + 1, 9):
        stake(pc, sx1, z)
    stations(pc)
    space_claim(pc, "way", "open", cap=fy + 2)
    node_mark(pc)
    leftovers_no_body(pc, reason="the tops of the marker stakes")
    return pc.finish("way", shown_faces=["north", "south", "east", "west"])


def hull(pc, r, x0, z0, L, W, axis, lean, broken=0):
    """an old hull lying on its side in the mud: a curved shell of planks and ribs"""
    fy = pc.dy
    for i in range(L):
        t = i / max(1, L - 1)
        w = max(1, int(W * (1 - (2 * t - 1) ** 4) + 0.5))
        for j in range(w):
            h = 1 + (j * lean) // max(1, w)
            for y in range(fy, fy + h + 1):
                c = (x0 + i, y, z0 + j) if axis == "x" else (x0 + j, y, z0 + i)
                if broken and (i % broken == 0) and y == fy + h:
                    continue
                edge = j in (0, w - 1) or y == fy + h
                if not edge:
                    # silted up to its gunwales: the mud fills the hull
                    pc.set(*c, MUD)
                    continue
                b = S("minecraft:dark_oak_log", axis="y") if (i % 4 == 0 and y < fy + h) else mix(r, [(DARK, 3), (PLANK, 2), (S("minecraft:stripped_dark_oak_log", axis=axis), 1)])
                pc.set(*c, b)


def wreck_field(node):
    pc = Piece(node)
    r = rng(node)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    fy = pc.dy
    ground(pc, lambda x, z: mix(r, WET), lambda x, z: PACKED)
    wall_seams(pc, "field", fill=PACKED)
    # the way across the field, its stakes
    wx0, wx1 = 172 - pc.wmin[0], 174 - pc.wmin[0]
    for z in range(sz0, sz1 + 1):
        for x in range(wx0 - 1, wx1 + 2):
            pc.set(x, fy - 1, z, mix(r, OLD_ROAD))
    for z in range(sz0 + 3, sz1, 9):
        stake(pc, wx1 + 1, z)
    # the wrecks, either side of the way
    for (x, z, L, W, axis, lean) in [(sx0 + 6, sz0 + 6, 16, 6, "x", 3), (sx0 + 30, sz0 + 18, 14, 5, "x", 2),
                                     (wx1 + 8, sz0 + 4, 18, 6, "x", 3), (wx1 + 34, sz0 + 20, 15, 6, "x", 2),
                                     (wx1 + 14, sz0 + 26, 12, 5, "z", 2), (sx0 + 12, sz0 + 24, 12, 5, "z", 3)]:
        hull(pc, r, x, z, L, W, axis, lean, broken=5)
    ledge_ring(pc, r, sides=("west", "east"))
    stations(pc)
    space_claim(pc, "field", "open", cap=fy + 1)
    node_mark(pc)
    leftovers_no_body(pc, reason="the wrecks' sides and the tops of the stakes")
    return pc.finish("field", shown_faces=["north", "south", "east", "west"])


def carved_pillars(node):
    pc = Piece(node)
    r = rng(node)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    fy = pc.dy
    ground(pc, lambda x, z: mix(r, WET), lambda x, z: PACKED)
    wall_seams(pc, "road", fill=PACKED)
    wx0, wx1 = 172 - pc.wmin[0], 174 - pc.wmin[0]
    for z in range(sz0, sz1 + 1):
        for x in range(wx0 - 1, wx1 + 2):
            pc.set(x, fy - 1, z, mix(r, OLD_ROAD))
    # the standing pillars of the old road, both sides, carved with the Rubbing's pictures
    sx_, sz_, _ = None, None, None
    script = pc.L(*M.STATIONS["anchor/pillar-script"][:3])
    carve = [S("minecraft:chiseled_stone_bricks"), S("minecraft:chiseled_tuff"), S("minecraft:chiseled_tuff_bricks"),
             S("minecraft:polished_tuff"), S("minecraft:tuff_bricks"), S("minecraft:cracked_stone_bricks")]
    for z in range(sz0 + 13, sz1 - 1, 7):
        for x in (wx0 - 4, wx1 + 4):
            h = 6 + (z * 3 + x) % 4
            for y in range(fy, fy + h):
                pc.set(x, y, z, carve[(y + z + x) % len(carve)] if y > fy else S("minecraft:tuff_bricks"))
                if y in (fy + 2, fy + 4):
                    pc.set(x, y, z, S("minecraft:chiseled_stone_bricks"))
            pc.set(x, fy + h, z, slab("tuff_brick", "bottom"))
    # the script at the foot of the pillar by the station: the station cell stays clear
    sxx, syy, szz = script
    for y in range(fy, fy + 7):
        pc.set(sxx - 1, y, szz, carve[y % len(carve)] if y > fy else S("minecraft:tuff_bricks"))
    for z in range(sz0 + 2, sz1, 9):
        stake(pc, wx1 + 1, z)
    stations(pc)
    space_claim(pc, "road", "open", cap=fy + 1)
    node_mark(pc)
    leftovers_no_body(pc, reason="the tops of the pillars and stakes")
    return pc.finish("road", shown_faces=["north", "south", "east", "west"])


def marracks_launch(node):
    pc = Piece(node)
    r = rng(node)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    fy = pc.dy
    ground(pc, lambda x, z: mix(r, WET), lambda x, z: PACKED)
    wall_seams(pc, "camp", fill=PACKED)
    # the grounded salvage launch, bow north, about 20 by 6, its deckhouse aft
    hx0, hz0 = 155 - pc.wmin[0], 301 - pc.wmin[2]
    L, W = 20, 6
    for i in range(L):
        bow = max(0, 3 - i)
        for j in range(W):
            if j < bow // 2 or j > W - 1 - bow // 2:
                continue
            x, z = hx0 + j, hz0 + i
            pc.set(x, fy, z, S("minecraft:dark_oak_log", axis="z") if j == W // 2 else DARK)
            side = j in (bow // 2, W - 1 - bow // 2) or i == 0 or i == L - 1
            pc.set(x, fy + 1, z, DARK if side else PLANK)
            pc.set(x, fy + 2, z, DFENCE if side else AIR)
    for i in range(L - 6, L - 1):
        for j in range(1, W - 1):
            for y in range(fy + 2, fy + 5):
                if j in (1, W - 2) or i in (L - 6, L - 2):
                    pc.set(hx0 + j, y, hz0 + i, PLANK if y < fy + 4 else DARK)
            pc.set(hx0 + j, fy + 5, hz0 + i, slab("dark_oak", "bottom"))
    pc.set(hx0 + 2, fy + 2, hz0 + L - 6, AIR)
    pc.set(hx0 + 2, fy + 3, hz0 + L - 6, AIR)
    # the mast, rising through the platform
    mx, mz = 157 - pc.wmin[0], 304 - pc.wmin[2]
    for y in range(fy + 1, pc.Y):
        pc.set(mx, y, mz, S("minecraft:spruce_log", axis="y"))
    # lanterns hung from the rail
    for i in (2, 8, 13):
        pc.set(hx0 - 1 if i % 2 else hx0 + W, fy + 2, hz0 + i, arch.lantern(False))
    # the stair up to the mast platform (through its floor)
    for s in pc.seams:
        if s["face"] == "up":
            (ax, ay, az), (bx, by, bz) = s["cells"]
            top = ay
            zs = range(min(az, bz), max(az, bz) + 1)
            treads = {ax - k: top - k for k in range(0, top - fy + 1)}
            for x, ty in treads.items():
                for z in zs:
                    pc.set(x, ty, z, stairs("spruce", "east"))
                    for yy in range(fy, ty):
                        pc.set(x, yy, z, S("minecraft:spruce_fence") if (x % 3 == 0 and yy < ty - 1) else AIR)
                    for yy in range(ty + 1, min(ty + 4, sy1 + 1)):
                        pc.set(x, yy, z, AIR)
                    if ty - 1 >= fy:
                        pc.set(x, ty - 1, z, S("minecraft:spruce_planks")) if False else None
            opening, landing, flight = [], [], []
            for x, ty in treads.items():
                for z in zs:
                    if ty == top:
                        opening.append((x, ty, z))
                    elif ty == top - 1:
                        landing += [(x, ty, z), (x, top, z)]
                    elif ty == top - 2:
                        landing += [(x, ty, z), (x, top - 1, z), (x, top, z)]
                    elif ty >= fy + 1:
                        flight += [(x, yy, z) for yy in range(ty, min(ty + 4, sy1 + 1))]
            # the cells under the stair are left to the mud: its posts stand there
            pc.claim(opening, "door-launch-to-mast")
            pc.claim(landing, "landing-launch-to-mast")
            pc.claim([c for c in flight if c not in landing], "flight-launch-to-mast")
            pc.space_decl("landing-launch-to-mast", "open")
            pc.edge(a="camp", b="landing-launch-to-mast", **{"class": "stair"}, rise=(top - 2) - fy,
                    via="flight-launch-to-mast")
            pc.edge(a="landing-launch-to-mast", b="exterior", **{"class": "stair"}, rise=0,
                    via="door-launch-to-mast")
    stations(pc)
    space_claim(pc, "camp", "open", cap=fy + 1)
    node_mark(pc)
    leftovers_no_body(pc, reason="the launch's deck and deckhouse, and the space under the stair")
    return pc.finish("camp", shown_faces=["north", "south", "east", "west", "up"])


def mast_platform(node):
    pc = Piece(node)
    r = rng(node)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    fy = pc.dy
    for x in range(0, pc.X):
        for z in range(0, pc.Z):
            pc.set(x, fy - 1, z, PLANK)
    for x in range(sx0 - 1, sx1 + 2):
        for z in (sz0 - 1, sz1 + 1):
            pc.set(x, fy, z, FENCE)
    for z in range(sz0, sz1 + 1):
        pc.set(sx0 - 1, fy, z, FENCE)
    # the hole the stair comes up through, and the well the climber's head passes
    for s in pc.seams:
        if s["face"] == "down":
            (ax, ay, az), (bx, by, bz) = s["cells"]
            cells = list(boxcells((ax, ay, az), (bx, by, bz)))
            well = [(x - 1, y, z) for (x, y, z) in cells]
            for c in cells + well:
                pc.set(*c, AIR)
            pc.claim(cells, "door-launch-to-mast")
            pc.claim(well, "deck")
            pc.edge(a="deck", b="exterior", **{"class": "walk"}, via="door-launch-to-mast")
    mx, mz = pc.L(157, 0, 304)[0], pc.L(157, 0, 304)[2]
    for y in range(fy - 1, pc.Y):
        pc.set(mx, y, mz, S("minecraft:spruce_log", axis="y"))
    pc.set(mx, fy + 2, mz - 1, arch.lantern(True)) if False else None
    stations(pc)
    space_claim(pc, "deck", "open")
    node_mark(pc)
    leftovers_no_body(pc, reason="the rail and the masthead")
    return pc.finish("deck", shown_faces=["north", "south", "east", "west"])


def narrows(node):
    pc = Piece(node)
    r = rng(node)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    fy = pc.dy
    ground(pc, lambda x, z: mix(r, OLD_ROAD), lambda x, z: PACKED)
    wall_seams(pc, "ridge", fill=PACKED)
    # the east side is open water: a step down there to climb out onto
    x0, z0, x1, z1 = shell_box(pc)
    shelf = set()
    for s in pc.seams:
        if s["edge"] == "edge/narrows-to-shelf":
            (a0, _, b0), (a1, _, b1) = s["cells"]
            shelf = {(a0, z) for z in range(min(b0, b1), max(b0, b1) + 1)}
    for z in range(sz0, sz1 + 1):
        if (x1, z) not in shelf:
            pc.set(x1, fy - 1, z, AIR)
            pc.set(x1, fy - 2, z, MUD)
    for z in range(sz0 + 3, sz1 + 1, 8):
        stake(pc, sx1, z)
    stations(pc)
    space_claim(pc, "ridge", "open", cap=fy + 2)
    node_mark(pc)
    leftovers_no_body(pc, reason="the tops of the marker stakes")
    return pc.finish("ridge", shown_faces=["north", "south", "east", "west"])


def narrows_shelf(node):
    pc = Piece(node)
    r = rng(node)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    fy = pc.dy
    ground(pc, lambda x, z: mix(r, WET), lambda x, z: PACKED)
    wall_seams(pc, "shelf", fill=PACKED)
    # the pit the tentacle stands in: a hole full of black water, a step down
    px, py, pz = pc.L(*M.STATIONS["anchor/narrows-pit"][:3])
    for x in range(px - 2, px + 3):
        for z in range(pz - 2, pz + 3):
            if abs(x - px) + abs(z - pz) <= 3:
                pc.set(x, fy - 1, z, WATER)
                pc.set(x, fy - 2, z, MUD)
    ledge_ring(pc, r, sides=("north", "south", "east"))
    stations(pc)
    pc.set(px, py, pz, AIR)
    space_claim(pc, "shelf", "open", cap=fy + 1)
    node_mark(pc)
    leftovers_no_body(pc)
    return pc.finish("shelf", shown_faces=["north", "south", "east", "west"])


def skiff_stage(node):
    pc = Piece(node)
    r = rng(node)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    fy = pc.dy
    ground(pc, lambda x, z: mix(r, [(STONE, 4), (MOSSY, 2), (CRACKED, 1)]), lambda x, z: mix(r, [(STONE, 3), (COBBLE, 1)]))
    wall_seams(pc, "stage", fill=STONE)
    ledge_ring(pc, r, sides=("east", "west", "south"))
    for (x, z) in [(sx0, sz1), (sx1, sz1)]:
        lantern_post(pc, x, z)
    stations(pc)
    space_claim(pc, "stage", "open", cap=fy + 2)
    node_mark(pc)
    leftovers_no_body(pc)
    return pc.finish("stage", shown_faces=["north", "south", "east", "west"])


# -- the skiff and the ferry houses ------------------------------------------
def skiff(pc, x0, z0, deck_y, hull=True):
    """Marrack's skiff, 5 in beam (x0..x0+4) and 10 long (z0..z0+9), bow north:
    a stem post and a flat transom, the sheer rising toward the bow, a gunwale
    rail, a thwart for the oarsman and one for passengers, an oar out over the
    water, the tiller head on the rudder post at the stern. `deck_y` is the
    course the floor boards lie in; the party stands one above it."""
    W, L = 5, 10
    for i in range(L):
        for j in range(W):
            x, z = x0 + j, z0 + i
            bow = i == 0
            stern = i == L - 1
            side = j in (0, W - 1)
            if hull:
                pc.set(x, deck_y - 1, z, DARK if (side or bow or stern) else S("minecraft:dark_oak_log", axis="z"))
            if bow and j != W // 2:
                pc.set(x, deck_y, z, DARK)
                pc.set(x, deck_y + 1, z, stairs("dark_oak", "north" if False else "south", "top") if False else DFENCE)
                continue
            pc.set(x, deck_y, z, PLANK)
            if side:
                gap = (j == 0 and i in (5, 6))      # where the party steps aboard from the quay
                pc.set(x, deck_y + 1, z, AIR if gap else DFENCE)
            if stern and not side:
                pc.set(x, deck_y + 1, z, DFENCE if j != W // 2 else AIR)
    # the stem post at the bow
    pc.set(x0 + W // 2, deck_y, z0, S("minecraft:dark_oak_log", axis="y"))
    pc.set(x0 + W // 2, deck_y + 1, z0, DFENCE)
    pc.set(x0 + W // 2, deck_y + 2, z0, DFENCE)
    # the thwarts across the beam: the oarsman's, forward, and the passengers'
    for j in range(1, W - 1):
        pc.set(x0 + j, deck_y + 1, z0 + 1, slab("spruce", "bottom")) if j != W // 2 else None
        pc.set(x0 + j, deck_y + 1, z0 + 7, slab("spruce", "bottom"))
    # the thwarts: the oarsman's forward (where Marrack sits, outside the seat
    # row), the passengers' aft
    # the oar out over the water on the far side from the quay
    pc.set(x0 + W, deck_y + 1, z0 + 1, S("minecraft:spruce_fence"))
    # the tiller head on the rudder post at the transom: the block the party uses
    pc.set(x0 + W // 2, deck_y + 1, z0 + L - 1, S("minecraft:spruce_fence"))


def ferry_house(node, door_face):
    pc = Piece(node)
    r = rng(node)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    fy = pc.dy
    x0, z0, x1, z1 = shell_box(pc)
    lid_y = pc.roof["lid_y"]
    # walls carried down to the sea floor, all round; the water gate shut
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            edge = x in (x0, x1) or z in (z0, z1)
            for y in range(0, lid_y):
                if edge:
                    pc.set(x, y, z, mix(r, RUBBLE) if y >= fy - 3 else mix(r, [(STONE, 2), (MOSSY, 2), (S("minecraft:prismarine_bricks"), 0), (COBBLE, 1)]))
                elif y < fy - 5:
                    pc.set(x, y, z, STONE)
    lid(pc, PLANK)
    roof(pc, "gable", "z", SLATE, mix(r, RUBBLE))
    # the quay along the west side, the slip of sea water to the east
    qx1 = sx0 + 5
    for x in range(sx0, sx1 + 1):
        for z in range(sz0, sz1 + 1):
            for y in range(fy - 5, fy):
                if x <= qx1:
                    pc.set(x, y, z, STONE if y < fy - 1 else mix(r, [(STONE, 3), (MOSSY, 1)]))
                else:
                    pc.set(x, y, z, WATER if y <= fy - 2 else AIR)
    # the skiff, at the same place in both houses
    skx, skz = sx0 + 6, sz0 + 3
    skiff(pc, skx, skz, fy - 1)
    # the water under and round the skiff stays water; above the sea it is air
    # the passage from the land door turns behind a screen before the slip
    built = wall_seams(pc, "quay", fill=STONE, threshold=STONE)
    door = [c for b in built.values() for c in b["cells"]]
    dx = door[0][0]
    inward = 1 if door_face == "north" else -1
    dz = door[0][2]
    screen_z = dz + 3 * inward
    for x in range(sx0, qx1 + 1):
        for y in range(fy, lid_y):
            if x != sx0:
                pc.set(x, y, screen_z, PLANK)
    # Marrack's lanterns hung from the beams
    for (x, z) in [(sx0 + 1, sz0 + 5), (sx0 + 1, sz1 - 3), (skx + 2, sz0 + 6), (sx1, sz1 - 1),
                   (sx1 - 1, sz0 + 1), (sx1 - 2, sz1 - 1)]:
        if pc.get(x, lid_y - 1, z) == AIR and (x, lid_y - 1, z) not in pc.prog.region:
            pc.set(x, lid_y - 1, z, arch.lantern(True))
    for st in M.P[node]["stations"]:
        station_mark(pc, st["anchor"], clear=not st["anchor"].endswith("tiller"))
    # the spaces: the quay and the skiff are one floor, at the walk plane
    space_claim(pc, "quay", "enclosed", box=((sx0, fy - 1, sz0), (sx1, sy1, sz1)))
    node_mark(pc)
    roof_no_body(pc)
    leftovers_no_body(pc)
    return pc.finish("quay", shown_faces=["north", "south", "east", "west", "up"])


def near_ferry_house(node):
    return ferry_house(node, "north")


def far_ferry_house(node):
    return ferry_house(node, "south")


def sea_skiff(node):
    pc = Piece(node)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = pc.space
    fy = pc.dy
    skiff(pc, sx0, sz0, fy - 1, hull=False)
    station_mark(pc, "anchor/sea-skiff")
    space_claim(pc, "skiff", "open", cap=fy + 2)
    node_mark(pc)
    leftovers_no_body(pc)
    return pc.finish("skiff", shown_faces=["north", "south", "east", "west"])


BUILDERS = {
    "node/mud-wrecks-west": mud_field,
    "node/mud-wrecks-east": mud_field,
    "node/mud-pillars-west": mud_field,
    "node/mud-pillars-east": mud_field,
    "node/mud-narrows-west": mud_field,
    "node/pilgrims-way": pilgrims_way,
    "node/wreck-field": wreck_field,
    "node/carved-pillars": carved_pillars,
    "node/marracks-launch": marracks_launch,
    "node/mast-platform": mast_platform,
    "node/narrows": narrows,
    "node/narrows-shelf": narrows_shelf,
    "node/skiff-stage": skiff_stage,
    "node/near-ferry-house": near_ferry_house,
    "node/far-ferry-house": far_ferry_house,
    "node/sea-skiff": sea_skiff,
}
