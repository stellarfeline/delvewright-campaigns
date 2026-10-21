# Saltstair, variant A — generation record (superseded, not the experiment)

Stopped before step 9: no program was written. Toolchain: delvec 1.13.0, dsl 0.55.0, mc 1.21.11, release build of engine da769d0ed4499caed7bcd0c69dc12f476586ce82 (cargo exit 0, sha256 8b8d9388a0b5f461e9ee92267c9c3ccbf06c6dc5c31deb10343a6afd2f51af68) on the remote build machine.

## Refusals, in order

1. validate (first plan) exit 1: DW0100 site-plan: views[] eye/look_at must be integers (73.5). Repair: each view coordinate is the cell holding the camera's point (floor); design/cameras.json keeps the exact point.
2. validate exit 1: DW0110 x18 layout-graph: an edge id is `edge/<kebab-case>`, and `--` is not kebab case. Repair: `edge/<a>-<b>`. DW0890 x1: the copied reference image has no design.json row. Repair: design.json, one row, sky `dusk` + `clear`.
3. build, stand-ins, exit 2: DW0210, 722 of 1698 reachable walkable cells below light 3 under the dusk sky (judged 4): the eight houses' stand-in interiors. Not repaired: the houses' pieces carry their own light at step 9, which was not reached.
