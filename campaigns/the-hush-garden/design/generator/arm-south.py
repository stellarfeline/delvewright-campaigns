#!/usr/bin/env python3
"""node/arm-south: the lookout's south arm — a railed glass walkway on thin dark oak beams, 22 over the maze.

Palette, measured with tools/creator/block-appearance.py against the pinned client jar:
  deck     minecraft:glass             clear: the caller sees the lanes straight below
  beam     minecraft:dark_oak_log      #402e18 (a stringer under each side rail and one under the far rail; none under the walk)
  rail     minecraft:spruce_fence      #735531 (one course: low enough to see the lanes over)
  lamp     minecraft:lantern           #6b5c55 (standing on a fence post, every six cells)
"""
import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
from starter import Model, fence, lantern, pillar, run  # noqa: E402

POST_PERIOD = 6


def build(place):
    m = Model(place)
    ex, ey, ez = m.ex, m.ey, m.ez
    d = place.datum.value  # the walk plane
    floor = d - 1
    xe, xw = 0, ex - 1          # the two edge columns (the ring)
    zend = ez - 1               # the far end's ring row
    m.palette["deck"] = "minecraft:glass"
    m.palette["stringer"] = pillar("minecraft:dark_oak_log", "z")
    m.palette["crossbeam"] = pillar("minecraft:dark_oak_log", "x")
    m.palette["rail"] = fence("spruce")
    m.palette["lamp-on-post"] = lantern()
    # the ring over the rail is open sky, never the empty place's wall: the
    # rail is the only thing between a body and the drop
    m.palette["open-air"] = "minecraft:air"

    # the deck course: clear glass between two dark oak stringers
    m.box(xe + 1, xw - 1, floor, floor, 0, zend - 1, "deck")
    m.box(xe, xe, floor, floor, 0, zend - 1, "stringer")
    m.box(xw, xw, floor, floor, 0, zend - 1, "stringer")
    # a dark oak beam under the far end's rail only: nothing under the walk
    posts = list(range(POST_PERIOD - 1, zend, POST_PERIOD))
    m.box(xe, xw, floor, floor, zend, zend, "crossbeam")
    # the clear above the deck
    m.clear(xe + 1, xw - 1, d, ey - 1, 0, zend - 1)
    # one course of rail along both sides and across the far end
    for x in (xe, xw):
        m.box(x, x, d, d, 0, zend, "rail")
        m.box(x, x, d + 1, ey - 1, 0, zend, "open-air")
    m.box(xe, xw, d, d, zend, zend, "rail")
    m.box(xe, xw, d + 1, ey - 1, zend, zend, "open-air")
    # a lantern on a post over the rail every six cells, on both sides
    for z in posts:
        for x in (xe, xw):
            m.box(x, x, d + 1, d + 1, z, z, "rail")
            m.set(x, d + 2, z, "lamp-on-post")
    m.show("up")
    m.mark("node-arm-south", (xe + xw) // 2, zend - 3, facing="south")
    m.finish()
    return m


raise SystemExit(run(build, reason="the rail's beams, posts and lanterns: seen, never stood on"))
