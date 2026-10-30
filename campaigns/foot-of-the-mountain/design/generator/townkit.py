"""Reusable building helpers for town plots, independent of any one town.

Every helper draws into a model `m` that has `set(x, y, z, role)`, `get(x, y, z)` and a
cell map `v` keyed by `(x, y, z)`, in the frame-relative coordinates the caller works in.
Course 0 is the ground course and course 1 the walk plane. No helper names a place, a
coordinate of a particular town, or a block: the caller states the extents, and the roles
it passes are looked up in the caller's palette. `AIR` is the role a model uses for a cell
it forces empty.

Standard library only.
"""

from __future__ import annotations

AIR = "~air"


def _solid(m, c):
    r = m.v.get(c)
    return r is not None and r != AIR


# ---------------------------------------------------------------- plot edges


def clip_beyond(m, x0, x1, z0, z1, above=0):
    """Delete every cell above course `above` outside the columns x0..x1, z0..z1: an
    eave or a rake that overhangs the plot's play space stops at its edge."""
    for c in [c for c in m.v if c[1] > above and not (x0 <= c[0] <= x1 and z0 <= c[2] <= z1)]:
        del m.v[c]


def clip_unwalled_edge(m, x0, x1, z0, z1, wall_roles, from_y):
    """On the plot's edge columns whose walk-plane cell is not one of `wall_roles`, delete
    every cell from course `from_y` up: an eave over a column with no wall under it would
    stand over air beside the neighbour's ground."""
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if x not in (x0, x1) and z not in (z0, z1):
                continue
            if m.get(x, 1, z) not in wall_roles:
                for c in [c for c in m.v if c[0] == x and c[2] == z and c[1] >= from_y]:
                    del m.v[c]


def close_edge_gaps(m, x0, x1, z0, z1, role):
    """On the plot's edge columns, fill the air between the lowest and the highest solid
    cell above the ground with `role` (a role, or a function of (x, z) giving one), so no
    edge column stands over air."""
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if x not in (x0, x1) and z not in (z0, z1):
                continue
            ys = sorted(y for (cx, y, cz) in m.v if cx == x and cz == z and y > 0 and m.v[(cx, y, cz)] != AIR)
            if len(ys) < 2:
                continue
            for y in range(ys[0], ys[-1]):
                if (x, y, z) not in m.v or m.v[(x, y, z)] == AIR:
                    m.set(x, y, z, role(x, z) if callable(role) else role)


# ---------------------------------------------------------------- buildings


def post_shed(m, box, plate, posts_x, roles, back_height=0, back="north"):
    """An open shed on posts. `box` = (x0, x1, z0, z1) its post lines inclusive; posts at
    every x of `posts_x` (and the four corners) on both long sides, up to course
    plate-1; a beam along each long side at `plate`; the back side boarded from course 1
    to `back_height` between its corner posts. `roles` maps "post", "beam" and "back".
    The roof is the caller's (the starter's `m.roof`), since its pitch and cover are."""
    x0, x1, z0, z1 = box
    for x in sorted(set(posts_x) | {x0, x1}):
        for z in (z0, z1):
            for y in range(1, plate):
                m.set(x, y, z, roles["post"])
    for z in (z0, z1):
        for x in range(x0, x1 + 1):
            m.set(x, plate, z, roles["beam"])
    if back_height:
        bz = z0 if back == "north" else z1
        for x in range(x0 + 1, x1):
            for y in range(1, back_height + 1):
                m.set(x, y, bz, roles["back"])


def loft(m, x0, x1, z0, z1, floor_y, ladder, roles):
    """A loft floor over the rows z0..z1 between x0 and x1 at course `floor_y`, and a
    ladder at column `ladder` = (x, z) from the walk plane up to the loft's course.
    `roles` maps "floor" and "ladder" (the ladder role carries its facing)."""
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            m.set(x, floor_y, z, roles["floor"])
    lx, lz = ladder
    for y in range(1, floor_y + 1):
        m.set(lx, y, lz, roles["ladder"])


# ---------------------------------------------------------------- boats


HULL_ROLES = ("hull", "keel", "deck", "gunwale", "gunwale_hi", "stem", "stem_post",
              "flare_n", "flare_s", "flare_e", "flare_w")


def hull(m, axis, s0, c0, widths, waterline, roles=None, toward=1, cols=None, shoulder=True):
    """A boat's hull in half steps, laid along `axis` ("x" or "z") from its stern station
    s0 toward its bow (`toward` = +1 or -1), centred on the cross line c0.

    `widths[i]` is the half-beam at station i: the stern's first stations and the bow's
    last narrow to a point (0 at the stem). In section: planks a cell in at `waterline`,
    the keel under them, upturned stairs flaring out a course above, a slab gunwale on
    top. The sheer rises toward both ends: a top slab on the first two and the last three
    stations, a strake more at the bow's shoulder (left out with `shoulder=False`, for a
    boat small enough that the strake would close its deck in), and the stem a post
    rising past the gunwale to a point. `roles` renames any of HULL_ROLES to the caller's palette;
    `cols`, a set, collects every column the hull stands on."""
    r = {k: k for k in HULL_ROLES}
    r.update(roles or {})
    deck_y = waterline + 1

    def at(i, c):
        s = s0 + toward * i
        return (s, c) if axis == "x" else (c, s)

    n = len(widths)
    for i, w in enumerate(widths):
        for c in range(c0 - w, c0 + w + 1):
            x, z = at(i, c)
            if cols is not None:
                cols.add((x, z))
            off = c - c0
            side = abs(off) == w and w > 0
            if abs(off) <= max(0, w - 1):
                m.set(x, waterline, z, r["hull"])
            if off == 0:
                m.set(x, waterline - 1, z, r["keel"])
            if w == 0 or (side and i == n - 1):
                m.set(x, deck_y, z, r["hull"])
                m.set(x, deck_y + 1, z, r["stem_post"])
                m.set(x, deck_y + 2, z, r["stem"])
            elif side and i == n - 2 and shoulder:
                m.set(x, deck_y, z, r["hull"])
                m.set(x, deck_y + 1, z, r["hull"])
                m.set(x, deck_y + 2, z, r["gunwale"])
            elif side:
                if axis == "x":
                    face = "south" if off < 0 else "north"
                else:
                    face = "east" if off < 0 else "west"
                m.set(x, deck_y, z, r["flare_" + face[0]])
                m.set(x, deck_y + 1, z, r["gunwale_hi"] if i <= 1 or i >= n - 3 else r["gunwale"])
            elif i == 0:
                m.set(x, deck_y, z, r["hull"])
                m.set(x, deck_y + 1, z, r["gunwale_hi"])
            else:
                m.set(x, deck_y, z, r["deck"])


def mast(m, axis, s, c0, foot_y, top_y, roles):
    """A mast at station s on the cross line c0 from course foot_y to top_y, a yard two
    each side of it a course under the top, and the sail furled along the yard: a thin
    roll lying on the yard's top course beside the mast, never a block hung under it.
    `roles` maps "mast", "yard_x" and "yard_z" (a thin spar running along x or along z:
    a fence joined along it), and "sail" (a thin block that stands on the yard: a carpet).
    The yard crosses the hull, so it runs along z on a boat laid along x."""
    x, z = (s, c0) if axis == "x" else (c0, s)
    for y in range(foot_y, top_y + 1):
        m.set(x, y, z, roles["mast"])
    for k in (-2, -1, 1, 2):
        xx, zz = (x + k, z) if axis == "z" else (x, z + k)
        m.set(xx, top_y - 1, zz, roles["yard_z" if axis == "x" else "yard_x"])
        m.set(xx, top_y, zz, roles["sail"])


def hull_on_stocks(m, axis, stern, bow, c0, keel_y, framed, stocks, roles=None):
    """A boat building on its stocks, its bow at station `bow` and its transom's foot at
    `stern` (stern < bow along `axis`), centred on the cross line c0, its keel at course
    keel_y on stocks at the stations `stocks`.

    The stem is a narrow post rising from a solid foot on the keel to a point, and the
    planking is drawn in to it: at the station behind the stem the sides are thin plates on
    their inner faces with nothing between them, so the hull's outline closes on the post; the sheer is at its
    highest there (a top slab at the shoulder, a bottom slab amidships); the turn of the bilge is upturned stairs and the planked
    strake amidships lapped planks on the outer face; the `framed` stations next to the
    transom stand in bare frames (a frame every other station) on their ribband; the
    transom rakes out over the stern. Side roles carry the side's letter ("bilge_n",
    "lap_s"; "_w"/"_e" along z), so the caller's palette gives each its facing.
    `roles` renames any role: stock, keel, stem (the solid foot), stem_post (the narrow
    post), stem_tip, strake, gunwale, gunwale_hi, rib, transom, transom_rake,
    bilge_<side>, lap_<side>, bow_plate_<side> (a plate on the side's inner face)."""
    r = dict(roles or {})
    R = lambda k: r.get(k, k)  # noqa: E731
    P = (lambda s, c, y: (s, y, c)) if axis == "x" else (lambda s, c, y: (c, y, s))

    def put(s, y, c, role):
        x, yy, z = P(s, c, y)
        m.set(x, yy, z, R(role))

    lo, hi = c0 - 1, c0 + 1
    side = (lambda c: "n" if c < c0 else "s") if axis == "x" else (lambda c: "w" if c < c0 else "e")
    for s in stocks:
        put(s, keel_y - 1, c0, "stock")
    for s in range(stern, bow):
        put(s, keel_y, c0, "keel")
    put(bow, keel_y, c0, "stem")
    for y in range(keel_y + 1, keel_y + 4):
        put(bow, y, c0, "stem_post")
    put(bow, keel_y + 4, c0, "stem_tip")
    for c in (lo, hi):
        for y in (keel_y + 1, keel_y + 2, keel_y + 3):
            put(bow - 1, y, c, "bow_plate_" + side(c))
        put(bow - 2, keel_y, c, "bilge_" + side(c))
        put(bow - 2, keel_y + 1, c, "strake")
        put(bow - 2, keel_y + 2, c, "gunwale_hi")
    for s in range(stern + 1 + framed, bow - 2):
        for c in (lo, hi):
            put(s, keel_y, c, "bilge_" + side(c))
            put(s, keel_y + 1, c, "lap_" + side(c))
            put(s, keel_y + 2, c, "gunwale")
    for s in range(stern + 1, stern + 1 + framed):
        for c in (lo, hi):
            put(s, keel_y, c, "bilge_" + side(c))
            if (s - stern) % 2 == 1:
                put(s, keel_y + 1, c, "rib")
            put(s, keel_y + 2, c, "rib")
    put(stern, keel_y + 1, c0, "transom")
    put(stern, keel_y + 1, lo, "bilge_" + side(lo))
    put(stern, keel_y + 1, hi, "bilge_" + side(hi))
    for c in range(lo, hi + 1):
        put(stern - 1, keel_y + 2, c, "transom_rake")
    put(stern - 1, keel_y + 3, c0, "gunwale")


# ---------------------------------------------------------------- quays and basins


def slipway(m, cols, edge, run_to, surface, bed, quay_y, roles, toward=1):
    """A slipway running down off a quay into the water along z, over the columns `cols`.

    Row `edge - toward` carries a low slab on the quay's ground course `quay_y`; from row
    `edge` to `run_to` the ramp drops half a course a row (slabs alternating bottom and
    top), starting a course under the quay, with `bed` filled solid under each slab and
    water over it up to `surface`. The quay course over its first row is forced empty.
    `roles` maps "low" (a dry bottom slab), "wet_lo", "wet_hi" (waterlogged bottom and
    top slabs), "fill" and "water"."""
    for x in cols:
        m.set(x, quay_y, edge - toward, roles["low"])
        m.set(x, quay_y, edge, AIR)
        for k, z in enumerate(range(edge, run_to + toward, toward)):
            y = surface - (k + 1) // 2
            for yy in range(bed, y):
                m.set(x, yy, z, roles["fill"])
            m.set(x, y, z, roles["wet_hi"] if k % 2 == 1 else roles["wet_lo"])
            for yy in range(y + 1, surface + 1):
                m.set(x, yy, z, roles["water"])


def pier(m, cols, z_from, z_to, quay_y, bed, roles, kerb_x=None):
    """A pier out into a basin along z: solid `fill` from `bed` up under the quay course,
    the quay course paved, kerbed on its head row and on the column `kerb_x`. `roles`
    maps "fill", "pave" and "kerb"."""
    for x in cols:
        for z in range(z_from, z_to + 1):
            for y in range(bed, quay_y):
                m.set(x, y, z, roles["fill"])
            m.set(x, quay_y, z, roles["kerb"] if z == z_to or x == kerb_x else roles["pave"])


def water_step(m, x, z, surface, bed, roles):
    """One stair at the water's surface course at (x, z), solid under it to `bed`, so a
    swimmer climbs out onto the quay beside it. `roles` maps "step" (a stair facing the
    quay) and "fill"."""
    m.set(x, surface, z, roles["step"])
    for y in range(bed, surface):
        m.set(x, y, z, roles["fill"])


# ---------------------------------------------------------------- street fronts


def street_front(m, x, z0, z1, door_rows, air, roles, door_h=3, solid=None):
    """Close a lot's street edge, the column `x` over rows z0..z1, as the street's
    air above it asks: up to course `air` nothing on that column is open but the
    doorway (`door_rows`, `door_h` high), and nothing stands proud of it above.

    Where the lot's building already stands on the edge (its walk-plane cell is
    solid) the building's front carries the closure: any open cell of it up to
    `air` is filled with roles["wall"] (a front's window is a pane: solid), and
    the doorway's head up to `air` with roles["lintel"]. Where nothing stands, a
    yard wall goes up: roles["wall"] to course air-1 and roles["coping"] on top,
    every cell above it cleared, so no eave stands over the yard wall at the edge.
    The doorway rows are left open from the walk plane to `door_h`. `solid` tells
    a filled cell (a role) from an open one; by default anything but air is."""
    is_solid = solid or (lambda r: r is not None and r != AIR)
    for z in range(z0, z1 + 1):
        if z in door_rows:
            for y in range(1, door_h + 1):
                m.set(x, y, z, AIR)
            for y in range(door_h + 1, air + 1):
                if not is_solid(m.get(x, y, z)):
                    m.set(x, y, z, roles["lintel"])
            continue
        if is_solid(m.get(x, 1, z)):
            for y in range(2, air + 1):
                if not is_solid(m.get(x, y, z)):
                    m.set(x, y, z, roles["wall"])
            continue
        for y in range(1, air):
            m.set(x, y, z, roles["wall"])
        m.set(x, air, z, roles["coping"])
        for c in [c for c in m.v if c[0] == x and c[2] == z and c[1] > air]:
            del m.v[c]


def shift(m, dx):
    """Draw into `m` moved `dx` along x from here on: every write and read through
    set, get, part and mark (and so box, door and roof) lands dx over. shift(m, 0)
    ends it. A building drawn at its own coordinates is stood, whole, on the edge."""
    for k in ("set", "get", "part", "mark"):
        m.__dict__.pop(k, None)
    if not dx:
        return
    cls = type(m)
    m.set = lambda x, y, z, r: cls.set(m, x + dx, y, z, r)
    m.get = lambda x, y, z: cls.get(m, x + dx, y, z)
    m.part = lambda x0, x1, z0, z1, stem: cls.part(m, x0 + dx, x1 + dx, z0, z1, stem)
    m.mark = lambda stem, x, z, facing="south": cls.mark(m, stem, x + dx, z, facing)


def street_seam(place, face):
    """Read a lot's street edge on `face` off its allocation (`place.a`):
    (fronted, (edge column or row, the rows the seam leaves open, the doorway's
    height, the course the street's air rises to)). Fronted means the seam is cut
    to a doorway narrower than the edge: the lot then stands its building on the
    edge. While it is uncut the rows are the whole edge. The street's air is the
    height of the street's void on the ring beside the edge (the seam's own top
    where no void is handed)."""
    a = place.a
    lo, hi = place.space
    for c in a["seams"]:
        if c.get("face") != face:
            continue
        (x0, y0, z0), (x1, y1, z1) = c["cells"]
        air = y1
        for v in a.get("voids", []):
            (vx0, vy0, vz0), (vx1, vy1, vz1) = v["cells"]
            if face in ("east", "west"):
                beside = vx0 == vx1 == x0 + (1 if face == "east" else -1)
            else:
                beside = vz0 == vz1 == z0 + (1 if face == "south" else -1)
            if beside:
                air = vy1
        if face in ("east", "west"):
            rows, span, edge = set(range(z0, z1 + 1)), hi[2] - lo[2] + 1, x0
        else:
            rows, span, edge = set(range(x0, x1 + 1)), hi[0] - lo[0] + 1, z0
        return len(rows) < span, (edge, rows, y1, air)
    return False, None
