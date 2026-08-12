# The Drowned Bell r2 — prefab generation record

This campaign's prefabs are produced by the engine's prefab procedure
(`docs/reference/prefab-procedure.md` in the pipeline repo): scene description
first, palette by measurement, grammar program as JSON, machine gates at
expansion, render before believing, admission. The scene-type route table in
that document decides the back end; every zone below is a grammar zone.

## The programs are campaign files

`design/programs/z*.json` are the **artifacts of record** (ADR-0018: the IR is
the artifact; a zone belongs to its campaign, not to the engine's library).
Exported 2026-08-12 from the engine library `bell::` module at engine commit
`4be4a12` — the engine copies are slated for removal once this campaign's
pipeline consumes only these files. Vocabulary is inlined at export, so each
file is self-contained and expands via `delve-grammar expand --file`.

An expansion's provenance (program hash, region, seed) is recorded in the
metadata the expander writes beside every `.nbt`; the same inputs regenerate
the same bytes.

## Zone status

One prefab per zone (owner decision, 2026-08-12 — no candidate sweeps until
the zone set is complete).

| Zone | Concept | Program | Status |
|---|---|---|---|
| Z0 barrow shore | `concept/z0-barrow-shore.jpg` | tidal-keep generator (pre-procedure; measured-palette pass 2026-08-11, engine PR #397) | owner-reviewed, accepted with the shoreline-edge correction applied |
| Z1 cliff road | `concept/z1-cliff-road.jpg` | `programs/z1-cliff-road.json` | program exported, unproduced |
| Z2 gate ward | `concept/z2-gatehouse.jpg` | `programs/z2-gate-ward.json` | **in production — the complexity probe zone** (largest program: 78 rules) |
| Z3 drowned ward | `concept/z3-drowned-ward.jpg` | `programs/z3-drowned-ward.json` | program exported, unproduced |
| Z4 chapel ward | `concept/z4-chapel-ward.jpg` | `programs/z4-chapel-ward.json` | **produced, awaiting owner review** — see below |
| Z5 hall keep | `concept/z5-hall-keep.jpg` | `programs/z5-hall-keep.json` | program exported, unproduced |
| Z6 cistern deep | `concept/z6-cistern-deep.jpg` | `programs/z6-cistern-deep.json` | program exported, unproduced |
| Z7 bell tower | `concept/z7-bell-tower.jpg` | `programs/z7-bell-tower.json` | program exported, unproduced |

Zone order of production is by complexity, hardest first (owner decision,
2026-08-12): the most complex zone is produced and owner-reviewed before the
rest, so a workflow defect is found on the zone most likely to expose it.

## Z4 chapel ward

**Scene** (fixed before any tool ran, per the procedure's §1): the player drops
out of the keep's kitchen duct onto the floor of a walled chapel ward of pale
grey-green ashlar, steps aside into a low paved nook to rest, and walks the
lane out past a side doorway — behind which a barred grate holds the sealed half
of a shortcut that only opens from the far side.

**Expansion** — `delve-grammar expand --file design/programs/z4-chapel-ward.json
--region 16x9x26 --seed 1 --traversable --allow-falls`. All gates pass with
non-zero bindings: `blocks-exist` 7, `non-empty` 3744, `traversable` 10 (5
standable cells at the approach end, 5 at the exit end, 165 in all; the entry is
a fall, hence `--allow-falls`). 3045 filled cells, 7 distinct states, 6 anchors,
silhouette complexity 1.03. `delve-admit audit` passes (0 forbidden, 0
non-allowlisted, 0 unknown).

**Provenance** — program `sha256:eb6b39ddd66c20ff4657767635a91269118b8d6cd494090988d7b90571435540`,
seed 1, region 16x9x26; re-expanding those inputs reproduces the `.nbt` byte for
byte (verified: `sha256:ac11c68d2eb97eca5f5218fbeb11df9dbb9a49eefb4bdfaaed0b8f67aecf6019`).
It is recorded here as well as in the metadata because `delve-admit lighting
--write` rewrites the metadata without the machine-readable `license.generated_by`
block.

**Artifacts** — `prefabs/z4-chapel-ward.nbt` + `prefabs/z4-chapel-ward.json`
(the repo's flat prefab library, where every other campaign's pieces live);
review shots in `design/review/z4/`.

**Palette** — measured, never named from memory: material colours sampled from
the concept image (patch means over verified crops), then blocks taken from
`tools/block-appearance.py --near` ranked lists, full-cube for everything
structural.

| Role | Block | Measured | Concept sample |
|---|---|---|---|
| `junction/rock` | `minecraft:tuff_bricks` | `#62675f` | `#626863` lit arcade ashlar |
| `hearth/rock` | `minecraft:tuff_bricks` | `#62675f` | `#626863` — same stone as the junction, so the lane reads as one building |
| `shortcut/rock` | `minecraft:polished_tuff` | `#626864` | `#5c6160` far-wall arch stone; smooth, for the plainer sealed chamber |
| `chute/rock` | `minecraft:cobbled_deepslate` | `#4d4d51` | `#4f554b` shadowed lower masonry — the service duct is not the ward |
| `hearth/hearth_floor` | `minecraft:polished_andesite` | `#848786` | `#7b8789` lit flagstone — the rest plate |
| `margin` | `minecraft:deepslate` | `#545456` | inert mass, no player-visible face |
| `shortcut/bar` | `minecraft:iron_bars` | `#898b88` | `#262e31` door ironwork |

The bar is the one deliberate departure from the nearest colour match. The
concept's barrier is a timber door leaf, but the rule seals a 6-wide by 3-high
partition opening, which is a portcullis and not a leaf; a see-through grate is
also what lets the player read the far side of a shortcut before it opens.

**Open against this piece**

- Lighting profile is `dark` (`DW0751`, min floor light 0 over 165 walkable
  cells). No rule in this zone exposes a light-emitting role, so the piece
  cannot be lit from its palette: light has to arrive as campaign-bound content
  on the declared anchors, or as a light role added to the library rules.
- The concept image is an open, roofless cloister; the zone's design intent and
  topology are an enclosed hub. The palette and proportions converge on the
  concept's material and tone, and the composition does not — deliberately, the
  topology is fixed.
- 47.9% of the piece is `margin`, the inert mass behind the shortcut rooms.
