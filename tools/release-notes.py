#!/usr/bin/env python3
"""A campaign's release notes, and the storybook checks they rest on.

ONE implementation, two callers:

* `release.yml`'s "compose the release notes" step runs `render` for the one
  campaign a release tag names, and publishes what it prints;
* `prefab-audit.yml`'s required job runs `check --base <the PR's base>` on
  every pull request, over the campaign directories that pull request changes.
  The release judges only the campaign it releases, built by the engine it
  pins, so an untouched campaign is not re-judged here.

Both go through `judge()` below, so a storybook the pull-request gate admits is
one the release step accepts, and a refusal is made at the pull request rather
than after a full release ladder has run on a tag push.

The reader-facing facts come from the STORYBOOK, which is the reviewed artifact,
and from nowhere else. They were once re-derived from `world.json`, which made
the notes a second rendering of the same facts with nothing binding it to the
first. So there is one source, and a campaign whose storybook does not carry
what the notes need is refused by name rather than shipped blank.

What `judge()` refuses, per campaign directory:

* no `world.json` — the directory is not a campaign, so nothing in it is
  releasable;
* no `README.md` — the notes are rendered from the storybook (spec-0007);
* a missing **Players**, **Playtime** or **Languages** header row;
* a Playtime row whose minutes disagree with `world.json` `target_minutes`;
* no blurb paragraph between the epigraph and the header table.

`check` states its binding with its denominator: changed campaign directories
judged, of the campaign directories in git's index. A change touching no
campaign, or a run with no base (a push or a dispatch), judges zero and says so
by name. Stdlib only, offline.

Exit 0 = pass, 1 = a finding.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys
from dataclasses import dataclass

ROOT = pathlib.Path(__file__).resolve().parents[1]


class Refused(Exception):
    """A campaign the release notes cannot be composed for."""


@dataclass
class Facts:
    content: dict
    title: str
    players: str
    playtime: str
    languages: str
    blurb: str


def judge(root: pathlib.Path, camp: str) -> Facts:
    """Every check the release notes make, or `Refused` naming the first failure."""
    base = root / "campaigns" / camp
    # `campaigns/<id>/` is not proof of a campaign: a directory of media and
    # build output with no stage documents is not releasable.
    try:
        content = json.loads((base / "world.json").read_text(encoding="utf-8"))["content"]
    except FileNotFoundError:
        raise Refused(
            f"{camp} has no world.json, so it is a directory rather than a campaign "
            f"— nothing here is releasable. If you meant a different campaign, check "
            f"the tag."
        ) from None
    try:
        book = (base / "README.md").read_text(encoding="utf-8")
    except FileNotFoundError:
        raise Refused(
            f"{camp} has no README.md. The release notes are rendered FROM the "
            f"storybook (spec-0007), so a campaign without one has nothing to "
            f"announce and cannot be released. Write the storybook first — title, "
            f"blurb, and a header table carrying **Players** and **Playtime**."
        ) from None

    def row(label: str) -> str:
        m = re.search(rf"^\|\s*\*\*{label}\*\*\s*\|\s*(.+?)\s*\|\s*$", book, re.M)
        if not m:
            raise Refused(
                f"{camp}/README.md has no **{label}** row — the release notes take "
                f"their reader-facing facts from the storybook, so a missing row is a "
                f"missing fact, not a blank line."
            )
        return m.group(1)

    title = (re.search(r"^#\s+(.+)$", book, re.M) or [None, content.get("title", camp)])[1]
    players, playtime = row("Players"), row("Playtime")
    languages = row("Languages")

    # The storybook and the campaign document agree about length.
    declared = content.get("target_minutes")
    book_mins = re.search(r"(\d+)\s*minute", playtime)
    if declared and book_mins and int(book_mins.group(1)) != int(declared):
        raise Refused(
            f"{camp} storybook says {playtime!r} but world.json declares "
            f"target_minutes={declared}. One of them is wrong; fix the source, not "
            f"this script."
        )

    # The blurb is the storybook's own one-paragraph pitch: what follows the last
    # blockquote (the engine-version marker and the epigraph both use one) and
    # precedes the header table. Anchoring on "after the last quote" keeps it from
    # picking up the `**vX.Y.Z**` stamp.
    head = book.split("| |")[0]
    after_quotes = head[head.rindex("\n>") :] if "\n>" in head else head
    blurb = next(
        (
            ln.strip()
            for ln in after_quotes.split("\n")
            if ln.strip() and not ln.lstrip().startswith((">", "!", "#", "|", "*"))
        ),
        None,
    )
    if not blurb:
        raise Refused(
            f"{camp}/README.md has no blurb paragraph between its epigraph and its "
            f"header table — a release with no description is a defect, not a "
            f"shorter release."
        )
    return Facts(content, title, players, playtime, languages, blurb)


def render(facts: Facts, image: str, version: str, has_pack: bool, prerelease: bool) -> str:
    out: list[str] = [f"## {facts.title}\n"]
    if prerelease:
        out.append(
            f"> **Pre-release.** v{version} is published for testing ahead of a "
            f"release; it passed the same machine checks a release does.\n"
        )
    out.append(facts.blurb + "\n")
    noun = "player" if facts.players.strip() == "1" else "players"
    out.append(f"For {facts.players} {noun}, {facts.playtime}.\n")
    out.append("### Host it\n")
    out.append("```")
    out.append(f"docker run -it -p 25565:25565 -e EULA=TRUE {image}:v{version}")
    out.append("```\n")
    out.append(
        "Players join at `<your-address>:25565` with a vanilla Minecraft Java "
        "1.21.11 client.\n"
    )
    if has_pack:
        out.append(
            "The resource pack (character skins and in-game art) is served by the "
            "delve itself — accept the prompt when you join. Nothing to install by "
            "hand.\n"
        )
    out.append(
        f"Languages: {facts.languages}. In-game text follows your Minecraft "
        f"client's language where the delve has been translated; accept the "
        f"resource-pack prompt and it happens by itself.\n"
    )
    out.append("### Terms\n")
    out.append(
        "This release contains **no Minecraft server software**. The server is "
        "downloaded by the container on first start, and you accept "
        "[Mojang's EULA](https://aka.ms/MinecraftEULA) yourself by passing "
        "`EULA=TRUE`. Delvewright is not affiliated with Mojang or Microsoft.\n"
    )
    out.append(
        "Campaign content is licensed "
        "[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/); "
        "see the repository README for the full picture.\n"
    )
    return "\n".join(out) + "\n"


def _git_z(root: pathlib.Path, *args: str) -> list[str]:
    out = subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, check=True
    ).stdout.decode("utf-8")
    return [rel for rel in out.split("\0") if rel]


def _campaign_of(rel: str) -> str | None:
    parts = pathlib.PurePosixPath(rel).parts
    if len(parts) >= 3 and parts[0] == "campaigns":
        return parts[1]
    return None


def campaign_dirs(root: pathlib.Path) -> list[str]:
    """Every directory directly under `campaigns/` that git's index holds a file in."""
    files = _git_z(root, "ls-files", "-z", "--", "campaigns/")
    return sorted({c for c in map(_campaign_of, files) if c})


def changed_campaigns(root: pathlib.Path, base: str) -> tuple[list[str], int]:
    """Campaign directories with a file changed between `base` and HEAD, and how
    many changed paths under `campaigns/` the diff listed."""
    files = _git_z(root, "diff", "--name-only", "-z", "--no-renames", base, "HEAD",
                   "--", "campaigns/")
    return sorted({c for c in map(_campaign_of, files) if c}), len(files)


def cmd_check(root: pathlib.Path, base: str) -> int:
    """Judge the campaign directories a pull request changes.

    The release step judges exactly one campaign, the one its tag names, and a
    campaign is only ever built by the engine revision it pins. So the
    pull-request arm judges what the release would judge of THIS change: every
    campaign directory the diff against the pull request's base touches, and
    no other. An untouched campaign is not re-judged here.
    """
    on_tree = campaign_dirs(root)
    if not base:
        print(
            f"release-notes: 0 changed campaign director(ies) judged of {len(on_tree)} "
            f"on the tree — no pull-request base was given (a push or a manual "
            f"dispatch has none), so no change exists to judge. Named zero binding."
        )
        return 0
    changed, npaths = changed_campaigns(root, base)
    present = [c for c in changed if c in on_tree]
    gone = [c for c in changed if c not in on_tree]
    refused = 0
    for camp in present:
        try:
            facts = judge(root, camp)
        except Refused as exc:
            refused += 1
            print(f"release-notes: REFUSED {camp}: {exc}")
            continue
        print(f"release-notes: ok      {camp}: Playtime {facts.playtime!r}, "
              f"target_minutes={facts.content.get('target_minutes')}")
    for camp in gone:
        print(f"release-notes: removed {camp}: changed by this diff and no longer on "
              f"the tree, so there is nothing to release and nothing to judge")
    print(
        f"release-notes: {len(present)} changed campaign director(ies) judged of "
        f"{len(on_tree)} on the tree ({npaths} changed path(s) under campaigns/ "
        f"against base {base[:12]}; {len(gone)} changed director(ies) removed); "
        f"{len(present) - refused} composable, {refused} refused"
    )
    if not present:
        print("release-notes: this change touches no campaign on the tree — a named "
              "zero binding, not a pass over campaigns it did not change")
    return 1 if refused else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=None, help="repo root (default: this repo)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="judge the campaign directories changed since --base")
    c.add_argument("--base", required=True,
                   help="the pull request's base revision; empty = no base (judges 0, says so)")
    r = sub.add_parser("render", help="print one campaign's release notes")
    r.add_argument("--campaign", required=True)
    r.add_argument("--image", required=True)
    r.add_argument("--version", required=True)
    r.add_argument("--has-pack", choices=["true", "false"], required=True)
    r.add_argument("--prerelease", choices=["true", "false"], required=True)
    args = ap.parse_args()
    root = pathlib.Path(args.root).resolve() if args.root else ROOT

    if args.cmd == "check":
        return cmd_check(root, args.base)
    try:
        facts = judge(root, args.campaign)
    except Refused as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    sys.stdout.write(render(facts, args.image, args.version,
                            args.has_pack == "true", args.prerelease == "true"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
