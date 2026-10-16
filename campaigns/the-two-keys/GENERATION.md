# Two Keys — generation record

## What the brief pinned down

The engine's demo-level queue row for spec-0018 pinned: a two-player vault
where progression is provably split, by `carrier: one` items and AND-join
objectives, and which a single player can still complete (`min_players` at its
floor of 1). Small, one mechanic, minimum cast.

## What was invented here

- The fiction: the Staple Hall at Marrowby, a wool guild's hall; its
  strongroom with two locks; the rule that the Warden's key and the Clerk's key
  are kept in two rooms and that the steward who keeps the door holds neither;
  Hesketh Marr, the steward; the charter that has to be out by dawn.
- The map: one row of three rooms west to east (the archive, the hall, the
  counting room) and the strongroom behind the hall's north wall, behind a
  barred door.
- The split: each arm is a key taken in its own wing (`interact`, then
  `give-item` with `carrier: one`) and turned in its own lock beside the
  strongroom door (`interact` with `requires_item`, the key held). The two keys
  are different items — a trial key and an ominous trial key — so a lock
  answers to one key only. The join is a `talk-to` with Hesketh whose `after`
  names both locks; its completion opens the strongroom door.
- One class, the Journeyman, carrying a lantern and bread: no weapon, because
  nothing in the level fights.

## Posture note

The level is told by its rule, not by its dramatics: Hesketh states the rule
once, plainly, and the building enforces it — two doors, two rooms, two locks.
Nothing is in danger and nothing escalates; the beat that lands is the second
click, when a door that held after the first lock opens. The end is a deed on a
table and a steward who will keep the door till morning.

## The design gate

Step 4 was not passed: no reference images were drawn and no one approved a
design walkthrough. This is a demo level whose gate is the built level itself;
`design/` and `design.json` do not exist, and no showcase camera is written.

## Engine and language

Built with `delvec 1.13.0, dsl 0.41.0, mc 1.21.11` from the engine's `main` at
`d1d499c71b9227ec68593568bfb2016f209f88d8`, built locally with
`cargo build --release -p delvec` (exit 0). Its version string is the same
number as the released `delvec--v1.13.0` (which answers `dsl 0.39.0`), so the
version alone does not say which engine built this level; the revision does.
The content repository's `versions.toml` `[engine].ref` names the engine a
release is built with and was not touched.

No shipped library taken: all four pieces are this campaign's own, written as
grammar programs under `programs/` at program version `1.10.0` and frozen by
`delvec detail` into `prefabs/the-two-keys-*`.

Languages: English, and zh-CN transcreated as a sidecar by the provider
(`tools/creator/i18n-translate.py`, 58 rows, 58 accepted by its fact check).
The provider's batches rendered four names two ways each (the Warden, the
Clerk, the charter, the strongroom); 25 rows were rewritten through
`delvec l10n-apply` so each name has one rendering.

The steward's face is composed by the skin toolchain from `skins/cast.json`.

## The skill run

Authored through `/new-delve` as the engine tree above carries it
(`.claude/skills/delvewright/skills/new-delve/`, at the same revision), not
through an installed plugin, with that tree's own `target/release/delvec` on
`PATH` through an environment file of its own. Init's pin check (I1b) refuses
that arrangement (exit 3) in both modes: it reads the machine's shared
`~/.delvewright/env.sh`, which names the released engine, and offers no way to
name this tree without rewriting it.

## The party mechanic, as built

- One AND-join of the campaign's 8 objectives: `obj/open-the-strongroom`,
  `after: [obj/turn-the-warden-lock, obj/turn-the-clerk-lock]`. The build
  emits one division-of-labour PackTest for it,
  `party_join_open_the_strongroom`, which spawns a second player, has the
  first turn the Warden's lock and the second the Clerk's, asserts the join
  shut before either, still shut after one, open after both, and has the
  second player complete the join.
- Two `give-item` effects, both `carrier: one`; each compiles to
  `give @s …` in the completion function of the objective whose click fired
  it.
- The engine prints no binding line for either: no count of AND-joins bound
  to a PackTest, and none for `carrier` or for the `min_players` division
  proof.
- Declaring `min_players: 2` on this design analyzes clean. With the Clerk's
  key made to wait on the Warden's lock, it is refused at `analyze` with
  `DW0358` (the widest join offers 1 arm reachable at once). Handing the
  Warden's key from a `move-npc` `on_arrive`, which no player drives, is
  refused at `validate` with `DW0357`.

## Target length

`target_minutes` is 12. The critical path measures 54 blocks of route over six
legs of the built map; the rest of the level is reading the steward, the two
rooms and the locks, and — with two players — finding each other again in the
hall.

## Machine ladder

On the build whose manifest sha256 is
`3dc1c84f41eed483eb368ee708c6fdc65405f30ab34a98448e2da0033449e04d` (two builds
on one machine byte-identical), every rung run locally:

- PackTest: **green**, all 30 required tests passed (29 generated templates),
  `party_join_open_the_strongroom` among them.
- Bot: critical path passed, 10 steps; each lock turned with its own key held
  (`minecraft:trial_key`, `minecraft:ominous_trial_key`). 9 of 9 owed cues
  arrived at the bot. Die-retry and the death loop are unbound (no combat, no
  death plan), stated by the run. No branch plan is emitted. The harness runs
  one bot, so no machine has watched a `carrier: one` key reach one player and
  not another.
- Written world (`DW0955`): 1037 non-air cells compared, 0 differing in the
  model class; the differences are six grass cells turned to dirt (random
  tick).
- Staging gate: not run here; it runs at `playtest-server.sh up`.

## Visual review — deferred

No Chunky scene was rendered; the visual review waits for the Lumenwright
review frames. The four rooms were looked at on CPU drafts (`delvec snapshot`)
from their doorways for layout only.
