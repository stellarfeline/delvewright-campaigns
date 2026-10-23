#!/usr/bin/env python3
"""Write the stage documents of Two Ways Off the Map (everything but the programs).

    python3 campaigns/two-ways-off-the-map/design/build_documents.py [--sixth] [l10n-inventory.json]

The documents are the artifact; this script is how they were typed, kept so a
change to one place's numbers is made once. `--sixth` also declares the sixth
jump (five columns flat), which the jump proof refuses; the shipped level does
not declare it. Given the engine's l10n inventory (`delvec l10n-inventory`), it
also writes the zh-CN sidecar.
"""
import json
import pathlib
import sys

CID = "two-ways-off-the-map"
V = "0.61.0"
HERE = pathlib.Path(__file__).resolve().parent.parent

# The course's declared jumps, in route order: (id, from anchor, to anchor).
# Every one is sprinted. The anchors are the launch and landing cells the
# course piece marks (`build_pieces.py`).
JUMPS = [
    ("jump/two-flat", "anchor/launch-1", "anchor/land-1"),
    ("jump/three-flat", "anchor/launch-2", "anchor/land-2"),
    ("jump/four-flat", "anchor/launch-3", "anchor/land-3"),
    ("jump/three-up-one", "anchor/launch-4", "anchor/land-4"),
    ("jump/under-the-lid", "anchor/launch-5", "anchor/land-5"),
]
LANGUAGES = []
SIXTH = ("jump/five-flat", "anchor/launch-6", "anchor/land-6")


def doc(stage, content):
    return {"campaign_id": CID, "content": content, "dsl_version": V, "stage": stage}


def write(name, d):
    p = HERE / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def main(sixth):
    jumps = JUMPS + ([SIXTH] if sixth else [])
    write("world.json", doc("world", {
        "areas": [],
        "demo_level": True,
        "boundary": {"margin": 8, "message": "The sea is too cold and too wide out there. You turn back to the rock."},
        "horizon": {"attributes": {"audio/background_music": {}}, "base": "ocean"},
        "jumps": [{"from": a, "id": i, "sprint": True, "to": b} for i, a, b in jumps],
        "languages": LANGUAGES,
        "min_players": 1,
        "outro": "The boat pushes off from the jetty, and the chapel on the rock falls away behind you.",
        "premise": "A chapel stands on a rock in the sea, its yard walled against the wind. The boat that takes you off the rock waits at the end of the jetty, and the only way to the jetty is the old broken wall-walk, leapt gap by gap.",
        "seed": 20261023,
        "target_minutes": 5,
        "theme": "A walled chapel yard with standing stones, a broken wall-walk over a dry cistern, and a plank jetty out into the open sea.",
        "time": "day",
        "title": "Two Ways Off the Map",
        "weather": "clear",
    }))
    write("npcs.json", doc("npcs", {"npcs": []}))
    write("dialogue.json", doc("dialogue", {"dialogues": []}))
    write("classes.json", doc("classes", {"classes": [{
        "blurb": "You came to the rock to see the chapel, and the boat is leaving. Get to the end of the jetty before it goes.",
        "id": "class/visitor",
        "kit": [
            {"count": 4, "item": "minecraft:bread"},
        ],
        "name": "Visitor",
    }]}))
    write("geometry-brief.json", doc("geometry-brief", {"facts": [
        {"id": "fact/site-span", "note": "Ninety-six blocks west to east: the yard, the wall-walk and the jetty in a row, and open sea round them.", "unit": "blocks", "value": 96},
        {"id": "fact/site-depth", "note": "Forty-eight blocks north to south: the yard north of the wall-walk, and open sea round both.", "unit": "blocks", "value": 48},
        {"id": "fact/site-height", "note": "Sixty-four blocks from the bedrock under the sea to the sky over the chapel.", "unit": "blocks", "value": 64},
    ]}))
    write("quest-plan.json", doc("quest-plan", {
        "finale": "quest/the-boat",
        "quests": [
            {"act": 1, "area": "area/site", "depends_on": [], "goal": "Leave the chapel yard by its gate and cross the broken wall-walk, leaping each gap, to the jetty.", "id": "quest/the-wall-walk", "mandatory": True, "npcs": []},
            {"act": 1, "area": "area/site", "depends_on": ["quest/the-wall-walk"], "goal": "Walk out to the end of the jetty, where the boat waits.", "id": "quest/the-boat", "mandatory": True, "npcs": []},
        ],
    }))
    write("layout-graph.json", doc("layout-graph", {
        "beats": [
            {"node": "node/course", "objective": "obj/cross-the-wall-walk", "quest": "quest/the-wall-walk"},
            {"node": "node/jetty", "objective": "obj/end-of-the-jetty", "quest": "quest/the-boat"},
        ],
        "critical_path": ["node/yard", "node/course", "node/jetty"],
        "edges": [
            {"a": "node/yard", "b": "node/course", "class": "walk", "id": "edge/yard-gate"},
            {"a": "node/course", "b": "node/jetty", "class": "walk", "id": "edge/jetty-foot"},
        ],
        "entry": "node/yard",
        "goal": "node/jetty",
        "nodes": [
            {"id": "node/yard", "intent": "entrance", "note": "The chapel yard: the chapel's front along its north wall, standing stones in the grass, a buttress against its east wall, a gate in its south wall onto the wall-walk. Past its east wall, a strip of old burying ground walled high on every side."},
            {"id": "node/course", "intent": "trial", "note": "The broken wall-walk over a dry cistern: stone platforms in a row with gaps a body leaps, the fourth platform raised one and the fifth leap down off it under a stone lid laid across the cistern's walls, and a stair at each end back up out of the cistern.",
             "stations": [
                 {"anchor": "anchor/high-platform", "kind": "point", "note": "The middle of the raised fourth platform, under the stone lid: reached only by the four leaps before it, and left only by the fifth."},
             ] + [st for k, (i, a, b) in enumerate(JUMPS + [SIXTH], start=1) for st in (
                 {"anchor": a, "kind": "point", "note": f"Where the leap `{i}` leaves from: the last cell of a platform, on its middle row."},
                 {"anchor": b, "kind": "point", "note": f"Where the leap `{i}` lands: the first cell of the next platform, on its middle row."},
             ) if sixth or k <= len(JUMPS)]},
            {"id": "node/jetty", "intent": "jetty", "note": "A plank jetty railed along both sides, running east out over the open sea, a loose plank ledge against its north rail, and the boat's mooring at its head.",
             "stations": [
                 {"anchor": "anchor/jetty-head", "kind": "point", "note": "The head of the jetty, where the boat is moored."},
             ]},
        ],
    }))
    write("site-plan.json", doc("site-plan", {
        "boxes": [
            {"ceiling": {"open": 10}, "extent": [19, 15], "floor": {"datum": "datum/grade"}, "min": [8200, 8198], "node": "node/yard"},
            {"ceiling": {"open": 6}, "extent": [58, 7], "floor": {"datum": "datum/grade"}, "node": "node/course"},
            {"ceiling": {"open": 4}, "extent": [22, 5], "floor": {"datum": "datum/grade"}, "node": "node/jetty"},
        ],
        "datums": [
            {"id": "datum/grade", "note": "The yard's grass, the wall-walk's platforms and the jetty's deck: six courses over the sea.", "y": 68},
            {"id": "datum/sea-floor", "note": "The gravel floor under the sea.", "y": 55},
        ],
        "fill": {"below": "minecraft:stone", "kind": "open", "surface": "minecraft:gravel",
                 "terrain": {"datum": "datum/sea-floor", "kind": "flat"}},
        "identities": [
            {"cmp": "eq", "fact": "fact/site-span", "measure": {"axis": "x", "of": "region-extent"}},
            {"cmp": "eq", "fact": "fact/site-depth", "measure": {"axis": "z", "of": "region-extent"}},
            {"cmp": "eq", "fact": "fact/site-height", "measure": {"axis": "y", "of": "region-extent"}},
        ],
        "lighting": {"fixture": "lantern", "min_light": 7},
        "region": {"extent": [96, 64, 48], "min": [8192, 40, 8192]},
        "seams": [
            {"at": 2, "edge": "edge/yard-gate", "face": "south", "form": "an open gateway three wide in the yard's south wall, straight onto the wall-walk's first platform", "meets": 1, "opening": {"height": 3, "width": 3}},
            {"at": 2, "edge": "edge/jetty-foot", "face": "east", "form": "the wall-walk's last platform running on through a gap in the cistern's east wall onto the jetty's deck, three wide", "meets": 1, "opening": {"height": 3, "width": 3}},
        ],
    }))


def quests():
    return doc("quests", {
        "quests": [
            {
                "cast": {},
                "happening": {"subject": "anchor/node-yard", "text": "The visitor stands in the chapel yard as the boat's bell rings from the jetty.", "verb": "arrives"},
                "id": "quest/the-wall-walk",
                "objectives": [{
                    "anchor": "anchor/high-platform", "radius": 1,
                    "happening": {"subject": "anchor/high-platform", "text": "The visitor lands on the high platform under the lid.", "verb": "arrives"},
                    "hint": "Go out through the yard's gate onto the wall-walk. Run and leap each gap to the high platform under the stone lid.",
                    "id": "obj/cross-the-wall-walk",
                    "title": "Leap to the high platform under the lid", "type": "reach-anchor",
                }],
                "on_complete": [],
                "on_objective_complete": {},
                "trigger": {"type": "campaign-start"},
            },
            {
                "cast": {},
                "happening": {"subject": "anchor/high-platform", "text": "The visitor stands on the high platform; the jetty is past the last leap.", "verb": "learns"},
                "id": "quest/the-boat",
                "objectives": [{
                    "anchor": "anchor/jetty-head", "radius": 1,
                    "happening": {"subject": "anchor/jetty-head", "text": "The visitor reaches the boat at the head of the jetty.", "verb": "arrives"},
                    "hint": "Leap down off the high platform, under the lid, and walk out to the far end of the jetty.",
                    "id": "obj/end-of-the-jetty",
                    "title": "Walk to the end of the jetty", "type": "reach-anchor",
                }],
                "on_complete": [
                    {"style": "subtitle", "text": "You made the boat.", "type": "narrate"},
                    {"type": "campaign-complete",
                     "happening": {"subject": "anchor/jetty-head", "text": "The boat pushes off.", "verb": "opens"}},
                ],
                "on_objective_complete": {},
                "trigger": {"quest": "quest/the-wall-walk", "type": "quest-complete"},
            },
        ],
        "triggers": [],
    })


ZH = {}


def l10n(inventory):
    content, source = {}, {}
    for e in inventory["entries"]:
        content[e["key"]] = ZH[e["en"]]
        source[e["key"]] = e["en"]
    return {"campaign_id": CID, "content": content, "dsl_version": V, "kind": "l10n", "lang": "zh-cn", "source": source}


if __name__ == "__main__":
    args = sys.argv[1:]
    sixth = "--sixth" in args
    args = [a for a in args if a != "--sixth"]
    main(sixth)
    write("quests.json", quests())
    if args:
        write("l10n/zh-cn.json", l10n(json.loads(pathlib.Path(args[0]).read_text())))
