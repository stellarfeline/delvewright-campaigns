# Nobody's Cave — Island Remake (design brief)

Planner-authored, 2026-08-01. Owner's staging vision + dramaturgy are fixed
inputs; everywhere the owner left unspecified, this design deliberately uses
**every feature the toolchain supports** (owner directive: showcase). This file
ships as DESIGN.md in the content-repo remake PR. Engine dependencies:
spec-0012 (checkpoints), spec-0013 (ocean horizon + boundary), spec-0014
(actors/staging verbs).

## 1. The island (layout — ONE contiguous area, zero transports)

No inter-area teleports, no filler corridors: every space serves a story beat
or a sightline. Walk-through order (west → east, rising):

1. **Beach camp** (entry piece, sea level y≈64): sand shore; campfire ring
   with log benches (campfire doubles as relight fixture); two tents; supply
   crates (barrels); class-selection NPC spot. **Greek galley** anchored just
   offshore with a gangplank to the beach — the escape-promise seen from
   minute one.
2. **Greenfield** (connector pieces, gentle rise): grass, scattered oaks,
   poppies/daisies, a worn dirt path; a grazing meadow with a low stone-wall
   sheep fold (foreshadowing; empty — the sheep are *his*).
3. **Mountain** (large terminal piece): grass-to-stone slope path switchbacks
   up the face to a cave-mouth ledge; the **boulder** sits beside the mouth
   (visible on approach — Chekhov's rock).
4. **Cavern** (mountain interior): one TALL WIDE hall (target ≥ 30×14×24
   interior), NOT rooms-and-corridors. Zones within the hall: cheese store
   (shelves near entry), central fire pit, rock-shelf **ramp** (owner: no
   ladders) to an upper sheep pen, 3–4 **shadow alcoves** (stealth zones,
   visually dark recesses), dripstone + moss dressing, two ceiling light
   shafts (beam accents; hall still reads dark, relight lanterns minimal).

World: `horizon: "ocean"` (sea level 62 — the map IS an island), `boundary`
margin 16 (out-of-bounds → last checkpoint + message), start `time: noon`,
`weather: clear`.

## 2. Dramaturgy (beats → mechanics; owner's script, feature-maxed)

- **B0 Beach**: crew mannequins (skins) around the campfire; class selection +
  named kit; Eurylochus dialogue sets premise (l10n en+zh). *Planner addition,
  owner may veto*: a dusk-tinted 3-drowned wave stumbling out of the surf as a
  30-second gear tutorial (kill objective, tuned weak) — the only real combat
  before the cave, classes get to matter.
- **B1 Follow**: Eurylochus `move-actor`-walks the path (beach → meadow →
  slope → mouth), player follows (reach-anchor chain along scenic beats, no
  filler). Positional sheep/ambient `play-sound` cues at the meadow.
- **B2 Cavern entry — CHECKPOINT 1** (`set-checkpoint`, narrate line). Cheese
  store `interact` + `give-item` (named "Kefalotyri Cheese"). **Choice
  dialogue** (dialogue flags): *take the cheese and slip away* → Ending B
  route (walk back down, gangplank `interact`, art title) vs *wait for the
  owner of this cave*.
- **B3 The giant returns** (waited): `sequence` cutscene — `set-time night`;
  player told to hide (`begin-stealth`, shadow alcoves); sheep flock (8 sheep
  actors) herded in by **Polyphemus** (warden actor) via synchronized
  `move-actor`s + hoof/roar sounds; boulder seals the mouth (`set-block`
  basalt fill + deepslate slam sounds); Polyphemus one-punches Eurylochus
  (rhythm-synced: attack-swing `actor-anim` if the spike proves it, else
  camera-cut + sound; Eurylochus `despawn-actor style: kill`); giant walks
  the ramp down to the fire pit; `end-stealth`. Caught during any of it →
  death → CP1. **CHECKPOINT 2** at the fire-pit aftermath.
- **B4 Trapped**: boulder `interact` → "it will not move" hint. Striking the
  giant (strike trigger) → `unleash-actor`: real warden, unwinnable; death →
  respawn CP2, `on_respawn` re-cages him to the idle puppet. Dialogue with
  Polyphemus: the **"Nobody"** exchange (flag `told-nobody`), wine offer
  (`interact` with wine-skin prop + requires_item), he sleeps (sleep
  pose/anim per spike; snore loop `play-sound`).
- **B5 The eye — CHECKPOINT 3**: eye-stab `interact` (requires the
  fire-hardened stake — grindstone prop sharpening beat retained from v0.4);
  `sequence`: roar + `set-weather thunder` + hurt sounds; blinded Polyphemus
  becomes a **weakened pacing puppet** (attack-weakened, HP unchanged)
  `move-actor`-patrolling toward the upper pen. Sneak-follow beat:
  `begin-stealth` with alcove-to-alcove zones up the ramp; caught → death →
  CP3 (`on_respawn` resets his patrol).
- **B6 Escape**: right-click a pen sheep (`interact`) → finale `sequence`:
  boulder opens (`open-gate`), Polyphemus roar-pose at the mouth, sheep
  procession + Perimedes + player walk out (`move-actor` convoy), `set-time
  day` + `set-weather clear` on the shore, gangplank boarding, **Ending A**.
- **Endings** (dialogue branches only, no achievements): A "escaped as
  Nobody" / B "took the cheese and sailed". Each fires its own big **art
  title** (`narrate style: art`, custom font) + distinct sound sting +
  `campaign-complete`.

## 3. Cast & actors

NPCs (dialogue): Eurylochus (guide; dies), Perimedes (survivor companion),
2 flavor crew at camp. All mannequin-skinned (reuse existing cast skins).
Actors (spec-0014): Polyphemus (warden; `vulnerable: false`), 8 sheep,
Eurylochus-walker (actor twin for scripted walks; the dialogue NPC despawns
during walk beats — same pattern v0.4 used for MoveNpc).

## 4. Feature-showcase checklist (everything supported, used on purpose)

classes+named kits · mannequin skins · dialogue flags + gated options ·
two endings · narrate (chat/title/subtitle/**art**) · give-item named ·
collect/interact/reach/kill objectives · props (grindstone, campfire, pot,
wine-skin) · triggers strike/use/approach · waves w/ attributes+effects
(tutorial wave; unwinnable fight via unleash) · move-actor flocks · sequence
cutscenes · spectator-dolly cutscene (one: the boulder-seal wide shot) ·
set-time/set-weather cuts (noon→night→thunder→dawn) · lighting fixtures
(campfire/lanterns) · checkpoints ×3 + on_respawn resets · ocean horizon +
boundary · positional sounds throughout · full en+zh-cn l10n · stealth zones.

## 5. Prefab piece list (contract for the prefab workers)

| Piece | Kind | Must provide anchors |
|-------|------|----------------------|
| `island-beach-camp` | entry | `entry`, `anchor/camp-fire`, `anchor/class-post`, `anchor/crew-a`, `anchor/crew-b`, `anchor/surf-wave` (tutorial wave, on sand, wet-cell-free), `anchor/gangplank` |
| `island-galley` | attached set piece (or merged into beach piece) | `anchor/deck` |
| `island-greenfield` | connector (1–2 variants) | `anchor/meadow`, `anchor/fold` |
| `island-mountain` | large terminal (shell + cavern interior, slope on the face) | `anchor/mouth`, `anchor/boulder` (gate region), `anchor/cheese-store`, `anchor/fire-pit`, `anchor/ramp-top`, `anchor/pen`, `anchor/alcove-1..4` (stealth), `anchor/checkpoint-1..3`, `anchor/shaft-1..2` (light beams) |

Rules: sockets per existing tileset conventions; gravity floors get substrate
(generator invariant); interiors relight-friendly; palette from the admitted
allowlist; NO long corridors — traversal is scenery. Galley: planks hull,
single mast + white wool sail, oar rows (spruce trapdoors/buttons), Greek eye
motif on the prow if palette allows. Deterministic generators, provenance
metadata, DW07xx-clean admission.

## 6. Delivery

New campaign id `nobodys-cave-island`, **separate PR** in the content repo
(current `campaign/nobodys-cave` PR #1 ships as-is once it clears owner
playtest). Full ladder green before the PR opens; this DESIGN.md included.
