r"""Guards for `tools/check-vendored.py`.

The defect it exists to prevent: `tools/check-pins.py` is ONE tool with two
copies, and the copies drifted. They differed by a single constant naming
directories to skip — inert in the repository it was written in, where every name
in it matched zero tracked files, and destructive here, where `campaigns/` IS the
content and the same entry removed 27 tracked files from both pin discovery and
the fetch-verb enumeration.

Nothing was red and nothing could have been. The binding counts were truthful
about what they were handed; the handing was the defect. So the tests below
assert the check fails in the direction the defect actually arrives from, and
that each way it could be vacuous is closed:

- the copy edited here in place (the drift that matters most),
- the copy that still matches its pin while the SOURCE moved upstream, which
  byte-identity alone passes forever,
- a declaration that names nothing to compare, and a run that compares nothing,
- an entry that declares vendored paths with no checkout supplied, which must be
  a red rather than a silent skip,
- a `reviewed` that is missing, so the staleness half cannot be answered.

Both directions throughout: identical copies pass. A checker that only ever
fails proves as little as one that only ever passes.

The last group exercises THIS repository's own registry, so the guard is bound to
the real tree rather than to fixtures alone.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CHECKER = REPO / "tools" / "check-vendored.py"

VENDORED = "tools/check-pins.py"
BODY_V1 = "#!/usr/bin/env python3\nMARKER = 'one'\n"
BODY_V2 = "#!/usr/bin/env python3\nMARKER = 'two'\n"

# `None` is a meaningful value here — it means "omit `reviewed` from the
# registry" — so "caller said nothing" needs a value of its own.
_KEEP = "<unspecified>"


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


def init(repo: Path) -> None:
    repo.mkdir(parents=True, exist_ok=True)
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "t@example.invalid")
    git(repo, "config", "user.name", "t")


def commit(repo: Path, rel: str, body: str, message: str) -> str:
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", message)
    return git(repo, "rev-parse", "HEAD")


def registry(value: str, *, reviewed: str | None, vendors: str | None) -> str:
    """One `track` entry, with the two fields under test made optional."""
    lines = [
        "[[pin]]",
        'id = "admit-ref"',
        f'value = "{value}"',
        'sites = [".github/workflows/audit.yml"]',
        'repo = "example/upstream"',
        'policy = "track"',
        'builds = []',
    ]
    if vendors is not None:
        lines.append(f"vendors = [{vendors}]")
    if reviewed is not None:
        lines.append(f'reviewed = "{reviewed}"')
    lines.append('why = "the tool this repository vendors"')
    return "\n".join(lines) + "\n"


class Fixture(unittest.TestCase):
    """An upstream repo carrying the source, and a local repo vendoring it."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        root = Path(self._tmp.name)
        self.upstream = root / "upstream"
        self.local = root / "local"
        init(self.upstream)
        self.rev1 = commit(self.upstream, VENDORED, BODY_V1, "v1")
        init(self.local)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def lay_local(
        self,
        *,
        body: str | None = BODY_V1,
        value: str | None = None,
        reviewed: str | None = _KEEP,
        vendors: str | None = f'"{VENDORED}"',
        track: bool = True,
    ) -> None:
        (self.local / ".github").mkdir(parents=True, exist_ok=True)
        (self.local / ".github" / "pins.toml").write_text(
            registry(
                value or self.rev1,
                reviewed=(value or self.rev1) if reviewed is _KEEP else reviewed,
                vendors=vendors,
            ),
            encoding="utf-8",
        )
        if body is not None:
            path = self.local / VENDORED
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body, encoding="utf-8")
        git(self.local, "add", "-A")
        if not track and body is not None:
            git(self.local, "rm", "--cached", "-q", VENDORED)

    def run_check(self, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [
                sys.executable,
                str(CHECKER),
                "--root",
                str(self.local),
                *args,
            ],
            capture_output=True,
            text=True,
        )


class AVendoredFileIsTheUpstreamFile(Fixture):
    def test_an_identical_copy_passes_and_states_its_binding(self) -> None:
        self.lay_local()
        r = self.run_check("--checkout", f"admit-ref={self.upstream}")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("check-vendored: ok", r.stdout)
        self.assertIn("1 vendored file(s) compared byte-for-byte", r.stdout)

    def test_the_binding_count_carries_its_denominator(self) -> None:
        """A truthful count over a truncated input is what went wrong before."""
        self.lay_local()
        r = self.run_check("--checkout", f"admit-ref={self.upstream}")
        line = next(
            ln for ln in r.stdout.splitlines() if ln.startswith("-- binding:")
        )
        self.assertIn("tracked file(s) in this repository", line)
        self.assertIn("registry entr(ies) of", line)

    def test_a_copy_edited_here_in_place_is_a_finding(self) -> None:
        """The drift that matters most: one tool quietly becoming two."""
        self.lay_local(body=BODY_V2)
        r = self.run_check("--checkout", f"admit-ref={self.upstream}")
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("has DRIFTED", r.stderr)
        self.assertIn(VENDORED, r.stderr)

    def test_it_compares_contents_and_not_paths(self) -> None:
        """Hashing `shasum` OUTPUT hashes the file paths too.

        The two copies live at the same relative path but under different roots,
        so a digest contaminated by the path would call identical files
        different. This asserts the green case survives differing roots.
        """
        self.lay_local()
        r = self.run_check("--checkout", f"admit-ref={self.upstream}")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotEqual(str(self.local), str(self.upstream))

    def test_a_file_the_source_does_not_have_is_a_finding(self) -> None:
        self.lay_local(vendors='"tools/not-there.py"')
        (self.local / "tools").mkdir(parents=True, exist_ok=True)
        (self.local / "tools" / "not-there.py").write_text("x\n", encoding="utf-8")
        git(self.local, "add", "-A")
        r = self.run_check("--checkout", f"admit-ref={self.upstream}")
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("does not exist at", r.stderr)

    def test_an_untracked_copy_is_a_finding(self) -> None:
        """An untracked copy ships to nobody, so it is not vendored at all."""
        self.lay_local(track=False)
        r = self.run_check("--checkout", f"admit-ref={self.upstream}")
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("is not tracked", r.stderr)


class ByteIdentityAloneIsSatisfiedByNeverLooking(Fixture):
    """The half that expires, and the reason the pin is not enough on its own."""

    def test_a_source_that_moved_after_reviewed_is_a_finding(self) -> None:
        commit(self.upstream, VENDORED, BODY_V2, "v2 upstream")
        self.lay_local(body=BODY_V1, value=self.rev1, reviewed=self.rev1)
        r = self.run_check("--checkout", f"admit-ref={self.upstream}")
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("changed the vendored source(s) upstream", r.stderr)
        # And the byte comparison passed, which is the point of the test.
        self.assertIn("identical to", r.stdout)

    def test_an_untouched_source_passes(self) -> None:
        """Both directions: an unrelated upstream commit is not a finding."""
        commit(self.upstream, "README.md", "unrelated\n", "unrelated")
        self.lay_local(body=BODY_V1, value=self.rev1, reviewed=self.rev1)
        r = self.run_check("--checkout", f"admit-ref={self.upstream}")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_a_missing_reviewed_is_a_finding(self) -> None:
        self.lay_local(reviewed=None)
        r = self.run_check("--checkout", f"admit-ref={self.upstream}")
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("carries no `reviewed`", r.stderr)


class ItCannotPassByComparingNothing(Fixture):
    """The vacuity modes. A green that bound nothing is not a pass."""

    def test_a_registry_declaring_no_vendored_path_is_a_finding(self) -> None:
        self.lay_local(vendors=None)
        r = self.run_check("--checkout", f"admit-ref={self.upstream}")
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("no registry entry declares `vendors`", r.stderr)

    def test_an_empty_vendors_list_is_a_finding(self) -> None:
        self.lay_local(vendors="")
        r = self.run_check("--checkout", f"admit-ref={self.upstream}")
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("no registry entry declares `vendors`", r.stderr)

    def test_a_missing_checkout_is_a_finding_not_a_skip(self) -> None:
        """A drift check that silently skips is the omission it prevents."""
        self.lay_local()
        r = self.run_check()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("no --checkout", r.stderr)

    def test_a_value_naming_no_commit_is_a_finding(self) -> None:
        self.lay_local(value="0" * 40, reviewed=self.rev1)
        r = self.run_check("--checkout", f"admit-ref={self.upstream}")
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("names nothing", r.stderr)


class ThisRepositorysOwnDeclaration(unittest.TestCase):
    """Bound to the real tree, so the guard is not fixtures all the way down."""

    def test_the_registry_declares_the_checker_as_vendored(self) -> None:
        import tomllib

        with (REPO / ".github" / "pins.toml").open("rb") as fh:
            pins = tomllib.load(fh).get("pin", [])
        declared = {v for p in pins for v in p.get("vendors", [])}
        self.assertIn(
            VENDORED,
            declared,
            "the vendored checker is not declared, so nothing holds it to its "
            "source",
        )

    def test_every_declared_path_is_tracked_here(self) -> None:
        import tomllib

        with (REPO / ".github" / "pins.toml").open("rb") as fh:
            pins = tomllib.load(fh).get("pin", [])
        listed = subprocess.run(
            ["git", "-C", str(REPO), "ls-files", "-z"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        tracked = {rel for rel in listed.split("\0") if rel}
        for pin in pins:
            for rel in pin.get("vendors", []):
                self.assertIn(rel, tracked, f"{rel} is declared vendored, untracked")

    def test_the_guard_itself_is_not_vendored(self) -> None:
        """It must not be removable by the act it exists to catch.

        `check-pins.py` ignores registry keys it does not know, so a vendor check
        living inside it would vanish the moment an older copy was vendored —
        which is exactly when the copies have drifted.
        """
        import tomllib

        with (REPO / ".github" / "pins.toml").open("rb") as fh:
            pins = tomllib.load(fh).get("pin", [])
        declared = {v for p in pins for v in p.get("vendors", [])}
        self.assertNotIn("tools/check-vendored.py", declared)


if __name__ == "__main__":
    unittest.main()
