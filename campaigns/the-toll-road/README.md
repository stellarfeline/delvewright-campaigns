# The Toll Road

*A short delve about paying attention.*

The tide road to Vesper Keep is the only dry way inland, and the keep still
collects its toll. It does not want your coin. Between the barrow shore and the
vault under the cistern there are three tollgates, and each one is a piece of
honest machinery: a plate in a stair, a slot in a shaft, a box in an alcove.
Every one of them shows you its hardware before it uses it. Nothing on this
road hides — which is the whole arrangement, and the reason nobody has ever
been able to complain afterwards.

Walk it carefully and you leave with the keep's writ and both your hands.

## Who you meet

**Ordwin the Tollwright** keeps the road. Not the fee — the *road*: true plates,
clear slots, oiled levers. He talks about the traps the way a good foreman talks
about a crew that has never once been late, and he will answer every question
you ask him, at length, for free. He would rather be understood than paid.

He does not walk his own road.

## Classes

Pick one at the start; you are kitted for it, and there is nothing to grind.

- **Roadwarden** — plate and shield. You take the arrows on the iron and keep
  walking.
- **Tidewalker** — light leathers, a lantern and two apples. You read the road
  instead of eating it.

## At a glance

|  |  |
|---|---|
| Players | 1–4 |
| Playtime | about 20 minutes |
| Mode | adventure; no grind, no base building |
| Combat | none — the road is the only thing that will hurt you |
| Languages | English, 简体中文 (`--lang zh-cn`) |

This is a **short teaching level**. It is built to be played once by somebody who
has never seen a Delvewright trap, and to leave them knowing how one is meant to
be read.

## Play it

Build the delve, then start the server:

```sh
delvec build campaigns/the-toll-road -o validation/delve-output
EULA=TRUE docker compose -f validation/compose.yaml --profile play up
```

For the Chinese build, add `--lang zh-cn` to the `delvec build` line.

Join on `localhost`. Set the difficulty from the world, not the server — the
delve seals its own rules.
