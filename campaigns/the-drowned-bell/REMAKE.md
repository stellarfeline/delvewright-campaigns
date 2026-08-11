# The Drowned Bell — remake design (10× castle)

- **Status**: **owner-approved in conversation, 2026-08-04** (task #182);
  design of record for the remake. Owner directives
  folded in: 10× castle via the grammar back end (spec-0027); souls staging
  authored AT THE PREFAB LEVEL, not sprinkled on top; elite/boss deterministic
  declared-subset drops (#179); real healing potions (#116); difficulty ×10;
  the knockback-niche cliff path is mandatory vocabulary, verbatim from the
  owner. Pattern catalogue mined from `docs/notes/souls-design-language.md`
  (the dossier) — sections cited as §n.

## 1. Premise (continuity, not a reboot)

Same fiction, grown to citadel scale: the tidal keep was never a lone tower —
it was the gatehouse of **Tidesend Citadel**, a drowned pilgrimage fortress
on a sea crag. The bell still hangs at the summit; the party still lands on
the barrow shore, still rings it home. The Ferrywoman (skin fixed: a woman),
the Sexton, and the Bellkeeper survive as cast. Everything between the shore
and the bell is new.

Target: 150–180 min, 1–4 players, seed-fixed, `difficulty: hard` (see §7).

## 2. Scale accounting — what "10×" buys

Current bell: 6 prefab pieces, 6 levels, 3 bonfires, 1 optional elite, 1 boss,
2 shortcuts. The remake:

| axis | bell r5 | remake |
|---|---|---|
| prefab pieces | 6 (hand generators) | ~40–60 grammar-expanded boxes in 8 zone programs |
| zones | 6 | 8 (below) |
| bonfires | 3 | 6 |
| shortcut loops | 2 | 5 (1 hub-opener + 4 local) |
| optional elites | 1 | 4 |
| stage bosses | 1 | 3 + final |
| 初见杀 set pieces | 2 | 6 (one per zone past the shore, teach→test→twist paced) |

The grammar back end carries the mass: each zone is ONE grammar program
(castle typology is in the ported rule library), seed-varied candidates,
machine-gated (§4 craft diagnostics), owner-curated contact sheet. Staging
hardware (niches, watch bays, murder holes, kickable ladders) enters as
**grammar-rule vocabulary** — split rules that emit the souls furniture — so
the flavor is structural, not decorated afterward.

## 3. Zones and the bonfire/loop topology

Ascent order (Demon's-Souls strict-hub is rejected; we build the DS1 shape —
one hub that the world folds back into, §1.2):

- **Z0 Barrow Shore** — landing, class pick, **BF1**. Optional elite #1
  (Barrow Warden, kept, dormant among the graves).
- **Z1 Cliff Road** — the owner's set piece: a switchback path cut into the
  sea crag, one block wide on the outer edge, cliff on one side. Wall niches
  hold **knockback ambushers** (§5, entry K). Teach→test→twist across three
  niches. No bonfire — Sen's-style withheld rest (§5.1 dossier).
- **Z2 Gatehouse + Outer Ward** — timed portcullis (crush, watch bay), boulder
  stair (kept, worn-tread tell), **BF2**. Stage boss #1: the **Gate Reeve**.
  Local loop A: portcullis bypass sally-port, barred far side.
- **Z3 Drowned Lower Ward** — the toll road (§7.2): a flooded ward, wading
  slows and drowns-in-armor pressure, attrition husks; a **dry causeway**
  exists, guarded by optional elite #2. Local loop B: sluice gate drains a
  side channel permanently (shortcut unlock = the drain wheel, far side).
- **Z4 Chapel Ward** — **THE HUB. BF3** at the chapel hearth (Sexton).
  Every later shortcut lands here. Siege defense beats (rebuilt: real
  composition, see §7) happen in this ward's yard.
- **Z5 Great Hall + Keep** — rafter ambushes over the hall (Cathedral
  grammar: perches in sightline from the door, §4.1), container ambush in
  the stores, bait-item on the gallery. **BF4** in the kitchen. Stage boss
  #2: the **Hall Marshal**. Local loop C: kitchen dumbwaiter shaft down to
  Z4 (ladder-kick equivalent).
- **Z6 Cistern Deep** — the drowned bell itself, dart gallery (kept,
  disarmable), pillar wardens. Optional elite #3 guards the one secret
  (grate visibly broken — in-world cue rule, §7.3). Local loop D: the
  cistern stair, barred from below.
- **Z7 Bell Tower** — rope room **BF5**, loft twist ambush (exposed, §4.4
  "twist" = very predictable, foilable), boss ring: **the Bellkeeper**,
  rebuilt (§6). After the bell: **the hub-opener** — the rope drop grows
  into a full elevator-kick: the bell's counterweight lift descends the
  keep's heart to the chapel (Z4). The world folds into the hub exactly
  once, at the climax (§1.2: hub-openers are once-per-game).
- **BF6** sits before the boss ring (DS3's missing-bonfire-before-boss is
  cited by the dossier as an experienced GAP — we don't reproduce it).

Runback budget: ≤ 30 s bonfire→failure-point (box-garden-scaled per §1.4
verdict; the 60 s lint is inert at our scale), measured per failure point.

## 4. The prefab-level staging catalogue (mined from the dossier)

Each entry: pattern → grammar/prefab realization → where. This is the
vocabulary the zone programs must emit as STRUCTURE.

| # | pattern (dossier §) | prefab realization | where |
|---|---|---|---|
| K | **Knockback niche on a one-wide cliff edge** (owner verbatim; §4.1 corner discipline) | niche cells recessed 1 into the inner wall of a 1-wide outer-edge path; ambusher holds a Knockback II blade; the niche is VISIBLE as a shadowed recess from the previous switchback (observability §2.2-5) — the first-time player who doesn't look dies to the sea | Z1 ×3 (teach: niche with a corpse + scattered gear; test: occupied, silhouette readable from below; twist: pair, one visible one hidden, the visible one baits the sightline) |
| A | Corner/doorway ambush (§4.1) | door-adjacent blind cells emitted by the door split rule itself — every "door" production has an optional flanking-alcove expansion | Z2, Z5, Z6 |
| R | Rafter/ceiling drop (§4.1 Cathedral) | hall grammar emits truss perches with clean sightline from the entry door (fairness = silhouette, §4.3) | Z5 great hall, Z7 loft |
| C | Container ambush (§4.1 Depths) | stores grammar mixes real loot barrels with a declared ambush container; tell = the odd one out is unbanded | Z5 stores |
| B | Bait item + co-located visible ambusher (§4.2 variant 1 ONLY; variant 3 displaced-trigger is BANNED as resented) | gallery item on a pedestal, ambusher hanging in frame above it | Z5 gallery |
| W | Worn-tread tell (§5.1 Sen's) | boulder-path stair rule emits smooth-variant treads down the hazard lane — the palette is the telegraph | Z2 boulder stair |
| O | Watch bay before every timed hazard (§5.3 — observability is THE rule) | every timed-gate/trap program emits a roofed bay with line of sight to the full cycle, outside the hazard span | Z2 portcullis, Z6 dart gallery |
| S | Safe pockets along a hazard run (§5.2 chariot alcoves) | boulder stair emits side alcoves at rhythm intervals | Z2 |
| D | Disable-able hazard, third rung (§5.2) | dart gallery lever behind grate (kept); NEW: the boulder release can be jammed from the stair head (timed-gate disarm, G2) | Z2, Z6 |
| L | One-way drops / ladder kicks / elevator kick (§1.1) | spill shaft (kept, Z2→BF2); dumbwaiter (Z5→Z4); cistern stair bar (Z6); counterweight lift (Z7→Z4 hub-opener) | per zone |
| F | Far-side barred door (§1.1) | sally-port + sluice wheel + stair bar — all `shortcut{gate,unlock}` with the bar physically modeled on the far face | Z2, Z3, Z6 |
| T | Toll road with a dry path (§7.2 — a swamp with no dry path is a tax) | flooded ward floor rule + raised causeway rule in one program; the causeway is guarded, the water is slow attrition | Z3 |
| E | Dormant optional elite in open ground (§3.3 four signals: no fog gate, open ground, dormancy tell, over-dressed) | kneeling/stationed pose, oversized silhouette, gold-accent armor; aggro only on strike or close approach; both flank lanes proven | Z0, Z3, Z6, Z7 approach |
| M | Mandatory-commitment marker (G5 dual of the fog gate) | boss thresholds get a uniform prefab motif: a bell-rope curtain + narrate line; taught at Z2's boss door, reused exactly at Z5/Z7 | boss doors |
| X | Secret with in-world cue (§7.3 — no message crowd exists) | ONE secret, behind the visibly broken grate | Z6 |

Anti-patterns, enforced in review: no boss-with-adds in a sealed closet
opening with an instant lunge (§2.1 Capra); no displaced-trigger ambush
(§4.2-3); no sound-cue-dependent fairness (§4.3); no illusory walls (§7.3).

## 5. Encounters, drops, and the ×10 contract

**Deterministic declared-subset drops (#179).** Every elite/stage boss wears
a full kit; the DSL declares WHICH pieces drop (per-slot drop_chance 1.0 on
declared, 0.0 on the rest — vanilla primitive, no hack):

| enemy | wears | declared drop |
|---|---|---|
| Cliff niche twins (Z1, elite pair) | chain + **Knockback II iron sword** | the sword (one of the pair only — the twist niche) |
| Gate Reeve (Z2 boss) | full iron, Sharpness III axe | **the axe + the sally-port key** (quest item) |
| Causeway Keeper (Z3 elite) | netherite boots (dry-footed on the causeway — the gear tells the story) | **the boots** |
| Hall Marshal (Z5 boss) | netherite chest + helm, shield | **the chest piece** |
| Cistern grate elite (Z6) | trident + drowned kit | **the trident** |
| Barrow Warden (Z0, kept) | full netherite Prot IV, Sharpness XII axe | **the helm** (the axe stays too strong to hand out — one piece, not the jackpot) |
| Bellkeeper (final) | — | **the Bell Hammer** (quest item that rings it home) + its blade |

Drops are power the route EARNS — the Z1 knockback sword is the player's
own niche-ambush tool for the rest of the climb; the Z3 boots make the
flooded ward walkable. That is the souls economy without currency (§7.4:
what survives translation is recoverable-once / earned-once, not farming).

**×10 difficulty** is composition + equipment + density, not HP sponges:
declared `hard`; no unarmored single zombies anywhere (the wall-zombie
finding); every wave armed and armored per zone tier; siege waves rebuilt
with vindicator cores + ranged support + aggro-edge summons layered per
phase; wave counts sized so peak simultaneous pressure ≈ 4–5 on a solo
player (bell r5 peaked at 3). Winnability proofs (DW0470–75) remain the
floor; the die-retry ladder stage must die at every new set piece.

**Healing**: every class kit declares **real healing potions** (#116
`contents`) — flask count 3–5 by class, refilled at rest, never farmable
(§8 green zone).

## 6. The Bellkeeper, rebuilt

Kept anti-Capra (open annulus, visible from the door), but ×10: two phases —
the walked round (phase 1) breaks at half health into bell-pit combat where
the loft rafters spill their remaining ambushers INTO the ring (the twist
the player already saw from the door — §4.4 predictable-third-beat). BF6
directly before; runback ≈ 15 s.

## 7. Engine prerequisites (all scheduled, none new)

1. **#180** rest/death re-seat: undefeated boss/elite deletes + respawns at
   origin, full HP — the foundation, first in queue.
2. **#179** declared-subset drops — DSL surface (per-slot drop_chance).
3. **#116** kit potion contents — in the merge train now (#245).
4. **G1 observability proof** (dossier): standable cell outside hazard span
   with line of sight — promote from gap to obligation for every timed
   hazard in this campaign (engine task, error tier for the remake).
5. **G2 timed-gate disarm** — the boulder jam (entry D). Small DSL surface.
6. **#163** grammar back end — the mass generator; zone programs are its
   first production workload after the temple contact sheet.
7. **#181 batch** (narrate rewrite, ferrywoman skin, shortcut prompt naming
   the hearth NPC, wave guidance) folds into the remake rather than
   patching r5 twice.

## 8. Build sequence

1. #180 + #179 + G1/G2 engine round (workers, serial with CI).
2. Grammar zone-program vocabulary: the staging catalogue (§4) lands as
   library split-rules with fixtures (K, R, O, W first — they carry the
   most flavor per rule).
3. Zone contact sheets → owner curates massing (8 sheets, one per zone).
4. Campaign DSL (planner-personal), zone by zone, ladder green per zone.
5. Full ladder + owner playtest — new-campaign gate: she plays before main.
