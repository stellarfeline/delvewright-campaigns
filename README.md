# Delvewright Campaigns

**Delves** are self-contained Minecraft adventure maps: a story, a set of
classes with the gear already in your hands, and two or three hours of dungeon
for one to four players. No mining, no grinding, no building a base — you arrive
equipped and you leave when the story is done.

This repository holds the campaigns themselves. Each finished one is published
as a [**Release**](https://github.com/stellarfeline/delvewright-campaigns/releases),
which is a single server image: one command and your friends have somewhere to
join.

Want to write one instead of play one? See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Play

You need **Minecraft: Java Edition 1.21.11** and someone hosting the delve (the
[Host](#host) section below — it takes one command).

Install a launcher if you do not have one:

| | Official launcher | Prism Launcher (open source) |
| --- | --- | --- |
| Windows | [Download](https://launcher.mojang.com/download/MinecraftInstaller.msi) | [Download](https://prismlauncher.org/download/windows/) |
| macOS | [Download](https://launcher.mojang.com/download/Minecraft.dmg) | [Download](https://prismlauncher.org/download/macos/) |
| Linux | [Download](https://launcher.mojang.com/download/Minecraft.tar.gz) | [Download](https://prismlauncher.org/download/linux/) |

The official links are the ones listed on
[minecraft.net/download](https://www.minecraft.net/en-us/download). A Minecraft
account is required — released delves run in online mode.

Then:

1. Start Minecraft 1.21.11.
2. **Multiplayer → Add Server**, address `your-host-address:25565`.
3. Join. Accept the resource pack when the game asks — it carries the
   characters' faces and the artwork you will see in the delve. Nothing to
   install by hand.
4. Pick a class at the start. Your gear comes with it.

Everyone joining plays the same story together; there is nothing to install per
player beyond the launcher.

## Host

You need [Docker](https://docs.docker.com/get-started/get-docker/) on a machine
you own — a desktop, a home server, a Raspberry Pi. Images are built for both
Intel/AMD and ARM, so a Pi works.

Pick a campaign and a version from the
[Releases page](https://github.com/stellarfeline/delvewright-campaigns/releases),
then:

```sh
docker run -d --name delve -p 25565:25565 -v delve-data:/data \
  -e EULA=TRUE \
  ghcr.io/stellarfeline/delve-<campaign>:v<version>
```

- `-e EULA=TRUE` is you accepting [Mojang's EULA](https://aka.ms/MinecraftEULA).
  The delve ships no Minecraft server software; the container downloads the
  official server on first start, which is why the acceptance has to be yours.
- First start takes a couple of minutes while the world is built. After that,
  join at `localhost:25565` from the same machine.
- **Playing with friends elsewhere?** Forward TCP port `25565` from your router
  to the hosting machine and give them your public address. Everything else —
  including the resource pack — the delve serves by itself.
- Stop and start it again with `docker stop delve` / `docker start delve`. Your
  party's progress lives in the `delve-data` volume.

## Reset for a fresh party

A delve is replayable: wipe the world and it is new again.

```sh
docker rm -f delve && docker volume rm delve-data
```

Then run the same `docker run` line as before. Nothing else needs cleaning up —
the story, the gear and the map are rebuilt identically every time.

## What you may do

Short version: **play it, host it, record it, remix it — keep it free for the
next person.**

| What | Licence |
| --- | --- |
| The campaigns in this repository, and the delves released from them | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) — see [`LICENSE`](LICENSE) |
| The building-block pieces in `prefabs/` | Mostly original to this project (GPL-3.0-or-later); a few by other creators under Apache-2.0, MIT or LGPL-3.0-only. Every piece names its source and licence in [`prefabs/LICENSE-ASSETS.md`](prefabs/LICENSE-ASSETS.md) |
| The software that builds delves | [GPL-3.0-or-later](https://www.gnu.org/licenses/gpl-3.0.html), in a separate repository |

So you may share a delve, stream or record it, change it, and build your own
campaign on top of one — as long as you credit the original and release your
version under the same CC BY-SA 4.0 terms.

**Minecraft is not part of this.** No Minecraft code, assets or server software
is included or redistributed here; a delve is a data pack plus artwork that runs
on the official server you download yourself. Delvewright is not affiliated with
Mojang or Microsoft, and hosting a Minecraft server is governed by
[Mojang's EULA](https://aka.ms/MinecraftEULA) and
[usage guidelines](https://www.minecraft.net/en-us/usage-guidelines).
