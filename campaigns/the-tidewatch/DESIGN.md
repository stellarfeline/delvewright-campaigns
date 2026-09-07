# The Tidewatch — design of record

Two scenes, two players, one class, one quest chain, one NPC, no branching. Thirty-five minutes.

## Premise

The Tidewatch has burned every night for as long as the coast has had ships. Tonight it is dark. Maren Sill, who has kept it for forty years, is on the tide stair below it with an empty oil jar and no way back up. Two wardens land on the stair, find her, recover what she needs, and climb the tower to put the light back in the window.

## Placement

`areas[]`, two areas, 256 blocks apart across void, with a one-way crossing emitted on the objective that carries the party from the shore into the tower.

| area | pool | pieces | what it is |
|---|---|---|---|
| `area/shore` | `pool/cave-shore` | 3–4 | the tide-cut stair and the rocks under it: where the party lands and where Maren is stranded |
| `area/tower` | `pool/vertical-keep` | 4–5 | the Tidewatch itself: entry hall, the stair, the lamp room at the top |

The first beat plays in `area/shore`, which is the spawn area, so the crossing has a completed objective to ride on. `area/tower` binds a pool whose `entry`-role member is `keep-spawn-hall`, which declares an `entry` anchor — the second condition a crossing needs.

**Anchors are taken only from each pool's `entry`-role member**, because that is the only member the assembly is guaranteed to seat: `spawn` and `anchor/exit` on `cave-shore`, and the same two on `keep-spawn-hall`. Anchors that exist on several members of one pool (`anchor/npc-stand`, `anchor/objective`) are not used at all.

## Dramaturgy

**Act 1 — the shore.** The party lands on the stair in the dark, with the sea at their backs and no lamp above them. Maren is the first thing they meet and she is not pleased to be met. She wants one thing and says so flatly: oil, and somebody to carry it up, because she is not going up that stair again.

**Act 2 — the climb.** The oil is in the rocks where the tide dragged the cask. Carrying it across is the crossing: the party goes up and Maren does not. The tower is lit and empty and wrong, and the lamp room at the top is the last room in the delve. Lighting the lamp ends it.

## Quest chain

| quest | act | area | what it is |
|---|---|---|---|
| `quest/the-empty-jar` | 1 | `area/shore` | find Maren, hear why the Tidewatch is dark |
| `quest/what-the-tide-left` | 1 | `area/shore` | recover the cask of lamp oil from the rocks |
| `quest/the-dark-lamp` | 2 | `area/tower` | climb and light the lamp — the finale |

No branch points, no optional quests, no endings other than the one.

**The finale is an AND-join, and it is what makes this a two-player delve.** The seaward window is shuttered and the shutter is wound from a chain in the entry hall at the foot of the climb, four floors below the lamp. So `obj/free-the-shutter` happens at the bottom and `obj/reach-the-lamp-room` at the top, and `obj/light-the-lamp` waits on both: one warden opens the window, the other is standing at the lamp with the jar when it opens. `min_players: 2` is refused without exactly this (`DW0358`), and the refusal is right — a delve billed for two that one body walks end to end is billed wrong.

The second arm is a `reach-anchor` rather than a second `interact` because both would stand on `anchor/exit` and their interaction boxes would be coincident, which is `DW0878`: the client would resolve the click by entity iteration order and one beat would silently stop firing.

## The world

`horizon: "ocean"` — the pinned water superflat, sea level 62, which is the coast this delve is named after; `boundary: {}` because an infinite swimmable sea with no return rule lets a player wander off the map (`DW0320`). `min_players: 2`. The shore area declares `lighting` with a lantern fixture at `min_light: 7`, because a cave pool assembled at night on an ocean horizon is not a place the tide stair can be read in; the tower's pool members are all measured lit and declare nothing.
