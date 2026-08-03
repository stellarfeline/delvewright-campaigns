# Nobody's Cave — Island Remake (authoritative design record)

**v3 — 2026-08-03** (v2: 2026-08-03; v1: 2026-08-01). This file is the single
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

## 1. The island (layout — ONE contiguous area, zero transports)

No inter-area teleports, no filler corridors: every space serves a story beat
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
  heartbeat are the warning. **Reading grace** (round 13): the blinded body
  is spawned inert at t0 and the neighbours answer over it; only at t400 does
  the title land, the roar go up and `unleash-actor` fire, and the stealth
  session arms at t460. The hunt starts after the scene can be read, not
  under the player's feet. (`DW0355` is unmoved by this — the proof measures
  from the objective anchor whatever the sequence does, and it stays green.)
- **B6 Escape**: right-click the ram at the pen → finale sequence. The stone
  opens; the giant appears **beside** the gap he holds open (`anchor/mouth-side`)
  and never in it (round 11) — standing inside the hall, west of the gap's
  throat, clear of the rock and **2 blocks off the flock's lane**, so every
  back passes under his hands (round 12: the anchor was inside the mouth wall
  until `DW0450` proved it); the whole flock streams out past him, staggered,
  and settles **in the meadow fold** (round 12); Perimedes goes out in two hops
  — a stand just inside the mouth that is the talk window, then down to the
  beach; Eurylochus goes to the gangplank; day returns and the weather clears
  on the shore. Board, and **Ending A**.
  **Reading grace** (round 13, the owner's playtest complaint — the flock left
  before she had finished reading): the stone and its narration land at t0, the
  giant takes his place beside the gap at t100 with the second half of the
  narration, the roar at t160, and the flock only begins to stream at t200,
  staggered 200/230/260/290. Ten seconds of reading before anything moves.
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

classes + named kits · mannequin skins · dialogue flags + gated options · two
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
