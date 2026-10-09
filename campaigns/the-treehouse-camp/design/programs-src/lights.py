"""The finale's lantern lines: one per rail segment, lit house by house.

(station anchor, node, centre (world x, y, z), half-extent [x, y, z]).
The centre is where the place's piece marks the station; the line is the
row of cells over the rail's fence tops, `centre +- half-extent`.
"""
LINES = [
    # nearest the lookout first
    ("anchor/lights-watch-n", "node/watch-house", (83, 85, 69), [4, 0, 0]),
    ("anchor/lights-watch-w", "node/watch-house", (67, 85, 79), [0, 0, 9]),
    ("anchor/lights-watch-e", "node/watch-house", (88, 85, 79), [0, 0, 9]),
    ("anchor/lights-watch-s", "node/watch-house", (77, 85, 90), [9, 0, 0]),
    ("anchor/lights-high-w", "node/high-bridge", (75, 81, 54), [0, 0, 7]),
    ("anchor/lights-high-e", "node/high-bridge", (80, 81, 54), [0, 0, 7]),
    ("anchor/lights-loom-n", "node/loom-house", (77, 81, 27), [7, 0, 0]),
    ("anchor/lights-loom-e", "node/loom-house", (86, 81, 35), [0, 0, 7]),
    ("anchor/lights-loom-w", "node/loom-house", (69, 81, 40), [0, 0, 2]),
    ("anchor/lights-loom-s", "node/loom-house", (83, 81, 44), [2, 0, 0]),
    ("anchor/lights-long-n", "node/long-bridge", (62, 81, 33), [4, 0, 0]),
    ("anchor/lights-long-s", "node/long-bridge", (62, 81, 38), [4, 0, 0]),
    ("anchor/lights-hearth-n", "node/hearth-house", (35, 87, 23), [11, 0, 0]),
    ("anchor/lights-hearth-w", "node/hearth-house", (23, 87, 35), [0, 0, 11]),
    ("anchor/lights-hearth-e", "node/hearth-house", (48, 87, 28), [0, 0, 4]),
    ("anchor/lights-hearth-s", "node/hearth-house", (28, 87, 48), [4, 0, 0]),
    ("anchor/lights-low-w", "node/low-bridge", (33, 83, 61), [0, 0, 5]),
    ("anchor/lights-low-e", "node/low-bridge", (38, 83, 61), [0, 0, 5]),
    ("anchor/lights-seed-n", "node/seed-house", (40, 83, 69), [3, 0, 0]),
    ("anchor/lights-seed-w", "node/seed-house", (27, 83, 77), [0, 0, 7]),
    ("anchor/lights-seed-e", "node/seed-house", (44, 83, 77), [0, 0, 7]),
    ("anchor/lights-seed-s", "node/seed-house", (35, 83, 86), [7, 0, 0]),
    ("anchor/lights-glade", "node/root-glade", (35, 72, 26), [8, 0, 0]),
]

# The order the places light in, and the tick each starts at.
ORDER = ["node/watch-house", "node/high-bridge", "node/loom-house", "node/long-bridge",
         "node/hearth-house", "node/low-bridge", "node/seed-house", "node/root-glade"]


def for_node(node):
    return [l for l in LINES if l[1] == node]
