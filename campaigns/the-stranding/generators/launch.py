"""Marrack's salvage launch, grounded on the mud beside the way.

Writes programs/marracks-launch.json. The frame is the allocation's
(16 x 9 x 24: the mud course and eight courses of air; local x east, z
south). The way runs down the west half; the launch lies along the east
half, bow to the north, keel in the mud, its deck four courses up.

The launch (proportions; sources in GENERATION.md round 5): a working
launch twenty blocks long and six in beam (length/beam 3.3, between the
33 ft x 8 ft steam launch of 1874 and Branksome's 50 x 9.3 ft, National
Historic Ships register), a stem post and a transom, a turned bilge, a
deck with a rail, a deckhouse aft, a short mast, and the lanterns Marrack keeps lit on
deck. A gangway of timber treads climbs from the way onto the deck, and
the deck runs on east to the mast platform.

Run from the campaign directory:  python3 generators/launch.py
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from voxgrammar import rows_z, marked, fence

W, H, L = 16, 9, 24
L_ = L
MUD = [{"weight": 5, "block": "minecraft:mud"}, {"weight": 3, "block": "minecraft:packed_mud"},
       {"weight": 1, "block": "minecraft:coarse_dirt"}]
HULL = "minecraft:dark_oak_planks"
STRAKE = "minecraft:spruce_planks"
DECK = "minecraft:stripped_spruce_wood[axis=z]"
STEM = "minecraft:dark_oak_log[axis=y]"
MAST = "minecraft:stripped_spruce_log[axis=y]"
CABIN = "minecraft:spruce_planks"
CABROOF = "minecraft:dark_oak_slab[type=bottom,waterlogged=false]"
TREADBODY = "minecraft:spruce_planks"
LANTERN = "minecraft:lantern[hanging=false,waterlogged=false]"
HANG = "minecraft:lantern[hanging=true,waterlogged=false]"
BARREL = "minecraft:barrel[facing=up,open=false]"
def stair(wood, facing, half="bottom"):
    return f"minecraft:{wood}_stairs[facing={facing},half={half},shape=straight,waterlogged=false]"

X0, X1 = 10, 15          # beam
BOW, TRANSOM = 2, 21

def beam(z):
    """The breadth row by row: a stem, a fine bow over three rows, the stern drawn in."""
    if z == BOW: return (12, 13)
    if z in (BOW + 1, BOW + 2): return (11, 14)
    if z == TRANSOM: return (11, 14)
    return (X0, X1)

def model():
    g = {(x, y, z): None for x in range(W) for y in range(H) for z in range(L)}
    c = {k: None for k in g}
    def put(x, y, z, b, claim=None): g[(x, y, z)] = b; c[(x, y, z)] = claim
    for x in range(W):
        for z in range(L):
            put(x, 0, z, "mud")
    # the launch
    for z in range(BOW, TRANSOM + 1):
        a, b = beam(z)
        for x in range(a, b + 1):
            side = x in (a, b)
            if z == BOW:
                for y in range(0, 7): put(x, y, z, STEM)  # the stem post, standing a course over the bow rail
                continue
            bow = z <= BOW + 3                                  # the sheer rises over the bow
            put(x, 0, z, HULL)
            put(x, 1, z, stair("dark_oak", "east" if x == a else "west", "top") if side else HULL)
            put(x, 2, z, HULL if side else HULL)
            put(x, 3, z, STRAKE)
            put(x, 4, z, DECK)
            if side or z in (BOW + 1, TRANSOM):
                gap_w = x == a and 10 <= z <= 12          # the gangway comes aboard here
                gap_e = x == b and 10 <= z <= 12          # and the deck runs on to the mast platform
                if bow:
                    put(x, 5, z, STRAKE); put(x, 6, z, "RAIL")   # a bulwark at the bow, railed
                elif not (gap_w or gap_e):
                    put(x, 5, z, "RAIL")
            if y_rub := 3:
                if side: put(x, y_rub, z, "minecraft:stripped_dark_oak_wood[axis=z]")   # the rubbing strake
    # the deckhouse aft: a timber house with a window each side and a slab roof
    for z in range(16, 21):
        for x in range(11, 15):
            for y in (5, 6):
                inside = 12 <= x <= 13 and 17 <= z <= 19
                door = x == 12 and z == 16
                window = y == 6 and z == 18 and x in (11, 14)
                if inside or door: continue
                put(x, y, z, "minecraft:glass" if window else CABIN)
            put(x, 7, z, CABROOF)
    put(13, 5, 19, LANTERN)
    # the mast
    for y in range(5, 9): put(12, y, 8, MAST)
    # the gangway: timber treads from the way up onto the deck, east
    for z in (10, 11, 12):
        put(7, 1, z, stair("spruce", "east"))
        put(8, 1, z, TREADBODY); put(8, 2, z, stair("spruce", "east"))
        put(9, 1, z, TREADBODY); put(9, 2, z, TREADBODY); put(9, 3, z, stair("spruce", "east"))
    # salvage on deck, lanterns on the rail posts and on posts in the mud
    put(13, 5, 13, BARREL); put(14, 5, 13, BARREL); put(13, 5, 4, BARREL)
    for (x, z) in ((10, 6), (15, 6), (10, 15), (15, 18)):
        put(x, 6, z, LANTERN)
    for (x, z) in ((2, 3), (2, 12), (2, 20), (5, 7), (5, 17)):
        put(x, 1, z, "POST"); put(x, 2, z, "POST"); put(x, 3, z, LANTERN)
    return g, c

def resolve(g):
    out = dict(g)
    for (x, y, z), b in g.items():
        if b in ("RAIL", "POST"):
            nb = lambda dx, dz: g.get((x + dx, y, z + dz))
            con = lambda v: v in ("RAIL",)
            out[(x, y, z)] = fence("spruce", n=con(nb(0, -1)), e=con(nb(1, 0)), s=con(nb(0, 1)), w=con(nb(-1, 0))) \
                if b == "RAIL" else fence("spruce")
        elif b == "mud":
            out[(x, y, z)] = {"role": "mud"}
    return out

TOPPED = ("lantern", "barrel", "dark_oak_log", "_slab", "stripped_spruce_log")
def claims(g):
    def deck_cell(x, z):
        if not (BOW <= z <= TRANSOM): return False
        a, b = beam(z); return a <= x <= b
    cl = {}
    for x in range(W):
        for z in range(L_):
            for y in range(1, H):
                below = g.get((x, y - 1, z))
                if g[(x, y, z)] is None and isinstance(below, str) and any(s in below for s in TOPPED):
                    cl[(x, y, z)] = "tops"; continue
                if 5 <= x <= 9 and z == 0 and y <= 5: cl[(x, y, z)] = "north-way"; continue
                if 5 <= x <= 9 and z == L_ - 1 and y <= 5: cl[(x, y, z)] = "south-way"; continue
                if 7 <= x <= 9 and 10 <= z <= 12 and y <= 5: cl[(x, y, z)] = "gangway"; continue
                if x == 15 and 10 <= z <= 12 and 5 <= y <= 7: cl[(x, y, z)] = "east-way"; continue
                if 12 <= x <= 13 and 17 <= z <= 19 and 5 <= y <= 6: cl[(x, y, z)] = "cabin"; continue
                if x == 12 and z == 16 and 5 <= y <= 6: cl[(x, y, z)] = "cabin-door"; continue
                if 11 <= x <= 14 and 16 <= z <= 20 and 5 <= y <= 7: continue
                if deck_cell(x, z):
                    if y >= 5: cl[(x, y, z)] = "deck"
                    continue
                cl[(x, y, z)] = "yard"
    return cl

def main():
    g, _ = model()
    g = resolve(g)
    cl = claims(g)
    def m(x, y, z): return (g[(x, y, z)], cl.get((x, y, z)))
    body = rows_z(m, range(W), range(H), range(L))
    marks = [("node-marracks-launch", (6, 1, 15), "east")]
    prog = {"version": "1.9.0", "name": "marracks-launch", "start": "launch",
            "params": {}, "palette": {"mud": MUD},
            "rules": {"launch": [{"weight": 1, "body": marked(body, marks)}]},
            "contract": {"entry": "yard",
                         "spaces": {"yard": {"envelope": "open"}, "deck": {"envelope": "open"},
                                    "cabin": {"envelope": "enclosed"}},
                         "no_body": {"tops": {"reason": "the tops of the lamps, the barrels, the stem post, the mast and the deckhouse roof, which nobody stands on"}},
                         "edges": [{"a": "exterior", "b": "yard", "class": "walk", "via": "north-way"},
                                   {"a": "yard", "b": "exterior", "class": "walk", "via": "south-way"},
                                   {"a": "yard", "b": "deck", "class": "stair", "rise": 4, "via": "gangway"},
                                   {"a": "deck", "b": "exterior", "class": "walk", "via": "east-way"},
                                   {"a": "deck", "b": "cabin", "class": "walk", "via": "cabin-door"}]},
            "shown_faces": ["up", "north", "south", "east", "west"]}
    here = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(here, "..", "programs", "marracks-launch.json"), "w") as f:
        json.dump(prog, f, indent=2, sort_keys=True); f.write("\n")
    print("wrote programs/marracks-launch.json")

if __name__ == "__main__":
    main()
