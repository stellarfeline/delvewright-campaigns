# The Latch — generation record

## What the brief pinned down

The engine's demo-level queue row for spec-0123 §3.1: a cottage of two rooms
with a closed oak door between them on the critical path, an oak trapdoor
over the cellar stair, a fence gate in the yard, and the way out an iron door
the story opens at its beat — every door a body meets built as a door.

## What was invented here

- The fiction: old Wenna's cottage, her locked garden, and the latch she left.
- The yard is hedged all round, open to the sky, with a hedge across it and
  the gate on the path; the front door is oak too.
- The cellar is as wide as the cottage, so its walls stand under the
  cottage's and the back room's floor is whole; three trapdoors lie over its
  stair, which climbs under them so each rise is jumped with headroom. Their
  hinges are on the hole's west side (`facing=east`), so each open panel hangs
  along the climb and a body steps off the top tread east onto the floor; a
  hatch turned across the climb shuts a body in under it (`DW1066`).
- The latch is a floor lever by the back room's east wall, away from the
  iron door: a lever beside the door's wall would power it (`DW1047`).
- The iron door's bar is declared as the door's lower half
  (`design/build_pieces.py`, role `garden-door`); the program lays the upper
  half over it, and the engine derives the same two states for the gate
  region from the one declared block.

## Engine and language

Built with `delvec 1.14.0, dsl 0.65.0, mc 1.21.11` from the engine's
`feat/trapdoor` worker branch, an unreleased tree that reads a trapdoor's shape
per state; the round's report names the revision.

Every piece is this campaign's own, written as a grammar program under
`programs/` by `design/build_pieces.py` from `delvec allocation --all`, and
frozen by `delvec detail --all` into `prefabs/the-latch-*`. The stage
documents are typed by `design/build_documents.py`.

Languages: English, and zh-CN transcreated as a sidecar.

## The design gate

A demo level carries no design record: its approved design is its queue row.
`design/` holds only the scripts; no reference image was drawn.
