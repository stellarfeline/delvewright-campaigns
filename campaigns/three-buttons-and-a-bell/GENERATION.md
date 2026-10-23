# Three Buttons and a Bell — generation record

## What the brief pinned down

The engine's demo-level queue row for spec-0117 pinned one room off a jetty
holding every kind of thing a player presses, each answering every press in
every state with one action-bar line and one refusal cue to the presser alone:
a bell an objective opens only after the keeper has spoken; a latched door
with `requires_item` that will not open before its step and is released to
the hand once unbarred; a lever that does not flip while chained and stays
thrown once thrown; a chest that will not lift its lid before its turn and
answers *empty* ever after; three buttons whose presses count toward the bolt
objective, each `once: false` with `serves` and both answers; the rest point,
answering *not yet* before its arming beat; a boulder struck by hand that tells
its striker, once it has moved, that it is done; and a sealed shortcut door
whose own leaf answers one line from the sealed side and another from the far
side, with its unlock button on the far side lit only within six blocks on
that side.

## What was invented here

- The fiction: Merrow Landing, its keeper Tamsin Merrow, her rule that the
  house is done in its turn, the oil in her chest that frees the three
  buttons, and the three pins in the shed gate's bolt.
- The places: the covered end of the jetty where the party arrives, the
  keeper's hall off it, her store behind the latched door, and the boat shed
  behind the barred gate. The store's boarded door onto the jetty is the
  shortcut: barred on the store side, so the long way to its button is through
  the hall and the latched door, and the short way back is through it.
- The bolt is a waxed lightning rod lying on its side by the shed gate, so it
  reads as a bolt and does not weather.
- No fight. One class.

## Departures from the queue row

- **The rest point is four unlit candles, not a campfire.** A campfire at the
  bonfire's anchor is refused by the engine as a respawn cell the party cannot
  walk on from: `DW0315` reads "checkpoint anchor/candles (cell [17, 64,
  27]) strands the party: the next required anchor [10, 64, 25] (critical
  step 2) is not walkable from it over the assembled geometry". The candles
  are `minecraft:candle[candles=4,lit=false,waterlogged=false]`, boxed as a
  block the game reports no press of.
- **The latched store door stands just inside the hall, in front of its
  doorway, not in the doorway itself.** A `prop` anchored in the doorway's
  transit cell is refused (`DW0845`: the anchor resolves into the piece's
  `via:store-doorway`, not play space). The door faces into the store, so its
  leaf sits flush with the wall.
- **The bell stands on the floor, and the three buttons sit low on the wall.**
  The critical path walks to each objective's anchor cell, so every press on
  it stands on the floor course; the bell on a post and the buttons at
  shoulder height were not walkable targets.
- **The barred door onto the jetty is boarded, two wide and two high, not a
  door leaf.** A one-wide door gives the gate no single thinnest axis and the
  engine cannot tell its sides apart (`DW0425`). Each of its four boards
  carries its own answer trigger, so the whole door answers.

## Engine and language

Built with `delvec 1.14.0, dsl 0.64.0, mc 1.21.11` from the engine's
`feat/impl-0117` branch at revision `9addaa67235188e002bbcad598abf757abb49169`,
an unreleased tree carrying spec-0117. The version string is the released
engine's number; the revision says which engine built this level.

Every piece is this campaign's own, written as a grammar program under
`programs/` by `design/build_pieces.py` from `delvec allocation --all`, and
frozen by `delvec detail --all` into `prefabs/three-buttons-and-a-bell-*`. The
stage documents are typed by `design/build_documents.py`, which also writes
the zh-CN sidecar from `delvec l10n-inventory`.

Languages: English, and zh-CN transcreated as a sidecar.

## The design gate

A demo level carries no design record: its approved design is its queue row.
`design/` holds only the two scripts; no reference image was drawn.
