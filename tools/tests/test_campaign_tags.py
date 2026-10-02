"""Guards for `tools/lib/campaign_tags.py`, the one judge of a campaign release tag.

`release.yml` hands this module the pushed tag (or a dry run's campaign and
version) and publishes whatever it answers, so every shape it claims to refuse
is planted here and must red with its named code, and every shape it accepts
must yield the family, the pre-release flag and the image tags the workflow
pushes. The CLI is exercised as the workflow runs it, in a subprocess.
"""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "tools" / "lib" / "campaign_tags.py"
sys.path.insert(0, str(SCRIPT.parent))

import campaign_tags as ct  # noqa: E402

OWNER = "StellarFeline"
IMAGE = "ghcr.io/stellarfeline/delve-vesperhold"


class ParseTag(unittest.TestCase):
    def test_release_tag(self) -> None:
        c = ct.parse("release/vesperhold/v1.0.0")
        self.assertEqual((c.family, c.campaign, c.version), ("release", "vesperhold", "1.0.0"))
        self.assertFalse(c.prerelease)
        self.assertEqual(c.tag, "release/vesperhold/v1.0.0")
        self.assertEqual(c.image_tags(OWNER), [f"{IMAGE}:v1.0.0", f"{IMAGE}:latest"])

    def test_prerelease_tag(self) -> None:
        c = ct.parse("prerelease/vesperhold/v1.1.0-beta.1")
        self.assertEqual((c.family, c.campaign, c.version), ("prerelease", "vesperhold", "1.1.0-beta.1"))
        self.assertTrue(c.prerelease)
        self.assertEqual(c.tag, "prerelease/vesperhold/v1.1.0-beta.1")
        self.assertEqual(c.image_tags(OWNER), [f"{IMAGE}:v1.1.0-beta.1"])

    def test_every_published_tag_parses(self) -> None:
        for tag in (
            "release/doune-castle-tour/v1.0.0",
            "release/nobodys-cave-island/v1.1.0",
            "prerelease/vesperhold/v1.0.0-beta.3",
        ):
            with self.subTest(tag=tag):
                self.assertEqual(ct.parse(tag).tag, tag)

    def assertRefused(self, code: str, fn, *args) -> None:
        with self.assertRaises(ct.Refused) as cm:
            fn(*args)
        self.assertEqual(cm.exception.code, code)

    def test_release_tag_with_prerelease_is_refused(self) -> None:
        self.assertRefused("RELEASE_HAS_PRERELEASE", ct.parse, "release/vesperhold/v1.1.0-beta.1")

    def test_prerelease_tag_without_prerelease_is_refused(self) -> None:
        self.assertRefused("PRERELEASE_WITHOUT_PRERELEASE", ct.parse, "prerelease/vesperhold/v1.1.0")

    def test_wrong_prefix_is_refused(self) -> None:
        for tag in (
            "releases/vesperhold/v1.0.0",
            "pre-release/vesperhold/v1.0.0-beta.1",
            "vesperhold/v1.0.0",
            "release/vesperhold/1.0.0",
            "release/vesperhold/extra/v1.0.0",
            "delvec--v1.6.0",
        ):
            with self.subTest(tag=tag):
                self.assertRefused("NOT_A_CAMPAIGN_TAG", ct.parse, tag)

    def test_bad_version_is_refused(self) -> None:
        for tag in (
            "release/vesperhold/v1.0",
            "release/vesperhold/v01.0.0",
            "release/vesperhold/v1.0.0+build.1",
            "prerelease/vesperhold/v1.0.0-beta.1+build.1",
            "prerelease/vesperhold/v1.0.0-01",
            "prerelease/vesperhold/v1.0.0-",
        ):
            with self.subTest(tag=tag):
                self.assertRefused("BAD_VERSION", ct.parse, tag)

    def test_bad_campaign_is_refused(self) -> None:
        for tag in ("release/Vesperhold/v1.0.0", "release/-vesperhold/v1.0.0", "release/vesper_hold/v1.0.0"):
            with self.subTest(tag=tag):
                self.assertRefused("BAD_CAMPAIGN_ID", ct.parse, tag)


class DryRun(unittest.TestCase):
    def test_version_decides_the_family(self) -> None:
        self.assertEqual(ct.for_version("vesperhold", "0.0.0-dryrun").family, "prerelease")
        self.assertEqual(ct.for_version("vesperhold", "1.2.0").family, "release")

    def test_dry_run_refuses_what_a_tag_would(self) -> None:
        with self.assertRaises(ct.Refused) as cm:
            ct.for_version("vesperhold", "1.2.0+meta")
        self.assertEqual(cm.exception.code, "BAD_VERSION")


class Cli(unittest.TestCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)

    def test_outputs_for_a_prerelease_tag(self) -> None:
        r = self.run_cli("outputs", "--tag", "prerelease/vesperhold/v1.1.0-beta.1", "--owner", OWNER)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(
            r.stdout.splitlines(),
            [
                "family=prerelease",
                "campaign=vesperhold",
                "version=1.1.0-beta.1",
                "tag=prerelease/vesperhold/v1.1.0-beta.1",
                "prerelease=true",
                f"image={IMAGE}",
                f"image_tags={IMAGE}:v1.1.0-beta.1",
            ],
        )

    def test_outputs_for_a_release_tag(self) -> None:
        r = self.run_cli("outputs", "--tag", "release/vesperhold/v1.1.0", "--owner", OWNER)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("prerelease=false", r.stdout.splitlines())
        self.assertIn(f"image_tags={IMAGE}:v1.1.0,{IMAGE}:latest", r.stdout.splitlines())

    def test_outputs_for_a_dry_run(self) -> None:
        r = self.run_cli("outputs", "--campaign", "vesperhold", "--version", "0.0.0-dryrun", "--owner", OWNER)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("tag=prerelease/vesperhold/v0.0.0-dryrun", r.stdout.splitlines())

    def test_refusal_exits_1_with_its_name_and_prints_nothing(self) -> None:
        r = self.run_cli("outputs", "--tag", "release/vesperhold/v1.1.0-rc.1", "--owner", OWNER)
        self.assertEqual(r.returncode, 1)
        self.assertEqual(r.stdout, "")
        self.assertIn("REFUSED RELEASE_HAS_PRERELEASE", r.stderr)

    def test_usage_exits_2(self) -> None:
        for args in ((), ("outputs", "--tag", "release/vesperhold/v1.0.0"), ("nope",)):
            with self.subTest(args=args):
                self.assertEqual(self.run_cli(*args).returncode, 2)


# Several campaigns interleaved, pre-releases of both campaigns, a stray tag.
TAGS = [
    "archive/bell-remake-r1-abandoned",
    "release/alpha/v1.0.0",
    "prerelease/alpha/v1.1.0-beta.1",
    "prerelease/beta/v1.0.0-beta.1",
    "release/beta/v0.9.0",
    "release/alpha/v1.1.0",
    "release/alpha/v1.10.0",
    "release/alpha/v1.2.0",
    "prerelease/alpha/v1.1.0-beta.2",
    "prerelease/alpha/v1.1.0-beta.10",
    "release/beta/v1.0.0",
    "release/alpha-two/v5.0.0",
]


class Previous(unittest.TestCase):
    def test_table(self) -> None:
        cases = [
            # stable: previous stable of the same campaign, semver not date or lexical order
            ("release/alpha/v1.1.0", "release/alpha/v1.0.0"),
            ("release/alpha/v1.2.0", "release/alpha/v1.1.0"),
            ("release/alpha/v1.10.0", "release/alpha/v1.2.0"),
            ("release/beta/v1.0.0", "release/beta/v0.9.0"),
            # a stable never looks back at a pre-release, nor at another campaign
            ("release/alpha/v1.0.0", None),
            ("release/beta/v0.9.0", None),
            ("release/alpha-two/v5.0.0", None),
            # pre-release: either family, whatever precedes it in semver order
            ("prerelease/alpha/v1.1.0-beta.1", "release/alpha/v1.0.0"),
            ("prerelease/alpha/v1.1.0-beta.2", "prerelease/alpha/v1.1.0-beta.1"),
            ("prerelease/alpha/v1.1.0-beta.10", "prerelease/alpha/v1.1.0-beta.2"),
            ("prerelease/beta/v1.0.0-beta.1", "release/beta/v0.9.0"),
            # a tag not yet in the list (the one being published) still resolves
            ("prerelease/alpha/v1.1.0-rc.1", "prerelease/alpha/v1.1.0-beta.10"),
            ("release/gamma/v1.0.0", None),
        ]
        for tag, want in cases:
            with self.subTest(tag=tag):
                self.assertEqual(ct.previous(tag, TAGS), want)

    def test_prerelease_precedes_its_release_but_a_release_skips_it(self) -> None:
        tags = ["prerelease/a/v1.0.0-beta.1", "release/a/v1.0.0"]
        self.assertIsNone(ct.previous("release/a/v1.0.0", tags))
        self.assertIsNone(ct.previous("prerelease/a/v1.0.0-beta.1", tags))
        self.assertEqual(ct.previous("prerelease/a/v1.0.0-rc.1", tags), "prerelease/a/v1.0.0-beta.1")

    def test_a_tag_is_never_its_own_predecessor(self) -> None:
        self.assertIsNone(ct.previous("release/alpha/v1.0.0", ["release/alpha/v1.0.0"]))

    def test_cli_reads_tags_on_stdin(self) -> None:
        r = subprocess.run(
            [sys.executable, str(SCRIPT), "previous", "--tag", "release/alpha/v1.2.0"],
            input="\n".join(TAGS), capture_output=True, text=True, check=False,
        )
        self.assertEqual((r.returncode, r.stdout), (0, "release/alpha/v1.1.0\n"))
        r = subprocess.run(
            [sys.executable, str(SCRIPT), "previous", "--tag", "release/gamma/v1.0.0"],
            input="\n".join(TAGS), capture_output=True, text=True, check=False,
        )
        self.assertEqual((r.returncode, r.stdout), (0, "\n"))


if __name__ == "__main__":
    unittest.main()
