# Doune Castle: A Guided Tour

> **Requires delve engine 1.5.0 or newer** — last verified with delvec 1.5.0 on Minecraft Java 1.21.11.

> *"Mind the stair — the left side is worn through, and has been since before either of us."*

A walk through a real castle with somebody who knows it. Nine stops, one guide, no combat, no grind: about thirty-five minutes if you follow her, longer if you wander, and wandering is allowed from the first minute.

| | |
|---|---|
| **Players** | 1–4 |
| **Playtime** | ~35 minutes |
| **Mode** | adventure, no combat |
| **Languages** | English, 简体中文 (`zh-cn`) |
| **Class** | one — the Visitor: a book, a spyglass, and bread |
| **Source** | Doune Castle, Stirling — late 14th century |
| **Licence** | CC BY-SA 4.0 |

## What it is

The party arrives on the north approach with the whole exterior in front of them. Elspeth Moncrieff has guided at Doune for twenty years; she takes you through the gate passage, the courtyard, the lord's hall and the duchess's, the great hall, the kitchen, the royal apartments, and out onto the wall-walk. Talk to her at a stop and you get that room and a piece of the castle's six centuries — dates as plain numbers, opinions owned out loud. When the conversation closes she walks on and waits.

Every door is open. You can run ahead of her, go down to the cellars alone, find the pit prison under the guardroom, or stand in the oratory she has not mentioned yet.

It ends on the garrison mustering in the courtyard below you.

## The castle is a real one

Doune, in Stirling, late fourteenth century — built for Robert Stewart, Duke of Albany, who governed Scotland without ever being its king. It was chosen because its rooms survive roofed and documented, its plan is a working household rather than a picturesque ruin, and its geometry is rectilinear enough to build honestly.

The layout follows the household's own circulation: the lord over his own gate, so nobody enters unseen by him; the great hall over its cellars with the dais against the lord's door; the kitchen at the hall's far end, feeding it through two hatches; guests over the kitchen, which is the warmest wall in any castle; the garrison on the gate and the wall. Sources are in `design/research.md`.

Scale is 1.5 blocks to the metre. The fourth range was planned and never built, and the tour ends there rather than on a summing-up.

## Known limits

- From the last stop on the wall-walk, the rail at your feet hides the near half of the courtyard. The muster is staged where you can see it; anything south of the well would be invisible from up there.
- The guard forms up as seven separate arrivals that end in a line. Nobody marches in step.
- The mounted display this ending was first imagined as is not built.

## Building it

```
delvec build campaigns/doune-castle-tour -o out
```

The whole map is one grammar-built site (104 × 56 × 120, seed 1) bound as `prefab/doune-castle` under a `valley` horizon. `design/programs/build_castle.py` generates the program from one module per part — grounds, gatehouse, hall, kitchen — each describing what stands at each course of its own columns; re-run the driver to regenerate. 31 anchors.
