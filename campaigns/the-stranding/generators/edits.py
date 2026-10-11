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


def batches():
    out = []
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
    return out


def main():
    doc = {"campaign_id": M.CID, "dsl_version": M.DSL, "stage": "world-edits",
           "content": {"batches": batches()}}
    with open(os.path.join(CAMPAIGN, "world-edits.json"), "w") as f:
        json.dump(doc, f, indent=2, sort_keys=True)
        f.write("\n")


if __name__ == "__main__":
    main()
