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

Optional: a pig race on the festival night, carrot on a stick, from the cathedral down the main street to the dock. For fun; not part of finishing.

## The map this needs

Over the town as built, filling the empty flank with places that have a use before more trees: two boats and a delivery point at the dock and a berth for the raiders' boats; six crate points in the bay's shoals, two beyond the sandbar; a landing beach on the flank with a walkable route to the main street; the wheat field on the flank; three goat start points on the terraces and the foothills; the goat pen on the main street; the shooting point and the bow stall on the main street, with the line to the belfry; the belfry target and the forecourt bell; the lighthouse's climbable inside, its two-state lamp room and its gallery's sight of the fox's road and both beaches; the walkable road from the cathedral's side up to the castle with four hiding places and the den by the gate; the castle's fireworks storeroom, crossbow rack and launch platform; cover and a supply chest on each of the three lines; the cake table, the audience's places and the decorations on the stage that hang only at night. Every new reachable cell passes the light check.

The owner's map notes from the town's pictures are carried in the same fill: farmland, ponds, orchards, sheep and cattle pens and buildings on the empty land between the town and the forest; a grid of streets and buildings beside the main street; the cathedral's flat cross-shaped top becomes a ridged pitched roof; the gap beside the guildhall is closed; the lighthouse's bare ground and the headland beyond its trees get something worth looking at.

## Characters

Hedda Brask (host), Inga (lighthouse keeper, D), Bernt (castle steward, fireworks, E), Sverre (boatwright, A), Kettil (cooper and goat keeper, B), Vidar Foss (guildhall clerk, who rings the bell, C), Oskar (baker of the cake), Lady Agathe Holm (guest of honour). The fox is an actor; the raiders are waves.

## What the build carries now, and what waits

The engine at the revision `GENERATION.md` names compiles the timed beat (a `limit` on an objective) and nothing else the script adds. Built: the opening; D except the spyglass; E except the key taken off the fox and the rockets' stars; the three dusk waves at a fixed count with the lighthouse's warning and the stage as the checkpoint; the night's clock, the walk to the square, the firework show full or thin, and the ending reading the lamp and the fireworks. Waiting on spec-0134 (small surfaces): A's crates in the water, B's census and `body-enters`, C's `shot` trigger and the bell's glow, the spyglass's `use-item`, the key's `use-actor`, the rockets' stars, the per-player counts, the dusk supply fills, the cake's `body-enters`, the night's lamps and bunting as a `by-effect` batch. Waiting on spec-0135 (vehicles): A's boats and the pig race. Nothing of these is replaced by another verb in the meantime.
