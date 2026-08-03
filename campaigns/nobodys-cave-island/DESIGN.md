# Nobody's Cave — Island Remake (authoritative design record)

**v2 — 2026-08-03** (v1: 2026-08-01). This file is the single authoritative
design document for the `nobodys-cave-island` campaign. Where it and the stage
JSONs disagree, one of the two is a defect.

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
  owner ruling round 5; the cut to night is drama only). **The wine of Maron
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
  11), and put it in the eye at `anchor/eye` beside the sleeping body. Then
  the neighbours answer from the hills, in **three variants keyed to the name
  the player gave** (nobody / boast / lie) — the campaign's real branch.
  The blinded giant is a **real unleashed vanilla warden** with ancient-city
  behaviour, not a scripted patrol (owner design, round 11): no attribute
  overrides, no waypoints, and he roams. The stealth beat is
  alcove-3 / alcove-4 / ramp-top with `grace_ticks: 260` — sized to the
  measured sneak time of the route, not guessed (rounds 7 and 10). Being
  caught no longer damages: the warden is the killer, the narrate and the
  heartbeat are the warning.
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
- **Endings** (dialogue branches only): A "escaped as Nobody" / B "took the
  cheese and sailed". Plain fullscreen titles — en NOBODY / THE QUIET SAIL,
  zh 无人 / 悄然扬帆 — each with its own sound sting and `campaign-complete`
  (owner ruling, round 4/5: no pixel-art banner; the art font stays an unused
  engine capability).

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

**Flock staging (round 12, owner finding)**: every sheep position, at every
moment of the campaign, is a distinct cell **inside the upper pen** or **at the
meadow fold** — never the open cavern floor, never the open meadow. The pen
carries one anchor per sheep (`anchor/pen`, `pen-d`…`pen-j`) plus two crew
stands (`pen-b`, `pen-c`, kept 2+ blocks off the ram so they never shadow its
affordance); the fold carries one anchor per sheep (`anchor/fold`,
`fold-b`…`fold-h`) — six inside it, two in and just outside its gate, because
the fold's west interior column is buried (see §7). The herd walks in from the
fold **straight to the pen** in one leg — it never parks on the hall floor —
and walks out to the fold in one leg at the escape.

## 4. Feature surface actually used

classes + named kits · mannequin skins · dialogue flags + gated options · two
endings · narrate chat/title/subtitle · give-item named · collect / interact /
reach / talk-to / kill objectives · props (grindstone) · triggers strike and
strike-npc · a tutorial wave with attributes + equipment · unwinnable combat by
`unleash-actor` · `move-actor` / `move-npc` with `on_arrive` · `sequence`
timelines · a six-shot spectator cinematic with `look_at` · set-time /
set-weather cuts · `close-gate` / `open-gate` · checkpoints ×3 with distinct
`on_respawn` resets · ocean horizon + boundary · area `night-vision`
mitigation · positional sounds · stealth zones · full en + zh-cn l10n (184
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

Recorded by the round-12 conformance review; not changed either way.

1. **B1 is one leg, not a scenic chain.** v1 designed a reach-anchor chain
   along the beach → meadow → slope → mouth walk; the campaign has a single
   `reach-anchor` to the mouth, because `anchor/meadow` and `anchor/fold` are
   defined by both placed greenfield pieces and any *required* reference to
   them is `DW0305`. Restoring the chain needs piece-unique outdoor anchors.
2. **The cheese has no name.** v1 specified a named "Kefalotyri Cheese"; the
   collect objective (owner-requested form) carries no item-name field, so the
   player picks up an unnamed sponge. Restoring the name needs the new
   container-loot surface.
3. **Four sheep are herded in, four were already penned.** v1 said the flock
   of eight is herded in; the pre-penned four match the fiction the dialogue
   established ("lambs penned and sorted by age") and have shipped since
   round 1.
4. **The boulder hint is a strike trigger, not an interact.** v1 said
   right-click; the campaign answers a hit on the stone.
5. **B0's night is a full night cut**, not the designed dusk tint — `set-time`
   takes vanilla keywords only.
6. **No Eurylochus walker twin.** v1 designed an actor twin for scripted
   walks; `move-npc` became a first-class primitive and the twin is
   unnecessary.
7. **Antiphos dies, not Eurylochus.** v1 had the giant kill Eurylochus; the
   round-6 restage moved the death to Antiphos so the victim is a man who
   climbed with the party on camera. Logged in an owner round, but the swap
   itself is not separately attributed to an owner request.
8. **The sheep fold's west interior column is buried** (round-12 finding). The
   round-8/9 landscape batches take piece-local x 0–3 as "the west bank" —
   `west-roll` smooths it, `bank-outcrops` and `shore-transition` scatter rock
   and sand over it, `meadow-treeline` plants oaks in it — but the fold sits at
   piece-local x 2–6, so x=3 is its **west interior column**. All three of its
   cells are solid in the assembled world. The fold that reads as 3×3 from
   outside holds six bodies, not nine; the flock's last two stand in and just
   outside its gate. Proposed restore: exclude the fold rectangle from those
   four batches' west regions (or add a `batch/fold-clear`), which would let
   the whole flock stand inside the walls.
