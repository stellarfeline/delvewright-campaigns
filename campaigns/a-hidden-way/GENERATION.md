# A Hidden Way — generation record

## What the brief pinned down

The engine's demo-level queue row for spec-0118's fourth word, `hidden`: a
hidden passage behind an opaque shutter, revealed only by its close-up shot,
with text that never tells it first — and one problem only, so no stair, no
street and no second way to judge.

## What was invented here

- The fiction: the keeper's hall at Ashby, its great hearth lit three
  generations ago, and the valve beside it that floods the flue.
- The hearth is built as The Hearth Door's is: the mouth three wide in the
  hall's north wall, cheeks beside it and a mantel over it, the fire on the
  hearth stone before the recess a gate of its own (`anchor/hearth-fire`),
  and the firebox's back — `minecraft:bricks`, a block the game draws as a
  full opaque cube — the way's own bar (`anchor/seam-hearth-door`). The beat
  that turns the valve puts the fire out, swings the back away, and plays a
  close-up shot of the opened mouth; the line after the shot names what it
  showed.
- The text before the shot says what is in view and what to do: the hearth
  burns, the valve is on the wall to its right. It says nothing of what lies
  behind. The connection declares `learned: hidden` with `secret: ["passage",
  "behind the hearth", "密道"]`.
- A porch south of the hall is the way in. No speaking cast, no fight.

## Engine and language

Built with `delvec 1.13.0, dsl 0.62.0, mc 1.21.11` from the engine's
`feat/impl-way-hidden` worker branch — an unreleased tree, the only one
carrying spec-0118's amendment. The version string is the released engine's
number; the revision, named in the round's report, says which engine built
this level.

Every piece is this campaign's own, written as a grammar program under
`programs/` by `design/build_pieces.py` from `delvec allocation --all`, and
frozen by `delvec detail --all` into `prefabs/a-hidden-way-*`. The stage
documents are typed by `design/build_documents.py`.

Languages: English, and zh-CN transcreated as a sidecar.

## The refused shapes

`design/probes/` holds three: the firebox's back built of blocks the eye looks
through (`DW1054`, the eye), the beat's shot turned on something else
(`DW1054`, the shot), and the arrival line saying what lies behind the hearth
(`DW1060`). `design/check_probes.py <delvec> <prefabs> <scratch>` puts each
through the engine and requires the code it names.

## The design gate

A demo level carries no design record: its approved design is its queue row.
`design/` holds only the scripts and the probes; no reference image was drawn.
