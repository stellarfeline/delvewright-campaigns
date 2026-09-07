# Tide Mill

*A short delve for 1–4 players. About 15 minutes.*

Sedgewick Mill does not grind on wind or on a stream. It grinds on the sea.

The flood fills the pond behind the sea wall twice a day; on the ebb the miller
lets the water back out down a stone race, and the race turns the wheel. Three
sluices stand along that race, and they are not levers anybody pulls. They open
and shut on the sea's own count — the same count they have kept since the keep
above them still had a garrison, and nobody alive has managed to change it.

This ebb the brake pin sheared.

The wheel is running with nothing holding it, and it will walk the mill off its
footings before the pond is empty. The brake stands at the far end of the race,
past all three sluices, under the sea wall. The miller cannot run them any more.

You can.

## The mill yard

**Corrin Sedge** keeps Sedgewick Mill, as his mother did. He counts under his
breath — sluices, sacks, tides — and he has not stopped counting since the pin
went. He will give you the count for every gate on the race, plainly and without
decoration, including the last one, which he will tell you has killed people.

He is the only person you will meet. Everything after him is water and stone.

## Classes

- **Race-walker** — sure-footed on wet stone. You have walked a mill race in the
  dark before, and you have never yet gone into one. Carries Sedge's tide-clock.
- **Sluice-keeper** — you read water. Where the race swells and where it goes
  slack tells you what the gate ahead is about to do. Carries the marker lamp.

Both are given to you at the start; there is nothing to grind and nothing to
craft.

## What this delve is about

One thing: **reading a gate instead of gambling on it.** Stand off it. Watch it
go round once. Then walk. The mill will give you three chances to learn that, and
it is generous with the first one.

## Playing it

Build the delve, then join a locally hosted server:

```sh
# English
delvec build campaigns/tide-mill -o validation/delve-output

# 简体中文
delvec build campaigns/tide-mill -o validation/delve-output --lang zh-cn
```

```sh
EULA=TRUE docker compose -f validation/compose.yaml --profile play up
```

To leave playtest notes as you go (`/trigger dw.note` in game):

```sh
CREATOR_NAME=<your minecraft name> \
  EULA=TRUE docker compose -f validation/compose.yaml --profile playtest up
```
