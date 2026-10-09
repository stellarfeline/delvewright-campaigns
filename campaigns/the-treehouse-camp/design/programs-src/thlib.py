"""The Treehouse Camp's place programs: a voxel design written in world
coordinates, compiled into a box-split grammar program.

Each place script (`places.py`) draws its place into a `Model` with the
primitives below — boxes, stepped discs, lines — in WORLD coordinates, taken
from the place's handout (`delvec allocation <campaign> <place>`, read at run
time, never typed). The model then:

- completes every block state from the pinned registry and derives fence,
  pane and wall connections from the neighbouring cells (`DW0735`, `DW0737`);
- guillotine-cuts the frame around the contract's claimed regions, so each
  region is one `claim` scope;
- band-compresses everything else (identical y layers form a band, identical
  x slices a column, z runs a fill) and shares repeated subtrees as rules;
- writes the marks, the contract and `shown_faces`.

No randomness: the same design writes the same bytes.
"""
import json
import math
import os
import subprocess

ENGINE = os.environ.get("DELVEWRIGHT_ENGINE", "")
DATA = os.path.join(ENGINE, "crates", "dsl", "data")
_REG = None
_DEF = None


def registry():
    global _REG, _DEF
    if _REG is None:
        _REG = json.load(open(os.path.join(DATA, "blocks-1.21.11.json")))
        _DEF = json.load(open(os.path.join(DATA, "block-defaults-1.21.11.json")))
    return _REG, _DEF


def parse_state(s):
    if "[" in s:
        bid, rest = s.split("[", 1)
        props = dict(kv.split("=") for kv in rest.rstrip("]").split(",") if kv)
    else:
        bid, props = s, {}
    if ":" not in bid:
        bid = "minecraft:" + bid
    return bid, props


def full_state(s):
    reg, dfl = registry()
    bid, props = parse_state(s)
    if bid not in reg:
        raise SystemExit(f"unknown block {bid}")
    allowed = reg[bid]
    out = dict(dfl.get(bid, {}))
    for k, v in props.items():
        if k not in allowed or v not in allowed[k]:
            raise SystemExit(f"bad property {k}={v} on {bid}")
        out[k] = v
    if not out:
        return bid
    return bid + "[" + ",".join(f"{k}={out[k]}" for k in sorted(out)) + "]"


def bid_of(s):
    return parse_state(s)[0] if s else None


FENCE_LIKE = ("_fence", "iron_bars", "_pane", "_wall")
NON_SOLID_FOR_CONNECT = ("lantern", "ladder", "iron_chain", "carpet", "fern", "grass", "flower", "torch",
                         "leaves", "slab", "stairs", "trapdoor", "campfire", "button", "sapling", "vine",
                         "bush", "door", "composter", "loom", "lectern", "wool")


def is_fence_like(b):
    return b is not None and any(b.endswith(t) or t in b for t in FENCE_LIKE) and "fence_gate" not in b


def solid_for_connect(b):
    if b is None:
        return False
    if is_fence_like(b) or b.endswith("fence_gate"):
        return True
    return not any(t in b for t in NON_SOLID_FOR_CONNECT)


DIRS = {"north": (0, 0, -1), "south": (0, 0, 1), "east": (1, 0, 0), "west": (-1, 0, 0)}


class Model:
    def __init__(self, handout):
        self.h = handout
        self.min = handout["world_min"]
        self.ext = handout["extent"]
        self.cells = {}          # local (x,y,z) -> block state (None/absent = air)
        self.regions = {}        # name -> [local boxes]
        self.spaces = {}
        self.no_body = {}
        self.edges = []
        self.entry = None
        self.marks = []

    # -- coordinates -------------------------------------------------------
    def inside_w(self, x, y, z):
        lx, ly, lz = x - self.min[0], y - self.min[1], z - self.min[2]
        return 0 <= lx < self.ext[0] and 0 <= ly < self.ext[1] and 0 <= lz < self.ext[2]

    def wmax(self):
        return [self.min[i] + self.ext[i] - 1 for i in range(3)]

    # -- drawing (world coordinates; cells outside the frame are skipped) ---
    def set(self, x, y, z, block):
        if not self.inside_w(x, y, z):
            return
        key = (x - self.min[0], y - self.min[1], z - self.min[2])
        if block is None or block == "air":
            self.cells.pop(key, None)
        else:
            self.cells[key] = block

    def get(self, x, y, z):
        return self.cells.get((x - self.min[0], y - self.min[1], z - self.min[2]))

    def box(self, x0, y0, z0, x1, y1, z1, block, only_air=False):
        for x in range(min(x0, x1), max(x0, x1) + 1):
            for y in range(min(y0, y1), max(y0, y1) + 1):
                for z in range(min(z0, z1), max(z0, z1) + 1):
                    if only_air and self.get(x, y, z) is not None:
                        continue
                    self.set(x, y, z, block)

    def disc_cells(self, cx, cz, r):
        out = []
        for x in range(math.floor(cx - r - 1), math.ceil(cx + r + 1)):
            for z in range(math.floor(cz - r - 1), math.ceil(cz + r + 1)):
                if (x + 0.5 - cx) ** 2 + (z + 0.5 - cz) ** 2 <= r * r + 1e-9:
                    out.append((x, z))
        return out

    def disc(self, cx, cz, r, y, block, only_air=False):
        for x, z in self.disc_cells(cx, cz, r):
            if only_air and self.get(x, y, z) is not None:
                continue
            self.set(x, y, z, block)

    def ring(self, cx, cz, r_in, r_out, y, block, only_air=False):
        inner = set(self.disc_cells(cx, cz, r_in))
        for x, z in self.disc_cells(cx, cz, r_out):
            if (x, z) in inner:
                continue
            if only_air and self.get(x, y, z) is not None:
                continue
            self.set(x, y, z, block)

    def pick(self, x, y, z, choices, salt=0):
        """A deterministic per-cell choice from a weighted list [(w, block)]."""
        h = (x * 73856093) ^ (y * 19349663) ^ (z * 83492791) ^ (salt * 2654435761)
        h &= 0xFFFFFFFF
        h = ((h ^ (h >> 15)) * 2246822519) & 0xFFFFFFFF
        tot = sum(w for w, _ in choices)
        r = h % tot
        for w, b in choices:
            if r < w:
                return b
            r -= w
        return choices[-1][1]

    # -- contract ------------------------------------------------------------
    def region(self, name, x0, y0, z0, x1, y1, z1):
        b = (min(x0, x1) - self.min[0], min(y0, y1) - self.min[1], min(z0, z1) - self.min[2],
             max(x0, x1) - self.min[0], max(y0, y1) - self.min[1], max(z0, z1) - self.min[2])
        for i in range(3):
            lo, hi = b[i], b[i + 3]
            lo, hi = max(lo, 0), min(hi, self.ext[i] - 1)
            b = b[:i] + (lo,) + b[i + 1:i + 3] + (hi,) + b[i + 4:]
        self.regions.setdefault(name, []).append(b)

    def space(self, name, envelope, *boxes):
        self.spaces[name] = {"envelope": envelope}
        for bx in boxes:
            self.region(name, *bx)

    def nobody(self, name, reason, *boxes):
        self.no_body[name] = {"reason": reason}
        for bx in boxes:
            self.region(name, *bx)

    def via(self, name, *boxes):
        for bx in boxes:
            self.region(name, *bx)

    def edge(self, **e):
        self.edges.append(e)

    def mark(self, stem, x, y, z, facing, role=None):
        self.marks.append((stem, x - self.min[0], y - self.min[1], z - self.min[2], facing, role))

    # -- finishing -------------------------------------------------------------
    def finalize(self):
        # Fence-like connections from the neighbours, then complete every state.
        done = {}
        for k, s in self.cells.items():
            bid, props = parse_state(s)
            if is_fence_like(bid):
                reg, _ = registry()
                for d, (dx, dy, dz) in DIRS.items():
                    if d in reg[bid]:
                        nb = self.cells.get((k[0] + dx, k[1] + dy, k[2] + dz))
                        nbid = bid_of(nb)
                        conn = solid_for_connect(nbid) if nbid else False
                        if "fence" in bid and nbid and not ("fence" in nbid) and is_fence_like(nbid):
                            conn = False
                        if "_wall" in bid:
                            props[d] = "low" if conn else "none"
                        else:
                            props[d] = "true" if conn else "false"
                if "_wall" in bid and "up" in reg[bid]:
                    props["up"] = "true"
                s = bid + ("[" + ",".join(f"{a}={b}" for a, b in props.items()) + "]" if props else "")
            done[k] = full_state(s)
        self.cells = done

    def shown_faces(self):
        X, Y, Z = self.ext
        faces = []
        tests = {
            "west": lambda k: k[0] == 0, "east": lambda k: k[0] == X - 1,
            "north": lambda k: k[2] == 0, "south": lambda k: k[2] == Z - 1,
            "up": lambda k: k[1] == Y - 1,
        }
        for f, t in tests.items():
            if any(t(k) for k in self.cells):
                faces.append(f)
        return sorted(faces)

    # -- compilation -------------------------------------------------------
    def program(self, name):
        self.finalize()
        roles = {}

        def role(state):
            if state not in roles:
                bid, props = parse_state(state)
                base = bid.split(":")[1].replace("_", "-")
                n = sum(1 for r in roles.values() if r.startswith(base))
                roles[state] = base if n == 0 else f"{base}-{n + 1}"
            return roles[state]

        rules = {}
        memo = {}

        def share(node):
            key = json.dumps(node, sort_keys=True)
            if len(key) < 120:
                return node
            if key not in memo:
                rname = f"part-{len(memo) + 1}"
                memo[key] = rname
                rules[rname] = [{"weight": 1, "body": node}]
            return {"op": "call", "symbol": memo[key]}

        def ab(n):
            return {"size": "absolute", "blocks": {"expr": "int", "value": n}}

        def split(axis, sizes, children):
            if len(children) == 1:
                return children[0]
            return {"op": "split", "axis": axis, "sizes": [ab(n) for n in sizes], "children": children}

        def fill(state):
            if state is None:
                return {"op": "void"}
            return {"op": "fill", "material": {"role": role(state)}}

        def column(x, y, z0, z1):
            runs = []
            for z in range(z0, z1 + 1):
                s = self.cells.get((x, y, z))
                if runs and runs[-1][0] == s:
                    runs[-1][1] += 1
                else:
                    runs.append([s, 1])
            return share(split("z", [n for _, n in runs], [fill(s) for s, _ in runs]))

        def band(bx, y):
            x0, _, z0, x1, _, z1 = bx
            groups = []
            for x in range(x0, x1 + 1):
                key = tuple(self.cells.get((x, y, z)) for z in range(z0, z1 + 1))
                if groups and groups[-1][0] == key:
                    groups[-1][1] += 1
                else:
                    groups.append([key, 1, x])
            return share(split("x", [n for _, n, _ in groups], [column(gx, y, z0, z1) for _, _, gx in groups]))

        def voxel(bx):
            x0, y0, z0, x1, y1, z1 = bx
            groups = []
            for y in range(y0, y1 + 1):
                key = tuple(self.cells.get((x, y, z)) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1))
                if groups and groups[-1][0] == key:
                    groups[-1][1] += 1
                else:
                    groups.append([key, 1, y])
            return share(split("y", [n for _, n, _ in groups], [band(bx, gy) for _, _, gy in groups]))

        regs = [(n, b) for n, bs in self.regions.items() for b in bs]

        def inside(b, bx):
            return all(bx[i] <= b[i] and b[i + 3] <= bx[i + 3] for i in range(3))

        def compile_scope(bx, rs):
            if not rs:
                return voxel(bx)
            if len(rs) == 1 and rs[0][1] == bx:
                return {"op": "claim", "region": rs[0][0], "body": voxel(bx)}
            for ai, axis in enumerate("xyz"):
                planes = sorted({p for _, b in rs for p in (b[ai], b[ai + 3] + 1) if bx[ai] < p <= bx[ai + 3]})
                for p in planes:
                    if any(b[ai] < p <= b[ai + 3] for _, b in rs):
                        continue
                    lo = list(bx); lo[ai + 3] = p - 1
                    hi = list(bx); hi[ai] = p
                    lo, hi = tuple(lo), tuple(hi)
                    rl = [r for r in rs if inside(r[1], lo)]
                    rh = [r for r in rs if inside(r[1], hi)]
                    assert len(rl) + len(rh) == len(rs)
                    return split(axis, [p - bx[ai], bx[ai + 3] - p + 1],
                                 [compile_scope(lo, rl), compile_scope(hi, rh)])
            raise SystemExit(f"{name}: regions not separable by a plane inside {bx}: {[r[0] for r in rs]}")

        root = (0, 0, 0, self.ext[0] - 1, self.ext[1] - 1, self.ext[2] - 1)
        for n, b in regs:
            if not inside(b, root):
                raise SystemExit(f"{name}: region {n} leaves the frame: {b}")
        for i, (n1, b1) in enumerate(regs):
            for n2, b2 in regs[i + 1:]:
                if all(b1[k] <= b2[k + 3] and b2[k] <= b1[k + 3] for k in range(3)):
                    raise SystemExit(f"{name}: regions overlap: {n1} {b1} / {n2} {b2}")
        body = compile_scope(root, regs)
        for stem, x, y, z, facing, r in reversed(self.marks):
            m = {"anchor": stem, "at": "offset", "facing": facing,
                 "x": {"expr": "int", "value": x}, "y": {"expr": "int", "value": y}, "z": {"expr": "int", "value": z}}
            if r:
                m["role"] = r
            body = {"op": "mark", "mark": m, "body": body}
        rules["place"] = [{"weight": 1, "body": body}]
        prog = {
            "version": "1.9.0", "name": name, "start": "place", "params": {},
            "palette": {r: s for s, r in roles.items()},
            "rules": rules,
            "contract": {"entry": self.entry, "spaces": self.spaces, "edges": self.edges},
            "shown_faces": self.shown_faces(),
        }
        if self.no_body:
            prog["contract"]["no_body"] = self.no_body
        return prog


def handout(campaign, place, prefabs):
    delvec = os.environ.get("D", "delvec")
    out = subprocess.run([delvec, "--prefabs", prefabs, "allocation", campaign, place],
                         check=True, capture_output=True, text=True).stdout
    return json.loads(out)
