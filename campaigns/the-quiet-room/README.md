# The Quiet Room

> **Requires delve engine 0.36.0 or newer** — last verified with delvec 1.8.2 on Minecraft Java 1.21.11.

> *"I am the Keeper. This is the Quiet Keep. Soldiers held it once."*

A ten-minute keep that tells you almost nothing. There is no glowing marker over the thing to pull, no line in chat when a task begins or ends, and no objective title but one. The keep answers what you do: pull the lever beside the closed gate and the gate lifts; ring the bell in the side room and the floor gives up its dead around you; pass through the gatehouse and it keeps you; find the Keeper in his hall and he tells you what the keep was keeping, and then — only once you have heard it — why the bell hangs there.

| | |
|---|---|
| **Players** | 1–4 |
| **Playtime** | ~10 minutes |
| **Mode** | adventure, one short fight |
| **Languages** | English |

## How to play

Join the server the host gives you, pick the one class, and look before you ask. Everything in the keep that matters is something you can see and use — a lever, a bell, a door, a man — and nothing points at it.

## For hosts

```sh
docker run --rm -p 25565:25565 -e EULA=TRUE ghcr.io/stellarfeline/delve-the-quiet-room:latest
```

The image is the whole delve: server, world, datapack and configuration. One container is one joinable keep.
