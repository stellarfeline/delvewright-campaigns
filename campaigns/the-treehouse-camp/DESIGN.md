# The Treehouse Camp — design record

A small showcase delve: a clan's camp of treehouses on four giant trees in a deep forest, joined by rope ladders and rope bridges. 1–4 players, 15–30 minutes, no combat. Every later round is judged against this file. The geometric facts in §4 are the authority on size and position; the images in `design/reference/` are the authority on look and mood only. Where an image and §4 disagree, §4 wins.

## 1. The fiction

The Greatwood is an old forest of giant trees, each wide enough at the base for a house to stand between its roots. The Greatwood clan lives in it, off the ground. Their camp is four giant trees, each with a house built around its trunk where the trunk is widest, and rope bridges between them. A rope ladder hangs from the lowest house down to the forest floor; that is the way in.

Tonight is Lantern Night. Once a year, when the nuts are pressed and the cloth for the new year is woven, the clan hangs a new lantern at the top of the Watch Tree, the tallest tree in the camp. When it is lit, every house hangs out its own lanterns in answer. Oru, the clan's headwoman, has climbed to the top and lit it for thirty years. This year her knee will not take the ladder, and she has asked the party, guests of the clan, to carry the lantern up for her.

The clan are ordinary people: weavers, nut-pressers, a headwoman, a boy who would rather not climb. They are friendly to the guests and busy with the festival. Nothing in the camp is hostile.

### Original work, and what "in the spirit of" means here

The brief asks for a camp in the spirit of the great tree villages of a well-known film. That spirit is taken as one idea only: **people living high in giant trees, moving between them on rope**. Nothing else is taken. Every name here is original or a plain English noun. There are no franchise names and no likeness of any franchise's people, creatures, plants, places or designs. The clan are ordinary humans in woven, earth-coloured clothes. The forest is lit by the sun and by lanterns and fires, never by glowing plants. There are no floating mountains, no single world-tree, no flying mounts and no nature deity. The houses are built around four separate ordinary (if giant) trees, not inside one tree. (Engine constitution, Forbidden zones and Conventions; `docs/reference/game-writing.md`.)

## 2. The mission

The party arrives on the forest floor in late afternoon and leaves at nightfall, after lighting the lantern.

| # | Beat | Where | What the player does | What the level shows |
|---|---|---|---|---|
| 1 | Arrival | Root Glade | Tobi, a boy of the clan, meets them among the roots and says Oru is waiting up in the Hearth House. He admits he is afraid of the ladder. | The rope ladder hangs on the Hearth Tree's bark up to the platform overhead. The first climb. |
| 2 | The ask | Hearth House | Oru explains Lantern Night and asks them to carry the lantern up for her. She needs the new lantern from Neve at the Loom House and lamp oil from Hessel at the Seed House, in either order. She says plainly that she is sad not to make the climb herself. | Two rope bridges leave the Hearth House platform: one climbs toward the Loom Tree, one drops toward the Seed Tree. |
| 3a | The lantern | Loom House, over the Long Bridge | Neve gives them the Night Lantern: an unlit lantern in a woven shade. She is in a quarrel with Hessel over whether the Low Bridge needs new rope or new planks. | Looms, hanging cloth, rope coils. A rope gate across the mouth of the High Bridge, tied shut. |
| 3b | The oil | Seed House, over the Low Bridge | Hessel gives them a flask of lamp oil. He tells his side of the quarrel. An optional branch: how the camp was built, one tree at a time. | Baskets, drying racks, a nut press. |
| 4 | The flame | Hearth House | Oru fills the lantern and lights it at the hearth. She tells them Neve will untie the High Bridge gate when she sees the lit lantern. | The fire on the stone hearth. |
| 5 | The gate | Loom House | Neve sees the lit lantern and unties the rope gate (`barred` seam opened by `open-gate`). | The High Bridge, the longest bridge, runs to the Watch Tree. |
| 6 | The climb | Watch House, then the long ladder | They cross the High Bridge and climb the long rope ladder up the Watch Tree's trunk, through its crown. | The highest platform in the camp; the ladder disappears up into the leaves. |
| 7 | Lantern Night | Crown Lookout | They hang the lantern on the hook at the top (a `use` trigger at the hook). Night falls (`set-time`). One house at a time, starting nearest and ending at the Root Glade, lanterns appear along every platform rail and bridge (`fill-region` beats). | From the lookout, above the other three crowns, the camp lights up below. |

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

Nine places, all in one site plan on one `open` site. The forest floor between the trees belongs to no place. It is heightmap terrain, and spec-0098 makes it the commons.

| Place | Kind | Tree | What is there |
|---|---|---|---|
| Root Glade | ground place, entry; covered by the Hearth House platform overhead | Hearth | The Hearth Tree's buttress roots, a fern floor, a cold fire ring, the foot of the first rope ladder. Opens between the roots onto the forest floor. |
| Hearth House | treehouse | Hearth | The widest platform. The clan's hall: a stone hearth with a fire, benches, a big thatched hut against the trunk. |
| Loom House | treehouse | Loom | Two looms under a lean-to roof, cloth drying on lines, rope coils, the rope gate at the High Bridge. |
| Seed House | treehouse | Seed | Baskets of nuts, drying racks, a log press, a storehouse hut. |
| Watch House | treehouse | Watch | A sentry hut and a small platform, the foot of the long ladder. |
| Crown Lookout | treehouse, stacked over the Watch House | Watch | A ring of planks at the top of the Watch Tree, just under its last branches, and the lantern hook. |
| Long Bridge | rope bridge, a way-classed place | Hearth → Loom | Plank deck, post-and-rope rails, climbs 4 by plank steps. |
| Low Bridge | rope bridge, a way-classed place | Hearth → Seed | The oldest bridge, worn planks (the quarrel's subject), drops 4. |
| High Bridge | rope bridge, a way-classed place | Loom → Watch | The longest bridge, climbs 4. Its Loom end is the rope gate. |

How each engine surface the demo row names is exercised:

- **A place owns its outside**: each treehouse's piece draws its platform, rails, hut walls, roofline and the part of its tree inside its claim. The crown above a treehouse is that place's declared `roof` zone (`roof: {courses, eaves}`), drawn by its piece as branches and leaves.
- **The giant trees are built out of blocks**: trunks are stepped round masses of logs and wood blocks with bark texture, flared at the base into buttress roots. No vanilla tree, and no vanilla block, is anywhere near this size.
- **Places at different floor heights on undulating heightmap terrain**: four ground heights and five floor heights (§4).
- **A connector that is itself a structure is a way-classed place**: the three rope bridges. Each treehouse provides only a landing where a bridge meets it.
- **Seams declare their form**: every seam carries its `form` (§4.4), and both places it joins read it in their handouts.
- **Open ground with no shell**: the forest floor, and the Root Glade's open sides.
- **A body climbs (spec-0099)**: two rope-ladder seams, 16 and 24 rungs.

### Light

Light is placed while each place is designed. Every platform carries hanging lanterns on chains and a fire on a stone hearth or in a fire basket. Every bridge carries a lantern on a post at each end and one at mid-span. The Root Glade has a lit fire ring. The canopy shades the forest floor. The finale's lanterns are added light on top of a camp that is already lit; the camp is never dark before beat 7.

### Safety

Every platform edge and every bridge deck has a rail at least fence height (1.5 blocks) that a body cannot jump. The only ways between levels are the ladders and the bridges. Below the Crown Lookout no fall is deeper than 22 blocks (§4.5), the unarmoured survivable fall. The Crown Lookout stands 24 above the Watch House platform, so its rail runs unbroken all round except at the ladder hole, whose ladder catches a body within a block (spec-0099 §3.5). The Root Glade opens onto the forest floor, so a body that somehow reaches the ground walks back to the first ladder. There is no killing volume anywhere.

## 4. The design brief: geometric facts

These numbers transcribe into `geometry-brief.json` at step 2, and `site-plan.json` is built to them. All horizontal positions are region-local block coordinates: x runs east, z runs south, both measured from the region's north-west corner. Heights are absolute world `y`. Horizontal positions sit on the metrics table's 4-block grid.

### 4.1 The site

| Fact | Value |
|---|---|
| Region footprint | 112 × 112 blocks |
| Region height | y 56 to y 143 |
| Fill | `open`, heightmap terrain, 112 × 112 pixels |
| Terrain range | ground top from y 62 (the dell at the Seed Tree, lowest) to y 74 (the rise at the Loom Tree, highest) |
| Terrain slope | at most 1 block of rise per 2 blocks of run anywhere a body can walk |
| Terrain surface and below | moss-and-podzol forest floor over dirt; no water anywhere (the nav model refuses water) |
| Giant trees | 4 |
| Treehouse places | 5 (one per tree, plus the Crown Lookout stacked on the Watch Tree) |
| Rope bridges | 3 |
| Rope ladders (seams) | 2 |
| Longest view | region diagonal 158 blocks, inside the 160-block floor of the served view distance |

### 4.2 The trees

| Tree | Trunk centre (x, z) | Ground at trunk (y) | Trunk width at the house | Buttress-root spread at the ground | Crown top (y) | Crown width |
|---|---|---|---|---|---|---|
| Hearth Tree | (44, 56) | 66 | 9 | 17 | 110 | 34 |
| Loom Tree | (84, 40) | 74 | 7 | 13 | 106 | 24 |
| Seed Tree | (28, 92) | 62 | 7 | 13 | 104 | 24 |
| Watch Tree | (84, 80) | 70 | 9 | 15 | 122 | 22 below the lookout, 14 above it |

The Watch Tree is the tallest. Its crown top stands 12 blocks over the next-highest crown (the Hearth Tree's), and the Crown Lookout's floor stands 4 over it. From the lookout a standing eye (y 115.6) looks down on all three other crowns.

Distances between trunk centres: Hearth–Loom 43, Hearth–Seed 39, Loom–Watch 40, Hearth–Watch 48, Seed–Watch 56. The crowns do not close over the camp. There is open sky over every bridge, between crowns that are 14 or more blocks apart.

### 4.3 The places

| Place | Footprint (x range × z range, interior) | Size | Floor (y) | Floor above its tree's ground | Headroom |
|---|---|---|---|---|---|
| Root Glade | x 32–55 × z 44–67 | 24 × 24, hall | 66 | 0 | 15 (y 66–80); the Hearth House floor course at y 81 is its cover |
| Hearth House | x 32–55 × z 44–67 | 24 × 24, hall | 82 | 16 | 8; `roof` zone holds the crown up to y 110, eaves 4 |
| Loom House | x 76–91 × z 32–47 | 16 × 16, room | 86 | 12 | 6; `roof` zone holds the crown up to y 106, eaves 4 |
| Seed House | x 20–35 × z 84–99 | 16 × 16, room | 78 | 16 | 6; `roof` zone holds the crown up to y 104, eaves 4 |
| Watch House | x 74–93 × z 70–89 | 20 × 20, hall | 90 | 20 | 23 (y 90–112), its hut and the Watch Tree's lower crown inside it; no `roof` (the lookout is stacked over it) |
| Crown Lookout | x 78–89 × z 74–85 | 12 × 12, room | 114 | 44 | 4; `roof` zone holds the crown top up to y 122, eaves 4 |
| Long Bridge | x 57–74 × z 44–46 | 18 long × 3 wide, corridor | 82 | — | 3 |
| Low Bridge | x 33–35 × z 69–82 | 14 long × 3 wide, corridor | 78 | — | 3 |
| High Bridge | x 82–84 × z 49–68 | 20 long × 3 wide, corridor | 86 | — | 3 |

Each bridge's deck runs from platform edge to platform edge across its run plus the two seam cells: Long Bridge 20, Low Bridge 16, High Bridge 22.

### 4.4 The seams

| Seam | Joins | Kind | Rise | Declared `form` |
|---|---|---|---|---|
| glade-ladder | Root Glade → Hearth House | through the Hearth House floor | up 16 | "rope ladder, up 16, hung on the Hearth Tree's bark" |
| hearth-long | Hearth House → Long Bridge | east face, arch opening | 0 | "rope bridge landing, level, 3 wide" |
| long-loom | Long Bridge → Loom House | east face, arch opening, stair hosted on the bridge | up 4 | "rope bridge, climbs 4 by plank steps on its last 8 blocks, 3 wide" |
| hearth-low | Hearth House → Low Bridge | south face, arch opening, stair hosted on the bridge | down 4 | "rope bridge, drops 4 by plank steps on its first 8 blocks, 3 wide" |
| low-seed | Low Bridge → Seed House | south face, arch opening | 0 | "rope bridge landing, level, 3 wide" |
| loom-high | Loom House → High Bridge | south face, arch opening, `barred` until Neve unties it | 0 | "rope gate across a rope bridge's mouth, tied shut, 3 wide" |
| high-watch | High Bridge → Watch House | south face, arch opening, stair hosted on the bridge | up 4 | "rope bridge, climbs 4 by plank steps on its last 8 blocks, 3 wide" |
| watch-ladder | Watch House → Crown Lookout | through the Crown Lookout floor | up 24 | "rope ladder, up 24, hung on the Watch Tree's bark through its crown" |

The Root Glade also opens onto the forest floor (the commons) between the buttress roots on its open sides. That opening is the place's own and is not a seam.

Every ladder hangs on a full block: the trunk's bark, or a post where a ladder leaves the trunk. A vanilla ladder needs a sturdy face behind it (spec-0099 §2.3), so the camp has no free-hanging rope ladder.

### 4.5 Heights at a glance

| Thing | y | Above the ground beneath it |
|---|---|---|
| Seed House floor | 78 | 16 over the dell (62) |
| Low Bridge deck | 78–82 | about 16 over the dell's slope |
| Hearth House floor | 82 | 16 over the glade (66) |
| Long Bridge deck | 82–86 | 12–16 |
| Loom House floor | 86 | 12 over the rise (74) |
| High Bridge deck | 86–90 | 12 at the Loom end, 20 at the Watch end |
| Watch House floor | 90 | 20 over its ground (70) |
| Crown Lookout floor | 114 | 44; reached only by the ladder through the Watch Tree's crown |

The deepest drop off any deck or platform below the lookout, rail aside, is 20 blocks (the High Bridge's Watch end and the Watch House), under the 22-block survivable fall. The Crown Lookout stands over the Watch House platform, not over open ground.

## 5. Time and weather

Played in late afternoon, clear, with sun coming in low through the canopy. Beat 7 sets the time to nightfall. The reference views are drawn at late afternoon.

## 6. Open capability findings this design depends on

See `GENERATION.md` § Capability findings. The design is not worked around any of them. A part that depends on one waits for the engine.
