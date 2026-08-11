# The Drowned Bell — design record

The campaign's design material lives here, beside the campaign it belongs to.
`concept/` holds the eight approved reference images, one per zone, in the
player's ascent order. Everything downstream of the design gate — the zone
programs, the massing candidates, the DSL — answers to these.

## The approved set

Approved by the owner in conversation, **2026-08-08**. The names below are the
approved names and the only ones any later document uses.

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

These are **reference images**: concept art for the design, drawn before the
geometry existed. They are not renders of anything, they are not shipped in a
delve, and no delve byte depends on them — so ADR-0013's asset licensing, which
governs what reaches a player, does not reach them. They are generation-time
material that belongs to the campaign, which is why they live in the campaign's
own directory rather than in a scratch folder.

## What a later round owes them

A massing candidate, a prefab, or a scene is judged **against the image for its
zone**. When a round asks the owner to choose, the choice is presented beside
that image, under the approved name, saying which element of the image the thing
on offer corresponds to. A round that cannot say that is not ready to ask.

## Why they are stored here

`tools/refimg.py` writes to a gitignored working directory, which is right for
a draft and wrong for an approved one. An approval that lives only in a
generated page is bound to nothing: the design gate ran, the owner said yes, and
the next round authored its candidates without ever seeing what she had
approved. The images are stored here so that reading the campaign is enough.
