"""Building parts drawn into a Piece in frame coordinates: walls, floors, roofs,
windows, lamps. Cited craft: docs/reference/roof-and-facade-craft.md (a 45° gable
rises one course per cell of half-span, an eave of one cell)."""

from blocks import S, stairs, slab

AIR = "minecraft:air"


def rect_walls(pc, x0, z0, x1, z1, y0, y1, block, corner=None):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            for z in (z0, z1):
                pc.set(x, y, z, block)
        for z in range(z0, z1 + 1):
            for x in (x0, x1):
                pc.set(x, y, z, block)
        if corner:
            for x, z in ((x0, z0), (x0, z1), (x1, z0), (x1, z1)):
                pc.set(x, y, z, corner)


def fill(pc, x0, y0, z0, x1, y1, z1, block):
    pc.box(x0, y0, z0, x1, y1, z1, block)


def gable(pc, x0, z0, x1, z1, ybase, ridge_axis, fam, gable_block, top_block=None, max_courses=None, inset=1):
    """A pitched roof over the rectangle x0..x1 / z0..z1 (eaves included), its
    first course at ybase, the ridge running along `ridge_axis` ('x' or 'z').
    The triangle under the slopes at the two gable ends is walled with
    `gable_block` (the end walls are the rectangle's first/last row inset by one,
    i.e. the wall lines one cell in from the eaves)."""
    top_block = top_block or slab(fam, "bottom")
    if ridge_axis == "x":
        lo, hi = z0, z1
    else:
        lo, hi = x0, x1
    span = hi - lo + 1
    n = (span + 1) // 2
    if max_courses is not None:
        n = min(n, max_courses)
    for i in range(n):
        y = ybase + i
        a, b = lo + i, hi - i
        if a > b:
            break
        if ridge_axis == "x":
            for x in range(x0, x1 + 1):
                if a == b:
                    pc.set(x, y, a, top_block)
                else:
                    pc.set(x, y, a, stairs(fam, "south"))
                    pc.set(x, y, b, stairs(fam, "north"))
                    if i == n - 1 and b - a > 1:
                        for z in range(a + 1, b):
                            pc.set(x, y, z, top_block)
            # gable ends: the wall lines one in from the eave ends
            for xg in (x0 + inset, x1 - inset):
                for z in range(a + 1, b):
                    pc.set(xg, y, z, gable_block)
        else:
            for z in range(z0, z1 + 1):
                if a == b:
                    pc.set(a, y, z, top_block)
                else:
                    pc.set(a, y, z, stairs(fam, "east"))
                    pc.set(b, y, z, stairs(fam, "west"))
                    if i == n - 1 and b - a > 1:
                        for x in range(a + 1, b):
                            pc.set(x, y, z, top_block)
            for zg in (z0 + inset, z1 - inset):
                for x in range(a + 1, b):
                    pc.set(x, y, zg, gable_block)


def hipped(pc, x0, z0, x1, z1, ybase, fam, fill_block, max_courses=None):
    """A hipped roof: every side slopes, each course one in on all four sides."""
    i = 0
    while True:
        ax, bx, az, bz = x0 + i, x1 - i, z0 + i, z1 - i
        if ax > bx or az > bz or (max_courses is not None and i >= max_courses):
            break
        y = ybase + i
        if ax == bx or az == bz:
            for x in range(ax, bx + 1):
                for z in range(az, bz + 1):
                    pc.set(x, y, z, slab(fam, "bottom"))
            break
        for x in range(ax, bx + 1):
            pc.set(x, y, az, stairs(fam, "south"))
            pc.set(x, y, bz, stairs(fam, "north"))
        for z in range(az + 1, bz):
            pc.set(ax, y, z, stairs(fam, "east"))
            pc.set(bx, y, z, stairs(fam, "west"))
        for x in range(ax + 1, bx):
            for z in range(az + 1, bz):
                pc.set(x, y, z, fill_block)
        i += 1


def pane(axis):
    """a glass pane running along `axis` (connections derived later)"""
    return S("minecraft:glass_pane")


def lantern(hanging=True):
    return S("minecraft:lantern", hanging=hanging)


def soul_lantern(hanging=True):
    return S("minecraft:soul_lantern", hanging=hanging)


def candle(n=1, color="white"):
    nm = "minecraft:%s_candle" % color if color else "minecraft:candle"
    return S(nm, candles=n, lit=True)


def wall_torch(facing):
    return S("minecraft:wall_torch", facing=facing)


def door(pc, x, y, z, fam, facing, hinge="left", open_=False):
    pc.set(x, y, z, S("minecraft:%s_door" % fam, facing=facing, half="lower", hinge=hinge, open=open_))
    pc.set(x, y + 1, z, S("minecraft:%s_door" % fam, facing=facing, half="upper", hinge=hinge, open=open_))


def bed(pc, x, y, z, color, facing):
    """the foot at (x,y,z), the head one step toward `facing`"""
    from blocks import STEP
    dx, _, dz = STEP[facing]
    pc.set(x, y, z, S("minecraft:%s_bed" % color, facing=facing, part="foot"))
    pc.set(x + dx, y, z + dz, S("minecraft:%s_bed" % color, facing=facing, part="head"))
