# An Item Laid at a Place — generation record

## What the brief pinned down

The engine's `docs/demo-levels.md` row for spec-0114 pinned: a small chapel
loft at dusk; the party takes a muster roll from a chest below, climbs to the
loft, and lays the roll on the lectern there; the objective is titled with a
placing word (*Lay the roll on the lectern*); the roll leaves the hand at the
click; the lectern then shows it, through a `set-block` of a lectern holding a
book in `on_objective_complete`; a second beat hangs a lantern on a hook the
same way. Its "what to look for": the roll is gone from the inventory the
moment the lectern is used, the lectern shows it, and nothing completes on
arrival alone.

## What was invented here

- The fiction: the chapel of Wending Cross, the muster at first light, the
  clerk who keeps the roll, the night watch the lantern is for.
- The lantern's source: a barrel at the foot of the loft stair, adopted by a
  second `collect`, so that each loft beat has its own item taken from the
  nave below.
- The hook: the bottom link of an iron chain hanging from the loft beam. The
  `interact` prop is that link; hanging the lantern replaces it with a lantern
  that hangs from the chain above.
- No objective for climbing to the loft: arriving there is not a beat, so the
  first thing the loft completes on is a click with an item held.

## Engine and language

- `delvec 1.13.0, dsl 0.51.0, mc 1.21.11`, built from source from the engine's
  `feature/an-objective-says-its-act` at
  `342b8a64dcb1b3b0989570b2d782c6c5f6d27029`, the unreleased tree that carries
  spec-0114. Its version string is the same as the released `delvec--v1.13.0`,
  so the revision, not the version, says which engine built this level.
- No shipped library taken: every piece is this campaign's own.
- Languages: English, and `zh-cn` transcreated from the English.

## The design gate

Not held. A demo level is confirmed on the finished thing: no reference images
were drawn, so there is no `design.json` and no `design/cameras.json`.
