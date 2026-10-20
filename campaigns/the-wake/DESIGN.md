# The Wake — design record

The authoritative design of this demo level. Every later round is diffed
against it beat by beat. Its approved design is the engine's demo-level queue
row for spec-0014 (actors, staging, cutscenes): a funeral procession level that
is mostly staging — mourners walk, a eulogy sequence plays, one player choice
redirects the procession. Small, one mechanic family, minimum cast.

## What this level is for

Staging in the spotlight: puppet bodies summoned on a timeline, walked across
the field by the engine, a rite read as a timed sequence of narration and
sound, three camera cuts, and one dialogue choice that decides where the
procession goes. The choice is a declared branch point with two short branches
and two endings.

**Zero combat.** No waves, no hostiles, no unleashed actor, no vulnerable body,
no declared difficulty. Nothing in this level can kill a player. One plain
checkpoint at the bier; no bonfire.

## Premise

Wren Ashlaw read the tide for the keep above the barrow field, and drowned
reading it. The field's people are already assembled among the graves when the
party comes ashore at low water. Her brother **Hallis** cannot say where she
should go; the barrow-warden **Sedge** has already cut a grave for her, and Wren
herself left no word except that she spent her whole life on the water. By the
field's custom the word belongs to whoever carried the body up the road, which
this evening is four strangers.

## Map

Two places on a tidal islet under `horizon: ocean`, at dusk, one ground plane
one course over the sea (`datum/grade`, y 64). The region is the two places and
their rings, so the sea is all round the islet.

| place | box | what it is |
|---|---|---|
| `node/shore` | 15 × 8, entry | the beach: the landing, the shore fire, driftwood, mud where the tide was, and a line of old tide stones along the waterline |
| `node/field` | 15 × 18 | the barrow field: the foot of the keep wall with its shut timber gate, a gravel grave road up the middle, the black banner and the bier, the grave row with the open cut at its end, old graves on both flanks |

`edge/grave-road` joins them as a contact front: the turf runs straight down
onto the sand the whole width between the dykes. Both places are detailed from
the campaign's own programs (`programs/shore.json`, `programs/field.json`,
written by `design/build_pieces.py`). Lantern posts light both places.

Stations (field): `anchor/keep-gate`, `anchor/bier`, `anchor/bier-side`,
`anchor/widow`, `anchor/west-flank`, `anchor/east-flank`,
`anchor/second-barrow`, `anchor/warden-post` (the head of the open cut, and the
ground branch's destination), `anchor/row-head`. Stations (shore):
`anchor/shore-fire`, `anchor/tide-line` (the tide branch's destination), and
the derived `spawn`.

## Cast

**Speaking (two, each with their own face)**

- `npc/sedge` — Sedge, the barrow-warden. Flat, few words; talks about weather
  and soil when asked about people. Motivation: the field takes everyone, and
  she will not have it cheated of one.
- `npc/hallis` — Hallis Ashlaw, the dead woman's brother. Over-explains,
  apologises, stops mid-sentence. Motivation: he cannot choose, and he knows
  that not choosing is also a choice.

**Staged (five actors)**

- `actor/bier` — an armour stand in a brown shroud, "Wren Ashlaw". The only body
  that crosses the fork.
- `actor/lamp-bearer` — Orrin, who comes out of the keep gate with the wake-lamp.
- `actor/widow` — Maud Pell, at the foot of the bier; never moves.
- `actor/elder` — Old Garrow, at his family's barrow on the flank; never moves.
- `actor/child` — Tam, by the far dyke; walks in as far as the second barrow.

## Beats

**Q1 `quest/low-water`** — the party comes ashore on the beach. `obj/greet`
(talk to Hallis at the shore fire, a few steps from the landing) → a `sequence`
tolls the keep bell and spawns the whole wake over 140 ticks, so the field fills
behind the party as they turn up it. `obj/come-up` (reach the bier) → checkpoint
at the bier, **cutscene A** (an establishing crane over the bier, then an insert
on the body) and the art title THE WAKE.

**Q2 `quest/the-eulogy`** — `obj/hear-the-rite` (talk to Sedge at the head of
the cut) → the eulogy `sequence`: three narration beats and two bell sounds over
260 ticks, and at tick 40 three concurrent walkers — Orrin from the gate to the
bier's side, Tam from the dyke to the second barrow, Sedge from her post to the
head of the row — under **cutscene B**, a side-track on Orrin.

**Q3 `quest/the-word`** — `obj/bring-the-word` (talk to Hallis back at the fire).
His tree is the fork: "The ground." sets `flag/to-the-ground`, "The tide." sets
`flag/to-the-tide`; each goes on to his reply to that word. Two non-committal
options (what Sedge says, why not him) walk the tree without setting anything.

**Q4 `quest/the-ground`** (`branch/ground`) — `obj/to-the-cut` (reach the
warden's post, gated on `flag/to-the-ground`) → a `sequence`: the bier walks from
the banner to the cut under **cutscene C** (locked-off), goes down (`despawn-actor
vanish`), the art title THE GROUND, `campaign-complete ending/the-ground`.

**Q5 `quest/the-tide`** (`branch/tide`, the plan's finale) — `obj/to-the-water`
(reach the tide line, gated on `flag/to-the-tide`) → the same shape: the long
carry from the banner down the grave road, past the fire to the tide stones,
under a side-track; the body given to the water, the art title THE TIDE,
`campaign-complete ending/the-tide`.

`quest/the-tide` declares `depends_on: [quest/the-word, quest/the-ground]` so
the plan has one convergent sink, while both quests trigger off
`quest/the-word`.

## Branch table

| branch | flags set | destination | ending |
|---|---|---|---|
| `branch/ground` | `flag/to-the-ground` | `anchor/warden-post` (the cut) | `ending/the-ground` |
| `branch/tide` | `flag/to-the-tide` | `anchor/tide-line` (the water) | `ending/the-tide` |

Branch point `branch-point/the-word`, `opens_at: quest/the-word`,
`forks_on: [flag/to-the-ground, flag/to-the-tide]`. Each walk of the bier
carries its branch's flag in its own `when`.

**Per-branch casts.** After the fork both NPCs declare a placement per branch in
every later quest: on the ground branch Sedge watches the plank go to the cut she
opened and Hallis comes to the fire's edge and no further; on the tide branch
Sedge stays at the row with the spade planted and will not walk to the water,
and Hallis banks the fire for the walk down.

## Endings

- `ending/the-ground` — the field closes over her.
- `ending/the-tide` — she goes out on the ebb, to the water she read.

`world.outro` is ending-neutral: the field keeps what it is given, and the
water keeps the rest.

## Verbs deliberately not used

`interact`, `collect`, waves, traps, stealth, timed gates, shortcuts, ambushes,
`unleash-actor`, bonfires, `damage-players`, party division of labour. A demo
level is one mechanic in the spotlight.
