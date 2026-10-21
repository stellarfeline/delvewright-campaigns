#!/usr/bin/env python3
"""Write the stage documents of Three Ways Shut (everything but the programs).

    python3 campaigns/three-ways-shut/design/build_documents.py

The documents are the artifact; this script is how they were typed, kept so a
change to one place's numbers is made once.
"""
import json
import pathlib

CID = "three-ways-shut"
V = "0.59.0"
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
        "outro": "The arch stands open behind you, and the toll yard is a way through again.",
        "premise": "The toll yard at Ashford Cut has been shut since the floods. Every way out of it is closed in its own fashion: the arch to the inner court is barred where everyone can see it, the toll house door is bolted from its own side, the keeper's hatch on the ledge is locked, and the old cart road behind the yard's fireplace has not been walked in years. The keeper left a key in the chest at the end of the passage. Somebody has to fetch it, open the cart road, and raise the bars on the arch from the toll house.",
        "seed": 20261020,
        "target_minutes": 10,
        "theme": "A walled toll yard under a timber roof, every way out of it shut a different way, and the one honest way round.",
        "time": "day",
        "title": "Three Ways Shut",
        "weather": "clear",
    }))
    write("npcs.json", doc("npcs", {"npcs": []}))
    write("dialogue.json", doc("dialogue", {"dialogues": []}))
    write("classes.json", doc("classes", {"classes": [{
        "blurb": "The toll company sends a runner when a yard is shut too long. This season it is you: find the keeper's key and open the way through.",
        "id": "class/runner",
        "kit": [
            {"count": 1, "item": "minecraft:iron_sword", "name": "Runner's sword"},
            {"count": 1, "item": "minecraft:leather_boots", "name": "Runner's boots"},
            {"count": 6, "item": "minecraft:bread"},
        ],
        "name": "Toll Runner",
    }]}))
    write("geometry-brief.json", doc("geometry-brief", {"facts": [
        {"id": "fact/site-span", "note": "Forty-eight blocks east to west: the yard, the passage, the toll house and the rock round them.", "unit": "blocks", "value": 48},
        {"id": "fact/site-depth", "note": "Forty-eight blocks north to south: the court north of the yard, the cart road south of it, and rock on every side.", "unit": "blocks", "value": 48},
        {"id": "fact/site-height", "note": "Thirty-two blocks from under the cart road to over the yard's roof.", "unit": "blocks", "value": 32},
        {"id": "fact/yard-span", "note": "The yard is sixteen blocks across, so the barred arch on its far side is read from the gate the party comes in by.", "unit": "blocks", "value": 16},
    ]}))
    write("quest-plan.json", doc("quest-plan", {
        "finale": "quest/the-way-through",
        "quests": [
            {"act": 1, "area": "area/site", "depends_on": [], "goal": "Arrive in the shut toll yard, find the keeper's key in the chest at the end of the passage, beside the bolted toll house door, and with it open the old cart road behind the yard's fireplace.", "id": "quest/the-key", "mandatory": True, "npcs": []},
            {"act": 1, "area": "area/site", "depends_on": ["quest/the-key"], "goal": "Walk the cart road to the toll house, pull the lever that raises the bars on the yard's arch, draw the bolt of the toll house door, and go through the arch into the inner court.", "id": "quest/the-way-through", "mandatory": True, "npcs": []},
        ],
    }))
    write("layout-graph.json", doc("layout-graph", {
        "beats": [
            {"node": "node/passage", "objective": "obj/take-the-key", "quest": "quest/the-key"},
            {"node": "node/hall", "objective": "obj/pull-the-lever", "quest": "quest/the-way-through"},
            {"node": "node/court", "objective": "obj/enter-the-court", "quest": "quest/the-way-through"},
        ],
        "critical_path": ["node/yard", "node/passage", "node/yard", "node/corridor", "node/hall", "node/corridor", "node/yard", "node/court"],
        "edges": [
            {"a": "node/yard", "b": "node/court", "class": "walk", "id": "edge/court-arch",
             "gating": {"flags": ["flag/arch-raised"], "learned": "seen"}},
            {"a": "node/yard", "b": "node/passage", "class": "walk", "id": "edge/passage-door"},
            {"a": "node/passage", "b": "node/hall", "class": "walk", "id": "edge/toll-door", "shortcut": True,
             "gating": {"flags": ["flag/bolt-drawn"], "learned": "told", "opens_from": "b"}},
            {"a": "node/yard", "b": "node/ledge", "class": "stair", "id": "edge/keeper-stair"},
            {"a": "node/ledge", "b": "node/corridor", "class": "drop", "falls": "a-to-b", "id": "edge/keeper-hatch",
             "gating": {"flags": ["flag/key-taken"], "learned": "rewarded"}},
            {"a": "node/yard", "b": "node/corridor", "class": "walk", "id": "edge/cart-road",
             "gating": {"flags": ["flag/key-taken"]}},
            {"a": "node/corridor", "b": "node/hall", "class": "walk", "id": "edge/road-end"},
        ],
        "entry": "node/yard",
        "goal": "node/court",
        "nodes": [
            {"id": "node/yard", "intent": "hub", "note": "The toll yard, under a timber roof: the party arrives by its south wall. The barred arch to the court stands straight across it; the passage to the toll house opens off its east side; the keeper's stair climbs its south wall; the cart road's mouth is hidden behind the fireplace in its south wall, beside the stair's foot.",
             "stations": [
                 {"anchor": "anchor/hearth-fire", "kind": "gate", "note": "The embers on the fireplace's hearth stone, before the cart road's hidden mouth, cleared when the road is opened."},
             ]},
            {"id": "node/court", "intent": "goal-chamber", "note": "The inner court beyond the barred arch: the way through, once the bars are raised."},
            {"id": "node/passage", "intent": "side-room", "note": "A short passage off the yard to the toll house door, which is bolted on the toll house's side; the keeper's key is in the chest beside it.",
             "stations": [
                 {"anchor": "anchor/key-chest", "kind": "point", "note": "The chest at the end of the passage, beside the bolted door."},
             ]},
            {"id": "node/hall", "intent": "side-room", "note": "The toll house: the lever that raises the arch's bars, and the bolt of the passage door.",
             "stations": [
                 {"anchor": "anchor/arch-lever", "kind": "point", "note": "The lever on the toll house wall that raises the bars on the yard's arch."},
             ]},
            {"id": "node/ledge", "intent": "cache", "note": "The keeper's walk along the top of the yard's south wall, up a side stair: the keeper's purse in a chest, and a hatch in its floor over the cart road, locked until the key is taken.",
             "stations": [
                 {"anchor": "anchor/purse-chest", "kind": "point", "note": "The keeper's chest on the ledge, beside the hatch, with the purse in it."},
             ]},
            {"id": "node/corridor", "intent": "connector", "note": "The old cart road: a long covered way south of the yard from the yard's fireplace at its mouth to the toll house."},
        ],
    }))

    write("site-plan.json", doc("site-plan", {
        "boxes": [
            {"ceiling": {"clearance": 9}, "extent": [16, 14], "floor": {"datum": "datum/grade"}, "min": [8, 14], "node": "node/yard"},
            {"ceiling": {"clearance": 5}, "extent": [10, 8], "floor": {"datum": "datum/grade"}, "node": "node/court"},
            {"ceiling": {"clearance": 4}, "extent": [8, 5], "floor": {"datum": "datum/grade"}, "node": "node/passage"},
            {"ceiling": {"clearance": 5}, "extent": [10, 14], "floor": {"datum": "datum/grade"}, "node": "node/hall"},
            {"ceiling": {"clearance": 3}, "extent": [8, 5], "floor": {"datum": "datum/ledge"}, "node": "node/ledge"},
            {"ceiling": {"clearance": 4}, "extent": [34, 5], "floor": {"datum": "datum/grade"}, "node": "node/corridor"},
        ],
        "datums": [
            {"id": "datum/grade", "note": "The yard's floor, and every floor at the yard's level.", "y": 64},
            {"id": "datum/ledge", "note": "The keeper's walk, five over the yard floor.", "y": 69},
        ],
        "fill": {"block": "minecraft:tuff", "kind": "solid"},
        "identities": [
            {"cmp": "eq", "fact": "fact/site-span", "measure": {"axis": "x", "of": "region-extent"}},
            {"cmp": "eq", "fact": "fact/site-depth", "measure": {"axis": "z", "of": "region-extent"}},
            {"cmp": "eq", "fact": "fact/site-height", "measure": {"axis": "y", "of": "region-extent"}},
            {"cmp": "eq", "fact": "fact/yard-span", "measure": {"axis": "x", "node": "node/yard", "of": "box-extent"}},
        ],
        "lighting": {"fixture": "torch", "min_light": 7},
        "region": {"extent": [48, 32, 48], "min": [0, 48, 0]},
        "seams": [
            {"at": 6, "edge": "edge/court-arch", "face": "north", "form": "an arch in the yard's far wall into the inner court, barred across", "meets": 3, "opening": "arch"},
            {"at": 6, "edge": "edge/passage-door", "face": "east", "form": "an open doorway in the yard's east wall into the passage", "meets": 1, "opening": "door"},
            {"at": 1, "edge": "edge/toll-door", "face": "east", "form": "the toll house door at the passage's end, two wide, bolted on the toll house side", "meets": 6, "opening": {"height": 2, "width": 2}},
            {"at": 1, "edge": "edge/keeper-stair", "face": "south", "form": "a stone stair up the yard's south wall to the keeper's walk", "meets": 1, "opening": "passage", "stair_in": "node/yard"},
            {"at": [3, 2], "edge": "edge/keeper-hatch", "face": "down", "form": "a hatch in the keeper's walk, over the cart road", "meets": [3, 2], "opening": {"height": 1, "width": 1}},
            {"at": 11, "edge": "edge/cart-road", "face": "south", "form": "the mouth of the old cart road in the yard's south wall, three wide, hidden behind the yard's fireplace: its fireback is the road's bar and the embers on its hearth stone stand before it", "meets": 11, "opening": "passage"},
            {"at": 30, "edge": "edge/road-end", "face": "north", "form": "the cart road's end, an open doorway into the toll house", "meets": 4, "opening": "door"},
        ],
    }))


def quests():
    key_taken = [
        {"flag": "flag/key-taken", "type": "set-flag"},
        {"anchor": "anchor/hearth-fire", "type": "open-gate",
         "happening": {"subject": "anchor/hearth-fire", "text": "The embers on the yard's hearth stone are raked away.", "verb": "opens"}},
        {"anchor": "anchor/seam-cart-road", "type": "open-gate",
         "happening": {"subject": "anchor/seam-cart-road", "text": "The fireback at the back of the yard's fireplace swings away, and the cart road's mouth stands open behind it.", "verb": "opens"}},
        {"anchor": "anchor/seam-keeper-hatch", "type": "open-gate",
         "happening": {"subject": "anchor/seam-keeper-hatch", "text": "The keeper's hatch on the ledge falls open over the cart road.", "verb": "opens"}},
        {"type": "cutscene", "seconds": 4,
         "look_at": {"anchor": "anchor/seam-cart-road"},
         "path": [{"anchor": "anchor/seam-cart-road", "offset": [1, 2, -7]}, {"anchor": "anchor/seam-cart-road", "offset": [1, 1, -4]}]},
        {"style": "chat", "text": "The key turns the cart road's lock. The embers go out on the yard's fireplace beside the stair, its fireback swings away, and the old road's mouth stands open behind it, as wide as the stair. Up on the keeper's walk, the hatch has fallen open too.", "type": "narrate"},
    ]
    return doc("quests", {
        "quests": [
            {
                "cast": {},
                "happening": {"subject": "anchor/node-yard", "text": "The runner comes into the shut toll yard and finds every way out of it closed.", "verb": "arrives"},
                "id": "quest/the-key",
                "objectives": [{
                    "anchor": "anchor/key-chest", "count": 1, "holder": "anchor/key-chest",
                    "happening": {"subject": "item/keepers-key", "text": "The runner takes the keeper's key from the chest at the end of the passage.", "verb": "gains"},
                    "hint": "Go through the doorway in the yard's side wall. The chest is at the end of the passage, beside the bolted door.",
                    "id": "obj/take-the-key", "item": "minecraft:tripwire_hook", "item_name": "The keeper's key",
                    "title": "Take the keeper's key", "type": "collect",
                }],
                "on_complete": [],
                "on_objective_complete": {"obj/take-the-key": key_taken},
                "trigger": {"type": "campaign-start"},
            },
            {
                "cast": {},
                "happening": {"subject": "anchor/seam-court-arch", "text": "The runner goes the long way round to raise the bars on the arch.", "verb": "learns"},
                "id": "quest/the-way-through",
                "objectives": [
                    {
                        "anchor": "anchor/arch-lever",
                        "happening": {"subject": "anchor/seam-court-arch", "text": "The runner pulls the lever in the toll house, and the bars on the yard's arch go up.", "verb": "opens"},
                        "hint": "Walk the cart road to its end. The lever is on the toll house floor, by the wall.",
                        "id": "obj/pull-the-lever",
                        "prop": {"block": "minecraft:lever[face=floor,facing=north,powered=false]"},
                        "title": "Pull the lever in the toll house", "type": "interact",
                    },
                    {
                        "after": ["obj/pull-the-lever"],
                        "anchor": "anchor/node-court", "radius": 2,
                        "happening": {"subject": "anchor/node-court", "text": "The runner walks through the open arch into the inner court.", "verb": "arrives"},
                        "hint": "The barred arch is across the yard from the stair. Draw the bolt of the toll house door to go back by the short way.",
                        "id": "obj/enter-the-court",
                        "title": "Go through the arch into the court", "type": "reach-anchor",
                    },
                ],
                "on_complete": [
                    {"style": "subtitle", "text": "The way through is open.", "type": "narrate"},
                    {"type": "campaign-complete",
                     "happening": {"subject": "anchor/node-court", "text": "The toll yard is a way through again.", "verb": "opens"}},
                ],
                "on_objective_complete": {"obj/pull-the-lever": [
                    {"flag": "flag/arch-raised", "type": "set-flag"},
                    {"anchor": "anchor/seam-court-arch", "type": "open-gate",
                     "happening": {"subject": "anchor/seam-court-arch", "text": "The bars on the yard's arch go up into the stone.", "verb": "opens"}},
                ]},
                "trigger": {"quest": "quest/the-key", "type": "quest-complete"},
            },
        ],
        "loot": [{"anchor": "anchor/purse-chest", "id": "loot/keepers-purse",
                  "items": [{"count": 5, "item": "minecraft:emerald"}, {"count": 3, "item": "minecraft:cooked_beef"}]}],
        "shortcuts": [{
            "gate": "anchor/seam-toll-door", "id": "shortcut/toll-door", "unlock": "anchor/unlock-toll-door",
            "on_unlock": [
                {"flag": "flag/bolt-drawn", "type": "set-flag"},
                {"style": "chat", "text": "The bolt slides back. The passage to the yard is one door away now.", "type": "narrate"},
            ],
        }],
        "triggers": [
            {"at": "anchor/node-yard", "id": "trigger/the-shut-yard", "on": {"on": "approach", "range": 6}, "once": True,
             "effects": [{"style": "chat", "text": "The toll yard has been shut since the floods. The arch to the court is barred, the toll house door is bolted from its own side, and the keeper's hatch is locked. The keeper left the key in the chest at the end of the passage.", "type": "narrate"}]},
            {"at": "anchor/seam-toll-door", "audience": "presser", "id": "trigger/toll-door-wrong-side", "on": {"on": "use"}, "once": False,
             "effects": [{"style": "actionbar", "text": "The door is bolted from the toll house side.", "type": "narrate"}]},
        ],
    })


ZH = {
    "The toll company sends a runner when a yard is shut too long. This season it is you: find the keeper's key and open the way through.": "关卡一关得太久，收费公司就会派个跑腿的来。今年轮到你：找到看守的钥匙，把路重新打通。",
    "Runner's sword": "跑腿人的剑",
    "Runner's boots": "跑腿人的靴子",
    "Toll Runner": "收费跑腿人",
    "The bolt slides back. The passage to the yard is one door away now.": "门闩滑开了。回院子的过道，如今只隔一扇门。",
    "The key turns the cart road's lock. The embers go out on the yard's fireplace beside the stair, its fireback swings away, and the old road's mouth stands open behind it, as wide as the stair. Up on the keeper's walk, the hatch has fallen open too.": "钥匙拧开了车道的锁。石阶旁那座壁炉里的余烬熄了，炉背转开，后面露出旧车道的入口，和石阶一样宽。上面看守走道里的活板门也落开了。",
    "The way through is open.": "路通了。",
    "The toll yard has been shut since the floods. The arch to the court is barred, the toll house door is bolted from its own side, and the keeper's hatch is locked. The keeper left the key in the chest at the end of the passage.": "自从那场洪水，收费院就一直关着。通往内院的拱门被铁栏封着，收费房的门从里头闩上了，看守的活板门也锁着。看守把钥匙留在了过道尽头的箱子里。",
    "The door is bolted from the toll house side.": "这扇门是从收费房那一侧闩上的。",
    "Go through the doorway in the yard's side wall. The chest is at the end of the passage, beside the bolted door.": "穿过院子侧墙上的门洞。箱子在过道尽头，就在那扇闩上的门旁边。",
    "The keeper's key": "看守的钥匙",
    "Take the keeper's key": "取看守的钥匙",
    "The barred arch is across the yard from the stair. Draw the bolt of the toll house door to go back by the short way.": "封着铁栏的拱门在院子另一头，与石阶相对。拉开收费房门的门闩，就能抄近路回去。",
    "Go through the arch into the court": "穿过拱门进入内院",
    "Walk the cart road to its end. The lever is on the toll house floor, by the wall.": "沿车道走到尽头。拉杆在收费房的地上，靠着墙。",
    "Pull the lever in the toll house": "拉动收费房里的拉杆",
    "Arrive in the shut toll yard, find the keeper's key in the chest at the end of the passage, beside the bolted toll house door, and with it open the old cart road behind the yard's fireplace.": "来到关闭的收费院，在过道尽头、那扇闩上的收费房门旁的箱子里找到看守的钥匙，用它打开院中壁炉后面的旧车道。",
    "Walk the cart road to the toll house, pull the lever that raises the bars on the yard's arch, draw the bolt of the toll house door, and go through the arch into the inner court.": "沿车道走到收费房，拉动升起院中拱门铁栏的拉杆，拉开收费房门的门闩，再穿过拱门进入内院。",
    "The arch stands open behind you, and the toll yard is a way through again.": "拱门在你身后敞开，收费院又成了一条通路。",
    "Three Ways Shut": "三道封路",
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
    import sys
    if len(sys.argv) > 1:
        write("l10n/zh-cn.json", l10n(json.loads(pathlib.Path(sys.argv[1]).read_text())))
