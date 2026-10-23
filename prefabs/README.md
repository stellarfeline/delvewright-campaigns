# The prefab library — what a piece says about its own outside

One reader: whoever adds or edits a piece here. `LICENSE-ASSETS.md` holds the
per-item licence. `generators/` holds the programs that wrote the tilesets, as
their provenance records; nothing builds or runs them.

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

## `walk_y` and `waterline_y`

`walk_y` is the local y of the cell a body's feet occupy on the piece's
principal floor, and every piece owes it. `waterline_y` is the local y of the
piece's topmost authored water block, and only a piece that really writes water
meeting a sea has one. Both are **measurements**, written by the generator that
built the piece — `delvec prefab planes --write` — never typed by hand.

## What two piece sets declare

**Why the cave set declares nothing.** Twelve of the thirteen `cave-shore`
pieces are interior passages and rooms: their sides are the cut edge of rock
and their `down` planes carry between 3.2% and 38.2% of a floor. They are built
to be buried, so they declare no face, and nothing among the shipped horizons
buries them. Declaring their sides shown would be a fiction that leaves a rock
slab in the sky with nothing saying so.

**Why the island set declares four sides and not six.** Each of its lateral
sides is the island's own edge, finished in the grass, sand and stone a player
standing in the water sees. Its `down` plane is solid substrate, which a sea
covers and nothing else does, so it is not declared and the set does not pretend
to stand on a horizon with no sea.
