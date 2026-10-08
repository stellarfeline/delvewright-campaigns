"""world-edits.json: the stamps the site plan does not place.

- batch/sea-skiff: the skiff out on the open water (pieces/the-stranding-sea-skiff.json,
  expanded into the library), stamped on node/open-water round anchor/sea-skiff.
- batch/the-figure: what stands in the sea west of the black water
  (forms/the-stranding-figure.json, sculpted into the library).
- batch/the-body: the body on its bank (forms/the-stranding-body.json), when present.

Positions are frame-relative to the campaign's own anchors, never world
coordinates. Run from the campaign directory: python3 generators/world_edits.py
"""
import json, os
here = os.path.dirname(os.path.abspath(__file__))
camp = os.path.join(here, "..")

def frame(anchor):
    return {"kind": "anchor-relative", "anchor": anchor}

batches = [
    {"id": "batch/sea-skiff", "area": "area/site",
     "note": "The skiff on the open water, stamped over the plan's massing of node/open-water; its seat (8,1,5) on anchor/sea-skiff.",
     "edits": [{"verb": "fragment", "prefab": "prefab/the-stranding-sea-skiff", "rotation": "none",
                "frame": frame("anchor/sea-skiff"), "at": [-8, -1, -5]}]},
    {"id": "batch/the-figure", "area": "area/site",
     "note": "What stands in the sea west of the black water, facing east toward the open water; never seen but in the crossing back and the return.",
     "edits": [{"verb": "fragment", "prefab": "prefab/the-stranding-figure", "rotation": "none",
                "frame": frame("anchor/sea-skiff"), "at": [-138, -10, -42]}]},
]
body = os.path.join(camp, "forms", "the-stranding-body.json")
if os.path.exists(body):
    meta = json.load(open(os.path.join(here, "body_place.json")))
    batches.append({"id": "batch/the-body", "area": "area/site",
        "note": "The body on its bank, sculpted from forms/the-stranding-body.json; its places are cut out of the form.",
        "edits": [{"verb": "fragment", "prefab": "prefab/the-stranding-body", "rotation": "none",
                   "frame": frame(meta["anchor"]), "at": meta["at"]}]})
doc = {"campaign_id": "the-stranding", "dsl_version": "0.36.0", "stage": "world-edits",
       "content": {"batches": batches}}
with open(os.path.join(camp, "world-edits.json"), "w") as f:
    json.dump(doc, f, indent=2, sort_keys=True); f.write("\n")
print("wrote world-edits.json:", [b["id"] for b in batches])
