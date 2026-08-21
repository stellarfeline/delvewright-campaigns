#!/usr/bin/env python3
"""Every CI job gates something, and every gate can report.

A required status check is matched BY ITS NAME STRING. That single fact has two
failure directions, and this repository has shipped both.

  FORWARD — a required context that no job produces never reports, so every pull
  request into that ref is blocked forever, including the pull request that
  would fix it. It happened here: a path filter meant a campaign-only change
  produced no run of `prefab-audit.yml`, so the context required on `main` never
  reported and the merge state was blocked with nothing to click.

  REVERSE — a job that runs and is not required gates nothing. Its red is a
  colour on a page and `gh pr merge` walks past it. `actionlint` has been in
  that state on every workflow-touching pull request into `main`.

Both are silent. Nothing about a repository looks different in either case, and
that is why this file exists: it turns each of them into an ordinary red on the
pull request that would have caused it.

## What is different about THIS repository

The pipeline repo's equivalent compares one flat list to one `ci.yml`, because
one branch is protected and every job is required on it. Here neither holds.

Protection lives in **rulesets**, not in classic branch protection — `main` has
no classic protection at all — and there are two of them, over different refs
with different required sets. And one required job's workflow, `zone-audit.yml`,
exists ONLY on the campaign branches, deliberately: it builds a pinned engine to
expand and judge zone programs, which is work only a campaign branch has. So it
is required exactly where it exists.

A single flat list would have to either be wrong about that or lie about it.
The declaration is therefore ref-scoped (`.github/required-status-checks.toml`),
and the checker judges in three ref-aware arms plus a live one:

  A. COVERAGE (ref-independent). Every job defined in THIS tree is required by
     at least one declared ruleset, or is declared advisory with a reason this
     file can evaluate. This is the reverse direction and it needs no ref: a job
     that gates on some ref is a gate; a job that gates nowhere is not.

  B. RESOLUTION (ref-scoped). Every context required on the ref being judged
     resolves to a job `name:` in this tree. On a pull request the ref judged is
     the BASE ref, and the tree is the MERGE ref — head merged into base, which
     is what `actions/checkout` gives a `pull_request` job and therefore exactly
     the pair whose workflows GitHub will run. So merging `main` forward into a
     campaign branch does not red for lacking `zone-audit.yml`, because the base
     half of the merge carries it; but a pull request that DELETES it does red,
     here, before the context it removed can block that ref forever. Contexts
     required only on refs this tree does not serve are STATED, with the ref
     pattern and the pull request that will judge them, never dropped.

  C. ELIGIBILITY (ref-independent). A job named as required must be ABLE to
     report on every pull request into the refs it guards: its workflow has a
     `pull_request:` trigger, that trigger carries no `paths`/`paths-ignore`/
     `branches`/`branches-ignore` filter, the job CANNOT BE SKIPPED (a skipped
     job reports "skipped", which GitHub counts as a satisfied required check —
     a hole that looks exactly like a pass), and it has no `strategy:` (a matrix
     job's context is `name (value)`, not `name`). This arm is the one that
     would have caught the path filter before it deadlocked the repository, and
     it is why `actionlint` cannot simply be promoted today.

     "Cannot be skipped" is asked of the job's effective condition and derived
     from it, never declared by its author — see the derivation above
     `skip_proof`. This arm used to ask instead whether the job HAD an `if:`,
     which is the syntax that usually carries the property and not the property.
     They invert on `if: always()`, which is not a condition but the absence of
     one: the file was red on the version that cannot be skipped and green on
     the version that can, so deleting the safety made the finding go away.

  D. LIVE (default on). The declaration equals the live rulesets: same ref
     patterns, same contexts, `enforcement = "active"`, and no live ruleset
     undeclared. This is what catches a ruleset edited in the web UI, which no
     file-to-file comparison can see.

## Why the live arm gates instead of merely reporting

The pipeline repo's checker reads only the repo, on the reasoning that CI's
token has `contents: read` and cannot see branch protection, and a gate that
needs a privileged token is a gate that quietly stops running. That reasoning is
sound and it does not apply here, which was worth measuring rather than
assuming: **both repositories are public, and a public repository's rulesets are
readable with NO credential at all** — `GET /repos/{owner}/{repo}/rulesets/{id}`
returns `conditions` and `rules`, contexts included, unauthenticated. So the
live comparison needs no token, no permission grant, and nothing that can be
revoked out from under it. It runs in the required job on every pull request.

It is on by DEFAULT, and the opt-out is `--offline`. That polarity is the whole
point: dropping the live guarantee then requires ADDING a flag, which a reviewer
sees in the diff, instead of removing one, which nobody notices.

And it never degrades to a pass. If the API cannot be read — offline, rate
limited, an HTTP error — that is not a green: the checker says the comparison
DID NOT RUN and exits non-zero. `--offline` is the honest way to get a green
without it, and it prints, loudly, which arm did not run. A creator with no
network can still run every other arm on their own clone, which is the floor
this project does not negotiate.

## Binding counts

Each arm states how many objects it examined, and zero is a finding rather than
a pass in every one of them. A checker that parsed no jobs, or resolved no
contexts, or compared no rulesets, has proved nothing — and it is green.

Exit 0 clean, 1 on any finding or refusal.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import subprocess
import sys
import tomllib
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MANIFEST = REPO / ".github" / "required-status-checks.toml"
WORKFLOW_DIR = REPO / ".github" / "workflows"

OWNER_REPO = "stellarfeline/delvewright-campaigns"
API = "https://api.github.com"

# The advisory reasons this checker can EVALUATE. A reason it cannot evaluate is
# a reason it cannot retire, which is a free-text hatch wearing an enum's name.
ADVISORY_REASONS = {
    "no-pull-request-trigger",
    "pull-request-path-filtered",
}

# Filters on a required job's `pull_request:` trigger that can stop it reporting.
DISQUALIFYING_PR_FILTERS = ("paths", "paths-ignore", "branches", "branches-ignore")


# ---------------------------------------------------------------------------
# A deliberately small YAML reader.
#
# Stdlib only, because this runs in a required CI job and on a creator's clone
# with nothing installed. It understands exactly the workflow shapes this
# repository uses and REFUSES on anything else rather than guessing — a parser
# that silently returns nothing is the vacuity mode this whole file is about.
# ---------------------------------------------------------------------------

_KEY = re.compile(r"^(?P<indent> *)(?P<key>[A-Za-z_][A-Za-z0-9_.-]*|\"[^\"]+\"|'[^']+'):(?P<rest>.*)$")


def _unquote(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1]
    return s


def _scalar(rest: str) -> str:
    """The value on a `key: value` line, with a trailing YAML comment removed."""
    v = rest.strip()
    # YAML starts a comment at ` #` (hash preceded by whitespace) or a leading #.
    if v.startswith("#"):
        return ""
    cut = v.find(" #")
    if cut != -1:
        v = v[:cut]
    return _unquote(v.strip())


def _structural_lines(text: str) -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []
    for n, line in enumerate(text.splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        out.append((n, line.rstrip()))
    return out


def _block(lines: list[tuple[int, str]], start: int, indent: int) -> list[tuple[int, str]]:
    """Lines after `start` that are indented deeper than `indent`."""
    out: list[tuple[int, str]] = []
    for i in range(start + 1, len(lines)):
        _, text = lines[i]
        if len(text) - len(text.lstrip()) <= indent:
            break
        out.append(lines[i])
    return out


class Workflow:
    def __init__(self, path: Path):
        self.path = path
        self.rel = path.relative_to(REPO).as_posix()
        self.errors: list[str] = []
        # trigger name -> set of its sub-keys
        self.triggers: dict[str, set[str]] = {}
        # job key -> attributes
        self.jobs: dict[str, dict[str, object]] = {}
        self._parse()

    def _parse(self) -> None:
        lines = _structural_lines(self.path.read_text(encoding="utf-8"))
        top: dict[str, tuple[int, str]] = {}
        for i, (_, text) in enumerate(lines):
            m = _KEY.match(text)
            if m and m.group("indent") == "":
                top[_unquote(m.group("key"))] = (i, m.group("rest"))

        # `on:` — YAML 1.1 folds bare `on` to boolean true, so a `true` key is
        # the same thing arriving through a different door.
        on_key = "on" if "on" in top else ("true" if "true" in top else None)
        if on_key is None:
            self.errors.append(f"{self.rel}: no top-level `on:` trigger block")
        else:
            i, rest = top[on_key]
            inline = _scalar(rest)
            if inline:
                # Flow form: `on: [pull_request, push]` or `on: push`.
                if inline.startswith("["):
                    for t in inline.strip("[]").split(","):
                        if t.strip():
                            self.triggers[_unquote(t)] = set()
                else:
                    self.triggers[inline] = set()
            else:
                for j in range(i + 1, len(lines)):
                    _, text = lines[j]
                    ind = len(text) - len(text.lstrip())
                    if ind == 0:
                        break
                    m = _KEY.match(text)
                    if not m or len(m.group("indent")) != 2:
                        continue
                    name = _unquote(m.group("key"))
                    subkeys = set()
                    for _, sub in _block(lines, j, 2):
                        sm = _KEY.match(sub)
                        if sm and len(sm.group("indent")) == 4:
                            subkeys.add(_unquote(sm.group("key")))
                    self.triggers[name] = subkeys

        if "jobs" not in top:
            self.errors.append(f"{self.rel}: no top-level `jobs:` block")
            return
        ji, _ = top["jobs"]
        for j in range(ji + 1, len(lines)):
            _, text = lines[j]
            ind = len(text) - len(text.lstrip())
            if ind == 0:
                break
            m = _KEY.match(text)
            if not m or len(m.group("indent")) != 2:
                continue
            key = _unquote(m.group("key"))
            # `if` holds the EXPRESSION, not a flag: whether a job can be
            # skipped is a property of what the condition says, and a boolean
            # here would throw that away before anything could ask. `None` is
            # "no `if:` at all", which is a different state from an empty one.
            attrs: dict[str, object] = {
                "if": None, "needs": False, "strategy": False, "uses": False,
            }
            # GitHub falls back to the job KEY when there is no `name:`, and so
            # does the status context. Defaulting to the key is not a guess.
            name = key
            block = _block(lines, j, 2)
            for bi, (_, sub) in enumerate(block):
                sm = _KEY.match(sub)
                if not sm or len(sm.group("indent")) != 4:
                    continue
                k = _unquote(sm.group("key"))
                if k == "name":
                    raw = sm.group("rest").strip()
                    if raw in ("|", ">", "|-", ">-"):
                        self.errors.append(
                            f"{self.rel}: job {key!r} names itself with a block "
                            f"scalar; this reader will not guess what context "
                            f"string that produces"
                        )
                    else:
                        name = _scalar(sm.group("rest"))
                elif k == "if":
                    raw = sm.group("rest").strip()
                    if raw in ("|", ">", "|-", ">-", "|+", ">+"):
                        # A folded or literal condition. Gathering it is not a
                        # nicety: refusing it would red a job whose safety is
                        # written across two lines, which is a false red on the
                        # exact shape this arm exists to protect.
                        parts = []
                        for _, cont in block[bi + 1:]:
                            if len(cont) - len(cont.lstrip()) <= 4:
                                break
                            parts.append(cont.strip())
                        attrs["if"] = " ".join(parts)
                    else:
                        attrs["if"] = _scalar(sm.group("rest"))
                elif k in ("needs", "strategy", "uses"):
                    attrs[k] = True
            attrs["name"] = name
            self.jobs[key] = attrs

    def pull_request_filters(self) -> list[str] | None:
        """Disqualifying filters on `pull_request:`, or None if there is no such
        trigger at all."""
        if "pull_request" not in self.triggers:
            return None
        return [f for f in DISQUALIFYING_PR_FILTERS if f in self.triggers["pull_request"]]


# ---------------------------------------------------------------------------
# CAN THIS JOB BE SKIPPED?
#
# The property this arm needs is *can this job be skipped*. The syntax that
# usually carries it is *the job has an `if:`*. They agree on every condition
# that can be false, and they INVERT on the one expression that cannot.
#
# `if: always()` is not a condition. It is the ABSENCE of one, and it is the
# only thing standing between a job with `needs:` and the very skip the finding
# warns about. Keying on the syntax made this file green on the version that can
# be silently skipped and red on the version that cannot — a gate that rewards
# removing the safety it exists to require. So the question is asked of the
# EXPRESSION, and the answer is derived from it rather than declared by whoever
# wrote it: there is no marker, no comment, no acknowledgement to reach for.
#
# ## Which expressions qualify, and why the derived set has one member
#
# A job's effective condition is its `if:` when it has one, and the implicit
# `success()` over `needs:` when it does not. So:
#
#   no `if:` and no `needs:`   the job runs on every run of its workflow. Nothing
#                              can skip it. SKIP-PROOF.
#   no `if:` and `needs:`      the implicit condition is `success()`: a need that
#                              fails or is skipped skips this job, which reports
#                              `skipped`, which protection counts as satisfied.
#                              SKIPPABLE — and this is the shape that is green
#                              today, which is the whole defect.
#   an `if:`                   decided below, by abstract evaluation.
#
# The evaluation is three-valued — TRUE / FALSE / UNKNOWN — over the operator
# grammar GitHub's expression language actually has, and every atom is UNKNOWN
# except one:
#
#   always()          TRUE. Documented to return true "even when canceled",
#                     which is the only expression for which GitHub states a
#                     guarantee that survives every state a run can reach.
#   success()         UNKNOWN. False when a need failed — the default, spelled
#                     out. Exactly the skip this arm is about.
#   failure()         UNKNOWN. False on the ordinary path.
#   cancelled()       UNKNOWN, and therefore `!cancelled()` is UNKNOWN too. It
#                     survives a failed need and does NOT survive cancellation,
#                     so it is a condition that can be false and is refused.
#   any github.*,     UNKNOWN. Run-dependent by construction.
#   needs.*, env.*,
#   inputs.*, ...
#   a comparison      UNKNOWN, whatever its operands.
#   `true` / `false`  UNKNOWN. A truthy literal is true in every state the
#     and every other  expression language can OBSERVE, and that is a weaker
#     literal          claim than the one this arm needs: `always()` is singled
#                     out in GitHub's own documentation precisely because
#                     cancellation is handled outside the expression. Refusing
#                     a literal costs nothing real — nobody writes `if: true` on
#                     a required job — and the direction of the error matters:
#                     wrongly refusing a safe job is a red somebody reads,
#                     wrongly accepting a skippable one is the hole.
#   anything this     UNKNOWN, by the same rule. A reader that cannot parse an
#     reader cannot    expression has not proved anything about it, and the
#     parse            unproved answer here is the refusing one.
#
# Composition is the ordinary lattice: `&&` is TRUE only if both sides are,
# `||` is TRUE if either side is, `!` inverts TRUE and FALSE and leaves UNKNOWN
# alone. Because `always()` is the only TRUE atom, every expression this
# function accepts derives its truth from an `always()`, and so inherits the
# guarantee that made `always()` the one member. That is not a coincidence to
# rely on quietly — it is why a one-member atom set is enough, and why the set
# is derived rather than remembered: `always() && success()` and
# `always() && github.ref == 'refs/heads/main'` are refused by the same
# machinery that accepts `always()`, without anybody having had to think of
# them.
# ---------------------------------------------------------------------------

TRUE, FALSE, UNKNOWN = "TRUE", "FALSE", "UNKNOWN"

_COMPARISONS = ("==", "!=", "<=", ">=", "<", ">")
_TWO_CHAR = ("&&", "||", "==", "!=", "<=", ">=")
_WORD = re.compile(r"[A-Za-z_0-9.*-]+")


class ExprRefusal(Exception):
    """This reader will not guess what an expression evaluates to."""


def _tokens(src: str) -> list[str]:
    out: list[str] = []
    i, n = 0, len(src)
    while i < n:
        c = src[i]
        if c.isspace():
            i += 1
            continue
        if any(src.startswith(t, i) for t in _TWO_CHAR):
            out.append(src[i:i + 2])
            i += 2
            continue
        if c in "()[],<>!":
            out.append(c)
            i += 1
            continue
        if c == "'":
            # GitHub escapes a single quote by doubling it.
            j = i + 1
            while j < n:
                if src[j] == "'":
                    if j + 1 < n and src[j + 1] == "'":
                        j += 2
                        continue
                    break
                j += 1
            if j >= n:
                raise ExprRefusal("unterminated string literal")
            out.append(src[i:j + 1])
            i = j + 1
            continue
        m = _WORD.match(src, i)
        if not m:
            raise ExprRefusal(f"unexpected character {c!r}")
        out.append(m.group(0))
        i = m.end()
    if not out:
        raise ExprRefusal("empty expression")
    return out


class _Eval:
    """Abstract evaluation to TRUE / FALSE / UNKNOWN. Never to a value."""

    def __init__(self, toks: list[str]):
        self.t = toks
        self.i = 0

    def peek(self) -> str | None:
        return self.t[self.i] if self.i < len(self.t) else None

    def take(self) -> str:
        tok = self.peek()
        if tok is None:
            raise ExprRefusal("expression ended early")
        self.i += 1
        return tok

    def parse(self) -> str:
        v = self.or_()
        if self.peek() is not None:
            raise ExprRefusal(f"trailing {self.peek()!r}")
        return v

    def or_(self) -> str:
        v = self.and_()
        while self.peek() == "||":
            self.take()
            r = self.and_()
            v = TRUE if TRUE in (v, r) else (FALSE if v == r == FALSE else UNKNOWN)
        return v

    def and_(self) -> str:
        v = self.not_()
        while self.peek() == "&&":
            self.take()
            r = self.not_()
            v = FALSE if FALSE in (v, r) else (TRUE if v == r == TRUE else UNKNOWN)
        return v

    def not_(self) -> str:
        if self.peek() == "!":
            self.take()
            return {TRUE: FALSE, FALSE: TRUE}.get(self.not_(), UNKNOWN)
        return self.cmp_()

    def cmp_(self) -> str:
        v = self.primary()
        if self.peek() in _COMPARISONS:
            self.take()
            self.primary()
            # Even `'a' == 'a'` is UNKNOWN here. Deciding constant comparisons
            # would buy nothing a required job's condition ever needs, and every
            # line of cleverness is a line that can be wrong in the direction
            # that opens the hole.
            return UNKNOWN
        return v

    def primary(self) -> str:
        tok = self.take()
        if tok == "(":
            v = self.or_()
            if self.take() != ")":
                raise ExprRefusal("unbalanced `(`")
            return self._suffix(v)
        if tok in ("&&", "||", ")", ",", "]"):
            raise ExprRefusal(f"unexpected {tok!r}")
        if tok.startswith("'"):
            return self._suffix(UNKNOWN)
        if self.peek() == "(":
            self._skip_balanced("(", ")")
            # The one atom whose truth GitHub guarantees in every state.
            return self._suffix(TRUE if tok == "always" else UNKNOWN)
        return self._suffix(UNKNOWN)

    def _suffix(self, v: str) -> str:
        """`x['k']` and `x.*[0]` — an index never makes a value provable."""
        while self.peek() == "[":
            self._skip_balanced("[", "]")
            v = UNKNOWN
        return v

    def _skip_balanced(self, opener: str, closer: str) -> None:
        if self.take() != opener:
            raise ExprRefusal(f"expected {opener!r}")
        depth = 1
        while depth:
            tok = self.take()
            if tok == opener:
                depth += 1
            elif tok == closer:
                depth -= 1


def evaluate_condition(expr: str) -> str:
    """TRUE, FALSE or UNKNOWN for a job-level `if:`, refusing rather than guessing."""
    s = expr.strip()
    if s.startswith("${{") and s.endswith("}}") and "${{" not in s[3:]:
        s = s[3:-2]
    elif "${{" in s:
        # A partly-interpolated condition. GitHub allows it; this reader will
        # not pretend to know what the surrounding text does with the result.
        raise ExprRefusal("`${{` appears other than as the whole expression")
    return _Eval(_tokens(s)).parse()


def skip_proof(attrs: dict) -> tuple[bool, str]:
    """Can this job be skipped? Returns (cannot-be-skipped, why)."""
    expr = attrs.get("if")
    if expr is None:
        if attrs.get("needs"):
            return False, (
                "it has no `if:`, so its condition is the implicit `success()` "
                "over its `needs:` — a need that fails or is skipped skips THIS "
                "job, and a skipped job reports `skipped`, which GitHub counts "
                "as a SATISFIED required check. `if: always()` is what removes "
                "that condition; without it the gate passes by not running"
            )
        return True, "it has no `if:` and no `needs:`, so nothing can skip it"
    try:
        verdict = evaluate_condition(str(expr))
    except ExprRefusal as exc:
        return False, (
            f"its `if:` is {expr!r}, which this reader will not evaluate "
            f"({exc}). An unproved condition is a condition that can be false, "
            f"and a skipped job reports `skipped`, which GitHub counts as a "
            f"SATISFIED required check"
        )
    if verdict == TRUE:
        return True, f"its `if:` is {expr!r}, which is true in every state a run can reach"
    return False, (
        f"its `if:` is {expr!r}, which is not provably true in every state — a "
        f"run in which it is false SKIPS the job, and a skipped job reports "
        f"`skipped`, which GitHub counts as a SATISFIED required check. The "
        f"gate would pass by not running. Only `always()` carries a guarantee "
        f"that survives a failed `needs:` and a cancellation both; "
        f"`!cancelled()`, `success()` and any `github.*` test do not"
    )


# ---------------------------------------------------------------------------
# Ref matching
# ---------------------------------------------------------------------------


def ref_matches(pattern: str, ref: str, default_branch: str) -> bool:
    """`ref` is a short branch name; `pattern` is a ruleset include pattern."""
    if pattern == "~ALL":
        return True
    if pattern == "~DEFAULT_BRANCH":
        return ref == default_branch
    full = ref if ref.startswith("refs/") else f"refs/heads/{ref}"
    return fnmatch.fnmatchcase(full, pattern)


def judged_ref(explicit: str | None) -> tuple[str | None, str]:
    """The ref whose required set this run judges, and how it was determined."""
    if explicit:
        return explicit, "--ref"
    base = os.environ.get("GITHUB_BASE_REF", "").strip()
    if base:
        return base, "GITHUB_BASE_REF (the pull request's base)"
    name = os.environ.get("GITHUB_REF_NAME", "").strip()
    if name:
        return name, "GITHUB_REF_NAME"
    try:
        out = subprocess.run(
            ["git", "-C", str(REPO), "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None, "undeterminable"
    if out and out != "HEAD":
        return out, "the current git branch"
    return None, "undeterminable"


# ---------------------------------------------------------------------------
# Live rulesets
# ---------------------------------------------------------------------------


def _fetch(path: str, timeout: float, token: str | None) -> object:
    req = urllib.request.Request(f"{API}{path}", headers={
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "delvewright-check-required-contexts",
    })
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=timeout) as fh:
        return json.load(fh)


def _get(path: str, timeout: float) -> object:
    """Read one endpoint, WITH a token first and anonymously second.

    A public repository's rulesets read with no credential at all, which is what
    lets this arm gate without a permission grant. But anonymous requests are
    rate limited PER IP at 60/hour, and a hosted runner's IP is shared with
    everything else on that host — so anonymous-only would be an intermittent
    red, which this project treats as a finding rather than something to re-run.
    A token raises the limit to a per-repository quota, and `GITHUB_TOKEN` is
    present in every job.

    The order is token-then-anonymous rather than one or the other, because the
    two failure modes are opposite: a token can be rate limited or scoped out of
    an endpoint anonymous access allows, and anonymous can be rate limited where
    a token is not. Trying both costs one extra request in the rare case and
    removes a class of red that is nobody's fault.
    """
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        return _fetch(path, timeout, None)
    try:
        return _fetch(path, timeout, token)
    except urllib.error.HTTPError as exc:
        if exc.code not in (401, 403, 404):
            raise
        return _fetch(path, timeout, None)


def list_branches(timeout: float) -> list[str]:
    """Every branch in the repository.

    Paginated to exhaustion rather than to a limit. A count equal to its own
    fetch limit is not a measurement, it is the limit — and truncation fakes
    coverage in the direction that reads as a clean pass, which is precisely the
    shape this file exists to catch.
    """
    names: list[str] = []
    page = 1
    per_page = 100
    while True:
        batch = _get(f"/repos/{OWNER_REPO}/branches?per_page={per_page}&page={page}", timeout)
        names.extend(b["name"] for b in batch)  # type: ignore[union-attr,index]
        if len(batch) < per_page:  # type: ignore[arg-type]
            return names
        page += 1
        if page > 100:
            raise ValueError("branch listing did not terminate within 100 pages")


def workflows_on_ref(ref: str, timeout: float) -> set[str] | None:
    """Workflow file paths present on `ref`, or None if it has no workflow dir."""
    try:
        entries = _get(
            f"/repos/{OWNER_REPO}/contents/.github/workflows?ref={urllib.parse.quote(ref, safe='')}",
            timeout,
        )
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None
        raise
    return {e["path"] for e in entries}  # type: ignore[union-attr,index]


def read_live(timeout: float) -> tuple[dict | None, str | None]:
    """(observed, None) or (None, why the comparison could not be made)."""
    try:
        repo = _get(f"/repos/{OWNER_REPO}", timeout)
        listing = _get(f"/repos/{OWNER_REPO}/rulesets", timeout)
        observed: dict[str, dict] = {}
        for entry in listing:  # type: ignore[union-attr]
            if entry.get("target") != "branch":
                continue
            full = _get(f"/repos/{OWNER_REPO}/rulesets/{entry['id']}", timeout)
            rules = full.get("rules", [])  # type: ignore[union-attr]
            checks = [r for r in rules if r.get("type") == "required_status_checks"]
            if not checks:
                # Out of scope: a branch ruleset carrying no status-check rule
                # decides nothing this file is about.
                continue
            params = checks[0].get("parameters", {})
            observed[full["name"]] = {  # type: ignore[index]
                "id": full["id"],  # type: ignore[index]
                "enforcement": full.get("enforcement"),  # type: ignore[union-attr]
                "include": list(full.get("conditions", {}).get("ref_name", {}).get("include", [])),  # type: ignore[union-attr]
                "contexts": sorted(
                    c.get("context", "") for c in params.get("required_status_checks", [])
                ),
                "strict": params.get("strict_required_status_checks_policy"),
            }
        return {"default_branch": repo.get("default_branch"), "rulesets": observed}, None  # type: ignore[union-attr]
    except urllib.error.HTTPError as exc:
        # A rate-limited 403 is a different problem from a missing repository or
        # a scoped-out token, and it is the one an operator can act on. Naming it
        # is what keeps this from reading as mysterious flakiness — which is how
        # an intermittent red gets re-run instead of root-caused.
        remaining = exc.headers.get("X-GitHub-RateLimit-Remaining") or exc.headers.get("X-RateLimit-Remaining")
        if exc.code == 403 and remaining == "0":
            reset = exc.headers.get("X-RateLimit-Reset", "?")
            return None, (
                f"the GitHub API rate limit is exhausted (HTTP 403, resets at "
                f"unix {reset}). Anonymous reads are limited per IP; set "
                f"GITHUB_TOKEN so the request is charged to a per-repository "
                f"quota instead"
            )
        return None, f"HTTP {exc.code} from {exc.url}"
    except urllib.error.URLError as exc:
        return None, f"the GitHub API is unreachable ({exc.reason})"
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return None, f"{type(exc).__name__}: {exc}"


# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument(
        "--offline", action="store_true",
        help="skip the live ruleset comparison and say so, loudly. The default "
             "is to make it, because dropping a guarantee should require adding "
             "a flag a reviewer can see, not removing one nobody notices.",
    )
    ap.add_argument("--ref", default=None, help="the ref whose required set to judge")
    ap.add_argument("--timeout", type=float, default=20.0)
    args = ap.parse_args()

    if not MANIFEST.is_file():
        print(f"check-required-contexts: FAIL — no declaration at {MANIFEST}", file=sys.stderr)
        return 1
    if not WORKFLOW_DIR.is_dir():
        print(f"check-required-contexts: FAIL — no {WORKFLOW_DIR}", file=sys.stderr)
        return 1

    with MANIFEST.open("rb") as fh:
        decl = tomllib.load(fh)

    default_branch = decl.get("default_branch")
    rulesets = decl.get("ruleset", [])
    advisory = decl.get("advisory", {})
    max_advisory = decl.get("max_advisory")
    if not default_branch or not rulesets or max_advisory is None:
        print(
            "check-required-contexts: FAIL — the declaration is missing "
            "`default_branch`, `[[ruleset]]`, or `max_advisory`",
            file=sys.stderr,
        )
        return 1

    findings: list[str] = []
    notes: list[str] = []

    # --- parse every workflow in this tree ---------------------------------
    workflows = sorted(
        list(WORKFLOW_DIR.glob("*.yml")) + list(WORKFLOW_DIR.glob("*.yaml"))
    )
    parsed = [Workflow(p) for p in workflows]
    for wf in parsed:
        findings.extend(wf.errors)

    # job context name -> (workflow, attrs)
    jobs: dict[str, tuple[Workflow, dict]] = {}
    for wf in parsed:
        for key, attrs in wf.jobs.items():
            name = str(attrs["name"])
            if name in jobs:
                findings.append(
                    f"two jobs produce the same status context {name!r} "
                    f"({jobs[name][0].rel} and {wf.rel}). A required context that "
                    f"two jobs report is satisfied by whichever reports last."
                )
            jobs[name] = (wf, attrs)

    # Vacuity: parsing nothing is not a pass.
    if not workflows:
        findings.append("no workflow files found; this checker examined nothing")
    if not jobs and not any(wf.errors for wf in parsed):
        findings.append(
            "parsed 0 job names from .github/workflows; the `  <job>:` / "
            "`    name:` shape this reader keys off has changed"
        )

    required_anywhere: set[str] = set()
    for rs in rulesets:
        required_anywhere.update(rs.get("contexts", []))
    if not required_anywhere:
        findings.append("the declaration names 0 required contexts; every gate would be advisory")

    # --- ARM A: coverage ---------------------------------------------------
    for name in sorted(jobs):
        if name in required_anywhere or name in advisory:
            continue
        findings.append(
            f"job {name!r} ({jobs[name][0].rel}) is required by no ruleset and is "
            f"not declared advisory.\n"
            f"    It runs and it gates nothing — its red is a colour on a page. "
            f"Add it to a `[[ruleset]]`'s `contexts` in "
            f"{MANIFEST.name} AND to that ruleset on GitHub, or declare it under "
            f"`[advisory.\"{name}\"]` with a `because` this checker can evaluate."
        )

    # --- advisory hygiene --------------------------------------------------
    if len(advisory) > max_advisory:
        findings.append(
            f"{len(advisory)} advisory jobs are declared and the budget is "
            f"{max_advisory}: {', '.join(sorted(advisory))}.\n"
            f"    Make the new one required, or raise `max_advisory` in "
            f"{MANIFEST.name} and say in the same diff why this repository now "
            f"needs another gate nobody has to obey."
        )
    for name, entry in sorted(advisory.items()):
        because = entry.get("because")
        wf_rel = entry.get("workflow")
        if because not in ADVISORY_REASONS:
            findings.append(
                f"advisory job {name!r} gives reason {because!r}, which this "
                f"checker cannot evaluate. Allowed: {', '.join(sorted(ADVISORY_REASONS))}.\n"
                f"    A reason that cannot be evaluated cannot be retired, which "
                f"is a free-text hatch wearing an enum's name."
            )
            continue
        if name in required_anywhere:
            findings.append(
                f"job {name!r} is declared advisory AND required by a ruleset. "
                f"It is one or the other."
            )
        if name not in jobs:
            findings.append(
                f"advisory job {name!r} is not a job in this tree. Drop the entry "
                f"— it is holding a budget slot for a gate that does not exist."
            )
            continue
        wf = jobs[name][0]
        if wf_rel != wf.rel:
            findings.append(
                f"advisory job {name!r} says it lives in {wf_rel!r}; it is defined "
                f"in {wf.rel!r}."
            )
        filters = wf.pull_request_filters()
        if because == "no-pull-request-trigger" and filters is not None:
            findings.append(
                f"advisory job {name!r} is exempt because its workflow has no "
                f"`pull_request:` trigger — and {wf.rel} now has one. The reason "
                f"has expired.\n"
                f"    It can report on a pull request now, so it can gate one. "
                f"Promote it, or re-declare it under a reason that still holds."
            )
        if because == "pull-request-path-filtered":
            if filters is None:
                findings.append(
                    f"advisory job {name!r} is exempt because its `pull_request:` "
                    f"is path-filtered, and {wf.rel} has no `pull_request:` "
                    f"trigger at all. Re-declare it under `no-pull-request-trigger`."
                )
            elif not any(f.startswith("paths") for f in filters):
                findings.append(
                    f"advisory job {name!r} is exempt because its `pull_request:` "
                    f"is path-filtered, and that filter is gone from {wf.rel}. "
                    f"The reason has expired.\n"
                    f"    It now reports on every pull request, so requiring it "
                    f"no longer risks a deadlock. Move its line into a "
                    f"`[[ruleset]]`'s `contexts`, add the context to that ruleset "
                    f"on GitHub in the same act, and delete this entry."
                )

    # --- ARM B: resolution, on the ref being judged ------------------------
    ref, how = judged_ref(args.ref)
    if ref is None:
        findings.append(
            "the ref to judge could not be determined (no --ref, no "
            "GITHUB_BASE_REF/GITHUB_REF_NAME, no current branch), so the "
            "resolution arm did not run. This is a refusal, not a pass."
        )
        governing: list[dict] = []
    else:
        governing = [
            rs for rs in rulesets
            if any(ref_matches(p, ref, default_branch) for p in rs.get("include", []))
        ]
        if not governing:
            governing = [
                rs for rs in rulesets
                if any(ref_matches(p, default_branch, default_branch) for p in rs.get("include", []))
            ]
            notes.append(
                f"ref {ref!r} matches no declared ruleset, so nothing is required "
                f"on it; judged against the default branch's ruleset(s) as the "
                f"floor this work will eventually meet."
            )

    resolved_count = 0
    for rs in governing:
        for ctx in rs.get("contexts", []):
            resolved_count += 1
            if ctx not in jobs:
                findings.append(
                    f"context {ctx!r}, required by ruleset {rs['name']!r} on "
                    f"{ref!r}, matches no job in this tree.\n"
                    f"    A required context that never reports blocks EVERY pull "
                    f"request into that ref, including the one that would fix it. "
                    f"If a job was renamed: add the NEW context to the ruleset "
                    f"first, then merge the rename with {MANIFEST.name}, then drop "
                    f"the old context."
                )
    if ref is not None and resolved_count == 0:
        findings.append(
            f"0 contexts were resolved for ref {ref!r}. A gate that examined "
            f"nothing has proved nothing."
        )

    # Contexts required only on refs this tree does not serve are STATED.
    elsewhere = sorted(
        (ctx, rs["name"], ", ".join(rs.get("include", [])))
        for rs in rulesets
        for ctx in rs.get("contexts", [])
        if rs not in governing and ctx not in jobs
    )
    for ctx, rs_name, patterns in elsewhere:
        notes.append(
            f"context {ctx!r} is required by {rs_name!r} on {patterns} and its "
            f"job is not in this tree. Not judged here; it is judged on a pull "
            f"request into those refs, where the head checkout carries it."
        )

    # --- ARM C: eligibility ------------------------------------------------
    # Counted by DISTINCT job, not by (ruleset, context) pair: a job required by
    # both rulesets is one job, and a count that says two is a number inflated by
    # its own iteration order.
    eligibility_seen: set[str] = set()
    for rs in rulesets:
        for ctx in rs.get("contexts", []):
            if ctx not in jobs or ctx in eligibility_seen:
                continue
            eligibility_seen.add(ctx)
            wf, attrs = jobs[ctx]
            filters = wf.pull_request_filters()
            if filters is None:
                findings.append(
                    f"required context {ctx!r} is produced by {wf.rel}, which has "
                    f"no `pull_request:` trigger. It can never report on a pull "
                    f"request, so every pull request into "
                    f"{', '.join(rs.get('include', []))} blocks forever."
                )
            elif filters:
                findings.append(
                    f"required context {ctx!r} is produced by {wf.rel}, whose "
                    f"`pull_request:` carries {', '.join(filters)}.\n"
                    f"    A pull request matching none of that filter produces no "
                    f"run, so the required context never reports and the merge is "
                    f"blocked with nothing to click. This repository has already "
                    f"paid for this once. Drop the filter; a gate's own driver "
                    f"stating a binding count of zero is an honest answer, and a "
                    f"check that never ran is a silence protection cannot tell "
                    f"from a pass."
                )
            proof, why = skip_proof(attrs)
            if not proof:
                findings.append(
                    f"required context {ctx!r} ({wf.rel}) can be SKIPPED: {why}."
                )
            if attrs.get("strategy"):
                findings.append(
                    f"required context {ctx!r} ({wf.rel}) has a `strategy:`. A "
                    f"matrix job reports as `name (value)`, so the bare name will "
                    f"never report."
                )
    if required_anywhere and not eligibility_seen:
        findings.append(
            "0 required jobs were examined for eligibility; no declared context "
            "resolves to a job in this tree."
        )

    # --- `provided_by` is complete, and agrees with this tree ---------------
    for rs in rulesets:
        provided = rs.get("provided_by", {})
        for ctx in rs.get("contexts", []):
            if ctx not in provided:
                findings.append(
                    f"ruleset {rs['name']!r} requires {ctx!r} and does not say "
                    f"which workflow produces it.\n"
                    f"    Add it to `[ruleset.provided_by]`. Without it nothing "
                    f"can ask whether every ref this ruleset covers is able to "
                    f"satisfy it."
                )
            elif ctx in jobs and jobs[ctx][0].rel != provided[ctx]:
                findings.append(
                    f"ruleset {rs['name']!r} says {ctx!r} comes from "
                    f"{provided[ctx]!r}; in this tree that job is defined in "
                    f"{jobs[ctx][0].rel!r}."
                )

    # --- ARM D: live rulesets ----------------------------------------------
    live_examined = 0
    covered_refs = 0
    if args.offline:
        notes.append(
            "the LIVE ruleset comparison did not run (--offline). This run cannot "
            "see a ruleset edited in the web UI: a context added, removed, "
            "renamed, or a ruleset switched out of `active`. Re-run without "
            "--offline to make that comparison."
        )
    else:
        observed, why = read_live(args.timeout)
        if observed is None:
            findings.append(
                f"the LIVE ruleset comparison did not run: {why}.\n"
                f"    This is a refusal, not a pass — the declaration below may be "
                f"describing protection that no longer exists. A public "
                f"repository's rulesets read without any credential, so this is "
                f"normally a network problem. To get a green without this arm, "
                f"pass --offline, which says so in its output."
            )
        else:
            if observed["default_branch"] != default_branch:
                findings.append(
                    f"the declaration says the default branch is "
                    f"{default_branch!r}; the repository says "
                    f"{observed['default_branch']!r}. `~DEFAULT_BRANCH` expands to "
                    f"the second one."
                )
            live = observed["rulesets"]
            declared_names = {rs["name"] for rs in rulesets}
            for name in sorted(set(live) - declared_names):
                findings.append(
                    f"ruleset {name!r} requires "
                    f"{', '.join(live[name]['contexts']) or '(nothing)'} on "
                    f"{', '.join(live[name]['include'])} and is not declared in "
                    f"{MANIFEST.name}. Protection nobody wrote down is protection "
                    f"nobody maintains."
                )
            for rs in rulesets:
                live_examined += 1
                name = rs["name"]
                if name not in live:
                    findings.append(
                        f"ruleset {name!r} is declared to require "
                        f"{', '.join(rs.get('contexts', []))} on "
                        f"{', '.join(rs.get('include', []))}, and no such live "
                        f"ruleset carries required status checks.\n"
                        f"    The file claims a gate that does not gate."
                    )
                    continue
                obs = live[name]
                if obs["enforcement"] != "active":
                    findings.append(
                        f"ruleset {name!r} is live but its enforcement is "
                        f"{obs['enforcement']!r}, not `active`. It reports its "
                        f"verdict and merges the pull request anyway."
                    )
                if sorted(obs["include"]) != sorted(rs.get("include", [])):
                    findings.append(
                        f"ruleset {name!r} covers {obs['include']} live and "
                        f"{rs.get('include')} in {MANIFEST.name}."
                    )
                want = sorted(rs.get("contexts", []))
                got = obs["contexts"]
                if want != got:
                    missing = [c for c in want if c not in got]
                    extra = [c for c in got if c not in want]
                    detail = []
                    if missing:
                        detail.append(
                            f"declared and NOT required live: {', '.join(repr(c) for c in missing)} "
                            f"— the file claims a gate that does not gate"
                        )
                    if extra:
                        detail.append(
                            f"required live and NOT declared: {', '.join(repr(c) for c in extra)} "
                            f"— an unwritten context that will block every pull "
                            f"request if its job is ever renamed"
                        )
                    findings.append(
                        f"ruleset {name!r} disagrees with the live setting.\n    "
                        + "\n    ".join(detail)
                    )
            if live_examined == 0:
                findings.append(
                    "the live arm compared 0 rulesets. A gate that examined "
                    "nothing has proved nothing."
                )

            # --- ARM E: every ref a ruleset COVERS can satisfy it -----------
            #
            # A ruleset's include pattern is a promise about a set of branches,
            # and the set is usually larger than whoever wrote the pattern was
            # picturing. A branch inside it that does not carry the workflow
            # producing a required context is a branch NO pull request can ever
            # merge into — the deadlock, already sprung, silently, on a ref
            # nobody has opened a pull request against yet.
            #
            # Nothing else in this file can see that: the other arms judge the
            # tree they are handed, and this failure lives on refs that tree
            # knows nothing about. It is the reason arm B alone would have been
            # an existence check that only looks where someone pointed.
            try:
                branches = list_branches(args.timeout)
                for rs in rulesets:
                    provided = rs.get("provided_by", {})
                    needed = {provided[c] for c in rs.get("contexts", []) if c in provided}
                    if not needed:
                        continue
                    covered = [
                        b for b in branches
                        if any(ref_matches(p, b, default_branch) for p in rs.get("include", []))
                    ]
                    if not covered:
                        notes.append(
                            f"ruleset {rs['name']!r} covers "
                            f"{', '.join(rs.get('include', []))}, which no branch "
                            f"currently matches. It gates nothing today."
                        )
                    for branch in covered:
                        covered_refs += 1
                        present = workflows_on_ref(branch, args.timeout)
                        have = present or set()
                        missing = sorted(needed - have)
                        if not missing:
                            continue
                        blocked = sorted(
                            c for c in rs.get("contexts", [])
                            if provided.get(c) in missing
                        )
                        findings.append(
                            f"branch {branch!r} is covered by ruleset "
                            f"{rs['name']!r}, which requires "
                            f"{', '.join(repr(c) for c in blocked)} — and the "
                            f"branch does not carry "
                            f"{', '.join(missing)}.\n"
                            f"    No workflow on that ref can report those "
                            f"contexts, so EVERY pull request into it is blocked "
                            f"forever, including one that would fix it. Either "
                            f"narrow the ruleset's pattern to the refs that can "
                            f"satisfy it, or put the workflow on the branch."
                        )
            except (urllib.error.URLError, OSError, ValueError, KeyError, TypeError) as exc:
                findings.append(
                    f"the covered-ref comparison did not run "
                    f"({type(exc).__name__}: {exc}). This is a refusal, not a "
                    f"pass — a ruleset may be covering refs that cannot satisfy "
                    f"it."
                )
            if covered_refs == 0:
                findings.append(
                    "arm E examined 0 covered refs. A gate that examined nothing "
                    "has proved nothing."
                )

    # --- report ------------------------------------------------------------
    scope = (
        f"{len(jobs)} jobs in {len(workflows)} workflows; "
        f"{resolved_count} contexts required on {ref!r} ({how}); "
        f"{len(eligibility_seen)} required jobs checked for eligibility; "
        f"{len(advisory)}/{max_advisory} advisory; "
        + ("live comparison SKIPPED (--offline)" if args.offline
           else f"{live_examined} live rulesets compared over {covered_refs} covered refs")
    )

    for n in notes:
        print(f"check-required-contexts: note — {n}")

    if findings:
        print(f"\ncheck-required-contexts: {len(findings)} finding(s) — {scope}\n", file=sys.stderr)
        for f in findings:
            print(f"  {f}\n", file=sys.stderr)
        return 1

    print(f"check-required-contexts: OK — {scope}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
