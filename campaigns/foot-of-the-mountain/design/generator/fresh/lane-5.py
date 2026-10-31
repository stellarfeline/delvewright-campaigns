#!/usr/bin/env python3
"""node/lane-5: a cobbled side street off stretch 5, the boatwright's shed and the cottages' gardens at its far end.

Paved by the starter's `lane` helper: cobbles with a kennel down the middle,
setts beside the outer columns, the verge (the column outside the clear way,
on the south) carrying lamps, a bench and a cart; flower beds and a hedge
fill the verge where the helper leaves it bare, kept off the cottages' and
the boatwright's fronts.

    "$DELVEWRIGHT_PYTHON" lane-5.py --allocation <allocation.json> \
        --out <campaign>/programs/lane-5.json --delvec <delvec>
"""

import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
from starter import Model, run, lane, flower_bed, seam_cols, leaves, hsh  # noqa: E402

FLOWERS = ["minecraft:poppy", "minecraft:cornflower", "minecraft:oxeye_daisy", "minecraft:allium"]


def build(place):
    m = Model(place)
    p = m.palette
    # the street's own materials: cobbles set in sand, a mossy kennel, stone setts, a worn verge
    p["paving"] = [{"block": "minecraft:cobblestone", "weight": 3}, {"block": "minecraft:mossy_cobblestone", "weight": 1}]
    p["kennel"] = "minecraft:mossy_stone_bricks"
    p["kerb"] = [{"block": "minecraft:cobblestone", "weight": 2}, {"block": "minecraft:andesite", "weight": 1}]
    p["verge"] = [{"block": "minecraft:coarse_dirt", "weight": 2}, {"block": "minecraft:gravel", "weight": 1},
                  {"block": "minecraft:cobblestone", "weight": 1}]

    lane(m, place, edge="high", every=5, things=("bench", "cart"))

    # `pave_way` lays its outer column on both edges as verge; the north one is in
    # the clear way the plan hands, so it is cobbled like the rest of the way
    (x0, _, z0), (x1, _, z1) = place.space
    c0, c1 = place.way["cols"]                    # the clear way, as the plan hands it
    for x in range(x0, x1 + 1):
        m.set(x, place.datum.value - 1, c0, "paving")

    # verge life where the helper left the verge bare: beds of flowers and a hedge
    w = place.datum.value
    vz = c1 + 1                                   # the verge column, outside the clear way
    keep = seam_cols(place, pad=1)
    beds = []
    for x in range(x0 + 2, x1 - 1):
        if (x, vz) in keep or m.get(x, w, vz) is not None or m.get(x - 1, w, vz) is not None:
            continue
        r = hsh(54, x, 9)
        if r < 0.35:
            beds.append((x, vz))
        elif r < 0.5:
            m.set(x, w - 1, vz, "minecraft:grass_block[snowy=false]")
            m.set(x, w, vz, leaves("oak"))
    flower_bed(m, beds, FLOWERS)
    m.finish()
    return m


raise SystemExit(run(build))
