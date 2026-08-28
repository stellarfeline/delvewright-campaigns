#!/usr/bin/env python3
"""The authoring engine pin has a reader, and it has exactly one copy.

`versions.toml` `[engine].authoring_ref` names the engine revision an AUTHOR
builds their own toolchain from — the revision `/new-delve` Init step 2 checks
out and builds. `.github/pins.toml` registers it and `tools/check-pins.py` holds
it to its policy. This script holds it to the two things that checker cannot
reach, and it is this repository's own file: it is never vendored, so nothing
that can go wrong with a vendored copy can stop it running.

## Why the vendored checker cannot reach these

`check-pins.py` discovers pins by scanning FETCH_SITES — workflow files,
manifests, Dockerfiles, shell. Markdown is deliberately outside that list,
because in every other repository a markdown file is prose and a revision
literal in prose fetches nothing.

That reasoning is correct and it does not hold for a skill page. `SKILL.md` is
not prose: it is a procedure a person executes command by command, and it is
precisely where somebody would paste the revision so the reader does not have to
look it up. A second copy there is invisible to pin discovery, drifts silently
from `versions.toml` the first time the pin moves, and hands the author an
engine nobody chose. The indirection is the whole repair — a literal on the page
goes stale, a read from the manifest stays true — so the indirection is what
gets checked.

The other half is the pin's SHAPE. `check-pins.py` judges a registered value
against upstream history, but it never asks what the value in the manifest looks
like: a branch name, a tag, or `HEAD` sits in that key perfectly happily, is not
a 40-hex literal, and so is not discovered as a pin at all — the registry entry
would then describe a value the file no longer holds and red for the wrong
reason, or, if somebody removed the entry too, for no reason at all. A moving
reference in that key is the exact defect this pin exists to remove, so it is
refused here by shape, before any question of history arises.

## What it demands

- `versions.toml` carries `[engine].authoring_ref`, and its value is a full
  lowercase 40-hex revision. A branch, a tag, `HEAD`, or a short sha is refused
  by name: an author fetching it would get whatever that reference meant on the
  day they ran, which is the moving instrument this pin replaced.
- The revision appears in NO other tracked file. `versions.toml` is the single
  copy; the skill page reads it from there.
- The skill page really reads it: `.claude/skills/new-delve/SKILL.md` names
  `authoring_ref`. A pin whose only reader is prose is a doc line, and a page
  that clones the engine without consulting the manifest is the state this pin
  was written to end.

## Which copies are allowed, and why that is not an exemption

`.github/pins.toml` necessarily carries the value — it is the registry, and the
entry's `value` IS the declaration. So the second-copy scan skips it, and an
exemption that stopped there would be the escape hatch the defect can supply: a
registry gone stale looks exactly like a registry deliberately unchanged.

It is replaced by a stronger demand rather than waived. The registry must parse,
exactly ONE entry must carry the manifest's revision AND name `versions.toml`
among its sites, and that entry is the authoring pin. Unregistered, nothing says
on what terms the pin may move; registered twice AT THIS MANIFEST, one literal
carries two decisions about when it may move and the effective obligation is the
disjunction of their policies — as strong as the weaker, and picked by whoever
wrote the second entry. The copy that is allowed is the copy that is checked.

A REVISION IS NOT A PIN — an occurrence of it at a declared site is. Two pins
answering different questions may hold the same revision, and where both track
the engine's moving tip, coinciding is their normal state rather than an
exception: `admit-ref` names which engine's rules judge a prefab, this one names
which engine an author builds from, and the day both were last re-pinned at the
same tip they agree. So the second-copy scan accounts an occurrence against the
sites the REGISTRY declares for that revision, and reports only what no entry
holding it declared. Asking the question of the bare value instead reported
`admit-ref`'s own correctly-declared site as this pin's stray second copy — an
honest, affirmative answer about a different object, and a refusal with no
truthful repair, since neither pin's value was wrong.

That accounting cannot become the hatch, because a declared site is not free.
`check-pins.py` holds every entry to its sites in the other direction: a shaped
value declared at a site pin discovery cannot see there — a markdown page, which
is prose to it — reds as a registry that drifted from its file. So a duplicate
pasted into the skill page cannot be silenced by adding that page to an entry's
`sites`; the escape route reds one gate over. Every exempted path is printed with
the run, so the accounting is visible rather than assumed.

Every count printed carries its DENOMINATOR — examined against what population —
because a truthful count over a truncated input is the failure this repository
has already paid for once. A binding of zero is a finding, not a pass.

Exit 0 = pass, 1 = a finding, 2 = the manifest is unusable.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys
import tomllib

MANIFEST = "versions.toml"
KEY = ("engine", "authoring_ref")
SKILL = ".claude/skills/new-delve/SKILL.md"
REGISTRY = ".github/pins.toml"

RE_REV = re.compile(r"[0-9a-f]{40}")


def tracked_files(root: pathlib.Path) -> list[str]:
    """Every tracked, authored file. Nothing is skipped, and that is deliberate.

    The population is `git ls-files`, which yields only tracked files — exactly
    the set a second copy of the revision can hide in. A skip list over this
    population can only subtract real content; build output is not tracked and
    was never in the list. The same lesson `check-pins.py` records against its
    own `BUILD_OUTPUT_DIRS`, and it cost 27 campaign documents the last time the
    two populations were confused.
    """
    out = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    files = []
    for rel in out.split("\0"):
        if not rel:
            continue
        p = root / rel
        if p.is_symlink() or not p.is_file():
            continue
        files.append(rel)
    return sorted(files)


def read_text(path: pathlib.Path) -> str | None:
    try:
        t = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None
    return None if "\0" in t[:4096] else t


def manifest_value(root: pathlib.Path) -> tuple[str | None, str | None]:
    """The declared authoring revision, or the reason there is not one."""
    text = read_text(root / MANIFEST)
    if text is None:
        return None, f"{MANIFEST} is not a readable file in this repo"
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        return None, f"{MANIFEST} is not parseable TOML ({exc})"
    node: object = data
    for part in KEY:
        if not isinstance(node, dict) or part not in node:
            return None, (
                f"{MANIFEST} has no `{'.'.join(KEY)}`. That key is the engine "
                f"revision an author builds their toolchain from; without it the "
                f"skill has nothing to read and the clone follows whatever the "
                f"default branch is that hour."
            )
        node = node[part]
    if not isinstance(node, str):
        return None, f"{MANIFEST} `{'.'.join(KEY)}` is not a string"
    return node, None


def registry_entry(
    root: pathlib.Path, value: str
) -> tuple[list[str], set[str]]:
    """Exactly one registry entry declares this revision AT THIS MANIFEST.

    Returns the findings and the set of paths the registry accounts this
    revision to — every site declared by every entry holding it. That set is
    what the second-copy scan reads: an occurrence at a declared site belongs to
    a pin somebody registered, and only an occurrence nobody declared is a stray
    copy.

    Identity is (entry, site) and never the bare value, because two pins that
    both track the engine's moving tip hold the same revision as their normal
    state. What may not happen is two entries claiming the SAME occurrence:
    `versions.toml` is this pin's site, and a second entry naming it would put
    two decisions on one literal, with the effective obligation the disjunction
    of their policies.

    This is also what makes skipping `REGISTRY` in the scan a demand rather than
    an exemption. A stale registry and a deliberately-unchanged one read
    identically, so the skip is paid for by asking the registry a question only
    a current entry can answer.
    """
    text = read_text(root / REGISTRY)
    if text is None:
        return [
            f"{REGISTRY} is not a readable file in this repo, so nothing "
            f"registers the authoring pin and nothing says on what terms it may "
            f"move"
        ], set()
    try:
        pins = tomllib.loads(text).get("pin", [])
    except tomllib.TOMLDecodeError as exc:
        return [f"{REGISTRY} is not parseable TOML ({exc})"], set()
    entries = [p for p in pins if p.get("value") == value]
    accounted = {
        s
        for p in entries
        for s in p.get("sites", [])
        if isinstance(s, str)
    }
    if not entries:
        return [
            f"no entry in {REGISTRY} declares {value}. The revision in "
            f"`{MANIFEST}` moved and the registry did not, so the terms on "
            f"record describe a revision nobody builds with."
        ], accounted
    owners = [p for p in entries if MANIFEST in p.get("sites", [])]
    ids = ", ".join(str(p.get("id", "<unnamed>")) for p in entries)
    if not owners:
        return [
            f"{len(entries)} entr{'y' if len(entries) == 1 else 'ies'} in "
            f"{REGISTRY} declare{'s' if len(entries) == 1 else ''} the "
            f"authoring revision ({ids}) and none names {MANIFEST} among its "
            f"sites, so the registry is describing some other file"
        ], accounted
    if len(owners) > 1:
        owner_ids = ", ".join(str(p.get("id", "<unnamed>")) for p in owners)
        return [
            f"{len(owners)} entries in {REGISTRY} declare {value} with "
            f"{MANIFEST} among their sites ({owner_ids}). One literal cannot "
            f"carry two decisions about when it may move: the effective "
            f"obligation becomes the disjunction of their policies, only as "
            f"strong as the weakest, chosen by whoever wrote the second entry "
            f"rather than by the object."
        ], accounted
    others = [p for p in entries if p not in owners]
    also = (
        ""
        if not others
        else (
            f"; the same revision is also held, at its own site(s), by "
            f"{', '.join(str(p.get('id', '<unnamed>')) for p in others)}"
        )
    )
    print(
        f"  ok   {REGISTRY} registers it once at {MANIFEST} "
        f"({owners[0].get('id', '<unnamed>')}){also}"
    )
    return [], accounted


def check(root: pathlib.Path) -> tuple[int, list[str]]:
    errors: list[str] = []
    value, why = manifest_value(root)
    if value is None:
        print(f"check-authoring-pin: FATAL — {why}", file=sys.stderr)
        raise SystemExit(2)

    shaped = bool(RE_REV.fullmatch(value))
    if not shaped:
        errors.append(
            f"`{'.'.join(KEY)}` is {value!r}, which is not a full 40-hex "
            f"revision. A branch, a tag or a short sha is a MOVING reference, "
            f"and an author fetching it gets whatever it meant on the day they "
            f"ran — which is the defect this pin replaced. Name the revision."
        )

    reg_errors, accounted = registry_entry(root, value)
    errors.extend(reg_errors)

    files = tracked_files(root)
    # An occurrence is accounted for when the REGISTRY declares this revision at
    # that file — which covers `MANIFEST` (this pin's own site, demanded above)
    # and every site of every other entry holding the same revision. `REGISTRY`
    # itself is skipped because its `value` IS the declaration; `registry_entry`
    # replaces that skip with a stricter demand, so the copy that is allowed is
    # the copy that is checked. `MANIFEST` is named here as well as derived, so
    # a registry that has stopped declaring it produces the one finding above
    # rather than a second, louder one about a file that is doing its job.
    accounted = accounted | {MANIFEST, REGISTRY}
    others = [f for f in files if f not in accounted]
    examined = 0
    if not shaped:
        # An unshaped value is an ordinary WORD, and searching the tree for it
        # returns every file that happens to contain it — a value of `main`
        # matched 35 files here, burying the one real finding under 35 that say
        # nothing. A diagnostic that hides its own subject is a defect, so the
        # scan is not run at all when there is no revision to scan for, and the
        # run says so. This cannot let anything pass: the shape finding above is
        # already recorded, so the exit is a red either way.
        print(
            f"-- second-copy scan: not run — `{'.'.join(KEY)}` is not a "
            f"revision, so there is no revision string to find a second copy of"
        )
    else:
        for rel in others:
            text = read_text(root / rel)
            if text is None:
                continue
            examined += 1
            if value in text:
                errors.append(
                    f"{rel} carries the authoring revision too. `{MANIFEST}` is "
                    f"the single copy and every reader extracts it from there — "
                    f"a second literal drifts the first time the pin moves, and "
                    f"nothing reports it, because pin discovery does not read "
                    f"prose."
                )
        held = sorted(p for p in accounted if p in set(files))
        print(
            f"-- second-copy scan: {examined} readable tracked file(s) "
            f"examined, out of {len(others)} tracked beside the "
            f"{len(held)} the registry accounts this revision to "
            f"({', '.join(held)}) — {len(files)} tracked in all"
        )
        if examined == 0:
            errors.append(
                "the second-copy scan read no file at all. It is that scan "
                "which stops a duplicate revision living where pin discovery "
                "cannot see it, so a zero here is the gate going dark, not a "
                "clean tree."
            )

    skill = read_text(root / SKILL)
    if skill is None:
        errors.append(
            f"{SKILL} is not a readable file in this repo, so the authoring pin "
            f"has no reader and nothing consults it"
        )
    elif KEY[-1] not in skill:
        errors.append(
            f"{SKILL} never names `{KEY[-1]}`, so the page that builds the "
            f"author's toolchain does not consult the pin. A pin whose only "
            f"reader is prose is a doc line: the page would clone the engine's "
            f"default branch and the author would author against whatever it "
            f"was that hour."
        )
    else:
        print(f"  ok   {SKILL} reads `{KEY[-1]}` from {MANIFEST}")

    return 1 + examined, errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=None, help="repo root (default: this repo)")
    args = ap.parse_args()
    root = (
        pathlib.Path(args.root).resolve()
        if args.root
        else pathlib.Path(__file__).resolve().parent.parent
    )
    print(f"== authoring pin — root {root} ==")

    bound, errors = check(root)
    print(f"-- binding: {bound} file(s) held to the authoring pin")
    if bound == 0:
        print(
            "check-authoring-pin: FAIL — a binding of zero. This gate examined "
            "nothing, which is not a pass.",
            file=sys.stderr,
        )
        return 1

    if errors:
        print(
            f"check-authoring-pin: FAIL — {len(errors)} finding(s)", file=sys.stderr
        )
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print("check-authoring-pin: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
