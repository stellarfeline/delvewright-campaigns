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
