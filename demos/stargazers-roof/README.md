# The Stargazer's Roof

The demo level for **a sky stated in a designer's words** (spec-0081): a time
names the sun or the moon, where it stands and what phase it shows, and the
engine computes the ticks, day included.

The level is a campaign, so it lives where every campaign lives:

    campaigns/stargazers-roof/

## What it is meant to show

One roofless tower top standing on the sea: an 8 × 8 roof inside a parapet one
course of stone brick high with two courses of glass above it, so the edge is
full height and the whole horizon shows through it from anywhere on the roof.
The world is the sea (`horizon: ocean`). The roof is twenty-two blocks above
it, on a stone-brick tower with a corbelled cornice and blind slit windows,
which stands on a rock skerry, so from the roof the sun and moon rise and set
over an unbroken sea line. The tower is a `massif` volume in the site plan,
refaced in `world-edits.json`; nobody can climb down it.
The Stargazer stands at the roof's centre. The party arrives under *a new moon, just
risen* — `{"moon": "just-risen", "phase": "new-moon"}`, day 4. Each sentence
you choose in her dialogue cuts the sky to it, and you look up and read the sky
against the sentence:

| Choice | Written as | Day, daytime |
|---|---|---|
| (arrival) | `{"moon": "just-risen", "phase": "new-moon"}` | 4, 12959 |
| A full moon, high | `{"moon": "high", "phase": "full-moon"}` | 0, 18000 |
| A new moon, high | `{"moon": "high"}` (the world's phase) | 4, 18000 |
| The sun just set | `{"sun": "just-set"}` | 4, 13047 |
| The sun rising | `{"sun": "rising"}` | 4, 23218 |
| A new moon, risen | `{"moon": "just-risen"}` | 4, 12959 |

This is where the eye confirms the position table once: `just-risen` shows the
whole disc clear of the horizon and `just-set` none of it, and the phase
changes with the day count while the hour does not (the two *high* choices).
No render can show this: the pinned renderer draws no moon.

**Where it departs from its queue row.** The bell is the Stargazer's
dialogue. Three `interact` objectives on one cell are refused (`DW0878`), and
a dialogue effect cannot play a sound, so no bell is heard. The sentence the
sky was cut to is the text of her reply.

## Walking it

Served on a local server; join with Multiplayer → Direct Connect →
`localhost:25565`. You play in adventure mode, and nothing on the walk needs a
command.

1. **Arriving.** You are put at the middle of the roof, beside the Stargazer.
   Turn until you find the moon: a dark, nearly unlit disc sitting low over the
   parapet, wholly clear of the sea's horizon. That way is **east**. The
   opposite way, **west**, the sky still glows where the sun has just gone
   under.
2. **Talk to the Stargazer** (right-click her). She lists the sentences; after
   each one she says what to look at, and "Another sentence." brings the list
   back. Stand anywhere on the roof and look through the glass.
   - **A full moon, high** — look straight up: a full moon at the zenith.
   - **A new moon, high** — look straight up again: the same hour, and the moon
     overhead is now new. The phase moved; the hour did not.
   - **The sun just set** — look **west**: no sun disc at all, the whole of it
     gone below the horizon. Look **east**: the new moon a little higher than
     when you arrived.
   - **The sun rising** — look **east**: the sun's middle on the horizon, half
     a disc above the sea. Look **west**: the new moon's middle on the horizon.
   - **A new moon, risen** — back to the arrival sky; compare with step 1.
   - **That is all** — completes the delve.

## Binding lines

Every build prints, for this campaign:

```
clock: world {"moon":"just-risen","phase":"new-moon"} -> day 4 daytime 12959 (dayTime 108959); sun -2.86° W, moon +2.86° E new-moon; sky light judged 4, game 8; burns: no
clock: set-time {"moon":"high","phase":"full-moon"} -> day 0 daytime 18000; sun -90.00°, moon +90.00° full-moon; sky light judged 4, game 4; burns: no
clock: set-time {"moon":"high"} -> day 4 daytime 18000 (dayTime 114000); sun -90.00°, moon +90.00° new-moon; sky light judged 4, game 4; burns: no
clock: set-time {"sun":"just-set"} -> day 4 daytime 13047 (dayTime 109047); sun -4.29° W, moon +4.29° E new-moon; sky light judged 4, game 8; burns: no
clock: set-time {"sun":"rising"} -> day 4 daytime 23218 (dayTime 119218); sun +0.00° E, moon +0.00° W new-moon; sky light judged 4, game 9; burns: no
clock: set-time {"moon":"just-risen"} -> day 4 daytime 12959 (dayTime 108959); sun -2.86° W, moon +2.86° E new-moon; sky light judged 4, game 8; burns: no
clocks: 1 world + 5 cut(s); 6 celestial, 0 keyword; phases stated {full-moon, new-moon}; days {0, 4}
```

## The four refusals

Each is the campaign plus one edit, refused by `delvec validate` with `DW0931`:

- **A phase under the noon sun** — the full-moon choice written
  `{"sun": "high", "phase": "full-moon"}`: *states the phase `full-moon` where
  the moon stands at -90.00° — below the horizon … REMOVE `phase`*.
- **A night whose moon nobody named** — `world.time` written
  `{"moon": "just-risen"}`: *puts the moon at +2.86° … and states no `phase` …
  STATE `phase`, one of the eight the pinned game names*.
- **A sky with two bodies** — `world.time` naming the moon just risen and the
  sun setting: *names both `sun` and `moon` … NAME ONE BODY*.
- **A phase that restates the world** — the sunset choice written
  `{"sun": "just-set", "phase": "new-moon"}`: *states the phase `new-moon`,
  which is the world's … REMOVE `phase`*.

## State

Builds on the engine branch `feat/celestial-time` (exit 0). The machine ladder
on the `validation/` image is green: PackTest passes all 17 required tests
(the ocean's `boundary` brings the two `v06_boundary_*` tests),
`sealed_state` among them — `daytime` 12959, `day` 4 and
`predicate stargazers-roof:moon_new-moon` asserted on the server — and the
mineflayer critical path passes (3 steps, 2 advisory findings: no death plan
and no combat plan, because the level has neither).

The staging gate refuses it on two findings, `drill3-01` and `drill3-03`: the
level has no design record, so the checks that read one are unbound. That is
tracked separately and is not overridden here.
