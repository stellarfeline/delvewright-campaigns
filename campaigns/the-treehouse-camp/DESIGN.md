# The Treehouse Camp — design record

**What this level is for: proving that several structures can be built in boxes at different `y` heights and connected.** Every tree is one box or a vertical stack of boxes. Eleven boxes stand at eight different floor heights, from y 66 to y 95, with the lantern ring at y 112, over terrain that runs from y 60 to y 76. Rope bridges join boxes side by side, and rope ladders join boxes stacked one over another. A player sees the whole thing from the ground, from each house and from the top of the tallest tree, and walks and climbs through every joint between boxes on the way. The four trees are split four different ways (§3.1), so each way of building in height is shown once.

A small showcase delve: a clan's camp of treehouses on four giant trees in a deep forest, joined by rope ladders and rope bridges. 1–4 players, 15–30 minutes, no combat. Every later round is judged against this file. The geometric facts in §4 are the authority on size and position, re-derived from reference view 4 (`design/reference/view4-aerial.jpg`), which governs geometry wherever the views disagree. The images are otherwise the authority on look and mood only. Where an image and §4 disagree, §4 wins.

## 1. The fiction

The Greatwood is an old forest of giant trees, each wide enough at the base for a house to stand between its roots. The Greatwood clan lives in it, off the ground. Their camp is four giant trees standing at the corners of a rough square, each with a house built around its trunk high above the ground, and rope bridges between them. A rope ladder hangs from the Hearth House down to the forest floor; that is the way in.

Tonight is Lantern Night. Once a year, when the nuts are pressed and the cloth for the new year is woven, the clan hangs a new lantern at the top of the Watch Tree, the tallest tree in the camp. When it is lit, every house hangs out its own lanterns in answer. Oru, the clan's headwoman, has climbed to the top and lit it for thirty years. This year her knee will not take the ladder, and she has asked the party, guests of the clan, to carry the lantern up for her.

The clan are ordinary people: weavers, nut-pressers, a headwoman, a boy who would rather not climb. They are friendly to the guests and busy with the festival. Nothing in the camp is hostile.

### Original work, and what "in the spirit of" means here

The brief asks for a camp in the spirit of the great tree villages of a well-known film. That spirit is taken as one idea only: **people living high in giant trees, moving between them on rope**. Nothing else is taken. Every name here is original or a plain English noun. There are no franchise names and no likeness of any franchise's people, creatures, plants, places or designs. The clan are ordinary humans in woven, earth-coloured clothes. The forest is lit by the sun and by lanterns and fires, never by glowing plants. There are no floating mountains, no single world-tree, no flying mounts and no nature deity. The houses are built around four separate ordinary (if giant) trees, not inside one tree. (Engine constitution, Forbidden zones and Conventions; `docs/reference/game-writing.md`.)

## 2. The mission

The party arrives on the forest floor in late afternoon and leaves at nightfall, after lighting the lantern.

| # | Beat | Where | What the player does | What the level shows |
|---|---|---|---|---|
| 1 | Arrival | Root Glade | Tobi, a boy of the clan, meets them among the roots and says Oru is waiting up in the Hearth House. He admits he is afraid of the ladder. | The rope ladder hangs on the Hearth Tree's bark up to the platform overhead. The first climb. |
| 2 | The ask | Hearth House | Oru explains Lantern Night and asks them to carry the lantern up for her. She needs the new lantern from Neve at the Loom House and lamp oil from Hessel at the Seed House, in either order. She says plainly that she is sad not to make the climb herself. | Two rope bridges leave the Hearth House, the highest house: one runs down toward the Loom Tree, one down toward the Seed Tree. |
| 3a | The lantern | Loom House, over the Long Bridge | Neve gives them the Night Lantern: an unlit lantern in a woven shade. She is in a quarrel with Hessel over whether the Low Bridge needs new rope or new planks. | Looms under a lean-to on the flat top of a topped tree, open to the sky; hanging cloth, rope coils. A rope gate across the mouth of the High Bridge, tied shut. |
| 3b | The oil | Seed House, over the Low Bridge | Hessel gives them a flask of lamp oil. He tells his side of the quarrel. An optional branch: how the camp was built, one tree at a time. | Baskets, drying racks, a nut press. |
| 4 | The flame | Hearth House | Oru fills the lantern and lights it at the hearth. She tells them Neve will untie the High Bridge gate when she sees the lit lantern. | The fire on the stone hearth. |
| 5 | The gate | Loom House | Neve sees the lit lantern and unties the rope gate (`barred` seam opened by `open-gate`). | The High Bridge runs to the Watch Tree. |
| 6 | The climb | Watch House, then the Watch Crown | They cross the High Bridge, climb the rope ladder through the Watch House roof into the crown, and keep climbing the trunk inside the crown to the ring at its top. | The ladder disappears up into the leaves. |
| 7 | Lantern Night | Crown Lookout, at the top of the Watch Crown | They hang the lantern on the hook at the top (a `use` trigger at the hook). Night falls (`set-time`). One house at a time, starting nearest and ending at the Root Glade, lanterns appear along every platform rail and bridge (`fill-region` beats). | From the lookout, above the other three trees, the camp lights up below. |

The quarrel between Neve and Hessel is never settled; each tells the party their side, and the ending does not resolve it.

Beat 7 is the delve's one big moment and is bigger than anything before it: every house and bridge in the camp changes at once while the party watches from the top of the tallest tree.

### Cast

| Name | Who | Where |
|---|---|---|
| Tobi | A boy of the clan. Meets the guests; afraid of the ladder and says so. | Root Glade |
| Oru | The clan's headwoman, keeper of the Hearth House. Has lit the lantern for thirty years. | Hearth House |
| Neve | The weaver. Makes the new lantern's shade each year. | Loom House |
| Hessel | The nut-presser and seed-keeper. Old, slow, talkative. | Seed House |

### Items

| Item | Given by | Used |
|---|---|---|
| Night Lantern (unlit) | Neve | taken by Oru at beat 4 |
| Flask of lamp oil | Hessel | taken by Oru at beat 4 |
| Night Lantern (lit) | Oru | hung on the hook at beat 7 |

### Telling

Per `docs/reference/game-writing.md`: every place is recognised by what is built there, with no signs and no glowing markers. The objective journal restates only what an NPC has already said. Lantern Night, the Loom House, the Seed House and the High Bridge are each named first by Oru in a sentence that says what they are. The rope gate is shut with a knot the player can see from the Loom House platform.

## 3. The places

Eleven places, one box each, in one site plan on one `open` site: nine the party enters and two that are scenery only, never entered. The forest floor between the trees belongs to no place. It is heightmap terrain, and spec-0098 makes it the commons.

### 3.1 How each tree is split into boxes

Each tree is split a different way, so the level shows every way a structure in height can be built. The Watch Tree is the full three-box stack the level exists to try.

| Tree | Boxes, bottom to top | Why this split |
|---|---|---|
| **Watch Tree** (tallest) | **Watch Roots** (scenery: trunk base and buttress roots on the ground) → **Watch House** (entered: platform and sentry hut) → **Watch Crown** (entered: the crown, with the Crown Lookout ring at its top) | The challenge case: three stacked boxes, one per part of the tree. The crown is entered, because the climb to the lantern hook runs up inside it. |
| **Hearth Tree** (widest) | **Root Glade** (entered: the ground among its roots) → **Hearth House** (entered) → **Hearth Crown** (scenery) | Also three boxes, but with the base entered and the crown scenery. The Hearth Tree's crown is the widest in the camp (32 across) and spreads well past its house. Its own box lets the crown be wider than the house below it, which a house's `roof` eaves cannot reach. |
| **Seed Tree** | **Seed House**, one box, its crown drawn in the box's declared `roof` zone | One box with a declared roof: a modest crown no wider than the house plus its eaves, so a separate box buys nothing. |
| **Loom Tree** | **Loom House**, one open (sky-open) box; the trunk below the platform is the box's own ground claim | One box with no crown. The Loom Tree is a topped tree: its top was cut off long ago and the house stands on the flat top, open to the sky, where the light is good for weaving. This is how view 4 draws it. |

### 3.2 The place list

| Place | Kind | Tree | What is there |
|---|---|---|---|
| Root Glade | entered; ground place, entry; covered by the Hearth House platform overhead | Hearth | The Hearth Tree's buttress roots on its high shelf of ground, a fern floor, a cold fire ring, the foot of the first rope ladder. Opens between the roots onto the forest floor. |
| Hearth House | entered; treehouse | Hearth | The highest house and the widest platform. The clan's hall: a stone hearth with a fire, benches, two thatched cabins against the trunk. |
| Hearth Crown | scenery | Hearth | Thick square branches and chunky leaf masses, 32 across, over the Hearth House and past it. |
| Loom House | entered; treehouse, sky-open | Loom | The lowest house. Two looms under a lean-to on the flat top of the topped trunk, cloth drying on lines, rope coils, the rope gate at the High Bridge. |
| Seed House | entered; treehouse | Seed | Baskets of nuts, drying racks, a log press, a storehouse hut; its crown overhead. |
| Watch Roots | scenery | Watch | The Watch Tree's trunk base and buttress roots on the ground. |
| Watch House | entered; treehouse | Watch | A sentry hut and its platform; the foot of the ladder into the crown. |
| Watch Crown | entered; the crown | Watch | The crown, 20 across. The ladder arrives on a small plank landing at the first fork, and a second ladder climbs the trunk inside the leaves to the Crown Lookout, a ring of planks just under the last branches, with the lantern hook. |
| Long Bridge | entered; rope bridge, way-classed | Loom ↔ Hearth | Plank deck, post-and-rope rails, climbs 6 by plank steps toward the Hearth House. |
| Low Bridge | entered; rope bridge, way-classed | Hearth ↔ Seed | The oldest bridge, worn planks (the quarrel's subject), drops 4 from the Hearth House. |
| High Bridge | entered; rope bridge, way-classed | Loom ↔ Watch | Climbs 4 toward the Watch House. Its Loom end is the rope gate. |

How each engine surface the demo row names is exercised:

- **A place owns its outside**: each piece draws its own platform, rails, hut walls and roofline, and the part of its tree inside its claim. The Seed Tree's crown is its house's declared `roof` zone (`roof: {courses, eaves}`).
- **Boxes stacked at different heights**: the Watch Tree's three boxes and the Hearth Tree's three boxes, each joined at a floor course, one box over the next.
- **Scenery places, never entered**: the Watch Roots and the Hearth Crown (the declaration PR #1010 adds).
- **The giant trees are built out of blocks**: trunks are stepped round masses of logs and wood blocks with bark texture, flared at the base into buttress roots. No vanilla tree, and no vanilla block, is anywhere near this size. A trunk that runs through several boxes is drawn by each box's piece for its own height and meets the next at the box's floor course.
- **Places at different floor heights on undulating heightmap terrain**: four ground heights and eight box floor heights (§4).
- **A connector that is itself a structure is a way-classed place**: the three rope bridges. Each treehouse provides only a landing where a bridge meets it.
- **Seams declare their form**: every seam carries its `form` (§4.4), and both places it joins read it in their handouts.
- **Open ground with no shell**: the forest floor, the Root Glade's open sides, and the sky-open Loom House.
- **A body climbs (spec-0099)**: two rope-ladder seams (up 14 and up 9), plus a 19-rung ladder inside the Watch Crown.

### Light

Light is placed while each place is designed. Every platform carries hanging lanterns on chains and a fire on a stone hearth or in a fire basket. Every bridge carries a lantern on a post at each end and one at mid-span. The Root Glade has a lit fire ring. The Watch Crown's landing and ring each carry lanterns. The canopy shades the forest floor. The finale's lanterns are added light on top of a camp that is already lit; the camp is never dark before beat 7.

### Safety

Every platform edge and every bridge deck has a rail at least fence height (1.5 blocks) that a body cannot jump. The only ways between levels are the ladders and the bridges. Below the Watch Crown no fall is deeper than 22 blocks, the unarmoured survivable fall (§4.5). The Watch Crown's landing and ring are railed all round except at their ladder holes, whose ladders catch a body within a block (spec-0099 §3.5). The Root Glade opens onto the forest floor, so a body that somehow reaches the ground walks back to the first ladder. The gully walls of the forest floor have walkable ramps at their ends, so no low ground is a pocket. There is no killing volume anywhere.

## 4. The design brief: geometric facts

These numbers are transcribed into `geometry-brief.json`, and `site-plan.json` is built to them. They are re-derived from reference view 4, which governs geometry. Seen from high in the north-east, view 4 puts the Loom Tree nearest, the Hearth Tree to the right and the Watch Tree to the left at the same depth, and the Seed Tree straight behind. In plan that is a square: Loom north-east, Hearth north-west, Seed south-west, Watch south-east. Bridges run along the north side (Loom–Hearth), the west side (Hearth–Seed) and the east side (Loom–Watch), with no bridge on the south side. View 4 also shows the Watch Tree's lookout above every other crown, the Hearth Tree as the widest with the highest house, the Loom house on top of a trunk with no crown over it, and the forest floor cut by gullies.

All horizontal positions are region-local block coordinates: x runs east, z runs south, both measured from the region's north-west corner (the region stands at world x 0, z 0, so they are also world coordinates). Heights are absolute world `y`.

### 4.1 The site

| Fact | Value |
|---|---|
| Region footprint | 112 × 112 blocks |
| Region height | y 56 to y 143 |
| Fill | `open`, heightmap terrain (`terrain/site.png`, 112 × 112 pixels, written by `terrain/heightmap.py`), moss over dirt |
| Terrain range | surface block from y 59 (the gully floor at the Loom Tree's foot, lowest) to y 71 (the high shelf round the Hearth Tree) |
| Terrain shape | four flat plots, one under each tree: the high shelf under the Hearth Tree (surface 71), the mound under the Seed Tree (69), the middle ground under the Watch Tree (65) and the gully floor under the Loom Tree (59); the region's rim at 63, where it meets the valley's gap floor. Between them the forest floor falls and rises smoothly, with no step over one block and no pit, so a body anywhere on it walks back to the Root Glade. |
| Terrain under the decks | never more than 20 blocks below the deck or platform above it |
| Terrain surface and below | moss-and-podzol forest floor over dirt; no water anywhere (the nav model refuses water) |
| Giant trees | 4, at the corners of a square, 42–44 apart along its sides |
| Boxes per tree | Watch 3, Hearth 3, Seed 1, Loom 1 |
| Places | 11 boxes: 9 entered, 2 scenery-only (Watch Roots, Hearth Crown) |
| Rope bridges | 3 |
| Rope-ladder seams | 2, plus one ladder inside the Watch Crown |
| Longest view | region diagonal 158 blocks, inside the 160-block floor of the served view distance |

### 4.2 The trees

| Tree | Trunk centre (x, z) | Ground at trunk (y) | Trunk width at the house | Buttress-root spread | Crown top (y) | Crown width |
|---|---|---|---|---|---|---|
| Hearth Tree | (35.5, 35.5) | 72 | 9 | 17 | 108 | 32 |
| Loom Tree | (79.5, 35.5) | 60 | 9, cut flat at y 79 | 15 | none (topped) | none |
| Seed Tree | (35.5, 77.5) | 70 | 7 | 13 | 104 | 24 |
| Watch Tree | (79.5, 77.5) | 66 | 9 | 15 | 122 | 20 |

Distances between trunk centres: Hearth–Loom 44, Seed–Watch 44, Hearth–Seed 42, Loom–Watch 42, diagonals 61.

The Watch Tree is the tallest. The Crown Lookout's ring stands at y 112, 4 above the next-highest crown (the Hearth Tree's, y 108). From the ring, a standing eye (y 113.6) looks down on every other tree. The crowns do not close over the camp. There is open sky over every bridge.

### 4.3 The boxes

| Box | Place | Footprint (x range × z range, interior) | Size, and what it stands on | Floor (y) | Floor above its tree's ground | Headroom | Roof |
|---|---|---|---|---|---|---|---|
| 1 | Watch Roots (scenery) | x 72–87 × z 70–85 | 16 × 16, on the ground | 66 | 0 | 17 (y 66–82); the Watch House floor course (y 83) is its top | — |
| 2 | Watch House | x 70–89 × z 68–87 | 20 × 20, aloft | 84 | 18 | 8 (y 84–91); the Watch Crown floor course (y 92) is its lid | — |
| 3 | Watch Crown | x 70–89 × z 68–87 | 20 × 20, aloft | 93 (the landing at the first fork) | 27 | 29 (y 93–121); lid y 122 is the crown top. The Crown Lookout ring is a second level inside it at y 112 | — |
| 4 | Root Glade | x 26–45 × z 26–45 | 20 × 20, on the ground | 72 | 0 | 13, open (y 72–84); the Hearth House floor course (y 85) is its cover | — |
| 5 | Hearth House | x 24–47 × z 24–47 | 24 × 24, aloft | 86 | 14 | 8 (y 86–93); the Hearth Crown floor course (y 94) is its lid | — |
| 6 | Hearth Crown (scenery) | x 20–51 × z 20–51 | 32 × 32, aloft | 95 | 23 | 13 (y 95–107); lid y 108 is the crown top | — |
| 7 | Seed House | x 28–43 × z 70–85 | 16 × 16, on the ground | 82 | 12 | 6 (y 82–87) | `roof` zone, 16 courses to y 104, eaves 4 |
| 8 | Loom House | x 72–87 × z 28–43 | 16 × 16, on the ground, sky-open | 80 | 20 | 6, open (y 80–85) | none (sky-open) |
| 9 | Long Bridge | x 49–70 × z 34–36 | 22 long × 3 wide, aloft | 80 | — | 9 (y 80–88): the steps climb 6 inside it | sky-open |
| 10 | Low Bridge | x 34–36 × z 49–68 | 20 long × 3 wide, aloft | 82 | — | 7 (y 82–88): the steps climb 4 inside it | sky-open |
| 11 | High Bridge | x 78–80 × z 45–66 | 22 long × 3 wide, aloft | 80 | — | 7 (y 80–86): the steps climb 4 inside it | sky-open |

Box floors take eight distinct values over the eleven boxes: 66, 72, 80 (Loom House, Long Bridge, High Bridge), 82 (Seed House, Low Bridge), 84, 86, 93 and 95. The Crown Lookout ring at y 112 is a second level inside box 3.

Each bridge's deck runs from platform edge to platform edge across its run plus the two seam cells: Long Bridge 24, Low Bridge 22, High Bridge 24.

A place on the ground owns the ground under it; a place aloft hangs, owning nothing under its floor (each bridge one course of beams), and the forest floor under it is the commons. The Root Glade is 20 × 20 under the 24 × 24 Hearth House: its open headroom must reach y 84 for the ladder, and at 24 × 24 its ring would share cells with both bridges' undersides that no connection awards (`DW0827`).

### 4.4 The seams

Every bridge seam declares its own opening, 3 wide and 3 high; each ladder seam an opening 1 × 2 through the floor, both cells along the trunk's face.

| Seam | Joins | Kind | Rise | Declared `form` |
|---|---|---|---|---|
| glade-ladder | Root Glade → Hearth House | through the Hearth House floor | up 14 | "rope ladder, up 14, hung on the Hearth Tree's bark" |
| loom-long | Loom House → Long Bridge | west face, arch opening | 0 | "rope bridge landing, level, 3 wide" |
| long-hearth | Long Bridge → Hearth House | west face, arch opening, stair hosted on the bridge | up 6 | "rope bridge, climbs 6 by plank steps on its last 12 blocks, 3 wide" |
| hearth-low | Hearth House → Low Bridge | south face, arch opening, stair hosted on the bridge | down 4 | "rope bridge, drops 4 by plank steps on its first 8 blocks, 3 wide" |
| low-seed | Low Bridge → Seed House | south face, arch opening | 0 | "rope bridge landing, level, 3 wide" |
| loom-high | Loom House → High Bridge | south face, arch opening, `barred` until Neve unties it | 0 | "rope gate across a rope bridge's mouth, tied shut, 3 wide" |
| high-watch | High Bridge → Watch House | south face, arch opening, stair hosted on the bridge | up 4 | "rope bridge, climbs 4 by plank steps on its last 8 blocks, 3 wide" |
| watch-ladder | Watch House → Watch Crown | through the Watch Crown floor | up 9 | "rope ladder, up 9, hung on the Watch Tree's bark through the Watch House roof to the first fork" |

The box joints with no seam are the scenery stacks: Watch Roots under Watch House (y 83), and Hearth Crown over Hearth House (y 94). They meet at a floor course and nothing crosses them. Inside the Watch Crown, a 19-rung ladder on the trunk joins the landing (y 93) to the Crown Lookout ring (y 112). That ladder is the crown piece's own and is not a seam: its contract joins the landing and the ring by a `climb` edge.

The Root Glade also opens onto the forest floor (the commons) between the buttress roots on its open sides. That opening is the place's own and is not a seam.

Every ladder hangs on a full block: the trunk's bark, or a post where a ladder leaves the trunk. A vanilla ladder needs a sturdy face behind it (spec-0099 §2.3), so the camp has no free-hanging rope ladder.

### 4.5 Heights at a glance

| Thing | y | Above the ground beneath it |
|---|---|---|
| Watch Roots | 66–82 | on the ground |
| Root Glade | 72 | on the high shelf |
| Loom House floor | 80 | 20 over the gully floor (60) |
| Long Bridge deck | 80–86 | 20 at the Loom end, 14 at the Hearth end |
| High Bridge deck | 80–84 | 20 at the Loom end, 18 at the Watch end |
| Seed House floor | 82 | 12 over the mound (70) |
| Low Bridge deck | 82–86 | 14 at the Hearth end, 12 at the Seed end |
| Watch House floor | 84 | 18 over its ground (66) |
| Hearth House floor | 86 | 14 over the shelf (72) |
| Watch Crown landing | 93 | over the Watch House roof |
| Hearth Crown (scenery) | 95–108 | over the Hearth House |
| Crown Lookout ring | 112 | inside the Watch Crown, over its landing; reached only by ladder |

The deepest drop off any deck or platform below the Watch Crown, rail aside, is 20 blocks (the Loom House and the Loom ends of both its bridges), under the 22-block survivable fall.

## 5. Style, horizon, time and weather

**The style is confirmed** on the reference sheet in `design/reference/` (style contract `design/reference/style.txt`). Build to it: look and mood from the images, sizes and positions from §4. Where the views disagree about geometry, view 4 governs.

The horizon is `valley` for now. A forest horizon is a recorded engine idea (the forest-horizon issue), and the camp takes it when the engine has it.

Played in late afternoon, clear, with sun coming in low through the canopy. Beat 7 sets the time to nightfall. The reference views are drawn at late afternoon.

## 6. Open capability findings this design depends on

See `GENERATION.md` § Capability findings. The design is not worked around any of them. A part that depends on one waits for the engine.
