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
- **`lighting` is declared** (`torch`, `min_light` 7). A derived map has no
  night-vision mitigation — that surface lives on an `areas[]` entry, and
  `DW0839` requires that list to be empty — so a blockout either lights itself or
  is refused by `DW0210`. The fixture was `lantern` first and the build refused
  it: `DW0211` named the darkest reachable cell, `[28, 64, 24]`, on the hub's
  floor. A lantern hangs from the ceiling, the hub is a hall with fourteen cells
  of headroom, and fifteen of block light fourteen blocks up arrives as one.
  `torch` stands ON the floor, so its distance to a walkable cell is horizontal,
  and the pass finds sites. **The repair is the fixture, not the number**: the
  threshold stayed at 7.
- **This campaign lives in `campaigns/`, not `demos/`.** `tools/campaign-build.py`
  — the CI build gate — hard-codes `CAMPAIGN_ROOT = "campaigns"` with no flag,
  and its population is every directory under it holding a `world.json`. A
  campaign-shaped level under `demos/` would be built by nothing. `demos/` holds
  tool exhibits — a program, a piece, its reports — and the exhibit for this
  level lives at `demos/the-derived-whole/` and points here.
- **`target_minutes` stays 15, and the fifteen minutes is the session** — the
  walk, the plan-edit exhibit and the observer pairs — not the route. Recorded as
  a deviation from the prompt, which pinned both the five places and the fifteen
  minutes: `DW0822` projects about 2 minutes over the graph and MEASURES 126
  blocks over 5 legs, about 3 minutes, over the built blockout. The README says
  so in the reader's own terms.
- **No reference imagery was drawn, and none is owed.** The step-4 design gate is
  confirmed on pictures because a picture is where a design's appearance and its
  scale are judged. On a derived blockout neither authority is the image's: the
  geometry comes from the plan and the metrics table, and the appearance comes
  from `compiler::blockout::palette`, which the module's own comment calls fixed
  rather than authored. A painting of a place here would show a room nobody can
  build in a palette nobody can choose. The gate was taken on a to-scale plan
  sheet drawn from the plan's own numbers — one character per block — and the
  appearance is judged at step 12 on POV frames rendered out of the built bytes.

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

Round 1, generation.

Validation-loop iterations to the step-3 state: 1. Iterations from there to a
clean `validate`: 1 — writing `quests.json` and `dialogue.json` cleared all 13
refusals at once. Iterations from a clean `validate` to a green `build`: 1, the
`DW0211` fixture repair above.

DW codes the round hit, with counts:

| where | codes |
|---|---|
| `validate`, step-3 state | `DW0150` x1, `DW0152` x1, `DW0816` x2, `DW0817` x1, `DW0818` x8 (13 refusals); `DW0822` x1, `DW0813` x1 |
| `validate`, after stage 5 | none; `DW0822` x1, `DW0813` x1 |
| `analyze` | none; `DW0822` x1, `DW0813` x1 |
| `build`, first attempt | `DW0211` x1 |
| `build`, green | none; `DW0781` x1, `DW0813` x1, `DW0822` x2 |

Every step-3 refusal is accounted for by the rule under *Where step 3 ends*:
each names something only `quests.json` or `dialogue.json` can supply.

The build's own two binding lines, which are half of what this level exists to
show — a green that examined nothing would look exactly like this one:

```
blockout binding: 5 place(s) massed (0 detailed, so 5 massed by the
derivation), 5 seam(s) cut (1 stair, 1 barred), 0 whole-owned volume(s), 7
anchor(s) synthesized, 67 region write(s) over 12325 cell(s).

blockout battery binding: 5 seam(s) proven over 5 shared wall(s) (of them 0
contact(s), 0 crossable column(s) measured), 5 place(s) proven reached, 1808
standable cell(s) classified over 10 place pair(s), 0 sightline(s) walked, 3
identity(ies) re-measured (0 declaration-only), 5 critical-path leg(s)
measured.
```

The three hashes and the engine they were taken with:

```
site plan sha256:    a5ba25932126576a98bb6707c524d94475aaf73cc932852fd54c9d75acb4d8de
layout graph sha256: 4cb7d99e17fa978b8afa8cbde465bd00e9a2ac4f6f28b0b2172c2b01b91cd3e9
blockout sha256:     fe61d6dad75c3447b6d76c3556f6948baa57539764ea7ba2775b3af1e546efde
engine revision:     417e12663330d70efb63ff65893b594a3847f310 (delvec 1.1.0)
```
