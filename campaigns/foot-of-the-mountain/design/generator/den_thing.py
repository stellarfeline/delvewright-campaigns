#!/usr/bin/env python3
"""The stone Cthulhu in the chasm behind the cat's bridge: the reference level's figure, turned to
face the bridge, set to the chasm's size and re-textured pale.

    python3 den_thing.py > ../../forms/den-thing.json
    delvec sculpt ../../forms/den-thing.json -o <the content prefabs directory>

The figure is `prefab/the-thing-beyond-the-fog`'s form (`references/the-thing-beyond-the-fog/
forms/the-thing-beyond-the-fog.json`: its shape is that level's reviewed shape, read from it, never
redrawn). Three things change, none of them its shape:

- it is turned a quarter to face east, at the bridge (a fragment cannot turn a piece with stairs in
  it, DW0323, so the form itself is turned and sculpted facing east);
- it is set to `SCALE` of its size, so its raised wing and its claws stand inside the cave (the
  chasm is 79 cells along the bridge; the figure's 91 would stand in its walls);
- it is re-textured pale, as `design/reference/cat-den` has it against the cave's dark rock: the
  form's tones and its solids' materials become diorite, calcite, smooth stone and pale stone brick
  with moss, and its eyes' lights become sea lanterns, cold blue-white.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.normpath(os.path.join(HERE, "../../../../references/the-thing-beyond-the-fog/forms/the-thing-beyond-the-fog.json"))
SCALE = 0.78
ID = "prefab/foot-of-the-mountain-den-thing"

PALE = {
    None: None,
    "deepslate_tile": {"family": "polished_diorite", "full": [["minecraft:polished_diorite", 3], ["minecraft:calcite", 2],
                                                                ["minecraft:smooth_stone", 1]]},
    "dark_prismarine": {"family": "mossy_stone_brick", "full": [["minecraft:calcite", 3], ["minecraft:mossy_stone_bricks", 2],
                                                                  ["minecraft:moss_block", 1]]},
}
TONES = [
    {"family": "diorite", "full": [["minecraft:calcite", 3], ["minecraft:diorite", 2]]},
    {"family": "polished_diorite", "full": [["minecraft:polished_diorite", 3], ["minecraft:calcite", 1]]},
    {"family": "stone_brick", "full": [["minecraft:stone_bricks", 2], ["minecraft:smooth_stone", 2], ["minecraft:diorite", 1]]},
    {"family": "mossy_stone_brick", "full": [["minecraft:mossy_stone_bricks", 2], ["minecraft:moss_block", 1],
                                             ["minecraft:stone_bricks", 2]]},
]
EYE = "minecraft:sea_lantern"


def load():
    with open(SOURCE, encoding="utf-8") as f:
        return json.load(f)


def turn(p, width):
    """Body point (x, y, z) facing south -> facing east, scaled: x' = z, z' = width - x."""
    x, y, z = p
    return [round(z * SCALE, 3), round(y * SCALE, 3), round((width - x) * SCALE, 3)]


def turned_form():
    src = load()
    W = src["box"][0]
    out = []
    for s in src["solids"]:
        t = dict(s)
        if s["shape"] == "box":
            a, b = turn(s["from"], W), turn(s["to"], W)
            t["from"] = [min(a[i], b[i]) for i in range(3)]
            t["to"] = [max(a[i], b[i]) for i in range(3)]
        elif s["shape"] == "capsule":
            t["from"], t["to"] = turn(s["from"], W), turn(s["to"], W)
            t["radius_from"] = round(s["radius_from"] * SCALE, 3)
            t["radius_to"] = round(s["radius_to"] * SCALE, 3)
        elif s["shape"] == "ellipsoid":
            t["centre"] = turn(s["centre"], W)
            rx, ry, rz = s["radii"]
            t["radii"] = [round(rz * SCALE, 3), round(ry * SCALE, 3), round(rx * SCALE, 3)]
        else:
            sys.exit(f"den_thing.py: a solid of shape {s['shape']} the turn does not know")
        if "material" in s:
            fam = s["material"].get("family")
            if fam not in PALE:
                sys.exit(f"den_thing.py: a material of family {fam} the re-texture does not know")
            t["material"] = PALE[fam]
        out.append(t)
    lights = []
    for l in src["lights"]:
        p = turn(l["at"], W - 1)
        lights.append({"at": [int(round(v)) for v in p], "block": EYE})
    box = [int(-(-src["box"][2] * SCALE // 1)), int(-(-src["box"][1] * SCALE // 1)), int(-(-src["box"][0] * SCALE // 1))]
    ax, ay, az = src["anchors"]["anchor/foot"]["pos"]
    foot = turn([ax, ay, az], W - 1)
    form = {
        "form_version": src["form_version"], "id": ID, "box": box, "sub": src["sub"], "ground": src["ground"],
        "sink": src["sink"], "noise": src["noise"], "palette": TONES, "solids": out,
        "lights": sorted({json.dumps(l, sort_keys=True) for l in lights}),
        "anchors": {"anchor/foot": {"facing": "east", "pos": [int(round(foot[0])), ay, int(round(foot[2]))], "role": "entry"}},
    }
    form["lights"] = [json.loads(l) for l in form["lights"]]
    return form


if __name__ == "__main__":
    print(json.dumps(turned_form(), indent=2, sort_keys=True))
