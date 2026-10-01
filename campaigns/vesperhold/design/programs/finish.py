#!/usr/bin/env python3
"""Expands vesperhold.json into the prefab library and finishes the piece.

The grammar declares point anchors only, so the gate regions the campaign
opens and closes are written into the metadata here, from gates.json, after
every expansion (an expansion rewrites the metadata). Then the piece's walk
plane and lighting are measured and it is audited.

    python3 finish.py <prefab library directory>
"""
import json, pathlib, subprocess, sys

HERE = pathlib.Path(__file__).parent
lib = pathlib.Path(sys.argv[1]).resolve()
SIZE = "172x104x292"


def run(*args):
    print("+", " ".join(args), flush=True)
    r = subprocess.run(args, text=True, capture_output=True)
    tail = (r.stdout + r.stderr).strip().splitlines()[-6:]
    print("\n".join("  " + l for l in tail))
    if r.returncode != 0:
        sys.exit(f"exit {r.returncode}")


for old in lib.glob("vesperhold.*"):
    old.unlink()
run("delvec", "--prefabs", str(lib), "grammar", "expand", "--file", str(HERE / "vesperhold.json"),
    "--region", SIZE, "--seed", "1", "-o", str(lib))
manifest = lib / "vesperhold.json"
# `prefab anchor` takes a single template, and this piece is a tile set, so the
# gate anchors are written into the manifest in the shape that command writes.
meta = json.loads(manifest.read_text())
for name, g in json.loads((HERE / "gates.json").read_text()).items():
    meta["anchors"][name] = {"region": {"from": g["from"], "to": g["to"]}, "block": g["block"]}
manifest.write_text(json.dumps(meta, indent=2) + "\n")
print(f"wrote {len(json.loads((HERE / 'gates.json').read_text()))} gate anchor(s) into {manifest.name}")
run("delvec", "--prefabs", str(lib), "prefab", "planes", str(manifest), "--write")
run("delvec", "--prefabs", str(lib), "prefab", "lighting", str(manifest), "--write")
run("delvec", "--prefabs", str(lib), "prefab", "audit", str(manifest))
