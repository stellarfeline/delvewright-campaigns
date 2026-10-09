"""The finale's lantern lines: one per rail segment, lit house by house.

(station anchor, node, centre (world x, y, z), half-extent [x, y, z]).
The centre is where the place's piece marks the station; the line is the
row of cells over the rail's fence tops, `centre +- half-extent`.
"""
LINES = [
    # nearest the lookout first
    ("anchor/lights-watch-n", "node/watch-house", (85, 85, 67), [3, 0, 0]),
    ("anchor/lights-watch-w", "node/watch-house", (69, 85, 77), [0, 0, 9]),
    ("anchor/lights-watch-e", "node/watch-house", (90, 85, 77), [0, 0, 9]),
    ("anchor/lights-watch-s", "node/watch-house", (79, 85, 88), [9, 0, 0]),
    ("anchor/lights-high-w", "node/high-bridge", (77, 81, 53), [0, 0, 6]),
    ("anchor/lights-high-e", "node/high-bridge", (81, 81, 53), [0, 0, 6]),
    ("anchor/lights-loom-n", "node/loom-house", (79, 81, 27), [7, 0, 0]),
    ("anchor/lights-loom-e", "node/loom-house", (88, 81, 35), [0, 0, 7]),
    ("anchor/lights-loom-w", "node/loom-house", (71, 81, 40), [0, 0, 2]),
    ("anchor/lights-loom-s", "node/loom-house", (84, 81, 44), [2, 0, 0]),
    ("anchor/lights-long-n", "node/long-bridge", (63, 81, 33), [5, 0, 0]),
    ("anchor/lights-long-s", "node/long-bridge", (63, 81, 37), [5, 0, 0]),
    ("anchor/lights-hearth-n", "node/hearth-house", (35, 87, 23), [11, 0, 0]),
    ("anchor/lights-hearth-w", "node/hearth-house", (23, 87, 35), [0, 0, 11]),
    ("anchor/lights-hearth-e", "node/hearth-house", (48, 87, 28), [0, 0, 4]),
    ("anchor/lights-hearth-s", "node/hearth-house", (28, 87, 48), [4, 0, 0]),
    ("anchor/lights-low-w", "node/low-bridge", (33, 83, 61), [0, 0, 5]),
    ("anchor/lights-low-e", "node/low-bridge", (37, 83, 61), [0, 0, 5]),
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
