"""node/arm-west: the lookout's west arm, a railed glass walkway over the maze."""

import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
from starter import Model, fence, lantern, pillar, run  # noqa: E402

POST_PERIOD = 6  # a lantern post every six cells, counted from the far end


def build(place):
    m = Model(place)
    ex, ez = m.ex, m.ez
    d = place.datum.value
    floor = d - 1
    m.palette["glass"] = "minecraft:glass"
    m.palette["beam-x"] = pillar("dark_oak_log", "x")
    m.palette["beam-z"] = pillar("dark_oak_log", "z")
    m.palette["rail"] = fence("spruce")
    m.palette["lamp"] = lantern()
    m.palette["open"] = "minecraft:air"

    # the walk: clear glass, three wide, the lanes seen straight through it
    m.box(1, ex - 1, floor, floor, 1, ez - 2, "glass")
    # dark oak beams only under the rails: the two sides and the far end
    m.box(0, ex - 1, floor, floor, 0, 0, "beam-x")
    m.box(0, ex - 1, floor, floor, ez - 1, ez - 1, "beam-x")
    m.box(0, 0, floor, floor, 1, ez - 2, "beam-z")

    # the walk kept clear, the full play height
    m.clear(1, ex - 1, d, m.ey - 1, 1, ez - 2)
    # the rail, one course high, on both sides and across the far end, with
    # open air over it so the lanes are seen over the rail
    m.box(0, ex - 1, d, m.ey - 1, 0, 0, "open")
    m.box(0, ex - 1, d, m.ey - 1, ez - 1, ez - 1, "open")
    m.box(0, 0, d, m.ey - 1, 0, ez - 1, "open")
    m.box(0, ex - 1, d, d, 0, 0, "rail")
    m.box(0, ex - 1, d, d, ez - 1, ez - 1, "rail")
    m.box(0, 0, d, d, 0, ez - 1, "rail")
    # lantern posts: the rail stood up one course, a lantern on top
    for x in range(0, ex - 1, POST_PERIOD):
        for z in (0, ez - 1):
            m.set(x, d + 1, z, "rail")
            m.set(x, d + 2, z, "lamp")

    m.mark("node-arm-west", ex // 2, ez // 2)
    m.show("up")
    m.finish()
    return m


raise SystemExit(run(build))
