"""The eligibility arm reds when the safety is REMOVED, not when it is present.

`tools/check-required-contexts.py` used to refuse any required job carrying a
job-level `if:`. The reasoning was right — a skipped job reports `skipped`, and
branch protection counts that as a satisfied required check — and it was pointed
the wrong way for the one expression that matters. `if: always()` is not a
condition; it is the absence of one, and on a job with `needs:` it is the only
thing preventing the very skip the finding warns about. So the checker was RED
on the version that cannot be silently skipped and GREEN on the version that
can, and deleting the safety made the finding disappear.

Nothing caught that, because nobody ran the test this whole class needs:
**perturb toward the vacuous shape and check the gate reddens.** That test is
`test_removing_the_safety_reddens_the_gate` and
`test_removing_needs_safety_from_the_shipped_workflow_reddens`, and everything
else here exists to keep them honest — a gate that reds for some other reason
has not demonstrated anything.

These run the SHIPPED script against real directories, offline, with the exit
status captured before anything is piped and BOTH streams read: this checker
writes its summary and findings to stderr and only its notes to stdout, so
reading one stream is a way to get a real-looking verdict out of a row that
measured nothing.
"""

from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
REPO = TOOLS.parent
CHECKER = TOOLS / "check-required-contexts.py"

_spec = importlib.util.spec_from_file_location("check_required_contexts", CHECKER)
assert _spec and _spec.loader
crc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(crc)


MANIFEST = """\
default_branch = "main"
max_advisory = 0

[[ruleset]]
name = "protect-main"
include = ["~DEFAULT_BRANCH"]
contexts = [ "gate" ]

[ruleset.provided_by]
"gate" = ".github/workflows/gate.yml"
"""


def workflow(if_line: str | None, needs: str | None = "[prep]") -> str:
    lines = [
        "name: gate",
        "on:",
        "  pull_request:",
        "jobs:",
        "  gate:",
        "    name: gate",
    ]
    if needs is not None:
        lines.append(f"    needs: {needs}")
    if if_line is not None:
        lines.append(f"    if: {if_line}")
    lines += [
        "    runs-on: ubuntu-latest",
        "    steps:",
        "      - run: echo hi",
    ]
    return "\n".join(lines) + "\n"


class Harness(unittest.TestCase):
    """Run the shipped checker over a directory it believes is the repository.

    The script derives `REPO` from its own `__file__.parent.parent`, so a copy
    at `<tmp>/tools/` judges `<tmp>`. No mocking and no monkeypatching: the
    object under test is the file that ships.
    """

    def judge(self, root: Path) -> tuple[int, str]:
        proc = subprocess.run(
            [sys.executable, str(root / "tools" / "check-required-contexts.py"),
             "--offline", "--ref", "main"],
            capture_output=True, text=True,
        )
        merged = proc.stdout + proc.stderr
        self.assertIn(
            "check-required-contexts:", merged,
            "the run produced no verdict at all; this row measured nothing",
        )
        return proc.returncode, merged

    def synthetic(self, root: Path, gate_yml: str, manifest: str = MANIFEST) -> None:
        (root / ".github" / "workflows").mkdir(parents=True)
        (root / "tools").mkdir(parents=True)
        shutil.copy2(CHECKER, root / "tools" / "check-required-contexts.py")
        (root / ".github" / "required-status-checks.toml").write_text(manifest, encoding="utf-8")
        (root / ".github" / "workflows" / "gate.yml").write_text(gate_yml, encoding="utf-8")

    def shipped(self, root: Path) -> None:
        """This repository's own `.github/` and the checker, nothing else."""
        (root / "tools").mkdir(parents=True)
        shutil.copy2(CHECKER, root / "tools" / "check-required-contexts.py")
        (root / ".github").mkdir(parents=True)
        shutil.copy2(
            REPO / ".github" / "required-status-checks.toml",
            root / ".github" / "required-status-checks.toml",
        )
        shutil.copytree(REPO / ".github" / "workflows", root / ".github" / "workflows")

    def assert_skip_finding(self, out: str, ctx: str = "gate") -> None:
        self.assertIn(
            f"required context {ctx!r} ", out,
            "red, but not about the job under test — this row is confounded",
        )
        self.assertIn("can be SKIPPED", out)

    def assert_no_skip_finding(self, out: str) -> None:
        self.assertNotIn("can be SKIPPED", out)


# ---------------------------------------------------------------------------
# THE ACCEPTANCE TEST: perturb toward the vacuous shape and the gate reddens.
# ---------------------------------------------------------------------------


class RemovingTheSafetyReddens(Harness):
    def test_removing_the_safety_reddens_the_gate(self):
        """`needs:` + `if: always()` is green; delete the `if:` line and it reds.

        This is the direction that was broken, and it was broken both ways at
        once: the safe tree was red and the vacuous tree was green.
        """
        with tempfile.TemporaryDirectory() as td:
            safe = Path(td) / "safe"
            safe.mkdir()
            self.synthetic(safe, workflow("always()"))
            rc, out = self.judge(safe)
            self.assertEqual(rc, 0, f"a job protected by `if: always()` should pass:\n{out}")
            self.assert_no_skip_finding(out)

            # Remove the safety, and assert the removal actually happened: a
            # scripted replacement that matches nothing is a silent no-op, and
            # the perturbed tree would then be the unperturbed one.
            wf = safe / ".github" / "workflows" / "gate.yml"
            before = wf.read_text(encoding="utf-8")
            self.assertEqual(before.count("    if: always()\n"), 1)
            wf.write_text(before.replace("    if: always()\n", "", 1), encoding="utf-8")
            after = wf.read_text(encoding="utf-8")
            self.assertNotIn("if: always()", after)
            self.assertEqual(len(before.splitlines()) - len(after.splitlines()), 1)

            rc, out = self.judge(safe)
            self.assertEqual(rc, 1, f"removing the safety must RED the gate:\n{out}")
            self.assert_skip_finding(out)
            self.assertIn("implicit `success()`", out)

    def test_removing_needs_safety_from_the_shipped_workflow_reddens(self):
        """The same perturbation, on this repository's own workflow tree.

        The synthetic case proves the rule; this proves the rule is BOUND to the
        files that ship. It reads `.github/` as committed, confirms it is green,
        then gives the one required job a `needs:` — which is the vacuous shape
        arriving without anybody writing an `if:` at all — and requires a red.
        """
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "repo"
            root.mkdir()
            self.shipped(root)
            rc, out = self.judge(root)
            self.assertEqual(rc, 0, f"the shipped tree must be green to start:\n{out}")

            audit = root / ".github" / "workflows" / "prefab-audit.yml"
            text = audit.read_text(encoding="utf-8")
            marker = "    name: NBT palette audit (allowlist + code-injection forbid)\n"
            self.assertEqual(
                text.count(marker), 1,
                "the required job's `name:` line moved; this perturbation is "
                "no longer aimed at the job it names",
            )
            audit.write_text(text.replace(marker, marker + "    needs: [prep]\n", 1),
                             encoding="utf-8")
            self.assertEqual(audit.read_text(encoding="utf-8").count("    needs: [prep]\n"), 1)

            rc, out = self.judge(root)
            self.assertEqual(
                rc, 1,
                f"a required job that a failed `needs:` can skip must RED:\n{out}",
            )
            self.assert_skip_finding(out, "NBT palette audit (allowlist + code-injection forbid)")

    def test_a_job_level_always_is_no_longer_a_finding_on_its_own(self):
        """The inversion itself: the safety must not be what makes the gate red."""
        for expr in ("always()", "${{ always() }}", "(always())",
                     "always() || github.event_name == 'push'"):
            with self.subTest(expr=expr), tempfile.TemporaryDirectory() as td:
                root = Path(td) / "repo"
                root.mkdir()
                self.synthetic(root, workflow(expr))
                rc, out = self.judge(root)
                self.assertEqual(rc, 0, f"{expr!r} should be accepted:\n{out}")
                self.assert_no_skip_finding(out)


# ---------------------------------------------------------------------------
# It must still refuse everything it refused before.
# ---------------------------------------------------------------------------


class StillRefusesASkippableCondition(Harness):
    SKIPPABLE = (
        "success()",
        "failure()",
        "!cancelled()",
        "cancelled()",
        "github.event_name == 'push'",
        "github.ref != 'refs/heads/main'",
        "always() && success()",
        "always() && github.ref == 'refs/heads/main'",
        "${{ !cancelled() && always() }}",
        "needs.prep.result == 'success'",
        "true",
        "false",
    )

    def test_every_skippable_condition_is_still_a_finding(self):
        for expr in self.SKIPPABLE:
            with self.subTest(expr=expr), tempfile.TemporaryDirectory() as td:
                root = Path(td) / "repo"
                root.mkdir()
                self.synthetic(root, workflow(expr))
                rc, out = self.judge(root)
                self.assertEqual(rc, 1, f"{expr!r} can be false; it must RED:\n{out}")
                self.assert_skip_finding(out)

    def test_needs_without_any_if_is_a_finding(self):
        """The hole that was green before this rule existed at all."""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "repo"
            root.mkdir()
            self.synthetic(root, workflow(None, needs="[prep]"))
            rc, out = self.judge(root)
            self.assertEqual(rc, 1, out)
            self.assert_skip_finding(out)

    def test_no_if_and_no_needs_is_not_a_finding(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "repo"
            root.mkdir()
            self.synthetic(root, workflow(None, needs=None))
            rc, out = self.judge(root)
            self.assertEqual(rc, 0, out)

    def test_a_step_level_if_is_not_a_job_level_one(self):
        """A step's `if: always()` says nothing about whether the JOB runs."""
        yml = workflow(None, needs=None).replace(
            "      - run: echo hi\n",
            "      - run: echo hi\n        if: always()\n",
        )
        self.assertIn("        if: always()", yml)
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "repo"
            root.mkdir()
            self.synthetic(root, yml)
            rc, out = self.judge(root)
            self.assertEqual(rc, 0, out)


# ---------------------------------------------------------------------------
# The derivation, asked of the expression directly.
# ---------------------------------------------------------------------------


class Derivation(unittest.TestCase):
    def test_always_is_the_only_true_atom(self):
        self.assertEqual(crc.evaluate_condition("always()"), crc.TRUE)
        for atom in ("success()", "failure()", "cancelled()", "true", "false",
                     "github.ref", "needs.a.result", "'x'", "1",
                     "hashFiles('**/x')", "contains(github.ref, 'main')"):
            with self.subTest(atom=atom):
                self.assertEqual(
                    crc.evaluate_condition(atom), crc.UNKNOWN,
                    f"{atom!r} is not provably true in every state a run can reach",
                )

    def test_composition_is_the_ordinary_lattice(self):
        cases = {
            "${{ always() }}": crc.TRUE,
            "(always())": crc.TRUE,
            "always() && always()": crc.TRUE,
            "always() || success()": crc.TRUE,
            "success() || always()": crc.TRUE,
            "!always()": crc.FALSE,
            "always() && success()": crc.UNKNOWN,
            "always() && github.ref == 'refs/heads/main'": crc.UNKNOWN,
            "!cancelled()": crc.UNKNOWN,
            "!cancelled() && always()": crc.UNKNOWN,
            "always() == true": crc.UNKNOWN,
        }
        for expr, want in cases.items():
            with self.subTest(expr=expr):
                self.assertEqual(crc.evaluate_condition(expr), want)

    def test_an_unparseable_condition_refuses_rather_than_guesses(self):
        for expr in ("", "always(", "&& always()", "'unterminated",
                     "always() ${{ x }}", "always() foo"):
            with self.subTest(expr=expr):
                with self.assertRaises(crc.ExprRefusal):
                    crc.evaluate_condition(expr)

    def test_skip_proof_reads_the_effective_condition(self):
        self.assertTrue(crc.skip_proof({"if": None, "needs": False})[0])
        self.assertFalse(crc.skip_proof({"if": None, "needs": True})[0])
        self.assertTrue(crc.skip_proof({"if": "always()", "needs": True})[0])
        self.assertFalse(crc.skip_proof({"if": "success()", "needs": False})[0])
        # An expression that cannot be evaluated is refused, not assumed.
        self.assertFalse(crc.skip_proof({"if": "always(", "needs": False})[0])
        self.assertFalse(crc.skip_proof({"if": "", "needs": False})[0])


class FoldedConditions(Harness):
    """A safety written across two lines is not a false red — and a folded
    SKIPPABLE condition is still a finding, so gathering the block scalar has
    not become a way to smuggle one past."""

    def yml(self, indicator: str, body: str) -> str:
        return (
            "name: gate\n"
            "on:\n"
            "  pull_request:\n"
            "jobs:\n"
            "  gate:\n"
            "    name: gate\n"
            "    needs: [prep]\n"
            f"    if: {indicator}\n"
            f"      {body}\n"
            "    runs-on: ubuntu-latest\n"
            "    steps:\n"
            "      - run: echo hi\n"
        )

    def test_folded_always_is_accepted(self):
        for indicator in (">-", ">", "|", "|-"):
            with self.subTest(indicator=indicator), tempfile.TemporaryDirectory() as td:
                root = Path(td) / "repo"
                root.mkdir()
                self.synthetic(root, self.yml(indicator, "always()"))
                rc, out = self.judge(root)
                self.assertEqual(rc, 0, out)
                self.assert_no_skip_finding(out)

    def test_folded_skippable_is_still_a_finding(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "repo"
            root.mkdir()
            self.synthetic(root, self.yml(">-", "success()"))
            rc, out = self.judge(root)
            self.assertEqual(rc, 1, out)
            self.assert_skip_finding(out)


if __name__ == "__main__":
    unittest.main()
