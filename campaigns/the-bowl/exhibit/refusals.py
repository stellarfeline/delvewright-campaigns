#!/usr/bin/env python3
"""The Bowl's second half: the two refusals, tripped rather than described.

A refusal nobody tripped is not a demonstration, so every case here PERTURBS the
green campaign, runs the engine, and asserts the exact code came back. The
perturbation is always a copy — the campaign in the repository is never left
edited, whatever happens below.

## The cases

`DW0855` — the same document with its site plan deleted and its `areas[]`
restored. A surround rings a DECLARED extent, and the only statement of a whole
map's extent this engine has is a site plan's `region`. Two areas seated with
`areas[]` state no extent at all: they sit on the compiler's fixed 256-block
stride, so the union of what they place is mostly the void between them, and
ringing it builds a mountain range around empty space. The exhibit also builds
that same areas-only document under `horizon: void`, and prints how far apart
the compiler actually put the two rooms — which is what makes the refusal read
as obvious instead of odd.

`DW0854` — the same valley with a staircase carved up its inner slope by a
stage-7 edit. **This case does not reach its code at this engine revision**, and
the exhibit says so rather than passing. See `README.md`; the control below is
what establishes that the blocker is the edit script's area check and has
nothing to do with the staircase.

Exit 0 = every case reached its code. 1 = a case did not. 2 = could not run.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

CODE = re.compile(r"^(DW\d{4}) \[(error|warning)\]", re.M)

# The staircase: one tread per block of rise, three cells wide, each with two
# cells of air over it, starting on the gap floor just outside the region's west
# edge and climbing past a crest declared at 24 over a gap floor at y 63.
STAIR_ANCHOR = "anchor/node-mouth"
STAIR_ANCHOR_POS = (7, 64, 7)   # what the derivation places `anchor/node-mouth` at
STAIR_START = (-1, 64, 7)
STAIR_STEPS = 27


class Refusal(Exception):
    """This script could not run at all — exit 2, never a pass."""


def run(delvec: str, campaign: pathlib.Path, prefabs: pathlib.Path,
        verb: str = "validate", out: pathlib.Path | None = None) -> tuple[int, list[str], str]:
    """One engine invocation. Returns (exit status, error codes, whole output).

    The status is captured before anything is piped: a pipeline reports the
    status of its LAST stage, and this one's verdict is the engine's.
    """
    argv = [delvec, verb, str(campaign), "--prefabs", str(prefabs)]
    if verb == "build":
        if out is None:
            raise Refusal("`delvec build` needs an output directory; without one it exits 2 "
                          "on usage and reports no diagnostic at all")
        argv += ["-o", str(out)]
    done = subprocess.run(argv, capture_output=True, text=True)
    said = done.stdout + done.stderr
    codes = [m.group(1) for m in CODE.finditer(said) if m.group(2) == "error"]
    return done.returncode, codes, said


def copy_campaign(src: pathlib.Path, dst: pathlib.Path) -> pathlib.Path:
    shutil.copytree(src, dst, ignore=shutil.ignore_patterns("exhibit"))
    return dst


def edit_json(path: pathlib.Path, fn) -> None:
    doc = json.loads(path.read_text(encoding="utf-8"))
    fn(doc)
    path.write_text(json.dumps(doc, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
                    encoding="utf-8")


def make_areas_campaign(camp: pathlib.Path) -> None:
    """Delete the map documents and put `areas[]` back.

    Two rooms, two different prefabs, and every reference the plan used to
    answer moved onto the prefabs' own anchors — which is what the campaign
    would have looked like had it never had a site plan.
    """
    for name in ("site-plan.json", "layout-graph.json", "geometry-brief.json"):
        p = camp / name
        if not p.is_file():
            raise Refusal(f"{name} is not there to delete — the green campaign has changed")
        p.unlink()

    def world(d):
        d["content"]["areas"] = [
            {"id": "area/near", "name": "The Near Room", "prefab": "prefab/hello-room"},
            {"id": "area/far", "name": "The Far Room", "prefab": "prefab/keep-shrine"},
        ]
    edit_json(camp / "world.json", world)

    def npcs(d):
        n = d["content"]["npcs"][0]
        n["area"] = "area/near"
        n["anchor"] = "anchor/keeper-stand"
    edit_json(camp / "npcs.json", npcs)
    edit_json(camp / "quest-plan.json",
              lambda d: d["content"]["quests"][0].__setitem__("area", "area/near"))

    def quests(d):
        q = d["content"]["quests"][0]
        q["cast"]["npc/warden"]["at"] = "anchor/keeper-stand"
        q["objectives"][1]["anchor"] = "anchor/keeper-stand"
        q["objectives"][2]["anchor"] = "anchor/exit"
        # The prefab shuts `anchor/door` at world-load and the way to the room's
        # exit runs through it, so a forced leg crossing it is `DW0317` until
        # something the party MUST do opens it. This is the areas-only document
        # being a real campaign rather than a straw one: the refusal above has to
        # be read against a version that would otherwise have been accepted.
        q["on_objective_complete"] = {
            "obj/hear-the-warden": [{
                "type": "open-gate",
                "anchor": "anchor/door",
                "happening": {"text": "The Warden draws the bar off the door.", "verb": "opens"},
            }]
        }
    edit_json(camp / "quests.json", quests)


def stair_script(campaign_id: str) -> dict:
    ax, ay, az = STAIR_ANCHOR_POS
    sx, sy, sz = STAIR_START
    frame = {"kind": "anchor-relative", "anchor": STAIR_ANCHOR}
    tread = {"blocks": [{"block": "minecraft:stone", "weight": 3},
                        {"block": "minecraft:cobblestone", "weight": 1}]}
    edits = []
    for i in range(STAIR_STEPS):
        x, y = sx - i, sy + i
        edits += [
            {"verb": "select", "name": f"region/tread-{i:02d}",
             "shape": {"kind": "box", "frame": frame,
                       "min": [x - ax, y - ay, sz - 1 - az],
                       "max": [x - ax, y - ay, sz + 1 - az]}},
            {"verb": "fill", "region": f"region/tread-{i:02d}", "recipe": tread},
            {"verb": "select", "name": f"region/head-{i:02d}",
             "shape": {"kind": "box", "frame": frame,
                       "min": [x - ax, y + 1 - ay, sz - 1 - az],
                       "max": [x - ax, y + 2 - ay, sz + 1 - az]}},
            {"verb": "carve", "region": f"region/head-{i:02d}"},
        ]
    return {
        "campaign_id": campaign_id,
        "content": {"batches": [{
            "id": "batch/a-way-out",
            "area": "area/site",
            "note": "A staircase up the surround's inner slope: a bowl with a way out of it.",
            "edits": edits,
        }]},
        "dsl_version": "0.12.0",
        "stage": "world-edits",
    }


def empty_script(campaign_id: str, area: str) -> dict:
    return {
        "campaign_id": campaign_id,
        "content": {"batches": [{"id": "batch/a-way-out", "area": area, "edits": []}]},
        "dsl_version": "0.12.0",
        "stage": "world-edits",
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--delvec", required=True)
    ap.add_argument("--repo", required=True, help="content repository root")
    ap.add_argument("--campaign", default="campaigns/the-bowl")
    ap.add_argument("--prefabs", default="prefabs")
    ap.add_argument("--out", help="where the void build of the areas document goes")
    args = ap.parse_args()

    repo = pathlib.Path(args.repo).resolve()
    green = repo / args.campaign
    prefabs = (repo / args.prefabs).resolve()
    if not (green / "site-plan.json").is_file():
        raise Refusal(f"{green} carries no site plan — this is not the green campaign")
    cid = json.loads((green / "world.json").read_text())["campaign_id"]

    findings: list[str] = []
    work = pathlib.Path(tempfile.mkdtemp(prefix="the-bowl-refusals-"))
    try:
        # -- DW0855 ---------------------------------------------------------
        print("=== DW0855: a horizon that builds terrain, on a campaign with no map")
        camp = copy_campaign(green, work / "dw0855")
        make_areas_campaign(camp)
        print("    perturbation: site-plan.json, layout-graph.json and geometry-brief.json "
              "deleted; areas[] restored with two rooms; horizon untouched")
        status, codes, out = run(args.delvec, camp, prefabs)
        print(f"    exit {status}, error code(s): {codes or 'none'}")
        for line in out.splitlines():
            if line.startswith("DW0855"):
                print(f"    {line}")
        if codes != ["DW0855"]:
            findings.append(f"DW0855 case came back {codes}, wanted exactly ['DW0855']")

        # What the accepted version would have been. The same areas-only
        # document under a horizon that needs no map builds, and the compiler
        # says where it put the two rooms — which is the distance the refused
        # surround would have had to ring around nothing.
        edit_json(camp / "world.json", lambda d: d["content"].__setitem__("horizon", "void"))
        out_dir = pathlib.Path(args.out or (work / "void-areas")).resolve()
        if out_dir.exists():
            shutil.rmtree(out_dir)
        status, codes, _ = run(args.delvec, camp, prefabs, verb="build", out=out_dir)
        done = subprocess.CompletedProcess([], status)
        if status != 0:
            findings.append("the same areas-only document does not build under `void` either, "
                            "so the refusal above cannot be read against an accepted version")
            print(f"    the void build of the areas document exits {status}: {codes}")
        else:
            layout = json.loads((out_dir / "creator-datapack" / "layout.json").read_text())
            areas = layout.get("areas", [])
            print("    under `horizon: void` the SAME document builds, and the compiler "
                  "seats its areas at:")
            for a in areas:
                print(f"        {a['id']:<12} origin {a['origin']}  size {a['size']}  "
                      f"({a['prefab']})")
            if len(areas) == 2:
                # The rectangle the union of the areas describes, and how much of
                # it is anything at all. This is the substitute extent the refusal
                # declines to guess, measured rather than asserted.
                xs = [(a["origin"][0], a["origin"][0] + a["size"][0] - 1) for a in areas]
                zs = [(a["origin"][2], a["origin"][2] + a["size"][2] - 1) for a in areas]
                span_x = max(h for _, h in xs) - min(l for l, _ in xs) + 1
                span_z = max(h for _, h in zs) - min(l for l, _ in zs) + 1
                built = sum(a["size"][0] * a["size"][2] for a in areas)
                print(f"    the union of what `areas[]` places is {span_x} x {span_z} = "
                      f"{span_x * span_z} column(s), of which {built} carry a room — "
                      f"{100.0 * built / (span_x * span_z):.1f}% of it. That rectangle is the "
                      f"extent a surround would have had to ring, and the rest of it is nothing.")

        # -- DW0854 ---------------------------------------------------------
        print()
        print("=== DW0854: the surround's inner slope has grown a standable staircase")
        camp = copy_campaign(green, work / "dw0854")
        (camp / "world-edits.json").write_text(
            json.dumps(stair_script(cid), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(f"    perturbation: a stage-7 batch on `area/site` carving {STAIR_STEPS} treads "
              f"from the gap floor at y {STAIR_START[1]} out past the crest")
        status, codes, out = run(args.delvec, camp, prefabs, verb="build",
                                 out=work / "dw0854-out")
        print(f"    exit {status}, error code(s): {codes or 'none'}")
        for line in out.splitlines():
            if line.startswith("DW0112") or line.startswith("DW0854"):
                print(f"    {line}")
        if "DW0854" not in codes:
            findings.append(
                f"DW0854 was not reached: the build came back {codes}. A refusal nobody "
                f"tripped is not a demonstration — see README.md")

            # The control, and it is the whole reason this is a finding about the
            # engine rather than about the staircase: a batch with NO edits at
            # all, on the same campaign, is refused for the same reason.
            print()
            print("    control: the SAME batch with zero edit verbs, so nothing is carved")
            camp = copy_campaign(green, work / "dw0854-empty")
            (camp / "world-edits.json").write_text(
                json.dumps(empty_script(cid, "area/site"), indent=2, sort_keys=True) + "\n",
                encoding="utf-8")
            _, empty_codes, _ = run(args.delvec, camp, prefabs)
            print(f"        error code(s): {empty_codes or 'none'}")

            # And the other half of the control: the identical empty batch on a
            # campaign that seats its pieces with `areas[]` is accepted. So the
            # refusal is about the placement authority, not about edit scripts.
            print("    control: the same empty batch on an `areas[]` campaign under `void`")
            camp = copy_campaign(green, work / "dw0854-areas")
            make_areas_campaign(camp)
            edit_json(camp / "world.json",
                      lambda d: d["content"].__setitem__("horizon", "void"))
            (camp / "world-edits.json").write_text(
                json.dumps(empty_script(cid, "area/near"), indent=2, sort_keys=True) + "\n",
                encoding="utf-8")
            _, areas_codes, _ = run(args.delvec, camp, prefabs)
            print(f"        error code(s): {areas_codes or 'none'}")
            if empty_codes == ["DW0112"] and areas_codes == []:
                print("        so the blocker is the batch's AREA, not the staircase: a "
                      "site-plan campaign has no `areas[]` by construction (DW0839) and the "
                      "edit script's area check reads `areas[]` alone.")
            else:
                findings.append("the control did not isolate the blocker — read it by hand")
    finally:
        shutil.rmtree(work, ignore_errors=True)

    print()
    if findings:
        for f in findings:
            print(f"FINDING: {f}")
        return 1
    print("both refusals tripped, each by its own code.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Refusal as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        sys.exit(2)
