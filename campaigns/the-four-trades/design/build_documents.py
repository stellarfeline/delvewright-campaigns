#!/usr/bin/env python3
"""Write the stage documents of The Four Trades (everything but the programs).

    python3 campaigns/the-four-trades/design/build_documents.py

The documents are the artifact; this script is how they were typed, kept so a
change to one place's numbers is made once.
"""
import json
import pathlib

CID = "the-four-trades"
V = "0.66.0"
HERE = pathlib.Path(__file__).resolve().parent.parent

WIKI = "https://minecraft.wiki/w/Village/Structure/Blueprints/"
WIKI_TERMS = "CC BY-NC-SA 3.0"
WP_TERMS = "CC BY-SA 4.0"

# The four trades, west to east along the lane's north side:
# `(stem, intent, note, references)`.
TRADES = [
    ("smithy", "smithy",
     "The smith's: a front shop where finished ironwork is sold over a counter, and behind a wall with a window and a door the forge, the anvil before it and the quench at hand.",
     [
         {"url": WIKI + "Plains_weaponsmith_1_blueprint", "shows": "The game's own weaponsmith, layer by layer: take the forge set against a wall with the anvil and the work space before it, and the open front that shows the work to the street.", "terms": WIKI_TERMS},
         {"url": "https://en.wikipedia.org/wiki/Blacksmith", "shows": "Smithies as people built and worked them: take the forge, the anvil and the quench standing together as one working triangle, and the finished goods hung where a customer sees them.", "terms": WP_TERMS},
     ]),
    ("weaver", "weaver's",
     "The weaver's: a front shop of cloth — bolts on the shelves, carpets laid out, a counter with cloth on it — and behind it the workroom with the looms, each with its weaver's seat, the wool waiting beside them.",
     [
         {"url": WIKI + "Plains_shepherd_house_blueprint", "shows": "The game's own shepherd's house: take the loom as the house's working object and the wool kept beside it.", "terms": WIKI_TERMS},
         {"url": "https://en.wikipedia.org/wiki/Loom", "shows": "Looms as people built and worked them: take the loom with its bench before it and the weaver's place at the bench, and the cloth coming off it.", "terms": WP_TERMS},
     ]),
    ("bakery", "bakery",
     "The baker's: a front shop where loaves are sold over a counter beside sacks of flour, and behind it the bakehouse with the brick oven burning, the kneading table and the wheat.",
     [
         {"url": WIKI + "Plains_butcher_shop_1_blueprint", "shows": "The game's own food shop: take the counter at the front where food is sold and the cooking done behind it.", "terms": WIKI_TERMS},
         {"url": "https://en.wikipedia.org/wiki/Bakery", "shows": "Bakeries as people built them: take the brick oven as the room's heart, the shop front with its counter, and the chimney that says baking from the street.", "terms": WP_TERMS},
     ]),
    ("cartographer", "cartographer's",
     "The cartographer's: a reception room with charts on the walls and a table to show a map on, and behind it the map room with the drawing tables, the lecterns and the shelves of surveys.",
     [
         {"url": WIKI + "Plains_cartographer_1_blueprint", "shows": "The game's own cartographer's house: take the cartography table as the working object and the room arranged round it.", "terms": WIKI_TERMS},
         {"url": "https://en.wikipedia.org/wiki/Cartography", "shows": "Map-making as people did it: take the drawing table in good light, the instruments and the finished charts shown on the wall.", "terms": WP_TERMS},
     ]),
]

LANE_MIN = [3, 36]
LANE_EXTENT = [70, 5]
TRADE = 14  # a trade with a workroom and a shop front: 14 x 14 of play space
DOOR_AT = [7, 25, 43, 61]  # the doors on the lane's north face, one per trade
WELL_AT = 62


def doc(stage, content):
    return {"campaign_id": CID, "content": content, "dsl_version": V, "stage": stage}


def write(name, d):
    p = HERE / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def main():
    write("world.json", doc("world", {
        "areas": [],
        "test_level": True,
        "horizon": {"attributes": {"audio/background_music": {}}, "base": "void"},
        "min_players": 1,
        "outro": "The lane is walked to its well, past every trade on it.",
        "premise": "Craft Lane runs off the market road: a smith, a weaver, a baker and a cartographer keep shop along it, and the lane ends at the old well.",
        "seed": 20261027,
        "target_minutes": 8,
        "theme": "A lane of four trades, each a two-room building: a front shop that says the trade and a workroom where it is worked — a smithy, a weaver's, a bakery and a cartographer's.",
        "time": "day",
        "title": "The Four Trades",
        "weather": "clear",
    }))
    write("npcs.json", doc("npcs", {"npcs": []}))
    write("dialogue.json", doc("dialogue", {"dialogues": []}))
    write("classes.json", doc("classes", {"classes": [{
        "blurb": "A traveller come up Craft Lane, free to look in at every trade on the way to the well.",
        "id": "class/traveller",
        "kit": [
            {"count": 1, "item": "minecraft:wooden_sword", "name": "Walking staff"},
            {"count": 6, "item": "minecraft:bread"},
        ],
        "name": "Traveller",
    }]}))
    write("geometry-brief.json", doc("geometry-brief", {"facts": [
        {"id": "fact/site-span", "note": "Seventy-six blocks east to west: the lane and the field walls at either end.", "unit": "blocks", "value": 76},
        {"id": "fact/site-depth", "note": "Thirty-four blocks north to south: the four trades north of the lane, the lane, the well-yard south of it.", "unit": "blocks", "value": 34},
        {"id": "fact/site-height", "note": "Twenty-four blocks from under the lane to the sky.", "unit": "blocks", "value": 24},
        {"id": "fact/trade-span", "note": "A trade building with a workroom and a shop front stands on at least fourteen by fourteen of play space.", "unit": "blocks", "value": TRADE},
    ]}))
    write("quest-plan.json", doc("quest-plan", {
        "finale": "quest/the-lane",
        "quests": [
            {"act": 1, "area": "area/site", "depends_on": [], "goal": "Walk Craft Lane to the old well at its end, looking in at any trade on the way.", "id": "quest/the-lane", "mandatory": True, "npcs": []},
        ],
    }))
    nodes = [{"id": "node/lane", "intent": "connector", "note": "Craft Lane, three wide with a verge on its south side and lamps on the verge; the four trades open their doors onto it."}]
    for stem, intent, note, refs in TRADES:
        nodes.append({"id": f"node/{stem}", "intent": intent, "note": note, "references": refs})
    nodes.append({"id": "node/well", "intent": "well-yard", "note": "The old well at the lane's end, in a yard open to the lane and the green."})
    edges = [{"a": "node/lane", "b": f"node/{s}", "class": "walk", "id": f"edge/{s}-door"} for s, *_ in TRADES]
    edges.append({"a": "node/lane", "b": "node/well", "class": "walk", "id": "edge/well-front"})
    write("layout-graph.json", doc("layout-graph", {
        "beats": [{"node": "node/well", "objective": "obj/the-well", "quest": "quest/the-lane"}],
        "critical_path": ["node/lane", "node/well"],
        "edges": edges,
        "entry": "node/lane",
        "goal": "node/well",
        "nodes": nodes,
    }))
    boxes = [
        {"ceiling": {"open": 4}, "extent": LANE_EXTENT, "floor": {"datum": "datum/grade"}, "min": LANE_MIN, "node": "node/lane",
         "way": {"at": 0, "axis": "x", "clear": 3}},
    ]
    seams = []
    identities = [
        {"cmp": "eq", "fact": "fact/site-span", "measure": {"axis": "x", "of": "region-extent"}},
        {"cmp": "eq", "fact": "fact/site-depth", "measure": {"axis": "z", "of": "region-extent"}},
        {"cmp": "eq", "fact": "fact/site-height", "measure": {"axis": "y", "of": "region-extent"}},
    ]
    forms = {
        "smithy": "the smith's front door, spruce, between two windows on the forge",
        "weaver": "the weaver's front door, oak, between two windows hung with cloth",
        "bakery": "the baker's front door, oak, under the oven's chimney",
        "cartographer": "the cartographer's front door, dark oak, between two windows on the charts",
    }
    for (stem, *_), at in zip(TRADES, DOOR_AT):
        boxes.append({"ceiling": {"clearance": 4}, "extent": [TRADE, TRADE], "floor": {"datum": "datum/grade"}, "node": f"node/{stem}",
                      "roof": {"courses": 3, "eaves": 0}})
        seams.append({"at": at, "edge": f"edge/{stem}-door", "face": "north", "form": forms[stem], "meets": 6, "opening": "door"})
        # The rooms divide the building across z, so the size is bound on x,
        # the axis every room spans whole: the built world re-measures a
        # box's extent as the clear run through its middle (DW0833).
        identities.append({"cmp": "ge", "fact": "fact/trade-span", "measure": {"axis": "x", "node": f"node/{stem}", "of": "box-extent"}})
    boxes.append({"ceiling": {"open": 4}, "extent": [7, 7], "floor": {"datum": "datum/grade"}, "node": "node/well",
                  "sides": {"east": "open", "north": "open", "south": "open", "west": "open"}})
    seams.append({"at": WELL_AT, "contact": {"extent": [7, 4]}, "edge": "edge/well-front", "face": "south", "form": "the well-yard's front, open along the whole of it", "meets": 0})
    write("site-plan.json", doc("site-plan", {
        "boxes": boxes,
        "datums": [{"id": "datum/grade", "note": "The lane and every place on it.", "y": 64}],
        "fill": {"below": "minecraft:dirt", "kind": "open", "surface": "minecraft:grass_block",
                 "terrain": {"datum": "datum/grade", "kind": "flat"}},
        "identities": identities,
        "lighting": {"fixture": "torch", "min_light": 7},
        "region": {"extent": [76, 24, 34], "min": [0, 52, 18]},
        "seams": seams,
        "volumes": [
            {"block": "minecraft:mossy_cobblestone", "id": "volume/field-wall-west", "note": "The field wall at the lane's west end.",
             "region": {"extent": [1, 8, 34], "min": [0, 58, 18]}, "role": "massif"},
            {"block": "minecraft:mossy_cobblestone", "id": "volume/field-wall-east", "note": "The field wall at the east end.",
             "region": {"extent": [1, 8, 34], "min": [75, 58, 18]}, "role": "massif"},
            {"block": "minecraft:mossy_cobblestone", "id": "volume/field-wall-north", "note": "The field wall behind the trades.",
             "region": {"extent": [74, 8, 1], "min": [1, 58, 18]}, "role": "massif"},
            {"block": "minecraft:mossy_cobblestone", "id": "volume/field-wall-south", "note": "The field wall along the south edge of the green.",
             "region": {"extent": [74, 8, 1], "min": [1, 58, 51]}, "role": "massif"},
        ],
    }))


def quests():
    return doc("quests", {
        "quests": [
            {
                "cast": {},
                "happening": {"subject": "anchor/node-lane", "text": "The traveller comes up Craft Lane.", "verb": "arrives"},
                "id": "quest/the-lane",
                "objectives": [
                    {"anchor": "anchor/node-well", "radius": 2,
                     "happening": {"subject": "anchor/node-well", "text": "The traveller reaches the old well at the lane's end.", "verb": "arrives"},
                     "hint": "The old well stands in the yard at the far end of the lane, past the four shops.",
                     "id": "obj/the-well", "title": "Reach the old well", "type": "reach-anchor"},
                ],
                "on_complete": [
                    {"style": "subtitle", "text": "The lane is walked to its well.", "type": "narrate"},
                    {"type": "campaign-complete",
                     "happening": {"subject": "anchor/node-well", "text": "Craft Lane is walked.", "verb": "opens"}},
                ],
                "on_objective_complete": {},
                "trigger": {"type": "campaign-start"},
            },
        ],
        "triggers": [
            {"at": "anchor/node-lane", "id": "trigger/the-lane", "on": {"on": "approach", "range": 4}, "once": True,
             "effects": [{"style": "chat", "text": "Craft Lane. Four shops keep their doors on it, and the old well waits at the far end. Look in where you like.", "type": "narrate"}]},
        ],
    })


if __name__ == "__main__":
    main()
    write("quests.json", quests())
