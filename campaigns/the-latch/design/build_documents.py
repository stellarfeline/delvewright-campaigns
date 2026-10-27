#!/usr/bin/env python3
"""Write the stage documents of The Latch (everything but the programs).

    python3 campaigns/the-latch/design/build_documents.py [l10n-inventory.json]

The documents are the artifact; this script is how they were typed, kept so a
change to one place's numbers is made once. Given the engine's l10n inventory
(`delvec l10n-inventory`), it also writes the zh-CN sidecar.
"""
import json
import pathlib
import sys

CID = "the-latch"
V = "0.66.0"
HERE = pathlib.Path(__file__).resolve().parent.parent


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
        "languages": ["zh-cn"],
        "min_players": 1,
        "outro": "The iron door stands open, and the old garden is yours to walk.",
        "premise": "Old Wenna's cottage stands at the end of the lane with its garden locked behind it. She has left the latch for whoever comes: through her yard gate, through the kitchen and the door to the back room, and the iron door to the garden opens when the latch is lifted.",
        "seed": 20261023,
        "target_minutes": 8,
        "theme": "A hedged yard with a wooden gate, a cottage of two rooms joined by an oak door, oak trapdoors over the stair to its cellar, and an iron door at the back that opens only when the latch is lifted.",
        "time": "day",
        "title": "The Latch",
        "weather": "clear",
    }))
    write("npcs.json", doc("npcs", {"npcs": []}))
    write("dialogue.json", doc("dialogue", {"dialogues": []}))
    write("classes.json", doc("classes", {"classes": [{
        "blurb": "Old Wenna asked a neighbour to mind her cottage and to open the garden she has kept locked for years.",
        "id": "class/neighbour",
        "kit": [
            {"count": 1, "item": "minecraft:wooden_sword", "name": "Walking stick"},
            {"count": 6, "item": "minecraft:bread"},
        ],
        "name": "Neighbour",
    }]}))
    write("geometry-brief.json", doc("geometry-brief", {"facts": [
        {"id": "fact/site-span", "note": "Thirty-two blocks east to west: the yard, the cottage, the garden and the meadow round them.", "unit": "blocks", "value": 32},
        {"id": "fact/site-depth", "note": "Thirty-six blocks north to south.", "unit": "blocks", "value": 36},
        {"id": "fact/site-height", "note": "Twenty-four blocks from under the cellar to the sky.", "unit": "blocks", "value": 24},
    ]}))
    write("quest-plan.json", doc("quest-plan", {
        "finale": "quest/the-garden",
        "quests": [
            {"act": 1, "area": "area/site", "depends_on": [], "goal": "Go through the yard gate and into the cottage, through the oak door to the back room, and lift the latch that opens the iron door to the garden.", "id": "quest/the-latch", "mandatory": True, "npcs": []},
            {"act": 1, "area": "area/site", "depends_on": ["quest/the-latch"], "goal": "Go out through the iron door into the garden.", "id": "quest/the-garden", "mandatory": True, "npcs": []},
        ],
    }))
    write("layout-graph.json", doc("layout-graph", {
        "beats": [
            {"node": "node/cottage", "objective": "obj/lift-the-latch", "quest": "quest/the-latch"},
            {"node": "node/garden", "objective": "obj/step-out", "quest": "quest/the-garden"},
        ],
        "critical_path": ["node/yard", "node/cottage", "node/garden"],
        "edges": [
            {"a": "node/yard", "b": "node/cottage", "class": "walk", "id": "edge/front-door"},
            {"a": "node/cottage", "b": "node/cellar", "class": "stair", "id": "edge/cellar-stair"},
            {"a": "node/cottage", "b": "node/garden", "class": "walk", "id": "edge/garden-door",
             "gating": {"learned": "seen", "quest": "quest/the-latch"}},
        ],
        "entry": "node/yard",
        "goal": "node/garden",
        "nodes": [
            {"id": "node/yard", "intent": "entrance", "note": "Wenna's yard, hedged all round, open to the sky: a wooden gate in a hedge across it on the path to the cottage door."},
            {"id": "node/cottage", "intent": "hub", "note": "The cottage: two rooms, the kitchen the front door opens into and the back room behind an oak door; oak trapdoors in the back room's floor over the cellar stair; the iron door to the garden in the back room's north wall, and the latch lever by the east wall.",
             "stations": [
                 {"anchor": "anchor/latch", "kind": "point", "note": "The latch lever on the back room's floor, by its east wall, its rod run under the floor to the iron door."},
             ]},
            {"id": "node/cellar", "intent": "cache", "note": "The cellar under the cottage, down a short stair under the trapdoors in the back room's floor: barrels and a shelf.", "reached": True},
            {"id": "node/garden", "intent": "goal-chamber", "note": "The old garden behind the cottage, hedged all round and open to the sky."},
        ],
    }))
    write("site-plan.json", doc("site-plan", {
        "boxes": [
            {"ceiling": {"open": 4}, "extent": [9, 7], "floor": {"datum": "datum/grade"}, "min": [10, 22], "node": "node/yard"},
            {"ceiling": {"clearance": 4}, "extent": [11, 6], "floor": {"datum": "datum/grade"}, "node": "node/cottage"},
            {"ceiling": {"clearance": 3}, "extent": [11, 6], "floor": {"datum": "datum/cellar"}, "node": "node/cellar"},
            {"ceiling": {"open": 4}, "extent": [9, 6], "floor": {"datum": "datum/grade"}, "node": "node/garden"},
        ],
        "datums": [
            {"id": "datum/grade", "note": "The yard, the cottage floor and the garden.", "y": 64},
            {"id": "datum/cellar", "note": "The cellar floor, four under the cottage's.", "y": 60},
        ],
        "fill": {"below": "minecraft:dirt", "kind": "open", "surface": "minecraft:grass_block",
                 "terrain": {"datum": "datum/grade", "kind": "flat"}},
        "identities": [
            {"cmp": "eq", "fact": "fact/site-span", "measure": {"axis": "x", "of": "region-extent"}},
            {"cmp": "eq", "fact": "fact/site-depth", "measure": {"axis": "z", "of": "region-extent"}},
            {"cmp": "eq", "fact": "fact/site-height", "measure": {"axis": "y", "of": "region-extent"}},
        ],
        "lighting": {"fixture": "torch", "min_light": 7},
        "region": {"extent": [32, 24, 36], "min": [0, 52, 0]},
        "seams": [
            {"at": 2, "edge": "edge/front-door", "face": "north", "form": "the cottage's front door, oak, from the yard into the kitchen", "meets": 2, "opening": "door"},
            {"at": [8, 0], "edge": "edge/cellar-stair", "face": "down", "form": "oak trapdoors in the back room's floor over a short stone stair down to the cellar", "meets": [8, 0], "opening": {"height": 3, "width": 1}, "stair_in": "node/cellar"},
            {"at": 7, "edge": "edge/garden-door", "face": "north", "form": "an iron door from the back room into the garden, opened when the latch is lifted", "meets": 5, "opening": "door"},
        ],
    }))


def quests():
    lifted = [
        {"anchor": "anchor/seam-garden-door", "type": "open-gate",
         "happening": {"subject": "anchor/seam-garden-door", "text": "The iron door to the garden swings open.", "verb": "opens"}},
        {"at": {"anchor": "anchor/latch", "at": "anchor"}, "sound": "minecraft:block.iron_door.open", "type": "play-sound"},
        {"style": "chat", "text": "The latch lifts with a clank, and the iron door to the garden swings open.", "type": "narrate"},
    ]
    return doc("quests", {
        "quests": [
            {
                "cast": {},
                "happening": {"subject": "anchor/node-yard", "text": "The neighbour comes into Wenna's yard.", "verb": "arrives"},
                "id": "quest/the-latch",
                "objectives": [{
                    "anchor": "anchor/latch",
                    "happening": {"subject": "anchor/seam-garden-door", "text": "The neighbour pulls the latch lever, and the bolt of the iron door draws back.", "verb": "opens"},
                    "hint": "Through the yard gate, the kitchen and the oak door. The latch lever is on the back room's floor, by the hay.",
                    "id": "obj/lift-the-latch",
                    "prop": {"block": "minecraft:lever[face=floor,facing=north,powered=false]"},
                    "title": "Lift the latch in the back room", "type": "interact",
                }],
                "on_complete": [],
                "on_objective_complete": {"obj/lift-the-latch": lifted},
                "trigger": {"type": "campaign-start"},
            },
            {
                "cast": {},
                "happening": {"subject": "anchor/seam-garden-door", "text": "The iron door stands open.", "verb": "learns"},
                "id": "quest/the-garden",
                "objectives": [{
                    "anchor": "anchor/node-garden", "radius": 2,
                    "happening": {"subject": "anchor/node-garden", "text": "The neighbour walks out into the old garden.", "verb": "arrives"},
                    "hint": "Go out through the iron door.",
                    "id": "obj/step-out",
                    "title": "Walk out into the garden", "type": "reach-anchor",
                }],
                "on_complete": [
                    {"style": "subtitle", "text": "The garden is open.", "type": "narrate"},
                    {"type": "campaign-complete",
                     "happening": {"subject": "anchor/node-garden", "text": "The old garden is open.", "verb": "opens"}},
                ],
                "on_objective_complete": {},
                "trigger": {"quest": "quest/the-latch", "type": "quest-complete"},
            },
        ],
        "triggers": [
            {"at": "anchor/node-yard", "id": "trigger/the-yard", "on": {"on": "approach", "range": 4}, "once": True,
             "effects": [{"style": "chat", "text": "Wenna's yard. Her note said the latch for the garden is in the back room, past the kitchen.", "type": "narrate"}]},
        ],
    })


ZH = {
    "Old Wenna asked a neighbour to mind her cottage and to open the garden she has kept locked for years.": "温娜老太托邻居照看她的小屋，顺便把她锁了好些年的花园打开。",
    "Walking stick": "手杖",
    "Neighbour": "邻居",
    "The garden is open.": "花园开了。",
    "The latch lifts with a clank, and the iron door to the garden swings open.": "门闩咔哒一声抬起，通往花园的铁门转开了。",
    "Wenna's yard. Her note said the latch for the garden is in the back room, past the kitchen.": "这是温娜的院子。她的字条上说，开花园的门闩在里屋，穿过厨房就到。",
    "Go out through the iron door.": "从铁门走出去。",
    "Walk out into the garden": "走进花园",
    "Through the yard gate, the kitchen and the oak door. The latch lever is on the back room's floor, by the hay.": "穿过院门、厨房和那扇橡木门。门闩的拉杆在里屋地上，干草捆旁边。",
    "Lift the latch in the back room": "抬起里屋的门闩",
    "Go out through the iron door into the garden.": "穿过铁门，走进花园。",
    "Go through the yard gate and into the cottage, through the oak door to the back room, and lift the latch that opens the iron door to the garden.": "穿过院门进屋，推开橡木门到里屋，抬起门闩，打开通往花园的铁门。",
    "The iron door stands open, and the old garden is yours to walk.": "铁门敞开着，老花园随你走走。",
    "The Latch": "门闩",
}


def l10n(inventory):
    content, source = {}, {}
    for e in inventory["entries"]:
        content[e["key"]] = ZH[e["en"]]
        source[e["key"]] = e["en"]
    return {"campaign_id": CID, "content": content, "dsl_version": V, "kind": "l10n", "lang": "zh-cn", "source": source}


if __name__ == "__main__":
    main()
    write("quests.json", quests())
    if len(sys.argv) > 1:
        write("l10n/zh-cn.json", l10n(json.loads(pathlib.Path(sys.argv[1]).read_text())))
