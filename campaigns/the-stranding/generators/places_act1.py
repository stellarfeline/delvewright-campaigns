"""Act 1 — Wrackham: the detail builders of the town's places.

Run from the campaign directory or anywhere:
    python3 generators/places_act1.py "$(command -v delvec)" "$DELVEWRIGHT_PREFABS" [stem ...]
writes programs/<stem>.json for each place named (default: all of this act's).
Every frame, seam and owed name comes from `delvec allocation`; each builder
states only the building. Local x runs east, y up from the floor course,
z south. A place's outer walls are the whole's (the blockout shell outside the
frame); a room's own walls stand inside its frame.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import *  # noqa: F401,F403
import kit

# ---- the town's materials (measured: block-appearance.py; GENERATION.md round 7) ----
TOWN_STONE = [{"weight": 6, "block": "minecraft:stone_bricks"},
              {"weight": 2, "block": "minecraft:mossy_stone_bricks"},
              {"weight": 2, "block": "minecraft:cracked_stone_bricks"}]
RUBBLE = [{"weight": 4, "block": "minecraft:cobblestone"},
          {"weight": 2, "block": "minecraft:mossy_cobblestone"},
          {"weight": 3, "block": "minecraft:andesite"},
          {"weight": 1, "block": "minecraft:tuff"}]
SETTS = [{"weight": 5, "block": "minecraft:polished_andesite"},
         {"weight": 3, "block": "minecraft:andesite"},
         {"weight": 2, "block": "minecraft:stone"},
         {"weight": 1, "block": "minecraft:cobblestone"}]
COBBLES = [{"weight": 5, "block": "minecraft:cobblestone"},
           {"weight": 2, "block": "minecraft:mossy_cobblestone"},
           {"weight": 2, "block": "minecraft:tuff"},
           {"weight": 1, "block": "minecraft:andesite"}]
PLASTER = [{"weight": 6, "block": "minecraft:calcite"},
           {"weight": 1, "block": "minecraft:diorite"}]
BOARDS = [{"weight": 4, "block": "minecraft:spruce_planks"},
          {"weight": 1, "block": "minecraft:dark_oak_planks"}]
FLAGS = [{"weight": 4, "block": "minecraft:stone_bricks"},
         {"weight": 2, "block": "minecraft:polished_andesite"},
         {"weight": 1, "block": "minecraft:cracked_stone_bricks"}]
MUD = [{"weight": 7, "block": "minecraft:mud"}, {"weight": 1, "block": "minecraft:muddy_mangrove_roots[axis=y]"},
       {"weight": 1, "block": "minecraft:gray_terracotta"}, {"weight": 1, "block": "minecraft:black_terracotta"}]
GRASSY = [{"weight": 5, "block": "minecraft:grass_block[snowy=false]"},
          {"weight": 2, "block": "minecraft:coarse_dirt"},
          {"weight": 1, "block": "minecraft:podzol[snowy=false]"}]
WEED = [{"weight": 6, "block": "minecraft:air"}, {"weight": 2, "block": "minecraft:short_grass"},
        {"weight": 1, "block": "minecraft:fern"}]

SLATE = "deepslate_tile"


# ---- shared pieces of building ----------------------------------------------
def room_shell(p, floor, wall, ceil, ceil_y=None, base=None, posts=None):
    """A room's own floor, four walls standing on the frame's boundary, and a ceiling."""
    W, L = p.W, p.L
    cy = p.H - 1 if ceil_y is None else ceil_y
    p.box(0, 0, 0, W - 1, 0, L - 1, floor)
    if ceil is not None:
        p.box(0, cy, 0, W - 1, cy, L - 1, ceil)
    for x in range(W):
        for z in range(L):
            if x in (0, W - 1) or z in (0, L - 1):
                for y in range(1, cy):
                    p.put(x, y, z, base if (base is not None and y == 1) else wall)
    if posts:
        for (x, z) in ((0, 0), (W - 1, 0), (0, L - 1), (W - 1, L - 1)):
            for y in range(1, cy):
                p.put(x, y, z, posts)


def hang(p, x, y, z, soul=False):
    """A lantern hung on a chain from the block above y."""
    p.put(x, y, z, SOUL_HANG if soul else LANTERN_HANG, struct=False)
    yy = y + 1
    while p.inb(x, yy, z) and p.get(x, yy, z) is None:
        yy += 1
    if p.inb(x, yy, z):                      # chained to the first thing above it
        for c in range(y + 1, yy):
            p.put(x, c, z, chain(), struct=False)


def lamp_post(p, x, z, h=3, wood="spruce", y0=1):
    for y in range(y0, y0 + h):
        p.put(x, y, z, fence(wood))
    p.put(x, y0 + h, z, LANTERN)


def wall_lamp(p, x, y, z, toward):
    """A bracket lamp on a wall: an arm of fence reaching out from the wall at `toward`,
    the lantern hung under it."""
    dx, dz = FACE_DIRS[toward]
    p.put(x, y, z, fence("spruce", n=toward == "north", s=toward == "south",
                         e=toward == "east", w=toward == "west"))
    p.put(x, y - 1, z, LANTERN_HANG, struct=False)


def flight(p, xs, zs, top, bottom, mat, fill, axis="z", via=None):
    """A straight flight along z (or x) over the run cells `zs` (ordered from the top end to
    the bottom end), across the columns `xs`, from standing level `top` down to `bottom`.
    Each tread is a stair facing up the flight; the body of the flight under it is `fill`;
    headroom over every tread is cleared."""
    n = len(zs)
    up = None
    if axis == "z":
        up = "north" if zs[0] < zs[-1] else "south"
    else:
        up = "west" if zs[0] < zs[-1] else "east"
    drop = top - bottom
    if n + 1 < drop:
        raise ValueError(f"{p.stem}: a flight of {n} treads cannot fall {drop} courses one at a time")
    for i, r in enumerate(zs):
        lvl = top - round((i + 1) * drop / (n + 1)) if n else bottom
        lvl = max(bottom, lvl)
        for c in xs:
            x, z = (c, r) if axis == "z" else (r, c)
            for y in range(0, lvl - 1):
                p.put(x, y, z, fill)
            if lvl - 1 >= 1 or lvl - 1 == 0:
                p.put(x, lvl - 1, z, stair(mat, up) if lvl > bottom else fill)
            for y in range(lvl, min(p.H - 1, lvl + 3)):
                if p.get(x, y, z) is not None and (x, y, z) in p.struct:
                    p.put(x, y, z, None)
            if via:
                for y in (lvl, lvl + 1):
                    if p.inb(x, y, z) and passable(p.get(x, y, z)):
                        p.cl[(x, y, z)] = via
    return up


def stair_head(p, name, x0, z0, x1, z1, level, envelope, fill, top=None):
    """The landing at a flight's top, as its own space: floor at `level`, air claimed up to
    `top` (default: the frame's top course for an open place, under the ceiling otherwise)."""
    landing(p, x0, z0, x1, z1, level, fill)
    t = top if top is not None else p.H - 1
    p.claim(name, x0, level, z0, x1, t, z1, envelope=envelope)


def landing(p, x0, z0, x1, z1, level, fill):
    for x in range(min(x0, x1), max(x0, x1) + 1):
        for z in range(min(z0, z1), max(z0, z1) + 1):
            for y in range(0, level):
                p.put(x, y, z, fill)
            for y in range(level, min(p.H - 1, level + 3)):
                if (x, y, z) in p.struct:
                    p.put(x, y, z, None)


def house_front(p, side, z0, z1, doors=(), windows=(), stone=None, open_doors=()):
    """A row of cottage fronts on the west (x=0) or east (x=W-1) edge of a street: four
    courses of stone, an eave course and a slate roof course; doors, windows and bracket
    lamps. `doors` are z positions of shut doors, `open_doors` of open doorways."""
    x = 0 if side == "west" else p.W - 1
    inward = "east" if side == "west" else "west"
    face = "west" if side == "west" else "east"   # the door's back is to the wall's outer side
    for z in range(z0, z1 + 1):
        for y in range(1, 5):
            p.put(x, y, z, stone)
        p.put(x, 5, z, stair(SLATE, face, "top"))
        p.put(x, 6, z, stair(SLATE, face))
    for z in range(z0, z1 + 1, 6):
        for y in range(1, 5):
            p.put(x, y, z, log("stripped_spruce_log"))   # the party walls between houses
    for z in doors:
        p.put(x, 1, z, f"minecraft:spruce_door[facing={inward},half=lower,hinge=left,open=false,powered=false]")
        p.put(x, 2, z, f"minecraft:spruce_door[facing={inward},half=upper,hinge=left,open=false,powered=false]")
        p.put(x, 3, z, stone)
    for z in open_doors:
        p.put(x, 1, z, None, struct=False)
        p.put(x, 2, z, None, struct=False)
        p.put(x, 3, z, log("dark_oak_log", "z"))
    for (z, y) in windows:
        p.put(x, y, z, pane("glass_pane", n=True, s=True))



# ---- the town's craft: the roof's underside over a room, fronts with depth on a street ------
def pitched(p, lo, hi, b0, b1, eave_y, along="z", stair_mat="spruce", board="minecraft:spruce_planks",
            beams_every=4):
    """The underside of a pitched roof over a room. The ridge runs `along` z (or x); across it,
    from `lo` to `hi`, the ceiling rises one course a cell from the eaves (`eave_y`) toward the
    ridge; its surface is upside-down stairs under roof boards; tie beams cross the room at the
    eaves every `beams_every` cells along the ridge. Every surface over a body faces down."""
    H = p.H
    for a in range(lo, hi + 1):
        d = min(a - lo, hi - a)
        c = eave_y + d
        if c >= H - 1:
            continue
        if a - lo < hi - a:
            f = "west" if along == "z" else "north"
        elif a - lo > hi - a:
            f = "east" if along == "z" else "south"
        else:
            f = None
        for b in range(b0, b1 + 1):
            x, z = (a, b) if along == "z" else (b, a)
            for y in range(c + 1, H):
                p.put(x, y, z, board)
            if f and p.get(x, c, z) is None:
                p.put(x, c, z, stair(stair_mat, f, "top"))
    if beams_every:
        for b in range(b0 + 1, b1, beams_every):
            for a in range(lo, hi + 1):
                x, z = (a, b) if along == "z" else (b, a)
                if p.get(x, eave_y, z) is None or "stairs" in str(p.get(x, eave_y, z)):
                    p.put(x, eave_y, z, log("dark_oak_log", "x" if along == "z" else "z"))


WALLMAT = {"stone": "minecraft:stone_bricks", "limewash": "minecraft:calcite",
           "brick": "minecraft:bricks", "rubble": "minecraft:cobblestone"}


def street_house(p, side, a0, a1, kind, door=None, windows=(), chimney=None, hood=True):
    """One cottage front on a street's edge (`side`: the frame edge it stands on), from `a0`
    to `a1` along that edge: a plinth course, the wall (stone, rubble, brick, or limewash in a
    dark timber frame), windows with a sill under and a lintel over, a door between jambs with
    a slate hood over it on the street side, the eaves and the slate roof course, a chimney
    stack at a party wall."""
    W, L = p.W, p.L
    inward = OPP[side]
    def cell(a, d=0):            # a along the edge, d cells in from it
        return {"west": (d, a), "east": (W - 1 - d, a), "north": (a, d), "south": (a, L - 1 - d)}[side]
    along_x = side in ("north", "south")
    def put(a, y, b, d=0):
        x, z = cell(a, d); p.put(x, y, z, b)
    wallmat = WALLMAT[kind]
    lo_dir, hi_dir = ("west", "east") if along_x else ("north", "south")
    for a in range(a0, a1 + 1):
        put(a, 1, "minecraft:polished_andesite")
        for y in range(2, 5):
            put(a, y, wallmat)
        put(a, 5, stair(SLATE, side, "top"))
        put(a, 6, stair(SLATE, side))
    if kind == "limewash":
        for a in (a0, a1):
            for y in range(1, 5):
                put(a, y, log("dark_oak_log"))
        for a in range(a0, a1 + 1):
            put(a, 4, log("dark_oak_log", "x" if along_x else "z"))
    else:
        for a in (a0, a1):
            for y in range(2, 5):
                put(a, y, "minecraft:stone_bricks" if kind != "stone" else "minecraft:polished_andesite")
    for (a, y) in windows:
        put(a, y, pane("glass_pane", e=along_x, w=along_x, n=not along_x, s=not along_x))
        if kind == "limewash":
            put(a, y - 1, log("dark_oak_log", "x" if along_x else "z"))
        else:
            put(a, y - 1, "minecraft:smooth_stone"); put(a, y + 1, "minecraft:polished_andesite")
    if door is not None:
        put(door, 1, f"minecraft:spruce_door[facing={inward},half=lower,hinge=left,open=false,powered=false]")
        put(door, 2, f"minecraft:spruce_door[facing={inward},half=upper,hinge=left,open=false,powered=false]")
        for sa in (door - 1, door + 1):
            if a0 <= sa <= a1:
                for y in (1, 2, 3):
                    put(sa, y, log("stripped_spruce_log"))
        put(door, 3, log("stripped_spruce_log", "x" if along_x else "z"))
        if hood:
            put(door, 3, slab(SLATE, "top"), d=1)
    if chimney is not None:
        for y in (5, 6):
            put(chimney, y, "minecraft:bricks")


# =============================================================================
def coach_road():
    """The cliff-top coach road: a cart road of setts between a rock bank on the north and a
    drystone parapet on the south over the drop to the town; the coach stop's shelter with
    its bench, the notice post in front of it, a milestone, lamp posts along both sides."""
    p = Place("coach-road", envelope="open")
    W, H, L = p.W, p.H, p.L
    setts = p.role("setts", SETTS)
    rubble = p.role("rubble", RUBBLE)
    grass = p.role("verge", GRASSY)
    p.box(0, 0, 0, W - 1, 0, L - 1, setts)
    for x in range(W):
        p.put(x, 0, 0, grass); p.put(x, 0, 1, grass)
        p.put(x, 0, L - 1, rubble)
    # the rock bank on the north: rubble rising behind the verge, grass on its top
    for x in range(W):
        h = 3 + (x * 7 % 3)
        for y in range(1, h + 1):
            p.put(x, y, 0, rubble)
        p.put(x, h + 1, 0, "minecraft:grass_block[snowy=false]")
        if x % 5 == 2:
            p.put(x, 1, 1, rubble)
    s = p.seam("coach-to-steps"); lo, hi = p.seam_box(s)
    # the parapet on the south, a drystone wall broken by the head of the steps
    for x in range(W):
        if lo[0] - 1 <= x <= hi[0] + 1:
            continue
        p.put(x, 1, L - 1, wall("cobblestone", e="low", w="low"))
    for x in (lo[0] - 1, hi[0] + 1):
        p.put(x, 1, L - 1, "minecraft:chiseled_stone_bricks")
        p.put(x, 2, L - 1, "minecraft:chiseled_stone_bricks")
        p.put(x, 3, L - 1, LANTERN)
    # the ends: the road turns away behind a field wall
    for z in range(1, L - 1):
        for x in (0, W - 1):
            p.put(x, 1, z, wall("mossy_cobblestone", n="low", s="low"))
    # the coach stop: a timber shelter against the bank, a bench under it
    cx = 22
    for x in range(cx - 4, cx + 3):
        for y in range(1, 4):
            p.put(x, y, 1, "minecraft:spruce_planks")
        p.put(x, 4, 1, slab("spruce"))
        p.put(x, 4, 2, slab("spruce"))
    for x in (cx - 4, cx + 2):
        for y in range(1, 4):
            p.put(x, y, 2, log("spruce_log"))
    for x in range(cx - 3, cx + 2):
        p.put(x, 1, 2, stair("spruce", "north"))
    # a milestone, lamp posts on both sides of the road
    p.put(8, 1, 2, "minecraft:chiseled_stone_bricks")
    for x in (5, 14, 33, 42):
        lamp_post(p, x, L - 2, 2)
    for x in (1, 10, 29, 38, 46):
        lamp_post(p, x, 2, 2)
    p.cut_seams(floor=setts)
    p.mark("coach-stop", (cx, 1, 3), "south")
    p.mark("node-coach-road", (cx + 1, 1, 4), "south")
    p.mark("spawn", (cx + 1, 1, 4), "south")
    return p


def cliff_steps():
    """The covered steps down the cliff: a narrow stone stair under a timber roof, from a
    landing at the coach road down to the high street; lanterns hung from the beams."""
    p = Place("cliff-steps", envelope="enclosed")
    W, H, L = p.W, p.H, p.L
    stone = p.role("stone", TOWN_STONE)
    rubble = p.role("rubble", RUBBLE)
    top = p.seam("coach-to-steps"); bot = p.seam("steps-to-street")
    tlo, thi = p.seam_box(top); blo, bhi = p.seam_box(bot)
    p.box(0, 0, 0, W - 1, 0, L - 1, stone)
    for z in range(L):
        for y in range(1, H):
            p.put(W - 1, y, z, rubble)
    xs = list(range(tlo[0], thi[0] + 1))
    # the roof: a ceiling course stepping down with the flight, four clear over every tread
    for z in range(L):
        for x in range(W - 1):
            for y in range(1, H):
                p.put(x, y, z, "minecraft:dark_oak_planks")
    stair_head(p, "head", xs[0], 1, xs[-1], 1, tlo[1], "enclosed", stone, top=tlo[1] + 3)
    for x in xs:
        for y in range(tlo[1], tlo[1] + 4):
            p.put(x, y, 0, None)
            p.put(x, y, 1, None)
    p.claim("head", xs[0], tlo[1], 1, xs[-1], tlo[1] + 3, 1)
    run = list(range(2, L - 2))
    for i, z in enumerate(run):
        lvl = tlo[1] - round((i + 1) * (tlo[1] - blo[1]) / (len(run) + 1))
        for x in xs:
            for y in range(lvl, lvl + 4):
                p.put(x, y, z, None)
    flight(p, xs, run, tlo[1], blo[1], "stone_brick", stone, via="flight")
    for x in xs:
        for z in (L - 2, L - 1):
            p.put(x, 0, z, stone)
            for y in range(blo[1], blo[1] + 4):
                p.put(x, y, z, None)
    p.claim("room", xs[0], 1, L - 2, xs[-1], blo[1] + 3, L - 1)
    for z in run:
        lv = max(y for y in range(H) if p.get(xs[0], y, z) is not None and y < H - 1 and passable(p.get(xs[0], y + 1, z)))
        # unclaimed air over a tread's body cells is the flight's too
        for x in xs:
            for y in range(lv + 1, H):
                if passable(p.get(x, y, z)) and (x, y, z) not in p.cl:
                    p.cl[(x, y, z)] = "flight"
    for z in (3, 7):
        lv = max(y for y in range(H) if passable(p.get(1, y, z)))
        hang(p, 1, lv, z)
    hang(p, 2, blo[1] + 3, L - 2)
    p.stair_edge("flight", "room", "head")
    p.seam_space = {"way-coach-to-steps": "head"}
    p.cut_seams(floor=stone)
    p.mark("node-cliff-steps", (1, blo[1], L - 2), "south")
    return p


def high_street():
    """The high street: a cobbled street between two terraces of cottages, each front its own
    (grey stone, rubble, brick, or limewash in a dark timber frame), on a plinth course, with
    windows set between sill and lintel, doors between jambs under slate hoods, slate eaves
    and chimney stacks at the party walls; lamp posts at the kerbs; the sleepers stand at two
    of the doors, facing the sea."""
    p = Place("high-street", envelope="open")
    W, H, L = p.W, p.H, p.L
    cob = p.role("cobbles", COBBLES)
    setts = p.role("setts", SETTS)
    p.box(0, 0, 0, W - 1, 0, L - 1, cob)
    for z in range(L):
        p.put(1, 0, z, setts); p.put(W - 2, 0, z, setts)
    kinds = ["stone", "limewash", "rubble", "brick"]
    west = [(0, 5, 3), (6, 11, 9), (12, 17, 15), (18, 23, 21), (24, 29, 27), (30, 35, 33), (36, 41, 39), (42, 47, 45)]
    east = [(0, 4, 2), (5, 10, 8), (11, 16, 14), (17, 22, 20), (23, 26, 25), (27, 31, 29), (32, 37, 35), (38, 42, 40), (43, 47, 45)]
    for k, (a0, a1, d) in enumerate(west):
        wins = [(a, 3) for a in (d - 2, d + 2) if a0 < a < a1]
        street_house(p, "west", a0, a1, kinds[k % 4], door=d, windows=wins, chimney=a0 if k % 2 == 0 else None)
    for k, (a0, a1, d) in enumerate(east):
        wins = [(a, 3) for a in (d - 2, d + 2) if a0 < a < a1]
        street_house(p, "east", a0, a1, kinds[(k + 2) % 4], door=d, windows=wins, chimney=a1 if k % 2 else None)
    for (x, z) in ((1, 1), (W - 2, 6), (1, 11), (W - 2, 18), (1, 24), (W - 2, 32), (1, 37), (W - 2, 43), (1, 47)):
        lamp_post(p, x, z, 2)
    p.put(W - 2, 1, 26, "minecraft:water_cauldron[level=3]"); p.put(W - 2, 1, 27, "minecraft:cauldron")
    p.put(1, 1, 30, barrel("east")); p.put(1, 1, 31, barrel("east"))
    p.cut_seams(floor=cob)
    p.mark("node-high-street", (3, 1, 23), "south")
    return p


def harbour_office():
    """The harbour office: a panelled room of two storeys, entered from the street onto a
    gallery and down a stair along the wall to the harbourmistress's floor; her desk and
    chart under the gallery, the tide board on the wall, shelves of tide books, a window
    over the harbour."""
    p = Place("harbour-office", envelope="enclosed")
    W, H, L = p.W, p.H, p.L
    boards = p.role("boards", BOARDS)
    stone = p.role("stone", TOWN_STONE)
    plaster = p.role("plaster", PLASTER)
    room_shell(p, boards, plaster, "minecraft:spruce_planks", base=stone, posts=log("stripped_spruce_log"))
    for x in range(W):
        for z in range(L):
            if x in (0, W - 1) or z in (0, L - 1):
                for y in (2, 3):
                    p.put(x, y, z, "minecraft:spruce_planks")
    north = p.seam("street-to-office"); nlo, nhi = p.seam_box(north)
    g = nlo[1] - 1
    for x in range(1, W - 1):
        for z in (1, 2, 3):
            p.put(x, g, z, "minecraft:spruce_planks")
    for x in range(1, W - 1):
        p.put(x, g, 4, "minecraft:spruce_planks")
        if x < W - 3:
            p.put(x, g + 1, 4, fence("spruce", e=x < W - 4, w=x > 1))
    for x in (1, 5):
        for y in range(1, g):
            p.put(x, y, 4, log("stripped_spruce_log"))
    p.claim("gallery", 1, g + 1, 1, W - 2, H - 2, 4, envelope="enclosed")
    # the stair: down the east wall from the gallery's end
    xs = [W - 3, W - 2]
    run = list(range(4, L - 1))
    for x in xs:
        p.put(x, g, 4, None)
    flight(p, xs, run, g + 1, 1, "spruce", "minecraft:spruce_planks", via="stair")
    for z in run:
        for x in xs:
            for y in range(1, H - 1):
                if passable(p.get(x, y, z)) and (x, y, z) not in p.cl:
                    pass
    p.stair_edge("stair", "room", "gallery")
    p.seam_space = {"way-street-to-office": "gallery"}
    # Wenna's desk and chart under the gallery, a candle on it
    p.put(3, 1, 2, "minecraft:dark_oak_planks"); p.put(4, 1, 2, barrel("south")); p.put(5, 1, 2, "minecraft:dark_oak_planks")
    p.put(3, 2, 2, candle(3)); p.put(5, 2, 2, "minecraft:dark_oak_pressure_plate[powered=false]")
    p.put(4, 1, 1, stair("dark_oak", "south"))
    # the tide board on the west wall: a dark board with its gauge stuck at low
    for z in range(3, 8):
        for y in range(4, 8):
            p.put(0, y, z, "minecraft:dark_oak_planks")
    for y in range(4, 8):
        p.put(0, y, 5, "minecraft:white_wool")
    p.put(0, 4, 5, "minecraft:blue_wool"); p.put(0, 4, 4, "minecraft:red_wool")
    # shelves of tide books to the gallery's floor, a chart table, a window over the harbour
    for z in (7, 8, 9):
        for y in range(1, H - 1):
            p.put(1, y, z, "minecraft:bookshelf")
    p.put(5, 1, 8, "minecraft:cartography_table")
    for x in (2, 3, 6, 7):
        for y in (4, 5, 6):
            p.put(x, y, L - 1, pane("glass_pane", e=True, w=True))
    hang(p, 3, 7, 8); hang(p, 6, 10, 6); hang(p, 3, 6, 2); hang(p, 7, 6, 2)
    hang(p, 7, 10, 2); hang(p, 2, 10, 2); hang(p, 7, 10, 9); hang(p, 4, 10, 10)
    p.put(7, 1, 10, LANTERN)
    p.cut_seams(floor=boards)
    p.mark("node-harbour-office", (3, 1, 3), "south")
    p.mark("tide-board", (1, 1, 5), "west")
    return p


def fish_market():
    """The covered fish market: a timber hall over flagstones, entered from the office down a
    stone stair; stalls of barrels and ice along the walls, nets hung from the trusses, the
    price slate stopped four days ago; on the south side the sea doors at the head of the
    slipway the Drowned came up, wet weed on the stones before them; open on the east to the
    seawall."""
    p = Place("fish-market", envelope="enclosed")
    W, H, L = p.W, p.H, p.L
    flags = p.role("flags", FLAGS)
    stone = p.role("stone", TOWN_STONE)
    room_shell(p, flags, stone, "minecraft:spruce_planks", base=stone)
    for z in range(L):
        for y in range(5, H - 1):
            p.put(0, y, z, "minecraft:spruce_planks"); p.put(W - 1, y, z, "minecraft:spruce_planks")
    for x in range(W):
        for y in range(5, H - 1):
            p.put(x, y, 0, "minecraft:spruce_planks"); p.put(x, y, L - 1, "minecraft:spruce_planks")
    pitched(p, 1, W - 2, 1, L - 2, 6, along="z", stair_mat="spruce", board="minecraft:spruce_planks", beams_every=4)
    for z in range(3, L - 1, 4):
        for x in (1, W - 2):
            if x == W - 2 and 9 <= z <= 15:
                continue
            for y in range(1, H - 3):
                p.put(x, y, z, log("spruce_log"))
    north = p.seam("office-to-market"); nlo, nhi = p.seam_box(north)
    xs = list(range(nlo[0], nhi[0] + 1))
    stair_head(p, "landing", xs[0], 1, xs[-1], 1, nlo[1], "enclosed", stone, top=H - 2)
    run = list(range(2, 10))
    flight(p, xs, run, nlo[1], 1, "stone_brick", stone, via="stair")
    for z in range(1, 10):
        top = max([y for y in range(H) if (xs[0], y, z) in p.struct] + [0])
        for x in (xs[0] - 1, xs[-1] + 1):
            for y in range(1, top + 1):
                p.put(x, y, z, stone)
            p.put(x, top + 1, z, wall("stone_brick", up=True))
    p.stair_edge("stair", "room", "landing")
    p.seam_space = {"way-office-to-market": "landing"}
    # stalls: barrels with ice and fish along the west wall and the south wall
    for z in range(2, L - 2):
        if z % 4 == 3:
            continue
        p.put(2, 1, z, barrel("east"))
        if z % 2 == 0:
            p.put(1, 1, z, "minecraft:packed_ice")
    for x in range(14, W - 2):
        if x % 4 == 3:
            continue
        p.put(x, 1, L - 3, barrel("north"))
    for x in (4, 6, 8):
        p.put(x, 1, L - 3, "minecraft:water_cauldron[level=3]")
    # striped awnings over the west stalls, on posts at their fronts
    for z in range(2, L - 2):
        p.put(3, 4, z, "minecraft:red_carpet" if z % 2 else "minecraft:white_carpet")
        p.put(2, 4, z, "minecraft:red_carpet" if z % 2 else "minecraft:white_carpet")
    for z in (2, 6, 10, 14, L - 3):
        for y in (1, 2, 3):
            if p.get(3, y, z) is None:
                p.put(3, y, z, fence("spruce"))
    # the sea doors at the head of the slip, weed and wet stone before them
    for x in range(15, 20):
        for y in range(1, 5):
            p.put(x, y, L - 1, "minecraft:dark_oak_planks" if (x + y) % 2 else log("stripped_dark_oak_log", "x"))
        for z in range(L - 5, L - 1):
            p.put(x, 0, z, "minecraft:mossy_stone_bricks" if (x + z) % 3 else "minecraft:prismarine_bricks")
    p.put(15, 1, L - 2, "minecraft:grindstone[face=floor,facing=north]")
    for (x, z) in ((5, 3), (9, 7), (18, 3), (14, 11), (6, 15), (20, 7)):
        p.put(x, H - 4, z, "minecraft:cobweb")
    for (x, z) in ((7, 3), (16, 3), (21, 11), (9, 15), (14, 7), (21, 3), (5, 7), (18, 15), (12, 17), (19, 7), (5, 11)):
        hang(p, x, 5, z)
    for (x, z) in ((3, 6), (3, 12), (20, 15)):
        p.put(x, 1, z, LANTERN)
    p.put(xs[0] - 1, nlo[1], 1, LANTERN); p.put(xs[-1] + 1, nlo[1], 1, LANTERN)
    p.cut_seams(floor=flags)
    p.mark("node-fish-market", (14, 1, 12), "east")
    p.mark("market-slate", (16, 1, 9), "south")
    return p


def seawall():
    """The seawall: a paved promenade on the wall between the town and the emptied harbour,
    a parapet on its sea side with bollards and lamps, the steps up to the net lofts, the
    chapel's lane on the north, and on the south the Customs House door with its lock."""
    p = Place("seawall", envelope="open")
    W, H, L = p.W, p.H, p.L
    setts = p.role("setts", SETTS)
    stone = p.role("stone", TOWN_STONE)
    p.box(0, 0, 0, W - 1, 0, L - 1, setts)
    for x in range(W):
        p.put(x, 0, L - 1, stone)
    cust = p.seam("seawall-to-customs"); clo, chi = p.seam_box(cust)
    lofts = p.seam("seawall-to-lofts"); llo, lhi = p.seam_box(lofts)
    chap = p.seam("seawall-to-chapel"); plo, phi = p.seam_box(chap)
    for x in range(W):
        if clo[0] - 2 <= x <= chi[0] + 2:
            continue
        p.put(x, 1, L - 1, "minecraft:stone_bricks")
        p.put(x, 2, L - 1, slab("stone_brick"))
    for x in range(clo[0] - 2, chi[0] + 3):
        for y in range(1, 5):
            if x == clo[0] and y in (1, 2):
                continue
            p.put(x, y, L - 1, stone)
        p.put(x, 5, L - 1, stair(SLATE, "south"))
    p.put(clo[0], 3, L - 1, "minecraft:chiseled_stone_bricks")
    # the harbour fronts along the north side, between the lanes to the lofts and the chapel
    segs = []
    gaps = sorted([(llo[0] - 1, lhi[0] + 1), (plo[0] - 1, phi[0] + 1)])
    start = 0
    for g0, g1 in gaps:
        if g0 - 1 >= start:
            segs.append((start, g0 - 1))
        start = g1 + 1
    segs.append((start, W - 1))
    kinds = ["rubble", "limewash", "stone", "brick"]
    k = 0
    for (s0, s1) in segs:
        a = s0
        while a <= s1:
            b = min(s1, a + 6)
            if b - a >= 2:
                d = (a + b) // 2
                street_house(p, "north", a, b, kinds[k % 4], door=d if k % 2 == 0 else None,
                             windows=[(w, 3) for w in (a + 1, b - 1) if w != d], chimney=a if k % 3 == 0 else None)
            else:
                for aa in range(a, b + 1):
                    for y in range(1, 5):
                        p.put(aa, y, 0, stone)
            k += 1
            a = b + 1
    # the steps up to the lofts: a landing under the loft door, a flight down to the wall
    xs = list(range(llo[0], lhi[0] + 1))
    for x in (llo[0] - 1, lhi[0] + 1):
        for z in range(0, 4):
            for y in range(1, 4 - max(z - 1, 0) + 1):
                p.put(x, y, z, stone)
            p.put(x, 4 - max(z - 1, 0) + 1, z, wall("stone_brick", up=True))
    for x in xs:
        for y in range(1, llo[1]):
            p.put(x, y, 0, stone)
    stair_head(p, "steps-top", xs[0], 1, xs[-1], 1, llo[1], "open", stone)
    flight(p, xs, [2, 3], llo[1], 1, "stone_brick", stone, via="steps")
    p.stair_edge("steps", "room", "steps-top")
    p.seam_space = {"way-seawall-to-lofts": "steps-top"}
    for x in (3, 10, 24, 31, 37):
        p.put(x, 1, L - 2, wall("stone_brick", up=True))
    for x in (6, 20, 28, 35):
        lamp_post(p, x, L - 2, 2, wood="dark_oak")
    for x in (2, 12, 33, 38, 9):
        lamp_post(p, x, 1 if x not in (33, 2) else 2, 2)
    # a covered seat for the harbour watch against the north houses
    for x in range(30, 35):
        p.put(x, 4, 1, slab("spruce", "top"))
    for x in (30, 34):
        for y in (1, 2, 3):
            p.put(x, y, 1, log("dark_oak_log"))
    for x in range(31, 34):
        p.put(x, 1, 1, stair("spruce", "north"))
    p.put(clo[0] - 2, 1, L - 2, LANTERN); p.put(chi[0] + 2, 1, L - 2, LANTERN)
    for x in (plo[0] - 2, phi[0] + 2, llo[0] + 5):
        lamp_post(p, x, 1, 2)
    p.cut_seams(floor=setts)
    p.mark("node-seawall", (19, 1, 3), "east")
    p.mark("customs-lock", (clo[0] + 1, 1, L - 2), "south")
    p.mark("unlock-seawall-to-customs", (clo[0] - 1, 1, L - 2), "south")
    return p


def seamens_chapel():
    """The seamen's chapel: a plastered nave under a boarded vault, pews either side of the
    aisle from the seawall door to the chancel; on the north wall behind the altar the
    Rubbing, four carved panels with the carvers' script under the second; candles; the
    door to the crypt stair on the west."""
    p = Place("seamens-chapel", envelope="enclosed")
    W, H, L = p.W, p.H, p.L
    flags = p.role("flags", FLAGS)
    stone = p.role("stone", TOWN_STONE)
    plaster = p.role("plaster", PLASTER)
    room_shell(p, flags, plaster, "minecraft:spruce_planks", base=stone, posts=stone)
    pitched(p, 1, W - 2, 1, L - 2, 7, along="z", stair_mat="spruce", board="minecraft:spruce_planks", beams_every=4)
    for z in (4, 12, 16, 20):
        for y in (3, 4, 5, 6):
            p.put(0, y, z, pane("light_blue_stained_glass_pane", n=True, s=True))
            p.put(W - 1, y, z, pane("light_blue_stained_glass_pane", n=True, s=True))
    for x in range(5, 11):
        p.put(x, 1, 1, "minecraft:chiseled_stone_bricks" if x in (7, 8) else "minecraft:polished_andesite")
    for i, x0 in enumerate((2, 5, 9, 12)):
        for x in (x0, x0 + 1):
            for y in range(3, 7):
                p.put(x, y, 0, "minecraft:smooth_sandstone")
        motif = [((0, 1), "minecraft:black_terracotta"), ((1, 0), "minecraft:brown_terracotta"),
                 ((0, 2), "minecraft:chiseled_sandstone"), ((1, 3), "minecraft:gray_terracotta")]
        for (dx, dy), b in motif[: i + 2]:
            p.put(x0 + dx, 3 + dy, 0, b)
    for y in range(3, 7):
        p.put(4, y, 0, log("dark_oak_log")); p.put(8, y, 0, log("dark_oak_log")); p.put(11, y, 0, log("dark_oak_log"))
    p.put(6, 2, 0, "minecraft:chiseled_stone_bricks")
    for z in range(8, L - 4, 2):
        for x in list(range(2, 6)) + list(range(10, 14)):
            p.put(x, 1, z, stair("spruce", "north"))
    p.put(7, 2, 1, candle(3)); p.put(8, 2, 1, candle(4)); p.put(5, 2, 1, candle(2)); p.put(10, 2, 1, candle(2))
    for z in (6, 12, 18):
        hang(p, 7, H - 4, z)
    for (x, z) in ((1, 13), (W - 2, 6), (W - 2, 15), (1, 19), (1, 3), (W - 2, 3), (13, 22), (2, 22)):
        p.put(x, 1, z, LANTERN)
    for (x, z) in ((4, 3), (11, 3), (7, 9)):
        hang(p, x, 6, z)
    p.cut_seams(floor=flags)
    p.mark("node-seamens-chapel", (8, 1, 4), "north")
    p.mark("rubbing", (6, 1, 3), "north")
    p.mark("rubbing-script", (6, 1, 2), "north")
    return p


def chapel_crypt():
    """The crypt under the chapel: a stair down from the chapel's door into a low vault of
    rubble; the drowned of earlier storms laid in niches in the walls; the founders'
    cupboard with the oldest chart."""
    p = Place("chapel-crypt", envelope="enclosed")
    W, H, L = p.W, p.H, p.L
    rubble = p.role("rubble", RUBBLE)
    stone = p.role("stone", TOWN_STONE)
    room_shell(p, stone, rubble, rubble)
    door = p.seam("chapel-to-crypt"); dlo, dhi = p.seam_box(door)
    zs = list(range(dlo[2], dhi[2] + 1))
    # the vault over the low room, and solid rock over the stair but for its headroom
    for x in range(1, W - 1):
        for z in range(1, L - 1):
            for y in range(6, H - 1):
                p.put(x, y, z, rubble)
            p.put(x, 5, z, stair("cobblestone", "east" if x <= 5 else "west", "top")) if x in (1, W - 2) else None
    stair_head(p, "stairhead", W - 2, zs[0], W - 2, zs[-1], dlo[1], "enclosed", stone, top=dlo[1] + 2)
    run = list(range(W - 3, 1, -1))
    fz = zs[1:]
    for i, x in enumerate(run):
        lvl = dlo[1] - round((i + 1) * (dlo[1] - 1) / (len(run) + 1))
        for z in fz:
            for y in range(lvl, lvl + 3):
                p.put(x, y, z, None)
    flight(p, fz, run, dlo[1], 1, "stone_brick", stone, axis="x", via="stair")
    for x in run:
        for z in fz:
            for y in range(1, H - 1):
                if passable(p.get(x, y, z)) and (x, y, z) not in p.cl and y > 4:
                    p.cl[(x, y, z)] = "stair"
        for y in range(1, 5):
            if p.get(x, y, zs[0]) is not None and (x, y, zs[0]) in p.struct and x < W - 2:
                p.put(x, y, zs[0], None)
    p.put(W - 2, dlo[1] + 1, zs[0] - 1, LANTERN)
    p.entry = "stairhead"
    p.stair_edge("stair", "room", "stairhead")
    p.seam_space = {"way-chapel-to-crypt": "stairhead"}
    for z in (8, 9):
        p.put(1, 1, z, "minecraft:bone_block[axis=z]")
        p.put(1, 2, z, "minecraft:skeleton_skull[powered=false,rotation=4]")
        p.put(1, 3, z, slab("cobblestone", "top"))
    for x in (4, 6):
        p.put(x, 1, 1, "minecraft:bone_block[axis=x]")
        p.put(x, 2, 1, "minecraft:skeleton_skull[powered=false,rotation=0]")
        p.put(x, 3, 1, slab("cobblestone", "top"))
    for y in (1, 2):
        p.put(2, y, 1, "minecraft:chiseled_bookshelf[facing=south,slot_0_occupied=true,slot_1_occupied=false,slot_2_occupied=true,slot_3_occupied=true,slot_4_occupied=false,slot_5_occupied=true]")
    p.put(2, 3, 1, slab("dark_oak", "top"))
    for x in range(1, 8):
        for y in (4, 5):
            p.put(x, y, 1, rubble)
    for z in range(1, L - 1):
        for y in (4, 5):
            p.put(1, y, z, rubble)
    for (x, z) in ((1, 3), (1, 6), (5, 1), (1, 9)):
        p.put(x, 1, z, candle(3))
    hang(p, 3, 4, 5); hang(p, 7, 4, 8); hang(p, 4, 4, 9)
    p.put(W - 2, 1, 1, LANTERN); p.put(W - 2, 1, L - 2, LANTERN)
    p.cut_seams(floor=stone)
    p.mark("node-chapel-crypt", (3, 1, 3), "north")
    p.mark("founders-cupboard", (2, 1, 2), "north")
    return p


def customs_house():
    """The Customs House: the town's record room behind its locked door; a counter across
    the room, shelves of ledgers to the ceiling, the chart cabinet by the west wall, the chip
    of the Brow Stone in its case at the counter's end, the night ledger on its desk."""
    p = Place("customs-house", envelope="enclosed")
    W, H, L = p.W, p.H, p.L
    boards = p.role("boards", BOARDS)
    stone = p.role("stone", TOWN_STONE)
    plaster = p.role("plaster", PLASTER)
    room_shell(p, boards, plaster, "minecraft:dark_oak_planks", base=stone, posts=log("stripped_dark_oak_log"))
    pitched(p, 1, L - 2, 1, W - 2, 4, along="x", stair_mat="dark_oak", board="minecraft:dark_oak_planks", beams_every=3)
    for x in range(3, W - 1):
        p.put(x, 1, 6, slab("dark_oak", "top") if x % 3 else barrel("north"))
    p.put(9, 2, 6, candle(3)); p.put(5, 2, 6, candle(2))
    for z in range(1, 6):
        for y in range(1, H - 2):
            p.put(W - 2, y, z, "minecraft:bookshelf")
    for x in range(9, W - 2):
        for y in range(1, H - 2):
            p.put(x, y, 1, "minecraft:bookshelf")
    p.put(1, 1, 2, "minecraft:lectern[facing=east,has_book=false,powered=false]")
    p.put(4, 1, 1, barrel("south")); p.put(5, 1, 1, barrel("south"))
    p.put(11, 1, 9, "minecraft:lectern[facing=north,has_book=false,powered=false]")
    p.put(12, 1, 9, stair("dark_oak", "north"))
    hang(p, 4, H - 3, 4); hang(p, 11, H - 3, 4) if p.get(11, H - 2, 4) is not None else hang(p, 11, H - 3, 3)
    hang(p, 7, H - 3, 9); hang(p, 13, H - 3, 9); hang(p, 3, H - 3, 9)
    p.put(1, 1, 9, LANTERN); p.put(1, 1, 1, LANTERN)
    p.cut_seams(floor=boards)
    p.mark("node-customs-house", (7, 1, 4), "south")
    p.mark("customs-chart", (2, 1, 3), "west")
    p.mark("stone-chip", (2, 1, 6), "south")
    return p


def net_lofts():
    """The net lofts: a low boarded loft under the eaves, nets hung over poles, floats in a
    heap, barrels of tar; the chest of food and arrows; a sleeper at the loft door."""
    p = Place("net-lofts", envelope="enclosed")
    W, H, L = p.W, p.H, p.L
    boards = p.role("boards", BOARDS)
    room_shell(p, boards, "minecraft:spruce_planks", "minecraft:spruce_planks", posts=log("stripped_spruce_log"))
    pitched(p, 1, L - 2, 1, W - 2, 3, along="x", beams_every=3)
    for (x, z) in ((2, 2), (2, 3), (6, 2), (6, 4), (9, 3), (9, 4), (2, 5)):
        p.put(x, H - 3, z, "minecraft:cobweb")
    for (x, z) in ((1, 1), (1, 2), (10, 1)):
        p.put(x, 1, z, barrel("up"))
    for (x, z) in ((10, 5), (10, 6)):
        p.put(x, 1, z, "minecraft:hay_block[axis=x]")
    p.put(7, 1, 1, "minecraft:chest[facing=south,type=single,waterlogged=false]")
    p.put(8, 1, 1, "minecraft:white_wool"); p.put(9, 1, 1, "minecraft:red_wool")
    p.put(3, 1, 1, "minecraft:loom[facing=south]")
    hang(p, 4, H - 3, 3); hang(p, 8, H - 3, 4)
    p.put(1, 1, 5, LANTERN)
    p.cut_seams(floor=boards)
    p.mark("node-net-lofts", (5, 1, 3), "north")
    return p


def boatyard():
    """The boatyard on the emptied harbour's mud: the town's boats lying where the water
    left them, a shipwright's shed on the mud with the note pinned to it, the quay walls on
    the north and west with their stone steps down from the Customs House and the pier."""
    p = Place("boatyard", envelope="open")
    W, H, L = p.W, p.H, p.L
    mud = p.role("mud", MUD)
    stone = p.role("stone", TOWN_STONE)
    p.box(0, 0, 0, W - 1, 0, L - 1, mud)
    n = p.seam("customs-to-boatyard"); nlo, nhi = p.seam_box(n)
    w = p.seam("boatyard-to-pier"); wlo, whi = p.seam_box(w)
    q = nlo[1]
    # the quay walls: north (z 0-1) and west (x 0-1), with a parapet on their heads
    for x in range(W):
        for z in (0, 1):
            for y in range(1, q):
                p.put(x, y, z, stone)
            p.put(x, q, z, wall("stone_brick", e="low", w="low"))
    for z in range(L):
        for x in (0, 1):
            for y in range(1, q):
                p.put(x, y, z, stone)
            p.put(x, q, z, wall("stone_brick", n="low", s="low"))
    # the steps down the north wall
    xs = list(range(nlo[0], nhi[0] + 1))
    for x in xs:
        for y in range(q, q + 3):
            p.put(x, y, 0, None); p.put(x, y, 1, None)
    stair_head(p, "north-head", xs[0], 1, xs[-1], 1, q, "open", stone)
    run = list(range(2, 2 + q))
    flight(p, xs, run, q, 1, "stone_brick", stone, via="north-steps")
    for z in range(1, 2 + q):
        for x in (xs[0] - 1, xs[-1] + 1):
            lv = max([y for y in range(H) if (xs[0], y, z) in p.struct] + [0])
            for y in range(1, lv + 1):
                p.put(x, y, z, stone)
            p.put(x, lv + 1, z, wall("stone_brick", up=True))
    p.stair_edge("north-steps", "room", "north-head")
    # the steps down the west wall
    zs = list(range(wlo[2], whi[2] + 1))
    for z in zs:
        for y in range(q, q + 3):
            p.put(0, y, z, None); p.put(1, y, z, None)
    stair_head(p, "west-head", 1, zs[0], 1, zs[-1], q, "open", stone)
    runx = list(range(2, 2 + q))
    flight(p, zs, runx, q, 1, "stone_brick", stone, axis="x", via="west-steps")
    for x in range(1, 2 + q):
        for z in (zs[0] - 1, zs[-1] + 1):
            lv = max([y for y in range(H) if (x, y, zs[0]) in p.struct] + [0])
            for y in range(1, lv + 1):
                p.put(x, y, z, stone)
            p.put(x, lv + 1, z, wall("stone_brick", up=True))
    p.stair_edge("west-steps", "room", "west-head")
    p.seam_space = {"way-customs-to-boatyard": "north-head", "way-boatyard-to-pier": "west-head"}
    # boats lying on the mud, heeled over
    def boat(x0, z0, length, along="z", heel=1):
        for i in range(length):
            x, z = (x0, z0 + i) if along == "z" else (x0 + i, z0)
            end = i in (0, length - 1)
            wd = 1 if end else 2
            for j in range(-wd, wd + 1):
                cx, cz = (x + j, z) if along == "z" else (x, z + j)
                p.put(cx, 1, cz, "minecraft:dark_oak_planks" if abs(j) < wd else "minecraft:spruce_planks")
                if abs(j) == wd and not end and j == heel * wd:
                    p.put(cx, 2, cz, "minecraft:spruce_planks")
                    p.put(cx, 3, cz, slab("spruce"))
            if end:
                p.put(x, 2, z, log("dark_oak_log"))
    boat(21, 14, 7, "z", 1)
    boat(24, 23, 6, "x", -1)
    boat(8, 20, 8, "z", -1)
    boat(15, 26, 5, "x", 1)
    # the shipwright's shed: a lean-to on posts, the note pinned to its post
    for x in range(12, 17):
        for z in range(14, 17):
            p.put(x, 4, z, slab("spruce"))
    for (x, z) in ((12, 14), (16, 14), (12, 16), (16, 16)):
        for y in (1, 2, 3):
            p.put(x, y, z, log("spruce_log"))
    p.put(13, 1, 14, "minecraft:smithing_table"); p.put(15, 1, 14, barrel("up")); p.put(14, 1, 14, "minecraft:spruce_planks")
    hang(p, 14, 3, 15)
    for z in (20, 21):
        p.put(15, 1, z, log("spruce_log", "x")); p.put(16, 1, z, log("spruce_log", "x"))
    for (x, z) in ((7, 12), (25, 10), (27, 29), (9, 29), (18, 22), (29, 17), (5, 5), (24, 5), (4, 13),
                   (5, 21), (13, 5), (20, 9), (12, 23), (25, 28), (29, 5), (5, 29), (19, 29), (30, 23)):
        lamp_post(p, x, z, 3)
    for (x, z) in ((xs[0] - 2, 1), (xs[-1] + 2, 1), (1, zs[0] - 2), (1, zs[-1] + 2)):
        p.put(x, q, z, LANTERN)
    p.cut_seams(floor=mud)
    p.mark("node-boatyard", (17, 1, 19), "south")
    p.mark("shipwright-note", (14, 1, 17), "north")
    return p


def whalers_shed():
    """The whalers' shed: a high timber shed of the last whaling crew; the try-pots over their
    fire, a whale's jawbone set up as an arch, barrels of oil, and on the rack by the north
    wall the flensing tools, the Flensing Spade among them."""
    p = Place("whalers-shed", envelope="enclosed")
    W, H, L = p.W, p.H, p.L
    boards = p.role("boards", BOARDS)
    room_shell(p, boards, "minecraft:spruce_planks", "minecraft:dark_oak_planks", posts=log("spruce_log"))
    pitched(p, 1, W - 2, 1, L - 2, 5, along="z", board="minecraft:dark_oak_planks", beams_every=4)
    for z in range(1, L - 1, 4):
        for x in (1, W - 2):
            for y in range(1, H - 2):
                p.put(x, y, z, log("spruce_log"))
    for x in range(9, 14):
        for z in range(10, 14):
            p.put(x, 0, z, "minecraft:bricks")
    p.put(10, 1, 11, "minecraft:cauldron"); p.put(12, 1, 11, "minecraft:cauldron")
    p.put(11, 1, 12, "minecraft:campfire[facing=north,lit=true,signal_fire=false,waterlogged=false]")
    for y in range(1, 6):
        p.put(4, y, 12, bone()); p.put(7, y, 12, bone())
    for x in range(4, 8):
        p.put(x, 6, 12, bone("x"))
    for (x, z) in ((13, 2), (13, 3), (12, 2), (13, 5)):
        p.put(x, 1, z, barrel("up"))
    for x in (3, 4, 5):
        p.put(x, 1, 2, "minecraft:spruce_planks" if x != 4 else "minecraft:smithing_table")
    for x in range(6, 10):
        p.put(x, 3, 1, fence("spruce", e=x < 9, w=x > 6))
        if x != 7:
            p.put(x, 2, 1, "minecraft:lightning_rod[facing=down,powered=false,waterlogged=false]")
    for (x, z) in ((4, 6), (11, 5), (8, 13), (3, 13), (2, 2), (7, 3), (13, 8), (12, 2)):
        hang(p, x, H - 3, z)
    p.put(1, 1, 10, LANTERN)
    p.cut_seams(floor=boards)
    p.mark("node-whalers-shed", (8, 1, 6), "north")
    p.mark("spade-rack", (7, 1, 2), "north")
    return p


def ropewalk():
    """The ropewalk: a long, low rope shed, the rope stretched down its length on posts; a
    sleeper standing at each end; at the far end a stair up to the breakwater."""
    p = Place("ropewalk", envelope="enclosed")
    W, H, L = p.W, p.H, p.L
    boards = p.role("boards", BOARDS)
    stone = p.role("stone", TOWN_STONE)
    s = p.seam("ropewalk-to-breakwater"); slo, shi = p.seam_box(s)
    p.box(0, 0, 0, W - 1, H - 1, L - 1, "minecraft:spruce_planks")
    xs = list(range(slo[0], shi[0] + 1))
    run = list(range(L - 3, L - 3 - slo[1], -1))      # from the head (south) back north
    # the walk: three wide and four high under a low roof
    for z in range(0, run[-1]):
        for x in xs:
            for y in range(1, 5):
                p.put(x, y, z, None)
            p.put(x, 0, z, boards)
    for i, z in enumerate(run):
        lvl = slo[1] - round((i + 1) * (slo[1] - 1) / (len(run) + 1))
        for x in xs:
            for y in range(lvl, lvl + 4):
                p.put(x, y, z, None)
    stair_head(p, "head", xs[0], L - 2, xs[-1], L - 2, slo[1], "enclosed", stone, top=slo[1] + 3)
    for x in xs:
        for z in (L - 2, L - 1):
            for y in range(slo[1], slo[1] + 4):
                p.put(x, y, z, None)
    p.claim("head", xs[0], slo[1], L - 2, xs[-1], slo[1] + 3, L - 2)
    flight(p, xs, run, slo[1], 1, "stone_brick", stone, via="stair")
    for z in run:
        for x in xs:
            for y in range(1, H - 1):
                if passable(p.get(x, y, z)) and (x, y, z) not in p.cl:
                    p.cl[(x, y, z)] = "stair"
    p.stair_edge("stair", "room", "head")
    p.seam_space = {"way-ropewalk-to-breakwater": "head"}
    # the rope: a strand on posts down the east side
    end = run[-1] - 1
    for z in range(2, end):
        p.put(2, 3, z, chain("z"))
    for z in range(2, end, 6):
        p.put(2, 1, z, fence("spruce")); p.put(2, 2, z, fence("spruce"))
        p.put(2, 3, z, fence("spruce", n=True, s=True))
    for z in range(4, end, 7):
        hang(p, 0, 4, z)
    for z in (run[-1] + 2, run[0] - 2):
        hang(p, 0, max(y for y in range(H) if passable(p.get(0, y, z))), z)
    p.put(0, 1, 1, barrel("up")); p.put(2, 1, 0, "minecraft:hay_block[axis=z]") if False else None
    p.cut_seams(floor=boards)
    p.mark("node-ropewalk", (1, 1, 23), "south")
    return p


def breakwater():
    """The breakwater: a stone arm out into the bay, a paved top between parapets, iron
    bollards, lamps on posts, the lighthouse at its end."""
    p = Place("breakwater", envelope="open")
    W, H, L = p.W, p.H, p.L
    setts = p.role("setts", SETTS)
    stone = p.role("stone", TOWN_STONE)
    p.box(0, 0, 0, W - 1, 0, L - 1, setts)
    for z in range(L):
        for x in (0, W - 1):
            p.put(x, 0, z, stone); p.put(x, 1, z, stone)
            p.put(x, 2, z, slab("stone_brick"))
    for z in range(4, L - 2, 8):
        lamp_post(p, 1, z, 2, wood="dark_oak")
        lamp_post(p, W - 2, z + 4, 2, wood="dark_oak")
    lamp_post(p, 1, 1, 2, wood="dark_oak"); lamp_post(p, W - 2, L - 2, 2, wood="dark_oak")
    for z in range(2, L, 10):
        p.put(W - 2, 1, z, wall("andesite", up=True))
    for z in range(26, 30):
        p.put(W - 2, 1, z, None); p.put(W - 2, 2, z, None)
        p.put(W - 2, 3, z, slab("stone_brick", "top"))
        p.put(W - 1, 2, z, "minecraft:stone_bricks"); p.put(W - 1, 3, z, "minecraft:stone_bricks")
    for y in (1, 2):
        p.put(W - 2, y, 25, "minecraft:stone_bricks"); p.put(W - 2, y, 30, "minecraft:stone_bricks")
    p.put(W - 2, 1, 27, stair("stone_brick", "east"))
    p.cut_seams(floor=setts)
    p.mark("node-breakwater", (3, 1, 27), "south")
    return p


def lighthouse():
    """The lighthouse: a stone tower, a stair winding up its inside wall round a solid core,
    the lamp room at the top with its windows over the flat; the lamp the party lights."""
    p = Place("lighthouse", envelope="enclosed")
    W, H, L = p.W, p.H, p.L
    stone = p.role("stone", TOWN_STONE)
    room_shell(p, "minecraft:polished_andesite", "minecraft:stone_bricks", "minecraft:spruce_planks")
    for (x, z) in ((0, 0), (W - 1, 0), (0, L - 1), (W - 1, L - 1)):
        for y in range(1, H - 1):
            p.put(x, y, z, "minecraft:polished_andesite")
    core = (2, 5)
    room = 24
    for x in range(core[0], core[1] + 1):
        for z in range(core[0], core[1] + 1):
            for y in range(1, room):
                p.put(x, y, z, stone)
    ring = []
    for x in range(3, 7): ring.append((x, 1))
    for z in range(2, 7): ring.append((6, z))
    for x in range(5, 0, -1): ring.append((x, 6))
    for z in range(5, 0, -1): ring.append((1, z))
    ring.append((2, 1))
    corners = {(6, 1), (6, 6), (1, 6), (1, 1)}
    lvl = 1; i = 0
    treads = []
    while lvl < room + 1:
        x, z = ring[i % len(ring)]
        nxt = ring[(i + 1) % len(ring)]
        if (x, z) in corners or i == 0:
            if lvl - 1 >= 1:
                p.put(x, lvl - 1, z, "minecraft:polished_andesite")
        else:
            lvl += 1
            d = (nxt[0] - x, nxt[1] - z)
            facing = {(1, 0): "east", (-1, 0): "west", (0, 1): "south", (0, -1): "north"}[d]
            p.put(x, lvl - 1, z, stair("stone_brick", facing))
            if lvl - 2 >= 1 and p.get(x, lvl - 2, z) is None:
                p.put(x, lvl - 2, z, stair("stone_brick", OPP[facing], "top"))
        treads.append((x, lvl, z))
        i += 1
    top_at = {}
    for (x, l, z) in treads:
        top_at[(x, z)] = max(top_at.get((x, z), 0), l)
    for x in range(1, W - 1):
        for z in range(1, L - 1):
            if p.get(x, room, z) is None and top_at.get((x, z), 0) <= room - 4:
                p.put(x, room, z, "minecraft:spruce_planks")
    for (x, l, z) in treads:
        if l <= 1:
            continue
        for y in (l, l + 1):
            if passable(p.get(x, y, z)):
                p.cl[(x, y, z)] = "stair"
    p.claim("lamp-room", 1, room + 1, 1, W - 2, H - 2, L - 2, envelope="enclosed")
    for (x, l, z) in treads:
        if l >= room:
            for y in (l, l + 1):
                p.cl[(x, y, z)] = "stair" if l < room + 1 else "lamp-room"
    for x in range(1, W - 1):
        for y in (room + 1, room + 2):
            p.put(x, y, 0, pane("glass_pane", e=True, w=True)); p.put(x, y, L - 1, pane("glass_pane", e=True, w=True))
    for z in range(1, L - 1):
        for y in (room + 1, room + 2):
            p.put(0, y, z, pane("glass_pane", n=True, s=True)); p.put(W - 1, y, z, pane("glass_pane", n=True, s=True))
    for (x, y, z) in ((5, 3, 4), (2, 3, 3), (5, 6, 2), (3, 8, 5), (2, 11, 2), (5, 12, 4),
                      (4, 15, 5), (2, 17, 4), (4, 19, 2), (5, 21, 5), (3, 22, 5), (2, 7, 4),
                      (4, 10, 2), (5, 16, 3), (3, 14, 2), (2, 20, 3), (3, 5, 5)):
        p.put(x, y, z, LANTERN)       # set into the core's face, the stone above it
    hang(p, 2, H - 2, 2); hang(p, 5, H - 2, 5)
    p.stair_edge("stair", "room", "lamp-room")
    p.cut_seams(floor="minecraft:polished_andesite")
    p.mark("node-lighthouse", (3, 1, 1), "south")
    p.mark("lighthouse-lamp", (4, room + 1, 4), "south")
    return p


def slipway_stair():
    """The slipway: a granite slip with its timber ways, from the boatyard to the iron gate
    onto the flat; a winch at its head, lamps on the slip walls."""
    p = Place("slipway-stair", envelope="open")
    W, H, L = p.W, p.H, p.L
    stone = p.role("stone", TOWN_STONE)
    flags = p.role("flags", FLAGS)
    p.box(0, 0, 0, W - 1, 0, L - 1, flags)
    for z in range(L):
        for x in (0, W - 1):
            for y in (1, 2):
                p.put(x, y, z, stone)
            p.put(x, 3, z, slab("stone_brick"))
        p.put(2, 0, z, log("stripped_spruce_log", "z")); p.put(5, 0, z, log("stripped_spruce_log", "z"))
    p.put(6, 1, 2, "minecraft:grindstone[face=floor,facing=south]")
    for z in (1, 2, 3):
        p.put(6, 3, z, slab("spruce", "top"))
    p.put(6, 1, 1, None); p.put(6, 2, 1, None)
    for z in (1, 6, 12, 17):
        lamp_post(p, 1, z, 2, wood="dark_oak")
    for z in (3, 9, 15):
        lamp_post(p, W - 2, z, 2, wood="dark_oak")
    p.cut_seams(floor=flags)
    p.mark("node-slipway-stair", (3, 1, 9), "south")
    return p


def pier():
    """The pier: a timber deck out from the quay, rails both sides, mooring posts and lamps,
    and at its far end the place the stone is thrown or handed over."""
    p = Place("pier", envelope="open")
    W, H, L = p.W, p.H, p.L
    p.box(0, 0, 0, W - 1, 0, L - 1, lambda x, y, z: "minecraft:spruce_planks" if (x + z) % 5 else "minecraft:dark_oak_planks")
    e = p.seam("boatyard-to-pier"); elo, ehi = p.seam_box(e)
    for z in range(L):
        if not (elo[2] - 1 <= z <= ehi[2] + 1):
            p.put(W - 1, 1, z, fence("spruce", n=z > 0, s=z < L - 1))
        p.put(0, 1, z, fence("spruce", n=z > 0, s=z < L - 1))
    for x in range(W):
        p.put(x, 1, L - 1, fence("spruce", e=x < W - 1, w=x > 0))
    for z in (4, 12, 20, 28):
        p.put(0, 1, z, log("spruce_log")); p.put(0, 2, z, LANTERN)
    for z in range(6, 10):
        p.put(1, 4, z, slab("spruce", "top"))
    for z in (6, 9):
        for y in (1, 2, 3):
            p.put(1, y, z, log("spruce_log"))
    p.put(1, 1, 7, stair("spruce", "west")); p.put(1, 1, 8, stair("spruce", "west"))
    for z in (1, 8, 18, 24):
        p.put(W - 1, 1, z, log("spruce_log")); p.put(W - 1, 2, z, LANTERN)
    p.cut_seams(floor="minecraft:spruce_planks")
    p.mark("node-pier", (3, 1, 20), "south")
    p.mark("pier-end", (2, 1, 29), "south")
    return p


def coyle_house():
    """Davey's room off the harbour lane: a fisherman's cottage room, plastered over a stone
    footing, a beamed ceiling; the soaked bed in the far corner, muddy prints from the bed to
    the door, and on the west wall the dream worked in coloured wool."""
    p = Place("coyle-house", envelope="enclosed")
    W, H, L = p.W, p.H, p.L
    stone = p.role("stone", TOWN_STONE)
    plaster = p.role("plaster", PLASTER)
    boards = p.role("boards", BOARDS)
    room_shell(p, boards, plaster, "minecraft:spruce_planks", base=stone, posts=log("stripped_spruce_log"))
    pitched(p, 1, W - 2, 1, L - 2, 3, along="z", beams_every=3)
    pic = {(z, y): "minecraft:black_wool" for z in range(1, 6) for y in range(2, 5)}
    for z in range(1, 6):
        pic[(z, 2)] = "minecraft:brown_wool"
    for z in (2, 3, 4):
        pic[(z, 3)] = "minecraft:gray_wool"
    pic[(4, 4)] = "minecraft:white_wool"
    pic[(1, 3)] = "minecraft:light_blue_wool"
    for (z, y), b in pic.items():
        p.put(0, y, z, b)
    p.put(5, 1, 1, "minecraft:light_blue_bed[facing=north,occupied=false,part=head]")
    p.put(5, 1, 2, "minecraft:light_blue_bed[facing=north,occupied=false,part=foot]")
    p.put(6, 1, 1, barrel("west"))
    p.put(6, 2, 1, candle(2))
    for (x, z) in ((5, 3), (6, 4), (5, 5)):
        p.put(x, 1, z, "minecraft:brown_carpet")
    p.put(2, 1, 6, fence("spruce"))
    p.put(2, 2, 6, candle(3))
    p.put(3, 1, 6, stair("spruce", "west"))
    p.put(6, 1, 6, barrel("west"))
    p.put(6, 2, 6, "minecraft:flower_pot")
    hang(p, 3, H - 3, 3)
    p.cut_seams(floor=boards)
    p.mark("node-coyle-house", (5, 1, 4), "west")
    p.mark("wool-picture", (1, 1, 3), "west")
    return p


BUILDERS = {
    "coach-road": coach_road, "cliff-steps": cliff_steps, "high-street": high_street,
    "harbour-office": harbour_office, "coyle-house": coyle_house, "fish-market": fish_market,
    "seawall": seawall, "seamens-chapel": seamens_chapel, "chapel-crypt": chapel_crypt,
    "customs-house": customs_house, "net-lofts": net_lofts, "boatyard": boatyard,
    "whalers-shed": whalers_shed, "ropewalk": ropewalk, "breakwater": breakwater,
    "lighthouse": lighthouse, "slipway-stair": slipway_stair, "pier": pier,
}

if __name__ == "__main__":
    kit.main(BUILDERS)
