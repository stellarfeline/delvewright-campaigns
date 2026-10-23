#!/usr/bin/env python3
"""Put every refused shape of The Hearth Door through the engine.

    python3 campaigns/the-hearth-door/design/check_probes.py <delvec> <prefabs-dir> <scratch-dir>

Each `probes/<name>.json` is the campaign plus one declared edit: `documents`
(JSON-pointer edits to a stage document) or `put` (cells a place's builder in
`build_pieces.py` lays differently, after which the place is detailed again).
Each must be refused by `delvec build` with the code it names, as the first
diagnostic the build reports. Prints one line per probe and a binding line; any
probe not refused with its code, or no probe at all, exits 1.
"""
import importlib.util
import json
import pathlib
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
CAMPAIGN = HERE.parent


def pointer(doc, path):
    parts = [p.replace("~1", "/").replace("~0", "~") for p in path.split("/")[1:]]
    node = doc
    for p in parts[:-1]:
        node = node[int(p)] if isinstance(node, list) else node[p]
    return node, parts[-1]


def apply(doc, op):
    parent, key = pointer(doc, op["path"])
    if isinstance(parent, list):
        key = len(parent) if key == "-" else int(key)
    if op["op"] == "remove":
        del parent[key]
    elif op["op"] == "replace":
        parent[key] = op["value"]
    elif op["op"] == "add":
        if isinstance(parent, list):
            parent.insert(key, op["value"])
        else:
            parent[key] = op["value"]


def first_code(out):
    for line in out.splitlines():
        line = line.strip()
        if line.startswith("{"):
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            if d.get("severity") == "error" and d.get("code"):
                return d["code"]
    return None


def main():
    delvec, prefabs, scratch = map(pathlib.Path, sys.argv[1:4])
    probes = sorted((HERE / "probes").glob("*.json"))
    if not probes:
        sys.exit("no probe under design/probes")
    spec = importlib.util.spec_from_file_location("build_pieces", HERE / "build_pieces.py")
    pieces = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pieces)
    refused = 0
    for path in probes:
        probe = json.loads(path.read_text())
        name = path.stem
        camp = scratch / name / "campaign"
        lib = scratch / name / "prefabs"
        shutil.rmtree(scratch / name, ignore_errors=True)
        shutil.copytree(CAMPAIGN, camp)
        shutil.copytree(prefabs, lib)
        for op in probe.get("documents", []):
            p = camp / op["doc"]
            doc = json.loads(p.read_text())
            apply(doc, op)
            p.write_text(json.dumps(doc, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
        if probe.get("put"):
            alloc = subprocess.run([str(delvec), "allocation", str(camp), "--all", "--prefabs", str(lib)],
                                   capture_output=True, text=True, check=True)
            places = {a["place"]: a for a in json.loads(alloc.stdout)}
            for put in probe["put"]:
                stem = put["place"].split("/", 1)[1]
                builder = getattr(pieces, stem)
                original = pieces.program

                def program(n, piece, palette, contract, marks, put=put):
                    piece.put(tuple(put["lo"]), tuple(put["hi"]), put["role"])
                    if put.get("claim"):
                        piece.claim_box(tuple(put["lo"]), tuple(put["hi"]), put["claim"])
                    return original(n, piece, palette, contract, marks)

                pieces.program = program
                try:
                    prog = builder(places[put["place"]])
                finally:
                    pieces.program = original
                (camp / "programs" / f"{stem}.json").write_text(
                    json.dumps(prog, indent=2, sort_keys=True, ensure_ascii=False) + "\n")
            d = subprocess.run([str(delvec), "--json", "--prefabs", str(lib), "detail", str(camp), "--all"],
                               capture_output=True, text=True)
            code = first_code(d.stdout + d.stderr)
            if d.returncode != 0:
                ok = code == probe["code"]
                refused += ok
                print(f"{'refused' if ok else 'WRONG  '} {name}: `detail` exit {d.returncode}, first code {code}, expected {probe['code']}")
                continue
        b = subprocess.run([str(delvec), "--json", "build", str(camp), "-o", str(scratch / name / "out"),
                            "--prefabs", str(lib)], capture_output=True, text=True)
        code = first_code(b.stdout + b.stderr)
        ok = b.returncode != 0 and code == probe["code"]
        refused += ok
        print(f"{'refused' if ok else 'WRONG  '} {name}: `build` exit {b.returncode}, first code {code}, expected {probe['code']}")
    print(f"probes: {refused} of {len(probes)} refused with the code they name")
    sys.exit(0 if refused == len(probes) else 1)


if __name__ == "__main__":
    main()
