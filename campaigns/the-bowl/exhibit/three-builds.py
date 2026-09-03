#!/usr/bin/env python3
"""The Bowl, built three times from one document.

The level is the SET of three builds, not any one of them. This script produces
the set: it rewrites exactly one field of `world.json` — `content.horizon` —
runs `delvec build`, and puts every byte back the way it found it.

## What it proves, and by what

**Nothing about the map changes between the three** is a claim about bytes, so
it is measured against bytes rather than argued.

*The engine's own derivation hash.* Every build prints a `blockout sha256`: the
mass the derivation makes of the plan, the graph and the metrics table. Three
equal hashes say the three worlds hold the same map.

*The emitted files.* Independently of that hash, every file under the output
directory is hashed BY CONTENT — never by piping `shasum` output through a
second hash, which would hash the differing PATHS too — and the three maps of
path to hash are compared. Every path that differs is NAMED and classified
rather than excluded up front: an exclusion list decided before the measurement
is a claim about what the answer will be.

*An observer outside the engine's arithmetic.* `critical-path.json` is what the
runtime bot walks, in blocks. It is compared whole.

The three methods share the engine binary and nothing else, which is the point:
a second method that shares the first's calibration measures one error twice.

## Refusals

The exit status of `delvec` is captured before anything is piped, because a
pipeline reports the status of its last stage. A build that fails is a finding,
and this script stops rather than reporting on the part it reached.

Exit 0 = three builds, one map. 1 = a finding. 2 = this script could not run.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import shutil
import subprocess
import sys

# The three horizons, in the order the exhibit is read in: no ground at all,
# then a low rim, then a high one.
HORIZONS = [
    ("void", "void"),
    ("valley-24", {"base": "valley", "ratio": 2.5, "rim_height": 24}),
    ("valley-96", {"base": "valley", "ratio": 2.5, "rim_height": 96}),
]

SURROUND_LINE = re.compile(r"^surround: .*$", re.M)
HASH_LINE = re.compile(r"^(site plan|layout graph|blockout) sha256:\s+([0-9a-f]{64})$", re.M)


class Refusal(Exception):
    """This script could not run at all — exit 2, never a pass."""


def sha_of_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def tree_hashes(root: pathlib.Path) -> dict[str, str]:
    """Path relative to `root` -> sha256 of that file's CONTENT.

    Deliberately not `shasum -r . | shasum`: that hashes the file names into the
    answer, so two differently-named output directories come out different when
    every file in them is the same.
    """
    out: dict[str, str] = {}
    for p in sorted(root.rglob("*")):
        if p.is_file():
            out[str(p.relative_to(root))] = sha_of_file(p)
    return out


def build(delvec: str, repo: pathlib.Path, campaign: str, out: pathlib.Path,
          prefabs: str) -> tuple[int, str]:
    """One `delvec build`. Returns (exit status, combined output)."""
    argv = [delvec, "build", campaign, "-o", str(out), "--prefabs", prefabs]
    print(f"    $ {' '.join(argv)}", flush=True)
    completed = subprocess.run(argv, cwd=repo, capture_output=True, text=True)
    return completed.returncode, completed.stdout + completed.stderr


SURROUND_TEMPLATE = re.compile(r"^place template \S+:horizon/valley/\S+ -?\d+ -?\d+ -?\d+$")
PLACE_COUNT = re.compile(r"^execute if score #placeok dw\.sys matches (\d+) run function \S+$")
FORCELOAD = re.compile(r"^forceload add (-?\d+ ){3}-?\d+$")
BIOME_BAND = re.compile(r"^fillbiome (-?\d+ ){6}\S+$")
MODIFICATION_CAP = re.compile(r"^gamerule max_block_modifications \d+$")
# `DW0724`: a review camera stands up out of whatever ground is under it, so its
# height and its pitch are functions of the GROUND. Nothing else about a shot is.
CAMERA_STANDUP = re.compile(r"^/shots\[\d+\]/camera/(pitch|pos\[1\])$")


def lines_of(path: pathlib.Path) -> list[str]:
    return [ln.rstrip("\n") for ln in path.read_text(encoding="utf-8").splitlines()]


def json_diff(a, b, p: str = "") -> list[str]:
    """Every key path at which two JSON documents disagree.

    An absent key is reported at its own path, so an ADDED block shows up as one
    finding rather than as a diff of everything under it.
    """
    out: list[str] = []
    if type(a) is not type(b):
        return [p or "/"]
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                out.append(f"{p}/{k}")
            else:
                out += json_diff(a[k], b[k], f"{p}/{k}")
    elif isinstance(a, list):
        if len(a) != len(b):
            return [p or "/"]
        for i, (x, y) in enumerate(zip(a, b)):
            out += json_diff(x, y, f"{p}[{i}]")
    elif a != b:
        out.append(p or "/")
    return out


def read_difference(void: pathlib.Path, valley: pathlib.Path, path: str,
                    templates: int) -> list[str]:
    """Account for ONE differing file, line by line. Returns findings.

    The claim being checked is not *these paths are allowed to differ* — an
    exclusion list decided before the measurement is a claim about what the
    answer will be. It is the stronger and more specific one: **the void build's
    emission survives intact, and everything a valley build adds to it is
    ground.** A map that moved would have to alter or delete a line the void
    build already emitted, or add a line that is not one of the four things the
    landform is made of.
    """
    f: list[str] = []
    a, b = void / path, valley / path
    if path.endswith(".json"):
        keys = json_diff(json.loads(a.read_text()), json.loads(b.read_text()))
        stray = [k for k in keys if k != "/horizon" and not CAMERA_STANDUP.match(k)]
        print(f"        {path}: {len(keys)} key path(s) differ "
              f"({'/horizon plus ' if '/horizon' in keys else ''}"
              f"{sum(1 for k in keys if CAMERA_STANDUP.match(k))} review-camera stand-up value(s))")
        if stray:
            f.append(f"{path}: key path(s) that are not the horizon or a camera stand-up: "
                     + ", ".join(stray[:10]))
        return f

    old, new = lines_of(a), lines_of(b)
    gone = [ln for ln in old if ln.strip() and ln not in new]
    added = [ln for ln in new if ln.strip() and ln not in old]
    print(f"        {path}: {len(added)} line(s) added, {len(gone)} line(s) of the void "
          f"build not present in the valley build")

    # The ONE line a valley build is allowed to change rather than add: the
    # count `place_verify` holds every placement to. It moves from 0 to the
    # number of templates, which is the number the surround's own binding line
    # states — so the message and the bytes are cross-checked against each other
    # rather than each being believed on its own.
    survivors_expected: list[str] = []
    for ln in gone:
        m = PLACE_COUNT.match(ln)
        if m and m.group(1) == "0":
            survivors_expected.append(ln)
        else:
            f.append(f"{path}: the valley build does not carry a line the void build emitted: {ln}")
    counted = [PLACE_COUNT.match(ln) for ln in added]
    for m in [c for c in counted if c]:
        if int(m.group(1)) != templates:
            f.append(f"{path}: the placement count is {m.group(1)} and the surround binding "
                     f"line states {templates} templates")
    if survivors_expected and not any(counted):
        f.append(f"{path}: the placement count line was dropped rather than raised")

    stray = [
        ln for ln in added
        if not (SURROUND_TEMPLATE.match(ln) or PLACE_COUNT.match(ln)
                or FORCELOAD.match(ln) or BIOME_BAND.match(ln)
                or MODIFICATION_CAP.match(ln) or ln.startswith("execute if block "))
    ]
    if stray:
        f.append(f"{path}: line(s) added that are not the landform: " + " | ".join(stray[:5]))

    # A sentinel per template, and no more: `place_verify` checks one block per
    # placed template, so the two counts are the same number seen twice.
    placed = sum(1 for ln in added if SURROUND_TEMPLATE.match(ln))
    sentinels = sum(1 for ln in added if ln.startswith("execute if block "))
    if placed and placed != templates:
        f.append(f"{path}: {placed} template(s) placed, {templates} stated by the binding line")
    if sentinels and sentinels != templates:
        f.append(f"{path}: {sentinels} sentinel(s) added, {templates} stated by the binding line")
    return f


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--delvec", required=True, help="path to the delvec binary")
    ap.add_argument("--repo", required=True, help="content repository root")
    ap.add_argument("--out", required=True, help="directory the three builds go in")
    ap.add_argument("--campaign", default="campaigns/the-bowl")
    ap.add_argument("--prefabs", default="prefabs")
    args = ap.parse_args()

    repo = pathlib.Path(args.repo).resolve()
    out_root = pathlib.Path(args.out).resolve()
    world_path = repo / args.campaign / "world.json"
    if not world_path.is_file():
        raise Refusal(f"{world_path} does not exist")

    original = world_path.read_bytes()
    results: dict[str, dict] = {}
    findings: list[str] = []

    # Three DISTINCT horizons, or the exhibit is one world built three times.
    declared = [json.dumps(h, sort_keys=True) for _, h in HORIZONS]
    if len(set(declared)) != len(HORIZONS):
        raise Refusal(f"the three horizons are not distinct: {declared}")

    try:
        for name, horizon in HORIZONS:
            doc = json.loads(original.decode("utf-8"))
            doc["content"]["horizon"] = horizon
            # The EFFECT is asserted, not the exit status of the assignment: a
            # scripted rewrite that lands nowhere is a silent no-op, and this
            # one decides which of the three worlds gets built. (Equality with
            # the previous contents is NOT the assertion — one of the three is
            # the horizon the campaign is authored with, and for that one the
            # right rewrite is a no-op.)
            if doc["content"].get("horizon") != horizon:
                raise Refusal(f"the horizon did not become {horizon!r} after the rewrite")
            world_path.write_text(
                json.dumps(doc, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            target = out_root / name
            if target.exists():
                shutil.rmtree(target)
            print(f"--- {name}: horizon = {json.dumps(horizon)}", flush=True)
            status, log = build(args.delvec, repo, args.campaign, target, args.prefabs)
            (out_root / f"{name}.log").write_text(log, encoding="utf-8")
            if status != 0:
                findings.append(f"{name}: delvec build exited {status}")
                results[name] = {"status": status}
                continue
            surround = SURROUND_LINE.search(log)
            results[name] = {
                "status": 0,
                "horizon": horizon,
                "surround_line": surround.group(0) if surround else None,
                "hashes": {m.group(1): m.group(2) for m in HASH_LINE.finditer(log)},
                "tree": tree_hashes(target),
            }
    finally:
        # The tree goes back byte-identical whatever happened above, because a
        # perturbation left live is an instrument nobody knows has moved.
        world_path.write_bytes(original)

    # -- the reconciliation, which runs whatever the walk did ----------------
    reached = [n for n, _ in HORIZONS if n in results]
    missing = [n for n, _ in HORIZONS if n not in reached]
    if missing:
        findings.append(f"no result for {', '.join(missing)}")

    green = [n for n in reached if results[n].get("status") == 0]
    print()
    print(f"=== three builds: {len(green)} of {len(HORIZONS)} green")

    for name in reached:
        r = results[name]
        print(f"--- {name}")
        if r.get("status") != 0:
            print(f"    REFUSED, exit {r['status']}")
            continue
        print(f"    {r['surround_line'] or 'no surround line printed (this is the void build)'}")
        for k, v in r["hashes"].items():
            print(f"    {k} sha256: {v}")

    if len(green) < len(HORIZONS):
        for f in findings:
            print(f"FINDING: {f}")
        return 1

    # Method A — the engine's own derivation hash.
    blockouts = {results[n]["hashes"].get("blockout") for n in green}
    print()
    print("=== method A: the derivation's own hash")
    if len(blockouts) == 1:
        print(f"    all three builds derive one blockout: {blockouts.pop()}")
    else:
        findings.append(f"the blockout hash differs across the three: {blockouts}")
        print(f"    DIFFER: {blockouts}")

    # Method B — the emitted files, hashed by content, then read line by line.
    print()
    print("=== method B: every emitted file, hashed by content")
    base = green[0]  # the void build: the map with no ground at all under it
    base_tree = results[base]["tree"]
    for other in green[1:]:
        tree = results[other]["tree"]
        templates = int(re.search(r"surround: (\d+) templates",
                                  results[other]["surround_line"]).group(1))
        vanished = sorted(p for p in base_tree if p not in tree)
        appeared = sorted(p for p in tree if p not in base_tree)
        common = sorted(p for p in base_tree if p in tree)
        differing = [p for p in common if base_tree[p] != tree[p]]
        print(f"    {base} vs {other}: {len(common)} shared path(s), "
              f"{len(common) - len(differing)} byte-identical, {len(differing)} differing; "
              f"{len(appeared)} path(s) only in {other}, {len(vanished)} only in {base}")
        if vanished:
            findings.append(f"{len(vanished)} path(s) the void build emits are gone from "
                            f"{other}: " + ", ".join(vanished[:5]))
        stray_new = [p for p in appeared if "structure/horizon/valley/" not in p]
        print(f"        of the {len(appeared)} new path(s), "
              f"{len(appeared) - len(stray_new)} are the landform's own templates")
        if stray_new:
            findings.append(f"path(s) only in {other} that are not the landform: "
                            + ", ".join(stray_new[:10]))
        for p in differing:
            # `manifest.json` hashes the campaign's own input documents, and the
            # one field that was rewritten lives in `world.json`. It differing
            # is the rewrite being visible, which is the point of the exercise.
            if p == "manifest.json":
                print(f"        {p}: the input hash of the one rewritten field")
                continue
            findings += read_difference(out_root / base, out_root / other, p, templates)

    # Method C — an observer outside the engine's derivation.
    print()
    print("=== method C: the route the bot walks")
    routes = {}
    for n in green:
        p = out_root / n / "critical-path.json"
        routes[n] = sha_of_file(p) if p.is_file() else None
    if len(set(routes.values())) == 1 and None not in routes.values():
        print(f"    critical-path.json is one file in all three: {next(iter(routes.values()))}")
    else:
        findings.append(f"critical-path.json differs across the three: {routes}")
        print(f"    DIFFER: {routes}")

    print()
    if findings:
        for f in findings:
            print(f"FINDING: {f}")
        return 1
    print("three builds from one document, and one map in all three.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Refusal as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        sys.exit(2)
