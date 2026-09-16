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

Measured with `delvec prefab seating` and with one `delvec build` per cell, over
an `areas[]` campaign whose only variable is the pool and the horizon.

| pool | `void` | `ocean` | `valley` |
| ---- | ------ | ------- | -------- |
| `pool/stone-keep` | stands | stands | see below |
| `pool/vertical-keep` | stands | stands | see below |
| `pool/island` | refused | stands | see below |
| `pool/cave-shore` | refused | refused | see below |

**`valley` takes no pool.** It rings a declared extent, and an `areas[]`
campaign whose area draws from a pool declares none, so every pool is refused
there by `DW0855` — a fact about the campaign's shape, not about any piece set.
The way a piece reaches `valley` is the one `DW0855` names: one area bound to
one `prefab`, the map being that piece. `prefab/keep-spawn-hall` and
`prefab/island-beach-camp` build that way; `prefab/cave-shore` is refused at
`DW0885` on five sides, for the reason below.

**`pool/island` on `void`.** `island-beach-camp` authors an ocean of its own,
and that water runs out of 171 of the piece's own faces; `void` puts nothing
beyond them. Every island piece's `down` plane is also 100% stone — the seabed
substrate its terrain rests on — which a sea buries and nothing else does. It is
not finished exterior surface and it is not declared. The island set is built
for `ocean`, and on `ocean` all four members stand.

**`pool/cave-shore` on any open horizon.** Twelve of its thirteen members are
interior passages and rooms: their sides are the cut edge of rock and their
`down` planes carry between 3.2% and 38.2% of a floor. `prefab/cave-cavern`'s
own air reaches its box boundary at local `[0, 4, 0]`, so a party that gets out
there puts every side of every member in question; and `prefab/cave-descent`
joins its neighbours at two different rises above the walk plane, so no horizon
can be credited with burying the set at a fixed height. The set is built to be
buried and nothing in the shipped horizons buries it. Declaring its sides shown
would be a fiction, so they are not declared, and the pool is refused rather
than quietly wrong.
