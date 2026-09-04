# The Derived Whole — generation record

## The prompt, verbatim

> `/new-delve` The Derived Whole — a demo level for one mechanic: a whole map
> with no authored geometry. Five places: a hub, a seam the plan cut, a slab
> ramp the derivation chose the pitch of, a barred way a keeper yields, and a
> hole that drops back to the hub. One player, fifteen minutes, one NPC, no
> combat, English only. The point a walker leaves with: the map they never built
> reads as a map, and a plan edit plus a regeneration is the same act.

Date: 2026-09-04. `dsl_version` 0.19.0 on every document, which is what
`delvec --version` printed (`delvec 1.1.0, dsl 0.19.0, mc 1.21.11`).

The design of record this level is built to is the queued row in the engine
repository's `docs/demo-levels.md`, *A whole map with no authored geometry — the
derived blockout and its observer*.

## The placement model

A site plan. The brief's first clause is that the map has no authored geometry,
and a site plan is the only placement authority under which that is true:
`areas[]` seats prefab pieces somebody built, and a site plan is derived.
`world.json`'s `areas` is empty, which is what `DW0839` requires of a campaign
carrying a plan.

## Decisions taken while authoring

- **Five places, five connections, one loop**, with the entry and the goal both
  `node/hub`. The brief's five items are one place and four connections; the
  circuit needs five places for the four connections plus the fall to close it,
  so the fifth is `node/lip`, the ledge the hole is at the end of.
- **The gallery is sixteen blocks deep because that is what buys the ramp.** The
  climb out of it rises five. The gentle standard is one block of rise per two of
  run, so it needs ten blocks of run, and the derivation spends the run on the
  axis the seam's face points along. Sixteen affords it; anything under ten does
  not, and the same rise comes back as the steeper standard. That number is bound
  to `fact/gallery-run` in the brief, so it cannot drift silently.
- **The two datums are five apart because the drop policy's cap is five.** The
  hole home is a designed fall at exactly the cap.
- **The fall is through a doorway five blocks up the hub's north wall**, not
  through the hub's ceiling. A ceiling hole is authorable — the seam takes a
  `down` face and a box may stand over another — but it costs the hub its size
  class: `hall`'s own minimum headroom is eight, which would put the ledge nine
  blocks up and past the drop cap, so the hub would have to become a `room` at
  four cells of clearance and the whole upper circuit would have to be re-laid
  over it. Recorded as an alternative, measured, not taken.
- **No stations.** The keeper stands at `anchor/node-upper-walk`, the footing the
  derivation synthesizes for her place. A station would be a second way to say
  where one body stands, and this level does not need one.
- **No `views[]` and no `volumes[]`.** The map is five enclosed boxes standing in
  the void: there is no landform for the whole to own and no silhouette to judge
  from outside. Both zeros are stated in the plan's binding lines rather than
  passed over.
- **`lighting` is declared** (`lantern`, `min_light` 7). A derived map has no
  night-vision mitigation — that surface lives on an `areas[]` entry, and
  `DW0839` requires that list to be empty — so a blockout either lights itself or
  is refused by `DW0210`.

## Posture note

Four axes pushed off the machine default for this campaign:

- **Thematic explicitness** — the level never states its own point. The keeper
  talks about paperwork; the mechanic is named nowhere a player can hear it.
- **Address** — she speaks to the player as someone standing in a survey, which
  is what they are. The fourth wall is the level's actual subject.
- **Emotion named outright** — she says what she is afraid of in plain words
  rather than performing it with a gesture.
- **Resolution** — nothing is resolved. The plan she gives up is the plan of the
  room you are standing in, and it is out of date.

## Findings ledger

| # | finding, as reported | round | status |
|---|---|---|---|
| 1 | The demo's second half — the observer shown as three pairs — cannot be produced from a campaign document. `DW0836`/`DW0837`/`DW0838` compare the plan against the derivation, and the derivation is a pure function of the plan, so a plan edit moves both sides together. Reddening one needs `blockout::Perturb`, which is a Rust API with no command-line surface. | 1 | `engine` |
| 2 | `DW0822` projects about 2 minutes of route against a `target_minutes` of 15. Five places is what the brief pins; the billing and the walking do not agree. | 1 | `open` |

## Round record

Round 1 (generation), stopped at the step-4 design gate.

Validation-loop iterations to the step-3 state: 1.

DW codes at the step-3 state, with counts, over
`delvec --prefabs prefabs validate campaigns/the-derived-whole`:
`DW0150 x1, DW0152 x1, DW0816 x2, DW0817 x1, DW0818 x8` (13 refusals), plus
`DW0822 x1` advisory and `DW0813 x1` engine notice. Every refusal is accounted
for by the rule under *Where step 3 ends*: each names something only
`quests.json` or `dialogue.json` can supply.
