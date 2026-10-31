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
from starter import Model, run, stretch, verge_life  # noqa: E402

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
            {"block": "minecraft:rooted_dirt", "weight": 1},
        ],
    })

    def verge(m, frame):
        # a lamp at each end of the stretch, on opposite verges, and the
        # rest of the verge furnished in turn between them
        rows = frame["rows"]
        verge_life(m, frame, things=("bed", "bench", "bed", "cart", "bed"), every=3,
                   at=[("lamp", rows[2], "low"), ("lamp", rows[-3], "high")])

    frame = stretch(m, place, seed=SEED, fronts={}, verge=verge)
    rows, c0, c1 = frame["rows"], frame["c0"], frame["c1"]
    x, z = frame["cell"](rows[len(rows) // 2], (c0 + c1) // 2)
    m.mark("node-street-9", x, z)
    m.finish()
    return m


if __name__ == "__main__":
    raise SystemExit(run(build))
