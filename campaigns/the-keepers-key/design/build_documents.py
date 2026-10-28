#!/usr/bin/env python3
"""Write the stage documents of The Keeper's Key (everything but the programs).

    python3 campaigns/the-keepers-key/design/build_documents.py

The documents are the artifact; this script is how they were typed, kept so a
change to one place's numbers is made once. `design/build_pieces.py` writes the
four place programs from the allocation the engine hands them.
"""
import json
import pathlib

CID = "the-keepers-key"
V = "0.68.0"
HERE = pathlib.Path(__file__).resolve().parent.parent

KEY = "minecraft:tripwire_hook"

# Every line the player reads at a device, in the keeper's own house.
L = {
    "door.not_yet": "Locked. Its key is at the keeper's belt: speak to him first.",
    "door.missing_item": "Locked. The keeper's key opens it, held in your hand.",
    "lever.not_yet": "The lever is padlocked to its bracket.",
    "lever.done": "The lever is thrown, and the shed gate across the yard stands open.",
    "hearth.not_yet": "This is the keeper's hearth. Speak to him before you rest here.",
    "lever.missing_item": "The lever is padlocked to its bracket. The keeper's key fits the padlock.",
}


def doc(stage, content):
    return {"campaign_id": CID, "content": content, "dsl_version": V, "stage": stage}


def write(name, d):
    p = HERE / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


PREMISE = (
    "Hob Varley keeps the toll house at Varley Ford: a hall with a hearth, the store behind it, "
    "and across the yard the shed where the ford's punt is kept. The store is locked and its key is at the keeper's belt; "
    "the shed gate is worked from a lever in the store."
)


def main():
    write("world.json", doc("world", {
        "areas": [],
        "horizon": {"attributes": {"audio/background_music": {}}, "base": "void"},
        "min_players": 1,
        "outro": "The shed gate stands open and the punt is there. The keeper's key did what he said it would.",
        "premise": PREMISE,
        "seed": 1240124,
        "target_minutes": 6,
        "test_level": True,
        "theme": "A toll house where one key opens one door, and a lever in the store works a gate across the yard.",
        "time": "day",
        "title": "The Keeper's Key",
        "weather": "clear",
    }))
    write("npcs.json", doc("npcs", {"npcs": [{
        "anchor": "anchor/keeper",
        "area": "area/site",
        "base_entity": "minecraft:villager",
        "id": "npc/keeper",
        "name": "Hob Varley",
        "persona": {
            "archetype": "The keeper of the toll house at Varley Ford, who holds its one key.",
            "demeanor": "Unhurried and exact: he says what a thing does before he hands it over.",
            "motivation": "See the punt taken out by somebody who will bring it back.",
            "speech_style": "Short sentences, each one an instruction.",
        },
        "role": "quest-giver",
    }]}))
    write("dialogue.json", doc("dialogue", {"dialogues": [{
        "nodes": [
            {
                "id": "dlg/keeper-root",
                "options": [
                    {"label": "What does the key open?", "next": "dlg/keeper-what"},
                    {
                        "effects": [{"objective": "obj/hear-the-keeper", "type": "complete-objective"}],
                        "label": "I need the punt.",
                    },
                ],
                "text": "The punt is in the shed across the yard. The shed gate is worked from the store, and the store is locked. Here is the key. Hold it when you try the door.",
            },
            {
                "id": "dlg/keeper-what",
                "options": [{"label": "Back.", "next": "dlg/keeper-root"}],
                "text": "The store door, and the padlock on the lever inside. One key, two locks. Nothing else in this house is locked.",
            },
        ],
        "npc": "npc/keeper",
        "root": "dlg/keeper-root",
    }]}))
    write("classes.json", doc("classes", {"classes": [{
        "blurb": "You came to Varley Ford to take the punt across, and the keeper holds the key to everything between you and it.",
        "id": "class/traveller",
        "kit": [
            {"count": 1, "item": "minecraft:leather_boots", "name": "Road boots"},
            {"count": 6, "item": "minecraft:bread"},
            {"contents": {"potion": "minecraft:healing"}, "count": 2, "flask": True, "item": "minecraft:potion", "name": "Road flask"},
        ],
        "name": "Traveller",
    }]}))
    write("geometry-brief.json", doc("geometry-brief", {"facts": [
        {"id": "fact/site-span", "note": "Thirty-two blocks east to west: the hall and the store, the yard below them, and the ground round them.", "unit": "blocks", "value": 32},
        {"id": "fact/site-depth", "note": "Thirty-six blocks north to south: the hall, the yard and the shed south of it.", "unit": "blocks", "value": 36},
        {"id": "fact/site-height", "note": "Twenty-four blocks from under the floors to the sky.", "unit": "blocks", "value": 24},
    ]}))
    write("quest-plan.json", doc("quest-plan", {
        "finale": "quest/the-punt",
        "quests": [
            {"act": 1, "area": "area/site", "depends_on": [], "goal": "Take the keeper's key, open his store with it, unlock the lever there that works the shed gate, and go into the shed.", "id": "quest/the-punt", "mandatory": True, "npcs": ["npc/keeper"]},
        ],
    }))
    write("layout-graph.json", doc("layout-graph", {
        "beats": [
            {"node": "node/hall", "objective": "obj/hear-the-keeper", "quest": "quest/the-punt"},
            {"node": "node/hall", "objective": "obj/unbar-the-store", "quest": "quest/the-punt"},
            {"node": "node/store", "objective": "obj/work-the-lever", "quest": "quest/the-punt"},
            {"node": "node/shed", "objective": "obj/enter-the-shed", "quest": "quest/the-punt"},
        ],
        "critical_path": ["node/yard", "node/hall", "node/store", "node/hall", "node/yard", "node/shed"],
        "edges": [
            {"a": "node/yard", "b": "node/hall", "class": "walk", "id": "edge/hall-door"},
            {"a": "node/hall", "b": "node/store", "class": "walk", "id": "edge/store-door",
             "gating": {"flags": ["flag/store-unbarred"], "learned": "seen", "opens_from": "a", "shut": "door"}},
            {"a": "node/yard", "b": "node/shed", "class": "walk", "id": "edge/shed-gate",
             "gating": {"flags": ["flag/shed-open"], "learned": "seen"}},
        ],
        "entry": "node/yard",
        "goal": "node/shed",
        "nodes": [
            {"id": "node/yard", "intent": "hub", "note": "The toll house's yard, open to the sky: the hall's doorway on its north side, the shed gate on its south side."},
            {"id": "node/hall", "intent": "hub", "note": "The keeper's hall: the keeper by his table, the hearth in the corner, and the store's door in the east wall.",
             "stations": [
                 {"anchor": "anchor/keeper", "kind": "point", "note": "Where the keeper stands, by his table."},
                 {"anchor": "anchor/hearth", "kind": "point", "note": "The hearth in the hall's corner: the rest point."},
             ]},
            {"id": "node/store", "intent": "side-room", "note": "The keeper's store behind its door: sacks and barrels, and the padlocked lever that works the shed gate.",
             "stations": [
                 {"anchor": "anchor/lever", "kind": "point", "note": "The lever on the store's back wall, padlocked to its bracket."},
             ]},
            {"id": "node/shed", "intent": "goal-chamber", "note": "The punt shed behind its barred gate, across the yard from the house."},
        ],
    }))
    write("site-plan.json", doc("site-plan", {
        "boxes": [
            {"ceiling": {"open": 5}, "extent": [16, 12], "floor": {"datum": "datum/grade"}, "min": [8, 14], "node": "node/yard"},
            {"ceiling": {"clearance": 5}, "extent": [12, 10], "floor": {"datum": "datum/grade"}, "node": "node/hall"},
            {"ceiling": {"clearance": 4}, "extent": [7, 10], "floor": {"datum": "datum/grade"}, "node": "node/store"},
            {"ceiling": {"clearance": 4}, "extent": [8, 7], "floor": {"datum": "datum/grade"}, "node": "node/shed"},
        ],
        "datums": [
            {"id": "datum/grade", "note": "The yard's cobbles and every floor in the house.", "y": 64},
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
            {"at": 6, "edge": "edge/hall-door", "face": "north", "form": "the open doorway from the yard into the keeper's hall", "meets": 6, "opening": "door"},
            {"at": 4, "edge": "edge/store-door", "face": "east", "form": "the store's door in the hall's east wall, shut by the door itself", "meets": 4, "opening": "door"},
            {"at": 8, "edge": "edge/shed-gate", "face": "south", "form": "the shed gate on the yard's south side, barred across", "meets": 4, "opening": "door"},
        ],
    }))


def quests():
    heard = [
        {"carrier": "all", "count": 1, "item": KEY, "name": "The keeper's key", "type": "give-item"},
        {"anchor": "anchor/hearth", "answers": {"not_yet": L["hearth.not_yet"]}, "prompt": "Rest at the hearth",
         "prop": {"block": "minecraft:campfire[facing=north,lit=true,signal_fire=false,waterlogged=false]"},
         "on_rest": [{"style": "chat", "text": "The keeper's hearth takes the chill off.", "type": "narrate"}],
         "type": "bonfire"},
        {"style": "chat", "text": "The keeper hands you a key on a hook. You may rest at his hearth.", "type": "narrate"},
    ]
    shot = {
        "path": [
            {"anchor": "anchor/seam-shed-gate", "offset": [-3, 3, -7]},
            {"anchor": "anchor/seam-shed-gate", "offset": [0, 2, -5]},
        ],
        "seconds": 4,
        "subject": {"anchor": "anchor/seam-shed-gate"},
        "look_at": {"anchor": "anchor/seam-shed-gate"},
        "type": "cutscene",
    }
    return doc("quests", {
        "quests": [
            {
                "cast": {"npc/keeper": {"at": "anchor/keeper", "dialogue": "dlg/keeper-root", "doing": "standing by his table in the hall, a key on a hook at his belt"}},
                "happening": {"subject": "anchor/keeper", "text": "The traveller comes across the yard into the keeper's hall at Varley Ford.", "verb": "arrives"},
                "id": "quest/the-punt",
                "objectives": [
                    {
                        "happening": {"subject": "npc/keeper", "text": "The keeper tells the traveller what his key opens, and hands it over.", "verb": "learns"},
                        "hint": "The keeper stands by his table in the hall, through the doorway off the yard. The keeper's key, a key on a hook at his belt, opens his store.",
                        "id": "obj/hear-the-keeper", "npc": "npc/keeper",
                        "title": "Speak to the keeper", "type": "talk-to",
                    },
                    {
                        "after": ["obj/hear-the-keeper"],
                        "anchor": "anchor/seam-store-door",
                        "answers": {"missing_item": L["door.missing_item"], "not_yet": L["door.not_yet"]},
                        "happening": {"subject": "anchor/seam-store-door", "text": "The traveller unlocks the keeper's store with his key.", "verb": "opens"},
                        "hint": "The store door is the one door in the hall, in its side wall. Hold the keeper's key and use the door.",
                        "id": "obj/unbar-the-store",
                        "requires_item": KEY,
                        "title": "Unlock the store door", "type": "interact",
                    },
                    {
                        "after": ["obj/unbar-the-store"],
                        "anchor": "anchor/lever",
                        "answers": {"done": L["lever.done"], "missing_item": L["lever.missing_item"], "not_yet": L["lever.not_yet"]},
                        "happening": {"subject": "anchor/seam-shed-gate", "text": "The traveller unlocks the lever in the store and throws it; across the yard the shed gate's bars go up.", "verb": "opens"},
                        "hint": "The lever is on the store's back wall. Hold the keeper's key.",
                        "id": "obj/work-the-lever",
                        "prop": {"block": "minecraft:lever[face=wall,facing=west,powered=false]"},
                        "requires_item": KEY,
                        "title": "Throw the lever in the store", "type": "interact",
                    },
                    {
                        "after": ["obj/work-the-lever"],
                        "anchor": "anchor/node-shed", "radius": 2,
                        "happening": {"subject": "anchor/node-shed", "text": "The traveller walks into the punt shed.", "verb": "arrives"},
                        "hint": "The shed gate across the yard is open. The punt is inside.",
                        "id": "obj/enter-the-shed",
                        "title": "Go into the punt shed", "type": "reach-anchor",
                    },
                ],
                "on_complete": [
                    {"style": "subtitle", "text": "The punt is yours to take.", "type": "narrate"},
                    {"type": "campaign-complete",
                     "happening": {"subject": "anchor/node-shed", "text": "The traveller stands in the punt shed at Varley Ford.", "verb": "arrives"}},
                ],
                "on_objective_complete": {
                    "obj/hear-the-keeper": heard,
                    "obj/unbar-the-store": [
                        {"flag": "flag/store-unbarred", "type": "set-flag"},
                        {"anchor": "anchor/seam-store-door", "type": "open-gate",
                         "happening": {"subject": "anchor/seam-store-door", "text": "The store door is unlocked, and opens and shuts by hand from now on.", "verb": "opens"}},
                        {"style": "actionbar", "text": "The key turns. The store door is yours to open.", "type": "narrate"},
                    ],
                    "obj/work-the-lever": [
                        {"flag": "flag/shed-open", "type": "set-flag"},
                        {"anchor": "anchor/seam-shed-gate", "type": "open-gate",
                         "happening": {"subject": "anchor/seam-shed-gate", "text": "The shed gate's bars go up into the stone.", "verb": "opens"}},
                        shot,
                        {"style": "chat", "text": "Across the yard, the shed gate's bars go up into the stone.", "type": "narrate"},
                    ],
                },
                "trigger": {"type": "campaign-start"},
            },
        ],
        "triggers": [],
    })


if __name__ == "__main__":
    main()
    write("quests.json", quests())
