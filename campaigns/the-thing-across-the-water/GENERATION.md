# The Thing Across the Water — generation record

- **Brief**: the engine's `docs/demo-levels.md` row for spec-0110 (a shot frames
  its subject). It pins a jetty on an ocean horizon, a hall with a keeper behind
  it, a figure of block displays on a sea-stack ninety blocks off that rises when
  a bell is rung, the three cutscenes (an establishing shot over the bay declared
  `"landscape"`; the bell's cutscene framing the figure as it rises, spawned by
  the beat before; the keeper through the hall's open door), the five refusals,
  and the walk's two questions (does the figure read at ninety blocks; is it
  still there at entity distance 50% and render distance 8). Everything else here
  is invented.
- **Engine**: `delvec 1.13.0, dsl 0.48.0`, built from the unreleased engine
  branch that carries spec-0110 (`feature/shots-frame-their-subject`). `dsl_version`
  is `0.48.0` on every document. The page's own pin (`versions.toml`) names the
  release `delvec--v1.13.0`, whose dsl is 0.39.0; no field of the page or of this
  campaign can name an unreleased engine revision, so the revision is recorded
  here and in the storybook's marker only by its version numbers.
- **Placement**: a site plan of three places. `node/jetty` (5 × 24, the entry),
  `node/hall` hung off its south face by the seam for the hall's door (a declared
  opening 3 wide and 3 high, so the keeper is in plain sight from the jetty), and
  `node/stack`, scenery (`reached: false`), pinned ninety blocks north and seen
  along the vision edge `edge/across-the-water`. The vista's far end is at y 79,
  above the stack's crown.
- **Below the sea**: every frame is solid masonry or rock up to the sea's top
  course (y 62), so no cell of the ocean is replaced by air when a template is
  placed. The jetty is a stone mole; the hall stands on a stone footing; the stack
  is rock from the sea floor.
- **The stack's crown**: the stack's top is a hollow ringed by a broken rock crown
  two courses high. `DW0322` roots its stranding proof at every anchor, the
  scenery stack's own `anchor/stack-top` included; with an open top it refused 20
  cells from which a body could step into the sea. The crown closes the top.
- **The stack's shape**: drawn first as a 7 × 7 shaft, which the draft frames read
  as a chimney. The box is 11 × 11, and each column of rock stands to its own
  height, stepping in from the full width at the waterline to a seven-wide top.
- **The figure**: no rig in the library is a figure on a rock, and a rig is a
  generator's output, never campaign JSON. The figure is the library's
  `rig/tentacle` (34 `block_display` segments; its `rise` clip brings it out of
  the rock to stand 25 blocks over the mark), regenerated into `prefabs/rigs/` by
  the engine's `prefabs/rig-generator`. It faces south, leaning toward the jetty.
  `initial: "rise"`, and the bell's beat spawns it in the same effect list ahead
  of its cutscene, one tick before the first `spectate`. No `seen_from` is
  declared: the build derives `view_range` 3.87 (the walked place's term won,
  3.861, over the shots' 3.012).
- **The keeper**: a villager body. A skinned mannequin is the page's default; for
  a one-character demo whose subject is a shot of him, the villager's box
  (cull radius 67.2) is part of what the build reports, and no skin was drawn.
- **The keeper's two talks**: two quests, because the keeper's cast row names a
  different entry node in each (`dlg/keeper-root`, `dlg/keeper-after`); one
  dialogue tree holds both.
- **Detail**: all three places are detailed from `programs/<place>.json`, written
  by `design/programs-src/bay.py` from `delvec allocation`; re-run it, then
  `delvec fmt` and `delvec detail . --all`, after any plan edit.
- **Languages**: English and zh-cn. The zh-cn sidecar was written through
  `delvec l10n-inventory` / `delvec l10n-apply`, every line transcreated by the
  agent from the English's intent; the provider path was not used.
- **Posture note**: (1) the keeper names his fear outright once, at the end;
  (2) nothing explains what the thing is or why the bell calls it; (3) the
  ending is unresolved — the thing is still standing when the delve ends.
- **The design gate**: not held. No reference art was drawn and no design record
  is approved: `design.json` does not exist. `world.json` declares
  `demo_level: true` and the engine's demo queue names
  `campaigns/the-thing-across-the-water`, so the staging gate's design-record
  findings measure this level zero. The design of record is the demo-levels row
  and `DESIGN.md`.

## Rebuilt on the refreshed engine (`feat/batch-b-refresh` at `351e631e54153b6277fbd02de106f66e92a53583`, `delvec 1.13.0, dsl 0.56.0`)

Every document carries 0.56.0 and `world.json` declares `demo_level: true`;
nothing a player meets changed. `build` exit 0 twice, byte-identical (419
files); PackTest 31 of 31 required tests passed; the bot's critical path
passed; the written world equals the server's at all 19632 compared cells; the
staging gate admits it with no override (147 rows: 45 bound, 75 inapplicable,
27 declared uncoverable, 0 refused).

## Rebuilt on the assembled Batch-B engine (`integrate/batch-b`, `delvec 1.13.0, dsl 0.54.0`)

What the engine merge forced: every document carries 0.54.0; the ground states
its music in the object form, the ocean's own vanilla statement; the hall's
west wall keeps one barrel and its other two stores are bales of dried kelp
(two empty containers are the most a place may hold as scenery), and the two
barrels left are declared scenery with one arrival line. The engine now hands
every player a compass and a journal. The ladder on that build: `build` exit 0
twice, byte-identical (419 files), `shot subjects` unchanged from the line
below; PackTest 31 of 31 required tests passed; the critical-path bot PASSED,
both `shot_subjects` rows `spawned_before: true`, `spawned_through: true`; the
written world equals the server's at all 19632 compared cells.

## Verification (engine `feature/shots-frame-their-subject` at `d4e6cb577df6`, `delvec 1.13.0, dsl 0.48.0`)

The numbers below are from the build the ladder ran; the storybook names what
the owner looks at.

- `validate`, `analyze`, `build`: exit 0. `shot subjects: 4 shot(s) in 3
  cutscene(s), 4 declare a subject (1 landscape, 0 marks, 1 bodies, 1 assemblies,
  1 places, 0 regions); 383 tick(s) judged, 0 out of frame, 0 occluded, clear
  lines 2643 of 3447; bodies: 2 present, sent, drawn — farthest 96.4 blocks,
  hidden below entity distance 0.23`.
- The five refusals: `refusals/`, each the primary plus one declared edit, each
  refused with its named code and no other error.
- PackTest (`validation/packtest-run.sh`): 27 of 27 required
  tests passed.
- Critical-path bot (`validation/bot-run.sh`, run report for
  manifest `38d82cff2bd0…`): every leg walked and every objective met, and the
  stage is RED on its two `shot_subjects` rows alone — both `spawned_before: true`,
  `spawned_through: false`. Not a campaign defect, and not repaired here: the
  harness's observer (`harness/src/shot-subjects.ts`) counts client physics ticks
  from the first tick the bot stands at the cutscene's first lens and records a
  shot when its count reaches `start_tick + ticks`; the cutscene's end function
  restores every player's gamemode in the same server tick as the last driver
  tick, so the last tick of a cutscene's last shot is never seen in spectator, and
  `finish()` records the unfinished shot as a body that left. Both body shots here
  end their cutscenes. Three runs over three builds: keeper false and figure true on the first,
  both false on the second and on this one. Varying only that, a scratch copy with
  a one-second `"landscape"` shot appended after each body shot (never shipped)
  ran both rows true and the critical path PASSED. The direction
  is a false red: it can only refuse a build, never let one through.
- Written world (`validation/world-save.sh`, `delvec written-world`,
  `tools/ci/check-written-world.py`): 0 differing cells of 19632 in every class.
- Staging gate (ledger at the engine revision above): REFUSED, 2 of 124 findings
  unbound — `drill3-01`, `drill3-03` (no design record). Not overridden, and the
  critical path's red run report is out of an override's reach.

## Visual review

The POV sequence (10 frames), the keeper, the spawn and the whole-map panorama,
rendered by Chunky at 64 spp (denoised) on the world the server wrote; the
interior, interact and seam scenes were not rendered. Chunky draws no entities,
so neither the keeper nor the figure is in any frame; the cutscene framing was
read on `delvec snapshot` drafts at the emitted lens poses. The hall reads from
the jetty as a stone harbour hall under a low spruce roof, its wide door open
onto a lit interior with two counters and shelves; the jetty's railings and
lantern posts lead the eye to it. From the end of the jetty the stack stands
alone on the horizon over open water, small and plain at ninety blocks. The
panorama shows the sea round the pieces and the stack; it is dim under the dusk
sky and legible.
