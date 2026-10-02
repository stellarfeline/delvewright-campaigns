# The Stranding — design record

The authoritative design of this campaign. Every later round is judged against it. It is written before step 4 (no reference images yet) and before any document but this one exists; it fixes the scenes, the beats, the cast, the classes, the danger model and what the engine owes before each act can be built.

Source: the plot skeleton of H. P. Lovecraft's *Dagon* (1919, public domain) — a floor of black mud risen from the sea overnight, a carved monolith on it, and something vast that lives. Every proper noun below is original. No "Call of Cthulhu" trademark, no later author's or publisher's setting.

## The brief, as fixed

- Four acts at Vesperhold scale, target 150 minutes: a coastal town at night (the main body of the map), the crossing of the mudflat, the inside of the body, the head and the escape.
- The mudflat sinks stage by stage as the story advances, never on a clock.
- Inside the body the party can split: those outside see the tentacles and call positions to those inside.
- All five techniques of the eldritch visuals lab are core (tentacle of animated display entities, a "wrong" atmosphere zone, perception effects, the endless corridor, the living sculk room).
- Adventure mode, class kits, 1–4 players, vanilla Minecraft Java 1.21.11. No mining, levelling or base building.

## The hidden story (never shown whole)

Wrackham is a fishing town on Wrack Bay. Off the bay the sea floor drops into a trench, and in the trench lies the Fathomer — the old Wrackham name for the thing that sleeps there. It is the size of a hill. Long before the town, a people nobody remembers carved a stone tablet, the Brow Stone, and drove it into the Fathomer's forehead. The carvings on it are the only account of why.

The Brow Stone keeps the Fathomer asleep. While it sleeps, it dreams, and whoever lives on the shore dreams with it. For three hundred years the dream was faint: fishermen spoke of "the low dream" and went to sea anyway.

Four nights ago the trench floor rose. A plain of black mud two miles wide came up out of the bay, and the Fathomer came up with it, stranded on the mud, wounded where the rising rock tore it. Since that night everyone in Wrackham has dreamt the same dream every night — of walking out onto the mud to lie down beside it — and every night more of them do it in their sleep. Most are found standing on the flat at dawn. Three never came back; one of them is Davey Coyle, the harbourmistress's son.

What the town does not know: the body is dying, and the Brow Stone is what keeps it from dying. Pinned, it cannot die and cannot go back down; it can only lie on the mud and dream louder. The carvings show that lifting the stone sends the Fathomer down into the trench. The bottom row of the carvings is broken off, and the rubbing the town keeps stops above the break.

What the party can learn, and where (each fact is placed at least twice):

| fact | where it is told |
|---|---|
| the town dreams one dream and sleepwalks onto the mud | Wenna Coyle at the Harbour Office; the sleepers standing in the High Street; Davey's room |
| the Brow Stone keeps the Fathomer asleep, and its dream reaches the shore | the Rubbing in the Seamen's Chapel, read by Absalom Tregear; the carved pillars of the Pilgrims' Way on the flat |
| lifting the stone sends the Fathomer down | the Rubbing's third panel; the pillars; Captain Marrack's log |
| the bottom row is lost | Tregear, at the Rubbing; the chip of the stone in the Customs House; the ending, which shows it |
| earlier visitors went inside and did not all come out | Marrack at his launch; his log; what lies in the Stomach |

## Posture

Three axes pushed off the machine default for this campaign (writing craft §B):

- **Escalation is uneven.** Acts 1 and 2 build slowly and quietly; the cutting of the Brow Stone is out of all proportion to anything before it — every tentacle rises at once, the eye opens, the ground goes.
- **People name their fear.** Wenna says she is afraid of the dream and of the flat in so many words; Tregear says he does not know what the bottom row showed.
- **The ending does not explain itself.** Neither ending tells the party what the Fathomer does next. One ending shows the bottom row of the carvings and does not interpret it.

## Placement

A site plan (step 2B): the map is the point, and no prefab is the town or the body. One region, one contiguous walk, no teleport between areas. The body lies on the flat and is entered through its mouth; the endless corridor is a loop inside the body, not a second space. Piece axes: x east, y up, z south. The town is the north end; the body is the south end.

Approximate extents, to be fixed in the geometry brief: the town on cliff terraces about 160 × 120 blocks, falling from the coach road (y 96) to the harbour (y 66); the flat about 320 blocks long from the slipway to the body, mud at y 64 over sea water at y 62; the body about 140 long, 60 wide, 45 high, the forehead at about y 108. `horizon` is `ocean` only if the library's sea pieces carry `waterline_y` (the step-1 query decides); otherwise `void` with the sea built into the plan. `boundary` with a message either way.

Hour: `time: night`, `weather: clear`. Moonlight on the mud is the image of the campaign. The darkest reachable sky is therefore the night floor, and every walked cell is lit by placed light (see *Light*).

## Act 1 — Wrackham (about 60 minutes)

The party comes down the coach road at night into a town where nobody is awake except the harbourmistress. They learn what lies on the flat, what the Brow Stone is and why it matters, take the tool to cut it, find that every boat has been staved in, and open the only way across: the Pilgrims' Way, the old road over the bay that the sea took before the town was built, marked out again by lamps from the lighthouse.

While they work, the wrong place creeps up from the shore. It starts at the seawall; after each of three beats it is repainted one terrace higher, so a street walked down under a clear night sky is walked back up under an olive sky and close yellow fog.

| # | place | what the player does there |
|---|---|---|
| 1 | Coach Road | spawn and class selection at the coach stop; the first view down over the roofs to the bay, the black flat under the moon, and the Fathomer's outline far out; first checkpoint |
| 2 | High Street | the walk down through town: sleepers standing in open doorways, all facing the sea, murmuring (a bark pool); at the far end of the street a tall dark figure stands facing the party and is gone when they come near (the watcher) |
| 3 | Harbour Office | Wenna Coyle hires the party: the town dreams one dream, the sleepers walk onto the mud, her son Davey did not come back; the tide board stuck at "low" for four days; the key to the Customs House |
| 4 | Coyle House | off the harbour lane: Davey's room — the bed soaked with sea water, muddy footprints from the bed to the door, and on the wall the picture he made of the dream in coloured wool (a block relief) |
| 5 | Fish Market | the first fight: the Drowned come up the slipway out of the harbour mud; when it is over, the wrong place reaches the seawall steps (**first creep**) |
| 6 | Seawall | the threshold of the wrong place: crossing the seawall steps, the sky turns olive, the fog closes in, the clouds go red and the music stops |
| 7 | Seamen's Chapel | Absalom Tregear, the town archivist, keeps the Rubbing — a copy of the Brow Stone's carvings his grandfather took from a fragment — on the wall (a four-panel block relief); he reads it to the party: the stone keeps the Fathomer asleep and dreaming; lifting it sends it down; the bottom row is lost |
| 8 | Chapel Crypt | below the chapel: the drowned of earlier storms in their niches, and the founders' cupboard with the town's oldest chart; checkpoint |
| 9 | Customs House | the town's records: the night ledger of the rising; the chart of the Pilgrims' Way; on the counter, under glass, a chip of the Brow Stone a net brought up forty years ago — whoever touches it is the first to feel the dream (**perception, light form**); after it, the wrong place reaches the harbour (**second creep**) |
| 10 | Net Lofts | off the harbour, up a stair: nets, floats and a sleeper standing at the loft door who does not move; a chest of food and arrows |
| 11 | Boatyard | every boat on the hard has its bottom staved in from inside; the shipwright's note says the sleepers did it, all on the same night; a fight among the hulls (the Drowned again); this is where the party learns there is no boat |
| 12 | Whalers' Shed | the flensing tools of the last whaling crew; the Flensing Spade, the one tool long and sharp enough to cut a stone out of flesh, on its rack |
| 13 | Ropewalk | the long rope shed between the shed and the breakwater; a sleeper at each end; the way to the breakwater |
| 14 | Breakwater | the stone arm out into the bay with the flat on both sides of it |
| 15 | Lighthouse | the climb up the tower stair; the party lights the lamp; out on the flat a line of old marker stakes catches the light one by one and their lamps come on, showing the Pilgrims' Way to the body (**third creep**: the wrong place now covers the whole lower town) |
| 16 | Slipway Stair | back down through the harbour to the stone stair onto the flat; Wenna at its head; act end, checkpoint |

Sixteen places: thirteen on the road, three off it (Coyle House, Net Lofts, Chapel Crypt).

The road: Coach Road → High Street → Harbour Office → Fish Market (fight; first creep) → Seawall → Seamen's Chapel (Rubbing) → Customs House (chart; the chip; second creep) → Boatyard (no boats; fight) → Whalers' Shed (Flensing Spade) → Ropewalk → Breakwater → Lighthouse (the lamps; third creep) → back through the harbour → Slipway Stair.

## Act 2 — The Crossing (about 25 minutes)

The party walks the Pilgrims' Way out across the flat by the lamps. The whole flat is the wrong place. The Fathomer grows from an outline to a hill. Each completed beat sinks the flat one stage: a layer of mud is cleared, the sea water under it shows, and the dry ground left is narrower. The sinking happens behind and beside the party and never takes the ground under the marked way.

| # | place | what the player does there |
|---|---|---|
| 17 | Pilgrims' Way | the first stretch: marker stakes with lamps, the town's lights behind; the watcher stands out on the mud in the fog |
| 18 | Wreck Field | old hulls the rising brought up, lying on their sides; the Drowned climb out of them; after the fight the flat sinks (**stage 1**: the open mud on both sides of the way goes under water) |
| 19 | Marrack's Launch | a salvage launch grounded beside the way; Captain Ivo Marrack, who came three days ago to salvage the body and went inside with two men and came out alone; he says the mouth is open at the low end and that his men are still in there; he gives the party his log; his mast platform (reached by a stair, not a ladder) looks along the body's flank (**stage 2** on leaving: the way behind the launch narrows to the causeway ridge) |
| 20 | Carved Pillars | the standing pillars of the old road, carved with the same pictures as the Rubbing, less worn — the second telling of what the Brow Stone does |
| 21 | The Narrows | the ridge narrows to three blocks between open water; beside it, the first tentacle rises out of a wound in the Fathomer's side and sways in the fog — it does not strike; the flat sinks (**stage 3**) |
| 22 | Flank Ridge | a mud ridge running along the body's west side, out of the tentacles' reach, from which three wounds on the flank are in plain sight — the Spotter's Post for act 3 |
| 23 | Jaw Bank | the bank of mud under the head; the open mouth, teeth like posts; checkpoint; act end |

Seven places, all on the road except the Flank Ridge (beside it; it becomes the outside post in act 3).

## Act 3 — Inside the body (about 45 minutes)

The inside is its own atmosphere zone: dark red sky where any shows through a wound, close fog, no music. A heartbeat sounds through the whole interior on a fixed interval and is loudest in the Heart Chamber.

| # | place | what the player does there |
|---|---|---|
| 24 | The Mouth | through the teeth onto the tongue; the inside zone begins; Marrack's chalk arrow on a tooth |
| 25 | The Throat | a corridor of ribs, every six blocks the same; walking forward returns the party twelve blocks back without a jump they can feel (**endless corridor**); after the second loop the walls crack, after the fourth half the lights are gone; one rib is not like the others — it is broken and set wrong — and striking it releases the loop |
| 26 | Rib Cathedral | the chest: a vault of ribs forty blocks high; moonlight falls through two wounds in the roof; walks along the ribs and across the cartilage; lice (silverfish) swarm out of the flesh walls; the diaphragm, a wall of membrane, closes the way down until the party cuts it with the Flensing Spade |
| 27 | The Stomach | a black pool behind a curb of bone, and on its shore what earlier visitors left: Marrack's men's lamps, a boot, a coil of rope, the two sleepers who did not come back — their coats, not their bodies; a fight with the Drowned that were Marrack's men; checkpoint |
| 28 | Heart Chamber | the living room: sculk grown over bone like flesh, sensors that click at every step and set off a shrieker, a floor that pulses with the heartbeat and puffs sculk, the watcher standing still and facing the party and moving when they come close; Davey Coyle stands by the heart, awake, speaking in the dream's words; three valves in the heart wall |
| 29 | The Breach | a short tunnel from the Heart Chamber out through a wound to the Flank Ridge and back — the way a lone player goes to see what a spotter would see |

**The split (the Heart Chamber valves).** The heart has three valves. Opening the right one squeezes the heart once; three right valves in a row stop the beat and open the stair up the spine. Which valve is right is shown only outside: each round, one tentacle rises from one of the three wounds on the flank (west, middle, east), and the matching valve is the right one. From the Flank Ridge a spotter sees which wound; inside, nobody can. The spotter calls it; the inside players open the valve. A wrong valve fires the perception bundle on whoever opened it, sends a pulse of damage through the chamber (non-lethal, announced by the heartbeat quickening), and resets the rounds to the first. Three rounds, a different wound each round, in a fixed order.

One player can do it alone: the Breach leads from the chamber to the ridge and back in under a minute. Two to four players divide naturally: one on the ridge, the rest at the valves. Nothing has to happen at the same moment; only what the spotter sees has to reach the valves.

When the third valve is opened the beat stops, Davey wakes and does not know where he is, and the spine stair opens. Davey goes out through the Breach and home along the causeway; the party goes up.

## Act 4 — The Brow and the escape (about 20 minutes)

| # | place | what the player does there |
|---|---|---|
| 30 | Spine Stair | up the inside of the neck on the vertebrae, built as steps; out through the blowhole onto the back |
| 31 | The Crown | the top of the head, forty blocks over the flat: the town's lights to the north, the tentacles standing out of the wounds all round; checkpoint |
| 32 | The Brow | the Brow Stone in the forehead; holding the Flensing Spade, a player cuts it out (**the full perception bundle** for everyone on the Brow: darkness, nausea, the face, blindness, a second face, the warden's sound behind them). Then the disproportionate beat: every tentacle rises at once, the largest out of the blowhole and over the Brow, the eye below the Brow opens, the flat starts to go. The stone is carried by one player. |
| 33 | The Run | down the back along the spine ridge, down the tail flank onto the causeway; the tentacles strike beside the way, each strike announced by the tip curling over the spot first; behind the party, the ground they have passed collapses into the sea, one section per marker passed |
| 34 | The Causeway | the Pilgrims' Way home with the water coming back on both sides; as the party comes off the flat, the wrong place lifts from the town terrace by terrace, from the top down |
| 35 | The Pier | Wenna on the pier, and Davey beside her (he left the body through the Breach and walked home along the causeway while the party climbed the spine); the choice of what to do with the Brow Stone |

## Branches and endings

| point | opens at | branches | leads to |
|---|---|---|---|
| The Brow Stone | the Pier | **Keep it**: the stone is given to Tregear, who locks it in the Chapel Crypt so it can never be put back. Sea fog comes in with the tide and covers the bay; at dawn the town is clear and the bay is fog, and the town does not dream that night. Tregear does not sleep: the stone dreams in the crypt under his chapel, and he hears it. | `ending/the-keeping` |
| | | **Give it back**: the stone is thrown off the end of the pier. As it goes down, the party sees the bottom row of the carvings for the first time: Wrackham, under water. Sea fog comes in with the tide and covers the bay; at dawn the fog has not lifted and nobody in Wrackham dreams. | `ending/the-return` |

Neither ending is labelled good. Davey lives in both; the two other sleepers who walked out and Marrack's two men do not come back in either.

Skies:

| sky | when |
|---|---|
| `night` + `clear` | the whole campaign |
| `dawn` + `clear` | `ending/the-keeping`; the bay under the sea-fog atmosphere, the town clear |
| `dawn` + `rain` | `ending/the-return`; the sea-fog atmosphere over the bay and the town |

## Acts and quests (outline for step 3)

1. **The Coach Road** — arrival, classes, the view.
2. **The Harbourmistress** — Wenna; the Customs House key.
3. **The Fish Market** — the fight; first creep.
4. **The Rubbing** — Tregear reads the Brow Stone.
5. **The Customs House** — the chart; the chip; second creep.
6. **No Boats** — the Boatyard; the Whalers' Shed; the Flensing Spade.
7. **The Lighthouse** — the lamps on the flat; third creep; down to the Slipway Stair.
8. **The Wreck Field** — onto the flat; the fight; sink stage 1.
9. **Marrack** — the launch, the log; sink stage 2; the Carved Pillars.
10. **The Narrows** — the first tentacle; sink stage 3; Flank Ridge; the Jaw Bank.
11. **The Throat** — the endless corridor and the wrong rib.
12. **The Cathedral** — the lice; the diaphragm cut; the Stomach.
13. **The Heart** — Davey; the three valves.
14. **The Brow** — the spine stair; the cut.
15. **The Run** — the collapse behind, the causeway, the creep lifting.
16. **The Pier** — the choice (finale).

`min_players` stays 1: the split divides information, and the Breach lets one player carry both halves.

## NPCs

Four, each with one job; the sleepers are a crowd (the `cast` ledger with a bark pool), not characters.

| NPC | job | where |
|---|---|---|
| **Wenna Coyle**, harbourmistress | hires the party and tells them what the town is living through; says plainly that she is afraid of the dream; waits at the Slipway Stair and on the Pier | Harbour Office → Slipway Stair → Pier |
| **Absalom Tregear**, archivist | reads the Rubbing: what the Brow Stone does, and that the bottom row is lost; the keeper of the stone in one ending | Seamen's Chapel → Pier |
| **Ivo Marrack**, salvage captain | the earlier visitor: how to get in, what happened to his men; his log | Marrack's Launch |
| **Davey Coyle**, Wenna's son | the sleeper who did not come back; found by the heart, speaking the dream; woken when the beat stops | Heart Chamber → Pier |

Each is a player model with its own skin. None fights. The watcher is a staged body (an enderman), not an NPC.

## Classes

| class | role in plain words | kit |
|---|---|---|
| **Harpooner** | mid-range fighter: throws a trident and calls it back | trident (Loyalty), leather and chain armour, food |
| **Flenser** | front-line fighter: a heavy axe and heavy armour; slow, very hard to kill | iron axe, iron armour, shield |
| **Wrecker** | ranged fighter: a crossbow from behind the line | crossbow, arrows, leather armour, iron sword |
| **Coxswain** | support: keeps the crew alive | sword and shield, splash healing potions, extra food |

The Flensing Spade is a story item found in act 1, not a class item, so no route depends on who chose what. Rest is by checkpoint only; there are no bonfires, so no class owes a flask.

## Fights

The antagonist is never fought. Fights are short and serve pace.

| where | what | count |
|---|---|---|
| Fish Market | the Drowned up the slipway | one wave |
| Boatyard | the Drowned among the hulls | one wave |
| Wreck Field | the Drowned out of the hulls | two waves |
| Rib Cathedral | lice (silverfish) out of the walls | one swarm |
| Stomach | the Drowned that were Marrack's men | one wave |
| The Run | tentacle strikes beside the way | telegraphed, non-lethal |

The Drowned walk on land and are fought on land. Night, so nothing burns.

## The five lab techniques, and where each lands

| technique | engine capability | where |
|---|---|---|
| tentacle of animated display entities (station 1) | A′ | the Narrows (the first); the flank wounds in the split (one per round, seen from the Flank Ridge); the Crown (standing); the Brow (all rise, the largest over the Brow); the Run (strikes) |
| the wrong place (station 2) | A | the Seawall threshold; three creeps up the town; the whole flat; the inside zone; the lifting at the end; the sea fog of `ending/the-return` |
| perception effects (station 3) | C | the chip in the Customs House (light form, the toucher only); a wrong valve (the opener); the cut at the Brow (full, everyone on the Brow) |
| endless corridor (station 4) | D | the Throat |
| the living room (station 5) | E, and sculk in the prefab | the Heart Chamber (sensors, shrieker, pulse floor, watcher); the watcher also in the High Street and on the flat; the heartbeat through the whole interior |

## Danger model

- **The sea is water, not a killer.** Water uncovered by the sinking is visible and swimmable; a body that goes in swims out. The route proof never counts swimming, and the marked way never needs it. Anyone who swims off the map is returned by the `boundary`.
- **The sinking never takes the ground under the way.** Each stage clears mud beside and behind the party, and is fired by a beat the party has completed — never by time. The marked way stays dry until the Run.
- **The Run's collapse is behind the party, and a fall into it costs a respawn, not the run.** Each section collapses when a player passes the next marker; that same trigger sets a checkpoint ahead of the collapse. The collapsed ground drops into water with a killing volume at the bottom of the hole, which exists only from the collapse onward (a staged lethal volume) — before the collapse it is under solid mud and unreachable. A straggler who falls returns at the checkpoint ahead of the party, not behind it.
- **The Stomach pool** is a lethal volume at the bottom of a deep pool behind a curb of bone, entered only by climbing over the curb — danger visible, like Vesperhold's Undertide Pool.
- **Falls from the body** (the Crown, the spine ridge) are falls off a visible edge; the walk along the spine is wide enough that nothing on the way pushes a body off it.
- **Tentacle strikes** are announced: the tip curls over the spot for two seconds before it comes down, and the damage is set below a full health bar.
- **The heart's pulse** after a wrong valve is non-lethal and announced by the heartbeat quickening.

## Light

Light is placed with each room and the engine only checks. Every walked cell is lit at the night floor.

- **Town:** lanterns on brackets at doors and along the seawall, lit windows, the lighthouse lamp, candles in the chapel.
- **Flat:** the lamps on the marker stakes of the Pilgrims' Way (lit by the lighthouse beat, before anyone walks the flat), lanterns on Marrack's launch.
- **Body, outside:** moonlight, and the lamps on the Jaw Bank Marrack's crew left.
- **Body, inside:** what earlier visitors brought (Marrack's lamps and chalk-marked lanterns in the Mouth, the Throat and the Stomach), moonlight through the wounds in the Rib Cathedral, and in the Heart Chamber the sculk's own sensors plus lanterns Davey's dream did not put out. **Open:** how a giant body's interior is lit without reading as a lit building is a craft question this record does not answer; it is researched against established practice (games set inside giant creatures) before step 2, never invented. Glowing blocks paved over flesh is the shape to avoid.

## Mechanisms: supported today, or the capability each needs

Verdicts from `docs/reference/dsl-coverage.md` at engine revision `9f3f2935` (branch `docs/dsl-coverage`; instrument `delvec 1.7.1, dsl 0.35.0`). Capability letters follow this list: **A** area atmosphere; **C** perception bundle; **A′** animated display assembly; **D** seamless relative-teleport region; **E** living environment (area periodic sound, and the watcher); **F** organic giant-body prefab with walk and light proofs on non-ground surfaces, climbing and jumping, and staged lethal volumes.

| mechanism | act | today | capability | note |
|---|---|---|---|---|
| a site-plan town, terraces, interiors | 1 | S | — | site plan, step 2B |
| branching dialogue, the ending choice | 1, 4 | S | — | M10, `branch_points` |
| sleepers as a crowd with barks | 1 | S | — | M11, `cast` |
| NPCs move with the story (Wenna, Davey) | 1–4 | S | — | M12 |
| fights: Drowned waves, lice swarm | 1–3 | S | — | M21; Drowned on land |
| checkpoints | all | S | — | M50 |
| the Customs House key, the Flensing Spade held to cut | 1, 3, 4 | S | — | M46, `interact.requires_item` |
| lighthouse lights the stake lamps on the flat | 1 | S | — | M28, `set-block` at another anchor |
| the wrong place: threshold, three creeps, the flat, the inside, the lifting, the sea fog | 1–4 | U | **A** | M02 |
| the chip, the wrong valve, the cut | 1, 3, 4 | P | **C** | M20 effects and M40 sounds exist; the curse-face particle, timing inside the bundle and the toucher/opener audience do not |
| the watcher (High Street, flat, Heart Chamber) | 1–3 | U | **E** | needs a spec ruling first: a body that turns every tick but never moves, against §4's refusal of per-tick teleport follow |
| the flat sinks in three stages | 2 | S | — | M03 solid half: `clear-region` of mud over pre-placed sea water; no runtime water fill |
| the hill-sized body seen from the town and the flat | 1–2 | U | **F** (placement only) | nobody stands on it in acts 1–2, so only the prefab is needed, not the walk proof |
| tentacles from the wounds; all rise at the Brow | 2–4 | U | **A′** | several assemblies at once; view range about 64 blocks, so each is watched from within that distance |
| the endless Throat, released by the wrong rib | 3 | U | **D** | the route proof must show the loop ends and the release is reachable |
| heartbeat through the interior | 3 | U | **E** | area periodic sound, switched by story |
| sculk sensors, shrieker, pulse floor | 3 | S | — | vanilla block behaviour in the prefab; shrieker placed with summoning off |
| walking inside and on the body | 3–4 | U | **F** | walk and light proofs from non-ground surfaces |
| the valve rounds, wrong resets | 3 | S | — | M47, `state` + `requires_state`, `clear-state` |
| spotter outside, valves inside | 3 | S | — | information crosses; no same-moment condition (M27 not needed) |
| the spine stair, the blowhole | 4 | U | **F** | built as steps; ladders or jumps on the road would also need climbing and jumping (M05, M06) |
| collapse behind the Run | 4 | S | — | M33 `collapse`, `clear-region` |
| killing volume in the collapse holes from the collapse on | 4 | P | **F** (staged lethal volumes) | M04: a lethal volume is always live; the hole is unreachable before the collapse, but `DW0891` and the route proof must judge it per stage |
| telegraphed tentacle strikes | 4 | P | **A′** + composition | `damage-players{in}` exists; tying it to a clip's frame is composition in a `sequence` |
| the town's sky returns as the creep lifts | 4 | U | **A** | the same repaint, in reverse |
| hour changes at the endings | 4 | S | — | M13 |
| the Rubbing and the carved pillars as block reliefs | 1–2 | S | — | prefab content |
| Marrack's log as a readable book | 2 | P | — | M14; read through `interact` + `narrate` instead; not required |
| glow squid in the Stomach pool | 3 | U | — | `locomotion: aquatic` refused (`DW0455`); glow lichen and sea pickles under the water instead; not required |
| a boat across the bay | — | U, excluded | — | M08 refuses vehicles; the fiction answers it (the boats are staved in) |
| water rising to a height | — | U, excluded | — | spec-0038 open; the tide is shown by mud cleared off standing water, never water that rises |

## What can be built before F

**Acts 1 and 2 can be built, walked and proved before F exists.** Neither puts a body on the Fathomer: act 1 is the town, act 2 is the flat, and both see the body only from a distance. They need **A** (the creep and the flat), **C** (the chip), **E** (the watcher, after its spec ruling), and **A′** (the Narrows tentacle, act 2), plus the Fathomer placed as a prefab that nobody walks (F's placement half only — a stand-in massing serves until the organic-voxel research hands over a real body). Content for acts 1–2 and the engine work on A, C, E and A′ proceed in parallel.

**Acts 3 and 4 wait on F** (walk and light proofs inside and on the body; staged lethal volumes for the Run) and on **D** (the Throat).

| act | needs |
|---|---|
| 1 Wrackham | A, C, E; F placement only (the far view) |
| 2 The Crossing | A, A′, E; F placement only |
| 3 Inside the body | A, A′, C, D, E, F |
| 4 The Brow and the escape | A, A′, C, F (walk proofs on the body, staged lethal volumes) |

## Capability limits (said, not faked)

- **No boats, no rising water.** The crossing is on foot; the tide is mud cleared off standing sea water.
- **The body never moves as blocks.** Moving block structures are refused permanently; the Fathomer moves through its tentacles, its eye and the ground around it. At the end it goes out of sight under the sea fog that comes in with the tide, in both endings; it is never shown sliding away or sinking.
- **The sun stays where it is.** An atmosphere zone cannot move the sun in the overworld; the night darkens every zone's colours.
- **Display entities share one light level and render to about 64 blocks.** Each tentacle is watched from within that range; their segments read as boxes where they bend hard.
- **Perception effects are weakened by accessibility settings** (Distortion Effects, Darkness Pulsing, Particles). The design never hides information in them.
- **No party-size scaling.** Fights are tuned for two to four at `normal`.
- **NPCs never fight, lie down or kneel.** Davey is found standing.
