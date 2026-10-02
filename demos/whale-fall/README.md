# Whale-Fall — a structure study

The skeleton of a giant dead sky-whale, floating over nothing. It is big as a
small hill: 128 blocks nose to tail, 45 across the flippers and 48 tall. The
spine is a walkway. Ten pairs of ribs arch around a chest the party walks
through on a stone catwalk. The skull holds a small colonnaded shrine.

This is a study, not a campaign. It asks one question: can the grammar build
a large, irregular, non-architectural thing that reads as itself at playable
scale? Nothing here has quests or dialogue. Nothing here is owner-approved.
The reference views under `design/reference/` are study material and carry no
approval (there is no `design.json`).

## Scene description (written before the first expansion)

A body lands on the tail tip. It walks forward along the vertebrae, between
the neural spines. It can go down the pilgrims' stair into the chest and
cross the catwalk under the rib vault. Or it can go on along the spine
through the foramen magnum, the hole in the back of the skull, into a low
hall of columns. The bone is bleached ivory, chalky and enormous. The only
human work is grey, mossy stone: the catwalk, the stair and the shrine.

## Anatomy (cited)

- The vertebral formula of the anterior column is C7 T16 L14, read off an early blue whale fetus. *Roston et al., "Anatomy and Age Estimation of an Early Blue Whale (Balaenoptera musculus) Fetus", The Anatomical Record, 2013* ([link](https://anatomypubs.onlinelibrary.wiley.com/doi/full/10.1002/ar.22678)).
- A pygmy blue whale has up to 27 caudal vertebrae, the same count as an ordinary blue whale. The skull is 21.2–23.9% of body length in females and 23–27% in males (Tomilin, as cited in *Osteology of Pygmy Blue Whale*, ICR Scientific Reports) ([link](https://www.icrwhale.org/pdf/SC0221-27.pdf)).
- Only the first rib pair meets the sternum. The thoracic vertebrae carry the ribs. The caudal vertebrae carry chevron bones underneath ([Nature Communications 2024, *Repatterning of mammalian backbone regionalization in cetaceans*](https://www.nature.com/articles/s41467-024-51963-w)).

What the study takes from this: the skull is 30 of 128 blocks (23%). The neck
is short. The rib-bearing thorax is 40 blocks long and the lumbar run is 24.
The caudal series shrinks to the tip and has chevrons under it. There is no
fluke, because a fluke has no bone.

**Departures, authored:**

- **Ten rib pairs, not 14–16.** At one block thick and a four-block pitch, sixteen pairs would close the cage into a wall.
- **The catwalk.** Ribs float free at the bottom and nothing can stand inside a real rib cage, so a stone catwalk hangs on beams from the ribs. In the fiction, pilgrims built it.
- **The neural spine sits on the midline**, as anatomy has it. The walkway is the two three-wide lanes either side of it.

## Palette (measured)

These were screened with `tools/creator/block-appearance.py --screen` under
`full_cube`, `L>=0.72`, `C_mean<0.05`, `texture_range<=0.35` and `not gravity`.
That leaves 21 survivors. The swatch sheet was looked at before anything was
chosen.

| role | paint | measured |
|---|---|---|
| bone (ribs, flippers, mandibles) | `bone_block[axis=y]` 8 : `calcite` 2 | bone_block #dcd8c2, calcite #dfe0dd |
| skull | `bone_block[axis=z]` 8 : `calcite` 2 | the grain runs the skull's length |
| spine | `bone_block[axis=z]` 9 : `calcite` 1 | the grain runs the spine's length |
| cartilage (discs) | `calcite` | #dfe0dd |
| walk, paving (human work) | stone_bricks 5 : mossy 3 : cracked 2 | chroma_mass 0.0101 |
| lamp | `pearlescent_froglight[axis=y]` | #f1e9ea |

The first mix had diorite at 10%. It read as checkerboard noise at eye range
in every interior frame, so it was removed. The measurement had not flagged
it, because chroma_mass was 0.0201.

## How it is built

Everything is one grammar program, `whale-fall.program.json`. It was expanded
at `45x48x128`, seed 1, and ships as a tile set of three. `build_program.py`
only spells that JSON. It places no block.

The techniques:

- **Counters as position.** The skull's taper, the mandible's bow, the rib cage's swell and the ribs' rake are each a recursion that rebinds a counter (`n`, `k`) to `n + 1`. Sizes are arithmetic over the counter. This is the grammar's only index into a recursion (`grammar.md` §2, `bind`). With it, a profile can vary along a length. The mandible's bow is `2 + n(27 − n)/14`, which is quadratic, so it reads as a curve stepped at one block per column.
- **Rib cross-section.** A ring is drawn one course at a time from the equator, inset by `n/3` and thickened to `max(2, n/3 + 1)`. The lower half is mirrored (idiom 3 on two halves, idiom 7). The upper half is pinned to the band's top, so the catwalk course holds one world height in every bay.
- **The skull is one wedge.** It is two-block slices from the occipital forward, mirrored on Z. Slices 0–6 are hollow: a paved floor at the walkway's height, a colonnade, a stepped vault, the foramen in slice 0 and the orbits in slices 3–4. The rest is solid rostrum.
- **Light** is placed while the room is designed. The column capitals and the altar are froglights.
- **Stairs are stairs.** The lumbar flight and the tail's descent use stair blocks facing the climb. The dais stair is written `{"local": …}`, because the hall is built mirrored.

## Machine verdict

`delvec grammar expand … --region 45x48x128 --seed 1` (engine `1ef29efa`,
delvec 1.7.1) gives:

- **Always-on gates:** all pass. That is blocks-exist, shape-complete, states-complete, oriented-fills (851 fills), stair-shape (84 stairs) and non-empty.
- **Size:** 14980 filled cells of 276480. 2659 cells are standable.
- **Determinism:** two expansions give byte-identical tiles and manifest (the hashes are in the commit body).
- **`delvec prefab audit` on the manifest:** pass.

`--traversable` and `--reachable-floor` were **not** passed, and the obstacle
list says why. The always-on reachability line is honest about what it
measured. Its largest unreached pocket holds 1485 cells, in the box
`x 8..36 y 8..35 z 16..125`. That box spans the whole walk network: catwalk,
stair, spine, tail and shrine. It is one pocket, which is grouping evidence
that the network is connected. It is not a directed walk.

## Renders

There are two instruments. Neither is Chunky, and the obstacle list says why.

- **`delvec render piece prefab/whale-fall.json`.** This is the piece-review path that `new-pieces.md` §5 prescribes. Its frames are flat-lit against a grey background.
- **`delvec snapshot campaign/whale-fall-study`.** This is the stub campaign: one `areas[]` area binding `prefab/whale-fall`, with `horizon: void`. The snapshot rasteriser is the same one `delvec cameras --preview` uses. It draws the void horizon: sky above, nothing below. Cameras are given in world coordinates. The piece's origin is `(0, 64, 0)`.

The renders are not committed. They regenerate from the bytes and the
commands above.

## Obstacles

Each obstacle below says what the structure needed, what was tried, what the
engine said, and what was done about it.

1. **A floating structure has no "grade", and three instruments derive their entrance from grade.**
   - Reachability (`nav::ground_entry`), the lighting profile and `walk_y` all seed from "the lowest Y at which any side-face cell is standable". On this piece that is the eight cells at the tips of the flipper digits and mandibles.
   - The result: `reachability 8 of 2659 standable cell(s) reachable on foot from 8 grade entry cell(s) (0.3%)`. `--reachable-floor` reds (`994 standable cell(s) under a roof; 994 of them have no walking route`, on the first program). `--traversable` reds and pairs flipper tips with mandible tips (`3 open side(s), derived from the blocks … no walk connects west side (4 cell(s)) <-> north side (11 cell(s))`).
   - The lighting profile reads `min over 8 floor cell(s) reachable on foot from 8 ground-level entry cell(s)`. That is the light at the finger bones, not in the shrine. `walk_y` is 3.
   - **Not worked around.** The two flags were dropped rather than satisfied. Any repair that would satisfy them is a hack: an artificial "ground" plane, or trimming the flippers. The honest instrument is the spatial contract's own reachability, seeded from a declared `entry` space (see 2).
2. **The spatial contract fits rooms, not a skeleton.**
   - Declaring the entry needs a `contract`. Its coverage obligation needs every standable cell inside a declared space or an out-of-walk region. Nearly every bone top is standable: rib steps, the neural spines, the skull roof, the mandibles, flipper courses. That is about 2000 open cells.
   - A `claim` names a scope box, and the cell a body stands in is the air above a bone. So covering it means claiming void scopes interleaved through every recursion. And each space must be "one floor (standable span ≤ 2 levels)", which the descending tail is not.
   - **Not done.** It is too large to do as a study, and it fights the language. The piece declares no contract, and `expand` says so as a finding.
3. **Smooth curves and diagonals come out as stair-steps.** This is the documented limit (`new-pieces.md`, *What the grammar cannot express*), and it shows plainly at this scale:
   - The skull's taper is a one-block step every two-block slice. From any oblique view it reads as vertical corrugation down the flanks (`d1-skull-and-open-jaw`).
   - The rib rake is two blocks over 21 courses. From the side it reads as a zigzag where the ribs meet the spine (`a2-far-flank-void`).
   - The mandible bow (one block per column, quadratic) is the best-looking curve in the piece.
   - Counters plus arithmetic do give polynomial profiles. What never goes away is the stair-step. **Reported, not worked around.**
4. **A cloud sea has no surround.** The horizons are `void`, `ocean` and `valley`. A sea of cloud below the whale is not one of them, and building it from blocks would be terrain in a prefab, which is excluded. **Stopped.** The renders show the void horizon.
5. **`delvec cameras` needs approved images.** A camera row's `answers` must name a `design.json` row, and `design.json` records approvals. Writing one would assert an approval the owner never gave. **So no camera record was written.** The frames come from `delvec snapshot --camera`, which the docs state is byte-identical to `cameras --preview` for the same numbers. There is no path-traced frame, because a Chunky scene needs a camera record and a world save (docker).
6. **The toolchain check is bound to one `~/.delvewright/env.sh` per machine.**
   - I1b compares the binary and engine that file names. On this machine it names another checkout and a stale binary (`found delvec 1.4.0 … want delvec 1.7.1 — DISAGREES`).
   - A second, parallel engine tree can only pass I1b by overwriting that file. That would break whoever else uses it.
   - **Worked around legitimately.** I1b was run under an isolated `HOME` whose `.delvewright/env.sh` names this study's engine and binary, and it exits 0.
7. **`grammar expand` takes its id from the file stem, so `whale-fall.program.json` is refused** (`"whale-fall.program" is not a usable structure id`). The same naming is what the demos here use. **Fixed** with `--id whale-fall`.
8. **The reference series is billed per image, and one call returned four.** The view-2 call returned four images, all billed (`returned: 4`). Init I7 documents this, and it is recorded here as cost.

## Verdict

From the far views it reads as **the skeleton of a big sea creature**. The
broad wedge skull, the bowed open jaw, the flippers with digits, the long
spine with neural spines and the tapering tail all register. Whether a viewer
says "whale" rather than "some huge fish or reptile" depends mostly on the
jaw and the flippers.

From inside, the rib cage is the strongest moment. Looking up the catwalk,
the ribs read unmistakably as ribs arching to a spine (`c1`, `c2`).

Walking the spine reads as a bone causeway, not obviously as vertebrae.

The skull reads as a stepped bone block with vertical corrugation. Its
interior is a low shrine of columns, not a temple of any scale. Holding a
real temple would take a skull far past whale proportion.
