"""Read a structure template (.nbt) or a tile set (manifest + parts) into a dict of
cells -> block state. Read-only: nothing here writes a template."""

import gzip
import json
import os
import struct


def _read(buf, pos, tag):
    if tag == 1:
        return struct.unpack(">b", buf[pos:pos + 1])[0], pos + 1
    if tag == 2:
        return struct.unpack(">h", buf[pos:pos + 2])[0], pos + 2
    if tag == 3:
        return struct.unpack(">i", buf[pos:pos + 4])[0], pos + 4
    if tag == 4:
        return struct.unpack(">q", buf[pos:pos + 8])[0], pos + 8
    if tag == 5:
        return struct.unpack(">f", buf[pos:pos + 4])[0], pos + 4
    if tag == 6:
        return struct.unpack(">d", buf[pos:pos + 8])[0], pos + 8
    if tag == 7:
        n = struct.unpack(">i", buf[pos:pos + 4])[0]
        return buf[pos + 4:pos + 4 + n], pos + 4 + n
    if tag == 8:
        n = struct.unpack(">H", buf[pos:pos + 2])[0]
        return buf[pos + 2:pos + 2 + n].decode("utf-8"), pos + 2 + n
    if tag == 9:
        t = buf[pos]
        n = struct.unpack(">i", buf[pos + 1:pos + 5])[0]
        pos += 5
        out = []
        for _ in range(n):
            v, pos = _read(buf, pos, t)
            out.append(v)
        return out, pos
    if tag == 10:
        out = {}
        while True:
            t = buf[pos]
            pos += 1
            if t == 0:
                return out, pos
            n = struct.unpack(">H", buf[pos:pos + 2])[0]
            name = buf[pos + 2:pos + 2 + n].decode("utf-8")
            pos += 2 + n
            out[name], pos = _read(buf, pos, t)
    if tag == 11:
        n = struct.unpack(">i", buf[pos:pos + 4])[0]
        return list(struct.unpack(">%di" % n, buf[pos + 4:pos + 4 + 4 * n])), pos + 4 + 4 * n
    if tag == 12:
        n = struct.unpack(">i", buf[pos:pos + 4])[0]
        return list(struct.unpack(">%dq" % n, buf[pos + 4:pos + 4 + 8 * n])), pos + 4 + 8 * n
    raise ValueError("tag %d" % tag)


def read_nbt(path):
    buf = gzip.open(path).read()
    t = buf[0]
    n = struct.unpack(">H", buf[1:3])[0]
    v, _ = _read(buf, 3 + n, t)
    return v


def state_of(entry):
    name = entry["Name"]
    props = entry.get("Properties") or {}
    if not props:
        return name
    return name + "[" + ",".join("%s=%s" % (k, props[k]) for k in sorted(props)) + "]"


def read_template(path, offset=(0, 0, 0)):
    d = read_nbt(path)
    pal = [state_of(e) for e in d["palette"]]
    cells = {}
    ox, oy, oz = offset
    for b in d["blocks"]:
        x, y, z = b["pos"]
        cells[(x + ox, y + oy, z + oz)] = pal[b["state"]]
    return cells, tuple(d["size"])


def read_piece(prefabs, pid):
    """A library piece by id: one .nbt, or a tile set named by its manifest."""
    name = pid.split("/", 1)[1]
    meta = json.load(open(os.path.join(prefabs, name + ".json")))
    single = os.path.join(prefabs, name + ".nbt")
    if "structure_set" not in meta and os.path.exists(single):
        cells, size = read_template(single)
        return cells, size, meta
    ss = meta["structure_set"]
    cells = {}
    for part in ss["parts"]:
        c, _ = read_template(os.path.join(prefabs, part["file"]), tuple(part["offset"]))
        cells.update(c)
    return cells, tuple(ss["size"]), meta
