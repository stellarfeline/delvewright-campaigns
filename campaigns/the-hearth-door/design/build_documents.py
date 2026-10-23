#!/usr/bin/env python3
"""Write the stage documents of The Hearth Door (everything but the programs).

    python3 campaigns/the-hearth-door/design/build_documents.py [l10n-inventory.json]

The documents are the artifact; this script is how they were typed, kept so a
change to one place's numbers is made once. Given the engine's l10n inventory
(`delvec l10n-inventory`), it also writes the zh-CN sidecar.
"""
import json
import pathlib
import sys

CID = "the-hearth-door"
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
        "outro": "The hearth stands open and cold, and the wardens' hall is quiet again.",
        "premise": "The wardens of Coldharbour kept their hall's great hearth burning for a hundred years and never let it die. The fire still burns. The sluice that floods its flue is up in Wardens' Lane, at the head of the stone stair, and the clerk the wardens sent for is to turn it.",
        "seed": 20261021,
        "target_minutes": 10,
        "theme": "A stone hall with a broad stair three wide up to a lane under the sky, a great hearth beside the stair's foot, and a newel beside the stair and a lamp post beside the lane, each outside the way's width.",
        "time": "day",
        "title": "The Hearth Door",
        "weather": "clear",
    }))
    write("npcs.json", doc("npcs", {"npcs": []}))
    write("dialogue.json", doc("dialogue", {"dialogues": []}))
    write("classes.json", doc("classes", {"classes": [{
        "blurb": "The wardens sent for a clerk to read their old records, and to put out the great hearth of their hall, which nobody has let go out in a hundred years.",
        "id": "class/clerk",
        "kit": [
            {"count": 1, "item": "minecraft:iron_sword", "name": "Clerk's sword"},
            {"count": 1, "item": "minecraft:leather_boots", "name": "Clerk's boots"},
            {"count": 6, "item": "minecraft:bread"},
        ],
        "name": "Warden's Clerk",
    }]}))
    write("geometry-brief.json", doc("geometry-brief", {"facts": [
        {"id": "fact/site-span", "note": "Forty blocks east to west: the hall, the lane east of it and the rock round them.", "unit": "blocks", "value": 40},
        {"id": "fact/site-depth", "note": "Forty-eight blocks north to south: the passage north of the hall, the lane running south past it, and rock on every side.", "unit": "blocks", "value": 48},
        {"id": "fact/site-height", "note": "Thirty-two blocks from under the hall's floor to the sky over the lane.", "unit": "blocks", "value": 32},
        {"id": "fact/stair-rise", "note": "The stair climbs five courses from the hall's floor to the lane.", "unit": "blocks", "value": 5},
    ]}))
    write("quest-plan.json", doc("quest-plan", {
        "finale": "quest/the-records",
        "quests": [
            {"act": 1, "area": "area/site", "depends_on": [], "goal": "Arrive in the wardens' hall, climb the broad stair to Wardens' Lane, and turn the sluice at the lane's end that floods the flue and puts out the great hearth.", "id": "quest/the-fire", "mandatory": True, "npcs": []},
            {"act": 1, "area": "area/site", "depends_on": ["quest/the-fire"], "goal": "Go back down the stair and through the cold hearth into the wardens' passage behind the hearth, where the records are kept.", "id": "quest/the-records", "mandatory": True, "npcs": []},
        ],
    }))
    write("layout-graph.json", doc("layout-graph", {
        "beats": [
            {"node": "node/lane", "objective": "obj/turn-the-sluice", "quest": "quest/the-fire"},
            {"node": "node/passage", "objective": "obj/enter-the-passage", "quest": "quest/the-records"},
        ],
        "critical_path": ["node/porch", "node/hall", "node/lane", "node/hall", "node/passage"],
        "edges": [
            {"a": "node/porch", "b": "node/hall", "class": "walk", "id": "edge/porch-door"},
            {"a": "node/hall", "b": "node/lane", "class": "stair", "id": "edge/hall-stair"},
            {"a": "node/hall", "b": "node/passage", "class": "walk", "id": "edge/hearth-door",
             "gating": {"flags": ["flag/hearth-out"], "learned": "hidden",
                        "secret": ["passage", "behind the hearth", "密道"]}},
        ],
        "entry": "node/porch",
        "goal": "node/passage",
        "nodes": [
            {"id": "node/porch", "intent": "entrance", "note": "The porch the clerk comes in by, south of the hall: a door into the hall."},
            {"id": "node/hall", "intent": "hub", "note": "The wardens' hall: a broad stone stair three wide climbs its east wall to the lane, a newel post on the floor beside its foot, and the great hearth stands in its north wall beside the stair's foot, its fire before the brick back of the firebox.",
             "stations": [
                 {"anchor": "anchor/hearth-fire", "kind": "gate", "note": "The fire on the hearth stone before the mouth, put out and washed away when the flue floods."},
             ]},
            {"id": "node/lane", "intent": "connector", "note": "Wardens' Lane, open to the sky at the head of the stair: a street four wide with a lamp post on its verge half-way along, and the flue's sluice at its far end.",
             "stations": [
                 {"anchor": "anchor/sluice", "kind": "point", "note": "The sluice lever at the lane's south end, which floods the flue."},
             ]},
            {"id": "node/passage", "intent": "goal-chamber", "note": "The wardens' passage behind the hearth: as wide as the stair, and the records at its end."},
        ],
    }))
    write("site-plan.json", doc("site-plan", {
        "boxes": [
            {"ceiling": {"clearance": 9}, "extent": [14, 10], "floor": {"datum": "datum/grade"}, "min": [8, 20], "node": "node/hall"},
            {"ceiling": {"clearance": 4}, "extent": [5, 4], "floor": {"datum": "datum/grade"}, "node": "node/porch"},
            {"ceiling": {"open": 4}, "extent": [5, 16], "floor": {"datum": "datum/lane"}, "node": "node/lane",
             "way": {"at": 0, "axis": "z", "clear": 4}},
            {"ceiling": {"clearance": 3}, "extent": [3, 12], "floor": {"datum": "datum/grade"}, "node": "node/passage"},
        ],
        "datums": [
            {"id": "datum/grade", "note": "The hall's floor, and the passage's behind the hearth.", "y": 64},
            {"id": "datum/lane", "note": "Wardens' Lane, five over the hall floor at the head of the stair.", "y": 69},
        ],
        "fill": {"block": "minecraft:tuff", "kind": "solid"},
        "identities": [
            {"cmp": "eq", "fact": "fact/site-span", "measure": {"axis": "x", "of": "region-extent"}},
            {"cmp": "eq", "fact": "fact/site-depth", "measure": {"axis": "z", "of": "region-extent"}},
            {"cmp": "eq", "fact": "fact/site-height", "measure": {"axis": "y", "of": "region-extent"}},
        ],
        "lighting": {"fixture": "torch", "min_light": 7},
        "region": {"extent": [40, 32, 48], "min": [0, 48, 0]},
        "volumes": [
            {"id": "volume/sky-over-the-lane", "note": "The sky Wardens' Lane is open to, kept clear from the top of its headroom to the top of the site: in rock, a cut open to the sky.",
             "region": {"extent": [5, 7, 16], "min": [23, 73, 20]}, "role": "clearance"},
        ],
        "seams": [
            {"at": 0, "edge": "edge/hall-stair", "face": "east", "form": "a stone stair three wide up the hall's east wall to the lane, a newel post on the floor beside its foot", "meets": 0, "opening": "passage", "stair_in": "node/hall"},
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
        {"style": "chat", "text": "Water roars down the flue. The fire on the great hearth hisses out and washes away, and the back of the firebox swings into the dark: behind the hearth, at the stair's foot, the wardens' passage is open.", "type": "narrate"},
    ]
    return doc("quests", {
        "quests": [
            {
                "cast": {},
                "happening": {"subject": "anchor/node-porch", "text": "The clerk comes in by the porch and finds the great hearth burning.", "verb": "arrives"},
                "id": "quest/the-fire",
                "objectives": [{
                    "anchor": "anchor/sluice",
                    "happening": {"subject": "anchor/seam-hearth-door", "text": "The clerk turns the sluice at the end of Wardens' Lane, and water floods the flue.", "verb": "opens"},
                    "hint": "Climb the broad stair beside the hearth to Wardens' Lane. The sluice is at the lane's far end.",
                    "id": "obj/turn-the-sluice",
                    "prop": {"block": "minecraft:lever[face=floor,facing=north,powered=false]"},
                    "title": "Pull the sluice at the lane's end", "type": "interact",
                }],
                "on_complete": [],
                "on_objective_complete": {"obj/turn-the-sluice": fire_out},
                "trigger": {"type": "campaign-start"},
            },
            {
                "cast": {},
                "happening": {"subject": "anchor/seam-hearth-door", "text": "The clerk goes back down to the cold hearth.", "verb": "learns"},
                "id": "quest/the-records",
                "objectives": [{
                    "anchor": "anchor/node-passage", "radius": 2,
                    "happening": {"subject": "anchor/node-passage", "text": "The clerk walks through the cold hearth into the wardens' passage.", "verb": "arrives"},
                    "hint": "Go back down the stair. The hearth is at its foot, and its fire is out.",
                    "id": "obj/enter-the-passage",
                    "title": "Go through the hearth into the passage", "type": "reach-anchor",
                }],
                "on_complete": [
                    {"style": "subtitle", "text": "The wardens' passage is open.", "type": "narrate"},
                    {"type": "campaign-complete",
                     "happening": {"subject": "anchor/node-passage", "text": "The wardens' records are reached.", "verb": "opens"}},
                ],
                "on_objective_complete": {},
                "trigger": {"quest": "quest/the-fire", "type": "quest-complete"},
            },
        ],
        "triggers": [
            {"at": "anchor/node-hall", "id": "trigger/the-burning-hearth", "on": {"on": "approach", "range": 6}, "once": True,
             "effects": [{"style": "chat", "text": "The great hearth burns, as it has for a hundred years. The sluice that floods its flue is up the stair, at the end of Wardens' Lane.", "type": "narrate"}]},
        ],
    })


ZH = {
    "The wardens sent for a clerk to read their old records, and to put out the great hearth of their hall, which nobody has let go out in a hundred years.": "守卫们请来一位书记，去读他们的旧档案，还要浇灭大厅里那座大壁炉——一百年来没人让它熄过。",
    "Clerk's sword": "书记的剑",
    "Clerk's boots": "书记的靴子",
    "Warden's Clerk": "守卫书记",
    "Water roars down the flue. The fire on the great hearth hisses out and washes away, and the back of the firebox swings into the dark: behind the hearth, at the stair's foot, the wardens' passage is open.": "水轰隆隆灌下烟道。炉石上的火嘶的一声灭了，被水冲走，炉膛的砖背向黑暗里转开：壁炉后面，石阶脚下，守卫的密道开了。",
    "The wardens' passage is open.": "守卫的密道开了。",
    "The great hearth burns, as it has for a hundred years. The sluice that floods its flue is up the stair, at the end of Wardens' Lane.": "大壁炉烧着，一烧就是一百年。能把烟道灌满水的闸门在石阶上面，守卫巷的尽头。",
    "Climb the broad stair beside the hearth to Wardens' Lane. The sluice is at the lane's far end.": "沿壁炉旁的宽石阶上到守卫巷。闸门在巷子的另一头。",
    "Pull the sluice at the lane's end": "拉开巷子尽头的闸门",
    "Go back down the stair. The hearth is at its foot, and its fire is out.": "从石阶下去。壁炉就在阶脚，火已经灭了。",
    "Go through the hearth into the passage": "穿过壁炉进入密道",
    "Arrive in the wardens' hall, climb the broad stair to Wardens' Lane, and turn the sluice at the lane's end that floods the flue and puts out the great hearth.": "来到守卫大厅，沿宽石阶上到守卫巷，拉开巷子尽头的闸门，让水灌满烟道，浇灭大壁炉。",
    "Go back down the stair and through the cold hearth into the wardens' passage behind the hearth, where the records are kept.": "回到石阶下，穿过熄了火的壁炉，进入壁炉后面存放档案的守卫密道。",
    "The hearth stands open and cold, and the wardens' hall is quiet again.": "壁炉敞着，冷了下来，守卫大厅又安静了。",
    "The Hearth Door": "壁炉之门",
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
