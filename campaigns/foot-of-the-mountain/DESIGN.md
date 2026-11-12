# Festival Day in Kelderby — design record

A cheerful, comic delve on the town at the foot of the mountain: the town's festival day, from dawn to midnight. 1–4 players, two to three hours, one fight (at dusk). The tension comes from things going wrong, never from a threat. Every daytime task is a soft failure: a task not done in time still lets the day go on; it only leaves the party one tool fewer at dusk and the ending one more joke. There is no hard failure anywhere. Each landmark carries a different verb; the town's people only hand out trouble and do not run conversation chains. Every later round is judged against this file.

This record transcribes the owner's festival-day script. Where the script is silent, the line says *authored*.

## The three acts and the clock

The clock is locked and jumps with progress; it never runs on its own.

| act | time | what happens |
|---|---|---|
| one | dawn → noon | the host opens the day on the stage; five tasks |
| two | dusk | raiders land by boat to take the festival; three waves |
| three | night | the festival; the ending is composed from the day's flags |

Opening: Hedda Brask, the innkeeper who hosts the festival, announces it from the stage on the square, and at once everything goes wrong. Tasks A–D open together and are done in any order (a party can split up); task E opens when D is settled. When A–E are all settled — done or lost — the party returns to the stage and act two begins.

*Authored*: the clock stands at 07:00 at the start (`daytime` 1000), 10:00 when the lamp is settled (4000), noon when the fox is settled (6000), 18:00 on the return to the stage (12000), midnight for the festival (18000).

## The day's tasks

| task | landmark | verb | success | soft failure | what it gives at night |
|---|---|---|---|---|---|
| A | the dock and the bay | rowing | ≥4 of 6 floating crates rowed back to the delivery point beside the harbour house in time | the rest sink | food in the three defence lines' supply chests; the feast |
| B | the main street | luring animals | Kettil's three goats in the pen on the main street by dusk, led with wheat from the field on the flank | the shepherd brings them back; failure | the pen at the street's throat; the goats charge once as the raiders pass |
| C | the cathedral | archery | three hits on the target in the belfry from the marked shooting point on the main street (25–30 blocks) in time | — | the forecourt bell can be rung: every raider glows for 10 s, with a cooldown |
| D | the lighthouse | climbing | the lamp room relit after a light-parkour climb past broken stairs, in time (*authored*: the window) | the lamp stays dark | the second landing is called 30 s early, with its side |
| E | the castle road to the castle | chasing | the fox, driven by script between four hiding places to its den by the castle gate, the key taken, the fireworks fetched in time | the fox sits in its den; half the fireworks | rockets for crossbows (area damage); the rest for the festival |

The spyglass on the lighthouse's gallery shows the fox with the shining key on the castle road: that is what opens E. *Authored*: the four hiding places are the four places beside the castle road — the wayside spring, the bee garden, the herder's hut, the lookout — and the den is under the gate road's bank.

Every bit of the day that rests on an animal's own behaviour has a deterministic fallback: the fox is driven by script for the whole chase; the goats are judged by whether they are inside the pen, and when time runs out the shepherd leads them home and the task is lost.

## Dusk

Back on the stage, the clock jumps to dusk and a horn sounds. Raiders come for the festival cake on the stage; a few slimes may be mixed in. Waves are scripted, never the game's raid; their size scales with the number of players.

1. The dock landing, straight up from the quay.
2. The flank landing on a beach to one side; the side is fixed by the author. The lighthouse only decides whether there is a warning.
3. The captain and his vindicators push up the main street.

A player who dies comes back on the stage. A raider who reaches the stage takes the cake: the fight still ends, and the ending has no cake. The day's flags change only what the party holds, never the waves.

Three defence lines along the main street — the dock square, the stretch by the goat pen, the cathedral forecourt with the stage — each with cover (hay bales, carts, festival stalls) and a supply chest. The raiders' way up is friendly to a mob's pathfinding: steps or slabs, no two-block rise, no dead end.

## Night

The clock jumps to midnight, the whole town's lamps come on, the townsfolk walk to the audience's places, and the party fires the remaining rockets from the castle's platform or from the stage.

| flag | done | lost |
|---|---|---|
| `cargo_saved` | a full feast | only bread on the table |
| `goats_home` | in their pen | on the stage |
| `bell_fixed` | the festival opens on the hour | the bell rings halfway through |
| `lighthouse_lit` | the beam sweeps over the festival | the host reads her speech in the dark |
| `fireworks_full` | a full sky | a few rockets |
| `cake_safe` | the cake stands | the host speaks to an empty plate |

The woods stay walkable at night and are hung with festival lanterns, placed as part of the woods' design, until every cell under the trees clears the light check (the owner's ruling).

Optional: a pig race on the festival night, carrot on a stick, from the cathedral down the main street to the dock. For fun; not part of finishing.

## The map this needs

Over the town as built, filling the empty flank with places that have a use before more trees: two boats and a delivery point at the dock and a berth for the raiders' boats; six crate points in the bay's shoals, two beyond the sandbar; a landing beach on the flank with a walkable route to the main street; the wheat field on the flank; three goat start points on the terraces and the foothills; the goat pen on the main street; the shooting point and the bow stall on the main street, with the line to the belfry; the belfry target and the forecourt bell; the lighthouse's climbable inside, its two-state lamp room and its gallery's sight of the fox's road and both beaches; the walkable road from the cathedral's side up to the castle with four hiding places and the den by the gate; the castle's fireworks storeroom, crossbow rack and launch platform; cover and a supply chest on each of the three lines; the cake table, the audience's places and the decorations on the stage that hang only at night. Every new reachable cell passes the light check.

The owner's map notes from the town's pictures are carried in the same fill: farmland, ponds, orchards, sheep and cattle pens and buildings on the empty land between the town and the forest; a grid of streets and buildings beside the main street; the cathedral's flat cross-shaped top becomes a ridged pitched roof; the gap beside the guildhall is closed; the lighthouse's bare ground and the headland beyond its trees get something worth looking at.

## The ending

*Owner's requirement*: the festival ends on a cutscene of a very lavish firework show — the sky full of rockets — over the townsfolk gathered together on the square. Built: three shots of eleven seconds each (from the stage over the crowd toward the sky over the main street; from high over the street back at the square; from behind the crowd), and under them rockets in layered volleys from ten marks along the top of the main street every half second, every flight, every shape and a mix of colours, closing on a finale burst from every mark at once; the ending follows the last shot. When the fireworks were not fetched in time the same cutscene plays over a few rockets with long gaps between them (the script's `fireworks_full` lost line). The townsfolk stand in a loose crowd on the square's west half, each on a cell with open sky and a clear cell round it. Under the whole show the crowd is glad (*authored* from the owner's requirement): everybody first turns to look up at the sky over the main street; each holds something up — Hedda a torch, Inga a lantern, Oskar a cake, Agathe a poppy (and a sunflower in her hat), Bernt a rocket, Sverre a fish, Kettil a sheaf of wheat (and a pumpkin on his head), Vidar the bell; six of them hop again and again, each a few ticks after the one before, so the hops roll through the crowd; four bounce, crouching and standing in turn; hearts rise over every head and notes over the hoppers, and a cheer runs through the crowd every four seconds.

## Departures from the script

- The party comes back from a death in the inn's taproom across the square, not on the stage: the stage is where every raider's lane ends, and a body brought back there is brought back into the fight (`DW0478`).
- The fireworks storeroom does not wait on the key taken off the fox: an objective gated on the key is armed only once the party stands at the den, out of sight of the cellars, so its hint would come too late (`DW0863`, measured again with the gate on the key). The key is still taken off the fox at the den.
- The wheat field is drawn cut, its sheaves stood in stooks of hay: a piece may not hold crops, which change after the proofs have judged them (`DW0730`). The wheat the goats follow is taken from the field's chest by the hay cart.
- *Authored*: the goats stray to the castle road's switchbacks above the square (Pearl), the wayside spring (Barley) and the orchard on the farm track (the Admiral); the pen is on the main street's fifth stretch, opening east off it halfway down.

## Characters

Hedda Brask (host), Inga (lighthouse keeper, D), Bernt (castle steward, fireworks, E), Sverre (boatwright, A), Kettil (cooper and goat keeper, B), Vidar Foss (guildhall clerk, who rings the bell, C), Oskar (baker of the cake), Lady Agathe Holm (guest of honour). The fox is an actor; the raiders are waves.

## What the build carries now, and what waits

`GENERATION.md` names the engine revision. Every task is in the documents: A (rowing Sverre's boats over the bay to the six crates on its shoals and the sandbar, landing them at the harbour house), B (the goats, the wheat, the pen's latch, the goats on the stage when they are lost), C (Vidar's bow, three hits on the belfry target, the bell and its glow on the raiders at dusk), D (the climb, the relight and the spyglass that spots the fox), E (the chase, the key taken out of the fox's mouth at its den and the fireworks fetched in time); the dusk waves scaled to the party, the crossbows and starred rockets, the lighthouse's warning, the inn as the checkpoint and the cake taken by a raider who reaches the stage; the night's bunting and lanterns over the main street, the woods' festival lanterns, the gathered and glad town, the lavish show and the ending reading all six flags. The pig race on the festival night.

On the map: the bay with its shoals, sandbar and the boats' slips; the goat pen on the main street; the cake table and a supply chest with hay-bale cover at each of the three defence lines (the quay, the goat pen, the stage's foot); the net green and the beacon point by the lighthouse; the farm district on the east flank; and, from the owner's second look at the town from the sea, the west terraces (the west track off the quay's end, the archery butts with the bow stall, the allotments, a croft, the bonfire green on the shore, and above them the terrace track off the back of the fishmonger's yard with the terrace orchard, a cottage, the sheep terrace and the kitchen garden), the east meadow behind the beach (the meadow track off the cliff path, the festival fair field round its maypole with its trestle tables, bonfire and dance floor running down toward the beach, the bee meadow, the dune cottage) and three pockets in the town (the games yard above the harbour house, the lantern-makers' yard between the houses, the cathedral garden below its south side).

Waiting on the engine: the food in the supply chests (A's payoff; a container's own cell cannot carry the name a fill is written to), and the goats' charge at dusk (no scripted charge with knock-back exists). Not placed: the gap beside the guildhall and the grid of back streets west of the main street (each needs the plan's west half re-laid). Nothing of these is replaced by another verb in the meantime.
