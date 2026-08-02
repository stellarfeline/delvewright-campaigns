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
  NPC's own); every right-click resolved to the wrong entity. Her left-click
  was a red herring. One-cell-one-hitbox rule + DW0350.
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
