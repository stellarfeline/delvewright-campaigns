"""The Stranding's map, as one geometry model.

Writes `geometry-brief.json`, `layout-graph.json`, `site-plan.json` and the
terrain heightmap from the numbers below. Every place generator and the body
form read the same model (`import mapmodel`), so a box moved here moves everything
built against it. Axes: x east, y up, z south; the town is north, the body south.

Run: python3 generators/mapmodel.py   (from the campaign directory or anywhere)
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CAMPAIGN = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import pngio  # noqa: E402

DSL = "0.39.0"
CID = "the-stranding"

SEA = 62           # the ocean horizon's sea level (top water block)
REGION_MIN = (0, 30, 0)
REGION_EXT = (400, 100, 760)
TERRAIN_BASE = 30  # heightmap: surface y = TERRAIN_BASE + value (range 255)

# ---------------------------------------------------------------------------
# datums
DATUMS = {
    "datum/coach-road": 96,
    "datum/cliff-steps": 86,
    "datum/high-street": 76,
    "datum/harbour": 66,
    "datum/lofts": 72,
    "datum/basin": 64,
    "datum/flat": 64,
    "datum/crypt": 64,
    "datum/chapel": 70,
    "datum/crown": 104,
    "datum/back-upper": 100,
    "datum/back-middle": 96,
    "datum/back-lower": 86,
    "datum/tail-flank": 70,
    "datum/mast": 75,
    "datum/spine-top": 84,
}

# ---------------------------------------------------------------------------
# places: (id, min x, min z, extent x, extent z, floor datum or y, ceiling, extra)
# ceiling: ("open", n) or ("clearance", n)
P = {}
ORDER = []


def place(node, x, z, dx, dz, floor, ceiling, roof=None, base=None, intent="",
          note=None, stations=(), reached=True, atmosphere=None):
    P[node] = dict(node=node, x=x, z=z, dx=dx, dz=dz, floor=floor, ceiling=ceiling,
                   roof=roof, base=base, intent=intent, note=note,
                   stations=list(stations), reached=reached, atmosphere=atmosphere)
    ORDER.append(node)
    return P[node]


def fy(p):
    f = p["floor"]
    return DATUMS[f] if isinstance(f, str) else f


def x1(p):
    return p["x"] + p["dx"] - 1


def z1(p):
    return p["z"] + p["dz"] - 1


def top(p):
    """The last course of play space."""
    kind, n = p["ceiling"]
    return fy(p) + n - 1


ST = lambda a, note=None, kind="point": {"anchor": a, "kind": kind, **({"note": note} if note else {})}

# ---- Act 1: Wrackham -------------------------------------------------------
place("node/coach-road", 196, 6, 84, 8, "datum/coach-road", ("open", 6),
      intent="arrival", note="The cobbled coach road along the cliff top, a drystone parapet on the drop and the rock bank behind; the coach stop's timber shelter at its east end.",
      stations=[ST("anchor/coach-stop", "the notice on the coach stop's post")])
place("node/cliff-steps", 200, 15, 5, 15, "datum/cliff-steps", ("clearance", 14),
      roof={"courses": 4, "eaves": 0}, intent="descent",
      note="The covered steps down the cliff from the coach road to the head of the High Street.")
place("node/high-street", 192, 31, 22, 56, "datum/high-street", ("open", 24),
      intent="street", note="The High Street between two terraces of tall slate-roofed houses; sleepers stand in the open doorways facing the sea.")
place("node/harbour-lane", 118, 88, 96, 14, "datum/harbour", ("open", 14),
      intent="quay", note="The harbour lane along the north quay: the office, the cottage, the lofts and the market open off it; the basin lies below its quay edge.")
place("node/harbour-office", 168, 79, 9, 8, "datum/harbour", ("clearance", 6),
      roof={"courses": 6, "eaves": 0}, intent="office",
      note="Wenna Coyle's office: the tide board stuck at low, the desk, a window over the harbour.")
place("node/coyle-house", 124, 81, 7, 6, "datum/harbour", ("clearance", 4),
      roof={"courses": 4, "eaves": 1}, intent="cottage",
      note="A single-storey limewashed cottage: Davey's room, the soaked bed, the footprints, the wool picture.",
      stations=[ST("anchor/wool-picture", "Davey's picture of the dream in coloured wool")])
place("node/net-lofts", 136, 80, 12, 7, "datum/lofts", ("clearance", 5),
      roof={"courses": 5, "eaves": 0}, intent="loft",
      note="A plank loft over the harbour up a stair, nets and floats, a sleeper at the loft door.")
place("node/boatyard", 124, 103, 44, 37, "datum/basin", ("open", 10),
      intent="arena", note="The emptied harbour basin: the town's boats lie on their sides on the mud.",
      stations=[ST("anchor/shipwright-note", "the shipwright's note nailed to a hull")])
place("node/fish-market", 169, 103, 21, 22, "datum/harbour", ("clearance", 7),
      roof={"courses": 12, "eaves": 0}, intent="arena",
      note="The covered fish market hall: stone slabs, barrels, nets; its sea doors open on the slipway up out of the basin.",
      stations=[ST("anchor/market-slate", "the market slate where the day's catch is chalked")])
place("node/seawall", 170, 126, 90, 9, "datum/harbour", ("open", 7),
      intent="threshold", note="The seawall along the town's south front, a parapet over the flat; the threshold of the wrong place.",
      stations=[ST("anchor/customs-lock", "the padlock on the Customs House door")])
place("node/seamens-chapel", 226, 106, 11, 19, "datum/chapel", ("clearance", 9),
      roof={"courses": 7, "eaves": 0}, intent="chapel",
      note="A small rubble-stone chapel, the Rubbing on its wall.",
      stations=[ST("anchor/rubbing-script", "the carvers' script under the Rubbing's second panel")])
place("node/chapel-crypt", 227, 108, 9, 15, "datum/crypt", ("clearance", 5),
      intent="crypt", note="The crypt under the chapel: niches of the drowned and the founders' cupboard.")
place("node/customs-house", 196, 109, 14, 16, "datum/harbour", ("clearance", 6),
      roof={"courses": 7, "eaves": 0}, intent="records",
      note="The town's records: the night ledger, the chart of the old road, the chip of the stone under glass.",
      stations=[ST("anchor/customs-chart", "the chart of the Pilgrims' Way"),
                ST("anchor/stone-chip", "the chip of the Brow Stone under glass")])
place("node/whalers-shed", 105, 106, 18, 14, "datum/harbour", ("clearance", 8),
      roof={"courses": 9, "eaves": 0}, intent="store",
      note="The last whaling crew's flensing tools; the Flensing Spade on its rack.",
      stations=[ST("anchor/spade-rack", "the Flensing Spade on its rack")])
place("node/ropewalk", 108, 121, 7, 40, "datum/harbour", ("clearance", 4),
      roof={"courses": 3, "eaves": 0}, intent="passage",
      note="The long low rope shed, a sleeper at each end.")
place("node/breakwater", 107, 162, 9, 44, "datum/harbour", ("open", 5),
      intent="causeway", note="The stone arm out into the bay with the flat on both sides of it.")
place("node/lighthouse", 106, 207, 11, 11, "datum/harbour", ("clearance", 27),
      roof={"courses": 5, "eaves": 0}, intent="tower",
      note="The white stone tower: a stair up the inside to the lamp room and its gallery.",
      stations=[ST("anchor/lighthouse-lamp", "the great lamp in the lamp room")])
place("node/slipway-stair", 170, 136, 7, 10, "datum/flat", ("open", 6),
      intent="threshold", note="The stone stair from the seawall down onto the flat; Wenna waits at its head.")
place("node/pier", 70, 92, 47, 6, "datum/harbour", ("open", 5), base={"aloft": 0},
      intent="pier", note="A timber deck on piles out over the open sea west of the harbour.",
      stations=[ST("anchor/pier-end", "the end of the pier over deep water")])

# ---- Act 2: the crossing ---------------------------------------------------
place("node/pilgrims-way", 171, 147, 5, 100, "datum/flat", ("open", 5),
      intent="road", note="The old road over the bay: packed mud and old stone, marker stakes with lamps.")
place("node/wreck-field", 120, 248, 121, 40, "datum/flat", ("open", 10),
      intent="arena", note="Old hulls the rising brought up, lying on their sides either side of the way.",
      stations=[ST("anchor/wreck-nameboard", "a nameboard broken off a hull")])
place("node/carved-pillars", 165, 289, 17, 50, "datum/flat", ("open", 12),
      intent="road", note="The stretch of the way past Marrack's launch, then lined both sides with the standing carved pillars.",
      stations=[ST("anchor/pillar-script", "the carvers' script at the foot of a pillar")])
place("node/marracks-launch", 140, 289, 24, 50, "datum/flat", ("open", 10),
      intent="camp", note="A salvage launch grounded on the mud beside the way, Marrack's lanterns on its rail.")
place("node/mast-platform", 155, 302, 5, 5, "datum/mast", ("open", 3), base={"aloft": 0},
      intent="lookout", note="Marrack's mast platform, reached by a timber stair from the mud; it looks along the body's flank.")
MUD = "A field of wet mud over the sea water that the rising left; it goes under when the flat sinks."
place("node/mud-wrecks-west", 120, 149, 50, 98, "datum/flat", ("open", 4), base={"aloft": 0},
      intent="mud", note=MUD + " Beside the first stretch of the way, west.")
place("node/mud-wrecks-east", 177, 149, 64, 98, "datum/flat", ("open", 4), base={"aloft": 0},
      intent="mud", note=MUD + " Beside the first stretch of the way, east.")
place("node/mud-pillars-west", 120, 289, 19, 50, "datum/flat", ("open", 4), base={"aloft": 0},
      intent="mud", note=MUD + " West of Marrack's launch.")
place("node/mud-pillars-east", 183, 289, 58, 50, "datum/flat", ("open", 4), base={"aloft": 0},
      intent="mud", note=MUD + " East of the carved pillars.")
place("node/mud-narrows-west", 120, 340, 51, 52, "datum/flat", ("open", 4), base={"aloft": 0},
      intent="mud", note=MUD + " West of the narrows.")
place("node/narrows", 172, 340, 3, 52, "datum/flat", ("open", 5),
      intent="ridge", note="The way narrowed to a ridge three blocks wide between open water.")
place("node/narrows-shelf", 176, 350, 24, 18, "datum/flat", ("open", 14),
      intent="arena", note="A mud shelf beside the ridge and the pit the first tentacle rises from.",
      stations=[ST("anchor/narrows-pit", "the pit the tentacle stands in"),
                ST("anchor/narrows-strike", "the middle of the stretch of shelf the tentacle strikes")])
place("node/skiff-stage", 164, 393, 19, 12, "datum/flat", ("open", 6),
      intent="landing", note="The stone stage at the end of the way, at the edge of the black water.",
      stations=[ST("anchor/near-bell", "the ferry bell beside the near house's land door"),
                ST("anchor/near-bell-stand", "where the ringer of the near bell stands")])
place("node/near-ferry-house", 166, 406, 12, 16, "datum/flat", ("clearance", 6),
      roof={"courses": 8, "eaves": 0}, intent="ferry",
      note="The old road's near ferry house: a stone quay beside the slip, Marrack's skiff inside.",
      stations=[ST("anchor/near-skiff", "the skiff's seat row"),
                ST("anchor/near-tiller", "the near skiff's tiller"),
                ST("anchor/near-door", "the land door, shut from inside while the party is across")])
place("node/sea-skiff", 62, 448, 5, 10, "datum/flat", ("open", 4), base={"aloft": 0},
      intent="reveal", note="The third copy of the skiff on the open water west of the ferry houses, in the sea fog; reached only by the crossing back.",
      stations=[ST("anchor/sea-skiff", "the seat row of the skiff on the open water")])
place("node/far-ferry-house", 140, 482, 12, 16, "datum/flat", ("clearance", 6),
      roof={"courses": 8, "eaves": 0}, intent="ferry",
      note="The far ferry house that came up with the trench floor, built like the near one; the skiff's twin inside.",
      stations=[ST("anchor/far-skiff", "the far skiff's seat row"),
                ST("anchor/far-tiller", "the far skiff's tiller"),
])
place("node/far-landing", 128, 499, 32, 15, "datum/flat", ("open", 8),
      intent="landing", note="The bank outside the far ferry house, Marrack's crew's lamps.",
      stations=[ST("anchor/far-bell", "the ferry bell beside the far house's land door"),
                ST("anchor/far-bell-stand", "where the ringer of the far bell stands")])
place("node/jaw-bank", 161, 500, 50, 20, "datum/flat", ("open", 24),
      intent="arena", note="The bank of mud under the head: the open jaw, teeth like posts, a tentacle in a pit on each side of the mouth.",
      stations=[ST("anchor/jaw-west-pit", "the west tentacle's pit"),
                ST("anchor/jaw-east-pit", "the east tentacle's pit")])
place("node/flank-ridge", 128, 515, 12, 126, "datum/flat", ("open", 8),
      intent="post", note="A mud ridge along the body's west side, out of the tentacles' reach; the three flank wounds in plain sight.")

# ---- Act 3: inside the body ----------------------------------------------
place("node/mouth", 168, 521, 20, 16, "datum/flat", ("clearance", 8),
      intent="threshold", note="Through the teeth onto the tongue.",
      stations=[ST("anchor/chalk-arrow", "Marrack's chalk arrow on a tooth")])
place("node/throat", 174, 538, 7, 30, "datum/flat", ("clearance", 5),
      intent="corridor", note="A corridor of ribs, every six blocks the same, that returns the walker twelve blocks back until the wrong rib is struck.",
      stations=[ST("anchor/wrong-rib", "the broken rib set wrong")])
place("node/rib-cathedral", 167, 569, 29, 39, "datum/flat", ("clearance", 30),
      intent="vault", note="The chest: a vault of ribs, moonlight through two roof wounds, the diaphragm closing the way down.",
      stations=[ST("anchor/diaphragm", "the membrane of the diaphragm")])
place("node/stomach", 171, 609, 22, 20, "datum/flat", ("clearance", 10),
      intent="arena", note="A black pool behind a curb of bone; on its shore what earlier visitors left.",
      stations=[ST("anchor/stomach-shore", "Marrack's men's lamp on the shore")])
place("node/heart-chamber", 157, 610, 13, 20, "datum/flat", ("clearance", 14),
      intent="living-room", note="Sculk over bone, sensors and a shrieker, the heart with three valves, Davey standing awake by it.",
      stations=[ST("anchor/davey-heart", "where Davey stands by the heart"),
                ST("anchor/valve-west", "the west valve"),
                ST("anchor/valve-middle", "the middle valve"),
                ST("anchor/valve-east", "the east valve")])
place("node/breach", 141, 618, 15, 4, "datum/flat", ("clearance", 4),
      intent="tunnel", note="A short tunnel of torn flesh from the heart chamber out through a wound to the flank ridge.")
place("node/spine-stair", 159, 564, 5, 45, "datum/flat", ("clearance", 24),
      intent="climb", note="Up the inside of the neck on the vertebrae, from the heart's door.")
place("node/spine-top", 159, 529, 5, 34, "datum/spine-top", ("clearance", 19),
      intent="climb", note="The upper neck, the vertebra stair climbing to the blowhole.")

# ---- Act 4: the brow and the escape -------------------------------------
place("node/crown", 156, 530, 30, 32, "datum/crown", ("open", 6), base={"aloft": 0},
      intent="summit", note="The top of the head, forty blocks over the flat; the blowhole; three tentacles by the way to the Brow.")
place("node/brow", 166, 520, 16, 9, "datum/crown", ("open", 6), base={"aloft": 0},
      intent="climax", note="The forehead, the Brow Stone driven into its face.",
      stations=[ST("anchor/brow-stone", "the Brow Stone")])
place("node/back-upper", 176, 563, 9, 27, "datum/back-upper", ("open", 8), base={"aloft": 0},
      intent="run", note="The back behind the head, falling along the spine ridge.")
place("node/back-middle", 176, 591, 9, 28, "datum/back-middle", ("open", 8), base={"aloft": 0},
      intent="run", note="The hump of the back.")
place("node/back-lower", 176, 620, 9, 26, "datum/back-lower", ("open", 13), base={"aloft": 0},
      intent="run", note="The knuckles of the spine toward the tail.")
place("node/tail-flank", 176, 647, 9, 18, "datum/tail-flank", ("open", 21), base={"aloft": 0},
      intent="run", note="Down the tail flank onto the bank.")
place("node/tail-bank", 160, 666, 40, 12, "datum/flat", ("open", 9),
      intent="run", note="The bank under the flukes.")
place("node/tail-road", 201, 655, 10, 24, "datum/flat", ("open", 6),
      intent="run", note="Round the flukes onto the east bank.")
place("node/run-bank", 212, 505, 8, 160, "datum/flat", ("open", 6),
      intent="run", note="The east bank back north to the head, Marrack's crew's lamp stakes along it; it falls into the sea behind the party.")

# ---------------------------------------------------------------------------
# where each station stands in the world: the cell a body's feet are in (or the
# prop's cell), and the way it faces. Every piece marks its stations here.
STATIONS = {
    "anchor/coach-stop": (270, 96, 9, "north"),
    "anchor/wool-picture": (127, 66, 81, "north"),
    "anchor/shipwright-note": (150, 64, 118, "south"),
    "anchor/market-slate": (186, 66, 107, "east"),
    "anchor/customs-lock": (204, 66, 127, "north"),
    "anchor/rubbing-script": (231, 70, 108, "north"),
    "anchor/customs-chart": (200, 66, 113, "north"),
    "anchor/stone-chip": (205, 66, 117, "north"),
    "anchor/spade-rack": (107, 66, 112, "west"),
    "anchor/lighthouse-lamp": (111, 89, 212, "north"),
    "anchor/pier-end": (72, 66, 94, "west"),
    "anchor/wreck-nameboard": (160, 64, 262, "west"),
    "anchor/pillar-script": (167, 64, 320, "west"),
    "anchor/narrows-pit": (196, 64, 358, "west"),
    "anchor/narrows-strike": (187, 64, 358, "east"),
    "anchor/near-bell": (175, 64, 403, "south"),
    "anchor/near-bell-stand": (176, 64, 402, "south"),
    "anchor/near-skiff": (174, 64, 413, "north"),
    "anchor/near-tiller": (174, 64, 418, "north"),
    "anchor/near-door": (170, 64, 406, "south"),
    "anchor/sea-skiff": (64, 64, 452, "north"),
    "anchor/far-skiff": (148, 64, 489, "north"),
    "anchor/far-tiller": (148, 64, 494, "north"),
    "anchor/far-bell": (147, 64, 500, "north"),
    "anchor/far-bell-stand": (148, 64, 501, "north"),
    "anchor/jaw-west-pit": (167, 64, 511, "south"),
    "anchor/jaw-east-pit": (189, 64, 511, "south"),
    "anchor/chalk-arrow": (176, 64, 524, "south"),
    "anchor/wrong-rib": (174, 65, 556, "east"),
    "anchor/diaphragm": (181, 64, 606, "south"),
    "anchor/stomach-shore": (176, 64, 614, "south"),
    "anchor/davey-heart": (163, 64, 616, "north"),
    "anchor/valve-west": (160, 64, 625, "south"),
    "anchor/valve-middle": (163, 64, 625, "south"),
    "anchor/valve-east": (166, 64, 625, "south"),
    "anchor/brow-stone": (173, 104, 520, "north"),
}


def node_anchor(nid):
    p = P[nid]
    return (p["x"] + (p["dx"] - 1) // 2, fy(p), p["z"] + (p["dz"] - 1) // 2)


def anchor_pos(aid):
    if aid in STATIONS:
        return STATIONS[aid][:3]
    if aid.startswith("anchor/node-"):
        return node_anchor("node/" + aid[len("anchor/node-"):])
    raise KeyError(aid)


# ---------------------------------------------------------------------------
# connections: (edge, a, b, class, extra)
E = []


def edge(eid, a, b, cls, **kw):
    E.append(dict(id=eid, a=a, b=b, cls=cls, **kw))


edge("edge/coach-to-steps", "node/coach-road", "node/cliff-steps", "stair")
edge("edge/steps-to-street", "node/cliff-steps", "node/high-street", "stair")
edge("edge/street-to-lane", "node/high-street", "node/harbour-lane", "stair")
edge("edge/lane-to-office", "node/harbour-lane", "node/harbour-office", "walk")
edge("edge/lane-to-coyle", "node/harbour-lane", "node/coyle-house", "walk")
edge("edge/lane-to-lofts", "node/harbour-lane", "node/net-lofts", "stair")
edge("edge/lane-to-basin", "node/harbour-lane", "node/boatyard", "stair")
edge("edge/lane-to-market", "node/harbour-lane", "node/fish-market", "walk")
edge("edge/slipway", "node/boatyard", "node/fish-market", "stair")
edge("edge/market-to-seawall", "node/fish-market", "node/seawall", "walk")
edge("edge/seawall-to-chapel", "node/seawall", "node/seamens-chapel", "stair")
edge("edge/chapel-to-crypt", "node/seamens-chapel", "node/chapel-crypt", "stair")
edge("edge/seawall-to-customs", "node/seawall", "node/customs-house", "barred",
     gating={"flags": ["flag/customs-key"]}, opens_from="a")
edge("edge/basin-to-shed", "node/boatyard", "node/whalers-shed", "stair")
edge("edge/shed-to-ropewalk", "node/whalers-shed", "node/ropewalk", "walk")
edge("edge/ropewalk-to-breakwater", "node/ropewalk", "node/breakwater", "walk")
edge("edge/breakwater-to-lighthouse", "node/breakwater", "node/lighthouse", "walk")
edge("edge/seawall-to-slipway", "node/seawall", "node/slipway-stair", "stair")
edge("edge/lane-to-pier", "node/harbour-lane", "node/pier", "walk")
edge("edge/slipway-to-way", "node/slipway-stair", "node/pilgrims-way", "barred",
     gating={"flags": ["flag/lamps-lit"]}, opens_from="a")
edge("edge/way-to-wrecks", "node/pilgrims-way", "node/wreck-field", "walk")
edge("edge/wrecks-to-pillars", "node/wreck-field", "node/carved-pillars", "walk")
edge("edge/pillars-to-launch", "node/carved-pillars", "node/marracks-launch", "walk")
edge("edge/launch-to-mast", "node/marracks-launch", "node/mast-platform", "stair")
edge("edge/way-to-mud-wrecks-west", "node/pilgrims-way", "node/mud-wrecks-west", "walk")
edge("edge/way-to-mud-wrecks-east", "node/pilgrims-way", "node/mud-wrecks-east", "walk")
edge("edge/mud-wrecks-west-to-wrecks", "node/mud-wrecks-west", "node/wreck-field", "walk")
edge("edge/mud-wrecks-east-to-wrecks", "node/mud-wrecks-east", "node/wreck-field", "walk")
edge("edge/wrecks-to-mud-pillars-west", "node/wreck-field", "node/mud-pillars-west", "walk")
edge("edge/wrecks-to-launch", "node/wreck-field", "node/marracks-launch", "walk")
edge("edge/wrecks-to-mud-pillars-east", "node/wreck-field", "node/mud-pillars-east", "walk")
edge("edge/mud-pillars-west-to-launch", "node/mud-pillars-west", "node/marracks-launch", "walk")
edge("edge/pillars-to-mud-pillars-east", "node/carved-pillars", "node/mud-pillars-east", "walk")
edge("edge/mud-pillars-west-to-narrows-mud", "node/mud-pillars-west", "node/mud-narrows-west", "walk")
edge("edge/launch-to-narrows-mud", "node/marracks-launch", "node/mud-narrows-west", "walk")
edge("edge/pillars-to-narrows-mud", "node/carved-pillars", "node/mud-narrows-west", "walk")
edge("edge/narrows-to-narrows-mud", "node/narrows", "node/mud-narrows-west", "walk")
edge("edge/narrows-mud-to-stage", "node/mud-narrows-west", "node/skiff-stage", "walk")
edge("edge/pillars-to-narrows", "node/carved-pillars", "node/narrows", "walk")
edge("edge/narrows-to-shelf", "node/narrows", "node/narrows-shelf", "walk")
edge("edge/narrows-to-stage", "node/narrows", "node/skiff-stage", "walk")
edge("edge/stage-to-near-house", "node/skiff-stage", "node/near-ferry-house", "walk")
edge("edge/crossing-out", "node/near-ferry-house", "node/far-ferry-house", "carry",
     gating={"flags": ["flag/skiff-lent"]})
edge("edge/crossing-back", "node/far-ferry-house", "node/sea-skiff", "carry",
     gating={"quest": "quest/the-brow"}, one_way="a-to-b")
edge("edge/reveal-ashore", "node/sea-skiff", "node/near-ferry-house", "carry",
     gating={"quest": "quest/the-brow"}, one_way="a-to-b")
edge("edge/near-bell", "node/skiff-stage", "node/far-ferry-house", "carry",
     gating={"flags": ["flag/skiff-lent"]}, one_way="a-to-b")
edge("edge/far-bell", "node/far-landing", "node/near-ferry-house", "carry",
     gating={"flags": ["flag/skiff-lent"]}, one_way="a-to-b")
edge("edge/far-house-door", "node/far-ferry-house", "node/far-landing", "barred",
     gating={"flags": ["flag/skiff-lent"]}, opens_from="a")
edge("edge/landing-to-jaw", "node/far-landing", "node/jaw-bank", "walk")
edge("edge/landing-to-ridge", "node/far-landing", "node/flank-ridge", "walk")
edge("edge/jaw-to-mouth", "node/jaw-bank", "node/mouth", "walk")
edge("edge/mouth-to-throat", "node/mouth", "node/throat", "walk")
edge("edge/throat-to-cathedral", "node/throat", "node/rib-cathedral", "walk")
edge("edge/diaphragm", "node/rib-cathedral", "node/stomach", "barred",
     gating={"flags": ["flag/diaphragm-cut"]}, opens_from="a")
edge("edge/stomach-to-heart", "node/stomach", "node/heart-chamber", "walk")
edge("edge/heart-to-breach", "node/heart-chamber", "node/breach", "walk")
edge("edge/breach-to-ridge", "node/breach", "node/flank-ridge", "walk")
edge("edge/heart-to-spine", "node/heart-chamber", "node/spine-stair", "barred",
     gating={"flags": ["flag/beat-stopped"]}, opens_from="a")
edge("edge/spine-up", "node/spine-stair", "node/spine-top", "stair")
edge("edge/spine-to-crown", "node/spine-top", "node/crown", "stair")
edge("edge/crown-to-brow", "node/crown", "node/brow", "walk")
edge("edge/crown-to-back", "node/crown", "node/back-upper", "stair")
edge("edge/back-upper-to-middle", "node/back-upper", "node/back-middle", "stair")
edge("edge/back-middle-to-lower", "node/back-middle", "node/back-lower", "stair")
edge("edge/back-lower-to-tail", "node/back-lower", "node/tail-flank", "stair")
edge("edge/tail-flank-to-bank", "node/tail-flank", "node/tail-bank", "drop", falls="a-to-b")
edge("edge/tail-bank-to-road", "node/tail-bank", "node/tail-road", "walk")
edge("edge/road-to-run-bank", "node/tail-road", "node/run-bank", "walk")
edge("edge/run-bank-to-jaw", "node/run-bank", "node/jaw-bank", "walk")

# seams: edge -> dict(face, lo (world coord along the face, or (x,z) through a floor),
#                     opening | contact, form, stair_in)
S = {}


def seam(eid, face, lo, form, opening=None, contact=None, stair_in=None):
    S[eid] = dict(face=face, lo=lo, form=form, opening=opening, contact=contact,
                  stair_in=stair_in)


ARCH = "arch"
DOOR = "door"
PASS = "passage"
seam("edge/coach-to-steps", "south", 201, "the head of the covered steps off the coach road, a stone stair down 10", PASS, stair_in="node/cliff-steps")
seam("edge/steps-to-street", "south", 201, "the foot of the covered steps: a stone stair down 10 into the head of the High Street", PASS, stair_in="node/high-street")
seam("edge/street-to-lane", "south", 201, "the High Street's last flight, a stone stair down 10 onto the harbour lane", PASS, stair_in="node/harbour-lane")
seam("edge/lane-to-office", "north", 171, "the Harbour Office's street door off the lane", DOOR)
seam("edge/lane-to-coyle", "north", 127, "the Coyles' cottage door off the lane", DOOR)
seam("edge/lane-to-lofts", "north", 140, "a timber stair up 6 from the lane to the loft door", DOOR, stair_in="node/harbour-lane")
seam("edge/lane-to-basin", "south", 140, "quay steps down 2 into the emptied basin", PASS, stair_in="node/boatyard")
seam("edge/lane-to-market", "south", 178, "the market's north doors off the lane", ARCH)
seam("edge/slipway", "east", 112, "the slipway: a stone ramp up 2 from the basin mud through the market's sea doors", PASS, stair_in="node/boatyard")
seam("edge/market-to-seawall", "south", 175, "the market's open arcade onto the seawall", ARCH)
seam("edge/seawall-to-chapel", "north", 231, "stone steps up 4 from the seawall to the chapel door in its south gable", DOOR, stair_in="node/seawall")
seam("edge/chapel-to-crypt", "down", (229, 120), "a stone stair down 6 through the chapel floor into the crypt", DOOR, stair_in="node/chapel-crypt")
seam("edge/seawall-to-customs", "north", 202, "the Customs House door on the seawall, padlocked", DOOR)
seam("edge/basin-to-shed", "west", 112, "a boat ramp up 2 from the basin into the shed's big doors", PASS, stair_in="node/boatyard")
seam("edge/shed-to-ropewalk", "south", 110, "the doorway from the shed into the north end of the ropewalk", DOOR)
seam("edge/ropewalk-to-breakwater", "south", 110, "the ropewalk's south door onto the breakwater", DOOR)
seam("edge/breakwater-to-lighthouse", "south", 111, "the lighthouse door at the end of the breakwater", DOOR)
seam("edge/seawall-to-slipway", "south", 172, "the slipway stair's head: stone steps down 2 off the seawall", PASS, stair_in="node/slipway-stair")
seam("edge/lane-to-pier", "west", 93, "the pier's landward end off the lane", PASS)
seam("edge/slipway-to-way", "south", 172, "a rope across the foot of the stair, where the old road begins", PASS)
seam("edge/way-to-wrecks", "south", 171, "the way runs on into the wreck field", contact=[5, 2])
seam("edge/wrecks-to-pillars", "south", 171, "the way runs on past the wrecks", contact=[5, 2])
seam("edge/pillars-to-launch", "west", 292, "the mud beside the way to Marrack's launch", contact=[6, 2])
seam("edge/launch-to-mast", "up", (156, 303), "a timber stair up 11 from the mud to the mast platform", DOOR, stair_in="node/marracks-launch")
seam("edge/way-to-mud-wrecks-west", "west", 149, "the way's west shoulder down onto the mud", contact=[98, 2])
seam("edge/way-to-mud-wrecks-east", "east", 149, "the way's east shoulder down onto the mud", contact=[98, 2])
seam("edge/mud-wrecks-west-to-wrecks", "south", 120, "the mud runs on among the wrecks", contact=[50, 2])
seam("edge/mud-wrecks-east-to-wrecks", "south", 177, "the mud runs on among the wrecks", contact=[64, 2])
seam("edge/wrecks-to-mud-pillars-west", "south", 120, "the mud runs on south of the wrecks", contact=[19, 2])
seam("edge/wrecks-to-launch", "south", 140, "the mud runs on to Marrack's launch", contact=[24, 2])
seam("edge/wrecks-to-mud-pillars-east", "south", 183, "the mud runs on south of the wrecks", contact=[58, 2])
seam("edge/mud-pillars-west-to-launch", "east", 289, "the mud runs on to Marrack's launch", contact=[50, 2])
seam("edge/pillars-to-mud-pillars-east", "east", 289, "the mud behind the eastern pillars", contact=[50, 2])
seam("edge/mud-pillars-west-to-narrows-mud", "south", 120, "the mud runs on toward the narrows", contact=[19, 2])
seam("edge/launch-to-narrows-mud", "south", 140, "the mud runs on toward the narrows", contact=[24, 2])
seam("edge/pillars-to-narrows-mud", "south", 165, "the mud runs on toward the narrows", contact=[6, 2])
seam("edge/narrows-to-narrows-mud", "west", 340, "the ridge's west shoulder down onto the mud", contact=[52, 2])
seam("edge/narrows-mud-to-stage", "south", 164, "the mud up to the stone stage", contact=[7, 2])
seam("edge/pillars-to-narrows", "south", 172, "the way narrowing to the ridge", contact=[3, 2])
seam("edge/narrows-to-shelf", "east", 352, "the mud shelf off the side of the ridge", contact=[14, 2])
seam("edge/narrows-to-stage", "south", 172, "the ridge onto the stone stage", contact=[3, 2])
seam("edge/stage-to-near-house", "south", 170, "the near ferry house's land door", DOOR)
seam("edge/far-house-door", "south", 144, "the far ferry house's land door, shut from the start", DOOR)
seam("edge/landing-to-jaw", "east", 503, "the bank runs on under the head", contact=[10, 2])
seam("edge/landing-to-ridge", "south", 128, "the bank runs on along the west flank", contact=[12, 2])
seam("edge/jaw-to-mouth", "south", 175, "between the teeth onto the tongue", {"width": 6, "height": 3})
seam("edge/mouth-to-throat", "south", 176, "the mouth narrows into the throat", PASS)
seam("edge/throat-to-cathedral", "south", 176, "the throat opens into the chest", PASS)
seam("edge/diaphragm", "south", 180, "the diaphragm, a wall of membrane cut open with the Flensing Spade", {"width": 3, "height": 3})
seam("edge/stomach-to-heart", "west", 618, "a fold of flesh from the stomach into the heart chamber", PASS)
seam("edge/heart-to-breach", "west", 619, "the torn opening from the heart chamber into the breach", DOOR)
seam("edge/breach-to-ridge", "west", 619, "the wound's mouth onto the flank ridge", DOOR)
seam("edge/heart-to-spine", "north", 160, "the foot of the spine stair, closed by a fold of bone until the beat stops", {"width": 3, "height": 3})
seam("edge/spine-up", "north", 160, "the vertebra stair up 20 into the upper neck", PASS, stair_in="node/spine-stair")
seam("edge/spine-to-crown", "up", (160, 531), "the vertebra stair up 20 through the blowhole onto the crown", PASS, stair_in="node/spine-top")
seam("edge/crown-to-brow", "north", 172, "the crown falls forward onto the brow", contact=[6, 2])
seam("edge/crown-to-back", "south", 179, "down the back from the crown, the spine's steps", PASS, stair_in="node/back-upper")
seam("edge/back-upper-to-middle", "south", 179, "the spine's steps down onto the hump", PASS, stair_in="node/back-middle")
seam("edge/back-middle-to-lower", "south", 179, "the spine's steps down the knuckles", PASS, stair_in="node/back-lower")
seam("edge/back-lower-to-tail", "south", 179, "the spine's steps down onto the tail flank", PASS, stair_in="node/tail-flank")
seam("edge/tail-flank-to-bank", "south", 179, "the end of the tail flank, a drop of 6 onto the bank", PASS)
seam("edge/tail-bank-to-road", "east", 668, "the bank round the flukes", contact=[6, 2])
seam("edge/road-to-run-bank", "east", 656, "the bank turns north", contact=[6, 2])
seam("edge/run-bank-to-jaw", "west", 506, "the east bank comes round under the head", contact=[12, 2])

# ---------------------------------------------------------------------------
# what each place's walk is judged against (the brief)
FACTS = [
    ("fact/site-span", 400, "The whole map is four hundred blocks east to west: the town, the flat and the body with sea round them."),
    ("fact/site-depth", 760, "Seven hundred and sixty blocks north to south: town, flat, black water, bank and body."),
    ("fact/site-height", 100, "From y 30 under the sea floor to y 130 over the top of the head."),
    ("fact/coach-road-y", 96, "The coach road runs along the cliff top at y 96."),
    ("fact/harbour-y", 66, "The harbour quays stand at y 66, four over the sea."),
    ("fact/flat-y", 64, "The flat's mud walk plane, one course over the sea water under it."),
    ("fact/crown-y", 104, "The top of the head, forty blocks over the flat."),
    ("fact/channel-width", 60, "The black water between the skiff stage and the body's bank is about sixty blocks wide."),
    ("fact/way-length", 240, "The Pilgrims' Way runs at least two hundred and forty blocks from the slipway stair to the narrows."),
    ("fact/cathedral-height", 30, "The rib vault of the chest is thirty blocks high."),
    ("fact/narrows-width", 3, "The ridge of the narrows is three blocks wide."),
]
IDENT = [
    ("fact/site-span", "eq", {"of": "region-extent", "axis": "x"}),
    ("fact/site-depth", "eq", {"of": "region-extent", "axis": "z"}),
    ("fact/site-height", "eq", {"of": "region-extent", "axis": "y"}),
    ("fact/coach-road-y", "eq", {"of": "datum-y", "datum": "datum/coach-road"}),
    ("fact/harbour-y", "eq", {"of": "datum-y", "datum": "datum/harbour"}),
    ("fact/flat-y", "eq", {"of": "datum-y", "datum": "datum/flat"}),
    ("fact/crown-y", "eq", {"of": "datum-y", "datum": "datum/crown"}),
    ("fact/way-length", "le", {"of": "distance-xz", "from": "node/pilgrims-way", "to": "node/narrows"}),
    ("fact/cathedral-height", "eq", {"of": "box-height", "node": "node/rib-cathedral"}),
    ("fact/narrows-width", "eq", {"of": "box-extent", "node": "node/narrows", "axis": "x"}),
]

# the walk through the story, in the order the quests walk it
CRITICAL = [
    "node/coach-road", "node/cliff-steps", "node/high-street", "node/harbour-lane",
    "node/harbour-office", "node/harbour-lane", "node/fish-market", "node/seawall",
    "node/seamens-chapel", "node/seawall", "node/customs-house", "node/seawall",
    "node/fish-market", "node/boatyard", "node/whalers-shed", "node/ropewalk",
    "node/breakwater", "node/lighthouse", "node/breakwater", "node/ropewalk",
    "node/whalers-shed", "node/boatyard", "node/fish-market", "node/seawall",
    "node/slipway-stair", "node/pilgrims-way", "node/wreck-field", "node/carved-pillars",
    "node/marracks-launch", "node/carved-pillars", "node/narrows", "node/skiff-stage",
    "node/near-ferry-house", "node/far-ferry-house", "node/far-landing", "node/jaw-bank",
    "node/mouth", "node/throat", "node/rib-cathedral", "node/stomach", "node/heart-chamber",
    "node/spine-stair", "node/spine-top", "node/crown", "node/brow", "node/crown", "node/back-upper",
    "node/back-middle", "node/back-lower", "node/tail-flank", "node/tail-bank",
    "node/tail-road", "node/run-bank", "node/jaw-bank", "node/far-landing",
    "node/far-ferry-house", "node/sea-skiff", "node/near-ferry-house", "node/skiff-stage",
    "node/narrows", "node/carved-pillars", "node/wreck-field", "node/pilgrims-way",
    "node/slipway-stair", "node/seawall", "node/fish-market", "node/harbour-lane", "node/pier",
]

BEATS = [
    ("quest/the-coach-road", "obj/the-notice", "node/coach-road"),
    ("quest/the-harbourmistress", "obj/hear-wenna", "node/harbour-office"),
    ("quest/the-fish-market", "obj/the-slipway-drowned", "node/fish-market"),
    ("quest/the-fish-market", "obj/the-market-slate", "node/fish-market"),
    ("quest/the-rubbing", "obj/hear-tregear", "node/seamens-chapel"),
    ("quest/the-customs-house", "obj/unlock-customs", "node/seawall"),
    ("quest/the-customs-house", "obj/the-chart", "node/customs-house"),
    ("quest/the-customs-house", "obj/the-chip", "node/customs-house"),
    ("quest/the-shut-harbour", "obj/the-shipwright-note", "node/boatyard"),
    ("quest/the-shut-harbour", "obj/the-hull-drowned", "node/boatyard"),
    ("quest/the-shut-harbour", "obj/the-spade", "node/whalers-shed"),
    ("quest/the-lighthouse", "obj/light-the-lamp", "node/lighthouse"),
    ("quest/the-wreck-field", "obj/wenna-at-the-stair", "node/slipway-stair"),
    ("quest/the-wreck-field", "obj/the-wreck-drowned", "node/wreck-field"),
    ("quest/the-wreck-field", "obj/the-wreck-drowned-2", "node/wreck-field"),
    ("quest/the-wreck-field", "obj/the-nameboard", "node/wreck-field"),
    ("quest/marrack", "obj/hear-marrack", "node/marracks-launch"),
    ("quest/marrack", "obj/the-pillars", "node/carved-pillars"),
    ("quest/the-narrows", "obj/the-chalk-arrow", "node/mouth"),
    ("quest/the-throat", "obj/the-wrong-rib", "node/throat"),
    ("quest/the-throat", "obj/the-lice", "node/rib-cathedral"),
    ("quest/the-cathedral", "obj/cut-the-diaphragm", "node/rib-cathedral"),
    ("quest/the-cathedral", "obj/marracks-men", "node/stomach"),
    ("quest/the-cathedral", "obj/the-shore", "node/stomach"),
    ("quest/the-heart", "obj/davey", "node/heart-chamber"),
    ("quest/the-heart", "obj/davey-wakes", "node/heart-chamber"),
    ("quest/the-brow", "obj/cut-the-stone", "node/brow"),
    ("quest/the-run", "obj/davey-in-the-skiff", "node/far-ferry-house"),
    ("quest/the-run", "obj/home", "node/pier"),
    ("quest/the-pier", "obj/the-choice", "node/pier"),
]

ATMOS = {}  # node -> atmosphere carried from the first tick (filled by set_atmospheres)


def set_atmospheres():
    # the flat carries the wrong place from the first tick; the body's bank and
    # its outside are painted by the lamps beat, because their paint meets the
    # inside's at the mouth and the breach (DW0929)
    wrong = ["node/pilgrims-way", "node/wreck-field", "node/carved-pillars", "node/marracks-launch",
             "node/mast-platform", "node/narrows", "node/narrows-shelf", "node/skiff-stage",
             "node/mud-wrecks-west", "node/mud-wrecks-east", "node/mud-pillars-west",
             "node/mud-pillars-east", "node/mud-narrows-west"]
    inside = ["node/mouth", "node/throat", "node/rib-cathedral", "node/stomach",
              "node/heart-chamber", "node/breach", "node/spine-stair", "node/spine-top"]
    for n in wrong:
        ATMOS[n] = "atmosphere/wrong-place"
    for n in inside:
        ATMOS[n] = "atmosphere/inside-body"


# ---------------------------------------------------------------------------
# terrain


TOWN_PADS = ["node/coach-road", "node/cliff-steps", "node/high-street", "node/harbour-lane",
             "node/harbour-office", "node/coyle-house", "node/net-lofts", "node/boatyard",
             "node/fish-market", "node/seawall", "node/seamens-chapel", "node/customs-house",
             "node/whalers-shed", "node/ropewalk", "node/slipway-stair"]


def _base_terrain(x, z):
    # the town on its cliff: the land north of the seawall
    if 118 <= x <= 300 and z <= 138:
        if z <= 14:
            return 95
        if z <= 30:
            return 85
        if z <= 75:
            return 75
        return 65
    # the west harbour arm (shed, ropewalk) stands on land at 65
    if (100 <= x <= 123 and 103 <= z <= 140) or (100 <= x <= 117 and 141 <= z <= 161):
        return 65
    # the flat: sea water four deep under the mud fields and the way
    if 118 <= x <= 242 and 147 <= z <= 392:
        return 58
    # its beach: one course under the walk plane, a swimmer climbs out onto it
    if 112 <= x <= 248 and 141 <= z <= 398:
        return 62
    # the body's bank, walk plane 64, a water trench under the run bank
    if 210 <= x <= 221 and 503 <= z <= 666:
        return 58
    if 126 <= x <= 226 and 498 <= z <= 690:
        return 63
    if 120 <= x <= 232 and 492 <= z <= 696:
        return 62
    return 46


_PAD_CACHE = {}


def terrain(x, z):
    """Surface y of the site's ground at a column (world): the base landform,
    with every town place's plot and ring padded to one under its floor."""
    if not _PAD_CACHE:
        for nid in TOWN_PADS:
            p = P[nid]
            for xx in range(p["x"] - 1, x1(p) + 2):
                for zz in range(p["z"] - 1, z1(p) + 2):
                    if any(q["base"] and q["x"] - 1 <= xx <= x1(q) + 1 and q["z"] - 1 <= zz <= z1(q) + 1
                           for q in P.values()):
                        continue
                    _PAD_CACHE[(xx, zz)] = fy(p) - 1
    if (x, z) in _PAD_CACHE:
        return _PAD_CACHE[(x, z)]
    return _base_terrain(x, z)


def heightmap():
    X, Z = REGION_EXT[0], REGION_EXT[2]

    def v(px, pz):
        return terrain(REGION_MIN[0] + px, REGION_MIN[2] + pz) - TERRAIN_BASE
    pngio.write_grey(os.path.join(CAMPAIGN, "terrain", "site.png"), X, Z, v)


# ---------------------------------------------------------------------------
# emission


def env(stage, content):
    return {"campaign_id": CID, "content": content, "dsl_version": DSL, "stage": stage}


def faces(p, face):
    """(axis, low, high) of the face's cells along it, and the plane coordinate."""
    raise NotImplementedError


def seam_doc(e):
    s = S[e["id"]]
    a, b = P[e["a"]], P[e["b"]]
    face = s["face"]
    doc = {"edge": e["id"], "face": face, "form": s["form"]}
    if face in ("north", "south"):
        doc["at"] = s["lo"] - a["x"]
        doc["meets"] = s["lo"] - b["x"]
    elif face in ("east", "west"):
        doc["at"] = s["lo"] - a["z"]
        doc["meets"] = s["lo"] - b["z"]
    else:
        lx, lz = s["lo"]
        doc["at"] = [lx - a["x"], lz - a["z"]]
        doc["meets"] = [lx - b["x"], lz - b["z"]]
    if s["contact"] is not None:
        doc["contact"] = {"extent": s["contact"]}
    else:
        doc["opening"] = s["opening"]
    if s["stair_in"]:
        doc["stair_in"] = s["stair_in"]
    return doc


def box_doc(p):
    d = {"node": p["node"], "extent": [p["dx"], p["dz"]], "min": [p["x"], p["z"]]}
    f = p["floor"]
    d["floor"] = {"datum": f} if isinstance(f, str) else {"y": f}
    kind, n = p["ceiling"]
    d["ceiling"] = {kind: n}
    if p["roof"]:
        d["roof"] = p["roof"]
    if p["base"]:
        d["base"] = p["base"]
    if p["node"] in ATMOS:
        d["atmosphere"] = ATMOS[p["node"]]
    return d


def write(name, doc):
    with open(os.path.join(CAMPAIGN, name), "w") as f:
        json.dump(doc, f, indent=2, sort_keys=True, ensure_ascii=False)
        f.write("\n")


def main():
    set_atmospheres()
    os.makedirs(os.path.join(CAMPAIGN, "terrain"), exist_ok=True)
    heightmap()
    write("geometry-brief.json", env("geometry-brief", {"facts": [
        {"id": i, "value": float(v), "unit": "blocks", "note": n} for i, v, n in FACTS]}))
    nodes = []
    for nid in ORDER:
        p = P[nid]
        nd = {"id": nid, "intent": p["intent"]}
        if p["note"]:
            nd["note"] = p["note"]
        if p["stations"]:
            nd["stations"] = p["stations"]
        if not p["reached"]:
            nd["reached"] = False
        nodes.append(nd)
    edges = []
    for e in E:
        ed = {"id": e["id"], "a": e["a"], "b": e["b"], "class": e["cls"]}
        for k in ("gating", "one_way", "opens_from", "shortcut", "falls"):
            if k in e:
                ed[k] = e[k]
        edges.append(ed)
    write("layout-graph.json", env("layout-graph", {
        "nodes": nodes, "edges": edges, "entry": "node/coach-road", "goal": "node/pier",
        "critical_path": CRITICAL,
        "beats": [{"quest": q, "objective": o, "node": n} for q, o, n in BEATS]}))
    write("site-plan.json", env("site-plan", {
        "region": {"min": list(REGION_MIN), "extent": list(REGION_EXT)},
        "datums": [{"id": k, "y": v} for k, v in DATUMS.items()],
        "fill": {"kind": "open", "surface": "minecraft:mud", "below": "minecraft:packed_mud",
                 "terrain": {"kind": "heightmap", "heightmap": "terrain/site.png",
                             "base_y": TERRAIN_BASE, "range": 255}},
        "boxes": [box_doc(P[n]) for n in ORDER],
        "seams": [seam_doc(e) for e in E if e["cls"] not in ("vision", "carry")],
        "identities": [{"fact": f, "cmp": c, "measure": m} for f, c, m in IDENT],
        "max_drop": 6,
    }))


if __name__ == "__main__":
    main()
