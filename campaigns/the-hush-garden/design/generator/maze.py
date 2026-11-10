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
  rose floor   pink_concrete_powder #e599b5       yellow floor yellow_concrete_powder #e9c737
  blue floor   light_blue_concrete_powder #4ab5d5 green floor lime_concrete_powder #7dbd2a
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
WELL = {(k, j) for k in (4, 5) for j in (4, 5)}  # rose quarter, beyond the sundial toward (0, 0)
COURTS = {"heart": HEART, "sundial": SUNDIAL, "well": WELL}
GATE_CELL = (27, 13)
# The bells: a wall segment between two cells near each quarter's middle, kept closed.
BELLS = {  # stem -> (cell a, cell b, the column the bell stands on)
    "nw": ((6, 6), (7, 6)),
    "ne": ((20, 6), (21, 6)),
    "se": ((20, 21), (21, 21)),
    "sw": ((6, 21), (7, 21)),
}
WELL_POINT = (14, 16)  # anchor/the-well's column: open floor beside the rim
WELL_MOUTH = (16, 14)  # the grate in the middle of the rim (rim 15..17 x 13..15), clear of the lane in
CRANK_FRAME = (24, 2, 25)  # the item frame on the plinth's south face
# The way from the sundial to the well: out of the court's west side on its
# south row, north up one lane, west into the well court -- two turns, and the
# well court's walls stand between (it is out of sight from the dial).
CORRIDOR = [((7, 8), (6, 8)), ((6, 8), (6, 7)), ((6, 7), (6, 6)), ((6, 6), (6, 5)), ((6, 5), (5, 5))]
# The well court's ways out: the corridor's, and one more from its outer corner
# (a court with one way out is a dead end beside the well).
WELL_EXITS = [((4, 4), (3, 4)), ((4, 4), (4, 3))]


def _run(cells):
    return [(a, b) for a, b in zip(cells, cells[1:])]


# The dial's fair loop, on the side away from the well: out of the court's east
# side along its north row, down to the heart, west along the heart's row and
# back up into the court's south side -- a square with the dial and the heart at
# opposite corners, every pair of its opposite points beyond the hunter's hearing.
FAIR_RING = (_run([(8, 7)] + [(k, 7) for k in range(9, 14)] + [(13, j) for j in range(8, 13)])
             + _run([(12, 13)] + [(k, 13) for k in range(11, 6, -1)] + [(7, j) for j in range(12, 7, -1)]))


def forbidden_edges() -> set:
    """Every wall of the sundial court on its well side and of the well court
    that is not one of the ways designed above stays shut."""
    out = set()
    allowed = {frozenset(e) for e in CORRIDOR + WELL_EXITS}
    for court, sides in ((SUNDIAL, ((-1, 0), (0, -1))), (WELL, ((-1, 0), (0, -1), (1, 0), (0, 1)))):
        for k, j in court:
            for dk, dj in sides:
                o = (k + dk, j + dj)
                if o in court or not (0 <= o[0] < N and 0 <= o[1] < N):
                    continue
                e = frozenset(((k, j), o))
                if e not in allowed:
                    out.add(e)
    return out


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


def well_dist(c) -> float:
    return min(cell_dist(c, WELL_POINT), cell_dist(c, WELL_MOUTH))


def generate():
    rng = SplitMix64(MAZE_SEED)
    cells = [(k, j) for k in range(N) for j in range(N)]
    blocked = {frozenset(ab) for ab in BELLS.values()} | forbidden_edges()
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
    # the designed ways round the dial and the well
    for e in CORRIDOR + WELL_EXITS + FAIR_RING:
        a, b = (node_of(c) for c in e)
        if a == b:
            continue
        assert b in adj[a], e
        opened.add(frozenset(e))
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
        near = well_dist(n) <= HEAR
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
        assert well_dist(n) > HEAR, f"a dead end {n} stands within {HEAR} of the well"
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
    loop = fair_loop(g, centre)
    added = []
    if loop is None:
        # open the one closed wall near the dial that gives the shortest fair loop
        best = None
        for n in nodes:
            for o, es in sorted(adj[n].items(), key=lambda t: str(t[0])):
                for e in sorted(es):
                    fe = frozenset(e)
                    if fe in opened or math.dist(centre(n), centre("sundial")) > 30:
                        continue
                    a, b = node_of(e[0]), node_of(e[1])
                    g[a].add(b)
                    g[b].add(a)
                    cand = fair_loop(g, centre)
                    g[a].discard(b)
                    g[b].discard(a)
                    if cand is not None and (best is None or cand[0] < best[0][0]):
                        best = (cand, fe)
        assert best is not None, "no wall opens a fair loop through the sundial court"
        loop = best[0]
        opened.add(best[1])
        added.append(sorted(best[1]))
        a, b = (node_of(c) for c in best[1])
        g[a].add(b)
        g[b].add(a)
        edges = sum(len(v) for v in g.values()) // 2
        loops = edges - len(nodes) + 1
    length, cyc = loop
    # how far a runner leaving the dial along that loop runs before the well is out of earshot
    def out_after(c):
        walked = 0.0
        for i in range(1, len(c)):
            walked += math.dist(centre(c[i - 1]), centre(c[i]))
            if math.dist(centre(c[i]), (WELL_MOUTH[0] + 0.5, WELL_MOUTH[1] + 0.5)) > HEAR:
                return round(walked, 1)
        return None

    outs = [o for o in (out_after(cyc), out_after(list(reversed(cyc)))) if o is not None]
    run_out = min(outs) if outs else None
    print("maze.py: fair loop " + json.dumps([n if isinstance(n, str) else list(n) for n in cyc]), file=sys.stderr)
    assert run_out is not None and run_out <= 12, f"the fair loop leaves the well's hearing only after {run_out} blocks"
    sundial_ways = len(g["sundial"])
    assert sundial_ways >= 3, f"the sundial court has {sundial_ways} way(s) out"
    stats = {
        "sundial_ways_out": sundial_ways,
        "fair_loop_blocks": round(length, 1),
        "fair_loop_nodes": len(cyc) - 1,
        "fair_loop_out_of_well_hearing_after_blocks": run_out,
        "fair_loop_walls_opened_for_it": added,
        "cells": N * N,
        "nodes": len(nodes),
        "dead_ends_before_braid": len(dead0),
        "dead_ends_kept": len(kept),
        "independent_loops": loops,
        "fundamental_loops_opposite_points_beyond_16": wide,
        "kept_dead_end_distance_from_well": sorted(round(well_dist(n), 1) for n in kept),
    }
    return opened, stats


def fair_loop(g, centre):
    """The shortest loop through the sundial court that a runner can circle
    with the hunter kept out of earshot: it winds round a point, keeps a disk
    round that point clear, and every pair of its opposite points stands more
    than HEAR apart. (length, nodes) or None."""
    from collections import deque
    S = "sundial"
    sc = centre(S)
    # the loop leaves by the dial's own ways, never down the well's lane
    shut = {"well"} | {c for e in CORRIDOR for c in e if node_of(c) not in ("sundial", "well")}
    g = {n: {o for o in vs if o not in shut} for n, vs in g.items() if n not in shut}
    best = None
    # the designed ring first: a loop of the open walls, checked as any other
    ring = ["sundial"]
    for e in FAIR_RING:
        for c in e:
            n = node_of(c)
            if n != ring[-1]:
                ring.append(n)
    ring.append("sundial")
    if all(ring[i + 1] in g.get(ring[i], ()) for i in range(len(ring) - 1)):
        pts = [centre(n) for n in ring[:-1]]
        L = len(pts)
        if len(set(ring[:-1])) == L and all(math.dist(pts[i], pts[(i + L // 2) % L]) > HEAR for i in range(L)):
            best = (sum(math.dist(centre(ring[i]), centre(ring[i + 1])) for i in range(L)), ring)
    for a in range(0, 29):
        for b in range(0, 29):
            px, pz = 3 * a + 0.37, 3 * b + 0.61
            d = math.dist((px, pz), sc)
            if d > 24:
                continue
            for R in (6.5, 7.5, 8.5, 9.5, 11.0):
                if d < R:
                    continue
                found = _wind(g, centre, S, px, pz, R)
                if found is None:
                    continue
                length, cyc = found
                ring = cyc[:-1]
                pts = [centre(n) for n in ring]
                L = len(pts)
                if len(set(ring)) != L or L < 4:
                    continue
                if not all(math.dist(pts[i], pts[(i + L // 2) % L]) > HEAR for i in range(L)):
                    continue
                if best is None or length < best[0]:
                    best = (length, cyc)
    return best


def _wind(g, centre, S, px, pz, R):
    """The fewest-node closed walk from S winding once round (px, pz), every node outside radius R of it."""
    from collections import deque

    def cross(u, v):
        (xu, zu), (xv, zv) = centre(u), centre(v)
        if (zu - pz) * (zv - pz) >= 0:
            return 0
        xi = xu + (pz - zu) * (xv - xu) / (zv - zu)
        return 1 if xi > px else 0

    par = {(S, 0): None}
    q = deque([(S, 0)])
    while q:
        st = q.popleft()
        n, k = st
        for o in sorted(g[n], key=str):
            ns = (o, k ^ cross(n, o))
            if o == S:
                if ns[1] == 1 and par[st] is not None:
                    path = [st]
                    while par[path[-1]] is not None:
                        path.append(par[path[-1]])
                    cyc = [S] + [x[0] for x in reversed(path)][1:] + [S]
                    length = sum(math.dist(centre(cyc[i]), centre(cyc[i + 1])) for i in range(len(cyc) - 1))
                    return length, cyc
                continue
            if ns not in par and math.dist(centre(o), (px, pz)) >= R:
                par[ns] = st
                q.append(ns)
    return None


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
    P["rose"] = "minecraft:pink_concrete_powder"
    P["yellow"] = "minecraft:yellow_concrete_powder"
    P["blue"] = "minecraft:light_blue_concrete_powder"
    P["green"] = "minecraft:lime_concrete_powder"
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
    RING = 6  # the enclosing wall's hedge course: two over the lane walls' (4)
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
            if ring:
                # the garden's enclosing wall stands two courses over the lane
                # walls: a body that reached a lane wall's head could neither
                # step up onto it nor jump from it clear of the garden
                m.set(x, 0, z, "footing")
                m.box(x, x, 1, RING - 1, z, z, "wallstone")
                m.set(x, RING, z, "hedge")
                m.box(x, x, RING + 1, TOP, z, z, "minecraft:air")
            elif (x, z) not in open_cols:
                m.set(x, 0, z, "footing")
                m.box(x, x, 1, 3, z, z, "wallstone")
                m.set(x, 4, z, "hedge")
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

    # -- the old well (rose quarter, beyond the dial): a rim in the court's
    # dial-side corner, the grate in its middle, sculk spread over the floor --
    mx, mz = WELL_MOUTH
    for x in range(mx - 1, mx + 2):
        for z in range(mz - 1, mz + 2):
            m.set(x, 1, z, "rim")
    m.set(mx, 1, mz, trapdoor("iron", "north"))
    m.set(mx, 0, mz, "sculk")
    frame_to_mouth = math.dist(CRANK_FRAME, (mx, 1, mz))
    assert 10 <= frame_to_mouth <= 14, f"the well mouth stands {frame_to_mouth:.1f} from the crank's frame"
    vein = "minecraft:sculk_vein[down=true,east=false,north=false,south=false,up=false,waterlogged=false,west=false]"
    wx, wz = WELL_POINT
    rim = {(x, z) for x in range(mx - 1, mx + 2) for z in range(mz - 1, mz + 2)}
    sculk_floor = sorted({(x, z) for x in range(mx - 2, mx + 2) for z in range(mz - 1, mz + 3)} - rim) + [(13, 14), (13, 16), (15, 17), (17, 17)]
    for x, z in sculk_floor:
        assert (x, z) in open_cols and m.get(x, 1, z) is None, (x, z)
        m.set(x, 0, z, "sculk")
    for x, z in ((13, 13), (16, 17), (13, 17)):
        assert (x, z) in open_cols and m.get(x, 1, z) is None, (x, z)
        m.set(x, 1, z, vein)
    for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        x, z = wx + dx, wz + dz
        assert (x, z) in open_cols and m.get(x, 1, z) is None, f"the well's dig-out cell has a closed neighbour {x, z}"
    assert all(m.get(wx, y, wz) is None for y in (1, 2, 3))

    # -- the dial does not see the well: every sight line between their floors is walled --
    def court_cols(cells):
        xs = [x for k, _ in cells for x in lane(k)]
        zs = [z for _, j in cells for z in lane(j)]
        return [(x, z) for x in range(min(xs), max(xs) + 1) for z in range(min(zs), max(zs) + 1)]

    def seen(a, b) -> bool:
        (ax, az), (bx, bz) = a, b
        steps = int(math.dist(a, b) * 8) + 1
        for i in range(steps + 1):
            t = i / steps
            x, z = math.floor(ax + (bx - ax) * t), math.floor(az + (bz - az) * t)
            if (x, z) not in open_cols:
                return False
        return True

    offs = (0.05, 0.5, 0.95)
    sight = 0
    rays = 0
    for a in court_cols(SUNDIAL):
        for b in court_cols(WELL):
            for fa in offs:
                for fb in offs:
                    rays += 1
                    if seen((a[0] + fa, a[1] + fb), (b[0] + fb, b[1] + fa)):
                        sight += 1
    assert sight == 0, f"{sight} of {rays} sight line(s) from the dial's court reach the well's"
    stats["dial_to_well_sight_lines_open"] = f"{sight}/{rays}"

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
    m.mark("the-well", WELL_POINT[0], WELL_POINT[1], "east")
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

    # turns from the dial to the well, along the fewest cells between the courts
    from collections import deque as _dq
    start = sorted(SUNDIAL)[0]
    par = {start: None}
    q = _dq([start])
    while q:
        u = q.popleft()
        if u in WELL:
            break
        for dk, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            v = (u[0] + dk, u[1] + dj)
            if v in par or not (0 <= v[0] < N and 0 <= v[1] < N):
                continue
            same = node_of(u) == node_of(v) and isinstance(node_of(u), str)
            if same or frozenset((u, v)) in opened:
                par[v] = u
                q.appendleft(v) if same else q.append(v)
    cells_ = [u]
    while par[cells_[-1]] is not None:
        cells_.append(par[cells_[-1]])
    cells_.reverse()
    dirs = [(v[0] - u_[0], v[1] - u_[1]) for u_, v in zip(cells_, cells_[1:])
            if not (node_of(u_) == node_of(v) and isinstance(node_of(v), str))]
    rw = route_cells(m, sundial, WELL_POINT)
    turns = sum(1 for d0, d1 in zip(dirs, dirs[1:]) if d0 != d1)
    assert 2 <= turns <= 3, f"the well is {turns} turn(s) from the dial"
    stats["dial_to_well_turns"] = turns
    stats["dial_to_well_blocks"] = len(rw) - 1
    stats["crank_frame_to_well_mouth_blocks"] = round(frame_to_mouth, 1)

    # the way from the dial toward the heart and the gate leads away from the well
    def wd(c):
        return math.dist(c, WELL_MOUTH)

    dial_floor = set(court_cols(SUNDIAL))
    for name, path in (("heart", r1), ("gate", r2)):
        assert min(wd(c) for c in path if c not in dial_floor) >= wd(sundial) - 0.01, f"the way from the dial to the {name} passes the well"
    stats["dial_way_nearest_to_well_blocks"] = round(min(wd(c) for c in r1 + r2 if c not in dial_floor), 1)

    # the slimes: a junction on the way to the gate in the yellow quarter, out
    # of the dial's and the heart's reach, with a way round their reach
    from collections import deque

    def court_near(c, cells, r):
        return any(math.dist(c, q) <= r for q in court_cols(cells))

    def bypass(c, r) -> bool:
        def ok(x, z):
            return (x, z) in open_cols and 1 <= x <= 83 and 1 <= z <= 83 and math.dist((x, z), c) > r \
                and all(m.get(x, y, z) in (None, AIR) for y in (1, 2))
        seen_ = {sundial}
        q = deque([sundial])
        while q:
            u = q.popleft()
            if u == gate:
                return True
            for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                v = (u[0] + dx, u[1] + dz)
                if v not in seen_ and ok(*v):
                    seen_.add(v)
                    q.append(v)
        return False

    cand = [c for c in r2 if quarter(min((c[0] - 1) // 3, 27), min((c[1] - 1) // 3, 27)) == "yellow" and junction(c)
            and not court_near(c, SUNDIAL, HEAR + 1) and not court_near(c, HEART, HEAR + 1)]
    mid = len(cand) // 2
    cand = [c for _, c in sorted(enumerate(cand), key=lambda t: (abs(t[0] - mid), t[0]))]
    sy = next((c for c in cand if bypass(c, HEAR + 1)), None)
    assert sy is not None, "no junction on the way to the gate has a way round it"
    m.mark("slimes-yellow", sy[0], sy[1], "south")

    # -- what the generator asserts and prints --
    stats["route_heart_to_sundial_blocks"] = len(r1) - 1
    stats["route_sundial_to_gate_blocks"] = len(r2) - 1
    stats["slimes_yellow"] = sy
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
    # ring's open air over the 6-course wall (its top is floor no body reaches),
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
