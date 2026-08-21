r"""Guards for `tools/check-pins.py`, and for the one narrowing inside it.

The gate keeps `FETCH_SITES` honest by reading every file no site pattern covers
and asking whether it can reach the network. A verb is read in the LANGUAGE of
the file it is found in, because the list holds two kinds. A COMMAND (`docker
run|pull`, `git clone`) is a program invocation and every language can spawn a
process, so it means the same thing everywhere. A DIRECTIVE (`uses: ...@`, a
Dockerfile `FROM`, a Cargo `git =` dependency) is a statement in ONE
configuration language, and in a file that is some other language the identical
characters are prose.

Both halves are asserted, because a narrowing that cannot tell prose from a real
fetch is not a narrowing, it is an exemption. The false positives below are the
shapes this repository actually holds: `demos/*/refusal.txt` and
`demos/*/boundary.txt` are verbatim compiler-diagnostic transcripts, and
`.github/pins.toml` carries multi-line `why` prose — a diagnostic whose all-caps
emphasis wraps onto a line beginning `FROM`, or a reason paragraph that does, was
refused as an unregistered Dockerfile stage. The true positives are what keep the
narrowing a repair: a campaign document is not safe by being JSON (it can carry a
command), a Dockerfile is not safe by sitting under a name no site pattern
reaches, and a file whose kind is unrecognised keeps every verb.

Stdlib only, and `unittest` rather than a framework, for the same reason the
checker itself is stdlib: it has to run on a creator's own clone with nothing
installed.

    python3 -m unittest discover -s tools/tests -t .

Point the guards at an OLDER copy of the checker to show they red there too --
a guard that only reds against the version it was written for is a shape the fix
happens to satisfy rather than a regression guard:

    CHECK_PINS=/path/to/old/check-pins.py python3 -m unittest discover -s tools/tests -t .

Every pin-shaped literal below is ASSEMBLED rather than written out, and every
fixture body keeps its newlines as escapes. This file is a `**/*.py`, so it is
itself a fetch site: a 40-hex string, a `sha256:` digest, an action ref or a
`repository:`/`ref:` pair spelled contiguously here would be discovered as a pin
in this repository and correctly reported as unregistered. Assembling them means
the enumeration needs no exemption for test data, which is the kind of exemption
that later covers a real pin.
"""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CHECKER = Path(os.environ.get("CHECK_PINS", REPO / "tools" / "check-pins.py"))

DIGEST = "sha256:" + "ab12" * 16
ACTION = "example/fetch" + "er@v4"
REV = "0123456789abcdef" * 2 + "01234567"

# One workflow holding one action ref and one image digest: the smallest tree
# that has something for the registry to be complete or incomplete about.
WORKFLOW = (
    "name: audit\njobs:\n  a:\n    steps:\n"
    "      - uses: " + ACTION + "\n"
    "        with:\n          image: " + DIGEST + "\n"
)

COMPLETE = f"""
[[pin]]
id = "fetcher"
value = "{ACTION}"
sites = [".github/workflows/audit.yml"]
policy = "floating"
why = "held at its major tag"

[[pin]]
id = "image"
value = "{DIGEST}"
sites = [".github/workflows/audit.yml"]
policy = "immutable"
why = "third-party bytes"
"""


def run(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(CHECKER), "--root", str(root), *args],
        capture_output=True,
        text=True,
    )


class Fixture(unittest.TestCase):
    """A minimal tracked repo, plus the two ways to add to it."""

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        # The repo is a SUBDIRECTORY of this run's temp dir, never the temp dir
        # itself. One test needs a path outside the examined tree, and if the
        # tree is the temp dir root then "outside" can only mean the system temp
        # directory — a location shared by every concurrent run on the machine.
        # It was, under a fixed filename: two suites running at once raced, one
        # deleted the other's file, and the loser raised FileNotFoundError. That
        # is a deterministic collision on a shared constant, not flakiness.
        # Nesting keeps "outside the tree" and "inside this run" compatible.
        self.tmp = Path(self._tmp.name)
        self.repo = self.tmp / "repo"
        (self.repo / ".github" / "workflows").mkdir(parents=True)
        (self.repo / ".github" / "workflows" / "audit.yml").write_text(
            WORKFLOW, encoding="utf-8"
        )
        subprocess.run(["git", "-C", str(self.repo), "init", "-q"], check=True)
        self.registry(COMPLETE)

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def registry(self, body: str) -> None:
        (self.repo / ".github" / "pins.toml").write_text(body, encoding="utf-8")
        self._track()

    def add(self, rel: str, body: str) -> None:
        """Track one more file, so the fetch-verb enumeration has to read it."""
        path = self.repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")
        self._track()

    def _track(self) -> None:
        subprocess.run(["git", "-C", str(self.repo), "add", "-A"], check=True)

    def assertGreen(self, r: subprocess.CompletedProcess) -> None:
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def assertRedAbout(self, r: subprocess.CompletedProcess, rel: str) -> None:
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn(rel, r.stderr)
        self.assertIn("no FETCH_SITES pattern covers it", r.stderr)


class DirectivesAreProseInAnotherLanguage(Fixture):
    """The false refusals. Each body is a shape this repository really holds."""

    def test_a_dockerfile_directive_wrapped_into_a_transcript_is_prose(self) -> None:
        """The live-reachable one: `demos/*/refusal.txt` is diagnostic text.

        Three such transcripts are committed today. A compiler diagnostic whose
        all-caps emphasis wraps onto a new line beginning `FROM` was read as an
        unregistered Dockerfile stage -- and the remedy this gate prints, add the
        pattern and the pins, has no meaning for a transcript that fetches
        nothing.
        """
        self.add(
            "demos/bell-landing/refusal.txt",
            "The refusal, as the tool prints it.\n\n"
            "$ delvec build --file quests.json -o out/\n"
            "error: the retry loop at `bell/landing` has no declared escape:\n"
            "  NOTHING THIS CAMPAIGN DECLARES SEPARATES THIS RETRY\n"
            "  FROM A SOFT-LOCK -- whether the loop is winnable is a combat\n"
            "  question this compiler refuses to simulate.\n"
            "exit 2\n",
        )
        self.assertGreen(run(self.repo))

    def test_a_workflow_directive_quoted_in_a_transcript_is_prose(self) -> None:
        self.add(
            "demos/bell-landing/hosting.txt",
            "The step a host adds to run this demo in CI:\n\n"
            "      - uses: " + ACTION + "\n"
            "        with:\n          lfs: true\n",
        )
        self.assertGreen(run(self.repo))

    def test_a_dockerfile_directive_in_the_registrys_own_prose_is_prose(self) -> None:
        """`.github/pins.toml` is TOML, is not a fetch site, and is read here.

        Its `why` fields are multi-line paragraphs, which is exactly where a
        wrapped line beginning `FROM` arrives.
        """
        self.registry(
            COMPLETE
            + '\n[[pin]]\nid = "note"\nvalue = "'
            + ACTION.replace("@v4", "@v3")
            + '"\nsites = [".github/workflows/audit.yml"]\n'
            + 'policy = "floating"\nwhy = """\n'
            + "Held at its major tag. The alternative a reader reaches for is to\n"
            + "FROM here on pin it by digest, which trades one silent staleness\n"
            + 'for another.\n"""\n'
        )
        # The extra entry describes a value the workflow does not carry, so the
        # registry-agreement half must be the only thing that speaks.
        r = run(self.repo)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertNotIn("no FETCH_SITES pattern covers it", r.stderr)

    def test_a_cargo_dependency_line_quoted_in_a_transcript_is_prose(self) -> None:
        self.add(
            "demos/bell-landing/building.txt",
            "To build the tool against an unreleased grammar:\n\n"
            '    delvewright-grammar = { git = "https://example.invalid/g" }\n',
        )
        self.assertGreen(run(self.repo))


class CommandsAreReadEverywhere(Fixture):
    """The true positives. A file is not safe by being any particular language."""

    def test_a_campaign_document_that_runs_a_container_is_a_finding(self) -> None:
        self.add(
            "campaigns/bell/world.json",
            '{\n  "id": "bell",\n'
            '  "hooks": ["docker run --rm example.invalid/props:latest"]\n}\n',
        )
        self.assertRedAbout(run(self.repo), "campaigns/bell/world.json")

    def test_a_campaign_document_that_clones_a_repository_is_a_finding(self) -> None:
        self.add(
            "campaigns/bell/quests.json",
            '{\n  "id": "bell",\n'
            '  "setup": ["git clone https://example.invalid/props"]\n}\n',
        )
        self.assertRedAbout(run(self.repo), "campaigns/bell/quests.json")


class DirectivesSurviveInTheirOwnLanguage(Fixture):
    """The half that makes the keying a repair and not an exemption."""

    def test_a_dockerfile_the_site_list_does_not_name_is_a_finding(self) -> None:
        """`**/Dockerfile.*` does not reach `base.dockerfile`, and the suffix does."""
        self.add("build/base.dockerfile", "FROM alpine:3.20\nRUN true\n")
        self.assertRedAbout(run(self.repo), "build/base.dockerfile")

    def test_a_file_of_unrecognised_kind_keeps_every_verb(self) -> None:
        """Fail-closed. The map says which kinds ARE a language, never which are safe.

        This repository has three such files today -- `LICENSE`, `.gitignore`
        and `.gitattributes` -- so the property is load-bearing rather than
        hypothetical: a Dockerfile written under a name nobody anticipated
        cannot change its language to escape the scan.
        """
        self.add("build/image-recipe", "FROM alpine:3.20\nRUN true\n")
        self.assertRedAbout(run(self.repo), "build/image-recipe")

    def test_a_cargo_git_dependency_in_a_toml_is_a_finding(self) -> None:
        self.add(
            "build/tool.toml",
            "[dependencies]\n"
            'delvewright-grammar = { git = "https://example.invalid/g" }\n',
        )
        self.assertRedAbout(run(self.repo), "build/tool.toml")


class TheEnumerationStatesItsOwnBinding(Fixture):
    def test_it_states_what_it_examined(self) -> None:
        """Spelled out rather than recomputed from `FETCH_VERBS`.

        A second copy of the implementation's own arithmetic would agree with it
        however wrong it was. Re-keying a verb moves these numbers, and that is
        the point: the change is meant to be looked at rather than absorbed.
        """
        self.add("campaigns/bell/world.json", '{\n  "id": "bell"\n}\n')
        r = run(self.repo)
        self.assertGreen(r)
        line = next(
            ln
            for ln in r.stdout.splitlines()
            if ln.startswith("-- fetch-verb enumeration")
        )
        applications = int(line.split()[3])
        files = int(line.split("over ")[1].split()[0])
        # Two files are uncovered: the registry and the campaign document (the
        # workflow is a site). `pins.toml` is TOML, so it keeps both commands and
        # the Cargo directive -- three. `world.json` is JSON, which is none of
        # the three directive languages, so it keeps the two commands only.
        self.assertEqual(files, 2, line)
        self.assertEqual(applications, 5, line)

    def test_an_enumeration_that_applies_no_verb_is_a_finding(self) -> None:
        """A zero here is the gate going dark, and the surrounding pins still bind.

        Every tracked file is either a fetch site or prose, so nothing is left
        for the enumeration to read -- the state in which a new kind of fetch
        site would escape unseen. The registry is held outside the tree so that
        it is not itself the one file being examined -- and inside this run's own
        temp dir, so that "outside the tree" is not a path shared with every
        other run on the machine.
        """
        (self.repo / ".github" / "pins.toml").unlink()
        (self.repo / "README.md").write_text("prose\n", encoding="utf-8")
        self._track()
        # Beside the tree, inside this run's temp dir: outside what is examined,
        # and unique per run. See setUp for what a fixed shared path cost.
        registry = self.tmp / "outside-pins.toml"
        registry.write_text(
            f'[[pin]]\nid = "fetcher"\nvalue = "{ACTION}"\n'
            'sites = [".github/workflows/audit.yml"]\n'
            'policy = "floating"\nwhy = "held at its major tag"\n'
            f'\n[[pin]]\nid = "image"\nvalue = "{DIGEST}"\n'
            'sites = [".github/workflows/audit.yml"]\n'
            'policy = "immutable"\nwhy = "third-party bytes"\n',
            encoding="utf-8",
        )
        r = run(self.repo, "--registry", str(registry))
        self.assertIn("binding: 2 pin(s)", r.stdout)
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("applied no verb to any file", r.stderr)


class ThisRepositorysOwnRegistry(unittest.TestCase):
    """Both directions. A checker that only ever passes proves nothing."""

    def test_it_is_complete_and_states_its_counts(self) -> None:
        r = run(REPO)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("-- fetch-verb enumeration:", r.stdout)
        self.assertIn("-- binding:", r.stdout)

    def test_the_enumeration_reads_this_tree_rather_than_nothing(self) -> None:
        """The real tree's own binding: a zero would be the gate going dark."""
        r = run(REPO)
        line = next(
            ln
            for ln in r.stdout.splitlines()
            if ln.startswith("-- fetch-verb enumeration")
        )
        self.assertGreater(int(line.split()[3]), 0, line)
        self.assertGreater(int(line.split("over ")[1].split()[0]), 0, line)

    def test_the_campaign_tree_is_inside_the_gate(self) -> None:
        """Every tracked file is examined, whatever directory it sits in.

        `campaigns/` is this repository's content. The pipeline repository
        reaches this one through a gitignored `campaigns` symlink, so its skip
        list once named that directory — inertly there, since a gitignored path
        is never listed by `git ls-files`. Carried across, the same entry took
        every campaign document out of both pin discovery and the fetch-verb
        enumeration while every count stayed green, because a file that is never
        listed cannot be reported as unexamined.

        Asserted as an EXACT population rather than as the absence of one name
        from one constant. Naming the constant would be vacuous twice over: the
        name can be renamed out from under the test, and `campaigns` not being
        in a list of build-output directories is true whether or not the tracked
        enumeration is filtered at all. Set equality against `git ls-files` is
        the property itself — any skip list reaching this population reds here,
        and the diff names the files it dropped.
        """
        spec = importlib.util.spec_from_file_location("check_pins_pop", CHECKER)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        listed = subprocess.run(
            ["git", "-C", str(REPO), "ls-files", "-z"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        # The function documents two exclusions and no others: it wants real
        # files, so a symlink and a gitlink are out. Everything else is in.
        expected = sorted(
            rel
            for rel in listed.split("\0")
            if rel
            and not (REPO / rel).is_symlink()
            and (REPO / rel).is_file()
        )
        examined = sorted(module.tracked_files(REPO))
        dropped = sorted(set(expected) - set(examined))
        self.assertEqual(
            examined,
            expected,
            f"{len(dropped)} of {len(expected)} tracked file(s) never reached "
            f"the enumeration: {dropped[:10]}",
        )

        campaigns = [rel for rel in examined if rel.startswith("campaigns/")]
        self.assertTrue(campaigns, "no campaign document reached the gate")

    def test_it_reds_when_a_pin_leaves_it(self) -> None:
        """Which entry is read from the registry rather than named here.

        A test that hardcodes today's pins is a second copy of the record, and a
        second copy drifts.
        """
        import tomllib

        source = REPO / ".github" / "pins.toml"
        with source.open("rb") as fh:
            pins = tomllib.load(fh).get("pin", [])
        self.assertTrue(pins, "the registry declares no pins")
        with tempfile.TemporaryDirectory() as tmp:
            thinned = Path(tmp) / "pins.toml"
            body = source.read_text(encoding="utf-8")
            head, _, _ = body.partition("[[pin]]")
            kept = ["[[pin]]" + chunk for chunk in body.split("[[pin]]")[2:]]
            thinned.write_text(head + "\n".join(kept), encoding="utf-8")
            r = run(REPO, "--registry", str(thinned))
        self.assertEqual(r.returncode, 1, r.stdout + r.stderr)
        self.assertIn("unregistered pin", r.stderr)


class TheLanguageMapIsAPositiveClaim(unittest.TestCase):
    """Read directly, because fail-closed is a property of the map's shape."""

    @staticmethod
    def _checker():
        spec = importlib.util.spec_from_file_location("check_pins", CHECKER)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_an_unrecognised_kind_has_no_language(self) -> None:
        language_of = self._checker().language_of
        for rel in ("LICENSE", ".gitignore", ".gitattributes", "build/image-recipe"):
            self.assertIsNone(language_of(rel), rel)

    def test_a_recognised_kind_names_its_language(self) -> None:
        language_of = self._checker().language_of
        self.assertEqual(language_of("campaigns/bell/world.json"), "json")
        self.assertEqual(language_of("demos/bell/refusal.txt"), "text")
        self.assertEqual(language_of(".github/pins.toml"), "toml")
        self.assertEqual(language_of("build/base.dockerfile"), "dockerfile")
        self.assertEqual(language_of("Dockerfile"), "dockerfile")

    def test_every_directive_names_a_language_the_map_can_produce(self) -> None:
        """A directive keyed to a language nothing resolves to is never dropped.

        It would be a verb applied everywhere wearing the keying's clothes --
        green, bound, and doing exactly what the defect did.

        A verb may belong to more than one language, so the keying is a SET of
        them, and the set shape is itself asserted. The checker asks `lang in
        verb_langs`, and `in` over a bare string is SUBSTRING matching: a verb
        keyed to the string "yaml" would silently answer for a language named
        "ya", which is the right question about the wrong key. An empty set is
        refused for the mirror reason -- it drops the verb for every file whose
        language is known, which is the defect this guard exists to catch,
        arriving from the other side.
        """
        checker = self._checker()
        producible = set(checker.LANGUAGE_BY_NAME.values()) | set(
            checker.LANGUAGE_BY_SUFFIX.values()
        )
        keyed = 0
        for verb, languages in checker.FETCH_VERBS:
            if languages is None:
                continue
            keyed += 1
            self.assertIsInstance(languages, (set, frozenset), verb.pattern)
            self.assertTrue(languages, verb.pattern)
            for language in sorted(languages):
                self.assertIn(language, producible, verb.pattern)
        # A binding of zero would pass every assertion above without making one.
        self.assertGreater(keyed, 0, "no directive in FETCH_VERBS is language-keyed")


if __name__ == "__main__":
    unittest.main()
