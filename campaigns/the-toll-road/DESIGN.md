# The Toll Road — design record

**Kind**: first-party mechanic demo (`docs/demo-levels.md`, row *Traps*).
**Spotlight**: spec-0011 / spec-0022 **traps**. Everything else is kept at the
floor: one NPC, no combat, no bonfires, no branches.
**Length**: 10–20 minutes. **Cast**: 1. **DSL**: 0.8.0. **Languages**: en (canonical) + zh-cn.

## Premise

The tide road to Vesper Keep is the only dry way inland, and the keep still
collects its toll. Ordwin the Tollwright meets travellers at the barrow shore
and explains the arrangement: the road takes payment in attention. Three tolls
stand between the shore and the vault, and each one shows you its hardware
before it uses it — a plate, a slot, a lever. Ordwin does not walk his own road.

## The teaching thesis

A stranger who plays this must come away knowing three things:

1. **A trap announces itself.** Every trigger in this delve is a visible block
   in the floor, and every disarm is a visible glowing lever. Nothing is hidden.
2. **Counterplay is a decision, not a reflex.** The volley saturates its kill
   zone (spec-0022), so strafing does not help — leaving the zone, or throwing
   the lever *before* you commit, is the play.
3. **The three trigger kinds behave differently.** A plate fires for anyone who
   steps; a chest fires only for a player who opens it. The delve puts one of
   each on the road and narrates the difference at the moment it matters.

## Layout — one area, the whole tidal-keep chain, walked end to end

`area/keep` binds `pool/tidal-keep` with `pieces {min: 5, max: 5}` and `seed: 11`.
Five is the count the pool's socket geometry and the compiler's filler arithmetic
actually admit (`DW0301`), and it lands exactly the chain the road wants — the
bell tower is the piece left out, which is the one the design did not want.

| Leg | Piece | Role on the road |
|---|---|---|
| 1 | `tk-barrow-field` | the shore: the briefing, the demonstration cache, the spawn |
| 2 | `tk-gatehouse` | **toll 1** — the stair volley |
| 3 | `tk-wall-walk` | the wall head; a checkpoint and a look ahead |
| 4 | `tk-courtyard-chapel` | the mustering yard, the road's midpoint checkpoint |
| 5 | `tk-cistern` | **tolls 2 and 3** — the dart gallery and the toll-box; the vault |

The bell tower is **off the road** — the narration at the wall head names it as
the thing the toll does not buy you.

The first version of this design bound three areas to three fixed pieces and
relied on the compiler's automatic inter-area transport. It cannot be built:
transport is emitted only when the destination area exposes an anchor literally
named `spawn`, and only the barrow field has one (GENERATION.md, finding 11).
Walking the whole keep is the better delve anyway — the road is the subject.

## The three tolls

### Toll 1 — the stair volley (`trap/stair-volley`)

- **Trigger**: `pressure-plate` at `anchor/l1a-trap-boulder` (the plate set into
  the third tread of the gatehouse stair).
- **Payload**: `play-sound` (dispenser launch, at the slot) then `volley` from
  `anchor/l1a-volley-slot` over a kill zone centred on `anchor/l1a-stair-run`.
  Two salvos, 20-tick interval — enough to hurt a kitted party and teach the
  shape of the fire, not enough to kill one that keeps moving.
- **Counterplay**: the mural landing on the east wall carries the disarm lever
  (`anchor/l1a-mural-door`, `flag/stair-stilled`). The trap declares
  `forbids_flags: [flag/stair-stilled]`, so throwing the lever physically
  removes the plate from the floor — the spec-0011 gate is a real block edit,
  not a bookkeeping flag.
- **Lethality**: `harmful`, `reset: rearm`.

### Toll 2 — the dart gallery (`trap/dart-gallery`)

- **Trigger**: `pressure-plate` at `anchor/l3-trap-darts`, on the shaft the
  party descends into the undercroft.
- **Payload**: `volley` from `anchor/l3-gallery-slot` down the shaft.
- **Counterplay**: the lever sits at `anchor/l3-dart-lever`, **five blocks from
  where the party lands and before the descent** — the whole point of the beat.
  The narration at the landing names it. `flag/darts-stilled`, gated the same
  physical way.
- **Lethality**: `harmful`, `reset: rearm`.

### Toll 3 — the toll-box (`trap/toll-box`)

- **Trigger**: `trapped-chest` at `anchor/l3-alcove-cache` — the only
  player-distinct trigger in the vocabulary, and the delve says so out loud.
- **Payload**: `narrate` + `play-sound` + `damage-players` scoped to the alcove.
- **The box is empty on purpose.** It is the keep's own toll-box, not loot: it
  is the beat that teaches "a container can be a trigger". The real cache is in
  the secret cell behind it (`anchor/l3-secret-cache`).
- **Lethality**: `harmful`, `reset: rearm`, **off the forced path** — a player
  who never touches it finishes the delve.

## Beat sheet

| # | Quest | Where | Beat |
|---|---|---|---|
| 1 | `quest/the-toll` | barrow field | Ordwin meets the party at the tide line and explains the arrangement; they take the Road's Terms from his open demonstration cache; checkpoint at the landing; Ordwin turns back — he does not walk his own road. |
| 2 | `quest/first-toll` | gatehouse | Checkpoint at the gate approach. The stair foot narrates the plate in the third tread and the lever on the mural landing. Climbing past the plate springs the volley. Checkpoint at the stair head. |
| 3 | `quest/last-toll` | wall → yard → cistern | The wall head and the mustering yard carry the road (and its checkpoints) to the vault. Arrive at the east landing beside the dart lever; descend the shaft (dart gallery); pass the toll-box alcove; take the writ from the secret cell; the road ends. |

**Staging note.** Ordwin stands at `anchor/l0-tide-line`, two blocks from where
the party lands, and the demonstration cache is a walk west to
`anchor/l0-reward`. The collect objectives deliberately sit *beside* their loot
containers rather than on them (GENERATION.md, finding 9), and the two prizes
are deliberately different base items (finding 10).

## Deliberate omissions

- **No bonfires, no `respawns_on_rest`** — plain `set-checkpoint` only
  (spec-0012), pending the owner's ruling on re-seat semantics.
- **No branch points** — the delve is linear, so `branch_points` is absent and
  no branch chronicle is emitted or reviewed (spec-0025 applies only to a plan
  that forks).
- **No combat** — no waves, no actors, no tiers. The dungeon is the antagonist.
- **The disarm levers are optional.** They are counterplay a *player* chooses;
  no objective is gated on a disarm flag, because the compiler's critical path
  has no "throw a lever" step and gating one would make the delve unprovable
  by machine (see GENERATION.md, finding 5).

## Known design constraints inherited from the library

The tidal-keep tileset was authored for *The Drowned Bell*; this delve reuses
three of its pieces unchanged. Two consequences the design absorbs rather than
fights:

- The gatehouse carries **no loot container**, so toll 1's reward is passage,
  not treasure; the two containers this delve fills are in the barrow field and
  the cistern.
- There is **no trapped-chest hardware anywhere in the library** (see
  GENERATION.md, finding 2). `trap/toll-box` binds the undercroft barrel, and
  the compiler's own interaction affordance is what the player clicks. The
  fiction calls it a toll-box for exactly that reason.
