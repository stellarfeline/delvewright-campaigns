#!/usr/bin/env python3
"""Write the stage documents of The Open Yard (everything but the programs).

    python3 campaigns/the-open-yard/design/build_documents.py [l10n-inventory.json]

The documents are the artifact; this script is how they were typed, kept so a
change to one place's numbers is made once. Given the engine's l10n inventory
(`delvec l10n-inventory`), it also writes the zh-CN sidecar.
"""
import json
import pathlib
import sys

CID = "the-open-yard"
V = "0.65.0"
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
        "horizon": {"attributes": {"audio/background_music": {}}, "base": "void"},
        "languages": ["zh-cn"],
        "min_players": 1,
        "outro": "The fair is set, and the street is ready for market day.",
        "premise": "Market day comes to Ashford tomorrow, and the steward has sent a runner down the high street to see that everything is ready: the fountain court, the smith's open front, the covered market, and the steward's own house at the street's end.",
        "seed": 20261024,
        "target_minutes": 8,
        "theme": "A short high street with four places on it: a fountain court open on every side, a smithy whose street side is an open counter with its door beside, a covered market on four posts and no walls, and a walled house.",
        "time": "day",
        "title": "The Open Yard",
        "weather": "clear",
    }))
    write("npcs.json", doc("npcs", {"npcs": []}))
    write("dialogue.json", doc("dialogue", {"dialogues": []}))
    write("classes.json", doc("classes", {"classes": [{
        "blurb": "The steward's runner, sent down the high street the day before market day to see that everything is ready.",
        "id": "class/runner",
        "kit": [
            {"count": 1, "item": "minecraft:wooden_sword", "name": "Runner's staff"},
            {"count": 6, "item": "minecraft:bread"},
        ],
        "name": "Steward's Runner",
    }]}))
    write("geometry-brief.json", doc("geometry-brief", {"facts": [
        {"id": "fact/site-span", "note": "Thirty-six blocks east to west: the high street and the field walls at either end.", "unit": "blocks", "value": 36},
        {"id": "fact/site-depth", "note": "Thirty blocks north to south: the places north of the street, the house south of it, and the green round them.", "unit": "blocks", "value": 30},
        {"id": "fact/site-height", "note": "Twenty-four blocks from under the street to the sky.", "unit": "blocks", "value": 24},
    ]}))
    write("quest-plan.json", doc("quest-plan", {
        "finale": "quest/market-day",
        "quests": [
            {"act": 1, "area": "area/site", "depends_on": [], "goal": "Walk the high street and look in on every place market day needs: the fountain court, the smith's front, the covered market, and last the steward's house.", "id": "quest/market-day", "mandatory": True, "npcs": []},
        ],
    }))
    write("layout-graph.json", doc("layout-graph", {
        "beats": [
            {"node": "node/court", "objective": "obj/the-fountain", "quest": "quest/market-day"},
            {"node": "node/smithy", "objective": "obj/the-smithy", "quest": "quest/market-day"},
            {"node": "node/market", "objective": "obj/the-market", "quest": "quest/market-day"},
            {"node": "node/house", "objective": "obj/the-house", "quest": "quest/market-day"},
        ],
        "critical_path": ["node/street", "node/court", "node/street", "node/smithy", "node/street", "node/market", "node/street", "node/house"],
        "edges": [
            {"a": "node/street", "b": "node/court", "class": "walk", "id": "edge/court-front"},
            {"a": "node/street", "b": "node/smithy", "class": "walk", "id": "edge/smithy-front"},
            {"a": "node/street", "b": "node/market", "class": "walk", "id": "edge/market-front"},
            {"a": "node/street", "b": "node/house", "class": "walk", "id": "edge/house-door"},
        ],
        "entry": "node/street",
        "goal": "node/house",
        "nodes": [
            {"id": "node/street", "intent": "connector", "note": "Ashford's high street, three wide with a verge on its south side, its lamps on the verge."},
            {"id": "node/court", "intent": "vista", "note": "The fountain court, open on every side: its front on the street, and the green round its other three sides. A fountain in its middle."},
            {"id": "node/smithy", "intent": "landmark", "note": "The smithy: roofed, walled on three sides, its street side open over the counter at the front of the room, its door beside the counter. The anvil and the smithing table behind."},
            {"id": "node/market", "intent": "hub", "note": "The covered market: a roof on four posts at its corners and no walls at all, its stalls under it."},
            {"id": "node/house", "intent": "goal-chamber", "note": "The steward's house at the street's south side, walled all round, its door on the street."},
        ],
    }))
    write("site-plan.json", doc("site-plan", {
        "boxes": [
            {"ceiling": {"open": 4}, "extent": [29, 4], "floor": {"datum": "datum/grade"}, "min": [2, 20], "node": "node/street",
             "way": {"at": 0, "axis": "x", "clear": 3}},
            {"ceiling": {"open": 4}, "extent": [6, 6], "floor": {"datum": "datum/grade"}, "node": "node/court",
             "sides": {"east": "open", "north": "open", "south": "open", "west": "open"}},
            {"ceiling": {"clearance": 4}, "extent": [7, 6], "floor": {"datum": "datum/grade"}, "node": "node/smithy",
             "sides": {"south": "open"}},
            {"ceiling": {"clearance": 4}, "extent": [6, 6], "floor": {"datum": "datum/grade"}, "node": "node/market",
             "sides": {"east": "open", "north": "open", "south": "open", "west": "open"}},
            {"ceiling": {"clearance": 4}, "extent": [6, 5], "floor": {"datum": "datum/grade"}, "node": "node/house"},
        ],
        "datums": [
            {"id": "datum/grade", "note": "The high street and every place on it.", "y": 64},
        ],
        "fill": {"below": "minecraft:dirt", "kind": "open", "surface": "minecraft:grass_block",
                 "terrain": {"datum": "datum/grade", "kind": "flat"}},
        "identities": [
            {"cmp": "eq", "fact": "fact/site-span", "measure": {"axis": "x", "of": "region-extent"}},
            {"cmp": "eq", "fact": "fact/site-depth", "measure": {"axis": "z", "of": "region-extent"}},
            {"cmp": "eq", "fact": "fact/site-height", "measure": {"axis": "y", "of": "region-extent"}},
        ],
        "lighting": {"fixture": "torch", "min_light": 7},
        "region": {"extent": [36, 24, 30], "min": [0, 52, 6]},
        "seams": [
            {"at": 12, "contact": {"extent": [6, 4]}, "edge": "edge/court-front", "face": "north", "form": "the fountain court's front, open along the whole of it", "meets": 0},
            {"at": 2, "contact": {"extent": [7, 4]}, "edge": "edge/smithy-front", "face": "north", "form": "the smith's open front: the counter along most of it, and the door beside", "meets": 0},
            {"at": 21, "contact": {"extent": [6, 4]}, "edge": "edge/market-front", "face": "north", "form": "the covered market's front, open between its corner posts", "meets": 0},
            {"at": 14, "edge": "edge/house-door", "face": "south", "form": "the steward's front door, oak, off the street", "meets": 2, "opening": "door"},
        ],
        "volumes": [
            {"block": "minecraft:mossy_cobblestone", "id": "volume/field-wall-west", "note": "The field wall that closes the green at the west end of the street, two courses high.",
             "region": {"extent": [1, 8, 30], "min": [0, 58, 6]}, "role": "massif"},
            {"block": "minecraft:mossy_cobblestone", "id": "volume/field-wall-east", "note": "The field wall at the east end.",
             "region": {"extent": [1, 8, 30], "min": [35, 58, 6]}, "role": "massif"},
            {"block": "minecraft:mossy_cobblestone", "id": "volume/field-wall-north", "note": "The field wall along the north edge of the green.",
             "region": {"extent": [34, 8, 1], "min": [1, 58, 6]}, "role": "massif"},
            {"block": "minecraft:mossy_cobblestone", "id": "volume/field-wall-south", "note": "The field wall along the south edge of the green.",
             "region": {"extent": [34, 8, 1], "min": [1, 58, 35]}, "role": "massif"},
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
                "happening": {"subject": "anchor/node-street", "text": "The runner comes down Ashford's high street the day before market day.", "verb": "arrives"},
                "id": "quest/market-day",
                "objectives": [
                    reach("obj/the-fountain", "anchor/node-court", "Look in at the fountain court", "The fountain court is the open square off the street, with the fountain in its middle.", "The runner stands by the fountain in the open court."),
                    dict(reach("obj/the-smithy", "anchor/node-smithy", "Step inside the smithy", "The smith's front is open over the counter. The door is beside it.", "The runner steps in through the smith's door, behind the counter."), after=["obj/the-fountain"]),
                    dict(reach("obj/the-market", "anchor/node-market", "Walk under the covered market", "The covered market stands further along the street, a roof on four posts.", "The runner walks in under the market roof."), after=["obj/the-smithy"]),
                    dict(reach("obj/the-house", "anchor/node-house", "Reach the steward's house", "The steward's house is across the street, its oak door on the street.", "The runner goes in at the steward's door."), after=["obj/the-market"]),
                ],
                "on_complete": [
                    {"style": "subtitle", "text": "Ashford is ready for market day.", "type": "narrate"},
                    {"type": "campaign-complete",
                     "happening": {"subject": "anchor/node-house", "text": "The street is ready for market day.", "verb": "opens"}},
                ],
                "on_objective_complete": {},
                "trigger": {"type": "campaign-start"},
            },
        ],
        "triggers": [
            {"at": "anchor/node-street", "id": "trigger/the-high-street", "on": {"on": "approach", "range": 4}, "once": True,
             "effects": [{"style": "chat", "text": "Ashford's high street. The steward wants every place on it looked at before market day: the court, the smith, the market, and his own house last.", "type": "narrate"}]},
        ],
    })


ZH = {
    "The steward's runner, sent down the high street the day before market day to see that everything is ready.": "管事的跑腿，赶集前一天被派到大街上，看看一切是否都准备好了。",
    "Runner's staff": "跑腿的木杖",
    "Steward's Runner": "管事的跑腿",
    "Ashford is ready for market day.": "阿什福德准备好赶集了。",
    "Ashford's high street. The steward wants every place on it looked at before market day: the court, the smith, the market, and his own house last.": "这是阿什福德的大街。管事要你在赶集前把街上每一处都看一遍：喷泉小院、铁匠铺、集市棚，最后是他自己的家。",
    "The fountain court is the open square off the street, with the fountain in its middle.": "喷泉小院就是街边那片敞开的小广场，中间有座喷泉。",
    "Look in at the fountain court": "去喷泉小院看看",
    "The steward's house is across the street, its oak door on the street.": "管事的家在街对面，橡木门朝着大街。",
    "Reach the steward's house": "走到管事的家",
    "The covered market stands further along the street, a roof on four posts.": "集市棚在街的前头，四根柱子撑着一个屋顶。",
    "Walk under the covered market": "走到集市棚底下",
    "The smith's front is open over the counter. The door is beside it.": "铁匠铺的门面越过柜台敞开着，门就在柜台旁边。",
    "Step inside the smithy": "走进铁匠铺",
    "Walk the high street and look in on every place market day needs: the fountain court, the smith's front, the covered market, and last the steward's house.": "沿大街走一趟，把赶集要用的地方都看一遍：喷泉小院、铁匠铺的门面、集市棚，最后是管事的家。",
    "The fair is set, and the street is ready for market day.": "集市都布置好了，这条街就等着赶集了。",
    "The Open Yard": "敞开的院子",
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
