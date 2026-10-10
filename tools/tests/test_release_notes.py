"""Guards for `tools/release-notes.py`, the one judge of a campaign's release notes.

`release.yml` renders the notes through it on a tag push and `prefab-audit.yml`
runs `check` through it on every pull request. Each refusal it claims is planted
here and the gate is required to red on it; the clean campaign must pass, and a
tree with no campaign directory is the vacuous shape and must red too.

The fixtures are real git repositories, because `check` walks git's index.
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


def git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], capture_output=True, check=True)


def build(root: Path, book: str | None, world: bool = True, minutes: int = 20) -> None:
    root.mkdir(parents=True, exist_ok=True)
    git(root, "init", "-q")
    camp = root / "campaigns" / "a-camp"
    camp.mkdir(parents=True)
    if world:
        (camp / "world.json").write_text(
            json.dumps({"content": {"title": "A Camp", "target_minutes": minutes}}),
            encoding="utf-8",
        )
    else:
        (camp / "notes.txt").write_text("media only\n", encoding="utf-8")
    if book is not None:
        (camp / "README.md").write_text(book, encoding="utf-8")
    git(root, "add", "-A")


def run(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(root), *args],
        capture_output=True,
        text=True,
    )


class ReleaseNotes(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "repo"

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def assertRefused(self, needle: str) -> None:
        res = run(self.root, "check")
        self.assertEqual(res.returncode, 1, res.stdout + res.stderr)
        self.assertIn("REFUSED a-camp", res.stdout)
        self.assertIn(needle, res.stdout)
        self.assertIn("1 refused", res.stdout)

    def test_clean_campaign_passes_and_states_binding(self) -> None:
        build(self.root, BOOK.format(playtime="~20 minutes"))
        res = run(self.root, "check")
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
        self.assertIn("1 campaign director(ies) judged of 1", res.stdout)

    def test_playtime_disagreeing_with_target_minutes_reds(self) -> None:
        build(self.root, BOOK.format(playtime="15–30 minutes"))
        self.assertRefused("target_minutes=20")

    def test_no_world_json_reds(self) -> None:
        build(self.root, BOOK.format(playtime="~20 minutes"), world=False)
        self.assertRefused("has no world.json")

    def test_no_storybook_reds(self) -> None:
        build(self.root, None)
        self.assertRefused("has no README.md")

    def test_missing_header_row_reds(self) -> None:
        build(self.root, BOOK.format(playtime="~20 minutes").replace("| **Languages** | English |\n", ""))
        self.assertRefused("no **Languages** row")

    def test_missing_blurb_reds(self) -> None:
        build(self.root, BOOK.format(playtime="~20 minutes").replace("A short walk among the trees.\n", ""))
        self.assertRefused("no blurb paragraph")

    def test_no_campaign_directory_is_a_finding(self) -> None:
        self.root.mkdir(parents=True)
        git(self.root, "init", "-q")
        res = run(self.root, "check")
        self.assertEqual(res.returncode, 1, res.stdout + res.stderr)
        self.assertIn("zero campaign directories bound", res.stdout)

    def test_render_refuses_what_check_refuses(self) -> None:
        build(self.root, BOOK.format(playtime="15–30 minutes"))
        res = run(self.root, "render", "--campaign", "a-camp", "--image", "img",
                  "--version", "1.0.0", "--has-pack", "false", "--prerelease", "false")
        self.assertEqual(res.returncode, 1)
        self.assertIn("target_minutes=20", res.stderr)

    def test_render_prints_the_notes(self) -> None:
        build(self.root, BOOK.format(playtime="~20 minutes"))
        res = run(self.root, "render", "--campaign", "a-camp", "--image", "img",
                  "--version", "1.0.0", "--has-pack", "true", "--prerelease", "false")
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertTrue(res.stdout.startswith("## A Camp\n\nA short walk among the trees.\n"))
        self.assertIn("For 1–4 players, ~20 minutes.", res.stdout)
        self.assertIn("img:v1.0.0", res.stdout)


if __name__ == "__main__":
    unittest.main()
