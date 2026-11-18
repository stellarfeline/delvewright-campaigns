#!/usr/bin/env python3
"""The stone Cthulhu in the chasm behind the cat's bridge: the reference level's figure, whole,
turned to face the bridge and re-textured to read against the cave's dark rock.

    python3 den_thing.py > ../../forms/den-thing.json
    delvec sculpt ../../forms/den-thing.json -o <the content prefabs directory>

The figure is `prefab/the-thing-beyond-the-fog`'s form (`references/the-thing-beyond-the-fog/
forms/the-thing-beyond-the-fog.json`: its shape is that level's reviewed shape, read from it, never
redrawn) at its own size and in its own pose: the hooded head, the two eyes, the tentacle beard,
the two wings, the one raised clawed hand. Two things change, neither of them its shape:

- it is turned a quarter to face east, at the bridge and the den's camera (a fragment cannot turn a
  piece with stairs in it, DW0323, so the form itself is turned and sculpted facing east);
- it is re-textured so its silhouette and its face read at a glance, as `design/reference/cat-den`
  has it: a white body (calcite, a little quartz), wings of a paler grey with white bones, dark
  sockets round the eyes, and a tentacle beard of dark prismarine with a sea lantern set in the
  front of each tentacle (the form's lights: a sculpted body never glows, DW0951). The eyes keep
  their own lights.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.normpath(os.path.join(HERE, "../../../../references/the-thing-beyond-the-fog/forms/the-thing-beyond-the-fog.json"))
ID = "prefab/foot-of-the-mountain-den-thing"

BODY = {"family": "quartz", "full": [["minecraft:calcite", 4], ["minecraft:quartz_block", 1]]}
TONES = [BODY, BODY, {"family": "quartz", "full": [["minecraft:calcite", 3], ["minecraft:smooth_quartz", 1]]},
         {"family": "polished_diorite", "full": [["minecraft:calcite", 3], ["minecraft:polished_diorite", 1]]}]
WING = {"family": "polished_diorite", "full": [["minecraft:polished_diorite", 3], ["minecraft:diorite", 1]]}
BONE = {"family": "quartz", "full": [["minecraft:calcite", 1]]}
BEARD = {"family": "dark_prismarine", "full": [["minecraft:dark_prismarine", 3], ["minecraft:prismarine", 1]]}
GLOW = "minecraft:sea_lantern"
SOCKET = {"family": "polished_deepslate", "full": [["minecraft:polished_deepslate", 3], ["minecraft:deepslate_tiles", 1]]}


def role(s):
    """The material a source solid takes: by the family the reference gave it, and for the two
    small ellipsoids that ring the eye sockets at the face's front, the sockets' dark."""
    fam = (s.get("material") or {}).get("family")
    if fam == "dark_prismarine":
        return BEARD
    if fam == "deepslate_tile":
        return WING if s["shape"] == "box" else BONE
    if fam is not None:
        sys.exit(f"den_thing.py: a material of family {fam} the re-texture does not know")
    if s["shape"] == "ellipsoid" and abs(s["centre"][1] - 63) <= 2 and s["centre"][2] >= 24:
        return SOCKET
    return None


def load():
    with open(SOURCE, encoding="utf-8") as f:
        return json.load(f)


def turn(p, width):
    """Body point (x, y, z) facing south -> facing east: x' = z, z' = width - x."""
    x, y, z = p
    return [z, y, width - x]


def turned_form():
    src = load()
    W = src["box"][0]
    out = []
    sockets = 0
    for s in src["solids"]:
        t = dict(s)
        if s["shape"] == "box":
            a, b = turn(s["from"], W), turn(s["to"], W)
            t["from"] = [min(a[i], b[i]) for i in range(3)]
            t["to"] = [max(a[i], b[i]) for i in range(3)]
        elif s["shape"] == "capsule":
            t["from"], t["to"] = turn(s["from"], W), turn(s["to"], W)
        elif s["shape"] == "ellipsoid":
            t["centre"] = turn(s["centre"], W)
            rx, ry, rz = s["radii"]
            t["radii"] = [rz, ry, rx]
        else:
            sys.exit(f"den_thing.py: a solid of shape {s['shape']} the turn does not know")
        m = role(s)
        sockets += m is SOCKET
        if m is None:
            t.pop("material", None)
        else:
            t["material"] = m
        out.append(t)
    if sockets != 2:
        sys.exit(f"den_thing.py: {sockets} eye socket(s) found in the reference's solids, not 2")
    glow = []
    for s in src["solids"]:
        if (s.get("material") or {}).get("family") == "dark_prismarine" and s["shape"] == "capsule":
            # a cell on the tentacle's front face, halfway down it
            a, b = s["from"], s["to"]
            r = min(s["radius_from"], s["radius_to"])
            mid = [round((a[0] + b[0]) / 2), round((a[1] + b[1]) / 2), int((a[2] + b[2]) / 2 + r - 0.5)]
            glow.append({"at": mid, "block": GLOW})
    if len(glow) != 24:
        sys.exit(f"den_thing.py: {len(glow)} tentacle(s) in the reference's beard, not 24")
    lights = sorted({json.dumps({"at": turn(l["at"], W - 1), "block": l["block"].replace("axis=x", "axis=z")},
                                sort_keys=True) for l in src["lights"] + glow})
    ax, ay, az = src["anchors"]["anchor/foot"]["pos"]
    fx, _, fz = turn([ax, ay, az], W - 1)
    return {
        "form_version": src["form_version"], "id": ID, "box": [src["box"][2], src["box"][1], src["box"][0]],
        "sub": src["sub"], "ground": src["ground"], "sink": src["sink"], "noise": src["noise"], "palette": TONES,
        "solids": out, "lights": [json.loads(l) for l in lights],
        "anchors": {"anchor/foot": {"facing": "east", "pos": [fx, ay, fz], "role": "entry"}},
    }


if __name__ == "__main__":
    print(json.dumps(turned_form(), indent=2, sort_keys=True))
