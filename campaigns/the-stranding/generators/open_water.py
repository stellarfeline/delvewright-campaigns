"""The skiff out on the open water: the ferry houses' skiff, turned to lie east-west.

Writes pieces/the-stranding-sea-skiff.json, a grammar program expanded into the
prefab library and stamped as a fragment on node/open-water (world-edits.json):
a place reached only by the carry has no way in a spatial contract can state,
so it is massed by the plan and its boat is stamped over the massing. The boat is ferry_house.skiff() block for
block, its long axis laid along x with the bow to the west (toward what
stands in the sea) and its beam along z; it rides on the black water, so
every cell of the floor course round the hull is sea water, and its rail
runs all the way round (nobody steps off it into the open sea).

Run from the campaign directory:  python3 generators/open_water.py
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import ferry_house as fh
from voxgrammar import rows_z, marked

W, H, L = 16, 5, 12
CZ = 5
def to_house(x, z):
    """Sea frame (x, z) -> the house frame's (x, z) of the same skiff cell."""
    return (z - CZ + fh.CX, x + 2)

def sea_model():
    g = {}
    for x in range(W):
        for y in range(H):
            for z in range(L):
                g[(x, y, z)] = fh.WATER if y == 0 else None
    turn = {"east": "south", "west": "north"}
    for x in range(W):
        for z in range(L):
            hx, hz = to_house(x, z)
            for y in range(4):
                b = fh.skiff(hx, y, hz)
                if b is None: continue
                if b == fh.STEP: b = fh.STRAKE           # no boarding gap out here
                if isinstance(b, str) and "facing=" in b:
                    for a, c in turn.items():
                        if f"facing={a}" in b:
                            b = b.replace(f"facing={a}", f"facing={c}"); break
                g[(x, y, z)] = b
    # the rail closes the boarding gap too
    for x in range(W):
        for z in range(L):
            hx, hz = to_house(x, z)
            if hz in (6, 7) and hx == fh.BX0:
                g[(x, 2, z)] = "RAIL"
    # the oar out over the water on the south side at the rowing thwart
    g[(5, 2, 8)] = "RAIL"
    return g

def claims(x, y, z):
    return None

def main():
    g = fh.resolve_rails(sea_model())
    def model(x, y, z):
        return (g[(x, y, z)], claims(x, y, z))
    body = rows_z(model, range(W), range(H), range(L))
    marks = [("sea-skiff", (8, 1, CZ), "west"), ("sea-oars", (5, 1, CZ), "east"),
             ("node-open-water", (6, 1, CZ), "west")]
    prog = {"version": "1.9.0", "name": "the-stranding-sea-skiff", "start": "sea",
            "params": {}, "palette": {},
            "rules": {"sea": [{"weight": 1, "body": marked(body, marks)}]},
            "shown_faces": ["up", "north", "south", "east", "west"]}
    here = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(here, "..", "pieces"), exist_ok=True)
    with open(os.path.join(here, "..", "pieces", "the-stranding-sea-skiff.json"), "w") as f:
        json.dump(prog, f, indent=2, sort_keys=True); f.write("\n")
    print("wrote pieces/the-stranding-sea-skiff.json")

if __name__ == "__main__":
    main()
