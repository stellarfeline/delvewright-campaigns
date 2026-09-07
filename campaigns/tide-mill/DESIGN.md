# Tide Mill — design record

Demo level for **timed gates** (spec-0016 §4 + the `crush` addendum), from the
`docs/demo-levels.md` queue. One mechanic in the spotlight, minimum cast, linear,
10–20 minutes. This file is the authoritative design; the stage JSONs implement it.

## Premise

Sedgewick Mill is a **tide mill**. The flood fills the pond behind the sea wall;
on the ebb the miller lets the water out down the race, and the race turns the
wheel. Three sluices stand along that race, and they are not levers — they run on
the sea's own clock, opening and shutting on a count nobody has changed in two
hundred years.

This ebb the brake pin sheared. The wheel is running free and will shake the mill
apart before the water is out. The brake stands at the far end of the race, past
all three sluices. Corrin Sedge, the miller, cannot run them any more. You can.

## Cast (one)

- `npc/miller` — **Corrin Sedge**, tide-miller, `minecraft:villager`, at
  `anchor/l0-tide-line`. He exists to hand the player the *count* — the level's
  entire teaching mechanism — and to state the stakes of the third gate before it
  can kill anybody.

## Layout (verified against seed 41)

| area | pool | pieces | fiction |
|---|---|---|---|
| `area/millrace` | `pool/tidal-keep` | 3 | tide-line yard → grate house → wheel pit |
| `area/undertow` | `pool/stone-keep` | 3 | spill room → tide gate → brake loft |

- `tk-barrow-field` = **the tide-line yard** (player spawn; Corrin)
- `tk-gatehouse` = **the grate house** — GATE 1
- `tk-cistern` = **the wheel pit** — GATE 2
- `keep-spawn-hall` = **the spill room** (the undertow lands you here)
- `keep-gate-room` = **the tide gate** — GATE 3, `crush: true`
- `keep-shrine` = **the brake loft** (finale)

**Inter-area transport is the point of no return.** The two areas are 256 blocks
apart across void, so completing `obj/wheelpit` teleports the party and the walk
back does not exist — physically enforced, not asserted. Diegetically: the
undertow takes you under the sea wall. Nobody swims back up a mill race.

## The three windows

`DW0378` charges the crossing at the `DW0355` sprint model (4 t/block) over the
A\* span between the footings either side of the gate. **The compiler measures all
three gates at 8 ticks (2 blocks)** — verified by deliberately failing each gate
in turn on a throwaway copy and reading the number out of its `DW0378` message —
so the crossing cost is a constant and the escalation is purely in the clock.
That is deliberate: the demo holds every variable but the window.

    admits  = open − 8 + 1 = open − 7
    window% = ⌊ admits · 100 / (open + closed) ⌋   ≥ 20 required

| gate | anchor | open | closed | cycle | phase | admits | window | crush |
|---|---|---|---|---|---|---|---|---|
| `timed-gate/grate` | `anchor/l1a-gate-timed` | 120 t (6.0 s) | 40 t (2.0 s) | 160 t | 0 | 113 t | **70 %** | no |
| `timed-gate/wheel` | `anchor/l3-shortcut-a` | 60 t (3.0 s) | 80 t (4.0 s) | 140 t | 25 | 53 t | **37 %** | no |
| `timed-gate/tide` | `anchor/gate` | 36 t (1.8 s) | 84 t (4.2 s) | 120 t | 55 | 29 t | **24 %** | **yes** |

The open half falls **6.0 s → 3.0 s → 1.8 s** while the shut half rises
**2.0 s → 4.0 s → 4.2 s**; the admitting share of the cycle falls
**70 % → 37 % → 24 %**. The third gate sits four points above the `DW0378` floor:
provably fair by the same arithmetic that proves the first one generous — and a
provably fair window is what earns an absolute penalty for misreading it
(spec-0016 §4 addendum). The first two gates teach the read; the third bills it.

Phases are staggered (0 / 25 / 55) so the three clocks never beat in unison — the
race should sound like a mill, not a metronome.

## Beats

1. `obj/hail` — talk to Corrin at the tide line. He gives the count for gate 1,
   halves it for gate 2, and says plainly that gate 3 has killed people.
2. `obj/grate` — through the grate into the sluice house. **Teaches**: 6 s open is
   long enough to walk it wrong once and still get through.
3. checkpoint at `anchor/l1a-ward` — governs the run at gate 2.
4. `obj/wheelpit` — through the wheel sluice into the pit. **Tightens**: 3 s, and
   the shut half is now longer than the open one. Completing it flushes the party
   into `area/undertow` **and moves the checkpoint across with them**, to
   `anchor/keeper-stand` — see below.
5. `obj/read` — stand at the mark in the spill room. The warning about the tide
   gate fires **here**, 13 blocks short of it, so the lethal beat cannot arm
   before the player has read what it is (owner ruling 2026-08-03).
6. `obj/brake` — through the tide gate, throw the brake. Ending
   `ending/wheel-stilled`.

### Checkpoints and the one-way transport

The obvious placement — a checkpoint at `anchor/l3-landing`, where the party
clears gate 2 — is **wrong and the compiler says so** (`DW0315`): the transport
fires on that same objective, so respawning there would put the party back in
`area/millrace` with the rest of the campaign on the far side of 236 blocks of
void. Nothing can be walked back.

So the campaign has exactly two checkpoints:

| fires on | at | governs |
|---|---|---|
| `obj/grate` | `anchor/l1a-ward` | the run at gate 2 |
| `obj/wheelpit` | `anchor/keeper-stand` (in `area/undertow`) | the run at gate 3 |

The second one is deliberately set from a quest in the *other* area: it moves the
party's respawn into `area/undertow` on the very tick the undertow lands them
there, so there is no window in which a death sends them somewhere they cannot
finish from. `anchor/keeper-stand` is 13 blocks upstream of the crush gate, so a
death at gate 3 costs one short walk and re-runs no earlier gate.

No branch points: the level is linear by brief. No waves, no bonfires, no traps —
the only lethal element in the delve is the closing edge of gate 3, and it has a
checkpoint 13 blocks upstream of it.

## Classes

Two, both traversal-flavoured (there is no combat):

- `class/race-walker` — sure-footed on wet stone; carries Sedge's tide-clock.
- `class/sluice-keeper` — reads water; carries the marker lamp.

The race-walker's boots were designed with Feather Falling on them. **They ship
plain**: the stage-3 `KitItem` surface is `{item, count, name?, carrier?, flask?}`
and has no `enchantments` field (it exists on wave `equipment` and on `loot`
stacks only). Recorded as friction rather than worked around — the class reads
the same, and nothing in the level depends on fall damage.

## What a player should leave knowing

That a timed gate is a **read**, not a gamble: you stand off, watch one full
cycle, and enter on the edge. The level proves it by giving that read three times
with the same crossing cost and three different windows, the last one lethal.
