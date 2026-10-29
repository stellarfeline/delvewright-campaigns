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
BASE_Y, RANGE = 48, 127    # heightmap: y = 48 + v * 127 // 255
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
SQ = (108, 270)
box("node/square", (30, 24), 92, OPEN(8), "the square",
    "The square at the top of the town, at the mountain's foot: the cathedral's "
    "west front on its east side, the inn on its west, the castle road leaving "
    "north up the mountain and the main street leaving south down to the sea. "
    "Cobbled, with a well at its middle and benches under two trees.",
    pin=SQ)

# ------------------------------------------------------- the main street
STREET_W, SEG_L, FLIGHT_L = 7, 20, 6
segs = []
prev, prev_face_at = "node/square", 11
floor = 92
for k in range(1, 8):
    fl = f"node/flight-{k}"
    floor -= 4
    box(fl, (STREET_W, FLIGHT_L), floor, OPEN(10), "a flight of the main street",
        f"Flight {k} of the main street: seven wide, four steps down, stone-brick "
        "stairs between low kerb walls with a lantern post at each top corner.",
        way={"axis": "z", "clear": 5})
    seam(prev, fl, "south", prev_face_at if prev == "node/square" else 0, 0,
         "stair", f"flight {k}: four down, the full width")
    if k == 7:
        break
    sg = f"node/street-{k}"
    box(sg, (STREET_W, SEG_L), floor, OPEN(8), "a terrace of the main street",
        f"Terrace {k} of the main street, walk plane {floor}: cobbles with a "
        "kerb of stone bricks, the plots' fronts on both sides.",
        way={"axis": "z", "clear": 5})
    seam(fl, sg, "south", 0, 0, "contact", "the street runs on at grade")
    segs.append(sg)
    prev = sg

# the quay and the harbour
box("node/quay", (60, 10), 64, OPEN(8), "the quay",
    "The quay at the foot of the street: a long stone wharf at walk plane 64, "
    "bollards, stacked crates and nets, the harbour basin beyond.",
    way={"axis": "x", "clear": 8})
seam("node/flight-7", "node/quay", "south", 0, 27, "contact",
     "the last flight lands on the quay")
box("node/harbour", (60, 28), 64, OPEN(12), "the harbour",
    "The harbour basin: two stone quays reaching into the water, a timber "
    "jetty, and three fishing boats moored as fixed builds.",
    holds=[
        {"id": "part/east-mole", "kind": "ground", "cells": 160,
         "use": "a stone mole reaching south into the sea, bollards along it"},
        {"id": "part/jetty", "kind": "ground", "cells": 90,
         "use": "a timber jetty on piles between the moles"},
        {"id": "part/boats", "kind": "structure", "cells": 120, "height": 6,
         "reached": False,
         "use": "three fishing boats moored along the jetty, masts and furled sails"},
        {"id": "part/basin", "kind": "ground", "cells": 900, "reached": False,
         "use": "the open water of the basin between the moles"},
    ])
seam("node/quay", "node/harbour", "south", 0, 0, "contact",
     "the quay's edge steps onto the moles and the jetty")

# ------------------------------------------------------------- the cathedral
box("node/cathedral", (56, 38), 92, OPEN(46), "the cathedral",
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
box("node/inn", (28, 24), 92, OPEN(16), "the inn",
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
# Doune's gate faces north, so the road climbs north along the castle hill's
# west flank, turns east along its north side, and comes south onto the
# castle's own approach road (a contact on the castle's north face at 74).
ROAD_W, RAMP_L, SEG_LEN = 5, 10, 17
CASTLE_WALK = 128            # Doune's grade walk, the castle box's floor
prev = "node/square"
floor = 92
for k in range(1, 10):
    ramp = f"node/road-{k}"
    box(ramp, (ROAD_W, RAMP_L), floor, OPEN(10), "the castle road",
        f"Ramp {k} of the castle road up the mountain: a cobbled stair-road, one "
        "step every two cells, between low parapets of mossy stone.",
        way={"axis": "z", "clear": 4})
    if prev == "node/square":
        seam(prev, ramp, "north", 13, 0, "contact",
             "the castle road leaves the square northward")
    else:
        seam(prev, ramp, "north", 0, 0, "contact", "the road runs on")
    floor += 4
    if k < 9:
        top, (dx, dz) = f"node/road-run-{k}", (ROAD_W, SEG_LEN)
        box(top, (dx, dz), floor, OPEN(8), "a level run of the castle road",
            "A level run of the castle road along the hillside, a rough stone "
            "parapet on the downhill side.", way={"axis": "z", "clear": 4})
    else:
        top, (dx, dz) = "node/road-top", (90, ROAD_W)
        box(top, (dx, dz), floor, OPEN(8), "the castle road's last stretch",
            "The road's last stretch, level along the castle hill's north side "
            "to the head of Doune's approach.", way={"axis": "x", "clear": 4})
    rx, rz = pos[ramp][0], pos[ramp][1]
    pos[top] = (rx, rz - dz - 1, dx, dz, floor)
    eid = "edge/" + top.split("/")[1] + "-to-" + ramp.split("/")[1]
    seams.append({"edge": eid, "face": "south", "at": 0, "meets": 0,
                  "opening": {"width": ROAD_W, "height": 4},
                  "stair_in": ramp, "form": "the ramp climbs to the level run"})
    edges.append({"a": top, "b": ramp, "class": "stair", "id": eid})
    prev = top
assert floor == CASTLE_WALK, floor

box("node/gate-road", (5, 8), CASTLE_WALK, OPEN(6), "the road onto Doune's approach",
    "The last stretch of the road from the town, arriving on the hilltop at the "
    "start of Doune's own approach road, five wide.", way={"axis": "z", "clear": 5})
seam("node/road-top", "node/gate-road", "south", 85, 0, "contact",
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
SIDE = {("node/street-2", "west"): 46, ("node/street-4", "east"): 44,
        ("node/street-6", "east"): 48}
for (sg, face), L in SIDE.items():
    k = sg.split("-")[1]
    sname = f"node/lane-{k}"
    _, f = ext(sg)
    box(sname, (L, 5), f, OPEN(8), "a side street",
        f"A side street off terrace {k}, cobbled, five wide, plots along it.",
        way={"axis": "x", "clear": 4})
    seam(sg, sname, face, 8, 0, "contact", "the side street leaves the terrace")

# main-street plots: (street, face, theme, dx, dz, meets)
MAIN = [  # (street, face, theme, dx, dz, at): a plot stays inside its terrace
    ("street-1", "west", "bakery", 22, 16, 2), ("street-1", "east", "apothecary", 16, 14, 4),
    ("street-2", "east", "merchant", 26, 16, 2),
    ("street-3", "west", "townhall", 24, 16, 2), ("street-3", "east", "weaver", 20, 15, 3),
    ("street-4", "west", "smithy", 24, 16, 2),
    ("street-5", "west", "chandler", 20, 14, 4), ("street-5", "east", "tavern", 24, 16, 2),
    ("street-6", "west", "fishmonger", 20, 14, 2),
]
# side-street plots: (lane, face, theme, at, dx, dz)
LANE = [
    ("lane-2", "north", "cottages", 22, 16, 12), ("lane-2", "south", "carpenter", 2, 18, 13),
    ("lane-4", "north", "cooper", 28, 16, 12), ("lane-4", "south", "tannery", 24, 20, 14),
    ("lane-6", "north", "netloft", 26, 16, 12), ("lane-6", "south", "boatwright", 22, 20, 12),
]
for st, face, theme, dx, dz, at in MAIN:
    plot(f"{theme}", theme, f"node/{st}", face, at, 0, dx, dz)
for ln, face, theme, at, dx, dz in LANE:
    plot(f"{theme}", theme, f"node/{ln}", face, at, 0, dx, dz)
# the lighthouse at the end of lane-6
plot("lighthouse", "lighthouse", "node/lane-6", "east", 0, 7, 20, 20)

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


# The island: a broad mainland block (the mountain country, far side
# hidden behind its ridges) and, running south from it, the town's
# promontory with the lighthouse headland on its east shoulder.
TOWN = (60, 216, 248, 500)     # the town's own ground: x0, x1, z0, z1


def land(x, z):
    """1 inside the island, 0 in the sea; a narrow edge makes the cliffs."""
    wob = (vnoise(x, z, 41, 1) - 0.5) * 0.22 + (vnoise(x, z, 13, 5) - 0.5) * 0.06
    main = (abs((x - 160) / 152) ** 4 + abs((z - 150) / 146) ** 4) ** 0.25
    taper = 1 + 0.35 * smooth((z - 330) / 150)          # the promontory narrows to its tip
    prom = rounded_rect(x, z, 136 - 70 / taper, 136 + 70 / taper, 250, 484, 36)
    head = ellipse(x, z, 194, 462, 24, 26)
    e = min(main, prom, head)
    return smooth((1.0 - (e + wob)) / 0.05)


def wild_height(x, z):
    """The mountain country: rolling ground, the castle hill, two peaks."""
    rolling = 74 + (vnoise(x, z, 53, 2) - 0.5) * 34 + (vnoise(x, z, 19, 3) - 0.5) * 10
    # the castle hill: a summit just under Doune's grade, falling away
    cx, cz = 183, 95
    d = math.hypot((x - cx) / 1.0, (z - cz) / 1.1)
    hill = 126 - 54 * smooth((d - 60) / 85) + (vnoise(x, z, 15, 8) - 0.5) * 6 * smooth((d - 64) / 20)
    # the main peak, north-east, and a lesser one north-west, with ridged noise
    ridge = 1 - abs(vnoise(x, z, 29, 6) - 0.5) * 2
    peak = 0.0
    for px, pz, r, hgt in ((270, 70, 85, 172), (48, 62, 70, 146), (300, 170, 60, 118)):
        dd = math.hypot(x - px, z - pz) / r
        peak = max(peak, 64 + (hgt - 64) * (1 - smooth(dd)) ** 1.6)
    peak_h = 64 + (peak - 64) * (0.8 + 0.2 * ridge)
    return max(rolling, hill, peak_h)


def town_height(x, z):
    """The promontory's slope: 92 at the mountain's foot, 63 at the shore."""
    return 63 + 29 * smooth((482 - z) / 212) + (vnoise(x, z, 19, 7) - 0.5) * 3


def base_height(x, z):
    m = land(x, z)
    wild = wild_height(x, z)
    town = town_height(x, z)
    # the town's ground takes over south of the mountain's foot
    t = smooth((z - 262) / 40) * smooth((x - 50) / 20) * smooth((226 - x) / 20)
    h = wild * (1 - t) + town * t
    sea_floor = 50 + (vnoise(x, z, 31, 4) - 0.5) * 4
    return sea_floor + (h - sea_floor) * m


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
    skirt = 16 if castle else (7 if road else 12)
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
                target = f - 1
                w = 1.0 if d == 0 else smooth(1 - d / skirt)
            if n == "node/harbour" and d == 0:
                continue  # the basin keeps the sea floor
            if w > W[z][x] + 1e-9 or (abs(w - W[z][x]) < 1e-9 and target > T[z][x]):
                W[z][x] = w
                T[z][x] = target
for z in range(RZ):
    for x in range(RX):
        w = W[z][x]
        if w > 0:
            H[z][x] = H[z][x] * (1 - w) + T[z][x] * w

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
P = lambda scale, mn, salt: {"scale": scale, "min": mn, "salt": salt}
STRATA = [
    # the sea floor and the shore
    {"when": {"y_max": 56}, "surface": "minecraft:gravel", "below": "minecraft:stone"},
    {"when": {"y_max": 63}, "surface": "minecraft:sand", "below": "minecraft:sandstone"},
    # the town: a step of two or more is a retaining wall a builder laid
    {"when": {"area": TOWN_AREA, "steep": 2, "patch": P(9, 600, 11)},
     "surface": "minecraft:mossy_stone_bricks", "below": "minecraft:mossy_stone_bricks"},
    {"when": {"area": TOWN_AREA, "steep": 2},
     "surface": "minecraft:stone_bricks", "below": "minecraft:stone_bricks"},
    {"when": {"area": TOWN_AREA, "patch": P(7, 780, 12)},
     "surface": "minecraft:coarse_dirt", "below": "minecraft:dirt"},
    {"when": {"area": TOWN_AREA}, "surface": "minecraft:grass_block", "below": "minecraft:dirt"},
    # the wild: rock where it is steep or high, scree, forest, heath
    {"when": {"steep": 3, "patch": P(11, 550, 21)},
     "surface": "minecraft:andesite", "below": "minecraft:andesite"},
    {"when": {"steep": 3}, "surface": "minecraft:stone", "below": "minecraft:stone"},
    {"when": {"y_min": 150}, "surface": "minecraft:stone", "below": "minecraft:stone"},
    {"when": {"y_min": 136, "patch": P(8, 500, 22)},
     "surface": "minecraft:gravel", "below": "minecraft:stone"},
    {"when": {"y_min": 136}, "surface": "minecraft:stone", "below": "minecraft:stone"},
    {"when": {"y_min": 96, "y_max": 135, "patch": P(30, 430, 23)},
     "surface": "minecraft:podzol", "below": "minecraft:dirt",
     "trees": {"per_mille": 70, "log": "minecraft:spruce_log",
               "leaves": "minecraft:spruce_leaves[persistent=true]", "height": [6, 9]}},
    {"when": {"y_min": 66, "y_max": 104, "patch": P(26, 470, 24)},
     "surface": "minecraft:grass_block", "below": "minecraft:dirt",
     "trees": {"per_mille": 55, "log": "minecraft:oak_log",
               "leaves": "minecraft:oak_leaves[persistent=true]", "height": [4, 6]}},
    {"when": {"y_min": 66, "patch": P(22, 620, 25)},
     "surface": "minecraft:grass_block", "below": "minecraft:dirt",
     "trees": {"per_mille": 30, "log": "minecraft:birch_log",
               "leaves": "minecraft:birch_leaves[persistent=true]", "height": [5, 7]}},
    {"when": {"patch": P(6, 800, 26)}, "surface": "minecraft:coarse_dirt", "below": "minecraft:dirt"},
    {"when": {"steep": 2, "patch": P(5, 650, 27)}, "surface": "minecraft:stone", "below": "minecraft:dirt"},
]


def write(name, stage, content):
    doc = {"campaign_id": CAMPAIGN, "content": content, "dsl_version": DSL,
           "stage": stage}
    with open(os.path.join(ROOT, name), "w") as fh:
        json.dump(doc, fh, indent=2, sort_keys=True, ensure_ascii=False)
        fh.write("\n")


main_path = ["node/square"]
for k in range(1, 8):
    main_path.append(f"node/flight-{k}")
    if k < 7:
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
for n in ("node/square", "node/castle", "node/quay", "node/harbour", "node/cathedral", "node/lighthouse"):
    print(n, pos[n])
