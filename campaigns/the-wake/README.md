# The Wake

> *"They are waiting on a word, and by the custom the word is yours, because you carried her up the road."*

A short delve for one evening: a walled field of graves above the sea, a body on
a plank, and a family that cannot say where she should go.

![The barrow field above the water, with the black banner at its heart](media/barrow-field.jpg)

| | |
|---|---|
| **Players** | 1–4 |
| **Playtime** | ~15 minutes |
| **Classes** | Three — chosen when you come ashore |
| **Languages** | English, 简体中文 (`zh-cn`) |
| **Combat** | None. Nothing in this delve can hurt you. |
| **Licence** | CC BY-SA 4.0 |

## The story so far

Wren Ashlaw read the tide for the keep on the headland. Thirty years of it —
when the causeway would dry, when the fishing boats could come in past the bar,
which mornings the water was lying about how calm it was. She was better at it
than anybody on this coast, which is the part her brother cannot get past.

She drowned reading it, eight days ago, and the sea kept her until yesterday.

You are strangers on this coast. You came in at low water with her on a plank
between you, because you were the ones on the road when the road needed
somebody, and by the time you set her down under the black banner in the middle
of the barrow field, the whole field had been standing there since noon waiting
for exactly that.

![Low water, the shore fire, and the grave road up into the field](media/shore-landing.jpg)

The wake can begin now. It cannot end, because nobody will say the word.

The field's custom is old and short: the dead go to the ground, or the dead go
to the water, and the word belongs to the family. Wren left no instruction. Her
brother has been at the shore fire since they brought her up and has not once
turned to look north. The barrow-warden opened a grave at first light without
being asked, and has an opinion she will give you in about eleven words.

By the same custom, the word passes to whoever carried the body. This evening,
that is you.

## Who you will meet

**Sedge, the Barrow-Warden.** She keeps this field and has done for a long time.
Ask her about a person and she will answer about soil, or weather, or how long
the clay holds under two spades of sand. It is not evasion — it is the only
register she has for this, and she uses it kindly. She had the cut open before
anyone thought to ask her for it, and she does not think that needs explaining.

**Hallis Ashlaw.** Wren's brother. He talks the way people talk when stopping
would be worse: too much, then an apology for it, then a sentence that runs out
partway. He knows the word is his and he knows he is not going to say it, and he
is not pretending otherwise. He is grateful to you in a way that is difficult to
be in the room for.

**The field.** A lamp-bearer comes down from the keep gate with the wake-lamp
lit. A woman who has not left the plank since morning. An elder at his own
family's barrow on the west flank, and a child on the east who comes in only so
far and stops. None of them will ask you for anything. All of them are waiting.

## The classes

**Pallbearer** — you took the front of the plank on the road up, and nobody has
offered to take it back. You carry the wake-lamp.

**Reed-Piper** — the field expects one note over the cut, and you are the one
carrying something that makes one.

**Grave-Child** — you carry the flowers, because somebody young always does, and
nobody here asked how old you were.

## Playing it

Build and run the delve from the repository root:

```
delvec build campaigns/the-wake -o campaigns/the-wake/out
EULA=TRUE docker compose -f validation/compose.yaml --profile play up
```

For the Chinese text, build with `--lang zh-cn`.

There is nothing to fight and nothing to solve. Walk up the field, stand for the
rite, and when you are asked, answer.
