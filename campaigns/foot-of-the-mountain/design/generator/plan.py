#!/usr/bin/env python3
"""The town at the foot of the mountain: the whole plan, generated.

Writes world.json, layout-graph.json, site-plan.json, geometry-brief.json,
quest-plan.json, quests.json and terrain/island.png into the campaign
directory. Stdlib only. Deterministic: no clock, no unseeded randomness.

Axes: +x east, +z south. The sea is south; the mountain is north. The main
street runs north to south from the square at the mountain's foot down to the
quay. Every box but the square is placed by the seam packing; this script
mirrors that packing to shape the terrain under each box.
"""
import json
import math
import os
import struct
import sys
import zlib

CAMPAIGN = "foot-of-the-mountain"
DSL = "0.69.0"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))

RX, RZ = 320, 512          # region footprint (saltstair-a: 144 x 224; 5.08x)
RY0, RYN = 40, 176         # region y span
BASE_Y, RANGE = 48, 160    # heightmap: y = 48 + v * 160 // 255
SEA = 62

boxes = []                 # site-plan boxes, in order
seams = []
nodes = []
edges = []
pos = {}                   # node -> (x0, z0, dx, dz, floor)


def box(node, extent, floor, ceiling, intent, note, holds=None, way=None,
        roof=None, pin=None):
    b = {"node": node, "extent": list(extent), "floor": {"y": floor},
         "ceiling": ceiling}
    if way:
        b["way"] = way
    if roof:
        b["roof"] = roof
    if pin:
        b["min"] = list(pin)
        pos[node] = (pin[0], pin[1], extent[0], extent[1], floor)
    boxes.append(b)
    n = {"id": node, "intent": intent, "note": note}
    if holds:
        n["holds"] = holds
    nodes.append(n)
    return b


def ext(node):
    for b in boxes:
        if b["node"] == node:
            return b["extent"], b["floor"]["y"]
    raise KeyError(node)


def seam(a, b, face, at, meets, kind, form):
    """Join a to b on a's `face`; place b by the packing rule."""
    eid = "edge/" + a.split("/")[1] + "-to-" + b.split("/")[1]
    s = {"edge": eid, "face": face, "at": at, "meets": meets, "form": form}
    cls = "walk"
    if kind == "contact":
        s["contact"] = {}
    elif kind == "stair":   # a is the upper place, b the flight below it
        (bdx, bdz), _ = ext(b)
        w = bdx if face in ("north", "south") else bdz
        s["opening"] = {"width": w, "height": 4}
        s["stair_in"] = b
        cls = "stair"
    seams.append(s)
    edges.append({"a": a, "b": b, "class": cls, "id": eid})
    ax, az, adx, adz, _ = pos[a]
    (bdx, bdz), bf = ext(b)
    # the packing leaves the one shared ring cell between two boxes
    if face == "south":
        p = (ax + at - meets, az + adz + 1)
    elif face == "north":
        p = (ax + at - meets, az - bdz - 1)
    elif face == "east":
        p = (ax + adx + 1, az + at - meets)
    else:
        p = (ax - bdx - 1, az + at - meets)
    pos[b] = (p[0], p[1], bdx, bdz, bf)
    return eid


OPEN = lambda n: {"open": n}

# ---------------------------------------------------------------- the square
SQF = 84                     # the square, at the mountain's foot
SQ = (108, 230)
box("node/square", (30, 24), SQF, OPEN(8), "the square",
    "The square at the top of the town, at the mountain's foot: the cathedral's "
    "west front on its east side, the inn on its west, the castle road leaving "
    "north up the mountain and the main street leaving south down to the sea. "
    "Cobbled, with a well at its middle and benches under two trees.",
    pin=SQ)

# ------------------------------------------------------- the main street
# Ten short flights of two, so the street and the plots beside it follow the
# slope in small steps: neighbours differ by two at most.
STREET_W, SEG_L, FLIGHT_L, NFL = 7, 14, 6, 10
segs = []
prev = "node/square"
floor = SQF
for k in range(1, NFL + 1):
    fl = f"node/flight-{k}"
    floor -= 2
    box(fl, (STREET_W, FLIGHT_L), floor, OPEN(10), "a flight of the main street",
        f"Flight {k} of the main street: seven wide, two shallow steps down, "
        "between low kerbs.", way={"axis": "z", "clear": 5})
    seam(prev, fl, "south", 11 if prev == "node/square" else 0, 0,
         "stair", f"flight {k}: two down, the full width")
    if k == NFL:
        break
    sg = f"node/street-{k}"
    box(sg, (STREET_W, SEG_L), floor, OPEN(8), "a stretch of the main street",
        f"Stretch {k} of the main street, walk plane {floor}: cobbles with a "
        "kerb, the plots' fronts on both sides.", way={"axis": "z", "clear": 5})
    seam(fl, sg, "south", 0, 0, "contact", "the street runs on at grade")
    segs.append(sg)
    prev = sg

# the quay at the foot of the street; the basin beyond it is the sea itself
box("node/quay", (60, 10), floor, OPEN(8), "the quay",
    f"The quay at the foot of the street: a long stone wharf at walk plane {floor}, "
    "bollards, stacked crates and nets, the open water of the harbour basin beyond.",
    way={"axis": "x", "clear": 8})
seam(f"node/flight-{NFL}", "node/quay", "south", 0, 27, "contact",
     "the last flight lands on the quay")
QUAYF = floor

# ------------------------------------------------------------- the cathedral
box("node/cathedral", (56, 38), SQF, OPEN(46), "the cathedral",
    "A large cathedral in the manner of Vesperhold's Chapel of Hours: a long "
    "nave running east from a west front on the square, aisles under flying "
    "buttresses, a transept, an apse at the east end and a tall bell tower at "
    "the north-west corner; a walled churchyard on the south side.",
    holds=[
        {"id": "part/church", "kind": "structure", "cells": 1100, "height": 28,
         "use": "the cathedral: nave, aisles, transept and apse, entered by the west door from the square"},
        {"id": "part/tower", "kind": "structure", "cells": 64, "height": 42,
         "reached": False,
         "use": "the bell tower at the north-west corner, its spire over the town"},
        {"id": "part/close", "kind": "ground", "cells": 300,
         "use": "the paved close before the west front, joining the square"},
        {"id": "part/churchyard", "kind": "ground", "cells": 380,
         "use": "the churchyard south of the nave, graves and yews inside a low wall"},
    ])
seam("node/square", "node/cathedral", "east", 0, 14, "contact",
     "the close before the west front opens onto the square")

# ------------------------------------------------------------------- the inn
box("node/inn", (28, 24), SQF, OPEN(16), "the inn",
    "The Bell, a large timber-framed coaching inn on the square's west side: "
    "an L of a taproom and a stable range around a cobbled yard.",
    holds=[
        {"id": "part/inn-house", "kind": "structure", "cells": 200, "height": 12,
         "use": "the inn: a taproom in front, a kitchen behind it, through a door"},
        {"id": "part/stables", "kind": "structure", "cells": 90, "height": 8,
         "use": "the stable range, open-fronted onto the yard"},
        {"id": "part/inn-yard", "kind": "ground", "cells": 160,
         "use": "the inn yard, a trough and a cart"},
    ])
seam("node/square", "node/inn", "west", 0, 0, "contact",
     "the inn's front yard opens onto the square")

# ----------------------------------------------------------- the castle road
# Doune's gate faces north. The road leaves the square northward and climbs
# the mountain's west flank in switchbacks: legs that follow the contour east
# and west, each turning north up a ramp at its end, then runs along the
# castle's north side to Doune's approach (a contact on the north face at 74).
ROAD_W, RAMP_L = 5, 10
CASTLE_WALK = 164            # Doune's grade walk, the castle box's floor: 80 over the square
OPP = {"north": "south", "south": "north", "east": "west", "west": "east"}


def place_next(prev, node, face, align):
    """Put `node` beside `prev` across `face`, one ring cell apart; `align`
    is 'lo' or 'hi': which end of prev's face the 5-wide road continues at."""
    ax, az, adx, adz, _ = pos[prev]
    (bdx, bdz), bf = ext(node)
    if face in ("north", "south"):
        x = ax if align == "lo" else ax + adx - bdx
        z = az - bdz - 1 if face == "north" else az + adz + 1
    else:
        z = az if align == "lo" else az + adz - bdz
        x = ax - bdx - 1 if face == "west" else ax + adx + 1
    pos[node] = (x, z, bdx, bdz, bf)


def join(a, b, face, kind, form):
    """A seam between two placed boxes, `b` across `a`'s `face`; at/meets read
    off the placement. kind: 'contact', or 'stair' (a is the upper place)."""
    ax, az, adx, adz, _ = pos[a]
    bx, bz, bdx, bdz, _ = pos[b]
    if face in ("north", "south"):
        lo = max(ax, bx); at, meets = lo - ax, lo - bx
        w = min(ax + adx, bx + bdx) - lo
    else:
        lo = max(az, bz); at, meets = lo - az, lo - bz
        w = min(az + adz, bz + bdz) - lo
    eid = "edge/" + a.split("/")[1] + "-to-" + b.split("/")[1]
    s = {"edge": eid, "face": face, "at": at, "meets": meets, "form": form}
    if kind == "contact":
        s["contact"] = {}
        cls = "walk"
    else:
        s["opening"] = {"width": w, "height": 4}
        s["stair_in"] = b
        cls = "stair"
    seams.append(s)
    edges.append({"a": a, "b": b, "class": cls, "id": eid})


CLIMB_RUN = 12
# Four traverses along the contours of the castle hill's west shoulder, each
# climbing twelve, joined by climbs up the slope between them; each traverse
# stands some forty-five cells above the last, so the hillside between two
# legs is a natural slope, never a bank.
ROUTE = [  # (direction of travel, kind, length): kind run (level) or ramp (+4)
    ("north", "run", 4),
    ("north", "ramp", RAMP_L), ("north", "run", CLIMB_RUN),
    ("west", "run", 8), ("west", "ramp", RAMP_L), ("west", "run", 8), ("west", "ramp", RAMP_L),
    ("west", "run", 8), ("west", "ramp", RAMP_L), ("west", "run", 8),
    ("north", "ramp", RAMP_L), ("north", "run", CLIMB_RUN),
    ("north", "ramp", RAMP_L), ("north", "run", CLIMB_RUN),
    ("east", "run", 8), ("east", "ramp", RAMP_L), ("east", "run", 8), ("east", "ramp", RAMP_L),
    ("east", "run", 8), ("east", "ramp", RAMP_L), ("east", "run", 8),
    ("north", "ramp", RAMP_L), ("north", "run", CLIMB_RUN),
    ("north", "ramp", RAMP_L), ("north", "run", CLIMB_RUN),
    ("west", "run", 8), ("west", "ramp", RAMP_L), ("west", "run", 8), ("west", "ramp", RAMP_L),
    ("west", "run", 8), ("west", "ramp", RAMP_L), ("west", "run", 8),
    ("north", "ramp", RAMP_L), ("north", "run", CLIMB_RUN),
    ("north", "ramp", RAMP_L), ("north", "run", CLIMB_RUN),
    ("east", "run", 8), ("east", "ramp", RAMP_L), ("east", "run", 8), ("east", "ramp", RAMP_L),
    ("east", "run", 8), ("east", "ramp", RAMP_L), ("east", "run", 8),
    ("north", "ramp", RAMP_L), ("north", "run", CLIMB_RUN),
]
prev, prev_dir, floor, rising = "node/square", "north", SQF, False
for k, (d, kind, L) in enumerate(ROUTE, 1):
    node = f"node/road-{k}"
    ext_ = (ROAD_W, L) if d in ("north", "south") else (L, ROAD_W)
    axis = "z" if d in ("north", "south") else "x"
    if kind == "ramp":
        box(node, ext_, floor, OPEN(10), "a ramp of the castle road",
            "A ramp of the castle road: a cobbled stair-road, one step every two "
            "cells, the hillside meeting it on both sides.", way={"axis": axis, "clear": 4})
    else:
        box(node, ext_, floor, OPEN(8), "the castle road",
            "The castle road along the mountain's flank, cobbled and level, the "
            "slope above it and below it running up to its edges.", way={"axis": axis, "clear": 4})
    if prev == "node/square":
        (sx, sz, sdx, sdz, _) = pos[prev]
        pos[node] = (sx + 13, sz - L - 1, ROAD_W, L, floor)
    else:
        # a turn joins at the end of the previous leg the road came along
        align = {"west": "lo", "east": "hi"}.get(prev_dir, "lo") if d == "north" else (
            "lo" if prev_dir == "north" else "lo")
        if d in ("west", "east") and prev_dir == "north":
            align = "lo"            # the turn leaves from the north end of a run up the slope
        place_next(prev, node, d, align)
    if rising:                      # prev was a ramp: node is the upper place
        join(node, prev, OPP[d], "stair", "the ramp climbs to the road")
    else:
        join(prev, node, d, "contact", "the road runs on")
    rising = kind == "ramp"
    if rising:
        floor += 4
        # the place after a ramp stands four higher
    prev, prev_dir = node, d
assert not rising and floor == CASTLE_WALK, floor

box("node/road-top", (10, ROAD_W), CASTLE_WALK, OPEN(8), "the castle road's last stretch",
    "The road's last stretch, level along the castle's north side to the head "
    "of Doune's approach.", way={"axis": "x", "clear": 4})
CASTLE_X0 = 170
rx = pos[prev][0]
L = CASTLE_X0 + 74 + ROAD_W - rx
boxes[-1]["extent"] = [L, ROAD_W]
place_next(prev, "node/road-top", "north", "lo")
join(prev, "node/road-top", "north", "contact", "the road turns east under the castle")
box("node/gate-road", (5, 8), CASTLE_WALK, OPEN(6), "the road onto Doune's approach",
    "The last stretch of the road from the town, arriving on the hilltop at the "
    "start of Doune's own approach road, five wide.", way={"axis": "z", "clear": 5})
place_next("node/road-top", "node/gate-road", "south", "hi")
join("node/road-top", "node/gate-road", "south", "contact",
     "the road turns south onto Doune's approach")
box("node/castle", (102, 118), CASTLE_WALK, OPEN(48), "the castle",
    "Doune Castle, copied whole as one plot: the gatehouse, the hall range, the "
    "kitchen tower, the courtyard, the curtain and the three ditches on the north "
    "approach.")
gx, gz = pos["node/gate-road"][0], pos["node/gate-road"][1]
pos["node/castle"] = (gx - 74, gz + 8 + 1, 102, 118, CASTLE_WALK)
seams.append({"edge": "edge/road-to-gate", "face": "north", "at": 74,
              "contact": {"extent": [5, 6]},
              "form": "Doune's approach road running on, level, onto the hilltop road: five wide, no wall across it"})
edges.append({"a": "node/castle", "b": "node/gate-road", "class": "walk",
              "id": "edge/road-to-gate"})

# --------------------------------------------------------------------- plots
THEMES = {
    "smithy": ("the smithy", "A blacksmith's yard: an open-walled forge shed under a deep roof, the smith's house behind it, a work yard with a quench trough.",
               [("structure", "house", 0.22, 9, "the smith's house: front room, back kitchen"),
                ("structure", "forge", 0.16, 7, "the open-walled forge: anvil, bellows, hearth under a hood"),
                ("ground", "work-yard", 0.22, None, "the work yard, a quench trough and stacked iron")]),
    "bakery": ("the bakery", "A baker's: a shop with a counter in front and the bake room behind it through a door, a domed oven house in the yard.",
               [("structure", "shop", 0.30, 10, "the shop in front and the bake room behind it, joined by a door"),
                ("structure", "oven", 0.06, 5, "a domed bread oven under a lean-to"),
                ("ground", "yard", 0.24, None, "the back yard, a woodpile and flour sacks")]),
    "weaver": ("the weaver's house", "A weaver's tall house with a loom room on the ground floor, a drying yard of cloth on lines and a dye shed.",
               [("structure", "house", 0.30, 12, "the weaver's house: loom room, stair up to the cloth store"),
                ("structure", "dye-shed", 0.08, 6, "an open dye shed with vats"),
                ("ground", "drying-yard", 0.22, None, "the drying yard, cloth hung on lines")]),
    "chandler": ("the chandler's", "A ship chandler's shop with a long store behind it, rope coils and barrels in the yard.",
                 [("structure", "shop", 0.34, 9, "the shop with its counter and the long store behind it through a door"),
                  ("ground", "yard", 0.26, None, "the yard, rope coils, barrels and a handcart")]),
    "cooper": ("the cooper's", "A cooper's workshop, open-fronted, with the family house beside it and barrels stacked in the yard.",
               [("structure", "workshop", 0.18, 7, "the open-fronted cooperage, staves and hoops"),
                ("structure", "house", 0.18, 9, "the cooper's house"),
                ("ground", "yard", 0.24, None, "the barrel yard")]),
    "apothecary": ("the apothecary", "An apothecary's narrow house with a physic garden behind it.",
                   [("structure", "house", 0.30, 11, "the shop with jars and a still room behind it"),
                    ("ground", "garden", 0.30, None, "the physic garden in raised beds")]),
    "merchant": ("the merchant's house", "A rich merchant's U-shaped stone house around a front court, a counting room by the door.",
                 [("structure", "house", 0.40, 13, "the merchant's house: counting room, hall, stair"),
                  ("ground", "court", 0.20, None, "the front court with a fountain")]),
    "tavern": ("the tavern", "A low sailors' tavern with a beer garden under a vine pergola.",
               [("structure", "tavern", 0.32, 9, "the taproom and the cellar stair"),
                ("ground", "garden", 0.28, None, "the beer garden under a pergola")]),
    "fishmonger": ("the fishmonger's", "A fishmonger's open stall-front with the smokehouse behind it.",
                   [("structure", "stall", 0.20, 7, "the open stall-front with a slab counter"),
                    ("structure", "smokehouse", 0.12, 8, "the smokehouse"),
                    ("ground", "yard", 0.24, None, "the yard with drying racks")]),
    "netloft": ("the net loft", "A tall net loft over a boat store, nets drying on poles in the yard.",
                [("structure", "loft", 0.30, 12, "the net loft over the boat store"),
                 ("ground", "yard", 0.28, None, "the yard with net poles")]),
    "tannery": ("the tannery", "A tanner's long shed with pits in the yard and the tanner's cottage.",
                [("structure", "shed", 0.20, 7, "the long open shed with hides on racks"),
                 ("structure", "cottage", 0.14, 8, "the tanner's cottage"),
                 ("ground", "pits", 0.24, None, "the yard of tanning pits")]),
    "carpenter": ("the carpenter's", "A carpenter's workshop and timber yard with a saw pit.",
                  [("structure", "workshop", 0.26, 9, "the workshop and the house over it"),
                   ("ground", "timber-yard", 0.32, None, "the timber yard and the saw pit")]),
    "cottages": ("a pair of cottages", "Two small fishermen's cottages with front gardens and a shared back yard.",
                 [("structure", "cottage-a", 0.16, 8, "the first cottage"),
                  ("structure", "cottage-b", 0.16, 8, "the second cottage"),
                  ("ground", "gardens", 0.26, None, "front gardens and the shared yard")]),
    "boatwright": ("the boatwright's", "A boatwright's shed with a hull on the stocks, open to the lane.",
                   [("structure", "shed", 0.30, 10, "the open boat shed with a hull on the stocks"),
                    ("ground", "yard", 0.28, None, "the yard with timber and a winch")]),
    "townhall": ("the guildhall", "The guildhall: a hall on an open arcade, a clock over the door.",
                 [("structure", "hall", 0.42, 14, "the guildhall over its open arcade"),
                  ("ground", "forecourt", 0.20, None, "the forecourt")]),
    "harbour": ("the harbour", "The harbourmaster's house on the quay's east end, and the fishing boats moored along its edge as fixed builds.",
                [("structure", "harbourmaster", 0.22, 9, "the harbourmaster's house: an office facing the quay, a store behind"),
                 ("structure", "boats", 0.20, 6, "fishing boats moored along the quay's edge, masts and furled sails"),
                 ("ground", "quayside", 0.30, None, "the quayside: bollards, nets, crates")]),
    "lighthouse": ("the lighthouse", "A tall white lighthouse on the headland with the keeper's cottage and a walled yard.",
                   [("structure", "tower", 0.14, 30, "the lighthouse tower, a stair to the lantern room"),
                    ("structure", "cottage", 0.16, 8, "the keeper's cottage"),
                    ("ground", "yard", 0.30, None, "the walled yard and the cliff path")]),
}


def holds_for(theme, dx, dz):
    area = dx * dz
    out = []
    for kind, pid, share, h, use in THEMES[theme][2]:
        p = {"id": f"part/{pid}", "kind": kind, "use": use,
             "cells": max(4, int(area * share))}
        if h:
            p["height"] = h
        out.append(p)
    return out


def plot(name, theme, street, face, at, meets, dx, dz):
    theme = theme.split("-")[0]
    node = f"node/{name}"
    _, f = ext(street)
    intent, note, _ = THEMES[theme]
    box(node, (dx, dz), f, OPEN(16 if theme != "lighthouse" else 34), intent,
        note, holds=holds_for(theme, dx, dz))
    seam(street, node, face, at, meets, "contact",
         f"the plot's front opens onto the street")
    return node


def overlaps(a, b, gap=0):
    ax, az, adx, adz, _ = a
    bx, bz, bdx, bdz, _ = b
    return not (ax + adx + gap <= bx or bx + bdx + gap <= ax or
                az + adz + gap <= bz or bz + bdz + gap <= az)


# two places one cell apart ask to draw one wall (DW0827): any pair not joined
# by a seam keeps two cells between its footprints


# side streets: from street-2 west, street-4 east, street-6 east to the light
SIDE = {("node/street-3", "west"): 40, ("node/street-5", "east"): 40,
        ("node/street-8", "east"): 46}
for (sg, face), L in SIDE.items():
    k = sg.split("-")[1]
    sname = f"node/lane-{k}"
    _, f = ext(sg)
    box(sname, (L, 5), f, OPEN(8), "a side street",
        f"A side street off stretch {k}, cobbled, five wide, plots along it.",
        way={"axis": "x", "clear": 4})
    seam(sg, sname, face, 5, 0, "contact", "the side street leaves the main street")

MAIN = [  # (street, face, theme, dx, dz, at): a plot stays inside its stretch
    ("street-1", "west", "bakery", 22, 10, 2), ("street-1", "east", "apothecary", 18, 10, 2),
    ("street-2", "west", "cottages", 20, 10, 2), ("street-2", "east", "merchant", 26, 12, 1),
    ("street-3", "east", "weaver", 22, 10, 2),
    ("street-4", "west", "townhall", 24, 10, 2), ("street-4", "east", "tavern", 24, 10, 2),
    ("street-5", "west", "smithy", 24, 10, 2),
    ("street-6", "west", "chandler", 20, 10, 2), ("street-6", "east", "cooper", 22, 10, 2),
    ("street-7", "west", "fishmonger", 20, 10, 2), ("street-7", "east", "tannery", 22, 10, 2),
    ("street-8", "west", "netloft", 20, 10, 2),
]
LANE = [  # (lane, face, theme, at, dx, dz)
    ("lane-3", "north", "carpenter", 2, 16, 16), ("lane-3", "south", "apothecary-2", 2, 16, 10),
    ("lane-5", "north", "boatwright", 26, 14, 10), ("lane-5", "south", "cottages-2", 26, 14, 10),
]
for st, face, theme, dx, dz, at in MAIN:
    plot(theme, theme, f"node/{st}", face, at, 0, dx, dz)
for ln, face, theme, at, dx, dz in LANE:
    plot(theme, theme.split("-")[0], f"node/{ln}", face, at, 0, dx, dz)
plot("lighthouse", "lighthouse", "node/lane-8", "east", 0, 7, 20, 20)
# the harbour plot on the quay's east side, at the quay's floor
plot("harbour", "harbour", "node/quay", "east", 0, 2, 24, 16)

# ---------------------------------------------------------- consistency check
names = list(pos)
bad = []
for i, a in enumerate(names):
    for b in names[i + 1:]:
        joined = any({e["a"], e["b"]} == {a, b} for e in edges)
        if overlaps(pos[a], pos[b], 0 if joined else 2):
            bad.append((a, b))
for a, b in bad:
    print("OVERLAP", a, pos[a], b, pos[b], file=sys.stderr)
for n, (x, z, dx, dz, f) in pos.items():
    if x < 1 or z < 1 or x + dx > RX - 1 or z + dz > RZ - 1:
        print("OUTSIDE", n, pos[n], file=sys.stderr)
if bad:
    sys.exit(1)

# ------------------------------------------------------------------- terrain


def smooth(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def hash2(ix, iz, s):
    h = (ix * 374761393 + iz * 668265263 + s * 2147483647) & 0xFFFFFFFF
    h = (h ^ (h >> 13)) * 1274126177 & 0xFFFFFFFF
    return ((h ^ (h >> 16)) & 0xFFFF) / 65535.0


def vnoise(x, z, scale, s):
    gx, gz = x / scale, z / scale
    ix, iz = math.floor(gx), math.floor(gz)
    fx, fz = smooth(gx - ix), smooth(gz - iz)
    a = hash2(ix, iz, s); b = hash2(ix + 1, iz, s)
    c = hash2(ix, iz + 1, s); d = hash2(ix + 1, iz + 1, s)
    return (a + (b - a) * fx) * (1 - fz) + (c + (d - c) * fx) * fz


def ellipse(x, z, cx, cz, rx, rz):
    return math.hypot((x - cx) / rx, (z - cz) / rz)


def rounded_rect(x, z, x0, x1, z0, z1, r):
    """A normalised distance: < 1 inside a rectangle with corners rounded by r."""
    cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
    hx, hz = (x1 - x0) / 2, (z1 - z0) / 2
    qx, qz = abs(x - cx) - (hx - r), abs(z - cz) - (hz - r)
    out = math.hypot(max(qx, 0), max(qz, 0)) + min(max(qx, qz), 0)
    return 1 + out / r


# The island: one land mass. The mountain rises behind the town with Doune
# near its summit; its broad lower slope falls south to an irregular coast of
# coves, rock and beach, and the town lies on that slope down to the harbour.
TOWN = (60, 216, 210, 500)     # the town's ground: x0, x1, z0, z1
CX, CZ = pos["node/castle"][0] + 51, pos["node/castle"][1] + 59   # Doune's centre


def fbm(x, z, scale, octaves, salt):
    v, amp, tot = 0.0, 1.0, 0.0
    for o in range(octaves):
        v += amp * vnoise(x, z, scale / (2 ** o), salt + o)
        tot += amp
        amp *= 0.5
    return v / tot


def ridged(x, z, scale, octaves, salt):
    v, amp, tot = 0.0, 1.0, 0.0
    for o in range(octaves):
        n = 1 - abs(vnoise(x, z, scale / (2 ** o), salt + o) * 2 - 1)
        v += amp * n * n
        tot += amp
        amp *= 0.5
    return v / tot


def coast_z(x):
    """The south coast's line: coves and points; the harbour inlet at the
    quay; a deep cove east of the lighthouse so it stands on its point."""
    z = 492 + (fbm(x, 0, 38, 3, 31) - 0.5) * 60
    z -= 30 * smooth(1 - abs(x - 122) / 40)          # the harbour inlet
    z -= 66 * smooth(1 - abs(x - 214) / 26)          # the cove under the lighthouse
    z -= 48 * smooth(1 - abs(x - 38) / 30)           # a western cove
    return z


def land(x, z):
    """1 on land, 0 at sea; the south coast slopes gently to beaches."""
    wob = (fbm(x, z, 40, 3, 1) - 0.5) * 30
    inset = min(x, RX - 1 - x, z) + wob
    edge = smooth((inset - 10) / 14)                 # cliffs on the far coasts
    south = smooth((coast_z(x) - z + wob * 0.3) / 18)  # a gentle shore by the town
    return min(edge, south)


def mountain(x, z):
    """One mountain at the town's foot: its lower slope starts at the town's
    upper edge and rises along the castle road's shoulder to the summit
    plateau Doune stands on, the summit itself north-east of Doune; domain
    warped, ridged and broken into uneven ledges, so nothing is a cone."""
    wx = x + (fbm(x, z, 60, 2, 41) - 0.5) * 40
    wz = z + (fbm(x, z, 60, 2, 43) - 0.5) * 30
    top = SQ[1] - 18                                  # the town's upper edge
    # the shoulder the road climbs: rising north from the town's edge
    shoulder = 84 + 0.40 * (top - wz)               # falls away south of the town's edge too
    # the plateau round Doune, falling away on every side
    # south of Doune the ground falls evenly from its ring to the square's
    # level (about one in one, so grass and trees hold, not a cliff); north
    # it rounds off over the summit plateau
    if wz > CZ:
        d = math.hypot((wx - CX) / 150, (wz - CZ) / 105)
        t = max(0.0, min(1.0, (d - 0.56) / 0.67))
        plateau = 84 + (CASTLE_WALK - 84) * (1 - t) - 34 * max(0.0, d - 1.23)
    else:
        d = math.hypot((wx - CX) / 150, (wz - CZ) / 150)
        plateau = 50 + (CASTLE_WALK - 50) * (1 - smooth((d - 0.60) / 0.95))
    # the summit, north-east of Doune
    p = math.hypot((wx - (CX + 40)) / 80, (wz - (CZ - 55)) / 70)
    summit = CASTLE_WALK - 20 + 56 * (1 - smooth(p)) ** 1.3
    h = max(min(shoulder, CASTLE_WALK - 2), plateau, summit if p < 1 else 0)
    # fade the mountain into the island's low country east and west
    fade = smooth((x - 8) / 40) * smooth((RX - 8 - x) / 40)
    h = 50 + (h - 50) * fade
    # uneven ledges and broken rock, strongest where the ground is high
    up = smooth((h - 90) / 40)
    h += (ridged(x, z, 18, 3, 47) - 0.45) * 12 * up + (vnoise(x, z, 5, 49) - 0.5) * 3.5 * up
    hills = (12 + (fbm(x, z, 44, 3, 53) - 0.35) * 30) * smooth((300 - z) / 60) * (1 - up)
    return h + hills


def slope(x, z):
    """The mountain's lower slope under the town: the street's own fall."""
    z0, z1 = SQ[1] + 12, pos['node/quay'][1]
    y = SQF - (SQF - QUAYF) * (max(z, z0) - z0) / (z1 - z0) - 10 * smooth((z0 - z) / 80)
    return y + (fbm(x, z, 33, 2, 7) - 0.5) * 3


def base_height(x, z):
    """The land: the soft maximum of the mountain and its lower slope, cut by
    the shore so the waterline follows the coast's coves and points, falling
    to the sea floor; cliffs only on the far coasts."""
    wob = (fbm(x, z, 40, 3, 1) - 0.5) * 30
    inset = min(x, RX - 1 - x, z) + wob
    edge = smooth((inset - 10) / 14)
    h_m, h_s = mountain(x, z), max(slope(x, z), 64.5)
    k = 6.0                                          # a soft maximum: no crease
    h = k * math.log(math.exp(h_m / k) + math.exp(h_s / k))
    shore = 62.5 + 0.35 * (coast_z(x) + wob * 0.3 - z)   # a beach rising from the waterline
    sea_floor = 50 + (vnoise(x, z, 31, 4) - 0.5) * 4
    h = max(sea_floor, min(h, shore))
    return sea_floor + (h - sea_floor) * edge


H = [[base_height(x, z) for x in range(RX)] for z in range(RZ)]

# each box: its columns at floor - 1; the ground eases to the natural ground
# over a skirt. Doune's plot: inside the ring its ditch floor (walk - 4), the
# ring at its surface course (walk - 1), flat, then the summit's own rock.
rects = [(n, *pos[n]) for n in pos]
W = [[0.0] * RX for _ in range(RZ)]
T = [[0.0] * RX for _ in range(RZ)]
for n, x0, z0, dx, dz, f in rects:
    castle = n == "node/castle"
    road = n.startswith("node/road") or n == "node/gate-road"
    skirt = 28 if castle else (12 if road else (3 if n == "node/quay" else 12))
    for z in range(max(0, z0 - 1 - skirt), min(RZ, z0 + dz + 1 + skirt)):
        for x in range(max(0, x0 - 1 - skirt), min(RX, x0 + dx + 1 + skirt)):
            ddx = max(x0 - x, 0, x - (x0 + dx - 1))
            ddz = max(z0 - z, 0, z - (z0 + dz - 1))
            d = math.hypot(ddx, ddz)
            if castle:
                if d == 0:
                    target, w = f - 4, 1.0
                elif max(ddx, ddz) <= 1:
                    target, w = f - 1, 1.0
                else:
                    target, w = f - 1, smooth(1 - (d - 1) / skirt)
            else:
                # the footprint and its ring lie at the floor course, so the
                # ground meets the next place level across the seam
                target = f - 1
                w = 1.0 if max(ddx, ddz) <= 1 else smooth(1 - (d - 1) / skirt)
            if n == "node/harbour" and max(ddx, ddz) <= 1:
                continue  # the harbour keeps the shore and the sea floor under it
            if w > W[z][x] + 1e-9 or (abs(w - W[z][x]) < 1e-9 and target > T[z][x]):
                W[z][x] = w
                T[z][x] = target
for z in range(RZ):
    for x in range(RX):
        w = W[z][x]
        if w > 0:
            H[z][x] = H[z][x] * (1 - w) + T[z][x] * w

# Behind the cathedral (north) and past its apse (east) the mountain's lower
# terrace stands some thirty above the cathedral's floor. The ground falls from
# that terrace to the cathedral's ring as a hillside, never a bank: there the
# ground is capped by a slope rising from the ring course, one in one at its
# foot and steepening gently (BACK_BEND) until it meets the natural ground,
# which then runs on up to Doune untouched. The cap only lowers ground, and
# never inside another box's footprint or ring. West (the square and the
# castle road) and south (the town) keep their own shaping.
BACK_RISE, BACK_BEND, BACK_REACH, BACK_WEST = 1.0, 0.02, 44, 12
_bx, _bz, _bdx, _bdz, _bf = pos["node/cathedral"]
for z in range(max(0, _bz - 1 - BACK_REACH), min(RZ, _bz + _bdz + 1 + BACK_REACH)):
    for x in range(_bx - BACK_WEST, min(RX, _bx + _bdx + 1 + BACK_REACH)):
        ddw = max(0, (_bx - 1) - x)               # past the west ring: eased out
        ddx = max(0, x - (_bx + _bdx))            # past the east ring
        ddz = max(0, (_bz - 1) - z, z - (_bz + _bdz))
        if ddx == 0 and ddz == 0 or W[z][x] >= 1.0:
            continue
        if z > _bz + _bdz and ddx == 0:
            continue                               # south of the cathedral: the town's
        d = math.hypot(ddx, ddz)
        cap = (_bf - 1) + BACK_RISE * d + BACK_BEND * d * d \
            + (vnoise(x, z, 6, 61) - 0.5) * 2.0 + 1.5 * ddw
        if H[z][x] > cap:
            H[z][x] = cap

# No pit a body cannot climb out of: a priority flood from the sea and the
# region's rim raises every column to at least one under the column it is
# reached from, so from anywhere a walk of steps no higher than one leads to
# the shore. Cliffs stay: only hollows are filled.
import heapq
Q = [[int(round(H[z][x])) for x in range(RX)] for z in range(RZ)]
seen = [[False] * RX for _ in range(RZ)]
heap = []
for z in range(RZ):
    for x in range(RX):
        if Q[z][x] < SEA + 1 or x in (0, RX - 1) or z in (0, RZ - 1):
            seen[z][x] = True
            heapq.heappush(heap, (Q[z][x], x, z))
while heap:
    h, x, z = heapq.heappop(heap)
    for nx, nz in ((x + 1, z), (x - 1, z), (x, z + 1), (x, z - 1)):
        if 0 <= nx < RX and 0 <= nz < RZ and not seen[nz][nx]:
            seen[nz][nx] = True
            if Q[nz][nx] < h - 1:
                Q[nz][nx] = h - 1
            heapq.heappush(heap, (Q[nz][nx], nx, nz))
H = [[float(Q[z][x]) for x in range(RX)] for z in range(RZ)]

pix = bytearray()
for z in range(RZ):
    pix.append(0)
    for x in range(RX):
        v = round((H[z][x] - BASE_Y) * 255 / RANGE)
        # y = BASE_Y + v * RANGE // 255 must land on the intended course
        want = int(round(H[z][x]))
        v = max(0, min(255, v))
        while v < 255 and BASE_Y + v * RANGE // 255 < want:
            v += 1
        while v > 0 and BASE_Y + v * RANGE // 255 > want:
            v -= 1
        pix.append(v)


def png(path, w, h, raw):
    def chunk(t, d):
        c = struct.pack(">I", len(d)) + t + d
        return c + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
    with open(path, "wb") as fh:
        fh.write(b"\x89PNG\r\n\x1a\n")
        fh.write(chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 0, 0, 0, 0)))
        fh.write(chunk(b"IDAT", zlib.compress(bytes(raw), 9)))
        fh.write(chunk(b"IEND", b""))


os.makedirs(os.path.join(ROOT, "terrain"), exist_ok=True)
png(os.path.join(ROOT, "terrain", "island.png"), RX, RZ, pix)

# ----------------------------------------------------------------- documents


TOWN_AREA = {"min": [TOWN[0], TOWN[2]], "max": [TOWN[1], TOWN[3]]}
BRICK_AREA = {"min": [TOWN[0], SQ[1] + 24], "max": [TOWN[1], TOWN[3]]}   # below the square: the mountain never takes a brick
_cx, _cz, _cdx, _cdz, _ = pos["node/castle"]
CASTLE_AREA = {"min": [_cx - 1, _cz - 1], "max": [_cx + _cdx, _cz + _cdz]}
P = lambda scale, mn, salt: {"scale": scale, "min": mn, "salt": salt}
STRATA = [
    # the sea floor and the shore
    {"when": {"y_max": 56}, "surface": "minecraft:gravel", "below": "minecraft:stone"},
    {"when": {"y_max": 63}, "surface": "minecraft:sand", "below": "minecraft:sandstone"},
    # Doune's plot and its ring: Doune's own turf, which its plants stand on
    {"when": {"area": CASTLE_AREA}, "surface": "minecraft:grass_block", "below": "minecraft:dirt"},
    # the town: a step of two or more is a retaining wall a builder laid
    {"when": {"area": BRICK_AREA, "steep": 3, "patch": P(9, 600, 11)},
     "surface": "minecraft:mossy_stone_bricks", "below": "minecraft:mossy_stone_bricks"},
    {"when": {"area": BRICK_AREA, "steep": 3},
     "surface": "minecraft:stone_bricks", "below": "minecraft:stone_bricks"},
    {"when": {"area": TOWN_AREA, "patch": P(7, 780, 12)},
     "surface": "minecraft:coarse_dirt", "below": "minecraft:dirt"},
    {"when": {"area": TOWN_AREA}, "surface": "minecraft:grass_block", "below": "minecraft:dirt"},
    # the wild: rock as it weathers, never one smooth face. A real cliff only
    # where it is very steep; elsewhere stone, andesite, tuff and moss broken
    # by grass in the cracks, and scree high up.
    {"when": {"steep": 5, "patch": P(4, 520, 21)}, "surface": "minecraft:andesite", "below": "minecraft:andesite"},
    {"when": {"steep": 5, "patch": P(5, 560, 30)}, "surface": "minecraft:tuff", "below": "minecraft:stone"},
    {"when": {"steep": 5}, "surface": "minecraft:stone", "below": "minecraft:stone"},
    {"when": {"steep": 3, "patch": P(3, 620, 31)}, "surface": "minecraft:moss_block", "below": "minecraft:stone"},
    {"when": {"steep": 3, "patch": P(4, 540, 32)}, "surface": "minecraft:grass_block", "below": "minecraft:dirt"},
    {"when": {"steep": 3, "patch": P(3, 500, 33)}, "surface": "minecraft:andesite", "below": "minecraft:stone"},
    {"when": {"steep": 3, "patch": P(4, 520, 34)}, "surface": "minecraft:tuff", "below": "minecraft:stone"},
    {"when": {"steep": 3}, "surface": "minecraft:stone", "below": "minecraft:stone"},
    {"when": {"y_min": 178, "patch": P(5, 520, 35)}, "surface": "minecraft:gravel", "below": "minecraft:stone"},
    {"when": {"y_min": 178, "patch": P(4, 600, 36)}, "surface": "minecraft:moss_block", "below": "minecraft:stone"},
    {"when": {"y_min": 178}, "surface": "minecraft:stone", "below": "minecraft:stone"},
    # outcrops breaking the slopes: small patches, mixed
    {"when": {"y_min": 100, "patch": P(7, 780, 28)}, "surface": "minecraft:stone", "below": "minecraft:stone"},
    {"when": {"y_min": 95, "patch": P(6, 800, 29)}, "surface": "minecraft:andesite", "below": "minecraft:stone"},
    {"when": {"y_min": 110, "patch": P(5, 820, 37)}, "surface": "minecraft:mossy_cobblestone", "below": "minecraft:stone"},
    {"when": {"y_min": 92, "y_max": 176, "patch": P(30, 400, 23)},
     "surface": "minecraft:podzol", "below": "minecraft:dirt",
     "trees": {"per_mille": 70, "log": "minecraft:spruce_log",
               "leaves": "minecraft:spruce_leaves[persistent=true]", "height": [6, 9]}},
    {"when": {"y_min": 66, "y_max": 104, "patch": P(26, 470, 24)},
     "surface": "minecraft:grass_block", "below": "minecraft:dirt",
     "trees": {"per_mille": 55, "log": "minecraft:oak_log",
               "leaves": "minecraft:oak_leaves[persistent=true]", "height": [5, 7]}},
    {"when": {"y_min": 66, "patch": P(22, 620, 25)},
     "surface": "minecraft:grass_block", "below": "minecraft:dirt",
     "trees": {"per_mille": 30, "log": "minecraft:birch_log",
               "leaves": "minecraft:birch_leaves[persistent=true]", "height": [5, 7]}},
    {"when": {"patch": P(6, 800, 26)}, "surface": "minecraft:coarse_dirt", "below": "minecraft:dirt"},
]


def write(name, stage, content):
    doc = {"campaign_id": CAMPAIGN, "content": content, "dsl_version": DSL,
           "stage": stage}
    with open(os.path.join(ROOT, name), "w") as fh:
        json.dump(doc, fh, indent=2, sort_keys=True, ensure_ascii=False)
        fh.write("\n")


main_path = ["node/square"]
for k in range(1, NFL + 1):
    main_path.append(f"node/flight-{k}")
    if k < NFL:
        main_path.append(f"node/street-{k}")
main_path.append("node/quay")

write("world.json", "world", {
    "areas": [],
    "boundary": {"margin": 8},
    "test_level": True,
    "horizon": {"attributes": {"audio/background_music": {}}, "base": "ocean"},
    "premise": "The party arrives on the square at the foot of the mountain and walks the main street down through the town to the harbour.",
    "seed": 20261028,
    "target_minutes": 20,
    "theme": "A harbour town on the slope below a castle mountain: one main street from the cathedral square down to the quays, side streets off it, a lighthouse on the headland.",
    "time": "noon",
    "title": "The Town at the Foot of the Mountain",
    "weather": "clear",
})
write("layout-graph.json", "layout-graph", {
    "beats": [{"node": "node/quay", "objective": "obj/reach-the-quay",
               "quest": "quest/down-to-the-harbour"}],
    "critical_path": main_path,
    "edges": edges,
    "entry": "node/square",
    "goal": "node/quay",
    "nodes": nodes,
})
write("site-plan.json", "site-plan", {
    "boxes": boxes,
    "datums": [],
    "fill": {"below": "minecraft:dirt", "kind": "open",
             "surface": "minecraft:grass_block", "strata": STRATA,
             "terrain": {"base_y": BASE_Y, "heightmap": "terrain/island.png",
                         "kind": "heightmap", "range": RANGE}},
    "identities": [
        {"cmp": "eq", "fact": "fact/region-span", "measure": {"axis": "x", "of": "region-extent"}},
        {"cmp": "eq", "fact": "fact/region-depth", "measure": {"axis": "z", "of": "region-extent"}},
    ],
    "region": {"extent": [RX, RYN, RZ], "min": [0, RY0, 0]},
    "seams": seams,
    "views": [],
    "volumes": [],
})
write("geometry-brief.json", "geometry-brief", {"facts": [
    {"id": "fact/region-span", "note": "The region east to west.", "unit": "blocks", "value": float(RX)},
    {"id": "fact/region-depth", "note": "The region north to south.", "unit": "blocks", "value": float(RZ)},
]})
write("quest-plan.json", "quest-plan", {
    "finale": "quest/down-to-the-harbour",
    "quests": [{"act": 1, "area": "area/site", "depends_on": [],
                "goal": "Walk the town from the square down to the harbour.",
                "id": "quest/down-to-the-harbour", "mandatory": True, "npcs": []}],
})
write("quests.json", "quests", {"quests": [{
    "happening": {"text": "You stand on the square at the foot of the mountain, the cathedral on one side and the inn on the other.", "verb": "arrives"},
    "id": "quest/down-to-the-harbour",
    "objectives": [{
        "anchor": "anchor/node-quay",
        "happening": {"text": "You reach the quay at the foot of the street.", "verb": "arrives"},
        "hint": "Down the main street from the square, past the side streets, to the stone quay at the harbour.",
        "id": "obj/reach-the-quay", "radius": 1, "title": "Go down to the harbour",
        "type": "reach-anchor"}],
    "on_complete": [{"happening": {"text": "The town is walked, square to harbour.", "verb": "departs"}, "type": "campaign-complete"}],
    "trigger": {"type": "campaign-start"},
}]})

print(f"boxes {len(boxes)}  seams {len(seams)}  plots {sum(1 for n in nodes if 'holds' in n)}")
for n in ("node/square", "node/castle", "node/quay", "node/cathedral", "node/lighthouse"):
    print(n, pos[n])
if os.environ.get("POS_OUT"):
    with open(os.environ["POS_OUT"], "w") as fh:
        json.dump(pos, fh)
