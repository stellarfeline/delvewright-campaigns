"""The Listening Hall's three place programs, written from each place's handout.

Each place is drawn as a voxel design in the place's own frame (local cells,
read from `delvec allocation <campaign> <place>` at run time and never typed),
then compiled into a box-split grammar program: the frame is cut along the
contract's claimed regions (so each region is one `claim` scope), and every
other box is cut into y layers, x columns and z runs. A cell another owner
holds (the handout's `voids`) is written as `skip`, never painted.

Run from the campaign directory with `delvec` on PATH:

    python3 design/programs-src/rooms.py

It writes `programs/<place stem>.json`. No randomness: the same handouts write
the same bytes.
"""
import json
import os
import subprocess
import sys

CAMPAIGN = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PREFABS = os.environ.get("DELVEWRIGHT_PREFABS", "")
SKIP = "<skip>"

FLOOR = "minecraft:deepslate_tiles"
EDGE = "minecraft:polished_deepslate"
WALL = "minecraft:deepslate_bricks"
PILASTER = "minecraft:chiseled_deepslate"
CEILING = "minecraft:deepslate_bricks"
LINTEL = "minecraft:polished_deepslate"


def handout(place):
    cmd = ["delvec"] + (["--prefabs", PREFABS] if PREFABS else []) + ["allocation", CAMPAIGN, place]
    out = subprocess.run(cmd, check=True, capture_output=True, text=True).stdout
    return json.loads(out)


class Room:
    def __init__(self, h):
        self.h = h
        self.ext = h["extent"]
        self.cells = {}
        self.regions = {}
        self.marks = []
        X, Y, Z = self.ext
        for x in range(X):
            for y in range(Y):
                for z in range(Z):
                    self.cells[(x, y, z)] = None
        for v in h["voids"]:
            (x0, y0, z0), (x1, y1, z1) = v["cells"]
            for x in range(x0, x1 + 1):
                for y in range(y0, y1 + 1):
                    for z in range(z0, z1 + 1):
                        self.cells[(x, y, z)] = SKIP

    def set(self, x, y, z, block):
        if self.cells.get((x, y, z), SKIP) is SKIP:
            return
        self.cells[(x, y, z)] = block

    def box(self, a, b, block):
        for x in range(min(a[0], b[0]), max(a[0], b[0]) + 1):
            for y in range(min(a[1], b[1]), max(a[1], b[1]) + 1):
                for z in range(min(a[2], b[2]), max(a[2], b[2]) + 1):
                    self.set(x, y, z, block)

    def claim(self, name, a, b):
        self.regions.setdefault(name, []).append(
            tuple(min(a[i], b[i]) for i in range(3)) + tuple(max(a[i], b[i]) for i in range(3)))

    def shell(self):
        """Floor course, walls on the ring, ceiling course; the play space air."""
        X, Y, Z = self.ext
        (sx0, sy0, sz0), (sx1, sy1, sz1) = self.h["space"]
        for x in range(X):
            for y in range(Y):
                for z in range(Z):
                    inside = sx0 <= x <= sx1 and sz0 <= z <= sz1
                    if y < sy0:
                        self.set(x, y, z, FLOOR if inside else WALL)
                    elif y > sy1:
                        self.set(x, y, z, CEILING)
                    elif not inside:
                        self.set(x, y, z, WALL)
        return (sx0, sy0, sz0), (sx1, sy1, sz1)

    def seam(self, s):
        """Open the handed cells, and claim them as the opening."""
        (x0, y0, z0), (x1, y1, z1) = s["cells"]
        self.box((x0, y0, z0), (x1, y1, z1), None)
        stem = s["edge"].split("/", 1)[1]
        self.claim(stem, (x0, y0, z0), (x1, y1, z1))
        return stem, ((x0, y0, z0), (x1, y1, z1))

    def space(self, name, a, b, holes):
        """Claim the play space `a..b` minus the opening boxes inside it."""
        for bx in subtract(tuple(a) + tuple(b), [tuple(h[0]) + tuple(h[1]) for h in holes]):
            self.claim(name, bx[:3], bx[3:])

    def mark(self, stem, x, y, z, facing, role=None):
        self.marks.append((stem, x, y, z, facing, role))

    def program(self, name, contract):
        roles = {}

        def role(state):
            if state not in roles:
                base = state.split(":")[1].split("[")[0].replace("_", "-")
                n = sum(1 for r in roles.values() if r == base or r.startswith(base + "-"))
                roles[state] = base if n == 0 else f"{base}-{n + 1}"
            return roles[state]

        def ab(n):
            return {"size": "absolute", "blocks": {"expr": "int", "value": n}}

        def split(axis, runs):
            if len(runs) == 1:
                return runs[0][1]
            return {"op": "split", "axis": axis, "sizes": [ab(n) for n, _ in runs],
                    "children": [c for _, c in runs]}

        def leaf(s):
            if s is SKIP:
                return {"op": "skip"}
            if s is None:
                return {"op": "void"}
            return {"op": "fill", "material": {"role": role(s)}}

        def runs_of(keys, make):
            out = []
            for k in keys:
                if out and out[-1][0] == k[0]:
                    out[-1][1] += 1
                else:
                    out.append([k[0], 1, k[1]])
            return [(n, make(arg)) for _, n, arg in out]

        def voxel(bx):
            x0, y0, z0, x1, y1, z1 = bx

            def column(xy):
                x, y = xy
                return split("z", runs_of([(self.cells[(x, y, z)], z) for z in range(z0, z1 + 1)],
                                          lambda z, x=x, y=y: leaf(self.cells[(x, y, z)])))

            def layer(y):
                keys = [(tuple(self.cells[(x, y, z)] for z in range(z0, z1 + 1)), x) for x in range(x0, x1 + 1)]
                return split("x", runs_of(keys, lambda x, y=y: column((x, y))))

            keys = [(tuple(self.cells[(x, y, z)] for x in range(x0, x1 + 1) for z in range(z0, z1 + 1)), y)
                    for y in range(y0, y1 + 1)]
            return split("y", runs_of(keys, layer))

        def inside(b, bx):
            return all(bx[i] <= b[i] and b[i + 3] <= bx[i + 3] for i in range(3))

        def scope(bx, rs):
            if not rs:
                return voxel(bx)
            if len(rs) == 1 and rs[0][1] == bx:
                return {"op": "claim", "region": rs[0][0], "body": voxel(bx)}
            for ai, axis in enumerate("xyz"):
                for p in sorted({p for _, b in rs for p in (b[ai], b[ai + 3] + 1) if bx[ai] < p <= bx[ai + 3]}):
                    if any(b[ai] < p <= b[ai + 3] for _, b in rs):
                        continue
                    lo = list(bx); lo[ai + 3] = p - 1
                    hi = list(bx); hi[ai] = p
                    rl = [r for r in rs if inside(r[1], tuple(lo))]
                    rh = [r for r in rs if inside(r[1], tuple(hi))]
                    return split(axis, [(p - bx[ai], scope(tuple(lo), rl)), (bx[ai + 3] - p + 1, scope(tuple(hi), rh))])
            raise SystemExit(f"{name}: regions inside {bx} are not guillotine-separable: {[r[0] for r in rs]}")

        X, Y, Z = self.ext
        regs = [(n, b) for n, bs in sorted(self.regions.items()) for b in bs]
        body = scope((0, 0, 0, X - 1, Y - 1, Z - 1), regs)
        for stem, x, y, z, facing, r in reversed(self.marks):
            m = {"anchor": stem, "at": "offset", "facing": facing,
                 "x": {"expr": "int", "value": x}, "y": {"expr": "int", "value": y}, "z": {"expr": "int", "value": z}}
            if r:
                m["role"] = r
            body = {"op": "mark", "mark": m, "body": body}
        return {
            "version": "1.10.0",
            "name": name,
            "start": "place",
            "params": {},
            "palette": {r: s for s, r in sorted(roles.items(), key=lambda kv: kv[1])},
            "rules": {"place": [{"weight": 1, "body": body}]},
            "contract": contract,
        }


def subtract(box, holes):
    """Disjoint boxes covering `box` minus `holes`, cut along the holes' faces."""
    for h in holes:
        if all(box[i] <= h[i + 3] and h[i] <= box[i + 3] for i in range(3)):
            break
    else:
        return [box]
    out = []
    lo, hi = list(box[:3]), list(box[3:])
    for i in range(3):
        if lo[i] < h[i]:
            piece = lo[:] + hi[:]; piece[i + 3] = h[i] - 1
            out.append(tuple(piece)); lo[i] = h[i]
        if hi[i] > h[i + 3]:
            piece = lo[:] + hi[:]; piece[i] = h[i + 3] + 1
            out.append(tuple(piece)); hi[i] = h[i + 3]
    rest = [hh for hh in holes if hh is not h]
    return [b for p in out for b in subtract(p, rest)]


def edges_to_exterior(space, openings):
    return [{"a": "exterior", "b": space, "class": "walk", "via": stem} for stem in openings]


def hall():
    h = handout("node/hall")
    r = Room(h)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = r.shell()
    # Pilasters of chiseled deepslate in both long walls, every four blocks,
    # and a polished course along the floor's two edges, where the sensors sit.
    for z in range(sz0 + 1, sz1 + 1, 4):
        r.box((sx0 - 1, sy0, z), (sx0 - 1, sy1, z), PILASTER)
        r.box((sx1 + 1, sy0, z), (sx1 + 1, sy1, z), PILASTER)
    r.box((sx0, sy0 - 1, sz0), (sx0, sy0 - 1, sz1), EDGE)
    r.box((sx1, sy0 - 1, sz0), (sx1, sy0 - 1, sz1), EDGE)
    holes, names = [], []
    for s in h["seams"]:
        stem, cells = r.seam(s)
        names.append(stem)
        holes.append(cells)
    r.space("hall", (sx0, sy0, sz0), (sx1, sy1, sz1), [c for c in holes
                                                       if all(sx0 <= c[0][i] <= sx1 for i in (0,)) and sz0 <= c[0][2] <= sz1])
    cx, cz = (sx0 + sx1) // 2, (sz0 + sz1) // 2
    r.mark("node-hall", cx, sy0, cz, "north")
    return r.program("the-listening-hall-hall", {
        "entry": "hall", "spaces": {"hall": {"envelope": "enclosed"}}, "edges": edges_to_exterior("hall", names)})


def antechamber():
    h = handout("node/antechamber")
    r = Room(h)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = r.shell()
    r.box((sx0, sy0 - 1, sz0), (sx1, sy0 - 1, sz0), EDGE)
    names, holes = [], []
    for s in h["seams"]:
        stem, cells = r.seam(s)
        names.append(stem)
        holes.append(cells)
        # A lintel of polished deepslate over the doorway.
        (x0, _, z0), (x1, y1, _) = cells
        r.box((x0 - 1, y1 + 1, z0), (x1 + 1, y1 + 1, z0), LINTEL)
    r.space("antechamber", (sx0, sy0, sz0), (sx1, sy1, sz1), [])
    cx, cz = (sx0 + sx1) // 2, (sz0 + sz1) // 2
    r.mark("node-antechamber", cx, sy0, cz, "north")
    r.mark("spawn", cx, sy0, cz, "north", role="entry")
    return r.program("the-listening-hall-antechamber", {
        "entry": "antechamber", "spaces": {"antechamber": {"envelope": "enclosed"}},
        "edges": edges_to_exterior("antechamber", names)})


def far_door():
    h = handout("node/far-door")
    r = Room(h)
    (sx0, sy0, sz0), (sx1, sy1, sz1) = r.shell()
    names, holes = [], []
    for s in h["seams"]:
        stem, cells = r.seam(s)
        names.append(stem)
        holes.append(cells)
    r.space("alcove", (sx0, sy0, sz0), (sx1, sy1, sz1), holes)
    cx, cz = (sx0 + sx1) // 2, (sz0 + sz1) // 2
    r.mark("node-far-door", cx, sy0, cz, "north")
    return r.program("the-listening-hall-far-door", {
        "entry": "alcove", "spaces": {"alcove": {"envelope": "enclosed"}}, "edges": edges_to_exterior("alcove", names)})


def main():
    os.makedirs(os.path.join(CAMPAIGN, "programs"), exist_ok=True)
    wanted = sys.argv[1:] or ["hall", "antechamber", "far-door"]
    for stem, make in (("hall", hall), ("antechamber", antechamber), ("far-door", far_door)):
        if stem not in wanted:
            continue
        prog = make()
        path = os.path.join(CAMPAIGN, "programs", f"{stem}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(prog, f, indent=2)
            f.write("\n")
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
