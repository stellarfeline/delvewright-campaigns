# The Four Trades — generation record

## What the brief pinned down

The engine's demo-level queue row for spec-0123 §3: a lane off the critical
path with four two-room trade buildings — a smithy, a weaver's, a baker's and
a cartographer's — each with its references gathered into its node rows and
its threshold frames drawn; the weaver's is the shape that was judged bad, a
plain house with a loom in it, built right. The test is the blind read: can
each trade be named from its threshold frame alone, and does the room a
customer enters differ from the room the work is done in.

## What was invented here

- The fiction: Craft Lane off the market road, its four shops, and the old
  well at its end; a traveller walks to the well and may look in anywhere.
- Each trade stands on fourteen by fourteen of play space under a flat lid
  with a parapet; a partition two thirds of the way in divides the front shop
  (the room a customer enters, with its counter) from the workroom (the trade's
  working objects in their working positions), joined by a door and seen
  through a window.
- The size is bound in the plan on `x`, the axis every room spans whole: the
  built world re-measures a box's extent as the clear run through its middle
  under the ceiling, so the partition makes the rooms on `z` measure as rooms
  (`DW0833`).
- Each shop says its trade from the lane through its windows and its door;
  the smithy's and the bakery's chimneys carry a lit campfire on the roof.
- Nothing in the shops is a container: a barrel or a chest a player opens to
  an empty grid is refused (`DW1018`), and the shops' goods are blocks.

## The references

Gathered before the first program, two per trade, recorded in each node's
`references[]` and fetched with `scripts/references.py --all`: for each trade,
the game's own village building of the nearest trade on the Minecraft Wiki
(CC BY-NC-SA 3.0, ideas only) and the Wikipedia article on the trade
(CC BY-SA 4.0). All eight rows are pages; none is an image to fetch.

## Engine and language

Built with `delvec 1.15.0, dsl 0.66.0, mc 1.21.11` from the engine's
`feat/impl-0123b` worker branch, an unreleased tree; the round's report names
the revision.

Every piece is this campaign's own, written as a grammar program under
`programs/` by `design/build_pieces.py` from `delvec allocation --all`, and
frozen by `delvec detail --all` into `prefabs/the-four-trades-*`. The stage
documents are typed by `design/build_documents.py`.

Languages: English.

## The design gate

A test level carries no design record: its approved design is its queue row.
`design/` holds only the scripts; no reference image was drawn.

## The ladder it passed

On engine `feat/impl-0123b` at 32bc95a53 (`delvec 1.15.0, dsl 0.66.0`):

- two builds byte-identical, manifest sha256 `e6e946ef755f5d959dc9…`;
- PackTest: all 14 required tests passed;
- the bot: the critical path walked, passed;
- the written world: 18853 non-air cells written, 18853 in the server save, all compared, none differing;
- the build's own lines: `doors framed: 8 of 8`; `threshold shots: 12 over 6 place(s), 8 door(s), 4 open side(s)`;
- the staging gate: refused on one row only, `latch-01` (the doors' thin-panel shape class, an open capability gap recorded in the same round), and admitted under an override that names it.
