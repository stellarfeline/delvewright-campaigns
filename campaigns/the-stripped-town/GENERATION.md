# The Stripped Town — generation record

## What the brief pinned down

The engine's demo-level queue row for spec-0105 pinned: one street of three
houses and a smokehouse; every cupboard in two of the houses is scenery, the
third holds the one parcel the story needs, and the smoker holds a cooked fish
in its result slot; the arrival line says the town was emptied. It is the first
read of whether the line, heard once at arrival, stops a player opening the
containers, and of whether a stocked smoker reads as a find. Small, one
mechanic, minimum cast. The engine caps scenery at two containers per place and
refuses scenery among containers that matter; those rules are the design.

## What was invented here

- The fiction: Saltlow, the herring that moved off, the town going inland in
  the autumn, Ansel Tarrow the ferryman, his sister Marra and her parcel.
- Which houses are which: the net-maker's and the chandler's are the stripped
  pair (two scenery containers each, at the cap); Marra's cottage is the third
  house, holding one chest and nothing else.
- The smoker's three slots: a raw salmon in the input slot, charcoal in the
  fuel slot, two smoked cod in the result slot. A smoker does not fire while its
  result slot holds something its input cannot become, so the world as loaded
  is still; once a player takes the cod, the smoker lights and smokes the
  salmon.
- The arrival line's sound, a barrel lid closing.
- One class, the Carrier, so the kit says why the party is here.

## Engine and language

Built with `delvec 1.13.0, dsl 0.43.0, mc 1.21.11` from the engine's
`feature/containers-are-declared` at
`4d531ea2041c15b3cb8e9f37fd82c240406e4986` — an unreleased tree, the only one
carrying spec-0105. Its version string is the same number as the released
`delvec--v1.13.0` (which answers `dsl 0.39.0`), so the version alone does not
say which engine built this level; the revision does.

No shipped library taken: every piece is this campaign's own, written as a
grammar program under `programs/` and frozen by `delvec detail` into
`prefabs/the-stripped-town-*`.

Languages: English, and zh-CN transcreated as a sidecar.

## Posture note

The level tells the player one thing outright — the town is empty, and what is
left was left on purpose — and lets the street confirm it. Ansel explains only
the errand, never the town's grief; the end is the boat leaving, not a
reflection on it.

## The design gate

Step 4 was not passed: no reference images were drawn and no one approved a
design walkthrough. This is a demo level whose gate is the built level itself;
`design/` and `design.json` do not exist, and no showcase camera is written.

## Target length

`target_minutes` is 10. The critical path measures 107 blocks of route over
six legs of the built map (about two minutes of walking); the rest is the
level's content — reading Ansel, opening (or not opening) the containers in
four houses, finding the smoker.

## The skill run

Authored through `/new-delve` as the engine tree above carries it
(`.claude/skills/delvewright/skills/new-delve/`, at the same revision), not
through an installed plugin. The skill's Init has no way to name an unreleased
engine revision: creator mode pins a release tag, and dev mode reads the
engine checkout's `campaigns/` link, which points at another content checkout.
The run used that tree's own binary, `target/release/delvec`, built with
`cargo build --release -p delvec` (exit 0), through an environment file of its
own rather than the machine's shared `~/.delvewright/env.sh`. Init's pin check
(I1b) refuses that arrangement (exit 3): it reads the shared `env.sh`, which
names the released engine, and offers no way to name this tree without
rewriting it.

## Container census, as built

`container census: 6 container cell(s) in the assembled world
(minecraft:barrel: 2, minecraft:chest: 3, minecraft:smoker: 1); 1 loot,
1 collect, 0 device, 4 decoration; notice declared; by place:
node/chandlers: 2, node/marras-house: 1, node/net-house: 2,
node/smokehouse: 1; arrangement: 0 mixed place(s), 0 over the cap of 2
decoration cell(s) per place.` The ledger's `census_input_sha256` is
`c290ddc8ade2eae4914827fe567f41b907e9e1f01a1b898f4a59ed96e06d9942`, and it
lists no place still standing in its stand-in (`stand_ins: []`). The fill
binding: `container binding: 2 container fill(s) (1 loot, 1 adopting
collect), 2 judged against the assembled world, 0 deferred to the detail of a
place still standing in its stand-in.`

A copy with one extra barrel in Marra's house was refused `DW1024` (mixed);
the transcript is in the storybook. On this engine, a copy whose program puts
a barrel where Marra's table stands is refused by `delvec detail` and by
`delvec build` (exit 3) with the same message, the barrel named at
`[8226, 64, 8195]`.

## Machine ladder

On the build whose manifest sha256 is
`03788292c3acb4a86243047817820bfbfb2b65d82b5deda8873bb3a41f19c937` (two
builds byte-identical):

- PackTest: 22 of 22 required tests passed, `v06_loot_smoker` and
  `watch_npc_ansel` among them.
- Bot: critical path passed, 5 steps; `container notice: ok — the chat notice
  arrived in the class step's window; its sound minecraft:block.barrel.close
  arrived at [8195.5,64,8202.5], the bot at [8195.5,64,8202.5] after the
  warp`; `cue binding: 4 of 4 owed cue(s) arrived at the bot`; `[watch] 1
  watcher(s) in the record, 1 within reach on the proven path, 1 asserted`
  (Ansel watches the party by default, `DW1025`). Die-retry and the death
  loop are unbound (no combat, no death plan), stated by the run.
- Written world (`DW0955`): 1447 non-air cells compared, 0 differing in the
  model class; the differences are the named server re-derivations (85 cells:
  leaf distance and wall connections) and grass under blocks turning to dirt
  (2 cells, random tick).

## Visual review

The frames were drawn from the world save of the build at manifest
`c6c4e03c1f59942a7c1ce7a807e798912fb31aa8c780e82df18fd8ae76cc0b00`. That
build and this one emit the same structures and the same render plan, and the
engine's at-load world model of both is
`460a35459eaedc34902ff6922d154c412b21c650132bdc9afe7fa7823a554d9e`; the two
differ only in the class function, its PackTest and the ledgers, so the frames
are this build's.

Rendered at each scene's own budget: the POV frames leg 0 waypoints 0 and 1
(the street from the road; arriving at Ansel), leg 1 waypoint 10 (arriving at
Marra's chest), leg 2 waypoint 8 (back at Ansel), Ansel's NPC shot and the
whole-map panorama. The other 33 of the 39 scenes were not rendered. The
world save carries no entities, so no frame shows Ansel.

- The street reads as a lane between hedged gardens and four cottages, the
  quay's wall closing the far end. A strip of grass crosses the street at the
  road's contact seam: the whole's fixed ring ground.
- Arriving at Marra's chest, the frame looks over the chest's lid at the
  pallet bed — white wool under a blue blanket — with the window beside it:
  the chest reads as standing at the foot of the bed.
- The quay reads as a walled stone yard, not a quay: there is no water, and
  the engine refuses water in the walk model (spec-0038), so the ferry and
  the sea are not built rather than faked. The arrival frames at Ansel face
  the quay's east wall.
- The cottages are boxes under flat plank lids; they read as small houses
  from the street, and as sheds from above.
- The interior shots (`interior/site/3`–`6`) stand above each cottage's lid
  and frame its roof from outside (rendered once at 32 samples to see this),
  so the interiors were judged on CPU drafts (`delvec snapshot`) from inside
  each doorway: the stripped pairs stand against the back walls, the smoker
  stands alone against the smokehouse's back wall facing the door.
