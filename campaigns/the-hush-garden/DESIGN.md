# The Hush Garden — design

The design of record. Written at steps 1–3 and confirmed at the design gate (step 4); every later round is judged against it.

## 1. The delve in one paragraph

Two friends are locked in the Hush Garden at closing time, at the tower in the middle of its hedge maze. Something old sleeps under the lanes, and it wakes to footsteps. One friend runs the lanes for the far gate; the other climbs the tower and calls the way, and draws the sleeper off with thrown eggs, arrows and the garden's bells. At the gate the runner winds the bridge up, and the friend on the tower walks across the top of the maze to meet them.

(The sections below are written at steps 2 and 3.)

## 2. The map

A site plan of six places on one flat garden lawn (`site-plan.json`; the numbers are `geometry-brief.json`'s). The map's reference is three views under one style (`design/reference/`): the whole garden from high in the south-west, straight down, and eye height in a lane. They are style, never dimensions: the maze's real pattern comes from its generator at step 9 and is judged on the built map.

| place | what it is | box |
|---|---|---|
| `node/maze` (entry) | the hedge maze, 85 × 85 blocks outer wall to outer wall: 28 × 28 lanes of 3 blocks (a lane 2 wide, a wall 1), walls 4 high (three courses of stone under a hedge cap), lanes on y 65. Four quarters told apart by floor colour: rose north-west, yellow north-east, blue south-east, green south-west. The heart court in the middle holds the watchtower's foot, its ladder shaft and the bench. The sundial court is in the rose quarter, the old well in the rose quarter, a bell near the middle of each quarter. | 83 × 83, open 21 courses |
| `node/lookout` | the watchtower's deck, 22 above the lanes: railed, a small copper roof, the bell lectern with one button per quarter | 5 × 5, hung over the heart |
| `node/bridge` | a plank bridge on chains from the deck to the gate tower's top, straight across the maze's east half; barred at the deck end until the gate is wound | 38 × 3, hung |
| `node/gatehouse` | the gate tower's hall on the maze's east edge: the winch, a ladder up | 7 × 9, 21 high |
| `node/gate-top` | the gate tower's roof, level with the deck, where the bridge lands | 7 × 9, hung |
| `node/meadow` (goal) | the flower meadow beyond the great gate, where the gardener waits | 20 × 41, open |

Ways: a ladder up the watchtower (maze → lookout); the bridge (lookout → bridge → gate-top), shut until the gate is wound; an arched door from the maze's east lane into the gate hall; a ladder up the gate tower (hall → top); the great gate (hall → meadow), shut until wound.

Why these numbers (from `warden-behaviour.md` and `maze-craft.md`, the engine's research record):
- The warden hears a footstep, a landing projectile or a rung bell to about 16 blocks. The maze is 85 across so that its loops can put more than 16 blocks of wall between walker and warden; a loop smaller than that is a corridor with a decoration in it.
- The warden walks a 1-wide lane as fast as a 2-wide one, so the 2-wide lanes are for two players passing and for reading from the deck, not shelter.
- The deck and the bridge stand 22 above the lanes: the warden's sniff and its ranged attack both reach 20 blocks up, so a caller on the deck is never its target.
- The maze is braided (loops, few dead ends): a dead end the warden can reach while the walker is in it is a trap with no second way out. Dead ends are kept only away from the well.

## 3. The story

**Premise.** At closing time Wren Applegate, the Hush Garden's head gardener, winds the great gate shut without seeing two friends still in the maze. They are at the heart, by the watchtower, with her note on the bench: the gate's crank handle is on the sundial in the rose quarter; wind the gate from the gate tower on the east side; walk softly, because something old sleeps under the old well just past the sundial and it wakes to footsteps.

**The two roles.** Each player picks a class at the start; either can be played alone.
- **Runner** — soft-soled boots and bread. Runs the lanes for the crank and then for the gate.
- **Caller** — a spyglass, sixteen eggs, a bow and sixteen arrows. Climbs the watchtower, watches the lanes from 22 blocks up and calls the way, draws the sleeper off with thrown eggs and arrows, and rings the garden's bells from the deck.

**The cast.** One character: Wren Applegate, in the meadow beyond the great gate. Everything before the gate is the two friends, the note, the garden and the sleeper.

**The sleeper.** A warden (`minecraft:warden`), asleep under the old well in the rose quarter, two or three turns past the sundial court and 10 to 14 blocks from the crank: within its hearing, so a runner who runs off from the sundial instead of creeping is heard at once (it turns toward the sound but is not yet hunting), while the seven deaf seconds of its emerge are the runner's grace to start sneaking. A loop out of the sundial court takes a runner beyond its hearing, and no dead end lies within 16 blocks of the well. It is not in the world at the start. When the runner takes the crank handle from the sundial, a close-up shows it digging up out of the ground at the well (about seven seconds, in which it hears nothing and cannot be hurt). Then it searches: it walks to every sound it hears within 16 blocks — a footstep that is not sneaking, a landing egg or arrow, a rung bell. When it has heard a player enough it hunts that player, at about 5 blocks a second, faster than a running player, and nothing lures it off until it loses the trail. It cannot be beaten; nothing in the level asks anyone to try.

**The two phases** (from the engine's measurements, `warden-behaviour.md` and the T11 trial in `GENERATION.md`):
1. *Searching.* The runner sneaks (silent beyond 6 blocks) and the caller steers it: one egg or arrow landing near it turns it to the spot for about ten seconds; a bell on the deck's lectern rings that quarter's bell, which turns it from up to 16 blocks away. Each bell can be rung three times, and a rung bell is quiet for twenty seconds before it can ring again, so the sleeper cannot be held forever. A thrown egg or arrow is not free: it puts the thrower on the sleeper's list a little each time, a lot when two land within five seconds, and a direct hit makes the thrower its quarry. The bells cost nothing but are few.
2. *Hunting.* Once it hunts the runner, lures are ignored. The runner breaks the chase by running a loop of the maze until more than 16 blocks of wall stand between them; the caller can only call the way.

**Monsters.** A few slimes bounce in the lanes of the yellow quarter, on the way to the gate tower: harmless enough on their own, but every hop is a sound the sleeper hears, and a runner who fights one makes more.

**The end.** At the gate tower the runner fits the crank to the winch and winds. The great gate swings open onto the meadow and, from the gate tower's top, a plank bridge on chains rises across the maze to the watchtower's deck, so the caller walks across the top of the maze and climbs down to meet the runner. Wren is waiting in the meadow. The ending reads whether the two came out together (the caller crossed the bridge) or the runner came out alone.

## 4. The lines and the evening

| line | body | acts | minutes |
|---|---|---|---|
| `quest/locked-in` (hub) | take the note from the bench at the heart; pick roles | take | 2 |
| `quest/the-crank` | find the way through the rose quarter to the sundial and take the crank handle; the sleeper digs out | reach, take | 8 |
| `quest/the-watch` (optional) | climb the watchtower's ladder and read the bell book on the deck (which button rings which bell) | reach, use | 3 |
| `quest/out` (finale) | get to the gate tower under the sleeper's search and hunt, fit the crank to the winch and wind, walk out and talk to Wren | reach, use, present, give, talk | 12 |
| | | **sum** | **25** |

`target_minutes` is 25: a small level for an evening's first half hour, longer when the sleeper catches the runner and the run restarts at the last checkpoint.

## 5. Endings

One fork, `branch-point/who-comes-out`, opening at the finale: `flag/crossed-the-bridge` is set when a player walks onto the bridge after it rises.
- `ending/together` — the caller crossed the bridge: Wren greets both friends and says she was frightened for them the whole way across.
- `ending/alone` — nobody crossed: Wren greets the runner, asks whether anyone else is inside and says the bridge is up for anyone on the tower. The runner can answer *I'll wait for them* (the conversation closes and the friend can still cross) or *Just me tonight*, which ends the delve alone.

The maze objectives (the sundial, the gate tower) carry no compass: finding the way is the runner's and the caller's job.

The sleeper is not beaten in either ending; it is still under the garden.
