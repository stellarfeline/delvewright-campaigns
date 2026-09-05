# The Toll Road — design of record

A demo level for the trap surface (spec-0011 trigger + spec-0022 command payload).
One area, one piece, one mechanic in the spotlight. Fifteen minutes.

## Premise

The Cinderwright Company cut a way through the Vench and took a toll on it for
ninety years. The company is wound up; the road is not. Its gear still works, its
tariff is still posted, and its last keeper is still counting.

## The place

`prefab/toll-road-pass` — a 9 x 7 x 45 way cut through tuff, a three-course paved
road down the middle of it, sconces set into the vault, and eight alcoves cut into
the eastern wall. The road climbs; the alcoves are where the company kept what the
road earned. The piece is a campaign zone: `design/programs/toll-road-pass.json`,
expanded at the region and seed `design/programs/zones.json` declares.

Anchors the campaign binds: `anchor/stair-run` (the road's midpoint),
`anchor/volley-slot` (the vault rib directly over it), `anchor/pocket-1` to
`anchor/pocket-8` (the alcoves, each facing the road).

## The cast

One speaking part. **Ottiline Sarr**, a Cinderwright clerk who outlasted her
company, at her desk in the last alcove. She is courteous, she quotes the tariff
by clause, and she is not wrong: the road was cut, the road was kept, and the
party is walking on it. She is owed forty years of back pay by a company that no
longer exists, which is why she is still counting and not why she says she is.

## The beats

| act | quest | what happens |
|---|---|---|
| 1 | `quest/the-tariff` | The party walks up the road. The first flagstone is a plate and the vault above it is a gallery. They meet Ottiline and hear what the road costs. |
| 2 | `quest/paid-in-kind` | The toll is payable in kind out of the road's own alcoves. Three stations, three kinds of gear, three levers the company left for its own people. |
| 3 | `quest/the-ledger` | Ottiline enters the party in the ledger and asks them to sign. The road stays open behind them. The ledger stays open in front of her. |

## The three stations

Each is one trap: a redstone-native trigger and a command payload, with a disarm
the party can reach before the trigger. Each guards one alcove of loot.

| station | trigger | payload | disarm lever | the alcove it guards |
|---|---|---|---|---|
| the stair gallery | `pressure-plate` at `anchor/stair-run` | `volley` from `anchor/volley-slot` over the road | `anchor/pocket-1` | `anchor/pocket-2` |
| the dart line | `tripwire` at `anchor/pocket-4` | `volley` across the way | `anchor/pocket-3` | `anchor/pocket-5` |
| the strongbox | `trapped-chest` at `anchor/pocket-7` | `collapse` of the vault over it | `anchor/pocket-6` | `anchor/pocket-8` |

The teaching order is deliberate. The gallery fires on a plate the party has
already stepped on, so the first lesson costs nothing but a fright and shows what
the road does. The dart line is visible before it is crossed. The strongbox is the
only one a player springs by choosing to spring it, which is what a trapped chest
is for — it is the one trigger a controlled mob cannot pull.

Every station is `lethality: harmful`, not `lethal`: this is a demo of the surface,
not a lesson in dying. The levers are the point. A player who reads the road pays
nothing; a player who does not is hurt and learns where the lever was.

## Endings

One. `ending/signed` — the party pays, in kind, and is entered. There is no branch
and no `branch_points`: a demo level with one mechanic in the spotlight does not
also carry a fork, and the chronicle step (skill page step 11) is skipped by
declaring none.

It ends unresolved on purpose. Ottiline is not persuaded, not defeated and not
redeemed, and the last thing the party reads is a line in a ledger rather than an
understanding they arrived at.
