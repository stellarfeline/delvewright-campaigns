#!/usr/bin/env python3
"""node/street-9: stretch 9 of the main street, drawn with the skill's street helpers.

    python3 street9.py --allocation <handout dir>/allocation.json \
        --out <campaign>/programs/street-9.json --delvec <delvec>

The way runs along z (north: flight 9 at grade; south: flight 10, two down).
`stretch` lays the cobbles, the wandering kennel, the kerb bands where the
flights land and the worn patches; `verge_life` furnishes the verges either
side of the five-wide clear way. No lot fronts this stretch, so no sign hangs.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
from starter import Model, run, stretch, verge_life, lamp  # noqa: E402

SEED = 9  # this stretch's own wear; the same on every run


def build(place):
    m = Model(place)
    m.palette.update({
        "paving": [
            {"block": "minecraft:cobblestone", "weight": 5},
            {"block": "minecraft:mossy_cobblestone", "weight": 1},
            {"block": "minecraft:andesite", "weight": 2},
        ],
        "kennel": "minecraft:polished_andesite",
        "kerb": "minecraft:stone_bricks",
        "verge": [
            {"block": "minecraft:coarse_dirt", "weight": 2},
            {"block": "minecraft:grass_block[snowy=false]", "weight": 3},
            {"block": "minecraft:gravel", "weight": 1},
        ],
    })
    m.palette["floor"] = m.palette["verge"]  # the ground under the open sides' ring runs on as verge

    def verge(m, frame):
        verge_life(m, frame, things=("lamp", "bed", "bench", "lamp", "bed", "cart", "bed"), every=3)
        # a second lamp, on the other verge and as far down the stretch as a
        # free column allows from the lamp the round put down
        y = place.datum.value
        lit = [(x, z) for (x, yy, z), r in m.v.items() if "lantern" in str(r)]
        taken = {(x, z) for (x, yy, z), r in m.v.items() if yy == y and r != "~air"}
        free = sorted(c for c in frame["free"] if c not in taken)
        if lit and free:
            lx, lz = lit[0]
            far = max(free, key=lambda c: (abs(c[0] - lx) > 1, abs(c[1] - lz), -c[0]))
            lamp(m, far[0], far[1])

    frame = stretch(m, place, "z", SEED, clear=5, fronts={}, verge=verge)
    rows, c0, c1 = frame["rows"], frame["c0"], frame["c1"]
    x, z = frame["cell"](rows[len(rows) // 2], (c0 + c1) // 2)
    m.mark("node-street-9", x, z)
    m.show("up")  # the lamps' lanterns stand on the frame's top course, in the open air
    m.finish()
    return m


if __name__ == "__main__":
    raise SystemExit(run(build))
