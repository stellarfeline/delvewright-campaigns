# The Lever and the Keeper — generation record

## Where this run stands

**Stopped at step 9 (detail).** The design needs one lettered sign over the
lever, and this engine has no surface through which a campaign can author a
sign's letters:

- a grammar program writes no block entity and no NBT (the engine's
  `docs/reference/prefab-procedure.md` §6: "No block entities and no NBT. No
  chest loot, no sign text");
- no quest effect writes one: `set-block` and an `interact` objective's `prop`
  take a block id with a blockstate and nothing else, and no schema of
  `delvec schema --stage all` names sign text;
- no piece in the content library carries one: 187 `.nbt` files under
  `prefabs/`, `campaigns/` and `references/` read, none holding a
  `front_text` compound.

The engine draws a template's lettered sign (its test writes one into a
hand-made template), but a creator authoring through `/new-delve` cannot place
one. Building the hall without the sign would be a workaround outside the
skill, so the hall is not detailed and the machine ladder, the visual review
and the storybook wait for that capability.

Steps 1–8 are done: the documents validate, analyze and build on the
stand-ins.

## What the brief pinned down

The engine's demo-level queue row for spec-0112 pinned: one hall; one keeper
at its far end facing the door; one lever on the side wall that an `interact`
objective places when its quest activates; one lettered sign over the lever;
two hanging lanterns; a two-shot cutscene the lever fires — a push-in on the
keeper, then a landscape shot of the hall under a `set-time` cut to dusk
ordered before it. What is looked at and the three transcripts are the row's.

## What was invented here

- The fiction: the Gap House, a refuge hall at the top of Harrow Gap; Bet
  Ashby, its keeper, who bars the door at dusk and rings the gap bell so
  nobody below tries the pass in the dark. She keeps the bell handle in her
  apron, which is why the lever is only set in the wall once she has greeted
  the party.
- A porch in front of the hall, so the party arrives outside a door that can
  be shut behind them; the door opens on arrival (`obj/come-to-the-door`) and
  is barred again when the keeper is greeted (`close-gate`), so it is shut at
  the step the lever fires.
- The landscape shot stands above the porch and looks at the hall, so the
  frame shows the dusk sky.
- The arrival objective carries `marker: hidden`: the door is the only thing
  on the porch, and the row's third transcript expects `0 not drawn`, which a
  lantern marker (an item display the renderer does not draw) would break.
- One class, the Traveller.

## Posture note

The level tells the player one thing outright — the bell is rung at dusk from
the lever on the west wall — and leaves the room to show where. Bet never
explains the bell's mechanism; she says where the handle goes and how many
pulls.

## The design gate

Step 4 was not passed: no reference images were drawn and no one approved a
design walkthrough. This is a demo level whose gate is the built level itself;
`design/` and `design.json` do not exist, and no showcase camera is written.

## Engine and language

Built with `delvec 1.13.0, dsl 0.41.0, mc 1.21.11` from the engine's
`feature/review-frames-show-the-scene` at
`9595285eaf24ba9639e8a0e83e8be2c27ee908f2`, an unreleased tree and the only
one carrying spec-0112 (`cargo build --release -p delvec`, exit 0). Its
version string is the same number as the released `delvec--v1.13.0`, which
answers `dsl 0.39.0`, so the revision, not the version, says which engine
built this level. The content repository's `versions.toml` was not touched.

No shipped library piece is used; the places stand in their stand-ins.

Languages: English, and zh-CN transcreated as a sidecar by
`tools/creator/i18n-translate.py` (29 rows, 29 accepted by its fact check).

## The skill run

Authored through `/new-delve` as the engine tree above carries it
(`.claude/skills/delvewright/skills/new-delve/`, at the same revision), with
that tree's own `target/release/delvec` on `PATH` through an environment file
of its own. Init's pin check (I1b) refuses that arrangement (exit 3): it reads
the machine's shared `~/.delvewright/env.sh`, which names the released engine.
The client jar was taken from the engine's `validation/client-jar-cache.sh`
(no fetch; sha256 verified against the pin) and named by
`DELVEWRIGHT_CLIENT_JAR`. Init's I8 lines answered: the toolchain, the
fidelity gate, a grammar expansion and a palette read through the jar.

## The build on the stand-ins

`delvec build` exits 0; two builds are byte-identical (manifest sha256
`0626017217add15fe4e42c259e58de33e140218ef0949c9096af61fe65052a16`). The
review-frames binding line:

`review frames: 24 shot(s) in 4 world(s) (10 at load, 14 after a step); 24
quick, 0 hq, 3 light frame(s) rendered quick; 3 cutscene frame(s) of 2 shot(s)
in 1 cutscene(s), 0 cutscene(s) no critical step fires; cameras proven clear:
24 of 24 in their own worlds`

The four worlds: `at-load` (13888 cells, the door shut),
`after-obj-come-to-the-door` (13886, the door's two cells open),
`after-obj-greet-the-keeper` (13889, the door shut again and the lever placed)
and `after-obj-ring-the-gap-bell` (the same bytes as the one before it).

The first styled push-in, at its default distance, started on the porch and
was refused `DW0308` at the shut door in world `after-obj-ring-the-gap-bell`;
`dist: 8` starts it inside the hall.

## Findings

- **A capability gap: a campaign cannot letter a sign** (above). It blocks
  this level.
- **The `interact` review frame of an objective with a `prop` stands in the
  load world**, where the prop is not yet placed, and its `expect` line says
  "glowing lantern marker visible at the interact anchor", which an objective
  with a `prop` never has. spec-0112 §7.3 places every `interact` shot at
  load, so this frame cannot show the lever it is about.
