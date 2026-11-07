#!/usr/bin/env python3
"""node/flight-5: Flight 5 of the main street, two shallow steps down between low kerbs.

The clear way's columns carry the treads; the verge column on each side of it
is a kerb of setts that steps down with the flight in whole courses, so a body
coming off an open side meets a kerb, never the end of a tread (DW0430)."""
import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
from starter import Model, run, flight, verge_life, clear_cols, way_frame, walk_of  # noqa: E402

ROLES = {"kerb": "setts", "paving": "cobble", "verge": "worn"}


def build(place):
    m = Model(place)
    m.palette["cobble"] = [
        {"block": "minecraft:cobblestone", "weight": 7},
        {"block": "minecraft:stone", "weight": 3},
        {"block": "minecraft:andesite", "weight": 2},
        {"block": "minecraft:mossy_cobblestone", "weight": 1},
        {"block": "minecraft:tuff", "weight": 1},
    ]
    m.palette["setts"] = [
        {"block": "minecraft:stone_bricks", "weight": 6},
        {"block": "minecraft:cracked_stone_bricks", "weight": 2},
        {"block": "minecraft:mossy_stone_bricks", "weight": 1},
    ]
    m.palette["worn"] = [
        {"block": "minecraft:cobblestone", "weight": 4},
        {"block": "minecraft:coarse_dirt", "weight": 3},
        {"block": "minecraft:tuff", "weight": 2},
        {"block": "minecraft:grass_block[snowy=false]", "weight": 3},
        {"block": "minecraft:mossy_cobblestone", "weight": 1},
        {"block": "minecraft:packed_mud", "weight": 1},
    ]
    frame = flight(m, place, ROLES, step="minecraft:stone_brick", lamp_side="low", flower="minecraft:allium")
    # The kerbs: every tread the helper laid on a verge column becomes a block of setts at its own course.
    axis, c0, c1 = clear_cols(place, frame["axis"], None, "flight")
    rows, cols, cell = way_frame(place, axis)
    w = walk_of(m)
    for b in cols:
        if c0 <= b <= c1:
            continue
        for a in rows:
            x, z = cell(a, b)
            for y in (w, w + 1):
                s = m.get(x, y, z)
                if s is not None and "_stairs" in s:
                    m.set(x, y, z, "setts")
    return m


if __name__ == "__main__":
    sys.exit(run(build, reason="lamp tops and the kerb's heads: seen, never stood on"))
