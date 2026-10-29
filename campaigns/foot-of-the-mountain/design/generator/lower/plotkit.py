#!/usr/bin/env python3
"""The lower street's plot kit: the skill's starter, plus a voxel model a plot module fills.

The first part is the starter `scripts/handout.py` copies beside every
handout, verbatim: it reads the place's allocation and binds the handing.
The second part (after the rule) is the cathedral generator's way of
building into it: a plot module draws its buildings, yards and life as a
voxel model in piece-local coordinates and names each part's columns; the
kit turns the model into the place's cells, claims what a body reaches into
the part it stands in, and claims what no body reaches as `unwalked`.

Standard library only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys

LAMP_PERIOD = 4  # one sconce (and one ceiling lamp) in four cells; yours to change

# ── BUILD HERE: the palette. Every role below is a name the rules paint; bind
# each to the material the design names (references/new-pieces.md step 2 —
# measure a block's colour, never guess it). A role the whole's palette names
# (`role/<stem>` in detail-plan.json) is rebound to it by `delvec detail`.
PALETTE = {
    "floor": "minecraft:stone_bricks",
    "wall": "minecraft:stone_bricks",
    "lid": "minecraft:spruce_planks",
    "lamp": "minecraft:sea_lantern",
}


# ---- the grammar's expression and operation vocabulary (grammar.md §2) ----


def num(v: int) -> dict:
    return {"expr": "int", "value": v}


def par(name: str) -> dict:
    return {"expr": "param", "name": name}


def arith(lhs: dict, op: str, rhs: dict) -> dict:
    return {"expr": "arith", "lhs": lhs, "op": op, "rhs": rhs}


def fill(role: str) -> dict:
    return {"material": {"role": role}, "op": "fill"}


VOID = {"op": "void"}


def claim(region: str, body: dict) -> dict:
    return {"body": body, "op": "claim", "region": region}


# ---- a value the program reads: a handed parameter, or this starter's literal ----


class Bound:
    """A coordinate on one axis: its value now, and how the program spells it."""

    def __init__(self, value: int, expr: dict, handed: bool) -> None:
        self.value, self.expr, self.handed = value, expr, handed

    def plus(self, n: int) -> "Bound":
        if n == 0:
            return self
        if self.expr.get("expr") == "int":
            return lit(self.value + n)
        return Bound(self.value + n, arith(self.expr, "add" if n > 0 else "sub", num(abs(n))), self.handed)


def lit(v: int) -> Bound:
    return Bound(v, num(v), False)


class Handed:
    """The handed values this program declares — each read only through its parameter."""

    def __init__(self) -> None:
        self.params: dict[str, int] = {}

    def __call__(self, name: str, value: int) -> Bound:
        key = f"handed/{name}"
        self.params[key] = value
        return Bound(value, par(key), True)


# ---- the place, read off the allocation ----


FACES = {"west": (0, -1), "east": (0, 1), "down": (1, -1), "up": (1, 1), "north": (2, -1), "south": (2, 1)}


class Place:
    def __init__(self, a: dict) -> None:
        self.a = a
        self.h = Handed()
        self.n = list(a["extent"])
        self.ex, self.ey, self.ez = self.n
        self.space = a["space"]
        self.datum = self.h("datum-y", a["datum_y"])
        self.aloft = isinstance(a["ground"].get("base"), dict)
        roof = a.get("roof")
        self.roofed = roof is not None or a.get("brief", {}).get("kind") == "roofed"
        if roof is not None:
            self.lid = self.h("roof/lid-y", roof["lid_y"])
        elif self.roofed:
            self.lid = lit(self.ey - 1)
        else:
            self.lid = None
        # The walls stand on the cells just outside the play space, from the
        # walk plane to the lid — or, open to the sky, to the top of the play
        # space. Outside them (the eaves the plan reserves) is air.
        self.wall_top = self.lid if self.lid is not None else lit(self.space[1][1] + 1)
        self.seams = []
        for s in a["seams"]:
            stem = s["edge"].removeprefix("edge/")
            (x0, y0, z0), (x1, y1, z1) = s["cells"]
            lo = [self.h(f"seam/{stem}/{k}", v) for k, v in (("x0", x0), ("y0", y0), ("z0", z0))]
            hi = [self.h(f"seam/{stem}/{k}", v).plus(1) for k, v in (("x1", x1), ("y1", y1), ("z1", z1))]
            axis, sign = FACES[s["face"]]
            bar = None
            if s.get("bar") is not None:
                (bx0, by0, bz0), (bx1, by1, bz1) = s["bar"]
                bar = ([bx0, by0, bz0], [bx1 + 1, by1 + 1, bz1 + 1])
            seam = {"stem": stem, "lo": lo, "hi": hi, "seam": s, "bar": bar, "axis": axis, "approach": None}
            seam["approach"] = self.approach(seam, sign)
            self.seams.append(seam)
        # Every side the place declares open (spec-0123 §5.3): its ring run at
        # the walk plane, corners excluded, piece-local and inclusive.
        self.sides = []
        for s in a.get("sides", []) or []:
            (sx0, _, sz0), (sx1, _, sz1) = s["cells"]
            self.sides.append({"face": s["face"], "lo": (sx0, sz0), "hi": (sx1, sz1)})
        self.scenery = a.get("brief", {}).get("reached") is False
        # A station of kind `gate` is a volume that seals and clears, so it is
        # answered by a region, never a mark: a grille of bars in front of a
        # one-cell alcove against the play space's north wall, joined to the
        # room by a `barred` edge whose bar is that region.
        self.gates: list[dict] = []
        for st in a.get("brief", {}).get("stations", []) or []:
            name, _, kind = st.partition(" (")
            if kind.rstrip(")") != "gate":
                continue
            self.gates.append(self.place_gate(name.removeprefix("anchor/")))
        # A plot's parts (spec-0125 §5.1): the allocation's `parts`, each laid
        # as a region of its declared cells, named for the part.
        self.parts: list[dict] = []
        self.col_part: dict[tuple[int, int], dict] = {}
        self.lay_parts(a.get("parts", []) or [])

    def approach(self, seam: dict, sign: int) -> dict | None:
        """How a body reaches an opening above the walk plane, or None.

        A sideways opening whose sill stands above the floor, or a hole in the
        lid, is reached from a pillar of masonry under it: one course high it is
        a step, higher it carries a landing (its own space) and a ladder up its
        side, joined to the room by a `climb` edge. A hole in the floor needs
        nothing: a body drops through it.
        """
        s, lo, hi, axis = seam["seam"], seam["lo"], seam["hi"], seam["axis"]
        d = self.datum.value
        if axis == 1:
            if sign < 0:
                return None
            sill = lo[1].plus(-1)
            plo, phi = [lo[0], None, lo[2]], [hi[0], None, hi[2]]
            top = lo[1]
            # the ladder stands on the pillar's side toward the room's middle
            cx = (self.space[0][0] + self.space[1][0]) // 2
            lax, ldir = 0, (1 if cx >= lo[0].value else -1)
        else:
            if lo[1].value <= d:
                return None
            sill = lo[1]
            inward = -sign
            plo, phi = list(lo), list(hi)
            if inward > 0:
                plo[axis] = lo[axis].plus(1) if s["owns_plane"] else lo[axis]
                phi[axis] = plo[axis].plus(2)
            else:
                phi[axis] = hi[axis].plus(-1) if s["owns_plane"] else hi[axis]
                plo[axis] = phi[axis].plus(-2)
            top = hi[1]
            lax, ldir = axis, inward
        rise = sill.value - d
        if rise <= 0:
            return None
        out = {"plo": plo, "phi": phi, "sill": sill, "top": top, "rise": rise, "ladder": None}
        if rise > 1:
            other = 2 if lax == 0 else 0
            mid = (plo[other].value + phi[other].value - 1) // 2
            at = (phi[lax].value if ldir > 0 else plo[lax].value - 1)
            facing = {(0, 1): "east", (0, -1): "west", (2, 1): "south", (2, -1): "north"}[(lax, ldir)]
            cell_lo, cell_hi = [0, 0, 0], [0, 0, 0]
            cell_lo[lax], cell_hi[lax] = at, at + 1
            cell_lo[other], cell_hi[other] = mid, mid + 1
            out["ladder"] = {"lo": cell_lo, "hi": cell_hi, "facing": facing}
        return out

    def place_gate(self, stem: str) -> dict:
        lo, hi = self.space
        d = self.datum.value
        z = lo[2]
        for x in range(hi[0] - 1, lo[0], -1):
            cells = [(x2, y, zz) for x2 in (x - 1, x, x + 1) for y in (d, d + 1) for zz in (z, z + 1, z + 2)]
            if all(self.cell(*c) == ("claim", "room", None) for c in cells):
                g = {"stem": stem, "lo": [x, d, z], "hi": [x + 1, d + 2, z + 2], "x": x, "z": z}
                return g
        sys.exit(f"starter.py: no room against the north wall for the gate station `{stem}`; place it by hand")

    def lay_parts(self, parts: list[dict]) -> None:
        """Lay each part as a region of exactly its declared cells.

        The columns beside every opening, ladder, landing and gate, and the
        middle of every open side, stay the `room`, so every edge the room declares keeps its cells; the
        rest of the play space is walked in rows, a part a body walks taking
        the next run of its `cells` columns and a part seen and never entered
        taking columns from the far end, an out-of-walk region over the floor
        no edge reaches, only where the walked floor stays one piece. Where
        the parts stand is this starter's choice and yours to change; the
        counts are the plan's.
        """
        if not parts:
            return
        lo, hi = self.space
        d = self.datum.value
        top = self.lid.value if self.lid is not None else self.wall_top.value
        plain = {("claim", "room", None), ("claim", "roof", None), ("fill", "floor"), ("fill", "wall"), ("fill", "lid"), ("fill", "lamp"), ("void",)}
        special = set()
        for x in range(lo[0] - 1, hi[0] + 2):
            for z in range(lo[2] - 1, hi[2] + 2):
                kinds = {self.cell(x, y, z) for y in range(d - 1, top + 1)} - plain
                # An open side's run is a way out along a whole side: the room
                # keeps the column inside its middle cell, and the parts may
                # stand along the rest of it.
                if kinds and not all(k[0] == "claim" and k[1].startswith("side-") for k in kinds):
                    special.add((x, z))
        room = ("claim", "room", None)
        floor = {
            (x, z)
            for x in range(lo[0], hi[0] + 1)
            for z in range(lo[2], hi[2] + 1)
            if self.cell(x, d, z) == room and self.cell(x, d + 1, z) == room
        }
        # A pillar, a ladder, an alcove: a column of the play space that is
        # not open floor is as special as an opening.
        special |= {(x, z) for x in range(lo[0], hi[0] + 1) for z in range(lo[2], hi[2] + 1)} - floor
        keep = set()
        for sd in self.sides:
            mx, mz = (sd["lo"][0] + sd["hi"][0]) // 2, (sd["lo"][1] + sd["hi"][1]) // 2
            keep.add((min(max(mx, lo[0]), hi[0]), min(max(mz, lo[2]), hi[2])))
        free = []
        for x in range(lo[0], hi[0] + 1):
            zs = range(lo[2], hi[2] + 1) if (x - lo[0]) % 2 == 0 else range(hi[2], lo[2] - 1, -1)
            for z in zs:
                if (x, z) not in floor:
                    continue
                if (x, z) in keep or any(n in special for n in ((x + 1, z), (x - 1, z), (x, z + 1), (x, z - 1))):
                    keep.add((x, z))
                else:
                    free.append((x, z))
        if not keep and free:
            keep.add(free.pop(len(free) // 2))
        need = sum(p["cells"] for p in parts)
        if need > len(free):
            targets = [max(-(-3 * p["cells"] // 4), p["cells"] * len(free) // need) for p in parts]
        else:
            targets = [p["cells"] for p in parts]
        if sum(targets) > len(free):
            sys.exit(
                f"starter.py: the play space beside the openings holds {len(free)} column(s) and the parts "
                f"need at least {sum(targets)}; lay them by hand"
            )
        walked = (keep & floor) | set(free)
        beside_sides = {
            (min(max(x, lo[0]), hi[0]), min(max(z, lo[2]), hi[2]))
            for sd in self.sides
            for x in range(sd["lo"][0], sd["hi"][0] + 1)
            for z in range(sd["lo"][1], sd["hi"][1] + 1)
        }

        def whole(cells: set) -> bool:
            if not cells:
                return True
            start = next(iter(cells))
            seen, todo = {start}, [start]
            while todo:
                x, z = todo.pop()
                for n in ((x + 1, z), (x - 1, z), (x, z + 1), (x, z - 1)):
                    if n in cells and n not in seen:
                        seen.add(n)
                        todo.append(n)
            return len(seen) == len(cells)

        for p, n in zip(parts, targets):
            stem = p["id"].removeprefix("part/")
            entry = {"part": p, "region": f"part-{stem}", "walked": p.get("reached", True), "cols": []}
            self.parts.append(entry)
            if entry["walked"]:
                continue
            for c in reversed(free):
                if len(entry["cols"]) == n:
                    break
                if c in beside_sides:
                    continue
                if whole(walked - {c}):
                    walked.discard(c)
                    entry["cols"].append(c)
            if len(entry["cols"]) < n:
                sys.exit(f"starter.py: no room for the seen part `{p['id']}` that leaves the walked floor one piece; lay it by hand")
            free = [c for c in free if c not in set(entry["cols"])]
        for e, n in zip(self.parts, targets):
            if e["walked"]:
                e["cols"], free = free[:n], free[n:]
        for e in self.parts:
            for c in e["cols"]:
                self.col_part[c] = e

    def in_space_xz(self, x: int, z: int) -> bool:
        lo, hi = self.space
        return lo[0] <= x <= hi[0] and lo[2] <= z <= hi[2]

    def open_side(self, x: int, z: int) -> str | None:
        """The face of the open side whose ring run holds column `(x, z)`."""
        for s in self.sides:
            if s["lo"][0] <= x <= s["hi"][0] and s["lo"][1] <= z <= s["hi"][1]:
                return s["face"]
        return None

    def wall_ring(self, x: int, z: int) -> bool:
        lo, hi = self.space
        return (lo[0] - 1 <= x <= hi[0] + 1 and lo[2] - 1 <= z <= hi[2] + 1) and not self.in_space_xz(x, z)

    # -- what one cell is, by the rules above --
    def cell(self, x: int, y: int, z: int) -> tuple:
        kind = self.base_cell(x, y, z)
        if kind[0] == "claim" and kind[1].startswith("side-") and getattr(self, "col_part", None):
            # An open side's cell is the way out of the space inside it.
            space = self.side_space(x, z)
            return kind if space == "room" else ("claim", f"{kind[1]}-{space}", None)
        part = getattr(self, "col_part", {}).get((x, z))
        if part is None or kind != ("claim", "room", None):
            return kind
        return ("claim", part["region"], None)

    def side_space(self, x: int, z: int) -> str:
        """The walked space whose column stands inside an open side's cell."""
        lo, hi = self.space
        inner = (min(max(x, lo[0]), hi[0]), min(max(z, lo[2]), hi[2]))
        e = self.col_part.get(inner)
        return e["region"] if e is not None and e["walked"] else "room"

    def walkable(self, kind: tuple) -> bool:
        """A cell of a space a body walks: the room, or a walked part."""
        return kind == ("claim", "room", None) or any(kind == ("claim", e["region"], None) for e in self.parts if e["walked"])

    def base_cell(self, x: int, y: int, z: int) -> tuple:
        c = (x, y, z)
        for s in self.seams:
            if s["bar"] is not None and all(s["bar"][0][i] <= c[i] < s["bar"][1][i] for i in range(3)):
                return ("claim", f"seam-{s['stem']}", f"bar-{s['stem']}")
        for s in self.seams:
            if all(s["lo"][i].value <= c[i] < s["hi"][i].value for i in range(3)):
                return ("claim", f"{s['stem']}-way", None)
        d = self.datum.value
        for g in getattr(self, "gates", []):
            # the alcove and its grille, two courses high, walled at both
            # sides and capped with wall to the lid, so the bar is the only way
            # between the alcove and the room
            if d <= y < self.wall_top.value and ((x == g["x"] and z in (g["z"], g["z"] + 1)) or (abs(x - g["x"]) == 1 and z == g["z"])):
                if x != g["x"] or y >= d + 2:
                    return ("fill", "wall")
                if z == g["z"]:
                    return ("claim", f"{g['stem']}-alcove", None)
                return ("claim", g["stem"], f"bar-{g['stem']}")
        for s in self.seams:
            ap = s["approach"]
            if ap is None:
                continue
            lad = ap["ladder"]
            if lad is not None and lad["lo"][0] <= x < lad["hi"][0] and lad["lo"][2] <= z < lad["hi"][2] and d <= y <= ap["sill"].value:
                # the ladder up to the sill, and the cell beside the landing
                # open, so the climb abuts both the room and the landing
                return ("claim", f"{s['stem']}-ladder", f"ladder-{lad['facing']}" if y < ap["sill"].value else None)
            xz = all(ap["plo"][i].value <= c[i] < ap["phi"][i].value for i in (0, 2))
            if xz and d <= y < ap["sill"].value:
                return ("fill", "floor")
            if xz and lad is not None and ap["sill"].value <= y < ap["top"].value:
                return ("claim", f"{s['stem']}-landing", None)
        d = self.datum.value
        if y < d:
            if self.aloft and y < d - 1:
                return ("void",)
            return ("fill", "floor")
        if self.lid is not None and y == self.lid.value:
            if self.in_space_xz(x, z) and (x % LAMP_PERIOD, z % LAMP_PERIOD) == (2, 2):
                return ("fill", "lamp")
            return ("fill", "lid")
        if self.lid is not None and y > self.lid.value:
            return ("claim", "roof", None)
        side = self.open_side(x, z)
        if side is not None and d <= y < self.wall_top.value:
            # An open side stands no wall: its ring cells are open from the
            # walk plane up, and the floor course below runs across them.
            return ("claim", f"side-{side}", None)
        if self.wall_ring(x, z) and y < self.wall_top.value:
            lo, hi = self.space
            along, a0, a1 = (z, lo[2], hi[2]) if x in (lo[0] - 1, hi[0] + 1) else (x, lo[0], hi[0])
            if y == d + 1 and along % LAMP_PERIOD == 2 and a0 <= along <= a1:
                return ("fill", "lamp")
            return ("fill", "wall")
        if self.in_space_xz(x, z) and y < self.wall_top.value:
            return ("claim", "room", None)
        return ("void",)

    def cuts(self, axis: int) -> list[Bound]:
        """Every coordinate on `axis` where what a cell is can change."""
        n = self.n[axis]
        lo, hi = self.space
        out = [lit(0), lit(n)]
        for s in self.seams:
            out += [s["lo"][axis], s["hi"][axis]]
            if s["bar"] is not None:
                out += [lit(s["bar"][0][axis]), lit(s["bar"][1][axis])]
            ap = s["approach"]
            if ap is not None:
                if axis == 1:
                    out += [ap["sill"], ap["top"]]
                else:
                    out += [ap["plo"][axis], ap["phi"][axis]]
                if ap["ladder"] is not None and axis != 1:
                    out += [lit(ap["ladder"]["lo"][axis]), lit(ap["ladder"]["hi"][axis])]
                if ap["ladder"] is not None and axis == 1:
                    out += [ap["sill"].plus(1)]
        for s in self.sides:
            if axis != 1:
                i = 0 if axis == 0 else 1
                out += [lit(s["lo"][i]), lit(s["hi"][i] + 1)]
        for g in self.gates:
            out += [lit(g["lo"][axis]), lit(g["hi"][axis])]
            if axis == 0:
                out += [lit(g["x"] - 1), lit(g["x"] + 2)]
        if axis == 1:
            out += [self.datum.plus(-1), self.datum, self.datum.plus(1), self.datum.plus(2), self.wall_top]
            if self.lid is not None:
                out += [self.lid, self.lid.plus(1)]
        else:
            out += [lit(lo[axis] - 1), lit(lo[axis]), lit(hi[axis] + 1), lit(hi[axis] + 2)]
            if self.parts:
                out += [lit(v) for v in range(lo[axis], hi[axis] + 2)]
            out += [lit(v) for v in range(0, n, LAMP_PERIOD)] + [lit(v) for v in range(2, n, LAMP_PERIOD)] + [lit(v + 1) for v in range(2, n, LAMP_PERIOD)]
        best: dict[int, Bound] = {}
        for b in out:
            if 0 <= b.value <= n and (b.value not in best or (b.handed and not best[b.value].handed)):
                best[b.value] = b
        best[0] = lit(0)
        return [best[v] for v in sorted(best) if v < n]


def size_of(lo: Bound, hi: Bound | None) -> dict:
    if hi is None:
        return {"size": "relative", "weight": num(1)}
    if lo.expr.get("expr") == "int" and hi.expr.get("expr") == "int":
        return {"blocks": num(hi.value - lo.value), "size": "absolute"}
    if lo.value == 0 and lo.expr.get("expr") == "int":
        return {"blocks": hi.expr, "size": "absolute"}
    return {"blocks": arith(hi.expr, "sub", lo.expr), "size": "absolute"}


class Rules:
    """Rules, each body stated once and called by name wherever it recurs."""

    def __init__(self) -> None:
        self.rules: dict[str, list] = {}
        self.names: dict[str, str] = {}

    def name(self, body: dict, hint: str) -> dict:
        key = json.dumps(body, sort_keys=True)
        if key not in self.names:
            name = f"{hint}_{len(self.names)}"
            self.names[key] = name
            self.rules[name] = [{"body": body, "weight": 1}]
        return {"op": "call", "symbol": self.names[key]}


def leaf(kind: tuple) -> dict:
    if kind[0] == "fill":
        return fill(kind[1])
    if kind[0] == "void":
        return VOID
    _, region, role = kind
    return claim(region, fill(role) if role else VOID)


def split(axis: str, cuts: list[Bound], children: list[dict]) -> dict:
    if len(children) == 1:
        return children[0]
    sizes = [size_of(cuts[i], cuts[i + 1] if i + 1 < len(cuts) else None) for i in range(len(cuts))]
    return {"axis": axis, "children": children, "op": "split", "sizes": sizes}


def body(p: Place, rules: Rules) -> dict:
    """The place, cut into boxes on x, then y, then z, each box one kind of cell."""
    xs, ys, zs = p.cuts(0), p.cuts(1), p.cuts(2)
    columns = []
    for x in xs:
        courses = []
        for y in ys:
            row = [leaf(p.cell(x.value, y.value, z.value)) for z in zs]
            courses.append(rules.name(split("z", zs, row), "row"))
        columns.append(rules.name(split("y", ys, courses), "column"))
    return split("x", xs, columns)


def marks(p: Place, inner: dict) -> dict:
    """Every owed name, answered by a `mark` of its stem on walkable floor."""
    lo, hi = p.a["space"]
    cx, cz = (lo[0] + hi[0]) // 2, (lo[2] + hi[2]) // 2
    taken: set[tuple[int, int]] = set()

    def free(x: int, z: int) -> tuple[int, int]:
        for dz in range(0, max(p.ex, p.ez)):
            for x2, z2 in ((x, z + dz), (x, z - dz), (x + dz, z), (x - dz, z)):
                if lo[0] <= x2 <= hi[0] and lo[2] <= z2 <= hi[2] and (x2, z2) not in taken:
                    if p.walkable(p.cell(x2, p.datum.value, z2)) and p.walkable(p.cell(x2, p.datum.value + 1, z2)) and p.cell(x2, p.datum.value - 1, z2) == ("fill", "floor"):
                        taken.add((x2, z2))
                        return x2, z2
        sys.exit("starter.py: no free floor cell for a mark; the play space is full")

    out = inner
    for name in reversed(p.a["owed_anchors"]):
        stem = name.removeprefix("anchor/")
        if stem.startswith("seam-") or any(g["stem"] == stem for g in p.gates):
            continue  # answered by a barred edge's region, never a mark
        mark = {"anchor": stem, "at": "offset", "facing": "south", "y": p.datum.expr}
        if stem == "spawn":
            mark["role"] = "entry"
        target = (cx, cz)
        if stem.startswith("unlock-"):
            s = next((s for s in p.seams if f"unlock-{s['stem']}" == stem), None)
            if s is not None:
                (x0, _, z0), (x1, _, z1) = s["seam"]["cells"]
                target = (min(max((x0 + x1) // 2, lo[0]), hi[0]), min(max((z0 + z1) // 2, lo[2]), hi[2]))
        x, z = free(*target)
        mark["x"], mark["z"] = num(x), num(z)
        out = {"body": out, "mark": mark, "op": "mark"}
    return out


def contract(p: Place) -> dict:
    """The spatial contract: the room, a landing under each raised opening, an
    edge per seam, the roof zone no body walks."""
    spaces = {"room": {"envelope": "enclosed" if p.lid is not None else "open"}}
    edges = []
    for s in p.seams:
        seam = s["seam"]
        space = "room"
        ap = s["approach"]
        if ap is not None and ap["ladder"] is not None:
            space = f"{s['stem']}-landing"
            spaces[space] = {"envelope": "open"}
            edges.append({"a": "room", "b": space, "class": "climb", "rise": ap["rise"], "via": f"{s['stem']}-ladder"})
        if s["bar"] is not None:
            edge = {"a": space, "b": "exterior", "bar": {"block": f"bar-{s['stem']}", "region": f"seam-{s['stem']}"}, "class": "barred"}
            if s["bar"] != ([v.value for v in s["lo"]], [v.value for v in s["hi"]]):
                edge["via"] = f"{s['stem']}-way"  # the opening the bar closes
            edges.append(edge)
            continue
        answers = [c for c in seam["answer_with"] if c != "barred"]
        cls = "walk" if "walk" in answers else answers[0]
        edge = {"a": space, "b": "exterior", "class": cls, "via": f"{s['stem']}-way"}
        if cls in ("stair", "drop", "climb"):
            edge["rise"] = 0  # the level beyond is the neighbour's to measure
        edges.append(edge)
    for s in p.sides:
        # A frontage a body crosses: the open side's cells are the way out
        # (spec-0123 §5.4). A counter a body does not cross stands at the play
        # space's edge, inside, and the side stays this edge's. On a plot the
        # run is one way out per walked space standing inside it.
        spaces_in = []
        for x in range(s["lo"][0], s["hi"][0] + 1):
            for z in range(s["lo"][1], s["hi"][1] + 1):
                sp = p.side_space(x, z) if p.col_part else "room"
                if sp not in spaces_in:
                    spaces_in.append(sp)
        for sp in sorted(spaces_in):
            via = f"side-{s['face']}" if sp == "room" else f"side-{s['face']}-{sp}"
            edges.append({"a": sp, "b": "exterior", "class": "walk", "via": via})
    no_body = {}
    pairs = set()
    for e in p.parts:
        if not e["walked"]:
            no_body[e["region"]] = {"part": e["part"]["id"], "reason": f"{e['part']['use']}: seen, never entered"}
            continue
        spaces[e["region"]] = {"envelope": spaces["room"]["envelope"], "part": e["part"]["id"]}
    # A walk edge between every two walked spaces whose columns touch.
    for (x, z), e in p.col_part.items():
        if not e["walked"]:
            continue
        for n in ((x + 1, z), (x, z + 1), (x - 1, z), (x, z - 1)):
            if not p.in_space_xz(*n):
                continue
            o = p.col_part.get(n)
            other = "room" if o is None else (o["region"] if o["walked"] else None)
            if other is not None and other != e["region"]:
                pairs.add(tuple(sorted((e["region"], other))))
    for a_, b_ in sorted(pairs):
        edges.append({"a": a_, "b": b_, "class": "walk"})
    for g in p.gates:
        spaces[f"{g['stem']}-alcove"] = {"envelope": "open"}
        edges.append({"a": "room", "b": f"{g['stem']}-alcove", "bar": {"block": f"bar-{g['stem']}", "region": g["stem"]}, "class": "barred"})
    out = {
        "edges": edges,
        "entry": "room",
        # ── BUILD HERE: the spaces. A room a body walks around inside walls and
        # under a lid is `enclosed`; a street, a deck or a court open to the sky
        # is `open`. A second floor is a second space and a `climb` or `stair`
        # edge between them — a landing below is reached that way
        # (grammar.md §2d; references/detail.md, the program's contract).
        "spaces": spaces,
    }
    if p.lid is not None and p.lid.value + 1 < p.ey:
        no_body["roof"] = {"reason": "the roof zone over the lid, which no one is meant to walk"}
        out["no_body_majority_ack"] = "the roof zone the plan reserves over the lid is left for the roof the author builds; nobody walks it"
    if no_body:
        out["no_body"] = no_body
    return out


# A handed block named with no state, written out as the gates require
# (`DW0735`, `DW0737`): every property, the block's own default where the
# design says nothing.
BARE_STATES = {
    "minecraft:iron_bars": "minecraft:iron_bars[east=false,north=false,south=false,waterlogged=false,west=false]",
}


def full_state(block: str) -> str:
    return BARE_STATES.get(block, block)


def program(a: dict) -> dict:
    p = Place(a)
    rules = Rules()
    # ── BUILD HERE: the building. The body below is the empty place — floor,
    # ring wall, lid, openings, sconces. Replace the `room` boxes with the
    # rooms the design draws, starting from the idioms (grammar.md §2c: 1
    # repetition for a colonnade or a run of bays, 3 shape for an arch or a
    # gable, 7 symmetry for a front, 9 light for where the lamps stand) and the
    # procedure (references/new-pieces.md step 3, the program; step 4, the
    # gates). Keep every seam's region and every mark; they are what binds.
    start = marks(p, body(p, rules))
    rules.rules["place"] = [{"body": start, "weight": 1}]
    palette = dict(PALETTE)
    for s in p.seams:
        if s["bar"] is not None:
            palette[f"bar-{s['stem']}"] = full_state(s["seam"]["bar_block"])
        ap = s["approach"]
        if ap is not None and ap["ladder"] is not None:
            f = ap["ladder"]["facing"]
            palette[f"ladder-{f}"] = f"minecraft:ladder[facing={f},waterlogged=false]"
    for g in p.gates:
        palette[f"bar-{g['stem']}"] = full_state("minecraft:iron_bars")
    climbs = any(e.get("class") == "climb" for e in contract(p)["edges"])
    return {
        "contract": contract(p),
        "name": f"{a['place'].removeprefix('node/')}-starter",
        "palette": palette,
        "params": dict(sorted(p.h.params.items())),
        "rules": rules.rules,
        # ── BUILD HERE: the faces the piece shows the world (grammar.md §2f).
        # Derived from what this skeleton draws: a declared side must hold a
        # block (`DW0885`), and a side over open air must be declared.
        "shown_faces": shown_faces(p),
        "start": "place",
        "version": "1.14.0" if p.parts else ("1.10.0" if climbs else "1.9.0"),
    }


def shown_faces(p) -> list[str]:
    """The sides this skeleton finishes: the four walls; the top course where
    the lid stands at it, or the walls reach it under an open sky (a lid under a
    declared roof zone leaves the top course to the roof the author builds, so
    `up` is the author's to add with the roof); and the underside of an aloft
    place, which stands over air the party can be in."""
    faces = ["east", "north", "south", "west"]
    if (p.lid is not None and p.lid.value == p.ey - 1) or (p.lid is None and p.wall_top.value >= p.ey):
        faces.append("up")
    if p.aloft:
        faces.append("down")
    return sorted(faces)



# ======================================================================
# Everything above is the skill's starter, verbatim: it binds the handing
# (datum, seams, open sides, owed names, parts). Everything below turns a
# voxel model of the plot into that place's cells, as the cathedral's
# generator does: a plot module builds a Model in piece-local coordinates
# (+x east, +z south, y 0 the ground course, y 1 the walk plane), names each
# part's columns in `model.region`, and says where its owed names stand.
# Nothing below reads a world coordinate: a moved box costs nothing.
# ======================================================================

AIR = "~air"

DIRS = {"north": (0, -1), "south": (0, 1), "east": (1, 0), "west": (-1, 0)}
OPP = {"north": "south", "south": "north", "east": "west", "west": "east"}
CCW = {"north": "west", "west": "south", "south": "east", "east": "north"}


class Model:
    def __init__(self, palette: dict):
        self.v: dict = {}
        self.region: dict = {}
        self.palette = palette

    def set(self, x, y, z, role):
        self.v[(x, y, z)] = role

    def box(self, x0, x1, y0, y1, z0, z1, role):
        for x in range(min(x0, x1), max(x0, x1) + 1):
            for y in range(min(y0, y1), max(y0, y1) + 1):
                for z in range(min(z0, z1), max(z0, z1) + 1):
                    self.v[(x, y, z)] = role

    def get(self, x, y, z):
        return self.v.get((x, y, z))

    def block(self, role):
        b = self.palette.get(role)
        if isinstance(b, list):
            b = b[0]["block"]
        return b or ""

    def regions(self, stem, x0, x1, z0, z1):
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                self.region[(x, z)] = stem


def hsh(*a):
    h = 2166136261
    for v in a:
        h = ((h ^ (v & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    return h


# ---- what a block does to a body: full, tall (a fence), low (a step), or pass ----

PASS_WORDS = ("_door[", "flower", "tulip", "poppy", "dandelion", "cornflower", "allium", "daisy", "orchid",
              "bluet", "lily_of_the_valley", "short_grass", "fern", "rose_bush", "lilac", "peony", "sunflower",
              "chain[", "ladder", "torch", "vine", "button", "pressure_plate", "carpet", "rail", "sweet_berry",
              "wheat", "carrots", "potatoes", "beetroots", "pink_petals", "leaf_litter", "bush[", "dead_bush",
              "lantern[hanging=true", "cobweb", "tripwire", "lever", "redstone_wire", "hanging_sign", "_sign[")
TALL_WORDS = ("_fence[", "_fence_gate[", "_wall[", "glass_pane", "iron_bars", "bamboo[")
LOW_WORDS = ("_stairs[", "_slab[", "lantern[", "candle[", "campfire[", "_trapdoor[", "flower_pot", "chest[",
             "composter", "bed[", "snow[", "daylight", "cake", "brewing_stand", "lectern", "stonecutter",
             "enchanting", "sea_pickle", "decorated_pot", "head[", "skull[", "heavy_core", "end_rod", "lightning_rod")


def classify(block: str) -> str:
    if not block or block == "minecraft:air":
        return "pass"
    if ("_slab[" in block and "type=top" in block) or ("_slab[" in block and "type=double" in block):
        return "full"
    if "_stairs[" in block and "half=top" in block:
        return "full"
    if "_trapdoor[" in block and ("open=true" in block or "half=top" in block):
        return "pass"
    for w in PASS_WORDS:
        if w in block:
            return "pass"
    for w in TALL_WORDS:
        if w in block:
            return "tall"
    for w in LOW_WORDS:
        if w in block:
            return "low"
    return "full"


def finish(m: Model):
    """Write every connecting block's state as the game derives it from its
    neighbours, so the written world is the world the server keeps: stair
    shapes, and the arms of panes, bars, fences and walls."""
    stair_shapes(m)
    connections(m)


def stair_shapes(m: Model):
    def props(role):
        b = m.palette.get(role)
        if not isinstance(b, str) or "_stairs[" not in b:
            return None
        kv = dict(p.split("=") for p in b[b.index("[") + 1:-1].split(","))
        return kv["facing"], kv["half"]

    def at(x, y, z):
        r = m.v.get((x, y, z))
        return props(r) if r else None

    new = {}
    for (x, y, z), r in list(m.v.items()):
        st = props(r)
        if st is None:
            continue
        f, h = st

        def take(face):
            dx, dz = DIRS[face]
            n = at(x + dx, y, z + dz)
            return n is None or n[0] != f or n[1] != h
        shape = "straight"
        dx, dz = DIRS[f]
        front = at(x + dx, y, z + dz)
        if front and front[1] == h:
            d = front[0]
            if (d in ("north", "south")) != (f in ("north", "south")) and take(OPP[d]):
                shape = "outer_left" if d == CCW[f] else "outer_right"
        if shape == "straight":
            back = at(x - dx, y, z - dz)
            if back and back[1] == h:
                d = back[0]
                if (d in ("north", "south")) != (f in ("north", "south")) and take(d):
                    shape = "inner_left" if d == CCW[f] else "inner_right"
        if shape != "straight":
            name = f"{r}~{shape}"
            if name not in m.palette:
                m.palette[name] = m.palette[r].replace("shape=straight", f"shape={shape}")
            new[(x, y, z)] = name
    m.v.update(new)


def _family(block: str) -> str | None:
    for w in ("glass_pane", "iron_bars"):
        if w in block:
            return "pane"
    if "_fence_gate[" in block:
        return "gate"
    if "_fence[" in block:
        return "fence"
    if "_wall[" in block:
        return "wall"
    return None


def connections(m: Model):
    """Panes, bars, fences and walls take arms toward a full block or a
    neighbour of their own family, as the game would set them."""
    new = {}
    for (x, y, z), r in list(m.v.items()):
        b = m.palette.get(r)
        if not isinstance(b, str):
            continue
        fam = _family(b)
        if fam not in ("pane", "fence", "wall"):
            continue
        arms = {}
        for face, (dx, dz) in DIRS.items():
            nr = m.v.get((x + dx, y, z + dz))
            nb = m.block(nr) if nr else ""
            nf = _family(nb) if nb else None
            joined = bool(nb) and (classify(nb) == "full" or nf == fam or (fam == "fence" and nf == "gate")
                                   or (fam == "wall" and nf == "pane"))
            arms[face] = joined
        name = r + "~" + "".join(f[0] for f in sorted(arms) if arms[f])
        if name not in m.palette:
            base = b[:b.index("[")]
            if fam == "wall":
                above = m.v.get((x, y + 1, z))
                up = not (arms["north"] and arms["south"] and not arms["east"] and not arms["west"]) and \
                    not (arms["east"] and arms["west"] and not arms["north"] and not arms["south"])
                if above:
                    up = True
                st = ",".join(f"{f}={'low' if arms[f] else 'none'}" if f != "up" else "" for f in ())
                st = (f"east={'low' if arms['east'] else 'none'},north={'low' if arms['north'] else 'none'},"
                      f"south={'low' if arms['south'] else 'none'},up={'true' if up else 'false'},"
                      f"waterlogged=false,west={'low' if arms['west'] else 'none'}")
            else:
                st = (f"east={str(arms['east']).lower()},north={str(arms['north']).lower()},"
                      f"south={str(arms['south']).lower()},waterlogged=false,west={str(arms['west']).lower()}")
            m.palette[name] = f"{base}[{st}]"
        new[(x, y, z)] = name
    m.v.update(new)


# ---- building helpers ----


def gable(m: Model, x0, x1, z0, z1, y0, along, stair, ridge, fill=None, ov=1):
    """A pitched roof over the footprint [x0..x1]x[z0..z1] (walls included),
    eaves one course below `y0`'s first stair course, overhanging `ov` cells
    on every side; ridge along `along`. `stair` is a role prefix with
    `_n/_s/_e/_w` suffixes; `fill` closes the gable ends inside the walls."""
    if along == "x":
        lo, hi, k = z0 - ov, z1 + ov, 0
        while lo <= hi:
            y = y0 + k
            if lo == hi:
                m.box(x0 - ov, x1 + ov, y, y, lo, lo, ridge)
            else:
                m.box(x0 - ov, x1 + ov, y, y, lo, lo, stair + "_s")
                m.box(x0 - ov, x1 + ov, y, y, hi, hi, stair + "_n")
                if fill and lo + 1 <= hi - 1:
                    for x in (x0, x1):
                        m.box(x, x, y, y, max(lo + 1, z0), min(hi - 1, z1), fill)
            lo, hi, k = lo + 1, hi - 1, k + 1
        return y0 + k - 1
    lo, hi, k = x0 - ov, x1 + ov, 0
    while lo <= hi:
        y = y0 + k
        if lo == hi:
            m.box(lo, lo, y, y, z0 - ov, z1 + ov, ridge)
        else:
            m.box(lo, lo, y, y, z0 - ov, z1 + ov, stair + "_e")
            m.box(hi, hi, y, y, z0 - ov, z1 + ov, stair + "_w")
            if fill and lo + 1 <= hi - 1:
                for z in (z0, z1):
                    m.box(max(lo + 1, x0), min(hi - 1, x1), y, y, z, z, fill)
        lo, hi, k = lo + 1, hi - 1, k + 1
    return y0 + k - 1


def frame_walls(m: Model, x0, x1, z0, z1, y0, y1, post, infill, beam_x=None, beam_z=None, bay=3, plinth=None):
    """A timber-framed box: posts at the corners and every `bay` cells, a
    plinth course at the bottom, a beam at the top, infill between."""
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if x not in (x0, x1) and z not in (z0, z1):
                continue
            corner = x in (x0, x1) and z in (z0, z1)
            along_x = z in (z0, z1)
            postcol = corner or (along_x and (x - x0) % bay == 0) or (not along_x and (z - z0) % bay == 0)
            for y in range(y0, y1 + 1):
                if plinth and y == y0:
                    role = plinth
                elif postcol:
                    role = post
                elif y == y1 and (beam_x or beam_z):
                    role = beam_x if along_x else beam_z
                else:
                    role = infill
                m.set(x, y, z, role)


def door(m: Model, x, y, z, role):
    """A door's two halves: `role` + '_lo' / '_hi'."""
    m.set(x, y, z, role + "_lo")
    m.set(x, y + 1, z, role + "_hi")


def door_roles(palette: dict, role: str, block: str, facing: str, hinge="left"):
    for half, suf in (("lower", "_lo"), ("upper", "_hi")):
        palette[role + suf] = f"{block}[facing={facing},half={half},hinge={hinge},open=false,powered=false]"


def flower_bed(m: Model, x0, x1, z0, z1, flowers, soil="bed_soil"):
    """A bed of flowers on soil, one flower per cell, chosen by a stable hash."""
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            m.set(x, 0, z, soil)
            m.set(x, 1, z, flowers[hsh(x, z, 7) % len(flowers)])


# ---- the place: the starter's, with the plot's model in place of the empty room ----


class Plot(Place):
    MODEL = None          # a function (place) -> Model, set by the plot module
    MARK_AT: dict = {}    # owed stem -> (x, z, facing)
    REASON = "wall heads, roof slopes and sills: seen, never stood on"

    def lay_parts(self, parts):
        self.model = type(self).MODEL(self)
        by_stem = {p["id"].removeprefix("part/"): p for p in parts}
        self.parts, self.col_part = [], {}
        for stem, p in by_stem.items():
            e = {"part": p, "region": f"part-{stem}", "walked": p.get("reached", True), "cols": []}
            self.parts.append(e)
            for c, st in sorted(self.model.region.items()):
                if st == stem:
                    e["cols"].append(c)
                    self.col_part[c] = e
        self.reach()

    def kind_of(self, r):
        if r is None or r == AIR:
            return "pass"
        return classify(self.model.block(r))

    def base_cell(self, x, y, z):
        kind = Place.base_cell(self, x, y, z)
        if not self.in_space_xz(x, z) and kind == ("fill", "wall"):
            return ("claim", "room", None)     # no corner post marks the plot
        if not self.in_space_xz(x, z) and kind == ("fill", "floor"):
            r = self.model.get(x, y, z)
            return ("fill", r if r and self.kind_of(r) == "full" else "turf")
        if not self.in_space_xz(x, z):
            if kind[0] == "claim" and kind[1].startswith("side-") and y >= self.datum.value + 2:
                return ("claim", "room", None)  # the side's opening is the body's height; above it, open air
            return kind
        if kind[0] == "claim" and kind[1].endswith("-way"):
            return kind                        # the connection's opening, kept clear
        r = self.model.get(x, y, z)
        if r is None or r == AIR:
            if y < self.datum.value:
                return ("fill", "turf")
            if (x, y, z) in self.unwalked:
                return ("claim", "unwalked", None)
            return kind if kind[0] == "claim" else ("claim", "room", None)
        if self.kind_of(r) == "full":
            return ("fill", r)
        if (x, y, z) in self.unwalked:
            return ("claim", "unwalked", r)
        if (x, y, z) not in self.reached:
            return ("fill", r)
        e = self.col_part.get((x, z))
        return ("claim", e["region"] if e is not None else "room", r)

    def reach(self):
        """Every standable cell a body cannot walk to from the plot's edges:
        roof slopes, wall heads, sills. Claimed as `unwalked`."""
        self.unwalked = set()
        lo, hi = self.space
        d = self.datum.value

        def kind(x, y, z):
            if not (lo[0] <= x <= hi[0] and lo[2] <= z <= hi[2]) or y < 0 or y > hi[1] + 1:
                return "pass"
            r = self.model.get(x, y, z)
            if r is None or r == AIR:
                return "full" if y < d else "pass"
            return self.kind_of(r)

        def standable(x, y, z):
            k = kind(x, y, z)
            if k not in ("pass", "low") or kind(x, y + 1, z) not in ("pass",):
                return False
            if k == "low" and kind(x, y + 1, z) != "pass":
                return False
            return k == "low" or kind(x, y - 1, z) in ("full", "low", "tall")

        cols = {(x, z) for x in range(lo[0], hi[0] + 1) for z in range(lo[2], hi[2] + 1)}
        cells = {(x, y, z) for (x, z) in cols for y in range(1, hi[1] + 1) if standable(x, y, z)}
        crowns = {c for c in cells if self.kind_of(self.model.get(c[0], c[1] - 1, c[2])) == "full"
                  and "leaves" in self.model.block(self.model.get(c[0], c[1] - 1, c[2]))}
        walk = cells - crowns
        start = [(x, y, z) for (x, y, z) in walk if y == d and (x in (lo[0], hi[0]) or z in (lo[2], hi[2]))]
        seen, todo = set(start), list(start)
        while todo:
            x, y, z = todo.pop()
            for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, nz = x + dx, z + dz
                h0 = y + (0.5 if kind(x, y, z) == "low" else 0)
                for ny in (y, y + 1):
                    if ny + (0.5 if kind(nx, ny, nz) == "low" else 0) - h0 > 1:
                        continue
                    if ny == y + 1 and kind(x, y + 2, z) != "pass":
                        continue
                    if (nx, ny, nz) in walk and (nx, ny, nz) not in seen:
                        seen.add((nx, ny, nz))
                        todo.append((nx, ny, nz))
                        break
                else:
                    ny = y - 1
                    while ny >= 1 and kind(nx, ny, nz) == "pass" and (nx, ny, nz) not in cells:
                        ny -= 1
                    if (nx, ny, nz) in walk and (nx, ny, nz) not in seen and kind(nx, y, nz) == "pass" \
                            and kind(nx, y + 1, nz) == "pass":
                        seen.add((nx, ny, nz))
                        todo.append((nx, ny, nz))
        for c in cells - seen:
            e = self.col_part.get((c[0], c[2]))
            if e is None or e["walked"]:
                self.unwalked.add(c)
        self.reached = seen

    def cuts(self, axis):
        n = self.n[axis]
        out = super().cuts(axis)
        best = {b.value: b for b in out}
        for v in range(n):
            best.setdefault(v, lit(v))
        return [best[v] for v in sorted(best)]


def plot_body(p, rules):
    """The place, cut on x, then y, then z; equal neighbours merged into one span."""
    xs, ys, zs = p.cuts(0), p.cuts(1), p.cuts(2)

    def runs(cuts, items):
        out_c, out_i = [], []
        for c, it in zip(cuts, items):
            if out_i and json.dumps(out_i[-1], sort_keys=True) == json.dumps(it, sort_keys=True):
                continue
            out_c.append(c)
            out_i.append(it)
        return out_c, out_i

    columns = []
    for x in xs:
        courses = []
        for y in ys:
            row = [leaf(p.cell(x.value, y.value, z.value)) for z in zs]
            cz, rz = runs(zs, row)
            courses.append(rules.name(split("z", cz, rz), "row"))
        cy, ry = runs(ys, courses)
        columns.append(rules.name(split("y", cy, ry), "column"))
    cx, rx = runs(xs, columns)
    return split("x", cx, rx)


def plot_marks(p, inner):
    out = inner
    for name in reversed(p.a["owed_anchors"]):
        stem = name.removeprefix("anchor/")
        x, z, facing = p.MARK_AT[stem]
        assert p.walkable(p.cell(x, p.datum.value, z)), (stem, p.cell(x, p.datum.value, z))
        mark = {"anchor": stem, "at": "offset", "facing": facing, "y": p.datum.expr, "x": num(x), "z": num(z)}
        out = {"body": out, "mark": mark, "op": "mark"}
    return out


def plot_contract(p) -> dict:
    """The starter's contract, with the walk edges between spaces taken from
    where a body actually steps from one to the other, not from touching columns."""
    c = contract(p)
    keep = [e for e in c["edges"] if e["b"] == "exterior" or e.get("class") != "walk" or "via" in e]

    def space_of(cell):
        k = p.cell(*cell)
        if k[0] == "claim" and p.walkable(("claim", k[1], None)):
            return k[1]
        return None

    pairs = set()
    for (x, y, z) in sorted(p.reached):
        a_ = space_of((x, y, z))
        if a_ is None:
            continue
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            for dy in (-1, 0, 1):
                n = (x + dx, y + dy, z + dz)
                if n in p.reached:
                    b_ = space_of(n)
                    if b_ is not None and b_ != a_:
                        pairs.add(tuple(sorted((a_, b_))))
    for a_, b_ in sorted(pairs):
        keep.append({"a": a_, "b": b_, "class": "walk"})
    c["edges"] = keep
    return c


def plot_program(cls, a: dict) -> dict:
    p = cls(a)
    rules = Rules()
    start = plot_marks(p, plot_body(p, rules))
    rules.rules["place"] = [{"body": start, "weight": 1}]
    c = plot_contract(p)
    if p.unwalked:
        c.setdefault("no_body", {})["unwalked"] = {"reason": cls.REASON}
    used = set()
    for alts in rules.rules.values():
        used |= set(re.findall(r'"role": "([^"]+)"', json.dumps(alts)))
    palette = {k: v for k, v in sorted(p.model.palette.items()) if k in used}
    return {
        "contract": c,
        "name": a["place"].removeprefix("node/"),
        "palette": palette,
        "params": dict(sorted(p.h.params.items())),
        "rules": rules.rules,
        "shown_faces": ["east", "north", "south", "west"],
        "start": "place",
        "version": "1.14.0",
    }


def run(cls, argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--allocation", required=True, help="`delvec allocation <campaign> <place>`, saved")
    ap.add_argument("--out", required=True, help="where the program is written")
    args = ap.parse_args(argv)
    with open(args.allocation, encoding="utf-8") as f:
        allocation = json.load(f)
    text = json.dumps(plot_program(cls, allocation), indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(text)
    return 0
