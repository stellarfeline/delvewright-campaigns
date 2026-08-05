# Nobody's Cave — Island Remake (authoritative design record)

**v7 — 2026-08-04** (v6: 2026-08-04; v5/v4/v3/v2: 2026-08-03; v1: 2026-08-01). This file is the single
authoritative design document for the `nobodys-cave-island` campaign. Where it
and the stage JSONs disagree, one of the two is a defect.

## 0. Iteration protocol (owner ruling, 2026-08-03)

1. **This file is the design.** Every iteration round updates it in the same
   commit that moves the campaign; `GENERATION.md` stays the round-by-round
   history, this file stays the current state.
2. **Only what was asked changes.** A mechanics fix must not incidentally
   rewrite story, staging, dialogue or balance. Owner-unrequested changes are
   forbidden.
3. **Every round ends with a conformance review**: the current
   `quests/dialogue/npcs/world-edits` JSON is diffed against this file beat by
   beat. A deviation traceable to an owner request is folded in here; a
   deviation with no owner request is reported to the owner, never silently
   kept and never silently restored.
4. Open, unresolved deviations live in §7 until the owner rules on them.

## 1. The island (layout — one contiguous play area, one ending set piece)

The island is ONE contiguous walk with no inter-area teleports inside it. Round 14
adds a second area, `area/open-sea` (`prefab/island-galley`), used only by the
ending: boarding at the strand transports the party to its deck. No filler corridors: every space serves a story beat
or a sightline. Walk-through order (south → north, rising):

1. **Beach camp** (entry piece, walk plane y=63, sea 62): sand shore; campfire
   ring with log benches; two tents; supply crates; class-selection post.
   **Greek galley** merged into the same prefab, anchored just offshore with a
   gangplank — the escape-promise seen from minute one (DESIGN v1 §5 reserved
   this merge: the DSL has no scenery-offset mechanism and areas sit 256 blocks
   apart, so "just offshore" is only achievable inside one piece).
2. **Greenfield** (two connector pieces, gentle rise): grass, oaks, flowers, a
   worn dirt path; a grazing meadow with a low mossy-cobble **sheep fold**
   (5×5, one gate gap; 3×3 interior) — foreshadowing, empty until the end.
3. **Mountain** (large terminal piece): grass-to-stone switchbacks up the face
   to the cave-mouth ledge; the boulder gate at the mouth, a decorative
   Chekhov boulder on the ledge beside it.
4. **Cavern** (mountain interior): one tall wide hall. Cheese racks near the
   entry, the walled **hearth** and the central fire pit, a rock-shelf **ramp**
   (no ladders) to the upper **sheep pen** (9×6 oak fence, gate on the south
   side, 7×4 interior), four shadow alcoves, two ceiling light shafts.

World: `horizon: "ocean"` (sea 62), `boundary` margin 16, start `time: noon`,
`weather: clear`, area `mitigation: "night-vision"` — the hall stays physically
dark and the party is given the sight to move in it (engine #114; the darkness
is never relit away).

**Landscape script** (`world-edits.json`, 9 batches, rounds 8–9): the box-garden
void-safety berms are cut back to the meadow datum and inverted into banks that
fall below the waterline; both banks get rock outcrops and a sparse outboard
treeline; the massif gets a four-ring stepped skirt and an undulating crown; the
shoreline grades into the sea in sand and gravel; the beach-greenfield seam and
its twin at the inner piece seam are levelled. The path spine is protected
structurally (every morph region's y-floor is the walk plane) and declared
keep-clear for every scatter.

## 2. Dramaturgy (beats → mechanics)

- **B0 Beach**: crew mannequins around the campfire; class selection + named
  kit; Eurylochus sets the premise. A 3-drowned wave stumbles out of the surf
  as a gear tutorial (leather caps, not a clock change, keep them alive —
  owner ruling round 5; **the cut is to `dusk`**, not night — round 13, engine
  #204 — and is drama only). **The wine of Maron
  is issued to the whole party at the end of the quest**, never as a class kit
  item — no class can soft-lock the wine beat (owner finding, round 3).
  Antiphos shoulders the provisions and **climbs with the party**; Elpenor
  holds the beach alone (round 6).
- **B1 Follow**: Eurylochus `move-npc`-walks beach → mouth; the player follows.
- **B2 Cavern entry — CHECKPOINT 1**. Perimedes enters at the party's heel and
  posts up in the recess by the racks. The cheese is a **collect** objective —
  take a wheel from the barrel among the racks (owner ruling, round 4/5), not
  an interact marker. **Choice dialogue**: *take the cheese and run* →
  Ending B route (walk back down, board at the gangplank) vs *wait for the
  owner of this cave*, which hides Eurylochus in the alcove beside the player.
- **B3 The giant comes home** — a **40-second, six-shot cinematic**, pure
  observation: no stealth clock, no fail state, no frozen player (owner
  ruling, round 6 — "a cutscene is pure observation"). Order is **cross, then
  seal** (round 11): every gate-crossing walk is provably arrived long before
  the stone comes down. The herdsman walks meadow → mouth (t80, arrives t368),
  roars in the doorway, **takes Antiphos on camera** (t380), walks the hall and
  settles at the fire (t521), handing off to the dialogue statue on arrival.
  The flock crosses the mouth inside shot 4 (t490–564) and is **in the upper
  pen** by t815. The stone comes across at **t880**. Shots: high meadow
  establish over the fold and ocean; dolly to the mouth; the mouth close-up for
  the Antiphos beat; the reverse angle — interior, looking out through the gap
  at daylight, sea and the galley's mast, flock silhouetted coming in; the
  giant settling at his fire; the stone, close. **CHECKPOINT 2** at the
  aftermath; its `on_respawn` clears every giant stand-in and re-seats the
  dialogue statue at his fire.
- **B4 Trapped**: the boulder answers a strike with "it will not move".
  Dialogue with Polyphemus: the wine gift (gated on being sealed in), the
  **name** — Nobody / Odysseus / Aithon — and he sleeps. **Striking the giant,
  awake or asleep, enters combat in earnest** (owner ruling, rounds 10–11):
  the statue despawns and a **vanilla-stat warden** is unleashed on the
  striker. The starting kits do not beat a warden; the player dies, and
  checkpoint 2 restores the scene exactly as it was. Losing quickly is how the
  unwinnable fight is marked.
- **B5 The eye — CHECKPOINT 3**: grind the olive stake under the west light
  shaft, char it at the **walled hearth** (the hall's one true fire — round
  11), and put it in the eye at `anchor/eye` beside the sleeping body.
  **The stake must be IN HAND** (owner ruling, round 13; engine #205 made
  `interact.requires_item` mean mainhand-held): a stake in the pack is not a
  stake in the eye, so the backpack-blinding path is impossible by
  construction. A click that arrives without it narrates a
  `missing_item_hint` — a sleep-murmur in the giant's own register, never a
  UI line; `obj/grind` carries one too. Then
  the neighbours answer from the hills, in **three variants keyed to the name
  the player gave** (nobody / boast / lie) — the campaign's real branch.
  The blinded giant is a **real unleashed vanilla warden** with ancient-city
  behaviour, not a scripted patrol (owner design, round 11): no attribute
  overrides, no waypoints, and he roams. The stealth beat is
  alcove-3 / alcove-4 / ramp-top with `grace_ticks: 260` — sized to the
  measured sneak time of the route, not guessed (rounds 7 and 10). Being
  caught no longer damages: the warden is the killer, the narrate and the
  heartbeat are the warning. **Pacing** (round 16, superseding round 13's
  reading grace): the blinded body is spawned inert at t0 and the neighbours
  answer over it; the title lands, the roar goes up, `unleash-actor` fires and
  the stealth session arms **in that same tick — t0, no gap at all**. Round 13 held those at
  t400/t460 so the scene could be read first; the owner's ruling is that this
  beat gets **no pause whatsoever** — 这个地方不要空场 — because the giant
  visibly standing up blind *is* the signal (§10 item 1). (`DW0355` is
  unmoved by this — the proof measures from the objective anchor whatever the
  sequence does, and it stays green either way.)
- **B6 Escape**: right-click the ram at the pen → finale sequence. The stone
  opens; the giant appears **beside** the gap he holds open (`anchor/mouth-side`)
  and never in it (round 11) — standing inside the hall, west of the gap's
  throat, clear of the rock and **2 blocks off the flock's lane**, so every
  back passes under his hands (round 12: the anchor was inside the mouth wall
  until `DW0450` proved it); the whole flock streams out past him, staggered,
  and settles **in the meadow fold** (round 12); Perimedes goes out with the
  flock in the same stagger and keeps going down to the strand — the belly-wool
  talk window and its doubling-back were deleted in round 14 (§8 item 5), so he
  leaves once and does not come back in; Eurylochus goes to the gangplank; day
  returns and the weather clears on the shore. Board, and **Ending A**.
  **Pacing** (round 13's grace, trimmed in round 16): the stone and its
  narration land at t0, the giant takes his place beside the gap at **t80**
  (was t100) with the second half of the narration, the roar at t160, and the
  flock begins to stream at t200, staggered 200/230/260/290. The flock still
  does not leave before the party can read — but no single gap now exceeds the
  four-second ceiling (§10 item 1).
- **Endings**: A "escaped as Nobody" / B "took the cheese and sailed". Plain
  fullscreen titles — en NOBODY / THE QUIET SAIL, zh 无人 / 悄然扬帆 — each with
  its own sound sting and `campaign-complete` (owner ruling, round 4/5: no
  pixel-art banner; the art font stays an unused engine capability).
  **Ending A's closing paragraph branches three ways on the name given over
  the wine** (owner ruling, round 13), each paying off its own neighbour
  scene: `flag/name-nobody` — the trick's quiet satisfaction, the neighbours
  gone back to their fires believing a sickness took him, and nobody ashore
  who will ever hear it; `flag/name-boast` — the mountain awake and every
  cousin coming at first light, so you leave before the help you summoned
  arrives, and the water will send the bill; `flag/name-lie` — the hills
  weighed "a Cretan" and went back to sleep, so the best hour of your life
  belongs to a man who does not exist. The title stays NOBODY: it names the
  ending, not the answer.

## 3. Cast

NPCs: **Eurylochus** (guide; survives to the gangplank), **Perimedes**
(deferred; enters at the party's heel, witnesses the grab, escapes with the
party), **Polyphemus** (deferred dialogue statue at `anchor/fire-side`),
**Antiphos** (climbs with the party and is taken on camera — the death beat),
**Elpenor** (holds the beach). All mannequin-skinned except the giant.

Actors: `polyphemus-herdsman` (the entrance walk only), `polyphemus-walker`
(the mouth-side stand at the escape), `polyphemus-roused` (unleashed by either
strike), `polyphemus-blinded` (unleashed after the eye) — four spawn sites, one
character; one actor with two spawn sites was the round-6 inside-out bug's
enabling condition. Eight **sheep**: four already penned, four herded home.

**The scene ledger (round 13, spec-0020, `dsl_version` 0.7.0)**. Every quest
carries a `cast` block naming, for all five NPCs, where they stand, what their
business is in that beat, and what a right-click offers: 9 quests × 5 NPCs = 45
entries, 43 of them per-branch lists (`DW0462` is campaign-global, and the
flee/wait fork moves four of the five, so every quest declares both branches —
the wait/pre-fork line gated `forbids flag/flee`, the flee line `requires
flag/flee`). 27 bark pools, 69 bark lines. Zero `DW0467`.

**The dialogue follows the story.** Each NPC's right-click advances instead of
looping one tree:

| NPC | scenes, in order |
|-----|------------------|
| Eurylochus | `dlg/root` (beach premise) → `dlg/at-the-racks` (the cheese argument, moved off the beach root) → hushed alcove barks → pen barks → `dlg/at-the-gangplank` (survivor: counting heads, Antiphos, "I'll do my grieving at the oar") |
| Perimedes | `dlg/just-arrived` (in at the heel with the wine-skin) → `dlg/root` (the premise: "Tell me what he is") → `dlg/after-the-eye` (gated on `flag/blinded` — the premise questions are gone the moment the eye is out) → `dlg/under-the-ram` (carries the escape option) → `dlg/on-the-sand` (survivor: two fists of wool, "tell me four is right") |
| Polyphemus | `dlg/guest` → sleep-murmur barks the instant `flag/asleep` is set (the awake tree is unreachable because the ledger says so, not because a flag was remembered) → `dead` |
| Antiphos | `dlg/root` (beach) → `dlg/at-the-mouth` (the pens, the bed, the last scene before he is taken) → `dead` |
| Elpenor | `dlg/root` → alone-at-the-fire barks for the whole cave act → `dlg/the-fire-held` on the return ("Where is Antiphos, Captain.") |

Barks print as `<Name>: <line>` in italics, so every pool is **speech**, never
narration — which is also why the sleeping giant's pool is sleep-talk and sets
up B5's `missing_item_hint` in the same register.

**Flock staging (round 12, owner finding; round-13 restore)**: every sheep position, at every
moment of the campaign, is a distinct cell **inside the upper pen** or **at the
meadow fold** — never the open cavern floor, never the open meadow. The pen
carries one anchor per sheep (`anchor/pen`, `pen-d`…`pen-j`) plus two crew
stands (`pen-b`, `pen-c`, kept 2+ blocks off the ram so they never shadow its
affordance); the fold carries one anchor per sheep (`anchor/fold`,
`fold-b`…`fold-h`) — **all eight now inside the walls**, on eight of the nine
interior cells, since round 13 un-buried the fold's west interior column
(`batch/fold-clear` + fold keep-clear envelopes; `fold-g`/`fold-h` moved from
the gate row to piece-local x=3). The herd walks in from the
fold **straight to the pen** in one leg — it never parks on the hall floor —
and walks out to the fold in one leg at the escape.

## 4. Feature surface actually used

one class (Odysseus — round 14: this is his story, and there is no one else to be) + named kit · mannequin skins · dialogue flags + gated options · two
endings, the first of them branching three ways on the name · **the stage-5
`cast` scene ledger with per-branch placements and bark pools (DSL 0.7)** ·
**`interact.missing_item_hint` over held-item `requires_item`** ·
narrate chat/title/subtitle · give-item named · collect / interact /
reach / talk-to / kill objectives · props (grindstone) · triggers strike and
strike-npc · a tutorial wave with attributes + equipment · unwinnable combat by
`unleash-actor` · `move-actor` / `move-npc` with `on_arrive` · `sequence`
timelines · a six-shot spectator cinematic with `look_at` · set-time /
set-weather cuts · `close-gate` / `open-gate` · checkpoints ×3 with distinct
`on_respawn` resets · ocean horizon + boundary · area `night-vision`
mitigation · positional sounds · stealth zones · full en + zh-cn l10n (312
keys) · the stage-7 world-edit script.

## 5. Prefab contract

| Piece | Kind | Anchors |
|-------|------|---------|
| `island-beach-camp` | entry (galley merged) | `entry`, `camp-fire`, `class-post`, `crew-a`, `crew-b`, `surf-wave`, `gangplank`, `deck`, `prow` |
| `island-greenfield` / `-bend` | connector ×2 | `meadow`, `fold`, `fold-b`…`fold-h` |
| `island-mountain` | large terminal (shell + cavern) | `mouth`, `mouth-side`, `boulder` (gate region), `cheese-store`, `fire-pit`, `fire-side`, `hearth`, `eye`, `ramp-top`, `pen`, `pen-b`…`pen-j`, `alcove-1..4`, `checkpoint-1..3`, `shaft-1..2` |

Rules: sockets per the island tileset conventions; gravity floors get
substrate; palette from the admitted allowlist; no long corridors — traversal
is scenery. Deterministic generators, provenance metadata, DW07xx-clean
admission. **Outdoor NPC destinations must be piece-unique** — the greenfield
is placed twice, so `meadow`/`fold` names resolve to one arbitrary carrier and
a top-level `move-npc` to either is a hard `DW0305`; only actor spawns and
`move-actor` targets may use them.

## 6. Delivery

Campaign id `nobodys-cave-island`, content repo, branch
`campaign/nobodys-cave-island`. Full ladder green (build + PackTest + bot)
before any round is handed to the owner. The v0.4 corridor original was
retired permanently (owner ruling, round 5).

## 7. Open deviations (pending owner ruling)

Round 12's list, carried forward with round-13 dispositions.

**Closed in round 13** (owner-ruled, folded into the body above): the dusk cut
(old #5, engine #204), the buried fold column (old #8 — `batch/fold-clear`
plus fold keep-clear envelopes on the three seeded batches; all eight sheep now
stand inside the walls).

**Still open, not changed either way:**

1. **B1 is one leg, not a scenic chain.** v1 designed a reach-anchor chain
   along the beach → meadow → slope → mouth walk; the campaign has a single
   `reach-anchor` to the mouth, because `anchor/meadow` and `anchor/fold` are
   defined by both placed greenfield pieces and any *required* reference to
   them is `DW0305`. **Owner ruling, round 13: this stays as it is** (洞穴外部
   到达就行) — the scenic chain is not to be built.
2. **The cheese has no name, and is not the barrel** (round-13 STOP). The
   owner asked for the collect target to become the cave's existing empty
   barrel, filled 27 × 64 with a named "Kefalotyri Cheese". It cannot be
   expressed: `collect` **places its own container** — at objective activation
   it emits `setblock <anchor> minecraft:chest` followed by `item replace block
   … container.0 with <item> <count>`. Pointed at the barrel's cell that
   overwrites the barrel and destroys the `loot[]` fill that `setup_finish`
   already put in it; pointed anywhere else it stands a spurious chest beside
   the barrel. `Objective::Collect` also has no `name` field. The *counting*
   half would work unchanged (the completion guards match on item **id**, so a
   renamed stack still counts). Needs engine work: a way for `collect` to adopt
   a container the prefab already placed instead of stamping one, and a
   `cheese-store`-adjacent anchor on an actual barrel cell (the current
   `anchor/cheese-store` is the walk cell in front of the shelf, not a barrel).
3. **Four sheep are herded in, four were already penned.** v1 said the flock
   of eight is herded in; the pre-penned four match the fiction the dialogue
   established ("lambs penned and sorted by age") and have shipped since
   round 1.
4. **The boulder hint is still strike-only** (round-13 STOP). The owner asked
   for right-click to produce the same hint. The compiler **accepts** a
   co-located `use` trigger on `anchor/boulder` and builds green — and that is
   the problem: `env_trigger_setup` then summons a *second* `minecraft:
   interaction` at the identical cell (verified: two summons at `8.5 69.0
   -44.5`). The compiler's own source documents the consequence (`emit.rs`,
   "one cell, one hitbox"): an exact ray-pick tie resolves to whichever entity
   the client iterates first, so one of the two triggers receives every click
   and the other never fires. Whichever ordering is chosen, either the existing
   left-click hint or the new right-click hint silently dies. Reverted rather
   than shipped. Needs engine work: merge co-located non-NPC click triggers
   onto ONE hitbox carrying both tags (exactly what `npc_hitbox_trigger_tags`
   already does for `strike-npc`), plus a diagnostic so the silent version can
   never ship again.
5. **No Eurylochus walker twin.** v1 designed an actor twin for scripted
   walks; `move-npc` became a first-class primitive and the twin is
   unnecessary.
6. **Antiphos dies, not Eurylochus.** v1 had the giant kill Eurylochus; the
   round-6 restage moved the death to Antiphos so the victim is a man who
   climbed with the party on camera. Logged in an owner round, but the swap
   itself is not separately attributed to an owner request.
7. **Two bridge options exist for a proof, not for a player** (round-13, new).
   `dsl::validate` seeds dialogue reachability from the tree root **plus every
   cast-ledger root** (spec-0020, so retiring a premise root cannot orphan its
   successor), but `compiler::flow` — which powers `DW0203` — still seeds from
   the tree root alone. Moving `obj/the-argument`'s and `obj/hold-fast`'s
   completing options onto the later scenes therefore reads as "no reachable
   option completes this objective". Each retired root keeps one in-fiction
   option through to its successor ("About that cheese in your arms.",
   requires `flag/cheese-taken`; "You have hold of a ram. So have I.", requires
   `flag/aboard`), gated so it can never be offered in the wrong beat. They are
   real lines and do no harm, but they exist because of the drift and should be
   deleted when `flow.rs` learns about cast roots.
   **Round-16 correction**: only one of the two still exists. The ram option
   went out with `obj/hold-fast` in round 14 (§8 item 5), and since round 15 the
   cheese option's sentence is its `tooltip` rather than its label — so the
   deletion this item anticipates is now a single option, not a pair.
8. **Four DW0451 at-rest advisories remain, and sixteen walked ones.** The
   sixteen are all one cell — the upper pen's fence gate, which every body that
   enters or leaves the pen must pass through. Of the at-rest four, three are
   warden bodies at `anchor/fire-side` / `anchor/fire-pit` (moving them
   restages the blind beat and the `anchor/eye` relationship, which also
   carries the two long-standing `DW0359`), and one is a sheep flush against
   the fold's north wall — unavoidable now that eight sheep occupy eight of the
   fold's nine interior cells, of which only the centre is clear of every wall.
   Round 13 took the one cheap nudge that existed (`actor/sheep-7` moved to the
   freed west column), 21 → 20.

## 8. Round-14 amendments

1. **One class.** `class/odysseus` only (owner ruling). The blurb absorbs the
   premise the pick used to carry: there is no one else to be on this island.
2. **The flee branch is a real branch, not a truncated one.** Taking the cheese
   and leaving used to strand the fork's own participants: Perimedes despawned
   at the mouth, Eurylochus held a cave nobody was in, and Elpenor mourned
   Antiphos — who never died on that branch. Now the whole party comes down
   (Perimedes to the fire, Eurylochus to the gangplank, Antiphos to the strand
   with the sacks), and three new scenes carry it: `dlg/quiet-sail`,
   `dlg/all-hands`, `dlg/all-of-you`. Mourning is gated to the branch that has a
   death in it. The ledger's flee line is now correct in **every** quest that
   begins on that branch, including the ones only the wait branch can finish.
3. **No dressing on a staircase.** `batch/shore-transition` was dropping eleven
   sand/gravel/stone blocks onto the bottom tread row of the mountain's
   switchback face. The whole stepped face (piece-local x 3–32, z 30–39) is a
   keep-clear envelope; the other three shore rows still grade into the water.
4. **The drowned come for the fire.** The cut is `dusk` at muster for the sunset
   sky, and a `sequence` step advances to `night` 40 ticks later — after the
   wave already exists, because drowned read 12000 as daylight and go back to
   the water, and delaying the *spawn* instead lets a bot clear the beat before
   it happens (round-13 lesson). **Routed lanes are not available here**: `lane`
   is raider-family only (`DW0382`) and drowned are not raiders; `summon:
   aggro-edge` seats them on the standable arc of the ring, which for a fire on
   a beach is *inland*, behind the party. The species-correct fix is the clock.
5. **No belly-wool doubling back.** `obj/hold-fast` and its dialogue option are
   deleted; Perimedes walks out of the pen with the flock and keeps going to the
   strand, instead of leaving and running back in to be talked to.
6. **The giant holds the mouth.** `flag/escaped` arms
   `trigger/he-holds-the-mouth` (approach, range 5, at `anchor/mouth`, once):
   walking back into the cave after the escape unleashes `actor/polyphemus-
   walker`. Telegraphed twice — the `obj/last-sand` narration says he has set
   himself across the mouth and that whatever is still in there is his, and the
   trigger's own title fires before the roar. Optional combat, so the spec-0023
   winnability proofs do not bind it.
7. **The ending is a voyage.** `quest/the-voyage` (finale, `area/open-sea`):
   boarding at the strand transports the party to the galley's deck, three
   mannequin crew actors spawn on it, a two-shot dolly recedes from the ship,
   the sky cuts to night mid-shot, and only then does the `NOBODY` art banner
   land with the branch's closing paragraph and `campaign-complete`.
   **Framing is proven by construction, not by distance**: `area/open-sea` sits
   at x=256 while the island spans x −8…27, so the dolly recedes along −x and
   looks back along +x — the island is a full 180° off the view axis, behind the
   camera at every point of both shots. The ship never moves; the drift is the
   camera. The art font is ASCII-only (`DW0328`), so the banner reads `NOBODY`
   in both languages and the Chinese lands in the line beneath it.

## 9. Round-15 amendment — the button captions, the hover box speaks

`DW0331` (engine #217) makes a dialogue option label wider than 146 font px a
build error: the dialog buttons are a fixed 150 px and anything longer scrolls.
Twenty-five English labels and the two Chinese ones that mirrored them were over
— this campaign's whole option register was written as full sentences.

Owner ruling (2026-08-03): **the caption goes in the button, the full line rides
a `tooltip`** (engine #233, `dialogue` stage at `dsl_version` 0.8.0 — the
narrowest bump that unlocks the field, and it cascades into nothing else).
The rule that governs the rewrite is the one SKILL.md states: **the button must
read on its own**, because fast and controller players never hover. So a caption
is a speech act, not an abbreviation — "We climb.", "Take it and run.",
"You have my word." — and the sentence it replaces survives verbatim in the
hover box.

Two sets are handled as sets rather than per-label, because they are choices the
player compares side by side:

- **The name at the wine** — `Nobody.` / `Odysseus.` / `Aithon.` The campaign's
  one real branch now reads as three parallel answers of the same shape, with
  the Odyssey lines ("My mother calls me Nobody, my father, my friends — all of
  them.") intact on hover.
- **The two ways to offer the wine** — `Wine, off my ship.` from `dlg/guest`
  and `A gift instead: wine.` from `dlg/law`, so the two routes to the same
  node stay distinguishable at a glance.

The Chinese side needed 25 new captions and **no new tooltip translations**: a
tooltip's English is the label's own former text, so the sidecar already carried
that sentence.

## 10. Round-16 amendment — pacing, and the standing findings audit

1. **A pause is never a punishment** (owner ruling, 2026-08-04, campaign-wide).
   A pause inserted so players can read guidance must be **optional**, and where
   a pause exists at all it is **3–4 seconds maximum**. The staging is the
   signal — a giant visibly standing up blind says "go" more clearly than any
   timer, and holding the party still afterwards only means they finish the beat
   before the game admits it started.

   **Two tiers, not one** (owner correction, 2026-08-04). Where the staging
   itself is the signal, the gap is **zero** — the 3–4 s ceiling is for places
   where a reading pause exists at all, and was never a target to aim at. The
   blinding beat is the zero case: its rise, roar, `unleash-actor` and
   `begin-stealth` all fire in the **same tick as the stand-up** (t0/t0, was
   t400/t460 — twenty seconds). The escape beat keeps a real reading pause,
   because the owner asked for one in round 13 by name (the flock left before
   she had finished reading), trimmed from 5 s to **4 s** — at the ceiling, not
   above it. `grace_ticks: 260` is
   untouched — engine #204 guarantees that delaying the arm does not discharge
   `DW0355`, so the escape budget is unchanged and only the standing-still is
   gone.

   Not applied, and why: gaps that run under a cutscene are the cinematic, not a
   pause (the seal beat's t40–t880 sits inside an 860-tick camera); and the seal
   beat's t900→t1000 settling echo carries no text to read, so it is sound
   design rather than reading grace.

   **The optional half has no vanilla primitive.** There is no dismissible
   prompt, so it is stated here as the authoring rule — *never author a timed
   gap whose only purpose is reading time* — rather than faked with a timer that
   pretends to be a choice. If a beat genuinely needs the party to have read
   something before it can fail them, gate it on an action they take, not on a
   clock.

   This supersedes the round-13 reading-grace rule (§7 history, GENERATION
   finding #36), which sized its gaps by feel and over-corrected.

2. **The findings audit is a standing gate.** No build is staged for the owner
   until every prior finding — from round 1, not from the last round — is
   fixed or explicitly deferred by her. The ledger lives in `GENERATION.md`
   under round 16 and is re-run in full every round. It exists because two
   findings (the named cheese and the boulder's right-click, both round 12)
   survived two playtests inside "STOP, needs engine work" notes that nobody
   converted into engine tasks.

3. **Two engine defects are open against this campaign's own staging** and are
   not content bugs: branch-blind walk-origin chaining (the wait branch's
   Eurylochus and Perimedes both teleport to the beach and walk back), and a
   night-vision lease shorter than the ending camera it has to survive. Both are
   root-caused in GENERATION round 16 and carry engine PRs.

## 11. Round-18 amendment — the cheese is the barrel, and every beat says what it does

1. **The cheese is the prefab's own barrel** (owner finding, open since round 12;
   engine task #95). `obj/cheese` adopts `anchor/cheese-barrel` — a **new
   anchor on a real barrel cell** in `island-mountain` (piece-local `[23,9,25]`,
   one of the four barrels the prefab has always had among the racks) — names the
   item **Kefalotyri Cheese** / **克法罗提里干酪**, and pads the barrel with
   `fill_count: 26` so all 27 slots are occupied and it reads full. The compiler
   now places **no chest at all**: the emitted `activate_o_cheese` is 27
   `item replace block` lines into the barrel where it stands, and not one
   `setblock`. The `hint` that has promised "a wheel from the barrel among them"
   since round 4 is finally true.

   **The anchor was added by hand, not by re-export.** `island-mountain`'s
   metadata is mixed-authorship: the generator emits 17 anchors, the file carries
   29. The other 12 — `eye`, `fire-side`, `hearth`, `mouth-side`, `pen-b`…`pen-j`
   and now `cheese-barrel` — were authored across rounds 10–13, and a re-export
   drops exactly those (it did once already, repaired in `830ce14`). The change
   is proven add-only by a semantic diff of the metadata: one anchor added, none
   lost, none moved, every non-anchor section byte-identical.

2. **Every beat declares what it does to the story** (spec-0025). `quests` and
   `dialogue` go to `dsl_version` 0.8.0 and carry **102 `happening`
   declarations** — 97 in `quests.json` (10 quests, 20 objectives, 67 staging /
   gate / ending effects) and 5 on the story-weight dialogue options (the
   flee/wait fork and the three name answers). Written against the B0–B6 beats in
   §2, not generated: the verbs are the closed vocabulary, and the subject names
   the character the beat is *about*.

   Four subjects were wrong on the first pass and were caught by reading the
   chronicle back: `departs` has to be true **of its subject**, so the party
   leaving the beach is not `departs(npc/elpenor)` (he stays), and boarding the
   ship is not `departs(npc/eurylochus)`. Those four now carry no subject,
   because the beat is about the party and the party is not an NPC.

3. **Athena's gift is a real potion.** `classes` goes to 0.8.0 and the Odysseus
   kit gains `minecraft:potion` with `contents: {potion:
   minecraft:long_night_vision}`. Round 3 deleted a *renamed water bottle* that
   granted nothing (#114) and moved the mitigation to the area declaration, where
   it stays and remains the guarantee — together with the round-16 camera lease,
   which is what stops it expiring under the ending. This item is the fiction's
   half of that, and it now actually pours.

4. **No chronicle artifact is emitted yet, and that is a declaration gap, not a
   defect.** The per-branch chronicle is emitted only for a campaign that
   declares stage-4 `branch_points`; this campaign's `quest-plan` is still
   `0.6.0` and declares none. The happenings are written and validated, so the
   input is ready — but turning the chronicle on means bumping stage 4 and
   admitting `DW0480`–`DW0485`, including the exclusive-content-leakage and
   event-contradiction proofs. On a campaign whose one real fork has a death on
   only one side, those will have findings, and findings there need owner
   rulings. Queued as its own round.

## 12. Round-21 amendment — every barrel is cheese, and the island does not let you leave

Three owner findings from the 2026-08-05 playtest plus a same-day staging
directive, one round.

### 12.1 All four barrels carry cheese (task #171)

The cave-of-plenty racks have always held **four** barrels; round 18 named one of
them (`anchor/cheese-barrel`) and filled it, so the other three were furniture the
player opened, found empty, and walked away from. The owner's rule: whichever
barrel you open, you find cheese and you progress.

**The mechanic makes this free.** A `collect` objective adjudicates on **item id**,
not on which container the item came out of — the completion advancement is
vanilla's `inventory_changed` matched on `minecraft:sponge`, and the per-tick
fallback is a held check on the same id. `container` only decides which piece of
furniture the compiler *fills*. So the fix is not an engine change: the other three
barrels get named (`anchor/cheese-barrel-{b,c,d}` on the real barrel cells
`[21,9,25]`, `[21,9,24]`, `[23,9,24]`) and each gets a `loot` entry of 27 stacks of
the same `minecraft:sponge` named **Kefalotyri Cheese** — identical contents,
identical display, 27 occupied slots so each reads as full as the adopted one.
`DW0435` keeps the two fills apart: one anchor, one positional fill, and no barrel
is claimed twice.

**One asymmetry, deliberate and harmless.** A `loot` barrel is filled at
`setup_finish` (world init); the adopted barrel is filled at objective
*activation*. So the three loot barrels are technically openable before
`obj/cheese` activates. They sit two steps past `anchor/checkpoint-1`, whose reach
is what activates the objective, and a wheel pocketed early still completes it via
the held check — so the window is unreachable in practice and non-blocking if
reached.

**Anchors added by hand, add-only** — the same mixed-authorship rule §11 records
for `island-mountain`. The round adds **six** there (three barrels here,
`anchor/mountain-foot` and the two shore anchors in §12.3) and **three** to
`island-beach-camp` (the deck stations in §12.3); none moved, none lost, every
non-anchor section byte-identical. Proven inert for the player: the pre-round
campaign built against the post-round prefabs produces a **byte-identical shipped
`datapack/`** — only the creator overlay's `layout.json` gains the new names.

### 12.2 The flee branch gets the ending cutscene (task #172)

The take-and-run branch used to `campaign-complete` on the deck the instant the
party boarded: no ending shot at all, just a title card. The wait branch has had
a 15-second pull-back since round 4. Owner ruling: **the flee branch gets the
ending cutscene too.**

It now does — `obj/board-flee` narrates the oars going out, plays the same
15-second two-shot pull-back (7 s + 8 s, same offsets, same `look_at`), and lands
the QUIET SAIL card on the same `at_ticks: 340` beat the wait ending uses. The
shot is filmed on the **flee branch's own galley** (`anchor/deck`) rather than the
open-sea one, and it dresses no deck with actors, because on this branch the crew
really are on the sand: the owner's same-day ruling is that the flee ending's
beach-camp staging is correct and stays. The wide pull-back therefore frames the
ship, the strand, the fire and the crew standing at it — which is the peaceful
ending's actual picture.

**Why not literally the wait branch's cutscene function.** It was built that way
first: a `quest/the-quiet-voyage` in `area/open-sea`, triggered off
`quest/take-the-cheese`, reusing `anchor/sea-deck` — and the compiler deduplicated
it onto the *same* emitted `cs_sea_deck_…` function, so it really was one cutscene.
It does not work, for a reason worth recording rather than working around:

- A cross-area camera anchor is legal at emission (`anchor_point_any` scans every
  area), but the layout solver's required-anchor set is per **quest area**, so
  filming `anchor/sea-deck` from a quest declared in `area/island` is `DW0302`.
  Putting the beat in `area/open-sea` fixes that.
- But then the party has to physically be there, and **inter-area transport is
  derived from the exported critical path only** (`plan::build_critical_path`
  walks one playthrough and fills `Plan::transport` from *its* consecutive
  objectives' areas). The exported path is a wait branch, so `complete_o_board_flee`
  emitted no `teleport` while `branch-path-flee.json` — built by the same function
  under `branch_critical_path` — *did* carry a `transport` marker. The datapack
  promised a jump it never performed, and the branch run failed on it exactly
  there: `[transport] did not observe the jump to [260, 65, 11]`.

The DSL has no player-teleport verb, so there is no content-level spelling of "put
the party on the other galley" — by design, since that transport is the
compiler's. Escalated (§12.4); the beat is authored in the form the engine can
actually deliver, and can be upgraded to the shared function the day transport
becomes branch-aware.

### 12.3 The storm-night escape gauntlet (task #175)

The 2026-08-05 playtest proved the pre-cave drowned beat **soft-locked the
mainline**: `obj/surf` was a `kill` gating `obj/climb-out`, which carried the
`move-npc` that put Eurylochus at the mouth, and the quest's `on_complete` carried
Antiphos and `flag/antiphos-posted` — the flag `obj/take-cover` requires. A player
who did not finish the drowned finished nothing after it. **No mainline progression
may depend on optional content**, so the beat is cut rather than repaired:
`obj/surf` and `wave/surf` are gone, `obj/climb-out` now follows `obj/muster`
directly, and the muster beat keeps only the fall of the light. `kill obj/surf` is
gone from `critical-path.json`, which is the machine statement of the cut.

The pressure moves to where it belongs — **the way out**.

**The beat.** `obj/under-ram` opens the stone into `set-time: night` +
`set-weather: thunder`. This is not a licence taken with Homer: a blind man cannot
tell noon from midnight, and Polyphemus puts his flock out at what he takes for
dawn. Poseidon has by now been told what was done to his son, and answers.

**The route is the fight.** `quest/the-sail` gains `obj/the-neck` — reach
`anchor/mountain-foot`, the waist of the island where the sea is genuinely on both
hands — so the escape is a three-surge run rather than a wall at either end:

| Beat | Waves | Where |
|------|-------|-------|
| `obj/the-neck` | `wave/tide-shore-west`, `wave/tide-shore-east` | `anchor/mountain-shore-{west,east}`, the two coasts at the mountain's foot |
| `obj/the-neck` +200t | `wave/tide-west`, `wave/tide-east` | `anchor/crew-a` / `anchor/crew-b`, either side of Elpenor's dead fire |
| `obj/last-sand` | `wave/tide-surf` + a re-fire of both beach waves | `anchor/surf-wave`, between the party and the plank |

**`obj/the-neck` is a choke, not a hope.** A `reach-anchor` completes on a
**3x3x3 box at the anchor cell** — `radius` is vestigial in v0.3+ — so an
`after`-gating reach objective on open ground is a soft-lock waiting to happen,
which is precisely the class of bug this round is fixing. `anchor/mountain-foot`
is at `island-mountain` piece-local `[18,3,40]`, one block north of the jigsaw
seam, and the emitted trigger is `@s[x=9,dx=2,y=62,dy=2,z=-33,dz=2]`. The
greenfield's north face is walled at piece-local `x6` and `x10`, so the only gap
out of the mountain is world `x in 9..11` at world `z=-30` — and a party cannot
enter that cell without first being sampled in the cell behind it, `z=-31`, which
the box covers. Every descent is therefore caught, by geometry rather than by
hope. The mountain's own apron there is thirty blocks wide; putting the anchor
anywhere else on it would have been exactly the trap this round is fixing.

**No `kill` objective names any of them.** Reaching the ship and triggering the
set-sail interaction is the victory; the drowned are pressure, not a checklist.
This is legal by construction — `DW0171` only requires that a *killed* wave be
spawned, never the converse — and it is what keeps the beat a run. Tuning follows
the same rule: `max_health: 8.0`, `attack_damage: 2.0`, `movement_speed: 0.2` —
quicker than the tutorial drowned they replace, still slower than a sprinting
party. Twenty-one bodies over roughly sixty blocks in three surges — six, six,
then nine at the plank — is pressure a 2–3 h delve can carry without becoming a
wall.

**The escape gets its own two checkpoints, and it needs them.** Before this round
the whole descent was covered by `anchor/checkpoint-3`, deep inside the cave —
acceptable when the way out was an empty daylight walk, a soft-lock now that it is
not. The specific trap: `trigger/he-holds-the-mouth` requires `flag/escaped`, which
`obj/last-sand` sets, and it **unleashes the warden** on anyone who comes back
within 5 blocks of `anchor/mouth`. A party that dies during the last push at the
plank would respawn in the cave, walk out through that trigger, meet a real warden
with a starting kit, and die again — a loop, in the campaign's most lethal ninety
seconds. So `obj/the-neck` moves the checkpoint to `anchor/mountain-foot` and
`obj/last-sand` moves it to `anchor/gangplank`, each **before** its own
`spawn-wave`s in the bundle, so a retry costs the beach run rather than the
campaign.

`spawn-wave` is deliberately **not** idempotent — each fire summons a fresh squad —
which is what lets the beach waves re-fire at the plank without a second wave id.

**The crew run it too** (owner directive, same day). Standing on the beach while
Poseidon empties the sea onto it is the immersion break; so `npc/perimedes`,
`npc/eurylochus` and `npc/elpenor` are walked at `speed: 0.28` (sprint pacing
against the `0.15` default) from the cave to **stations aboard** —
`anchor/oar-star`, `anchor/oar-port`, `anchor/helm`, three new anchors on the
beached galley's own deck planks, clear of `anchor/deck` so no body eclipses the
set-sail affordance. `quest/the-sail`'s wait-branch cast declares them there.
Branch-aware move origins (`DW0488`) keep the flee branch's beach staging — which
is correct for the peaceful ending and is unchanged — from bleeding into these
walks.

**Why the surges hang on objectives rather than environment triggers.** The first
spelling used `approach` triggers. Two things were wrong with it. A non-`once`
approach trigger has no edge detection — it fires *every tick* a player is in
range — and a `once` one is still an **ambient beat** the chronicle refuses to
date, so `branch-chronicle-flee.md` reported drowned coming ashore on the branch
where the sea is calm. Hanging every surge on a `quest/the-sail` objective makes
each one branch-dated, orders it in the chronicle, and puts it on the bot's own
path.

### 12.4 Engine findings (for the compiler, not this campaign)

1. **Inter-area transport is not branch-aware.** `Plan::transport` is filled from
   `build_critical_path` over the **exported** playthrough only, while
   `Plan::branch_critical_path` runs the same function per branch and writes a
   `transport` marker into every `branch-path-<b>.json`. A branch whose area
   changes off the exported path therefore ships a path artifact that promises a
   jump the datapack never performs, and its branch run hangs at the discontinuity.
   Either the transport map should be the union over every enumerated branch, or a
   branch path should not claim a transport the emission does not carry. §12.2 is
   the campaign-side consequence.

2. **`plan::wave_area` does not descend into `sequence` steps.** It resolves a
   wave's area from the first quest whose effect list fires its `spawn-wave`, with a
   shallow `.any()` — unlike the wave/flag producer scans elsewhere, which use the
   shared nested traversal. A wave spawned *only* from inside a `sequence`, in a
   multi-area campaign, resolves no area and fails `DW0310` with "its spawn anchor
   is not placed in any assembled area" — while the anchor is in fact placed.
   Every wave here also has a top-level spawn, so the campaign is unaffected.

3. **`pool/island` draws `island-greenfield` twice**; `island-greenfield-bend` is
   never placed. Every greenfield anchor is therefore ambiguous (`DW0305`) and
   unusable as a wave anchor or `reach-anchor` target. The gauntlet's mid-route beat
   sits on the mountain piece for that reason, not by preference. Two shore anchors
   were added to `island-greenfield` on the first attempt and **reverted** when this
   surfaced — the prefab diff carries none of them.

4. **A `loot` container and an adopted `collect` container fill at different
   times** — world init vs objective activation — with no way to say otherwise
   (§12.1).

5. **`DW0461` replays effect history without branch awareness.** An NPC whose walks
   are all ungated is not "branch-divergent" by `continuity`'s test, so `DW0462`
   does not take over; but a walk that only *runs* on one branch still moves them in
   the replay, and the other branch's cast entry is then reported as contradicting a
   position that branch never reaches. Answered here by declaring what the replay
   says (the diagnostic's own prescription), on a quest the flee branch cannot enter.
