r"""Guards for `tools/check-authoring-pin.py`.

The defect it exists to prevent: the skill page told an author to clone the
engine and named no revision, so the toolchain they authored with was whatever
the default branch happened to be that hour. The repair is a pin in
`versions.toml` and an INDIRECTION on the page — and an indirection is only worth
anything while it is the only copy.

`tools/check-pins.py` cannot reach either half. It discovers pins by scanning
FETCH_SITES, and markdown is deliberately not one, because in every other
repository a revision literal in prose fetches nothing. A skill page is the
exception: it is a procedure a person executes, and it is exactly where a second
copy would be pasted. So the tests below assert the check fails in the direction
the defect actually arrives from, and that each way it could be vacuous is
closed:

- a moving reference in the pin key (a branch, a tag, `HEAD`, a short sha),
  which is the original defect wearing the pin's clothes,
- a second copy of the revision in the skill page, and in any other tracked
  file — the drift pin discovery structurally cannot see,
- a page that never reads the key, which is the pin with no reader at all,
- a run that examined no file, which would be the gate going dark rather than a
  clean tree.

Both directions throughout: a correct tree passes. A checker that only ever
fails proves as little as one that only ever passes.

The last group exercises THIS repository's own tree, so the guard is bound to
the real manifest rather than to fixtures alone.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CHECKER = REPO / "tools" / "check-authoring-pin.py"

MANIFEST = "versions.toml"
SKILL = ".claude/skills/new-delve/SKILL.md"
REGISTRY = ".github/pins.toml"
# Composed rather than written out, so the fixture revisions are not themselves
# 40-hex literals in a `.py` file — `check-pins.py` scans this file as a fetch
# site, and a test constant is not a pin. The same reason `test_check_pins.py`
# builds its own the same way.
REV = "a1b2c3d4e5f60718" * 2 + "293a4b5c"
OTHER_REV = "9876543210fedcba" * 2 + "98765432"

PAGE_READS_THE_PIN = (
    "# /new-delve\n"
    "\n"
    "Read the revision from the manifest:\n"
    "\n"
    "```sh\n"
    'ENGINE_REF="$(python3 -c \'...["engine"]["authoring_ref"]\')"\n'
    "```\n"
)
PAGE_IGNORES_THE_PIN = "# /new-delve\n\nClone the engine and build it.\n"


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()


def manifest(value: str | None, *, key: str = "authoring_ref") -> str:
    lines = ["[engine]", 'repo = "example/engine"']
    if value is not None:
        lines.append(f'{key} = "{value}"')
    return "\n".join(lines) + "\n"


def registry(*values: str, sites: str = f'"{MANIFEST}"') -> str:
    """One `[[pin]]` per value, so duplication and absence are both expressible."""
    out = []
    for i, v in enumerate(values):
        out.append(
            "[[pin]]\n"
            f'id = "engine-authoring-{i}"\n'
            f'value = "{v}"\n'
            f"sites = [{sites}]\n"
            'policy = "track"\n'
            'why = "the engine an author builds with"\n'
        )
    return "\n".join(out)


class Fixture(unittest.TestCase):
    """A repository carrying a manifest and a skill page, and nothing else."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name) / "repo"
        self.root.mkdir(parents=True)
        git(self.root, "init", "-q")
        git(self.root, "config", "user.email", "t@example.invalid")
        git(self.root, "config", "user.name", "t")

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def lay(
        self,
        *,
        value: str | None = REV,
        key: str = "authoring_ref",
        page: str = PAGE_READS_THE_PIN,
        extra: dict[str, str] | None = None,
        pins: str | None = None,
    ) -> None:
        (self.root / MANIFEST).write_text(manifest(value, key=key), encoding="utf-8")
        reg = self.root / REGISTRY
        reg.parent.mkdir(parents=True, exist_ok=True)
        reg.write_text(
            registry(value) if pins is None and value is not None else (pins or ""),
            encoding="utf-8",
        )
        skill = self.root / SKILL
        skill.parent.mkdir(parents=True, exist_ok=True)
        skill.write_text(page, encoding="utf-8")
        for rel, body in (extra or {}).items():
            path = self.root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body, encoding="utf-8")
        git(self.root, "add", "-A")

    def run_check(self) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(CHECKER), "--root", str(self.root)],
            capture_output=True,
            text=True,
        )


class ThePinIsARevision(Fixture):
    def test_a_correct_tree_passes_and_states_its_binding(self) -> None:
        self.lay()
        r = self.run_check()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("check-authoring-pin: ok", r.stdout)
        self.assertIn("-- binding:", r.stdout)

    def test_the_binding_count_carries_its_denominator(self) -> None:
        """A truthful count over a truncated input is the shape that failed."""
        self.lay()
        r = self.run_check()
        line = next(
            ln for ln in r.stdout.splitlines() if ln.startswith("-- second-copy")
        )
        self.assertIn("out of", line)
        self.assertIn("tracked in all", line)

    def test_a_branch_name_in_the_pin_key_is_a_finding(self) -> None:
        """The original defect, wearing the pin's clothes."""
        self.lay(value="main")
        r = self.run_check()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("MOVING reference", r.stderr)

    def test_a_tag_in_the_pin_key_is_a_finding(self) -> None:
        self.lay(value="v1.1.0")
        r = self.run_check()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("not a full 40-hex revision", r.stderr)

    def test_an_unshaped_value_does_not_bury_its_own_finding(self) -> None:
        """A value of `main` matched 35 files here when it was first measured.

        Searching the tree for an ordinary word returns every file containing
        it, and 35 findings that say nothing hide the one that does. The scan is
        not run when there is no revision to scan for; the shape finding stands
        alone, and the run says why the scan was skipped.
        """
        self.lay(value="main", extra={"docs/a.md": "main\n", "docs/b.md": "main\n"})
        r = self.run_check()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("FAIL — 1 finding(s)", r.stderr)
        self.assertIn("second-copy scan: not run", r.stdout)

    def test_a_short_sha_is_a_finding(self) -> None:
        """A short sha is not a name: it is a prefix, and prefixes collide."""
        self.lay(value=REV[:12])
        r = self.run_check()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("not a full 40-hex revision", r.stderr)

    def test_a_missing_key_is_unusable_rather_than_a_pass(self) -> None:
        self.lay(value=None)
        r = self.run_check()
        self.assertEqual(r.returncode, 2, r.stdout)
        self.assertIn("has no `engine.authoring_ref`", r.stderr)


class TheManifestIsTheOnlyCopy(Fixture):
    def test_a_second_copy_in_the_skill_page_is_a_finding(self) -> None:
        """The drift pin discovery structurally cannot see."""
        self.lay(page=PAGE_READS_THE_PIN + f"\nBuild at `{REV}`.\n")
        r = self.run_check()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn(SKILL, r.stderr)
        self.assertIn("single copy", r.stderr)

    def test_a_second_copy_in_any_other_tracked_file_is_a_finding(self) -> None:
        self.lay(extra={"docs/toolchain.md": f"engine {REV}\n"})
        r = self.run_check()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("docs/toolchain.md", r.stderr)

    def test_an_unrelated_revision_elsewhere_is_not_a_finding(self) -> None:
        """The check is about THIS value, not about revisions in general.

        A checker that reds on any 40-hex anywhere would be red forever and
        would teach a reader to wave it through.
        """
        self.lay(extra={"docs/other.md": f"something else at {OTHER_REV}\n"})
        r = self.run_check()
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


class TheAllowedCopyIsTheCheckedCopy(Fixture):
    """The registry is skipped by the scan, so it is held by a demand instead.

    A skip that stopped at "the registry is allowed to carry it" would be the
    escape hatch the defect can supply: a registry gone stale and one
    deliberately unchanged read identically.
    """

    def test_a_registry_naming_a_different_revision_is_a_finding(self) -> None:
        self.lay(pins=registry(OTHER_REV))
        r = self.run_check()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("no entry in", r.stderr)

    def test_two_entries_for_one_revision_are_a_finding(self) -> None:
        """Discovery is keyed by the value; the loser stops being checked."""
        self.lay(pins=registry(REV, REV))
        r = self.run_check()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("2 entries", r.stderr)

    def test_an_entry_naming_another_site_is_a_finding(self) -> None:
        self.lay(pins=registry(REV, sites='"somewhere/else.yml"'))
        r = self.run_check()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("among its sites", r.stderr)

    def test_a_missing_registry_is_a_finding(self) -> None:
        self.lay()
        (self.root / REGISTRY).unlink()
        git(self.root, "add", "-A")
        r = self.run_check()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("nothing registers the authoring pin", r.stderr)


class ThePinHasAReader(Fixture):
    def test_a_page_that_never_names_the_key_is_a_finding(self) -> None:
        """A pin whose only reader is prose is a doc line."""
        self.lay(page=PAGE_IGNORES_THE_PIN)
        r = self.run_check()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("never names `authoring_ref`", r.stderr)

    def test_a_missing_page_is_a_finding(self) -> None:
        self.lay()
        (self.root / SKILL).unlink()
        git(self.root, "add", "-A")
        r = self.run_check()
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertIn("has no reader", r.stderr)


class ThisRepositorysOwnTree(unittest.TestCase):
    """Bound to the real tree, so the guard is not fixtures all the way down."""

    def test_the_real_tree_passes(self) -> None:
        r = subprocess.run(
            [sys.executable, str(CHECKER)], capture_output=True, text=True
        )
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_the_authoring_pin_is_registered_with_its_manifest_as_its_site(
        self,
    ) -> None:
        with (REPO / MANIFEST).open("rb") as fh:
            value = tomllib.load(fh)["engine"]["authoring_ref"]
        with (REPO / ".github" / "pins.toml").open("rb") as fh:
            pins = tomllib.load(fh).get("pin", [])
        entries = [p for p in pins if p.get("value") == value]
        self.assertEqual(
            len(entries),
            1,
            "the authoring revision must carry exactly one registry entry — "
            "unregistered, nothing says on what terms it may move; twice, and "
            "discovery merges them and one stops being checked at all",
        )
        self.assertIn(MANIFEST, entries[0].get("sites", []))

    def test_the_guard_itself_is_not_vendored(self) -> None:
        """It must not be removable by the act it exists to catch.

        `check-pins.py` is a verbatim copy of the engine's, so a rule added to
        it here would be a red on the vendor check rather than a gate. This
        script is this repository's own and nothing holds it to an upstream.
        """
        with (REPO / ".github" / "pins.toml").open("rb") as fh:
            pins = tomllib.load(fh).get("pin", [])
        declared = {v for p in pins for v in p.get("vendors", [])}
        self.assertNotIn("tools/check-authoring-pin.py", declared)

    def test_the_workflow_runs_it(self) -> None:
        """A gate nothing invokes is not a gate."""
        wf = (REPO / ".github" / "workflows" / "prefab-audit.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("tools/check-authoring-pin.py", wf)
        self.assertIn("--checkout engine-authoring=admit-src", wf)


if __name__ == "__main__":
    unittest.main()
