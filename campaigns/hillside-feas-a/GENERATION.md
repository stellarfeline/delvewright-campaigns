# Hillside feasibility A — generation record

The smallest case of the hillside comparison's cut A (`campaigns/hillside/DESIGN.md` §5.1): two roofed houses at different floors joined through a way box on a slope, on a small island under the `ocean` horizon with a `boundary` of margin 8. It exists to show that the cut compiles and walks on the current engine, and to read where the derived boundary falls. Not a demo level and not staged.

## Toolchain

`delvec 1.13.0, dsl 0.55.0, mc 1.21.11`, built in release mode from the engine at `da769d0ed4499caed7bcd0c69dc12f476586ce82` (`origin/main`; `cargo build --release -p delvec --bin delvec`, exit 0) on the remote build machine, invoked by path with `--prefabs` the content repository's `prefabs/` at the revision that carries this directory.

## The plan

Region `[0, 40, 0]` + `[80, 48, 96]`; `fill: open` over `terrain/site.png` (80 × 96, written by `terrain/site.py` on `campaigns/hillside/terrain/heightfield.py`: pads at walk plane − 1 under each box and its ring, a hill on the mainland, the ground falling half a block a column to the sea; land x 12..66, z 5..79). Three boxes: `node/house-high` 7 × 7 at floor 74, clearance 4, roof 4/1, pinned at `[36, 40]`; `node/way` 5 × 8 at floor 70, `open: 8`; `node/house-low` 7 × 7 at floor 70, clearance 4, roof 4/1. Two seams: `edge/high-way`, a `stair` on the high house's south face, opening 3 × 3, `stair_in: node/way`; `edge/way-low`, a `walk` on the way's south face, opening 3 × 3. One quest, one `reach-anchor` objective at `anchor/node-house-low`, radius 1.

## Runs

| Run | Exit | Refusals | Repair |
|---|---|---|---|
| `validate`, first plan (`node/way` at `open: 6`) | 1 | `DW0829`: the 3 × 3 opening anchored at y 74 runs to y 76 and the face the high house and the way share ends at y 75 | the way takes `open: 8` |
| `build`, first plan | 1 | the same | — |
| `build`, second plan (reach radius 3) | not reached on this fixture; the same objective shape was refused on fixture B with `DW0881` | the objective takes `radius: 1` here too |
| `validate`, final | 0 | none; advisories `DW0822` (pacing, no threshold), `DW0813` (provisional metrics) | — |
| `build`, final, stand-ins | 0 | none | — |

## What the final build states

- Blockout: 3 places massed by the derivation, 2 roof zones massed, 140 fixed ring ground cells laid, 2 seams cut (1 stair), 4 anchors synthesized.
- Battery: 2 seams proven over 2 shared walls, 2 portals over 6 standable opening cells; 3 places proven reached; 154 fixed ring ground cells handed, 82 plot-edge columns examined, **0 cracks** (`DW0990`); 7716 standable cells outside every claim (the commons), 0 place pairs joined through it (`DW0838`).
- `DW0311`: 1 leg walked. `DW0921`: 144 cells a body can reach, 0 it cannot leave. Sea seepage: 144 walk cells, 0 submerged, 0 wading. Boundary binding: the region returns; 1 place a body is put examined, 0 outside.
- **Where the boundary fell** (read from the emitted `setup_finish`): `dw:region bounds {min:[27,61,31],max:[51,1024,72]}`; the clock's selector is `x=27,dx=25,y=61,dy=963,z=31,dz=42`. That is the union of the three box shells (x 35..43, z 39..64) grown by the margin 8 on each horizontal side, floored at the lowest placed block − 8. The island's land runs z 5..79 and x 12..66: the mainland north of z 31, the slopes west of x 27 and east of x 51, and the sea south of z 72 are all outside the region, and the clock returns a body there to its last checkpoint. **The fill does not count toward the boundary**: only the plan's placed pieces — box shells and `volumes[]` — do (`crates/delvec/src/compiler/emit/boundary.rs`, `playable_region`, over the pieces `crates/delvec/src/compiler/blockout.rs` lists).

Not run here: the detail of any place (the cut's question at stage 5 is answered by the stand-ins), PackTest, the bot. The engine's one defect found by this fixture is none; the two refusals were the plan's.
