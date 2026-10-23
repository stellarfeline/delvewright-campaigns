#!/usr/bin/env python3
"""Writes the Lantern Night finale into quests.json: one cutscene and the
lantern lines lit in step with it.

    python3 finale.py

The finale is the `on_complete` sequence of `quest/lantern-night`. It keeps
the lantern-line `fill-region` effects already there (one step per place,
in `lights.ORDER`) and re-times them under one multi-shot cutscene:

1. five shots of the camp under the setting sun, wide and close, from
   different sides;
2. one wide shot from over the lookout as night falls (`set-time`);
3. one shot per place along the lighting route, its lines lit a second
   into its shot;
4. a last wide shot of the whole camp lit.

A shot is a straight dolly between two camera points with the camera held on
one subject. Every point is written in world coordinates here and stated
relative to `anchor/node-root-glade`, which stands at world (28, 72, 38).
The camera's time on each shot and the tick each shot starts on follow
compiler.md's cutscene row: shot k owns 20 x seconds + 1 ticks of the
cutscene's counter, back to back (hard cuts).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
import lights  # noqa: E402

C = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ANCHOR = "anchor/node-root-glade"
ORIGIN = (28, 72, 38)
CUTSCENE_AT = 40          # the sequence tick the cutscene starts on

# (name, seconds, [camera points], subject) — world coordinates.
SUNSET = [
    ("over the camp from the north-east", 7, [(116, 126, 2), (106, 120, 10)], (56, 86, 56)),
    ("the camp from the south", 6, [(52, 98, 126), (66, 98, 122)], (58, 90, 52)),
    ("along the Long Bridge to the Hearth House", 6, [(64, 92, 44), (56, 92, 44)], (40, 90, 32)),
    ("the Low Bridge and the Seed Tree", 6, [(48, 90, 60), (48, 90, 68)], (36, 84, 78)),
    ("the lookout under the last sun", 6, [(98, 118, 66), (98, 118, 88)], (80, 113, 78)),
]
NIGHTFALL = ("night falls over the camp", 8, [(84, 126, 86), (82, 128, 84)], (50, 84, 50))
ROUTE = {   # one shot per place, in lights.ORDER
    "node/watch-house": ("the Watch House", 5, [(62, 94, 60), (64, 94, 62)], (79, 85, 77)),
    "node/high-bridge": ("the High Bridge", 5, [(92, 90, 48), (92, 90, 58)], (79, 81, 53)),
    "node/loom-house": ("the Loom House", 5, [(96, 92, 20), (98, 92, 28)], (80, 81, 36)),
    "node/long-bridge": ("the Long Bridge", 5, [(58, 90, 24), (66, 90, 24)], (61, 81, 35)),
    "node/hearth-house": ("the Hearth House", 5, [(52, 98, 20), (54, 98, 28)], (35, 87, 35)),
    "node/low-bridge": ("the Low Bridge", 5, [(24, 90, 54), (24, 90, 64)], (35, 83, 60)),
    "node/seed-house": ("the Seed House", 5, [(16, 92, 70), (16, 92, 80)], (35, 83, 77)),
    "node/root-glade": ("the Root Glade", 5, [(18, 77, 16), (24, 77, 16)], (35, 72, 26)),
}
LAST = ("the camp lit", 7, [(80, 128, 84), (86, 132, 90)], (50, 84, 50))
NIGHT_INTO_SHOT = 40      # ticks into the nightfall shot that night falls
LIGHT_INTO_SHOT = 20      # ticks into a place's shot that its lines light


def mark(p):
    off = [p[0] - ORIGIN[0], p[1] - ORIGIN[1], p[2] - ORIGIN[2]]
    m = {"anchor": ANCHOR}
    if off != [0, 0, 0]:
        m["offset"] = off
    return m


def shot(spec):
    _, seconds, path, subject = spec
    return {"path": [mark(p) for p in path], "seconds": seconds, "look_at": mark(subject)}


def main():
    path = os.path.join(C, "quests.json")
    doc = json.load(open(path))
    q = next(q for q in doc["content"]["quests"] if q["id"] == "quest/lantern-night")
    seq = next(e for e in q["on_complete"] if e["type"] == "sequence")
    steps = seq["steps"]

    # What the old timeline carried, by kind.
    opening = steps[0]["effects"]
    set_time = next(x for s in steps for x in s["effects"] if x["type"] == "set-time")
    by_place = {}
    for s in steps:
        fills = [x for x in s["effects"] if x["type"] == "fill-region"]
        if not fills:
            continue
        node = next(n for a, n, _, _ in lights.LINES if a == fills[0]["region"]["anchor"])
        by_place[node] = s["effects"]
    assert sorted(by_place) == sorted(lights.ORDER), sorted(by_place)
    closing = [x for s in steps for x in s["effects"] if x["type"] == "narrate" and x is not opening[-1]
               and x not in opening]
    complete = [x for s in steps for x in s["effects"] if x["type"] == "campaign-complete"]
    assert len(closing) == 1 and len(complete) == 1

    specs = SUNSET + [NIGHTFALL] + [ROUTE[n] for n in lights.ORDER] + [LAST]
    starts, t = [], 0
    for spec in specs:
        starts.append(t)
        t += 20 * spec[1] + 1
    end = CUTSCENE_AT + t     # the tick after the cutscene's last owned tick

    new = [{"at_ticks": 0, "effects": opening},
           {"at_ticks": CUTSCENE_AT, "effects": [{"type": "cutscene", "shots": [shot(s) for s in specs]}]},
           {"at_ticks": CUTSCENE_AT + starts[len(SUNSET)] + NIGHT_INTO_SHOT, "effects": [set_time]}]
    for i, node in enumerate(lights.ORDER):
        k = len(SUNSET) + 1 + i
        new.append({"at_ticks": CUTSCENE_AT + starts[k] + LIGHT_INTO_SHOT, "effects": by_place[node]})
    new.append({"at_ticks": end + 20, "effects": closing})
    new.append({"at_ticks": end + 100, "effects": complete})
    seq["steps"] = new
    open(path, "w").write(json.dumps(doc, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
    print(f"finale: {len(specs)} shots, cutscene {t} ticks ({t / 20:.1f} s) from tick {CUTSCENE_AT}; "
          f"night at {new[2]['at_ticks']}; lines at {[s['at_ticks'] for s in new[3:3 + len(lights.ORDER)]]}; "
          f"complete at {end + 100}")


if __name__ == "__main__":
    main()
