# The Wake — design of record

A demo level: one mechanic in the spotlight, minimum cast, ten to twenty
minutes. The mechanic is **staging** — scripted actors, a procession that
moves, cutscenes, and a single choice that redirects all of it.

## Premise

Oris Vane kept the sea wall at Sallow Reach. When the storm came he opened the
sluice: the harbour lived and the low fields drowned. He is dead now, the
burial road forks, and the village has four hands for a bier that wants six.
The party are the other two, hired that morning, and they are the only people
on the road who did not know him.

## The choice, and what it is not

At the fork stone the party decides which road the bier takes. **Both roads
end at the same grave** — the keepers' ground on the headland — so the choice
is never "where is he buried". It is *what the procession is made to walk
through on the way*.

- **The high road** is level, dry, and costs nothing. It is the road keepers
  are carried on.
- **The drowned road** is a lane sunk below the fields, standing water over the
  floor of it. Carrying him down it means the procession goes through what he
  did before anyone stands over him and says what he was.

Ceren is not asking for revenge on a corpse. He is asking for witness. That is
the whole argument, and the delve does not settle it.

## Cast

| body | who | posture |
|---|---|---|
| `npc/halda` | Halda Vane, the dead man's sister | Has already done all her crying and is now only organising. Says what she feels in the plainest word available and moves on. |
| `npc/ceren` | Ceren Aldby, a farmer whose ground is under water | Careful, unraised, never insults the dead and never concedes. He has the better case. |
| `npc/wick` | Wick, the gravedigger | Waiting at the fork with a spade because nobody has told him which hole to finish. Bark pool; no stake in it. |

Scripted puppets carry the staging: the body on its bier, two bearers, and a
mourner who follows. They are `spawn-actor` / `move-actor` bodies, not NPCs —
the procession is a moved thing, which is the point of the level.

## The route

Eight places, one area (`area/site`), no prefabs.

| place | class | what happens |
|---|---|---|
| `node/wake-house` | room | The body on its trestles. Halda hires the party; the bier is lifted. |
| `node/lych-gate` | alcove | The bier rests on the gate stone. **The eulogy sequence** — the one enclosed place on the route, which is why it is spoken here. |
| `node/coast-road` | road, 96 | The carry. Ceren steps up out of the fields and makes his case while the party is walking and cannot leave. |
| `node/fork-stone` | room | The stone with both names cut on it. **The choice.** Wick waits. |
| `node/high-road` | road, 40 | Level and easy. |
| `node/drowned-road` | road, 40, three below grade | Water over the floor of it. |
| `node/barrow-shoulder` | hall | Both roads arrive here. The bier is set down once. Halda and Ceren, two-shot. |
| `node/cliff-barrow` | hall, on the headland | The cut grave. Both endings are staged here. |

The two roads are the same length on purpose: neither is offered as the shorter
way, so the choice cannot be made on convenience. Both climb the last five to
the headland together.

## Dramaturgy

1. **The room.** No ceremony. A body under a cloth and a sister who wants it
   moved. The party is told what they are being paid for and nothing else.
2. **The gate.** The eulogy. Halda speaks it and it is about the wall, not the
   man — she never once says why the sluice was opened.
3. **The road.** Ceren catches up. The argument happens at walking pace with a
   body between them, which is the only reason it stays civil.
4. **The stone.** The party chooses. **They choose without the decisive fact**:
   nobody has yet said whose order opened the sluice.
5. **The road they chose.** On the drowned lane the water is the scene. On the
   high road, nothing happens, and the nothing is the content.
6. **The shoulder.** The bier is set down. Halda says the thing she has not
   said: she was in the tower, and she told him to open it.
7. **The grave.** He goes in. Nobody reconciles. The last beat is an act, not a
   realisation.

## Branch and ending table

| branch | flag | road walked | ending |
|---|---|---|---|
| `branch/high-road` | `flag/high-road` | the level road | `ending/laid-with-keepers` |
| `branch/low-road` | `flag/low-road` | the drowned lane | `ending/laid-in-the-field` |

Both converge at `quest/lay-him-down`, whose two objectives are gated by the
branch flags; the ending fired differs by flag. The names are what the village
calls the two burials afterwards, not two graves.

## What the walk has to settle

The blockout is derived from the plan; no picture of it exists, and none is
drawn. Standing in it is what decides:

- Does a 96-block carry read as a procession, or as a long empty road? The
  pacing line measures 214 blocks of route, about 4 minutes; the rest of the
  billed twelve is staged.
- Is the drowned lane's descent legible from the fork — can a player see what
  they are choosing before they choose it?
- Does the headland read as high enough to be the honour ground, at five above
  the shoulder and eight above the lane?
- `view/from-the-fork` and `view/from-the-barrow` are the two declared vantages
  the silhouette is judged from.
