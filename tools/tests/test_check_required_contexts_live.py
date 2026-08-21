"""One file cannot be aspiration to one arm and fact to the arm beside it.

The deadlock arm — "branch X is covered by ruleset R, which requires C, and the
branch does not carry W … EVERY pull request into it is blocked forever" — used
to read `contexts` and `include` out of `.github/required-status-checks.toml`.
It never consulted live protection. The arm immediately beside it compares that
same file AGAINST live protection and correctly reports "declared and NOT
required live — the file claims a gate that does not gate".

So a single run held one context to be unrequired and to be blocking every pull
request forever. Both cannot be true, and the deadlock arm was the false one: a
context written down and not yet granted blocks nothing, because nothing
requires it.

It was not cosmetic. It made a promotion UNREPRESENTABLE. This repository
prescribes merge-then-protect precisely because granting first names a context
the base cannot report, and a pull request that carries a workflow AND its
declaration is exactly the state that order requires it to pass through — so
such a pull request was red by construction, for being correct.

WHICH ARM OWNS WHICH FAILURE, after the repair. Stated here because two arms
that both go quiet is how a promotion gets left half-done:

  declared, not granted     ARM D  ("declared and NOT required live"). Arm E is
                                   silent: nothing requires it, so nothing is
                                   blocked.
  granted, not declared     ARM D  ("required live and NOT declared") AND ARM E,
                                   which now judges it like any other live
                                   context — it could not see one at all before.
  granted, unreportable     ARM E  (the deadlock). This is the whole reason the
                                   arm exists and this repository has sprung it.
  granted, and nothing can  ARM D reds; ARM E states in a note that it could not
    say which workflow             judge it, rather than passing over in silence.
    produces it

Arm E's other half is judged the way arm B already judges its own: for the ref
BEING JUDGED, "can report" is answered from the tree in hand, because on a pull
request that tree is head-merged-into-base and is what will be on the ref after
the merge. Reading the API there reds the pull request that would FIX a
deadlock — the exact shape in the arm's own message. Every other covered ref is
still read from the API, which is the point of the arm.

These tests drive the REAL arm over a REAL directory. Only the three network
functions are replaced, because the live protection states being demonstrated
must not exist on the real repository — a granted-but-unreportable context would
block every pull request into `main` for as long as the test ran.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

TOOLS = Path(__file__).resolve().parent.parent
CHECKER = TOOLS / "check-required-contexts.py"

WF = ".github/workflows"


def manifest(contexts: list[str], provided: dict[str, str],
             include: list[str]) -> str:
    """A declaration. `include` matches the live ruleset in every fixture here
    unless the test is about a mismatch, so that a red is unambiguously the
    thing under test rather than arm D objecting to the fixture."""
    ctx = "".join(f'  "{c}",\n' for c in contexts)
    prov = "".join(f'"{c}" = "{p}"\n' for c, p in provided.items())
    inc = ", ".join(f'"{i}"' for i in include)
    return (
        'default_branch = "main"\n'
        "max_advisory = 0\n\n"
        "[[ruleset]]\n"
        'name = "protect-main"\n'
        f"include = [{inc}]\n"
        f"contexts = [\n{ctx}]\n\n"
        "[ruleset.provided_by]\n"
        f"{prov}"
    )


def workflow(job_name: str) -> str:
    return (
        f"name: {job_name}\n"
        "on:\n"
        "  pull_request:\n"
        "jobs:\n"
        "  j:\n"
        f"    name: {job_name}\n"
        "    runs-on: ubuntu-latest\n"
        "    steps:\n"
        "      - run: echo hi\n"
    )


def live(include: list[str], contexts: list[str], name: str = "protect-main") -> dict:
    return {
        "default_branch": "main",
        "rulesets": {
            name: {
                "id": 1,
                "enforcement": "active",
                "include": include,
                "contexts": sorted(contexts),
                "strict": True,
            }
        },
    }


class LiveArms(unittest.TestCase):
    """Load a fresh copy of the checker inside a fixture tree and run `main()`.

    The script derives `REPO` from its own `__file__.parent.parent`, so a copy
    under `<tmp>/tools/` judges `<tmp>` with nothing patched. Only `read_live`,
    `list_branches` and `workflows_on_ref` — the network boundary — are
    replaced. Both streams are captured and `main()`'s return value IS the exit
    status, taken directly rather than read back through a pipe.
    """

    DEADLOCK = "blocked forever"
    NOT_LIVE = "declared and NOT required live"
    NOT_DECLARED = "required live and NOT declared"

    def build(self, files: dict[str, str]):
        td = tempfile.TemporaryDirectory()
        self.addCleanup(td.cleanup)
        # `.resolve()`, because the checker resolves its own path and on macOS a
        # temp dir handed out as /var resolves to /private/var.
        root = (Path(td.name) / "repo").resolve()
        (root / "tools").mkdir(parents=True)
        (root / WF).mkdir(parents=True)
        shutil.copy2(CHECKER, root / "tools" / "check-required-contexts.py")
        for rel, text in files.items():
            p = root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding="utf-8")
        spec = importlib.util.spec_from_file_location(
            f"crc_live_{id(td)}", root / "tools" / "check-required-contexts.py"
        )
        assert spec and spec.loader
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        self.assertEqual(mod.REPO, root, "the fixture is not the repository it judges")
        return mod

    def tree(self, declared: list[str], provided: dict[str, str],
             include: list[str], jobs: list[str]):
        files = {
            ".github/required-status-checks.toml": manifest(declared, provided, include),
        }
        for name, path in provided.items():
            if name in jobs:
                files[path] = workflow(name)
        for name in jobs:
            if name not in provided:
                files[f"{WF}/{name.replace(' ', '-')}.yml"] = workflow(name)
        return self.build(files)

    def run_checker(self, mod, observed, branches, on_ref) -> tuple[int, str]:
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.object(mod, "read_live", lambda t: (observed, None)), \
             mock.patch.object(mod, "list_branches", lambda t: branches), \
             mock.patch.object(mod, "workflows_on_ref", lambda r, t: on_ref.get(r)), \
             mock.patch.object(sys, "argv",
                               ["check-required-contexts.py", "--ref", "main"]), \
             contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = mod.main()
        merged = out.getvalue() + err.getvalue()
        self.assertIn(
            "check-required-contexts:", merged,
            "the run produced no verdict at all; this row measured nothing",
        )
        return rc, merged

    def assert_deadlock(self, out: str, ctx: str, branch: str):
        self.assertIn(self.DEADLOCK, out)
        self.assertIn(f"branch {branch!r} is covered", out)
        self.assertIn(repr(ctx), out)

    def assert_no_deadlock(self, out: str):
        self.assertNotIn(self.DEADLOCK, out)

    def assert_fixture_not_confounded(self, out: str):
        """The declared and live `include` agree in these fixtures, so arm D
        must never be objecting to the fixture itself."""
        self.assertNotIn("live and [", out)


# ---------------------------------------------------------------------------
# 1. It must STILL catch the real deadlock. This repository has sprung it.
# ---------------------------------------------------------------------------


class TheRealDeadlockIsStillCaught(LiveArms):
    # `~ALL` rather than a campaign-only pattern, so that `main` — the ref
    # these fixtures judge — resolves a required context. A ruleset covering
    # only campaign branches would red arm B for resolving nothing on `main`,
    # and confound every row here with a finding that is not the subject.
    CAMPAIGNS = ["~ALL"]

    def test_a_live_context_no_covered_branch_can_report_is_a_finding(self):
        mod = self.tree(["gate"], {"gate": f"{WF}/gate.yml"}, self.CAMPAIGNS, ["gate"])
        rc, out = self.run_checker(
            mod,
            live(self.CAMPAIGNS, ["gate"]),
            ["main", "campaign/a", "campaign/b"],
            {"campaign/a": set(), "campaign/b": {f"{WF}/other.yml"}},
        )
        self.assertEqual(rc, 1, out)
        self.assert_fixture_not_confounded(out)
        self.assert_deadlock(out, "gate", "campaign/a")
        self.assert_deadlock(out, "gate", "campaign/b")

    def test_a_covered_branch_that_carries_the_workflow_is_not_a_finding(self):
        mod = self.tree(["gate"], {"gate": f"{WF}/gate.yml"}, self.CAMPAIGNS, ["gate"])
        rc, out = self.run_checker(
            mod,
            live(self.CAMPAIGNS, ["gate"]),
            ["main", "campaign/a"],
            {"campaign/a": {f"{WF}/gate.yml"}},
        )
        self.assertEqual(rc, 0, out)
        self.assert_no_deadlock(out)

    def test_a_ref_with_no_workflow_directory_at_all_is_a_finding(self):
        """`workflows_on_ref` returns None for a ref with no `.github/workflows`,
        which is the emptiest possible answer and must not read as a pass."""
        mod = self.tree(["gate"], {"gate": f"{WF}/gate.yml"}, self.CAMPAIGNS, ["gate"])
        rc, out = self.run_checker(
            mod,
            live(self.CAMPAIGNS, ["gate"]),
            ["main", "campaign/bare"],
            {},                       # -> None for every ref
        )
        self.assertEqual(rc, 1, out)
        self.assert_deadlock(out, "gate", "campaign/bare")


# ---------------------------------------------------------------------------
# 2. THE REPAIR: a declaration is not protection, so it deadlocks nothing.
# ---------------------------------------------------------------------------


class ADeclarationBlocksNothing(LiveArms):
    """A promotion in flight: the workflow and its declaration arrive together
    and the context is not granted yet. That is the state merge-then-protect
    requires a pull request to pass through."""

    def promotion_in_flight(self):
        mod = self.tree(
            ["gate", "newly declared"],
            {"gate": f"{WF}/gate.yml", "newly declared": f"{WF}/new.yml"},
            ["~DEFAULT_BRANCH"],
            ["gate", "newly declared"],
        )
        return self.run_checker(
            mod,
            live(["~DEFAULT_BRANCH"], ["gate"]),   # only the old one is granted
            ["main"],
            {"main": {f"{WF}/gate.yml"}},          # `main` has not merged it yet
        )

    def test_arm_e_is_silent_about_a_context_nothing_requires(self):
        _, out = self.promotion_in_flight()
        self.assert_no_deadlock(out)

    def test_arm_d_still_fires_so_the_promotion_cannot_be_left_half_done(self):
        """Point three. If BOTH arms went quiet a declaration that is never
        granted would sail through, and nothing here would ever notice."""
        rc, out = self.promotion_in_flight()
        self.assertEqual(rc, 1, out)
        self.assertIn(self.NOT_LIVE, out)
        self.assertIn("newly declared", out)
        self.assertIn("the file claims a gate that does not gate", out)

    def test_exactly_one_arm_speaks_and_the_two_do_not_contradict(self):
        _, out = self.promotion_in_flight()
        self.assertEqual(out.count(self.NOT_LIVE), 1)
        self.assertEqual(out.count(self.DEADLOCK), 0)


# ---------------------------------------------------------------------------
# 3. A context required LIVE that the declaration does not mention.
#    Iterating declarations made this invisible to arm E. It is not now.
# ---------------------------------------------------------------------------


class AGrantedButUnwrittenContext(LiveArms):
    # `~ALL` rather than a campaign-only pattern, so that `main` — the ref
    # these fixtures judge — resolves a required context. A ruleset covering
    # only campaign branches would red arm B for resolving nothing on `main`,
    # and confound every row here with a finding that is not the subject.
    CAMPAIGNS = ["~ALL"]

    def test_it_is_judged_through_this_tree_when_the_declaration_is_silent(self):
        mod = self.tree(
            ["gate"], {"gate": f"{WF}/gate.yml"}, self.CAMPAIGNS,
            ["gate", "surprise"],          # `surprise` is a job here, undeclared
        )
        rc, out = self.run_checker(
            mod,
            live(self.CAMPAIGNS, ["gate", "surprise"]),
            ["main", "campaign/a"],
            {"campaign/a": {f"{WF}/gate.yml"}},
        )
        self.assertEqual(rc, 1, out)
        # Arm D owns "nobody wrote it down"…
        self.assertIn(self.NOT_DECLARED, out)
        # …and arm E now owns "and a ref it covers cannot report it".
        self.assert_deadlock(out, "surprise", "campaign/a")

    def test_an_unresolvable_live_context_is_stated_rather_than_passed_over(self):
        """No declaration and no job here produces it, so arm E cannot judge it.
        It says so, and names the arm that does red about it."""
        mod = self.tree(["gate"], {"gate": f"{WF}/gate.yml"}, self.CAMPAIGNS, ["gate"])
        rc, out = self.run_checker(
            mod,
            live(self.CAMPAIGNS, ["gate", "from nowhere"]),
            ["main", "campaign/a"],
            {"campaign/a": {f"{WF}/gate.yml"}},
        )
        self.assertEqual(rc, 1, out)
        self.assertIn("arm E could not ask whether the refs it covers", out)
        self.assertIn("from nowhere", out)
        self.assertIn(self.NOT_DECLARED, out)
        self.assert_no_deadlock(out)


# ---------------------------------------------------------------------------
# 4. The judged ref is answered from the tree in hand — the same correction
#    arm B already carries — because that tree is what the ref becomes.
# ---------------------------------------------------------------------------


class TheJudgedRefIsTheTreeInHand(LiveArms):
    def test_a_pull_request_that_adds_the_missing_workflow_is_not_blocked(self):
        """The repair. The API view of `main` lacks the workflow; the tree in
        hand — head merged into base — has it, and that is what `main`
        becomes. Reading the API here reds the pull request that fixes the
        deadlock, which is the shape this arm's own message names."""
        mod = self.tree(["gate"], {"gate": f"{WF}/gate.yml"},
                        ["~DEFAULT_BRANCH"], ["gate"])
        rc, out = self.run_checker(
            mod,
            live(["~DEFAULT_BRANCH"], ["gate"]),
            ["main"],
            {"main": set()},                     # not there yet, per the API
        )
        self.assertEqual(rc, 0, out)
        self.assert_no_deadlock(out)

    def test_a_pull_request_that_does_not_add_it_is_still_blocked(self):
        """The other direction, and what keeps this from being a hole: if the
        merge result STILL cannot report the context, it still reds."""
        mod = self.tree(
            ["gate", "elsewhere"],
            {"gate": f"{WF}/gate.yml", "elsewhere": f"{WF}/elsewhere.yml"},
            ["~DEFAULT_BRANCH"],
            ["gate"],                            # `elsewhere` exists nowhere
        )
        rc, out = self.run_checker(
            mod,
            live(["~DEFAULT_BRANCH"], ["gate", "elsewhere"]),
            ["main"],
            {"main": {f"{WF}/gate.yml"}},
        )
        self.assertEqual(rc, 1, out)
        self.assert_deadlock(out, "elsewhere", "main")
        self.assertIn("the tree in hand does not carry", out)

    def test_another_covered_ref_is_still_read_from_the_api(self):
        """The tree in hand answers for ONE ref. Every other covered ref is the
        reason this arm exists — a deadlock on a branch no tree here knows."""
        mod = self.tree(["gate"], {"gate": f"{WF}/gate.yml"}, ["~ALL"], ["gate"])
        rc, out = self.run_checker(
            mod,
            live(["~ALL"], ["gate"]),
            ["main", "campaign/a"],
            {"main": set(), "campaign/a": set()},
        )
        self.assertEqual(rc, 1, out)
        self.assert_deadlock(out, "gate", "campaign/a")
        self.assertIn("that ref does not carry", out)
        # `main` is the judged ref and the tree in hand carries it, so the arm
        # must not also be claiming `main` is deadlocked.
        self.assertNotIn("branch 'main' is covered", out)


# ---------------------------------------------------------------------------
# 5. Vacuity: an arm that examined nothing has proved nothing.
# ---------------------------------------------------------------------------


class ExaminingNothingIsAFinding(LiveArms):
    def test_zero_covered_refs_is_a_finding(self):
        mod = self.tree(["gate"], {"gate": f"{WF}/gate.yml"},
                        ["refs/heads/nothing/*"], ["gate"])
        rc, out = self.run_checker(
            mod,
            live(["refs/heads/nothing/*"], ["gate"]),
            ["main"],
            {},
        )
        self.assertEqual(rc, 1, out)
        self.assertIn("arm E examined 0 covered refs", out)

    def test_the_scope_line_states_the_denominator(self):
        mod = self.tree(["gate"], {"gate": f"{WF}/gate.yml"}, ["~ALL"], ["gate"])
        rc, out = self.run_checker(
            mod,
            live(["~ALL"], ["gate"]),
            ["main", "campaign/a"],
            {"main": {f"{WF}/gate.yml"}, "campaign/a": {f"{WF}/gate.yml"}},
        )
        self.assertEqual(rc, 0, out)
        self.assertIn("1 live rulesets compared over 2 covered refs", out)


if __name__ == "__main__":
    unittest.main()
