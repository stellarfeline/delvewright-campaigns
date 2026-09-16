#!/usr/bin/env python3
"""The engine a release is built with is newer than every claim a storybook makes.

`versions.toml` `[engine] ref` names the engine release `.github/workflows/
release.yml` checks out to build and validate a delve image. It is a RELEASE TAG
in the engine's own grammar (`<name>--v<major>.<minor>.<patch>`), registered as
`engine-release` in `.github/pins.toml`.

## Why this script exists at all

A tag name carries no shape a scan can find. `tools/ci/check-pins.py` discovers a
40-hex revision or a digest wherever it sits, and it says so itself: "a version
string is not [found], and no amount of declaring makes it so". An entry whose
value cannot be discovered may not rest on `sites` alone — that claim is
unfalsifiable — so it names `bound_by`, the checker that holds its sites, and
`bound_key`, the key that checker reads the value under. This is that checker and
the key is `engine.ref`.

## What it holds, and why that is a real question rather than a restatement

Re-reading `engine.ref` and comparing it to the registry would be circular: the
pin gate already verifies the value stands in every declared site. So the binding
is the obligation a reader of that key actually has.

A campaign's storybook marker states the compiler the campaign was last verified
with:

    > **Requires delve engine 1.5.0 or newer** — last verified with delvec 1.5.0 …

A delve is built with the pinned engine and nothing else. If a campaign claims a
delvec NEWER than the one this file pins, then either the claim is false or the
pin is behind what the campaign needs — and both answers are discovered at the
most expensive possible moment, because the pin's only other reader is the
release workflow, which runs on a tag push. The same refusal is made here, on
every pull request, out of the two files that already state it.

The comparison is one-directional, like the engine-side check it mirrors: a
storybook may claim an OLDER delvec (a campaign nobody has re-verified is not a
release blocker), and may not claim a newer one.

## The grammar is not re-implemented

`tools/lib/release_tags.py` is the engine's release-tag grammar, vendored beside
`tools/ci/check-pins.py` because that file imports it. This script parses the
pinned tag through the same module, so this repository holds one grammar and not
a second private regex that agrees with it until the day it matters.

States its binding with denominators; a binding of zero is a finding, because a
repository with no storybook to check is indistinguishable from a walk that found
none. Stdlib only, offline.

Exit 0 = pass, 1 = a finding, 2 = a file this check needs is unusable.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys
import tomllib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / "lib"))
import release_tags  # noqa: E402  — one grammar, vendored, never a second copy

BOUND_KEY = "engine.ref"
MARKER_RE = re.compile(r"last verified with delvec (\d+\.\d+\.\d+)")


def tracked(root: pathlib.Path) -> list[str]:
    out = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z"],
        capture_output=True,
        check=True,
    ).stdout.decode("utf-8")
    return [rel for rel in out.split("\0") if rel]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=None, help="repo root (default: this repo)")
    args = ap.parse_args()

    root = (
        pathlib.Path(args.root).resolve()
        if args.root
        else pathlib.Path(__file__).resolve().parents[1]
    )

    manifest = root / "versions.toml"
    if not manifest.is_file():
        print(f"check-engine-pin: FATAL — no versions.toml at {manifest}", file=sys.stderr)
        return 2
    with manifest.open("rb") as fh:
        engine = tomllib.load(fh).get("engine", {})
    ref = engine.get("ref")
    if not ref:
        print(
            "check-engine-pin: FATAL — versions.toml has no `engine.ref`, which is "
            "the key this check is registered against in .github/pins.toml",
            file=sys.stderr,
        )
        return 2

    try:
        name, pinned = release_tags.parse(ref)
    except release_tags.Refused as exc:
        print(
            f"check-engine-pin: FINDING — versions.toml `{BOUND_KEY}` is not a "
            f"release tag: {exc}",
            file=sys.stderr,
        )
        return 1
    pinned_key = release_tags.version_key(pinned)

    files = tracked(root)
    storybooks = [
        f for f in files if f.startswith("campaigns/") and pathlib.PurePath(f).name.startswith("README")
    ]

    print(
        f"== engine pin — versions.toml `{BOUND_KEY}` = {ref} ({name} {pinned}), "
        f"against {len(storybooks)} storybook(s) of {len(files)} tracked file(s) =="
    )

    errors: list[str] = []
    examined = 0
    for rel in sorted(storybooks):
        text = (root / rel).read_text(encoding="utf-8")
        found = MARKER_RE.findall(text)
        if not found:
            print(f"  ---  {rel}: no `last verified with delvec` marker, nothing to hold")
            continue
        for claimed in found:
            examined += 1
            if release_tags.version_key(claimed) > pinned_key:
                errors.append(
                    f"{rel} says it was last verified with delvec {claimed}, and "
                    f"`{BOUND_KEY}` pins {name} {pinned}. A release builds with the "
                    f"pinned engine and nothing else, so this campaign would ship "
                    f"built by a compiler older than the one it claims to have "
                    f"passed on. Move the pin to the release that carries "
                    f"{claimed}, or re-verify the campaign against {pinned} and "
                    f"say so in the marker."
                )
            else:
                print(f"  ok   {rel}: verified with delvec {claimed} <= pinned {pinned}")

    print(
        f"-- binding: {examined} storybook claim(s) judged over {len(storybooks)} "
        f"storybook(s) in campaigns/, against one pinned engine release"
    )

    if not examined and not errors:
        print(
            "check-engine-pin: FINDING — no storybook states a verified-with "
            "delvec, so the pin was compared against nothing.\n"
            "      A pass with a binding of zero is indistinguishable from a walk "
            "that found no campaigns.",
            file=sys.stderr,
        )
        return 1

    if errors:
        for e in errors:
            print(f"check-engine-pin: FINDING — {e}", file=sys.stderr)
        return 1

    print("check-engine-pin: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
