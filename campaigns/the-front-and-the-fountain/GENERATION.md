# The Front and the Fountain — generation record

## What the brief pinned down

The engine's demo-level queue row for spec-0123 §3.5: one short street with
four places on it — a smithy whose open front is a frame of posts and a beam
where the wall would have been, its counter under the beam and its door in the
frame under the same head; a square whose centrepiece is water raised on a
stack over a basin; and beside them the two shapes the ruling judged, a
free-standing two-course door beside a one-course counter under a five-course
open face, and a flat ring round one cell of water — each with its own
threshold frame, and the census naming the free-standing door as the one
unframed door, `doors framed: 1 of 2`.

## What was invented here

- The fiction: Tanner's Row before the fair, and the town warden walking it.
- The row is a way place three wide with a verge on its south side; the four
  places stand on its north side, each front a contact the whole width of the
  place, three cells of green between them so each open side's approach is
  the commons.
- The smithy's frame stands behind the front's first row, not in it: the row's
  contact crosses onto that row, and its clear width keeps every column of it
  clear (`DW1057`), so a counter or a post in it is refused. The stall's
  counter and door stand on the same row for the same reason.
- The warden's lodge across the row, behind an open doorway, is the plan's one
  portal (a doorway with no door, so the census's door line counts the row's two fronts); nothing is judged in it. It is there because the findings ledger
  binds its clear-width rows (`tws-01`, `thd-01`) over a plan's portal seams,
  and a row of contacts alone measured those rows as unbound.
- The fountain's water stands: a piece's water is still (`DW0800` refuses a
  source with open air beside or below it), so the bowl on the stack holds its
  water and does not pour it into the basin.

## Engine and language

Built with `delvec 1.15.0, dsl 0.66.0, mc 1.21.11` from the engine's
`feat/impl-0123b` worker branch, an unreleased tree; the round's report names
the revision.

Every piece is this campaign's own, written as a grammar program under
`programs/` by `design/build_pieces.py` from `delvec allocation --all`, and
frozen by `delvec detail --all` into `prefabs/the-front-and-the-fountain-*`.
The stage documents are typed by `design/build_documents.py`.

Languages: English.

## The design gate

A test level carries no design record: its approved design is its queue row.
`design/` holds only the scripts; no reference image was drawn.

## The ladder it passed

On engine `feat/impl-0123b` at 32bc95a53 (`delvec 1.15.0, dsl 0.66.0`):

- two builds byte-identical, manifest sha256 `757f591420d8120637d9…`;
- PackTest: all 14 required tests passed;
- the bot: the critical path walked, passed;
- the written world: 13730 non-air cells written, 13730 in the server save, all compared, none differing;
- the build's own lines: `doors framed: 1 of 2`; `threshold shots: 12 over 6 place(s), 2 door(s), 10 open side(s)`;
- the staging gate: refused on one row only, `latch-01` (the doors' thin-panel shape class, an open capability gap recorded in the same round), and admitted under an override that names it.
