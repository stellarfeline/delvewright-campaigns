# The Muster Loft — generation record

## What the brief pinned down

The engine's demo-level queue row for spec-0107 pinned four places: a hall; a
loft up a stair whose head is barred until the muster in the hall falls; a
cellar down a shaft whose hatch is shut until the same beat; and a ladder back
up from the cellar to the hall, with a grating over its hole opened from the
hall's side only (`opens_from`). Played in order: the long way round on the
walk, the bar met at each shut way before its beat, each opening at the beat.
It is the first read of whether a bar at the head of a stair and a grating
over a ladder read as ways the story will open, and of whether the ladder's
top rung under the grating feels like the stop it is. Small, one mechanic,
minimum cast.

## What was invented here

- The fiction: the Harrowgate levy that mustered under the hill and never came
  home, the reeve's bars, the roll kept in the cellar and laid in the loft.
- The fourth place, the stores, and with it the long way round: out of the
  cellar up the stores stair, through the stores door, back into the hall. The
  stores stair is gated on the same beat as the shaft and the loft stair,
  because a way into the cellar left open before the muster falls is a way
  round the hatch, and `DW1011` refuses it. That makes one gated connection of
  each kind the spec builds: a stair head in a wall (the loft stair), a hatch
  over a drop (the shaft), a hatch over a stair (the stores stair), and a
  grating over a floor climb (the ladder).
- The ladder is the declared shortcut (`shortcut: true`). Once the muster
  falls the cellar is open by two other ways, so the grating separates nothing
  the story keeps shut; `DW1011` counts it and does not judge it. Its one-sided
  opening is a beat: the party draws it at the winch beside it in the hall (an
  `interact`), and `opens_from: b` names the hall as the side it opens from.
- No speaking cast. Narration carries the premise once, on arrival, and the
  objective titles carry the rest.
- The roll's chest is the cellar's own, standing in its corner, and the
  `collect` adopts it (`container: anchor/roll-shelf`): a chest the compiler
  conjures binds neither the adopted-container nor the distinguishable-target
  check, and the staging gate refused that shape as two unbound findings.
- The muster: three zombies with declared health, on the hall floor, spawned
  once the four bars have been tried. A checkpoint in the stores governs it.
- One class, the Hall Warden: a sword, a shield, mail and bread.

## Engine and language

Built with `delvec 1.13.0, dsl 0.45.0, mc 1.21.11` from the engine's
`feature/a-gated-edge-is-built` at
`717109f9a8f7d3668718bf53681e76e4b20631b6` — an unreleased tree, the only one
carrying spec-0107. Its version string is the same number as the released
`delvec--v1.13.0` (which answers `dsl 0.39.0`), so the version alone does not
say which engine built this level; the revision does.

No shipped library taken: every piece is this campaign's own, written as a
grammar program under `programs/` and frozen by `delvec detail` into
`prefabs/the-muster-loft-*`. Each program is a course-by-course split of its
frame (y, then x, then runs along z), emitted from a cell layout by a scratch
script that is not part of the campaign; the programs are the artifact.

Languages: English, and zh-CN transcreated as a sidecar.

## Posture note

The level states its rule once, at arrival — the bars lift only when the muster
falls — and then lets the bars say it again at every way out. Nothing explains
the levy's grief or the reeve's reasons. The end is the roll laid in the loft
and an empty hall floor, not a reflection on either.

## The design gate

Step 4 was not passed: no reference images were drawn and no one approved a
design walkthrough. This is a demo level whose gate is the built level itself;
`design/` and `design.json` do not exist, and no showcase camera is written.

## Target length

`target_minutes` is 10. The critical path measures 85 blocks of route over six
legs of the built map (about two minutes of walking); the rest is the level's
content — reading each bar, the fight, the long way round, the grating.

## The skill run

Authored through `/new-delve` as the engine tree above carries it
(`.claude/skills/delvewright/skills/new-delve/`, at the same revision), not
through an installed plugin. The skill's Init has no way to name an unreleased
engine revision: creator mode pins a release tag, and dev mode needs the
working directory to be the engine checkout, whose `campaigns/` link points at
another content checkout. The run used that tree's own binary,
`target/release/delvec`, built with `cargo build --release -p delvec` (exit 0),
through an environment file of its own. Init's pin check (I1b) reads only
`~/.delvewright/env.sh`, which names the released engine and is shared by
other runs on this machine; it refused that file (exit 3), and passed (exit 0)
only when run with `HOME` pointed at a directory holding this run's own
`.delvewright/env.sh`.

## Binding lines, as built

On the build whose manifest sha256 is
`8441353e29bae7e62327f9af4f2218616e9a2733ba4cf0c4a11a26be63f4ebd1` (two
builds byte-identical):

- `DW1027 binding: 4 gated connection(s), 0 of them fronts.`
- `DW1028 binding: 4 gated connection(s), 4 opened by an `open-gate`, 0 by a
  shortcut, 0 by a clock, 0 by nothing.`
- `DW1011 binding: 4 gate(s) resolved (4 of 4 gated connection(s) among them);
  1 declared a way round (shortcut), 0 clocked, 0 operated by no beat, 0 with
  no two faces; over 3 quest configuration(s), 3 (gate, configuration) pair(s)
  shut, 0 with a face no body can stand at, 3 with the party at a face, 0 got
  round by walking, falling, jumping or swimming`
- `blockout binding: 4 place(s) massed (4 detailed, so 0 massed by the
  derivation; …), 5 seam(s) cut (0 stair, 0 climb, 4 shut), 0 stairwell
  cell(s) cut over through-floor runs, …`
- The world-load seal (`validation/gate-seal.json`): 4 gates examined, 4
  sealed at world load — the loft stair's head (9 cells), the shaft's hatch (4),
  the stores stair's hatch (12) and the grating (1, the course above the
  ladder's hole, whose own cell holds the top rung).
- `attached blocks (DW1002): 20 of 48895 non-air cell(s) at load need a
  neighbour to stay — 20 held, 0 dropped`.

## Machine ladder

On the build above:

- PackTest: all 30 required tests passed.
- Bot: critical path passed, 11 steps; die-retry passed, two scripted deaths
  at the muster, each respawned at the stores checkpoint with the kit kept and
  re-engaged; the muster read 3 of 3 declared bodies matching their
  declaration over 2 checked facts. `cue binding: 10 of 10 owed cue(s)
  arrived at the bot (9 announced objective(s) in the build), 1 of the 10
  judged farther than 16 blocks from the world spawn; 9 of 9 other cue
  packet(s) at the bot`. Death loop: not run — the campaign declares
  no lethal volume, `on_death` or recovery stake, so there is none to prove.
- Written world (`DW0955`): 5633 non-air cells compared, 0 differing in the
  model class; the differences are the named server re-derivation of the iron
  bars' connections (25 cells: the two hatches and the stair head).
- Staging gate (run as a check, its token written outside the build and
  discarded): all 127 findings carry a live, binding check or a justified
  exemption; 67 classes are inapplicable to this campaign.

## Visual review — deferred

Step 12 is not complete: the Chunky renders were stopped before the set was
drawn, and the rest of the review waits for the Lumenwright review frames.

Rendered and checked, all as 64-sample drafts (framing only, not the scenes'
own budget), from server world saves of this campaign:

- `pov/leg0/wp4`, walking up to the loft stair's head, from the world of a
  build at engine `6645a102`, two campaign revisions earlier, whose structures
  differ from this one only in the cellar's chest: bars fill the passage at the stair's head, the loft's
  spruce ceiling visible through them; it reads as a barred way, not a wall.
- `gate/site/seam_cellar_shaft/a` and `gate/site/seam_cellar_stair/a`, from
  the world of the build at engine `6645a102` whose manifest sha256 is
  `2f464603a6fa3618f862b51c7797fba0c4a74feec4ef715e8fdc951ba9d002ad`; this
  build's gate seal is the same record, cell for cell: each looks down through its hatch — a lattice of bars
  over the shaft, with the cellar floor below; over the stairwell, with the
  stone treads below. Both read as barred holes in the floor.

Not rendered: the other 98 of the 103 scenes `render-shots.sh` wrote for that
build, among them the grating from both sides (`gate/site/seam_cellar_ladder/a`,
`/b`), the loft stair's head from the loft (`gate/site/seam_loft_stair/b`),
every other POV frame, every interior and spawn shot, and the whole-map
panorama. The fill is solid rock, so the panorama would show the hill's mass
and nothing of the places inside it. The storybook carries no image for the
same reason.

CPU drafts (`delvec snapshot`) of the hall, the stores, the cellar and the loft
were looked at for layout before the ladder; the CPU renderer draws neither the
iron bars nor the lanterns, so they say nothing about the bars.

## Findings from this run

- **A gated stair through a floor, hosted by a stand-in, is built open.** With
  the cellar still massed by the derivation, the stores stair's hatch was
  written (blockout step 6c) and then cut to air by the stairwell over the
  stair's run (step 7), which clears the floor course over the treads after
  the bar is laid. The world-load seal then measured that gate as not shut, so
  `DW1011` did not judge it, and the shaft's hatch was refused as got round
  through it. Once the cellar was detailed the derivation laid no treads and
  cut no stairwell, and the piece's bar stands. Direction: it turns a proof
  red on a stand-in build; a stand-in never ships. The engine at `717109f9a`
  lays a shut seam's bar after the stairwell is cut, so the hatch stays shut on
  a stand-in too; this level, every place detailed, does not exercise that
  path.
- **The bot does not measure the top rung under the grating.** The harness
  walks only the route the compiler proves; no step stands a body on the
  ladder's top rung with the grating shut and asserts that it cannot climb
  out. What holds that claim is the engine's model: the shortcut's gate is
  sealed for the whole completability model, and the proven route from the
  ladder's foot to the winch goes the long way round, which the bot walked.
