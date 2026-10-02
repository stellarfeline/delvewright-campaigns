# The Stargazer's Roof

The demo level for **a sky stated in a designer's words** (spec-0081): a time
names the sun or the moon, where it stands and what phase it shows, and the
engine computes the ticks, day included.

The level is a campaign, so it lives where every campaign lives:

    campaigns/stargazers-roof/

## What it is meant to show

One roofless tower top standing on the sea, an 8 × 8 roof inside a low parapet,
open to the sky. The Stargazer stands at its centre. The party arrives under
*a new moon, just risen* — `{"moon": "just-risen", "phase": "new-moon"}`, day 4.
Each sentence you choose in her dialogue cuts the sky to it, and you look up and
read the sky against the sentence:

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

## Walking it in the test world

The build's `datapack/` goes into the save's `datapacks/` as
`stargazers-roof`. A Delvewright delve pack and another delve pack in one
save share the engine's run-once guard and player state, so the steps
disable the other delve while you walk this one, and put it back after.

1. Open the world. If cheats are off: Esc → Open to LAN → Allow Commands ON
   → Start LAN World.
2. If another delve pack is enabled (`/datapack list enabled`), disable it,
   e.g. `/datapack disable "file/the-threshold"`.
3. `/function stargazers-roof:setup`
4. `/tag @s remove dw_joined`, `/scoreboard players reset @s dw.classed`,
   `/scoreboard players reset @s dw.dlg_shown`
5. Pick **Stargazer** in the class dialog (a spyglass). You are put at
   12303 64 12303, the middle of the roof.
6. To see over the parapet: `/gamemode creative`, then
   `/tp @s 12303.5 69 12301.5 -90 -5` (facing east, +X). Yaw `90` faces west;
   pitch `-90` looks straight up.
7. **Arrival.** `/time query day` → 4, `/time query daytime` → 12959. East:
   the dark new-moon disc wholly just above the horizon (+2.86°). West: the
   sun just under it (−2.86°).
8. Right-click the Stargazer and choose a sentence; "Another sentence." comes
   back to the list. Confirm each with `/time query day` and
   `/time query daytime` against the table above:
   - **A full moon, high** — look up: a full moon at the zenith.
   - **A new moon, high** — look up: the same hour, and the moon is new.
   - **The sun just set** — west: no sun disc at all (−4.29°); east: the new
     moon at +4.29°.
   - **The sun rising** — east: the sun's centre on the horizon, half a disc;
     west: the moon's centre on the horizon.
   - **A new moon, risen** — back to the arrival sky.
   - **That is all** — completes the delve.
9. Afterwards: `/datapack disable "file/stargazers-roof"`, re-enable the other
   delve, and run its `setup` if you want its spawn point back — this level's
   setup moved the world spawn to the roof.

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

Builds on the engine branch `feat/celestial-time`. Validates and builds there
(exit 0). The machine ladder on the `validation/` image has not been run.
