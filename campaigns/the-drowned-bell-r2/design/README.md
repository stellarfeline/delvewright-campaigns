# The Drowned Bell — design record

`concept/` holds the eight approved reference images, one per zone, in the
player's ascent order. **They are the campaign's starting point and its only
inherited material.** Everything else is authored from them.

## The approved set

Approved by the owner in conversation, **2026-08-08**. These are the approved
names; no later document uses any other.

| zone | file | name |
|---|---|---|
| Z0 | `concept/z0-barrow-shore.jpg`  | 冢泽潮滩 |
| Z1 | `concept/z1-cliff-road.jpg`    | 崖道 |
| Z2 | `concept/z2-gatehouse.jpg`     | 门楼 |
| Z3 | `concept/z3-drowned-ward.jpg`  | 下沉外庭 |
| Z4 | `concept/z4-chapel-ward.jpg`   | 礼拜堂中庭 |
| Z5 | `concept/z5-hall-keep.jpg`     | 大厅与主楼 |
| Z6 | `concept/z6-cistern-deep.jpg`  | 深蓄水池 |
| Z7 | `concept/z7-bell-tower.jpg`    | 钟塔 |

These are **reference images**: concept art for the design, drawn before any
geometry existed. They are not renders, they are not shipped in a delve, and no
delve byte depends on them.

## The design

| file | holds |
|---|---|
| `story.md` | the place, the bell, what happened, what the player is, the endings |
| `beats.md` | the beat sheet Z0→Z7, every beat naming the image element it is built on |
| `quests.md` | the quest graph: critical path, optional strands, gates, shortcuts, the one branch |
| `tide.md` | the sea as one moving plane: levels, elevations, the four steps, what each changes, and the anti-softlock audit |
| `cast.md` | the five speaking characters, what they want, and their written dialogue |
| `encounters.md` | the fights by intent and role, and the five first-encounter kills |

## The order, and it is not advisory

**Read `design/` before authoring anything.** A zone program, a massing
candidate, a prefab, a scene, or a line of DSL is authored *from* the image for
its zone and is judged *against* it. A round that asks the owner to choose
presents the choice beside that image, under the approved name, saying which
element of the image the thing on offer corresponds to. **A round that cannot
say that is not ready to ask.**

## What is NOT inherited

`archive/bell-remake-r1-abandoned` (content repo) and `archive/bell-engine-r1`
(engine repo) hold the abandoned first round. **Neither is a source.** Nothing
in this campaign is derived from them, and a later round that reaches for them
for a design decision is reintroducing the defect that ended that round.

Its zone programs were written before the design gate; its massing candidates
were authored without these images; three zones were renamed away from the
approved names. The engine primitives it produced are general and survive on
their own merits, because a primitive may not be bound to one campaign — but
every design decision in it is void.
