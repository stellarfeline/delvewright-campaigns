#!/usr/bin/env python3
"""A vendored file is the upstream file, byte for byte, or it is a finding.

`tools/check-pins.py` exists in this repository and in the pipeline repository,
and it is ONE tool. It is not maintained twice: the pipeline's copy is the
source, this one is a verbatim vendored copy, and this script is what makes that
sentence checkable instead of aspirational.

## What went wrong, and why a binding count could not catch it

The two copies once differed by a single constant — a list of directory names the
scanner skipped. In the pipeline repository every name in it matched zero tracked
files, so the entry was inert and correct where it was written. Carried here,
where `campaigns/` IS the content, that same entry removed 27 tracked files —
every campaign stage document — from both pin discovery and the fetch-verb
enumeration.

**Nothing was red and nothing could have been.** The counts were truthful about
what they were handed; the handing was the defect. A file the enumeration never
lists cannot be reported as unexamined, so the usual remedy — state your binding
count, and a zero is a finding — is powerless: the count was neither zero nor
wrong, it was about a smaller world than the one the tool claimed to cover.

That is why every count this script prints carries its DENOMINATOR: examined
against what population. A number with no denominator is the shape that failed.

## Why this is its own script, and not a mode of `check-pins.py`

Because a check that lives inside the file it validates can be removed by the
very act it exists to catch. `check-pins.py` does not reject unknown registry
keys — measured, not assumed: adding `vendors` to an entry and running it exits
0 with no complaint. So had this check been a mode of that tool, vendoring an
OLDER copy of it would carry a `vendors` key nothing reads, the audit step would
print `check-pins: ok`, and the drift check would vanish at precisely the moment
the copies had drifted. The defect would supply its own exemption, which is the
one thing an escape hatch may never do.

This script is therefore NOT vendored. It is this repository's own, it is never
copied from anywhere, and nothing that can go wrong with a vendored file can stop
it running.

## What it demands, and there is no way to satisfy it but the truth

For every path a registry entry declares in `vendors`:

- the path is TRACKED here (an untracked copy ships to nobody);
- its bytes equal the bytes of the same path in the pinned repository AT THE
  PINNED REVISION, read out of git objects with `git show <value>:<path>` rather
  than off the worktree, so the comparison names its instrument literally and a
  dirty or re-pointed checkout cannot quietly change the answer;
- no commit has touched that path upstream since the entry's `reviewed`.

The last is what keeps the guarantee alive between re-pins. Byte-identity against
a pinned revision is satisfied forever by never looking; the upstream watch is
what turns "the source moved and this copy did not" into a red. It is the same
demand `check-pins.py` makes of a `track` pin's sources, asked of the paths this
repository copies rather than the packages it builds.

There is no acknowledgement, no override and no per-file exemption, deliberately.
A vendored path that cannot be compared is a red, not a skip — an absent
checkout, a missing file on either side, or a registry that declares nothing to
vendor all fail. A binding of zero is a finding, because "nobody declared
anything" is exactly what the defect looks like.

Exit 0 = pass, 1 = a finding, 2 = the registry or a checkout is unusable.
"""

from __future__ import annotations

import argparse
import hashlib
import pathlib
import subprocess
import sys
import tomllib


def git_text(repo: pathlib.Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


def git_bytes(repo: pathlib.Path, *args: str) -> bytes:
    """Raw bytes, never decoded — byte-identity is the whole question here."""
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        check=True,
    ).stdout


def default_head(repo: pathlib.Path) -> str:
    for ref in ("refs/remotes/origin/HEAD", "refs/remotes/origin/main"):
        try:
            return git_text(repo, "rev-parse", ref)
        except subprocess.CalledProcessError:
            continue
    return git_text(repo, "rev-parse", "HEAD")


def digest(data: bytes) -> str:
    """sha256 of CONTENTS.

    Spelled out because the neighbouring mistake is easy and silent: hashing the
    OUTPUT of `shasum` hashes the file PATHS as well as the bytes, so two copies
    under different names compare unequal while being identical. Here the bytes
    go in and nothing else does.
    """
    return hashlib.sha256(data).hexdigest()


def tracked_here(root: pathlib.Path) -> set[str]:
    out = git_bytes(root, "ls-files", "-z").decode("utf-8")
    return {rel for rel in out.split("\0") if rel}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=None, help="repo root (default: this repo)")
    ap.add_argument(
        "--registry", default=".github/pins.toml", help="pin registry, root-relative"
    )
    ap.add_argument(
        "--checkout",
        action="append",
        default=[],
        metavar="ID=PATH",
        help="full checkout of the repo a pin names",
    )
    args = ap.parse_args()

    root = (
        pathlib.Path(args.root).resolve()
        if args.root
        else pathlib.Path(__file__).resolve().parents[1]
    )
    registry_path = root / args.registry
    if not registry_path.is_file():
        print(f"check-vendored: FATAL — no pin registry at {registry_path}",
              file=sys.stderr)
        return 2

    with registry_path.open("rb") as fh:
        registry = tomllib.load(fh).get("pin", [])

    checkouts: dict[str, pathlib.Path] = {}
    for spec in args.checkout:
        if "=" not in spec:
            print(f"check-vendored: FATAL — --checkout wants ID=PATH, got {spec!r}",
                  file=sys.stderr)
            return 2
        pid, _, path = spec.partition("=")
        checkouts[pid] = pathlib.Path(path).resolve()

    print(f"== vendored files — registry {args.registry}, root {root} ==")

    tracked = tracked_here(root)
    entries = [p for p in registry if p.get("vendors")]

    # A binding of zero is a finding. "Nobody declared anything to vendor" is
    # indistinguishable from "the declaration was deleted", and the second is the
    # defect this script exists to catch.
    if not entries:
        print(
            f"check-vendored: FINDING — no registry entry declares `vendors`, so "
            f"nothing was compared.\n"
            f"      {len(registry)} entr(ies) in the registry, "
            f"{len(tracked)} tracked file(s) in this repository.\n"
            f"      This tool exists because files here are verbatim copies of "
            f"another repository's.\n"
            f"      An empty declaration is how that guarantee disappears "
            f"silently, so it is a red rather than a quiet pass.",
            file=sys.stderr,
        )
        return 1

    errors: list[str] = []
    compared = 0

    for pin in entries:
        pid = pin.get("id", "<unnamed>")
        vendors = pin["vendors"]
        upstream = pin.get("repo", "<unnamed repo>")
        value = pin.get("value")
        repo = checkouts.get(pid)

        if repo is None:
            errors.append(
                f"{pid}: declares {len(vendors)} vendored path(s) and no "
                f"--checkout {pid}=<path> was given. A drift check that silently "
                f"skips is the omission it exists to prevent."
            )
            continue

        try:
            git_text(repo, "cat-file", "-e", f"{value}^{{commit}}")
        except subprocess.CalledProcessError:
            errors.append(
                f"{pid}: {value} is not a commit in {upstream} — the pin names "
                f"nothing, so there is no upstream file to compare against"
            )
            continue

        upstream_tracked = [
            rel
            for rel in git_text(repo, "ls-tree", "-r", "--name-only", value).splitlines()
            if rel
        ]
        print(
            f"  ---  {pid}: {len(vendors)} vendored path(s) declared, against "
            f"{len(tracked)} tracked file(s) here and "
            f"{len(upstream_tracked)} at {upstream} {value[:8]}"
        )

        for rel in vendors:
            local = root / rel
            if rel not in tracked:
                errors.append(
                    f"{pid}: `{rel}` is declared vendored and is not tracked in "
                    f"this repository — an untracked copy ships to nobody"
                )
                continue
            try:
                theirs = git_bytes(repo, "show", f"{value}:{rel}")
            except subprocess.CalledProcessError:
                errors.append(
                    f"{pid}: `{rel}` does not exist at {upstream} {value[:8]} — "
                    f"this repository is vendoring a file the source does not have"
                )
                continue

            mine = local.read_bytes()
            compared += 1
            if mine != theirs:
                errors.append(
                    f"{pid}: `{rel}` has DRIFTED from {upstream} {value[:8]}.\n"
                    f"      here     {digest(mine)}  ({len(mine)} bytes)\n"
                    f"      upstream {digest(theirs)}  ({len(theirs)} bytes)\n"
                    f"      This file is not maintained here. Copy it from the\n"
                    f"      pinned checkout — `git -C <checkout> show "
                    f"{value[:8]}:{rel}` —\n"
                    f"      or, if the change belongs in the tool, make it "
                    f"upstream\n"
                    f"      and re-pin. Editing this copy in place is what "
                    f"splits one\n"
                    f"      tool into two that agree until the day they matter."
                )
            else:
                print(f"  ok   {pid}: `{rel}` identical to {upstream} "
                      f"{value[:8]} ({len(mine)} bytes, {digest(mine)[:12]})")

        # Byte-identity against a PINNED revision is satisfied forever by never
        # looking. This is the half that expires: if the source moved after the
        # entry was last reviewed, the copy is stale even though it matches.
        reviewed = pin.get("reviewed")
        if not reviewed:
            errors.append(
                f"{pid}: declares `vendors` and carries no `reviewed`. Matching a "
                f"pinned revision proves the copy was right once; only `reviewed` "
                f"says anyone has looked since."
            )
            continue
        try:
            git_text(repo, "cat-file", "-e", f"{reviewed}^{{commit}}")
        except subprocess.CalledProcessError:
            errors.append(
                f"{pid}: `reviewed` names {reviewed}, which is not a commit in "
                f"{upstream}"
            )
            continue

        head = default_head(repo)
        moved = git_text(
            repo, "log", "--oneline", f"{reviewed}..{head}", "--", *vendors
        ).splitlines()
        if moved:
            listed = "".join(f"      {line}\n" for line in moved[:20])
            more = f"      … and {len(moved) - 20} more\n" if len(moved) > 20 else ""
            errors.append(
                f"{pid}: {len(moved)} commit(s) have changed the vendored "
                f"source(s) upstream since this pin was last reviewed "
                f"({reviewed[:8]}):\n"
                + listed
                + more
                + f"      Byte-identity against {value[:8]} cannot see this: a "
                f"frozen revision\n"
                f"      is matched forever by never looking. Re-pin `value` to a "
                f"commit that\n"
                f"      carries them, re-vendor {', '.join(vendors)}, and set "
                f"`reviewed`."
            )
        else:
            print(
                f"  ok   {pid}: no upstream change to "
                f"{', '.join(vendors)} since {reviewed[:8]}"
            )

    print(
        f"-- binding: {compared} vendored file(s) compared byte-for-byte, "
        f"from {len(entries)} registry entr(ies) of {len(registry)}, against "
        f"{len(tracked)} tracked file(s) in this repository"
    )

    if not compared and not errors:
        print(
            "check-vendored: FINDING — entries declare vendored paths and none "
            "was compared.\n"
            "      A pass with a binding of zero is the vacuity this check "
            "exists to refuse.",
            file=sys.stderr,
        )
        return 1

    if errors:
        for e in errors:
            print(f"check-vendored: FINDING — {e}", file=sys.stderr)
        return 1

    print("check-vendored: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
