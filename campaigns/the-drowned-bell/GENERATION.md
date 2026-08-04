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

## Round 3 (2026-08-03) — real difficulty, and the first live spec-0023 ladder

Engine merges consumed: #204 (gate flanking pair), #206 (`world.difficulty`,
actor `attributes`), #208 (spec-0023 combat verification).

1. **`difficulty: "normal"` declared.** The retune it forced was one encounter,
   not a sweep — attacker-less `/damage` does not scale with difficulty, so every
   trap/gate/scripted number was already true; only mob melee changes. The
   cistern wardens' Sharpness XIX existed purely to buy back the Easy halving and
   would have become a 20.6-damage one-shot at `normal`; dropped, the plain
   netherite axe restores exactly the intended 11.04 two-hit kill. Full arithmetic
   in DESIGN.md. `DW0470`–`DW0475` all pass. The optional Barrow Warden was NOT
   softened (~18.25/hit, one short of a one-shot).
2. **Wave tiers — DEFERRED with the cast ledger, because they are the same task.**
   `waves[].tier` is DSL v0.7 (`DW0141` below it), and v0.7 makes the cast ledger
   mandatory: bumping the campaign fired **21 × `DW0460`** (3 NPCs × 7 quests).
   The whole benefit here is a single label — only `wave/bellkeeper` is non-
   ordinary; the campaign's other elite is the Barrow Warden, which is an
   `actor`, not a wave, and cannot carry a tier at all. See item 5.
3. **`crush: true` gate fix verified.** Both crossing legs now emit only the
   flanking pair `[24, 63, -9]` / `[24, 63, -11]` and nothing inside the region.
   Statically confirmed against the round-2 artifact, which had `[24, 63, -10]`.
4. **Ladder — PackTest 32/32 green** (up one: the new `declared_difficulty` test
   asserts the live world really is `normal`). Bot tier re-run after engine #209
   fixed the ops seeding; see "Runtime leg" below.
5. **Cast ledger — deferred to round 4, as more than a mechanical migration.**
   21 entries each needing an authored `doing` (the spec's own forcing function —
   free prose stating each character's business in that beat) and a per-quest
   `dialogue` root decision; plus `npc/barrow-warden` is branch-divergent (the
   strike trigger despawns it) so `DW0462` wants per-branch casts, and the trigger
   currently sets no flag to gate them on — a new flag and a lifecycle model, not
   a migration. It also lands on prose the owner hand-corrected last round, so it
   deserves its own pass.

### Blocker: the opped-bot wiring cannot start the server

`validation/compose.yaml` sets `OPS: ${DELVEWRIGHT_BOT_USERNAME:-delve-bot}` so
the harness can run its assist and scripted-death commands. The itzg image
resolves `OPS` names through Mojang's PlayerDB, and `delve-bot` is not a real
account, so the server aborts at init:

```
ERROR : Invalid parameter provided for 'manage-users' command:
        Could not resolve user from Playerdb: delve-bot
dependency failed to start: container dw-worker-bellr3-server-1 exited (2)
```

`ONLINE_MODE: FALSE` is already set; the lookup happens anyway. This blocks the
whole bot tier — die-retry, assist windows and the floor gate are all unexercised,
so none of round 3's runtime questions are answered yet. There is no env-only
workaround from a caller: `DELVEWRIGHT_BOT_USERNAME` feeds both `OPS` and the
bot's login name, so setting it to a resolvable value renames the bot. The fix
belongs in the compose file — give `OPS` the offline UUID (deterministic:
UUID v3 of `MD5("OfflinePlayer:<name>")`), or seed an `ops.json` directly, so an
offline-mode name never goes to PlayerDB.

`validation/fresh-volumes.sh --project dw-worker-bellr3` was exercised and is
correct: with the project already torn down it reported
`project 'dw-worker-bellr3' verified clean (containers + volumes)` and exited 0.


### Runtime leg (after engine #209)

The ops fix works: the entrypoint seeds `/data/ops.json` locally —
`Seeded offline op delve-bot (b159a31e-861c-3453-b687-97f9ddb13d37)` — with no
PlayerDB call, and the server boots.

`run-report.json` (v1, difficulty `normal`, 4 mandatory encounters, die-retry ON):

| stage | ran | passed |
| --- | --- | --- |
| critical-path | yes | **no** — `step 11 (kill) failed: bot died at [13, 71, -85], delve-bot died because of Hollow Gate-Warder` |
| die-retry | yes | yes |

`assist_windows: []`, `die_retry: []`, `floor_findings: []`.

**The finding: at `normal` the bot floor cannot clear the first siege phase.**
`wave/gate-assault` is two vindicators landing 7.74 per hit on the 8-armour
Warden kit, against 4.35 at `easy` — the doubling the difficulty declaration
buys. The bot reached step 11, took its scripted die-retry death, respawned, and
then lost the real fight. Nothing past step 11 was exercised, so the Bellkeeper,
the assist windows and the floor gate remain unexercised.

**Not retuned this round** — that call goes through the coordinator. Worth noting
the shape of the choice: the gate squad is `max_health 6`, `attack_damage 1.0`
plus a stone axe's +8, and it is the axe rather than the authored attribute that
carries almost all of that damage.

Two wiring observations from the first live die-retry exercise:

- `DELVEWRIGHT_RUN_TIMEOUT_MS` is **not** in the bot service's `environment:`
  block in `validation/compose.yaml`, so a caller cannot raise the run budget
  from outside; the run took the 20-minute default despite being asked for more.
  Die-retry adds two scripted deaths per encounter, so the knob the stage most
  needs is the one that is not plumbed.
- The die-retry stage reported `passed: true` with an **empty** `die_retry`
  array, although the log shows
  `[die-retry] wave/gate-assault death 1/2 (first-contact)`. A stage that
  recorded nothing reading as passed is worth a look before the artifact is
  trusted as evidence.

`validation/fresh-volumes.sh --project dw-worker-bellr3` again reported
`verified clean (containers + volumes)` and exited 0.

### Queued for round 4 — DW0331 dialogue-label overflow

Engine main (post 2026-08-03 09:44Z) makes a dialogue option label wider than
**146 font px** a build ERROR: the dialog buttons are a fixed 150 px and longer
labels scroll (owner directive). The bell has **five violating ENGLISH labels**;
the `zh-cn` sidecar is entirely clean, and its translations are the target
register — captions, not sentences.

| key | px |
| --- | --- |
| `dlg.ferrywoman.fw-root.opt.1` | 204 |
| `dlg.ferrywoman.fw-root.opt.2` | 180 |
| `dlg.sexton.sx-root.opt.0` | 184 |
| `dlg.sexton.sx-root.opt.1` | 188 |
| `dlg.sexton.sx-root.opt.3` | 164 |

Budget is roughly **≤20 Latin characters**. Keep the meaning, cut to a label —
these are buttons, not lines of dialogue. Do this when round 4 updates its engine
tree, and fold it into round 4's commit. Note it interacts with round 2's
de-AI prose pass: these five strings were hand-edited then, so shorten them
without re-introducing the fragment/verdict rhythm that pass removed.

### Round-3 bot re-run (engine #209/#212/#213) — the fight is fine, the respawn is not

Previous verdict withdrawn: #213 confirmed the "died to a Hollow Gate-Warder"
failure was the harness misreporting its own scripted `/damage`. With that fixed:

**The gate siege IS winnable at `normal`.** Both die-retry trials record
`re_engaged: true`, `objectives_intact: true`, `completed: true`. The retuned
numbers are not the problem.

**The problem is where dying puts you.** Both trials report
`at_checkpoint: false`, respawning at `[24, 63, 31]` — the campaign's world
spawn on the barrow shore — when the encounter's governing checkpoint is
`[34, 71, -113]` at the chapel. The stage's own words: *"Dying must always be
safe — an unpredictable respawn point is the one thing a souls delve cannot
ship."* The critical path then failed downstream for exactly that reason:
`reaching wave/gate-assault: timed out after 60000ms; bot at [5.4, 63.0, 29.5]`
— five levels away, with a 60 s leg budget.

Likely cause, for whoever picks this up: this campaign's checkpoints are
**bonfires**, and a bonfire only sets the spawn point when a player *rests* at it
(`bonfire_rest_<i>`, a right-click). The bot log shows no rest at any of BF1–BF3,
so no checkpoint was ever armed and the spawn point stayed at world spawn. That
makes it a question about the harness's obligations, not obviously a content
defect — but it is a real "souls delve cannot ship this" finding either way.

Also from the report: one assist window fired (gate assault, amplifier 2,
**1200 ticks**, `reason: "policy: ordinary encounter"`, `phase_reached:
"assisted"`); the other three encounters are `not-reached`, so the Bellkeeper and
its wither remain unproven for a third round. `floor_findings: []` — and note the
inverted floor gate structurally *cannot* see this campaign's elite: the Barrow
Warden is an `actor`, and only waves carry a `tier`.

No #214 lucky-red signature — `re_engaged` was true both times.

### r4-prep bot run (engine #220/#221/#222) — checkpoints fixed, return leg is not

**Round 3's respawn finding is RESOLVED.** The bot now rests (`[rest] bonfire 0`,
`bonfire 1`, two `Triggered [dw.rest]` on the server) and both die-retry deaths
report `respawn_pos: [34, 71, -113]`, **`at_checkpoint: true`** — the chapel,
the checkpoint governing that encounter. Dying is safe now.

**The new blocker is the way back.** Both trials:

> `wave/gate-assault death 1 (first-contact): the route from the respawn back to
> the encounter is not walkable. The retry loop is broken: the party can die but
> not try again.`

`returned: false` on both, and the critical path failed the same way —
`step 13 (kill) failed: reaching wave/gate-assault: timed out after 60000ms;
bot at [2.5, 63.0, 33.5]`. That position is the **barrow shore**, five levels
below the chapel it respawned at, so between respawning correctly and the return
timing out the bot ended up back at the start. Both trials still recorded
`re_engaged: true, completed: true`, so the fight itself remains winnable at
`normal` — this is a navigation/return failure, not a tuning one.

Worth a look from whoever picks it up: the governing checkpoint resolves to
`[34, 71, -113]`, which is the **Sexton's cell by the altar**, not
`anchor/l2-bonfire` itself. A checkpoint inside the chapel may be what makes the
route back to the gate lane unwalkable to the stage's model.

Everything else this run:

- Assist: one window, `obj/hold-the-gate`, amplifier 2, **1200 ticks**,
  `reason: "policy: ordinary encounter"`, `phase_reached: "assisted"`.
- `wall-assault`, `grave-echoes`, `bellkeeper` — all `not-reached`. **The
  Bellkeeper and its wither are unproven for a fourth round.**
- `floor_findings: []`, and no floor-gate coverage ledger key in the report. The
  Barrow Warden still carries no tier: `actors[].tier` is 0.8.0 on the quests
  stage, and bumping that stage would drag it through 0.7.0's 21 mandatory cast
  entries, so it was left alone per instruction. DW0477 did not fire.
- Not the #214 lucky-red signature — `re_engaged` was true both times.

### Run five (engine #223/#224/#225) — unchanged red, and the signature is a contradiction

PackTest **33/33 green**. Bot red with the SAME signature as r4-prep; #223 did not
move it.

Correcting my r4-prep speculation: the checkpoint is NOT the Sexton's cell. The
report's new `rests` ledger shows bonfire 1 = `anchor/l2-bonfire` at
`[34, 71, -113]`, armed at **step 8**; the gate siege is **step 13**. So #223's
`fire_step < i` rule is satisfied and the stage agrees — both deaths record
`respawn_pos: [34, 71, -113]`, `at_checkpoint: true`.

**The contradiction is between that record and where the bot actually is.** Both
trials then report `returned: false` — *"the route from the respawn back to the
encounter is not walkable"* — and the critical path fails with:

> `step 13 (kill) failed: reaching wave/gate-assault: timed out after 60000ms;
> bot at [4.5, 63.0, 30.5]`

`[4.5, 63.0, 30.5]` is the **barrow shore**, ~150 blocks and 8 levels below the
chapel the report says it respawned at. So the recorded respawn and the bot's
real position disagree: either the record is what the stage *expects* rather than
what vanilla did, or something returns the bot to world spawn after it. A route
from the chapel bonfire to the gate lane — both in the courtyard, a few blocks
apart — being "not walkable" is only explicable if the bot never started there.

Reported and stopped, per instruction; not iterated on.

Other answers from this run:

- **Bellkeeper + wither: still unreached** (`phase_reached: "not-reached"`), a
  fifth round without an answer. `wall-assault` and `grave-echoes` likewise.
- **Assist**: one window, `obj/hold-the-gate`, amplifier 2, **1200 ticks**,
  `reason: "policy: ordinary encounter"`.
- **Floor-gate ledger now prints but is empty**: `floor_gate: {present: true,
  covered: [], not_covered: []}` and `actors: []`. The Barrow Warden does **not**
  appear as `not_covered` with a reason, which is what #225 was expected to show.
- Both trials still `re_engaged: true, completed: true` — the gate siege remains
  winnable at `normal`. Not the #214 lucky-red signature.

### Run six (engine #227) — the warp is gone; the bot now loses the fight where it stands

PackTest **33/33**. Bot red, but with a **genuinely new** signature — the first
one in four runs that is about the delve rather than the harness:

> `step 13 (kill) failed: bot died at [13, 71, -89] — likely cause: delve-bot was
> slain by Hollow Gate-Warder`

`[13, 71, -89]` is the **gate lane in the courtyard**, three blocks from the wave
anchor `[12, 71, -85]`. Every previous run failed with the bot stranded on the
barrow shore at y=63. So `#227` closed it: the return leg from `anchor/l2-bonfire`
IS walkable, the bot gets back to the siege, and it fights there. My chapel
respawn measurements were truthful, as diagnosed.

**What is now unproven, and why.** `phase_reached: "die-retry"` for the gate
assault — further than any previous run — but:

> `wave/gate-assault: the die-retry stage ENGAGED this encounter but proved only
> 0/2 scripted death(s) (0 recorded). "Dying is always safe" is unproven here.`

The bot lost the real fight before the stage could script its deaths, so
`die_retry: []`, `assist_windows: []`, and the remaining three encounters are
`not-reached` again. The Bellkeeper and its wither are unanswered for a **sixth**
round, and `kit_kept` never got a value because no trial ran.

This is the first evidence that the gate assault is hard for the bot floor **in
its own right** at `normal`, with no harness artifact in the way — note it is
also the first run with **no assist window at all**, where runs four and five
each opened one (amplifier 2, 1200 t). Not tuned, per instruction; the numbers
and the decision are in DESIGN.md and belong to the owner.

Unchanged and still worth a look: `floor_gate: {present: true, covered: [],
not_covered: []}` with `actors: []` — the Barrow Warden still does not appear.
`rests` confirms both bonfires armed (BF1 step 2, BF2 step 8) before the step-13
siege.

### Run seven (engine #228) — three encounters cleared, and a real wave defect surfaces

PackTest **33/33**. The die-retry stage finally ran end to end on three of four
encounters, and every mechanic it exercises reported clean:

| wave | trials | at_checkpoint | returned | re_engaged | kit_kept | completed |
| --- | --- | --- | --- | --- | --- | --- |
| gate-assault | 2/2 | true | **true** | true | **true** | true |
| wall-assault | 2/2 | true | **true** | true | **true** | true |
| grave-echoes | 2/2 | true | **true** | true | **true** | true |

All six respawns at `[34, 71, -113]` (BF2). `phase_reached: "cleared"` on all
three, 5 assist windows each. **`returned` and `kit_kept` are true for the first
time** — #227 and #228 between them closed the walk-back and the bare-approach
death. Assist ledger, 15 windows, all named as designed: 6 × *walk back and
re-engage probe*, 3 × *approach into melee range*, 3 × *trading blows before the
scripted death*, 3 × *policy: ordinary encounter*.

**The new red is a content/engine defect the stage caught, not a tuning problem.**
Four separate findings, one class:

> `wave/gate-assault death 1 (first-contact): 2 of the 4 wave mob(s) standing
> after the re-seat are entities the bot already fought in a previous life. A
> `respawns_on_rest` wave must be REMOVED and re-summoned whole, never topped up
> around its survivors — otherwise the party grinds it down one swing per death.`

Both `respawns_on_rest` waves are affected — gate-assault (declares 2, **4**
standing) and wall-assault (declares 1, **4** then **6** standing). The wave
accumulates across deaths instead of being re-summoned whole.

That also explains the run's terminal failure, which is downstream of it:

> `step 16 (reach) failed: bot died at [34, 71, -102] — likely cause: delve-bot
> was slain by Hollow Gate-Warder`

`[34, 71, -102]` is beside the chapel, on a **reach** step — the bot was walking,
not fighting, and was killed by accumulated Gate-Warders that should never have
been standing. **The Bellkeeper remains unreached for a seventh round**, and it
will stay unreachable until the re-seat defect is fixed: the siege leaves
survivors that follow the party.

No `ASSIST_SECONDS` lapse signature seen — the deaths were not late in a return
leg; all six returns succeeded.

`floor_gate: {present: true, covered: [], not_covered: []}`, `actors: []` — the
Barrow Warden still absent, seventh run running.

## Round 4a (2026-08-03) — the two bonfires leave the aggro

Deliberately small round: one defect class (`DW0478`, task #132) and a full
ladder re-run on merged engine main. No cast ledger, no wave tiers, no version
bump — those are owner-sequenced. The two owner-deferred tuning beats were not
touched.

### What moved, and why it had to

`DW0478` (engine #238's lane term included) rejected **both** rest points. Under
the owner's 2026-08-04 drift ruling a marching squad is a corridor around its
polyline, not the polyline, so a lane's reach is `aggro_radius + 7.9`.

| fire | anchor before | nearest hostile cell | dist before | required reach | anchor after | dist after | margin |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BF1 barrow fire | `[19, 63, 29]` | `actor/barrow-warden` staging anchor `[23, 63, 16]` | **13.6** | 16.0 (`follow_range` default, stationary cell) | `[10, 63, 31]` | **19.85** | +3.85 |
| BF2 chapel hearth | `[34, 71, -113]` | `wave/gate-assault` lane, last waypoint `[17, 71, -107]` | **18.0** | 23.9 (`aggro_radius` 16 + 7.9 measured march drift) | `[42, 71, -101]` | **25.71** | +1.81 |

Neither was moved by editing the prefab metadata: `tk-barrow-field` and
`tk-courtyard-chapel` are deterministic output of the engine's
`prefabs/tidal-keep-generator`, so a hand-edited anchor is a silent drift the
next regeneration reverts. The generator was changed, re-run, and its output
copied in. Proved before and after: the unmodified generator reproduces the
prefabs as they stood on this branch **byte for byte** (all six pieces), and the
modified generator is byte-identical across two runs (all six). Only the two
intended pieces differ; the other four are unchanged bytes.

Both fires are physical fixtures, not bare anchors, so the hearths moved with
them.

- **BF1** — the campfire, its cobble ring and the driftwood spar now sit far down
  the western strand at `(10,_,30)`, rest cell south of the flame at `(10,_,31)`,
  facing the field. Still on the landing beach, still visible from spawn across
  open sand, still the first thing the shore offers — and 19.8 blocks from the
  kneeling warden. It could not simply move south: the tide bounds the piece at
  local z=33, so no cell on the centre line is more than 17.0 blocks from the
  kneel and clearing 16 needs the lateral run. The west driftwood spar moved from
  local x=11 to x=15 so it no longer lies on the new rest cell.
- **BF2** — the hearth left the north wall of the nave for the **south wall at
  the east end**, beside the undercroft door: the last fire before the drowned
  way down. This is the "defensibly safe interior cell" case. The chapel simply
  cannot do better — its interior is x 30..42 local and its two east corners are
  the farthest cells from the lane end at ~26.9 blocks, so 25.7 with a 1.8-block
  margin is near the room's ceiling, not a choice. It is also the better fire:
  the party regroups at the head of the stair it is about to descend rather than
  in the corner the gate breach opens onto.

Every field referencing either anchor still resolves — `anchor/l0-bonfire` and
`anchor/l2-bonfire` each have exactly one campaign reference (the `bonfire`
effect in `quest/the-landing` and `quest/the-hollow-watch`); the re-seat /
checkpoint machinery reaches them through those beats, and the compiler's own
`rest` steps 2 and 8 on the exported critical path now name the new cells.

### Compile proof

- `delvec validate` / `analyze` / `build` — **exit 0**, and **zero `DW0478`
  findings**. The only diagnostic left is the pre-existing `DW0465` *warning*
  (no `cast` ledger at `dsl_version` 0.6.0), which is the owner-sequenced work
  this round deliberately does not do.
- `--lang zh-cn` build — exit 0.
- English double build — byte-identical
  (`054bb5777d668c0233db997370256793cc6b9cd3`).
- No campaign JSON was edited this round. The diff is four prefab files.

### Storybook + version marker (owner directive, this round)

The bell had **no** player-facing storybook — every other delivered campaign
(tide-mill, the-wake, nobodys-cave-island) ships `README.md` +
`README.zh-cn.md` and the bell was the gap. Both were written this round, to the
tide-mill shape, and both open with the version marker the owner asked for:

> **Requires delve engine `delvec` ≥ 0.1.0 · Minecraft 1.21.11 · campaign format 0.8**

The numbers are read off the campaign and the toolchain, not chosen:
**campaign format 0.8** is the **maximum** declared per-stage `dsl_version`
(`classes.json` is `0.8.0` for the `flask` kit entry; the other five stages are
`0.6.0`), and the engine line is verbatim `delvec --version` for the binary this
round validates green with (`delvec 0.1.0, dsl 0.8.0, mc 1.21.11`). A machine
check on that consistency is task #147.

The zh-cn storybook is written in Chinese, not translated from the English —
names and voice are taken from the campaign's own `l10n/zh-cn.json` (沉钟,
晚钟堡, 摆渡妇, 司事, 坟场戍卫, and the four class names) so the page and the
game agree. Both pages are player/host-facing only: no pipeline machinery, no
diagnostics, no round history.

### Round-4a ladder (engine main `fac18f8`: #235 + #238 + #239 + #249)

Isolated project `dw-worker-bell4a`, mutex holder `bell4a`, `worker-override.yaml`
(config verified: no `container_name`, no published port), fresh volumes before
each stage and after teardown, `DELVEWRIGHT_RUN_TIMEOUT_MS=2700000` (the knob is
plumbed now; the 20-minute default is what stopped run four).

#### PackTest — GREEN

> `========= 37 GAME TESTS COMPLETE IN 959.4 ms ======================`
> `All 37 required tests passed :)`

Exit 0. 33 templates in run seven, **37** now.

#### Bot ladder — `die-retry` GREEN, `critical-path` RED at step 22 of 23

Exit 3. Both stages ran.

| stage | ran | passed | failures |
| --- | --- | --- | --- |
| `critical-path` | true | **false** | `step 22 (talk-to) failed: bot died at [24, 63, -15] — likely cause: delve-bot was slain by Hollow Gate-Warder` |
| `die-retry` | true | **true** | — |

**All four encounters `phase_reached: "cleared"`, 5 assist windows each, 20 in
total.** The Bellkeeper was reached, fought and killed — the first time in
**eight** runs.

| encounter | wave | trials | at_checkpoint | respawn | kit_kept | returned | re_engaged | outcome |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `obj/hold-the-gate` | `wave/gate-assault` | 2/2 | true | `[42,71,-101]` | true | true | true | `re-engaged` ×2 |
| `obj/hold-the-wall` | `wave/wall-assault` | 2/2 | true | `[42,71,-101]` | true | true | true | `re-engaged` ×2 |
| `obj/the-echoes` | `wave/grave-echoes` | 2/2 | true | `[42,71,-101]` | true | true | true | `re-engaged` ×2 |
| `obj/the-keeper` | `wave/bellkeeper` | 2/2 | true | `[97,71,-96]` | true | true | true / false | `re-engaged`, then `cleared-before-retry` |

`rests[]` — all three fires armed at the new cells: BF1 `anchor/l0-bonfire`
`[10,63,31]` step 2, BF2 `anchor/l2-bonfire` `[42,71,-101]` step 8, BF3
`anchor/l4-bonfire` `[97,71,-96]` step 17.

**Run seven's re-seat accumulation defect is GONE.** Every `respawns_on_rest`
wave came back at its declared count, as all-new entities, at full health —
`carried_over: 0` on all six of their trials, `declared == present` every time,
`damaged: 0` every time:

> `wave/gate-assault death 2: 2/2 wave mob(s) after 250ms, 4.5–4.6 blocks from the anchor, 0/2 damaged`
> `wave/wall-assault death 1: 1/1 wave mob(s) after 251ms, 4.3–4.3 blocks from the anchor, 0/1 damaged`
> `wave/grave-echoes death 1: 2/2 wave mob(s) after 250ms, 3.6–11.8 blocks from the anchor, 0/2 damaged`

Run seven read 4 standing against 2 declared, and 6 against 1. This run reads
exactly the declared count, every time.

The Bellkeeper's `carried_over: 1` on death 1 is **correct and not a defect**:
`wave/bellkeeper` declares no `respawns_on_rest`, so the boss you already
engaged is the boss still standing. Death 2 is `cleared-before-retry` — a
documented PASS (`obj/the-keeper` was already complete, so the death cost no
progress).

#### The two old reds

**(a) gate-assault bot-floor variance — CLEARED.** Run six had the bot lose the
gate fight on its feet with `assist_windows: []`; run seven fought it but
accumulated survivors. This run: `phase_reached: "cleared"`, 5 assist windows,
2/2 trials, both `re-engaged`, no carry-over. The gate siege is winnable at
`normal` and now measurable.

**(b) portcullis phase-read — FIXED, and the evidence is explicit.** #239's
observed gate-edge machinery is visible doing exactly what it was built to do:

> `[timed-gate] anchor anchor/l1a-ward: proven route crosses timed-gate/portcullis (70t open / 30t closed, 100t cycle ≈ 5.0s)`
> `[timed-gate] anchor anchor/l1a-ward waypoint 3/5: crush gate ahead — staging at the edge of timed-gate/portcullis for a fresh window`
> `[timed-gate] anchor anchor/l1a-ward waypoint 3/5: staged crossing of timed-gate/portcullis (budget 25.0s, min 3 attempts)`
> `[timed-gate] gate is shut; waiting for it to open`
> `[timed-gate] window open — crossing now`

The bot staged at the edge, read the phase, waited out the shut, crossed on the
open, and was not crushed. Step 4 passed and never came back.

#### The new red — the walk home crosses re-armed siege ground

The remaining failure is a **content/pacing fact, not a harness artifact**, and
it is the shape only a run that gets this far can see.

The finale is step 21 `reach anchor/l2-muster` → step 22 `talk-to
npc/ferrywoman` on the shore. Resting at **BF3** (step 17, the rope room, before
the Bellkeeper) re-seats `wave/gate-assault` and `wave/wall-assault` back in the
courtyard — correctly, at full strength. The rope drop then lands the party in
that same courtyard, and the walk home goes straight through the muster yard
with the siege already won and standing again.

Once aggroed, the re-seated Gate-Warders **pursued across the map**. The bodies
say how far:

> `Named entity 'Hollow Gate-Warder'/256 … x=24.50, y=69.64, z=-28.80 died: … was shot by Arrow`
> `Named entity 'Hollow Gate-Warder'/257 … x=24.50, y=64.00, z=-16.24 died: … was killed`

Their lane is in the courtyard at `[12,71,-85]`. They died at `z=-28.8` and
`z=-16.2` — down the whole gatehouse descent, ~70 and ~85 blocks from the lane,
three levels below it. The bot was walking a `talk-to` step, not fighting, and
ate two stews on the way down without recovering (`health 4.5 → 0.6 → 0.0`):
`rabbit_stew` fills hunger, and hunger regen cannot outrun a vindicator with a
stone axe.

Three separable questions, none of them touched this round, all of them the
owner's:

1. Should a rest at BF3 — past the siege, inside the tower — re-arm the courtyard
   at all? `respawns_on_rest` is per-wave and global to every fire.
2. Should the finale route cross the muster yard, or should the rope drop feed a
   way out that does not?
3. Is being chased three levels down by the siege you already beat the delve
   working, or the delve leaking?

Not tuned, not rerolled, and the bot's fencing is telemetry rather than the gate:
the die-retry stage proved the same wave winnable eight times over on the way up.

#### Unchanged, and still worth an engine look

`floor_gate: {present: true, covered: [], not_covered: []}` and `actors: []` —
the Barrow Warden has not appeared in the ledger for **eight** runs. It is an
`actor` and only waves carry a `tier`; `actors[].tier` is 0.8.0 on the quests
stage, which this campaign has not been raised to.

`validation/fresh-volumes.sh --project dw-worker-bell4a` reported
`verified clean (containers + volumes)` before the run and after teardown; the
mutex was released by name.

One new log observation, harmless but new: on world save the server logs
`Failed to encode value 'DYING' to field 'pose': Invalid pose: dying` for the
`Mannequin` entities backing the Sexton and the Ferrywoman. It is a `WARN` at
serialization time, not a test failure — PackTest was 37/37 with it present —
but a pose vanilla refuses to persist is worth an engine glance.
