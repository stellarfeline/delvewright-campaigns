"""The place kit: a piece designed in the frame `delvec allocation` hands a place.

`Piece(node)` reads the allocation (by running `delvec allocation`), knows which
cells of the frame the place owns, where its seams are and what ground it was
handed, and offers drawing helpers in world or frame coordinates. `finish()`
writes the program to `programs/<stem>.json`, where `delvec detail` reads it.
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CAMPAIGN = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import voxgrammar  # noqa: E402
import blocks  # noqa: E402
import mapmodel as M  # noqa: E402

AIR = "minecraft:air"
VOID = "minecraft:structure_void"


def _delvec():
    return os.environ.get("DELVEC", "delvec")


def allocation(node):
    out = subprocess.run(
        [_delvec(), "--prefabs", os.environ["DELVEWRIGHT_PREFABS"], "allocation", CAMPAIGN, node],
        capture_output=True, text=True)
    if out.returncode != 0:
        raise SystemExit("allocation %s failed:\n%s" % (node, out.stderr[-3000:]))
    return json.loads(out.stdout)


def stem(i):
    return i.split("/", 1)[1]


def boxcells(c0, c1):
    for x in range(min(c0[0], c1[0]), max(c0[0], c1[0]) + 1):
        for y in range(min(c0[1], c1[1]), max(c0[1], c1[1]) + 1):
            for z in range(min(c0[2], c1[2]), max(c0[2], c1[2]) + 1):
                yield (x, y, z)


class Piece:
    def __init__(self, node):
        self.node = node
        self.a = a = allocation(node)
        self.p = M.P[node]
        self.X, self.Y, self.Z = a["extent"]
        self.wmin = tuple(a["world_min"])
        self.dy = a["datum_y"]  # local walk plane y (feet)
        self.space = (tuple(a["space"][0]), tuple(a["space"][1]))
        self.prog = voxgrammar.Program("the-stranding-" + stem(node), (self.X, self.Y, self.Z))
        self.voids = set()
        self.void_owner = {}
        for v in a["voids"]:
            for c in boxcells(v["cells"][0], v["cells"][1]):
                self.voids.add(c)
                self.void_owner[c] = v["owner"]
        self.seams = a["seams"]
        self.roof = a.get("roof")
        self.ground = a.get("ground") or {}
        self.spaces = {}
        self.edges = []
        self.no_body = {}
        self.marks_done = set()
        self.majority_ack = None

    # -- coordinates --------------------------------------------------------
    def L(self, x, y, z):
        return (x - self.wmin[0], y - self.wmin[1], z - self.wmin[2])

    def W(self, x, y, z):
        return (x + self.wmin[0], y + self.wmin[1], z + self.wmin[2])

    def owned(self, c):
        x, y, z = c
        return 0 <= x < self.X and 0 <= y < self.Y and 0 <= z < self.Z and c not in self.voids

    # -- drawing (frame coordinates) ------------------------------------------
    def set(self, x, y, z, block):
        if self.owned((x, y, z)):
            self.prog.set(x, y, z, block)

    def get(self, x, y, z):
        return self.prog.get(x, y, z)

    def box(self, x0, y0, z0, x1, y1, z1, block):
        for c in boxcells((x0, y0, z0), (x1, y1, z1)):
            self.set(*c, block)

    def wset(self, x, y, z, block):
        self.set(*self.L(x, y, z), block)

    def wbox(self, x0, y0, z0, x1, y1, z1, block):
        a = self.L(x0, y0, z0)
        b = self.L(x1, y1, z1)
        self.box(*a, *b, block)

    # -- the handed things ---------------------------------------------------
    def seam(self, eid):
        for s in self.seams:
            if s["edge"] == eid:
                return s
        raise KeyError(eid)

    def seam_cells(self, eid):
        s = self.seam(eid)
        return list(boxcells(s["cells"][0], s["cells"][1]))

    def station(self, aid):
        x, y, z, f = M.STATIONS[aid]
        return self.L(x, y, z), f

    # -- the spatial contract ------------------------------------------------
    def claim(self, cells, region, only_air=False, share=False):
        """only_air: claim the cells a body can be in (air and the thin and
        partial blocks it stands in or on), leaving the full blocks. share: a
        cell already claimed by another opening is claimed by both (two
        openings meeting at a corner column)."""
        for c in cells:
            if not self.owned(c):
                continue
            if only_air and blocks.is_full(self.prog.get(*c)):
                continue
            old = self.prog.region.get(c)
            if share and old and old != region:
                olds = old if isinstance(old, tuple) else (old,)
                if region not in olds:
                    self.prog.region[c] = olds + (region,)
                continue
            self.prog.region[c] = region

    def claim_box(self, x0, y0, z0, x1, y1, z1, region, only_air=False):
        self.claim(boxcells((x0, y0, z0), (x1, y1, z1)), region, only_air)

    def roof_no_body(self, y_from, reason="the roof and the loft space under it, which nobody walks"):
        self.no_body["roof"] = {"reason": reason}
        for c in boxcells((0, y_from, 0), (self.X - 1, self.Y - 1, self.Z - 1)):
            if self.owned(c) and not blocks.is_full(self.prog.get(*c)) and c not in self.prog.region:
                self.prog.region[c] = "roof"
        self.majority_ack = ("a building that owns its outside owns its roof, and a pitched roof is "
                             "more standable surface than the room under it; nobody walks it")

    def space_decl(self, name, envelope):
        self.spaces[name] = {"envelope": envelope}

    def edge(self, **e):
        self.edges.append(e)

    def mark(self, stem_, cell, facing=None, role=None):
        self.prog.mark(stem_, *cell, facing=facing, role=role)
        self.marks_done.add(stem_)

    # -- finishing ---------------------------------------------------------
    def finish(self, entry, shown_faces=None):
        # an owed unlock affordance stands on this side of its barred seam
        for name in self.a.get("owed_anchors", []):
            if "/" not in name:
                continue
            st = name.split("/", 1)[1]
            if st.startswith("unlock-") and st not in self.marks_done:
                eid = "edge/" + st[len("unlock-"):]
                s = self.seam(eid)
                (x0, y0, z0), (x1, y1, z1) = s["cells"]
                ix, _, iz = INWARD[s["face"]]
                c = (min(x0, x1) + ix, min(y0, y1), min(z0, z1) + iz)
                if not s["owns_plane"]:
                    c = (min(x0, x1) + ix, min(y0, y1), min(z0, z1) + iz)
                self.mark(st, c, facing=s["face"])
        blocks.derive(self.prog.cells)
        for c in self.voids:
            self.prog.cells[c] = VOID
        self.prog.contract = {"entry": entry, "spaces": self.spaces, "edges": self.edges}
        if self.no_body:
            self.prog.contract["no_body"] = self.no_body
        if self.majority_ack:
            self.prog.contract["no_body_majority_ack"] = self.majority_ack
        if shown_faces:
            # a face is shown only when the piece has something on it; a place
            # standing aloft shows its underside too (DW0885)
            def has(face):
                X, Y, Z = self.X, self.Y, self.Z
                rng = {"up": (range(X), [Y - 1], range(Z)), "down": (range(X), [0], range(Z)),
                       "north": (range(X), range(Y), [0]), "south": (range(X), range(Y), [Z - 1]),
                       "west": ([0], range(Y), range(Z)), "east": ([X - 1], range(Y), range(Z))}[face]
                for x in rng[0]:
                    for y in rng[1]:
                        for z in rng[2]:
                            if self.get(x, y, z) not in (AIR, VOID):
                                return True
                return False
            faces = list(shown_faces)
            if "up" not in faces:
                faces.append("up")
            if M.P[self.node]["base"] and "down" not in faces:
                faces.append("down")
            self.prog.shown_faces = [f for f in faces if f not in ("up", "down") or has(f)]
        os.makedirs(os.path.join(CAMPAIGN, "programs"), exist_ok=True)
        path = os.path.join(CAMPAIGN, "programs", stem(self.node) + ".json")
        self.prog.write(path)
        return path


# -- seams -------------------------------------------------------------------
INWARD = {"north": (0, 0, 1), "south": (0, 0, -1), "east": (-1, 0, 0), "west": (1, 0, 0)}
CLIMB_FACING = {"north": "north", "south": "south", "east": "east", "west": "west"}


def seam_box(s):
    (x0, y0, z0), (x1, y1, z1) = s["cells"]
    return min(x0, x1), min(y0, y1), min(z0, z1), max(x0, x1), max(y0, y1), max(z0, z1)


def answer_wall_seam(pc, s, space, tread=None, fill=None, threshold=None, bar_block=None, bar_role="bar",
                     rise_space=None):
    """Answer one wall-face seam of the allocation in this piece.

    Opening cells are made air and claimed; the exterior edge is declared. A
    stair this place hosts (it is the lower place) is built as a flight of
    `tread` stairs climbing toward the opening, solid `fill` under it, a landing
    space at its head and the flight as the stair edge's transit volume.
    Returns a dict of what was built (regions, landing cells, flight cells)."""
    eid = s["edge"]
    est = eid.split("/")[1]
    face = s["face"]
    x0, y0, z0, x1, y1, z1 = seam_box(s)
    cells = list(boxcells((x0, y0, z0), (x1, y1, z1)))
    out = {"edge": eid, "cells": cells}
    cls = s["class"]
    if cls == "barred" and s["owns_plane"]:
        region = "seam-" + est
        for c in cells:
            pc.set(*c, bar_block)
        pc.claim(cells, region)
        pc.prog.named_roles[bar_role] = bar_block
        pc.edge(a=space, b="exterior", **{"class": "barred"}, bar={"region": region, "block": bar_role})
        out["region"] = region
        return out
    for c in cells:
        pc.set(*c, AIR)
    region = "door-" + est
    hosts = cls == "stair" and s["rise"] > 0 and "stair" in s["answer_with"]
    if not hosts:
        pc.claim(cells, region, share=True)
        if threshold is not None and s["owns_plane"]:
            for (x, y, z) in cells:
                if y == y0:
                    pc.set(x, y - 1, z, threshold)
        ecls = "drop" if (cls == "drop" and s["rise"] < 0) else "walk"
        kw = {"class": ecls, "via": region}
        if ecls == "drop":
            kw["rise"] = 0
        pc.edge(a=space, b="exterior", **kw)
        out["region"] = region
        return out
    # this place hosts the stair: a flight climbing toward the opening
    R = s["rise"]
    ix, _, iz = INWARD[face]
    climb = face
    owned = s["owns_plane"]
    if owned and threshold is not None:
        for (x, y, z) in cells:
            if y == y0:
                pc.set(x, y - 1, z, threshold)
    cols = [(x, z) for (x, y, z) in cells if y == y0]
    h = y1 - y0 + 1
    d0 = 1 if owned else 0
    rows = []  # (d, tread y)
    for k in range(R):
        rows.append((d0 + k, y0 - 1 - k))
    per = {}
    for d, ty in rows:
        cs = []
        for (cx, cz) in cols:
            x, z = cx + ix * d, cz + iz * d
            pc.set(x, ty, z, tread(climb))
            for yy in range(pc.dy - 1, ty):
                pc.set(x, yy, z, fill)
            for yy in range(ty + 1, ty + 1 + h + 1):
                pc.set(x, yy, z, AIR)
                cs.append((x, yy, z))
        per[d] = cs
        per.setdefault("treads", []).extend((cx + ix * d, ty, cz + iz * d) for (cx, cz) in cols)
    pc.claim(cells, region)
    # cheeks: the flight is walled at both sides up past a climber's head, so
    # it is climbed from its foot and never stepped onto from beside (DW0430)
    side = [(cx - iz, cz + ix) for (cx, cz) in cols] + [(cx + iz, cz - ix) for (cx, cz) in cols]
    side = [c for c in side if c not in cols]
    for d, ty in rows:
        for (sx, sz) in side:
            x, z = sx + ix * d, sz + iz * d
            for y in range(pc.dy, ty + 3):
                c = (x, y, z)
                if pc.owned(c) and c not in pc.prog.region and not blocks.is_full(pc.get(*c)):
                    pc.set(*c, fill)
    treads = per.pop("treads")
    land_d = d0 if owned else 1
    flight_ds = [d for d, _ in rows if d > land_d]
    if not flight_ds:
        # a short rise: the treads are the room's own floor
        pc.claim([c for d in per for c in per[d] if c not in cells] + treads, space)
        pc.edge(a=space, b="exterior", **{"class": "walk"}, via=region)
        out.update(region=region)
        return out
    lreg = "landing-" + est
    freg = "flight-" + est
    pc.claim([c for c in per[land_d] if c not in cells], lreg)
    pc.claim([c for d in flight_ds for c in per[d]] + [t for t in treads if t not in per[land_d]], freg)
    pc.space_decl(lreg, "open")
    land_y = y0 if owned else y0 - 1
    pc.edge(a=rise_space or space, b=lreg, **{"class": "stair"}, rise=land_y - pc.dy, via=freg)
    pc.edge(a=lreg, b="exterior", **{"class": "walk"}, via=region)
    out.update(region=region, landing=per[land_d], flight=[c for d in flight_ds for c in per[d]])
    return out


# -- common shapes -------------------------------------------------------------
def ring_cells(pc, y):
    (sx0, _, sz0), (sx1, _, sz1) = pc.space
    out = []
    for x in range(sx0 - 1, sx1 + 2):
        out += [(x, y, sz0 - 1), (x, y, sz1 + 1)]
    for z in range(sz0, sz1 + 1):
        out += [(sx0 - 1, y, z), (sx1 + 1, y, z)]
    return out


def ground(pc, surface, below, over_ring=True):
    """Fill the place's ground: every owned cell under the walk plane within
    the footprint (and the ring) with `below`, the floor course with `surface`.
    `surface`/`below` may be callables of (x, z)."""
    (sx0, _, sz0), (sx1, _, sz1) = pc.space
    r = 1 if over_ring else 0
    for x in range(sx0 - r, sx1 + 1 + r):
        for z in range(sz0 - r, sz1 + 1 + r):
            for y in range(0, pc.dy):
                if not pc.owned((x, y, z)):
                    continue
                if y == pc.dy - 1:
                    b = surface(x, z) if callable(surface) else surface
                else:
                    b = below(x, z) if callable(below) else below
                pc.set(x, y, z, b)


def seams_of(pc, cls=None):
    return [s for s in pc.seams if cls is None or s["class"] == cls]
