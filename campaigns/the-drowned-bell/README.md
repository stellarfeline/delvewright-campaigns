# The Drowned Bell

> **Requires delve engine `delvec` ≥ 0.1.0 · Minecraft 1.21.11 · campaign format 0.8**

*A souls delve for 1–4 players. About 2–3 hours. It expects to kill you.*

The bell of Vesper Keep used to ring the tide out twice a day, and the causeway
ran dry, and the pilgrims walked across. Then somebody cut the bell down and
drowned it in the keep's own cistern. The wardens hollowed at their posts. The
sea stopped listening.

A ferrywoman has landed you on the barrow shore at low water.

Climb the keep. Raise what was drowned. Ring it.

## What kind of delve this is

Three rules, and the keep keeps all three:

- **Death teaches.** Dying is cheap and it is supposed to happen. Rest at a fire
  and it holds your place. What it does not do is hold your ground: everything
  the keep has already sent against you stands back up when you do.
- **Shortcuts are earned.** Every long way round has a door on the far side of
  it, barred from the wrong end. Open it from behind and you never walk that way
  again. The keep folds up as you learn it.
- **Nothing is explained twice.** Warnings arrive once, as something you saw, or
  as a remark somebody made while sweeping. Look up before you walk in. Watch a
  thing go round once before you step past it.

There is no grinding, no crafting, no levelling. You are given everything you
will ever have in the first two minutes.

## The fires

Three fires, and they are the whole safety net. Sitting at one lets you **rest
and save** — your place is kept, your stew is refilled, and the keep re-arms —
or **save only**, if you would rather not wake anything up. You will learn which
one you meant.

## Who you meet

**The Ferrywoman** beaches her boat at the tide line and will not be hurried.
She has ferried worse than you. She still keeps the old crossing schedule for a
tide that no longer comes, and she would like to hear the bell once more before
her arms give out.

**The Sexton** sweeps a hearth he can no longer light, in a chapel across the
courtyard. He greets you as though you were expected some years ago. He gives
warnings the way other people mention the weather.

**The Barrow Warden** kneels among the graves with its sword point-down. It does
not patrol and it does not chase. The ground on both sides of it is wide and
open, and going around it costs you nothing at all.

That is a real choice. It is not a hint.

## Classes

Pick one at the fire on the shore. All four are given complete — armour, weapon,
and a **Hearth Stew** flask that refills every time you rest.

- **The Last Warden** — sword, shield, and the patience to let the enemy make
  the first mistake. The keep was built by people who fought the way you fight,
  which is why you can read its dangers where others read decoration. Three
  stews, because reach is your language and mercy toward yourself is rationed.
- **The Steeple Archer** — you learned the trade shooting gulls off the bell
  towers of a living coast. Nothing here survives being seen first, and you are
  very good at seeing first. Two stews; you plan on needing fewer.
- **The Lampbearer** — you walked ahead of pilgrims with a light, back when
  there were pilgrims. Most of what kills people in the dark was visible the
  whole time. You set torches in the corners you have cleared so nobody clears
  them twice.
- **The Underminer** — every keep is two keeps: the one on the plans, and the
  one water and neglect have been quietly building underneath. You worked the
  second one. A stone thrown into the right pool has started more fights on your
  terms than any blade.

## Playing it

Build the delve, then join a locally hosted server:

```sh
# English
delvec build campaigns/the-drowned-bell -o validation/delve-output

# 简体中文
delvec build campaigns/the-drowned-bell -o validation/delve-output --lang zh-cn
```

```sh
EULA=TRUE docker compose -f validation/compose.yaml --profile play up
```

Join from a vanilla **1.21.11** client. It is night, and it is storming, and
that is on purpose.

To leave playtest notes as you go (`/trigger dw.note` in game):

```sh
CREATOR_NAME=<your minecraft name> \
  EULA=TRUE docker compose -f validation/compose.yaml --profile playtest up
```
