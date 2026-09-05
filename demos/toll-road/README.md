# The Toll Road

The demo level for the **trap surface** — spec-0011's redstone-native trigger and
spec-0022's command payload, with the `volley` and `collapse` trap verbs.

The level itself is a campaign, so it lives where every campaign lives and where
this repository's own gate (`tools/campaign-build.py`, the `every campaign builds`
check) can find it:

    campaigns/toll-road/

`campaigns/toll-road/DESIGN.md` is the design of record — the place, the cast, the
three stations and what each one teaches. `campaigns/toll-road/GENERATION.md`
carries the decisions, the measurements and the findings ledger.

## What it is meant to show

A short fortified pass with eight alcoves cut into one wall. Three of them are
guarded, one by each trigger the DSL has:

| station | trigger | payload |
|---|---|---|
| the stair gallery | `pressure-plate` | `volley` from the vault rib over the road |
| the dart line | `tripwire` | `volley` across the way |
| the strongbox | `trapped-chest` | `collapse` of the vault above it |

Each has a lever the party can reach before the trigger. Reading the road costs
nothing; not reading it costs a hit and shows where the lever was.

## State

**Blocked at `delvec build`, and the blocker is an engine gap, not a content one.**
`DW0345` requires the piece the party spawns in to declare an anchor with
`"role": "entry"`, and nothing in the documented pipeline can write one: a grammar
`mark` cannot declare it, and `delve-admit anchor` writes only `pos`, `facing`,
`region` and `block`. Nor does a spawn antechamber help: crossing into the pass from another area is refused by `DW0872`, which asks the destination area for the same anchor. The piece, the placement and the story documents are all
authored and the campaign is at the skill page's design gate.
