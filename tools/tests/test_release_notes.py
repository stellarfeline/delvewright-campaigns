"""Guards for `tools/release-notes.py`, the one judge of a campaign's release notes.

`release.yml` renders the notes through it on a tag push and `prefab-audit.yml`
runs `check` through it on every pull request. Each refusal it claims is planted
here and the gate is required to red on it; the clean campaign must pass. The
pull-request arm judges only campaigns the change touches, so an untouched
campaign is not judged, and a change touching none states its zero by name.

The fixtures are real git repositories, because `check` diffs against a base.
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SCRIPT = REPO / "tools" / "release-notes.py"

BOOK = """# A Camp

> **Requires delve engine 1.0.0 or newer** — last verified with delvec 1.0.0.

A short walk among the trees.

| | |
|---|---|
| **Players** | 1–4 |
| **Playtime** | {playtime} |
| **Languages** | English |
"""


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, check=True
    ).stdout.strip()


def init(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    git(root, "init", "-q")
    git(root, "config", "user.email", "t@example.invalid")
    git(root, "config", "user.name", "t")
    (root / "README.md").write_text("repo\n", encoding="utf-8")
    commit(root, "base")


def commit(root: Path, msg: str) -> str:
    git(root, "add", "-A")
    git(root, "commit", "-q", "--allow-empty", "-m", msg)
    return git(root, "rev-parse", "HEAD")


def write_camp(root: Path, camp: str, book: str | None, world: bool = True,
               minutes: int = 20) -> None:
    base = root / "campaigns" / camp
    base.mkdir(parents=True, exist_ok=True)
    if world:
        (base / "world.json").write_text(
            json.dumps({"content": {"title": "A Camp", "target_minutes": minutes}}),
            encoding="utf-8",
        )
    else:
        (base / "notes.txt").write_text("media only\n", encoding="utf-8")
    if book is not None:
        (base / "README.md").write_text(book, encoding="utf-8")


def run(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(root), *args],
        capture_output=True,
        text=True,
    )


GOOD = BOOK.format(playtime="~20 minutes")


class ReleaseNotes(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "repo"
        init(self.root)
        self.base = git(self.root, "rev-parse", "HEAD")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def change(self, book: str | None, **kw) -> subprocess.CompletedProcess:
        """Commit `a-camp` as the pull request's change, then check against base."""
        write_camp(self.root, "a-camp", book, **kw)
        commit(self.root, "change")
        return run(self.root, "check", "--base", self.base)

    def assertRefused(self, res: subprocess.CompletedProcess, needle: str) -> None:
        self.assertEqual(res.returncode, 1, res.stdout + res.stderr)
        self.assertIn("REFUSED a-camp", res.stdout)
        self.assertIn(needle, res.stdout)
        self.assertIn("1 refused", res.stdout)

    def test_clean_changed_campaign_passes_and_states_binding(self) -> None:
        res = self.change(GOOD)
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        self.assertIn("1 changed campaign director(ies) judged of 1 on the tree", res.stdout)
        self.assertIn("1 composable, 0 refused", res.stdout)

    def test_playtime_disagreeing_with_target_minutes_reds(self) -> None:
        self.assertRefused(self.change(BOOK.format(playtime="15–30 minutes")),
                           "target_minutes=20")

    def test_no_world_json_reds(self) -> None:
        self.assertRefused(self.change(GOOD, world=False), "has no world.json")

    def test_no_storybook_reds(self) -> None:
        self.assertRefused(self.change(None), "has no README.md")

    def test_missing_header_row_reds(self) -> None:
        self.assertRefused(self.change(GOOD.replace("| **Languages** | English |\n", "")),
                           "no **Languages** row")

    def test_missing_blurb_reds(self) -> None:
        self.assertRefused(self.change(GOOD.replace("A short walk among the trees.\n", "")),
                           "no blurb paragraph")

    def test_untouched_campaign_without_storybook_is_not_judged(self) -> None:
        write_camp(self.root, "old-camp", None)
        self.base = commit(self.root, "an old campaign with no storybook, on the base")
        res = self.change(GOOD)
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        self.assertNotIn("old-camp", res.stdout)
        self.assertIn("1 changed campaign director(ies) judged of 2 on the tree", res.stdout)

    def test_zero_changed_campaigns_states_its_zero(self) -> None:
        write_camp(self.root, "old-camp", None)
        self.base = commit(self.root, "base with a campaign")
        (self.root / "README.md").write_text("changed\n", encoding="utf-8")
        commit(self.root, "a change outside campaigns/")
        res = run(self.root, "check", "--base", self.base)
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        self.assertIn("0 changed campaign director(ies) judged of 1 on the tree", res.stdout)
        self.assertIn("named zero binding", res.stdout)

    def test_no_base_states_its_zero(self) -> None:
        write_camp(self.root, "old-camp", None)
        commit(self.root, "a campaign")
        res = run(self.root, "check", "--base", "")
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        self.assertIn("0 changed campaign director(ies) judged of 1", res.stdout)
        self.assertIn("no pull-request base was given", res.stdout)

    def test_removed_campaign_is_named_not_judged(self) -> None:
        write_camp(self.root, "a-camp", None)
        self.base = commit(self.root, "a campaign")
        git(self.root, "rm", "-r", "-q", "campaigns/a-camp")
        commit(self.root, "remove it")
        res = run(self.root, "check", "--base", self.base)
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        self.assertIn("removed a-camp", res.stdout)

    def test_render_refuses_what_check_refuses(self) -> None:
        write_camp(self.root, "a-camp", BOOK.format(playtime="15–30 minutes"))
        res = run(self.root, "render", "--campaign", "a-camp", "--image", "img",
                  "--version", "1.0.0", "--has-pack", "false", "--prerelease", "false")
        self.assertEqual(res.returncode, 1)
        self.assertIn("target_minutes=20", res.stderr)

    def test_render_prints_the_notes(self) -> None:
        write_camp(self.root, "a-camp", GOOD)
        res = run(self.root, "render", "--campaign", "a-camp", "--image", "img",
                  "--version", "1.0.0", "--has-pack", "true", "--prerelease", "false")
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertTrue(res.stdout.startswith("## A Camp\n\nA short walk among the trees.\n"))
        self.assertIn("For 1–4 players, ~20 minutes.", res.stdout)
        self.assertIn("img:v1.0.0", res.stdout)


if __name__ == "__main__":
    unittest.main()
