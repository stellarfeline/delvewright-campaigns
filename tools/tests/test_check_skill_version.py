"""The skill version-line gate (`tools/check-skill-version.py`).

The drift this pins (ADR-0016 line 3): the `/new-delve` skill declares its own
version and the `delvec` range it drives. Both are hand-typed, and a hand-typed
range nobody reads is the project's recurring failure class — the unbound
declaration that is green because it examined nothing.

Two declarations, two different bindings, and the tests keep them apart:
`requires.delvec` is a COMPATIBILITY window checked by MEMBERSHIP (the engine
must fall inside it), `verified_with` is EVIDENCE checked by EQUALITY (it must
be the engine the authoring pin names). Collapsing them would make the
frontmatter assert, after every engine release, that older engines are
unsupported — untested, and probably false.

WHAT THIS FILE ADDS OVER THE ENGINE'S VERSION OF IT, because the gate moved
repositories and the move is exactly where a check quietly stops checking:

  - the engine is a SECOND REPOSITORY now, so the ways of failing to reach it
    are new and each is a refusal rather than a skip — no `--engine`, a path
    that is not a checkout, a revision the checkout cannot serve, a file the
    engine no longer has, a manifest with no `authoring_ref`. A version gate
    that shrugged at any of these would be green having compared nothing, which
    is the shape the gate exists to refuse;
  - the engine tree is read at a REVISION, never from the working tree. The
    test that pins this puts a DIFFERENT engine in the checkout's working tree
    from the one at the pinned commit and asserts the verdict follows the
    commit. In CI that is not a hypothetical: the audit job's checkout sits at
    `ADMIT_REF` and the authoring revision is fetched beside it;
  - check 6, the idiom-index counts, which arrived with the page. It used to be
    a row in the engine's `check-stated-counts.py` SITES table; a row cannot
    cross a repository boundary, so the claim came here instead of being
    dropped.

`unittest`, not `pytest`: everything under `tools/` here is stdlib-only so that
a creator runs it on their own clone with nothing installed, and a guard that
needed an install the thing it guards does not need would not run there.

The gate is driven over a SYNTHETIC engine (a `Cargo.toml`, a `main.rs`, an
`envelope.rs`, a `grammar.md`) and a synthetic skill page rather than the live
tree, so these keep failing for the right reason as the real page and the real
CLI grow.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import pathlib
import subprocess
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "check-skill-version.py"
STATED_COUNTS = pathlib.Path(__file__).resolve().parents[1] / "check-stated-counts.py"

ENGINE = "1.0.0"

# A miniature `delvec` CLI in the exact clap shape the gate parses out of
# `crates/compiler/src/main.rs`.
MAIN_RS = '''
#[derive(Parser)]
#[command(name = "delvec")]
struct Cli {
    /// Print the version and exit.
    #[arg(long, global = true)]
    version: bool,
    #[arg(long, global = true, default_value = "en")]
    lang: String,
    #[command(subcommand)]
    command: Option<Command>,
}

#[derive(Subcommand)]
enum Command {
    /// Validate.
    Validate {
        campaign_dir: PathBuf,
    },
    /// Schema.
    Schema {
        #[arg(long)]
        stage: String,
    },
    /// The l10n inventory.
    L10nInventory {
        campaign_dir: PathBuf,
    },
    /// Snapshot.
    Snapshot {
        campaign_dir: PathBuf,
        #[arg(long)]
        at: Option<String>,
        #[arg(long, requires = "at")]
        dist: Option<f64>,
        #[arg(long)]
        labels: bool,
    },
    /// The map editor.
    Edit {
        #[command(subcommand)]
        action: EditAction,
    },
}

#[derive(Subcommand)]
enum EditAction {
    /// Apply.
    Apply {
        campaign_dir: PathBuf,
        #[arg(long)]
        batch: Option<PathBuf>,
    },
}
'''

ENVELOPE_RS = """
// A real engine carries this beside the stage names, and the gate reads
// both out of this one file. The fixture carries it for the same reason it
// carries `Stage::name`: a synthetic engine that omits what a real one has
// makes the gate fail for a reason no real tree would produce.
pub const SUPPORTED_DSL_VERSION: &str = "0.19.0";

impl Stage {
    pub fn name(self) -> &'static str {
        match self {
            Stage::World => "world",
            Stage::Npcs => "npcs",
            Stage::SitePlan => "site-plan",
        }
    }
}
"""

# Three numbered rows, so the oracle's answer is `three` and a page saying
# anything else is red. The delimiter row and the blank line above the table
# matter: `mdtable` is what decides where the table starts and stops, and this
# gate deliberately does not own that rule.
GRAMMAR_MD = """# Grammar

## 2c. The idiom index — how the constructs make shapes

Three techniques, one minimal program each:

| # | Technique | Program | Region, seed | What it shows |
|---|---|---|---|---|
| 1 | Repetition | `idiom-repetition` | 3 x 5 x 17, 1 | repeat tiles a pattern |
| 2 | Priority | `idiom-priority` | 13 x 6 x 2, 1 | otherwise is the precedence |
| 3 | Shape | `idiom-shape` | 15 x 9 x 3, 1 | a taper is a recursion |

## 2d. Something else
"""

SKILL_BODY = """
## The envelope

```json
{
  "dsl_version": "0.19.0",
  "campaign_id": "the-weighbridge",
  "stage": "world"
}
```

## The loop

Stages: `world`, `npcs`, and — for a campaign whose map is planned as a whole —
`site-plan`.

1. `delvec schema --stage <n>` — generate against the live schema.
2. `delvec validate <campaign-dir>` — fix by diagnostic code.
3. `delvec l10n-inventory <campaign-dir> --lang <code>` gives the key inventory.
4. `delvec snapshot` (`--at <anchor> --dist`, `--labels`) for visual review.

Read the idiom index first: three techniques with a runnable program each. What
looks impossible is usually one of the three.

The storybook marker names an engine but no subcommand:

```
> **Requires delve engine 0.9.0 or newer** — last verified with delvec <version>.
```
"""

GOOD_FRONTMATTER = f"""name: new-delve
description: Generate a delve.
version: 1.0.0
requires:
  delvec: ">=1.0.0 <2.0.0"
verified_with: {ENGINE}"""


def load_gate():
    spec = importlib.util.spec_from_file_location("check_skill_version", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def write_engine(root: pathlib.Path, version: str = ENGINE) -> pathlib.Path:
    """A synthetic engine tree, in the layout `ENGINE_PATHS` names."""
    cargo = root / "crates" / "compiler" / "Cargo.toml"
    cargo.parent.mkdir(parents=True, exist_ok=True)
    cargo.write_text(
        f'[package]\nname = "delvec"\nversion = "{version}"\n', encoding="utf-8"
    )
    main_rs = root / "crates" / "compiler" / "src" / "main.rs"
    main_rs.parent.mkdir(parents=True, exist_ok=True)
    main_rs.write_text(MAIN_RS, encoding="utf-8")
    envelope = root / "crates" / "dsl" / "src" / "envelope.rs"
    envelope.parent.mkdir(parents=True, exist_ok=True)
    envelope.write_text(ENVELOPE_RS, encoding="utf-8")
    grammar = root / "docs" / "reference" / "grammar.md"
    grammar.parent.mkdir(parents=True, exist_ok=True)
    grammar.write_text(GRAMMAR_MD, encoding="utf-8")
    return root


class GateTest(unittest.TestCase):
    """Each test drives `check()` over its own synthetic engine and page."""

    maxDiff = None

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        self.gate = load_gate()

        self.engine = write_engine(self.root / "engine")
        self.skill = self.root / ".claude" / "skills" / "new-delve" / "SKILL.md"
        self.skill.parent.mkdir(parents=True)
        self.gate.SKILL = self.skill
        self.gate.REPO = self.root
        self.gate.STATED_COUNTS = STATED_COUNTS

    def write_skill(self, frontmatter: str, body: str = SKILL_BODY) -> None:
        self.skill.write_text(f"---\n{frontmatter}\n---\n{body}", encoding="utf-8")

    def run_check(self, rev: str = "b" * 40) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = self.gate.check(self.engine, rev)
        return code, out.getvalue(), err.getvalue()

    # -- the happy path, and what it says it examined ------------------------

    def test_true_declaration_passes_and_states_its_binding(self) -> None:
        self.write_skill(GOOD_FRONTMATTER)
        code, out, err = self.run_check()
        self.assertEqual(code, 0, err)
        self.assertIn("check-skill-version: OK", out)
        self.assertIn(
            "4 distinct subcommand(s) (l10n-inventory, schema, snapshot, validate)", out
        )
        self.assertIn("5 long-flag reference(s)", out)
        self.assertIn("3 of the engine's 3 campaign stage document(s)", out)
        self.assertIn("2 stated idiom-index count(s)", out)

    def test_the_instrument_is_named_by_revision_not_by_description(self) -> None:
        """A frozen measurement names its instrument literally (CLAUDE.md).

        "the pinned engine" in an output line means every recorded figure is
        re-read against a different engine the moment the pin moves, silently.
        """
        self.write_skill(GOOD_FRONTMATTER)
        _, out, _ = self.run_check(rev="a" * 40)
        self.assertIn("a" * 40, out)
        self.assertIn("versions.toml [engine].authoring_ref", out)

    # -- check 2: the window is a MEMBERSHIP claim ---------------------------

    def test_a_patch_engine_bump_inside_the_window_stays_green(self) -> None:
        write_engine(self.engine, version="1.4.2")
        self.write_skill(GOOD_FRONTMATTER.replace(f"verified_with: {ENGINE}", "verified_with: 1.4.2"))
        code, _, err = self.run_check()
        self.assertEqual(code, 0, err)

    def test_window_above_the_engine_is_red(self) -> None:
        self.write_skill(GOOD_FRONTMATTER.replace(">=1.0.0 <2.0.0", ">=2.0.0 <3.0.0"))
        code, _, err = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("is OUTSIDE the declared window", err)

    def test_major_engine_bump_leaves_the_window_behind(self) -> None:
        write_engine(self.engine, version="2.0.0")
        self.write_skill(GOOD_FRONTMATTER.replace(f"verified_with: {ENGINE}", "verified_with: 2.0.0"))
        code, _, err = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("delvec 2.0.0 is OUTSIDE the declared window >=1.0.0 <2.0.0", err)

    def test_ceiling_must_be_the_floors_next_major(self) -> None:
        self.write_skill(GOOD_FRONTMATTER.replace("<2.0.0", "<1.9.0"))
        code, _, err = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("next major", err)

    # -- check 3: `verified_with` is EQUALITY, both directions ---------------

    def test_verified_with_above_the_engine_is_red(self) -> None:
        self.write_skill(GOOD_FRONTMATTER.replace(f"verified_with: {ENGINE}", "verified_with: 1.4.0"))
        code, _, err = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("ABOVE the authoring engine", err)

    def test_verified_with_below_the_engine_is_stale(self) -> None:
        write_engine(self.engine, version="1.4.0")
        self.write_skill(GOOD_FRONTMATTER)
        code, _, err = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("is STALE", err)
        self.assertIn("verified_with: 1.4.0", err)
        self.assertIn("Leave `requires.delvec` alone", err)

    def test_missing_verified_with_is_red(self) -> None:
        self.write_skill(
            "\n".join(
                line
                for line in GOOD_FRONTMATTER.splitlines()
                if not line.startswith("verified_with")
            )
        )
        code, _, err = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("`verified_with:` is missing", err)

    # -- check 4: the CLI surface --------------------------------------------

    def test_subcommand_the_cli_does_not_have_is_red(self) -> None:
        self.write_skill(
            GOOD_FRONTMATTER, SKILL_BODY.replace("delvec validate", "delvec rehearse")
        )
        code, _, err = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("`delvec rehearse`, which the CLI does not have", err)

    def test_flag_the_subcommand_does_not_have_is_red(self) -> None:
        self.write_skill(
            GOOD_FRONTMATTER, SKILL_BODY.replace("--stage <n>", "--stages <n>")
        )
        code, _, err = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("`--stages`", err)

    def test_zero_binding_is_a_failure_not_a_pass(self) -> None:
        self.write_skill(GOOD_FRONTMATTER, "\nStages: `world`, `npcs`, `site-plan`.\n")
        code, _, err = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("extracted 0 delvec subcommand references", err)

    def test_unparseable_cli_is_a_failure_not_a_pass(self) -> None:
        (self.engine / "crates" / "compiler" / "src" / "main.rs").write_text(
            "// the clap shape this gate keys off is gone\n", encoding="utf-8"
        )
        self.write_skill(GOOD_FRONTMATTER)
        code, _, err = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("parsed 0 subcommands", err)

    # -- check 5: the engine's stages ----------------------------------------

    def test_a_stage_the_skill_never_mentions_is_red(self) -> None:
        self.write_skill(GOOD_FRONTMATTER, SKILL_BODY.replace("`site-plan`", "`nothing`"))
        code, _, err = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("`site-plan.json` and the skill never mentions it", err)

    # -- check 6: the idiom-index counts, which arrived with the page --------

    def test_a_stale_idiom_count_on_the_page_is_red(self) -> None:
        """The claim the engine's SITES row used to make, made here instead."""
        self.write_skill(
            GOOD_FRONTMATTER, SKILL_BODY.replace("three techniques", "nine techniques")
        )
        code, _, err = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("claims there are 9", err)
        self.assertIn("has 3", err)

    def test_every_phrasing_binds_not_just_the_first(self) -> None:
        """"usually one of the N" is a second phrasing and states the same number.

        A gate that only read the headline sentence would pass a page whose
        other sentence had drifted — and that second sentence is the one an
        author acts on, because it is the one telling them where to look.
        """
        self.write_skill(
            GOOD_FRONTMATTER,
            SKILL_BODY.replace("usually one of the three", "usually one of the eight"),
        )
        code, _, err = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("claims there are 8", err)

    def test_a_stale_printed_dsl_version_is_refused(self) -> None:
        """The envelope an author COPIES is held to the engine, not trusted.

        Measured on the live page before this check existed: it printed 0.17.0
        against an engine supporting 0.19.0. Nothing downstream said so -- a
        document declaring the older number validates green, because the fences
        are per-feature minimums -- so the author meets it much later, as a
        fence error about a document this page told them how to write.
        """
        self.write_skill(
            GOOD_FRONTMATTER,
            SKILL_BODY.replace('"dsl_version": "0.19.0"', '"dsl_version": "0.17.0"'),
        )
        code, _, err = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("0.17.0", err)
        self.assertIn("0.19.0", err)

    def test_a_page_printing_no_dsl_version_is_a_failure_not_a_pass(self) -> None:
        """The vacuity direction, and it is the one worth testing.

        A page that stopped printing the envelope and a pattern that stopped
        matching are indistinguishable from the outside, and both leave the
        example unchecked. A gate that went GREEN there would reward deleting
        the thing it exists to check.
        """
        self.write_skill(
            GOOD_FRONTMATTER,
            SKILL_BODY.replace('  "dsl_version": "0.19.0",\n', ""),
        )
        code, _, err = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("0 `dsl_version` literals", err)

    def test_an_engine_without_the_constant_is_a_refusal_not_a_skip(self) -> None:
        """A reader whose constant has moved refuses; it does not quietly pass.

        The number is a fact about the engine at the authoring revision. If it
        cannot be read, this check has no authority to compare against and says
        so, rather than skipping and reporting a binding it did not measure.
        """
        self.write_skill(GOOD_FRONTMATTER)
        envelope = self.engine / "crates" / "dsl" / "src" / "envelope.rs"
        envelope.write_text(
            envelope.read_text(encoding="utf-8").replace(
                'pub const SUPPORTED_DSL_VERSION: &str = "0.19.0";', ""
            ),
            encoding="utf-8",
        )
        code, _, err = self.run_check()
        self.assertNotEqual(code, 0)
        self.assertIn("SUPPORTED_DSL_VERSION", err)

    def test_a_page_that_states_no_idiom_count_is_a_failure_not_a_pass(self) -> None:
        body = SKILL_BODY.replace(
            "Read the idiom index first: three techniques with a runnable program "
            "each. What\nlooks impossible is usually one of the three.",
            "Read the idiom index first.",
        )
        self.write_skill(GOOD_FRONTMATTER, body)
        code, _, err = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("states 0 idiom-index counts", err)

    def test_an_unparseable_idiom_index_is_a_failure_not_a_pass(self) -> None:
        """A blank line detaches the rows; `mdtable` is what notices, not this gate."""
        (self.engine / "docs" / "reference" / "grammar.md").write_text(
            GRAMMAR_MD.replace(
                "|---|---|---|---|---|\n", "|---|---|---|---|---|\n\n"
            ),
            encoding="utf-8",
        )
        self.write_skill(GOOD_FRONTMATTER)
        code, _, err = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("idiom index did not parse", err)

    # -- a missing engine file is a refusal, not a skip ----------------------

    def test_an_engine_missing_a_file_this_gate_reads_is_a_refusal(self) -> None:
        (self.engine / "crates" / "dsl" / "src" / "envelope.rs").unlink()
        self.write_skill(GOOD_FRONTMATTER)
        code, _, err = self.run_check()
        self.assertEqual(code, 2)
        self.assertIn("has no crates/dsl/src/envelope.rs", err)


class EngineReachTest(unittest.TestCase):
    """Reaching the second repository — every failure is a refusal by name.

    These are the ways the gate can fail to have an engine at all, which did not
    exist while it lived in the engine's own tree. Each one must be a refusal:
    a version gate that skipped when it could not find its engine would be green
    exactly when it had checked nothing.
    """

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        self.gate = load_gate()

    def git(self, repo: pathlib.Path, *args: str) -> None:
        subprocess.run(
            ["git", "-C", str(repo), *args],
            check=True,
            capture_output=True,
            env={
                "PATH": "/usr/bin:/bin:/usr/local/bin",
                "GIT_AUTHOR_NAME": "t",
                "GIT_AUTHOR_EMAIL": "t@example.invalid",
                "GIT_COMMITTER_NAME": "t",
                "GIT_COMMITTER_EMAIL": "t@example.invalid",
                "HOME": str(self.root),
            },
        )

    def make_engine_repo(self) -> tuple[pathlib.Path, str]:
        """An engine checkout whose WORKING TREE differs from the pinned commit.

        That difference is the whole point: it is CI's actual state (the checkout
        sits at `ADMIT_REF`, the authoring revision is fetched beside it), and a
        gate that read files off disk would judge the page against an engine
        nobody chose and say nothing about it.
        """
        repo = self.root / "engine"
        repo.mkdir()
        self.git(repo, "init", "-q", "-b", "main")
        write_engine(repo, version="1.0.0")
        self.git(repo, "add", "-A")
        self.git(repo, "commit", "-qm", "pinned")
        rev = subprocess.run(
            ["git", "-C", str(repo), "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        # Now move the working tree to a DIFFERENT engine and commit it, so the
        # tip and the pin disagree.
        write_engine(repo, version="9.9.9")
        self.git(repo, "add", "-A")
        self.git(repo, "commit", "-qm", "tip")
        return repo, rev

    def test_the_revision_decides_not_the_working_tree(self) -> None:
        repo, rev = self.make_engine_repo()
        into = self.root / "materialised"
        into.mkdir()
        self.gate.materialise_engine(repo, rev, into)
        cargo = (into / "crates" / "compiler" / "Cargo.toml").read_text()
        self.assertIn('version = "1.0.0"', cargo)
        self.assertNotIn("9.9.9", cargo)

    def test_a_path_that_is_not_a_checkout_is_a_refusal(self) -> None:
        with self.assertRaises(SystemExit) as caught:
            self.gate.materialise_engine(self.root, "b" * 40, self.root)
        self.assertIn("is not a git checkout", str(caught.exception))

    def test_a_revision_the_checkout_cannot_serve_is_a_refusal(self) -> None:
        repo, _ = self.make_engine_repo()
        into = self.root / "m2"
        into.mkdir()
        with self.assertRaises(SystemExit) as caught:
            self.gate.materialise_engine(repo, "b" * 40, into)
        message = str(caught.exception)
        self.assertIn("cannot serve", message)
        self.assertIn("authoring_ref", message)

    def test_a_manifest_without_an_authoring_ref_is_a_refusal(self) -> None:
        manifest = self.root / "versions.toml"
        manifest.write_text('[engine]\nref = "x"\n', encoding="utf-8")
        self.gate.MANIFEST = manifest
        with self.assertRaises(SystemExit) as caught:
            self.gate.authoring_ref()
        self.assertIn("no `[engine].authoring_ref`", str(caught.exception))

    def test_a_moving_reference_in_the_pin_is_a_refusal(self) -> None:
        """A branch or a tag there is the moving instrument the pin replaced."""
        manifest = self.root / "versions.toml"
        manifest.write_text('[engine]\nauthoring_ref = "main"\n', encoding="utf-8")
        self.gate.MANIFEST = manifest
        with self.assertRaises(SystemExit) as caught:
            self.gate.authoring_ref()
        self.assertIn("not a full 40-hex revision", str(caught.exception))

    def test_the_live_manifest_is_a_40_hex_revision(self) -> None:
        """Bound to the real `versions.toml`, so this suite is not all synthetic."""
        self.assertRegex(self.gate.authoring_ref(), r"^[0-9a-f]{40}$")


if __name__ == "__main__":
    unittest.main()
