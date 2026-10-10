# The Listening Hall

> **Requires delve engine 0.39.0 or newer** — last verified with delvec 1.12.0 on Minecraft Java 1.21.11.

Under the hill a long hall has been sealed for as long as anyone remembers. Its floor is set with listening stones, something in the dark answers them, and at the hall's heart a well of glass holds a light nobody can reach.

One player, about ten minutes. There is nothing to fight. You arrive as the **Listener**, carrying a lantern.

## The demo level

This is the demo level for the sculk family (spec-0100): sculk sensors, a calibrated sensor, a shrieker and a catalyst, each placed as the vanilla block it is, at rest, with nothing their redstone can reach and with the catalyst where no body can be within its hearing. The engine states each of them at build time; the critical-path bot walks the hall and listens for each predicted click and shriek.

| Thing | Where |
| --- | --- |
| Antechamber (where you arrive) | x 8201–8207, z 8236–8242, floor y 64 |
| The hall | x 8200–8208, z 8210–8234, four blocks of headroom |
| Six plain sensors, set into the floor course | west row x 8200 at z 8216, 8224, 8232; east row x 8208 at z 8212, 8220, 8228 (all y 63) |
| Shrieker, `can_summon=false` | in a niche in the west wall at (8199, 64, 8226) |
| Glass well | a 3 × 3 glass lid at x 8203–8205, z 8221–8223 (y 63), over a shaft |
| Catalyst | at the bottom of the well, (8204, 54, 8222): ten blocks under the lid |
| Alcove past the north arch (the way out) | x 8202–8206, z 8204–8208 |
| Calibrated sensor, `facing=north` | in the alcove's north wall at walk height, (8204, 64, 8203); the cell south of it is open air |

## What to look for

Walk it in order:

1. **Every footstep clicks.** Walk north out of the antechamber and up the middle of the hall. At every step at least one sensor in the floor beside the walls should light its tendrils and click. Then crouch and walk: nothing should click.
2. **The shrieker answers, and does nothing else.** About a third of the way up the hall, the niche in the west wall shrieks — its sound and its rising particles — each time a nearby sensor clicks under your feet (at most once every four and a half seconds). Nothing more may follow: no warning sound, no Darkness on your screen, no warden.
3. **The catalyst is visibly out of reach.** Stand on the glass in the middle of the floor and look down. The catalyst glows ten blocks down a shaft you cannot enter. Nothing you do in the hall can reach it.
4. **The far calibrated sensor hears from sixteen blocks.** From the glass, look north through the arch to the alcove's back wall. Walk slowly towards it: the calibrated sensor in that wall should start clicking while you are still out in the hall, about fifteen blocks short of it — twice as far as a plain sensor hears. The bot asserts its click only from within seven blocks (the engine predicts every sensor at a plain sensor's margin), so the sixteen-block reach is yours to hear.
5. **The bloom beat reads.** Walk into the alcove. Behind you, the hall floor between the two rows of sensors is overgrown with sculk veins, sculk particles puff over it, and the catalyst's bloom sounds from the well, with the line "The well flares; the floor darkens." Turn round and look back down the hall: does it read as the floor turning to sculk? Ten seconds later the delve ends.

## State

Built with the engine's sculk integration branch. The build states: 7 sensors (1 calibrated), 47 reach cells checked, 1 shrieker, 1 catalyst, with the nearest body cell at distSqr 100; the waypoint export predicts 7 of 7 sensors and 1 of 1 shrieker on the walk's 2 legs. PackTest passes 12 of 12. The critical-path bot ladder is not yet green on this build.
