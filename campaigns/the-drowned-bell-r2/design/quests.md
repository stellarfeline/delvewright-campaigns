# The Drowned Bell — quest structure

The campaign quest plan as a reachable graph: the critical path, the optional
strands, the gates, and the one branch. Node ids are stable and later DSL stages
use them.

## Critical path

A linear chain. Every node is reachable from `CP-01` using only nodes in this
list — no optional node is ever a prerequisite of a critical node.

| id | node | zone | completed by | opens |
|---|---|---|---|---|
| CP-01 | Wake on the flat | Z0 | standing up | CP-02 |
| CP-02 | Walk the stake line | Z0 | reaching the shelf inside the tide-stakes | CP-03 |
| CP-03 | The lamp | Z0 | speaking to Emeric (one exchange; skippable content, not a skippable node — he is on the only route) | CP-04 |
| CP-04 | The cliff road | Z1 | crossing the fallen ledge | CP-05 |
| CP-05 | The mooring line | Z1 | taking the **rope** from the cliff opening | CP-06 |
| CP-06 | Through the breach | Z1→Z2 | entering the gate passage | CP-07 |
| CP-07 | The winch | Z2 | raising the portcullis (**S1**) | CP-08 |
| CP-08 | The causeway | Z3 | crossing to the water-gate tower | CP-09 |
| CP-09 | Over the arcade | Z3 | entering the tower at shutter height | CP-10 |
| CP-10 | Unbar the tower | Z3 | opening the barred door from inside (**S2**) | CP-11 |
| CP-11 | The cloister | Z4 | defeating the Two Sextons | CP-12 |
| CP-12 | The banded door | Z4 | unbarring it from the chapel side (**S3**) | CP-13 |
| CP-13 | The hall | Z5 | defeating **Housecarl Ridd** | CP-14 |
| CP-14 | The prior | Z5 | speaking to Ancel — he names the well and the broken stair | CP-15 |
| CP-15 | The descent | Z6 | reaching the well head | CP-16 |
| CP-16 | The Founder | Z6 | defeating **the Founder** | CP-17 |
| CP-17 | The tongue | Z6 | taking the bell's tongue | CP-18 |
| CP-18 | The grille | Z6 | breaking **S4** outward (the only route back up) | CP-19 |
| CP-19 | The ramp | Z7 | reaching the tower foot | CP-20 |
| CP-20 | The broken flight | Z7 | bridging the stair with the rope from CP-05 | CP-21 |
| CP-21 | The stairhead | Z7 | resolving **Odo Ferrier** (defeat *or* the tally, see OPT-C) | CP-22 |
| CP-22 | Hang the tongue | Z7 | fitting tongue and rope to the bell | **END** |

Required carried objects: exactly two — the **rope** (CP-05) and the **tongue**
(CP-17). Nothing else in the delve is a key item on the critical path.

## The branch

One branch point, at the end, on one object.

```
CP-22 ──┬── END-THREE   ring three · the way is open
        ├── END-TWO     ring two   · the way is shut
        └── END-SILENT  fell the frame · the bell goes through the floor
```

The three are mutually exclusive and each ends the delve. All three are
reachable from a run that did zero optional content. The optional strands change
the *content* of the chosen ending — who is present, what is said — and never
its reachability.

## Optional strands

Each hangs off a critical-path node and returns to it. None gates another.

### OPT-A · The ledger (Z2)
`CP-07 → A1 the Gatewright (optional elite, gatehouse roof) → A2 guardroom key → A3 the crossing-ledger (G1) → back to CP-07`

The ledger is the priory's list of who bought passage-tokens in the week of the
Long Tide. It is long. The player's own name is on it, but there is no way to
know that yet — the name is confirmed by OPT-C.

Unlocks: Emeric's confession (he is named in the ledger's margin as the runner
who carried the order up), and a dialogue option with Ancel.
Reward: the ledger's strongbox holds a second-tier weapon.

### OPT-B · Ide's rite (Z4)
`CP-11 → B1 Ide teaches the tolls → B2 ring her hand-bell at three stations of her round → B3 the hour-vault opens (G2) → back to CP-11`

The rite is the delve's only "do it the way it is supposed to be done" content
and it is the one that most changes the ending: a player who has done it knows
that a toll is rung *at the ebb, by a hand that owes nothing*, and knows that
their own hand owes something.

Unlocks: END-THREE's full form (Ide walks down off the rock at its head instead
of standing on the stair); Ide stops her round and sits.
Reward: the hour-vault holds the priory's own bell-hand equipment.

### OPT-C · The ferry-tally (Z3)
`CP-08 → C1 swim to the wrecks (G4) → C2 take Odo's tally → back to CP-08`

The tally is every crossing Odo made in thirty years, each line struck through
when the passenger landed. The last line is not struck through and it is the
player's name.

Unlocks: the pacifist resolution of CP-21 — Odo stands aside and follows the
player up. The one place in the delve where a boss is resolved without a fight.

### OPT-D · Hask's passage (Z6)
`CP-15 → D1 find Hask in the side vault → D2 promise him the ebb toll → back to CP-15`

Hask is a living scavenger who came out to loot the rock nine years ago and got
caught by a tide. He cannot cross the flat alone because the answered walk it.
He asks for three tolls rung at the ebb, so he can run for the mainland while
the causeway is dry.

Unlocks: in END-THREE, Hask is on the causeway ahead of the answered, running,
and makes it. In END-TWO and END-SILENT the delve says what happened to him
instead, and it is the sharpest line either ending has.

### OPT-E · The Choir (Z6)
`CP-15 → E1 the Choir (optional elite, side vault) → back to CP-15`

Three of the answered making the sound of a bell with no bell. Pure optional
elite: no story unlock, a gear reward, and it is the fight the delve expects
most players to walk past on a first run.

## Reachability statement

- Critical path: 22 nodes, one chain, no cycles, terminal at CP-22.
- Optional nodes: 12 across five strands, each with exactly one predecessor on
  the critical path and no successors outside its own strand.
- Endings: 3, all from CP-22, all reachable with the optional set empty.
- Locks: 5 shortcuts (S1–S5) and 4 gates (G1–G4). S1, S2, S3, S4 and S5 are all
  opened from their far side. G1 needs the Gatewright's key; G2 needs OPT-B
  completed; G3 needs Ridd's key; G4 needs no key, only the swim.
- No optional item is required by any critical node. No critical item is
  obtained inside a gate.
- Deadlock check: the tongue (CP-17) is obtained below the only route back up
  (CP-18, S4), and S4 opens from the cistern side, so the sequence cannot strand
  a player. The rope (CP-05) is on the Z1 corridor, which is single-route.

## Shortcut ledger

| id | zone | opened from | collapses |
|---|---|---|---|
| S1 | Z2 | inside the gate passage | Z0 → Z2 in one walk; Z1 never mandatory again |
| S2 | Z3 | inside the water-gate tower | the causeway crossing becomes one-way-free |
| S3 | Z4 | the chapel side | Z4 → Z2 yard directly; all of Z3 becomes optional |
| S4 | Z6 | the cistern side | Z6 → Z3 waterline; the descent becomes a drop |
| S5 | Z7 | inside the tower foot | the boss retry walk becomes seconds |

Every one is a door or grate that the player has already stood on the wrong side
of, and every one answers the player when they try it from that wrong side.

## Class fictions

Four classes, chosen at the start; gear is pre-provided and never upgraded by
grinding. Their fiction is *what you were on the flat that night*, and each
matches a role without stating a stat:

| class | was | plays as |
|---|---|---|
| Mourner | came to bury someone | balanced; a staff and a lantern |
| Sexton | worked the rock, carried the dead | heavy; a shovel-blade and a door-shield |
| Ferrier's mate | pulled an oar for Odo | fast, reach; a gaff and a knife |
| Bellwright | came to see about the crack in Mercy | light, tools; a hammer and a coil of line |

The Ferrier's mate gets one extra line from Odo at CP-21, and the Bellwright one
extra from Sister Ide at OPT-B. Neither changes any node.
