# The Stranding — generation record

The campaign's own decisions, as its author records them. `DESIGN.md` is the design of record; this file says what was pinned by the brief, what the toolchain is, which decisions stand, and where the map restarts.

## Toolchain

- Engine: `delvec` built from source at `507a5e0e20712c8c1e80f52ab1583b1ef91adaaa`, `dsl 0.38.0`, `mc 1.21.11`.
- Prefab library: this content clone's `prefabs/`.
- Reference images: `gemini-native`, model `gemini-3.1-flash-image`, series anchored with `--chain-from`, style contract in `--style-note`.
- The engine's other half of its constitution (`CLAUDE.local.md`) is not available to a run; nothing here concerns dispatch, review, merge or staging.

## What the brief pinned

`DESIGN.md` is a detailed brief, so it is honoured exactly and nothing is showcased beyond it: four acts and thirty-six places in the order it gives, the cast of four, the four classes and their kits, the fights and tentacle counts, twelve cutscenes, the two endings, the danger model, the light plan, the hour (`night`, `clear`, full moon). `DESIGN.md` § Posture is the posture note: escalation is uneven, people name their fear, and the ending does not explain itself.

## Map restart

The map is rebuilt from the site-plan step on the new route. Nothing from the previous map is reused: no site plan, layout graph, geometry brief, detail plan, world edits, program, piece, form, generator or `the-stranding-*` prefab remains in the tree (git history keeps them). The story documents (`world.json`, `npcs.json`, `classes.json`, `quest-plan.json`, `quests.json`, `dialogue.json`, `l10n/`), `design/`, `design.json`, `skins/`, `textures/` and both design files stay; ids in them that named the old map's anchors, boxes and places are re-bound by the new map, not kept alive by it. `design/cameras.json` positions are in the old map's coordinates and are re-aimed with the new map.

## Standing decisions

Story and mechanic decisions that do not concern map geometry.

- **Seed** `1919`. **Difficulty** `normal`. **Horizon** `ocean` (sea level y 62 under the flat's mud at y 64), `boundary` carries a message.
- **Atmospheres**: `wrong-place` (olive sky, close yellow fog, red clouds, no music), `inside-body` (dark red, close fog, no music), `red-night` (the body, the bank and the flat after the cut), `sea-fog` (the endings). The wrong place stands over the body's bank and outside until the cut at the Brow, then `red-night`; whether the bank carries it or a beat paints it is settled with the new map (a shared paint boundary at the mouth and breach is refused, `DW0929`).
- **NPCs**: Wenna, Tregear and Marrack are `quest-giver`, Davey `flavor`; Davey stands by the heart from world load. Each body is a `minecraft:mannequin` with the skins in `skins/`.
- **Classes**: the four kits of `DESIGN.md`, nothing added; the Physician's splash potions carry `minecraft:healing`; the Scholar's brush is in no other kit; no bonfire, no flask.
- **Quest plan**: sixteen quests in one chain, all mandatory, finale `quest/the-pier`; one branch point at the pier forking on `flag/stone-kept` and `flag/stone-returned` to `ending/the-keeping` and `ending/the-return`. `min_players` 1.
- **One body**: a realistic rotting sperm whale (`DESIGN.md` § The body); tentacles rising from its wounds are the wrongness and are not the whale's. Approved images stand as style; where they differ from § The body, the record wins.
- **The escape crossing is the climax reveal** (cutscene 10), played once. **The return is the bad ending**: by what it shows, and the same figure rises at the town's shore at its end. No player text labels either ending. The Figure is unnamed, mentioned obliquely, never by the townsfolk.
- **Inside light** follows the engine's `interior-lighting.md` §7 and the owner's lighting rules: natural light set into walls and vault, artificial sources hidden, placement staggered in three dimensions, the upper space lit.
- **Round 3 rulings (content issue 168)**: the journal restates only what the story has told (seventeen objectives titled, twelve with a hint; untold objectives untitled); fourteen of the sixteen interact objectives sit on a prop block; the notice and Wenna say the party came to find out what is happening and stop it, the return's closing line says plainly that the catastrophe was not averted; Marrack rows, with his declarations at the oars of each skiff copy so a carry never moves him, and after the crossing back his talk opens on a repeatable exchange; the outbound crossing is one shot then the carry, the crossing back plays its reveal once; Davey says plainly which valve is right, no line narrates the heartbeat, every line addressed to the party reads right for one player or four.
- **zh-cn**: one rendering per name (额石, 探海者, 温娜, 特雷加尔, 剥鲸铲, 溺亡者, 朝圣者之路, 窄口, 小艇, 打捞船, 渡屋, 山脊), no 你们 aimed at the party; transcreated, not translated.
- **Round 4**: the fish-market wave is a titled objective restating Wenna's warning and nothing more; fights no line has announced stay untitled beats (`DW0863` refuses a titled-less `kill`).
- **Round 5**: far views the engine cannot serve (`DW0956`, 512 blocks) are re-aimed at the farthest servable thing, `world.view_distance` 30, and the body is first seen whole from the Narrows; quiet fights (spec-0093) spawn from approach triggers in the place they are fought; `guidance.markers: hidden`, with props on pressables (black banner on the wool picture, red mushroom block on the valves, a bell as its own detector, heavy core as the Customs House padlock, nether wart block as the diaphragm); the crossing back's ordinary branch is one ten-second shot and the carry. The Narrows tentacle locks nearest player on its shelf, three reaches, every fourth blow the retract holds, the twelfth sends it down for good, no text.
- **Round 6**: the heart's valves read the round once into a scratch datum (`state/valve-right`), take back the standing wound, run the wrong press's lines and reset or the right press's beat, wound swap and advance off the scratch datum, then clear it (a right press must not undo itself, `DW0985`; `DW0527` clean). With the spine open both ways the leg to the landing skipped the Run, so at the cut the bar falls again (`close-gate`, happening `seals`), as `DESIGN.md` row 31 says.
- **Round 7**: the sea fog over the open water is painted at the lamps beat, not the notice (the coach stop lies past the declared 480 blocks from the fog's region; the lighthouse is the first beat from which that water is seen). The far bell's ringer stands at its own station.
- **Tentacle strikes**: only the Narrows tentacle strikes. The Jaw Bank, Rib Cathedral and Crown tentacles do not strike yet: a lock's landing region is a box centred on an anchor, every cell 5 to 19 blocks from the mark (`delvec rig describe rig/tentacle`), off the way, 3 blocks from any drop, so each owes a landing station of its own beside the way. Strikes written for them were parked and are deleted with the old map; they are rewritten against the new map's anchors (`DW0968`: the blow must lie inside `while_in`). Ranged hits on tentacle hitboxes are settled as melee only (spec-0082 §8).
- **Small craft** (cited or authored; ideas only): the skiff has stem, transom, keel line, sheer, gunwale, thwarts and tiller at block scale (Wikipedia, *Whitehall rowboat*, *Dory (boat)*, CC BY-SA); the sheer rises forward, depth forward > aft > amidships (Glen-L 17' Whitehall plan listing); skiff 10 x 5 is authored (a pulling boat runs about 3.8; this one carries four and an oarsman); the launch is about 20 x 6, between a 33 x 8 ft steam launch of 1874 and *Branksome* (National Historic Ships register no. 2); its deckhouse aft, mast, rubbing strake and bow bulwark are authored.

## The exterior each place needs

A design requirement for the new map: a building reads from outside as the thing it is, and an open place stays open.

| place | open or enclosed | roof form | facade |
|---|---|---|---|
| Coach Road | open | none | drystone parapet on the drop, rock bank behind, the coach stop's timber shelter |
| Cliff Steps | enclosed | slate roof stepping down the cliff with the flight | rubble walls |
| High Street | open | the terraces behind its fronts: pitched slate roofs, ridges along the street, chimneys at party walls | its own street fronts |
| Harbour Office | enclosed | slate gable, ridge east-west, chimney | two-storey stone house; street door on the upper floor; a window over the harbour |
| Coyle House | enclosed | pitched slate roof, chimney | single-storey limewashed cottage, small window, plain door |
| Fish Market | enclosed hall, open on the seawall side | long pitched plank and slate roof, ridge north-south | timber frame on a stone footing; open arcade with awnings to the seawall; sea doors to the slipway |
| Seawall | open | none | parapet with bollards; the harbour fronts along the north |
| Seamen's Chapel | enclosed | steep slate gable, ridge north-south, a bell-cote on the south gable | rubble stone, tall narrow windows, door in the gable end |
| Chapel Crypt | below ground | none (buried) | none |
| Customs House | enclosed | hipped slate roof | dressed stone, a door on the seawall with a lamp each side |
| Net Lofts | enclosed | pitched plank roof | plank loft with a loading door over the harbour |
| Boatyard | open (the emptied basin) | none | quay walls with their steps |
| Whalers' Shed | enclosed | tall timber gable with a louvre | plank walls, big doors |
| Ropewalk | enclosed | long low pitched roof, rising over the stair at its south end | timber |
| Breakwater, Slipway Stair, Pier | open | none | stone arm with parapets; stone slip walls; timber deck on piles |
| Lighthouse | enclosed tower | lantern room glazed all round under a cap | white stone tower with a gallery |
| Pilgrims' Way, Wreck Field, mud fields, Narrows Shelf, Carved Pillars, Skiff Stage, Marrack's launch, Mast Platform | open | none | the flat itself; the mud fields stay open to the sea to sink |
| The Narrows | open | none | a ridge three stones wide between water |
| Near and far ferry houses | enclosed | slate roof | stone walls down to the sea floor, the water gate shut |
| Far Landing, Jaw Bank, Flank Ridge, Tail Bank, Tail Road, Run Bank | open | none | the body's bank |
| Mouth to Spine Stair | inside the body | the body form | the body form |
| Crown, Brow, Back, Tail Flank | open, on the body | none | the hide; drops at the edges visible |

## Open items

- **Engine capabilities not yet built** (engine work is in progress before map building resumes): the out-of-sight check for the two skiffs, the watcher, and the heartbeat. A part of the campaign that needs one waits for the release and is not worked around.
- **Waits on the engine** (see `DESIGN.md`, *Waiting on the engine*): the Figure, the lightning and the party's stand-ins in the reveal; the obfuscated line; a visible press object for every `use` trigger and for the Customs House lock and the diaphragm; progress that does not hang on reading an object; tentacle lock, re-arm and perception range.
- **Sculk (engine issue #1007)**: `sculk` and `sculk_vein` are allowed. `sculk_catalyst`, `sculk_sensor`, `calibrated_sculk_sensor` and `sculk_shrieker` stay refused until a spec exists; `DESIGN.md`'s heart mechanism counts on sensors and a shrieker, and a mechanism that counts on them is blocked.
- **Engine issues #1004-#1006** are fixed in engine main and no longer constrain the campaign.
- **The fog repaint distance** (lamps beat) is not proved on a ladder run.
- **Far-landing placement**: the body's stamp was placed from `node/far-landing`; the new map states what the body is placed from.
- **The ladder** (PackTest, bot, branch runs, muster, staging gate, Chunky frames) is run on the new map; none of an earlier map's results carry over.
