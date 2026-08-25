# The Drowned Bell — how this place is lit

Principles, not placements. This document says what light *means* on Halgrave and which sources
belong to which kind of space, so that a round building any geometry can light it without
inventing a scheme. It is deliberately not tied to any zone program.

The craft rules and the engine's mechanical constraints are `docs/reference/interior-lighting.md`
in the engine repository. This document is the campaign half: what the fiction motivates.

Every statement is marked **[record]** — transcribed from this campaign's own design documents,
which outrank anything a later round invents — or **[authored]** — reasoned here from the record
plus the engine's measured behaviour.

## 1. The fact that governs everything

**It is night for the whole delve.** `world.json` declares `"time": "night"`, `"weather":
"clear"`, and **no `set-time` or `set-weather` effect exists anywhere in the campaign** — the
clock never moves. The engine gives a clear night an effective sky of **4** against a darkness
threshold of **3**, and light falls one level per step, so **sky light reaches exactly two cells
deep**: a cell open to the sky, and its immediate neighbour. Everything else on this rock is dark
unless someone lit it. **[record for the declaration, authored for the consequence]**

That is not a limitation to work around. It is the campaign's premise made mechanical: a priory
that has been empty for fifty-one years is dark because nobody is left to light it, and the few
lights that exist are all somebody's deliberate act.

### The record contradicts this in three places, and a future round must resolve it

`beats.md` describes daylight that the world declaration does not allow. **[record]**

| beat | what it says | status |
|---|---|---|
| 0.5 | Emeric on the shelf "with a shore-lamp lit **in full daylight**" | contradicts `"time": "night"` |
| 5.1 | "dust standing in the light… the **shafts of light** through the slit windows" | at sky 4 there is no shaft |
| 6.2 | "The **daylight shaft** falls through a collapse in the vault. It is the zone's only landmark and every route is described from it" | contradicts `"time": "night"` |

The third is load-bearing, because a 初见杀 depends on it: K5's tell is that "the shaft's
reflection lies flat on ankle-deep water and goes black over the channel", and `encounters.md`
adds "water depth is readable off the light, and this zone is read by its one lamp".

**The mechanic survives; only the word "daylight" does not. [authored]** The tell needs *a light
above the water*, not the sun — a deeper channel puts its floor further from any overhead source,
so the reflection dies over it exactly as designed. Resolve it by making the shaft a real
overhead emitter at the collapse (moonlight through the hole reads as a dim column at sky 4; a
placed source reads as a shaft), never by moving the campaign to day, which would delete the
premise. Whoever resolves this should correct `beats.md` rather than leave two documents
disagreeing.

## 2. The one carried light, and what it means

**Emeric Tallow, the Lampman, is this delve's key light, and he walks.** **[record]**

- He "has lit the shore lamps every night" for fifty-one years (`cast.md`).
- Beat 0.5: he is on the last dry shelf with a shore-lamp lit.
- Beat 2.7: "Emeric moves up to the gate passage once S1 is open and stays there… **The lamp goes
  with him.**" — the passage is "the first shelter in the delve".
- Beat 4.7: "He sets the lamp on the chapel step. This is where his confession becomes available."
- `cast.md`: *"I'll come this far. Not the tower."*

**So the lamp is a boundary marker, not illumination. [authored]** It marks the furthest point a
living person will go, and it moves that boundary upward three times as the player opens
shortcuts. Everything above the chapel step is unlit because **nobody tends it** — which is the
motivated reason the tower is dark, and it is better than any atmospheric justification a later
round could invent.

Two consequences a build must honour:

- **The lamp is a prop that moves with an NPC**, so it is not part of any room's static lighting.
  A room Emeric is standing in must read correctly *without* him.
- His lamp is the campaign's only warm domestic light. `cast.md` has him put "the lamp out for the
  first time in fifty-one years" and, elsewhere, relight it. **A light that can go out is worth
  more than ten that cannot** — reserve that gesture for him.

The other carried light is the player's: the **Mourner** class starts with "a staff and a lantern"
(`quests.md`). One of four classes therefore experiences this delve differently. **[record]** A
lighting design must not assume it, and must not be wrecked by it.

## 3. What light means on this rock

The vocabulary below is authored from the fiction; the fictional facts under each are transcribed.

| light | means | fictional warrant **[record]** |
|---|---|---|
| **a tended flame** | someone living is here, or was until recently | Emeric's shore-lamp, lit nightly for 51 years |
| **a cold, laid, unlit fixture** | the institution stopped, mid-order | beat 5.2: the great hearth is "cold, laid, and never lit — kindling under the andirons, fifty-one years old. Ancel's household has been waiting for an order to light it" |
| **a lit run leading down** | the building still works, and it is showing you out | beat 5.8: "the sconces along the right wall, lit, leading down" |
| **one source in a large dark room** | orientation; the room is read *from* it | beat 6.1–6.2: the cistern is "lit by one hole… the zone's only landmark and every route is described from it" |
| **no light at all** | the climb the dead are also making | beat 7.4: "The climb up the tower passes the drowned going the same way **in the dark**"; `encounters.md`: the stairhead arena is "tight, dark, one exit up and one down" |

**The single most useful thing in this table is the third row.** A lit run of sconces is already
*path highlighting* in the level-design sense, and it is already in the record — it does not need
to be invented, only built.

**And the second row is the campaign's best lighting idea. [authored]** A fixture that is present,
complete and deliberately dark says more than a lit one: the hearth is laid, the kindling is
there, and no order came. Build unlit fixtures — cold hearths, empty sconces, lanterns with no
flame, candle stubs burnt out — as *decoration in their own right*. They cost no light budget and
they carry the theme the story states plainly: "An institution's worst act is a memo."

## 4. Which source belongs where

Authored, from §3 plus the emitter mechanics in `docs/reference/interior-lighting.md`.

| space | source | why |
|---|---|---|
| **the flat, the shore** | standing lantern on a shelf or stake head | Emeric's own; the tide-stake line is a lethal boundary and is "marking the line" (`cast.md`) |
| **a sheltered passage a person now occupies** | standing lantern set down on the floor beside a wall, or on a ledge | it is a lamp somebody carried in and put down |
| **a stair the household still used** | wall-mounted sconce run, one per landing or half-flight | beat 5.8; a run reads as a route |
| **a hall the household kept** | hearth (unlit) plus sparse wall sconces | the hall is "intact… the first place in the delve that is not a ruin, and that is worse" |
| **a vaulted cistern** | one overhead source at the collapse, nothing else | the room is read from its one landmark; a second source destroys the K5 tell |
| **the tower interior** | nothing tended — only what the tower itself gives | nobody has been up it in fifty-one years |
| **the belfry** | the bell and the sky; light the *frame*, not the room | Mercy is the landmark and the silhouette carries it |

**The soul variants are this campaign's cold light. [authored]** Soul lantern, soul torch and soul
campfire burn cyan-white at emission 10 against the orange 15 of ordinary flame, so *cooler* and
*dimmer* are the same decision. That maps onto the fiction without being told to: warm light is
where the living are (Emeric, the hall), cold light is where the drowned are. Use it sparingly and
consistently, or it stops meaning anything — the code is learned within a delve, not innate.

## 5. How dark the dark rooms actually are

The record says "dark" in three places and the engine refuses light below 3. **These do not
conflict, and the resolution is the craft rule about contrast. [authored]**

Contrast is what the eye reads, not absolute brightness. A room whose lit pool sits at 12–15 and
whose far corners fall to 3 reads as *darker* than a room flat at 7 — and only the first passes
the gate. So:

- **A "dark" room is a high-ratio room, not an unlit one.** Put a real source in it, place it so
  most of the floor falls away toward 3, and let the corners be the dark the record asked for.
- **Never light a room evenly.** A flat room is the thing both the gate's authors and the craft
  reject; it is also what an algorithmic relight pass produces, which is why this campaign does
  not use one.
- **The stairhead arena** wants the strongest ratio in the delve: one source, low, at the landing's
  edge, so the fight happens between a lit floor and a black ceiling.

## 6. Refusals

These are decisions already taken for this campaign. A round that finds them inconvenient should
report that, not work around them.

- **No `world.areas[].lighting` declaration.** That is the post-hoc relight pass; light on Halgrave
  is placed while the room is designed.
- **No change to `world.time` or `world.weather`.** One night of two ebbs is the premise.
- **No `mitigation: "night-vision"`.** The point is that the player is walking in the dark.
- **Nothing paved.** No floor, wall or ceiling is tiled with a glowing block to make a number come
  out. Emitters are things a person hung, set down or lit, in places where someone would have.
- **No candle used as a light source.** The engine models candles at emission **0** (they are
  absent from `emission()` in `crates/compiler/src/light.rs`, which falls through to 0), so a room
  lit by candles measures dark and refuses. Candles remain available as *unlit* decoration, which
  §3 argues is worth more here anyway.
