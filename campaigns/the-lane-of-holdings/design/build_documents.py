#!/usr/bin/env python3
"""Write the stage documents of The Lane of Holdings (everything but the programs).

    python3 campaigns/the-lane-of-holdings/design/build_documents.py

Each plot is planned with what it holds before its box is written: its parts,
which are walked, and each part's play space in cells. The box is then sized
from the parts and the ways between them. `design/build_pieces.py` builds each
part in the outline drawn there, and the plan's numbers here are the ones the
pieces were drawn to. The documents are the artifact; this script is how they
were typed, kept so a change to one place's numbers is made once.
"""
import json
import pathlib

CID = "the-lane-of-holdings"
V = "0.69.0"
HERE = pathlib.Path(__file__).resolve().parent.parent

# The plots, west to east along the lane's north side:
# (stem, intent, note, extent [x, z], ceiling, at, holds or None).
# The dwelling's play space is 20 x 20: an L of a house (10 x 9 inside) and a
# cart shed (5 x 4 inside) against its east wall; a front strip between the
# lane and the door; a back yard behind, which the shed opens onto; a bed of
# flowers behind a low hedge at the front, nobody walks.
DWELLING = [
    {"id": "part/house", "kind": "structure", "use": "the family's house: one long room with the hearth, the table and the beds", "cells": 90, "height": 5},
    {"id": "part/garage", "kind": "structure", "use": "the cart shed against the house's east wall, through a door from the house, its own door onto the back yard", "cells": 20, "height": 5},
    {"id": "part/front", "kind": "ground", "use": "the front strip between the lane's gate and the house door", "cells": 120},
    {"id": "part/back", "kind": "ground", "use": "the back yard: the washing line, the vegetable rows and the shed's door", "cells": 95},
    {"id": "part/bed", "kind": "ground", "use": "a bed of flowers under the front windows, behind a low hedge", "cells": 10, "reached": False},
]
FORGE = [
    {"id": "part/shop", "kind": "structure", "use": "the smith's shop at the lane with its counter, and behind it the workroom with the forge and the anvil", "cells": 56, "height": 5},
    {"id": "part/yard", "kind": "ground", "use": "the work yard beside the shop: the grindstone, the quench and the wood stack", "cells": 109},
    {"id": "part/store", "kind": "structure", "use": "the iron store in the yard's corner, shut", "cells": 4, "height": 5, "reached": False},
]
CHAPEL = [
    {"id": "part/chapel", "kind": "structure", "use": "the chapel: one hall under its roof, the altar at the north end", "cells": 90, "height": 6},
]
BYRE = [
    {"id": "part/byre", "kind": "structure", "use": "the byre: stalls and hay for the cattle, its door onto the pen", "cells": 30, "height": 5},
    {"id": "part/pen", "kind": "ground", "use": "the pen round the byre where the cattle stand, fenced from the lane", "cells": 112},
]
PLOTS = [
    ("dwelling", "dwelling on its lot",
     "A house on its own ground: an L of the house and the cart shed, the front strip to the door, the back yard behind, a flower bed behind the hedge.",
     [20, 20], {"open": 7}, 4, DWELLING),
    ("forge", "forge on its frontage",
     "The smith's holding: the shop and workroom at the lane's edge, the work yard beside it, the iron store in the yard's corner.",
     [16, 14], {"open": 7}, 27, FORGE),
    ("chapel", "chapel that is its plot",
     "The chapel standing alone on its ground: one structure that is the whole of the plot, cut as a sky-open plot of one part.",
     [9, 11], {"open": 8}, 46, CHAPEL),
    ("chapel-lidded", "chapel under a lid",
     "The same chapel cut the other way: a lidded box with no parts, beside the plot of one structure, so the two spellings stand side by side.",
     [9, 11], {"clearance": 5}, 58, None),
    ("byre", "byre and its pen",
     "The farm's edge at the lane's end: the byre and the pen round it.",
     [14, 12], {"open": 6}, 70, BYRE),
]
# Where each plot's way in stands along its own south face, from its west
# edge: the dwelling's gate, the forge's shop door, the chapels' doors, the
# pen's gate.
MEETS = {"dwelling": 8, "forge": 4, "chapel": 4, "chapel-lidded": 4, "byre": 10}
FORMS = {
    "dwelling": "the dwelling's front gate, a gap in the hedge onto the front strip",
    "forge": "the smith's shop door, on the lane's edge",
    "chapel": "the chapel's west door — the plot of one structure",
    "chapel-lidded": "the lidded chapel's door",
    "byre": "the pen's gate off the lane's end",
}

LANE_MIN = [3, 40]
LANE_EXTENT = [88, 5]


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
        "outro": "The lane is walked to the byre at its end, past every holding on it.",
        "premise": "Holding Lane runs out of the village to the fields: a family's house on its lot, the smith's forge, a chapel, and a byre at the end where the lane meets the pasture.",
        "seed": 20261028,
        "target_minutes": 8,
        "theme": "A lane of holdings, each planned with what it holds: a house and its cart shed with their yards, a forge with its work yard, a chapel that is its whole plot, and a byre with its pen.",
        "time": "day",
        "title": "The Lane of Holdings",
        "weather": "clear",
    }))
    write("npcs.json", doc("npcs", {"npcs": []}))
    write("dialogue.json", doc("dialogue", {"dialogues": []}))
    write("classes.json", doc("classes", {"classes": [{
        "blurb": "A traveller come down Holding Lane, free to look in at every holding on the way to the byre.",
        "id": "class/traveller",
        "kit": [
            {"count": 1, "item": "minecraft:wooden_sword", "name": "Walking staff"},
            {"count": 6, "item": "minecraft:bread"},
        ],
        "name": "Traveller",
    }]}))
    write("geometry-brief.json", doc("geometry-brief", {"facts": [
        {"id": "fact/site-span", "note": "Ninety-four blocks east to west: the lane and the field walls at either end.", "unit": "blocks", "value": 94},
        {"id": "fact/site-depth", "note": "Thirty-two blocks north to south: the holdings north of the lane, the lane, and the green south of it.", "unit": "blocks", "value": 32},
        {"id": "fact/site-height", "note": "Twenty-four blocks from under the lane to the sky.", "unit": "blocks", "value": 24},
    ]}))
    write("quest-plan.json", doc("quest-plan", {
        "finale": "quest/the-lane",
        "quests": [
            {"act": 1, "area": "area/site", "depends_on": [], "goal": "Walk Holding Lane to the byre at its end, looking in at any holding on the way.", "id": "quest/the-lane", "mandatory": True, "npcs": []},
        ],
    }))
    nodes = [{"id": "node/lane", "intent": "connector", "note": "Holding Lane, three wide with a verge on its south side and lamps on the verge; every holding opens onto it."}]
    for stem, intent, note, _, _, _, holds in PLOTS:
        n = {"id": f"node/{stem}", "intent": intent, "note": note}
        if holds:
            n["holds"] = holds
        nodes.append(n)
    edges = [{"a": "node/lane", "b": f"node/{p[0]}", "class": "walk", "id": f"edge/{p[0]}-way"} for p in PLOTS]
    write("layout-graph.json", doc("layout-graph", {
        "beats": [{"node": "node/byre", "objective": "obj/the-byre", "quest": "quest/the-lane"}],
        "critical_path": ["node/lane", "node/byre"],
        "edges": edges,
        "entry": "node/lane",
        "goal": "node/byre",
        "nodes": nodes,
    }))
    boxes = [
        {"ceiling": {"open": 4}, "extent": LANE_EXTENT, "floor": {"datum": "datum/grade"}, "min": LANE_MIN, "node": "node/lane",
         "way": {"at": 0, "axis": "x", "clear": 3}},
    ]
    seams = []
    for stem, _, _, extent, ceiling, at, _ in PLOTS:
        box = {"ceiling": ceiling, "extent": extent, "floor": {"datum": "datum/grade"}, "node": f"node/{stem}"}
        if "clearance" in ceiling:
            box["roof"] = {"courses": 2, "eaves": 0}
        boxes.append(box)
        seams.append({"at": at + MEETS[stem], "edge": f"edge/{stem}-way", "face": "north", "form": FORMS[stem],
                      "meets": MEETS[stem], "opening": "door"})
    identities = [
        {"cmp": "eq", "fact": "fact/site-span", "measure": {"axis": "x", "of": "region-extent"}},
        {"cmp": "eq", "fact": "fact/site-depth", "measure": {"axis": "z", "of": "region-extent"}},
        {"cmp": "eq", "fact": "fact/site-height", "measure": {"axis": "y", "of": "region-extent"}},
    ]
    write("site-plan.json", doc("site-plan", {
        "boxes": boxes,
        "datums": [{"id": "datum/grade", "note": "The lane and every holding on it.", "y": 64}],
        "fill": {"below": "minecraft:dirt", "kind": "open", "surface": "minecraft:grass_block",
                 "terrain": {"datum": "datum/grade", "kind": "flat"}},
        "identities": identities,
        "lighting": {"fixture": "torch", "min_light": 7},
        "region": {"extent": [94, 24, 32], "min": [0, 52, 15]},
        "seams": seams,
        "volumes": [
            {"block": "minecraft:mossy_cobblestone", "id": "volume/field-wall-west", "note": "The field wall at the lane's west end.",
             "region": {"extent": [1, 8, 32], "min": [0, 58, 15]}, "role": "massif"},
            {"block": "minecraft:mossy_cobblestone", "id": "volume/field-wall-east", "note": "The field wall at the east end.",
             "region": {"extent": [1, 8, 32], "min": [93, 58, 15]}, "role": "massif"},
            {"block": "minecraft:mossy_cobblestone", "id": "volume/field-wall-north", "note": "The field wall behind the holdings.",
             "region": {"extent": [92, 8, 1], "min": [1, 58, 15]}, "role": "massif"},
            {"block": "minecraft:mossy_cobblestone", "id": "volume/field-wall-south", "note": "The field wall along the south edge of the green.",
             "region": {"extent": [92, 8, 1], "min": [1, 58, 46]}, "role": "massif"},
        ],
    }))


def quests():
    return doc("quests", {
        "quests": [
            {
                "cast": {},
                "happening": {"subject": "anchor/node-lane", "text": "The traveller comes down Holding Lane.", "verb": "arrives"},
                "id": "quest/the-lane",
                "objectives": [
                    {"anchor": "anchor/node-byre", "radius": 2,
                     "happening": {"subject": "anchor/node-byre", "text": "The traveller reaches the byre at the lane's end.", "verb": "arrives"},
                     "hint": "The byre stands in its pen at the far end of the lane, past the house, the forge and the chapels.",
                     "id": "obj/the-byre", "title": "Reach the byre", "type": "reach-anchor"},
                ],
                "on_complete": [
                    {"style": "subtitle", "text": "The lane is walked to its end.", "type": "narrate"},
                    {"type": "campaign-complete",
                     "happening": {"subject": "anchor/node-byre", "text": "Holding Lane is walked.", "verb": "opens"}},
                ],
                "on_objective_complete": {},
                "trigger": {"type": "campaign-start"},
            },
        ],
        "triggers": [
            {"at": "anchor/node-lane", "id": "trigger/the-lane", "on": {"on": "approach", "range": 4}, "once": True,
             "effects": [{"style": "chat", "text": "Holding Lane. A house, a forge and a chapel keep their ground on it, and the byre waits at the far end. Look in where you like.", "type": "narrate"}]},
        ],
    })


if __name__ == "__main__":
    main()
    write("quests.json", quests())
