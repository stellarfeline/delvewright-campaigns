# The Tidewatch

> **Requires delve engine 0.20.0 or newer** — last verified with delvec 1.2.0 on Minecraft Java 1.21.11.

A watchtower on a black rock headland has burned every night for as long as the coast has had ships. Tonight it is dark.

## The coast

The Tidewatch is not a lighthouse for anybody in particular. It is older than the harbour it warns off, and the coast has grown so used to it that nobody down the shore has looked at it directly in years — which is why nobody has come. The tower stands over a tide-cut stair of wet black rock that drops in broken flights to a shingle landing, and a sea cave opens in the headland beside it. What the tide takes off that landing it usually brings back.

Two wardens come ashore on the landing. That is where this starts.

## Who is here

**Maren Sill** has kept the lamp for forty years and speaks about the sea the way other people speak about the weather — as a fact, not a subject. She is on the stair when you arrive, holding a jar with nothing in it, and she is not especially glad to see anyone. She will tell you what she needs. She will not tell you more than that.

She is the only other person on this coast tonight.

## Your party

Two players. One class:

**Lampwarden** — iron sword, shield, leather chest and boots, a lantern, and bread. You carry the light and the means to defend it. There is nothing to mine, nothing to farm and nothing to level: everything you need is handed to you at the start.

The finale needs both of you in different places at once. Plan for that.

## Playtime

About thirty-five minutes.

## Running it

Build and serve it in one command, from a clone of this repository with the toolchain in place:

```sh
"$DELVEWRIGHT_ENGINE/tools/playtest-server.sh" up campaigns/the-tidewatch \
    --prefabs prefabs --out "$PWD/.out/delve"
```

It prints the address to connect to. In the Minecraft Java client the marker above names: **Multiplayer → Direct Connect → `localhost:25565`**.

The published image is tagged `:latest`. If you need an exact version, take it from the release page, where the tag is machine-written.
