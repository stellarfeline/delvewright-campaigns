# Vesperhold — generation record

## Toolchain

- Built with the engine at revision `14517e99` (`delvec 1.6.0, dsl 0.33.0, mc 1.21.11`), `dsl_version` 0.33.0 on every stage document and the `zh-cn` sidecar.
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
- **Health bars** (`health_bar`, spec-0073) on every fight billed `boss` or `elite`, each titled by the fight's own name. A bar is drawn for a player within `range` blocks of a live body, so each `range` is the distance from the body's seat to the threshold of its arena — the bar comes up as the player crosses into the room and not before:

  | fight | seat (piece) | range | threshold it answers |
  |---|---|---|---|
  | the Porter | (87, 24, 158) | 14 | the barbican's south arch, z 172 |
  | the Drowned Choir | (36, 12, 70) | 22 | the pool's south mouth from the crypt passage, z 92 |
  | the Last Warden-Knight | (47, 13, 115) | 24 | the crypt's west door (25, 125); he shows it only once he stands |
  | the Chandler | (153, 24, 135) | 14 | the chandlery yard's corners; he shows it only once he turns from the vat |
  | the Hedge Knight | (142, 24, 27) | 14 | the summerhouse and its lawn; he shows it only once he steps out |
  | the Ringer Unmade | (24, 52, 12) | 12 | the head of the stair onto the bell deck; the Tower Fire, one flight down, is 18 away |
  | the Unremembered Guard | (83, 24, 72) | 20 | the Keep Doors, z 93 |
  | King Oswin | (83, 28, 32) | 14 | the throne hall's door, z 46; the Throne Fire is 19 away |

  The Gilded Bowman is bait and the east side's rank and file are no one's billing; they show none.
- The Hedge Garden's set piece is a bait held by terrain: the Gilded Bowman on a plinth four high with a ladder on its far face, and three lurkers sprung behind the company when it reaches the fountain. The lurkers come without a telegraph.
- The armory's two real chests each hold one piece a step above the kits: an iron sword with Sharpness II, an iron chestplate with Protection II.
- Pellam sells arrows, a golden apple, an iron spear, a crossbow, a diamond sword, three enchanted books and an enchanted iron sword, and one lie. The anvil at the east end of his counter is how a book reaches a weapon.
- **Pellam's prices** are set against the tallow a player holds at his stall. The story beats pay every player: 40 (the Porter), 35 (the cliff path), 40 (beneath the psalter) and 20 (the rampart cleared) put 135 in a player's purse on the first visit; the hired knives add 20 (155), the Ringer 60 (215) and the keep 50 (265), the last after the road has left him. A death can forfeit all of it. On the first visit a player affords one major piece and change, never the shelf:

  | offer | price | why |
  |---|---|---|
  | Book of Smite III (*Litany for the Unquiet*) | 70 | the strongest thing he sells: almost everything in Vesperhold is undead, and Smite III goes on every class's weapon (sword, axe, mace). Dearer than any single piece so it is the first visit's one choice |
  | Iron sword, Smite II, Unbreaking I (*Sexton's Blade*) | 80 | the enchanted mid-tier weapon: a ready-made undead-killer that needs no anvil and no experience, priced above the book it is weaker than because it is the one that needs nothing else |
  | Book of Power II (*Bowyer's Hymnal*) | 55 | the archer's book; one class uses it, so it sits under the Smite book |
  | Book of Protection II (*Vigil Psalter*) | 50 | one armour piece a step up — the Garrison Hauberk's enchantment, for any piece |
  | diamond sword (*Altar-Blessed Sword*) | 100 | unchanged: the lie on the shelf. It costs more than the Smite book and does less against the dead |

  A book applied at the anvil costs experience levels, which the party earns only from kills; by vanilla's anvil rule a book costs its level times its enchantment's anvil multiplier halved (Smite III, Power II and Protection II come to two or three levels each). These figures are from memory of the game's rule and are not measured here; the next playtest reads whether a player arrives at the stall with the levels to spend.
- **What a kill pays** (`on_kill`, spec-0074). Tallow is a `player` datum, so a kill pays the player the game credits with it. A purse forfeited on a second death is gone for good, so earnings have to be repeatable or the economy only shrinks; the rank and file are the repeatable part, and they are a top-up, never the road's income:

  | fight | per kill | `fires` | bodies |
  |---|---|---|---|
  | cliff watch, grooms, barracks, rampart archers, hired knives | 2 | `every-kill` | 3, 4, 4, 3, 3 |
  | the armory ambush | 2 | (left off: sprung once by its trap, never back) | 3 |
  | Tallow-Hands, Gardeners | 3 | `every-kill` | 3, 3 |
  | the Gilded Bowman | 5 | `every-kill` | 1 |
  | Hedge-Lurkers | 3 | `first-kill` (an actor is re-stood only while it stands, so a dead one never pays again) | 3 |
  | the Last Warden-Knight, the Chandler, the Hedge Knight | 25 | `first-kill` | 1 each |

  The Porter, the Drowned Choir, the Ringer, the Unremembered Guard and the King keep the payout of the `kill` objective that ends them and carry no `on_kill`, so no boss pays twice.

  The arithmetic, in tallow paid across the party (each kill goes to the one player who makes it):
  - **The road's first pass.** Before the first visit to Pellam the road's rank and file are 17 bodies (cliff 3, grooms 4, barracks 4, armory 3, archers 3): 34 tallow, plus 25 for the Warden-Knight if the company wakes him. Against 135 each from the story beats, a pair of players arrives with about 165 each, a party of four with about 150: the kills add a tenth to a fifth.
  - **The farm.** One loop of the east side after a rest — three Tallow-Hands, three Gardeners, the Bowman — pays 23. The Sexton's Blade (80) is 27 east-side kills, three and a half loops; the Smite book (70) three loops; the diamond sword (100) four and a half. A first-visit purse lost for good (135) is six loops. On the road, a rest's worth of the barracks pays 8, and the same 80 takes 40 kills.
  - **Against the road's pace.** The story beats pay 265 over a campaign aimed at 80 minutes; a loop of the east side is a few minutes of fighting and pays 23, near the four smaller story beats (15 to 20) and under the mean of the eight (33, from 15 to 60), so farming tops a purse up or rebuilds it, and never outpaces walking on.

  Research: spec-0074's record (§7) holds the precedent — in Dark Souls a rest respawns every enemy except bosses and mini-bosses, and the respawned enemies drop souls again, which is what makes soul farming possible (Fextralife, *Bonfire*, ideas only). The pair `every-kill` for the rank and file, once for the elites, is transcribed from that. No yield figure from any reference game is used; the amounts are this record's own, set against Vesperhold's purse and shelf above.
- **The Undertide Pool's well is curbed, and its killing volume sits at the bottom of a shaft.** The choir killed itself: `lethal/undertide`'s box stood at the water's surface in the well's heart, and its `@e` arm kills every body that is not a player; the four choristers, seated nine blocks north of the well with the party entering from the south, walked down the old treads into the water on their way to the party and died with their heads in the box, on every life, before the party touched them. The fix walls the well, of the three the diagnosis offered: every cell that touches the water carries a polished-deepslate wall block, a block and a half high — over the lift of a blow and under a player's eye, the reasoning the cliff shelves' parapet rests on — so no body walks, jumps or is knocked into the water, and the treads and the gaps in the lip are gone. The box moved to the bottom of a shaft under the well's heart, five below the well floor (piece y 2–4, world y 58–60), so a killing volume sits at the bottom of the pit, and water floats an item up, never down to it. A deeper shaft alone was refused: the diagnosis found the choristers standing on the well's floor, and a drowned keeps to the floor of the water it is in unless provoked ([minecraft.wiki, *Drowned*](https://minecraft.wiki/w/Drowned), ideas only), so a shaft deepened under open treads is a shaft the choir walks down into. Re-seating the choir away from the well was refused too: the party enters south of the well and the choir must come to it, so any seat puts the water between them. Four soul lanterns stand on the curb.
- **One body carries the tongue.** Every chorister's death loot dropped "The Vesper's Tongue", so a fight left four copies, and a chorister the well killed dropped its copy inside the box. The wave is now two stacks with the same body, gear and numbers — three Drowned Choristers and one Drowned Precentor — and only the Precentor declares the drop; the `collect` stays `dropped_by: wave/drowned-choir` with a count of one (`DW0492` asks that the wave declares at least that many). The emitted datapack carries one `dw_drop` death loot table for the choir, on the Precentor's summon. The fight is four bodies at 34 health, 6 attack, 24 follow range, as before; its health bar is titled "The Drowned Choir", since the wave now names two kinds of body (`DW0910`).
- The portcullis windlass stands against the gatehouse wall west of the gate — two uprights, a drum with a wheel at each end under a plank hood, and its chain running up the wall and across to the gate — so the gate's passage is clear.
- The garth's tree is an old dark oak with a two-wide bole, root flares, limbs and a full crown; the east garden's trees and the orchard rows are the same tree, one wide.
- Wave mobs that are one kind of creature share one name on purpose: `Nameless Soldier` (barracks and armory), `Hired Knife` (both mobs of the walk ambush). The `zh-cn` sidecar translates each consistently.
- The `zh-cn` sidecar was translated in-agent from the finished English, with each character's speech style held (Halvard archaic and courteous, Pellam wheedling, the apprentice blunt).

## Posture note

Three axes pushed off the default for this campaign: **time order** — the decisive event is shown out of order, in the echoes, after its consequences; **morality** — the final boss is right and the sympathetic keeper caused the ruin; **emotion rendering** — Warden Hesk names her fear outright ("I am afraid of the day I will not know her"). The Silence ending is disproportionate to everything before it and explains nothing.

## The castle piece

The whole site is one grammar-built piece, `prefab/vesperhold`, expanded at **172 x 104 x 292, seed 1** and bound in the campaign's one area under a `valley` horizon. `design/programs/build_castle.py` paints the site into a voxel grid from one module per part (`castle/terrain.py`, `approach.py`, `walls.py`, `ward.py`, `cathedral.py`, `undercroft.py`, `keep.py`, `belltower.py`, `gardens.py`), reading every position from `castle/layout.py`, derives every stair's shape the way vanilla does, and emits the grammar's partition as `vesperhold.json`. `finish.py` expands it into the prefab library and writes the six gate regions (`gates.json`) into the manifest — the grammar declares point anchors only — then measures the planes and the lighting and audits the piece. Re-run both to regenerate.

Heights in piece coordinates: valley floor feet 8, castle floor 24, keep dais 28, wall walks 36, bell deck 52, undercroft 12.

What the machine says about the piece at admission: every expansion gate passes (blocks exist, shapes and states complete, oriented fills, stair shapes as vanilla derives them, fluid contained); `prefab audit` passes; `walk_y` 8, `waterline_y` 11; lighting profile `dark`: 4812 of 42886 floor cells reachable on foot are below light 3 under a clear night sky (1936 at 0, 1112 at 1, 1764 at 2); the area's torch pass (`min_light` 3) lights the rest at build. The piece marks 101 point anchors — 95 cells a body stands in, four furniture cells (the armory's three chests and the rampart's plate) and two cells nobody stands in — and six gate regions.

The valley field is ringed by a two-course dry-stone wall on the piece's edge, and `world.boundary` holds the party four blocks beyond it, so the party's world ends where the piece does. The causeway's parapets are unbroken, iron bars between merlons, so nothing on the bridge is a way off it.

### What the build asked of the piece

- **Three doors are built open.** The postern, the Keep Doors and the Warden's Door are air in the piece and shut by `close-gate` when the party first speaks with Tamsin, a few steps from the spawn. Built shut, the stake proof (`DW0525`) refused every rest behind them: the delvec 1.6.0 compiler reads a door the piece builds shut as shut again at the two critical-path steps past the last objective, where no opening precedes, so from the Cloister Fire the whole valley read as unreachable. A door built open and sealed at a story step does not carry that reading. The engine side of this is a finding for the engine, not a fence the campaign works round forever; when it is fixed the three doors can be built shut again. The shortcut doors stay built shut, as the engine requires.
- **The Almoner's Door is barred for good.** As a shortcut it failed `DW0374`: from the campaign entry the Keep Doors reach the Great Hall sooner than the cloister lane does, so opening it shortened no walk. The Throne Fire already stands beside the keep's fights. The door stays in the hall's west wall, as the approved image shows it.
- **Every reach volume is sized to its own floor** (`DW0881`), so no cube takes in a parapet top or a floor on the far side of a wall. The Buttress Walk gained a short roofed arch where its objective is, so the parapet under it is no floor, and the Antechamber's floor was filled beneath, closing a hollow.
- **The Tower Fire is lit when the second shard wakes, not when the Warden's Door opens.** Armed in the door's own beat, the stake proof (`DW0525`) refused it: it measures a fire's reign from the state the party arrives in at the arming step, which is before the door that same step opens, so from inside the tower the whole castle read as unreachable. The shard is in the same stair hall, one objective later, and nothing about the fight changes.
- **Every trap stands on its trigger** (`DW0917`). The false chest is a `minecraft:trapped_chest` at piece (157, 24, 152), world (157, 80, 152), facing west like the real chests beside it; the volley's `minecraft:stone_pressure_plate` sits at piece (155, 36, 90), world (155, 92, 90), on a whole stone-brick flag in the middle of the east rampart's walk. The plate's anchor is a furniture cell (it names a block, not air).
- **The volley leaves a way out** (the owner's rule: a timed hazard admits passage in at least a fifth of its cycle). Its kill zone is the plate's cell ± 3 across and along, 7 × 3 × 7; the deepest cell a body can stand in is four blocks from the zone's edge, 16 ticks at a sprint. The salvos are 20 ticks apart, so a body caught by one salvo walks out before the next from 5 of 20 phases (25%); at 15 it could not from any. The interval moved rather than the zone: the zone spans the walk's full width (x 152–158 of 152–159), and a shallower one would leave a lane down the side the volley is meant to punish.
- **The anvil** stands at piece (156, 36, 12), world (156, 92, 12), at the east end of Pellam's counter on the company's side.
- **The Chandler's hands wait in the lean-to**, not in the yard: seated in the yard, their aggro radius reached the rampart stair's flights through the wall and `DW0380` read the road as running through an optional fight.
- **The shelves' parapet is unbroken.** The side route's open edges — the south shelf's lip (piece z 177, x 4–75), the west shelf's lip (x 4, z 128–176) and the west shelf's blind north end (z 127, x 4–11, on a course of rock added under it) — carry one continuous course of wall blocks at the shelf's feet level (piece y 24, world y 80), mixed stone-brick, mossy stone-brick, cobblestone and mossy cobblestone, stepping up every ten or so cells into a stub of the old parapet (a stone with a post on it). A wall block stands a block and a half: over the height a knockback lifts a body (about a block and a quarter) and under a player's eye (a block and five eighths), so the valley stays in view and nothing fought on the shelf goes over. The broken one-course parapet it replaces let the party's blows knock the Cliff Watchmen (`wave/cliff-watch`, the kill objective `obj/clear-the-shelf`) sixteen blocks into the valley, where a survivor stood with no way back and the objective could not complete. A parapet was chosen over re-seating the wave (the shelf is the fight, and it is five wide everywhere, so no seat is far from an edge) and over a lethal floor under the shelf (a death volume on open valley turf reads as safe floor, which the danger rule forbids). The wall blocks' sides and posts are derived from their neighbours the way vanilla derives them. The approved image of the cliff path (`design/concept/cliff-path-near.jpg`) already shows an unbroken parapet.
- **No kill-objective body has an open drop to ground the party cannot reach.** Every wave a `kill` objective names was checked over the grid the generator paints: a flood of the floor a body can walk from its seat (steps of one, drops of three, out to twice its follow range, wall blocks not climbable, air-mixed ruin courses counted as gaps), and every edge in it with a fall of four or more. After the parapet: the Porter, the Cliff Watchmen, the grooms, the rampart archers, the hired knives and the King's and the Unremembered Guard's halls have none that leave the room they fight in (the Guard's and the King's only drop is four blocks off the dais into the Great Hall); the Drowned Choir has none, since the well is curbed; the Ringer's is the stair well inside the bell tower, down to the Tower Fire's hall. The flood is a model of the geometry, not a measurement of the game; the next bot run is the measurement.
- **Two flights gained a newel post** at their first tread (the rampart stair, the bell tower's first flight), so the only way onto them is up their climb (`DW0430`).
