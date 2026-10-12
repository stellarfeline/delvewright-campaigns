# The Stranding — generation record

The campaign's own decisions, as its author records them. `DESIGN.md` is the design of record; this file says what was pinned by the brief, what the toolchain is, which decisions stand, and where the map restarts.

## Toolchain

- Engine: `delvec` built from source at `a7f3f621ee8fc22d29f06e9ae298383b88126056` (`cargo build --release`), `delvec 1.12.0, dsl 0.39.0, mc 1.21.11`; the `/new-delve` skill of that tree, plugin version 1.12.0.
- Prefab library: this content clone's `prefabs/`; every `the-stranding-*` piece is detailed from `programs/` by `delvec detail` or sculpted from `forms/` by `delvec sculpt`.
- Generators: `generators/` (Python, standard library only) write the site plan, the layout graph, the geometry brief, the terrain, the body form and every place's program; `delvec` does every expansion, gate and write.
- Reference images: `gemini-native`, model `gemini-3.1-flash-image`, series anchored with `--chain-from`, style contract in `--style-note`.
- The engine's other half of its constitution (`CLAUDE.local.md`) is not available to a run; nothing here concerns dispatch, review, merge or staging.

## What the brief pinned

`DESIGN.md` is a detailed brief, so it is honoured exactly and nothing is showcased beyond it: four acts and thirty-six places in the order it gives, the cast of four, the four classes and their kits, the fights and tentacle counts, twelve cutscenes, the two endings, the danger model, the light plan, the hour (`night`, `clear`, full moon). `DESIGN.md` § Posture is the posture note: escalation is uneven, people name their fear, and the ending does not explain itself.

## The map

Rebuilt from the site-plan step on the current route; nothing of an earlier map is reused. One geometry model (`generators/mapmodel.py`) states the places, edges, seams, stations and datums and writes `geometry-brief.json`, `layout-graph.json`, `site-plan.json` and `terrain/site.png`. Fifty-five places in the order of `DESIGN.md`, four acts:

- Act 1, Wrackham: the coach road down the cliff steps and the High Street to the harbour lane, the houses, the fish market, the basin, the seawall, the chapel and its crypt, the Customs House, the whalers' shed, the ropewalk, the breakwater and the lighthouse, the pier, and the slipway stair onto the flat.
- Act 2, the Crossing: the Pilgrims' Way with the mud fields either side, the wreck field, the carved pillars, Marrack's launch and its mast platform, the Narrows and the shelf beside them, the skiff stage and the two ferry houses, the sea skiff.
- Act 3, inside the body: the far landing, the jaw bank, the flank ridge, the mouth, the throat, the rib cathedral, the stomach, the heart chamber, the breach, and the neck stair in two places of 20 rise each up to the blowhole.
- Act 4: the crown, the brow, the back in three terraces, the tail flank, the tail bank, the tail road and the run bank.

The body is one sculpted piece (`forms/the-stranding-body.json`, `prefab/the-stranding-body`), stamped by `world-edits.json` relative to the jaw bank. Each place inside it is cut out of the form a cell wider than its claim (except where it opens out of the body), each place on it is cut from a course under its floor, so the stamp lays nothing on what the places' own pieces draw.

## Standing decisions

Story and mechanic decisions that do not concern map geometry.

- **Seed** `1919`. **Difficulty** `normal`. **Horizon** `ocean` (sea level y 62 under the flat's mud at y 64), `boundary` carries a message.
- **Atmospheres**: `wrong-place` (olive sky, close yellow fog, red clouds, no music), `inside-body` (dark red, close fog, no music), `red-night` (the body, the bank and the flat after the cut), `sea-fog` (the endings). The flat and the mud fields carry `wrong-place` from load; the places inside the body carry `inside-body`; the far bank and the body's outside are painted `wrong-place` at the lamps beat, so no paint boundary falls at the mouth or the breach (`DW0929`); at the cut everything outside turns `red-night`.
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
- **Tentacle strikes**: only the Narrows tentacle strikes, from its shelf; its lock region lies 5 to 19 blocks from its mark and its blow inside `while_in`. The Jaw Bank, Rib Cathedral and Crown tentacles rise and can be struck down and retract; their strikes wait (see *Waiting on the engine*). Ranged hits on tentacle hitboxes are melee only (spec-0082 §8).
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

## Map decisions

- **Placement**: the town on its terraces at the north, the Pilgrims' Way running south across the flat between mud fields that tile it to the sea, the Narrows and the skiff stage at the black water, the body lying head north across the channel with its bank all round. Every open place meets its neighbour along their whole shared front (a contact as high as the lower of their skies); ring cells where two places touch outside a seam carry a post, so no place leaks into another (DW0836, DW0838).
- **The body** is one sculpted piece; its inside places are cut from the form and drawn by their own pieces in flesh, bone and sculk, lit by what grows in it (glow-berry strands staggered tile to tile, shroomlight in the vault and the walls, glow lichen) and by Marrack's lamps recessed behind a lip of flesh; its outside places are slices of the sculpt with their own floor course. The flanks fall sheer to the mud and an apron of hide fills the strip to the east bank, so nothing overhangs walkable ground and no channel of sea lies along a bank.
- **The neck** is two places of 20 rise each (the spine stair and the spine top), because one place may hold at most one floor and a stair's rise is an edge's.
- **The Brow Stone** is a two-block-deep tablet in the forehead, its face toward the crown; the cut is made standing on the brow.
- **The basin** is entered by dropping two from the quay edge (a one-way contact); it is left by the slipway into the market. The pier meets the lane along its whole landward end; the market's arcade meets the seawall along its whole south side.
- **The sea** stands in every hollow of the site under y 62 and under each mud field's crust (world-edits batch `the-sea`, after the body): the open fill lays ground and nothing over it.
- **The sinking** takes each mud field whole (each centred clear is joined by the strip it leaves, stations `anchor/sink-*`); a course of stone one under each field's crust, under its ring and first row, is the step a swimmer climbs out by once the mud has gone, and a field's edge on the open sea alternates such steps with a half step of crust.
- **Slip steps**: each ferry house's slip has a stone at each end a swimmer climbs out by (DW0322).
- **The stomach pool**'s bone curb stands two high, because the Drowned fight on its shore and would step into the killing volume (DW0922); the whole pool is the killing volume, so the pool cannot be entered — a departure from `DESIGN.md` row 28's "entered only by climbing over the curb".
- **The tail** stands sheer out of the mud and the tail flank comes down to the bank by steps of hide (a stair, not a drop): the back is reached only by the spine stair.
- **Hosted stairs** are walled at both sides past a climber's head, so a flight is climbed from its foot (DW0430).
- **The skiffs**: each carry takes the whole skiff and its tiller's reach; the tiller's head stands on the rudder post over the carried volume (DW0932, DW0542, DW0963).
- **Showcase cameras** (`design/cameras.json`): all 81 re-aimed at the new map as estimates, each lens in open air (`delvec cameras --preview`: 81 of 81 clear, 81 of 81 approved images answered).
- **The Run**: the bank falls behind the party one section per lamp stake, each stake setting a checkpoint at itself; the hole is one course deep and carries no killing volume (see *Engine findings*).
- **The throat** keeps its six-block bays, everything in it repeating with the ribs, ready for the endless corridor; the loop itself is not authored (see *Waiting*).
- **The watchers** turn to face the nearest player within 16 (street), 24 (flat) and 10 (heart) blocks (spec-0101). **The heartbeat** sounds through the inside every 30 ticks inside the body once the skiff is lent and until the beat stops, and every 14 ticks, higher, in the heart chamber (spec-0102). **Sculk**: sensors across the heart chamber floor and one shrieker in its corner, summoning off (spec-0100).

## Waiting on the engine

- **The out-of-sight check for the two skiffs** (brief): the near and far skiffs stand inside their houses as built; nothing proves a player cannot see both at once.
- **`DESIGN.md` *Waiting on the engine***: the oarsman's obfuscated line; the striking of the Jaw Bank, Rib Cathedral, Crown and Run tentacles (they rise, can be struck down and retract; only the Narrows tentacle strikes).
- **The endless throat**: the loop (spec-0086) holds until the wrong rib is struck, and the wrong rib's interaction body stands inside the loop's span, which `DW0948` refuses (a body moved a bay back would see it twice). The release `DESIGN.md` gives cannot be declared; the throat is walked straight.
- **The Run's killing volume**: `DW0891` refuses a staged volume whose keep-out reaches the floor in the configuration before its flip, and prescribes a volume on an anchor at the pit's bottom; the pit's bottom is a sealed hollow under the bank until the fall, and `DW0845` refuses an owed anchor that resolves into a `no_body` region. The collapse and its checkpoints stand; a fall costs nothing.
- **The sea skiff** (`node/sea-skiff`, reached only by the crossing's carry) stays a stand-in: a place joined only by a `carry` edge cannot be detailed (the contract owes an exterior walk edge on its entry while `DW0844` refuses any face no seam allocates).

## Engine findings (met while building this map)

Each is recorded with its diagnostic and a minimal reproduction; none was worked around outside the skill.

- **A carry-only place cannot be detailed** (`node/sea-skiff`). `contract-well-formed` requires an `exterior` edge of a traversal class on the entry space, while `DW0844` refuses any declared face no seam allocates; a place whose only edge is a `carry` has no seam. Repro: a site plan with a box joined to the rest only by a `carry` edge; `delvec detail <campaign> node/<box>`.
- **A plan edit cannot be absorbed by `detail`**: after a seam or owed-anchor change, `delvec detail <place>` and `delvec detail --all` (the step `references/detail.md` prescribes "after any plan or graph edit") both refuse up front with `DW0844`/`DW0845` on every *other* row the change made stale, so no row can be re-made. The documented procedure has never run green on such a change. Used here: delete the affected rows from `detail-plan.json`, then `--all`. Repro: change one contact's extent between two detailed places; run `delvec detail . --all`.
- **The staged-pit pair**: `DW0891` refuses a staged killing volume whose keep-out reaches floor in the configuration before its flip and prescribes "an anchor at the pit's bottom"; a pit opened by a `clear-region` has its bottom in a sealed hollow, and `DW0845` refuses an owed anchor that resolves into a `no_body` region. The prescribed remedy is unreachable. Repro: a floor course over a sealed two-high hollow claimed `no_body`, a station in the hollow, a `lethal_volumes[]` row on it gated by a flag a trigger sets beside a `clear-region` of the floor.
- **A loop cannot be released by something inside it**: `DW0948` refuses any body (an interact objective's interaction) inside a loop's near field, and the span of a twelve-block loop covers a whole thirty-block corridor, so `DESIGN.md`'s "striking the wrong rib releases the loop" cannot be declared.
- **The stamp writes into bound frames silently**: a world-edits `fragment` lays its non-air cells over every bound place's frame (`DW0210`, `DW0311`, `DW0430` reported the consequences, never the overlap); with a sculpted form, the dressing of a cut's faces lands inside the cut. Repro: cut a box from a form exactly at a place's claim; stamp it; the place's ring and lid hold slabs and stairs.
- **The open fill floods nothing**: an `open` site's heightmap below the ocean horizon's sea level is dry inside the region (the channels were pits); the sea had to be filled by world-edits. A `replace` matching `minecraft:air` matches nothing in empty model cells.
- **Generated `pulse_<s>_shut` PackTest is not isolated**: it asserts `schedule clear` returns 0 without clearing first, while other generated tests that set the pulse's gate flag run beside it and the tick edge starts the chain; `pulse_heartbeat_shut` fails ("Expected #pclr_heartbeat dw.sys to match 0, but got 1"). Repro: a gated pulse whose gate flag any quest or trigger test sets.
- **The bot ladder does not wait for the delve to be placed**: the harness takes its first leg as soon as the login window closes, while the datapack is still placing (`#placed dw.sys` is what `world-save.sh` waits on; nothing in `bot-run.sh` or the harness reads it). On this map placement outlasts the login window: one run walked leg 1 from the world origin (`No path to the goal!`, bot at `[10.5, 57.7, 8.5]`), the next was teleported to the entry spawn mid-leg (`The goal was changed before it could be completed!`); an earlier run of the same course passed step 1. Repro: any map whose placement takes longer than the login window; run `validation/bot-run.sh`.
- **`open-gate` misses a bar the server has re-connected**: the gate writes `fill … air replace minecraft:iron_bars[east=false,north=false,south=false,…]`, and a row of bars placed as written is re-derived by the server to `east=true,west=true`, so the gate matches nothing and the seam never opens (the far land door stopped the bot at critical-path step 21). Used here: barred seams are shut with dark oak planks, which carry no connection state. Repro: a barred seam two or more cells wide, opened by `open-gate`.
- **The written world leaves stone out under two stretches of sea**: `DW0955`'s model class holds 3744 cells, written air and server stone, at y47..54 in x61..67 z447..458 and x69..116 z91..98 (the server holds stone to y54 and water above; the model holds air from y47 up). The two stretches are exactly the footprints, with their one-cell rings, of the two places that stand over open sea: `node/pier` and `node/sea-skiff`.
- **Friction**: one global `~/.delvewright/env.sh` names one engine tree; detailing one place re-runs the whole build (about ten minutes on this map) while `--all` re-makes all 54 places in about the same time; adding stations to two places at once deadlocks per-place detail; the light probe needs a side entrance on top-entered pieces; through-floor stair contract patterns (top tread in the hole, head clearance over the two top treads) are undocumented.

## Open items

- **The fog repaint distance** (lamps beat) is proved by the build, not walked on a ladder run.
- **The critical path is long**: 3030 blocks of measured route, about 51 minutes of walking at the engine's provisional pace (`DW0822`), against `target_minutes` 150 for the whole delve.
