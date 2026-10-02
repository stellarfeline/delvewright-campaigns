"""The campaign release tag grammar, stated once, and every decision that hangs off it.

## What it is

A campaign ships from this repository by a tag, in one of two families:

    release/<campaign>/v<major>.<minor>.<patch>                 a release
    prerelease/<campaign>/v<major>.<minor>.<patch>-<prerelease> a pre-release

`.github/workflows/release.yml` fires on both. Its trigger filter can only say
"starts with the family and has a `/v`"; the strict half is this module, which
the workflow's first step runs before anything is built, so a tag the filter
lets through and the grammar refuses stops there with a named refusal.

The family and the version must agree: a `release/` tag carries no prerelease
part, and a `prerelease/` tag must carry one. Build metadata (`+...`) is refused
in both, because `v<version>` becomes an OCI image tag and that charset has no
`+`.

What follows from the family is decided here as well, so the workflow restates
none of it:

- a release is published as the campaign's GitHub Release, and its image is
  pushed as `v<version>` and `latest`;
- a pre-release is published as a GitHub pre-release that is never marked
  latest, and its image is pushed as `v<version>` only.

`tools/lib/release_tags.py` is a different grammar — the engine's own
`<name>--v<semver>` tags, vendored byte for byte — and is not this one.

## Refusals

Each refusal carries a name, printed first, so a red run says which rule the
tag broke:

    NOT_A_CAMPAIGN_TAG         neither `release/<campaign>/v<version>` nor `prerelease/...`
    BAD_CAMPAIGN_ID            the id is not lowercase alphanumerics and inner hyphens
    BAD_VERSION                the version is not semver without build metadata
    RELEASE_HAS_PRERELEASE     a `release/` tag whose version has a prerelease part
    PRERELEASE_WITHOUT_PRERELEASE  a `prerelease/` tag whose version has none

Stdlib only. CLI exit codes: 0 answered, 1 refused, 2 usage.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass

RELEASE = "release"
PRERELEASE = "prerelease"
FAMILIES = (RELEASE, PRERELEASE)

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

    def image(self, owner: str) -> str:
        """The GHCR repository the campaign's delve image lives in."""
        return f"ghcr.io/{owner.lower()}/delve-{self.campaign}"

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
    return Coordinates(family, campaign, version)


def parse(tag: str) -> Coordinates:
    """The coordinates a pushed tag names; `Refused` for anything outside the grammar."""
    m = TAG_RE.match(tag)
    if not m:
        raise Refused(
            "NOT_A_CAMPAIGN_TAG",
            f"tag {tag!r} is neither `release/<campaign>/v<version>` nor "
            f"`prerelease/<campaign>/v<version>`",
        )
    return coordinates(m.group(1), m.group(2), m.group(3))


def for_version(campaign: str, version: str) -> Coordinates:
    """The coordinates a dry run simulates: the version itself decides the family."""
    family = family_of(version)
    return coordinates(family, campaign, version)


def outputs(c: Coordinates, owner: str) -> list[str]:
    """`key=value` lines for `$GITHUB_OUTPUT`; every value is single-line."""
    return [
        f"family={c.family}",
        f"campaign={c.campaign}",
        f"version={c.version}",
        f"tag={c.tag}",
        f"prerelease={'true' if c.prerelease else 'false'}",
        f"image={c.image(owner)}",
        f"image_tags={','.join(c.image_tags(owner))}",
    ]


USAGE = """usage: campaign_tags.py <command> [args]

  parse <tag>                          print "<family> <campaign> <version>", refused (exit 1) outside the grammar
  outputs --tag <tag> --owner <owner>  print $GITHUB_OUTPUT lines for a pushed tag
  outputs --campaign <id> --version <semver> --owner <owner>
                                       the same for a dry run; the version decides the family
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
        if command == "outputs":
            flags = _flags(rest)
            if flags is not None and set(flags) == {"tag", "owner"}:
                c = parse(flags["tag"])
            elif flags is not None and set(flags) == {"campaign", "version", "owner"}:
                c = for_version(flags["campaign"], flags["version"])
            else:
                print(USAGE, file=sys.stderr)
                return 2
            print("\n".join(outputs(c, flags["owner"])))
            return 0
    except Refused as exc:
        print(f"campaign_tags: REFUSED {exc}", file=sys.stderr)
        return 1
    print(USAGE, file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
