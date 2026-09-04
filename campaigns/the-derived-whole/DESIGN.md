# The Derived Whole — design of record

A demo level for one mechanic: **a whole map with no authored geometry.**

The campaign carries four documents that describe the map, and not one line in
any of them describes a block. `world.json` declares no areas. `geometry-brief`
holds three numbers. `layout-graph` holds five places and five connections.
`site-plan` embeds that graph in world coordinates. The mass a body walks is
derived from those and from the metrics table, by the compiler, every build.

The question the walk answers is the one a picture cannot: **does a map you
never built read as a map?**

## The circuit

Five places, five connections, one loop. A body starts in the hub and comes
back into it through the ceiling of the world above it.

```
        node/vault ──X── node/upper-walk
             │                  ╱
             =                 ╱  (climb)
             │                ╱
         node/lip      node/long-gallery
             │                │
             v                =
             └──────► node/hub ┘
```

| # | place | class | footprint | floor | headroom | what it is |
|---|---|---|---|---|---|---|
| A | `node/hub` | `hall` | 16 × 16 | 64 | 14 | Where a body starts, and the only place the walk sees twice. |
| B | `node/long-gallery` | `room` | 16 × 16 | 64 | 8 | The far side of the first seam, and the place that pays for the climb out of it. |
| C | `node/upper-walk` | `road` | 20 × 4 | 69 | 6 | The upper circuit's spine. The keeper stands on it. |
| D | `node/vault` | `room` | 12 × 12 | 69 | 8 | Behind the bar. What is kept here is the plan the map was derived from. |
| E | `node/lip` | `corridor` | 4 × 16 | 69 | 5 | A ledge running back over the hub, ending at the hole. |

| connection | class | opening | what the walker meets |
|---|---|---|---|
| `edge/hub-to-gallery` | walk | `passage` 3 × 3 | A seam the plan cut: a doorway framed in a different block from the wall it is in. |
| `edge/gallery-climb` | stair | `arch` 2 × 3 | Five blocks of rise. Nothing says how to climb it. |
| `edge/the-bar` | barred | `door` 1 × 2 | Shut until the keeper yields. |
| `edge/vault-to-lip` | walk | `arch` 2 × 3 | Out of the vault onto the ledge. |
| `edge/the-hole` | drop | `arch` 2 × 3 | Five blocks down, back into the hub. |

## The four things a walker is meant to notice

1. **The floor says where you are.** Each place's floor is a different colour,
   cycled over the plan's own document order. Nobody chose the colours and
   nobody placed them.
2. **The seam is cut, not built.** A doorway is a hole in a one-cell wall, ringed
   in a frame block, at the cells the plan allocated and at no others.
3. **The climb's pitch was chosen, not authored.** The gallery is sixteen blocks
   deep. The rise is five. The gentle standard needs ten blocks of run and gets
   them, so the climb comes out as a ramp of half-courses. Shorten the gallery
   below ten and the same five blocks of rise come back as a steeper stair, with
   no other edit anywhere.
4. **The way home is a fall the plan declared.** Five blocks is the drop policy's
   cap, which is why the two datums are five apart and not some other number.

## The exhibit: a plan edit and a regeneration are the same act

Move one box eight blocks and rebuild. The whole map moves with it — the seam
that pierces its wall, the run of the climb into it, the anchor a quest hangs
on, the route the completability proof walks. There is no hand edit to lose,
because there was never a hand edit to make.

## The keeper

One NPC, no combat. She is a clerk who has outlived the office, and she is
guarding a copy of the plan of the place you are both standing in. She talks
about paperwork. She never explains the mechanic, and neither does the level:
the point of the walk lives in the walk.

## Dramaturgy

| act | quest | beat |
|---|---|---|
| 1 | `quest/the-way-in` | Cross the seam. Climb whatever the plan left you to climb. |
| 2 | `quest/the-keeper` | Ask the keeper. The bar lifts. Read what is behind it. |
| 3 | `quest/the-hole-home` | Walk the lip. Take the hole home. |

No branches, no endings table: the campaign declares no `branch_points`, so
there is one storyline and one ending.

## What this level does not do

No combat, no traps, no waves, no stealth, no shops, no second language. One
player, one class, one NPC. Every surface it does not use is a surface the
mechanic it teaches does not need, and a demo that taught two mechanics would
teach neither.
