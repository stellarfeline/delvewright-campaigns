# The Derived Whole

> **Requires delve engine 0.19.0 or newer** — last verified with delvec 1.1.0 on Minecraft Java 1.21.11.

> *"Every wall you have walked past is in it, and not one of them is in it as a wall."*

A short single-player circuit through five rooms nobody laid a block of. You start on a coloured floor in a hall, and you come back to it through a hole in the wall above your head.

![The hall you start in, and come back to](media/hub.jpg)

| | |
|---|---|
| **Players** | 1 |
| **Playtime** | a few minutes to walk; longer if you stop and look, which is the point |
| **Combat** | none |
| **Languages** | English |
| **Licence** | CC BY-SA 4.0 |

## The place

There was a survey once. Somebody measured this ground, wrote down how far it was across and how high things stood, and filed the paper. Then the office closed.

What is left is the ground the survey describes: a hall with one door, a long gallery, a run of steps out of it, a walk along the top, a vault, and a ledge that runs back over where you began. Each floor is a different colour, and the colour is the only thing that tells you which room you are in. The doorways are framed in a darker stone than the walls they pierce, so you can find a way out from across a room.

Nothing in it was built for you. It is simply what those numbers came to.

## Who you will meet

**The Keeper** — a clerk who outlived the office. She stands on the upper walk beside a barred door with the survey behind it, and she has been standing there long enough to have stopped expecting anyone. She speaks flatly and briefly, says the difficult thing once and does not say it again, and will tell you outright what she is afraid of if you ask her who she is.

## Your class

**Surveyor** — a lamp, a blank map and something to eat. You walk, you look, and you carry the light. There is nothing here to fight and nothing here to dig.

## Playing it

Build and serve it from a checkout of the campaigns repository, with the engine built beside it:

```sh
delvec --prefabs prefabs build campaigns/the-derived-whole -o .out/delve
```

Or host the published image and connect on `localhost:25565`:

```sh
docker run --rm -p 25565:25565 -e EULA=TRUE \
    ghcr.io/stellarfeline/delve-the-derived-whole:latest
```

`:latest` is what this book describes. If you want an exact edition, take the tag from the release page, where it is written by the build rather than by hand.
