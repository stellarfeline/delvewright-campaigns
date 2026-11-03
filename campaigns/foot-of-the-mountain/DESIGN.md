# Curtain Up in Kelderby — design record

A cheerful town RPG on the town at the foot of the mountain, as built. 1–4 players, about two and a half hours, no fighting. Every later round is judged against this file.

## The premise

Every year at sunset Kelderby performs the Founders' Play on the cathedral square. It retells the town's legend: a fisherwoman, the Founder, sailed into the bay; a Dragon on the mountain demanded a loaf a year; she baked the first Mountain Loaf; the Dragon became the town's friend. The bakery still bakes a Mountain Loaf every year, and the lady of the castle has played the Dragon for thirty years.

The party walk into town on the afternoon of the play. Hedda Brask, the innkeeper who directs it, takes them for the travelling troupe she hired, who never came. The play is missing three things — its Dragon, its Founder and its Loaf — and the party have until sunset.

Hedda knows inside a minute that the party are not the troupe. She keeps it to herself until the curtain call, where she says so to the audience.

## The map

The town as built, with nothing rebuilt. Placement named where things happen (layout-graph `beats[]`), moved the goal from the quay to the square (the play is on the square), and re-derived the authored `critical_path[]` as the mandatory walk: square → castle → square → bakery → smithy → lighthouse → smithy → bakery → square.

| place | what happens there |
|---|---|
| the square (`node/square`) | the hub, Hedda; the finale, the play |
| the castle (`node/castle`), up the castle road | spoke A, the Dragon: Bernt, Lady Agathe, Dumpling |
| the lighthouse (`node/lighthouse`), by lane-8 and the cliff path | spoke B, the Founder: Inga, Sanna |
| the bakery (`node/bakery`) and the smithy (`node/smithy`) on the main street | spoke C, the Loaf: Oskar, Runa |
| the tavern, the cooper's, the net loft, the boatwright's | optional strand, the chorus: Fenna, Kettil, Mari, Sverre |
| the weaver's and the guildhall | optional strand, the curtain: Elin, Vidar |

The spokes are in three districts — the mountain, the middle street, the headland — and none of them shuts or opens a way another one crosses. No connection is gated.

## The web

- **Hub** `quest/the-troupe` (square). Hedda takes the party for the troupe and gives them the three missing things. All three spokes and both strands open when it completes.
- **Spoke A** `quest/the-dragon` (castle). Lady Agathe will not come down: a jackdaw has nested in the costume's tail, and she will not evict a neighbour. She also says plainly that she is afraid she is too old for the part. Choice, a flag on each option: **move the nest** to a box in the courtyard and she wears the whole costume (`flag/tail-nest-moved`), or **let Dumpling be the tail**, the ghast floating behind her wrapped in sailcloth (`flag/tail-dumpling`). Dumpling comes down to the square only on the second branch — a fork in the cast, declared as `branch-point/the-tail`.
- **Spoke B** `quest/the-founder` (lighthouse). Sanna has run to her aunt's lighthouse. She knows every line until a face looks at her, and rehearses to a row of buoys she has painted faces on. Choice, a flag on each option: **bring the buoys** to sit in the front row (`flag/founder-buoys`), or **turn the speeches into a net-mending work-song** her hands already know (`flag/founder-song`). The finale reads it in dialogue and epilogue only.
- **Spoke C** `quest/the-loaf` (bakery, smithy). Runa mended Oskar's oven door and has hung it over her forge as a trophy; she will hand it back when somebody admits a forge bakes better. Choice, a flag on each option: **take the door back** and bake in Oskar's oven (`flag/loaf-oven`), or **bake it in the forge**, which Runa swears is quicker (`flag/loaf-forge`). The forge loaf comes out as hard as an anvil. Declared as `branch-point/the-loaf`: the forge branch runs to its own ending.
- **Optional strand** `quest/the-chorus` (tavern, and three houses). Fenna's shanty chorus has scattered: Kettil sings only where nobody looks at him, Mari can reach the harmony nobody else can, Sverre waits to be asked by name. Finishing it adds one to `state/applause` and sets `flag/chorus-done`; the chorus then stands on the square at the finale — a fork in the cast, declared as `branch-point/the-chorus`, its other branch `flags: []`.
- **Optional strand** `quest/the-curtain` (weaver, guildhall). Elin has woven a new curtain; Vidar Foss says it blocks the square's fire lane, and he is right. The party carry the by-law back and Elin re-hangs it to clear the lane. Finishing it adds one to `state/applause` and sets `flag/curtain-done`. Read by dialogue and epilogue only.
- **Finale** `quest/opening-night` (square), after all three spokes. The party take their places; Hedda raises the curtain; the play is told scene by scene, each scene reading what the run did. When Sanna loses a line, the party prompt her through the dialogue options, and what they can offer depends on the buoys or the work-song.

## The endings

`endings_read`: at least 3 inputs, at least 1 deed.

| ending | gate | what happens |
|---|---|---|
| `ending/encore` | `flag/loaf-oven`, `state/applause` ≥ 2 | the play runs whole, the town calls for it again, and Lady Agathe promises to come down every year |
| `ending/curtain-call` | `flag/loaf-oven`, `state/applause` ≤ 1 | the play runs whole and the town goes home pleased |
| `ending/no-ending` | `flag/loaf-forge` | the Dragon cannot bite the forge loaf, the play stops before its last scene, and the town argues happily into the night about how the legend ends; it is never settled |

The epilogue then says what each thread came to: the tail (nest or Dumpling), the Founder (buoys or work-song), the chorus (sung or not), the curtain (hung or not). Each is an input the final scene reads.

The deciding deed is elective: `state/applause` is written only by the two optional strands.

## Cast

Fourteen NPCs; nine speak with the party in the mainline. Each named character gets a face (a player-model skin) at step 5, except Dumpling, who is a happy ghast. Faces, to brief the skins:

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

## The hour

`time` is late afternoon (`{"daytime": 10500}`), `weather` clear: the party arrive in golden light, and the finale is the sunset the play is set at. Whether the finale moves the clock to sunset is a step-5 decision against the brightness checks.
