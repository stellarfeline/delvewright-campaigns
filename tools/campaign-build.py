#!/usr/bin/env python3
"""Every campaign in this repository compiles, and the count says against what.

A campaign nothing compiles is a campaign nothing checks. The other workflows
here audit pieces, lint workflows, and ship a release from a tag; none of them
ever built a campaign, so a compiler obligation that arrived after a campaign was
authored reached nobody.

## Why the whole check lives here rather than in the workflow

Two reasons, and the second is the one that decided the shape.

Every validation must be runnable on the creator's own machine, so the check is
one command with nothing installed beyond the engine binary it is handed. A check
only we can run is not a check the product has.

And the job that runs it has to be a REQUIRED status check, which branch
protection matches by NAME STRING. A matrix job reports as `name (value)`, so its
context appears and vanishes as campaigns land and could never be required; a
summary job over such a matrix needs `if: always()` to survive a failing leg, and
a job-level `if:` is itself disqualifying, because a skipped job reports
`skipped` and GitHub counts that as a SATISFIED required check. Neither shape can
be held. One job with a fixed name walking the population itself can, and it is
the shape `prefab-audit.yml` next door already uses for the same reason. The
parallelism that costs is worth less than a gate that can gate.

## What it refuses, and why each refusal cannot be produced by the defect

A GATE THAT BINDS TO NOTHING is not a pass. An empty population means the
discovery rule broke, not that the repository is clean, so zero campaigns is a
refusal rather than a silent success.

AN EXCLUSION IS COUNTED. The population is every directory under `campaigns/`
holding a `world.json` — `release.yml` states the same rule in its own words,
having already met a directory here that was media and build output and no
campaign. That rule is an EXCLUSION, and an exclusion nobody counts is how a
count stays honest about a smaller world than the tool claims to cover: this
repository has already paid for that, when a constant naming directories to skip
removed 27 tracked files, every campaign stage document among them, from a tool's
enumeration while every stated number remained truthful about what it had been
handed. So the excluded set is named, and the kind is decided by the object
rather than by whoever wrote the directory — a directory carrying no stage
document at all is media, and one carrying any OTHER stage document is a campaign
that has lost its entry document and is a refusal. The innocent case cannot
present the second proof.

A CAMPAIGN OUTSIDE `campaigns/` IS A CAMPAIGN THIS GATE WOULD NEVER SEE.
Discovery reads one directory, so a campaign authored anywhere else — under
`demos/`, beside a prefab, at the root — is not a smaller population, it is an
invisible one, and the binding count would go on being truthful about a world
that no longer contains it. That is the same defect the excluded set above
exists for, one directory further out. So the walk also enumerates the
repository's TRACKED files and refuses any stage document outside
`campaigns/`, naming the directory. Tracked, because the rule is about content
somebody committed: a build tree is untracked by construction, so the
population needs no exclusion list and cannot acquire one that drifts.
`demos/` is not the exception — it holds demonstrations of a generation-time
surface (a grammar program, the piece it exports, its reports, its refusal
transcripts), which carry no stage document because no delve is built from
them. A demo LEVEL is a campaign and lives in `campaigns/` like any other.

A CAMPAIGN STOPPED AT THE DESIGN GATE IS NOT A BUILD FAILURE, AND THE BRANCH IS
WHAT SAYS SO. Three things live in this repository and only two of them owe a
green build: a campaign on `main` must build; a demo owes nothing because it is
not a campaign; and a campaign still being authored does not build yet, because
`/new-delve` stops at the design gate with `quests.json` and `dialogue.json`
unwritten and the compiler is right to refuse it. An in-progress campaign lives
on its own `campaign/<id>` branch and reaches `main` once, after acceptance, so
the BRANCH NAME is what tells the three apart — not a field in the campaign, and
not a list in this file. `--branch campaign/<id>` therefore reports that one
campaign's findings without counting them, and every other campaign in the tree
still must build.

`--branch` is the ref this run's result LANDS ON — a pull request's base, or the
branch being pushed — and not the head it came from. Those differ at exactly the
moment that matters: the acceptance pull request from `campaign/<id>` into
`main` has that head and that base, and it is the one run where the campaign
must build. Reading the head would excuse the merge that ships it.

That hatch is shaped so it cannot become habit, and so the defect cannot supply
it. It excuses exactly ONE campaign, named by the branch rather than chosen; a
`campaign/<id>` branch naming a campaign this tree does not carry is a refusal,
not a free pass; absent `--branch` nothing is excused at all; and merging to
`main` removes the branch and with it the excuse. Every run prints what it
excused and what that campaign's findings were, so an excused red is read, never
hidden.

EVERY DISCOVERED CAMPAIGN IS ACCOUNTED FOR AT THE END. The population is fixed
before the walk and reconciled against the RESULTS after it, in a `finally`, so a
walk that stopped early cannot report on the part it reached and stay silent
about the part it did not. Truncation fakes coverage, and it fakes it in the
direction that reads as a clean pass — a `cargo test` that halted at 21 of 175
binaries is the recorded instance. A campaign with no result is a red naming it,
whether the walk crashed, was interrupted, or simply never got there.

Exit 0 = every campaign built in every language it declares. 1 = a finding.
2 = this tool could not run at all, which is a refusal and not a pass.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys

# Every document a campaign is authored out of. A directory carrying one of these
# is a campaign whatever else is true of it — which is what tells a campaign that
# has lost its entry document apart from a directory that never was one.
STAGE_DOCUMENTS = (
    "world.json",
    "quest-plan.json",
    "quests.json",
    "npcs.json",
    "classes.json",
    "dialogue.json",
    "world-edits.json",
)

# The entry document. Its presence is what makes a directory a campaign, and the
# rule is shared with `release.yml` so the two cannot disagree about what a
# campaign is.
ENTRY_DOCUMENT = "world.json"

CAMPAIGN_ROOT = "campaigns"

# The branch an in-progress campaign lives on. `campaign/<id>` names the one
# campaign that has not reached `main` yet, which is the only thing that excuses
# a campaign from building — see the header. The id is the rest of the name, so
# the branch cannot excuse a campaign it does not name.
IN_PROGRESS_PREFIX = "campaign/"


class Refusal(Exception):
    """The tool cannot run at all — exit 2, never a pass."""


def discover(root: pathlib.Path) -> tuple[list[str], list[dict], list[dict]]:
    """(campaigns, excluded-as-media, excluded-as-headless).

    Sorted, so the walk order is the same on every machine and in every run.
    """
    base = root / CAMPAIGN_ROOT
    if not base.is_dir():
        raise Refusal(
            f"{CAMPAIGN_ROOT}/ is not a directory in {root}. This tool is run "
            f"from the root of the content repository."
        )
    campaigns: list[str] = []
    media: list[dict] = []
    headless: list[dict] = []
    for path in sorted(base.iterdir()):
        if not path.is_dir():
            continue
        if (path / ENTRY_DOCUMENT).is_file():
            campaigns.append(path.name)
            continue
        carries = [s for s in STAGE_DOCUMENTS if (path / s).is_file()]
        (headless if carries else media).append(
            {"dir": path.name, "carries": carries}
        )
    return campaigns, media, headless


def tracked(root: pathlib.Path) -> list[str]:
    """Every file git tracks here, sorted. A Refusal when this is not a checkout.

    The population for the misplacement scan below. It is git's answer and not a
    directory walk because the rule is about committed content: a build tree, a
    virtualenv and a draft image directory are untracked by construction, so this
    population needs no exclusion list — and an exclusion list is the thing that
    drifts, silently, in the direction of covering less than it claims.
    """
    proc = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z"],
        capture_output=True,
    )
    if proc.returncode != 0:
        raise Refusal(
            f"`git ls-files` failed in {root}: "
            f"{proc.stderr.decode('utf-8', 'replace').strip()}. This gate reads "
            f"the tracked file list to find a campaign authored outside "
            f"{CAMPAIGN_ROOT}/, and a scan that cannot run is a refusal, never a "
            f"pass."
        )
    return sorted(
        p for p in proc.stdout.decode("utf-8", "replace").split("\0") if p
    )


def misplaced(paths: list[str]) -> list[dict]:
    """Directories outside `campaigns/` that hold a campaign stage document.

    Sorted, so the finding order is the same on every machine. A campaign here is
    not a campaign with a problem — it is a campaign this gate's discovery cannot
    see at all, which is why it is a finding about the tree rather than a row in
    the population.
    """
    carried: dict[str, list[str]] = {}
    for path in paths:
        parts = path.split("/")
        if parts[0] == CAMPAIGN_ROOT:
            continue
        if parts[-1] not in STAGE_DOCUMENTS:
            continue
        carried.setdefault("/".join(parts[:-1]) or ".", []).append(parts[-1])
    return [
        {"dir": d, "carries": sorted(carried[d])} for d in sorted(carried)
    ]


def in_progress_campaign(branch: str | None, population: list[str]) -> str | None:
    """The one campaign a `campaign/<id>` branch excuses. None on any other ref.

    Raises `Refusal` when the branch names a campaign this tree does not carry:
    the branch is a claim about what is being authored here, and a claim about a
    campaign that is not present excuses nothing and would hide the next real
    one. That is the property the defect cannot supply — an excuse has to name a
    campaign the walk also discovered.
    """
    if not branch or not branch.startswith(IN_PROGRESS_PREFIX):
        return None
    name = branch[len(IN_PROGRESS_PREFIX):]
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise Refusal(
            f"--branch {branch} is not `{IN_PROGRESS_PREFIX}<campaign-id>`: "
            f"{name!r} is not a campaign id. A branch that excuses a build has "
            f"to name the campaign it is excusing."
        )
    if name not in population:
        raise Refusal(
            f"--branch {branch} says campaign `{name}` is in progress here, and "
            f"the walk discovered {', '.join(population) or '(none)'}. A branch "
            f"naming a campaign this tree does not carry excuses nothing and "
            f"would hide the next campaign that does go red."
        )
    return name


def languages_of(root: pathlib.Path, campaign: str) -> list[str]:
    """English plus every language the campaign declares.

    An emission defect can be language-specific, and a localized build is what a
    playtest is run on, so a campaign is not built until every language it
    declares is built.
    """
    doc = root / CAMPAIGN_ROOT / campaign / ENTRY_DOCUMENT
    try:
        world = json.loads(doc.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise Refusal(f"{doc} cannot be read as JSON: {exc}") from exc
    declared = world.get("content", {}).get("languages", [])
    if not isinstance(declared, list):
        raise Refusal(f"{doc} declares `content.languages` that is not a list")
    out = ["en"]
    for lang in declared:
        if lang not in out:
            out.append(lang)
    return out


def run(argv: list[str], root: pathlib.Path) -> bool:
    """Run one engine invocation, streaming its output. True when it succeeded."""
    print(f"    $ {' '.join(argv)}", flush=True)
    completed = subprocess.run(argv, cwd=root)
    return completed.returncode == 0


def build_campaign(
    delvec: str,
    root: pathlib.Path,
    campaign: str,
    prefabs: str,
    out_dir: pathlib.Path,
) -> list[str]:
    """Validate, then build every declared language. Returns this campaign's errors.

    Both ladder stages, in order: `validate` is schema, referential, text fit and
    l10n sidecar coverage and is language-independent, so it runs once; `build`
    is the full deterministic emission and runs per language. A language that
    fails does not stop the others — one red language must not hide the state of
    the rest.
    """
    errors: list[str] = []
    campaign_path = f"{CAMPAIGN_ROOT}/{campaign}"
    print(f"--- {campaign}: validate", flush=True)
    if not run([delvec, "validate", campaign_path, "--prefabs", prefabs], root):
        errors.append(f"{campaign} does not validate")
        # A campaign that fails validation is still built below: `build` reports
        # placement and emission findings that `validate` never reaches, and a
        # round that stopped here would learn one obligation per run.
    for lang in languages_of(root, campaign):
        print(f"--- {campaign}: build --lang {lang}", flush=True)
        target = out_dir / f"delve-{campaign}-{lang}"
        if not run(
            [
                delvec, "build", campaign_path,
                "-o", str(target),
                "--prefabs", prefabs,
                "--lang", lang,
            ],
            root,
        ):
            errors.append(f"{campaign} does not build at --lang {lang}")
    return errors


def reconcile(population: list[str], reached: list[str]) -> list[str]:
    """Every discovered campaign has a result. A pure function over both sets.

    This is the accounting that a truncated walk cannot satisfy. It is separate
    from the walk on purpose: the walk can be stopped by anything at all — an
    exception, an interrupt, a bug in this file — and the reconciliation still
    runs, because a walk is not entitled to report on the part it reached and
    stay silent about the part it did not.
    """
    errors: list[str] = []
    missing = [c for c in population if c not in reached]
    if missing:
        errors.append(
            f"the walk discovered {len(population)} campaign(s) and produced a "
            f"result for {len(reached)}: {', '.join(missing)} was never "
            f"examined. A run that stops early and reports on what it reached is "
            f"truncation faking coverage, and it fakes it in the direction that "
            f"reads as a clean pass"
        )
    unknown = [c for c in reached if c not in population]
    if unknown:
        errors.append(
            f"a result was produced for {', '.join(unknown)}, which the "
            f"discovery did not name. The walk and the population disagree about "
            f"what this gate examined"
        )
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--delvec", help="the engine binary to build with")
    parser.add_argument("--root", default=".", help="the repository root")
    parser.add_argument("--prefabs", default="prefabs")
    parser.add_argument("--out", help="where built delves are written")
    parser.add_argument(
        "--branch",
        help=(
            "the branch this run's result lands on — a pull request's BASE, or "
            "the branch being pushed. A `campaign/<id>` branch is where an "
            "in-progress campaign lives, so that one campaign's findings are "
            "reported and not counted; every other campaign still must build. "
            "Absent, nothing is excused."
        ),
    )
    parser.add_argument(
        "--discover-only",
        action="store_true",
        help="state the population and its exclusions without building anything",
    )
    parser.add_argument(
        "--github",
        action="store_true",
        help="emit findings as GitHub workflow error annotations",
    )
    args = parser.parse_args(argv)

    root = pathlib.Path(args.root).resolve()
    errors: list[str] = []

    try:
        population, media, headless = discover(root)
        stray = misplaced(tracked(root))
        excused = in_progress_campaign(args.branch, population)
    except Refusal as exc:
        print(f"campaign-build: FATAL — {exc}", file=sys.stderr)
        return 2

    print(f"discovered {len(population)} campaign(s): "
          f"{', '.join(population) or '(none)'}")
    print(f"excluded {len(media) + len(headless)} directory/ies holding no "
          f"{ENTRY_DOCUMENT}: "
          f"{', '.join(d['dir'] for d in media + headless) or '(none)'}")
    if excused:
        print(
            f"in progress on {args.branch}: {excused} — its findings are "
            f"reported below and not counted. Every other campaign must build."
        )

    # An exclusion that cannot be innocent. A media directory has no stage
    # document to present, so this refusal is one the defect cannot supply.
    for entry in headless:
        errors.append(
            f"{CAMPAIGN_ROOT}/{entry['dir']} carries "
            f"{', '.join(entry['carries'])} but no {ENTRY_DOCUMENT}, so it is a "
            f"campaign this gate would drop while still reporting a binding "
            f"count — an honest number about a smaller world than it claims to "
            f"cover"
        )

    # A campaign outside `campaigns/` is not a smaller population — it is one
    # this gate's discovery cannot see, so the count above would stay truthful
    # about a world that no longer holds it. `demos/` is the directory this
    # actually guards: it holds demonstrations of a generation-time surface,
    # which carry no stage document, and a demo LEVEL is a campaign that belongs
    # in `campaigns/` like any other.
    for entry in stray:
        errors.append(
            f"{entry['dir']} carries {', '.join(entry['carries'])}, which is a "
            f"campaign stage document outside {CAMPAIGN_ROOT}/. Discovery reads "
            f"{CAMPAIGN_ROOT}/ and nothing else, so nothing here would ever "
            f"compile it and the binding count above would go on being honest "
            f"about a world that no longer contains it. A campaign — a demo "
            f"level included — lives at {CAMPAIGN_ROOT}/<id>/"
        )

    # A gate that binds to nothing is vacuous, not a pass.
    if not population:
        errors.append(
            f"no campaign found under {CAMPAIGN_ROOT}/ (a campaign is a "
            f"directory holding {ENTRY_DOCUMENT}), so this gate would examine "
            f"nothing. A zero binding is a finding"
        )

    reached: list[str] = []
    if population and not args.discover_only:
        if not args.delvec:
            print("campaign-build: FATAL — --delvec is required unless "
                  "--discover-only", file=sys.stderr)
            return 2
        out_dir = pathlib.Path(args.out).resolve() if args.out else root / ".build"
        out_dir.mkdir(parents=True, exist_ok=True)
        try:
            for campaign in population:
                found = build_campaign(
                    args.delvec, root, campaign, args.prefabs, out_dir
                )
                if campaign == excused:
                    # Printed, never counted, and never silent: an excused red is
                    # a campaign somebody is still authoring, and the reader of
                    # this run is entitled to see exactly what it was.
                    for message in found:
                        print(
                            f"in progress ({args.branch}), not counted: "
                            f"{message}"
                        )
                    if not found:
                        print(
                            f"in progress ({args.branch}), not counted: "
                            f"{campaign} already builds clean"
                        )
                else:
                    errors += found
                # Recorded only once the campaign is finished, so a campaign the
                # walk began and did not complete is as unaccounted-for as one it
                # never began.
                reached.append(campaign)
        except Exception as exc:  # noqa: BLE001 — see below
            # Deliberately every exception. The accounting below is worthless if
            # an abort carries it away before anyone reads it: a `finally` that
            # computes a finding the propagating exception then discards is the
            # shape where a check runs and its answer is never read. So the crash
            # becomes a finding beside the reconciliation rather than instead of
            # it, and the run still reports what it did and did not examine.
            errors.append(
                f"the walk stopped on an unhandled "
                f"{type(exc).__name__}: {exc}. What follows is the accounting "
                f"for the campaigns it had reached, which is the part a crash "
                f"would otherwise take with it"
            )
        finally:
            errors += reconcile(population, reached)

    for message in errors:
        print(f"::error::{message}" if args.github else f"error: {message}")

    # The binding count, with the denominator it was measured against. A count
    # with no denominator is the shape that stayed honest while covering a
    # smaller world than the tool claimed.
    #
    # The two modes report in different words on purpose. `--discover-only`
    # builds nothing, so saying "0 of 2 campaigns examined" beside an exit 0
    # would be a shortfall reported as a pass — the precise reading this gate
    # refuses everywhere else, arriving through its own summary line. It says
    # what it is instead, and never borrows the verdict shape.
    excluded = len(media) + len(headless)
    scanned = len(tracked(root))
    if excused:
        excuse = (
            f"1 campaign ({excused}) in progress on {args.branch} and not counted"
        )
    else:
        excuse = "no campaign excused"
    scope = (
        f"{len(stray)} stage document site(s) outside {CAMPAIGN_ROOT}/ over "
        f"{scanned} tracked file(s), {excuse}"
    )
    if args.discover_only:
        print(
            f"campaign build gate: DISCOVERY ONLY — {len(population)} "
            f"campaign(s) discovered, {excluded} directory/ies excluded and "
            f"named, {scope}, {len(errors)} finding(s). Nothing was built, so "
            f"this is a report on the population and not a verdict on whether it "
            f"compiles."
        )
    else:
        languages = sum(len(languages_of(root, c)) for c in reached)
        print(
            f"campaign build gate: {len(reached)} of {len(population)} "
            f"campaign(s) examined, {languages} language build(s), "
            f"{excluded} directory/ies excluded and named, {scope}, "
            f"{len(errors)} finding(s)"
        )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
