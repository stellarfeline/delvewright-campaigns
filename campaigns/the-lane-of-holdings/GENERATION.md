# The Lane of Holdings — generation record

## What the brief pinned down

The engine's demo-level queue row for spec-0125: one lane with four plots on
it, each planned with its program before its box and each built to it. A
dwelling on its lot — an L of the house and its cart shed, the front strip to
the door, the back yard the shed opens onto, a bed behind a hedge nobody walks;
a forge on its frontage — the shop and workroom at the lane's edge, a work yard
beside it, a store; a chapel that is the whole of its plot beside the same
chapel cut as a lidded box; a byre and its pen at the lane's end. Beside it,
the refusals as transcripts.

## What was invented here

- The fiction: Holding Lane out of the village to the fields, its four holdings
  and the byre at its end; a traveller walks to the byre and may look in
  anywhere.
- The plan: each plot's parts were listed with their use and play space, the
  box sized from them, and each part drawn in the outline `design/build_pieces.py`
  builds. The parts' cells in `layout-graph.json` are the cells the pieces claim;
  the script prints them.
- The dwelling's front is open to the lane along its whole width (an open side
  crossed by a contact); the other holdings open onto the lane through a door
  or a gate in the lane's wall.
- Every roof inside a box is closed by a parapet of two courses or set on the
  frame's top course, the lane's wall stands its full height, and the yards are
  lit from lamps set flush in the ground: nothing outside the ways is a place a
  body can climb to.

## Engine and language

Built with `delvec 1.15.0, dsl 0.69.0, mc 1.21.11` from the engine's
`feat/impl-0125` worker branch, an unreleased tree; the round's report names
the revision.

Every piece is this campaign's own, written as a grammar program under
`programs/` by `design/build_pieces.py` from `delvec allocation --all`, and
frozen by `delvec detail --all` into `prefabs/the-lane-of-holdings-*`. The stage
documents are typed by `design/build_documents.py`. The programs were written
by the session that built the engine change, not by a fresh author per place.

Languages: English.

## The design gate

A test level carries no design record: its approved design is its queue row.
`design/` holds the scripts and `design/refusals/`, the four refusals the row
asks for, each the engine's own words over a scratch copy with one edit.

## The ladder it passed

See the round's report for the ladder, run on the engine revision it names.
