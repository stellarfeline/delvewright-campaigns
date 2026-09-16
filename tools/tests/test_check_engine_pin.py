r"""Guards for `tools/check-engine-pin.py`, the binder `engine-release` names.

The entry it binds carries a value the pin scan cannot discover — a release tag
has no shape — so `tools/ci/check-pins.py` refuses to let that entry rest on
`sites` alone and demands a binder instead. A binder that passes whatever it is
handed is the UNRUN mode wearing a field's clothes, so each shape it claims to
catch is planted here and the gate is required to red on it.

The four: a storybook claiming a delvec NEWER than the pinned release; a pinned
value that is not a release tag at all; a repository where nothing states a
claim, which is the vacuous shape; and the clean tree, which must pass.

The fixtures are real git repositories, because the checker closes its walk over
git's index rather than a glob — a storybook nobody tracked is one the walk must
not find.

`REV` below is ASSEMBLED rather than written out, for the reason
`test_check_pins.py` states: this file is a `**/*.py` and therefore itself a
fetch site. The release-tag fixtures need no such care — a version string has no
pin shape, which is the whole reason the entry they exercise carries `bound_by`.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CHECKER = REPO / "tools" / "check-engine-pin.py"

MARKER = (
    "> **Requires delve engine 1.0.0 or newer** — last verified with delvec "
    "{version} on Minecraft Java 1.21.11.\n"
)

REV = "0123456789abcdef" * 2 + "01234567"


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, check=True
    ).stdout.strip()


def build(root: Path, ref: str, claims: dict[str, str]) -> None:
    """A repository pinning `ref`, with one storybook per entry of `claims`."""
    root.mkdir(parents=True, exist_ok=True)
    git(root, "init", "-q")
    git(root, "config", "user.email", "t@example.invalid")
    git(root, "config", "user.name", "t")
    (root / "versions.toml").write_text(
        f'[engine]\nrepo = "stellarfeline/delvewright"\nref = "{ref}"\n',
        encoding="utf-8",
    )
    for campaign, version in claims.items():
        book = root / "campaigns" / campaign / "README.md"
        book.parent.mkdir(parents=True, exist_ok=True)
        book.write_text(f"# {campaign}\n\n" + MARKER.format(version=version), encoding="utf-8")
    (root / "campaigns").mkdir(exist_ok=True)
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "fixture")


def run(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(CHECKER), "--root", str(root)],
        capture_output=True,
        text=True,
    )


class EnginePinBinder(unittest.TestCase):
    def test_a_clean_tree_passes_and_states_its_binding(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            build(root, "delvec--v1.6.0", {"alpha": "1.5.0", "beta": "1.1.0"})
            r = run(root)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("check-engine-pin: ok", r.stdout)
            self.assertIn("2 storybook claim(s) judged over 2 storybook(s)", r.stdout)

    def test_a_storybook_newer_than_the_pin_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            build(root, "delvec--v1.6.0", {"alpha": "1.5.0", "beta": "1.7.0"})
            r = run(root)
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("last verified with delvec 1.7.0", r.stderr)
            self.assertIn("campaigns/beta/README.md", r.stderr)
            # The older claim is not swept up with it.
            self.assertNotIn("campaigns/alpha/README.md says", r.stderr)

    def test_an_equal_claim_is_not_a_finding(self) -> None:
        """One-directional, like the engine-side check it mirrors."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            build(root, "delvec--v1.6.0", {"alpha": "1.6.0"})
            r = run(root)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_a_pin_that_is_not_a_release_tag_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            build(root, REV, {"alpha": "1.5.0"})
            r = run(root)
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("is not a release tag", r.stderr)

    def test_a_legacy_v_tag_is_refused(self) -> None:
        """The six pre-grammar tags are published history, never a new pin."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            build(root, "v1.5.0", {"alpha": "1.5.0"})
            r = run(root)
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("is not a release tag", r.stderr)

    def test_a_binding_of_zero_is_a_finding(self) -> None:
        """The vacuous shape: nothing states a claim, so nothing was compared."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            build(root, "delvec--v1.6.0", {})
            r = run(root)
            self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
            self.assertIn("binding of zero", r.stderr)

    def test_an_untracked_storybook_is_not_examined(self) -> None:
        """The walk closes over git's index; a file nobody committed ships to nobody."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            build(root, "delvec--v1.6.0", {"alpha": "1.5.0"})
            rogue = root / "campaigns" / "ghost" / "README.md"
            rogue.parent.mkdir(parents=True, exist_ok=True)
            rogue.write_text(MARKER.format(version="9.9.9"), encoding="utf-8")
            r = run(root)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertNotIn("ghost", r.stdout + r.stderr)

    def test_a_missing_versions_toml_is_unusable_not_a_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "repo"
            build(root, "delvec--v1.6.0", {"alpha": "1.5.0"})
            (root / "versions.toml").unlink()
            r = run(root)
            self.assertEqual(r.returncode, 2, r.stdout + r.stderr)

    def test_the_registry_entry_really_names_this_file_and_its_key(self) -> None:
        """The binding is a fact about the registry, not about this test file."""
        import tomllib

        with (REPO / ".github" / "pins.toml").open("rb") as fh:
            entries = tomllib.load(fh)["pin"]
        bound = [p for p in entries if p.get("bound_by") == "tools/check-engine-pin.py"]
        self.assertEqual(len(bound), 1, "exactly one entry names this binder")
        self.assertEqual(bound[0]["bound_key"], "engine.ref")
        self.assertEqual(bound[0]["id"], "engine-release")


if __name__ == "__main__":
    unittest.main()
