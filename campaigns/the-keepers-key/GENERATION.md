# The Keeper's Key — generation record

## What the brief pinned down

The engine's demo-level queue row for spec-0124: a hall and a store with one
door between them, shut by the door itself. A keeper hands over a key; before
it the door answers *locked* and the way is barred; with the key in hand one
press unbars it, and from then on it opens and shuts by hand onto the store. In
the store a lever opens the shed gate across the yard, out of view, and the
beat cuts to a shot of the gate. At the hearth a rest point whose two buttons
are captioned in the engine's defaults. The level confirms the door-shut seam
alone.

## What was invented here

- The fiction: the toll house at Varley Ford, its keeper Hob Varley, the punt
  in the shed across the yard.
- The lever is padlocked, and the keeper's one key opens both the door and the
  padlock: so the lever is a key objective too, and its effect, out of sight
  from the store, is the one the shot shows.
- The shed gate is barred, and its two bar cells each answer a press with
  where the gate is worked from: that is how the player learns it is shut.
- The plan: the yard is pinned and open to the sky; the hall hangs off its
  north face, the store off the hall's east face, the shed off the yard's south
  face. The hall owns the store door's plane, so the hall's piece ships the
  door against the gate region it owes.

## Engine and language

Built with `delvec 1.15.0, dsl 0.68.0, mc 1.21.11` from the engine's
`feat/impl-0124` branch, an unreleased tree; the round's report names the
revision.

Every piece is this campaign's own, written as a grammar program under
`programs/` by `design/build_pieces.py` from `delvec allocation --all`, and
frozen by `delvec detail --all` into `prefabs/the-keepers-key-*`. The stage
documents are typed by `design/build_documents.py`.

Languages: English.

## The design gate

A test level carries no design record: its approved design is its queue row.

## The ladder it passed

See the round's report for the ladder, run on the engine revision it names.
