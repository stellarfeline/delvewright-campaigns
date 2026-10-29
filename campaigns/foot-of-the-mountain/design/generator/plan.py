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
    eid = "edge/" + a.split("/")[1] + "--" + b.split("/")[1]
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
    if face == "south":
        p = (ax + at - meets, az + adz)
    elif face == "north":
        p = (ax + at - meets, az - bdz)
    elif face == "east":
        p = (ax + adx, az + at - meets)
    else:
        p = (ax - bdx, az + at - meets)
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
ROAD_W, RAMP_L, LAND_L = 5, 8, 3
prev = "node/square"
floor = 92
for k in range(1, 9):
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
    top = f"node/castle" if k == 8 else f"node/landing-{k}"
    if k < 8:
        box(top, (ROAD_W, LAND_L), floor, OPEN(8), "a landing on the castle road",
            "A level landing on the castle road.",
            way={"axis": "z", "clear": 4})
        # the landing is above the ramp: landing (a) south face -> ramp (b)
        (dx, dz), _ = ext(top)
        rx, rz = pos[ramp][0], pos[ramp][1]
        pos[top] = (rx, rz - dz, dx, dz, floor)
        eid = "edge/" + top.split("/")[1] + "--" + ramp.split("/")[1]
        seams.append({"edge": eid, "face": "south", "at": 0, "meets": 0,
                      "opening": {"width": ROAD_W, "height": 4},
                      "stair_in": ramp, "form": "the ramp climbs to the landing"})
        edges.append({"a": top, "b": ramp, "class": "stair", "id": eid})
        prev = top

box("node/castle", (104, 114), 124, OPEN(52), "the castle plot",
    "PLACEHOLDER for Doune Castle, which another round drops in as one plot: "
    "the levelled summit ground and the road's arrival at the gate. Marked as a "
    "placeholder by a ring of white banners on posts; no castle is built here.",
    holds=[
        {"id": "part/castle-ground", "kind": "ground", "cells": 9000,
         "use": "PLACEHOLDER: the levelled summit where Doune stands, enclosure and approach"},
    ])
(cdx, cdz), _ = ext("node/castle")
rx, rz = pos["node/road-8"][0], pos["node/road-8"][1]
pos["node/castle"] = (rx - 50, rz - cdz, cdx, cdz, 124)
seams.append({"edge": "edge/castle--road-8", "face": "south", "at": 50,
              "meets": 0, "opening": {"width": ROAD_W, "height": 4},
              "stair_in": "node/road-8",
              "form": "the last ramp climbs to the gate ground"})
edges.append({"a": "node/castle", "b": "node/road-8", "class": "stair",
              "id": "edge/castle--road-8"})

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
MAIN = [
    ("street-1", "west", "bakery", 22, 18, 2), ("street-1", "east", "apothecary", 18, 20, -1),
    ("street-2", "east", "merchant", 26, 22, 0),
    ("street-3", "west", "townhall", 24, 20, -1), ("street-3", "east", "weaver", 20, 18, -2),
    ("street-4", "west", "smithy", 24, 20, 0),
    ("street-5", "west", "chandler", 22, 18, 2), ("street-5", "east", "tavern", 24, 20, -1),
    ("street-6", "west", "fishmonger", 20, 16, 0),
]
# side-street plots: (lane, face, theme, at, dx, dz)
LANE = [
    ("lane-2", "north", "cottages", 30, 16, 14), ("lane-2", "south", "carpenter", 2, 18, 13),
    ("lane-4", "north", "cooper", 28, 16, 14), ("lane-4", "south", "tannery", 24, 20, 16),
    ("lane-6", "north", "netloft", 26, 16, 14), ("lane-6", "south", "boatwright", 22, 20, 12),
]
for st, face, theme, dx, dz, meets in MAIN:
    plot(f"{theme}", theme, f"node/{st}", face, 0, meets, dx, dz)
for ln, face, theme, at, dx, dz in LANE:
    plot(f"{theme}", theme, f"node/{ln}", face, at, 0, dx, dz)
# the lighthouse at the end of lane-6
plot("lighthouse", "lighthouse", "node/lane-6", "east", 0, 7, 20, 20)

# ---------------------------------------------------------- consistency check
names = list(pos)
bad = []
for i, a in enumerate(names):
    for b in names[i + 1:]:
        if overlaps(pos[a], pos[b]):
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


def land(x, z):
    """1 inside the island, falling to 0 at the coast (a soft mask)."""
    wob = (vnoise(x, z, 37, 1) - 0.5) * 0.18
    e = min(ellipse(x, z, 178, 215, 150, 205),
            ellipse(x, z, 122, 372, 100, 110),
            ellipse(x, z, 196, 452, 22, 24))
    return smooth((1.0 - (e + wob)) / 0.10)


def base_height(x, z):
    m = land(x, z)
    # the town slope: 92 at the mountain's foot, 63 at the shore
    slope = 63 + 29 * smooth((470 - z) / 200)
    # the mountain: a massif north and east of the castle
    peak = 0.0
    for cx, cz, r, hgt in ((230, 112, 85, 112), (150, 118, 70, 74),
                           (270, 200, 70, 60), (110, 60, 60, 52)):
        d = math.hypot(x - cx, z - cz) / r
        peak = max(peak, hgt * smooth(1 - d))
    rough = (vnoise(x, z, 23, 2) - 0.5) * 6 + (vnoise(x, z, 9, 3) - 0.5) * 2
    h = max(slope, 63 + peak) + rough * (0.4 + 0.6 * smooth((peak - 4) / 30))
    sea_floor = 50 + (vnoise(x, z, 31, 4) - 0.5) * 4
    return sea_floor + (h - sea_floor) * m


H = [[base_height(x, z) for x in range(RX)] for z in range(RZ)]

# each box: its columns at floor - 1; the ground eases to the natural ground
# over a skirt whose width grows with the height to meet
rects = [(n, *pos[n]) for n in pos]
W = [[0.0] * RX for _ in range(RZ)]
T = [[0.0] * RX for _ in range(RZ)]
for n, x0, z0, dx, dz, f in rects:
    target = f - 1
    skirt = 6 if not n.startswith("node/castle") else 14
    for z in range(max(0, z0 - skirt), min(RZ, z0 + dz + skirt)):
        for x in range(max(0, x0 - skirt), min(RX, x0 + dx + skirt)):
            ddx = max(x0 - x, 0, x - (x0 + dx - 1))
            ddz = max(z0 - z, 0, z - (z0 + dz - 1))
            d = math.hypot(ddx, ddz)
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
             "surface": "minecraft:grass_block",
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
