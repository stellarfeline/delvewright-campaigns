# The Tidewatch — generation record

`dsl_version` on every document: `0.20.0`, the number `delvec --version` printed for the engine this campaign was authored with.

## What the brief pinned down, and what was invented

Pinned: two scenes; two players; one class; one quest chain; one NPC who wants something; no branching; a coastal watchtower. Everything else is invented — the keeper, the oil, the tide as the clock the story runs against, the names, and both areas' pools.

## Posture

Flat and weather-worn. Nobody in this delve explains the sea to anybody. Maren states her trouble the way she would state the wind, and the party is not thanked for solving it. The prose carries no exclamation and no quest-giver warmth; what makes the ending land is the lamp catching, not a line about it.

## The decisions

- **`areas[]` and not a site plan.** The library holds no watchtower prefab, and the page's test for that case — "the missing piece is the building the story is about, so `areas[]` was never the right placement model" — points at a site plan. `pool/vertical-keep` was taken as the tower instead: it is an interior keep pool whose members are an entry hall, corridors, a stair with a five-block rise, and terminal rooms, which is what the inside of a tower is. The judgement is that the story is about climbing the tower, and the pool can be climbed. Recorded here because the page's test has no procedure and the reading could go the other way.
- **Anchors only from each pool's `entry`-role member.** A pool area seats a subset of its members, so an anchor declared on a `room` or `terminal` member may not exist in the built world at all, and one declared on several members is ambiguous the moment an objective hangs on it (`DW0498` advisory, `DW0305` hard). The `entry`-role member is the one the assembly always seats. That leaves `spawn` and `anchor/exit` per area, and the design is written to fit them rather than the other way round.
- **`horizon: "ocean"`.** The delve is coastal and the horizon library has a base for exactly that. It brought `DW0320` with it — an ocean horizon needs a `boundary` — which was a repair owed at step 3 and not a stage-5 state.
- **`min_players: 2`** because the brief pinned the party size, though no beat in this design is an AND-join that two bodies are mechanically required for.

- **The AND-join was authored to keep `min_players: 2`, not the other way round.** `DW0358` refuses a delve that requires two players and has no objective with two `after` arms, and this design had none until step 7 said so. The shutter chain in the entry hall is the answer: the design gained a mechanism because the number it had already declared demanded one, which is the right direction for that refusal to push.

## Findings ledger

| # | what | state |
|---|---|---|
| 1 | `horizon: "ocean"` cannot be honestly used with the shipped `cave-*` and `keep-*` pools. `DW0344` reports the ocean-datum check examined **zero of 7 placed pieces**: four stand at or below the sea plane and not one declares a `waterline_y`, so nothing proves anything in this world meets the sea where the sea is. The diagnostic states in its own words that the demand "is not yet authorable — no lever lifts a piece clear of the sea". Only the `island-*` pieces carry the convention. | open — a capability gap, not a campaign defect |
| 2 | `DW0781` reports the piece-mating check examined **zero abutting faces**: of 7 placed pieces, none carries a spatial contract, so nothing proves the pieces of this world fit together. A jigsaw-assembled `areas[]` campaign gets no mating proof at all from the shipped library. | open — a capability gap, not a campaign defect |
| 3 | A pool area's usable anchor set is effectively only its `entry`-role member's, because that is the one member the assembly is guaranteed to seat, and an anchor declared on several members is ambiguous. Two anchors per area is what this campaign had to design against. | open — a constraint, recorded so the next round does not rediscover it |
| 4 | **The critical path stands in the sea.** Read straight out of the world save at the cells `critical-path.json` names: `260,61,4` and `260,61,8` are both `minecraft:water`, with `stone_bricks` floor at y=60 and air at y=62. The party wades through every objective in the tower. The build's own `validation/sea-seepage.json` reports `walk_cells_submerged: 0`, `walk_cells_wading: 0`, `in_pieces: []`, `verdict: "pass"` over the same tree — the two observers disagree and the block read is authoritative. Same root as finding 1: both the unbound `DW0344` invariant and the passing seepage verdict are keyed off a `waterline_y` these pieces do not carry. | open — engine defect, and the reason this campaign is not shippable as built |
| 5 | The built areas bear no resemblance to the design set approved at the gate: the shore is a flat sand floor in a box of cobble with a stone slab floating unattached above the back wall, where the approved image is a tide-cut stair on a black rock headland. `DW0781` reports the piece-mating check examined zero abutting faces, which is why the floating piece is not a red. Nothing in the pipeline compares a built `areas[]` assembly against `design/concept/`. | open |
