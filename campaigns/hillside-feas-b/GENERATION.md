# Hillside feasibility B — generation record

The smallest case of the hillside comparison's cut B (`campaigns/hillside/DESIGN.md` §5.2): one sky-open box on a slope whose piece draws a street above its floor and meets the heightmap at its ring, over a stair seam to a landing, on a small island under the `ocean` horizon with a `boundary` of margin 8. It exists to show that a bound piece may draw its own ground above its floor on the current engine, to find what the engine asks of such a piece, and to read where the derived boundary falls. Not a demo level and not staged.

## Toolchain

`delvec 1.13.0, dsl 0.55.0, mc 1.21.11`, built in release mode from the engine at `da769d0ed4499caed7bcd0c69dc12f476586ce82` (`origin/main`; `cargo build --release -p delvec --bin delvec`, exit 0) on the remote build machine, invoked by path with `--prefabs` the content repository's `prefabs/` at the revision that carries this directory. The piece is written by `design/programs-src/slope.py` from the handout (`delvec allocation`), through `campaigns/hillside/design/thlib.py`.

## The plan

Region `[0, 40, 0]` + `[80, 48, 96]`; `fill: open` over `terrain/site.png` (80 × 96, `terrain/site.py` on `campaigns/hillside/terrain/heightfield.py`; land x 8..71, z 9..80). Two boxes: `node/street` 16 × 20 at floor 70 (its south end), `open: 10`, pinned at `[32, 44]`; `node/landing` 16 × 8 at floor 66, `open: 8`. One seam, `edge/street-landing`: a `stair` on the street's south face, opening 6 × 2, `stair_in: node/landing`. One quest, one `reach-anchor` objective at `anchor/node-landing`, radius 1. The street's terrain steps in three flat terraces at its ring, 73 / 71 / 69 (surface), the seam row at 69, the sill minus one.

## Runs

| Run | Exit | Refusals | Repair |
|---|---|---|---|
| `validate` | 0 | none | — |
| `build`, stand-ins, reach radius 3 | 3 | `DW0881`: the objective's 7 × 7 × 7 volume covers nine standable cells on the landing's treads a body cannot walk to the anchor's footing from inside it | `radius: 1` |
| `build`, stand-ins | 0 | none | — |
| `detail node/street`, first piece: one space over a 0.3 ramp, 69..75 | 1 | `contract-well-formed`: "space `street` has standable floor at y 1..7, which is 7 levels — a space is ONE floor (at most two consecutive levels, for a dais)"; `contract-coverage`: 12 standable cells (the parapet's top) in nothing the contract declares; `contract-no-body` bound zero | the heightmap steps the street in three flat terraces; the piece draws each terrace as a space and one tread row between each two as a `stair` edge (rise 2, via the tread row); the parapet's top is a `no_body` region |
| `detail`, second piece | 3 | every contract gate green and the piece written; the whole's battery: `DW0836`, "the wall at x 32..47 y 70..73 z 64 is open in 20 cell(s) the plan allocated no seam for" — a 2-high parapet under the 4-course face the two places share | the parapet fills the shared face (the overlap of the two play spaces, four courses over the sill) with a lintel over the opening; the opening is declared 6 × 2 |
| `detail`, third piece (opening 6 × 2, parapet still 2) | 3 | `DW0836`, now 32 open cells: the band is the shared face, not the opening's height | the parapet rises to the face's top, with the lintel |
| `detail`, final | 0 | none | — |
| `build`, final, detailed | 0 | none; advisories `DW0822`, `DW0813` | — |

## What the final detail states

`prefab/hillside-feas-b-street` written from `programs/street.json`: frame 18 × 11 × 22, seed 5887336984852359558; 1 declared face answering 1 allocated seam; 2 of 2 owed names bound (`anchor/node-street`, `spawn`); light `lit` over 384 measured cells; 1020 blocks, 48 rules, 5 palette roles, `shown_faces` down, east, south, west. Void binding: 0 void cells examined, 0 painted (`DW0987`); 224 fixed ring ground cells examined, 0 written (`DW0990`). Files: `prefabs/hillside-feas-b-street.{json,nbt,report.json}`, `detail-plan.json`.

## What the final build states

- Blockout: 2 places, 1 detailed, 1 massed by the derivation; 362 fixed ring ground cells laid; 1 seam cut.
- Battery: 1 seam proven over 1 shared wall, 6 standable opening cells; 2 places proven reached; 380 fixed ring ground cells handed, 120 plot-edge columns examined, **0 cracks** (`DW0990`); 7156 standable cells outside every claim (the commons), 0 place pairs joined through it (`DW0838`).
- `DW0311`: 1 leg walked. `DW0921`: 7634 cells a body can reach (the street opens onto the commons on three sides, so the whole island is walked), 0 it cannot leave, 0 afloat. Sea seepage: 7634 walk cells, 0 submerged, 0 wading. Piece exposure: 1 piece examined, 700 solid cells on its box boundary, 8 standing in air the party can be in, 2 sides seen, against 4 `shown_faces` declarations of which 2 are bound. Boundary binding: the region returns; 1 place a body is put examined, 0 outside.
- **Where the boundary fell**: `dw:region bounds {min:[23,57,35],max:[56,1024,81]}` — the union of the two box shells (x 31..48, z 43..73) grown by the margin 8, floored at the lowest placed block − 8. The island's land runs z 9..80 and x 8..71: the mainland north of z 35, the slopes beyond x 23 and x 56, and the sea past z 81 are outside, and the clock returns a body there. The same on the stand-in build (the fill does not count; the bound piece did not move the region).

## What this fixture found about the engine

1. **A piece's space is one floor** (`grammar::contract::well_formed`, spec-0098 departure 33): a bound piece that draws a sloping surface declares every level as a space and every step between two as a `stair` edge whose via is its treads. The engine refuses the slope-as-one-space with the count of levels; it does not refuse the design.
2. **The face two places share is wall wherever the opening is not** (`DW0836`), over the whole overlap of their play spaces in x and y — not over the opening's height. A piece that owns a seam's plane closes that face itself; in cut B that is a parapet across the whole town at its one seam, as tall as the two boxes' play spaces overlap.
3. **The handout's `ground.perimeter` entries are `[x, top, z]`** (piece-local), where the struct's doc comment (`crates/delvec/src/compiler/detail.rs`, `HandedGround::perimeter`) says `[x, z, top]`. A doc defect; the bytes are consistent.
4. The boundary is derived from the plan's placed pieces — box shells and volumes — and never from the fill; a heightmap island larger than its boxes has its far part outside the region by construction.
