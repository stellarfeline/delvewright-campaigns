# The Armoury — generation record

## What the brief pinned down

The engine's demo-level queue row for spec-0111 pinned: one room with a rack
of three armour stands (a helmet, a sword, a shield in the off hand), a map in
a glow item frame beside the door, and a chest holding nothing but arrows
under the window; the quest item is the sword, taken from its stand. It is the
first read of whether a player understands, unprompted, that the worn sword is
theirs to take, and of where on a stand players click. Small, one mechanic,
minimum cast. Holders are placed by the piece and owned by the engine;
`loot[]` and `collect` fill them by slot.

## What was invented here

- The fiction: Greyholt, a watch-house on a moor road; Ide Fenwick, its keeper
  for thirty winters, handing the post over to the new watch; the post sword
  that goes with the post.
- A yard in front of the armoury, so the warden has somewhere to stand that is
  not the room the level is about, and the sword has somewhere to be carried
  to.
- Which stand is which: the shield to the north, the sword in the middle, the
  helmet to the south. The frame is east of the door on the door wall; the
  window is in the middle of the north wall with the chest under it.
- One class, the New Watch, carrying a bow and four arrows, so the chest of
  arrows is worth opening and the sword is the one blade in the party's hands.

## Posture note

The level tells the player one thing outright — the sword on the rack is the
post's, and the post is theirs now — and leaves the room to show how a sword
on a stand is taken. Ide never says how to take anything; she says where it
is and whose it is. The end is her walking down the road, not a speech.

## The design gate

Step 4 was not passed: no reference images were drawn and no one approved a
design walkthrough. This is a demo level whose gate is the built level itself;
`design/` and `design.json` do not exist, and no showcase camera is written.

## Engine and language

Built with `delvec 1.13.0, dsl 0.49.0, mc 1.21.11` from the engine's
`feature/holders-hold-items` at
`92f00562574ab4c05f4386f8f0fb7c8814aa5e40` — an unreleased tree, the only one
carrying spec-0111. Its version string is the same number as the released
`delvec--v1.13.0` (which answers `dsl 0.39.0`), so the version alone does not
say which engine built this level; the revision does. The content
repository's `versions.toml` `[engine].ref` names the engine a release is
built with and was not touched: nothing in the skill or the content repository
names an unreleased engine revision for one campaign, so this record is where
the revision is written.

No shipped library taken: both pieces are this campaign's own, written as
grammar programs under `programs/` at program version `1.12.0` (the version
that carries `holder` on a `mark`) and frozen by `delvec detail` into
`prefabs/the-armoury-*`.

Languages: English, and zh-CN transcreated as a sidecar.

## The skill run

Authored through `/new-delve` as the engine tree above carries it
(`.claude/skills/delvewright/skills/new-delve/`, at the same revision), not
through an installed plugin, with that tree's own `target/release/delvec`
(`cargo build --release -p delvec`, exit 0) on `PATH` through an environment
file of its own. Init's pin check (I1b) refuses that arrangement (exit 3):
it reads the machine's shared `~/.delvewright/env.sh`, which names the
released engine, and offers no way to name this tree without rewriting it.

The skill page is held to the released engine, so it does not yet describe
the holder surface: its *Items, containers and loot* still names
`collect.container` (this engine spells it `collect.holder`) and does not
mention `LootItem.slot` or `mark.holder`. The surface was read from
spec-0111, `docs/reference/grammar.md` and
`docs/reference/delvec/compiler/holders.md` in the engine tree.

## The sword sits on its stand's head

The demo row wants the post sword *worn* by its stand and taken from it. A
`collect` adopting an armour stand fills the stand's first slot, which is
`armor.head`, and nothing in the document can name another: `collect` has no
`slot` field (a copy carrying `"slot": "weapon.mainhand"` on the objective is
refused `DW0100`, unknown field `slot`). So in this build the sword is on the
middle stand's head, the bot takes it by clicking the head band
(`click_height` 1.78), and the stand reads as wearing a sword for a helmet.
The helmet, the shield and the map are `loot` fills, which do name their
slots, and sit where the design puts them. The sword stand moves to
`weapon.mainhand` once `collect` can say which slot its item lands in; nothing
else in the campaign changes.

## Known engine issue

The quest interface sounds — the new-objective chime, the objective-complete
sound and the campaign-complete toast — play at the world spawn rather than at
the player, on this engine revision.

## Holder census, as built

`holder census: 5 holder(s) in the assembled world (armor-stand: 3,
container: 1, glow-item-frame: 1); 4 loot, 1 collect, 0 device, 0 decoration,
0 empty (frozen), 4 exempt (contents show from outside); notice none; by
place: node/armoury: 5; arrangement: 0 mixed place(s), 0 over the cap of 2
decoration cell(s) per place. stance: 4 filled holder(s) and 4 holder(s)
judged, 0 unsupported, 0 unreachable.` The fill binding: `holder binding: 5
fill(s) (4 loot, 1 adopting collect; by kind: armor-stand: 3, container: 1,
glow-item-frame: 1), 5 judged against the assembled world, 0 deferred to the
detail of a place still standing in its stand-in.` The runtime-edit pair:
`holder edits: 0 runtime edit(s) examined against 4 holder entit(y/ies), 0
reaching a holder (DW1038).` The ledger's `census_input_sha256` is
`6ff94d9f25d61e4076766396b55df1ba23701dc88d6cc9b9bd41ed5e5f40663d`.

The critical path's stance for the sword stand is the stand's own foot
cell (`[8198, 64, 8200]`): the stance pass reads the block model, in which a
stand is not an obstacle, so the nearest standable cell to a stand is the cell
it stands in. A player can stand there — a stand does not collide — and the
take works from inside it, but the bot's walk and the arrival frame end
inside the stand rather than in front of it.

A copy whose shield is filled into `armor.chest` instead of `weapon.offhand`
is refused at `validate` (`DW1035`): the game puts a stack in `armor.chest`
only when its `equippable` slot is `chest`, and a shield's is not.

## Target length

`target_minutes` is 10. The critical path measures 14 blocks of route over two
legs of the built map; the rest of the level is the room — reading Ide,
looking at the rack, the frame and the chest, and taking what the party wants.

## Machine ladder

On the build whose manifest sha256 is
`af27012dd0fdac1fff06fa63cf0f7e2253faf32fad177fd442869012778d09ed` (two
builds byte-identical):

- PackTest: 23 of 23 required tests passed, the four `holder_*` templates
  among them (one per filled entity holder: the three stands and the glow
  frame, the frame's including the emptied-frame freeze).
- Bot: critical path passed, 5 steps, the sword taken from its stand by the
  stand's own click. Die-retry and the death loop are unbound (no combat,
  no death plan), stated by the run. No branch plan is emitted.
- Written world (`DW0955`): 455 non-air cells compared, 0 differing in the
  model class; the differences are one named server re-derivation (the lamp
  post's lower wall block drawn `south=tall` where the model writes `low`)
  and one grass cell under a block turning to dirt (random tick).
- Staging gate: stageable; 75 of 123 finding classes inapplicable to this
  campaign, none red.
