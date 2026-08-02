# The Drowned Bell — generation log

Planner-authored souls campaign (M4 acceptance). Design brief: five-level
tidal keep, two loops (chapel shortcut + bell-rope hub fold), 初见杀 without
telegraphs, sightline-budgeted ambushes, optional dormant-leash elite,
timed portcullis, disable-able dart gallery, TD siege with an AND-join.
Authored against docs/notes/souls-design-language.md and the four owner
rulings recorded in spec-0016.

## Round 1 (2026-08-02)

- Stages 1–6 + zh-CN sidecar (107 keys, hand-written) + composed skins
  (ferrywoman/sexton, delve-skin, original, deterministic).
- Tileset: pool/tidal-keep (engine PR #168), six pieces, seed 17.
- `delvec validate` CLEAN after the schema round-trip (finale, radius,
  quest triggers, main_hand, l10n envelope, ASCII art titles per DW0328).
- `delvec build` currently RED on DW0210 at the gatehouse plate cell —
  the known light-model gap (trap triggers measured opaque; engine fix in
  review). No mitigation declared on purpose: the keep is lit, the
  measurement is wrong, and the fix belongs in the engine.
- Siege waves are plain waves this round; upgrade to TD raider lanes
  (`wave.lane`) when the primitive lands, before the delivery PR is final.
- Known deferred: elite dormancy staged via small follow_range leash
  (wave) rather than a posed actor — revisit if the campaign needs the
  Heide-Knight hunch visual; finite bonfire-refilled heals await the
  spec-0016 amendment batch (kits carry fixed stews meanwhile).

## Round 2 (2026-08-02, same session)

- Engine #169 merged: siege upgraded to real TD lanes (gate + wall columns)
  plus `summon: aggro-edge` grave echoes — three-arm AND-join.
- Engine #170/#171 merged: the light-model fix landed (nav-passable blocks
  now transparent per vanilla filterLight) and shortcut gates are proven
  exempt from the DW0306 piece-split by construction.
- DW0386 caught a real lane defect: the wall lane's last leg measured
  exactly 10.0 blocks — inside vanilla's patrol-target re-roll radius, the
  "working-but-drunk" failure. Dropped the final waypoint rather than
  nudging thresholds.
- `delvec build` GREEN end-to-end: critical path across all six pieces,
  bonfires standable + no stranding, shortcut long-route/leak/permanence,
  timed-gate window, three ambush counterplay proofs, both traps avoidable
  + dart gallery disarmable, lane geometry, aggro-edge ring, ocean
  boundary re-climbability, lighting, gravity.
- Determinism: double build byte-identical. zh-CN build green.

## Round 3 (2026-08-02) — first honest-ladder findings

- Ladder run 1: bot slain at step 3 by the live-wave Barrow Warden — the
  DW0380 bypass proof guarantees a route exists, but the exported critical
  path walks the desire line and vanilla wander drifts a live mob onto it.
  Root fix is the design the dossier wanted all along: the elite is now a
  DORMANT NoAI actor kneeling among the barrows, unleashed into its real
  twin only by a player strike (Heide-Knight dormancy = the legibility
  signal AND the determinism guarantee). Unprovoked, it never moves.
- Ladder run 2: bot passes the barrow field, fails at the portcullis —
  mineflayer aborts when the timed gate closes mid-approach. The runtime
  rung lacks the "timing" verb; engine/harness fix dispatched (timed-gate
  export + bounded window-wait on marked legs only). Content unchanged.

## Round 4 (2026-08-02) — siege tuning by ladder evidence

- Runs 3–5 all died at the courtyard siege; the ladder narrowed the cause
  in three steps: 9 concurrent hostiles + crossbows (run 3) → 4 melee
  still fatal (run 4) → run 5's log showed the third assailant was the
  WALL-WALK AMBUSH HUSK, legitimately bypassed earlier and stalking the
  bot ever since. Souls-correct behavior (the world is persistent), but
  it exposed the bot's last capability gap: it only fights the tracked
  wave and never defends itself against untracked attackers, and never
  eats its kit food. Harness fix dispatched (retaliation + fight-or-
  flight + eating — generic capabilities, no campaign knowledge).
- Content retuned meanwhile: siege is now three sequential phases
  (gate 2 vindicators → wall 2 → grave echoes 2, melee-only, hp 10,
  dmg 4) — peak simultaneous pressure 2 plus at most one stalker. The
  division-of-labor proof for parties lives in spec-0018's n-dummy
  PackTests, not this beat; min_players 1 makes the solo floor the
  binding constraint, and the bot is that floor's oracle.

## Rounds 5–13 (2026-08-02) — the convergence ladder

Thirteen full-server bot runs, each red a distinct lesson, none wasted:

- Run 5–7: siege sequenced into three phases; the stalking wall-walk
  ambusher became a ZOMBIE (the open-sky parapet's daylight scours a
  bypassed ambusher — vanilla-native persistence discipline).
- Run 6–8: class kits gained armor (a warden without a cuirass was the
  actual defect — vindicator axe item-modifiers add +8 on top of authored
  attack_damage); siege squads retuned hollow-frail (the wardens are 空壳
  in the fiction and in the arithmetic).
- Run 8–9, 11–12: Bellkeeper walked down to the bot floor (30 hp / dmg 1 /
  speed .23); rafters twist trimmed to two perched husks (visibility is
  the design, not quantity).
- Run 10/12/13 vs 11: the aggro-edge coin flip — mobs seated exactly AT
  follow_range acquire a defender only marginally. Engine fix #174 moved
  the summon band one block inside perception.
- Run 13: the last deadlock — self-defense kills of WAVE mobs were
  deliberately uncounted by #173's guard; harness fix #175 credits
  proximity-confirmed kills during the whole kill step and adds a
  live-mob terminal condition.

## FINAL (2026-08-02): honest ladder GREEN

- Bot: 21/21 steps, exit 0, both on this campaign and the island
  regression (20/20). Every combat number in this file currently sits at
  the BOT FLOOR — the intended human difficulty pass is the owner's
  domain-expert call, one line per wave, and harness task #85 (shield/
  strafe/kite) raises the floor for every future campaign.
