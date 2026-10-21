# Three Ways Shut — generation record

## What the brief pinned down

The engine's demo-level queue row for spec-0118 pinned a small yard with three
shut ways off it, one per way a player learns a way is shut: a barred arch
across the yard, seen the moment the player enters (`seen`); a one-way door at
the end of a short passage, met first from its wrong side, whose press says it
does not open from this side, and which the player later opens from the far
side as the loop home (`told`, a `shortcuts[]` gate); a side stair up to a
ledge with a shut hatch and a chest beside it (`rewarded`). Beside them, a long
corridor the story opens later, shut at its mouth on the yard side and hidden
by a structure that belongs to the setting, with a short close-up shot of the
opened mouth when the beat fires.

## What was invented here

- The fiction: the toll yard at Ashford Cut, shut since the floods, the keeper's
  key left in the chest on the ledge, and the lever in the toll house that raises
  the arch's bars.
- The hatch in the keeper's walk drops into the cart road. It opens with the key,
  so once the road is open it is a quick way down into it.
- The corridor's mouth is hidden behind the yard's fireplace, in the yard's
  south wall east of the keeper's stair, and is three wide, as wide as the
  stair. The fireback in the wall is the road's own bar; the recess before it
  is the mouth's approach, two high under the mantel; the embers on the hearth
  stone before the recess are a gate of their own (the station
  `anchor/hearth-fire`), cleared by the same beat that swings the fireback
  away, so no body reaches the fireback's face before the beat and the mouth
  owes no word. The engine counts it as never met. The cheeks, mantel and
  chimney breast stand beside and above the mouth's three columns, and no
  structure of the fireplace stands in the stair's three columns or its foot,
  in either state. The fire is embers, not logs: no wood stands in the way.
- The toll house door is two wide, so its bar has one thinnest axis and the
  shortcut's wrong side is decided by the engine, not guessed.
- No speaking cast, no fight. Narration carries the premise once, on arrival.

## Engine and language

Built with `delvec 1.13.0, dsl 0.59.0, mc 1.21.11` from the engine's
`integrate/batch-c` branch — an unreleased tree, the only one carrying both
spec-0118 and spec-0120. The version string is the released engine's number; the revision,
named in the round's report, says which engine built this level.

Every piece is this campaign's own, written as a grammar program under
`programs/` by `design/build_pieces.py` from `delvec allocation --all`, and
frozen by `delvec detail --all` into `prefabs/three-ways-shut-*`. The stage
documents are typed by `design/build_documents.py`.

Languages: English, and zh-CN transcreated as a sidecar.

## The design gate

A demo level carries no design record: its approved design is its queue row.
`design/` holds only the two scripts; no reference image was drawn.
