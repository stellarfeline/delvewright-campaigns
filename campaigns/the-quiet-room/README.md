# The Quiet Room

> **Requires delve engine 0.36.0 or newer** — last verified with delvec 1.8.2 on Minecraft Java 1.21.11.

> *"You read it. Good. Most do not."*

A ten-minute keep that tells you nothing. There is no glowing marker over the thing to press, no line in chat when a task begins or ends, and no objective title anywhere. The keep answers what you do: read the slate and a gate lifts; pull a lever and the floor gives up its watch where you stand; walk out to the warden's empty stand and it keeps you; find the Keeper in his hall and he says one thing, and then — only once you have heard it — the other.

| | |
|---|---|
| **Players** | 1–4 |
| **Playtime** | ~10 minutes |
| **Mode** | adventure, one short fight |
| **Languages** | English |

## How to play

Join the server the host gives you, pick the one class, and look before you ask. Everything in the keep that matters is something you can read, press, pull or walk to; nothing points at it.

## For hosts

```sh
docker run --rm -p 25565:25565 -e EULA=TRUE ghcr.io/stellarfeline/delve-the-quiet-room:latest
```

The image is the whole delve: server, world, datapack and configuration. One container is one joinable keep.
