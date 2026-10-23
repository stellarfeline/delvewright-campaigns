# The Open Yard — generation record

## What the brief pinned down

The engine's demo-level queue row for spec-0123 §5: a short street with four
places on it — a fountain court open on all four sides in the street's
middle, joined to the street by contacts and facing the commons elsewhere; a
smithy roofed on three walls with its street side open over a counter one
cell in and its door beside; a covered market whose four sides are open and
whose roof stands on posts in the ring's corners; and a walled house for
contrast.

## What was invented here

- The fiction: Ashford's high street the day before market day, and the
  steward's runner sent to look in on every place.
- The street is a way place three wide with a verge on its south side and its
  lamps on the verge; low walls close its ring where nothing meets it.
- The court, the smithy and the market stand on the street's north side, each
  front a contact the whole width of the place; the commons between and behind
  them is a green, closed by field walls at the region's edges.
- The smithy's counter stands one cell in from the open front, so the front
  row is as wide as the front; the door is in the counter's line.
- The fountain is a single cell of water in a rim of stone bricks.

## Engine and language

Built with `delvec 1.14.0, dsl 0.65.0, mc 1.21.11` from the engine's
`feat/impl-0123a` worker branch, an unreleased tree; the round's report names
the revision.

Every piece is this campaign's own, written as a grammar program under
`programs/` by `design/build_pieces.py` from `delvec allocation --all`, and
frozen by `delvec detail --all` into `prefabs/the-open-yard-*`. The stage
documents are typed by `design/build_documents.py`.

Languages: English, and zh-CN transcreated as a sidecar.

## The design gate

A demo level carries no design record: its approved design is its queue row.
`design/` holds only the scripts; no reference image was drawn.
