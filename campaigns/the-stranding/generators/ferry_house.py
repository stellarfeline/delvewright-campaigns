"""The two ferry houses of the old road, each with Marrack's skiff in its slip.

Writes programs/near-ferry-house.json and programs/far-ferry-house.json.
The two houses are one building: the far house is the near one turned
end for end (its land door faces south, onto the far landing), so the two
skiffs are the same boat block for block.

Run from the campaign directory:  python3 generators/ferry_house.py

The frame is the allocation's (12 x 6 x 16: floor course, four courses of
room, a ceiling course). Local x runs east, z runs from the land door to
the water gate.

The skiff (proportions; sources in GENERATION.md round 5):
- a pointed bow (stem post) and a flat transom stern, flat bottom with a
  turned bilge, the sheer rising toward the bow (Glen-L 17' Whitehall:
  depth forward 2'6", amidships 1'10", aft 2'2");
- ten blocks long and five in beam: fuller than a pulling boat (Whitehall
  length/beam about 3.8) because it carries a party of four and an
  oarsman; the length reads from the taper over the first three rows;
- a gunwale rail, two thwarts, an oar out over the water, a rudder with
  its tiller head over the transom.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from voxgrammar import rows_z, marked, lit, fence

W, H, L = 12, 6, 16
STONE = [{"weight": 6, "block": "minecraft:stone_bricks"},
         {"weight": 2, "block": "minecraft:mossy_stone_bricks"},
         {"weight": 1, "block": "minecraft:cracked_stone_bricks"}]
FLOOR = [{"weight": 3, "block": "minecraft:cobblestone"},
         {"weight": 2, "block": "minecraft:mossy_cobblestone"},
         {"weight": 2, "block": "minecraft:stone"}]
PALETTE = {"wall": STONE, "floor": FLOOR}
WATER = "minecraft:water[level=0]"
HULL = "minecraft:dark_oak_planks"
STRAKE = "minecraft:spruce_planks"
BOARD = "minecraft:dark_oak_planks"   # the skiff's floorboards
CEIL = "minecraft:spruce_planks"
SCREEN = "minecraft:spruce_planks"
GATE = "minecraft:dark_oak_planks"
POST = "minecraft:stripped_spruce_log[axis=y]"
STEM = "minecraft:dark_oak_log[axis=y]"
THWART = "minecraft:spruce_slab[type=bottom,waterlogged=false]"
STEP = "minecraft:dark_oak_slab[type=bottom,waterlogged=false]"
HANG = "minecraft:lantern[hanging=true,waterlogged=false]"
STAND = "minecraft:lantern[hanging=false,waterlogged=false]"
BARREL = "minecraft:barrel[facing=up,open=false]"
TILLER = "minecraft:stripped_dark_oak_log[axis=z]"

def stair(wood, facing, half):
    return f"minecraft:{wood}_stairs[facing={facing},half={half},shape=straight,waterlogged=false]"

# --- the skiff, in house coordinates (near house) ---------------------------
BX0, BX1 = 5, 9          # hull beam: x 5..9, centreline x 7
BOW, TRANSOM = 4, 13     # stem at z 4, transom at z 13
CX = 7

def half_breadth(z):
    """Hull half-breadth at row z: the stem, then the bow's taper, then full."""
    if z == BOW: return 0
    if z == BOW + 1: return 1
    return 2

def skiff(x, y, z):
    """Block of the skiff at (x, y, z), or None for outside the hull."""
    if not (BOW <= z <= TRANSOM): return None
    hb = half_breadth(z)
    dx = x - CX
    if abs(dx) > hb: return None
    side = abs(dx) == hb
    if z == BOW:  # the stem post, standing above the sheer
        return STEM if y <= 3 else None
    if z == TRANSOM:  # the transom, with the tiller head over it
        if y == 0: return HULL
        if y == 1: return STRAKE if not side else HULL
        if y == 2: return "RAIL"
        if y == 3 and dx == 0: return "TILLER"   # the tiller head, on the rudder post over the transom rail
        return None
    bow_rows = z <= BOW + 2          # the sheer rises over the bow rows
    if y == 0:
        if side:  # the turned bilge: a stair whose full half stands inboard
            return stair("dark_oak", "east" if dx < 0 else "west", "top")
        return BOARD  # floorboards
    if y == 1:
        if side:
            if z in (6, 7) and dx < 0: return STEP   # where the party steps in from the quay
            return STRAKE
        if z == 7 and dx == 0: return None          # the oarsman's place
        if z == 8 and dx != 0: return THWART        # the passengers' thwart, aft of the oarsman
        return None
    if y == 2:
        if side:
            if bow_rows: return HULL
            if z in (6, 7) and dx < 0: return None
            return "RAIL"
        return None
    if y == 3 and side and bow_rows:
        return "RAIL"
    return None

def near_model():
    g = {}
    for x in range(W):
        for y in range(H):
            for z in range(L):
                g[(x, y, z)] = None
    def put(x, y, z, b): g[(x, y, z)] = b
    for x in range(W):
        for z in range(L):
            put(x, 0, z, "floor")
            put(x, H - 1, z, CEIL)
            edge = x in (0, W - 1) or z in (0, L - 1)
            if edge:
                for y in range(1, H - 1): put(x, y, z, "wall")
    # the shut water gate in the seaward wall, over the slip
    for x in range(5, 11):
        for y in range(1, H - 1):
            put(x, y, L - 1, GATE if (x + y) % 3 else stair("dark_oak", "north", "top"))
    # the screen that turns the passage: z 2..3, x 2..10; the way in is at x 1
    for x in range(2, W - 1):
        for z in (2, 3):
            for y in range(1, H - 1): put(x, y, z, SCREEN if z == 2 else "wall")
    # the slip: water from x 5 to x 10, z 4..13; a landing at the stern, z 14
    # (the slip water stops at z 11: past it the house stands over open sea, and
    # water there would join the sea under the frame with no way back up)
    for x in range(5, W - 1):
        for z in range(4, 12):
            put(x, 0, z, WATER)
    for x in range(5, W - 1):
        put(x, 0, 14, "floor")
    # the quay: x 1..4 boarded
    for x in range(1, 5):
        for z in range(4, L - 1):
            put(x, 0, z, "floor")
    # the skiff
    for x in range(BX0, BX1 + 1):
        for y in range(0, 4):
            for z in range(BOW, TRANSOM + 1):
                b = skiff(x, y, z)
                if b is not None: put(x, y, z, b)
    # the oar: shipped out over the water on the east side at the rowing thwart
    put(10, 2, 7, "RAIL")
    # stores on the quay, against the west wall, and a lamp post at the quay's edge
    for z in (11, 12, 13):
        put(1, 1, z, BARREL)
    # lanterns Marrack hung: from the ceiling
    for (x, z) in ((5, 1), (2, 5), (2, 9), (7, 9), (9, 13), (3, 14), (10, 5)):
        put(x, H - 2, z, HANG)
    # the oarsman's thwart is the forward one: z 7, standing in the middle
    return g

def resolve_rails(g):
    """Fences join their neighbours: other rails and solid blocks."""
    out = dict(g)
    def solid(b):
        return b is not None and b not in ("RAIL",) and "water" not in b and "lantern" not in b \
            and "slab" not in b and "stairs" not in b and b != "TILLER"
    for (x, y, z), b in g.items():
        if b in ("RAIL", "TILLER"):
            nb = lambda dx, dz: g.get((x + dx, y, z + dz))
            con = lambda v: v in ("RAIL", "TILLER") or solid(v)
            if b == "TILLER":
                out[(x, y, z)] = fence("dark_oak", n=con(nb(0, -1)) and False,
                                       e=con(nb(1, 0)), s=False, w=con(nb(-1, 0)))
            else:
                out[(x, y, z)] = fence("spruce", n=con(nb(0, -1)), e=con(nb(1, 0)),
                                       s=con(nb(0, 1)), w=con(nb(-1, 0)))
    return out

def claims(g, x, y, z):
    """Which declared region a cell belongs to."""
    if x in (0, W - 1) or z in (0, L - 1) or y == H - 1: return None
    if y == 0:
        return "house" if g[(x, 0, z)] == WATER else None
    return "house"

def mirror_z(g):
    """The far house: the near house turned end for end (z reversed); facings follow."""
    flip = {"north": "south", "south": "north"}
    out = {}
    for (x, y, z), b in g.items():
        if isinstance(b, str) and "facing=" in b:
            for a, c in flip.items():
                if f"facing={a}" in b:
                    b = b.replace(f"facing={a}", f"facing={c}"); break
        out[(x, y, L - 1 - z)] = b
    return out

def program(name, g, door_edge, door_z, marks):
    def model(x, y, z):
        b = g[(x, y, z)]
        if isinstance(b, str) and b in PALETTE: b = {"role": b}
        return (b, claims_fn(x, y, z))
    claims_fn = lambda x, y, z: claims(gz, x, y, z)
    gz = g
    # the land-door row is written with the handed seam, the rest as computed
    zs_body = [z for z in range(L) if z != door_z]
    p = f"handed/seam/{door_edge}"
    door_row = {"op": "split", "axis": "x", "sizes": [
            {"size": "absolute", "blocks": {"expr": "param", "name": f"{p}/x0"}},
            {"size": "absolute", "blocks": {"expr": "arith", "op": "add", "rhs": lit(1),
                "lhs": {"expr": "arith", "op": "sub", "lhs": {"expr": "param", "name": f"{p}/x1"},
                        "rhs": {"expr": "param", "name": f"{p}/x0"}}}},
            {"size": "relative", "weight": lit(1)}],
        "children": [
            {"op": "call", "symbol": "end_wall"},
            {"op": "split", "axis": "y", "sizes": [
                {"size": "absolute", "blocks": {"expr": "param", "name": f"{p}/y0"}},
                {"size": "absolute", "blocks": {"expr": "arith", "op": "add", "rhs": lit(1),
                    "lhs": {"expr": "arith", "op": "sub", "lhs": {"expr": "param", "name": f"{p}/y1"},
                            "rhs": {"expr": "param", "name": f"{p}/y0"}}}},
                {"size": "relative", "weight": lit(1)}],
             "children": [{"op": "fill", "material": {"role": "floor"}},
                          {"op": "claim", "region": "door", "body": {"op": "void"}},
                          {"op": "split", "axis": "y", "sizes": [
                              {"size": "relative", "weight": lit(1)},
                              {"size": "absolute", "blocks": lit(1)}],
                           "children": [{"op": "fill", "material": {"role": "wall"}},
                                        {"op": "fill", "material": CEIL}]}]},
            {"op": "call", "symbol": "end_wall"}]}
    end_wall = {"op": "split", "axis": "y", "sizes": [
        {"size": "absolute", "blocks": lit(1)}, {"size": "relative", "weight": lit(1)},
        {"size": "absolute", "blocks": lit(1)}],
        "children": [{"op": "fill", "material": {"role": "floor"}},
                     {"op": "fill", "material": {"role": "wall"}},
                     {"op": "fill", "material": CEIL}]}
    body_rows = rows_z(model, range(W), range(H), zs_body)
    if door_z == 0:
        sizes = [{"size": "absolute", "blocks": lit(1)}, {"size": "relative", "weight": lit(1)}]
        children = [door_row, body_rows]
    else:
        sizes = [{"size": "relative", "weight": lit(1)}, {"size": "absolute", "blocks": lit(1)}]
        children = [body_rows, door_row]
    start = marked({"op": "split", "axis": "z", "sizes": sizes, "children": children}, marks)
    return {
        "version": "1.9.0", "name": name, "start": "house",
        "params": {f"{p}/x0": 3, f"{p}/x1": 3, f"{p}/y0": 1, f"{p}/y1": 2},
        "palette": PALETTE,
        "rules": {"house": [{"weight": 1, "body": start}],
                  "end_wall": [{"weight": 1, "body": end_wall}]},
        "contract": {"entry": "house", "spaces": {"house": {"envelope": "enclosed"}},
                     "no_body": {},
                     "edges": [{"a": "exterior", "b": "house", "class": "walk", "via": "door"}]},
        "shown_faces": [],
    }

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "..", "programs")
    os.makedirs(out, exist_ok=True)
    raw = near_model()
    g = resolve_rails(raw)
    near_marks = [("near-skiff", (CX, 1, 11), "north"), ("near-tiller", (CX, 3, TRANSOM), "north"),
                  ("node-near-ferry-house", (2, 1, 8), "south"), ("near-oars", (CX, 1, 7), "south"), ("near-door", (3, 2, 1), "north")]
    gf = resolve_rails(mirror_z(raw))
    f = lambda z: L - 1 - z
    far_marks = [("far-skiff", (CX, 1, f(11)), "south"), ("far-tiller", (CX, 3, f(TRANSOM)), "south"),
                 ("node-far-ferry-house", (2, 1, f(8)), "north"), ("far-oars", (CX, 1, f(7)), "north")]
    for name, gg, edge, dz, marks in (
            ("near-ferry-house", g, "stage-to-near-house", 0, near_marks),
            ("far-ferry-house", gf, "far-house-door", L - 1, far_marks)):
        prog = program(name, gg, edge, dz, marks)
        with open(os.path.join(out, f"{name}.json"), "w") as fh:
            json.dump(prog, fh, indent=2, sort_keys=True); fh.write("\n")
        print("wrote", name)

if __name__ == "__main__":
    main()
