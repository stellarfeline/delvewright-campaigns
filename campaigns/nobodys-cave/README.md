# Nobody's Cave

> *"You are in a great hurry to be liked, little one. Slow down. There is time.
> The stone is not going anywhere tonight, and neither are you."*

A single-player delve for one sitting — bronze-age firelight, salt wind, and a
conversation you cannot afford to lose.

| | |
|---|---|
| **Players** | 1 |
| **Playtime** | ~20 minutes |
| **Class** | Fixed — no selection this time |
| **Languages** | English, 简体中文 (`zh-cn`) |
| **Source** | Homer, *Odyssey* Book 9 — public domain |
| **Licence** | CC BY-SA 4.0 |

## The story so far

Troy fell ten years ago. The horse at the end was your idea, and everyone has
heard the song by now — but the song stops there, because you still are not home.
The sea keeps handing you islands instead of Ithaca.

This one came out of the fog with no harbour, no smoke, no ploughed field and no
boundary stone. Nobody has ever cut a furrow here. Up the path from the beach
there is a cave with cheese racked to the roof, lambs penned and sorted by age,
and milk pails still wet — an empty house that is very obviously not empty, only
temporarily unattended.

Your second-in-command wants to take what you can carry and be off the sand
before dark. He is almost certainly right. He usually is.

You want to meet whoever milks them.

## Who you will meet

**Odysseus of Ithaca** — you. A king nine years overdue, famous for winning fights
by not having them. You have a short sword, a torch, and a skin of wine carried up
from the ship.

**Eurylochus** — your second, and your wife's brother, which is the only reason he
is allowed to talk to you the way he does. Blunt, unflattering, and given to
counting things aloud: days, jars, men. He argues to your face and then does
exactly as he is told.

**Perimedes** — the quiet hand who does the frightening job before anyone has
finished asking. He speaks in nouns and verbs, reports what he can see, and stops.
He shipped out of Ithaca alongside a man named Antiphus; they drew the same oar
for nine years.

**Polyphemus** — a shepherd, of a sort. Poseidon's son, alone on this island with
his flock since before anyone thought of building ships. He is enormous and
unhurried, he speaks plainly and without cruelty, and he has never in his life had
to ask anyone's permission for anything. He will talk to you about guests, and
gifts, and law, in the tone of a man reciting rules he owns rather than obeys.

He is monstrous. He is also, if you let him talk, a little pitiable — and knowing
which of those two things you are dealing with, and when, is most of this delve.

## What kind of delve this is

Three pillars, in the proportions the source demands: it is mostly **talking**,
partly **a puzzle you build with your hands**, and once — briefly — a matter of
getting somewhere without being caught. There is no grinding, no mining, no
levelling, and remarkably little swinging of the sword you were issued.

Book 9 is not a story about beating something stronger than you. Bear that in
mind when you are handed the option to try.

## Play it

```sh
# play (English)
EULA=TRUE docker compose -f validation/compose.yaml --profile play up

# play with creator notes captured
EULA=TRUE CREATOR_NAME=<your mc name> \
  docker compose -f validation/compose.yaml --profile playtest up
```

Build from source with the main repo's compiler:

```sh
delvec build campaigns/nobodys-cave -o out/            # English
delvec build campaigns/nobodys-cave --lang zh-cn -o out-zh/   # 简体中文
```

---

*Adaptation notes, the decisions behind this campaign, and the known limits of the
current DSL are recorded in `GENERATION.md` — that file discusses the plot freely
and is not spoiler-safe.*
