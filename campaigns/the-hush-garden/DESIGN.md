# The Hush Garden — design

The design of record. Written at steps 1–3 and confirmed at the design gate (step 4); every later round is judged against it.

## 1. The delve in one paragraph

Two friends are locked in the Hush Garden at closing time, at the tower in the middle of its hedge maze. Something old sleeps under the lanes, and it wakes to footsteps. One friend runs the lanes for the far gate; the other climbs the tower and calls the way, and draws the sleeper off with thrown eggs, arrows and the garden's bells. At the gate the runner winds the bridge up, and the friend on the tower walks across the top of the maze to meet them.

(The sections below are written at steps 2 and 3.)

## 2. The map

A site plan of six places on one flat garden lawn (`site-plan.json`; the numbers are `geometry-brief.json`'s). The map's reference is three views under one style (`design/reference/`): the whole garden from high in the south-west, straight down, and eye height in a lane. They are style, never dimensions: the maze's real pattern comes from its generator at step 9 and is judged on the built map.

| place | what it is | box |
|---|---|---|
| `node/maze` (entry) | the hedge maze, 85 × 85 blocks outer wall to outer wall: 28 × 28 lanes of 3 blocks (a lane 2 wide, a wall 1), walls 4 high (three courses of stone under a hedge cap), lanes on y 65. Four quarters told apart by floor colour: rose north-west, yellow north-east, blue south-east, green south-west. The heart court in the middle holds the watchtower's foot, its ladder shaft and the bench. The sundial court is in the rose quarter, the old well in the green quarter's far corner, a bell near the middle of each quarter. | 83 × 83, open 21 courses |
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
