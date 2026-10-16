# The Toll Road

> **Requires delve engine 0.41.0 or newer** — last verified with delvec 1.13.0 on Minecraft Java 1.21.11.

The toll wardens left Harrow Gap a generation ago and took nothing with them.
The road through the gap is free now, but the strongrooms cut into its walls
are still set the way the wardens left them, and the toll bar at the head of
the pass is still down.

A demo level of about fifteen minutes, for one to four players. No combat.

## Classes

- **Carter** — you drive goods through the gap. A coat, a knife for rope, and
  bread for the road.

## Playing it

Start the server, then in the Minecraft Java client at the version the marker
above names: Multiplayer → Direct Connect → `localhost:25565`. Accept the
resource pack when the server offers it.

---

## For the owner: what to look for

This level is where traps (spec-0011) are looked at in the game: each trap
kind the engine builds guards one strongroom off the road, and each trapped
strongroom has a disarm lever on the road wall beside its mouth. The machine
has proved that every trigger block stands where its trap is, that every
volley's slot can see every cell of the zone it covers and fires slowly
enough that a player who sets off when it fires can walk out, that the
collapse leaves the strongbox reachable, and that every trap fires from its
PackTest. The bot walked the road and raised the toll bar; it went into no
strongroom. What the machine cannot say is whether a player **reads** each
trap before springing it, and whether the levers teach the counterplay. Walk
the strongrooms in order, from the foot of the pass to the head, and try each
one once with its lever left alone and once after pulling it.

1. **The toll booth, first on the right (east).** A stone plate lies in its
   one-wide mouth. Stepping on it rings a bell in the booth and puts a line on
   the actionbar, and nothing else happens. Does a harmless plate first read
   as the lesson for the plates after it? The barrel behind it holds a shield;
   note whether you think to carry it into the next strongroom.
2. **The stair, on the left (west).** Three steps climb to a landing with a
   plate on it and a barrel behind. The plate fires three salvos of arrows
   from the hole over the stair, sweeping the landing and every step. Is the
   plate visible from the bottom of the stair? Can you reach the barrel
   without stepping on it, and does the volley give you time to get down the
   stair? Then pull the lever on the road wall just past the stair's mouth
   (towards the head of the pass) and step on the plate again: nothing should
   fire, and the lever should be gone from the wall.
3. **The dart gallery, on the right.** A narrow gallery turns off the road; a
   tripwire is strung across it half-way along, between two hooks, and a
   barrel waits at the far end. Low arrow loops in the road wall let you see
   down the gallery from the road. Crossing the string fires three salvos of
   arrows down the gallery from above the barrel, slow enough to walk out
   between them. Do you see the string before you walk into it, and do the
   loops show you the gallery? The lever is on the road wall just short of the
   gallery's mouth (towards the foot of the pass).
4. **The strongbox, on the left.** A room with a single chest against its back
   wall: the chest is trapped. Opening it brings the cobbled patch of roof in
   front of it down as gravel, once, onto whoever is standing there. Does the
   cobbled patch in a brick roof read as a warning? Can you still reach the
   chest over the gravel afterwards? The lever is on the road wall just past
   the room's mouth.
5. **Levers.** Each disarm lever should vanish when it is used, and its trap
   should stay safe for the whole party from then on. Note any lever that
   does not answer a click, or a trap that still fires after its lever.

Raise the toll bar with the winch lever beside it at the head of the pass,
and walk through to finish.
