# The Wake — design record

**Authoritative design document.** Every iteration round is diffed against this
file beat by beat (SKILL iteration protocol). Campaign id `the-wake`, DSL 0.9.0
(world stage; the later stages stay at 0.8.0 behind their own fences),
Minecraft 1.21.11.

## What this level is for

A first-party **mechanic demo** (`docs/demo-levels.md`, row "Actors, staging,
cutscenes (spec-0014)"). One mechanic family in the spotlight, 10–20 minutes,
minimum cast: **staging**. Roughly 80% of the level's runtime is actors walking,
a scripted eulogy timeline, and camera. It is also the first *authored* content
to exercise spec-0025's declared branch point, per-branch casts, chronicle
review and branch runs.

**Zero combat.** No waves, no hostiles, no `unleash-actor`, no `vulnerable`
actor, no declared `difficulty` (a delve with no waves ships peaceful by
derivation — `DW0468`). Nothing in this level can kill a player. One plain
`set-checkpoint`, no bonfire (so no `flask`, no `DW0476`).

## Premise

Wren Ashlaw read the tide for the keep above the barrow field, and drowned
reading it. The field's people are already assembled among the graves when the
party comes ashore at low water. Her brother **Hallis** cannot say where she
should go; the barrow-warden **Sedge** has already cut a grave for her, and Wren
herself left no word except that she spent her whole life on the water. By the
field's custom the word belongs to whoever carried the body up the road — which,
this evening, is four strangers.

## Map

One area, one piece: `prefab/tk-barrow-field` (48 × 14 × 40, open air,
`time: dusk`), bound as `prefab_pool: "pool/tidal-keep"` with
`pieces {min: 1, max: 1}`. Exactly one piece is drawn — the pool's `entry` — so
every anchor is unambiguous by construction (no `DW0305`), and the whole level
is one readable open field with the keep gate at the north end and the water at
the south.

**Horizon — the cherry valley** (owner ruling, task #177; adopted at DSL 0.9.0):

```json
"horizon": { "base": "valley", "ratio": 3.0, "rim_height": 32,
             "flora": "cherry", "palette": "stone-petal" }
```

A mountain annulus rings the field, cherry-crowned, with a flat gap floor
between the field's edge and the slopes. Parameter rationale, one line each:

- `ratio: 3.0` — the scene is 48 × 40, and the annulus band is floored at
  `GAP_WIDTH + SLOPE_RUN` = 30 per axis, so at the 2.5 default the **short (Z)
  axis** gets exactly 30 and has no outer face at all: the blossom line stops
  crowning the north and south crests, which are the two directions this level
  actually looks (the keep gate, the water). 3.0 is the smallest value that
  gives the 40-deep axis a real outer face (40 > 30); measured cherry trunk
  columns north/south rise 23/35 → 66/84, total 154 → 386.
- `rim_height: 32` — the ring must close the horizon and must not lid the dusk
  sky, since `time: dusk` under a clear sky is this level's whole mood and its
  camera work is a low crane over a flat field. Measured from the party's eye at
  spawn: the crest clears eye level at **every** azimuth (worst gap +6.0°, so no
  window onto the ambient void anywhere in the field) while occupying only the
  lower 6–25° of the view; the 48 default takes 11–36° and reads as a well over
  a 40-deep scene.
- `flora: cherry` — the owner's ruling; a funeral is what the blossom is for.
- `palette: stone-petal` — the `"cherry-valley"` shorthand's own pairing: fallen
  `pink_petals` as the slope understory rather than `short_grass`/`fern`. This
  is the one parameter where this campaign deliberately differs from the
  hollow-vigil construction mule, which kept `stone-grass` for a moorland keep.

The horizon change re-datums the piece: `valley`'s `walk_ref_y` is the gap floor
+ 1, so the piece is placed at y 61 (was 60) and the field's walk plane sits at
64 (was 63). The piece's own authored water (`waterline_y: 2`, world y 63) is
therefore flush with the surrounding gap floor and reads as a valley tarn rather
than as open sea. **The prose has not been re-fictioned** — `theme`, `premise`
and the tide branch still say coast, tide and low water. That is an owner call,
recorded as an open item in `GENERATION.md`.

**Why the pool binding and not `areas[].prefab`.** The direct single-prefab
binding skips the socket-sealing pass: the piece's unmated north connector was
left open to the sea with the prefab's `minecraft:jigsaw` marker block standing
in the gap, in plain view from the party's spawn and from the establishing
crane. The identical piece drawn from a one-member pool seals the same socket
into a stone panel. Recorded as an engine finding in `GENERATION.md`; the pool
binding is the correct authoring choice regardless, since it is the form the
solver actually validates.

Anchor allocation (prefab-local coordinates):

| anchor | pos | occupant / use |
|---|---|---|
| `anchor/l0-gate-approach` | 24,3,4 | `actor/lamp-bearer` start — the keep gate |
| `anchor/l0-banner` | 22,3,14 | `actor/bier` — Wren on her plank under the black banner |
| `anchor/l0-elite-dormant` | 23,3,16 | lamp-bearer's destination (beside the bier) |
| `anchor/l0-barrow-2` | 33,3,17 | `actor/mourner-child` destination |
| `anchor/l0-elite-stand` | 24,3,18 | `actor/mourner-widow` (never moves) |
| `anchor/l0-flank-west` | 7,3,18 | `actor/mourner-elder` (never moves) |
| `anchor/l0-flank-east` | 40,3,18 | `actor/mourner-child` start |
| `anchor/l0-barrow-3` | 19,3,19 | Sedge's rite position (after her walk) — the row's head |
| `anchor/l0-reward` | 12,3,20 | `npc/sedge` start — the warden's post, **and the open cut**: ground-branch destination |
| `anchor/l0-reward-cache` | 12,4,21 | the warden's barrel (`loot[]`) |
| `anchor/l0-barrow-1` | 14,3,15 | unused — a recessed grave niche, not walkable-into (see `GENERATION.md` item 11) |
| `anchor/l0-bonfire` | 19,3,29 | `npc/hallis` — the shore fire (never moves) |
| `spawn` | 24,3,31 | party landing |
| `anchor/l0-tide-line` | 24,3,33 | **the water** — tide-branch destination |

## Cast

**Speaking (stage 2, 2 roles)**

- `npc/sedge` — Sedge, Barrow-Warden. Villager body. Flat, few words, talks
  about weather and soil when asked about people. Motivation: the field takes
  everyone, and she will not have it cheated of one.
- `npc/hallis` — Hallis Ashlaw, the dead woman's brother. Villager body.
  Over-explains, apologises, stops mid-sentence. Motivation: he cannot choose,
  and he knows that not choosing is also a choice.

**Staged (stage 5 actors, 4 mourners + the dead)**

- `actor/bier` — `minecraft:armor_stand`, "Wren Ashlaw". The shrouded body on
  its plank. The only actor that crosses the fork.
- `actor/lamp-bearer` — comes down from the keep gate with the wake-lamp.
- `actor/mourner-widow` — has not left the bier since morning; never moves.
- `actor/mourner-elder` — stands at her own family's barrow on the west flank;
  never moves.
- `actor/mourner-child` — on the east flank; walks in to the second barrow.

## Beats

Two dialogue edges exist purely as **flow plumbing**, not as playable beats:
`dlg/sedge-arrival` → `dlg/sedge-rite` (gated on `flag/came-up`) and
`dlg/hallis-arrival` → `dlg/hallis-word` (gated on `flag/rite-said`). The
compiler's branch-flow model reaches dialogue only from a tree's `root`, not
from a cast-ledger root, so a fork node served by the ledger is invisible to it
and every branch reads as unreachable (`DW0482`). Both flags are set on every
playthrough, so no undeclared fork is introduced; both edges are unreachable in
play, because the ledger has already swapped those NPCs onto later roots by the
time the flags exist. Recorded as an engine finding in `GENERATION.md` — these
two edges should be deleted when the flow model learns about cast roots.

**Q1 `quest/low-water`** — the party comes ashore at `spawn` at dusk.
`obj/greet` (talk-to Hallis at the shore fire, ~5 blocks from the landing) →
a `sequence` tolls the keep bell and spawns the whole wake over 140 ticks, so
the field fills in behind the party as they turn north. `obj/come-up`
(reach `anchor/l0-banner`) → checkpoint at the bier + **cutscene A**
(`establishing-crane` over the field, then an `insert` on the bier) + the art
title.

**Q2 `quest/the-eulogy`** — `obj/hear-the-rite` (talk-to Sedge at her post) →
the eulogy `sequence`: three narration beats over ~260 ticks, and at t=40 three
concurrent walkers — `move-actor` lamp-bearer (gate → bier-side, 12 blocks),
`move-actor` mourner-child (east flank → second barrow), `move-npc` Sedge (post
→ the grave-row head) — under **cutscene B** (`side-track` on the lamp-bearer,
the moving-subject style, `DW0349`-legal because the move is in the same
sequence step).

**Q3 `quest/the-word`** — `obj/bring-the-word` (talk-to Hallis, back down at the
fire). His tree is the **fork**: two flag-setting options, `flag/to-the-ground`
and `flag/to-the-tide`, each with a `happening`. Non-committal options (ask
about Wren, ask what Sedge says) walk the tree without setting anything.

**Q4 `quest/the-ground`** (branch `branch/ground`) — `obj/to-the-cut`
(reach `anchor/l0-reward`, gated on `flag/to-the-ground`) → a `sequence`:
`move-actor` the bier from the banner west to the cut under **cutscene C**
(`locked-off`), then `despawn-actor … vanish` (she goes down), the art title
**THE GROUND**, `campaign-complete ending/the-ground`.

**Q5 `quest/the-tide`** (branch `branch/tide`, and the plan's `finale`) —
`obj/to-the-water` (reach `anchor/l0-tide-line`, gated on `flag/to-the-tide`) →
the same shape: the long 19-block carry south past the fire to the tide line,
`side-track`, the body given to the water, art title **THE TIDE**,
`campaign-complete ending/the-tide`.

`quest/the-tide` declares `depends_on: [quest/the-word, quest/the-ground]` so
that the plan has one convergent sink (`DW0132`) while both quests actually
trigger off `quest/the-word` — the shape the compiler's own
`branch-two-endings` fixture uses.

## Branch table

| branch | flags set | flags pinned unset | destination | ending |
|---|---|---|---|---|
| `branch/ground` | `flag/to-the-ground` | `flag/to-the-tide` | `anchor/l0-reward` (the cut) | `ending/the-ground` |
| `branch/tide` | `flag/to-the-tide` | `flag/to-the-ground` | `anchor/l0-tide-line` (the water) | `ending/the-tide` |

Branch point `branch-point/the-word`, `opens_at: quest/the-word`,
`forks_on: [flag/to-the-ground, flag/to-the-tide]`.

Both branches are deliberately **short** — one objective, one walk, one
sequence — so that neither the chronicle review nor the branch-run ladder has to
carry a second act.

**Per-branch casts.** After the fork, both NPCs declare a list of placements in
*every* later quest, each gated on the flags of the branch it belongs to
(`DW0483`). The divergence is characterisation, not bookkeeping: on
`branch/ground` Sedge hands the plank down and takes up the spade; on
`branch/tide` she stays at the grave-row with the spade planted and refuses to
walk to the water. Hallis comes to the fire's edge and no further on the ground
branch; on the tide branch he banks the fire for the walk down.

## Endings

- `ending/the-ground` — the field closes over her. The last chronicle line is a
  `seals` on `anchor/l0-reward`; nothing acts on her afterwards.
- `ending/the-tide` — she goes to the water she read. The last chronicle line is
  a `departs` on `actor/bier`.

`world.outro` is ending-neutral: the field keeps what it is given.

## Verbs deliberately NOT used

`interact`, `collect`, waves, traps, stealth, timed gates, shortcuts, ambushes,
`unleash-actor`, bonfires, `damage-players`, party division of labour. A demo
level is one mechanic in the spotlight; everything above belongs to a different
row of `docs/demo-levels.md`.

## Known engine finding (does not change this design)

`compiler::nav::plan_actor_moves` chains each actor's move origins in **campaign
document order**, blind to branch exclusivity. `actor/bier` is redirected by the
fork, so exactly one of its two legs is planned from the *sibling branch's*
destination: the tide leg starts at `anchor/l0-reward`, the ground branch's
grave, and the bier snaps ~11 blocks before it walks to the water. Recorded with
emitted-command evidence in `GENERATION.md`; the design is not bent around it
(debug doctrine — a workaround that turns a toolchain bug green ships the bug to
every future campaign).

A second engine finding is open and **unfixed in this campaign by choice**: the
generated `campaign` PackTest asserts `dw.campaign` in the same tick it drives
the objectives, so it cannot pass for a campaign whose `campaign-complete` is
scheduled inside a `sequence` — which this one's is, deliberately, so the
completion fanfare lands after the burial rather than during it. See
`GENERATION.md` item 10.
