# Vesperhold

> **Requires delve engine 0.34.0 or newer** — last verified with delvec 1.6.0 on Minecraft Java 1.21.11.

> *"Friends of the watch. Ser Halvard Dray, sworn to the king's door. I cannot recall which door."*

A souls-like castle delve for a small company of hired blades — a Gothic hold on a crag in the rain, a cracked bell that still hums, a court that keeps its watch without remembering why, and five fires between the causeway and the throne.

| | |
|---|---|
| **Players** | 1–4 |
| **Playtime** | ~60 minutes |
| **Mode** | adventure, combat |
| **Languages** | English, 简体中文 (`zh-cn`) |
| **Classes** | four — Sellsword, Wall-Breaker, Rampart Archer, Ash Pilgrim |
| **Licence** | CC BY-SA 4.0 |

## The story so far

Ten years ago the great bell of Vesperhold rang for the last time. The gates stayed shut. The guards kept their rounds, and the king kept his throne, and none of them can say any longer what they are keeping.

At the foot of the causeway, beside a wayside shrine, a woman keeps a fire. She has posted a notice for hired blades, and she is plain about the terms: the hold does not open for anyone, so you will have to open it. She calls the castle "the hold" and the bell "her", she answers most questions with a task, and she says "I don't know" when she doesn't.

You answered the notice. It is dusk, it is raining, and the castle is on the crag above you with every gate shut.

## Who you will meet

**Tamsin Hesk** — keeper of the last fire outside the castle. Practical, generous with fire and bread, sparing with answers. She once carried the warden's lantern up there. That, she says, is all you need to know.

**Ser Halvard Dray** — an old knight sworn to the king's door, who can no longer remember which door, and so chooses one every morning and stands at it. Courteous, slow, glad of anyone who talks back, and honest about what he is afraid of. He will ask you for news of his king. What you tell him matters.

**Brother Pellam** — pilgrim, peddler, and possibly a monk; he is no longer sure himself. He sells the belongings of the dead back to the living, for tallow only, with a saying for every sale that nobody has heard before. His stories change. His prices do not.

**The court** — a porter at the gate, guards on their rounds, a king on his throne. They are all still at their posts, and none of them can tell you why.

And the castle itself remembers. Where a piece of the broken bell lies, for the length of an echo the rain stops, the sky turns to the clear noon of that last morning, and the people who stood in the room then stand in it again, saying what they said. Then the rain comes back, and they are gone.

## What kind of delve this is

A souls-like, in adventure mode. Here is what that means in play.

**Fires.** Five of them, from the causeway to the throne. At a fire you can *rest*: you are healed, fed and mended, your Vigil Draughts are refilled, and this is where you come back if you fall — but everything ordinary you have killed since comes back too. Or you can *only warm up*: the fire becomes your return point and nothing else changes.

**Dying.** You wake at your last fire. Your tallow — the castle's only coin — stays on the ground where you fell. Walk back and pick it up. Die again before you reach it, and it is gone. Tallow comes from putting down the castle's rank and file, each kill paying the player who made it, so a lost purse can be earned back.

**Walking back.** The walk from a fire to the next hard fight is short, and doors you open from the far side stay open. The castle folds back on itself as you learn it.

**Off the road.** Every part of the castle has somewhere you do not have to go: a guard room, a bastion, a yard behind the chapel, a garden behind a gate. Some hold a chest. Some hold a fight you can walk past — and a few of those are elites who drop the weapon or armour they fought you with. Nothing on the road needs any of them. There are books to be had, and an anvil to put them on.

**Trust your eyes, then look again.** Not every wall is a wall, and not every chest is a chest. The castle gives a hint before it plays a trick.

**Pack nothing.** Pick one of four classes at the start and you are given everything that class carries. There is no mining, no crafting and no levelling.

**Your word counts.** Twice the castle asks the company to decide something. Both answers are real: what you say changes what you find further in and how the story ends. There are four endings. None of them is labelled good.

## Play it

One command and the castle is up — then Multiplayer → Direct Connect to `localhost:25565`:

```sh
docker run -d --name delve -p 25565:25565 -v delve-data:/data \
  -e EULA=TRUE ghcr.io/stellarfeline/delve-vesperhold:latest
```

That is the current delve. To hold a delve at one exact version — the same world, the same words, forever — take the `:vX.Y.Z` tag from a release page instead; every release names its own. Your client will offer a resource pack when you join (character skins); accept it. The release page for each version carries the full changelog. To start the story over, `docker rm -f delve && docker volume rm delve-data`, then run the same command again.

About an hour is a party's first run: the main line, and a look around as it goes.

## Known limits

- Nobody swims in Vesperhold. The grey well under the castle kills whoever goes into it, and the curb around it is there to keep you out.
- The anvils wear out as anvils do, and nothing in the castle mends them. Expect a handful of uses from each.

---

*The design of this campaign and the decisions behind it are recorded in `DESIGN.md` and `GENERATION.md` — those files discuss the plot and every ending freely and are not spoiler-safe.*
