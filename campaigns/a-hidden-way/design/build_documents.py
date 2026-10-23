#!/usr/bin/env python3
"""Write the stage documents of A Hidden Way (everything but the programs).

    python3 campaigns/a-hidden-way/design/build_documents.py [l10n-inventory.json]

The documents are the artifact; this script is how they were typed, kept so a
change to one place's numbers is made once. Given the engine's l10n inventory
(`delvec l10n-inventory`), it also writes the zh-CN sidecar.
"""
import json
import pathlib
import sys

CID = "a-hidden-way"
V = "0.62.0"
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
        "demo_level": True,
        "languages": ["zh-cn"],
        "min_players": 1,
        "outro": "The hearth stands cold and open, and the keeper's hall is quiet.",
        "premise": "The keeper's hall at Ashby has a great hearth whose fire has burned since the keeper's grandfather lit it. A valve on the hall's wall floods the flue, and the keeper has sent for someone to turn it at last.",
        "seed": 20261022,
        "target_minutes": 5,
        "theme": "A stone hall with a great hearth in its north wall and a valve beside it; the hearth's brick back hides what is behind it until the valve puts the fire out.",
        "time": "day",
        "title": "A Hidden Way",
        "weather": "clear",
    }))
    write("npcs.json", doc("npcs", {"npcs": []}))
    write("dialogue.json", doc("dialogue", {"dialogues": []}))
    write("classes.json", doc("classes", {"classes": [{
        "blurb": "The keeper sent for a hand to turn the old valve and put out the great hearth of the hall, which has burned for three generations.",
        "id": "class/hand",
        "kit": [
            {"count": 1, "item": "minecraft:iron_sword", "name": "Hand's sword"},
            {"count": 1, "item": "minecraft:leather_boots", "name": "Hand's boots"},
            {"count": 6, "item": "minecraft:bread"},
        ],
        "name": "Keeper's Hand",
    }]}))
    write("geometry-brief.json", doc("geometry-brief", {"facts": [
        {"id": "fact/site-span", "note": "Thirty-two blocks east to west: the hall and the rock round it.", "unit": "blocks", "value": 32},
        {"id": "fact/site-depth", "note": "Forty blocks north to south: the porch south of the hall, the hall, the rock north of it, and rock on every side.", "unit": "blocks", "value": 40},
        {"id": "fact/site-height", "note": "Twenty-four blocks from under the hall's floor to over its roof.", "unit": "blocks", "value": 24},
    ]}))
    write("quest-plan.json", doc("quest-plan", {
        "finale": "quest/the-way",
        "quests": [
            {"act": 1, "area": "area/site", "depends_on": [], "goal": "Come into the keeper's hall and turn the valve to the right of the great hearth, which floods the flue and puts out the fire.", "id": "quest/the-fire", "mandatory": True, "npcs": []},
            {"act": 1, "area": "area/site", "depends_on": ["quest/the-fire"], "goal": "Go through the cold hearth into the passage behind it.", "id": "quest/the-way", "mandatory": True, "npcs": []},
        ],
    }))
    write("layout-graph.json", doc("layout-graph", {
        "beats": [
            {"node": "node/hall", "objective": "obj/turn-the-valve", "quest": "quest/the-fire"},
            {"node": "node/passage", "objective": "obj/enter-the-passage", "quest": "quest/the-way"},
        ],
        "critical_path": ["node/porch", "node/hall", "node/passage"],
        "edges": [
            {"a": "node/porch", "b": "node/hall", "class": "walk", "id": "edge/porch-door"},
            {"a": "node/hall", "b": "node/passage", "class": "walk", "id": "edge/hearth-door",
             "gating": {"flags": ["flag/hearth-out"], "learned": "hidden",
                        "secret": ["passage", "behind the hearth", "密道"]}},
        ],
        "entry": "node/porch",
        "goal": "node/passage",
        "nodes": [
            {"id": "node/porch", "intent": "entrance", "note": "The porch the hand comes in by, south of the hall: a door into the hall."},
            {"id": "node/hall", "intent": "hub", "note": "The keeper's hall: the great hearth in its north wall, its fire burning before the brick back of the firebox, and the flue's valve on the wall to its right.",
             "stations": [
                 {"anchor": "anchor/hearth-fire", "kind": "gate", "note": "The fire on the hearth stone before the mouth, put out and washed away when the flue floods."},
                 {"anchor": "anchor/valve", "kind": "point", "note": "The valve on the hall's wall to the right of the hearth, which floods the flue."},
             ]},
            {"id": "node/passage", "intent": "goal-chamber", "note": "The passage behind the hearth, three wide, the keeper's shelves at its end."},
        ],
    }))
    write("site-plan.json", doc("site-plan", {
        "boxes": [
            {"ceiling": {"clearance": 7}, "extent": [12, 10], "floor": {"datum": "datum/grade"}, "min": [8, 16], "node": "node/hall"},
            {"ceiling": {"clearance": 4}, "extent": [5, 4], "floor": {"datum": "datum/grade"}, "node": "node/porch"},
            {"ceiling": {"clearance": 3}, "extent": [3, 10], "floor": {"datum": "datum/grade"}, "node": "node/passage"},
        ],
        "datums": [
            {"id": "datum/grade", "note": "The hall's floor, and the porch's and the passage's.", "y": 64},
        ],
        "fill": {"block": "minecraft:tuff", "kind": "solid"},
        "identities": [
            {"cmp": "eq", "fact": "fact/site-span", "measure": {"axis": "x", "of": "region-extent"}},
            {"cmp": "eq", "fact": "fact/site-depth", "measure": {"axis": "z", "of": "region-extent"}},
            {"cmp": "eq", "fact": "fact/site-height", "measure": {"axis": "y", "of": "region-extent"}},
        ],
        "lighting": {"fixture": "torch", "min_light": 7},
        "region": {"extent": [32, 24, 40], "min": [0, 52, 0]},
        "seams": [
            {"at": 2, "edge": "edge/porch-door", "face": "north", "form": "a plain door from the porch into the hall", "meets": 7, "opening": "door"},
            {"at": 2, "edge": "edge/hearth-door", "face": "north", "form": "the great hearth's mouth, three wide, the brick back of the firebox behind it and the fire on the hearth stone before it; a door into the passage when the fire is out", "meets": 0, "opening": "passage"},
        ],
    }))


def quests():
    fire_out = [
        {"flag": "flag/hearth-out", "type": "set-flag"},
        {"anchor": "anchor/hearth-fire", "type": "open-gate",
         "happening": {"subject": "anchor/hearth-fire", "text": "The fire on the hearth stone hisses out, and its embers wash down into the flue.", "verb": "opens"}},
        {"anchor": "anchor/seam-hearth-door", "type": "open-gate",
         "happening": {"subject": "anchor/seam-hearth-door", "text": "The brick back of the firebox swings away into the dark, and the passage behind it stands open.", "verb": "opens"}},
        {"type": "cutscene", "seconds": 4,
         "look_at": {"anchor": "anchor/seam-hearth-door"},
         "path": [{"anchor": "anchor/seam-hearth-door", "offset": [1, 2, 7]}, {"anchor": "anchor/seam-hearth-door", "offset": [1, 1, 4]}]},
        {"style": "chat", "text": "Water roars down the flue. The fire hisses out, and the back of the firebox swings into the dark: behind the hearth, a passage runs on into the rock.", "type": "narrate"},
    ]
    return doc("quests", {
        "quests": [
            {
                "cast": {},
                "happening": {"subject": "anchor/node-porch", "text": "The hand comes in by the porch and finds the great hearth burning.", "verb": "arrives"},
                "id": "quest/the-fire",
                "objectives": [{
                    "anchor": "anchor/valve",
                    "happening": {"subject": "anchor/seam-hearth-door", "text": "The hand turns the valve, and water floods the flue.", "verb": "opens"},
                    "hint": "The valve is on the wall to the right of the great hearth, as you face its fire.",
                    "id": "obj/turn-the-valve",
                    "prop": {"block": "minecraft:lever[face=wall,facing=west,powered=false]"},
                    "title": "Pull the valve beside the hearth", "type": "interact",
                }],
                "on_complete": [],
                "on_objective_complete": {"obj/turn-the-valve": fire_out},
                "trigger": {"type": "campaign-start"},
            },
            {
                "cast": {},
                "happening": {"subject": "anchor/seam-hearth-door", "text": "The hand goes to the cold hearth.", "verb": "learns"},
                "id": "quest/the-way",
                "objectives": [{
                    "anchor": "anchor/node-passage", "radius": 2,
                    "happening": {"subject": "anchor/node-passage", "text": "The hand walks through the cold hearth into the passage.", "verb": "arrives"},
                    "hint": "The hearth's fire is out. Go through it into the passage behind it.",
                    "id": "obj/enter-the-passage",
                    "title": "Go through the hearth into the passage", "type": "reach-anchor",
                }],
                "on_complete": [
                    {"style": "subtitle", "text": "The keeper's passage is found.", "type": "narrate"},
                    {"type": "campaign-complete",
                     "happening": {"subject": "anchor/node-passage", "text": "The keeper's passage is reached.", "verb": "opens"}},
                ],
                "on_objective_complete": {},
                "trigger": {"quest": "quest/the-fire", "type": "quest-complete"},
            },
        ],
        "triggers": [
            {"at": "anchor/node-hall", "id": "trigger/the-burning-hearth", "on": {"on": "approach", "range": 6}, "once": True,
             "effects": [{"style": "chat", "text": "The great hearth burns, as it has since the keeper's grandfather lit it. The valve that floods its flue is on the wall to its right.", "type": "narrate"}]},
        ],
    })


ZH = {
    "The keeper sent for a hand to turn the old valve and put out the great hearth of the hall, which has burned for three generations.": "看守请来一个帮手，去拧开那只老阀门，浇灭大厅里烧了三代人的大壁炉。",
    "Hand's sword": "帮手的剑",
    "Hand's boots": "帮手的靴子",
    "Keeper's Hand": "看守的帮手",
    "Water roars down the flue. The fire hisses out, and the back of the firebox swings into the dark: behind the hearth, a passage runs on into the rock.": "水轰隆隆灌下烟道。火嘶的一声灭了，炉膛的砖背向黑暗里转开：壁炉后面，一条密道一直钻进岩石里。",
    "The keeper's passage is found.": "看守的密道找到了。",
    "The great hearth burns, as it has since the keeper's grandfather lit it. The valve that floods its flue is on the wall to its right.": "大壁炉烧着，自从看守的祖父点着它就没熄过。能把烟道灌满水的阀门在它右手边的墙上。",
    "The valve is on the wall to the right of the great hearth, as you face its fire.": "面朝壁炉的火，阀门就在它右手边的墙上。",
    "Pull the valve beside the hearth": "拉开壁炉旁的阀门",
    "The hearth's fire is out. Go through it into the passage behind it.": "壁炉的火灭了。穿过它，进到它后面的密道里。",
    "Go through the hearth into the passage": "穿过壁炉进入密道",
    "Come into the keeper's hall and turn the valve to the right of the great hearth, which floods the flue and puts out the fire.": "走进看守的大厅，拧开大壁炉右手边的阀门，让水灌满烟道，浇灭炉火。",
    "Go through the cold hearth into the passage behind it.": "穿过熄了火的壁炉，进到它后面的密道里。",
    "The hearth stands cold and open, and the keeper's hall is quiet.": "壁炉冷了，敞着，看守的大厅安静了下来。",
    "A Hidden Way": "暗道",
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
