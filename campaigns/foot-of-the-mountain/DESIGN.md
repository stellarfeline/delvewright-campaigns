# Curtain Up in Kelderby — design record

A cheerful town RPG on the town at the foot of the mountain, as built. 1–4 players, two to three hours, no fighting. Every later round is judged against this file.

## The premise

Every year at sunset Kelderby performs the Founders' Play on the cathedral square. It retells the town's legend: a fisherwoman, the Founder, sailed into the bay; a Dragon on the mountain demanded a loaf a year; she baked the first Mountain Loaf; the Dragon became the town's friend. The bakery still bakes a Mountain Loaf every year, and the lady of the castle has played the Dragon for thirty years.

The party walk into town on the afternoon of the play. Hedda Brask, the innkeeper who directs it, takes them for the travelling troupe she hired, who never came. The play is missing three things — its Dragon, its Founder and its Loaf — and the party have until sunset.

Hedda knows inside a minute that the party are not the troupe. She keeps it to herself until the curtain call, where she says so to the audience.

## The map

The town as built, with nothing rebuilt. Placement names where things happen (layout-graph `beats[]`); the goal is the square; the authored `critical_path[]` is the mandatory walk: square → castle (and through it) → square → bakery → the spring and the bee garden on the castle road → smithy → the lower town's yards and the harbour → lighthouse → back up the main street → bakery → square.

| place | what happens there |
|---|---|
| the square (`node/square`) | the hub, Hedda; the finale, the play, its curtain lever on the stage |
| the castle (`node/castle`), up the castle road | spoke A, the Dragon: Bernt at the courtyard, Lady Agathe in the great hall, Dumpling; the kitchen, the royal apartments and the wall walk searched; three candles in three of the lady's rooms |
| the lighthouse (`node/lighthouse`) and the lower town's yards | spoke B, the Founder: Inga, Sanna; four pumpkins hidden in the fishmonger's, the chandler's, the harbour and the lower cottages |
| the bakery, the wayside spring, the bee garden, the smithy | spoke C, the Loaf: Oskar, Runa; the recipe board, the spring, the hive, the oven door |
| the tavern, the cooper's, the net loft, the boatwright's | optional strand, the chorus: Fenna, Kettil, Mari, Sverre; the big tub, the bell, the hull |
| the weaver's, the inn's front, the cathedral | optional strand, the curtain: Elin; Vidar and Fenna as witnesses; the drying frame, the inn's bench, the by-law book |
| the castle's lord's hall and cellars, the apothecary, the tannery, the herder's hut, the lookout, the potter's, the upper cottages, the carpenter's, the merchant's | side finds, and the merchant's stall |

Adjustments inside plots ("moderately"): Lady Agathe stands in the castle's great hall (`anchor/stop-great-hall`), not on the courtyard path; Oskar, Runa, Kettil, Mari, Sverre and Elin stand two steps off their places' marks, which now hold the thing pressed there. The castle's program already marks its rooms; the layout graph declares nine of them as the castle's stations. No box, seam, piece or program changes.

The spokes are in three districts — the mountain, the middle street, the headland — and none of them shuts or opens a way another one crosses. No connection is gated. The three spokes and the two strands are taken in any order, by one player or by several at once; inside each one its steps keep their order.

## The web: each line and what the player does in it

Every line but the hub and the finale has at most two `talk-to` objectives: talk opens a line and closes it, and the body is something the party does.

- **Hub** `quest/the-troupe` (square). Hedda takes the party for the troupe and gives them the three missing things, and tells them the play's order: the Founder, the Dragon, the Loaf. *Talk 1.* All three spokes and both strands open when it completes.
- **Spoke A** `quest/the-dragon` — *a search of the castle, with one puzzle.* Climb to the castle (`reach-anchor`); Bernt, who packed the Dragon costume away after last year's play, tells where the pieces went (`talk-to`). The head is in a trunk in the kitchen (`collect`). Upstairs are the lady's rooms (`reach-anchor`). The wings are in a trunk in the royal apartments that the old lady latched with the candle lock: three unlit candles stand in three of the lady's rooms — blue in the duchess's hall, red in the bedchamber, yellow in the oratory — and the latch gives when they are lit in the order the play is told (the Founder's sea, the Dragon, the Loaf). A candle pressed out of turn will not take, and says so; the party try another. Each candle is a real candle pressed and lit. Nobody recites the order: Bernt says the latch wants the order the play is told and that the lady keeps every programme framed in the lord's hall; the programmes there list the three scenes with their colours (the Founder's blue sea, the Dragon's red mountain, the Loaf's golden oven); Hedda's telling of the legend gives the same order of scenes. Then the wings (`collect`, waiting on the latch). On the wall walk the tail hangs drying with a jackdaw nesting in it (`reach-anchor`). In the great hall Lady Agathe will not evict a neighbour, and says plainly she is afraid she is too old for the part (`talk-to`). Choice, a flag on each option: **move the nest** to a box in the courtyard (`flag/tail-nest-moved`), or **let Dumpling be the tail** (`flag/tail-dumpling`). Dumpling comes down to the square only on the second branch — `branch-point/the-tail`. *Reach 3, talk 2, collect 2; the puzzle is three pressed candles.*
- **Spoke B** `quest/the-founder` — *a hide-and-seek in the lower town.* Sanna, the Founder, has climbed into the lamp room. She rehearses only to an audience of pumpkins she carved faces into, and the harbour children have hidden them all over the lower town for a lark. Inga sends the party after them (`talk-to`). The four pumpkins stand in the harbour, the fishmonger's yard, the chandler's and the lower cottages (four `interact`s, one pumpkin picked up at each), each found three ways: its hint, Inga naming the place again, and the pumpkin itself, a carved face where nothing else has one. Then Sanna, with her audience back (`talk-to`). Choice, a flag on each option: **the pumpkins in the front row** (`flag/founder-buoys`), or **turn the speeches into a net-mending work-song** her hands already know (`flag/founder-song`). The finale reads it in dialogue and epilogue only. *Talk 2, interact 4.*
- **Spoke C** `quest/the-loaf` — *a gathering on the mountain, and a door won one of four ways.* Oskar's recipe board says what the Mountain Loaf needs (`interact`: read it, and Oskar hands over a bucket and a bottle). The party fill the bucket at the wayside spring and the bottle at the bee garden's hive (two `interact`s, each with the vessel in hand). The oven door lies on Runa's bench by the forge as a trophy (`talk-to`, four ways, each its own flag Runa remembers): talk her round with what a found page of her ledger tells (`flag/door-persuaded`), tell her where the herder left her lost lucky horseshoe (`flag/door-traded`), lift it off her bench while she is busy at the anvil (`flag/door-lifted`, a press on the door, which she then owns up to), or admit, as she wants, that a forge bakes better (always open, the way with no flag of its own). Back at the bakery (`talk-to`), choice, a flag on each option: **bake in Oskar's oven** (`flag/loaf-oven`) or **in Runa's forge**, which she swears is quicker (`flag/loaf-forge`). The forge loaf comes out as hard as an anvil — `branch-point/the-loaf`, the forge branch running to its own ending. *Talk 2, interact 3.*
- **Optional strand** `quest/the-chorus` — *a hunt by ear, by bell and by name.* Fenna's shanty chorus has scattered (`talk-to`). Kettil sings only where nobody looks at him: the compass will not point at him, and a low hum sounds from the cooper's yard until the party lift the lid of the big tub he is sitting in (`interact`). Mari can reach the harmony nobody else can, but only after she hears her note: ring the bell in the net loft's yard (`interact`). Sverre waits to be asked by his whole name, which is painted on the hull he is building: read it out (`interact`). Back to Fenna with her chorus (`talk-to`). Finishing it adds one to `state/applause` and sets `flag/chorus-done`; the chorus then stands on the square at the finale — `branch-point/the-chorus`, its other branch `flags: []`. *Talk 2, interact 3.*
- **Optional strand** `quest/the-curtain` — *an investigation.* Elin's new curtain has vanished off her drying frame since dawn (`talk-to`). The clues: the drying frame, where somebody has pencilled lengths on the post (`interact`); a thread of the curtain's blue caught on the bench by the inn's door (`interact`); and in the cathedral the by-law book, open at the fire-lane page, a playbill for a bookmark with a pencilled "measure!" (`collect`). The witnesses, in their own dialogue: Vidar, who objected to the curtain and says so; Fenna, who saw a blue bundle carried towards the square at dawn; Hedda, who changes the subject. Then the party name the taker to Elin (`talk-to`): Hedda, who took it to measure it so it could hang clear of the fire lane, is the answer and always on offer; each clue found adds a better way of saying it. A wrong name costs something real and mendable: naming Vidar sends Elin to scold him (`flag/accused-vidar`), and he stays stiff with the party until they apologise (`flag/vidar-forgiven`); naming the harbour children, who are Inga's to mind, puts Inga out with the party (`flag/accused-children`) until they set it right with her (`flag/inga-forgiven`). The curtain's return says whether a wrong name was mended. Finishing it adds one to `state/applause` and sets `flag/curtain-done`. *Talk 2, interact 2, collect 1.*
- **Finale** `quest/opening-night` (square), after all three spokes. The party go back to the square (`reach-anchor`), the evening comes on, they pull the curtain lever on the stage (`interact`), and Hedda runs the play from her own dialogue (`talk-to`): the Founder's scene, the Dragon's scene and the Loaf's scene, each offering what the run made possible, then her curtain call. *Reach 1, interact 1, talk 1.*

Objective kinds: 32 objectives — 12 `talk-to`, 4 `reach-anchor`, 3 `collect`, 13 `interact` (the previous version: 18, of which 16 `talk-to` and 2 `reach-anchor`).

## Side content

None of it is needed; all of it pays.

- **Overheard** (8; a scene that plays in chat as the party come near, once): Hedda rehearsing alone by the stage; Bernt talking to Dumpling at the castle gate; Inga calling up the lighthouse stairs; Fenna grumbling about her lost chorus (points at the chorus); Elin wailing at her empty drying frame (points at the curtain); Runa boasting to her anvil; Oskar talking to his dough; two fishing boats calling across the bay, heard from the quay.
- **Finds** (9; a thing pressed once, read in chat, a penny to whoever finds it): in the castle's lord's hall, thirty years of Dragon programmes; in the castle cellars, the steward's biscuit tin (three pennies); at the apothecary's, a calming tea recipe; at the tannery, a page of Runa's ledger; at the herder's hut, the herder's note about a smith's horseshoe he found; at the lookout, a board of initials on the rail; at the potter's, a pot with a song painted round it; at the upper cottages, the troupe's letter, delivered to the wrong door; at the carpenter's, a carved dragon's head. Five of them open a better line with someone (Agathe, Sanna, Runa twice, Kettil), and one gives Hedda a line at the curtain call.
- **Small events** (3): the cathedral bell over the square, the harbour bell over the quay, fireworks over the cathedral at the curtain call.
- **Trading** (1 stall, 4 offers): the merchant's stall sells a festival ribbon, a sweet bun, a paper crown and sugared almonds for the pennies the finds and the strands pay. The purse is each player's own and stands on the screen.

## The endings

`endings_read`: at least 3 inputs, at least 1 deed.

| ending | gate | what happens |
|---|---|---|
| `ending/encore` | `flag/loaf-oven`, `state/applause` ≥ 2 | the play runs whole, the town calls for it again, and Lady Agathe promises to come down every year |
| `ending/curtain-call` | `flag/loaf-oven`, `state/applause` ≤ 1 | the play runs whole and the town goes home pleased |
| `ending/no-ending` | `flag/loaf-forge` | the Dragon cannot bite the forge loaf, the play stops before its last scene, and the town argues happily into the night about how the legend ends; it is never settled |

The epilogue then says what each thread came to: the tail (nest or Dumpling), the Founder (pumpkins or work-song), the chorus (sung or not), the curtain (found or not). The two smaller outcomes are told where they happen, not in the epilogue: the way the door was won, when Runa hands it over; whether a wrong name was mended, when the curtain comes back. Each is an input the final scene reads. The deciding deed is elective: `state/applause` is written only by the two optional strands.

## Cast

Fourteen NPCs; each named character wears a face (a player-model skin), except Dumpling, who is a happy ghast. Faces:

- **Hedda Brask** — middle-aged, an apron over a good dark dress, a pencil behind her ear.
- **Lady Agathe Holm** — elderly, tall, silver hair up, a green velvet coat.
- **Bernt** — an old steward in castle grey and black.
- **Sanna** — a teenager in a fisher's smock and boots, hair tied back.
- **Inga** — weathered, oilskin coat, knitted cap.
- **Oskar** — flour to the elbows, white cap.
- **Runa** — leather apron, rolled sleeves, soot on her face.
- **Fenna** — tavern keeper, red scarf.
- **Kettil, Mari, Sverre** — working clothes of the cooper, the net loft and the boatwright.
- **Elin** — the weaver, in her own bright cloth.
- **Vidar Foss** — the clerk in a buttoned coat, a ledger under his arm.

## Classes

Four parts in a travelling troupe, each a prop and bread for the walk: The Lead (a feathered hat), The Prompter (a prompt book), The Musician (a horn), The Stagehand (a lantern). No fight is planned, so no class carries a weapon or a flask.

## How long

An estimate, not a measurement; the method is `GENERATION.md`, *Research*, last section. Per line, for an attentive party:

| line | what takes the time | minutes |
|---|---|---|
| arrival and hub | the square, Hedda, the overheard scene, the stall seen | 6–8 |
| the Dragon | the climb and back (the road's four roadside places on the way), Bernt, three rooms searched, the candle puzzle, Agathe | 27–37 |
| the Founder | the lower town and the headland, four pumpkins searched, Inga, Sanna | 22–30 |
| the Loaf | the recipe, the spring and the bee garden up the road and back, the door one of four ways, Oskar | 22–30 |
| the chorus | the hum hunt, the bell, the hull, Fenna twice | 12–18 |
| the curtain | three clues, three witnesses, the name, a wrong name mended | 15–22 |
| the finale | the lever, the play's three scenes, the curtain call, the epilogue | 8–12 |
| side content | 8 overheard, 9 finds, the stall | 15–25 |
| **total** | | **127–182** |

A party that takes only the mainline needs about 85–117 minutes; the strands and the side content are what carry the evening to two to three hours.

## The hour

`time` is late afternoon (`{"daytime": 10500}`), `weather` clear: the party arrive in golden light, and the finale is played in the last hour before sunset. When the party come back to the square for the play (`obj/take-places`, which opens once the Dragon, the Founder and the Loaf are all found), the world cuts to `{"daytime": 11867}` and stays there through the play and the endings. The cut is the one `set-time` in the campaign. Why 11867: it is the latest hour the engine judges as daylight, so the sun stands as low over the sea as it can while the town, lit for the day, stays light enough everywhere a player can walk. The design record's two Scene 7 pictures are drawn and recorded at the same hour.

## What the engine cannot do here, and what stands in for it

- **Dumpling flies, and its walk cannot say so.** A happy ghast's marks stand on the ground (`DW0307` refuses a walk that starts or ends in the air), so Dumpling floats low and walks the ground to the square. A flying body's move is not authorable at `delvec` 1.15.0; recorded, not worked around.
- **A walking NPC takes the shortest standable way down, not the road.** An engine defect being fixed separately; recorded, not worked around.
- **The compass leaves the line the party is on.** When a step completes, the compass follows the first open objective in file order, which can be another line's; recorded as an engine defect.
