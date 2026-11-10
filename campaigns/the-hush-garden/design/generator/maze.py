#!/usr/bin/env python3
"""node/maze of The Hush Garden: a braided hedge maze round a watchtower court.

Drawn into the starter's `Model` (imported from `$DELVEWRIGHT_SKILL/scripts`).
The lane grid, the courts, the bells and the anchors are read off the play
space; the maze itself is a recursive backtracker over the cell grid from the
heart, braided, seeded through this file's own named PRNG (`MAZE_SEED`).

Palette (measured, block-appearance.py against the pinned 1.21.11 client jar):
  wall stone   stone_bricks #7a7a7a 5 : mossy_stone_bricks #737969 4 : cracked_stone_bricks 1
               (mix mean #777973, chroma_mass 0.0125, loudest member mossy at 40%)
  hedge cap    azalea_leaves #5a732c (persistent)
  rose floor   pink_terracotta #a24e4f      yellow floor yellow_terracotta #ba8523
  blue floor   light_blue_terracotta #716d8a green floor lime_terracotta #687635
  heart paving calcite #dfe0dd               tower smooth_sandstone #e0d6aa
  well rim     cracked_deepslate_bricks #414141, sculk #0d1c22
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import sys

sys.path.insert(0, os.path.join(os.environ["DELVEWRIGHT_SKILL"], "scripts"))
from starter import AIR, Model, run, stairs, slab, trapdoor, fence, lantern, barrel, leaves, ladder  # noqa: E402

# ---- the named PRNG: splitmix64 over a seed derived from the place's name ----

MAZE_SEED = int.from_bytes(hashlib.sha256(b"the-hush-garden/node/maze/lanes").digest()[:8], "big")


class SplitMix64:
    def __init__(self, seed: int) -> None:
        self.s = seed & 0xFFFFFFFFFFFFFFFF

    def next(self) -> int:
        self.s = (self.s + 0x9E3779B97F4A7C15) & 0xFFFFFFFFFFFFFFFF
        z = self.s
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & 0xFFFFFFFFFFFFFFFF
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & 0xFFFFFFFFFFFFFFFF
        return z ^ (z >> 31)

    def below(self, n: int) -> int:
        return self.next() % n

    def unit(self) -> float:
        return (self.next() >> 11) / float(1 << 53)

    def choice(self, seq):
        return seq[self.below(len(seq))]

    def shuffle(self, seq) -> None:
        for i in range(len(seq) - 1, 0, -1):
            j = self.below(i + 1)
            seq[i], seq[j] = seq[j], seq[i]


# ---- the grid: 28 x 28 cells at a pitch of 3, lanes on 3k+1, 3k+2 ----

N = 28
HEAR = 16  # the warden's hearing reach, blocks
BRAID = 0.85


def lane(k: int) -> tuple[int, int]:
    """The two piece-local columns of cell index k (play space starts at 1)."""
    return 3 * k + 1, 3 * k + 2


def wall_at(k: int) -> int:
    """The wall column between cell k and k+1."""
    return 3 * k + 3


HEART = {(k, j) for k in range(12, 16) for j in range(12, 16)}
SUNDIAL = {(k, j) for k in (7, 8) for j in (7, 8)}
WELL = {(k, j) for k in (0, 1) for j in (26, 27)}
COURTS = {"heart": HEART, "sundial": SUNDIAL, "well": WELL}
GATE_CELL = (27, 13)
# The bells: a wall segment between two cells near each quarter's middle, kept closed.
BELLS = {  # stem -> (cell a, cell b, the column the bell stands on)
    "nw": ((6, 6), (7, 6)),
    "ne": ((20, 6), (21, 6)),
    "se": ((20, 21), (21, 21)),
    "sw": ((6, 21), (7, 21)),
}
WELL_POINT = (2, 80)  # anchor/the-well's column


def quarter(k: int, j: int) -> str:
    west, north = k < 14, j < 14
    return {(True, True): "rose", (False, True): "yellow", (False, False): "blue", (True, False): "green"}[(west, north)]


def node_of(c):
    for name, cells in COURTS.items():
        if c in cells:
            return name
    return c


def segment(a, b) -> list[tuple[int, int]]:
    """The wall cells (x, z) between two adjacent cells."""
    (k0, j0), (k1, j1) = sorted([a, b])
    if j0 == j1:
        x = wall_at(k0)
        return [(x, z) for z in lane(j0)]
    z = wall_at(j0)
    return [(x, z) for x in lane(k0)]


def cell_dist(c, p) -> float:
    return min(math.hypot(x + 0.5 - (p[0] + 0.5), z + 0.5 - (p[1] + 0.5)) for x in lane(c[0]) for z in lane(c[1]))


def generate():
    rng = SplitMix64(MAZE_SEED)
    cells = [(k, j) for k in range(N) for j in range(N)]
    blocked = {frozenset(ab) for ab in BELLS.values()}
    adj: dict = {}
    for k, j in cells:
        for dk, dj in ((1, 0), (0, 1)):
            o = (k + dk, j + dj)
            if o[0] >= N or o[1] >= N:
                continue
            a, b = node_of((k, j)), node_of(o)
            if a == b or frozenset(((k, j), o)) in blocked:
                continue
            adj.setdefault(a, {}).setdefault(b, []).append(((k, j), o))
            adj.setdefault(b, {}).setdefault(a, []).append(((k, j), o))
    nodes = sorted(adj, key=str)
    opened: set = set()  # frozenset of the two cells
    tree: dict = {}  # node -> parent
    # recursive backtracker from the heart
    seen = {"heart"}
    stack = ["heart"]
    tree["heart"] = None
    while stack:
        top = stack[-1]
        nxt = sorted([n for n in adj[top] if n not in seen], key=str)
        if not nxt:
            stack.pop()
            continue
        n = rng.choice(nxt)
        e = rng.choice(sorted(adj[top][n]))
        opened.add(frozenset(e))
        seen.add(n)
        tree[n] = top
        stack.append(n)
    assert len(seen) == len(nodes), "the backtracker left cells unvisited"
    tree_edges = set(opened)

    def degree(n) -> int:
        d = sum(1 for m, es in adj[n].items() if any(frozenset(e) in opened for e in es))
        return d + (1 if n == GATE_CELL else 0)

    def dead(n) -> bool:
        return not isinstance(n, str) and degree(n) == 1

    dead0 = [n for n in nodes if dead(n)]
    order = list(dead0)
    rng.shuffle(order)
    for n in order:
        if not dead(n):
            continue
        near = cell_dist(n, WELL_POINT) <= HEAR
        if not near and rng.unit() >= BRAID:
            continue
        closed = [(m, e) for m, es in sorted(adj[n].items(), key=lambda t: str(t[0])) for e in sorted(es) if frozenset(e) not in opened]
        if not closed:
            continue
        prefer = [(m, e) for m, e in closed if dead(m)]
        m, e = rng.choice(prefer or closed)
        opened.add(frozenset(e))
    kept = [n for n in nodes if dead(n)]
    for n in kept:
        assert cell_dist(n, WELL_POINT) > HEAR, f"a dead end {n} stands within {HEAR} of the well"
    braids = opened - tree_edges
    # the node graph after braiding
    g: dict = {n: set() for n in nodes}
    for e in opened:
        a, b = (node_of(c) for c in e)
        g[a].add(b)
        g[b].add(a)
    edges = sum(len(v) for v in g.values()) // 2
    loops = edges - len(nodes) + 1
    # fundamental loops: the tree path between a braid's ends, plus the braid
    def centre(n):
        cs = sorted(COURTS[n]) if isinstance(n, str) else [n]
        return (sum(3 * k + 2 for k, _ in cs) / len(cs), sum(3 * j + 2 for _, j in cs) / len(cs))

    def to_root(n):
        out = [n]
        while tree[out[-1]] is not None:
            out.append(tree[out[-1]])
        return out

    wide = 0
    for e in braids:
        a, b = (node_of(c) for c in sorted(e))
        pa, pb = to_root(a), to_root(b)
        common = next(x for x in pa if x in set(pb))
        cyc = pa[: pa.index(common) + 1] + list(reversed(pb[: pb.index(common)]))
        pts = [centre(n) for n in cyc]
        L = len(pts)
        ok = L >= 4 and all(math.dist(pts[i], pts[(i + L // 2) % L]) > HEAR for i in range(L))
        wide += ok
    stats = {
        "cells": N * N,
        "nodes": len(nodes),
        "dead_ends_before_braid": len(dead0),
        "dead_ends_kept": len(kept),
        "independent_loops": loops,
        "fundamental_loops_opposite_points_beyond_16": wide,
        "kept_dead_end_distance_from_well": sorted(round(cell_dist(n, WELL_POINT), 1) for n in kept),
    }
    return opened, stats


def route(m: Model, a, b) -> int:
    """Blocks walked from column a to column b along open lane floor (4-connected)."""
    def free(x, z):
        if not (1 <= x <= 83 and 1 <= z <= 83):
            return False
        for y in (1, 2):
            r = m.v.get((x, y, z))
            if r not in (None, AIR) and not str(r).startswith("minecraft:sculk_vein"):
                return False
        return True

    from collections import deque
    dist = {a: 0}
    q = deque([a])
    while q:
        c = q.popleft()
        if c == b:
            return dist[c]
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (c[0] + dx, c[1] + dz)
            if n not in dist and free(*n):
                dist[n] = dist[c] + 1
                q.append(n)
    raise AssertionError(f"no route from {a} to {b}")


def route_cells(m: Model, a, b) -> list:
    """The cells of one shortest route (by BFS parents)."""
    def free(x, z):
        if not (1 <= x <= 83 and 1 <= z <= 83):
            return False
        return all(m.v.get((x, y, z)) in (None, AIR) for y in (1, 2))

    from collections import deque
    par = {a: None}
    q = deque([a])
    while q:
        c = q.popleft()
        if c == b:
            break
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (c[0] + dx, c[1] + dz)
            if n not in par and free(*n):
                par[n] = c
                q.append(n)
    out = [b]
    while par[out[-1]] is not None:
        out.append(par[out[-1]])
    return list(reversed(out))


def build(place):
    m = Model(place)
    P = m.palette
    P["wallstone"] = [
        {"block": "minecraft:stone_bricks", "weight": 5},
        {"block": "minecraft:mossy_stone_bricks", "weight": 4},
        {"block": "minecraft:cracked_stone_bricks", "weight": 1},
    ]
    P["hedge"] = [
        {"block": leaves("azalea"), "weight": 7},
        {"block": leaves("flowering_azalea"), "weight": 1},
    ]
    P["rose"] = "minecraft:pink_terracotta"
    P["yellow"] = "minecraft:yellow_terracotta"
    P["blue"] = "minecraft:light_blue_terracotta"
    P["green"] = "minecraft:lime_terracotta"
    P["paving"] = "minecraft:calcite"
    P["footing"] = "minecraft:stone_bricks"
    P["tower"] = "minecraft:smooth_sandstone"
    P["band"] = "minecraft:chiseled_sandstone"
    P["cut"] = "minecraft:cut_sandstone"
    P["deck"] = "minecraft:spruce_planks"
    P["rim"] = "minecraft:cracked_deepslate_bricks"
    P["sculk"] = "minecraft:sculk"
    P["soil"] = "minecraft:grass_block[snowy=false]"
    P["plinth"] = "minecraft:chiseled_stone_bricks"

    opened, stats = generate()
    TOP = 21  # the play space's top course, piece-local (place.space)
    assert place.space[1][1] == TOP

    # -- floor (y 0) and walls (y 1..4) over the whole frame --
    open_cols = set()
    for c in [(k, j) for k in range(N) for j in range(N)]:
        for x in lane(c[0]):
            for z in lane(c[1]):
                open_cols.add((x, z))
    for e in opened:
        open_cols.update(segment(*sorted(e)))
    for name, cells in COURTS.items():
        xs = [x for k, _ in cells for x in lane(k)]
        zs = [z for _, j in cells for z in lane(j)]
        for x in range(min(xs), max(xs) + 1):
            for z in range(min(zs), max(zs) + 1):
                open_cols.add((x, z))

    def floor_role(x, z):
        k, j = min((x - 1) // 3, N - 1), min((z - 1) // 3, N - 1)
        if (k, j) in HEART and 37 <= x <= 47 and 37 <= z <= 47:
            return "paving"
        return quarter(k, j)

    for x in range(0, 85):
        for z in range(0, 85):
            ring = x in (0, 84) or z in (0, 84)
            if ring or (x, z) not in open_cols:
                m.set(x, 0, z, "footing")
                m.box(x, x, 1, 3, z, z, "wallstone")
                m.set(x, 4, z, "hedge")
                if ring:
                    # an open place's ring is the same 4-course wall, open sky above
                    m.box(x, x, 5, TOP, z, z, "minecraft:air")
            else:
                m.set(x, 0, z, floor_role(x, z))

    # -- the heart: the watchtower, 5 x 5, hollow, from the walk plane to the top --
    for y in range(1, TOP + 1):
        role = "cut" if y in (1, TOP) else ("band" if y == 10 else "tower")
        m.hollow(40, 44, y, y, 40, 44, role)
    m.box(41, 43, 0, 0, 41, 43, "tower")
    # the arched door on the court, 1 wide and 2 high, south face
    m.clear(42, 42, 1, 2, 44, 44)
    m.set(41, 3, 44, stairs("sandstone", "east", "top"))
    m.set(43, 3, 44, stairs("sandstone", "west", "top"))
    m.set(42, 3, 44, "band")
    # the ladder straight up the shaft's middle to the hatch, hung on a spine
    # of the tower's stone on its north side; the rung in the hatch's own cell
    # is written by `post` (the opening's cells are the seam's)
    m.climbs_to("edge/up-the-tower")
    m.box(42, 42, 1, TOP, 41, 41, "tower")
    m.box(42, 42, 1, TOP - 1, 42, 42, ladder("south"))
    # a resting deck under the hatch, round the ladder
    for x in range(41, 44):
        for z in range(41, 44):
            if (x, z) not in ((42, 42), (42, 41)):
                m.set(x, 19, z, "deck")
    # slits let the afternoon light down the shaft
    for y in (5, 9, 13, 17):
        for x, z in ((42, 40), (40, 42), (44, 42)):
            m.clear(x, x, y, y, z, z)
        if y > 3:
            m.clear(42, 42, y, y, 44, 44)
    # lanterns at the foot of the shaft and under the deck
    m.set(41, 1, 41, lantern())
    m.set(41, 1, 43, lantern())
    m.set(41, 18, 43, lantern(hanging=True))
    m.set(43, 18, 41, lantern(hanging=True))
    # beside the tower, west: lantern post, bench of stairs, barrel, lantern post
    m.set(39, 1, 40, fence("spruce"))
    m.set(39, 2, 40, lantern())
    m.set(39, 1, 41, stairs("spruce", "east"))
    m.set(39, 1, 42, stairs("spruce", "east"))
    m.set(39, 1, 43, barrel("up"))
    m.set(39, 1, 44, fence("spruce"))
    m.set(39, 2, 44, lantern())
    # rose bushes in the heart's four corners
    for x, z in ((37, 37), (47, 37), (37, 47), (47, 47)):
        m.set(x, 0, z, "soil")
        m.tall(x, 1, z, "rose_bush")

    # -- the sundial court (rose quarter): a stepped plinth, a dial, a gnomon --
    m.set(24, 1, 24, "plinth")
    m.set(24, 2, 24, "plinth")
    m.set(24, 3, 24, slab("smooth_stone"))
    m.set(24, 1, 23, stairs("stone_brick", "south"))
    m.set(24, 1, 25, stairs("stone_brick", "north"))
    m.set(23, 1, 24, stairs("stone_brick", "east"))
    m.set(25, 1, 24, stairs("stone_brick", "west"))
    for x, z in ((23, 23), (25, 23), (23, 25), (25, 25)):
        m.set(x, 1, z, slab("stone_brick"))
    for x in range(22, 27):
        for z in range(22, 27):
            if max(abs(x - 24), abs(z - 24)) == 2:
                m.set(x, 0, z, "minecraft:smooth_stone")

    # -- the old well (green quarter's far corner) --
    for x in range(3, 6):
        for z in range(81, 84):
            m.set(x, 1, z, "rim")
    m.set(4, 1, 82, trapdoor("iron", "north"))
    m.set(4, 0, 82, "sculk")
    vein = "minecraft:sculk_vein[down=true,east=false,north=false,south=false,up=false,waterlogged=false,west=false]"
    sculk_floor = [(1, 83), (2, 83), (1, 82), (2, 82), (3, 80), (4, 80), (5, 80), (5, 79), (1, 81), (3, 79), (6, 82), (4, 79)]
    for x, z in sculk_floor:
        if (x, z) in open_cols:
            m.set(x, 0, z, "sculk")
    for x, z in ((1, 79), (3, 79), (1, 81), (1, 83)):
        if (x, z) in open_cols and m.get(x, 1, z) is None and (x, z) != WELL_POINT:
            m.set(x, 1, z, vein)

    # -- the bells: on the wall's top stone course, hedge cap removed --
    bell_cells = {}
    for stem, (a, b) in BELLS.items():
        x, z = segment(a, b)[0]
        facing = "east" if a[1] == b[1] else "north"  # the bell's face across the lanes either side
        m.set(x, 3, z, "minecraft:stone_bricks")
        m.set(x, 4, z, f"minecraft:bell[attachment=floor,facing={facing},powered=false]")
        # a little bell-cote: two spruce posts on the hedge either side along the
        # wall, a slab roof over the bell; the air between bell and roof is the
        # power cell, too low for a body to stand in
        along = (0, 1) if a[1] == b[1] else (1, 0)
        for sgn in (-1, 1):
            m.set(x + sgn * along[0], 5, z + sgn * along[1], fence("spruce"))
        for t in (-1, 0, 1):
            m.set(x + t * along[0], 6, z + t * along[1], slab("spruce"))
        bell_cells[stem] = (x, z)
        m.mark(f"bell-{stem}", x, z, "south", y=4)
        m.mark(f"bell-{stem}-power", x, z, "south", y=5)

    # -- the anchors --
    m.mark("spawn", 42, 46, "east")
    m.mark("node-maze", 46, 42, "south")
    m.mark("bench", 38, 41, "west")
    m.mark("note-basket", 39, 43, "east", y=1)
    m.mark("crank-frame", 24, 25, "south", y=2)
    m.mark("sundial", 24, 26, "north")
    m.mark("the-well", WELL_POINT[0], WELL_POINT[1], "south")
    gate = (83, 40)
    sundial = (24, 26)
    spawn = (42, 46)
    r1 = route_cells(m, spawn, sundial)
    r2 = route_cells(m, sundial, gate)

    def junction(c) -> bool:
        x, z = c
        return sum(1 for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)) if (x + 2 * dx, z + 2 * dz) in open_cols and (x + dx, z + dz) in open_cols) >= 3

    def pick(path, q, frac):
        cand = [c for c in path if quarter(min((c[0] - 1) // 3, 27), min((c[1] - 1) // 3, 27)) == q
                and (min((c[0] - 1) // 3, 27), min((c[1] - 1) // 3, 27)) not in HEART | SUNDIAL
                and junction(c)]
        assert cand, f"no junction in the {q} quarter on the route"
        return cand[min(len(cand) - 1, int(len(cand) * frac))]

    sr = pick(r1, "rose", 0.5)
    sy = pick(r2, "yellow", 0.5)
    m.mark("slimes-rose", sr[0], sr[1], "south")
    m.mark("slimes-yellow", sy[0], sy[1], "south")

    # -- what the generator asserts and prints --
    stats["route_heart_to_sundial_blocks"] = len(r1) - 1
    stats["route_sundial_to_gate_blocks"] = len(r2) - 1
    stats["slimes"] = {"rose": sr, "yellow": sy}
    cover = {}
    for stem, (bx, bz) in bell_cells.items():
        q = {"nw": "rose", "ne": "yellow", "se": "blue", "sw": "green"}[stem]
        cols = [(x, z) for (x, z) in open_cols if 1 <= x <= 83 and 1 <= z <= 83
                and quarter(min((x - 1) // 3, 27), min((z - 1) // 3, 27)) == q
                and (min((x - 1) // 3, 27), min((z - 1) // 3, 27)) not in HEART]
        near = sum(1 for x, z in cols if math.dist((x, 1, z), (bx, 4, bz)) <= HEAR)
        cover[stem] = f"{near}/{len(cols)}"
    stats["bell_lane_columns_within_16"] = cover
    print("maze.py: " + json.dumps(stats), file=sys.stderr)
    m.show("up")
    m.finish()
    return m


def post(path: str) -> None:
    """What the starter's `mark` does not write: the spawn's `entry` role and the crank frame's holder."""
    with open(path, encoding="utf-8") as f:
        doc = json.load(f)
    found = {"spawn": 0, "crank-frame": 0}

    def walk(o):
        if isinstance(o, dict):
            mk = o.get("mark") if o.get("op") == "mark" else None
            if isinstance(mk, dict):
                if mk.get("anchor") == "spawn":
                    mk["role"] = "entry"
                    found["spawn"] += 1
                if mk.get("anchor") == "crank-frame":
                    mk["holder"] = {"kind": "item-frame"}
                    found["crank-frame"] += 1
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(doc["rules"])
    assert found == {"spawn": 1, "crank-frame": 1}, found
    # the top rung, in the hatch's own cell: the seam's opening holds the ladder
    rung = [r for r, st in doc["palette"].items() if st == ladder("south")]
    assert len(rung) == 1, rung
    hatch = {"n": 0}

    def rung_in(o):
        if isinstance(o, dict):
            if o.get("op") == "claim" and o.get("region") == "up-the-tower-way":
                assert o["body"] == {"op": "void"}, o
                o["body"] = {"material": {"role": rung[0]}, "op": "fill"}
                hatch["n"] += 1
            for v in o.values():
                rung_in(v)
        elif isinstance(o, list):
            for v in o:
                rung_in(v)

    rung_in(doc["rules"])
    assert hatch["n"] == 1, hatch
    # Cells the starter writes as bare fills that the contract must hold: the
    # ring's open air over the 4-course wall (its top is floor no body reaches),
    # the bells on the walls (their anchors), and the note basket (its anchor).
    wrap = {}
    for role, state in doc["palette"].items():
        if not isinstance(state, str):
            continue
        if state == "minecraft:air":
            wrap[role] = "unwalked"
        elif state.startswith("minecraft:barrel[") or state.startswith("minecraft:bell["):
            wrap[role] = "room"
    assert sorted(set(wrap.values())) == ["room", "unwalked"], wrap
    assert "unwalked" in doc["contract"].get("no_body", {}), "no unwalked region declared"
    count = {r: 0 for r in wrap}

    def claim(o):
        if isinstance(o, dict):
            for k, v in list(o.items()):
                if isinstance(v, dict) and v.get("op") == "fill" and v.get("material", {}).get("role") in wrap:
                    r = v["material"]["role"]
                    o[k] = {"body": v, "op": "claim", "region": wrap[r]}
                    count[r] += 1
                else:
                    claim(v)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                if isinstance(v, dict) and v.get("op") == "fill" and v.get("material", {}).get("role") in wrap:
                    r = v["material"]["role"]
                    o[i] = {"body": v, "op": "claim", "region": wrap[r]}
                    count[r] += 1
                else:
                    claim(v)

    claim(doc["rules"])
    assert all(n > 0 for n in count.values()), count
    print("maze.py: post — claimed " + ", ".join(f"{doc['palette'][r]} -> {wrap[r]} ({n} leaf/leaves)" for r, n in sorted(count.items())), file=sys.stderr)
    with open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(doc, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    code = run(build, reason="the hedge tops, the tower's head and the plinth: seen, never stood on")
    if code == 0:
        post(sys.argv[sys.argv.index("--out") + 1])
    raise SystemExit(code)
