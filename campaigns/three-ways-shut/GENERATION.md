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
- The corridor's mouth is a barred doorway in the yard wall set back one cell,
  with a timber barricade standing across the recess. The barricade is a gate of
  its own (the station `anchor/barricade`), cleared by the same beat that lifts
  the bars, so no body reaches the bars' face before the beat and the mouth owes
  no word. The engine counts it as never met.
- The toll house door is two wide, so its bar has one thinnest axis and the
  shortcut's wrong side is decided by the engine, not guessed.
- No speaking cast, no fight. Narration carries the premise once, on arrival.

## Engine and language

Built with `delvec 1.13.0, dsl 0.57.0, mc 1.21.11` from the engine's
`feat/impl-0118` worker branch — an unreleased tree, the only one carrying
spec-0118. The version string is the released engine's number; the revision,
named in the round's report, says which engine built this level.

Every piece is this campaign's own, written as a grammar program under
`programs/` by `design/build_pieces.py` from `delvec allocation --all`, and
frozen by `delvec detail --all` into `prefabs/three-ways-shut-*`. The stage
documents are typed by `design/build_documents.py`.

Languages: English, and zh-CN transcreated as a sidecar.

## The design gate

A demo level carries no design record: its approved design is its queue row.
`design/` holds only the two scripts; no reference image was drawn.
