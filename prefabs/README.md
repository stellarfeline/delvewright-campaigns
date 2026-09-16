# The prefab library — what a piece says about its own outside

One reader: whoever adds or edits a piece here. `LICENSE-ASSETS.md` holds the
per-item licence; `pools.json` holds the piece sets a campaign draws from.

A piece's `<id>.json` is a metadata file beside its `.nbt`. Three of its fields
are the piece's claims about its outside, and the engine reads each one against
the piece's own blocks. `delvec schema --stage all` does not export them — they
belong to the library, not to a campaign stage — so their definitions live on
the engine's own prefab-metadata schema. What is written here is what they mean
for the pieces in this directory.

## `shown_faces`

**The sides of the box a player standing outside is meant to look at.** Six
words, in the piece's own frame: `east` `west` `up` `down` `north` `south`.
They turn with the placement.

A side goes in this list because the piece's blocks finish it — a grass edge, a
beach, a parapet, a rock face the silhouette was shaped for. A side stays out of
it because the piece was built to have that side covered: the cut edge of
something that belongs inside a hill, a substrate underside, the wall a
neighbouring tile is meant to close. **Absent means no side is shown**, which is
the strict answer, and it is the right answer for a piece authored to be buried.

Declaring a side is a claim, not a way to quiet a diagnostic. The engine holds
it two ways, both under `DW0886`: a side with blocks on it and no declaration is
refused where nothing else answers for it, and a declared side with no block on
it is refused everywhere. Measure before you write: read the piece's boundary
plane and see what is actually there.

Re-measure the whole library against a horizon with

    delvec --prefabs prefabs prefab seating --horizon <void|ocean|valley>

which prints, per pool, the verdict, the reason and the counts.

## `walk_y` and `waterline_y`

`walk_y` is the local y of the cell a body's feet occupy on the piece's
principal floor, and every piece owes it. `waterline_y` is the local y of the
piece's topmost authored water block, and only a piece that really writes water
meeting a sea has one. Both are **measurements**, written by the generator that
built the piece — `delvec prefab planes --write` — never typed by hand.

## What the shipped pools stand on

Not written here, because it is derivable from the pieces and a table somebody
types goes stale the first time a piece changes. `tools/check-seating.py`
derives it on every pull request — every pool in `pools.json` against every base
the pinned engine exports — and `seating-limits.toml` records the cells this
library is not expected to stand on, each with its reason and with the exact
diagnostic its refusal carries, so a refusal this library chose reads
differently from one nobody noticed. Run it on your own clone:

    python3 tools/check-seating.py --bin <path to delvec>

Two facts about the pieces sit outside that record, because neither is a seating
verdict.

**Why the cave set declares nothing.** Twelve of `pool/cave-shore`'s thirteen
members are interior passages and rooms: their sides are the cut edge of rock
and their `down` planes carry between 3.2% and 38.2% of a floor. They are built
to be buried, so they declare no face, and nothing among the shipped horizons
buries them. Declaring their sides shown would be a fiction that leaves a rock
slab in the sky with nothing saying so.

**Why the island set declares four sides and not six.** Each of its lateral
sides is the island's own edge, finished in the grass, sand and stone a player
standing in the water sees. Its `down` plane is solid substrate, which a sea
covers and nothing else does, so it is not declared and the set does not pretend
to stand on a horizon with no sea.

**`valley` reaches a piece, not a pool.** The base rings a declared extent, and
an `areas[]` campaign whose area draws from a pool declares none, so a campaign
written that way is refused at `DW0855` whatever the pool is — a fact about the
campaign's shape rather than about any piece set. The way in is the one `DW0855`
names: one area bound to one `prefab`, the map being that piece.
`prefab/keep-spawn-hall` and `prefab/island-beach-camp` build that way.
`prefab/cave-shore` does not: the surround rings the extent instead of burying
it, so the build refuses the piece at `DW0885` on five sides. A `valley` verdict
from the seating gate is about the pool's documents; what happens to a piece
placed there is the build's answer and it can differ.
