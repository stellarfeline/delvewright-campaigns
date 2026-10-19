# An Item Laid at a Place — design

The demo level for **an item laid at a place** (spec-0114): an objective's
title opens on the act that completes it, and an `interact` with
`requires_item` and `takes_item: true` takes one of the presented item from the
hand at the click. One mechanic in the spotlight, one class, no speaking cast,
about ten minutes.

## The places

A small parish chapel at dusk, sealed: the party arrives inside it. Grid: x
east, z south.

| place | box | floor | what it is |
|---|---|---|---|
| `node/nave` (entry) | x 8188–8194, z 8182–8194 | 64 | the nave: the altar at the north end, pews either side of the aisle, the vestry chest beside the altar, a barrel at the foot of the loft stair |
| `node/loft` (goal) | x 8188–8194, z 8196–8199 | 69 | the loft at the south end, five up: a glazed screen in its front looking down the nave, the reading lectern against the screen, an iron chain hanging from the ceiling beside it |

One connection, `edge/loft-stair`: a timber stair up the nave's west wall to
a doorway at the west end of the loft's front. The rest of that front is a
glazed screen: the site plan allocates one opening in the wall, and an open
rail there would be a second way between the places that the plan never
agreed to (`DW0836`).

## The beats, in order

One quest, `quest/the-roll`, from campaign start.

| # | objective | kind | where | what the player does | what the world does |
|---|---|---|---|---|---|
| 1 | *Take the muster roll* (`obj/take-the-roll`) | `collect`, adopting the vestry chest | nave | takes the roll (`minecraft:writable_book`, named *Muster Roll of Wending Cross*) out of the chest | — |
| 2 | *Take the watch lantern* (`obj/take-the-lantern`) | `collect`, adopting the barrel | nave | takes the lantern (`minecraft:lantern`, named *Watch Lantern*) out of the barrel | — |
| 3 | *Lay the roll on the lectern* (`obj/lay-the-roll`) | `interact` at the lectern, `prop` an empty lectern, `requires_item: minecraft:writable_book`, `takes_item: true` | loft | climbs the stair and uses the lectern with the roll in hand | one roll leaves the hand at the click; the lectern then shows a book (`set-block` of `minecraft:lectern[facing=north,has_book=true]`) |
| 4 | *Hang the lantern on the hook* (`obj/hang-the-lantern`) | `interact` at the chain's end, `prop` an iron chain, `requires_item: minecraft:lantern`, `takes_item: true` | loft | uses the chain's end with the lantern in hand | one lantern leaves the hand; a lantern hangs from the chain (`set-block` of `minecraft:lantern[hanging=true]`) |

All four beats are open from the start, so the lectern and the chain's hook
stand in the loft before the party has anything to lay or hang. Arriving in the
loft completes nothing: both loft beats complete only on the click with the
item held in the main hand. An empty-handed click is answered by a
`missing_item_hint`. When all four are done the delve ends.

## What the lectern can show

A lectern's block state is `facing`, `has_book` and `powered`; the book it
holds is block-entity data (`Book`, `Page`). The client draws the book on the
lectern from `has_book` alone. `set-block` writes a block state and no block
entity, so the lectern shows a book and holds none: a player who opens it sees
an empty book. The level states what is true: the roll is laid on the lectern
and shows there; it is not read there.

## Hour and weather

Dusk, clear. No mob is fielded. The nave and the loft are lit by lanterns
placed with the room.

## Branches and endings

None. One ending, when the lantern hangs over the roll.
