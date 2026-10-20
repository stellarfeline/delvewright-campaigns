# The Wake

> **Requires delve engine 0.55.0 or newer** — last verified with delvec 1.13.0 on Minecraft Java 1.21.11.

Below the keep wall, on an islet the tide leaves twice a day, is a field of
graves. Wren Ashlaw read the tide for the keep, and drowned reading it. Her
people have stood among the graves since noon. The party comes ashore at low
water with her body, carried up the road by strangers, and by the field's
custom whoever carries the body is owed the last word on where she goes.

A demo level of about fifteen minutes, for one to four players. No combat.

## Who you will meet

- **Hallis Ashlaw**, her brother, who has kept the shore fire since they
  carried her up and has not once looked up the field.
- **Sedge**, the barrow-warden, who has cut every grave in this field with her
  own hands.

## Classes

- **Pallbearer** — you took the front of the plank on the road up, and nobody
  has offered to take it back. A wake-lamp, a mourning coat, some bread.
- **Reed-Piper** — the field expects a note over the cut, and you carry the
  horn that makes one.
- **Grave-Child** — you carry the flowers, because somebody young always does.

## Playing it

Start the server, then in the Minecraft Java client at the version the marker
above names: Multiplayer → Direct Connect → `localhost:25565`. Accept the
resource pack when the server offers it.

---

## For the owner: what to look for

This level is where staging (spec-0014) is looked at in the game: bodies the
engine summons on a timeline, walks across the field and removes, a rite told
as a timed run of lines and sounds, and the camera cutting away to show it. The
machine has proved that every walk has a route for the body that takes it, that
every timeline step lands in order, and that each of the two answers at the fire
reaches its own ending; the bot has played the level through both answers. What
the machine cannot say is how any of it **reads**. Allow about fifteen minutes a
walk; walk it twice, and at the fire give the other answer the second time.

1. **The field fills behind you.** Talk to the brother at the fire first. As
   you turn up the field, the bell strikes and the mourners appear one by one
   over about seven seconds. Does the field read as filling up, or as bodies
   popping into place?
2. **The bodies walk.** When the warden starts the rite, three people walk at
   once: the lamp-bearer down from the gate, the child in from the dyke, the
   warden along the grave row. Watch their legs and their facing: does each one
   walk, face the way it is going, and stop where it should, without sliding,
   jumping a cell or walking through a gravestone?
3. **The cameras.** Three times the view leaves you: a wide shot coming down
   over the field when you reach the banner, a shot running beside the
   lamp-bearer during the rite, and one at the end. Is the moving body in the
   frame for the whole shot? Is your own party standing in the wide shot where
   you stood? Do you come back to where you were?
4. **The rite's pacing.** The rite is three lines and two bells over about
   thirteen seconds. Is there time to read each line before the next arrives?
5. **The body.** The dead woman is an armour stand in a brown shroud with her
   name over it. Does it read as the dead being carried, or as an armour stand
   walking? This is the one we most want your eye on.
6. **The last walk, both times.** At the end the body goes from the banner to
   wherever you sent it. On both walks it should start from the banner and walk
   the whole way, with no jump at the start. The longer of the two walks runs
   the length of the field.
7. **Faces and gaze.** The warden and the brother wear their own faces and turn
   to whoever comes close. The mourners do not turn. Does any of that break the
   mood of a funeral?

Nothing in the level can hurt you; the stones along the waterline keep you out
of the sea.
