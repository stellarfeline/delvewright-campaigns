# The Saltworks at Greyhithe

> **Requires delve engine 0.19.0 or newer** — last verified with delvec 1.1.0.

A cliffside salt works and the small abbey that owned it, on a headland the sea
has been taking back for a generation. One to four players, about two and a
half hours, adventure mode, all your gear provided.

![The works from the sea](media/from-the-sea.jpg)

## Where you are

Greyhithe boiled sea water for a living. The lower pans lie in the water now,
their walls broken, and the boiling house above them has not been lit in twenty
years. The abbey that owned the works stands one terrace higher again, its gate
barred from the inside.

At the end of the headland there is a light tower, and the lamp in it is burning.

Nobody on this coast knows who keeps it lit. A boat will put you on the shingle
at dusk and come back for you.

## Who is still here

**Goodwife Teague** lands you and does not follow you up. She has piloted this
coast for forty years and has never seen the lamp out.

**Hask** was the works' engineman. He has been deaf since the furnaces and he
greases the coal hoist every day, though there has been no coal to lift since
the water came.

**Pyke** is a salter's son turned wrecker, camped in the driest room left
standing. Some of what he tells you is true.

**Sister Elent** is the last of the abbey community. She keeps one fire alight
in the chapter house and she will tell you what happened here, in plain words,
including the parts about herself.

## What it is to play

One connected map, walked on foot from the shingle to the lamp — twenty-four
places, each with its own reason to exist. There is a fire to rest at, a barred
door that opens once from the far side and then stays open, a drop you cannot
climb back up, and one fight at the end that is meant to be hard.

No mining, no crafting, no farming. Everything you need is in your kit.

## The three you can be

**Salter** — a works hand. You know what every one of these buildings was for,
and you are the only one who does. Iron gear, a rake, and a pocket of furnace
splints.

**Lay Brother** — the abbey's hired hand. You carried for them without being one
of them, and you know every door in the precinct. Mail, a hatchet and a shield.

**Wrecker** — you work this coast after a storm, and you were coming here
anyway. A bow, a knife and a tarred jerkin.

Every kit carries a brine flask. It refills when you rest.

## Playing it

Build the delve and start a server, then join at `localhost:25565` with the
Minecraft Java client the release page names:

```sh
tools/playtest-server.sh up campaigns/greyhithe-saltworks --prefabs prefabs \
    --out "$PWD/.out/delve"
```

Or run the published image:

```sh
docker run --rm -p 25565:25565 -e EULA=TRUE \
    ghcr.io/stellarfeline/delve-greyhithe-saltworks:latest
```

`:latest` is what this edition describes. For an exact version, take the tag
from the release page.
