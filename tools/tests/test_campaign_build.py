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
import subprocess
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


def make_repo(campaigns, media=(), headless=(), released=(), outside=()):
    """A tree shaped like the content repository, with nothing else in it.

    `outside` plants stage documents where discovery does not look — the shape a
    campaign authored under `demos/` has.

    `released` names campaigns that get a real `release/<id>/v1.0.0` tag, which
    is the only thing that makes a campaign released. A git repository with no
    remote: `git ls-remote origin` then fails, the cross-check does not run, and
    the driver says so — which is the offline creator's case as well.
    """
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
    for where, carries in outside:
        d = root / where
        d.mkdir(parents=True, exist_ok=True)
        for doc in carries:
            (d / doc).write_text("{}", encoding="utf-8")
    _git(root, "init", "-q", str(root))
    _git(root, "add", "-A", "-f")
    _git(root, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q", "--allow-empty", "-m", "t")
    for name in released:
        _git(root, "tag", f"release/{name}/v1.0.0")
    return root


def _git(root: pathlib.Path, *argv):
    subprocess.run(["git", "-C", str(root), *argv], check=True, capture_output=True)


def make_stub(root: pathlib.Path, fail_for=()):
    """An engine stub that fails for the campaigns named and succeeds otherwise."""
    path = root / "delvec-stub"
    # Built OUTSIDE the f-string. A same-quote nesting inside one
    # (`f"… {x or \'""\'} …"`) is a syntax error before Python 3.12, and this
    # repository's floor is 3.11 — where the whole module then fails to import
    # and its tests are reported as one error rather than run.
    names = " ".join(f'"{n}"' for n in fail_for) or '""'
    path.write_text(
        "#!/usr/bin/env bash\n"
        f"for bad in {names}; do\n"
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
        self.assertIn("2 of 2 eligible campaign(s) examined", out)
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
        self.assertIn("2 of 2 eligible campaign(s) examined", out)
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
        self.assertIn("1 of 3 eligible campaign(s) examined", out)

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
        self.assertIn("0 of 0 eligible campaign(s) examined", out)

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


class AReleasedCampaignIsNotThisGatesBusiness(unittest.TestCase):
    """A `release/<id>/v*` tag is the whole of what makes a campaign released.

    It is verified at that tag by `release.yml` with the engine it pins, and is
    never edited again — so building it here against a moving engine would assert
    a compatibility nobody promises, and the red would name the one campaign that
    cannot be repaired.
    """

    def test_a_tagged_campaign_is_excluded_and_an_untagged_one_is_built(self):
        root = make_repo(["alpha", "beta"], released=["beta"])
        # The stub fails for beta, so a run that built it would be RED. It is not.
        code, out = run_gate(root, make_stub(root, fail_for=["beta"]))
        self.assertEqual(code, 0, out)
        self.assertIn("released, not built here: beta — release/beta/v1.0.0", out)
        self.assertIn("1 released and excluded by tag [beta (release/beta/v1.0.0)]", out)
        self.assertIn("1 of 1 eligible campaign(s) examined", out)
        self.assertNotIn("beta does not", out)

    def test_an_untagged_campaign_is_still_judged(self):
        """The other half: the exclusion excludes exactly what carries a tag."""
        root = make_repo(["alpha", "beta"], released=["beta"])
        code, out = run_gate(root, make_stub(root, fail_for=["alpha"]))
        self.assertEqual(code, 1, out)
        self.assertIn("alpha does not validate", out)

    def test_the_reason_and_the_tag_are_printed_not_just_the_count(self):
        root = make_repo(["beta"], released=["beta"])
        code, out = run_gate(root, make_stub(root))
        self.assertIn("verified at its tag by release.yml", out)
        self.assertIn("release/beta/v1.0.0", out)

    def test_a_tag_of_another_shape_releases_nothing(self):
        root = make_repo(["alpha"])
        _git(root, "tag", "archive/alpha-abandoned")
        _git(root, "tag", "v1.0.0")
        code, out = run_gate(root, make_stub(root, fail_for=["alpha"]))
        self.assertEqual(code, 1, out)
        self.assertIn("release tags examined: 0", out)
        self.assertIn("alpha does not validate", out)

    def test_the_binding_line_carries_discovered_released_and_built(self):
        root = make_repo(["alpha", "beta"], released=["beta"])
        code, out = run_gate(root, make_stub(root))
        line = [l for l in out.splitlines() if l.startswith("campaign build gate:")]
        self.assertEqual(len(line), 1, out)
        self.assertIn("2 campaign(s) discovered", line[0])
        self.assertIn("1 released and excluded by tag", line[0])
        self.assertIn("1 eligible", line[0])
        self.assertIn("1 of 1 eligible campaign(s) examined", line[0])

    def test_everything_released_is_not_a_finding(self):
        """A repository whose every campaign is published has nothing to build,
        and that is the population's shape rather than a failure."""
        root = make_repo(["alpha"], released=["alpha"])
        code, out = run_gate(root, make_stub(root, fail_for=["alpha"]))
        self.assertEqual(code, 0, out)
        self.assertIn("nothing is eligible", out)
        self.assertIn("0 finding(s)", out)

    def test_no_campaign_at_all_is_still_a_finding(self):
        """The distinction the rule above rests on: nothing eligible is a shape,
        nothing discovered is a broken discovery rule."""
        root = make_repo([])
        code, out = run_gate(root, make_stub(root))
        self.assertEqual(code, 1, out)
        self.assertIn("A zero binding is a finding", out)
        self.assertNotIn("nothing is eligible", out)

    def test_a_checkout_short_of_the_remotes_tags_is_a_refusal(self):
        """The silent failure this cross-check exists for: a checkout without
        tags excludes nothing and reads exactly like a repository that has
        published nothing. The remote shares no configuration with it."""
        origin = make_repo(["alpha"], released=["alpha"])
        clone = pathlib.Path(tempfile.mkdtemp()) / "clone"
        subprocess.run(
            ["git", "clone", "-q", "--no-tags", str(origin), str(clone)],
            check=True, capture_output=True,
        )
        code, out = run_gate(clone, make_stub(clone))
        self.assertEqual(code, 2, out)
        self.assertIn("release/alpha/v1.0.0", out)
        self.assertIn("git fetch --tags", out)

    def test_a_checkout_carrying_them_passes_the_cross_check(self):
        origin = make_repo(["alpha", "beta"], released=["beta"])
        clone = pathlib.Path(tempfile.mkdtemp()) / "clone"
        subprocess.run(
            ["git", "clone", "-q", str(origin), str(clone)],
            check=True, capture_output=True,
        )
        code, out = run_gate(clone, make_stub(clone))
        self.assertEqual(code, 0, out)
        self.assertIn("the remote agrees", out)

    def test_an_unreachable_remote_says_so_rather_than_claiming_the_check_ran(self):
        root = make_repo(["alpha"], released=["alpha"])
        code, out = run_gate(root, make_stub(root))
        self.assertIn("the remote cross-check did NOT run", out)


class TheAuthoringEngineIsWhatBuildsThem(unittest.TestCase):
    """The gate's claim: an UNRELEASED campaign compiles with the engine its
    author uses. That is `[engine].authoring_ref`, never the release pin."""

    WORKFLOW = TOOLS.parent / ".github/workflows/campaign-build.yml"

    def test_the_workflow_reads_the_authoring_pin(self):
        text = self.WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("e['authoring_ref']", text)
        self.assertNotIn("e['ref']", text)

    def test_it_writes_no_second_copy_of_the_revision(self):
        """A literal here would be a pin held in two places, which
        `check-authoring-pin.py` refuses by name."""
        import tomllib
        text = self.WORKFLOW.read_text(encoding="utf-8")
        manifest = tomllib.load(
            open(TOOLS.parent / "versions.toml", "rb")
        )["engine"]
        self.assertNotIn(manifest["authoring_ref"], text)
        self.assertNotIn(manifest["ref"], text)

    def test_the_release_tags_are_fetched_before_the_gate_runs(self):
        """Without them the exclusion binds to nothing and the gate builds the
        published campaign after all — the defect wearing the shape of a pass."""
        text = self.WORKFLOW.read_text(encoding="utf-8")
        fetch = text.index("git fetch --tags")
        gate = text.index("python3 tools/campaign-build.py")
        self.assertLess(fetch, gate)

    def test_the_pin_policy_is_untouched_by_this_job(self):
        """`builds` stays empty: the package this job builds is the compiler,
        whose closure is the whole engine, so a watch derived from it would red
        on every upstream commit."""
        import tomllib
        pins = tomllib.load(open(TOOLS.parent / ".github/pins.toml", "rb"))
        entry = next(p for p in pins["pin"] if p["id"] == "engine-authoring")
        self.assertEqual(entry["builds"], [])
        self.assertEqual(entry["policy"], "track")
        self.assertEqual(entry["sites"], ["versions.toml"])


class ACampaignOutsideCampaigns(unittest.TestCase):
    """Discovery reads one directory, so a campaign anywhere else is invisible."""

    def test_a_stage_document_outside_campaigns_reds_naming_the_directory(self):
        root = make_repo(["alpha"], outside=[("demos/toll-road", ["world.json"])])
        code, out = run_gate(root, make_stub(root))
        self.assertEqual(code, 1, out)
        self.assertIn("demos/toll-road carries world.json", out)
        self.assertIn("campaigns/<id>/", out)

    def test_a_demo_that_is_not_a_campaign_does_not_red(self):
        """The three demos this repository holds are exactly this shape."""
        root = make_repo(["alpha"], outside=[("demos/mill-race", ["mill-race.json"])])
        code, out = run_gate(root, make_stub(root))
        self.assertEqual(code, 0, out)
        self.assertIn("0 stage document site(s) outside campaigns/", out)

    def test_the_scan_states_its_denominator(self):
        root = make_repo(["alpha"])
        code, out = run_gate(root, make_stub(root))
        self.assertEqual(code, 0, out)
        self.assertIn("tracked file(s)", out)

    def test_every_stage_document_is_watched_not_just_the_entry_one(self):
        """`world.json` is what discovery keys on; a lost entry document is the
        shape that would otherwise slip past the scan as well."""
        root = make_repo(["alpha"], outside=[("demos/x", ["quests.json"])])
        code, out = run_gate(root, make_stub(root))
        self.assertEqual(code, 1, out)
        self.assertIn("demos/x carries quests.json", out)

    def test_an_untracked_tree_refuses_rather_than_scanning_nothing(self):
        root = make_repo(["alpha"])
        for path in sorted(
            (root / ".git").rglob("*"), key=lambda p: len(p.parts), reverse=True
        ):
            path.unlink() if path.is_file() or path.is_symlink() else path.rmdir()
        (root / ".git").rmdir()
        code, out = run_gate(root, make_stub(root))
        self.assertEqual(code, 2, out)
        self.assertIn("ls-files", out)


class AnInProgressCampaignIsNotABuildFailure(unittest.TestCase):
    """The branch is what tells a campaign on `main` from one still being made."""

    def test_the_named_campaign_is_reported_and_not_counted(self):
        root = make_repo(["alpha", "beta"])
        code, out = run_gate(
            root,
            make_stub(root, fail_for=["alpha"]),
            extra=["--branch", "campaign/alpha"],
        )
        self.assertEqual(code, 0, out)
        self.assertIn("in progress on campaign/alpha: alpha", out)
        self.assertIn("not counted: alpha does not validate", out)
        self.assertIn("0 finding(s)", out)

    def test_it_excuses_that_campaign_and_no_other(self):
        root = make_repo(["alpha", "beta"])
        code, out = run_gate(
            root,
            make_stub(root, fail_for=["alpha", "beta"]),
            extra=["--branch", "campaign/alpha"],
        )
        self.assertEqual(code, 1, out)
        self.assertIn("beta does not validate", out)
        self.assertNotIn("error: alpha does not validate", out)

    def test_without_a_branch_nothing_is_excused(self):
        root = make_repo(["alpha"])
        code, out = run_gate(root, make_stub(root, fail_for=["alpha"]))
        self.assertEqual(code, 1, out)
        self.assertIn("no campaign excused", out)

    def test_a_branch_that_is_not_a_campaign_branch_excuses_nothing(self):
        root = make_repo(["alpha"])
        code, out = run_gate(
            root, make_stub(root, fail_for=["alpha"]), extra=["--branch", "main"]
        )
        self.assertEqual(code, 1, out)
        self.assertIn("no campaign excused", out)

    def test_a_branch_naming_a_campaign_the_tree_lacks_is_a_refusal(self):
        """The property the defect cannot supply: the excuse must name a campaign
        the walk also discovered, so `campaign/anything` is not a free pass."""
        root = make_repo(["alpha"])
        code, out = run_gate(
            root,
            make_stub(root, fail_for=["alpha"]),
            extra=["--branch", "campaign/ghost"],
        )
        self.assertEqual(code, 2, out)
        self.assertIn("does not carry", out)

    def test_an_excused_campaign_that_builds_clean_says_so(self):
        root = make_repo(["alpha"])
        code, out = run_gate(
            root, make_stub(root), extra=["--branch", "campaign/alpha"]
        )
        self.assertEqual(code, 0, out)
        self.assertIn("already builds clean", out)

    def test_an_excused_campaign_is_still_reconciled(self):
        """Excused from COUNTING, never from being accounted for."""
        root = make_repo(["alpha"])
        code, out = run_gate(
            root, make_stub(root), extra=["--branch", "campaign/alpha"]
        )
        self.assertIn("1 of 1 eligible campaign(s) examined", out)


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
