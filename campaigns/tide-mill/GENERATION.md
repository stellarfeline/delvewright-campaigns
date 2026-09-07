# Tide Mill — generation record

- **Date**: 2026-08-03
- **Front-end**: `/new-delve` (ADR-0012), run end to end as a deliberate
  dogfooding exercise — every friction point below is a deliverable, not an aside.
- **dsl_version**: 0.8.0 · **delvec**: workspace build at
  `cb9c014` · **Minecraft**: 1.21.11 (ADR-0009)
- **Seed**: 41 · **Languages**: `en` (canonical) + `zh-cn` sidecar

## Brief (from the owner-approved demo-level queue, `docs/demo-levels.md`)

> **Tide Mill** — a mill race where the water gate cycles; the whole level is
> timing runs through THREE timed gates (spec-0016 §4 timed-gate machinery in the
> spotlight) with escalating windows: generous first gate, tight third. Consider
> `crush: true` on the final gate only — the 20 % window proof is what earns it;
> the first two gates teach, the third bites. 10–20 minutes, minimal cast (a
> miller NPC framing the run), linear (no branch machinery needed).

Constraints carried in with it: dsl 0.8.0 with `happening` declarations and no
branch points; the ≥ 20 % window rule must pass on all three gates with real
crossing-time arithmetic, not vibes; `DW0331` caption labels; no waves, no
bonfires; plain checkpoints between gates; full ladder in both languages.

## Design decisions

The design itself is `DESIGN.md`. What follows is why it came out that shape.

1. **Three gates forced a two-area layout.** The prefab library has very few
   gate regions that the nav model can actually prove, and only one usable
   distinct gate-anchor *name* per tileset — see friction 1–3 below. The three
   provable gates in the whole library that can coexist in one campaign are
   `anchor/l1a-gate-timed` (tk-gatehouse), `anchor/l3-shortcut-a` (tk-cistern)
   and `anchor/gate` (keep-gate-room). The first two live in `pool/tidal-keep`
   and the third in `pool/stone-keep`, so the level is two areas.
   That turned out to be a gift, not a compromise: the area change emits a
   one-way teleport, which is exactly what a mill race is — you do not swim back
   up one. The fiction (the undertow takes you under the sea wall) was written to
   the mechanism, not the other way round.

2. **All three crossings cost the same 8 ticks**, measured out of the compiler
   rather than assumed (method in `DESIGN.md`). Holding the crossing cost
   constant is what makes the escalation legible: the *only* thing that changes
   between gate 1 and gate 3 is the window. 70 % → 37 % → 24 % of cycle, open
   half 6.0 s → 3.0 s → 1.8 s.

3. **`crush: true` on the third gate only.** The addendum's rule is that the
   20 % proof is what earns the lethal edge. Gate 3 clears the floor by four
   points — provably fair by the same arithmetic that proves gate 1 generous —
   so the penalty may be absolute. Gates 1 and 2 teach the read for free.

4. **Two checkpoints, and the second one is set from the other area.** See the
   `DW0315` finding in the build log below. This was the one genuine content bug
   of the run and the compiler caught it cold.

5. **No `loot`, no `traps`, no waves, no bonfires.** The brief asked for one
   mechanic in the spotlight. The only lethal element in the delve is the closing
   edge of gate 3, and it has a checkpoint 13 blocks upstream.

## Branch chronicle review (spec-0025 §4)

**Not applicable — and that is a checkable claim, not a skip.** The stage-4 plan
declares no `branch_points` (the brief specified a linear level), so the build
emitted no `validation/branch-plan.json` and no
`validation/branch-chronicle-*.md`. The pass is mandatory *whenever the plan
declares `branch_points`*; with none declared there is exactly one storyline and
the single critical-path run proves it. `ls out/validation/` shows
`critical-path-waypoints.json` and nothing else.

## Build log

| step | result |
|---|---|
| `delvec validate` | exit 0 (after the l10n sidecar landed) |
| `delvec analyze` | exit 0 — no unreachable quest, no deadlock, no unmitigated darkness |
| `delvec build` (en) | exit 0 |
| `delvec build --lang zh-cn` | exit 0 |
| determinism | two consecutive `build` runs are byte-identical (ADR-0006) |
| `DW0378` | all three gates proven: 70 % / 37 % / 24 % against the 20 % floor |
| critical-path waypoints | each gate crossed exactly once, in escalating order |

### The one content bug: `DW0315`

The first build failed:

> checkpoint `anchor/l3-landing` (cell [27, 71, -83]) strands the party: the next
> required anchor [260, 61, 24] is not walkable from it over the assembled
> geometry.

The design had put a checkpoint where the party clears gate 2 — but the inter-area
transport fires on that *same* objective, so a respawn there would drop them back
in `area/millrace` with the rest of the campaign 236 blocks away across void.
Fixed by setting that checkpoint at `anchor/keeper-stand` instead: checkpoint
anchors resolve globally by name, so a quest in `area/millrace` can move the
respawn into `area/undertow` on the tick the undertow lands the party there.
`DESIGN.md` was updated in the same change.

Removing the now-duplicate checkpoint one step later shifted the position-derived
l10n key `fx.the-brake.oc.read.1.narrate` → `…read.0.narrate`, and
`DW0180`/`DW0181` caught both halves of the shift immediately. The documented
pitfall behaved exactly as documented.

## Localization

`delvewright.local.toml` declares an `[i18n]` section but the env var it names
(`DELVEWRIGHT_I18N_API_KEY`) is unset, so per the skill the sidecar was
translated **in-agent** from the finished English via
`delvec l10n-inventory --lang zh-cn` (43 keys, covered exactly). Button captions
were kept inside the `DW0331` Han budget. No non-English string was written into
any stage document.

## Toolchain friction found (the point of the exercise)

0. **PackTest covers only the FIRST declared timed gate — so the `crush` edge
   ships with no runtime coverage here.** `emit_timed_gate_packtest`
   (`compiler/src/emit.rs`) opens with `let Some(g) = plan.timed_gates.first()`
   and emits exactly one `souls_timed_gate.mcfunction` per campaign;
   `emit_timed_gate_crush_packtest` is only ever called on that same first gate.
   Tide Mill declares three gates and puts `crush: true` on the **third**, so the
   generated suite contains `souls_timed_gate` for `timed-gate/grate` and **no
   `souls_timed_gate_crush` at all** — the region-selector scoping assertion the
   addendum specifies never runs. Verified against the emitted
   `packtest-datapack/` tree.
   This has been invisible until now because the only shipped campaign with a
   timed gate (the-drowned-bell) declares exactly one, and it happens to be the
   crush gate. The fix is a loop over `plan.timed_gates` with per-gate file names
   (`souls_timed_gate_<safe>`), which is also what makes the multi-gate case
   testable at all. **This is the most consequential finding of the run**: a
   lethal mechanic with a compile-time proof and no runtime proof.

1. **A timed gate on an anchor no placed piece provides is silently dropped.**
   `required_anchors_for_area` (`compiler/src/plan.rs`) collects objective, NPC,
   wave, lane and quest-effect anchors — but **not** `timed_gates[].gate`,
   `shortcuts[]`, `ambushes[]` or `loot[]` anchors. So the layout solver has no
   obligation to place the piece a timed gate lives in, and
   `gate_region_block_any` drops an unresolvable gate inside a `filter_map`.
   Reproduced: a campaign declaring `timed-gate/ghost` on
   `anchor/l2-breach-gate` while the chapel is not in the assembly **validates,
   builds, and exits 0**, with the gate simply absent from the emitted
   `timed_gates` table and no diagnostic anywhere. This is the same class as the
   TD-lane waypoint bug already fixed in that function, whose own comment says it
   fails "for a reason the author cannot act on".

2. **A timed gate with no standable footing on both sides is silently unproven.**
   `verify_timed_gates` `continue`s when `gate_crossing_footings` returns `None`
   ("no footing on both sides — a geometry concern, not a timing one"). But the
   result is that `DW0378` never runs on that gate. Reproduced on
   `anchor/l3-commit-gate` (its far side is a drop, not floor): a gate declared
   **1 tick open / 400 ticks closed — a 0 % window — builds green, exit 0**.
   The design proof the whole mechanic rests on can be absent without saying so.
   Both 1 and 2 want the same shape of fix: a `DW04xx` warning (or error) when a
   declared timed gate ends up with no proof attached to it.

3. **The library is gate-starved, and gate anchors collide across areas.** The
   whole prefab library contains ten region anchors with a fill `block`, of which
   exactly three are cross-corridor chokepoints the nav model can prove; two of
   those share the anchor **name** `anchor/gate` (`cave-mouth`,
   `keep-gate-room`). Gate anchors resolve **globally by name**
   (`gate_region_block_any` / `point_any` scan `(area, name)` for the first
   matching name), so the same prefab in two areas — or two prefabs sharing an
   anchor name — cannot carry two different gates: the second clock lands on the
   first region and trips `DW0377`. A "three timed gates" level is therefore
   near-maximally constrained today. Two library-side fixes would unblock it:
   more purpose-built timed-gate anchors, and an area-qualified anchor reference
   in the DSL.

4. **`anchor/l2-breach-gate` is decoration, not a gate.** It resolves and proves
   nothing about routing: the critical path never crosses it (verified in the
   waypoint artifact) because the chapel's main socket sits beside it. Worth a
   note in the prefab metadata so the next author does not spend a build finding
   out.

5. **Class kits cannot carry enchantments.** `KitItem` is
   `{item, count, name?, carrier?, flask?}` with `additionalProperties: false`;
   enchantments exist on wave `equipment` and on `loot` stacks but not on the
   gear the player actually starts with. A traversal class that wants Feather
   Falling on its boots cannot have it. Reported, not worked around.

6. **`happening` is rejected on `narrate`.** Only the eleven story-node effects
   accept one. The skill's wording ("every staging / wave / gate /
   `campaign-complete` effect") is right, but a narrate beat that carries real
   story weight ("the undertow takes you") ends up with no `happening` and so is
   invisible to the chronicle decompilation. Worth a look when spec-0025's
   chronicle coverage is next revisited.

7. **`validation/delve-output` is not worker-isolatable.** `-p dw-worker-<x>`
   plus `worker-override.yaml` isolate container names, ports, volumes and
   networks — but the `server` and `bot` services read the build tree from the
   hard-coded relative path `./delve-output`, and only `packtest` honours
   `$DELVE_OUTPUT`. Two workers therefore share one output tree and must
   serialise on the mutex for that reason alone. Extending `${DELVE_OUTPUT:-…}`
   to the `server` build context and the `bot` mounts would close it.

8. **`i18n --reflect` does not exist.** Neither `delvec l10n-inventory` nor
   `tools/i18n-translate.py` has a `--reflect` flag, and the string appears
   nowhere in `docs/reference/`. Flagged in case it is a planned flag that leaked
   into a brief early.

9. **Visual review could not run locally** (skill step 9): no 1.21.11 client jar
   is present on this workstation, so `delve-render batch` has no textures and
   `validation/render-shots.sh` has nothing to path-trace. Noted rather than
   faked; the storybook ships without images. (The build did emit a 53-shot
   `render-plan.json` with `expect` checklists, so the review is ready to run the
   moment a client jar is available.)

   Related and worth resolving either way: **the skill and the content repo
   contradict each other about images.** Skill step 10 says the storybook carries
   "Images (relative links into `media/`, small JPEGs) … media ships with the
   campaign PR"; this repo's contribution contract says "**No images, no worlds,
   no binaries, ever** — canonical images are built only by trusted CI from these
   sources". One of the two has to give. This campaign followed the repo.

10. **The shipped `server/README.md` misreports the difficulty.** It is emitted
    from a string literal in `compiler/src/emit.rs` that hardcodes
    "`gamemode=adventure`, `difficulty=peaceful`", while the `server.properties`
    beside it correctly carries `difficulty=normal` from `world.difficulty`.
    Stale since the v0.5 difficulty surface landed. It ships inside the delve, so
    it is a player-visible artifact stating the opposite of the world's actual
    setting.

11. **A minor sharp edge**: `delvec` resolves prefabs from the *relative* path
    `campaigns/prefabs`, so every invocation must be made from the engine repo
    root. Running it with the campaign directory as cwd fails with
    `internal error: cannot read prefabs dir campaigns/prefabs`, which reads like
    a bug rather than a cwd requirement.

## Conformance review (skill iteration protocol)

Read the compiled campaign back against `DESIGN.md` beat by beat:

- **The miller's count is arithmetically true to the compiled clocks.** He says
  the grate is "six seconds open, two shut" (120 t / 40 t ✓), the wheel sluice is
  "half of it: three open, four shut" (60 t / 80 t ✓), and the tide gate is
  "under two seconds open, four and better shut" (36 t / 84 t ✓). If any clock is
  ever retuned, these four lines and their `zh-cn` counterparts must move with it.
- Emission spot-checked: three self-sustaining `tgate_open_*`/`tgate_close_*`
  ping-pong pairs, and the `damage @s 1000` judgement appears on
  `tgate_close_tide` **only**, ahead of its `fill` — gate 3 alone is lethal, as
  designed.
- `server.properties` carries `spawn-monsters=false`, so the closing edge of gate
  3 really is the only thing in the delve that can kill a player.
- **One deliberate non-deviation**: the root dialogue node lets a player answer
  "I'll run it." and leave without hearing the count. That is allowed on purpose —
  the objective hints still say "stand off, watch it once, then walk", so the read
  is taught twice and refusing the briefing is a legitimate choice.
- Deviations from the design as first written: exactly two, both recorded above
  and both folded back into `DESIGN.md` — the checkpoint move forced by `DW0315`,
  and the unenchantable class boots.

## Machine validation ladder

`delvec validate`, `analyze` and `build` are green in both languages, all three
`DW0378` window proofs pass, and the emitted clock is correct
(`tgate_open_*`/`tgate_close_*` ping-pong, `damage @s 1000` on the tide gate only,
ahead of its fill). PackTest and the critical-path bot were run in an isolated
compose project (`-p dw-worker-tidemill` + `validation/worker-override.yaml`, no
host port, mutex held as `worker-tidemill`).

**The bot run REDs, and it is a harness bug — the delve is completable.**

### The finding: gate-retry vs. inter-area transport on the same leg

```
FAILED: step 3 (reach) failed: anchor anchor/l3-landing waypoint 23/27:
  still blocked after 3 timed-gate crossing attempt(s) over 110.3s — more than
  two full cycles of `timed-gate/wheel` (60t open / 80t closed, 140t cycle ≈ 7.0s).
  The window is not the problem; this is a real navigation failure:
  failed anchor anchor/l3-landing waypoint 23/27 at [24, 71, -58] (range 1);
  bot at [257.3, 61.0, 2.5]: No path to the goal!
```

Read the two positions together. The waypoint the harness is trying to reach,
`[24, 71, -58]`, is the far mouth of gate 2 in `area/millrace`. The bot is at
`[257–260, 61, 2–4]` — which is the **inter-area transport destination**, and the
only command in the entire datapack that puts a player there is
`teleport @s 260 61 4` inside `complete_o_wheelpit`.

Confirmed against the live server while the loop was still spinning:

```
$ rcon-cli "scoreboard players get #party dw.o_wheelpit"   →  #party has 1
$ rcon-cli "scoreboard players get #party dw.q_the_count"  →  #party has 1
```

**The objective and the entire first quest are complete.** The bot crossed the
wheel sluice, reached the landing, and was transported exactly as designed — and
the harness then treated the resulting position discontinuity as the timed gate
blocking it, entered the `timed-gate` retry loop, and failed a leg it had already
walked. Its own recovery ("re-centering on proven cell `[24, 71, -56]`") cannot
work: the transport is a one-way point of no return, so there is by construction
no path back.

Reproduced identically on a second, demonstrably fresh world (fresh
`fresh-volumes.sh --project`, server log shows the level being generated), so it
is deterministic, not a stale-volume artifact and not the known crush-gate phase
flub — note that gate 1 (`timed-gate/grate`) is crossed with **zero** retry lines,
and the failure is at gate 2, which does **not** carry `crush`.

The compiler already exports what the harness needs to avoid this:
`critical_path_transport` is a per-step marker that exists, in its own words, "so
the harness can wait for the position discontinuity". The timed-gate retry path
does not appear to consult it. Tide Mill is plausibly the first campaign where a
single leg both **crosses a timed gate** and **ends in an inter-area transport** —
the-drowned-bell has a timed gate but no transport on that leg, and
nobodys-cave-island has transports but no timed gates.

Per the debug doctrine this was **not** worked around: the gate was not widened,
the seed was not rerolled, and the campaign was not restructured to split the
gate leg from the transport leg. The delve is proven completable by the server's
own scoreboard; the harness needs the fix.

### Per-run results

Six bot attempts — three English, three `zh-cn` — every one reproducing the same
signature. PackTest green in both languages.

| language | packtest | bot attempt 1 | attempt 2 | attempt 3 |
|---|---|---|---|---|
| `en` | **exit 0** — 16/16 | exit 1 | exit 1 | exit 1 |
| `zh-cn` | **exit 0** — 16/16 | exit 1 | exit 1 | exit 1 |

- `critical-path`: `ran: true, passed: false` in all six.
- `die-retry`: `ran: false` — *"no combat plan in this build — the campaign
  declares no mandatory combat"*. Expected: the delve has no mandatory combat, so
  the stage is correctly recorded as not run rather than as passed.
- `floor_gate`: `{"present": false, "covered": [], "not_covered": []}` in all six
  — correct, the campaign declares no tiered wave and no tiered actor.
- `actors`: `[]` in all six — correct, the campaign stages no actors.
- The `zh-cn` PackTest run shows `科林·塞奇` in the server log, confirming the
  localized delve loads its sidecar.

**The most telling sample is `zh-cn` attempt 1**, which failed at *waypoint
26/27 at `[27, 71, -83]`* — that is `anchor/l3-landing` **itself**, the objective
anchor. The bot was reported unable to path to the very cell whose trigger zone
had just completed the objective and teleported it away. The other five failed one
waypoint earlier, at the far mouth of gate 2. Same bug, caught at two points along
the same leg.

Gate 1 is crossed with **zero** retry lines in every run, and gate 3 — the only
`crush` gate — is never reached, so nothing here is evidence about the crush
edge either way. Combined with finding 0 above (no `souls_timed_gate_crush`
PackTest is emitted for this campaign), **the lethal closing edge of
`timed-gate/tide` currently has no runtime proof of any kind in this delve.** Its
compile-time proof (`DW0378`, 24 % window) is green, and the emitted command is
correct by inspection, but no machine has watched it fire.
