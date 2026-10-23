# The Hearth Door — generation record

## What the brief pinned down

The engine's demo-level queue row for spec-0120, and the brief that built it,
pinned a hall with a stone stair three wide, and at the stair's foot the mouth
of a passage the story opens later, hidden behind a fireplace built right: the
hearth's cheeks and mantel beside and above the mouth's declared width, the
fire and its grate the way's own gate, cleared by the beat that opens it, and
nothing of it in the stair's three columns; a newel post one column wide at
the stair's foot inside its width, declared; a street way place with one lamp
post inside its width, declared; and the refused shapes as probes.

Rebuilt when the engine withdrew the declaration that excused a structure in a
way's width (spec-0120's amendment): the newel moved onto the hall floor
beside the bottom tread, at the rail's end, and the lamp post onto the lane's
verge, each outside the width it stands beside, and both declarations left
with the surface. The level now confirms the stair alone. The hearth's passage
is declared `learned: hidden` with its secret (spec-0118's amendment), its
back the brick of the firebox rather than a grate, and the text before the
sluice rewritten to say nothing of what lies behind it, so the level builds;
the hidden way is confirmed on a demo level of its own, A Hidden Way.

## What was invented here

- The fiction: the wardens of Coldharbour, their records behind the hearth, and
  the sluice at the end of Wardens' Lane that floods the flue.
- The lane is the stair's head: a street four wide open to the sky, cut in the
  rock five courses over the hall, with hay along its verge outside its width.
- The fire burns on the hearth stone before the mouth's recess and is a gate of
  its own (`anchor/hearth-fire`), cleared by the same beat that raises the
  grate at the hearth's back (`anchor/seam-hearth-door`); the recess under the
  mantel is the mouth's approach, two high.
- A porch south of the hall is the way in, so the hall has a door the party
  arrives by.
- No speaking cast, no fight. Narration carries the premise once, on arrival.

## Engine and language

Built with `delvec 1.13.0, dsl 0.62.0, mc 1.21.11` from the engine's
`feat/impl-way-hidden` worker branch — an unreleased tree, the only one carrying
both amendments. The version string is the released engine's number; the revision,
named in the round's report, says which engine built this level.

Every piece is this campaign's own, written as a grammar program under
`programs/` by `design/build_pieces.py` from `delvec allocation --all`, and
frozen by `delvec detail --all` into `prefabs/the-hearth-door-*`. The stage
documents are typed by `design/build_documents.py`.

Languages: English, and zh-CN transcreated as a sidecar.

## The refused shapes

`design/probes/` holds one: the hearth's chimney breast built one column into
the stair's foot (`DW1057`).
`design/check_probes.py <delvec> <prefabs> <scratch>` puts each through the
engine and requires the code it names.

## The design gate

A demo level carries no design record: its approved design is its queue row.
`design/` holds only the scripts and the probes; no reference image was drawn.
