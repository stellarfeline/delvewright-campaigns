# The Tide Mill

> **Requires delve engine 0.41.0 or newer** — last verified with delvec 1.13.0 on Minecraft Java 1.21.11.

The tide mill at Saltmarsh Reach has had no miller for years, but its wheel
still turns on the ebb, and the wheel still works the three paddle gates in
the dry race below it. The only way up to the mill yard from the sea wall is
along that race, through the paddles, each one quicker than the last.

A demo level of about ten minutes, for one to four players. No combat.

## Classes

- **Porter** — you carry sacks up from the boats to the mill. Boots for the
  wet stones, and bread for the climb.

## Playing it

Start the server, then in the Minecraft Java client at the version the marker
above names: Multiplayer → Direct Connect → `localhost:25565`. Accept the
resource pack when the server offers it.

---

## For the owner: what to look for

This level is where timed gates (spec-0016 §4) are looked at in the game. The
race is one straight walled walk, and three paddle gates cross it; each lifts
and drops on its own clock, and a body under a paddle when it drops is killed.
The machine has proved that no paddle can be got round (the walk is closed on
both sides, and each paddle is the only way between one pound and the next),
that every paddle is crossed on the route, that each one leaves a fair share
of its cycle in which a walker who sets off can still make it through — 60%,
43% and 23% for the first, second and third — that each pound has ground at
least five blocks back from the next paddle where you can stand and watch it,
and, in PackTest, that every paddle lifts and drops on its clock and that its
drop singles out only a body standing under it (PackTest's stand-in players
cannot be killed, so the death itself is not machine-walked). The bot walked
the race through all three paddles to the yard, waiting at each for its
window; it never stood under one as it dropped. What
the machine cannot say is whether a player **reads** the rhythm before
committing, and whether the tightening feels like a lesson rather than a coin
toss.

1. **The first paddle, ahead of you as you arrive.** A plank board three wide
   and three high, under a dark beam. It stays up for four seconds and down
   for two. Do you stop and watch it before you go, or walk straight into it?
   Is it clear from the tail pound that this board moves?
2. **What happens when you mistime it.** Stand under a paddle as it drops, at
   least once. You should die at once, and come back at the last pound you
   reached (the first time, at the foot of the race). Does the death read as
   the paddle's doing, and is where you come back fair?
3. **The second paddle.** Up for two and a half seconds, down for two and a
   half. Does the shorter window read as the next step up, given what the
   first paddle taught?
4. **The third paddle.** Up for a second and a half, down for three and a
   half. It is the tightest the engine allows by a small margin. Is it still a
   read you can make by watching, or does it feel like luck?
5. **The pounds between.** Each is eight blocks long, enough to stand back
   five from the next paddle. Is that enough room to watch a full cycle
   without feeling rushed?
6. **As a party.** With more than one player, try going through together and
   one at a time. Note anything that only goes wrong with several bodies
   under one board.

The head of the race opens onto the mill yard; walking into it ends the level.
