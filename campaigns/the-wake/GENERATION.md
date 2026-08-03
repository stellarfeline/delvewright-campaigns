# The Wake — generation record

- **Date**: 2026-08-03
- **Generator**: `/new-delve` (Claude Code skill, ADR-0012), followed end to end
- **DSL version**: 0.8.0 (all six stages)
- **Engine**: `delvec` at Delvewright `main` d2d51d9
- **Content base**: `delvewright-campaigns` `campaign/the-drowned-bell` 7bfc0b5
  (stacked — see "PR base" below; `main` does not carry the tidal-keep tileset)
- **Prefab library**: `prefab/tk-barrow-field` (tidal-keep tileset, original asset,
  GPL-3.0-or-later, provenance in the prefab's own metadata)

## Prompt (verbatim, as queued)

> **The Wake** — a funeral procession level that is 80% staging (spec-0014
> actors/move-npc/sequence/cutscene machinery in the spotlight): mourners walk, a
> eulogy sequence plays, ONE player choice redirects the procession. 10-20
> minutes, small cast (4-6 mourners + 1-2 speaking roles). The one choice = a
> declared branch point (dsl 0.8.0): two short branches to two ending beats — this
> makes The Wake ALSO the first organic exercise of the spec-0025 chronicle +
> branch-run machinery in authored content, which is valuable; keep both branches
> SHORT.
>
> CONSTRAINTS: dsl 0.8.0 with the branch point declared and per-branch chronicle
> review; DW0331 caption labels; NPC walk yaw is per-segment (engine #212) so
> processions face where they walk; no combat at all (zero waves, zero hostiles);
> plain checkpoints if any (no bonfires); cutscene/camera via the existing dolly
> machinery, minding the air-corridor check; full ladder green in both languages
> (zh-cn sidecar); isolated compose project `dw-worker-wake`.

This is a **detailed brief**, not a thin one — so showcase mode does not apply
and the level honors exactly what the brief pins down and showcases nothing
extra (SKILL "Showcase mode").

## Design decisions

Full design record: `DESIGN.md`. The decisions worth stating here are the ones
that were *choices between authorable alternatives*:

1. **One piece, drawn from a one-member pool.** `prefab_pool: "pool/tidal-keep"`
   with `pieces {min: 1, max: 1}`, which draws the pool's `entry`,
   `prefab/tk-barrow-field`, and nothing else. A staging demo hangs objectives,
   walks and camera subjects on a dozen anchors, so it needs each anchor to be
   unique — a multi-piece draw can place a piece twice and make its anchors
   `DW0305`-ambiguous, and one 48×40 open-air piece gives the level one readable
   stage. The level was authored against the direct `areas[].prefab` binding and
   moved to the pool form only after that binding was found to skip socket
   sealing (friction item 3).
2. **The party are the pallbearers.** The class names (`Pallbearer`,
   `Reed-Piper`, `Grave-Child`) put the players inside the rite rather than
   beside it, which is what motivates a *stranger* holding the family's word —
   the fork's premise.
3. **Zero combat, and therefore no declared `difficulty`.** A campaign that
   fields no wave ships peaceful by derivation; declaring `peaceful` is refused
   (`DW0468`) and declaring `easy` would be a lie about a level with nothing to
   fight. One plain `set-checkpoint` at the bier, no bonfire — so no class kit
   needs a `flask` and `DW0476` never arises.
4. **The bier is an `armor_stand` actor.** The shrouded body has to be *carried*
   — i.e. moved by `move-actor` — and the dims table (`nav::entity_dims`) carries
   `armor_stand` at 0.6 × 1.8, the same footprint as a player, so the walk plans
   over exactly the corridor a person would use.
5. **Only the bier crosses the fork.** Every other staged body either walks
   before the fork or does not walk at all. That keeps both branches to one
   objective and one sequence each, as the brief asks, and it isolates the
   per-branch staging to a single walker whose behaviour is easy to read in the
   chronicle.

## Branch chronicle review (spec-0025 §4) — citation table

Read per branch, end to end, in one pass, against `DESIGN.md` and against the
dialogue reachable under that branch's flags. Line numbers cite
`out/validation/branch-chronicle-<branch>.md` **of the shipped build**. The
review was re-run against the rebuilt chronicles after every round of fixes; the
rows below are the state after the last one, each naming the original defect. The
chronicle line NUMBERS never moved across the rounds — only two subjects did,
when the ground branch's destination anchor changed (`anchor/l0-barrow-1` →
`anchor/l0-reward`, friction item 11).

| branch | claim reviewed (dialogue / design beat) | chronicle line(s) | verdict |
|---|---|---|---|
| `branch/ground` | design: the wake assembles behind the party as the bell tolls | 3–7 `arrives` ×5 | cleared |
| `branch/ground` | design: three concurrent walkers converge during the rite | 11, 12, 13 `arrives` | cleared |
| `branch/ground` | Hallis: "You said the ground. Thank you." | 15 `learns`, entry option #8 | cleared |
| `branch/ground` | Sedge: "Ground, then. … the cut is at the west end of the row, where I was standing when you came up." | 13 `arrives` (her move off the cut), 17 `arrives` `anchor/l0-reward` | cleared |
| `branch/ground` | Sedge: "I will close it at first light and it will be level by noon." | 19 `departs`, 20 `seals` | cleared — off-screen, after the last dated beat |
| `branch/ground` | Sedge (as first written): "I will come down behind you with the spade" | — | **FINDING (fixed)** — no chronicle line moves `npc/sedge` after 13; the ledger promised a walk the staging never performs |
| `branch/ground` | narration (as first written): "Sedge takes the first spadeful" | — | **FINDING (fixed)** — same defect, in narration rather than dialogue |
| `branch/ground` | Hallis (as first written): "watch the lamp go west" | 11 only | **FINDING (fixed)** — the lamp-bearer's only move is pre-fork and ends beside the bier; it is the bier that goes west |
| `branch/ground` | Hallis: "I will come to the edge of the fire and watch you carry her west." | 17, 18 `arrives` | cleared |
| `branch/ground` | cast: Sedge "at the head of the row … watching the plank go west to the cut she opened" | 13, 18 | cleared |
| `branch/ground` | cast (`quest/the-tide`, ground placement, as first written): Sedge "filling the cut back in behind the party" | — | **FINDING (fixed)** — she is at the row's head, seven blocks from the cut, and never moves again |
| `branch/ground` | ending: art title **THE GROUND**, "the field will be level again, and it will keep her" | 20 `seals` `anchor/l0-reward` | cleared |
| `branch/tide` | design: identical opening through the fork (shared prologue) | 1–15 | cleared — byte-identical to the ground chronicle, as the design intends |
| `branch/tide` | Hallis: "You said the water. She would have said the water." | 15 `learns`, entry option #9 | cleared |
| `branch/tide` | Sedge: "Water, then. I do not walk to the water." | 16–20 contain no beat naming `npc/sedge` | cleared — the *absence* is what licenses the line |
| `branch/tide` | Sedge: "The cut stays open tonight and I will fill it in the morning, empty." | 16–20 contain no `seals` on `anchor/l0-reward` | cleared |
| `branch/tide` | cast: Sedge "watching the plank go south with the spade still planted where she left it" | 13, 17 | cleared |
| `branch/tide` | Hallis (as first written): "banking the fire and coming down with you … not stopping at the edge of it" | — | **FINDING (fixed)** — no chronicle line on any branch moves `npc/hallis`; his cast pins him at the shore fire |
| `branch/tide` | Hallis: "I am banking the fire and I will watch from it until the ebb has her. That is as far down as I get." | 18, 19 | cleared |
| `branch/tide` | narration: "They wade her out to the line and let go." | 18 `arrives`, 19 `departs` | cleared |
| `branch/tide` | ending: art title **THE TIDE**, "the field … keeps nothing of her" | 20 `loses` | cleared |
| both | cross-branch exclusivity: `dlg/sedge-ground` / `dlg/hallis-ground` are unreachable on `branch/tide` and vice versa | per-branch cast gates; `DW0484` green | cleared |

All four findings were the same class — **the ledger moved and the bodies did
not** — which is exactly the defect spec-0025 exists to surface, and none of
them was visible to any compiler check. Each was fixed by making the text match
the staging (nobody follows the bier; the field watches it go), not by adding
staging the design did not ask for.

## Visual review (spec-0003 visual tier)

`delve-render fidelity-gate` PASSED (no missing-texture placeholder), and the
per-piece Nucleation set for `tk-barrow-field` was rendered with the pinned
1.21.11 client jar; the two storybook images in `media/` come from it. Every
dolly segment of all three cutscenes was rendered start / mid / end with
`delvec snapshot --camera` against the camera keyframes the build actually
emits, plus the `spawn`, `npc/*` and POV shots of `render-plan.json`.

Outcomes:

- **establishing crane** — start frames the whole field from above the water,
  lands centred on the banner with the barrows left and right. Good.
- **`insert` on the bier** — originally framed a solid barrow face; fixed with
  `bearing: 90` (friction item 6) and now frames the bier at the foot of the
  black banner.
- **`side-track` on the lamp-bearer** and **`locked-off` / `side-track` on the
  bier** — subjects framed, cameras in open air, no clipping.
- **north socket** — the `minecraft:jigsaw` marker and the hole to the ocean
  (friction item 3) were found here and are gone in the shipped binding.
- **Accepted deviation:** `pov/leg0/wp7` (arriving at `anchor/l0-banner`) fails
  its generic third expectation, "the way ahead is open — no wall or block
  clipping the near camera": the banner post stands one cell east of the
  objective anchor and fills that frame. This is deliberate staging — the bier
  lies *under* the black banner, which is the level's central image — and the
  objective completes at `radius: 3`, so a player never has to stand in the
  post. Recorded rather than fixed; moving the anchor would move the picture.

## Toolchain friction

Recorded here because `docs/demo-levels.md` says polishing levels is the driver
for toolchain improvement: friction found on a demo level is toolchain work.
Ordered by severity.

1. **`compiler::flow` reaches dialogue only from a tree's `root`, never from a
   cast-ledger root** — the sharpest finding, and a soundness gap rather than an
   inconvenience. This campaign's fork node is served to the player by the
   spec-0020 ledger (`cast[npc/hallis].dialogue = "dlg/hallis-word"`), which
   `DW0120` treats as a first-class entry point. The branch-flow world
   enumeration does not, so no enumerated world set either fork flag and BOTH
   branches failed `DW0482` "is NOT REACHABLE". The message's prescription —
   *"give the fork a dialogue option (or a beat) that really sets this branch's
   flags"* — is actively misleading: the options did set them. Worse, the same
   blindness means a fork flag reached only through a ledger root is invisible to
   `DW0480`/`DW0484` too, so the gap can hide a fork instead of merely reporting
   one. Worked around with two always-set progress flags and two flag-gated
   `next` edges from the tree roots (see `DESIGN.md`); those edges are dead in
   play and should be deleted when the model is fixed.
2. **`move-actor` origin chaining is blind to branch exclusivity.**
   `nav::plan_actor_moves` chains each actor's successive move origins in
   campaign document order. `actor/bier` is redirected by the fork, so its two
   legs are treated as consecutive rather than exclusive. Emitted evidence from
   this build:
   - `ma_tick_bier_l0_reward` (ground) frame 0 → `22.5 63.0 14.5` — the banner,
     correct.
   - `ma_tick_bier_l0_tide_line` (tide) frame 0 → `12.5 63.0 20.5` — that is
     `anchor/l0-reward`, **the ground branch's grave**.
   On `branch/tide` the bier is standing at the banner when the driver starts, so
   its first tick teleports it ~11.7 blocks across the field and it then walks to
   the water from the wrong place. No diagnostic fires — every proof is green,
   because a path exists from there too. The design was deliberately NOT bent
   around this (debug doctrine). Prescription: plan each leg from the origin its
   own branch leaves the body at.
3. **A single-`prefab` area does not seal its unmated connectors.** With
   `areas[].prefab: "prefab/tk-barrow-field"` the piece's north socket shipped
   **open to the ocean with the prefab's `minecraft:jigsaw` marker block standing
   in the gap** — in plain sight from the party's spawn and framed by the
   establishing crane. Binding the identical piece as `prefab_pool` +
   `pieces {min: 1, max: 1}` seals the same socket into a stone panel. Nothing
   diagnosed it; only a rendered frame did. This campaign now uses the pool
   binding.
4. **The tidal-keep tileset is not on the content repo's `main`.** It was
   introduced *inside* campaign PR #14 rather than as its own prefab PR — unlike
   the cave, island and hero sets, which landed as prefab PRs (#6–#12) and are on
   `main`. A campaign branched from `main` therefore cannot use the tileset a
   shipped campaign is built on. This cost a whole authoring pass. It is also why
   this PR is stacked on `campaign/the-drowned-bell` instead of `main`
   (see below). Prescription: land tilesets as their own prefab PRs.
5. **`DW0142` misdiagnoses a missing prefab as ten missing anchors.** With the
   bound prefab absent from the library, the build reported
   `anchor … is not provided by any area's prefab` once per actor anchor,
   `move-actor` destination and `loot` anchor — and, oddly, *not* for stage-2 NPC
   anchors or `reach-anchor` objectives, which resolved silently. It reads as a
   per-anchor content error and sent the dev pass hunting for wrong anchor names.
   Prescription: a distinct diagnostic when `areas[].prefab` / `prefab_pool`
   names something the library does not carry, raised once.
6. **`DW0308` proves the corridor, not the composition** — a known limit, with a
   fresh instance worth recording. The `insert` shot on the bier was fully green
   and framed a grey barrow face filling the frame, because the style's default
   bearing seats the camera on the side a mound happens to occupy. Fixed with
   `bearing: 90`. Rendering start/mid/end of every dolly segment is the only
   thing that caught it, exactly as the skill says.
7. **`DW0180`'s prescription offers deleting the requirement as an equal
   option.** "…add the sidecar, **or remove `zh-cn` from `world.languages`**".
   The mechanical pass took the cheap half and dropped the declared language, so
   the campaign quietly stopped being bilingual. Both halves are legitimate, but
   the second silently discards a product requirement; worth wording so that
   removing a declared language reads as the deliberate act it is.
8. **The harness gives an ending 15 s, and an authored ending cinematic can be
   longer.** `branch/tide` came back red on the first full ladder pass with
   `step 6 (assert-complete) failed: campaign not complete after 15000ms … objectives completed: obj/greet, obj/come-up, obj/hear-the-rite, obj/bring-the-word, obj/to-the-water`
   — every objective done, the delve simply had not *finished* yet, because the
   tide ending's `campaign-complete` sits at `at_ticks: 340` (17 s) of the
   closing `sequence`. `branch/ground` passed only because its ending sat at 300
   ticks (15.0 s), i.e. on the boundary. The harness already models
   `cutscene_seconds` from the critical path, but it has no notion of a
   `sequence` tail after the last objective, so a staging-heavy delve — exactly
   the kind this demo exists to showcase — fails for pacing rather than for
   correctness. Fixed here by tightening both endings (ground 240 ticks / 12 s,
   tide 250 ticks / 12.5 s), which is a real pacing improvement on a 15-minute
   level and not a check being weakened. Prescription: derive the
   assert-complete window from the authored tail of the final objective's
   effects, the way cutscene seconds are already derived.
9. **Worktree bootstrap is undocumented.** `delvec` defaults `--prefabs` to
   `campaigns/prefabs`, but `campaigns/` is an untracked symlink to the content
   repo root — so a fresh engine worktree has none, and the campaign path is the
   easily-missed `campaigns/campaigns/<id>`. `delvewright.local.toml` is
   gitignored too, so i18n config does not follow a worktree either. One line in
   the skill (or a bootstrap check in `delvec`) would save the next session the
   same detour.
10. **The generated `campaign` PackTest cannot express a scheduled ending —
   ESCALATED, not patched around.** The compiler emits
   `packtest-datapack/data/the-wake/test/campaign.mcfunction`, which drives every
   `complete_o_*` and then asserts, **in the same tick**:

   ```
   execute as @a[tag=dw_t_camp,limit=1] run function the-wake:complete_o_to_the_water
   assert score #party dw.campaign matches 1
   ```

   The Wake's `campaign-complete` is nested in the closing `sequence` at
   `at_ticks: 240` (ground) / `250` (tide), so the assert at tick 0 is
   **structurally unreachable** and the test fails
   `Expected #party dw.campaign to match 1, but got 0 on tick 0`. The compiler
   emitted both halves: it scheduled the ending and then generated a test that
   assumes the ending is synchronous. spec-0025 explicitly blesses
   `campaign-complete` "at any nesting depth" (`DW0481`), and both shipped
   campaigns — `hollow-vigil` and `the-drowned-bell` — fire it directly from
   `on_complete`, which is why no build has ever exercised this. The template
   knows the offset (it is in the same emission pass), and PackTest supports
   multi-tick templates, so the fix is to await the deepest scheduled offset
   before asserting. A second, smaller defect in the same template: it drives
   BOTH branches' terminal objectives (`to_the_cut` **and** `to_the_water`) in
   one tick, a state no playthrough can reach — the template does not model
   branches at all. **Not worked around here**: moving `campaign-complete` out of
   the sequence would fire the completion fanfare while the body is still being
   carried, which is worse content and would move the chronicle's last line off
   the beat the design puts it on.
11. **A branch's route is flow-proven, not nav-proven — and it cost a red.**
   `branch/ground` failed the branch run with
   `step 5 (reach) failed: reach anchor/l0-barrow-1: objective obj/to-the-cut did not complete within 30000ms … bot at [14.4, 63.0, 17.6]`.
   Root cause is content, found by rendering the approach:
   `anchor/l0-barrow-1` is a **recessed grave niche cut into the side of a barrow
   mound**, not open ground — the bot reached the right column and stopped one
   cell outside the objective's fixed 3×3×3 completion box. Two things made it
   expensive to find: (a) `reach-anchor`'s `radius` is documented as ignored
   (completion is a fixed 3×3×3 box), so authoring `radius: 3` bought no
   tolerance; (b) `DW0311` only walks the **exported** critical path, which for
   this campaign is the tide branch, so the ground branch's route was never
   geometry-checked at compile time — exactly the "known gap" in
   `docs/reference/compiler.md` §DW048x. The branch-run report says so out loud
   (`branch branch/ground walked without the compiler's waypoint artifact … per-branch waypoints are a compiler follow-up`),
   which is the two-layer split working, but the static layer should own it.
   Fixed in content by moving both the objective and the bier's destination to
   `anchor/l0-reward`, open flat ground with a wide approach from the south and
   east (verified by render before changing anything).
12. **Minor**: the queued brief named an `i18n --reflect` flow;
   `tools/i18n-translate.py` has no `--reflect` flag, and
   `DELVEWRIGHT_I18N_API_KEY` was unset in this environment, so the documented
   fallback applied and the `zh-cn` sidecar was translated in-agent from the
   finished English (`docs/reference/i18n.md`, "Fallback rule"). The three art
   titles stay ASCII in the sidecar deliberately — the `delve:art` banner font is
   glyph-checked (`DW0328`) and carries no Han glyphs.

## PR base — read this first

This branch is **stacked on `campaign/the-drowned-bell`** (open content PR #14),
not on `main`, for one reason: friction item 4. `prefab/tk-barrow-field` and
`pool/tidal-keep` exist only on that branch. The campaign diff is this directory
and nothing else. Retarget to `main` once #14 lands.
