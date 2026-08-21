"""The campaign gate refuses in every direction it is supposed to.

These run in the `NBT palette audit` job, which is a required status check, so
the gate's own refusals are bound to a merge rather than to a doc line. A gate
nothing invokes is not a gate.

The engine is not needed and is not built: `--delvec` is handed a stub whose exit
status the test chooses, which is what lets a FAILING CAMPAIGN be exercised
without an engine on the machine. The one case a stub cannot produce — a walk
that stops before it reaches every campaign — is exercised by making the walk
itself raise, because that is the real way the state arises and the accounting
that catches it lives in a `finally`.
"""

from __future__ import annotations

import importlib.util
import io
import json
import contextlib
import pathlib
import stat
import sys
import tempfile
import unittest
from unittest import mock

HERE = pathlib.Path(__file__).resolve()
TOOLS = HERE.parent.parent
spec = importlib.util.spec_from_file_location(
    "campaign_build", TOOLS / "campaign-build.py"
)
cb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cb)


WORLD = {"content": {"title": "t", "languages": ["zh-cn"]}}


def make_repo(campaigns, media=(), headless=()):
    """A tree shaped like the content repository, with nothing else in it."""
    root = pathlib.Path(tempfile.mkdtemp())
    (root / "campaigns").mkdir()
    for name in campaigns:
        d = root / "campaigns" / name
        d.mkdir()
        (d / "world.json").write_text(json.dumps(WORLD), encoding="utf-8")
    for name in media:
        d = root / "campaigns" / name
        d.mkdir()
        (d / "cover.png").write_text("not a stage document", encoding="utf-8")
    for name, carries in headless:
        d = root / "campaigns" / name
        d.mkdir()
        for doc in carries:
            (d / doc).write_text("{}", encoding="utf-8")
    return root


def make_stub(root: pathlib.Path, fail_for=()):
    """An engine stub that fails for the campaigns named and succeeds otherwise."""
    path = root / "delvec-stub"
    names = " ".join(f'"{n}"' for n in fail_for)
    path.write_text(
        "#!/usr/bin/env bash\n"
        f"for bad in {names or '""'}; do\n"
        '  for arg in "$@"; do\n'
        '    if [ "$arg" = "campaigns/$bad" ]; then exit 1; fi\n'
        "  done\n"
        "done\n"
        "exit 0\n",
        encoding="utf-8",
    )
    path.chmod(path.stat().st_mode | stat.S_IXUSR)
    return str(path)


def run_gate(root, delvec=None, extra=()):
    """(exit code, everything printed)."""
    argv = ["--root", str(root), "--out", str(root / "out"), *extra]
    if delvec:
        argv += ["--delvec", delvec]
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        code = cb.main(argv)
    return code, buf.getvalue()


class GreenPath(unittest.TestCase):
    def test_every_campaign_built_in_every_declared_language(self):
        root = make_repo(["alpha", "beta"])
        code, out = run_gate(root, make_stub(root))
        self.assertEqual(code, 0, out)
        # The binding count carries its denominator, and the language count is
        # the population times the languages each campaign declares.
        self.assertIn("2 of 2 campaign(s) examined", out)
        self.assertIn("4 language build(s)", out)
        self.assertIn("0 finding(s)", out)

    def test_english_is_built_even_when_only_others_are_declared(self):
        root = make_repo(["alpha"])
        self.assertEqual(cb.languages_of(root, "alpha"), ["en", "zh-cn"])


class AFailingCampaign(unittest.TestCase):
    def test_a_campaign_that_does_not_build_is_a_finding(self):
        root = make_repo(["alpha", "beta"])
        code, out = run_gate(root, make_stub(root, fail_for=["beta"]))
        self.assertEqual(code, 1, out)
        self.assertIn("beta does not build at --lang en", out)

    def test_one_red_campaign_does_not_hide_the_others(self):
        """The walk continues, so the run reports the whole state of the tree."""
        root = make_repo(["alpha", "beta"])
        code, out = run_gate(root, make_stub(root, fail_for=["alpha"]))
        self.assertEqual(code, 1, out)
        self.assertIn("2 of 2 campaign(s) examined", out)
        self.assertNotIn("beta does not", out)


class ACampaignThatNeverRan(unittest.TestCase):
    def test_a_walk_that_stops_early_reds_naming_what_it_never_reached(self):
        """The accounting is REPORTED, not merely computed.

        A `finally` that computes a finding which the propagating exception then
        carries away is a check whose answer nobody reads, and this test is what
        caught exactly that in the first version of the driver.
        """
        root = make_repo(["alpha", "beta", "gamma"])

        def explode(delvec, r, campaign, prefabs, out_dir):
            if campaign == "beta":
                raise RuntimeError("the walk stopped")
            return []

        with mock.patch.object(cb, "build_campaign", explode):
            code, out = run_gate(root, make_stub(root))
        self.assertEqual(code, 1, out)
        self.assertIn("the walk stopped on an unhandled RuntimeError", out)
        self.assertIn("beta, gamma was never examined", out)
        # And it says how much of the tree it actually got through.
        self.assertIn("1 of 3 campaign(s) examined", out)

    def test_the_reconciliation_names_every_campaign_with_no_result(self):
        errors = cb.reconcile(["alpha", "beta", "gamma"], ["alpha"])
        self.assertEqual(len(errors), 1)
        self.assertIn("discovered 3 campaign(s) and produced a result for 1",
                      errors[0])
        self.assertIn("beta, gamma was never examined", errors[0])

    def test_a_result_for_a_campaign_nobody_discovered_is_also_a_finding(self):
        errors = cb.reconcile(["alpha"], ["alpha", "ghost"])
        self.assertEqual(len(errors), 1)
        self.assertIn("ghost", errors[0])

    def test_a_complete_walk_reconciles_clean(self):
        self.assertEqual(cb.reconcile(["alpha", "beta"], ["alpha", "beta"]), [])


class AnEmptyPopulation(unittest.TestCase):
    def test_zero_campaigns_is_a_finding_and_not_a_pass(self):
        root = make_repo([])
        code, out = run_gate(root, make_stub(root))
        self.assertEqual(code, 1, out)
        self.assertIn("A zero binding is a finding", out)
        self.assertIn("0 of 0 campaign(s) examined", out)

    def test_a_tree_with_only_media_directories_is_still_empty(self):
        """Exclusions do not fill a population — they are counted beside it."""
        root = make_repo([], media=["the-drowned-bell"])
        code, out = run_gate(root, make_stub(root))
        self.assertEqual(code, 1, out)
        self.assertIn("A zero binding is a finding", out)
        self.assertIn("1 directory/ies excluded and named", out)


class TheExclusionIsCounted(unittest.TestCase):
    def test_a_media_directory_is_named_and_does_not_red(self):
        root = make_repo(["alpha"], media=["the-drowned-bell"])
        code, out = run_gate(root, make_stub(root))
        self.assertEqual(code, 0, out)
        self.assertIn("the-drowned-bell", out)
        self.assertIn("1 directory/ies excluded and named", out)

    def test_a_campaign_that_lost_its_entry_document_reds(self):
        root = make_repo(
            ["alpha"], headless=[("beta", ["quests.json", "npcs.json"])]
        )
        code, out = run_gate(root, make_stub(root))
        self.assertEqual(code, 1, out)
        self.assertIn("carries quests.json, npcs.json but no world.json", out)

    def test_the_two_kinds_are_told_apart_by_the_object(self):
        """A media directory cannot present the proof the headless one fails on."""
        root = make_repo([], media=["m"], headless=[("h", ["quests.json"])])
        campaigns, media, headless = cb.discover(root)
        self.assertEqual(campaigns, [])
        self.assertEqual([d["dir"] for d in media], ["m"])
        self.assertEqual([d["dir"] for d in headless], ["h"])


class ItRefusesRatherThanPassing(unittest.TestCase):
    def test_a_tree_with_no_campaigns_directory_is_exit_2(self):
        root = pathlib.Path(tempfile.mkdtemp())
        code, out = run_gate(root)
        self.assertEqual(code, 2, out)

    def test_discover_only_needs_no_engine_and_still_refuses_a_zero(self):
        root = make_repo([])
        code, out = run_gate(root, extra=["--discover-only"])
        self.assertEqual(code, 1, out)

    def test_discover_only_never_reports_a_shortfall_as_a_pass(self):
        """It builds nothing, so it must not borrow the verdict's wording.

        Saying `0 of 2 campaign(s) examined` beside an exit 0 is the reading this
        gate refuses everywhere else, arriving through its own summary line.
        """
        root = make_repo(["alpha", "beta"])
        code, out = run_gate(root, extra=["--discover-only"])
        self.assertEqual(code, 0, out)
        self.assertIn("DISCOVERY ONLY", out)
        self.assertIn("2 campaign(s) discovered", out)
        self.assertNotIn("of 2 campaign(s) examined", out)
        self.assertIn("not a verdict on whether it compiles", out)

    def test_building_without_an_engine_refuses_rather_than_reporting_green(self):
        root = make_repo(["alpha"])
        code, out = run_gate(root)
        self.assertEqual(code, 2, out)


class TheWorkflowAgreesWithTheDeclaration(unittest.TestCase):
    """The two halves of the promotion cannot disagree about the name.

    The lockstep checker holds the declaration against the workflow, and this
    holds the workflow against the shape a required context needs: one job, a
    name with no expression in it, no `strategy:`, no job-level `if:`.
    """

    WORKFLOW = TOOLS.parent / ".github/workflows/campaign-build.yml"

    def test_the_context_name_is_fixed_and_declared(self):
        text = self.WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("    name: every campaign builds\n", text)
        manifest = (TOOLS.parent / ".github/required-status-checks.toml").read_text(
            encoding="utf-8"
        )
        self.assertIn('"every campaign builds"', manifest)

    def test_the_job_carries_nothing_that_would_stop_it_reporting(self):
        text = self.WORKFLOW.read_text(encoding="utf-8")
        jobs = text.partition("jobs:\n")[2]
        for disqualifying in ("\n    strategy:", "\n    if:", "\n    needs:"):
            self.assertNotIn(disqualifying, jobs, disqualifying.strip())

    def test_the_trigger_carries_no_path_filter(self):
        text = self.WORKFLOW.read_text(encoding="utf-8")
        trigger = text.partition("\non:\n")[2].partition("\npermissions:")[0]
        self.assertIn("\n  pull_request:\n", trigger)
        for line in trigger.splitlines():
            self.assertNotIn("paths", line.split("#")[0])


if __name__ == "__main__":
    unittest.main()
