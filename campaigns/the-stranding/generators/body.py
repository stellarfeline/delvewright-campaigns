"""The Fathomer: the body form (`forms/the-stranding-body.json`), sculpted by
`delvec sculpt` into `prefab/the-stranding-body`, stamped over the bank by the
world-edits script, and sliced for the places that stand on it.

A rotting sperm whale (DESIGN.md, The body): a tall square blunt head a third of
the length, the Brow Stone in its face; a low hump and knuckles toward the tail;
small flippers splayed; broad flukes laid flat; three wounds torn in the west
flank with pale ribs in them. Every place inside the body is cut out of the form
as its whole claim, so that place's own piece draws the inside of the body; the
places on the body's outside are slices of the sculpted piece.

Run: python3 generators/body.py           (writes the form and sculpts it)
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CAMPAIGN = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import mapmodel as M  # noqa: E402

# the piece's frame in the world: piece (0,0,0) is world ORIGIN; the apron is
# piece y 0 (world 61, buried under the bank); body y 0 is world 62
ORIGIN = (148, 61, 521)
BOX = (63, 52, 144)          # x 148..210, y 61..112, z 521..664
BODY_Y0 = 62
FORM = os.path.join(CAMPAIGN, "forms", "the-stranding-body.json")
PID = "prefab/the-stranding-body"

ROOF_WOUNDS = ((192, 583), (194, 601))
INSIDE = ["node/mouth", "node/throat", "node/rib-cathedral", "node/stomach",
          "node/heart-chamber", "node/breach", "node/spine-stair", "node/spine-top"]
OUTSIDE = ["node/crown", "node/brow", "node/back-upper", "node/back-middle",
           "node/back-lower", "node/tail-flank"]


def b(x, y, z):
    """world (continuous) -> body frame"""
    return [round(x - ORIGIN[0], 3), round(y - BODY_Y0, 3), round(z - ORIGIN[2], 3)]


def box(x0, y0, z0, x1, y1, z1, op="add", material=None, noisy=False):
    """cells x0..x1, y0..y1, z0..z1 inclusive (world)"""
    s = {"shape": "box", "op": op, "from": b(x0, y0, z0), "to": b(x1 + 1, y1 + 1, z1 + 1), "noisy": noisy}
    if material:
        s["material"] = material
    return s


def capsule(p0, p1, r0, r1, stretch=1.0, op="add", material=None, noisy=True):
    s = {"shape": "capsule", "op": op, "from": b(*p0), "to": b(*p1), "radius_from": r0,
         "radius_to": r1, "stretch_y": stretch, "noisy": noisy}
    if material:
        s["material"] = material
    return s


def ellipsoid(c, r, op="add", material=None, noisy=True):
    s = {"shape": "ellipsoid", "op": op, "centre": b(*c), "radii": list(r), "noisy": noisy}
    if material:
        s["material"] = material
    return s


# the hide, bleached to weathered (dark grey-brown, wrinkled)
PALETTE = [
    {"family": "tuff", "full": [["minecraft:tuff", 3], ["minecraft:polished_tuff", 1], ["minecraft:andesite", 1]]},
    {"family": "cobbled_deepslate", "full": [["minecraft:cobbled_deepslate", 3], ["minecraft:tuff", 2]]},
    {"family": "cobbled_deepslate", "full": [["minecraft:deepslate", 3], ["minecraft:cobbled_deepslate", 2], ["minecraft:mud_bricks", 1]]},
    {"family": "blackstone", "full": [["minecraft:blackstone", 2], ["minecraft:deepslate_tiles", 2], ["minecraft:cracked_deepslate_tiles", 1]]},
]
FLESH = {"family": "red_nether_brick", "full": [["minecraft:red_nether_bricks", 2], ["minecraft:nether_wart_block", 2], ["minecraft:red_terracotta", 1]]}
BONE = {"family": "smooth_quartz", "full": [["minecraft:bone_block", 3], ["minecraft:calcite", 1]]}
STONE_TABLET = {"family": "quartz", "full": [["minecraft:chiseled_quartz_block", 2], ["minecraft:quartz_block", 1]]}
EYE = {"family": "blackstone", "full": [["minecraft:blackstone", 1]]}


def claim_box(nid):
    """The cells a place claims: footprint + ring, from its bottom to its top."""
    p = M.P[nid]
    fy = M.fy(p)
    kind, n = p["ceiling"]
    bottom = fy - 1
    if not p["base"]:
        bottom = min(fy - 1, M.terrain(p["x"], p["z"]))
    top = fy + n - 1
    if kind == "clearance":
        top = fy + n  # the lid
        if p["roof"]:
            top += p["roof"]["courses"]
    return (p["x"] - 1, bottom, p["z"] - 1, M.x1(p) + 1, top, M.z1(p) + 1)


def solids():
    S = []
    # -- the head: tall, square and blunt; its top flat at y 103 under the crown
    S.append(box(153, 62, 521, 207, 95, 562))
    S.append(box(155, 96, 521, 205, 103, 562))
    S.append(capsule((157, 95, 523), (157, 95, 560), 3.5, 3.5, 1.0, noisy=False))
    S.append(capsule((203, 95, 523), (203, 95, 560), 3.5, 3.5, 1.0, noisy=False))
    # wrinkled hide over the head's flanks below the top
    for x in (155.5, 204.5):
        S.append(capsule((x, 78, 526), (x, 78, 558), 4.0, 4.0, 3.5, noisy=True))
    # the flanks fall sheer to the mud, so nothing overhangs the ground
    S.append(box(151, 62, 522, 153, 79, 561, noisy=True))
    S.append(box(207, 62, 522, 209, 79, 561, noisy=True))
    # -- the back: a low hump falling in steps toward the tail
    S.append(capsule((180, 62, 563), (180, 62, 590), 30, 30, 38 / 30, noisy=True))
    S.append(capsule((180, 62, 590), (180, 62, 619), 29.5, 28, 34 / 29.5, noisy=True))
    S.append(capsule((180, 62, 619), (180, 62, 646), 27, 21, 24 / 27, noisy=True))
    S.append(capsule((180, 62, 646), (180, 62, 664), 15, 8, 8 / 15, noisy=True))
    # the spine walk: each place on the back stands on a flat course of hide
    for nid, (fl,) in (("node/back-upper", (100,)), ("node/back-middle", (96,)),
                       ("node/back-lower", (86,)), ("node/tail-flank", (70,))):
        p = M.P[nid]
        S.append(box(p["x"] - 1, fl - 6, p["z"] - 1, M.x1(p) + 1, fl - 1, M.z1(p) + 1, noisy=False))
    # the knuckles along the spine toward the tail
    for z in (628, 634, 640):
        S.append(capsule((187.5, 76, z), (187.5, 84, z), 2.0, 1.2, 1.0, noisy=False))
    # the flank stands thick beside the heart, so its chamber is walled, not shelled
    S.append(box(150, 62, 600, 156, 77, 640, noisy=True))
    # -- the flippers, splayed on the mud
    S.append(capsule((154, 65, 584), (149, 63, 597), 3.0, 1.5, 0.5, noisy=False))
    S.append(capsule((206, 65, 584), (210, 63, 597), 3.0, 1.5, 0.5, noisy=False))
    # -- the flukes, laid flat on the mud
    S.append(capsule((180, 63, 652), (163, 63, 663), 4.0, 1.5, 0.45, noisy=False))
    S.append(capsule((180, 63, 652), (197, 63, 663), 4.0, 1.5, 0.45, noisy=False))
    # -- the eyes, small and low at the back of the head, shut
    S.append(ellipsoid((153.2, 70, 556), (1.2, 1.0, 1.6), material=EYE, noisy=False))
    S.append(ellipsoid((206.8, 70, 556), (1.2, 1.0, 1.6), material=EYE, noisy=False))
    # -- the three wounds torn in the west flank: red flesh, pale ribs standing out
    for z in (548, 572, 596):
        S.append(ellipsoid((152, 74, z), (3.5, 6.5, 5.0), op="cut", noisy=True))
        S.append(ellipsoid((153.5, 74, z), (2.0, 5.5, 4.0), material=FLESH, noisy=True))
        for dz in (-2.5, 0, 2.5):
            S.append(capsule((151.5, 69, z + dz), (151.5, 79, z + dz), 0.7, 0.7, 1.0, material=BONE, noisy=False))
    # wounds torn along the back, the cathedral's two roof wounds among them
    for (x, z) in ROOF_WOUNDS:
        S.append(capsule((x, 85, z), (x, 101, z), 3.0, 3.8, 1.0, op="cut", noisy=True))
    S.append(ellipsoid((196, 92, 576), (3.0, 1.8, 4.0), op="cut", noisy=True))
    S.append(ellipsoid((196, 91.5, 576), (2.0, 1.5, 3.0), material=FLESH, noisy=True))
    # -- every place inside the body is cut out whole: its own piece draws it
    # one cell wider than the claim all round: the sculpt dresses a cut's faces
    # with slabs and stairs in the cells just inside it, and the stamp would lay
    # those over the place's own walls and lid
    # Where a place opens out of the body (the mouth's front, the breach) the
    # wider cut would leave a gap round its walls open to the outside, so there
    # the cut is the claim itself.
    def cut(x0, y0, z0, x1, y1, z1):
        S.append(box(max(x0, ORIGIN[0]), max(y0, BODY_Y0), max(z0, ORIGIN[2]),
                     min(x1, ORIGIN[0] + BOX[0] - 1), y1, min(z1, ORIGIN[2] + BOX[2] - 1), op="cut"))

    for nid in INSIDE:
        x0, y0, z0, x1, y1, z1 = claim_box(nid)
        if nid == "node/breach":
            cut(x0, y0, z0, x1, y1, z1)
        elif nid == "node/mouth":
            cut(x0, y0, z0, x1, y1, z0 + 2)
            cut(x0 - 1, y0, z0 + 3, x1 + 1, y1 + 1, z1 + 1)
        else:
            cut(x0 - 1, y0, z0 - 1, x1 + 1, y1 + 1, z1 + 1)
    # the Brow Stone: a tall pale carved tablet driven into the forehead
    S.append(box(172, 99, 521, 175, 102, 521, material=STONE_TABLET))
    return S


def form():
    return {
        "form_version": "1.0.0",
        "id": PID,
        "box": list(BOX),
        "sub": 2,
        "ground": {"block": "minecraft:packed_mud", "top": 0},
        "sink": 0,
        "noise": {"amplitude": 0.8, "cell": 6.0},
        "palette": PALETTE,
        "solids": solids(),
        "lights": [],
        "anchors": {
            "anchor/body-foot": {"pos": [1, 1, 1], "facing": "south", "role": "entry"},
        },
    }


def write_form():
    os.makedirs(os.path.dirname(FORM), exist_ok=True)
    with open(FORM, "w") as f:
        json.dump(form(), f, indent=2, sort_keys=True)
        f.write("\n")


def sculpt():
    out = subprocess.run(["delvec", "--prefabs", os.environ["DELVEWRIGHT_PREFABS"], "sculpt", FORM,
                          "-o", os.environ["DELVEWRIGHT_PREFABS"], "--seed", "1919"],
                         capture_output=True, text=True)
    sys.stdout.write(out.stdout[-6000:])
    sys.stderr.write(out.stderr[-6000:])
    return out.returncode


_CELLS = None


def cells():
    """the sculpted piece, keyed by WORLD cell"""
    global _CELLS
    if _CELLS is None:
        import nbtio
        c, size, meta = nbtio.read_piece(os.environ["DELVEWRIGHT_PREFABS"], PID)
        _CELLS = {(x + ORIGIN[0], y + ORIGIN[1], z + ORIGIN[2]): st for (x, y, z), st in c.items()}
    return _CELLS


if __name__ == "__main__":
    write_form()
    if "--no-sculpt" not in sys.argv:
        sys.exit(sculpt())
