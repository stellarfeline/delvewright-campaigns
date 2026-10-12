# The Stranding: problems met while making the map

This lists every problem met while rebuilding the map of `campaigns/the-stranding` on the site-plan route through `/new-delve`. The engine is `delvec 1.12.0` at `a7f3f621ee8fc22d29f06e9ae298383b88126056`, with dsl 0.39.0 and Minecraft 1.21.11. Each row gives the symptom, a minimal repro, a class, what was done about it, and whether it still blocks anything. The record uses place ids and capabilities, never story.

The classes are:

- **engine**: an engine defect.
- **capability**: a missing capability.
- **friction**: tooling friction.
- **doc**: a gap in the skill docs.
- **mine**: my own mistake.

## Engine defects and missing capabilities

| # | Symptom | Minimal repro | Class | What was done | Still blocks |
|---|---|---|---|---|---|
| 1 | `node/sea-skiff` cannot be detailed. `contract-well-formed` needs an `exterior` traversal edge on the entry space, and `DW0844` refuses any face no seam allocates. | A site-plan box joined to the rest only by a `carry` edge, then `delvec detail . node/<box>`. | capability | The place stays a site-plan stand-in. Its builder is kept, but its program is not written. | Yes. `node/sea-skiff` is a stand-in. |
| 2 | After a seam or owed-anchor change, `delvec detail <place>` and `delvec detail . --all` both refuse up front with `DW0844` or `DW0845` on every other row the change made stale. The documented "after any plan edit run `--all`" step has never run green on such a change. | Change one contact's extent between two detailed places, then run `delvec detail . --all`. | engine | Delete the affected rows from `detail-plan.json`, then run `--all`. This cost about half a day before it was found. | No, while the workaround is used. |
| 3 | `DW0891` refuses a staged killing volume whose keep-out reaches floor before its flip, and prescribes an anchor at the pit's bottom. That bottom is a sealed hollow, and `DW0845` refuses an owed anchor inside a `no_body` region. | A floor course over a two-high hollow claimed `no_body`, with a station in the hollow and a `lethal_volumes[]` row gated by a flag set beside a `clear-region` of the floor. | engine (unreachable remedy) | The collapsing bank in `node/run-bank` and the back places keeps its collapse and checkpoints, but has no killing volume. A fall costs nothing. | Yes. A simplification. |
| 4 | `DW0948` refuses any interaction body inside a loop's near field. A 12-block loop's span covers a whole 30-block corridor, so a loop released by something inside it cannot be declared. | A spec-0086 loop in a corridor whose release is an interact objective inside the corridor. | capability | No loop is authored in `node/throat`. The place is walked straight. | Yes. A simplification. |
| 5 | A world-edits `fragment` writes its non-air cells over bound place frames silently. The sculpt dresses a cut's faces with slabs and stairs inside the cut. Only the consequences were reported (`DW0210`, `DW0311`, `DW0430`), never the overlap. | Cut a box from a form exactly at a place's claim, then stamp it. The place's ring and lid hold slabs and stairs. | engine | Inside cuts are made 1 cell wider and 1 lower. Places on the body are cut from a course under their floor. This took several build cycles. | No. |
| 6 | An `open` site fill floods nothing below the ocean horizon's sea level inside the region, so the channels were dry pits a body fell into (`DW0921`). A world-edits `replace` matching `minecraft:air` matches nothing in empty model cells. | An `open` site whose heightmap dips below y62 inside the region. | engine | The sea is filled by the world-edits batch `batch/the-sea` (surface band ∩ under-sea box), plus water under each mud field. | No. |
| 7 | The generated PackTest `pulse_heartbeat_shut` fails: `Expected #pclr_heartbeat dw.sys to match 0, but got 1`. It asserts that `schedule clear` returns 0 without clearing first, while concurrent tests set the pulse's gate flag. | A gated pulse whose gate flag any quest or trigger test sets, then `validation/packtest-run.sh`. | engine | Recorded. It was red on two builds and was not re-run to get green. | Yes. PackTest is red by exactly this one test. |
| 8 | `open-gate` writes `fill … air replace minecraft:iron_bars[east=false,…,west=false]`. The server re-derives a row of bars to `east=true,west=true`, so the gate matches nothing and the seam never opens. The bot stood in the doorway: `step 21 (interact) failed … timed out after 60000ms`. | A barred seam two or more cells wide, opened by `open-gate`. | engine | The two barred seams (`node/far-ferry-house` land door, `node/slipway-stair` shortcut) are shut with dark oak planks instead. | No. |
| 9 | The bot ladder does not wait for placement (`#placed dw.sys`). Its first leg starts when the login window closes. One run walked from the world origin (`No path to the goal!`, bot at `[10.5, 57.7, 8.5]`). Another was teleported mid-leg (`The goal was changed before it could be completed!`). Other runs of the same build passed step 1. | Any map whose placement outlasts the login window, then `validation/bot-run.sh`. | engine | Recorded. The red runs are kept as red. | Intermittently. It can red any ladder run at step 1. |
| 10 | `DW0955` model class has 3744 cells, written air against server stone, at y47..54 under exactly the footprints (plus a 1-cell ring) of `node/pier` and `node/sea-skiff`. | Those are the two places standing over open sea. Run `delvec written-world`, `validation/world-save.sh` and `tools/ci/check-written-world.py`. | engine | Recorded. No document of this campaign writes those cells. | Yes. The DW0955 verdict is red. The staging gate refuses a red written-world record. |
| 11 | The die-retry respawn was refused: `respawned at 270,96,9, which is not the checkpoint governing this encounter`. The combat plan read the last trigger-set checkpoint (`[215,64,511]`, set late on the route) as governing every encounter from the start. | A trigger effect `set-checkpoint` late on the route, plus an early wave. Read `validation/combat-plan.json` `checkpoint`. | engine | The collapse stakes in `node/run-bank` no longer set checkpoints. | No, but the stakes set none. |
| 12 | Carried paint meeting the inside's paint at the body's mouth is refused (`DW0929`). | Two atmosphere zones, one carried, meeting at a place boundary. | capability | The far bank and the body's outside take the inside's atmosphere beat. | No. A simplification of the atmosphere layout. |
| 13 | Two skiffs are never proven out of sight of each other. | The brief asks for the check, and the engine has no out-of-sight proof. | capability | Recorded. | It does not block the build. Do not judge it. |
| 14 | A delve-killing volume needs an `on_death` bundle, or the death plan is `UNBOUND`, and the death-loop stage is skipped. | `lethal/stomach-pool` with no `on_death`. | doc | Left. The design declares no death consequence. | No. The death-loop stage is reported skipped. |
| 30 | Critical-path stage red on the muster: `wave/drowned-wrecks-2: wave seating: the campaign declares 6 body/bodies … the muster read 5: 1 of the missing 1 were felled by the party since this seating, before the muster read them`. | Two waves seated close together in `node/mud-wrecks-east`/`-west`, so a body of the second reaches the bot during the first. | mine (spacing) or engine (muster ordering), undecided | Recorded. Not re-run. | Yes. The critical-path stage is red. Every step was walked. |

## Tooling friction and skill-doc gaps

| # | Symptom | Class | What was done | Still blocks |
|---|---|---|---|---|
| 15 | `detail <one place>` re-runs the whole build, about 10 minutes on this map. `--all` re-makes all 54 places in about the same time. Hours went into per-place detail before `--all` was found to be fast. | friction / doc | `--all` is used after every edit. | No. |
| 16 | Adding stations in two places at once deadlocks per-place detail: each refuses on the other's stale row. | friction | Places are edited one at a time, or rows are deleted (see #2). | No. |
| 17 | One global `~/.delvewright/env.sh` names one engine tree. | friction | The pinned tree was named in it. | No. |
| 18 | The light probe needs a side entrance on top-entered pieces. | doc | A side entrance was added where the probe asked. | No. |
| 19 | Through-floor stair contract patterns are undocumented: the top tread sits in the hole, and the two top treads need head clearance. | doc | Found by trial against `DW0430` and DW0836-class refusals. | No. |
| 20 | `branch-runs.sh` takes the default 20-minute budget unless `DELVEWRIGHT_RUN_TIMEOUT_MS` is set. This route is about 51 minutes. The first branch run failed with `run exceeded wall-clock budget of 1200000ms`. | doc / mine | The budget is now set to 5400000 for every run. | No. |
| 21 | The critical path is long: 3030 blocks, about 51 minutes at the provisional pace (`DW0822`), against `target_minutes` 150. | (measurement) | Recorded. | No. |

## My own mistakes

| # | Symptom | What was done | Still blocks |
|---|---|---|---|
| 22 | An early helper script wrote scratch output under `/tmp`, which the brief forbids. | Moved to the campaign worktree's untracked `.out/`. | No. |
| 23 | Waiting loops built on `ps aux \| grep` never terminated. 35 were killed. | Waits are now by PID or on a sentinel line. | No. |
| 24 | A world save ran beside a bot run, so two delve servers booted on one host at once. That run's step-1 red (#9) may have been made more likely by the load. | Rungs now run one after another. | No. |
| 25 | Two bodies stood on one mark at the far skiff, so a talk target was unclickable: `the crosshair cannot acquire interaction … Their hitboxes are COINCIDENT`. | One NPC now stands 2 cells aft. | No. |
| 26 | Barred seams were built of iron bars (see #8). | Shut with planks instead. | No. |
| 27 | Dressing the server breaks or re-derives produced `DW0955` model cells: glow-berry strands hung under lichen, not a sturdy block (262 cells); dead bushes stood on packed mud (5); lanterns stood on nothing (3); red mushroom blocks re-derive their faces (10). | Every piece now settles its vines before it is written. Bushes stand on mud, lanterns on posts, and mushroom blocks were dropped. | No. |
| 28 | Many build-proof refusals were met and answered in the documents and generators. Each was a content defect, fixed there: `DW0836`, `DW0837`, `DW0838`, `DW0877`, `DW0990` (blockout battery, 127 down to 0); `DW0210`, `DW0311`, `DW0315` (route and checkpoint proofs); `DW0430` (stair facing); `DW0885` (shown faces); `DW0897` (tentacle and watcher stands); `DW0921`, `DW0922` (pits and killing volume); `DW0932`, `DW0542` (carry extents); `DW0963` (tiller affordance); `DW0724` (camera lens); `DW0359` (watcher in valves); `DW0995` (pulse not live on the forced route); `DW0187`, `DW0982` (localisation). | Fixed. | No. |
| 29 | The showcase cameras are estimated poses written through `delvec place-camera`, not composed views. | Recorded. | It does not block the build. |
