#!/usr/bin/env python3
"""Write the stage documents of The Front and the Fountain (everything but the programs).

    python3 campaigns/the-front-and-the-fountain/design/build_documents.py

The documents are the artifact; this script is how they were typed, kept so a
change to one place's numbers is made once.
"""
import json
import pathlib

CID = "the-front-and-the-fountain"
V = "0.66.0"
HERE = pathlib.Path(__file__).resolve().parent.parent


def doc(stage, content):
    return {"campaign_id": CID, "content": content, "dsl_version": V, "stage": stage}


def write(name, d):
    p = HERE / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


# Four places on the street's north side, west to east, each a contact the
# whole width of its open front: `(stem, x0 on the street's face, width, depth,
# ceiling)`.
PLACES = [
    ("smithy", 1, 9, 7, {"clearance": 5}),
    ("square", 13, 9, 9, {"open": 4}),
    ("stall", 25, 9, 7, {"clearance": 5}),
    ("ring", 37, 7, 7, {"open": 4}),
]
STREET_MIN = [3, 30]
STREET_EXTENT = [46, 4]


def main():
    write("world.json", doc("world", {
        "areas": [],
        "test_level": True,
        "horizon": {"attributes": {"audio/background_music": {}}, "base": "void"},
        "min_players": 1,
        "outro": "The street is walked, and the warden has seen every front and every fountain on it.",
        "premise": "The town warden walks Tanner's Row before the fair: the new smithy front, the fountain square, the old stall and the old well-yard, to judge which of them looks right.",
        "seed": 20261026,
        "target_minutes": 6,
        "theme": "One short street with four places on it: a smithy whose front is a frame of posts and a beam, a square with a fountain whose water stands in a bowl raised on a stack over a basin, a stall with a door standing free beside its counter, and a yard with a flat ring round one cell of water.",
        "time": "day",
        "title": "The Front and the Fountain",
        "weather": "clear",
    }))
    write("npcs.json", doc("npcs", {"npcs": []}))
    write("dialogue.json", doc("dialogue", {"dialogues": []}))
    write("classes.json", doc("classes", {"classes": [{
        "blurb": "The town warden, walking Tanner's Row before the fair to judge its fronts and its water.",
        "id": "class/warden",
        "kit": [
            {"count": 1, "item": "minecraft:wooden_sword", "name": "Warden's rod"},
            {"count": 6, "item": "minecraft:bread"},
        ],
        "name": "Town Warden",
    }]}))
    write("geometry-brief.json", doc("geometry-brief", {"facts": [
        {"id": "fact/site-span", "note": "Fifty-two blocks east to west: the row and the field walls at either end.", "unit": "blocks", "value": 52},
        {"id": "fact/site-depth", "note": "Forty blocks north to south: the four places north of the row, the row, the lodge south of it, and the green round them.", "unit": "blocks", "value": 40},
        {"id": "fact/site-height", "note": "Twenty-four blocks from under the row to the sky.", "unit": "blocks", "value": 24},
    ]}))
    write("quest-plan.json", doc("quest-plan", {
        "finale": "quest/the-row",
        "quests": [
            {"act": 1, "area": "area/site", "depends_on": [], "goal": "Walk Tanner's Row and look at each place on it: the new smithy front, the fountain square, the old stall, and the old well-yard at the end.", "id": "quest/the-row", "mandatory": True, "npcs": []},
        ],
    }))
    nodes = [
        {"id": "node/row", "intent": "connector", "note": "Tanner's Row, three wide with a verge on its south side and its lamps on the verge."},
        {"id": "node/smithy", "intent": "smithy", "note": "The new smithy: roofed, walled on three sides, its street side open. Behind the open front's first row, which the row's crossing keeps clear, a frame of posts and a beam stands where the wall would have been, its counter under the beam and its door in the frame under the same head. The forge and the anvil behind."},
        {"id": "node/square", "intent": "fountain square", "note": "The fountain square, open on every side. In its middle a fountain: water raised in a bowl on a stack over a basin round it."},
        {"id": "node/stall", "intent": "stall", "note": "The old stall: roofed, walled on three sides, its street side open. Behind the open front's first row a one-course counter and a two-course door stand side by side with nothing over them under the five-course void."},
        {"id": "node/ring", "intent": "well-yard", "note": "The old well-yard, open on every side, a flat ring of stone round one cell of water at the ring's own height."},
        {"id": "node/lodge", "intent": "lodge", "note": "The warden's lodge across the row, walled all round, its doorway on the row."},
    ]
    write("layout-graph.json", doc("layout-graph", {
        "beats": [
            {"node": "node/smithy", "objective": "obj/the-smithy", "quest": "quest/the-row"},
            {"node": "node/square", "objective": "obj/the-square", "quest": "quest/the-row"},
            {"node": "node/stall", "objective": "obj/the-stall", "quest": "quest/the-row"},
            {"node": "node/ring", "objective": "obj/the-ring", "quest": "quest/the-row"},
        ],
        "critical_path": ["node/row", "node/smithy", "node/row", "node/square", "node/row", "node/stall", "node/row", "node/ring"],
        "edges": [{"a": "node/row", "b": f"node/{s}", "class": "walk", "id": f"edge/{s}-front"} for s, *_ in PLACES]
        + [{"a": "node/row", "b": "node/lodge", "class": "walk", "id": "edge/lodge-door"}],
        "entry": "node/row",
        "goal": "node/ring",
        "nodes": nodes,
    }))
    boxes = [
        {"ceiling": {"open": 4}, "extent": STREET_EXTENT, "floor": {"datum": "datum/grade"}, "min": STREET_MIN, "node": "node/row",
         "way": {"at": 0, "axis": "x", "clear": 3}},
    ]
    seams = []
    forms = {
        "smithy": "the new smithy's front: the frame of posts and a beam, its counter and its door under the same head",
        "square": "the fountain square's front, open along the whole of it",
        "stall": "the old stall's front: a counter and a door standing free under the open face",
        "ring": "the old well-yard's front, open along the whole of it",
    }
    for stem, at, w, d, ceiling in PLACES:
        box = {"ceiling": ceiling, "extent": [w, d], "floor": {"datum": "datum/grade"}, "node": f"node/{stem}"}
        if "open" in ceiling:
            box["sides"] = {"east": "open", "north": "open", "south": "open", "west": "open"}
        else:
            box["sides"] = {"south": "open"}
        boxes.append(box)
        seams.append({"at": at, "contact": {"extent": [w, 4]}, "edge": f"edge/{stem}-front", "face": "north", "form": forms[stem], "meets": 0})
    boxes.append({"ceiling": {"clearance": 4}, "extent": [6, 5], "floor": {"datum": "datum/grade"}, "node": "node/lodge"})
    seams.append({"at": 20, "edge": "edge/lodge-door", "face": "south", "form": "the warden's lodge doorway, off the row", "meets": 2, "opening": "door"})
    write("site-plan.json", doc("site-plan", {
        "boxes": boxes,
        "datums": [{"id": "datum/grade", "note": "The row and every place on it.", "y": 64}],
        "fill": {"below": "minecraft:dirt", "kind": "open", "surface": "minecraft:grass_block",
                 "terrain": {"datum": "datum/grade", "kind": "flat"}},
        "identities": [
            {"cmp": "eq", "fact": "fact/site-span", "measure": {"axis": "x", "of": "region-extent"}},
            {"cmp": "eq", "fact": "fact/site-depth", "measure": {"axis": "z", "of": "region-extent"}},
            {"cmp": "eq", "fact": "fact/site-height", "measure": {"axis": "y", "of": "region-extent"}},
        ],
        "lighting": {"fixture": "torch", "min_light": 7},
        "region": {"extent": [52, 24, 40], "min": [0, 52, 2]},
        "seams": seams,
        "volumes": [
            {"block": "minecraft:mossy_cobblestone", "id": "volume/field-wall-west", "note": "The field wall that closes the green at the west end of the row.",
             "region": {"extent": [1, 8, 40], "min": [0, 58, 2]}, "role": "massif"},
            {"block": "minecraft:mossy_cobblestone", "id": "volume/field-wall-east", "note": "The field wall at the east end.",
             "region": {"extent": [1, 8, 40], "min": [51, 58, 2]}, "role": "massif"},
            {"block": "minecraft:mossy_cobblestone", "id": "volume/field-wall-north", "note": "The field wall along the north edge of the green.",
             "region": {"extent": [50, 8, 1], "min": [1, 58, 2]}, "role": "massif"},
            {"block": "minecraft:mossy_cobblestone", "id": "volume/field-wall-south", "note": "The field wall along the south edge of the green.",
             "region": {"extent": [50, 8, 1], "min": [1, 58, 41]}, "role": "massif"},
        ],
    }))


def quests():
    def reach(oid, anchor, title, hint, text):
        return {"anchor": anchor, "radius": 2, "happening": {"subject": anchor, "text": text, "verb": "arrives"},
                "hint": hint, "id": oid, "title": title, "type": "reach-anchor"}
    return doc("quests", {
        "quests": [
            {
                "cast": {},
                "happening": {"subject": "anchor/node-row", "text": "The warden comes down Tanner's Row before the fair.", "verb": "arrives"},
                "id": "quest/the-row",
                "objectives": [
                    reach("obj/the-smithy", "anchor/node-smithy", "Step into the new smithy", "The new smithy is the first front on the row, its door beside the counter.", "The warden steps in through the smithy's door, behind the counter."),
                    dict(reach("obj/the-square", "anchor/node-square", "Stand in the fountain square", "The fountain square is the next place along the row.", "The warden stands in the square, by the fountain."), after=["obj/the-smithy"]),
                    dict(reach("obj/the-stall", "anchor/node-stall", "Step into the old stall", "The old stall is further along the row, its door beside its counter.", "The warden steps into the old stall."), after=["obj/the-square"]),
                    dict(reach("obj/the-ring", "anchor/node-ring", "Stand in the old well-yard", "The old well-yard is at the end of the row.", "The warden stands by the ring of stone in the old yard."), after=["obj/the-stall"]),
                ],
                "on_complete": [
                    {"style": "subtitle", "text": "Every front on the row is seen.", "type": "narrate"},
                    {"type": "campaign-complete",
                     "happening": {"subject": "anchor/node-ring", "text": "The row is walked.", "verb": "opens"}},
                ],
                "on_objective_complete": {},
                "trigger": {"type": "campaign-start"},
            },
        ],
        "triggers": [
            {"at": "anchor/node-row", "id": "trigger/the-row", "on": {"on": "approach", "range": 4}, "once": True,
             "effects": [{"style": "chat", "text": "Tanner's Row. Look at each place on it before the fair: the new smithy, the fountain square, the old stall, and the old well-yard at the end.", "type": "narrate"}]},
        ],
    })


if __name__ == "__main__":
    main()
    write("quests.json", quests())
