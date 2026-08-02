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
