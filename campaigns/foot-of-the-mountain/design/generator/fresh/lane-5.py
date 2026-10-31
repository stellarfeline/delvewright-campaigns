#!/usr/bin/env python3
"""node/lane-5: a cobbled side street off stretch 5, the boatwright's shed and the cottages' gardens at its far end.

Paved by the starter's `lane` helper over the clear way the plan hands:
cobbles with a kennel down the middle, the verge (the column outside the
clear way, on the south) furnished by `verge_life` with lamps, a bench, a
cart, flower beds and a hedge, kept off the cottages' and the boatwright's
fronts.

    "$DELVEWRIGHT_PYTHON" lane-5.py --allocation <allocation.json> \
        --out <campaign>/programs/lane-5.json --delvec <delvec>
"""

import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
from starter import Model, run, lane, verge_life  # noqa: E402

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

    # lamps, a bench, a cart, beds of flowers and a hedge on the verge
    lane(m, place, verge=lambda m, f: verge_life(
        m, f, things=("lamp", "bed", "bench", "hedge", "lamp", "bed", "cart", "hedge"), every=2,
        flowers=FLOWERS, cart_load=None))
    m.finish()
    return m


raise SystemExit(run(build))
