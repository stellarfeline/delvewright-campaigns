"""The body on its bank: a rotting sperm whale, written as a sculpt form.

Writes forms/the-stranding-body.json and generators/body_place.json. Sculpt
with `delvec sculpt forms/the-stranding-body.json -o <library>`; the piece is
stamped by world-edits.json (batch/the-body).

The body is the demo level The Beached Thing's whale (its form, its tones,
its rules for reading at a distance; the citations are in that demo's
README) laid over the site plan's own places on the far bank: every place
of the bank is cut out of the form, so the stamp never writes into a play
space, and every seam between two of them is cut through the wall between,
so no doorway is filled. The boxes come from `delvec allocation`, asked
afresh on every run (argv[1] is the delvec binary, argv[2] the prefab
library), so the form follows the plan.

Run from the campaign directory:
    python3 generators/body_form.py "$(command -v delvec)" ../../prefabs
"""
import json, os, subprocess, sys

DELVEC, PREFABS = sys.argv[1], sys.argv[2]
here = os.path.dirname(os.path.abspath(__file__))
camp = os.path.abspath(os.path.join(here, ".."))

# --- the piece's frame in the world ----------------------------------------
X0, Y0, Z0 = 110, 59, 575          # piece origin (world)
BOX = [76, 61, 296]                # x 110..185, y 59..119, z 575..870
GROUND_TOP = 4                     # piece y 4 = world 63, the bank's mud course
SINK = 0                           # body y 0 = piece y 5 = world 64
def B(wx, wy, wz):                 # world -> body frame
    return [wx - X0, wy - 64, wz - Z0]
def P(wx, wy, wz):                 # world -> piece frame
    return [wx - X0, wy - Y0, wz - Z0]

PLACES = ["far-landing", "jaw-bank", "flank-ridge", "mouth", "throat", "rib-cathedral",
          "stomach", "heart-chamber", "breach", "spine-stair", "crown", "brow",
          "back-upper", "back-middle", "back-lower", "tail-flank", "tail-bank", "tail-road",
          "far-ferry-house"]
INSIDE = {"mouth", "throat", "rib-cathedral", "stomach", "heart-chamber", "breach", "spine-stair"}
OPEN = {"far-landing", "jaw-bank", "flank-ridge", "crown", "brow", "back-upper", "back-middle",
        "back-lower", "tail-flank", "tail-bank", "tail-road"}

def allocation(place):
    out = subprocess.run([DELVEC, "--prefabs", PREFABS, "allocation", camp, f"node/{place}"],
                         check=True, capture_output=True, text=True).stdout
    return json.loads(out)

alloc = {p: allocation(p) for p in PLACES}

# --- tones (The Beached Thing's) --------------------------------------------
HIDE = {"family": "deepslate_tile", "full": [["minecraft:gray_concrete", 1]]}
LOWER = {"family": "polished_blackstone", "full": [["minecraft:gray_terracotta", 1]]}
SLOUGH = {"family": "stone", "full": [["minecraft:light_gray_concrete", 1]]}
FLUKE = {"family": "cobbled_deepslate", "full": [["minecraft:cyan_terracotta", 1]]}
BONE = {"family": "pale_oak", "full": [["minecraft:bone_block", 6], ["minecraft:calcite", 1]]}
FLESH = {"family": "polished_granite", "full": [["minecraft:red_terracotta", 4], ["minecraft:brown_terracotta", 2],
                                               ["minecraft:pink_terracotta", 1], ["minecraft:nether_wart_block", 1]]}
MUD = {"family": "mud_brick", "full": [["minecraft:packed_mud", 3], ["minecraft:coarse_dirt", 1], ["minecraft:rooted_dirt", 1]]}

solids = []
def capsule(a, b, r0, r1, mat, stretch=None, noisy=True):
    s = {"shape": "capsule", "op": "add", "from": B(*a), "to": B(*b), "radius_from": r0, "radius_to": r1,
         "material": mat, "noisy": noisy}
    if stretch: s["stretch_y"] = stretch
    solids.append(s)
def ellipsoid(c, r, mat, noisy=True):
    solids.append({"shape": "ellipsoid", "op": "add", "centre": B(*c), "radii": r, "material": mat, "noisy": noisy})
def box(a, b, mat=None, op="add"):
    s = {"shape": "box", "op": op, "from": B(*a), "to": B(*b)}
    if op == "cut":
        # The octant fit dilates a solid by half a block at its faces, so a cut
        # is drawn half a block wider and higher than the cells it frees, and a
        # fifth of a block below the floor it stands on: at sub 4 that frees
        # every cell of the box and leaves the floor course whole (measured on
        # a test form; GENERATION.md round 5).
        s["from"] = [s["from"][0] - 0.5, s["from"][1] - 0.2, s["from"][2] - 0.5]
        s["to"] = [s["to"][0] + 0.5, s["to"][1] + 0.5, s["to"][2] + 0.5]
    if mat: s["material"] = mat
    solids.append(s)

# --- the head: the front third, a tall squared block, blunt in front --------
# core, then its long edges rounded by capsules (the squared sperm-whale head)
box((131, 58, 600), (170, 104, 690), HIDE)
for (x, y) in ((131, 99), (169, 99), (131, 70), (169, 70)):
    capsule((x, y, 604), (x, y, 690), 6.0, 6.5, HIDE)
capsule((150, 99, 604), (150, 99, 690), 6.0, 6.0, HIDE)
# the brow's bulge over the front, the blowhole ridge to the left of the crown
ellipsoid((150, 90, 606), [20.0, 16.0, 8.0], HIDE)
capsule((141, 104, 660), (141, 104, 672), 1.6, 1.2, SLOUGH, noisy=False)
# --- the trunk: widest behind the head, sagging and spread on the mud --------
stations = [  # (z, x centre, y centre, radius, vertical stretch)
    (690, 150, 70, 30.0, 1.4), (740, 149, 68, 29.0, 1.35), (790, 148, 66, 24.0, 1.3),
    (830, 146, 65, 19.0, 1.2), (852, 146, 64, 6.0, 1.0)]
for (z0, x0, y0, r0, s0), (z1, x1, y1, r1, s1) in zip(stations, stations[1:]):
    capsule((x0, y0, z0), (x1, y1, z1), r0, r1, HIDE, stretch=(s0 + s1) / 2)
# the lower flanks spread on the mud: a darker, browner grey
for (z0, z1, r0, r1) in ((700, 760, 31.0, 30.0), (760, 820, 30.0, 22.0)):
    capsule((149, 62, z0), (148, 62, z1), r0, r1, LOWER, stretch=0.5)
# the spine ridge over the stair up the inside of the back (east side)
capsule((164, 105, 698), (164, 104, 768), 7.0, 7.0, HIDE)
# --- flippers, the jaw, the flukes ------------------------------------------
capsule((172, 64, 712), (183, 63, 724), 3.3, 1.4, HIDE)           # east flipper, splayed on the mud
capsule((163, 64, 600), (172, 64, 583), 2.2, 1.7, BONE, noisy=False)  # the lower jaw, bare bone, swung east
for i in range(8):
    z = 598 - i * 2.0; x = 163 + (172 - 163) * (i * 2.0) / 17.0
    capsule((x - 1.0, 65.5, z), (x - 1.3, 66.6, z), 0.55, 0.3, BONE, noisy=False)  # teeth
for side in (-1, 1):
    capsule((146, 64, 842), (146 + side * 26, 64, 846), 4.0, 1.0, FLUKE, stretch=0.4)
    capsule((146, 64, 842), (146 + side * 22, 64, 838), 3.6, 1.0, FLUKE, stretch=0.4)
# --- the three wounds on the west flank, over the ridge, and sloughed skin ---
for z in (615, 655, 695):
    ellipsoid((128, 74, z), [3.0, 4.5, 4.0], FLESH)
for (c, r) in (((150, 104, 640), [8.0, 1.5, 10.0]), ((136, 100, 720), [6.0, 1.5, 9.0]),
               ((131, 92, 668), [3.0, 6.0, 8.0])):
    ellipsoid(c, r, SLOUGH, noisy=False)
# --- the inside: flesh lining round every inside place ----------------------
def frame(place):
    a = alloc[place]; m = a["world_min"]; e = a["extent"]
    return m, [m[i] + e[i] - 1 for i in range(3)], a["datum_y"]
for place in sorted(INSIDE):
    lo, hi, d = frame(place)
    box((lo[0] - 1, lo[1] - 1, lo[2] - 1), (hi[0] + 2, hi[1] + 2, hi[2] + 2), FLESH)
# --- cut: every place's play space, and every seam's way through the wall ---
for place in PLACES:
    lo, hi, d = frame(place)
    top = BOX[1] + Y0 + 5 if place in OPEN else hi[1] + 1
    box((lo[0], lo[1] + d, lo[2]), (hi[0] + 1, top, hi[2] + 1), op="cut")
cells = {}
for place in PLACES:
    a = alloc[place]; m = a["world_min"]
    for s in a["seams"]:
        cells.setdefault(s["edge"], []).extend([m[0] + c[0], m[1] + c[1], m[2] + c[2]] for c in s["cells"])
for edge in sorted(cells):
    cs = cells[edge]
    lo = [min(c[i] for c in cs) for i in range(3)]; hi = [max(c[i] for c in cs) for i in range(3)]
    box(tuple(lo), (hi[0] + 1, hi[1] + 1, hi[2] + 1), op="cut")

# --- light set into the inside surfaces (interior-lighting.md sec. 7) -------
lights = []
for place in sorted(INSIDE):
    lo, hi, d = frame(place)
    within = {"from": B(lo[0] - 1, lo[1] + d - 1, lo[2] - 1), "to": B(hi[0] + 1, hi[1] + 1, hi[2] + 1)}
    lights.append({"block": "minecraft:soul_lantern[hanging=false,waterlogged=false]",
                   "hull": {"mode": "recessed", "cover": "minecraft:polished_granite_stairs",
                            "on": ["wall", "vault"], "spacing": 3.0, "within": within}})

form = {"form_version": "1.0.0", "id": "prefab/the-stranding-body", "box": BOX,
        "ground": {"block": "minecraft:packed_mud", "top": GROUND_TOP}, "sink": SINK, "sub": 4,
        "noise": {"amplitude": 0.5, "cell": 2.5},
        "palette": [SLOUGH, HIDE, LOWER, LOWER],
        "anchors": {"anchor/entry": {"pos": P(144, 64, 590), "facing": "south", "role": "entry"}},
        "solids": solids, "lights": lights}
os.makedirs(os.path.join(camp, "forms"), exist_ok=True)
with open(os.path.join(camp, "forms", "the-stranding-body.json"), "w") as f:
    json.dump(form, f, indent=2, sort_keys=True); f.write("\n")
# where world-edits stamps it: the piece origin relative to the far landing's anchor
ANCHOR, AW = "anchor/node-far-landing", (177, 64, 576)
with open(os.path.join(here, "body_place.json"), "w") as f:
    json.dump({"anchor": ANCHOR, "anchor_world": list(AW), "at": [X0 - AW[0], Y0 - AW[1], Z0 - AW[2]]},
              f, indent=2, sort_keys=True); f.write("\n")
print("wrote forms/the-stranding-body.json:", len(solids), "solids,", len(lights), "lights")
