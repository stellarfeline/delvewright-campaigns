#!/usr/bin/env python3
"""Audit every prefab in the library, one AUDITED UNIT at a time.

This is the whole of the `prefab palette audit` gate. The workflow builds
`delve-admit` and calls this script; nothing about the check lives in the
workflow YAML, so a creator runs exactly what CI runs:

    python3 tools/prefab-audit.py --bin <path to delve-admit>

# What an audited unit is

A prefab whose region fits under the 48-per-axis structure-template cap ships
as one `.nbt` beside its metadata `.json`, and the `.nbt` is the unit.

A zone past that cap ships as SEVERAL `.nbt` plus one metadata `.json` carrying
a `structure_set`, and there is no single `.nbt` anywhere. For that zone the
**manifest is the unit**: `delve-admit audit` reads every tile it names and
returns one verdict over the whole zone. Handing the tool one tile instead is
refused (`DW0739`) rather than answered, because a verdict over a fifth of a
building reads as a verdict about the building.

So the enumeration is not a glob. It is an accounting over `prefabs/`:

    every .nbt is EITHER a unit of its own
                  OR a tile named by exactly one manifest

and the script asserts that identity holds for every file. Anything the
accounting cannot place is an error, never a skip:

  * a `<base>.x<i>y<j>z<k>.nbt` that no manifest claims — an orphan tile, which
    is what a half-committed zone looks like, and what a plain glob would have
    audited as if it were a whole building;
  * a manifest naming a tile that is not on disk;
  * two manifests claiming the same tile.

A `.json` carrying no `structure_set` is not a unit and is not audited: either
it is the metadata beside a single-file prefab — whose `.nbt` IS the unit and
carries the blocks — or it is a library-wide document such as `pools.json`.

What it does NOT cover, stated so nobody has to infer it: prefab `.nbt` files
outside `prefabs/`, the campaign zone PROGRAMS (`delve-grammar audit`, the
`zone program audit` workflow), and the catalog cards under `catalog/`
(`delve-admit catalog`). Those are other gates over other objects.

# Binding count

Every run prints how many single-file prefabs and how many tiled zones it
examined, and how many tiles those zones covered. A run that examines zero
units fails: a gate that matched nothing is not a pass.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

# The tile name `split::part_filename` gives a tile of a set. `delve-admit`
# recognises a tile by this name too (DW0739) — it is carried by the bytes
# through any copy or rename of the directory.
TILE_RE = re.compile(r"^(?P<base>.+)\.x(?P<x>\d+)y(?P<y>\d+)z(?P<z>\d+)\.nbt$")


class Finding(Exception):
    pass


def read_json(path: Path) -> dict:
    try:
        with path.open(encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        raise Finding(f"{path}: unreadable metadata: {exc}") from exc


def enumerate_units(prefabs: Path) -> tuple[list[Path], list[Path], dict[Path, Path]]:
    """Return (single-file units, tiled-zone manifests, tile -> its manifest)."""
    nbts = sorted(p for p in prefabs.glob("*.nbt") if p.is_file())
    jsons = sorted(p for p in prefabs.glob("*.json") if p.is_file())

    manifests: list[Path] = []
    tile_owner: dict[Path, Path] = {}
    errors: list[str] = []

    for meta in jsons:
        doc = read_json(meta)
        if not isinstance(doc, dict):
            continue
        tile_set = doc.get("structure_set")
        if tile_set is None:
            # A single-template metadata file, or a library-wide document such
            # as `pools.json`. Neither is a unit; the `.nbt` beside it is.
            continue
        parts = tile_set.get("parts")
        if not isinstance(parts, list) or not parts:
            errors.append(f"{meta}: `structure_set` names no parts")
            continue
        for part in parts:
            name = (part or {}).get("file")
            if not name:
                errors.append(f"{meta}: a part has no `file`")
                continue
            tile = prefabs / name
            if tile in tile_owner:
                errors.append(
                    f"{tile.name}: claimed by two manifests "
                    f"({tile_owner[tile].name} and {meta.name})"
                )
                continue
            tile_owner[tile] = meta
        manifests.append(meta)

    singles: list[Path] = []
    for nbt in nbts:
        if nbt in tile_owner:
            continue
        if TILE_RE.match(nbt.name):
            errors.append(
                f"{nbt.name} is named as one tile of a set, and no manifest in "
                f"{prefabs}/ claims it. A tiled zone ships every tile plus the "
                f"`.json` that names them; auditing this file alone would "
                f"return a verdict over a fragment"
            )
            continue
        singles.append(nbt)

    # Every file the accounting places must actually be there.
    for tile, meta in sorted(tile_owner.items()):
        if not tile.is_file():
            errors.append(f"{meta.name} names a tile that is not on disk: {tile.name}")

    if errors:
        raise Finding("\n".join(errors))

    covered = len(singles) + len(tile_owner)
    if covered != len(nbts):
        raise Finding(
            f"accounting does not close: {len(singles)} single-file unit(s) + "
            f"{len(tile_owner)} tile(s) = {covered}, but {len(nbts)} `.nbt` "
            f"file(s) are present"
        )
    return singles, manifests, tile_owner


def audit(binary: Path, unit: Path, reports: Path | None) -> tuple[int, str]:
    cmd = [str(binary), "audit", str(unit)]
    if reports is not None:
        reports.mkdir(parents=True, exist_ok=True)
        cmd += ["-o", str(reports / f"{unit.name}.report.json")]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    # The report is the machine-readable record; diagnostics come back on
    # stderr and are what a reader needs, so they are always relayed.
    out = proc.stderr if reports is not None else proc.stderr + proc.stdout
    return proc.returncode, out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--bin", required=True, type=Path, help="the `delve-admit` binary")
    ap.add_argument("--prefabs", default=Path("prefabs"), type=Path)
    ap.add_argument(
        "--reports",
        type=Path,
        default=None,
        help="write each unit's JSON report here instead of to stdout",
    )
    ap.add_argument(
        "--github",
        action="store_true",
        help="also emit GitHub Actions `::error` annotations",
    )
    args = ap.parse_args()

    if not args.bin.is_file():
        print(f"::error::no delve-admit binary at {args.bin}", file=sys.stderr)
        return 2
    if not args.prefabs.is_dir():
        print(f"::error::no prefab library at {args.prefabs}", file=sys.stderr)
        return 2

    try:
        singles, manifests, tile_owner = enumerate_units(args.prefabs)
    except Finding as exc:
        for line in str(exc).splitlines():
            print(f"::error::{line}" if args.github else f"error: {line}", file=sys.stderr)
        return 1

    units = [(p, "prefab") for p in singles] + [(p, "tiled zone") for p in manifests]
    if not units:
        msg = (
            f"the audit examined ZERO units under {args.prefabs} — a gate that "
            f"matched nothing is not a pass. Is git-lfs materialized?"
        )
        print(f"::error::{msg}" if args.github else f"error: {msg}", file=sys.stderr)
        return 1

    failed: list[Path] = []
    for unit, kind in units:
        print(f"--- auditing {unit} ({kind}) ---", flush=True)
        code, text = audit(args.bin, unit, args.reports)
        if text.strip():
            print(text.rstrip(), file=sys.stderr, flush=True)
        if code != 0:
            failed.append(unit)
            if args.github:
                print(
                    f"::error file={unit}::palette audit failed "
                    f"(exit {code}) — see the DW diagnostics above",
                    flush=True,
                )

    print(
        f"binding: examined {len(singles)} single-file prefab(s) and "
        f"{len(manifests)} tiled zone(s) covering {len(tile_owner)} tile(s); "
        f"{len(units)} audited unit(s) over "
        f"{len(singles) + len(tile_owner)} `.nbt` file(s)."
    )
    if not manifests:
        print("binding: no tiled zone is present in this library.")
    if failed:
        print(f"FAILED: {len(failed)} of {len(units)} unit(s): "
              + ", ".join(p.name for p in failed))
        return 1
    print(f"PASS: {len(units)} of {len(units)} unit(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
