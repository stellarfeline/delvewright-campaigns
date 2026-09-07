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

## Findings ledger

Nothing yet.
