#!/usr/bin/env python3
"""CAN THIS LIBRARY STAND ON THE HORIZONS THIS ENGINE DECLARES — the CI gate.

`prefabs/` ships piece sets; a campaign seats one of them on a horizon base. The
pairing is refused before a piece is placed (`DW0886`), and until this gate
existed nothing in THIS repository asked the question: `tools/prefab-audit.py`
audits a piece's palette and its waterline, one piece at a time, and knows
nothing about pools, horizons or `shown_faces`. A library could therefore lose
its seating — or gain it — with every check here green, which is exactly the
green-gate-that-binds-to-nothing `CLAUDE.md` refuses to call a pass.

WHAT IT ASKS, AND OF WHAT. Both sides of the matrix are ENUMERATED, never typed:

  pools  — every key of `prefabs/pools.json`, the object that defines them
  bases  — every variant the pinned engine's own `delvec schema --stage world`
           exports for `HorizonBase`

so a pool added here, or a base added upstream, enters the matrix by existing.
The verdicts come from `delvec prefab seating --json`, which is the same
implementation the compiler's own validation check runs, so this gate cannot
call a library seatable that a build then refuses.

WHAT IT HOLDS THEM TO. `prefabs/seating-limits.toml` records the cells this
library is not expected to stand on, each with the codes and shapes its refusal
carries. Every other cell must be SEATABLE. Three findings, not one:

  - a cell refuses and no limit row claims it      (a regression, or a new piece)
  - a limit row's cell now stands                  (the record has gone stale)
  - a limit row's cell refuses differently         (a different defect, hidden
                                                    behind an expected refusal)

The third is the one a plain allowlist would miss, and it is why a row carries
codes and shapes rather than a boolean.

IT STATES ITS BINDING, WITH DENOMINATORS, on every run including a clean one:
cells judged over cells that exist, members examined, and `shown_faces`
declarations put in front of the engine. A run that judges zero cells fails —
a matrix with no pools or no bases is an instrument that has stopped reading its
inputs, and it would otherwise report as a pass.

Offline and stdlib-only, like every other checker here, so a creator runs
exactly what CI runs on their own clone with nothing installed.

Exit 0 = pass, 1 = a finding, 2 = the inputs or the engine are unusable.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
import tomllib

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIMITS = "prefabs/seating-limits.toml"


def die(msg: str) -> int:
    print(f"check-seating: {msg}", file=sys.stderr)
    return 2


def horizon_bases(bin_path: pathlib.Path) -> list[str]:
    """Every base the ENGINE declares, read out of its own exported schema.

    Not a constant here. A base this repository had never heard of would
    otherwise be a column the matrix silently omits, and the omission would
    look exactly like a pass.
    """
    out = subprocess.run(
        [str(bin_path), "schema", "--stage", "world"],
        capture_output=True, text=True, check=False,
    )
    if out.returncode != 0:
        raise RuntimeError(f"`delvec schema --stage world` exited {out.returncode}")
    schema = json.loads(out.stdout)
    defs = schema.get("$defs") or schema.get("definitions") or {}
    base = defs.get("HorizonBase")
    if not base:
        raise RuntimeError("the exported world schema declares no `HorizonBase`")
    names = [v["const"] for v in base.get("oneOf", []) if "const" in v]
    if not names:
        raise RuntimeError("`HorizonBase` exports no variants")
    return sorted(names)


def seating(bin_path: pathlib.Path, prefabs: pathlib.Path, base: str) -> dict:
    """One `delvec prefab seating` run, as JSON.

    Its exit status is deliberately NOT read as the verdict: a refused pool is
    an expected state here, and what this gate compares is the per-pool answer.
    A run that produces no parsable object is the failure that matters.
    """
    out = subprocess.run(
        [str(bin_path), "--prefabs", str(prefabs), "--json",
         "prefab", "seating", "--horizon", base],
        capture_output=True, text=True, check=False,
    )
    obj = None
    for line in out.stdout.splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        cand = json.loads(line)
        if cand.get("check") == "seating":
            obj = cand
    if obj is None:
        raise RuntimeError(
            f"`prefab seating --horizon {base}` printed no seating object "
            f"(exit {out.returncode}); stderr: {out.stderr.strip()[:400]}"
        )
    return obj


def declarations(prefabs: pathlib.Path, pools: dict) -> tuple[int, int]:
    """`shown_faces` entries the engine is handed, and the member slots they sit on.

    Computed from the objects — the pool membership and each member's own
    document — so it is the denominator the seating check's declared-face arm
    quantifies over, not a number somebody wrote down.
    """
    decls = 0
    slots = 0
    for spec in pools.values():
        ids = sorted({m["prefab"] for m in spec.get("members", [])})
        slots += len(ids)
        for pid in ids:
            doc = prefabs / (pid.split("/", 1)[-1] + ".json")
            if not doc.exists():
                continue
            decls += len(json.loads(doc.read_text()).get("shown_faces", []))
    return decls, slots


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--bin", required=True, help="the pinned `delvec` to judge with")
    ap.add_argument("--prefabs", default=str(ROOT / "prefabs"),
                    help="the prefab library to judge (default: this repo's)")
    args = ap.parse_args()

    bin_path = pathlib.Path(args.bin).resolve()
    prefabs = pathlib.Path(args.prefabs).resolve()
    if not bin_path.exists():
        return die(f"no engine binary at {bin_path}")
    pools_file = prefabs / "pools.json"
    if not pools_file.exists():
        return die(f"no {pools_file}")

    pools = json.loads(pools_file.read_text())["pools"]
    limits_path = ROOT / LIMITS
    if not limits_path.exists():
        return die(f"no {LIMITS} — the record of which cells are expected to refuse")
    limits_doc = tomllib.loads(limits_path.read_text())
    limits = {(r["pool"], r["base"]): r for r in limits_doc.get("limit", [])}

    version = subprocess.run([str(bin_path), "--version"],
                             capture_output=True, text=True, check=False).stdout.strip()
    print(f"== seating — library {prefabs}, judged by {version} ==")

    try:
        bases = horizon_bases(bin_path)
    except Exception as exc:  # noqa: BLE001 — any failure here is an unusable instrument
        return die(str(exc))

    findings: list[str] = []

    # A limit row naming a cell the matrix does not contain is a stale record,
    # and it would otherwise sit here forever claiming to excuse something.
    for pool, base in sorted(limits):
        if pool not in pools:
            findings.append(f"{LIMITS} records a limit for `{pool}`, which this library has no pool for")
        if base not in bases:
            findings.append(f"{LIMITS} records a limit on base `{base}`, which this engine does not declare")

    judged = 0
    members_seen = 0
    for base in bases:
        try:
            obj = seating(bin_path, prefabs, base)
        except Exception as exc:  # noqa: BLE001
            return die(str(exc))
        seen = {p["pool"]: p for p in obj.get("pools", [])}
        # The instrument must have read the same library this gate enumerated.
        missing = sorted(set(pools) - set(seen))
        if missing:
            findings.append(
                f"base `{base}`: the engine reported no verdict for {len(missing)} pool(s) "
                f"this library declares: {', '.join(missing)}"
            )
        for pool in sorted(pools):
            p = seen.get(pool)
            if p is None:
                continue
            judged += 1
            members_seen += p["members"]
            codes = sorted({r["code"] for r in p["reasons"]})
            shapes = sorted({r["shape"] for r in p["reasons"]})
            row = limits.get((pool, base))
            stands = p["verdict"] == "SEATABLE"
            if stands and row is None:
                print(f"  ok   {pool:<22} {base:<7} stands ({p['members_seatable']}/{p['members']} member(s))")
            elif stands and row is not None:
                findings.append(
                    f"`{pool}` now STANDS on `{base}`, and {LIMITS} still records it as a limit. "
                    f"Delete that row — the record is what says a refusal is deliberate, and one "
                    f"that has stopped being true excuses a future refusal nobody chose"
                )
            elif not stands and row is None:
                findings.append(
                    f"`{pool}` is REFUSED on `{base}` and no row of {LIMITS} claims it "
                    f"({p['members_seatable']}/{p['members']} member(s) seatable; {', '.join(codes) or 'no code'}; "
                    f"{', '.join(shapes) or 'no shape'}). Either the pieces regressed, or this is a "
                    f"deliberate limit and owes a row saying so with its reason"
                )
            else:
                want_c, want_s = sorted(row.get("codes", [])), sorted(row.get("shapes", []))
                if codes != want_c or shapes != want_s:
                    findings.append(
                        f"`{pool}` is REFUSED on `{base}` for a different reason than "
                        f"{LIMITS} records: codes {codes} against {want_c}, shapes {shapes} "
                        f"against {want_s}. An expected refusal is not a place to hide a new one"
                    )
                else:
                    print(f"  ---  {pool:<22} {base:<7} refused as recorded ({', '.join(shapes)})")

    decls, slots = declarations(prefabs, pools)
    cells = len(pools) * len(bases)
    print(
        f"-- binding: {judged} cell(s) judged of {cells} that exist "
        f"({len(pools)} pool(s) in prefabs/pools.json x {len(bases)} base(s) the engine exports: "
        f"{', '.join(bases)}); {members_seen} member verdict(s) read over {slots} member slot(s); "
        f"{decls} `shown_faces` declaration(s) put in front of the engine; "
        f"{len(limits)} recorded limit(s)"
    )

    if judged == 0:
        findings.append(
            f"ZERO cells judged, over {len(pools)} pool(s) and {len(bases)} base(s). "
            f"A matrix with nothing in it is an instrument that has stopped reading its inputs"
        )

    if findings:
        print()
        for f in findings:
            print(f"  FAIL {f}")
        print(f"\ncheck-seating: {len(findings)} finding(s)")
        return 1
    print("check-seating: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
