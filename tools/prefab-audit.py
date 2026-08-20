#!/usr/bin/env python3
"""Audit every `.nbt` in this repository, one AUDITED UNIT at a time.

This is the whole of the `prefab palette audit` gate. The workflow builds
`delve-admit` and calls this script; nothing about the check lives in the
workflow YAML, so a creator runs exactly what CI runs:

    python3 tools/prefab-audit.py --bin <path to delve-admit>

# The audited set is DISCOVERED, never listed

The property this gate exists to hold is: **no `.nbt` file anywhere in this
repository can reach a merge without a verdict.** A gate that globs a list of
directories — `prefabs/*.nbt`, then `demos/*/*.nbt`, then whatever the next
piece needs — only ever looks where somebody already pointed, so the first
piece committed somewhere nobody anticipated enters through the one door with
no gate on it. Widening the list after the fact is the same shape again.

So the audited set is not a glob over known roots. It is a **walk of the
working tree** (everything but `.git/`), and the roots are an OUTPUT of that
walk, printed on every run, not an input to it. A `.nbt` under a directory this
script has never heard of is audited on the run it appears, and gets a verdict.

One thing the walk finds is genuinely out of scope, and it is excluded by a
property the defect cannot supply. A file git will not carry cannot reach a
merge, so build output under `out/` is not this gate's business. The test is
**git's index**, not git's ignore patterns: a file is in scope if it is TRACKED
(`git ls-files`) or would be added by a plain `git add .`
(`git ls-files --others --exclude-standard`). Committing a piece and then
listing it in `.gitignore` does not remove it — it stays tracked, so it stays
audited. Anything the walk finds and git disowns is PRINTED by name with the
reason; the exclusion is never silent, and it is never a directory name. With
no git available at all the walk's result is used whole, because the safe
direction is to audit more.

# What an audited unit is

A prefab whose region fits under the 48-per-axis structure-template cap ships
as one `.nbt` beside its metadata `.json`, and the `.nbt` is the unit.

A zone past that cap ships as SEVERAL `.nbt` plus one metadata `.json` carrying
a `structure_set`, and there is no single `.nbt` anywhere. For that zone the
**manifest is the unit**: `delve-admit audit` reads every tile it names and
returns one verdict over the whole zone. Handing the tool one tile instead is
refused (`DW0739`) rather than answered, because a verdict over a fifth of a
building reads as a verdict about the building.

A manifest is looked for in every directory the walk found a `.nbt` in, and its
`parts[].file` resolve against that directory. The accounting then has to close
over the whole repository:

    every in-scope .nbt is EITHER a unit of its own
                           OR a tile named by exactly one manifest

and the script asserts that identity. The closure is what makes the manifest
search safe: a tile whose manifest lives somewhere the search did not look is
an unplaced file, and unplaced is an error, never a skip:

  * a `<base>.x<i>y<j>z<k>.nbt` that no manifest claims — an orphan tile, which
    is what a half-committed zone looks like, and what a plain glob would have
    audited as if it were a whole building;
  * a manifest naming a tile that is not on disk;
  * two manifests claiming the same tile;
  * a `.nbt` git tracks that the walk did not find.

A `.json` carrying no `structure_set` is not a unit and is not audited: either
it is the metadata beside a single-file prefab — whose `.nbt` IS the unit and
carries the blocks — or it is some other document such as `pools.json`, a zone
program, or a report.

What this gate does NOT cover, stated so nobody has to infer it: objects that
are not `.nbt` structures — the campaign zone PROGRAMS (`delve-grammar audit`,
the `zone program audit` workflow) and the catalog cards under `catalog/`
(`delve-admit catalog`). Those are other gates over other objects. There is no
directory anywhere that this gate declines to walk, and nothing is left out for
sitting somewhere: the only thing that removes a `.nbt` from the audited set is
git disowning it, and that is printed by name every run.

# Binding count

Every run prints the roots it discovered and, per root, how many single-file
prefabs and how many tiled zones it examined and how many tiles those zones
covered — plus the totals, and the count of `.nbt` files the walk found. Those
numbers come from the walk and from git, so they can disagree with each other
and with the accounting, and any disagreement is red. A run that examines zero
units fails: a gate that matched nothing is not a pass.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

# The tile name `split::part_filename` gives a tile of a set. `delve-admit`
# recognises a tile by this name too (DW0739) — it is carried by the bytes
# through any copy or rename of the directory.
TILE_RE = re.compile(r"^(?P<base>.+)\.x(?P<x>\d+)y(?P<y>\d+)z(?P<z>\d+)\.nbt$")

NBT_SUFFIX = ".nbt"


class Finding(Exception):
    pass


def read_json(path: Path) -> object:
    try:
        with path.open(encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        raise Finding(f"{path}: unreadable metadata: {exc}") from exc


# --------------------------------------------------------------------------
# discovery
# --------------------------------------------------------------------------


def git_paths(root: Path, *args: str) -> set[Path] | None:
    """NUL-separated `git ls-files` output as absolute paths, or None if this
    is not a git checkout / git is not installed."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z", *args, "--", "*.nbt", "*.NBT"],
            capture_output=True,
            text=True,
        )
    except OSError:
        return None
    if proc.returncode != 0:
        return None
    return {(root / rel).resolve() for rel in proc.stdout.split("\0") if rel}


def walk_nbt(root: Path) -> list[Path]:
    """Every `.nbt` in the working tree. `.git/` is skipped; symlinked
    directories are not descended into, so a convenience symlink pointing at
    another checkout cannot double-count or loop."""
    found: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames[:] = sorted(d for d in dirnames if d != ".git")
        here = Path(dirpath)
        for name in sorted(filenames):
            if name.lower().endswith(NBT_SUFFIX):
                found.append((here / name).resolve())
    return sorted(found)


def in_scope(
    root: Path, walked: list[Path]
) -> tuple[list[Path], list[tuple[Path, str]], list[str]]:
    """Split the walk into (audited, excluded-with-reason, errors).

    In scope = git tracks it, or `git add .` would add it. That is a fact about
    git's index, which a file destined for a merge cannot fail to have; it is
    deliberately NOT a fact about `.gitignore` patterns, which a merged file
    can match.
    """
    tracked = git_paths(root)
    if tracked is None:
        # No git: the walk is the whole truth. Audit everything found — the
        # safe direction is more coverage, not less.
        return walked, [], []

    addable = git_paths(root, "--others", "--exclude-standard") or set()
    reachable = tracked | addable

    walked_set = set(walked)
    errors = [
        f"{p.relative_to(root)}: git tracks this `.nbt` but it is not on disk "
        f"(a tracked file the audit cannot read is not a file the audit passed)"
        for p in sorted(tracked - walked_set)
    ]

    audited: list[Path] = []
    excluded: list[tuple[Path, str]] = []
    for p in walked:
        if p in reachable:
            audited.append(p)
        else:
            excluded.append(
                (p, "git neither tracks it nor would add it — it cannot reach a merge")
            )
    return audited, excluded, errors


# --------------------------------------------------------------------------
# accounting
# --------------------------------------------------------------------------


def enumerate_units(
    nbts: list[Path],
) -> tuple[list[Path], list[Path], dict[Path, Path]]:
    """Return (single-file units, tiled-zone manifests, tile -> its manifest)."""
    manifests: list[Path] = []
    tile_owner: dict[Path, Path] = {}
    errors: list[str] = []

    for directory in sorted({p.parent for p in nbts}):
        for meta in sorted(directory.glob("*.json")):
            doc = read_json(meta)
            if not isinstance(doc, dict):
                continue
            tile_set = doc.get("structure_set")
            if not isinstance(tile_set, dict):
                # A single-template metadata file, or some other document such
                # as `pools.json`, a zone program or a report. Not a unit; the
                # `.nbt` beside it is.
                continue
            parts = tile_set.get("parts")
            if not isinstance(parts, list) or not parts:
                errors.append(f"{meta}: `structure_set` names no parts")
                continue
            for part in parts:
                name = (part or {}).get("file") if isinstance(part, dict) else None
                if not name:
                    errors.append(f"{meta}: a part has no `file`")
                    continue
                tile = (meta.parent / name).resolve()
                if tile in tile_owner:
                    errors.append(
                        f"{tile.name}: claimed by two manifests "
                        f"({tile_owner[tile]} and {meta})"
                    )
                    continue
                tile_owner[tile] = meta
            manifests.append(meta)

    known = set(nbts)
    singles: list[Path] = []
    for nbt in nbts:
        if nbt in tile_owner:
            continue
        if TILE_RE.match(nbt.name):
            errors.append(
                f"{nbt} is named as one tile of a set, and no manifest beside "
                f"it claims it. A tiled zone ships every tile plus the `.json` "
                f"that names them; auditing this file alone would return a "
                f"verdict over a fragment"
            )
            continue
        singles.append(nbt)

    # Every file the accounting places must actually be there, and must be one
    # of the files the walk found — a manifest cannot vouch for a file outside
    # the audited set.
    for tile, meta in sorted(tile_owner.items()):
        if not tile.is_file():
            errors.append(f"{meta} names a tile that is not on disk: {tile}")
        elif tile not in known:
            errors.append(
                f"{meta} names a tile outside the audited set: {tile} "
                f"(a manifest cannot pull a file into the audit that the walk "
                f"did not find, or that git will not carry)"
            )

    if errors:
        raise Finding("\n".join(errors))

    covered = len(singles) + len(tile_owner)
    if covered != len(nbts):
        raise Finding(
            f"accounting does not close: {len(singles)} single-file unit(s) + "
            f"{len(tile_owner)} tile(s) = {covered}, but {len(nbts)} `.nbt` "
            f"file(s) are in scope"
        )
    return singles, manifests, tile_owner


# --------------------------------------------------------------------------
# running
# --------------------------------------------------------------------------


def audit(binary: Path, unit: Path, reports: Path | None, name: str) -> tuple[int, str]:
    cmd = [str(binary), "audit", str(unit)]
    if reports is not None:
        reports.mkdir(parents=True, exist_ok=True)
        # Named by the unit's PATH, not its basename. Once the audited set spans
        # the whole repository, two roots can hold a `probe.nbt` each, and a
        # basename would have one report quietly overwrite the other.
        flat = name.replace(os.sep, "__").replace("/", "__")
        cmd += ["-o", str(reports / f"{flat}.report.json")]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    # The report is the machine-readable record; diagnostics come back on
    # stderr and are what a reader needs, so they are always relayed.
    out = proc.stderr if reports is not None else proc.stderr + proc.stdout
    return proc.returncode, out


def default_root() -> Path:
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True
        )
    except OSError:
        return Path.cwd()
    if proc.returncode != 0:
        return Path.cwd()
    return Path(proc.stdout.strip() or ".")


def emit(msg: str, github: bool) -> None:
    print(f"::error::{msg}" if github else f"error: {msg}", file=sys.stderr)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--bin", required=True, type=Path, help="the `delve-admit` binary")
    ap.add_argument(
        "--root",
        default=None,
        type=Path,
        help="repository root to walk (default: this git checkout's top level). "
        "There is no per-directory option on purpose — the audited set is "
        "discovered, and narrowing it would put the hole back.",
    )
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
        emit(f"no delve-admit binary at {args.bin}", args.github)
        return 2
    root = (args.root or default_root()).resolve()
    if not root.is_dir():
        emit(f"no repository at {root}", args.github)
        return 2

    walked = walk_nbt(root)
    nbts, excluded, scope_errors = in_scope(root, walked)

    def rel(p: Path) -> str:
        try:
            return str(p.relative_to(root))
        except ValueError:
            return str(p)

    print(f"root: {root}")
    for path, why in excluded:
        print(f"not audited: {rel(path)} — {why}")

    errors = list(scope_errors)
    singles: list[Path] = []
    manifests: list[Path] = []
    tile_owner: dict[Path, Path] = {}
    if not errors:
        try:
            singles, manifests, tile_owner = enumerate_units(nbts)
        except Finding as exc:
            errors = str(exc).splitlines()
    if errors:
        for line in errors:
            emit(line.replace(str(root) + os.sep, ""), args.github)
        return 1

    units = [(p, "prefab") for p in singles] + [(p, "tiled zone") for p in manifests]
    if not units:
        emit(
            f"the audit examined ZERO units under {root} — a gate that matched "
            f"nothing is not a pass. Is git-lfs materialized?",
            args.github,
        )
        return 1

    failed: list[Path] = []
    for unit, kind in units:
        print(f"--- auditing {rel(unit)} ({kind}) ---", flush=True)
        code, text = audit(args.bin, unit, args.reports, rel(unit))
        if text.strip():
            print(text.rstrip(), file=sys.stderr, flush=True)
        if code != 0:
            failed.append(unit)
            if args.github:
                print(
                    f"::error file={rel(unit)}::palette audit failed "
                    f"(exit {code}) — see the DW diagnostics above",
                    flush=True,
                )

    # Binding count. The roots are an OUTPUT of the walk; per-root figures come
    # from the walk, the total `.nbt` figure is what the walk found before git
    # was consulted, and the accounting had to close over the two.
    roots = sorted({p.parent for p in nbts})
    print(f"binding: {len(roots)} root(s) discovered by walking {root}:")
    for directory in roots:
        here = [p for p in nbts if p.parent == directory]
        here_singles = [p for p in here if p in singles]
        here_manifests = [m for m in manifests if m.parent == directory]
        here_tiles = [p for p in here if p in tile_owner]
        print(
            f"  {rel(directory) or '.'}: {len(here_singles)} single-file "
            f"prefab(s), {len(here_manifests)} tiled zone(s) covering "
            f"{len(here_tiles)} tile(s) — {len(here)} `.nbt` file(s)"
        )
    print(
        f"binding: examined {len(singles)} single-file prefab(s) and "
        f"{len(manifests)} tiled zone(s) covering {len(tile_owner)} tile(s); "
        f"{len(units)} audited unit(s) over {len(nbts)} in-scope `.nbt` "
        f"file(s); the walk found {len(walked)} `.nbt` file(s) and "
        f"{len(excluded)} was/were disowned by git."
    )
    if not manifests:
        print("binding: no tiled zone is present in this repository.")
    if failed:
        print(
            f"FAILED: {len(failed)} of {len(units)} unit(s): "
            + ", ".join(rel(p) for p in failed)
        )
        return 1
    print(f"PASS: {len(units)} of {len(units)} unit(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
