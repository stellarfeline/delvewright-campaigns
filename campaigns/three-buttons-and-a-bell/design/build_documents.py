#!/usr/bin/env python3
"""Write the stage documents of Three Buttons and a Bell (everything but the programs).

    python3 campaigns/three-buttons-and-a-bell/design/build_documents.py
    delvec l10n-inventory campaigns/three-buttons-and-a-bell --prefabs prefabs > inv.json
    python3 campaigns/three-buttons-and-a-bell/design/build_documents.py inv.json

The documents are the artifact; this script is how they were typed, kept so a
change to one place's numbers is made once. The second run writes the zh-CN
sidecar from the key inventory the engine prints.
"""
import json
import pathlib

CID = "three-buttons-and-a-bell"
V = "0.64.0"
HERE = pathlib.Path(__file__).resolve().parent.parent


def doc(stage, content):
    return {"campaign_id": CID, "content": content, "dsl_version": V, "stage": stage}


def write(name, d):
    p = HERE / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


PREMISE = (
    "Merrow Landing is a keeper's house at the end of a jetty, and the keeper's boat is in the shed behind it. "
    "Nothing in the house moves for a stranger: the bell rope is tied up, the store door is barred, the keeper's chest stays shut, "
    "and the shed gate's bolt is pinned fast. Speak to the keeper, and do each thing in its turn, and she will let you take the boat."
)


def main():
    write("world.json", doc("world", {
        "areas": [],
        "demo_level": True,
        "horizon": {"attributes": {"audio/background_music": {}}, "base": "void"},
        "languages": ["zh-cn"],
        "min_players": 1,
        "outro": "The shed gate stands open and the keeper's boat knocks at its mooring. Merrow Landing has let you through.",
        "premise": PREMISE,
        "seed": 117117,
        "target_minutes": 10,
        "theme": "A keeper's house at the end of a jetty, where every handle, bell and button answers the hand that tries it.",
        "time": "day",
        "title": "Three Buttons and a Bell",
        "weather": "clear",
    }))
    write("npcs.json", doc("npcs", {"npcs": [{
        "anchor": "anchor/keeper",
        "area": "area/site",
        "base_entity": "minecraft:villager",
        "id": "npc/keeper",
        "name": "Tamsin Merrow",
        "persona": {
            "archetype": "The keeper of Merrow Landing, who has kept its boat and its bell for thirty years.",
            "demeanor": "Slow to trust and quick to explain, once she has decided to.",
            "motivation": "See that nobody takes the boat out who has not done each thing in the house in its turn.",
            "speech_style": "Plain and short. She gives orders as if they were weather.",
        },
        "role": "quest-giver",
    }]}))
    write("dialogue.json", doc("dialogue", {"dialogues": [{
        "nodes": [
            {
                "id": "dlg/keeper-root",
                "options": [
                    {"label": "Why is everything tied up?", "next": "dlg/keeper-why"},
                    {
                        "effects": [{"objective": "obj/hear-the-keeper", "type": "complete-objective"}],
                        "label": "I need the boat.",
                    },
                ],
                "text": "Nobody takes my boat who has not done the house in its turn. Ring the bell, so the far bank knows. Then the store, with this key. Then my chest. Then the three buttons on the wall, and the bolt on the shed gate.",
            },
            {
                "id": "dlg/keeper-why",
                "options": [{"label": "Back.", "next": "dlg/keeper-root"}],
                "text": "Because people press things. A thing that moves for anybody gets moved by everybody. In this house a thing moves when its turn comes, and not before.",
            },
            {
                "id": "dlg/keeper-bolt",
                "options": [{"label": "I will."}],
                "text": "The house is done, and done in its turn. Three buttons on the wall, one pin each. Then draw the bolt, and the boat is yours till sundown.",
            },
        ],
        "npc": "npc/keeper",
        "root": "dlg/keeper-root",
    }]}))
    write("classes.json", doc("classes", {"classes": [{
        "blurb": "You came down the river road to borrow a boat, and the keeper of Merrow Landing is the only one who has one.",
        "id": "class/traveller",
        "kit": [
            {"count": 1, "item": "minecraft:leather_boots", "name": "Road boots"},
            {"count": 6, "item": "minecraft:bread"},
            {"contents": {"potion": "minecraft:healing"}, "count": 2, "flask": True, "item": "minecraft:potion", "name": "Road flask"},
        ],
        "name": "Traveller",
    }]}))
    write("geometry-brief.json", doc("geometry-brief", {"facts": [
        {"id": "fact/site-span", "note": "Thirty-two blocks across: the keeper's house, its store and the rock round them.", "unit": "blocks", "value": 32},
        {"id": "fact/site-depth", "note": "Forty blocks from the shed to the jetty and the rock beyond them.", "unit": "blocks", "value": 40},
        {"id": "fact/site-height", "note": "Thirty-two blocks from under the floor to over the roofs.", "unit": "blocks", "value": 32},
        {"id": "fact/hall-span", "note": "The keeper's hall is twelve blocks across, so every thing in it is in sight from its doorway.", "unit": "blocks", "value": 12},
    ]}))
    write("quest-plan.json", doc("quest-plan", {
        "finale": "quest/the-boat",
        "quests": [
            {"act": 1, "area": "area/site", "depends_on": [], "goal": "Speak to the keeper of Merrow Landing, ring her bell, unbar her store with her key, and lift the lid of her chest.", "id": "quest/the-house", "mandatory": True, "npcs": ["npc/keeper"]},
            {"act": 1, "area": "area/site", "depends_on": ["quest/the-house"], "goal": "Knock the three pins out of the shed gate's bolt with the three buttons, draw the bolt, and go into the boat shed.", "id": "quest/the-boat", "mandatory": True, "npcs": []},
        ],
    }))
    write("layout-graph.json", doc("layout-graph", {
        "beats": [
            {"node": "node/hall", "objective": "obj/hear-the-keeper", "quest": "quest/the-house"},
            {"node": "node/hall", "objective": "obj/ring-the-bell", "quest": "quest/the-house"},
            {"node": "node/hall", "objective": "obj/unbar-the-store", "quest": "quest/the-house"},
            {"node": "node/hall", "objective": "obj/lift-the-lid", "quest": "quest/the-house"},
            {"node": "node/hall", "objective": "obj/draw-the-bolt", "quest": "quest/the-boat"},
            {"node": "node/shed", "objective": "obj/enter-the-shed", "quest": "quest/the-boat"},
        ],
        "critical_path": ["node/jetty", "node/hall", "node/shed"],
        "edges": [
            {"a": "node/jetty", "b": "node/hall", "class": "walk", "id": "edge/hall-door"},
            {"a": "node/hall", "b": "node/store", "class": "walk", "id": "edge/store-door"},
            {"a": "node/jetty", "b": "node/store", "class": "walk", "id": "edge/jetty-door", "shortcut": True,
             "gating": {"flags": ["flag/jetty-door-open"], "opens_from": "b"}},
            {"a": "node/hall", "b": "node/shed", "class": "walk", "id": "edge/shed-gate",
             "gating": {"flags": ["flag/bolt-drawn"]}},
        ],
        "entry": "node/jetty",
        "goal": "node/shed",
        "nodes": [
            {"id": "node/jetty", "intent": "hub", "note": "The covered end of the jetty, where the party arrives: the open doorway into the keeper's hall, and the barred door into her store, which opens from the store's side.",
             "stations": [
                 {"anchor": f"anchor/jetty-door-{c}", "kind": "point", "note": f"The {w} board of the barred store door, pressed from the jetty or from the store."}
                 for c, w in CELLS
             ]},
            {"id": "node/hall", "intent": "hub", "note": "The keeper's hall: the keeper at her counter, the bell on its post, the chained lever behind her, her chest, the candles, a loose boulder, the three buttons and the bolt on the shed gate, and the latched store door.",
             "stations": [
                 {"anchor": "anchor/keeper", "kind": "point", "note": "Where the keeper stands, at her counter."},
                 {"anchor": "anchor/lever", "kind": "point", "note": "The chained lever on the wall behind the keeper."},
                 {"anchor": "anchor/candles", "kind": "point", "note": "The keeper's candles by the hearth: the rest point."},
                 {"anchor": "anchor/boulder", "kind": "point", "note": "A loose boulder in the corner, struck by hand."},
                 {"anchor": "anchor/button-one", "kind": "point", "note": "The first of the three buttons on the wall."},
                 {"anchor": "anchor/button-two", "kind": "point", "note": "The second of the three buttons."},
                 {"anchor": "anchor/button-three", "kind": "point", "note": "The third of the three buttons."},
                 {"anchor": "anchor/bell", "kind": "point", "note": "The bell on its post."},
                 {"anchor": "anchor/store-door", "kind": "point", "note": "The latched store door, in the hall's wall."},
                 {"anchor": "anchor/chest", "kind": "point", "note": "The keeper's chest against the wall."},
                 {"anchor": "anchor/bolt", "kind": "point", "note": "The bolt beside the shed gate."},
             ]},
            {"id": "node/store", "intent": "side-room", "note": "The keeper's store behind the latched door: the barred door back to the jetty and the button that throws its bar."},
            {"id": "node/shed", "intent": "goal-chamber", "note": "The boat shed behind the barred gate: where the boat is kept."},
        ],
    }))
    write("site-plan.json", doc("site-plan", {
        "boxes": [
            {"ceiling": {"clearance": 4}, "extent": [16, 7], "floor": {"datum": "datum/grade"}, "min": [8, 30], "node": "node/jetty"},
            {"ceiling": {"clearance": 5}, "extent": [12, 12], "floor": {"datum": "datum/grade"}, "node": "node/hall"},
            {"ceiling": {"clearance": 4}, "extent": [6, 12], "floor": {"datum": "datum/grade"}, "node": "node/store"},
            {"ceiling": {"clearance": 4}, "extent": [8, 6], "floor": {"datum": "datum/grade"}, "node": "node/shed"},
        ],
        "datums": [
            {"id": "datum/grade", "note": "The jetty's boards, and every floor in the house.", "y": 64},
        ],
        "fill": {"block": "minecraft:tuff", "kind": "solid"},
        "identities": [
            {"cmp": "eq", "fact": "fact/site-span", "measure": {"axis": "x", "of": "region-extent"}},
            {"cmp": "eq", "fact": "fact/site-depth", "measure": {"axis": "z", "of": "region-extent"}},
            {"cmp": "eq", "fact": "fact/site-height", "measure": {"axis": "y", "of": "region-extent"}},
            {"cmp": "eq", "fact": "fact/hall-span", "measure": {"axis": "x", "node": "node/hall", "of": "box-extent"}},
        ],
        "lighting": {"fixture": "torch", "min_light": 7},
        "region": {"extent": [32, 32, 40], "min": [0, 48, 0]},
        "seams": [
            {"at": 3, "edge": "edge/hall-door", "face": "north", "form": "an open doorway from the jetty into the keeper's hall", "meets": 3, "opening": "door"},
            {"at": 4, "edge": "edge/store-door", "face": "east", "form": "the latched store door in the hall's wall", "meets": 4, "opening": "door"},
            {"at": 14, "edge": "edge/jetty-door", "face": "north", "form": "the store's door onto the jetty, two wide, barred on the store side", "meets": 1, "opening": {"height": 2, "width": 2}},
            {"at": 4, "edge": "edge/shed-gate", "face": "north", "form": "the shed gate in the hall's far wall, barred across", "meets": 2, "opening": "door"},
        ],
    }))


# The barred door onto the jetty is two wide and two high, so the engine can
# tell its sides apart; every one of its four boards answers for it.
CELLS = (("low-left", "lower left"), ("low-right", "lower right"), ("high-left", "upper left"), ("high-right", "upper right"))


# Every line the player reads, in the landing's own voice.
L = {
    "bell.not_yet": "The bell rope is tied up. The keeper unties it once she has spoken to you.",
    "bell.done": "The bell has been rung. The far bank heard it.",
    "door.not_yet": "The store door is barred from within. Ring the bell first.",
    "door.missing_item": "Locked. The keeper's key opens it, held in your hand.",
    "chest.not_yet": "The lid will not lift while the keeper watches. Open her store first.",
    "chest.done": "Empty. You took the oil already.",
    "lever.not_yet": "The lever is chained to the wall. The keeper unchains it once she has spoken to you.",
    "lever.done": "The lever is thrown, and it stays thrown.",
    "button.not_yet": "The button is stiff with rust. The oil is in the keeper's chest.",
    "button.done": "The bolt is already drawn. The pins are all out.",
    "bolt.not_yet": "The bolt is pinned fast. The three buttons on the wall knock its pins out.",
    "bolt.done": "The bolt is drawn. The shed gate stands open.",
    "candles.not_yet": "These are the keeper's candles. Speak to her before you rest here.",
    "boulder.done": "The boulder has already settled into its socket. It will not move again.",
    "jetty_door.sealed_side": "The door does not open from this side. It is barred from the store.",
    "jetty_door.not_yet": "Barred. The bar is on this side: the button beside the door throws it.",
    "jetty_door.done": "The bar is thrown. The door to the jetty stands open.",
}


def quests():
    heard = [
        {"flag": "flag/keeper-spoke", "type": "set-flag"},
        {"carrier": "all", "count": 1, "item": "minecraft:tripwire_hook", "name": "The keeper's key", "type": "give-item"},
        {"anchor": "anchor/candles", "answers": {"not_yet": L["candles.not_yet"]},
         "prompt": "Rest at the candles", "prop": {"block": "minecraft:candle[candles=4,lit=false,waterlogged=false]"},
         "rest_label": "Rest", "rest_tooltip": "The candles keep you, and the house sets itself back up.",
         "save_label": "Save and quit", "save_tooltip": "The candles keep you; nothing in the house is reset.",
         "on_rest": [{"style": "chat", "text": "The keeper's candles take the chill off.", "type": "narrate"}],
         "type": "bonfire"},
        {"style": "chat", "text": "The keeper hands you a key on a hook and unties the bell rope. The lever behind her is unchained, and you may rest at her candles by the hearth.", "type": "narrate"},
    ]
    return doc("quests", {
        "quests": [
            {
                "cast": {"npc/keeper": {"at": "anchor/keeper", "dialogue": "dlg/keeper-root", "doing": "standing at her counter in the hall, a key on a hook at her belt"}},
                "happening": {"subject": "anchor/keeper", "text": "The traveller comes off the jetty into the keeper's hall at Merrow Landing.", "verb": "arrives"},
                "id": "quest/the-house",
                "objectives": [
                    {
                        "happening": {"subject": "npc/keeper", "text": "The keeper tells the traveller to do the house in its turn, and hands over her key.", "verb": "learns"},
                        "hint": "The keeper stands at her counter in the hall, through the doorway off the jetty.",
                        "id": "obj/hear-the-keeper", "npc": "npc/keeper",
                        "title": "Speak to the keeper", "type": "talk-to",
                    },
                    {
                        "after": ["obj/hear-the-keeper"], "anchor": "anchor/bell",
                        "answers": {"done": L["bell.done"], "not_yet": L["bell.not_yet"]},
                        "happening": {"subject": "anchor/bell", "text": "The traveller rings the keeper's bell.", "verb": "opens"},
                        "hint": "The bell stands on its post in the hall.",
                        "id": "obj/ring-the-bell",
                        "prop": {"block": "minecraft:bell[attachment=floor,facing=east,powered=false]"},
                        "title": "Ring the bell", "type": "interact",
                    },
                    {
                        "after": ["obj/ring-the-bell"], "anchor": "anchor/store-door",
                        "answers": {"missing_item": L["door.missing_item"], "not_yet": L["door.not_yet"]},
                        "happening": {"subject": "anchor/store-door", "text": "The traveller unbars the keeper's store with her key.", "verb": "opens"},
                        "hint": "The store door is in the hall's wall, past the counter. Hold the keeper's key.",
                        "id": "obj/unbar-the-store",
                        "prop": {"block": "minecraft:spruce_door[facing=west,half=lower,hinge=left,open=false,powered=false]"},
                        "release": True,
                        "requires_item": "minecraft:tripwire_hook",
                        "title": "Unbar the store door", "type": "interact",
                    },
                    {
                        "after": ["obj/unbar-the-store"], "anchor": "anchor/chest",
                        "answers": {"done": L["chest.done"], "not_yet": L["chest.not_yet"]},
                        "happening": {"subject": "anchor/chest", "text": "The traveller lifts the lid of the keeper's chest and takes the oil.", "verb": "gains"},
                        "hint": "The keeper's chest is against the hall's wall.",
                        "id": "obj/lift-the-lid",
                        "prop": {"block": "minecraft:chest[facing=west,type=single,waterlogged=false]"},
                        "title": "Lift the lid of the keeper's chest", "type": "interact",
                    },
                ],
                "on_complete": [],
                "on_objective_complete": {
                    "obj/hear-the-keeper": heard,
                    "obj/lift-the-lid": [
                        {"style": "chat", "text": "There is a flask of oil in the chest. You work it into the three buttons by the shed gate until they give.", "type": "narrate"},
                    ],
                },
                "trigger": {"type": "campaign-start"},
            },
            {
                "cast": {"npc/keeper": {"at": "anchor/keeper", "dialogue": "dlg/keeper-bolt", "doing": "standing at her counter, watching the bolt"}},
                "happening": {"subject": "anchor/bolt", "text": "The traveller sets about the bolt on the shed gate.", "verb": "learns"},
                "id": "quest/the-boat",
                "objectives": [
                    {
                        "anchor": "anchor/bolt",
                        "answers": {"done": L["bolt.done"], "not_yet": L["bolt.not_yet"]},
                        "happening": {"subject": "anchor/seam-shed-gate", "text": "The traveller draws the bolt, and the shed gate's bars go up.", "verb": "opens"},
                        "hint": "Press the three buttons on the wall, then draw the bolt beside the shed gate.",
                        "id": "obj/draw-the-bolt",
                        "prop": {"block": "minecraft:waxed_lightning_rod[facing=east,powered=false,waterlogged=false]"},
                        "requires_state": [{"op": "at-least", "state": "state/pins-out", "value": 3}],
                        "title": "Draw the bolt on the shed gate", "type": "interact",
                    },
                    {
                        "after": ["obj/draw-the-bolt"],
                        "anchor": "anchor/node-shed", "radius": 2,
                        "happening": {"subject": "anchor/node-shed", "text": "The traveller walks into the boat shed.", "verb": "arrives"},
                        "hint": "The shed gate is open. The boat is inside.",
                        "id": "obj/enter-the-shed",
                        "title": "Go into the boat shed", "type": "reach-anchor",
                    },
                ],
                "on_complete": [
                    {"style": "subtitle", "text": "The boat is yours to take.", "type": "narrate"},
                    {"type": "campaign-complete",
                     "happening": {"subject": "anchor/node-shed", "text": "Merrow Landing lets the traveller through.", "verb": "opens"}},
                ],
                "on_objective_complete": {"obj/draw-the-bolt": [
                    {"flag": "flag/bolt-drawn", "type": "set-flag"},
                    {"anchor": "anchor/seam-shed-gate", "type": "open-gate",
                     "happening": {"subject": "anchor/seam-shed-gate", "text": "The bars of the shed gate go up into the stone.", "verb": "opens"}},
                ]},
                "trigger": {"quest": "quest/the-house", "type": "quest-complete"},
            },
        ],
        "shortcuts": [{
            "answers": {"done": L["jetty_door.done"], "not_yet": L["jetty_door.not_yet"]},
            "gate": "anchor/seam-jetty-door", "highlight": {"within": 6}, "id": "shortcut/jetty-door",
            "on_unlock": [
                {"flag": "flag/jetty-door-open", "type": "set-flag"},
                {"style": "chat", "text": "The bar falls away. The jetty is one door away now.", "type": "narrate"},
            ],
            "prop": {"block": "minecraft:stone_button[face=wall,facing=north,powered=false]"},
            "unlock": "anchor/unlock-jetty-door",
        }],
        "state": [{"id": "state/pins-out", "initial": 0, "name": "Pins out", "note": "How many of the bolt's three pins the buttons have knocked out. Party-scoped: the bolt is one bolt.", "scope": "party"}],
        "triggers": [
        ] + [
            {"at": f"anchor/jetty-door-{c}", "audience": "presser", "id": f"trigger/jetty-door-{c}", "on": {"on": "use"}, "once": False,
             "serves": {"gate": "anchor/seam-jetty-door"},
             "effects": [{"style": "actionbar", "text": L["jetty_door.sealed_side"], "type": "narrate"}]}
            for c, _ in CELLS
        ] + [
            {"at": "anchor/lever", "id": "trigger/the-lever", "on": {"on": "use"}, "once": True,
             "answers": {"done": L["lever.done"], "not_yet": L["lever.not_yet"]},
             "prop": {"block": "minecraft:lever[face=wall,facing=south,powered=false]"},
             "requires_flags": ["flag/keeper-spoke"],
             "effects": [
                 {"flag": "flag/mooring-slipped", "type": "set-flag"},
                 {"style": "chat", "text": "Under the jetty a chain runs out, and the boat in the shed knocks against its mooring.", "type": "narrate"},
             ]},
        ] + [
            {"at": f"anchor/button-{n}", "id": f"trigger/button-{n}", "on": {"on": "use"}, "once": False,
             "answers": {"done": L["button.done"], "not_yet": L["button.not_yet"]},
             "prop": {"block": f"minecraft:{wood}_button[face=wall,facing=east,powered=false]"},
             "serves": {"objective": "obj/draw-the-bolt"},
             "effects": [
                 {"amount": 1, "state": "state/pins-out", "type": "add-state"},
                 {"style": "actionbar", "text": "A pin knocks out of the bolt.", "type": "narrate"},
             ]}
            for n, wood in (("one", "oak"), ("two", "spruce"), ("three", "birch"))
        ] + [
            {"at": "anchor/boulder", "audience": "presser", "id": "trigger/the-boulder", "on": {"on": "strike"}, "once": True,
             "answers": {"done": L["boulder.done"]},
             "prop": {"block": "minecraft:cobbled_deepslate"},
             "effects": [
                 {"flag": "flag/boulder-struck", "type": "set-flag"},
                 {"style": "actionbar", "text": "The boulder rocks under your hand and settles deeper into its socket with a thud.", "type": "narrate"},
             ]},
        ],
    })


ZH = {
    "You came down the river road to borrow a boat, and the keeper of Merrow Landing is the only one who has one.": "你顺着河边的路下来，想借一条船。整个梅罗渡口，只有看守手里有船。",
    "Road boots": "赶路的靴子",
    "Road flask": "路上的药瓶",
    "Traveller": "旅人",
    "I will.": "好。",
    "The house is done, and done in its turn. Three buttons on the wall, one pin each. Then draw the bolt, and the boat is yours till sundown.": "屋里的事都办完了，一样没乱。墙上三个按钮，一个顶掉一根销子。然后拉开门闩，船归你，到天黑为止。",
    "Why is everything tied up?": "怎么什么都拴着？",
    "I need the boat.": "我要借船。",
    "Nobody takes my boat who has not done the house in its turn. Ring the bell, so the far bank knows. Then the store, with this key. Then my chest. Then the three buttons on the wall, and the bolt on the shed gate.": "想用我的船，屋里的事就得一样一样按顺序办。先敲钟，让对岸知道。再拿这把钥匙开库房。再开我的箱子。最后是墙上那三个按钮，还有船棚门上的门闩。",
    "Back.": "回去。",
    "Because people press things. A thing that moves for anybody gets moved by everybody. In this house a thing moves when its turn comes, and not before.": "因为人见了东西就想按。谁碰都会动的东西，迟早被所有人碰个遍。在我这屋里，东西轮到了才动，没轮到就不动。",
    "The bar falls away. The jetty is one door away now.": "门杠落下了。码头如今只隔一扇门。",
    "The boat is yours to take.": "船可以划走了。",
    "The keeper's key": "看守的钥匙",
    "These are the keeper's candles. Speak to her before you rest here.": "这是看守的蜡烛。先跟她说过话，再来这里歇脚。",
    "The keeper's candles take the chill off.": "看守的烛光驱散了寒意。",
    "Rest": "歇息",
    "Rest at the candles": "在烛旁歇息",
    "The candles keep you, and the house sets itself back up.": "烛光护着你，屋里的一切回到原样。",
    "Save and quit": "保存并退出",
    "The candles keep you; nothing in the house is reset.": "烛光护着你；屋里什么都不会重置。",
    "The keeper hands you a key on a hook and unties the bell rope. The lever behind her is unchained, and you may rest at her candles by the hearth.": "看守递给你一把挂在钩子上的钥匙，解开了钟绳。她身后拉杆上的铁链也卸了，炉边她那几支蜡烛旁，你可以歇脚了。",
    "There is a flask of oil in the chest. You work it into the three buttons by the shed gate until they give.": "箱子里有一瓶油。你把油抹进船棚门边那三个按钮里，直到它们按得动了。",
    "A pin knocks out of the bolt.": "一根销子从门闩里掉了出来。",
    "The door does not open from this side. It is barred from the store.": "这扇门从这一侧打不开。门杠在库房那边。",
    "The boulder rocks under your hand and settles deeper into its socket with a thud.": "大石头在你手下晃了晃，咚的一声往凹槽里又沉了一截。",
    "Under the jetty a chain runs out, and the boat in the shed knocks against its mooring.": "码头底下有条铁链哗啦啦放了出去，船棚里的船撞了撞系船桩。",
    "Tamsin Merrow": "塔姆辛·梅罗",
    "The bolt is drawn. The shed gate stands open.": "门闩已经拉开了。船棚的门开着。",
    "The bolt is pinned fast. The three buttons on the wall knock its pins out.": "门闩被销子卡死了。墙上那三个按钮能把销子顶掉。",
    "Press the three buttons on the wall, then draw the bolt beside the shed gate.": "按下墙上的三个按钮，再拉开船棚门边的门闩。",
    "Draw the bolt on the shed gate": "拉开船棚门的门闩",
    "The shed gate is open. The boat is inside.": "船棚的门开了。船就在里面。",
    "Go into the boat shed": "走进船棚",
    "The keeper stands at her counter in the hall, through the doorway off the jetty.": "看守站在厅里的柜台后面，从码头那道门进去就是。",
    "Speak to the keeper": "和看守说话",
    "Empty. You took the oil already.": "空的。油你已经拿走了。",
    "The lid will not lift while the keeper watches. Open her store first.": "看守盯着呢，箱盖掀不开。先去开她的库房。",
    "The keeper's chest is against the hall's wall.": "看守的箱子靠在厅里的墙边。",
    "Lift the lid of the keeper's chest": "掀开看守箱子的盖子",
    "The bell has been rung. The far bank heard it.": "钟已经敲过了。对岸听见了。",
    "The bell rope is tied up. The keeper unties it once she has spoken to you.": "钟绳拴着。看守跟你说过话，才会给你解开。",
    "The bell stands on its post in the hall.": "钟立在厅里的木桩上。",
    "Ring the bell": "敲钟",
    "Locked. The keeper's key opens it, held in your hand.": "锁着。把看守的钥匙拿在手里，就能打开。",
    "The store door is barred from within. Ring the bell first.": "库房的门从里面闩着。先去敲钟。",
    "The store door is in the hall's wall, past the counter. Hold the keeper's key.": "库房的门在厅里的墙上，过了柜台就是。把看守的钥匙拿在手里。",
    "Unbar the store door": "打开库房的门",
    "Knock the three pins out of the shed gate's bolt with the three buttons, draw the bolt, and go into the boat shed.": "用三个按钮顶掉船棚门闩上的三根销子，拉开门闩，走进船棚。",
    "Speak to the keeper of Merrow Landing, ring her bell, unbar her store with her key, and lift the lid of her chest.": "和梅罗渡口的看守说话，敲响她的钟，用她的钥匙打开库房，再掀开她箱子的盖子。",
    "The bar is thrown. The door to the jetty stands open.": "门杠已经卸下了。通往码头的门开着。",
    "Barred. The bar is on this side: the button beside the door throws it.": "门杠插着。门杠在这一侧：门边的按钮能把它卸下。",
    "Pins out": "已顶掉的销子",
    "The bolt is already drawn. The pins are all out.": "门闩早就拉开了。销子都掉光了。",
    "The button is stiff with rust. The oil is in the keeper's chest.": "按钮锈死了，按不动。油在看守的箱子里。",
    "The boulder has already settled into its socket. It will not move again.": "大石头已经沉进凹槽里了，再也不会动了。",
    "The lever is thrown, and it stays thrown.": "拉杆已经扳过了，就停在那儿。",
    "The lever is chained to the wall. The keeper unchains it once she has spoken to you.": "拉杆用铁链锁在墙上。看守跟你说过话，才会卸下铁链。",
    "The shed gate stands open and the keeper's boat knocks at its mooring. Merrow Landing has let you through.": "船棚的门开着，看守的船在系船桩边轻轻磕碰。梅罗渡口放你过去了。",
    "Three Buttons and a Bell": "三个按钮一口钟",
}


def l10n(inventory):
    content, source = {}, {}
    missing = []
    for e in inventory["entries"]:
        if e["en"] not in ZH:
            missing.append(e["en"])
            continue
        content[e["key"]] = ZH[e["en"]]
        source[e["key"]] = e["en"]
    if missing:
        raise SystemExit("untranslated:\n" + "\n".join(missing))
    return {"campaign_id": CID, "content": content, "dsl_version": V, "kind": "l10n", "lang": "zh-cn", "source": source}


if __name__ == "__main__":
    main()
    write("quests.json", quests())
    import sys
    if len(sys.argv) > 1:
        write("l10n/zh-cn.json", l10n(json.loads(pathlib.Path(sys.argv[1]).read_text())))
