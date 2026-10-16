# Two Keys

> **Requires delve engine 0.41.0 or newer** — last verified with delvec 1.13.0 on Minecraft Java 1.21.11.

The Staple Hall at Marrowby keeps its charter in a strongroom with two locks.
By the guild's oldest rule the Warden's key hangs in the counting room and the
Clerk's key lies in the archive, and the steward who keeps the door may hold
neither. The new masters are sworn in at dawn, and the charter has to be
brought out tonight.

A demo level of about ten minutes, made for two players and playable by one.
No combat.

## Who you will meet

- **Hesketh Marr** has kept the strongroom door of the Staple Hall for
  twenty-two years, and has never once held its key.

## Classes

- **Journeyman** — your own lantern and your supper. You were sent up to the
  hall tonight to help the steward.

## Playing it

Start the server, then in the Minecraft Java client at the version the marker
above names: Multiplayer → Direct Connect → `localhost:25565`. Accept the
resource pack when the server offers it. Bring a second player if you can.

---

## For the owner: what to look for

This level is where party-shared progression (spec-0018) is looked at in the
game: the party's progress is one fact, two players can each do one half of a
job in two rooms, a quest prop goes to the one player who took it, and one
player alone can still finish. The machine has proved, on a server, that the
strongroom does not open after one lock and does open after both when two
different players turn them (the two-player PackTest for the join), and the
bot walked the whole level alone, holding each key at its own lock. What the
machine cannot say is how the division feels to two people, and it has not
watched a key land in one inventory and not the other: the bot plays alone.
Play it once with two players, one wing each, and once alone.

1. **Each of you takes one wing.** After Hesketh has spoken, one player goes
   through the east door to the counting room, the other through the west door
   to the archive. Each wing holds one key. Does the hall make it plain, without
   Hesketh saying it twice, that the job splits in two?
2. **A key goes to the one who took it.** When one player takes a key, look in
   the other player's inventory: it should hold no key. Only the player who
   clicked receives it.
3. **A lock wants its own key, held.** Click a lock with an empty hand, with
   the key in your inventory but not in your hand, and with the other wing's
   key in your hand. Each should give you one line saying the key is not in
   your hand, and the lock should not turn. Held in the main hand, the right
   key turns it.
4. **One lock is not enough.** After the first lock turns, the strongroom door
   stays barred and Hesketh still has nothing to offer about opening it. Only
   once both locks are turned does he offer to draw the bolts.
5. **The party moves together.** When one player turns a lock, both players
   should see the same journal lines. Whoever did not turn the first lock can
   be the one who tells Hesketh both are turned, and the door opens for both.
6. **A key can change hands.** Drop a key and let the other player pick it up
   and turn the lock with it.
7. **One player alone can finish.** Play it again on your own: fetch both
   keys, turn both locks, and bring the charter out.

Bring the charter out to Hesketh to finish.
