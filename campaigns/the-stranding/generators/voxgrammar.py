"""Encode a designed voxel model as a grammar program (`delvec grammar`, document 1.10.0).

The place generators in this directory design each piece as a grid of block
states in the frame `delvec allocation` hands the place; this module writes
that grid as a program of nested splits (y courses, z rows, x runs), with the
spatial contract's claims and the anchors' marks on the runs that carry them.
Nothing here decides what a building looks like; it only writes it down.
"""

import json

VERSION = "1.10.0"
AIR = "minecraft:air"
VOID = "minecraft:structure_void"


def _abs(n):
    return {"size": "absolute", "blocks": {"expr": "int", "value": n}}


class Program:
    def __init__(self, name, extent):
        self.name = name
        self.X, self.Y, self.Z = extent
        self.cells = {}  # (x,y,z) -> block state ; absent = air
        self.region = {}  # (x,y,z) -> region name
        self.marks = {}  # (x,y,z) -> list of (stem, facing, role)
        self.contract = None
        self.shown_faces = None

    # -- authoring --------------------------------------------------------
    def inside(self, x, y, z):
        return 0 <= x < self.X and 0 <= y < self.Y and 0 <= z < self.Z

    def set(self, x, y, z, block):
        if self.inside(x, y, z):
            self.cells[(x, y, z)] = block

    def get(self, x, y, z):
        return self.cells.get((x, y, z), AIR)

    def box(self, x0, y0, z0, x1, y1, z1, block):
        for x in range(min(x0, x1), max(x0, x1) + 1):
            for y in range(min(y0, y1), max(y0, y1) + 1):
                for z in range(min(z0, z1), max(z0, z1) + 1):
                    self.set(x, y, z, block)

    def claim(self, x0, y0, z0, x1, y1, z1, name, only_air=False):
        for x in range(min(x0, x1), max(x0, x1) + 1):
            for y in range(min(y0, y1), max(y0, y1) + 1):
                for z in range(min(z0, z1), max(z0, z1) + 1):
                    if not self.inside(x, y, z):
                        continue
                    if only_air and self.get(x, y, z) != AIR:
                        continue
                    self.region[(x, y, z)] = name

    def mark(self, stem, x, y, z, facing=None, role=None):
        self.marks.setdefault((x, y, z), []).append((stem, facing, role))

    # -- emission ---------------------------------------------------------
    def to_json(self):
        roles = {}
        rules = {}
        rule_of_body = {}

        def role_for(block):
            if block not in roles:
                roles[block] = "b%d" % len(roles)
            return roles[block]

        def leaf(block, region, marks):
            if block == AIR:
                body = {"op": "void"}
            else:
                body = {"op": "fill", "material": {"role": role_for(block)}}
            if region:
                body = {"op": "claim", "region": region, "body": body}
            for stem, facing, role in sorted(marks or [], key=lambda m: m[0]):
                mk = {"anchor": stem, "at": "corner_min"}
                if facing:
                    mk["facing"] = facing
                if role:
                    mk["role"] = role
                body = {"op": "mark", "mark": mk, "body": body}
            return body

        def named(body):
            key = json.dumps(body, sort_keys=True)
            if key not in rule_of_body:
                nm = "r%d" % len(rule_of_body)
                rule_of_body[key] = nm
                rules[nm] = [{"weight": 1, "body": body}]
            return {"op": "call", "symbol": rule_of_body[key]}

        def row(y, z):
            runs = []
            x = 0
            while x < self.X:
                k = (x, y, z)
                sig = (self.get(*k), self.region.get(k))
                if k in self.marks:
                    runs.append((1, sig, self.marks[k]))
                    x += 1
                    continue
                n = 1
                while x + n < self.X:
                    k2 = (x + n, y, z)
                    if k2 in self.marks or (self.get(*k2), self.region.get(k2)) != sig:
                        break
                    n += 1
                runs.append((n, sig, None))
                x += n
            if len(runs) == 1:
                n, (b, r), m = runs[0]
                return named(leaf(b, r, m))
            return named({
                "op": "split", "axis": "x",
                "sizes": [_abs(n) for n, _, _ in runs],
                "children": [named(leaf(b, r, m)) for _, (b, r), m in runs],
            })

        def layer(y):
            rows = [row(y, z) for z in range(self.Z)]
            # merge equal consecutive rows
            groups = []
            for r in rows:
                if groups and groups[-1][1] == r:
                    groups[-1][0] += 1
                else:
                    groups.append([1, r])
            if len(groups) == 1:
                return groups[0][1]
            return named({
                "op": "split", "axis": "z",
                "sizes": [_abs(n) for n, _ in groups],
                "children": [r for _, r in groups],
            })

        layers = [layer(y) for y in range(self.Y)]
        groups = []
        for l in layers:
            if groups and groups[-1][1] == l:
                groups[-1][0] += 1
            else:
                groups.append([1, l])
        if len(groups) == 1:
            top = groups[0][1]
        else:
            top = {"op": "split", "axis": "y",
                   "sizes": [_abs(n) for n, _ in groups],
                   "children": [l for _, l in groups]}
        rules["piece"] = [{"weight": 1, "body": top}]
        doc = {
            "version": VERSION,
            "name": self.name,
            "start": "piece",
            "params": {},
            "palette": {r: b for b, r in roles.items()},
            "rules": rules,
        }
        if self.contract is not None:
            doc["contract"] = self.contract
        if self.shown_faces:
            doc["shown_faces"] = sorted(self.shown_faces)
        return doc

    def write(self, path):
        with open(path, "w") as f:
            json.dump(self.to_json(), f, indent=1, sort_keys=True)
            f.write("\n")
