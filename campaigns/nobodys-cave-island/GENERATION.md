# nobodys-cave-island — generation record

- **Date**: 2026-08-01
- **dsl_version**: 0.6.0 (delvec 0.1.0, MC 1.21.11)
- **Author**: planning agent (planner-personal authoring; owner production
  order 2026-07-31: showcase the toolchain — wherever the brief leaves a
  choice open, use every feature the current DSL supports)
- **Prompt (constraint set)**: the owner's island staging vision (beach camp /
  offshore galley / greenfield / mountain-interior cavern; pseudo-open-world,
  no filler corridors, zero inter-area transports) + the full dramaturgy in
  `DESIGN.md` (B0–B6, two endings, three checkpoints). Everywhere unspecified,
  the design deliberately uses every feature the v0.6 toolchain supports.
- **Relationship to `nobodys-cave`**: full remake on the island stage; the v0.4
  corridor original ships separately (content PR #1). Narrative beats and cast
  carry over; the name-branch echo variants (nobody/boast/lie) carry over from
  the round-2 fix.

## Decisions

- One contiguous area (`area/island`, `pool/island`, 4 pieces fixed:
  beach-camp → greenfield ×2 → mountain). No inter-area teleports anywhere.
- The galley is merged into the beach-camp prefab (engine generator change):
  the DSL has no scenery-offset mechanism and areas sit 256 blocks apart, so
  "anchored just offshore" is only achievable inside one piece — the fallback
  explicitly reserved in DESIGN.md §5.
- Polyphemus staging per the W-G spike verdicts: NoAI warden puppet
  (`vulnerable: false`), walk = `move-actor`; hurt-flash and death are the only
  forceable animations; the giant's punch = camera cut + sound + kill-style
  despawn; roar = sound + positioning. No live-AI warden ever (self-digs and
  despawns in ~5 s — owner playtest finding, spike-confirmed).
- Planner addition pending owner veto: the dusk 3-drowned surf tutorial wave
  (B0).
- Seed: 9 — Odyssey, Book 9.

## Process log

(appended as stages complete)

### 2026-08-01 stages complete

- Stages 1–3: validate exit 0. Dark cavern preserved via night-vision kit items
  (NO relight — alcoves stay black). Three classes (odysseus/polites/eurybates);
  quest-critical items (wine, stake) delivered by quest beats, never kits.
- Stages 4–6 + l10n: validate/analyze/build en+zh all exit 0, byte-identical
  double builds. 9-quest convergent DAG, two endings (THE QUIET SAIL / NOBODY),
  3 checkpoints with distinct on_respawn hooks, warden puppet + 8 sheep actors,
  2 stealth beats, 1 spectator dolly (boulder seal), 171 zh-cn keys.
- Deviations from DESIGN (schema-forced, recorded honestly):
  meadow/fold anchors DW0305-ambiguous (greenfield placed twice) → Q2 single
  reach-the-mouth leg; Eurylochus walks via move-npc (no NPC re-place
  primitive); boulder seal = narrate+sound+dolly (no close-gate verb yet);
  stealth caught-consequence soft (no damage verb yet). The last two are
  engine-verb gaps queued for first-class fixes; two compiler bugs found during
  authoring (DW0210 l10n-dependent verdict; sequence-nested producer
  mis-indexing) escalated per debug doctrine.

### 2026-08-01 v0.6.1 rewire (close-gate / damage-players)

- Q4 seal sequence now fires `close-gate anchor/boulder` (physical basalt fill,
  #106) alongside the Sealed In title; Q7's existing nested `open-gate` becomes
  the true reopen. Both stealth beats' `on_caught` now end in
  `damage-players 40` (#107): caught = death = last checkpoint, per the
  approved design ("Caught during any of it → death → CP").
- First build after the rewire failed DW0311: the nav gate-state scan is
  another top-level-only effect consumer (sees neither nested open-gate) —
  the same defect class as the #102/#104 walkers. Escalated into the in-flight
  nested-consumer recursion PR rather than lifting the open-gate out of the
  finale sequence (content must not dodge toolchain bugs).

### 2026-08-01 machine playthrough green (bot 22/22, PackTest 19/19)

Three ladder rounds to full green, every red fixed at root, none in content-dodge:
1. Ocean world booted as void (delve image ignored the build's
   generator-settings) + two PackTest templates assumed single instances —
   toolchain, fixed (#103).
2. Surf-wave third drowned never died: bot target selection classed Invulnerable
   mannequin NPCs as wave mobs and fixated on Eurylochus's puppet — harness,
   fixed (#109; kill steps now count confirmed kills and blacklist unkillable
   targets). Content kept the follow_range 48 aggro raise: the tutorial wave
   now rushes the camp as designed.
3. Pen-approach wedge: the compiler's full-cube model proved a waypoint ON TOP
   of a 1.5-block oak fence; the real route is through the adjacent gate —
   harness, fixed (#110; waypoint replay skips non-physical supports,
   canOpenDoors for adventure-legal gate use). Residual compiler-model
   soundness gap (fence-top false proofs with no adjacent opening) filed as an
   engine follow-up task.

### 2026-08-01 player-POV visual review (first live Chunky run)

221/221 POV scenes rendered (draft 960×540, spp 32) after two toolchain fixes
the first run flushed out: delve-render's Chunky camera mapping used a naive
to_radians (every POV camera aimed at the ground — root-caused against the
Chunky core's bytecode basis, fixed + regression-tested, #111), and emitted
scene world.path is relative (patched locally; delve-render fix pending).
Planner review of the corrected set: surface legs read correctly at eye level
(beach approach, terraced climb with the cave mouth ahead, gangplank/deck
arrival with lantern glow). Declared-dark cavern shots render faithfully dark —
Chunky cannot emulate the night-vision mitigation and the render plan carries
no per-shot darkness flag; dark-interior review stays in-game for now
(engine follow-up filed). No blocking content defects found; backlog noted:
mountain exterior silhouette polish, unflattering framing on rising-step
waypoints.

### 2026-08-01 QA round 3 (owner live findings → 8 engine PRs + content rework)

Owner LAN + singleplayer playtest yielded six findings; every one fixed at
root, none patched over:
- zh l10n rewritten in full by the planner (per-persona voice, 182 keys).
- Wine now issued to the whole party before the climb (Q1 end) — no class
  soft-lock, narrative-consistent with the class blurbs.
- Cheese-store crowding: Perimedes re-anchored to alcove-2; Eurylochus's
  guided walk ends at the checkpoint shelf, off the interact marker.
- Polyphemus + Perimedes are deferred NPCs (#113): the giant does not exist
  until the herd enters — walker puppet swaps to the dialogue statue at
  arrival via on_arrive, statue exits for the blind-patrol era, wake-trigger
  summons the unleashed warden on demand (also fixes a latent two-giants
  overlap post-blinding).
- Night vision is now an area declaration (#114) emitting a persistent effect
  clock; the renamed-water-bottle "potion" is deleted; the compiler invariant
  "semantics never key on player-facing free text" is documented.
- NPC block-clipping root-caused (#115): entities were emitted at cell
  CORNERS (~70% inside walls); all summons/tps now cell-centred.
- Sea level (#116): ocean areas place at the waterline datum (walk plane 63,
  sea 62 — vanilla-normal shoreline); new DW0344 proves waterline==sea level.
- Singleplayer parity (#117–#120): the island had NO entry point (anchor
  `entry` vs compiler's `spawn` — DW0345 now catches it); first-join placement
  is datapack-owned + respawn_radius pinned; dialogue triggers re-arm in the
  handler (immune to the singleplayer pause tick-freeze); resource-pack
  pack.mcmeta gains 1.21.11 min/max_format (skins actually load client-side).

### 2026-08-01 QA round 4 (owner findings → 9 engine PRs + content rework)

Owner round-4 playtest + design session. Engine (#121–#129):
- Cutscenes: look_at aim + multi-shot cinematic sequences (#124); "a cutscene
  is pure observation" invariant — stealth clock and damage-players frozen for
  players in cinematic state (#125); strike triggers fire on Invulnerable
  NPCs via shared hitbox tagging — root cause was overlapping interaction
  entities racing the attack raycast (#128).
- Greenfield trees regrown structurally (lean-or-grow rule, canopy ≥3 above
  the walk plane, corridor-clearance generator invariant) — no more sheared
  half-trees (#121).
- DW0330 on-screen text-width lint (measured font metrics: Han 9px, Latin
  6px, em-dash trap) (#127); art font fixed to source scale (#129).
- Pluggable external-LLM l10n (delvewright.toml + tools/i18n-translate.py +
  l10n-inventory subcommand) (#122).
Content:
- Cheese is a collect objective (take a wheel from the barrel), not an
  interact marker; wine-offer dialogue gated on flag/sealed-in (the empty
  wine-node soft-lock); Eurylochus hides in the alcove with the player on
  the wait branch; seal cutscene re-authored as two shots (hall-wide toward
  the dying light, then close on the stone).
- Subtitle discipline: 15 prose narrates demoted subtitle→chat (subtitles
  are one-line punches, chat carries prose); ending banners now plain
  fullscreen titles — en NOBODY / THE QUIET SAIL, zh 无人 / 悄然扬帆
  (owner: no pixel-art banner needed; the art font remains an engine
  capability, unused here).
- Owner rulings recorded: old corridor campaign PR closed (superseded);
  helmet-not-set-time is the proper daylight-undead fix (wave equipment
  field queued); routed-then-feral TD movement queued as an M4 primitive.

### 2026-08-01 round-5 delivery addenda

- Surf drowned now wear leather caps via the new wave `equipment` field
  (#130) — the owner's ruling: helmets, not clock changes, are the correct
  daylight-undead protection (dusk kept purely for drama).
- Two PackTest reds root-caused to the BATCH MODEL (#135): the generated
  suite runs as one batch on one shared server — one dummy per test, all
  coexisting — so `@p` in a template can retarget to a neighbor's dummy and
  `@a`-wide flag writes pollute sibling tests. Templates now pin their own
  dummy. Island 27/27, hollow-vigil 11/11.
- Owner rulings this round: old corridor campaign PR closed permanently;
  ending banners are plain fullscreen titles (art font retired from this
  campaign; zh shows 无人 / 悄然扬帆); cheese is a collect-from-the-barrel
  objective; specs 0013/0014/0015 approved.

### 2026-08-01 QA round 6 (owner findings → 4 engine PRs + the seal beat re-staged)

Owner round-5 findings; engine first (#142–#144, plus #140 landed in parallel),
then this content pass:
- **Giant-dialogue soft-lock root-caused (#142)**: two co-located interaction
  hitboxes at the fire-pit (the world-init strike-trigger box shadowing the
  NPC's own); every right-click resolved to the wrong entity. The reported
  left-click was a red herring. One-cell-one-hitbox rule + DW0350.
- **Stealth no longer wants a crouch (#143)**: zone presence = hidden,
  engine-wide; the spectator camera no longer strobes if a player holds sneak
  mid-cutscene (input-predicate gated re-attach).
- **Staging primitives (#144)**: move-npc on_arrive, forbids_flags, DW0351
  continuity lint, chained move origins (the giant now genuinely walks).
- **The seal beat is a 40 s six-shot cinematic** (was 7 s of shots): the flock
  streams in past the boulder-side camera; the giant fills the hall-wide
  doorway and ducks through; Antiphos — who now climbs with the party,
  carrying the provisions, while Elpenor holds the beach alone — is taken in
  the light of the mouth, on camera; the stone comes across in hall-wide,
  then close; the giant walks the hall (81-waypoint real walk) and settles at
  the hearth, handing off to the dialogue statue on arrival. The beat's
  begin-stealth is gone: it is pure observation now, and no fail state can
  reach a frozen player.
- **Cast continuity (DW0351 clean)**: Perimedes enters at the party's heel
  (deferred spawn at the mouth, staged walk to the recess by the racks) and
  witnesses the grab he later reports; both companions get staged flee-branch
  exits. Antiphos's dialogue re-voiced to survive the move (fatalist
  arithmetic, no beach-bound lines).
- **Attacking the giant now answers (trigger/his-house)**: sealed-in but not
  yet asleep, a strike draws one backhand — narrate + warden impact +
  damage-players 40 → death → checkpoint. The unwinnable fight is marked by
  being lost, quickly. forbids_flags hands the anchor to wake-the-giant once
  he sleeps.
- Beat gating: obj/take-cover now requires eury-hidden + antiphos-posted
  (walk-arrival flags via on_arrive) — nobody's entrance can lag the camera
  again.
- l10n: 184 zh keys (5 carried moves, 1 dead, 6 new, 6 re-voiced); shot 3
  repositioned once on DW0308 (camera-through-rock is a compile error, used
  as the collision oracle); en double-build byte-identical.

## Round 7 — the blinding beat becomes a fair souls beat (engine PR #157)

The first **honest** run of the validation ladder (after the harness became a
real completion oracle) reached a beat the hollow ladder never could, and the
delve failed it. On a live server the bot completed `obj/grind`, `obj/harden`
and `obj/blind` — then died two seconds later, standing beside the fire-pit, of
a no-attacker death: the `damage-players 40` in the blinding beat's
`begin-stealth` `on_caught`.

Root cause, now measured rather than guessed: `begin-stealth` arms the instant
`obj/blind` completes, with the player standing at the fire-pit — the most
exposed cell in the hall — and the nearest zone (`anchor/ramp-top`) is **56
ticks of sprinting away**. Against a 50-tick grace window, every player, machine
or human, dies there at a fixed moment. Per spec-0016 that is not 初见杀: an
unavoidable death is a broken beat, not a lesson.

The engine now proves this at compile time (`DW0355`, stealth onset
survivability). It fired red on this content and named the deficit exactly:
56 t of flee + 10 t of standing-start reaction = 66 t against `grace_ticks` 50,
short by 16.

**Change**: `grace_ticks` 50 → **90** on the blinding beat. Sized to the proven
requirement, not guessed at: 66 t is the measured sprint-speed need, ~75 t
covers the same route at plain walking pace, and the remainder is tension
margin. 4.5 s to get out of the firelight after you put the stake in his eye —
tense, and beatable by anyone who moves.

**Not changed, deliberately**: the `damage-players 40` consequence. Getting
caught in the open still kills you; that is the beat.

Checkpoint-3 verdict (the death-loop question): its respawn anchor measures
**28 t** of flee time from the same zone, so the retry was survivable even at
grace 50 — but only just, and nothing before `DW0355` could say so. At grace 90
the retry carries ~52 ticks of slack: you come to below the ramp with real time
to choose your moment. The anchor stays where the narration puts it.

## Round 8 — the map editor's first workload: the island's landscape (spec-0017)

The first real use of the stage-7 edit script (`world-edits.json`). Everything
below is edit verbs replayed over the assembled world: no generator code
changed, no prefab was touched, no block was hand-authored. Eight batches, each
snapshot-reviewed before the next was written.

### The finding

Two landscape defects, both inherited from the box-garden's void-safety habit:

1. **The greenfield corridor read as wall-enclosed.** The greenfield prefab
   carries a 3-high berm at its piece edges. Placed twice in series, that put
   continuous walls (top y=65, three above the meadow) down both flanks *and*
   four full-width cross-berms at world z = -1, -15, -16 and -30, each pierced
   only by the 3-wide path notch. The corridor was three walled rooms with
   doorways, not one meadow.
2. **The massif read as a rectangular slab** — vertical faces from the water to
   a flat top, cut off square at the waterline.

### The batches

1. `batch/open-seam-walls` — drop the four cross-berms to the meadow datum, so
   the meadow runs unbroken from the beach to the mountain foot.
2. `batch/west-bank-falls` — invert the west berm from an outward rise into an
   outward fall: rim below the waterline, bank at meadow height, two smoothing
   passes.
3. `batch/east-bank-falls` — the same, mirrored.
4. `batch/bank-outcrops` — seeded stone/andesite/tuff/mossy-cobble speckle down
   both banks, so the fall reads as eroded rock rather than earthworks.
5. `batch/meadow-treeline` — sparse oak clusters on the outboard band where the
   meadow breaks into the bank.
6. `batch/massif-stepped-skirt` — four concentric rings around the west, north
   and east cliff feet and under the two south flanking walls, cresting at
   world y=71/66/63/61, so the cliff steps back on its way down.
7. `batch/massif-crown-crags` — an undulating crest grown above the plateau to
   break the flat skyline; the two daylight shafts are subtracted from the
   region with a one-block pad so the cavern's light wells are never capped.
8. `batch/shore-transition` — sand and gravel tongues with occasional rock
   across the 61-64 band on both greenfield flanks and the mountain's south
   shore.

The path spine is protected structurally rather than by enumeration: each seam
region's y-floor is the walk plane, so the spine columns (top solid 62) have no
cell in the region at all and cannot be touched. `scatter` and `plant`
additionally declare the spine as a keep-clear envelope.

### What the loop rejected

Four designs were tried and thrown away on the evidence of their own snapshots,
which is the point of the loop:

- **A treeline at count 10 / spacing 4** closed the canopy into a leaf tunnel
  over the path — the grass wall traded for a green ceiling. Thinned to
  count 5 / spacing 6 and moved outboard.
- **Crown crags in a five-block band** left detached slabs hanging over the
  crest: the value noise decorrelates across that much vertical distance. The
  band is now two blocks, where a crag cell and the cell beneath it sample
  nearly the same noise.
- **Thin cantilevered ledges on the cliff faces** read as fins stuck to the
  rock, not as weathering — a shelf needs rock under it. Replaced by the
  stepped skirt, which is benching with a foot.
- **A crest running one block proud of the rim**, intended to ragged the
  plateau's plan-view outline, produced overhanging fins for the same reason.
  Reverted: raggeding that outline needs material *removed* at the rim, and the
  plateau is a thin crust over interior voids in places, so removal there is
  unsafe and there is no thickness-aware region selector to make it safe. The
  outline stays straight; recorded as an editor gap.

`DW0313` refused gravel in the skirt recipes and was right to: a cell at the
island's base sits in the ambient water column with no substrate, so a falling
block would have sunk to the seabed and silently deformed the apron. Scree is
rock here.

### The boundary-safety story (engine PRs #159, #161)

The first attempt at any batch at all failed `DW0322` on a cell no edit had
written to — the mountain's south shoreline. The check derived fall-arrest
support solely from the placed-piece occupancy model, but an `ocean`-horizon
world ships a superflat with bedrock, stone and water under every column: there
is no void to fall out of, and stepping off the island is swimming.
Reconstructing the assembled model showed the false positive covered the whole
coast — 182 columns — and that filling a shelf under one exposed cell simply
moved the error to that shelf's own new edge, so no content-side fix could
terminate. Authoring the ocean into the datapack as thousands of water cells
would have been a downstream workaround for a missing world model, so the
finding was escalated instead of coded around.

`DW0322` is now stated against the world-generator ambient: under `ocean` the
rule is the stranding invariant — every body of water a player can enter must
have a climb-out back into the reachable walk region — and violations aggregate
with a total instead of aborting on the first. The de-walled banks satisfy it by
design: the rim sits one block below the waterline, so the bank *is* the
climb-out. Under `void` the original bottomless-column rule is unchanged. A
second engine change lists the placed pieces in the scene manifest, so a batch's
piece-local frames no longer have to be back-solved from anchor positions.

### Proofs

- All eight batches replay green under `delvec edit apply`: trap-hardware
  integrity, gravity settling, relight, critical-path and checkpoint
  walkability, boundary safety and block-support validity re-proved after every
  batch, plus the full build-tier proof set.
- English double build **byte-identical** (ADR-0006).
- Bot playthrough **PASSED, 20/20 critical-path steps**; PackTest **31/31
  required tests passed**. Both under the validation compose profiles with fresh
  named volumes.
- The six seal-cutscene poses were extracted from the built `cs_tick` keyframes
  and re-rendered. All six frame the cavern interior only — no edited cell lies
  in any of them — and the build's own cutscene-clipping check stays green.

Review cameras (spec-0015 shot grammar; reproduce with `delvec snapshot
--camera=`): corridor `10,64.6,-2,180,2` and `10,64.6,-16,180,2`; flanks
`10,64.6,-16,90,5` and `...,270,5`; beach approach `10,64.6,11,180,0`;
exterior `-55,74,-8,225,6`, `10,72,-135,0,4`, `88,72,-51,90,4`, `78,78,8,135,7`;
shoreline `-26,70,-14,250,10`; crown `-30,92,-40,250,14`.

## Round 9 — the beach seam (owner playtest finding)

Owner playtest of the round-8 landscape: the corridor itself is much improved,
but the **beach-greenfield junction still reads as a wall layer**. Standing on
the strand looking north, a continuous grass-topped band sat at eye level across
the full width, pierced only by the 3-wide path notch — the exact defect
round 8 set out to remove, surviving at the one seam that matters most, because
it is the first thing the player walks into.

### Why round 8 missed it

The greenfield prefab edges its pieces in **two rows, not one**. Round 8 cut the
four 65-high cross-berms at world z = -1, -15, -16 and -30. Behind each of those
sits a second, lower lip at prefab-local z=13 — top y=64, two blocks above both
the sand and the meadow — which no cut reached. At the strand that lip covers
ten of the fourteen non-spine columns: a wall with a doorway.

Round 8 also made it slightly worse without noticing. The west/east bank
smoothing passes relax each column toward its cardinal-neighbour mean, and the
already-cut z=14 row had an *un-cut* 64 neighbour at z=13 — so smoothing pulled
z=14 back up to 63-64 at the edges, rebuilding part of the very step that had
just been removed. A lesson worth keeping: **`morph smooth` will restore a
feature you deleted if you leave its neighbour standing.**

### The change (`batch/beach-seam`)

- Drop the local-z=13 lip row to the meadow datum on both greenfield pieces.
- Re-flatten the local-z=14 south edge row that smoothing had raised.
- Finger sand and gravel from the strand into the meadow so the material changes
  over a few blocks instead of at a line.
- **No smoothing pass**, deliberately: with the lip gone the junction is already
  flat at the meadow datum, and smoothing is what re-raised it last time.

The path spine is untouched structurally as before — every morph region's
y-floor is the walk plane, so the spine columns hold no cell in range — and is
declared keep-clear for the scatter on both sides of the seam.

The same prefab row is levelled at the inner piece seam (world z=-17) in the
same batch. It is literally the same lip; cutting only the one the owner stood
in front of would have left its twin standing mid-corridor for the next round to
find.

### Proofs

Nine batches replay green under `delvec edit apply` (full build-tier proof set
after every batch, `DW0322` shoreline re-climbability included), full build
green, English double build byte-identical. The bot ladder was deliberately not
re-run: it is being run once against the combined state after the concurrent
giant-restage and cinematic work lands.

Review cameras (`delvec snapshot --camera=`), beach eye level looking up the
corridor: `10,64.6,12,180,0`, `10,64.6,5,180,0`, `10,64.6,2,180,0`, plus an
oblique `-9,72,9,215,22`.

## Round 10 — the giant answers to being struck (owner round-7 findings 1–3)

Owner round-7 findings, engine first (#179 `DW0359` body-eclipse diagnostic,
#180 `strike-npc` trigger), then this content pass. All three findings shared
one root: **four interaction surfaces and the giant's body stacked on
`anchor/fire-pit`** — the NPC's hitbox (carrying both strike triggers), the
`obj/harden` and `obj/blind` interaction entities, and a 0.9 × 2.9 warden body
in front of all of them. Every click resolved by ray-pick lottery.

### The restage

- **`anchor/fire-side`** (new, island-mountain metadata): the giant's stand,
  3 blocks west of the fire. `npc/polyphemus` moves there; the fire-pit keeps
  the two interact affordances and nothing else. The pre-fix DSL now fails the
  build with `DW0359` — the compiler-level check the owner asked for exists
  and this campaign was its red proof.
- **Strike triggers become `strike-npc`** (v0.6, #180): `trigger/wake-the-giant`
  and `trigger/his-house` name the character, not a cell — no summoned
  interaction entity left to eclipse, and the click rides the giant's own
  hitbox wherever he stands.
- **The wake consequence is a real warden** (owner ruling): striking the
  sleeping giant despawns the NPC and unleashes `actor/polyphemus-roused` — a
  **vanilla-stat** warden, no attribute overrides. The starting kits do not
  beat a warden; the player dies and checkpoint-2's `on_respawn` restores the
  scene (both stand-ins despawned, NPC re-seated, flags untouched — he is
  asleep at his fire again, exactly the pre-strike checkpoint state). The
  first-strike kill is repeatable by construction.
- **Actor roles split**: `polyphemus-walker` (interior duties: blind pacing,
  finale) keeps `anchor/ramp-top`; new `polyphemus-herdsman` (`anchor/meadow`)
  exists only for the seal cinematic's exterior entrance. One actor with two
  spawn sites was the round-6 inside-out bug's enabling condition.

### Cinematic v3 — the herd comes home (finding 3)

Sheep 5–8 spawn at the greenfield **fold**, the herdsman in the meadow; the
flock is walked meadow → mouth → pen through the open boulder while six shots
track them from **outside**: high meadow establish over the fold and ocean,
a dolly along the walkway to the mouth (fire glow visible through it), the
mouth close-up for the Antiphos beat, the seal watched from outside the
boulder (+z is exterior — the round-6 shots' negative offsets were the
"inside-out" the owner saw), then interior: the daylight line dying at the
mouth, and the giant settling at his fire. Every shot was **render-verified
frame-by-frame** this time (`delvec snapshot --camera` at start/mid/end of
each dolly segment, 20 frames reviewed; shot 1 recomposed once — the first
framing was a steep look-down into oak canopy).

### The stealth grace was human-unfair (ladder catch)

Run 1: bot died 4.5 s into the blind-giant stealth leg — `grace_ticks: 90`
covers the fire-to-ramp-top distance at **walking** pace only; the fiction
("do not run") demands sneaking, which needs ~11 s, and no hidden zone lies
on the route. The bot had previously passed this leg walking; a sneaking
human never could have. `grace_ticks` 90 → 260: sneak-completable with
margin, still a death sentence to linger. Content design corrected, no
check weakened.

### Proofs

Build green (DW0359 silent at 2+ blocks), zh-cn build green, double build
byte-identical, PackTest 31/31 (now includes the generated `strike-npc`
separability tests), full bot ladder green after the grace fix.

## Round 11 — the giant enters before the stone, and the blind hunt is real

Owner round-8 findings, in two stages against engine #188–#190 (`DW0410`
timeline gate proof, terrain-shaped path cost, shared-hitbox trigger fix,
burrowing-unleashed-warden fix, sanctioned validation mutex).

### Stage 1 — one hearth, and both strikes answer in kind (findings 1–2)

The hall's one true fire: `obj/harden` moved to the prefab's walled hearth
(new `anchor/hearth`) and dropped its prop campfire — the loose ground fire is
gone; `obj/blind` moved to `anchor/eye` beside the sleeping giant's body.
`trigger/his-house` stopped swatting for 40: striking the **awake** giant now
despawns the NPC and unleashes the vanilla-stat roused warden exactly like the
wake path (owner ruling: both strikes enter combat), the aggro-lock landing on
the striker via #189.

### Stage 2 — seal cinematic v4 (the giant enters BEFORE the stone)

Round 10's cinematic shipped green and was wrong on the live server: the
sequence closed the boulder at `at_ticks: 460` and walked the herdsman across
that region at `700`, so he stepped through solid basalt. `DW0410` now makes
that a build error, and this campaign's own pre-fix DSL is its red proof — the
first build of this round failed on exactly that leg.

The order is now **cross, then seal**. Every gate-crossing walk is provably
arrived long before the stone comes down at `t880`; the flock's second leg is
interior-only and starts at `t1100`. This is deliberate over-provision:
`DW0410` proves walks that *start* after a seal, but a walk still **in flight**
when a later seal crosses its path is a known model gap the compiler cannot
see. The authoring rule that falls out: never leave a gate-crossing walk
unfinished across a `close-gate` — prove the arrival, do not estimate it.

**Arrival math is readable, so read it.** The emitted `ma_tick_<actor>_<dest>`
/ `mv_tick_<npc>_<dest>` functions are per-tick keyframe tables; the terminal
`matches N.. run scoreboard` line is the walk's exact tick count, and the
keyframe coordinates say exactly when a walker crosses the boulder plane.
Three storyboard timings were authored from guesswork and corrected against
those numbers:

- meadow → mouth is **288 ticks**, not the assumed handful. At the planned
  `t200` start the herdsman reached the mouth at `t488` — *after* his own
  `t420` departure for the fire (two walks driving one body at once) and
  *after* the `t380` Antiphos beat that needs him standing there. Start moved
  to `t80`: arrives `t368`, roars inside shot 3, takes Antiphos at `t380`,
  leaves at `t420`, settles at the fire `t521` as shot 5 opens.
- the flock crosses the gap **324 ticks** after setting out. Starting at
  `t0–60` they were through the mouth by `t391` — during shots 2–3, with shot
  4 ("the flock streaming in, daylight behind") playing to an empty gap.
  Starts moved to `t180–240`: crossings land `t504–571`, inside shot 4's
  `t480–620`, and all four are parked by `t775`.

Six shots, all render-verified frame-by-frame (`delvec snapshot --camera` at
start/mid/end of every dolly segment, 18 frames reviewed). New shot 4 is the
reverse angle the sequence never had: interior, near the mouth, looking **out**
through the gap at daylight, sea and the galley's mast, with the flock
silhouetted coming in.

### Stage 2 — the blind giant is a real warden

Owner design: vanilla ancient-city behaviour, not a scripted patrol. `obj/blind`
no longer spawns a walker and marches it to the ramp; it spawns and **unleashes**
`actor/polyphemus-blinded` (vanilla-stat warden, no overrides). Unleashing from
an objective bundle carries no striker, so there is no aggro seed and he starts
calm; #189 seeds `dig_cooldown` so he roams instead of burrowing on sight. If
he does sink into the floor after a long silence, that is the character, not a
defect. `begin-stealth`'s `on_caught` accordingly dropped its `damage-players 40`
— the warden is the killer now; the narrate and the heartbeat stay as the
warning. Checkpoint-3's `on_respawn` restores the roaming threat (despawn,
respawn, re-unleash); checkpoint-2's cleanup list gained him too.

### Stage 2 — the way out

The giant no longer stands *in* the gap he is holding open: `actor/polyphemus-walker`
re-anchors to new `anchor/mouth-side`, beside it, and simply appears there on
the emerge beat (he is never walked again). The flock streams out past him,
four to the fold and four to the meadow, staggered 20 ticks apart. The crew go
out with them — Eurylochus to the gangplank, Perimedes in two hops: a stand
just inside the mouth that *is* the talk window for `obj/hold-fast`, then on
down to the beach once the party reaches him. Both are staged to the pen
(new `anchor/pen-b` / `-c`) when the party climbs there, kept 2+ blocks off
`anchor/pen` so they never shadow `obj/under-ram`'s affordance.

### Two ambiguity findings worth keeping

**`anchor/fold` and `anchor/meadow` are not addressable by `move-npc`.** The
4-piece island layout draws **two** greenfield connectors, and every greenfield
piece defines both anchors — so they resolve to one arbitrary carrier. The
campaign has always lived with that (the sheep spawn there, shot 1 aims there)
because `required_anchors` is built from top-level effects only: actor spawn
anchors and `move-actor` targets never enter it, and `collect_effect_anchors`
does not recurse into `sequence`. A single **top-level** `move-npc` to
`anchor/fold` makes it required and turns the latent ambiguity into a hard
`DW0305`. The rule for this campaign: outdoor destinations for NPCs must be
piece-unique, which on this island means the beach-camp (entry) or the mountain
(terminal) — never a greenfield anchor. Routing around the check by burying the
move inside a `sequence` would have built green and is exactly the wrong fix.

**An unleashed actor is still checked where it spawns.** `DW0359` skips any
body the campaign ever *moves*, but spawn-and-unleash is not a move, so a
roamer is measured standing on its declared anchor forever. Anchoring the blind
warden at `anchor/fire-side` therefore raised a third fire-side/eye advisory
even though he leaves that cell within a tick and `obj/blind` is already
complete when he appears. Followed the diagnostic's own prescription and moved
the spawn mark 2 blocks to `anchor/fire-pit` — same beat (he rises at his own
fire), advisory gone.

### Proofs

Full build green (exit 0) with only the two long-standing fire-side/eye
`DW0359` advisories, `DW0410` clean, zh-cn build green, English double build
byte-identical. Every gate-crossing walk verified arrived before `t880` from
the emitted keyframe tables; all 18 cutscene dolly frames reviewed. The bot +
PackTest ladder ran once the Docker slot freed: bot playthrough GREEN, PackTest GREEN (planner-run, post-delivery).

## Round 12 — the flock stays in its pen, and DESIGN.md becomes authoritative

Owner round-11 verdict: the delve plays well; two items. Owner-requested
changes only this round — nothing else in the campaign was touched.

### The sheep dispersal was an overcorrection (owner finding)

Round 11 read "spread the sheep" as "spread them across the space". It is
"spread them **within the pen**". Two places broke that:

- the herd's entrance walk parked the four incoming sheep on the open cavern
  floor (`checkpoint-3`, `shaft-2`, `checkpoint-2`, `alcove-4` — one of them in
  a stealth alcove) from t≈635 to t1100, then walked them up to the pen in a
  second leg;
- the escape convoy sent four sheep to the fold and four to `anchor/meadow`,
  the middle of the open meadow.

Both are gone. The entrance is now **one leg, fold → pen**, and the escape is
**one leg, pen → fold**. Every sheep, at every moment, stands on a distinct
cell inside one of the two footprints:

- `island-mountain` gains `anchor/pen-e`…`pen-j`, and `anchor/pen-d` moves
  from `(26,13,4)` to `(24,13,7)`. `(26,13,4)` was **on the pen's north fence
  line** — a round-11 slip the block model permits (scripted walks may use
  fence and gate cells) and the eye does not. All eight sheep cells are now
  verified interior air against the prefab NBT (fence rectangle x22–30, z4–9,
  gate at x26; hay at 23,13,5 left clear).
- `island-greenfield` and `-bend` gain `anchor/fold-b`…`fold-h`: the fold's
  3×3 interior (walls x2–6, z5–9, gate gap at x4), minus the hay tuft. The
  four sheep that come home now also **spawn** spread across the fold, so
  cinematic shot 1 establishes a fold with a flock in it rather than a stack.

**Arrival math re-read from the emitted keyframe tables, not estimated**
(round-11 rule: never leave a gate-crossing walk unfinished across a
`close-gate`). fold → pen is 528–575 ticks; starting t180–240 the four cross
the boulder plane at **t490 / t504 / t517 / t564** — still inside shot 4's
t480–620 window, so the reverse-angle "flock streaming in" beat is unchanged —
and are parked in the pen at **t728–815**, all clear of the t880 seal by 65+
ticks. The escape legs are 541–581 ticks from a gate that stays open.

The mouth-side giant stand (`anchor/mouth-side`) was **not** touched: the new
routes cross the mouth exactly where the old ones did, so the wall-clip
question an engine worker is root-causing is untouched by this round.

### DESIGN.md is now the authoritative design record (owner ruling, 2026-08-03)

`DESIGN.md` was written 2026-08-01 and never updated across rounds 3–11. It is
now **v2**, with an iteration protocol at the top: the file is the design,
every round updates it, every round ends with a conformance review, and
owner-unrequested changes are forbidden.

A beat-by-beat conformance audit of the current `quests/dialogue/npcs/
world-edits` JSON against v1 was run to produce it. Deviations traceable to a
numbered owner round were folded into v2 as the new authoritative state:
checkpoints and their `on_respawn` resets, wine issued to the whole party,
cheese as a collect objective, the six-shot cross-then-seal cinematic, both
strikes unleashing a vanilla-stat warden, the walled hearth and `anchor/eye`,
the blind giant as a real roaming warden with `grace_ticks: 260` and no
`damage-players`, the three name-branch neighbour scenes, the mouth-side
stand and the escape choreography, the nine world-edit batches, plain-title
endings, and the deferred-NPC cast.

Seven deviations with **no traceable owner request** were found and left
untouched, recorded in DESIGN.md §7 for the owner to rule on: the collapsed
B1 follow chain (blocked by `DW0305` on the twice-placed greenfield), the
unnamed cheese (the collect verb has no item-name field), the four
already-penned sheep, the boulder hint as a strike rather than an interact,
the full-night cut where the design said dusk, the absent Eurylochus walker
twin, and Antiphos dying in Eurylochus's place.

### The giant was standing inside the mountain (engine PR #196)

Root cause of the owner's "giant in the wall" finding, found by the engine's
new body-clearance proof: `anchor/mouth-side` was prefab-local `[14,9,27]`,
which is **inside the mouth wall**. The mouth is a 3x3 hole (local x16-18)
punched through a solid 3-deep wall spanning z27-29; every cell of that wall
other than the hole is rock, so the round-11 "beside the gap" anchor put a
2.9-block warden inside cobblestone. `DW0450` (body hitbox vs block collision
volumes, at every anchor and every walked waypoint) is an error, so the
campaign at round 11 no longer builds on current main — its own DSL is the
red proof.

The anchor moves to local `[15,9,25]` (world `[7,69,-47]`): inside the hall,
one bay west of the gap's throat, two cells clear of the mouth wall. Chosen by
measurement, not by taste:

- `DW0450` and `DW0451` both silent there — no rock in the hitbox and none
  within the 0.2-block model-overhang margin, so nothing about him reads as
  embedded. The two cells nearer the wall are clear of the hitbox rule but
  trip the overhang advisory, which is what "in the wall" looks like on a
  client.
- `DW0359` silent — the cells beside the gap's inner mouth sit within a block
  of `trigger/boulder-wont-move`'s affordance on the stone and would eat its
  clicks.
- The staging survives: **every one of the twelve sheep walks passes within
  exactly 2.00 blocks of him**, measured from the emitted keyframe tables, so
  the flock still files out under his hands — and he stands beside the 3-wide
  gap, never in it.

The pen and fold work above was re-verified against the same proof: `DW0450`
clean everywhere, and one fold cell had to move because of it (below).

### The sheep fold's west third is buried (finding, not fixed)

`DW0450` refused a sheep spawn inside the fold and named the cell. Probing all
nine interior cells against the assembled world: the fold's **entire west
interior column is solid**. Four round-8/9 landscape batches take piece-local
x 0-3 as "the west bank" — `west-roll` smooths it, `bank-outcrops` and
`shore-transition` scatter rock and sand across it, `meadow-treeline` plants
oaks in it — but the fold rectangle is x 2-6, so local x=3 is inside the
walls. The fold has looked 3x3 and been 2x3 since round 8.

This round does not touch it: it is drift with no owner request behind it, and
the protocol says report rather than restore. The flock is staged in the six
cells that are real, plus the gate cell and the cell at its mouth — eight
distinct positions, all at the fold. Recorded in DESIGN.md section 7 with the
proposed restore.

### Advisories

22 `DW0451` and 2 `DW0359`, and **no class of them is new this round**: three
warden bodies flush at the hearth cells, three sheep flush against fold walls,
and sixteen bodies passing through the upper pen's 1.5-block fence gate — the
gate the flock and the crew have always walked through, which the compiler
counts once per walk. The two `DW0359` are the long-standing fire-side/eye
pair. Not chased, per the round's scope.

### Proofs

Full build green (exit 0) against `delvec` built from engine main at #196;
`DW0450` clean; zh-cn build green; English double build byte-identical;
`DW0410` clean. Every new anchor cell is proven walkable by construction (a
`move-actor` destination that is not routable is `DW0325`), proven body-clear
by `DW0450`, and proven interior to its fence rectangle by direct inspection
of the prefab NBT.

Bot + PackTest ladder GREEN under the isolated `dw-worker-island12` compose
project (no host binding on 25565, torn down with `-p dw-worker-island12` only,
mutex taken and released through `validation/mutex.sh` after waiting out an
owner play session): **PackTest all 31 required tests passed**, **bot critical
path PASSED, 20 steps**.

## Round 13 — the scene ledger, and the last polish before friends see it

Ten owner-ruled items (2026-08-03). Eight landed; two are STOPs with the engine
work they need written down in DESIGN.md §7.

### The headline: every quest now says where its cast is (spec-0020)

`quests.json` moves to `dsl_version` 0.7.0 and carries a `cast` block on all
nine quests: 45 NPC entries, 43 of them per-branch lists. `DW0462` is
campaign-global — the flee/wait fork drives four of the five NPCs through a
flag-gated effect, so *every* quest has to declare both branches, including the
ones before the fork and the ones only one branch can reach. The pattern is
uniform: the wait/pre-fork placement carries `forbids_flags: [flag/flee]` (so it
is also what a pre-fork player lands on) and the flee placement carries
`requires_flags: [flag/flee]`; later clauses override earlier ones, which is
what makes "the latest-begun beat wins" tell the truth on both branches.

The ledger is what retires a tree. `cast_perimedes.mcfunction` is the proof:

```
… qa_cave_of_plenty … unless … f_flee … set @s dw.cast 1   # dlg/just-arrived
… qa_hide          … unless … f_flee … set @s dw.cast 2   # dlg/root (the premise)
… qa_the_stake … if score #party dw.f_blinded matches 1 … set @s dw.cast 3   # dlg/after-the-eye
… qa_under_the_rams … unless … f_flee … set @s dw.cast 4   # dlg/under-the-ram
… qa_the_sail      … unless … f_flee … set @s dw.cast 5   # dlg/on-the-sand
```

"Tell me what he is." stops being offered the instant `flag/blinded` is set —
because the ledger says so, not because an author remembered a flag. Eleven new
dialogue nodes were written for the scenes the ledger points at, including the
two the owner asked for by name: post-escape survivor roots for Perimedes (two
fists of wool, "tell me four is right") and Eurylochus (counting heads, "I will
do my grieving at the oar, like a sailor").

27 bark pools / 69 bark lines cover the beats where a conversation would be
absurd. **Barks print as `<Name>: <line>`**, so a pool is speech, never
narration — which is why the sleeping giant's pool is sleep-talk rather than
observation, and why it sits in the same register as the `missing_item_hint`
item 10 later added. Zero `DW0467`.

### Reading grace (owner ruling: a beat that can fail you must arm after its prompt can be read)

Two beats restaged, both in `sequence` steps:

- **The blinding.** The blinded body spawns inert at t0 and the neighbours
  answer over it; the title, the roar and `unleash-actor` land at t400, and
  `begin-stealth` arms at t460. `DW0355` is deliberately unmoved by this —
  engine #204 states the rule outright ("delaying the arm does not discharge
  it") — and it stays green either way, so the drama is free.
- **The escape.** The owner's complaint was that the flock left before she had
  finished reading. Stone and first narration at t0, the giant taking his place
  beside the gap at t100 with the second half, roar at t160, and the flock only
  begins at t200 (staggered 200/230/260/290).

A third change — delaying the drowned tutorial's `spawn-wave` by 160 ticks —
was made, caught by the bot, and **reverted**: the bot cleared the wave step
before the wave existed, `obj/surf` never completed, and the whole quest chain
stalled at `obj/reach-mouth`. It was also outside the owner's list. The lesson
is the general one: reading grace must never be bought by delaying a hazard past
the point the party can walk away from it.

### Three endings, one per name

`obj/board-nobody` keeps the NOBODY title (it names the ending, not the answer)
and branches its closing paragraph on `flag/name-nobody` / `-boast` / `-lie`,
each paying off its own neighbour scene. zh for all three.

### The fold is a real pen again

Round 12 found the fold's west interior column (piece-local x=3) solid, so a
5×5 pen with a 3×3 interior held six bodies. Four west-region batches were
burying it. The fix splits by verb: the three **seeded** batches
(`bank-outcrops`, `meadow-treeline`, `shore-transition`) gained the fold
rectangle as a keep-clear `avoid` envelope — no rock, sand or oak lands inside
the walls — while `west-bank-falls` reshapes terrain with a `morph`, which
carries no keep-clear, so a new `batch/fold-clear` re-cuts exactly what the
smoothing filled: grass on the fold's west floor row, air in the three cells
above it, nine columns per piece and nothing else. `anchor/fold-g`/`fold-h`
moved from the gate row into the freed column. **All eight sheep now stand on
eight of the fold's nine interior cells** — proven by construction, since a
`move-actor` destination that is not routable is `DW0325` and a body in rock is
`DW0450`.

### Prose

Five English strings rewritten to kill the four negation-pivot constructions
("That isn't an empty house. That's a house someone is coming back to.") and one
observation+verdict fragment pair; in-character speech rhythm was left alone,
because deleting a terrified boy's "It's fine." is not a de-AI pass. Six zh
strings re-perceived rather than transliterated, including the owner's canonical
bad example — "pails still wet" is now "奶桶还带着奶的温度", and the calqued
"这不是那种东西。这是……" in the wine scene became "跟这个不沾边。这是人做梦才梦得着的酒。"

### Two STOPs (see DESIGN.md §7 for the engine asks)

- **The cheese barrel.** `collect` *places its own container* at objective
  activation (`setblock … minecraft:chest` + `item replace … container.0`), so
  aiming it at the prefab's barrel destroys the barrel and the `loot[]` fill,
  and aiming it anywhere else stands a spurious chest next to it. Counting would
  have worked (the guards match on item id, so a renamed stack still counts).
- **The boulder's right-click.** The compiler *accepts* a co-located `use`
  trigger and builds green, then summons a second `minecraft:interaction` at the
  identical cell — the exact ray-pick ambiguity `emit.rs` documents under "one
  cell, one hitbox". One of the two triggers would silently never fire. Reverted
  rather than shipped.

### Two engine defects found by this round's ladder

1. **The bot never held what `requires_item` requires.** Engine #205 made
   `interact.requires_item` mean mainhand-held, but the harness's `interact`
   step only walks and chats the trigger — it never equips the item, though
   `critical-path.json` has carried `requires_item` per step all along and the
   `InteractStep` doc comment already said "must be held". Every campaign with
   an `interact.requires_item` therefore fails its own bot ladder: here
   `obj/grind` timed out with the stake in the pack. Reproduced, fixed in
   `harness/src/executor.ts` (equip `requiresItem` to `hand` before the chat,
   with a diagnostic line), and the ladder went green. **The fix is an engine
   change and is NOT part of this commit** — it is handed to the engine side as
   its own PR.
2. **A stale worker world volume silently poisons a run.** `docker compose -p
   <proj> … down -v` leaves the named `*_server-data` volume behind when an
   exited container of the project still holds it, and the world volume carries
   the scoreboard: `dw.o_muster` already 1 means `dlg_eurylochus_4` runs
   `unless score … o_muster matches 1` and completes nothing, so the bot waits
   30 s for a marker that will never come and reports a content failure. Cost
   three misattributed red runs before an A/B against the untouched round-12
   campaign showed the *baseline* failing identically. `validation/fresh-
   volumes.sh` exists for exactly this but matches `server-data$` daemon-wide
   and force-removes the owner's container names, so a worker must not run it; a
   project-scoped equivalent (down → force-rm the project's containers → rm the
   project's volumes → assert clean) was used instead and should probably be
   what the script offers workers.

### Deferred / not done

Nothing is deferred. Items 6 (dusk) and 10 (held-item + `missing_item_hint`)
were engine-blocked at the start of the round and both landed mid-round (#204,
#205); both are in.

### Advisories

20 `DW0451` (down from 22) and the 2 long-standing `DW0359`. Sixteen of the 20
are one cell — the upper pen's fence gate, which every body entering or leaving
the pen walks through. The rest are documented in DESIGN.md §7.

### Proofs

`delvec` built from engine `main` at #205/#206/#202. English and zh-cn builds
both exit 0; English double build **byte-identical**. Ladder GREEN under the
isolated `dw-worker-island13` compose project with `worker-override.yaml` (no
`container_name`, no host binding on 25565, torn down with `-p
dw-worker-island13` only; mutex taken as `worker-island13` and released by name
through `dw_mutex_release_named`): **PackTest all 34 required tests passed**
(31 → 34: the generated `cast_root_swap` and `cast_bark_cycle` templates now
exist and run on a live server), **bot critical path PASSED, 20 steps**.

## Round 14 — the branch that was never finished, and a way to leave

Eight owner-ruled items after the round-13 playtest. All eight land.

### The big one: the flee branch was half-built (item 2)

Taking the cheese and leaving is a whole ending, and round 13's ledger described
it correctly for Antiphos while the *staging* still belonged to the other branch.
Three separate desyncs, one cause — the fork moved the ledger but never moved the
bodies:

- Perimedes walked to the mouth and `despawn-npc`'d himself. Now he goes down the
  path ahead of everyone to `anchor/class-post` and stays, with `dlg/all-hands`.
- Eurylochus had no flee leg at all, so he held the racks in a cave the party had
  left — the "idle NPC at the cave mouth with no scene". He now walks to
  `anchor/gangplank` and counts the party aboard twice, with `dlg/quiet-sail`.
- Elpenor asked "Where is Antiphos, Captain." on a branch where Antiphos is
  standing next to him. `dlg/the-fire-held` is now wait-branch only; the flee
  branch gets `dlg/all-of-you`, whose joke is that he prepared a eulogy he does
  not get to use.

The audit that matters is which quests *begin* on the flee branch:
`take-the-cheese` and `hide` open together off `cave-of-plenty`, and the later
declaration wins the `dw.cast` selector — so the flee line has to be right in
**hide** too, and in every quest after it, none of which a flee player can ever
finish. `cast_elpenor.mcfunction` now reads flee→3 in every quest from
cave-of-plenty on, and wait→4 only at `the-sail`: the mourning scene is
structurally unreachable on the branch with no death in it.

### The rest

- **One class** (item 1). `class/polites` and `class/eurybates` are gone; the
  Odysseus blurb absorbs what the pick used to say. No combat proof moved —
  neither removed kit held the best hit or the only food.
- **Stair debris** (item 3). Found by diffing the emitted `world_edits`
  setblocks against the mountain prefab's own stair cells: eleven scatter blocks
  standing on the bottom tread row (world y=64, z=−33). `batch/shore-transition`
  now declares the whole switchback face keep-clear. Verified 11 → 0 by the same
  diff.
- **The drowned** (item 4). Two findings. The clock is the root cause and is
  fixed with a `sequence` step to `night` **after** the wave exists. The routed
  lane the round asked for is **not available for this species**: `lane` is
  raider-family only (`DW0382`), and the non-patrol substitute `summon:
  aggro-edge` seats mobs on the standable arc of the perception ring — which,
  for a fire on a beach, is the meadow behind the party. Tried, inspected in the
  emitted summons (`9.5 63 −9.5`, i.e. 18 blocks inland), reverted.
- **Belly-wool step deleted** (item 5): `obj/hold-fast`, its dialogue option and
  the round-13 bridge that existed only to prove it reachable all go; Perimedes
  now leaves with the flock in the same stagger and keeps going to the strand.
- **The giant holds the mouth** (item 6): `flag/escaped` +
  `trigger/he-holds-the-mouth` (approach 5 at `anchor/mouth`, once) unleashes the
  walker actor. Optional combat, so spec-0023's mandatory-encounter proofs do not
  bind it.
- **The voyage** (item 7). A second area, `area/open-sea`, bound to the existing
  `prefab/island-galley`. Four things had to be learned to make it work, all of
  them the compiler telling me:
  1. the plan must **converge on the finale**, so the voyage becomes the finale
     and depends on `quest/the-sail` (`DW0132`);
  2. an inter-area transport is only emitted when consecutive critical
     objectives name **different anchors in different areas** — both galleys had
     `anchor/deck`, so the proof demanded a 250-block walk (`DW0311`);
  3. the transport target is the destination area's `spawn`, and the entry-anchor
     names are **unprefixed** metadata keys (`spawn`, not `anchor/spawn`) —
     `campaign_spawn` scans areas in order, so area 0's `entry` still wins the
     world spawn and this one only ever serves the ending;
  4. the `delve:art` font is ASCII-only (`DW0328`), so the banner is `NOBODY` in
     both languages and the Chinese closing line carries the meaning.

  Framing is proven by construction rather than by distance: the island spans
  x −8…27 and the ending area sits at x=256, so the dolly recedes along −x and
  looks back along +x — the island is 180° off the view axis, behind the camera
  for the whole shot, whatever the client's FOV.

### Proofs

`delvec` built from engine `main` at #208. English and zh-cn both exit 0;
English double build **byte-identical**. Advisories 19 `DW0451` (down from 20 —
Perimedes no longer walks the pen gate twice) and the 2 long-standing `DW0359`.
No `DW047x`: the only mandatory wave is the tutorial, and the giant is optional.

## Round 15 — the button captions, the hover box speaks (DW0331)

Recorded late: round 15 shipped as commit `43e8807` and updated `DESIGN.md` §9
but never wrote its GENERATION entry. The gap is itself a round-16 finding —
the process rule is that every round appends here, and a round that skips it
leaves the next session reconstructing intent from a commit message.

`DW0331` (engine #217) makes a dialogue option label wider than 146 font px a
build error: dialog buttons are a fixed 150 px and anything longer scrolls. This
campaign had 27 over the limit (25 English, plus the 2 Chinese labels that
mirrored the worst two) — the whole option register had been written as full
sentences.

Owner ruling: **the caption goes in the button, the full line rides a `tooltip`**
(engine #233; the `dialogue` stage alone goes to `dsl_version` 0.8.0 — the
narrowest bump that unlocks the field, probed first with a single tooltip to
confirm no `DW048x` cascade). The governing rule is SKILL.md's: the button must
read on its own, because fast and controller players never hover — so a caption
is a speech act, not an abbreviation ("We climb.", "Take it and run.", "You have
my word."), and the sentence it replaces survives verbatim on hover.

Two label sets were treated as sets rather than per-label, because the player
compares them side by side: the three name answers at the wine
(`Nobody.` / `Odysseus.` / `Aithon.`) and the two routes that offer the wine.

The Chinese side needed 25 new captions and **zero** new tooltip translations —
a tooltip's English is its label's own former text, so the sidecar already
carried that sentence. Both languages exit 0; English double build
byte-identical.

## Round 16 — the findings ledger, and pauses stop being punishment

Owner playtest 2026-08-04, four items. Opened with a rebuke that reframes the
whole round: **findings from her first playtest survived into her second** (the
cheese items, open since round 13). The standing rule that falls out, and which
this section exists to serve:

> **No build is staged for the owner until every prior finding is either fixed
> or explicitly deferred by her.** The audit below runs every round, in full,
> from round 1 — not from the last round.

### The findings ledger (audit, all rounds)

Status key: **fixed@N** = landed in round N and still holds on this branch;
**open** = reported and not yet fixed; **engine** = blocked on engine work;
**ruled** = owner closed it without a code change.

| # | Finding | Reported | Status |
|---|---|---|---|
| 1 | zh l10n read as machine translation | r3 | fixed@r3 (rewritten per-persona; re-perceived again r13) |
| 2 | Wine issued per-class → soft-lock | r3 | fixed@r3 (whole party, Q1 end) |
| 3 | Cheese-store crowding (NPCs on the marker) | r3 | fixed@r3 |
| 4 | Live-AI giant self-digs and despawns | r3 | fixed@r3 (#113 deferred NPCs) |
| 5 | Night vision was a renamed water bottle | r3 | fixed@r3 (#114 area declaration) |
| 6 | NPCs clipped into blocks (cell corners) | r3 | fixed@r3 (#115 cell-centred) |
| 7 | Ocean sat below the shoreline | r3 | fixed@r3 (#116 waterline datum, DW0344) |
| 8 | Singleplayer had no entry point at all | r3 | fixed@r3 (#117–#120, DW0345) |
| 9 | Cutscenes could not aim or cut | r4 | fixed@r4 (#124 look_at + multi-shot) |
| 10 | Stealth clock ran during a cutscene | r4 | fixed@r4 (#125 "a cutscene is pure observation") |
| 11 | Strikes did not register on the giant | r4 | fixed@r4 (#128 shared hitbox tagging) |
| 12 | Sheared half-trees in the greenfield | r4 | fixed@r4 (#121 structural regrow) |
| 13 | On-screen text overran its box | r4 | fixed@r4 (#127 DW0330 measured metrics) |
| 14 | Cheese should be taken, not clicked | r4 | fixed@r4 as a `collect` — **but see #33** |
| 15 | Prose was narrated as subtitles | r4 | fixed@r4 (15 demoted subtitle→chat) |
| 16 | Ending banner wanted no pixel art | r4 | fixed@r4 (plain fullscreen titles) |
| 17 | Daylight killed the drowned | r4 | fixed@r5 (#130 wave `equipment`: helmets, not clock) |
| 18 | Giant's dialogue soft-locked | r5 | fixed@r6 (#142 one-cell-one-hitbox, DW0350) |
| 19 | Stealth demanded a crouch | r5 | fixed@r6 (#143 zone presence = hidden) |
| 20 | The giant teleported instead of walking | r5 | fixed@r6 (#144 move-npc on_arrive, DW0351) |
| 21 | The seal beat was over in 7 s | r5 | fixed@r6 (40 s six-shot cinematic) |
| 22 | Clicks at the fire-pit hit the wrong entity | r7 | fixed@r10 (#179/#180 `anchor/fire-side` + `strike-npc`) |
| 23 | Striking the giant did nothing | r7 | fixed@r10 (unleashes a vanilla-stat warden) |
| 24 | The seal cinematic was inside-out | r7 | fixed@r10 (shots re-staged exterior, render-verified) |
| 25 | Greenfield read as three walled rooms | r7 | fixed@r8 (eight world-edit batches) |
| 26 | The massif read as a rectangular slab | r7 | fixed@r8 (stepped skirt + crown crags) |
| 27 | The beach seam was still a wall | r8 | fixed@r9 (`batch/beach-seam`, both lip rows) |
| 28 | Two hearths; strikes answered differently | r8 | fixed@r11 (one `anchor/hearth`, both strikes unleash) |
| 29 | The giant walked through the sealed stone | r8 | fixed@r11 (#188 DW0410; cross-then-seal order) |
| 30 | The blind giant was a scripted patrol | r8 | fixed@r11 (real unleashed warden) |
| 31 | Sheep scattered across the whole cavern | r11 | fixed@r12 (one leg fold→pen; all 8 inside a footprint) |
| 32 | The giant stood inside the mountain wall | r11 | fixed@r12 (#196 DW0450; `anchor/mouth-side` moved) |
| 33 | **Cheese: name it, fill the EXISTING barrel** | **r12** | **engine — open 4 rounds.** `collect` stamps its own chest and has no `name` field. Engine task #95 in flight (`worker/collect-adopt-container`); applies the moment it merges. **This is the finding the round-16 rebuke is about.** |
| 34 | **Boulder hint should answer right-click too** | **r12** | **engine — open 4 rounds.** A co-located `use` trigger builds green and then summons a second `minecraft:interaction` at the identical cell; one of the two triggers silently never fires. Needs the `strike-npc` treatment for non-NPC triggers (merge co-located click triggers onto ONE hitbox carrying both tags) **plus a diagnostic**. Reverted rather than shipped, r13. No engine task is open on it — filed this round. |
| 35 | NPCs offered premise questions after the finale | r12 | fixed@r13 (spec-0020 cast ledger, 45 entries) |
| 36 | Beats armed before their prompt could be read | r12 | fixed@r13 — **then over-corrected; superseded by #45** |
| 37 | One ending for three names | r12 | fixed@r13 (branch closing paragraphs) |
| 38 | The fold's west third was buried | r12 | fixed@r13 (`batch/fold-clear` + keep-clear envelopes) |
| 39 | Prose had AI tells (negation pivots) | r12 | fixed@r13 (5 en rewritten, 6 zh re-perceived) |
| 40 | Dusk read as daylight to the drowned | r12 | fixed@r13/@r14 (#204; `sequence` to night after the wave exists) |
| 41 | `requires_item` did not mean held | r12 | fixed@r13 (#205 + `missing_item_hint`) |
| 42 | Class picks that changed nothing | r13 | fixed@r14 (one class) |
| 43 | The flee branch was half-built | r13 | fixed@r14 — **and introduced #46** |
| 44 | Scatter debris on the switchback treads | r13 | fixed@r14 (keep-clear envelope) + engine #212 (prefab re-export) |
| 45 | Belly-wool step made you double back | r13 | fixed@r14 (`obj/hold-fast` deleted) |
| 46 | The giant should hold the mouth after the escape | r13 | fixed@r14 (`trigger/he-holds-the-mouth`) |
| 47 | The ending should be a voyage, not a fade | r13 | fixed@r14 (`area/open-sea`, two-shot dolly) |
| 48 | Routed lanes for the drowned | r13 | **ruled — not available for this species.** `lane` is raider-family only (`DW0382`); `summon: aggro-edge` seats them inland. Reported r14, no owner objection since. |
| 49 | 27 option labels overran the button | r14 | fixed@r15 (captions in the button, sentences on hover) |
| 50 | **Blind-stealth: ~10 s of forced dead air** | **r15** | **fixed@r16** — this round, below |
| 51 | **Wait branch: Eurylochus vanishes and walks back** | **r15** | **engine — root-caused this round.** `nav.rs` chains walk origins branch-blind. Content cannot express the fix; engine PR open. |
| 52 | **Ending night-vision expires and flickers** | **r15** | **engine — root-caused this round.** The 12 s lease trails the player out of the mitigated area and dies inside the 17 s ending camera. Engine PR open. |

Non-finding deviations still awaiting an owner ruling live in `DESIGN.md` §7 and
are unchanged this round: the single-leg B1 approach (owner-ruled r13: stays),
the four already-penned sheep, Antiphos dying in Eurylochus's place, the
`DW0451`/`DW0359` advisory set, and one surviving bridge option
("About that cheese in your arms.", now a tooltip) that exists because
`compiler::flow` does not seed `DW0203` from cast roots. Its twin
("You have hold of a ram…") went out with `obj/hold-fast` in round 14, so §7's
item 7 is now half-stale and is corrected there.

### Item 1 — a pause is never a punishment (fixed)

Owner ruling, applying **campaign-wide**: a pause inserted so players can read
guidance must be **optional**, and where a pause exists at all it is **3–4
seconds maximum**. The staging is the signal; the gap is not.

The concrete complaint: after the giant visibly stands up blind, ~10 s of dead
air before anything happens — by which time the party is already at the sheep.
Round 13 built that gap deliberately (finding #36, "a beat that can fail you
must arm after its prompt can be read") and sized it by feel at **400 ticks =
20 seconds**. It was an over-correction, and it is now the opposite defect.

Swept every timed gap in the campaign. Five `sequence` blocks, 26 steps. A gap
counts as dead air only where the player holds the camera and nothing is
staged — a gap under a running cutscene is the cinematic, not a pause:

| Beat | Gap | Verdict |
|---|---|---|
| `obj/blind` — blinding → "He Rises Blind" | 400 t = **20 s** | **cut to 80 t (4 s)** |
| `obj/blind` — rise → `begin-stealth` arms | 60 t = 3 s | kept (within the rule; this is the reaction window) |
| `obj/under-ram` — stone opens → giant takes the gap | 100 t = **5 s** | **cut to 80 t (4 s)** |
| `obj/take-cover` — every step t40→t880 | — | under the 860-tick cutscene; not dead air |
| `obj/take-cover` — camera ends t900 → settling echo t1000 | 100 t = 5 s | kept: a deliberate sound beat with no text to read, not a reading pause |
| `obj/aboard` — camera ends t300 → banner t340 | 40 t = 2 s | kept |
| `obj/muster` — muster → `set-time night` | 40 t = 2 s | kept (the round-14 drowned clock, not a pause) |

`grace_ticks: 260` on the blinding stealth is **unchanged** — engine #204 states
that delaying the arm does not discharge `DW0355`, so shrinking the delay cannot
make the beat less survivable, and `DW0355` stays green either way. What the
player loses is 16 seconds of standing still; what the beat keeps is its whole
escape budget.

The **optional** half of the ruling has no vanilla primitive behind it (there is
no dismissible prompt), so it is recorded as an authoring rule in `DESIGN.md`
§10 rather than faked with a longer timer.

### Item 2 — the wait branch (ENGINE, root-caused, not fixable in content)

Reported: after choosing to wait, Eurylochus **disappears**, ~10 s of nothing,
then reappears and walks to the niche. A true regression — this beat passed
earlier rounds.

Root cause, read out of the emitted datapack rather than guessed:
`mv_tick_eurylochus_alcove_1.mcfunction` has **701 waypoints** and its
waypoint[0] is `10.5 63.0 15.5` — **the beach gangplank**, 110 blocks and six
y-levels from where the player is standing. The driver teleports him out of the
cave down to the beach on tick 1, then walks him **35 seconds** back up the
mountain; he re-enters visibility partway up. The owner's description is exact.

`crates/compiler/src/nav.rs::plan_moves` chains each NPC's walk origin linearly
through the flat campaign effect order and never reads the branch gates on the
moves it is chaining:

```
obj/climb-out    → anchor/mouth                            chained := mouth
obj/reach-mouth  → anchor/checkpoint-1   (21 t)            chained := checkpoint-1
obj/the-argument → anchor/gangplank      requires flag/flee  (488 t)  chained := BEACH
q/cave-of-plenty → anchor/alcove-1       requires flag/wait  (701 t)  ← starts at the BEACH
```

The flee-only leg overwrites the origin the wait-only leg inherits. The two can
never both run.

**Second victim, found by this audit and not reported by the owner**:
`mv_tick_perimedes_pen_c` starts at `7.5 63.0 9.5` (`anchor/class-post`, the
beach), poisoned by the flee-only `mv_perimedes_class_post`, and walks **648
ticks = 32 seconds**. Same vanish-and-trudge on the same branch.

**Why r14 caused it**: r14 finding #43 added the flee legs
`eurylochus → gangplank` and `perimedes → class-post`. Before that neither NPC
had a flee move and the linear chain was accidentally correct. Finishing the
flee branch silently broke the wait branch. It is **not** the cast ledger —
`cast.rs` is dialogue dispatch only and emits no `tp` at all ("Declaring an
anchor does not teleport anybody").

**Why content cannot fix it**: the only content lever is declaration order, and
swapping the two legs just moves the teleport onto the flee branch. There is no
DSL surface for "this walk starts where this branch left the body". Escalated
rather than reordered, per the no-hack rule; engine PR carries the fix.

### Item 3 — the ending night-vision flicker (ENGINE)

`area/island` declares `mitigation: "night-vision"`; `area/open-sea` does not.
The clock re-applies a **12-second** lease once a second to everyone inside the
island's box. The ending transports the party to the deck at x=256 — outside
that box — so they arrive holding **at most 12 s** of night vision, against a
**17-second** ending camera (300-tick cutscene + a sequence closing at t340).
Vanilla's `GameRenderer` starts ramping the brightness down at 200 ticks
remaining, so the flicker begins ~1.5 s after arrival and the effect dies
mid-shot. Fixed as an engine guarantee, not as a content timing tweak — see the
engine PR for the chosen mechanism and why.

### Item 4 — cheese (still blocked)

Finding #33, open since round 12. Engine task #95
(`worker/collect-adopt-container`) is in flight; nothing in this campaign can
express it until that lands. Note the current `hint` already promises the barrel
("Take a wheel from the barrel among them") while `collect` stamps its own
chest — so the text is currently ahead of the mechanism, and both land together.

### Proofs

`delvec` built from engine `main` at `5e84c70`. English and zh-cn builds both
exit 0; English **double build byte-identical**. `DW0355` and `DW0410` silent.
Advisory set unchanged from round 14 (19 `DW0451`, 2 long-standing `DW0359`) —
no class of advisory is new. Emitted timings verified in the datapack:
the blinding sequence schedules moved `400t/460t` → `80t/140t` and the escape
sequence's second step `100t` → `80t`, with every other schedule byte-unchanged.

## Round 17 — the prose pass (planner-personal, PR #215 method applied unmerged)

The comparison round: the owner judges the prose-craft method (engine PR #215)
on this campaign's before/after. Method applied from the PR branch verbatim —
§A seven-tell sweep over every player-facing line, §B posture declaration, §C
budgets respected, zh three-step (translate → criticise → revise) by hand.

**Posture note (§B, declared here; the campaign has held it since round 3):**
morality — the antagonist-of-the-plan is right (Eurylochus's caution is
vindicated at the cost of Antiphos); emotion named outright over somatic ("我
发觉我想说了" / "I froze" / "rather be here and afraid"); resolutions close on
a cost, never on acceptance — all three name-endings sting; one deliberately
disproportionate beat (Antiphos taken in a single line, no buildup).

**Coverage:** 60 dialogue texts + 63 narration/hint/goal strings audited in
English; all 348 zh keys audited. English: **2 lines changed**, rest
byte-identical. zh: **6 keys changed**, rest byte-identical. Anti-churn is the
method's own rule: "no change" is an expected verdict, and this campaign had
already absorbed two hand passes (rounds 3, 12) — the sweep mostly CONFIRMED.

Changes, each with its driving rule:
1. en `take-cover` seq 7 narration — de-duplicated the "nine years on the same
   oar" clause that repeated verbatim in Perimedes's root dialogue (§A-4,
   repetition across surfaces); the moment now gets a milking-world simile, the
   dialogue keeps the grief line.
2. en Odysseus-ending — "send you the bill" → "come to collect" (register:
   invoice is post-Homeric; zh already said 收账 and needed no change).
3. zh mirror of (1).
4. zh wake-the-giant trigger — dropped the English "Never do X" skeleton
   (永远不要去打…), now 熟睡的神之子,动他不得 (checklist: imported
   construction).
5. zh shipwrecked goal — un-stacked 冒烟的山下的沙滩上 modifiers (checklist:
   front-loaded modifiers).
6. zh under-ram daylight — replaced the awkward 直挺挺的梁 simile with the
   concrete 直直的一长条,白得晃眼 (§A-2: simile must sharpen the thing).
7. zh board-nobody hint — 水面听得见 → 海在听 (Poseidon is listening; terser
   and truer).
8. zh Elpenor `why` — unified his mother's saying with `told-you`'s rendering
   (海先带走最嫩的那个); the callback only lands if the phrase repeats
   (terminology axis).

**Considered and KEPT, on the method's own "pattern warning, not ban" rule:**
"sword drawn and pointless" (the verdict IS the image); "He did not say he had
stopped" (one deliberate correction-beat); "the wine one dreams about"; all
dialogue-voice repetitions (panic and grief registers, not narrator intensity).

### Round 16 follow-up — the blind beat gets no pause at all

Owner correction on item 1, same day: the round-16 commit read her ruling as a
uniform 3–4 second ceiling and set the blinding beat to 4 s. That was still one
tier too coarse. For this beat she ruled **no pause whatsoever** — 这个地方不要
空场 — because the giant visibly standing up blind *is* the signal. The 3–4 s cap
governs places where a reading pause exists at all; it is a ceiling, never a
target.

- **The blinding beat → zero.** Both sequence steps move to `at_ticks: 0`: the
  title, the roar, `unleash-actor` and `begin-stealth` now fire in the **same
  tick** as the `spawn-actor` that stands him up. There is no engine floor to
  work around — `at_ticks: 0` is a legal step and the compiler *inlines* a
  zero-offset step into the completion function rather than scheduling it, so
  the emitted `complete_o_blind.mcfunction` calls the sequence body directly and
  the whole beat carries **no `schedule` at all**. Verified in the datapack: the
  blinding sequence contributes zero `schedule function … seq_…` lines, where it
  previously contributed two.
- **The escape beat stays at 4 s**, deliberately. Judged by the owner's own rule:
  that gap is a *guidance-reading* pause, not dead air after obvious staging —
  she asked for it by name in round 13 ("the flock left before I had finished
  reading"). It is trimmed to the ceiling (100 t → 80 t) and not below it.

`grace_ticks: 260` untouched; `DW0355` and `DW0410` silent with the arm at t0 —
engine #204's rule (delaying an arm does not discharge the proof) holds in the
other direction too, so removing the delay cannot make the beat less survivable.

## Round 18 — the cheese is the barrel, and every beat says what it does

The repeat finding closes. `obj/cheese` has been a `collect` since round 4, but
the compiler *stamped its own chest* next to the racks, so the objective and the
`hint` ("take a wheel from the barrel among them") disagreed with the room for
four rounds and two playtests. Engine task #95 landed the three fields that fix
it, and this round applies them.

### The cheese (finding #33, open since round 12)

```json
"container": "anchor/cheese-barrel", "item_name": "Kefalotyri Cheese", "fill_count": 26
```

Proof, read out of the datapack: `activate_o_cheese.mcfunction` contains **no
`setblock` at all** and 27 `item replace block 15 69 -47 container.<n>` lines —
slot 0 the wheel the objective wants, slots 1–26 the padding that makes the
barrel read full (vanilla fullness is occupied slots, not stack size). The zh
build carries `custom_name={"text":"克法罗提里干酪"}` in the same position, so
the name translates and the adjudication — which matches on item **id** — does
not notice.

### The anchor route: hand-added, NOT re-exported

`anchor/cheese-barrel` is piece-local `[23,9,25]` in `island-mountain` — one of
four `minecraft:barrel` cells the prefab has carried all along (`[21,9,24]`,
`[21,9,25]`, `[23,9,24]`, `[23,9,25]`), the one diagonally adjacent to the
`anchor/cheese-store` walk cell at `[22,9,26]`.

**Provenance was checked first, and it decided the route.** `island-mountain` is
nominally generator-owned (`island-terrain-generator`), but the generator emits
**17** anchors while the metadata carries **28**. The other eleven — `eye`,
`fire-side`, `hearth`, `mouth-side`, `pen-b`…`pen-j` — are hand-authored, added
across rounds 10–13, and a re-export drops precisely those. That already happened
once and had to be repaired (`830ce14`, "restore the hand-authored mountain
anchors the re-export dropped"). So the anchor was added to the metadata by hand,
the way its eleven neighbours live there, and the edit is proven **add-only** by a
semantic diff rather than by a line diff (the re-serialization reorders keys, so
the line diff is noise):

```
added  : ['anchor/cheese-barrel']
LOST   : []
changed: []
non-anchor sections identical: True
```

The `.nbt` is untouched — no block moved, so no re-export was needed at all.

### 102 happenings (spec-0025)

`quests` and `dialogue` go to `dsl_version` 0.8.0. `DW0481` named all 102 sites
and the round wrote all 102: 97 in `quests.json` (10 quests, 20 objectives, 67
staging/gate/ending effects) and 5 on the story-weight dialogue options — the
flee/wait fork and the three name answers at the wine.

They are authored from the B0–B6 beats in `DESIGN.md` §2, which is what makes
them worth reading; the diagnostic's own warning against placeholders is the
point of the exercise. **Reading the chain back caught four real errors**: `departs`
has to be true *of its subject*, and the party leaving the beach had been written
as `departs(npc/elpenor)` — the one man who stays — while boarding the ship was
`departs(npc/eurylochus)`. Those four now carry no subject at all, because the
beat is about the party and the party is not an NPC. That is the forcing function
working exactly as advertised: the declaration was wrong in a way the prose never
would have shown.

### Athena's gift actually pours now

`classes` to 0.8.0; the Odysseus kit gains `minecraft:potion` with `contents:
{potion: minecraft:long_night_vision}` as **Athena's Gift of Night Vision** /
**雅典娜赐下的夜视之礼**. Round 3 deleted a renamed water bottle that granted
nothing and moved the mitigation to the area declaration (#114) — that
declaration is still the guarantee, together with round 16's camera lease. This
is the fiction's half of it, and unlike its ancestor it is a real potion.

### The chronicle is NOT emitted yet — a declaration gap, stated not hidden

The per-branch chronicle is emitted only for a campaign that declares stage-4
`branch_points`. This campaign's `quest-plan` is still `0.6.0` and declares none,
so the happenings validate and feed nothing yet. Turning it on means bumping
stage 4 and admitting `DW0480`–`DW0485` — including exclusive-content leakage and
event contradiction — on a campaign whose one real fork has a death on only one
side. Those will have findings, and findings there need owner rulings, so it is
queued as its own round rather than rushed in behind the cheese. The wait branch
was instead read end to end by hand against `DESIGN.md` §2 before pushing; it
tracks B0–B6 with no beat missing and no beat out of order.

### Also

`DESIGN.md` §2 B6 was still describing Perimedes leaving "in two hops — a stand
just inside the mouth that is the talk window", which round 14 deleted with
`obj/hold-fast`. Folded in; the file is v7.

### Proofs

`delvec` built from `integration/island-r18` (`origin/main` + #243 + #245 + #244
+ #246). All via the CLI, since in-process build tests do not run the
`compiler::branch` checks: `validate` and `analyze` exit 0; English and zh-cn
builds both exit 0; English **double build byte-identical**; **`DW0331` zero**;
advisories unchanged at 20 `DW0451` + 2 `DW0359`. PackTest run under the isolated
`dw-worker-island18` project. The bot tier is deliberately **not** run: it is red
for harness reasons under task #144, and the final green ladder waits on that.
