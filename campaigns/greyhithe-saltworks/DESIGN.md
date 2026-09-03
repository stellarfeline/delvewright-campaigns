# The Saltworks at Greyhithe — design of record

A site-plan delve for 1–4 players, target 150 minutes, twenty-four places on
one connected map. Adventure mode, three classes, pre-provided gear.

## The place

A headland on a cold coast. Two things stand on it and one hand built both: a
salt works that boiled sea water for a living, and the small abbey that owned
the works and took its profit. The works is one storey above the highest tide;
the precinct is one storey above the works; the headland runs east from the
precinct and ends in a light tower.

Three rules hold the whole site together and every later decision is judged
against them:

1. **One masonry.** Grey limestone in long thin courses, iron-stained where the
   sea reaches it, dressed square at every jamb and quoin. No second material
   anywhere that carries a wall.
2. **One way of letting light in.** Tall narrow round-headed openings, high in
   the wall, in a repeated rhythm. The boiling house clerestory, the salt
   store's high windows, the cloister arcade and the church clerestory are the
   same opening at four scales.
3. **One silhouette from the sea.** Low at the water, rising in two steps,
   ending in the light. `view/from-the-sea` in the site plan is where that is
   judged.

The identity that carries rule 3 into geometry: the boiling house and the
abbey church have **the same storey height, fourteen blocks**
(`fact/boiling-house-height`, `fact/church-height`). It is why the two read as
one builder from the water.

## The story

The sea took the lower pans a generation ago and the works died with them. The
community was sent away in one night by its prior, who then stayed. The light
on the headland has burned every night since and nobody on the coast knows who
keeps it.

Warden Aumery keeps it. She held the abbey's sea office; the pans were being
cut deeper into the cliff every year to reach stronger brine, and she opened
the sea sluice herself. The headland is still standing because of it. The
delve is walked from the newest ruin to the oldest cause: the party arrives
after everything has already happened, and every place they cross tells them a
piece of it in reverse.

Nobody in the delve states its point, and the ending does not explain itself.

## The places, in the order they are walked

| # | place | class | what it is for |
|---|---|---|---|
| 1 | tide landing | hall, open | put ashore; the light is visible from here, once |
| 2 | drowned pans | expanse, open | the first cost: crossing what the sea took |
| 3 | pan house | room | first shelter; the tide ledger |
| 4 | wreck stair | road | the climb off the pans |
| 5 | brine gallery | corridor | the works' throat |
| 6 | boiling house | hall | the building the delve is named after |
| 7 | furnace walk | corridor | the black side of the same room |
| 8 | coal yard | hall, open | where the works met the world |
| 9 | hoist tower | room | Hask, and the only vertical interior |
| 10 | salt store | hall | Pyke's camp; the driest room |
| 11 | cooperage | room | the hoop iron that lifts a bar |
| 12 | works yard | hall, open | the hinge: everything opens onto it |
| 13 | abbey gate | room | the first held door |
| 14 | cloister garth | hall, open | the precinct, entered |
| 15 | cloister walk | corridor | rule 2, repeated the length of it |
| 16 | chapter house | room | **the bonfire**; Sister Elent |
| 17 | refectory | hall | the middle revelation: they were sent |
| 18 | abbey church | hall | the tallest thing before the light |
| 19 | undercroft | room | the sea office's ledger |
| 20 | prior's lodging | room | the prior stayed, and is still there |
| 21 | night stair | corridor | the last place inside the walls |
| 22 | headland path | road | no cover; the whole site reads from here |
| 23 | light court | arena | **the boss** |
| 24 | lantern room | alcove | the goal |

## Souls-adjacent structure

- **Bonfire** — one, at the chapter house (16), reached at the end of act 2's
  first quest. Every class kit carries a flask.
- **Shortcut** — `edge/boiling-house-to-works-yard`: a barred door in the
  boiling house's east wall, openable **only from the works yard side**. It
  closes the loop 6 → 7 → 8 → 9 → 10 → 11 → 12 → 6, so the whole works becomes
  one circuit once it is lifted. Pushed on from inside the boiling house it
  answers and does not open.
- **Point of no return** — `edge/night-stair-to-headland-path`: a four-block
  drop off the head of the night stair onto the headland. It falls one way and
  there is no way back up. Everything past it is act 3.
- **Boss** — Warden Aumery, in the light court (23), staged and unleashed.

## Acts

**Act 1 — the works (1–9).** Nobody is here who can explain anything. Hask is
deaf and talks about the hoist.

**Act 2 — the precinct (10–20).** Every place hands over one piece of the past.
Pyke lies a little; Elent does not; Ivo counts. The refectory says the
community was sent away. The undercroft says the sluice was opened on purpose.
The prior's room says who opened it.

**Act 3 — the light (21–24).** One walk out, one fight, one conversation.

## Branch and endings

The fork opens in the prior's lodging, on what leaves the room.

| branch | set by | ending | what it is |
|---|---|---|---|
| `branch/ledger-kept` | `flag/ledger-kept` | `ending/the-relief` | the sea office's record leaves with the party; Aumery is relieved of a watch she never asked for and goes down to the boat |
| `branch/ledger-burned` | `flag/ledger-burned` | `ending/the-watch` | the record burns in the chapter-house fire; nothing is proved, and the light is still burning when the boat comes back |

The two are exclusive and neither is the right one.

## Dramaturgy beats

1. **The lamp, seen once, from the beach** — declared as `edge/tide-landing-to-light-court`,
   a `vision` edge with a sightline, so the destination is legible from the
   first frame and never again until act 3.
2. **The clerestory** — the boiling house is the first interior with height in
   it, and the church repeats it exactly. The player is taught rule 2 in the
   works and shown it again in the abbey.
3. **The loop shuts** — the shortcut lifts from the works yard, and the works
   stops being a corridor and becomes a place.
4. **The table still laid** — the refectory is the beat that turns the delve
   from a ruin crawl into a story about a decision.
5. **The chair is occupied** — the prior's lodging, and the only body in the
   delve that is not a fight.
6. **The drop** — the party takes it because there is no other way, and the
   abbey is behind them for good.

## What is deliberately absent

No grind, no mining, no resource loop, no filler corridor. Every one of the
twenty-four places carries exactly one beat of the mission and nothing is a
place you cross to reach another place — the two ways that exist
(`wreck-stair`, `headland-path`) each carry their own beat.
