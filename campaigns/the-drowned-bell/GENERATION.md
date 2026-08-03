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

## Round 2 — the owner's playtest batch (2026-08-03)

Live playtest findings, worked as one batch. `DESIGN.md` is new this round and
is now the authoritative design of record (owner standing rule, 2026-08-03);
this log stays the history.

### Engine work this round paired with the content

- Engine PR: tidal-keep stair fix + traps-v2/loot anchors. `DW0430` had reported
  132 reversed stair blocks on proven routes ("场景里的楼梯都是反的"). Two
  distinct defects: six wrong `facing` literals (every flight in this tileset
  climbs toward -Z, so every tread is `facing=north`), and one cell that was no
  literal at all — the bell-tower flights rise through open room air, so the loft
  floor sat flush one block under a mid-flight tread and the router side-stepped
  onto it. 177 stair blocks turned, 6 newels added, two pieces byte-identical.
- The same PR wired the first CI coverage the prefab generators have ever had:
  they are separate workspaces outside `crates/`, so nothing in CI compiled or
  ran them, which is exactly how a tileset with 132 backwards stairs shipped
  through a green pipeline.

### Content changes

1. **Portcullis** — 100/100 → **70/30** and `crush: true`. The cycle halves
   and the shut phase drops to a third, which is what "sluggish" meant; being
   caught by the closing edge is now lethal by command. Landed at 70/30 by
   ladder evidence, not by taste — see the ladder log below.
2. **Container loot** — all three reachable barrels filled via stage-5 `loot[]`
   (barrow reward cache, undercroft alcove, drowned side-cell). The compiler
   fills and never places, so the prefabs gained container anchors naming the
   barrel CELL rather than the footing beside it.
3. **Barrow elite** — full netherite, Protection IV throughout, netherite axe
   with Sharpness XII + Knockback I, through actor `equipment`. It reads as the
   armoured thing it always should have been, and the costume survives the
   unleash because equipment is emitted into both puppet and twin.
4. **Cistern enemies** — see `DESIGN.md` *Difficulty* for the full arithmetic.
   Blocked twice at the engine layer and worked around at the content layer:
   `actors[]` has no `attributes`, so the ambush husks can only be tuned through
   `equipment`; and the compiler hardcodes `difficulty=easy`, which halves all
   player damage taken. Netherite axe + Sharpness XIX lands 11.04 on the
   heaviest class kit — two hits, never one. Both engine limits are escalated
   rather than papered over.
5. **Wall zombie** — iron helmet via `equipment`, the sanctioned daylight-undead
   fix. Never `set-time`.
6. **Atmosphere** — `time: night` + `weather: thunder`. `DW0210` immediately
   caught the open-air pieces going dark (the tileset doc had predicted exactly
   this: "braziers and lanterns supplement after dusk"), and it was answered with
   the first mitigation in spec-0010's hierarchy — an area relight fixture
   (`lantern`, `min_light: 4`) — rather than by brightening the scene back, which
   would have undone the request.
7. **Traps v2** — both payloads are command `volley`s now. Placing the two
   firing slots was the round's real geometry work and `DW0442` rejected three
   candidates before accepting: a slot level with the arch rib sees two z of a
   stair before the next riser eats the ray; a slot directly above the rib cannot
   shoot down through its own arch; and the dart dispenser kept as scenery is
   still a solid block that shadowed the whole east column of its kill zone. Each
   rejection is recorded in the generator beside the coordinate it produced.
8. **Prose de-AI pass** — line edit of the English source (owner-diagnosed):
   the negation-pivot tic ("That isn't X. That's Y.") rewritten as direct
   assertion, observation+verdict fragment pairs collapsed into built sentences,
   sensory detail kept but re-phrased as something a person notices. No new story
   content. `zh-cn` re-perceived rather than transliterated for every changed key.
9. **`DESIGN.md`** — created, stamped, and carrying the iteration protocol.

### Ladder (round 2)

Three runs, each red a distinct lesson.

- **Run 1** — PackTest 1/31 failed: `v06_loot` found `container.1` empty at the
  barrow cache. `minecraft:rabbit_stew` has a **max stack size of 1**, so
  `item replace block … container.1 with … 2` is rejected outright and the slot
  stays empty. Two stews are two STACKS, not a count of two. Fixed in the
  content. Worth noting that the build tier passed this: `loot[]` validates item
  ids (`DW0143`) and slot count (`DW0432`) but not `count` against the item's own
  stack limit, and the runtime failure is silent — the same hazard class
  `DW0431` exists for. A build-tier check would move this one tier earlier.
  Bot also red: crushed at the portcullis.
- **Run 2** — PackTest **31/31 green** (incl. `v06_loot`, `v06_volley`,
  `v06_actor_equipment`, `souls_timed_gate_crush`). Bot still died at exactly
  the same cell, `[24, 63, -10]`, despite the window widening from 50 to 70
  ticks — which is what ruled out "the window is too tight" and pointed at the
  gate itself.
- **Run 3 (isolation, `crush` off)** — PackTest 30/30 green, **bot 21/21,
  exit 0**, campaign completed end to end. Everything else in round 2 is
  ladder-green: the night/thunder relight, both command volleys, the loot fills,
  the elite's and ambushers' equipment, and the 70/30 gate.

**Open blocker (engine, escalated).** `crush: true` is currently unpassable by
the bot, and it is not a content defect. `compiler::waypoints::gate_mouth_cells`
deliberately force-keeps three cells for a clocked crossing — the cell before the
gate, **the cell inside the gate region**, and the cell after — so that "the hop
that actually crosses a clocked span is SHORT". The harness turns every waypoint
into a pathfinder goal it navigates to and arrives at (`walkGoals`), so the bot
parks under the portcullis and is killed on the next closing tick. The waypoint
predates this round (round 1's artifact has the same cell) and was harmless while
a shut gate merely blocked. Two legs are affected — the outbound crossing and the
return to the Ferrywoman.

The fix belongs in the exporter, not the content: keep the two MOUTH cells and
drop the in-region ones, so the crossing is a single short hop between the
footings either side. That is already the span `DW0378` charges the crossing
over, so the proof and the artifact would finally agree. The campaign keeps
`crush: true` — the owner asked for it, and weakening it to buy a green bot would
hide the defect.

**Also observed (harness, minor):** on the return leg the bot ate rotten flesh at
7.3 health and poisoned itself down to 3.4. It finished anyway, but the eat
heuristic has no notion of a food that hurts.

### Run 4 — final ladder on merged main (engine #198 merged as a2e23c9)

Rebuilt with `delvec 0.1.0, dsl 0.7.0` from main and re-run.

- **PackTest 31/31 green**, including `souls_timed_gate_crush`, `v06_loot`,
  `v06_volley` and `v06_actor_equipment`.
- **Bot red at step 16** (`kill` the Bellkeeper): it reached the boss, killed it,
  and then **withered away** at `[102, 94, -101]` — the vanilla Wither the boss
  applies on hit finished a player that arrived already worn down.
- The crushing portcullis was **passed** on this run, having killed the bot on
  run 2 at the same cell. So `crush` + the in-region waypoint is *flaky*, not
  deterministic: the bot sometimes clears the gate before the clock shuts it.
  That makes the engine defect worse rather than better — an intermittent
  scripted death is harder to attribute than a reliable one. The exporter fix
  (drop the in-region cells from `gate_mouth_cells`) still stands.

**Reading of the boss death.** This is a genuine round-2 difficulty regression,
not a flake: the bot is the solo-player floor, and it now arrives at the tower
with far less health than it used to. Round 2 raised damage everywhere at once —
the Sharpness XIX cistern ambushers, the volleys, a lethal gate — and the
Bellkeeper's Wither is what collects the debt. Deliberately NOT tuned down in
this round: the owner asked for lethality and the correct next move is one
evidence-led adjustment (most likely the cistern axes, which are the largest
single jump), taken with the owner's difficulty intent in hand rather than
guessed at by a worker.

### Carried into round 3

- The `gate_mouth_cells` waypoint fix (engine), which unblocks `crush`.
- `DW0465`: the campaign is `dsl_version 0.6.0` with no `cast` ledger and is now
  inside the one-version deprecation window for spec-0020. Add a `cast` block per
  quest and raise to 0.7.0.
- A build-tier check that a `loot` stack's `count` fits the item's max stack size.
- Boss-fight survivability after the round-2 damage rise.
