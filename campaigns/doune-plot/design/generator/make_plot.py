#!/usr/bin/env python3
"""Writes the doune-plot test map: Doune Castle, copied whole from
`campaigns/doune-castle-tour`, standing as one plot on a hilltop.

Story documents are Doune's own, carried verbatim except for the area name
(a site-plan map has no `areas[]`). The map documents are this file's: one
open place, `node/castle`, whose box is Doune's footprint less its ring, on a
plateau whose surface is Doune's own grade.

    python3 make_plot.py        # from anywhere; writes into the campaign
"""
import json, pathlib, struct, zlib, math

HERE = pathlib.Path(__file__).resolve().parent
CAMP = HERE.parent.parent                       # campaigns/doune-plot
SRC = CAMP.parent / "doune-castle-tour"
DSL = "0.69.0"
ID = "doune-plot"

# ---- geometry ----------------------------------------------------------
DX, DY, DZ = 104, 56, 120   # Doune's structure set
CUT = 4                     # Doune courses under its deepest ditch floor, not carried
WALK = 103                  # world y a body stands at on Doune's grade (local y8)
GRADE_Y = WALK - 1          # Doune's surface course (local y7), the plateau's surface
DITCH_Y = WALK - 4          # Doune's deepest ditch floor course (local y4): the terrain under the plot
REGION_MIN = [0, 50, 0]
REGION = [280, 120, 300]
BOX_MIN = [90, 120]         # play-space corner; the frame is one cell further out
EXTENT = [DX - 2, DZ - 2]
OPEN = DY - 8               # courses of air over the walk plane: Doune y8..55
ROAD_X, ROAD_W, ROAD_L = 75, 5, 8   # Doune-local x of the approach road at its north end; its width; the road place's length
FRAME0 = (BOX_MIN[0] - 1, DITCH_Y, BOX_MIN[1] - 1)   # world corner of Doune-local (0, CUT, 0)


def doc(stage, content):
    return {"campaign_id": ID, "content": content, "dsl_version": DSL, "stage": stage}


def write(name, obj):
    p = CAMP / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def src(name):
    return json.loads((SRC / name).read_text(encoding="utf-8"))


def retarget(o):
    """Doune's story documents, area name swapped, campaign id swapped."""
    s = json.dumps(o, ensure_ascii=False)
    s = s.replace('"area/castle"', '"area/site"').replace('"doune-castle-tour"', f'"{ID}"')
    return json.loads(s)


# ---- the hill ----------------------------------------------------------
def heightmap():
    """A hill whose flat top carries the castle's plot; pixel = surface y - 40."""
    w, h = REGION[0], REGION[2]
    x0, z0 = FRAME0[0] - 8, FRAME0[2] - 8
    x1, z1 = FRAME0[0] + DX + 8, FRAME0[2] + DZ + 8
    rows = []
    for z in range(h):
        row = bytearray([0])
        for x in range(w):
            dx = max(x0 - x, 0, x - x1)
            dz = max(z0 - z, 0, z - z1)
            d = math.hypot(dx, dz)
            fall = 30 * (1 - math.cos(min(d, 70) / 70 * math.pi)) / 2   # 0 → 30 over 70 cells
            y = GRADE_Y - round(fall)
            if FRAME0[0] < x < FRAME0[0] + DX - 1 and FRAME0[2] < z < FRAME0[2] + DZ - 1:
                y = DITCH_Y     # inside the ring the plot owns its ground down to the ditch floors
            row.append(y - 40)
        rows.append(bytes(row))
    raw = b"".join(rows)

    def chunk(t, d):
        c = struct.pack(">I", len(d)) + t + d
        return c + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 0, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")
    (CAMP / "hill.png").write_bytes(png)


def main():
    # story: Doune's own
    w = src("world.json")
    w = retarget(w)
    c = w["content"]
    c["areas"] = []
    c["test_level"] = True
    c["horizon"] = {"attributes": {"audio/background_music": {}}, "base": "void"}
    c.pop("boundary", None)
    write("world.json", w)
    for n in ["npcs.json", "classes.json", "quest-plan.json", "quests.json", "dialogue.json"]:
        write(n, retarget(src(n)))
    side = retarget(src("l10n/zh-cn.json"))
    for k in ["area.castle.name", "world.boundary.message"]:   # no area, no boundary here
        del side["content"][k]
        del side["source"][k]
    write("l10n/zh-cn.json", side)

    quests = src("quests.json")["content"]["quests"]
    used = sorted({a for a in json.dumps([src("quests.json"), src("npcs.json"),
                                          src("dialogue.json")]).split('"')
                   if a.startswith("anchor/")})
    beats = [{"node": "node/castle", "objective": o["id"], "quest": q["id"]}
             for q in quests for o in q["objectives"]]
    write("layout-graph.json", doc("layout-graph", {
        "beats": beats,
        "critical_path": ["node/castle"],
        "edges": [{"a": "node/castle", "b": "node/road", "class": "walk", "id": "edge/road-to-gate"}],
        "entry": "node/castle",
        "goal": "node/castle",
        "nodes": [{
            "id": "node/castle",
            "intent": "a courtyard castle with its approach, ditches and grounds",
            "note": "Doune Castle, copied whole: the gatehouse, the hall range, the kitchen tower, the courtyard, the curtain and the three ditches on the north approach.",
            "stations": [{"anchor": a, "kind": "point", "note": f"Doune's own `{a}`."}
                         for a in used],
        }, {
            "id": "node/road",
            "intent": "the road up to the castle's north approach",
            "note": "The last stretch of the road from the town, arriving on the hilltop at the start of Doune's own approach road, five wide.",
        }],
    }))
    write("geometry-brief.json", doc("geometry-brief", {"facts": [
        {"id": "fact/castle-width", "note": "Doune's footprint east-west, less the ring the plot's walls may stand in.",
         "unit": "blocks", "value": float(EXTENT[0])},
    ]}))
    write("site-plan.json", doc("site-plan", {
        "boxes": [{
            "ceiling": {"open": OPEN},
            "extent": EXTENT,
            "floor": {"datum": "datum/grade"},
            "min": BOX_MIN,
            "node": "node/castle",
        }, {
            "ceiling": {"open": 6},
            "extent": [ROAD_W + 4, ROAD_L],
            "floor": {"datum": "datum/grade"},
            "node": "node/road",
            "way": {"axis": "z", "clear": ROAD_W},
        }],
        "datums": [{"id": "datum/grade", "note": "Where a body stands on Doune's grade and on the hilltop around it; the ditches are cut four courses into the plot's own ground.", "y": WALK}],
        "fill": {"below": "minecraft:dirt", "kind": "open", "surface": "minecraft:grass_block",
                 "terrain": {"kind": "heightmap", "heightmap": "hill.png", "base_y": 40, "range": 255}},
        "identities": [{"cmp": "eq", "fact": "fact/castle-width",
                        "measure": {"axis": "x", "node": "node/castle", "of": "box-extent"}}],
        "lighting": {"fixture": "lantern", "min_light": 7},
        "region": {"extent": REGION, "min": REGION_MIN},
        "seams": [{"at": ROAD_X - 1, "contact": {"extent": [ROAD_W, 3]}, "edge": "edge/road-to-gate", "face": "north",
                   "form": "Doune's approach road running on, level, onto the hilltop road: five wide, no wall across it"}],
    }))
    anchors = {a: a for a in used}
    anchors["anchor/node-castle"] = "anchor/node-castle"
    anchors["spawn"] = "anchor/spawn"
    write("detail-plan.json", doc("detail-plan", {"details": [
        {"anchors": anchors, "piece": "prefab/doune-plot-castle", "place": "node/castle"}]}))
    heightmap()
    print("frame corner (Doune-local 0,%d,0) at world %s; open %d" % (CUT, FRAME0, OPEN))


if __name__ == "__main__":
    main()
