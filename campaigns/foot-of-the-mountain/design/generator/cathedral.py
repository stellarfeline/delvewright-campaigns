#!/usr/bin/env python3
"""The starter generator for ONE place: an empty-but-correct program, read off its allocation.

`scripts/handout.py` copies this file beside every handout, with the place's
allocation saved next to it, so a place's author starts from a program that
already passes `delvec detail --check` and builds the place into it — never
from research. Run it as the handout prints it:

    "$DELVEWRIGHT_PYTHON" starter.py --allocation allocation.json --out <campaign>/programs/<stem>.json

It runs no binary and names no path: it reads the allocation `delvec allocation
<campaign> <place>` printed and writes the program. What it emits, for any
allocation the engine hands:

- the ground: a ground place's floor drawn down to the bottom of its claim; an
  aloft place's one floor course under its walk plane and nothing beneath;
- a wall on every cell of the one-cell ring, from the walk plane up — a cell a
  neighbour or the whole owns is a void the verb replaces, so painting it is
  harmless and nothing depends on it — except on a side the place declares
  open, whose ring run (its two corners excluded) is left open from the walk
  plane up with the floor course running across it, claimed as the region a
  `walk` edge to `exterior` goes `via`;
- a lid over a roofed place (at the plan's `roof/lid-y` where it declares a
  roof, at the frame's top course otherwise), and the declared roof zone above
  it claimed as a region no body walks;
- every seam answered: its handed cells claimed as the region its contract
  edge goes `via`, or — where this place owns the bar — filled with the bar's
  block inside a `barred` edge over exactly those cells;
- every owed name answered by a `mark` of its stem on walkable floor: `spawn`
  with the `entry` role, `unlock-<edge>` beside its bar, the rest along the
  room's middle;
- on a plot, every handed part laid as a region of exactly its declared
  cells, named for the part with `part`: the columns beside every opening,
  ladder, landing and gate, and the middle of every open side, stay the room; a walked part is a space
  (a walk edge joins every two walked spaces that touch); a part seen and
  never entered is an out-of-walk region over the floor that no edge reaches,
  laid only where the walked floor stays one piece — what keeps a body off it
  (a hedge, a crop, a fence) is yours to build. Where each part stands is this starter's
  choice; its count is the plan's;
- a sconce every four cells of wall a course above the floor, and on a roofed
  place a lamp every four cells of the lid, so the light probe has something
  to measure.

Every handed value it uses is declared as a `handed/…` parameter with the
allocation's value as its default, and the body reads it only through that
parameter (`references/detail.md`, *The program's contract*). A number that is
not handed — where a mark stands, how far apart the lamps are — is this
starter's choice and yours to change.

The building is yours. The places to put it are marked `# ── BUILD HERE`, each
naming the idiom of `docs/reference/grammar.md` §2c it reaches for and the step
of `references/new-pieces.md` that says how. Edit a copy under
`<campaign>/design/generator/<stem>.py`, re-run it, and check after every edit:
`delvec --prefabs "$DELVEWRIGHT_PREFABS" detail --check <campaign> <place>`.

Standard library only.
"""

from __future__ import annotations

import argparse
import json
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
        space = p.seam_space(s)
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
    p = Cathedral(a)
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


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--allocation", required=True, help="`delvec allocation <campaign> <place>`, saved")
    ap.add_argument("--out", required=True, help="where the program is written")
    args = ap.parse_args(argv)
    with open(args.allocation, encoding="utf-8") as f:
        allocation = json.load(f)
    text = json.dumps(program(allocation), indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(text)
    return 0


# ===================================================================== the cathedral
#
# Everything above is the starter, which binds the handing (datum, seams, open
# sides, owed names, parts). Everything below is the building: a voxel model of
# the cathedral, its close and its churchyard, which the place's cell() reads.
#
# Form, after the Gothic cathedral as builders lay it out (a Latin-cross plan):
# a west front on the close with a rose window over a pointed portal; a nave of
# five bays between arcades of piers, aisles either side under lean-to roofs,
# the nave's clerestory carried over them on flying buttresses; a crossing and
# a transept whose gables carry rose windows; a choir of two bays and a
# semicircular apse; a bell tower with a spire at the north-west corner,
# flanking the west front. The churchyard lies south of the nave inside a low
# wall, the plot's only fence.
#
# Axes are piece-local: +x east, +z south; y 0 is the ground course, y 1 the
# walk plane. The square is west, the mountain north, the town south.

AIR = "~air"

PALETTE = {
    # the handed starter's roles, kept for the ring and the ground
    "floor": "minecraft:stone_bricks",
    "wall": "minecraft:stone_bricks",
    "lid": "minecraft:spruce_planks",
    "lamp": "minecraft:lantern[hanging=false,waterlogged=false]",
    # masonry: one structural stone and one dressing stone
    "stone": [{"weight": 12, "block": "minecraft:stone_bricks"},
              {"weight": 2, "block": "minecraft:cracked_stone_bricks"},
              {"weight": 1, "block": "minecraft:mossy_stone_bricks"}],
    "dress": "minecraft:tuff_bricks",
    "quoin": "minecraft:chiseled_tuff_bricks",
    "pier": "minecraft:polished_tuff",
    "plinth": "minecraft:polished_andesite",
    "sill": "minecraft:tuff_brick_slab[type=bottom,waterlogged=false]",
    "glass": "minecraft:light_gray_stained_glass",
    "glass_blue": "minecraft:blue_stained_glass",
    "glass_red": "minecraft:red_stained_glass",
    "glass_gold": "minecraft:yellow_stained_glass",
    "tracery": "minecraft:tuff_brick_wall[east=none,north=none,south=none,up=true,waterlogged=false,west=none]",
    # roofs: deepslate tiles, as the castle's
    "roof": "minecraft:deepslate_tiles",
    "roof_n": "minecraft:deepslate_tile_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]",
    "roof_s": "minecraft:deepslate_tile_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]",
    "roof_e": "minecraft:deepslate_tile_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]",
    "roof_w": "minecraft:deepslate_tile_stairs[facing=west,half=bottom,shape=straight,waterlogged=false]",
    "ridge": "minecraft:deepslate_tile_slab[type=bottom,waterlogged=false]",
    "fly_n": "minecraft:tuff_brick_stairs[facing=north,half=top,shape=straight,waterlogged=false]",
    "fly_s": "minecraft:tuff_brick_stairs[facing=south,half=top,shape=straight,waterlogged=false]",
    "spire": "minecraft:deepslate_tiles",
    "finial": "minecraft:lightning_rod[facing=up,powered=false,waterlogged=false]",
    # floors
    "nave_a": "minecraft:polished_andesite",
    "nave_b": "minecraft:polished_tuff",
    "aisle_floor": "minecraft:stone_bricks",
    "pave": [{"weight": 6, "block": "minecraft:stone_bricks"},
             {"weight": 3, "block": "minecraft:andesite"},
             {"weight": 2, "block": "minecraft:cobblestone"},
             {"weight": 1, "block": "minecraft:mossy_cobblestone"}],
    "path": "minecraft:gravel",
    "turf": "minecraft:grass_block[snowy=false]",
    # furniture
    "pew": "minecraft:spruce_stairs[facing=west,half=bottom,shape=straight,waterlogged=false]",
    "stall_n": "minecraft:dark_oak_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]",
    "stall_s": "minecraft:dark_oak_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]",
    "altar": "minecraft:chiseled_tuff",
    "altar_top": "minecraft:smooth_quartz_slab[type=bottom,waterlogged=false]",
    "candles": "minecraft:white_candle[candles=4,lit=true,waterlogged=false]",
    "font": "minecraft:cauldron",
    "lectern": "minecraft:lectern[facing=west,has_book=false,powered=false]",
    "lantern": "minecraft:lantern[hanging=false,waterlogged=false]",
    "lantern_h": "minecraft:lantern[hanging=true,waterlogged=false]",
    "bell": "minecraft:bell[attachment=ceiling,facing=north,powered=false]",
    "beam": "minecraft:dark_oak_planks",
    "louvre_x": "minecraft:dark_oak_slab[type=top,waterlogged=false]",
    "louvre_z": "minecraft:dark_oak_slab[type=bottom,waterlogged=false]",
    # the churchyard and the close
    "cwall": [{"weight": 4, "block": "minecraft:cobblestone"},
              {"weight": 2, "block": "minecraft:mossy_cobblestone"},
              {"weight": 1, "block": "minecraft:stone_bricks"}],
    "cap": "minecraft:stone_brick_slab[type=bottom,waterlogged=false]",
    "grave": "minecraft:mossy_stone_brick_wall[east=none,north=none,south=none,up=true,waterlogged=false,west=none]",
    "grave_flat": "minecraft:andesite_slab[type=bottom,waterlogged=false]",
    "yew_log": "minecraft:spruce_log[axis=y]",
    "yew": "minecraft:spruce_leaves[distance=1,persistent=true,waterlogged=false]",
    "post": "minecraft:dark_oak_fence[east=false,north=false,south=false,waterlogged=false,west=false]",
    "bench": "minecraft:spruce_stairs[facing=north,half=bottom,shape=straight,waterlogged=false]",
    "bench_s": "minecraft:spruce_stairs[facing=south,half=bottom,shape=straight,waterlogged=false]",
    "pot_a": "minecraft:red_tulip",
    "pot_b": "minecraft:cornflower",
    "pot_c": "minecraft:allium",
    "woodpile": "minecraft:spruce_log[axis=x]",
    "bush": "minecraft:oak_leaves[distance=1,persistent=true,waterlogged=false]",
    "rose": "minecraft:rose_bush[half=lower]",
    "rose_top": "minecraft:rose_bush[half=upper]",
    "lilac": "minecraft:lilac[half=lower]",
    "lilac_top": "minecraft:lilac[half=upper]",
    "fern": "minecraft:fern",
    "tuft": "minecraft:short_grass",
    "poppy": "minecraft:poppy",
    "daisy": "minecraft:oxeye_daisy",
}

# ---- the plan, piece-local ----
ZC = 14                     # the church's axis
NAVE = (10, 18)             # nave interior, z
PIER_N, PIER_S = 9, 19      # the arcades
AISLE_N, AISLE_S = (5, 8), (20, 23)
WALL_N, WALL_S = 4, 24      # the aisle walls
FRONT = (11, 12)            # the west front, two thick
X0 = 13                     # the nave's first interior column
PIERS = (16, 20, 24, 28, 32)
BAYS = (18, 22, 26, 30, 34)  # bay centres: windows and buttresses fall between piers
TR = (37, 45)               # the crossing and transept, interior x
TR_W, TR_E = 36, 46         # transept walls
TR_N, TR_S = 2, 26          # transept gable walls, z
CHOIR = (47, 52)            # choir interior x
CHOIR_E = 53                # choir aisles' east wall
APSE_C, APSE_R = 50, 4      # the apse's centre x and interior radius
TOWER = (11, 18, 19, 26)     # the bell tower's footprint (x0, x1, z0, z1)
CLOSE = (1, 10, 9, 38)      # the paved close before the west front
YARD = (15, 53, 28, 37)     # the churchyard's wall ring (x0, x1, z0, z1)

AISLE_TOP = 10              # aisle wall head; aisle vault under it
ARC_TOP = 9                 # arcade arch apex
CLER = (14, 19)             # clerestory window courses
NAVE_TOP = 21               # nave wall head
EAVE = 22                   # first roof course
TOWER_TOP = 29
SPIRE_TOP = 43


class Model:
    def __init__(self):
        self.v = {}
        self.region = {}    # (x, z) -> part stem, for the columns of each part

    def set(self, x, y, z, role):
        self.v[(x, y, z)] = role

    def box(self, x0, x1, y0, y1, z0, z1, role):
        for x in range(min(x0, x1), max(x0, x1) + 1):
            for y in range(min(y0, y1), max(y0, y1) + 1):
                for z in range(min(z0, z1), max(z0, z1) + 1):
                    self.v[(x, y, z)] = role

    def get(self, x, y, z):
        return self.v.get((x, y, z))


def hsh(*a):
    h = 2166136261
    for v in a:
        h = ((h ^ (v & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
    return h


def in_apse(x, z):
    return x >= APSE_C and (x - APSE_C) ** 2 + (z - ZC) ** 2 <= APSE_R * APSE_R + 2


def church_interior(x, z):
    """A column of the church's floor."""
    if X0 <= x <= TR_W and AISLE_N[0] <= z <= AISLE_S[1]:
        return not (TOWER[0] <= x <= TOWER[1] and z >= TOWER[2])
    if TR[0] <= x <= TR[1] and TR_N + 1 <= z <= TR_S - 1:
        return True
    if TR_E <= x <= CHOIR[1] and AISLE_N[0] <= z <= AISLE_S[1]:
        return True
    if in_apse(x, z) and NAVE[0] <= z <= NAVE[1]:
        return True
    return False


def church_footprint(x, z):
    """Interior plus its walls: every column within one cell of the interior."""
    if church_interior(x, z):
        return True
    return any(church_interior(x + dx, z + dz) for dx in (-1, 0, 1) for dz in (-1, 0, 1))


def gable(m, x0, x1, z0, z1, y0, along, wall_role="stone", end_walls=True):
    """A pitched roof over [x0..x1]x[z0..z1] from course y0, ridge along `along`."""
    if along == "x":
        lo, hi = z0, z1
        k = 0
        while lo <= hi:
            y = y0 + k
            if lo == hi:
                m.box(x0, x1, y, y, lo, lo, "ridge")
            else:
                m.box(x0, x1, y, y, lo, lo, "roof_s")
                m.box(x0, x1, y, y, hi, hi, "roof_n")
                if end_walls:   # the gable ends filled in behind the slopes
                    for x in (x0, x1):
                        m.box(x, x, y, y, lo + 1, hi - 1, wall_role)
            lo, hi, k = lo + 1, hi - 1, k + 1
    else:
        lo, hi = x0, x1
        k = 0
        while lo <= hi:
            y = y0 + k
            if lo == hi:
                m.box(lo, lo, y, y, z0, z1, "ridge")
            else:
                m.box(lo, lo, y, y, z0, z1, "roof_e")
                m.box(hi, hi, y, y, z0, z1, "roof_w")
                if end_walls:
                    for z in (z0, z1):
                        m.box(lo + 1, hi - 1, y, y, z, z, wall_role)
            lo, hi, k = lo + 1, hi - 1, k + 1


def pointed(m, axis, fixed, c0, c1, y0, y1, role):
    """A pointed opening in a wall: the cells [c0..c1] from y0 to y1, the head
    drawn in one course at each side (a lancet's two-centred head, block-built)."""
    w = c1 - c0 + 1
    for c in range(c0, c1 + 1):
        top = y1
        if w >= 3 and c in (c0, c1):
            top = y1 - 1
        if w >= 5 and c in (c0, c1):
            top = y1 - 2
        if w >= 5 and c in (c0 + 1, c1 - 1):
            top = y1 - 1
        for y in range(y0, top + 1):
            if axis == "x":
                m.set(fixed, y, c, role)
            else:
                m.set(c, y, fixed, role)


def rose(m, axis, fixed, cc, cy, r, depth=(0,)):
    """A rose window: a disc of coloured glass in a dressed ring, with spokes."""
    for dc in range(-r, r + 1):
        for dy in range(-r, r + 1):
            d2 = dc * dc + dy * dy
            if d2 > r * r + r:
                continue
            if d2 > (r - 1) * (r - 1) + (r - 1):
                role = "dress"
            elif dc == 0 or dy == 0 or abs(dc) == abs(dy):
                role = "tracery" if (dc, dy) != (0, 0) else "glass_gold"
            elif d2 <= 2:
                role = "glass_gold"
            else:
                role = "glass_red" if (abs(dc) + abs(dy)) % 2 else "glass_blue"
            for dd in depth:
                if axis == "x":
                    m.set(fixed + dd, cy + dy, cc + dc, role)
                else:
                    m.set(cc + dc, cy + dy, fixed + dd, role)


def build_model() -> Model:
    m = Model()
    # ---------- the ground: grass everywhere, then paving and paths over it
    for x in range(1, 57):
        for z in range(1, 39):
            m.set(x, 0, z, "turf")
    cx0, cx1, cz0, cz1 = CLOSE
    m.box(cx0, cx1 + 1, 0, 0, cz0, cz1, "pave")
    # a paved walk round the church's foot on the north, east and south
    for x in range(1, 57):
        for z in range(1, 39):
            if church_footprint(x, z):
                m.set(x, 0, z, "aisle_floor")
            elif any(church_footprint(x + dx, z + dz) for dx in (-1, 0, 1) for dz in (-1, 0, 1)):
                m.set(x, 0, z, "path")
    m.box(13, 56, 0, 0, 25, 27, "path")
    m.box(12, 14, 0, 0, 25, 38, "path")

    # ---------- the church shell
    top_of = {}
    for x in range(1, 57):
        for z in range(1, 39):
            if church_footprint(x, z) and not church_interior(x, z):
                # wall height: the nave and choir walls carry to the eave, the aisles' to theirs
                h = AISLE_TOP
                if TR_W <= x <= TR_E:
                    h = NAVE_TOP
                if in_apse(x + 1, z) or in_apse(x, z) or x >= CHOIR_E and NAVE[0] - 1 <= z <= NAVE[1] + 1:
                    h = NAVE_TOP
                if x in FRONT:
                    h = NAVE_TOP
                top_of[(x, z)] = h
                m.box(x, x, 1, h, z, z, "stone")
                m.set(x, 1, z, "plinth")
    # the interior floor: a chequer down the nave, plain stone in the aisles
    for x in range(1, 57):
        for z in range(1, 39):
            if church_interior(x, z):
                if NAVE[0] <= z <= NAVE[1] or TR[0] <= x <= TR[1] or x >= TR_E and NAVE[0] <= z <= NAVE[1]:
                    m.set(x, 0, z, "nave_a" if (x + z) % 2 else "nave_b")
                else:
                    m.set(x, 0, z, "aisle_floor")

    # the arcades: piers on both lines, pointed arches between them, the
    # triforium and clerestory wall over them up to the nave's wall head
    pier_xs = list(PIERS) + [TR_W, TR_E, 49]
    for zl in (PIER_N, PIER_S):
        for x in range(X0, CHOIR[1] + 1):
            if TR[0] <= x <= TR[1]:
                continue        # the crossing stands open to the transept
            if x in pier_xs:
                m.box(x, x, 1, NAVE_TOP, zl, zl, "pier")
                m.set(x, 1, zl, "plinth")
            else:
                # the arch: open below, its head stepping to the apex
                prev = max(p for p in [X0 - 1] + pier_xs if p < x)
                nxt = min(p for p in pier_xs + [CHOIR[1] + 1] if p > x)
                d = min(x - prev, nxt - x)
                spring = ARC_TOP - 2 + min(d, 2)
                m.box(x, x, spring, NAVE_TOP, zl, zl, "stone")
                m.set(x, AISLE_TOP + 1, zl, "dress")       # the string course over the arcade
                if d >= 2:
                    m.set(x, spring - 1, zl, "dress")
    # the crossing piers carry the tower-less crossing arches
    for (px, pz) in ((TR_W, PIER_N), (TR_W, PIER_S), (TR_E, PIER_N), (TR_E, PIER_S)):
        m.box(px, px, 1, NAVE_TOP, pz, pz, "pier")
    for z in range(NAVE[0], NAVE[1] + 1):
        for x in (TR_W, TR_E):
            d = min(z - PIER_N, PIER_S - z)
            m.box(x, x, 14 + min(d, 3), NAVE_TOP, z, z, "dress")
    for x in range(TR[0], TR[1] + 1):
        for z in (PIER_N, PIER_S):
            d = min(x - TR_W, TR_E - x)
            m.box(x, x, 14 + min(d, 3), NAVE_TOP, z, z, "dress")
    # the transept's own east/west walls beyond the aisles carry to the nave's head
    for x in (TR_W, TR_E):
        for z in list(range(TR_N, WALL_N + 1)) + list(range(WALL_S, TR_S + 1)):
            m.box(x, x, 1, NAVE_TOP, z, z, "stone")
    for z in (TR_N, TR_S):
        m.box(TR_W, TR_E, 1, NAVE_TOP, z, z, "stone")

    # aisle vaults: a flat ceiling under the lean-to, its beams on the bays
    for x in range(X0, CHOIR_E):
        if TR[0] <= x <= TR[1]:
            continue
        for zr in (AISLE_N, AISLE_S):
            for z in range(zr[0], zr[1] + 1):
                if (x, z) in top_of or not church_interior(x, z):
                    continue
                m.set(x, AISLE_TOP, z, "beam" if x in PIERS or x in (49,) else "stone")
    # aisle lean-to roofs, from the aisle wall's head up to the arcade wall
    for x in range(X0 - 1, CHOIR_E + 1):
        if TR_W <= x <= TR_E:
            continue
        zs_s = [] if TOWER[0] <= x <= TOWER[1] else list(range(WALL_S, PIER_S, -1))
        for k, z in enumerate(range(WALL_N, PIER_N)):
            m.set(x, AISLE_TOP + 1 + (k * 3) // 5, z, "roof_s")
        for k, z in enumerate(zs_s):
            m.set(x, AISLE_TOP + 1 + (k * 3) // 5, z, "roof_n")
    # fill the aisle roofs' risers so they read as one slope
    for x in range(X0 - 1, CHOIR_E + 1):
        if TR_W <= x <= TR_E:
            continue
        for z in list(range(WALL_N, PIER_N)) + list(range(PIER_S + 1, WALL_S + 1)):
            ys = [y for y in range(AISLE_TOP + 1, AISLE_TOP + 6) if m.get(x, y, z) in ("roof_s", "roof_n")]
            if ys:
                for y in range(AISLE_TOP + 1, ys[0]):
                    m.set(x, y, z, "roof")

    # the nave, choir and transept roofs
    gable(m, FRONT[0], CHOIR[1], PIER_N - 1, PIER_S + 1, EAVE, "x")
    gable(m, TR_W - 1, TR_E + 1, TR_N, TR_S, EAVE, "z")
    # the nave's wall head: a dressed cornice
    for x in range(FRONT[0], CHOIR[1] + 1):
        for z in (PIER_N, PIER_S):
            if (x, NAVE_TOP, z) in m.v:
                m.set(x, NAVE_TOP, z, "dress")
    # a flat inner vault course under the roof, so the nave reads as a ceiling
    for x in range(X0, CHOIR[1] + 1):
        for z in range(NAVE[0], NAVE[1] + 1):
            if church_interior(x, z):
                m.set(x, NAVE_TOP + 1, z, "beam" if x % 4 == 0 else "stone")
                if abs(z - ZC) <= 2:
                    m.set(x, NAVE_TOP + 2, z, "stone")
    for x in range(TR[0], TR[1] + 1):
        for z in range(TR_N + 1, TR_S):
            m.set(x, NAVE_TOP + 1, z, "beam" if z % 4 == 1 else "stone")
    # the apse: a half-cone of tiles over its round wall
    for x in range(APSE_C, 57):
        for z in range(1, 39):
            d2 = (x - APSE_C) ** 2 + (z - ZC) ** 2
            if x > CHOIR[1] and d2 <= (APSE_R + 1) ** 2 + 2:
                r = int(d2 ** 0.5)
                y = EAVE + max(0, APSE_R + 1 - r)
                for yy in range(NAVE_TOP + 1, y):
                    m.set(x, yy, z, "roof")
                m.set(x, y, z, "roof")
    # a flèche over the crossing
    m.box(41, 41, EAVE + 6, EAVE + 13, ZC, ZC, "spire")
    m.set(41, EAVE + 14, ZC, "finial")
    for (dx, dz) in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        m.box(41 + dx, 41 + dx, EAVE + 6, EAVE + 8, ZC + dz, ZC + dz, "spire")

    # ---------- the west front
    fx0, fx1 = FRONT
    for z in range(WALL_N, WALL_S + 1):
        m.box(fx0, fx1, 1, NAVE_TOP, z, z, "stone")
    # the front's gable stands proud of the roof, stepped
    for k in range(0, 12):
        lo, hi = PIER_N - 1 + k, PIER_S + 1 - k
        if lo > hi:
            break
        m.box(fx0, fx1, EAVE + k, EAVE + k, lo, hi, "stone")
    m.box(fx0, fx0, EAVE + 7, EAVE + 7, ZC, ZC, "quoin")
    # twin buttresses with pinnacles framing the nave on the front
    for z in (PIER_N - 1, PIER_S + 1):
        m.box(fx0 - 1, fx1, 1, NAVE_TOP + 4, z, z, "dress")
        m.box(fx0 - 1, fx0 - 1, NAVE_TOP + 5, NAVE_TOP + 7, z, z, "quoin")
        m.set(fx0 - 1, NAVE_TOP + 8, z, "finial")
    # corner buttresses at the south aisle's end
    m.box(fx0 - 1, fx1, 1, AISLE_TOP + 4, WALL_S, WALL_S, "dress")
    m.set(fx0 - 1, AISLE_TOP + 5, WALL_S, "finial")
    # the portal: a pointed arch three wide and six high, under a deep archivolt
    for x in (fx0 - 1, fx0, fx1):
        pointed(m, "x", x, ZC - 1, ZC + 1, 1, 6, AIR)
    for z in range(ZC - 3, ZC + 4):
        m.set(fx0 - 1, 1, z, "plinth") if abs(z - ZC) >= 2 else None
    for z in (ZC - 2, ZC + 2):
        m.box(fx0 - 1, fx0 - 1, 2, 6, z, z, "dress")
    for z in range(ZC - 2, ZC + 3):
        top = 8 - (1 if abs(z - ZC) == 2 else 0)
        m.box(fx0 - 1, fx0 - 1, 6 + (0 if abs(z - ZC) == 2 else 1), top, z, z, "dress")
    m.set(fx0 - 1, 9, ZC, "quoin")
    # the rose window over the portal
    rose(m, "x", fx0, ZC, 15, 4, depth=(0, 1))
    # side portals into the aisles: smaller lancet doors
    # lancets in the front over the aisles
    for zc in (6, 22):
        pointed(m, "x", fx0, zc - 1, zc, 3, 7, "glass")
        pointed(m, "x", fx1, zc - 1, zc, 3, 7, "glass")
        m.set(fx0 - 1, 2, zc, "sill") if False else None

    # ---------- windows
    for x in BAYS:
        for z_out in (WALL_N, WALL_S):
            if TOWER[0] <= x <= TOWER[1] and z_out == WALL_S:
                continue
            pointed(m, "z", z_out, x - 1, x + 1, 3, 7, "glass")
            m.set(x, 4, z_out, "tracery")
            m.set(x, 5, z_out, "tracery")
        for zl in (PIER_N, PIER_S):
            pointed(m, "z", zl, x - 1, x + 1, CLER[0], CLER[1], "glass")
            m.box(x, x, CLER[0], CLER[0] + 3, zl, zl, "tracery")
    # choir aisle and clerestory windows
    for x in (51,):
        for z_out in (WALL_N, WALL_S):
            pointed(m, "z", z_out, x - 1, x + 1, 3, 7, "glass")
        for zl in (PIER_N, PIER_S):
            pointed(m, "z", zl, x - 1, x + 1, CLER[0], CLER[1], "glass")
    # apse windows: tall lancets round the curve
    for wx in range(CHOIR[1] + 2, 57):
        for wz in range(NAVE[0] - 1, NAVE[1] + 2):
            if church_footprint(wx, wz) and not church_interior(wx, wz) and (wz - ZC) % 3 == 0:
                for y in range(3, 15):
                    if m.get(wx, y, wz) == "stone":
                        m.set(wx, y, wz, "glass")
    # transept gables: a rose in each, a door under the north one
    rose(m, "z", TR_N, 41, 15, 4)
    rose(m, "z", TR_S, 41, 15, 4)
    pointed(m, "z", TR_N, 40, 42, 1, 5, AIR)
    pointed(m, "z", TR_S, 40, 42, 1, 5, AIR)
    for zz in (TR_N, TR_S):
        for x in (38, 44):
            pointed(m, "z", zz, x, x, 3, 9, "glass")
    # transept side windows
    for x in (TR_W, TR_E):
        for z in (2, 24):
            pass
    # the south porch door from the south aisle into the churchyard walk
    pointed(m, "z", WALL_S, 25, 27, 1, 4, AIR)

    # ---------- flying buttresses
    for x in PIERS + (TR_E + 3,):
        if x == TR_E + 3:
            x = 49
        for side in (-1, 1):
            if side > 0 and TOWER[0] <= x <= TOWER[1]:
                continue
            zw = WALL_N if side < 0 else WALL_S
            zb = zw + side          # the buttress pier, one out from the aisle wall
            zb2 = zw + 2 * side
            m.box(x, x, 1, AISLE_TOP + 5, zb, zb, "dress")
            m.box(x, x, 1, AISLE_TOP + 1, zb2, zb2, "dress")
            m.set(x, AISLE_TOP + 2, zb2, "sill")
            m.set(x, AISLE_TOP + 6, zb, "quoin")
            m.set(x, AISLE_TOP + 7, zb, "finial")
            # the flyer: a half-arch from the pier's head to the nave wall
            stair = "fly_s" if side < 0 else "fly_n"
            for k in range(0, 5):
                z = zw - side * k
                y = AISLE_TOP + 4 + k
                if z == (PIER_N if side < 0 else PIER_S):
                    break
                m.set(x, y, z, stair)
                m.set(x, y + 1, z, "dress")

    # ---------- the bell tower
    tx0, tx1, tz0, tz1 = TOWER
    for x in range(tx0, tx1 + 1):
        for z in range(tz0, tz1 + 1):
            edge = x in (tx0, tx1) or z in (tz0, tz1)
            corner = x in (tx0, tx1) and z in (tz0, tz1)
            if edge:
                m.box(x, x, 1, TOWER_TOP, z, z, "quoin" if corner else "stone")
            else:
                m.box(x, x, 1, TOWER_TOP, z, z, AIR)
            m.set(x, 0, z, "aisle_floor")
    m.box(tx0 + 1, tx1 - 1, AISLE_TOP, AISLE_TOP, tz0 + 1, tz1 - 1, "beam")
    m.box(tx0 + 1, tx1 - 1, 21, 21, tz0 + 1, tz1 - 1, "beam")
    # string courses
    for y in (AISLE_TOP + 1, 17, 22):
        for x in range(tx0, tx1 + 1):
            for z in range(tz0, tz1 + 1):
                if x in (tx0, tx1) or z in (tz0, tz1):
                    m.set(x, y, z, "dress")
    # lancet slits, and the belfry's paired openings on every face
    for c in (14, 15):
        for y0, y1 in ((13, 17),):
            pointed(m, "z", tz1, c, c, y0, y1, "glass")
            pointed(m, "x", tx0, c + 8, c + 8, y0, y1, "glass")
    for face in ("n", "s", "e", "w"):
        for c0 in (13, 16) if face in "ns" else (tz0 + 1, tz0 + 4):
            c1 = c0 + 1
            if face == "n":
                pointed(m, "z", tz0, c0, c1, 23, 27, "louvre_x")
            elif face == "s":
                pointed(m, "z", tz1, c0, c1, 23, 27, "louvre_x")
            elif face == "w":
                pointed(m, "x", tx0, c0, c1, 23, 27, "louvre_z")
            else:
                pointed(m, "x", tx1, c0, c1, 23, 27, "louvre_z")
    for x in range(tx0, tx1 + 1):
        for z in range(tz0, tz1 + 1):
            if x in (tx0, tx1) or z in (tz0, tz1):
                if m.get(x, 23, z) in ("louvre_x", "louvre_z"):
                    m.set(x, 23, z, "sill")
                    # louvres: dark oak boards, a top and a bottom slab in turn, so the
                    # opening reads as slatted and no body passes or stands in it
                    for y in range(24, 28):
                        m.set(x, y, z, "louvre_x" if y % 2 == 0 else "louvre_z")
    # the bell, hung from the belfry's floor beam
    m.box(tx0 + 1, tx1 - 1, 28, 28, tz0 + 1, tz1 - 1, "beam")
    m.set(14, 27, tz0 + 3, "bell")
    m.set(15, 27, tz0 + 4, "bell")
    # battlement and corner pinnacles, then the spire
    for x in range(tx0, tx1 + 1):
        for z in range(tz0, tz1 + 1):
            if x in (tx0, tx1) or z in (tz0, tz1):
                if (x + z) % 2 == 0:
                    m.set(x, TOWER_TOP + 1, z, "dress")
    for x in (tx0, tx1):
        for z in (tz0, tz1):
            m.box(x, x, TOWER_TOP + 1, TOWER_TOP + 3, z, z, "quoin")
            m.set(x, TOWER_TOP + 4, z, "finial")
    # the spire: a steep broach of tiles, narrowing a cell each side every four courses
    for k in range(0, SPIRE_TOP - TOWER_TOP):
        i = min(k // 4, 2)
        a0, a1 = tx0 + 1 + i, tx1 - 1 - i
        b0, b1 = tz0 + 1 + i, tz1 - 1 - i
        y = TOWER_TOP + 1 + k
        for x in range(a0, a1 + 1):
            for z in range(b0, b1 + 1):
                if x in (a0, a1) or z in (b0, b1):
                    m.set(x, y, z, "spire")
    m.box(14, 15, SPIRE_TOP - 1, SPIRE_TOP, tz0 + 3, tz0 + 4, "spire")
    m.set(14, SPIRE_TOP + 1, tz0 + 3, "finial")

    # ---------- the inside
    # pews in the nave facing the altar, a walk down the middle
    for x in range(X0 + 4, PIERS[-1] + 1):
        if x in PIERS or x % 2 == 1:
            continue
        for z in list(range(NAVE[0] + 1, ZC - 1)) + list(range(ZC + 2, NAVE[1])):
            m.set(x, 1, z, "pew")
    # the font by the west door
    m.set(X0 + 1, 1, ZC - 3, "font")
    # choir stalls along both sides of the choir
    for x in range(TR_E + 1, CHOIR[1] - 1):
        if x == 49:
            continue
        m.set(x, 1, NAVE[0], "stall_s")
        m.set(x, 1, NAVE[1], "stall_n")
    # the high altar in the apse, on a step, with candles
    for z in range(NAVE[0] + 1, NAVE[1]):
        for x in range(CHOIR[1] + 1, 57):
            if church_interior(x, z):
                m.set(x, 0, z, "plinth")
    m.box(54, 54, 1, 1, ZC - 1, ZC + 1, "altar")
    m.set(54, 2, ZC - 1, "candles")
    m.set(54, 2, ZC + 1, "candles")
    m.set(CHOIR[1], 1, ZC + 2, "lectern")
    # side altars in the transept arms
    for z in (TR_N + 1, TR_S - 1):
        m.box(43, 44, 1, 1, z, z, "altar")
        m.set(43, 2, z, "candles")
        m.set(44, 2, z, "candles")
    # light: a lantern on the floor at the foot of every pier, hanging lanterns
    # under the aisle ceilings and under each arcade arch's apex
    for x in pier_xs:
        for z in (PIER_N + 1, PIER_S - 1):
            if church_interior(x, z) and m.get(x, 1, z) is None:
                m.set(x, 1, z, "lantern")
    for x in BAYS + (51,):
        for zr in (AISLE_N, AISLE_S):
            z = (zr[0] + zr[1]) // 2
            if m.get(x, AISLE_TOP, z) in ("stone", "beam") and church_interior(x, z):
                m.set(x, AISLE_TOP - 1, z, "lantern_h")
                m.set(x, 1, zr[1] if zr == AISLE_N else zr[0], "lantern") if m.get(x, 1, z) is None else None
    for x in range(TR[0] + 1, TR[1], 3):
        for z in (5, ZC, 23):
            m.set(x, NAVE_TOP, z, "lantern_h")
            m.set(x, 1, z, "lantern") if z != ZC else None
    for x in (X0 + 2, 22, 26, 30, 34, 48, 51):
        for z in (ZC - 1, ZC + 1):
            m.set(x, NAVE_TOP, z, "lantern_h")
    for z in (ZC - 2, ZC + 2):
        m.set(52, 1, z, "lantern")
    # the tower is not entered: its door is a blind arch
    # ---------- the close
    # benches facing the west front, pots and lamps at its corners
    for z in (ZC - 6, ZC - 5, ZC + 5, ZC + 6):
        m.set(4, 1, z, "bench_s" if False else "bench")
    for (x, z) in ((3, 10), (9, 10), (3, 36), (9, 36)):
        m.set(x, 1, z, "post")
        m.set(x, 2, z, "lantern")
    for (x, z, r) in ((10, 20, "pot_a"), (10, 21, "pot_b"), (10, 7, "pot_c"), (10, 25, "pot_a"),
                      (10, 26, "pot_c"), (10, 6, "pot_b")):
        m.set(x, 1, z, r)
        m.set(x, 0, z, "turf")
    # beds of roses and lilacs against the front's foot either side of the portal
    for z in (5, 7, 19, 21, 23):
        role = "rose" if z % 4 == 2 else "lilac"
        if m.get(fx0 - 1, 1, z) is None:
            m.set(fx0 - 1, 1, z, role)
            m.set(fx0 - 1, 2, z, role + "_top")
            m.set(fx0 - 1, 0, z, "turf")
    # a lawn with two trees north-west of the tower
    for (tx, tz) in ((5, 5),):
        m.box(tx, tx, 1, 4, tz, tz, "yew_log")
        for dx in range(-2, 3):
            for dz in range(-2, 3):
                for dy in (3, 4, 5, 6):
                    if abs(dx) + abs(dz) <= (3 if dy < 6 else 1) and (dx, dz) != (0, 0) or dy >= 5 and (dx, dz) == (0, 0):
                        if 2 <= tx + dx <= 9 and 2 <= tz + dz <= 7:
                            m.set(tx + dx, dy, tz + dz, "bush")
    # ---------- the churchyard
    yx0, yx1, yz0, yz1 = YARD
    for x in range(yx0, yx1 + 1):
        for z in range(yz0, yz1 + 1):
            if x in (yx0, yx1) or z in (yz0, yz1):
                m.set(x, 1, z, "cwall")
                m.set(x, 2, z, "cap")
    # gates: from the close on the west, from the south porch on the north, onto the town on the south
    for z in range(31, 34):
        m.set(yx0, 1, z, AIR)
        m.set(yx0, 2, z, AIR)
    for x in range(25, 28):
        m.set(x, 1, yz0, AIR)
        m.set(x, 2, yz0, AIR)
    for x in range(40, 43):
        m.set(x, 1, yz1, AIR)
        m.set(x, 2, yz1, AIR)
    # gate posts with lanterns
    for (x, z) in ((yx0, 30), (yx0, 34), (24, yz0), (28, yz0), (39, yz1), (43, yz1)):
        m.set(x, 2, z, "cwall")
        m.set(x, 3, z, "lantern")
    # the paths inside: west gate to the south gate, a spur up to the porch
    for x in range(yx0 + 1, yx1):
        for z in range(yz0 + 1, yz1):
            m.set(x, 0, z, "turf")
    m.box(yx0 + 1, 41, 0, 0, 32, 32, "path")
    m.box(41, 41, 0, 0, 32, yz1 - 1, "path")
    m.box(26, 26, 0, 0, yz0 + 1, 32, "path")
    # graves in rows, east of the porch path; headstones with a slab before each
    for x in range(29, yx1 - 1, 3):
        for z in (30, 34):
            if x in (41,) or abs(x - 41) <= 1:
                continue
            if hsh(x, z, 7) % 5 == 0:
                continue
            m.set(x, 1, z, "grave")
            m.set(x, 1, z + 1, "grave_flat")
    for x in range(yx0 + 3, 25, 3):
        for z in (30, 35):
            m.set(x, 1, z, "grave")
            m.set(x, 1, z + 1 if z == 30 else z - 1, "grave_flat")
    # yews at the yard's corners
    for (tx, tz) in ((yx0 + 2, yz1 - 2), (yx1 - 2, yz0 + 2), (yx1 - 2, yz1 - 2)):
        m.box(tx, tx, 1, 3, tz, tz, "yew_log")
        for dy in range(3, 8):
            r = 2 if dy < 6 else (1 if dy < 7 else 0)
            for dx in range(-r, r + 1):
                for dz in range(-r, r + 1):
                    if (dx, dz) == (0, 0) and dy <= 3:
                        continue
                    if abs(dx) + abs(dz) <= r + (1 if dy in (4, 5) else 0):
                        xx, zz = tx + dx, tz + dz
                        if yx0 < xx < yx1 and yz0 < zz < yz1:
                            m.set(xx, dy, zz, "yew")
    # flowers among the graves
    for x in range(yx0 + 1, yx1):
        for z in range(yz0 + 1, yz1):
            if m.get(x, 1, z) is None and m.get(x, 0, z) == "turf":
                h = hsh(x, z, 3) % 23
                if h == 0:
                    m.set(x, 1, z, "poppy")
                elif h == 1:
                    m.set(x, 1, z, "daisy")
                elif h in (2, 3):
                    m.set(x, 1, z, "tuft")
    # ---------- the church's foot outside: barrels and pots by the porch, a bench, ferns on the north
    m.box(21, 23, 1, 1, 25, 25, "woodpile")
    m.set(22, 2, 25, "woodpile")
    for x, r in ((29, "pot_b"), (30, "pot_a"), (31, "pot_c")):
        m.set(x, 1, 25, r)
        m.set(x, 0, 25, "turf")
    for x in (33, 34):
        m.set(x, 1, 27, "bench")
    for x in range(20, 36, 3):
        if m.get(x, 1, 2) is None and m.get(x, 0, 2) == "turf":
            m.set(x, 1, 2, "fern")

    refine(m)
    stair_shapes(m)
    # ---------- the parts: which columns are which
    for x in range(1, 57):
        for z in range(1, 39):
            if TOWER[0] <= x <= TOWER[1] and TOWER[2] <= z <= TOWER[3]:
                m.region[(x, z)] = "tower"
            elif church_footprint(x, z) or (x in PIERS + (49,) and z in (2, 3, 25, 26)) or (
                    FRONT[0] - 3 <= x <= FRONT[0] - 1 and WALL_N - 1 <= z <= TOWER[2] + 1):
                m.region[(x, z)] = "church"
            elif CLOSE[0] <= x <= CLOSE[1] and CLOSE[2] <= z <= CLOSE[3]:
                m.region[(x, z)] = "close"
            elif yx0 <= x <= yx1 and yz0 <= z <= yz1:
                m.region[(x, z)] = "churchyard"
    return m


# ===================================================================== the second pass
#
# Depth, after the references: the west front's portal is a stack of pointed
# archivolts stepping inward between buttresses that project three cells and set
# off twice as they rise (minecraftonline's Cathedral; minecraft.how's guide);
# every bay is a buttress pier between paired lancets under an oculus, the walls
# carry a plinth below and a cornice above (the abfielder gallery's rhythm); the
# nave, aisles, transept and choir are vaulted in stepped upside-down stairs with
# a transverse rib at every pier, over clustered piers and pointed arcades.

VAULT0 = 19                  # the vault springs here at the wall line, crown four higher
SHAFT_N = "shaft_n"          # a wall block joined to the pier on its south side
SHAFT_S = "shaft_s"          # joined on its north side
PIER_XS = tuple(PIERS) + (TR_W, TR_E, 49)


def nave_d(z):
    return min(z - NAVE[0], NAVE[1] - z)


def tr_d(x):
    return min(x - TR[0], TR[1] - x)


def vault_floor(x, z):
    """The lowest vault course over a church floor column, or None under no high vault."""
    if not church_interior(x, z):
        return None
    in_nave = NAVE[0] <= z <= NAVE[1] and X0 <= x <= CHOIR[1]
    in_tr = TR[0] <= x <= TR[1] and TR_N + 1 <= z <= TR_S - 1
    if x > CHOIR[1]:                              # the apse: a half-dome of the same profile
        r = ((x - APSE_C) ** 2 + (z - ZC) ** 2) ** 0.5
        return VAULT0 + max(0, min(4, 4 - int(r)))
    if in_nave and in_tr:                         # the crossing: a groin, the two barrels' union
        return VAULT0 + max(nave_d(z), tr_d(x))
    if in_nave:
        return VAULT0 + nave_d(z)
    if in_tr:
        return VAULT0 + tr_d(x)
    return None


def refine(m):
    PALETTE.update({
        "vault": "minecraft:tuff_bricks",
        "vault_n": "minecraft:tuff_brick_stairs[facing=north,half=top,shape=straight,waterlogged=false]",
        "vault_s": "minecraft:tuff_brick_stairs[facing=south,half=top,shape=straight,waterlogged=false]",
        "vault_e": "minecraft:tuff_brick_stairs[facing=east,half=top,shape=straight,waterlogged=false]",
        "vault_w": "minecraft:tuff_brick_stairs[facing=west,half=top,shape=straight,waterlogged=false]",
        "rib": "minecraft:polished_deepslate",
        "rib_n": "minecraft:polished_deepslate_stairs[facing=north,half=top,shape=straight,waterlogged=false]",
        "rib_s": "minecraft:polished_deepslate_stairs[facing=south,half=top,shape=straight,waterlogged=false]",
        "rib_e": "minecraft:polished_deepslate_stairs[facing=east,half=top,shape=straight,waterlogged=false]",
        "rib_w": "minecraft:polished_deepslate_stairs[facing=west,half=top,shape=straight,waterlogged=false]",
        "arch_e": "minecraft:tuff_brick_stairs[facing=east,half=top,shape=straight,waterlogged=false]",
        "arch_w": "minecraft:tuff_brick_stairs[facing=west,half=top,shape=straight,waterlogged=false]",
        SHAFT_N: "minecraft:tuff_brick_wall[east=none,north=none,south=tall,up=true,waterlogged=false,west=none]",
        SHAFT_S: "minecraft:tuff_brick_wall[east=none,north=tall,south=none,up=true,waterlogged=false,west=none]",
        "capital": "minecraft:chiseled_tuff",
        "cornice_n": "minecraft:stone_brick_stairs[facing=south,half=top,shape=straight,waterlogged=false]",
        "cornice_s": "minecraft:stone_brick_stairs[facing=north,half=top,shape=straight,waterlogged=false]",
        "set_e": "minecraft:stone_brick_stairs[facing=east,half=bottom,shape=straight,waterlogged=false]",
        "kneel": "minecraft:spruce_slab[type=bottom,waterlogged=false]",
        "pot_a": "minecraft:potted_red_tulip",
        "pot_b": "minecraft:potted_cornflower",
        "pot_c": "minecraft:potted_azure_bluet",
    })
    ceiling_old = (None, AIR, "beam", "stone", "lantern_h", "dress")

    # ---------- the high vaults: nave, crossing, transept, choir, apse
    for x in range(X0, 57):
        for z in range(1, 39):
            v = vault_floor(x, z)
            if v is None:
                continue
            # clear the old flat ceiling's courses below the vault
            for y in range(NAVE_TOP - 1, v):
                if m.get(x, y, z) in ("beam", "stone", "lantern_h") and y > NAVE_TOP - 1:
                    m.set(x, y, z, AIR)
            # the shell above the vault, up to the roof, is masonry: no cavity
            for y in range(v, EAVE + 8):
                if m.get(x, y, z) in ceiling_old:
                    m.set(x, y, z, "vault")
            # the vault's face: a step of upside-down stairs, the back to the higher side
            rib = x in PIER_XS or (TR[0] <= x <= TR[1] and z in (PIER_N + 0, PIER_S)) or z in (
                TR_N + 1, TR_S - 1) and TR[0] <= x <= TR[1]
            in_nave = NAVE[0] <= z <= NAVE[1] and x <= CHOIR[1]
            role = None
            if v < VAULT0 + 4:
                if in_nave and (not (TR[0] <= x <= TR[1]) or nave_d(z) >= tr_d(x)):
                    role = "n" if z < ZC else "s"
                elif TR[0] <= x <= TR[1]:
                    role = "w" if x < (TR[0] + TR[1]) // 2 else "e"
            if x in PIER_XS and in_nave:
                face = ("rib_" + role) if role else "rib"
            else:
                face = ("vault_" + role) if role else "vault"
            m.set(x, v, z, face)
            # a transverse rib hangs one course under the vault at every pier
            if x in PIER_XS and in_nave and v - 1 > VAULT0 - 2:
                m.set(x, v - 1, z, ("rib_" + role) if role else "rib")

    # ---------- the aisle vaults: corbelled stairs at both walls, a rib at every pier
    for x in range(X0, CHOIR_E):
        if TR[0] <= x <= TR[1]:
            continue
        for (z0, z1) in (AISLE_N, AISLE_S):
            for z in range(z0, z1 + 1):
                if not church_interior(x, z):
                    continue
                m.set(x, AISLE_TOP, z, "vault")
                if z == z0:
                    m.set(x, AISLE_TOP - 1, z, "rib_n" if x in PIER_XS else "vault_n")
                elif z == z1:
                    m.set(x, AISLE_TOP - 1, z, "rib_s" if x in PIER_XS else "vault_s")
                elif x in PIER_XS:
                    m.set(x, AISLE_TOP - 1, z, "rib")

    # ---------- the arcades: clustered piers and pointed arches
    for zl in (PIER_N, PIER_S):
        nave_side = zl + 1 if zl == PIER_N else zl - 1
        aisle_side = zl - 1 if zl == PIER_N else zl + 1
        for x in range(X0, CHOIR[1] + 1):
            if TR[0] <= x <= TR[1]:
                continue
            if zl == PIER_S and TOWER[0] <= x <= TOWER[1]:
                continue            # the tower's north wall: the arcade begins east of it
            if x in PIER_XS:
                m.box(x, x, 1, NAVE_TOP, zl, zl, "pier")
                m.set(x, 1, zl, "plinth")
                for zs in (nave_side, aisle_side):
                    if not church_interior(x, zs):
                        continue
                    sh = SHAFT_S if zs > zl else SHAFT_N
                    m.set(x, 1, zs, "plinth")
                    m.box(x, x, 2, 7, zs, zs, sh)
                    m.set(x, 8, zs, "capital")
                    if zs == nave_side:       # the vaulting shaft runs on up to the springing
                        m.box(x, x, 9, VAULT0 - 2, zs, zs, sh)
                        m.set(x, VAULT0 - 1, zs, "capital")
                continue
            prev = max(p for p in (X0 - 1,) + PIER_XS if p < x)
            nxt = min(p for p in PIER_XS + (CHOIR[1] + 1,) if p > x)
            d = min(x - prev, nxt - x)
            top = 7 + min(d, 2)
            m.box(x, x, 1, top, zl, zl, AIR)
            for y in range(top + 1, NAVE_TOP + 1):
                if m.get(x, y, zl) in (None, AIR, "dress", "glass", "tracery"):
                    m.set(x, y, zl, "stone")
            if nxt - prev - 1 >= 3 and d == 2:
                m.set(x, top + 1, zl, "dress")             # the keystone
            elif x - prev < nxt - x or nxt - prev - 1 < 3 and x - prev == 1:
                m.set(x, top + 1, zl, "arch_w")            # the shoulder springs from the pier west
            else:
                m.set(x, top + 1, zl, "arch_e")
            m.set(x, AISLE_TOP + 1, zl, "dress")           # the string course over the arcade

    # ---------- windows: paired lancets under an oculus, a hood over them
    def window(zw, xc, y0, h):
        for xx in range(xc - 1, xc + 2):
            for y in range(y0 - 1, y0 + h + 2):
                if m.get(xx, y, zw) in ("glass", "tracery", None, AIR, "dress", "stone"):
                    m.set(xx, y, zw, "stone")
        for xx in (xc - 1, xc + 1):
            m.box(xx, xx, y0, y0 + h - 1, zw, zw, "glass")
        m.box(xc, xc, y0, y0 + h - 1, zw, zw, "dress")      # the mullion
        m.set(xc, y0 + h, zw, "glass_gold")                 # the oculus
        m.set(xc, y0 - 1, zw, "dress")
        for xx in (xc - 1, xc + 1):
            m.set(xx, y0 - 1, zw, "dress")                  # the sill
    for xc in BAYS + (51,):
        for zw in (WALL_N, WALL_S):
            if TOWER[0] <= xc <= TOWER[1] and zw == WALL_S:
                continue
            if zw == WALL_S and 24 <= xc <= 28:
                window(zw, xc, 6, 2)                        # over the south porch door
                continue
            window(zw, xc, 3, 5)
        for zl in (PIER_N, PIER_S):
            if TOWER[0] <= xc <= TOWER[1] and zl == PIER_S:
                continue
            window(zl, xc, 14, 4)
    # the porch door through the south aisle wall stays open under its window
    m.box(25, 27, 1, 4, WALL_S, WALL_S, AIR)

    # ---------- the walls' second and third depths: a plinth below, a cornice above
    for x in range(X0, CHOIR_E + 1):
        if TR_W <= x <= TR_E:
            continue
        for (zw, zo, cor) in ((WALL_N, WALL_N - 1, "cornice_n"), (WALL_S, WALL_S + 1, "cornice_s")):
            if TOWER[0] <= x <= TOWER[1] and zw == WALL_S:
                continue
            if m.get(x, AISLE_TOP, zw) is None or m.get(x, 2, zo) not in (None, AIR):
                continue
            if zw == WALL_S and 24 <= x <= 28:
                continue                                    # the porch door's walk
            m.set(x, 1, zo, "plinth")
            if m.get(x, AISLE_TOP, zo) in (None, AIR):
                m.set(x, AISLE_TOP, zo, cor)
    for x in range(FRONT[0], CHOIR[1] + 1):
        if TR_W <= x <= TR_E:
            continue
        for (zo, cor) in ((PIER_N - 1, "cornice_n"), (PIER_S + 1, "cornice_s")):
            if TOWER[0] <= x <= TOWER[1] and zo == PIER_S + 1:
                continue
            if m.get(x, NAVE_TOP, zo) in (None, AIR):
                m.set(x, NAVE_TOP, zo, cor)

    # ---------- the west front, rebuilt in depth
    fx0, fx1 = FRONT
    for x in range(fx0 - 4, fx0):
        for z in range(WALL_N - 1, TOWER[2] + 2):
            for y in range(1, 32):
                m.v.pop((x, y, z), None)
            m.set(x, 0, z, "pave")
    for z in range(WALL_N, TOWER[2]):
        for x in (fx0, fx1):
            for y in range(1, NAVE_TOP + 1):
                m.set(x, y, z, "stone")
    # buttresses three deep, setting off at courses 9 and 17, a pinnacle on top
    for (za, zb) in ((WALL_N - 1, WALL_N), (PIER_N - 1, PIER_N), (TOWER[2], TOWER[2] + 1)):
        for z in (za, zb):
            m.box(fx0 - 3, fx0 - 1, 1, 8, z, z, "dress")
            m.set(fx0 - 3, 9, z, "set_e")
            m.box(fx0 - 2, fx0 - 1, 9, 16, z, z, "dress")
            m.set(fx0 - 2, 17, z, "set_e")
            top = NAVE_TOP + 4 if za != WALL_N - 1 else AISLE_TOP + 6
            m.box(fx0 - 1, fx0 - 1, 17, top, z, z, "dress")
            m.set(fx0 - 1, top + 1, z, "quoin")
            m.set(fx0 - 1, 1, z, "plinth")
        m.set(fx0 - 1, top + 2, za, "finial")
    # the portal: four orders of pointed arches stepping in from the porch's face
    porch_z0, porch_z1 = PIER_N + 1, TOWER[2] - 1        # between the buttresses
    PORCH_TOP = 12
    for x in range(fx0 - 3, fx0):
        for z in range(porch_z0, porch_z1 + 1):
            m.box(x, x, 1, PORCH_TOP, z, z, "dress" if (fx0 - x) % 2 else "stone")
    orders = {fx1: 1, fx0: 1, fx0 - 1: 2, fx0 - 2: 3, fx0 - 3: 4}   # the half-width each order opens
    for x, half in orders.items():
        for dz in range(-half, half + 1):
            top = 5 + half - abs(dz) + (1 if half > 1 else 0)
            m.box(x, x, 1, top, ZC + dz, ZC + dz, AIR)
            m.set(x, 0, ZC + dz, "pave")
    for x in range(fx0 - 3, fx1 + 1):
        m.set(x, 0, ZC, "nave_a")
    m.set(fx0, 8, ZC, "quoin")                           # the tympanum's boss
    # the porch's gable (a wimperg) over the arches, with a finial
    for k in range(0, 6):
        lo, hi = porch_z0 + k, porch_z1 - k
        if lo > hi:
            break
        m.box(fx0 - 3, fx0 - 1, PORCH_TOP + 1 + k, PORCH_TOP + 1 + k, lo, hi, "stone")
        m.set(fx0 - 3, PORCH_TOP + 1 + k, lo, "set_e" if False else "dress")
        m.set(fx0 - 3, PORCH_TOP + 1 + k, hi, "dress")
    m.set(fx0 - 3, PORCH_TOP + 6, ZC, "finial")
    # the rose: glass in the inner plane, the outer plane cut back round it
    rose(m, "x", fx1, ZC, 17, 4)
    for dz in range(-4, 5):
        for dy in range(-4, 5):
            d2 = dz * dz + dy * dy
            if d2 <= 16 + 4:
                m.set(fx0, 17 + dy, ZC + dz, "dress" if d2 > 9 + 3 else AIR)
    # the north aisle's bay of the front: a tall lancet, set back one cell
    for z in (WALL_N + 1, WALL_N + 2):
        m.box(fx1, fx1, 3, 9, z, z, "glass")
        m.box(fx0, fx0, 3, 9, z, z, AIR)
        m.set(fx0, 2, z, "sill")
    m.set(fx1, 10, WALL_N + 1, "glass_gold")
    # a blind arcade across the front's gable over the rose
    for z in range(PIER_N + 1, PIER_S):
        if z % 2 == 0:
            m.box(fx0, fx0, 23, 25, z, z, AIR)
            m.set(fx0, 22, z, "sill")
    # flower beds before the front's north bay
    for z in (WALL_N + 1, WALL_N + 2):
        m.set(fx0 - 4, 0, z, "turf")
        m.set(fx0 - 4, 1, z, "rose" if z % 2 else "lilac")
        m.set(fx0 - 4, 2, z, ("rose" if z % 2 else "lilac") + "_top")

    # ---------- pews of stairs and slabs: a seat, and a kneeler before the next
    for x in range(X0 + 3, PIERS[-1] + 2):
        for z in list(range(NAVE[0] + 1, ZC - 1)) + list(range(ZC + 2, NAVE[1])):
            if m.get(x, 1, z) in ("pew", "kneel", None):
                m.v.pop((x, 1, z), None)
                if x in PIER_XS or (x + 1) in PIER_XS:
                    continue
                m.set(x, 1, z, "pew" if x % 2 == 0 else "kneel")

    # ---------- light: lanterns where people sit and walk, gathered at the altar
    for x in BAYS + (51,):
        for z in (AISLE_N[0], AISLE_S[1]):
            if church_interior(x, z) and m.get(x, 1, z) is None:
                m.set(x, 1, z, "lantern")
        if X0 <= x <= CHOIR[1]:
            v = vault_floor(x, ZC)
            if v is not None:
                m.set(x, v - 1, ZC, "lantern_h")
    for x in range(X0 + 1, PIERS[-1] + 1, 4):
        for z in (ZC - 1, ZC + 1):
            if m.get(x, 1, z) is None:
                m.set(x, 1, z, "lantern")
    for x in range(TR[0], TR[1] + 1, 4):
        for z in (TR_N + 2, TR_S - 2, PIER_N + 1, PIER_S - 1):
            if church_interior(x, z) and m.get(x, 1, z) is None:
                m.set(x, 1, z, "lantern")
    for z in (ZC - 3, ZC + 3):
        if church_interior(53, z) and m.get(53, 1, z) is None:
            m.set(53, 1, z, "lantern")
    # the north lawn's tree and the churchyard's yews shade their floor: a lamp beside each
    m.set(3, 1, 7, "post")
    m.set(3, 2, 7, "lantern")
    m.set(52, 1, 33, "post")
    m.set(52, 2, 33, "lantern")


DIRS = {"north": (0, -1), "south": (0, 1), "east": (1, 0), "west": (-1, 0)}
CCW = {"north": "west", "west": "south", "south": "east", "east": "north"}


def stair_shapes(m):
    """Write every stair's `shape` as the game derives it from its neighbours
    (StairBlock.getStairsShape), so the written world is the world the server keeps."""
    def props(role):
        b = PALETTE.get(role)
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
            if name not in PALETTE:
                PALETTE[name] = PALETTE[r].replace("shape=straight", f"shape={shape}")
                LOW.add(name)
            new[(x, y, z)] = name
    m.v.update(new)


OPP = {"north": "south", "south": "north", "east": "west", "west": "east"}


class Cathedral(Place):
    """The starter's place, with the cathedral's model in place of the empty room."""

    def lay_parts(self, parts):
        self.model = build_model()
        by_stem = {p["id"].removeprefix("part/"): p for p in parts}
        self.parts = []
        self.col_part = {}
        for stem, p in by_stem.items():
            e = {"part": p, "region": f"part-{stem}", "walked": p.get("reached", True), "cols": []}
            self.parts.append(e)
            for c, st in self.model.region.items():
                if st == stem:
                    e["cols"].append(c)
                    self.col_part[c] = e
        self.reach()

    def seam_space(self, s):
        (x0, _, z0), (x1, _, z1) = s["seam"]["cells"]
        e = self.col_part.get(((x0 + x1) // 2, (z0 + z1) // 2))
        return e["region"] if e is not None and e["walked"] else "room"

    def base_cell(self, x, y, z):
        kind = Place.base_cell(self, x, y, z)
        # the ring's four corners: nothing stands there, so no post marks the plot;
        # their ground course is the room's to walk
        if not self.in_space_xz(x, z) and kind == ("fill", "wall"):
            return ("claim", "room", None)
        if not self.in_space_xz(x, z):
            return kind
        if kind[0] == "claim" and kind[1].endswith("-way"):
            return kind          # a seam's opening is the connection's, kept clear
        r = self.model.get(x, y, z)
        if r is None or r == AIR:
            if y < self.datum.value:
                return ("fill", "turf")
            if (x, y, z) in self.unwalked:
                return ("claim", "unwalked", None)
            return kind if kind[0] == "claim" else ("claim", "room", None)
        if r in FULL:
            return ("fill", r)
        # a block a body stands in or on: inside the space its column is
        if (x, y, z) in self.unwalked:
            return ("claim", "unwalked", r)
        if (x, y, z) not in self.reached:
            return ("fill", r)
        e = self.col_part.get((x, z))
        return ("claim", e["region"] if e is not None else "room", r)

    def reach(self):
        """Every standable cell a body cannot walk to from the plot's edges: the
        roof spaces, the wall heads, the aisle roofs. Claimed as `unwalked`."""
        self.unwalked = set()
        role = lambda x, y, z: self.model.get(x, y, z)
        lo, hi = self.space

        def kind(x, y, z):
            if not (lo[0] <= x <= hi[0] and lo[2] <= z <= hi[2]) or y < 0 or y > hi[1] + 1:
                return "pass"
            r = role(x, y, z)
            if r is None or r == AIR:
                return "full" if y < self.datum.value else "pass"
            if r in FULL:
                return "full"
            if r in TALL:
                return "tall"
            if r in LOW:
                return "low"
            return "pass"

        def standable(x, y, z):
            k = kind(x, y, z)
            if k not in ("pass", "low") or kind(x, y + 1, z) != "pass":
                return False
            return k == "low" or kind(x, y - 1, z) in ("full", "low", "tall")

        cols = {(x, z) for x in range(lo[0], hi[0] + 1) for z in range(lo[2], hi[2] + 1)}
        cells = {(x, y, z) for (x, z) in cols for y in range(1, hi[1] + 1) if standable(x, y, z)}
        crowns = {c for c in cells if role(c[0], c[1] - 1, c[2]) in ("yew", "bush", "yew_log")}
        walk = cells - crowns
        start = [(x, y, z) for (x, y, z) in walk if y == self.datum.value and (x in (lo[0], hi[0]) or z in (lo[2], hi[2]))]
        seen, todo = set(start), list(start)
        while todo:
            x, y, z = todo.pop()
            for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, nz = x + dx, z + dz
                h0 = y + (0.5 if kind(x, y, z) == "low" else 0)
                for ny in (y, y + 1):
                    if ny + (0.5 if kind(nx, ny, nz) == "low" else 0) - h0 > 1:
                        continue
                    if (nx, ny, nz) in walk and (nx, ny, nz) not in seen:
                        seen.add((nx, ny, nz))
                        todo.append((nx, ny, nz))
                        break
                else:
                    ny = y - 1
                    while ny >= 1 and kind(nx, ny, nz) == "pass" and (nx, ny, nz) not in cells:
                        ny -= 1
                    if (nx, ny, nz) in walk and (nx, ny, nz) not in seen and kind(nx, y, nz) == "pass":
                        seen.add((nx, ny, nz))
                        todo.append((nx, ny, nz))
        for c in cells - seen:
            e = self.col_part.get((c[0], c[2]))
            if e is None or e["walked"]:
                self.unwalked.add(c)
        # A cavity sealed from the sky and the ground (the roof space over a
        # vault): every cell of its air is out of walk, not only its floor.
        self.reached = seen
        air = lambda c: role(*c) in (None, AIR) and lo[0] <= c[0] <= hi[0] and lo[2] <= c[2] <= hi[2] and 1 <= c[1] <= hi[1]
        done = set()
        for c0 in sorted(self.unwalked):
            if c0 in done:
                continue
            comp, todo, open_ = {c0}, [c0], False
            while todo:
                x, y, z = todo.pop()
                for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
                    n = (x + d[0], y + d[1], z + d[2])
                    if n in comp:
                        continue
                    if not air(n):
                        inside = lo[0] <= n[0] <= hi[0] and lo[2] <= n[2] <= hi[2] and 1 <= n[1] <= hi[1]
                        if not inside:
                            open_ = True      # it runs out of the piece: the sky or the ring
                        continue
                    if n in seen:
                        open_ = True
                        continue
                    comp.add(n)
                    todo.append(n)
                if open_ or len(comp) > 20000:
                    open_ = True
                    break
            done |= comp
            if not open_:
                for c in comp:
                    e = self.col_part.get((c[0], c[2]))
                    if e is None or e["walked"]:
                        self.unwalked.add(c)

    def cuts(self, axis):
        n = self.n[axis]
        out = super().cuts(axis)
        best = {b.value: b for b in out}
        for v in range(n):
            best.setdefault(v, lit(v))
        return [best[v] for v in sorted(best)]


def body(p, rules):
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


FULL = {"floor", "wall", "lid", "stone", "dress", "quoin", "pier", "plinth", "glass", "glass_blue", "glass_red",
        "glass_gold", "roof", "spire", "nave_a", "nave_b", "aisle_floor", "pave", "path", "turf", "altar", "beam",
        "cwall", "yew_log", "yew", "bush", "woodpile", "font", "louvre_x", "louvre_z",
        "vault", "rib", "capital"}
TALL = {"tracery", "grave", "post", "finial", "shaft_n", "shaft_s"}
LOW = {"roof_n", "roof_s", "roof_e", "roof_w", "ridge", "fly_n", "fly_s", "sill", "pew", "stall_n", "stall_s",
       "bench", "bench_s", "cap", "grave_flat", "altar_top", "candles", "lantern",
       "lectern", "vault_n", "vault_s", "vault_e", "vault_w", "rib_n", "rib_s", "rib_e", "rib_w", "arch_e",
       "arch_w", "cornice_n", "cornice_s", "set_e", "kneel", "pot_a", "pot_b", "pot_c"}

_starter_contract = contract


def contract(p):
    out = _starter_contract(p)
    if p.unwalked:
        out.setdefault("no_body", {})["unwalked"] = {
            "reason": "the roof spaces over the vaults, the aisle roofs, the wall heads and the belfry's sills: seen, never stood on"}
    return out



def shown_faces(p):
    """The four sides; the top course is the sky over the spire, which holds nothing."""
    return ["east", "north", "south", "west"]

MARK_AT = {"node-cathedral": (41, ZC, "west")}   # in the crossing, facing the west door


def marks(p, inner):
    """Every owed name, marked where the cathedral puts it."""
    out = inner
    for name in reversed(p.a["owed_anchors"]):
        stem = name.removeprefix("anchor/")
        x, z, facing = MARK_AT[stem]
        assert p.walkable(p.cell(x, p.datum.value, z)), stem
        mark = {"anchor": stem, "at": "offset", "facing": facing, "y": p.datum.expr, "x": num(x), "z": num(z)}
        out = {"body": out, "mark": mark, "op": "mark"}
    return out


if __name__ == "__main__":
    raise SystemExit(main())
