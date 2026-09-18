"""The voxel canvas the castle is drawn on, and the drawing vocabulary.

Every part of the site paints roles into one grid; the driver turns the grid
into the grammar's partition. A role is a palette name, so weathering (a
weighted mix, air included) is the palette's business, not the painter's.
Cells are addressed (x, y, z) in piece coordinates: x east, y up, z south.
"""
from .layout import X, Y, Z

AIR = 0


class Palette:
    def __init__(self):
        self.names = [None]          # role id 0 is air
        self.blocks = [None]
        self.index = {}

    def role(self, name, block):
        """Declare a role once; declaring it again with the same paint is a no-op."""
        if name in self.index:
            if self.blocks[self.index[name]] != block:
                raise ValueError(f"role {name} declared twice with different paint")
            return self.index[name]
        self.index[name] = len(self.names)
        self.names.append(name)
        self.blocks.append(block)
        if len(self.names) > 255:
            raise ValueError("more than 255 roles")
        return self.index[name]

    def __getitem__(self, name):
        return self.index[name]


PAL = Palette()


def state(block, **props):
    """A block state with every property spelled, in sorted order."""
    if not props:
        return block
    inner = ",".join(f"{k}={str(v).lower()}" for k, v in sorted(props.items()))
    return f"{block}[{inner}]"


STAIRS = {}                          # role id -> (material, facing, half, shape)


def stairs(material, facing, half="bottom", shape="straight", wet=False):
    """A stair role: `facing` is the direction a body ascends it. The shape is
    written straight here and derived from the neighbours by `settle_stairs`.
    `wet` is a stair standing in water (waterlogged)."""
    suffix = "" if shape == "straight" else f"_{shape}"
    name = f"{material.split(':')[1]}__{facing}_{half}{suffix}{'_wet' if wet else ''}"
    r = PAL.role(name, state(material, facing=facing, half=half,
                             shape=shape, waterlogged=wet))
    STAIRS[r] = (material, facing, half, shape, wet)
    return r


_STEP = {"north": (0, -1), "south": (0, 1), "east": (1, 0), "west": (-1, 0)}
_OPP = {"north": "south", "south": "north", "east": "west", "west": "east"}
_CCW = {"north": "west", "west": "south", "south": "east", "east": "north"}


def settle_stairs(g):
    """Write every stair's shape the way vanilla derives it from its
    neighbours (StairBlock.getStairsShape), so what is built is what stays."""
    from .layout import X, Y, Z
    cells = g.cells
    ids = set(STAIRS)
    changes = []
    for i, r in enumerate(cells):
        if r not in ids:
            continue
        x = i % X; rest = i // X; y = rest % Y; z = rest // Y
        mat, facing, half, _, wet = STAIRS[r]

        def at(d, _x=x, _z=z):
            dx, dz = _STEP[d]
            n = g.get(_x + dx, y, _z + dz)
            return STAIRS.get(n)

        def can_take(d):
            n = at(d)
            return n is None or n[1] != facing or n[2] != half

        shape = "straight"
        front = at(facing)
        if front and front[2] == half:
            d1 = front[1]
            if _STEP[d1][0] != _STEP[facing][0] or _STEP[d1][1] != _STEP[facing][1]:
                if (d1 in ("east", "west")) != (facing in ("east", "west")) and can_take(_OPP[d1]):
                    shape = "outer_left" if d1 == _CCW[facing] else "outer_right"
        if shape == "straight":
            back = at(_OPP[facing])
            if back and back[2] == half:
                d2 = back[1]
                if (d2 in ("east", "west")) != (facing in ("east", "west")) and can_take(d2):
                    shape = "inner_left" if d2 == _CCW[facing] else "inner_right"
        if shape != "straight":
            changes.append((x, y, z, stairs(mat, facing, half, shape, wet)))
    for x, y, z, r in changes:
        g.set(x, y, z, r)
    return len(changes)


RAILS = {}                           # role id -> wall-block material


def rail(material):
    """A wall-block role (`minecraft:*_wall`), laid as a lone post; its sides
    and post are derived from the neighbours by `settle_rails`."""
    return rail_state(material, "none", "none", "none", "none", True)


def rail_state(material, north, east, south, west, up):
    name = f"{material.split(':')[1]}__{north[0]}{east[0]}{south[0]}{west[0]}{'p' if up else ''}"
    r = PAL.role(name, state(material, north=north, east=east, south=south,
                             west=west, up=up, waterlogged=False))
    RAILS[r] = material
    return r


def settle_rails(g, sturdy):
    """Write every wall block's sides and post the way vanilla derives them
    (WallBlock.updateShape / shouldRaisePost): a side connects to another wall
    block, to iron bars or to a full block (`sturdy`, role ids), and is low
    under open air; the post stands unless the block runs straight through."""
    from .layout import X, Y, Z
    ids = set(RAILS)
    bars = {PAL.index[n] for n in ("bars_x", "bars_z") if n in PAL.index}
    changes = []
    for i, r in enumerate(g.cells):
        if r not in ids:
            continue
        x = i % X; rest = i // X; y = rest % Y; z = rest // Y
        side = {}
        for d, (dx, dz) in _STEP.items():
            n = g.get(x + dx, y, z + dz)
            side[d] = "low" if (n in ids or n in bars or n in sturdy) else "none"
        above = g.get(x, y + 1, z)
        nn, ee, ss, ww = (side[d] == "none" for d in ("north", "east", "south", "west"))
        up = (above in ids) or (nn and ee and ss and ww) or nn != ss or ee != ww
        changes.append((x, y, z, rail_state(RAILS[r], side["north"], side["east"],
                                            side["south"], side["west"], up)))
    for x, y, z, r in changes:
        g.set(x, y, z, r)
    return len(changes)


def slab(material, kind="bottom"):
    name = f"{material.split(':')[1]}__{kind}"
    return PAL.role(name, state(material, type=kind, waterlogged=False))


def block(bid):
    """A plain one-block role named after the block."""
    return PAL.role(bid.split(":")[1].replace("[", "_").replace("]", "")
                    .replace("=", "-").replace(",", "_"), bid)


class Grid:
    def __init__(self):
        self.cells = bytearray(X * Y * Z)
        self.anchors = {}            # name -> (x, y, z, facing, role)
        self.gates = {}              # name -> ((x0,y0,z0),(x1,y1,z1), block)
        self.points = set()          # anchors that name a cell nobody stands in
        self.furniture = set()       # point anchors that name a block (a chest), not air

    def _i(self, x, y, z):
        return (z * Y + y) * X + x

    def inside(self, x, y, z):
        return 0 <= x < X and 0 <= y < Y and 0 <= z < Z

    def get(self, x, y, z):
        if not self.inside(x, y, z):
            return AIR
        return self.cells[self._i(x, y, z)]

    def set(self, x, y, z, r):
        if self.inside(x, y, z):
            self.cells[self._i(x, y, z)] = r

    def box(self, x0, x1, y0, y1, z0, z1, r):
        """Fill an inclusive box."""
        x0, x1 = max(x0, 0), min(x1, X - 1)
        y0, y1 = max(y0, 0), min(y1, Y - 1)
        z0, z1 = max(z0, 0), min(z1, Z - 1)
        for z in range(z0, z1 + 1):
            for y in range(y0, y1 + 1):
                base = (z * Y + y) * X
                self.cells[base + x0: base + x1 + 1] = bytes([r]) * (x1 - x0 + 1)

    def clear(self, x0, x1, y0, y1, z0, z1):
        self.box(x0, x1, y0, y1, z0, z1, AIR)

    def column_top(self, x, z):
        for y in range(Y - 1, -1, -1):
            if self.get(x, y, z) != AIR:
                return y
        return -1

    def mark(self, name, x, y, z, facing, role=None, stand=True, holds=False):
        """`stand=False` names a cell nobody stands in; `holds=True` names the
        cell of a piece of furniture the campaign fills (a chest)."""
        if not stand or holds:
            self.points.add(name)
        if holds:
            self.furniture.add(name)
        if name in self.anchors:
            raise ValueError(f"anchor {name} marked twice")
        self.anchors[name] = (x, y, z, facing, role)

    def gate(self, name, x0, x1, y0, y1, z0, z1, bid, r):
        """A sealed opening: paint it, and remember its region for the metadata."""
        self.box(x0, x1, y0, y1, z0, z1, r)
        self.gates[name] = ((x0, y0, z0), (x1, y1, z1), bid)


def hsh(*v):
    """A deterministic hash in [0, 1) — the only randomness the site uses."""
    h = 2166136261
    for n in v:
        h = ((h ^ (n & 0xFFFFFFFF)) * 16777619) & 0xFFFFFFFF
        h ^= h >> 13
        h = (h * 0x5bd1e995) & 0xFFFFFFFF
    return (h & 0xFFFFFF) / 0x1000000


# ------------------------------------------------------------------ drawing

def room(g, x0, x1, z0, z1, floor, height, wall, floor_role, ceiling=None, t=1):
    """A walled room: `x0..x1`/`z0..z1` is the space a body walks in, `floor`
    the feet level, `height` the clear air above it. Walls stand outside the
    box, `t` thick. The ceiling course sits at floor + height."""
    top = floor + height
    g.box(x0 - t, x1 + t, floor - 1, top, z0 - t, z1 + t, wall)
    g.box(x0, x1, floor - 1, floor - 1, z0, z1, floor_role)
    if ceiling is not None:
        g.box(x0 - t, x1 + t, top, top, z0 - t, z1 + t, ceiling)
    g.clear(x0, x1, floor, top - 1, z0, z1)


def crenels(g, x0, x1, z0, z1, y, r, step=2):
    """Merlons on the outer ring of a box, one course at `y`."""
    for x in range(x0, x1 + 1):
        for z in (z0, z1):
            if (x - x0) % step == 0:
                g.set(x, y, z, r)
    for z in range(z0, z1 + 1):
        for x in (x0, x1):
            if (z - z0) % step == 0:
                g.set(x, y, z, r)


def flight(g, axis, lo, hi, start, direction, feet, n, material, under, headroom=3):
    """A straight flight of `n` treads climbing `direction` (+1/-1) along
    `axis` ('x' or 'z'), `lo..hi` wide on the other axis. The first tread is
    at `start` and a body standing on it has its feet at `feet + 1`; every
    tread is a stair block, the mass under it `under`, the air over it clear."""
    facing = {("z", -1): "north", ("z", 1): "south", ("x", 1): "east", ("x", -1): "west"}[(axis, direction)]
    r = stairs(material, facing)
    for k in range(n):
        a = start + direction * k
        y = feet + k
        for b in range(lo, hi + 1):
            x, z = (a, b) if axis == "x" else (b, a)
            g.box(x, x, feet - 1 - 8, y - 1, z, z, under) if under else None
            g.set(x, y, z, r)
            g.clear(x, x, y + 1, y + headroom + 1, z, z)


def gable(g, x0, x1, z0, z1, base, material, fill, along="x", eaves=1):
    """A pitched roof over the box, ridge running `along`. Slopes are stair
    blocks facing up the slope; the gable ends and the space under the slope
    are `fill` (None leaves an open attic)."""
    if along == "x":
        a0, a1 = z0 - eaves, z1 + eaves
    else:
        a0, a1 = x0 - eaves, x1 + eaves
    layer = 0
    while a0 + layer <= a1 - layer:
        y = base + layer
        lo, hi = a0 + layer, a1 - layer
        if along == "x":
            if lo == hi:
                g.box(x0 - eaves, x1 + eaves, y, y, lo, lo, fill or stairs(material, "north"))
            else:
                g.box(x0 - eaves, x1 + eaves, y, y, lo, lo, stairs(material, "south"))
                g.box(x0 - eaves, x1 + eaves, y, y, hi, hi, stairs(material, "north"))
                if fill and hi - lo > 1:
                    for x in (x0, x1):
                        g.box(x, x, y, y, lo + 1, hi - 1, fill)
                if hi - lo == 1:
                    pass
        else:
            if lo == hi:
                g.box(lo, lo, y, y, z0 - eaves, z1 + eaves, fill or stairs(material, "west"))
            else:
                g.box(lo, lo, y, y, z0 - eaves, z1 + eaves, stairs(material, "east"))
                g.box(hi, hi, y, y, z0 - eaves, z1 + eaves, stairs(material, "west"))
                if fill and hi - lo > 1:
                    for z in (z0, z1):
                        g.box(lo + 1, hi - 1, y, y, z, z, fill)
        layer += 1
    return base + layer


def pyramid(g, x0, x1, z0, z1, base, r, cap=None):
    """A stepped spire: each course one cell in from the one below."""
    y = base
    while x0 <= x1 and z0 <= z1:
        g.box(x0, x1, y, y, z0, z0, r); g.box(x0, x1, y, y, z1, z1, r)
        g.box(x0, x0, y, y, z0, z1, r); g.box(x1, x1, y, y, z0, z1, r)
        x0 += 1; x1 -= 1; z0 += 1; z1 -= 1; y += 1
    if cap:
        g.set((x0 + x1) // 2, y, (z0 + z1) // 2, cap)
    return y


def lancet(g, plane, u, y0, height, w, fixed, r, axis):
    """A pointed window of width `w` in a wall: `axis` is the wall's own
    horizontal axis ('x' or 'z'), `fixed` its coordinate on the other axis.
    The top narrows to a point."""
    for k in range(height):
        for d in range(w):
            if k >= height - 1 and w > 1 and d not in (w // 2,):
                continue
            x, z = (u + d, fixed) if axis == "x" else (fixed, u + d)
            g.set(x, y0 + k, z, r)


def rose(g, cx, cy, fixed, radius, axis, rim, glass, spokes):
    """A round window in a wall plane."""
    for du in range(-radius, radius + 1):
        for dv in range(-radius, radius + 1):
            d2 = du * du + dv * dv
            if d2 > radius * radius + radius:
                continue
            x, z = (cx + du, fixed) if axis == "x" else (fixed, cx + du)
            y = cy + dv
            if d2 >= (radius - 1) * (radius - 1) + radius - 1:
                g.set(x, y, z, rim)
            elif du == 0 or dv == 0 or abs(du) == abs(dv) or d2 <= 1:
                g.set(x, y, z, spokes)
            else:
                g.set(x, y, z, glass)


def machicolate(g, x0, x1, z0, z1, y, wall, material, sides="nsew"):
    """A corbelled parapet: the course at `y` steps out one cell over
    upside-down stairs, and the course above it carries merlons."""
    if "n" in sides:
        g.box(x0, x1, y - 1, y - 1, z0 - 1, z0 - 1, stairs(material, "south", "top"))
        g.box(x0 - 1, x1 + 1, y, y, z0 - 1, z0 - 1, wall)
        for x in range(x0 - 1, x1 + 2, 2):
            g.set(x, y + 1, z0 - 1, wall)
    if "s" in sides:
        g.box(x0, x1, y - 1, y - 1, z1 + 1, z1 + 1, stairs(material, "north", "top"))
        g.box(x0 - 1, x1 + 1, y, y, z1 + 1, z1 + 1, wall)
        for x in range(x0 - 1, x1 + 2, 2):
            g.set(x, y + 1, z1 + 1, wall)
    if "w" in sides:
        g.box(x0 - 1, x0 - 1, y - 1, y - 1, z0, z1, stairs(material, "east", "top"))
        g.box(x0 - 1, x0 - 1, y, y, z0 - 1, z1 + 1, wall)
        for z in range(z0 - 1, z1 + 2, 2):
            g.set(x0 - 1, y + 1, z, wall)
    if "e" in sides:
        g.box(x1 + 1, x1 + 1, y - 1, y - 1, z0, z1, stairs(material, "west", "top"))
        g.box(x1 + 1, x1 + 1, y, y, z0 - 1, z1 + 1, wall)
        for z in range(z0 - 1, z1 + 2, 2):
            g.set(x1 + 1, y + 1, z, wall)


def tower(g, x0, x1, z0, z1, base, top, wall, roof, trim, quoin=None, cap=True, slits=True):
    """A square tower with chamfered corners, a machicolated head and a
    pyramid roof — the silhouette every tower on the site shares."""
    g.box(x0, x1, base, top, z0, z1, wall)
    from .layout import CASTLE
    chamfer = max(base, CASTLE + 3)
    for (cx, cz) in ((x0, z0), (x1, z0), (x0, z1), (x1, z1)):
        g.box(cx, cx, chamfer, top, cz, cz, AIR)
        if quoin:
            dx = 1 if cx == x0 else -1
            dz = 1 if cz == z0 else -1
            g.box(cx + dx, cx + dx, base, top, cz, cz, quoin)
            g.box(cx, cx, base, top, cz + dz, cz + dz, quoin)
    machicolate(g, x0 + 1, x1 - 1, z0 + 1, z1 - 1, top + 1, wall, "minecraft:stone_brick_stairs")
    g.box(x0, x1, top + 1, top + 1, z0, z1, wall)
    if slits:
        for y in range(base + 6, top - 2, 5):
            mx, mz = (x0 + x1) // 2, (z0 + z1) // 2
            for (sx, sz) in ((mx, z0), (mx, z1), (x0, mz), (x1, mz)):
                g.box(sx, sx, y, y + 2, sz, sz, trim)
            g.clear(mx, mx, y, y + 1, z0, z0); g.clear(mx, mx, y, y + 1, z1, z1)
            g.clear(x0, x0, y, y + 1, mz, mz); g.clear(x1, x1, y, y + 1, mz, mz)
    if cap:
        pyramid(g, x0, x1, z0, z1, top + 2, roof, cap=trim)


def tree(g, tx, tz, base, log, wood, leaves, trunk=2, height=6, spread=5, seed=0):
    """A broad old tree that reads as one at a walker's eye: a `trunk`-wide
    bole with root flares, four limbs forking out and up from its head, and a
    layered crown of leaves over the limbs. `(tx, tz)` is the bole's north-west
    column, `base` the course its roots stand on, `log`/`wood` the axis-y log
    and bark-all-round block of one species, `leaves` its (persistent) leaves.
    Returns the crown's centre (x, y, z)."""
    cx, cz = tx + (trunk - 1) / 2, tz + (trunk - 1) / 2
    for dx in range(trunk):
        for dz in range(trunk):
            g.box(tx + dx, tx + dx, base, base + height, tz + dz, tz + dz, log)
    # root flares on the four sides of the bole
    for (rx, rz) in ((tx - 1, tz), (tx + trunk, tz + trunk - 1), (tx + trunk - 1, tz - 1), (tx, tz + trunk)):
        g.set(rx, base, rz, wood)
    # four limbs, one from each face of the head, climbing as they reach out
    head = base + height
    for k, (ux, uz) in enumerate(((1, 0), (-1, 0), (0, 1), (0, -1))):
        reach = 2 + int(2 * hsh(tx, tz, seed, k))
        sx = tx + (trunk if ux > 0 else -1 if ux < 0 else int(hsh(tx, k, seed) * trunk))
        sz = tz + (trunk if uz > 0 else -1 if uz < 0 else int(hsh(tz, k, seed) * trunk))
        y = head - 2 + (k % 2)
        for s in range(reach):
            g.set(sx + ux * s, y + s // 2, sz + uz * s, wood)
    # the crown: three courses of leaves, broad in the middle, holed a little
    top = head + 3
    for y in range(head - 1, top + 1):
        r = spread - (1 if y in (head - 1, top) else 0) - (1 if y == top else 0)
        for x in range(int(cx - r - 1), int(cx + r + 2)):
            for z in range(int(cz - r - 1), int(cz + r + 2)):
                d2 = (x - cx) ** 2 + (z - cz) ** 2
                if d2 <= r * r + .5 and hsh(x, y, z, seed) < (.93 if d2 < (r - 1) ** 2 else .7):
                    if g.get(x, y, z) == AIR:
                        g.set(x, y, z, leaves)
    return (cx, head, cz)
