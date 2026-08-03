# The Drowned Bell — design of record

- **Status**: authoritative. Stamped **round 3, 2026-08-03**.
- **Scope**: what this delve currently IS. Not history — `GENERATION.md` keeps
  the history, this file keeps the present tense.

## Iteration protocol (standing rule, owner 2026-08-03)

1. This file is rewritten **every round**, before the round's work is committed,
   to describe the design the round is producing.
2. Every round **closes with a conformance review**: read this file against the
   built campaign and fix whichever of the two is wrong. A divergence found here
   is a finding, not a formality.
3. `GENERATION.md` gains one section per round — what changed, what a proof
   rejected, what the ladder said. It is append-only.
4. A design decision that is not in this file did not happen. If a round's work
   implies one, it lands here in the same commit.

## Premise

A tidal keep whose bell once rang the tide out for pilgrims. The bell was cut
down and drowned in the keep's own cistern; the wardens hollowed at their posts.
The party lands on the barrow shore at low water, climbs the keep, raises what
was drowned, and rings it.

Souls delve: death teaches, shortcuts are earned, nothing is explained twice.
1–4 players, `min_players: 1`, target 150 minutes, seed 17.

## World

| | |
| --- | --- |
| Tileset | `pool/tidal-keep`, six pieces, fixed 6/6 |
| Horizon | `ocean` (the keep rises out of a sea backdrop) |
| Difficulty | **`normal`** (round 3) — declared, not derived. The compiler's historical derivation was `easy`, which halves incoming player damage; the souls delve runs at real difficulty |
| Time / weather | **`night` + `thunder`** — the drowned-bell fiction, and the owner's ruling that broad daylight killed the mood (round 2) |
| Lighting | area relight `lantern`, `min_light: 4` — the open-air pieces need it once the sky goes; the gloom stays, the floor stays readable (`DW0210`) |
| Boundary | 16-block margin, tide shoves the party back |
| Languages | English canonical + `zh-cn` sidecar |

## Level chain

The keep assembles as a tree, so every fork and rejoin is authored INSIDE a
piece. Six levels, in solver order:

| L | piece | beat |
| --- | --- | --- |
| L0 | `tk-barrow-field` | shore landing, class pick, BF1, the optional elite |
| L1a | `tk-gatehouse` | timed portcullis, boulder stair (初见杀 #1), spill-shaft shortcut home |
| L1b | `tk-wall-walk` | open parapet, ambush turret |
| L2 | `tk-courtyard-chapel` | the hub: BF2, the Sexton, the cracked bell, two breach lanes |
| L3 | `tk-cistern` | the drowned undercroft, pillar ambush, dart gallery, shortcut A |
| L4 | `tk-bell-tower` | rope room + BF3, bell loft (twist ambush), boss ring, the rope drop |

## Quest spine

Seven quests, strictly sequential (`quest-complete` triggers).

1. **The Landing** — talk to the Ferrywoman → cross the barrow field. Arms BF1
   and defers the Barrow Warden into the field.
2. **The Gate Tax** — pass the portcullis → climb the worn stair.
3. **The Hollow Watch** — walk the wall → find the Sexton. Arms BF2.
4. **The Drowned Way** — drop into the cistern → reach the far side of the
   barred door → return to the hearth. Opens shortcut A.
5. **The Bell Toll** — strike the cracked bell → hold the gate breach → hold the
   wall breach → lay the grave echoes. Three sequential siege phases.
6. **The Keeper** — rope room (arms BF3) → the loft → kill the Bellkeeper.
7. **Ring It Home** — hang the bell → take the rope drop into the chapel → tell
   the Ferrywoman. `campaign-complete`.

## Bonfires and loops

- **BF1** barrow fire (`anchor/l0-bonfire`), armed on first contact.
- **BF2** chapel hearth (`anchor/l2-bonfire`), armed on meeting the Sexton.
- **BF3** rope room (`anchor/l4-bonfire`), armed on entering the tower.
- **Shortcut A** — the chapel side door (`shortcut/chapel-door`), barred from the
  far side, thrown from behind after the cistern's long route. Permanent: no
  emitted function ever re-seals it.
- **Spill shaft** — a one-way geometric drop from the stair-head runout back to
  BF1. The thing that kills you IS the shortcut you learn.
- **Rope drop** — the L4 hub fold: the bell rope falls through the keep's heart
  into the chapel, collapsing the whole climb into one keep at the end.

## Set pieces

### The optional elite — the Barrow Warden

A dormant `wither_skeleton` NPC kneeling among the graves, athwart the
spawn→gate desire line. It never moves unprovoked. Striking it
(`trigger/warden-answers`) despawns the NPC and unleashes a real-AI twin, aggro
locked onto whoever struck. Both flank lanes are proven open by the generator,
so "optional" is geometry, not a promise.

**Round 2 (owner: it was embarrassingly weak):** full netherite, Protection IV on
every piece, netherite axe with Sharpness XII and Knockback I, via actor
`equipment` (spec-0021). Drop chances are zero — an actor's kit is never
farmable.

### The timed portcullis (L1a)

`timed-gate/portcullis`, **70 ticks open / 30 closed** (round 2 — the old
100/100 read as sluggish); no `phase`, so the clock's first act is an open, as
the prefab ships the gate sealed. The cycle halves (200 → 100 ticks) and the
shut phase drops to a third, which is what "sluggish" actually meant. A tighter
50/30 was tried first and the bot was crushed in it: `DW0378` admitted the
window, but a ~1s entry gap is not a timing read for a solo player, it is a
reflex test. A roofed watch bay six blocks out holds
clean line of sight up the passage, so the cycle is readable before anyone
commits. **`crush: true`** (round 2): a player inside the gate region on the
closing tick is killed by command. `DW0378` proves the admitting window is a
readable fraction of the cycle, which is what earns the right to make the
penalty absolute.

Round 2's blocker is **fixed** (engine #204): both gate-crossing legs now emit
only the flanking pair `[24, 63, -9]` / `[24, 63, -11]` and nothing inside the
region, so the crossing is one hop between footings and nothing parks under the
portcullis.

### The boulder stair (初见杀 #1, L1a)

A long straight run whose centre lane is polished smooth by a century of rolling
stone — the palette IS the tell. A plate row mid-run springs
`trap/stair-volley`. The runout alcove at the head hides the spill shaft.

**Round 2 — traps v2 (spec-0022):** the payload is a command `volley`, not
dispenser wiring. Fired from `anchor/l1a-volley-slot` (the vault down-run of the
arch rib) into a kill zone centred on `anchor/l1a-stair-run`, extent `[2,1,2]`,
3 salvos at 10 ticks. Saturation, not sniping: `DW0442` proves a clear line of
fire to every standable cell, so escaping means leaving the zone. The dispenser
stays in the rib as visible scenery.

### The dart gallery (L3)

A tripwire over the exit climb, disarmable at `anchor/l3-dart-lever` behind a
grate on the far side (`flag/darts-stilled`). Also a `volley` in round 2, fired
from `anchor/l3-gallery-slot` at the head of the shaft — three treads ABOVE the
plate, so the climber walks into the fire rather than being shot in the back.

### Ambushes

Un-telegraphed by design (souls vocabulary; the compiler asks for no tell), each
with proven counterplay.

| ambush | where | actors |
| --- | --- | --- |
| `ambush/wall-watch` | parapet mid | `actor/wall-sentinel` (zombie) |
| `ambush/cistern-pillars` | the item alcove | `actor/pillar-warden-a`/`-b` (husks) |
| `ambush/the-rafters` | the loft doorway | `actor/rafter-1`/`-2` (husks) |

Round 2: the wall sentinel gains an **iron helmet** — the sanctioned fix for a
bypassed undead standing under an open sky (never `set-time`). The two cistern
wardens carry heavily enchanted netherite axes (see *Difficulty*, below).

### The courtyard siege (L2)

Three sequential phases, melee-only, so peak simultaneous pressure stays at two
plus at most one stalker: gate lane (2 vindicators) → wall lane (1) → grave
echoes (2 husks, `summon: aggro-edge` out of the grave soil). Gate and wall
squads walk authored TD lanes.

### The Bellkeeper (L4 boss)

A named `wither_skeleton` walking a fixed round on the open annulus around the
bell pit. Anti-Capra by construction: no closets, no chokepoint, visible from the
ring doorway. The loft's rafter perches are in clean sightline from the loft
door — the twist is meant to be seen and beaten.

## Containers

Every reachable container is filled by the compiler (`loot[]`, spec-0021); the
furniture belongs to the prefab and the compiler never places it.

| loot | container | contents |
| --- | --- | --- |
| `loot/barrow-cache` | barrow reward barrel, behind the elite | Grave-Goods Apple, 2× Hearth Stew (two stacks — stew caps at 1) |
| `loot/tide-stores` | undercroft item alcove | 3 cooked cod, 16 Grey-Fletched Arrows |
| `loot/sexton-cell` | the drowned side-cell | The Sexton's Tide Ledger, Hearth Stew |

The elite's cache is the reward for taking the optional fight; the side-cell is
the one secret, entered through a visibly broken grate (no illusory walls
anywhere in this tileset).

## Classes

Four, each two-armour-pieces plus a weapon and stews: Warden (iron helm + iron
cuirass, sword and shield), Steeple Archer (leather, bow), Lampbearer (leather
helm + iron plate, sword and soul torches), Underminer (chainmail, axe and
throwables). Armour totals 8 / 4 / 7 / 7 points respectively — the Warden is the
binding case for every damage number below.

## Difficulty

Declared **`normal`** (round 3). Two round-2 constraints are now gone: the
`difficulty` field exists, and `actors[]` takes `attributes`.

The retune this forced is smaller than it looks, because attacker-less `/damage`
— which is how every `damage-players` emission lands — does **not** scale with
difficulty. Eight of the nine DSL damage types ignore the Easy halving, so the
trap, gate and scripted numbers were already being measured at their true value.
What changes at `normal` is **mob melee**, and exactly one encounter was tuned
around the halving:

- **Cistern wardens.** Round 2 gave them Sharpness XIX to buy back the halving:
  husk 3 + netherite axe 9 + 10 = 22 raw, halved to 12, landing 11.04 on the
  8-armour Warden kit — two hits. At `normal` that same axe lands
  `22 × (1 − max(1.6, 8 − 11)/25)` = **20.6, a one-shot from full health**. The
  enchantment is dropped: a plain netherite axe is husk 3 + 9 = **12 raw**, which
  is `12 × (1 − 2/25)` = **11.04** again — the same two-hit kill, now stated
  honestly instead of through the halving. Against the 4-armour Archer kit it is
  11.6. The 初见杀 character is unchanged; only the arithmetic moved.

Everything else roughly doubles at `normal` and was left alone, because the
compiler's winnability proofs accept it: the gate vindicators land 7.74/hit
(was 4.35), the wall vindicator 8.8, the grave echoes 1.44, the Bellkeeper 4.8
plus its Wither. `DW0470`–`DW0475` all pass — nothing is unkillable, unfightable,
absurdly tanky or an unavoidable ≥20 hit, and the kits carry food.

**The optional Barrow Warden was deliberately not softened** (owner rule): full
netherite, Protection IV, Sharpness XII axe. At `normal` it lands ~18.25 on the
Warden kit — one hit short of a one-shot, which is what an optional elite you
chose to wake should feel like.
