# nobodys-cave-island — generation record

- **Date**: 2026-08-01
- **dsl_version**: 0.6.0 (delvec 0.1.0, MC 1.21.11)
- **Author**: planning agent (planner-personal authoring; owner production order
  2026-07-31: "设计要炫技,我没有指定的地方你就把我们支持的特性能加的都加上去")
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
