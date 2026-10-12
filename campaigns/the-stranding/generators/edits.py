"""The world-edits script: the body stamped over its bank, and the ground of the
town dressed where the site's single fill block (mud) would be wrong.

Run: python3 generators/edits.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CAMPAIGN = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import mapmodel as M  # noqa: E402
import body  # noqa: E402

ANCHOR = "anchor/node-jaw-bank"


def rel(world):
    a = M.anchor_pos(ANCHOR)
    return [world[0] - a[0], world[1] - a[1], world[2] - a[2]]


def under_the_mud():
    """the sea standing under each mud field's crust, which the sinking clears"""
    out = []
    for nid, p in M.P.items():
        if not nid.startswith("node/mud-"):
            continue
        name = "region/under-" + nid[len("node/"):]
        out.append({"verb": "select", "name": name,
                    "shape": {"kind": "box", "frame": {"kind": "anchor-relative", "anchor": ANCHOR},
                              "min": rel((p["x"], 59, p["z"])), "max": rel((M.x1(p), 62, M.z1(p)))}})
        out.append({"verb": "fill", "region": name,
                    "recipe": {"blocks": [{"block": "minecraft:water", "weight": 1.0}]}})
        # the stones of the field's steps: under its ring and its first row
        # inside, one course under the crust (what the mud field's piece leaves
        # open over them is a step a swimmer climbs out by)
        x0, z0, x1, z1 = p["x"] - 1, p["z"] - 1, M.x1(p) + 1, M.z1(p) + 1
        for k, (a, b) in enumerate([((x0, z0), (x1, z0 + 1)), ((x0, z1 - 1), (x1, z1)),
                                    ((x0, z0), (x0 + 1, z1)), ((x1 - 1, z0), (x1, z1))]):
            rn = "%s-step-%d" % (name, k)
            out.append({"verb": "select", "name": rn,
                        "shape": {"kind": "box", "frame": {"kind": "anchor-relative", "anchor": ANCHOR},
                                  "min": rel((a[0], 62, a[1])), "max": rel((b[0], 62, b[1]))}})
            out.append({"verb": "fill", "region": rn,
                        "recipe": {"blocks": [{"block": "minecraft:packed_mud", "weight": 3.0},
                                              {"block": "minecraft:mud", "weight": 1.0}]}})
    return out


def batches():
    out = []
    # the sea stands in every hollow of the site under its level: the open
    # fill lays the heightmap's ground and nothing over it, so the channels,
    # the harbour mouth and the water beside the Narrows are flooded here
    lo = (0, 31, 0)
    hi = (399, 62, 759)
    out.append({
        "id": "batch/the-sea",
        "area": "area/site",
        "note": "The sea in every hollow of the site below its level (y 62): the black water either side of the flat, the channel to the body, the harbour mouth.",
        "edits": [
            {"verb": "select", "name": "region/the-site",
             "shape": {"kind": "box", "frame": {"kind": "anchor-relative", "anchor": ANCHOR},
                       "min": rel(lo), "max": rel((hi[0], 200, hi[2]))}},
            {"verb": "select", "name": "region/under-sea-level",
             "shape": {"kind": "box", "frame": {"kind": "anchor-relative", "anchor": ANCHOR},
                       "min": rel(lo), "max": rel(hi)}},
            {"verb": "select", "name": "region/over-the-ground",
             "shape": {"kind": "surface-band", "over": "region/the-site", "from": 1, "to": 31}},
            {"verb": "select", "name": "region/the-sea",
             "shape": {"kind": "intersect", "of": ["region/over-the-ground", "region/under-sea-level"]}},
            {"verb": "fill", "region": "region/the-sea",
             "recipe": {"blocks": [{"block": "minecraft:water", "weight": 1.0}]}},
        ] + under_the_mud(),
    })
    out.append({
        "id": "batch/the-body",
        "area": "area/site",
        "note": "The Fathomer, sculpted from forms/the-stranding-body.json, stamped over its bank; the places inside it are cut out of the form and drawn by their own pieces.",
        "edits": [{
            "verb": "fragment",
            "prefab": body.PID,
            "frame": {"kind": "anchor-relative", "anchor": ANCHOR},
            "at": rel(body.ORIGIN),
        }],
    })
    # the body first: every batch is judged as it leaves the world
    return out[1:] + out[:1]


def main():
    doc = {"campaign_id": M.CID, "dsl_version": M.DSL, "stage": "world-edits",
           "content": {"batches": batches()}}
    with open(os.path.join(CAMPAIGN, "world-edits.json"), "w") as f:
        json.dump(doc, f, indent=2, sort_keys=True)
        f.write("\n")


if __name__ == "__main__":
    main()
