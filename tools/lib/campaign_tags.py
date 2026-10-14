"""The release tag grammar for this repository's levels, stated once, and every decision that hangs off it.

## What it is

A level ships from this repository by a tag, in one of three families:

    release/<campaign>/v<major>.<minor>.<patch>                 a campaign release
    prerelease/<campaign>/v<major>.<minor>.<patch>-<prerelease> a campaign pre-release
    reference/<level>/v<major>.<minor>.<patch>                  a reference level release

A campaign lives in `campaigns/<id>/`; a reference level — a level that shows
how to build one kind of map — lives whole in `references/<id>/`. The family
decides the category, and the category decides everything that keeps the two
apart: the directory the level is read from, the prefab directory it builds
with, the image it is published as, and the title of its Release.

`.github/workflows/release.yml` fires on all three. Its trigger filter can only say
"starts with the family and has a `/v`"; the strict half is this module, which
the workflow's first step runs before anything is built, so a tag the filter
lets through and the grammar refuses stops there with a named refusal.

The family and the version must agree: a `release/` or `reference/` tag
carries no prerelease part, and a `prerelease/` tag must carry one. Build metadata (`+...`) is refused
in both, because `v<version>` becomes an OCI image tag and that charset has no
`+`.

What follows from the family is decided here as well, so the workflow restates
none of it:

- a release is published as the campaign's GitHub Release, and its image is
  pushed as `v<version>` and `latest`;
- a pre-release is published as a GitHub pre-release that is never marked
  latest, and its image is pushed as `v<version>` only;
- a campaign is read from `campaigns/<id>/`, builds with the shared library
  `prefabs/`, is published as `ghcr.io/<owner>/delve-<id>`, and its Release is
  titled `<title> v<version>`;
- a reference level is read from `references/<id>/`, builds with its own
  `references/<id>/prefabs/`, is published as
  `ghcr.io/<owner>/delve-reference-<id>`, and its Release is titled
  `Reference level: <title> v<version>`. It has no pre-release family.

A campaign id may not begin with `reference-`: `delve-reference-<x>` is the
image of the reference level `<x>`, and one image name is one package.

The changelog of a published release starts from the previous tag of the same
campaign, never from whatever tag GitHub finds nearest: `previous()` answers it
in semver order (not date). A release looks back through `release/` tags only; a
pre-release looks back through both campaign families; a reference level looks
back through `reference/` tags only. Tags of other levels, of the other
category, and tags outside the grammar are not candidates. With no earlier tag (a campaign's first
release) the answer is none, and the workflow generates no changelog.

`tools/lib/release_tags.py` is a different grammar — the engine's own
`<name>--v<semver>` tags, vendored byte for byte — and is not this one.

## Refusals

Each refusal carries a name, printed first, so a red run says which rule the
tag broke:

    NOT_A_CAMPAIGN_TAG         not `release/<campaign>/v<version>`, `prerelease/...` or `reference/...`
    BAD_CAMPAIGN_ID            the id is not lowercase alphanumerics and inner hyphens
    RESERVED_CAMPAIGN_ID       a campaign id beginning `reference-`, whose image a reference level owns
    BAD_VERSION                the version is not semver without build metadata
    RELEASE_HAS_PRERELEASE     a `release/` tag whose version has a prerelease part
    PRERELEASE_WITHOUT_PRERELEASE  a `prerelease/` tag whose version has none
    REFERENCE_HAS_PRERELEASE   a `reference/` tag whose version has a prerelease part

Stdlib only. CLI exit codes: 0 answered, 1 refused, 2 usage.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass

RELEASE = "release"
PRERELEASE = "prerelease"
REFERENCE = "reference"
FAMILIES = (RELEASE, PRERELEASE, REFERENCE)

CAMPAIGN = "campaign"
CATEGORIES = (CAMPAIGN, REFERENCE)
REFERENCE_IMAGE_PREFIX = "reference-"
REFERENCE_TITLE_PREFIX = "Reference level: "

TAG_RE = re.compile(r"^(" + "|".join(FAMILIES) + r")/([^/]+)/v([^/]+)$")
CAMPAIGN_RE = re.compile(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$")
_NUM = r"(?:0|[1-9][0-9]*)"
_IDENT = r"(?:0|[1-9][0-9]*|[0-9]*[a-zA-Z-][0-9a-zA-Z-]*)"
VERSION_RE = re.compile(r"^" + _NUM + r"\." + _NUM + r"\." + _NUM + r"(-" + _IDENT + r"(?:\." + _IDENT + r")*)?$")


class Refused(ValueError):
    """A tag or coordinate outside the grammar; `code` names the rule it broke."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code


@dataclass(frozen=True)
class Coordinates:
    family: str
    campaign: str
    version: str

    @property
    def tag(self) -> str:
        return f"{self.family}/{self.campaign}/v{self.version}"

    @property
    def prerelease(self) -> bool:
        return self.family == PRERELEASE

    @property
    def category(self) -> str:
        return REFERENCE if self.family == REFERENCE else CAMPAIGN

    @property
    def directory(self) -> str:
        """The level's directory, relative to the repository root."""
        return f"references/{self.campaign}" if self.category == REFERENCE else f"campaigns/{self.campaign}"

    @property
    def prefabs(self) -> str:
        """The prefab directory the level builds with, relative to the repository root."""
        return f"{self.directory}/prefabs" if self.category == REFERENCE else "prefabs"

    def title(self, world_title: str) -> str:
        """The GitHub Release's title, from the level's own `world.json` title."""
        prefix = REFERENCE_TITLE_PREFIX if self.category == REFERENCE else ""
        return f"{prefix}{world_title} v{self.version}"

    def image(self, owner: str) -> str:
        """The GHCR repository the level's delve image lives in."""
        infix = REFERENCE_IMAGE_PREFIX if self.category == REFERENCE else ""
        return f"ghcr.io/{owner.lower()}/delve-{infix}{self.campaign}"

    def image_tags(self, owner: str) -> list[str]:
        """Every tag the image is pushed under: a pre-release never moves `latest`."""
        image = self.image(owner)
        tags = [f"{image}:v{self.version}"]
        if not self.prerelease:
            tags.append(f"{image}:latest")
        return tags


def family_of(version: str) -> str:
    """The family a version belongs to; `Refused` for a version outside semver."""
    m = VERSION_RE.match(version)
    if not m:
        raise Refused(
            "BAD_VERSION",
            f"{version!r} is not a semver `major.minor.patch[-prerelease]` (build metadata "
            f"`+...` is not allowed: `v<version>` is also an OCI image tag, which has no `+`)",
        )
    return PRERELEASE if m.group(1) else RELEASE


def coordinates(family: str, campaign: str, version: str) -> Coordinates:
    """Judge one (family, campaign, version) triple; the only judge of the grammar."""
    if family not in FAMILIES:
        raise Refused("NOT_A_CAMPAIGN_TAG", f"{family!r} is not one of {', '.join(FAMILIES)}")
    if not CAMPAIGN_RE.match(campaign):
        raise Refused(
            "BAD_CAMPAIGN_ID",
            f"campaign id {campaign!r} must be lowercase alphanumerics and inner hyphens "
            f"(it becomes a GHCR repository path segment)",
        )
    if family != REFERENCE and campaign.startswith(REFERENCE_IMAGE_PREFIX):
        raise Refused(
            "RESERVED_CAMPAIGN_ID",
            f"campaign id {campaign!r} begins `{REFERENCE_IMAGE_PREFIX}`, and "
            f"`delve-{campaign}` is the image of the reference level "
            f"{campaign[len(REFERENCE_IMAGE_PREFIX):]!r}: name the campaign otherwise",
        )
    implied = family_of(version)
    if family == RELEASE and implied == PRERELEASE:
        raise Refused(
            "RELEASE_HAS_PRERELEASE",
            f"version {version!r} has a prerelease part, so it is a pre-release: tag it "
            f"`prerelease/{campaign}/v{version}`",
        )
    if family == PRERELEASE and implied == RELEASE:
        raise Refused(
            "PRERELEASE_WITHOUT_PRERELEASE",
            f"version {version!r} has no prerelease part, so it is a release: tag it "
            f"`release/{campaign}/v{version}`, or add a suffix such as `-beta.1`",
        )
    if family == REFERENCE and implied == PRERELEASE:
        raise Refused(
            "REFERENCE_HAS_PRERELEASE",
            f"version {version!r} has a prerelease part, and a reference level has no "
            f"pre-release family: tag it `reference/{campaign}/v<major>.<minor>.<patch>`",
        )
    return Coordinates(family, campaign, version)


def parse(tag: str) -> Coordinates:
    """The coordinates a pushed tag names; `Refused` for anything outside the grammar."""
    m = TAG_RE.match(tag)
    if not m:
        raise Refused(
            "NOT_A_CAMPAIGN_TAG",
            f"tag {tag!r} is not `release/<campaign>/v<version>`, "
            f"`prerelease/<campaign>/v<version>` or `reference/<level>/v<version>`",
        )
    return coordinates(m.group(1), m.group(2), m.group(3))


def for_version(campaign: str, version: str, category: str = CAMPAIGN) -> Coordinates:
    """The coordinates a dry run simulates.

    For a campaign the version decides the family; a reference level has one
    family, so a version with a prerelease part is refused as its tag would be.
    """
    if category not in CATEGORIES:
        raise Refused("NOT_A_CAMPAIGN_TAG", f"category {category!r} is not one of {', '.join(CATEGORIES)}")
    family = REFERENCE if category == REFERENCE else family_of(version)
    return coordinates(family, campaign, version)


def _semver_key(version: str) -> tuple:
    """Sort key implementing semver 2.0 precedence (prerelease < its release)."""
    core, _, pre = version.partition("-")
    nums = tuple(int(x) for x in core.split("."))
    if not pre:
        return (nums, 1, ())
    # numeric identifiers sort below alphanumeric ones, numerically among themselves
    ids = tuple((0, int(i), "") if i.isdigit() else (1, 0, i) for i in pre.split("."))
    return (nums, 0, ids)


def previous(tag: str, existing: list[str]) -> str | None:
    """The tag a changelog for `tag` starts from, or None when it is the campaign's first.

    `existing` is every tag of the repository, in any order; entries outside the
    grammar are ignored. A release is compared against `release/` tags only, a
    pre-release against both campaign families, a reference level against
    `reference/` tags only; the candidate must precede `tag` in semver order, and
    the latest such wins.
    """
    c = parse(tag)
    families = {RELEASE: (RELEASE,), PRERELEASE: (RELEASE, PRERELEASE), REFERENCE: (REFERENCE,)}[c.family]
    mine = _semver_key(c.version)
    best: tuple | None = None
    best_tag: str | None = None
    for t in existing:
        try:
            o = parse(t)
        except Refused:
            continue
        if o.campaign != c.campaign or o.family not in families:
            continue
        key = _semver_key(o.version)
        if key < mine and (best is None or key > best):
            best, best_tag = key, o.tag
    return best_tag


def outputs(c: Coordinates, owner: str) -> list[str]:
    """`key=value` lines for `$GITHUB_OUTPUT`; every value is single-line."""
    return [
        f"family={c.family}",
        f"category={c.category}",
        f"campaign={c.campaign}",
        f"dir={c.directory}",
        f"prefabs={c.prefabs}",
        f"version={c.version}",
        f"tag={c.tag}",
        f"prerelease={'true' if c.prerelease else 'false'}",
        f"image={c.image(owner)}",
        f"image_tags={','.join(c.image_tags(owner))}",
    ]


USAGE = """usage: campaign_tags.py <command> [args]

  parse <tag>                          print "<family> <campaign> <version>", refused (exit 1) outside the grammar
  previous --tag <tag>                 read every repository tag on stdin; print the tag a changelog starts
                                       from (empty line when <tag> is the campaign's first)
  outputs --tag <tag> --owner <owner>  print $GITHUB_OUTPUT lines for a pushed tag
  outputs --campaign <id> --version <semver> --owner <owner> [--category campaign|reference]
                                       the same for a dry run; for a campaign the version decides the family
  title --tag <tag> --world-title <title>
                                       print the GitHub Release's title for a level whose world.json title is <title>
"""


def _flags(rest: list[str]) -> dict[str, str] | None:
    if len(rest) % 2:
        return None
    pairs = dict(zip(rest[::2], rest[1::2]))
    if len(pairs) * 2 != len(rest) or not all(k.startswith("--") for k in pairs):
        return None
    return {k[2:]: v for k, v in pairs.items()}


def main(argv: list[str]) -> int:
    sys.stdout.reconfigure(newline="\n")
    if not argv:
        print(USAGE, file=sys.stderr)
        return 2
    command, rest = argv[0], argv[1:]
    try:
        if command == "parse" and len(rest) == 1:
            c = parse(rest[0])
            print(f"{c.family} {c.campaign} {c.version}")
            return 0
        if command == "previous":
            flags = _flags(rest)
            if flags is None or set(flags) != {"tag"}:
                print(USAGE, file=sys.stderr)
                return 2
            print(previous(flags["tag"], sys.stdin.read().split()) or "")
            return 0
        if command == "outputs":
            flags = _flags(rest)
            if flags is not None and set(flags) == {"tag", "owner"}:
                c = parse(flags["tag"])
            elif flags is not None and set(flags) in ({"campaign", "version", "owner"},
                                                      {"campaign", "version", "owner", "category"}):
                c = for_version(flags["campaign"], flags["version"], flags.get("category", CAMPAIGN))
            else:
                print(USAGE, file=sys.stderr)
                return 2
            print("\n".join(outputs(c, flags["owner"])))
            return 0
        if command == "title":
            flags = _flags(rest)
            if flags is None or set(flags) != {"tag", "world-title"}:
                print(USAGE, file=sys.stderr)
                return 2
            print(parse(flags["tag"]).title(flags["world-title"]))
            return 0
    except Refused as exc:
        print(f"campaign_tags: REFUSED {exc}", file=sys.stderr)
        return 1
    print(USAGE, file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
