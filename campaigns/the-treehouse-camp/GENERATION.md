# The Treehouse Camp — generation record

## Toolchain

- Built on spec-0098 (a place owns its outside; boxes as cuboids; `fill: open` over heightmap terrain; seam `form`; the per-place handout; the contract `climb` edge; ADR-0032) and spec-0099 (a body climbs), at the engine revision the last section names. No release carries them yet.
- Placement: a site plan. The camp's exterior is the whole point: four giant trees and their houses, seen from the ground, from each other and from the top.
- The reference views were drawn with `tools/creator/refimg.py` on `gemini-native` (`gemini-3.1-flash-image`). Before the series, the provider's image input was checked two ways. First, a probe image of a red triangle and a magenta square on yellow was passed as `--style-ref` with a prompt that named neither shape nor colour, and it came back as the same picture. Second, the probe call's sidecar reports 1120 image input tokens.
- The engine constitution's operating half (`CLAUDE.local.md`) was in force for this run.

## What the brief pinned, and what was invented

Pinned: a clan's camp deep in a great forest, in the spirit of the great tree villages of a well-known film; several treehouses built around the waists of several giant trees; rope ladders and rope bridges between them; houses at different heights, on trees growing from ground at different heights; small and refined. A showcase of 15–30 minutes for 1–4 players, with no combat or very little.

Invented: everything named in `DESIGN.md`: the Greatwood, Lantern Night, the four trees and five houses, the cast, the quarrel, and the route. "In the spirit of" is taken as one idea only (people living high in giant trees, moving on rope). No franchise name, likeness or design is used (`DESIGN.md` §1).

## Posture note

This campaign pushes three axes off the machine default (skill *writing craft* §B). **Feelings are named outright**: Tobi says he is afraid of the ladder, and Oru says she is sad not to climb. **A subplot is left unresolved**: Neve and Hessel's quarrel over the Low Bridge is told from both sides and never settled. **The escalation is uneven**: a quiet errand ends in one beat larger than all the rest, when the whole camp lights up at once.

## Decisions

- No combat. The showcase is the place and the climb.
- The level exists to prove building and connecting several structures in boxes at different `y` heights. One site plan, one `open` site, eleven boxes: nine entered places (one ground place, the Hearth, Loom, Seed and Watch Houses, the Watch Crown, three rope bridges) and two scenery places (Watch Roots, Hearth Crown).
- Geometry is re-derived from reference view 4, which governs where the views disagree: the four trees stand at the corners of a square, with bridges on three of its sides.
- Each tree is split a different way. The Watch Tree is three stacked boxes: scenery roots, house, entered crown. The Hearth Tree is three: entered glade, house, scenery crown (its crown is wider than its house's eaves reach). The Seed Tree is one box with a `roof`-zone crown. The Loom Tree is one sky-open box on a topped trunk with no crown.
- The bridges are sky-open (`ceiling: {open: n}`), with headroom enough for the plank steps each hosts (4–6 high), and hang one course of beams under their decks (`base: {aloft: 1}`).
- The forest floor is the commons and no place. A body that reaches it walks back to the first ladder through the Root Glade.
- Every ladder hangs on bark or on a post, because a vanilla ladder needs a sturdy face behind it.
- The delve ships in English and Chinese (`l10n/zh-cn.json`), transcreated on DeepSeek by `tools/creator/i18n-translate.py` and held to one rendering per place name by hand.

## Capability findings

The four engine gaps this design was written against, and where each stands:

1. **A seam aloft stood on a column of earth.** Corrected in spec-0098 (correction 1: a seam aloft fixes no earth), and boxes now hang (`base: aloft`). Closed.
2. **No edge class meant "climb".** The layout graph has `climb` (correction 2), and a piece's contract has a `climb` edge for a ladder between two of its own levels (departure 33). Both are used here. Closed.
3. **The forest floor is dressed by a world edit, not by a place.** Confirmed: the lantern posts on the commons are set by `world-edits.json`. Ferns, logs and small trees on the commons would go the same way; none are added yet.
4. **Scenery places.** `reached: false` is declared on the Watch Roots and the Hearth Crown, and the battery proves both not reached. Closed, with the light pair in the round record below.

## Build round on engine 442c3e7c (dsl 0.38.0, grammar program 1.10.0)

Built with `delvec 1.11.0, dsl 0.38.0, mc 1.21.11`, force-rebuilt in release mode from the read-only engine tree at `442c3e7ca2ce52e52ac208d4cd361d82037dea65` (cargo exit 0) and invoked by path. The skill pages are read at that revision. The toolchain's `env.sh` is not used: the engine this level needs is not released.

Each place is a grammar program under `programs/`, written by `design/programs-src/places.py` (the design, in world coordinates, from each place's handout fetched at run time) through `design/programs-src/thlib.py` (states completed from the pinned registry; contract regions cut out by guillotine; the rest band-compressed). `design/programs-src/lights.py` lists the finale's 23 lantern lines, read both by the pieces (their marks) and by the quests (their `fill-region` boxes). `terrain/heightmap.py` writes the forest floor; `terrain/lanterns.py` writes `world-edits.json`, the lantern posts on it.

### State

- `validate`, `analyze` and `build` exit 0; `detail --all` exits 0. Blockout: 11 places detailed, 0 stand-ins. Battery: 11 places reached, 2 of them scenery, proven not reached. All 15 identities hold, the four trunk spacings exactly (44, 42, 42, 44).
- DW0311: 8 of 8 legs walked. DW0921: 39,760 cells a body can reach, 0 it cannot leave.
- PackTest: 41 of 41 required tests pass.
- Bot critical path: **red**, blocked by the toolchain defect in the next list.
- Staging gate: stageable, no override.

### What the engine still bends, and what it no longer does

Undone on this engine:

- **Way width (`DW0825`).** The bridges are 3 wide and 22, 20 and 22 long, at the designed trunk spacing.
- **The lookout as its own box.** The Crown Lookout is a second level inside the Watch Crown, joined to the landing by a `climb` edge of the crown's contract.
- **The spacing identities.** They are exact again (`eq`). DW0833 reads each floor's centre.
- **Size and way classes.** None is declared.
- **The forest floor.** The bridges, the Hearth House and the Watch House and crown hang (`base: aloft`). The forest floor under and between them is the commons, walkable everywhere: the terrain is a harmonic field between the four ground pads and the rim, with no step over one block and no pit. The Root Glade opens onto it, so a body that reaches the ground walks back to the first ladder.
- **The sealed lit hollows.** The scenery pieces no longer carry them.

Still bent (recorded here, not worked around):

1. **The Root Glade is 20 × 20, not 24 × 24 (`DW0827`).** The glade's open headroom must reach y 84, one course under the Hearth House floor, for the climb into it. At 24 × 24 its ring column (x 48 and z 48) shares cells at y 78–84 with the Long and Low Bridges' undersides, and no seam joins the glade and a bridge to award them. Reproduced on this engine: "the cuboids of `node/long-bridge` and `node/root-glade` all claim 30 cell(s) and no rule awards them" (and 20 for the Low Bridge).
2. **A scenery piece with standable surfaces owes light.** Departure 32 lets a scenery piece state zero standable cells only when none of its cells is standable. A crown's leaf tops are standable, so its contract must declare one standable cell in a space (`contract-reachability` refuses a space with none), and the build's DW0210 then holds that cell to light 3. The Hearth Crown answers with the hall's festival lanterns, hung from its great arms over the platform, beside the declared cell on the east arm.
3. **Toolchain defect: a climb is exported across two ladder columns.** Leg 6 of `validation/critical-path-waypoints.json` carries one climb with `bottom` [74, 84, 78] and `top` [74, 111, 79]. The body climbs the Watch House ladder (column z 78) into the landing's hole, steps over the top onto [74, 93, 79], which is both standable and the foot of the crown's own ladder (column z 79), and climbs that to the ring. The exporter does not end the climb at the standable cell, so the two columns are merged, and the harness refuses the record: `waypoints/legs/6/climbs/0 bottom and top must be one column, bottom not above top` (bot exit 1). The ladders are not moved to dodge it.

### Visual review (Chunky, pinned core, 150 samples per frame)

Rendered from the build tree `out/build-r4` and its world save; the frames stand in `out/renders/` beside the build, which is not tracked. 15 of the 178 scenes `render-shots.sh` emitted are rendered: the five showcase cameras, and one or two eye-height POVs per walkable place. The other 163 are not rendered. Every frame carries the declared hour (late afternoon); no frame shows the night of beat 7 as night.

| Frame | Answers | Does it read as the thing |
|---|---|---|
| `camera_north-east-aerial` | view 4 | Yes. Four giant trees on a square; the Loom House in front on its topped trunk; bridges to the Hearth House (two thatched cabins) and to the Watch Tree, whose lookout ring stands over every crown; the Seed Tree behind. The forest floor round the camp is bare moss under the valley rim, not the forest the view draws (the horizon is `valley` until the engine has a forest one). |
| `camera_from-the-south` | view 3 | Yes. The Seed Tree left, the Watch Tree right with its landing and the lookout above everything, the bridges between, lamp posts along the paths below. |
| `camera_plan` | view 2 | Yes. North up: the Hearth crown north-west, the Loom platform north-east, the Seed Tree south-west, the Watch Tree south-east, three bridges, none on the south side. |
| `camera_from-the-glade` | view 1 | Partly. Under the Hearth platform among the buttress roots, the Long Bridge leaving right toward the Loom House. Dark under the deck, and the rope ladder (on the trunk's west face) is out of frame. |
| `camera_lantern-night` | concept/lantern-night | The lanterns, yes: from the lookout, every rail and bridge below is lined with lanterns, the Hearth Tree ahead. The night, no: the frame is drawn under the declared late-afternoon sky. |
| `pov_leg0_wp6` | Root Glade | Close against the trunk and its two-wide rope ladder; the bark and roots read, the glade's space does not. |
| `pov_leg2_wp3` | Hearth House | Wedged between the stone chimney and cabin B's door, under the thatch; reads as a hut by a hearth, cramped. |
| `pov_leg2_wp16` | Long Bridge | Yes: a railed plank deck running to the Loom House's framed gateway, its thatch cap and lanterns. |
| `pov_leg2_wp21` | Loom House | Yes: the topped trunk's red end grain in the deck, the lean-to's post, the rail and a lamp post, open to the sky. |
| `pov_leg6_wp4` | High Bridge | Yes: plank steps climbing into the Watch House under its crown, the lookout ring high above. |
| `pov_leg6_wp10` | Watch House | **No: nearly black.** The crown's leaf floor course, which `DW0836` requires closed over the Watch House (a stacked plane with a seam is wall except at its opening), roofs the platform; it reads as a dim box even by day. DW0210 passes there. A finding for the next round. |
| `pov_leg6_wp24` | Watch Crown (the lookout) | Yes: the plank ring round the trunk under its last branches, a chain lantern, the rail. |
| `pov_leg6_wp31` | Watch Crown (the hook) | Looks east, out over the valley rim, away from the camp: the height reads, the camp does not. |
| `pov_leg4_wp11` | Low Bridge | Yes: the plank steps up into the Hearth House, the chimney ahead, the huge crown over it. |
| `pov_leg4_wp1` | Seed House | Yes: the deck under its crown, a chain lantern, the gateway to the Low Bridge, the Hearth House beyond. |

The two scenery places are seen, not entered: the Watch Roots in `camera_from-the-south`, the Hearth Crown in the aerial and the plan.

### Design decisions made in this round

- Every rail is two fences high. A finale lantern line is a station, and a station stands in play space, so the ring rows are part of each floor's space; Lantern Night swaps the rail's top course for lanterns. A platform corner is a single fence.
- A place's plane with its bridge is closed above the 3-high mouth (`DW0836`), so the Loom House's and the Seed House's bridge mouths are framed gateways.
- The Watch Crown's floor course is leaves round the landing's planks (`DW0836`). The Watch House's ladder tops out in the landing's hole; the crown's own ladder starts on the landing beside it and climbs a flute in the bark (ribs either side, clear air west of it) to the ring, so a climber can step off only onto the landing or the ring (`DW0921`).
- The forest floor is lit by design: 29 lantern posts under the three bridges and round the trees' feet, set by the edit script. The plan declares no `lighting`, so the relight pass sets no torch.
- The three vistas' eyes stand at y 115 on the lookout's rim: the DDA counts the one-fence rail as solid at a standing eye.
- Lantern Night's sky is `{"moon": "high"}` under the world's new moon. `concept/lantern-night` records it: drawn earlier, and **waiting on the owner** (design/README.md).

## Build round on engine f3d18699 (dsl 0.38.0, grammar program 1.10.0)

Built with `delvec 1.11.0, dsl 0.38.0, mc 1.21.11`, force-rebuilt in release mode from the read-only engine tree at `f3d18699bc8ee651b7f69d67ac53f485efebd96e` (cargo exit 0; binary sha1 `5989d7cb…`) and invoked by path. The tree was first built on `cbf56248` the same day; that engine drew a setting sun as full night, so every frame rendered on it is void and none is cited here. The pieces did not move between the two engines: `detail --all` on `f3d18699` rewrote no prefab byte.

### State (build tree `out/build-r7`)

- `validate`, `build` and `detail --all` exit 0. Blockout: 11 places detailed, 0 stand-ins. Battery: 11 places reached, 2 of them scenery, proven not reached. All 15 identities re-measured with no DW0833.
- DW0311: 8 of 8 legs walked. DW0921: 39,700 cells a body can reach, 0 it cannot leave.
- PackTest: 41 of 41 required tests pass.
- Bot critical path: **red** (exit 1), on the engine defect named first in the next list. Climbs driven: 1, the glade ladder (14 rungs, [30, 72, 36] to [29, 86, 36]). The two climbs leg 6 now exports, one per ladder column ([74, 84, 78] to [74, 92, 78], then [74, 93, 79] to [74, 111, 79]), were never reached.
- Staging gate: stageable, no override (122 finding classes, 64 inapplicable). It admits this build with its bot red and its floors holed (below).
- Showcase cameras: 5 of 5 approved images answered; the lens is clear of every block by 0.25 (0 flagged).

### Undone on this engine

- **The Root Glade is 24 × 24**, square under the Hearth House, at min [24, 24], with its ladder seam at [6, 11]. Spec-0098 departure 35 gives the bridges the cells of their undersides that hang in the glade's sky ring, and DW0827 does not fire. The terrain pad under it widens to x and z 21–50, so its ring ground meets the forest floor: at the old pad, DW0885 named 43 exposed ring cells.
- **The scenery crowns declare no standable cell.** Each scenery contract's one space is two cells of air at the top of a column of its frame. `delvec detail` excludes 631 standable cells (Hearth Crown) and 244 (Watch Roots) from its light probe.
- **The Watch House under its crown** carries seven lanterns on chains hung from the canopy round the trunk. The crown's leaf floor stays: the house is a platform under a canopy.
- **The lantern hook** moves to the ring's north-west, at [74, 114, 73].
- **The from-the-glade camera** stands at the glade's south-west, at (19.5, 75.5, 45.5) with yaw 228, pitch −14 and fov 80, above the lamp posts. From there it looks at the trunk's west face, where the ladder hangs.

### What the engine still breaks or bends (recorded here, not worked around)

1. **Engine defect: a piece's `structure_void` cells are written into the world.** `place_all` places each piece with `place template`, in site-plan order, and the game writes the `minecraft:structure_void` the piece holds at every frame cell its place does not own. Where the voiding piece is placed after the owner, its void replaces the owner's blocks. The engine's model reads those cells as showing the owner through (compiler.md, "the game places"), and so do the worlds `delvec cameras` writes. Measured with `tools/lib/anvil.py` (the engine's own reader):
   - The server-saved world `out/build-r7/world` holds 6,607 structure_void blocks in four clusters:
     - the Seed House frame, 6,527 cells over x 23–48 × y 69–88 × z 65–90, which takes out the Low Bridge's last four deck rows and rails (z 65–68);
     - 20 cells at the Hearth House's south ring (x 33–37, y 85–88, z 48), the Low Bridge's mouth, floor course included;
     - 20 cells at its east ring (x 48, y 85–88, z 33–37), the Long Bridge's mouth;
     - 40 cells at the Loom House's south ring (x 77–81, y 78–85, z 44), the High Bridge's mouth.
   - The world `delvec cameras` writes for the same build (`out/build-r7/showcase/worlds/at-load`) holds 0.
   - `place_verify` tests a frame corner `if block … minecraft:structure_void`, so the datapack expects the void blocks to be there.
   - The game reads a structure_void cell as air. The bot fell through the Low Bridge mouth at z 48 on build-r6: health 20 → 9, a 14-block fall to the forest floor. On build-r7 its pathfinder found no path south from the Hearth House ladder ([30.5, 86.0, 37.5], `No path to the goal!`). DW0311 and DW0921 pass, because they walk the model.
2. **Engine defect: the light survey grades a scenery place through the anchor the blockout synthesizes for it.** `anchor/node-hearth-crown` is resolved at [35, 95, 35], inside the trunk (`out/build-r7/creator-datapack/layout.json`). `owed_anchors` excuses scenery, but the blockout writes a node anchor for every box, and DW0210 floods from every point anchor in the area. Without its lanterns, the Hearth Crown fails the build: "3 of the 3 reachable walkable cell(s) … [32..33, 98, 32..33] at light 1". No DW0837 fires, so no body reaches those cells. The crown's eight hung lanterns stay, with the reason in `places.py`. This item is stopped.
3. **The hook frame does not face the camp.** A review frame's direction is the walk's last step, and the arrival frame `pov_leg6_wp15` looks out over the valley rim. The lookout's view of the camp is the showcase camera `lantern-night`.

### Visual review (Chunky, pinned core, 150 samples per frame, engine f3d18699)

The frames are in `out/renders-r7/`, beside the build, which is not tracked. 16 of the 157 scenes `render-shots.sh` emitted are rendered: the five showcase cameras and 11 eye-height POVs. The POVs load the server-saved world, holes included; the showcase cameras load the world `delvec cameras` writes, which has none.

| Frame | Place or image | Does it read as the thing |
|---|---|---|
| `camera_north-east-aerial` | view 4 | Yes, under a sunset sky: the Watch Tree's lookout over every crown, the Loom House in front, the Hearth House's two thatched cabins, the Seed Tree, every rail and path lit. |
| `camera_from-the-south` | view 3 | Yes: the Seed Tree left, the Watch Tree right with its landing and lookout, the bridges between, lamp posts on the forest floor. |
| `camera_plan` | view 2 | Yes: four trees on a square, three bridges, none on the south side. |
| `camera_from-the-glade` | view 1 | Yes: the Hearth Tree's trunk with its rope ladder, the platform’s underside with its hung lanterns, the buttress roots and lamp posts, the Low Bridge leaving right. |
| `camera_lantern-night` | concept/lantern-night | Yes, as night: a black sky, the Hearth House ahead and every rail and bridge below lined with lit lanterns. |
| `pov_leg0_wp1` | Root Glade | Partly: under the platform among the lamp posts, a hung lantern and the trunk; a post fills the near left. |
| `pov_leg0_wp0` | Root Glade | No: it looks north out of the glade at the valley rim. |
| `pov_leg3_wp13` | Hearth House | Partly: the railed deck, its lanterns and the stone chimney at sunset; a corner post fills the left, and the cabins are out of frame. |
| `pov_leg2_wp16` | Long Bridge | Yes: a railed plank deck to the Loom House's thatched gateway. |
| `pov_leg2_wp21` | Loom House | Yes: the open deck, the lean-to, the rail, a lamp post, under the sky. |
| `pov_leg6_wp4` | High Bridge | Yes: the plank steps up into the Watch House under its crown, the lookout rail above. |
| `pov_leg6_wp9` | Watch House | Yes: the deck under the canopy, lanterns on chains, the rail and lamp posts. It no longer reads as a dark box. |
| `pov_leg6_wp14` | Watch Crown (the lookout) | Partly: the plank ring and its rail under the last branch, at sunset; the camp is below the frame. |
| `pov_leg6_wp15` | Watch Crown (the hook) | No: sky and the valley rim (item 3 above). |
| `pov_leg4_wp11` | Low Bridge | Yes: the plank steps up to the Hearth House, the chimney ahead, the crown over it. |
| `pov_leg4_wp1` | Seed House | Yes: the deck under its crown, a hung lantern, the gateway, the Hearth House beyond. |

## Build round on engine 3c5f1e81 (dsl 0.38.0, grammar program 1.10.0)

Built with `delvec 1.11.0, dsl 0.38.0, mc 1.21.11`, force-rebuilt in release mode from the read-only engine tree at `3c5f1e810d6a68805c9501fc7e5e42de370ae9e8` (cargo exit 0) and invoked by path. The bot image is built by `validation/bot-run.sh` from that tree under a fresh compose project. Every result below is from build tree `out/build-r9`, manifest sha256 `6f0d6228…`, unless it names another build.

### State

- `validate`, `build` and `detail --all` exit 0. All 15 identities hold. DW0311: 8 of 8 legs walked. DW0921: 39,700 cells a body can reach, 0 it cannot leave.
- The shipped templates in `datapack/` hold 0 structure_void blocks across 11 pieces. The server-saved world `out/build-r9/world` holds 0 (build-r7 held 6,607).
- PackTest: 41 of 41 required tests pass.
- DW0955, the written world against the server's world: green (`out/written-world-r9.json`). Of 71,333 cells in the layout box:

  | Class | Differing cells |
  |---|---|
  | model | 0 |
  | clock | 0 |
  | gravity | 0 |
  | fluid | 0 |
  | random-tick | 0 |
  | re-derived (fence and leaf properties a block update sets) | 6,996 |

- Bot critical path: **red** (exit 1); see item 1 below.
  - Steps 1–6 pass: talks to Tobi, Oru, Neve, Hessel, Oru and Neve.
  - Climbs driven: 1, the glade ladder ([30, 72, 36] to [29, 86, 36]).
  - Leg 6 exports two one-column climbs ([74, 84, 78]→[74, 92, 78], then [74, 93, 79]→[74, 111, 79]), and the harness plans both as climb hops. It never reaches the first.
- The step-4 refusal on build-r7 (`No path to the goal!` from the Hearth House) is gone. It was the void blocks at the Low Bridge's mouth (z 48).
- Staging gate: **refused**, given both records (`--run-report`, `--written-world`): "critical path: stage `critical-path` is RED". The written-world record is accepted.

### Content fixed this round

- **The Hearth Crown carries no lanterns.** The engine no longer synthesizes an anchor for a scenery place, and the design never asked for them.
- **Every hanging lantern hangs from something.** On build-r8, DW0955 named 12 hanging lanterns the server drops to air. Four hung under nothing: two on the Hearth House, one each at the Seed and Watch House huts. Eight in the Watch Crown's ladder flute hung under leaves, which cannot hold a hanging lantern (vanilla `LanternBlock.canSurvive`, via `Block.canSupportCenter`). `places.py` now refuses, at write, a piece with a hanging lantern that nothing holds; its check listed exactly those 12 cells. The four now hang on chains from the block above them. The eight hang from a stub of branch where the leaf was.
- **The Seed House composters are level 6.** A level-7 composter ticks itself to 8 (all 8 cells, DW0955).

### What still stops the ladder (recorded here, not worked around)

1. **Toolchain: the bot cannot walk along a ladder's face to reach the climb's bottom.** The Watch House ladder is two columns wide (x 74, z 77–78, facing west, on the trunk). Leg 6's route comes south along x 74, and its first climb starts at the far column, [74, 84, 78]. The harness walks to a climb's `from` with the pathfinder (range 1). The bot stops at [74.5, 84.0, 76.5], at the edge of ladder cell (74, 77), and times out after 60 s. The log says "nothing within 12 blocks — the refusal is about blocks".
   - Reproduced on build-r8 and build-r9.
   - In the server-saved world the cells are clear: deck at y 83, the ladder panel on the cell's east face, air above.
   - The glade climb passes because its route enters the ladder column from the side opposite the panel.
   - Unverified hypothesis: the pathfinder will not step into a ladder cell from the side, so the climb's `from` is reachable only from within the column itself. The two-wide ladder is the design (the seam's 1 × 2 opening) and is not narrowed to dodge this.

### Visual review (Chunky, pinned core, 150 samples per frame, engine 3c5f1e81, build-r9)

15 frames are in `out/renders-r9/`. The POVs load the server-saved world, which now equals the model.

| Frame | Place or image | Does it read as the thing |
|---|---|---|
| `camera_north-east-aerial` | view 4 | Yes, under a sunset sky. |
| `camera_from-the-south` | view 3 | Yes. |
| `camera_plan` | view 2 | Yes. |
| `camera_from-the-glade` | view 1 | Yes: the trunk, its rope ladder, the deck's underside with its hung lanterns, the Low Bridge leaving right. |
| `camera_lantern-night` | concept/lantern-night | Yes, as night: black sky, every rail and bridge lined with lanterns. |
| `pov_leg0_wp1` | Root Glade | Partly: under the platform among lamp posts; a post fills the near left. |
| `pov_leg3_wp13` | Hearth House | Partly: the railed deck and chimney at sunset; a corner post fills the left, and the cabins are out of frame. |
| `pov_leg2_wp16` | Long Bridge | Yes. |
| `pov_leg2_wp21` | Loom House | Yes. |
| `pov_leg6_wp4` | High Bridge | Yes. |
| `pov_leg6_wp9` | Watch House | Yes: the deck under the canopy, lanterns on chains. |
| `pov_leg6_wp14` | Watch Crown (the lookout) | Partly: the ring and its rail; the camp is below the frame. |
| `pov_leg6_wp15` | Watch Crown (the hook) | No: sky and the valley rim. A review frame faces along the walk's last step. |
| `pov_leg4_wp11` | Low Bridge | Yes. |
| `pov_leg4_wp1` | Seed House | Yes. |
