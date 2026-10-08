"""The Figure: the demo level The Thing Beyond the Fog's form, turned to face east.

Reads the demo's committed form (content branch demo/the-thing-beyond-the-fog,
demos/the-thing-beyond-the-fog/forms/the-thing-beyond-the-fog.json, passed as
argv[1]) and writes forms/the-stranding-figure.json: every solid, light and
anchor turned a quarter about the vertical so the face that looked south
(+z) looks east (+x). A stamped prefab may not be rotated (DW0323: its stairs
and slabs carry facings), so the turn is made in the form, before the sculpt
derives any block.

    new x = old z,   new z = (X - old x),   X = the old box's x extent
"""
import json, sys, os
src = json.load(open(sys.argv[1]))
X, Y, Z = src["box"]
def p(v):  # a continuous point
    return [round(v[2], 4), v[1], round(X - v[0], 4)]
def cell(v):  # a cell [x,y,z] spanning x..x+1
    return [v[2], v[1], X - 1 - v[0]]
out = dict(src)
out["id"] = "prefab/the-stranding-figure"
out["box"] = [Z, Y, X]
solids = []
for s in src["solids"]:
    s = dict(s)
    if s["shape"] == "box":
        a, b = p(s["from"]), p(s["to"])
        s["from"] = [min(a[i], b[i]) for i in range(3)]
        s["to"] = [max(a[i], b[i]) for i in range(3)]
    elif s["shape"] == "capsule":
        s["from"], s["to"] = p(s["from"]), p(s["to"])
    elif s["shape"] == "ellipsoid":
        s["centre"] = p(s["centre"])
        r = s["radii"]; s["radii"] = [r[2], r[1], r[0]]
    else:
        raise SystemExit(f"unknown shape {s['shape']}")
    solids.append(s)
out["solids"] = solids
lights = []
for l in src["lights"]:
    l = dict(l)
    l["at"] = cell(l["at"])
    l["block"] = l["block"].replace("axis=x", "axis=Z").replace("axis=z", "axis=x").replace("axis=Z", "axis=z")
    lights.append(l)
out["lights"] = lights
turn = {"south": "east", "east": "north", "north": "west", "west": "south"}
anchors = {}
for k, a in src["anchors"].items():
    a = dict(a); a["pos"] = cell(a["pos"]); a["facing"] = turn[a["facing"]]
    anchors[k] = a
out["anchors"] = anchors
here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "..", "forms", "the-stranding-figure.json"), "w") as fh:
    json.dump(out, fh, indent=2, sort_keys=True); fh.write("\n")
print("wrote forms/the-stranding-figure.json", out["box"])
