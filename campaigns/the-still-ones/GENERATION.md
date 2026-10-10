# The Still Ones — generation record

## What the brief pinned down

The engine's demo-level queue row for spec-0101 pinned: a short street of
doorways with a figure in each — a skinned mannequin, a plain mob body, and
one that watches only the warder's class — every one turning to face whoever
is nearest and holding its last look out of reach; at the street's end a
fourth figure that walks away through an `approach` trigger as the party
comes near and watches again from where it stops. Small, one mechanic, minimum
cast.

## What was invented here

- The fiction: Lantern Row at dusk, the custom of the still ones, Reeve
  Annick, the tailor's sister, old Brand who dried out, the keeper who was a
  warder.
- Which body is which class: the three doorway figures are stage-5 actors
  (no dialogue owed), the walking figure is the one stage-2 NPC, so both body
  classes watch and the NPC's walk is the yield.
- The second class, Traveller, exists so that the class-only watcher has
  someone to ignore.
- The husk as the plain mob body: a mob that does not burn at dusk. The
  campaign declares `difficulty: easy` so that a hostile-category body is not
  discarded; with no waves the engine's derivation would otherwise be
  peaceful, and no diagnostic fires for a hostile actor under it.
- The reach of each watcher (7, 7, 8, 10), chosen so each figure has turned
  away from the party behind it before the next one turns, and the reeve sees
  the whole top third of the row.

## Engine and language

- `delvec 1.12.0, dsl 0.39.0, mc 1.21.11`, built from the engine's
  `integrate/sculk-sound-sight` at `6560650b70d677f5bb6a68273dc72d489e7e5629`
  — an unreleased tree, the only one carrying spec-0101. Its version string
  is the same as the released `delvec--v1.12.0`, so the version alone does not
  say which engine built this level; the revision does.
- No shipped library taken: every piece is this campaign's own, written as a
  grammar program under `programs/` and frozen by `delvec detail` into
  `prefabs/the-still-ones-*`.
- English only; no other language was asked for.

## Placement

A site plan: the street is the thing walked, and the walking is the content.

## Posture note

Three axes off the default: the reeve names the custom outright and never
explains what the still ones are beyond what she says (thematic
explicitness withheld, resolution unexplained); the level addresses the
player through its one subtitle as a statement about the street, not about
the player's feelings; and it ends on the doors closing rather than on any
understanding reached.

## The design gate

Step 4 was not passed: no reference images were drawn and no one approved a
design walkthrough. This is a demo level whose gate is the built level
itself; `design/` and `design.json` do not exist, and no showcase camera is
written.

## Target length

`target_minutes` is 10. The critical path measures 39 blocks of route (about
one minute of walking); the rest of the time is the level's content — stopping
in front of each door, stepping out of reach and back, changing class, and a
second player walking beside the first.

## Visual review (round 1)

Rendered at each scene's own budget: the POV frames leg 0 waypoints 0 and 1
(the row from the gate; arriving at the top of the row), leg 1 waypoints 4
and 7 (round the well to the reeve), the square's interior shot and the
whole-map panorama; the other 19 scenes of the 25 were not rendered. The
world save carries no entities, so no frame shows a figure.

- The row reads as a street from the gate: plastered timber fronts on both
  sides, torches between the doors, the three doorways dark openings in the
  frontage, the square's hedge closing the far end.
- A strip of grass crosses the street at each contact seam (gate to row, row
  to square): the plane cells there are the whole's fixed ring ground, which
  no piece may paint.
- From above, the fronts are one-block walls standing on open grass with the
  three small houses behind them; from the street, where the player stands,
  nothing behind them is seen.
- The square is a paved yard ringed by a hedge three high, the well a block
  of mossy brick round a full cauldron, a lantern at each corner.

## Machine proofs (round 1, after the torch fix)

- Every row torch hangs on plaster or a post: on panes the server dropped
  four of them, which the written-world check (DW0955) caught.
- The bot asserts all four watchers on the proven path, and the written-world
  record compares the server's world with the engine's model and passes.
