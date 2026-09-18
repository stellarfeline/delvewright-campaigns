# Vesperhold — generation record

## Toolchain

- Built with the engine at revision `509ebc58` (`delvec 1.6.0, dsl 0.30.0, mc 1.21.11`), `dsl_version` 0.30.0 on every stage document and the `zh-cn` sidecar.
- Placement: `areas[]` with one area bound to one campaign-built piece, `prefab/vesperhold` — the whole site as a grammar program generated from `design/programs/`, ringed by a `valley` surround. A site plan was drafted first and dropped: its derived walls and roofs are the blockout's fixed palette and stay whole-owned after detail, so it cannot give the castle a designed exterior, which is the brief's one standing requirement (the Doune Castle site in this repository is the bar). The same single-area shape rules out a second space, so the second timeline is told as echoes in the present rooms.
- No shipped library piece is bound; the campaign's only piece is its own.
- The engine constitution's operating half (`CLAUDE.local.md`) was not available to this run; nothing here decides dispatch, review, merge or staging.

## What the brief pinned, and what was invented

Pinned: souls-like combat and exploration; a cryptic main plot; one huge Gothic castle with regions and a spectacular exterior; twenty or more designed places; about half of Stormveil Castle; up to four co-op players; an hour or more of play; ruined or whole at the author's choice; a second timeline ten years earlier allowed; research before authoring.

Invented: everything named in `DESIGN.md` — the bell and its price, the Undertide, the cast, the route, the echoes, the two endings.

Research consulted before authoring (ideas only): the anatomy of Stormveil Castle and the lessons of other souls castles for structure, rest spacing, shortcuts, gatekeepers and traps; FromSoftware's fragmented storytelling, recurring allies, tricksters and past-layer precedents for the story and the echoes.

Research consulted for the off-road content (ideas only; counts are cited, the density drawn from them is this record's own arithmetic):

- Optional bosses and mini-bosses per legacy dungeon, counted: Elden Ring's Stormveil Castle holds two clearly off the critical path (the Ulcerated Tree Spirit under the Liftside Chamber, the Crucible Knight in the Rampart Tower) plus two avoidable ones on it (the Grafted Scion, the Lion Guardian) — [Fextralife, Stormveil Castle](https://eldenring.wiki.fextralife.com/Stormveil+Castle) (not freely licensed: ideas only); Dark Souls' Undead Burg and Undead Parish together hold about six off-path elites (Black Knights, Havel, the Channeler, the Berenike Knight, the Fang Boar, the Hellkite's tail) — [Fandom, Dark Souls wiki](https://darksouls.fandom.com/wiki/Taurus_Demon) (CC BY-SA) and Fextralife (ideas only); Dark Souls III's High Wall of Lothric holds one (the Lothric Wyvern) — [Fextralife, High Wall of Lothric](https://darksouls3.wiki.fextralife.com/High+Wall+of+Lothric) (ideas only).
- Every off-path elite in those counts is a one-time kill whose reward is a named piece of gear or a material, never currency alone; each sits in its own pocket with ordinary enemies and at most one treasure.
- The optional-elite pattern, its bypass and its dormancy tell, and the teach / test / twist pacing of ambushes: the engine's souls dossier (`docs/notes/souls-design-language.md` §3–4, and the sources it cites), which also records that bait set pieces in the series cover an ambush with something conspicuous in frame.
- No source found gives a count of ordinary enemies for a legacy dungeon or a share of its content off the critical path; nothing here claims one. Nor was a named instance found of a bait *enemy* held up by terrain; the Hedge Garden's set piece is authored on the dossier's bait-item grammar (the conspicuous thing in frame, the ambushers behind it), not transcribed.

Calibration drawn from those counts: about one optional elite per eight to ten main-route places, one to a side pocket, each with its own rank and file and one high-tier drop. Twenty-nine places on the road gives three optional elites; Stormveil itself, the nearest in size, has two clearly off its path, so three is the ceiling, not the floor.

## Decisions

- The second timeline is told as echoes: a sky cut and the people of that morning staged in the present room, because the engine has no timeline primitive and the one-area site holds no second space.
- The castle's exterior is designed block by block and must read at least as well as the Doune Castle site.
- The castle is a ruin in the present and whole in the echoes.
- In-game text ships in English with a `zh-cn` sidecar.
- `difficulty` is `normal`: the souls baseline, without zombie reinforcement muddying the tuned waves.
- `horizon` is a valley with a 64-block rim, so the castle stands in a mountain bowl; the approach and the causeway cross the piece's own valley floor.

## Content decisions

- The past is staged in the present rooms: two echoes put the people of the Last Vesper's morning where they stood (a deferred NPC and skinned actors), the third is the campaign's one camera cutscene. The engine's `DW0351` advisory on the two deferred NPCs is accepted with narrative cover — each appears under the title card of an echo ("the morning of it", "The stair remembers.") and leaves as the rain returns.
- The chapel echo is two quests (`the-chapel-echo`, `the-wardens-key`) because a body spawned mid-quest can only be cast from the next quest on.
- Both forks put their options in one node, each option setting its flag and completing the talk objective, so the two branches are exclusive by construction. Halvard leaves the watch tower on both branches; only what the party finds at the Throne Fire differs.
- Five fires: the Causeway, Cloister, Watch, Tower and Throne Fires. The Watch Fire stands in the watch tower's north-east corner, beyond the rampart archers' reach, lit when the rampart is cleared; the Tower Fire stands in the bell tower's stair hall, one flight under the Ringer.
- The east side is the castle's one off-road pocket: the Chandlery Yard (the Chandler, three Tallow-Hands), the Spur Passage, the Hedge Garden (the Gilded Bowman, three Hedge-Lurkers, three Gardeners) and the Summerhouse (the Hedge Knight). Every wave there returns on rest; the two elites are actors sprung by approach, as the Last Warden-Knight is, and each drops the piece it wears.
- The Hedge Garden's set piece is a bait held by terrain: the Gilded Bowman on a plinth four high with a ladder on its far face, and three lurkers sprung behind the company when it reaches the fountain. The lurkers come without a telegraph.
- The armory's two real chests each hold one piece a step above the kits: an iron sword with Sharpness II, an iron chestplate with Protection II.
- Pellam sells arrows, a golden apple, an iron spear, a crossbow and a diamond sword, and one lie.
- The Undertide Pool's well has three treads up out of the water to a gap in its lip on the north and south, each gap between two soul lanterns.
- The portcullis windlass stands against the gatehouse wall west of the gate — two uprights, a drum with a wheel at each end under a plank hood, and its chain running up the wall and across to the gate — so the gate's passage is clear.
- The garth's tree is an old dark oak with a two-wide bole, root flares, limbs and a full crown; the east garden's trees and the orchard rows are the same tree, one wide.
- Wave mobs that are one kind of creature share one name on purpose: `Nameless Soldier` (barracks and armory), `Hired Knife` (both mobs of the walk ambush). The `zh-cn` sidecar translates each consistently.
- The `zh-cn` sidecar was translated in-agent from the finished English, with each character's speech style held (Halvard archaic and courteous, Pellam wheedling, the apprentice blunt).

## Posture note

Three axes pushed off the default for this campaign: **time order** — the decisive event is shown out of order, in the echoes, after its consequences; **morality** — the final boss is right and the sympathetic keeper caused the ruin; **emotion rendering** — Warden Hesk names her fear outright ("I am afraid of the day I will not know her"). The Silence ending is disproportionate to everything before it and explains nothing.

## The castle piece

The whole site is one grammar-built piece, `prefab/vesperhold`, expanded at **172 x 104 x 292, seed 1** and bound in the campaign's one area under a `valley` horizon. `design/programs/build_castle.py` paints the site into a voxel grid from one module per part (`castle/terrain.py`, `approach.py`, `walls.py`, `ward.py`, `cathedral.py`, `undercroft.py`, `keep.py`, `belltower.py`, `gardens.py`), reading every position from `castle/layout.py`, derives every stair's shape the way vanilla does, and emits the grammar's partition as `vesperhold.json`. `finish.py` expands it into the prefab library and writes the six gate regions (`gates.json`) into the manifest — the grammar declares point anchors only — then measures the planes and the lighting and audits the piece. Re-run both to regenerate.

Heights in piece coordinates: valley floor feet 8, castle floor 24, keep dais 28, wall walks 36, bell deck 52, undercroft 12.

What the machine says about the piece at admission: every expansion gate passes (blocks exist, shapes and states complete, oriented fills, stair shapes as vanilla derives them, fluid contained); `prefab audit` passes; `walk_y` 8, `waterline_y` 11; lighting profile `dark`: 4812 of 43015 floor cells reachable on foot are below light 3 under a clear night sky (1935 at 0, 1113 at 1, 1764 at 2); the area's torch pass (`min_light` 3) lights the rest at build. The piece marks 101 point anchors — 96 cells a body stands in, three furniture cells (the armory's three chests) and two cells nobody stands in — and six gate regions.

The valley field is ringed by a two-course dry-stone wall on the piece's edge, and `world.boundary` holds the party four blocks beyond it, so the party's world ends where the piece does. The causeway's parapets are unbroken, iron bars between merlons, so nothing on the bridge is a way off it.

### What the build asked of the piece

- **Three doors are built open.** The postern, the Keep Doors and the Warden's Door are air in the piece and shut by `close-gate` when the party first speaks with Tamsin, a few steps from the spawn. Built shut, the stake proof (`DW0525`) refused every rest behind them: the delvec 1.6.0 compiler reads a door the piece builds shut as shut again at the two critical-path steps past the last objective, where no opening precedes, so from the Cloister Fire the whole valley read as unreachable. A door built open and sealed at a story step does not carry that reading. The engine side of this is a finding for the engine, not a fence the campaign works round forever; when it is fixed the three doors can be built shut again. The shortcut doors stay built shut, as the engine requires.
- **The Almoner's Door is barred for good.** As a shortcut it failed `DW0374`: from the campaign entry the Keep Doors reach the Great Hall sooner than the cloister lane does, so opening it shortened no walk. The Throne Fire already stands beside the keep's fights. The door stays in the hall's west wall, as the approved image shows it.
- **Every reach volume is sized to its own floor** (`DW0881`), so no cube takes in a parapet top or a floor on the far side of a wall. The Buttress Walk gained a short roofed arch where its objective is, so the parapet under it is no floor, and the Antechamber's floor was filled beneath, closing a hollow.
- **The Tower Fire is lit when the second shard wakes, not when the Warden's Door opens.** Armed in the door's own beat, the stake proof (`DW0525`) refused it: it measures a fire's reign from the state the party arrives in at the arming step, which is before the door that same step opens, so from inside the tower the whole castle read as unreachable. The shard is in the same stair hall, one objective later, and nothing about the fight changes.
- **The false chest is a plain chest.** The prefab audit's palette refuses `minecraft:trapped_chest` (`DW0730`), which is the block a `trapped-chest` trap names as its visible trigger; a plain chest is the only chest the audit admits, and the trap's own trigger is the interaction the compiler places on that cell. The armory's two real chests are plain chests too, so nothing tells the false one apart.
- **No anvil stands at Pellam's stall.** The prefab audit refuses `minecraft:anvil` (`DW0730`).
- **The Chandler's hands wait in the lean-to**, not in the yard: seated in the yard, their aggro radius reached the rampart stair's flights through the wall and `DW0380` read the road as running through an optional fight.
- **Two flights gained a newel post** at their first tread (the rampart stair, the bell tower's first flight), so the only way onto them is up their climb (`DW0430`).
